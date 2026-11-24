#!/usr/bin/env python3
"""A priori power analysis for v0.46 (#76) Stage 1 manuscript r4 (2026-11-24): D7 = cell_d applied. Synthetic only.

No model is called. Runs the r1 power analysis (power_analysis_v0_46_stage1.py) and the r0 precision simulation
(precision_sim_v0_46.py), both imported unchanged, on the unit set of the probe builder's live units, which follow
the logged D7 record (osf/v46/prereg/d7_fisker_v0_46.json): with Fisker in Cell D the cars category has 18 units.
Same seed (46760; precision simulation 76), same simulation and draw counts, same assumptions A1-A7.

Provenance of the unit values (A1): r0's PI table is the t4 recall pi_N3_S0 of v42_brand_table.csv at
v0.42-scoring-locked, rounded to 2 decimals, in that table's (alphabetical) row order, Cell D cars removed. This
script reads the table from git, checks that it reproduces PI exactly for all four categories, and then keeps only
the live units (dropping Fisker, pi 0.00). A6's rated counts (13, 15, 14, 18) are unchanged: Fisker is not a rated
unit at t4 (v1.14 Stage 1, stage1_v1_14.json at commit 3129674), which is checked here too.
Usage: python3 power_analysis_v0_46_stage1_r2.py [n_sims] [n_draws]
Writes osf/v46/prereg/power_analysis_v0_46_stage1_r2.json and .txt.
"""
import csv
import io
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import build_probes_v0_46 as BP               # noqa: E402
import precision_sim_v0_46 as P0              # noqa: E402
import power_analysis_v0_46_stage1 as PA      # noqa: E402

TAG, TABLE = "v0.42-scoring-locked", "osf/v42/v42_brand_table.csv"
STAGE1_REF, STAGE1_JSON = "3129674", "osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json"
SUB = {"skincare": "v0.20", "cosmetics": "v0.21", "cars": "v0.22", "spirits": "v0.23"}


def git_show(ref, path):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{ref}:{path}"], capture_output=True, text=True,
                          check=True).stdout


def unit_names():
    """{category: [brand]} aligned with P0.PI (asserted), from the t4 brand table at the locked tag."""
    rows = list(csv.DictReader(io.StringIO(git_show(TAG, TABLE))))
    names = {}
    for c in P0.CATS:
        rr = [r for r in rows if r["substrate"] == SUB[c] and not (c == "cars" and r["brand"] in BP.CELL_D)]
        pi = list(P0.PI[c])
        # r0's order is the table's, except that two 0.00 cars (Nissan, Polestar) stand at the end of the list.
        # Alignment rule: walk the table in order; a row whose value equals r0's next value takes that place; a
        # 0.00 row that does not is deferred to r0's trailing 0.00 places, in table order. Any other mismatch fails.
        got, deferred = [], []
        for r in rr:
            v = round(float(r["pi_N3_S0"]), 2)
            if len(got) < len(pi) and v == pi[len(got)]:
                got.append(r["brand"])
            elif v == 0.0:
                deferred.append(r["brand"])
            else:
                raise SystemExit(f"[v46] PI provenance FAIL for {c} at {r['brand']} ({v})")
        tail = pi[len(got):]
        if len(tail) != len(deferred) or any(v != 0.0 for v in tail) or len(rr) != len(pi):
            raise SystemExit(f"[v46] PI provenance FAIL for {c}: tail {tail} vs deferred {deferred}")
        names[c] = got + deferred
    return names


def check_rated():
    units = json.loads(git_show(STAGE1_REF, STAGE1_JSON))["units"]
    rated = {c: sum(1 for u in units if u["substrate"] == SUB[c] and u.get("rated_S0")) for c in P0.CATS}
    fisker = [u for u in units if u["substrate"] == "v0.22" and u["brand"] == "Fisker" and u.get("rated_S0")]
    if rated != PA.N_RATED or fisker:
        raise SystemExit(f"[v46] A6 check FAIL: rated {rated} vs {PA.N_RATED}; Fisker rated: {bool(fisker)}")
    return rated


def apply_unit_set(fisker_defunct=None):
    """Restrict P0 / PA unit values to the builder's live units (in place). -> {category: kept brands}."""
    fd = BP.FISKER_DEFUNCT_DEFAULT if fisker_defunct is None else fisker_defunct
    live = BP.live_units(fd)
    names = unit_names()
    kept = {}
    for c in P0.CATS:
        keep = [i for i, b in enumerate(names[c]) if c != "cars" or b in live[c]]   # D7 touches cars only
        if len(keep) != len(live[c]):
            raise SystemExit(f"[v46] unit set FAIL for {c}: {len(keep)} kept != {len(live[c])} live")
        pi = np.asarray(P0.PI[c])[keep]
        P0.PI[c] = list(pi)
        P0.U[c] = (rankdata(pi) - 0.5) / len(pi)
        P0.Z[c] = (pi - np.mean(pi)) / np.std(pi)        # P0's definition; PA.Z is the same dict
        PA.L[c] = len(pi)
        kept[c] = [names[c][i] for i in keep]
    dropped = sorted(b for c in P0.CATS for b in names[c] if b not in kept[c])
    return fd, kept, dropped


def precision_top3(n=200, draws=1000):
    """r0's precision simulation (seed 76, its six scenarios) on the current unit set: top-3 shares (A2)."""
    rng = np.random.default_rng(76)
    out = {}
    for beta, scale, label in P0.SCENARIOS:
        res = [P0.test(P0.simulate(beta, scale, rng), rng, draws) for _ in range(n)]
        out[label] = round(float(np.mean([r[2] for r in res])), 2)
    return out


def main():
    sims = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    draws = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    rated = check_rated()
    fd, kept, dropped = apply_unit_set()
    print(f"[v46] D7 Fisker Cell D = {fd}; units per category {dict(PA.L)}; dropped {dropped}; rated (t4) {rated}",
          flush=True)
    rng = np.random.default_rng(PA.SEED)
    t0 = time.time()
    out = {"seed": PA.SEED, "sims": sims, "permutation_draws": draws, "d7_fisker_defunct": fd,
           "units": dict(PA.L), "units_dropped_vs_r1": dropped,
           "note": "draws reduced from the pre-registered 10,000 (H1-H3, H5) and 2,000 (H4) for simulation",
           "results": {}}
    PA.h1(rng, sims, draws, out["results"])
    PA.h2(rng, sims, draws, out["results"])
    PA.h34(rng, max(100, sims // 4), draws, 200, out["results"])
    PA.h5(rng, max(100, sims // 2), draws, out["results"])
    out["precision_sim_top3_share"] = precision_top3()
    out["seconds"] = round(time.time() - t0, 1)
    path = HERE.parent / "prereg" / "power_analysis_v0_46_stage1_r2.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    path.with_suffix(".txt").write_text("\n".join(f"{k}: {v}" for k, v in out["results"].items()) + "\n"
                                        + f"precision_sim_top3_share: {out['precision_sim_top3_share']}\n")
    print("done", out["seconds"], "s")


if __name__ == "__main__":
    main()
