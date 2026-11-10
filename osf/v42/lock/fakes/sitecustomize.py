"""Rehearsal only (PYTHONPATH=osf/v42/lock/fakes).
1. A namespace-package .pth file can pre-load the real `google` package before PYTHONPATH is consulted; drop it from
   sys.modules so that `from google import genai` resolves to the local fake in this directory.
2. With FAKE_FAST=1, time.sleep sleeps at most 0.02 s, so the script's pauses between synchronous calls and its
   60-second batch polls do not slow the fake run."""
import os
import sys
import time

for _k in [k for k in sys.modules if k == "google" or k.startswith("google.")]:
    del sys.modules[_k]

if os.environ.get("FAKE_FAST") == "1":
    _real_sleep = time.sleep
    time.sleep = lambda s: _real_sleep(min(float(s), 0.02))
