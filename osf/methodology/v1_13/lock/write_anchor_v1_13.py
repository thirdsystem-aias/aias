#!/usr/bin/env python3
"""Write the v1.13 anchor files after the tags are pushed (LOCK_STEPS.md steps 4, 7 and 9).

  (default)        anchor/git_anchor_v1_13.json   Part I, tag v1.13-prereg-r1 (read by score_v1_13.py: locked_files,
                   conditional_legs). Records the tag, its commit and tree, every file of LOCK_MANIFEST_v1_13.sha256
                   (SHA-256 and git blob at the tag), the activation record of H4-H6 (section 3), the v0.42 pins.
  --audit          anchor/audit_anchor_v1_13.json Part II, tag v1.13-audit-r1 (read by audit_v1_13.py --collect:
                   commit, brand_domains_sha256).
  --receipt TIME   anchor/audit_receipt_v1_13.json: when Pablo received the locked Part II text (ISO 8601 with a
                   UTC offset, e.g. 2026-11-11T22:05:00+00:00; a time without offset is refused because the audit
                   guard compares it with an aware UTC clock).

Writes only the named file. Network: `git ls-remote` only (read-only). --dry-run prints instead of writing;
--ref REV (with --dry-run, testing only) reads blobs at REV instead of the tag, skips the origin checks of the
v1.13 tags and marks the record TEST_ONLY.
"""
import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PH = "osf/methodology/v1_13"
MANIFEST = f"{PH}/prereg/LOCK_MANIFEST_v1_13.sha256"
TAG_I, TAG_II = "v1.13-prereg-r1", "v1.13-audit-r1"
OUT_I = ROOT / PH / "anchor/git_anchor_v1_13.json"
OUT_II = ROOT / PH / "anchor/audit_anchor_v1_13.json"
OUT_RECEIPT = ROOT / PH / "anchor/audit_receipt_v1_13.json"
DOMAINS = f"{PH}/registries/brand_domains_v1_13.csv"
CLASSES = f"{PH}/prereg/source_classes_v1_13.md"
PART_II_FILES = [f"{PH}/prereg/website_audit_protocol_v1_13.md", f"{PH}/registries/wikidata_types_v1_13.csv",
                 f"{PH}/prereg/dry_run_audit_v1_13.txt", f"{PH}/scripts/audit_v1_13.py",
                 f"{PH}/scripts/tests/test_audit_v1_13.py", DOMAINS, CLASSES]   # fixtures added from the manifest
V114_TAG, V114_COMMIT = "v1.14-prereg-r2", "a5feb4b1c4b9e9d19979129afcfd616a50b88c64"   # section 12 (y); r1 was 20fbc342
V114_FILES = ["osf/methodology/v1_14/prereg/PRE_REGISTRATION_v1_14.md", "scripts/score_v1_14.py"]
V112_TAG = "v1.12-prereg-r1"
V112_FILES = ["osf/methodology/v1_12/prereg/PRE_REGISTRATION_v1_12.md", "osf/methodology/v1_12/scripts/score_v1_12.py"]
V111_TAG = "v1.11-prereg-r1"
V042_TAG = "v0.42-prereg-r1"
V042_PINS = {"osf/v42/scripts/code_t4_v0_42.py": "2d36735d512cf9e13b74010ba5a7f655fc7de0bc",
             "osf/v42/scripts/score_v0_42.py": "934f09ae69300cb13bdde56c7964b7b2cc7700b9"}


def git(*a, check=True):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    if r.returncode:
        if check:
            sys.exit(f"git {' '.join(a)} failed: {r.stderr.strip()}")
        return None
    return r.stdout.strip()


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def blob_sha256(spec):
    r = subprocess.run(["git", "-C", str(ROOT), "show", spec], capture_output=True)
    return hashlib.sha256(r.stdout).hexdigest() if r.returncode == 0 and r.stdout else None


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def on_origin(tag):
    out = git("ls-remote", "--tags", "origin", tag, check=False) or ""
    return out if f"refs/tags/{tag}" in out else ""


def manifest_files(ref):
    files = {}
    for line in (ROOT / MANIFEST).read_text(encoding="utf-8").splitlines():
        h, p = line.split(None, 1)
        p = p.strip()
        if sha(p) != h:
            sys.exit(f"REFUSED: {p} on disk ({sha(p)[:12]}) differs from the manifest ({h[:12]})")
        files[p] = {"sha256": h, "git_blob": git("rev-parse", f"{ref}:{p}")}
    files[MANIFEST] = {"sha256": sha(MANIFEST), "git_blob": git("rev-parse", f"{ref}:{MANIFEST}")}
    return files


def tag_record(tag, ref, testing):
    remote = "" if testing else on_origin(tag)
    if not testing and not remote:
        sys.exit(f"REFUSED: tag {tag} is not on origin; push it first (LOCK_STEPS.md)")
    return {"tag": tag, "tag_object": git("rev-parse", ref), "commit": git("rev-parse", f"{ref}^{{commit}}"),
            "tree": git("rev-parse", f"{ref}^{{tree}}"), "branch": "v1.13",
            "commit_date": git("log", "-1", "--format=%cI", f"{ref}^{{commit}}"),
            "tagger_date": None if testing else git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{tag}"),
            "remote_tag_ref": remote, "recorded_utc": now_utc(),
            "repository": "https://github.com/thirdsystem-aias/aias"}


def legs(commit_date, testing, h6_inactive=None):
    v114_commit = git("rev-parse", f"{V114_TAG}^{{commit}}")
    if v114_commit != V114_COMMIT:
        sys.exit(f"REFUSED: {V114_TAG} resolves to {v114_commit}, not {V114_COMMIT}")
    v114_remote = on_origin(V114_TAG)
    if not v114_remote:
        sys.exit(f"REFUSED: {V114_TAG} is not on origin")
    out = {"H4_Sep_Ranking": {
        "pushed_before_lock": True, "tag": V114_TAG, "remote_tag_ref": v114_remote, "commit": v114_commit,
        "score_definition_files": {p: git("rev-parse", f"{V114_TAG}:{p}") for p in V114_FILES},
        "score": "v1.14's R*_S1, read from osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json (SHA-256 recorded "
                 "at scoring); may downgrade only if v1.14's STAGE1_VERDICT is 'SEPARABLE (Stage 2 pending)' "
                 "(section 3, section 12 (g), N17-N19)"}}
    out["H5_Sep_Sentiment"] = {
        "pushed_before_lock": False, "t4_answers": False,
        "status": "INACTIVE: no locked Sentiment score on the t4 answers was pushed before this lock; v1.11-prereg-r1 "
                  "defines its score on the archived waves only (section 12 (i), N20)",
        "v1.11_remote_tag_ref": on_origin(V111_TAG)}
    v112_remote = on_origin(V112_TAG)
    v112_local = git("rev-parse", f"{V112_TAG}^{{commit}}", check=False)
    h6 = {"tag": V112_TAG, "remote_tag_ref": v112_remote, "commit": v112_local}
    if h6_inactive:
        h6.update({"pushed_before_lock": False,
                   "status": f"INACTIVE by the runner's decision recorded before the lock: {h6_inactive}"})
    elif v112_remote and v112_local:
        v112_date = git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{V112_TAG}")
        before = datetime.datetime.fromisoformat(v112_date) < datetime.datetime.fromisoformat(commit_date)
        if not before and not testing:
            sys.exit(f"REFUSED: {V112_TAG} (tagged {v112_date}) is on origin but the v1.13 lock commit is older "
                     f"({commit_date}): make the lock commit after v1.12's push (LOCK_STEPS.md step 2), or pass --h6-inactive "
                     f"REASON with the runner's decision logged in section 12")
        h6.update({"pushed_before_lock": before, "v1.12_tagger_date": v112_date, "v1.13_lock_commit_date": commit_date,
                   "score_definition_files": {p: git("rev-parse", f"{V112_TAG}:{p}", check=False) for p in V112_FILES},
                   "scorer_sha256_at_tag": blob_sha256(f"{V112_TAG}:{V112_FILES[1]}"),
                   "score": "v1.12's locked Cov* on its own collection (112 units, N3, S0): score_v1_13.py --h6-cov "
                            "reads column cov_star_N3 of osf/methodology/v1_12/v112_unit_table.csv, refusing it unless "
                            "v112_verdicts.json beside it names this scorer SHA-256 and a passed P1 (section 12 (x), "
                            "N21); PENDING at Stage C1 until it exists, computed at Stage C2, else UNDETERMINED and "
                            "handed to Paper B (section 3, N10)",
                   "status": "ACTIVE (v1.12-prereg-r1 pushed before the v1.13 lock commit)" if before else
                             "INACTIVE (TEST_ONLY reading: lock commit older than v1.12's tag)"})
    else:
        h6.update({"pushed_before_lock": False,
                   "status": "INACTIVE: v1.12-prereg-r1 was not on origin (or not present locally) when this anchor "
                             "was written"})
    out["H6_Sep_Coverage"] = h6
    return out


def part_i(a):
    ref, testing = a.ref or TAG_I, bool(a.ref)
    rec = tag_record(TAG_I, ref, testing)
    rec["phase"], rec["part"] = "v1.13", "I [RE-ANALYSIS: t4]"
    rec["osf_deposit"] = "https://osf.io/ec6wh/ (osfstorage: methodology/v1_13/prereg, /registries, /anchor)"
    rec["locked_files"] = manifest_files(ref)
    rec["brand_domains_sha256"] = sha(DOMAINS)
    rec["source_classes_sha256"] = sha(CLASSES)
    rec["conditional_legs"] = legs(rec["commit_date"], testing, a.h6_inactive)
    v042_remote = on_origin(V042_TAG)
    rec["v0_42"] = {"tag": V042_TAG, "tag_on_origin": bool(v042_remote), "remote_tag_ref": v042_remote,
                    "pins": {p: {"pinned": b, "at_tag_locally": git("rev-parse", f"{V042_TAG}:{p}", check=False)}
                             for p, b in V042_PINS.items()},
                    "note": "re-checked by MQ7 at Stage C1 if the tag does not exist at this lock (section 0); "
                            "a difference is logged in DEVIATIONS.md before Stage C1"}
    rec["t4_raw_sha256"] = None
    rec["t4_raw_note"] = "recorded before the first read of osf/v42/data/t4_raw.jsonl (section 0), not at the lock"
    return rec, OUT_I


def part_ii(a):
    ref, testing = a.ref or TAG_II, bool(a.ref)
    rec = tag_record(TAG_II, ref, testing)
    rec["phase"], rec["part"] = "v1.13", "II [NEW WEB DATA: audit]"
    rec["osf_deposit"] = "https://osf.io/ec6wh/ (osfstorage: methodology/v1_13/anchor)"
    rec["brand_domains_sha256"] = sha(DOMAINS)
    man = {}
    for line in (ROOT / MANIFEST).read_text(encoding="utf-8").splitlines():
        h, p = line.split(None, 1)
        man[p.strip()] = h
    paths = PART_II_FILES + sorted(p for p in man if "/scripts/fixtures/audit/" in p)
    files = {}
    for p in paths:
        if sha(p) != man.get(p):
            sys.exit(f"REFUSED: {p} differs from the manifest or is not in it")
        files[p] = {"sha256": man[p], "git_blob": git("rev-parse", f"{ref}:{p}")}
    rec["locked_files"] = files
    rec["prereg_tag_commit"] = git("rev-parse", f"{TAG_I}^{{commit}}", check=False)
    rec["run_window"] = ("pass 1 >= 24 h after the receipt and only if its 72 h end before 2026-11-17T00:00Z, else "
                         "from 2026-11-22T12:00Z; no request 2026-11-17T00:00Z to 2026-11-22T12:00Z (protocol section 4)")
    return rec, OUT_II


def receipt(a):
    t = datetime.datetime.fromisoformat(a.receipt)
    if t.tzinfo is None:
        sys.exit("REFUSED: --receipt needs a UTC offset (e.g. 2026-11-11T22:05:00+00:00)")
    t = t.astimezone(datetime.timezone.utc)
    if not a.dry_run and not on_origin(TAG_II):
        sys.exit(f"REFUSED: {TAG_II} is not on origin; the receipt is for the locked Part II text")
    return {"received_utc": t.isoformat(), "audit_tag": TAG_II, "recorded_utc": now_utc(),
            "earliest_pass1_utc": (t + datetime.timedelta(hours=24)).isoformat(),
            "note": "when Pablo received the locked Part II text (protocol section 8); written by the runner"}, OUT_RECEIPT


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--audit", action="store_true", help="Part II anchor (tag v1.13-audit-r1)")
    g.add_argument("--receipt", metavar="ISO_TIME", help="Part II receipt time")
    ap.add_argument("--h6-inactive", metavar="REASON", help="Part I: record H6 INACTIVE by the runner's decision (logged in section 12 before the lock) instead of reading the order of the tags")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--ref", default=None, help="testing only (with --dry-run): read blobs at this revision")
    a = ap.parse_args()
    if a.ref and not a.dry_run:
        sys.exit("--ref is for testing and needs --dry-run")
    rec, out = receipt(a) if a.receipt else part_ii(a) if a.audit else part_i(a)
    if a.ref:
        rec["TEST_ONLY"] = f"blobs read at {a.ref}, not at the tag; v1.13 tag origin checks skipped; not an anchor"
    text = json.dumps(rec, indent=2, ensure_ascii=False) + "\n"
    if a.dry_run:
        print(text)
        return 0
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}" + (f" (commit {rec['commit']}, {len(rec['locked_files'])} files)"
                                               if "locked_files" in rec else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
