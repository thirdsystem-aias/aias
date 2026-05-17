"""v0.16 Hypothesis evaluation for kitchen knives.

Port of score_v15.py with the following changes:
  1. Substrate: premium_tea -> kitchen_knives (fresh category)
  2. Registry schema adapter: v0.16 uses panel/alternates with
     display_name/brand_id/tradition_cell (not canonical/tradition)
  3. TRADITION_LEVELS: 6 tea cells -> 5 knives cells
     [japanese, german, french, american_specialty, chinese]
     k_adj = 1 (age) + 4 (dummies; 5 cells − 1 reference) = 5
  4. PIVOT: Twinings -> Victorinox
  5. H_Regime4_robustness -> H_Regime4_replication_knives:
     - Condition operationalization UNCHANGED (Cond 1: n >= 12; Cond 2:
       |rho(AI, Trends)| < 0.35; Cond 3: partial rho < 0). Matches
       v0.15-canonical per AIAS Protocol v1.2 §3.4.
     - Verdict structure refined: v0.15 binary -> v0.16 ternary with
       PARTIAL added as strict sub-classification of v0.15-canonical
       FALSIFIED. Documented in pre-reg §2; not a contradiction with v0.15.
  6. H_Coverage_Closure REMOVED (v0.15-specific; v0.16 is fresh category)
  7. H_Discourse_Language_carryforward ADDED:
     - New evaluator. Per-brand AI Presence stratified by prompt language
       on Japanese tradition cell.
     - Tests v0.8 finding (SSRN 6728000) under v1.2 protocol.
     - Decision rules from pre-reg §2.

Inputs:
  - data/kitchen_knives/results_enriched_kitchen_knives_*.csv  (LLM enrichment)
  - osf/v16/data/trends_processed/per_brand_within_window.csv  (Trends)
  - osf/v16/registries/topic_id_resolution_log_v0.16.csv       (Phase B)
  - osf/v16/registries/brand_age_sources_v0.16.csv             (ages)
  - ~/aias/registries/brands_kitchen_knives_v0.16.json         (registry)

Outputs:
  - osf/v16/analysis/per_brand_paired.csv
  - osf/v16/analysis/canonical_scoring.csv
  - osf/v16/analysis/canonical_scoring.json
  - osf/v16/analysis/h7_regime_classification.csv
  - osf/v16/analysis/h_regime4_replication_knives.csv
  - osf/v16/analysis/h_discourse_language_carryforward.csv

Pre-reg: v0.16-prereg (commit 511e339; corrected per DEVIATIONS Entry 2)
Methodology base: AIAS Presence Measurement Protocol v1.2 (SSRN 6761698)

Run:
    python3 ~/aias/scripts/score_v16.py
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
# Configuration (locked at v0.16-prereg, 511e339)
# ============================================================================

HOME = Path.home()
AIAS_ROOT = HOME / "aias"
V16_ROOT = AIAS_ROOT / "osf" / "v16"

TRENDS_PROC = V16_ROOT / "data" / "trends_processed" / "per_brand_within_window.csv"
PHASEB_LOG  = V16_ROOT / "registries" / "topic_id_resolution_log_v0.16.csv"
AGE_FILE    = V16_ROOT / "registries" / "brand_age_sources_v0.16.csv"
REGISTRY    = AIAS_ROOT / "registries" / "brands_kitchen_knives_v0.16.json"
PROMPTS     = AIAS_ROOT / "prompts" / "prompts_knives_v0.16.json"

OUT_DIR = V16_ROOT / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# LLM panel for canonical scoring — confirm at run time matches Phase B / acquisition
MATCHED_MODELS = {"claude-sonnet-4-6", "gpt-5.4-mini"}

CATEGORY = "kitchen_knives"
PIVOT = "Wüsthof"
CURRENT_YEAR = 2026  # for brand_age_years computation

# Wave split (locked per v0.13 design — single acquisition split by run_idx)
T1_RUN_IDX = {1, 2, 3, 4}
T2_RUN_IDX = {5, 6, 7, 8}

# v0.16 tradition cells (5 cells; k_adj = 1 + 4 = 5)
TRADITION_LEVELS = [
    "japanese", "german", "french", "american_specialty", "chinese",
]

# H1-H4 thresholds (programme-standard, inherited from v0.13)
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

# H_Regime4_replication_knives thresholds (per pre-reg §2; aligns v0.15 canonical)
HR4_N_FLOOR     = 12
HR4_RHO_MAX     = 0.35
HR4_PARTIAL_MAX = 0.0   # partial rho must be < 0 for CONFIRMED

# H_Discourse_Language_carryforward thresholds (per pre-reg §2)
HDL_N_FLOOR_JAPANESE = 5
HDL_RHO_CONFIRMED    = 0.85    # < this -> CARRY-FORWARD CONFIRMED
HDL_RHO_FALSIFIED    = 0.95    # >= this -> FALSIFIED-favorable; [0.85, 0.95) -> WEAKENED


# ============================================================================
# Step 0: Load registry (v0.16 schema adapter)
# ============================================================================

with REGISTRY.open() as f:
    registry_raw = json.load(f)

# v0.16 schema: panel + alternates
# Adapt to v15-compatible (brand_canonical, tradition_cell, etc.) for internal use
canonical_to_meta = {}
for b in registry_raw["panel"]:
    canonical_to_meta[b["display_name"]] = {
        "brand_id":         b["brand_id"],
        "tradition_cell":   b["tradition_cell"],
        "tier":             b["tier"],
        "founded":          b.get("founded"),
        "role":             "panel",
    }

canonical_brands = list(canonical_to_meta.keys())
print(f"Registry: {len(canonical_brands)} panel brands loaded "
      f"(v0.16 schema)")
print(f"Pivot: {PIVOT}")


# ============================================================================
# Step 1: Load E1a exclusions from Phase B log
# ============================================================================

e1a_excluded = set()
tested_not_activated = set()
phase_b = pd.read_csv(PHASEB_LOG)
for _, row in phase_b.iterrows():
    if row.get("role") == "alternate":
        # Alternate rows — flagged TESTED_NOT_ACTIVATED unless promoted
        notes = str(row.get("notes", "") or "")
        if "TESTED_NOT_ACTIVATED" in notes:
            tested_not_activated.add(row["brand_canonical"])
        continue
    if row["final_query_tier"] == "EXCLUDED_E1a":
        e1a_excluded.add(row["brand_canonical"])

print(f"E1a-excluded brands: {len(e1a_excluded)}: {sorted(e1a_excluded)}")
print(f"Tested-not-activated alternates: {len(tested_not_activated)}")
print()


# ============================================================================
# Step 2: Load brand ages
# ============================================================================

brand_age_years = {}
with AGE_FILE.open() as f:
    for row in csv.DictReader(f):
        bname = row["display_name"]
        fy = row.get("founded_year", "")
        if fy and fy.isdigit():
            brand_age_years[bname] = CURRENT_YEAR - int(fy)

print(f"Brand ages loaded: {len(brand_age_years)} brands")
print()


# ============================================================================
# Step 3: Compute AI Presence per wave (carry-forward from v0.15)
# ============================================================================

def compute_presence_split(enriched_path, registry_brands, t1_runs, t2_runs):
    """Aggregate per-(brand, wave) AI Presence across all prompts.

    Returns DataFrame with columns:
      brand, ai_t1_pct, ai_t2_pct, ai_t1_n, ai_t2_n
    """
    df = pd.read_csv(enriched_path)
    df = df[df["model_slot"].isin(MATCHED_MODELS)]

    def compute_one_wave(d):
        out = {}
        for brand in registry_brands:
            brand_rows = d[d["brand"] == brand]
            n = len(brand_rows)
            if n == 0:
                out[brand] = (None, 0)
            else:
                pct = brand_rows["ai_brand_mentioned"].mean() * 100
                out[brand] = (round(pct, 2), n)
        return out

    t1 = compute_one_wave(df[df["run_idx"].isin(t1_runs)])
    t2 = compute_one_wave(df[df["run_idx"].isin(t2_runs)])

    rows = []
    for brand in registry_brands:
        t1_pct, t1_n = t1[brand]
        t2_pct, t2_n = t2[brand]
        rows.append({
            "brand":      brand,
            "ai_t1_pct":  t1_pct,
            "ai_t2_pct":  t2_pct,
            "ai_t1_n":    t1_n,
            "ai_t2_n":    t2_n,
        })
    return pd.DataFrame(rows)


# ============================================================================
# Step 3b (NEW for v0.16): Per-(brand, prompt_id, wave) presence
#   for H_Discourse_Language_carryforward
# ============================================================================

def compute_presence_by_prompt(enriched_path, prompt_ids, brand_list,
                               t1_runs, t2_runs):
    """Per-(brand, prompt_id, wave) AI Presence.

    Used for H_Discourse_Language_carryforward to compare English vs
    native-language prompt conditions on the Japanese tradition cell.

    Returns dict[brand][prompt_id][wave] -> pct (or None if no rows).
    """
    df = pd.read_csv(enriched_path)
    df = df[df["model_slot"].isin(MATCHED_MODELS)]
    df = df[df["prompt_id"].isin(prompt_ids)]
    df = df[df["brand"].isin(brand_list)]

    out = {b: {p: {} for p in prompt_ids} for b in brand_list}

    for brand in brand_list:
        for prompt_id in prompt_ids:
            for wave, run_set in [("t1", t1_runs), ("t2", t2_runs)]:
                wave_rows = df[
                    (df["brand"] == brand) &
                    (df["prompt_id"] == prompt_id) &
                    (df["run_idx"].isin(run_set))
                ]
                if len(wave_rows) == 0:
                    out[brand][prompt_id][wave] = None
                else:
                    out[brand][prompt_id][wave] = round(
                        wave_rows["ai_brand_mentioned"].mean() * 100, 2)
    return out


# ============================================================================
# Step 4: Build paired DataFrame (AI x Trends x covariates)
# ============================================================================

# Locate the most recent enriched results CSV for kitchen knives
ENRICHED_DIR = AIAS_ROOT / "data" / "kitchen_knives"
enriched_candidates = sorted(ENRICHED_DIR.glob("results_enriched_kitchen_knives_*.csv"))
if not enriched_candidates:
    import sys
    sys.exit(f"ERROR: no enriched results CSV at {ENRICHED_DIR}\n"
             f"LLM acquisition + enrichment must complete before scoring.")
ENRICHED = enriched_candidates[-1]
print(f"Enriched CSV: {ENRICHED.name}")

ai_df = compute_presence_split(ENRICHED, canonical_brands, T1_RUN_IDX, T2_RUN_IDX)

trends_df = pd.read_csv(TRENDS_PROC)
trends_df = trends_df[trends_df["category"] == CATEGORY]

# Merge per region
paired = ai_df.copy()
for region in ("worldwide", "US"):
    r = trends_df[trends_df["region"] == region]
    r = r.rename(columns={
        "t1_mean": f"trends_{region}_t1_mean",
        "t2_mean": f"trends_{region}_t2_mean",
        "t1_eligible_E1b": f"trends_{region}_t1_eligible",
        "t2_eligible_E1b": f"trends_{region}_t2_eligible",
    })
    paired = paired.merge(
        r[["brand", f"trends_{region}_t1_mean", f"trends_{region}_t2_mean",
           f"trends_{region}_t1_eligible", f"trends_{region}_t2_eligible"]],
        on="brand", how="left"
    )

# Add covariates
paired["e1a_excluded"]        = paired["brand"].isin(e1a_excluded)
paired["tested_not_activated"] = paired["brand"].isin(tested_not_activated)
paired["brand_age_years"]     = paired["brand"].map(brand_age_years)
paired["tradition"]           = paired["brand"].map(
    lambda b: canonical_to_meta.get(b, {}).get("tradition_cell", "unknown"))
paired["tier"]                = paired["brand"].map(
    lambda b: canonical_to_meta.get(b, {}).get("tier", "unknown"))

paired.to_csv(OUT_DIR / "per_brand_paired.csv", index=False)
print(f"per_brand_paired.csv: {len(paired)} rows")
print()


# ============================================================================
# Step 5: Correlation function (port from v0.15)
# ============================================================================

def correlations(df, region, wave, exclude_brands=None):
    """Compute correlations for one (region, wave) slice.

    Returns dict with spearman_rho (bivariate AI~Trends),
    partial_spearman_rho (AI~Trends controlling for age + tradition dummies).

    Per pre-reg §2: Cond 2 is |spearman_rho| < 0.35; Cond 3 is
    partial_spearman_rho < 0. Brand age (continuous, rank-transformed) and
    tradition_cell (categorical dummies) are the partial controls.
    """
    exclude_brands = exclude_brands or set()
    elig_col = f"trends_{region}_{wave}_eligible"
    elig = df[df[elig_col]].copy()
    elig = elig[~elig["e1a_excluded"]]
    elig = elig[~elig["tested_not_activated"]]
    elig = elig[~elig["brand"].isin(exclude_brands)]
    elig = elig.dropna(subset=[
        f"trends_{region}_{wave}_mean", f"ai_{wave}_pct",
        "brand_age_years", "tradition",
    ])
    n = len(elig)
    out = {"n": n, "brands": list(elig["brand"])}
    if n < 4:
        for k in ("spearman_rho", "spearman_p_two_tailed", "spearman_p_one_tailed",
                  "pearson_r", "pearson_p_two_tailed",
                  "partial_spearman_rho", "partial_spearman_p_one_tailed",
                  "ai_age_rho", "ai_age_p_two_tailed",
                  "partial_n_traditions_in_slice", "partial_df_adj_k"):
            out[k] = None
        return out

    x = elig[f"ai_{wave}_pct"].values.astype(float)
    y = elig[f"trends_{region}_{wave}_mean"].values.astype(float)
    z1 = elig["brand_age_years"].values.astype(float)
    trad = elig["tradition"].values

    # Bivariate AI~Trends (canonical Cond 2 per pre-reg §2, AIAS v1.2 §3.4)
    rho, p_rho = stats.spearmanr(x, y)
    p_rho_1t = float(p_rho / 2) if rho > 0 else float(1 - p_rho / 2)
    r, p_r = stats.pearsonr(x, y)

    # Bivariate AI~age (informational; v0.14 legacy)
    rho_age, p_age = stats.spearmanr(x, z1)

    # Partial Spearman: AI~Trends, controlling for age (continuous) +
    # tradition dummies. Reference category: first TRADITION_LEVELS level
    # present in slice (arbitrary; partial corr is invariant to reference).
    xr = stats.rankdata(x)
    yr = stats.rankdata(y)
    z1r = stats.rankdata(z1)

    levels_in_slice = [lvl for lvl in TRADITION_LEVELS if (trad == lvl).any()]
    n_traditions = len(levels_in_slice)
    if n_traditions < 2:
        Z = np.column_stack([np.ones(n), z1r])
        df_adj_k = 1
    else:
        non_ref = levels_in_slice[1:]
        dummies = np.column_stack([(trad == lvl).astype(float) for lvl in non_ref])
        Z = np.column_stack([np.ones(n), z1r, dummies])
        df_adj_k = 1 + len(non_ref)  # expected = 5 per pre-reg §2 (5 cells)

    def resid(t):
        coef, *_ = np.linalg.lstsq(Z, t, rcond=None)
        return t - Z @ coef

    xr_res = resid(xr)
    yr_res = resid(yr)
    pr, _ = stats.pearsonr(xr_res, yr_res)
    df_adj = n - 2 - df_adj_k
    if df_adj > 0 and abs(pr) < 1:
        t_stat = pr * np.sqrt(df_adj / (1 - pr ** 2))
        partial_p_1t = float(1 - stats.t.cdf(t_stat, df=df_adj))
    else:
        partial_p_1t = float("nan")

    out.update({
        "spearman_rho":                  float(rho),
        "spearman_p_two_tailed":         float(p_rho),
        "spearman_p_one_tailed":         p_rho_1t,
        "pearson_r":                     float(r),
        "pearson_p_two_tailed":          float(p_r),
        "partial_spearman_rho":          float(pr),
        "partial_spearman_p_one_tailed": partial_p_1t,
        "ai_age_rho":                    float(rho_age),
        "ai_age_p_two_tailed":           float(p_age),
        "partial_n_traditions_in_slice": int(n_traditions),
        "partial_df_adj_k":              int(df_adj_k),
    })
    return out


# ============================================================================
# Step 6: H_Regime4_replication_knives evaluator
#   (per pre-reg §2; v0.15-canonical operationalization + PARTIAL verdict)
# ============================================================================

def eval_h_regime4_replication_knives(corr_t1, corr_t2, label="primary"):
    """Three-condition test for Regime 4 fit with v0.16 PARTIAL verdict.

    Per pre-reg §2 (commit 511e339, corrected per DEVIATIONS Entry 2):
        Cond 1: n_eligible >= HR4_N_FLOOR at both waves
        Cond 2: |rho(AI, Trends)| < HR4_RHO_MAX at both waves
        Cond 3: partial rho(AI, Trends | brand_age, tradition_cell)
                < HR4_PARTIAL_MAX at both waves

    Verdicts:
        CONFIRMED: All three hold
        PARTIAL: Cond 1 and Cond 2 hold; Cond 3 fails (positive partial).
                 Strict sub-classification of v0.15-canonical FALSIFIED;
                 v0.16 refinement, not a contradiction.
        FALSIFIED: Cond 1 fails OR Cond 2 fails
    """
    n_t1 = corr_t1.get("n", 0)
    n_t2 = corr_t2.get("n", 0)
    cond1 = n_t1 >= HR4_N_FLOOR and n_t2 >= HR4_N_FLOOR

    bivar_t1 = corr_t1.get("spearman_rho")
    bivar_t2 = corr_t2.get("spearman_rho")
    partial_t1 = corr_t1.get("partial_spearman_rho")
    partial_t2 = corr_t2.get("partial_spearman_rho")

    if any(v is None for v in (bivar_t1, bivar_t2, partial_t1, partial_t2)):
        return {
            "label": label,
            "status": "INDETERMINATE",
            "rationale": "Insufficient n; cannot compute correlations.",
            "n_t1": n_t1, "n_t2": n_t2,
        }

    cond2 = abs(bivar_t1) < HR4_RHO_MAX and abs(bivar_t2) < HR4_RHO_MAX
    cond3 = partial_t1 < HR4_PARTIAL_MAX and partial_t2 < HR4_PARTIAL_MAX

    if cond1 and cond2 and cond3:
        status = "CONFIRMED"
    elif cond1 and cond2 and not cond3:
        status = "PARTIAL"
    else:
        status = "FALSIFIED"

    return {
        "label": label,
        "status": status,
        "condition_1_n_floor": {
            "n_t1": n_t1, "n_t2": n_t2, "threshold": HR4_N_FLOOR,
            "satisfied": cond1,
        },
        "condition_2_trends": {
            "bivariate_rho_t1": bivar_t1, "bivariate_rho_t2": bivar_t2,
            "threshold": HR4_RHO_MAX, "satisfied": cond2,
            "interpretation": (
                "|rho(AI_presence, Trends)| < 0.35 at both waves "
                "(per pre-reg §2; AIAS Protocol v1.2 §3.4)"
            ),
        },
        "condition_3_partial": {
            "partial_rho_t1": partial_t1, "partial_rho_t2": partial_t2,
            "threshold": HR4_PARTIAL_MAX, "satisfied": cond3,
            "interpretation": (
                "Partial rho(AI, Trends) controlling for brand_age + "
                "tradition_cell (k_adj=5 expected) at both waves < 0"
            ),
        },
        "rationale": (
            f"C1 (n>={HR4_N_FLOOR} both waves): {cond1} "
            f"(n_t1={n_t1}, n_t2={n_t2}). "
            f"C2 (|rho_AI~Trends|<{HR4_RHO_MAX}): {cond2} "
            f"(t1={bivar_t1:.3f}, t2={bivar_t2:.3f}). "
            f"C3 (partial<{HR4_PARTIAL_MAX}): {cond3} "
            f"(t1={partial_t1:.3f}, t2={partial_t2:.3f})."
        ),
    }


# ============================================================================
# Step 7: H_Discourse_Language_carryforward evaluator (NEW for v0.16)
# ============================================================================

def eval_h_discourse_language_carryforward(presence_by_prompt, japanese_brands,
                                           en_prompt, ja_prompt):
    """v0.16 pre-reg §2 H_Discourse_Language_carryforward.

    Tests v0.8 (SSRN 6728000) finding under v1.2 protocol with corrected
    eligibility filtering.

    Decision rules (Japanese tradition cell anchor; n_eligible_japanese >= 5):
        ρ_(en,ja) < 0.85 at both waves -> CARRY-FORWARD CONFIRMED
        ρ_(en,ja) ∈ [0.85, 0.95) at both waves -> CARRY-FORWARD WEAKENED
        ρ_(en,ja) >= 0.95 at both waves -> CARRY-FORWARD FALSIFIED-favorable
        n < 5 -> INCONCLUSIVE

    Args:
        presence_by_prompt: output of compute_presence_by_prompt
        japanese_brands: list of brand canonicals in Japanese tradition cell
        en_prompt: prompt_id of English tradition-anchored prompt for Japan
                   (e.g., "knives_b3_en_jp")
        ja_prompt: prompt_id of Japanese-language tradition prompt
                   (e.g., "knives_b4_ja_01")
    """
    result = {
        "label": "H_Discourse_Language_carryforward",
        "japanese_brands_in_panel": japanese_brands,
        "en_prompt_id": en_prompt,
        "ja_prompt_id": ja_prompt,
        "n_floor": HDL_N_FLOOR_JAPANESE,
        "thresholds": {
            "confirmed_upper": HDL_RHO_CONFIRMED,
            "falsified_lower": HDL_RHO_FALSIFIED,
        },
    }

    waves_data = {}
    for wave in ("t1", "t2"):
        en_vals = []
        ja_vals = []
        eligible_brands = []
        for brand in japanese_brands:
            en_v = presence_by_prompt.get(brand, {}).get(en_prompt, {}).get(wave)
            ja_v = presence_by_prompt.get(brand, {}).get(ja_prompt, {}).get(wave)
            if en_v is not None and ja_v is not None:
                en_vals.append(en_v)
                ja_vals.append(ja_v)
                eligible_brands.append(brand)
        n = len(eligible_brands)
        if n < 2:
            waves_data[wave] = {"n": n, "rho": None, "p": None,
                                "brands": eligible_brands}
        else:
            rho, p = stats.spearmanr(en_vals, ja_vals)
            waves_data[wave] = {
                "n": n,
                "rho": float(rho) if not np.isnan(rho) else None,
                "p": float(p) if not np.isnan(p) else None,
                "brands": eligible_brands,
            }
    result["waves"] = waves_data

    n_t1 = waves_data["t1"]["n"]
    n_t2 = waves_data["t2"]["n"]
    if n_t1 < HDL_N_FLOOR_JAPANESE or n_t2 < HDL_N_FLOOR_JAPANESE:
        result["status"] = "INCONCLUSIVE"
        result["rationale"] = (
            f"n_eligible_japanese < {HDL_N_FLOOR_JAPANESE} "
            f"(t1={n_t1}, t2={n_t2}). Insufficient cell coverage."
        )
        return result

    rho_t1 = waves_data["t1"]["rho"]
    rho_t2 = waves_data["t2"]["rho"]

    if rho_t1 is None or rho_t2 is None:
        result["status"] = "INDETERMINATE"
        result["rationale"] = "rho undefined (zero variance in one or both waves)"
        return result

    if rho_t1 < HDL_RHO_CONFIRMED and rho_t2 < HDL_RHO_CONFIRMED:
        status = "CARRY-FORWARD CONFIRMED"
        interp = ("Both waves below 0.85 threshold; v0.8 finding survives "
                  "v1.2 protocol with corrected eligibility filtering.")
    elif rho_t1 < HDL_RHO_FALSIFIED and rho_t2 < HDL_RHO_FALSIFIED:
        status = "CARRY-FORWARD WEAKENED"
        interp = ("One or both waves in [0.85, 0.95); v0.8 finding "
                  "attenuated under v1.2 eligibility filtering — partial "
                  "artifact reading: some signal protocol-correctable, "
                  "substantive component remains.")
    else:
        status = "CARRY-FORWARD FALSIFIED-favorable"
        interp = ("One or both waves at/above 0.95; v0.8 finding does not "
                  "survive v1.2 eligibility filtering; documented as "
                  "pre-v1.2 protocol artifact now corrected. "
                  "Methodologically informative.")

    result["status"] = status
    result["rationale"] = (
        f"rho_t1={rho_t1:.3f}, rho_t2={rho_t2:.3f}, "
        f"n_t1={n_t1}, n_t2={n_t2}. {interp}"
    )
    return result


# ============================================================================
# Step 8: Run correlations for both regions, both waves
# ============================================================================

correlations_by_region_wave = {
    "ww_t1": correlations(paired, "worldwide", "t1"),
    "ww_t2": correlations(paired, "worldwide", "t2"),
    "us_t1": correlations(paired, "US", "t1"),
    "us_t2": correlations(paired, "US", "t2"),
}

print("Correlations:")
for k, v in correlations_by_region_wave.items():
    if v.get("spearman_rho") is None:
        print(f"  {k}: n={v['n']} (insufficient)")
    else:
        print(f"  {k}: n={v['n']}  rho={v['spearman_rho']:.3f}  "
              f"partial={v['partial_spearman_rho']:.3f}  "
              f"(k_adj={v['partial_df_adj_k']})")
print()


# ============================================================================
# Step 9: H_Regime4_replication_knives — primary verdict
# ============================================================================

hr4 = eval_h_regime4_replication_knives(
    correlations_by_region_wave["ww_t1"],
    correlations_by_region_wave["ww_t2"],
    label="primary",
)

print("=" * 72)
print(f"H_Regime4_replication_knives (worldwide, primary): {hr4['status']}")
print(f"  {hr4.get('rationale', '')}")
print()


# ============================================================================
# Step 10: H_Discourse_Language_carryforward
# ============================================================================

# Japanese tradition cell brands from registry
japanese_brands = [b for b, m in canonical_to_meta.items()
                   if m["tradition_cell"] == "japanese"]
# Filter to Phase B-eligible only
japanese_brands_eligible = [b for b in japanese_brands
                            if b not in e1a_excluded]

# Look up discourse-language pair from prompts JSON
with PROMPTS.open() as f:
    prompts_data = json.load(f)
discourse_pairs = prompts_data["prompt_summary"]["discourse_language_pairs"]
ja_pair = next(p for p in discourse_pairs if p["pair_id"] == "pair_japanese")

# Compute per-prompt presence
presence_by_prompt = compute_presence_by_prompt(
    ENRICHED,
    [ja_pair["en_prompt"], ja_pair["native_prompt"]],
    japanese_brands_eligible,
    T1_RUN_IDX, T2_RUN_IDX,
)

hdl = eval_h_discourse_language_carryforward(
    presence_by_prompt,
    japanese_brands_eligible,
    ja_pair["en_prompt"],
    ja_pair["native_prompt"],
)

print("=" * 72)
print(f"H_Discourse_Language_carryforward: {hdl['status']}")
print(f"  {hdl.get('rationale', '')}")
print()


# ============================================================================
# Step 11: Write canonical scoring outputs
# ============================================================================

scoring_results = {
    "phase": "v0.16",
    "category": CATEGORY,
    "session_timestamp": datetime.now(timezone.utc).isoformat(),
    "pre_reg_tag": "v0.16-prereg",
    "pre_reg_commit": "511e339",
    "methodology_base": "AIAS Protocol v1.2 (SSRN 6761698)",
    "carry_forward_base": "v0.15 (SSRN 6768059)",
    "correlations": correlations_by_region_wave,
    "H_Regime4_replication_knives": hr4,
    "H_Discourse_Language_carryforward": hdl,
    "panel_size": len(canonical_brands),
    "e1a_excluded": sorted(e1a_excluded),
    "japanese_cell_size": len(japanese_brands_eligible),
}

with (OUT_DIR / "canonical_scoring.json").open("w") as f:
    json.dump(scoring_results, f, indent=2, ensure_ascii=False, default=str)

# Flat CSV for spreadsheet review
flat_rows = []
for hyp_key, hyp_result in [
    ("H_Regime4_replication_knives", hr4),
    ("H_Discourse_Language_carryforward", hdl),
]:
    flat_rows.append({
        "phase":     "v0.16",
        "category":  CATEGORY,
        "hypothesis": hyp_key,
        "status":    hyp_result.get("status", ""),
        "rationale": hyp_result.get("rationale", ""),
    })

with (OUT_DIR / "canonical_scoring.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(flat_rows[0].keys()))
    writer.writeheader()
    writer.writerows(flat_rows)

# Per-hypothesis detail CSVs
hr4_row = {
    "hypothesis": "H_Regime4_replication_knives",
    "status": hr4.get("status"),
    "n_t1": hr4.get("condition_1_n_floor", {}).get("n_t1"),
    "n_t2": hr4.get("condition_1_n_floor", {}).get("n_t2"),
    "bivariate_rho_t1": hr4.get("condition_2_trends", {}).get("bivariate_rho_t1"),
    "bivariate_rho_t2": hr4.get("condition_2_trends", {}).get("bivariate_rho_t2"),
    "partial_rho_t1": hr4.get("condition_3_partial", {}).get("partial_rho_t1"),
    "partial_rho_t2": hr4.get("condition_3_partial", {}).get("partial_rho_t2"),
    "cond1_satisfied": hr4.get("condition_1_n_floor", {}).get("satisfied"),
    "cond2_satisfied": hr4.get("condition_2_trends", {}).get("satisfied"),
    "cond3_satisfied": hr4.get("condition_3_partial", {}).get("satisfied"),
    "rationale": hr4.get("rationale"),
}
with (OUT_DIR / "h_regime4_replication_knives.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(hr4_row.keys()))
    writer.writeheader()
    writer.writerow(hr4_row)

hdl_row = {
    "hypothesis": "H_Discourse_Language_carryforward",
    "status": hdl.get("status"),
    "n_t1": hdl.get("waves", {}).get("t1", {}).get("n"),
    "n_t2": hdl.get("waves", {}).get("t2", {}).get("n"),
    "rho_t1": hdl.get("waves", {}).get("t1", {}).get("rho"),
    "rho_t2": hdl.get("waves", {}).get("t2", {}).get("rho"),
    "japanese_brands": ",".join(hdl.get("japanese_brands_in_panel", [])),
    "rationale": hdl.get("rationale"),
}
with (OUT_DIR / "h_discourse_language_carryforward.csv").open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(hdl_row.keys()))
    writer.writeheader()
    writer.writerow(hdl_row)

print("=" * 72)
print("v0.16 scoring complete. Outputs:")
print(f"  {OUT_DIR}/canonical_scoring.json")
print(f"  {OUT_DIR}/canonical_scoring.csv")
print(f"  {OUT_DIR}/h_regime4_replication_knives.csv")
print(f"  {OUT_DIR}/h_discourse_language_carryforward.csv")
print()
print("Next: chart build, brand-format report, SSRN paper draft.")
