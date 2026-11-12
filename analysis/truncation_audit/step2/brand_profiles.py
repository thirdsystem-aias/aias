#!/usr/bin/env python3
"""Step 2 (SENSITIVITY ONLY): per brand, per wave, the site's Presence P and Consistency C*
(AIAS 2.0 profiles = score_v1_9.unit_table on score_v41.wave_metrics, spec C_phi+FLOOR+ADD)
on all six models vs on the five models other than Gemini 2.5 Flash.

The six-model values are checked against the published osf/aias_2_0/aias_2_0_profiles.csv
(aias-2.0 branch; same 6-decimal formatting) and the script stops on any mismatch.
For v0.19 and v0.23 the five-model values are what variants (a) and (b) both give; for
v0.20-v0.22 they are variant (b) only (variant (a) keeps the six-model values there).

Run with AIAS_ROOT=<aias-2.0 worktree>:  brand_profiles.py --t3 DIR --published CSV --out CSV
"""
import os
import sys
from pathlib import Path

_root = Path(os.environ["AIAS_ROOT"])
sys.path.insert(0, str(_root / "osf/methodology/v1_9/scripts"))
sys.path.insert(0, str(_root / "osf/v41/scripts"))
import score_v1_9 as V19  # noqa: E402  (imports score_v41: HOME shim re-exec)

import argparse  # noqa: E402
import csv  # noqa: E402
import json  # noqa: E402

import score_v0_31 as S31  # noqa: E402

S = V19.S
PANEL = S31.PANEL
FULL = list(range(S.M))
FLASH = PANEL.index("gemini-2.5-flash")
NOFL = [i for i in FULL if i != FLASH]
CATEGORY = {"v0.19": "headphones", "v0.20": "v0.20", "v0.21": "v0.21", "v0.22": "v0.22",
            "v0.23": "premium spirits"}


def ranks_desc(vals):
    """competition rank, highest = 1 (ties share the best rank); None stays None."""
    out = {}
    defined = {k: v for k, v in vals.items() if v is not None}
    for k, v in defined.items():
        out[k] = 1 + sum(1 for w in defined.values() if w > v)
    return {k: out.get(k) for k in vals}


def f6(x):
    return "" if x is None else f"{x:.6f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t3", required=True)
    ap.add_argument("--published", required=True, help="osf/aias_2_0/aias_2_0_profiles.csv (aias-2.0)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = V19.SELECTED_SPEC
    base = Path(a.t3).resolve()
    waves = {"t1": S.load_wave(S.LAYOUT["t1"]), "t2": S.load_wave(S.LAYOUT["t2"]),
             "t3": S.load_wave(S._layout(base, base / "v23"))}
    names = {r["brand_id"]: r["brand_name"] for r in json.load(open(base / "v23" / "v23_phase_a_scored.json"))}
    pub = {(r["wave"], r["substrate"], r["brand"]): r for r in csv.DictReader(open(a.published, newline=""))}
    rows, mism = [], []
    for wv, wave in waves.items():
        wm6, wm5 = S.wave_metrics(wave, FULL), S.wave_metrics(wave, NOFL)
        u6 = {(x["s"], x["b"]): x for x in V19.unit_table(wm6, spec)}
        u5 = {(x["s"], x["b"]): x for x in V19.unit_table(wm5, spec)}
        for s in S.OMNI:
            keys = [k for k in u6 if k[0] == s]
            rP6 = ranks_desc({k: u6[k]["P"] for k in keys}); rP5 = ranks_desc({k: u5[k]["P"] for k in keys})
            rC6 = ranks_desc({k: u6[k]["C"] for k in keys}); rC5 = ranks_desc({k: u5[k]["C"] for k in keys})
            for k in sorted(keys, key=lambda k: k[1]):
                x6, x5, m6, m5 = u6[k], u5[k], wm6[s][k[1]], wm5[s][k[1]]
                p = pub.get((wv, s, k[1]))
                if p is None or (p["P"], p["C_star"], p["rated"], p["n_mentions"]) != (
                        f6(x6["P"]), f6(x6["C"]), str(int(x6["C"] is not None)), str(x6["n"])):
                    mism.append((wv, s, k[1]))
                dC = None if x6["C"] is None or x5["C"] is None else x5["C"] - x6["C"]
                rows.append({
                    "wave": wv, "substrate": s, "category": CATEGORY[s], "brand": k[1],
                    "brand_name": names.get(k[1], k[1]) if s == "v0.23" else k[1],
                    "k_per_model_6": json.dumps(m6["k"]), "flash_k": m6["k"][FLASH],
                    "C_P_6": m6["C_P"], "C_P_5": m5["C_P"], "pi_hat_6": m6["pi_hat"], "pi_hat_5": m5["pi_hat"],
                    "P_6": x6["P"], "P_5": x5["P"], "dP": x5["P"] - x6["P"],
                    "n_mentions_6": x6["n"], "n_mentions_5": x5["n"],
                    "rated_6": int(x6["C"] is not None), "rated_5": int(x5["C"] is not None),
                    "C_star_6": x6["C"], "C_star_5": x5["C"], "dC_star": dC,
                    "rank_P_6": rP6[k], "rank_P_5": rP5[k], "rank_C_6": rC6[k], "rank_C_5": rC5[k],
                    "variant_a_uses": "5-model" if s in ("v0.19", "v0.23") else "6-model",
                    "variant_b_uses": "5-model"})
    if mism:
        sys.exit(f"six-model values do not reproduce the published profiles at {len(mism)} rows: {mism[:5]}")
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print(f"six-model P, C*, rated, n reproduce all {len(rows)} published profile rows; wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
