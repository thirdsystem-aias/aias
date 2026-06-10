# NOTE: cloned from v33_provider_asymmetry_content.py on phase scaffold.
# All COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, PATTERNS,
# LIMITATIONS, WHATS_NEXT, HYPOTHESIS_DETAILS, CLOSING text
# must be re-written for the v0.34 longitudinal t1-t2 omnibus
# substrate. Do not ship this file as-is.

"""
v0.34 - Provider-Asymmetric CPC - Brand-format report content module.
Third System(TM) managerial register (P1-P5 propositional framing).

Replaces the stale v0.32 clone. Authored against the locked verdicts
(osf/v34/v34_longitudinal_t1_t2_omnibus_verdicts.json; commit fdceda9). Honest framing:
  P1 - a real but faint provider fingerprint on recall consistency;
  P2 - the "beyond recognition" question could NOT be answered (recognition saturated);
  P3 - no provider is reliably the steadiest (unresolved, underpowered);
  P4 - the faint-brand pattern is mechanical, not a signature;
  P5 - the provider lens is informative only outside saturated recognition (the central lesson).

Register: brand editorial voice, P1-P5 propositions (no H_* notation). No Samsung anywhere
(the COI disclosure lives in the SSRN paper's Declarations, not in this report). Statistics
are translated to plain language; no Greek, subscripts, or logical operators, to stay clear
of the Akkurat glyph gaps the builder otherwise has to patch.

The 11 standard attributes follow: COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY,
WHAT_WE_MEASURED, PATTERNS, LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING,
HYPOTHESIS_DETAILS, CLOSING. (Prose attributes are strings; the two scoring attributes are
lists of dicts - align types to build_report_v34.py when the builder is rewritten.)
"""

COVER = {
    "title": "The Provider Fingerprint",
    "subtitle": (
        "Does the company that built an AI model leave a systematic mark on how "
        "consistently it recalls brands? A pre-registered re-analysis across five "
        "categories finds a real but faint signal - and a measurement blind spot "
        "worth naming."
    ),
}

STANDFIRST = (
    "Three companies build the large language models most brands are now seen "
    "through. We asked whether that authorship shows up as a consistent pattern in "
    "how brands are recalled - and found that the more useful answer was about the "
    "question we could not yet ask."
)

LEAD_DECK = (
    "AI Availability - how a brand surfaces inside large language models - is the "
    "third front of brand availability, alongside the mental and physical "
    "availability marketers already manage. Within it, Consistency asks how steadily "
    "a brand is recalled across the models people actually use. Holding the models "
    "fixed at a single moment, this study asked a narrower question: does the "
    "provider behind a model - Anthropic, OpenAI, or Google - leave a systematic "
    "fingerprint on that consistency?"
)

EXEC_SUMMARY = (
    "The short answer is yes, but faintly - and the more important answer is that we "
    "could not test the question that matters most.\n\n"
    "Across 112 brands in five categories, which provider built a model does explain "
    "a real, repeatable share of the variation in how consistently brands are "
    "recalled. The effect is reliable but small: provider sits just above what the "
    "structure of the test would produce by chance, and no further.\n\n"
    "We then asked the sharper question - whether that provider pattern reflects "
    "consistency over and above simple recognition, or merely restates which brands "
    "the models already know. We could not answer it. Among the brands a model "
    "recalls at all, recognition is effectively universal - every model recognizes "
    "them - so there is no provider pattern in recognition to compare against. The "
    "test we had pre-registered to settle this passed its arithmetic, but the "
    "comparison was empty. Reporting that honestly, rather than as a win, is the "
    "study's most useful result.\n\n"
    "No single provider proved reliably the most consistent across categories, and "
    "the smaller differences seen for lesser-known brands turned out to be mechanical "
    "rather than meaningful."
)

WHAT_WE_MEASURED = (
    "This is a re-analysis: no new model queries were run. It re-examines frozen "
    "measurements from an earlier cross-category study - 112 brands across audiophile "
    "headphones, skincare, cosmetics, automotive, and premium spirits - scored across "
    "a fixed panel of six models, two each from Anthropic, OpenAI, and Google. For "
    "each brand we asked how much of the model-to-model variation in recall is "
    "organized by provider rather than scattered within each provider's own pair, and "
    "whether the same pattern appears in plain recognition. The full method, the "
    "questions to be tested, and the rules for judging them were locked and "
    "time-stamped before any scoring, and every figure was checked back against the "
    "original study."
)

PATTERNS = (
    "Three things to take away. Provider authorship shapes how consistently models "
    "recall a brand - reliably, but faintly. Whether that shaping is about "
    "consistency rather than familiarity could not be tested, because recognition is "
    "already universal among the brands models recall. And no single provider proved "
    "the steadiest. The faint and the unanswerable, not a bold provider effect, are "
    "the honest results."
)

LIMITATIONS = (
    "Three cautions frame these findings. First, scope: five categories and a "
    "six-model panel can detect whether a provider effect exists, but not rank the "
    "providers with confidence or generalize broadly. Second, the consistency score "
    "used here is an inherited, not-yet-validated measure, treated as-is; this study "
    "does not certify it. Third, and most consequentially, the recognition signal "
    "available to us is all-or-nothing and saturated among recalled brands, so the "
    "'beyond recognition' question is bounded by the instrument rather than settled - "
    "a graded recognition signal simply does not exist in this data to push further. "
    "The provider effect is also small, and should be read against the high baseline "
    "the test's structure imposes."
)

WHATS_NEXT = (
    "The clearest next move is a recognition signal with room to vary. The "
    "beyond-recognition question is answerable only where recognition is not already "
    "saturated, so a graded or scaled recognition measure - which this data does not "
    "contain - is the prerequisite for any future claim that provider shapes "
    "consistency rather than mere familiarity. Beyond that, a wider set of categories "
    "would support the provider ranking this study could not resolve, and more models "
    "per provider would lift the test off its high chance floor. Each feeds the "
    "program's next-generation consistency instrument."
)

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "A real fingerprint, faintly pressed",
     "proposition": "Provider identity shapes how consistently models recall a brand.",
     "verdict": "SUPPORTED", "qualifier": "real but modest", "status_class": "positive"},
    {"id": "P2", "headline": "The question that had no answer",
     "proposition": "That provider effect reflects consistency beyond simple recognition.",
     "verdict": "NOT ESTABLISHED", "qualifier": "untestable here - recognition saturated", "status_class": "neutral"},
    {"id": "P3", "headline": "No provider stands out as steadiest",
     "proposition": "One provider is reliably the most internally consistent across categories.",
     "verdict": "NOT SUPPORTED", "qualifier": "unresolved; underpowered at five categories", "status_class": "neutral"},
    {"id": "P4", "headline": "Obscurity is not a signature",
     "proposition": "Lesser-known brands carry a distinct provider signature.",
     "verdict": "NOT SUPPORTED", "qualifier": "the pattern is mechanical, not a signature", "status_class": "neutral"},
    {"id": "P5", "headline": "Read the lens before the brand is known",
     "proposition": "The provider lens is informative only where recognition is not yet saturated.",
     "verdict": "SUPPORTED", "qualifier": "the study's central lesson", "status_class": "positive"},
]

HYPOTHESIS_DETAILS = {
    "P1": "The provider share of recall variation is reliably above chance and holds across all five categories, surviving every leave-one-category-out recheck. Its size is small - just above the high floor the three-pair structure imposes - so it reads as a dependable but minor influence.",
    "P2": "The pre-registered gate met its number, but only because recognition contributed essentially nothing to compare against: among recalled brands, every model recognizes the brand, leaving no provider pattern in recognition. The gate therefore measured recall asymmetry alone, not a separation from recognition. We treat the beyond-recognition question as unanswered.",
    "P3": "Provider consistency rankings change from category to category, and five categories are too few to distinguish a true ordering from noise. The result is read as uninformative rather than as evidence of parity.",
    "P4": "Barely-recalled brands show smaller provider differences, but this follows mechanically from their having little recall variation to organize. It is not a distinct property of obscure brands.",
    "P5": "Taken together, the provider lens is meaningful only where recognition still varies - the emerging-recognition regime. For universally recognized brands, today's recognition signal is too saturated to support the comparison. This is a scoping rule for measuring AI Availability Consistency, and the study's most portable conclusion.",
}

CLOSING = (
    "The most valuable findings sometimes map their own edges. Provider authorship "
    "leaves a faint, real mark on how consistently AI models recall a brand - worth "
    "knowing, easy to overstate. But the question brands will most want answered - is "
    "this about consistency, or just familiarity? - turns out to be unanswerable for "
    "the brands that need it least, and answerable only for those still earning "
    "recognition. That boundary, not the faint signal, is what to carry forward: "
    "read the provider lens where recognition is still being won, and treat it with "
    "caution once it has been."
)
