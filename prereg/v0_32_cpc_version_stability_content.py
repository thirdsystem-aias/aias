"""
AIAS(TM) v0.32 -- CPC Version-Snapshot Stability
Pre-registration content module (r1).

Locked at git tag v0.32-prereg-r1 BEFORE any acquisition.
Phase type: PROSPECTIVE -- two acquisitions on a frozen registry, one per
model-vintage arm (before/after version contrast).
Registry: v0.22 automotive 24-brand list, reused verbatim.
Score: v1.7 CPC, computed independently per arm.

Snapshot resolution (probe-confirmed REACHABLE both arms; gate cleared):
  registries/v0_32_snapshot_resolution.json
Panel definition + neutral tier labels: registries/v0_32_registry.json
"""

PHASE_ID = "v0.32"
PHASE_TITLE = "CPC Version-Snapshot Stability"
METHODOLOGY_LOCK = "v1.7"            # SSRN 6878818 (CPC score as computed; see FRAMING)
INSTRUMENT_SOURCE = "v0.30"          # SSRN 6875319 (CPC instrument specification pilot)
BASELINE_SOURCE = "v0.31"            # SSRN 6880959 (CPC cross-category baseline)
PHASE_TYPE = "prospective_two_arm"   # new acquisition, twice; one run per vintage arm
PREREG_TAG = "v0.32-prereg-r1"
SUBSTRATE = "Automotive"             # true substrate; slug is construct-led (cpc_version_stability)

# ---------------------------------------------------------------------------
# FRAMING -- front of the methods, non-negotiable.
# ---------------------------------------------------------------------------
FRAMING = (
    "v1.7 (SSRN 6878818) established that the CV-based score CPC = 1/(1+CV) is "
    "NOT a mean-independent consistency construct: it is mechanically coupled to "
    "recall level (rho(CV, mean recall) = -0.77; |rho| with Presence = 0.77, above "
    "the 0.50 dissociation ceiling). The instrument was NOT adopted, and "
    "redefinition of Consistency on a mean-independent basis was escalated to v1.8. "
    "v0.32 therefore characterizes the VERSION-STABILITY of the v1.7 recall-coupled "
    "score as an empirical input to v1.8. It does NOT validate CPC as a consistency "
    "construct. PRIMARY and SECONDARY are, operationally, recall-level stability "
    "tests and are reported as such. "
    "v0.31 (SSRN 6880959) reported a cross-category baseline on this same v1.7 score "
    "without foregrounding its not-adopted status; v0.32 introduces that framing "
    "explicitly. A framing-consistency reconciliation of v0.31 is a separate program "
    "action, not a dependency of this pre-registration."
)

# ---------------------------------------------------------------------------
# Panel -- six slots x two vintage arms. Full dated IDs + tier labels live in
# registries/v0_32_registry.json; mirrored here for the locked record.
# ---------------------------------------------------------------------------
PANEL_N = 6  # population (whole panel), not a sample -> ddof=0 in dispersion
MODEL_PANEL_ARMS = {
    # slot_key: (tier_label, arm_A_older, arm_B_current)
    "claude_opus":       ("Anthropic flagship",  "claude-opus-4-5-20251101",   "claude-opus-4-8"),
    "claude_sonnet":     ("Anthropic mid",       "claude-sonnet-4-5-20250929", "claude-sonnet-4-6"),
    "gpt_4o":            ("OpenAI flagship",      "gpt-4o-2024-11-20",          "gpt-5.5-2026-04-23"),
    "gpt_4o_mini":       ("OpenAI mini",          "gpt-4o-mini-2024-07-18",     "gpt-5.4-mini-2026-03-17"),
    "gemini_flash":      ("Google flash",         "gemini-2.5-flash",           "gemini-3.5-flash"),
    "gemini_flash_lite": ("Google flash-lite",    "gemini-2.5-flash-lite",      "gemini-3.1-flash-lite"),
}
VINTAGES = {"A": "older (v0.17-era class)", "B": "current"}

# ---------------------------------------------------------------------------
# CPC computation (inherited from v1.7, applied independently per arm)
# ---------------------------------------------------------------------------
DISPERSION = "CV = population_SD / mean (ddof=0)"
TRANSFORM = "CPC = 1 / (1 + CV)"   # bounded (0, 1]; higher = more consistent
CPC_RANGE = "(0, 1]"
FLOOR = {
    "rule": "mean(combined_recall_count) < 1.0  ->  CPC = UNDEFINED (N/A)",
    "note": "Inherited v1.7 floor (mu_floor = 1.0). Unchanged.",
}

# ---------------------------------------------------------------------------
# N/A rule + flip count (the denominator + the survivor-bias guardrail)
# ---------------------------------------------------------------------------
NA_AND_FLIP_RULE = {
    "pairwise_complete": (
        "rho (PRIMARY) and mean |dCPC| (SECONDARY/TERTIARY-secondary) are computed "
        "over brands with DEFINED CPC in BOTH arms."
    ),
    "flip_count": (
        "FIRST-CLASS, MANDATORY co-reported instability indicator -- not a side count. "
        "Brands flipping defined<->N/A across arms are by definition the most "
        "version-sensitive; dropping them from the numeric stats biases those stats "
        "toward 'more stable' than the full registry is. The flip count is the part of "
        "the instability the numeric stats structurally cannot see."
    ),
    "joint_reporting": (
        "Flip count reported JOINTLY with rho in the verdict JSON and the abstract, "
        "with the committed interpretive role that a high flip count materially "
        "qualifies any stability narrative REGARDLESS of rho (the v0.28 enterprise-panel "
        "interpretation-guardrail pattern). PRIMARY verdict stays crisp on rho >= 0.70 "
        "alone -- no compound fuzzy condition."
    ),
    "reported_directionally_and_by_cell": (
        "Flips reported by direction (A-defined->B-N/A vs B-defined->A-N/A; net "
        "direction is a composition-change signal) and by Cell."
    ),
}

# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------
HYPOTHESES = {
    "H_ScoreRankStable": {  # PRIMARY
        "rank": "PRIMARY",
        "statement": (
            "The v1.7 score's per-brand rank-order is preserved across the version "
            "contrast."
        ),
        "test": "Spearman rho(CPC_A, CPC_B) over pairwise-complete brands.",
        "confirm_if": "rho >= 0.70",
        "interpretive_bands": {
            ">=0.70": "rank-stable",
            "0.50-0.70": "partially version-sensitive",
            "<0.50": "version-dominated",
        },
        "verdict_rule": "Confirm/falsify on 0.70 ALONE; bands are interpretive context.",
        "falsified_if": (
            "rho < 0.70 -- the v1.7 score is version-vintage-dependent, not a stable "
            "brand property (a material finding for the 2.0 composite)."
        ),
        "interpretation": (
            "Per FRAMING, this is operationally a recall-level rank-stability test."
        ),
        "figure": "fig_01_rank_stability",
    },
    "H_ScoreMagnitudeStable": {  # SECONDARY
        "rank": "SECONDARY",
        "statement": "Per-brand score magnitude is stable across the version contrast.",
        "test": "mean |dCPC| over pairwise-complete brands.",
        "stable_if": "mean |dCPC| <= 0.5 * SD(CPC_A)",
        "threshold_basis": (
            "Scale-relative. Multiplier (0.5) and reference arm (A) FIXED pre-data; "
            "SD(CPC_A) -- population SD over defined-CPC Arm-A brands -- plugs in at "
            "scoring. Ties tolerance to the instrument's own between-brand discriminating "
            "power; scale-invariant (CPC in (0,1] compresses high, so an absolute cut "
            "would mis-anchor)."
        ),
        "falsified_if": "mean |dCPC| > 0.5 * SD(CPC_A)",
        "reporting": "Reported directionally regardless of confirm/falsify.",
        "figure": "fig_02_magnitude_shift",
    },
    "H_EmergingInstability": {  # TERTIARY -- Cell-B
        "rank": "TERTIARY",
        "subset": "Cell_B_Disruptor (thin-but-present emerging brands)",
        "statement": (
            "The thin-but-present disruptor subset (v0.22 Cell-B: Tesla, Rivian, Lucid, "
            "Polestar, Fisker) exhibits the highest N/A->defined flip rate across the "
            "contrast, as newer models learn emerging brands."
        ),
        "primary_read": (
            "FLIP RATE (Cell-B N/A->defined). Rivian (Arm-A mean_r 0.167 -> N/A) and "
            "Fisker (Arm-A mean_r 0.0 -> N/A) are the live N/A->defined candidates under "
            "Arm B."
        ),
        "secondary_read": (
            "|dCPC| contrast among Cell-B brands defined in BOTH arms -- descriptive only "
            "(pairwise-complete Cell-B n is small)."
        ),
        "type": "directional (descriptive; not significance-tested -- subset underpowered)",
        "falsified_if": (
            "Cell-B is not the highest-flip-rate cell, OR the contrast runs counter to "
            "prediction."
        ),
        "figure": "fig_03_emerging_instability",
    },
}

# Cell-D phantoms: descriptive record, NOT a hypothesis.
PHANTOM_DESCRIPTIVE = (
    "Cell-D defunct brands (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn) sit at "
    "0.0 recall in v0.22 and are stably N/A in both arms (defunct brands are not newly "
    "recalled by newer models). Recorded as version-INVARIANTLY undefined -- a "
    "descriptive observation, not a tested hypothesis. This is why the version-"
    "sensitivity hypothesis is sited at Cell-B (emerging), not Cell-D (phantom): the "
    "phantom |dCPC| and flip-rate legs are empty by construction."
)

# ---------------------------------------------------------------------------
# Pre-registered sensitivity analysis
# ---------------------------------------------------------------------------
SENSITIVITY = {
    "leave_one_provider_out": (
        "Recompute rho (PRIMARY) with each provider's two slots removed in turn, to test "
        "whether the OpenAI two-generation jump (gpt-4o -> gpt-5.x, the widest version "
        "distance in the panel) drives any movement in the rank-stability result."
    ),
}

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
SCORING = {
    "phase_a": "Recognition, 24 brands x 6 slots, per vintage arm.",
    "phase_b": "two-channel Recall, 6 probes x 24 brands x 6 slots, per vintage arm.",
    "runs": "twice -- once per vintage arm (A then B), frozen-identical registry/probes.",
    "cpc": "scored per v1.7, independently per arm.",
    "derived_at_scoring": "dCPC, Spearman rho, flip table, leave-one-provider-out rho.",
    "verdicts_out": "osf/v32/v32_verdicts.json",
}

# ---------------------------------------------------------------------------
# Falsification summary
# ---------------------------------------------------------------------------
FALSIFICATION = {
    "PRIMARY":   "rho < 0.70.",
    "SECONDARY": "mean |dCPC| > 0.5 * SD(CPC_A).",
    "TERTIARY":  "Cell-B not the highest-flip-rate cell, or contrast counter to prediction.",
}

# ---------------------------------------------------------------------------
# Predictions (directional, pre-committed)
# ---------------------------------------------------------------------------
PREDICTIONS = [
    "PRIMARY confirmed (established-brand recall rank tends stable).",
    "Nonzero flips concentrated in Cell-B.",
    "TERTIARY confirmed; Rivian and Fisker the modal N/A->defined flips under Arm B.",
]

# ---------------------------------------------------------------------------
# Methods notes / limitations
# ---------------------------------------------------------------------------
LIMITATIONS = [
    "gpt-4o family frozen at 2024-11-20 -- a landscape finding; Arm B necessarily jumps "
    "to the gpt-5.x line. Internal slot keys (gpt_4o/gpt_4o_mini) retained for pipeline "
    "stability; neutral tier labels (OpenAI flagship/mini) published with exact dated IDs "
    "per arm in the registry and panel table.",
    "Gemini Arm A is a best-available floating alias (no dated 2.5 base snapshot exists); "
    "API-returned version metadata recorded at acquisition. Acquire before the "
    "~2026-10-16 shutdown window.",
    "Version-distance asymmetry across slots is a documented characteristic of 'panel "
    "ages to current'; handled by the leave-one-provider-out sensitivity check.",
    "PRIMARY/SECONDARY are recall-level stability tests by construction (FRAMING), not "
    "consistency-construct validation.",
]

# ---------------------------------------------------------------------------
# Figures (one per finding)
# ---------------------------------------------------------------------------
FIGURES = [
    {"id": "fig_01_rank_stability", "finding": "H_ScoreRankStable",
     "spec": "CPC_A vs CPC_B scatter (pairwise-complete); Spearman rho + band annotated; "
             "flip count co-stated."},
    {"id": "fig_02_magnitude_shift", "finding": "H_ScoreMagnitudeStable",
     "spec": "|dCPC| distribution with the 0.5*SD(CPC_A) tolerance band; direction noted."},
    {"id": "fig_03_emerging_instability", "finding": "H_EmergingInstability",
     "spec": "N/A->defined flip rate by Cell; Cell-B highlighted; Cell-D shown as "
             "stably-undefined."},
]

# ---------------------------------------------------------------------------
# DEVIATIONS -- Entry 0 reserved for r1->r2 amendments (none pre-tag).
# ---------------------------------------------------------------------------
DEVIATIONS = {
    "Entry 0": (
        "RESERVED -- nothing to log at r1. The cross-generation panel (every slot tests "
        "that provider-tier's current frontier, not a same-model snapshot bump), the "
        "gpt-4o-frozen-at-2024-11-20 note, the Gemini-Arm-A floating-alias limitation, "
        "and the Cell-B (not Cell-D) siting of the version-sensitivity hypothesis are all "
        "design-rationale declared at r1 in FRAMING / HYPOTHESES / LIMITATIONS -- not r2 "
        "amendments to a tagged pre-reg."
    ),
}
