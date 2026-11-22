"""
Text of the v0.43 predictive-validity brief (TS-BR-v0.43-r1; Stage 1, a test on past data). Managerial register:
plain findings, no hypothesis labels. Every number is a {KEY} placeholder filled by reports/build_brief_v0_43.py from
brief_v0_43_values.py (unknown key -> KeyError). Note markers are {N1}, {N2}, ... (small_print.NoteSeq, per page).
"""

TITLE = "Brands AI answers named more in June did not gain more search interest later"
KICKER = "BRIEF · PREDICTIVE VALIDITY, STAGE 1"
RUNNING_LABEL = "AIAS™ v0.43 · November 2026"

STANDFIRST = ("A pre-registered test on past data asked whether brands that AI answers named more in June 2026 "
              "gained more US Google search interest by November than brands of the same category and the same "
              "June search level{N1}. They did not: the link was negative, and the data rule out even a small "
              "positive one{N2}. The forward test{N3}, on weeks still to come, is set for March 2027.")

NUMBERS = [
    {"value": "{RHO_P_ABS}", "unit": "", "label": "Size of the negative link between June Presence and later change",
     "source": "Value {RHO_P}; 90% upper end {HI_P}, under {FALS}"},
    {"value": "{CONC}", "unit": "", "label": "Same-time link of Presence and search level",
     "source": "Check passed; at least {CONC_LINE} required"},
    {"value": "{N_P}", "unit": "", "label": "Brands with a defined change in search",
     "source": "Of {UNITS}; at least {MIN_N} needed for a test"},
]

NOTES_P1 = [
    "Presence: how often a fixed panel of six AI models recognises and names a brand, scored in June 2026 and "
    "locked before this study. Search interest: Google Trends, United States, web search, requested only after the "
    "pre-registration was locked, in three pulls of size-matched bundles that agreed closely (mean {REL}; at least "
    "{REL_LINE} required).",
    "Within-category partial rank correlation of June Presence with the change in search interest, holding June "
    "search level fixed: {RHO_P}, 90% interval {LO_P} to {HI_P}, over {N_P} brands. The plan confirms at {CONF} or "
    "more with one-sided p below {ALPHA}, falsifies when the upper end of the 90% interval is below {FALS}, and "
    "needs at least {MIN_N} brands ({MIN_N_C} for Consistency).",
    "Stage 2 repeats the test from the November 2026 scores to search interest in early March 2027, locked in the "
    "same pre-registration before any of its outcome weeks had happened. A predictive-validity claim rests on it.",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>June Presence did not predict a gain.</b> If anything, brands that AI answers named more in June "
        "gained less search interest by November ({RHO_P}; 90% interval {LO_P} to {HI_P}): the main test is "
        "falsified. "
        "The negative link fell short of the plan's bar for a reversal (two-sided p {P2_P}, {ALPHA} needed).",
        "<b>A seasonal adjustment changes nothing.</b> Against each brand's own previous year: {RHO_SA} over "
        "{N_SA} brands, upper end {HI_SA}, falsified.",
        "<b>With the earlier trend held fixed, it counts as reversed.</b> Also holding the February-to-June change "
        "fixed: {RHO_M} (two-sided p {P2_M}), falsified and labelled reversed, which the plan counts as support "
        "for AI availability lagging demand. It is one secondary test, with no correction for four tests.",
        "<b>Consistency is undecided.</b> Among {N_C} brands with a Consistency score (how evenly the models name "
        "a brand), at equal Presence: {RHO_C}, interval {LO_C} to {HI_C}, undetermined.",
    ]),
    ("How firm it is", [
        "Every check passed and no verdict carries a flag: Presence and June search level went together "
        "({CONC}), the pulls agreed ({REL}), and {TOPIC} of brands were searched as Google topics rather than "
        "plain words. Without the five defunct car brands ({D_DEFUNCT}), with recall alone ({D_RECALL}), with May "
        "scores ({D_LEAD}) or with topic terms only ({D_TOPIC}), the link stays negative; these carry no verdict.",
    ]),
    ("What it means for a marketer", [
        "On this evidence, Presence measures how available a brand is in AI answers now; it is not a leading "
        "indicator of search demand. Search interest is a trace of people looking for a brand, not of buying it, "
        "and this is a test on past data.",
    ]),
    ("How the result was reached", [
        "No model call: the June scores of {UNITS} brand units in five categories, already locked, were set against "
        "search interest requested after the lock. Ranks are taken within each category, with June search level "
        "held fixed; p-values come from shuffling and intervals from resampling brands.",
    ]),
    ("What comes next", [
        "Stage 2, the forward test, uses the November 2026 scores and search interest to early March 2027.",
    ]),
]

NOTES_P2 = [
    "Data: the programme's five registries (audiophile headphones, skincare, cosmetics, cars, premium spirits), "
    "scored on the legacy six-model panel; US Google search interest by brand, as a topic where one matched and "
    "otherwise as a plain search term; brands too rarely searched for a defined change leave the tests.",
    "Pre-registered at tag v0.43-prereg-r1, deposited on OSF before any search-interest request. Pre-registration, "
    "data and code: osf.io/ec6wh, folder v43 (AI Availability Scores and Later Change in Brand Search Interest, "
    "AIAS™ v0.43, Stage 1).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the study's verdict file "
               "(osf/v43/v43_stage1_verdicts.json) and the locked scorer's decision lines; none is typed.")

DISCLOSURES = {
    "conflicts_of_interest": (
        "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
        "Declarations. The headphones registry includes Denon, which has belonged to the employer's group since "
        "September 23, 2025 (through Harman International); it had replaced AKG, another group brand, before that "
        "study's lock, and its group ownership was noticed only on November 10, 2026. In cars, group subsidiaries "
        "supply components to several registry brands. {CHEIL} These brands stay in the registries and the "
        "analysis as locked. Collection and scoring are automated, and the pre-registration was locked and "
        "deposited before any search-interest request."),
    "held_out_brands": ("No brand was held out or added: the study uses the {UNITS} brand units of five registries "
                        "fixed in earlier studies."),
    "ai_use": "{AI_USE}",
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
