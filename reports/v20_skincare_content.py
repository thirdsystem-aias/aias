"""
v20_skincare_content.py — Content module for the v0.20 Third System
brand-format report.

Forked from v19_audiophile_content.py with surgical content changes only.
Schema matches the contract consumed by build_report_v20.py (which is the
v19 builder forked surgically — same data shapes, different facts).

Attributes (in builder-consumption order):
  COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED,
  PATTERNS, LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING,
  HYPOTHESIS_DETAILS, CLOSING

PATTERNS items expose: number, title, chart_slot, chart_after_text (opt),
paragraphs. The chart_slot string is one of f1_cp_distribution,
f2_dissociation_scatter, f3_channel_asymmetry — resolved in build_report_v20.py
via _slot_lookup() to the v0.20 chart filenames in reports/figs/v20/.
"""

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "Type 2 Emergence on the Skincare Substrate",
    "subtitle": (
        "Cultural-channel Recall populates the construct\u2019s third dissociation "
        "quadrant for the first time. The skincare panel anchors a fourth substrate "
        "family for the multi-component AI Availability construct, and v1.5\u2019s "
        "C2 multi-statistic ships its first prospective test."
    ),
    "date": "May 2026",
    "byline_short": "Pablo Ulpiano Gonz\u00e1lez Castro \u00b7 Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}


# ---------------------------------------------------------------------------
# STANDFIRST — single Paragraph (set in cover_subtitle style by builder)
# ---------------------------------------------------------------------------

STANDFIRST = (
    "AIAS\u2122 v0.20 ships the first prospective phase under v1.5 methodology. "
    "The substrate is skincare, sampled across three cells stratified by Identity "
    "Load. The headline result is empirical: a category of AI brand presence that "
    "the program\u2019s earlier measurements had not yet captured \u2014 brands "
    "that LLMs surface heavily in cultural-discovery frames while surfacing zero "
    "or near-zero times in canonical category frames \u2014 is now populated. "
    "Glossier and Rhode anchor the Type 2 quadrant. The construct\u2019s "
    "cross-substrate generalization claim is defensible across four substrate "
    "families."
)


# ---------------------------------------------------------------------------
# LEAD_DECK — single Paragraph
# ---------------------------------------------------------------------------

LEAD_DECK = (
    "Three findings shape the v0.20 phase. First, the cultural-channel Recall "
    "pathway is real and measurable: two clean Type 2 cases (Glossier and Rhode) "
    "appear in Cell B, populating the v1.5 dissociation framework\u2019s third "
    "quadrant for the first time. Second, the v1.5 C2 multi-statistic rule "
    "behaves on three differently-shaped within-cell distributions exactly as "
    "the methodology paper specified \u2014 accepting variance-rich Cell B, "
    "rejecting saturated Cell C, rejecting bimodal Cell A. Third, the "
    "Recognition \u00d7 Recall dissociation construct extends to a fourth "
    "substrate family with Iwachu cases in all three skincare cells, the "
    "strongest available generalization verdict."
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
        "retrieval (R_cult). v0.20 is the first prospective phase under v1.5."
    ),
    (
        "The substrate is skincare, sampled across three IL-stratified cells of "
        "8 brands each. Cell A (Prestige, medium IL): Est\u00e9e Lauder, "
        "Lanc\u00f4me, La Mer, Sisley, Dior Beauty, Chanel Beauty, La Prairie, "
        "Cl\u00e9 de Peau Beaut\u00e9. Cell B (Celebrity DTC / cult, high IL "
        "\u2014 the Type 2 hunting cell): Rare Beauty, Rhode, Fenty Skin, Goop, "
        "Drunk Elephant, Glossier, Augustinus Bader, Tower 28. Cell C (Clinical, "
        "low IL): SkinCeuticals, La Roche-Posay, Paula\u2019s Choice, CeraVe, "
        "The Ordinary, Cetaphil, Eucerin, Bioderma. Reference panel: the six-slot "
        "LLM panel carried forward from v0.17 (Claude Opus 4.5, Claude Sonnet "
        "4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite)."
    ),
    (
        "Four hypotheses were pre-registered at commit 4e5ab60 (tag "
        "v0.20-prereg-r1). H_Type2_emergence \u2014 the primary novel "
        "hypothesis \u2014 returned PARTIAL: two clean Type 2 cases in Cell B "
        "(Glossier with R_cult = 9 and zero R_cat; Rhode with R_cult = 8 and "
        "zero R_cat). The Type 2 quadrant is empirically populated for the "
        "first time across the AIAS\u2122 program."
    ),
    (
        "H_Regime4_skincare returned FALSIFIED on v1.5 C2 failing in two of "
        "three cells. The failure pattern is the methodological finding: "
        "Cell C (clinical, fully saturated) and Cell A (prestige, bimodal) "
        "are both correctly rejected by the rule; Cell B (variance-rich) "
        "passes. The first prospective v1.5 C2 exercise behaves as the "
        "methodology paper predicted across three different distributional "
        "shapes."
    ),
    (
        "H_Dissociation_substrate_generalization returned GENERALIZED \u2014 "
        "the strongest available verdict \u2014 with Iwachu-pattern cases "
        "distributed across all three skincare cells. The v1.4/v1.5 "
        "multi-component construct is now anchored across four substrate "
        "families (Japanese kitchenware via v0.17, indie fragrance via v0.18, "
        "audiophile electronics via v0.19, skincare via v0.20). The "
        "cross-substrate generalization claim AIAS\u2122 1.0 will make is "
        "defensible on the data the program has shipped."
    ),
    (
        "H_IdentityLoad_moderator (four-leg joint) returned NARROWED, driven "
        "structurally by the v0.20 Regime 4 falsification. But the raw "
        "channel data tracks the IL-gradient prediction exactly: Cell C "
        "(low IL) is canonical-channel-dominant (mean R_cat = 10.88 vs. "
        "R_cult = 8.38); Cell B (high IL) is cultural-channel-dominant "
        "(mean R_cult = 5.38 vs. R_cat = 1.62). The verdict-vs-data tension "
        "is itself interpretively informative and suggests a Protocol v1.6 "
        "candidate: a moderator-evaluation pathway evaluable independently "
        "of Regime 4\u2019s C2 conditions."
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
            "before any data collection (commit 4e5ab60, tag v0.20-prereg-r1)."
        ),
        (
            "<b>Phase A \u2014 Recognition.</b> For each of the 24 brands in "
            "the panel, each of the 6 LLMs was asked: \u201cIs the brand X "
            "commonly recognized as a skincare brand? Answer yes or no.\u201d "
            "The brand\u2019s C_P score (range 0\u20136) is the count of yes "
            "responses. C_P is the Recognition component of AI Availability."
        ),
        (
            "<b>Phase B \u2014 Recall, two-channel decomposition.</b> Six "
            "category-anchored queries were sent to each of the 6 LLMs (36 "
            "total queries). Three queries anchor the canonical channel "
            "(R_cat): best skincare brands, dermatologist-recommended, most "
            "effective. Three queries anchor the cultural-footprint channel "
            "(R_cult): popular right now, celebrity / influencer, viral or "
            "cult-favorite. For each (frame \u00d7 LLM) response, the 24-brand "
            "registry was scanned for mention presence using case-insensitive, "
            "accent-stripped, possessive-aware matching. Per-brand R_cat (max "
            "18) and R_cult (max 18) follow."
        ),
        (
            "<b>Three dissociation patterns are recognized at the v1.5 "
            "thresholds.</b> Iwachu: high Recognition with sparse canonical "
            "Recall (C_P \u2265 5 \u2227 R_cat \u2264 2). Type 1: canonical-"
            "channel-preferred (R_cat \u2265 5 \u2227 R_cult \u2264 2). Type "
            "2: cultural-channel-preferred (R_cat \u2264 2 \u2227 R_cult "
            "\u2265 5). Type 2 is the primary novel target of v0.20."
        ),
        (
            "<b>v1.5 C2 multi-statistic.</b> A cell passes C2 when it carries "
            "at least three distinct C_P values and its modal C_P share is "
            "at most 0.625. Calibrated retrospectively against joint v0.18 + "
            "v0.19 data; v0.20 is the first phase to lock the rule into "
            "pre-registration prospectively."
        ),
    ],
}


# ---------------------------------------------------------------------------
# PATTERNS — three findings, each with a chart_slot
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "Recognition is not uniform across cells.",
        "chart_slot": "f1_cp_distribution",
        "paragraphs": [
            (
                "Cell C (Clinical) is fully Recognition-saturated. All eight "
                "brands score C_P = 6/6 \u2014 every dermatologist-recommended "
                "brand in the panel is recognized as a skincare brand by "
                "every LLM. Distinct C_P count = 1; modal share = 1.000. "
                "v1.5 C2 correctly rejects: a fully saturated distribution "
                "doesn\u2019t supply the within-cell variance the analytical "
                "pipeline needs."
            ),
            (
                "Cell A (Prestige) is bimodal. Six brands score C_P = 6/6 "
                "(Est\u00e9e Lauder, Lanc\u00f4me, La Mer, Sisley, La "
                "Prairie, Cl\u00e9 de Peau Beaut\u00e9), two score C_P = 3/6 "
                "(Dior Beauty, Chanel Beauty). The bimodality reflects which "
                "prestige beauty houses LLMs primarily categorize as skincare "
                "versus those they primarily categorize as cosmetics or "
                "fragrance with skincare extension lines. v1.5 C2 also "
                "rejects: distinct values of 2 are below the floor of 3, "
                "modal share of 0.750 exceeds the 0.625 ceiling."
            ),
            (
                "Cell B (Celebrity DTC) is variance-rich. Five brands score "
                "C_P = 6/6 (Rhode, Fenty Skin, Drunk Elephant, Glossier, "
                "Augustinus Bader), two score C_P = 2/6 (Goop, Tower 28), "
                "one scores C_P = 0/6 (Rare Beauty \u2014 its primary LLM "
                "brand identity is makeup). v1.5 C2 passes cleanly: distinct "
                "count of 3 meets the floor; modal share of 0.625 sits "
                "exactly at the ceiling. This is the cell the rule was "
                "designed for, and v0.20 confirms the rule behaves on real "
                "data as calibrated."
            ),
            (
                "The first prospective v1.5 C2 exercise therefore behaves "
                "across three differently-shaped distributions exactly as "
                "the methodology paper specified \u2014 accepting variance-"
                "rich cells, rejecting saturated cells, rejecting bimodal "
                "cells. The rule\u2019s prospective utility is established."
            ),
        ],
    },
    {
        "number": 2,
        "title": "Iwachu dissociation now anchors four substrate families.",
        "chart_slot": "f2_dissociation_scatter",
        "paragraphs": [
            (
                "The Iwachu pattern \u2014 brands that LLMs recognize as "
                "members of a category but don\u2019t list when asked to "
                "enumerate the category \u2014 was first observed in v0.17 "
                "on the Japanese kitchen-knives substrate (Iwachu, Vermicular "
                "and related). v0.18 extended it to indie fragrance with "
                "cases in the higher-IL cells. v0.19 confirmed it on "
                "audiophile electronics in the Boutique cell. v0.20 extends "
                "it to skincare with cases in all three cells \u2014 eleven "
                "total, the most of any single phase to date."
            ),
            (
                "Cell A contributes the bulk: the high-Recognition prestige "
                "brands have near-zero canonical Recall (Cell A total R_cat "
                "= 3 across 8 brands). Cell B contributes brands that "
                "simultaneously qualify as Type 2 \u2014 the same C_P = 6 / "
                "R_cat \u2264 2 brands surface again in the cultural-channel "
                "frames. Cell C contributes the cell\u2019s less consumer-"
                "facing brands \u2014 typically the more specialized "
                "clinical names operating below the cell\u2019s top-of-mind "
                "ceiling."
            ),
            (
                "For brand strategy, the substantive implication is that "
                "being recognized by an AI is not the same as being "
                "retrieved by an AI. The two are decoupled enough across "
                "categories and language families that they need to be "
                "measured and managed as separate components of brand "
                "presence."
            ),
            (
                "For AIAS\u2122 1.0\u2019s headline cross-substrate "
                "generalization claim, this is the empirical ground the "
                "methodology layer required. The pattern is not specific to "
                "any one substrate, language, or cultural context."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Cultural-channel Recall is real, and concentrated in the celebrity-DTC tier.",
        "chart_slot": "f3_channel_asymmetry",
        "paragraphs": [
            (
                "Before v0.20, the v1.5 dissociation framework predicted "
                "three quadrants but only two had empirical cases. The Type "
                "2 quadrant \u2014 cultural-channel-preferred \u2014 was "
                "predicted but unpopulated across v0.17, v0.18, and v0.19. "
                "v0.20 produces three cases, all in Cell B (the predicted "
                "hunting cell): Glossier (R_cat = 0, R_cult = 9), Rhode "
                "(R_cat = 0, R_cult = 8), Augustinus Bader (R_cat = 2, "
                "R_cult = 7)."
            ),
            (
                "These are not Iwachu cases (which are about Recognition "
                "vs. canonical Recall); they are about the canonical Recall "
                "channel vs. the cultural-footprint Recall channel. LLMs "
                "treat \u201cwhat are the best skincare brands?\u201d and "
                "\u201cwhat skincare brands are popular right now?\u201d as "
                "questions returning different brand lists. The asymmetry "
                "is not a quirk of prompt wording \u2014 it is a property "
                "of how these brands are represented across the LLMs\u2019 "
                "training data corpora."
            ),
            (
                "For brand strategy, a brand\u2019s AI Availability has at "
                "least two components that can move independently. A brand "
                "can be culturally salient (heavy mentions in popular / "
                "celebrity / viral discourse) without being canonically "
                "available (sparse mentions in best / dermatologist-"
                "recommended / effective discourse), or vice versa. The "
                "two require different inputs to influence \u2014 cultural-"
                "channel Recall responds to discourse density, canonical-"
                "channel Recall responds to authority surfaces."
            ),
            (
                "The cell concentration of Type 2 cases in Cell B (the "
                "high-IL celebrity-DTC tier) is itself substantive: the "
                "cultural-channel pathway is most pronounced where Identity "
                "Load is highest. This is the IL moderator\u2019s "
                "substantive signature visible in the raw data, even where "
                "the four-leg joint verdict routes formally to NARROWED."
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
            "Cell B Type 2 count of 2 sits at the PARTIAL / EMERGED boundary. "
            "A third clean case (rather than Augustinus Bader at the R_cat = "
            "2 threshold ceiling) would have routed the primary hypothesis "
            "to EMERGED. The verdict is the strongest available given the "
            "pre-registered thresholds, but those thresholds were "
            "demanding \u2014 designed to require multiple, clean Type 2 "
            "cases rather than a single instance."
        ),
        (
            "Cell C\u2019s full Recognition saturation precludes within-cell "
            "rank-coherence analysis on the clinical tier. Spearman rank "
            "correlation is mathematically undefined when one input has zero "
            "variance. Future Cell C stratifications could surface within-"
            "cell C_P variance (separating icon-tier clinical brands from "
            "broader category members) and enable the analysis."
        ),
        (
            "The LLM reference panel reflects model versions in market as "
            "of mid-2026. Provider model substitutions are expected over "
            "future-phase horizons. v0.20\u2019s Type 2 cases should be "
            "interpreted as the pattern observed against the locked panel "
            "at acquisition time, not as a permanent property of the "
            "substrate."
        ),
        (
            "The cultural channel\u2019s specific frame wording (popular, "
            "celebrity, viral / cult-favorite) is calibrated to skincare\u2019s "
            "consumer-discovery surface. Different substrates require "
            "different cultural-channel lexicons \u2014 fragrance\u2019s "
            "perfumistas-native frames (v0.18), audiophile\u2019s audiophile-"
            "community frames (v0.19), skincare\u2019s celebrity-influencer "
            "frames (v0.20). A substrate-general specification of the "
            "cultural channel is a v1.6 candidate."
        ),
        (
            "Conglomerate-owned borderline brands behave per their consumer-"
            "identity classification, not their ownership tree. Fenty Skin "
            "(LVMH / Kendo) behaves as Cell B celebrity-DTC; Drunk Elephant "
            "(Shiseido) behaves as Cell B cult-clinical; The Ordinary "
            "(EL / Deciem) behaves as Cell C clinical; Rare Beauty\u2019s "
            "near-zero Recognition reflects its cosmetics-primary identity "
            "rather than its skincare-extension. The pre-registered "
            "borderline classifications hold up empirically."
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
            "<b>v0.21 candidate substrates.</b> The Type 2 PARTIAL verdict "
            "invites substrates with even higher Cell B Identity Load "
            "saturation. Candidate domains where the celebrity-DTC tier is "
            "more populous: cosmetics (where Rare Beauty would be a Cell B "
            "native rather than an unrecognized skincare-extension), "
            "wellness supplements, athletic footwear with founder-identity "
            "brands. Each would test whether Cell B Type 2 counts can clear "
            "the EMERGED threshold of 3."
        ),
        (
            "<b>Cell C stratification.</b> The v0.20 Cell C saturation "
            "finding suggests a v0.21+ design with finer Cell C "
            "stratification \u2014 separating icon-tier clinical (CeraVe, "
            "La Roche-Posay) from broader category members (Cetaphil, "
            "Eucerin). Within-cell C_P variance could be surfaced, enabling "
            "Phase D rank-coherence analysis on the clinical tier and "
            "potentially clearing v1.5 C2."
        ),
        (
            "<b>Protocol v1.6 candidate.</b> The IL-moderator verdict-vs-"
            "data tension suggests v1.6 should add a moderator-evaluation "
            "pathway independent of Regime 4\u2019s C2 conditions. A direct "
            "test of channel-mean asymmetry across cells (with bootstrap "
            "confidence intervals on the asymmetry estimate) would let the "
            "moderator hypothesis be evaluated on its own terms rather than "
            "as a downstream consequence of Regime 4\u2019s verdict."
        ),
        (
            "<b>AIAS\u2122 1.0 trajectory.</b> With v0.20\u2019s "
            "contributions in place, the AIAS\u2122 1.0 publication package "
            "spans four substrate families with multi-cell dissociation "
            "distribution, all three dissociation quadrants empirically "
            "populated, and the v1.5 C2 multi-statistic prospectively "
            "validated. Remaining work to lock the 1.0 release: a fifth-"
            "family substrate (one phase), a Protocol v1.6 increment for "
            "the moderator pathway, and a synthesis paper consolidating "
            "the four-family anchor base."
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
        "Four hypotheses were pre-registered at commit 4e5ab60 (tag "
        "v0.20-prereg-r1) on May 21, 2026, prior to any acquisition. "
        "Verdict matrices were locked ex-ante. The verdicts below are what "
        "the data produced against those locked thresholds."
    ),
    "rows": [
        (
            "H_Type2_emergence",
            "Cultural-channel Recall populates the Type 2 quadrant (R_cat \u2264 2 "
            "\u2227 R_cult \u2265 5) in Cell B at post-attrition n \u2265 5. "
            "EMERGED requires \u2265 3 Cell B cases; PARTIAL routes 1\u20132.",
            "Two Cell B cases at threshold: Glossier (R_cat = 0, R_cult = 9), "
            "Rhode (R_cat = 0, R_cult = 8); Augustinus Bader (R_cat = 2, "
            "R_cult = 7) at boundary.",
            "PARTIAL",
            "partial",
        ),
        (
            "H_Regime4_skincare",
            "Four-regime substantive test under v1.5: C1 (n \u2265 12) \u2192 "
            "C2 multi-statistic (distinct C_P \u2265 3 \u2227 modal \u2264 "
            "0.625, per cell) \u2192 IL-gradient guard \u2192 C3 per-cell "
            "\u03c1. FALSIFIED if C2 fails in \u2265 2 cells.",
            "C2 fails Cell A (distinct = 2, modal = 0.750) and Cell C (distinct "
            "= 1, modal = 1.000). Cell B passes (distinct = 3, modal = 0.625).",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H_Dissociation_substrate_generalization",
            "Iwachu-pattern cases (C_P \u2265 5 \u2227 R_cat \u2264 2) appear "
            "in \u2265 2 of 3 cells. GENERALIZED routes to all-3-cell "
            "distribution; PARTIAL routes single-cell concentration.",
            "11 Iwachu cases distributed across all three cells. Construct "
            "now anchored across four substrate families with multi-cell "
            "distribution in v0.20.",
            "GENERALIZED",
            "confirmed",
        ),
        (
            "H_IdentityLoad_moderator",
            "Four-leg joint over v0.16 \u00d7 v0.17 \u00d7 v0.18 \u00d7 v0.20. "
            "Joint matrix routes pessimistically when within-phase Regime 4 "
            "test falsifies (not on panel inadequacy).",
            "v0.20 Regime 4 FALSIFIED routes joint to NARROWED. Substantive "
            "channel asymmetry (Cell C R_cat-dominant, Cell B R_cult-dominant) "
            "tracks IL gradient regardless.",
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
        "each verdict for the construct, the moderator, and the v0.21+ "
        "trajectory is what the prose below addresses."
    ),
    "items": [
        (
            "H_Type2_emergence",
            "<b>What it means.</b> The construct\u2019s third dissociation "
            "quadrant is no longer theoretical. The cultural-channel Recall "
            "pathway exists, is measurable, and is concentrated in exactly "
            "the substrate tier the moderator hypothesis predicts (high-IL "
            "celebrity-DTC). For brands operating in that tier, AI "
            "Availability has a cultural-channel component that can be "
            "high while the canonical-channel component is zero. "
            "<b>What it doesn\u2019t mean.</b> PARTIAL is not EMERGED. The "
            "Type 2 quadrant is populated but not densely. Future substrates "
            "with stronger Identity Load saturation in the celebrity-DTC tier "
            "may produce higher Cell B Type 2 counts; v0.20 establishes the "
            "pattern exists but does not establish that it is the typical "
            "pattern."
        ),
        (
            "H_Regime4_skincare",
            "<b>What it means.</b> The methodological finding is the "
            "headline: v1.5 C2 was calibrated retrospectively against "
            "v0.18 + v0.19 data; v0.20 is the first prospective test. The "
            "rule behaves exactly as the methodology paper predicted "
            "across three different distributional shapes \u2014 accepting "
            "variance-rich cells, rejecting saturated cells, rejecting "
            "bimodal cells. The rule\u2019s prospective utility is "
            "established. <b>What it doesn\u2019t mean.</b> FALSIFIED is "
            "not a refutation of the underlying construct. The four-regime "
            "framework was tested in a substrate where Cell C is "
            "structurally saturated and Cell A is structurally bimodal. "
            "Future skincare phases with finer Cell C stratification could "
            "clear the C2 rule. The construct remains testable; v0.20 "
            "documents what the rule does when the substrate doesn\u2019t "
            "cooperate."
        ),
        (
            "H_Dissociation_substrate_generalization",
            "<b>What it means.</b> The multi-component Recognition \u00d7 "
            "Recall construct is now empirically anchored across four "
            "substrate families with multi-cell distribution in v0.20 "
            "specifically. For AIAS\u2122 1.0\u2019s headline cross-substrate "
            "generalization claim, this is the empirical ground the "
            "methodology layer required. The pattern is not specific to any "
            "one substrate, language, or cultural context. <b>What it "
            "doesn\u2019t mean.</b> GENERALIZED does not mean the "
            "dissociation pattern operates identically across all substrate "
            "families. The cell distribution of the pattern is substrate-"
            "specific \u2014 multi-cell in v0.18 and v0.20, weighted-"
            "concentration in v0.19, cross-cultural in v0.17. The pattern "
            "generalizes; its cell distribution does not."
        ),
        (
            "H_IdentityLoad_moderator",
            "<b>What it means.</b> The verdict-vs-data tension is "
            "interpretively informative. The joint matrix\u2019s NARROWED "
            "routing reflects pessimism \u2014 when the within-phase Regime "
            "4 test falsifies, the joint backs off. But the moderator\u2019s "
            "substantive signature is visible in the data and operates as "
            "the hypothesis predicts. Future v1.5+ refinements may benefit "
            "from a moderator-evaluation pathway evaluable independently of "
            "Regime 4\u2019s conditions. <b>What it doesn\u2019t mean.</b> "
            "NARROWED is not equivalent to FALSIFIED. The hypothesis is "
            "bounded, not refuted. Across four legs (PARTIAL, FALSIFIED-on-"
            "panel-inadequacy, PARTIAL, FALSIFIED), the moderator operates "
            "with substrate-specific qualifications. v0.20 supplies the "
            "strongest substantive evidence of IL-tracking channel "
            "asymmetry yet observed in the program."
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
        "v0.20 Phase A acquisition (Recognition C_P, n = 144 probes): "
        "osf.io/ec6wh/v20/data/phase_a_results.csv",
        "v0.20 Phase B acquisition (Recall two-channel, n = 36 queries): "
        "osf.io/ec6wh/v20/data/phase_b_results.csv",
        "v0.20 scoring verdicts (four hypothesis matrices resolved): "
        "osf.io/ec6wh/v20/data/v20_verdicts.json",
        "v0.20 brand registry (locked at pre-reg r1): "
        "osf.io/ec6wh/v20/prereg/v0_20_registry.json",
    ],
    "methodology_log": (
        "v0.20 pre-registration locked at commit 4e5ab60 (git tag "
        "v0.20-prereg-r1, branch v0.20-skincare-il-gradient). First "
        "prospective phase under Protocol v1.5 (SSRN 6810758). Acquisition "
        "locked at git tag v0.20-acquisition-locked. Academic companion: "
        "SSRN 6811441"
    ),
}
