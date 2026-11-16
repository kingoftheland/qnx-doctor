"""Tests for the 22 QNX Doctor rules (rules.py)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from qnx_doctor.rules import RULES, SEVERITY_WEIGHTS, all_rules, get_rule


class TestRules(unittest.TestCase):
    def test_exactly_22_rules(self):
        self.assertEqual(len(RULES), 22)

    def test_rule_ids(self):
        expected = (
            [f"RT-{i:02d}" for i in range(1, 13)]
            + [f"BF-{i:02d}" for i in range(1, 6)]
            + [f"QX-{i:02d}" for i in range(1, 6)]
        )
        self.assertEqual(sorted(RULES), sorted(expected))
        # RT-10 is registered but merged into BF-01/BF-02/BF-03
        # (see rules.py); it is never emitted as its own finding.

    def test_severities_match_spec(self):
        spec = {
            "RT-01": "high", "RT-02": "high", "RT-03": "high",
            "RT-04": "critical", "RT-05": "high", "RT-06": "medium",
            "RT-07": "medium", "RT-08": "low", "RT-09": "medium",
            "RT-10": "high", "RT-11": "high", "RT-12": "low",
            "BF-01": "critical", "BF-02": "high", "BF-03": "high",
            "BF-04": "medium", "BF-05": "low",
            "QX-01": "info", "QX-02": "low", "QX-03": "info",
            "QX-04": "low", "QX-05": "medium",
        }
        for rid, sev in spec.items():
            self.assertEqual(RULES[rid].severity, sev, rid)

    def test_every_rule_has_title_description_recommendation_reference(self):
        for rule in all_rules():
            self.assertTrue(rule.title, rule.id)
            self.assertTrue(rule.description, rule.id)
            self.assertTrue(rule.recommendation, rule.id)
            self.assertTrue(rule.references, rule.id)
            for ref in rule.references:
                self.assertTrue(ref.startswith("http"), rule.id)

    def test_get_rule_case_insensitive(self):
        self.assertIsNotNone(get_rule("rt-04"))
        self.assertIsNotNone(get_rule("BF-01"))
        self.assertIsNone(get_rule("RT-99"))

    def test_severity_weights(self):
        self.assertEqual(SEVERITY_WEIGHTS["critical"], 25)
        self.assertEqual(SEVERITY_WEIGHTS["high"], 15)
        self.assertEqual(SEVERITY_WEIGHTS["medium"], 8)
        self.assertEqual(SEVERITY_WEIGHTS["low"], 3)
        self.assertEqual(SEVERITY_WEIGHTS["info"], 0)


if __name__ == "__main__":
    unittest.main()
