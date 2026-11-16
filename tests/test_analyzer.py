"""Tests for the analyzer end-to-end (analyzer.py + reporters + CLI).

Fixtures are examples/bad (intentionally buggy, 12+ findings incl.
Critical RT-04 and Critical BF-01) and examples/good (0 findings,
score 100). Run:  python -m unittest discover -s tests -v
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from qnx_doctor.analyzer import (
    analyze_path,
    score_findings,
    Finding,
)
from qnx_doctor.reporters import render_json, render_sarif, render_html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BAD = os.path.join(ROOT, "examples", "bad")
GOOD = os.path.join(ROOT, "examples", "good")


def rule_ids(report):
    return [f.rule_id for f in report.findings]


class TestAnalyzerBad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = analyze_path(BAD)

    def test_at_least_12_findings(self):
        self.assertGreaterEqual(len(self.report.findings), 12)

    def test_has_critical_rt04(self):
        self.assertIn("RT-04", rule_ids(self.report))
        crit = [f for f in self.report.findings
                if f.rule_id == "RT-04" and f.severity == "critical"]
        self.assertGreaterEqual(len(crit), 1)

    def test_has_critical_bf01(self):
        self.assertIn("BF-01", rule_ids(self.report))
        crit = [f for f in self.report.findings
                if f.rule_id == "BF-01" and f.severity == "critical"]
        self.assertGreaterEqual(len(crit), 1)

    def test_buildfile_family_all_present(self):
        for rid in ("BF-01", "BF-02", "BF-03", "BF-04", "BF-05"):
            self.assertIn(rid, rule_ids(self.report), rid)

    def test_rt_family_breadth(self):
        for rid in ("RT-01", "RT-02", "RT-03", "RT-04", "RT-05",
                    "RT-06", "RT-07", "RT-08", "RT-09", "RT-11", "RT-12"):
            self.assertIn(rid, rule_ids(self.report), rid)

    def test_low_score_and_f_grade(self):
        self.assertLess(self.report.score, 60)
        self.assertEqual(self.report.grade, "F")

    def test_summary_counts_add_up(self):
        s = self.report.summary
        self.assertEqual(
            s["total"],
            s["critical"] + s["high"] + s["medium"] + s["low"] + s["info"])

    def test_findings_have_snippet_and_recommendation(self):
        for f in self.report.findings:
            self.assertTrue(f.message, f.rule_id)
            self.assertTrue(f.recommendation, f.rule_id)
            self.assertTrue(f.references, f.rule_id)


class TestAnalyzerGood(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = analyze_path(GOOD)

    def test_zero_findings(self):
        self.assertEqual(self.report.findings, [])

    def test_score_100_grade_a(self):
        self.assertEqual(self.report.score, 100)
        self.assertEqual(self.report.grade, "A")


class TestScoring(unittest.TestCase):
    def _mk(self, severity):
        return Finding(rule_id="X", severity=severity, file="f.c", line=1,
                       column=1, message="m", code_snippet="",
                       recommendation="r")

    def test_clean_scores_100(self):
        score, grade = score_findings([])
        self.assertEqual((score, grade), (100, "A"))

    def test_critical_costs_25(self):
        score, _ = score_findings([self._mk("critical")])
        self.assertEqual(score, 75)

    def test_score_floors_at_zero(self):
        score, grade = score_findings([self._mk("critical")] * 10)
        self.assertEqual((score, grade), (0, "F"))

    def test_grade_boundaries(self):
        self.assertEqual(score_findings([self._mk("high")])[1], "B")   # 85
        self.assertEqual(score_findings([self._mk("medium")] * 2)[1], "B")  # 84
        self.assertEqual(score_findings([self._mk("medium")] * 3)[1], "C")  # 76
        self.assertEqual(score_findings([self._mk("low")] * 10)[1], "C")    # 70


class TestReporters(unittest.TestCase):
    def test_json_round_trip(self):
        report = analyze_path(BAD)
        data = json.loads(render_json(report))
        self.assertEqual(data["tool"], "qnx-doctor")
        self.assertEqual(data["qnx_version"], "8.0")
        self.assertEqual(data["score"], report.score)
        self.assertEqual(len(data["findings"]), len(report.findings))
        self.assertIn("RT-04", [f["id"] for f in data["findings"]])

    def test_sarif_structure(self):
        report = analyze_path(BAD)
        data = json.loads(render_sarif(report))
        self.assertEqual(data["version"], "2.1.0")
        self.assertEqual(data["runs"][0]["tool"]["driver"]["name"],
                         "qnx-doctor")
        self.assertEqual(len(data["runs"][0]["results"]),
                         len(report.findings))
        rule_ids = {r["id"] for r in data["runs"][0]["tool"]["driver"]["rules"]}
        self.assertIn("RT-04", rule_ids)
        self.assertIn("BF-01", rule_ids)

    def test_html_single_file(self):
        report = analyze_path(GOOD)
        out = render_html(report)
        self.assertIn("<!DOCTYPE html>", out)
        self.assertIn("100/100", out)
        self.assertIn("No findings", out)
        bad_html = render_html(analyze_path(BAD))
        self.assertIn("RT-04", bad_html)


class TestCli(unittest.TestCase):
    def _run(self, *argv):
        env = dict(os.environ, PYTHONPATH=os.path.join(ROOT, "src"))
        return subprocess.run(
            [sys.executable, "-m", "qnx_doctor", *argv],
            cwd=ROOT, env=env, capture_output=True, text=True)

    def test_check_bad_exit_1(self):
        self.assertEqual(self._run("check", "examples/bad").returncode, 1)

    def test_check_good_exit_0(self):
        self.assertEqual(self._run("check", "examples/good").returncode, 0)

    def test_check_missing_path_exit_2(self):
        self.assertEqual(self._run("check", "no-such-dir").returncode, 2)

    def test_fail_on_critical(self):
        self.assertEqual(
            self._run("check", "examples/bad",
                      "--fail-on", "critical").returncode, 1)

    def test_explain(self):
        r = self._run("explain", "RT-04")
        self.assertEqual(r.returncode, 0)
        self.assertIn("InterruptAttachEvent", r.stdout)

    def test_explain_unknown_rule_exit_2(self):
        self.assertEqual(self._run("explain", "RT-99").returncode, 2)

    def test_init_scaffolds_checkable_project(self):
        with tempfile.TemporaryDirectory() as td:
            dest = os.path.join(td, "proj")
            r = self._run("init", dest)
            self.assertEqual(r.returncode, 0)
            self.assertTrue(os.path.exists(os.path.join(dest, "bad", "src")))
            self.assertTrue(os.path.exists(os.path.join(dest, "good", "src")))
            bad = analyze_path(os.path.join(dest, "bad"))
            self.assertGreaterEqual(len(bad.findings), 12)
            good = analyze_path(os.path.join(dest, "good"))
            self.assertEqual(good.findings, [])

    def test_qemu_mode_degrades_without_sdp(self):
        r = self._run("check", "examples/good", "--qemu")
        self.assertEqual(r.returncode, 0)
        self.assertIn("SDP available: False", r.stderr)


if __name__ == "__main__":
    unittest.main()
