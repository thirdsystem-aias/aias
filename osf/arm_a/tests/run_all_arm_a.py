#!/usr/bin/env python3
"""Run every Arm A test (no API call) and write the record to osf/arm_a/prereg/tests_arm_a.txt."""
import io
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    sys.path.insert(0, str(HERE))
    sys.path.insert(0, str(HERE.parent / "scripts"))
    suite = unittest.defaultTestLoader.discover(str(HERE), pattern="test_*.py")
    buf = io.StringIO()
    res = unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
    ok = res.testsRun - len(res.failures) - len(res.errors)
    head = (f"Arm A tests, {datetime.now(timezone.utc).isoformat(timespec='seconds')}: {ok} of {res.testsRun} passed "
            f"(failures {len(res.failures)}, errors {len(res.errors)}); no API call, simulated Google data only\n")
    (HERE.parent / "prereg" / "tests_arm_a.txt").write_text(head + buf.getvalue(), encoding="utf-8")
    print(head + buf.getvalue()[-600:])
    return 0 if res.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
