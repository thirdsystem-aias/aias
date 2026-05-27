"""
v0.25 — B2B SaaS Construct Validity
Pre-Registration Content Module

Predictive Validity of AI Presence Index Against Google Trends
Search Interest on the B2B SaaS Substrate.

Input data: v0.24 B2B SaaS (SSRN 6838802), Protocol v1.6.
External validator: Google Trends search-interest index via SerpAPI.
"""

# ---------------------------------------------------------------------------
# Study identity
# ---------------------------------------------------------------------------

STUDY_ID = "v0.25"
STUDY_TITLE = (
    "Predictive Validity of AI Presence Index Against Google Trends "
    "Search Interest on the B2B SaaS Substrate"
)
STUDY_SUBTITLE = "Construct Validity Pilot Under Protocol v1.6"
DESIGNED_FOR_TEST = "Construct Validity (Convergent + Discriminant)"
INPUT_DATA_SOURCE = "v0.24 B2B SaaS (SSRN 6838802)"
PROTOCOL_VERSION = "v1.6"
EXTERNAL_VALIDATOR = "Google Trends search-interest index (0-100 normalized)"
ACQUISITION_ENGINE = "SerpAPI Google Trends"

# ---------------------------------------------------------------------------
# Registry — inherited verbatim from v0.24
# ---------------------------------------------------------------------------

REGISTRY = {
    "Cell_A_Enterprise_Incumbents": [
        "Slack", "Salesforce", "HubSpot", "Workday", "SAP", "Oracle",
    ],
    "Cell_B_High_Identity_Challengers": [
        "Notion", "Figma", "Linear", "Airtable", "Miro", "Cloudflare",
    ],
    "Cell_C_Infrastructure_Dev_Platform": [
        "ServiceNow", "Snowflake", "Zendesk", "Datadog", "Stripe",
        "MongoDB", "Twilio",
    ],
    "Cell_D_Phantom_Defunct": [
        "Quip", "Yammer", "Wunderlist", "HipChat", "Stride",
    ],
}

BRAND_COUNT = 24  # 6 + 6 + 7 + 5
PIVOT_BRAND = "Salesforce"  # appears in every Trends query bundle

# ---------------------------------------------------------------------------
# Google Trends design parameters
# ---------------------------------------------------------------------------

TRENDS_GEOGRAPHY = "US"
TRENDS_WINDOW_DAYS = 7  # 7-day window contemporaneous with v0.24 acquisition
# Actual dates locked at pre-reg commit after confirming v0.24 timestamps:
TRENDS_WINDOW_START = "PENDING_LOCK"  # e.g. "2026-05-19"
TRENDS_WINDOW_END = "PENDING_LOCK"    # e.g. "2026-05-25"

TRENDS_BUNDLE_SIZE = 5  # Google Trends comparison limit
# Bundling: pivot brand (Salesforce) appears in every bundle.
# 23 remaining brands across 6 bundles of 3-4 brands + pivot = 5 per bundle.
TRENDS_BUNDLE_COUNT = 6

TRENDS_VALIDATION_WINDOW = "PENDING_LOCK"  # 7-day OOS window, 1 week prior

BOOTSTRAP_N = 10_000
BOOTSTRAP_METHOD = "BCa"  # bias-corrected accelerated
# Seed: pre-reg commit hash truncated to 32-bit integer
BOOTSTRAP_SEED = "PENDING_LOCK"  # set at commit time

# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------

HYPOTHESES = {
    "H_CV_Primary": {
        "label": "Convergent validity (composite)",
        "description": (
            "Brand-level AIAS Presence composite and Google Trends search "
            "interest are positively rank-correlated across all 24 brands."
        ),
        "statistic": "Spearman rho, 95% BCa bootstrap CI (10,000 resamples)",
        "threshold_confirmed": "CI_lower > 0",
        "threshold_partial": "point estimate > 0 but CI includes zero",
        "threshold_falsified": "point estimate <= 0",
        "prediction": "CONFIRMED",
        "prediction_rationale": (
            "Brands that LLMs surface more frequently should also be brands "
            "that people search for more. Presence and search interest both "
            "proxy brand salience in their respective substrates."
        ),
    },
    "H_CV_Recognition": {
        "label": "Convergent validity (Recognition alone)",
        "description": (
            "C_P (Recognition score, 0-6) alone correlates positively "
            "with Google Trends search interest."
        ),
        "statistic": "Spearman rho, 95% BCa bootstrap CI",
        "threshold_confirmed": "CI_lower > 0",
        "threshold_partial": "point estimate > 0 but CI includes zero",
        "threshold_falsified": "point estimate <= 0",
        "prediction": "CONFIRMED",
        "prediction_rationale": (
            "Recognition is the coarser signal but should still track "
            "search interest — brands known to more models are brands "
            "known to more searchers."
        ),
    },
    "H_CV_Recall": {
        "label": "Convergent validity (Category Recall alone)",
        "description": (
            "R_cat (category-channel recall mentions, 0-36) correlates "
            "positively with Google Trends search interest."
        ),
        "statistic": "Spearman rho, 95% BCa bootstrap CI",
        "threshold_confirmed": "CI_lower > 0",
        "threshold_partial": "point estimate > 0 but CI includes zero",
        "threshold_falsified": "point estimate <= 0",
        "prediction": "CONFIRMED",
        "prediction_rationale": (
            "R_cat should carry more predictive weight than C_P because "
            "it captures frequency of spontaneous mention, not just "
            "binary recognition."
        ),
    },
    "H_CV_Phantom": {
        "label": "Discriminant anchoring",
        "description": (
            "Cell D brands (Phantom/defunct) have both AIAS Presence "
            "composite and Google Trends scores at or near floor relative "
            "to active brands (Cells A+B+C)."
        ),
        "statistic": (
            "Mean separation with 95% CIs on both measures; "
            "Cell D vs. Cells A+B+C"
        ),
        "threshold_confirmed": (
            "Both separations hold with non-overlapping 95% CIs"
        ),
        "threshold_partial": (
            "Both directions hold but one or both CIs overlap"
        ),
        "threshold_falsified": "Either direction reverses",
        "prediction": "CONFIRMED",
        "prediction_rationale": (
            "Five defunct brands (Quip, Yammer, Wunderlist, HipChat, "
            "Stride) should anchor the floor on both axes. Nearly "
            "mechanical given product discontinuation."
        ),
    },
    "H_CV_CellOrder": {
        "label": "Cell-level monotonicity",
        "description": (
            "Cell-level mean AIAS Presence and cell-level mean Google "
            "Trends follow the same rank order across Cells A, B, C, D."
        ),
        "statistic": "Kendall tau between two cell-mean vectors (k=4)",
        "threshold_confirmed": "tau = 1.0 (perfect concordance)",
        "threshold_partial": "tau > 0 but < 1.0",
        "threshold_falsified": "tau <= 0",
        "prediction": "PARTIAL",
        "prediction_rationale": (
            "Cells A and D should anchor the extremes, but B vs. C "
            "ordering may not be identical across the two measures. "
            "High-identity challengers (Notion, Figma) may have "
            "disproportionate Trends signal relative to their LLM "
            "presence, or vice versa for infrastructure brands."
        ),
    },
    "H_CV_Discriminant_IL": {
        "label": "Discriminant validity (Identity Load)",
        "description": (
            "Identity Load (R_cult - R_cat, signed) is NOT significantly "
            "correlated with Google Trends search interest."
        ),
        "statistic": "Spearman rho, 95% BCa bootstrap CI",
        "threshold_confirmed": "CI includes zero",
        "threshold_partial": "N/A (null-hypothesis test)",
        "threshold_falsified": (
            "CI excludes zero (IL predicts Trends, undermining "
            "discriminant status)"
        ),
        "prediction": "CONFIRMED",
        "prediction_rationale": (
            "Identity Load measures a within-brand structural property "
            "(the gap between cultural and category recall), which "
            "should be orthogonal to raw brand popularity as proxied "
            "by search interest."
        ),
    },
}

# ---------------------------------------------------------------------------
# Scoring rules
# ---------------------------------------------------------------------------

SCORING = {
    "presence_composite": (
        "Arithmetic mean of C_P (scaled 0-100), R_cat (scaled 0-100), "
        "R_cult (scaled 0-100). Three equal-weight components, consistent "
        "with v1.6 section 9.5a Presence definition. "
        "C_P scaling: (raw / 6) * 100. "
        "R_cat scaling: (raw / 36) * 100. "
        "R_cult scaling: (raw / 36) * 100."
    ),
    "trends_score": (
        "Pivot-normalized search interest (0-100 scale) after cross-bundle "
        "chaining. Pivot brand (Salesforce) appears in every bundle. "
        "Per-brand score = (brand_raw / pivot_raw_in_same_bundle) * "
        "pivot_global_score. Pivot global score set to its raw score in "
        "the first bundle."
    ),
    "correlation_scope": (
        "All correlations computed on the full 24-brand vector. "
        "No subsetting except where H_CV_Phantom explicitly requires "
        "cell-level partitioning."
    ),
    "bootstrap": (
        "10,000 resamples, BCa method, seeded at pre-reg commit hash "
        "truncated to 32-bit integer."
    ),
}

# ---------------------------------------------------------------------------
# Exclusions / scope boundaries
# ---------------------------------------------------------------------------

EXCLUSIONS = {
    "no_causal_claims": (
        "This is correlational convergent validity, not causal inference. "
        "No claim about Trends -> Presence or Presence -> Trends direction."
    ),
    "no_temporal_dynamics": (
        "Whether Presence leads or lags Trends is CV.02+ territory."
    ),
    "presence_only": (
        "Non-Presence AIAS components (Ranking, Consistency, Coverage, "
        "Grounding, Sentiment) are out of scope."
    ),
    "no_transaction_data": (
        "Google Trends is a behavioral proxy for brand mindshare, "
        "not a transaction measure."
    ),
}

# ---------------------------------------------------------------------------
# Prior work citations
# ---------------------------------------------------------------------------

PRIOR_CV_WORK = {
    "v0.11": {
        "ssrn_id": "6745040",
        "description": (
            "Original construct validity pilot: PM software x Google Trends, "
            "single category, pre-v1.6 data (v0.6/v0.9)."
        ),
        "relationship": "CV.01 supersedes methodologically (v1.6 protocol).",
    },
    "v0.12": {
        "ssrn_id": "6748341",
        "description": (
            "Three-category expansion (PM software + olive oil + running "
            "shoes), pre-v1.6 data."
        ),
        "relationship": "CV.01 supersedes methodologically (v1.6 protocol).",
    },
}

# ---------------------------------------------------------------------------
# Deviations log (empty at pre-reg; populated if amendments needed)
# ---------------------------------------------------------------------------

DEVIATIONS = []
# Format: {"entry": 0, "description": "...", "date": "...", "impact": "..."}
