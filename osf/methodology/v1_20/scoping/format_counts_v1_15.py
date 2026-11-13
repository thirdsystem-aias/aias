#!/usr/bin/env python3
"""v1.20 r0 — parser demonstration on v1.15's stored judge replies (format counts only).

Read-only. Reads v1.15's frozen raw judge records and its unit table (unit_id and set columns only),
checks the raw file against the SHA-256 in v1.15's frozen-outputs record, and counts reply formats and
parse outcomes under v1.15's rule (v1.11's locked parser and outcome rule, which v1.15 imported
unchanged) and under the v1.20 rule. It never reads, prints or writes a valence, an evidence quote, a
reply text or any score. v1.15's own result (Stage J halt, DEVIATIONS Entry 2) is not changed by this.

Usage (repository root of the sentiment-successor worktree):
  PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_20/scoping/format_counts_v1_15.py \
      --v115 /Users/pablou/aias/_worktrees/v1.15/osf/methodology/v1_15 \
      --out osf/methodology/v1_20/scoping/format_counts_v1_15.json
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402
import score_v1_20 as R  # noqa: E402


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--v115", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    a = ap.parse_args(argv)
    raw_p = a.v115 / "data/judge_raw_v1_15.jsonl"
    frozen_p = a.v115 / "outputs/judge_outputs_frozen_v1_15.json"
    units_p = a.v115 / "prereg/units_v1_15.csv"

    def rel(p: Path) -> str:
        try:
            return str(p.resolve().relative_to(a.v115.resolve().parents[2]))
        except ValueError:
            return p.name

    frozen = json.loads(frozen_p.read_text(encoding="utf-8"))
    got = sha256(raw_p)
    if got != frozen["raw_sha256"]:
        print(f"STOP: raw file SHA-256 {got} differs from the frozen record {frozen['raw_sha256']}")
        return 2
    roles = frozen["roles"]
    recs = [json.loads(x) for x in raw_p.read_text(encoding="utf-8").splitlines() if x.strip()]
    csv.field_size_limit(sys.maxsize)
    with open(units_p, encoding="utf-8", newline="") as f:
        set_of = {row["unit_id"]: row["set"] for row in csv.DictReader(f)}

    per = defaultdict(Counter)
    for r in recs:
        if roles.get(r["role"]) != r["judge_model"]:
            per["other_model"]["records"] += 1
            continue
        c = per[f"{r['role']} {r['pass']}"]
        c["records"] += 1
        c[f"attempt={r['attempt']}"] += 1
        c[f"status={r.get('status')}"] += 1
        c[f"served_ok={bool(r.get('served_ok'))}"] += 1
        c[f"cut_by_cap={R.cut_by_cap(r.get('finish_reason'))}"] += 1
        cl = R.classify(r.get("text") or "")
        c[f"shape={cl['shape']}"] += 1
        c[f"shape={cl['shape']} fenced={cl['fenced']}"] += 1
        if cl["object_checks"] and cl["object_checks"] != "pass":
            c[f"one_object_fails_v111_checks={cl['object_checks']}"] += 1
        ok_rec = r.get("status") == "ok" and bool(r.get("served_ok"))
        v111 = ok_rec and cl["v111_valid"]
        v120 = R.record_judgement(r) is not None
        c["reply_valid_v1.15_rule"] += int(v111)
        c["reply_valid_v1.20_rule"] += int(v120)
        c[f"attempt={r['attempt']} valid_v1.15={v111} valid_v1.20={v120}"] += 1
        c[f"attempt={r['attempt']} shape={cl['shape']} fenced={cl['fenced']}"] += 1
        if v111 and not v120:
            c["ANOMALY_valid_v1.15_not_v1.20"] += 1

    oc_old, oc_new = S.outcomes(recs, roles), R.outcomes(recs, roles)
    units = defaultdict(Counter)
    fails = defaultdict(Counter)
    for k in sorted(set(oc_old) | set(oc_new)):
        role, uid, pas = k
        o = oc_old.get(k, {"status": S.UNJUDGED})["status"]
        n = oc_new.get(k, {"status": S.UNJUDGED})["status"]
        u = units[f"{role} {pas}"]
        u[f"v1.15_rule={o}"] += 1
        u[f"v1.20_rule={n}"] += 1
        u[f"{o} -> {n}"] += 1
        if n == S.VALID:
            u[f"v1.20_attempt_used={oc_new[k]['attempt_used']}"] += 1
        if pas == "main":
            f_ = fails[f"{role} {set_of.get(uid, 'UNKNOWN_SET')}"]
            f_["units"] += 1
            f_["judge_fail_v1.15_rule"] += int(o == S.FAIL)
            f_["judge_fail_v1.20_rule"] += int(n == S.FAIL)
    fail_tab = {}
    for k, c in sorted(fails.items()):
        row = dict(c)
        for rule in ("v1.15_rule", "v1.20_rule"):
            share = c[f"judge_fail_{rule}"] / c["units"] if c["units"] else None
            row[f"share_{rule}"] = None if share is None else round(share, 6)
            row[f"over_2pct_{rule}"] = share is not None and share > S.JUDGE_FAIL_HALT_SHARE
        fail_tab[k] = row

    doc = {"what": "v1.20 r0 parser demonstration on v1.15's stored judge replies: format counts only "
                   "(no valence, evidence, reply text or score read out or computed)",
           "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "inputs": {"where": "branch v1.15 worktree (paths relative to its root)",
                      "raw": rel(raw_p), "raw_sha256": got, "raw_sha256_frozen_record": frozen["raw_sha256"],
                      "frozen_record": rel(frozen_p), "units": rel(units_p), "units_sha256": sha256(units_p),
                      "records": len(recs), "roles": roles},
           "rules": {"v1.15_rule": "score_v1_11.outcomes + parse_judge_output (v1.11-prereg-r1), as v1.15 imported them",
                     "v1.20_rule": "score_v1_20.outcomes + record_judgement (exactly one complete top-level JSON object "
                                   "passing v1.11's checks; surrounding text ignored; cap-cut and served-model rules kept)"},
           "records_by_judge_pass": {k: dict(sorted(v.items())) for k, v in sorted(per.items())},
           "units_by_judge_pass": {k: dict(sorted(v.items())) for k, v in sorted(units.items())},
           "judge_fail_main_pass_by_set": fail_tab}
    a.out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: doc[k] for k in ("records_by_judge_pass", "units_by_judge_pass")}, indent=1))
    print(json.dumps(fail_tab, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
