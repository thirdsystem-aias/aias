#!/usr/bin/env python3
"""Write osf/v62/anchor/osf_anchor_v0_62.json after tag v0.62-prereg-r1 is pushed (lock_v0_62.sh).

Adapted from osf/v45/lock/write_anchor_v0_45.py. Records the tag (object, peeled commit, tree, tagger date, remote refs),
every locked file (SHA-256 from prereg/LOCK_MANIFEST_v0_62.sha256, checked on disk AND at the tag, plus its git blob),
the pins to v0.42 that the branch does not contain (coder blob at v0.42-prereg-r1; t4_raw.jsonl and t4_batches.jsonl at
v0.42-acquisition-locked) and that no v0.62 raw file exists yet. `acquire_v0_62.py --collect` refuses unless this file
names the commit (or tag object) of the tag on origin. Refuses if: the tag is not on origin; origin's tag object or
peeled commit differs from the local tag; a manifested file differs on disk or at the tag; a pin differs; a v0.62 raw
file exists. Writes only the anchor file. Network: `git ls-remote` (read-only).
git 2.54 omits the peeled `^{}` line for a bare tag name, so the query is `refs/tags/<tag>*`.
--dry-run prints instead of writing; --ref REV (with --dry-run, testing only) reads blobs at REV, skips the origin checks.
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
TAG = "v0.62-prereg-r1"
MANIFEST = "osf/v62/prereg/LOCK_MANIFEST_v0_62.sha256"
OUT = ROOT / "osf/v62/anchor/osf_anchor_v0_62.json"
RAW = ROOT / "osf/v62/data/v62_raw.jsonl"
CODER = "osf/v42/scripts/code_t4_v0_42.py"
CODER_BLOB = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"
V42_PINNED = ["osf/v42/scripts/code_t4_v0_42.py", "osf/v42/scripts/score_v0_42.py", "osf/v41/scripts/score_v41.py"]
V42_TAG = "v0.42-prereg-r1"
V42_COMMIT = "58d1891bf2fa65b2a0f2f1e2adfcffc93fd56e0f"
T4_INPUTS = {
    ("v0.42-acquisition-locked", "osf/v42/data/t4_raw.jsonl"):
        "f3109091f51af7899098d83a1d7b2080a26a06824caa5f6fc0486f3d6196d4bf",
    ("v0.42-acquisition-locked", "osf/v42/data/t4_batches.jsonl"):
        "d73b8e81fc6402e81860222737b6a211a8cd394c4c3687bb577955bb6e39298c",
}


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
        sys.exit(f"REFUSED: {RAW} exists: the anchor must precede every v0.62 call")
    remote = git("ls-remote", "origin", f"refs/tags/{TAG}*") or ""
    commit = git("rev-parse", f"{ref}^{{commit}}")
    if not a.ref:
        refs = dict(reversed(l.split("\t")) for l in remote.splitlines())
        if f"refs/tags/{TAG}" not in refs:
            sys.exit(f"REFUSED: tag {TAG} is not on origin; push it first")
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
    if git("rev-parse", f"{V42_TAG}^{{commit}}") != V42_COMMIT:
        sys.exit(f"REFUSED: {V42_TAG} does not point to {V42_COMMIT}")
    pins = {}
    for p in V42_PINNED:
        pins[p] = git("rev-parse", f"{V42_TAG}:{p}")
    if pins[CODER] != CODER_BLOB:
        sys.exit(f"REFUSED: coder blob at {V42_TAG} is {pins[CODER]}, not the pinned {CODER_BLOB}")
    t4 = []
    for (rev, p), h in T4_INPUTS.items():
        got = hashlib.sha256(git("show", f"{rev}:{p}", raw=True)).hexdigest()
        if got != h:
            sys.exit(f"REFUSED: t4 input {rev}:{p} has SHA-256 {got}, not {h}")
        t4.append({"revision": rev, "commit": git("rev-parse", f"{rev}^{{commit}}"), "path": p, "sha256": h,
                   "git_blob": git("rev-parse", f"{rev}:{p}")})
    rec = {
        "phase": "v0.62", "revision": "r3", "tag": TAG,
        "tag_object": git("rev-parse", ref), "commit": commit, "tree": git("rev-parse", f"{ref}^{{tree}}"),
        "branch": "v0.62",
        "tagger_date": None if a.ref else git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{TAG}"),
        "remote_tag_refs": remote,
        "recorded_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": git("remote", "get-url", "origin", check=False),
        "osf_deposit": "https://osf.io/ec6wh/ (osfstorage: v62/prereg, v62/prereg/scripts, v62/prereg/translations, "
                       "v62/prereg/inputs, v62/prereg/summaries, v62/anchor)",
        "locked_files": files,
        "v0_42_pins": {"tag": V42_TAG, "commit": V42_COMMIT, "blobs": pins, "coder_pin_blob": CODER_BLOB},
        "t4_inputs": t4,
        "collection": {"raw_file": "osf/v62/data/v62_raw.jsonl", "exists_at_anchor": False,
                       "command": "acquire_v0_62.py --collect (refuses unless this file names the tag's commit)"},
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
