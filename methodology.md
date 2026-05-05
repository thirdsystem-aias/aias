# Methodology — AI Presence Index (Tri-System AIAS Framework)

**Project:** Third System — AI-Mediated Brand Visibility Measurement
**Author:** Pablo Ulpiano Gonzalez Castro
**Current Version:** v0.3
**Last Updated:** 2026-04-29

---

## 1. What This Document Is

This is the methodology log for the AI Presence Index measurement system, the first operational implementation of the AIAS (AI Availability Score) framework specified in the Tri-System Brand Growth model.

This document is the source of truth for how data is collected, processed, and scored. Any published report should cite a specific version of this methodology. Future critics, peer reviewers, and customers will compare published numbers against this log; if a discrepancy arises, the methodology log governs.

---

## 2. Conceptual Foundation

The AIAS framework, as specified in the Tri-System book and academic paper, defines AI Availability as a six-component composite:

1. **Presence** — frequency of brand surfacing across AI-mediated queries
2. **Ranking** — position-weighted prominence within AI responses
3. **Consistency** — variance of brand visibility across AI models
4. **Coverage** — distribution of presence across Category Entry Points
5. **Grounding quality** — quality of sources the AI draws on for the brand
6. **Sentiment posture** — directional valence of how the brand is described

Each component is intended to be measured on a 0–100 scale, where 100 represents near-saturation. The headline AIAS score is a composite, equal-weighted by default, until calibration data accumulates to support evidence-based weighting.

**Current implementation measures Presence only.** This is appropriate for Phase 1 deployment in a category where no prior measurement exists. The eBook explicitly supports this staged approach: *"adopting AIAS now is appropriate for organizations operating in mediated categories where the alternative is no measurement at all"* and *"the methodology will be refined as cross-organization data accumulates."*

The published output is therefore labeled **AI Presence Index** rather than **AIAS**, in alignment with the framework's component-based architecture. AIAS as a full composite will be reported only once at least three components are measured with stable methodology across multiple categories.

---

## 3. Version History

### v0.1 — Day 2 baseline (2026-04-28)
- 5 prompts × 3 models × 5 runs = 75 calls
- Brand registry: 15 brands
- Detection: regex word-boundary matching against alias list
- Output metric: mention rate, displayed as raw percentage

### v0.2 — Path C, Step 1 (2026-04-29 morning)
- Same 5 prompts, same registry
- Re-extracted existing data with structured-output (function calling) extraction
- Added rank, sentiment, primary-recommendation flags
- Composite formula introduced: `0.4 × MentionRate + 0.4 × RankSOM + 0.2 × PrimaryRecRate`
- Output normalized so leader = 100

**v0.2 calibration error (acknowledged and corrected in v0.3):**
The v0.2 composite used rank-relative normalization, dividing all brand scores by the leader's score. This forced whichever brand led to display as 100, regardless of absolute performance. With Asana, Jira, and Linear all clustered near 79% mention rate, the v0.2 output displayed Linear at 100 and the others at 92 and 84 respectively, implying near-saturation that the underlying data did not support.

This was identified as inconsistent with the framework's own definition, which specifies AIAS as a 0–100 absolute scale where 100 represents saturation across all six components. A 79% mention rate cannot legitimately produce a 100 score under that construction, because the other five components would necessarily reduce the composite.

The v0.2 output should be treated as superseded. Any external reference to v0.2 numbers should be accompanied by a link to this methodology log.

### v0.3 — Path C, Steps 2 + corrected scoring (2026-04-29 evening)
- 6 prompts (added Comparison CEP) × 2 models (Google removed due to free-tier rate limiting) × 8 runs = 96 calls
- Brand registry: 19 brands (added Coda, Confluence, GitHub Projects, Workfront)
- Retry logic: up to 4 attempts per call, with provider-specified retry-after delays honored
- Methodology metadata stamped in every row (versioning, model versions, registry version)
- **Headline metric: Presence (raw mention rate, NOT normalized)**
- RankSOM, Primary-Rec, and Consistency displayed in output but **NOT blended into the headline score** — labeled as descriptive only, pending future AIAS component releases

---

## 4. Current Methodology (v0.3) — Detailed

### 4.1 Models
- OpenAI `gpt-5.4-mini`
- Anthropic `claude-sonnet-4-6`
- Google removed for v0.3 due to free-tier daily rate limits making complete runs infeasible. Will be reinstated in v0.4 once paid-tier billing is configured.

### 4.2 Prompts
Six prompts mapped to Category Entry Points (Romaniuk, Ehrenberg-Bass framework):
1. **FUNCTIONAL_WHY** — utility-driven recommendation request
2. **CONTEXTUAL_WHEN** — situational trigger
3. **CONSTRAINT_WITH** — domain constraint (engineering teams)
4. **IDENTITY_HOW_FEELING** — identity-loaded inquiry
5. **DISCOVERY** — emerging-tools probe
6. **COMPARISON** — head-to-head choice request (no brands named in prompt)

No brand names appear in any prompt. This prevents inflation of mention rates for any brand the prompt itself names.

### 4.3 Run Configuration
- Temperature: 0.7
- Runs per prompt per model: 8
- Total target calls per category run: 6 × 2 × 8 = 96
- Realized success rate v0.3: 96/96 (100%)

### 4.4 Brand Detection
**Primary path:** OpenAI `gpt-5.4-mini` with function calling. The extractor receives the AI response and is forced to return structured JSON with brand name, rank-position, sentiment, and is-primary-recommendation flag.

**Fallback path:** regex word-boundary matching against the brand registry's alias list. Used only when function calling fails (rare).

**Deduplication:** within a single response, each brand is recorded at most once, at its first appearance.

### 4.5 Brand Registry (v2)
19 brands across three tiers:
- **Incumbents (5):** Asana, Monday, Jira, Trello, Confluence
- **Mid-tier (8):** Notion, ClickUp, Smartsheet, Wrike, Airtable, Basecamp, Coda, Workfront
- **Challengers (6):** Linear, Height, Motion, Shortcut, Todoist, GitHub Projects

Brands deliberately excluded from v0.3:
- Slack, Figma, Miro, Loom — collaboration adjacencies, not PM tools
- GitHub (the platform), GitLab, Bitbucket — code hosting, not PM tools
- Microsoft Project, Microsoft Planner, Google Workspace — included only as ecosystem references in adjacent products

The registry is reviewed each version. Brands appearing repeatedly in the "Unknown Brands" output are evaluated for inclusion. Inclusion criteria: (a) credibly competes in PM software category, (b) appears in at least 5 mentions across measurement runs, (c) inclusion doesn't change the category boundary in a way that breaks comparability with prior versions.

### 4.6 Scoring (Presence Only)

Presence(brand) = (number of runs mentioning brand) / (total successful runs) × 100


Range: 0–100. Not normalized. A brand mentioned in every run scores 100; a brand mentioned in none scores 0.

Per-model Presence is computed identically with model-specific runs as the denominator.

**Spread = max(per-model presence) − min(per-model presence).** Reported as a transparency metric, not part of any composite.

### 4.7 Descriptive Companion Metrics (NOT blended into Presence)

Three additional metrics are computed and displayed alongside Presence for transparency, but are explicitly NOT part of the headline score:

**Rank-weighted Share of Model (RankSOM):**

```
RankSOM(brand) = sum across runs of (1 / rank_position) / total runs × 100
```

Where rank_position is the position the brand appears in within a single AI response. Rank 1 = full credit; rank 5 = 0.2 credit. This is a preliminary signal for AIAS Component #2 (Ranking).

**Primary Recommendation Rate:**

```
PrimaryRec(brand) = (runs where brand was flagged as primary recommendation) / total runs × 100
```

Preliminary signal for sentiment-adjacent positioning.

**Consistency:**

```
Consistency(brand) = max(0, (1 − (stdev / mean) of per-model presence) × 100)
```

A 0–100 score where 100 = identical presence across models, 0 = high variance. Preliminary signal for AIAS Component #3 (Consistency).

These metrics are visible in the leaderboard CSV but are not blended into the Presence score and are not part of any reported AIAS composite.

---

## 5. Decision Rule for Adding Components

The Presence-only methodology will run unchanged across Phase 1 (current category) and Phase 2 (additional categories). No new components will be added until all of the following conditions are met:

**Trigger conditions for adding any single AIAS component:**
1. Presence-only has run unchanged across at least 3 categories.
2. At least 4 weeks of time-series data exist showing that Presence rates are stable enough that genuine movement is detectable above noise.
3. An external benchmark is available against which the new component can be validated.
4. The new component must enable a specific decision that Presence alone does not.

If condition 4 cannot be answered for a candidate component, that component is not ready.

**Suggested order when components are added:**
1. **Consistency** — already computable from existing data; adds dispersion signal.
2. **Ranking (formal)** — required to defend strategic claims; framework's rank-sensitivity curves depend on it.
3. **Sentiment posture** — pre-empts the "you're conflating positive and negative" critique.
4. **Coverage** — per-CEP rolldown.
5. **Grounding** — last; requires source-level engineering.

The Identity Load Index (ILI) moderation specified in the framework requires cross-category data on at least 3 categories of varying ILI before it can meaningfully be applied. ILI integration is therefore deferred to Phase 2 conclusion at the earliest.

---

## 6. Limitations Acknowledged

Any report citing this methodology should also acknowledge these limitations:

- **Sample size.** v0.3 represents 96 successful API calls in one category. Confidence intervals on Presence rates are wide (approximately ±10 percentage points at 95% CI). Findings are descriptive, not inferential.
- **One category.** Generalization to other categories is not yet supported. Multiple categories are required before patterns can be claimed as framework-level.
- **Two models in v0.3.** Three models is the minimum target. Google was excluded from v0.3 due to operational constraints, not methodological choice. v0.4 will reinstate.
- **Model-version sensitivity.** AI model behavior changes when providers update underlying models. Every measurement is timestamped and model-version stamped. Longitudinal comparisons require the same model versions or explicit re-baselining.
- **Brand registry constraints.** The registry defines what is measured. Brands outside the registry are surfaced as "Unknown" but do not participate in scoring. This is an intentional methodological choice to preserve category integrity.
- **Construct validity not yet established.** Whether AIAS scores correlate with real-world brand consideration or sales is unproven. A validity study against external brand-tracking data is planned for Phase 3.
- **Single point in time.** All v0.3 data was collected on a single day. Time-series claims are not yet supportable.

---

## 7. Reproducibility

All measurement code, prompts, and brand registry are versioned alongside this document. To reproduce a report:

1. Clone the repository (or restore the timestamped snapshot)
2. Use the model versions specified in the version history
3. Use the prompt set version specified
4. Use the brand registry version specified
5. Run the documented number of attempts per prompt at the documented temperature

Note that AI model outputs are stochastic; exact reproduction of any specific response is not possible. Reproduction at the leaderboard level (within confidence intervals) is the methodological standard.

---

## 8. Citation

When citing this methodology, please reference both the version and the date:

> Gonzalez Castro, P. (2026). *AI Presence Index Methodology v0.3*. Third System.

---

*This document is updated with each methodology version. Errors discovered post-release are documented in the version history rather than silently corrected. Naming methodological errors is the strongest credibility signal a measurement organization can offer.*
