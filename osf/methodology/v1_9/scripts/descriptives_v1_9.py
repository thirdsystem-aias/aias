#!/usr/bin/env python3
"""
descriptives_v1_9.py — per-brand Presence P and Consistency C* (C_phi+FLOOR), t1/t2/t3.

DESCRIPTIVE ONLY (report figures, deposit). Uses score_v1_9's locked functions
(presence, c_star, unit_table) and score_v41's loaders unchanged; no statistic here is
verdict-bearing. Writes osf/methodology/v1_9/v1_9_unit_table.csv.

  AIAS_ROOT=<v1.9 tree> python3 descriptives_v1_9.py --t3 <v0.41 tree>/osf/v41/data
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_9 as V   # noqa: E402
S = V.S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t3", required=True)
    a = ap.parse_args()
    gates, t1, t2 = S.run_gates()
    d3 = Path(a.t3).resolve()
    t3 = S.load_wave(S._layout(d3, d3 / "v23"))
    full = list(range(S.M))
    out = V.OUT / "v1_9_unit_table.csv"
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wave", "substrate", "brand", "mentions", "P", "C_star", "A_add_descriptive"])
        for name, wave in (("t1", t1), ("t2", t2), ("t3", t3)):
            for r in V.unit_table(S.wave_metrics(wave, full), V.SELECTED_SPEC):
                w.writerow([name, r["s"], r["b"], r["n"], f"{r['P']:.4f}",
                            "" if r["C"] is None else f"{r['C']:.4f}", f"{r['A']:.4f}"])
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
