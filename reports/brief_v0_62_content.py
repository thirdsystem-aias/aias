"""
Text of the non-English wave brief (TS-BR-v0.62-r1). Managerial register: plain findings, no hypothesis labels.
Every number is a {KEY} placeholder filled by reports/build_brief_v0_62.py from brief_v0_62_values.py (unknown key
-> KeyError). Note markers are {N1}, {N2}, ... (small_print.NoteSeq, numbered per page).
"""

TITLE = "Asked in Spanish, Korean or Chinese, AI models kept the English order of brands"
KICKER = "BRIEF · NON-ENGLISH WAVE"
RUNNING_LABEL = "AIAS™ v0.62 · November 2026"

STANDFIRST = ("Every AI Availability measurement so far was taken in US English. Asked the same category questions "
              "in Spanish, Korean and Chinese, the three newest flagship models named the {N_UNITS} brands of five "
              "categories in much the same order as in English{N1}. Whether the models agree on a brand held in "
              "Spanish but only weakly in Korean and Chinese{N2}. No result changed under any check{N3}.")

NUMBERS = [
    {"value": "{PRES_ES}", "unit": "", "label": "Agreement with the English order, Spanish",
     "source": "95% interval {PRES_ES_LO} to {PRES_ES_HI}; {PRES_CONF} needed"},
    {"value": "{PRES_KO}", "unit": "", "label": "Agreement with the English order, Korean",
     "source": "95% interval {PRES_KO_LO} to {PRES_KO_HI}"},
    {"value": "{PRES_ZH}", "unit": "", "label": "Agreement with the English order, Chinese",
     "source": "95% interval {PRES_ZH_LO} to {PRES_ZH_HI}"},
]

NOTES_P1 = [
    "Agreement: the within-category rank correlation (centred) between how often answers name each brand in "
    "English (the v0.42 wave, same models, no web search) and in the language asked, over {N_UNITS} brand units in "
    "audiophile headphones, skincare, cosmetics, cars and premium spirits. The plan counts {PRES_CONF} or above "
    "(with p under {ALPHA}) as the order holding and under {PRES_FALS} as not holding; permutation p {P_ES} in "
    "each language.",
    "Consistency (whether the three models agree in naming a brand), correlation with English: {PHI_ES} in Spanish "
    "({PHI_ES_N} brands with a value in both languages), {PHI_KO} in Korean ({PHI_KO_N}), {PHI_ZH} in Chinese ({PHI_ZH_N}). "
    "The plan counts {PHI_CONF} or above as holding and under {PHI_FALS} as not holding; between is marginal.",
    "Checks: without Denon ({DENON_N} units) or the headphones category ({HP_N}); without translation-flagged "
    "questions or the alias an independent AI check judged unused (no value changes); without {SLANG_ZH_X} "
    "off-language Chinese answers ({SLANG_ZH}; no Chinese answer used Traditional script); with aliases that can "
    "match other words switched off ({SALIAS_KO} Korean, {SALIAS_ZH} Chinese); and the two checks on page 2. "
    "Lowest agreement under any check: {SENS_MIN}.",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>The order of brands carried across languages.</b> Agreement with the English order was {PRES_ES} in "
        "Spanish, {PRES_KO} in Korean and {PRES_ZH} in Chinese, all above the {PRES_CONF} the plan set before any "
        "answer was collected. Within single categories it ran from {CAT_MIN} to {CAT_MAX}.",
        "<b>The level moved.</b> Spanish answers named the registry brands slightly more often than English answers "
        "(a mean difference of {DL_ES} in the share of answers naming a brand), Korean ({DL_KO}) and Chinese "
        "({DL_ZH}) answers less often. A brand's Presence in one language is not its Presence in another, even "
        "where its rank among competitors holds.",
        "<b>The second measure held in Spanish only.</b> Whether the three models agree in naming a brand carried "
        "over to Spanish ({PHI_ES}) but only weakly to Korean ({PHI_KO}) and Chinese ({PHI_ZH}): marginal, above "
        "the {PHI_FALS} that would fail it and under the {PHI_CONF} it needed.",
        "<b>Ranking was not tested</b>, because its instrument has not yet passed its own test.",
    ]),
    ("How firm it is", [
        "Checks reported beside the result change no verdict. Without the units with a disclosed tie to the "
        "author's employer, agreement is {COI106_ES}, {COI106_KO} and {COI106_ZH} on {COI_N_106} units ({COI_ES}, "
        "{COI_KO} and {COI_ZH} on the {COI_N_RUN} units as scored, where a key mismatch left Jack Daniel's in). "
        "Against the English table corrected for a coding erratum it is {CORR_ES}, {CORR_KO} and {CORR_ZH}, and "
        "the second measure in Chinese falls to {CORR_PHI_ZH}, still marginal. Other checks are in the notes on page 1.",
    ]),
    ("What it means for brands that sell in several languages", [
        "An English reading is a good guide to the order in which the same models name brands in these three "
        "languages, at least in five consumer categories and for questions that name no market. It is not a guide "
        "to the level: a brand can keep its rank among competitors and still be named less often in Korean or "
        "Chinese. Read the English order across; measure the level, and the models' agreement, in each language.",
    ]),
    ("How the result was reached", [
        "The category questions of the English wave were translated into Spanish, Korean and Simplified Chinese "
        "and asked of Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, without web search, three times each, on "
        "November 25, 2026: {CALLS} of {CALLS_SENT} planned calls answered, for {SPEND} of recorded spend against "
        "a {CAP} cap ({SPEND_STRICT} if the one call that timed out is charged at its worst case). The translations "
        "were made and checked by AI models; no native speaker reviewed them.",
    ]),
]

NOTES_P2 = [
    "Data: the Spanish, Korean and Chinese answers beside the English answers of the v0.42 wave, same models and "
    "settings; no country or market is named in any question. Correlations are centred within-category Spearman "
    "correlations with 95% bootstrap intervals. Checks added after scoring are in DEVIATIONS Entries 4 to 8.",
    "Pre-registered at tag v0.62-prereg-r1, deposited on OSF before the first call. Paper, data and code: "
    "osf.io/ec6wh, folder v62 (Does AI Brand Presence Hold Across Languages?, AIAS™ v0.62).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the study's verdict file (osf/v62/v62_verdicts.json), "
               "its post-scoring sensitivity files, the paper's cost record and the locked scorer's constants; none "
               "is typed.")

DISCLOSURES = {
    "conflicts_of_interest": (
        "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
        "Declarations. The headphones registry includes Denon, which has belonged to the employer's group since "
        "September 23, 2025 (through Harman International); it had replaced AKG, another group brand, before that "
        "study's lock, and its group ownership was noticed only on November 10, 2026. In cars, group subsidiaries "
        "supply components (tier 2/3) to several registry brands. A marketing company of the group (Cheil "
        "Worldwide) or its agency Iris has worked for Chevrolet, BMW, Bentley, Jack Daniel's and Eucerin; further "
        "supply contracts and duty-free retail are listed in the paper. Korean is the group's home-market "
        "language; only registry brands are coded. These brands stay in every analysis as locked, and every result "
        "is also reported without them."),
    "held_out_brands": ("No brand was held out or added: the study asked about the {N_UNITS} brand units of five "
                        "registries fixed in earlier studies."),
    "ai_use": "{AI_USE}",
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
