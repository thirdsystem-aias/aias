"""v0.12 Hypothesis evaluation: H1-H4 per category, H5/H6 cross-category,
and Category-Scale Mismatch Finding for olive oil (descriptive-only per
pre-reg §3.4a).

Inputs:
  - ~/aias/osf_staging/v09/data/{pm,oliveoil,running}/results_enriched_v06_*.csv  (t1)
  - ~/aias/osf_staging/v09/data/{pm,oliveoil,running}/results_enriched_v09_*.csv  (t2)
  - ~/aias/osf/v12/data/trends_processed/per_brand_within_window.csv
  - ~/aias/osf/v12/registries/brand_age_sources_v0.12.csv
  - ~/aias/osf/v12/registries/topic_id_resolution_log_v0.12.csv (E1a flags)
  - ~/aias/registries/brands_{pm,oliveoil,running}.json

Outputs:
  - ~/aias/osf/v12/analysis/per_brand_paired.csv
  - ~/aias/osf/v12/analysis/canonical_scoring.csv
  - ~/aias/osf/v12/analysis/canonical_scoring.json
  - ~/aias/osf/v12/analysis/category_scale_mismatch_table.csv

Key conventions:
  - Pre-reg §5.1 pivot exemption applied: pivots eligible despite Trends sd=0
  - Pre-acquisition exclusions (E1a) loaded from topic_id_resolution_log_v0.12.csv
  - At-acquisition exclusions (E1b) per-wave from per_brand_within_window.csv
  - n-floor: hard 10 (descriptive route below), alignment 12 per pre-reg §3.4
  - H5/H6 cross-category: 2-of-2 effective (olive oil routed to descriptive-only)
  - Partial Spearman: Pearson on rank residuals after OLS on rank-transformed
    covariates; df corrected by k=2

Run:
    python scripts/score_v12.py
"""
import csv
import glob
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# ============================================================================
# Configuration
# ============================================================================

HOME = Path.home()
V12_ROOT = HOME / "aias" / "osf" / "v12"
V09_DATA = HOME / "aias" / "osf_staging" / "v09" / "data"
REGISTRIES_DIR = HOME / "aias" / "registries"

TRENDS_FILE = V12_ROOT / "data" / "trends_processed" / "per_brand_within_window.csv"
AGE_FILE = V12_ROOT / "registries" / "brand_age_sources_v0.12.csv"
PHASE_B_LOG = V12_ROOT / "registries" / "topic_id_resolution_log_v0.12.csv"

OUT_DIR = V12_ROOT / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MATCHED_MODELS = {"claude-sonnet-4-6", "gpt-5.4-mini"}

# Per-category configuration
CATEGORIES = {
    "pmsoftware": {
        "pivot": "Asana",
        "data_dir": "pm",
        "registry": "brands_pm.json",
        "descriptive_only": False,
    },
    "oliveoil": {
        "pivot": "California Olive Ranch",
        "data_dir": "oliveoil",
        "registry": "brands_oliveoil.json",
        "descriptive_only": True,  # pre-reg §3.4a
    },
    "running": {
        "pivot": "Asics",
        "data_dir": "running",
        "registry": "brands_running.json",
        "descriptive_only": False,
    },
}

# Hypothesis thresholds (per pre-reg §3)
H1_RHO_THRESHOLD = 0.5
H1_P_THRESHOLD = 0.05
H2_DELTA_THRESHOLD = 0.15
H3_TOP_K_AI = 3
H3_TOP_K_TRENDS = 5
H4_RHO_THRESHOLD = 0.5
H4_P_THRESHOLD = 0.05
N_FLOOR_HARD = 10
N_FLOOR_ALIGN = 12

# H6 thresholds (per pre-reg §2.2 H6a)
H6_LINEAR_AI_MIN = 50.0
H6_LINEAR_TRENDS_MAX = 5.0
H6_TODOIST_AI_MAX = 5.0
H6_TODOIST_TRENDS_MIN = 20.0

# Category-scale-mismatch threshold (pre-reg §10.2)
SCALE_MISMATCH_AI_MIN = 5.0  # brand counts as scale-mismatch if AI Pres >= 5% AND Trends below display threshold

TIER_ORDINAL = {"incumbent": 1, "mid-tier": 2, "challenger": 3}

# ============================================================================
# Step 1: Load E1a exclusions from Phase B locked CSV
# ============================================================================

phase_b = pd.read_csv(PHASE_B_LOG)
e1a_by_cat = {cat: set() for cat in CATEGORIES}
for _, row in phase_b.iterrows():
    if row["final_query_tier"] == "EXCLUDED_E1a":
        e1a_by_cat[row["category"]].add(row["brand_canonical"])

print("E1a exclusions by category (from Phase B locked CSV):")
for cat, brands in e1a_by_cat.items():
    print(f"  {cat}: {sorted(brands) if brands else '(none)'}")
print()

# ============================================================================
# Step 2: Load registries per category
# ============================================================================

registries = {}
for cat, cfg in CATEGORIES.items():
    reg_path = REGISTRIES_DIR / cfg["registry"]
    with reg_path.open() as f:
        r = json.load(f)
    brands_list = r["brands"] if isinstance(r, dict) else r
    registries[cat] = brands_list

# ============================================================================
# Step 3: Compute AI Presence rates per category per wave
# ============================================================================

def compute_presence(csv_path, registry_brands):
    df = pd.read_csv(csv_path)
    df = df[df["model_version"].isin(MATCHED_MODELS)]
    df = df[df["call_status"] == "ok"]
    n = len(df)
    presence = {}
    for b in [r["canonical"] for r in registry_brands]:
        def hit(s):
            if pd.isna(s):
                return False
            return b in str(s).split("|")
        c = int(df["brands_canonical"].apply(hit).sum())
        presence[b] = round(100.0 * c / n, 2) if n else 0.0
    return presence, n


ai_presence = {}  # ai_presence[cat][wave][brand] = pct
n_responses = {}  # n_responses[cat][wave] = int
for cat, cfg in CATEGORIES.items():
    data_dir = V09_DATA / cfg["data_dir"]
    v06_files = sorted(glob.glob(str(data_dir / "results_enriched_v06_*.csv")))
    v09_files = sorted(glob.glob(str(data_dir / "results_enriched_v09_*.csv")))
    if not v06_files or not v09_files:
        print(f"WARN: missing v06 or v09 files for {cat} at {data_dir}")
        continue
    v06_path = Path(v06_files[-1])  # latest
    v09_path = Path(v09_files[-1])
    print(f"{cat}: t1 source = {v06_path.name}; t2 source = {v09_path.name}")
    p_t1, n_t1 = compute_presence(v06_path, registries[cat])
    p_t2, n_t2 = compute_presence(v09_path, registries[cat])
    ai_presence[cat] = {"t1": p_t1, "t2": p_t2}
    n_responses[cat] = {"t1": n_t1, "t2": n_t2}
print()

# ============================================================================
# Step 4: Load Trends + ages, build paired dataset per category
# ============================================================================

trends_df = pd.read_csv(TRENDS_FILE)
age_df = pd.read_csv(AGE_FILE)
age_map = dict(zip(age_df["brand"], age_df["founding_year"]))
age_yrs_map = dict(zip(age_df["brand"], age_df["age_as_of_2026_01_01"]))


def build_paired(cat):
    """Build paired dataset for one category. Returns DataFrame."""
    pivot = CATEGORIES[cat]["pivot"]
    brand_tier = {b["canonical"]: b["tier"] for b in registries[cat]}
    analysis_brands = [b["canonical"] for b in registries[cat]
                       if b["canonical"] not in e1a_by_cat[cat]]

    trends_ww = trends_df[(trends_df["region"] == "worldwide") &
                          (trends_df["category"] == cat)].set_index("brand")
    trends_us = trends_df[(trends_df["region"] == "US") &
                          (trends_df["category"] == cat)].set_index("brand")

    records = []
    for b in [r["canonical"] for r in registries[cat]]:  # all registry brands incl. E1a
        rec = {
            "brand": b,
            "category": cat,
            "market_tier": brand_tier.get(b, ""),
            "tier_ordinal": TIER_ORDINAL.get(brand_tier.get(b, ""), None),
            "brand_age_years": age_yrs_map.get(b),
            "founding_year": age_map.get(b),
            "ai_t1_pct": ai_presence.get(cat, {}).get("t1", {}).get(b, 0.0),
            "ai_t2_pct": ai_presence.get(cat, {}).get("t2", {}).get(b, 0.0),
            "e1a_excluded": b in e1a_by_cat[cat],
            "is_pivot": b == pivot,
        }
        for label, src in [("ww", trends_ww), ("us", trends_us)]:
            if b in src.index:
                row = src.loc[b]
                for w in ("t1", "t2"):
                    rec[f"trends_{label}_{w}_mean"] = (
                        float(row[f"{w}_mean"]) if pd.notna(row[f"{w}_mean"]) else None
                    )
                    rec[f"trends_{label}_{w}_eligible"] = bool(row[f"{w}_eligible_E1b"])
                    rec[f"trends_{label}_{w}_raw_eligible"] = bool(row[f"{w}_raw_eligible"])
                    rec[f"trends_{label}_{w}_sparse"] = bool(row[f"{w}_sparse_E5"])
            else:
                for w in ("t1", "t2"):
                    rec[f"trends_{label}_{w}_mean"] = None
                    rec[f"trends_{label}_{w}_eligible"] = False
                    rec[f"trends_{label}_{w}_raw_eligible"] = False
                    rec[f"trends_{label}_{w}_sparse"] = False
        # Pivot exemption per pre-reg §5.1
        if b == pivot:
            for label in ("ww", "us"):
                for w in ("t1", "t2"):
                    rec[f"trends_{label}_{w}_eligible"] = True
        records.append(rec)
    return pd.DataFrame(records)


paired_all = pd.concat([build_paired(cat) for cat in CATEGORIES], ignore_index=True)
paired_path = OUT_DIR / "per_brand_paired.csv"
paired_all.to_csv(paired_path, index=False)
print(f"Paired dataset: {paired_path} ({len(paired_all)} rows)")
print()

# ============================================================================
# Step 5: Correlation function (Spearman + Pearson + partial Spearman)
# ============================================================================

def correlations(df, region, wave, raw_strict=False):
    """Compute correlations for one (category, region, wave) slice.

    df: paired dataset for ONE category (already filtered).
    raw_strict: if True, only include brands with raw_eligible=True (sensitivity).
    """
    elig_col = f"trends_{region}_{wave}_eligible"
    raw_col = f"trends_{region}_{wave}_raw_eligible"
    elig = df[df[elig_col]].copy()
    if raw_strict:
        elig = elig[elig[raw_col]]
    elig = elig[~elig["e1a_excluded"]]
    elig = elig.dropna(subset=[f"trends_{region}_{wave}_mean", f"ai_{wave}_pct",
                                "brand_age_years", "tier_ordinal"])
    n = len(elig)
    out = {"n": n, "brands": list(elig["brand"])}
    if n < 4:
        for k in ("spearman_rho", "spearman_p_two_tailed", "spearman_p_one_tailed",
                  "pearson_r", "pearson_p_two_tailed", "pearson_p_one_tailed",
                  "partial_spearman_rho", "partial_spearman_p_one_tailed"):
            out[k] = None
        return out

    x = elig[f"ai_{wave}_pct"].values.astype(float)
    y = elig[f"trends_{region}_{wave}_mean"].values.astype(float)

    rho, p_rho = stats.spearmanr(x, y)
    p_rho_1t = float(p_rho / 2) if rho > 0 else float(1 - p_rho / 2)

    r, p_r = stats.pearsonr(x, y)
    p_r_1t = float(p_r / 2) if r > 0 else float(1 - p_r / 2)

    z1 = elig["brand_age_years"].values.astype(float)
    z2 = elig["tier_ordinal"].values.astype(float)
    xr = stats.rankdata(x)
    yr = stats.rankdata(y)
    z1r = stats.rankdata(z1)
    z2r = stats.rankdata(z2)
    Z = np.column_stack([np.ones(n), z1r, z2r])

    def resid(t):
        coef, *_ = np.linalg.lstsq(Z, t, rcond=None)
        return t - Z @ coef

    xr_res = resid(xr)
    yr_res = resid(yr)
    pr, _ = stats.pearsonr(xr_res, yr_res)
    df_adj = n - 2 - 2
    if df_adj > 0 and abs(pr) < 1:
        t_stat = pr * np.sqrt(df_adj / (1 - pr ** 2))
        partial_p_1t = float(1 - stats.t.cdf(t_stat, df=df_adj))
    else:
        partial_p_1t = float("nan")

    out.update({
        "spearman_rho": float(rho),
        "spearman_p_two_tailed": float(p_rho),
        "spearman_p_one_tailed": p_rho_1t,
        "pearson_r": float(r),
        "pearson_p_two_tailed": float(p_r),
        "pearson_p_one_tailed": p_r_1t,
        "partial_spearman_rho": float(pr),
        "partial_spearman_p_one_tailed": partial_p_1t,
    })
    return out

# ============================================================================
# Step 6: Hypothesis evaluators
# ============================================================================

def eval_h1_or_h4(t1, t2, thr_rho, thr_p, key_rho, key_p, label):
    if t1["n"] < N_FLOOR_HARD or t2["n"] < N_FLOOR_HARD:
        return {
            "status": "INDETERMINATE",
            "rationale": f"n-floor breached: t1 n={t1['n']}, t2 n={t2['n']} (hard floor={N_FLOOR_HARD})",
            "threshold_rho": thr_rho, "threshold_p": thr_p,
            f"{label}_t1": t1.get(key_rho), f"{label}_t2": t2.get(key_rho),
        }
    rt1, rt2, pt1, pt2 = t1[key_rho], t2[key_rho], t1[key_p], t2[key_p]
    pass1 = (rt1 is not None) and rt1 > thr_rho and pt1 < thr_p
    pass2 = (rt2 is not None) and rt2 > thr_rho and pt2 < thr_p
    status = "CONFIRMED" if (pass1 and pass2) else "FALSIFIED"
    return {
        "status": status,
        "threshold_rho": thr_rho, "threshold_p": thr_p,
        f"{label}_t1": rt1, f"{label}_t2": rt2,
        "p_t1_one_tailed": pt1, "p_t2_one_tailed": pt2,
        "pass_t1": pass1, "pass_t2": pass2,
        "rationale": (
            f"t1: ρ={rt1:.3f} (>{thr_rho}? {rt1 > thr_rho}), "
            f"p1t={pt1:.4f} (<{thr_p}? {pt1 < thr_p}). "
            f"t2: ρ={rt2:.3f}, p1t={pt2:.4f}."
        ),
    }


def eval_h2(t1, t2):
    if t1["n"] < N_FLOOR_HARD or t2["n"] < N_FLOOR_HARD:
        return {"status": "INDETERMINATE", "rationale": "n-floor breached"}
    rho1, rho2 = t1["spearman_rho"], t2["spearman_rho"]
    delta = abs(rho2 - rho1)
    return {
        "status": "CONFIRMED" if delta <= H2_DELTA_THRESHOLD else "FALSIFIED",
        "rho_t1": rho1, "rho_t2": rho2, "abs_delta_rho": delta,
        "threshold": H2_DELTA_THRESHOLD,
        "rationale": f"|Δρ| = |{rho2:.3f} − {rho1:.3f}| = {delta:.3f} {'≤' if delta <= H2_DELTA_THRESHOLD else '>'} {H2_DELTA_THRESHOLD}",
    }


def eval_h3(df_cat, region):
    out = {"per_wave": {}, "status_per_wave": {}}
    pass_both = True
    for wave in ("t1", "t2"):
        e = df_cat[df_cat[f"trends_{region}_{wave}_eligible"] & (~df_cat["e1a_excluded"])].copy()
        e = e.dropna(subset=[f"trends_{region}_{wave}_mean", f"ai_{wave}_pct"])
        top3_ai = list(e.sort_values(f"ai_{wave}_pct", ascending=False).head(H3_TOP_K_AI)["brand"])
        top5_t = list(e.sort_values(f"trends_{region}_{wave}_mean", ascending=False).head(H3_TOP_K_TRENDS)["brand"])
        in5 = [b for b in top3_ai if b in top5_t]
        out["per_wave"][wave] = {
            "top3_ai": top3_ai, "top5_trends": top5_t,
            "top3_in_top5": in5, "n_in_top5": len(in5),
        }
        ws = "CONFIRMED" if len(in5) == H3_TOP_K_AI else "FALSIFIED"
        out["status_per_wave"][wave] = ws
        if ws != "CONFIRMED":
            pass_both = False
    out["status"] = "CONFIRMED" if pass_both else "FALSIFIED"
    return out


def detect_h6_diagnostics(df_cat, region):
    """Find Linear-style and Todoist-style brands per wave per category."""
    out = {"per_wave": {}}
    confirms_both_waves = True
    for wave in ("t1", "t2"):
        e = df_cat[df_cat[f"trends_{region}_{wave}_eligible"] & (~df_cat["e1a_excluded"])].copy()
        e = e.dropna(subset=[f"trends_{region}_{wave}_mean", f"ai_{wave}_pct"])
        linear_style = list(e[(e[f"ai_{wave}_pct"] >= H6_LINEAR_AI_MIN) &
                              (e[f"trends_{region}_{wave}_mean"] <= H6_LINEAR_TRENDS_MAX)]["brand"])
        todoist_style = list(e[(e[f"ai_{wave}_pct"] <= H6_TODOIST_AI_MAX) &
                               (e[f"trends_{region}_{wave}_mean"] >= H6_TODOIST_TRENDS_MIN)]["brand"])
        out["per_wave"][wave] = {
            "linear_style": linear_style,
            "todoist_style": todoist_style,
            "h6a_confirmed": len(linear_style) > 0 and len(todoist_style) > 0,
        }
        if not (linear_style and todoist_style):
            confirms_both_waves = False
    out["h6a_status"] = "CONFIRMED" if confirms_both_waves else "FALSIFIED"
    return out

# ============================================================================
# Step 7: Per-category evaluation
# ============================================================================

all_results = {}

for cat in CATEGORIES:
    df_cat = paired_all[paired_all["category"] == cat].copy()
    descriptive_only = CATEGORIES[cat]["descriptive_only"]

    print("=" * 80)
    print(f"### CATEGORY: {cat}  (descriptive-only: {descriptive_only})")
    print("=" * 80)

    cat_results = {"descriptive_only": descriptive_only, "correlations": {}, "hypotheses": {}}

    # Correlations across both regions, both waves
    for region in ("ww", "us"):
        rname = "worldwide" if region == "ww" else "US"
        for wave in ("t1", "t2"):
            r = correlations(df_cat, region, wave)
            cat_results["correlations"][f"{region}_{wave}"] = r
            if r["spearman_rho"] is None:
                print(f"  {rname} {wave}: n={r['n']} (insufficient)")
            else:
                print(f"  {rname} {wave}: n={r['n']}  ρ={r['spearman_rho']:.3f}  "
                      f"p1t={r['spearman_p_one_tailed']:.4f}  "
                      f"r={r['pearson_r']:.3f}  partial_ρ={r['partial_spearman_rho']:.3f}")
    print()

    if not descriptive_only:
        # H1, H2, H4 on Worldwide primary
        h1 = eval_h1_or_h4(cat_results["correlations"]["ww_t1"],
                           cat_results["correlations"]["ww_t2"],
                           H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                           "spearman_rho", "spearman_p_one_tailed", "rho")
        h2 = eval_h2(cat_results["correlations"]["ww_t1"],
                     cat_results["correlations"]["ww_t2"])
        h3 = eval_h3(df_cat, "ww")
        h4 = eval_h1_or_h4(cat_results["correlations"]["ww_t1"],
                           cat_results["correlations"]["ww_t2"],
                           H4_RHO_THRESHOLD, H4_P_THRESHOLD,
                           "partial_spearman_rho", "partial_spearman_p_one_tailed",
                           "partial_rho")
        h1_us = eval_h1_or_h4(cat_results["correlations"]["us_t1"],
                              cat_results["correlations"]["us_t2"],
                              H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                              "spearman_rho", "spearman_p_one_tailed", "rho")
        h1_pearson = eval_h1_or_h4(cat_results["correlations"]["ww_t1"],
                                   cat_results["correlations"]["ww_t2"],
                                   H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                                   "pearson_r", "pearson_p_one_tailed", "r")

        cat_results["hypotheses"] = {
            "H1_primary": h1, "H2": h2, "H3": h3, "H4": h4,
            "H1_us_sensitivity": h1_us, "H1_pearson_sensitivity": h1_pearson,
        }

        # H6 diagnostic detection
        cat_results["h6_diagnostics"] = detect_h6_diagnostics(df_cat, "ww")

        # Running-specific sensitivity: raw-strict E1b (exclude raw-floor brands)
        if cat == "running":
            r_t1 = correlations(df_cat, "ww", "t1", raw_strict=True)
            r_t2 = correlations(df_cat, "ww", "t2", raw_strict=True)
            h1_raw_strict = eval_h1_or_h4(r_t1, r_t2, H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                                          "spearman_rho", "spearman_p_one_tailed", "rho")
            cat_results["hypotheses"]["H1_raw_strict_sensitivity"] = h1_raw_strict
            cat_results["correlations"]["ww_t1_raw_strict"] = r_t1
            cat_results["correlations"]["ww_t2_raw_strict"] = r_t2

        print(f"H1: {h1['status']}  ({h1['rationale']})")
        print(f"H2: {h2['status']}  ({h2['rationale']})")
        print(f"H3: {h3['status']}")
        for wave in ("t1", "t2"):
            pw = h3["per_wave"][wave]
            print(f"   {wave}: top3 AI={pw['top3_ai']} → in top5 Trends: {pw['n_in_top5']}/3")
        print(f"H4: {h4['status']}  ({h4['rationale']})")
        print(f"H6 diagnostics: {cat_results['h6_diagnostics']['h6a_status']}")
        for wave in ("t1", "t2"):
            pw = cat_results["h6_diagnostics"]["per_wave"][wave]
            print(f"   {wave}: Linear-style={pw['linear_style']}; Todoist-style={pw['todoist_style']}")
        print()
        print(f"Sensitivities:")
        print(f"  H1 US-only:    {h1_us['status']}  ({h1_us.get('rationale', '')[:200]})")
        print(f"  H1 Pearson:    {h1_pearson['status']}  ({h1_pearson.get('rationale', '')[:200]})")
        if cat == "running":
            print(f"  H1 raw-strict: {h1_raw_strict['status']}  (n_t1={r_t1['n']}, n_t2={r_t2['n']}; "
                  f"excludes raw-floor-constant brands)")
            if h1_raw_strict.get('rationale'):
                print(f"                 ({h1_raw_strict['rationale'][:200]})")
        print()
    else:
        print(f"  (descriptive-only category — H1-H4 indeterminate per §3.4a)")
        print()

    all_results[cat] = cat_results

# ============================================================================
# Step 8: H5 cross-category integrator (effective 2-of-2)
# ============================================================================

def v11_signature_per_category(cat_results):
    """v0.11 signature: ρ<0.5 AND p<0.05 AND H3 falsified, at both waves."""
    if cat_results["descriptive_only"]:
        return {"applicable": False, "reason": "descriptive-only"}
    h1 = cat_results["hypotheses"]["H1_primary"]
    h3 = cat_results["hypotheses"]["H3"]
    if h1["status"] == "INDETERMINATE":
        return {"applicable": False, "reason": "H1 indeterminate"}
    rt1, rt2 = h1["rho_t1"], h1["rho_t2"]
    pt1, pt2 = h1["p_t1_one_tailed"], h1["p_t2_one_tailed"]
    sig_t1 = (rt1 is not None) and rt1 < 0.5 and pt1 < 0.05
    sig_t2 = (rt2 is not None) and rt2 < 0.5 and pt2 < 0.05
    h3_falsified_both = (h3["status_per_wave"]["t1"] == "FALSIFIED" and
                         h3["status_per_wave"]["t2"] == "FALSIFIED")
    full_signature = sig_t1 and sig_t2 and h3_falsified_both
    return {
        "applicable": True,
        "signature_present": full_signature,
        "components": {
            "rho_t1_under_0.5": (rt1 is not None) and rt1 < 0.5,
            "rho_t2_under_0.5": (rt2 is not None) and rt2 < 0.5,
            "p_t1_under_0.05": (pt1 is not None) and pt1 < 0.05,
            "p_t2_under_0.05": (pt2 is not None) and pt2 < 0.05,
            "h3_falsified_both": h3_falsified_both,
        },
    }


def eval_h5(per_cat_sig):
    applicable_cats = [c for c, s in per_cat_sig.items() if s["applicable"]]
    confirmed_cats = [c for c in applicable_cats if per_cat_sig[c]["signature_present"]]
    n_apply = len(applicable_cats)
    n_confirm = len(confirmed_cats)
    if n_apply == 0:
        return {"status": "INDETERMINATE", "rationale": "All categories descriptive-only"}
    if n_apply == 1:
        # Cannot evaluate cross-category generalisation with only 1 applicable category
        return {
            "status": "INDETERMINATE",
            "applicable_categories": applicable_cats,
            "confirmed_categories": confirmed_cats,
            "rationale": (f"Only {n_apply} of 3 categories evaluable for H5 — "
                          f"cross-category generalisation undefined with single category. "
                          f"Single-category signature presence: "
                          f"{applicable_cats[0]}={per_cat_sig[applicable_cats[0]]['signature_present']}"),
        }
    # Effective threshold: 2 of n_apply applicable categories must show signature
    # (with n_apply=2 this becomes the 2-of-2 effective rule per pre-reg §2.2 lock)
    required = 2
    confirmed = (n_confirm >= required)
    return {
        "status": "CONFIRMED" if confirmed else "FALSIFIED",
        "applicable_categories": applicable_cats,
        "confirmed_categories": confirmed_cats,
        "rationale": (f"{n_confirm} of {n_apply} applicable categories show v0.11 signature "
                      f"({required}-of-{n_apply} required)"),
    }


def eval_h6(all_results):
    applicable_cats = [c for c, r in all_results.items() if not r["descriptive_only"]]
    confirmed_cats = [c for c in applicable_cats
                      if all_results[c]["h6_diagnostics"]["h6a_status"] == "CONFIRMED"]
    n_apply = len(applicable_cats)
    n_confirm = len(confirmed_cats)
    confirmed = (n_confirm >= 2)
    return {
        "status": "CONFIRMED" if confirmed else "FALSIFIED",
        "applicable_categories": applicable_cats,
        "confirmed_categories": confirmed_cats,
        "rationale": (f"{n_confirm} of {n_apply} applicable categories confirm H6a "
                      f"(2-of-{n_apply} required)"),
    }


per_cat_sig = {c: v11_signature_per_category(all_results[c]) for c in CATEGORIES}
h5 = eval_h5(per_cat_sig)
h6 = eval_h6(all_results)

print("=" * 80)
print("CROSS-CATEGORY HYPOTHESES")
print("=" * 80)
print(f"H5 (v0.11 signature generalisation): {h5['status']}")
print(f"   {h5['rationale']}")
print(f"   Per-category signature presence:")
for cat, sig in per_cat_sig.items():
    if sig["applicable"]:
        print(f"     {cat}: signature_present={sig['signature_present']}")
    else:
        print(f"     {cat}: {sig['reason']}")
print()
print(f"H6 (Linear-style + Todoist-style cross-category): {h6['status']}")
print(f"   {h6['rationale']}")
print()

# ============================================================================
# Step 9: Category-Scale Mismatch table for olive oil
# ============================================================================

mismatch_rows = []
# Matched-subset olive oil brands (per pre-reg §10.2 — denominator for scale-mismatch index)
# Sourced from matched_subset_v0.12.json: 15 brands incl. pivot + 7 E1a + 7 PASS/PASS_E5
OLIVEOIL_MATCHED_SUBSET = {
    "California Olive Ranch", "Bertolli", "Cobram Estate",
    "Brightland", "Castillo de Canena", "Frantoio Muraglia",
    "Frescobaldi Laudemio", "Graza", "Kosterina", "Lucini",
    "Manni", "McEvoy Ranch", "Núñez de Prado", "Olio Verde", "Colonna",
}

for _, row in paired_all[paired_all["category"] == "oliveoil"].iterrows():
    brand = row["brand"]
    if brand not in OLIVEOIL_MATCHED_SUBSET:
        continue  # Skip registry brands not in v0.9 matched subset (per pre-reg §10.2)
    ai_t1 = row["ai_t1_pct"]
    ai_t2 = row["ai_t2_pct"]
    e1a = row["e1a_excluded"]
    is_pivot = row["is_pivot"]
    sparse_t1 = row.get("trends_ww_t1_sparse", False)
    sparse_t2 = row.get("trends_ww_t2_sparse", False)

    if e1a:
        disposition = "EXCLUDED_E1a"
        trends_t1_str = "below display threshold"
        trends_t2_str = "below display threshold"
        scale_mismatch = (max(ai_t1, ai_t2) >= SCALE_MISMATCH_AI_MIN)
    elif sparse_t1 or sparse_t2:
        disposition = "PASS_E5"
        t1m = row.get("trends_ww_t1_mean")
        t2m = row.get("trends_ww_t2_mean")
        trends_t1_str = f"{t1m:.2f}" if t1m is not None else "—"
        trends_t2_str = f"{t2m:.2f}" if t2m is not None else "—"
        scale_mismatch = False
    else:
        disposition = "PASS"
        t1m = row.get("trends_ww_t1_mean")
        t2m = row.get("trends_ww_t2_mean")
        trends_t1_str = f"{t1m:.2f}" if t1m is not None else "—"
        trends_t2_str = f"{t2m:.2f}" if t2m is not None else "—"
        scale_mismatch = False

    mismatch_rows.append({
        "brand": brand,
        "market_tier": row["market_tier"],
        "is_pivot": is_pivot,
        "phase_b_disposition": disposition,
        "ai_presence_t1_pct": ai_t1,
        "ai_presence_t2_pct": ai_t2,
        "trends_ww_t1_rescaled": trends_t1_str,
        "trends_ww_t2_rescaled": trends_t2_str,
        "scale_mismatch_case": scale_mismatch,
    })

mismatch_df = pd.DataFrame(mismatch_rows)
mismatch_path = OUT_DIR / "category_scale_mismatch_table.csv"
mismatch_df.to_csv(mismatch_path, index=False)

print("=" * 80)
print("CATEGORY-SCALE MISMATCH FINDING — OLIVE OIL")
print("=" * 80)
print(f"{'Brand':<26} {'Tier':<12} {'Disp':<14} {'AI t1':>7} {'AI t2':>7} "
      f"{'Tr_t1':>22} {'Tr_t2':>22} {'SM':>3}")
print("-" * 130)
for r in sorted(mismatch_rows, key=lambda x: -x["ai_presence_t1_pct"]):
    print(f"{r['brand']:<26} {r['market_tier']:<12} {r['phase_b_disposition']:<14} "
          f"{r['ai_presence_t1_pct']:>6.1f}% {r['ai_presence_t2_pct']:>6.1f}% "
          f"{r['trends_ww_t1_rescaled']:>22} {r['trends_ww_t2_rescaled']:>22} "
          f"{'Y' if r['scale_mismatch_case'] else '':>3}")

n_scale_mismatch = sum(1 for r in mismatch_rows if r["scale_mismatch_case"])
n_total = len(mismatch_rows)
print()
print(f"Scale-mismatch index for olive oil: {n_scale_mismatch}/{n_total} = "
      f"{100*n_scale_mismatch/n_total:.1f}%")
print(f"(brand has AI Presence ≥ {SCALE_MISMATCH_AI_MIN}% AND Trends below display threshold)")
print()

# ============================================================================
# Step 10: Pooled sensitivity ρ (stacked rank-within-category)
# ============================================================================

print("=" * 80)
print("POOLED SENSITIVITY ρ (rank-within-category, stacked across PM + running)")
print("=" * 80)

pooled_rows = {"t1": [], "t2": []}
for cat in ["pmsoftware", "running"]:  # exclude olive oil (descriptive-only)
    cat_df = paired_all[(paired_all["category"] == cat) & (~paired_all["e1a_excluded"])].copy()
    for wave in ("t1", "t2"):
        elig = cat_df[cat_df[f"trends_ww_{wave}_eligible"]].copy()
        elig = elig.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"])
        if len(elig) > 1:
            elig[f"ai_rank"] = stats.rankdata(elig[f"ai_{wave}_pct"])
            elig[f"trends_rank"] = stats.rankdata(elig[f"trends_ww_{wave}_mean"])
            for _, row in elig.iterrows():
                pooled_rows[wave].append({
                    "category": cat,
                    "brand": row["brand"],
                    "ai_rank": row["ai_rank"],
                    "trends_rank": row["trends_rank"],
                })

pooled_results = {}
for wave in ("t1", "t2"):
    if len(pooled_rows[wave]) > 4:
        ai_ranks = np.array([r["ai_rank"] for r in pooled_rows[wave]])
        tr_ranks = np.array([r["trends_rank"] for r in pooled_rows[wave]])
        rho, p = stats.spearmanr(ai_ranks, tr_ranks)
        pooled_results[wave] = {"n": len(pooled_rows[wave]), "rho": float(rho), "p_two_tailed": float(p)}
        print(f"  {wave}: n={len(pooled_rows[wave])}  pooled ρ={rho:.3f}  p={p:.4f}")
    else:
        pooled_results[wave] = {"n": len(pooled_rows[wave]), "rho": None, "p_two_tailed": None}

print()

# ============================================================================
# Step 11: Write canonical scoring outputs
# ============================================================================

canonical = {
    "meta": {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "v0_12_prereg_tag": "v0.12-prereg",
        "matched_models": sorted(MATCHED_MODELS),
        "n_responses_per_category_per_wave": n_responses,
        "e1a_exclusions": {cat: sorted(brands) for cat, brands in e1a_by_cat.items()},
    },
    "per_category": all_results,
    "cross_category": {"H5": h5, "H6": h6, "per_category_signature": per_cat_sig},
    "pooled_sensitivity": pooled_results,
    "category_scale_mismatch_olive_oil": {
        "n_scale_mismatch": n_scale_mismatch,
        "n_total": n_total,
        "scale_mismatch_index_pct": round(100 * n_scale_mismatch / n_total, 1),
        "table_path": str(mismatch_path.relative_to(V12_ROOT)),
    },
}

(OUT_DIR / "canonical_scoring.json").write_text(
    json.dumps(canonical, indent=2, default=str))
print(f"Canonical scoring (JSON): {OUT_DIR / 'canonical_scoring.json'}")

# Flat CSV for quick reading
with (OUT_DIR / "canonical_scoring.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["scope", "hypothesis", "status", "rationale"])
    w.writeheader()
    for cat in CATEGORIES:
        cat_res = all_results[cat]
        if cat_res["descriptive_only"]:
            w.writerow({"scope": cat, "hypothesis": "H1-H4",
                        "status": "INDETERMINATE",
                        "rationale": "Descriptive-only per pre-reg §3.4a (n-floor breached)"})
        else:
            for hn, hd in cat_res["hypotheses"].items():
                w.writerow({"scope": cat, "hypothesis": hn,
                            "status": hd.get("status"),
                            "rationale": str(hd.get("rationale", ""))[:300]})
    w.writerow({"scope": "cross_category", "hypothesis": "H5",
                "status": h5["status"], "rationale": h5["rationale"]})
    w.writerow({"scope": "cross_category", "hypothesis": "H6",
                "status": h6["status"], "rationale": h6["rationale"]})

print(f"Canonical scoring (CSV):  {OUT_DIR / 'canonical_scoring.csv'}")
print(f"Category-Scale Mismatch table: {mismatch_path}")
print()
print("Scoring complete. Next: chart builds and SSRN paper draft.")
