"""AIAS 3.0 (Coverage) release report (Tier 1 Flagship, report design system v2): content, managerial register
(P1-P5 findings, no hypothesis labels, no verdict words). DRAFT, pre-data (branch aias-3.0-draft, Nov 26, 2026).
Not built, not published.

Tokens (papers/aias_3_0/tokens_aias3.py): {{L:KEY}} is a value that exists today, copied by
papers/aias_3_0/sources_aias3.py from the cited locked file at the cited commit; {{P:KEY}} is a placeholder for an
input that does not exist yet (the release pre-registration, its calibration and dissociation outputs, the optional
Coverage retest, the predictive-validity amendment, build facts). No number is typed: the tests fail on a typed
number in this module (papers/aias_3_0/tests/test_tokens_aias3.py). A dict with "requires" is kept only when its
flags hold in the values file written at the data lock.

Register rules applied: one chart per finding, and a chart title says what is plotted and never repeats or
paraphrases its finding's title (CLAUDE.md, Nov 9, 2026); the employer and its affiliates are not named (brand
file, byline.commercial_outputs_disclosure; the small-print COI carries every item of the paper's Declarations in
employer-neutral words, as in the AIAS 6.0 Preview draft); AI-use statement verbatim; small-print notes and a
Disclosures block (Pablo, Nov 15, 2026); no held study; Coverage is named as the AIAS 3.0 part because it passed its
gate (control panel milestone, Nov 14) and this is its release.
Builder (to fork after the data lock, not before): reports/build_report_aias6_preview.py with reports/ts_layout.py,
reports/small_print.py and reports/report_code.py from branch preview-6.0-draft (taken unchanged from v0.44-report).
"""

REPORT_CODE = "{{P:REPORT_CODE}}"   # Pablo's call (the Preview's was his call 5)
TIER = 1                            # CLAUDE.md: Tier 1 Flagship includes the AIAS 3.0 to 5.0 releases
COVER = "{{P:COVER_IMAGE}}"         # photo library: the AIAS 3.0 image is "Curved slats" (claude/photo-library-v2-prompt.md);
                                    # full-size file from Pablo before any print cover

TITLE = "Named in Which Situations"   # working title (AIAS 2.0's report: "How Often, and How Evenly"); Pablo's call
DECK = "AIAS™ 3.0 adds Coverage: for how many of a category's buying situations AI answers name a brand"

STANDFIRST = [
    "AIAS™ 3.0 adds a third score to Presence and Consistency. Coverage asks whether AI answers name a brand across a "
    "category's buying situations or only in a few, read against how often the brand is named at all. "
    "{{P:REPORT_HEADLINE}}",
]

GLANCE_NUMBERS = [
    {"value": "{{L:a.h1.rho}}", "unit": "",
     "label": "Rank correlation of Coverage with Presence, within category",
     "source": "{{L:a.h1.n}} rated brands; separate at {{L:a.band.conf}} or below"},
    {"value": "{{L:a.h4.rel}}", "unit": "",
     "label": "Reliability of Coverage across two halves of the situations",
     "source": "{{L:a.h4.n}} brands rated on both halves"},
    {"value": "{{L:a.rated}}", "unit": "",
     "label": "Brands named often enough to rate for Coverage",
     "source": "of {{L:a.units}} brands in five categories"},
]

MEASURED = ("Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, the newest flagship of three providers, search off. "
            "{{L:a.cep_per_cat}} buying situations per category, asked as questions that name no brand, for "
            "{{L:a.units}} brands in headphones, skincare, cosmetics, cars and spirits. Plan, scorer and "
            "deviations record: {{P:DEPOSIT}}, pre-registration {{P:PREREG_TAG}}.")

SUMMARY = [
    "AIAS™ describes how AI answers treat a brand in parts, each its own score from 0 to 100. Presence (AIAS 1.0) is "
    "how often AI names the brand; Consistency (AIAS 2.0) is how evenly different models name it. Coverage is the "
    "third: whether the naming spreads across the situations in which people buy.",
    "{{P:REPORT_HEADLINE}} No single AIAS number per brand is published unless a combined score passes its "
    "pre-set tests. {{P:CAL_COMPOSITE_SENTENCE}}",
]

INTRO_LEAD = ("Two brands can be named equally often by AI and still differ in where: one across every kind of "
              "buying situation, the other only when a buyer mentions a particular need. Coverage measures that "
              "difference.")

INTRO = [
    "People meet a category in situations: a gift, a first purchase on a tight budget, a product for hot weather. "
    "Brand research calls these category entry points, and a brand linked to more of them is more likely to come "
    "to mind. Bigger brands are linked to more situations, so a plain count would mostly repeat how big a brand is.",
    "Coverage therefore compares the situations in which a model names a brand with the situations it would cover "
    "if it named the brand without regard to the situation, given the same number of mentions. A score of 50 "
    "means the situation made no difference; lower means the naming is packed into fewer situations.",
    "Coverage became the third released part after it passed its own pre-set test and a second study of its "
    "robustness. This release sets out how it sits beside Presence and Consistency.",
]

MEASURED_HEAD = "What we measured"
MEASURED_PARAS = [
    "Brands. The {{L:a.units}} brands of five category studies (headphones, skincare, cosmetics, cars and "
    "spirits), unchanged since their first wave in May 2026.",
    "Questions. {{L:a.cep_per_cat}} situations per category, two for each of seven kinds of cue (why, when, where, "
    "while, with whom, with what, how feeling), each asked as a question that names no brand, three times to each "
    "model.",
    "Rules. A brand is rated for Coverage only when the models name it often enough ({{L:a.floor}} mentions or "
    "more, by at least two models). Two scores count as separate when the rank correlation of their brand orders "
    "within each category is at most {{L:a.band.conf}}, and as overlapping at {{L:a.band.fals}} or above.",
]

# One chart per finding. Chart titles say what is plotted and never repeat or paraphrase the finding title.
CHARTS = {
    "report_fig_01_gate.pdf": {
        "title": "Rank correlation of the Coverage score with each existing measure, within category",
        "subtitle": "{{L:a.h1.n}} rated brands; shaded: separate at {{L:a.band.conf}} or below",
        "data": "v1.12 verdict file, legs H1-H3 (L tokens a.h1-a.h3)"},
    "report_fig_02_reliability.pdf": {
        "title": "Split-half reliability for every balanced way of halving the questions",
        "subtitle": "{{L:b.h32.splits}} splits, sorted; median {{L:b.h32.rel}}",
        "data": "v1.19 verdict file, H32_SetSampling per_split"},
    "report_fig_03_baseline.pdf": {
        "title": "Coverage score per rated brand, by category",
        "subtitle": "Line at 50: situation-blind naming; category medians {{L:a.median_lo}} to {{L:a.median_hi}}",
        "data": "v1.12 unit table (cov_star_N3)"},
    "report_fig_04_calibration.pdf": {
        "title": "Rank correlation of each candidate combined score with Presence",
        "subtitle": "{{P:CAL_N_CANDIDATES}} candidates against the pre-set line",
        "data": "{{P:FIG_CALIBRATION}}"},
    "report_fig_05_three_scores.pdf": {
        "title": "Brand ranks on Presence, Consistency and Coverage, pair by pair",
        "subtitle": "{{P:DIS_N}} brands rated on all three, within category",
        "data": "{{P:FIG_DISSOCIATION}}"},
    "report_fig_06_search_interest.pdf": {
        "requires": ["PRED_RESULT"],
        "title": "Change in search interest against the November Coverage score",
        "subtitle": "Four weeks ending {{L:pv.s2.window_end}} against the four weeks ending in early November",
        "data": "v0.43 Stage 2 verdicts with the Coverage amendment"},
}

FINDINGS = [
    {"title": "Coverage is a third reading of a brand",
     "chart": "report_fig_01_gate.pdf",
     "caption": "Dot: rank correlation within category; bar: its bootstrap interval; shaded: the pre-set band for "
                "separate scores. Source: Coverage Paper A (v1.12).",
     "body": [
         "How widely a brand's naming spreads across situations did not follow how often it is named: the rank "
         "correlation with Presence was {{L:a.h1.rho}}, with Consistency {{L:a.h2.rho}} and with the brand's own "
         "naming rate {{L:a.h3.rho}}, all inside the band set in advance.",
         "A plain count of situations would have told a different story: it followed the naming rate closely, as "
         "bigger brands are linked to more situations. The adjusted score is what makes Coverage a separate reading.",
     ]},
    {"title": "The score holds on other models, less firmly across questions",
     "chart": "report_fig_02_reliability.pdf",
     "caption": "Each bar one way of splitting the situations into two balanced halves; height: how alike the two "
                "halves rank brands. Source: Coverage Paper B (v1.19).",
     "body": [
         "Swapping one model for another left the brand order largely in place (rank correlation {{L:a.h8.rho}}). "
         "Across the {{L:b.h32.splits}} ways of splitting the situations in half, the median reliability was "
         "{{L:b.h32.rel}}, below the bar set in advance: which situations are asked matters for a single brand's "
         "score.",
         "Read one brand's Coverage as a broad indication, and compare brands only when the gap is large.",
     ]},
    {"title": "No brand types and no fading-brand pattern",
     "chart": "report_fig_03_baseline.pdf",
     "caption": "Each dot a rated brand; line at 50: naming that ignores the situation. Source: Coverage Paper A "
                "(v1.12).",
     "body": [
         "Brands did not lean towards the same kind of situation twice, so no brand types are reported. Brands the "
         "older models rarely named were not tied to fewer situations, and no question about cars to buy new named "
         "a discontinued brand.",
         "None of the {{L:b.broad_of}} rated brands scored above 50: on these models no rated brand's naming spread "
         "wider than naming that ignored the situation would give.",
     ]},
    {"title": "How the three scores are reported together",
     "chart": "report_fig_04_calibration.pdf",
     "caption": "Each bar a candidate way of combining the scores; line: the pre-set limit above which a combined "
                "score only repeats Presence. Source: {{P:DEPOSIT}}.",
     "body": [
         "{{P:CAL_COMPOSITE_SENTENCE}}",
         "{{P:CAL_BRIDGE_SENTENCE}}",
     ]},
    {"title": "Presence, Consistency and Coverage on the same brands",
     "chart": "report_fig_05_three_scores.pdf",
     "caption": "Rank correlations within category for each pair of scores, with the pre-set band. Source: "
                "{{P:DEPOSIT}}.",
     "body": [
         "{{P:DIS_PREVIEW_SENTENCE}}",
         "{{P:REPORT_HEADLINE}}",
     ]},
    {"requires": ["PRED_RESULT"],
     "title": "Coverage and where search interest went next",
     "chart": "report_fig_06_search_interest.pdf",
     "caption": "Each dot a brand; change in US search interest against its November Coverage score. Source: v0.43.",
     "body": ["{{P:PRED_SENTENCE}}"]},
]

SCORED_HEAD = "The pre-set tests, scored"
SCORED_INTRO = ("Each test, its bar and the wording of every possible headline were deposited before the data they "
                "read. Results use the pre-set words and were computed once by the locked scoring scripts.")
SCORED_ROWS = [
    {"row": ["01", "Coverage is separate from Presence, from Consistency and from how often a brand is named, and "
                   "reliable across two halves of the situations",
             "Held (rank correlations {{L:a.h1.rho}}, {{L:a.h2.rho}} and {{L:a.h3.rho}}; reliability "
             "{{L:a.h4.rel}})"]},
    {"row": ["02", "Coverage is reliable across samples of situations",
             "Partly held (median {{L:b.h32.rel}})"]},
    {"row": ["03", "Brands have situation profiles that repeat", "Did not hold"]},
    {"row": ["04", "Brands below the recall floor are tied to fewer situations", "Did not hold"]},
    {"row": ["05", "The three scores, calibrated and compared on the same brands", "{{P:DIS_VERDICT}}"]},
    {"requires": ["RETEST_RUN"],
     "row": ["06", "Coverage keeps its brand order over time",
             "{{P:RETEST_SENTENCE}} (rank correlation {{P:RETEST_RHO}}, {{P:RETEST_N}} brands, {{P:RETEST_DAYS}} "
             "days apart)"]},
    {"requires": ["!RETEST_RUN"],
     "row": ["06", "Coverage keeps its brand order over time", "Not yet measured"]},
]

LIMITS_HEAD = "Limitations"
LIMITS = [
    "One week of answers from three models, one per provider, in US English, search off, on five categories whose "
    "brands were fixed in May 2026. Answers change between model versions.",
    "One set of situations per category, written by one procedure; the score depends on which situations are "
    "asked, and no buyer data weight them.",
    "Only brands named often enough are rated; Coverage is read among registry brands only.",
    "{{P:RETEST_SENTENCE}}",
    "Separate is not the same as valid: {{P:PRED_SENTENCE}}",
    "{{P:APOS_SENTENCE}}",
]

NEXT_HEAD = "What's next"
NEXT = [
    "An independently written set of situations with buyer weights, and a test of question wording, each need their "
    "own collection. The next releases, AIAS 4.0 and 5.0, add the remaining parts in the order their tests pass.",
    "Plan, scorer, outputs and deviations record: {{P:DEPOSIT}}. Code: github.com/thirdsystem-aias/aias, tag "
    "{{P:PREREG_TAG}}.",
]

DISCLOSURES = {
    "conflicts_of_interest": "The author is employed by a consumer-electronics company. This release selects no "
                             "brands: it reads scores computed on five registries fixed in earlier studies, each "
                             "with its own conflict-of-interest handling. Denon, which replaced a group-owned "
                             "headphone brand before the headphones study was locked, has itself been owned by a "
                             "subsidiary of the company's group since September 23, 2025, which was noticed on "
                             "November 10, 2026; it stays in the analysis, and the Coverage studies' results are "
                             "also computed without it. Group subsidiaries supply components (audio systems, battery "
                             "cells, displays) to several brands in the car registry, a non-competitive "
                             "relationship disclosed without restriction. A group advertising affiliate or its "
                             "agency has worked for five registry brands (Chevrolet, BMW, Bentley, Jack Daniel's "
                             "and Eucerin); they stay in every analysis. The situation questions name no brand. The "
                             "company had no role in this work; it and its affiliates are named in the paper's "
                             "Declarations.",
    "held_out_brands": "No brand was held out. The registries are those of the five category studies, unchanged.",
    "ai_use": "During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with "
              "study design, analysis and writing. The author reviewed and edited all content and takes full "
              "responsibility for it.",
    "independence": "Self-funded. No brand was contacted, sponsored the work or saw it before publication. Every "
                    "result was computed once by a locked scoring script from locked study files.",
}

CLOSING_STATEMENT = ["{{P:REPORT_HEADLINE}}"]
