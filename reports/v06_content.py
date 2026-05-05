"""
v06 Cross-Category Findings — structured content.

Authored from v06_source_text.md (which was extracted from report_v0_6_cross.pdf).
Body copy is preserved verbatim per Phase C handoff: typeset what's there, fix only
obvious typos and PDF-extraction artifacts (rejoin hyphenated linebreaks, restore
missing spaces).
"""

# ---- Cover ----
COVER = {
    "title": "Cross-Category Findings",
    "subtitle": "AI Presence Index v0.6 across Five Categories",
    "date": "30 April 2026",
    "byline_short": "Pablo Ulpiano Gonzalez Castro · Third System",
    "tagline": "Independent measurement for the AI mediation layer.",
}

# ---- Standfirst (lead spread) ----
STANDFIRST = "For the first time, we can measure the moment that matters."
LEAD_DECK = (
    "Five categories. Same patterns. AI mediation is producing structural effects "
    "on brand visibility that traditional measurement cannot capture, and the effects "
    "are now clear enough to act on."
)

# ---- Executive summary (the body that opens p1 and runs through p2 of the original) ----
EXEC_SUMMARY = [
    (
        "Third System has measured the AI Presence Index in five categories: project "
        "management software, running shoes, premium olive oil, premium facial skincare, "
        "and personal finance applications. The categories were chosen to span the broadest "
        "possible range of properties — software and physical goods, B2B and consumer, "
        "mature and emerging, identity-light and identity-heavy, US-centric and globally "
        "fragmented, low regulatory salience and high. The five differ on every meaningful "
        "axis except one: each is a category in which a meaningful share of consumers now "
        "consult AI before deciding what to buy."
    ),
    (
        "Across all five, six patterns hold. The first five replicate strongly, in some cases "
        "across all five categories. The sixth emerged from a single category but is the most "
        "consequential single finding in the dataset."
    ),
    (
        "<b>First</b>, AI Presence varies meaningfully across models for the same brand, and "
        "the size of the variance follows the coherence of the category's discourse. Personal "
        "finance, the most fragmented discourse in the dataset, produced a 71-percentage-point "
        "spread for Rocket Money — the largest single-brand variance observed across any "
        "category. Skincare, the most coherent discourse (dermatology consensus, "
        "ingredient-focused, science-positioned), produced single-digit spreads for top brands. "
        "Olive oil and project management software, both fragmented in different ways, produced "
        "spreads of 40 and 41 points. Running shoes, with its converged technical-review "
        "consensus, produced narrow spreads. The relationship between discourse coherence and "
        "per-model variance is now strongly supported across all five categories."
    ),
    (
        "<b>Second</b>, AI converges on incumbents when forced to compare and elevates "
        "challengers when asked about emerging tools. The asymmetry repeats across all five "
        "categories. The strength varies — sharpest in PM software, running shoes, and olive "
        "oil; weaker in skincare where no clear \u201cemerging\u201d tier exists. Across the five "
        "categories, brands that surface in Discovery contexts are systematically different "
        "from brands that surface in Comparison contexts, often dramatically so."
    ),
    (
        "<b>Third</b>, AI brand visibility diverges from consumer awareness, and the gap "
        "intensifies with category age and discourse maturity. Nike places sixth in running "
        "shoes despite the largest marketing budget in the category. Bertolli, Colavita, and "
        "Goya combine for less than 8% AI Presence in olive oil despite dominating supermarket "
        "distribution. La Mer, SK-II, and the entire luxury heritage skincare tier combined "
        "are outscored ten-to-one by CeraVe alone. In personal finance, the divergence inverts "
        "in a different way: YNAB, with roughly one million paid subscribers, achieves 100% AI "
        "Presence, while Rocket Money, with five times more users, surfaces inconsistently "
        "across models."
    ),
    (
        "<b>Fourth</b>, Default Reinforcement intensifies when AI training data carries strong "
        "consensus aligned with the prompt's framing. In skincare, when asked what "
        "dermatologists recommend, three drugstore brands hit 100% mention rate — the AI's "
        "response was nearly deterministic. In personal finance, when asked what people good "
        "with money use, YNAB and Empower hit 100%. The consensus brands win the identity "
        "prompts so completely that brands outside the consensus simply don't appear, "
        "regardless of marketing weight."
    ),
    (
        "<b>Fifth</b>, AI brand visibility appears to carry a discourse-language bias. Spanish "
        "olive oil brands underperformed substantially in a category Spain dominates globally. "
        "Korean skincare brands disappeared entirely in a category where K-beauty is "
        "well-covered in English. The pattern is preliminary — only two categories produced "
        "this signal — but the consistency across two categories with different language "
        "profiles strengthens the finding from where it stood at one category. A category "
        "designed specifically to test the hypothesis is planned for Phase 2 continuation."
    ),
    (
        "<b>Sixth</b>, and most consequentially, AI training data lag creates phantom brand "
        "presence. Mint, the personal finance application shut down by Intuit in March 2024, "
        "was mentioned in 44% of AI responses about personal finance in measurements taken "
        "two years after its decommissioning. On Anthropic specifically, Mint surfaced in 65% "
        "of responses — a brand that no longer exists, mentioned in two-thirds of "
        "recommendations about live products. The implication is direct: AI brand visibility "
        "is its own time-lagged surface, and brands that have shut down, rebranded, or merged "
        "can persist for years in the recommendation tier. Marketers may be optimizing against "
        "competitors that no longer exist, while their own past marketing investment continues "
        "to generate AI presence after their products are discontinued. In AI mediation, "
        "brands die slowly."
    ),
    (
        "The implication for brand strategy compounds across these six findings. Marketers "
        "operating with brand-tracking instruments built for the human-mediated era are "
        "measuring a smaller and time-shifted surface than the one their consumers actually "
        "navigate. Brands that lead in awareness can trail in AI recommendation. Brands that "
        "lead in AI can be unknown to broader markets. Brands that have ceased to exist can "
        "still dominate AI mediation. Every brand valuation model in use today was built for "
        "a world where humans browsed. The AI Presence Index is the adjustment for a world "
        "where they ask."
    ),
    (
        "Third System publishes all five category measurements alongside this summary. "
        "Methodology, full leaderboards, and the underlying datasets are available at "
        "thirdsystem.ai. Phase 3 of the program will correlate these measurements against "
        "external brand-tracking data to test whether AI Presence functions as a leading "
        "indicator of consumer behavior or whether it measures AI behavior in isolation. "
        "Both findings would be useful, and neither has been established."
    ),
]

# ---- "What we measured" ----
WHAT_WE_MEASURED = {
    "heading": "What we measured",
    "paragraphs": [
        (
            "This report combines findings from five Third System category measurements "
            "completed in late April 2026."
        ),
        (
            "The five categories were chosen sequentially, each selected to test framework "
            "properties not represented by prior measurements. Project management software "
            "was the inaugural category, selected for a mature B2B competitive set with high "
            "AI delegation by buyers. Running shoes followed, selected for a contrast on "
            "physical-versus-software, consumer-versus-B2B, and substantially higher identity "
            "load. Premium olive oil was added third, selected to introduce a category in "
            "which English-language editorial discourse dominates a globally distributed "
            "production base. Premium facial skincare was added fourth, selected to test a "
            "category with extremely coherent editorial consensus dominated by dermatological "
            "recommendation logic. Personal finance applications were added fifth, selected "
            "to test a category with regulatory salience, fragmented discourse, and recent "
            "market disruption."
        ),
        (
            "The five categories collectively span every meaningful axis the framework claims "
            "to apply across: identity load (low to very high), buyer type (B2B to consumer), "
            "domain (software, durables, food, beauty, financial services), discourse "
            "coherence (very low to very high), production geography (US-centric to globally "
            "fragmented), and regulatory salience (low to high)."
        ),
        (
            "All five measurements followed the same methodology. Six prompts mapped to "
            "Category Entry Points were issued eight times each to two frontier AI models, "
            "OpenAI's gpt-5.4-mini and Anthropic's claude-sonnet-4-6, at temperature 0.7. "
            "Brand mentions were extracted via structured-output classification and mapped "
            "against a category-specific brand registry. Project management software covered "
            "19 brands, running shoes 17, premium olive oil 20 (after one registry revision), "
            "premium facial skincare 24 (registry of approximately 31 brands; 24 surfaced in measurements), and personal finance "
            "applications 16. Each category produced 96 successful measurements. The headline "
            "metric in each case is Presence: the raw mention rate of each brand across all "
            "measurements, reported on an absolute 0-100 scale without normalization."
        ),
        (
            "Two registry revisions occurred during the measurement period. In premium olive "
            "oil, the first run surfaced Cobram Estate as the most-mentioned brand outside "
            "the registry; the registry was expanded to include it and three additional "
            "brands present in the unknown-mentions list. In premium facial skincare, the "
            "first run surfaced La Roche-Posay, Vanicream, and six additional "
            "dermatologist-recommended drugstore brands as significant unknowns; the registry "
            "was expanded to include all of them. The published data for both categories "
            "comes from the post-revision runs. Earlier runs are preserved in the methodology "
            "log for traceability. The unknown-mentions list serves as a continuing "
            "diagnostic for registry quality, and registry expansion is now a standard "
            "practice across measurement cycles."
        ),
        (
            "The full methodology log, including version history and the documented v0.2 "
            "calibration error, is published as methodology.md v0.3. All five category "
            "leaderboards and the underlying response datasets are available alongside this "
            "report."
        ),
        (
            "Five categories is the threshold at which cross-category claims can move from "
            "suggestive to substantively defensible. The findings reported here cross that "
            "threshold. They are not yet at the threshold of universal generalizability, "
            "which would require both broader category coverage and longitudinal data across "
            "model updates. Phase 2 continuation will introduce both."
        ),
    ],
}

# ---- "Three modes of AI response" ----
THREE_MODES = {
    "heading": "Three modes of AI response",
    "paragraphs": [
        (
            "When we measure AI Presence, we are not measuring a single behavior. Across the "
            "five categories Third System has measured, the AI engages three structurally "
            "distinct modes when responding to category prompts, and which mode it engages "
            "depends on the framing of the question rather than the structure of the "
            "category. Recognizing these modes is foundational to interpreting everything "
            "that follows in this report."
        ),
        (
            "<b>Brand mode</b> is what most of this report measures. The AI is asked about a "
            "category, and it names brands within that category. CeraVe at 100% in skincare's "
            "Identity prompt, YNAB at 100% in personal finance's Identity prompt, Linear and "
            "Asana at 100% in project management software's Comparison prompt — all of this "
            "is brand mode. The AI treats the category as a marketplace of named producers "
            "and answers accordingly."
        ),
        (
            "<b>Component mode</b> appears when the prompt activates a clinical, technical, "
            "or specifications frame. The AI shifts from naming brands to naming ingredients, "
            "materials, or product properties. In skincare, the Contextual prompt about fine "
            "lines in one's late thirties produced this mode 95% of the time. Across both "
            "Anthropic and OpenAI, the AI named SPF 30+, retinol, tretinoin, vitamin C, "
            "niacinamide, hyaluronic acid, and peptides. The AI named almost no brands. It "
            "treated the question as a dermatological consultation, in which the answer is "
            "what's in the bottle, not whose bottle to buy. Olive oil showed component mode "
            "at lower intensity in the Functional prompt (62%): the AI named \u201cextra virgin "
            "olive oil,\u201d \u201cEVOO,\u201d \u201clight olive oil,\u201d and \u201crefined olive oil\u201d "
            "instead of producer brands. The Comparison prompt for olive oil showed component "
            "mode in 62% of empty-canonical responses, with the AI distinguishing "
            "\u201csingle-origin,\u201d \u201cestate-bottled,\u201d and \u201cPDO/PGI\u201d categories rather "
            "than naming specific estates."
        ),
        (
            "<b>Authority mode</b> appears when the prompt asks about discovery, novelty, or "
            "where to learn. The AI shifts from naming brands to naming publications, "
            "communities, retailers, and competitions. In skincare's Discovery prompt, the AI "
            "exclusively named <i>Allure</i>, <i>Byrdie</i>, r/SkincareAddiction, Reddit, "
            "<i>WWD Beauty</i>, <i>Vogue</i>, Sephora, and Ulta. In olive oil's Discovery prompt, "
            "the AI exclusively named <i>Olive Oil Times</i>, NYIOOC World Olive Oil "
            "Competition, <i>Flos Olei</i>, <i>Bon Appétit</i>, <i>Saveur</i>, and "
            "Zingerman's. Asked where the new and noteworthy can be found, the AI named the "
            "discourse infrastructure rather than the products. It treated the question as one "
            "of orientation toward a category's information sources, not as one of product "
            "recommendation."
        ),
        (
            "The implication for measurement is structural. A leaderboard cell with zero "
            "brand mentions does not necessarily indicate a brand's absence from the AI's "
            "awareness. It can indicate that the prompt activated a different mode entirely, "
            "in which the AI was making a different kind of recommendation. Component mode "
            "and authority mode are not measurement failures. They are the AI engaging the "
            "question on a different layer of category understanding, and the framework's job "
            "is to recognize which layer is active."
        ),
        (
            "The implication for brand strategy is broader. AI brand visibility is one of "
            "three surfaces on which a brand competes in the AI tier. The second surface is "
            "ingredient or component association: the brands a consumer associates with "
            "retinoids will benefit from any prompt that activates component mode in skincare, "
            "regardless of the brands' overall AI Presence. The third surface is authority "
            "and publication relationships: the brands featured by the publications the AI "
            "names in authority mode have a privileged path into the AI's discovery "
            "recommendations. A brand strategist who optimizes only for the first surface — "
            "direct brand mentions — will under-invest in the other two."
        ),
        (
            "Future Phase 2 categories will introduce a mode classifier as a pre-step in the "
            "measurement process, allowing each prompt's response to be scored on which mode "
            "it activated, with brand-mode Presence reported alongside the rate of "
            "component-mode and authority-mode activation. This refinement strengthens the "
            "framework's epistemic architecture without requiring re-measurement of existing "
            "categories: the modes are visible in the data already collected, and the existing "
            "Presence scores remain valid as brand-mode-conditional measurements."
        ),
        (
            "What this section establishes will reappear in the patterns that follow. Pattern "
            "4 (discourse-language bias) is strengthened by the observation that "
            "authority-mode responses in two unrelated categories named exclusively "
            "English-language publications. Pattern 5 (Default Reinforcement) is sharpened by "
            "the recognition that the AI's \u201cdefault\u201d can be a mode rather than a brand. "
            "Pattern 1 (per-model variance) reads differently when one accepts that two AIs "
            "may be in different modes for the same prompt rather than disagreeing within "
            "brand mode. The three-mode structure is the foundation; the patterns are "
            "observations across that foundation."
        ),
    ],
}

# ---- Six patterns ----
PATTERNS = [
    {
        "number": 1,
        "title": "AI Presence varies meaningfully across models, in proportion to discourse fragmentation",
        "chart_slot": "inline_p1_variance",
        "paragraphs": [
            (
                "Across all five categories, the same brand can score significantly higher on "
                "one AI than another. The variance is consistent enough to be measured, large "
                "enough to matter for strategy, and follows a predictable relationship with "
                "the structure of the underlying discourse."
            ),
            (
                "The largest single-brand variance observed across the five-category dataset "
                "comes from personal finance. Rocket Money, a subscription-management and "
                "budgeting application owned by Rocket Companies, was mentioned in 71% of "
                "OpenAI responses about personal finance applications and zero percent of "
                "Anthropic responses. Two AI models, asked the same six prompts about the "
                "same category, produced effectively disjoint answers about whether Rocket "
                "Money exists as a category player. Mint, the defunct Intuit application, "
                "showed a 42-point spread in the same direction (Anthropic 65%, OpenAI 23%). "
                "Five other personal finance brands had spreads above 14 points."
            ),
            (
                "Premium olive oil produced spreads nearly as wide. Frescobaldi Laudemio, a "
                "Tuscan estate brand with strong editorial presence and limited US retail "
                "distribution, appeared in 42% of Anthropic responses and 2% of OpenAI "
                "responses, a forty-point spread. Castillo de Canena, a Spanish premium "
                "estate brand, showed the inverse asymmetry. Frantoio Muraglia, an Italian "
                "premium brand, appeared in 15% of Anthropic responses and 42% of OpenAI "
                "responses."
            ),
            (
                "Project management software showed similar magnitudes for top brands. "
                "ClickUp surfaced in 83% of OpenAI responses and 42% of Anthropic responses, "
                "a forty-one-point spread. Asana showed inverse asymmetry, dominant on OpenAI "
                "at 94% and softer on Anthropic at 67%."
            ),
            (
                "Running shoes and skincare produced markedly narrower variance. The largest "
                "top-brand spread in running shoes was Hoka at 19 points. In skincare, CeraVe "
                "registered identical 67% Presence on both models — zero spread, the only "
                "zero-spread leader observed across any category. The largest top-brand "
                "spread in skincare was Paula's Choice at 23 points."
            ),
            (
                "The pattern across five categories now points clearly to a structural "
                "relationship. Variance is not a function of category maturity, the v0.4 "
                "hypothesis: olive oil is mature and produces high variance, while running "
                "shoes is similarly mature and produces low variance. The unifying variable "
                "is discourse coherence. Personal finance has the most fragmented discourse "
                "in the dataset — split across YouTube creators, traditional financial media, "
                "fintech press, Reddit communities, and influencer recommendations, none of "
                "which agree about which brands deserve consideration. Olive oil discourse "
                "fragments across geographies (Italy, Spain, California, Australia), "
                "production traditions, and audience tiers. Project management software "
                "discourse fragments across competing professional frames. Running shoes "
                "discourse converges around a small number of authoritative voices speaking "
                "in one language about a small set of technical criteria. Skincare discourse "
                "converges even more tightly around dermatological recommendation logic. The "
                "two converged-discourse categories produce narrow variance; the three "
                "fragmented-discourse categories produce wide variance."
            ),
            (
                "The relationship is now strongly supported across all five categories. The "
                "implication for brand strategy is that per-model variance is not a transient "
                "artifact of any specific category's youth, but a structural property of how "
                "the AI tier processes the underlying discourse. Brands operating in "
                "fragmented-discourse categories should expect persistent variance across "
                "models and plan AI-channel strategy with that variability in mind. Brands in "
                "converged-discourse categories will see narrower variance but should not "
                "mistake convergence for stability — model updates can shift consensus "
                "quickly, and convergence makes those shifts more visible."
            ),
            (
                "A practical consequence holds in every category measured. A marketer running "
                "an AI-visibility audit on a single model is measuring a slice of a larger "
                "and more variable surface. Multi-model measurement is not a refinement of "
                "the methodology. It is the methodology."
            ),
        ],
    },
    {
        "number": 2,
        "title": "The AI's answer depends on the question",
        "chart_slot": "hero_p2_scatter",
        "paragraphs": [
            (
                "Across all five categories, the AI converges on incumbent brands when forced "
                "to compare options and elevates a sharply different set when asked about "
                "emerging tools. The asymmetry is consistent. The strength varies."
            ),
            (
                "In premium olive oil, the comparison prompt returned California Olive Ranch "
                "and Cobram Estate at near-saturation; the discovery prompt elevated "
                "Brightland, Graza, and Kosterina, three direct-to-consumer brands whose "
                "combined sales are a fraction of the comparison-prompt leaders. In running "
                "shoes, the comparison prompt returned Nike, Asics, and New Balance at 100%; "
                "the discovery prompt returned Norda, a four-year-old Canadian trail-running "
                "brand at 100%. In project management software, comparison returned Asana, "
                "Monday, and Jira at 100%; discovery surfaced Linear and Height. In personal "
                "finance, comparison returned YNAB, Empower, and Monarch Money; discovery "
                "(which named Mint by name) elevated Monarch and Copilot."
            ),
            (
                "Skincare is the structural exception. The comparison prompt produced strong "
                "convergence on CeraVe, Drunk Elephant, and Skinceuticals. But the discovery "
                "prompt did not produce a clear \u201cemerging tier\u201d — Tatcha, Augustinus "
                "Bader, and Youth to the People surfaced at 25%, 25%, and 12% respectively, "
                "with no brand achieving the 50% threshold seen in other categories. The "
                "asymmetry exists in skincare; it is just weaker. The mechanism appears to be "
                "that skincare's editorial discourse has been so thoroughly worked through "
                "that no brand confidently occupies an \u201cemerging\u201d cognitive slot in the "
                "AI's recommendation logic. Every plausible \u201cemerging\u201d skincare brand has "
                "been editorially established for half a decade or more."
            ),
            (
                "Three findings sit inside this asymmetry, all of them strengthened by "
                "five-category replication."
            ),
            (
                "The first is that the AI's working definition of \u201cemerging\u201d is unstable "
                "across categories and consistently does not mean \u201cnew.\u201d In project "
                "management software, the AI's emerging-tools list included Notion, valued in "
                "the tens of billions of dollars. In olive oil, the discovery-prompt leaders "
                "Brightland and Kosterina are seven and eight years old respectively. In "
                "personal finance, the discovery prompt named YNAB at 100% — a 17-year-old "
                "company. The AI's working definition of \u201cemerging\u201d appears to mean "
                "\u201cnon-dominant in the comparison frame,\u201d not \u201cyoung,\u201d \u201csmall,\u201d or "
                "\u201cnovel.\u201d"
            ),
            (
                "The second is that challenger brands can achieve concentrated AI presence in "
                "narrow Category Entry Points without registering at all on broader prompts. "
                "Norda's overall Presence in running shoes is 17%; its Discovery Presence is "
                "100%. Kosterina's overall Presence in olive oil is 27%; its Discovery "
                "Presence is 60%. Augustinus Bader's overall Presence in skincare is 7%; its "
                "Discovery Presence is 25%. The leverage available to a challenger brand in a "
                "single CEP can be much larger than its overall AI visibility would suggest, "
                "and that leverage is the right strategic target."
            ),
            (
                "The third is that prompt design materially affects which version of the "
                "asymmetry shows up. Discovery prompts that name a specific market disruption "
                "(the personal finance prompt naming Mint by name) produce strong "
                "convergence. Discovery prompts that ask generically about \u201cemerging "
                "brands\u201d produce diffuse responses, particularly in categories with no "
                "clearly defined emerging tier. Brand strategy that tests AI presence with "
                "generic discovery prompts will under-detect the visibility available in "
                "narrow CEPs that more concrete framings would surface."
            ),
            (
                "The strategic implication for any challenger brand follows from these three "
                "findings. Pursuing AI visibility as a category-level objective will "
                "under-serve any brand that is not already an incumbent. The visibility worth "
                "pursuing is contextual, varies by the cognitive frame of the consumer query, "
                "and is most accessible to challengers in narrow CEPs where the AI's frame is "
                "more permissive. Strategists who treat AI presence as a single number will "
                "misread the surface they are operating on."
            ),
        ],
    },
    {
        "number": 3,
        "title": "AI brand visibility diverges from consumer awareness, in two directions",
        "chart_slot": "inline_p3_awareness_gap",
        "paragraphs": [
            (
                "Across all five categories, AI brand visibility does not track consumer "
                "awareness, and the gap takes different forms depending on the category's "
                "structure. In four of the five categories, the divergence runs one direction: "
                "brands with high consumer awareness underperform their market position in AI "
                "mediation. In personal finance, the divergence inverts: a brand with modest "
                "market share dominates AI mediation completely. The framework predicts both "
                "directions."
            ),
            (
                "The four downward-divergence cases form a clear pattern. Premium olive oil "
                "shows it in extreme form: the four most distributed legacy supermarket "
                "brands — Bertolli, Colavita, Goya, and Filippo Berio — combine for less than "
                "8% AI Presence in aggregate. Goya, despite being one of the largest Latin "
                "foods brands in the United States, scored exactly zero. Brightland, a "
                "seven-year-old direct-to-consumer brand that exists in only a small fraction "
                "of those brands' retail footprint, scored 46%. AI mediation prefers the "
                "seven-year-old."
            ),
            (
                "Skincare shows it in even sharper form. La Mer, SK-II, Lancôme, Estée Lauder, "
                "Clinique, and Olay — six legacy luxury heritage brands — combine to roughly "
                "6% Presence. CeraVe, the dermatologist-recommended drugstore brand, scored "
                "67% alone. The legacy luxury tier in skincare is outscored ten-to-one by a "
                "single drugstore brand. La Mer's $400 cream loses to CeraVe's $15 cream at "
                "thirty-to-one in AI presence ratio."
            ),
            (
                "Running shoes shows it in less extreme but still strong form. Nike has the "
                "largest marketing budget of any brand in the running-shoe category and "
                "arguably the highest cultural saturation of any brand on Earth. In AI "
                "Presence, Nike places sixth at 57%, behind Asics, Brooks, Saucony, New "
                "Balance, and Hoka. Brooks, a brand whose marketing budget is a fraction of "
                "Nike's, ties for first at 80%."
            ),
            (
                "Project management software shows the divergence in mild form, consistent "
                "with v0.4. AI presence and traditional consideration tracked more closely at "
                "the top of the leaderboard. The asymmetry is not absent — Linear's AI "
                "Presence runs ahead of its current market share — but the gap is narrow."
            ),
            (
                "The fifth case, personal finance, inverts the direction. YNAB, with "
                "approximately one million paid subscribers, scored 100% AI Presence across "
                "every prompt and every model. Rocket Money, with five times more users (over "
                "five million), surfaced in zero percent of Anthropic responses and 71% of "
                "OpenAI responses, depending on the model. EveryDollar, the budgeting "
                "application from Ramsey Solutions with millions of users in its ecosystem, "
                "scored 25%. Empower, the platform for higher net-worth users, scored 66%. "
                "The brand with the smallest user base in the top tier dominates the category "
                "in AI mediation; brands with substantially larger user bases trail or "
                "splinter across models."
            ),
            (
                "The mechanism connecting these five cases is consistent. AI training data "
                "accumulates editorial framings over time. Where editorial discourse builds a "
                "coherent quality narrative aligned with a specific brand's positioning, that "
                "brand's AI presence outpaces its commercial scale. CeraVe is not the largest "
                "skincare brand by revenue; it is the most consistently recommended brand in "
                "dermatological discourse. YNAB is not the largest personal finance brand by "
                "users; it is the most methodologically distinctive brand in the discourse "
                "about financial discipline. The AI tier privileges discourse position over "
                "distribution scale."
            ),
            (
                "The pattern holds in both directions. In categories where editorial "
                "discourse has built up coherent quality narratives, AI mediation rewards "
                "discourse positioning regardless of market share — upward when small brands "
                "have strong narratives, downward when large brands lack them. This is the "
                "same finding pointing two directions, and it now holds across all five "
                "categories."
            ),
            (
                "The implication for brand strategy is that AI visibility is a function of "
                "discourse position, not commercial position, and the two are not necessarily "
                "aligned. In some categories they correlate weakly. In others they correlate "
                "inversely. The CMO of a brand whose marketing investment optimizes for "
                "distribution scale is not necessarily building AI presence. The CMO of a "
                "brand whose investment optimizes for editorial positioning may be building "
                "substantial AI presence on a small commercial base. The instruments of brand "
                "strategy need to read both surfaces, and the reading needs to be specific to "
                "the category being measured."
            ),
        ],
    },
    {
        "number": 4,
        "title": "AI brand visibility appears to carry a discourse-language bias",
        "chart_slot": "hero_p4_country",
        "paragraphs": [
            (
                "The fourth pattern emerged in two of the five categories with consistent "
                "direction, in different national-origin contexts. It remains preliminary "
                "because no measurement to date has been designed specifically to test the "
                "hypothesis. The consistency of the signal across two unrelated categories "
                "strengthens it from where it stood at one category, while leaving room for "
                "refinement."
            ),
            (
                "In premium olive oil, three brands were added to the registry specifically "
                "to ensure Spanish representation. Spain produces more olive oil than any "
                "other country in the world, accounting for roughly 45% of global production. "
                "Goya is one of the most widely distributed Spanish-affiliated brands in the "
                "United States. Castillo de Canena is a premium Andalusian estate brand with "
                "growing US specialty distribution. Núñez de Prado is a respected "
                "family-owned Andalusian producer with strong editorial presence in "
                "Spanish-language food media. Their AI Presence scores were 0%, 23%, and 5% "
                "respectively. None of the three placed in the top five. The category leaders "
                "were California Olive Ranch (US), Cobram Estate (Australia), Brightland "
                "(US), Frantoio Muraglia (Italy), and Graza (US). Italian brands collectively "
                "performed in line with their commercial profile in the US market. American "
                "and Australian brands over-performed relative to global production share. "
                "Spanish brands under-performed substantially."
            ),
            (
                "In premium facial skincare, Beauty of Joseon was included in the registry as "
                "a representative of K-beauty's strongest current brand presence in US "
                "specialty retail. Korean cosmetics enjoy significant English-language "
                "coverage in major beauty media — <i>Allure</i>, <i>Vogue</i>, "
                "<i>Glamour</i>, and <i>The Strategist</i> have published extensively on "
                "K-beauty for over a decade. Beauty of Joseon scored zero across both runs of "
                "the skincare measurement. The skincare unknowns list, which surfaced eight "
                "additional missing brands, contained no non-English-discourse brands at all. "
                "Every brand the AI surfaced as a category player was an American DTC brand "
                "or a French/American clinical brand."
            ),
            (
                "The most defensible explanation for both results is that AI training corpora "
                "over-represent English-language discourse on these categories, and the bias "
                "persists even when the cultural reference of the brand is well-covered in "
                "English. American food magazines, Italian food media translated into "
                "English, and US-based recipe websites dominate the digital corpus on olive "
                "oil. American beauty magazines and US-based dermatology blogs dominate the "
                "corpus on skincare. Spanish-language food media and Korean-language beauty "
                "media, even when authoritative within their domestic markets, do not "
                "propagate into English-language AI training data at the rates that "
                "comparable English-language sources do. The AI's recommendations therefore "
                "reflect the geography and language of the discourse it was trained on, not "
                "the geography of the production it is asked about."
            ),
            (
                "A subtle refinement of the hypothesis becomes visible across the two cases. "
                "Tatcha, a Japanese-themed skincare brand founded in San Francisco with "
                "American-English marketing, scored 18% Presence in skincare. Beauty of "
                "Joseon, a Korean brand with Korean-language primary marketing despite some "
                "US-targeted English content, scored zero. The cultural reference (Japanese "
                "aesthetic) does not seem to be the constraint. The marketing-discourse "
                "language does. The hypothesis, refined: <i>AI under-surfaces brands whose "
                "primary marketing discourse is conducted in a language under-represented in "
                "AI training data, even when the cultural reference is well-known in "
                "English.</i>"
            ),
            (
                "The audit of authority-mode responses across the two affected categories "
                "provides additional, unexpected evidence for the discourse-language "
                "hypothesis. When the AI was asked about discovery in skincare and olive oil, "
                "it named publications, communities, and retailers rather than brands. Every "
                "publication the AI named was English-language: <i>Allure</i>, <i>Byrdie</i>, "
                "<i>Vogue</i>, and <i>WWD Beauty</i> in skincare; <i>Olive Oil Times</i>, "
                "<i>Flos Olei</i>, <i>Bon Appétit</i>, and <i>Saveur</i> in olive oil. "
                "Spanish-language food media did not appear. Korean-language beauty media did "
                "not appear. Japanese, Italian, French, and German publications respected "
                "within their domestic categories did not appear. The AI's recommended path "
                "to category orientation runs entirely through English-language sources, even "
                "in categories where authoritative non-English sources demonstrably exist. "
                "This is not a finding about which brands the AI surfaces; it is a finding "
                "about which infrastructure the AI treats as legitimate. The "
                "discourse-language bias in brand recommendations is consistent with a deeper "
                "bias in which media systems are recognized as authoritative."
            ),
            (
                "This finding remains preliminary in three ways. It is based on two "
                "categories with single nationally-skewed signals each. It involves small "
                "absolute numbers of test brands. And the alternative explanations — US "
                "retail availability, marketing investment in English-targeted channels, or "
                "category-specific distribution structures — have not been controlled for. A "
                "more rigorous test would require measuring a category in which a "
                "non-English-discourse country dominates global production but has limited "
                "US-targeted English-language marketing, and observing whether the same "
                "asymmetry persists. Japanese kitchen knives, French wine, or Korean small "
                "electronics would each provide such a test. Phase 2 continuation will "
                "include at least one such category."
            ),
            (
                "If subsequent measurements confirm the pattern, the implications are wide. "
                "AI mediation may systematically under-surface brands whose primary discourse "
                "is conducted in languages or media systems under-represented in AI training "
                "corpora. For global brands, this would mean that domestic-language "
                "brand-building does not propagate into international AI mediation at the "
                "same rate that English-language brand-building does. Brand strategy that "
                "ignores this asymmetry will under-invest in English-language presence "
                "relative to its strategic value, particularly for brands whose AI-mediated "
                "visibility matters in markets outside their primary linguistic context."
            ),
            (
                "This is hypothesis at the edge of finding. Two categories support it. A "
                "third designed-for-test category will determine its status."
            ),
        ],
    },
    {
        "number": 5,
        "title": "Default Reinforcement intensifies with discourse-prompt alignment",
        "chart_slot": "inline_p5_default_reinforcement",
        "paragraphs": [
            (
                "The fifth pattern is closely connected to Pattern 1 (discourse coherence) "
                "and Pattern 3 (AI vs awareness divergence) but distinct from both. It "
                "describes how the strength of incumbent dominance in AI mediation depends "
                "not just on the underlying discourse coherence, but on how well-aligned that "
                "discourse is with the framing of the prompt itself."
            ),
            (
                "Skincare provides the cleanest illustration. The Identity prompt asked: "
                "\u201cWhat skincare brands do dermatologists actually recommend to their "
                "patients?\u201d CeraVe, Cetaphil, and Neutrogena each appeared at 100% mention "
                "rate. Three brands tied at perfect saturation in 96 measurements. The "
                "Constraint prompt asked about sensitive skin: CeraVe and La Roche-Posay each "
                "appeared at 100%, with Vanicream at the same level. The Functional prompt "
                "asked about moisturizers for normal-to-dry skin: CeraVe at 100%. Across "
                "three different prompts framed in three different ways, the answers "
                "converged on the same small set of dermatologist-recommended drugstore "
                "brands."
            ),
            (
                "The mechanism is visible: skincare's editorial discourse has built a tight, "
                "well-documented consensus that dermatologists recommend specific "
                "clinical-positioning brands, and the prompts in this study repeatedly "
                "aligned with that consensus. When the AI's training data carries strong "
                "consensus and the prompt's cognitive frame activates that consensus, the "
                "AI's response is nearly deterministic. There is no observable randomness; "
                "the same brands appear at saturation across measurements."
            ),
            (
                "Personal finance shows a parallel pattern with different content. The "
                "Identity prompt asked about apps that \u201cpeople who are actually good with "
                "money use,\u201d loaded but ambiguous identity language. YNAB and Empower both "
                "scored 100% on this prompt. The Comparison prompt produced YNAB, Empower, "
                "and Monarch Money each at 100%. The Constraint prompt about partners "
                "managing money together produced YNAB and Monarch Money each at 100%. "
                "Across multiple identity frames, the AI converged on the same small brand "
                "set with deterministic confidence."
            ),
            (
                "The contrast with running shoes and PM software is informative. In running "
                "shoes, the Identity prompt (\u201cwhat serious competitive runners actually "
                "wear\u201d) produced Nike at 100% — but no other brand reached 100% on that "
                "prompt. The category's discourse is more contested between cultural-narrative "
                "(\u201cNike is what serious runners wear\u201d) and technical-recommendation "
                "(\u201cAsics and Brooks are what serious runners wear\u201d) framings. AI "
                "surfaces both, depending on which CEP is activated. The discourse exists; "
                "the prompt-discourse alignment is weaker."
            ),
            (
                "In PM software, the Identity prompt produced multiple brands across both "
                "models without any single brand reaching saturation. The category's "
                "discourse fragments across multiple identity-loaded frames (developer-first, "
                "marketing-first, generalist), none of which dominates. Default Reinforcement "
                "is observable, but compressed."
            ),
            (
                "The cross-category data now suggests a structural relationship: the strength "
                "of Default Reinforcement at the prompt level is a function of how "
                "completely the category's editorial consensus aligns with the prompt's "
                "framing. When alignment is high (skincare's dermatologist prompts, personal "
                "finance's discipline prompts), AI responses are nearly deterministic. When "
                "alignment is partial (running shoes' identity prompt, PM software's "
                "frame-divided prompts), AI responses are stratified. When alignment is low "
                "(any prompt that activates a discourse the AI's training data does not "
                "strongly carry), AI responses are diffuse."
            ),
            (
                "The strategic implication for brand strategy is consequential and practical. "
                "A brand attempting to build AI presence cannot do so by general marketing "
                "investment; it must build editorial position aligned with the specific "
                "cognitive frames consumers are likely to use when prompting AI in the "
                "category. Generic awareness-building does not propagate into AI mediation "
                "efficiently. Identity-aligned editorial positioning does, with "
                "disproportionate efficiency in categories where consensus is tight. The "
                "leverage of the right editorial position in the right CEP is far higher than "
                "the leverage of broad-distribution awareness investment."
            ),
        ],
    },
    {
        "number": 6,
        "title": "AI training data lag creates phantom brand presence",
        "chart_slot": "inline_p6_phantom",
        "paragraphs": [
            (
                "The sixth pattern emerged from a single category measurement but is "
                "sufficiently striking to warrant inclusion as a standalone finding. It "
                "describes a structural property of AI-mediated brand visibility that no "
                "prior pattern captures: the temporal lag between actual market reality and "
                "the AI tier's representation of that market."
            ),
            (
                "In March 2024, Intuit decommissioned Mint, its consumer personal finance "
                "application that had been the dominant brand in the category for over a "
                "decade. Existing users were migrated to Credit Karma; the Mint application "
                "was retired; the brand effectively ceased to exist as a current consumer "
                "product. By April 2026, when this measurement was conducted, Mint had not "
                "been a live application for 25 months."
            ),
            (
                "In Third System's measurement of personal finance applications, Mint was "
                "mentioned in 44% of AI responses. Among brands with non-zero Presence "
                "scores, Mint placed fifth — ahead of Rocket Money, EveryDollar, Quicken "
                "Simplifi, and PocketGuard, all of which are live applications with active "
                "user bases. The AI tier mentioned a brand that had not existed for over two "
                "years more frequently than it mentioned multiple applications consumers can "
                "actually use today."
            ),
            (
                "Per-model breakdown reveals an additional dimension. On Anthropic, Mint "
                "surfaced in 65% of responses. On OpenAI, Mint surfaced in 23% of responses. "
                "The 42-point spread is the second-largest in the category dataset, and it "
                "suggests that the two AI models have meaningfully different training-data "
                "freshness on this specific category change. Anthropic's recommendations "
                "remain anchored in pre-shutdown training data more strongly than OpenAI's. "
                "Both systems lag actual market reality, in different ways and to different "
                "extents."
            ),
            (
                "The mechanism is straightforward. AI training corpora are necessarily "
                "backward-looking. They capture the discourse that existed when the data was "
                "crawled, not the discourse that exists at the moment a query is made. For a "
                "brand that had been the dominant player for over a decade and had "
                "accumulated proportionate volume of editorial coverage, blog posts, "
                "comparison articles, and how-to guides, that backward-facing volume "
                "continues to surface in responses long after the brand itself has stopped "
                "existing. The AI tier does not have a mechanism to remove a brand from its "
                "training corpus when the brand shuts down. The corpus simply ages, and the "
                "brand persists within it."
            ),
            (
                "The implications follow directly. AI brand visibility is not a current "
                "measurement of market reality. It is a measurement of how the AI tier "
                "currently weighs an aging corpus against more recent inputs. This makes the "
                "AI Presence Index a hybrid signal: partly reflective of current market "
                "position, partly reflective of accumulated marketing investment that may "
                "extend many years backward, partly reflective of category disruptions that "
                "have not yet propagated through the AI's training systems."
            ),
            (
                "For brand strategy, the implications cascade. A brand that has shut down, "
                "been acquired, or rebranded continues to generate AI presence for an "
                "indeterminate period after the change. Marketers may be allocating budget "
                "against a competitor that no longer exists, while their own past marketing "
                "investment continues to generate AI presence after their products are "
                "discontinued. A brand currently rebranding may face a multi-year period "
                "during which the new brand name underperforms in AI mediation while the old "
                "name persists. A brand entering a category currently dominated by a defunct "
                "brand may find it easier to win AI presence than the leaderboard structure "
                "would suggest, because the dominant entity is not actually competing for "
                "share."
            ),
            (
                "The single-category basis for this finding limits its current "
                "generalizability. Other category disruptions — Twitter's rebrand to X, the "
                "GE Brands company splits, the Toys R Us shutdown and limited revival, "
                "several pharmaceutical brand transitions — would provide additional test "
                "cases. Phase 2 continuation will include at least one category selected "
                "specifically for the presence of a recent major brand disruption, to test "
                "whether the phantom brand presence pattern observed for Mint replicates in "
                "other category-shutdown contexts."
            ),
            (
                "<i>In AI mediation, brands die slowly.</i> The brand value of a discontinued "
                "brand persists in the AI tier for years after the brand stops existing in "
                "the market. Every brand strategist needs to know whether their category "
                "contains such phantoms, because the leaderboard cannot be read accurately "
                "without that knowledge."
            ),
        ],
    },
]

# ---- Limitations ----
LIMITATIONS = {
    "heading": "Limitations",
    "paragraphs": [
        (
            "Five categories meets the threshold at which cross-category claims become "
            "substantively defensible. They do not meet the threshold at which the patterns "
            "can be claimed as universal. Six limitations apply to the findings reported here."
        ),
        (
            "<b>Sample size.</b> Each category measurement comprises 96 successful API "
            "calls, producing approximately ten-percentage-point confidence bands around "
            "individual brand Presence scores. The cross-category patterns reported here "
            "survive that uncertainty because the patterns are large relative to the band. "
            "Smaller margins between specific brands within a category should not be treated "
            "as decisive."
        ),
        (
            "<b>Two models, not three.</b> The original measurement design included Google's "
            "Gemini, which has been excluded from v0.3, v0.4, and v0.6 results because of a "
            "Workspace-domain access restriction during the study window. Gemini will be "
            "reinstated when the restriction clears. Cross-model variance reported here is "
            "likely a lower bound; introducing a third model historically widens the range, "
            "and the variance findings would likely strengthen."
        ),
        (
            "<b>Five categories, not many.</b> Five categories is enough to claim replication "
            "of patterns across diverse contexts. It is not enough to claim that the patterns "
            "hold in general. Phase 2 continuation will introduce additional categories "
            "specifically designed to test framework predictions, including a category "
            "designed to test the discourse-language bias hypothesis introduced in Pattern 4."
        ),
        (
            "<b>A single point in time per category.</b> Each category was measured on a "
            "single day in late April 2026. The findings describe AI behavior on those days. "
            "They do not describe how AI brand visibility moves over time. AI models are "
            "updated frequently, often without external notice. Longitudinal measurement "
            "requires periodic re-baselining and will be added in Phase 2 continuation. The "
            "phantom brand presence pattern (Pattern 6) is the most time-sensitive of the "
            "findings; its strength may evolve as AI training data refreshes."
        ),
        (
            "<b>Construct validity remains unproven.</b> The AI Presence Index measures a "
            "real and stable property of the AI tier, but whether that property correlates "
            "with consumer consideration, purchase intent, or sales is currently unknown. A "
            "correlation study against external brand-tracking data is planned for Phase 3. "
            "Until that study is complete, AI Presence should be treated as a leading "
            "indicator with unverified predictive value."
        ),
        (
            "<b>Registry construction is not perfectly neutral.</b> The brand registry for "
            "each category is curated and reflects the framework's view of which brands "
            "constitute the category's competitive set. Two of the five categories required "
            "registry revision after the first measurement surfaced significant unknown "
            "brands. The unknown-mentions list provides a continuing diagnostic, but "
            "registry construction remains the methodological choice with the most direct "
            "effect on which brands appear in measurements."
        ),
    ],
}

# ---- What's next ----
WHATS_NEXT = {
    "heading": "What\u2019s next",
    "paragraphs": [
        (
            "Phase 2 will continue with two additional category measurements designed to test "
            "specific framework predictions. The first is a category selected explicitly to "
            "test the discourse-language bias hypothesis from Pattern 4: a category in which "
            "a non-English-discourse country dominates global production but has limited "
            "US-targeted English-language marketing. Candidate categories include Japanese "
            "kitchen knives, French wine, and Korean small electronics. The second is a "
            "category selected to test the phantom brand presence hypothesis from Pattern 6: "
            "a category with a recent major brand disruption (shutdown, acquisition, or "
            "rebrand) sufficient to generate measurable training-data lag effects. Candidate "
            "categories include social media platforms (testing the Twitter-to-X transition), "
            "retail (testing the Bed Bath &amp; Beyond shutdown and revival), and several "
            "pharmaceutical brand transitions."
        ),
        (
            "Phase 3 is the construct-validity study. The structure is straightforward. AI "
            "Presence scores from at least three categories, measured at two points in time, "
            "will be correlated against consumer-tracking data from the same windows. The "
            "result will determine whether AI-mediated visibility predicts shifts in "
            "consideration, purchase intent, or share of category. A finding of strong "
            "correlation establishes the AI Presence Index as a leading indicator with "
            "predictive value beyond the AI tier itself. A finding of weak correlation "
            "establishes the index as a measurement of AI behavior alone, with strategic "
            "implications limited to AI-channel optimization. Both outcomes are publishable, "
            "and both are useful."
        ),
        (
            "Phase 4, contingent on Phase 3 results, will release the remaining five AIAS "
            "components: Ranking, Consistency, Coverage, Grounding, and Sentiment. Each will "
            "be added as a separate measurement layer, with documented rationale and a "
            "defined trigger condition for inclusion. The order of release will follow the "
            "priority specified in the methodology log: Consistency first because it is "
            "computable from existing data, Ranking second because the framework's strategic "
            "implications depend on it, the others as cross-category data permits."
        ),
        (
            "Third System publishes its methodology, its data, and its corrections openly. "
            "Each subsequent report includes the underlying response dataset alongside the "
            "leaderboard, allowing critics, peer reviewers, and customers to verify the "
            "analysis. Brand strategy in the AI-mediated era requires measurement that can "
            "be inspected."
        ),
    ],
}

# ---- Closing footer block (final page) ----
CLOSING = {
    "byline_long": [
        "Pablo Ulpiano Gonzalez Castro",
        "Principal Researcher, Third System",
        "Faculty, MPS Branding Program, School of Visual Arts",
    ],
    "datasets": [
        "presence_index_v0.3_pmsoftware.csv",
        "presence_index_v0.3_runningshoes.csv",
        "presence_index_v0.3_oliveoil.csv",
        "presence_index_v0.3_skincare.csv",
        "presence_index_v0.3_finance.csv",
    ],
    "methodology_log": "methodology.md v0.3",
}
