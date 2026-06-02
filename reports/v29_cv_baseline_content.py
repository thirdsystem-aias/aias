"""
v0.29 (CV.05) — The Presence Component Is Construct-Valid
Convergent–Discriminant (Campbell–Fiske) baseline for AI Availability.

Brand-format report content module (Third System).
P1–P5 propositional register for managerial readers.

DESIGN CLASS: SYNTHESIS. No acquisition. Every number below is transcribed from
the locked verdict (osf/v29/v29_verdicts.json, scored at 191a793) — the managerial
register of the same result the SSRN paper reports, not a separate finding.
  convergent (v0.25): rho = 0.7411, p = 3.4e-05, n = 24
  discriminant (v0.26 pooled): rho = -0.0002, p = 0.998, n = 88
  Campbell–Fiske gap C3 = 0.7409  ->  H_CV_Baseline CONFIRMED
"""

VERSION = "v0.29"
SUBSTRATE = "Construct-Validity Baseline (Presence)"
SUBTITLE = "Convergent–Discriminant (Campbell–Fiske)"

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "The Presence Component\nIs Construct-Valid",
    "subtitle": (
        "A convergent–discriminant baseline: AI Presence tracks what it "
        "should and ignores what it should"
    ),
    "version": "v0.29",
    "category": "Construct Validity — Campbell–Fiske Baseline",
    "substrate": "Synthesis of v0.25 (convergent) + v0.26 (discriminant)",
    "date": "June 2026",
}

# ---------------------------------------------------------------------------
# STANDFIRST
# ---------------------------------------------------------------------------

STANDFIRST = (
    "AI Presence correlates strongly with what consumers search for "
    "(ρ = 0.74) and not at all with where products rank in retail sales "
    "(ρ = 0.00). A measure that behaves that way — close to the "
    "related signal, far from the unrelated one — is measuring a real, "
    "distinct thing. That is the textbook test of a valid construct, and the "
    "Presence component passes it."
)

# ---------------------------------------------------------------------------
# LEAD_DECK
# ---------------------------------------------------------------------------

LEAD_DECK = [
    {
        "metric": "ρ = 0.74",
        "label": "Convergent",
        "detail": "Presence × Google Trends search interest (v0.25; p &lt; 0.001, n = 24)",
    },
    {
        "metric": "ρ = 0.00",
        "label": "Discriminant",
        "detail": "Presence × Amazon Best Sellers Rank (v0.26; p = 0.998, n = 88)",
    },
    {
        "metric": "0.74",
        "label": "Campbell–Fiske gap",
        "detail": "C₃ = |ρ convergent| − |ρ discriminant|, well above zero",
    },
    {
        "metric": "CONFIRMED",
        "label": "Baseline verdict",
        "detail": "All three pre-registered conditions hold; significance asymmetry intact",
    },
]

# ---------------------------------------------------------------------------
# EXEC_SUMMARY
# ---------------------------------------------------------------------------

EXEC_SUMMARY = (
    "A measurement only earns the word “construct” when it is shown to "
    "track the things it should and stay clear of the things it should not. "
    "This baseline assembles two already-locked results into that test — "
    "it runs no new measurement of its own.\n\n"

    "On the related side, AI Presence moves with consumer search interest: "
    "across 24 B2B SaaS brands, Presence and Google Trends correlate at "
    "ρ = 0.74 (v0.25). On the unrelated side, AI Presence is indifferent "
    "to retail sales rank: across 88 brands, Presence and Amazon Best Sellers "
    "Rank correlate at ρ = −0.0002 — statistically "
    "indistinguishable from zero (v0.26). The gap between the two, 0.74, is the "
    "single quantity this synthesis computes.\n\n"

    "That pattern — strong where it should be strong, absent where it "
    "should be absent — is the Campbell–Fiske signature of a valid, "
    "distinct construct. The baseline verdict is CONFIRMED. The program "
    "proposes AI Availability as a third system alongside Mental and Physical "
    "Availability; for that proposal to stand, its Presence measure must first "
    "be shown valid — which is what this study establishes. The bounded "
    "finding is about the measure: Presence tracks brand salience and is "
    "distinct from retail sales rank, so it cannot be read off a search "
    "dashboard or a sales report. It has to be measured on its own terms."
)

# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = (
    "This is a synthesis. It performs no new acquisition; it reads two locked "
    "studies and computes one comparison.\n\n"

    "<b>The convergent leg (v0.25).</b> AI Presence was correlated with Google "
    "Trends search interest across a 24-brand B2B SaaS panel. Search interest "
    "is a <i>related</i> signal — both reflect how present a brand is in "
    "the wider discourse — so a valid Presence measure should track it. "
    "It did: Spearman ρ = 0.74 (p &lt; 0.001).\n\n"

    "<b>The discriminant leg (v0.26).</b> AI Presence was tested against Amazon "
    "Best Sellers Rank across a pooled 88-brand set. Sales rank is an "
    "<i>unrelated</i> signal — it reflects price, distribution, and "
    "logistics, not AI salience — so a valid Presence measure should "
    "<i>not</i> track it. It did not: ρ = −0.00 (p = 0.998).\n\n"

    "<b>The test.</b> Campbell &amp; Fiske (1959) require both: correlation "
    "with the related trait, near-zero correlation with the unrelated one. The "
    "gap between the two coefficients — here 0.74 — is the evidence. "
    "A positive gap with the right significance pattern confirms the construct."
)

# ---------------------------------------------------------------------------
# PATTERNS  (chart_slot wired in build_report_v29.py: p1 -> mtmm_gap, p2 -> convergent_scatter)
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "id": "p1",
        "title": "Strong where it should be, absent where it should be",
        "body": (
            "The whole case sits in one comparison. Against a related signal "
            "(search interest), AI Presence correlates at ρ = 0.74. "
            "Against an unrelated one (retail sales rank), it correlates at "
            "ρ = 0.00. The first is a strong, significant relationship; "
            "the second is statistically indistinguishable from zero.\n\n"

            "A measure that correlated with both would be ambiguous — you "
            "could not say what it captured. A measure that correlated with "
            "neither would be noise. AI Presence does exactly what a valid, "
            "specific construct does: it lines up with the thing it is "
            "supposed to reflect and ignores the thing it is not."
        ),
    },
    {
        "id": "p2",
        "title": "The convergent leg: Presence tracks search demand",
        "body": (
            "Across 24 B2B SaaS brands, the brands the models surface most "
            "are, by and large, the brands people search for most "
            "(ρ = 0.74, p &lt; 0.001). This is the reassuring half of "
            "construct validity: AI Presence is anchored to a real-world "
            "salience signal, not floating free of it.\n\n"

            "It matters that the related signal is search rather than sales. "
            "Search interest, like AI Presence, is a measure of mind-presence "
            "— how much a brand occupies the conversation — which is "
            "the dimension Presence is meant to capture. The strong tie to "
            "search is what makes the near-zero tie to sales meaningful rather "
            "than merely a weak measure."
        ),
    },
    {
        "id": "p3",
        "title": "The discriminant leg: Presence is not a sales proxy",
        "body": (
            "Against Amazon Best Sellers Rank — pooled across 88 brands "
            "— AI Presence correlates at ρ = −0.0002, p = 0.998. "
            "There is no relationship to detect. A brand can be highly present "
            "to the models and sell modestly, or sell heavily and be thin in "
            "the models; the two are independent.\n\n"

            "This is not a weakness in the measure — it is the point. If "
            "AI Presence simply re-indexed sales, it would add nothing to the "
            "metrics brands already have. Its indifference to retail rank is "
            "what establishes it as a separate lever, worth measuring in its "
            "own right. The original v0.26 study framed this null as a failed "
            "prediction; in the construct-validity frame it is the evidence."
        ),
    },
    {
        "id": "p4",
        "title": "Verdict: a construct-valid baseline for AI Availability",
        "body": (
            "Three pre-registered conditions had to hold together: the "
            "convergent leg positive and significant; the discriminant leg "
            "below a |ρ| = 0.20 ceiling and non-significant; and the gap "
            "between them strictly positive. All three hold, with the "
            "significance asymmetry intact — convergent significant, "
            "discriminant not. The baseline is CONFIRMED.\n\n"

            "What this establishes is bounded and about the measure: the "
            "Presence component is construct-valid — measurable, anchored to a "
            "related salience signal, and distinct from commercial outcomes. "
            "That validity is the precondition the program's larger proposal "
            "depends on — that AI Availability is a third system alongside "
            "Mental and Physical Availability — but the proposal is the frame, "
            "not a result of this study. For brand leaders, the usable "
            "implication is narrower and firm: because Presence is valid and "
            "distinct, it cannot be inferred from search dashboards or sales "
            "reports; it has to be measured on its own surface."
        ),
    },
]

# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------

LIMITATIONS = (
    "This is a baseline, not the last word. The convergent and discriminant "
    "legs come from different substrates (B2B SaaS for search; consumer goods "
    "for sales rank), so the synthesis assembles two contexts rather than one "
    "matched panel. A single panel measured against both signals at once would "
    "be a stronger MTMM cell.\n\n"

    "The discriminant leg is a near-zero correlation, which is the desired "
    "result but also the easiest to obtain by accident; its weight comes from "
    "being paired with a strong, significant convergent leg, not from "
    "standing alone.\n\n"

    "The predictive leg — whether AI Presence forecasts a future "
    "behavioral outcome — is not part of this baseline and is deferred to "
    "a later gated wave."
)

# ---------------------------------------------------------------------------
# WHATS_NEXT
# ---------------------------------------------------------------------------

WHATS_NEXT = (
    "The baseline establishes that Presence is construct-valid; the next "
    "questions are about reach. A matched-panel MTMM — one brand set "
    "measured against both a related and an unrelated signal simultaneously "
    "— would tighten the convergent–discriminant pair into a single "
    "design.\n\n"

    "Beyond that, the predictive wave: testing whether AI Presence "
    "anticipates a downstream behavioral outcome would extend the construct "
    "from “distinct and well-anchored” to “decision-relevant.” "
    "That is the gate from a measurement claim to a management claim."
)

# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING
# ---------------------------------------------------------------------------

HYPOTHESIS_SCORING = [
    {
        "id": "C1",
        "label": "Convergent leg positive and significant",
        "prediction": "Presence × search interest correlates, p &lt; 0.05",
        "verdict": "CONFIRMED",
        "detail": "ρ = 0.7411, p = 3.4e-05, n = 24 (inherited v0.25, H_CV_Primary).",
    },
    {
        "id": "C2",
        "label": "Discriminant leg below ceiling and non-significant",
        "prediction": "Presence × sales rank: |ρ| &lt; 0.20, n.s.",
        "verdict": "CONFIRMED",
        "detail": "ρ = −0.0002, p = 0.998, n = 88 (inherited v0.26, H_PV_Pooled).",
    },
    {
        "id": "C3",
        "label": "Campbell–Fiske gap strictly positive",
        "prediction": "|ρ convergent| − |ρ discriminant| &gt; 0",
        "verdict": "CONFIRMED",
        "detail": "C3 = |0.7411| − |−0.0002| = 0.7409 &gt; 0; significance asymmetry intact.",
    },
    {
        "id": "H_CV_Baseline",
        "label": "Conjunctive construct-validity baseline",
        "prediction": "C1 ∧ C2 ∧ C3 all hold",
        "verdict": "CONFIRMED",
        "detail": "All three conditions hold jointly — the Presence component clears the baseline.",
    },
]

# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS
# ---------------------------------------------------------------------------

HYPOTHESIS_DETAILS = (
    "<b>C1 — Convergent leg: CONFIRMED.</b>\n"
    "Inherited from v0.25 (SSRN 6842138, pre-reg v0.25-prereg-r1). AIAS Presence "
    "× Google Trends, 24-brand B2B SaaS panel: Spearman ρ = 0.7411, "
    "p = 3.4e-05, 95% CI [0.398, 0.912]. Positive and significant.\n\n"

    "<b>C2 — Discriminant leg: CONFIRMED.</b>\n"
    "Inherited from v0.26 (SSRN 6847678, pre-reg v0.26-prereg-r2). AIAS Presence "
    "× Amazon Best Sellers Rank, pooled n = 88: ρ = −0.0002, "
    "p = 0.998 — below the |ρ| = 0.20 ceiling and non-significant.\n\n"

    "<b>C3 — Campbell–Fiske gap: CONFIRMED.</b>\n"
    "C3 = |0.7411| − |−0.0002| = 0.7409 &gt; 0. The pre-registered "
    "point forecast was ~0.55; the realized gap exceeds it because the "
    "discriminant coefficient came in near zero rather than near the band "
    "ceiling. Forecast-versus-realization only; the lock is untouched.\n\n"

    "<b>H_CV_Baseline — Conjunctive verdict: CONFIRMED.</b>\n"
    "C1 ∧ C2 ∧ C3 hold jointly with the significance asymmetry intact. "
    "The Presence component clears a convergent–discriminant construct-"
    "validity baseline."
)

# ---------------------------------------------------------------------------
# CLOSING
# ---------------------------------------------------------------------------

CLOSING = (
    "AI Presence tracks what consumers search for and ignores where products "
    "rank in sales. That double result — convergence with the related "
    "signal, divergence from the unrelated one — is what makes it a valid, "
    "distinct construct rather than a repackaging of metrics brands already "
    "hold.\n\n"

    "The program proposes AI Availability as a third system alongside Mental "
    "and Physical Availability. That proposal rests on the Presence measure "
    "being valid in the first place — and that is what this study supplies, "
    "not the third-system claim itself. What is established here is the "
    "narrower, firmer point: the Presence component is construct-valid, so it "
    "cannot be read off a search dashboard or a sales report. It is measured "
    "on its own surface, and that is where it must be managed."
)
