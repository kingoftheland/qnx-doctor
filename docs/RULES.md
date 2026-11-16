# QNX Doctor — Rule Reference (22 checks)

All rules are grounded in public QNX documentation (SDP 8.0 / Neutrino
Library Reference). Severity weights for the 0–100 score: Critical −25,
High −15, Medium −8, Low −3, Info −0.

## RT — Real-time safety (C/C++)

### RT-01 — Heap allocation in RT thread (High)
`malloc`/`calloc`/`realloc`/`free` in a `SCHED_FIFO`/`SCHED_RR` thread
after initialisation. Heap allocation can block or page-fault.
```c
/* WRONG */ void *rt(void *a){ void *p = malloc(128); /* ... */ }
/* RIGHT */ /* allocate once in init(), reuse a static pool, then
               mlockall(MCL_CURRENT | MCL_FUTURE); */
```

### RT-02 — Mutex without priority protocol (High)
`pthread_mutex_init(&m, NULL)` — no priority inheritance/ceiling.
```c
/* WRONG */ pthread_mutex_init(&m, NULL);
/* RIGHT */ pthread_mutexattr_init(&a);
            pthread_mutexattr_setprotocol(&a, PTHREAD_PRIO_INHERIT);
            pthread_mutex_init(&m, &a);
```

### RT-03 — Thread without explicit scheduling (High)
`pthread_create()` without `PTHREAD_EXPLICIT_SCHED` + policy + priority.
The default `PTHREAD_INHERIT_SCHED` silently ignores the attribute values.
```c
/* WRONG */ pthread_attr_setschedpolicy(&a, SCHED_FIFO);
            pthread_create(&t, &a, fn, NULL);   /* priority defaults to 0 */
/* RIGHT */ pthread_attr_setinheritsched(&a, PTHREAD_EXPLICIT_SCHED);
            pthread_attr_setschedpolicy(&a, SCHED_FIFO);
            sp.sched_priority = 10;
            pthread_attr_setschedparam(&a, &sp);
            pthread_create(&t, &a, fn, NULL);
```

### RT-04 — Blocking call in ISR (Critical)
`MsgSend`, `pthread_mutex_lock`, `malloc`, `printf`, `sleep`, `open`,
`read` inside an `InterruptAttach()` handler.
```c
/* WRONG */ handler(){ MsgSend(coid, ...); }
/* RIGHT */ InterruptAttachEvent(irq, &event, 0);   /* event.sigev_notify = SIGEV_INTR */
            /* ... in a thread: */ InterruptWait(NULL, NULL);
```

### RT-05 — Unbounded allocation in RT loop (High)
`malloc`/`realloc` inside `while(1)` of an RT thread.
```c
/* WRONG */ while (1) { buf = malloc(n); /* ... */ }
/* RIGHT */ /* pre-allocate a fixed buffer pool in init(), reuse it */
```

### RT-06 — Unchecked QNX kernel call (Medium)
Return value of `ChannelCreate`, `ConnectAttach`, `MsgSend`,
`name_attach`, `resmgr_attach`, `InterruptAttach`, … never checked.
```c
/* WRONG */ chid = ChannelCreate(0);
/* RIGHT */ chid = ChannelCreate(0);
            if (chid == -1) { perror("ChannelCreate"); exit(EXIT_FAILURE); }
```

### RT-07 — MsgSend without timeout (Medium)
`MsgSend()` with no `TimerTimeout()` armed (and no `MsgSendnc`).
```c
/* WRONG */ MsgSend(coid, ...);
/* RIGHT */ TimerTimeout(CLOCK_REALTIME, _NTO_TIMEOUT_SEND, &event, &timeout, NULL);
            MsgSend(coid, ...);
```

### RT-08 — Flat priority (Low)
No `pthread_setschedparam()` anywhere, or every thread at the same
`sched_priority`. Give the critical thread a higher priority (e.g. 20)
than background threads (e.g. 10).

### RT-09 — Blocking I/O in RT thread (Medium)
`printf`/`fprintf`/`fopen`/`read`/`write` on the RT path.
```c
/* WRONG */ printf("tick\n");        /* in the RT loop */
/* RIGHT */ slog2f(_SLOG_SETCODE(_SLOG_SYSMSG, 0), _SLOG_INFO, "tick");
```

### RT-10 — Buildfile cannot boot (High, merged)
No `procnto`, wrong `startup-*`, or a file missing from the image.
Implemented by the more specific BF-01 / BF-02 / BF-03 so the same
defect is reported once under the precise id. Kept in the registry to
keep rule numbering stable (see RESEARCH.md §5.1).

### RT-11 — Priority zero thread (High)
`sched_priority = 0` — priority 0 is IDLE in QNX Neutrino; the thread
practically never runs. Use 1–255 (e.g. 10).

### RT-12 — Missing mlockall in RT thread (Low)
RT thread without `mlockall(MCL_CURRENT | MCL_FUTURE)` after init.

## BF — Buildfile / image (mkifs)

### BF-01 — Missing procnto in bootstrap (Critical)
```text
# WRONG
[virtual=x86_64,multiboot] boot = { startup-x86 -D 8250 }
# RIGHT
[virtual=x86_64,multiboot] boot = {
    startup-x86 -D 8250
    procnto-smp-instr
}
```

### BF-02 — Startup/arch mismatch (High)
`virtual=x86_64` with `startup-rpi4` → use `startup-x86`.

### BF-03 — Script references missing file (High)
A binary started in `[+script]` is not in the image file list — add it.

### BF-04 — Missing libc / ldqnx link (Medium)
Add `libc.so` and `[type=link] /usr/lib/ldqnx.so.2=/proc/boot/libc.so`.

### BF-05 — Session without reopen (Low)
Run `devc-con -n9 &` + `reopen /dev/con1` (or `devc-ser8250` +
`reopen /dev/ser1`) before `[+session]`.

## QX — QNX-specific APIs

### QX-01 — Channel without pulse pool (Info)
`ChannelCreate(0)` in a server that also handles pulses — consider
`ChannelCreatePulsePool()`.

### QX-02 — PPS object without persistence check (Low)
`open("/pps/...")` without checking that the `pps` service is running.

### QX-03 — Resource manager without root note (Info)
`resmgr_attach()` requires root privileges in the image.

### QX-04 — name_attach without name_detach / cleanup (Low)
`name_attach()` with no matching `name_detach()` — the pathname leaks.

### QX-05 — ThreadCtl(_NTO_TCTL_IO_PRIV) without error check (Medium)
Check the return value; I/O privilege requires root.
