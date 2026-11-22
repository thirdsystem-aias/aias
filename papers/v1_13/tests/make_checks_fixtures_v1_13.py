#!/usr/bin/env python3
"""
make_checks_fixtures_v1_13.py -- SYNTHETIC Part II audit-check fixtures for the fill tests. SYNTHETIC DATA ONLY.

For every committed scenario whose Part II was collected (SYNTHETIC_<scenario>_v1_13_sdri.csv exists), builds
synthetic pass-1 and pass-2 audit records from that SDRI table (P1 outcome as the table records it; status 200 when ok;
schema.org types and sameAs set from indicators (1)-(5); one JSON-LD block per ok page; in pass 2 the first ok unit
loses its Product type, so AQ4 has one change), and runs the postlock script's own run() (audit_checks_v1_13.py,
imported read-only) with the scenario's verdict file. Writes SYNTHETIC_<scenario>_v1_13_audit_checks.json next to
the fixtures, marked synthetic_fixture. The numbers are not meaningful; only the wording and the provenance are under
test.

  python3 papers/v1_13/tests/make_checks_fixtures_v1_13.py
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FX = HERE / "fixtures"
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "osf/methodology/v1_13/postlock"))
sys.dont_write_bytecode = True
import audit_checks_v1_13 as AC  # noqa: E402  (read-only: its run() on synthetic records)

SCENARIOS = ["scored", "pass_reported", "downgraded", "downgraded_h6", "c1_h4", "h3_undetermined", "dropped", "floor"]


def records_from(rows, pass2=False):
    recs, changed = [], False
    for r in rows:
        ok = r["p1_outcome"] == "ok"
        types, same = [], []
        if ok:
            if r.get("i1") == "1":
                types.append("Organization")
            if r.get("i2") == "1":
                types.append("Brand")
            if r.get("i3") == "1" and not (pass2 and not changed):
                types.append("Product")
            elif r.get("i3") == "1":
                changed = True
            if r.get("i4") == "1":
                same.append("https://www.example.test/profile")
            if r.get("i5") == "1":
                same.append("https://www.wikidata.org/wiki/Q1")
        p1 = {"outcome": r["p1_outcome"], "status": 200 if ok else 403, "types": types, "same_as": same,
              "ld_blocks": 1 if ok else 0, "ld_errors": 0}
        recs.append({"substrate": r["substrate"], "brand_id": r["brand_id"], "phantom": r.get("phantom") == "1",
                     "domain": f"{r['brand_id'].lower()}.test", "pages": {"P1": p1}})
    return recs


def main():
    n = 0
    for s in SCENARIOS:
        sd = FX / f"SYNTHETIC_{s}_v1_13_sdri.csv"
        if not sd.exists():
            continue
        rows = list(csv.DictReader(sd.read_text(encoding="utf-8").splitlines()))
        V = json.loads((FX / f"SYNTHETIC_{s}_v1_13_verdicts.json").read_text(encoding="utf-8"))
        units = {(r["substrate"], r["brand_id"]): {"status": "RESOLVED"} for r in rows}
        out = AC.run(records_from(rows), records_from(rows, pass2=True), rows, V, units)
        out = json.loads(json.dumps(out, default=str))
        out["synthetic_fixture"] = {"scenario": s, "note": "SYNTHETIC: audit_checks_v1_13.run on synthetic records "
                                                           "built from the scenario's SDRI table; see "
                                                           "make_checks_fixtures_v1_13.py"}
        (FX / f"SYNTHETIC_{s}_v1_13_audit_checks.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
        n += 1
        print(f"{s}: AQ2 {out['AQ2']['p1_status_200']}/{out['AQ2']['units_with_domain']}, AQ4 changed "
              f"{out['AQ4']['changed']}, S_KG {out['S_KG'].get('band_reading_H7')}")
    print(f"wrote {n} fixtures")


if __name__ == "__main__":
    main()
