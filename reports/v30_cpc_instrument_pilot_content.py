"""
v30_cpc_instrument_pilot_content.py

AIAS 2.0 — The Consistency Component (CPC). Managerial brand-format report content.
Instrument-specification pilot: cross-model consistency of recall across a fixed
six-model panel, on three categories (skincare, cosmetics, automotive, 24 brands each).

Authored from the LOCKED verdicts (osf/v30/v30_cpc_verdicts.json, tag v0.30-results-r2);
results-aware. Replaces the inherited v0.28 carryover WHOLESALE.

Two-register rule: managerial voice, propositions P1–P4, NO H_* labels.
™ convention for THIS report: ™ on first mention of Third System and AIAS in the
COVER only; unmarked everywhere after.

Consumed by reports/build_report_v30.py. Attribute contract (14 names):
  VERSION, SUBSTRATE, SUBTITLE        -> str   (metadata; not rendered by the builder)
  COVER                               -> dict{title, subtitle, version, category, substrate,
                                               date, byline_short, tagline, eyebrow, footer}
  STANDFIRST                          -> str
  LEAD_DECK                           -> str   (prose deck; builder renders the string)
  EXEC_SUMMARY                        -> str   (\\n\\n -> paragraphs)
  WHAT_WE_MEASURED                    -> str   (\\n\\n -> paragraphs)
  PATTERNS                            -> list[{id, title, body}]  (4; index i -> chart i)
  LIMITATIONS                         -> str   (\\n\\n -> paragraphs)
  WHATS_NEXT                          -> str   (\\n\\n -> paragraphs)
  HYPOTHESIS_SCORING                  -> list[{id, label, prediction, verdict, detail}]
  HYPOTHESIS_DETAILS                  -> str   (\\n\\n -> items)
  CLOSING                             -> dict{byline_long, datasets, methodology_log, closing_text}
"""

VERSION = "Instrument-Specification Pilot · v0.30 / CPC.01"

SUBSTRATE = "skincare · cosmetics · automotive — 24 brands each"

SUBTITLE = (
    "An instrument-specification pilot — measuring how steadily large language "
    "models surface a brand across the model panel, in categories where "
    "recognition no longer tells brands apart."
)

COVER = {
    "title": "Recognition Saturates. Consistency Doesn't.",
    "subtitle": (
        "An instrument-specification pilot — measuring how steadily large language "
        "models surface a brand across the model panel, in categories where "
        "recognition no longer tells brands apart."
    ),
    # tagline + eyebrow carry the ™ first-mention for AIAS (cover only)
    "tagline": "AIAS™ 2.0 — The Consistency Component (CPC)",
    "eyebrow": "AIAS™ 2.0 — The Consistency Component (CPC)",
    # footer carries the ™ first-mention for Third System (cover only)
    "footer": ("Third System™ · Instrument-Specification Pilot v0.30 · June 2026 · "
               "Categories: skincare, cosmetics, automotive"),
    "byline_short": "Pablo Ulpiano González Castro",
    "version": "Instrument-Specification Pilot · v0.30",
    "category": "skincare · cosmetics · automotive",
    "substrate": "24 brands × 3 categories",
    "date": "June 2026",
}

STANDFIRST = (
    "In mature categories AI recognizes every serious brand, so recognition stops "
    "telling them apart. Consistency — how steadily a brand surfaces across models — "
    "still does. This pilot establishes that the signal is real, separates it from "
    "mere prominence, and maps what a clean measurement of it requires."
)

# Stat-strip deck (builder shape: list of {metric, label, detail}). The framing
# prose this replaces is covered by EXEC_SUMMARY + WHAT_WE_MEASURED.
LEAD_DECK = [
    {"metric": "79% / 0%", "label": "recall vs recognition coverage (cosmetics)",
     "detail": "consistency is measurable where recognition has saturated"},
    {"metric": "-0.47 -> -0.13", "label": "raw -> corrected bias (skincare)",
     "detail": "the level-correction cut the prominence bias 72%"},
    {"metric": "H = 14.24, p<.001", "label": "consistency across categories",
     "detail": "category-conditioned, not a fixed brand trait"},
    {"metric": "1 of 3", "label": "categories testable for the bias",
     "detail": "apparatus-homogeneity and level-variance pull apart — the pilot's core lesson"},
]

EXEC_SUMMARY = """AI consistency is a measurable, category-conditioned signal that survives the point at which recognition stops discriminating — and this pilot both validated the measure's bias-correction in the one category that could test it and mapped exactly the category mix the next measurement will need.

P1 — Consistency is measurable from recall precisely where recognition is exhausted. In cosmetics, every brand is recognized by every model, so recognition yields a usable consistency score for none of them — yet recall yields one for 79%. Automotive shows the same gap: 62% from recall against 4% from recognition. Where recognition flatlines, consistency keeps discriminating.

P2 — Raw consistency is biased by prominence. Where brand prominence varied across the panel (skincare), less-prominent brands scored as "less consistent" for a purely mechanical reason (rho = -0.47). Where every brand is universally recognized, this bias cannot even be tested — the diagnostic itself requires a spread of prominence to run.

P3 — The correction works where it can be tested. The max-normalized (Bhatia-Davis) correction cut the prominence bias by 72% in skincare (-0.47 -> -0.13, no longer significant). Confirming it across categories is the next measurement's task, by design, not a gap in this one.

P4 — Consistency is category-conditioned, not a fixed brand trait. How steadily brands surface across the panel differs significantly across the three categories (p < 0.001).

The pilot's sharpest lesson is a constraint: the category mix that isolates the category effect most cleanly is the same mix that erases the prominence spread the correction needs to prove itself. The next stage must select categories for both at once."""

WHAT_WE_MEASURED = """Consistency asks a simple question: when you query a panel of large language models about a category, does a given brand surface evenly across them, or does it appear for some models and vanish for others? A brand that surfaces uniformly is consistent; one that flickers in and out is not. The instrument (CPC) measures this as the variation in a brand's recall presence across a fixed six-model panel — lower variation, higher consistency.

Two versions are computed. The raw measure is a plain coefficient of variation. Because that statistic mechanically inflates for brands that surface rarely — penalizing them for being small, not for being erratic — a level-corrected version is also computed, which scales the variation against the most it could possibly be at that frequency. The level a brand is corrected against is its recognition: whether the models recognize it at all.

The pilot ran across three categories — skincare, cosmetics, automotive — 24 brands each, against the same six models, reusing already-published measurement data. No new model queries were made."""

PATTERNS = [
    {
        "id": "coverage",
        "title": "Recall yields a consistency signal where recognition cannot",
        "body": (
            "In all three categories recognition has saturated: nearly every brand is "
            "recognized by every model (cosmetics, 24 of 24; automotive, 23 of 24). "
            "Recognition can no longer separate these brands. Recall-based consistency "
            "still can — it is defined for 79% of skincare brands, 79% of cosmetics, and "
            "62% of automotive (Figure 1). The signal lives exactly where the older one "
            "has gone dark."
        ),
    },
    {
        "id": "confound",
        "title": "Raw consistency tracks prominence — where prominence still varies",
        "body": (
            "The raw consistency score carries a bias. In skincare — the one category "
            "where brands still differ in how recognized they are — less-recognized "
            "brands score as less consistent for a purely mechanical reason "
            "(rho = -0.47): the raw statistic inflates at low frequency. In cosmetics "
            "and automotive that bias cannot even be measured, because recognition is "
            "uniform — which Figure 2 shows as a vertical collapse at full recognition."
        ),
    },
    {
        "id": "correction",
        "title": "The level-correction removes the prominence bias (skincare)",
        "body": (
            "The level-correction flattens the bias where it could be tested: skincare's "
            "-0.47 falls to -0.13, no longer significant — a 72% reduction (Figure 3). "
            "One category cleared the bar cleanly; certifying the correction across the "
            "full range of prominence is the next measurement's job, by design."
        ),
    },
    {
        "id": "variation",
        "title": "Consistency differs by category — and the tension that bounds the pilot",
        "body": (
            "Consistency genuinely differs by category: the corrected distributions "
            "diverge significantly (H = 14.24, p < 0.001; Figure 4). And the tension is "
            "unmissable — the categories that delivered the cleanest category effect are "
            "the same ones whose saturated recognition blocked the bias test. The mix "
            "that sharpened P4 is the mix that bounded P2 and P3."
        ),
    },
]

LIMITATIONS = """Three bounds frame these findings. First, and most important: the bias correction was tested in only one of the three categories. Recognition saturated the other two, and a bias defined against recognition cannot be measured where recognition does not vary — so skincare alone certifies the correction, and one category is a demonstration, not a guarantee.

Second, the trio sits mid-to-high on brand identity and carries no low-recognition category — which is precisely what would have preserved the prominence spread the correction needs. The selection that sharpened the category finding is the one that bounded the bias finding.

Third, this is cross-model consistency at a single point in time, computed on reused measurement data; consistency across deployment surfaces — the consumer apps, with their retrieval and augmentation — and consistency over time are defined but not measured here, and remain open."""

WHATS_NEXT = """The pilot hands the next stage a precise instruction. Validating the consistency instrument requires a category set that satisfies two demands at once: a uniform measurement apparatus, so category differences are real and not artifacts; and a spread of brand prominence, so the bias correction can actually be tested. These demands pull against each other — uniform, mature categories tend to saturate recognition — so the next measurement must be designed to hold both, not stumble into one.

Concretely, the cross-category consistency baseline will pre-register, before any data is seen, a graded prominence measure that keeps its variance even when recognition tops out, and a category set deliberately spanning recognition levels from niche to ubiquitous. The max-normalized correction carries forward as the working normalization — proven where it could be tested — pending that broader confirmation.

The instrument is specified; what remains is to certify it on the ground its own first run mapped out."""

HYPOTHESIS_SCORING = [
    {
        "id": "P1",
        "label": "Consistency is measurable from recall where recognition is exhausted",
        "prediction": "—",
        "verdict": "Established",
        "detail": "Defined for 79% / 79% / 62% of brands vs 0% / 4% from recognition.",
    },
    {
        "id": "P2",
        "label": "Raw consistency is biased by prominence",
        "prediction": "—",
        "verdict": "Demonstrated where testable",
        "detail": "rho = -0.47 in skincare; untestable under saturation.",
    },
    {
        "id": "P3",
        "label": "The level-correction removes the bias",
        "prediction": "—",
        "verdict": "Validated in one category",
        "detail": "72% reduction in skincare; cross-category confirmation pending by design.",
    },
    {
        "id": "P4",
        "label": "Consistency is category-conditioned",
        "prediction": "—",
        "verdict": "Established",
        "detail": "Distributions differ significantly (p < 0.001).",
    },
]

HYPOTHESIS_DETAILS = """P1. Across the trio, recall yields a defined consistency score for a clear majority of brands, while recognition — saturated — yields almost none: cosmetics 79% vs 0%, automotive 62% vs 4%, skincare 79% vs 17%. The recall signal is not a marginal improvement on recognition in these categories; it is the only signal still standing.

P2. Consistency must be separated from sheer prominence, or it merely re-measures it. In skincare, where recognition still varied, the raw score correlated with recognition at rho = -0.47 (p = .04) — confirming the contamination. In cosmetics and automotive, every brand sits at full recognition, so the correlation is mathematically undefined: the very uniformity that proves recognition has saturated also removes the variation the bias test needs.

P3. Applied in skincare, the max-normalized correction reduced the contamination from -0.47 to -0.13 (no longer significant), a 72% attenuation; an alternative residual-based correction moved it in the same direction (-0.27), corroborating that the bias is both real and removable. One category cleared the bar cleanly — but one category cannot, on its own, certify the correction across the board, and the pilot does not claim it does.

P4. With the apparatus held identical across categories, the corrected consistency distributions still differ significantly (Kruskal-Wallis H = 14.24, p < 0.001) — so the differences are attributable to category, not to measurement artifacts. Consistency is a property of the brand-in-its-category, not a fixed trait a brand carries everywhere."""

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano González Castro",
        "School of Visual Arts, MPS Branding Program, New York, NY",
        "Third System (research entity)",
    ],
    "datasets": [
        "CPC scores: osf.io/ec6wh/v30/data/v30_cpc.csv",
        "Verdicts: osf.io/ec6wh/v30/v30_cpc_verdicts.json",
        "Reused measurement data: osf.io/ec6wh (v20 skincare, v21 cosmetics, v22 automotive — Phase A recognition + Phase B recall)",
    ],
    "methodology_log": "v0.30-prereg-r2 / v0.30-results-r2; reuses v0.20 skincare (SSRN 6811441), v0.21 cosmetics (6815378), v0.22 automotive (6829118) Phase A + Phase B under methodology lock v1.6 (6816340); no new model queries",
    "closing_text": (
        "Recognition saturates; consistency does not. As AI becomes the surface on "
        "which brands are discovered, the question stops being whether a model knows a "
        "brand and becomes how steadily it surfaces one. That steadiness, this pilot "
        "shows, is measurable exactly where the older signal has gone flat; it belongs "
        "to the brand-in-its-category rather than traveling with the brand; and its one "
        "mechanical bias can be corrected. What is left is to prove that correction "
        "across the full range of prominence — a test this run has defined precisely. "
        "The consistency component is no longer a proposal. It is an instrument with a "
        "known next move."
    ),
}
