#!/usr/bin/env python3
"""Step 2 (SENSITIVITY ONLY, not a replacement of any locked result): v0.41 hypotheses with a
PER-SUBSTRATE keep list, built from score_v41's own functions.

score_v41.wave_metrics(wave, keep) takes one keep list for all substrates, and the stock path
halts when a model is missing in only some substrates. This wrapper calls wave_metrics once per
keep list and takes, for each substrate, the block computed with that substrate's list; the
frame-structure null (score_v41.frame_shuffle_null) is transcribed with only one change: the
kept models are looked up per substrate (with one list everywhere it consumes the RNG exactly
as the original). h_phi_long, h_presence_long, h_horizon_decay, h_drift, h_phantom, phi_m,
load_wave and run_gates are score_v41's own, called unchanged.

  --mode baseline  all six models in every substrate (must reproduce osf/v41/v41_verdicts.json)
  --mode a         Gemini 2.5 Flash dropped in v0.19 and v0.23 only (t1, t2, t3)
  --mode b         Gemini 2.5 Flash dropped everywhere (cross-check of the stock --synthetic run)

Usage (worktree root): AIAS_ROOT=$PWD PYTHONDONTWRITEBYTECODE=1 python3 \
   analysis/truncation_audit/step2/v41_per_substrate.py --mode a --t3 DIR --out DIR
Writes only into --out (v41_verdicts.json, v41_three_wave_table.csv).
"""
import os
import sys
from pathlib import Path

WT = Path(__file__).resolve().parents[3]
os.environ.setdefault("AIAS_ROOT", str(WT))
sys.path.insert(0, str(WT / "osf/v41/scripts"))
import score_v41 as V  # noqa: E402  (re-executes this script under score_v41's HOME shim)

import argparse  # noqa: E402
import json  # noqa: E402

import numpy as np  # noqa: E402
import score_v0_31 as S31  # noqa: E402  (on sys.path via score_v41: ROOT/scripts)

PANEL = S31.PANEL
FULL = list(range(V.M))
FLASH = PANEL.index("gemini-2.5-flash")
NOFL = [i for i in FULL if i != FLASH]
AFFECTED = ("v0.19", "v0.23")


def keep_lists(mode):
    if mode == "baseline":
        return {s: FULL for s in V.OMNI}
    if mode == "a":
        return {s: (NOFL if s in AFFECTED else FULL) for s in V.OMNI}
    if mode == "b":
        return {s: NOFL for s in V.OMNI}
    raise SystemExit(f"unknown mode {mode}")


def wave_metrics_ps(wave, keep_by_sub):
    """score_v41.wave_metrics, substrate s taken from the call with keep_by_sub[s]."""
    cache, out = {}, {}
    for s in V.OMNI:
        key = tuple(keep_by_sub[s])
        if key not in cache:
            cache[key] = V.wave_metrics(wave, list(key))
        out[s] = cache[key][s]
    return out


def frame_shuffle_null_ps(w2, t3, keep_by_sub, obs, seed=V.SEED_FRAME, draws=None):
    """score_v41.frame_shuffle_null (SCORER_NOTES S2) with the kept models looked up per
    substrate. Identical code otherwise; with one keep list everywhere it is the original."""
    draws = draws or V.N_FRAME
    rng = np.random.default_rng(seed)
    prep = []
    for s in V.OMNI:
        kept = [PANEL[i] for i in keep_by_sub[s]]
        fr = sorted({f for b in t3[s]["frames"].values() for m, fs in b.items() if m in kept for f in fs}, key=str)
        fidx = {f: i for i, f in enumerate(fr)}
        brands = []
        for b in t3[s]["counts"]:
            if b in w2[s] and w2[s][b]["phi"] is not None:
                hits = [(kept.index(m), fidx[f]) for m, fs in t3[s]["frames"].get(b, {}).items()
                        if m in kept for f in fs]
                brands.append((w2[s][b]["phi"], np.array(hits, int).reshape(-1, 2)))
        prep.append((len(fr), len(kept), brands))
    nulls = np.empty(draws)
    for d in range(draws):
        xs, ys = [], []
        for nf, nk, brands in prep:
            perm = np.array([rng.permutation(nk) for _ in range(nf)]).reshape(nf, nk)
            for phi2, hits in brands:
                k = np.zeros(nk, int)
                if len(hits):
                    np.add.at(k, perm[hits[:, 1], hits[:, 0]], 1)
                p3 = V.phi_m(list(k))[0]
                if p3 is not None:
                    xs.append(phi2); ys.append(p3)
        nulls[d] = V.spearman(xs, ys)
    nulls = nulls[np.isfinite(nulls)]
    p = (np.sum(nulls >= obs - 1e-12) + 1) / (len(nulls) + 1)
    return {"p_frame": float(p), "null_mean": float(nulls.mean()), "null_p95": float(np.percentile(nulls, 95)),
            "null_max": float(nulls.max()), "draws": int(len(nulls)), "seed": seed}


def score_all_ps(t1, t2, t3, keep_by_sub):
    """score_v41.score_all with a per-substrate keep list (same hypothesis functions)."""
    w1, w2, w3 = (wave_metrics_ps(w, keep_by_sub) for w in (t1, t2, t3))
    hyps = {
        "H_Phi_LongHorizon": {"tier": "PRIMARY", **V.h_phi_long(
            w2, w3, frame_null=lambda obs: frame_shuffle_null_ps(w2, t3, keep_by_sub, obs))},
        "H_Presence_LongHorizon": {"tier": "PRIMARY", **V.h_presence_long(w2, w3)},
        "H_Horizon_Decay": {"tier": "SECONDARY", **V.h_horizon_decay(w1, w2, w3)},
        "H_Drift_Dissociation": {"tier": "SECONDARY", **V.h_drift(w2, w3)},
        "H_Phantom_LongPersistence": {"tier": "TERTIARY (descriptive)", **V.h_phantom(w2, w3)},
    }
    return hyps, (w1, w2, w3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["baseline", "a", "b"])
    ap.add_argument("--t3", required=True, help="t3 folder (same layout as osf/v41/data)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    kb = keep_lists(a.mode)
    gates, t1, t2 = V.run_gates()                      # full-panel parity gates P1-P4 (read-only)
    base = Path(a.t3).resolve()
    t3 = V.load_wave(V._layout(base, base / "v23"))
    hyps, waves = score_all_ps(t1, t2, t3, kb)
    out = {"SENSITIVITY_ONLY": "not a replacement of osf/v41/v41_verdicts.json",
           "mode": a.mode, "t3_dir": str(base),
           "keep_by_substrate": {s: [PANEL[i] for i in kb[s]] for s in V.OMNI},
           "parity_gates_all_passed": gates["all_passed"], "verdicts": hyps}
    d = Path(a.out)
    d.mkdir(parents=True, exist_ok=True)
    json.dump(V._clean(out), open(d / "v41_verdicts.json", "w"), indent=2, allow_nan=False)
    rows = V.three_wave_rows(waves)
    import csv
    with open(d / "v41_three_wave_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print(f"wrote {d}")
    for k, v in hyps.items():
        if k == "H_Horizon_Decay":
            print(f"  {k}: phi {v['phi']['verdict']} / pi_hat {v['pi_hat']['verdict']}")
        else:
            print(f"  {k}: {v['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
