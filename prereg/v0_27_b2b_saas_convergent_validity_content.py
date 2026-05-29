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

# Reference panel as present in the inherited v0.24 Phase B corpus
# (r2: corrected from a stale "4.5" listing to the actual model set in
#  osf/v24/data/v24_phase_b.csv; sourced verbatim, not edited by hand).
PANEL = [
    "Claude Opus 4.7", "Claude Sonnet 4.6",
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
        "query_frame": "category-competitive (generic B2B-SaaS-leadership topic), matching AIAS R_cat; use within-category share_of_voice / market_competition dimensions, NOT the brand-absolute visibility grade, where the tool exposes them",
        "construct_match": "loose - brand-entry tool; brand-absolute orientation is a looser match to R_cat's category-competitive recall; generic-vs-brand-specific gap is an expected I1 attenuation source",
    },
    "I2": {
        "name": "Profound", "role": "convergent_coprimary",
        "trait": "ai_presence", "access": "api_or_csv_if_obtained",
        "guaranteed": False, "reports_som": True,
        "variables": ["visibility_score", "share_of_model"],
        "query_frame": "scope Share-of-Model to the generic B2B-SaaS-leadership topic cluster, matching AIAS R_cat",
        "construct_match": "tight - Share-of-Model is natively per-topic-cluster competitive; cleanest available analog to R_cat",
    },
    "I3": {
        "name": "Brandwatch", "role": "discriminant_contrast",
        "trait": "web_mention_volume", "access": "export", "guaranteed": True,
        "variables": ["mention_volume"],
        "query_frame": "n/a (discriminant; web/social mention volume by design)",
        "construct_match": "intentional heterotrait (discriminant contrast)",
    },
    "pull_window_days": 7,        # instrument pulls within +/-7d of Phase B
    "coverage_gate_min_n": 12,    # covered n < 12 -> hypothesis UNDETERMINED
    "construct_alignment_rule": ("Convergent instruments (I1, I2) are operated in the same category-competitive frame as AIAS R_cat (generic B2B-SaaS-leadership), NOT brand-absolute presence. If an instrument exposes only a brand-absolute score, that is recorded and its construct_match downgraded to 'loose', with the gap documented."),
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
    "som_definition": "recall_channel_som = R_cat_scaled = (R_cat/36)*100; pooled mention count over 6 category probes x 6 models; reuses score_v0_25.py:88-130 verbatim",
    "som_denominator": "pooled, fixed /36 (NOT per-model-averaged)",
    "aias_composite_definition": "v0.25 presence_composite = mean(C_P_scaled, R_cat_scaled, R_cult_scaled); the recoverable inherited composite (full 6-component AIAS was never computed for v0.24)",
    "r_cult_handling": "excluded from convergent SOM; retained in identity_load = R_cult - R_cat",
    "sensitivity_analysis": {
        "name": "type2_construct_gap",
        "rule": "exclude brands where (R_cat == 0 AND R_cult > 0) - the type-2 set: category-competitive-invisible but specialist/cult-salient",
        "report": "primary rho on all covered brands PLUS this sensitivity rho; a RISE on exclusion = attenuation attributable to the generic-leadership vs brand-specific construct gap",
        "scope": "convergent hypotheses only (H_CV3_Primary, H_CV3_Profound, H_CV3_SOM); NOT H_CV3_Discriminant",
        "cell_d_handling": "Cell_D true-zeros (R_cat==0 AND R_cult==0) are RETAINED in primary - genuine concordant absence, not a construct artifact",
    },
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
    {
        "entry": 1,
        "trigger": "AIAS-side handling under-specified at r1.",
        "action": ("recall_channel_som and aias_composite are COMPUTED from the inherited "
                   "v0.24 Phase B corpus (osf/v24/data/v24_phase_b.csv), not freshly acquired. "
                   "Timing window redefined: instrument pulls within +/-7d of EACH OTHER "
                   "(not of Phase B); AIAS-side dated to v0.24 (same calendar month). "
                   "v0.24->pull temporal gap moved to LIMITATIONS as a named threat-to-validity."),
        "status": "fired",
    },
    {
        "entry": 2,
        "trigger": "PANEL string did not match the inherited v0.24 Phase B data.",
        "action": "PANEL corrected to the actual model set present in v24_phase_b.csv (sourced verbatim).",
        "status": "fired",
    },
    {
        "entry": 3,
        "trigger": "recall_channel_som denominator not pinned at r1 (R_cat alone vs two-channel fusion).",
        "action": ("Pinned: recall_channel_som = R_cat_scaled, pooled /36, per score_v0_25.py:88-130 "
                   "verbatim. Matches the v0.25 H_CV_Recall metric, preserving comparability to "
                   "the rho_Trends=0.74 anchor."),
        "status": "fired",
    },
    {
        "entry": 4,
        "trigger": ("AIAS-side derivation surfaced a two-tier zero floor: 5 Cell_D true-zeros "
                    "(R_cat=0, R_cult=0) and 4 type-2 brands (R_cat=0, R_cult>0) that are "
                    "category-competitive-invisible but specialist-salient."),
        "action": ("Pre-pull, before any instrument data: (a) pinned instrument-query construct "
                   "alignment to R_cat's category-competitive frame in INSTRUMENT_PROTOCOL; "
                   "(b) added one rule-defined sensitivity rho (exclude R_cat=0 & R_cult>0) to SCORING; "
                   "(c) added the construct-gap LIMITATION. No hypothesis or threshold changed."),
        "status": "fired",
    },
]

# r2: LIMITATIONS block created fresh — the r1 conform-to-v0.26-schema pass dropped
# the original draft's LIMITATIONS var. First line authored at r2 (review); second
# is the temporal-gap threat referenced by DEVIATIONS Entry 1.
LIMITATIONS = [
    "Convergent instruments (HubSpot AEO Grader, Profound, Brandwatch) report "
    "continuously-refreshed live measurements, whereas the AIAS-side variable is a "
    "single point-in-time measurement inherited from v0.24; convergent rho compares a "
    "point measurement against continuously-refreshed instruments, which can attenuate "
    "observed agreement.",
    "AIAS-side inherited from v0.24 (same month as instrument pulls); residual "
    "brand-level drift over the gap is a threat to convergent rho, mitigated but not "
    "removed by rank-based (Spearman) correlation.",
    "R_cat (generic-leadership recall) and brand-entry instruments (notably HubSpot AEO Grader) operationalize 'AI presence' differently - category-competitive vs brand-absolute. For the type-2 set (R_cat=0, R_cult>0: e.g. Linear, Airtable, Miro, Cloudflare), AIAS reads 0 while a brand-absolute instrument may read non-trivial visibility, attenuating convergent rho. Mitigated by category-frame instrument scoping (tight for Profound) and a pre-registered type-2 sensitivity rho; residual gap is largest where an instrument yields only brand-absolute scores.",
]
