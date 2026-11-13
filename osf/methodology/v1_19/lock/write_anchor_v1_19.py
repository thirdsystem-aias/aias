#!/usr/bin/env python3
"""Write osf/methodology/v1_19/anchor/osf_anchor_v1_19.json after tag v1.19-prereg-r1 is pushed and the OSF deposit of
prereg/, scripts/, dryrun/ and anchor/ (methodology/v1_19) is done (pre-registration sections 0, 9.2 and 15).

Adapted from osf/methodology/v1_12/lock/write_anchor_v1_12.py and osf/v65/lock/write_anchor_v0_65.py. Records the tag
(object, peeled commit, tree, tagger date = the lock time, remote refs), the lock manifest's own SHA-256, every locked
file (SHA-256 from prereg/LOCK_MANIFEST_v1_19.sha256, checked on disk AND at the tag, plus its git blob), Paper A's
pins (tag v1.12-prereg-r1 -> 49efc47; the imported scorer and the three other inputs are the same blobs as at that
tag; the scorer's SHA-256 is v1.12's locked f7689898...), whether any Paper A answer existed, and the OSF deposit
checked file by file against the files at the tag (read-only, OSF v2 API, OSF_TOKEN; osf_verify_v1_19.py's listing).
`score_v1_19.py --run` refuses unless this file's "commit" is the commit of the tag on origin (section 9.2).
Refuses if: the tag is not on origin; origin's tag object or peeled commit differs from the local tag; a manifested
file differs on disk or at the tag; the final text is not a byte copy of draft r1; a Paper A pin differs; a deposited
folder on OSF does not hold exactly the files at the tag (an anchor/ folder may lack this file itself). Writes only the
anchor file. --dry-run prints instead of writing; --ref REV (with --dry-run, testing only) reads blobs at REV and skips
the origin and OSF checks.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
D = "osf/methodology/v1_19"
TAG = "v1.19-prereg-r1"
MANIFEST = f"{D}/prereg/LOCK_MANIFEST_v1_19.sha256"
FINAL = f"{D}/prereg/PRE_REGISTRATION_v1_19.md"
DRAFT = f"{D}/prereg/PRE_REGISTRATION_v1_19_DRAFT_r1.md"
OUT = ROOT / f"{D}/anchor/osf_anchor_v1_19.json"
A_TAG, A_COMMIT = "v1.12-prereg-r1", "49efc473a63f415b9ae3eaa86811ca62fd81b91a"
A_SCORER = "osf/methodology/v1_12/scripts/score_v1_12.py"
A_SCORER_SHA256 = "f7689898fdc68715f207ffc0c1e335a0264aefcce0b2836d1fd5e79624709d20"
A_INPUTS = [A_SCORER, "osf/methodology/v1_12/prereg/probes_v1_12.jsonl", "osf/v31/data/v31_cpc.csv",
            "prereg/v0_22_registry.json"]
A_DATA = "osf/methodology/v1_12/data"
A_WINDOW_OPENS_UTC = "2026-11-14T00:00:00+00:00"
OSF_FOLDERS = ["prereg", "scripts", "dryrun", "anchor"]
OSF_BASE = "methodology/v1_19"


def git(*a, check=True, raw=False):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=not raw)
    if r.returncode:
        if check:
            sys.exit(f"git {' '.join(a)} failed: {(r.stderr if not raw else r.stderr.decode()).strip()}")
        return None
    return r.stdout if raw else r.stdout.strip()


def sha_at(ref, p):
    return hashlib.sha256(git("show", f"{ref}:{p}", raw=True)).hexdigest()


def osf_check(ref):
    """Each deposited folder on OSF against the tracked files of that folder at ref (SHA-256, name by name)."""
    if not os.environ.get("OSF_TOKEN"):
        sys.exit("REFUSED: OSF_TOKEN is not set: the deposit cannot be checked")
    sys.path.insert(0, str(HERE))
    import osf_verify_v1_19 as OV  # noqa: E402  (listing functions; read-only)
    out = {}
    for f in OSF_FOLDERS:
        local = {}
        for p in git("ls-tree", "-r", "--name-only", ref, "--", f"{D}/{f}").splitlines():
            local[p[len(f"{D}/{f}/"):]] = sha_at(ref, p)
        remote = OV.walk(OV.find_folder(f"{OSF_BASE}/{f}"), "", {})
        if f == "anchor":
            remote.pop(OUT.name, None)  # this file itself is committed and deposited after the tag
        match = sorted(n for n in local if remote.get(n) == local[n])
        missing = sorted(n for n in local if n not in remote)
        differ = sorted(n for n in local if n in remote and remote[n] != local[n])
        extra = sorted(n for n in remote if n not in local)
        if differ or extra or missing or not local:
            sys.exit(f"REFUSED: OSF {OSF_BASE}/{f}: differ {differ}, missing {missing}, extra {extra}")
        out[f"{OSF_BASE}/{f}"] = {"files_at_tag": len(local), "match": len(match)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ref", default=None, help="testing only (with --dry-run): read blobs at this revision")
    a = ap.parse_args()
    if a.ref and not a.dry_run:
        sys.exit("--ref is for testing and needs --dry-run")
    ref = a.ref or TAG
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
        at_ref = sha_at(ref, p)
        if disk != h or at_ref != h:
            sys.exit(f"REFUSED: {p}: manifest {h[:12]}, disk {disk[:12]}, at {ref} {at_ref[:12]}")
        files[p] = {"sha256": h, "git_blob": git("rev-parse", f"{ref}:{p}")}
    n_listed = len(files)
    for p in (FINAL, DRAFT, *A_INPUTS):
        if p not in files:
            sys.exit(f"REFUSED: the manifest does not list {p}")
    if files[FINAL]["sha256"] != files[DRAFT]["sha256"]:
        sys.exit(f"REFUSED: {FINAL} is not a byte copy of {DRAFT}")
    msha = hashlib.sha256((ROOT / MANIFEST).read_bytes()).hexdigest()
    if sha_at(ref, MANIFEST) != msha:
        sys.exit(f"REFUSED: the manifest on disk differs from the manifest at {ref}")
    files[MANIFEST] = {"sha256": msha, "git_blob": git("rev-parse", f"{ref}:{MANIFEST}")}
    if git("rev-parse", f"{A_TAG}^{{commit}}") != A_COMMIT:
        sys.exit(f"REFUSED: {A_TAG} does not point to {A_COMMIT}")
    a_blobs = {}
    for p in A_INPUTS:
        b = git("rev-parse", f"{A_TAG}:{p}")
        if b != files[p]["git_blob"]:
            sys.exit(f"REFUSED: {p} at {ref} is blob {files[p]['git_blob']}, at {A_TAG} {b}")
        a_blobs[p] = b
    if files[A_SCORER]["sha256"] != A_SCORER_SHA256:
        sys.exit(f"REFUSED: Paper A's scorer SHA-256 {files[A_SCORER]['sha256']} is not v1.12's locked {A_SCORER_SHA256}")
    tagger = None if a.ref else git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{TAG}")
    a_data_origin = git("ls-tree", "-r", "--name-only", "refs/remotes/origin/v1.12", "--", A_DATA)
    rec = {
        "phase": "v1.19", "study": "Coverage Paper B (re-analysis: #32, #34, #35, #36)", "revision": "r1",
        "tag": TAG, "tag_object": git("rev-parse", ref), "commit": commit, "tree": git("rev-parse", f"{ref}^{{tree}}"),
        "branch": "v1.19", "tagger_date": tagger, "remote_tag_refs": remote,
        "recorded_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": git("remote", "get-url", "origin", check=False),
        "osf_deposit": f"https://osf.io/ec6wh/ (osfstorage: {', '.join(f'{OSF_BASE}/{f}' for f in OSF_FOLDERS)}; "
                       f"{OSF_BASE}/draft_r0 and draft_r1 hold the drafts the pre-registrant received)",
        "osf_verified": None if a.ref else osf_check(ref),
        "lock_manifest": {"path": MANIFEST, "sha256": msha, "files_listed": n_listed},
        "final_text": {"path": FINAL, "byte_copy_of": DRAFT, "sha256": files[FINAL]["sha256"]},
        "locked_files": files,
        "paper_A_pins": {"tag": A_TAG, "commit": A_COMMIT, "blobs": a_blobs, "scorer_sha256": A_SCORER_SHA256},
        "paper_A_answers": {f"{A_DATA}_in_this_tree": (ROOT / A_DATA).exists(),
                            f"{A_DATA}_files_on_origin_v1.12": len(a_data_origin.splitlines()) if a_data_origin else 0,
                            "collection_window_opens_utc": A_WINDOW_OPENS_UTC,
                            "tag_before_window_opens": None if not tagger else
                            datetime.datetime.fromisoformat(tagger) < datetime.datetime.fromisoformat(A_WINDOW_OPENS_UTC)},
        "scoring": {"output_dir": f"{D}/outputs", "command": "score_v1_19.py --run (once; refuses unless the tag is on "
                    "origin, this file names its commit, Paper A's v112_verdicts.json and v112_unit_table.csv exist "
                    "and outputs/ is empty; section 9.2)"},
    }
    if a.ref:
        rec["TEST_ONLY"] = f"blobs read at {a.ref}, not at the tag; origin and OSF not checked; not an anchor"
    text = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
    if a.dry_run:
        print(text)
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT} (tag {TAG} -> commit {commit}; {len(files)} locked files incl. the manifest)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
