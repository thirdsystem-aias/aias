#!/usr/bin/env python3
"""
make_run_values_v1_20.py -- the small values file for the Sentiment Paper A judge-run record (descriptive only).

The scorer's outputs (v1.11 frozen record, v1.20 Stage J/C, the comparison file) carry the run totals, the outcomes
and the verdicts. Pre-registration v1.11 section 6.5 also lists the served-model and finish-reason counts and the
reasoning tokens per judge, which no scorer output writes. This script reads them from the call records
`osf/methodology/v1_11/data/judge_raw_v1_11.jsonl` (metadata fields only: role, pass, attempt, status, served model,
finish reason, token counts, usd, mode, batch id, time stamps; the reply `text` and the `request` body are never read
into the output) after checking that the file's SHA-256 equals `raw_sha256` in the frozen record. No verdict depends
on these values. Output: papers/v1_20/run_values_v1_20.json (counts, sums, the run window, and the SHA-256 checked).

Usage (repository or worktree root):  python3 papers/v1_20/make_run_values_v1_20.py
"""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "osf/methodology/v1_11/data/judge_raw_v1_11.jsonl"
FROZEN = ROOT / "osf/methodology/v1_11/outputs/judge_outputs_frozen_v1_11.json"
OUT = Path(__file__).resolve().parent / "run_values_v1_20.json"
FIELDS = ("role", "pass", "attempt", "status", "served_model", "served_ok", "finish_reason", "input_tokens",
          "output_tokens", "thinking_tokens", "usd", "mode", "batch_id", "started_utc", "finished_utc", "error")


def main():
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    sha = hashlib.sha256(RAW.read_bytes()).hexdigest()
    if sha != frozen["raw_sha256"]:
        sys.exit(f"REFUSED: {RAW.name} SHA-256 {sha} != frozen raw_sha256 {frozen['raw_sha256']}")
    n = 0
    by_role = defaultdict(Counter)
    status, finish, served, mode = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter), Counter()
    tok = defaultdict(lambda: {"input_tokens": 0, "output_tokens": 0, "thinking_tokens": 0, "thinking_reported": 0})
    usd = defaultdict(float)
    batches = defaultdict(set)
    first, last = None, None
    errors = 0
    for line in RAW.open(encoding="utf-8"):
        rec = json.loads(line)
        r = {k: rec.get(k) for k in FIELDS}           # metadata only; text and request are dropped here
        n += 1
        role = r["role"]
        by_role[role][f"{r['pass']}|attempt {r['attempt']}"] += 1
        status[role][str(r["status"])] += 1
        finish[role][str(r["finish_reason"])] += 1
        served[role][str(r["served_model"])] += 1
        mode[str(r["mode"])] += 1
        for k in ("input_tokens", "output_tokens"):
            tok[role][k] += int(r[k] or 0)
        if r["thinking_tokens"] is not None:
            tok[role]["thinking_tokens"] += int(r["thinking_tokens"])
            tok[role]["thinking_reported"] += 1
        usd[role] += float(r["usd"] or 0)
        if r["batch_id"]:
            batches[role].add(r["batch_id"])
        if r["error"] or r["status"] != "ok":
            errors += 1
        for t in (r["started_utc"], r["finished_utc"]):
            if t:
                first = t if first is None or t < first else first
                last = t if last is None or t > last else last
    doc = {"source": str(RAW.relative_to(ROOT)), "raw_sha256": sha, "matches_frozen_raw_sha256": True,
           "records": n, "records_with_error_or_status_not_ok": errors,
           "records_by_role": {k: sum(v.values()) for k, v in by_role.items()},
           "records_by_role_pass_attempt": {k: dict(sorted(v.items())) for k, v in by_role.items()},
           "status_by_role": {k: dict(v) for k, v in status.items()},
           "finish_reason_by_role": {k: dict(v) for k, v in finish.items()},
           "served_model_by_role": {k: dict(v) for k, v in served.items()},
           "mode": dict(mode), "batches_by_role": {k: len(v) for k, v in batches.items()},
           "tokens_by_role": {k: dict(v) for k, v in tok.items()},
           "usd_by_role": {k: round(v, 6) for k, v in usd.items()},
           "usd_total": round(sum(usd.values()), 6), "first_utc": first, "last_utc": last}
    OUT.write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({n} records, {errors} with an error)")


if __name__ == "__main__":
    main()
