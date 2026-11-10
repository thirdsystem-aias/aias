"""Run every v0.44 unit test (system Python with numpy and scipy). Usage: python3 osf/v44/scripts/tests/run_all_v0_44.py
The tests are unittest classes; pytest, where installed, collects the same files. No network, no model call."""
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "osf", "v44", "scripts", "tests"))
sys.path.insert(0, os.path.join(ROOT, "osf", "v44", "scripts"))
import score_v0_44  # noqa: E402,F401  (re-executes this runner once under the v0.42 HOME shim, before any test runs)
suite = unittest.defaultTestLoader.discover(os.path.join("osf", "v44", "scripts", "tests"), pattern="test_*.py")
result = unittest.TextTestRunner(verbosity=2).run(suite)
print("RESULT", "OK" if result.wasSuccessful() else "FAIL", result.testsRun,
      "failures", len(result.failures), "errors", len(result.errors))
sys.exit(0 if result.wasSuccessful() else 1)
