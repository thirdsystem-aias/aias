"""v0.40 flagship report: content (managerial register). Every number is a {{v:KEY}} placeholder filled from
osf/v40/v40_values.json by build_report_v40_r1.py through values_v0_40.fill(); none is typed here.
No hypothesis labels; plain words; "named", not "recommended", for what the measure counts."""

TITLE = "Leaders, challengers and ghosts"
DECK = ("How nine AI models name US airlines and retail banks against market share, "
        "and what they say about brands that are gone")

STANDFIRST = ("We asked nine AI models, older and newest, which US airlines and banks to use, and whether brands "
              "that merged away or failed still operate. Their naming follows the market's order. When asked "
              "directly, they say a departed brand is gone.")

GLANCE_NUMBERS = [
    {"value": "{{v:H_Reinforce.bank.rho}}", "unit": "", "label": "Rank correlation of bank market share with AI naming",
     "source": "{{v:H_Reinforce.bank.n_units}} bank holders, nine models"},
    {"value": "{{v:H_Flag.ghost_rate}}", "unit": "", "label": "Status answers that say a departed brand is gone",
     "source": "{{v:H_Flag.ghost_flagged}} of {{v:H_Flag.ghost_answers}} answers"},
    {"value": "{{v:H_Search.post_cutoff_s1_flagged}}", "unit": "of {{v:H_Search.post_cutoff_cells}}",
     "label": "Exits after a model's cutoff flagged with web search",
     "source": "newest models, search on; a small count"},
]

MEASURED = ("Six older models and the newest model of three providers, each with and without its own web search, "
            "answered {{v:acquisition.records_total}} questions in November 2026: which airline or bank to use, "
            "whether a brand is known, and whether one can still book with it or open an account.")

SUMMARY = [
    "Across both categories the models named brands roughly in the order of their market share. The bank result "
    "held in every check; the airline result rests on how one small airline is counted. Departed brands were seldom "
    "named in recommendations without a word that they had gone, and when asked directly the models said so in "
    "nearly every answer. Whether the leaders get more than their share could not be tested as designed (finding 02).",
]

INTRO_LEAD = ("Brands leave markets on known dates. AI models stop learning on known dates. "
              "This study used the gap between the two.")

INTRO = [
    "US airlines and retail banks have official market shares (passenger miles from the Bureau of Transportation "
    "Statistics; deposits from the FDIC) and many brands that left through a merger, a failure or a rename since "
    "2008, such as Continental, US Airways, Washington Mutual, Wachovia, SunTrust and Silicon Valley Bank. We call "
    "them ghosts. The study asked whether AI answers follow the market, favour the leader, keep ghosts alive, "
    "let them fade, say they are gone, and whether web search corrects them.",
    "Every test and every threshold was fixed and published before the first question was sent, and every result "
    "is reported here, including the ones that failed. The study is independent: no brand is its focus, no finding "
    "is addressed to a brand, and no brand was contacted.",
]

MEASURED_HEAD = "What we measured"
MEASURED_PARAS = [
    "Each model answered brand-free recommendation questions for each category (in general, by need and by US "
    "region), three times with search off; the newest models answered once more with search on. For each ghost "
    "and each living control brand it also answered whether it knew the brand and whether one could still use it.",
    "An answer names a brand when it contains one of the brand's registered names. A brand's share of AI naming "
    "is how often it is named, out of all namings of the category's current brands. A mention counts as saying "
    "the brand is gone when words such as \"merged into\", \"acquired by\" or \"no longer\" appear within "
    "{{v:window_chars}} characters of it. Coding was automatic; two AI coders from other providers checked a sample "
    "of {{v:audit.answers.total}} answers, with no human check.",
]

FINDINGS = [
    {"verdict": "{{v:H_Reinforce.verdict}}",
     "title": "AI names brands in the market's order",
     "chart": "report_fig_01_share_order.pdf",
     "caption": "Each dot is a rank correlation between market share and share of AI naming; 1 would be the "
                "market's exact order. Filled: below the pre-set bar. Older models: six; newest: three.",
     "body": [
         "Across the nine models, brands with more of the market were named more often: a rank correlation of "
         "{{v:H_Reinforce.airline.rho}} for airlines and {{v:H_Reinforce.bank.rho}} for banks, both above the "
         "pre-set bar of {{v:thresholds.reinforce_rho}}. For banks this held in every version we had set in advance, "
         "including without the brokerage holders ({{v:sensitivity.S-D4.rho}}).",
         "The airline result is fragile. With only {{v:H_Reinforce.airline.n_units}} airline units, counting Sun "
         "Country inside Allegiant drops the correlation to {{v:sensitivity.S-SunCountry.H_Reinforce_airline.rho}}, "
         "below the bar, and the newest models alone reach only "
         "{{v:sensitivity.S-Arm.current.H_Reinforce.airline.rho}}. For airlines, read this as a tendency.",
     ]},
    {"verdict": "{{v:H_Amplify.verdict}}",
     "title": "The leaders get less than their share",
     "chart": "report_fig_02_leader_multiple.pdf",
     "caption": "The leader's share of all brand namings divided by its share of the market; 1 means the same as "
                "the market. The test counts every brand named in an answer, so even a leader named in every "
                "answer stays below the amplified line.",
     "body": [
         "American received {{v:H_Amplify.airline.ratio}} times and the JPMorgan Chase holder "
         "{{v:H_Amplify.bank.ratio}} times their market share of all brand namings, so the pre-set prediction that "
         "AI amplifies the leader failed. That result says less than it seems. Each answer names several brands, "
         "and the measure divides the leader's answers by all namings. Given how often the other brands were named, "
         "a leader named in every answer would still fall short of the amplified line for airlines and of the "
         "market's share for banks.",
         "The JPMorgan Chase holder was in fact named in {{v:H_Amplify.bank.k}} of the "
         "{{v:descriptives.8_near_floor_other.L_S0.answers}} older-model and "
         "{{v:descriptives.8_near_floor_other.C_S0.answers}} newest-model bank recommendation answers. Whether "
         "AI favours leaders needs a measure built per answer.",
     ]},
    {"verdict": "{{v:H_Afterlife.verdict}}",
     "title": "Few departed brands are named as current",
     "chart": "report_fig_03_departed_named.pdf",
     "caption": "Share of departed-brand and model pairs in which the model named the brand in a recommendation "
                "without a word that it had gone. Floor and bar were set in advance. Only brands that left before "
                "the model's training cutoff count.",
     "body": [
         "Ghosts were named without any sign that they had gone in {{v:H_Afterlife.airline.rate}} of airline "
         "and {{v:H_Afterlife.bank.rate}} of bank pairs: above the floor of {{v:thresholds.afterlife_null}} but far "
         "below the bar of {{v:thresholds.afterlife_rate}}, so the test is undecided.",
         "These rates are more likely too high than too low. In the checked sample the automatic coder missed "
         "more \"gone\" wording in recommendation answers than it added (agreement {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.kappa}} "
         "on those answers, against {{v:audit.threshold.kappa}} overall).",
     ]},
    {"verdict": "{{v:H_Decay.verdict}}",
     "title": "Brands gone longer are named less",
     "chart": "report_fig_04_fade.pdf",
     "caption": "Rank correlation between the months from a brand's exit to a model's training cutoff and how "
                "often that model names the brand. Negative means it fades. Labels give the pairs named at all.",
     "body": [
         "Across all pairs the correlation was {{v:H_Decay.rho}}: a clear fade, just short of the strong fade "
         "set in advance ({{v:thresholds.decay_rho}}). The older models alone passed it "
         "({{v:sensitivity.S-Arm.legacy.H_Decay.rho}}).",
         "Most departed brands are never named at all, so the pattern rests on {{v:H_Decay.pairs_present}} of "
         "{{v:H_Decay.pairs}} pairs. The newest models named too few to test. The data show a link, not its cause.",
     ]},
    {"verdict": "{{v:H_Flag.verdict}}",
     "title": "Asked, the models say the brand is gone",
     "chart": "report_fig_05_status_answers.pdf",
     "caption": "Share of answers to \"can I still book with / open an account at...\" that carry gone wording. "
                "Departed: brands that left before the model's cutoff. Living: control brands and the four "
                "incumbents.",
     "body": [
         "The models said a departed brand was gone in {{v:H_Flag.ghost_flagged}} of {{v:H_Flag.ghost_answers}} "
         "answers, against {{v:H_Flag.control_rate}} for living brands. The newest models flagged every departed "
         "brand.",
         "The living-brand rate is not all error. Two control brands were in recent mergers or account moves "
         "(Hawaiian with Alaska, Discover with Capital One), and an answer that says so carries the same words. "
         "The newest models used them about living brands more often ({{v:sensitivity.S-Arm.current.H_Flag.control_rate}}).",
     ]},
    {"verdict": "{{v:H_Search.verdict}}",
     "title": "With search on, every late exit was flagged",
     "chart": "report_fig_06_search_status.pdf",
     "caption": "Newest models, status questions about departed brands. A cell is one brand asked of one model. "
                "The pre-set paired test needed at least ten cells that changed with search.",
     "body": [
         "Some brands left after a model stopped learning, such as Silicon Valley Bank for all three newest "
         "models. With search on, all {{v:H_Search.post_cutoff_cells}} such cells were flagged as gone. The count "
         "is small, and there is no search-off comparison for them.",
         "Elsewhere search had little left to fix: without it the newest models already flagged nearly every "
         "departed brand. Only {{v:H_Search.s1_only_flagged}} cell changed toward gone with search and "
         "{{v:H_Search.s0_only_flagged}} the other way. One model searched in only "
         "{{v:manipulation_checks.MC2_search_used_C3.searched}} of {{v:manipulation_checks.MC2_search_used_C3.n}} "
         "search-on answers.",
     ]},
]

SCORED_HEAD = "The six pre-set tests, scored"
SCORED_INTRO = ("Each test, its bar and its outcome were published before the first question. Outcomes use the "
                "pre-set words; none was changed after the data came in.")
SCORED_ROWS = [
    ["01", "Naming follows market share in both categories", "{{v:H_Reinforce.verdict}}"],
    ["02", "The leader gets more than its market share", "{{v:H_Amplify.verdict}} (measure could not show it; finding 02)"],
    ["03", "Departed brands are still named as current", "{{v:H_Afterlife.verdict}}"],
    ["04", "Naming fades with time since exit", "{{v:H_Decay.verdict}} (fade found, below the strong bar)"],
    ["05", "Status answers say a departed brand is gone", "{{v:H_Flag.verdict}}"],
    ["06", "Web search corrects departed-brand status", "{{v:H_Search.verdict}} (one of two parts passed)"],
]

LIMITS_HEAD = "Limitations"
LIMITS = [
    "One market, one language, two categories, three days in November 2026, and questions asked without a "
    "buyer persona. Answers change between model versions.",
    "Search on was run once per question, and one model often chose not to search.",
    "Coding is automatic and reads words near a brand's name; it misses paraphrases and also fires on living "
    "brands that went through a merger. Its check used AI coders only, one of which is also a model in the study.",
    "The leader test counts all brand namings, which caps how high the leader's multiple can go (finding 02).",
    "The published plan's first line still reads \"draft\"; the lock rests on the dated git tag and the "
    "OSF deposit made before the first question.",
]
NEXT_HEAD = "What's next"
NEXT = [
    "A second wave on the same brands and questions, with more search-on runs and a persona arm, and a "
    "per-answer measure of whether AI favours the leader. Data, plan and paper are on OSF (osf.io/ec6wh, v40).",
]

DISCLOSURES = {
    "conflicts_of_interest": "The author is employed by a consumer-electronics company that does not compete in "
                             "US airlines or retail banking; the company and its affiliates are named, with the "
                             "registry screen, in the paper's Declarations. No registry brand has a recorded tie.",
    "held_out_brands": "No brand was held out. The registry was built mechanically from official data (BTS, FDIC) "
                       "and frozen before the first question.",
    "ai_use": "The models studied produced the answers; Claude Fable 5.2 and GPT-6.2 Astra, with Gemini 4 Carbon "
              "breaking ties, checked the coding of a sample; Anthropic's Claude assisted with design, analysis and "
              "writing, which the author reviewed.",
    "independence": "Self-funded. No brand was contacted, sponsored the work or saw it before publication.",
}

CLOSING_STATEMENT = ("AI answers about airlines and banks follow the market's order, and when asked, they say "
                     "which brands are gone.")
