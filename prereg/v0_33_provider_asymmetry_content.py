"""
v0.33 - Provider-Asymmetric CPC - Pre-Registration Content Module
AIAS(TM) Measurement Program - Third System(TM)

Locked pre-registration artifact (tag v0.33-prereg-r1).

Re-analysis (secondary analysis of v0.31's frozen per-model inputs; NO LLM
acquisition). Tests whether the v0.31 CV-CPC quantity carries systematic
between-provider structure, and - the gating question - whether that structure
exceeds the provider structure already present in Presence.

Cloned from v0.32 (CPC Version-Snapshot Stability). The measurement schema
(PHASE_TYPE=prospective_two_arm, MODEL_PANEL_ARMS, VINTAGES, ACQUISITION, and the
v0_33_snapshot_resolution.json reachability gate) is replaced with a re-analysis
schema. There is no reachability/snapshot-resolution gate in a re-analysis - the
PROVENANCE lock IS the registry.
"""

PHASE_ID = "v0.33"
PHASE_TITLE = "Provider-Asymmetric CPC"
METHODOLOGY_LOCK = "v1.7"        # CV-CPC definition inherited; walled by FRAMING (v1.7 not adopted)
INSTRUMENT_SOURCE = "v0.30"      # CV-CPC instrument origin (pilot spec)
BASELINE_SOURCE = "v0.31"        # frozen data source (SSRN 6880959)
PHASE_TYPE = "reanalysis"        # secondary analysis, no acquisition
PREREG_TAG = "v0.33-prereg-r1"   # scaffold pre-set r2; corrected to r1 (substrate set fixed pre-lock)

# ---------------------------------------------------------------------------
# Substrate scope (corrected pre-lock: the "8 substrates v0.16-v0.24" framing
# FAILED verification - only 5 carry the canonical six-model panel).
# ---------------------------------------------------------------------------
SUBSTRATES = [
    {"phase": "v0.19", "name": "audiophile headphones", "brands": 16, "panel": "canonical-6", "role": "omnibus"},
    {"phase": "v0.20", "name": "skincare",              "brands": 24, "panel": "canonical-6", "role": "omnibus"},
    {"phase": "v0.21", "name": "cosmetics",             "brands": 24, "panel": "canonical-6", "role": "omnibus"},
    {"phase": "v0.22", "name": "automotive",            "brands": 24, "panel": "canonical-6", "role": "omnibus"},
    {"phase": "v0.23", "name": "premium spirits",       "brands": 24, "panel": "canonical-6", "role": "omnibus"},
]
N_BRAND_UNITS = 112       # 16 + 24*4
N_SUBSTRATE_UNITS = 5

SUBSTRATES_DESCRIPTIVE = [
    {"phase": "v0.18", "name": "indie fragrance", "brands": 24, "panel": "canonical-6 / 3-frame",
     "role": "descriptive concordance aside - geometry non-comparable; walled from omnibus"},
]
SUBSTRATES_EXCLUDED = [
    {"phase": "v0.16", "name": "kitchen knives", "reason": "14-model legacy panel; no per-model recall"},
    {"phase": "v0.17", "name": "kitchenware",    "reason": "deferred / unscored"},
    {"phase": "v0.24", "name": "B2B SaaS",       "reason": "off-panel models (opus-4-7 / sonnet-4-6)"},
]

# ---------------------------------------------------------------------------
# FRAMING (repurpose-in-place: the scaffold's v1.7-not-adopted / rho=0.77 /
# v0.31-reconciliation language aligns with the instrument-status paragraph;
# the snapshot-vs-version and panel-scope paragraphs are the v0.33 additions).
# ---------------------------------------------------------------------------
FRAMING = """
Instrument status (walled). This phase analyzes provider structure in the CV-CPC
quantity exactly as computed in v0.31. It makes NO claim that CV-CPC is a valid
Consistency instrument: v1.7 falsified CV-CPC as dissociating from Presence
(recall-coupling rho = 0.77) and did not adopt it. CV-CPC is treated here as a
descriptive, Presence-coupled quantity pending v1.8's mean-independent instrument.
Forward-note resolving the v0.31 <-> v0.32 status inconsistency: v0.31 is the
frozen data source; v1.7 is the (not-adopted) definitional lock.

Snapshot vs. version (scope; distinct from v0.32). v0.32 found CPC version
fragility concentrated in OpenAI's gpt-4o -> gpt-5.x transition. v0.33 re-analyzes
v0.31's FIXED snapshot panel (gpt-4o, the canonical six), asking the orthogonal
cross-sectional question: at one point in time, do providers differ in CV-CPC?
v0.32 = within-provider, across versions, over time. v0.33 = between-provider, at a
fixed snapshot. The two dimensions are genuinely distinct and must not be conflated.
v0.33 cites v0.32 as motivating (temporal provider-dependence observed -> test
cross-sectional provider asymmetry).

Panel-uniformity scope (does not overclaim). Only the 5 omnibus substrates carry
the canonical six-model panel. v0.33 does NOT claim panel uniformity across the
full anchor base: v0.18's 3-frame geometry and v0.24's off-panel models are
pre-existing program-hygiene items, out of v0.33 scope. The claim is bounded to
the 5-substrate panel-uniform set.
"""

# ===========================================================================
# CV-CPC DEFINITIONAL CONSTANTS - inherited from v0.31 (the true re-analysis
# ancestor), unchanged.
#   PANEL_N = 6                          (panel design)
#   DISPERSION / TRANSFORM / CPC_RANGE   identical in v0.31 and v0.32; copy verbatim
#   FLOOR                                use v0.31's (richer; undefined-brand handling)
#   NA_AND_FLIP_RULE                     OMITTED - a v0.32 two-arm / version-stability
#     construct (arms, flips, version rho>=0.70) with no analogue in a cross-sectional
#     provider re-analysis. N/A handling lives in FLOOR.handling (per v0.31); the
#     eta^2 zero-variance convention is specified in SCORING.
# ===========================================================================
PANEL_N = 6
DISPERSION = "CV = population_SD / mean (ddof=0)"
TRANSFORM = "CPC = 1 / (1 + CV)"   # bounded (0, 1]; higher = more consistent
CPC_RANGE = "(0, 1]"
FLOOR = {
    "rule": "mean(combined_recall_count) < 1.0  ->  CPC = UNDEFINED (N/A)",
    "handling": (
        "Undefined brands excluded from the substrate CPC distribution; "
        "count of undefined brands reported per substrate."
    ),
    "note": (
        "Inherited v1.7 floor. Subsumes 'defunct / zero-signal -> undefined, "
        "not zero'; no separate phase-level floor is introduced."
    ),
}
# ===========================================================================

# ---------------------------------------------------------------------------
# PROVIDER_GROUPS (replaces MODEL_PANEL_ARMS + VINTAGES)
# ---------------------------------------------------------------------------
PROVIDER_GROUPS = {
    "Anthropic": ["Claude Opus 4.5", "Claude Sonnet 4.5"],
    "OpenAI":    ["GPT-4o", "GPT-4o-mini"],
    "Google":    ["Gemini 2.5 Flash", "Gemini 2.5 Flash Lite"],
}
# 3 providers x 2 models = canonical six-model panel (v0.31 snapshot).

# ---------------------------------------------------------------------------
# PROVENANCE (replaces ACQUISITION) - the registry for a re-analysis.
# ---------------------------------------------------------------------------
PROVENANCE = {
    "phase_type": "reanalysis - no LLM acquisition",
    "frozen_inputs": [
        {"phase": "v0.19", "path": "osf/v19/phase_b_results.csv",
         "shape": "brand, panel_model, frame, mentioned, rank",
         "extraction_path": "A"},
        {"phase": "v0.20", "path": "osf/v20/phase_b_results.csv",
         "shape": "model, frame_id, channel, frame_text, response_text (brand NOT pre-coded)",
         "extraction_path": "B", "dependency": "v0.31 certified brand matcher (carried forward)"},
        {"phase": "v0.21", "path": "osf/v21/phase_b_results.csv",
         "shape": "(as v0.20)", "extraction_path": "B", "dependency": "v0.31 certified brand matcher"},
        {"phase": "v0.22", "path": "osf/v22/phase_b_results.csv",
         "shape": "(as v0.20)", "extraction_path": "B", "dependency": "v0.31 certified brand matcher"},
        {"phase": "v0.23", "path": "osf/v23/data/v23_phase_b_scored.json",
         "shape": "model_id, brand_mentions{brand_id:0/1}; recognition coded as r_level (normalize to binary)",
         "extraction_path": "C"},
    ],
    "per_model_recovery": (
        "v0.31 published outputs are brand-collapsed (v31_cpc.csv: mean_r, cpc_score; "
        "no per-model vector). Per-model recall AND per-model Presence are recomputed "
        "from the raw Phase A/Phase B files above by re-running v0.31's extraction "
        "across the three heterogeneous input paths (A/B/C)."
    ),
    "presence_recovery": (
        "Per-model Presence (C_P) recomputed from Phase A recognition (per-model by "
        "construction): v0.19 recognition_yes; v0.20-22 recognized; v0.23 r_level "
        "(normalize to binary). Gating input for H_Provider_Beyond_Presence."
    ),
    "reconciliation_guardrail": (
        "Recomputed v0.20/0.21/0.22 per-model RECALL vectors MUST reproduce "
        "osf/methodology/v1_7/data/v1_7_cpc.csv 'r_per_model' bit-for-bit. Mismatch = "
        "computational-reproducibility note in OSF README (NOT a DEVIATIONS entry); "
        "halt recompute until resolved. SCOPE LIMIT: this external anchor covers ONLY "
        "v0.20/0.21/0.22. v0.19 and v0.23 recompute has no independent external anchor "
        "- correctness rests on v0.31's extraction-function provenance alone. State in "
        "the OSF README; do not overclaim guardrail coverage as all five."
    ),
    "registry_note": "No reachability / snapshot-resolution gate (re-analysis). The provenance lock is the registry.",
}

# ---------------------------------------------------------------------------
# HYPOTHESES (replaces the v0.32 HYPOTHESES block)
# ---------------------------------------------------------------------------
HYPOTHESES = [
    {"tag": "H_Provider_Asymmetry", "tier": "PRIMARY",
     "statement": "Between-provider component is a material, non-null share of total cross-model CV-CPC dispersion.",
     "confirmed_iff": "mean eta^2 exceeds permutation-null upper bound, one-sided p < 0.05",
     "falsified_iff": "observed eta^2 within null envelope",
     "undetermined": "marginal / fragile under leave-one-substrate-out (legitimate verdict)"},
    {"tag": "H_Provider_Beyond_Presence", "tier": "PRIMARY (gate)",
     "statement": "Provider asymmetry in CV-CPC exceeds provider asymmetry in Presence (C_P).",
     "confirmed_iff": "delta_eta2 = eta^2_CVCPC - eta^2_CP > 0, permutation p < 0.05",
     "falsified_iff": "delta_eta2 <= 0 or within null -> 'provider asymmetry restates Presence'"},
    {"tag": "H_Provider_Ordinal", "tier": "SECONDARY (underpowered at N=5)",
     "statement": "Provider within-pair consistency ranks are stable across the 5 omnibus substrates.",
     "confirmed_iff": "Kendall's W across 5 substrates significant (exact null, 6^5 = 7776 arrangements)",
     "falsified_iff": "W n.s. - but a null W is UNINFORMATIVE about true concordance at N=5; report descriptively regardless"},
    {"tag": "H_Provider_Phantom", "tier": "TERTIARY (exploratory, walled)",
     "statement": "Provider asymmetry amplifies for below-recall-floor / phantom-prone brands (v0.31 recall-floor classification).",
     "confirmed_iff": "-- descriptive contrast only; no confirmatory threshold --",
     "falsified_iff": "-- n/a (exploratory) --"},
]

# ---------------------------------------------------------------------------
# SCORING (replaces v0.32 SCORING; sections 3 + 4)
# ---------------------------------------------------------------------------
SCORING = """
Unit of analysis: per brand b within substrate s. Per-model values x_{b,m}, m in
the canonical six models; provider p(m) in {Anthropic, OpenAI, Google}. One-way
layout, provider as 3-level factor, 2 replicates per level.

Between-provider variance share:  eta^2_b = SS_between(provider) / SS_total.
Population summary: mean eta^2 across all 112 brand units; also per-substrate.

Zero-variance convention: a brand with SS_total = 0 - identical per-model values
across all six models (e.g. a brand recognized/recalled identically by every
model; distinct from below-floor brands, which FLOOR removes) - has no cross-model
variance to partition, so its provider-asymmetry share is defined as eta^2 := 0,
NOT excluded. Rationale: a brand where models do not differ shows zero provider
asymmetry; excluding such brands would upward-bias the mean-eta^2 Asymmetry test
and, in C_P, discard the saturated-recognition brands (eta^2_CP = 0, eta^2_CVCPC
> 0) that are the purest beyond-Presence signal. Applies identically to CV-CPC and
C_P.

Within-provider CPC (per provider, per substrate): within-pair agreement =
1 - normalized |x_m1 - x_m2| over each provider's two models, averaged over brands.

Null model (PRIMARY): the per-brand label space is EXACTLY enumerable - 6 models
into 3 labeled pairs = 6!/(2!2!2!) = 90 assignments. Population test = Monte Carlo
resampling from the per-brand exact null spaces, >= 10,000 draws, one-sided.

Presence guardrail (gating - H_Provider_Beyond_Presence): run the IDENTICAL eta^2
provider-decomposition on raw Presence (C_P) from the same inputs. Decisive
statistic delta_eta2 = eta^2_CVCPC - eta^2_CP, with its own permutation null. Gates
whether the finding is Consistency-flavored asymmetry or restated Presence asymmetry.

Beyond_Presence (delta_eta2): paired per brand over all above-floor brands,
delta_eta2 = mean_b[eta^2_CVCPC,b - eta^2_CP,b], permutation null as above. Under
this convention every above-floor brand is defined (no intersection shrinkage);
saturated-recognition brands correctly contribute CV-CPC structure that Presence
cannot account for.

Ordinal (SECONDARY): rank the 3 providers by mean within-pair consistency per
substrate; Kendall's W across the 5 substrates; exact null (6^5 = 7776 joint rank
arrangements). Report raw W and the provider rank table descriptively.
"""

# ---------------------------------------------------------------------------
# SENSITIVITY (section 7 robustness)
# ---------------------------------------------------------------------------
SENSITIVITY = """
PRIMARY robustness: leave-one-substrate-out (LOSO) over the 5 omnibus substrates.
A PRIMARY verdict that does not survive LOSO is reported as fragile / UNDETERMINED
(cf. v0.32 PRIMARY fragility precedent under leave-one-provider-out).
"""

# ---------------------------------------------------------------------------
# PHANTOM_DESCRIPTIVE (tertiary, walled) + v0.18 concordance aside
# ---------------------------------------------------------------------------
PHANTOM_DESCRIPTIVE = """
H_Provider_Phantom (tertiary, walled, exploratory): contrast provider-asymmetry
magnitude (eta^2) in below-recall-floor / phantom-prone brands vs. above-floor,
using v0.31's recall-floor classification (cf. the spirits recognition-recall
inversion). Descriptive only; no confirmatory threshold; hypothesis-generating.

v0.18 descriptive concordance aside (walled from the omnibus): compute v0.18's
eta^2 under its own 3-frame geometry and report DIRECTIONAL concordance with the
omnibus (does the sign and provider ordering of asymmetry agree?). NOT pooled into
PRIMARY / delta_eta2 / Kendall's W - geometry is non-comparable.
"""

# ---------------------------------------------------------------------------
# PREDICTIONS (section 6)
# ---------------------------------------------------------------------------
PREDICTIONS = """
H_Provider_Asymmetry: lean CONFIRMED (distinct corpora / RLHF -> plausible
per-provider response tendencies); UNDETERMINED plausible given thin substrate N.
H_Provider_Beyond_Presence: GENUINELY OPEN, lean FALSIFIED-or-marginal - CV-CPC's
rho = 0.77 Presence-coupling makes pure-Presence inheritance plausible. This is the
honest pre-commitment and the substantive core of the phase.
H_Provider_Ordinal: lean UNDETERMINED (N=5 too thin to resolve); reported descriptively.
H_Provider_Phantom: no directional commitment.
"""

# ---------------------------------------------------------------------------
# LIMITATIONS (section 7 two-level N)
# ---------------------------------------------------------------------------
LIMITATIONS = """
Two-level N. Brand level ~ 112 units (16 + 24 + 24 + 24 + 24): adequate to detect
the EXISTENCE of aggregate provider asymmetry (PRIMARY) and delta_eta2
(Beyond_Presence) against the per-brand permutation null. Substrate level = 5:
thin - limits provider-level characterization, substrate generalization, and
Ordinal. Within-provider variance per brand is 1 df (2 models/provider), partially
offset by pooling 112 brands. Phase is exploratory / descriptive overall;
UNDETERMINED is a legitimate PRIMARY verdict.

Instrument inheritance: CV-CPC is Presence-coupled (v1.7). The Beyond_Presence gate,
not the bare Asymmetry test, carries the substantive claim.

Recompute provenance: v0.20/0.21/0.22 externally anchored to v1.7 r_per_model;
v0.19 and v0.23 rest on v0.31's extraction-function provenance alone.
"""

# ---------------------------------------------------------------------------
# FALSIFICATION (kept; repointed to the four hypotheses)
# ---------------------------------------------------------------------------
FALSIFICATION = """
Per-hypothesis falsification is defined in HYPOTHESES (falsified_iff):
- H_Provider_Asymmetry:      eta^2 within permutation-null envelope.
- H_Provider_Beyond_Presence: delta_eta2 <= 0 or within null (restates Presence).
- H_Provider_Ordinal:        Kendall's W n.s. (interpreted as UNINFORMATIVE at N=5, not disconfirming).
- H_Provider_Phantom:        exploratory; not falsifiable in this phase.
"""

# ---------------------------------------------------------------------------
# FIGURES (re-analysis set - one per finding)
# ---------------------------------------------------------------------------
FIGURES = [
    {"id": "fig1", "topic": "eta2_by_provider",
     "desc": "Between-provider variance share (eta^2) of CV-CPC across 112 brands, by substrate."},
    {"id": "fig2", "topic": "delta_eta2_cvcpc_minus_cp",
     "desc": "delta_eta2 = eta^2_CVCPC - eta^2_CP with permutation null (the Beyond_Presence gate)."},
    {"id": "fig3", "topic": "provider_rank_table",
     "desc": "Within-pair consistency provider ranks across the 5 omnibus substrates (Kendall's W)."},
]

# ---------------------------------------------------------------------------
# DEVIATIONS
# ---------------------------------------------------------------------------
DEVIATIONS = []   # r1: substrate set corrected pre-lock (5-substrate omnibus); no Entry 0.
