"""Run every v0.45 unit test (system Python with numpy). Usage: python3 osf/v45/scripts/tests/run_all_v0_45.py
(run as a script: v0.42's coder re-executes this file with a HOME shim when the worktree is not ~/aias)."""
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
os.chdir(ROOT)
pattern = sys.argv[1] if len(sys.argv) > 1 else "test_*.py"
suite = unittest.defaultTestLoader.discover(os.path.join("osf", "v45", "scripts", "tests"), pattern=pattern)
result = unittest.TextTestRunner(verbosity=1).run(suite)
print("RESULT", "OK" if result.wasSuccessful() else "FAIL", result.testsRun)
sys.exit(0 if result.wasSuccessful() else 1)
