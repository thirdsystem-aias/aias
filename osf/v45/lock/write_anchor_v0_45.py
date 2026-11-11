#!/usr/bin/env python3
"""Write osf/v45/anchor/osf_anchor_v0_45.json after tag v0.45-prereg-r1 is pushed (osf/v45/LOCK_STEPS.md step 5).

Adapted from osf/v42/lock/write_anchor_v0_42.py (v0.42 @ 58d1891). Records the tag (object, peeled commit, tree, tagger
date, the remote refs), every locked file (SHA-256 from prereg/LOCK_MANIFEST_v0_45.sha256, checked on disk AND at the
tag, plus its git blob at the tag), the coder pin (code_t4_v0_42.py blob 2d36735d...), t4's inputs to J1 (raw file at
v0.42-acquisition-locked, coded v0.23 Phase A table at v0.42 commit c84f6fa) and that no t5 raw file exists yet.
`acquire_v0_45.py --collect` refuses unless this file names the commit (or tag object) of the tag on origin.
Refuses if: the tag is not on origin; origin's tag object or peeled commit differs from the local tag; a manifested
file differs on disk or at the tag; the coder blob at the tag is not the pin; a t4 input differs from its pin;
osf/v45/data/t5_raw.jsonl exists. Writes only the anchor file. Network: `git ls-remote` (read-only).
git 2.54 omits the peeled `^{}` line when ls-remote is given a bare tag name (found at v0.44's anchor, Nov 10), so the
query is `refs/tags/<tag>*`, which returns both lines.
--dry-run prints instead of writing; --ref REV (with --dry-run, testing only) reads blobs at REV, skips the origin
checks and marks the record TEST_ONLY. AIAS_ROOT overrides the repository root.
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
TAG = "v0.45-prereg-r1"
MANIFEST = "osf/v45/prereg/LOCK_MANIFEST_v0_45.sha256"
OUT = ROOT / "osf/v45/anchor/osf_anchor_v0_45.json"
RAW = ROOT / "osf/v45/data/t5_raw.jsonl"
CODER = "osf/v42/scripts/code_t4_v0_42.py"
CODER_BLOB = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"     # v0.42 section 5.1; pinned by v1.12, v1.13, v1.14, v0.45
T4_INPUTS = {   # (revision, path) -> SHA-256: t4's records that J1 and the t4 -> t5 tests read (section 5.1, r1)
    ("v0.42-acquisition-locked", "osf/v42/data/t4_raw.jsonl"):
        "f3109091f51af7899098d83a1d7b2080a26a06824caa5f6fc0486f3d6196d4bf",
    ("c84f6faf3003687c598a1970498492b8f68eb91c", "osf/v42/data/coded/v23_phase_a.csv"):
        "52a1c9d7a32ab1bd176eb39af68559a3336ec0442bd2ba52a5ef4a464802358e",
}
FORK_SOURCE = "58d1891bf2fa65b2a0f2f1e2adfcffc93fd56e0f"   # tag v0.42-prereg-r1 (acquire_v0_45.py is forked from it)


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
        sys.exit(f"REFUSED: {RAW} exists: the anchor must precede every t5 call")
    remote = git("ls-remote", "origin", f"refs/tags/{TAG}*") or ""
    commit = git("rev-parse", f"{ref}^{{commit}}")
    if not a.ref:
        refs = dict(reversed(l.split("\t")) for l in remote.splitlines())
        if f"refs/tags/{TAG}" not in refs:
            sys.exit(f"REFUSED: tag {TAG} is not on origin; push it first (LOCK_STEPS step 4)")
        if refs[f"refs/tags/{TAG}"] != git("rev-parse", TAG):
            sys.exit(f"REFUSED: origin's {TAG} object {refs[f'refs/tags/{TAG}']} differs from the local tag")
        peeled = refs.get(f"refs/tags/{TAG}^{{}}")
        if peeled is not None and peeled != commit:
            sys.exit(f"REFUSED: origin's {TAG} -> commit {peeled}, local -> {commit}")
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
        sys.exit(f"REFUSED: coder blob at {ref} is {coder_blob}, not the pinned {CODER_BLOB}")
    t4 = []
    for (rev, p), h in T4_INPUTS.items():
        got = hashlib.sha256(git("show", f"{rev}:{p}", raw=True)).hexdigest()
        if got != h:
            sys.exit(f"REFUSED: t4 input {rev}:{p} has SHA-256 {got}, not {h}")
        t4.append({"revision": rev, "commit": git("rev-parse", f"{rev}^{{commit}}"), "path": p, "sha256": h,
                   "git_blob": git("rev-parse", f"{rev}:{p}")})
    rec = {
        "phase": "v0.45", "revision": "r1", "tag": TAG,
        "tag_object": git("rev-parse", ref), "commit": commit, "tree": git("rev-parse", f"{ref}^{{tree}}"),
        "branch": "v0.45",
        "tagger_date": None if a.ref else git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{TAG}"),
        "remote_tag_refs": remote,
        "recorded_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": git("remote", "get-url", "origin", check=False),
        "osf_deposit": "https://osf.io/ec6wh/ (osfstorage: v45/prereg, v45/prereg/scripts, v45/anchor)",
        "locked_files": files,
        "coder_pin": {"path": CODER, "git_blob": coder_blob},
        "fork_source": {"tag": "v0.42-prereg-r1", "commit": FORK_SOURCE, "path": "osf/v42/scripts/acquire_v0_42.py"},
        "t4_inputs": t4,
        "collection": {"raw_file": "osf/v45/data/t5_raw.jsonl", "exists_at_anchor": False,
                       "command": "acquire_v0_45.py --collect (refuses unless this file names the tag's commit)"},
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
