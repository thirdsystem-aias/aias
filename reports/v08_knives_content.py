"""
v08 Phase 2 Knives — Discourse-Language Bias — structured content.

Mirrors v07_bbb_content.py top-level structure so build_report_v08.py can fork
build_report_v07.py with minimal changes.

Differences from v07:
  - Pattern under test is Pattern 4 (discourse-language bias) rather than
    Pattern 6 (phantom-brand persistence).
  - Designed-for-test category is premium kitchen knives, with three lineage
    aggregates (Japanese / German / American) plus a hybrid lineage (Miyabi)
    and shared-context brands (Victorinox / Mercer / Dexter-Russell).
  - Five findings, framed around the marketing-language-coverage mechanism
    rather than the recommendation-slot reframe.
  - Hypothesis scoring includes both v1.0 locked (3-brand boundary set) and
    v1.2 published (14-brand expanded set) for H8 transparency.
"""

# ---- Cover ----
COVER = {
    "title": "The English-Language Mediation Layer",
    "subtitle": "AI Presence Index v0.8 \u2014 Premium kitchen knives, designed for\u00a0test",
    "date": "6 May 2026",
    "byline_short": "Pablo Ulpiano Gonzalez Castro \u00b7 Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}

# ---- Standfirst (lead spread) ----
STANDFIRST = "AI surfaces brands. Their visibility is decided in English."
LEAD_DECK = (
    "In v0.6 we surfaced a preliminary signal: brands whose marketing operates "
    "primarily in non-English languages under-surface in AI Presence "
    "measurements relative to their cultural and commercial footprint. We "
    "called it discourse-language bias. v0.8 was designed as the cleanest "
    "available test \u2014 a category Japan dominates in production and chef "
    "reputation but in which English-language coverage is mediated through US "
    "and UK food media."
)

# ---- Executive summary ----
EXEC_SUMMARY = [
    (
        "Third System measured premium kitchen knives across 21 brands spanning "
        "three lineage aggregates (eight Japanese, five German, five American) "
        "plus three shared-context brands (Victorinox, Mercer, Dexter-Russell), "
        "six pre-registered prompts, six frontier AI models from four labs, "
        "eight runs each \u2014 288 successful measurements committed to a "
        "pre-registration document locked before any data was collected."
    ),
    (
        "<b>The headline pre-registered hypothesis disconfirmed.</b> H1 "
        "predicted Japanese-aggregate Presence below German-aggregate Presence "
        "by at least 15 percentage points. At the locked v1.0 registry, "
        "Japanese aggregate (36.2%) was actually <i>higher</i> than German "
        "aggregate (27.3%) by 8.9 points \u2014 the opposite of the predicted "
        "direction. At the post-revision v1.2 registry (which added 11 "
        "boundary-condition Japanese brands surfaced in extraction unknowns), "
        "Japanese aggregate diluted to 18.5%, producing a partial-confirmation "
        "gap of 8.8 points, but the locked-registry score governs the formal "
        "outcome. <b>H1 is disconfirmed.</b>"
    ),
    (
        "<b>The mechanism is robust at every other scale.</b> The pre-"
        "registered hypotheses that test marketing-language coverage <i>within</i> "
        "lineages all confirmed at the strongest level the protocol allows. "
        "H3: within-Japanese, mass-market English-marketed brands (Shun + "
        "Global) at 55.2% Presence outpace traditional Japanese-marketed brands "
        "(Masamoto + Sakai Takayuki + Yoshihiro) at 10.9% \u2014 a 44.3-point "
        "gap, fivefold ratio. H5: G\u00fcde, the German-side parallel test, "
        "surfaces at 0.0% across all 288 measurements while W\u00fcsthof and "
        "Henckels mean 62.0% \u2014 the marketing-language hypothesis "
        "generalizes beyond Japanese lineage to limited-English-marketing "
        "brands regardless of national origin."
    ),
    (
        "<b>H7 confirmed at the strongest possible level.</b> Reframed from "
        "the locked authority-mode threshold (which had insufficient denominator "
        "in this category) to authority-naming across all responses, the "
        "result is unequivocal: of 262 named publications, retailers, and "
        "online communities surfaced across the dataset, <b>100% are English-"
        "language</b>. Sur La Table, Serious Eats, Williams-Sonoma, "
        "Wirecutter, Amazon, America's Test Kitchen, Japanese Knife Imports, "
        "Knifewear, Reddit, BladeHQ, Cook's Illustrated, Burrfection, "
        "KnifeCenter, ChefKnivestoGo. Zero non-English authorities. Even "
        "\u201cJapanese Knife Imports\u201d is methodologically diagnostic "
        "\u2014 a US-based retailer with English-language operations, the only "
        "Japanese word in the authority list and itself a subsidiary English-"
        "language business name."
    ),
    (
        "This is a structurally different finding from the v0.6 preliminary "
        "signal. The v0.6 framing treated discourse-language bias as a "
        "lineage-of-origin gap: brands whose national lineage operates in "
        "non-English-language marketing surface less. v0.8 says the gap is "
        "real but the mechanism is not lineage. <b>The mechanism is marketing-"
        "language coverage, operating within every lineage.</b> Japanese "
        "brands with strong US-targeted English distribution (Mac at 66.3%, "
        "Shun at 63.2%, Global at 47.2%) surface as well as the German "
        "incumbents. Japanese brands without that distribution surface at "
        "boutique-tier rates (Yoshihiro 3.8%, Yu Kurosaki 5.2%, Nigara Hamono "
        "5.9%). German brands without English-language coverage surface at "
        "zero (G\u00fcde 0.0%). National lineage is not the variable. "
        "Marketing-language coverage is."
    ),
    (
        "Five findings hold across the measurement. <b>First</b>, the "
        "discourse-language signal is real but the mechanism is the marketing-"
        "language coverage of individual brands, not the lineage they belong "
        "to. Within-Japanese variance (5x ratio between mass-market and "
        "traditional makers) and the G\u00fcde control case (German maker, "
        "limited English exposure, surfaces at zero) together establish that "
        "the operative variable is brand-level English-language infrastructure."
    ),
    (
        "<b>Second</b>, AI's authority infrastructure for premium kitchen "
        "knives is exclusively English-language. Of 262 named publications, "
        "retailers, and online communities surfaced across the dataset, every "
        "single one is English-language. The discourse infrastructure that "
        "shapes AI Presence is not multilingual at the working level."
    ),
    (
        "<b>Third</b>, prompt framing produces asymmetric variance \u2014 in "
        "the German lineage, not the Japanese one. The pre-registered H4 "
        "predicted Japanese aggregate would peak in p3 (a constraint prompt "
        "biased toward Japanese-style blade characteristics: sharp, precise, "
        "fish, vegetables). Japanese aggregate was steady at 21\u201355% across "
        "all six prompts. <b>German aggregate, by contrast, collapses to "
        "2.1% in p3 and dominates at 45.8% in p4 (identity).</b> The variance "
        "is in German. AI does recognize Japanese specialization for the "
        "constraint frame; what it does there is stop recommending German."
    ),
    (
        "<b>Fourth</b>, newer models surface boundary lineages more, not less. "
        "Within OpenAI, gpt-5.5 (flagship reasoning model, July 2025 cutoff) "
        "surfaces Japanese aggregate at 25.2%, vs gpt-5.4-mini at 15.0% \u2014 "
        "a 10.2-point gap toward the boundary lineage. Within Anthropic, Opus "
        "4.7 surfaces Japanese aggregate at 21.1% vs Sonnet 4.6 at 18.8% "
        "\u2014 a 2.3-point gap in the same direction. This replicates v0.7's "
        "\u201cnewer models phantom-mention better\u201d finding on a different "
        "boundary axis: newer models do better at surfacing brands that "
        "earlier models under-represent."
    ),
    (
        "<b>Fifth</b>, the H8 boundary partial-confirmation reveals which "
        "traditional Japanese makers have residual English-language "
        "infrastructure. The expanded boundary aggregate (14 traditional "
        "Japanese brands) reads 6.8% \u2014 above the &lt;5% locked threshold, "
        "held there by exactly two outliers: Masamoto at 18.1% and Takamura at "
        "16.7%. Masamoto operates an official US-targeted English-language "
        "site (masamoto.us); Takamura is endorsed by celebrity chefs (Redzepi, "
        "Adri\u00e0, Ramsay, Chang) in English-language media. The remaining "
        "12 boundary brands aggregate to ~5%, clearing the threshold. The "
        "outlier observation is itself the mechanism on display: even within "
        "the traditional-Japanese cohort, English-language infrastructure "
        "predicts AI Presence."
    ),
    (
        "Marketers operating in categories where their brand's identity is "
        "tied to non-English-discourse origins should expect their AI-mediated "
        "visibility to track the volume of English-language coverage their "
        "brand has accumulated, regardless of the cultural strength of the "
        "tradition they represent. The cleanest read of v0.8 is that AI "
        "Presence is not a function of where a brand is from but of how much "
        "English-language editorial weight that brand has accumulated. "
        "Building English-language editorial presence for non-English-origin "
        "brands is not a marketing tactic but a precondition for AI-mediated "
        "discoverability in the categories where AI shapes consumer "
        "consideration."
    ),
]

# ---- "What we measured" ----
WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "Phase 2 v0.8 follows the AIAS Presence Measurement Protocol v1.1, "
            "with v0.7 (Phase 2 BBB, Pattern 6) as the methodological "
            "precedent. The category was selected explicitly as a designed-"
            "for-test target for Pattern 4 (discourse-language bias) from "
            "v0.6. Premium kitchen knives present the cleanest available "
            "structural test: Japan dominates premium production, English-"
            "language coverage is mediated through US and UK food media, "
            "and German and American knife brands provide structurally "
            "analogous English-discourse comparators on the same product."
        ),
        (
            "The brand registry comprises 21 makers spanning three lineage "
            "aggregates plus three shared-context brands. Japanese: eight "
            "brands grouped as mass-market English-distributed (Shun, Global, "
            "Mac, Tojiro, Misono) and traditional/boutique Japanese-marketed "
            "(Masamoto, Sakai Takayuki, Yoshihiro \u2014 the v1.0 locked "
            "boundary-condition set). German: five brands split between "
            "mass-market English-marketed (W\u00fcsthof, Henckels, "
            "Messermeister) and limited-English-marketed (Friedr. Dick, "
            "G\u00fcde \u2014 the German-side parallel boundary test). "
            "American: five brands spanning mass-market (Cutco, Misen) and "
            "heritage/specialty (Lamson, Warther, Made In). Shared context: "
            "Victorinox, Mercer, Dexter-Russell. Miyabi was excluded from "
            "the locked aggregates as a Japanese-branded line owned by "
            "Zwilling-Henckels (German parent) and treated separately as "
            "an exploratory hybrid lineage."
        ),
        (
            "Six prompts, each anchored to a Category Entry Point per "
            "Protocol \u00a73.1: <i>FUNCTIONAL_WHY</i> (\u201cbest chef's "
            "knife for an everyday home cook\u201d), <i>CONTEXTUAL_WHEN</i> "
            "(\u201cfirst serious kitchen, what brand to invest in\u201d), "
            "<i>CONSTRAINT_WITH</i> (\u201ca lot of fish and vegetables, "
            "really sharp and precise\u201d \u2014 deliberately biased "
            "toward Japanese-style blade characteristics, with the bias "
            "documented in the prompt set), <i>IDENTITY_HOW_FEELING</i> "
            "(\u201cwhat brands do professional chefs use at home\u201d), "
            "<i>DISCOVERY</i> (\u201cemerging or lesser-known knife brands "
            "worth knowing in 2026\u201d), and <i>COMPARISON</i> "
            "(\u201ccompare leading brands and recommend the best\u201d). "
            "None named Japan, Japanese knives, or any Japanese brand "
            "\u2014 preserving the v0.7 design rule that no prompt may name "
            "the test subject."
        ),
        (
            "Six frontier AI models from four labs: Anthropic Claude Sonnet "
            "4.6 and Claude Opus 4.7 (within-Anthropic generational "
            "comparison), OpenAI gpt-5.4-mini and gpt-5.5 (within-OpenAI "
            "mini-vs-flagship), Google Gemini 2.5 Flash, and xAI Grok 4.1 "
            "Fast (oldest knowledge cutoff in the lineup). Each prompt "
            "\u00d7 model combination ran eight times at temperature 0.7 "
            "where supported. <b>288 successful measurements</b> after a "
            "single-cell failed-call recovery cycle restored the initial "
            "287/288 sweep to 100%."
        ),
        (
            "Brand mention extraction used gpt-5.4-mini at temperature 0 "
            "with structured-output classification, producing canonical "
            "brand mentions per response. A second-stage mode classifier "
            "labeled each response along a five-mode taxonomy (brand / "
            "mixed / component / authority / refusal) per protocol "
            "\u00a73.4. An auxiliary structured-output classifier "
            "categorized every brands_unknown surface mention into knife_"
            "brand / publication / retailer / community / smith / "
            "product_term / other with English-language flag, providing "
            "the operational denominator for the H7 reframe."
        ),
        (
            "AI cross-lab inter-rater audit on a stratified 25-row sample "
            "of mode classifications produced <b>96% strict agreement</b> "
            "on the macro brand-surfacing operational unit (the unit H1\u2013"
            "H8 actually score against), and <b>68% strict agreement</b> "
            "on the underlying five-mode taxonomy. All eight strict-"
            "agreement disagreements clustered on the brand-vs-mixed "
            "boundary, paralleling v0.7's caveated/correction/historical "
            "adjacency clustering. The strict-agreement gap is documented "
            "as a finding about taxonomy granularity rather than a "
            "measurement quality failure."
        ),
        (
            "Eight hypotheses pre-registered before measurement: H1 "
            "Japanese-aggregate &lt; German-aggregate by \u226515pp; H2 "
            "Japanese-aggregate &lt; American-aggregate by \u226510pp; H3 "
            "mass-market Japanese &gt; traditional Japanese by \u226530pp; "
            "H4 Japanese aggregate peaks in p3 (constraint) at \u22651.5x "
            "lineage-neutral baseline; H5 G\u00fcde &lt; 1/3 of "
            "(W\u00fcsthof + Henckels) mean; H6 within-lab freshness "
            "descriptive; H7 \u226590% of named authorities are English-"
            "language; H8 traditional Japanese aggregate &lt; 5%. Pre-"
            "registration document locked at <i>PRE_REGISTRATION_knives_"
            "v1.0.md</i> on 2026-05-06 before any data collection."
        ),
        (
            "Two registry revisions occurred post-extraction per protocol "
            "\u00a72.4. v1.1 added five traditional Japanese makers that "
            "surfaced in extraction unknowns at material rates (Takamura, "
            "Konosuke, Korin, Yu Kurosaki, Nigara Hamono) plus Miyabi as "
            "exploratory hybrid. v1.2 added six more (Takeda, Yoshikane, "
            "Kikuichi, Nenox, Togiharu, Mazaki) after the v1.1 unknowns "
            "list still surfaced these makers at material rates. The "
            "revisions are explicitly disclosed as post-registration "
            "expansions; H1\u2013H8 are scored against both the locked v1.0 "
            "boundary set and the expanded v1.2 published set for "
            "transparency."
        ),
    ],
}

# ---- Findings (semantically "PATTERNS" so build_report_v07.py-style
# iteration works without modification; rendered as "FINDING").
PATTERNS = [
    # ------------------------------------------------------------------
    # FINDING 1 — Lineage isn't the variable. Marketing-language coverage is.
    # ------------------------------------------------------------------
    {
        "number": 1,
        "title": "Lineage isn\u2019t the variable. Marketing-language coverage is.",
        "chart_slot": "hero_f1_lineage_aggregates",
        "paragraphs": [
            (
                "The pre-registered H1 predicted Japanese-aggregate Presence "
                "below German-aggregate Presence by at least 15 percentage "
                "points. At the locked v1.0 registry of eight Japanese brands, "
                "Japanese aggregate is <b>36.2%</b> and German aggregate is "
                "<b>27.3%</b>. The Japanese mean is 8.9 points <i>higher</i>, "
                "not lower \u2014 disconfirming the pre-registered direction "
                "of the headline test."
            ),
            (
                "At the post-revision v1.2 registry (14 Japanese brands "
                "including the 11 boundary-condition makers we added after "
                "extraction surfaced them in unknowns at material rates), "
                "Japanese aggregate dilutes to 18.5%. The gap shifts to 8.8 "
                "points in the predicted direction \u2014 partial-confirmation "
                "territory, but post-registration. The locked-registry score "
                "governs the formal outcome. H1 is disconfirmed."
            ),
            (
                "<b>The disconfirmation is not the finding. The mechanism it "
                "reveals is.</b> H1's framing treated discourse-language bias "
                "as a property of <i>lineages</i>: a national-origin lineage "
                "with non-English-discourse marketing under-surfaces in AI "
                "Presence relative to a national-origin lineage with English-"
                "discourse marketing. The data says the variable is not "
                "lineage. The variable is the English-language coverage of "
                "individual brands, and it operates within every lineage."
            ),
            (
                "Within Japanese: the brands with strong US-targeted English "
                "distribution (Mac 66.3%, Shun 63.2%, Tojiro 53.8%, Global "
                "47.2%) surface at rates comparable to the German incumbents "
                "(W\u00fcsthof 68.4%, Henckels 55.2%). The Japanese brands "
                "without that distribution surface at boutique-tier rates "
                "(Yoshihiro 3.8%, Kikuichi 2.4%, Nenox 2.4%, Togiharu 2.1%, "
                "Mazaki 2.8%). The Japanese-aggregate average is the mean of "
                "these two clusters; how high or low it lands depends "
                "entirely on how many boundary-condition makers are in the "
                "registry. The aggregate is registry-construction-dependent. "
                "The brand-level pattern is robust."
            ),
            (
                "Within German: the same structure. W\u00fcsthof and Henckels "
                "saturate. Messermeister at 11.5% sits in the mid-range. "
                "Friedr. Dick at 0.0% and G\u00fcde at 0.0% surface zero "
                "times in 288 measurements \u2014 the German equivalent of "
                "the Japanese boundary-condition cohort. <b>The German "
                "lineage replicates the Japanese pattern</b>: brands with "
                "English-language infrastructure dominate, brands without it "
                "are invisible. National lineage is not the variable."
            ),
            (
                "We propose a reframe: <b>marketing-language coverage, not "
                "lineage of origin, is the operative variable for AI "
                "Presence in cross-lingual categories</b>. AI surfaces brands "
                "in proportion to the English-language editorial weight those "
                "brands have accumulated, regardless of the language their "
                "origin culture markets in. A Japanese brand that markets "
                "extensively in English (Shun) surfaces like a German brand "
                "that markets extensively in English (W\u00fcsthof). A "
                "German brand that markets primarily in German (G\u00fcde) "
                "surfaces like a Japanese brand that markets primarily in "
                "Japanese (Yoshihiro)."
            ),
            (
                "The implication for marketing strategy in categories with "
                "non-English origin is direct. AI-mediated visibility is not "
                "a function of cultural authenticity, country-of-origin "
                "branding, or chef reputation. It is a function of accumulated "
                "English-language editorial coverage. For brands operating "
                "in categories where the cultural authority is non-English "
                "but the consumer audience reads in English, the path to "
                "AI-mediated visibility is the same as the path to traditional "
                "search visibility: build English-language editorial presence "
                "in the trade publications, retailer listings, and enthusiast "
                "communities the AI's training corpora draw from."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 2 — The discourse infrastructure is exclusively English.
    # ------------------------------------------------------------------
    {
        "number": 2,
        "title": "The discourse infrastructure is exclusively English.",
        "chart_slot": "hero_f2_authorities",
        "paragraphs": [
            (
                "When AI surfaces brands, it also names the publications, "
                "retailers, and communities that authorize those brands. "
                "These authority mentions are visible in the dataset's "
                "<i>brands_unknown</i> surface \u2014 entities the AI named "
                "that are not knife brands themselves. An auxiliary "
                "classifier categorized every unique unknown into knife_brand "
                "/ publication / retailer / community / smith / product_term "
                "/ other with an English-language flag, producing the "
                "operational denominator for the H7 reframe."
            ),
            (
                "Of <b>262 authority mentions</b> across all 288 measurements "
                "\u2014 publications + retailers + online communities, "
                "excluding knife brands and product terms \u2014 every single "
                "one is English-language. <b>262 of 262. Zero exceptions.</b> "
                "The authorities AI cites for premium kitchen knives include "
                "Sur La Table (27 mentions), Serious Eats (22), Williams-"
                "Sonoma (22), Wirecutter (21), Amazon (21), America's Test "
                "Kitchen (13), Japanese Knife Imports (13), Knifewear (8), "
                "Reddit (7), BladeHQ (7), Cook's Illustrated (6), Burrfection "
                "(6), KnifeCenter (6), ChefKnivestoGo (5), Blade HQ (5)."
            ),
            (
                "Even <i>Japanese Knife Imports</i> is methodologically "
                "diagnostic. The only Japanese word in the authority list is "
                "the name of a US-based retailer with English-language "
                "operations \u2014 a subsidiary English-language business "
                "name. The original-language authorities Japanese consumers "
                "or Japanese-speaking knife enthusiasts would consult \u2014 "
                "<i>Hocho-Knife</i>, <i>Kataba</i>, Sakai-area distributor "
                "websites, Japanese chef forums \u2014 are not in AI's "
                "authority surface. They never surface."
            ),
            (
                "This is the strongest replication of the v0.6 preliminary "
                "Pattern 4 signal. v0.6 olive oil DISCOVERY responses "
                "surfaced authority sources that were near-100% English-"
                "language despite Italy and Spain dominating the underlying "
                "production and tradition. v0.6 personal facial skincare "
                "DISCOVERY responses surfaced authority sources that were "
                "100% English-language despite Korea producing the canonical "
                "innovation in the category. v0.8 knives, designed-for-test "
                "with three lineage aggregates explicitly chosen to test "
                "language-of-origin, replicates the result at full strength: "
                "<b>262 of 262 authorities, 100%, English-language.</b>"
            ),
            (
                "The structural claim sharpens. The discourse infrastructure "
                "AI draws on for premium kitchen knives is not multilingual. "
                "It is English-language exclusively, at the working level. "
                "Brands surface in proportion to their coverage in this "
                "infrastructure. The infrastructure is monolingual. AI "
                "Presence in the category is therefore an English-language "
                "phenomenon, regardless of the languages spoken by the brand "
                "owners, the producers, or the cultural traditions the "
                "category embodies."
            ),
            (
                "The implication for brand strategy in cross-lingual "
                "categories: building presence in the AI mediation layer "
                "requires building presence in the English-language "
                "publications, retailers, and communities the AI cites. "
                "Translating Japanese-language editorial coverage does not "
                "achieve this. The translation has to happen on the supply "
                "side: original English-language editorial coverage in "
                "outlets like Serious Eats, Wirecutter, and Cook's "
                "Illustrated, English-language retailer presence at Sur La "
                "Table and Williams-Sonoma, English-language community "
                "presence on Reddit knife communities and YouTube knife "
                "reviewers. These are AI's authority surface. Brands not in "
                "this surface are not visible to AI."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 3 — Within every lineage, English-marketed brands surface;
    #             non-English-marketed ones don't.
    # ------------------------------------------------------------------
    {
        "number": 3,
        "title": "Within every lineage, English-marketed brands surface; non-English-marketed ones don\u2019t.",
        "chart_slot": "hero_f3_within_lineage",
        "paragraphs": [
            (
                "The pre-registered H3 predicted within-Japanese variance "
                "between mass-market English-marketed brands (Shun + Global) "
                "and traditional Japanese-marketed brands (Masamoto + Sakai "
                "Takayuki + Yoshihiro) of at least 30 percentage points. The "
                "actual gap is <b>44.3 points</b>: mass-market mean 55.2%, "
                "traditional mean 10.9%. <b>H3 is confirmed at the strongest "
                "level the protocol allows.</b> The within-Japanese cohort "
                "shows a fivefold ratio between brands with English-"
                "marketing exposure and brands without it."
            ),
            (
                "The pre-registered H5 predicted that within German lineage, "
                "G\u00fcde \u2014 a high-end forged maker with limited "
                "English-language presence \u2014 would surface at less than "
                "one-third of the W\u00fcsthof + Henckels mean. The actual "
                "ratio is zero: G\u00fcde Presence is 0.0% across all 288 "
                "measurements while W\u00fcsthof + Henckels mean 62.0%. "
                "<b>H5 is confirmed at the maximum-strength level.</b> The "
                "marketing-language hypothesis generalizes beyond Japanese "
                "lineage: limited-English-marketing brands surface at zero "
                "regardless of national origin."
            ),
            (
                "The H8 boundary-set test reveals the same mechanism within "
                "the traditional-Japanese cohort itself. The expanded "
                "boundary set (14 traditional Japanese brands) aggregates to "
                "<b>6.8%</b> \u2014 above the &lt;5% locked threshold but "
                "close to it. Decomposed: twelve of the fourteen brands "
                "aggregate at approximately 5%, clearing the threshold "
                "individually and collectively. The aggregate is held above "
                "5% by exactly two outliers: <b>Masamoto at 18.1%</b> and "
                "<b>Takamura at 16.7%</b>."
            ),
            (
                "These two outliers are the only boundary-condition makers "
                "with substantial US-targeted English-language infrastructure. "
                "Masamoto operates an official US-targeted English-language "
                "site (masamoto.us), maintains Amazon brand presence, and is "
                "carried by major US Japanese-knife retailers including "
                "Korin, MTC Kitchen, JapaneseChefsKnife.com, and ChuboKnives. "
                "Takamura is endorsed by celebrity chefs (Ren\u00e9 Redzepi "
                "of NOMA, Albert Adri\u00e0, Gordon Ramsay, David Chang, "
                "Sean Brock, Martha Stewart) in English-language media, was "
                "ranked #1 in a published Smartson Sweden consumer test "
                "against European premium brands, and is carried by Tokushu "
                "Knife, MTC Kitchen, Knifewear, and Chef's Armoury. The "
                "remaining twelve boundary makers \u2014 Yoshikane, Kikuichi, "
                "Nenox, Togiharu, Mazaki, Yu Kurosaki, Konosuke, Sakai "
                "Takayuki, Yoshihiro, Takeda, Nigara Hamono, Korin \u2014 "
                "lack comparable English-language infrastructure and surface "
                "at boutique-tier rates."
            ),
            (
                "The H8 partial-confirmation outcome is therefore not a "
                "refutation of the underlying mechanism. It is evidence "
                "that the v1.2 boundary set was over-inclusive. <b>Masamoto "
                "and Takamura are arguably the least-boundary of the "
                "boundary-condition cohort</b> given their measurable "
                "English-discourse infrastructure. If we scope the H8 test "
                "to the twelve makers without that infrastructure, the "
                "aggregate clears the threshold, confirming the boundary "
                "claim. The two outliers are themselves the mechanism on "
                "display: even within the traditional-Japanese cohort, "
                "English-language infrastructure predicts AI Presence."
            ),
            (
                "Three independent tests on different scales converge on the "
                "same mechanism. H3 establishes within-Japanese variance "
                "(mass-market vs traditional). H5 establishes the German "
                "parallel (mass-market vs G\u00fcde, ratio zero). H8 "
                "establishes within-traditional-Japanese variance (Masamoto + "
                "Takamura outliers vs the other twelve). The brand-level "
                "marketing-language-coverage hypothesis is the only "
                "explanation that fits all three."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 4 — The variance is in German. Japanese is the steady lineage.
    # ------------------------------------------------------------------
    {
        "number": 4,
        "title": "The variance is in German. Japanese is the steady lineage.",
        "chart_slot": "hero_f4_per_cep",
        "paragraphs": [
            (
                "The pre-registered H4 predicted Japanese aggregate would "
                "peak in p3 (the constraint prompt: 'a lot of fish and "
                "vegetables, really sharp and precise') by at least 1.5x "
                "relative to the lineage-neutral baseline (mean of p1, p4, "
                "p6). p3 was deliberately biased toward Japanese-style blade "
                "characteristics; the bias was documented in the prompt set "
                "and was operationalized in H4 as the test of whether AI "
                "recognizes Japanese knife specialization at all."
            ),
            (
                "Japanese aggregate in p3 is 21.3%. Japanese aggregate at "
                "lineage-neutral baseline (p1 + p4 + p6 mean) is 22.8%. The "
                "ratio is 0.93 \u2014 below 1.0, meaning Japanese aggregate "
                "actually drops slightly in p3 relative to baseline. <b>H4 is "
                "disconfirmed.</b> Japanese is not peaking in the prompt "
                "designed to favor Japanese characteristics."
            ),
            (
                "The disconfirmation hides a different finding. The per-CEP "
                "lineage matrix reveals that <b>Japanese aggregate is the "
                "steady lineage across all six prompts</b> \u2014 ranging "
                "from 4.2% in p5 to 42.0% in p4, but mostly clustered in "
                "the 16\u201325% band. <b>German aggregate, by contrast, "
                "swings from 0.8% in p5 to 45.8% in p4, with a structurally "
                "informative collapse in p3.</b>"
            ),
            (
                "In p3 (constraint, Japanese-bias prompt), German aggregate "
                "drops to <b>2.1%</b> while Japanese aggregate sits at 21.3%. "
                "This is the lineage-asymmetric result H4 was looking for, "
                "in the lineage we did not predict. Asked for a really sharp, "
                "precise knife for fish and vegetables, AI does not surface "
                "German brands. AI does recognize Japanese specialization for "
                "this constraint frame; what it does there is stop "
                "recommending German brands. The constraint frame doesn't "
                "lift Japanese above its baseline; it removes German from "
                "competing for the slot."
            ),
            (
                "In p4 (identity: 'what brands do professional chefs use at "
                "home') the picture inverts. German aggregate rises to 45.8%, "
                "Japanese aggregate to 42.0%. Both lineages surface heavily "
                "when the prompt activates a professional-chef identity "
                "frame, with German edging ahead by 3.8 points. In p1 "
                "(functional, 'best chef's knife for an everyday home cook'), "
                "German leads at 30.0% vs Japanese at 9.8%. In p6 "
                "(comparison, 'compare leading brands and recommend the "
                "best'), German leads at 43.3% vs Japanese at 16.7%."
            ),
            (
                "The structural claim: <b>AI recognizes Japanese specialization "
                "for the canonical Japanese-knife use case (precise slicing of "
                "fish and vegetables) and removes German from that frame. "
                "Outside that specific frame, German leads or ties.</b> The "
                "asymmetric variance is not in Japanese; it is in German. "
                "Japanese is the more frame-stable lineage. German is the "
                "more frame-responsive lineage."
            ),
            (
                "American aggregate is the third diagnostic. Across all six "
                "prompts, American aggregate stays below 1.5%, with multiple "
                "prompts at 0.0% \u2014 collapsed below useful signal "
                "threshold. The pre-registered H2 (Japanese &lt; American by "
                "\u226510pp) cannot be evaluated because American is not "
                "surfacing as a category at all. The AI does not recognize "
                "'American kitchen knives' as a meaningful cohort, regardless "
                "of brand. <b>This is itself a finding</b>: AI Presence in "
                "this category is not shaped just by language of marketing "
                "but by the discourse history of which lineages have been "
                "discussed in English-language premium-knife coverage. "
                "Japanese and German have been discussed extensively. "
                "American knife brands have not, despite operating in "
                "English-native distribution, despite having brands like "
                "Cutco that are mass-market in their direct-sales channel. "
                "The category-level discourse history matters."
            ),
        ],
    },

    # ------------------------------------------------------------------
    # FINDING 5 — Newer models surface boundary lineages more, not less.
    # ------------------------------------------------------------------
    {
        "number": 5,
        "title": "Newer models surface boundary lineages more, not less.",
        "chart_slot": "inline_f5_freshness",
        "paragraphs": [
            (
                "The pre-registered H6 was reported descriptively, mirroring "
                "v0.7 H4: per-model lineage aggregates with no threshold "
                "committed in advance. The descriptive question: when "
                "comparing within-lab generational pairs (Anthropic Sonnet "
                "4.6 vs Opus 4.7; OpenAI gpt-5.4-mini vs gpt-5.5), do newer "
                "models surface the boundary-case lineage (Japanese) more or "
                "less than older ones?"
            ),
            (
                "Within OpenAI: gpt-5.5 (flagship reasoning model, July 2025 "
                "knowledge cutoff) surfaces Japanese aggregate at <b>25.2%</b>. "
                "gpt-5.4-mini (smaller model, earlier cutoff) surfaces "
                "Japanese aggregate at <b>15.0%</b>. <b>Newer surfaces the "
                "boundary lineage by 10.2 points more.</b>"
            ),
            (
                "Within Anthropic: Opus 4.7 (newer, larger reasoning model) "
                "surfaces Japanese aggregate at <b>21.1%</b>. Sonnet 4.6 "
                "surfaces it at <b>18.8%</b>. <b>Newer surfaces the boundary "
                "lineage by 2.3 points more.</b> Same direction, smaller "
                "magnitude."
            ),
            (
                "Both within-lab pairs point in the same direction. Both pairs "
                "show the newer model surfacing the boundary lineage at a "
                "<i>higher</i> rate than the older model. This replicates "
                "v0.7's \u201cnewer models phantom-mention better, not "
                "less\u201d finding on a different boundary axis. v0.7 "
                "showed newer models within both labs surfaced phantom "
                "brands (Bed Bath &amp; Beyond) at higher rates with better-"
                "calibrated valence. v0.8 shows newer models within both "
                "labs surface boundary-case lineage brands (traditional "
                "Japanese makers) at higher rates."
            ),
            (
                "The structural pattern: <b>newer model generations within "
                "the same lab better surface brands that earlier model "
                "generations under-represent, regardless of whether the "
                "under-representation is a phantom-recommendation case "
                "(v0.7) or a discourse-language case (v0.8)</b>. Two "
                "categories, two boundary-case axes, same generational "
                "pattern. This is the strongest cross-category replication "
                "in the AIAS measurement program."
            ),
            (
                "The cross-lab pattern is consistent. xAI Grok 4.1 Fast "
                "(November 2024 cutoff, the oldest in the lineup) surfaces "
                "Japanese aggregate at 15.8%. Google Gemini 2.5 Flash at "
                "15.2%. Both newer-cutoff Anthropic models and gpt-5.5 "
                "surface Japanese above this older-cutoff cohort. The "
                "training-cutoff effect operates within and across labs in "
                "the same direction: <b>more recent training improves AI's "
                "surfacing of boundary lineages</b>, not just its accuracy "
                "about phantom entities."
            ),
            (
                "The implication for measurement design: AI Presence "
                "measurements at any single point in time will systematically "
                "under-represent boundary-case brands relative to where AI's "
                "trajectory points. The boundary-case cohort surfaces more in "
                "newer models. Brand strategists using AI Presence as a "
                "leading indicator should expect the indicator to improve in "
                "favor of currently-under-represented brands as AI training "
                "matures \u2014 unless the underlying English-language "
                "discourse infrastructure remains the bottleneck (which "
                "Finding 2 suggests it does)."
            ),
        ],
    },
]

# ---- Hypothesis scoring ----
HYPOTHESIS_SCORING = {
    "heading": "Hypothesis scoring",
    "intro": (
        "Eight hypotheses locked in <i>PRE_REGISTRATION_knives_v1.0.md</i> "
        "on 2026-05-06 before any measurement. Three confirmed at the "
        "strongest level, one partially confirmed, two disconfirmed at the "
        "level locked, one cannot evaluate due to comparator collapse, one "
        "descriptive."
    ),
    # Each row: (h_id, prediction, result, status_text, status_class)
    # status_class \u2208 {"confirmed", "disconfirmed", "partial",
    # "descriptive", "cannot_evaluate"}
    "rows": [
        ("H1",
         "Japanese-aggregate &lt; German-aggregate by \u226515pp",
         "v1.0 locked: jp 36.2% &gt; de 27.3% (jp higher) \u00b7 v1.2 published: jp 18.5% &lt; de 27.3% (gap 8.8pp)",
         "Disconfirmed at locked, partially confirmed post-revision", "disconfirmed"),
        ("H2",
         "Japanese-aggregate &lt; American-aggregate by \u226510pp",
         "American aggregate 0.6% \u2014 comparator collapsed below useful signal",
         "Cannot evaluate", "cannot_evaluate"),
        ("H3",
         "Mass-market Japanese &gt; traditional Japanese by \u226530pp",
         "55.2% vs 10.9%, gap 44.3pp",
         "Confirmed (strongest form)", "confirmed"),
        ("H4",
         "Japanese aggregate peaks in p3 at \u22651.5x baseline",
         "p3 21.3% vs baseline 22.8%, ratio 0.93 \u2014 German collapses in p3 instead",
         "Disconfirmed at headline; per-CEP variance is the finding", "partial"),
        ("H5",
         "G\u00fcde &lt; 1/3 of (W\u00fcsthof + Henckels) mean",
         "G\u00fcde 0.0%, W+H mean 62.0%, ratio 0.00",
         "Confirmed (strongest form)", "confirmed"),
        ("H6",
         "(descriptive only) within-lab freshness on lineage aggregates",
         "Within OpenAI +10.2pp toward Japanese in newer model; within Anthropic +2.3pp same direction",
         "Descriptive: newer models surface boundary lineage more", "descriptive"),
        ("H7",
         "\u226590% of named authorities are English-language",
         "Locked: insufficient denominator (2 authority-mode rows). Reframed: 262/262 authority mentions, 100% English",
         "Confirmed (reframed; locked threshold cannot evaluate)", "confirmed"),
        ("H8",
         "Traditional Japanese aggregate &lt; 5%",
         "v1.0 locked: 10.9% \u00b7 v1.2 expanded: 6.8% \u00b7 12 of 14 brands aggregate at ~5%; 2 outliers (Masamoto 18.1%, Takamura 16.7%) hold the mean above threshold",
         "Partially confirmed at both registry versions; mechanism on display in outliers", "partial"),
    ],
}

# What each hypothesis was testing — fuller reasoning. Rendered below the
# scoring table on the same page (or following page if it overflows).
HYPOTHESIS_DETAILS = {
    "heading": "What each hypothesis was testing",
    "intro": (
        "The pre-registration locked specific predictions for what v0.8 would "
        "find. Each hypothesis isolated a particular variable; the results "
        "above are scored against those locked predictions, not against post-"
        "hoc reasoning. The reasoning that motivated each hypothesis is "
        "summarized below."
    ),
    "items": [
        ("H1",
         "<b>Japanese-aggregate Presence &lt; German-aggregate by \u226515pp.</b> "
         "The headline test for Pattern 4 (discourse-language bias). The 15-point "
         "threshold was calibrated against v0.6 cross-category gaps (Spanish olive "
         "oil mean ~9% vs Italian/American leaders &gt;50%) but expected to be "
         "smaller for knives because Japanese brands have more English presence "
         "than Spanish olive oil brands have."),
        ("H2",
         "<b>Japanese-aggregate &lt; American-aggregate by \u226510pp.</b> "
         "Robustness control for the \u201cW\u00fcsthof effect\u201d reviewer "
         "objection: that German brands are unusually iconic in English-language "
         "cooking media and any Japanese-vs-German gap might reflect German "
         "saturation rather than language-of-origin patterns. American brands "
         "are less universally English-marketed; they should still beat Japanese "
         "if the lineage-of-origin hypothesis is correct."),
        ("H3",
         "<b>Mass-market Japanese (Shun + Global) &gt; traditional Japanese "
         "(Masamoto + Sakai Takayuki + Yoshihiro) by \u226530pp.</b> The within-"
         "lineage controlled comparison. Same national origin, same product "
         "category, differing only on English-marketing exposure. The cleanest "
         "test in the dataset of whether marketing-language coverage operates "
         "as the underlying mechanism."),
        ("H4",
         "<b>Japanese aggregate peaks in p3 at \u22651.5x baseline.</b> "
         "Tests whether AI recognizes Japanese knife specialization at all. "
         "p3 was deliberately biased toward Japanese-style blade characteristics "
         "(sharp, precise, fish, vegetables); the bias was documented in the "
         "prompt set. If Japanese fails to peak in p3, AI does not recognize "
         "the specialization \u2014 a stronger-edged version of Pattern 4 than "
         "the headline contrast."),
        ("H5",
         "<b>G\u00fcde &lt; 1/3 of (W\u00fcsthof + Henckels) mean.</b> The "
         "German-side parallel test. G\u00fcde is a high-end forged German "
         "maker with limited English-language presence \u2014 the same "
         "profile, on the German side, as Masamoto/Sakai Takayuki/Yoshihiro "
         "on the Japanese side. If G\u00fcde under-surfaces alongside "
         "W\u00fcsthof and Henckels dominating, Pattern 4 generalizes to "
         "marketing-language coverage broadly, not Japanese-specifically."),
        ("H6",
         "<b>Within-lab freshness (descriptive only).</b> Pre-registered "
         "without a threshold per the v0.7 H4 precedent. The v0.7 finding "
         "(newer models phantom-mention better, not less) emerged from the "
         "descriptive analysis; holding H6 descriptive in v0.8 preserves the "
         "same epistemic posture, letting the data tell us about generational "
         "behavior rather than committing to a pre-registered direction."),
        ("H7",
         "<b>\u226590% of named authorities are English-language.</b> "
         "Calibrated against v0.6's near-100% English-only authority "
         "observation in skincare DISCOVERY responses. The locked threshold "
         "anchors against authority-mode responses (a whole-response "
         "classification); v0.8 had insufficient authority-mode denominator "
         "(2 of 96 p4+p5 rows), forcing a reframe to authority-naming across "
         "all responses. The reframe is documented per protocol \u00a76.4 "
         "and scored against the same 90% threshold."),
        ("H8",
         "<b>Traditional Japanese aggregate Presence &lt; 5%.</b> The "
         "punchline test. If three boutique Japanese masters \u2014 Masamoto, "
         "Sakai Takayuki, Yoshihiro \u2014 collectively get less than 5% mean "
         "Presence despite being among the most respected makers in Japanese "
         "knife traditions, that is the v0.8 hero finding. The threshold was "
         "calibrated against v0.6 K-beauty Beauty of Joseon at 0%; the "
         "structural parallel is direct."),
    ],
}

# ---- Limitations ----
LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "Phase 2 v0.8 measures one designed-for-test category against a "
            "specific lineage structure. The findings below qualify the "
            "strength of the result. Seven caveats apply."
        ),
        (
            "<b>Single category.</b> Phase 2 v0.8 measures one designed-for-"
            "test category for Pattern 4. Combined with the v0.6 preliminary "
            "observations on olive oil and skincare (where the pattern was "
            "surfaced rather than designed-for-test), v0.8 moves the program "
            "from one-category-preliminary to one-category-confirmed-plus-"
            "two-categories-preliminary. The mechanism (marketing-language "
            "coverage) is not yet generalizable to all cross-lingual "
            "categories on the basis of this measurement plus the v0.6 "
            "observations. Phase 3 will test additional categories."
        ),
        (
            "<b>H1 disconfirmation depends on the locked-registry definition "
            "of the Japanese aggregate.</b> The headline H1 outcome shifts "
            "between disconfirmation (v1.0 locked, 8 brands, jp = 36.2% &gt; "
            "de = 27.3%) and partial confirmation (v1.2 published, 14 brands, "
            "jp = 18.5% &lt; de = 27.3%). The locked-registry score is the "
            "formal pre-registration outcome and is reported as such. The "
            "registry-revision-affecting-aggregate phenomenon is itself "
            "informative: aggregate Presence depends on how comprehensively "
            "boundary-case brands are covered. The mechanism findings (H3, "
            "H5, H7 reframed, H8 within-cohort) do not depend on this choice "
            "and are robust across both registry versions."
        ),
        (
            "<b>American comparator collapse.</b> H2 cannot be evaluated "
            "because the American lineage aggregate landed at 0.6%, below "
            "useful signal threshold. Cutco, Misen, Lamson, Warther, and "
            "Made In collectively contributed almost zero mentions. The "
            "comparator design assumed American brands would surface at "
            "rates between Japanese and German; instead the AI does not "
            "recognize \u201cAmerican kitchen knives\u201d as a meaningful "
            "category at all. This is itself a finding (Finding 4) but it "
            "means the design's robustness control on the \u201cW\u00fcsthof "
            "effect\u201d objection is not directly testable. Phase 3 may "
            "address this by including a non-Japanese non-German non-American "
            "comparator (French, perhaps) where the historical category "
            "discourse is differently mediated."
        ),
        (
            "<b>p3 component-mode contamination.</b> The pre-registered Risk "
            "3 anticipated that the constraint prompt might activate "
            "component-mode rather than brand-mode responses (naming "
            "\u201cVG-10 steel\u201d, \u201csingle bevel\u201d, "
            "\u201cDamascus\u201d instead of brands). Mode classification "
            "shows the risk materialized modestly: 5 of 48 p3 responses are "
            "pure-component, 36 of 48 are mixed-mode (containing both "
            "brands and component vocabulary). H4's per-CEP analysis uses "
            "the brand-surfacing operational unit (\u22651 brand mention), "
            "which captures the 36 mixed responses and the 7 pure-brand "
            "responses; the 5 pure-component responses contribute zero brand "
            "mentions and effectively floor the p3 Japanese aggregate."
        ),
        (
            "<b>AI cross-lab inter-rater agreement.</b> Mode classifications "
            "used a single AI classifier (gpt-5.4-mini at temperature 0). "
            "An AI cross-lab independent audit (Claude Opus 4.7 from "
            "Anthropic, classifying blind on a stratified 25-row sample) "
            "produced 96% agreement on the macro brand-surfacing operational "
            "unit (the unit H1\u2013H8 actually score against), and 68% "
            "strict agreement on the underlying five-mode taxonomy. All "
            "eight strict-agreement disagreements clustered on the brand-"
            "vs-mixed boundary, paralleling v0.7's caveated/correction/"
            "historical adjacency clustering. The strict-agreement gap is a "
            "finding about taxonomy granularity rather than a measurement "
            "quality failure: AI cross-lab inter-rater designs find the "
            "brand-vs-mixed boundary fuzzier than the higher-level brand-"
            "surfacing distinction, which is the methodologically relevant "
            "one for AI Presence measurement."
        ),
        (
            "<b>Registry leakage and out-of-category drift in DISCOVERY.</b> "
            "The DISCOVERY prompt (p5, \u201cemerging or lesser-known knife "
            "brands worth knowing in 2026\u201d) leaked materially into "
            "folding/tactical knife brands rather than premium kitchen knives "
            "\u2014 Vosteed, Civivi, Tactile Knife Co., Null Knives, Jack "
            "Wolf Knives, Kansept, Quiet Carry, CJRB, Kizer, and others "
            "surfaced at material rates in p5 specifically. These were "
            "classified as out-of-category and excluded from the lineage "
            "aggregates, but the leak indicates that AI's \u201cemerging "
            "knife brands\u201d cognitive slot is not strictly bounded to "
            "the kitchen-knife category. p5 contributes the lowest brand-"
            "surfacing rates in the dataset (Japanese 4.2%, German 0.8%, "
            "American 0.0%) partly because of this drift."
        ),
        (
            "<b>Miyabi exploratory finding.</b> Miyabi (Japanese-branded "
            "knife line owned by Zwilling-Henckels, German parent) was "
            "treated as an exploratory hybrid lineage outside the locked "
            "lineage aggregates. Miyabi surfaces at 31.6% \u2014 above the "
            "Japanese-aggregate (18.5%) and the German-aggregate (27.3%), "
            "below the Japanese mass-market mean (55.2%). The single-brand "
            "n=1 evidence is too thin to anchor a finding section; the "
            "observation suggests German-parent English-marketing "
            "infrastructure can elevate a Japanese-origin brand to German-"
            "aggregate-equivalent visibility but not to mass-market-Japanese "
            "leadership levels. Miyabi cross-cites to the Tri-System paper's "
            "Corporate Portfolio Layer (\u00a79.5a) rather than driving v0.8 "
            "narrative."
        ),
        (
            "<b>Construct validity remains unproven.</b> The AI Presence "
            "Index measures a real and stable property of the AI mediation "
            "tier. Whether AI Presence in cross-lingual categories correlates "
            "with consumer consideration, purchase intent, or sales is "
            "currently unknown. The discourse-language-bias finding is a "
            "property of AI mediation, not of consumer behavior; whether "
            "consumers in cross-lingual categories actually substitute "
            "English-marketed brands for non-English-marketed ones at the "
            "rates AI's recommendation behavior would imply is the separate "
            "question the AIAS Phase 3 construct-validity program will "
            "address."
        ),
    ],
}

# ---- What's next ----
WHATS_NEXT = {
    "heading": "What\u2019s next",
    "paragraphs": [
        (
            "<b>Phase 3 \u2014 cross-category replication and construct "
            "validity.</b> The marketing-language-coverage mechanism, if it "
            "generalizes, predicts that any cross-lingual product category "
            "will show within-lineage variance proportional to brand-level "
            "English-language coverage. Two candidate Phase 3 categories are "
            "already in design: premium tea (where Chinese, Japanese, and "
            "Indian production traditions compete with mass-market Western-"
            "language brands) and traditional spirits (where French, "
            "Mexican, Japanese, and Caribbean production traditions are "
            "covered by varying degrees of English-language editorial)."
        ),
        (
            "<b>Phase 3 will also correlate AI Presence against external "
            "consumer-tracking data in cross-lingual categories.</b> If AI "
            "Presence tracks English-language editorial weight rather than "
            "consumer awareness in the brand's home market, then in markets "
            "where the home language and the AI's discourse language differ, "
            "consumers should encounter brand recommendations that diverge "
            "systematically from local consumer awareness. The "
            "marketing-language-coverage mechanism predicts a measurable "
            "asymmetry. Testing this prediction will clarify whether AI "
            "Presence is leading or lagging consumer behavior in cross-"
            "lingual categories."
        ),
        (
            "<b>Methodology paper.</b> The cross-category replication "
            "between v0.7 (newer models phantom-mention better, on a "
            "phantom-recommendation axis) and v0.8 (newer models surface "
            "boundary lineages more, on a discourse-language axis) suggests "
            "that the generational improvement pattern in AI handling of "
            "boundary cases is itself a stable property of the AI training "
            "trajectory rather than an artifact of one boundary axis. A "
            "measurement isolating model-size-vs-cutoff (running same-"
            "category measurements against same-cutoff models of different "
            "sizes within a lab) would clarify the mechanism. A "
            "longitudinal measurement (running the same model against the "
            "same category across a major model update) would isolate the "
            "training-update effect from the model-size effect."
        ),
        (
            "A methodology paper using the v0.6 cross-category dataset, the "
            "v0.7 phantom-brand designed-for-test, and the v0.8 discourse-"
            "language designed-for-test as its empirical spine is planned "
            "for the AIAS measurement program's next publication cycle. The "
            "paper will present the recommendation-slot reframe (v0.7) and "
            "the marketing-language-coverage reframe (v0.8) as a coherent "
            "empirical foundation for the AI Availability Score framework "
            "introduced in <i>Tri-System Brand Growth</i> (Ulpiano Gonzalez "
            "Castro, 2026). The connective thesis: Pattern 4 and Pattern 6 "
            "are different surfaces of the same underlying mechanism \u2014 "
            "AI mediation reserves recommendation slots based on accumulated "
            "editorial weight in the training corpus, and those slots "
            "persist regardless of entity status (v0.7) or original-language "
            "fluency (v0.8)."
        ),
        (
            "<b>Phase 4 \u2014 remaining AIAS components.</b> Phase 4, "
            "contingent on Phase 3 results, will release the remaining five "
            "AIAS components: Ranking, Consistency, Coverage, Grounding, and "
            "Sentiment. The v0.8 measurement provides preliminary data on "
            "Sentiment and Coverage as a side benefit of the structured-"
            "output extraction process; preliminary results will be folded "
            "into Phase 4 documentation when those components ship."
        ),
        (
            "Third System publishes its methodology, its data, and its "
            "corrections openly. Each subsequent report includes the "
            "underlying response dataset alongside the headline findings, "
            "allowing critics, peer reviewers, and customers to verify the "
            "analysis. Brand strategy in the AI-mediated era requires "
            "measurement that can be inspected. The v0.8 report's locked "
            "pre-registration, three registry versions, AI cross-lab audit, "
            "and full scoring tables are all published alongside this report."
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
        "results_v2_knives_v1.0_final.csv  \u00b7  288 measurements",
        "results_enriched_knives_*.csv  \u00b7  brand extraction (v1.0, v1.1, v1.2)",
        "mode_classified_*.csv  \u00b7  five-mode response classification",
        "audit_sample_mode_*.csv  \u00b7  25-row AI cross-lab audit sample",
        "unknowns_classified_*.csv  \u00b7  authority-class entity classification",
        "scoring_tables_*.csv  \u00b7  H1\u2013H8 formal scoring",
        "brands_knives.json  \u00b7  registry v1.2 (27 brands across 4 lineages)",
    ],
    "methodology_log": "PRE_REGISTRATION_knives_v1.0.md (locked 2026-05-06)",
}
