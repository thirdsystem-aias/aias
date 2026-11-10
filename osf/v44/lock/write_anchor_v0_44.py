#!/usr/bin/env python3
"""AIAS v0.44: write osf/v44/anchor/osf_anchor_v0_44.json after the tag is pushed (LOCK_STEPS.md step 5).

No model is called, nothing is uploaded. Refuses unless tag v0.44-prereg-r1 is on origin, every file of
LOCK_MANIFEST_v0_44.sha256 still has its listed SHA-256 in the working tree and at the tagged commit, and the tag's
peeled commit equals the local tag's commit. The anchor names the tag object and the commit (the collection guard
`acquire_v0_44.py --collect` looks for either in the file).
Usage: python3 osf/v44/lock/write_anchor_v0_44.py [--pharmacies-dropped]
"""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TAG = "v0.44-prereg-r1"
MANIFEST = ROOT / "osf/v44/LOCK_MANIFEST_v0_44.sha256"
OUT = ROOT / "osf/v44/anchor/osf_anchor_v0_44.json"


def git(*a):
    r = subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def main():
    dropped = "--pharmacies-dropped" in sys.argv[1:]
    remote = {}
    for line in git("ls-remote", "--tags", "origin", TAG).splitlines():
        sha, ref = line.split("\t")
        remote[ref] = sha
    ref = f"refs/tags/{TAG}"
    if ref not in remote:
        sys.exit(f"REFUSED: {TAG} is not on origin")
    tag_obj, commit = remote[ref], remote.get(ref + "^{}", remote[ref])
    if git("rev-parse", f"{TAG}^{{commit}}") != commit:
        sys.exit("REFUSED: local tag commit differs from origin's")
    files = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        h, p = line.split("  ", 1)
        if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h:
            sys.exit(f"REFUSED: {p} differs from the manifest in the working tree")
        blob = git("rev-parse", f"{TAG}:{p}")
        data = subprocess.run(["git", "show", f"{TAG}:{p}"], cwd=ROOT, capture_output=True).stdout
        if hashlib.sha256(data).hexdigest() != h:
            sys.exit(f"REFUSED: {p} at the tag differs from the manifest")
        files.append({"path": p, "sha256": h, "git_blob_at_tag": blob})
    doc = {
        "study": "AIAS v0.44 industry-breadth wave",
        "tag": TAG, "tag_object": tag_obj, "commit": commit, "tree": git("rev-parse", f"{TAG}^{{tree}}"),
        "branch": "v0.44", "remote": git("remote", "get-url", "origin"),
        "pharmacies_dropped_before_lock": dropped,
        "lock_manifest": "osf/v44/LOCK_MANIFEST_v0_44.sha256",
        "lock_manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "locked_files": files,
        "osf": {"project": "ec6wh", "folders": ["v44/prereg", "v44/registries", "v44/scripts", "v44/anchor"],
                "draft_not_a_lock": "v44/prereg/draft_r1"},
        "written_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"{len(files)} files; tag object {tag_obj}; commit {commit} -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
