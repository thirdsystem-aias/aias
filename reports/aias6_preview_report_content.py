"""AIAS 6.0 Preview report (Tier 1, report design system v2): content, managerial register (P1-P5, no hypothesis
labels). DRAFT SKELETON, pre-data (branch preview-6.0-draft, Nov 25, 2026). Not built, not published.

Every number and every outcome word is a {{v:KEY}} token resolved by papers/aias_6_0_preview/tokens_aias6.py from
the locked scorer's outputs (osf/aias_6_0_preview/outputs/, written once after the data lock, section 11.4) or
from the paper fill's own values (the section 6.6 headline and W1 sentence), so the two registers print one
outcome in the same words. None is typed. A dict with "requires" is kept only when the paper fill's flags or
cases satisfy it: "STRUCT" (a structure test ran), "CLASS=A|A_k" (the wording class), "CASE_R=MARGINAL" (a gate
state), "PC=CONFIRMED" (Presence-Consistency result), "!FLAG" for the negation.

Register rules applied: "provisional" on the title, every finding and every chart caption (pre-registration
section 5); the validation status line printed once; no single AIAS number per brand; Ranking sentences carry
"retest pending" while v1.14 has no final gate (W3, through the state word and label); a chart title says what
is plotted and never repeats or paraphrases its finding's title (CLAUDE.md, Nov 9, 2026); the report omits the
author's employer by name (brand file, byline.commercial_outputs_disclosure) and the small-print COI carries
every item of record from the paper's Declarations in employer-neutral words; AI-use statement verbatim.
Builder (to fork after the data lock, not before): reports/build_report_v44_r1.py with reports/ts_layout.py and
reports/small_print.py from branch v0.44-report. Report code: see REPORT_CODE.

Pablo's nine Preview calls (control panel, Wed 2026-11-25, 7:15 am CT, "Ok to all", as drafted at ~0:35 am):
(1) Sentiment stays NOT RUN (v1.11 issued no verdict file); v1.20/v1.21 are named in one exploratory sentence with
a dated note (paper, section 3.2). (2) Its legacy-panel fallback prints as "pending" with the cause (paper and
finding 03). (3) Ranking is analysed as locked and described as reported within Presence (finding 03). (4) The
locked "six parts" name stays, with the drafted subtitle (paper title page: "Are the Six Parts of AI Availability
Separate Readings of a Brand?" / "A Pre-Registered Structure Test of Six Provisional Components on the Newest
Models"). (5) REPORT_CODE. (6) TITLE. (7) "provisional" meets the S&P "(prelim)" rule (standing rule 1, Pablo, Mon
2026-11-23): every Preview score and chart already carries "provisional", so no separate "(prelim)" label is added.
(8) A new "all parts" group in the website's Methodology ledger (scripts/methodology_data.py, website branch
site-preview-6.0-draft). (9) COVER.
"""

REPORT_CODE = "TS-SY-AIAS6.0Preview-r1"      # decided (Pablo, Wed 2026-11-25, 7:15 am CT, call 5)
TIER = 1                                      # CLAUDE.md: Tier 1 Flagship includes the AIAS 6.0 Preview
# Call 9 (Pablo, Wed 2026-11-25, 7:15 am CT): the next unused A-pool image. A04 ("Wave facade"): first id in pool order
# never used on a published page or report (A01-A03, A07-A11 and A14 were on the website's category study pages on
# Nov 11-12, 2026, website commit 384fe34, replaced by d8d0d3a; A17 Literature 2.0; A18 AIAS 2.0 r3; A05/A06 are C3
# only); A04 was only reserved for v0.40 and freed when v0.40 took v0.40_airlines (brand file usage_record). The
# brand file's usage_record entry is added with the real build (locked file: diff to Pablo first).
COVER = "A04"

TITLE = "All the Parts at Once"               # decided (Pablo, Wed 2026-11-25, 7:15 am CT, call 6); every outcome class
DECK = ("{{v:pv.title}}: how the parts of AI Availability relate when all are measured on the same "
        "brands, models and week")

STANDFIRST = [
    {"requires": ["STRUCT"],
     "text": "We read every part of AI Availability that has been measured on the newest AI models, for the same "
             "{{v:pv.units}} brands, and asked whether they are separate readings of a brand. {{v:pv.report_headline}}"},
    {"requires": ["!STRUCT"],
     "text": "We read every part of AI Availability that has been measured on the newest AI models, for the same "
             "{{v:pv.units}} brands. {{v:pv.report_headline}}"},
]

GLANCE_NUMBERS = [
    {"requires": ["STRUCT"], "value": "{{v:pv.K.n}}", "unit": "",
     "label": "Parts included in the structure test (provisional)",
     "source": "of six parts; the state of each in finding 03"},   # the names overflow the number row at k >= 5
    # no structure test: no "structure test" count (Pablo, Wed 2026-11-25, 8:38 am CT, Preview report point 3)
    {"requires": ["!STRUCT"], "value": "{{v:pv.K.n}}", "unit": "",
     "label": "Parts that passed their own first test or are published",
     "source": "of six parts; the state of each in finding 03"},
    {"requires": ["STRUCT"], "value": "{{v:pv.pc.rho_2dp}}", "unit": "",
     "label": "Rank correlation of Presence with Consistency on the newest models",
     "source": "within categories, {{v:pv.pc.n}} brands; pre-set bar {{v:pv.band.confirm}}"},
    {"requires": ["STRUCT"], "value": "{{v:pv.uk.n}}", "unit": "",
     "label": "Brands rated on every included part",
     "source": "of {{v:pv.units}} brands in five categories"},
    # no structure test (section 4.3): the number row still takes three numbers (ts_layout.number_row); big numbers
    # print two decimals (a signed three-decimal value is wider than its column)
    {"requires": ["!STRUCT"], "value": "{{v:pv.units}}", "unit": "",
     "label": "Brands in the five category registries",
     "source": "each part read from its own locked study"},
    {"requires": ["!STRUCT"], "value": "{{v:pv.bridge.rho_P_2dp}}", "unit": "",
     "label": "Rank correlation of Presence now with Presence in AIAS 2.0",
     "source": "within categories, {{v:pv.bridge.n_P}} brands; descriptive"},
]

MEASURED = ("Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon, the newest flagship of three providers, in the "
            "week of the fourth omnibus wave: {{v:pv.units}} brands in headphones, skincare, cosmetics, cars and "
            "spirits. No new question was asked: each part's score comes from its own locked study. Plan, scorer "
            "and deviations record: osf.io/ec6wh (aias_6_0_preview), pre-registration {{v:pv.prereg_tag}}.")

SUMMARY = [
    "AIAS™ describes how AI answers treat a brand in parts. Presence and Consistency are published; the others "
    "are provisional and each has had one test of its own. This preview is the first time the parts are read "
    "together, on the same brands and the same three models. {{v:pv.k_sentence}} {{v:pv.report_headline}}",
    {"requires": ["STRUCT"], "text": "{{v:pv.w1}} No single AIAS number per brand is published: the parts are "
                                     "shown side by side."},
]

INTRO_LEAD = ("Is a brand's place in AI answers one thing, or several? This preview reads every part measured so far "
              "on the same brands and the same models, and tests whether each adds something the others do not.")

INTRO = [
    "AIAS™, the AI Availability Score, reports each part of how AI answers treat a brand as its own score from 0 "
    "to 100. Two are published: Presence, how often AI answers name a brand, and Consistency, how evenly "
    "different models name it. Ranking, where a brand sits in an answer, is reported as part of Presence after "
    "its last redesign; Sentiment, Coverage and Grounding are still in their first tests. Each part was tested "
    "against Presence and Consistency in its own study, but never against the others on the same brands.",
    "This preview does that, provisionally. It reads each part in the state its own first test gave it, keeps "
    "only the parts that passed in the structure test, and asks whether each one can be predicted from the "
    "others, one at a time and all together. Every test, bar and headline wording was fixed and deposited before "
    "any score on the newest models existed.",
    "{{v:pv.validation_line}}",
]

MEASURED_HEAD = "What we measured"
MEASURED_PARAS = [
    "Brands. The {{v:pv.units}} brands of five category studies (headphones, skincare, cosmetics, cars and "
    "spirits), unchanged since their first wave in May 2026.",
    "Models and week. Claude Fable 5.2, GPT-6 Astra and Gemini 4 Argon in the week of the fourth omnibus wave. "
    "Coverage comes from its own questions to the same models that week; Grounding from answers with web search "
    "on, every other part from answers with search off.",
    "Rules. A pair of parts counts as separate when the rank correlation of their scores within each category is "
    "at most {{v:pv.band.confirm}}, and as overlapping at {{v:pv.band.falsify}} or above; in between, it is "
    "partly separate. The same bars apply to each part against all earlier parts together. Intervals come from "
    "{{v:pv.n_boot}} resamples and chance levels from {{v:pv.n_perm}} reshuffles within category.",
    "Parts that did not pass their own first test are not in the structure test: a part under review is shown "
    "below the profile and counts in no result; a part not yet scored is pending.",
]

# One chart per finding. Chart titles say what is plotted and never repeat or paraphrase the finding title.
CHARTS = {
    "report_fig_01_pairs.pdf": {
        "requires": ["STRUCT"],
        "title": "Within-category rank correlation for each pair of included parts",
        "subtitle": "Pre-set bars at {{v:pv.band.confirm}} and {{v:pv.band.falsify}}; parts under review in a "
                    "separate lower band (provisional)"},
    "report_fig_02_presence_consistency.pdf": {
        "requires": ["STRUCT"],
        "title": "Presence rank against Consistency rank, by category",
        "subtitle": "{{v:pv.pc.n}} brands rated on both, newest models (provisional)"},
    "report_fig_03_part_states.pdf": {
        "title": "State of each part at the data lock",
        "subtitle": "As each part's own first test issued it (provisional)"},
    "report_fig_04_parts_per_brand.pdf": {
        "title": "Brands by number of included parts rated, per category",
        "subtitle": "{{v:pv.units}} brands, five categories (provisional)"},
    "report_fig_05_average_vs_presence.pdf": {
        "requires": ["STRUCT"],
        "title": "Rank correlation of the parts' average with Presence",
        "subtitle": "Against the pre-set limit of {{v:pv.k2_max}} (descriptive; provisional)"},
}

# Findings (P1-P5). Titles are fixed per outcome, written before the data; the body carries the section 6.6
# report-only headline through {{v:pv.report_headline}} (8:38 am, point 2). Class C has no report: drafting pauses (pre-registration 6.6).
FINDINGS = [
    {"requires": ["STRUCT"],
     "verdict": "{{v:pv.structure.verdict}}",
     "title_by_class": [
         # titles under 58 characters (contents page); "of a brand" is in the body's section 6.6 headline
         {"requires": ["CLASS=A"], "text": "On the newest models, the parts are separate readings"},
         {"requires": ["CLASS=A_k"], "text": "The parts measured so far are separate readings"},
         {"requires": ["CLASS=B"], "text": "Most parts are separate readings; some overlap"},
         {"requires": ["CLASS=U"], "text": "How the parts relate could not be determined"},
     ],
     "chart": "report_fig_01_pairs.pdf",
     "caption": "Dot: rank correlation within category of each pair of included parts; bar: its 90% interval; "
                "shaded: the pre-set bars. Parts under review are shown below, descriptive only. Provisional.",
     "body": [
         "{{v:pv.report_headline}}",
         "The test compared every pair of included parts, and each part with all earlier parts together. Of the "
         "{{v:pv.structure.k}} included parts, {{v:pv.structure.d}} were separate or partly separate readings "
         "(Presence counted as the anchor). Separate: {{v:pv.structure.distinct}}. Partly separate: "
         "{{v:pv.structure.partly}}. Not separate: {{v:pv.structure.not_distinct}}.",
     ]},
    {"requires": ["STRUCT"],
     "verdict": "{{v:pv.pc.verdict}}",
     "title_by_class": [
         {"requires": ["PC=CONFIRMED"], "text": "Presence and Consistency stay apart on the newest models"},
         {"requires": ["PC=MARGINAL"], "text": "Presence and Consistency stay apart, with some coupling"},
         {"requires": ["PC=FALSIFIED"], "text": "On the newest models, Consistency moves with Presence"},
         {"requires": ["PC=UNDETERMINED"], "text": "Too few brands to tell Presence and Consistency apart"},
     ],
     "chart": "report_fig_02_presence_consistency.pdf",
     "caption": "Each dot a brand rated on both scores; ranks centred within its category. Provisional.",
     "body": [
         "{{v:pv.w1}}",
         "Across the {{v:pv.pc.n}} brands rated on both, the rank correlation within categories was "
         "{{v:pv.pc.rho}} (90% interval {{v:pv.pc.lo}} to {{v:pv.pc.hi}}), against a pre-set bar of "
         "{{v:pv.band.confirm}}. AIAS 2.0 showed the two scores apart on an older panel of six models; this is "
         "the first test of that result on the newest models.",
     ]},
    {"verdict": "",
     "title": "Each part is shown with the state of its own first test",
     "chart": "report_fig_03_part_states.pdf",
     "caption": "State as each part's own study issued it at the data lock; label as the plan assigns it. "
                "Provisional.",
     "body": [
         "Presence: {{v:pv.label.P}}, {{v:pv.bridge.P}}. Consistency: {{v:pv.label.C}}, {{v:pv.bridge.C}}. "
         "Ranking: {{v:pv.state.R}} ({{v:pv.label.R}}). Sentiment: {{v:pv.state.S}} ({{v:pv.label.S}}). "
         "Coverage: {{v:pv.state.Cov}} ({{v:pv.label.Cov}}). Grounding: {{v:pv.state.G}} ({{v:pv.label.G}}).",
         {"requires": ["CASE_R=MARGINAL|PASS_RETEST_PENDING"],
          "text": "Ranking's final reading needs the retest wave; until then every Ranking "
                  "result here is provisional, retest pending."},
         # call 3: Ranking analysed as locked, described as reported within Presence
         "Ranking is read here as this preview's locked plan defines it; the published score reports Ranking as "
         "part of Presence.",
         {"requires": ["W2", "!S_FALLBACK_PENDING"],
          "text": "Sentiment has no score yet on the newest models' answers, so it is not in the structure test."},
         # call 2: the legacy-panel fallback printed as pending, with its cause
         {"requires": ["W2", "S_FALLBACK_PENDING"],
          "text": "Sentiment has no score yet on the newest models' answers, so it is not in the structure test. "
                  "The planned fallback, Sentiment on the older model panel, is pending: that study issued no "
                  "verdict file, because its judging step stopped under its own pre-set rule."},
     ]},
    {"requires": ["STRUCT"],
     "verdict": "",
     "title": "The full profile leans to brands that are named often",
     "chart": "report_fig_04_parts_per_brand.pdf",
     "caption": "Brands by how many included parts rate them, per category. A part rates a brand only when "
                "answers name it often enough. Provisional.",
     "body": [
         "{{v:pv.uk.n}} of the {{v:pv.units}} brands are rated on every included part. Every part needs a brand "
         "to be named often enough before it can rate it, so the full profile leans to well-named brands.",
     ]},
    {"requires": ["STRUCT"],
     "verdict": "",
     "title": "An average of the parts is not published",
     "chart": "report_fig_05_average_vs_presence.pdf",
     "caption": "Rank correlation of the equal-weight average of the included parts with Presence; dashed line: "
                "the pre-set limit. Descriptive; nothing adopted. Provisional.",
     "body": [
         "As in AIAS 2.0, the parts are shown side by side. As a check only, the equal-weight average of the "
         "included parts ranked brands with a correlation of {{v:pv.comp.rho_AP}} to Presence (limit "
         "{{v:pv.k2_max}}): it {{v:pv.comp.k2}} the added-information rule and {{v:pv.comp.k3}} the no-windfall "
         "rule ({{v:pv.k3_points}} points). No combined score is adopted in a preview.",
     ]},
]

SCORED_HEAD = "The pre-set tests, scored"
SCORED_INTRO = ("Each test, its bar and the wording of every possible headline were deposited before any score on "
                "the newest models existed. Outcomes use the pre-set words and were computed once by the locked "
                "scoring script. Later changes to a part's state enter only as dated addenda, listed with the "
                "original result.")
SCORED_ROWS = [
    {"requires": ["STRUCT"],
     "row": ["01", "The included parts are separate readings of a brand, pair by pair and each against all earlier "
                   "parts together",
             "{{v:pv.structure.verdict}} ({{v:pv.structure.d}} of {{v:pv.structure.k}} parts separate or partly "
             "separate; bars {{v:pv.band.confirm}} and {{v:pv.band.falsify}})"]},
    {"requires": ["STRUCT"],
     "row": ["02", "Presence and Consistency stay apart on the newest models",
             "{{v:pv.pc.verdict}} (rank correlation {{v:pv.pc.rho}}, 90% interval {{v:pv.pc.lo}} to {{v:pv.pc.hi}}, "
             "{{v:pv.pc.n}} brands)"]},
    {"requires": ["!STRUCT"],
     "row": ["01", "The included parts are separate readings of a brand", "{{v:pv.structure.verdict}}"]},
    {"row": ["", "Pre-set checks: plan locked and unchanged, every part's file is the one its study scored, the same "
                 "brands in every file, the Presence and Consistency recomputation matches",
             "See the methodology log (osf.io/ec6wh, aias_6_0_preview)"]},
]

LIMITS_HEAD = "Limitations"
LIMITS = [
    "One week of answers from three models, one per provider, in US English, on five categories whose brands were "
    "fixed in May 2026. Answers change between model versions.",
    "The parts come from two collections and two search settings within one week: Grounding from answers with web "
    "search on, the others from answers with search off.",
    "Every part rates a brand only once answers name it often enough, so the brands with a full profile lean to "
    "well-named brands, and correlations with Presence are computed on a narrower range of Presence.",
    "Separate is not the same as valid: no part is tested here against what buyers do. Four of the six parts are "
    "provisional and none has completed its validation.",
    "Sentiment is judged by AI models; the check against human labels is a separate study.",
    "Fixed bars, many tests and no correction for multiplicity: a part needs every one of its tests inside the "
    "bar to count as separate, so small true overlaps can still show as partly separate.",
]

NEXT_HEAD = "What's next"
NEXT = [
    "Each provisional part becomes a released AIAS score only after its own second study and calibration; the "
    "next releases are AIAS 3.0 to 5.0. Ranking's retest, and any part scored after the data lock, enter this "
    "preview as dated addenda before its paper is locked.",
    "Plan, scorer, outputs and deviations record: osf.io/ec6wh (aias_6_0_preview). Code: "
    "github.com/thirdsystem-aias/aias, tag {{v:pv.prereg_tag}}.",
]

DISCLOSURES = {
    "conflicts_of_interest": "The author is employed by a consumer-electronics company. This preview selects no "
                             "brands: it reads scores computed on five registries fixed in earlier studies, each "
                             "with its own conflict-of-interest handling. Denon, which replaced a group-owned "
                             "headphone brand before the headphones study was locked, has itself been owned by a "
                             "subsidiary of the company's group since September 23, 2025, which was noticed on "
                             "November 10, 2026; it stays in the analysis, and every structure result is also "
                             "computed without it. Group subsidiaries supply components (audio systems, battery "
                             "cells, displays) to several brands in the car registry, a non-competitive "
                             "relationship disclosed without restriction. A group advertising affiliate or its "
                             "agency has worked for five registry brands (Chevrolet, BMW, Bentley, Jack Daniel's "
                             "and Eucerin); they stay in every analysis. The company had no role in this work; it "
                             "and its affiliates are named in the paper's Declarations.",
    "held_out_brands": "No brand was held out. The registries are those of the five category studies, unchanged.",
    "ai_use": "During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with "
              "study design, analysis and writing. The author reviewed and edited all content and takes full "
              "responsibility for it.",
    "independence": "Self-funded. No brand was contacted, sponsored the work or saw it before publication. Every "
                    "result was computed once by the locked scoring script from locked study files.",
}

CLOSING_STATEMENT = [
    {"requires": ["STRUCT"], "text": "{{v:pv.report_headline}}"},
    {"requires": ["!STRUCT"], "text": "The parts are shown side by side; how they relate is not yet determined."},
]
