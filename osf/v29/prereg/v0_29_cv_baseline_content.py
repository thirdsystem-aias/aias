"""
v0.29 — Phase 3 Construct-Validity Baseline (Presence)
Pre-registration content module.

DESIGN CLASS: SYNTHESIS. No new measurement, no probes, no acquisition.
Verdicts are inherited from two locked component papers; v0.29 computes
exactly ONE new quantity — the Campbell-Fiske gap (C3) — and otherwise
asserts from inherited verdicts.

This module REPLACES the cloned v0.26 Amazon-BSR predictive-validity prereg
content wholesale. A synthesis breaks the acquisition template by design:
a provenance manifest stands in for the 24-brand registry, and inherited
verdicts stand in for hypotheses-to-test.

Locked at git tag: v0.29-prereg-r1
"""

PHASE = "v0.29"
PROJECT_ID = "CV.05"
DESIGN_CLASS = "synthesis"          # assembly of inherited verdicts; no acquisition
PROTOCOL = "v1.6"
SLUG = "cv_baseline"
FOOTER_LABEL = "Construct-Validity Baseline"   # short label for chart footers

TITLE = ("The Presence Component Is Construct-Valid: "
         "A Convergent-Discriminant (Campbell-Fiske) Baseline")

# ---------------------------------------------------------------------------
# Provenance manifest  (stands in for the acquisition registry)
# ---------------------------------------------------------------------------
PROVENANCE = {
    "convergent": {
        "phase": "v0.25",
        "ssrn": "6842138",
        "prereg_tag": "v0.25-prereg-r1",
        "prereg_commit": "6ff9403",
        "registry": "24-brand B2B SaaS",
        "instrument": "Google Trends via SerpAPI",
        "statistic": "Spearman rho",
        "inherited_verdict": "H_CV_Primary CONFIRMED",
        "rho": 0.74,
        "p": "<0.001",
        "verdicts_json": "osf/v25/v25_verdicts.json",
    },
    "discriminant": {
        "phase": "v0.26",
        "ssrn": "6847678",
        "registry": "Amazon BSR set (incl. v0.16 retrofit; v0.26 locked list only)",
        "instrument": "Amazon Best Sellers Rank (BSR)",
        "statistic": "Spearman rho",
        "inherited_verdict": ("H_PV_Primary FALSIFIED (0/3) — "
                              "the falsification IS the discriminant evidence"),
        "rho": None,   # near-zero / non-significant; read from verdicts at scoring
        "verdicts_json": "osf/v26/v26_verdicts.json",
    },
}

# Substrates explicitly OUT of the baseline claim (extension candidates only):
DISCRIMINANT_EXCLUSIONS = ["v0.17", "v0.19", "v0.20", "v0.21"]

# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------
HYPOTHESES = {
    "C1_convergent": {
        "statement": ("rho(C_P, GoogleTrends) positive and significant -> "
                      "monotrait-heteromethod convergence holds."),
        "status": "INHERITED (v0.25); not re-tested",
        "locked_value": "rho=0.74, p<0.001",
    },
    "C2_discriminant": {
        "statement": ("rho(C_P, AmazonBSR) non-significant / near-zero -> "
                      "heterotrait divergence holds; Presence does not track sales rank."),
        "status": "INHERITED (v0.26); not re-tested",
    },
    "C3_campbell_fiske_gap": {
        "statement": ("abs(rho_convergent) - abs(rho_discriminant) > 0, WITH "
                      "convergent significant AND discriminant non-significant."),
        "status": "COMPUTED — the single new quantity v0.29 produces",
    },
    "H_CV_Baseline": {
        "statement": ("C1 AND C2 AND C3 hold -> the Presence component clears a "
                      "Campbell-Fiske convergent-discriminant validity baseline."),
        "status": "PRIMARY pooled claim",
    },
}

# ---------------------------------------------------------------------------
# Scoring / assembly rules
# ---------------------------------------------------------------------------
SCORING = {
    "C3": "difference of absolute Spearman coefficients from the two inherited verdicts.json",
    "significance_pattern": ("read from inherited p-values; convergent MUST be significant, "
                             "discriminant MUST be non-significant"),
    "output": "osf/v29/v29_verdicts.json — assembled 2x2 MTMM matrix + H_CV_Baseline verdict",
    "verdict_levels": ["CONFIRMED", "PARTIAL", "FALSIFIED"],
    "partial_reserved_for": ("gap>0 but discriminant drifts to marginal significance, OR "
                             "convergent magnitude restates below the v0.25 locked value"),
}

# ---------------------------------------------------------------------------
# Falsification criteria  (any one fails H_CV_Baseline)
# ---------------------------------------------------------------------------
FALSIFICATION = [
    "C3 <= 0  (Campbell-Fiske inversion: discriminant >= convergent)",
    "convergent leg non-significant when restated",
    "discriminant leg significant (Presence tracks BSR after all)",
]

# ---------------------------------------------------------------------------
# Pre-registered predictions
# ---------------------------------------------------------------------------
PREDICTIONS = {
    "C1": "rho ~ 0.74, p<0.001 (significant)",
    "C2": "abs(rho) < ~0.20, non-significant",
    "C3": "gap ~ 0.55, clears > 0 with significance asymmetry intact",
    "H_CV_Baseline": "CONFIRMED (expected)",
}

# ---------------------------------------------------------------------------
# Deviations from original scope
# ---------------------------------------------------------------------------
DEVIATIONS = {
    "entry_0": (
        "CV.05 was originally scoped three-leg (predictive + convergent + discriminant). "
        "Predictive validity requires a t1->t2 longitudinal external-criterion design; no "
        "lagged wave exists in the pipeline, and asserting predictive validity without one "
        "would violate both construct-validity logic and the no-new-acquisition structure of "
        "a synthesis. Scope reduced AT r1 (no acquisition occurred — this is a scope lock, not "
        "a post-hoc change) to a two-leg convergent-discriminant baseline. Predictive validity "
        "is queued as the next gated study, requiring a second measurement wave. Title and "
        "H_CV_Baseline reflect the two-leg scope."
    ),
}
