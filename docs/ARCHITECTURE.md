# QNX Doctor — Architecture

```
qnx-doctor check <path>
        │
        ▼
┌──────────────┐   C/C++ sources      ┌──────────────────┐
│  analyzer.py │ ───────────────────▶ │  c_parser.py     │
│  (orchestr.) │   buildfiles (.build)│  buildfile_      │
└──────┬───────┘ ───────────────────▶ │  parser.py       │
       │                              └──────────────────┘
       │ rules.py (22 checks: id, severity, pattern, fix, docs)
       ▼
┌──────────────┐
│ reporters.py │ ──▶ terminal (colour) / json / sarif 2.1.0 / html
└──────────────┘
       │  --qemu (optional)
       ▼
┌──────────────┐
│   qemu.py    │ ──▶ qcc → mkifs → qemu-system-x86_64 (only if SDP present)
└──────────────┘
```

## Components

- **`c_parser.py`** — stdlib-only C tokenizer/parser. Strips comments and
  string literals (preserving line numbers), finds top-level function
  definitions with brace matching, and extracts call sites, loop ranges
  and statements per function. No libclang, no dependencies.
- **`buildfile_parser.py`** — mkifs buildfile parser: `[attributes]`
  blocks, `.bootstrap` / `[+script]` sections, file list and
  `[type=link]` entries; extracts script commands for cross-checking.
- **`analyzer.py`** — the rule engine. Per C file it builds a
  cross-file view: pthread attribute tracking (`setschedpolicy`,
  `setinheritsched`, `setschedparam`, `setprotocol`, priority
  assignments), the set of RT routines (threads created with
  `SCHED_FIFO`/`SCHED_RR`, or calling `pthread_setschedparam` with
  those policies), the transitive call graph from RT routines, and
  ISR handlers (2nd argument of `InterruptAttach`). Then it applies
  the RT + QX rules; buildfiles go through the BF rules. Findings are
  sorted by severity, scored (Critical −25, High −15, Medium −8,
  Low −3, Info −0) and graded A–F.
- **`rules.py`** — the single source of truth for the 22 checks: id,
  family, severity, title, description, fix recommendation, and the
  public QNX docs reference each rule is grounded in.
- **`reporters.py`** — terminal (ANSI colour, disabled when piped or
  with `NO_COLOR`), JSON, SARIF 2.1.0 (uploadable to GitHub Code
  Scanning), single-file HTML with a score bar and collapsible findings.
- **`qemu.py`** — optional runtime probe. Checks for `qcc`, `mkifs`
  and `qemu-system-x86_64`; if any is missing it returns a structured
  `sdp_not_available` result instead of failing the tool. When the SDP
  is present it cross-compiles `examples/probe.c`, builds the IFS and
  boots QEMU, asserting the `done rc=0` serial marker.
- **`cli.py`** — `check` / `explain` / `init` / `report` subcommands,
  exit codes 0/1/2, `--fail-on high|critical|any`.

## Known limitations (honest)

- The C parser is heuristic, not a full compiler front-end: macros,
  function pointers as thread routines, and priorities passed through
  variables (non-literal) are handled conservatively (a non-literal
  priority counts as "set" for RT-03, but is not used for RT-08/RT-11).
- The "checked return value" heuristic (RT-06/QX-05) looks for an
  `if`/`assert`/`return` on the same statement, or a test on the
  assigned variable within 5 lines.
- RT-01 excludes functions whose name contains `init` (initialisation
  phase) — a deliberate, documented heuristic.
- The rules have **not** yet been validated against the real SDP 8.0
  headers/toolchain (SDP not downloaded yet — needs a myQNX account).
  They are grounded in the public QNX 8.0 documentation listed in
  `RESEARCH.md` §7.
