#!/usr/bin/env python3
"""Write v1.12's anchor/t4_complete_v1_12.json once t4 (v0.42) is finished (osf/v42/LOCK_STEPS.md step 10).

v1.12's collection guard (acquire_v1_12.t4_guard, v1.12 section 6.7) refuses --collect until this record exists and
reads exactly these fields: t4_raw_path (absolute), t4_raw_sha256, t4_last_call_utc, recorded_by. It refuses if the raw
file's SHA-256 changed since, if any raw line finished after t4_last_call_utc, or if t4_last_call_utc is not in the
past. Nothing else in the programme writes this file.

This script refuses unless: no acquire_v*.py --collect is running; the Message Batches journal has no batch in flight;
tag v0.42-acquisition-locked is on origin and the raw file at that tag is byte-identical to the file on disk (so the
record is written after the re-run pass and the acquisition lock). t4_last_call_utc = the latest started_utc or
finished_utc of any raw line. After writing, it runs v1.12's own t4_guard on the record (imported read-only from the
v1.12 worktree) and reports the result. Writes only --out. Network: `git ls-remote` (read-only).

Usage: python3 osf/v42/lock/write_t4_complete_v0_42.py [--dry-run] [--out PATH] [--v112-scripts DIR]
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path(__file__).resolve().parents[3])))
sys.path.insert(0, str(ROOT / "osf/v42/scripts"))
import acquire_v0_42 as AQ  # noqa: E402

ACQ_TAG = "v0.42-acquisition-locked"
RAW_REL = "osf/v42/data/t4_raw.jsonl"
V112 = Path("/Users/pablou/aias/_worktrees/v1.12/osf/methodology/v1_12")
OUT = V112 / "anchor" / "t4_complete_v1_12.json"


def git(*a, raw=False):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=not raw)
    if r.returncode:
        sys.exit(f"git {' '.join(a)} failed: {(r.stderr if not raw else r.stderr.decode()).strip()}")
    return r.stdout if raw else r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--v112-scripts", default=str(V112 / "scripts"))
    a = ap.parse_args()
    AQ.other_collection_guard()                                     # no paid collection may still be running
    if AQ.open_batches(AQ.BATCH_LOG):
        sys.exit("REFUSED: the batch journal shows a Message Batch in flight; run acquire_v0_42.py --collect to record it")
    raw = (ROOT / RAW_REL).resolve()
    if not raw.is_file():
        sys.exit(f"REFUSED: {raw} not found")
    remote = git("ls-remote", "--tags", "origin", ACQ_TAG)
    if f"refs/tags/{ACQ_TAG}" not in remote:
        sys.exit(f"REFUSED: tag {ACQ_TAG} is not on origin (LOCK_STEPS step 9 first)")
    data = raw.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    at_tag = hashlib.sha256(git("show", f"{ACQ_TAG}:{RAW_REL}", raw=True)).hexdigest()
    if at_tag != sha:
        sys.exit(f"REFUSED: {RAW_REL} on disk ({sha[:12]}) differs from the file at {ACQ_TAG} ({at_tag[:12]})")
    last, n, calls, answered = None, 0, set(), set()
    for line in data.decode("utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        n += 1
        calls.add(r["call_id"])
        if r.get("status") == "ok" and (r.get("text") or "").strip() and not r.get("error"):
            answered.add(r["call_id"])
        for k in ("started_utc", "finished_utc"):
            if r.get(k):
                t = datetime.fromisoformat(r[k])
                last = t if last is None or t > last else last
    if last is None or not last < datetime.now(timezone.utc):
        sys.exit(f"REFUSED: no usable call time, or the last call ({last}) is not in the past")
    rec = {"t4_raw_path": str(raw), "t4_raw_sha256": sha, "t4_last_call_utc": last.isoformat(),
           "recorded_by": "osf/v42/lock/write_t4_complete_v0_42.py (AIAS runner), v1.12 section 6.7",
           "recorded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "t4_acquisition_tag": ACQ_TAG, "t4_acquisition_commit": git("rev-parse", f"{ACQ_TAG}^{{commit}}"),
           "t4_raw_git_blob_at_tag": git("rev-parse", f"{ACQ_TAG}:{RAW_REL}"),
           "t4_raw_lines": n, "t4_calls_with_a_line": len(calls), "t4_calls_answered": len(answered),
           "t4_expected_calls": AQ.EXPECTED_TOTAL}
    text = json.dumps(rec, indent=2) + "\n"
    if a.dry_run:
        print(text)
        return 0
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out}")
    sys.path.insert(0, a.v112_scripts)
    try:
        import acquire_v1_12 as V112A
    except Exception as e:  # noqa: BLE001
        print(f"v1.12 t4_guard not run: cannot import acquire_v1_12 from {a.v112_scripts}: {e}")
        return 0
    V112A.T4_RECORD = out
    V112A.t4_guard(datetime.now(timezone.utc))                     # exits with REFUSED on any mismatch
    print("v1.12 t4_guard on this record: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
