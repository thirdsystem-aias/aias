"""
Text of the Grounding Paper A brief (TS-BR-v1.13-r1). Managerial register: plain findings, no hypothesis labels.
Every number is a {KEY} placeholder filled by reports/build_brief_v1_13.py from brief_v1_13_values.py (unknown key
-> KeyError). Note markers are {N1}, {N2}, ... (small_print.NoteSeq, numbered per page).
"""

TITLE = "How often AI search finds a brand's own site is not yet a measure of its own"
KICKER = "BRIEF · GROUNDING PAPER A"
RUNNING_LABEL = "AIAS™ Methodology v1.13 · November 2026"

STANDFIRST = ("When AI models search the web to answer category questions, the sources they retrieve include a "
              "brand's own website for only some brands{N1}. A score of that share stayed apart from Consistency "
              "but overlapped Presence more than the plan allows{N2}, and too few brands were scored run by run to "
              "test whether it repeats{N3}. The pre-registered gate is marginal.")

NUMBERS = [
    {"value": "{H1_S0}", "unit": "", "label": "Overlap of the score with Presence",
     "source": "Separate at {SEP_LO} or below; {H1_S1} with search on"},
    {"value": "{N_RATED}", "unit": "", "label": "Brands with enough grounded answers to score",
     "source": "Of {UNITS}; at least {FLOOR_G} answers each"},
    {"value": "{ZERO_NUM}", "unit": "%", "label": "Scored brands whose own site was never retrieved",
     "source": "Median score by category {MED_MIN} to {MED_MAX}"},
]

NOTES_P1 = [
    "Grounding score: of the answers naming a brand whose search returned a source, the share whose sources "
    "include one of its own domains (a list fixed before any answer was read). Over {ANSWERS} search-on category "
    "answers; a brand is scored with at least {FLOOR_G} such answers.",
    "Within-category rank correlation of the score with Presence (how often AI answers name the brand): {H1_S1} "
    "with search on, {H1_S0} with search off ({H1_N} brands); with Consistency (how far the models agree on it): "
    "{H2_S1} and {H2_S0} ({H2_N1} and {H2_N0} brands). The plan counts a score as separate when both are at "
    "{SEP_LO} or below and as not separate at {SEP_HI} or above.",
    "Each run's score (at least {FLOOR_RUN} such answers in the run) needed {FLOOR_UNITS} brands scored in both "
    "runs of a pair; the three pairs had {PAIR_MIN} to {PAIR_MAX}.",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>Own sites are a small part of what search returns.</b> For {ZERO_PCT} of the {N_RATED} scored brands, "
        "no answer's sources held the brand's own site; the median score by category ran from {MED_MIN} to "
        "{MED_MAX}. {MQ3_PCT} of the domains retrieved could be classed only as other or not at all, so the mix "
        "of source types is described only roughly.",
        "<b>Apart from Consistency, not clearly apart from Presence.</b> The score was unrelated to Consistency "
        "({H2_S1} and {H2_S0}) but overlapped Presence at {H1_S1} with search on and {H1_S0} with search off: "
        "under the {SEP_HI} that would fail it, above the {SEP_LO} a separate score must meet.",
        "<b>Whether it repeats could not be tested.</b> Scored run by run, no pair of runs had {FLOOR_UNITS} "
        "brands in common (at most {PAIR_MAX}), so reliability is undetermined.",
        "<b>Other components.</b> Against Coverage the overlap was {H6} ({H6_N} brands), between the lines; it "
        "counts toward the gate and leaves it marginal. Against Ranking it was {H4}, reported only, as Ranking's "
        "own interim result was marginal; two sensitivity variants read it as marginal. Sentiment was not "
        "compared: no score on these answers was registered in time.",
        "<b>Structured data stays open.</b> An audit of the brands' own sites and Wikidata records left only "
        "{H7_N} brands with both readings, under the {FLOOR_UNITS} needed, so its link to the score was not tested.",
    ]),
    ("How firm it is", [
        "These checks are reported beside the result and do not replace it. With a floor of {FLOOR_S3} answers "
        "the overlap with Presence reaches {S4_3_H1_S0}, which would fail the gate; at {FLOOR_S10}, too few "
        "brands remain to decide. Gemini 4 Argon's search returned sources for only {GEM_PCT} of its answers "
        "(flagged); dropping it changes no verdict. A brand-site list widened by the audit changes none either, "
        "though it took {S6_N_BARE} bare country endings such as co.th as brand sites (a recorded deviation).",
    ]),
    ("What it means for a marketer", [
        "On this evidence, how often AI search lands on a brand's own website is not yet a separate reading of AI "
        "availability: it partly follows how often the brand is named. It is reported beside Presence and "
        "Consistency, not combined with them. A low score can reflect a site closed to automated visitors.",
    ]),
    ("How the result was reached", [
        "No model call: the study re-read the stored search-on answers of the programme's fourth wave, six "
        "category questions per category in three runs, for {UNITS} brand units in five categories, with a "
        "source rule and a brand-domain list frozen before any search record was read. Presence and Consistency "
        "come from the same wave.",
    ]),
    ("What comes next", [
        "A second paper follows only on the author's recorded decision, testing first the two conditions not "
        "met here: Presence and run-to-run reliability.",
    ]),
]

NOTES_P2 = [
    "Data: the search-on category answers of Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon in the fourth "
    "wave, in audiophile headphones, skincare, cosmetics, cars and premium spirits; every source the search "
    "returned counts, cited or not. Correlations are Spearman rank correlations within category.",
    "Pre-registered in two parts, at tags v1.13-prereg-r1 (deposited on OSF before any search record was read) "
    "and v1.13-audit-r1. Paper, data and code: osf.io/ec6wh, folder methodology/v1_13 (Grounding: What Search-On "
    "AI Answers about Brands Retrieve, AIAS™ Methodology v1.13).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the study's verdict file "
               "(osf/methodology/v1_13/v1_13_verdicts.json), its sensitivity file and the locked scorer's "
               "constants; none is typed.")

DISCLOSURES = {
    "conflicts_of_interest": (
        "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
        "Declarations. The headphones registry includes Denon, which has belonged to the employer's group since "
        "September 23, 2025 (through Harman International); it had replaced AKG, another group brand, before that "
        "study's lock, and its group ownership was noticed only on November 10, 2026. Denon had too few grounded "
        "answers to be scored, and every gate result without it is unchanged. In cars, group subsidiaries supply "
        "components (tier 2/3) to several registry brands. These brands stay in every analysis as locked. The "
        "audit read every brand's public pages under the same rules and contacted no brand."),
    "held_out_brands": ("No brand was held out or added: the study re-read answers about the {UNITS} brand units of "
                        "five registries fixed in earlier studies."),
    "ai_use": "{AI_USE}",
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
