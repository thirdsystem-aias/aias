#!/usr/bin/env python3
"""Write osf/methodology/v1_15/anchor/git_anchor_v1_15.json from the PUSHED tag v1.15-prereg-r1 (after v1.11's
anchor writer: the fields of score_v1_11.ANCHOR_FIELDS). Refuses if the tag is not on origin, if the deposit string
is empty, or if any locked file on disk differs from the tag's tree. Lock helper, not locked itself.

Usage (repository root, after `git push origin v1.15 v1.15-prereg-r1`):
  python3 osf/methodology/v1_15/lock/write_anchor_v1_15.py --osf-deposit "osf.io/ec6wh methodology/v1_15/prereg"
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import score_v1_15 as T  # noqa: E402


def git(*a):
    r = subprocess.run(["git", "-C", str(T.ROOT), *a], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"REFUSED: git {' '.join(a)}: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def build(osf_deposit: str) -> dict:
    if not osf_deposit.strip():
        sys.exit("REFUSED: --osf-deposit is empty")
    remote = git("ls-remote", "--tags", "origin", T.PREREG_TAG)
    refs = dict(reversed(line.split("\t")) for line in remote.splitlines() if "\t" in line)
    ref = f"refs/tags/{T.PREREG_TAG}"
    if ref not in refs:
        sys.exit(f"REFUSED: {T.PREREG_TAG} is not on origin")
    commit = git("rev-parse", f"{T.PREREG_TAG}^{{commit}}")
    if refs.get(ref + "^{}", refs[ref]) != commit:
        sys.exit("REFUSED: the local tag differs from origin's")
    files = {}
    for p in T.LOCK_FILES + [str(T.LOCK_MANIFEST_FILE.relative_to(T.ROOT))]:
        blob = git("rev-parse", f"{commit}:{p}")
        data = subprocess.run(["git", "-C", str(T.ROOT), "cat-file", "blob", blob], capture_output=True).stdout
        if (T.ROOT / p).read_bytes() != data:
            sys.exit(f"REFUSED: {p} on disk differs from the tag")
        files[p] = {"git_blob": blob, "sha256": hashlib.sha256(data).hexdigest()}
    return {"tag": T.PREREG_TAG, "tag_object": refs[ref], "commit": commit, "tree": git("rev-parse", f"{commit}^{{tree}}"),
            "branch": "v1.15", "tagger_date": git("for-each-ref", "--format=%(taggerdate:iso-strict)", ref),
            "remote_tag_ref": ref, "recorded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "repository": git("remote", "get-url", "origin"), "osf_deposit": osf_deposit, "locked_files": files}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--osf-deposit", required=True)
    a = ap.parse_args(argv)
    doc = build(a.osf_deposit)
    T.ANCHOR_FILE.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {T.ANCHOR_FILE} ({doc['tag']} -> {doc['commit'][:12]}, {len(doc['locked_files'])} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
