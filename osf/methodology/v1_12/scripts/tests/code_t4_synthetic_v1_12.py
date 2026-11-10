#!/usr/bin/env python3
"""Test helper (synthetic files only): code a synthetic t4-shaped raw file with the pinned copy of v0.42's coder, as
v0.42's coder CLI does (dedupe_calls, code_calls, write_tables), without v0.42's probe map (the synthetic Phase A
records carry brand / brand_id). The v0.23 Phase A judge stays OFF. No API is called.

    python3 code_t4_synthetic_v1_12.py RAW.jsonl OUTDIR
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import score_v1_12 as S   # noqa: E402

C = S.load_coder()        # may re-execute this script under the coder's HOME shim
calls = C.dedupe_calls(C.read_raw(sys.argv[1]))
A, B = C.code_calls(calls, probes={}, strip=True)
C.write_tables(A, B, sys.argv[2])
print(f"coded {len(calls)} calls -> {len(A)} Phase A rows, {len(B)} Phase B rows")
