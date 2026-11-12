#!/usr/bin/env python3
"""Freeze the v1.19 phantom roster (#34) from existing records only; no Coverage answer is read, none exists.

Recall-floor flag (F): status == "undefined" in osf/v31/data/v31_cpc.csv (set "omnibus"), i.e. mean recall < 1.0
across the six legacy models at t1: the frozen flags v0.33 (H_Provider_Phantom), v0.34 (t1 phantom set) and v0.35
(Naive-Phantom x CPC) consumed (v0.35 prereg PHANTOM_CLASSIFICATION; score_v35.py, FLOOR = 1.0).
Defunct (D): the v0.22 registry's Cell_D_Defunct (prereg/v0_22_registry.json), Paper A's MC_Defunct list.
Fisker (v0.22 Cell_B_Disruptor) is listed in its own column because v1.12 section 10 names it beside cell D;
whether it joins D is decision D4 of the pre-registration (default: no).

Run from the repository root: python3 osf/methodology/v1_19/prereg/build_roster_v1_19.py
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "osf/v31/data/v31_cpc.csv"
REG22 = ROOT / "prereg/v0_22_registry.json"
OUT = Path(__file__).resolve().parent / "phantom_roster_v1_19.csv"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    rows = [r for r in csv.DictReader(SRC.open(encoding="utf-8")) if r["set"] == "omnibus"]
    cell_d = [b["name"] for b in json.loads(REG22.read_text(encoding="utf-8"))["cells"]["D"]["brands"]]
    out = []
    for r in rows:
        out.append({"substrate": r["substrate"], "brand": r["brand"], "cell_t1": r["cell"],
                    "mean_recall_t1": r["mean_r"], "recall_floor_flag_F": int(r["status"] == "undefined"),
                    "defunct_D": int(r["substrate"] == "v0.22" and r["brand"] in cell_d),
                    "fisker_D4": int(r["substrate"] == "v0.22" and r["brand"] == "Fisker")})
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(json.dumps({"units": len(out), "F": sum(r["recall_floor_flag_F"] for r in out),
                      "D": sum(r["defunct_D"] for r in out), "source_sha256": sha(SRC),
                      "registry_v0_22_sha256": sha(REG22), "roster_sha256": sha(OUT)}, indent=1))


if __name__ == "__main__":
    main()
