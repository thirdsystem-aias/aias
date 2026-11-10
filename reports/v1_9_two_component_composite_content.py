"""
v1.9 - Two-Component Composite Calibration - Brand-format report content module.
Third System(TM) managerial register (P1-P5 propositional framing).

Authored against the locked records (osf/methodology/v1_9/prereg/v1_9_calibration.json,
osf/methodology/v1_9/v1_9_verdicts.json). Framing:
  P1 - no single score passed (SUPPORTED; 8 of 8 candidates fail at least one test);
  P2 - one number would repeat Presence (SUPPORTED; rho(A, P) 0.971-0.997, 0.969 in November);
  P3 - two reliable scores, kept apart (SUPPORTED; blind: 0.95 / 0.65 / 0.19);
  P4 - Consistency is rated only with six or more mentions (LOCKED RULE);
  P5 - two scores, side by side (DECIDED).

Register: brand editorial voice, P1-P5 (no H_* notation). No employer disclosure here
(it lives in the paper's Declarations).
"""

COVER = {
    "title": "One Score or Two?",
    "subtitle": (
        "We tested every pre-set way of folding Consistency into Presence. None added "
        "anything, so the AI Availability Score now reports two numbers."
    ),
}

STANDFIRST = (
    "Third System™ now measures two things about a brand in AI answers: Presence, how "
    "often AI models name it, and Consistency, whether the models agree about it. The "
    "obvious next step was one combined AIAS™ number. Before building it, we fixed the "
    "tests a combined number would have to pass, ran them on the May and June data, and "
    "then checked the outcome blind on November's. No combined number passed. Brand teams "
    "get two scores, each reliable over five months, and each saying something the other "
    "does not."
)

LEAD_DECK = (
    "All eight pre-specified ways of combining the two scores failed at least one of three "
    "tests. Each that kept Consistency separate ranked brands almost exactly as Presence "
    "already does. Shown side by side, the two scores held their brand order from June to "
    "November (0.95 and 0.65) and stayed unrelated (0.19)."
)

EXEC_SUMMARY = (
    "Three findings and one rule. First, no combined score passed: each candidate either "
    "pulled Consistency toward Presence, gave brands credit for a mention or two, or ranked "
    "brands as Presence already does. Second, the reason is a difference in spread: Presence "
    "runs across the whole scale, while Consistency, for the brands it can rate, sits high, "
    "so any average follows Presence. Third, the two scores work as a pair: tested blind on "
    "November's data, both kept their brand order and stayed separate. The rule: "
    "Consistency is rated only for brands named at least six times across the six models; "
    "below that, agreement cannot be observed.\n\n"
    "The implication for brand teams: read the two numbers separately. Presence says how "
    "often AI names you. Consistency says whether that visibility is shared across models "
    "or depends on a few of them. A combined score would hide the second answer inside the "
    "first."
)

WHAT_WE_MEASURED = (
    "The data are the five categories the program has tracked since May 2026: audiophile "
    "headphones, skincare, cosmetics, automotive and premium spirits, 112 brands asked "
    "about in the same words by the same six models (two each from Anthropic, OpenAI and "
    "Google), in May, June and November.\n\n"
    "Before looking at any result we fixed eight candidate combined scores: two ways to "
    "score Consistency, two ways to handle brands with few mentions, and two ways to "
    "combine. Each had to pass three tests in both May and June. Consistency must stay "
    "separate from Presence; the combined score must rank brands differently from "
    "Presence; and a brand named once or twice must not gain more than Presence already "
    "gives it. The selection rule, including what to do if nothing passed, was written down "
    "before the tests ran. The outcome was then registered publicly and checked on the "
    "November wave, which had not been collected yet."
)

PATTERNS = ""

LIMITATIONS = (
    "The May and June data had been analysed before, so that stage is calibration, not a "
    "test; only the November check is a test. Eight candidates is a deliberately small, "
    "pre-set list; other forms of combined score were not tried, so the result says none of "
    "these adds information, not that none ever could.\n\n"
    "Everything here applies to one panel of six models, now retiring, which answer without "
    "web search; a new panel needs its own calibration. Five categories and 112 brands limit "
    "the precision of every figure, and the November Consistency checks rest on about 50 "
    "brands. Neither score has yet been tested against what buyers actually do."
)

WHATS_NEXT = (
    "The program's next synthesis reports Presence and Consistency side by side under these "
    "definitions, with the share of brands too rarely named to rate shown next to "
    "Consistency.\n\n"
    "The same tests will be run on the current generation of models, with web search off "
    "and on, before their scores are compared with these. The question of one combined "
    "number reopens when a third component is measured, under the same tests and the same "
    "rule."
)

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "No single score passed",
     "proposition": "A combined Presence and Consistency score passes all three tests.",
     "verdict": "NOT SUPPORTED",
     "qualifier": "8 of 8 candidates failed at least one test; the rule fixed in advance therefore locks two scores",
     "status_class": "neutral"},
    {"id": "P2", "headline": "One number would repeat Presence",
     "proposition": "A combined score ranks brands as Presence already does.",
     "verdict": "SUPPORTED",
     "qualifier": "0.97 to 0.99 with Presence in May and June; 0.97 again in November",
     "status_class": "positive"},
    {"id": "P3", "headline": "Two reliable scores, kept apart",
     "proposition": "Both reported scores hold their order and stay separate over five months.",
     "verdict": "SUPPORTED",
     "qualifier": "tested blind: 0.95 and 0.65 June to November; 0.19 between them",
     "status_class": "positive"},
    {"id": "P4", "headline": "Consistency needs at least six mentions",
     "proposition": "Consistency is rated only for brands named six or more times.",
     "verdict": "LOCKED RULE",
     "qualifier": "fixed before the November check; about half the brands are not rated",
     "status_class": "neutral"},
    {"id": "P5", "headline": "Two scores, side by side",
     "proposition": "The AI Availability Score reports Presence and Consistency separately.",
     "verdict": "DECIDED",
     "qualifier": "follows from P1 to P3 under the rule set in advance",
     "status_class": "neutral"},
]

HYPOTHESIS_DETAILS = {
    "P1": ("The eight candidates combine two Consistency scores (dispersion alone, or "
           "dispersion with a positional measure), two rules for brands with few mentions "
           "(leave them unrated, or pull their score toward the middle) and two ways to "
           "combine (average, or multiply). Every one failed at least one test, so under the "
           "rule written in advance, no combined score is adopted."),
    "P2": ("The candidates that kept Consistency separate from Presence produced a combined "
           "score that ranked brands at 0.97 to 0.99 with Presence alone, against a limit of "
           "0.95. The reason is spread: Presence runs from near zero to near 100, while "
           "rated Consistency sits mostly between 65 and 97. In November the best candidate "
           "still matched Presence at 0.97."),
    "P3": ("June to November, Presence kept its brand order at 0.95 across all 112 brands. "
           "Consistency kept its order at 0.65 across the 52 brands rated in both waves; "
           "scrambling which model gave which answer would produce 0.44 on average and 0.58 "
           "at most in 95 of 100 tries, so the score is more stable than the questions alone "
           "explain. In November the two scores were related at only 0.19 (54 brands), "
           "within the limit of 0.30."),
    "P4": ("A brand named once or twice looks consistent by default: its Consistency score "
           "averaged 85 in the early data, higher than for brands named 19 times or more "
           "(76). Pulling such scores toward the middle tied Consistency to Presence (0.72 "
           "to 0.77). Leaving them unrated kept the two separate and made Consistency more "
           "reliable over three weeks (0.74 against 0.53). The cost is coverage: 51 to 52% "
           "of brands are not rated in each wave."),
    "P5": ("Presence answers how often AI names a brand; Consistency answers whether the "
           "models agree. Reported side by side, a brand can see that it is often named but "
           "only by some models, or rarely named but consistently so. A brand too rarely "
           "named to rate is shown as not rated, not as inconsistent."),
}

CLOSING = (
    "A score earns its place by telling you something you did not already know. Tested "
    "against rules set in advance, a single AI Availability number did not: it repeated "
    "Presence. Two numbers do, and both held for five months. Until a further component "
    "changes that, the honest report is the pair."
)
