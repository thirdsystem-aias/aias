#!/usr/bin/env python3
"""
score_v34.py — v0.34 CPC Longitudinal t1->t2 Stability scorer.

Computes per-brand CV-CPC and C_P for BOTH waves via the identical locked extraction
(score_v0_31 extractors + score_v33 recognition fns; v1.4 matcher for raw-text
substrates), then the pre-registered per-substrate Spearman statistics with Monte
Carlo permutation nulls. Writes osf/v34/v34_verdicts.json.

t1 = frozen substrate-phase data (osf/v19..v23), recomputed (parity-gated bit-for-bit
     vs v1.7 r_per_model for v0.20/21/22; provenance for v0.19/23).
t2 = v0.34 re-acquisition (osf/v34/data/<sub>/), same extraction paths.

Hypotheses (locked, prereg/v0_34_*_content.py HYPOTHESES):
  H_CPC_Temporal_Stability   PRIMARY  rho(CVCPC_t1,CVCPC_t2) >=0.70 in >=4/5 (CONF) / <0.50 in >=3/5 (FALS)
  H_CPC_Drift_Beyond_Presence PRIMARY gate  residual-CVCPC rho >=0.50 in >=3/5 (CONF); +rho(dCVCPC,dCP); >=90% saturation flag
  H_Presence_Temporal_Stability SECONDARY  rho(CP_t1,CP_t2) >=0.80 in >=4/5 (CONF) / <0.60 in >=3/5 (FALS)
  H_Phantom_Temporal_Persistence TERTIARY  descriptive retention proportion
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "scripts"))
import score_v33 as S33          # t1 extraction (parity-gated) + recog fns + RECON_CFG
import score_v0_31 as S31        # raw extractors
import score_v20, score_v21, score_v22

PANEL = S31.PANEL                # canonical-6 order
FLOOR = 1.0
N_MC = 10_000
SEED = 280400
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
DATA2 = ROOT / "osf" / "v34" / "data"

# t2 sub-dir keys
SUB2 = {"v0.19": "v19", "v0.20": "v20", "v0.21": "v21", "v0.22": "v22", "v0.23": "v23"}


# --------------------------------------------------------------------------- #
# per-wave per-brand vectors: {sub: {brand: {"recall":[6], "recog":[6]}}}
# --------------------------------------------------------------------------- #
def wave_t1():
    recall = S33.recall_counts()
    recog, _ = S33.recognition_vectors()
    out = {}
    for s in OMNI:
        rc = recall[s][0]
        rg = recog[s]
        out[s] = {b: {"recall": list(map(int, rc[b])), "recog": list(map(int, rg.get(b, [0] * 6)))}
                  for b in rc}
    return out


def wave_t2():
    """Same extraction, pointed at osf/v34/data/. Requires v19 parse + v23 coding done."""
    out = {}
    # v0.20/21/22 — raw-text matcher at extraction
    cfg = {"v0.20": ("json", ROOT / "prereg/v0_20_registry.json", score_v20),
           "v0.21": ("json", ROOT / "prereg/v0_21_registry.json", score_v21),
           "v0.22": ("module", ROOT / "prereg/v0_22_automotive_content.py", score_v22)}
    for s, (rk, rp, mod) in cfg.items():
        sub = SUB2[s]
        rc, _ = S31.counts_raw_text(rk, rp, mod, DATA2 / sub / "phase_b_results.csv")
        rg = S33.recog_raw(DATA2 / sub / "phase_a_results.csv")
        out[s] = {b: {"recall": list(map(int, rc[b])), "recog": list(map(int, rg.get(b, [0] * 6)))}
                  for b in rc}
    # v0.19 — parsed results.csv
    rc19, _ = S31.counts_v19(DATA2 / "v19" / "phase_b_results.csv")
    rg19 = S33.recog_v19(DATA2 / "v19" / "phase_a_results.csv")
    out["v0.19"] = {b: {"recall": list(map(int, rc19[b])), "recog": list(map(int, rg19.get(b, [0] * 6)))}
                    for b in rc19}
    # v0.23 — coded scored json
    rc23, _ = S31.counts_v23(DATA2 / "v23" / "v23_phase_b_scored.json")
    rg23, _ = S33.recog_v23(DATA2 / "v23" / "v23_phase_a_scored.json")
    out["v0.23"] = {b: {"recall": list(map(int, rc23[b])), "recog": list(map(int, rg23.get(b, [0] * 6)))}
                    for b in rc23}
    return out


# --------------------------------------------------------------------------- #
# metrics
# --------------------------------------------------------------------------- #
def cv_cpc(recall):
    x = np.asarray(recall, float)
    m = x.mean()
    if m < FLOOR:
        return None                      # undefined (below floor)
    cv = x.std(ddof=0) / m
    return 1.0 / (1.0 + cv)


def c_p(recog):
    return int(sum(recog))               # 0..6


def spearman(a, b):
    if len(a) < 3:
        return float("nan")
    r, _ = stats.spearmanr(a, b)
    return float(r)


def mc_perm_p(a, b, obs_rho, rng):
    """One-sided (positive-stability) permutation p: shuffle b, count rho_perm >= obs."""
    if not np.isfinite(obs_rho) or len(a) < 3:
        return float("nan")
    a = np.asarray(a, float); b = np.asarray(b, float)
    ge = 0
    for _ in range(N_MC):
        rp, _ = stats.spearmanr(a, rng.permutation(b))
        if np.isfinite(rp) and rp >= obs_rho:
            ge += 1
    return (ge + 1) / (N_MC + 1)


def residualize(cvcpc, cp):
    """OLS residuals of CV-CPC on C_P across brands (within one wave)."""
    cvcpc = np.asarray(cvcpc, float); cp = np.asarray(cp, float)
    if len(cvcpc) < 3 or np.ptp(cp) == 0:        # no C_P variance -> residual == centered cvcpc
        return cvcpc - cvcpc.mean()
    A = np.vstack([cp, np.ones_like(cp)]).T
    coef, *_ = np.linalg.lstsq(A, cvcpc, rcond=None)
    return cvcpc - A @ coef


def saturated(brands, wave, defined_keys):
    """>=90% per-model recognition among defined brands (single pre-reg trigger)."""
    if not defined_keys:
        return False, []
    rates = []
    for mi in range(6):
        rec = sum(1 for b in defined_keys if wave[b]["recog"][mi] == 1)
        rates.append(rec / len(defined_keys))
    return all(r >= 0.90 for r in rates), rates


# --------------------------------------------------------------------------- #
# main scoring
# --------------------------------------------------------------------------- #
def score():
    rng = np.random.default_rng(SEED)
    t1, t2 = wave_t1(), wave_t2()
    per_sub = {}

    for s in OMNI:
        w1, w2 = t1[s], t2[s]
        brands = [b for b in w1 if b in w2]            # present both waves
        # CV-CPC defined in BOTH waves
        cc1 = {b: cv_cpc(w1[b]["recall"]) for b in brands}
        cc2 = {b: cv_cpc(w2[b]["recall"]) for b in brands}
        both = [b for b in brands if cc1[b] is not None and cc2[b] is not None]
        a1 = [cc1[b] for b in both]; a2 = [cc2[b] for b in both]
        rho_cpc = spearman(a1, a2)
        p_cpc = mc_perm_p(a1, a2, rho_cpc, rng)

        # C_P (all brands present both waves)
        cp1 = [c_p(w1[b]["recog"]) for b in brands]
        cp2 = [c_p(w2[b]["recog"]) for b in brands]
        rho_cp = spearman(cp1, cp2)
        p_cp = mc_perm_p(cp1, cp2, rho_cp, rng)

        # gate (a): delta-coupling over `both`
        dcpc = [cc2[b] - cc1[b] for b in both]
        dcp = [c_p(w2[b]["recog"]) - c_p(w1[b]["recog"]) for b in both]
        rho_delta = spearman(dcpc, dcp)
        # gate (b): residual-CVCPC stability over `both`
        cp1b = [c_p(w1[b]["recog"]) for b in both]
        cp2b = [c_p(w2[b]["recog"]) for b in both]
        res1 = residualize(a1, cp1b); res2 = residualize(a2, cp2b)
        rho_resid = spearman(list(res1), list(res2))
        # saturation flag (either wave) among `both`
        sat1, rates1 = saturated(w1, w1, both)
        sat2, rates2 = saturated(w2, w2, both)
        sat_flag = bool(sat1 or sat2)

        # phantom persistence (below-floor at t1 retained at t2)
        ph1 = [b for b in brands if cc1[b] is None]
        ph_ret = [b for b in ph1 if cc2[b] is None]
        phantom = {"t1_phantom": len(ph1), "retained_t2": len(ph_ret),
                   "proportion": (len(ph_ret) / len(ph1)) if ph1 else None}

        # DESCRIPTIVE supplements (guidance #1): non-verdict-bearing. Captures the
        # "constant stayed constant" stability that Spearman cannot see when C_P (or
        # recall) has zero rank variance. NOT used in any verdict.
        cp_exact = sum(1 for i in range(len(brands)) if cp1[i] == cp2[i])
        recall_exact = sum(1 for b in brands if w1[b]["recall"] == w2[b]["recall"])
        n_def_t1 = sum(1 for b in brands if cc1[b] is not None)
        n_def_t2 = sum(1 for b in brands if cc2[b] is not None)
        descriptive = {
            "note": "descriptive only; non-verdict-bearing; complements rank stats where C_P/recall is rank-degenerate",
            "cp_exact_match_proportion": (cp_exact / len(brands)) if brands else None,
            "cp_constant_both_waves": (len(set(cp1)) == 1 and len(set(cp2)) == 1),
            "recall_vector_exact_match_proportion": (recall_exact / len(brands)) if brands else None,
            "defined_brand_counts": {
                "note": "CV-CPC defined (mean per-model recall >= 1.0 floor) per wave; n_both is the Spearman n",
                "n_defined_t1": n_def_t1, "n_defined_t2": n_def_t2,
                "n_defined_both": len(both), "n_brands_total": len(brands),
            },
        }

        per_sub[s] = {
            "n_brands_both_waves": len(brands),
            "cpc": {"rho": rho_cpc, "mc_p": p_cpc, "n_defined_both": len(both)},
            "presence": {"rho": rho_cp, "mc_p": p_cp, "n": len(brands)},
            "gate": {"rho_delta_cpc_cp": rho_delta, "residual_rho": rho_resid,
                     "saturation_flagged": sat_flag,
                     "per_model_recog_rate_t1": rates1, "per_model_recog_rate_t2": rates2},
            "phantom": phantom,
            "descriptive": descriptive,
        }

    out = verdicts(per_sub)
    out["delta_t"] = delta_t_table()
    return out


# --------------------------------------------------------------------------- #
# Exact t2-date stamping (guidance #3) — from acquisition timestamps.
# --------------------------------------------------------------------------- #
T1_DATE = {"v0.19": "2026-05-20", "v0.20": "2026-05-21", "v0.21": "2026-05-22",
           "v0.22": "2026-05-25", "v0.23": "2026-05-26"}


def _t2_date(sub):
    """Earliest acquisition timestamp date for a substrate's t2 data."""
    import csv as _csv
    from datetime import datetime, date
    s2 = SUB2[sub]
    stamps = []
    try:
        if sub in ("v0.20", "v0.21", "v0.22"):
            for r in _csv.DictReader(open(DATA2 / s2 / "phase_a_results.csv")):
                if r.get("timestamp"):
                    stamps.append(r["timestamp"])
        elif sub == "v0.23":
            for r in json.load(open(DATA2 / "v23" / "v23_phase_a_raw.json")):
                if r.get("ts_start"):
                    stamps.append(r["ts_start"])
        elif sub == "v0.19":
            for line in open(DATA2 / "v19" / "phase_a_responses.jsonl"):
                o = json.loads(line)
                for k in ("timestamp", "ts", "ts_start"):
                    if o.get(k):
                        stamps.append(o[k]); break
    except Exception:
        pass
    if not stamps:
        # v0.19 responses carry no ISO timestamp -> fall back to the data file's date
        try:
            import os
            f = DATA2 / SUB2[sub] / ("phase_a_responses.jsonl" if sub == "v0.19" else "phase_a_results.csv")
            return date.fromtimestamp(os.path.getmtime(f)).isoformat()
        except Exception:
            return None
    try:
        return min(datetime.fromisoformat(s.replace("Z", "+00:00")) for s in stamps).date().isoformat()
    except Exception:
        return sorted(stamps)[0][:10]


def delta_t_table():
    from datetime import date
    rows = []
    for s in OMNI:
        t1 = T1_DATE[s]; t2 = _t2_date(s)
        dd = None
        if t2:
            try:
                dd = (date.fromisoformat(t2) - date.fromisoformat(t1)).days
            except Exception:
                pass
        rows.append({"substrate": s, "t1": t1, "t2": t2, "delta_days": dd})
    return rows


def verdicts(per_sub):
    def count(pred):
        return sum(1 for s in OMNI if pred(per_sub[s]))

    # PRIMARY CV-CPC
    cpc_conf = count(lambda d: np.isfinite(d["cpc"]["rho"]) and d["cpc"]["rho"] >= 0.70)
    cpc_fals = count(lambda d: np.isfinite(d["cpc"]["rho"]) and d["cpc"]["rho"] < 0.50)
    v_cpc = "CONFIRMED" if cpc_conf >= 4 else "FALSIFIED" if cpc_fals >= 3 else "MARGINAL"

    # SECONDARY Presence
    cp_conf = count(lambda d: np.isfinite(d["presence"]["rho"]) and d["presence"]["rho"] >= 0.80)
    cp_fals = count(lambda d: np.isfinite(d["presence"]["rho"]) and d["presence"]["rho"] < 0.60)
    v_cp = "CONFIRMED" if cp_conf >= 4 else "FALSIFIED" if cp_fals >= 3 else "MARGINAL"

    # PRIMARY gate — non-flagged substrates only
    nonflag = [s for s in OMNI if not per_sub[s]["gate"]["saturation_flagged"]]
    g_conf = sum(1 for s in nonflag
                 if np.isfinite(per_sub[s]["gate"]["residual_rho"]) and per_sub[s]["gate"]["residual_rho"] >= 0.50)
    g_fals = sum(1 for s in nonflag
                 if np.isfinite(per_sub[s]["gate"]["residual_rho"]) and per_sub[s]["gate"]["residual_rho"] < 0.50)
    v_gate = ("CONFIRMED" if g_conf >= 3 else "FALSIFIED" if g_fals >= 3 else "MARGINAL")

    return {
        "phase": "v0.34", "title": "CPC Longitudinal t1->t2 Stability",
        "lock": "v0.34-prereg-r1", "seed": SEED, "mc_draws": N_MC, "panel": PANEL,
        "n_brand_units": sum(per_sub[s]["n_brands_both_waves"] for s in OMNI),
        "verdicts": {
            "H_CPC_Temporal_Stability": {"tier": "PRIMARY", "verdict": v_cpc,
                "n_conf_ge070": cpc_conf, "n_fals_lt050": cpc_fals,
                "per_substrate_rho": {s: per_sub[s]["cpc"]["rho"] for s in OMNI}},
            "H_CPC_Drift_Beyond_Presence": {"tier": "PRIMARY_gate", "verdict": v_gate,
                "directional_lean": "FALSIFIED-or-marginal",
                "nonflagged_substrates": nonflag, "n_resid_ge050": g_conf, "n_resid_lt050": g_fals,
                "per_substrate_residual_rho": {s: per_sub[s]["gate"]["residual_rho"] for s in OMNI},
                "per_substrate_delta_coupling_rho": {s: per_sub[s]["gate"]["rho_delta_cpc_cp"] for s in OMNI},
                "saturation_flagged": {s: per_sub[s]["gate"]["saturation_flagged"] for s in OMNI}},
            "H_Presence_Temporal_Stability": {"tier": "SECONDARY", "verdict": v_cp,
                "n_conf_ge080": cp_conf, "n_fals_lt060": cp_fals,
                "per_substrate_rho": {s: per_sub[s]["presence"]["rho"] for s in OMNI}},
            "H_Phantom_Temporal_Persistence": {"tier": "TERTIARY", "verdict": "DESCRIPTIVE",
                "per_substrate": {s: per_sub[s]["phantom"] for s in OMNI}},
        },
        "per_substrate": per_sub,
    }


def _clean(o):
    """JSON-safe: NaN/inf floats -> None (valid JSON). Serialization only; no verdict change."""
    if isinstance(o, float):
        return None if not np.isfinite(o) else o
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_clean(v) for v in o]
    return o


if __name__ == "__main__":
    out = score()
    p = ROOT / "osf" / "v34" / "v34_verdicts.json"
    json.dump(_clean(out), open(p, "w"), indent=2, allow_nan=False)
    print(f"wrote {p}")
    for tag, v in out["verdicts"].items():
        print(f"  {tag}: {v['verdict']}")
