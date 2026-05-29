"""
v0.27 - CV.03 Convergent Validity - Pre-registration content module
AIAS Measurement Program - Protocol v1.6 lock (SSRN 6816340)

Schema conformed to prereg/v0_26_amazon_bsr_predictive_validity_content.py so the
v0.26-cloned v27 scripts import without structural change. ONE domain-specific slot
renamed for lineage honesty: v0.26 BSR_PROTOCOL -> INSTRUMENT_PROTOCOL. The cloned
v27 scorer/builders reference BSR_PROTOCOL by name; rename those references (surgical,
grep-scoped) AFTER the pre-reg commit and BEFORE scoring. The pre-reg commit/tag
imports nothing, so this is non-blocking for the lock.

Confirm SCORING and ANALYSIS_STEPS internal shapes against v0_26 by eye before commit
(those two shapes were inferred from key names, not the literal file).

AIAS-side variable for all convergent tests is the variance-bearing recall-channel SOM
(and AIAS composite). Recognition C_P is at ceiling on B2B SaaS (6/6, per v0.24/v0.25)
and enters only as the Recognition_Null control.
"""

VERSION = "v0.27"

STUDY_TITLE = ("Convergent Validity of AIAS Presence Against "
               "Third-Party AI Brand-Visibility Instruments")
STUDY_SUBTITLE = ("A single-substrate (B2B SaaS) convergent-validity test of the "
                  "AI Availability Score against commercial AI-visibility tools")

PROTOCOL_LOCK = "v1.6 (SSRN 6816340)"

DESIGN_TYPE = "convergent_validity"   # cf. v0.26 discriminant/predictive_validity

# Single-substrate study; dict shape preserved from v0.26 so SUBSTRATES.items()
# iteration in the cloned scripts still works.
SUBSTRATES = {
    "b2b_saas": {
        "source_phase": "v0.24 / v0.25",
        "ssrn": "6838802 (v0.24) / 6842138 (v0.25)",
        "cp_source": ("v0.24 Phase A recognition (C_P = 6/6 ceiling); "
                      "convergent test uses recall-channel SOM"),
        "category": "B2B SaaS",
    },
}

# Inherited verbatim from v0.24 (osf/v24/registries/v24_registry.json), copied into
# the v0.27 tree so the lock is self-contained.
REGISTRY_SOURCE = "osf/v27/registries/v27_registry.json"

# Fixed reference panel, held from v0.17 onward.
PANEL = [
    "Claude Opus 4.5", "Claude Sonnet 4.5",
    "GPT-4o", "GPT-4o-mini",
    "Gemini 2.5 Flash", "Gemini 2.5 Flash Lite",
]

# v0.26 BSR_PROTOCOL analog: external instruments + pull/alignment config.
INSTRUMENT_PROTOCOL = {
    "I1": {
        "name": "HubSpot AEO Grader", "role": "convergent_primary_floor",
        "trait": "ai_presence", "access": "free_no_account", "guaranteed": True,
        "variables": ["visibility_composite", "sentiment", "presence_quality",
                      "brand_recognition", "share_of_voice", "market_competition"],
    },
    "I2": {
        "name": "Profound", "role": "convergent_coprimary",
        "trait": "ai_presence", "access": "api_or_csv_if_obtained",
        "guaranteed": False, "reports_som": True,
        "variables": ["visibility_score", "share_of_model"],
    },
    "I3": {
        "name": "Brandwatch", "role": "discriminant_contrast",
        "trait": "web_mention_volume", "access": "export", "guaranteed": True,
        "variables": ["mention_volume"],
    },
    "pull_window_days": 7,        # instrument pulls within +/-7d of Phase B
    "coverage_gate_min_n": 12,    # covered n < 12 -> hypothesis UNDETERMINED
}

PRIOR_PROXY_RHO = 0.74   # v0.25 AIAS x Google Trends anchor for the directional prediction

_VERDICTS = ["CONFIRMED", "STRONG", "PARTIAL", "FALSIFIED", "UNDETERMINED", "NOT_RUN"]

# HYPOTHESES internal shape conformed to v0.26.
HYPOTHESES = {
    "H_CV3_Primary": {
        "claim": ("AIAS recall-channel SOM converges with the HubSpot AEO "
                  "visibility composite across the registry."),
        "rationale": ("HubSpot AEO is a same-construct (AI-presence) instrument; "
                      "convergent validity predicts positive rank association on the "
                      "variance-bearing AIAS variable."),
        "test": ("Spearman rho(recall_channel_som, HubSpot_AEO_visibility_composite), "
                 "brand-level, pairwise on covered subset."),
        "thresholds": {"confirmed": "rho >= 0.60 and p < 0.05", "strong": "rho >= 0.74"},
        "falsification": "rho < 0.30 or not significant.",
        "verdict_taxonomy": _VERDICTS,
    },
    "H_CV3_Profound": {
        "claim": "AIAS recall-channel SOM converges with the Profound visibility score.",
        "rationale": ("Profound is a same-construct AI-presence instrument running its "
                      "own engine panel; convergent validity predicts positive association."),
        "test": "Spearman rho(recall_channel_som, Profound_visibility_score), brand-level.",
        "thresholds": {"confirmed": "rho >= 0.60", "strong": "rho >= 0.74"},
        "falsification": "rho < 0.30.",
        "verdict_taxonomy": _VERDICTS,
        "not_run_if": "Profound access not obtained (DEVIATIONS Entry 0).",
    },
    "H_CV3_SOM": {
        "claim": "AIAS computed SOM converges with Profound-reported Share-of-Model.",
        "rationale": ("Flagship same-metric test: identical metric name, independent "
                      "pipelines. Strongest possible convergent evidence; higher bar warranted."),
        "test": "Spearman rho(aias_computed_som, profound_share_of_model), brand-level.",
        "thresholds": {"confirmed": "rho >= 0.70", "strong": "rho >= 0.80"},
        "falsification": "rho < 0.40.",
        "verdict_taxonomy": _VERDICTS,
        "not_run_if": "Profound access not obtained (DEVIATIONS Entry 0).",
    },
    "H_CV3_Discriminant": {
        "claim": ("AIAS converges with Brandwatch web-mention volume substantially LESS "
                  "than with the AI-native instruments."),
        "rationale": ("Brandwatch measures web/social mention volume, not AI presence "
                      "(heterotrait). The MTMM heterotrait-heteromethod cell should be low; "
                      "a high value would mean AIAS tracks generic salience rather than "
                      "AI-specific presence."),
        "test": "Compare rho(AIAS, Brandwatch) against rho(AIAS, I1).",
        "thresholds": {"confirmed": "rho_I3 < 0.50 and (rho_I1 - rho_I3) >= 0.20"},
        "falsification": "rho_I3 >= rho_I1.",
        "verdict_taxonomy": _VERDICTS,
    },
    "H_CV3_Component": {
        "claim": ("Within-study MTMM block holds: AIAS visibility-type components track "
                  "instrument visibility dimensions; AIAS sentiment tracks instrument "
                  "sentiment, not visibility."),
        "rationale": ("Component-resolved convergent/discriminant structure is stronger "
                      "evidence than a single pooled correlation."),
        "test": "Component x matched instrument sub-dimension correlation matrix; inspect block structure.",
        "thresholds": {"confirmed": "predicted convergent/discriminant block structure present"},
        "falsification": "block structure absent.",
        "verdict_taxonomy": _VERDICTS,
        "tier": "secondary_exploratory",
    },
    "H_CV3_Recognition_Null": {
        "claim": ("Recognition C_P carries no usable variance on B2B SaaS "
                  "(replicates v0.24/v0.25 ceiling) and is excluded from the primary test."),
        "rationale": ("C_P = 6/6 for all brands -> zero variance -> uncorrelatable. "
                      "Documents why the AIAS-side variable is recall-channel SOM."),
        "test": "SD of recognition C_P across the 24 brands.",
        "thresholds": {"confirmed": "SD ~= 0; excluded from primary"},
        "falsification": "non-falsifying control",
        "verdict_taxonomy": ["CONFIRMED", "UNDETERMINED"],
    },
}

PREDICTIONS = {
    "ordering": "rho_Profound ~= rho_HubSpot > rho_Trends(0.74) > rho_Brandwatch",
    "same_construct_floor": ("AI-native instruments should converge at least as strongly "
                             "as the v0.25 proxy (0.74); converging below is logged as a "
                             "substantive tension against AIAS."),
}

SCORING = {
    "statistic": "spearman_rho",
    "unit": "brand",
    "min_n_for_valid_rho": 12,        # below -> UNDETERMINED, not FALSIFIED
    "bootstrap_resamples": 10000,
    "ci": "95%",
    "multiple_comparison": "holm",
    "primary_family": ["H_CV3_Primary", "H_CV3_Profound", "H_CV3_SOM"],
    "aias_side_primary": "recall_channel_som",
    "aias_side_secondary": "aias_composite",
    "verdicts_out": "osf/v27/v0.27_verdicts.json",
}

ANALYSIS_STEPS = [
    "Load locked 24-brand registry (osf/v27/registries/v27_registry.json; inherited verbatim from v0.24).",
    "Phase A recognition (144 probes) -> C_P per brand (ceiling-expected; Null control only).",
    "Phase B two-channel recall (36 queries) -> recall-channel SOM and AIAS composite per brand.",
    "Instrument pulls I1/I2/I3 within +/-7d of Phase B; record non-null coverage; no imputation.",
    "Coverage pre-screen: per-instrument covered subset; covered n < 12 -> UNDETERMINED.",
    "Spearman rho (bootstrap 95% CI, 10k) per hypothesis; Holm correction across primary family.",
    "Emit osf/v27/v0.27_verdicts.json against the locked HYPOTHESES matrix.",
]

DEVIATIONS = [
    {
        "entry": 0,
        "trigger": "Profound (I2) access not secured before acquisition.",
        "action": ("Amend at v0.27-prereg-r2. I2 and H_CV3_SOM -> NOT_RUN. Study proceeds "
                   "on I1 (HubSpot AEO, pre-committed floor) + I3 (Brandwatch). No threshold "
                   "or hypothesis changes to I1/I3."),
        "status": "armed",   # flips to 'fired' in r2 if triggered
    },
]
