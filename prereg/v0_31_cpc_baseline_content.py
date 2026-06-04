"""
AIAS(TM) v0.31 -- CPC Cross-Category Baseline
Pre-registration content module (r1).

Pure-data module. Locked at git tag v0.31-prereg-r1 BEFORE any scoring.
Phase type: RETROACTIVE RESCORE -- no new LLM acquisition.
Methodology lock: v1.7 CPC instrument, generalized per PER_MODEL_UNIT below
(channel-agnostic; identity to v1.7 on two-channel substrates).
"""

PHASE_ID = "v0.31"
PHASE_TITLE = "CPC Cross-Category Baseline"
METHODOLOGY_LOCK = "v1.7"            # SSRN 6878818
INSTRUMENT_SOURCE = "v0.30"          # SSRN 6875319 (CPC instrument specification pilot)
PHASE_TYPE = "retroactive_rescore"   # rescore of committed Phase B recall; no new calls
PREREG_TAG = "v0.31-prereg-r1"

# --- Reference panel (canonical six, held fixed from v0.17) -------------------
MODEL_PANEL = [
    "claude-opus-4-5",
    "claude-sonnet-4-5",
    "gpt-4o",
    "gpt-4o-mini",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]
PANEL_N = 6  # population (whole panel), not a sample -> ddof=0 in dispersion

# --- Signal & per-model unit -------------------------------------------------
SIGNAL = "phase_b_recall"  # recall ONLY; Recognition (Phase A) is NOT used

PER_MODEL_UNIT = {
    "name": "combined_recall_count (channel-agnostic generalization)",
    "definition": (
        "Total per-model brand mentions summed across all Phase B frames, "
        "irrespective of channel labelling. Range 0..6 on the omnibus set "
        "(6 frames per model)."
    ),
    "identity_to_v1_7": (
        "On a two-channel substrate, total-across-frames == R_cat + R_cult "
        "== v1.7 combined_recall_count, by construction: the channels partition "
        "the six frames; no frame is dropped or double-counted. The generalization "
        "CONTAINS the locked v1.7 unit as a special case -- no instrument is swapped."
    ),
    "counting_convention": (
        "Per (brand, model): sum of frames with mention==1 over all 6 frames. "
        "Frames absent from a brand-resolved table are treated as mention==0. "
        "(Applies to v0.19, whose rows are brand|panel_model|frame|mentioned.)"
    ),
}

# --- Reconciliation gate (scoring step 0; precondition for the phase) --------
RECONCILIATION_GATE = {
    "test": (
        "Compute generalized CPC on v0.20 / v0.21 / v0.22 and assert EXACT equality "
        "(zero difference) to v1.7-published CPC."
    ),
    "tolerance": 0.0,  # definitional identity -> exact, not approximate
    "rationale": (
        "Equality is definitional, not approximate. The gate functions as a "
        "regression test on the channel-agnostic scorer implementation; a coding "
        "defect is the only way it can fail."
    ),
    "reference": "osf/methodology/v1_7/v1_7_cpc_verdicts.json",
    "on_failure": "HALT -- generalization invalid / scorer defective. Do not score.",
}

# --- Dispersion / transform / floor (inherited from v1.7) --------------------
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

# --- Registry ----------------------------------------------------------------
BRANDS_PER_SUBSTRATE = 24

# Confirmatory set: canonical-6 panel x 6 frames -> uniform 0..6 unit, per-model recall
OMNIBUS_SUBSTRATES = {
    "v0.19": {"category": "audiophile headphones", "channels": "single", "frames": 6,
              "rows": "brand|panel_model|frame|mentioned"},
    "v0.20": {"category": "skincare",   "channels": "two (3+3)", "frames": 6,
              "rows": "raw_text -> certified matcher"},
    "v0.21": {"category": "cosmetics",  "channels": "two (3+3)", "frames": 6,
              "rows": "raw_text -> certified matcher"},
    "v0.22": {"category": "automotive", "channels": "two (3+3)", "frames": 6,
              "rows": "raw_text -> certified matcher"},
    "v0.23": {"category": "premium spirits",
              "channels": "two (editorial-authority / cultural-cult)", "frames": 6,
              "rows": "brand_mentions coded per (model, probe); 6 probes"},
}

# Descriptive ONLY -- 3-frame -> 0..3 unit; EXCLUDED from the omnibus KW test
SUPPLEMENTARY_SUBSTRATES = {
    "v0.17": {"category": "kitchenware", "channels": "single", "frames": 3,
              "note": "confirm panel composition at scoring before descriptive inclusion"},
    "v0.18": {"category": "indie fragrance", "channels": "single", "frames": 3},
}

# Excluded -- non-comparable model axis
EXCLUDED_SUBSTRATES = {
    "v0.16": {"category": "kitchen knives",
              "reason": "14-model legacy panel (v1.2 sec.3); Phase B is Trends-validation "
                        "format with no clean per-model LLM recall.",
              "deviation": None},
    "v0.24": {"category": "B2B SaaS",
              "reason": "off the locked six (ran opus-4-7 / sonnet-4-6).",
              "deviation": None},
}

# --- Hypotheses --------------------------------------------------------------
HYPOTHESES = {
    "H_CPC_Computable": {
        "statement": (
            "Within each omnibus substrate, brand-level CPC over defined brands "
            "exhibits non-degenerate variance; the instrument is not a near-constant."
        ),
        "test": "Within-substrate spread of brand-level CPC (defined brands only).",
        "scale": "CPC native (0,1]; degenerate := near-constant CPC across defined brands.",
        "falsification": "Fails if CPC is degenerate in >= 4 of the 5 omnibus substrates.",
    },
    "H_CPC_CrossCategory": {
        "statement": "CPC differs systematically across the 5 omnibus substrates.",
        "test": "Kruskal-Wallis across substrate brand-level CPC (defined brands).",
        "alpha": 0.05,
        "reporting_rule": (
            "A significant or large effect is reported as-scored. No post-hoc "
            "reframing toward null; no re-narration of direction after seeing it."
        ),
        "falsification": "Fails to reject if Kruskal-Wallis p >= 0.05.",
    },
}

# --- Predictions (directional, pre-committed) --------------------------------
PREDICTIONS = [
    "Defined CPC concentrated in high-recall incumbents; thin / low-recall brands "
    "resolve to UNDEFINED under the floor.",
    "Editorial/cultural-dense substrates (premium spirits) predicted LESS consistent "
    "than utilitarian substrates (skincare, automotive).",
    "Defunct / near-zero-recall brands resolve to UNDEFINED, not low, CPC.",
]

# --- Deviations --------------------------------------------------------------
DEVIATIONS = {
    "Entry 0": (
        "RELEASED -- nothing to log. v0.16 and v0.24 exclusions are clean pre-scoring "
        "non-comparability calls (legacy 14-model panel; off-panel), not methodology "
        "amendments. The channel-agnostic unit is a pre-registered compatible "
        "generalization declared at r1 and gated by exact reconciliation against v1.7 "
        "-- not an r2 amendment."
    ),
}
