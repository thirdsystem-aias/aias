"""Run the S-Q sensitivity tests (DEVIATIONS Entry 2). Usage: python3 osf/v45/sensitivity/tests/run_all_sq_v0_45.py
(run as a script: v0.42's coder re-executes this file with a HOME shim when the worktree is not ~/aias).
Set AIAS_T4_DIR=<dir with t4_raw.jsonl and coded/> to include the real-t4 check."""
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
os.chdir(ROOT)
suite = unittest.defaultTestLoader.discover(os.path.join("osf", "v45", "sensitivity", "tests"), pattern="test_*.py",
                                            top_level_dir=os.path.join("osf", "v45", "sensitivity", "tests"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
print("RESULT", "OK" if result.wasSuccessful() else "FAIL", result.testsRun)
sys.exit(0 if result.wasSuccessful() else 1)
