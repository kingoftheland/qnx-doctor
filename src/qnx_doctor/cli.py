"""CLI for QNX Doctor.

Subcommands:
  check <path> [--format terminal|json|sarif|html] [--output FILE]
               [--fail-on high|critical|any] [--qemu]
  explain <RULE-ID>
  init [dir]
  report [path] [--output FILE]      (alias: check --format html)

Exit codes: 0 = no finding at/above the --fail-on threshold;
            1 = finding at/above threshold; 2 = tool error.
"""

from __future__ import annotations

import argparse
import importlib.resources
import os
import shutil
import sys

from . import __version__
from .analyzer import analyze_path
from .qemu import check_sdp, run_probe
from .reporters import render
from .rules import all_rules, get_rule

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_ERROR = 2


def _fail_threshold(fail_on: str, summary: dict) -> bool:
    if fail_on == "any":
        return summary["total"] > 0
    if fail_on == "critical":
        return summary["critical"] > 0
    return summary["critical"] + summary["high"] > 0  # default: high


def cmd_check(args: argparse.Namespace) -> int:
    try:
        report = analyze_path(args.path)
    except FileNotFoundError as exc:
        print(f"qnx-doctor: error: {exc}", file=sys.stderr)
        return EXIT_ERROR
    except (OSError, ValueError) as exc:
        print(f"qnx-doctor: error: {exc}", file=sys.stderr)
        return EXIT_ERROR

    if args.qemu:
        status = check_sdp()
        print(f"QEMU mode: SDP available: {status.available}"
              + ("" if status.available
                 else f" (missing: {', '.join(status.missing)})"),
              file=sys.stderr)
        if status.available:
            probe_c = os.path.join(os.path.dirname(__file__),
                                   "templates", "probe.c")
            probe_build = os.path.join(os.path.dirname(__file__),
                                       "templates", "probe.build")
            if os.path.exists(probe_c) and os.path.exists(probe_build):
                res = run_probe(probe_c, probe_build)
                print(f"QEMU probe: {res.status} — {res.detail}",
                      file=sys.stderr)
                if res.serial_output:
                    print(res.serial_output, file=sys.stderr)
            else:
                print("QEMU probe: templates not found in install",
                      file=sys.stderr)

    output = render(report, args.format)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output)
        print(f"Report written to {args.output}")
    else:
        sys.stdout.write(output)
    return EXIT_FINDINGS if _fail_threshold(args.fail_on, report.summary) else EXIT_OK


def cmd_explain(args: argparse.Namespace) -> int:
    rule = get_rule(args.rule_id)
    if rule is None:
        print(f"qnx-doctor: unknown rule '{args.rule_id}'. "
              f"Known rules: {', '.join(r.id for r in all_rules())}",
              file=sys.stderr)
        return EXIT_ERROR
    print(f"{rule.id} [{rule.severity.upper()}] — {rule.title}")
    print(f"Family: {rule.family}")
    print()
    print(rule.description)
    print()
    print(f"Fix: {rule.recommendation}")
    if rule.references:
        print()
        print("References:")
        for ref in rule.references:
            print(f"  {ref}")
    return EXIT_OK


def cmd_init(args: argparse.Namespace) -> int:
    dest = os.path.abspath(args.dir or "qnx-doctor-example")
    templates = importlib.resources.files("qnx_doctor") / "templates"
    if not templates.is_dir():
        print("qnx-doctor: error: example templates not found in install",
              file=sys.stderr)
        return EXIT_ERROR
    if os.path.exists(dest) and os.listdir(dest):
        print(f"qnx-doctor: error: directory '{dest}' is not empty",
              file=sys.stderr)
        return EXIT_ERROR
    os.makedirs(dest, exist_ok=True)
    for name in ("bad", "good"):
        src = templates / name
        shutil.copytree(src, os.path.join(dest, name))
    print(f"Scaffolded example QNX project in {dest}")
    print("  bad/   — intentionally buggy project (expect 12+ findings)")
    print("  good/  — fixed version (expect 0 findings, score 100)")
    print("Run:  qnx-doctor check bad/   then   qnx-doctor check good/")
    return EXIT_OK


def cmd_report(args: argparse.Namespace) -> int:
    args.format = "html"
    args.output = args.output or "qnx-doctor-report.html"
    args.qemu = False
    return cmd_check(args)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="qnx-doctor",
        description="Static analyzer for QNX 8.0 real-time projects "
                    "(no SDP required).")
    p.add_argument("--version", action="version",
                   version=f"qnx-doctor {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    c = sub.add_parser("check", help="analyse a project directory or file")
    c.add_argument("path", nargs="?", default=".",
                   help="project directory or file (default: .)")
    c.add_argument("--format", choices=["terminal", "json", "sarif", "html"],
                   default="terminal")
    c.add_argument("--output", help="write the report to FILE")
    c.add_argument("--fail-on", choices=["high", "critical", "any"],
                   default="high",
                   help="exit 1 when a finding at/above this severity "
                        "exists (default: high)")
    c.add_argument("--qemu", action="store_true",
                   help="also run the QEMU probe (requires QNX SDP 8.0; "
                        "skipped gracefully when the SDP is absent)")
    c.set_defaults(func=cmd_check)

    e = sub.add_parser("explain", help="explain one rule in detail")
    e.add_argument("rule_id", help="rule id, e.g. RT-04")
    e.set_defaults(func=cmd_explain)

    i = sub.add_parser("init", help="scaffold an example project")
    i.add_argument("dir", nargs="?", default=None,
                   help="destination directory (default: qnx-doctor-example)")
    i.set_defaults(func=cmd_init)

    r = sub.add_parser("report", help="analyse and write an HTML report")
    r.add_argument("path", nargs="?", default=".",
                   help="project directory or file (default: .)")
    r.add_argument("--output", default="qnx-doctor-report.html",
                   help="HTML file to write (default: qnx-doctor-report.html)")
    r.add_argument("--fail-on", choices=["high", "critical", "any"],
                   default="high")
    r.set_defaults(func=cmd_report)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
