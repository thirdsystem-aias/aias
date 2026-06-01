"""
v0.28 (CV.04) — BRAND Discriminant Validator
Pre-registration content module.

Tests whether the AIAS Presence score is DISCRIMINANT from established external
brand-norm measures — i.e. that Presence is not merely re-measuring brand
familiarity or recognition memory. The external criterion is the BRAND database
(Raffaelli, Bocchi, Estes & Adelman, 2025), the most comprehensive open
familiarity / recognition norm set for top US brands.

Design type:   Construct Validity — Discriminant (cross-sectional, correlational)
Protocol lock: v1.6 (SSRN 6816340)
Prior CV studies in the chain:
  v0.25 (CV.01) Google Trends CONVERGENT validity, B2B SaaS  — rho = 0.74 anchor
  v0.26 (CV.02) Amazon BSR predictive validity (cross-substrate)
  v0.27 (CV.03) third-party AI-visibility convergent validity, B2B SaaS

The v0.25 convergent anchor (rho = 0.74) is the discriminant BENCHMARK here: a
measure that is genuinely distinct from familiarity should correlate with it
*well below* the level at which Presence tracks a convergent instrument.
"""

# ---------------------------------------------------------------------------
# STUDY METADATA
# ---------------------------------------------------------------------------

STUDY_TITLE = "AIAS Presence × BRAND Norms: Discriminant Validity on a Tech Panel"
STUDY_SUBTITLE = (
    "Testing whether AI Presence is distinct from brand familiarity and "
    "recognition memory, using the BRAND database as external criterion"
)
VERSION = "v0.28"
PROTOCOL_LOCK = "v1.6"
DESIGN_TYPE = "Construct Validity — Discriminant"
CV_INDEX = "CV.04"

# Multitrait-multimethod framing: this study occupies the DISCRIMINANT cell of a
# Campbell-Fiske matrix for AIAS Presence — Presence (one method) measured against
# human familiarity / recognition norms (a different trait family). It is read
# jointly with its convergent and predictive companions.
MTMM_CELL = "discriminant (Presence x human familiarity/recognition)"
PAIRS_WITH = {
    "v0.25": "CV.01 convergent — Google Trends (rho = 0.74 anchor)",
    "v0.26": "CV.02 discriminant — Amazon BSR (cross-substrate predictive)",
}

# ---------------------------------------------------------------------------
# FROZEN ARTIFACTS (locked pre-acquisition)
# ---------------------------------------------------------------------------
# The panel and the validator values are FROZEN before any Presence measurement.
# Selection seed is recorded so the draw is reproducible from the BRAND source.

SEED = 280400

PANEL_FILE = "prereg/v0_28_panel_brands.txt"          # 24 Tech brands, frozen
VALIDATOR_FILE = "prereg/v0_28_brand_validator.csv"   # brand, familiarity_1_7, dprime
PRESENCE_FILE = "osf/v28/data/v0.28_presence.csv"     # brand, presence (acquisition output)

PANEL_N = 24

# ---------------------------------------------------------------------------
# EXTERNAL CRITERION — BRAND DATABASE PROVENANCE (verified)
# ---------------------------------------------------------------------------
# Acquired from the authors' ResearchBox repository (NOT OSF). Brand-level norms
# are in the single sheet 'BRAND' of BRAND_dataset.xlsx; header is on row 3.
# Verified column mapping (header-discovered, not assumed):
#   col B = Brand Name
#   col C = Category
#   col H = Familiarity M  (1-7 Likert mean)   -> validator 'familiarity_1_7'
#   col Y = d'             (recognition-memory sensitivity, SDT block T..AA)
#                                               -> validator 'dprime'

BRAND_SOURCE = {
    "dataset": "BRAND: Brand recognition and attitude norms database",
    "citation": "Raffaelli, Bocchi, Estes & Adelman (2025), Behavior Research Methods 57:17",
    "doi": "10.3758/s13428-024-02525-x",
    "repository": "ResearchBox 1892 (https://researchbox.org/1892)",
    "file": "ResearchBox 1892/Materials/BRAND_dataset.xlsx",
    "file_size_bytes": 51693499,
    "file_sha256": "1a440ceeb74920f776e54d0c053d9e5c5f1149b6d9d3f66568cd312bb39a7ce5",
    "sheet": "BRAND",
    "header_row": 3,
    "columns": {"brand": "B", "category": "C", "familiarity_1_7": "H", "dprime": "Y"},
    "underlying_list": "Brand Finance US 500 (+ 2024 additions); 597 brands total",
}

# ---------------------------------------------------------------------------
# PANEL CONSTRUCTION (locked rationale)
# ---------------------------------------------------------------------------
# Substrate = the BRAND 'Tech' category. Frame reduction is 80 -> 70 -> 69:
#   80  Tech brands in BRAND
#   70  carry complete Familiarity + d' (10 blank on one or both -> dropped)
#   69  after the ex-ante Samsung-owned COI screen removes Harman International
#       (DEVIATIONS Entry 0; Samsung-owned since 2017; was a mid-tertile candidate)
# The COI-screened 69-brand frame was split into familiarity terciles (23 each)
# and 8 brands were drawn at random per tertile (seed 280400), giving the 24-brand
# panel spanning the full familiarity range (1.00–6.83) and a wide d' range.
#
# Tech is chosen as an ADVERSARIAL substrate for discriminant validity: it is the
# most familiarity-variance-rich category in BRAND, so it is the category where
# Presence is MOST likely to track familiarity. A discriminant result here is
# therefore a strong test, not a favorable one.

PANEL_CONSTRUCTION = {
    "substrate": "BRAND 'Tech' category",
    "category_n_total": 80,
    "complete_data_frame_n": 70,      # complete familiarity_1_7 AND dprime
    "data_exclusion": "10 Tech brands blank on familiarity or d'",
    "coi_screened_frame_n": 69,       # after Samsung-owned removal (Harman)
    "coi_exclusion": "Harman International (Samsung-owned) — see DEVIATIONS Entry 0",
    "stratification": "familiarity terciles of the COI-screened 69-brand frame (23 each), 8 drawn per tertile",
    "seed": SEED,
    "panel_n": PANEL_N,
    "familiarity_range_in_panel": [1.0, 6.833],
    "note": "Tech is adversarial for discriminance (max familiarity variance).",
}

# ---------------------------------------------------------------------------
# AIAS PRESENCE ACQUISITION
# ---------------------------------------------------------------------------
# Presence is measured over the 24 frozen panel brands using the locked six-model
# reference panel. The validator (familiarity, d') is fixed; only Presence is
# acquired after this pre-registration is locked.

REFERENCE_PANEL = [
    "claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o",
    "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite",
]

PRESENCE_PROTOCOL = {
    "join_key": "brand (exact, then case-insensitive)",
    "presence_definition": (
        "AIAS Presence score over the Tech panel (acquisition output written to "
        "osf/v28/data/v0.28_presence.csv with columns brand,presence)."
    ),
    "phase_a": "Recognition — 24 brands x 6 models = 144 probes",
    "phase_b": "Two-channel recall (category-canonical R_cat + cultural R_cult)",
    "model_panel_lock": "six-model reference panel fixed from v0.17 onward",
    "composition": "Presence composed per Protocol v1.6 (SSRN 6816340)",
    "blinding": (
        "Presence is acquired BLIND to per-brand validator values: the BRAND "
        "familiarity / d' figures are frozen before acquisition and are not "
        "consulted during Phase A/B measurement. The validator is the criterion, "
        "never an input to the measure under test."
    ),
    "frozen_before_acquisition": ["panel brands", "familiarity_1_7", "dprime"],
}

# ---------------------------------------------------------------------------
# DECISION RULES — LOCKED NUMERIC THRESHOLDS
# ---------------------------------------------------------------------------
# Convergent benchmark is the v0.25 Google Trends anchor. Bands are evaluated on
# |rho| (a strong NEGATIVE Presence–familiarity relationship is NOT discriminant);
# signed rho and a negative_correlation flag are reported alongside.

CONVERGENT_BENCHMARK = 0.74      # v0.25 (CV.01) Google Trends convergent anchor
CONFIRMED_CEIL = 0.50            # |rho| below -> CONFIRMED (discriminant)
MIN_N = 12                       # below -> UNDETERMINED
N_BOOT = 10000                   # BCa bootstrap resamples
BOOTSTRAP_SEED = SEED

BANDS_ABS_RHO = {
    "CONFIRMED": "|rho| < 0.50            (discriminant: distinct from criterion)",
    "PARTIAL":   "0.50 <= |rho| < 0.74    (partial overlap with criterion)",
    "FALSIFIED": "|rho| >= 0.74           (converges; not discriminant)",
}

# ---------------------------------------------------------------------------
# HYPOTHESES
# ---------------------------------------------------------------------------
# Two load-bearing correlation hypotheses (primary + secondary) and one
# DESCRIPTIVE dissociation pattern (tertiary, non-gating). The phase headline
# rests on H_Disc_Familiarity and H_Disc_Recognition only.

HYPOTHESES = {
    "H_Disc_Familiarity": {
        "role": "PRIMARY",
        "label": "Presence is discriminant from brand familiarity",
        "claim": (
            "Spearman rho between AIAS Presence and BRAND familiarity (1-7) over "
            "the 24-brand Tech panel falls below the convergent benchmark, "
            "|rho| < 0.50."
        ),
        "criterion_column": "familiarity_1_7",
        "rationale": (
            "If Presence merely re-measured familiarity it would correlate with "
            "it near the v0.25 convergent level (0.74). A discriminant measure "
            "correlates well below that ceiling."
        ),
        "test": "Spearman primary (drives verdict); Pearson secondary (reported)",
        "thresholds": dict(BANDS_ABS_RHO),
        "verdict_taxonomy": {
            "CONFIRMED": "|rho| < 0.50",
            "PARTIAL": "0.50 <= |rho| < 0.74",
            "FALSIFIED": "|rho| >= 0.74",
            "UNDETERMINED": "n < 12  OR  BCa 95% CI (on |rho|) spans all three bands",
        },
        "falsification": "|rho| >= 0.74 (Presence converges with familiarity).",
    },
    "H_Disc_Recognition": {
        "role": "SECONDARY",
        "label": "Presence is discriminant from recognition memory",
        "claim": (
            "Spearman rho between AIAS Presence and BRAND recognition memory "
            "(d') over the panel falls below the convergent benchmark, "
            "|rho| < 0.50."
        ),
        "criterion_column": "dprime",
        "rationale": (
            "Recognition memory (d') is a distinct facet of brand knowledge from "
            "familiarity; a discriminant Presence measure should also stay below "
            "the convergent ceiling against it."
        ),
        "test": "Spearman primary; Pearson secondary; same |rho| bands",
        "thresholds": dict(BANDS_ABS_RHO),
        "verdict_taxonomy": {
            "CONFIRMED": "|rho| < 0.50",
            "PARTIAL": "0.50 <= |rho| < 0.74",
            "FALSIFIED": "|rho| >= 0.74",
            "UNDETERMINED": "n < 12  OR  BCa 95% CI (on |rho|) spans all three bands",
        },
        "falsification": "|rho| >= 0.74 (Presence converges with recognition memory).",
    },
    "H_Dissociation": {
        "role": "TERTIARY",
        "tier": "DESCRIPTIVE",                 # non-gating; excluded from headline
        "label": "Presence / familiarity dissociation cases",
        "claim": (
            "Within the panel, individual brands show Presence that is amplified "
            "or suppressed relative to familiarity. Standardize Presence and "
            "familiarity within the n=24 panel; for each brand compute "
            "d = z(Presence) - z(familiarity). Amplified if d > +1.0, suppressed "
            "if d < -1.0."
        ),
        "z_reference": "panel (n=24), population standard deviation",
        "direction_rule": "amplified d > +1.0 ; suppressed d < -1.0",
        "verdict_taxonomy": {
            "FULL": ">= 4 cases AND both directions present",
            "PARTIAL": "1-3 cases, OR >= 4 cases all one-directional",
            "ABSENT": "0 cases",
        },
        "reporting": "count + named brands per direction (amplified / suppressed)",
        "note": (
            "Mechanically coupled to H_Disc_Familiarity (same Presence and "
            "familiarity vectors); corroborating / illustrative of the primary "
            "rho, NOT an independent test. Non-gating."
        ),
    },
}

# ---------------------------------------------------------------------------
# REGISTERED PREDICTION (directional, pre-registered)
# ---------------------------------------------------------------------------

PREDICTIONS = {
    "modal_expectation": "PARTIAL",
    "expected_rho_range": [0.30, 0.60],
    "rationale": (
        "Tech is the adversarial (max-familiarity-variance) substrate, so some "
        "Presence-familiarity overlap is expected; rho in 0.30-0.60 puts the "
        "modal outcome in the PARTIAL band. A CONFIRMED result here (|rho| < 0.50) "
        "would be strong evidence of discriminance precisely because the substrate "
        "was chosen to favor convergence."
    ),
    "negative_rho": (
        "If signed rho is strongly negative the negative_correlation flag is set; "
        "the verdict still bands on |rho| (a strong inverse relationship is not "
        "discriminant)."
    ),
}

# ---------------------------------------------------------------------------
# SCORING RULES
# ---------------------------------------------------------------------------

SCORING = {
    "primary_family": ["H_Disc_Familiarity", "H_Disc_Recognition"],
    "descriptive": ["H_Dissociation"],
    "statistic_primary": "Spearman rank correlation",
    "statistic_secondary": "Pearson (reported, non-gating)",
    "ci_method": "BCa bootstrap 95% CI",
    "bootstrap_resamples": N_BOOT,
    "bootstrap_seed": BOOTSTRAP_SEED,
    "min_n_for_valid_rho": MIN_N,
    "convergent_benchmark": CONVERGENT_BENCHMARK,
    "band_on": "abs(rho)",
    "report_signed_rho": True,
    "report_negative_correlation_flag": True,
    "verdict_basis": "point |rho| vs bands",
    "ci_role": "reported, NON-GATING",
    "ci_flags": {
        "ci_straddles_boundary": "|rho| CI interval crosses 0.50 or 0.74",
        "ci_excludes_reducibility": "|rho| CI upper bound < 0.74",
        "provisional": "CONFIRMED AND not ci_excludes_reducibility",
    },
    "undetermined_if": "n < 12  OR  |rho| CI spans all three bands",
    "headline_rests_on": ["H_Disc_Familiarity", "H_Disc_Recognition"],
    "dissociation_excluded_from_headline": True,
    "C_P_recompute": False,
    "presence_source": PRESENCE_FILE,
}

# ---------------------------------------------------------------------------
# VERIFICATION DISCIPLINE
# ---------------------------------------------------------------------------
# All paper-grade figures (validator values, panel composition, BRAND provenance,
# row/category counts) are binary-cross-verified against the source file with
# independent tools (unzip / grep / stat / shasum), not trusted from a single
# parse. Any value that could not be independently re-derived is flagged
# UNCERTIFIED in the artifact and in the paper.

VERIFICATION = {
    "policy": "binary cross-verification for every paper-grade figure",
    "tools": ["unzip", "grep", "stat", "shasum"],
    "uncertified_handling": "flag explicitly in artifact and paper",
    "binary_certified": {
        "brand_dataset_size_bytes": 51693499,
        "brand_dataset_sha256": "1a440ceeb74920f776e54d0c053d9e5c5f1149b6d9d3f66568cd312bb39a7ce5",
        "brand_total_data_rows": 597,        # grep '<row ' = 600 minus 3 header rows
        "tech_category_count": 80,           # <c r="C..."> resolving to 'Tech'
        "tech_complete_data_frame": 70,      # complete familiarity + d'
        "tech_coi_screened_frame": 69,       # after Samsung-owned (Harman) removal
    },
    "uncertified": [
        "per-category familiarity / d' means and SDs (stdlib aggregates; internally "
        "consistent across two independent inline parses, not re-derived by a "
        "non-Python tool)",
    ],
}

# ---------------------------------------------------------------------------
# ANALYSIS PIPELINE
# ---------------------------------------------------------------------------

ANALYSIS_STEPS = [
    "1. Load frozen validator (familiarity_1_7, dprime) and frozen 24-brand panel.",
    "2. Join AIAS Presence (osf/v28/data/v0.28_presence.csv) on brand name.",
    "3. H_Disc_Familiarity: Spearman rho(Presence, familiarity_1_7); Pearson alongside; "
    "BCa 95% CI (10k, seed 280400); band on |rho|.",
    "4. H_Disc_Recognition: same against d'.",
    "5. H_Dissociation (descriptive): within-panel z(Presence)-z(familiarity); "
    "classify amplified/suppressed; FULL/PARTIAL/ABSENT.",
    "6. Apply UNDETERMINED override (n<12 or CI spans all three bands); set "
    "ci_excludes_reducibility / provisional flags; write osf/v28/v28_verdicts.json.",
]

# ---------------------------------------------------------------------------
# DEVIATIONS LOG
# ---------------------------------------------------------------------------
# Per program convention (v0.21 onward), Entry 0 is the ex-ante COI screen.
# Entry 1 is a pre-acquisition SCOPE AMENDMENT logged before any data collection.
# This is r1, not an amendment to a prior committed methodology: no v0.28 data
# exists at lock time, so the reframing below defines the registration rather
# than departing from one.

DEVIATIONS = [
    {
        "entry_id": "Entry 0",
        "type": "COI screen (ex-ante, applied at FRAME level)",
        "ex_ante": True,
        "subject": "Samsung Electronics America (author's primary employer)",
        "samsung_affiliated_brands_in_panel": 0,
        "applied_at": "sampling frame, prior to the stratified tertile draw",
        "screen_method": (
            "Samsung-owned brands were excluded from the 70-brand usable Tech "
            "frame BEFORE the familiarity-tertile split, by case-insensitive match "
            "on samsung|harman|jbl|akg|smartthings. One brand was excluded: Harman "
            "International (Samsung-owned since 2017), which carried complete "
            "familiarity + d' and sat in the mid-familiarity tertile, i.e. it was "
            "an eligible candidate that the screen removed by design (not by seed). "
            "Seed 280400 was then applied to the COI-screened frame (n=69), 8 per "
            "tertile. Precedent: v0.19 AKG->Denon pre-screen-and-reseed. The frozen "
            "panel (prereg/v0_28_panel_brands.txt, all 24 brands) re-verifies "
            "COI-clean: grep samsung|harman|jbl|akg|smartthings -> zero matches."
        ),
        "frame_counts": "Tech 80/70/69: 80 in category; 70 with complete "
                        "familiarity + d'; 69 after Samsung-owned exclusion (Harman).",
        "rationale": (
            "After the frame-level screen, none of the 24 panel brands is Samsung- "
            "or Harman-affiliated (Motorola Solutions is the independent "
            "enterprise-networking company, not Samsung). Samsung is disclosed only "
            "in Declarations Section COI of the formal paper, never in the author "
            "block."
        ),
        "lock_state": "v0.28-prereg-r1",
    },
    {
        "entry_id": "Entry 1",
        "type": "scope amendment (pre-acquisition)",
        "ex_ante": True,
        "logged_before_data_collection": True,
        "is_r1_not_amendment": True,
        "title": "CV.04 reframed from Mental Availability (YouGov/CEP) to "
                 "discriminant validity vs human recognition/familiarity norms (BRAND)",
        "roadmap_specified": (
            "CV.04 as originally roadmapped: AIAS Presence x Mental Availability "
            "via YouGov BrandIndex / Category Entry Points (CEP)."
        ),
        "infeasibility": [
            "YouGov BrandIndex is licensed and operationalizes an awareness-funnel "
            "construct, not directly comparable and not openly available.",
            "CEP measurement requires a human-subjects survey, excluded by the "
            "program's standing ethics declaration (no human subjects).",
            "No public brand-level CEP dataset overlaps the existing registries.",
        ],
        "reframing": (
            "Retargeted to the DISCRIMINANT cell: AIAS Presence vs human recognition "
            "/ familiarity norms using the open BRAND database (familiarity 1-7, d')."
        ),
        "mental_availability_leg": "deferred to a future CV phase (Mental Availability leg)",
        "substrate_change": (
            "Moved from registry reuse (automotive 9/24 name-match, cosmetics 6/24, "
            "zero Cell-B coverage, and placeholder/blank validator values among the "
            "matches) to a PROSPECTIVE stratified 24-brand Tech panel drawn from "
            "BRAND's Tech category."
        ),
        "lock_state": "v0.28-prereg-r1",
    },
    {
        "entry_id": "Entry 2",
        "type": "methodology pin (pre-acquisition): Presence-bridge recall denominator",
        "ex_ante": True,
        "logged_before_data_collection": True,
        "revision": "r2",
        "title": "Pin the raw->Presence bridge to v1.6-canonical /18 recall "
                 "normalization (not v0.25's /36 literal)",
        "finding": (
            "The pinned Presence scalar reuses v0.25's presence_composite "
            "(score_v0_25.py) = equal-weighted mean of each component's "
            "fraction-of-max, *100. v0.25's code divides recall by 36. Empirical "
            "check of osf/v24/data/v24_phase_b.csv (the corpus behind the rho=0.74 "
            "anchor) shows that /36 came from a NON-canonical Phase B with 6 "
            "distinct frames per channel x 6 models (6 distinct probe_num in each "
            "of R_cat and R_cult). Protocol v1.6 canon is a SIX-frame battery = 3 "
            "frames per channel, max 18 per channel, max 36 across both channels "
            "(v1.6 SSRN 6816340: 'Phase B six-frame battery'; phantom layer "
            "'R_cat_phantom (max 18, q1-q3)', 'R_cult_phantom (max 18, q4-q6)'). "
            "The v0.28 r1 Phase B (q1-q3 R_cat, q4-q6 R_cult, max 18 each) is "
            "therefore CORRECT per v1.6; v0.24/25's 6-frame/channel design was the "
            "non-canonical instantiation."
        ),
        "pin": (
            "v0.28 normalizes recall on /18 (fraction of the v1.6 max-18), keeping "
            "the equal-weight fraction-of-max SEMANTIC of presence_composite but "
            "NOT copying v0.25's /36 literal: "
            "presence = mean(C_P/6, R_cat/18, R_cult/18) * 100. "
            "Implemented in scripts/bridge_v28.py."
        ),
        "anchor_commensurability_caveat": (
            "The rho=0.74 convergent anchor (v0.25) was computed on a non-canonical "
            "6-cue-per-channel recall; v0.28 uses the canonical 3-cue-per-channel "
            "recall. The discriminant-vs-benchmark comparison is therefore "
            "APPROXIMATE on recall cue breadth (3 vs 6 cues/channel). Carried to "
            "the paper's limitations section. Spearman is rank-based, so the "
            "uniform /18 normalization does not alter within-v0.28 brand ranks; the "
            "caveat concerns cross-study cue-breadth comparability, not internal "
            "validity."
        ),
        "unchanged_from_r1": (
            "EXPLICITLY UNCHANGED at r2: r1 Phase B (3 frames/channel) probe "
            "wording; the frozen panel and validator; Phase A probe; the three "
            "hypotheses and their |rho| bands; the Presence-composite definition "
            "(equal-weight fraction-of-max mean). r2 pins ONLY the bridge "
            "denominator and adds the bridge implementation."
        ),
        "lock_state": "v0.28-prereg-r2",
    },
]

# COI screen is DEVIATIONS Entry 0 above; this alias is kept for any downstream
# tooling that references COI_SCREEN by name.
COI_SCREEN = DEVIATIONS[0]
