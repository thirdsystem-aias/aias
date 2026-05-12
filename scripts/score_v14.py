"""v0.14 Hypothesis evaluation for premium tea (single category).

Focused port of score_v13.py. Strips cross-category logic (H5/H6/H8) since
v0.14 is single-category by design. Adds H_Regime4_replication evaluator
and Tea Box-excluded sensitivity analysis.

v0.14 vs v0.13 differences:
  - Single category: premium tea only (no reuse arm, no cross-category H5/H6/H8)
  - Wave split: one acquisition split by run_idx (1-4 t1, 5-8 t2) rather than
    two separate enriched files
  - Premium-tier covariate: {luxury, mainstream-premium, specialty} ordinal
    encoding instead of v0.13's {incumbent, mid-tier, challenger}
  - H_Regime4_replication (new): three-condition test for Regime 4 fit
  - Tea Box sensitivity (new): primary panel n=16 plus n=15 (Tea Box excluded
    for query-phrase-ambiguity flagged at rescale stage)

Inputs:
  - data/premium_tea/results_enriched_premium_tea_*.csv  (LLM enrichment)
  - osf/v14/data/trends_processed/per_brand_within_window.csv  (Trends)
  - osf/v14/registries/topic_id_resolution_log_v0.14.csv  (Phase B E1a)
  - osf/v14/registries/brand_age_sources_v0.14_verified.csv  (age + tier)
  - osf/v14/registries/brands_premium_tea.json  (registry, v3 schema)

Outputs:
  - osf/v14/analysis/per_brand_paired.csv
  - osf/v14/analysis/canonical_scoring.csv
  - osf/v14/analysis/canonical_scoring.json
  - osf/v14/analysis/h7_regime_classification.csv
  - osf/v14/analysis/h_regime4_replication.csv  (primary + Tea Box-excluded)

Run from ~/aias/:
    python3 ~/aias/scripts/score_v14.py
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
# Configuration (locked at v0.14-prereg)
# ============================================================================

HOME = Path.home()
V14_ROOT = HOME / "aias" / "osf" / "v14"

TRENDS_PROC = V14_ROOT / "data" / "trends_processed" / "per_brand_within_window.csv"
PHASEB_LOG  = V14_ROOT / "registries" / "topic_id_resolution_log_v0.14.csv"
AGE_FILE    = V14_ROOT / "registries" / "brand_age_sources_v0.14_verified.csv"
REGISTRY    = V14_ROOT / "registries" / "brands_premium_tea.json"

OUT_DIR = V14_ROOT / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MATCHED_MODELS = {"claude-sonnet-4-6", "gpt-5.4-mini"}
CATEGORY = "premium_tea"
PIVOT = "Twinings"

# Wave split (locked per v0.14 design — single acquisition split by run_idx)
T1_RUN_IDX = {1, 2, 3, 4}
T2_RUN_IDX = {5, 6, 7, 8}

# Premium-tier ordinal encoding (luxury > mainstream-premium > specialty)
PREMIUM_TIER_ORDINAL = {
    "luxury": 3,
    "mainstream-premium": 2,
    "specialty": 1,
}

# H1-H4 thresholds (inherited from v0.13)
H1_RHO_THRESHOLD = 0.5
H1_P_THRESHOLD   = 0.05
H2_DELTA_THRESHOLD = 0.15
H3_TOP_K_AI     = 3
H3_TOP_K_TRENDS = 5
H4_RHO_THRESHOLD = 0.5
H4_P_THRESHOLD   = 0.05

N_FLOOR_HARD  = 10
N_FLOOR_ALIGN = 12

# H7 regime thresholds (inherited from v0.13)
H7_R1_RHO_MIN        = 0.35
H7_R1_RHO_MAX        = 0.65
H7_R1_DECREMENT_MAX  = 0.15
H7_R2_RHO_MIN        = 0.65
H7_R2_DECREMENT_MIN  = 0.25
H7_BOUNDARY_TOLERANCE = 0.05

# H_Regime4_replication thresholds (v0.14-specific)
HR4_N_FLOOR     = 12
HR4_RHO_MAX     = 0.35
HR4_PARTIAL_MAX = 0.0  # partial must be < 0


# ============================================================================
# Step 1: Load E1a exclusions from Phase B log
# ============================================================================

e1a_excluded = set()
tested_not_activated = set()
phase_b = pd.read_csv(PHASEB_LOG)
for _, row in phase_b.iterrows():
    notes = str(row.get("notes", "") or "")
    if row["final_query_tier"] == "EXCLUDED_E1a":
        e1a_excluded.add(row["brand_canonical"])
    elif "TESTED_NOT_ACTIVATED" in notes:
        tested_not_activated.add(row["brand_canonical"])

print(f"E1a-excluded brands: {len(e1a_excluded)}: {sorted(e1a_excluded)}")
print(f"Tested-not-activated alternates: {len(tested_not_activated)}: "
      f"{sorted(tested_not_activated)}")
print()


# ============================================================================
# Step 2: Load brand registry
# ============================================================================

with REGISTRY.open() as f:
    registry_raw = json.load(f)
brands_list = registry_raw["brands"] if isinstance(registry_raw, dict) else registry_raw
canonical_brands = [b["canonical"] for b in brands_list]
print(f"Registry: {len(canonical_brands)} brands (registry_version="
      f"{registry_raw.get('registry_version', 'unknown')})")


# ============================================================================
# Step 3: Compute AI Presence per wave
# ============================================================================

def compute_presence_split(enriched_path, registry_brands, t1_runs, t2_runs):
    """Compute AI Presence per brand per wave, splitting one CSV by run_idx.

    Returns: (presence_t1, presence_t2, n_t1, n_t2)
    """
    df = pd.read_csv(enriched_path)
    df = df[df["model_version"].isin(MATCHED_MODELS)]
    df = df[df["call_status"] == "ok"]
    df["run_idx"] = df["run_idx"].astype(int)

    df_t1 = df[df["run_idx"].isin(t1_runs)]
    df_t2 = df[df["run_idx"].isin(t2_runs)]
    n_t1 = len(df_t1)
    n_t2 = len(df_t2)

    def compute_one_wave(d):
        n = len(d)
        out = {}
        for b in registry_brands:
            def hit(s):
                if pd.isna(s):
                    return False
                return b in str(s).split("|")
            c = int(d["brands_canonical"].apply(hit).sum())
            out[b] = round(100.0 * c / n, 2) if n else 0.0
        return out

    return compute_one_wave(df_t1), compute_one_wave(df_t2), n_t1, n_t2


# Find most recent enriched CSV
enriched_candidates = sorted(
    Path("data/premium_tea").glob(f"results_enriched_{CATEGORY}_*.csv")
)
if not enriched_candidates:
    raise FileNotFoundError(
        "No results_enriched_premium_tea_*.csv found at data/premium_tea/. "
        "Run enrich.py first."
    )
enriched_path = enriched_candidates[-1]
print(f"Enriched CSV: {enriched_path.name}")

ai_t1, ai_t2, n_t1, n_t2 = compute_presence_split(
    enriched_path, canonical_brands, T1_RUN_IDX, T2_RUN_IDX
)
print(f"AI Presence computed: n_t1={n_t1} rows (run_idx ∈ {sorted(T1_RUN_IDX)}), "
      f"n_t2={n_t2} rows (run_idx ∈ {sorted(T2_RUN_IDX)})")
print()


# ============================================================================
# Step 4: Load Trends + ages, build paired dataset
# ============================================================================

trends_df = pd.read_csv(TRENDS_PROC)
trends_ww = trends_df[trends_df["region"] == "worldwide"].set_index("brand")
trends_us = trends_df[trends_df["region"] == "US"].set_index("brand")

age_df = pd.read_csv(AGE_FILE)
age_year_map = dict(zip(age_df["brand"], age_df["founding_year"]))
tier_map = dict(zip(age_df["brand"], age_df["premium_tier"]))


def brand_age_years(brand):
    year = age_year_map.get(brand)
    if pd.isna(year) or year is None:
        return None
    return 2026 - int(year)


records = []
for b in canonical_brands:
    rec = {
        "brand": b,
        "category": CATEGORY,
        "premium_tier": tier_map.get(b, ""),
        "tier_ordinal": PREMIUM_TIER_ORDINAL.get(tier_map.get(b, ""), None),
        "founding_year": age_year_map.get(b),
        "brand_age_years": brand_age_years(b),
        "ai_t1_pct": ai_t1.get(b, 0.0),
        "ai_t2_pct": ai_t2.get(b, 0.0),
        "e1a_excluded": b in e1a_excluded,
        "tested_not_activated": b in tested_not_activated,
        "is_pivot": b == PIVOT,
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
    # Pivot exemption: Twinings rescales to 100.0 every day → sd=0 → E1b=False
    # by construction; treat as eligible regardless.
    if b == PIVOT:
        for label in ("ww", "us"):
            for w in ("t1", "t2"):
                rec[f"trends_{label}_{w}_eligible"] = True
    records.append(rec)

paired = pd.DataFrame(records)
paired_path = OUT_DIR / "per_brand_paired.csv"
paired.to_csv(paired_path, index=False)
print(f"Paired dataset: {paired_path} ({len(paired)} rows)")
print()


# ============================================================================
# Step 5: Correlation function (port from v0.13, premium_tier covariate)
# ============================================================================

def correlations(df, region, wave, exclude_brands=None):
    """Compute correlations for one (region, wave) slice.

    Filters by trends eligibility (E1b) + Phase B E1a + optional exclusion list.
    Returns dict with spearman_rho, pearson_r, partial_spearman_rho (controlling
    for age + premium_tier_ordinal), plus AI~age bivariate (for pre-reg condition
    2 transparency).
    """
    exclude_brands = exclude_brands or set()
    elig_col = f"trends_{region}_{wave}_eligible"
    elig = df[df[elig_col]].copy()
    elig = elig[~elig["e1a_excluded"]]
    elig = elig[~elig["tested_not_activated"]]
    elig = elig[~elig["brand"].isin(exclude_brands)]
    elig = elig.dropna(subset=[
        f"trends_{region}_{wave}_mean", f"ai_{wave}_pct",
        "brand_age_years", "tier_ordinal",
    ])
    n = len(elig)
    out = {"n": n, "brands": list(elig["brand"])}
    if n < 4:
        for k in ("spearman_rho", "spearman_p_two_tailed", "spearman_p_one_tailed",
                  "pearson_r", "pearson_p_two_tailed",
                  "partial_spearman_rho", "partial_spearman_p_one_tailed",
                  "ai_age_rho", "ai_age_p_two_tailed"):
            out[k] = None
        return out

    x = elig[f"ai_{wave}_pct"].values.astype(float)
    y = elig[f"trends_{region}_{wave}_mean"].values.astype(float)
    z1 = elig["brand_age_years"].values.astype(float)
    z2 = elig["tier_ordinal"].values.astype(float)

    # Bivariate AI vs Trends (v0.13-canonical)
    rho, p_rho = stats.spearmanr(x, y)
    p_rho_1t = float(p_rho / 2) if rho > 0 else float(1 - p_rho / 2)
    r, p_r = stats.pearsonr(x, y)

    # Bivariate AI vs brand age (pre-reg condition 2 literal reading)
    rho_age, p_age = stats.spearmanr(x, z1)

    # Partial Spearman: AI vs Trends, controlling for age + premium_tier_ordinal
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
        "partial_spearman_rho": float(pr),
        "partial_spearman_p_one_tailed": partial_p_1t,
        "ai_age_rho": float(rho_age),
        "ai_age_p_two_tailed": float(p_age),
    })
    return out


# ============================================================================
# Step 6: H1-H4 evaluators (port from v0.13)
# ============================================================================

def eval_h1_or_h4(t1, t2, thr_rho, thr_p, key_rho, key_p, label):
    if t1["n"] < N_FLOOR_HARD or t2["n"] < N_FLOOR_HARD:
        return {
            "status": "INDETERMINATE",
            "rationale": f"n-floor breached: t1 n={t1['n']}, t2 n={t2['n']} "
                         f"(hard floor={N_FLOOR_HARD})",
        }
    rt1, rt2 = t1[key_rho], t2[key_rho]
    pt1, pt2 = t1[key_p], t2[key_p]
    pass1 = (rt1 is not None) and rt1 > thr_rho and pt1 < thr_p
    pass2 = (rt2 is not None) and rt2 > thr_rho and pt2 < thr_p
    status = "CONFIRMED" if (pass1 and pass2) else "FALSIFIED"
    return {
        "status": status,
        "threshold_rho": thr_rho, "threshold_p": thr_p,
        f"{label}_t1": rt1, f"{label}_t2": rt2,
        "p_t1": pt1, "p_t2": pt2,
        "rationale": f"t1: ρ={rt1:.3f}, p1t={pt1:.4f}. t2: ρ={rt2:.3f}, p1t={pt2:.4f}.",
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
        "rationale": f"|Δρ| = {delta:.3f} {'≤' if delta <= H2_DELTA_THRESHOLD else '>'} "
                     f"{H2_DELTA_THRESHOLD}",
    }


def eval_h3(df, region):
    out = {"per_wave": {}, "status_per_wave": {}}
    pass_both = True
    for wave in ("t1", "t2"):
        e = df[df[f"trends_{region}_{wave}_eligible"] & (~df["e1a_excluded"])
               & (~df["tested_not_activated"])].copy()
        e = e.dropna(subset=[f"trends_{region}_{wave}_mean", f"ai_{wave}_pct"])
        top3_ai = list(e.sort_values(f"ai_{wave}_pct", ascending=False)
                        .head(H3_TOP_K_AI)["brand"])
        top5_t  = list(e.sort_values(f"trends_{region}_{wave}_mean", ascending=False)
                        .head(H3_TOP_K_TRENDS)["brand"])
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


# ============================================================================
# Step 7: H7 regime classifier (port from v0.13)
# ============================================================================

def h7_classify(corr_t1, corr_t2):
    bivar_t1 = corr_t1.get("spearman_rho")
    bivar_t2 = corr_t2.get("spearman_rho")
    partial_t1 = corr_t1.get("partial_spearman_rho")
    partial_t2 = corr_t2.get("partial_spearman_rho")
    n_t1 = corr_t1.get("n", 0)
    n_t2 = corr_t2.get("n", 0)

    if any(v is None for v in (bivar_t1, bivar_t2, partial_t1, partial_t2)):
        return {
            "regime_class": "Unclassifiable (insufficient n)",
            "boundary_flag": False,
            "unclassifiable_flag": True,
            "rationale": f"n_t1={n_t1}, n_t2={n_t2}; cannot compute ρ.",
            "bivariate_rho_t1": bivar_t1, "bivariate_rho_t2": bivar_t2,
            "partial_rho_t1": partial_t1, "partial_rho_t2": partial_t2,
            "decrement_t1": None, "decrement_t2": None,
            "n_eligible_t1": n_t1, "n_eligible_t2": n_t2,
        }

    decrement_t1 = bivar_t1 - partial_t1
    decrement_t2 = bivar_t2 - partial_t2

    is_regime_1 = (
        H7_R1_RHO_MIN <= bivar_t1 <= H7_R1_RHO_MAX and
        H7_R1_RHO_MIN <= bivar_t2 <= H7_R1_RHO_MAX and
        decrement_t1 <= H7_R1_DECREMENT_MAX and
        decrement_t2 <= H7_R1_DECREMENT_MAX and
        n_t1 >= N_FLOOR_HARD and n_t2 >= N_FLOOR_HARD
    )
    is_regime_2 = (
        bivar_t1 > H7_R2_RHO_MIN and bivar_t2 > H7_R2_RHO_MIN and
        decrement_t1 > H7_R2_DECREMENT_MIN and decrement_t2 > H7_R2_DECREMENT_MIN and
        n_t1 >= N_FLOOR_HARD and n_t2 >= N_FLOOR_HARD
    )

    tol = H7_BOUNDARY_TOLERANCE
    boundary_flag = any(
        abs(b - t) <= tol
        for b in (bivar_t1, bivar_t2)
        for t in (H7_R1_RHO_MIN, H7_R1_RHO_MAX, H7_R2_RHO_MIN)
    ) or any(
        abs(d - t) <= tol
        for d in (decrement_t1, decrement_t2)
        for t in (H7_R1_DECREMENT_MAX, H7_R2_DECREMENT_MIN)
    )

    if is_regime_1 and is_regime_2:
        regime = "Unclassifiable (matches Regimes 1 and 2)"
        unclass = True
    elif is_regime_1:
        regime = "Regime 1 (Marginal direct)"
        unclass = False
    elif is_regime_2:
        regime = "Regime 2 (Age-mediated strong)"
        unclass = False
    else:
        regime = "Regime 4 candidate (matches neither Regime 1 nor 2)"
        unclass = True  # in v0.14 framing, this IS the Regime 4 signature

    return {
        "regime_class": regime,
        "boundary_flag": boundary_flag,
        "unclassifiable_flag": unclass,
        "rationale": (f"ρ_t1={bivar_t1:.3f}, ρ_t2={bivar_t2:.3f}, "
                      f"partial_ρ_t1={partial_t1:.3f}, partial_ρ_t2={partial_t2:.3f}, "
                      f"Δ_t1={decrement_t1:.3f}, Δ_t2={decrement_t2:.3f}, "
                      f"n_t1={n_t1}, n_t2={n_t2}."),
        "bivariate_rho_t1": bivar_t1, "bivariate_rho_t2": bivar_t2,
        "partial_rho_t1": partial_t1, "partial_rho_t2": partial_t2,
        "decrement_t1": decrement_t1, "decrement_t2": decrement_t2,
        "n_eligible_t1": n_t1, "n_eligible_t2": n_t2,
    }


# ============================================================================
# Step 8: H_Regime4_replication evaluator (v0.14-specific)
# ============================================================================

def eval_h_regime4_replication(corr_t1, corr_t2, label="primary"):
    """Three-condition test for Regime 4 fit.

    Condition 1: n_eligible >= HR4_N_FLOOR at BOTH waves
    Condition 2 (v0.13-canonical): |bivariate ρ(AI, Trends)| < HR4_RHO_MAX at both waves
    Condition 2_age (pre-reg literal): |ρ(AI, brand age)| < HR4_RHO_MAX at both waves
    Condition 3: partial ρ(AI, Trends | age, premium_tier) < HR4_PARTIAL_MAX at both waves

    Primary determination uses Condition 2 (v0.13-canonical) for consistency with
    the named Regime 4 cases (skincare, finance) under the broader programme.
    The AI~age version is reported in parallel for transparency to the pre-reg's
    condition 2 wording.
    """
    n_t1 = corr_t1.get("n", 0)
    n_t2 = corr_t2.get("n", 0)
    cond1 = n_t1 >= HR4_N_FLOOR and n_t2 >= HR4_N_FLOOR

    bivar_t1 = corr_t1.get("spearman_rho")
    bivar_t2 = corr_t2.get("spearman_rho")
    partial_t1 = corr_t1.get("partial_spearman_rho")
    partial_t2 = corr_t2.get("partial_spearman_rho")
    ai_age_t1 = corr_t1.get("ai_age_rho")
    ai_age_t2 = corr_t2.get("ai_age_rho")

    if any(v is None for v in (bivar_t1, bivar_t2, partial_t1, partial_t2,
                                ai_age_t1, ai_age_t2)):
        return {
            "label": label,
            "status": "INDETERMINATE",
            "rationale": "Insufficient n; cannot compute correlations.",
            "n_t1": n_t1, "n_t2": n_t2,
        }

    cond2_trends = abs(bivar_t1) < HR4_RHO_MAX and abs(bivar_t2) < HR4_RHO_MAX
    cond2_age    = abs(ai_age_t1) < HR4_RHO_MAX and abs(ai_age_t2) < HR4_RHO_MAX
    cond3 = partial_t1 < HR4_PARTIAL_MAX and partial_t2 < HR4_PARTIAL_MAX

    # Primary determination per v0.13 framework
    primary_status = "CONFIRMED" if (cond1 and cond2_trends and cond3) else "FALSIFIED"

    # AI~age version for transparency
    age_version_status = "CONFIRMED" if (cond1 and cond2_age and cond3) else "FALSIFIED"

    return {
        "label": label,
        "status": primary_status,
        "status_age_version": age_version_status,
        "condition_1_n_floor": {
            "n_t1": n_t1, "n_t2": n_t2, "threshold": HR4_N_FLOOR, "satisfied": cond1,
        },
        "condition_2_trends": {
            "bivariate_rho_t1": bivar_t1, "bivariate_rho_t2": bivar_t2,
            "threshold": HR4_RHO_MAX, "satisfied": cond2_trends,
            "interpretation": "v0.13-canonical: AI Presence ~ Trends correlation",
        },
        "condition_2_age": {
            "ai_age_rho_t1": ai_age_t1, "ai_age_rho_t2": ai_age_t2,
            "threshold": HR4_RHO_MAX, "satisfied": cond2_age,
            "interpretation": "Pre-reg literal: AI Presence ~ brand age correlation",
        },
        "condition_3_partial": {
            "partial_rho_t1": partial_t1, "partial_rho_t2": partial_t2,
            "threshold": HR4_PARTIAL_MAX, "satisfied": cond3,
            "interpretation": "Partial AI~Trends controlling for age + premium_tier",
        },
        "rationale": (
            f"C1 (n≥{HR4_N_FLOOR} both waves): {cond1} "
            f"(n_t1={n_t1}, n_t2={n_t2}). "
            f"C2_trends (|ρ_AI~Trends|<{HR4_RHO_MAX}): {cond2_trends} "
            f"(t1={bivar_t1:.3f}, t2={bivar_t2:.3f}). "
            f"C2_age (|ρ_AI~age|<{HR4_RHO_MAX}): {cond2_age} "
            f"(t1={ai_age_t1:.3f}, t2={ai_age_t2:.3f}). "
            f"C3 (partial<{HR4_PARTIAL_MAX}): {cond3} "
            f"(t1={partial_t1:.3f}, t2={partial_t2:.3f}). "
            f"Primary status uses C1+C2_trends+C3."
        ),
    }


# ============================================================================
# Step 9: Run evaluation — primary + Tea Box-excluded sensitivity
# ============================================================================

print("=" * 80)
print(f"### PRIMARY ANALYSIS (n_eligible per Phase B + alternates)")
print("=" * 80)

correlations_by_region_wave = {}
for region in ("ww", "us"):
    rname = "worldwide" if region == "ww" else "US"
    for wave in ("t1", "t2"):
        r = correlations(paired, region, wave)
        correlations_by_region_wave[f"{region}_{wave}"] = r
        if r["spearman_rho"] is None:
            print(f"  {rname} {wave}: n={r['n']} (insufficient)")
        else:
            print(f"  {rname} {wave}: n={r['n']}  "
                  f"ρ_AI~Trends={r['spearman_rho']:.3f}  "
                  f"ρ_AI~age={r['ai_age_rho']:.3f}  "
                  f"partial_ρ={r['partial_spearman_rho']:.3f}")
print()

h1 = eval_h1_or_h4(correlations_by_region_wave["ww_t1"],
                   correlations_by_region_wave["ww_t2"],
                   H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                   "spearman_rho", "spearman_p_one_tailed", "rho")
h2 = eval_h2(correlations_by_region_wave["ww_t1"],
             correlations_by_region_wave["ww_t2"])
h3 = eval_h3(paired, "ww")
h4 = eval_h1_or_h4(correlations_by_region_wave["ww_t1"],
                   correlations_by_region_wave["ww_t2"],
                   H4_RHO_THRESHOLD, H4_P_THRESHOLD,
                   "partial_spearman_rho", "partial_spearman_p_one_tailed", "partial_rho")
h1_us = eval_h1_or_h4(correlations_by_region_wave["us_t1"],
                      correlations_by_region_wave["us_t2"],
                      H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                      "spearman_rho", "spearman_p_one_tailed", "rho")

h7 = h7_classify(correlations_by_region_wave["ww_t1"],
                 correlations_by_region_wave["ww_t2"])

hr4_primary = eval_h_regime4_replication(
    correlations_by_region_wave["ww_t1"],
    correlations_by_region_wave["ww_t2"],
    label="primary"
)

print(f"H1 (AI~Trends ρ > 0.5):           {h1['status']}")
print(f"   {h1['rationale']}")
print(f"H2 (|Δρ| ≤ 0.15):                  {h2['status']}")
print(f"   {h2['rationale']}")
print(f"H3 (top-3 AI ⊂ top-5 Trends):     {h3['status']}")
print(f"H4 (partial ρ > 0.5):              {h4['status']}")
print(f"   {h4['rationale']}")
print(f"H1 (US sensitivity):               {h1_us['status']}")
print()
print(f"H7 regime classification:          {h7['regime_class']}")
print(f"   {h7['rationale']}")
if h7["boundary_flag"]:
    print(f"   (boundary flag — within {H7_BOUNDARY_TOLERANCE} of a threshold)")
print()
print(f"H_Regime4_replication (primary, n=16): {hr4_primary['status']}")
print(f"   AI~age version status: {hr4_primary['status_age_version']}")
print(f"   {hr4_primary['rationale']}")
print()

# Tea Box-excluded sensitivity analysis
print("=" * 80)
print(f"### SENSITIVITY: Tea Box-excluded (query-phrase ambiguity flagged at rescale)")
print("=" * 80)

correlations_sensitivity = {}
for region in ("ww", "us"):
    for wave in ("t1", "t2"):
        r = correlations(paired, region, wave, exclude_brands={"Tea Box"})
        correlations_sensitivity[f"{region}_{wave}"] = r
        rname = "worldwide" if region == "ww" else "US"
        if r["spearman_rho"] is not None:
            print(f"  {rname} {wave}: n={r['n']}  "
                  f"ρ_AI~Trends={r['spearman_rho']:.3f}  "
                  f"ρ_AI~age={r['ai_age_rho']:.3f}  "
                  f"partial_ρ={r['partial_spearman_rho']:.3f}")
print()

h7_sens = h7_classify(correlations_sensitivity["ww_t1"],
                      correlations_sensitivity["ww_t2"])
hr4_sens = eval_h_regime4_replication(
    correlations_sensitivity["ww_t1"],
    correlations_sensitivity["ww_t2"],
    label="tea_box_excluded"
)

print(f"H7 regime (Tea Box excluded):      {h7_sens['regime_class']}")
print(f"   {h7_sens['rationale']}")
print(f"H_Regime4_replication (Tea Box excluded, n={correlations_sensitivity['ww_t1']['n']}): "
      f"{hr4_sens['status']}")
print(f"   AI~age version status: {hr4_sens['status_age_version']}")
print()


# ============================================================================
# Step 10: Write outputs
# ============================================================================

# Canonical scoring CSV
with (OUT_DIR / "canonical_scoring.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["scope", "hypothesis", "status", "rationale"])
    w.writeheader()
    rows_to_write = [
        ("premium_tea", "H1_primary",            h1),
        ("premium_tea", "H2",                    h2),
        ("premium_tea", "H3",                    h3),
        ("premium_tea", "H4",                    h4),
        ("premium_tea", "H1_us_sensitivity",     h1_us),
        ("premium_tea", "H7",                    h7),
        ("premium_tea", "H_Regime4_replication_primary", hr4_primary),
        ("premium_tea", "H_Regime4_replication_tea_box_excluded", hr4_sens),
    ]
    for scope, hn, hd in rows_to_write:
        w.writerow({
            "scope": scope, "hypothesis": hn,
            "status": hd.get("status", hd.get("regime_class", "")),
            "rationale": str(hd.get("rationale", ""))[:500],
        })

# H7 classification CSV
h7_rows = [
    {**h7, "panel": "primary", "n_brands": 16},
    {**h7_sens, "panel": "tea_box_excluded", "n_brands": 15},
]
pd.DataFrame(h7_rows).to_csv(OUT_DIR / "h7_regime_classification.csv", index=False)

# H_Regime4_replication CSV
hr4_rows = [hr4_primary, hr4_sens]
pd.DataFrame([{
    "panel": r["label"],
    "status": r["status"],
    "status_age_version": r.get("status_age_version"),
    "n_t1": r["condition_1_n_floor"]["n_t1"] if "condition_1_n_floor" in r else None,
    "n_t2": r["condition_1_n_floor"]["n_t2"] if "condition_1_n_floor" in r else None,
    "bivariate_rho_t1": r.get("condition_2_trends", {}).get("bivariate_rho_t1"),
    "bivariate_rho_t2": r.get("condition_2_trends", {}).get("bivariate_rho_t2"),
    "ai_age_rho_t1": r.get("condition_2_age", {}).get("ai_age_rho_t1"),
    "ai_age_rho_t2": r.get("condition_2_age", {}).get("ai_age_rho_t2"),
    "partial_rho_t1": r.get("condition_3_partial", {}).get("partial_rho_t1"),
    "partial_rho_t2": r.get("condition_3_partial", {}).get("partial_rho_t2"),
    "rationale": r.get("rationale"),
} for r in hr4_rows]).to_csv(OUT_DIR / "h_regime4_replication.csv", index=False)

# Full canonical JSON
canonical = {
    "meta": {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "v0_14_prereg_tag": "v0.14-prereg",
        "matched_models": sorted(MATCHED_MODELS),
        "n_responses_t1": n_t1,
        "n_responses_t2": n_t2,
        "wave_split": {"t1_runs": sorted(T1_RUN_IDX), "t2_runs": sorted(T2_RUN_IDX)},
        "e1a_exclusions": sorted(e1a_excluded),
        "tested_not_activated": sorted(tested_not_activated),
    },
    "primary_analysis": {
        "correlations": correlations_by_region_wave,
        "hypotheses": {
            "H1": h1, "H2": h2, "H3": h3, "H4": h4,
            "H1_us": h1_us, "H7": h7,
            "H_Regime4_replication": hr4_primary,
        },
    },
    "tea_box_excluded_sensitivity": {
        "correlations": correlations_sensitivity,
        "H7": h7_sens,
        "H_Regime4_replication": hr4_sens,
    },
}
(OUT_DIR / "canonical_scoring.json").write_text(
    json.dumps(canonical, indent=2, default=str))

print("=" * 80)
print(f"Outputs:")
print(f"  {paired_path}")
print(f"  {OUT_DIR / 'canonical_scoring.csv'}")
print(f"  {OUT_DIR / 'canonical_scoring.json'}")
print(f"  {OUT_DIR / 'h7_regime_classification.csv'}")
print(f"  {OUT_DIR / 'h_regime4_replication.csv'}")
print()
print("Scoring complete.")
