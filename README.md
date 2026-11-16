# QNX Doctor

**A static doctor for QNX 8.0 real-time projects.** It audits C/C++ sources
and mkifs buildfiles for real-time anti-patterns and QNX-specific API misuse
— without needing the QNX SDP, a toolchain, or QEMU. Run it on any Linux
host, in CI, or before you ever boot an image.

Built for the **QNX Global Hackathon 2026** (Devpost, $50,000+ prizes),
category **Developer Tooling & Host Tools**.

> **Honest status (17 Nov 2026): QNX Doctor is static analysis only, no SDP
> required.** QNX SDP 8.0 has **not** been downloaded yet (it needs a myQNX
> account + email verification), so the rules have **not** been validated
> against the real SDP headers/toolchain, and `examples/probe.c` has **not**
> been compiled or booted under QEMU yet. The QEMU mode (`--qemu`) exists
> and degrades gracefully when the SDP is absent. Nothing in this repo
> claims a validation that has not happened.

## What it does

| Feature | Detail |
|---|---|
| 22 checks | RT-01..RT-12 (real-time safety), BF-01..BF-05 (mkifs buildfile/image), QX-01..QX-05 (QNX-specific APIs: message passing, resource managers, PPS, `name_attach`, `ThreadCtl`) |
| Score 0–100 + grade A–F | Weighted by severity: Critical −25, High −15, Medium −8, Low −3, Info −0 |
| Output formats | Coloured terminal (default), `--format json`, `--format sarif` (SARIF 2.1.0 — uploadable to GitHub Code Scanning), `--format html` (single-file report) |
| CI-ready exit codes | `0` = no finding ≥ `--fail-on` (default `high`); `1` = finding at/above threshold; `2` = tool error |
| `explain` | `qnx-doctor explain RT-04` — the rule, why it matters, the fix, and the QNX docs link |
| `init` | Scaffolds an example project (`bad/` + `good/`) to learn from |
| `--qemu` (optional) | Cross-compiles `examples/probe.c` with `qcc`, builds the IFS with `mkifs`, boots QEMU x86_64 and asserts the serial output — **only when SDP 8.0 is installed**; otherwise it prints a note and continues |

## Quick start (no SDP needed)

```bash
# Python 3.11+, stdlib only — no dependencies to install
pip install -e .
qnx-doctor check examples/bad     # 36 findings, score 0/100, exit 1
qnx-doctor check examples/good    # 0 findings, score 100/100, exit 0
qnx-doctor check . --format sarif --output report.sarif
qnx-doctor explain RT-04
qnx-doctor init my-qnx-project
```

## Example output

```
QNX Doctor — report for examples/bad
Score: 0/100  Grade: F  (36 findings: 4 Critical, 11 High, 15 Medium, 5 Low, 1 Info)
[CRITICAL] RT-04  src/isr_bad.c:21  blocking MsgSend() inside ISR handler 'isr_handler'
  → use InterruptAttachEvent() + InterruptWait() in a thread
[CRITICAL] BF-01  image_bad.build:7  .bootstrap section has no procnto — image cannot boot
  → Add procnto (e.g. procnto-smp-instr) to the .bootstrap section after startup-*.
...
```

## The 22 checks (summary)

Real-time safety (`RT-*`, C/C++): heap allocation in RT threads (RT-01),
unbounded allocation in RT loops (RT-05), mutexes without priority
inheritance/ceiling (RT-02), threads without explicit scheduling (RT-03),
blocking calls in ISRs (RT-04, Critical), unchecked QNX kernel calls
(RT-06), `MsgSend` without timeout (RT-07), flat priorities (RT-08),
blocking I/O in RT threads (RT-09), priority 0 = IDLE (RT-11), missing
`mlockall` (RT-12). RT-10 (unbootable buildfile) is covered by the BF
family — see `docs/RULES.md`.

Buildfile / image (`BF-*`, mkifs): missing `procnto` (BF-01, Critical),
startup/arch mismatch (BF-02), script starts a file not in the image
(BF-03), missing `libc.so` / `ldqnx.so.2` (BF-04), `[+session]` without
`reopen` (BF-05).

QNX-specific APIs (`QX-*`): channel without pulse pool (QX-01), PPS
without a service check (QX-02), `resmgr_attach` needs root (QX-03),
`name_attach` without `name_detach` (QX-04), unchecked
`ThreadCtl(_NTO_TCTL_IO_PRIV)` (QX-05).

Full documentation with wrong→right code for every rule: [`docs/RULES.md`](docs/RULES.md).

## How it differs from QNX Bootlab

[QNX Bootlab](https://devpost.com/software/qnx-bootlab) (Devpost, published
6 Nov 2026) is a complementary tool, not a competitor to copy: it is
**build & boot orchestration** — cross-compile, rebuild the image, boot
QEMU, check the serial console ("does the image run?"). QNX Doctor is
**static audit** — "is the code *correct* as real-time QNX code?" It runs
with **no SDP and no QEMU**, so it works in any CI before the SDP is even
installed, and it adds what Bootlab does not have: 22 grounded RT/QNX
rules, a 0–100 score, SARIF output, and bad/good teaching fixtures. Use
both: Doctor to catch the bug, Bootlab to prove the fixed image boots.

## Evidence of QNX use (for the judges)

- **QNX-specific source analysed:** `src/qnx_doctor/c_parser.py`
  (detects `SCHED_FIFO`/`SCHED_RR` threads, `InterruptAttach` handlers,
  `pthread_setschedparam`/`PTHREAD_EXPLICIT_SCHED`,
  `PTHREAD_PRIO_INHERIT`), `src/qnx_doctor/buildfile_parser.py`
  (mkifs grammar: `[attributes]`, `.bootstrap`, `[+script]`, `[type=link]`),
  `src/qnx_doctor/analyzer.py` (RT/QX/BF rule engine),
  `src/qnx_doctor/rules.py` (22 rules grounded in the public QNX 8.0 docs).
- **QNX buildfiles in repo:** `examples/bad/image_bad.build`,
  `examples/good/image_good.build`, `examples/probe.build` (x86_64
  multiboot, pattern from the official QNX "From The Board Up #2" blog).
- **QNX C code in repo:** `examples/probe.c` (uses `uname`,
  `CLOCK_MONOTONIC`, prime checksum — the QEMU probe), plus the bad/good
  fixtures that use real Neutrino APIs (`ChannelCreate`, `MsgSend`,
  `MsgReceivePulse`, `name_attach`, `resmgr_attach`, `InterruptAttachEvent`,
  `slog2f`, `mlockall`, `ThreadCtl`).
- **QEMU output (once SDP is available):** `qnx-doctor check --qemu`
  prints the probe's serial output (`done rc=0`). Until then, the honest
  status is: *not yet validated — see the note at the top of this README*.

## Build & run instructions

- **QNX version:** QNX 8.0 (QNX Neutrino 8.0, QNX Everywhere / SDP 8.0).
- **Target:** QEMU x86_64 (`qemu-system-x86_64 -cpu max -smp 1 -display none -kernel probe.ifs -serial stdio`); static analysis itself runs on the Linux host and targets any QNX 8.0 architecture.
- **Toolchain:** `qcc -V gcc_ntox86_64` (QEMU mode only). Static analysis needs only Python 3.11+ stdlib.
- **Host:** Linux x86_64 (the SDP does not support macOS or ARM hosts).

QEMU mode (requires SDP 8.0 installed, `QNX_HOST`/`QNX_TARGET` set):

```bash
qnx-doctor check examples/good --qemu
# QEMU mode: SDP available: True
# QEMU probe: ok — probe booted and printed done rc=0
```

Without the SDP you get:

```bash
QEMU mode: SDP available: False (missing: qcc, mkifs, qemu-system-x86_64)
```

and the static analysis still runs and exits normally.

## Tests

```bash
python3 -m unittest discover -s tests -v   # 37 tests, stdlib unittest
```

CI (`.github/workflows/ci.yml`) runs the suite on every push, checks that
`examples/bad` fails (exit 1) and `examples/good` passes (exit 0), and
uploads the SARIF report to GitHub Code Scanning.

## Codelab (bonus: Best Codelab / Tutorial)

[`docs/CODELAB.md`](docs/CODELAB.md) — "Audit your first QNX project with
QNX Doctor": install SDP 8.0 via QNX Everywhere, scaffold the example,
run the audit, fix every finding, watch the score go 0 → 100, then boot
the fixed image in QEMU.

## License

MIT — see [LICENSE](LICENSE).
