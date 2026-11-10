#!/bin/zsh
# Runs the v0.42 unit tests with the system Python (numpy, scipy); writes the log beside this script's caller.
cd "$(dirname "$0")/../../../.." || exit 1
PY=/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
"$PY" -c 'import sys, unittest; r = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.discover("osf/v42/scripts/tests", pattern="test_*.py")); sys.exit(0 if r.wasSuccessful() else 1)'
