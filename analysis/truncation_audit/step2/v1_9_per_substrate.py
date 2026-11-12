#!/usr/bin/env python3
"""Step 2 (SENSITIVITY ONLY, not a replacement of any locked result): v1.9 Stage 2 with a
PER-SUBSTRATE keep list, built from score_v1_9's own functions (branch aias-2.0 / v1.9).

stage2_ps() is score_v1_9.stage2() line for line, except that (1) wave metrics come from
score_v41.wave_metrics called once per keep list, each substrate taken from its own list,
and (2) frame_null_cstar is transcribed with the kept models looked up per substrate (with
one list everywhere it consumes the RNG exactly as the original). unit_table, c_star,
presence, retest, constraints, _rho, perm_within and every threshold are score_v1_9's own.

  --mode baseline | a | b   (as in v41_per_substrate.py)
Run with AIAS_ROOT=<aias-2.0 worktree> (score_v1_9 lives there). Writes only into --out.
"""
import os
import sys
from pathlib import Path

_root = Path(os.environ["AIAS_ROOT"])
sys.path.insert(0, str(_root / "osf/methodology/v1_9/scripts"))
sys.path.insert(0, str(_root / "osf/v41/scripts"))
import score_v1_9 as V9  # noqa: E402  (imports score_v41, which re-executes this script under its HOME shim)

import argparse  # noqa: E402
import json  # noqa: E402

import numpy as np  # noqa: E402
import score_v0_31 as S31  # noqa: E402

S = V9.S
PANEL = S31.PANEL
FULL = list(range(S.M))
NOFL = [i for i in FULL if PANEL[i] != "gemini-2.5-flash"]
AFFECTED = ("v0.19", "v0.23")


def keep_lists(mode):
    return {"baseline": {s: FULL for s in S.OMNI},
            "a": {s: (NOFL if s in AFFECTED else FULL) for s in S.OMNI},
            "b": {s: NOFL for s in S.OMNI}}[mode]


def wave_metrics_ps(wave, kb):
    cache, out = {}, {}
    for s in S.OMNI:
        key = tuple(kb[s])
        if key not in cache:
            cache[key] = S.wave_metrics(wave, list(key))
        out[s] = cache[key][s]
    return out


def frame_null_cstar_ps(w2, t3, kb, spec, obs, draws=V9.N_PERM, seed=V9.SEED_FRAME):
    """score_v1_9.frame_null_cstar with the kept models looked up per substrate."""
    rng = np.random.default_rng(seed)
    prep = []
    for s in S.OMNI:
        keep = kb[s]
        kept = [PANEL[i] for i in keep]
        fr = sorted({f for b in t3[s]["frames"].values() for m, fs in b.items() if m in kept for f in fs}, key=str)
        fidx = {f: i for i, f in enumerate(fr)}
        units = []
        for b in t3[s]["counts"]:
            if b not in w2[s]:
                continue
            c2 = V9.c_star(w2[s][b], spec[0], spec[1])
            if c2 is None:
                continue
            hits = [(kept.index(m), fidx[f]) for m, fs in t3[s]["frames"].get(b, {}).items() if m in kept for f in fs]
            rg = t3[s]["recog"].get(b, [0] * S.M)
            units.append((c2, np.array(hits, int).reshape(-1, 2), sum(int(rg[i]) for i in keep)))
        prep.append((s, len(fr), len(kept), units))
    nulls = []
    for _ in range(draws):
        xs, ys, gs = [], [], []
        for s, nf, nk, units in prep:
            perm = np.array([rng.permutation(nk) for _ in range(nf)]).reshape(nf, nk)
            for c2, hits, cp in units:
                k = np.zeros(nk, int)
                if len(hits):
                    np.add.at(k, perm[hits[:, 1], hits[:, 0]], 1)
                phi, pi, _ = S.phi_m(list(k))
                J = None
                if spec[0] == "C_phiJ":
                    sets = {}
                    for mi, fi in hits:
                        sets.setdefault(int(perm[fi, mi]), set()).add(int(fi))
                    J, _ = S.jaccard_of(sets)
                m = {"k": list(k), "pi_hat": pi, "phi": phi, "J": J, "C_P": cp}
                c3 = V9.c_star(m, spec[0], spec[1])
                if c3 is not None:
                    xs.append(c2); ys.append(c3); gs.append(s)
        nulls.append(S.pooled_within_rho(xs, ys, gs))
    nulls = np.array([x for x in nulls if np.isfinite(x)])
    p = (np.sum(nulls >= obs - 1e-12) + 1) / (len(nulls) + 1)
    return {"p_frame": float(p), "null_mean": float(nulls.mean()), "null_p95": float(np.percentile(nulls, 95)),
            "draws": int(len(nulls)), "seed": seed}


def stage2_ps(lay3, kb):
    """score_v1_9.stage2 with a per-substrate keep list (same tests, thresholds, seeds)."""
    spec = V9.SELECTED_SPEC
    gates, t1, t2 = S.run_gates()
    t3 = S.load_wave(lay3)
    w2, w3 = wave_metrics_ps(t2, kb), wave_metrics_ps(t3, kb)
    r2, r3 = V9.unit_table(w2, spec), V9.unit_table(w3, spec)

    k3 = {(x["s"], x["b"]): x for x in r3}
    pairs = [(x, k3[(x["s"], x["b"])]) for x in r2 if (x["s"], x["b"]) in k3]
    p2 = np.array([a["P"] for a, _ in pairs]); p3 = np.array([b["P"] for _, b in pairs])
    g = np.array([a["s"] for a, _ in pairs])
    rp2, rp3 = S.within_ranks(p2, g), S.within_ranks(p3, g)
    rhoP = S._pearson(rp2, rp3)
    pP = V9.perm_within(rp2, rp3, g, rhoP, V9.SEED_REL) if np.isfinite(rhoP) else float("nan")
    if not np.isfinite(rhoP):
        vP = "UNDETERMINED"
    elif rhoP >= V9.REL_CONF and pP < .05:
        vP = "CONFIRMED"
    elif rhoP < V9.REL_FALS or pP >= .05:
        vP = "FALSIFIED"
    else:
        vP = "MARGINAL"
    nocomp, nn = V9._rho(r3, "A", "P")
    d, nd = V9._rho(r3, "C", "P")
    vD = "CONFIRMED" if abs(d) <= V9.DIS_CONF else "FALSIFIED" if abs(d) >= V9.DIS_FALS else "MARGINAL"
    rhoC, nC = V9.retest(r2, r3, "C")
    fn = frame_null_cstar_ps(w2, t3, kb, spec, rhoC)
    if rhoC >= V9.CR_CONF and fn["p_frame"] < .05:
        vC = "CONFIRMED"
    elif rhoC < V9.CR_FALS or fn["p_frame"] >= .05:
        vC = "FALSIFIED"
    else:
        vC = "MARGINAL"
    c3 = V9.constraints(r3)
    out = {"SENSITIVITY_ONLY": "not a replacement of osf/methodology/v1_9/v1_9_verdicts.json",
           "keep_by_substrate": {s: [PANEL[i] for i in kb[s]] for s in S.OMNI},
           "parity_gates_all_passed": gates["all_passed"],
           "verdicts": {
               "H_Presence_Score_Reliability": {"tier": "PRIMARY", "verdict": vP, "rho": rhoP,
                                                "p_perm": pP, "n": len(pairs)},
               "H_Dissociation_t3": {"tier": "PRIMARY", "verdict": vD, "rho": d, "n": nd},
               "H_Consistency_Reliability": {"tier": "PRIMARY", "verdict": vC, "rho": rhoC, "n": nC,
                                             "frame_structure_null": fn},
               "H_NoComposite_t3": {"tier": "SECONDARY (descriptive)", "verdict": "DESCRIPTIVE",
                                    "rho_A_P": nocomp, "n": nn, "k2_line": V9.K2_MAX}},
           "constraints_t3": c3}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["baseline", "a", "b"])
    ap.add_argument("--t3", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    base = Path(a.t3).resolve()
    out = stage2_ps(S._layout(base, base / "v23"), keep_lists(a.mode))
    out["mode"] = a.mode
    d = Path(a.out)
    d.mkdir(parents=True, exist_ok=True)
    json.dump(S._clean(out), open(d / "v1_9_verdicts.json", "w"), indent=2, allow_nan=False)
    print(f"wrote {d}")
    for k, v in out["verdicts"].items():
        print(f"  {k}: {v['verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
