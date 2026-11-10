#!/usr/bin/env python3
"""Write osf/v42/anchor/osf_anchor_v0_42.json after tag v0.42-prereg-r1 is pushed (osf/v42/LOCK_STEPS.md step 4).

Records the tag (object, peeled commit, tree, tagger date, the remote ref), every locked file (SHA-256 from
prereg/LOCK_MANIFEST_v0_42.sha256, checked on disk AND at the tag, plus its git blob at the tag), the coder pin that
v1.12, v1.13 and v1.14 rely on (code_t4_v0_42.py blob 2d36735d...), and that no t4 raw file exists yet.
`acquire_v0_42.py --collect` refuses unless this file names the commit of the tag on origin.
Refuses if: the tag is not on origin; origin's peeled commit differs from the local tag; a manifested file differs
on disk or at the tag; the coder blob at the tag is not the pinned one; osf/v42/data/t4_raw.jsonl exists.
Writes only the anchor file. Network: `git ls-remote` (read-only).
--dry-run prints instead of writing; --ref REV (with --dry-run, testing only) reads blobs at REV, skips the origin
checks and marks the record TEST_ONLY. AIAS_ROOT overrides the repository root (rehearsal on a scratch copy).
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
TAG = "v0.42-prereg-r1"
MANIFEST = "osf/v42/prereg/LOCK_MANIFEST_v0_42.sha256"
OUT = ROOT / "osf/v42/anchor/osf_anchor_v0_42.json"
RAW = ROOT / "osf/v42/data/t4_raw.jsonl"
CODER = "osf/v42/scripts/code_t4_v0_42.py"
CODER_BLOB = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"     # pinned by v1.12 (section 2.3), v1.13 and v1.14


def git(*a, check=True, raw=False):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=not raw)
    if r.returncode:
        if check:
            sys.exit(f"git {' '.join(a)} failed: {(r.stderr if not raw else r.stderr.decode()).strip()}")
        return None
    return r.stdout if raw else r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ref", default=None, help="testing only (with --dry-run): read blobs at this revision")
    a = ap.parse_args()
    if a.ref and not a.dry_run:
        sys.exit("--ref is for testing and needs --dry-run")
    ref = a.ref or TAG
    if RAW.exists():
        sys.exit(f"REFUSED: {RAW} exists: the anchor must precede every study call")
    remote = git("ls-remote", "--tags", "origin", TAG) or ""
    commit = git("rev-parse", f"{ref}^{{commit}}")
    if not a.ref:
        refs = dict(reversed(l.split("\t")) for l in remote.splitlines())
        if f"refs/tags/{TAG}" not in refs:
            sys.exit(f"REFUSED: tag {TAG} is not on origin; push it first (LOCK_STEPS step 3)")
        peeled = refs.get(f"refs/tags/{TAG}^{{}}")     # GitHub lists it; a local bare origin may not
        if peeled is not None and peeled != commit:
            sys.exit(f"REFUSED: origin's {TAG} -> commit {peeled}, local -> {commit}")
        if refs[f"refs/tags/{TAG}"] != git("rev-parse", TAG):
            sys.exit(f"REFUSED: origin's {TAG} object {refs[f'refs/tags/{TAG}']} differs from the local tag")
    files = {}
    for line in (ROOT / MANIFEST).read_text(encoding="utf-8").splitlines():
        h, p = line.split(None, 1)
        p = p.strip()
        disk = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
        at_ref = hashlib.sha256(git("show", f"{ref}:{p}", raw=True)).hexdigest()
        if disk != h or at_ref != h:
            sys.exit(f"REFUSED: {p}: manifest {h[:12]}, disk {disk[:12]}, at {ref} {at_ref[:12]}")
        files[p] = {"sha256": h, "git_blob": git("rev-parse", f"{ref}:{p}")}
    msha = hashlib.sha256((ROOT / MANIFEST).read_bytes()).hexdigest()
    if hashlib.sha256(git("show", f"{ref}:{MANIFEST}", raw=True)).hexdigest() != msha:
        sys.exit(f"REFUSED: the manifest on disk differs from the manifest at {ref}")
    files[MANIFEST] = {"sha256": msha, "git_blob": git("rev-parse", f"{ref}:{MANIFEST}")}
    coder_blob = git("rev-parse", f"{ref}:{CODER}")
    if coder_blob != CODER_BLOB:
        sys.exit(f"REFUSED: coder blob at {ref} is {coder_blob}, not the pinned {CODER_BLOB} (v1.12/v1.13/v1.14)")
    rec = {
        "phase": "v0.42", "revision": "r2 + clarifications C25, C26", "tag": TAG,
        "tag_object": git("rev-parse", ref), "commit": commit, "tree": git("rev-parse", f"{ref}^{{tree}}"),
        "branch": "v0.42",
        "tagger_date": None if a.ref else git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{TAG}"),
        "remote_tag_ref": remote,
        "recorded_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": git("remote", "get-url", "origin", check=False),
        "osf_deposit": "https://osf.io/ec6wh/ (osfstorage: v42/prereg, v42/anchor)",
        "locked_files": files,
        "coder_pin": {"path": CODER, "git_blob": coder_blob, "pinned_by": ["v1.12 section 2.3", "v1.13", "v1.14 section 5"]},
        "collection": {"raw_file": "osf/v42/data/t4_raw.jsonl", "exists_at_anchor": False,
                       "command": "acquire_v0_42.py --collect (refuses unless this file names the tag's commit)"},
    }
    if a.ref:
        rec["TEST_ONLY"] = f"blobs read at {a.ref}, not at the tag; origin not checked; not an anchor"
    text = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
    if a.dry_run:
        print(text)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} (tag {TAG} -> commit {commit}; {len(files)} locked files incl. the manifest)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
