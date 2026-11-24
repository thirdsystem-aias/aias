"""v0.44 flagship report (TS-FL-v0.44-r1): content, managerial register (P1-P5 propositions, no hypothesis labels).

Every number is a {{v:KEY}} placeholder filled by build_report_v44_r1.py from papers/v0_44/v44_values.json (the
paper's values file) and reports/v44_report_values.json (v44_report_values.py: design counts, thresholds and tier
shares computed by code from the verdict file, the unit table and the locked scorer's constants). None is typed.
Claims follow the paper (papers/v0_44/v0_44_paper_draft.md at 0af9cb9) and the DEVIATIONS log (osf/v44/DEVIATIONS.md).
Commercial outputs omit the author's employer by name (brand file, commercial_outputs_disclosure); the paper's
Declarations name it, and the small-print COI below carries every item of record from those Declarations and
DEVIATIONS Entry 0 in employer-neutral words. Findings 04 and 05 are pre-registered descriptives and carry no verdict.
Revised after the row 32 review gate of 2026-11-24 (reviews/v0.44-report/2026-11-24.md).
"""

TITLE = "Known, but not named"
DECK = ("How the newest AI models name brands in {{v:rv.industries.n}} US service and retail industries, "
        "from market leaders to smaller brands")

STANDFIRST = ("We asked {{v:rv.models.n}} of the newest AI models about {{v:reg.units_total}} brands in "
              "{{v:rv.industries.n}} US industries the programme had not measured, from car insurance to fashion. "
              "They name market leaders far more often than smaller brands, and pass over many brands they know.")

GLANCE_NUMBERS = [
    {"value": "{{v:H_Tier.rho}}", "unit": "",
     "label": "Rank correlation of market tier with how often AI names a brand",
     "source": "within industries, {{v:H_Tier.n}} brands; pre-set bar {{v:rv.threshold.tier_conf}}"},
    {"value": "{{v:D2.gap.S}}", "unit": "",
     "label": "Smaller brands every model recognised but no answer named",
     "source": "of {{v:rv.tier.n.S}} smaller brands; {{v:D2.gap.L}} of {{v:rv.tier.n.L}} leaders"},
    {"value": "{{v:H_Sep.rho}}", "unit": "",
     "label": "Rank correlation of Consistency with how often a brand is named",
     "source": "{{v:H_Sep.n}} rated brands; pre-set limit ±{{v:rv.threshold.sep_max}}"},
]

MEASURED = ("{{v:rv.models.names}}, the newest flagship of {{v:rv.models.n}} providers, answered "
            "{{v:MC_Complete.answered}} questions on {{v:rv.collection_date}} with web search off: "
            "{{v:rv.calls.B}} open questions ({{v:rv.questions_per_industry}} per industry, asked {{v:rv.runs.n}} "
            "times by each model) and {{v:rv.calls.A}} questions on whether they recognise a brand. Plan and "
            "deviations record: osf.io/ec6wh (v44).")

SUMMARY = [
    "In every industry the models named some brands far more than others, and mostly the brands that lead their "
    "industry on premiums, sales, locations or store counts. Many smaller brands were known to every model but "
    "never named. Among the {{v:H_Sep.n}} brands named often enough to be rated, how consistently the models named "
    "a brand did not follow how often they named it. All {{v:rv.tests.n}} pre-set tests were confirmed, and the "
    "models largely agreed with each other.",
]

INTRO_LEAD = ("Which insurer, hotel, grocer or pharmacy does an AI model name when asked? This study measured it in "
              "{{v:rv.industries.n}} industries the programme had not covered.")

INTRO = [
    "AIAS™, the AI Availability Score, measures how AI answers represent brands. Its two components are Presence, "
    "how often AI answers name a brand, and Consistency, how evenly different models agree in naming it. Both were "
    "established on premium consumer goods (headphones, skincare, cosmetics, cars and spirits) and on older models. "
    "This study asked whether they behave the same way where people buy a service, choose a store or visit a "
    "chain: car insurance, hotel chains, grocery store chains, fast-food chains, clothing and department stores, "
    "pharmacies, convenience stores and gas stations, and fashion and luxury.",
    "Each industry's brands came from a dated public ranking (in some industries two) and were placed by one "
    "fixed rule: leaders (ranks {{v:rv.rank.L.min}} to {{v:rv.rank.L.max}}), challengers ({{v:rv.rank.C.min}} to "
    "{{v:rv.rank.C.max}}) and smaller brands. Esurance, A&amp;P and Rite Aid, which have left the US market, were "
    "added as departed brands. Every test and threshold was fixed and published before the first question, and "
    "every result is reported here.",
    "All {{v:MC_Complete.answered}} of {{v:MC_Complete.expected}} planned questions were answered, "
    "{{v:raw.rerun_ok}} of them in the planned re-run of failed calls, for {{v:MC_Budget.spend_usd}} against a "
    "{{v:rv.budget.cap}} cap, and every pre-set quality check passed. The collection script's own safeguards "
    "stopped its first launch, whose keep-awake wrapper it read as a second collection, and the first start of the "
    "re-run, which found no API keys; nothing had been sent, and both were restarted, the one under another "
    "keep-awake wrapper, the other in a login shell (DEVIATIONS Entry 3). The study is independent: no brand is its "
    "focus, no finding is addressed to a brand, and no brand was contacted (Disclosures, at the end).",
]

MEASURED_HEAD = "What we measured"
MEASURED_PARAS = [
    "The models were {{v:rv.models.names}}, the newest generally available flagship of each of {{v:rv.models.n}} "
    "providers, with web search off. Each answered {{v:rv.questions_per_industry}} open questions per industry "
    "{{v:rv.runs.n}} times, such as \"What are the best car insurance companies in the US?\", and, for each brand, "
    "whether it recognised the brand as one of its industry. No question names a brand.",
    "A brand's naming rate (its Presence) is the share of answer cells, one per model, run and open question, "
    "that name it, from 0 (never) to 1 (every cell). Consistency, scored 0 to 100, is how evenly the "
    "{{v:rv.models.n}} models name a brand across the runs; it is rated only for brands named in at least "
    "{{v:rv.threshold.rated_floor}} cells and in enough runs ({{v:H_Sep.n}} of {{v:reg.units_total}}). A rank correlation compares two "
    "orders (1 = the same order, 0 = unrelated, below 0 = reversed); here it is computed within each industry and "
    "pooled. A 95% interval is the range the true value most likely lies in. Coding was automatic: a brand counts "
    "as named when one of its registered names appears in the answer. No person or second model checked it.",
]

FINDINGS = [
    {"verdict": "{{v:H_Spread.verdict}}",
     "title": "In every industry, some brands are named far more",
     "chart": "report_fig_01_spread.pdf",
     "caption": "Dot: standard deviation of the brands' naming rates in each industry (0 = every brand named "
                "equally often); bar: its 95% interval; dashed line: the bar set in advance. Departed brands are "
                "left out.",
     "body": [
         "The test asked whether naming varies across an industry's brands clearly more than run-to-run noise, in "
         "at least {{v:rv.threshold.spread_confirm}} of the {{v:H_Spread.n_industries}} industries. It did in all "
         "{{v:H_Spread.n_with_spread}}: the standard deviation ran from {{v:H_Spread.sd_min}} to "
         "{{v:H_Spread.sd_max}}, against a pre-set bar of {{v:rv.threshold.spread_sd}}, and even the lowest "
         "interval bound, {{v:H_Spread.ci_low_min}} ({{v:H_Spread.ci_low_min_ind}}), clears it.",
         "Every industry had brands that no answer named, from {{v:H_Spread.APR.share0}} of clothing and "
         "department stores to {{v:H_Spread.HOT.share0}} of hotel chains. The same models' answers about the "
         "programme's earlier consumer-goods categories (AIAS v0.42) also cleared the bar in {{v:omni.n_spread}} "
         "of {{v:omni.n_sub}}, a comparison made after scoring, with no verdict (paper, section 3.3).",
     ]},
    {"verdict": "{{v:H_Tier.verdict}}",
     "title": "Market leaders are named most, smaller brands least",
     "chart": "report_fig_02_tier_means.pdf",
     "caption": "Average naming rate of each tier, per industry. Leaders: ranks {{v:rv.rank.L.min}} to "
                "{{v:rv.rank.L.max}} of the industry's public ranking; challengers: {{v:rv.rank.C.min}} to "
                "{{v:rv.rank.C.max}}; smaller brands: below. Right: each industry's rank correlation (descriptive).",
     "body": [
         "Within industries, how often the models named a brand followed its place in the public ranking: a rank "
         "correlation of {{v:H_Tier.rho}} (95% interval {{v:H_Tier.ci}}; {{v:H_Tier.n}} brands), above the pre-set "
         "bar of {{v:rv.threshold.tier_conf}}; p {{v:H_Tier.p}} is the chance of a value this high if tier did not "
         "matter. The pre-set variants, reported without a verdict, gave similar values: {{v:H_Tier.elig.rho}} on "
         "exact ranks, {{v:H_Tier.nofas.rho}} without fashion and luxury (one of its sources uses AI discovery "
         "signals) and {{v:H_Tier.nopha.rho}} without Health Mart and Good Neighbor Pharmacy, ranked by another measure.",
         "The order holds in most industries, not all: among {{v:rv.tier.S_gt_C}}, the sampled smaller ones averaged "
         "{{v:H_Tier.mean.QSR.S}} against {{v:H_Tier.mean.QSR.C}} for challengers. The answers also named brands "
         "the rankings left out, such as Trader Joe's ({{v:rv.d6.GRO.TraderJoes}} mentions, counted from bold names "
         "and list items) and Costco ({{v:rv.d6.GRO.Costco}}) in grocery; the study does not score them.",
     ]},
    {"verdict": "{{v:H_Sep.verdict}}",
     "title": "Consistency is a separate signal from naming",
     "chart": "report_fig_03_consistency_scatter.pdf",
     "caption": "Each dot is a rated brand: its Consistency (0 to 100, how evenly the {{v:rv.models.n}} models "
                "name it) against its naming rate (0 to 1).",
     "body": [
         "Among the {{v:H_Sep.n}} brands that could be rated, how consistently the {{v:rv.models.n}} models named a "
         "brand did not follow how often they named it: a rank correlation of {{v:H_Sep.rho}} (95% interval "
         "{{v:H_Sep.ci}}), inside the pre-set limits (the correlation within ±{{v:rv.threshold.sep_max}}, its "
         "interval within ±{{v:rv.threshold.sep_ci}}). Presence and Consistency carry different information here, "
         "as they did in the programme's consumer-goods studies (summarised in its AIAS 2.0 synthesis).",
         "The base is narrow. Rating needs a brand to be named often enough, so it left "
         "{{v:H_Sep.unrated.tier.S}} smaller brands unrated, against {{v:H_Sep.unrated.tier.L}} leaders. Rated "
         "brands scored from {{v:unit.cphi_min}} to {{v:unit.cphi_max}}, mostly high, so the test compares brands "
         "the models already name with fairly even agreement. It says nothing about rarely named brands.",
     ]},
    {"verdict": "DESCRIPTIVE",
     "title": "Many smaller brands are known but never named",
     "chart": "report_fig_04_known_not_named.pdf",
     "caption": "Recognised: all {{v:rv.models.n}} models said yes when asked whether the brand belongs to its "
                "industry. Naming rate zero: no open answer named it. A pre-set description, with no test.",
     "body": [
         "Asked directly, the models recognised almost every brand: {{v:D2.claude-fable-5-2.all}} (Claude Fable "
         "5.2), {{v:D2.gpt-6-astra.all}} (GPT-6 Astra) and {{v:D2.gemini-4-argon.all}} (Gemini 4 Argon). Asked "
         "open questions, they passed many over: {{v:D2.gap.total}} brands were recognised by all "
         "{{v:rv.models.n}} yet never named in an open answer: {{v:D2.gap.S}} smaller brands, {{v:D2.gap.C}} "
         "challengers, {{v:D2.gap.L}} leader and {{v:D2.gap.G}} departed brand.",
         "This gap between being known and being named is what Presence was built to capture, and here it falls "
         "mostly on smaller brands. Each departed brand was recognised by all {{v:rv.models.n}} models; in open "
         "answers Esurance was never named, while A&amp;P (naming rate {{v:D3.AandP.pi}}) and Rite Aid "
         "({{v:D3.RiteAid.pi}}) were. Whether those answers presented them as current was not coded.",
     ]},
    {"verdict": "DESCRIPTIVE",
     "title": "The models largely agree and repeat themselves",
     "chart": "report_fig_05_agreement.pdf",
     "caption": "Rank correlation of how often each of the {{v:reg.units_total}} brands is named: between two "
                "models (circles) and between one model's runs (diamonds, mean over pairs of runs). "
                "A pre-set description, with no test.",
     "body": [
         "The models largely agreed on which brands to name, with pairwise rank correlations of "
         "{{v:rv.agree.min}} to {{v:rv.agree.max}} over all {{v:reg.units_total}} brands, and each repeated itself "
         "closely from run to run ({{v:rv.rel1.min}} to {{v:rv.rel1.max}}). Their industry averages were close: "
         "the largest gap between two models in one industry was {{v:D1.max_model_gap}} in naming rate "
         "({{v:D1.max_model_gap_ind}}).",
         "This agreement is within one night: every run was collected on {{v:rv.collection_date}}, within "
         "{{v:MC_Window.span_hours}} hours. Whether the industries' orders hold over months needs a retest. With "
         "web search off, the results describe the models' own knowledge, not what a search-enabled assistant "
         "would retrieve.",
     ]},
]

SCORED_HEAD = "The {{v:rv.tests.n}} pre-set tests, scored"
SCORED_INTRO = ("Each test, its bar and the rule for its outcome were published before the first question. "
                "Outcomes use the pre-set words and were computed once by the locked scoring script. No test, bar "
                "or rule changed after the lock. The DEVIATIONS log records the waived review period before the "
                "lock (Entry 1), a known limit in how refusals are recorded (Entry 2) and the refused starts "
                "of the collection (Entry 3).")
SCORED_ROWS = [
    ["01", "AI naming varies across brands in at least {{v:rv.threshold.spread_confirm}} of "
           "{{v:H_Spread.n_industries}} industries",
     "{{v:H_Spread.verdict}} ({{v:H_Spread.n_with_spread}} of {{v:H_Spread.n_industries}}; standard deviation "
     "{{v:H_Spread.sd_min}} to {{v:H_Spread.sd_max}}, bar {{v:rv.threshold.spread_sd}})"],
    ["02", "Leaders are named more than challengers, and challengers more than smaller brands",
     "{{v:H_Tier.verdict}} (rank correlation {{v:H_Tier.rho}}, 95% interval {{v:H_Tier.ci}}, p {{v:H_Tier.p}}, "
     "{{v:H_Tier.n}} brands; bar {{v:rv.threshold.tier_conf}})"],
    ["03", "How consistently a brand is named does not follow how often it is named",
     "{{v:H_Sep.verdict}} (rank correlation {{v:H_Sep.rho}}, 95% interval {{v:H_Sep.ci}}, {{v:H_Sep.n}} rated "
     "brands; rule: correlation within ±{{v:rv.threshold.sep_max}} and interval within "
     "±{{v:rv.threshold.sep_ci}})"],
    ["", "Pre-set quality checks: every question answered, the right model served, no answer cut off, inside the "
         "time window, scoring code reproduced, within budget",
     "All passed ({{v:MC_Complete.answered}} of {{v:MC_Complete.expected}} answered; {{v:MC_Budget.spend_usd}} "
     "spent)"],
]

LIMITS_HEAD = "Limitations"
LIMITS = [
    "One market and language (US English), one collection on one night, {{v:rv.models.n}} models with "
    "{{v:rv.runs.n}} runs each, no web search and no retest. Answers change between model versions.",
    "Tiers come from different public measures (premiums, sales, locations, store counts, brand rankings), some "
    "read from reproductions of the original tables; within an industry they order size or salience, not one "
    "common quantity. Fashion and luxury rests on global sources, one of which uses AI discovery signals; the "
    "tier result holds without it.",
    "Some company totals cover several store brands while the measured brand is one, and hotel groups are "
    "measured by group names that guests may know by their sub-brands, which lowers their measured naming. "
    "Kroger, Publix and Albertsons appear in both grocery and pharmacies, measured separately and not independent.",
    "With {{v:rv.models.n}} models, Consistency is noisier than on the larger panel of earlier waves (AIAS "
    "v0.41), and rating leaves out most smaller brands (finding 03).",
    "Coding is automatic and its name matcher is new: it was tested before the lock on made-up answers, not "
    "checked on these. Its {{v:alias.matches}} matches of names that are also common words (such as Progressive "
    "or Gap) were exported, not reviewed; no person or second model checked the coding.",
    "The consumer-goods comparison was computed after scoring from AIAS v0.42's table and carries no verdict. "
    "Rank correlations are computed within industry, so they differ slightly in form from those of AIAS v0.41 and "
    "v0.42. Refusals may be undercounted, as some kinds leave no trace in the record (DEVIATIONS Entry 2). The "
    "collection's launch differed from the planned command only in its keep-awake wrapper, and the re-run's "
    "restart only in the shell it was launched from (DEVIATIONS Entry 3).",
]
NEXT_HEAD = "What's next"
NEXT = [
    "A retest on the same brands and questions, to see whether the industries' orders hold; a registry that adds "
    "the brands the models name outside the rankings; and a search-on arm.",
    "Plan, registries, scripts and DEVIATIONS log: osf.io/ec6wh (v44). Answers, coding and values files: "
    "github.com/thirdsystem-aias/aias, branch v0.44, planned for OSF with the data deposit.",
]

DISCLOSURES = {
    "conflicts_of_interest": "The author is employed by a consumer-electronics company. Before collection the "
                             "registries were screened for ownership by, and relationships with, the company's "
                             "group: no registry brand was found to be group-owned (the screen checked the owners "
                             "named by the registry sources; no ownership filing was opened per brand). A group "
                             "affiliate supplies a medicine through subsidiaries of the companies behind CVS "
                             "Pharmacy and Express Scripts, a non-competitive relationship disclosed without "
                             "restriction; Walmart and Costco, behind two pharmacy units, also sell the company's "
                             "products. Group affiliates are active outside the US in insurance, hotels and "
                             "fashion; whether their stores sell any registry brand, and whether a group "
                             "advertising affiliate serves any, was not screened. Industries in which the company "
                             "competes or that are its device and network customers were not selected, nor were "
                             "drug makers. The company had no role in this work; it and its affiliates are named in "
                             "the paper's Declarations.",
    "held_out_brands": "No registry brand was held out on conflict grounds. Brands outside an industry's definition "
                       "were excluded by the pre-set rule and are listed with the registries, frozen before the "
                       "first question.",
    "ai_use": "During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with "
              "study design, analysis and writing. The author reviewed and edited all content and takes full "
              "responsibility for it.",
    "independence": "Self-funded. No brand was contacted, sponsored the work or saw it before publication. Coding "
                    "was automatic; no person or second model checked it.",
}

CLOSING_STATEMENT = ("In {{v:rv.industries.n}} service and retail industries, the newest AI models name market "
                     "leaders most, and pass over many smaller brands they know.")
