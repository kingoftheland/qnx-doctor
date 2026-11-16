"""Parser for QNX mkifs buildfiles (IFS image build files).

Grammar (QNX Utilities Reference, mkifs), see RESEARCH.md §3.1:
  - each line: [attributes] file_specification; '#' starts a comment
  - attributes: boolean +name / -name, or value name=value
  - sections: [attrs] name = { ... }  (bootstrap + script)
  - file list entries, incl. [type=link] /dest=/proc/boot/src
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Commands that are mkifs script builtins / variable assignments, not
# binaries that must exist in the image file list (BF-03).
SCRIPT_BUILTINS = {
    "display_msg", "reopen", "waitfor", "echo", "export", "umask",
    "mount", "ln", "cp", "rm", "mkdir", "sleep", "procnto",
    "startup", "boot", "set", "unset",
}

# Expected startup-* binary prefixes per virtual= architecture.
ARCH_STARTUP_PREFIX = {
    "x86_64": ("startup-x86",),
    "x86": ("startup-x86",),
    "aarch64": ("startup-aarch64", "startup-bcm", "startup-rpi"),
    "armv7": ("startup-",),
    "arm": ("startup-",),
}


@dataclass
class Section:
    name: str
    attrs: dict[str, str | bool]
    body: list[str]  # raw body lines (comments stripped)
    start_line: int


@dataclass
class Buildfile:
    path: str
    sections: dict[str, Section] = field(default_factory=dict)
    files: list[str] = field(default_factory=list)   # basenames in image
    links: list[str] = field(default_factory=list)   # link destinations
    global_attrs: dict[str, str | bool] = field(default_factory=dict)
    script_commands: list[tuple[str, int]] = field(default_factory=list)  # (cmd, line)
    script_reopen_lines: list[int] = field(default_factory=list)
    script_session_lines: list[int] = field(default_factory=list)

    @property
    def script_has_reopen(self) -> bool:
        return bool(self.script_reopen_lines)

    @property
    def script_has_session(self) -> bool:
        return bool(self.script_session_lines)

    def script_session_without_reopen(self) -> bool:
        """True if any [+session] has no reopen before it in the script."""
        if not self.script_session_lines:
            return False
        return not any(
            r < s
            for s in self.script_session_lines
            for r in self.script_reopen_lines
        )
    virtual_arch: str | None = None
    bootstraps: list[Section] = field(default_factory=list)

    # -- convenience ------------------------------------------------------
    def bootstrap_text(self) -> str:
        return "\n".join(
            line for s in self.bootstraps for line in s.body)

    def has_procnto(self) -> bool:
        return any(
            re.search(r"\bprocnto\b", line)
            for s in self.bootstraps for line in s.body)

    def startup_binaries(self) -> list[str]:
        out = []
        for line in self.bootstrap_text().splitlines():
            m = re.match(r"\s*(startup-[\w\-\.]+)", line)
            if m:
                out.append(m.group(1))
        return out

    def has_libc(self) -> bool:
        if any(f == "libc.so" or f.endswith("/libc.so") for f in self.files):
            return True
        return any("ldqnx.so" in link for link in self.links)


_ATTR_RE = re.compile(r"\[([^\]]*)\]")
_ASSIGN_RE = re.compile(r"^\s*([A-Za-z_][\w\.\-]*)\s*=\s*(.+?)\s*$")


def parse_attrs(attr_text: str) -> dict[str, str | bool]:
    """Parse the inside of [ ... ] into {name: True/False/value}."""
    attrs: dict[str, str | bool] = {}
    for token in attr_text.replace(",", " ").split():
        token = token.strip()
        if not token:
            continue
        if token.startswith("+"):
            attrs[token[1:]] = True
        elif token.startswith("-"):
            attrs[token[1:]] = False
        elif "=" in token:
            key, _, val = token.partition("=")
            attrs[key.strip()] = val.strip()
        else:
            attrs[token] = True
    return attrs


def _strip_comment(line: str) -> str:
    # '#' starts a comment in buildfiles; no escaping is supported.
    return line.split("#", 1)[0].rstrip()


def _first_token(line: str) -> str:
    line = line.strip().lstrip("+").strip()
    return line.split()[0] if line.split() else ""


def parse_buildfile_source(path: str, source: str) -> Buildfile:
    bf = Buildfile(path=path)
    lines = source.splitlines()
    i = 0
    n = len(lines)

    while i < n:
        raw = _strip_comment(lines[i])
        stripped = raw.strip()
        i += 1
        if not stripped:
            continue

        # Attribute block at start of line, e.g. [virtual=x86_64,multiboot]
        attrs: dict[str, str | bool] = {}
        rest = stripped
        m = _ATTR_RE.match(rest)
        if m:
            attrs = parse_attrs(m.group(1))
            rest = rest[m.end():].strip()
            if "virtual" in attrs and isinstance(attrs["virtual"], str):
                bf.virtual_arch = str(attrs["virtual"]).split(",")[0].strip()

        if not rest:
            # Bare attribute line, e.g. [image=0x400000] or [data=copy]
            bf.global_attrs.update(attrs)
            continue

        # Section start:  name = {
        sec_m = re.match(r"(\.?[A-Za-z_][\w\.\-]*)\s*=\s*\{\s*$", rest)
        if sec_m:
            name = sec_m.group(1)
            body: list[str] = []
            start_line = i  # 1-based line of the '{' line
            depth = 1
            while i < n and depth > 0:
                body_raw = _strip_comment(lines[i])
                i += 1
                depth += body_raw.count("{") - body_raw.count("}")
                if depth > 0:
                    body.append(body_raw.rstrip())
            section = Section(name=name, attrs=attrs, body=body,
                              start_line=start_line)
            bf.sections.setdefault(name, section)
            if name in (".bootstrap", "boot"):
                bf.bootstraps.append(section)
            if attrs.get("script") is True or name in (".script", "init", "startup-script"):
                _analyse_script(bf, section)
            continue

        # [type=link] /dest=/proc/boot/src
        if attrs.get("type") == "link" or "type" in attrs:
            link_m = re.match(r"(\S+)\s*=\s*(\S+)", rest)
            if link_m:
                bf.links.append(link_m.group(1))
                bf.files.append(link_m.group(1).split("/")[-1])
            continue

        # Plain file entry:  [data=copy] devc-con   or   libc.so
        # A line that is only an attribute block was handled above.
        # Anything that looks like a path / bare filename is a file entry.
        token = rest.split()[0]
        if "=" not in token and not token.startswith("{"):
            bf.files.append(token.split("/")[-1])
        # Lines with '=' that are not sections/links are ignored (assignments
        # outside sections are not valid mkifs, but we stay lenient).

    return bf


def _analyse_script(bf: Buildfile, section: Section) -> None:
    """Extract the commands of a [+script] section for BF-03 / BF-05."""
    for offset, line in enumerate(section.body):
        lineno = section.start_line + offset + 1
        s = line.strip()
        if not s:
            continue
        # [+session] esh  — session marker, command after the bracket
        sess = re.match(r"\[\+session\]\s*(.+)", s)
        if sess:
            bf.script_session_lines.append(lineno)
            cmd = _first_token(sess.group(1))
            if cmd:
                bf.script_commands.append((cmd, lineno))
            continue
        if s.startswith("reopen"):
            bf.script_reopen_lines.append(lineno)
            continue
        if s.startswith("["):
            # Other bracketed directives (+optional etc.) — ignore.
            continue
        # Variable assignment (SYSNAME=nto) is not a binary.
        if re.match(r"^[A-Za-z_]\w*=", s):
            continue
        cmd = _first_token(s)
        if not cmd:
            continue
        base = cmd.split("/")[-1]
        if base in SCRIPT_BUILTINS:
            continue
        bf.script_commands.append((cmd, lineno))


def parse_buildfile(path: str) -> Buildfile:
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return parse_buildfile_source(path, fh.read())
