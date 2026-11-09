"""
v0.41 - Long-Horizon Stability t1->t2->t3 - Brand-format report content module.
Third System(TM) managerial register (P1-P5 propositional framing).

Authored against the locked verdicts (osf/v41/v41_verdicts.json). Framing:
  P1 - consistency standings hold over five months (SUPPORTED; beyond the question-structure baseline);
  P2 - presence standings hold over five months (SUPPORTED, 5 of 5 categories);
  P3 - five months is as stable as three weeks (NO FADING DETECTED; both differences span zero);
  P4 - consistency and presence change independently (SUPPORTED; change-on-change 0.03);
  P5 - AI invisibility persists over five months (OBSERVED; descriptive, 56/58).

Register: brand editorial voice, P1-P5 propositions (no H_* notation). No employer
disclosure here (it lives in the SSRN paper's Declarations). Statistics translated to
plain language; markup per build_report: <sub> subscripts, NBSP-wrapped arrows.
"""

_AR = " → "

COVER = {
    "title": "Five Months On",
    "subtitle": (
        "The same 112 brands, the same six AI models, the same questions, five months "
        "apart. The standings held, and the brands the models never mention are still "
        "not mentioned."
    ),
}

STANDFIRST = (
    "A brand measure is only worth managing if it holds still while nothing about the "
    "brand changes. In June, Third System™ showed that AI brand standings survive "
    "three weeks. In November we asked the same six models the same questions about the "
    "same 112 brands once more, 152 days later, and just before those models begin to "
    "retire. Both of the AIAS™ scores, Presence and Consistency, kept their order. "
    "Neither showed any sign of fading with time."
)

LEAD_DECK = (
    "Consistency rank order held from June to November across 80 brands (0.68), above "
    "the level the questions alone would produce. Presence held in all five categories "
    "(0.93 to 0.98). A brand's Consistency and its Presence moved independently of each "
    "other. And 56 of 58 brands below the recall floor in June were still below it in "
    "November."
)

EXEC_SUMMARY = (
    "Four findings and one observation. First, Consistency: which brands the models "
    "agree on, and which they split on, stayed the same over five months. Second, "
    "Presence: how often each brand is named kept its order in every category, with "
    "correlations between 0.93 and 0.98. Third, time: the five-month comparison "
    "was as stable as the three-week one for both scores; we found no fading. Fourth, "
    "independence: when a brand's Consistency moved, its Presence did not move with "
    "it. The two scores are separate signals, which is why the program now reports them "
    "side by side rather than blended into one number. The observation: almost every "
    "brand the models did not name in June was still unnamed in November.\n\n"
    "The implication for brand teams: a brand's standing in AI answers has inertia "
    "measured in months, not weeks. It does not drift away on its own, and it does not "
    "improve by waiting. Absence in particular is a durable condition."
)

WHAT_WE_MEASURED = (
    "This is the third measurement of five category panels first measured in May 2026: "
    "audiophile headphones (16 brands), and skincare, cosmetics, automotive and premium "
    "spirits (24 each). The second wave ran in June, 15 to 21 days after the first. The "
    "third ran on 9 November, 152 days after the second, with the brand lists, the "
    "question wording and the six models (two each from Anthropic, OpenAI and Google) "
    "unchanged. For the four models that report a dated version, we confirmed it was "
    "the same version as in June.\n\n"
    "Presence measures how often a model names a brand when a buyer-style question is "
    "asked without prompting. Consistency measures whether the six models agree about "
    "that brand, or whether some name it reliably and others ignore it; it uses the "
    "program's current Consistency method, adopted in July, which does not rise and "
    "fall with how often a brand is named. The method, the tests and the pass marks were "
    "registered publicly before the first November question was sent, and all 852 "
    "questions returned an answer."
)

PATTERNS = ""

LIMITATIONS = (
    "Part of Consistency's stability comes from the question set itself. When we "
    "scrambled which model gave which answer within each question, the brand order "
    "still repeated at 0.36 on average. The observed 0.68 exceeded every one of 10,000 "
    "scrambled versions, but the share of stability that belongs to the brand is smaller "
    "than the headline figure alone suggests.\n\n"
    "Consistency could be computed for 80 of the 112 brands; the other 32 went unnamed "
    "in at least one of the two waves, so there was no agreement to measure. The panels are small (16 to 24 "
    "brands), the categories are five mature consumer markets, and the models are one "
    "generation old and answer from their training alone, without web search. Stability "
    "here is stability of the measurement, not proof that it tracks sales or "
    "preference. And because these models are being retired, this exact panel cannot be "
    "re-run: these are the last data it can provide."
)

WHATS_NEXT = (
    "The program's next synthesis treats Presence and Consistency as two separate "
    "scores reported side by side, and this study supplies the long-horizon evidence "
    "that both are stable enough to report. Consistency will be rated only for brands "
    "named often enough for agreement to mean something.\n\n"
    "Measurement continues on the current generation of models, with web search off and "
    "on. Whether brand standings carry across a change of model generation, and what "
    "actually moves a brand across the recall floor, are the open questions for brand "
    "teams."
)

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "The models agreed on the same brands five months later",
     "proposition": "Consistency standings hold over five months.",
     "verdict": "SUPPORTED",
     "qualifier": "rank order 0.68 across 80 brands, above every one of 10,000 scrambled baselines",
     "status_class": "positive"},
    {"id": "P2", "headline": "Presence kept its order in every category",
     "proposition": "Presence standings hold over five months.",
     "verdict": "SUPPORTED",
     "qualifier": "5 of 5 categories at or above the registered bar of 0.70",
     "status_class": "positive"},
    {"id": "P3", "headline": "Five months was as stable as three weeks",
     "proposition": "Standings fade as the interval grows.",
     "verdict": "NO FADING DETECTED",
     "qualifier": "the three-week and five-month figures differ by less than their margin of error, for both scores",
     "status_class": "neutral"},
    {"id": "P4", "headline": "Two scores, two separate signals",
     "proposition": "Consistency and Presence change independently.",
     "verdict": "SUPPORTED",
     "qualifier": "change in one is unrelated to change in the other (0.03 across 80 brands)",
     "status_class": "positive"},
    {"id": "P5", "headline": "Invisibility lasts",
     "proposition": "AI invisibility persists over five months.",
     "verdict": "OBSERVED",
     "qualifier": "descriptive; 56 of 58 below-floor brands kept the status; no pass mark was set",
     "status_class": "neutral"},
]

HYPOTHESIS_DETAILS = {
    "P1": ("Across the 80 brands with a Consistency score in both June and November, the "
           "brand order correlated at 0.68 (12 headphones, 16 skincare, 19 cosmetics, 15 "
           "automotive and 18 spirits brands). The registered bar was 0.50, and the result "
           "also had to beat two chance baselines: shuffled brand labels, and a scramble of "
           "which model answered within each question. It beat both; the scrambles "
           "averaged 0.36 and never exceeded 0.66. Leaving out any one category, the "
           "figure stays between 0.64 and 0.73."),
    "P2": ("Rank correlation of Presence between June and November: headphones 0.94, "
           "skincare 0.94, cosmetics 0.94, automotive 0.98, spirits 0.93. Every category "
           "cleared the registered bar of 0.70, and unlike recognition in the earlier "
           "waves, Presence showed no ceiling: no brand was named in every question by "
           "every model."),
    "P3": ("Measured from May, Consistency's brand order correlated at 0.66 three weeks "
           "later and 0.64 five and a half months later. Presence: 0.965 and 0.963. Both "
           "differences are smaller than their margins of error, so the study detects no "
           "decay. That is a finding of no change, not proof that none exists."),
    "P4": ("For each brand we compared how far its Consistency rank moved from June to "
           "November with how far its Presence rank moved. The two movements were "
           "unrelated (0.03). Even at a single point in time the two scores are only "
           "weakly related (0.15), which supports reporting them separately."),
    "P5": ("Brands below the recall floor in June that were still below it in November: "
           "headphones 8 of 8, skincare 15 of 15, cosmetics 9 of 10, automotive 10 of 10, "
           "spirits 14 of 15. Pooled, 56 of 58 (97%). Over the first three weeks the "
           "figure was 56 of 57."),
}

CLOSING = (
    "The first wave showed that AI systems hold measurable brand standings. The second "
    "showed that they survive three weeks. This third wave shows that they survive five "
    "months, for both of the scores the program now reports, and that the two scores "
    "move independently. A standing that holds this long is one a brand can set out to "
    "change on purpose, and measure whether it did."
)
