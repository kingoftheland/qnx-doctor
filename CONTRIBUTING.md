# Contributing to QNX Doctor

Thanks for helping make QNX real-time code safer. Short version: keep it
honest, keep it grounded, keep it stdlib-only.

## Ground rules

1. **Stdlib only.** No third-party dependencies — the tool must run on a
   bare Linux host without the QNX SDP. If you need a new capability,
   implement it (like the C parser in `c_parser.py`) rather than adding a
   dependency.
2. **Every new rule must be grounded.** A rule needs: a real QNX API or
   documented behaviour, a public QNX docs link, a wrong→right code
   example, and a fixture that triggers it (bad) plus one that does not
   (good). Add both to `docs/RULES.md` and to `rules.py`.
3. **Never claim a validation that has not happened.** SDP 8.0 has not
   been downloaded yet. Do not write "validated against SDP 8.0" or
   "tested on QEMU" until it actually has been — and when it has, say
   exactly how (command, QEMU output, date).
4. **No false positives on the good fixture.** `examples/good` must stay
   at 0 findings / score 100. If your change flags it, the change (or
   the fixture) is wrong — fix the rule, not the test expectation.
5. **Tests first for rules.** Add a case to `tests/test_analyzer.py`
   (bad fixture gains the finding, good fixture stays clean) and run the
   full suite before opening a PR.

## Development

```bash
python3 -m unittest discover -s tests -v
qnx-doctor check examples/bad    # expect exit 1, 36 findings
qnx-doctor check examples/good   # expect exit 0, 0 findings
```

## Reporting issues

Include: the QNX Doctor version, the smallest C file / buildfile that
reproduces the problem, and the expected vs actual finding. Reports
about false positives are especially welcome — a linter that cries wolf
is worse than no linter.
