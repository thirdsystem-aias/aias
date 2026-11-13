#!/usr/bin/env python3
"""
score_v1_9.py — AIAS(TM) v1.9 two-component composite calibration (Presence x Consistency).

Transcribes osf/methodology/v1_9/prereg/v1_9_two_component_composite_content.py. The
pre-registration prose is authoritative; constants cite the section they transcribe.

  --stage1   CALIBRATION on the frozen t1/t2 waves (declared calibration, run before the
             lock): all 8 candidates, constraints K1-K3 at t1 and t2, test-retest, the
             selection rule. Writes osf/methodology/v1_9/v1_9_calibration.json.
  --stage2   CONFIRMATION on t2 -> t3 (v0.41 data) under the locked SELECTED
             specification. Refuses unless tag v1.9-prereg-r1 exists.
             Writes osf/methodology/v1_9/v1_9_verdicts.json.
  --stage2-synthetic DIR   Stage 2 on a synthetic t3 folder (tests only).

Extraction, kernel and parity gates come from osf/v41/scripts/score_v41.py (v0.41 P1-P4
run first; any failure halts).
"""
import os
import sys
from pathlib import Path

_root = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
sys.path.insert(0, str(_root / "osf/v41/scripts"))
import score_v41 as S   # noqa: E402  (re-executes with the ~/aias shim if needed)

import argparse         # noqa: E402
import json             # noqa: E402
import subprocess       # noqa: E402

import numpy as np      # noqa: E402

ROOT = S.ROOT
OUT = ROOT / "osf/methodology/v1_9"
PREREG_TAG = "v1.9-prereg-r1"                       # PREREG_TAG

KAPPA = 6            # CANDIDATES.low_count_rule.SHRINK: kappa = 6
C0 = 50.0            # CANDIDATES.low_count_rule.SHRINK: C_0 = 50
N_FLOOR = 6          # CANDIDATES.low_count_rule.FLOOR: n >= 6
K1_MAX = 0.50        # CONSTRAINTS K1
K2_MAX = 0.95        # CONSTRAINTS K2
K3_SLACK = 5.0       # CONSTRAINTS K3
TIE = 0.01           # SELECTION_RULE
# Stage 2 (HYPOTHESES)
SEED_REL, SEED_FRAME = 190019, 190020
N_PERM = 10_000
REL_CONF, REL_FALS, REL_MARGIN = 0.80, 0.60, 0.05
DIS_CONF, DIS_FALS = 0.30, 0.50
CR_CONF, CR_FALS = 0.50, 0.30

SELECTED_SPEC = ("C_phi", "FLOOR", "ADD")      # STAGE1_RESULT / SELECTED_CONSISTENCY
CANDIDATE_ORDER = [(c, l, f) for c in ("C_phi", "C_phiJ") for l in ("FLOOR", "SHRINK") for f in ("ADD", "MOD")]
SIMPLICITY = {"C_phi": 0, "C_phiJ": 1, "FLOOR": 0, "SHRINK": 1, "ADD": 0, "MOD": 1}


# ===========================================================================
# components
# ===========================================================================
def presence(m):
    """PRESENCE: P = 100 * (C_P/6 + 2*pi_hat) / 3 (v0.25 composite, channel-agnostic form)."""
    return 100.0 * (m["C_P"] / len(m["k"]) + 2.0 * m["pi_hat"]) / 3.0


def c_phi(m):
    """CONSISTENCY.scale: 100 * (1 - phi/phi_max), phi_max = F*M/(M-1); pi_hat=1 -> 100; pi_hat=0 -> None."""
    M = len(m["k"])
    if m["pi_hat"] >= 1.0:
        return 100.0
    if m["phi"] is None:
        return None
    return 100.0 * (1.0 - m["phi"] / (S.F * M / (M - 1)))


def c_phij(m):
    """CONSISTENCY.J_option: (C_phi + 100*J)/2 where J defined; C_phi otherwise."""
    c = c_phi(m)
    if c is None:
        return None
    if m["pi_hat"] >= 1.0:
        return 100.0
    return (c + 100.0 * m["J"]) / 2.0 if m["J"] is not None else c


def c_star(m, cons, low):
    c = c_phi(m) if cons == "C_phi" else c_phij(m)
    if c is None:
        return None
    n = sum(m["k"])
    if low == "FLOOR":
        return c if n >= N_FLOOR else None
    w = n / (n + KAPPA)
    return w * c + (1.0 - w) * C0


def composite(P, C, form):
    if form == "ADD":
        return P if C is None else (P + C) / 2.0
    return 0.5 * P if C is None else P * (0.5 + 0.5 * C / 100.0)


def unit_table(w, spec):
    cons, low, form = spec
    rows = []
    for s in S.OMNI:
        for b, m in w[s].items():
            P = presence(m)
            C = c_star(m, cons, low)
            rows.append({"s": s, "b": b, "P": P, "C": C, "A": composite(P, C, form), "n": sum(m["k"])})
    return rows


def _rho(rows, a, b):
    r = [x for x in rows if x[a] is not None and x[b] is not None]
    return S.pooled_within_rho([x[a] for x in r], [x[b] for x in r], [x["s"] for x in r]), len(r)


def constraints(rows):
    k1, n1 = _rho(rows, "C", "P")
    k2, n2 = _rho(rows, "A", "P")
    low = [x for x in rows if 1 <= x["n"] <= 2]
    zero = [x for x in rows if x["n"] == 0]
    if low and zero:
        dA = np.mean([x["A"] for x in low]) - np.mean([x["A"] for x in zero])
        dP = np.mean([x["P"] for x in low]) - np.mean([x["P"] for x in zero])
        k3 = {"dA": float(dA), "dP": float(dP), "pass": bool(dA <= dP + K3_SLACK),
              "n_low": len(low), "n_zero": len(zero)}
    else:
        k3 = {"pass": True, "note": "no units at 1-2 or 0 mentions", "n_low": len(low), "n_zero": len(zero)}
    return {"K1": {"rho": k1, "n": n1, "pass": bool(np.isfinite(k1) and abs(k1) <= K1_MAX)},
            "K2": {"rho": k2, "n": n2, "pass": bool(np.isfinite(k2) and abs(k2) <= K2_MAX)},
            "K3": k3,
            "share_C_not_rated": sum(1 for x in rows if x["C"] is None) / len(rows)}


def retest(ra, rb, field):
    kb = {(x["s"], x["b"]): x for x in rb}
    pairs = [(x, kb[(x["s"], x["b"])]) for x in ra if (x["s"], x["b"]) in kb
             and x[field] is not None and kb[(x["s"], x["b"])][field] is not None]
    rho = S.pooled_within_rho([a[field] for a, _ in pairs], [b[field] for _, b in pairs], [a["s"] for a, _ in pairs])
    return rho, len(pairs)


# ===========================================================================
# Stage 1
# ===========================================================================
def stage1():
    gates, t1, t2 = S.run_gates()                       # v0.41 P1-P4 (halts on failure)
    full = list(range(S.M))
    w1, w2 = S.wave_metrics(t1, full), S.wave_metrics(t2, full)
    table = []
    for spec in CANDIDATE_ORDER:
        r1, r2 = unit_table(w1, spec), unit_table(w2, spec)
        c1, c2 = constraints(r1), constraints(r2)
        relA, nA = retest(r1, r2, "A")
        relC, nC = retest(r1, r2, "C")
        ok = all(c[k]["pass"] for c in (c1, c2) for k in ("K1", "K2", "K3"))
        table.append({"spec": "+".join(spec), "consistency": spec[0], "low_count": spec[1], "form": spec[2],
                      "t1": c1, "t2": c2, "retest_A": relA, "retest_A_n": nA,
                      "retest_C": relC, "retest_C_n": nC, "passes_all": ok})
    relP, nP = retest(unit_table(w1, CANDIDATE_ORDER[0]), unit_table(w2, CANDIDATE_ORDER[0]), "P")
    passing = [r for r in table if r["passes_all"]]
    if not passing:
        selected, note = None, "no candidate passes K1-K3 at both waves: v1.9 locks 'no composite'"
    else:
        best = max(r["retest_A"] for r in passing)
        tied = [r for r in passing if r["retest_A"] >= best - TIE]
        tied.sort(key=lambda r: (SIMPLICITY[r["consistency"]], SIMPLICITY[r["low_count"]], SIMPLICITY[r["form"]]))
        selected = tied[0]["spec"]
        note = (f"best retest {best:.3f}; {len(tied)} within {TIE}; simplest of those selected"
                if len(tied) > 1 else f"best retest {best:.3f}")
    out = {"phase": "v1.9", "stage": "1 (calibration on frozen t1/t2; declared, not a test)",
           "parity_gates_v0_41": {g: gates[g]["passed"] for g in ("P1", "P2", "P3", "P4")},
           "presence_retest_t1_t2": relP, "presence_retest_n": nP,
           "constants": {"kappa": KAPPA, "C0": C0, "floor_n": N_FLOOR, "K1": K1_MAX, "K2": K2_MAX,
                         "K3_slack": K3_SLACK, "tie": TIE},
           "candidates": table, "selected": selected, "selection_note": note}
    (OUT / "prereg").mkdir(parents=True, exist_ok=True)
    json.dump(S._clean(out), open(OUT / "prereg" / "v1_9_calibration.json", "w"), indent=2, allow_nan=False)
    return out


# ===========================================================================
# Stage 2
# ===========================================================================
def stage2(lay3, outdir):
    # Locked outcome (STAGE1_RESULT): no single composite; C* = C_phi+FLOOR.
    # ADD is used only for the descriptive H_NoComposite_t3 check.
    spec = SELECTED_SPEC
    gates, t1, t2 = S.run_gates()
    import score_v0_31 as S31
    comp = S.mc_completeness(lay3["base"], lay3["v23"])
    if comp["partially_failed_models"]:
        raise S.Halt("v0.41 t3 has residual failures; resolve before Stage 2")
    keep = [i for i, m in enumerate(S31.PANEL) if m not in comp["unavailable_models"]]
    t3 = S.load_wave(lay3)
    w2, w3 = S.wave_metrics(t2, keep), S.wave_metrics(t3, keep)
    r2, r3 = unit_table(w2, spec), unit_table(w3, spec)

    # H_Presence_Score_Reliability
    k3 = {(x["s"], x["b"]): x for x in r3}
    pairs = [(x, k3[(x["s"], x["b"])]) for x in r2 if (x["s"], x["b"]) in k3]
    p2 = np.array([a["P"] for a, _ in pairs]); p3 = np.array([b["P"] for _, b in pairs])
    g = np.array([a["s"] for a, _ in pairs])
    rp2, rp3 = S.within_ranks(p2, g), S.within_ranks(p3, g)
    rhoP = S._pearson(rp2, rp3)
    pP = perm_within(rp2, rp3, g, rhoP, SEED_REL) if np.isfinite(rhoP) else float("nan")
    if not np.isfinite(rhoP):
        vP = "UNDETERMINED"
    elif rhoP >= REL_CONF and pP < .05:
        vP = "CONFIRMED"
    elif rhoP < REL_FALS or pP >= .05:
        vP = "FALSIFIED"
    else:
        vP = "MARGINAL"
    nocomp, nn = _rho(r3, "A", "P")

    # H_Dissociation_t3
    d, nd = _rho(r3, "C", "P")
    vD = "CONFIRMED" if abs(d) <= DIS_CONF else "FALSIFIED" if abs(d) >= DIS_FALS else "MARGINAL"

    # H_Consistency_Reliability with the v0.41 frame-structure null applied to C*
    rhoC, nC = retest(r2, r3, "C")
    fn = frame_null_cstar(w2, t3, keep, spec, rhoC)
    if rhoC >= CR_CONF and fn["p_frame"] < .05:
        vC = "CONFIRMED"
    elif rhoC < CR_FALS or fn["p_frame"] >= .05:
        vC = "FALSIFIED"
    else:
        vC = "MARGINAL"

    c3 = constraints(r3)
    out = {"phase": "v1.9", "stage": "2 (confirmation, t2 -> t3)", "prereg_tag": PREREG_TAG,
           "locked_outcome": "no single composite; C* = C_phi+FLOOR",
           "panel_used": [S31.PANEL[i] for i in keep],
           "verdicts": {
               "H_Presence_Score_Reliability": {"tier": "PRIMARY", "verdict": vP, "rho": rhoP,
                                                "p_perm": pP, "n": len(pairs)},
               "H_Dissociation_t3": {"tier": "PRIMARY", "verdict": vD, "rho": d, "n": nd},
               "H_Consistency_Reliability": {"tier": "PRIMARY", "verdict": vC, "rho": rhoC, "n": nC,
                                             "frame_structure_null": fn},
               "H_NoComposite_t3": {"tier": "SECONDARY (descriptive)", "verdict": "DESCRIPTIVE",
                                    "rho_A_P": nocomp, "n": nn, "k2_line": K2_MAX}},
           "constraints_t3": c3}
    outdir.mkdir(parents=True, exist_ok=True)
    json.dump(S._clean(out), open(outdir / "v1_9_verdicts.json", "w"), indent=2, allow_nan=False)
    return out


def perm_within(r2, r3, g, obs, seed, draws=N_PERM):
    """One-sided stratified permutation for the within-substrate-rank statistic: t3 ranks
    permuted within substrate; statistic = Pearson on within-substrate ranks."""
    rng = np.random.default_rng(seed)
    gidx = S._group_index(g)
    idx = np.arange(len(r3))
    hits = 0
    for _ in range(draws):
        for gi in gidx:
            idx[gi] = rng.permutation(gi)
        hits += S._pearson(r2, r3[idx]) >= obs - 1e-12
    return (hits + 1) / (draws + 1)


def frame_null_cstar(w2, t3, keep, spec, obs, draws=N_PERM, seed=SEED_FRAME):
    """v0.41 within-frame model-shuffle null, applied to the calibrated C* (rated in both)."""
    import score_v0_31 as S31
    kept = [S31.PANEL[i] for i in keep]
    rng = np.random.default_rng(seed)
    prep = []
    for s in S.OMNI:
        fr = sorted({f for b in t3[s]["frames"].values() for m, fs in b.items() if m in kept for f in fs}, key=str)
        fidx = {f: i for i, f in enumerate(fr)}
        units = []
        for b in t3[s]["counts"]:
            if b not in w2[s]:
                continue
            c2 = c_star(w2[s][b], spec[0], spec[1])
            if c2 is None:
                continue
            hits = [(kept.index(m), fidx[f]) for m, fs in t3[s]["frames"].get(b, {}).items() if m in kept for f in fs]
            rg = t3[s]["recog"].get(b, [0] * S.M)
            units.append((c2, np.array(hits, int).reshape(-1, 2), sum(int(rg[i]) for i in keep)))
        prep.append((s, len(fr), units))
    nulls = []
    for _ in range(draws):
        xs, ys, gs = [], [], []
        for s, nf, units in prep:
            perm = np.array([rng.permutation(len(kept)) for _ in range(nf)]).reshape(nf, len(kept))
            for c2, hits, cp in units:
                k = np.zeros(len(kept), int)
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
                c3 = c_star(m, spec[0], spec[1])
                if c3 is not None:
                    xs.append(c2); ys.append(c3); gs.append(s)
        nulls.append(S.pooled_within_rho(xs, ys, gs))
    nulls = np.array([x for x in nulls if np.isfinite(x)])
    p = (np.sum(nulls >= obs - 1e-12) + 1) / (len(nulls) + 1)
    return {"p_frame": float(p), "null_mean": float(nulls.mean()), "null_p95": float(np.percentile(nulls, 95)),
            "draws": int(len(nulls)), "seed": seed}


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--stage1", action="store_true")
    g.add_argument("--stage2", action="store_true")
    g.add_argument("--stage2-synthetic", metavar="DIR")
    ap.add_argument("--t3", metavar="DIR", help="v0.41 t3 data folder (default osf/v41/data in this tree)")
    a = ap.parse_args()
    try:
        if a.stage1:
            out = stage1()
            print(f"selected: {out['selected']}  ({out['selection_note']})")
            for r in out["candidates"]:
                print(f"  {r['spec']:<22} pass={r['passes_all']!s:<5} retest_A={r['retest_A']:.3f} "
                      f"retest_C={r['retest_C']:.3f}  K1 t1/t2={r['t1']['K1']['rho']:+.3f}/{r['t2']['K1']['rho']:+.3f}  "
                      f"K2={r['t1']['K2']['rho']:.3f}/{r['t2']['K2']['rho']:.3f}  "
                      f"K3 dA={r['t1']['K3'].get('dA', float('nan')):.1f} vs dP+5={r['t1']['K3'].get('dP', float('nan')) + 5:.1f}")
            print(f"  presence retest t1->t2: {out['presence_retest_t1_t2']:.3f}")
            return 0
        if a.stage2_synthetic:
            base = Path(a.stage2_synthetic).resolve()
            out = stage2(S._layout(base, base / "v23"), base / "_score_v1_9")
        else:
            r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", f"refs/tags/{PREREG_TAG}"],
                               capture_output=True)
            if r.returncode != 0:
                print(f"refusing --stage2: tag {PREREG_TAG} does not exist", file=sys.stderr)
                return 3
            d3 = Path(a.t3).resolve() if a.t3 else S.DATA3
            out = stage2(S._layout(d3, d3 / "v23"), OUT)
        for k, v in out["verdicts"].items():
            print(f"  {k}: {v['verdict']}")
        return 0
    except S.GateFailure as e:
        print("[v1.9] PARITY GATE FAILURE\n" + str(e), file=sys.stderr)
        return 2
    except S.Halt as e:
        print(f"[v1.9] HALT: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
