"""
Text of the Coverage Paper A brief (TS-BR-v1.12-r1). Managerial register: plain findings, no hypothesis labels.
Every number is a {KEY} placeholder filled by reports/build_brief_v1_12.py from brief_v1_12_values.py (unknown key
-> KeyError). Note markers are {N1}, {N2}, ... (small_print.NoteSeq, numbered per page).
"""

TITLE = "How widely AI answers name a brand across buying situations is a measure of its own"
KICKER = "BRIEF · COVERAGE PAPER A"
RUNNING_LABEL = "AIAS™ Methodology v1.12 · November 2026"

STANDFIRST = ("Buying situations change which brands AI answers name{N1}. How widely a brand's mentions spread over "
              "them, adjusted for how often it is named, is separate from Presence, Consistency and naming rate{N2} "
              "and holds on two halves of the situations{N3}: Coverage passes as a third AIAS™ component.")

NUMBERS = [
    {"value": "{MSIT_DIFF}", "unit": "", "label": "Situations change the brands named",
     "source": "Gap in brand-list overlap; required {MSIT_DIFF_MIN}"},
    {"value": "{H1}", "unit": "", "label": "Overlap of Coverage with Presence",
     "source": "Separate at {BAND_LO} or below; {H1_N} brands"},
    {"value": "{H4_REL}", "unit": "", "label": "Agreement between two halves of the situations",
     "source": "Split-half reliability; required {REL_MIN}"},
]

NOTES_P1 = [
    "Overlap (Jaccard similarity) of the sets of listed brands named, averaged over {MSIT_CELLS} model, run and "
    "category cells of the three-model panel: {MSIT_WITHIN} between repeats of one situation question, "
    "{MSIT_BETWEEN} between different situations. The plan required a gap of at least {MSIT_DIFF_MIN}, with overlap between situations of at most "
    "{MSIT_JB_MAX}.",
    "Within-category rank correlation of the Coverage score with Presence (how often AI answers name the brand), "
    "{H1} ({H1_N} brands); Consistency (how far the models agree on it), {H2} ({H2_N}); and the brand's naming rate "
    "in these answers, {H3} ({H3_N}). The plan counts a score as separate at {BAND_LO} or "
    "below and as not separate at {BAND_HI} or above.",
    "The score computed on two halves of seven situations each correlated at {H4_R} across {H4_N} brands, a "
    "split-half reliability of {H4_REL}; the plan required at least {REL_MIN}.",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>Situations matter.</b> The models named different brands for different buying situations, such as a "
        "gift: lists overlapped {MSIT_WITHIN} between repeats of a question, {MSIT_BETWEEN} between situations.",
        "<b>Breadth is a reading of its own.</b> The score compares how many situations a brand's mentions reach in "
        "each model with what naming blind to the situation would give for the same number of mentions. It was "
        "unrelated to Presence ({H1}), Consistency ({H2}) and how often the brand is named ({H3}), against a line "
        "of {BAND_LO} for a separate score.",
        "<b>It holds up.</b> Two halves of the situations ordered brands alike (reliability {H4_REL}; required "
        "{REL_MIN}); with Claude Opus 5.5 as one model the order held ({H8}; required {REP_MIN}).",
        "<b>A raw count would have failed.</b> The share of situations in which a brand is named followed its "
        "naming rate ({RAW_H3}) and Presence ({RAW_H1}); hence the adjustment.",
    ]),
    ("Other checks", [
        "Against Ranking the score was also apart ({H5}), reported but not counted: Ranking's own interim result "
        "was marginal. Sentiment was not compared, as no Sentiment score was registered "
        "in time. Two sensitivity checks differ: a floor of {FLOOR_HI} mentions left under {NUNITS_MIN} brands, "
        "too few to decide, and averaging only over models in which a brand's count of situations could vary put reliability between "
        "the lines. Neither "
        "replaces the result.",
    ]),
    ("What it means for a marketer", [
        "Coverage asks what Presence cannot: whether a brand's naming in AI answers spreads across the situations "
        "in which people buy, or stays tied to a few. It does not follow how often a brand is named, so being named "
        "more does not by itself raise it. It covers only the brands on each category's fixed list, in US English with search off, and one set of "
        "{CEP_PER_CAT} situations per category, none weighted by how common it is among buyers.",
    ]),
    ("How the result was reached", [
        "In all, {CEPS} questions without a brand name, {CEP_PER_CAT} per category and two for each of seven kinds of "
        "situation (why, when, where, while, with whom, with what, how feeling), were asked three times each to the "
        "newest flagship model of three providers and to Claude Opus 5.5: {CALLS} of {CALLS_EXP} calls answered, "
        "five categories, {BRANDS} brands. A brand is scored when the panel names it at least {FLOOR} times and at "
        "least {MINMOD} models name it; {H1_N} brands qualified. Presence and Consistency come from the same panel's "
        "answers in the programme's fourth wave. The plan was locked before the first call; the scorer ran once.",
    ]),
    ("What comes next", [
        "Coverage passes to a second paper on the same frozen questions, coder and scorer. It starts with how much "
        "the score depends on the choice of situations, and which brands are broad and which are tied to a few.",
    ]),
]

NOTES_P2 = [
    "Data: {CALLS} answers collected for this study without tools or search, from Claude Fable 5.2, GPT-6 Astra and "
    "Gemini 4 Argon (the primary panel) and Claude Opus 5.5; {SPEND}. Categories and brands of earlier studies: "
    "audiophile headphones, skincare, cosmetics, cars and premium spirits. Correlations are Spearman rank "
    "correlations within category.",
    "Pre-registered at tag v1.12-prereg-r1, deposited on OSF before the first call. Paper, data and code: "
    "osf.io/ec6wh, folder methodology/v1_12 (Coverage of Buying Situations in AI Answers about Brands, AIAS™ "
    "Methodology v1.12).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the study's verdict file "
               "(osf/methodology/v1_12/v112_verdicts.json) and the locked scorer's constants; none is typed.")

DISCLOSURES = {
    "conflicts_of_interest": (
        "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
        "Declarations. The headphones registry includes Denon, which has belonged to the employer's group since "
        "September 23, 2025 (through Harman International); it had replaced AKG, another group brand, before that "
        "study's lock, and its group ownership was noticed only on November 10, 2026. Every gate result was "
        "recomputed without Denon, with {SD_SAME}. In cars, group subsidiaries supply components (tier 2/3) to "
        "several registry brands. {CHEIL} These brands stay in every analysis as locked. The situation questions "
        "name no brand, and headphone situations stay inside audiophile listening, away from the uses where group "
        "brands compete; brands outside the registries, which may include group brands, are not counted."),
    "held_out_brands": ("No brand was held out or added: the study used the {BRANDS} brands of five registries "
                        "fixed in earlier studies, unchanged."),
    "ai_use": "{AI_USE}",
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
