#!/usr/bin/env python3
"""Step 2 (sensitivity only): scratch copies of the t3 folder osf/v41/data.

  full/     byte copy of osf/v41/data (baseline: must reproduce osf/v41/v41_verdicts.json)
  noflash/  same files with every gemini-2.5-flash row/record removed, in every file that
            carries a model field (v19 jsonl+csv, v20-v22 csv, v23 json, the interrupted v23
            run, and the provenance sidecar v41_provenance.csv). Exact id match after the
            'models/' prefix: gemini-2.5-flash-lite is kept. Logs are copied unchanged
            (no scorer reads them).

Usage: make_t3_copies.py SRC_DATA_DIR DST_DIR   (writes DST_DIR/full, DST_DIR/noflash,
       DST_DIR/noflash_filter_log.json). Reads SRC only.
"""
import csv
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

DROP = "gemini-2.5-flash"
FIELDS = ("panel_model", "model", "model_id", "alias", "returned_model_id")


def norm(v):
    return (v or "").strip().removeprefix("models/")


def is_drop(rec):
    return any(norm(rec.get(f)) == DROP for f in FIELDS if f in rec)


def models_of(recs):
    c = Counter()
    for r in recs:
        for f in FIELDS:
            if f in r:
                c[f"{f}={norm(r.get(f))}"] += 1
    return dict(c)


def main():
    src, dst = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    full, nof = dst / "full", dst / "noflash"
    for d in (full, nof):
        if d.exists():
            shutil.rmtree(d)
    shutil.copytree(src, full)
    shutil.copytree(src, nof)
    log = {}
    for p in sorted(nof.rglob("*")):
        if not p.is_file():
            continue
        rel = str(p.relative_to(nof))
        if p.suffix == ".jsonl":
            recs = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
            keep = [r for r in recs if not is_drop(r)]
            p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep), encoding="utf-8")
        elif p.suffix == ".csv":
            with open(p, newline="", encoding="utf-8") as f:
                rd = csv.DictReader(f)
                fields = rd.fieldnames
                recs = list(rd)
            keep = [r for r in recs if not is_drop(r)]
            with open(p, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(keep)
        elif p.suffix == ".json":
            recs = json.load(open(p, encoding="utf-8"))
            if not isinstance(recs, list):
                log[rel] = {"skipped": "not a list"}
                continue
            keep = [r for r in recs if not is_drop(r)]
            json.dump(keep, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        else:
            log[rel] = {"copied_unchanged": True}
            continue
        log[rel] = {"rows_in": len(recs), "rows_out": len(keep), "dropped": len(recs) - len(keep),
                    "models_after": models_of(keep)}
        assert not any(is_drop(r) for r in keep)
    json.dump(log, open(dst / "noflash_filter_log.json", "w"), indent=2)
    for k, v in log.items():
        print(k, {a: v[a] for a in ("rows_in", "rows_out", "dropped") if a in v} or v)


if __name__ == "__main__":
    main()
