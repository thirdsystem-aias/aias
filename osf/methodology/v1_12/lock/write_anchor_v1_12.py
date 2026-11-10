#!/usr/bin/env python3
"""Write osf/methodology/v1_12/anchor/osf_anchor_v1_12.json after tag v1.12-prereg-r1 is pushed (LOCK_STEPS.md step 6).

Records the tag, its commit, every locked file (SHA-256 from LOCK_MANIFEST_v1_12.sha256, git blob at the tag), the
conditional legs as the activation rule requires (section 3: tag, commit and the file defining the score), and the
coder pin. Writes only the anchor file. Network: `git ls-remote` only (read-only).
--dry-run prints the record instead of writing it; --ref REV (with --dry-run, testing only) reads blobs at REV
instead of the tag and marks the record TEST_ONLY.
"""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TAG = "v1.12-prereg-r1"
MANIFEST = "osf/methodology/v1_12/prereg/LOCK_MANIFEST_v1_12.sha256"
OUT = ROOT / "osf/methodology/v1_12/anchor/osf_anchor_v1_12.json"
V114_TAG, V114_COMMIT = "v1.14-prereg-r1", "20fbc3423a4c328d14234f4c7c6d3aaecdce501a"
V114_FILES = ["osf/methodology/v1_14/prereg/PRE_REGISTRATION_v1_14.md", "scripts/score_v1_14.py"]
V042_TAG, V042_CODER = "v0.42-prereg-r1", "osf/v42/scripts/code_t4_v0_42.py"
CODER_BLOB = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"


def git(*a, check=True):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    if r.returncode:
        if check:
            sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()}")
        return None
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ref", default=None, help="testing only (with --dry-run): read blobs at this revision")
    a = ap.parse_args()
    if a.ref and not a.dry_run:
        sys.exit("--ref is for testing and needs --dry-run")
    ref = a.ref or TAG
    remote = git("ls-remote", "--tags", "origin", TAG)
    if not a.ref and f"refs/tags/{TAG}" not in (remote or ""):
        sys.exit(f"REFUSED: tag {TAG} is not on origin; push it first (LOCK_STEPS step 3)")
    files = {}
    for line in (ROOT / MANIFEST).read_text(encoding="utf-8").splitlines():
        h, p = line.split(None, 1)
        p = p.strip()
        disk = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        if disk != h:
            sys.exit(f"REFUSED: {p} on disk ({disk[:12]}) differs from the manifest ({h[:12]})")
        files[p] = {"sha256": h, "git_blob": git("rev-parse", f"{ref}:{p}")}
    files[MANIFEST] = {"sha256": hashlib.sha256((ROOT / MANIFEST).read_bytes()).hexdigest(),
                       "git_blob": git("rev-parse", f"{ref}:{MANIFEST}")}
    v114_commit = git("rev-parse", f"{V114_TAG}^{{commit}}")
    if v114_commit != V114_COMMIT:
        sys.exit(f"REFUSED: {V114_TAG} resolves to {v114_commit}, not {V114_COMMIT}")
    v114_remote = git("ls-remote", "--tags", "origin", V114_TAG)
    if f"refs/tags/{V114_TAG}" not in (v114_remote or ""):
        sys.exit(f"REFUSED: {V114_TAG} is not on origin")
    v042_remote = git("ls-remote", "--tags", "origin", V042_TAG)
    rec = {
        "phase": "v1.12", "tag": TAG,
        "tag_object": git("rev-parse", ref), "commit": git("rev-parse", f"{ref}^{{commit}}"),
        "tree": git("rev-parse", f"{ref}^{{tree}}"), "branch": "v1.12",
        "tagger_date": None if a.ref else git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{TAG}"),
        "remote_tag_ref": remote,
        "recorded_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": "https://github.com/thirdsystem-aias/aias",
        "osf_deposit": "https://osf.io/ec6wh/ (osfstorage: methodology/v1_12/prereg, methodology/v1_12/anchor)",
        "locked_files": files,
        "conditional_legs": {
            "H5_Sep_Ranking": {
                "status": "ACTIVE (tag pushed before this lock); gates only if v1.14's STAGE1_VERDICT is "
                          "'SEPARABLE (Stage 2 pending)' (section 3, section 12 (f), N35)",
                "tag": V114_TAG, "remote_tag_ref": v114_remote, "commit": v114_commit,
                "score_definition_files": {p: git("rev-parse", f"{V114_TAG}:{p}") for p in V114_FILES},
                "score": "R*_S0 (modal position), read from osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json; "
                         "its SHA-256 is recorded at scoring (N32)"},
            "H6_Sep_Sentiment": {
                "status": "INACTIVE: no locked Sentiment score on the t4 answers was tagged before this lock; "
                          "v1.11-prereg-r1 defines its score on the archived waves only (section 12 (h), N36)",
                "v1.11_remote_tag_ref": git("ls-remote", "--tags", "origin", "v1.11-prereg-r1")}},
        "coder": {"vendored": "osf/methodology/v1_12/scripts/code_t4_v0_42.py", "pinned_git_blob": CODER_BLOB,
                  "v0.42_tag": V042_TAG, "v0.42_tag_on_origin": bool(v042_remote),
                  "blob_at_v0.42_tag_locally": git("rev-parse", f"{V042_TAG}:{V042_CODER}", check=False),
                  "note": "re-checked against the v0.42 tag before any v1.12 answer is coded (section 2.3, P1)"},
        "mc_brandfree_hits": json.loads((ROOT / "osf/methodology/v1_12/anchor/mc_brandfree_v1_12.json")
                                        .read_text(encoding="utf-8"))["hits"],
    }
    if a.ref:
        rec["TEST_ONLY"] = f"blobs read at {a.ref}, not at the tag; not an anchor"
    text = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
    if a.dry_run:
        print(text)
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} (commit {rec['commit']}, {len(files)} locked files incl. the manifest)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
