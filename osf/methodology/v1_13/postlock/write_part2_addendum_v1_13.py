#!/usr/bin/env python3
"""
write_part2_addendum_v1_13.py -- after tag v1.13-audit-r1 exists: records what the Part II lock adds beside the frozen
text, without touching any locked file (postlock/DEVIATIONS_continued_v1_13.md, "Part II lock"). NOT a locked file.

Checks, at REF (default the tag v1.13-audit-r1):
  1. every file of prereg/LOCK_MANIFEST_v1_13.sha256, and the manifest itself, has the same git blob at REF as at the
     Part I lock commit b83efb2 (the frozen text, both parts, is unchanged by the clarifications);
  2. every file under osf/methodology/v1_13/postlock/ at REF (the clarification log, the new modules, their tests).
Writes osf/methodology/v1_13/postlock/part2_addendum_v1_13.json: tag, tag object, commit, the frozen-text check, and
the SHA-256 and git blob of each postlock file at REF. Refuses if a frozen file differs.

  python3 osf/methodology/v1_13/postlock/write_part2_addendum_v1_13.py [--ref REV] [--dry-run]
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PH = "osf/methodology/v1_13"
MANIFEST = f"{PH}/prereg/LOCK_MANIFEST_v1_13.sha256"
LOCK_COMMIT = "b83efb25a3c2442e3c13a4f63d2968b312ec8f65"     # Part I lock commit (anchor/git_anchor_v1_13.json)
TAG_II = "v1.13-audit-r1"
OUT = ROOT / PH / "postlock" / "part2_addendum_v1_13.json"


def git(*a, check=True, binary=False):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=not binary)
    if r.returncode:
        if check:
            sys.exit(f"git {' '.join(a)} failed: {r.stderr if not binary else r.stderr.decode()}".strip())
        return None
    return r.stdout if binary else r.stdout.strip()


def frozen_check(ref):
    paths = [l.split(None, 1)[1].strip() for l in git("show", f"{LOCK_COMMIT}:{MANIFEST}").splitlines()] + [MANIFEST]
    diff = [p for p in paths if git("rev-parse", f"{ref}:{p}", check=False) != git("rev-parse", f"{LOCK_COMMIT}:{p}")]
    return {"files": len(paths), "differ_from_lock_commit": diff, "lock_commit": LOCK_COMMIT}


def postlock_files(ref):
    names = git("ls-tree", "-r", "--name-only", ref, f"{PH}/postlock/").splitlines()
    out = {}
    for p in names:
        if p.endswith("part2_addendum_v1_13.json"):
            continue
        data = git("show", f"{ref}:{p}", binary=True)
        out[p] = {"sha256": hashlib.sha256(data).hexdigest(), "git_blob": git("rev-parse", f"{ref}:{p}")}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default=TAG_II)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    if git("rev-parse", "-q", "--verify", f"{a.ref}^{{commit}}", check=False) is None:
        sys.exit(f"REFUSED: {a.ref} does not exist")
    fc = frozen_check(a.ref)
    if fc["differ_from_lock_commit"]:
        sys.exit(f"REFUSED: frozen files differ at {a.ref} from {LOCK_COMMIT[:8]}: {fc['differ_from_lock_commit']}")
    rec = {"ref": a.ref, "tag_object": git("rev-parse", a.ref), "commit": git("rev-parse", f"{a.ref}^{{commit}}"),
           "frozen_text_unchanged": fc, "postlock_files": postlock_files(a.ref),
           "recorded_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "note": "Part II clarifications 1-4 and the Part I ex-ante entries 5-12 (postlock/DEVIATIONS_continued_v1_13."
                   "md) and the modules that compute what the frozen text specifies and no locked script computes"}
    if a.ref != TAG_II:
        rec["TEST_ONLY"] = f"read at {a.ref}, not at tag {TAG_II}"
    text = json.dumps(rec, indent=2) + "\n"
    if a.dry_run:
        print(text)
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} (commit {rec['commit'][:10]}, {len(rec['postlock_files'])} postlock files; "
          f"{fc['files']} frozen files unchanged)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
