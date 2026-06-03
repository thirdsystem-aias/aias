"""
v0.30 (CPC.01) — CPC Consistency Instrument Specification Pilot
Pre-registration content module (ANALYSIS pre-registration).

Specifies and stress-tests a coefficient-of-variation Consistency instrument
(CPC) on existing anchored data, to recommend a normalization choice to the
v1.7 methodology lock. CPC measures cross-model dispersion of recall: how
consistently a brand surfaces across the fixed six-model reference panel.

Confirmatory scope = CPC_model (dispersion across the fixed 6-model panel).
CPC_platform is defined but NOT measured (deferred — no platform harness).

This is an ANALYSIS pre-registration: it is locked at a git tag BEFORE any
scoring code runs. No new LLM calls; no brand selection; no acquisition. The
study reuses, verbatim, the locked 24-brand registries and the already-deposited
Phase A recognition + Phase B two-channel recall CSVs from three prior phases:
  v0.20 (skincare,   SSRN 6811441)
  v0.21 (cosmetics,  SSRN 6815378)
  v0.22 (automotive, SSRN 6829118)

The designed outcome is F2-then-F3: demonstrate that raw cross-model CV is
contaminated by Presence level, then show a level-correction neutralizes that
confound — handing the v1.7 lock a validated normalization. If F3 fails, the
pre-committed fallback (residualized-CV variant or an ICC/agreement-coefficient
reformulation) is itself a legitimate publishable result.
"""

# ---------------------------------------------------------------------------
# STUDY METADATA
# ---------------------------------------------------------------------------

STUDY_TITLE = "AIAS CPC: A Level-Corrected Cross-Model Consistency Coefficient"
STUDY_SUBTITLE = (
    "An analysis pre-registration specifying and stress-testing a "
    "coefficient-of-variation Consistency instrument (CPC) on anchored "
    "v0.20 / v0.21 / v0.22 recall data, to recommend a normalization to the "
    "v1.7 methodology lock"
)
VERSION = "v0.30"
PROTOCOL_LOCK = "v1.6 (reused data under v1.6-era locks); recommendation target: v1.7 normalization lock"
DESIGN_TYPE = "Instrument Specification — Consistency (CPC) pilot; analysis pre-registration (no new acquisition)"
# Repurposed from the inherited CV-series index. v0.30 is an instrument pilot,
# not a Construct-Validity-series entry — flagged in the mapping report.
CV_INDEX = "CPC.01 (instrument-specification pilot; NOT a Construct-Validity-series entry)"

# Repurposed from the inherited Campbell-Fiske MTMM cell. v0.30 is not an MTMM
# cell — it is a Consistency (C-component) instrument pilot. Confirmatory scope
# is CPC_model (cross-model dispersion); CPC_platform is defined but deferred.
MTMM_CELL = (
    "n/a — Consistency (C-component) instrument pilot. Confirmatory scope = "
    "CPC_model (dispersion across the fixed 6-model panel). CPC_platform "
    "specified, measurement deferred."
)
# Repurposed: the three reused source phases (data providers), not companion
# MTMM studies.
PAIRS_WITH = {
    "v0.20": "skincare (SSRN 6811441) — locked 24-brand registry; Phase A recognition + Phase B recall CSVs (CPC data source)",
    "v0.21": "cosmetics (SSRN 6815378) — locked 24-brand registry; Phase A + Phase B CSVs (CPC data source)",
    "v0.22": "automotive (SSRN 6829118) — locked 24-brand registry; Phase A + Phase B CSVs (CPC data source; heritage-ceiling substrate)",
}

# ---------------------------------------------------------------------------
# FROZEN ARTIFACTS (locked pre-analysis)
# ---------------------------------------------------------------------------
# No new panel and no acquisition. The "frozen" artifacts are the reused
# registries and the already-deposited CSVs, plus the CPC instrument
# definition itself. Seed retained (program-standard) for reproducible BCa
# bootstrap CIs on the confound correlations; no brand selection uses it.

SEED = 280400

# Repurposed file pointers (no new panel/validator in an analysis prereg):
PANEL_FILE = "(reused) locked 24-brand registries from v0.20, v0.21, v0.22 — no new panel"
VALIDATOR_FILE = "(reused) Phase A recognition + Phase B two-channel recall CSVs already deposited for v0.20 / v0.21 / v0.22"
PRESENCE_FILE = "osf/v30/data/v30_cpc.csv"   # CPC output (brand, substrate, mu, sd, cpc_raw, cpc_corr, cpc_resid, L, defined)

PANEL_N = 24   # per substrate; 3 substrates -> 72 brand-substrate cells before degenerate-cell exclusion

# ---------------------------------------------------------------------------
# DATA PROVENANCE — REUSED ANCHORED CORPUS (no new acquisition)
# ---------------------------------------------------------------------------
# Repurposed from the inherited external-criterion (BRAND database) block.
# Here the "source" is the program's own prior anchored data, reused verbatim.

BRAND_SOURCE = {
    "type": "reused anchored corpus — NO new acquisition, NO new LLM calls",
    "source_phases": {
        "v0.20": "skincare — SSRN 6811441",
        "v0.21": "cosmetics — SSRN 6815378",
        "v0.22": "automotive — SSRN 6829118",
    },
    "registries": "locked 24-brand registries, reused verbatim (no brand selection)",
    "inputs": (
        "Phase A recognition CSV + Phase B two-channel recall CSV already "
        "deposited per phase; CPC is computed from the Phase B recall channel."
    ),
    "model_panel": "fixed six-model reference panel (see REFERENCE_PANEL)",
    "integrity": (
        "sha256 + row/column counts of each reused CSV certified against the "
        "deposited files at lock (see VERIFICATION); hashes recorded at the "
        "lock commit, not invented here."
    ),
}

# ---------------------------------------------------------------------------
# CORPUS COMPOSITION (no construction — reuse only)
# ---------------------------------------------------------------------------
# Repurposed from the inherited panel-construction block. There is NO panel
# construction in v0.30: registries are reused verbatim.

PANEL_CONSTRUCTION = {
    "selection": "NONE — registries reused verbatim; no brand selection, no acquisition",
    "substrates": ["v0.20 skincare", "v0.21 cosmetics", "v0.22 automotive"],
    "panel_n_per_substrate": PANEL_N,
    "brand_substrate_cells": 72,    # 24 x 3, before degenerate-cell exclusion
    "dispersion_population": "the fixed 6-model panel is the FULL reference population (population SD, divide by 6)",
    "note": (
        "Automotive (heritage ceiling) is the substrate predicted to show the "
        "largest recognition->recall coverage gap and the highest raw-CV "
        "inflation (see PREDICTIONS)."
    ),
}

# ---------------------------------------------------------------------------
# REFERENCE PANEL (fixed six-model population)
# ---------------------------------------------------------------------------
# The six models are treated as the FULL reference population, so panel
# dispersion uses POPULATION SD (divide by 6), not sample SD.

REFERENCE_PANEL = [
    "claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o",
    "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite",
]

# ---------------------------------------------------------------------------
# CPC INSTRUMENT — OPERATIONAL DEFINITIONS
# ---------------------------------------------------------------------------
# Repurposed from the inherited PRESENCE_PROTOCOL (acquisition protocol).
# Here it carries the CPC instrument's operational definitions: the quantity
# being specified, not a measurement to be acquired.

PRESENCE_PROTOCOL = {
    "recall_signal": (
        "Per-cell recall signal s(b,m) = fraction of Phase B recall "
        "probe-channel opportunities (6 probes x 2 channels) in which brand b "
        "surfaced in model m's response. Bounded [0,1]. Each brand -> a "
        "6-vector across the reference-panel models."
    ),
    "dispersion": (
        "Panel dispersion uses POPULATION SD (divide by 6): the six models are "
        "the full reference population."
    ),
    "cpc_raw": "CPC_raw = SD_m[s] / mean_m[s]  (cross-model CV of recall; lower = more consistent)",
    "cpc_corr_primary": (
        "CPC_corr (PRIMARY, level-corrected) = SD_m[s] / sqrt(mu*(1-mu)), "
        "mu = mean_m[s]. The denominator is the maximum attainable SD for any "
        "[0,1] variable with mean mu (Bhatia-Davis), so CPC_corr in [0,1] = "
        "dispersion as a fraction of the maximum possible at that level."
    ),
    "robustness_variant": (
        "Level-residualized CV (CV regressed on mu, residuals retained). "
        "Reported, NOT primary."
    ),
    "level_variable_L": (
        "L(b) = Phase A Presence C_P (recognition-based AIAS 1.0 score). "
        "Deliberately a DIFFERENT signal than the recall mean inside CPC, so "
        "the confound test is non-tautological (it tests whether CPC is "
        "redundant with Presence, not with its own input)."
    ),
    "degenerate_cell_rule": (
        "A brand is CPC-UNDEFINED if mu == 0 (recall floor) or mu >= 0.98 "
        "(recall ceiling); excluded from CPC distributions. The COVERAGE RATE "
        "(share of brands with defined CPC) is itself a primary outcome (F1)."
    ),
    "cpc_platform_deferred": (
        "CPC_platform (specified, DEFERRED): the same dispersion taken across "
        "deployment surfaces (consumer app vs API, with their retrieval / "
        "system-prompt augmentation) rather than across model weights. Needs a "
        "platform harness not in the pipeline; measurement deferred."
    ),
    "confirmatory_scope": "CPC_model only (cross-model dispersion over the fixed 6-model panel)",
}

# ---------------------------------------------------------------------------
# DECISION RULES — LOCKED NUMERIC THRESHOLDS
# ---------------------------------------------------------------------------
# The inherited correlation-band constants are REPURPOSED to CPC's
# level-confound thresholds. NOTE (flagged in mapping): CONVERGENT_BENCHMARK
# and CONFIRMED_CEIL no longer carry their inherited discriminant-validity
# meaning. New CPC-specific thresholds are added below them (additive; does
# not break the schema backbone).

CONVERGENT_BENCHMARK = 0.30   # REPURPOSED -> F2 confound benchmark: |rho(CPC_raw, L)| >= this => level confound present
CONFIRMED_CEIL = 0.20         # REPURPOSED -> F3 corrected ceiling: |rho(CPC_corr, L)| < this => confound neutralized
MIN_N = 12                    # min defined-CPC brands in a substrate for a valid rho (carried CV-family floor)
N_BOOT = 10000                # BCa bootstrap resamples for the confound-rho CIs (reported)
BOOTSTRAP_SEED = SEED

# CPC-specific thresholds (new; no inherited analog):
COVERAGE_FLOOR = 0.50         # F1: defined-CPC coverage must be >= 50% of brands per substrate
ATTENUATION_CONFIRM = 0.50    # F3 confirm: corrected rho must attenuate >= 50% vs raw
ATTENUATION_FLOOR = 0.30      # F3 falsify: attenuation < 30% => F3 FALSIFIED
KW_ALPHA = 0.05               # F4: Kruskal-Wallis significance threshold
CEIL_MU = 0.98                # degenerate-cell recall ceiling
FLOOR_MU = 0.0                # degenerate-cell recall floor

# Repurposed correlation bands -> CPC level-confound interpretation bands.
BANDS_ABS_RHO = {
    "CONFOUND_PRESENT": "|rho(CPC_raw, L)| >= 0.30           (F2: level contamination present)",
    "RESIDUAL":         "0.20 <= |rho(CPC_corr, L)| < 0.30   (correction incomplete / partial)",
    "NEUTRALIZED":      "|rho(CPC_corr, L)| < 0.20           (F3: correction removed the confound)",
}

# ---------------------------------------------------------------------------
# HYPOTHESES (F1-F4 confirmatory; one exploratory)
# ---------------------------------------------------------------------------
# All four falsification hypotheses are confirmatory (CPC_model scope). F2-then-F3
# is the load-bearing pair that hands v1.7 a validated normalization. The
# recognition-vs-recall rank concordance is exploratory (non-confirmatory).

HYPOTHESES = {
    "H_CPC_Computable": {
        "role": "CONFIRMATORY",
        "falsification_id": "F1",
        "label": "Recall yields a usable consistency signal where recognition saturates",
        "claim": (
            "Recall CPC-coverage (share of brands with defined CPC) is >= 50% "
            "of brands in ALL three substrates, AND recall coverage exceeds "
            "recognition coverage on automotive."
        ),
        "outcome_variable": "defined-CPC coverage rate per substrate",
        "verdict_taxonomy": {
            "CONFIRM": "recall CPC-coverage >= 50% in all 3 substrates AND recall coverage > recognition coverage on automotive",
            "FALSIFIED": "recall coverage < 50% in any substrate, OR recall coverage <= recognition coverage on automotive",
        },
        "falsification": "recall coverage < 50% in any substrate, or recall <= recognition coverage on automotive",
    },
    "H_CPC_LevelConfound": {
        "role": "CONFIRMATORY",
        "falsification_id": "F2",
        "label": "Raw cross-model CV is contaminated by Presence level",
        "claim": (
            "Significant |rho(CPC_raw, L)| >= 0.30 in >= 2 of the 3 substrates "
            "(L = Phase A Presence C_P)."
        ),
        "statistic": "Spearman rho(CPC_raw, L) per substrate; BCa 95% CI (10k, seed 280400)",
        "thresholds": dict(BANDS_ABS_RHO),
        "verdict_taxonomy": {
            "CONFIRM": "significant |rho(CPC_raw, L)| >= 0.30 in >= 2 of 3 substrates",
            "FALSIFIED": "not significant, or |rho| < 0.30 across substrates",
        },
        "falsification": "rho not significant or |rho| < 0.30 across all substrates",
    },
    "H_CPC_LevelCorrected": {
        "role": "CONFIRMATORY (HEADLINE — the normalization recommendation)",
        "falsification_id": "F3",
        "label": "The Bhatia-Davis level-correction removes the confound",
        "claim": (
            "|rho(CPC_corr, L)| < 0.20 AND >= 50% attenuation vs CPC_raw, in "
            ">= 2 of the 3 substrates."
        ),
        "statistic": "Spearman rho(CPC_corr, L) per substrate; attenuation = 1 - |rho_corr|/|rho_raw|",
        "thresholds": dict(BANDS_ABS_RHO),
        "verdict_taxonomy": {
            "CONFIRM": "|rho(CPC_corr, L)| < 0.20 AND attenuation >= 50% vs raw, in >= 2 of 3 substrates",
            "FALSIFIED": "attenuation < 30%, OR corrected rho remains significant at raw magnitude",
        },
        "falsification": "attenuation < 30% or corrected rho remains significant at raw magnitude",
        "fallback_if_falsified": (
            "Pre-committed v1.7 recommendation becomes the residualized-CV "
            "variant OR an ICC / agreement-coefficient reformulation; that "
            "failure path is a legitimate publishable result."
        ),
    },
    "H_CPC_SubstrateVariation": {
        "role": "CONFIRMATORY",
        "falsification_id": "F4",
        "label": "Consistency is substrate-conditioned",
        "claim": (
            "Kruskal-Wallis across the 3 substrates' CPC_corr distributions is "
            "significant at p < .05."
        ),
        "statistic": "Kruskal-Wallis H across 3 substrates' CPC_corr",
        "verdict_taxonomy": {
            "CONFIRM": "Kruskal-Wallis significant at p < .05",
            "FALSIFIED": "no significant difference across substrates",
        },
        "falsification": "no significant difference (p >= .05)",
    },
    "H_CPC_RankConcordance": {
        "role": "EXPLORATORY",
        "tier": "DESCRIPTIVE",            # non-confirmatory; NO figure
        "falsification_id": None,
        "label": "Recognition-vs-recall CPC rank concordance",
        "claim": (
            "Rank concordance between recognition-based and recall-based CPC "
            "orderings, to inform the v1.7 channel decision."
        ),
        "reporting": "concordance statistic only; no figure; non-gating",
        "note": "Informs the v1.7 channel choice; not part of the confirmatory verdict set.",
    },
}

# ---------------------------------------------------------------------------
# REGISTERED PREDICTIONS (directional, pre-registered)
# ---------------------------------------------------------------------------

PREDICTIONS = {
    "designed_outcome": (
        "F2 confirms (confound demonstrated) then F3 confirms (confound "
        "neutralized) — the designed path that hands v1.7 a validated "
        "normalization."
    ),
    "fallback_recommendation": (
        "If F3 FAILS, the pre-committed fallback recommendation to v1.7 is the "
        "residualized-CV variant or an ICC / agreement-coefficient "
        "reformulation. That failure path is a legitimate publishable result."
    ),
    "substrate_prediction": (
        "Automotive (heritage ceiling) predicted to show the largest "
        "recognition->recall coverage gap (F1) and the highest raw-CV inflation."
    ),
}

# ---------------------------------------------------------------------------
# SCORING RULES
# ---------------------------------------------------------------------------

SCORING = {
    "confirmatory_scope": "CPC_model (cross-model dispersion over the fixed 6-model panel)",
    "confirmatory_family": [
        "H_CPC_Computable", "H_CPC_LevelConfound",
        "H_CPC_LevelCorrected", "H_CPC_SubstrateVariation",
    ],
    "headline_rests_on": ["H_CPC_LevelConfound", "H_CPC_LevelCorrected"],   # F2-then-F3
    "exploratory": ["H_CPC_RankConcordance"],
    "primary_cpc": "CPC_corr = SD_m[s] / sqrt(mu*(1-mu))  (Bhatia-Davis level-corrected)",
    "raw_cpc": "CPC_raw = SD_m[s] / mean_m[s]",
    "robustness_variant": "level-residualized CV (reported, non-primary)",
    "dispersion": "POPULATION SD (divide by 6); the 6-model panel is the full reference population",
    "level_variable": "L(b) = Phase A Presence C_P (recognition-based AIAS 1.0 score)",
    "confound_statistic": "Spearman rho(CPC, L) per substrate",
    "substrate_statistic": "Kruskal-Wallis across 3 substrates' CPC_corr",
    "ci_method": "BCa bootstrap 95% CI",
    "bootstrap_resamples": N_BOOT,
    "bootstrap_seed": BOOTSTRAP_SEED,
    "min_n_for_valid_rho": MIN_N,
    "coverage_floor": COVERAGE_FLOOR,
    "confound_rho_min": CONVERGENT_BENCHMARK,    # repurposed constant (F2 = 0.30)
    "corrected_ceiling": CONFIRMED_CEIL,         # repurposed constant (F3 = 0.20)
    "attenuation_confirm": ATTENUATION_CONFIRM,
    "attenuation_floor": ATTENUATION_FLOOR,
    "kw_alpha": KW_ALPHA,
    "degenerate_cell_rule": (
        "UNDEFINED if mu == 0 (floor) or mu >= 0.98 (ceiling); excluded from "
        "CPC distributions; coverage rate is itself the F1 outcome"
    ),
    "no_new_acquisition": True,
    "no_new_llm_calls": True,
    "cpc_output": PRESENCE_FILE,
}

# ---------------------------------------------------------------------------
# VERIFICATION DISCIPLINE
# ---------------------------------------------------------------------------
# Binary cross-verification applies to the REUSED corpus: every paper-grade
# figure (CSV row/column counts, sha256, coverage and degenerate-cell counts)
# is independently re-derived, not trusted from a single parse. Hashes for the
# reused CSVs are recorded at the lock commit (not fabricated here).

VERIFICATION = {
    "policy": "binary cross-verification for every paper-grade figure",
    "tools": ["grep", "stat", "shasum", "wc"],
    "verify_targets": [
        "sha256 + row/column counts of each reused v0.20 / v0.21 / v0.22 Phase A + Phase B CSV, vs the deposited files",
        "six-model reference-panel membership present in every reused CSV",
        "degenerate-cell counts (mu == 0 / mu >= 0.98) per substrate, independently re-derived",
        "defined-CPC coverage rate per substrate, independently re-counted (F1)",
    ],
    "reused_csv_sha256": "certified at r2 — full hashes in osf/v30/v30_run_log.md and DEVIATIONS Entry 1 (v0.20 / v0.21 / v0.22 Phase A + Phase B)",
    "uncertified_handling": "flag explicitly in artifact and paper",
}

# ---------------------------------------------------------------------------
# ANALYSIS PIPELINE
# ---------------------------------------------------------------------------

ANALYSIS_STEPS = [
    "1. Load the reused Phase A recognition + Phase B recall CSVs for v0.20, v0.21, v0.22; "
    "verify integrity (sha256 + row/column counts vs deposited files).",
    "2. Build per-cell recall signal s(b,m) = fraction of Phase B recall probe-channel "
    "opportunities (6 probes x 2 channels) in which brand b surfaced in model m -> 6-vector per brand.",
    "3. Compute mu = mean_m[s] and POPULATION SD_m[s] (divide by 6). Apply the degenerate-cell rule "
    "(mu == 0 or mu >= 0.98 -> UNDEFINED). Record defined-CPC coverage rate per substrate (F1).",
    "4. CPC_raw = SD/mu; CPC_corr = SD/sqrt(mu*(1-mu)); plus the level-residualized-CV robustness variant.",
    "5. Level variable L(b) = Phase A Presence C_P. F2: Spearman rho(CPC_raw, L) per substrate; "
    "F3: rho(CPC_corr, L) and attenuation vs raw; BCa 95% CIs (10k, seed 280400).",
    "6. F4: Kruskal-Wallis across the 3 substrates' CPC_corr distributions (alpha = .05).",
    "7. Exploratory: recognition-vs-recall CPC rank concordance (no figure; informs v1.7 channel choice).",
    "8. Resolve F1-F4 verdicts; write osf/v30/v30_cpc_verdicts.json and osf/v30/data/v30_cpc.csv.",
]

# ---------------------------------------------------------------------------
# DEVIATIONS LOG
# ---------------------------------------------------------------------------
# This is an ANALYSIS pre-registration locked at tag before any scoring code
# runs. Per program convention Entry 0 is the ex-ante scope lock. No new
# acquisition occurs, so there is no per-phase COI sampling screen; the reused
# registries carry the COI screens already applied in their source phases
# (v0.20 / v0.21 / v0.22 after the r2 substrate swap; see Entry 1), and Samsung
# is disclosed only in Declarations COI of the formal paper, never in the author
# block.

DEVIATIONS = [
    {
        "entry_id": "Entry 0",
        "type": "scope lock (ex-ante, pre-analysis)",
        "ex_ante": True,
        "logged_before_any_scoring_code": True,
        "is_analysis_prereg": True,
        "items": {
            "a": (
                "CPC_platform is specified but its empirical measurement is "
                "DEFERRED (no platform harness in the pipeline)."
            ),
            "b": (
                "No new LLM calls; reuse the existing v0.20 / v0.21 / v0.22 "
                "Phase A + Phase B data verbatim."
            ),
            "c": (
                "The recall channel is the primary CPC input; recognition "
                "enters only as the F1 coverage comparator and as the "
                "independent level variable L(b) = Phase A Presence C_P."
            ),
        },
        "coi_note": (
            "No brand selection in v0.30 — reused registries carry their "
            "source-phase COI screens; Samsung disclosed only in Declarations "
            "COI of the paper, never in the author block."
        ),
        "lock_state": "v0.30-prereg-r1",
    },
    {
        "entry_id": "Entry 1",
        "type": "substrate-set amendment (pre-analysis)",
        "ex_ante": True,
        "logged_before_any_scoring_code": True,
        "revision": "r2",
        "title": "Swap v0.18 + v0.24 -> v0.20 + v0.21 to restore a doubly-homogeneous apparatus",
        "finding": (
            "STEP-1 input certification (osf/v30/v30_run_log.md) showed two r1 substrates violate the "
            "locked apparatus premise: v0.24 (B2B SaaS) was acquired on Opus 4.7 / Sonnet 4.6, not the "
            "fixed 4.5 panel; v0.18 (indie fragrance) is single-channel (3 flat frames, no R_cat/R_cult). "
            "Each breaks a literal r1 premise (panel 'fixed from v0.17 onward, present in every CSV'; "
            "recall 'two-channel')."
        ),
        "resolution": (
            "Substrate set amended v0.18 -> v0.20 (skincare, SSRN 6811441) and v0.24 -> v0.21 (cosmetics, "
            "SSRN 6815378); v0.22 (automotive, SSRN 6829118) retained. Certification confirms v0.20 / "
            "v0.21 / v0.22 are identical apparatus: 4.5 Claude pair + the four shared non-Claude models, "
            "two-channel canonical recall (3 frames/channel, 6/model), 24 brands, locked registries, "
            "reusable matchers (score_v20/21/22.py)."
        ),
        "consequence": (
            "The r1 panel-identity and two-channel premises now hold literally across all three "
            "substrates. No role-slot reframe and no F4 sensitivity are required; F4 (cross-substrate "
            "CPC variation) is confound-free and stays exactly as locked in r1."
        ),
        "il_spread_note": (
            "Trio leans mid-to-high IL (skincare mid; cosmetics, automotive mid-high); the niche/low-IL "
            "anchor is forfeited. F1's saturation contrast is preserved: automotive saturates recognition "
            "(heritage ceiling); skincare/cosmetics do not."
        ),
        "unchanged_from_r1": (
            "EXPLICITLY UNCHANGED: all F1-F4 definitions and thresholds, CPC_raw / CPC_corr (Bhatia-Davis) "
            "/ residualized-CV definitions, the degenerate-cell rule, CPC_model scope, no-new-LLM-calls. "
            "r2 changes ONLY the three substrate identities and the provenance fields naming them."
        ),
        "certified_inputs": {
            "v0.20": "phase_a c8ad6335c982ec95...; phase_b 4791113a93b8a258...",
            "v0.21": "phase_a d470940aa497f555...; phase_b 45e4c3acca67f8c6...",
            "v0.22": "certified at STEP 1 (run log)",
        },
        "v1_7_forward_note": (
            "Pilot lesson for the v1.7 lock: deposited substrates vary in panel generation and recall "
            "channel structure; v1.7 should mandate an apparatus-homogeneity screen (panel generation + "
            "channel structure + frame count) as a precondition for any cross-substrate CPC comparison."
        ),
        "lock_state": "v0.30-prereg-r2",
    },
]

# Entry 0 is the scope lock above; alias kept for any downstream tooling that
# references COI_SCREEN by name (no separate COI sampling screen in v0.30).
COI_SCREEN = DEVIATIONS[0]
