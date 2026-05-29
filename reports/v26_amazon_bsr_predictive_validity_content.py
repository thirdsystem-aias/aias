"""
v0.26 — What AI Presence Does Not Predict
Amazon Best Sellers Rank as Discriminant Validity Evidence

Brand-format report content module (Third System)
P1–P5 propositional register for managerial readers.
"""

VERSION = "v0.26"
SUBSTRATE = "Cross-Substrate Construct Validity"
SUBTITLE = "Amazon Best Sellers Rank"

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "What AI Presence\nDoes Not Predict",
    "subtitle": (
        "Amazon Best Sellers Rank as discriminant validity "
        "evidence for the AIAS construct"
    ),
    "version": "v0.26",
    "category": "Construct Validity \u2014 Discriminant",
    "substrate": "Kitchen Knives \u00b7 Audiophile Headphones \u00b7 Skincare \u00b7 Cosmetics",
    "date": "May 2026",
}

# ---------------------------------------------------------------------------
# STANDFIRST
# ---------------------------------------------------------------------------

STANDFIRST = (
    "AI Presence scores show zero correlation with Amazon Best Sellers Rank "
    "across three consumer-goods categories. Brands that language models "
    "recognize are not the same brands that dominate retail sales. "
    "This is not a failure of the measure \u2014 it is evidence that "
    "AI Availability captures something genuinely new."
)

# ---------------------------------------------------------------------------
# LEAD_DECK
# ---------------------------------------------------------------------------

LEAD_DECK = [
    {
        "metric": "rho \u2248 0.000",
        "label": "Pooled correlation",
        "detail": "C<sub>P</sub> \u00d7 BSR across 88 listed brands (p = 0.998)",
    },
    {
        "metric": "0 / 3",
        "label": "Substrates with signal",
        "detail": "No substrate reached the pre-registered threshold (rho \u2264 \u22120.40)",
    },
    {
        "metric": "104 / 106",
        "label": "Amazon coverage",
        "detail": "98% of panel brands have Amazon listings with BSR data",
    },
    {
        "metric": "3 orders",
        "label": "BSR range",
        "detail": "Best Sellers Rank spans 18 to 422,730 across substrates",
    },
]

# ---------------------------------------------------------------------------
# EXEC_SUMMARY
# ---------------------------------------------------------------------------

EXEC_SUMMARY = (
    "This study tested whether brands that score high on AI Presence "
    "also sell well on Amazon. They do not. Across kitchen knives, "
    "audiophile headphones, and skincare, the correlation between "
    "AI Presence Index (C<sub>P</sub>) and Amazon Best Sellers Rank "
    "was indistinguishable from zero \u2014 not merely non-significant, "
    "but effectively absent.\n\n"

    "The null result is the finding. Combined with the strong positive "
    "correlation between C<sub>P</sub> and Google Trends search interest "
    "found in v0.25 (rho\u00a0=\u00a00.74), this study completes "
    "a convergent\u2013discriminant validity pair: AI Presence tracks "
    "brand salience in AI knowledge systems (converges with search interest) "
    "but does not track commercial outcomes (diverges from retail sales rank).\n\n"

    "For brand strategists, the implication is clear: AI Availability is not "
    "a proxy for market share. A brand can be universally recognized by "
    "language models and still rank poorly on Amazon, or dominate Amazon "
    "sales while being invisible to AI systems. These are independent "
    "dimensions of brand access \u2014 exactly what the Tri-System "
    "framework predicts."
)

# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = (
    "We correlated two signals across 106 brands in five consumer-goods "
    "categories.\n\n"

    "<b>AI Presence Index (C<sub>P</sub>):</b> How many of six major language "
    "models recognize each brand in its category (integer 0\u20136). "
    "Three substrates provided within-category variance: kitchen knives "
    "(26 brands, v0.16 retrofitted), audiophile headphones (16 brands, v0.19), "
    "and skincare (24 brands, v0.20). A fourth substrate \u2014 cosmetics "
    "(v0.21) \u2014 showed a ceiling effect where all 24 brands scored "
    "C<sub>P</sub>\u00a0=\u00a06, providing a natural control. "
    "A fifth substrate (premium kitchenware, v0.17) was excluded because "
    "its Phase A data was incomplete.\n\n"

    "<b>Amazon Best Sellers Rank (BSR):</b> The sales-velocity rank of each "
    "brand\u2019s best-selling product on Amazon, acquired via automated "
    "browser extraction in a single 48-hour window. Lower rank = more sales. "
    "Coverage: 104 of 106 brands listed (98.1%).\n\n"

    "<b>Test:</b> Spearman rank correlation per substrate (does higher "
    "C<sub>P</sub> predict lower/better BSR?), plus pooled cross-substrate "
    "correlation and a Cell\u00a0A separation test."
)

# ---------------------------------------------------------------------------
# PATTERNS
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "id": "p1",
        "title": "Zero correlation, uniformly",
        "body": (
            "Within-substrate Spearman correlations: kitchen knives "
            "rho\u00a0=\u00a0+0.048 (p\u00a0=\u00a00.819), "
            "audiophile headphones rho\u00a0=\u00a0\u22120.116 "
            "(p\u00a0=\u00a00.668), skincare rho\u00a0=\u00a0+0.049 "
            "(p\u00a0=\u00a00.823). Pooled across 88 brands: "
            "rho\u00a0=\u00a0\u22120.0002 (p\u00a0=\u00a00.998). "
            "The correlations are not merely non-significant \u2014 "
            "they are effectively zero."
        ),
    },
    {
        "id": "p2",
        "title": "The ceiling proves the point",
        "body": (
            "In cosmetics, all 24 brands achieved C<sub>P</sub>\u00a0=\u00a06 "
            "(full AI recognition), yet BSR ranged from 12 (Maybelline) "
            "to 29,364 (Anastasia Beverly Hills). Full AI recognition "
            "is compatible with any level of retail performance. "
            "The two constructs are independent."
        ),
    },
    {
        "id": "p3",
        "title": "Convergent + discriminant = construct validity",
        "body": (
            "v0.25 showed C<sub>P</sub> correlates strongly with Google "
            "Trends search interest (rho\u00a0=\u00a00.74). This study "
            "shows C<sub>P</sub> does not correlate with Amazon retail "
            "performance (rho\u00a0\u2248\u00a00). Together, these "
            "satisfy the Campbell\u2013Fiske requirements: AI Presence "
            "converges with related salience measures and diverges from "
            "unrelated commercial outcomes."
        ),
    },
    {
        "id": "p4",
        "title": "Different data-generating processes",
        "body": (
            "LLM training corpora overrepresent editorial and enthusiast "
            "discourse; Amazon BSR reflects pricing, distribution logistics, "
            "Prime eligibility, and advertising spend. A brand can dominate "
            "knife forums (high C<sub>P</sub>) without dominating Amazon "
            "sales, and vice versa. The signals originate in fundamentally "
            "different systems."
        ),
    },
]

# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------

LIMITATIONS = (
    "BSR captures sales velocity within one retail channel (Amazon), "
    "not total market performance. Brands with strong offline or "
    "DTC distribution may appear weaker in BSR than their true "
    "market position warrants. A multi-channel sales metric would "
    "provide a stronger discriminant validity test.\n\n"

    "The v0.16 kitchen knives C<sub>P</sub> was retrofitted under "
    "the v1.4+ protocol because the original v1.2 methodology did not "
    "produce comparable scores. The retrofit aligns the metric but "
    "introduces a provenance asymmetry documented in DEVIATIONS Entry 0.\n\n"

    "Three testable substrates is the minimum for cross-substrate "
    "generalization. The v0.17 exclusion and v0.21 ceiling effect "
    "were not anticipated at pre-registration."
)

# ---------------------------------------------------------------------------
# WHATS_NEXT
# ---------------------------------------------------------------------------

WHATS_NEXT = (
    "Extend discriminant validity testing to additional commercial "
    "outcome measures: Sephora rankings, B&H Photo bestsellers, "
    "and specialty retailer data. Prioritize behavioral correlates "
    "(click-through rates, recommendation acceptance) as convergent "
    "measures that sit closer to the theorized mechanism of AI Availability. "
    "Expand the Campbell\u2013Fiske matrix with additional convergent "
    "measures (Wikipedia pageviews, news-corpus brand mentions) and "
    "discriminant measures (brand equity surveys, stock price)."
)

# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING
# ---------------------------------------------------------------------------

HYPOTHESIS_SCORING = [
    {
        "id": "P1",
        "label": "Per-substrate predictive validity",
        "prediction": (
            "C<sub>P</sub> and Amazon BSR correlate negatively "
            "(higher Presence \u2192 better rank) in at least 2 of 3 "
            "testable substrates."
        ),
        "verdict": "FALSIFIED",
        "detail": "0 of 3 substrates met the rho \u2264 \u22120.40 threshold.",
    },
    {
        "id": "P2",
        "label": "Cross-substrate pooled correlation",
        "prediction": (
            "Pooled Spearman rho across all listed brands reaches "
            "rho \u2264 \u22120.30 (p < 0.01)."
        ),
        "verdict": "FALSIFIED",
        "detail": "Pooled rho = \u22120.0002, p = 0.998. Indistinguishable from zero.",
    },
    {
        "id": "P3",
        "label": "Cell A separation",
        "prediction": (
            "Brands with C<sub>P</sub> \u2265 4 have significantly better "
            "(lower) BSR than brands with C<sub>P</sub> < 4."
        ),
        "verdict": "FALSIFIED",
        "detail": (
            "Median BSR percentile: Cell A = 51.09, Other = 54.00. "
            "Negligible and non-significant."
        ),
    },
    {
        "id": "P4",
        "label": "Absence\u2013Presence alignment",
        "prediction": (
            "Brands absent from Amazon have lower mean C<sub>P</sub> "
            "than listed brands."
        ),
        "verdict": "UNDETERMINED",
        "detail": (
            "Only 2 brands Amazon-absent (Nogent, Cl\u00e9 de Peau Beaut\u00e9). "
            "Below the pre-registered minimum of 5 for inferential testing."
        ),
    },
]

# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS
# ---------------------------------------------------------------------------

HYPOTHESIS_DETAILS = (
    "<b>P1 \u2014 Per-substrate predictive validity: FALSIFIED</b>\n"
    "Kitchen knives: rho = +0.048, p = 0.819 (n = 25)\n"
    "Audiophile headphones: rho = \u22120.116, p = 0.668 (n = 16)\n"
    "Skincare: rho = +0.049, p = 0.823 (n = 23)\n"
    "Cosmetics: ceiling effect (all C<sub>P</sub> = 6), rho undefined\n\n"

    "<b>P2 \u2014 Pooled correlation: FALSIFIED</b>\n"
    "88 listed brands, percentile-normalized BSR: "
    "rho = \u22120.0002, p = 0.998\n\n"

    "<b>P3 \u2014 Cell A separation: FALSIFIED</b>\n"
    "C<sub>P</sub> \u2265 4 (n = 78): median BSR percentile = 51.09\n"
    "C<sub>P</sub> < 4 (n = 10): median BSR percentile = 54.00\n"
    "Mann-Whitney U: not significant\n\n"

    "<b>P4 \u2014 Absence\u2013Presence alignment: UNDETERMINED</b>\n"
    "Only 2 absent brands across all substrates. Insufficient sample "
    "for the pre-registered Mann-Whitney U test (minimum n = 5)."
)

# ---------------------------------------------------------------------------
# CLOSING
# ---------------------------------------------------------------------------

CLOSING = (
    "AI Presence does not predict Amazon retail performance. "
    "That is not a flaw in the measure \u2014 it is evidence of what "
    "the measure captures. Combined with the convergent validity "
    "evidence from v0.25, this study establishes that AI Availability "
    "is a specific, novel construct: the breadth of a brand\u2019s "
    "recognition across AI knowledge systems, independent of "
    "commercial outcomes in retail channels.\n\n"

    "For brand leaders, the strategic implication is direct: "
    "AI Availability and Physical Availability are separate levers. "
    "Optimizing for one does not guarantee the other. The brands "
    "that language models recommend are not necessarily the brands "
    "that consumers buy on Amazon \u2014 and vice versa. Managing "
    "both systems requires distinct strategies, distinct metrics, "
    "and distinct investment."
)
