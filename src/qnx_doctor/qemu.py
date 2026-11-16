"""Optional QEMU mode — cross-compile a probe with qcc, build an IFS
with mkifs, boot it under QEMU and assert the serial output.

This module NEVER fails the tool when the QNX SDP is absent: every
entry point first checks for qcc/mkifs/qemu-system-x86_64 and returns a
structured "sdp_not_available" result instead of raising. Static
analysis (the core of QNX Doctor) works without any SDP.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field


class SdpUnavailableError(RuntimeError):
    """Raised only when a caller explicitly requires the SDP."""


@dataclass
class SdpStatus:
    qcc: str | None = None
    mkifs: str | None = None
    qemu: str | None = None
    qnx_host: str | None = None
    qnx_target: str | None = None

    @property
    def available(self) -> bool:
        return bool(self.qcc and self.mkifs and self.qemu)

    @property
    def missing(self) -> list[str]:
        out = []
        if not self.qcc:
            out.append("qcc")
        if not self.mkifs:
            out.append("mkifs")
        if not self.qemu:
            out.append("qemu-system-x86_64")
        return out

    def to_dict(self) -> dict:
        return {
            "available": self.available,
            "qcc": self.qcc,
            "mkifs": self.mkifs,
            "qemu": self.qemu,
            "qnx_host": self.qnx_host,
            "qnx_target": self.qnx_target,
            "missing": self.missing,
        }


def check_sdp() -> SdpStatus:
    return SdpStatus(
        qcc=shutil.which("qcc"),
        mkifs=shutil.which("mkifs"),
        qemu=shutil.which("qemu-system-x86_64"),
        qnx_host=os.environ.get("QNX_HOST"),
        qnx_target=os.environ.get("QNX_TARGET"),
    )


@dataclass
class QemuResult:
    ok: bool
    status: str  # ok | sdp_not_available | build_failed | boot_failed | timeout
    detail: str = ""
    serial_output: str = ""
    log: list[str] = field(default_factory=list)


def run_probe(probe_c: str, probe_build: str, timeout: int = 60) -> QemuResult:
    """Build probe.c -> probe.ifs and boot it under QEMU (x86_64).

    Returns a QemuResult; never raises for a missing SDP — the caller
    decides whether that is fatal (it is not, for `qnx-doctor check`).
    """
    status = check_sdp()
    if not status.available:
        return QemuResult(
            ok=False,
            status="sdp_not_available",
            detail="QEMU mode requires QNX SDP 8.0 (missing: "
                   + ", ".join(status.missing) + "). "
                   "Static analysis still works without it.",
        )
    log: list[str] = []
    with tempfile.TemporaryDirectory(prefix="qnx-doctor-qemu-") as td:
        ifs_path = os.path.join(td, "probe.ifs")
        bin_path = os.path.join(td, "probe")

        def _run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
            log.append("$ " + " ".join(cmd))
            return subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=timeout, **kw)

        try:
            r = _run([status.qcc, "-V", "gcc_ntox86_64", probe_c,
                      "-o", bin_path])
            log.append(r.stdout + r.stderr)
            if r.returncode != 0:
                return QemuResult(False, "build_failed",
                                  f"qcc failed (rc={r.returncode})", "", log)
            # mkifs needs the binary next to the buildfile; copy it in.
            shutil.copy(bin_path, os.path.join(td, "probe"))
            r = _run([status.mkifs, probe_build, ifs_path], cwd=td)
            log.append(r.stdout + r.stderr)
            if r.returncode != 0:
                return QemuResult(False, "build_failed",
                                  f"mkifs failed (rc={r.returncode})", "", log)
            r = _run([status.qemu, "-cpu", "max", "-smp", "1",
                      "-display", "none", "-kernel", ifs_path,
                      "-serial", "stdio"], cwd=td)
            serial = r.stdout + r.stderr
            log.append(serial)
            if "done rc=0" in serial:
                return QemuResult(True, "ok",
                                  "probe booted and printed done rc=0",
                                  serial, log)
            return QemuResult(False, "boot_failed",
                              "probe did not print the expected 'done rc=0' "
                              "marker on the serial console", serial, log)
        except subprocess.TimeoutExpired:
            return QemuResult(False, "timeout",
                              f"QEMU run exceeded {timeout}s", "", log)
        except FileNotFoundError as exc:
            return QemuResult(False, "sdp_not_available",
                              f"tool disappeared mid-run: {exc}", "", log)
