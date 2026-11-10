#!/usr/bin/env python3
"""Read-only pre-tag checks for the v1.12 lock (LOCK_STEPS.md step 1d). Exit 0 only if all pass.

N1 record PASS and naming the current scorer's SHA-256; MC_BrandFree record with 0 hits, built on the current probe
file, with the coder pin matching; the vendored coder's git blob equals the pin; LOCK_MANIFEST all OK.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "osf/methodology/v1_12"
PIN = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


checks = []
n1 = json.loads((D / "prereg/calibration_N1_v1_12.json").read_text(encoding="utf-8"))
checks.append(("N1 result PASS", n1["statistic_r1"]["result"] == "PASS"))
checks.append(("N1 record names current scorer", n1["code"]["sha256"] == sha(D / "scripts/score_v1_12.py")))
bf = json.loads((D / "anchor/mc_brandfree_v1_12.json").read_text(encoding="utf-8"))
checks.append(("MC_BrandFree 0 hits", bf["hits"] == [] and bf["passed"] is True))
checks.append(("MC_BrandFree on current probes", bf["probes_sha256"] == sha(D / "prereg/probes_v1_12.jsonl")))
checks.append(("MC_BrandFree coder match", bf["coder"]["match"] is True))
blob = subprocess.run(["git", "-C", str(ROOT), "hash-object", str(D / "scripts/code_t4_v0_42.py")],
                      capture_output=True, text=True).stdout.strip()
checks.append((f"coder blob {blob[:8]} == pin", blob == PIN))
bad = []
for line in (D / "prereg/LOCK_MANIFEST_v1_12.sha256").read_text(encoding="utf-8").splitlines():
    h, p = line.split(None, 1)
    if sha(ROOT / p.strip()) != h:
        bad.append(p.strip())
checks.append((f"manifest: {len(bad)} mismatches", not bad))
for name, ok in checks:
    print(("OK   " if ok else "FAIL ") + name)
for p in bad:
    print("     mismatch:", p)
sys.exit(0 if all(ok for _, ok in checks) else 1)
