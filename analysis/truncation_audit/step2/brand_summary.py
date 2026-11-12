#!/usr/bin/env python3
"""Step 2: headphones (v0.19) and premium spirits (v0.23) movers, from results/brand_profiles_6_vs_5.csv.
A brand is listed when it is Sennheiser, or its C* moves by >= 10 points on the 0-100 scale
(= 0.10 on a 0-1 scale) or by >= 0.10 points (both flags reported), or its rank by P or by C*
within the category changes, or its rated status changes. Writes results/brand_movers.csv."""
import csv
from pathlib import Path

R = Path(__file__).resolve().parent / "results"


def f(x):
    return None if x in ("", None) else float(x)


def main():
    rows = [r for r in csv.DictReader(open(R / "brand_profiles_6_vs_5.csv", newline=""))
            if r["substrate"] in ("v0.19", "v0.23")]
    out = []
    for r in rows:
        dC = f(r["dC_star"])
        why = []
        if r["brand_name"] == "Sennheiser":
            why.append("Sennheiser")
        if dC is not None and abs(dC) >= 10:
            why.append("|dC*|>=10 pts (0.10 on 0-1)")
        if r["rank_P_6"] != r["rank_P_5"]:
            why.append("P rank")
        if r["rank_C_6"] != r["rank_C_5"]:
            why.append("C* rank")
        if r["rated_6"] != r["rated_5"]:
            why.append("rated status")
        if why:
            out.append({"category": r["category"], "wave": r["wave"], "brand": r["brand_name"],
                        "flash_k": r["flash_k"], "P_6": r["P_6"], "P_5": r["P_5"], "dP": r["dP"],
                        "C_star_6": r["C_star_6"], "C_star_5": r["C_star_5"], "dC_star": r["dC_star"],
                        "rank_P_6": r["rank_P_6"], "rank_P_5": r["rank_P_5"],
                        "rank_C_6": r["rank_C_6"], "rank_C_5": r["rank_C_5"],
                        "rated_6": r["rated_6"], "rated_5": r["rated_5"],
                        "n_mentions_6": r["n_mentions_6"], "n_mentions_5": r["n_mentions_5"],
                        "dC_ge_0.10_points": int(dC is not None and abs(dC) >= 0.10), "why": "; ".join(why)})
    with open(R / "brand_movers.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for cat in ("headphones", "premium spirits"):
        for wave in ("t1", "t2", "t3"):
            sel = [r for r in rows if r["category"] == cat and r["wave"] == wave]
            rated = [r for r in sel if r["rated_6"] == "1" and r["rated_5"] == "1"]
            ds = [float(r["dC_star"]) for r in rated]
            big = [r["brand_name"] for r in rated if abs(float(r["dC_star"])) >= 10]
            print(f"{cat:15} {wave}: rated both {len(rated)}; dC* min {min(ds):+.1f} max {max(ds):+.1f}; "
                  f">=10 pts: {len(big)} {big}; P rank changes "
                  f"{sum(r['rank_P_6'] != r['rank_P_5'] for r in sel)}; C* rank changes "
                  f"{sum(r['rank_C_6'] != r['rank_C_5'] for r in sel)}; rated status changes "
                  f"{sum(r['rated_6'] != r['rated_5'] for r in sel)}")
    for r in rows:
        if r["brand_name"] == "Sennheiser":
            print(f"Sennheiser {r['wave']}: P {float(r['P_6']):.4f} -> {float(r['P_5']):.4f}; "
                  f"C* {float(r['C_star_6']):.4f} -> {float(r['C_star_5']):.4f}; C* rank {r['rank_C_6']} -> "
                  f"{r['rank_C_5']}; P rank {r['rank_P_6']} -> {r['rank_P_5']}; k {r['k_per_model_6']}")
    print(f"wrote {R / 'brand_movers.csv'} ({len(out)} rows)")


if __name__ == "__main__":
    main()
