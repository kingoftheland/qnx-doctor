"""Rule definitions for QNX Doctor — the 22 grounded checks.

Each rule carries its id, family, severity, a short title, what it looks
for, a one-line fix recommendation, and the public QNX documentation
reference it is grounded in (see RESEARCH.md §3 / §5.1).

Severity weights used by the scorer (analyzer.score_report):
critical=25, high=15, medium=8, low=3, info=0.
"""

from __future__ import annotations

from dataclasses import dataclass

DOCS_BASE = "https://www.qnx.com/developers/docs/8.0"
DOCS_71 = "https://www.qnx.com/developers/docs/7.1"


@dataclass(frozen=True)
class Rule:
    id: str
    family: str  # RT | BF | QX
    severity: str  # critical | high | medium | low | info
    title: str
    description: str
    recommendation: str
    references: tuple[str, ...]
    # Machine-readable pattern hint (used by docs / explain, not the engine)
    pattern: str = ""


RULES: dict[str, Rule] = {}


def _add(rule: Rule) -> Rule:
    RULES[rule.id] = rule
    return rule


# ---------------------------------------------------------------- RT family
_add(Rule(
    "RT-01", "RT", "high",
    "Heap allocation in RT thread",
    "malloc/calloc/realloc/free (or new/delete) inside a real-time thread "
    "(SCHED_FIFO/SCHED_RR) after initialisation. Heap allocation can block "
    "or page-fault, giving unbounded jitter.",
    "Pre-allocate in init() before pthread_setschedparam(), then reuse a "
    "static pool; call mlockall(MCL_CURRENT | MCL_FUTURE).",
    (f"{DOCS_71}/com.qnx.doc.neutrino.getting_started/topic/s1_procs_Thread_attributes_scheduling.html",),
    pattern=r"malloc\(|calloc\(|realloc\(|free\(|new\s|delete\s",
))
_add(Rule(
    "RT-02", "RT", "high",
    "Mutex without priority protocol",
    "pthread_mutex_init() with a NULL/default attribute, or an attribute "
    "that never had pthread_mutexattr_setprotocol() called on it. Without "
    "PTHREAD_PRIO_INHERIT or PTHREAD_PRIO_PROTECT a low-priority holder "
    "can block a high-priority waiter (priority inversion).",
    "pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT) before "
    "pthread_mutex_init().",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/p/pthread_mutexattr_setprotocol.html",),
    pattern=r"pthread_mutex_init\([^,]+,\s*NULL\)",
))
_add(Rule(
    "RT-03", "RT", "high",
    "Thread without explicit scheduling",
    "pthread_create() without PTHREAD_EXPLICIT_SCHED plus an explicit "
    "policy and priority. The default PTHREAD_INHERIT_SCHED silently "
    "ignores the policy/priority stored in the attribute object.",
    "pthread_attr_setinheritsched(&attr, PTHREAD_EXPLICIT_SCHED); "
    "pthread_attr_setschedpolicy(&attr, SCHED_FIFO); "
    "pthread_attr_setschedparam(&attr, &sp);",
    (f"{DOCS_71}/com.qnx.doc.neutrino.getting_started/topic/s1_procs_Thread_attributes_scheduling.html",),
    pattern=r"pthread_create\(",
))
_add(Rule(
    "RT-04", "RT", "critical",
    "Blocking call in ISR",
    "A blocking call (MsgSend, pthread_mutex_lock, malloc, printf, sleep, "
    "open, read) inside an InterruptAttach() handler. An ISR must be short; "
    "blocking here can hang the whole system.",
    "Use InterruptAttachEvent() with SIGEV_INTR and handle the interrupt "
    "in a thread via InterruptWait().",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/i/interruptattach.html",),
    pattern=r"InterruptAttach\(",
))
_add(Rule(
    "RT-05", "RT", "high",
    "Unbounded allocation in RT loop",
    "malloc/realloc inside an unbounded (while(1) / for(;;)) loop of a "
    "real-time thread. The heap grows without bound and fragments.",
    "Pre-allocate a fixed buffer pool in init() and reuse it in the loop.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.getting_started/topic/s1_procs_Thread_attributes_scheduling.html",),
    pattern=r"malloc\(|realloc\(",
))
_add(Rule(
    "RT-06", "RT", "medium",
    "Unchecked QNX kernel call",
    "The return value of a QNX kernel call (ChannelCreate, ConnectAttach, "
    "MsgSend, name_attach, resmgr_attach, InterruptAttach, ...) is never "
    "checked against -1, so a failure is silently ignored.",
    "Check the return value: if (chid == -1) { perror(\"ChannelCreate\"); "
    "exit(EXIT_FAILURE); }",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/c/channelcreate.html",),
    pattern=r"ChannelCreate\(|ConnectAttach\(|MsgSend\(|name_attach\(|resmgr_attach\(",
))
_add(Rule(
    "RT-07", "RT", "medium",
    "MsgSend without timeout",
    "MsgSend() with no TimerTimeout() armed beforehand (and no MsgSendnc). "
    "If the server dies or hangs, the client blocks forever.",
    "Arm TimerTimeout(CLOCK_REALTIME, _NTO_TIMEOUT_SEND, ...) before "
    "MsgSend(), or use MsgSendnc().",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/t/timertimeout.html",),
    pattern=r"MsgSend\(",
))
_add(Rule(
    "RT-08", "RT", "low",
    "Flat priority (no differentiation)",
    "No pthread_setschedparam() anywhere, or every thread runs at the same "
    "sched_priority. Real-time work cannot be distinguished from background "
    "work, so background threads can delay critical ones.",
    "Give the critical thread a higher priority (e.g. 20) than background "
    "threads (e.g. 10).",
    (f"{DOCS_71}/com.qnx.doc.neutrino.getting_started/topic/s1_procs_Thread_attributes_scheduling.html",),
    pattern=r"sched_priority",
))
_add(Rule(
    "RT-09", "RT", "medium",
    "Blocking I/O in RT thread",
    "Blocking I/O (printf, fprintf, fopen, read, write) on the path of a "
    "real-time thread. Console/file I/O can block for an unbounded time.",
    "Use slog2f() or write to a ring buffer instead of printf() in the "
    "RT loop.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/s/slogger2.html",),
    pattern=r"printf\(|fprintf\(|fopen\(|read\(|write\(",
))
_add(Rule(
    "RT-10", "RT", "high",
    "Buildfile cannot boot (procnto / startup / missing file)",
    "Buildfile problem that prevents boot: no procnto in .bootstrap, a "
    "startup binary that does not match the target architecture, or a "
    "file referenced by the boot script that is missing from the image. "
    "This check is merged into the more specific BF-01 (missing procnto), "
    "BF-02 (startup/arch mismatch) and BF-03 (script references missing "
    "file) so the same defect is reported once, under the precise id; "
    "RT-10 is kept in the registry to keep rule numbering stable.",
    "Fix the underlying BF-01 / BF-02 / BF-03 finding.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.utilities/topic/m/mkifs.html",),
    pattern=r"procnto|startup-",
))
_add(Rule(
    "RT-11", "RT", "high",
    "Priority zero thread",
    "sched_priority = 0. Priority 0 is the IDLE priority in QNX Neutrino: "
    "the thread practically never runs. Classic bug when "
    "PTHREAD_EXPLICIT_SCHED is set but setschedparam is forgotten.",
    "Set a real priority: sp.sched_priority = 10; (valid range 1-255).",
    (f"{DOCS_71}/com.qnx.doc.neutrino.getting_started/topic/s1_procs_Thread_attributes_scheduling.html",),
    pattern=r"sched_priority\s*=\s*0\b",
))
_add(Rule(
    "RT-12", "RT", "low",
    "Missing mlockall in RT thread",
    "A real-time thread runs without mlockall(MCL_CURRENT | MCL_FUTURE), "
    "so a page fault can occur on the real-time path.",
    "Call mlockall(MCL_CURRENT | MCL_FUTURE) after init, before the RT loop.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/m/mlockall.html",),
    pattern=r"mlockall\(",
))

# ---------------------------------------------------------------- BF family
_add(Rule(
    "BF-01", "BF", "critical",
    "Missing procnto in bootstrap",
    "The [virtual=...] .bootstrap section does not contain procnto. "
    "Without the process manager the image cannot boot.",
    "Add procnto (e.g. procnto-smp-instr) to the .bootstrap section after "
    "startup-*.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.utilities/topic/m/mkifs.html",),
    pattern=r"procnto",
))
_add(Rule(
    "BF-02", "BF", "high",
    "Startup/arch mismatch",
    "The startup-* binary does not match the virtual=<arch> of the "
    "bootstrap section (e.g. virtual=x86_64 with startup-rpi4).",
    "Use startup-x86 for virtual=x86_64 / x86, and the matching ARM "
    "startup for aarch64 targets.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.utilities/topic/m/mkifs.html",),
    pattern=r"startup-",
))
_add(Rule(
    "BF-03", "BF", "high",
    "Script references missing file",
    "A binary started in the [+script] section is not present in the "
    "image file list, so it will fail to start at boot.",
    "Add the binary to the buildfile's file list.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.utilities/topic/m/mkifs.html",),
    pattern=r"\[\+script\]",
))
_add(Rule(
    "BF-04", "BF", "medium",
    "Missing libc / ldqnx link",
    "The image contains neither libc.so nor the [type=link] "
    "/usr/lib/ldqnx.so.2 symlink, so dynamically linked binaries cannot run.",
    "Add libc.so and [type=link] /usr/lib/ldqnx.so.2=/proc/boot/libc.so "
    "to the file list.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.utilities/topic/m/mkifs.html",),
    pattern=r"libc\.so|ldqnx\.so",
))
_add(Rule(
    "BF-05", "BF", "low",
    "Session without reopen",
    "A [+session] shell is started without a preceding reopen of the "
    "console/serial device, so the session has no terminal attached.",
    "Run devc-con -n9 & (or devc-ser8250 &) and reopen /dev/con1 "
    "(or /dev/ser1) before [+session].",
    (f"{DOCS_71}/com.qnx.doc.neutrino.utilities/topic/m/mkifs.html",),
    pattern=r"\[\+session\]",
))

# ---------------------------------------------------------------- QX family
_add(Rule(
    "QX-01", "QX", "info",
    "Channel without pulse pool",
    "ChannelCreate(0) in a server that also handles pulses "
    "(MsgReceivePulse). A dedicated pulse pool avoids pulse loss under load.",
    "Consider ChannelCreatePulsePool() for servers that receive pulses.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/c/channelcreatepulsepool.html",),
    pattern=r"ChannelCreate\(0\)",
))
_add(Rule(
    "QX-02", "QX", "low",
    "PPS object without persistence check",
    "A PPS object is opened (/pps/... or /fs/pps/...) without checking "
    "that the pps service is running, so publishes can be silently lost.",
    "Check that the pps service is running (e.g. verify the object opens "
    "and the service responds) before publishing.",
    ("http://www.qnx.com/developers/docs/6.5.0SP1/neutrino/sys_arch/pps.html",),
    pattern=r"open\(\s*\"[^\"]*pps",
))
_add(Rule(
    "QX-03", "QX", "info",
    "Resource manager without root note",
    "resmgr_attach() is used. Attaching a resource manager requires root "
    "privileges; the image must run this process as root.",
    "Make sure the process runs as root (or with the required abilities) "
    "in the image.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/r/resmgr_attach.html",),
    pattern=r"resmgr_attach\(",
))
_add(Rule(
    "QX-04", "QX", "low",
    "name_attach without name_detach / cleanup",
    "name_attach() is called but the file never calls name_detach(), so "
    "the pathname entry leaks on exit.",
    "Call name_detach() (and ChannelDestroy()) during shutdown/cleanup.",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/n/name_attach.html",),
    pattern=r"name_attach\(",
))
_add(Rule(
    "QX-05", "QX", "medium",
    "ThreadCtl(_NTO_TCTL_IO_PRIV) without error check",
    "ThreadCtl(_NTO_TCTL_IO_PRIV, ...) return value is not checked. "
    "I/O privilege requires root; failure leaves the thread without the "
    "privilege it assumes it has.",
    "Check the return value: if (ThreadCtl(...) == -1) { perror(...); ... }",
    (f"{DOCS_71}/com.qnx.doc.neutrino.lib_ref/topic/t/threadctl.html",),
    pattern=r"ThreadCtl\(_NTO_TCTL_IO",
))

SEVERITY_WEIGHTS = {"critical": 25, "high": 15, "medium": 8, "low": 3, "info": 0}
SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]


def get_rule(rule_id: str) -> Rule | None:
    return RULES.get(rule_id.upper())


def all_rules() -> list[Rule]:
    return [RULES[k] for k in sorted(RULES)]
