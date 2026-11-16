"""Tests for the mkifs buildfile parser (buildfile_parser.py)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from qnx_doctor.buildfile_parser import parse_buildfile, parse_buildfile_source

ROOT = os.path.join(os.path.dirname(__file__), "..")

GOOD = """[image=0x400000]
[virtual=x86_64,multiboot] boot = {
    startup-x86 -D 8250
    procnto-smp-instr
}
[+script] init = {
    display_msg "Welcome to QNX 8.0"
    devc-ser8250 &
    reopen /dev/ser1
    [+session] sh
}
libc.so
devc-ser8250
sh
[type=link] /usr/lib/ldqnx.so.2=/proc/boot/libc.so
"""

BAD = """[virtual=x86_64,multiboot] boot = {
    startup-rpi4 -D 8250
}
[+script] init = {
    display_msg "Welcome"
    myapp &
    [+session] esh
}
esh
"""


class TestBuildfileParser(unittest.TestCase):
    def test_good_buildfile_sections(self):
        bf = parse_buildfile_source("x.build", GOOD)
        self.assertEqual(bf.virtual_arch, "x86_64")
        self.assertEqual(len(bf.bootstraps), 1)
        self.assertTrue(bf.has_procnto())
        self.assertEqual(bf.startup_binaries(), ["startup-x86"])
        self.assertTrue(bf.has_libc())
        self.assertIn("libc.so", bf.files)
        self.assertIn("devc-ser8250", bf.files)
        self.assertIn("/usr/lib/ldqnx.so.2", bf.links)

    def test_good_script_commands(self):
        bf = parse_buildfile_source("x.build", GOOD)
        self.assertEqual([c for c, _ in bf.script_commands],
                         ["devc-ser8250", "sh"])
        self.assertTrue(bf.script_has_reopen)
        self.assertTrue(bf.script_has_session)
        self.assertFalse(bf.script_session_without_reopen())

    def test_bad_buildfile(self):
        bf = parse_buildfile_source("x.build", BAD)
        self.assertEqual(bf.virtual_arch, "x86_64")
        self.assertFalse(bf.has_procnto())
        self.assertEqual(bf.startup_binaries(), ["startup-rpi4"])
        self.assertFalse(bf.has_libc())
        self.assertIn(("myapp", 6), bf.script_commands)
        self.assertTrue(bf.script_session_without_reopen())

    def test_comment_and_blank_lines_ignored(self):
        src = "# comment\n\n[virtual=x86,multiboot] boot = {\n    startup-x86 # trailing\n    procnto\n}\n"
        bf = parse_buildfile_source("x.build", src)
        self.assertTrue(bf.has_procnto())
        self.assertEqual(bf.virtual_arch, "x86")

    def test_example_buildfiles_parse(self):
        good = parse_buildfile(os.path.join(ROOT, "examples/good/image_good.build"))
        self.assertTrue(good.has_procnto())
        self.assertTrue(good.has_libc())
        self.assertFalse(good.script_session_without_reopen())
        bad = parse_buildfile(os.path.join(ROOT, "examples/bad/image_bad.build"))
        self.assertFalse(bad.has_procnto())
        self.assertFalse(bad.has_libc())
        self.assertTrue(bad.script_session_without_reopen())

    def test_arch_startup_expectations(self):
        from qnx_doctor.buildfile_parser import ARCH_STARTUP_PREFIX
        self.assertIn("startup-x86", ARCH_STARTUP_PREFIX["x86_64"])
        self.assertIn("startup-rpi", ARCH_STARTUP_PREFIX["aarch64"])


if __name__ == "__main__":
    unittest.main()
