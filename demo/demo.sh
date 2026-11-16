#!/usr/bin/env bash
# demo.sh — terminal demo for the QNX Doctor video (< 3 min).
# Runs the audit on the bad fixture, explains one rule, then shows the
# good fixture scoring 100. No SDP required.
set -e
cd "$(dirname "$0")/.."
export PYTHONPATH=src
PY=python3

echo "=== 1. Audit the buggy project ==="
$PY -m qnx_doctor check examples/bad || true
echo
echo "=== 2. What does RT-04 mean? ==="
$PY -m qnx_doctor explain RT-04
echo
echo "=== 3. The fixed project ==="
$PY -m qnx_doctor check examples/good
echo
echo "=== 4. HTML + SARIF reports ==="
$PY -m qnx_doctor check examples/bad --format html --output /tmp/qnx-doctor-report.html || true
$PY -m qnx_doctor check examples/bad --format sarif --output /tmp/qnx-doctor.sarif || true
ls -la /tmp/qnx-doctor-report.html /tmp/qnx-doctor.sarif
