# Codelab: Audit your first QNX project with QNX Doctor

*Learn to catch real-time bugs in a QNX 8.0 project before they reach
hardware — with a static analyzer that needs no SDP to run. (~20 minutes)*

## What you will learn

- How QNX Doctor finds real-time anti-patterns (blocking ISRs, priority-0
  threads, heap allocation on the RT path) and buildfile mistakes.
- How to fix each finding and watch the project score go from **0 → 100**.
- (Optional, needs SDP 8.0) How to boot the fixed image in QEMU.

## Prerequisites

- Linux x86_64, Python 3.11+.
- No QNX SDP needed for steps 1–4. Step 5 needs QNX SDP 8.0
  (free via [QNX Everywhere](https://qnx.software/en/developers/get-started/qnx-everywhere):
  create a myQNX account, request the licence, install via QNX Software
  Center).

## Step 1 — Install QNX Doctor

```bash
git clone https://github.com/kingoftheland/qnx-doctor.git
cd qnx-doctor
pip install -e .
qnx-doctor --version
```

## Step 2 — Audit the buggy example

```bash
qnx-doctor check examples/bad
```

You should see **36 findings, score 0/100, grade F** — including:

- `[CRITICAL] RT-04` — `MsgSend()` inside an ISR handler in
  `src/isr_bad.c:21`
- `[CRITICAL] BF-01` — `.bootstrap` without `procnto` in
  `image_bad.build:7`

Pick one rule and read its full explanation:

```bash
qnx-doctor explain RT-04
```

## Step 3 — Fix one finding at a time

Open `examples/bad/src/isr_bad.c`. The handler calls `MsgSend()`,
`printf()` and `malloc()` — all blocking, all forbidden in an ISR.
The QNX way is `InterruptAttachEvent()` + `InterruptWait()` in a thread:

```c
struct sigevent event;
SIGEV_INTR_INIT(&event);
if (InterruptAttachEvent(irq, &event, 0) == -1) { /* handle error */ }
/* in the RT thread: */
InterruptWait(NULL, NULL);
```

The fixed version is already in the repo — compare it:

```bash
diff examples/bad/src/isr_bad.c examples/good/src/isr_good.c
```

Do the same for the other files: `mutex_bad.c` → `mutex_good.c`
(priority-inheritance mutex, checked kernel calls, `MsgSend` with
`TimerTimeout`), `thread_bad.c` → `thread_good.c` (explicit scheduling,
priority 20 vs 10, `mlockall`), `heap_bad.c` → `heap_good.c`
(allocate once in `init()`, reuse a static pool), and
`image_bad.build` → `image_good.build` (`procnto-smp-instr`,
`startup-x86`, `libc.so`, `reopen` before `[+session]`).

## Step 4 — Watch the score go to 100

```bash
qnx-doctor check examples/good
# Score: 100/100  Grade: A  (0 findings)

qnx-doctor check examples/good --format html --output report.html
# open report.html — a single-file report you can share
```

Try the CI gate: `qnx-doctor check examples/bad --fail-on high` exits
`1`; on `examples/good` it exits `0`. That is the command to put in
your own CI.

## Step 5 — (Optional) Boot the fixed image in QEMU

Requires SDP 8.0 with `qcc`, `mkifs` and `qemu-system-x86_64`:

```bash
qnx-doctor check examples/good --qemu
# QEMU mode: SDP available: True
# QEMU probe: ok — probe booted and printed done rc=0
```

Without the SDP you will see `SDP available: False` and the static
analysis still runs — that is by design.

## Step 6 — Audit your own project

```bash
qnx-doctor init my-project        # scaffold bad/ + good/ to practise on
qnx-doctor check /path/to/your/qnx/project --format sarif --output report.sarif
```

Upload `report.sarif` to GitHub Code Scanning (Security tab) and fix
findings highest-severity first: Critical → High → Medium → Low.

## What you built

A repeatable audit loop for any QNX 8.0 codebase: static analysis in CI,
a score you can track over time, and — once the SDP is installed — a
QEMU boot check that the fixed image actually runs.
