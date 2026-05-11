"""v0.11 Hypothesis evaluation: H1-H4 against pre-reg thresholds.

Inputs:
  - ~/aias/osf_staging/v09/data/pm/results_enriched_v06_*.csv  (t1 source)
  - ~/aias/osf_staging/v09/data/pm/results_enriched_v09_*.csv  (t2 source)
  - ~/aias/osf/v11/data/trends_processed/per_brand_within_window.csv
  - ~/aias/osf/v11/registries/brand_age_sources.csv
  - ~/aias/osf/v11/registries/brands_pm.json

Outputs:
  - ~/aias/osf/v11/analysis/per_brand_paired.csv
  - ~/aias/osf/v11/analysis/canonical_scoring.csv
  - ~/aias/osf/v11/analysis/canonical_scoring.json

Key conventions:
  - Pre-reg sec.5.1 pivot exemption applied: Asana eligible despite Trends sd=0.
  - Pre-acquisition exclusions (E1a) removed before analysis: Shortcut.
  - At-acquisition exclusions (E1b) per-wave from per_brand_within_window.csv.
  - Partial Spearman computed as Pearson on rank residuals after OLS on
    rank-transformed covariates; df corrected by k=2 covariates.

Run:
    python scripts/score_v11.py
"""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# ============================================================================
# Configuration
# ============================================================================

V11_ROOT = Path.home() / "aias" / "osf" / "v11"
V09_DATA = Path.home() / "aias" / "osf_staging" / "v09" / "data" / "pm"

V06_FILE = V09_DATA / "results_enriched_v06_20260507_181205.csv"
V09_FILE = V09_DATA / "results_enriched_v09_20260507_181205.csv"
TRENDS_FILE = V11_ROOT / "data" / "trends_processed" / "per_brand_within_window.csv"
AGE_FILE = V11_ROOT / "registries" / "brand_age_sources.csv"
REGISTRY_FILE = V11_ROOT / "registries" / "brands_pm.json"

OUT_DIR = V11_ROOT / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MATCHED_MODELS = {"claude-sonnet-4-6", "gpt-5.4-mini"}
PRE_ACQUISITION_EXCLUSIONS = {"Shortcut"}
PIVOT_BRAND = "Asana"

H1_RHO_THRESHOLD = 0.5
H1_P_THRESHOLD = 0.05
H2_DELTA_THRESHOLD = 0.15
H3_TOP_K_AI = 3
H3_TOP_K_TRENDS = 5
H4_RHO_THRESHOLD = 0.5
H4_P_THRESHOLD = 0.05
N_FLOOR = 16

TIER_ORDINAL = {"incumbent": 1, "mid-tier": 2, "challenger": 3}

# ============================================================================
# Step 1: Load registry, define analysis brand set
# ============================================================================

with REGISTRY_FILE.open() as f:
    registry = json.load(f)

analysis_brands = [b["canonical"] for b in registry
                   if b["canonical"] not in PRE_ACQUISITION_EXCLUSIONS]
brand_tier = {b["canonical"]: b["tier"] for b in registry}

print(f"Registry: {len(registry)} brands; "
      f"{len(analysis_brands)} after E1a exclusions")
print(f"  E1a excluded: {sorted(PRE_ACQUISITION_EXCLUSIONS)}")
print()

# ============================================================================
# Step 2: Compute AI Presence rates per brand per wave
# ============================================================================

def compute_presence(csv_path):
    df = pd.read_csv(csv_path)
    print(f"  {csv_path.name}: {len(df)} rows total")
    df = df[df["model_version"].isin(MATCHED_MODELS)]
    df = df[df["call_status"] == "ok"]
    n = len(df)
    print(f"  matched-subset (Sonnet+mini, ok): {n} responses")
    presence = {}
    for b in [r["canonical"] for r in registry]:
        def hit(s):
            if pd.isna(s):
                return False
            return b in str(s).split("|")
        c = int(df["brands_canonical"].apply(hit).sum())
        presence[b] = round(100.0 * c / n, 2) if n else 0.0
    return presence, n

print("Computing AI Presence...")
print("t1 (v06):")
ai_t1, n_resp_t1 = compute_presence(V06_FILE)
print("t2 (v09):")
ai_t2, n_resp_t2 = compute_presence(V09_FILE)
print()

print("Top 10 by AI Presence at t1:")
for b, r in sorted(ai_t1.items(), key=lambda x: -x[1])[:10]:
    print(f"  {b:<20} {r:>6.1f}%")
print()
print("Top 10 by AI Presence at t2:")
for b, r in sorted(ai_t2.items(), key=lambda x: -x[1])[:10]:
    print(f"  {b:<20} {r:>6.1f}%")
print()

# ============================================================================
# Step 3: Load Trends data + ages, build paired dataset
# ============================================================================

trends_df = pd.read_csv(TRENDS_FILE)
trends_ww = trends_df[trends_df["region"] == "worldwide"].set_index("brand")
trends_us = trends_df[trends_df["region"] == "US"].set_index("brand")

age_df = pd.read_csv(AGE_FILE)
age_map = dict(zip(age_df["brand_canonical"], age_df["brand_age_years"]))

records = []
for b in analysis_brands:
    rec = {
        "brand": b,
        "market_tier": brand_tier[b],
        "tier_ordinal": TIER_ORDINAL[brand_tier[b]],
        "brand_age_years": age_map.get(b),
        "ai_t1_pct": ai_t1.get(b, 0.0),
        "ai_t2_pct": ai_t2.get(b, 0.0),
    }
    for label, src in [("ww", trends_ww), ("us", trends_us)]:
        if b in src.index:
            row = src.loc[b]
            for w in ("t1", "t2"):
                rec[f"trends_{label}_{w}_mean"] = float(row[f"{w}_mean"]) if pd.notna(row[f"{w}_mean"]) else None
                rec[f"trends_{label}_{w}_eligible"] = bool(row[f"{w}_eligible_E1b"])
                rec[f"trends_{label}_{w}_sparse"] = bool(row[f"{w}_sparse_E5"])
        else:
            for w in ("t1", "t2"):
                rec[f"trends_{label}_{w}_mean"] = None
                rec[f"trends_{label}_{w}_eligible"] = False
                rec[f"trends_{label}_{w}_sparse"] = False
    # Pivot exemption sec.5.1.
    if b == PIVOT_BRAND:
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
# Step 4: Compute correlations per wave per region
# ============================================================================

def correlations(df, region, wave):
    elig = df[df[f"trends_{region}_{wave}_eligible"]].copy()
    elig = elig.dropna(subset=[f"trends_{region}_{wave}_mean", f"ai_{wave}_pct",
                                "brand_age_years", "tier_ordinal"])
    n = len(elig)
    out = {"n": n, "brands": list(elig["brand"])}
    if n < 4:
        for k in ("spearman_rho", "spearman_p_two_tailed",
                  "spearman_p_one_tailed", "pearson_r",
                  "pearson_p_two_tailed", "pearson_p_one_tailed",
                  "partial_spearman_rho",
                  "partial_spearman_p_one_tailed"):
            out[k] = None
        return out

    x = elig[f"ai_{wave}_pct"].values.astype(float)
    y = elig[f"trends_{region}_{wave}_mean"].values.astype(float)

    rho, p_rho = stats.spearmanr(x, y)
    p_rho_1t = p_rho / 2 if rho > 0 else 1 - p_rho / 2

    r, p_r = stats.pearsonr(x, y)
    p_r_1t = p_r / 2 if r > 0 else 1 - p_r / 2

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
    df_adj = n - 2 - 2  # 2 covariates
    if df_adj > 0 and abs(pr) < 1:
        t_stat = pr * np.sqrt(df_adj / (1 - pr ** 2))
        partial_p_1t = float(1 - stats.t.cdf(t_stat, df=df_adj))
    else:
        partial_p_1t = float("nan")

    out.update({
        "spearman_rho": float(rho),
        "spearman_p_two_tailed": float(p_rho),
        "spearman_p_one_tailed": float(p_rho_1t),
        "pearson_r": float(r),
        "pearson_p_two_tailed": float(p_r),
        "pearson_p_one_tailed": float(p_r_1t),
        "partial_spearman_rho": float(pr),
        "partial_spearman_p_one_tailed": partial_p_1t,
    })
    return out

print("Correlations:")
results = {}
for region in ("ww", "us"):
    rname = "worldwide" if region == "ww" else "US"
    for wave in ("t1", "t2"):
        key = f"{region}_{wave}"
        results[key] = correlations(paired, region, wave)
        r = results[key]
        if r["spearman_rho"] is None:
            print(f"  {rname} {wave}: n={r['n']} (insufficient)")
        else:
            print(f"  {rname} {wave}: n={r['n']}  ρ={r['spearman_rho']:.3f}  "
                  f"p1t={r['spearman_p_one_tailed']:.4f}  "
                  f"r={r['pearson_r']:.3f}  partial_ρ={r['partial_spearman_rho']:.3f}")
print()

# ============================================================================
# Step 5: Hypothesis evaluation
# ============================================================================

def eval_h1_or_h4(t1, t2, thr_rho, thr_p, key_rho, key_p, label):
    if t1["n"] < N_FLOOR or t2["n"] < N_FLOOR:
        return {
            "status": "INDETERMINATE",
            "rationale": f"n-floor breached: t1 n={t1['n']}, t2 n={t2['n']} (floor={N_FLOOR})",
            "threshold_rho": thr_rho, "threshold_p": thr_p,
            f"{label}_t1": t1[key_rho], f"{label}_t2": t2[key_rho],
            "p_t1_one_tailed": t1[key_p], "p_t2_one_tailed": t2[key_p],
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
    if t1["n"] < N_FLOOR or t2["n"] < N_FLOOR:
        return {"status": "INDETERMINATE",
                "rationale": f"n-floor breached"}
    rho1, rho2 = t1["spearman_rho"], t2["spearman_rho"]
    delta = abs(rho2 - rho1)
    return {
        "status": "CONFIRMED" if delta <= H2_DELTA_THRESHOLD else "FALSIFIED",
        "rho_t1": rho1, "rho_t2": rho2, "abs_delta_rho": delta,
        "threshold": H2_DELTA_THRESHOLD,
        "rationale": (
            f"|Δρ| = |{rho2:.3f} − {rho1:.3f}| = {delta:.3f} "
            f"{'≤' if delta <= H2_DELTA_THRESHOLD else '>'} {H2_DELTA_THRESHOLD}"
        ),
    }

def eval_h3(df, region):
    out = {"per_wave": {}, "status_per_wave": {}}
    pass_both = True
    for wave in ("t1", "t2"):
        e = df[df[f"trends_{region}_{wave}_eligible"]].copy()
        e = e.dropna(subset=[f"trends_{region}_{wave}_mean", f"ai_{wave}_pct"])
        top3_ai = list(e.sort_values(f"ai_{wave}_pct", ascending=False)
                        .head(H3_TOP_K_AI)["brand"])
        top5_t = list(e.sort_values(f"trends_{region}_{wave}_mean", ascending=False)
                       .head(H3_TOP_K_TRENDS)["brand"])
        in5 = [b for b in top3_ai if b in top5_t]
        out["per_wave"][wave] = {
            "top3_ai": top3_ai,
            "top5_trends": top5_t,
            "top3_in_top5": in5,
            "n_in_top5": len(in5),
        }
        ws = "CONFIRMED" if len(in5) == H3_TOP_K_AI else "FALSIFIED"
        out["status_per_wave"][wave] = ws
        if ws != "CONFIRMED":
            pass_both = False
    out["status"] = "CONFIRMED" if pass_both else "FALSIFIED"
    return out

h1 = eval_h1_or_h4(results["ww_t1"], results["ww_t2"],
                   H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                   "spearman_rho", "spearman_p_one_tailed", "rho")
h2 = eval_h2(results["ww_t1"], results["ww_t2"])
h3 = eval_h3(paired, "ww")
h4 = eval_h1_or_h4(results["ww_t1"], results["ww_t2"],
                   H4_RHO_THRESHOLD, H4_P_THRESHOLD,
                   "partial_spearman_rho", "partial_spearman_p_one_tailed",
                   "partial_rho")
h1_us = eval_h1_or_h4(results["us_t1"], results["us_t2"],
                       H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                       "spearman_rho", "spearman_p_one_tailed", "rho")
h1_pearson = eval_h1_or_h4(results["ww_t1"], results["ww_t2"],
                            H1_RHO_THRESHOLD, H1_P_THRESHOLD,
                            "pearson_r", "pearson_p_one_tailed", "r")

# ============================================================================
# Print summary
# ============================================================================

print("=" * 76)
print("HYPOTHESIS EVALUATION (Worldwide primary)")
print("=" * 76)
print(f"H1 — Cross-sectional construct validity: {h1['status']}")
print(f"   {h1['rationale']}")
print()
print(f"H2 — Correlation stability: {h2['status']}")
print(f"   {h2['rationale']}")
print()
print(f"H3 — Leaderboard top-3 ⊆ top-5: {h3['status']}")
for wave in ("t1", "t2"):
    pw = h3["per_wave"][wave]
    print(f"   {wave}: AI top-3 = {pw['top3_ai']}")
    print(f"        Trends top-5 = {pw['top5_trends']}")
    print(f"        in top-5 = {pw['n_in_top5']}/3")
print()
print(f"H4 — Covariate-controlled: {h4['status']}")
print(f"   {h4['rationale']}")
print()
print("Sensitivities:")
print(f"  H1 US-only:  {h1_us['status']}")
print(f"  H1 Pearson:  {h1_pearson['status']}")
print()

# ============================================================================
# Output canonical scoring
# ============================================================================

canonical = {
    "meta": {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "v0_11_prereg_lock_commit": "f20ade8",
        "n_brands_in_registry": len(registry),
        "n_brands_after_e1a": len(analysis_brands),
        "pivot_brand": PIVOT_BRAND,
        "ai_presence_source": {
            "t1_file": str(V06_FILE.name),
            "t2_file": str(V09_FILE.name),
            "matched_models": sorted(MATCHED_MODELS),
            "n_responses_t1": n_resp_t1,
            "n_responses_t2": n_resp_t2,
        },
    },
    "n_floor": {
        "threshold": N_FLOOR,
        "ww_t1": results["ww_t1"]["n"],
        "ww_t2": results["ww_t2"]["n"],
        "us_t1": results["us_t1"]["n"],
        "us_t2": results["us_t2"]["n"],
        "ww_t1_pass": results["ww_t1"]["n"] >= N_FLOOR,
        "ww_t2_pass": results["ww_t2"]["n"] >= N_FLOOR,
    },
    "correlations": {
        k: {kk: vv for kk, vv in v.items() if kk != "brands"}
        for k, v in results.items()
    },
    "brands_per_wave": {k: v["brands"] for k, v in results.items()},
    "hypotheses": {
        "H1_primary": h1, "H2": h2, "H3": h3, "H4": h4,
        "H1_us_sensitivity": h1_us, "H1_pearson_sensitivity": h1_pearson,
    },
}

(OUT_DIR / "canonical_scoring.json").write_text(
    json.dumps(canonical, indent=2, default=str))
print(f"Canonical scoring (JSON): {OUT_DIR / 'canonical_scoring.json'}")

with (OUT_DIR / "canonical_scoring.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["hypothesis", "status", "rationale"])
    w.writeheader()
    for hn, hd in canonical["hypotheses"].items():
        w.writerow({"hypothesis": hn, "status": hd.get("status"),
                    "rationale": hd.get("rationale", "")[:300]})
print(f"Canonical scoring (CSV):  {OUT_DIR / 'canonical_scoring.csv'}")
