#!/usr/bin/env python3
"""
run_stage_v1_13.py -- runs the LOCKED score_v1_13.py unchanged and records the SHA-256 of every input it is given in a
sidecar file (postlock/DEVIATIONS_continued_v1_13.md, Entries 3 and 10). NOT a locked file.

The locked verdict file records no input hashes (t4 raw file, v0.42 coder tables, v0.42 brand table, v1.14 Stage 1
output, v1.12 unit table) and Stage C2 does not record the SDRI table it reads, nor when "Part II collected" was
decided. This wrapper hashes the inputs BEFORE the scorer runs (bytes only; nothing is parsed or scored here), runs
`python3 score_v1_13.py <the same arguments>` as a subprocess, then hashes the verdict file it wrote, and writes
`<out dir>/v1_13_inputs_<stage>.json` (refusing to overwrite one). At Stage C2 it records whether the SDRI table
existed at the moment C2 started (the scorer's own test: `Path(--sdri).exists()`) and, if so, its SHA-256.

  python3 osf/methodology/v1_13/postlock/run_stage_v1_13.py -- --stage C1 --t4 T --coded D --brand-table B \
      [--h4-stage1 F] [--h6-cov F] [--out V]
  python3 osf/methodology/v1_13/postlock/run_stage_v1_13.py -- --stage C2 --t4 T --coded D --brand-table B \
      [--h4-stage1 F | --h4-unavailable R] [--h6-cov F | --h6-unavailable R] [--sdri S] [--out V]

Exit status = the scorer's. A run the scorer refuses is recorded too, under v1_13_inputs_<stage>_exit<N>_<time>.json.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
SCORER = PHASE / "scripts" / "score_v1_13.py"
DEFAULT_OUT = PHASE / "v1_13_verdicts.json"
DEFAULT_SDRI = PHASE / "audit" / "v1_13_sdri.csv"
SUBSTRATES = ("v19", "v20", "v21", "v22", "v23")


def sha(p):
    p = Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def entry(p):
    if p is None:
        return None
    p = Path(p)
    return {"path": str(p), "exists": p.is_file(), "sha256": sha(p), "bytes": p.stat().st_size if p.is_file() else None}


def parse(args):
    ap = argparse.ArgumentParser(add_help=False)
    for f in ("--stage", "--t4", "--coded", "--brand-table", "--sdri", "--out", "--h4-stage1", "--h4-unavailable",
              "--h6-cov", "--h6-unavailable"):
        ap.add_argument(f)
    a, _ = ap.parse_known_args(args)
    return a


def inputs(a):
    rec = {"t4_raw": entry(a.t4), "brand_table": entry(a.brand_table), "coded": {}}
    if a.coded:
        for s in SUBSTRATES:
            for ph in ("a", "b"):
                p = Path(a.coded) / f"{s}_phase_{ph}.csv"
                rec["coded"][p.name] = entry(p)
    if a.h4_stage1:
        rec["h4_stage1"] = entry(a.h4_stage1)
        rec["h4_rank_table"] = entry(Path(a.h4_stage1).parent / "rank_table_t4_v1_14.csv")
    if a.h6_cov:
        rec["h6_unit_table"] = entry(a.h6_cov)
        rec["h6_verdicts"] = entry(Path(a.h6_cov).parent / "v112_verdicts.json")
    if a.stage == "C2":
        sd = Path(a.sdri) if a.sdri else DEFAULT_SDRI
        e = entry(sd)
        rec["sdri"] = dict(e, part2_collected_at_c2_start=e["exists"],
                           rule="Part II counts as collected before Stage C2 iff this file existed when C2 started "
                                "(the scorer's own test, Path(--sdri).exists())")
    return rec


def main(argv=None, scorer=SCORER):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--":
        argv = argv[1:]
    a = parse(argv)
    if a.stage not in ("C1", "C2"):
        sys.exit("REFUSED: pass the scorer's arguments after --, with --stage C1 or C2")
    out = Path(a.out) if a.out else DEFAULT_OUT
    side = out.parent / f"v1_13_inputs_{a.stage}.json"
    if side.exists():
        sys.exit(f"REFUSED: {side} exists (one record per stage)")
    started = datetime.now(timezone.utc).isoformat()
    rec = {"stage": a.stage, "started_utc": started, "scorer": entry(scorer), "wrapper_sha256": sha(__file__),
           "argv": argv, "inputs": inputs(a), "verdict_file_before": entry(out)}
    r = subprocess.run([sys.executable, str(scorer)] + argv, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    rec.update(finished_utc=datetime.now(timezone.utc).isoformat(), scorer_exit=r.returncode,
               scorer_stdout=r.stdout[-2000:], scorer_stderr=r.stderr[-2000:], verdict_file_after=entry(out))
    if r.returncode != 0:                              # a refused run never blocks the real record
        side = side.with_name(f"v1_13_inputs_{a.stage}_exit{r.returncode}_{started[:19].replace(':', '')}.json")
    side.parent.mkdir(parents=True, exist_ok=True)
    side.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    print(f"[run_stage_v1_13] inputs recorded -> {side}")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
