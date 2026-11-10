"""Run every v0.42 unit test (system Python with numpy and scipy). Usage: python3 osf/v42/scripts/tests/run_all_v0_42.py"""
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
os.chdir(ROOT)
suite = unittest.defaultTestLoader.discover(os.path.join("osf", "v42", "scripts", "tests"), pattern="test_*.py")
result = unittest.TextTestRunner(verbosity=1).run(suite)
print("RESULT", "OK" if result.wasSuccessful() else "FAIL", result.testsRun)
sys.exit(0 if result.wasSuccessful() else 1)
