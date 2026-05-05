---
title: "AI Presence Index v0.3"
subtitle: "Project Management Software"
date: "Third System  ·  29 April 2026"
---

**AI brand visibility varies by as much as 42 percentage points across major AI models for the same brand in the same category. The era of measuring brand strength as a single number is ending.**

Third System's first study of the AI Presence Index, the foundational layer of the AIAS framework, measured project management software across 19 brands, two frontier AI models, and 96 prompted recommendations. The most consequential finding has nothing to do with which brand led the leaderboard. It is how much the leaderboard changes depending on which AI a consumer happens to ask.

ClickUp appears in 83% of OpenAI responses and 42% of Anthropic responses. Asana shows the opposite pattern, dominant on OpenAI and softer on Anthropic. Linear, a seven-year-old challenger competing against incumbents two decades older, was mentioned in every Anthropic response and 73% of OpenAI ones. No conventional brand tracker would surface a result like that, because conventional brand trackers were built for a world where every consumer received roughly the same set of cultural inputs. AI mediation changes that.

A second pattern emerges across category entry points. When the AI is asked to compare options, it consistently returns the incumbents: Asana, Monday, and Jira appear in 100% of comparison-context responses. When asked about emerging tools, it elevates a mixed set of mid-tier players and challengers. The framing of the question shapes the answer more than the underlying merits of the brands do, and brand strategy that ignores this asymmetry will misread its own market.

Brand measurement has a forty-year history of treating share of voice, share of mind, and recall as single numbers attached to single brands. Those instruments worked when consumers shared a media environment. They do not work when the answer to "what should I buy" varies by which AI delivered the recommendation. Strategists need new tools, calibrated to the new conditions.

This report releases the AI Presence Index v0.3, an open-methodology measurement of one of the six AIAS components. The other five — Ranking, Consistency, Coverage, Grounding, and Sentiment — will follow as cross-category data accumulates. Throughout, methodology is disclosed in full, including a documented calibration error in v0.2 and the correction applied in v0.3. Critics, peer reviewers, and customers should be able to see and audit every choice.

---

## What we measured

Project management software was chosen as the inaugural category for three reasons. The competitive set is mature enough to include both incumbents and challengers, the buyers genuinely use AI assistants to evaluate tools, and the identity load of the category is low enough that AI delegation is plausible at scale. Future Third System reports will cover categories with higher identity load, where the AI mediation question takes a different shape.

The measurement collected 96 successful AI recommendations across six prompts, each mapped to a Category Entry Point from the Ehrenberg-Bass tradition: Functional, Contextual, Constraint-driven, Identity-loaded, Discovery, and Comparison. Each prompt was issued eight times to OpenAI's gpt-5.4-mini and Anthropic's claude-sonnet-4-6, at temperature 0.7. Brand mentions were extracted using a structured-output classifier and mapped against a registry of 19 PM-software brands.

No brand names appear in any prompt. This rules out one of the most common contamination patterns in AI-mediated brand studies: prompts that name a brand inflate that brand's mention rate, producing measurements of the prompt rather than of the AI. The trade-off is that brands outside the registry surface as unknowns and do not score, which is a deliberate choice to preserve category integrity.

The headline metric, Presence, is the raw mention rate across all measurements. It is reported on a 0-100 absolute scale, not normalized to the leader. Three companion metrics — Rank-weighted Share, Primary Recommendation Rate, and Consistency across models — are reported alongside Presence for transparency, but are not blended into the headline score. The full methodology, including version history and a documented calibration error in v0.2, is published as `methodology.md v0.3`.

---

## Finding 1: Variance is the story

When the same brand can score 100 on one AI and 73 on another, the question "what is this brand's AI visibility?" becomes ill-posed. There is no single answer. There are model-specific answers, and they diverge.

Linear, the strongest performer in the dataset, illustrates the pattern at its sharpest. Every Anthropic response in this study mentioned Linear. Only 73% of OpenAI responses did. Twenty-seven percentage points separate the two scores for what the brand strategy literature would treat as a single brand-perception measurement. Asana shows the inverse asymmetry, leading on OpenAI at 94% and softening to 67% on Anthropic. ClickUp opens an even wider gap: 83% on OpenAI, 42% on Anthropic, a 41-point spread on a brand that traditional brand-tracking would describe in a single line.

Notion is the conspicuous exception. It appears in 81% of Anthropic responses and 77% of OpenAI ones, a four-point spread that is consistent across measurements. Notion has achieved what most brands in the dataset have not: AI presence that does not depend on which AI a consumer happens to use. That consistency may be a leading indicator of mature AI-tier brand strength. It may also be an artifact of Notion's content saturation across the open web. Both possibilities are testable in subsequent rounds of measurement.

The implication for brand strategy is direct. Marketers running AI-visibility audits with a single-model benchmark are measuring one slice of a much more variable surface. A brand can lead on the model the analyst happened to test and trail on the one the consumer happened to use. Multi-model measurement is not a refinement of the existing methodology. It is the methodology.

---

## Finding 2: The AI's answer depends on the question

A second pattern emerges across the six Category Entry Points tested in this study. The same brand pool produces different rankings depending on the cognitive frame of the prompt.

When the prompt requests a comparison ("compare the leading options and recommend the best one"), the AI converges on incumbents. Asana, Monday, and Jira each appear in 100% of comparison-context responses. The discovery prompt ("what are some emerging project management tools worth knowing about in 2026") elevates a different set, in which Linear, Notion, and Height surface most reliably. Notion, at 94% mention in the discovery context, is a particularly striking case. The brand has a reported valuation in the tens of billions and is by no reasonable definition an emerging tool. Yet the AI's working definition of "emerging" includes it.

The constraint-driven prompt, which specified an engineering context, produced the most differentiated result. Jira and Linear each appeared in 100% of responses, and GitHub Projects, which barely surfaces elsewhere in the data, also reaches 100% mention rate when the engineering context is supplied. The cognitive frame unlocks a sub-segment of the brand pool that is otherwise dormant.

What this means in practice is that AI-mediated brand visibility is not a steady-state property of the brand. It is a function of the brand and the question, and the question varies by consumer intent. A challenger brand cannot simply pursue "AI visibility" as a global objective. The visibility worth pursuing is contextual, and the strongest leverage often lies in narrow CEPs where the AI's frame admits brands that broader prompts exclude.

---

## Limitations

This study is the first measurement under a methodology that will improve. Five limitations should be considered before drawing strategic conclusions from the findings.

**The sample is small.** Ninety-six successful API calls produces a 95% confidence band of approximately ten percentage points around any individual brand's Presence score. The 42-point variance reported in Finding 1 is well outside this band and survives the sampling constraint. Smaller margins between brands at the leaderboard's middle are within the band and should not be read as decisive. Future measurements will use 200 or more calls per category, narrowing the band to roughly five points.

**Two models, not three.** The original measurement design included Google's Gemini, which was excluded from the v0.3 results because the free-tier rate limits made completion infeasible during the study window. Gemini will be reinstated in v0.4 once paid-tier billing is configured. The two-model variance reported here is likely a lower bound; introducing a third model historically widens the range.

**One category, one moment.** The findings describe project management software on a single day in late April 2026. They do not generalize to other categories without further measurement, and they say nothing about how AI-mediated visibility moves over time. Both gaps are scheduled to close in Phase 2, when at least three additional categories will be measured under the same methodology.

**Construct validity is unproven.** The Presence Index measures a real and stable property of the AI tier, but whether that property correlates with consumer consideration, purchase intent, or sales is currently unknown. A correlation study against external brand-tracking data — likely YouGov BrandIndex or Kantar — is planned for Phase 3. Until that study is complete, AI Presence should be treated as a leading indicator with unverified predictive value.

**The brand registry is curated, not exhaustive.** Nineteen brands were selected as the project management software competitive set. Twelve other brands appeared in AI responses with sufficient frequency to suggest they belong in subsequent rounds of measurement, including Coda's collaboration peers and several developer-tooling crossovers. Decisions about registry expansion are documented in the methodology log. Marketers concerned about a specific brand's omission should contact Third System directly.

---

## What's next

Phase 2 will extend the AI Presence Index to four additional categories selected for variation in identity load and AI delegation behavior. Three are confirmed: consumer running shoes, wireless audio, and customer relationship management software. The fourth will be selected from a list of candidate categories with high regulatory or trust salience — financial services, healthcare, and legal tools are under consideration. Each report will follow the same methodology, with version increments documented openly.

Phase 3 will conduct the construct-validity study against external brand-tracking data. The structure is straightforward: AI Presence scores from at least three categories, measured at two points in time, will be correlated against consumer-tracking data from the same windows. The result will determine whether AI-mediated visibility predicts shifts in consideration, purchase intent, or share of category. A finding of strong correlation establishes the Presence Index as a leading indicator. A finding of weak correlation establishes it as a measurement of AI behavior alone, with strategic implications limited to AI-channel optimization. Either outcome is publishable, and both are useful.

Phase 4, contingent on Phase 3 results, will release the remaining five AIAS components — Ranking, Consistency, Coverage, Grounding, and Sentiment — as separate measurement layers, integrated into a composite AIAS score. The order of release will follow the operational priority specified in the methodology log: Consistency first, because it is computable from existing data; Ranking second, because the framework's strategic implications depend on it; the others as cross-category data permits.

Third System publishes its methodology, its data, and its corrections openly. Subsequent reports will include the underlying response dataset alongside the leaderboard, allowing critics, peer reviewers, and customers to verify the analysis. Brand strategy in the AI-mediated era requires measurement that can be inspected, not measurement that asks for trust.

---

*Authored by Pablo Ulpiano Gonzalez Castro. Methodology log: methodology.md v0.3. Underlying dataset: presence_index_v0.3_20260429_181355.csv. Inquiries: hello@thirdsystem.ai.*
