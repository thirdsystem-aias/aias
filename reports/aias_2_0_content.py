"""
AIAS 2.0 - Synthesis - Third System brand-format report content module.
Managerial register (P1-P5 propositional framing; no H_* notation, no employer disclosure:
that lives in the paper's Declarations).

Authored against the AIAS 2.0 paper draft (papers/aias_2_0/aias_2_0_synthesis_paper_draft.md)
and the locked records it cites (osf/aias_2_0/aias_2_0_synthesis_data.json; v1.9 and v0.41
verdicts; v1.8 instrument). Every number below appears in the paper. Framing:
  P1 - Consistency is its own measure (SUPPORTED; 0.07 / 0.08 / 0.19; change 0.03);
  P2 - both scores held for five months (SUPPORTED; 0.95 and 0.65, beyond shuffled 0.44/0.58);
  P3 - the first agreement measure failed, the second did not (RECORD; 0.68 vs 0.09);
  P4 - Consistency is rated only where there is evidence (LOCKED RULE; 48-49% rated);
  P5 - two numbers, not one (DECIDED; 8 of 8 combined scores failed; 0.97 with Presence).
Chart titles (CHART_SPECS) say what is plotted and never repeat a finding's headline.
"""

COVER = {
    "title": "How Often, and How Evenly",
    "subtitle": (
        "AIAS™ 2.0 measures two separate things about a brand in AI answers. Both held "
        "for five months, and neither can stand in for the other."
    ),
}

STANDFIRST = (
    "When someone asks an AI assistant which brand to buy, the brands it names become the "
    "shortlist. Third System™ measures that shortlist as AI Availability. Until now the "
    "measure had one part, Presence: how often AI models name a brand. AIAS™ 2.0 adds a "
    "second, Consistency: whether the models agree in naming it. Across five categories, "
    "112 brands and three waves from May to November 2026, the two parts stayed separate "
    "and each kept its brand order for five months. Brand teams now get two scores, read "
    "side by side."
)

LEAD_DECK = (
    "Consistency does not follow Presence: the two were nearly unrelated in May, June and "
    "November (0.07, 0.08 and 0.19). Both kept their brand order from June to November "
    "(0.95 and 0.65), Consistency by more than the questions alone explain. No single "
    "combined number passed the tests set for it, so the score is reported as a pair."
)

EXEC_SUMMARY = (
    "Four findings and one rule. First, Consistency is a measure of its own: a brand's "
    "Consistency says little about its Presence, and changes in one say nothing about "
    "changes in the other. Second, both scores are stable properties of a brand: Presence "
    "kept its order almost perfectly over five months, and Consistency kept its order well "
    "beyond what the structure of the questions produces. Third, the agreement measure that "
    "works is the second one built: the first moved with how often a brand is named, so it "
    "was replaced. Fourth, folding the two into one number does not work: every combined "
    "score tested either repeated Presence or broke one of the tests. The rule: Consistency "
    "is rated only for brands the six models name at least six times, which in each wave "
    "is about half the brands.\n\n"
    "For brand teams this separates two questions that are easy to read as one. Presence "
    "asks how often AI assistants name you. Consistency asks whether they agree in doing "
    "so. A brand named by some models and not others depends on which assistant a buyer "
    "happens to use; a brand named evenly does not. Because the two scores move "
    "independently, improving one says nothing about the other, and each needs tracking."
)

WHAT_WE_MEASURED = (
    "The data are the five categories the program has tracked since May 2026: audiophile "
    "headphones, skincare, cosmetics, automotive and premium spirits, 112 brands in all. "
    "The same six AI models (two each from Anthropic, OpenAI and Google) answered the same "
    "questions three times (852 answers per wave): in late May, in June, and on November 9, 152 days later. "
    "Each brand was asked about directly (does the model know it?) and indirectly (does "
    "the model name it when asked about the category?).\n\n"
    "Presence combines the two into a score from 0 to 100. Consistency compares the six "
    "models: it is 100 when every model names a brand equally often across the same "
    "questions, and falls toward 0 as some models name it and others do not. Before the "
    "November answers were scored, the synthesis registered publicly which tests it would "
    "rely on and how its headline would read for every possible result."
)

PATTERNS = ""

LIMITATIONS = (
    "Everything here applies to one panel of six models, now retiring, which answered "
    "without web search; scores from a new panel must be recalibrated before they are "
    "compared with these. Five categories and 112 brands limit the precision of every "
    "figure, and the Consistency checks rest on 52 to 54 rated brands. About half the "
    "brands are named too rarely to rate, so Consistency describes the regularly named "
    "part of each category.\n\n"
    "Part of Consistency's stability comes from the questions themselves; the comparison "
    "with shuffled answers measures that share but does not remove it. Questions were in "
    "English. Neither score has yet been tested against what buyers do: stable, separate "
    "scores are what a useful measure needs, not proof that it predicts sales."
)

WHATS_NEXT = (
    "The same 112 brands are being measured this month on the newest AI models, with web search off "
    "and on, so that both scores can be recalibrated for the panel the program uses from "
    "now on. A separate study, registered before any of its data were looked at, tests "
    "whether Presence and Consistency anticipate changes in how often people search for a "
    "brand.\n\n"
    "The third part of AI Availability, Ranking (where a brand appears in an AI answer's "
    "list), opens AIAS 3.0. When it is measured, the question of one combined number "
    "reopens under the same tests and the same rule."
)

HYPOTHESIS_SCORING = [
    {"id": "P1", "headline": "Consistency is a measure of its own",
     "proposition": "A brand's Consistency carries information its Presence does not.",
     "verdict": "SUPPORTED",
     "qualifier": "0.07, 0.08 and 0.19 with Presence in May, June and November; 0.03 between their changes",
     "status_class": "positive"},
    {"id": "P2", "headline": "Both scores held for five months",
     "proposition": "Presence and Consistency keep their brand order from June to November.",
     "verdict": "SUPPORTED",
     "qualifier": "0.95 for Presence (112 brands); 0.65 for Consistency (52 brands), above shuffled answers",
     "status_class": "positive"},
    {"id": "P3", "headline": "The first agreement measure failed; the second did not",
     "proposition": "Consistency can be measured without moving with how often a brand is named.",
     "verdict": "SUPPORTED",
     "qualifier": "first measure 0.68 with naming frequency; current measure 0.09",
     "status_class": "positive"},
    {"id": "P4", "headline": "Rated only where there is evidence",
     "proposition": "Consistency is rated only for brands named at least six times.",
     "verdict": "LOCKED RULE",
     "qualifier": "fixed before November; 48 to 49% of brands rated in each wave",
     "status_class": "neutral"},
    {"id": "P5", "headline": "Two numbers, not one",
     "proposition": "The AI Availability Score reports Presence and Consistency separately.",
     "verdict": "DECIDED",
     "qualifier": "8 of 8 pre-set combined scores failed; an average of the two still matched Presence at 0.97 in November",
     "status_class": "neutral"},
]

HYPOTHESIS_DETAILS = {
    "P1": ("Within each category, brands were ranked on both scores and the two rankings "
           "compared. The link was 0.07 in May, 0.08 in June and 0.19 in November, the "
           "wave that served as the test, against a pass mark of 0.30. Changes were "
           "unrelated too: how far a brand's Consistency moved between June and November "
           "had nothing to do with how far its Presence moved (0.03, 80 brands). A factor "
           "that shapes Presence, how much of a brand's naming comes from its cultural "
           "identity rather than its category, has no effect on Consistency (-0.01, 53 "
           "brands). Two brands with the same Presence can sit far apart on Consistency."),
    "P2": ("From June to November, Presence kept its brand order at 0.95 across all 112 "
           "brands, and the naming rate within every category at 0.93 or more. Consistency kept its order "
           "at 0.65 across the 52 brands rated in both waves, against a pass mark of 0.50. "
           "Any measure of agreement gets some stability from the questions themselves: "
           "with each model's answers shuffled within each question, the same comparison "
           "averages 0.44, and 95 of 100 tries stay below 0.59. Consistency clears that "
           "line, so the stability belongs to the brands, not only to the questions. "
           "A test for decay between the three-week and five-month comparisons found none."),
    "P3": ("The program's first agreement measure, built in June, compared how much the "
           "models' counts varied with their average. Counts that can only run from zero to "
           "six make that ratio follow the average, so the measure moved with how often a "
           "brand is named (0.68 on the same data), and a registered test rejected it. Its "
           "replacement compares the models' spread with the spread expected from chance "
           "at the same naming rate. It is unrelated to naming frequency (0.09) and can be "
           "computed for every brand named at least once (84 of 84, against 55)."),
    "P4": ("A brand named once or twice looks consistent by default, because a single "
           "mention cannot show disagreement. Averaged with Presence, an unrated score "
           "would have given brands named once 58 points against 30 for brands never "
           "named, a premium earned by chance. Rating Consistency only from six mentions "
           "removes it. The cost is coverage: 55, 54 and 54 of 112 brands were rated in "
           "May, June and November, between 38% and 58% by category. A brand below the "
           "line is shown as not rated, not as inconsistent."),
    "P5": ("Before the November data were scored, eight combined scores were fixed and "
           "tested on the May and June data against three conditions: keep Consistency "
           "separate, rank brands differently from Presence, and give no extra credit for "
           "a mention or two. Each failed at least one. The ones that kept Consistency "
           "separate ranked brands at 0.97 to 0.99 with Presence, against a limit of 0.95, "
           "because Presence runs across the whole scale while rated Consistency sits "
           "mostly between 60 and 100. In November a plain average of the two still "
           "matched Presence at 0.97. A single 0-100 score remains the goal; with two parts it "
           "would be Presence under another name."),
}

CHART_SPECS = {
    "P1": {"title": "Link between the two scores, by wave",
           "subtitle": "Rank correlation of Consistency with Presence within each category (0 = unrelated)",
           "data": "|rho(C*, P)|: May 0.073 (n 55), June 0.082 (n 54), November 0.189 (n 54); lines at 0.30 (pass mark) and 0.50 (too close)",
           "source": "AIAS 2.0 synthesis data; Methodology v1.9 (SSRN 7685126)"},
    "P2": {"title": "Brand order kept from June to November",
           "subtitle": "Rank correlation between the two waves, with the range produced by shuffled answers",
           "data": "Presence 0.954 (n 112, pass 0.80); Consistency 0.647 (n 52, pass 0.50); shuffled-answer null mean 0.438, 95th percentile 0.585",
           "source": "AIAS 2.0 synthesis data; v0.41 (SSRN 7685100); v1.9"},
    "P3": {"title": "How much each agreement measure moves with naming frequency",
           "subtitle": "Rank correlation with mean recall on the same brands (0 = independent)",
           "data": "first measure (coefficient of variation) 0.682 (n 55); current measure (phi) 0.091 (n 197); line at 0.50 (independence ceiling)",
           "source": "Methodology v1.8 (SSRN 6963359); v1.7 (SSRN 6878818)"},
    "P4": {"title": "Share of brands named often enough to rate, by category and wave",
           "subtitle": "Rated = the six models together name the brand at least six times out of 36",
           "data": "per category x wave rated share from aias_2_0_synthesis_data.json; totals 55, 54, 54 of 112",
           "source": "AIAS 2.0 synthesis data; v1.9 rating rule"},
    "P5": {"title": "Eight combined scores against the tests set for them",
           "subtitle": "How closely each candidate ranks brands like Presence, May and June, and the condition it failed",
           "data": "v1.9 Stage 1 grid: rho(A, P) per candidate and wave, limit 0.95; failed condition per candidate; November value 0.969 for the floored average (C_phi+FLOOR+ADD, descriptive)",
           "source": "Methodology v1.9 calibration record"},
}

CLOSING = (
    "AI assistants now sit between many buyers and the brands they consider. Knowing how "
    "often they name a brand was the first step. Knowing whether they agree is the second, "
    "and it turns out to be a different fact about the brand, stable enough to track. Read "
    "together, the two scores show not only whether a brand is in the AI shortlist, but "
    "how dependably."
)
