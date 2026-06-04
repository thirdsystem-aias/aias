"""
v1.7 — CPC Consistency Methodology Lock · Pre-registration content (r1)

AIAS™ Measurement Program. This module encodes the locked CPC protocol:
construct, computation, hypotheses, thresholds, verdict keys, and figure map.
Methodology locked at git tag v1.7-prereg-r1, amended at v1.7-prereg-r2
(anchored-set narrowing; see DEVIATIONS Entry 0). No new acquisition in v1.7.

Lineage: extends v1.6 (SSRN 6816340); pilots from v0.30 (SSRN 6875319).
"""

# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------
METADATA = {
    "version": "v1.7",
    "type": "methodology_lock",
    "component": "CPC",                 # Consistency
    "extends": "v1.6",                  # SSRN 6816340
    "pilots_from": "v0.30",             # SSRN 6875319
    "prereg_tag": "v1.7-prereg-r2",   # r1 7d94ac3; r2 narrows anchored set (Entry 0)
    "acquisition": False,               # reads existing Phase B recall data
    "register": "academic",             # paper + figures only; report deferred to AIAS 2.0
}

# ---------------------------------------------------------------------------
# Construct
# ---------------------------------------------------------------------------
CONSTRUCT = {
    "name": "Cross-model Presence Consistency (CPC)",
    "definition": (
        "Stability of a brand's AI presence reading across the fixed six-model "
        "reference panel."
    ),
    "signal_source": "phase_b_recall",  # LOCKED: Recall, never Recognition
    "rationale": (
        "Recall counts are ratio-scale and mean-independent in their dispersion, "
        "unlike binary Recognition whose variance is mechanically pinned to the "
        "mean. Reading CPC from Recall is the dissociation guarantee — it prevents "
        "CPC from collapsing into a deterministic function of Presence."
    ),
}

# ---------------------------------------------------------------------------
# Computation (per brand b, across the six-model panel)
# ---------------------------------------------------------------------------
#   r_{b,k} = R_cat hits + R_cult hits for model k across its 6 probes  (0..12)
#   CPC_raw,b = sd(r_{b,·}) / mean(r_{b,·})                              (CV)
#   CPC_b     = 1 / (1 + CPC_raw,b)                                      (0,1]
#   floor     : if mean(r_{b,·}) < FLOOR -> CPC = N/A
# ---------------------------------------------------------------------------
COMPUTATION = {
    "per_model_unit": "combined_recall_count",   # R_cat + R_cult, range 0..12
    "panel_n": 6,                                # fixed six-model panel
    "dispersion": "coefficient_of_variation",    # sd / mean
    "dispersion_ddof": 0,                        # population sd; 6 models = whole panel (v0.30 convention)
    "transform": "reciprocal_one_plus_cv",       # 1 / (1 + CV); bounded (0,1]
    "score_direction": "higher_is_more_consistent",
    "rejected_transforms": {
        "raw_cv": "unbounded; undefined at mean=0",
        "one_minus_cv": "requires clipping when CV>1 (common here)",
    },
}

THRESHOLDS = {
    "mu_floor": 1.0,            # mean recall below this -> CPC = N/A
    "dissociation_ceiling": 0.50,  # |rho(CPC, Presence)| must fall below this
}

# ---------------------------------------------------------------------------
# Hypotheses (protocol-validation triad)
# ---------------------------------------------------------------------------
HYPOTHESES = [
    {
        "id": "H_CPC_Defined",
        "statement": (
            "CPC computes (mean >= floor) and lands in (0,1] for in-market brands across "
            "the substrates carrying canonical two-channel (R_cat + R_cult) recall on the "
            "fixed six-model panel: v0.20, v0.21, v0.22 — the set validated in the v0.30 "
            "CPC pilot."
        ),
        "falsified_if": (
            "A material fraction of in-market brands return N/A -> floor is mis-set."
        ),
        "figure": "fig_01_cpc_defined",
    },
    {
        "id": "H_CPC_Dissociates",
        "statement": (
            "CPC is not a deterministic function of Presence."
        ),
        "operationalization": (
            "|rho(CPC, Presence)| < 0.50 across pooled anchored brands AND at least "
            "one substrate populates an off-diagonal quadrant (high-Presence/low-CPC "
            "or low-Presence/high-CPC)."
        ),
        "falsified_if": (
            "|rho| >= 0.50 -> CPC is redundant with Presence; lock fails; escalate "
            "to redefinition rather than publish a non-independent component."
        ),
        "figure": "fig_02_cpc_dissociation",
    },
    {
        "id": "H_CPC_PhantomNull",
        "statement": (
            "Cell D phantom brands return CPC = N/A under the floor rule "
            "(consistency is undefined for absent brands)."
        ),
        "falsified_if": (
            "Any phantom returns a defined CPC -> floor rule is mis-specified."
        ),
        "figure": "fig_03_phantom_null",
    },
]

# ---------------------------------------------------------------------------
# Pipeline integration
# ---------------------------------------------------------------------------
VERDICT_KEYS = ["cpc_score", "cpc_status", "cpc_panel_n"]  # per brand in verdicts.json

INTEGRATION = {
    "computed_in": "scoring_step",
    "inputs": "existing per-(brand, model, probe, channel) Phase B recall outputs",
    "reacquisition_required": False,
    "regime": "inherits_four_regime_taxonomy",   # v1.2
    "native_typology_deferred_to": ["v0.36", "v1.8"],
}

# ---------------------------------------------------------------------------
# Illustration boundary
# ---------------------------------------------------------------------------
ILLUSTRATION = {
    "scope": "protocol_validation_only",
    "note": (
        "v1.7 uses existing recall data solely as evidence the protocol is "
        "well-defined and dissociates. The formal per-brand cross-category CPC "
        "baseline is v0.31. Same data, distinct register."
    ),
}

# ---------------------------------------------------------------------------
# Figures (one per finding)
# ---------------------------------------------------------------------------
FIGURES = [
    {"id": "fig_01_cpc_defined",      "finding": "H_CPC_Defined",
     "spec": "CPC distribution / defined-rate across the eight anchored substrates."},
    {"id": "fig_02_cpc_dissociation", "finding": "H_CPC_Dissociates",
     "spec": "CPC x Presence scatter; dissociation quadrants; rho annotated."},
    {"id": "fig_03_phantom_null",     "finding": "H_CPC_PhantomNull",
     "spec": "Phantom N/A confirmation bar (Cell D)."},
]

# ---------------------------------------------------------------------------
# DEVIATIONS — contemporaneous log (Entry 0 reserved for r1->r2 amendments)
# ---------------------------------------------------------------------------
DEVIATIONS = [
    {
        "entry": 0,
        "amendment": "r1 -> r2",
        "type": "pre-computation data-availability scope correction",
        "summary": (
            "r1 asserted H_CPC_Defined across all eight anchored substrates "
            "(v0.16-v0.24). A pre-computation granularity audit (no CPC values "
            "computed) found the locked input — two-channel R_cat+R_cult recall on "
            "the canonical six-model panel — present only for v0.20-v0.22. "
            "Exclusions on data-availability grounds: v0.16 (no LLM-panel recall); "
            "v0.17-v0.19 (single-channel; r=R_cat+R_cult cannot be formed); v0.23 "
            "(two-channel but non-canonical pair editorial-authority/cultural-cult; "
            "channel-construct equivalence deferred to v0.31); v0.24 (off-panel "
            "models, per v0.30). Anchored set narrowed to v0.20-v0.22. No "
            "re-acquisition path in v1.7; cross-substrate recall back-fill logged "
            "as future work. Exclusions are mechanical (input not formable), "
            "decided before any computation — not result-driven."
        ),
    },
]
