# AIAS Presence Measurement Protocol

**Author:** Pablo Ulpiano Gonzalez Castro
**Affiliation:** Third System (Principal Researcher); Faculty, MPS Branding Program, School of Visual Arts
**Version:** 1.0 (final draft, May 2026)
**Status:** Working document. The canonical reference for how AIAS Presence measurements are produced.

---

## Reading guide

Sections without flags are confirmed against source files (`run_aias_v2.py`, `extractor.py`, `brands.json` and `prompts.json` snapshots in iCloud, and the v0.6 enriched CSVs).

`[VERIFY: ...]` marks claims that should be double-checked against your local files before publication. `[FILL: ...]` marks the small remaining set of operational decisions for Pablo to make (release date, GitHub URL, retention policy, refusal-handling policy).

---

## What this document is

The protocol for measuring **AI Presence** for a brand within a category. AI Presence is the first of six components in the broader AI Availability Score (AIAS) framework. The other five — Ranking, Consistency, Coverage, Grounding, and Sentiment — are scoped for Phase 4 release contingent on Phase 3 construct-validity findings; Consistency is computable from existing data and is targeted for first release, Ranking second, the others as cross-category data permits. The Tri-System Brand Growth paper (Gonzalez Castro 2026, JBM) defines the full framework; this protocol documents the measurement of its first operational component.

This document is separate from any specific report. Reports cite this document as their methodological reference; this document does not change between reports unless the protocol itself is revised.

The structure is intended to double as the spine of a forthcoming methodology paper ("Measuring AI Availability: Methodological Notes from the AIAS Protocol").

---

## 1. Scope and definitions

### 1.1 What AI Presence measures

AI Presence is the rate at which a brand surfaces in AI-mediated responses to category-relevant prompts, measured across a fixed prompt set and a fixed model set. It is reported on an absolute 0–100 scale as the raw mention rate, without normalization. It measures one specific surface — what a consumer encounters when they query an AI model about a category — not brand awareness, brand value, or market share.

### 1.2 What it does not measure

AI Presence is not a proxy for brand health, marketing ROI, or consumer consideration. The correlation between AI Presence and traditional brand metrics is **inconsistent across categories** — sometimes weak, sometimes inverse (see §8). Treating AI Presence as a substitute for traditional brand measurement is a category error. **Phase 3** is the construct-validity study that will determine whether AI Presence functions as a leading indicator of consumer behavior or a measurement of AI behavior in isolation. Both outcomes are scientifically useful; until Phase 3 completes, AI Presence is a measurement of the AI tier itself.

### 1.3 Key terms

- **Category Entry Point (CEP)** — a cognitive frame a consumer brings to a category query (Romaniuk, building on Sharp/Ehrenberg-Bass). The framework operationalizes CEPs as prompt modes (§3).
- **Category** — the unit of measurement. A bounded space of consumer choice. v0.6 categories: project management software, running shoes, premium olive oil, premium facial skincare, personal finance applications.
- **Brand** — a producer named within a category. Brands are scoped via a curated category-specific registry (§2.2).
- **Prompt mode** — one of six CEP-anchored framings: `FUNCTIONAL_WHY`, `CONTEXTUAL_WHEN`, `CONSTRAINT_WITH`, `IDENTITY_HOW_FEELING`, `DISCOVERY`, `COMPARISON`. CEP keys are stored in ALL CAPS in v0.6 enriched data. See §3.
- **Mention** — a discrete reference to a brand within a model response, extracted via structured-output (function-calling) classification (§5.1). Mentions are counted regardless of sentiment polarity; a negative mention ("X is not recommended") still counts toward Presence and is captured separately in the sentiment field.
- **Presence** — the rate (0–100%) at which a brand surfaces across the fixed prompt set within a category.
- **Three modes of AI response** — a foundational distinction (brand mode / component mode / authority mode) that conditions how Presence should be read. See §3.4.

---

## 2. Category and brand selection

### 2.1 Category inclusion criteria

A category is suitable for AIAS Presence measurement when:

1. A meaningful share of consumers consult AI before deciding what to buy.
2. The category has a clear bounded space — competing alternatives are recognizable as such.
3. There is enough public discourse that AI models have training material to draw on.

Categories run to date (v0.6, late April 2026): project management software (inaugural, B2B mature with high AI delegation), running shoes (consumer durables, higher identity load), premium olive oil (English-discourse-dominated globally fragmented production), premium facial skincare (very coherent editorial consensus dominated by dermatology), personal finance applications (regulatory salience, fragmented discourse, recent market disruption).

The v0.6 categories were chosen sequentially to span the broadest range of properties the framework claims to apply across: identity load, buyer type, domain, discourse coherence, production geography, and regulatory salience.

### 2.2 Brand registry construction

Each category measurement uses a curated brand registry organized in three tiers: **incumbents**, **mid-tier**, **challengers**. Each registry entry has a `canonical` name and an `aliases` list capturing how the AI may surface the brand in conversational responses.

Registry construction principles:

- Top brands by market share within the category
- Brands surfaced by editorial discourse (publication audit)
- Brands surfaced by exploratory AI runs that exceed an unknown-mention threshold (drives §2.4 revision)
- Manual additions for boundary-condition testing (§2.3)
- Aliases are **intentionally narrow** to keep false positives rare; the structured-output extractor (§5.1) handles contextual disambiguation for ambiguous tokens (e.g., "On" the running brand, where the bare token "on" is excluded from the alias list to avoid false-positives on the preposition).

Registry sizes from v0.6 (verified from `brands.json` snapshots in iCloud backups, except where noted):

- Project management software: **19 brands** (post-revision; pre-revision was 15 brands; expansion added Confluence, Coda, Workfront, GitHub Projects)
- Running shoes: **17 brands**
- Premium olive oil: **20 brands** (post-revision; pre-revision was 16 brands; expansion added Cobram Estate, Manni, McEvoy Ranch, Colonna)
- Premium facial skincare: **31 brands claimed in narrative; 24 surfaced in measurements.** `[VERIFY: source brands.json for skincare not preserved in iCloud snapshots; 24 distinct brands appeared at least once across the 86 measurements. The 7-brand gap may represent registry entries that scored zero mentions, or may reflect an over-count in the v0.5 narrative. Recovery options: (a) check Time Machine for an older brands.json from 30 April afternoon; (b) accept the 24-brand actually-surfaced list as canonical and note the discrepancy.]`
- Personal finance applications: **16 brands**

### 2.3 Boundary-condition additions

When a category is being used to test a specific hypothesis, additional brands are added specifically to expose that boundary. In v0.6:

- **Olive oil**: Spanish brands (Goya, Castillo de Canena, Núñez de Prado) included to test discourse-language bias against a country producing ~45% of global supply.
- **Skincare**: Beauty of Joseon (and possibly other K-beauty brands) included to test K-beauty representation in a category where Korean cosmetics have substantial English-language editorial coverage. **Note:** Beauty of Joseon, Sulwhasoo, and AmorePacific did not surface in any measurement — their absence is consistent with the Pattern 4 finding (discourse-language bias against non-English-marketed brands), but cannot be verified as registry entries that scored zero vs registry entries that never existed.

These test brands surface findings that contributed to Pattern 4 (discourse-language bias).

### 2.4 Registry revision protocol

When a first run of a category surfaces brands in the unknown-mentions list at a level that affects the leaderboard, the registry is expanded and the category is re-measured. The unknown-mentions list is the operational diagnostic — brands appearing with high frequency as unknowns are almost always real omissions, not noise. v0.6 examples:

- **Olive oil**: first run surfaced Cobram Estate as the most-mentioned unknown brand. Registry expanded from 16 to 20 brands. Confirmed by two separate `brands_registry_version` tags in the CSVs (`v2-oliveoil` and `v2-oliveoil-rev1`, dated 30 April 2026 morning).
- **Skincare**: first run surfaced La Roche-Posay, Vanicream, and additional dermatologist-recommended drugstore brands. Registry expanded.
- **PM software**: first run (15-brand registry, 29 April 2026 morning) surfaced Confluence, Coda, Workfront, and GitHub Projects as unknowns. Registry expanded to 19 brands by 29 April afternoon.

Published data comes from post-revision runs. Earlier runs are preserved in the methodology log for traceability. Registry expansion is now a standard practice across measurement cycles.

The registry-revision feedback loop is itself a methodological finding: the unknown-mentions list functions as a high-signal feedback loop for registry quality, and registry construction is the methodological choice with the most direct effect on which brands appear in measurements (§8.6).

---

## 3. Prompt design

### 3.1 The six CEP-anchored prompts

Each category is measured across **six prompts**, each anchored to a Category Entry Point. CEPs are operationalized as question-frames; the suffix encodes the pragmatic anchor. CEP names use ALL CAPS keys in v0.6 enriched data:

1. **`FUNCTIONAL_WHY`** — what's the best brand for the category's primary functional purpose? Generic utility framing.
2. **`CONTEXTUAL_WHEN`** — what's the best brand for a specific use context?
3. **`CONSTRAINT_WITH`** — what works given a specific constraint?
4. **`IDENTITY_HOW_FEELING`** — what brands does a reference group use/recommend? Activates editorial-consensus framing.
5. **`DISCOVERY`** — what are emerging or lesser-known options? Activates novelty framing.
6. **`COMPARISON`** — compare leading options and recommend one. Activates ranking framing.

The full prompt sets per category appear in **Appendix A**. Verbatim text comes from `prompts.json` snapshots in iCloud (modification dates 29–30 April 2026 corresponding to each category's run). Skincare prompts (Appendix A.4) are reconstructed from response evidence; the source `prompts.json` was overwritten before any backup snapshot captured it.

### 3.2 Prompt count per category

Six prompts × eight runs × two models = **96 successful measurements per category target**. Eight runs per prompt are used to estimate within-prompt variance and to produce stable mention-rate estimates. This sample size produces approximately **10-percentage-point confidence bands** around individual brand Presence scores (§5.4).

In v0.6, three of the five categories met the 96-measurement target. Two categories had reduced counts due to API errors or model refusals during collection (see §3.3).

### 3.3 Prompt invariance and successful-run requirements

The same six prompts are used across all eight runs and both models for a category. Across categories the prompts are paraphrased to fit the domain but the CEP anchoring is constant. Prompt-design changes constitute a protocol revision and must be versioned. Within-version paraphrasing for category fit is permitted; cross-mode bleed (a Discovery-framed prompt that the model interprets as Comparison) is a documented failure mode (§6.3) — though, importantly, sometimes a "diffuse" response is itself a structural finding rather than a prompt failure (skincare's Discovery prompt is the canonical example, see §6.3).

**Successful-run counts in v0.6 (per CEP, summed across both models):**

| Category | FUNCTIONAL | CONTEXTUAL | CONSTRAINT | IDENTITY | DISCOVERY | COMPARISON | Total |
|---|---|---|---|---|---|---|---|
| PM software | 16 | 16 | 16 | 16 | 16 | 16 | 96 |
| Running shoes | 16 | 16 | 16 | 16 | 16 | 16 | 96 |
| Personal finance | 16 | 16 | 16 | 16 | 16 | 16 | 96 |
| Premium olive oil | 8 | 13 | 16 | 16 | 8 | 14 | 75 |
| Premium facial skincare | 16 | 15 | 16 | 15 | 8 | 16 | 86 |

The reduced counts in olive oil and skincare widen confidence bands on those specific cells but do not affect the cross-category patterns reported in v0.6, because patterns are large relative to the band. Cells with fewer than 12 successful runs are flagged in published leaderboards. This asymmetry is a documented data-collection artifact, not a protocol revision.

### 3.4 The three modes of AI response

A foundational distinction that conditions how Presence is read. Across all v0.6 categories, AI responses to category prompts fall into three structurally different modes, and which mode the AI engages depends on the framing of the question rather than the structure of the category:

- **Brand mode** — the AI names brands within the category. This is what most of the report measures. Example: CeraVe at 100% in skincare's Identity prompt.
- **Component mode** — the AI names ingredients, materials, or product properties instead of brands. Example: skincare's Contextual prompt about fine lines in late thirties produced component mode 95% of the time, with the AI naming SPF 30+, retinol, vitamin C, niacinamide. Olive oil's Functional prompt also produced component mode (62%) — "extra virgin olive oil," "single-origin," "PDO/PGI" categories rather than brands.
- **Authority mode** — the AI names publications, communities, retailers, or competitions instead of brands. Example: skincare's Discovery prompt named exclusively *Allure*, *Byrdie*, r/SkincareAddiction, *WWD Beauty*, *Vogue*, Sephora, Ulta. Olive oil's Discovery prompt named *Olive Oil Times*, NYIOOC, *Flos Olei*, *Bon Appétit*, *Saveur*, Zingerman's.

A leaderboard cell with zero brand mentions does not necessarily indicate brand absence — it can indicate the prompt activated a different mode. Component mode and authority mode are not measurement failures; they are the AI engaging the question on a different layer.

The authority-mode finding produced unexpected secondary evidence for Pattern 4 (discourse-language bias): every publication named in v0.6 authority-mode responses across affected categories was English-language. The brand-mention bias is downstream of an authority-recognition bias.

Phase 2 will introduce a mode classifier as a pre-step in measurement, allowing each prompt's response to be scored on which mode it activated, with brand-mode Presence reported alongside component-mode and authority-mode activation rates. Existing v0.6 Presence scores remain valid as **brand-mode-conditional** measurements.

---

## 4. Model selection and execution

### 4.1 Models in scope (v0.6)

- **OpenAI**: `gpt-5.4-mini` (model string captured per-row in CSV `model_version` column)
- **Anthropic**: `claude-sonnet-4-6` (model string captured per-row in CSV `model_version` column)

**Run dates (v0.6):** April 29–30, 2026, across seven separate run sessions. Per-run timestamps are captured in dataset filenames (`presence_index_v0.3_<YYYYMMDD>_<HHMMSS>.csv`).

`[VERIFY: model versions captured at the string level (e.g., "gpt-5.4-mini") but not at the build/snapshot level. Both providers update model behavior under the same string identifier without explicit version bumps. If exact build IDs are needed for reproducibility, future runs should capture API response metadata (`response.id`, `system_fingerprint` for OpenAI, `response.model` for Anthropic) into a dedicated CSV column.]`

### 4.2 Model exclusion: Google Gemini

Gemini was included in the original measurement design and has been **excluded from v0.3, v0.4, and v0.6 results**. The original v0.1/v0.2 exclusion was due to free-tier rate limits during the study window; the v0.3/v0.4/v0.6 exclusion was due to a Workspace-domain access restriction. Gemini will be reinstated when access clears (Phase 2). Cross-model variance reported in v0.6 is therefore a **lower bound**; introducing a third model historically widens the range, and the variance findings (Pattern 1) would likely strengthen.

A `call_google()` function exists in `run_aias_v2.py` and remains uncalled in v0.6; the measurement pipeline is ready to re-include Gemini once access is restored.

### 4.3 Run conditions

Verified from `run_aias_v2.py`:

- **Authentication mode**: API direct via `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` environment variables (loaded via `python-dotenv`).
- **Browsing/search tools**: disabled. Models respond from training corpus only — this is structurally important for Pattern 6 (phantom brands), which would not surface if browsing were enabled.
- **Temperature**: `0.7` across all runs (constant `TEMPERATURE = 0.7` in `run_aias_v2.py`).
- **System prompt for measurement runs**: **none.** Measurement runs are unscaffolded. The OpenAI and Anthropic call functions pass only `messages: [{"role": "user", "content": prompt_text}]` with no system role. This is intentional — the goal is to measure default model behavior, not behavior under specific instructions.
- **Repetition**: 8 runs per prompt per model (`RUNS_PER_PROMPT = 8`).
- **Date of run**: captured per-prompt in CSV `timestamp` column (ISO 8601, second-precision). v0.6 measurements were conducted April 29–30, 2026, with each category measured on a single day.
- **API parameters**:
  - OpenAI: `temperature=0.7`. All other parameters at SDK defaults (`max_tokens` not capped, `top_p`, `frequency_penalty`, `presence_penalty` at API defaults).
  - Anthropic: `temperature=0.7`, `max_tokens=1024`. All other parameters at SDK defaults.
- **Retry logic**: rate-limit and transient errors are retried via `retry_helper.retry_call()`, which returns `(result, status, attempts)`. Only `status == "ok"` calls enter the dataset. Run summary reports counts of `ok / rate_limit_final / transient_final / hard_error`.

### 4.4 Capturing responses

Full response text is captured and stored in `results_v2_<timestamp>.csv`. No interpretation at run-time. Enriched outputs (`results_enriched_<timestamp>.csv`) add structured-output extraction (§5.1) plus rank, sentiment, and primary-recommendation columns. Aggregated leaderboards are written to `presence_index_v0.3_<timestamp>.csv` (the public artifact).

CSV column convention (v0.6 enriched data, 20 columns):

```
timestamp, methodology_version, prompt_set_version, brand_registry_version,
prompt_id, cep, model, model_version, temperature, run_idx,
call_status, attempts, elapsed_sec, raw_response,
brands_canonical, brands_unknown, brands_ranked,
primary_recommendation, sentiment_summary, extraction_method
```

`brands_canonical` is pipe-separated (`Asana|Jira|Linear`); `brands_ranked` is `name@rank` format (`Asana@1|Jira@2|Linear@3`); `sentiment_summary` is `pos:N|neu:N|neg:N` counts.

Raw response text is retained on Third System infrastructure for replay and audit. `[FILL: confirm retention period and whether raw responses are made available alongside the public `presence_index_v0.3_*.csv` files, available on request, or retained internally only.]`

---

## 5. Scoring rules

### 5.1 Mention extraction

Brand mentions are extracted via **two-tier extraction**, defined in `extractor.py`:

1. **Primary**: OpenAI `gpt-5.4-mini` function-calling at `temperature=0` with a structured-output schema (`record_brand_mentions`). The extractor receives the AI's raw response and returns a JSON list of brand mentions in order, with per-mention fields:
   - `name` (string, as the AI named it)
   - `rank` (integer position within the response)
   - `sentiment` (enum: `positive | neutral | negative`)
   - `is_primary_recommendation` (boolean)
2. **Fallback**: regex word-boundary alias matching (the original v0.1 method), used when function calling fails. Triggered automatically when an exception is raised by the function-calling primary path.

**Canonical mapping logic** (in `map_to_canonical()`):
1. Exact match on `canonical` name (case-insensitive)
2. Exact match on any alias (case-insensitive)
3. Substring match: alias contained in extracted name, or extracted name contained in alias

The substring fallback is the reason aliases are intentionally narrow (§2.2) — it explains why "On" the running brand has `"on"` excluded from its alias list to avoid false-positives.

Within a single response, mentions are deduplicated by canonical brand (a response naming "Shortcut" twice counts as one mention of Shortcut). The extraction system prompt instructs: *"List every brand mentioned in the order they appear. Do not invent brands. If a brand appears multiple times, record it only at its first appearance."*

**Negation policy.** Mentions are counted regardless of sentiment polarity. A response saying "Mint is no longer recommended" still counts as a Mint mention; the `sentiment` field captures the polarity (`negative` in this case), but Presence is sentiment-agnostic. A consequence is that **high Presence ≠ favorable AI treatment** — high Presence with a high `neg:` sentiment count is structurally distinct from high Presence with high `pos:`. Reports surface sentiment alongside Presence for affected brands.

**Known artifact.** The extraction system prompt is hardcoded: *"You extract brand mentions from text about project management software."* This PM-specific framing was used unchanged across all five v0.6 categories. The extractor still performed correctly (the brand registry is per-category and provides domain context via the canonical/alias list), but the system-prompt framing was never updated. This is documented here for transparency. Phase 2 will update the extractor to take a category parameter.

### 5.2 Mention weighting

Equal weighting across mentions. The headline metric is raw mention rate; per-prompt-mode and per-model breakdowns are reported alongside as descriptive metrics. Rank and sentiment fields are captured but not blended into the headline Presence score — they are descriptive columns for transparency and feed future AIAS components (Ranking, Sentiment).

Because Presence is sentiment-agnostic (§5.1), reports cite Presence alongside the `sentiment_summary` for any brand whose mentions trend net-negative.

### 5.3 Presence aggregation

The headline metric is the raw mention rate of each brand across all successful measurements in a category, on an absolute 0–100 scale, **without normalization**. Per-mode and per-model breakdowns are reported alongside.

For brand B in category C:

- For each measurement (prompt P × model M × run R), `mention_BCPMR = 1` if B is named in the response, else 0.
- `Presence_BC = mean(mention_BCPMR across all N(C) measurements) × 100`

where `N(C)` is the total successful measurements in category C (target: 96; actual ranges in v0.6 from 75 for olive oil to 96 for PM/Running/Finance — see §3.3).

Per-mode Presence: `Presence_BCM = mean(mention across N(C,M) measurements in mode M) × 100` (target N(C,M) = 16 = 8 runs × 2 models; actual varies per §3.3 table).

Per-model Presence: `Presence_BCmodel = mean(mention across N(C,model) measurements in that model) × 100` (target 48; actual varies per §3.3).

### 5.4 Variance reporting

- **Per-brand cross-model spread** (Pattern 1 unit of analysis): difference between OpenAI and Anthropic Presence for the same brand in the same category. Largest observed in v0.6: Rocket Money at 71 points (OpenAI 71%, Anthropic 0%) in personal finance.
- **Per-prompt-mode spread within a model** (Pattern 5 unit of analysis): how concentrated are responses on a small brand set within a single mode.
- **Consistency** (preview of Phase 4 component): `1 − coefficient_of_variation(Presence across models)`, displayed for transparency in v0.3+ leaderboards but explicitly marked as "future AIAS component, displayed for transparency."
- **Confidence bands**: the up-to-96-measurement sample produces approximately **10-percentage-point confidence bands** around individual brand Presence scores. Cross-category patterns reported in v0.6 survive that uncertainty because the patterns are large relative to the band. Smaller within-category margins should not be treated as decisive. Categories with reduced run counts (§3.3) carry wider bands.

---

## 6. Quality assurance

### 6.1 Pre-run checks

Verified in `run_aias_v2.py`:

- Brand registry sanity check (the script prints registry size at run start)
- Prompt count sanity check (the script prints `len(PROMPTS) × len(MODELS) × RUNS_PER_PROMPT = total calls` at run start)
- Methodology metadata stamp: `METHODOLOGY_VERSION`, `PROMPT_SET_VERSION`, `BRAND_REGISTRY_VERSION` printed and embedded in every CSV row
- Environment variable check: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`. Script prints `ERROR: missing <KEY>` and exits with code 1 if any are missing. Note Google key is currently checked but unused (§4.2).

`[FILL: any additional checks beyond what's in the script — manual prompt review against CEP coverage, dry run before full sweep, etc. These are operational practices that may not be encoded in the script.]`

### 6.2 Post-run checks

- Response completeness check (96 `ok` rows expected; investigate any `rate_limit_final` / `transient_final` / `hard_error`)
- Manual review of a sampled fraction of responses for parser accuracy
- Out-of-distribution model behavior flagged
- **Unknown-mentions list reviewed** against the brand registry to trigger §2.4 revision protocol if needed

### 6.3 Known failure modes

- **Prompt-mode bleed.** A Discovery-framed prompt that the model interprets as Comparison (or vice versa). Detected by comparing within-mode Presence distributions. The cleanest case in v0.6 is skincare's Discovery prompt, which produced no clear emerging tier — interpreted as a structural finding (skincare's editorial discourse has thoroughly worked through "emerging" so the cognitive slot is empty), not a prompt-bleed failure. **Distinguishing structural finding from prompt failure may require manual response inspection.**
- **Model refusals and rate limits.** Handled by `retry_helper.retry_call()`. The retry helper attempts each call multiple times and returns one of four statuses: `ok` (success, included in dataset), `rate_limit_final` (rate-limited after retries; excluded), `transient_final` (transient error after retries; excluded), `hard_error` (immediate failure; excluded). `[FILL: confirm retry count, backoff schedule, and whether refused responses are re-prompted with rephrased text or excluded entirely. The fact that olive oil and skincare have reduced run counts (§3.3) suggests either some responses were excluded as failures or runs were cut short — needs explicit policy.]` In v0.6 personal finance, zero hard errors and zero rate limits despite regulatory category — models answered with disclaimers but did engage.
- **Hallucinated brands.** Models occasionally surface brands that don't exist. Distinguished from real obscure brands via the registry expansion process: an unknown mention that turns out to be real triggers registry expansion (§2.4); an unknown mention that turns out to be a hallucination is logged. Disambiguation is manual review against external sources.
- **Phantom brands** (Pattern 6). The Mint case — brands that have shut down still surface in AI responses (Mint at 44% in v0.6 personal finance, 25 months after decommissioning). This is a **finding about the AI surface**, not a measurement failure. Reports flag known phantom-brand cases (§8.4).
- **Component-mode and authority-mode responses** (§3.4). Not failure modes; they are the AI engaging the question on a different layer. Phase 2 mode classifier will allow these to be reported as activation rates.
- **Per-model training-data freshness differences.** Anthropic and OpenAI lag actual market reality at different rates. The Mint v0.6 finding (Anthropic 65% vs OpenAI 23%) is the cleanest example: the 42-point spread is a per-model freshness signal, not a finding about Mint specifically.

---

## 7. Reproducibility

### 7.1 What is shared per measurement

For each AIAS Presence run, Third System publishes:

- The full prompt set for the category (Appendix A)
- Model versions and date of run
- The brand registry, post-revision (Appendix B)
- The leaderboard
- The underlying response dataset, named `presence_index_v0.3_<timestamp>.csv` in v0.6
- The build artifacts: report PDF and chart manifest

Raw API responses are preserved in `results_v2_<timestamp>.csv` files alongside enriched extraction. `[FILL: confirm whether raw responses (`results_v2_*.csv`) are part of the public release or available on request only. The aggregated `presence_index_v0.3_*.csv` files are public; the raw response captures may or may not be.]`

### 7.2 Methodology log

The full methodology log, including version history and the documented v0.2 calibration error, is published as `methodology.md v0.3`. **v1.0 supersedes this** with the present document plus a public reference paper.

### 7.3 Versioning

This protocol is versioned semantically. Breaking changes (e.g., a different prompt mode taxonomy, a different scoring rule) bump the major version. Within-version changes are clarifications and parameter updates, not methodological revisions.

---

## 8. Construct validity and limits

### 8.1 What AI Presence correlates with empirically

Based on v0.6 cross-category observations:

- **Strong correlation with editorial discourse coherence** (Pattern 1). Categories with fragmented discourse (personal finance, olive oil, PM software) produce wide cross-model variance; categories with converged discourse (skincare, running shoes) produce narrow variance.
- **Inconsistent correlation with consumer awareness / market share** (Pattern 3). In four of five v0.6 categories the divergence runs downward (large brands under-perform their market position in AI mediation: Nike at 6th in running shoes despite the category's largest marketing budget; Bertolli, Colavita, Goya combining for <8% in olive oil despite supermarket dominance; La Mer/SK-II/Lancôme/Estée Lauder/Clinique/Olay combining to ~6% Presence vs CeraVe at 67% alone). In personal finance the divergence inverts: YNAB (~1M paid subscribers) at 100% Presence across every prompt and model, Rocket Money (~5M users) at 71% / 0% by model.
- **Strong correlation with editorial consensus alignment to prompt framing** (Pattern 5). When the AI's training data carries strong consensus and the prompt's cognitive frame activates that consensus, AI responses are nearly deterministic.

The cleanest negative result: **AI Presence is not predicted by marketing budget or distribution scale** — Nike, Bertolli, La Mer all under-perform dramatically. This is a methodologically important paper claim — the construct AI Presence measures is not redundant with existing brand metrics.

### 8.2 What AI Presence does not yet predict

Whether AI Presence correlates with consumer consideration, purchase intent, or sales is currently unknown. **Phase 3** correlates AI Presence scores from at least three categories at two time points against external consumer-tracking data. A finding of strong correlation establishes AI Presence as a leading indicator with predictive value beyond the AI tier itself; weak correlation establishes it as a measurement of AI behavior alone. **Both outcomes are publishable, and both are useful.**

Until Phase 3 completes, AI Presence is treated as a leading indicator with unverified predictive value.

### 8.3 The discourse-language bias (Pattern 4 boundary)

The protocol currently runs **English-language prompts only**, executed against models trained predominantly on English-language corpora. v0.6 surfaced a preliminary signal (Pattern 4): brands whose primary marketing discourse is conducted in a language under-represented in AI training data are systematically under-surfaced — even when the cultural reference of the brand is well-known in English.

Test cases in v0.6:

- **Spanish olive oil**: Goya 0%, Castillo de Canena 23%, Núñez de Prado 5%, against a country producing ~45% of global supply. None placed in the top five.
- **Korean skincare**: Beauty of Joseon 0%, in a category where K-beauty has substantial English-language editorial coverage (*Allure*, *Vogue*, *Glamour*, *The Strategist*).
- **Tatcha** (Japanese aesthetic, San Francisco-founded, **English-language marketing**) at 18% Presence — sitting next to Beauty of Joseon's 0% suggests **marketing-discourse language**, not cultural reference, is the operative variable.

Authority-mode responses across both affected categories named exclusively English-language publications, providing secondary evidence for the hypothesis.

The pattern is preliminary because no v0.6 category was designed-for-test. **Phase 2** will add at least one designed-for-test category. Candidates: Japanese kitchen knives, French wine, Korean small electronics — categories where a non-English-discourse country dominates global production but has limited US-targeted English marketing.

This is a documented limit, not a defect — but it constrains the categories to which AI Presence applies cleanly.

### 8.4 Temporal lag (Pattern 6 boundary)

AI training corpora are necessarily backward-looking. Brands that have shut down, rebranded, or merged persist in AI mediation for an indeterminate period. **AI Presence measures the current AI surface, which is not the same as current market reality.**

v0.6 documented this with Mint: 25 months after Intuit decommissioned the application (March 2024), Mint surfaced in 44% of personal finance responses (Anthropic 65%, OpenAI 23%). The 42-point cross-model spread is the second-largest in the personal finance dataset, indicating per-model training-data freshness differences rather than a finding about Mint specifically.

The mechanism is structural — there is no removal mechanism in AI training pipelines for a brand that ceases to exist; the corpus simply ages and the brand persists within it. Reports cite measurement dates and flag known phantom-brand cases.

**Phase 2** will include at least one category selected for the presence of a recent major brand disruption to test whether the phantom-brand pattern replicates. Candidates: Twitter→X transition, Bed Bath & Beyond shutdown and revival, several pharmaceutical brand transitions.

### 8.5 Sample-size and time-window limits

- **Up to 96 measurements per category** is sufficient to claim cross-category replication of patterns when patterns are large relative to the ~10pp confidence band. v0.6 categories range from 75 to 96 successful measurements (§3.3); cells with reduced run counts carry proportionally wider bands. Smaller within-category margins should not be treated as decisive.
- **Five categories** is enough to claim replication across diverse contexts; not enough to claim universal generalizability. Phase 2 broadens the category set.
- **Single-day measurement per category** describes AI behavior on those days, not how AI brand visibility moves over time. AI models update frequently, often without external notice. Longitudinal measurement requires periodic re-baselining and is targeted for Phase 2.
- **Two models, not three.** See §4.2.

### 8.6 Registry construction is not perfectly neutral

The brand registry for each category is curated and reflects the framework's view of which brands constitute the category's competitive set. Two of v0.6's five categories required revision after first measurement. The unknown-mentions list provides a continuing diagnostic, but registry construction remains the methodological choice with the most direct effect on which brands appear in measurements.

---

## 9. The Phase structure

- **Phase 1** (v0.1 → v0.6): Five-category baseline. AI Presence as a single component, two models, single time-point per category. **Complete.**
- **Phase 2** (in progress): Two designed-for-test categories — one for discourse-language bias (Pattern 4), one for phantom-brand persistence (Pattern 6). Mode classifier added as pre-step. Gemini reinstatement when access clears. Longitudinal re-baselining begins. Extractor system prompt parameterized by category.
- **Phase 3**: Construct-validity study. AI Presence correlated against external consumer-tracking data across at least three categories at two time points.
- **Phase 4** (contingent on Phase 3): Release of remaining five AIAS components — Consistency first (computable from existing data), Ranking second (framework's strategic implications depend on it), then Coverage, Grounding, Sentiment as cross-category data permits.

---

## 10. Citation

> Gonzalez Castro, P. U. (2026). *AIAS Presence Measurement Protocol* (Version 1.0). Third System. https://thirdsystem.ai/methodology

Reports built using this protocol cite:

> Method: AIAS Presence Measurement Protocol v1.0 (Gonzalez Castro, 2026).

The v0.6 cross-category report cites the predecessor methodology log (`methodology.md v0.3`); v1.0 supersedes it.

---

## 11. Change log

| Version | Date | Change |
|---|---|---|
| **v0.1** | 28 April 2026 (Day 2 baseline) | 5 prompts × 3 models × 5 runs = 75 calls. 15-brand registry. Detection: regex word-boundary matching against alias list. Output metric: mention rate, raw percentage. |
| **v0.2** | 29 April 2026 morning (Path C, Step 1) | Same 5 prompts, same registry. Re-extracted existing data with structured-output (function-calling) extraction. Added rank, sentiment, primary-recommendation flags. Composite formula introduced: `0.4 × MentionRate + 0.4 × RankSOM + 0.2 × PrimaryRecRate`, normalized so leader = 100. **Documented calibration error**: rank-relative normalization forced the leader to 100 regardless of absolute performance; with Asana/Jira/Linear clustered near 79% mention rate, the v0.2 output displayed Linear at 100 and the others at 92/84, implying near-saturation the underlying data did not support. Inconsistent with the framework's own definition of AIAS as a 0–100 absolute scale. v0.2 output is superseded. |
| **v0.3** | 29 April 2026 evening | Reframed output as **AI Presence Index** (the first of six AIAS components), not AIAS. `presence_score = raw mention rate`, no normalization. RankSOM and Primary-Rec kept as separate descriptive columns. Consistency column added, explicitly marked as "future AIAS component, displayed for transparency." Sixth prompt (`COMPARISON`) added. Eight runs per prompt (96 measurements per category). Methodology log `methodology.md v0.3` published. PM software dataset published. PM registry expansion (15 → 19 brands) confirmed by `iCloud:aias backup/brands.json` snapshot at 17:38. |
| **v0.4** | 30 April 2026 morning–evening | Olive oil run with initial 16-brand registry (08:33), then revised to 20 brands (`v2-oliveoil-rev1`) after Cobram Estate surfaced as the most-mentioned unknown. Running shoes run completed evening of 29 April with 17-brand registry (no revision needed). Skincare run completed evening of 30 April with revised registry. Hypothesis revisions including the variance-vs-category-maturity hypothesis (since rejected — v0.6 demonstrates discourse coherence is the operative variable, not maturity). Registry-revision protocol (§2.4) formalized. |
| **v0.6** | April 29–30, 2026 (cross-category report) | Five-category cross-category run complete. Patterns 1–6 stabilized. Three-modes structure (§3.4) formalized. Cross-category report shipped. |
| **v1.0** | `[FILL: target date — likely May/June 2026, contingent on completion of v0.6 typeset and methodology paper draft]` | First public protocol release as a research instrument. Methodology paper, build pipeline, and example reports shipped together. |

---

## Appendix A — Full prompt templates per category

All prompts follow the six-CEP structure (`FUNCTIONAL_WHY`, `CONTEXTUAL_WHEN`, `CONSTRAINT_WITH`, `IDENTITY_HOW_FEELING`, `DISCOVERY`, `COMPARISON`).

Verbatim text is from `prompts.json` snapshots in iCloud (modification dates correspond to category run dates), except A.4 Skincare, which was reconstructed from CSV response evidence because no `prompts.json` snapshot was preserved.

### A.1 Project management software

Source: `iCloud:aias backup/prompts.json` (modified 29 April 2026 17:38, post-revision).

| ID | CEP | Prompt |
|---|---|---|
| p1_functional | FUNCTIONAL_WHY | What's the best project management software for a small startup team? |
| p2_contextual | CONTEXTUAL_WHEN | My team just hit 50 people and we're outgrowing spreadsheets. What project management tool should we move to? |
| p3_constraint | CONSTRAINT_WITH | What project management software works best for engineering teams that ship every week? |
| p4_identity | IDENTITY_HOW_FEELING | What project management tools do top tech startups actually use? |
| p5_discovery | DISCOVERY | What are some emerging project management tools worth knowing about in 2026? |
| p6_comparison | COMPARISON | I'm choosing between project management tools for a 30-person product team. Compare the leading options and recommend the best one. |

### A.2 Running shoes

Source: `iCloud:aias 2/prompts.json` (modified 29 April 2026 20:38).

| ID | CEP | Prompt |
|---|---|---|
| p1_functional | FUNCTIONAL_WHY | What's the best running shoe for someone training for their first marathon? |
| p2_contextual | CONTEXTUAL_WHEN | I run on wet roads early in the morning and need a shoe that holds up. What should I get? |
| p3_constraint | CONSTRAINT_WITH | I have flat feet, knee pain, and overpronation. What running shoe is right for me? |
| p4_identity | IDENTITY_HOW_FEELING | What running shoes do serious competitive runners actually wear? |
| p5_discovery | DISCOVERY | What are some emerging running shoe brands worth knowing about in 2026? |
| p6_comparison | COMPARISON | I'm choosing my next pair of running shoes and want a daily trainer. Compare the leading options and recommend the best one. |

### A.3 Premium olive oil

Source: `iCloud:aias/prompts.json` (modified 30 April 2026 08:33).

| ID | CEP | Prompt |
|---|---|---|
| p1_functional | FUNCTIONAL_WHY | What's the best olive oil for everyday cooking? |
| p2_contextual | CONTEXTUAL_WHEN | I want to gift a really nice olive oil to a friend who's into food. What should I get? |
| p3_constraint | CONSTRAINT_WITH | What's a good olive oil for finishing dishes — bright, peppery, high quality? |
| p4_identity | IDENTITY_HOW_FEELING | What olive oils do serious chefs and food writers actually use at home? |
| p5_discovery | DISCOVERY | What are some emerging olive oil brands worth knowing about in 2026? |
| p6_comparison | COMPARISON | I'm choosing a premium olive oil for my pantry. Compare the leading options and recommend the best one. |

### A.4 Premium facial skincare

`[VERIFY: source `prompts.json` was not preserved in any iCloud snapshot. Prompts below are reconstructed from the opening sentences of AI responses across the v2-skincare measurement set. Each reconstruction is supported by direct response echo (e.g., the `p1_functional` response opens with "For normal-to-dry skin..." closely mirroring the prompt). Confirm against your own memory or any other backup before publication.]`

| ID | CEP | Prompt (reconstructed) |
|---|---|---|
| p1_functional | FUNCTIONAL_WHY | What's the best moisturizer for normal-to-dry skin? |
| p2_contextual | CONTEXTUAL_WHEN | I'm in my late 30s and starting to notice fine lines. What skincare products should I use? |
| p3_constraint | CONSTRAINT_WITH | I have sensitive skin that reacts to fragrances and harsh ingredients. What skincare brands work for me? |
| p4_identity | IDENTITY_HOW_FEELING | What skincare brands do dermatologists actually recommend to their patients? |
| p5_discovery | DISCOVERY | What are some emerging skincare brands worth knowing about in 2026? |
| p6_comparison | COMPARISON | I'm building a skincare routine and want to invest in quality products. Compare the leading brands and recommend the best one. |

### A.5 Personal finance applications

Source: `/Users/pablou/aias/prompts.json` (live file at time of v1.0 draft; modification date 30 April 2026 evening).

| ID | CEP | Prompt |
|---|---|---|
| p1_functional | FUNCTIONAL_WHY | What's the best app for tracking my spending and creating a budget? |
| p2_contextual | CONTEXTUAL_WHEN | I just paid off my credit card debt and want to start saving for big goals. What app should I use? |
| p3_constraint | CONSTRAINT_WITH | My partner and I want to manage our money together but keep some accounts separate. What apps support this? |
| p4_identity | IDENTITY_HOW_FEELING | What personal finance apps do people who are actually good with money use? |
| p5_discovery | DISCOVERY | Mint shut down. What are the best modern alternatives I should consider? |
| p6_comparison | COMPARISON | I want to take my personal finances seriously. Compare the leading personal finance apps and recommend the best one. |

---

## Appendix B — Brand registries per category as of v0.6

Each registry uses the schema `{canonical, tier, aliases}` where `tier ∈ {incumbent, mid-tier, challenger}`. Aliases are intentionally narrow; the structured-output extractor handles contextual disambiguation (§5.1).

### B.1 Project management software (19 brands, post-revision)

Source: `iCloud:aias backup/brands.json` (modified 29 April 2026 17:38, post-revision).

**Incumbents (5):** Asana, Monday, Jira, Trello, Confluence
**Mid-tier (8):** Notion, ClickUp, Smartsheet, Wrike, Airtable, Basecamp, Coda, Workfront
**Challengers (6):** Linear, Height, Motion, Shortcut, Todoist, GitHub Projects

Pre-revision registry was 15 brands (29 April 2026 morning); the four added during the registry-revision step were Confluence, Coda, Workfront, and GitHub Projects.

### B.2 Running shoes (17 brands)

Source: `iCloud:aias 2/brands.json` (modified 29 April 2026 21:03). No revision required.

**Incumbents (5):** Nike, Adidas, Asics, New Balance, Brooks
**Mid-tier (5):** Saucony, Mizuno, Puma, Under Armour, Reebok
**Challengers (7):** Hoka, On, Altra, Topo Athletic, Salomon, Norda, Tracksmith

Note: the `On` alias list excludes the bare token "on" to avoid false-positives on the preposition; structured-output extraction handles contextual disambiguation.

### B.3 Premium olive oil (20 brands, post-revision)

Source: `iCloud:aias/brands.json` (modified 30 April 2026 09:01, post-revision).

**Incumbents (6):** Bertolli, Colavita, Filippo Berio, California Olive Ranch, Goya, Cobram Estate
**Mid-tier (7):** Lucini, Partanna, Frantoio Muraglia, Castillo de Canena, McEvoy Ranch, Manni, Colonna
**Challengers (7):** Brightland, Graza, Fly By Jing, Frescobaldi Laudemio, Olio Verde, Kosterina, Núñez de Prado

Pre-revision registry was 16 brands; the four added during the registry-revision step were Cobram Estate (promoted to incumbent), Manni (mid-tier), McEvoy Ranch (mid-tier), Colonna (mid-tier).

**Boundary-condition test brands** (Spanish representation, §2.3): Goya (incumbent), Castillo de Canena (mid-tier), Núñez de Prado (challenger).

### B.4 Premium facial skincare (24 brands surfaced; ~31 claimed in narrative)

`[VERIFY: source brands.json for skincare not preserved in any iCloud snapshot. The 24 brands below are the canonical brands that appeared at least once in the v2-skincare CSVs (i.e., in `brands_canonical` after extractor matching). The v0.5 protocol narrative claimed a 31-brand registry post-revision; the 7-brand discrepancy may represent registry entries that scored zero mentions in measurement (consistent with Pattern 4's discourse-language bias finding for absent K-beauty brands), or may reflect imprecision in the v0.5 narrative. For final publication, either recover the original `brands.json` from Time Machine, or use the 24-brand actually-surfaced list as canonical and note the discrepancy explicitly. Tier assignments below are reconstructed by analogy with the four other registries and brand-knowledge; verify or correct against an authoritative source before publication.]`

**Incumbents (likely 7):** CeraVe, Cetaphil, Neutrogena, La Roche-Posay, Vanicream, Skinceuticals, Eucerin
**Mid-tier (likely 9):** Paula's Choice, Drunk Elephant, Tatcha, The Ordinary, EltaMD, Bioderma, Avène, Aveeno, First Aid Beauty
**Challengers (likely 8):** Augustinus Bader, Youth to the People, La Mer, Estée Lauder, Lancôme, Clinique, Kiehl's, Sunday Riley

**Brands cited in v0.6 findings but absent from measurements** (likely registered but scored 0%): SK-II, Olay, Origins, Dermalogica, Murad, Glossier. Their absence is consistent with the v0.6 Pattern 3 finding that traditional luxury skincare brands underperform in AI mediation.

**Boundary-condition test brand** (K-beauty representation, §2.3): Beauty of Joseon (and possibly Sulwhasoo, AmorePacific). All scored 0% — consistent with Pattern 4 (discourse-language bias).

### B.5 Personal finance applications (16 brands)

Source: `/Users/pablou/aias/brands.json` (live file).

**Incumbents (6):** Mint, Quicken, Quicken Simplifi, YNAB, Empower, NerdWallet
**Mid-tier (4):** Rocket Money, PocketGuard, Goodbudget, EveryDollar
**Challengers (6):** Monarch Money, Copilot, Lunch Money, Origin, Cleo, Tiller

Mint is flagged as a phantom brand (decommissioned March 2024, 25 months prior to v0.6 measurement; see §8.4 and Pattern 6). Empower's alias list includes "personal capital" because the brand was rebranded from Personal Capital and AI training data may surface either name.

The v0.5 protocol narrative listed Fidelity as part of the personal finance registry; the actual `brands.json` does not include Fidelity. The 16-brand count is verified against the source file.

---

## Appendix C — Reference implementation

The reference build pipeline is at `/Users/pablou/aias/`. `[FILL: GitHub URL if the repository is public, or "Reference implementation is closed-source pending Phase 4 release; selected artifacts available on request to hello@thirdsystem.ai" if the repo is private.]`

The pipeline takes (1) this protocol as a fixed input, (2) a per-report `report_spec.json`, (3) a content module, and (4) a chart manifest, and produces a typeset PDF.

The measurement engine consists of:

- `run_aias_v2.py` — measurement runner with retry logic and version metadata. Constants: `METHODOLOGY_VERSION = "0.3"`, `RUNS_PER_PROMPT = 8`, `TEMPERATURE = 0.7`. Reads `brands.json` and `prompts.json` from working directory.
- `extractor.py` — function-calling brand extraction (`record_brand_mentions` schema). Uses `gpt-5.4-mini` at `temperature=0` for extraction. Includes regex fallback.
- `reextract.py` — re-extraction utility for existing data (used during the v0.1 → v0.2 rework).
- `analyze_v3.py` — Presence-only analyzer.
- `retry_helper.py` — rate-limit and retry handling. Returns `(result, status, attempts)`.
- `brands.json` — category brand registry (per-category file; swapped between runs).
- `prompts.json` — category prompt set (per-category file; swapped between runs).
- `methodology.md` — predecessor to this protocol (v0.3).

**Workflow note from v0.6**: the runner reads `brands.json` and `prompts.json` from the current working directory rather than taking a category parameter. As a result, running multiple categories required swapping these files between runs. iCloud snapshots from key dates (29 April morning/afternoon/evening, 30 April morning) preserve historical states for PM, Running, and Olive Oil; the Skincare snapshot was not preserved, complicating reconstruction (§A.4, §B.4). **Phase 2 will refactor the runner to take an explicit category argument** and read `brands_<category>.json` / `prompts_<category>.json`, eliminating the swap workflow and the snapshot-loss risk.

**Reporting pipeline** (Phase B, May 2026): produces nine canonical chart PDFs per cross-category report at locked dimensions (3-col inline 3.68×2.85", 4-col 4.95×3.71", 6-col hero 7.5×5.0", 6-col TALL 7.5×6.5", spread 7.5×4.5"). Charts are sourced from `chart_style.py` and `chart_utils.py`, which read all visual parameters from `third_system_brand.json` v1.4. Chart slot mappings appear in `report_specs.json`.

See the repo README for run instructions.

---

## Appendix D — Outstanding decisions for v1.0 release

The following items are operational or editorial decisions Pablo must make before public v1.0 release. All have proposed defaults that can be accepted as-is if no override is needed.

| # | Item | Proposed default | Section |
|---|---|---|---|
| 1 | Raw response retention period | "Indefinitely on Third System infrastructure for replay and audit" | §4.4, §7.1 |
| 2 | Public availability of raw responses (`results_v2_*.csv`) | "Available on request to hello@thirdsystem.ai" | §7.1 |
| 3 | Refusal/error handling policy | "Failed calls (`rate_limit_final`/`transient_final`/`hard_error`) excluded from dataset; reduced run counts disclosed in §3.3" | §6.3 |
| 4 | Retry count and backoff schedule | (read from `retry_helper.py`) | §6.3 |
| 5 | Pre-run check beyond what's in script | "Manual prompt-template review against CEP coverage; dry run on one prompt-model pair before full sweep" | §6.1 |
| 6 | v1.0 target release date | May or June 2026 | §11 |
| 7 | GitHub URL or closed-source statement | Closed-source pending Phase 4 | App. C |
| 8 | Skincare prompts: accept reconstructions or recover from Time Machine | Accept reconstructions; flag in §A.4 footnote | §A.4 |
| 9 | Skincare brands: accept 24-brand surfaced list or recover registry | Accept 24-brand list; flag in §B.4 footnote | §B.4 |

For items 1–5: pull values from `retry_helper.py` and your operational practice. For items 6–7: editorial decisions for v1.0. For items 8–9: choose recovery vs honest acknowledgment.

Once Appendix D is closed, v1.0 is publication-ready.
