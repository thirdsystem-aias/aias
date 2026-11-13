#!/usr/bin/env python3
"""Write osf/v65/anchor/osf_anchor_v0_65.json after tag v0.65-prereg-r1 is pushed.

Adapted from osf/v62/lock/write_anchor_v0_62.py. Records the tag (object, peeled commit, tree, tagger date = the lock
time, remote refs), the lock manifest's own SHA-256, every locked file (SHA-256 from prereg/LOCK_MANIFEST_v0_65.sha256,
checked on disk AND at the tag, plus its git blob), the files v0.65 reads from outside its folder (the same git blobs
as at tag v0.62-prereg-r1 -> e449b6c, v0.65's base), t4's coded Phase B tables (the blob ids at v0.42-scoring-locked
pinned in score_v0_65.EN_BLOBS; metadata only, no content read), and that no v0.62 answer and no v0.65 output exists
yet. `score_v0_65.py --run` refuses unless the tag is on origin, v0.62 has been scored, the lock manifest verifies and
no v0.65 output exists (pre-registration section 5.2).
Refuses if: the tag is not on origin; origin's tag object or peeled commit differs from the local tag; a manifested
file differs on disk or at the tag; the final text is not a byte copy of the r0 draft; a pin differs; v0.62 data or a
v0.65 output exists. Writes only the anchor file. Network: `git ls-remote` (read-only).
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
sys.path.insert(0, str(ROOT / "osf/v65/scripts"))
import score_v0_65 as S  # noqa: E402  (the locked scorer, imported unchanged: file list and pins)

TAG = "v0.65-prereg-r1"
MANIFEST = "osf/v65/prereg/LOCK_MANIFEST_v0_65.sha256"
FINAL = "osf/v65/prereg/PRE_REGISTRATION_v0_65.md"
DRAFT = "osf/v65/prereg/PRE_REGISTRATION_v0_65_DRAFT_r0.md"
OUT = ROOT / "osf/v65/anchor/osf_anchor_v0_65.json"
BASE_TAG = "v0.62-prereg-r1"
BASE_COMMIT = "e449b6cff382f3f26d35e25fa93ec5c9ce34217a"
EN_TAG = S.EN_TAG
EN_COMMIT = "31c64c64656b7b0393eca49e5d10384744475dd9"
READ_FROM_BASE = [p for p in S.MANIFEST_FILES if not p.startswith("osf/v65/")]
V62_DATA = "osf/v62/data"


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
    if S.VERDICTS.exists():
        sys.exit(f"REFUSED: {S.VERDICTS} exists: the anchor must precede the single --run")
    if (ROOT / V62_DATA).exists():
        sys.exit(f"REFUSED: {V62_DATA} exists in this tree: the lock must precede every v0.62 answer")
    v62_data_origin = git("ls-tree", "-r", "--name-only", "refs/remotes/origin/v0.62", "--", V62_DATA)
    if v62_data_origin:
        sys.exit(f"REFUSED: origin/v0.62 holds files under {V62_DATA}: the lock must precede every v0.62 answer")
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
    n_listed = len(files)
    missing = [p for p in [FINAL] + list(S.MANIFEST_FILES) if p not in files]
    if missing:
        sys.exit(f"REFUSED: the manifest does not list {missing}")
    if files[FINAL]["sha256"] != files[DRAFT]["sha256"]:
        sys.exit(f"REFUSED: {FINAL} is not a byte copy of {DRAFT}")
    msha = hashlib.sha256((ROOT / MANIFEST).read_bytes()).hexdigest()
    if hashlib.sha256(git("show", f"{ref}:{MANIFEST}", raw=True)).hexdigest() != msha:
        sys.exit(f"REFUSED: the manifest on disk differs from the manifest at {ref}")
    files[MANIFEST] = {"sha256": msha, "git_blob": git("rev-parse", f"{ref}:{MANIFEST}")}
    if git("rev-parse", f"{BASE_TAG}^{{commit}}") != BASE_COMMIT:
        sys.exit(f"REFUSED: {BASE_TAG} does not point to {BASE_COMMIT}")
    base_blobs = {}
    for p in READ_FROM_BASE:
        b = git("rev-parse", f"{BASE_TAG}:{p}")
        if b != files[p]["git_blob"]:
            sys.exit(f"REFUSED: {p} at {ref} is blob {files[p]['git_blob']}, at {BASE_TAG} {b}")
        base_blobs[p] = b
    if git("rev-parse", f"{EN_TAG}^{{commit}}") != EN_COMMIT:
        sys.exit(f"REFUSED: {EN_TAG} does not point to {EN_COMMIT}")
    en = {raw: git("rev-parse", f"{EN_TAG}:osf/v42/data/coded/{raw}_phase_b.csv") for raw in S.EN_BLOBS}
    if en != S.EN_BLOBS:
        sys.exit(f"REFUSED: t4 coded tables at {EN_TAG} differ from score_v0_65.EN_BLOBS: {en}")
    rec = {
        "phase": "v0.65", "study": "#55 cross-cultural identity load", "revision": "r0", "tag": TAG,
        "tag_object": git("rev-parse", ref), "commit": commit, "tree": git("rev-parse", f"{ref}^{{tree}}"),
        "branch": "v0.65",
        "tagger_date": None if a.ref else git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{TAG}"),
        "remote_tag_refs": remote,
        "recorded_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": git("remote", "get-url", "origin", check=False),
        "osf_deposit": "https://osf.io/ec6wh/ (osfstorage: v65/prereg, v65/prereg/scripts, v65/prereg/summaries, "
                       "v65/anchor)",
        "lock_manifest": {"path": MANIFEST, "sha256": msha, "files_listed": n_listed},
        "final_text": {"path": FINAL, "byte_copy_of": DRAFT, "sha256": files[FINAL]["sha256"]},
        "locked_files": files,
        "base_pins": {"tag": BASE_TAG, "commit": BASE_COMMIT, "blobs": base_blobs,
                      "note": "files read from v0.62's lock and t1, the same blobs as at the base tag"},
        "t4_english_pins": {"tag": EN_TAG, "commit": EN_COMMIT, "coded_phase_b_blobs": en,
                            "content_read_at_anchor": False},
        "v0_62_answers": {"osf/v62/data_in_this_tree": False, "osf/v62/data_files_on_origin_v0.62": 0},
        "scoring": {"verdicts_file": "osf/v65/outputs/v65_verdicts.json", "exists_at_anchor": False,
                    "command": "score_v0_65.py --run (once, after v0.62's own scoring run; section 5.2)"},
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
