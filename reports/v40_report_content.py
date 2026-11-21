"""v0.40 flagship report: content (managerial register). Every result number is a {{v:KEY}} placeholder filled from
osf/v40/v40_values.json by build_report_v40_r1.py through values_v0_40.fill(); none is typed here. Design counts
(nine models, six older, three newest, three runs) follow the locked pre-registration (§2.1, §4.2).
No hypothesis labels; plain words; "named", not "recommended", for what the measure counts.
Revised after the row 32 review gate of 2026-11-21 (reviews/v0.40-report/2026-11-21.md)."""

TITLE = "Leaders, challengers and ghosts"
DECK = ("How nine AI models name US airlines and retail banks against market share, "
        "and what they say about brands that are gone")

STANDFIRST = ("We asked nine AI models, older and newest, which US airlines and banks to use, and whether brands "
              "that merged away or failed still operate. Their naming broadly follows the market's order, firmly "
              "for banks. Asked directly, they say a departed brand is gone.")

GLANCE_NUMBERS = [
    {"value": "{{v:H_Reinforce.bank.rho}}", "unit": "", "label": "Rank correlation of bank market share with AI naming",
     "source": "1 = the market's exact order; pre-set bar {{v:thresholds.reinforce_rho}}"},
    {"value": "{{v:H_Flag.ghost_rate}}", "unit": "", "label": "Status answers with gone wording for departed brands",
     "source": "{{v:H_Flag.ghost_flagged}} of {{v:H_Flag.ghost_answers}} answers"},
    {"value": "{{v:H_Amplify.bank.ratio}}", "unit": "x", "label": "Bank leader's share of naming, as a multiple of its market share",
     "source": "below 1: less than its market share"},
]

MEASURED = ("Six older models and the newest model of three providers (the newest also with their own web search) "
            "gave {{v:acquisition.records_total}} answers in November 2026: which airline or bank to use, whether a "
            "brand is known, and whether one can still book with it or open an account. All numbers: the study's "
            "values file, osf.io/ec6wh (v40).")

SUMMARY = [
    "The models named brands roughly in the order of their market share: firmly for banks, less firmly for airlines. "
    "The largest airline and bank got less than their market share of naming, so the pre-set prediction that AI "
    "favours leaders failed on this measure (finding 02). Departed brands were sometimes named without a word that "
    "they had gone, at rates the test could not settle; asked directly, the models said they were gone in nearly "
    "every answer.",
]

INTRO_LEAD = ("Brands leave markets on known dates. AI models stop learning on known dates. "
              "This study used the gap between the two.")

INTRO = [
    "AIAS™, the AI Availability Score, measures how AI answers represent brands. This study applied it to US "
    "airlines and retail banks, which have official market shares (passenger miles from the Bureau of Transportation "
    "Statistics; deposits from the FDIC) and many brands that left through a merger, a failure or a rename since "
    "2008, such as Continental, US Airways, Washington Mutual, Wachovia, SunTrust and Silicon Valley Bank. We call "
    "them ghosts. Banks are counted by holding company (JPMorgan Chase, Bank of America and so on).",
    "Every test and threshold was fixed and published before the first question, and every result is reported "
    "here, including the ones that failed. One step changed after collection: the plan named a human to check the "
    "coding; this was changed to three AI coders, with no human check (a declared deviation). All pre-set quality "
    "checks passed except one: Gemini 4 Argon used web search in only "
    "{{v:manipulation_checks.MC2_search_used_C3.searched}} of {{v:manipulation_checks.MC2_search_used_C3.n}} "
    "search-on answers, below the pre-set bar. The study is independent: no brand is its focus, no finding is "
    "addressed to a brand, and no brand was contacted.",
]

MEASURED_HEAD = "What we measured"
MEASURED_PARAS = [
    "Each model answered brand-free recommendation questions for each category (in general, by need and by US "
    "region), three times with search off; the newest models answered once more with search on. For each ghost "
    "and each control brand (living brands, including the four biggest incumbents) it also answered whether it knew "
    "the brand and whether one could still use it.",
    "An answer names a brand when it contains one of the brand's registered names. A brand's share of AI naming "
    "is how often it is named, out of all namings of the category's current brands; a rank correlation compares that "
    "order with the market's (1 = same order). A mention counts as saying the brand is gone when words such as "
    "\"merged into\", \"acquired by\" or \"no longer\" appear within {{v:window_chars}} characters of it. Coding was "
    "automatic; three AI coders, one of them also a model in the study, checked a sample of "
    "{{v:audit.answers.total}} answers.",
]

FINDINGS = [
    {"verdict": "{{v:H_Reinforce.verdict}}",
     "title": "Naming follows market share, firmly for banks",
     "chart": "report_fig_01_share_order.pdf",
     "caption": "Each dot is a rank correlation between market share and share of AI naming; 1 would be the "
                "market's exact order. Filled: below the pre-set bar. Older models: six; newest: three.",
     "body": [
         "Across the nine models, brands with more of the market were named more often: a rank correlation of "
         "{{v:H_Reinforce.airline.rho}} for airlines and {{v:H_Reinforce.bank.rho}} for banks, both above the "
         "pre-set bar of {{v:thresholds.reinforce_rho}}. For banks this held in every version set in advance, "
         "including without the three brokerage firms that hold bank deposits ({{v:sensitivity.S-D4.rho}}).",
         "The airline result is fragile. With only {{v:H_Reinforce.airline.n_units}} airline units, counting Sun "
         "Country's share together with Allegiant's, an alternative grouping the registry records, drops the "
         "correlation to {{v:sensitivity.S-SunCountry.H_Reinforce_airline.rho}}, below the bar, and the newest models "
         "alone reach only {{v:sensitivity.S-Arm.current.H_Reinforce.airline.rho}}.",
     ]},
    {"verdict": "{{v:H_Amplify.verdict}}",
     "title": "On this measure, the leaders get less than their share",
     "chart": "report_fig_02_leader_multiple.pdf",
     "caption": "The leader's share of all brand namings divided by its share of the market; 1 means the same as "
                "the market. Filled: all nine models; open: model groups. The amplified line was set in advance.",
     "body": [
         "American received {{v:H_Amplify.airline.ratio}} times and the JPMorgan Chase holding company "
         "{{v:H_Amplify.bank.ratio}} times their market share of all brand namings: less than their share in both "
         "categories, so the pre-set prediction that AI amplifies the leader failed. For the newest models alone the "
         "bank figure was {{v:sensitivity.S-Arm.current.H_Amplify.bank.ratio}}, undecided.",
         "An added check, not in the plan: each answer names several brands, so even a leader named in every answer "
         "would not have reached the amplified line at this breadth of answers, and in banks not its market share. "
         "JPMorgan Chase was in fact named in {{v:H_Amplify.bank.k}} of the bank recommendation answers "
         "({{v:descriptives.8_near_floor_other.L_S0.answers}} from older models, "
         "{{v:descriptives.8_near_floor_other.C_S0.answers}} from the newest).",
     ]},
    {"verdict": "{{v:H_Afterlife.verdict}}",
     "title": "Departed brands named as current: undecided",
     "chart": "report_fig_03_departed_named.pdf",
     "caption": "Share of departed-brand and model pairs in which the model named the brand in a recommendation "
                "without gone wording. Floor and bar were set in advance. Only brands that left before the model's "
                "training cutoff count.",
     "body": [
         "Ghosts were named without any sign that they had gone in {{v:H_Afterlife.airline.rate}} of airline "
         "and {{v:H_Afterlife.bank.rate}} of bank pairs: above the floor of {{v:thresholds.afterlife_null}} but far "
         "below the bar of {{v:thresholds.afterlife_rate}}, so the test is undecided.",
         "These rates are more likely too high than too low. The coding check met its pre-set bar overall (kappa "
         "{{v:audit.threshold.kappa}} against {{v:audit.threshold.kappa_min}}), but on recommendation answers kappa "
         "was {{v:audit.agreement.consensus_vs_rule.gone_flag.recommendation.kappa}}, and in the "
         "{{v:audit.sample_rates.rule.rec_ghost_mentions}} sampled ghost mentions the automatic coder missed more gone "
         "wording than it added.",
     ]},
    {"verdict": "{{v:H_Decay.verdict}}",
     "title": "Brands gone longer are named less",
     "chart": "report_fig_04_fade.pdf",
     "caption": "Rank correlation between the months from a brand's exit to a model's training cutoff and how "
                "often that model names the brand. Negative means it fades. Filled: all nine models.",
     "body": [
         "Across all pairs the correlation was {{v:H_Decay.rho}}: a fade, just short of the strong fade set in "
         "advance ({{v:thresholds.decay_rho}}). On the older models alone it was "
         "{{v:sensitivity.S-Arm.legacy.H_Decay.rho}} (a check, not a test).",
         "Most departed brands are never named at all, so the pattern rests on {{v:H_Decay.pairs_present}} of "
         "{{v:H_Decay.pairs}} pairs. The newest models named too few to test. The data show a link, not its cause.",
     ]},
    {"verdict": "{{v:H_Flag.verdict}}",
     "title": "Asked, the models say the brand is gone",
     "chart": "report_fig_05_status_answers.pdf",
     "caption": "Share of answers to \"can I still book with / open an account at...\" that carry gone wording. "
                "Departed: brands that left before the model's cutoff. Living: three control brands and the four "
                "biggest incumbents (American, Delta, Chase, Bank of America).",
     "body": [
         "The models' answers carried gone wording for a departed brand in {{v:H_Flag.ghost_flagged}} of "
         "{{v:H_Flag.ghost_answers}} cases, against {{v:H_Flag.control_rate}} for living brands. The newest models "
         "did so for every departed brand.",
         "The living-brand rate is not all error. The three control brands, Hawaiian, Sun Country and Discover, have "
         "been through mergers or account moves, and an answer that says so carries the same words. Without Discover "
         "the living-brand rate was {{v:sensitivity.S-Discover.control_rate}}; for the newest models it was "
         "{{v:sensitivity.S-Arm.current.H_Flag.control_rate}}.",
     ]},
    {"verdict": "{{v:H_Search.verdict}}",
     "title": "Late exits were flagged; search changed little",
     "chart": "report_fig_06_search_status.pdf",
     "caption": "Newest models, status questions about departed brands. A cell is one brand asked of one model, "
                "compared with search off and on.",
     "body": [
         "Some brands left after a model stopped learning, such as Silicon Valley Bank for all three newest models. "
         "With search on, all {{v:H_Search.post_cutoff_cells}} such cells were flagged as gone. Most were already "
         "flagged without search: only {{v:H_Search.s1_only_flagged}} of all cells changed toward gone with search.",
         "The paired half of the test failed its pre-set floor: {{v:H_Search.s1_only_flagged}} cell changed toward "
         "gone and {{v:H_Search.s0_only_flagged}} the other way, against at least "
         "{{v:thresholds.search_min_discordant}} changed cells needed. Gemini 4 Argon searched in only "
         "{{v:manipulation_checks.MC2_search_used_C3.searched}} of {{v:manipulation_checks.MC2_search_used_C3.n}} "
         "search-on answers.",
     ]},
]

SCORED_HEAD = "The six pre-set tests, scored"
SCORED_INTRO = ("Each test, its bar and its outcome were published before the first question. Outcomes use the "
                "pre-set words; none was changed after the data came in. One step changed after collection: who "
                "checked the coding (a declared deviation).")
SCORED_ROWS = [
    ["01", "Naming follows market share in both categories", "{{v:H_Reinforce.verdict}}"],
    ["02", "The leader gets more than its market share", "{{v:H_Amplify.verdict}} (less than its share in both)"],
    ["03", "Departed brands are still named as current", "{{v:H_Afterlife.verdict}}"],
    ["04", "Naming fades with time since exit", "{{v:H_Decay.verdict}} (fade found, below the strong bar)"],
    ["05", "Status answers say a departed brand is gone", "{{v:H_Flag.verdict}}"],
    ["06", "Web search corrects departed-brand status", "{{v:H_Search.verdict}} (late exits flagged; paired half failed)"],
]

LIMITS_HEAD = "Limitations"
LIMITS = [
    "One market, one language, two categories, three days in November 2026, and questions asked without a "
    "buyer persona. Answers change between model versions.",
    "Search on was run once per question, and one model often chose not to search.",
    "Coding is automatic and reads words near a brand's name; it misses paraphrases and also fires on living "
    "brands that went through a merger. Its check used AI coders only, one of which is also a model in the study, "
    "in place of the human the plan named.",
    "The leader test divides answers by all brand namings, which caps how high the leader's multiple can go "
    "(finding 02).",
    "Pairs of brands and models share questions and runs, and the tests treat them as independent. Some "
    "pre-registered detail tables are not in the scored record; the paper lists them.",
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
                             "US airlines or retail banking; banking has an adjacency through the company's digital "
                             "wallet. The company and its affiliates are named, with the registry screen, in the "
                             "paper's Declarations. No registry brand has a recorded tie.",
    "held_out_brands": "No brand was held out. The registry was built mechanically from official data (BTS, FDIC) "
                       "and frozen before the first question.",
    "ai_use": "During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with "
              "study design, analysis and writing. The author reviewed and edited all content and takes full "
              "responsibility for it. Claude Fable 5.2 and GPT-6.2 Astra, with Gemini 4 Carbon breaking ties, "
              "checked the coding of a sample.",
    "independence": "Self-funded. No brand was contacted, sponsored the work or saw it before publication.",
}

CLOSING_STATEMENT = ("AI answers about airlines and banks broadly follow the market's order, firmly for banks, and "
                     "when asked, they say which brands are gone.")
