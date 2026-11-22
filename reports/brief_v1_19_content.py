"""
Text of the Coverage Paper B brief (TS-BR-v1.19-r1). Managerial register: plain findings, no hypothesis labels.
Every number is a {KEY} placeholder filled by reports/build_brief_v1_19.py from brief_v1_19_values.py (unknown key
-> KeyError). Note markers are {N1}, {N2}, ... (small_print.NoteSeq, numbered per page).
"""

TITLE = "Coverage works as one breadth score, with moderate reliability and no brand types"
KICKER = "BRIEF · COVERAGE PAPER B"
RUNNING_LABEL = "AIAS™ Methodology v1.19 · November 2026"

STANDFIRST = ("In a re-reading of Coverage Paper A's answers, the brand order held only moderately across other ways of "
              "halving the situations{N1}. Brands an earlier model panel rarely named were not tied to particular situations{N2}, "
              "and a brand's lean towards a kind of situation did not repeat{N3}, so no brand types are reported.")

NUMBERS = [
    {"value": "{REL_MED}", "unit": "", "label": "Reliability over {SPLITS} ways to halve the situations",
     "source": "Required {REL_LINE}; Paper A's own split {REL_A}"},
    {"value": "{DELTA_ABS}", "unit": "", "label": "Size of the gap for rarely named brands",
     "source": "Cliff's delta; no gap below {D_FALS}"},
    {"value": "{IL_N}", "unit": "", "label": "Brands with an identity-load reading",
     "source": "Required {IL_FLOOR}; question not tested"},
]

NOTES_P1 = [
    "Each split puts one situation of each kind in each half; {SPLIT_NMIN} to {SPLIT_NMAX} brands were rated on both "
    "halves. The median correlation of the halves, {MED_R}, gives a reliability of {REL_MED}, and a tenth of the "
    "splits fall below {P10}. The plan required at least {REL_LINE}, with a tenth of splits at {P10_LINE} or more. "
    "Paper A's split ({REL_A}) is at the {PCTL_A}th percentile.",
    "Cliff's delta of the Coverage score, within category, between the {N_FLAG} rated brands on the programme's list "
    "of brands rarely named in general questions and the {N_OTHER} other rated brands: {DELTA}; with Presence "
    "removed, {DELTA_RES}. The plan counts a delta under {D_FALS} as no difference and {D_CONF} or more as one.",
    "Mean over the seven kinds of situation of the correlation between each brand's lean in one half and in the "
    "other, over {REP_N} brands: {REP_R}, from {REP_MIN} to {REP_MAX} by kind. The plan required at least "
    "{REPL_LINE}; below {REPL_LOW}, no typology is reported.",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>Reliability is moderate.</b> Over all {SPLITS} ways of halving the situations, the halves agreed less "
        "than in Paper A's one split: {REL_MED} against {REL_A}, with {REL_LINE} required. Dropping any one kind of "
        "situation kept the brand order ({CUE_MIN} to {CUE_MAX}); only \"with what\" fell below the reference "
        "range ({CUE_P5}), within the one allowed.",
        "<b>Rarely named brands are not tied to situations.</b> The {N_FLAG} rated brands that an earlier six-model "
        "panel rarely named in general questions spread over situations like the {N_OTHER} others ({DELTA}; {DELTA_RES} with Presence "
        "removed). The result rests on those {N_FLAG} brands and does not rule out such a link in larger panels.",
        "<b>Two questions stay open.</b> None of the {DEF_ANS} answers about cars named a defunct brand, so their "
        "situations could not be compared. Only {IL_N} brands had an eligible identity-load reading, against "
        "{IL_FLOOR} required, so whether culture-led brands are named in fewer situations was not tested.",
        "<b>No brand types.</b> A brand's lean towards one kind of situation did not repeat in the other situation "
        "of the same kind ({REP_R}; required {REPL_LINE}), so, as the plan requires, no typology is reported.",
    ]),
    ("How firm it is", [
        "These checks are reported beside the result and do not replace it. Both tests on rarely named brands could "
        "not be decided whenever one of the {N_FLAG} brands dropped out, and at a lower rating floor the main one is "
        "marginal. The reliability test fails with an alternative form of the score and cannot be decided without spirits.",
    ]),
    ("What it means for a marketer", [
        "Coverage reads as one number: how widely AI answers name a brand across buying situations. On "
        "{CEP_PER_CAT} situations per category it orders brands only moderately reliably, so small differences "
        "between brands should not be read as precise. Nothing here supports brand types with their own situation profiles.",
    ]),
    ("How the result was reached", [
        "No new model call: the study re-read Paper A's answers from Claude Fable 5.2, GPT-6 Astra and Gemini 4 "
        "Argon for {RATED} rated brands in five categories, with Paper A's score and rules unchanged. Pre-registered "
        "before Paper A's first call and run once after Paper A passed, its tests are confirmatory.",
    ]),
    ("What comes next", [
        "An independently written set of situations with buyer weights, and new question wordings, need new "
        "collections under their own pre-registrations.",
    ]),
]

NOTES_P2 = [
    "Data: Paper A's answers of its three-model panel, search off, in five categories (audiophile headphones, "
    "skincare, cosmetics, cars, premium spirits). Rarely named brands: the programme's frozen recall-floor list from "
    "an earlier six-model panel. Identity load: the same models' answers in the fourth wave, in skincare, cosmetics "
    "and cars.",
    "Pre-registered at tag v1.19-prereg-r1, deposited on OSF before Paper A's first call. Paper, data and code: "
    "osf.io/ec6wh, folder methodology/v1_19 (Situation Sampling, Phantom Brands, Identity Load and Brand Profiles in "
    "AI Coverage Answers, AIAS™ Methodology v1.19).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the study's verdict file "
               "(osf/methodology/v1_19/outputs/v119_verdicts.json) and the locked scorer's constants; none is typed.")

DISCLOSURES = {
    "conflicts_of_interest": (
        "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
        "Declarations. The headphones registry includes Denon, which has belonged to the employer's group since "
        "September 23, 2025 (through Harman International); it had replaced AKG, another group brand, before that "
        "study's lock, and its group ownership was noticed only on November 10, 2026. In cars, group subsidiaries "
        "supply components (tier 2/3) to several registry brands. {CHEIL} These five brands and Denon stay in every "
        "analysis; every test was also run without them, which left both tests on rarely named brands undecided "
        "(one of their {N_FLAG} brands drops out) and changed no other verdict. The situation questions name no "
        "brand, and headphone situations stay inside audiophile listening, away from the uses where group brands "
        "compete; brands outside the registries are not counted. This study made no model call."),
    "held_out_brands": ("No brand was held out or added: the study re-read answers about the {BRANDS} brands of "
                        "five registries fixed in earlier studies."),
    "ai_use": "{AI_USE}",
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
