"""
Text of the Sentiment Paper A brief (TS-BR-v1.20-r1). Managerial register: plain findings, no hypothesis labels.
Every number is a {KEY} placeholder filled by reports/build_brief_v1_20.py from brief_v1_20_values.py (unknown key
-> KeyError). Note markers are {N1}, {N2}, ... (small_print.NoteSeq, numbered per page).
"""

TITLE = "Sentiment in AI answers can be measured reliably, but it is not yet a score of its own"
KICKER = "BRIEF · SENTIMENT PAPER A"
RUNNING_LABEL = "AIAS™ Methodology v1.20 · November 2026"

STANDFIRST = ("Two AI judges from different providers agree on how AI answers describe brands{N1}, and the reading "
              "holds over months{N2}. But warmer descriptions go with brands the models already name more often{N3}, "
              "so Sentiment is reported and redesigned, not added to the AIAS™ score.")

NUMBERS = [
    {"value": "{ALPHA}", "unit": "", "label": "Agreement between two AI judges",
     "source": "Krippendorff's alpha; {PAIRS} passages"},
    {"value": "{H6}", "unit": "", "label": "Brand order kept over five months",
     "source": "Rank correlation; {H4} over three weeks"},
    {"value": "{H2_t3}", "unit": "", "label": "Overlap with Presence, third wave",
     "source": "Not separate at {BAND_HI} or above; {H2_t3_N} brands"},
]

NOTES_P1 = [
    "Ordinal agreement between Claude Opus 5.5 and GPT-6.1 Sol on the {PAIRS} passages both rated (the plan required "
    "at least {ALPHA_MIN}); on brand scores the two judges' rank correlation was {BRHO} ({BRHO_N} scores; required "
    "{BRHO_MIN}).",
    "Within-category rank correlation of each brand's score between waves: {H4} over three weeks ({H4_N} brands) and "
    "{H6} over five months ({H6_N} brands); the plan required {STAB_MIN}.",
    "Within-category rank correlation with Presence: {H2_t1}, {H2_t2} and {H2_t3} at the three waves. The plan counts "
    "a score as separate at {BAND_LO} or below at every wave and as not separate at {BAND_HI} or above at any wave.",
]

# ---------------------------------------------------------------- page 2
KICKER_P2 = "WHAT WE FOUND AND WHAT IT MEANS"

SECTIONS = [
    ("What we found", [
        "<b>The reading is reliable.</b> Two AI judges from different providers rated how warmly passages of AI "
        "answers describe a brand. They agreed closely ({ALPHA} on passages, {BRHO} on brand scores), and the "
        "primary judge did not favour answers written by its own provider's models.",
        "<b>It is stable.</b> Brands kept their order: {H4} over three weeks and {H6} over five months.",
        "<b>It is distinct from Consistency.</b> Tone has almost nothing to do with how evenly the models name a "
        "brand (at most {H3_MAX} at any wave).",
        "<b>It is not distinct from Presence.</b> Within each category, the brands the models name more often are "
        "described more warmly. The correlation with Presence was {H2_t1}, {H2_t2} and {H2_t3} at the three waves; "
        "the plan set {BAND_HI} as the line at which Sentiment is not a separate score, and the third wave reached "
        "it. In {N_EARLY_CATS} earlier categories, answered by another panel of models, the score also rose with how "
        "often a brand is named ({H7}), and it partly overlaps with Ranking ({H5_MIN} to {H5_MAX}).",
        "<b>The miss is narrow.</b> Without the {CUT_ANSWERS} answers cut off at the answering model's length "
        "limit, the third-wave figure is {SCUT_T3}, just under the line. Such checks are reported beside the result "
        "and do not replace it, and none placed Sentiment clearly apart from Presence. Per the plan, it is reported "
        "and redesigned rather than shipped as a separate score.",
    ]),
    ("What it means for a marketer", [
        "How AI answers describe a brand can be read consistently, and the reading does not swing from month to "
        "month. But a warm description is largely a by-product of being present: the brands the models already "
        "name are the ones they describe well, so a separate Sentiment number would mostly repeat Presence. Treat "
        "tone as part of the Presence picture, not as a second lever. The ratings are made by AI judges and are "
        "not yet checked against human readers.",
    ]),
    ("How the result was reached", [
        "The study's own judging rule (v1.11) accepted a reply only if the whole reply was one block of structured "
        "data. The primary judge sometimes put a short sentence before a complete reply, so {V111_FAIL} of {UNITS} "
        "passages ({V111_SHARE}) failed, above the {HALT} stop line in {V111_HALTS} of {SETS} answer sets, and the "
        "study stopped without a score, as its plan required. A successor rule (v1.20), registered before any reply "
        "existed, counts a reply that holds exactly one complete, valid block. Applied once to the same stored "
        "replies, all else unchanged, it left {V120_FAIL} failures; the results here are v1.20's.",
    ]),
    ("What comes next", [
        "Sentiment does not enter the AIAS™ score. Two paths are open, and the choice is a later decision by the "
        "author: a redesigned measure under its own pre-registration, or reporting tone within Presence without a "
        "separate score. A companion study (Paper B) compares the AI judges with human readers.",
    ]),
]

NOTES_P2 = [
    "Data: archived answers, no new collection: five categories (headphones, skincare, cosmetics, cars, spirits) at "
    "three waves from a six-model panel, and {N_EARLY_CATS} earlier categories from a second six-model panel. Claude "
    "Opus 5.5 rated {UNITS} passages on a five-point scale, GPT-6.1 Sol {PAIRS} of them; {CALLS} batch calls, "
    "{SPEND}. A brand is scored with at least {NFLOOR} rated passages. Correlations are Spearman rank correlations "
    "within category.",
    "Pre-registered at tags v1.11-prereg-r1 and v1.20-prereg-r1, both deposited on OSF before the first judge call. "
    "Paper, data and code: osf.io/ec6wh, folder methodology/v1_20 (Sentiment in AI Answers about Brands, AIAS™ "
    "Methodology v1.11 scored under v1.20).",
]

SOURCE_LINE = ("Every number in this brief is read by code from the study's output files "
               "(osf/methodology/v1_20/outputs/v1_20_verdicts.json and its companions); none is typed.")

DISCLOSURES = {
    "conflicts_of_interest": (
        "The author is employed by a consumer-electronics company; it and its affiliates are named in the paper's "
        "Declarations. The headphones registry includes Denon, which has belonged to the employer's group since "
        "September 23, 2025 (through Harman International); it had replaced AKG, another group brand, before that "
        "study's lock, and its group ownership was noticed only on November 10, 2026. Every gate result was "
        "recomputed without Denon, with {SD_SAME}. In cars, group subsidiaries supply components (tier 2/3) to "
        "several registry brands. {CHEIL} These brands stay in every analysis as locked."),
    "held_out_brands": ("No brand was held out or added: the study re-read answers about the brands of registries "
                        "fixed in earlier studies."),
    "ai_use": ("During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with "
               "study design, analysis and writing. The author reviewed and edited all content and takes full "
               "responsibility for it."),
    "independence": ("Self-funded. No brand was contacted, sponsored the work or saw it before publication. Third "
                     "System does not accept compensation contingent on improving a brand's AI Availability Score."),
}
