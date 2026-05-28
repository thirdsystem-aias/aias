"""
v0.26 — AIAS Presence × Amazon Best Sellers Rank: Cross-Substrate Predictive Validity
Pre-registration content module

Protocol lock: v1.6 (SSRN 6816340)
Design type: Construct Validity — Predictive (cross-sectional, correlational)
Prior CV study: v0.25 (Google Trends convergent validity, B2B SaaS)
"""

# ---------------------------------------------------------------------------
# STUDY METADATA
# ---------------------------------------------------------------------------

STUDY_TITLE = "AIAS Presence × Amazon Best Sellers Rank: Cross-Substrate Predictive Validity"
STUDY_SUBTITLE = (
    "Testing whether AI Presence scores predict real-world market performance "
    "across five consumer-goods substrates"
)
VERSION = "v0.26"
PROTOCOL_LOCK = "v1.6"
DESIGN_TYPE = "Construct Validity — Predictive"

# ---------------------------------------------------------------------------
# SUBSTRATE REGISTRY
# ---------------------------------------------------------------------------
# Five substrates drawn from the AIAS 1.0 base (6-substrate + automotive + B2B SaaS).
# Excluded: Indie Fragrance (v0.18, sparse/inconsistent Amazon distribution),
#           Automotive (v0.22, not sold on Amazon),
#           B2B SaaS (v0.24, software subscriptions, no Amazon listings).
#
# Brand lists are INHERITED from the locked registries of each source phase.
# No additions, removals, or substitutions. 24 brands per substrate = 120 total.

SUBSTRATES = {
    "kitchen_knives": {
        "source_phase": "v0.16",
        "ssrn": "6791999",
        "cp_source": "osf/v16/v16_verdicts.json",
        "n_brands": 24,
        "amazon_category": "Kitchen Knives & Accessories",
        "search_suffix": "kitchen knife",
    },
    "premium_kitchenware": {
        "source_phase": "v0.17",
        "ssrn": "6802261",
        "cp_source": "osf/v17/v17_verdicts.json",
        "n_brands": 24,
        "amazon_category": "Cookware",
        "search_suffix": "cookware",
    },
    "audiophile_headphones": {
        "source_phase": "v0.19",
        "ssrn": "6809182",
        "cp_source": "osf/v19/v19_verdicts.json",
        "n_brands": 24,
        "amazon_category": "Over-Ear Headphones",
        "search_suffix": "headphones",
    },
    "skincare": {
        "source_phase": "v0.20",
        "ssrn": "6811441",
        "cp_source": "osf/v20/v20_verdicts.json",
        "n_brands": 24,
        "amazon_category": "Skin Care",
        "search_suffix": "skincare",
    },
    "cosmetics": {
        "source_phase": "v0.21",
        "ssrn": "6815378",
        "cp_source": "osf/v21/v21_verdicts.json",
        "n_brands": 24,
        "amazon_category": "Makeup",
        "search_suffix": "makeup",
    },
}

TOTAL_BRAND_OBSERVATIONS = 120  # 5 × 24

# ---------------------------------------------------------------------------
# MODEL PANEL (not used for new probes — C_P reused from source phases)
# ---------------------------------------------------------------------------
# Source phases used the six-model reference panel (locked v0.17 onward):
# Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini,
# Gemini 2.5 Flash, Gemini 2.5 Flash Lite.
# No new LLM probes in this study. C_P scores are inherited canonical values.

# ---------------------------------------------------------------------------
# BSR ACQUISITION PROTOCOL
# ---------------------------------------------------------------------------

ACQUISITION_METHOD = "Automated browser-based extraction (Claude in Chrome)"
ACQUISITION_TIMING = (
    "Single session or contiguous sessions within a 48-hour window. "
    "Per-brand timestamps logged. Acquisition date recorded in DEVIATIONS."
)

BSR_PROTOCOL = {
    "search_template": "{brand_name} {search_suffix}",
    "site": "amazon.com",
    "best_of_n_rule": (
        "For each brand, retain the single product with the lowest (best) "
        "BSR among all products attributed to that brand in the relevant "
        "Amazon category. If multiple categories appear, use the BSR from "
        "the pre-registered category anchor."
    ),
    "absent_brand_coding": (
        "If a brand returns zero Amazon listings in the relevant category, "
        "or only third-party/gray-market listings not attributable to the "
        "brand's authorized distribution, code as BSR = absent. "
        "This is data, not missing data."
    ),
    "output_schema": [
        "substrate",
        "brand",
        "amazon_status",  # listed | absent
        "asin",
        "product_title",
        "bsr_rank",
        "bsr_category",
        "listing_url",
        "acquisition_timestamp",
        "notes",
    ],
}

# ---------------------------------------------------------------------------
# HYPOTHESES
# ---------------------------------------------------------------------------

HYPOTHESES = {
    "H_PV_Primary": {
        "label": "Per-substrate predictive validity",
        "claim": (
            "Among listed brands (BSR ≠ absent), C_P and Amazon BSR rank "
            "correlate negatively (higher Presence → lower/better BSR rank) "
            "at Spearman ρ ≤ −0.40, p < 0.05, in at least 3 of 5 substrates."
        ),
        "rationale": (
            "If AI Presence captures brand salience, it should predict "
            "market-performance proxies. ρ ≤ −0.40 represents a moderate "
            "effect appropriate for a distal outcome variable."
        ),
        "test": "Spearman rank correlation per substrate (listed brands only)",
        "thresholds": {"rho": -0.40, "p": 0.05, "min_substrates": 3},
        "falsification": (
            "Fewer than 3 substrates meet both magnitude (ρ ≤ −0.40) "
            "and significance (p < 0.05) thresholds."
        ),
        "verdict_taxonomy": {
            "CONFIRMED": "≥ 3/5 substrates meet both thresholds",
            "PARTIAL": "1–2/5 substrates meet both thresholds",
            "FALSIFIED": "0/5 substrates meet both thresholds",
        },
    },
    "H_PV_Pooled": {
        "label": "Cross-substrate pooled correlation",
        "claim": (
            "Pooled Spearman ρ across all listed brands "
            "(within-substrate rank-normalized BSR) reaches ρ ≤ −0.30, p < 0.01."
        ),
        "rationale": (
            "Pooling tests generalizability beyond any single category. "
            "Threshold relaxed to −0.30 due to cross-substrate noise."
        ),
        "operationalization": (
            "Within each substrate, convert raw BSR to within-substrate "
            "percentile rank (0–100, lower = better seller). Pool all 5 "
            "substrates. Compute Spearman ρ between C_P and percentile-rank BSR."
        ),
        "test": "Spearman rank correlation on pooled percentile-normalized BSR",
        "thresholds": {"rho": -0.30, "p": 0.01},
        "falsification": "Pooled ρ > −0.30 or p ≥ 0.01.",
        "verdict_taxonomy": {
            "CONFIRMED": "Pooled ρ ≤ −0.30 and p < 0.01",
            "FALSIFIED": "Pooled ρ > −0.30 or p ≥ 0.01",
        },
    },
    "H_PV_CellA": {
        "label": "Cell A separation",
        "claim": (
            "Brands with C_P ≥ 4 (Cell A candidates) have significantly "
            "lower (better) median BSR percentile rank than brands with "
            "C_P < 4, tested via Mann-Whitney U at p < 0.05."
        ),
        "rationale": (
            "The 4-regime taxonomy predicts high-Presence brands occupy "
            "the favorable quadrant of AI-mediated market access. "
            "If BSR proxies Physical Availability, Cell A brands should dominate."
        ),
        "test": "Mann-Whitney U on BSR percentile rank, split at C_P ≥ 4",
        "thresholds": {"p": 0.05},
        "falsification": (
            "Mann-Whitney U p ≥ 0.05 or direction reversal "
            "(Cell A brands have worse BSR)."
        ),
        "verdict_taxonomy": {
            "CONFIRMED": "p < 0.05 and correct direction",
            "FALSIFIED": "p ≥ 0.05 or direction reversal",
        },
    },
    "H_PV_Absent": {
        "label": "Absence–Presence alignment",
        "claim": (
            "Brands coded as Amazon-absent have lower mean C_P than "
            "Amazon-listed brands, tested via Mann-Whitney U at p < 0.05."
        ),
        "rationale": (
            "Brands lacking Amazon distribution should show lower AI Presence — "
            "absence from a major commercial channel and absence from AI "
            "recommendation surfaces should co-occur if both reflect "
            "underlying brand salience."
        ),
        "test": "Mann-Whitney U on C_P, split by Amazon status",
        "thresholds": {"p": 0.05, "min_absent": 5},
        "falsification": "Direction reversal or p ≥ 0.05.",
        "verdict_taxonomy": {
            "CONFIRMED": "Correct direction and p < 0.05",
            "PARTIAL": "Correct direction, p in [0.05, 0.10)",
            "FALSIFIED": "Wrong direction or p ≥ 0.10",
            "UNDETERMINED": "Fewer than 5 absent brands across all substrates",
        },
    },
}

# ---------------------------------------------------------------------------
# PREDICTIONS (directional expectations, pre-registered)
# ---------------------------------------------------------------------------

PREDICTIONS = {
    "kitchen_knives": {
        "expected_rho_direction": "negative (moderate)",
        "expected_absent_brands": "1–3 (artisan/Japanese specialists)",
        "notes": "Strong Amazon category; most brands have direct listings",
    },
    "premium_kitchenware": {
        "expected_rho_direction": "negative (moderate)",
        "expected_absent_brands": "1–2",
        "notes": "Most brands have Amazon presence; Lodge/Le Creuset/Staub are top sellers",
    },
    "audiophile_headphones": {
        "expected_rho_direction": "negative (moderate–strong)",
        "expected_absent_brands": "2–4 (boutique audiophile brands)",
        "notes": "Consumer electronics = Amazon-native category",
    },
    "skincare": {
        "expected_rho_direction": "negative (moderate)",
        "expected_absent_brands": "1–3 (prestige/clinical brands)",
        "notes": "Amazon is major channel but some brands restrict distribution",
    },
    "cosmetics": {
        "expected_rho_direction": "negative (weak–moderate)",
        "expected_absent_brands": "2–5 (prestige brands restrict Amazon)",
        "notes": "Most distribution-restricted substrate in the panel",
    },
}

# ---------------------------------------------------------------------------
# SCORING RULES
# ---------------------------------------------------------------------------

SCORING = {
    "C_P": {
        "source": "Existing vNN_verdicts.json from source phases",
        "type": "Integer 0–6 (already scored)",
        "recompute": False,
    },
    "BSR_raw": {
        "source": "Amazon browser-automation snapshot",
        "type": "Integer rank (1 = best seller)",
    },
    "BSR_pctile": {
        "source": "Derived from BSR_raw",
        "type": "Within-substrate percentile: rank(BSR_raw) / N_listed × 100",
        "notes": "Lower = better seller. Used for cross-substrate pooling.",
    },
    "Amazon_status": {
        "source": "Amazon browser-automation snapshot",
        "type": "Binary: listed | absent",
    },
}

# ---------------------------------------------------------------------------
# ANALYSIS PIPELINE
# ---------------------------------------------------------------------------

ANALYSIS_STEPS = [
    "1. Merge C_P scores from 5 verdict files with BSR acquisition CSV on brand name.",
    "2. Per-substrate: filter to listed brands → Spearman ρ(C_P, BSR_raw) → record ρ, p, N.",
    "3. Pooled: compute BSR_pctile within each substrate → stack → Spearman ρ(C_P, BSR_pctile) → record ρ, p, N.",
    "4. Cell A test: split on C_P ≥ 4 vs. < 4 → Mann-Whitney U on BSR_pctile → record U, p, median difference.",
    "5. Absent test: split on Amazon_status → Mann-Whitney U on C_P → record statistic, p, means.",
]

# ---------------------------------------------------------------------------
# DEVIATIONS LOG
# ---------------------------------------------------------------------------
# Entry 0 reserved for pre-reg amendments (r1 → r2) if methodology defects
# surface pre-acquisition. Currently empty.

DEVIATIONS = []
