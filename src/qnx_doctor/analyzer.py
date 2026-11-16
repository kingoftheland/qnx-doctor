"""Analyzer — orchestrates the 22 QNX Doctor checks over a project.

Pipeline: C files -> c_parser (functions / calls / loops) -> RT + QX
rules; buildfiles -> buildfile_parser -> BF rules. Findings are scored
0-100 with a grade (A-F) and an exit-code-friendly summary.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

from .buildfile_parser import ARCH_STARTUP_PREFIX, parse_buildfile
from .c_parser import (
    BLOCKING_CALLS,
    HEAP_CALLS,
    IO_CALLS,
    CallSite,
    CFile,
    Function,
    parse_c_file,
)
from .rules import RULES, SEVERITY_ORDER, SEVERITY_WEIGHTS, get_rule

VERSION = "0.1.0"
TOOL = "qnx-doctor"
QNX_VERSION = "8.0"

C_EXTS = {".c", ".h", ".cpp", ".cc", ".cxx", ".hpp"}
BUILDFILE_NAMES = {"buildfile", "image.build"}
BUILDFILE_EXTS = {".build", ".bld"}

RT_POLICIES = {"SCHED_FIFO", "SCHED_RR"}

# Kernel calls whose return value must be checked (RT-06).
UNCHECKED_KERNEL_CALLS = {
    "ChannelCreate", "ConnectAttach", "MsgSend", "MsgSendv",
    "name_attach", "resmgr_attach", "InterruptAttach",
    "InterruptAttachEvent", "mq_open", "shm_open",
}


@dataclass
class Finding:
    rule_id: str
    severity: str
    file: str
    line: int
    column: int
    message: str
    code_snippet: str
    recommendation: str
    references: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.rule_id,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "column": self.column,
            "message": self.message,
            "code_snippet": self.code_snippet,
            "recommendation": self.recommendation,
            "references": self.references,
        }


@dataclass
class Report:
    target: str
    score: int
    grade: str
    summary: dict[str, int]
    findings: list[Finding]
    files_scanned: list[str]

    def to_dict(self) -> dict:
        return {
            "tool": TOOL,
            "version": VERSION,
            "target": self.target,
            "qnx_version": QNX_VERSION,
            "score": self.score,
            "grade": self.grade,
            "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings],
            "files_scanned": self.files_scanned,
        }


# ---------------------------------------------------------------- helpers
def _split_args(args: str) -> list[str]:
    """Split a call argument list on top-level commas."""
    out, depth, cur = [], 0, []
    for ch in args:
        if ch in "([":
            depth += 1
            cur.append(ch)
        elif ch in ")]":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur).strip())
    return out


def _bare(arg: str) -> str:
    return arg.strip().lstrip("&").strip()


def _snippet(cfile: CFile, line: int) -> str:
    if 0 < line <= len(cfile.lines):
        return cfile.lines[line - 1].strip()
    return ""


def _is_checked(cfile: CFile, call: CallSite) -> bool:
    """Heuristic: is the return value of this call checked?

    Checked if the call sits inside an if/while/assert/return statement,
    or if an assignment `x = Call(...)` is followed within 5 lines by a
    test on x (== -1, < 0, != -1, or if (x ...)).
    """
    stmt = call.stmt
    if re.search(r"\b(if|while|assert|return)\b", stmt):
        return True
    m = re.match(r"\s*(?:[A-Za-z_][\w\s\*]*?\s+)?([A-Za-z_]\w*)\s*=\s*[^=]", stmt)
    if m and call.name in stmt:
        var = m.group(1)
        check_re = re.compile(
            rf"\b{re.escape(var)}\s*(==|!=|<=|<)\s*-1\b"
            rf"|\bif\s*\(\s*!?\s*{re.escape(var)}\b"
            rf"|\b{re.escape(var)}\s*<\s*0\b"
        )
        for ln in range(call.line, min(call.line + 5, len(cfile.lines))):
            if check_re.search(cfile.lines[ln]):
                return True
    return False


# ---------------------------------------------------------------- C analysis
class _CProject:
    """Cross-file view: thread attributes, RT routines, call graph."""

    def __init__(self, cfiles: list[CFile]):
        self.cfiles = cfiles
        self.functions: dict[str, Function] = {}
        for cf in cfiles:
            self.functions.update(cf.functions)
        self.attr_policy: dict[str, str] = {}
        self.attr_explicit: set[str] = set()
        self.attr_protocol: set[str] = set()
        self.attr_priority: dict[str, int] = {}   # attr var -> priority
        self.attr_priority_set: set[str] = set()  # attr var with any priority assigned (incl. non-literal)
        self.sp_priority: dict[str, int] = {}     # struct var -> priority
        self.sp_assigned: set[str] = set()        # struct var with any sched_priority assignment
        self.sp_to_attr: dict[str, str] = {}      # struct var -> attr var
        self.prio_assignments: list[tuple[str, int, int, str]] = []  # (var, val, line, file)
        self.create_sites: list[tuple[CFile, CallSite, str | None, str | None]] = []
        self.rt_routines: set[str] = set()
        self._collect()

    def _collect(self) -> None:
        for cf in self.cfiles:
            # sched_priority assignments anywhere in the file.
            # The value may be a literal (20) or a variable/expression
            # (prio); literals feed RT-11/RT-08, any assignment counts
            # as "priority set" for RT-03.
            for ln, line in enumerate(cf.lines, start=1):
                m = re.search(r"([A-Za-z_]\w*)\s*(?:\.|->)\s*sched_priority\s*=\s*([^\s;]+)", line)
                if m:
                    self.sp_assigned.add(m.group(1))
                    if m.group(2).isdigit():
                        self.sp_priority[m.group(1)] = int(m.group(2))
                        self.prio_assignments.append(
                            (m.group(1), int(m.group(2)), ln, cf.path))
            for fn in cf.functions.values():
                for call in fn.calls:
                    args = _split_args(call.args)
                    if call.name == "pthread_attr_setschedpolicy" and len(args) >= 2:
                        self.attr_policy[_bare(args[0])] = _bare(args[1])
                    elif call.name == "pthread_attr_setinheritsched" and len(args) >= 2:
                        if "PTHREAD_EXPLICIT_SCHED" in args[1]:
                            self.attr_explicit.add(_bare(args[0]))
                    elif call.name == "pthread_attr_setschedparam" and len(args) >= 2:
                        self.sp_to_attr[_bare(args[1])] = _bare(args[0])
                    elif call.name == "pthread_mutexattr_setprotocol" and len(args) >= 2:
                        if "PTHREAD_PRIO_INHERIT" in args[1] or "PTHREAD_PRIO_PROTECT" in args[1]:
                            self.attr_protocol.add(_bare(args[0]))
                    elif call.name == "pthread_create" and len(args) >= 3:
                        attr = None if _bare(args[1]) == "NULL" else _bare(args[1])
                        self.create_sites.append((cf, call, attr, _bare(args[2])))
                    elif call.name == "pthread_setschedparam" and len(args) >= 2:
                        if _bare(args[1]) in RT_POLICIES:
                            self.rt_routines.add(fn.name)
        for sp_var, attr_var in self.sp_to_attr.items():
            if sp_var in self.sp_priority:
                self.attr_priority[attr_var] = self.sp_priority[sp_var]
            if sp_var in self.sp_assigned:
                self.attr_priority_set.add(attr_var)
        for _, call, attr, routine in self.create_sites:
            if attr and self.attr_policy.get(attr) in RT_POLICIES:
                self.rt_routines.add(routine)

    def reachable(self, roots: set[str]) -> set[str]:
        """Transitive callees of the given functions (incl. themselves)."""
        seen, stack = set(), list(roots)
        while stack:
            name = stack.pop()
            if name in seen:
                continue
            seen.add(name)
            fn = self.functions.get(name)
            if fn:
                stack.extend(c.name for c in fn.calls)
        return seen

    def priorities(self) -> list[int]:
        vals = list(self.attr_priority.values())
        # Direct pthread_setschedparam(..., &sp) priorities.
        for cf in self.cfiles:
            for fn in cf.functions.values():
                for call in fn.calls_named("pthread_setschedparam"):
                    args = _split_args(call.args)
                    if len(args) >= 3:
                        sp = _bare(args[2])
                        if sp in self.sp_priority:
                            vals.append(self.sp_priority[sp])
        return vals


def _finding(rule_id: str, rel: str, line: int, column: int,
             message: str, snippet: str) -> Finding:
    rule = get_rule(rule_id)
    assert rule is not None
    return Finding(
        rule_id=rule.id, severity=rule.severity, file=rel, line=line,
        column=column, message=message, code_snippet=snippet,
        recommendation=rule.recommendation,
        references=list(rule.references),
    )


def analyze_c_file(cf: CFile, proj: _CProject, rel_of) -> list[Finding]:
    findings: list[Finding] = []
    rel = rel_of(cf.path)
    rt_reachable = proj.reachable(proj.rt_routines)

    for fn in cf.functions.values():
        is_rt = fn.name in rt_reachable
        for call in fn.calls:
            # -- RT-04: blocking call inside an ISR handler --------------
            # (handled below via InterruptAttach sites; skip here)
            # -- RT-06: unchecked QNX kernel call ------------------------
            if call.name in UNCHECKED_KERNEL_CALLS and not _is_checked(cf, call):
                findings.append(_finding(
                    "RT-06", rel, call.line, call.column,
                    f"unchecked {call.name}() return value",
                    _snippet(cf, call.line)))
            # -- RT-07: MsgSend without timeout --------------------------
            if call.name in ("MsgSend", "MsgSendv") and not fn.has_call("TimerTimeout"):
                findings.append(_finding(
                    "RT-07", rel, call.line, call.column,
                    f"{call.name}() without TimerTimeout() — client can block forever",
                    _snippet(cf, call.line)))
            # -- RT-01 / RT-05 / RT-09: only on the RT path --------------
            if is_rt and "init" not in fn.name.lower():
                if call.name in HEAP_CALLS:
                    findings.append(_finding(
                        "RT-01", rel, call.line, call.column,
                        f"heap allocation {call.name}() in real-time thread "
                        f"'{fn.name}'",
                        _snippet(cf, call.line)))
                    if call.name in ("malloc", "calloc", "realloc") and fn.in_loop(call.line):
                        findings.append(_finding(
                            "RT-05", rel, call.line, call.column,
                            f"{call.name}() inside unbounded loop of real-time "
                            f"thread '{fn.name}'",
                            _snippet(cf, call.line)))
                if call.name in IO_CALLS:
                    findings.append(_finding(
                        "RT-09", rel, call.line, call.column,
                        f"blocking I/O {call.name}() in real-time thread "
                        f"'{fn.name}' — use slog2f() or a ring buffer",
                        _snippet(cf, call.line)))
            # -- QX-02: PPS open ------------------------------------------
            if call.name == "open" and ("/pps" in call.args or "/fs/pps" in call.args):
                findings.append(_finding(
                    "QX-02", rel, call.line, call.column,
                    "PPS object opened without checking that the pps service "
                    "is running",
                    _snippet(cf, call.line)))
            # -- QX-03: resmgr_attach (info) ------------------------------
            if call.name == "resmgr_attach":
                findings.append(_finding(
                    "QX-03", rel, call.line, call.column,
                    "resmgr_attach() requires root privileges in the image",
                    _snippet(cf, call.line)))
            # -- QX-05: ThreadCtl IO_PRIV unchecked -----------------------
            if call.name == "ThreadCtl" and "_NTO_TCTL_IO" in call.args \
                    and not _is_checked(cf, call):
                findings.append(_finding(
                    "QX-05", rel, call.line, call.column,
                    "unchecked ThreadCtl(_NTO_TCTL_IO_PRIV, ...) return value",
                    _snippet(cf, call.line)))

        # -- RT-04: blocking calls inside InterruptAttach handlers -------
        for call in fn.calls_named("InterruptAttach"):
            args = _split_args(call.args)
            if len(args) >= 2:
                handler = _bare(args[1])
                hfn = proj.functions.get(handler)
                if hfn:
                    hcf = next(
                        (c for c in proj.cfiles if handler in c.functions),
                        cf)
                    hrel = rel_of(hcf.path)
                    for hc in hfn.calls:
                        if hc.name in BLOCKING_CALLS:
                            findings.append(_finding(
                                "RT-04", hrel, hc.line, hc.column,
                                f"blocking {hc.name}() inside ISR handler "
                                f"'{handler}'",
                                _snippet(hcf, hc.line)))

    # -- RT-02: mutex without priority protocol ---------------------------
    for fn in cf.functions.values():
        for call in fn.calls_named("pthread_mutex_init"):
            args = _split_args(call.args)
            attr = _bare(args[1]) if len(args) >= 2 else "NULL"
            if attr == "NULL" or attr not in proj.attr_protocol:
                findings.append(_finding(
                    "RT-02", rel, call.line, call.column,
                    "pthread_mutex_init() without priority inheritance/ceiling "
                    "protocol (NULL or default attributes)",
                    _snippet(cf, call.line)))

    # -- RT-03: pthread_create without explicit scheduling ----------------
    for _, call, attr, routine in proj.create_sites:
        if call.line < 1:
            continue
        # Only report a create site once, in the file that contains it.
        if not any(call is c for f in cf.functions.values() for c in f.calls):
            continue
        if attr is None:
            reason = "NULL attributes — thread inherits creator scheduling"
        elif attr not in proj.attr_explicit:
            reason = (f"attribute '{attr}' never set to "
                      "PTHREAD_EXPLICIT_SCHED")
        elif attr not in proj.attr_policy:
            reason = f"attribute '{attr}' has no schedpolicy set"
        elif attr not in proj.attr_priority and attr not in proj.attr_priority_set:
            reason = (f"attribute '{attr}' sets policy "
                      f"{proj.attr_policy[attr]} but no sched_priority")
        else:
            continue
        findings.append(_finding(
            "RT-03", rel, call.line, call.column,
            f"pthread_create() for '{routine}' without explicit scheduling: "
            f"{reason}",
            _snippet(cf, call.line)))

    # -- RT-11: sched_priority = 0 ----------------------------------------
    for var, val, ln, _path in proj.prio_assignments:
        if val == 0 and _path == cf.path:
            findings.append(_finding(
                "RT-11", rel, ln, 1,
                f"sched_priority = 0 for '{var}' — priority 0 is IDLE in QNX",
                _snippet(cf, ln)))

    # -- QX-01: ChannelCreate(0) in a server that handles pulses ---------
    has_pulse = any(
        c.name == "MsgReceivePulse"
        for fn in cf.functions.values() for c in fn.calls)
    if has_pulse:
        for fn in cf.functions.values():
            for call in fn.calls_named("ChannelCreate"):
                if _bare(_split_args(call.args)[0]) == "0" if call.args else False:
                    findings.append(_finding(
                        "QX-01", rel, call.line, call.column,
                        "ChannelCreate(0) in a server that handles pulses — "
                        "consider ChannelCreatePulsePool()",
                        _snippet(cf, call.line)))

    # -- QX-04: name_attach without name_detach ---------------------------
    attached = [c for fn in cf.functions.values()
                for c in fn.calls_named("name_attach")]
    detached = any(
        c.name == "name_detach"
        for fn in cf.functions.values() for c in fn.calls)
    if attached and not detached:
        call = attached[0]
        findings.append(_finding(
            "QX-04", rel, call.line, call.column,
            "name_attach() without a matching name_detach() — pathname "
            "entry leaks on exit",
            _snippet(cf, call.line)))

    return findings


def analyze_c_project(cfiles: list[CFile], rel_of) -> list[Finding]:
    proj = _CProject(cfiles)
    findings: list[Finding] = []
    for cf in cfiles:
        findings.extend(analyze_c_file(cf, proj, rel_of))

    # -- RT-08: flat priority (project level, once) -----------------------
    if proj.create_sites:
        prios = proj.priorities()
        first = cfiles[0]
        rel = rel_of(first.path)
        if not prios:
            findings.append(_finding(
                "RT-08", rel, 1, 1,
                "no explicit thread priorities (no pthread_setschedparam) — "
                "all threads run at the same priority",
                _snippet(first, 1)))
        elif len(set(prios)) == 1:
            findings.append(_finding(
                "RT-08", rel, 1, 1,
                f"all threads share sched_priority {prios[0]} — no priority "
                "differentiation between RT and background work",
                _snippet(first, 1)))

    # -- RT-12: RT thread without mlockall --------------------------------
    for routine in sorted(proj.rt_routines):
        fn = proj.functions.get(routine)
        if fn is None:
            continue
        reachable = proj.reachable({routine})
        has_mlock = any(
            c.name == "mlockall"
            for name in reachable
            if name in proj.functions
            for c in proj.functions[name].calls)
        if not has_mlock:
            cf = next((c for c in cfiles if routine in c.functions), cfiles[0])
            findings.append(_finding(
                "RT-12", rel_of(cf.path), fn.start_line, 1,
                f"real-time thread '{routine}' runs without "
                "mlockall(MCL_CURRENT | MCL_FUTURE)",
                _snippet(cf, fn.start_line)))
    return findings


# ---------------------------------------------------------------- buildfile
def analyze_buildfile(path: str, rel: str) -> list[Finding]:
    bf = parse_buildfile(path)
    findings: list[Finding] = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()

    def snippet(ln: int) -> str:
        return lines[ln - 1].strip() if 0 < ln <= len(lines) else ""

    # -- BF-01: missing procnto in bootstrap ------------------------------
    if not bf.bootstraps:
        findings.append(_finding(
            "BF-01", rel, 1, 1,
            "no .bootstrap section — image has no startup/procnto and "
            "cannot boot", snippet(1)))
    elif not bf.has_procnto():
        sec = bf.bootstraps[0]
        findings.append(_finding(
            "BF-01", rel, sec.start_line, 1,
            ".bootstrap section has no procnto — image cannot boot",
            snippet(sec.start_line)))

    # -- BF-02: startup/arch mismatch -------------------------------------
    if bf.virtual_arch:
        expected = ARCH_STARTUP_PREFIX.get(bf.virtual_arch)
        if expected:
            for sec in bf.bootstraps:
                for off, body_line in enumerate(sec.body):
                    m = re.match(r"\s*(startup-[\w\-\.]+)", body_line)
                    if m and not m.group(1).startswith(expected):
                        findings.append(_finding(
                            "BF-02", rel, sec.start_line + off + 1, 1,
                            f"startup binary '{m.group(1)}' does not match "
                            f"virtual={bf.virtual_arch}",
                            snippet(sec.start_line + off + 1)))

    # -- BF-03: script references missing file ----------------------------
    known = {f for f in bf.files}
    for cmd, ln in bf.script_commands:
        base = cmd.split("/")[-1]
        if base not in known:
            findings.append(_finding(
                "BF-03", rel, ln, 1,
                f"script starts '{cmd}' but it is not in the image file list",
                snippet(ln)))

    # -- BF-04: missing libc / ldqnx link ---------------------------------
    if not bf.has_libc():
        findings.append(_finding(
            "BF-04", rel, 1, 1,
            "image has no libc.so and no ldqnx.so.2 link — dynamically "
            "linked binaries cannot run",
            snippet(1)))

    # -- BF-05: session without reopen ------------------------------------
    if bf.script_session_without_reopen():
        ln = bf.script_session_lines[0]
        findings.append(_finding(
            "BF-05", rel, ln, 1,
            "[+session] shell started without a preceding reopen of the "
            "console/serial device",
            snippet(ln)))

    return findings


# ---------------------------------------------------------------- scoring
def score_findings(findings: list[Finding]) -> tuple[int, str]:
    penalty = sum(SEVERITY_WEIGHTS[f.severity] for f in findings)
    score = max(0, 100 - penalty)
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    return score, grade


def summarize(findings: list[Finding]) -> dict[str, int]:
    summary = {sev: 0 for sev in SEVERITY_ORDER}
    for f in findings:
        summary[f.severity] += 1
    summary["total"] = len(findings)
    return summary


def _sort_key(f: Finding):
    return (SEVERITY_ORDER.index(f.severity), f.file, f.line)


# ---------------------------------------------------------------- entry point
def analyze_path(target: str) -> Report:
    """Analyse a file or directory. Raises FileNotFoundError / ValueError."""
    if not os.path.exists(target):
        raise FileNotFoundError(f"path not found: {target}")
    if os.path.isfile(target):
        root = os.path.dirname(os.path.abspath(target))
        candidates = [target]
    else:
        root = os.path.abspath(target)
        candidates = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames
                           if d not in (".git", "__pycache__", ".venv", "venv", "node_modules")]
            for name in sorted(filenames):
                candidates.append(os.path.join(dirpath, name))

    def rel_of(p: str) -> str:
        try:
            return os.path.relpath(p, root)
        except ValueError:
            return os.path.basename(p)

    c_paths, bf_paths, other = [], [], []
    for p in candidates:
        base = os.path.basename(p)
        ext = os.path.splitext(p)[1].lower()
        if ext in C_EXTS:
            c_paths.append(p)
        elif ext in BUILDFILE_EXTS or base.lower() in BUILDFILE_NAMES:
            bf_paths.append(p)
        elif base in ("CMakeLists.txt", "Makefile", "Makefile.qnx"):
            other.append(p)

    findings: list[Finding] = []
    cfiles = [parse_c_file(p) for p in c_paths]
    if cfiles:
        findings.extend(analyze_c_project(cfiles, rel_of))
    for p in bf_paths:
        findings.extend(analyze_buildfile(p, rel_of(p)))

    findings.sort(key=_sort_key)
    score, grade = score_findings(findings)
    scanned = [rel_of(p) for p in c_paths + bf_paths + other]
    return Report(
        target=target,
        score=score,
        grade=grade,
        summary=summarize(findings),
        findings=findings,
        files_scanned=sorted(scanned),
    )
