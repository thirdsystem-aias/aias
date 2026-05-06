---
title: "Third System — Cross-Category Findings"
subtitle: "AI Presence Index v0.4 across Three Categories"
date: "Third System  ·  30 April 2026"
---

*For the first time, we can measure the moment that matters.*

**The same brand visibility patterns repeat across three categories that share almost nothing else. AI mediation is producing structural effects in brand strategy that traditional measurement cannot capture.**

Third System has now measured the AI Presence Index in three categories: premium olive oil, a mature consumer category dominated by editorial discourse and fragmented across geographies; running shoes, a mature consumer category with strong incumbent brand-building and clear technical sub-segments; and project management software, a young B2B category in active competitive flux. The three differ in buyers, decision cycles, distribution structures, identity loads, and cultural meanings. They should not, on first principles, behave alike in AI-mediated recommendation.

They behave alike anyway. Four patterns hold across all three.

First, AI Presence varies meaningfully across models for the same brand. The variance is widest where the underlying discourse is most fragmented — Frescobaldi Laudemio appears in 42% of Anthropic responses about premium olive oil and 2% of OpenAI responses, a forty-point gap. The variance is narrowest in mature categories with strong industry consensus, like running shoes, where the largest spread among top brands is twenty points. Every category measured produces brands whose AI visibility depends materially on which AI delivers the recommendation.

Second, AI converges on incumbents when forced to compare and elevates challengers when asked about emerging tools. The same asymmetry repeats in all three categories. In olive oil, the comparison prompt returned California Olive Ranch and Cobram Estate at near-saturation; the discovery prompt elevated Brightland, Graza, and Kosterina, three direct-to-consumer brands whose combined sales are a fraction of the incumbents'. In running shoes, the comparison prompt returned Nike, Asics, and New Balance; the discovery prompt returned Norda, a four-year-old Canadian brand. In project management software, comparison returned Asana, Monday, and Jira; discovery surfaced Linear and Height. The cognitive frame of the question shapes the answer more than the underlying merits of the brands do.

Third, AI brand visibility diverges from consumer awareness, and the gap is largest in mature categories where editorial discourse has had time to accumulate. In olive oil, the most distributed legacy supermarket brands — Bertolli, Colavita, Goya, Filippo Berio — combine for less than 8% AI Presence in aggregate. Brightland, a seven-year-old direct-to-consumer brand that exists in only a small fraction of those brands' retail footprint, scores 46%. The pattern repeats with Nike in running shoes, where Nike places sixth at 57% Presence behind Asics, Brooks, Saucony, New Balance, and Hoka, despite having the largest marketing budget of any brand in the category. Project management software, the youngest category, shows the divergence in milder form: AI elevates Linear above its current market share, but incumbents remain near the top of the leaderboard. The decoupling between AI visibility and consumer awareness compounds with category age.

Fourth, AI brand visibility appears to carry a discourse-language bias. In olive oil, three brands were added to the registry specifically to ensure Spanish representation — Goya, Castillo de Canena, Núñez de Prado. Spain produces more olive oil than any other country in the world. The three Spanish brands scored 0%, 23%, and 5% respectively. The English-language food media, which makes up the bulk of AI training data on this category, is centered in the United States and Italy. The AI's recommendations reflect the geography of the discourse, not the geography of the production. This finding emerged from a single category and is preliminary, but it has implications for any global brand whose marketing is conducted in a language other than English.

The implication for brand strategy is direct. Marketers operating with brand-tracking instruments built for the human-mediated era are measuring a smaller surface than the one their consumers actually navigate. Brands that lead in awareness can trail in AI recommendation. Brands that lead in AI can be unknown to broader markets. Brands that lead in their domestic non-English discourse can be invisible in AI mediation. The decoupling is structural and measurable. Every brand valuation model in use today was built for a world where humans browsed. The AI Presence Index is the adjustment for a world where they ask.

Third System publishes all three category measurements alongside this summary. Methodology, full leaderboards, and the underlying datasets are available at thirdsystem.ai. Phase 3 of the program will correlate these measurements against external brand-tracking data to test whether AI Presence functions as a leading indicator of consumer behavior or whether it measures AI behavior in isolation. Both findings would be useful, and neither has been established.

## What we measured

This report combines findings from three Third System category measurements completed in late April 2026. Project management software was the inaugural category, selected for its mature competitive set and high AI delegation by buyers. Running shoes followed, selected to test the framework against a category with sharply different properties: physical goods rather than software, consumer rather than B2B, mature rather than emerging, and meaningfully higher identity load. Premium olive oil was added third, selected to introduce a category in which English-language editorial discourse dominates the global production base, where direct-to-consumer brands have built strong cultural presence on small distribution footprints, and where major supermarket incumbents are widely distributed but face active critical scrutiny in food media.

All three measurements followed the same methodology. Six prompts mapped to Category Entry Points were issued eight times each to two frontier AI models, OpenAI's gpt-5.4-mini and Anthropic's claude-sonnet-4-6, at temperature 0.7. Brand mentions were extracted via structured-output classification and mapped against a category-specific brand registry. Project management software covered 19 brands across 96 successful measurements. Running shoes covered 17 brands across 96 successful measurements. Premium olive oil covered 20 brands across 96 successful measurements. The headline metric in each case is Presence: the raw mention rate of each brand across all measurements, reported on an absolute 0-100 scale without normalization.

The full methodology log, including version history and the documented calibration error in v0.2, is published as `methodology.md v0.3`. All three category leaderboards and the underlying response datasets are available alongside this report.

The premium olive oil registry was revised once during the measurement period. The first run surfaced an Australian brand, Cobram Estate, as the most-mentioned brand outside the registry, at 53 mentions. The registry was expanded to include Cobram Estate and three additional brands present in the unknown-mentions list. The full data presented in this report comes from the post-revision run. The earlier run is preserved in the methodology log for traceability.

Three categories is the threshold at which cross-category claims become meaningfully more defensible than they were at two. The findings reported here meet that threshold. A fourth and fifth category measurement, planned for Phase 2 continuation, will further test whether these patterns persist across categories with higher regulatory salience and stronger demographic skew.

![](chart_leaderboards_side_by_side.pdf){ width=100% }

*Top 8 brands by AI Presence in each of the three categories. Bars colored by tier: incumbent (dark), mid-tier (gray), challenger (rust).*


## Pattern 1: AI Presence varies meaningfully across models

The first pattern that holds across all three categories is the existence of measurable per-model variance for individual brands. The same brand can score significantly higher on one AI than another, in ways that no single-model measurement would surface.

Premium olive oil produced the widest variance observed in any of the three categories. Frescobaldi Laudemio, a Tuscan estate brand with strong editorial presence and limited US retail distribution, appeared in 42% of Anthropic responses and 2% of OpenAI responses, a forty-point spread. Castillo de Canena, a premium Spanish estate brand, showed the inverse asymmetry, appearing in 8% of Anthropic responses and 38% of OpenAI responses. Frantoio Muraglia, an Italian premium brand, hit 15% on Anthropic and 42% on OpenAI. Five olive oil brands showed cross-model spreads exceeding 15 points.

Project management software produced spreads of similar magnitude, though concentrated in different brand archetypes. ClickUp surfaces in 83% of OpenAI responses and 42% of Anthropic responses, a forty-one-point spread. Asana shows the inverse asymmetry, dominant on OpenAI at 94% and softer on Anthropic at 67%. For five of the top ten brands in the PM category, the gap between the two models exceeded eighteen percentage points.

Running shoes produced the narrowest variance of the three categories. The largest spread among top brands was Hoka at 18.8 points (Anthropic 62.5%, OpenAI 81.2%) and Nike at 18.7 points (Anthropic 47.9%, OpenAI 66.7%). The category leaders, Asics and Brooks, showed much tighter cross-model agreement at six and two points respectively.



![](chart_per_model_variance.pdf){ width=100% }

*The largest per-model variance for top brands across all three categories. Each row shows AI Presence on Anthropic (dark) and OpenAI (rust), with the spread on the right.*

The pattern across all three points to a deeper finding. The 2024 v0.3 report (covering only two categories) suggested that variance correlates with category maturity — newer categories show wider AI disagreement, older categories show convergence. With three categories, that framing is incomplete. Olive oil is mature, with fifty years of accumulated industry discourse, but produces the widest variance of the three. Running shoes is mature with comparable industry consensus, but produces the narrowest. The difference is not maturity. The difference is **discourse fragmentation**. Olive oil discourse fragments across geographies (Italy, Spain, California, Australia), languages, technical traditions (cold-pressed, single-estate, blended), and audience segments (chefs, food writers, supermarket shoppers, DTC enthusiasts). Running shoes discourse, by contrast, has converged around a small number of authoritative voices (running stores, performance reviewers, podiatrists) speaking in one language about a small set of technical criteria. Project management software discourse is mid-fragmentation, with multiple competing frames (developer-first, marketing-first, generalist) that have not yet stabilized.

The implication is that per-model variance is not a transient artifact of a category being young. It is a stable property of the category's underlying discourse structure. Brands operating in fragmented-discourse categories should expect persistent AI variance and plan their channel strategies accordingly. Brands operating in convergent-discourse categories will see narrower AI variance, but should not mistake convergence for stability — model updates can shift consensus quickly.

A practical consequence: a marketer running an AI-visibility audit on a single model is measuring a slice of a larger and more variable surface. Multi-model measurement is required to surface the full picture. Brands that lead on the model the analyst tested can trail on the one the consumer used, and the gap is not small.

## Pattern 2: The AI's answer depends on the question

The second cross-category pattern is the asymmetry between Comparison and Discovery prompts. All three categories show the same behavior: when AI is forced to compare options, it converges on incumbents; when asked about emerging tools, it elevates a sharply different set of brands.

In premium olive oil, the comparison prompt returned California Olive Ranch and Cobram Estate at near-saturation (88% each), with Brightland in third position. Both leaders are mass-distribution incumbents in the supermarket and warehouse-club channels. The discovery prompt produced an entirely different leaderboard: Brightland, Graza, and Kosterina each at exactly 50%, three direct-to-consumer brands with combined sales that are a fraction of the comparison-prompt leaders. None of the discovery-prompt top three appears at the top of the comparison prompt.

In running shoes, the comparison prompt produced 100% mention rates for Nike, Asics, and New Balance, three of the most established performance brands on the planet. The discovery prompt produced a leaderboard with Norda at 100%, Topo Athletic at 75%, and On at 31%. Norda is a four-year-old Canadian trail-running brand. Most consumers have never heard of it. The AI surfaces it as the top "emerging" brand in 100% of cases when asked.

In project management software, the comparison prompt returned 100% mention rates for Asana, Monday, and Jira, the three most established tools in the category. The discovery prompt produced a different leaderboard, with Linear at 100%, Notion at 94%, and Height at 81% mention rates.



![](chart_cep_comparison.pdf){ width=100% }

*AI Presence by Category Entry Point for the top 6 brands in each category. Cell intensity = mention rate. Color = tier.*

Three findings sit inside this asymmetry, all of them strengthened by the three-category replication.

The first is that the AI's working definition of "emerging" is unstable across categories, but consistently does not mean "new." In project management software, the AI's emerging-tools list included Notion, a company valued in the tens of billions of dollars. In olive oil, the discovery-prompt leaders Brightland and Kosterina are seven-to-eight years old. The AI's definition of "emerging" appears to mean "non-dominant in the comparison frame" rather than "young," "small," or "novel."

The second is that challenger brands can achieve concentrated AI presence in narrow Category Entry Points without registering at all on broader prompts. In olive oil, Kosterina's overall Presence is 27%; its Discovery Presence is 60%. In running shoes, Norda's overall Presence is 16.7%; its Discovery Presence is 100%. The leverage available to a challenger brand in a single CEP can be much larger than its overall AI visibility would suggest, and that leverage is the right strategic target.

The third is that the asymmetry is a structural feature of how AI handles the recommendation task, not a category-specific quirk. The replication across three categories with sharply different properties strongly suggests this. The mechanism is likely simple: when forced to compare, the AI minimizes risk by anchoring on the safest answers; when asked about emerging tools, the AI minimizes redundancy by surfacing brands that aren't already in the safe-answer set. Brand strategy that ignores this asymmetry will misread its own market.

The strategic implication for any challenger brand follows from these findings. Pursuing AI visibility as a category-level objective will under-serve any brand that is not already an incumbent. The visibility worth pursuing is contextual, varies by the cognitive frame of the consumer query, and is most accessible to challengers in narrow CEPs where the AI's frame is more permissive. Strategists who treat AI presence as a single number will misread the surface they are operating on.

## Pattern 3: AI brand visibility diverges from consumer awareness

The third cross-category pattern is the one with the most consequential implications for working brand strategy. AI brand visibility does not track consumer awareness, and the size of the gap varies systematically by category in ways that are now visible across three measurements.

Premium olive oil shows the divergence in its sharpest form. The four most distributed legacy supermarket olive oil brands — Bertolli, Colavita, Goya, and Filippo Berio — combine for less than 8% AI Presence in aggregate. Goya, despite being one of the largest Latin foods brands in the United States, scored exactly zero. The two leading brands by AI Presence are California Olive Ranch at 70% and Cobram Estate at 49%, both mass-distribution but with strong recent editorial positioning around quality. The two leading challengers, Brightland at 46% and Graza at 28%, are direct-to-consumer brands that exist in only a small fraction of the legacy brands' retail footprint. Brightland is seven years old. Bertolli has been on American supermarket shelves for over fifty years. AI mediation prefers the seven-year-old.

Running shoes shows the same pattern in less extreme form. Nike has the largest marketing budget of any brand in the running-shoe category and arguably the highest cultural saturation of any brand on Earth. In the AI Presence Index, Nike places sixth at 57.3%, behind Asics, Brooks, Saucony, New Balance, and Hoka. Brooks, a brand whose marketing budget is a fraction of Nike's, is tied for first at 80.2%. The mechanism is visible in the per-CEP data. When the prompt asks about identity ("what running shoes do serious competitive runners actually wear"), Nike hits 100% mention rate. When the prompt asks about utility ("the best running shoe for someone training for their first marathon"), Nike does not appear in the top three. The AI tier appears to associate Nike with the cultural performance of running rather than with the technical practice of it.

Project management software, the youngest category in the dataset, shows the divergence in mild form. AI presence and traditional consideration tracked more closely at the top of the leaderboard, with Asana, Jira, and Linear all clustering near 80% Presence. The category is too young for a strong divergence between awareness and AI visibility to have built up. The asymmetry is not absent — Linear's AI Presence runs ahead of its current market share, in a way that prefigures the larger divergences seen in olive oil and running shoes — but the gap is narrow.

The pattern across three categories suggests a structural relationship: **the divergence between AI visibility and consumer awareness compounds with category age and discourse maturity.** In young categories, AI mediation and consumer awareness still track each other. In mature categories with active editorial discourse, they decouple. In olive oil, where editorial discourse has had decades to articulate quality criteria distinct from supermarket distribution, the decoupling is nearly complete. The mechanism appears to be that AI training data accumulates editorial framings over time, while consumer awareness still reflects distribution scale and advertising weight. The two measure different surfaces, and the surfaces drift apart.

The implication for brand strategy is direct. AI visibility is its own surface, with its own selection logic. In some categories that surface tracks consumer awareness closely. In others, particularly mature categories where editorial discourse has shaped quality narratives, the surfaces have decoupled and continue to drift apart. A CMO who measures only the consumer-awareness surface will not see what the AI tier is doing to brand consideration. A CMO who measures only the AI surface will miss the brands that still dominate human-mediated channels. The instruments of brand strategy need to read both surfaces, and the reading needs to be specific to the category being measured.

## Pattern 4: AI brand visibility appears to carry a discourse-language bias

The fourth pattern is the most preliminary of the four. It emerged from a single category and has not yet been replicated. It is reported here because the implications, if confirmed, are significant for any global brand whose marketing is conducted in a language other than English.

In premium olive oil, three brands were added to the registry specifically to ensure Spanish representation. Spain produces more olive oil than any other country in the world, accounting for roughly 45% of global production. Goya is one of the most widely distributed Spanish-affiliated brands in the United States. Castillo de Canena is a premium Andalusian estate brand with growing US specialty distribution. Núñez de Prado is a respected family-owned Andalusian producer with strong editorial presence in food media.

Their AI Presence scores were 0%, 23%, and 5% respectively. None of the three Spanish brands placed in the top five. The category leaders were California Olive Ranch (US), Cobram Estate (Australia), Brightland (US), Frantoio Muraglia (Italy), and Graza (US). Italian brands collectively performed in line with their commercial profile in the US market. American and Australian brands over-performed relative to global production share. Spanish brands under-performed substantially.

The most defensible explanation for this asymmetry is that AI training corpora over-represent English-language food media, which is centered in the United States and Italy. American food magazines, Italian food media translated into English, and US-based recipe websites dominate the digital corpus on olive oil. Spanish-language food media, even when authoritative within Spain, does not propagate into English-language AI training data at the same rate. The AI's recommendations therefore reflect the geography of the discourse it was trained on, not the geography of the production it is asked about.

This finding is preliminary in three ways. It is based on a single category, with a single national-origin under-represented. It involves a small absolute number of brands (three Spanish brands, against thirteen non-Spanish ones in the registry). And the alternative explanations — Spanish brand availability in the US market, retail positioning, or marketing investment by Spanish brands in US-targeted channels — have not been controlled for. A more rigorous test would require measuring a category in which a non-English-discourse country dominates global production but has limited US presence, and observing whether the same asymmetry persists.

If subsequent measurements confirm the pattern, the implications are wide. AI mediation may systematically under-surface brands whose primary discourse is conducted in languages or media systems under-represented in AI training corpora. For global brands, this would mean that domestic-language brand-building does not propagate into international AI mediation at the same rate that English-language brand-building does. Brand strategy that ignores this asymmetry will under-invest in English-language presence relative to its strategic value.

This is hypothesis, not finding. Phase 2 measurements will include at least one category designed specifically to test it.

## Limitations

The findings reported here meet the threshold at which cross-category claims become meaningfully more defensible than they were at two categories. They do not meet the threshold at which the patterns can be claimed as universal. Five limitations should be considered before drawing strategic conclusions.

**Sample size.** Each category measurement comprises 96 successful API calls, producing approximately ten-percentage-point confidence bands around individual brand Presence scores. The cross-category patterns reported here survive that uncertainty because the patterns are large relative to the band. Smaller margins between specific brands within a category should not be treated as decisive.

**Two models, not three.** The original measurement design included Google's Gemini, which has been excluded from v0.3 and v0.4 results because of a Workspace-domain access restriction during the study window. Gemini will be reinstated when the restriction clears. Cross-model variance reported here is likely a lower bound; introducing a third model historically widens the range, and the variance findings would likely strengthen.

**Three categories, not many.** Three categories is enough to claim replication of a pattern across diverse contexts. It is not enough to claim that the patterns hold in general. A fourth and fifth category measurement, planned for Phase 2 continuation, will test whether these patterns persist in categories with higher regulatory salience and stronger demographic skew. Pattern 4 specifically requires a fourth category designed to test the discourse-language bias hypothesis.

**A single point in time.** All three categories were measured on single days in late April 2026. The findings describe AI behavior on those days. They do not describe how AI brand visibility moves over time. AI models are updated frequently, often without external notice. Longitudinal measurement requires periodic re-baselining and will be added in Phase 2 continuation.

**Construct validity remains unproven.** The AI Presence Index measures a real and stable property of the AI tier, but whether that property correlates with consumer consideration, purchase intent, or sales is currently unknown. A correlation study against external brand-tracking data is planned for Phase 3. Until that study is complete, AI Presence should be treated as a leading indicator with unverified predictive value.

## What's next

Phase 2 will continue with two additional category measurements. The selection criteria favor categories that test the framework against properties not represented in the current set: a category with high regulatory salience, where AI-mediated recommendations carry consumer-protection implications; and a category designed to test the discourse-language bias hypothesis introduced in Pattern 4, in which a non-English-language production geography dominates global supply but is under-represented in English-language editorial discourse. Candidate categories under consideration for the regulatory-salience slot include personal finance tools, mental health applications, and consumer healthcare devices. Candidate categories for the language-bias test include Japanese knife brands, French wine, or German automotive accessories. The exact selections will be announced before Phase 2 measurement begins.

Phase 3 is the construct-validity study. The structure is straightforward. AI Presence scores from at least three categories, measured at two points in time, will be correlated against consumer-tracking data from the same windows. The result will determine whether AI-mediated visibility predicts shifts in consideration, purchase intent, or share of category. A finding of strong correlation establishes the AI Presence Index as a leading indicator with predictive value beyond the AI tier itself. A finding of weak correlation establishes the index as a measurement of AI behavior alone, with strategic implications limited to AI-channel optimization. Both outcomes are publishable, and both are useful.

Phase 4, contingent on Phase 3 results, will release the remaining five AIAS components: Ranking, Consistency, Coverage, Grounding, and Sentiment. Each will be added as a separate measurement layer, with documented rationale and a defined trigger condition for inclusion. The order of release will follow the priority specified in the methodology log: Consistency first because it is computable from existing data, Ranking second because the framework's strategic implications depend on it, the others as cross-category data permits.

Third System publishes its methodology, its data, and its corrections openly. Each subsequent report will include the underlying response dataset alongside the leaderboard, allowing critics, peer reviewers, and customers to verify the analysis. Brand strategy in the AI-mediated era requires measurement that can be inspected.

---

*Authored by Pablo Ulpiano Gonzalez Castro. Methodology log: methodology.md v0.3. Underlying datasets: presence_index_v0.3_pmsoftware.csv, presence_index_v0.3_runningshoes.csv, presence_index_v0.3_oliveoil.csv. Inquiries: hello@thirdsystem.ai.*
