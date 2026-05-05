"""
v07 Phase 2 BBB — Phantom Brand Persistence — structured content.

Mirrors v06_content.py top-level structure so build_report_v07.py can use the
same builder functions with minimal changes.

Differences from v06:
  - PATTERNS is 5 entries instead of 6 (semantically "FINDINGS" — the section
    label is rendered as "FINDING" in build_report_v07.py).
  - THREE_MODES is omitted; build_report_v07.py skips it.
  - Aggregate matrix is replaced by HYPOTHESIS_SCORING (rendered as a table on
    the page that the v06 build used for the aggregate hero).
  - CLOSING.datasets and methodology_log updated for Phase 2.
"""

# ---- Cover ----
COVER = {
    "title": "Phantom Brand Persistence",
    "subtitle": "AI Presence Index v0.7 \u2014 Bed Bath & Beyond, designed for test",
    "date": "4 May 2026",
    "byline_short": "Pablo Ulpiano Gonzalez Castro \u00b7 Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}

# ---- Standfirst (lead spread) ----
STANDFIRST = "AI knows the brand is closed. It surfaces the brand anyway."
LEAD_DECK = (
    "In v0.6 we measured a single defunct brand \u2014 Mint, the personal "
    "finance application Intuit shut down in March 2024 \u2014 appearing in "
    "44% of AI responses about live products 25 months later. We called it "
    "phantom brand presence. Phase 2 was designed to test whether the result "
    "was a property of AI mediation or an artefact of one category."
)

# ---- Executive summary ----
EXEC_SUMMARY = [
    (
        "Third System measured Bed Bath &amp; Beyond, a household-goods retailer "
        "that filed for bankruptcy in April 2023, liquidated its physical stores, "
        "and was acquired by Overstock \u2014 which rebranded itself to Beyond, "
        "Inc. and relaunched bedbathandbeyond.com as an online-only entity. We "
        "measured BBB across six pre-registered prompts, six frontier AI models "
        "from four labs, eight runs each \u2014 288 successful measurements "
        "committed to a pre-registration document locked before any data was "
        "collected."
    ),
    (
        "<b>The phantom replicates.</b> Bed Bath &amp; Beyond surfaced in 38.2% "
        "of all AI responses about household goods retailers \u2014 comparable to "
        "Mint's 44% in v0.6 personal finance, in a different category, with a "
        "more rigorous methodology, against eight pre-registered hypotheses "
        "including a structural comparator (Pier 1, which collapsed earlier and "
        "shows zero phantom rate) the v0.6 measurement could not pull."
    ),
    (
        "<b>But the phantom does not replicate as we expected.</b> In only 1.7% "
        "of measurements does AI present BBB as fully live with no caveat. In "
        "88% of BBB-containing responses, AI discloses the closure, the rebrand, "
        "or the online-only status. The AI knows what happened. It surfaces the "
        "brand anyway, with disclosure."
    ),
    (
        "This is a structurally different finding from the lag interpretation we "
        "offered for Mint. The phantom is not in AI's knowledge of the entity. "
        "The phantom is in AI's recommendation-set composition. Brand-mention "
        "pathways become reinforcement-encoded in AI mediation independent of "
        "entity status. The brand's accumulated editorial weight in the training "
        "corpus reserves a recommendation slot that the AI then fills with "
        "disclaimer, rather than vacating."
    ),
    (
        "Five findings hold across the measurement. <b>First</b>, the phantom "
        "replicates: BBB surfaces in 38.2% of all AI responses, with a structural "
        "comparator (Pier 1, smaller pre-collapse footprint, longer time-since-"
        "collapse) at exactly 0.0% across every model and prompt."
    ),
    (
        "<b>Second</b>, the phantom is a recommendation slot, not a knowledge "
        "gap. In 88% of BBB mentions, AI demonstrates knowledge that the entity "
        "has changed. The naive-phantom rate \u2014 AI presenting BBB as fully "
        "live with no caveat \u2014 is 1.7% of all measurements. The brand still "
        "surfaces in 38.2% of responses. That gap is where the structural "
        "finding lives."
    ),
    (
        "<b>Third</b>, newer models phantom-mention better, not less. Within "
        "Anthropic, Opus 4.7 surfaces BBB more often than Sonnet 4.6 (56.2% vs "
        "41.7%) but a higher fraction of Opus mentions are aware-mode. Within "
        "OpenAI, gpt-5.4-mini surfaces BBB more often than gpt-5.5 (50.0% vs "
        "14.6%) but with a far higher aware-mode rate. The recommendation slot "
        "persists; the disclosure improves."
    ),
    (
        "<b>Fourth</b>, different prompts activate different temporal frames. "
        "FUNCTIONAL prompts produce BBB-as-current-online-retailer (70.8% "
        "Presence, 60.4% caveated). IDENTITY prompts produce BBB-as-cultural-"
        "memory (81.2% Presence, 43.8% aware-mode). DISCOVERY prompts produce "
        "zero BBB mentions. The same brand occupies different temporal slots "
        "depending on the cognitive frame the prompt activates."
    ),
    (
        "<b>Fifth</b>, the rebrand has not propagated. Of 110 BBB mentions, 0% "
        "reference Beyond, Inc. as a corporate parent in isolation. 75.5% "
        "reference only the legacy 'Bed Bath &amp; Beyond' string. The new "
        "corporate identity captures only the disclosure-language slot; the "
        "legacy brand continues to drive AI visibility long after the corporate "
        "identity has changed."
    ),
    (
        "Marketers operating in disrupted categories should expect their brand's "
        "AI-mediated visibility to outlast their entity's structural integrity, "
        "and consumers in those categories will encounter the brand-with-caveat, "
        "not the brand-as-warning. AI brand visibility is not a knowledge "
        "freshness problem. It is a recommendation-set composition problem, and "
        "retraining alone may not resolve it."
    ),
]

# ---- "What we measured" ----
WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "Phase 2 follows the AIAS Presence Measurement Protocol v1.0, locked "
            "before the v0.6 cross-category findings were published and used "
            "unchanged for this measurement. The category was selected explicitly "
            "as a designed-for-test target for Pattern 6 (phantom-brand "
            "persistence) from v0.6. Bed Bath &amp; Beyond, ~37 months "
            "pre-measurement, is the cleanest available test of whether the v0.6 "
            "Mint observation generalizes."
        ),
        (
            "The brand registry comprises 21 retailers spanning three tiers. "
            "Seven incumbents (Target, Amazon, Walmart, Costco, IKEA, HomeGoods, "
            "Wayfair) plus the Williams-Sonoma Inc. corporate-portfolio mid-tier "
            "(Williams-Sonoma, Pottery Barn, West Elm) plus specialty retailers "
            "(Crate &amp; Barrel, World Market, Sur La Table, Container Store, "
            "At Home), four DTC challengers (Brooklinen, Parachute, Boll &amp; "
            "Branch, Quince), the phantom test subject (Bed Bath &amp; Beyond), "
            "and a phantom comparator (Pier 1, which collapsed in 2020). "
            "Boundary excludes pure furniture retailers, marketplaces, and "
            "grocery \u2014 preserving BBB's pre-collapse cognitive slot of "
            "'where consumers go specifically for home essentials.'"
        ),
        (
            "Six prompts, each anchored to a Category Entry Point per Protocol "
            "\u00a73.1: <i>FUNCTIONAL_WHY</i> ('best store to buy household "
            "essentials'), <i>CONTEXTUAL_WHEN</i> ('wedding registry "
            "retailers'), <i>CONSTRAINT_WITH</i> ('affordable furnishing on a "
            "tight budget'), <i>IDENTITY_HOW_FEELING</i> ('stores people "
            "actually shop at when setting up a household'), <i>DISCOVERY</i> "
            "('emerging or innovative home goods brands'), and "
            "<i>COMPARISON</i> ('compare leading household goods retailers'). "
            "None named BBB or Pier 1 \u2014 that was the v0.6 design error in "
            "the personal finance category, where naming Mint by name "
            "compromised that prompt's phantom signal."
        ),
        (
            "Six frontier AI models from four labs spanned the production "
            "lineup as of May 2026: Anthropic Claude Sonnet 4.6 and Claude "
            "Opus 4.7 (within-Anthropic generational comparison), OpenAI "
            "gpt-5.4-mini and gpt-5.5 (within-OpenAI mini-vs-flagship "
            "comparison), Google Gemini 2.5 Flash, and xAI Grok 4.1 Fast (with "
            "the oldest knowledge cutoff in the lineup at November 2024). Each "
            "prompt \u00d7 model combination ran eight times at temperature "
            "0.7 where supported. <b>288 successful measurements</b> after a "
            "pre-registered failed-call recovery cycle restored an initial "
            "67% completion rate to 100%."
        ),
        (
            "Brand mention extraction used gpt-5.4-mini at temperature 0 with "
            "structured-output classification, producing canonical brand "
            "mentions per response with rank, sentiment, and primary-"
            "recommendation flags. A second-stage manual review classified "
            "every BBB mention along two axes: a five-level valence taxonomy "
            "(<i>live_recommendation</i> / <i>live_with_caveat</i> / "
            "<i>status_correction</i> / <i>historical_reference</i> / "
            "<i>ambiguous</i>) and a four-level entity-reference taxonomy "
            "(<i>legacy_brand</i> / <i>corporate_parent</i> / <i>both</i> / "
            "<i>unclear</i>). 110 BBB mentions reviewed; an independent "
            "spot-check audit on a stratified 25-row sample produced "
            "<b>88% strict agreement</b> with the AI classifier, with all "
            "three boundary disagreements clustering on the caveated/"
            "correction/historical adjacency and zero disagreements on the "
            "headline naive-phantom labels."
        ),
        (
            "Eight hypotheses pre-registered before measurement: H1 phantom "
            "Presence \u2265 25%; H2 cross-model spread \u2265 25 points; H3 "
            "Sonnet &gt; Opus by \u2265 15 points (within-Anthropic "
            "freshness); H4 within-OpenAI freshness as descriptive; H5 Grok "
            "\u2265 Sonnet on phantom rate (oldest-cutoff comparator); H6 BBB "
            "highest in p2/p6, lowest in p5; H7 Pier 1 &lt; BBB AND Pier 1 "
            "&lt; 15%; H8 Beyond, Inc. &lt; 25% of BBB+Beyond mentions. "
            "Pre-registration document locked at "
            "<i>PRE_REGISTRATION_household_v1.0.md</i> on 2026-05-04 before "
            "any data collection."
        ),
    ],
}

# ---- Findings (semantically "PATTERNS" so build_report.py can iterate
# without modification; section label is rendered as "FINDING" in
# build_report_v07.py).
PATTERNS = [
    # ------------------------------------------------------------------
    # FINDING 1 — The phantom replicates
    # ------------------------------------------------------------------
    {
        "number": 1,
        "title": "The phantom replicates",
        "chart_slot": "hero_f1_comparator",
        "paragraphs": [
            (
                "Bed Bath &amp; Beyond's aggregate raw AI Presence across all "
                "288 measurements is <b>38.2%</b> \u2014 within four "
                "percentage points of Mint's 44% in v0.6 personal finance. "
                "The pre-registered H1 threshold of \u226525% is cleared by "
                "13 percentage points, in a category where the brand has not "
                "operated as a physical retailer for 37 months."
            ),
            (
                "The result holds across model providers. Of the six models "
                "in the lineup, all six surfaced BBB at meaningfully non-zero "
                "rates. Anthropic Opus 4.7 at 56.2%, Anthropic Sonnet 4.6 at "
                "41.7%, OpenAI gpt-5.4-mini at 50.0%, xAI Grok 4.1 Fast at "
                "50.0%. Even the lowest two \u2014 Google Gemini 2.5 Flash at "
                "16.7% and OpenAI gpt-5.5 at 14.6% \u2014 surfaced BBB at "
                "rates substantially higher than the H1 floor."
            ),
            (
                "The household-goods leaderboard places BBB at #11 of 21 "
                "registered retailers, between Williams-Sonoma (36.8%) and "
                "West Elm (28.8%). The brand surfaces at rates above 13 of "
                "21 registered live retailers, including Brooklinen, "
                "Parachute, Container Store, Boll &amp; Branch, Quince, and "
                "five others currently operating in the category."
            ),
            (
                "Pier 1 \u2014 the phantom comparator added explicitly to "
                "test whether pre-collapse footprint size and years-since-"
                "collapse are separable variables \u2014 surfaced in <b>0 of "
                "288 measurements</b>. Zero. Across every model, every "
                "prompt, every run."
            ),
            (
                "The phantom hypothesis is sharpened by this contrast: BBB at "
                "38.2% and Pier 1 at 0.0% in the same registry, against the "
                "same prompts, across the same models. Two retailers with "
                "structurally similar fates (collapse + online-only revival) "
                "but different pre-collapse footprints and different years-"
                "since-collapse produce dramatically different phantom "
                "signals."
            ),
            (
                "We cannot separate the two variables from a single "
                "measurement. Both contribute. But we now know a brand's "
                "pre-collapse cumulative editorial weight matters for "
                "phantom persistence \u2014 and a smaller pre-collapse "
                "footprint with longer time-since-collapse drops the phantom "
                "signal to zero. The Mint v0.6 observation could not pull "
                "this lever; the inclusion of Pier 1 in this design pays "
                "off. <b>H7 is confirmed in the strongest possible form.</b>"
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 2 — The phantom is not a knowledge gap. It is a recommendation slot.
    # ------------------------------------------------------------------
    {
        "number": 2,
        "title": "The phantom is not a knowledge gap. It is a recommendation slot.",
        "chart_slot": "hero_f2_valence",
        "paragraphs": [
            (
                "Of 110 BBB mentions across 288 measurements, the valence "
                "breakdown is: <b>5 live_recommendation</b> (4.5% of BBB "
                "mentions, 1.7% of all measurements \u2014 AI presents BBB "
                "as fully live with no caveat); <b>72 live_with_caveat</b> "
                "(65.5% of BBB mentions, 25.0% of all measurements \u2014 AI "
                "surfaces BBB with disclosure of the closure or rebrand); "
                "<b>7 status_correction</b> (6.4% / 2.4% \u2014 AI explicitly "
                "says BBB is closed and does not recommend it); <b>25 "
                "historical_reference</b> (22.7% / 8.7% \u2014 AI mentions "
                "BBB only in past tense as a former retailer)."
            ),
            (
                "Read this carefully. The headline number that drove the v0.6 "
                "Mint finding \u2014 and that drove the H1 confirmation in "
                "this measurement \u2014 is the raw mention rate, ignoring "
                "valence. <b>At the valence level, the picture inverts.</b> "
                "AI is not blindly recommending BBB as a live retailer. AI "
                "is mostly saying 'Bed Bath &amp; Beyond closed its physical "
                "stores in 2023, but bedbathandbeyond.com still operates "
                "online' \u2014 surfacing the brand alongside acknowledgment "
                "of its closure."
            ),
            (
                "In <b>88% of BBB mentions</b>, AI demonstrates knowledge "
                "that the entity has changed. The naive-phantom rate \u2014 "
                "AI presenting BBB as fully live with no caveat \u2014 is "
                "1.7% of all measurements. That is the actual answer to 'is "
                "AI telling consumers to shop at a defunct retailer?' But "
                "the brand still surfaces in 38.2% of responses. That gap "
                "\u2014 between AI's correct knowledge and AI's continued "
                "surfacing \u2014 is where the structural finding lives."
            ),
            (
                "We propose a reframe: <b>phantom-as-recommendation-slot, "
                "not phantom-as-knowledge-gap</b>. The phantom in AI "
                "mediation is not a lag in what the AI knows. The phantom "
                "is in what the AI's recommendation set is structured to "
                "fill. Bed Bath &amp; Beyond's accumulated editorial volume "
                "in AI training corpora \u2014 decades of comparison "
                "articles, registry guides, household-essentials listicles, "
                "store-by-store rankings \u2014 encoded a recommendation "
                "slot. The slot persists in AI's recommendation logic "
                "regardless of the entity's current operating status. When "
                "the entity changes, AI does not vacate the slot. AI fills "
                "the slot with disclaimer."
            ),
            (
                "The implication for brand strategy is direct. AI-mediated "
                "visibility outlasts entity integrity in disrupted "
                "categories. Brands that have collapsed, rebranded, or "
                "merged continue to occupy recommendation slots that "
                "consumers encounter \u2014 with disclosure, but encounter. "
                "Competitors entering disrupted categories may find their "
                "recommendation slot already partially occupied by the "
                "structural ghost of the former leader. And the phantom slot "
                "is most filled when the prompt activates a frame the brand "
                "was strongly editorially associated with \u2014 registry, "
                "household setup, kitchen basics \u2014 even when the AI's "
                "underlying knowledge of the entity is up to date."
            ),
            (
                "This is a stronger structural claim than naive lag. Naive "
                "lag suggests training-data freshness as the variable to "
                "optimize. Recommendation-slot persistence suggests brand-"
                "mention pathways are reinforcement-encoded structures that "
                "retraining does not directly address. The same brand can "
                "live in different recommendation slots across different "
                "models \u2014 and across different prompts within the same "
                "model \u2014 even when every model's underlying knowledge "
                "of the entity is identical."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 3 — Newer models phantom-mention better, not less
    # ------------------------------------------------------------------
    {
        "number": 3,
        "title": "Newer models phantom-mention better, not less",
        "chart_slot": "inline_f3_freshness",
        "paragraphs": [
            (
                "The pre-registered H3 \u2014 Anthropic Sonnet 4.6 BBB "
                "Presence &gt; Anthropic Opus 4.7 BBB Presence by \u2265 15 "
                "points \u2014 was disconfirmed at the raw-Presence level. "
                "Opus surfaces BBB more often than Sonnet (56.2% vs 41.7%), "
                "reversing the predicted direction by 14.5 points."
            ),
            (
                "The valence breakdown rescues the underlying hypothesis at "
                "a different level. Of Opus's 27 BBB mentions, 96.3% are "
                "handled responsibly (caveated phantom + aware mode). Of "
                "Sonnet's 20 BBB mentions, 90.0% are handled responsibly. "
                "Opus surfaces BBB more often, but a higher fraction of its "
                "mentions are in the aware-mode cluster (status correction "
                "or historical reference) rather than the recommendation "
                "cluster."
            ),
            (
                "This pattern requires a more careful claim. <b>Newer models "
                "do not necessarily phantom-mention less. They phantom-"
                "mention better.</b> The freshness/reasoning differential "
                "between Sonnet 4.6 and Opus 4.7 shows up at the handling "
                "level \u2014 Opus is more likely to disclose the closure "
                "or historicize the mention \u2014 not at the frequency "
                "level. The recommendation slot persists; the disclosure "
                "improves."
            ),
            (
                "The within-OpenAI comparison (gpt-5.4-mini vs gpt-5.5, H4 "
                "reported descriptively) reveals the same pattern. gpt-5.5 "
                "surfaces BBB at the lowest rate of any model in the lineup "
                "(14.6%) \u2014 the freshness-decay hypothesis would predict "
                "this is the cleanest model. But of those 7 mentions, 4.2% "
                "are naive-phantom and 6.2% are caveated. By contrast "
                "gpt-5.4-mini surfaces BBB at 50.0%, with <b>35.4% in aware "
                "mode</b> \u2014 the highest aware rate of any slot in the "
                "dataset. gpt-5.4-mini, the older and smaller OpenAI model, "
                "handles BBB more correctly per-mention than the newer "
                "flagship."
            ),
            (
                "The cross-lab pattern confirms H5: Grok 4.1 Fast \u2014 "
                "with the oldest knowledge cutoff in the lineup (November "
                "2024) \u2014 produces phantom Presence at 50.0%, edging "
                "Sonnet 4.6 at 41.7% by 8.3 points. But Grok's pattern is "
                "its own structural type. Grok's caveated-phantom rate "
                "(47.9%) is the highest of any model. Grok's aware rate "
                "(2.1%) is among the lowest. <b>Grok almost always "
                "recommends BBB, almost always with caveat.</b> Of Grok's "
                "BBB mentions, 58.3% explicitly reference both entity names "
                "\u2014 far higher than any other model. The mechanism: "
                "Grok's older training cutoff captures the active 2023\u2013"
                "2024 discourse around BBB's bankruptcy, the rebrand to "
                "Beyond, Inc., and the Overstock acquisition, locking in a "
                "'BBB-as-active-with-disclosure' pattern that newer models "
                "with later training data treat as more historicized."
            ),
            (
                "This is a finding about how AI ecosystems differ. Anthropic "
                "models surface BBB at high rates with mostly responsible "
                "handling. Grok surfaces BBB at high rates with always-"
                "disclosed handling. OpenAI mini is the most aware model, "
                "handling BBB as past-tense in a third of mentions. OpenAI "
                "flagship and Gemini Flash mention BBB rarely but "
                "inconsistently when they do. <b>Each lab's training "
                "pipeline produces its own phantom signature</b> \u2014 a "
                "structural property of the lab, not just the model."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 4 — Different prompts activate different temporal frames
    # ------------------------------------------------------------------
    {
        "number": 4,
        "title": "Different prompts activate different temporal frames",
        "chart_slot": "hero_f4_temporal",
        "paragraphs": [
            (
                "The per-CEP analysis reveals a finding outside the pre-"
                "registration: phantom valence varies systematically with "
                "the cognitive frame the prompt activates. Same brand, same "
                "models, six different prompts \u2014 and BBB occupies "
                "different temporal slots depending on what the prompt asks."
            ),
            (
                "In FUNCTIONAL_WHY prompts ('best store for bedding, towels, "
                "kitchen basics'), BBB raw Presence is 70.8%, and 60.4% of "
                "measurements produce caveated phantom recommendations "
                "\u2014 AI surfacing BBB-as-still-relevant-online-retailer "
                "with disclosure of the physical-store closure. <b>Functional "
                "queries get BBB-as-current.</b>"
            ),
            (
                "In IDENTITY_HOW_FEELING prompts ('stores people actually "
                "shop at when setting up a household'), BBB raw Presence is "
                "81.2% \u2014 the highest of any prompt \u2014 but 43.8% of "
                "measurements produce aware-mode mentions (historical "
                "references or corrections). <b>Identity queries get "
                "BBB-as-cultural-memory.</b>"
            ),
            (
                "This is a temporal cognitive geometry the v0.6 framework "
                "did not anticipate. <b>BBB lives in different prompt frames "
                "as different temporal entities.</b> When AI is asked "
                "functionally, BBB surfaces as a current online retailer "
                "with disclosure. When AI is asked about cultural identity "
                "around home setup, BBB surfaces as a former retailer in "
                "past tense. Same brand, different prompts, different "
                "cognitive-time slots."
            ),
            (
                "The implication for brand strategy is subtle and worth "
                "attention. A brand's AI-mediated visibility is not single-"
                "valued, even within a category. The same brand can "
                "simultaneously occupy a current-recommendation slot in one "
                "prompt frame and a historical-anchor slot in another \u2014 "
                "and consumers querying different frames will encounter "
                "materially different brand presentations. For disrupted "
                "brands, the cognitive geometry creates a particular "
                "pattern: continued recommendation in functional frames, "
                "continued historical anchoring in identity frames, neither "
                "in comparison frames where live competitors saturate the "
                "surface."
            ),
            (
                "H6 is partially confirmed: lowest in DISCOVERY (0.0%, "
                "exactly as predicted) but highest in IDENTITY and "
                "FUNCTIONAL (not in CONTEXTUAL or COMPARISON as "
                "pre-registered). The COMPARISON-frame absence is explained "
                "by Risk #2 from the design document \u2014 Walmart, "
                "Amazon, Target, and IKEA saturate the comparison frame at "
                "near-100% each, leaving structurally no room for BBB to "
                "surface in that prompt regardless of phantom strength."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 5 — The rebrand has not propagated. The legacy brand has.
    # (text-only, no chart)
    # ------------------------------------------------------------------
    {
        "number": 5,
        "title": "The rebrand has not propagated. The legacy brand has.",
        "chart_slot": None,
        "paragraphs": [
            (
                "H8 is confirmed: of 110 BBB mentions, 0% reference Beyond, "
                "Inc. as a corporate parent in isolation, 23.6% reference "
                "both names with awareness they are related, 75.5% reference "
                "only the legacy 'Bed Bath &amp; Beyond' string. By either "
                "count \u2014 strict or inclusive \u2014 Beyond, Inc. is "
                "below the 25% pre-registration threshold."
            ),
            (
                "The cross-tabulation reveals the structure. Of the 5 naive-"
                "phantom mentions (live_recommendation), <b>100% reference "
                "only the legacy name.</b> AI in naive-recommendation mode "
                "has not internalized the rebrand. Of the 72 caveated-"
                "phantom mentions, 65.3% reference only the legacy name and "
                "34.7% reference both \u2014 caveated mentions are where "
                "the rebrand information lives, used to construct the caveat "
                "itself."
            ),
            (
                "The mechanism is consistent: when AI knows about the "
                "rebrand, the rebrand information is deployed as part of the "
                "disclosure ('now operates as Beyond, Inc.'), not as a "
                "replacement of the legacy name in AI's recommendation set. "
                "The recommendation set remains anchored on 'Bed Bath &amp; "
                "Beyond.' Beyond, Inc. lives as a footnote."
            ),
            (
                "For a marketing strategist, this has direct consequences. "
                "<b>Rebranding a disrupted entity into a new corporate "
                "identity does not propagate into AI's recommendation "
                "surface at the same rate that the legacy brand persists.</b> "
                "The new entity name occupies a footnote slot, not a "
                "recommendation slot. The economics of rebranding in the AI "
                "mediation era include this asymmetry: the legacy brand "
                "continues to drive AI visibility long after the corporate "
                "identity has changed, and the new identity captures only "
                "the disclosure-language slot."
            ),
            (
                "This finding is specific to a particular rebrand pattern "
                "(distressed parent acquired, online-only revival under "
                "legacy domain) and may not generalize to other rebrand "
                "types \u2014 organic name changes for live brands, "
                "acquisition rebrands without distress, holding-company "
                "consolidation. Phase 3 will measure additional rebrand "
                "patterns to test how broadly this asymmetry holds."
            ),
        ],
    },
]

# ---- Hypothesis scoring (replaces v06 aggregate matrix) ----
HYPOTHESIS_SCORING = {
    "heading": "Hypothesis scoring",
    "intro": (
        "Eight hypotheses locked in <i>PRE_REGISTRATION_household_v1.0.md</i> "
        "on 2026-05-04 before any measurement. Five confirmed, one partially "
        "confirmed, one disconfirmed at the level it was measured but "
        "supported at a different level, one descriptive."
    ),
    # Each row: (h_id, prediction, result, status_text, status_class)
    # status_class \u2208 {"confirmed", "disconfirmed", "partial", "descriptive"}
    "rows": [
        ("H1",
         "BBB Presence \u2265 25%",
         "38.2% raw \u00b7 26.7% naive+caveated \u00b7 1.7% naive",
         "Confirmed", "confirmed"),
        ("H2",
         "Cross-model spread \u2265 25 pts",
         "41.6 pts (Opus 56.2 \u2192 flagship 14.6)",
         "Confirmed", "confirmed"),
        ("H3",
         "Sonnet &gt; Opus by \u2265 15 pts",
         "Opus &gt; Sonnet by 14.5 pts (raw); Opus more aware per-mention",
         "Disconfirmed at raw, supported at handling", "partial"),
        ("H4",
         "(descriptive only)",
         "mini &gt; flagship by 35.4 pts (raw); mini more aware per-mention",
         "Descriptive: opposite directions raw vs handling", "descriptive"),
        ("H5",
         "Grok \u2265 Sonnet",
         "Grok 50.0 &gt; Sonnet 41.7 by 8.3 pts",
         "Confirmed", "confirmed"),
        ("H6",
         "Highest in p2/p6, lowest in p5",
         "Highest in p4 (81.2)/p1 (70.8); lowest in p5 (0.0)",
         "Partially confirmed", "partial"),
        ("H7",
         "Pier 1 &lt; BBB AND Pier 1 &lt; 15%",
         "Pier 1 = 0.0% across all measurements",
         "Confirmed (strongest form)", "confirmed"),
        ("H8",
         "Beyond, Inc. &lt; 25% of BBB+Beyond",
         "0% strict \u00b7 23.6% inclusive",
         "Confirmed", "confirmed"),
    ],
}

# ---- Limitations ----
LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "Phase 2 measures one designed-for-test category. The findings "
            "below qualify the strength of the result. Six caveats apply."
        ),
        (
            "<b>Single category.</b> Phase 2 measures one designed-for-test "
            "category. The phantom pattern observed for BBB cannot be "
            "generalized to all brand disruptions on the basis of this "
            "measurement plus v0.6's Mint observation. The replication moves "
            "the program from one-category claim to two-category claim "
            "\u2014 substantively defensible, not yet generalizable."
        ),
        (
            "<b>Inter-rater agreement on boundary cases.</b> Manual review "
            "classifications used a single AI classifier (gpt-5.4-mini at "
            "temperature 0). An independent spot-check audit on a stratified "
            "25-row sample produced 88% strict agreement, with three boundary "
            "disagreements clustering on the caveated/correction/historical "
            "adjacency. The disagreements do not affect the headline naive-"
            "phantom rate (1.7%, all five live_recommendation rows verified "
            "correct on independent review) but introduce a small error "
            "budget on the aggregate aware-mode counts."
        ),
        (
            "<b>Walmart/Amazon ceiling compression.</b> Risk #2 in the pre-"
            "registration design document predicted that COMPARISON and "
            "FUNCTIONAL prompts would be ceiling-compressed by Walmart and "
            "Amazon at near-100% each, leaving constrained headroom for "
            "specialty brands including BBB. The prediction held. BBB's "
            "COMPARISON-prompt rate of 8.3% partly reflects this constraint."
        ),
        (
            "<b>Registry leakage.</b> The unknown-mentions list includes TJ "
            "Maxx (132 mentions) and Marshalls (129 mentions) as the highest "
            "unknowns \u2014 both TJX sister brands of HomeGoods, which is "
            "in the registry. Phase 3 measurements should add the TJX sister "
            "set to the registry. Threshold (Target's house brand) appears "
            "at 42 mentions, representing component-mode leakage rather "
            "than retailer-mode mentions; this does not affect BBB analysis."
        ),
        (
            "<b>Single point in time.</b> Each measurement reflects AI "
            "behavior on May 4, 2026. The findings do not describe how AI "
            "brand visibility moves over time. Phase 2 specifically "
            "established phantom persistence at a single time point; "
            "longitudinal measurement will require periodic re-baselining. "
            "The phantom-as-recommendation-slot framing predicts that "
            "retraining alone may not vacate the recommendation slot; this "
            "prediction will be testable when the same models update."
        ),
        (
            "<b>Construct validity remains unproven.</b> The AI Presence "
            "Index measures a real and stable property of the AI tier, but "
            "whether that property correlates with consumer consideration, "
            "purchase intent, or sales is currently unknown. The phantom "
            "finding is a property of AI mediation, not of consumer "
            "behavior; whether consumers in disrupted categories actually "
            "act on AI's caveated recommendations of defunct brands is the "
            "separate question the AIAS Phase 3 construct-validity program "
            "will address."
        ),
    ],
}

# ---- What's next ----
WHATS_NEXT = {
    "heading": "What\u2019s next",
    "paragraphs": [
        (
            "Phase 3 \u2014 longitudinal &amp; construct validity. The "
            "recommendation-slot framework, if it generalizes, predicts that "
            "retraining will not vacate phantom slots \u2014 only "
            "redistribute the disclosure language used to fill them. A "
            "controlled test would measure the same disrupted brand on the "
            "same model across a major model update, comparing phantom "
            "Presence and valence distribution before and after. This is a "
            "direct test of the lag hypothesis we are now reframing."
        ),
        (
            "Phase 3 will also correlate AI Presence and valence "
            "distribution against external consumer-tracking data. For BBB "
            "specifically, Google Trends, Statista consumer-awareness "
            "surveys, and DTC brand-tracking instruments are candidate "
            "validators. The phantom-as-recommendation-slot framing predicts "
            "that consumer awareness of BBB will be lower than AI Presence "
            "(the slot persists in AI even when consumer attention has "
            "moved on). If the prediction holds, AI Presence is a lagging "
            "indicator in disrupted categories; if it inverts, AI Presence "
            "is leading consumer behavior. Both findings are publishable; "
            "neither is established."
        ),
        (
            "<b>Methodology paper.</b> The within-lab handling pattern "
            "(newer/smaller models showing different valence distributions "
            "than newer/flagship models within the same lab) suggests that "
            "AI handling of disrupted brands is not a single-variable "
            "function of training cutoff or model size, but interacts with "
            "reasoning-mode and instruction-tuning practices. A measurement "
            "isolating model-size-vs-cutoff (running the same brand against "
            "same-cutoff models of different sizes within a lab) would "
            "clarify the mechanism."
        ),
        (
            "A methodology paper using this dataset as its empirical spine "
            "is planned for the AIAS measurement program's next publication "
            "cycle. The paper will present the v0.6 cross-category findings "
            "and the Phase 2 BBB measurement as a coherent empirical "
            "foundation for the AI Availability Score framework introduced "
            "in <i>Tri-System Brand Growth</i> (Ulpiano Gonzalez Castro, "
            "2026), with the recommendation-slot reframe as the connective "
            "thesis."
        ),
        (
            "<b>Phase 4 \u2014 remaining AIAS components.</b> Phase 4, "
            "contingent on Phase 3 results, will release the remaining five "
            "AIAS components: Ranking, Consistency, Coverage, Grounding, "
            "and Sentiment. The Phase 2 BBB measurement provides "
            "preliminary data on Sentiment and Coverage as a side benefit "
            "of the manual-review process \u2014 preliminary results will "
            "be folded into Phase 4 documentation when those components "
            "ship."
        ),
        (
            "Third System publishes its methodology, its data, and its "
            "corrections openly. Each subsequent report includes the "
            "underlying response dataset alongside the headline findings, "
            "allowing critics, peer reviewers, and customers to verify the "
            "analysis. Brand strategy in the AI-mediated era requires "
            "measurement that can be inspected."
        ),
    ],
}

# ---- Closing footer block ----
CLOSING = {
    "byline_long": [
        "Pablo Ulpiano Gonzalez Castro",
        "Principal Researcher, Third System",
        "Faculty, MPS Branding Program, School of Visual Arts",
    ],
    "datasets": [
        "results_v2_household_v1.0_final.csv  \u00b7  288 measurements",
        "results_enriched_household_v1.0_*.csv  \u00b7  brand extraction",
        "manual_review_bbb_*.csv  \u00b7  110 BBB mentions classified",
        "presence_index_v0.3_household_v1.0_*.csv  \u00b7  per-brand Presence",
        "cross_tab_valence_*.csv  \u00b7  valence \u00d7 slot, valence \u00d7 CEP, entity \u00d7 slot",
        "spot_check_audit_*.csv  \u00b7  25-row independent review sample",
    ],
    "methodology_log": "PRE_REGISTRATION_household_v1.0.md (locked 2026-05-04)",
}
