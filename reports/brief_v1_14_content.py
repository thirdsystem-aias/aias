"""
Text of the Ranking closing brief (TS-BR-v1.14-r1; the combined v1.14 + v1.16 paper). Managerial register: plain
findings, no hypothesis labels. Every number is a {KEY} placeholder filled by reports/build_brief_v1_14.py from
brief_v1_14_values.py (unknown key -> KeyError). Note markers are {N1}, {N2}, ... (small_print.NoteSeq, per page).
"""

TITLE = "Where AI answers place a brand is stable, but it tracks Presence"
KICKER = "BRIEF · RANKING CLOSING PAPER (v1.14 AND v1.16)"
RUNNING_LABEL = "AIAS™ Methodology v1.14 and v1.16 · November 2026"

STANDFIRST = ("Two pre-registered re-analyses asked whether the place a brand takes among the brands an AI answer "
              "names is a score of its own. The order held over three weeks{N1} and was distinct from Consistency "
              "(how evenly the models name a brand), but it moved too closely with Presence (how often they name "
              "it) at two of four waves{N2}, so, as fixed before the run{N3}, "
              "Ranking is reported as part of Presence.")

NUMBERS = [
    {"value": "{H3}", "unit": "", "label": "Brand order kept over three weeks",
     "source": "Required {STAB_CONF}; order shuffled {SHUF}"},
    {"value": "{P_MAX}", "unit": "", "label": "Highest link with Presence over four waves",
     "source": "Separate score needs {SEP_CONF} or less at each"},
    {"value": "{M_H1}", "unit": "", "label": "The earlier measure's link with Presence",
     "source": "Most frequent position, newest panel; {SEP_CONF} needed"},
]

NOTES_P1 = [
    "Precedence: for each pair of brands named in the same answer, the one named first wins; a standard model for "
    "paired comparisons (Bradley–Terry) turns the wins into one strength per brand, category and wave. Correlation "
    "of the brand order from the first to the second wave, within category, over {H3_N} brands: {H3}; with the "
    "order shuffled inside each answer, {SHUF}. The plan required at least {STAB_CONF} and both chance tests below "
    "{ALPHA} (both {H3_P}).",
    "Within-category correlation with Presence at the four waves: {P1}, {P2}, {P3} and {P4}. The plan counts a "
    "brand-level score as separate only at {SEP_CONF} or less at every wave and as failing at {SEP_FALS} or more "
    "at any; in between is marginal.",
    "The consequence was fixed before the run: if the test did not pass, Ranking is reported as part of Presence "
    "and not as a separate AIAS component, and there is no further Ranking redesign.",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>The order among co-named brands is stable.</b> Which brand comes first among brands named together "
        "held over three weeks ({H3}; {STAB_CONF} required) and five months ({H5}). Shuffling the order inside each "
        "answer removes it ({SHUF}), so it lies in the order, not the brand mix.",
        "<b>It is distinct from Consistency</b>, how evenly the models name a brand: at most {C_MAX} at every "
        "wave.",
        "<b>It is not clear of Presence.</b> Its correlation with how often a brand is named was {P1}, {P2}, {P3} "
        "and {P4}: inside the {SEP_CONF} line at two waves, short of {SEP_FALS} at the other two; {H4} with search "
        "on. The test is marginal: brands named more often tend to come first.",
        "<b>The earlier measure did no better.</b> A brand's most frequent position, tested on a wave it had not "
        "seen, was distinct from Consistency ({M_H2}) but linked to Presence at {M_H1} ({M_S1} with search on): "
        "marginal.",
    ]),
    ("How firm it is", [
        "Checks reported beside the result, which cannot change it. Counting only brands with ten or more "
        "rankable mentions ({F10_1} and {F10_2} at the first two waves), or leaving out spirits ({NOSP_2} and "
        "{NOSP_3}), the Presence test fails; without cars it passes (at most {NOCAR_MAX}); ranks not centred by category make "
        "the Consistency test marginal ({UNC_1}). For the earlier measure, a floor of ten ({M_F10}) and the "
        "top-position variant ({M_TOP1}) pass. Without the brands in the Disclosures, no verdict changes.",
    ]),
    ("What it means for a marketer", [
        "As fixed before the run, Ranking is reported as part of Presence and not as a separate AIAS component, "
        "and there is no further Ranking redesign. Where a brand comes among its rivals remains a fair description "
        "of how a model presents it, but it is not added to the score. A reader with a looser bar could decide "
        "otherwise on the same numbers.",
    ]),
    ("How the result was reached", [
        "No new model call: both studies re-read archived answers in five categories, three waves of a six-model "
        "panel and one wave of the newest panel (Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon; {ANSWERS} "
        "answers). Each was pre-registered and run once; {U_MIN} to {U_MAX} brands with at least {FLOOR} "
        "rankable mentions were rated per wave.",
    ]),
    ("What comes next", [
        "No Ranking redesign follows. The newest panel's retest on a fifth wave runs for the record and cannot "
        "change the verdict.",
    ]),
]

NOTES_P2 = [
    "Data: archived answers to category questions in five categories (audiophile headphones, skincare, cosmetics, "
    "cars, premium spirits), {BRANDS} registry brands; Presence and Consistency from the programme's locked "
    "tables. Positions count registry brands only.",
    "Pre-registered at tags v1.14-prereg-r2 and v1.16-prereg-r1, each deposited on OSF before its run. Data and "
    "code: osf.io/ec6wh, folders methodology/v1_14 and methodology/v1_16 (Precedence Without Separation: Closing "
    "the Ranking Component of AI Brand Availability, AIAS™ Methodology v1.14 and v1.16).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the studies' result files "
               "(osf/methodology/v1_16/outputs/results_v1_16.json, osf/methodology/v1_14/outputs/stage1/"
               "stage1_v1_14.json) and the locked scorer's constants; none is typed.")

DISCLOSURES = {
    "conflicts_of_interest": (
        "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
        "Declarations. The headphones registry includes Denon, which has belonged to the employer's group since "
        "September 23, 2025 (through Harman International); it had replaced AKG, another group brand, before that "
        "study's lock, and its group ownership was noticed only on November 10, 2026. In cars, group subsidiaries "
        "supply components to several registry brands. {CHEIL} These five brands and Denon stay in every "
        "analysis; the tests were also run without Denon (both studies) and without all six (v1.16), and no "
        "verdict changed. Both studies re-read answers to questions fixed in earlier studies and made no model "
        "call."),
    "held_out_brands": ("No brand was held out or added: both studies re-read answers about the {BRANDS} brands of "
                        "five registries fixed in earlier studies."),
    "ai_use": "{AI_USE}",
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
