---
documentclass: article
geometry: margin=1in
fontsize: 11pt
mainfont: Carlito
header-includes:
  - \usepackage{setspace}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage{caption}
  - \captionsetup[figure]{font=small,labelfont={bf,it},textfont=it,justification=raggedright,singlelinecheck=false}
  - \usepackage{titlesec}
  - \titleformat{\section}{\Large\bfseries}{\thesection.}{0.5em}{}
  - \titleformat{\subsection}{\large\bfseries}{\thesubsection}{0.5em}{}
---

\begin{center}
\setlength{\parskip}{10.36pt}

\vspace{2em}

SSRN WORKING PAPER

\vspace{1em}

{\fontsize{16}{21.76}\selectfont\bfseries AI Presence Drift: A Longitudinal Re-Baseline of Five Brand Categories}

\textit{One-Week Stability Validates the AIAS Measurement Program, Sharpens Pattern 4, and Confirms Phantom-Brand Persistence}

Working Paper · Version 0.9 · Longitudinal Re-Baseline (Five Categories)

\vspace{2em}

Pablo Ulpiano González Castro

School of Visual Arts, MPS Branding Program, New York, NY \\
(primary academic affiliation)

Third System\textsuperscript{™} (research entity; data archive and methodology venue)

Correspondence: pablou@pablou.com · pablou.com

ORCID: https://orcid.org/0009-0003-8968-9990

\vspace{1em}

8 May 2026

\textit{Working paper. Not under peer review. Pre-registered.}

\end{center}

\newpage

# Abstract {-}

This paper reports a longitudinal re-baseline of the five categories first measured in the v0.6 cross-category baseline of the AIAS measurement program — project management software, premium running shoes, premium olive oil, premium facial skincare, and personal finance applications — at a second time point approximately seven days later. The study closes Phase 2 of the AIAS program by giving each baseline category a t₂ measurement and provides the data spine for Phase 3 construct-validity work. Six hypotheses with explicit numerical thresholds were committed to a pre-registration document locked at git commit f8cebbd (tag v0.9-prereg-locked) prior to any t₂ data collection. Methodology decisions — including the matched 2-model subset (claude-sonnet-4-6 and gpt-5.4-mini, the original v0.6 lineup) for longitudinal deltas, retroactive mode classification of v0.6 data, and registry freeze at v0.6's final state — were locked at git commit e6428a4 prior to the pre-registration.

The headline result is decisive. Five formal hypotheses were confirmed and the sixth landed at the predicted stability band. Per-brand drift across all 5 categories on the matched subset (n = 103 brand-level deltas) was small: 88.3 percent of brands within ±5 percentage points and 99.0 percent within ±10 percentage points (H1 confirmed). Top-three brands at t₁ remained in the top-five at t₂ in every category (H2 confirmed, 5 of 5). Variance-rank-order across the five categories at t₂ correlated with t₁ at Spearman ρ = 0.8, replicating Pattern 1 from v0.6 (H3 confirmed). The Mint phantom-brand stayed at 41.7 percent matched-subset Presence at t₂ versus 44.8 percent at t₁ — a −3.1 percentage-point delta within the predicted stability band, replicating the phantom-brand persistence mechanism from v0.7 (H4 stability, the predicted outcome). Pattern 4 discourse-language bias replicated under the strict reading: Spanish olive oil aggregate Presence at 11.5 percentage points fell below the 12.5-percentage-point threshold derived from the International Olive Council production share, and K-beauty aggregate Presence in skincare at 1.0 percentage point fell well below the 5-percentage-point threshold (H5 confirmed strict; partially confirmed under an inclusive reading that adds Graza, a US-headquartered Spanish-sourced brand). Per-brand cross-model spread between the two matched-subset models correlated between t₁ and t₂ at Pearson r ≥ 0.7 in every category (H6 confirmed, 5 of 5).

A meta-finding emerged from the H5 work: the v0.6 skincare registry contains a single K-beauty brand among thirty-one entries, mirroring inside the registry construction the same Anglo-discourse bias the test is designed to detect. The H5 strict-versus-inclusive sensitivity also sharpens Pattern 4 from v0.8: when Spanish-sourced English-marketed brands are included, the under-surfacing washes out, confirming that the mechanism operates at the level of discourse-language coverage rather than country of origin.

The combined result set is interpreted as a longitudinal validity argument for the AIAS measurement program. AI Presence behaves like a real underlying construct — drift is small, leaderboards are stable, structural variance patterns replicate, the phantom-brand persistence mechanism holds across waves, and cross-model relative behavior is preserved. The argument unblocks Phase 3 construct-validity work, which requires at least three categories at two time points and now has data for five.

# Keywords {-}

AI brand visibility; longitudinal validity; pre-registered measurement; brand presence; large language models; drift; phantom-brand persistence; discourse-language bias; AIAS

# JEL Classification {-}

M31 (Marketing) — primary; L86 (Information and Internet Services; Computer Software); C81 (Methodology for Collecting, Estimating, and Organizing Microeconomic Data); D83 (Search; Learning; Information and Knowledge; Communication; Belief; Unawareness)

# Paper status {-}

Working paper. Not under peer review. Pre-registered longitudinal re-baseline closing Phase 2 of the AIAS measurement program. Builds directly on the cross-category baseline reported in González Castro (2026), "AI Presence Measurement Across Consumer Categories" (SSRN ID 6720959). Replicates and sharpens the discourse-language bias mechanism reported in González Castro (2026), "A Designed-for-Test Measurement of Discourse-Language Bias in Large Language Model Brand Recommendations" (SSRN ID 6728000). Replicates the phantom-brand persistence mechanism reported in González Castro (2026), "A Designed-for-Test Measurement of Phantom-Brand Presence in Large Language Model Outputs" (SSRN ID 6721779). Companion empirical artifact to González Castro (2026), "AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval" (SSRN ID 6659000). Methodological reference: González Castro (2026), "AIAS Presence Measurement Protocol v1.1" (SSRN ID 6722319). Pre-registration document (PRE_REGISTRATION_v09_rebaseline_v1.0.md, locked at git commit f8cebbd, tag v0.9-prereg-locked) and underlying datasets released alongside this paper at osf.io/[id-pending]/.

\newpage

# 1. Introduction

The cross-category baseline reported as v0.6 of the AIAS measurement program (González Castro 2026, "AI Presence Measurement Across Consumer Categories") established a snapshot of brand visibility in large language model (LLM) outputs across five consumer categories at a single time point in late April 2026. The baseline produced six structural patterns — including discourse coherence as a driver of within-category variance (Pattern 1), incumbent-clustering with challenger-fragmentation (Pattern 2), discourse-language bias in cross-lingual categories (Pattern 4), and phantom-brand persistence in defunct or transformed brand cases (Pattern 6) — and a single time-point dataset across approximately one hundred registered brands. Two designed-for-test follow-up studies (v0.7 phantom-brand persistence; v0.8 discourse-language bias) confirmed two of the patterns at category-specific resolution but left open a question that no single-time-point measurement can answer: *does AI Presence behave like a real underlying construct, or like measurement noise?* Without longitudinal evidence, the v0.6 baseline patterns are observations whose stability is unknown, and the construct-validity work that the AIAS program targets in Phase 3 cannot be undertaken — Phase 3 requires at least three categories measured at two time points correlated against external consumer-tracking data.

The longitudinal re-baseline reported here addresses both gaps directly. The same five categories from v0.6 — project management software, premium running shoes, premium olive oil, premium facial skincare, and personal finance applications — were re-measured at a second time point approximately seven days later, against a frozen registry, with the same six pre-registered prompts anchored to Category Entry Points. The matched 2-model subset for the longitudinal claims comprises the original v0.6 model lineup (Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini); the t₂ measurement adds four parallel-baseline models (Anthropic Opus 4.7, OpenAI gpt-5.5, Google Gemini 2.5 Flash, xAI Grok 4.1 Fast) for cross-version completeness, but these are reported as parallel new baselines outside the longitudinal frame. The methodological choice preserves clean t₁/t₂ attribution: longitudinal deltas are computed only on the subset of models that were measured at t₁, so any divergence is attributable to AI behavior change rather than to model-set expansion.

Six hypotheses with explicit numerical thresholds were committed to a pre-registration document (PRE_REGISTRATION_v09_rebaseline_v1.0.md) locked at git commit f8cebbd (tag v0.9-prereg-locked) prior to any t₂ data collection (Nosek et al. 2018). The hypotheses isolated specific candidate properties of the LLM tier: brand-level drift noise floor (H1); top-of-leaderboard stability (H2); replication of the v0.6 within-category-variance ordering across categories (H3); phantom-brand persistence on Mint, the canonical phantom case from v0.7 (H4); replication of Pattern 4 discourse-language bias on Spanish olive oil and K-beauty skincare brands (H5); and cross-model relative-behavior stability between the two matched-subset models (H6). A seventh observation — mode-distribution stability after retroactive mode classification of v0.6 — was deferred to exploratory status because no prior calibration existed for what threshold counts as "meaningful shift" in mode share.

The headline result is decisive. Five formal hypotheses were confirmed and the sixth landed at the predicted stability band. Drift across the five categories on the matched subset was small (88.3 percent of brands within ±5 percentage points). Leaderboards were stable across all five categories. The variance-rank-order across categories preserved at Spearman ρ = 0.8. Mint persisted at 41.7 percent at t₂ versus 44.8 percent at t₁, within the predicted ±5-percentage-point stability band. Spanish olive oil under-surfacing and K-beauty under-representation in skincare both replicated. Cross-model relative behavior between Sonnet and gpt-5.4-mini correlated between t₁ and t₂ at Pearson r ≥ 0.7 in every category. The combined result set supports interpreting AI Presence as a real, structured property of the LLM tier rather than as the residue of measurement noise — and unblocks the Phase 3 construct-validity program.

Two findings worth highlighting in the introduction emerged outside the formal pre-registration. First, the H5 strict-versus-inclusive sensitivity sharpens Pattern 4. When the Spanish olive oil cohort is restricted to brands that present themselves to consumers as Spanish-discourse-coverage (Castillo de Canena, Núñez de Prado), the aggregate Presence is 11.5 percent and falls below the 12.5-percent threshold derived from Spain's roughly 50-percent share of global olive oil production; H5 confirms. When Graza (a US-headquartered, Spanish-sourced, English-marketed D2C brand that surfaces at approximately 14 percent in the matched subset) is added to the cohort, the aggregate rises to 14.2 percent and the threshold is breached; H5 partially confirms. The 2.7-percentage-point swing is entirely Graza. The interpretation is that Pattern 4 operates at the level of *discourse language* — the language in which a brand is marketed, indexed in retailer feeds, and discussed in food media — rather than at the level of *country of origin*. Brands that source Spanish but market English are absorbed into the English-language discourse infrastructure that LLMs draw on; the under-surfacing observed in v0.6 and v0.8 specifically reflects under-coverage in the discourse, not under-production in the supply chain. The framing is a tighter version of Pattern 4 than v0.6 stated.

Second, the K-beauty registry coverage is itself a finding. The v0.6 skincare registry contains thirty-one brands, of which exactly one (Beauty of Joseon) is a Korean-headquartered, Korean-discourse-marketed K-beauty brand. The under-representation mirrors inside the registry-construction process the same Anglo-discourse bias the test is designed to detect: an analyst constructing a "premium skincare registry" by surveying English-language category coverage will tend to compose a registry that itself under-represents non-English-discourse cohorts. The observation is reported as a methodological observation in §6; it does not affect the H5 K-beauty score (which uses Beauty of Joseon's measured Presence regardless of registry coverage) but constrains how confidently we can interpret the K-beauty under-surfacing as a measurement of LLM behavior versus a measurement of registry construction.

The remainder of the paper is organized as follows. Section 2 describes the pre-registered method, including the matched-subset framing for the longitudinal claim, registry freeze with documented metadata anomalies, retroactive mode classification of v0.6, and pre-registration. Section 3 reports the six findings in narrative form. Section 4 reports pre-registered hypothesis outcomes in tabular form. Section 5 develops the longitudinal validity argument: drift, leaderboard stability, structural-pattern replication, and the phantom-brand persistence and discourse-language bias replications interpreted together. Section 6 addresses limitations including the single-pair longitudinal subset, the seven-day inter-measurement interval, and the registry-construction reflexivity exposed by the K-beauty observation. Section 7 outlines Phase 3 work: construct-validity correlation against external consumer-tracking data, additional longitudinal time points, and category expansion to cross-lingual categories beyond the v0.6 baseline.

# 2. Method

The measurement followed the AIAS Presence Measurement Protocol v1.1 (González Castro 2026), with the longitudinal-re-baseline addendum (matched-subset framing for the longitudinal claim; parallel new-baseline framing for the four added models) developed and locked in the v0.9 methodology decision note (docs/v09_DECISION_NOTE.md) at git commit e6428a4 prior to the pre-registration.

## 2.1 Longitudinal Frame and Matched Subset

The v0.6 measurement was conducted with two models per category: Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini. The Phase 2 measurement program (v0.7 phantom-brand and v0.8 discourse-language) expanded the lineup to six models across four labs. The v0.9 measurement runs the full Phase 2 lineup (six models) at t₂, but for the longitudinal claim — the t₁→t₂ comparison that constitutes the substance of H1 through H6 — only the matched two-model subset (Sonnet 4.6 and gpt-5.4-mini) is used. The four additional models (Anthropic Opus 4.7, OpenAI gpt-5.5, Google Gemini 2.5 Flash, xAI Grok 4.1 Fast) report as parallel new baselines: a first measurement for each at t₂, providing the t₁ reference for that model's own future longitudinal work. The framing preserves clean t₁/t₂ attribution: any t₁→t₂ delta on the matched subset is attributable to AI behavior change between waves, not to model-set expansion. The framing is documented in the v0.9 methodology decision note (Decision #1).

## 2.2 Registry and Prompt Freeze

The registry and prompt set were frozen at v0.6's final state per Decision #3 of the methodology note. The registries used at t₂ are the per-category JSON files committed to the repository as of the pre-Phase-2 reorganization (git commit 179b3d7), which split the original consolidated `brands.json` into per-category `registries/brands_<category>.json` files. The reorganization was structural — it added the per-category file layout but preserved the underlying brand lists and prompt text — and is treated for the purposes of the registry-freeze decision as a schema-only change rather than a content revision. Inspection of the v0.6 measurement CSVs confirmed that the brand lists and prompt text in the t₁ measurements match the brand lists and prompt text loaded at t₂ in all five categories.

One documented metadata anomaly affects the personal finance v0.6 measurement. The brand_registry_version field on the personal finance v0.6 rows reads `v2-skincare`, inherited from a module-level constant in the pre-Phase-2 runner that was not reset between the skincare and finance sessions on 30 April 2026 (skincare ran at 17:51 UTC; finance ran at 18:16 UTC, twenty-five minutes later). Inspection of the v0.6 finance raw responses confirmed that the prompts that fired were the finance prompts and the brand mentions extracted are personal finance brands; the metadata stamp is a cosmetic carryover, not a measurement defect. The anomaly is disclosed here for transparency and does not affect any H1 through H6 score.

## 2.3 Prompt Set

The same six prompts used at t₁ were used at t₂, anchored to Category Entry Points per AIAS Protocol §3.1: FUNCTIONAL (p1), CONTEXTUAL (p2), CONSTRAINT (p3), IDENTITY (p4), DISCOVERY (p5), COMPARISON (p6). Per-category prompt text was re-used verbatim from v0.6.

## 2.4 Model Lineup at t₂

Six frontier models from four labs were measured at t₂. Two of the six (Anthropic Sonnet 4.6 and OpenAI gpt-5.4-mini) are the matched-subset models — present in v0.6 and used for the longitudinal claim. Four (Anthropic Opus 4.7, OpenAI gpt-5.5, Google Gemini 2.5 Flash, xAI Grok 4.1 Fast) are parallel new baselines. The Phase 2 lineup matches v0.7 and v0.8, enabling cross-version comparison of the parallel-baseline measurements with the same model lineup observed in those studies.

## 2.5 Measurement Volume and Failed-Call Recovery

Each (prompt, model, run) tuple was measured once at temperature 0.7 where supported. The target measurement volume per category at t₂ is 6 prompts × 6 models × 8 runs = 288 cells, totalling 1,440 cells across the five categories. The first-pass run on project management software produced 233 of 288 successful measurements (80.9 percent), driven by an OpenAI billing-quota ceiling that was reached partway through the run. After the billing ceiling was raised, the remaining four categories' first-pass runs produced 287 of 288 (running shoes), 287 of 288 (olive oil), 288 of 288 (skincare), and 282 of 288 (personal finance) — totalling 96.5 percent first-pass completion across the four categories that ran after the billing fix. Failed cells were recovered through the pre-registered failed-call recovery cycle (AIAS Protocol §4.3) per provider, yielding 1,440 of 1,440 successful measurements (100.0 percent) after recovery. One observation worth flagging: Google Gemini 2.5 Flash retries during the project management software recovery pass averaged 322 seconds per call (versus approximately 8 seconds during the original run), with all eight retried cells eventually returning successfully. The slow-response episode is bounded to that recovery pass and does not affect the per-cell measurement; it is disclosed as a methodological observation.

## 2.6 Mode Classification, Retroactive at t₁

Per Decision #2 of the methodology note, the mode classifier developed during v0.7 and v0.8 was applied retroactively to the v0.6 raw measurements as well as forward to the v0.9 raw measurements, so that t₁ and t₂ datasets carry mode classifications under the same scheme. The classifier assigns each successful measurement to one of five modes: brand, mixed, component, authority, refusal. Cross-lab AI audits (twenty-five-row stratified samples per (category, wave) file) were generated for inter-rater agreement work; the audits are deposited but not analyzed for v0.9 hypothesis scoring, which uses the brand-surfacing macro unit (per AIAS Protocol §6.5 reframe convention) at which 96 percent agreement was established in v0.8. Mode-distribution stability between t₁ and t₂ is reported as exploratory observation in §3.7.

## 2.7 Pre-Registration

Six hypotheses with explicit numerical thresholds were locked in PRE_REGISTRATION_v09_rebaseline_v1.0.md at git commit f8cebbd, with tag v0.9-prereg-locked, prior to any t₂ data collection. Pre-registered methodological risks (the finance v2-skincare metadata stamp; possible undisclosed model updates between t₁ and t₂; rate-limit and API-failure handling; parallel-baseline failure as not contaminating the longitudinal claim) were documented at lock time. Hypotheses, predicted thresholds, and outcomes are reported in Table 1 (§4).

# 3. Results

## 3.1 Finding 1 — Drift across categories is small and tightly bounded.

Across all 103 brand-level deltas computed on the matched subset (the union of registered brands across the five categories, excluding any brand not in the v0.6 final-state registry), 88.3 percent of brands surfaced at t₂ within ±5 percentage points of their t₁ Presence, and 99.0 percent surfaced within ±10 percentage points. The H1 confirmation thresholds were ≥70 percent within ±5pp and ≥90 percent within ±10pp, both cleared with margin. The empirical noise floor of AI Presence measurement on a one-week interval, on the matched subset, is therefore approximately ±5 percentage points for the modal brand and approximately ±10 percentage points for ninety-nine of every hundred. Among the largest movers, no single brand exceeded ±20 percentage points; the distribution is concentrated near zero.

## 3.2 Finding 2 — Leaderboards are stable.

In each of the five categories, the top-three brands by matched-subset Presence at t₁ remained in the top-five at t₂. The result confirmed at 5 of 5 categories with no exceptions, well above the 5-of-5 threshold for the headline confirmation band. The leaderboard stability is the most directly category-management-relevant of the six findings: brand managers and category buyers tracking AI Presence as a leading indicator can rely on the top-of-leaderboard composition across at least the seven-day measurement interval.

## 3.3 Finding 3 — The v0.6 within-category variance ordering replicates.

The v0.6 baseline established that within-category variance on per-brand Presence is itself an ordered structural property — categories with higher discourse coherence produce tighter brand-level distributions, while categories with contested or fragmented discourse produce wider distributions. The v0.9 measurement preserves this ordering. The Spearman rank correlation of within-category variance between t₁ and t₂ across the five categories is ρ = 0.8, above the 0.7 threshold for confirmation and well above the 0.4 threshold for partial confirmation. The replication suggests that Pattern 1 captures a structural property of the categories' AI representation rather than an artifact of single-time-point sampling.

## 3.4 Finding 4 — Mint persists.

The Mint phantom-brand observation from v0.7 (the brand was a leading personal finance application until its operational shutdown in 2024) holds at t₂. Mint's matched-subset Presence in personal finance was 44.8 percent at t₁ and 41.7 percent at t₂, a delta of −3.1 percentage points within the predicted ±5-percentage-point stability band. The pre-registration explicitly named stability rather than decay as the predicted outcome under the corpus-aging hypothesis: one additional time point seven days later is not enough for a defunct brand to be displaced from the LLM corpus, particularly when the brand's prior dominance generated extensive English-language discourse that persists in both training data and continuing inferential context. The H4 finding is therefore a confirmation of the predicted-stability outcome rather than a failure to confirm a decay prediction. The phantom-brand persistence mechanism from v0.7 holds across the longitudinal interval.

## 3.5 Finding 5 — Pattern 4 replicates and sharpens.

The v0.6 baseline observed in two cross-lingual categories (premium olive oil and premium facial skincare) that brand presence rates appeared to track English-language marketing infrastructure rather than country of origin or production heritage; the observation was termed Pattern 4 (discourse-language bias). The v0.8 designed-for-test on premium kitchen knives (González Castro 2026, "Discourse-Language Bias") confirmed the mechanism in the kitchen-knives category. The v0.9 longitudinal re-baseline tests Pattern 4 replication on the original two cross-lingual categories at t₂ against the same threshold framing. The strict-reading H5 outcome confirms the pattern. Spanish olive oil aggregate Presence, restricted to the two registered brands that present themselves to consumers as Spanish-discourse-coverage (Castillo de Canena and Núñez de Prado), measured 11.5 percentage points — below the 12.5-percent threshold derived from Spain's approximately 50-percent share of global olive oil production. K-beauty aggregate Presence in skincare, comprising the single registered K-beauty brand (Beauty of Joseon), measured 1.0 percentage point — well below the 5-percent threshold.

A sensitivity check sharpens the mechanism. When Graza — a US-headquartered, Spanish-sourced, English-marketed D2C olive oil brand that surfaces at approximately 14 percent matched-subset Presence — is added to the Spanish cohort, the aggregate rises to 14.2 percentage points and breaches the 12.5-percent threshold. The 2.7-point swing is entirely Graza. The interpretation is that Pattern 4 operates at the level of discourse-language coverage (the language in which a brand is marketed, indexed in retailer feeds, and discussed in category media) rather than at the level of country of origin. A brand that sources its olives from Spain but markets to American consumers in English is absorbed into the English-language discourse infrastructure that LLMs draw on; the discourse-language bias persists at the brand-marketing-language tier even when the supply-chain country is Spanish.

## 3.6 Finding 6 — Cross-model relative behavior is stable.

For each of the five categories, the per-brand spread between Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini at t₂ correlated with the same-pair spread at t₁ at Pearson r ≥ 0.7. The result confirmed at 5 of 5 categories, above the 4-of-5 threshold for headline confirmation. The finding indicates that the cross-model differential — what each model emphasizes versus what its companion emphasizes within a category — is preserved across the seven-day interval. Divergent brand-level shifts between the two models would suggest model-specific behavior change; the observed stability instead suggests that whatever AI behavior changed between t₁ and t₂ affected both models in approximately parallel ways, or affected neither.

## 3.7 Exploratory: mode-distribution shifts.

After retroactive mode classification of v0.6 and forward classification of v0.9 (per Decision #2), the mode-share distributions on the matched subset were compared per category. The largest within-category mode shifts include: project management software (brand mode +7.3 percentage points, authority mode −4.1pp), olive oil (brand mode −8.3pp, mixed mode +5.3pp, component mode +5.2pp), and skincare (component mode −6.2pp, mixed mode +4.2pp). Personal finance and running shoes were comparatively stable on mode share. The mode-distribution observation is exploratory rather than pre-registered because no prior calibration existed for what threshold counts as "meaningful shift" in mode share at this stage of the program. The v0.9 distributions are reported as a calibration baseline for a future v0.10 pre-registered mode-stability hypothesis with thresholds derived from observed v0.9 noise floors.

# 4. Pre-Registration Outcomes

The eight pre-registered outcomes (six formal hypotheses plus the H5 sensitivity check plus the exploratory mode observation) are reported in Table 1.

\begin{center}
\textit{Table 1. v0.9 longitudinal re-baseline pre-registration outcomes.}
\end{center}

| Hyp. | Claim (matched subset, t₁→t₂) | Threshold | Outcome | Band |
|---|---|---|---|---|
| H1 | ≥70% within ±5pp; ≥90% within ±10pp | both | 88.3% within ±5pp; 99.0% within ±10pp | **CONFIRMED** |
| H2 | Top-3 at t₁ remain in top-5 at t₂, per category | 5 of 5 | 5 of 5 | **CONFIRMED** |
| H3 | Spearman ρ ≥ 0.7 on variance-rank-order | ρ ≥ 0.7 | ρ = 0.8 | **CONFIRMED** |
| H4 | Mint within ±5pp (stability predicted) | ±5pp | −3.1pp | **STABILITY (predicted)** |
| H5 (strict) | Spanish ≤12.5pp AND K-beauty ≤5pp | both | 11.5pp; 1.0pp | **CONFIRMED** |
| H5 (incl. Graza) | as H5 with Graza in Spanish cohort | both | 14.2pp; 1.0pp | PARTIALLY CONFIRMED |
| H6 | Pearson r ≥ 0.7 in ≥4/5 categories | ≥4 of 5 | 5 of 5 | **CONFIRMED** |
| Mode dist. | exploratory; no threshold | — | reported in §3.7 | EXPLORATORY |

The headline result — five formal hypotheses confirmed plus the sixth landing at the predicted stability band, with the H5 sensitivity producing a sharper version of Pattern 4 — is a clean longitudinal validity outcome for the AIAS measurement program.

# 5. Discussion: AI Presence as a Real Underlying Construct

The combined H1 through H6 result set supports a specific interpretive claim: AI Presence behaves like a real, structured property of the LLM tier rather than like measurement noise. The argument has four legs.

*First, drift is small.* H1 establishes that 88.3 percent of brand-level deltas across the five categories are within ±5 percentage points across a seven-day interval, on the matched subset. If AI Presence were a noisy observation of an unstructured underlying signal, the per-brand deltas would distribute more widely and more uniformly across the brand population. The observed concentration near zero is the empirical signature of a stable underlying quantity that the measurement is recovering with bounded noise.

*Second, leaderboards are stable.* H2 establishes that the top-three brands at t₁ remained in the top-five at t₂ in every category. A noise-dominated process would, with non-trivial probability, reorder leaderboards across an interval; the observed across-the-board stability indicates that the position of dominant brands within a category is not artefactual.

*Third, structural patterns replicate.* H3 establishes that the within-category variance ordering across the five categories — first observed in v0.6 as Pattern 1 — preserves between waves at Spearman ρ = 0.8. The replication moves Pattern 1 from a single-time-point observation to a confirmed structural property. The v0.6 baseline patterns are, at least for Pattern 1, not artefacts of the specific date on which the baseline measurement happened to fall.

*Fourth, established mechanisms hold.* H4 establishes that the phantom-brand persistence mechanism observed for Mint in v0.7 holds across the longitudinal interval; the brand stays at near-44-percent matched-subset Presence despite being operationally defunct since 2024. H5 establishes that the discourse-language bias mechanism observed in v0.6 and confirmed for kitchen knives in v0.8 holds at t₂ for olive oil and skincare. H6 establishes that cross-model relative behavior is preserved across the interval. Each of the three mechanisms has independent prior support; the fact that they jointly hold across a longitudinal interval rather than only at a snapshot is what longitudinal evidence contributes to the construct-validity argument.

The four legs together motivate interpretation of AI Presence as a measurable construct rather than as an instrument-and-occasion artifact. The interpretation is stronger than any single hypothesis taken in isolation; the multi-pattern joint replication is what changes the inferential ceiling.

Two findings beyond the formal hypothesis set deserve discussion. *The H5 strict-versus-inclusive sensitivity sharpens Pattern 4.* The v0.6 framing of Pattern 4 was that "brand presence rates track English-language marketing infrastructure rather than country of origin." The v0.9 H5 sensitivity makes the framing more precise: the bias operates at the level of discourse-language coverage — the language in which a brand is marketed, indexed in retailer feeds, and discussed in category media — and is not invariant to country of origin in the way a strict supply-chain test would assume. Graza is the diagnostic case: a brand whose olives come from Spain but whose marketing, retailer indexing, and discourse coverage are entirely English. Including Graza in the Spanish cohort breaches the H5 threshold; excluding Graza confirms the threshold. The brand-marketing-language tier is the binding variable. Pattern 4 is thereby tightened from a country-level claim to a brand-marketing-language claim — a distinction with downstream consequences for any policy or industry interpretation of the discourse-language-bias mechanism.

*The K-beauty registry coverage is itself a finding.* The v0.6 skincare registry contains thirty-one brands, of which exactly one (Beauty of Joseon) is a Korean-headquartered K-beauty brand discoursed primarily in Korean-language category media. The under-representation in the registry construction parallels the discourse-language bias the test is designed to detect. The implication is that the registry-construction process inherits, at the analyst tier, the same Anglo-discourse coverage gap that produces the LLM-tier discourse-language bias. The observation does not affect the H5 K-beauty score (which uses Beauty of Joseon's measured Presence regardless of registry coverage) but constrains how confidently the K-beauty under-surfacing can be interpreted. If a registry constructed with full K-beauty population coverage produced a different H5 K-beauty aggregate, the interpretation would shift; the v0.9 measurement cannot rule that out. The observation is therefore reported as a methodological reflexivity caveat: the test is partially measuring its own registry construction. The reflexivity is, however, internally consistent with the discourse-language bias hypothesis itself — it would be more surprising if registry construction were free of the bias the registry is designed to detect.

# 6. Limitations

Six caveats apply to the findings reported here.

*Single-pair longitudinal subset.* The longitudinal claim is computed on the matched two-model subset (Anthropic Claude Sonnet 4.6 and OpenAI gpt-5.4-mini) — the only models present at both t₁ and t₂. The four parallel-baseline models added at t₂ contribute parallel new baselines but cannot contribute to the longitudinal claim. The validity argument generalizes most directly to the matched-subset model behavior; whether the four added models would, in their own future longitudinal measurements, exhibit similar drift profiles is an open empirical question.

*Seven-day inter-measurement interval.* The t₁ to t₂ interval is approximately seven days (29–30 April 2026 to 7 May 2026). The interval is short enough that no major model release or training cutoff change is expected to fall within it, supporting the assumption that drift observed across the interval is incidental rather than structural. Longer intervals (one month, three months, twelve months) are required to characterize drift across model-pipeline transitions, and the v0.9 measurement does not address that timescale.

*Registry-construction reflexivity.* The K-beauty observation in §5 establishes that the registry-construction process inherits Anglo-discourse coverage bias. The reflexivity does not invalidate the H1 through H6 results — which are computed on the registered brand population whatever its construction — but constrains their generalization. Stronger generalization would require a registry constructed with full population coverage of all relevant lineages, which is feasible in some categories (skincare) but not in others (premium olive oil includes thousands of small producers whose enumeration would be infeasible).

*Construct validity remains open.* The longitudinal validity argument in §5 establishes that AI Presence behaves like a real LLM-tier construct. Whether AI Presence correlates with consumer awareness, purchase intent, or category share at the consumer-facing tier is the separate question the AIAS Phase 3 program will address. The v0.9 result unblocks Phase 3 (which requires three categories at two time points and now has data for five) but does not itself constitute construct-validity evidence at the consumer tier.

*Personal finance metadata anomaly.* The v0.6 personal finance measurement carries the brand_registry_version stamp `v2-skincare`, inherited from the prior session's module-level constant. The metadata is cosmetic; raw-response inspection confirms that the prompts and registry that fired at v0.6 were the personal finance prompts and registry. The anomaly is disclosed for transparency. If subsequent investigation reveals any subtle dependence on the registry-version stamp through the analysis pipeline, the personal finance H4 (Mint persistence) result would need re-examination; no such dependence has been identified.

*Mode-classification audits deferred.* Manual inter-rater agreement audits on the v0.9 mode-classified data have not been completed at the time of this paper's posting. The v0.8 audit established 96-percent strict agreement on the brand-surfacing macro unit (the unit at which H1 through H6 score) and 68-percent strict agreement on the underlying five-mode taxonomy. The v0.9 H1 through H6 results score against the macro unit and are therefore not dependent on the strict-mode-taxonomy agreement budget. The exploratory mode-distribution observation in §3.7 is more directly dependent on classifier reliability and is reported with that caveat in mind. Manual audits are scheduled as a methodology disclosure prior to v0.10.

# 7. Future Research

The Phase 3 program will address five priorities surfaced by the v0.9 findings.

*Construct-validity correlation.* The v0.9 result unblocks the Phase 3 construct-validity study by providing five categories at two time points. Candidate consumer-tier validators include search-volume data (Google Trends), retail-tracking data (Amazon Best Seller ranks; category-share trackers where available), DTC brand-tracking instruments, and survey-based brand-awareness measurements. The marketing-language-coverage framing predicts that consumer awareness should correlate with AI Presence after controlling for production volume and category prestige. The construct-validity work is the program's gate to v1.0 release.

*Longer-interval longitudinal measurements.* Drift across one-month, three-month, and twelve-month intervals — particularly across model-pipeline transitions or training-cutoff changes — would characterize the temporal stability of AI Presence at scales that bracket model retraining, brand-discourse evolution, and consumer-behavior cycles. The v0.9 seven-day interval establishes a noise floor; longer intervals would add structural drift on top of the noise floor and reveal which categories and brand-types are most temporally stable.

*Cross-lingual category expansion.* Premium tea and traditional spirits remain candidate categories for designed-for-test measurements of Pattern 4, both satisfying the four cross-lingual structural criteria stated in v0.8. The v0.9 H5 sharpening — Pattern 4 at the brand-marketing-language tier rather than country-of-origin — informs the design of future cross-lingual studies: the discourse-language coverage of each registered brand becomes a primary variable, with country of origin as a secondary controlled covariate.

*Registry-construction protocols for cross-lingual categories.* The K-beauty observation suggests a structural improvement to the AIAS registry-construction methodology for cross-lingual categories. A formal protocol for registry construction that explicitly probes for non-English-discourse coverage gaps (for example, through the requirement that any registry intended to measure Pattern 4 in a category include a stated population-share survey of non-English-discourse producers) would mitigate the reflexivity caveat in §5. The protocol revision is planned as part of AIAS Presence Measurement Protocol v1.2.

*Mode-stability hypothesis at v0.10.* The v0.9 exploratory mode-distribution observations establish a calibration baseline for what counts as ordinary inter-wave shift in mode share. A v0.10 pre-registration could include a formal mode-stability hypothesis with thresholds derived from observed v0.9 shifts (the largest observed within-category shift was approximately ±8 percentage points; a sensible v0.10 threshold might be ±10 percentage points). The mode-stability hypothesis would test whether category-level discourse mode is itself a stable structural property of categories or whether it shifts more readily than brand-presence rates.

# References {-}

Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the dangers of stochastic parrots: Can language models be too big? *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency*, 610–623.

Brown, T. B., Mann, B., Ryder, N., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33.

González Castro, P. U. (2026). AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval. *SSRN Working Paper*. https://ssrn.com/abstract=6659000

González Castro, P. U. (2026). AI Presence Measurement Across Consumer Categories: A Cross-Category Baseline of Brand Visibility in Large Language Model Outputs. *SSRN Working Paper*. https://ssrn.com/abstract=6720959

González Castro, P. U. (2026). A Designed-for-Test Measurement of Phantom-Brand Presence in Large Language Model Outputs: Pre-Registered Evidence from Bed Bath & Beyond, with Pier 1 as Structural Comparator. *SSRN Working Paper*. https://ssrn.com/abstract=6721779

González Castro, P. U. (2026). AIAS Presence Measurement Protocol v1.1. *SSRN Working Paper*. https://ssrn.com/abstract=6722319

González Castro, P. U. (2026). A Designed-for-Test Measurement of Discourse-Language Bias in Large Language Model Brand Recommendations: Pre-Registered Evidence from Premium Kitchen Knives, with Marketing-Language Coverage as the Candidate Mechanism. *SSRN Working Paper*. https://ssrn.com/abstract=6728000

Keller, K. L. (2013). *Strategic Brand Management: Building, Measuring, and Managing Brand Equity* (4th ed.). Pearson.

Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600–2606.

Romaniuk, J. (2023). *Better Brand Health: Measures and Metrics for a How Brands Grow World*. Oxford University Press.

Romaniuk, J., & Sharp, B. (2016). *How Brands Grow: Part 2 — Including Emerging Markets, Services, Durables, New and Luxury Brands*. Oxford University Press.

Sharp, B. (2010). *How Brands Grow: What Marketers Don't Know*. Oxford University Press.

# Declarations {-}

## Conflict of Interest {-}

The author serves as Director, Corporate Brand Creative and Governance at Samsung Electronics America. The research presented here is independent of Samsung Electronics America and does not constitute Samsung research. No Samsung Electronics America data, personnel, or commercial interests influenced the design, conduct, analysis, or reporting of this study. Samsung Electronics America did not review the manuscript prior to posting. The brand population evaluated in this study (the v0.6 cross-category baseline of project management software, premium running shoes, premium olive oil, premium facial skincare, and personal finance applications) does not include Samsung product lines.

## Funding {-}

Self-funded. No external funding sources contributed to this research.

## Data Availability {-}

Underlying datasets, the locked pre-registration document (PRE_REGISTRATION_v09_rebaseline_v1.0.md, locked at git commit f8cebbd, tag v0.9-prereg-locked, lock date 6 May 2026 prior to t₂ data collection), the methodology decision note (docs/v09_DECISION_NOTE.md, locked at git commit e6428a4 prior to the pre-registration), the per-category registry files (frozen at v0.6's final state), the canonical scoring tables, the auxiliary unknowns classification, the cross-lab AI audit samples, and the build-pipeline source code are deposited in an Open Science Framework project at https://osf.io/[id-pending]/. The deposit contains row-level CSV outputs throughout — the v0.9 measurement was conducted within a git-tracked repository from methodology lock through publication, and no provenance gaps obtain. The OSF MANIFEST.md documents the file inventory, the lineage between raw measurements and derived analyses, and the cryptographic git-commit anchors for the methodology decision note, the locked pre-registration, and the published scoring tables.

# Author Information {-}

Pablo Ulpiano González Castro is faculty in the MPS Branding Program at the School of Visual Arts, New York, where he teaches Brand Transformation through Human-Centered Methodologies. He maintains Third System™ (research entity; data archive and methodology venue) as the publication venue for the AIAS measurement program. Correspondence: pablou@pablou.com · pablou.com.
