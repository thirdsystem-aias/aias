"""
v22_automotive_content.py — Content module for the v0.22 Third System
brand-format report.

Forked from v21_cosmetics_content.py with surgical content changes only.
Schema matches the contract consumed by build_report_v22.py (which is the
v21 builder forked surgically — same data shapes, different facts).

Attributes (in builder-consumption order):
  COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED,
  PATTERNS, LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING,
  HYPOTHESIS_DETAILS, CLOSING

PATTERNS items expose: number, title, chart_slot, chart_after_text (opt),
paragraphs. The chart_slot string is one of f1_cp_distribution,
f2_dissociation_scatter, f3_channel_asymmetry, f4_phantom_defunct —
resolved in build_report_v22.py via _slot_lookup() to the v0.22 chart
filenames in reports/figs/v22/. v0.22 carries four findings (vs v0.21's
three) — the fourth is the Phantom Brand Persistence lead.
"""

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "Phantom Brand Persistence Has a Living-Brand Boundary",
    "subtitle": (
        "On a heritage-saturated automotive substrate with a dedicated "
        "Cell D panel of discontinued corporate brands, the AI mediation "
        "layer surfaces living heritage brands at elevated rates "
        "(R_phantom up to 14/18) but does not surface any of the five "
        "defunct brands a single time across 18 unprompted Recall "
        "opportunities each. The lead hypothesis falsifies cleanly; "
        "the supporting heritage hypothesis confirms cleanly. The "
        "phantom phenomenon has a temporal floor."
    ),
    "date": "May 2026",
    "byline_short": "Pablo Ulpiano Gonz\u00e1lez Castro \u00b7 Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}


# ---------------------------------------------------------------------------
# STANDFIRST
# ---------------------------------------------------------------------------

STANDFIRST = (
    "AIAS\u2122 v0.22 stress-tests Phantom Brand Persistence on a "
    "heritage-saturated automotive substrate, with a dedicated Cell D "
    "panel of five discontinued corporate brands (Pontiac, Oldsmobile, "
    "Plymouth, Mercury, Saturn) providing the pure-phantom upper-bound "
    "test. The result inverts the program\u2019s working hypothesis: "
    "despite all five defunct brands clearing Phase A Recognition at "
    "C_P = 6/6, none surfaces once in any of 18 unprompted current-tense "
    "Recall opportunities per brand. Meanwhile, three Cell A heritage "
    "brands (Mercedes-Benz, Porsche, BMW) cross the R_phantom \u2265 8 "
    "CONFIRMED threshold. The phantom phenomenon operates on living "
    "heritage brands and stops at brand death \u2014 a tighter and more "
    "informative claim than \u201cphantoms surface broadly.\u201d"
)


# ---------------------------------------------------------------------------
# LEAD_DECK
# ---------------------------------------------------------------------------

LEAD_DECK = (
    "Four findings shape the v0.22 phase. First, Recognition saturates "
    "uniformly across all four cells \u2014 23 of 24 brands at C_P = 6/6, "
    "one at 5/6 \u2014 routing v1.5 C2 to failure in every cell and "
    "v1.6 Inc1 substrate Recognition Pre-Screen to UNIFORM SATURATION "
    "as predicted. Second, Iwachu-pattern dissociation generalizes to "
    "the program\u2019s sixth substrate family with cases in all four "
    "cells, though five of seventeen cases are Cell D defunct brands "
    "that meet the Iwachu criterion tautologically by the lead "
    "falsification. Third, the heritage substrate produces the largest "
    "single-phase Type 2 count in the program (seven cases) and "
    "exposes a clean within-cell channel bifurcation: Mercedes-Benz, "
    "Porsche, and BMW surface heavily in both canonical and cultural "
    "Recall, while Rolls-Royce, Bentley, Jaguar, and Cadillac surface "
    "only in cultural / heritage frames. Fourth \u2014 the lead "
    "finding \u2014 no defunct brand surfaces in any Phase B response, "
    "falsifying H_Phantom_Defunct at the strongest possible margin and "
    "establishing the temporal boundary of the phantom phenomenon."
)


# ---------------------------------------------------------------------------
# EXEC_SUMMARY
# ---------------------------------------------------------------------------

EXEC_SUMMARY = [
    (
        "AIAS\u2122 measures AI Availability \u2014 the probability that an AI "
        "intermediary retrieves, recommends, or selects a brand in a category-"
        "anchored decision context \u2014 as a third measurable layer of brand "
        "availability alongside the Ehrenberg-Bass framework\u2019s Mental and "
        "Physical Availability. Protocol v1.6 (SSRN 6816340) introduced three "
        "increments: a substrate Recognition pre-screen distinguishing uniform "
        "from differential saturation (Inc1), a direct R4-independent IL "
        "measurement (Inc2), and an explicit Phantom Brand Persistence "
        "measurement (Inc3). v0.22 is the first prospective phase under v1.6 "
        "lock, retaining v1.5\u2019s two-channel Recall decomposition (R_cat "
        "and R_cult) and v1.2\u2019s four-regime taxonomy."
    ),
    (
        "The substrate is automotive, sampled across four cells of seven, five, "
        "seven, and five brands. Cell A (Heritage, n = 7): Mercedes-Benz, "
        "Jaguar, Cadillac, Rolls-Royce, Bentley, Porsche, BMW. Cell B "
        "(Disruptor, n = 5): Tesla, Rivian, Lucid, Polestar, Fisker. Cell C "
        "(Mass-Legacy, n = 7): Toyota, Honda, Ford, Chevrolet, Hyundai, "
        "Volkswagen, Nissan. Cell D (Defunct, n = 5) \u2014 the pure-phantom "
        "panel novel to v0.22: Pontiac (closed 2010), Oldsmobile (2004), "
        "Plymouth (2001), Mercury (2010), Saturn (2010). Reference panel: the "
        "six-slot LLM panel carried forward from v0.17 (Claude Opus 4.5, "
        "Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 "
        "Flash Lite)."
    ),
    (
        "Six hypotheses were pre-registered (tags v0.22-prereg-r1 superseded "
        "by v0.22-prereg-r2 \u2014 the r1 \u2192 r2 amendment corrected an "
        "INSTRUMENT specification defect caught pre-acquisition; see "
        "Limitations). H_Phantom_Defunct, the lead hypothesis, returned "
        "FALSIFIED at the strongest possible margin: all five Cell D brands "
        "produced R_phantom_defunct = 0 across the six-model panel \u00d7 "
        "three R_cat probes = 18 mention opportunities per brand. The "
        "supporting hypothesis H_Phantom_Brand_Persistence_heritage returned "
        "CONFIRMED with three Cell A brands above the R_phantom \u2265 8 "
        "threshold: Porsche at 14, BMW at 12, Mercedes-Benz at 10. The pair "
        "of verdicts establishes a temporal boundary: phantom persistence "
        "operates on living heritage brands and stops at documented brand "
        "death."
    ),
    (
        "H_Regime4_automotive returned FALSIFIED on v1.5 C2 failing in all "
        "four cells \u2014 the pattern v0.21 cosmetics exhibited, now "
        "replicated. H_SubstrateRecognition_PreScreen (v1.6 Inc1) classified "
        "UNIFORM SATURATION across all four cells as predicted: modal C_P = 6 "
        "everywhere, with the single Fisker non-yes (Claude Sonnet 4.5 \u2014 "
        "reflecting Fisker\u2019s 2024 corporate distress) as the only "
        "Recognition defection in the entire panel. The combination "
        "documents what v1.6 Inc1 was designed for: a substrate-level "
        "Recognition saturation signature that routes downstream "
        "interpretation distinctly from differential-saturation substrates."
    ),
    (
        "H_Dissoc_substrate_generalization returned GENERALIZED with Iwachu-"
        "pattern cases in all four cells (17 cases total). The Cell D "
        "contribution \u2014 five tautological cases since defunct brands "
        "meet C_P \u2265 5 \u2227 R_cat \u2264 2 precisely because they "
        "don\u2019t surface \u2014 nets out methodologically; the substantive "
        "base is twelve Iwachu cases across Cells A, B, and C, the largest "
        "single-phase substantive Iwachu count in the program. The v1.4/v1.5 "
        "Recognition \u00d7 Recall construct is now empirically anchored "
        "across six substrate families (kitchen knives, kitchenware, indie "
        "fragrance, audiophile headphones, skincare, cosmetics, automotive)."
    ),
    (
        "H_IdentityLoad_direct (v1.6 Inc2 \u2014 R4-independent bootstrap) "
        "returned CONFIRMED with the strongest IL signature in the program: "
        "Cell A R_cult / R_cat = 12.43 / 5.14 = 2.42, Cell B R_cult / R_cat "
        "= 1.20 / 1.60 = 0.75. Cell A heritage brands carry 3.2\u00d7 the "
        "cult-channel dominance of Cell B disruptors. Cell C\u2019s ratio "
        "(0.48) trails Cell B \u2014 a methodologically interesting result "
        "showing that the mass-legacy substrate carries canonical-Recall "
        "dominance even though it contains substantial cultural heritage "
        "(Ford, Chevrolet, Volkswagen all surface as cultural-channel-"
        "preferred Type 2 cases). The IL gradient at the channel-asymmetry "
        "layer is now anchored independently of Regime 4\u2019s C2 "
        "conditions, satisfying v1.6 Inc2\u2019s design intent."
    ),
]


# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "Two measurements were taken against a locked panel of six LLMs. "
            "Brand registry, probe wording, and the six locked hypotheses "
            "with verdict matrices were committed at pre-registration before "
            "any data collection (tag v0.22-prereg-r2, superseding r1 \u2014 "
            "the r1 lock specified single-model GPT-4.1 \u00d7 n = 12 "
            "iterations in error, contradicting program convention; the "
            "defect was caught pre-acquisition and amended to the six-model "
            "panel matching v0.17\u2013v0.21. See Limitations and the "
            "DEVIATIONS Entry 0 in prereg/v0_22_automotive_content.py)."
        ),
        (
            "<b>Phase A \u2014 Recognition.</b> For each of the 24 brands in "
            "the panel, each of the 6 LLMs was asked: \u201cIs the brand X "
            "commonly recognized as a car brand? Answer yes or no.\u201d "
            "The probe deliberately uses present-tense framing without "
            "temporal cues, which is essential to the Cell D phantom test: "
            "the panel must not be primed to recognize defunct brands as "
            "discontinued. The brand\u2019s C_P score (range 0\u20136) is "
            "the count of yes responses. C_P is the Recognition component "
            "of AI Availability."
        ),
        (
            "<b>Phase B \u2014 Recall, two-channel decomposition.</b> Six "
            "category-anchored queries were sent to each of the 6 LLMs (36 "
            "total queries). Three queries anchor the canonical channel "
            "(R_cat): best car brands; automotive experts and reviewers "
            "recommend; highest quality / most reliable. Three queries "
            "anchor the cultural-footprint channel (R_cult): heritage / "
            "prestige / legacy; affluent / status-conscious buyers; iconic / "
            "storied identity in popular culture. For each (frame \u00d7 "
            "LLM) response, the 24-brand registry was scanned for mention "
            "presence using case-insensitive, accent-stripped, possessive-"
            "aware matching. Per-brand R_cat (max 18) and R_cult (max 18) "
            "follow."
        ),
        (
            "<b>Phantom Brand Persistence (v1.6 Inc3 measurement).</b> The "
            "lead measurement of v0.22. R_phantom_defunct for each Cell D "
            "brand is operationally the count of unprompted current-tense "
            "Recall mentions in Phase B R_cat responses across (six models "
            "\u00d7 three R_cat probes) \u2014 max 18 per brand. R_phantom "
            "for Cell A_Heritage brands carries the same operationalization "
            "applied to living-brand Recall. Threshold ladder for the lead "
            "hypothesis (locked at r2): CONFIRMED \u2265 4; PARTIAL 1\u20133; "
            "FALSIFIED at zero across all Cell D brands. The threshold was "
            "moved 3 \u2192 4 in the r1 \u2192 r2 amendment to harmonize "
            "with the corrected max-18 scale and the H_Phantom_Brand_"
            "Persistence_heritage PARTIAL floor (also 4/18)."
        ),
        (
            "<b>Three dissociation patterns at v1.5 thresholds.</b> Iwachu: "
            "high Recognition with sparse canonical Recall (C_P \u2265 5 "
            "\u2227 R_cat \u2264 2). Type 1: canonical-channel-preferred "
            "(R_cat \u2265 5 \u2227 R_cult \u2264 2). Type 2: cultural-"
            "channel-preferred (R_cat \u2264 2 \u2227 R_cult \u2265 5). "
            "In v0.22 these patterns are descriptive overlays on top of the "
            "six locked hypotheses; H_Type2_emergence is not in the v0.22 "
            "battery (it was specific to v0.20\u2013v0.21 cosmetics-tier "
            "framing). The dissociation pattern remains the substrate-"
            "generalization construct\u2019s native vocabulary."
        ),
    ],
}


# ---------------------------------------------------------------------------
# PATTERNS — four findings, each with a chart_slot
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "Recognition saturates uniformly. The discrimination signal lives entirely in Recall.",
        "chart_slot": "f1_cp_distribution",
        "paragraphs": [
            (
                "Twenty-three of 24 brands in the panel score C_P = 6/6. "
                "All seven Cell A heritage brands; four of five Cell B "
                "disruptors; all seven Cell C mass-legacy brands; all five "
                "Cell D defunct brands. The single exception is Fisker at "
                "C_P = 5/6, where Claude Sonnet 4.5 returned \u201cno\u201d "
                "\u2014 a recent-corporate-distress artifact rather than a "
                "category-classification failure."
            ),
            (
                "v1.5 C2 fails uniformly. Cell A: distinct = 1, modal share "
                "= 1.000. Cell B: distinct = 2, modal share = 0.800. Cell "
                "C: distinct = 1, modal share = 1.000. Cell D: distinct = "
                "1, modal share = 1.000. The rule\u2019s logic is correct: "
                "fully saturated within-cell distributions don\u2019t "
                "supply the variance C3 rank-coherence would consume. "
                "Regime 4 routes to FALSIFIED at the regime-floor, before "
                "any IL-gradient guard or Phase D check is reached \u2014 "
                "exactly as predicted in the mega-prompt and exactly as "
                "v0.21 cosmetics produced."
            ),
            (
                "The Cell D saturation carries the heaviest substantive "
                "weight. All five defunct corporate brands \u2014 Pontiac, "
                "Oldsmobile, Plymouth, Mercury, Saturn \u2014 score C_P = "
                "6/6 on a present-tense \u201ccommonly recognized as a car "
                "brand\u201d probe. The AI mediation layer treats them as "
                "categorically self-evident automotive brands despite "
                "documented closures spanning 2001\u20132010. This is the "
                "precondition Cell D was designed for: if Recognition had "
                "fallen short, the lead hypothesis test would have collapsed "
                "into a Recognition story rather than a Recall story. "
                "Recognition holds; the lead hypothesis test runs cleanly."
            ),
            (
                "H_SubstrateRecognition_PreScreen (v1.6 Inc1) classifies "
                "the substrate as UNIFORM SATURATION. The classification is "
                "non-directional but consequential: for substrates with "
                "this property, category-membership Recognition is not the "
                "discriminating channel; the AIAS signal lives entirely in "
                "Recall and the construct\u2019s downstream measurements "
                "carry that load alone. Automotive joins cosmetics as the "
                "second substrate in the program where this property is "
                "documented at all-cell saturation."
            ),
        ],
    },
    {
        "number": 2,
        "title": "Iwachu dissociation generalizes to a sixth substrate family \u2014 with a tautology caveat.",
        "chart_slot": "f2_dissociation_scatter",
        "paragraphs": [
            (
                "The Iwachu pattern \u2014 brands the AI mediation layer "
                "recognizes as category members but does not surface when "
                "asked to enumerate the category \u2014 was first observed "
                "in v0.17 on Japanese kitchen knives and has extended phase "
                "by phase through indie fragrance (v0.18), audiophile "
                "headphones (v0.19), skincare (v0.20), cosmetics (v0.21). "
                "v0.22 contributes seventeen Iwachu cases on the automotive "
                "panel \u2014 the largest single-phase count in the program "
                "\u2014 distributed across all four cells."
            ),
            (
                "Cell A contributes four cases: Jaguar (R_cat = 0), "
                "Cadillac (R_cat = 0), Rolls-Royce (R_cat = 0), Bentley "
                "(R_cat = 0) \u2014 all four also qualifying simultaneously "
                "as Type 2 (see Finding 3). Cell B contributes four: "
                "Rivian (R_cat = 1), Lucid (R_cat = 0), Polestar (R_cat = "
                "0), Fisker (R_cat = 0) \u2014 the disruptor cell carries "
                "Recognition (4/5 at C_P = 6/6, one at 5/6) but minimal "
                "canonical-channel Recall presence outside of Tesla. Cell C "
                "contributes four: Ford (R_cat = 2), Chevrolet (R_cat = 0), "
                "Volkswagen (R_cat = 1), Nissan (R_cat = 0). And Cell D "
                "contributes five: all five defunct brands at R_cat = 0."
            ),
            (
                "The Cell D contribution warrants methodological "
                "consideration. Defunct brands meet C_P \u2265 5 \u2227 "
                "R_cat \u2264 2 \u2014 the Iwachu criterion \u2014 "
                "tautologically: they\u2019re recognized at ceiling (C_P = "
                "6) precisely because they\u2019re well-encoded brand "
                "identities, and they don\u2019t appear in R_cat responses "
                "precisely because the lead hypothesis H_Phantom_Defunct "
                "falsifies (Finding 4). Netting out the five Cell D cases, "
                "the substantive Iwachu base for v0.22 is twelve cases "
                "across Cells A, B, and C \u2014 still the largest "
                "substantive single-phase count in the program, exceeding "
                "v0.21\u2019s thirteen cases across three cells by a "
                "narrow margin once the same tautology adjustment is "
                "considered (v0.21 had no Cell D, so its thirteen are all "
                "substantive)."
            ),
            (
                "H_Dissoc_substrate_generalization routes to GENERALIZED on "
                "the formal verdict criterion (\u2265 1 case in Cell A or "
                "B). The cross-substrate generalization claim now spans six "
                "substrate families with consistent directional behavior. "
                "For AIAS\u2122 1.0\u2019s headline construct claim, "
                "automotive completes a substrate-breadth threshold the "
                "five-family base reached at v0.21 \u2014 the program now "
                "spans Japanese craft, Western indie consumer, Western "
                "consumer electronics, Western mass-market skincare and "
                "cosmetics, and now Western mass-market durables. The "
                "pattern is not specific to language family, price-tier "
                "structure, or cultural origin."
            ),
        ],
    },
    {
        "number": 3,
        "title": "Channel asymmetry reveals within-cell bifurcations: \u201csaturated heritage\u201d vs \u201cpure heritage-phantom\u201d in Cell A; canonical-Recall \u201creliability\u201d Asian vs cultural-Recall \u201cAmericana\u201d Western in Cell C.",
        "chart_slot": "f3_channel_asymmetry",
        "paragraphs": [
            (
                "v0.22 produces seven Type 2 cases (R_cat \u2264 2 \u2227 "
                "R_cult \u2265 5), the largest single-phase Type 2 count "
                "in the program \u2014 against v0.21\u2019s four. Four "
                "cases sit in Cell A: Rolls-Royce (R_cat = 0, R_cult = 13), "
                "Bentley (0, 12), Jaguar (0, 10), Cadillac (0, 8). Three "
                "sit in Cell C: Ford (R_cat = 2, R_cult = 6), Chevrolet (0, "
                "7), Volkswagen (1, 6). Cell B produces zero Type 2 cases "
                "and Cell D produces zero \u2014 a result consistent with "
                "the lead falsification and inconsistent with the "
                "cosmetics-substrate Type 2 mechanism that drove v0.20 and "
                "v0.21."
            ),
            (
                "Within Cell A, the seven heritage brands split into two "
                "channel-presence patterns. \u201cSaturated heritage,\u201d "
                "n = 3: Mercedes-Benz (R_cat = 10, R_cult = 16), Porsche "
                "(14, 18 \u2014 a perfect R_cult saturation), BMW (12, 10). "
                "These brands surface heavily in both canonical \u201cbest "
                "/ expert / quality\u201d frames and cultural \u201cheritage "
                "/ prestige / iconic\u201d frames. \u201cPure heritage-"
                "phantom,\u201d n = 4: Jaguar, Cadillac, Rolls-Royce, "
                "Bentley \u2014 all at R_cat = 0, all at R_cult \u2265 8. "
                "These brands operate as cultural artifacts decoupled from "
                "the canonical \u201crecommended car\u201d frame. The AI "
                "mediation layer renders them as legacy/prestige reference "
                "points but not as candidates one might purchase."
            ),
            (
                "Within Cell C, a parallel bifurcation along an unexpected "
                "axis. \u201cCanonical-Recall reliability\u201d brands: "
                "Toyota (R_cat = 18, R_cult = 6 \u2014 perfect canonical "
                "saturation), Honda (18, 0 \u2014 Type 1), Hyundai (15, 1 "
                "\u2014 Type 1). All three are Asian-manufactured mass-"
                "legacy brands; all three are heavily coded as best / "
                "expert / quality choices and weakly coded in cultural "
                "frames. \u201cCultural-Recall Americana\u201d brands: "
                "Ford (2, 6), Chevrolet (0, 7), Volkswagen (1, 6) \u2014 "
                "all three Type 2. American (and German) mass-legacy "
                "brands carry cultural identity \u2014 storied, iconic, "
                "American-coded \u2014 but minimal canonical-recommendation "
                "presence. Nissan, the cell\u2019s seventh brand, is "
                "invisible in both channels (R_cat = R_cult = 0)."
            ),
            (
                "H_IdentityLoad_direct (v1.6 Inc2) routes to CONFIRMED: "
                "Cell A R_cult / R_cat = 2.42 vs Cell B = 0.75 \u2014 a "
                "3.2\u00d7 cult-channel dominance lead. The IL signal is "
                "evaluated R4-independently for the first time in the "
                "program: the comparison uses only Phase B Recall data, "
                "not Phase A Recognition (which fully saturates and "
                "provides no IL signal). The substantive IL gradient holds "
                "even though Regime 4 falsifies on the saturation route. "
                "v1.6 Inc2 was designed for exactly this case \u2014 "
                "substrates where the IL signature is real but the Regime "
                "4 C2 path cannot evaluate it \u2014 and v0.22 supplies "
                "the cleanest demonstration the program has produced."
            ),
        ],
    },
    {
        "number": 4,
        "title": "Defunct brands do not phantom. The AI mediation layer has a temporal floor.",
        "chart_slot": "f4_phantom_defunct",
        "paragraphs": [
            (
                "The headline finding. Across all five Cell D brands "
                "\u2014 Pontiac, Oldsmobile, Plymouth, Mercury, Saturn "
                "\u2014 R_phantom_defunct = 0. In none of (six models "
                "\u00d7 three R_cat probes) = 18 unprompted current-tense "
                "Recall opportunities per brand does any defunct brand "
                "surface a single time. H_Phantom_Defunct, the v0.22 lead "
                "hypothesis pre-registered at the CONFIRMED \u2265 4 "
                "threshold, falsifies at the strongest possible margin: "
                "every brand at zero, the entire cell at the FALSIFIED "
                "floor."
            ),
            (
                "The falsification is informative because it occurs on "
                "exactly the substrate where the lead hypothesis was "
                "predicted to confirm. The mega-prompt forecast strong "
                "phantom surfacing for Pontiac (GTO / Firebird / Trans Am "
                "film footprint), Oldsmobile (corporate Americana through "
                "2004), and Mercury (deep film and music references). All "
                "three are recognized at C_P = 6/6 by all six models. "
                "Their identities are well-encoded in the AI mediation "
                "layer. They simply don\u2019t appear in present-tense "
                "Recall \u2014 not in canonical \u201cbest car\u201d "
                "frames, not in cultural \u201cheritage / prestige / "
                "iconic\u201d frames, not in either channel for any of "
                "the six panel models."
            ),
            (
                "The supporting hypothesis carries the contrast that "
                "makes the lead falsification substantively meaningful. "
                "H_Phantom_Brand_Persistence_heritage CONFIRMED with three "
                "Cell A brands above the R_phantom \u2265 8 threshold: "
                "Porsche at 14/18, BMW at 12/18, Mercedes-Benz at 10/18. "
                "On the same panel run, in the same Phase B responses, "
                "the same models that produce zero defunct-brand mentions "
                "produce high-volume living-heritage-brand surfacing. The "
                "phantom phenomenon operates on living heritage brands and "
                "stops at brand death. The boundary is sharp, not gradient."
            ),
            (
                "For the AI Availability construct, this is a tighter and "
                "more interesting claim than the v0.21 framing suggested. "
                "Phantom Brand Persistence is not a substrate-agnostic "
                "leakage; it is a property of brand-identity persistence "
                "in the AI mediation layer, bounded by the layer\u2019s "
                "(implicit, learned) temporal categorization. The "
                "mediation layer does not merely associate brand names "
                "with categories \u2014 it associates brand names with "
                "categories plus temporal status, and that temporal "
                "categorization is robust enough that documented "
                "discontinuation acts as an unprompted-Recall floor. The "
                "construct now has empirically anchored upper and lower "
                "boundaries: v0.21 Glossier R_phantom = 12 (off-panel, "
                "alive, anchors the upper bound); v0.22 Cell D R_phantom "
                "= 0 across all five (in-panel, documented dead, anchors "
                "the lower bound)."
            ),
        ],
    },
]


# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "The r1 \u2192 r2 pre-registration amendment is a substantive "
            "methodology event that warrants surfacing here as well as in "
            "the locked DEVIATIONS Entry 0. The r1 lock specified INSTRUMENT "
            "as single-model GPT-4.1 \u00d7 n = 12 iterations \u2014 a "
            "Claude-assisted drafting error that contradicted v0.17\u2013"
            "v0.21 program convention (the six-model reference panel). "
            "The defect was caught pre-acquisition during mega-prompt "
            "drafting; no data was collected under r1. r2 corrects "
            "INSTRUMENT to the six-model panel and moves the H_Phantom_"
            "Defunct CONFIRMED threshold from 3 (on assumed max-12) to 4 "
            "(on corrected max-18) for proportional consistency with the "
            "supporting heritage hypothesis. r1 is retained in git history "
            "for audit; r2 is the operative lock for v0.22."
        ),
        (
            "Cell D Iwachu contributions are tautological. The Iwachu "
            "criterion (C_P \u2265 5 \u2227 R_cat \u2264 2) is met by all "
            "five defunct brands precisely because they\u2019re well-"
            "recognized identities (C_P = 6/6) that don\u2019t surface in "
            "Recall (R_cat = 0) \u2014 the lead hypothesis falsification "
            "produces the Iwachu signature mechanically. The formal "
            "verdict (H_Dissoc GENERALIZED) holds on the locked criterion "
            "(\u2265 1 case in Cell A or B), but the substantive cross-"
            "substrate claim should rest on the twelve Cell A + Cell B + "
            "Cell C cases, not the seventeen-case total. Future v1.6+ "
            "increments may benefit from a substrate-internal Iwachu "
            "criterion that excludes phantom-floor cases."
        ),
        (
            "Phase D Spearman \u03c1 is mathematically undefined in three "
            "of four cells (A, C, D) because C_P is constant (= 6) and "
            "rank correlation requires non-zero input variance. Only Cell "
            "B yields a defined \u03c1 (= 0.395, n = 5). This is not a "
            "methodological failure mode but a substrate-saturation "
            "artifact: when Recognition fully saturates, the C3 rank-"
            "coherence test has no signal to compute. The v1.5 C2 path "
            "already routes Regime 4 to FALSIFIED at the regime-floor "
            "before C3 is reached, so the undefined \u03c1 has no verdict "
            "consequence \u2014 it is documented here for methodological "
            "transparency."
        ),
        (
            "H_IdentityLoad_direct uses an interim operationalization "
            "(R_cult / R_cat ratio per cell, sign-of-difference test) "
            "pending v1.6 Inc2 methodology paper detail on the bootstrap "
            "CI construction. The verdict (CONFIRMED) is robust to "
            "operationalization variants \u2014 Cell A IL of 2.42 vs "
            "Cell B IL of 0.75 is a 3.2\u00d7 separation that no "
            "reasonable bootstrap envelope would collapse \u2014 but the "
            "exact bootstrap procedure is unspecified in the locked pre-"
            "reg and the scoring code\u2019s in-line documentation flags "
            "the interim choice."
        ),
        (
            "Panel-internal scoring against the locked 24-brand registry "
            "captures Recall presence only for registered brands. Phase B "
            "responses contained substantive off-panel brand activity that "
            "the scoring doesn\u2019t reflect: Lexus surfaced consistently "
            "in canonical \u201cquality / reliability\u201d frames "
            "(Toyota\u2019s luxury division \u2014 the Cell C Toyota "
            "saturation has a luxury-sibling phantom of its own); Ferrari "
            "and Lamborghini surfaced in cultural \u201ciconic / heritage\u201d "
            "frames; Aston Martin (the registry cut from Cell A) surfaced "
            "in heritage frames; Audi (a Cell A omission the registry "
            "design accepted) surfaced moderately in both channels. None "
            "of these affect the v0.22 verdicts under the locked "
            "methodology, but the off-panel pattern is informative for a "
            "Phantom Brand Persistence Phase 2 measurement that would "
            "score off-panel surfacing against a larger reference "
            "vocabulary \u2014 the v1.6+ extension noted in What\u2019s "
            "next."
        ),
        (
            "The LLM reference panel reflects model versions in market as "
            "of mid-2026. Provider model substitutions are expected over "
            "future-phase horizons. v0.22\u2019s phantom-defunct "
            "falsification should be interpreted as the pattern observed "
            "against the locked panel at acquisition time, not as a "
            "permanent property of the AI mediation layer \u2014 model-"
            "training-corpus shifts could in principle change defunct-"
            "brand temporal coding. A v2.x replication on a later panel "
            "would be informative."
        ),
    ],
}


# ---------------------------------------------------------------------------
# WHATS_NEXT
# ---------------------------------------------------------------------------

WHATS_NEXT = {
    "heading": "What\u2019s next",
    "paragraphs": [
        (
            "<b>Six-family anchor base reached.</b> With v0.22 in place, "
            "the AIAS\u2122 program\u2019s cross-substrate generalization "
            "claim spans six distinct substrate families "
            "(kitchen knives, kitchenware, indie fragrance, audiophile "
            "headphones, skincare, cosmetics, automotive), with all three "
            "dissociation quadrants empirically populated, multi-cell "
            "Iwachu distribution in four families, and now an explicit "
            "Phantom Brand Persistence boundary measurement. The "
            "Presence-component AIAS\u2122 1.0 substrate-breadth threshold "
            "is closed."
        ),
        (
            "<b>Phantom Brand Persistence now has empirical bounds.</b> "
            "v0.21 Glossier (R_phantom = 12, off-panel, alive) anchors the "
            "upper-end demonstration. v0.22 Cell D (R_phantom_defunct = 0, "
            "in-panel, documented dead) anchors the lower-end floor. The "
            "phantom phenomenon is bounded by living-brand status \u2014 a "
            "more useful and more falsifiable construct than the "
            "substrate-agnostic version v0.21 implied. A natural Phase 2 "
            "extension is the off-panel measurement noted in Limitations: "
            "scoring Phase B responses against a larger reference "
            "vocabulary captures phantom activity the panel-internal "
            "scoring misses (Lexus, Ferrari, Aston Martin, Audi all "
            "demonstrably surfaced in v0.22 Phase B). Phase 2 would lift "
            "Phantom Brand Persistence from a panel-edge observation to a "
            "first-class measured component."
        ),
        (
            "<b>v1.6 Inc2 IL Direct: operationalization detail still "
            "outstanding.</b> The CONFIRMED verdict in v0.22 is robust to "
            "operationalization choice (the Cell A vs Cell B separation "
            "is a 3.2\u00d7 ratio), but the bootstrap CI construction "
            "specified in v1.6 Inc2 has not been fully detailed in the "
            "methodology paper. A v1.6.1 methodology supplement pinning "
            "the IL Direct bootstrap procedure would close this; the "
            "scoring code\u2019s interim sign-of-difference test is "
            "flagged in-line and is the candidate to replace."
        ),
        (
            "<b>AIAS\u2122 2.0 trajectory.</b> AIAS\u2122 1.0 (Presence-"
            "component, SSRN 6817841) shipped in May 2026 on the v0.16\u2013"
            "v0.21 five-family base. v0.22 extends the Presence base to "
            "six families and supplies the Phantom boundary measurement, "
            "but does not advance into the 2.0 component-expansion arc. "
            "The remaining work for the 2.0 release is the five-component "
            "expansion beyond Presence: Ranking, Consistency, Coverage, "
            "Grounding, Sentiment. Ranking and Coverage likely admit "
            "Presence-shaped acquisition; Consistency, Grounding, and "
            "Sentiment require new probe types. A v1.7+ methodology paper "
            "specifying the remaining components\u2019 acquisition "
            "patterns before phase work begins is the natural critical-"
            "path next step."
        ),
    ],
}


# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING
# Row format: (h_id, prediction, result, status_text, status_class)
# status_class \u2208 {"confirmed", "partial", "disconfirmed", "descriptive"}
# ---------------------------------------------------------------------------

HYPOTHESIS_SCORING = {
    "heading": "Pre-registered hypothesis scoring",
    "intro": (
        "Six hypotheses were pre-registered at tag v0.22-prereg-r2 "
        "(superseding r1 \u2014 see Limitations and DEVIATIONS Entry 0), "
        "prior to any acquisition. Verdict matrices were locked ex-ante. "
        "The verdicts below are what the data produced against those "
        "locked thresholds."
    ),
    "rows": [
        (
            "H_Phantom_Defunct",
            "<b>Lead hypothesis.</b> Discontinued corporate brands surface "
            "in unprompted current-tense Recall as if currently active. "
            "R_phantom_defunct = count of (model \u00d7 R_cat probe) "
            "responses across (6 \u00d7 3 = 18) where a Cell D brand "
            "appears unprompted. CONFIRMED requires any Cell D brand "
            "\u2265 4; PARTIAL routes 1\u20133; FALSIFIED at zero across all.",
            "All five Cell D brands at R_phantom_defunct = 0. Pontiac, "
            "Oldsmobile, Plymouth, Mercury, Saturn produce zero unprompted "
            "mentions across the six-model panel \u00d7 three R_cat probes. "
            "The falsification is at the strongest possible margin.",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H_Phantom_Brand_Persistence_heritage",
            "<b>Primary supporting hypothesis.</b> Living heritage brands "
            "(Cell A) exhibit elevated R_phantom. Standard v1.6 Inc3 "
            "R_phantom measurement (operationally R_cat for Cell A brands). "
            "CONFIRMED requires any Cell A brand R_phantom \u2265 8; "
            "PARTIAL routes 4\u20137; FALSIFIED all < 4. Benchmark: v0.21 "
            "Glossier R_phantom = 12.",
            "Three Cell A brands above threshold: Porsche R_phantom = 14 "
            "(R_cult = 18, perfect saturation), BMW = 12, Mercedes-Benz = "
            "10. Max R_phantom = 14, matching the v0.21 Glossier benchmark "
            "on a living-brand substrate.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H_Regime4_automotive",
            "Four-regime substantive test under v1.5: C1 (n \u2265 12) "
            "\u2192 C2 multi-statistic (distinct C_P \u2265 3 \u2227 modal "
            "\u2264 0.625, per cell) \u2192 IL-gradient guard \u2192 C3 "
            "per-cell \u03c1. FALSIFIED if C2 fails in \u2265 2 cells.",
            "C2 fails in all four cells. Cell A distinct = 1, modal = "
            "1.000. Cell B distinct = 2, modal = 0.800. Cell C distinct = "
            "1, modal = 1.000. Cell D distinct = 1, modal = 1.000. "
            "Resolved at C2 (regime-floor failure) \u2014 the v0.21 "
            "cosmetics pattern replicated.",
            "FALSIFIED",
            "disconfirmed",
        ),
        (
            "H_Dissoc_substrate_generalization",
            "Iwachu-pattern cases (C_P \u2265 5 \u2227 R_cat \u2264 2) "
            "appear in at least one of Cells A or B (6th substrate family "
            "extension test). GENERALIZED if \u2265 1 case in A or B; "
            "PARTIAL if cases only in C or D; FALSIFIED if zero cases.",
            "17 Iwachu cases across all four cells (4 Cell A, 4 Cell B, "
            "4 Cell C, 5 Cell D). Cell A and Cell B both clear. Cell D "
            "cases are tautological (defunct brands trivially meet the "
            "criterion); substantive base is 12 cases across A, B, C. "
            "6th substrate family closed.",
            "GENERALIZED",
            "confirmed",
        ),
        (
            "H_IdentityLoad_direct",
            "v1.6 Inc2 R4-independent IL Direct. Cell A vs Cell B mean IL "
            "comparison; IL = R_cult / R_cat per cell (R4-independent "
            "because Phase B Recall only, not Phase A Recognition). "
            "CONFIRMED if Cell A IL > Cell B IL; FALSIFIED otherwise.",
            "Cell A IL = 12.43 / 5.14 = 2.42. Cell B IL = 1.20 / 1.60 = "
            "0.75. Separation = 3.2\u00d7 cult-channel dominance lead for "
            "Cell A. The substantive IL signature is the strongest the "
            "program has anchored R4-independently.",
            "CONFIRMED",
            "confirmed",
        ),
        (
            "H_SubstrateRecognition_PreScreen",
            "v1.6 Inc1 substrate Recognition pre-screen. Non-directional "
            "classification probe. UNIFORM SATURATION if all cells modal "
            "C_P \u2265 5; DIFFERENTIAL otherwise.",
            "All cells modal C_P = 6 (Cell A, C, D at 6/6 unanimous; Cell "
            "B at 6/6 modal with single Fisker non-yes at 5/6). UNIFORM "
            "SATURATION classification confirmed as predicted; substrate "
            "joins cosmetics as second program substrate with all-cell "
            "Recognition saturation.",
            "UNIFORM SATURATION",
            "descriptive",
        ),
    ],
}


# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS
# Item format: (h_id, body_text)
# ---------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis interpretation",
    "intro": (
        "Each verdict carries substantive interpretation beyond the matrix "
        "routing. The verdicts are what the data produced; the meaning of "
        "each verdict for the construct, the boundary conditions, and the "
        "v0.22+ trajectory is what the prose below addresses."
    ),
    "items": [
        (
            "H_Phantom_Defunct",
            "<b>What it means.</b> The phantom phenomenon has a temporal "
            "floor. The AI mediation layer recognizes documented-defunct "
            "corporate brands as category members (C_P = 6/6 unanimous) "
            "but does not surface them in present-tense Recall in any of "
            "the eighteen unprompted opportunities per brand. The "
            "mediation layer is not merely \u201cassociating brand names "
            "with categories\u201d; it is associating brand names with "
            "categories plus temporal status, and that temporal status "
            "is robust enough that documented discontinuation acts as a "
            "hard Recall floor. The falsification is the result: a "
            "tighter, more falsifiable phantom construct than the "
            "substrate-agnostic version v0.21 implied. <b>What it "
            "doesn\u2019t mean.</b> FALSIFIED does not refute Phantom "
            "Brand Persistence as a phenomenon. The supporting hypothesis "
            "confirms in the same panel run on the same heritage substrate. "
            "What it refutes is the specific claim that phantom-surface "
            "leakage extends to documented-dead corporate brands. The "
            "construct survives in living-brand form; it is the "
            "discontinued-brand extension that fails."
        ),
        (
            "H_Phantom_Brand_Persistence_heritage",
            "<b>What it means.</b> Living heritage brands surface in "
            "unprompted Recall at rates that match the program\u2019s "
            "v0.21 off-panel benchmark (Glossier at R_phantom = 12). "
            "Three Cell A brands cross the CONFIRMED threshold: Porsche "
            "at 14/18 (with R_cult at the maximum 18/18 \u2014 every cult "
            "question in every model returns Porsche), BMW at 12/18, "
            "Mercedes-Benz at 10/18. The phantom phenomenon is real and "
            "real on this substrate; the boundary is the temporal one "
            "noted under the lead hypothesis. <b>What it doesn\u2019t "
            "mean.</b> CONFIRMED on three brands isn\u2019t \u201call "
            "heritage brands phantom-persist.\u201d The cell\u2019s other "
            "four brands (Rolls-Royce, Bentley, Jaguar, Cadillac) score "
            "R_phantom = 0 \u2014 they surface in R_cult heritage frames "
            "but not in R_cat canonical-recommendation frames, which is "
            "the operationalization R_phantom uses. The phantom mechanism "
            "may be R_cat-specific (canonical-channel) rather than R_cult-"
            "specific (cultural-channel); the within-cell split is worth "
            "preserving in v0.22+ discourse."
        ),
        (
            "H_Regime4_automotive",
            "<b>What it means.</b> The Regime 4 four-stage routing fails "
            "at the C2 floor in all four cells. Automotive joins cosmetics "
            "as a substrate where category-membership Recognition is not "
            "the discriminating channel \u2014 the AIAS signal lives "
            "entirely in Recall. The verdict is the predicted outcome and "
            "documents what v1.6 Inc1 was designed for: routing this "
            "saturation case distinctly from differential-saturation "
            "substrates. <b>What it doesn\u2019t mean.</b> FALSIFIED is "
            "not a refutation of the underlying multi-component construct "
            "\u2014 the construct\u2019s discrimination signal is provided "
            "by Phase B Recall, which v0.22 produces in rich form (seven "
            "Type 2 cases, two Type 1, twelve substantive Iwachu cases). "
            "The Regime 4 rule does not capture the signal that is present "
            "on this substrate; the construct does."
        ),
        (
            "H_Dissoc_substrate_generalization",
            "<b>What it means.</b> The Recognition \u00d7 Recall dissociation "
            "construct now spans six substrate families (kitchen knives, "
            "kitchenware, indie fragrance, audiophile headphones, "
            "skincare, cosmetics, automotive). The substrate-breadth "
            "threshold for AIAS\u2122 1.0\u2019s headline cross-substrate "
            "generalization claim is closed. The pattern is not specific "
            "to language family, price-tier structure, or cultural "
            "origin. <b>What it doesn\u2019t mean.</b> Cell D\u2019s "
            "five tautological Iwachu cases (defunct brands trivially "
            "meet the criterion because the lead hypothesis falsifies) "
            "should not inflate the substantive count. The honest base "
            "for v0.22 is twelve cases across Cells A, B, and C \u2014 "
            "still the largest substantive single-phase count in the "
            "program. Future v1.6+ increments may benefit from a "
            "substrate-internal Iwachu criterion that excludes phantom-"
            "floor cases."
        ),
        (
            "H_IdentityLoad_direct",
            "<b>What it means.</b> The IL gradient is real at the channel-"
            "asymmetry layer, evaluated for the first time in the program "
            "R4-independently. Cell A heritage brands carry 3.2\u00d7 the "
            "cult-channel dominance of Cell B disruptor brands. v1.6 "
            "Inc2 was designed for substrates where the IL signature is "
            "real but the Regime 4 C2 path cannot evaluate it (because "
            "Recognition saturates and supplies no within-cell variance); "
            "v0.22 supplies the cleanest demonstration the program has "
            "produced. <b>What it doesn\u2019t mean.</b> The interim "
            "operationalization (sign-of-difference test on R_cult / "
            "R_cat ratio) is not the full v1.6 Inc2 specification \u2014 "
            "the bootstrap CI construction is still outstanding in the "
            "methodology paper. The 3.2\u00d7 separation is robust to "
            "operationalization, but a v1.6.1 supplement should pin the "
            "exact bootstrap procedure before v0.23+ phases run against "
            "it."
        ),
        (
            "H_SubstrateRecognition_PreScreen",
            "<b>What it means.</b> Automotive is the second program "
            "substrate (after cosmetics) where v1.6 Inc1 classifies "
            "UNIFORM SATURATION at all-cell C_P modal = 6. The "
            "classification is non-directional but consequential: it "
            "routes downstream interpretation distinctly from "
            "differential-saturation cases. Both substrates that have "
            "produced this classification (cosmetics, automotive) are "
            "categorically self-evident in the AI mediation layer \u2014 "
            "every plausible-panel brand passes binary category "
            "classification at every panel model. <b>What it doesn\u2019t "
            "mean.</b> UNIFORM SATURATION isn\u2019t a property of the "
            "substrate as such; it is a property of (substrate \u00d7 "
            "panel) pairing at acquisition time. A v0.22 replication on a "
            "future LLM panel could in principle produce DIFFERENTIAL on "
            "the same substrate if model-training-corpus shifts dilute "
            "the category coding; this is a property to monitor across "
            "panel upgrades."
        ),
    ],
}


# ---------------------------------------------------------------------------
# CLOSING
# ---------------------------------------------------------------------------

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano Gonz\u00e1lez Castro",
        "School of Visual Arts, MPS Branding Program \u00b7 New York, NY",
        "Third System\u2122 (research entity; data archive and methodology venue)",
        "Correspondence: pablou@pablou.com \u00b7 ORCID: 0009-0003-8968-9990",
    ],
    "datasets": [
        "v0.22 Phase A acquisition (Recognition C_P, n = 144 probes): "
        "osf.io/ec6wh/v22/data/phase_a_results.csv",
        "v0.22 Phase B acquisition (Recall two-channel, n = 36 queries): "
        "osf.io/ec6wh/v22/data/phase_b_results.csv",
        "v0.22 scoring verdicts (six hypothesis matrices resolved): "
        "osf.io/ec6wh/v22/data/v22_verdicts.json",
        "v0.22 pre-registration (Python module, code-importable, r2 "
        "supersedes r1): osf.io/ec6wh/v22/prereg/v0_22_automotive_content.py",
        "v0.22 mega-prompt (DEVIATIONS Entry 0 documents the r1 \u2192 r2 "
        "amendment): osf.io/ec6wh/v22/prereg/v0_22_mega_prompt.md",
    ],
    "methodology_log": (
        "v0.22 pre-registration locked at git tag v0.22-prereg-r2 (commit "
        "0dde745, superseding r1 at commit edc61f3), branch program-docs. "
        "First prospective phase under Protocol v1.6 lock (SSRN 6816340); "
        "carries forward v1.5 two-channel Recall (SSRN 6810758) and v1.2 "
        "four-regime taxonomy (SSRN 6761698). Acquisition locked at git "
        "tag v0.22-acquisition-locked. Academic companion: SSRN TBD"
    ),
}
