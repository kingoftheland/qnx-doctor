"""Lightweight C tokenizer / parser (stdlib only, no libclang).

It is deliberately shallow: it strips comments and string/char literals
(preserving line numbers), finds top-level function definitions with
brace matching, and extracts call sites, loop ranges and statements
inside each function. That is all the analyzer needs to detect the
RT/QX rule patterns from RESEARCH.md §3.4 / §5.1.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_C_KEYWORDS = {
    "if", "else", "while", "for", "switch", "return", "sizeof",
    "do", "case", "break", "continue", "goto", "typedef", "struct",
    "union", "enum", "static", "extern", "const", "volatile", "void",
    "int", "char", "long", "short", "unsigned", "signed", "float",
    "double", "register", "inline", "restrict",
}

# Calls that block (or can block) inside an interrupt handler — RT-04.
BLOCKING_CALLS = {
    "MsgSend", "MsgSendv", "pthread_mutex_lock", "pthread_cond_wait",
    "malloc", "calloc", "realloc", "printf", "fprintf", "sleep",
    "usleep", "nanosleep", "open", "read", "write", "fopen",
}

HEAP_CALLS = {"malloc", "calloc", "realloc", "free"}
IO_CALLS = {"printf", "fprintf", "fopen", "read", "write", "fwrite", "puts"}
# QNX kernel calls whose return value must be checked — RT-06 / QX-05.
KERNEL_CALLS = {
    "ChannelCreate", "ChannelDestroy", "ConnectAttach", "ConnectDetach",
    "MsgSend", "MsgSendv", "MsgSendnc", "MsgReceive", "MsgReply",
    "name_attach", "name_open", "resmgr_attach", "InterruptAttach",
    "InterruptAttachEvent", "InterruptWait", "ThreadCtl", "mq_open",
    "shm_open", "TimerTimeout", "ClockTime",
}


@dataclass
class CallSite:
    name: str
    line: int
    column: int
    args: str  # raw argument text (may be empty)
    stmt: str  # the full source line the call sits on


@dataclass
class Function:
    name: str
    file: str
    start_line: int
    end_line: int
    calls: list[CallSite] = field(default_factory=list)
    loops: list[tuple[int, int]] = field(default_factory=list)  # (start,end) lines
    body: str = ""

    def calls_named(self, *names: str) -> list[CallSite]:
        wanted = set(names)
        return [c for c in self.calls if c.name in wanted]

    def has_call(self, *names: str) -> bool:
        return bool(self.calls_named(*names))

    def in_loop(self, line: int) -> bool:
        return any(start <= line <= end for start, end in self.loops)


@dataclass
class CFile:
    path: str
    text: str
    lines: list[str]
    functions: dict[str, Function] = field(default_factory=dict)
    includes: list[str] = field(default_factory=list)

    def all_calls(self) -> list[CallSite]:
        out: list[CallSite] = []
        for fn in self.functions.values():
            out.extend(fn.calls)
        return out


def strip_comments_and_strings(source: str) -> str:
    """Remove /* */ and // comments and string/char literals.

    Every removed character is replaced by a space, except newlines,
    so line/column numbers of the remaining code stay identical.
    """
    out: list[str] = []
    i, n = 0, len(source)
    state = "code"
    while i < n:
        ch = source[i]
        nxt = source[i + 1] if i + 1 < n else ""
        if state == "code":
            if ch == "/" and nxt == "*":
                state = "block_comment"
                out.append("  ")
                i += 2
            elif ch == "/" and nxt == "/":
                state = "line_comment"
                out.append("  ")
                i += 2
            elif ch == '"':
                state = "string"
                out.append(" ")
                i += 1
            elif ch == "'":
                state = "char"
                out.append(" ")
                i += 1
            else:
                out.append(ch)
                i += 1
        elif state == "block_comment":
            if ch == "*" and nxt == "/":
                state = "code"
                out.append("  ")
                i += 2
            else:
                out.append("\n" if ch == "\n" else " ")
                i += 1
        elif state == "line_comment":
            if ch == "\n":
                state = "code"
                out.append("\n")
            else:
                out.append(" ")
            i += 1
        elif state == "string":
            if ch == "\\" and i + 1 < n:
                out.append("  ")
                i += 2
            elif ch == '"':
                state = "code"
                out.append(" ")
                i += 1
            else:
                out.append("\n" if ch == "\n" else " ")
                i += 1
        elif state == "char":
            if ch == "\\" and i + 1 < n:
                out.append("  ")
                i += 2
            elif ch == "'":
                state = "code"
                out.append(" ")
                i += 1
            else:
                out.append(" ")
                i += 1
    return "".join(out)


def _find_matching_brace(text: str, open_pos: int) -> int:
    """Index of the '}' matching the '{' at open_pos, or -1."""
    depth = 0
    for i in range(open_pos, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


_CALL_RE = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
_LOOP_RE = re.compile(r"\b(while|for)\s*\(")
_FUNC_DEF_RE = re.compile(
    r"(?:^|[;{}]\s*)\s*"                      # start of a top-level declaration
    r"(?:[A-Za-z_][\w\s\*]*?[\s\*])?"          # return type, ending in a space or '*'
    r"([A-Za-z_]\w*)\s*\(([^;{}]*)\)\s*\{"    # name(params) {
    , re.MULTILINE,
)


def _extract_calls(body: str, base_line: int, src_lines: list[str]) -> list[CallSite]:
    calls: list[CallSite] = []
    for m in _CALL_RE.finditer(body):
        name = m.group(1)
        if name in _C_KEYWORDS:
            continue
        # Skip function-pointer declarations like "(*handler)(" — the
        # char before the name would be '(' or '*'.
        line = base_line + body.count("\n", 0, m.start())
        # Find matching close paren for the argument list.
        depth = 0
        j = m.end() - 1  # at '('
        end = -1
        for k in range(j, len(body)):
            if body[k] == "(":
                depth += 1
            elif body[k] == ")":
                depth -= 1
                if depth == 0:
                    end = k
                    break
        args = body[m.end():end] if end != -1 else ""
        stmt = src_lines[line - 1].strip() if 0 < line <= len(src_lines) else ""
        calls.append(CallSite(
            name=name,
            line=line,
            column=body.rfind("\n", 0, m.start()) and (m.start() - body.rfind("\n", 0, m.start())),
            args=args.strip(),
            stmt=stmt,
        ))
    return calls


def _extract_loops(body: str, base_line: int) -> list[tuple[int, int]]:
    loops: list[tuple[int, int]] = []
    for m in _LOOP_RE.finditer(body):
        # Find the '(' ... ')' of the loop header, then the '{' of its body.
        depth = 0
        j = m.end() - 1
        k = j
        while k < len(body):
            if body[k] == "(":
                depth += 1
            elif body[k] == ")":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        brace = body.find("{", k)
        if brace == -1:
            continue
        close = _find_matching_brace(body, brace)
        if close == -1:
            continue
        start = base_line + body.count("\n", 0, m.start())
        end = base_line + body.count("\n", 0, close)
        loops.append((start, end))
    return loops


def parse_c_source(path: str, source: str) -> CFile:
    """Parse one C/C++ source file into functions, calls and loops."""
    cleaned = strip_comments_and_strings(source)
    lines = source.splitlines()
    cfile = CFile(path=path, text=source, lines=lines)
    cfile.includes = re.findall(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]', source, re.M)

    seen_spans: list[tuple[int, int]] = []
    for m in _FUNC_DEF_RE.finditer(cleaned):
        name = m.group(1)
        if name in _C_KEYWORDS:
            continue
        open_brace = cleaned.find("{", m.end() - 1)
        if open_brace == -1:
            continue
        close_brace = _find_matching_brace(cleaned, open_brace)
        if close_brace == -1:
            continue
        # Skip if this span is nested inside an already-found function.
        if any(s <= open_brace <= e for s, e in seen_spans):
            continue
        seen_spans.append((open_brace, close_brace))
        start_line = _line_of(cleaned, open_brace)
        end_line = _line_of(cleaned, close_brace)
        body = cleaned[open_brace + 1:close_brace]
        fn = Function(
            name=name,
            file=path,
            start_line=start_line,
            end_line=end_line,
            calls=_extract_calls(body, start_line, lines),
            loops=_extract_loops(body, start_line),
            body=body,
        )
        # Keep the first definition if a name repeats (e.g. overloads).
        cfile.functions.setdefault(name, fn)
    return cfile


def parse_c_file(path: str) -> CFile:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return parse_c_source(path, fh.read())
