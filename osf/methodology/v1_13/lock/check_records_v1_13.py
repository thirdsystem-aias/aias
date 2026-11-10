#!/usr/bin/env python3
"""Read-only pre-tag checks for the v1.13 lock (LOCK_STEPS.md step 1d). Exit 0 only if all pass. Local git only
(run `git fetch origin v0.42` first so that origin/v0.42 is current).

LOCK_MANIFEST all OK; D_b has no UNRESOLVED row and its SHA-256 equals the section 2.3 pin; the scorer's v0.42 pins
equal the blobs on origin/v0.42 (and at tag v0.42-prereg-r1 if it exists locally); v1.14-prereg-r2 -> a5feb4b1
(section 12 (y); r1 -> 20fbc342 superseded);
the dry-run record names the current audit script and fixture manifest; the scorer's activation constants.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
D = ROOT / "osf/methodology/v1_13"
sys.path.insert(0, str(D / "scripts"))
sys.dont_write_bytecode = True
import score_v1_13 as S  # noqa: E402


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(*a):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


checks = []
bad = []
for line in (D / "prereg/LOCK_MANIFEST_v1_13.sha256").read_text(encoding="utf-8").splitlines():
    h, p = line.split(None, 1)
    if sha(ROOT / p.strip()) != h:
        bad.append(p.strip())
checks.append((f"manifest: {len(bad)} mismatches", not bad))
units = S.load_brand_domains()
checks.append((f"D_b: {len(units)} units, {len(S.unresolved_units(units))} UNRESOLVED", not S.unresolved_units(units)))
prereg = (D / "prereg/PRE_REGISTRATION_v1_13.md").read_text(encoding="utf-8")
d_sha = sha(S.DOMAINS_CSV)
checks.append((f"D_b SHA-256 {d_sha[:8]} is the section 2.3 pin", f"SHA-256 of the file as decided: `{d_sha}`" in prereg))
for path, blob in S.V042_PINS.items():
    at_branch = git("rev-parse", f"origin/v0.42:{path}")
    checks.append((f"{Path(path).name}: pin {blob[:8]} == origin/v0.42 {str(at_branch)[:8]}", at_branch == blob))
    at_tag = git("rev-parse", f"{S.V042_TAG}:{path}")
    if at_tag is not None:
        checks.append((f"{Path(path).name}: pin {blob[:8]} == {S.V042_TAG} {at_tag[:8]}", at_tag == blob))
v114 = git("rev-parse", "v1.14-prereg-r2^{commit}")
checks.append((f"v1.14-prereg-r2 -> {str(v114)[:8]}", v114 == "a5feb4b1c4b9e9d19979129afcfd616a50b88c64"))
rec = (D / "prereg/dry_run_audit_v1_13.txt").read_text(encoding="utf-8")
checks.append(("dry-run record names current audit_v1_13.py", sha(D / "scripts/audit_v1_13.py") in rec))
checks.append(("dry-run record names current fixture manifest", sha(D / "scripts/fixtures/audit/manifest.json") in rec))
checks.append(("activation constants: H4 v1.14-prereg-r2, H5 None, H6 v1.12-prereg-r1",
               S.ACTIVATION_TAG == {"H4_Sep_Ranking": "v1.14-prereg-r2", "H5_Sep_Sentiment": None,
                                    "H6_Sep_Coverage": "v1.12-prereg-r1"}))
for name, ok in checks:
    print(("OK   " if ok else "FAIL ") + name)
for p in bad:
    print("     mismatch:", p)
sys.exit(0 if all(ok for _, ok in checks) else 1)
