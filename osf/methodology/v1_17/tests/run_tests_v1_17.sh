#!/bin/zsh
# Runs the v1.17 test suite with the system python3 (numpy + scipy). No network except `git ls-remote` in one gate test.
cd "${0:A:h}" && python3 -m unittest -v test_v1_17 2>&1
