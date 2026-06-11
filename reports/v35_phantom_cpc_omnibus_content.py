# NOTE: cloned from v34_longitudinal_t1_t2_omnibus_content.py on phase scaffold.
# All COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, PATTERNS,
# LIMITATIONS, WHATS_NEXT, HYPOTHESIS_DETAILS, CLOSING text
# must be re-written for the v0.35 phantom-cpc omnibus
# substrate. Do not ship this file as-is.

"""
v0.35 - CPC Longitudinal t1->t2 Stability - Brand-format report content module.
Third System(TM) managerial register (P1-P4 propositional framing).

Authored against the locked verdicts (osf/v35/v35_verdicts.json). Honest framing:
  P1 - recall-consistency standings hold over weeks (SUPPORTED, 4/5 categories);
  P2 - consistency moves independently of recognition (NOT ESTABLISHED; recognition saturated);
  P3 - recognition standings hold over weeks (SUPPORTED WHERE MEASURABLE; 2/5 at ceiling);
  P4 - AI invisibility persists (OBSERVED; descriptive, 56/57).

Register: brand editorial voice, P1-P4 propositions (no H_* notation). No Samsung anywhere
(the COI disclosure lives in the SSRN paper's Declarations, not in this report). Statistics
are translated to plain language; markup conventions per build_report: <sub> subscripts,
NBSP-wrapped arrows.

The 11 standard attributes follow: COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY,
WHAT_WE_MEASURED, PATTERNS, LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING,
HYPOTHESIS_DETAILS, CLOSING.
"""

# arrow wrapped in non-breaking spaces (prevents line-splits across the connector)
_AR = " → "

COVER = {
    "title": "The Standings Hold",
    "subtitle": (
        "Three weeks later, AI brand rankings barely moved - and the brands AI "
        "couldn't see stayed invisible. A 112-brand, two-wave stability study across "
        "six leading models."
    ),
}

STANDFIRST = (
    "If AI-generated brand recommendations reshuffled at random from week to week, no "
    "one would need to manage them. They don't. Third System™ re-measured five "
    "full category panels - 112 brands, six models, identical questions, twenty-one "
    "days apart at most - and the standings held. Which brands the models recall, and "
    "how consistently they recall them, is a stable property of the brand, not noise "
    "in the machine."
)

LEAD_DECK = (
    "A brand's AI recall-consistency rank held t<sub>1</sub>" + _AR + "t<sub>2</sub> "
    "in four of five categories. Recognition sat at ceiling almost everywhere - every "
    "established brand is “known”; the competition happens in recall. And "
    "invisibility proved the stickiest state of all: 56 of 57 brands below the recall "
    "floor at first measurement were still there three weeks later."
)

EXEC_SUMMARY = (
    "Three findings, one implication. First, stability: per-brand recall-consistency "
    "rankings correlated strongly across waves in skincare, cosmetics, automotive, and "
    "premium spirits (rank correlations 0.76-0.96); only audiophile headphones - the "
    "smallest panel - failed the bar. Second, ceiling: AI recognition of established "
    "brands is saturated. In four of five categories, effectively every brand was "
    "recognized by every model, both waves. Recognition no longer discriminates; "
    "recall does. Third, persistence of absence: brands that failed to surface in AI "
    "recall at the first wave almost universally failed again at the second.\n\n"
    "The implication: a brand's AI standing is a managed asset with inertia - it "
    "neither decays in days nor improves by waiting. If your brand is absent from the "
    "AI conversation today, that is its standing until something changes it."
)

WHAT_WE_MEASURED = (
    "Two identical measurement waves, fifteen to twenty-one days apart, across five "
    "locked category panels: audiophile headphones (16 brands), skincare, cosmetics, "
    "automotive, and premium spirits (24 each). Each wave asked six leading AI models "
    "- two each from Anthropic, OpenAI, and Google - the same recognition and recall "
    "questions, word for word, under the AIAS™ measurement protocol. Recognition "
    "asks whether a model knows the brand; recall asks whether the model surfaces it "
    "unprompted when a buyer-style question is posed.\n\n"
    "From per-model recall we compute a consistency score per brand; the study tests "
    "whether each brand's scores, ranks, and visibility status at wave one predict "
    "wave two. Probe wording, brand registries, and model identities were locked and "
    "externally registered before a single second-wave call was made."
)

PATTERNS = (
    "The stability is not uniform - it is structured, and the structure is "
    "informative. The four categories that passed are mature consumer categories with "
    "deep editorial and review coverage; their AI standings look like settled "
    "consensus. The one miss, audiophile headphones, combines the smallest panel with "
    "the most enthusiast-driven, fragmented discourse - the conditions under which a "
    "ranking plausibly should wobble. Meanwhile recognition's ceiling effect tells "
    "brand teams where the game is: the models know your brand exists; the question is "
    "whether they bring it up. And the near-perfect persistence of the invisible "
    "cohort - fourteen of fourteen unsurfaced skincare brands still unsurfaced, "
    "fifteen of fifteen spirits - is the strongest managerial signal in the study: AI "
    "invisibility is a standing condition, not a sampling accident."
)

LIMITATIONS = (
    "Honest boundaries. The consistency instrument remains entangled with "
    "recognition-and-recall presence (a known limitation, documented in the program's "
    "methodology track); this study measures the stability of the quantity, not its "
    "validity as an independent construct. The interval is three weeks - stability "
    "over quarters is a separate, unanswered question. Models were called by their "
    "public names, as a real buyer's tool would; any silent provider-side version "
    "change inside the window is part of what “stability” means here, by "
    "design. Five categories and 16-24 brands per panel bound the precision of any "
    "single category's result. And because recognition sat at ceiling, the study could "
    "not cleanly test whether consistency moves independently of presence - one "
    "category suggests it does; four could not speak."
)

WHATS_NEXT = (
    "The program's next methodology phase replaces the presence-entangled consistency "
    "instrument with a mean-independent one - this study's ceiling effects are direct "
    "evidence for why. The second wave also captured each provider's dated model "
    "version per call, which the first wave could not; that establishes the baseline "
    "for a future third wave able to separate “the model changed” from "
    "“the answers drifted.” And the open managerial question is the "
    "actionable one: if invisibility is sticky, what interventions move a brand across "
    "the recall floor - and how long do they take to register?"
)

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "The standings held through the wait",
     "proposition": "AI recall-consistency standings hold over weeks.",
     "verdict": "SUPPORTED", "qualifier": "4 of 5 categories at or above the pre-registered bar",
     "status_class": "positive"},
    {"id": "P2", "headline": "The question recognition wouldn't let us ask",
     "proposition": "Consistency moves independently of recognition.",
     "verdict": "NOT ESTABLISHED",
     "qualifier": "testable in only 1 of 5 categories - recognition saturated elsewhere; the one informative category is suggestive, not sufficient",
     "status_class": "neutral"},
    {"id": "P3", "headline": "Recognition held where there was a ranking to hold",
     "proposition": "Recognition standings hold over weeks.",
     "verdict": "SUPPORTED WHERE MEASURABLE",
     "qualifier": "strong in all 3 categories with rank variation; 2 categories at a constant ceiling both waves - nothing to rank",
     "status_class": "neutral"},
    {"id": "P4", "headline": "Invisibility is the stickiest state",
     "proposition": "AI invisibility persists.",
     "verdict": "OBSERVED",
     "qualifier": "descriptive; 56 of 57 below-floor brands retained the status; no pass/fail threshold was set",
     "status_class": "neutral"},
]

HYPOTHESIS_DETAILS = {
    "P1": ("Rank correlations by category - headphones 0.42 (miss; smallest panel, "
           "n=8 comparable brands), skincare 0.78, cosmetics 0.89, automotive 0.96, "
           "spirits 0.76; the pre-registered bar was 0.70 in at least four of five."),
    "P2": ("The test requires recognition to vary; in four categories every model "
           "recognized at least nine in ten established brands both waves, collapsing "
           "the test onto recall itself. In headphones - the only category with "
           "recognition variation - consistency was more stable after recognition was "
           "accounted for (0.61 vs 0.42), the study's one suggestive sign of an "
           "independent consistency signal."),
    "P3": ("Recognition rank correlations 0.81 / 0.99 / 1.00 where measurable; in "
           "cosmetics and spirits every brand scored a perfect six of six models, both "
           "waves - 100% exact match, but no ranking to test."),
    "P4": ("Retention of below-floor status - 8/8, 14/14, 9/10, 10/10, 15/15; pooled "
           "56/57 (98%). The single mover was one cosmetics brand."),
}

CLOSING = (
    "The first wave of this program established that AI systems hold measurable, "
    "structured brand standings. This study establishes that those standings persist "
    "- through three weeks, through whatever silent updates providers shipped, through "
    "852 fresh probes. Stability is what makes a measurement worth managing: a number "
    "that holds still long enough to be moved deliberately. The brands with the most "
    "at stake are the ones the models never mention - because as of this measurement, "
    "nothing about waiting changes that."
)
