"""
v21_cosmetics_content.py — Content module for the v0.21 Third System
brand-format report.

Forked from v20_skincare_content.py with surgical content changes only.
Schema matches the contract consumed by build_report_v21.py (which is the
v20 builder forked surgically — same data shapes, different facts).

Attributes (in builder-consumption order):
  COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED,
  PATTERNS, LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING,
  HYPOTHESIS_DETAILS, CLOSING

PATTERNS items expose: number, title, chart_slot, chart_after_text (opt),
paragraphs. The chart_slot string is one of f1_cp_distribution,
f2_dissociation_scatter, f3_channel_asymmetry — resolved in build_report_v21.py
via _slot_lookup() to the v0.21 chart filenames in reports/figs/v21/.
"""

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "Type 2 Confirmation on the Cosmetics Substrate",
    "subtitle": (
        "Cultural-channel Recall populates the dissociation construct\u2019s "
        "third quadrant above the EMERGED threshold for the first time. "
        "Recognition saturates uniformly across all three IL-gradient cells, "
        "routing v1.5 C2 to a regime-floor failure and forcing the entire "
        "discrimination signal into Recall. The cosmetics panel anchors a "
        "fifth substrate family for the multi-component AI Availability "
        "construct, and Phantom Brand Persistence reaches its strongest "
        "single demonstration in the program."
    ),
    "date": "May 2026",
    "byline_short": "Pablo Ulpiano Gonz\u00e1lez Castro \u00b7 Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}


# ---------------------------------------------------------------------------
# STANDFIRST — single Paragraph (set in cover_subtitle style by builder)
# ---------------------------------------------------------------------------

STANDFIRST = (
    "AIAS\u2122 v0.21 replicates v1.5 on a cosmetics substrate stratified by "
    "Identity Load. The headline is structural: every panel brand scores "
    "C_P = 6/6, collapsing v1.5 C2 in all three cells and forcing the AIAS "
    "signal entirely into Recall. Three Cell B cases clear the EMERGED "
    "Type 2 threshold for the first time (Rare Beauty, Huda Beauty, Kylie "
    "Cosmetics); Rare Beauty\u2019s 1\u202f:\u202f17 R_cat\u202f:\u202fR_cult "
    "split anchors the program\u2019s textbook Recognition \u00d7 Recall "
    "dissociation. The cross-substrate generalization claim is defensible "
    "across five substrate families."
)


# ---------------------------------------------------------------------------
# LEAD_DECK — single Paragraph
# ---------------------------------------------------------------------------

LEAD_DECK = (
    "Three findings shape the v0.21 phase. First, Recognition saturates "
    "uniformly: every brand in every cell scores C_P = 6/6, producing "
    "distinct = 1 and modal share = 1.000 in all three cells. v1.5 C2 "
    "fails uniformly and Regime 4 routes to FALSIFIED at the regime-floor "
    "\u2014 the cleanest demonstration the program has produced that "
    "category-membership Recognition is not the discriminating channel for "
    "every substrate. Second, the Recognition \u00d7 Recall dissociation "
    "reaches its largest single-phase footprint: 13 Iwachu cases distributed "
    "across all three cells, with the construct now anchored across five "
    "substrate families. Third, the Type 2 quadrant transitions PARTIAL "
    "(v0.20) \u2192 EMERGED (v0.21) with three clean Cell B cases plus a "
    "first out-of-cell Type 2 surface in Cell C (e.l.f. Cosmetics), "
    "establishing the cultural-channel Recall pathway as a routine, not "
    "exceptional, feature of high-IL substrate tiers."
)


# ---------------------------------------------------------------------------
# EXEC_SUMMARY — list of paragraph strings
# ---------------------------------------------------------------------------

EXEC_SUMMARY = [
    (
        "AIAS\u2122 measures AI Availability \u2014 the probability that an AI "
        "intermediary retrieves, recommends, or selects a brand in a category-"
        "anchored decision context \u2014 as a third measurable layer of brand "
        "availability alongside the Ehrenberg-Bass framework\u2019s Mental and "
        "Physical Availability. Protocol v1.5 (SSRN 6810758) introduced two "
        "methodology refinements: a stricter within-cell adequacy rule "
        "(\u201cC2 multi-statistic\u201d) and a two-channel decomposition of "
        "category Recall into canonical retrieval (R_cat) and cultural-footprint "
        "retrieval (R_cult). v0.20 was the first prospective phase under v1.5; "
        "v0.21 is the first replication phase, holding the protocol fixed and "
        "testing it on a substrate selected to maximize Cell B Identity Load."
    ),
    (
        "The substrate is cosmetics, sampled across three IL-stratified cells "
        "of 8 brands each. Cell A (Prestige, medium IL): MAC Cosmetics, NARS, "
        "Bobbi Brown, Tom Ford Beauty, Giorgio Armani Beauty, Hourglass, "
        "Chantecaille, Laura Mercier. Cell B (Celebrity DTC / cult, high IL "
        "\u2014 the Type 2 hunting cell): Rare Beauty, Fenty Beauty, Haus "
        "Labs, Pat McGrath Labs, Charlotte Tilbury, Huda Beauty, Kylie "
        "Cosmetics, Anastasia Beverly Hills. Cell C (Drugstore / mass, low "
        "IL): Maybelline, L\u2019Or\u00e9al Paris, CoverGirl, Revlon, NYX "
        "Professional Makeup, e.l.f. Cosmetics, Wet n Wild, Milani Cosmetics. "
        "Reference panel: the six-slot LLM panel carried forward from v0.17 "
        "(Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 "
        "Flash, Gemini 2.5 Flash Lite)."
    ),
    (
        "Four hypotheses were pre-registered (tag v0.21-prereg-r1) prior to "
        "any acquisition. H_Type2_emergence \u2014 the primary hypothesis "
        "\u2014 returned EMERGED: three Cell B cases at threshold (Rare "
        "Beauty with R_cat = 1 and R_cult = 17; Huda Beauty with R_cat = 0 "
        "and R_cult = 11; Kylie Cosmetics with R_cat = 0 and R_cult = 5), "
        "plus a fourth Type 2 case in Cell C (e.l.f. Cosmetics, R_cat = 1, "
        "R_cult = 9) \u2014 the first out-of-cell Type 2 surface in the "
        "program. The Type 2 quadrant is no longer marginal; it is the "
        "expected pattern for high-IL substrate tiers."
    ),
    (
        "H_Regime4_cosmetics returned FALSIFIED on v1.5 C2 failing in all "
        "three cells. The failure is uniform rather than differential: "
        "every cell shows distinct count = 1 and modal share = 1.000. The "
        "verdict carries a structural finding: cosmetics is a category in "
        "which LLM Recognition collapses to ceiling because every brand "
        "that would plausibly be on the panel is correctly categorized as "
        "a cosmetics brand by every model. The methodological implication "
        "is substantive: for substrates with this property, the v1.5 "
        "framework\u2019s discrimination signal lives entirely in Recall."
    ),
    (
        "H_Dissociation_substrate_generalization returned GENERALIZED \u2014 "
        "the strongest available verdict \u2014 with Iwachu-pattern cases "
        "distributed across all three cosmetics cells (13 cases total: 4 "
        "Cell A, 4 Cell B, 5 Cell C). The v1.4/v1.5 multi-component "
        "construct is now anchored across five substrate families "
        "(Japanese kitchenware via v0.17, indie fragrance via v0.18, "
        "audiophile electronics via v0.19, skincare via v0.20, cosmetics "
        "via v0.21). The cross-substrate generalization claim AIAS\u2122 "
        "1.0 will make is defensible on the data the program has shipped."
    ),
    (
        "H_IdentityLoad_moderator (five-leg joint) returned NARROWED, driven "
        "structurally by the v0.21 Regime 4 falsification. But the raw "
        "channel data tracks the IL-gradient prediction more cleanly than "
        "any prior phase: Cell A R_cat-leading (5.75 vs. 2.62), Cell B "
        "strongly R_cult-leading (11.00 vs. 3.88 \u2014 a 2.83\u00d7 lead). "
        "The substantive IL signature is the strongest the program has "
        "observed and reinforces the case for a Protocol v1.6 moderator "
        "pathway evaluable independently of Regime 4\u2019s C2 conditions."
    ),
]


# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED — heading + paragraphs
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "Two measurements were taken against a locked panel of six LLMs. "
            "Brand registry and probe wording were locked at pre-registration "
            "before any data collection (tag v0.21-prereg-r1)."
        ),
        (
            "<b>Phase A \u2014 Recognition.</b> For each of the 24 brands in "
            "the panel, each of the 6 LLMs was asked: \u201cIs the brand X "
            "commonly recognized as a cosmetics brand? Answer yes or no.\u201d "
            "The brand\u2019s C_P score (range 0\u20136) is the count of yes "
            "responses. C_P is the Recognition component of AI Availability."
        ),
        (
            "<b>Phase B \u2014 Recall, two-channel decomposition.</b> Six "
            "category-anchored queries were sent to each of the 6 LLMs (36 "
            "total queries). Three queries anchor the canonical channel "
            "(R_cat): best cosmetics brands, makeup-artist-recommended, "
            "highest quality / most reliable. Three queries anchor the "
            "cultural-footprint channel (R_cult): popular right now, "
            "celebrity / influencer, viral or cult-favorite. For each "
            "(frame \u00d7 LLM) response, the 24-brand registry was scanned "
            "for mention presence using case-insensitive, accent-stripped, "
            "possessive-aware matching. Per-brand R_cat (max 18) and R_cult "
            "(max 18) follow."
        ),
        (
            "<b>Three dissociation patterns are recognized at the v1.5 "
            "thresholds.</b> Iwachu: high Recognition with sparse canonical "
            "Recall (C_P \u2265 5 \u2227 R_cat \u2264 2). Type 1: canonical-"
            "channel-preferred (R_cat \u2265 5 \u2227 R_cult \u2264 2). Type "
            "2: cultural-channel-preferred (R_cat \u2264 2 \u2227 R_cult "
            "\u2265 5). Type 2 emergence above the EMERGED threshold (\u2265 "
            "3 Cell B cases) is the primary v0.21 hypothesis."
        ),
        (
            "<b>v1.5 C2 multi-statistic.</b> A cell passes C2 when it carries "
            "at least three distinct C_P values and its modal C_P share is "
            "at most 0.625. The rule was calibrated retrospectively against "
            "joint v0.18 + v0.19 data and tested prospectively for the first "
            "time in v0.20. v0.21 holds the rule fixed and tests it on a "
            "substrate where Recognition collapses to ceiling uniformly."
        ),
    ],
}


# ---------------------------------------------------------------------------
# PATTERNS — three findings, each with a chart_slot
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "Recognition saturates uniformly. The discrimination signal lives in Recall.",
        "chart_slot": "f1_cp_distribution",
        "paragraphs": [
            (
                "Every brand in every cell scores C_P = 6/6. All 24 panel "
                "brands across prestige, celebrity-DTC, and drugstore-mass "
                "tiers are recognized as cosmetics brands by every one of "
                "the six panel LLMs. There are no exceptions \u2014 not at "
                "the prestige tier, not in the celebrity-DTC tier where "
                "v0.20 Cell B showed substantial within-cell C_P variance, "
                "not in the mass-market tier where one might have expected "
                "the lower-distribution brands to fall short."
            ),
            (
                "v1.5 C2 fails uniformly. Cell A: distinct = 1, modal share "
                "= 1.000. Cell B: distinct = 1, modal share = 1.000. Cell "
                "C: distinct = 1, modal share = 1.000. The rule\u2019s "
                "logic is correct: a fully saturated within-cell "
                "distribution doesn\u2019t supply the variance the C3 "
                "rank-coherence analysis would consume. The cell-floor "
                "failure routes Regime 4 to FALSIFIED at the regime-floor, "
                "before any IL-gradient guard or Phase D check is reached."
            ),
            (
                "The structural finding is the headline. Cosmetics is a "
                "maximally-coded category at the Recognition layer: "
                "category-membership classification is binary-true for "
                "every brand that would plausibly appear on the panel. "
                "This is not panel inadequacy in the v0.17 sense (n is "
                "sufficient at 8 per cell, 24 worldwide); it is substrate "
                "ceiling. For substrates with this property, "
                "category-membership Recognition is not the discriminating "
                "channel \u2014 the AIAS signal lives entirely in Recall."
            ),
            (
                "The methodological implication is substantive: the v1.5 "
                "framework\u2019s four-regime taxonomy needs an additional "
                "pre-screen for substrate-level Recognition saturation. "
                "When all three cells fail C2 by identical uniform "
                "saturation, the verdict carries different information than "
                "when cells fail differently (as in v0.20, where Cell C "
                "saturated, Cell A was bimodal, and Cell B passed). The "
                "v0.21 falsification documents what the rule does when the "
                "substrate is categorically self-evident; v1.6 should "
                "capture this case distinctly."
            ),
        ],
    },
    {
        "number": 2,
        "title": "Iwachu dissociation now anchors five substrate families with multi-cell distribution.",
        "chart_slot": "f2_dissociation_scatter",
        "paragraphs": [
            (
                "The Iwachu pattern \u2014 brands that LLMs recognize as "
                "members of a category but don\u2019t list when asked to "
                "enumerate the category \u2014 was first observed in v0.17 "
                "on the Japanese kitchen-knives substrate. v0.18 extended "
                "it to indie fragrance in higher-IL cells. v0.19 confirmed "
                "it on audiophile electronics in the Boutique cell. v0.20 "
                "extended it to skincare with cases in all three cells. "
                "v0.21 produces thirteen Iwachu cases on the cosmetics "
                "panel \u2014 the largest single-phase count in the "
                "program \u2014 distributed across all three cells."
            ),
            (
                "Cell A contributes four cases: Tom Ford Beauty (R_cat = 2), "
                "Giorgio Armani Beauty (R_cat = 0), Hourglass (R_cat = 1), "
                "Chantecaille (R_cat = 0). Cell B contributes four: Rare "
                "Beauty (R_cat = 1), Haus Labs (R_cat = 0), Huda Beauty "
                "(R_cat = 0), Kylie Cosmetics (R_cat = 0) \u2014 with "
                "three of these qualifying simultaneously as Type 2 (the "
                "primary hypothesis). Cell C contributes five: CoverGirl, "
                "Revlon, Wet n Wild, Milani Cosmetics (all R_cat = 0, "
                "R_cult = 0) and e.l.f. Cosmetics (R_cat = 1, R_cult = 9)."
            ),
            (
                "The Cell C pattern is itself substantively interesting: "
                "four of the five drugstore-mass Iwachu cases produce zero "
                "mentions in both channels. The cell carries categorical "
                "Recognition but minimal retrieval salience overall \u2014 "
                "LLMs recognize these as cosmetics brands when asked, but "
                "don\u2019t surface them in either canonical or cultural "
                "frames. The cell\u2019s Recall presence concentrates in "
                "four of its eight brands (Maybelline, L\u2019Or\u00e9al "
                "Paris, NYX, e.l.f.); the remaining four are AI-recognized "
                "but AI-invisible."
            ),
            (
                "For AIAS\u2122 1.0\u2019s headline cross-substrate "
                "generalization claim, this is the empirical ground the "
                "methodology layer required. The pattern is not specific "
                "to any one substrate, language family, or cultural "
                "context. Five substrate families, multi-cell distribution "
                "in three of them (v0.18, v0.20, v0.21), and consistent "
                "directional behavior across all five. The construct is "
                "as cross-substrate generalized as a five-family anchor "
                "base can make it."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Type 2 emerges above threshold. Rare Beauty anchors the program\u2019s textbook dissociation case.",
        "chart_slot": "f3_channel_asymmetry",
        "paragraphs": [
            (
                "Through v0.20, the v1.5 dissociation framework predicted "
                "three quadrants and populated the third only marginally: "
                "v0.20 Cell B produced two clean Type 2 cases (Glossier, "
                "Rhode) with a third at the boundary (Augustinus Bader at "
                "R_cat = 2), routing H_Type2_emergence to PARTIAL. v0.21 "
                "produces three Cell B cases above threshold: Rare Beauty "
                "(R_cat = 1, R_cult = 17), Huda Beauty (R_cat = 0, R_cult "
                "= 11), Kylie Cosmetics (R_cat = 0, R_cult = 5). The "
                "primary hypothesis routes to EMERGED."
            ),
            (
                "Rare Beauty anchors the result. C_P = 6, R_cat = 1, "
                "R_cult = 17 \u2014 universally categorized as cosmetics "
                "by LLMs, essentially never surfaced when one asks for the "
                "best or most-recommended, and almost always surfaced in "
                "popular / celebrity / viral frames. This 1\u202f:\u202f17 "
                "channel split is the program\u2019s textbook Recognition "
                "\u00d7 Recall dissociation and the strongest single-brand "
                "demonstration of why a multi-component AI Availability "
                "construct is the right primitive. A fourth Type 2 case "
                "surfaces out of the predicted hunting cell: e.l.f. "
                "Cosmetics (Cell C, R_cat = 1, R_cult = 9) \u2014 the "
                "first out-of-cell Type 2 surface in the program. "
                "e.l.f.\u2019s drugstore-mass tier on the supply side "
                "coexists with a social-media-native cultural footprint "
                "that crosses the IL-gradient cell boundary the panel "
                "design assumes, informing cell-classification more than "
                "the Type 2 mechanism."
            ),
            (
                "For brand strategy, the substantive implication is "
                "sharpened. A brand\u2019s AI Availability has at least "
                "two components that can move independently and "
                "asymmetrically far apart. Rare Beauty\u2019s 1\u202f:\u202f17 "
                "channel split establishes the upper bound on how "
                "decoupled the two components can be while remaining a "
                "single brand. The two require different inputs to "
                "influence \u2014 canonical-channel Recall responds to "
                "authority surfaces (editorial, expert recommendation, "
                "category-best lists); cultural-channel Recall responds "
                "to discourse density (social media, celebrity "
                "endorsement, viral content). The two pathways operate "
                "on disjoint inputs and can be managed separately."
            ),
        ],
    },
]


# ---------------------------------------------------------------------------
# LIMITATIONS — heading + paragraphs
# ---------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "Uniform Recognition saturation precludes any within-cell rank-"
            "coherence analysis in v0.21. Spearman rank correlation between "
            "C_P and R_cat is mathematically undefined when one input has "
            "zero variance; this holds in all three cells. The "
            "discrimination signal that v1.5\u2019s C3 layer was designed "
            "to evaluate cannot be evaluated on the cosmetics substrate at "
            "the C_P resolution the probe template provides."
        ),
        (
            "Cell-classification limits surfaced through the e.l.f. "
            "Cosmetics out-of-cell Type 2 case. The IL-gradient cell "
            "structure assumes brands behave per their supply-side tier "
            "classification; a brand with mass-market price points and a "
            "social-media-native marketing identity violates that "
            "assumption. Future panel designs may benefit from an "
            "auxiliary cultural-presence pre-classification independent "
            "of price-tier."
        ),
        (
            "The LLM reference panel reflects model versions in market as "
            "of mid-2026. Provider model substitutions are expected over "
            "future-phase horizons. v0.21\u2019s Type 2 cases should be "
            "interpreted as the pattern observed against the locked panel "
            "at acquisition time, not as a permanent property of the "
            "substrate."
        ),
        (
            "The panel is tier-balanced (eight brands per cell) rather "
            "than market-cap-complete \u2014 n = 8 per cell holds across "
            "the program for cross-phase comparability. The acquisition "
            "log surfaced substantial off-panel brand presence the panel-"
            "internal scoring doesn\u2019t capture: Glossier (a v0.20 "
            "Cell B panel brand) appeared in cultural-channel frames for "
            "all six LLMs in q6 and three of six in q4 and q5 \u2014 the "
            "strongest single Phantom Brand Persistence demonstration in "
            "the program. Est\u00e9e Lauder appeared in the canonical "
            "channel for all six models (R_cat = 13/18). Non-trivial "
            "Phase B presence also surfaced for Urban Decay, Make Up For "
            "Ever, Clinique, Lanc\u00f4me, and Too Faced. The panel-"
            "internal scoring is correct under the locked methodology, "
            "but the off-panel pattern is informative about both panel "
            "design and the construct\u2019s ecosystem footprint; "
            "reviewers of the cosmetics substrate should anticipate this "
            "question."
        ),
    ],
}


# ---------------------------------------------------------------------------
# WHATS_NEXT — heading + paragraphs
# ---------------------------------------------------------------------------

WHATS_NEXT = {
    "heading": "What\u2019s next",
    "paragraphs": [
        (
            "<b>Five-family anchor base reached.</b> With v0.21 in place, "
            "the AIAS\u2122 program\u2019s cross-substrate generalization "
            "claim spans five distinct substrate families "
            "(kitchenware, fragrance, audio electronics, skincare, "
            "cosmetics), with all three dissociation quadrants empirically "
            "populated, multi-cell Iwachu distribution in three families, "
            "and Type 2 emergence above the EMERGED threshold in one. The "
            "headline cross-substrate claim for AIAS\u2122 1.0 is "
            "defensible on data shipped through v0.21."
        ),
        (
            "<b>Protocol v1.6 candidates.</b> The v0.21 falsification "
            "pattern sharpens the case for a v1.6 increment in three "
            "directions. First, a substrate-level Recognition pre-screen "
            "that distinguishes uniform-saturation cases (cosmetics) from "
            "differential-saturation cases (v0.20 skincare) before C2 "
            "routing. Second, a moderator-evaluation pathway evaluable "
            "independently of Regime 4\u2019s C2 conditions \u2014 the "
            "v0.21 raw channel asymmetry (Cell B R_cult 11.00 vs. R_cat "
            "3.88) is the strongest IL signature in the program but is "
            "captured only descriptively under the current verdict "
            "matrix. Third, a Phantom Brand Persistence extension scoring "
            "off-panel Phase B mentions (Glossier at 6/6 model coverage "
            "in q6, Est\u00e9e Lauder at 13/18 R_cat) against a larger "
            "reference vocabulary \u2014 lifting this from side "
            "observation to measured component."
        ),
        (
            "<b>AIAS\u2122 1.0 trajectory.</b> Remaining work to lock the "
            "1.0 release: a Protocol v1.6 increment for the moderator and "
            "Phantom pathways noted above, and a synthesis paper "
            "consolidating the five-family anchor base. The v0.21 phase "
            "completes the substrate breadth requirement; the remaining "
            "work is methodology-internal."
        ),
    ],
}


# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING — heading + intro + rows (5-tuples)
# Row format: (h_id, prediction, result, status_text, status_class)
# status_class ∈ {"confirmed", "partial", "disconfirmed", "descriptive"}
# ---------------------------------------------------------------------------

HYPOTHESIS_SCORING = {
    "heading": "Pre-registered hypothesis scoring",
    "intro": (
        "Four hypotheses were pre-registered at tag v0.21-prereg-r1, prior "
        "to any acquisition. Verdict matrices were locked ex-ante. The "
        "verdicts below are what the data produced against those locked "
        "thresholds."
    ),
    "rows": [
        (
            "H_Type2_emergence",
            "Cultural-channel Recall populates the Type 2 quadrant (R_cat \u2264 2 "
            "\u2227 R_cult \u2265 5) in Cell B at post-attrition n \u2265 5. "
            "EMERGED requires \u2265 3 Cell B cases; PARTIAL routes 1\u20132.",
            "Three Cell B cases above threshold: Rare Beauty (R_cat = 1, "
            "R_cult = 17), Huda Beauty (R_cat = 0, R_cult = 11), Kylie "
            "Cosmetics (R_cat = 0, R_cult = 5). Plus e.l.f. Cosmetics "
            "(Cell C, R_cat = 1, R_cult = 9) \u2014 first out-of-cell Type 2.",
            "EMERGED",
            "confirmed",
        ),
        (
            "H_Regime4_cosmetics",
            "Four-regime substantive test under v1.5: C1 (n \u2265 12) \u2192 "
            "C2 multi-statistic (distinct C_P \u2265 3 \u2227 modal \u2264 "
            "0.625, per cell) \u2192 IL-gradient guard \u2192 C3 per-cell "
            "\u03c1. FALSIFIED if C2 fails in \u2265 2 cells.",
            "C2 fails in all three cells with identical uniform-saturation "
            "shape: Cell A distinct = 1, modal = 1.000; Cell B distinct = 1, "
            "modal = 1.000; Cell C distinct = 1, modal = 1.000. Resolved at "
            "C2 (regime-floor failure).",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H_Dissociation_substrate_generalization",
            "Iwachu-pattern cases (C_P \u2265 5 \u2227 R_cat \u2264 2) appear "
            "in \u2265 2 of 3 cells. GENERALIZED routes to all-3-cell "
            "distribution; PARTIAL routes single-cell concentration.",
            "13 Iwachu cases distributed across all three cells (4 Cell A, "
            "4 Cell B, 5 Cell C). Construct now anchored across five substrate "
            "families; largest single-phase Iwachu count in the program.",
            "GENERALIZED",
            "confirmed",
        ),
        (
            "H_IdentityLoad_moderator",
            "Five-leg joint over v0.16 \u00d7 v0.17 \u00d7 v0.18 \u00d7 v0.20 "
            "\u00d7 v0.21 (v0.19 excluded; uniform-IL design). Joint matrix "
            "routes pessimistically when within-phase Regime 4 test "
            "falsifies (not on panel inadequacy).",
            "v0.21 Regime 4 FALSIFIED (not on panel inadequacy) routes joint "
            "to NARROWED. Substantive channel asymmetry tracks IL gradient "
            "more cleanly than any prior phase (Cell B R_cult-lead = 2.83\u00d7).",
            "NARROWED",
            "descriptive",
        ),
    ],
}


# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS — heading + intro + items (2-tuples)
# Item format: (h_id, body_text)
# ---------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis interpretation",
    "intro": (
        "Each verdict carries substantive interpretation beyond the matrix "
        "routing. The verdicts are what the data produced; the meaning of "
        "each verdict for the construct, the moderator, and the v0.22+ "
        "trajectory is what the prose below addresses."
    ),
    "items": [
        (
            "H_Type2_emergence",
            "<b>What it means.</b> The cultural-channel Recall pathway is "
            "established as a routine, not exceptional, feature of high-IL "
            "substrate tiers. Three Cell B cases above the EMERGED "
            "threshold across one phase \u2014 plus a fourth out-of-cell "
            "case in Cell C \u2014 establishes that the Type 2 quadrant "
            "is densely populable where Identity Load is high. Rare "
            "Beauty\u2019s 1\u202f:\u202f17 channel split is the program\u2019s "
            "textbook Recognition \u00d7 Recall dissociation case. <b>What "
            "it doesn\u2019t mean.</b> EMERGED is not universal. Cell A "
            "(Prestige) produced zero Type 2 cases; Type 1 dominated Cell A "
            "instead (Bobbi Brown, Laura Mercier). The cultural-channel "
            "Recall pathway is tier-specific within a substrate, and the "
            "tier specificity is the moderator hypothesis\u2019s "
            "substantive signature even where the formal verdict routes "
            "to NARROWED."
        ),
        (
            "H_Regime4_cosmetics",
            "<b>What it means.</b> The structural finding is the headline: "
            "cosmetics is a maximally-coded category at the Recognition "
            "channel. Every brand scores C_P = 6/6 and v1.5 C2 fails by "
            "the widest possible margin in all three cells. The rule "
            "correctly identifies that no within-cell discrimination is "
            "available from Recognition alone. <b>What it doesn\u2019t "
            "mean.</b> FALSIFIED is not a refutation of the underlying "
            "construct \u2014 the substrate is one where Recognition is "
            "structurally unavailable as a discriminator and the entire "
            "signal lives in Recall. A v1.6 substrate-level pre-screen "
            "would route uniform-saturation substrates distinctly from "
            "the differential-saturation case v0.20 exhibited."
        ),
        (
            "H_Dissociation_substrate_generalization",
            "<b>What it means.</b> The multi-component Recognition \u00d7 "
            "Recall construct is now empirically anchored across five "
            "substrate families. v0.21 contributes the largest single-"
            "phase Iwachu count in the program (13) with multi-cell "
            "distribution across all three cells. For AIAS\u2122 1.0\u2019s "
            "headline cross-substrate generalization claim, this is the "
            "five-family anchor base the methodology layer required. The "
            "pattern is not specific to any one substrate, language, or "
            "cultural context. <b>What it doesn\u2019t mean.</b> "
            "GENERALIZED does not mean the dissociation pattern operates "
            "identically across all substrate families. The cell "
            "distribution remains substrate-specific \u2014 multi-cell in "
            "v0.18 and v0.20 and v0.21, weighted-concentration in v0.19, "
            "cross-cultural in v0.17. The pattern generalizes; its cell "
            "distribution does not."
        ),
        (
            "H_IdentityLoad_moderator",
            "<b>What it means.</b> The verdict-vs-data tension is sharpened "
            "in v0.21. NARROWED reflects matrix pessimism \u2014 when "
            "within-phase Regime 4 falsifies, the joint backs off \u2014 "
            "but the moderator\u2019s substantive signature is more "
            "visible than in any prior phase: Cell B R_cult 11.00 vs. "
            "R_cat 3.88 (a 2.83\u00d7 cultural-channel lead); Cell A "
            "opposite-direction R_cat-leading at 5.75 vs. 2.62. The IL-"
            "gradient predicts directional asymmetry that operates "
            "exactly as v0.21 shows. <b>What it doesn\u2019t mean.</b> "
            "NARROWED is bounded, not refuted. Across five legs "
            "(PARTIAL, FALSIFIED-on-panel-inadequacy, PARTIAL, FALSIFIED, "
            "FALSIFIED), the moderator operates with substrate-specific "
            "qualifications. v0.21 supplies the strongest IL-tracking "
            "channel-asymmetry evidence in the program."
        ),
    ],
}


# ---------------------------------------------------------------------------
# CLOSING — byline_long + datasets + methodology_log
# ---------------------------------------------------------------------------

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano Gonz\u00e1lez Castro",
        "School of Visual Arts, MPS Branding Program \u00b7 New York, NY",
        "Third System\u2122 (research entity; data archive and methodology venue)",
        "Correspondence: pablou@pablou.com \u00b7 ORCID: 0009-0003-8968-9990",
    ],
    "datasets": [
        "v0.21 Phase A acquisition (Recognition C_P, n = 144 probes): "
        "osf.io/ec6wh/v21/data/phase_a_results.csv",
        "v0.21 Phase B acquisition (Recall two-channel, n = 36 queries): "
        "osf.io/ec6wh/v21/data/phase_b_results.csv",
        "v0.21 scoring verdicts (four hypothesis matrices resolved): "
        "osf.io/ec6wh/v21/data/v21_verdicts.json",
        "v0.21 brand registry (locked at pre-reg r1): "
        "osf.io/ec6wh/v21/prereg/v0_21_registry.json",
    ],
    "methodology_log": (
        "v0.21 pre-registration locked at git tag v0.21-prereg-r1, branch "
        "v0.21-cosmetics-il-gradient. Replicates Protocol v1.5 (SSRN "
        "6810758); first prospective replication of v0.20\u2019s C2 "
        "calibration. Acquisition locked at git tag v0.21-acquisition-"
        "locked. Academic companion: SSRN TBD"
    ),
}
