"""v0.13 Hypothesis evaluation: H1-H4 per category (5 categories), H5/H6/H7
cross-category, H8 Mint phantom-persistence diagnostic, plus Category-Scale
Mismatch Finding for olive oil (descriptive-only per pre-reg §3.6a, inherited
from v0.12).

Structural fork of score_v12.py. The Spearman / Pearson / partial-Spearman
machinery, the per-category evaluation loop, the H1/H2/H3/H4 evaluators, the
H6 diagnostic detector, the Category-Scale Mismatch table, and the pooled
sensitivity ρ all transfer verbatim. v0.13 changes:

  - 5 categories instead of 3 (skincare + finance added; PM/oliveoil/running
    inherited from v0.12 trends_processed deposit per pre-reg §5.3).
  - Trends source per category: v0.12 deposit for reuse arm, v0.13 deposit
    for fresh arm.
  - Phase B source per category: v0.12 log for reuse arm, v0.13 log for
    fresh arm.
  - H5 redefined per pre-reg §2 H5: 'v0.12 marginal signature in 3+ of
    effective-N categories', where the signature is ρ ∈ [0.35, 0.65] at both
    waves AND H3 falsified at 1 or 2 of 3 at both waves AND at least one
    Linear-style brand surfaces.
  - H6 threshold updated per pre-reg §2 H6: '4+ of effective-N' (was 2+ in
    v0.12's smaller 3-category panel).
  - H7 NEW per pre-reg §2 H7: three-regimes classification (Marginal-direct /
    Age-mediated strong / Scale-mismatch) with clean-classification rule;
    excludes phantom-flagged brands (Mint) before re-computing correlations
    for the regime decision tree.
  - H8 NEW per pre-reg §2 H8: Mint phantom-persistence three-condition
    diagnostic (finance only); confirmation requires all three to hold.

Inputs:
  - ~/aias/osf_staging/v09/data/{pm,oliveoil,running,skincare,finance}/results_enriched_v06_*.csv  (t1)
  - ~/aias/osf_staging/v09/data/{pm,oliveoil,running,skincare,finance}/results_enriched_v09_*.csv  (t2)
  - ~/aias/osf/v12/data/trends_processed/per_brand_within_window.csv  (reuse-arm Trends)
  - ~/aias/osf/v13/data/trends_processed/per_brand_within_window.csv  (fresh-arm Trends)
  - ~/aias/osf/v12/registries/topic_id_resolution_log_v0.12.csv  (reuse-arm Phase B)
  - ~/aias/osf/v13/registries/topic_id_resolution_log_v0.13.csv  (fresh-arm Phase B)
  - ~/aias/osf/v13/registries/brand_age_sources_v0.13.csv  (93 brands; extended from v0.12)
  - ~/aias/registries/brands_{pm,oliveoil,running}.json  (v0.12 registries)
  - ~/aias/osf/v13/registries/brands_{skincare,finance}.json  (v0.13 registries)

Outputs:
  - ~/aias/osf/v13/analysis/per_brand_paired.csv
  - ~/aias/osf/v13/analysis/canonical_scoring.csv
  - ~/aias/osf/v13/analysis/canonical_scoring.json
  - ~/aias/osf/v13/analysis/category_scale_mismatch_table.csv  (olive oil)
  - ~/aias/osf/v13/analysis/h7_regime_classification.csv
  - ~/aias/osf/v13/analysis/h8_mint_diagnostic.csv

Run:
    python3 ~/aias/scripts/score_v13.py
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
V13_ROOT = HOME / "aias" / "osf" / "v13"
V09_DATA = HOME / "aias" / "osf_staging" / "v09" / "data"
LEGACY_REGISTRIES = HOME / "aias" / "registries"

V12_TRENDS  = V12_ROOT / "data" / "trends_processed" / "per_brand_within_window.csv"
V13_TRENDS  = V13_ROOT / "data" / "trends_processed" / "per_brand_within_window.csv"
V12_PHASEB  = V12_ROOT / "registries" / "topic_id_resolution_log_v0.12.csv"
V13_PHASEB  = V13_ROOT / "registries" / "topic_id_resolution_log_v0.13.csv"
AGE_FILE    = V13_ROOT / "registries" / "brand_age_sources_v0.13.csv"

OUT_DIR = V13_ROOT / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MATCHED_MODELS = {"claude-sonnet-4-6", "gpt-5.4-mini"}

# Per-category configuration. trends_source and phaseb_source route reuse-arm
# categories to v0.12 deposit and fresh-arm categories to v0.13 deposit per
# pre-reg §5.3.
CATEGORIES = {
    "pmsoftware": {
        "pivot": "Asana",
        "data_dir": "pm",
        "trends_source": V12_TRENDS,
        "phaseb_source": V12_PHASEB,
        "trends_category_label": "pmsoftware",
        "phaseb_category_label": "pmsoftware",
        "registry_path": LEGACY_REGISTRIES / "brands_pm.json",
        "descriptive_only": False,
        "phantom_brands": [],
    },
    "oliveoil": {
        "pivot": "California Olive Ranch",
        "data_dir": "oliveoil",
        "trends_source": V12_TRENDS,
        "phaseb_source": V12_PHASEB,
        "trends_category_label": "oliveoil",
        "phaseb_category_label": "oliveoil",
        "registry_path": LEGACY_REGISTRIES / "brands_oliveoil.json",
        "descriptive_only": True,  # pre-reg §3.6a inherited from v0.12
        "phantom_brands": [],
    },
    "running": {
        "pivot": "Asics",
        "data_dir": "running",
        "trends_source": V12_TRENDS,
        "phaseb_source": V12_PHASEB,
        "trends_category_label": "running",
        "phaseb_category_label": "running",
        "registry_path": LEGACY_REGISTRIES / "brands_running.json",
        "descriptive_only": False,
        "phantom_brands": [],
    },
    "skincare": {
        "pivot": "CeraVe",
        "data_dir": "skincare",
        "trends_source": V13_TRENDS,
        "phaseb_source": V13_PHASEB,
        "trends_category_label": "skincare",
        "phaseb_category_label": "skincare",
        "registry_path": V13_ROOT / "registries" / "brands_skincare.json",
        "descriptive_only": False,
        "phantom_brands": [],
    },
    "finance": {
        "pivot": "YNAB",
        "data_dir": "finance",
        "trends_source": V13_TRENDS,
        "phaseb_source": V13_PHASEB,
        "trends_category_label": "finance",
        "phaseb_category_label": "finance",
        "registry_path": V13_ROOT / "registries" / "brands_finance.json",
        "descriptive_only": False,
        "phantom_brands": ["Mint"],  # per pre-reg §2 H8
    },
}

# Hypothesis thresholds (per pre-reg §2)
H1_RHO_THRESHOLD = 0.5
H1_P_THRESHOLD   = 0.05
H2_DELTA_THRESHOLD = 0.15
H3_TOP_K_AI     = 3
H3_TOP_K_TRENDS = 5
H4_RHO_THRESHOLD = 0.5
H4_P_THRESHOLD   = 0.05
N_FLOOR_HARD  = 10
N_FLOOR_ALIGN = 12

# H5 v0.13: v0.12 marginal signature definition + 3-of-effective-N rule
H5_MARGINAL_RHO_MIN = 0.35
H5_MARGINAL_RHO_MAX = 0.65
H5_REQUIRED_COUNT   = 3

# H6 (per pre-reg §2 H6) — same Linear/Todoist thresholds as v0.12; new count rule
H6_LINEAR_AI_MIN     = 50.0
H6_LINEAR_TRENDS_MAX = 5.0
H6_TODOIST_AI_MAX    = 5.0
H6_TODOIST_TRENDS_MIN = 20.0
H6_REQUIRED_COUNT    = 4

# H7 (per pre-reg §2 H7) — three regimes decision tree
H7_R1_RHO_MIN        = 0.35
H7_R1_RHO_MAX        = 0.65
H7_R1_DECREMENT_MAX  = 0.15
H7_R2_RHO_MIN        = 0.65   # exclusive — > 0.65
H7_R2_DECREMENT_MIN  = 0.25   # exclusive — > 0.25
H7_R3_PASS_FRAC_MAX  = 0.6
H7_BOUNDARY_TOLERANCE = 0.05

# H8 (per pre-reg §2 H8) — Mint phantom-persistence
H8_AI_FLOOR_PCT = 5.0
H8_TOP_K_AI     = 5
H8_TOP_K_TRENDS = 5

# Category-scale-mismatch threshold (pre-reg §10.2 / §10)
SCALE_MISMATCH_AI_MIN = 5.0

TIER_ORDINAL = {"incumbent": 1, "mid-tier": 2, "challenger": 3}

# ============================================================================
# Step 1: Load E1a exclusions from both Phase B logs
# ============================================================================

e1a_by_cat = {cat: set() for cat in CATEGORIES}

# v0.12 Phase B has categories: pmsoftware, oliveoil, running
phase_b_v12 = pd.read_csv(V12_PHASEB)
for _, row in phase_b_v12.iterrows():
    if row["final_query_tier"] == "EXCLUDED_E1a":
        cat = row["category"]
        if cat in e1a_by_cat:
            e1a_by_cat[cat].add(row["brand_canonical"])

# v0.13 Phase B has categories: skincare, finance
phase_b_v13 = pd.read_csv(V13_PHASEB)
for _, row in phase_b_v13.iterrows():
    if row["final_query_tier"] == "EXCLUDED_E1a":
        cat = row["category"]
        if cat in e1a_by_cat:
            e1a_by_cat[cat].add(row["brand_canonical"])

print("E1a exclusions by category (from Phase B locked CSVs):")
for cat, brands in e1a_by_cat.items():
    print(f"  {cat}: {sorted(brands) if brands else '(none)'}")
print()

# ============================================================================
# Step 2: Load registries per category
# ============================================================================

registries = {}
for cat, cfg in CATEGORIES.items():
    reg_path = cfg["registry_path"]
    if not reg_path.exists():
        print(f"WARN: registry not found at {reg_path}; skipping {cat}")
        registries[cat] = []
        continue
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


ai_presence = {}
n_responses = {}
for cat, cfg in CATEGORIES.items():
    data_dir = V09_DATA / cfg["data_dir"]
    v06_files = sorted(glob.glob(str(data_dir / "results_enriched_v06_*.csv")))
    v09_files = sorted(glob.glob(str(data_dir / "results_enriched_v09_*.csv")))
    if not v06_files or not v09_files:
        print(f"WARN: missing v06 or v09 files for {cat} at {data_dir}")
        ai_presence[cat] = {"t1": {}, "t2": {}}
        n_responses[cat] = {"t1": 0, "t2": 0}
        continue
    v06_path = Path(v06_files[-1])
    v09_path = Path(v09_files[-1])
    print(f"{cat}: t1 = {v06_path.name}; t2 = {v09_path.name}")
    p_t1, n_t1 = compute_presence(v06_path, registries[cat])
    p_t2, n_t2 = compute_presence(v09_path, registries[cat])
    ai_presence[cat] = {"t1": p_t1, "t2": p_t2}
    n_responses[cat] = {"t1": n_t1, "t2": n_t2}
print()

# ============================================================================
# Step 4: Load combined Trends + ages, build paired dataset per category
# ============================================================================

trends_v12 = pd.read_csv(V12_TRENDS)
trends_v13 = pd.read_csv(V13_TRENDS)
trends_df = pd.concat([trends_v12, trends_v13], ignore_index=True)

if not AGE_FILE.exists():
    raise FileNotFoundError(
        f"Age file not found at {AGE_FILE}. Combine v0.12's brand_age_sources "
        f"with the v0.13 new-brand template per the setup instructions."
    )

age_df = pd.read_csv(AGE_FILE)
age_year_map = dict(zip(age_df["brand"], age_df["founding_year"]))
age_yrs_map  = dict(zip(age_df["brand"], age_df["age_as_of_2026_01_01"]))


def build_paired(cat):
    """Build paired dataset for one category. Returns DataFrame."""
    pivot = CATEGORIES[cat]["pivot"]
    brand_tier = {b["canonical"]: b["tier"] for b in registries[cat]}
    trends_label = CATEGORIES[cat]["trends_category_label"]

    trends_ww = trends_df[(trends_df["region"] == "worldwide") &
                          (trends_df["category"] == trends_label)].set_index("brand")
    trends_us = trends_df[(trends_df["region"] == "US") &
                          (trends_df["category"] == trends_label)].set_index("brand")

    records = []
    for b in [r["canonical"] for r in registries[cat]]:
        rec = {
            "brand": b,
            "category": cat,
            "market_tier": brand_tier.get(b, ""),
            "tier_ordinal": TIER_ORDINAL.get(brand_tier.get(b, ""), None),
            "brand_age_years": age_yrs_map.get(b),
            "founding_year":   age_year_map.get(b),
            "ai_t1_pct": ai_presence.get(cat, {}).get("t1", {}).get(b, 0.0),
            "ai_t2_pct": ai_presence.get(cat, {}).get("t2", {}).get(b, 0.0),
            "e1a_excluded": b in e1a_by_cat[cat],
            "is_pivot":     b == pivot,
            "is_phantom":   b in CATEGORIES[cat]["phantom_brands"],
        }
        for label, src in [("ww", trends_ww), ("us", trends_us)]:
            if b in src.index:
                row = src.loc[b]
                for w in ("t1", "t2"):
                    rec[f"trends_{label}_{w}_mean"] = (
                        float(row[f"{w}_mean"]) if pd.notna(row[f"{w}_mean"]) else None
                    )
                    rec[f"trends_{label}_{w}_eligible"]    = bool(row[f"{w}_eligible_E1b"])
                    rec[f"trends_{label}_{w}_raw_eligible"] = bool(row[f"{w}_raw_eligible"])
                    rec[f"trends_{label}_{w}_sparse"]       = bool(row[f"{w}_sparse_E5"])
            else:
                for w in ("t1", "t2"):
                    rec[f"trends_{label}_{w}_mean"] = None
                    rec[f"trends_{label}_{w}_eligible"]    = False
                    rec[f"trends_{label}_{w}_raw_eligible"] = False
                    rec[f"trends_{label}_{w}_sparse"]       = False
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
# Step 5: Correlation function (verbatim from score_v12.py)
# ============================================================================

def correlations(df, region, wave, raw_strict=False, exclude_phantoms=False):
    """Compute correlations for one (category, region, wave) slice.

    df: paired dataset for ONE category (already filtered).
    raw_strict: if True, only include brands with raw_eligible=True (sensitivity).
    exclude_phantoms: if True, also exclude is_phantom=True brands (for H7).
    """
    elig_col = f"trends_{region}_{wave}_eligible"
    raw_col  = f"trends_{region}_{wave}_raw_eligible"
    elig = df[df[elig_col]].copy()
    if raw_strict:
        elig = elig[elig[raw_col]]
    elig = elig[~elig["e1a_excluded"]]
    if exclude_phantoms:
        elig = elig[~elig["is_phantom"]]
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
# Step 6: Hypothesis evaluators (H1-H4 verbatim from score_v12.py)
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
        top5_t  = list(e.sort_values(f"trends_{region}_{wave}_mean", ascending=False).head(H3_TOP_K_TRENDS)["brand"])
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
# Step 7: Per-category evaluation (verbatim from score_v12.py)
# ============================================================================

all_results = {}

for cat in CATEGORIES:
    df_cat = paired_all[paired_all["category"] == cat].copy()
    descriptive_only = CATEGORIES[cat]["descriptive_only"]

    print("=" * 80)
    print(f"### CATEGORY: {cat}  (descriptive-only: {descriptive_only})")
    print("=" * 80)

    cat_results = {"descriptive_only": descriptive_only, "correlations": {}, "hypotheses": {}}

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

        cat_results["h6_diagnostics"] = detect_h6_diagnostics(df_cat, "ww")

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
        print(f"  H1 US-only:    {h1_us['status']}")
        print(f"  H1 Pearson:    {h1_pearson['status']}")
        if cat == "running":
            print(f"  H1 raw-strict: {h1_raw_strict['status']}  (n_t1={r_t1['n']}, n_t2={r_t2['n']})")
        print()
    else:
        print(f"  (descriptive-only category — H1-H4 indeterminate per §3.6a)")
        print()

    all_results[cat] = cat_results

# ============================================================================
# Step 8: H5 cross-category — v0.12 marginal signature, 3-of-effective-N
# ============================================================================

def v12_marginal_signature_per_category(cat_results):
    """v0.12 marginal signature per pre-reg §2 H5:
    ρ ∈ [0.35, 0.65] at both waves AND H3 falsified at 1 or 2 of 3 at both
    waves AND at least one Linear-style brand surfaces.
    """
    if cat_results["descriptive_only"]:
        return {"applicable": False, "reason": "descriptive-only"}
    h1 = cat_results["hypotheses"]["H1_primary"]
    h3 = cat_results["hypotheses"]["H3"]
    h6_diag = cat_results["h6_diagnostics"]
    if h1["status"] == "INDETERMINATE":
        return {"applicable": False, "reason": "H1 indeterminate"}

    rt1, rt2 = h1.get("rho_t1"), h1.get("rho_t2")
    in_range_t1 = (rt1 is not None) and H5_MARGINAL_RHO_MIN <= rt1 <= H5_MARGINAL_RHO_MAX
    in_range_t2 = (rt2 is not None) and H5_MARGINAL_RHO_MIN <= rt2 <= H5_MARGINAL_RHO_MAX

    # H3 marginal: top-3 AI brands overlap with top-5 Trends at 1 or 2 of 3 (not 0, not 3)
    n_t1 = h3["per_wave"]["t1"]["n_in_top5"]
    n_t2 = h3["per_wave"]["t2"]["n_in_top5"]
    h3_marginal_t1 = (1 <= n_t1 <= 2)
    h3_marginal_t2 = (1 <= n_t2 <= 2)

    # At least one Linear-style brand at either wave
    has_linear = any(len(h6_diag["per_wave"][w]["linear_style"]) >= 1
                     for w in ("t1", "t2"))

    full_signature = (in_range_t1 and in_range_t2 and
                      h3_marginal_t1 and h3_marginal_t2 and
                      has_linear)
    return {
        "applicable": True,
        "signature_present": full_signature,
        "components": {
            "rho_in_range_t1": in_range_t1,
            "rho_in_range_t2": in_range_t2,
            "h3_marginal_t1":  h3_marginal_t1,
            "h3_marginal_t2":  h3_marginal_t2,
            "linear_style_present": has_linear,
        },
        "diagnostics": {
            "rho_t1": rt1, "rho_t2": rt2,
            "h3_n_in_top5_t1": n_t1, "h3_n_in_top5_t2": n_t2,
        },
    }


def eval_h5(per_cat_sig):
    applicable_cats = [c for c, s in per_cat_sig.items() if s["applicable"]]
    confirmed_cats  = [c for c in applicable_cats if per_cat_sig[c]["signature_present"]]
    n_apply   = len(applicable_cats)
    n_confirm = len(confirmed_cats)
    if n_apply == 0:
        return {"status": "INDETERMINATE", "rationale": "No applicable categories"}
    confirmed = (n_confirm >= H5_REQUIRED_COUNT)
    return {
        "status": "CONFIRMED" if confirmed else "FALSIFIED",
        "applicable_categories": applicable_cats,
        "confirmed_categories":  confirmed_cats,
        "rationale": (f"{n_confirm} of {n_apply} applicable categories show v0.12 "
                      f"marginal signature ({H5_REQUIRED_COUNT}-of-effective-N required)"),
    }


def eval_h6(all_results):
    applicable_cats = [c for c, r in all_results.items() if not r["descriptive_only"]]
    confirmed_cats  = [c for c in applicable_cats
                       if all_results[c]["h6_diagnostics"]["h6a_status"] == "CONFIRMED"]
    n_apply   = len(applicable_cats)
    n_confirm = len(confirmed_cats)
    confirmed = (n_confirm >= H6_REQUIRED_COUNT)
    return {
        "status": "CONFIRMED" if confirmed else "FALSIFIED",
        "applicable_categories": applicable_cats,
        "confirmed_categories":  confirmed_cats,
        "rationale": (f"{n_confirm} of {n_apply} applicable categories show both "
                      f"Linear-style and Todoist-style brands "
                      f"({H6_REQUIRED_COUNT}-of-effective-N required)"),
    }


per_cat_sig = {c: v12_marginal_signature_per_category(all_results[c]) for c in CATEGORIES}
h5 = eval_h5(per_cat_sig)
h6 = eval_h6(all_results)

print("=" * 80)
print("CROSS-CATEGORY HYPOTHESES")
print("=" * 80)
print(f"H5 (v0.12 marginal signature, 3-of-effective-N): {h5['status']}")
print(f"   {h5['rationale']}")
for cat, sig in per_cat_sig.items():
    if sig["applicable"]:
        rt1 = sig["diagnostics"]["rho_t1"]
        rt2 = sig["diagnostics"]["rho_t2"]
        rt1_str = f"{rt1:.3f}" if isinstance(rt1, (int, float)) else "NA"
        rt2_str = f"{rt2:.3f}" if isinstance(rt2, (int, float)) else "NA"
        n_t1 = sig["diagnostics"]["h3_n_in_top5_t1"]
        n_t2 = sig["diagnostics"]["h3_n_in_top5_t2"]
        comps = sig["components"]
        print(f"     {cat}: signature_present={sig['signature_present']}  "
              f"ρ=({rt1_str},{rt2_str})  H3_in_top5=({n_t1},{n_t2})  "
              f"linear={comps['linear_style_present']}")
    else:
        print(f"     {cat}: {sig['reason']}")
print()
print(f"H6 (Linear-style + Todoist-style, 4-of-effective-N): {h6['status']}")
print(f"   {h6['rationale']}")
print()

# ============================================================================
# Step 9: H7 — Three-regimes classification (NEW per pre-reg §2 H7)
# ============================================================================

def h7_classify_category(cat, df_cat, cat_results):
    """Re-compute correlations excluding phantom-flagged brands, then
    classify into one of three regimes per pre-reg §2 H7 decision tree.
    """
    if cat_results["descriptive_only"]:
        return {
            "applicable": False,
            "regime_class": "Regime 3 (Scale-mismatch via §3.6a)",
            "boundary_flag": False,
            "unclassifiable_flag": False,
            "rationale": "Descriptive-only routing inherits Regime 3 classification.",
            "n_eligible_t1": None, "n_eligible_t2": None,
        }

    # Re-compute correlations on live-brands-only dataset (excludes phantoms)
    live_corr_t1 = correlations(df_cat, "ww", "t1", exclude_phantoms=True)
    live_corr_t2 = correlations(df_cat, "ww", "t2", exclude_phantoms=True)

    bivar_t1 = live_corr_t1.get("spearman_rho")
    bivar_t2 = live_corr_t2.get("spearman_rho")
    partial_t1 = live_corr_t1.get("partial_spearman_rho")
    partial_t2 = live_corr_t2.get("partial_spearman_rho")
    n_t1 = live_corr_t1.get("n", 0)
    n_t2 = live_corr_t2.get("n", 0)

    if any(v is None for v in (bivar_t1, bivar_t2, partial_t1, partial_t2)):
        return {
            "applicable": True,
            "regime_class": "Unclassifiable (insufficient n)",
            "boundary_flag": False,
            "unclassifiable_flag": True,
            "rationale": f"n_t1={n_t1}, n_t2={n_t2}; cannot compute ρ.",
            "bivariate_rho_t1": bivar_t1, "bivariate_rho_t2": bivar_t2,
            "partial_rho_t1":   partial_t1, "partial_rho_t2":   partial_t2,
            "decrement_t1":     None, "decrement_t2":     None,
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

    # Boundary detection: within H7_BOUNDARY_TOLERANCE of any threshold
    tol = H7_BOUNDARY_TOLERANCE
    near_r1_lower = (abs(bivar_t1 - H7_R1_RHO_MIN) <= tol or
                     abs(bivar_t2 - H7_R1_RHO_MIN) <= tol)
    near_r1_upper = (abs(bivar_t1 - H7_R1_RHO_MAX) <= tol or
                     abs(bivar_t2 - H7_R1_RHO_MAX) <= tol)
    near_r2_lower = (abs(bivar_t1 - H7_R2_RHO_MIN) <= tol or
                     abs(bivar_t2 - H7_R2_RHO_MIN) <= tol)
    near_decrement_r1 = (abs(decrement_t1 - H7_R1_DECREMENT_MAX) <= tol or
                         abs(decrement_t2 - H7_R1_DECREMENT_MAX) <= tol)
    near_decrement_r2 = (abs(decrement_t1 - H7_R2_DECREMENT_MIN) <= tol or
                         abs(decrement_t2 - H7_R2_DECREMENT_MIN) <= tol)
    boundary_flag = (near_r1_lower or near_r1_upper or near_r2_lower or
                     near_decrement_r1 or near_decrement_r2)

    if is_regime_1 and is_regime_2:
        return {
            "applicable": True,
            "regime_class": "Unclassifiable (matches Regimes 1 and 2)",
            "boundary_flag": boundary_flag,
            "unclassifiable_flag": True,
            "rationale": "Satisfies both Regime 1 and Regime 2 criteria simultaneously.",
            "bivariate_rho_t1": bivar_t1, "bivariate_rho_t2": bivar_t2,
            "partial_rho_t1":   partial_t1, "partial_rho_t2":   partial_t2,
            "decrement_t1":     decrement_t1, "decrement_t2":     decrement_t2,
            "n_eligible_t1": n_t1, "n_eligible_t2": n_t2,
        }
    if is_regime_1:
        regime = "Regime 1 (Marginal direct)"
    elif is_regime_2:
        regime = "Regime 2 (Age-mediated strong)"
    else:
        regime = "Unclassifiable (matches neither Regime 1 nor 2)"

    return {
        "applicable": True,
        "regime_class": regime,
        "boundary_flag": boundary_flag,
        "unclassifiable_flag": regime.startswith("Unclassifiable"),
        "rationale": (f"ρ_t1={bivar_t1:.3f}, ρ_t2={bivar_t2:.3f}, "
                      f"partial_ρ_t1={partial_t1:.3f}, partial_ρ_t2={partial_t2:.3f}, "
                      f"Δ_t1={decrement_t1:.3f}, Δ_t2={decrement_t2:.3f}, "
                      f"n_t1={n_t1}, n_t2={n_t2}."),
        "bivariate_rho_t1": bivar_t1, "bivariate_rho_t2": bivar_t2,
        "partial_rho_t1":   partial_t1, "partial_rho_t2":   partial_t2,
        "decrement_t1":     decrement_t1, "decrement_t2":     decrement_t2,
        "n_eligible_t1": n_t1, "n_eligible_t2": n_t2,
    }


h7_per_cat = {}
for cat in CATEGORIES:
    df_cat = paired_all[paired_all["category"] == cat].copy()
    h7_per_cat[cat] = h7_classify_category(cat, df_cat, all_results[cat])

# H7 confirmation: every category classifies cleanly (not unclassifiable, not boundary)
n_clean = sum(1 for c, v in h7_per_cat.items()
              if v["applicable"] and not v["unclassifiable_flag"] and not v["boundary_flag"])
n_applicable = sum(1 for v in h7_per_cat.values() if v["applicable"])
# Olive oil is descriptive-only but pre-reg §2 H7 specifies "every v0.13 category
# classifies cleanly". Descriptive-only counts as Regime 3 (clean).
n_clean_inclusive = sum(1 for c, v in h7_per_cat.items()
                        if not v["unclassifiable_flag"] and not v["boundary_flag"])

h7_status = "CONFIRMED" if n_clean_inclusive == len(CATEGORIES) else "FALSIFIED"
h7_result = {
    "status": h7_status,
    "n_clean": n_clean_inclusive,
    "n_total_categories": len(CATEGORIES),
    "per_category": h7_per_cat,
    "rationale": (f"{n_clean_inclusive} of {len(CATEGORIES)} categories classify "
                  f"cleanly (not unclassifiable, not boundary); H7 requires all 5."),
}

# Write h7_regime_classification.csv
h7_rows = []
for cat, v in h7_per_cat.items():
    h7_rows.append({
        "category":              cat,
        "applicable":            v["applicable"],
        "regime_class":          v["regime_class"],
        "boundary_flag":         v["boundary_flag"],
        "unclassifiable_flag":   v["unclassifiable_flag"],
        "bivariate_rho_t1":      v.get("bivariate_rho_t1"),
        "bivariate_rho_t2":      v.get("bivariate_rho_t2"),
        "partial_rho_t1":        v.get("partial_rho_t1"),
        "partial_rho_t2":        v.get("partial_rho_t2"),
        "decrement_t1":          v.get("decrement_t1"),
        "decrement_t2":          v.get("decrement_t2"),
        "n_eligible_t1":         v.get("n_eligible_t1"),
        "n_eligible_t2":         v.get("n_eligible_t2"),
        "rationale":             v["rationale"],
    })
h7_path = OUT_DIR / "h7_regime_classification.csv"
pd.DataFrame(h7_rows).to_csv(h7_path, index=False)

print("=" * 80)
print(f"H7 (Three-regimes accounting, clean classification): {h7_status}")
print("=" * 80)
for cat, v in h7_per_cat.items():
    marker = "✓" if (not v["unclassifiable_flag"] and not v["boundary_flag"]) else "✗"
    print(f"  {marker} {cat:<12}  {v['regime_class']}")
    if v["boundary_flag"]:
        print(f"      (boundary flag — within {H7_BOUNDARY_TOLERANCE} of a regime threshold)")
print()

# ============================================================================
# Step 10: H8 — Mint phantom-persistence diagnostic (NEW per pre-reg §2 H8)
# ============================================================================

def evaluate_h8(paired_all):
    """Mint phantom-persistence three-condition diagnostic per pre-reg §2 H8."""
    finance_df = paired_all[paired_all["category"] == "finance"].copy()
    if not (finance_df["brand"] == "Mint").any():
        return {"status": "INDETERMINATE",
                "rationale": "Mint not in finance brand registry."}

    mint_row = finance_df[finance_df["brand"] == "Mint"].iloc[0]
    ai_t1 = float(mint_row["ai_t1_pct"])
    ai_t2 = float(mint_row["ai_t2_pct"])

    # Condition 1: Mint AI Presence >= 5% at BOTH waves
    cond1 = (ai_t1 >= H8_AI_FLOOR_PCT) and (ai_t2 >= H8_AI_FLOOR_PCT)

    # Condition 2: Mint top-5 by AI Presence at BOTH waves
    sorted_t1 = finance_df.sort_values("ai_t1_pct", ascending=False).reset_index(drop=True)
    sorted_t2 = finance_df.sort_values("ai_t2_pct", ascending=False).reset_index(drop=True)
    mint_ai_rank_t1 = int(sorted_t1[sorted_t1["brand"] == "Mint"].index[0]) + 1
    mint_ai_rank_t2 = int(sorted_t2[sorted_t2["brand"] == "Mint"].index[0]) + 1
    cond2 = (mint_ai_rank_t1 <= H8_TOP_K_AI) and (mint_ai_rank_t2 <= H8_TOP_K_AI)

    # Condition 3: Mint NOT top-5 by Trends (worldwide) at EITHER wave.
    # Per pre-reg §11: if Mint not eligible (no Trends signal), trivially satisfied.
    elig_t1 = finance_df[finance_df["trends_ww_t1_eligible"]].dropna(
        subset=["trends_ww_t1_mean"]).sort_values(
        "trends_ww_t1_mean", ascending=False).reset_index(drop=True)
    elig_t2 = finance_df[finance_df["trends_ww_t2_eligible"]].dropna(
        subset=["trends_ww_t2_mean"]).sort_values(
        "trends_ww_t2_mean", ascending=False).reset_index(drop=True)

    if (elig_t1["brand"] == "Mint").any():
        mint_tr_rank_t1 = int(elig_t1[elig_t1["brand"] == "Mint"].index[0]) + 1
        cond3_t1 = mint_tr_rank_t1 > H8_TOP_K_TRENDS
        cond3_t1_basis = f"Mint rank {mint_tr_rank_t1} in Trends t1"
    else:
        mint_tr_rank_t1 = None
        cond3_t1 = True
        cond3_t1_basis = "Mint not E1b-eligible at t1 (trivially satisfied per §11)"

    if (elig_t2["brand"] == "Mint").any():
        mint_tr_rank_t2 = int(elig_t2[elig_t2["brand"] == "Mint"].index[0]) + 1
        cond3_t2 = mint_tr_rank_t2 > H8_TOP_K_TRENDS
        cond3_t2_basis = f"Mint rank {mint_tr_rank_t2} in Trends t2"
    else:
        mint_tr_rank_t2 = None
        cond3_t2 = True
        cond3_t2_basis = "Mint not E1b-eligible at t2 (trivially satisfied per §11)"

    cond3 = cond3_t1 and cond3_t2

    status = "CONFIRMED" if (cond1 and cond2 and cond3) else "FALSIFIED"
    return {
        "status": status,
        "condition_1_ai_above_5pct": {
            "ai_t1_pct": ai_t1, "ai_t2_pct": ai_t2,
            "threshold": H8_AI_FLOOR_PCT, "satisfied": cond1,
        },
        "condition_2_ai_top5": {
            "rank_t1": mint_ai_rank_t1, "rank_t2": mint_ai_rank_t2,
            "threshold_k": H8_TOP_K_AI, "satisfied": cond2,
        },
        "condition_3_trends_not_top5": {
            "rank_t1": mint_tr_rank_t1, "rank_t2": mint_tr_rank_t2,
            "basis_t1": cond3_t1_basis, "basis_t2": cond3_t2_basis,
            "threshold_k": H8_TOP_K_TRENDS, "satisfied": cond3,
        },
        "rationale": (f"Cond1 (AI≥5% both waves): {cond1}. "
                      f"Cond2 (AI top-5 both waves): {cond2}. "
                      f"Cond3 (NOT Trends top-5 either wave): {cond3}. "
                      f"All three required for CONFIRMED."),
    }


h8 = evaluate_h8(paired_all)

# Write h8_mint_diagnostic.csv
h8_rows = [{
    "metric": "AI Presence t1",
    "value": h8["condition_1_ai_above_5pct"].get("ai_t1_pct"),
    "threshold": f">={H8_AI_FLOOR_PCT}%",
    "condition": "C1", "satisfied": h8["condition_1_ai_above_5pct"]["satisfied"],
}, {
    "metric": "AI Presence t2",
    "value": h8["condition_1_ai_above_5pct"].get("ai_t2_pct"),
    "threshold": f">={H8_AI_FLOOR_PCT}%",
    "condition": "C1", "satisfied": h8["condition_1_ai_above_5pct"]["satisfied"],
}, {
    "metric": "AI rank t1",
    "value": h8["condition_2_ai_top5"].get("rank_t1"),
    "threshold": f"<={H8_TOP_K_AI}",
    "condition": "C2", "satisfied": h8["condition_2_ai_top5"]["satisfied"],
}, {
    "metric": "AI rank t2",
    "value": h8["condition_2_ai_top5"].get("rank_t2"),
    "threshold": f"<={H8_TOP_K_AI}",
    "condition": "C2", "satisfied": h8["condition_2_ai_top5"]["satisfied"],
}, {
    "metric": "Trends rank t1",
    "value": h8["condition_3_trends_not_top5"].get("rank_t1"),
    "threshold": f">{H8_TOP_K_TRENDS} OR not eligible",
    "condition": "C3", "satisfied": h8["condition_3_trends_not_top5"]["satisfied"],
}, {
    "metric": "Trends rank t2",
    "value": h8["condition_3_trends_not_top5"].get("rank_t2"),
    "threshold": f">{H8_TOP_K_TRENDS} OR not eligible",
    "condition": "C3", "satisfied": h8["condition_3_trends_not_top5"]["satisfied"],
}]
h8_path = OUT_DIR / "h8_mint_diagnostic.csv"
pd.DataFrame(h8_rows).to_csv(h8_path, index=False)

print("=" * 80)
print(f"H8 (Mint phantom-persistence three-condition diagnostic): {h8['status']}")
print("=" * 80)
print(f"  C1 (AI ≥ {H8_AI_FLOOR_PCT}% both waves): "
      f"t1={h8['condition_1_ai_above_5pct']['ai_t1_pct']:.1f}%, "
      f"t2={h8['condition_1_ai_above_5pct']['ai_t2_pct']:.1f}% "
      f"→ {h8['condition_1_ai_above_5pct']['satisfied']}")
print(f"  C2 (AI top-{H8_TOP_K_AI} both waves): "
      f"rank_t1={h8['condition_2_ai_top5']['rank_t1']}, "
      f"rank_t2={h8['condition_2_ai_top5']['rank_t2']} "
      f"→ {h8['condition_2_ai_top5']['satisfied']}")
print(f"  C3 (NOT Trends top-{H8_TOP_K_TRENDS} either wave): "
      f"t1={h8['condition_3_trends_not_top5']['basis_t1']}; "
      f"t2={h8['condition_3_trends_not_top5']['basis_t2']} "
      f"→ {h8['condition_3_trends_not_top5']['satisfied']}")
print()

# ============================================================================
# Step 11: Category-Scale Mismatch table (olive oil; inherited from v0.12)
# ============================================================================

mismatch_rows = []
OLIVEOIL_MATCHED_SUBSET = {
    "California Olive Ranch", "Bertolli", "Cobram Estate",
    "Brightland", "Castillo de Canena", "Frantoio Muraglia",
    "Frescobaldi Laudemio", "Graza", "Kosterina", "Lucini",
    "Manni", "McEvoy Ranch", "Núñez de Prado", "Olio Verde", "Colonna",
}

for _, row in paired_all[paired_all["category"] == "oliveoil"].iterrows():
    brand = row["brand"]
    if brand not in OLIVEOIL_MATCHED_SUBSET:
        continue
    ai_t1 = row["ai_t1_pct"]
    ai_t2 = row["ai_t2_pct"]
    e1a   = row["e1a_excluded"]
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

n_scale_mismatch = sum(1 for r in mismatch_rows if r["scale_mismatch_case"])
n_total = len(mismatch_rows)

print("=" * 80)
print(f"CATEGORY-SCALE MISMATCH FINDING — OLIVE OIL "
      f"({n_scale_mismatch}/{n_total} = "
      f"{100*n_scale_mismatch/n_total:.1f}%)")
print("=" * 80)
print()

# ============================================================================
# Step 12: Pooled sensitivity ρ (rank-within-category, across confirmatory cats)
# ============================================================================

pooled_rows = {"t1": [], "t2": []}
for cat in [c for c in CATEGORIES if not CATEGORIES[c]["descriptive_only"]]:
    cat_df = paired_all[(paired_all["category"] == cat) & (~paired_all["e1a_excluded"])].copy()
    for wave in ("t1", "t2"):
        elig = cat_df[cat_df[f"trends_ww_{wave}_eligible"]].copy()
        elig = elig.dropna(subset=[f"trends_ww_{wave}_mean", f"ai_{wave}_pct"])
        if len(elig) > 1:
            elig["ai_rank"]     = stats.rankdata(elig[f"ai_{wave}_pct"])
            elig["trends_rank"] = stats.rankdata(elig[f"trends_ww_{wave}_mean"])
            for _, row in elig.iterrows():
                pooled_rows[wave].append({
                    "category": cat, "brand": row["brand"],
                    "ai_rank": row["ai_rank"], "trends_rank": row["trends_rank"],
                })

pooled_results = {}
for wave in ("t1", "t2"):
    if len(pooled_rows[wave]) > 4:
        ai_ranks = np.array([r["ai_rank"] for r in pooled_rows[wave]])
        tr_ranks = np.array([r["trends_rank"] for r in pooled_rows[wave]])
        rho, p = stats.spearmanr(ai_ranks, tr_ranks)
        pooled_results[wave] = {"n": len(pooled_rows[wave]), "rho": float(rho), "p_two_tailed": float(p)}
        print(f"  Pooled {wave}: n={len(pooled_rows[wave])}  ρ={rho:.3f}  p={p:.4f}")
    else:
        pooled_results[wave] = {"n": len(pooled_rows[wave]), "rho": None, "p_two_tailed": None}
print()

# ============================================================================
# Step 13: Write canonical scoring outputs
# ============================================================================

canonical = {
    "meta": {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "v0_13_prereg_tag": "v0.13-prereg",
        "matched_models": sorted(MATCHED_MODELS),
        "n_responses_per_category_per_wave": n_responses,
        "e1a_exclusions": {cat: sorted(brands) for cat, brands in e1a_by_cat.items()},
    },
    "per_category": all_results,
    "cross_category": {
        "H5": h5,
        "H6": h6,
        "H7": h7_result,
        "H8": h8,
        "per_category_marginal_signature": per_cat_sig,
    },
    "pooled_sensitivity": pooled_results,
    "category_scale_mismatch_olive_oil": {
        "n_scale_mismatch": n_scale_mismatch,
        "n_total": n_total,
        "scale_mismatch_index_pct": round(100 * n_scale_mismatch / n_total, 1) if n_total else None,
        "table_path": str(mismatch_path.relative_to(V13_ROOT)),
    },
}

(OUT_DIR / "canonical_scoring.json").write_text(
    json.dumps(canonical, indent=2, default=str))
print(f"Canonical scoring (JSON): {OUT_DIR / 'canonical_scoring.json'}")

with (OUT_DIR / "canonical_scoring.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["scope", "hypothesis", "status", "rationale"])
    w.writeheader()
    for cat in CATEGORIES:
        cat_res = all_results[cat]
        if cat_res["descriptive_only"]:
            w.writerow({"scope": cat, "hypothesis": "H1-H4",
                        "status": "INDETERMINATE",
                        "rationale": "Descriptive-only per pre-reg §3.6a (n-floor breached)"})
        else:
            for hn, hd in cat_res["hypotheses"].items():
                w.writerow({"scope": cat, "hypothesis": hn,
                            "status": hd.get("status"),
                            "rationale": str(hd.get("rationale", ""))[:300]})
    w.writerow({"scope": "cross_category", "hypothesis": "H5",
                "status": h5["status"], "rationale": h5["rationale"]})
    w.writerow({"scope": "cross_category", "hypothesis": "H6",
                "status": h6["status"], "rationale": h6["rationale"]})
    w.writerow({"scope": "cross_category", "hypothesis": "H7",
                "status": h7_result["status"], "rationale": h7_result["rationale"]})
    w.writerow({"scope": "finance", "hypothesis": "H8",
                "status": h8["status"], "rationale": h8["rationale"]})

print(f"Canonical scoring (CSV):       {OUT_DIR / 'canonical_scoring.csv'}")
print(f"Category-Scale Mismatch table: {mismatch_path}")
print(f"H7 regime classification:      {h7_path}")
print(f"H8 Mint diagnostic:            {h8_path}")
print()
print("Scoring complete.")
