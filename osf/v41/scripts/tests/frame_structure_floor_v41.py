#!/usr/bin/env python3
"""
frame_structure_floor_v41.py — pre-lock calibration for H_Phi_LongHorizon (no API calls).

Question: how much of phi's brand rank order survives when model identity is scrambled
but each frame keeps which brands it elicits? For each draw, the six models' answers
are permuted WITHIN every (substrate, frame) — one permutation per frame, applied to
all brands, since a model's answer covers every brand — on the frozen t2 wave; phi is
recomputed and rho(phi_t2, phi_shuffled) taken exactly as the H_Phi statistic
(pooled Spearman over brands phi-defined in both). pi_hat is preserved exactly.

Also on t1 -> shuffled t1 for comparison, and for the program's observed
t1 -> t2 rho = 0.6454 (v1.8).

Usage: AIAS_ROOT=<tree> python3 osf/v41/scripts/tests/frame_structure_floor_v41.py [--draws 1000] [--out FILE]
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import score_v41 as S   # noqa: E402  (score_v41 re-executes with the ~/aias shim if needed)

import argparse         # noqa: E402
import json             # noqa: E402
import numpy as np      # noqa: E402

SEED = 410099


def shuffled_counts(wave, rng, panel):
    out = {}
    for s in S.OMNI:
        frames = sorted({f for b in wave[s]["frames"].values() for fs in b.values() for f in fs}, key=str)
        perm = {f: dict(zip(panel, rng.permutation(panel))) for f in frames}
        out[s] = {}
        for b in wave[s]["counts"]:
            k = {m: 0 for m in panel}
            for m, fs in wave[s]["frames"].get(b, {}).items():
                for f in fs:
                    k[perm[f][m]] += 1
            out[s][b] = [k[m] for m in panel]
    return out


def rho_vs(wave, counts):
    xs, ys = [], []
    for s in S.OMNI:
        for b, vec in wave[s]["counts"].items():
            p1 = S.phi_of(vec)[0]
            p2 = S.phi_of(counts[s][b])[0]
            if p1 is not None and p2 is not None:
                xs.append(p1); ys.append(p2)
    return S.spearman(xs, ys), len(xs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    import score_v0_31 as S31
    panel = list(S31.PANEL)
    rng = np.random.default_rng(SEED)
    res = {}
    for name in ("t2", "t1"):
        wave = S.load_wave(S.LAYOUT[name])
        rhos = np.array([rho_vs(wave, shuffled_counts(wave, rng, panel))[0] for _ in range(a.draws)])
        res[name] = {"draws": a.draws, "mean": float(rhos.mean()), "sd": float(rhos.std(ddof=1)),
                     "p05": float(np.percentile(rhos, 5)), "median": float(np.median(rhos)),
                     "p95": float(np.percentile(rhos, 95)), "max": float(rhos.max()),
                     "share_ge_0_50": float(np.mean(rhos >= 0.50)),
                     "share_ge_0_30": float(np.mean(rhos >= 0.30))}
        print(name, json.dumps(res[name]))
    res["observed_t1_t2_rho_v1_8"] = 0.6454
    res["seed"] = SEED
    if a.out:
        json.dump(res, open(a.out, "w"), indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
