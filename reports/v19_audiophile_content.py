"""
v0.19 Audiophile Headphones — Brand-format report content.

Schema matches v18_indie_fragrance_content.py exactly so build_report_v19.py
can fork build_report_v18.py with surgical changes.

All verdict markers reflect the actual v0.19 scoring outputs:
  - H_C3 = UNDETERMINED (Rule 4 routing; both cells fail C2 modal share)
  - H_Dissociation_Replication = PARTIAL (3 cases on third substrate family)
  - H_CulturalFootprint = descriptive (3 Type 1 cases, 0 Type 2 cases)

Citation chain:
  - AIAS Protocol v1.4 (SSRN 6799479) — methodology base
  - v0.16 (SSRN 6791999), v0.17 (SSRN 6802261), v0.18 (SSRN 6806558) — predecessor legs
  - Pre-reg tag v0.19-prereg-r1 at commit 2cbd36c
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path.home() / "aias"
V19_ROOT = ROOT / "osf" / "v19"
PHASE_A_RESULTS = V19_ROOT / "phase_a_results.csv"
PHASE_B_RESULTS = V19_ROOT / "phase_b_results.csv"
VERDICTS_TXT = V19_ROOT / "scoring_output_v0_19.txt"

# Panel totals
TOTAL_PRE = 16
TOTAL_POST = 16

CELL_COUNTS = {
    "Cell A — Heritage (pre-2008 audiophile)":   {"pre": 8, "post": 8},
    "Cell B — Boutique (post-2008 audiophile)":  {"pre": 8, "post": 8},
}


# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------

COVER = {
    "title": "At the Boundary",
    "subtitle": "AIAS v0.19 — Audiophile Headphones",
    "date": "May 2026",
    "byline_short": "Pablo Ulpiano González Castro",
    "tagline": (
        "Three Iwachu cases on a third substrate family. "
        "A Recognition ceiling holding at exactly 0.500 modal share. "
        "A cultural channel waiting for v0.20."
    ),
}


# ---------------------------------------------------------------------------
# STANDFIRST
# ---------------------------------------------------------------------------

STANDFIRST = (
    "The audiophile-headphones panel met the Recognition ceiling that "
    "v0.18 met before it. Cell A_Heritage stops at exactly 0.500 "
    "modal share — failing C2 by a single brand at the ceiling. Cell "
    "B_Boutique sits well above the threshold at 0.875. H_C3 routes "
    "to UNDETERMINED per pre-registered Rule 4. But three new Iwachu "
    "cases extend the Recognition × Recall dissociation construct to "
    "a third substrate family, and a cultural-channel asymmetry — "
    "three Type 1 brands, zero Type 2 brands — identifies a panel-"
    "composition limit that points cleanly at v0.20's substrate "
    "selection. The phase is informative below the headline."
)


# ---------------------------------------------------------------------------
# LEAD_DECK
# ---------------------------------------------------------------------------

LEAD_DECK = (
    "The AIAS™ Presence Measurement Protocol v1.4 multi-component construct "
    "widens to three substrate families. The C3 ranking-coherence rescue "
    "attempted on a same-IL Heritage × Boutique design didn't land — the "
    "audiophile-headphone substrate produces Recognition ceiling effects in "
    "both cells. Three pre-registered hypotheses; one UNDETERMINED, one "
    "PARTIAL, one descriptive. The methodology gains an empirical anchor; "
    "the construct gains three more cases."
)


# ---------------------------------------------------------------------------
# EXEC_SUMMARY
# ---------------------------------------------------------------------------

EXEC_SUMMARY = [
    "v0.19 was designed as the C3 rescue phase. v0.18 left the ranking-"
    "coherence test structurally degenerate — Cell A's flat Recognition "
    "(7 of 8 brands tied at C_P = 6/6) and Cell B's flat Recall (7 of 8 "
    "brands tied at 0 mentions) both undermined within-cell rank "
    "correlation. v0.19 selected a substrate engineered for within-cell "
    "variance in both dimensions: audiophile headphones, two same-IL cells "
    "split by audiophile headphone product-line emergence year (Heritage "
    "≤ 2008, Boutique > 2008), 16 brands worldwide pre-floor, English-"
    "language anchored throughout.",

    "The substrate did not deliver C3. Cell A_Heritage produced Recognition "
    "modal share = 0.500 (four of eight brands at C_P = 6/6: Sennheiser, "
    "Beyerdynamic, Grado, Audio-Technica) — exactly at the C2 strict-less-"
    "than threshold and failing by a single brand at the ceiling. Cell "
    "B_Boutique produced modal share = 0.875 (seven of eight brands at "
    "C_P = 6/6; only Spirit Torino at 5/6 below ceiling). Both cells fail "
    "C2; H_C3 routes to UNDETERMINED per pre-registered DEVIATIONS Rule 4. "
    "Per the rule, panel is NOT substituted; the substantive finding stands.",

    "The substantive value of v0.19 sits below the UNDETERMINED headline. "
    "Three Iwachu-pattern cases (Phase A C_P ≥ 5/6 AND Phase B category-"
    "anchored mentions ≤ 2/18) replicate on the headphone substrate: ZMF "
    "Headphones (6/6, 1/18), Spirit Torino (5/6, 0/18), and Final Audio "
    "(6/6, 0/18) — all Cell B_Boutique. The v1.4 multi-component construct "
    "now has 13 cases across three substrate families (v0.17 Iwachu cross-"
    "cultural + v0.18 indie fragrance 9 cases + v0.19 audiophile 3 cases), "
    "strengthening its empirical foundation beyond what a single phase can "
    "provide. PARTIAL on the matrix, but the third-substrate-family "
    "contribution is the headline.",

    "A cultural-channel asymmetry surfaces three Type 1 cases (Audeze, "
    "HiFiMan, Dan Clark Audio: category-anchored mentions ≥ 5/18 AND "
    "cultural-footprint mentions ≤ 2/18) and zero Type 2 cases. The Type "
    "2 absence reflects panel composition, not the absence of the "
    "cultural-footprint Recall pathway: the Heritage × Boutique audiophile-"
    "electronics design places both cells inside the category-recognition "
    "envelope. A v0.20 substrate including a mass-consumer headphone cell "
    "(Bose, Beats, Apple, Skullcandy, JBL) would test Type 2 cleanly. The "
    "finding identifies a load-bearing v0.20 substrate selection criterion.",
]


# ---------------------------------------------------------------------------
# WHAT_WE_MEASURED
# ---------------------------------------------------------------------------

WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        "Two acquisition phases scored by pre-registered decision rules. "
        "Phase A measures <b>Recognition</b> — whether the AI panel "
        "recognizes a brand as belonging to the category. Phase B measures "
        "<b>Recall</b> — whether the AI panel surfaces the brand when asked "
        "to enumerate category members. Verdicts route through a C1 → C2 → "
        "C3 cascade per the locked pre-registration.",

        "Phase A asks each of the six reference panel models a single "
        "question per brand: <i>'Is the brand X commonly recognized as a "
        "brand of audiophile headphones?'</i> The brand's Recognition "
        "score (C_P, range 0..6) is the count of recognition-positive "
        "responses across the panel. Cell-level variance is tested via "
        "C2 modal share — the share of brands at the cell's most common "
        "C_P value, which must be strictly less than 0.50 for the cell "
        "to pass.",

        "Phase B asks the same six models six queries: three category-"
        "anchored frames (<i>best audiophile headphones</i>, <i>high-quality "
        "headphones for serious music listening</i>, <i>reference-grade "
        "headphones</i>) that load-bear on the verdict matrix; plus three "
        "cultural-footprint frames (<i>most famous headphone brands</i>, "
        "<i>most well-known among general consumers</i>, <i>strongest "
        "cultural recognition</i>) that operate as descriptive sensitivity "
        "for the cultural-footprint Recall channel surfaced as a v0.18 "
        "finding. Each brand has at most 18 observation slots per channel "
        "(3 frames × 6 models).",

        "The Recognition × Recall dissociation threshold (Iwachu-pattern) "
        "requires C_P ≥ 5/6 AND category-anchored mentions ≤ 2/18 — the "
        "brand is recognized in 5+ of 6 single-brand probes, but surfaces "
        "in 2 or fewer of 18 enumeration responses. The Type 1 / Type 2 "
        "channel-asymmetry thresholds replicate this asymmetric structure "
        "across the cultural-footprint axis. The pre-registration is locked "
        "at commit 2cbd36c with C1, C2, C3, Iwachu, and channel-asymmetry "
        "thresholds all fixed ex-ante.",
    ],
}


# ---------------------------------------------------------------------------
# PATTERNS — three findings, each anchored by one chart
# ---------------------------------------------------------------------------

PATTERNS = [
    {
        "number": 1,
        "title": "Recognition saturated: the ceiling in both cells",
        "chart_slot": "f1_cp_distribution",
        "paragraphs": [
            "Cell A_Heritage produced a Recognition distribution that is "
            "substantively richer than v0.18's degenerate Cell A but "
            "operationally fails the pre-registered C2 threshold by a "
            "single brand at the ceiling. C_P scores: Sennheiser, "
            "Beyerdynamic, Grado, and Audio-Technica at 6/6; Stax at "
            "5/6; Sony at 4/6; Denon at 3/6; Koss at 2/6. Five distinct "
            "C_P values across eight brands, range 2 to 6, mean ≈ 4.75. "
            "But the modal value (6/6) is held by four of eight brands — "
            "modal share = exactly 0.500. Under the pre-registered C2 rule "
            "(strict less-than 0.50), Cell A fails by the smallest "
            "possible margin.",

            "Cell B_Boutique saturated. Seven of eight brands score "
            "C_P = 6/6 (Audeze, HiFiMan, Focal, Meze, ZMF Headphones, "
            "Final Audio, Dan Clark Audio); only Spirit Torino at 5/6 "
            "breaks the ceiling. Modal share = 0.875, well above the C2 "
            "threshold. This is the v0.18 ceiling pattern repeating — "
            "boutique audiophile brands are universally recognized by "
            "the panel as audiophile-headphone brands, leaving no within-"
            "cell Recognition variance for C3 ranking coherence to test.",

            "Per DEVIATIONS Rule 4, both cells route H_C3 to UNDETERMINED. "
            "The verdict is methodologically appropriate: C3 measures rank "
            "correlation between Recognition and Recall, and when "
            "Recognition variance collapses the rank correlation is "
            "uninformative regardless of the Recall distribution. UNDETERMINED "
            "preserves the substantive interpretation: the substrate did not "
            "expose C3, not that C3 is false.",

            "Cell A's failure at exactly 0.500 is a documented limit of the "
            "C2 operationalization, not a substrate failure per se. The "
            "distribution is qualitatively different from v0.18's Cell A "
            "(7/8 tied at 6/6, modal share 0.875). Five distinct values, "
            "range 4 across 8 brands — a substantively rich Recognition "
            "profile that the modal-share metric flags as uniform. AIAS™ "
            "1.0's methodology layer should consider entropy-based or "
            "multi-statistic C2 specifications; the v0.19 boundary case "
            "is the empirical anchor motivating the refinement.",
        ],
    },
    {
        "number": 2,
        "title": "Three more cases: dissociation lands in Boutique",
        "chart_slot": "f2_dissociation_scatter",
        "paragraphs": [
            "Three Iwachu-pattern cases on the audiophile substrate, all "
            "concentrated in Cell B_Boutique: ZMF Headphones (Phase A "
            "C_P = 6/6, Phase B category-anchored mentions = 1/18), "
            "Spirit Torino (C_P = 5/6, mentions = 0/18), and Final Audio "
            "(C_P = 6/6, mentions = 0/18). All three brands are panel-"
            "recognized as audiophile headphone brands at high consensus, "
            "yet the same panel does not surface them when asked to "
            "enumerate the category. The construct that v0.17 anchored "
            "and v0.18 generalized now extends to a third substrate family.",

            "Cell A_Heritage contributes zero Iwachu-pattern cases — not "
            "by Recognition-floor design (as Cell C did in v0.18) but "
            "because Heritage brands that achieve C_P ≥ 5/6 (Sennheiser, "
            "Beyerdynamic, Grado, Audio-Technica, Stax) also surface "
            "substantively in Phase B category-anchored frames. The "
            "Heritage tier's broad LLM training-data depth supports both "
            "Recognition and Recall; the Boutique tier's enthusiast-"
            "discourse presence supports Recognition without producing "
            "comparable Recall.",

            "The cumulative anchor base for the v1.4 multi-component "
            "construct now spans three substrate families: 1 case from "
            "v0.17 (Iwachu, Japanese cell, cross-cultural), 9 cases from "
            "v0.18 (indie fragrance, English-language, IL-stratified), "
            "and 3 cases from v0.19 (audiophile electronics, English-"
            "language, brand-era stratified). Thirteen cases total. "
            "Before v0.18, the construct rested on one cross-cultural "
            "case; before v0.19, on a same-language substrate where the "
            "pattern could be argued to be IL-specific. v0.19 closes "
            "that argument: dissociation appears at the high-IL tier of "
            "fragrance and at the boutique tier of audiophile-electronics "
            "alike. The construct travels.",

            "The cell-clustering pattern continues. v0.18 saw 6 of 9 "
            "cases in its highest-IL cell (75% of cell brands). v0.19 "
            "sees 3 of 3 cases in Boutique (37.5% of cell brands). "
            "Different cell-level prevalence, but the same directional "
            "story: dissociation concentrates in the cell whose brands "
            "operate further from the mainstream cultural-discourse "
            "surface. This is the empirical regularity the v1.4 construct "
            "predicts, observed twice on two distinct substrates.",
        ],
    },
    {
        "number": 3,
        "title": "The channel that wasn't: cultural-footprint asymmetry",
        "chart_slot": "f3_channel_asymmetry",
        "paragraphs": [
            "v0.19's six-frame Phase B battery split category-anchored "
            "Recall (three frames testing audiophile-discourse retrieval) "
            "from cultural-footprint Recall (three frames testing "
            "mainstream consumer-discourse retrieval) so the two "
            "pathways could be observed independently. The v0.18 §4.3 "
            "sensitivity finding — Tom Ford and Chanel surfacing in "
            "category-anchored Phase B frames despite failing the "
            "niche-fragrance Recognition probe — predicted that v0.19 "
            "should produce <b>Type 2 cases</b>: brands with low "
            "category-anchored Recall but high cultural-footprint Recall.",

            "Three Type 1 cases (category-channel-preferred): Audeze "
            "(category-anchored 13/18, cultural-footprint 2/18), HiFiMan "
            "(12/18, 1/18), and Dan Clark Audio (5/18, 0/18) — all Cell "
            "B_Boutique boutique audiophile brands. These brands surface "
            "strongly in audiophile discourse but minimally in mainstream "
            "cultural-recognition prompts, the expected profile for "
            "discourse-strong boutique brands.",

            "Zero Type 2 cases — no brand in the v0.19 panel exhibits "
            "low category-anchored Recall paired with high cultural-"
            "footprint Recall. The cultural-footprint pathway is "
            "demonstrably operating (Phase B q4–q6 responses surface "
            "Bose, Beats, AirPods Max, Sony WH-1000XM, Skullcandy, JBL "
            "extensively) but the brands surfacing through it are not "
            "in the v0.19 panel. The Heritage × Boutique audiophile-"
            "electronics design places both cells inside the category-"
            "recognition envelope; nothing in panel tests the 'cultural "
            "without category' shape.",

            "For AIAS™ 1.0's methodology layer, the Type 2 absence is a "
            "load-bearing finding: it identifies a panel-composition "
            "criterion v0.20+ must satisfy to test the cultural-footprint "
            "channel cleanly. A future phase needs a third cell of mass-"
            "consumer brands (Bose, Beats, Apple, Skullcandy, JBL) "
            "deliberately placed below the audiophile-category Recognition "
            "threshold. Type 2 cases will then be observable; the v1.5 "
            "methodology paper can formalize cultural-footprint Recall as "
            "a distinct Recall mode alongside category-anchored Recall.",
        ],
    },
]


# ---------------------------------------------------------------------------
# HYPOTHESIS_SCORING
# ---------------------------------------------------------------------------

HYPOTHESIS_SCORING = {
    "heading": "The three verdicts",
    "intro": (
        "Three pre-registered hypotheses; three verdicts of different "
        "shapes. H_C3 routes to UNDETERMINED per DEVIATIONS Rule 4 — the "
        "substrate did not expose the ranking-coherence test. H_Dissoc "
        "lands PARTIAL with three new Iwachu cases on a third substrate "
        "family. H_CulturalFootprint is descriptive only, returning a "
        "case-list that identifies a panel-composition limit for v0.20."
    ),
    "rows": [
        (
            "H_C3",
            "C1 (n ≥ 12) → C2 (per-cell modal share < 0.50, both "
            "dimensions) → C3 (per-cell ρ ≥ 0.50 AND bootstrap CI lower "
            "bound > 0.20, in ≥ 1 of 2 cells)",
            "C1 ✓ (n = 16); C2 ✗ — Cell A_Heritage modal share = "
            "0.500 (FAIL at boundary), Cell B_Boutique modal share = "
            "0.875 (FAIL); C3 SKIPPED per Rule 4",
            "UNDETERMINED",
            "partial",
        ),
        (
            "H_Dissoc",
            "Iwachu pattern (C_P ≥ 5 ∧ category-anchored mentions ≤ 2) "
            "replicates on third substrate family (≥ 5 cases ⇒ "
            "REPLICATED; 1–4 cases ⇒ PARTIAL; 0 cases ⇒ NOT_REPLICATED)",
            "3 cases identified: ZMF Headphones (6/6, 1/18), Spirit "
            "Torino (5/6, 0/18), Final Audio (6/6, 0/18). All Cell "
            "B_Boutique. Cumulative anchor base = 13 cases across 3 "
            "substrate families.",
            "PARTIAL",
            "partial",
        ),
        (
            "H_CulturalFootprint",
            "Document Type 1 (category-preferred) and Type 2 (cultural-"
            "preferred) dissociation cases per cell. Descriptive output; "
            "no verdict.",
            "Type 1: 3 cases (Audeze 13/18 vs 2/18; HiFiMan 12/18 vs "
            "1/18; Dan Clark Audio 5/18 vs 0/18 — all Cell B). Type "
            "2: 0 cases (panel-composition limit).",
            "DESCRIPTIVE",
            "descriptive",
        ),
    ],
}


# ---------------------------------------------------------------------------
# HYPOTHESIS_DETAILS
# ---------------------------------------------------------------------------

HYPOTHESIS_DETAILS = {
    "heading": "Hypothesis details",
    "intro": (
        "The three verdicts in more detail, with the resolution path each "
        "took through the pre-registered decision cascade."
    ),
    "items": [
        (
            "H_C3_Within_Cell_Variance",
            "Resolved at C2 (variance adequacy). C1 panel adequacy clears "
            "cleanly (worldwide n = 16, per-cell n = 8, both above floors). "
            "C2 fails in both cells: Cell A_Heritage modal share = 0.500 "
            "(four of eight brands at C_P = 6/6), Cell B_Boutique modal "
            "share = 0.875 (seven of eight brands at C_P = 6/6). Per "
            "DEVIATIONS Rule 4, both cells route to UNDETERMINED. C3 is "
            "not computed — the substrate did not expose the test. The "
            "Cell A boundary case (failing by one brand at the ceiling) "
            "is documented as a methodological finding for AIAS™ 1.0 C2 "
            "operationalization refinement.",
        ),
        (
            "H_Recognition_Recall_Dissociation_Replication",
            "Three Iwachu-pattern cases identified on the v0.19 panel: "
            "ZMF Headphones (Phase A C_P = 6/6, Phase B category-anchored "
            "mentions = 1/18), Spirit Torino (5/6, 0/18), and Final Audio "
            "(6/6, 0/18). All three are Cell B_Boutique. PARTIAL routes "
            "between REPLICATED (≥ 5 cases) and NOT_REPLICATED (0 cases). "
            "Substantively this is the v0.19 headline: the v1.4 multi-"
            "component construct now spans three substrate families "
            "(v0.17 Japanese kitchenware + v0.18 indie fragrance + v0.19 "
            "audiophile electronics), with 13 cumulative cases across the "
            "three. The construct is no longer anchored by single-case or "
            "single-substrate evidence.",
        ),
        (
            "H_CulturalFootprint_Dissociation_Sensitivity",
            "Three Type 1 cases (category-channel-preferred): Audeze, "
            "HiFiMan, Dan Clark Audio — all Cell B_Boutique brands with "
            "strong audiophile-discourse Recall and minimal mainstream "
            "cultural-footprint Recall. Zero Type 2 cases (cultural-"
            "channel-preferred). The Type 2 absence reflects panel "
            "composition: both cells of v0.19's Heritage × Boutique design "
            "sit inside the category-recognition envelope, so no panel "
            "brand has the 'low category-anchored Recall plus high "
            "cultural-footprint Recall' profile the cultural channel "
            "would produce. The descriptive finding identifies a v0.20 "
            "panel-composition criterion: include a mass-consumer cell "
            "below the category-recognition floor to test Type 2.",
        ),
    ],
}


# ---------------------------------------------------------------------------
# LIMITATIONS
# ---------------------------------------------------------------------------

LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        "<b>C2 operationalization at the strict-less-than boundary.</b> "
        "Cell A_Heritage's C_P distribution [2, 3, 4, 5, 6, 6, 6, 6] is "
        "substantively richer than v0.18's degenerate Cell A (7/8 tied "
        "at C_P = 6/6, modal share 0.875). Five distinct C_P values "
        "across eight brands, range 4. But the modal-share metric "
        "captures only the most common value's prevalence and flags this "
        "as variance-degenerate at exactly 0.500. The strict-less-than "
        "C2 threshold is appropriately tight for catching v0.18-shape "
        "degeneracy but over-sensitive on mixed distributions where 50% "
        "of brands sit at one value with the other 50% distributed. "
        "AIAS™ 1.0 / v1.5 should consider entropy-based or multi-"
        "statistic C2 (e.g., distinct-value count + modal share, or "
        "Shannon entropy normalized to the cell).",

        "<b>Type 2 absence reflects panel composition, not pathway absence.</b> "
        "The zero-Type-2 finding does not falsify the cultural-footprint "
        "Recall channel — Phase B q4–q6 responses surface Bose, Beats, "
        "AirPods Max, Sony WH-1000XM, Skullcandy, JBL extensively. The "
        "Heritage × Boutique audiophile-electronics design places both "
        "cells inside the category-recognition envelope, so no panel "
        "brand has the profile (low category-anchored Recall + high "
        "cultural-footprint Recall) the channel would produce. v0.20+ "
        "should include a mass-consumer cell deliberately placed below "
        "the audiophile-category Recognition floor.",

        "<b>Cross-cultural robustness analysis not applicable.</b> "
        "Pre-registered DEVIATIONS Rule 6 requires Stax / HiFiMan "
        "exclusion analysis as Δρ comparison against full-cell ρ. Because "
        "both cells failed C2, ρ was not computed for either cell, and "
        "the robustness analysis reports 'not applicable' for both. "
        "Cross-cultural confound exposure for v0.19 is therefore "
        "documented but unquantified. Future substrates with within-"
        "cell variance adequate to clear C2 will permit the robustness "
        "computation per Rule 6.",

        "<b>LLM panel temporal validity.</b> The six-slot reference panel "
        "(claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, "
        "gemini-2.5-flash, gemini-2.5-flash-lite) reflects model versions "
        "in market as of mid-2026. Provider model substitutions over "
        "future-phase horizons are expected and documented in the "
        "DEVIATIONS protocol. v0.19 dissociation cases and channel-"
        "asymmetry pattern should be read as the result observed against "
        "the locked panel at acquisition (2026-05-20), not as permanent "
        "substrate properties.",
    ],
}


# ---------------------------------------------------------------------------
# WHATS_NEXT
# ---------------------------------------------------------------------------

WHATS_NEXT = {
    "heading": "What's next",
    "paragraphs": [
        "Four pre-registerable directions emerge from the v0.19 verdicts. "
        "None requires retracting v0.19; each addresses a specific "
        "v0.19 finding.",

        "<b>Substrates with within-cell Recognition variance below the "
        "0.50 modal-share floor.</b> The C3 rescue did not land on the "
        "audiophile-electronics substrate. v0.20 should select a substrate "
        "where the within-cell Recognition distribution spans enough "
        "range that modal share sits cleanly below 0.50 in both cells — "
        "categories with a long tail of enthusiast-known but not "
        "universally-known brands (specialty board games, particular "
        "wine appellations, kitchenware tiers below premium) are "
        "candidates worth evaluating.",

        "<b>Mass-consumer cell inclusion to test Type 2 dissociation.</b> "
        "v0.20 should include at least one cell of mass-consumer brands "
        "(in the headphone substrate: Bose, Beats, Apple AirPods, "
        "Skullcandy, JBL) deliberately placed below the audiophile-"
        "category Recognition floor. With brands in panel that the "
        "cultural-footprint frames surface but the category-anchored "
        "frames do not, Type 2 cases become observable and the "
        "cultural-footprint Recall channel can be formalized in v1.5.",

        "<b>v1.5 methodology paper: C2 operationalization refinement + "
        "cultural-footprint Recall mode.</b> The methodology layer "
        "between v1.4 (current) and AIAS™ 1.0 (target) has two open "
        "items surfaced by v0.18 and v0.19 together. First, C2's modal-"
        "share-< 0.50 operationalization is over-sensitive on mixed "
        "distributions (v0.19 Cell A_Heritage) while under-sensitive on "
        "saturation (v0.19 Cell B_Boutique fails at 0.875). An entropy-"
        "based or distinct-value-count alternative is the candidate "
        "replacement. Second, cultural-footprint Recall surfaces in "
        "every multi-substrate phase but has no canonical methodology "
        "treatment; v1.5 can formalize it as a distinct Recall mode.",

        "<b>The C3 question remains open across the program.</b> Four "
        "phases (v0.16, v0.17, v0.18, v0.19) have probed the C3 "
        "ranking-coherence test; none has produced a clean PASS on "
        "both cells of a substrate. The substrate-selection lever is "
        "the right one to pull next — v0.18's IL-gradient and v0.19's "
        "Heritage × Boutique designs both produced ceiling effects "
        "where the C3 test needs variance. The lever is not threshold "
        "loosening; it is substrate engineering. v0.20 carries that "
        "constraint into substrate selection from the start.",
    ],
}


# ---------------------------------------------------------------------------
# CLOSING
# ---------------------------------------------------------------------------

CLOSING = {
    "byline_long": [
        "Pablo Ulpiano González Castro",
        "School of Visual Arts, MPS Branding Program (primary academic affiliation)",
        "Third System™ — research entity",
        "pablou@pablou.com · pablou.com · ORCID 0009-0003-8968-9990",
    ],
    "datasets": [
        "Pre-registration and DEVIATIONS log: osf.io/ec6wh/v19/PRE_REGISTRATION_v0_19.md "
        "and osf.io/ec6wh/v19/DEVIATIONS.md",
        "Phase A and Phase B acquisition data: osf.io/ec6wh/v19/phase_a_results.csv "
        "and osf.io/ec6wh/v19/phase_b_results.csv",
        "Scoring code, registry, figures: osf.io/ec6wh/v19/score_v0_19.py, "
        "panel_registry_v0_19.csv, thresholds_v0_19.json, scoring_output_v0_19.txt",
    ],
    "methodology_log": "thirdsystem.ai/methodology and osf.io/ec6wh",
}
