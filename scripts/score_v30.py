#!/usr/bin/env python3
"""
v0.30 (CPC.01) — CPC Consistency Instrument scorer.
Locked against v0.30-prereg-r2 (doubly-homogeneous trio v0.20 / v0.21 / v0.22).

Single-source discipline: ALL thresholds are read from the pre-reg module
prereg/v0_30_cpc_instrument_pilot_content.py (SCORING dict + CEIL_MU / FLOOR_MU).
No threshold or methodology is defined here.

Mention detection REUSES each phase's own v1.4 canonical matcher
(scripts/score_v20.py / score_v21.py / score_v22.py :: detect_mention) — not
reimplemented — so recall detection matches how each phase was originally scored.

No new LLM calls. Reuses already-deposited Phase A + Phase B data.
"""
import sys, json, csv, hashlib, importlib, warnings
from pathlib import Path
import numpy as np
from scipy import stats

ROOT = Path.home() / "aias"
sys.path.insert(0, str(ROOT / "prereg"))
sys.path.insert(0, str(ROOT / "scripts"))

# --- single-source thresholds from the locked pre-reg module -----------------
import v0_30_cpc_instrument_pilot_content as PREREG
S = PREREG.SCORING
COVERAGE_FLOOR    = S["coverage_floor"]        # F1  0.50
CONFOUND_RHO_MIN  = S["confound_rho_min"]      # F2  0.30
CORRECTED_CEILING = S["corrected_ceiling"]     # F3  0.20
ATTEN_CONFIRM     = S["attenuation_confirm"]   # F3  0.50
ATTEN_FLOOR       = S["attenuation_floor"]     # F3  0.30
KW_ALPHA          = S["kw_alpha"]              # F4  0.05
MIN_N             = S["min_n_for_valid_rho"]   # 12
N_BOOT            = S["bootstrap_resamples"]   # 10000
SEED              = S["bootstrap_seed"]        # 280400
CEIL_MU           = PREREG.CEIL_MU             # 0.98
FLOOR_MU          = PREREG.FLOOR_MU            # 0.0
SIG_ALPHA         = 0.05                        # significance for Spearman p
PANEL             = list(PREREG.REFERENCE_PANEL)  # 6 fixed models

import score_v20, score_v21, score_v22

SUBSTRATES = [
    {"key": "v0.20", "name": "skincare",   "mod": score_v20,
     "reg": ("json",   ROOT / "prereg" / "v0_20_registry.json"),
     "pa": ROOT / "osf/v20/phase_a_results.csv", "pb": ROOT / "osf/v20/phase_b_results.csv"},
    {"key": "v0.21", "name": "cosmetics",  "mod": score_v21,
     "reg": ("json",   ROOT / "prereg" / "v0_21_registry.json"),
     "pa": ROOT / "osf/v21/phase_a_results.csv", "pb": ROOT / "osf/v21/phase_b_results.csv"},
    {"key": "v0.22", "name": "automotive", "mod": score_v22,
     "reg": ("module", ROOT / "prereg" / "v0_22_automotive_content.py"),
     "pa": ROOT / "osf/v22/phase_a_results.csv", "pb": ROOT / "osf/v22/phase_b_results.csv"},
]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(65536), b""):
            h.update(c)
    return h.hexdigest()


def brand_list(sub):
    kind, path = sub["reg"]
    reg = sub["mod"].load_registry(path) if kind == "json" else sub["mod"].load_prereg_module(path)
    return [b["name"] for cell in reg["cells"].values() for b in cell["brands"]]


def read_csv(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pop_sd(vec):
    return float(np.std(np.asarray(vec, float), ddof=0))


def spearman_ci(x, y):
    """Spearman rho, p, and BCa 95% CI (N_BOOT, SEED). Returns dict; CI nan if degenerate."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    res = stats.spearmanr(x, y)
    rho, p = float(res.statistic), float(res.pvalue)
    ci_lo = ci_hi = float("nan")
    if len(x) >= MIN_N:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                bs = stats.bootstrap(
                    (x, y),
                    lambda a, b: stats.spearmanr(a, b).statistic,
                    paired=True, vectorized=False, n_resamples=N_BOOT,
                    method="BCa", random_state=SEED,
                )
            ci_lo, ci_hi = float(bs.confidence_interval.low), float(bs.confidence_interval.high)
        except Exception:
            pass
    return {"rho": rho, "p": p, "ci_low": ci_lo, "ci_high": ci_hi, "n": int(len(x))}


# --- per-substrate CPC computation -------------------------------------------
def score_substrate(sub):
    brands = brand_list(sub)
    pa = read_csv(sub["pa"])
    pb = read_csv(sub["pb"])
    detect = sub["mod"].detect_mention

    # Phase A: per-(brand,model) recognized bool; C_P = count over panel
    recog = {b: {} for b in brands}
    for r in pa:
        if r["brand"] in recog and r["model"] in PANEL:
            recog[r["brand"]][r["model"]] = (r["recognized"].strip().lower() == "yes")

    # Phase B: frames present per model (denominator guard), and per-(brand,model) mention over frames
    frames_by_model = {m: set() for m in PANEL}
    rows_by_model = {m: [] for m in PANEL}
    for r in pb:
        m = r["model"]
        if m in PANEL:
            frames_by_model[m].add(r["frame_id"])
            rows_by_model[m].append(r)
    denom = {m: len(frames_by_model[m]) for m in PANEL}

    out = []
    recall_s, recog_vecs = {}, {}
    for b in brands:
        s_vec = []
        ok = True
        for m in PANEL:
            d = denom[m]
            if d == 0:
                ok = False; break
            hits = sum(1 for row in rows_by_model[m] if detect(row["response_text"], b))
            s_vec.append(hits / d)
        if not ok or len(s_vec) != 6:
            continue  # require all 6 models present
        recall_s[b] = s_vec
        # recognition vector (binary) over panel
        rvec = [1.0 if recog.get(b, {}).get(m, False) else 0.0 for m in PANEL]
        recog_vecs[b] = rvec

    # build per-brand records
    records = {}
    for b in brands:
        if b not in recall_s:
            continue
        s = np.asarray(recall_s[b], float)
        mu = float(s.mean()); sd = pop_sd(s)
        cp = int(sum(recog_vecs[b]))
        recall_defined = not (mu == FLOOR_MU or mu >= CEIL_MU)
        cpc_raw  = (sd / mu) if (recall_defined and mu > 0) else None
        cpc_corr = (sd / np.sqrt(mu * (1 - mu))) if recall_defined else None
        recog_defined = (0 < cp < 6)
        records[b] = {
            "brand": b, "substrate": sub["key"], "mu": mu, "sd_pop": sd,
            "cpc_raw": cpc_raw, "cpc_corr": cpc_corr, "cpc_resid": None,
            "C_P": cp, "L": cp,
            "recall_defined": recall_defined, "recog_defined": recog_defined,
        }

    # level-residualized CV (robustness): regress CPC_raw on mu across DEFINED brands
    dfb = [r for r in records.values() if r["recall_defined"] and r["cpc_raw"] is not None]
    if len(dfb) >= 2:
        mus = np.array([r["mu"] for r in dfb]); cvs = np.array([r["cpc_raw"] for r in dfb])
        slope, intercept = np.polyfit(mus, cvs, 1)
        for r in dfb:
            r["cpc_resid"] = float(r["cpc_raw"] - (slope * r["mu"] + intercept))

    # recognition-CPC_corr per brand (exploratory comparator)
    recog_cpc = {}
    for b, rvec in recog_vecs.items():
        v = np.asarray(rvec, float); mu_r = float(v.mean())
        if 0 < mu_r < 1:
            recog_cpc[b] = pop_sd(v) / np.sqrt(mu_r * (1 - mu_r))

    n = len(records)
    recall_cov = sum(r["recall_defined"] for r in records.values()) / n if n else 0.0
    recog_cov  = sum(r["recog_defined"]  for r in records.values()) / n if n else 0.0
    return {
        "key": sub["key"], "name": sub["name"], "n_brands": n,
        "recall_coverage": recall_cov, "recognition_coverage": recog_cov,
        "records": records, "recog_cpc": recog_cpc,
        "frames_per_model": denom,
    }


def main():
    subs = [score_substrate(s) for s in SUBSTRATES]
    by = {s["key"]: s for s in subs}

    # ---- F1: computability / coverage ----
    recall_covs = {s["key"]: s["recall_coverage"] for s in subs}
    recog_covs  = {s["key"]: s["recognition_coverage"] for s in subs}
    all_ge_floor = all(c >= COVERAGE_FLOOR for c in recall_covs.values())
    auto_gap = by["v0.22"]["recall_coverage"] > by["v0.22"]["recognition_coverage"]
    F1 = "CONFIRM" if (all_ge_floor and auto_gap) else "FALSIFIED"

    # ---- F2 / F3 per substrate ----
    # A substrate is TESTABLE for the confound only if n >= MIN_N AND L has
    # variance (>= 2 distinct L values) — otherwise Spearman rho(CPC, L) is
    # mathematically undefined (constant input) and the substrate is UNDETERMINED,
    # NOT evidence for or against. With < 2 testable substrates the >=2/3 bar
    # cannot be reached, so the hypothesis verdict is UNDETERMINED (not FALSIFIED).
    f2_rows, f3_rows = {}, {}
    f2_confirm = f3_confirm = 0
    n_testable = 0
    for s in subs:
        k = s["key"]
        defined = [r for r in s["records"].values() if r["recall_defined"] and r["cpc_corr"] is not None and r["cpc_raw"] is not None]
        L  = [r["L"] for r in defined]
        raw = [r["cpc_raw"] for r in defined]
        corr = [r["cpc_corr"] for r in defined]
        resid = [r["cpc_resid"] for r in defined]
        nd = len(defined)
        l_constant = len(set(L)) < 2
        testable = (nd >= MIN_N) and (not l_constant)
        undetermined = not testable
        undet_reason = None
        if nd < MIN_N:
            undet_reason = f"n={nd} < MIN_N={MIN_N}"
        elif l_constant:
            undet_reason = f"L (recognition C_P) constant at {L[0] if L else 'NA'} — rho undefined (recognition saturated)"
        r2 = spearman_ci(raw, L)
        r3 = spearman_ci(corr, L)
        rr = spearman_ci(resid, L)
        atten = (1 - abs(r3["rho"]) / abs(r2["rho"])) if (r2["rho"] == r2["rho"] and r2["rho"] != 0) else float("nan")
        f2_sig = testable and (r2["p"] < SIG_ALPHA) and (abs(r2["rho"]) >= CONFOUND_RHO_MIN)
        f3_sig = testable and (abs(r3["rho"]) < CORRECTED_CEILING) and (atten >= ATTEN_CONFIRM)
        f3_falsify = testable and ((atten < ATTEN_FLOOR) or (r3["p"] < SIG_ALPHA and abs(r3["rho"]) >= abs(r2["rho"])))
        if testable:
            n_testable += 1
            if f2_sig: f2_confirm += 1
            if f3_sig: f3_confirm += 1
        f2_rows[k] = {**r2, "defined_n": nd, "testable": testable, "undetermined": undetermined,
                      "undetermined_reason": undet_reason, "meets_F2": bool(f2_sig)}
        f3_rows[k] = {**r3, "defined_n": nd, "testable": testable, "undetermined": undetermined,
                      "undetermined_reason": undet_reason,
                      "attenuation": (None if np.isnan(atten) else atten),
                      "meets_F3": bool(f3_sig), "f3_falsify_flag": bool(f3_falsify),
                      "resid_rho": rr["rho"], "resid_p": rr["p"]}

    def verdict_2of3(confirm, testable):
        if confirm >= 2:
            return "CONFIRM"
        if testable < 2:
            return "UNDETERMINED"   # cannot reach the >=2/3 bar — too few testable substrates
        return "FALSIFIED"
    F2 = verdict_2of3(f2_confirm, n_testable)
    F3 = verdict_2of3(f3_confirm, n_testable)

    # ---- F4: Kruskal-Wallis across substrates' CPC_corr (defined) ----
    groups = []
    for s in subs:
        groups.append([r["cpc_corr"] for r in s["records"].values() if r["recall_defined"] and r["cpc_corr"] is not None])
    kw = stats.kruskal(*groups)
    F4 = "CONFIRM" if kw.pvalue < KW_ALPHA else "FALSIFIED"

    # ---- Exploratory: recognition-CPC vs recall-CPC rank concordance ----
    cx, cy = [], []
    per_sub_conc = {}
    for s in subs:
        sx, sy = [], []
        for b, rec in s["records"].items():
            if rec["recall_defined"] and rec["cpc_corr"] is not None and b in s["recog_cpc"]:
                sx.append(s["recog_cpc"][b]); sy.append(rec["cpc_corr"])
        if len(sx) >= 3:
            pr = stats.spearmanr(sx, sy)
            per_sub_conc[s["key"]] = {"rho": float(pr.statistic), "p": float(pr.pvalue), "n": len(sx)}
        cx += sx; cy += sy
    pooled = stats.spearmanr(cx, cy) if len(cx) >= 3 else None
    concordance = {"pooled": ({"rho": float(pooled.statistic), "p": float(pooled.pvalue), "n": len(cx)} if pooled else None),
                   "per_substrate": per_sub_conc}

    # ---- write per-brand CSV ----
    out_dir = ROOT / "osf/v30/data"; out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "v30_cpc.csv"
    cols = ["brand", "substrate", "mu", "sd_pop", "cpc_raw", "cpc_corr", "cpc_resid",
            "C_P", "L", "recall_defined", "recog_defined"]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for s in subs:
            for b, r in s["records"].items():
                w.writerow({c: r[c] for c in cols})

    # ---- input certification ----
    certified = {}
    for s in SUBSTRATES:
        certified[s["key"]] = {"phase_a": sha256(s["pa"]), "phase_b": sha256(s["pb"])}

    verdicts = {
        "phase": "v0.30", "cpc_index": "CPC.01", "lock": "v0.30-prereg-r2",
        "scope": "CPC_model (confirmatory)", "no_new_llm_calls": True,
        "thresholds_source": "prereg/v0_30_cpc_instrument_pilot_content.py :: SCORING",
        "trio": [{"key": s["key"], "name": s["name"]} for s in subs],
        "coverage": {s["key"]: {"recall": s["recall_coverage"],
                                "recognition": s["recognition_coverage"],
                                "n_brands": s["n_brands"],
                                "frames_per_model": s["frames_per_model"]} for s in subs},
        "F1_H_CPC_Computable": {"verdict": F1, "all_ge_floor": all_ge_floor,
                                "automotive_recall_gt_recognition": auto_gap,
                                "coverage_floor": COVERAGE_FLOOR},
        "F2_H_CPC_LevelConfound": {"verdict": F2, "confirm_count": f2_confirm, "n_testable": n_testable,
                                   "confound_rho_min": CONFOUND_RHO_MIN, "per_substrate": f2_rows},
        "F3_H_CPC_LevelCorrected": {"verdict": F3, "confirm_count": f3_confirm, "n_testable": n_testable,
                                    "corrected_ceiling": CORRECTED_CEILING,
                                    "attenuation_confirm": ATTEN_CONFIRM,
                                    "attenuation_floor": ATTEN_FLOOR, "per_substrate": f3_rows},
        "level_variable_note": ("L = Phase A recognition C_P is SATURATED (C_P=6 for ~all brands) in "
                                "cosmetics and automotive, so rho(CPC, L) is undefined there; only "
                                "skincare is testable for F2/F3. See v1_7 forward note."),
        "F4_H_CPC_SubstrateVariation": {"verdict": F4, "kruskal_H": float(kw.statistic),
                                        "kruskal_p": float(kw.pvalue), "kw_alpha": KW_ALPHA},
        "exploratory_recognition_vs_recall_concordance": concordance,
        "certified_inputs_sha256": certified,
        "bootstrap": {"resamples": N_BOOT, "seed": SEED, "method": "BCa", "ci": "95%"},
    }
    vpath = ROOT / "osf/v30/v30_cpc_verdicts.json"
    with open(vpath, "w") as f:
        json.dump(verdicts, f, indent=2)

    # ---- console summary ----
    print("=" * 78)
    print("v0.30 (CPC.01) verdicts — lock v0.30-prereg-r2  |  trio: skincare / cosmetics / automotive")
    print("=" * 78)
    print(f"  F1 H_CPC_Computable      : {F1}")
    print(f"  F2 H_CPC_LevelConfound   : {F2}   (confirm {f2_confirm}/{n_testable} testable; {3-n_testable} substrate(s) UNDETERMINED — L saturated)")
    print(f"  F3 H_CPC_LevelCorrected  : {F3}   (confirm {f3_confirm}/{n_testable} testable)  [HEADLINE]")
    print(f"  F4 H_CPC_SubstrateVar    : {F4}   (Kruskal-Wallis H={kw.statistic:.3f}, p={kw.pvalue:.4g})")
    print()
    hdr = f"{'substrate':<12}{'n':>3}{'recallCov':>11}{'recogCov':>10}{'rho_raw(L)':>12}{'rho_corr(L)':>13}{'atten':>8}{'rho_resid':>11}"
    print(hdr); print("-" * len(hdr))
    for s in subs:
        k = s["key"]; a = f2_rows[k]; b = f3_rows[k]
        at = b["attenuation"]
        print(f"{s['name']:<12}{a['defined_n']:>3}{s['recall_coverage']*100:>10.0f}%{s['recognition_coverage']*100:>9.0f}%"
              f"{a['rho']:>12.3f}{b['rho']:>13.3f}{(at if at is not None else float('nan')):>8.2f}{b['resid_rho']:>11.3f}")
    print()
    pc = concordance["pooled"]
    if pc: print(f"  exploratory recognition-vs-recall CPC concordance (pooled): rho={pc['rho']:.3f}, p={pc['p']:.4g}, n={pc['n']}")
    print(f"\n  wrote: {csv_path}")
    print(f"  wrote: {vpath}")
    return verdicts


if __name__ == "__main__":
    main()
