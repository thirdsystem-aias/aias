---
title: "Third System — Cross-Category Findings"
subtitle: "AI Presence Index v0.3 across Two Categories"
date: "Third System  ·  29 April 2026"
---

**The same brand visibility patterns repeat across categories that share almost nothing else. AI mediation is producing structural effects in brand strategy that traditional measurement cannot capture.**

Third System has now measured the AI Presence Index in two categories: project management software, a young B2B category with low identity load, and running shoes, a mature consumer category with high identity load. The two have different buyers, different price points, different decision cycles, and different cultural meanings. They should behave very differently in AI-mediated recommendation.

They behave alike anyway. Three patterns hold in both.

First, AI Presence varies meaningfully across models for the same brand. The variance is wider in PM software, where a brand can score forty-one points higher on one AI than another, and narrower in running shoes, where the spread for top brands is closer to twenty points. Every category measured produces brands whose AI visibility depends materially on which AI delivers the recommendation.

Second, AI converges on incumbents when forced to compare and elevates challengers when asked about emerging tools. In PM software, the comparison prompt returned Asana, Monday, and Jira at 100% mention rate; the discovery prompt surfaced Linear and Height. In running shoes the same asymmetry sharpens further: the comparison prompt returned Nike, Asics, and New Balance at 100%; the discovery prompt returned Norda, a four-year-old Canadian trail brand most consumers have never heard of, also at 100%. The cognitive frame of the question shapes the answer more than the underlying merits of the brands do.

Third, AI brand visibility diverges from consumer awareness in measurable ways that vary by category. The most striking instance is Nike. Nike has the largest marketing budget of any brand in this study and arguably the highest cultural saturation of any brand on Earth. In Third System's measurement of running shoes, Nike places sixth, behind Asics, Brooks, Saucony, New Balance, and Hoka. The AI tier weights technical credibility over cultural saturation. Traditional brand tracking, which measures awareness as if all attention were equivalent, does not surface this distinction.

These three patterns emerged independently in each category before being compared. The replication across categories with sharply different identity loads is the strongest evidence so far that the framework describes something structural about AI-mediated visibility itself.

The implication for brand strategy is direct. Marketers operating with brand-tracking instruments built for the human-mediated era are measuring a smaller surface than the one their consumers actually navigate. Brands that lead in awareness can trail in AI recommendation. Brands that lead in AI can be unknown to broader markets. The two are decoupling, and the decoupling is measurable.

Third System publishes both category measurements alongside this summary. Methodology, full leaderboards, and the underlying datasets are available at thirdsystem.ai. Phase 3 of the program will correlate these measurements against external brand-tracking data to test whether AI Presence functions as a leading indicator of consumer behavior or whether it measures AI behavior in isolation. Both findings would be useful, and neither has been established.

## What we measured

This report combines findings from two Third System category measurements completed in April 2026. Project management software was the inaugural category, selected for its mature competitive set and high AI delegation by buyers. Running shoes followed, selected to test the framework against a category with sharply different properties: physical goods rather than software, consumer rather than B2B, mature rather than emerging, and meaningfully higher identity load.

Both measurements followed the same methodology. Six prompts mapped to Category Entry Points were issued eight times each to two frontier AI models, OpenAI's gpt-5.4-mini and Anthropic's claude-sonnet-4-6, at temperature 0.7. Brand mentions were extracted via structured-output classification and mapped against a category-specific brand registry. PM software covered 19 brands across 96 successful measurements; running shoes covered 17 brands across 96 successful measurements. The headline metric in each case is Presence: the raw mention rate of each brand across all measurements, reported on an absolute 0-100 scale without normalization.

The full methodology log, including version history and the documented calibration error in v0.2, is published as `methodology.md v0.3`. Both category leaderboards and the underlying response datasets are available alongside this report.

Two categories is the minimum threshold at which cross-category claims become defensible. The findings reported here meet that threshold and not more. A third and fourth category measurement, planned for Phase 2 continuation, will test whether these patterns persist or whether they are artifacts of the specific category pair selected.

![](chart_leaderboards_side_by_side.pdf){ width=100% }

*Top 10 brands by AI Presence in each category. Bars colored by tier: incumbent (dark), mid-tier (gray), challenger (rust).*


## Pattern 1: AI Presence varies meaningfully across models

The first pattern that holds across both categories is the existence of measurable per-model variance for individual brands. The same brand can score significantly higher on one AI than another, in ways that no single-model measurement would surface.

In project management software, the variance is striking. ClickUp surfaces in 83% of OpenAI responses and 42% of Anthropic responses, a forty-one point spread. Linear, the category leader, hits 100% on Anthropic and 73% on OpenAI. Asana shows the inverse asymmetry, dominant on OpenAI at 94% and softer on Anthropic at 67%. For five of the top ten brands in the category, the gap between the two models exceeds eighteen percentage points.

In running shoes, the variance is real but compressed. The largest spread among top brands is Hoka at 18.8 points (Anthropic 62.5%, OpenAI 81.2%) and Nike at 18.7 points (Anthropic 47.9%, OpenAI 66.7%). The category leaders, Asics and Brooks, show much tighter cross-model agreement at six and two points respectively.



![](chart_per_model_variance.pdf){ width=100% }

*The largest per-model variance for top brands in both categories. Each row shows AI Presence on Anthropic (dark) and OpenAI (rust), with the spread on the right.*

The compression of variance in running shoes relative to PM software is a finding in itself. PM software is a young category in flux: the AI models still disagree about category boundaries, about which tools are PM tools, and about which challengers deserve incumbent status. Running shoes is a mature category with fifty years of accumulated industry consensus, much of which is reflected in the corpus the AI models trained on. The framework appears to predict that per-model variance correlates inversely with category maturity. Newer categories show wider AI disagreement; older categories show convergence.

The implication for brand strategy is the same in both categories. A marketer running an AI-visibility audit on a single model is measuring a slice of a larger and more variable surface. Multi-model measurement is required to surface the full picture. Brands that lead on the model the analyst tested can trail on the one the consumer used, and the gap is not small.

## Pattern 2: The AI's answer depends on the question

The second cross-category pattern is the asymmetry between Comparison and Discovery prompts. Both categories show the same behavior: when AI is forced to compare options, it converges on incumbents; when asked about emerging tools, it elevates a sharply different set of brands.

In PM software, the Comparison prompt produced 100% mention rates for Asana, Monday, and Jira, the three most established tools in the category. The Discovery prompt produced a different leaderboard, with Linear at 100%, Notion at 94%, and Height at 81% mention rates.

In running shoes, the same asymmetry sharpens further. The Comparison prompt produced 100% mention rates for Nike, Asics, and New Balance, three of the most established performance brands on Earth. The Discovery prompt produced a leaderboard with Norda at 100%, Topo Athletic at 75%, and On at 31%. Norda is a four-year-old Canadian trail-running brand. Most consumers have never heard of it. The AI surfaces it as the top "emerging" brand in 100% of cases when asked.



![](chart_cep_comparison.pdf){ width=100% }

*AI Presence by Category Entry Point for the top 6 brands in each category. Cell intensity = mention rate. Color = tier.*

Two related findings sit inside this asymmetry. The first is that the AI's working definition of "emerging" is unstable. In PM software, the AI's emerging-tools list included Notion, a company valued in the tens of billions of dollars. Notion is by no reasonable definition emerging. The AI's definition appears to mean "non-dominant" rather than "new." The second finding is that challenger brands can achieve concentrated AI presence in narrow Category Entry Points without registering at all on broader prompts. Norda's overall Presence in running shoes is 16.7%; its Discovery Presence is 100%. The leverage available to a challenger brand in a single CEP is potentially much larger than its overall AI visibility would suggest.

The strategic implication for brand strategy follows from these findings. Pursuing AI visibility as a category-level objective will under-serve any brand that is not already an incumbent. The visibility worth pursuing is contextual, varies by the cognitive frame of the consumer query, and is most accessible to challengers in narrow CEPs where the AI's frame is more permissive. Strategists who treat AI presence as a single number will misread the surface they are operating on.

## Pattern 3: AI brand visibility diverges from consumer awareness

The third cross-category pattern is the most consequential for working brand strategy. AI brand visibility does not track consumer awareness, and the gap between the two varies in measurable ways by category.

Nike is the clearest illustration. By any traditional brand-tracking measure, Nike is among the strongest brands in the world: largest marketing budget in the running-shoe category, highest unaided awareness, deepest cultural penetration. In Third System's measurement of running shoes, Nike places sixth at 57.3% Presence, behind Asics, Brooks, Saucony, New Balance, and Hoka. Brooks, a brand whose marketing budget is a fraction of Nike's, is tied for first at 80.2%. Saucony, in third place at 78.1%, ranks above Nike by twenty points. The AI tier is reading the running-shoe category differently from the way the cultural conversation reads it.

The mechanism is visible in the per-CEP data. When the prompt asks about identity ("what running shoes do serious competitive runners actually wear"), Nike hits 100% mention rate. When the prompt asks about utility ("the best running shoe for someone training for their first marathon"), Nike does not appear in the top three. The AI tier appears to associate Nike with the cultural performance of running rather than with the technical practice of it. Asics, Brooks, and Saucony — brands historically built around fit, motion control, and runner specialization — dominate the utility prompts.

The pattern has an inverse in PM software. There, AI presence and traditional consideration tracked more closely at the top of the leaderboard, with Asana, Jira, and Linear all clustering near 80% Presence. The category is too young for a strong divergence between awareness and AI visibility to have built up. The asymmetry is not absent in PM software; it appears in narrower forms, such as the AI's tendency to elevate Linear above its current market share. In running shoes, with fifty years of accumulated brand-building, the divergence is structural and large.

What this means for brand strategy is direct. AI visibility is its own surface, with its own selection logic. In some categories that surface tracks consumer awareness closely. In others, particularly mature categories where technical recommendation matters, the surfaces have decoupled and continue to drift apart. A CMO who measures only the consumer-awareness surface will not see what the AI tier is doing to brand consideration. The instruments of brand strategy need to read both surfaces, and the reading needs to be specific to the category being measured.

## Limitations

Two categories is the minimum threshold at which cross-category claims are defensible. The findings in this report meet that threshold and not more. Five limitations should be considered before drawing strategic conclusions.

**Sample size.** Each category measurement comprises 96 successful API calls, producing approximately ten-percentage-point confidence bands around individual brand Presence scores. The cross-category patterns reported here survive that uncertainty because the patterns are large relative to the band. Smaller margins between specific brands within a category should not be treated as decisive.

**Two models, not three.** The original measurement design included Google's Gemini, which was excluded from the v0.3 results because of free-tier rate limits during the study window. Gemini will be reinstated in v0.4. Cross-model variance reported here is likely a lower bound; introducing a third model historically widens the range.

**Two categories, not many.** Two categories is enough to claim replication of a pattern. It is not enough to claim that the pattern holds in general. A third and fourth category measurement, planned for Phase 2 continuation, will test whether these patterns persist across categories with higher regulatory salience, different demographic profiles, and varying decision urgency.

**A single point in time.** Both categories were measured on single days in late April 2026. The findings describe AI behavior on those days. They do not describe how AI brand visibility moves over time. AI models are updated frequently, often without external notice. Longitudinal measurement requires periodic re-baselining and will be added in Phase 2 continuation.

**Construct validity remains unproven.** The AI Presence Index measures a real and stable property of the AI tier, but whether that property correlates with consumer consideration, purchase intent, or sales is currently unknown. A correlation study against external brand-tracking data is planned for Phase 3. Until that study is complete, AI Presence should be treated as a leading indicator with unverified predictive value.

## What's next

Phase 2 will continue with two additional category measurements. The selection criteria favor categories that test the framework against properties not represented in the current pair: a category with high regulatory salience, where AI-mediated recommendations carry consumer-protection implications; and a category with strong demographic skew, where the AI's recommendation logic may interact with audience composition in ways the present sample cannot test. Candidate categories under consideration include personal finance tools, mental health applications, and consumer healthcare devices. The fourth category will be selected after the third is complete, informed by what the third reveals.

Phase 3 is the construct-validity study. The structure is straightforward. AI Presence scores from at least three categories, measured at two points in time, will be correlated against consumer-tracking data from the same windows. The result will determine whether AI-mediated visibility predicts shifts in consideration, purchase intent, or share of category. A finding of strong correlation establishes the AI Presence Index as a leading indicator with predictive value beyond the AI tier itself. A finding of weak correlation establishes the index as a measurement of AI behavior alone, with strategic implications limited to AI-channel optimization. Both outcomes are publishable, and both are useful.

Phase 4, contingent on Phase 3 results, will release the remaining five AIAS components: Ranking, Consistency, Coverage, Grounding, and Sentiment. Each will be added as a separate measurement layer, with documented rationale and a defined trigger condition for inclusion. The order of release will follow the priority specified in the methodology log: Consistency first because it is computable from existing data, Ranking second because the framework's strategic implications depend on it, the others as cross-category data permits.

Third System publishes its methodology, its data, and its corrections openly. Each subsequent report will include the underlying response dataset alongside the leaderboard, allowing critics, peer reviewers, and customers to verify the analysis. Brand strategy in the AI-mediated era requires measurement that can be inspected.

---

*Authored by Pablo Ulpiano Gonzalez Castro. Methodology log: methodology.md v0.3. Underlying datasets: presence_index_v0.3_pmsoftware.csv and presence_index_v0.3_runningshoes.csv. Inquiries: hello@thirdsystem.ai.*
