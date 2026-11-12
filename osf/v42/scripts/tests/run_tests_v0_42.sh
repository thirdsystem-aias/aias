#!/bin/zsh
# Runs every v0.42 unit test with the system Python (numpy, scipy) through run_all_v0_42.py (a script entry point:
# the coder's HOME shim re-executes sys.argv[0], which `python3 -c` cannot provide; clarification C28, F4).
cd "$(dirname "$0")/../../../.." || exit 1
PYTHONDONTWRITEBYTECODE=1 python3 osf/v42/scripts/tests/run_all_v0_42.py
