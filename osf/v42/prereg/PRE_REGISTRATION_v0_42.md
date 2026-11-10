
# AIAS™ Presence Measurement Protocol — Pre-Registration v0.42 (revision r2, draft for review)

**Study:** The t₄ wave on the newest models — cross-generation stability of AIAS Presence and Consistency, and the baseline of the t₄ → t₅ → t₆ series.
**Design:** Re-asks, verbatim, questions of the five-substrate omnibus (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units) to the newest generally available flagship model of each provider (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon): the 30 category questions (Phase B) without and with the provider's own web search, three independent runs each, and the 112 brand questions (Phase A) without search, one run: 3 models × (30 × 2 conditions × 3 runs + 112) = 876 calls. Compares the answers with the t₃ wave on the retiring six-model panel, collected on 2026-11-09 (v0.41).
**Budget:** at most US$100 of paid model calls, hard cap (programme rule, 2026-11-10). Estimated cost $64 (central; §4.5). Spend is computed from the recorded usage of every billed request; collection pauses at $80 and stops before $100 (§4.5).
**Programme position:** First wave on the programme's next reference panel. It is (i) the cross-generation study of the plan (study list #56 and #58; the within-provider version contrast is removed in r2, §9 C12), (ii) the baseline of the short-term (t₅, about +3 weeks) and three-month (t₆) stability waves, and (iii) a stored corpus of answers for the four new components (Ranking, Sentiment, Coverage, Grounding), whose analyses are pre-registered in their own papers (§6).
**Protocol version:** Recall Presence (π̂), recognition and Consistency (φ, Methodology v1.8, SSRN 6963359) as locked for the omnibus and implemented in the v0.41 scorer (`osf/v41/scripts/score_v41.py`; v0.41, SSRN 7685100). Mention detection and recognition coding by each substrate's certified t₁ functions (§5.1).
**Lock target:** git tag `v0.42-prereg-r1` on branch `v0.42`, pushed to `origin` (tag name unchanged from r1, which was never locked; the coder pins it; §9 C21). **External anchor (pre-declared):** deposit of this pre-registration, the probe file, the parity and feasibility records, the cost estimate, the scripts and the lock manifest at OSF `ec6wh` → `v42/prereg/`, with `v42/anchor/` naming the tag's commit, before any study probe is sent. `acquire_v0_42.py --collect` refuses to run until the tag is on `origin` and the anchor file exists.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r2 draft, written on 2026-11-10 after the pre-registrant's hold on r1 (Nov 10, 8:03 am US Central: "do not lock or collect v0.42 as drafted (~$400). New rule: at most $100 of paid model calls per paper."). r1 (3,408 calls, about $400) was deposited at OSF `v42/prereg/draft/` and is superseded. r2 locks 24 hours after it reaches the pre-registrant unless he objects (programme rule for new collections, Nov 9, 2026). No study probe has been sent.
**Pre-lock feasibility check (non-acquisition, under r1):** on 2026-11-10 at 05:13 UTC each of the four r1 models received the neutral prompt "Reply with the single word: ready" without tools, and the two neutral search-enabled prompts of v0.39 (today's date in UTC; the current top headline on bbc.com) with its provider's web search. 11 of 12 calls returned ok, and every model served its requested ID (`claude-fable-5-2`, `claude-opus-5-5`, `gpt-6-astra`, `gemini-4-argon`). Claude Fable 5.2 ended the headline prompt with an empty answer after a tool call (finish reason `tool_use`) despite the script's one retry; a single diagnostic re-send of the same neutral prompt, outside the record, ended normally after 4 searches. Gemini 4 Argon answered the date prompt without searching. Record: `osf/v42/prereg/feasibility_v0_42.json`. No study probe was sent. The Message Batches path used for Claude Fable 5.2 in r2 (§4.4) was not part of this check; it is tested against local fakes only (§9 C20).
**Collection window:** after the lock; all 876 calls within 72 hours. It must not overlap v0.40's collection (2026-11-17 to 2026-11-21): one paid collection at a time on the collection machine. The v0.23 recognition coding uses Claude Sonnet 4.5 and must finish before that model's scheduled retirement on 2026-11-30.

---

## §1 Context

The six-model panel used since v0.17 is retiring: Claude Opus 4.5 not sooner than 2026-11-24, Claude Sonnet 4.5 on 2026-11-30, the GPT-4o and GPT-4o mini snapshots on 2027-01-14 (`osf/v40/registries/model_cutoffs.csv`). v0.41 took its last wave (t₃) on 2026-11-09. Over the 152 days from t₂ to t₃ both components held on that panel: recall Presence ρ = 0.93–0.98 in all five substrates, and φ ρ = 0.681 (n = 80). From now on every new collection runs on current models.

Two questions follow before the programme builds its next components on those models:

1. **Generation.** Does the ordering of brands by AI availability carry over from the 2024–25 model generation to the 2026 generation? If it does, the programme's record on the legacy panel can be bridged to the new panel; if it does not, the new panel starts its own series.
2. **Series.** How much do the new models' answers vary from run to run? That noise floor is what the t₅ and t₆ stability waves will be judged against.

r1 also asked a version question (do two current versions of one provider's model, Claude Fable 5.2 and Claude Opus 5.5, order brands alike?). It needs two flagships of one provider side by side, which the programme's collection budget rule excludes; r2 removes it (§9 C12, with the budget that would test it).

Panel rule (Pablo, Nov 9, 2026): the newest generally available flagship model of each provider (Anthropic, OpenAI, Google), verified from the vendor's own model documentation when the pre-registration is written; restricted or pre-release models are out. §4.3 records the verification. Budget rule (Pablo, Nov 10, 2026): at most $100 of paid model calls per paper, hard cap, overriding any larger cap in a draft; one flagship per provider, cheaper tiers where a question does not need the flagship, the fewest runs that keep the pre-registered tests valid, batch pricing and output caps where the vendor offers them. §4.5 gives the estimate and the design trade-off.

---

## §2 Pre-registered hypotheses

### §2.1 Definitions (used by every test)

- **Brand units.** The 112 brands of the five omnibus registries (16 + 24 + 24 + 24 + 24), unchanged from t₁–t₃.
- **Phase B (recall).** Six category questions per substrate (30 in all). **Phase A (recognition).** One question per brand (112).
- **k_{b,m,r}.** Number of the six Phase B questions of brand b's substrate in which model m's answer in run r mentions b (§5.1). At t₃: one run, the locked v0.41 counts (`osf/v41/v41_three_wave_table.csv`, column `k_per_model`, wave t3).
- **Recall Presence** of brand b on panel P: π̂_{b,P} = Σ_{m∈P} Σ_r k_{b,m,r} ÷ (6 · |P| · R), with R runs. At t₃ (P = L6, R = 1) this is the locked v0.41 `pi_hat`. Rates use the answered calls as the denominator (§5.4).
- **Consistency.** φ_{b,P,r} = the v1.8 formula on panel P in run r, φ = [1/(M − 1)] · Σ_m (k_m − 6π̂)² ÷ [6π̂(1 − π̂)] with M = |P| and π̂ the run's recall rate, with the locked partitions (π̂ = 0 → zero; π̂ = 1 → saturated; otherwise defined) and the v0.41 reduced-panel kernel `phi_m`. Higher φ = less consistent. At t₄, φ_{b,P} = the mean of φ_{b,P,r} over the runs whose partition is defined; undefined if fewer than 2 of the 3 runs are defined. At t₃: the locked v0.41 `phi` (defined partition only).
- **Panels.** L6 = the six legacy models at t₃ (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite). N3 = the newest generally available flagship of each provider: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon (§4.3). r1's current-arm panel C3 (Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon) is not collected in r2 (§9 C11).
- **Conditions.** S0 = no tools; S1 = the provider's own web search (§4.4). Phase B is collected in S0 and S1; Phase A in S0 only (§9 C13).
- **ρ_pw(x, y).** Pooled within-substrate Spearman correlation: values ranked within substrate (average ranks for ties), then Pearson's r of those ranks over all brands pooled (`pooled_within_rho` in `score_v41.py`).
- **Permutation p.** One-sided; y shuffled within substrate; ρ_pw recomputed on each draw exactly as observed (within-substrate ranks); 10,000 draws; p = (1 + #{ρ_perm ≥ ρ_obs}) ÷ 10,001.
- **Bootstrap.** Brands resampled with replacement within substrate; 10,000 resamples; percentile 95% interval.
- **Seeds.** 420041 (H_Gen_Presence), 420043 (H_Gen_Phi), 420044 (H_Search_Presence), 420045 (descriptives). 420042 belonged to the removed H_Version_Presence and is retired.
- **α.** 0.05 per test, no multiplicity correction; verdicts rest on pre-set effect-size thresholds, and every test is reported.

### §2.2 PRIMARY: `H_Gen_Presence` — Presence carries over to the new model generation

**Statement.** On the newest models (N3, S0, t₄), recall Presence orders brands as it did on the retiring panel (L6, t₃) a few days earlier (t₃ on 2026-11-09; t₄ after the lock and before 2026-11-17).

**Operationalisation.** x = π̂_{b,L6} at t₃; y = π̂_{b,N3,S0} at t₄ (three runs); all 112 brands.

**Test.** ρ_gen = ρ_pw(x, y); permutation p (seed 420041); bootstrap interval.

**Verdict rule.** CONFIRMED if ρ_gen ≥ 0.70 and p < 0.05 · FALSIFIED if ρ_gen < 0.50 · MARGINAL otherwise.

**Rationale.** 0.70 is the programme's stability bar (v0.34). The legacy panel held 0.93–0.98 over five months (v0.41), so a value below 0.70 across a few days is attributable to the change of model generation, not to time. Below 0.50 the two generations order brands too differently for the legacy record to be bridged quantitatively, and the new panel starts its own series. Thresholds are set before any t₄ answer exists; the t₃ values are already published.

**Reported alongside.** Per-substrate ρ; the same test with S1 in place of S0; per-provider generation pairs, each the ρ_pw between the provider's two legacy models pooled and its new model (Anthropic: Claude Opus 4.5 + Claude Sonnet 4.5 → Claude Fable 5.2; OpenAI: GPT-4o + GPT-4o mini → GPT-6 Astra; Google: Gemini 2.5 Flash + Flash-Lite → Gemini 4 Argon); the level shift Δ = mean(y − x) with its bootstrap interval.

### §2.3 (removed in r2) `H_Version_Presence`

r1's second primary hypothesis (Claude Fable 5.2 vs Claude Opus 5.5, disattenuated ρ* ≥ 0.80) is removed: it needs both models side by side, which the budget rule excludes. No other hypothesis depends on it. §9 C12 records why and the smallest separate budget that would test it.

### §2.4 SECONDARY: `H_Gen_Phi` — Consistency carries over to the new model generation

**Statement.** On the newest models (N3, S0, t₄), φ orders brands as it did on the retiring panel at t₃.

**Operationalisation.** x = φ_{b,L6} at t₃; y = φ_{b,N3,S0} at t₄ (§2.1); brands with φ defined on both.

**Test.** ρ_pw; permutation p (seed 420043); bootstrap interval.

**Verdict rule.** UNDETERMINED if n < 40 · CONFIRMED if ρ ≥ 0.50 and p < 0.05 · FALSIFIED if ρ < 0.30 · MARGINAL otherwise (the thresholds and n floor of v0.41's `H_Phi_LongHorizon`).

**Declared.** φ on three models carries less information per brand than on six; that is why this test is secondary.

**Reported alongside.** Mean-independence on N3 (|ρ_pw(φ, π̂)|, flagged if ≥ 0.50, the v1.7 ceiling); partition counts (zero, saturated, defined) per condition.

### §2.5 SECONDARY: `H_Search_Presence` — what web search does to Presence

**Statement (two-sided question).** Turning on each provider's web search leaves the Presence ordering of brands intact.

**Operationalisation.** N3; x = π̂_{b,N3,S0}; y = π̂_{b,N3,S1} (three runs each).

**Statistic.** ρ_S = ρ_pw(x, y) with its bootstrap interval (seed 420044); level shift Δ = mean(y − x) with its interval.

**Reading (pre-declared labels; no confirm or falsify).** Search-robust if the interval's lower bound ≥ 0.80 · search-dominated if its upper bound < 0.50 · search-sensitive otherwise.

**Reported alongside.** Per model and per substrate.

### §2.6 Manipulation checks

- **MC_Complete.** At least 98% of the 876 calls end with non-empty answer text after the retry policy (§4.4). A model × condition below 90% of its calls (S0: 202 per model; S1: 90 per model) triggers the model drop rule (§5.4).
- **MC_Served.** Every served model ID equals the requested ID (a dated snapshot of it is recorded and accepted). Any other ID: the call is excluded and re-run, and logged.
- **MC_Search.** Share of S1 calls with at least one web search, per model. Below 25% flags that model's S1 as "search rarely used" in every S1 result.
- **MC_Truncation.** Share of calls that end at the output cap, per model × condition; above 5% is flagged.
- **MC_Window.** First and last call times; all calls within 72 hours.
- **MC_Parity.** Gates P1–P3 (§5.3) pass before any t₄ statistic is computed.
- **MC_Budget (new in r2).** Spend from the recorded usage (§4.5) stays at or below $100 including the judge reserve; every pause, approval and stop is logged in `osf/v42/data/t4_budget_state.json` and reported, with the calls not sent.

### §2.7 Pre-registered descriptives (no verdicts)

1. Run-to-run reliability per model × condition: rel1 (the mean of ρ_pw over the three run pairs of k_{b,m,r} ÷ 6) and rel3 = 3 · rel1 ÷ (1 + 2 · rel1) of recall. These are the noise floor for t₅. Recognition agreement across runs is not computed (Phase A has one run; §9 C13).
2. Recognition: share of brands coded as recognized, per model (S0), beside each legacy model at t₃.
3. Floor persistence: of the brands below v0.41's recall floor at t₃ (mean k per model < 1), the share still below it on N3, S0, at t₄ (mean k per model-run < 1); and the reverse.
4. Answer form: words per answer; registry brands named per Phase B answer; finish reasons; non-answers (a v0.19–v0.22 Phase A answer with no yes or no; refusals).
5. Search (S1): searches, sources and citations per call; share of answers with at least one citation; the 20 most-cited domains per model.
6. Cost: tokens, searches and spend per model × condition, from the recorded usage of every billed request at the list prices of §4.5.

---

## §3 Brand registries

Unchanged from t₁–t₃: the five omnibus registries and their probe artefacts, SHA-256-checked against the v0.41 acquisition manifest (8 of 8 match; `osf/v42/prereg/probe_parity_v0_42.json`). No brand is added, removed or renamed. Each registry's conflict-of-interest handling is carried forward unchanged (§8).

---

## §4 Probes and collection

### §4.1 Probe file

`osf/v42/prereg/probes_v0_42.jsonl`: 142 lines (Phase A 112, Phase B 30), built by `osf/v42/scripts/export_probes_v0_42.py`, which runs each legacy runner's own prompt-building code with the provider call stubbed out (no prompt is retyped). No probe carries a system prompt. Phase A for v0.19–v0.22 asks whether a named brand is commonly recognized as a brand of the category and asks for yes or no (for example, "Is the brand Mercedes-Benz commonly recognized as a car brand? Answer yes or no."); Phase A for v0.23 asks an open question about the brand. Phase B asks six category questions per substrate (for v0.19–v0.22 the first is of the form "What are the best skincare brands? List several with descriptions."; v0.23 uses three expert-acclaim frames, EA-1 to EA-3, and three cultural-community frames, CC-1 to CC-3). The probe file is unchanged in r2.

**Parity with t₃** (`probe_parity_v0_42.json`): for v0.20–v0.23 every prompt recorded at t₃ (720 of 720 records) equals the exported prompt byte for byte. v0.19 recorded no prompt text at t₃; its parity rests on the artefact checksums (8 of 8 match) and on the query IDs (the 132 recorded IDs equal the artefact's).

### §4.2 Design

| Block (collection order) | Phase | Condition | Run | Calls per model | Calls (N3) |
|---|---|---|---|---|---|
| 1–3 | B (30 category questions) | S0 | 1, 2, 3 | 90 | 270 |
| 4 | A (112 brand questions) | S0 | 1 | 112 | 336 |
| 5–7 | B | S1 | 1, 2, 3 | 90 | 270 |
| **Total** | | | | **292** | **876** |

Each call is independent (no conversation state carried between calls). Blocks run in this order, the three models in parallel within a block, so that the primary test's answers (S0) and the recognition answers are complete before the costly search-on answers begin (§4.5).

### §4.3 Panel (verified on 2026-11-10 from each vendor's own documentation)

| Provider | Newest generally available flagship (N3) | Verification |
|---|---|---|
| Anthropic | Claude Fable 5.2, `claude-fable-5-2` | Claude Fable 5.2 model page (platform.claude.com): status "Active (latest)", released November 9, 2026, retirement not sooner than November 9, 2027. Claude Mythos 5.2, with the same capabilities, is available only to organizations verified through Anthropic's verification programs: restricted, so excluded. |
| OpenAI | GPT-6 Astra, `gpt-6-astra` | GPT-6 Astra model page (developers.openai.com): "Our most capable model for the most demanding work"; the latest-model guide lists GPT-6.1 Sol ("Balanced speed, cost, and intelligence") and GPT-6.1 Terra ("Fast and efficient") below it. No dated snapshot is listed. |
| Google | Gemini 4 Argon, `gemini-4-argon` | Gemini API changelog: "Gemini 4 Argon (`gemini-4-argon`) generally available (GA)" on October 13, 2026; model page lists it as stable; no newer stable model listed. |

**Note on the candidate list.** The plan of Nov 9 named GPT-6.1 Terra as OpenAI's candidate. OpenAI's own documentation places GPT-6.1 Terra two tiers below GPT-6 Astra, so the rule ("the newest generally available flagship") selects GPT-6 Astra.

**One Anthropic flagship (r2).** The budget rule allows one flagship per provider. Claude Fable 5.2 and Claude Opus 5.5 (`claude-opus-5-5`, the current arm since v0.38) are both active; Claude Fable 5.2 is the newest ("Active (latest)", released November 9, 2026), so the model rule selects it. Cost does not force the cheaper model: with Anthropic's Batch API the design's central estimate is $64, below the $80 pause, at both t₄ and t₅/t₆ prices (§4.5). Claude Fable 5.2's per-call cost is the least certain input of the estimate; the guard and the collection order (§4.5) bound the consequence. Claude Opus 5.5 is not collected (§9 C11).

**Cheaper tiers.** Not used: every kept question is about the newest flagship models (generation contrast; the series baseline; the Grounding corpus of v1.13, defined on N3), so a lower tier would change the question. The v0.23 recognition judge (Claude Sonnet 4.5, coding, not acquisition) is already a non-flagship model.

### §4.4 Conditions, decoding and call policy

- **S0:** no tools. **S1:** the provider's own web search, configured exactly as in v0.39 (Anthropic `web_search_20250305`, at most 5 uses; OpenAI Responses API `web_search`, search context size medium, sources included; Google Search grounding). S1 records every search query, consulted source and citation.
- **Decoding.** Temperature, top-p and reasoning effort are left at provider defaults. Claude Fable 5.2 accepts no temperature, top-p or top-k; its adaptive thinking is always on (default effort high). Maximum output 16,384 tokens (the v0.38–v0.40 current-arm cap). The cap is not lowered for cost: the largest current-arm answer at v0.39 used 2,749 output tokens, so a lower cap would save money only by truncating answers (MC_Truncation); the budget guard bounds the tail instead (§4.5).
- **Call modes (r2).** Claude Fable 5.2 is sent through Anthropic's Message Batches API: each request carries exactly the parameters of the synchronous call of r1 and v0.39 (model, `max_tokens` 16,384, the user message, and in S1 the same web-search tool), built by `anthropic_params` and tested against the synchronous call function. Anthropic's batch documentation states that "All server tools (web search, web fetch, code execution, MCP connectors, advisor, and tool search) work in batch requests" and that "All usage is charged at 50 percent of the standard API prices"; batches are processed asynchronously ("most batches finishing in less than 1 hour"; they expire if not completed within 24 hours). GPT-6 Astra and Gemini 4 Argon are called synchronously, as in r1: OpenAI documents a 50% Batch price for GPT-6 Astra and `/v1/responses` in its Batch API, but none of its pricing, Batch or web-search pages says whether the web-search tool works in Batch, and Google lists no batch price for Gemini 4 Argon (§4.5).
- **Order.** Blocks 1–7 of §4.2 in order; within a block one worker per model, the three in parallel, probes in file order.
- **Retries.** Synchronous calls: transient errors and empty answers are retried under the v0.39 policy (`_call_with_retry`; an empty answer is re-sent once). Batched calls: a request that ends with a transient error type (`api_error`, `overloaded_error`, `rate_limit_error`, `timeout_error`) or expires is re-sent in a later batch, up to 3 attempts in all; an empty answer is re-sent once; any other error is not re-sent. An Anthropic `pause_turn` is continued once with identical tools (for a batched call, synchronously). Calls still failing after the main pass get one logged re-run pass inside the window. The run is resumable; every attempt is logged, and every billed request is costed (§4.5).
- **Legacy settings that do not carry over (declared).** The t₁–t₃ runners used temperature 0.0 where they set it, output caps of 64 to 2,048 tokens, no tools, and, for v0.19–v0.22, the deprecated `google.generativeai` SDK (`probe_parity_v0_42.json`). The generation contrast is therefore a contrast of model generation together with its default serving settings, as a user meets it.
- **Artefact.** `osf/v42/data/t4_raw.jsonl`, one line per attempt: call ID, substrate, phase, probe ID, brand or frame ID, requested and served model, condition, run, prompt, answer text, finish reason, input, output and thinking tokens where reported, S1 search record (queries, sources, citations, errors), pause continuation, start and end times (UTC), error, attempt count; new in r2: call mode (`batch` or `standard`), the usage of every billed request (`usage_parts`), its cost at the §4.5 prices (`cost_usd`), and for batched calls the batch and request IDs.

### §4.5 Budget (r2)

**Cap.** At most $100 of paid model calls for this paper, including re-sends and the v0.23 recognition judge (programme rule, 2026-11-10).

**Prices** (vendors' own pages, opened 2026-11-10; machine copy in `osf/v42/scripts/budget_v0_42.py`):

| Model / item | Standard, US$ per 1M tokens in / out | Batch | Search fee | Source |
|---|---|---|---|---|
| Claude Fable 5.2 | 8 / 40 | 4 / 20 | web search $10 per 1,000 searches, "plus standard token costs for search-generated content" | https://platform.claude.com/docs/about-claude/pricing ; batch supports web search: https://platform.claude.com/docs/en/build-with-claude/batch-processing |
| Claude Opus 5.5 (not collected; alternatives only) | 4 / 20 | 2 / 10 | as above | same |
| Claude Sonnet 4.5 (v0.23 judge) | 3 / 15 | — | — | same |
| GPT-6 Astra | 10 / 50 | 5 / 25 ("Batch and Flex are priced at 50% of Standard rates"; not used) | web search $10 per 1,000 calls; "Search content tokens billed at model rates" | https://developers.openai.com/api/docs/pricing ; https://developers.openai.com/docs/models/gpt-6-astra |
| Gemini 4 Argon | 2 / 10 through 2026-11-30; 4 / 20 from 2026-12-01 (output "including thinking") | not listed | grounding $14 per 1,000 grounding queries beyond 5,000 free per month (free allowance not assumed) | https://ai.google.dev/gemini-api/docs/latest-model ; grounding: https://cloud.google.com/vertex-ai/generative-ai/pricing |

Thinking and reasoning tokens are billed as output: Anthropic ("Tokens Claude uses while thinking (billed as output tokens)"; `output_tokens` "the inclusive, authoritative total used for billing", https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost), OpenAI (reasoning tokens "billed as output tokens", https://developers.openai.com/api/docs/guides/reasoning), Google (output "including thinking"). Gemini 4 Argon is not listed on the Gemini API pricing page (https://ai.google.dev/gemini-api/docs/pricing, read 2026-11-10); its price is taken from Google's own Gemini 4 Argon page, which confirms r1's unverified $2/$10 for November and gives $4/$20 from December 1, 2026. The per-search fees are charged in full under Anthropic's Batch API (its pages state the batch discount for tokens only).

**Token basis.** Measured, not assumed, wherever a record exists: the v0.39 current arm (`osf/v39/data/v39_raw.json`, 30 calls per model × condition): list-type questions (24 calls) for Phase B and for v0.23 Phase A ("… Please be detailed and specific."); brand probes (6 calls) for the v0.19–v0.22 yes/no questions (conservative: no current-model yes/no answer is on record). Mean per call (S0 output; S1 input / output / searches): GPT-6 Astra 680; 19,773 / 821 / 1.9. Gemini 4 Argon 1,319; 233 / 1,312 / 0.4. Claude Opus 5.5 1,836; 15,006 / 1,727 / 1.0. Claude Fable 5.2 has no study-type record: its basis is Claude Opus 5.5's × 2 (central; Fable's default effort is high, Opus 5.5's medium) or × 3 (high; the one completed paired search prompt of the feasibility check gave Fable/Opus = 40,269/13,625 input tokens, 1,042/325 output tokens and 3/1 searches). Central = means, +2% for re-sends; high = every call at the 90th percentile (Fable × 3; Gemini output × 1.5 for unrecorded thinking), +10% for re-sends. Script and full basis: `osf/v42/scripts/cost_estimate_v0_42.py` → `osf/v42/prereg/cost_estimate_v0_42_r2.json` and `.txt`.

**Estimate of the r2 design** (US$, t₄ prices; central / high; cells rounded, totals from unrounded values):

| Model (mode) | Phase B S0 ×3 (90) | Phase B S1 ×3 (90) | Phase A S0 ×1 (112) | Total (292 calls) |
|---|---|---|---|---|
| Claude Fable 5.2 (Batch API) | 6.75 / 13.41 | 19.20 / 53.91 | 4.83 / 10.52 | 30.78 / 77.84 |
| GPT-6 Astra (standard) | 3.14 / 4.60 | 23.68 / 40.12 | 2.54 / 3.73 | 29.36 / 48.45 |
| Gemini 4 Argon (standard) | 1.22 / 2.36 | 1.78 / 4.81 | 0.84 / 2.17 | 3.84 / 9.34 |
| **All (876 calls)** | **11.11 / 20.37** | **44.66 / 98.84** | **8.21 / 16.42** | **63.97 / 135.62** |

Plus the v0.23 judge reserve, $0.50 (72 answers; at most about 1,500 input and 10 output tokens each on Claude Sonnet 4.5 = $0.33). At t₅/t₆ prices (Gemini 4 Argon at its listed price from 2026-12-01; other prices as read on 2026-11-10): $67.27 central, $142.60 high.

**Design trade-off** (same basis; full list in `cost_estimate_v0_42_r2.txt`):

| Design | Calls | t₄ central / high | t₅–t₆ central / high |
|---|---|---|---|
| r1 as drafted (4 models, 142 probes × S0/S1 × 3 runs, synchronous) | 3,408 | 378 / 718 | 387 / 738 |
| **r2 (adopted): N3, Fable via Batch API, Phase B S0/S1 × 3, Phase A S0 × 1** | **876** | **64 / 136** | **67 / 143** |
| r2 with Fable synchronous | 876 | 93 / 208 | 96 / 215 |
| r2 with Claude Opus 5.5 in place of Fable, synchronous | 876 | 49 / 84 | 52 / 91 |
| r2 with Claude Opus 5.5 in place of Fable, Batch API | 876 | 41 / 72 | 45 / 79 |
| r2 with Phase B S1 × 2 runs | 786 | 49 / 103 | 52 / 109 |
| r2 with Phase A S0 × 3 runs | 1,548 | 80 / 168 | 85 / 180 |

What r2 gives up, in the order the budget rule and the programme's priorities set: the second Anthropic flagship and with it `H_Version_Presence` and the C3 panel (§9 C11–C12); Phase A with search and Phase A runs 2–3 (§9 C13); Batch pricing for GPT-6 Astra (not documented for web search). What it keeps: the primary test on N3 in S0 with three runs, the search-on answers on N3 with three runs (v1.13's Grounding corpus), and the same design for t₅ and t₆.

**Guard (computed from actual usage).** `budget_v0_42.Ledger`: spend = the judge reserve + the cost of every raw line already written (its `usage_parts` at the prices above). Before any request is sent its worst case is reserved (output at the 16,384-token cap, 2,000 input tokens in S0 or 150,000 in S1, and up to 10 searches; a batch is cut to the number of requests whose worst cases fit). (i) **Hard stop:** no request is sent if spend + reservations + its worst case would exceed $100. (ii) **Pause at $80:** once spend reaches $80, no new request starts until the pre-registrant's OK is recorded (`acquire_v0_42.py --collect --approve-past-80 "<who, when>"`). (iii) **Projection pause:** after block 5 (Phase B S1, run 1), if spend + 2 × that block's actual cost exceeds $100, collection pauses before runs 2–3 of S1 and the pre-registrant decides (`--approve-projection`); the hard stop still applies. At the central estimate none of these is reached (spend after block 5 ≈ $34; projection ≈ $64). At the high estimate blocks 1–4 (the primary test and recognition) end at ≈ $37 and the projection pause stops collection before S1 runs 2–3 (projection ≈ $136). The bounds of the worst case are practical, not absolute; a request whose actual cost exceeded its reservation would be logged under MC_Budget and nothing further would be sent once spend reached $100.

---

## §5 Analysis plan

### §5.1 Coding

- **Mentions (Phase B).** Each substrate's certified function, unchanged: v0.20–v0.22, the content module's `detect_mention` (as called in `score_v41.load_wave`); v0.19, `acquire_v0_19.parse_phase_b`; v0.23, `score_v0_23.score_phase_b`. Applied to the visible answer text. In both conditions URLs are removed before matching (`https?://` addresses and the targets of Markdown links; link text is kept), so a brand counts only when the answer names it, not when a cited address contains it. Citation records are kept separately (§2.7, item 5).
- **Recognition (Phase A, S0, run 1).** v0.19–v0.22: the same yes/no parsers as at t₁–t₃. v0.23: the t₁–t₃ recognition judge (`score_v0_23.score_phase_a`, Claude Sonnet 4.5), which is coding, not acquisition; 72 judge calls (24 answers × 3 models), inside the budget (§4.5); it must finish before 2026-11-30.
- **Coder.** `osf/v42/scripts/code_t4_v0_42.py`, unchanged in r2 (git blob `2d36735d512cf9e13b74010ba5a7f655fc7de0bc`).

### §5.2 Computation

All statistics are computed by `osf/v42/scripts/score_v0_42.py`, written and tested on synthetic data before the lock (its SHA-256 is in the lock manifest), and run once after the parity gates.

### §5.3 Parity gates (before any t₄ statistic)

- **P1.** `score_v0_42.py`, run on the locked t₃ data, reproduces v0.41's t₃ k, π̂ and φ for all 112 brands exactly (`osf/v41/v41_three_wave_table.csv`).
- **P2.** The t₄ coder, applied to the t₃ raw answers, reproduces the locked t₃ mention and recognition codes exactly with URL removal switched off; with it on, any changed t₃ code is listed.
- **P3.** Probe parity (§4.1); passed at draft.

A failed gate stops scoring; the fix is logged in `osf/v42/DEVIATIONS.md` before scoring resumes.

### §5.4 Model drop rule and missing data

A model × condition with fewer than 90% of its calls answered after the re-run pass (S0: 202 calls per model; S1: 90) is excluded from that condition's panel statistics and reported. `H_Gen_Presence` and `H_Gen_Phi` need all three N3 models in S0: if any is excluded, both are UNDETERMINED (r1's fallback to C3 is gone with Claude Opus 5.5). Their S1 variant and `H_Search_Presence` use the N3 models retained in the condition(s) concerned, flagged as a reduced panel. Calls not sent because of a budget stop count as unanswered. Rates use the answered calls as the denominator; a model-run missing a Phase B answer in a substrate yields no φ for that substrate's brands in that run. No imputation.

### §5.5 Reporting

Every test, including failures and undetermined results, with per-substrate breakdowns. Results go to the t₄ paper and its OSF deposit; the run-to-run descriptives also go to the t₅ pre-registration.

---

## §6 The stored answers and the series

- **New components.** The 876 answers and their S1 search records are the t₄ corpus for Ranking (the order of brands in Phase B lists), Sentiment (how brands are described), Coverage and Grounding (sources and citations in S1). v0.42 runs none of these analyses. Each component's own pre-registration (Paper A and Paper B: v1.10 Ranking, v1.11 Sentiment, v1.12 Coverage, v1.13 Grounding) declares its use of these answers before computing anything from them. r2 keeps, for them, Phase B in both conditions on N3 with three runs (54 category answers per substrate and condition); it no longer provides Phase A with search, Phase A runs 2–3, or any Claude Opus 5.5 answer (§9 C11, C13).
- **Series.** t₅ (target 2026-12-03) and t₆ (target 2027-02-12) re-ask the same probes to the same three model IDs with the same design (§4.2), conditions, runs, call modes, call policy and budget guard, each under its own pre-registration and its own $100 budget; at the prices read on 2026-11-10 each is estimated at $67 central ($143 high), with Gemini 4 Argon at the doubled list price Google announces from 2026-12-01. Prices are re-read at each wave's pre-registration. A newer flagship released before t₅ or t₆ is added as an extra arm only if the wave still fits its $100 budget, and is never substituted. If a model is retired or changed, the series continues on the remaining models and says so. Claude Sonnet 4.5, the v0.23 recognition judge, retires on 2026-11-30, so t₅ needs a successor judge with a parity check against the t₄ codes.

---

## §7 Limitations

1. Model generation is confounded with serving settings (temperature, output cap, thinking) and with knowledge cut-off; `H_Gen_Presence` tests the bundle as a user meets it.
2. One model per provider: there is no within-provider replication at t₄ (r1's C3 panel and version contrast are removed).
3. Three runs estimate run-to-run noise only coarsely.
4. φ on three models is noisier than on six.
5. S1 answers depend on the web on the day; they are reproducible only as recorded.
6. One market and language (US English); five categories chosen in May 2026.
7. t₃ and t₄ are a few days apart, not simultaneous.
8. Claude Fable 5.2 is sent through Anthropic's Message Batches API and the other two models synchronously. The batch requests carry the same parameters as the synchronous calls; the serving path differs and is declared.
9. Recognition rests on one Phase A run per model, in S0 only.
10. Claude Fable 5.2's cost per call is estimated from Claude Opus 5.5's (no study-type record exists); if it runs at the high end, the budget guard can end the collection before S1 runs 2–3 (§4.5), which would weaken `H_Search_Presence` and the Grounding corpus, not the primary test.

---

## §8 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks questions against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Acquisition, coding and scoring are fully automated against the locked registries, and this pre-registration is locked and deposited before any t₄ call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects.

**Use of AI tools.** During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §9 Lock procedure and change log

- **r1 draft** sent to the pre-registrant on 2026-11-10 (UTC); held by him the same day (8:03 am US Central) before its lock; superseded by r2.
- **r2 draft** sent to the pre-registrant by the coordinator; it locks 24 hours after it reached him unless he objects.
- **Between sending and lock:** clarifications that change no hypothesis, threshold, panel, probe or decision rule are logged below; any other change restarts the 24 hours.
- **Lock:** refresh `LOCK_MANIFEST_v0_42.sha256` (this file, the probe file, the parity and feasibility records, the cost estimate, the export, acquisition, budget, cost-estimate and scoring scripts, the coder and their tests); commit; tag `v0.42-prereg-r1`; push branch and tag; deposit `osf/v42/prereg/` and `osf/v42/anchor/` at OSF `v42/` and verify their SHA-256 there. Only then `acquire_v0_42.py --collect`.

**Change log**

- **2026-11-10, clarifications C1–C9 (r1; no hypothesis, threshold, panel, probe or decision rule changed; found while writing and testing the scorer, before any t₄ answer exists).**
  - C1 (§5.1). v0.23 Phase B mentions are coded by the deterministic brand matching of `score_v0_23.score_phase_b`; its optional LLM elaboration step enters no v0.42 statistic and is not run (`dry_run=True`). Parity gate P2 shows the deterministic codes reproduce t₃ exactly.
  - C2 (§2.7, item 3). "The reverse" = the share of brands above the floor at t₃ that fall below it at t₄. Also reported: the share of brands below the floor at t₄ that were below it at t₃.
  - C3 (§5.4). The C3 fallback applies per condition: S0 for `H_Gen_Presence` and `H_Gen_Phi`, S1 in their S1 variants. (Superseded in r2 by C18.)
  - C4 (§2.3). Every bootstrap resample recomputes rel1, rel3, ρ_FO and ρ*; all statistics of one test share the same resamples. (Moot in r2: C12.)
  - C5 (§2.6, MC_Served). The re-run of a call served by another model happens in the collection's re-run pass; the scorer excludes any such call that remains.
  - C6 (§2.7, item 4). A refusal = a call whose finish reason or content flag marks a refusal or a safety block (Anthropic `refusal`; OpenAI refusal content; Google `SAFETY` or a blocked prompt); a non-answer = a v0.19–v0.22 Phase A answer that the yes/no parser cannot code.
  - C7 (§2.7, item 1). Recognition agreement across runs = for each brand, the share of run pairs with the same code, averaged over brands. (Not computable in r2: C13.)
  - C8 (§2.3). In the version recognition agreement, a brand with no majority (possible only when a run is missing) is left out and counted. (Moot in r2: C12.)
  - C9 (§5.3, P2). For v0.20–v0.22 the t₃ mention codes exist only as the frame sets that `score_v41.load_wave` derives from the t₃ answers; P2 compares the t₄ coder with those. "Answered" (§5.4) = status ok, non-empty text and an accepted served ID. A permutation draw counts as a hit if ρ_perm ≥ ρ_obs − 10⁻¹². Seed 420045 is recorded; no descriptive needs a random draw.
- **2026-11-10, scorer built and parity gates run on t₃ only (r1).** `code_t4_v0_42.py`, `score_v0_42.py` and 55 unit tests (all pass). P1: the scorer reproduces v0.41's t₃ k, π̂ and φ for 112 of 112 brands exactly (φ defined for 83). P2: the t₄ coder recodes all 852 t₃ answers with 0 mismatches (4,032 mention cells, 672 recognition cells; the v0.23 judge replayed from its locked t₃ outputs, not re-run); URL removal changes no t₃ code (no t₃ answer contains a URL). Records: `osf/v42/prereg/parity_P1_v0_42.json`, `parity_P2_v0_42.json`.
- **2026-11-10, revision r2 (design changes under the programme's collection budget rule; the 24 hours restart).** Trigger: the pre-registrant's hold on r1 (Nov 10, 8:03 am US Central) and the rule "at most $100 of paid model calls per paper, hard cap; this overrides any larger cap in a draft". r1's design (3,408 calls) is re-estimated at $378 central / $718 high on the basis of §4.5. No t₄ answer exists; no study probe has been sent.
  - C10 (header, §4.2, §4.5). Design: 876 calls = N3 × (Phase B × S0/S1 × 3 runs + Phase A × S0 × 1 run), collected in seven blocks (S0 first, Phase A, then S1); budget $100 with the cost table, sources, access dates and trade-off of §4.5.
  - C11 (§2.1, §4.3). One flagship per provider. Claude Opus 5.5 (the current arm) and the C3 panel are not collected; every C3 variant "reported alongside" (§2.2, §2.4, §2.5) is removed, and the Anthropic generation pair is Claude Fable 5.2 only. The one Anthropic flagship is Claude Fable 5.2 under the model rule (newest generally available, "Active (latest)", released 2026-11-09); cost does not force Claude Opus 5.5, since with the Batch API the design's central estimate ($64) stays below the $80 pause at t₄ and at t₅/t₆ prices. The alternative with Claude Opus 5.5 is costed in §4.5 ($49 central / $84 high synchronous; $41 / $72 with the Batch API).
  - C12 (§1, §2.3). `H_Version_Presence` (r1 PRIMARY: Claude Fable 5.2 vs Claude Opus 5.5, ρ* ≥ 0.80) is removed: it needs both Anthropic flagships side by side, which the budget rule excludes ("no Fable 5.2 and Opus 5.5 side by side"). Seed 420042 is retired. Smallest separate budget that would test it as r1 defined it (S0, Phase B, three runs per model, so that rel1 rests on three run pairs): inside the t₄ window, reusing t₄'s Claude Fable 5.2 answers, 90 Claude Opus 5.5 calls, $1.69 central / $2.24 high with the Batch API ($3.38 / $4.48 synchronous); as a separate study with both models, 180 calls, $8.45 / $15.65 with the Batch API. For the pre-registrant's decision list; not part of r2.
  - C13 (§2.1, §2.7, §5.1, §6). Phase A (recognition) is collected in S0, one run. No hypothesis of r1 or r2 rests on Phase A; it feeds descriptives 1–2 and the recognition share used by the component papers. Phase A with search (336 calls, $50.60 / $88.71) and Phase A runs 2–3 (672 calls, $16.39 / $32.83) do not fit beside the kept arms. Consequences: recognition agreement across runs (r1 descriptive 1, C7) is not computed; recognition is reported for S0 only; the component papers that read t₄ recognition in S1 or as a majority of three runs need their own clarification.
  - C14 (§2.2–§2.5, §4.2). Runs: Phase B keeps three runs in both conditions, the fewest that keep each kept test as specified: `H_Gen_Phi` defines φ_{b} as the mean over at least 2 of 3 defined runs; descriptive 1 (the noise floor for t₅ and t₆) needs run pairs; `H_Gen_Presence`'s thresholds were set for a three-run mean on N3, and one run would attenuate ρ_gen toward FALSIFIED at a saving of about $7 (central); `H_Search_Presence` compares three-run means in both conditions; and the Grounding corpus of v1.13 is defined on three pooled S1 runs. Two S1 runs would save $15 central (§4.5) and are the first fallback only through the projection pause.
  - C15 (§4.4). Claude Fable 5.2 is sent through Anthropic's Message Batches API (50% token price; same request parameters; web search supported in batches per Anthropic's documentation); batched retries and `pause_turn` continuation as in §4.4. GPT-6 Astra and Gemini 4 Argon stay synchronous (Batch with web search not documented by OpenAI; no Gemini 4 Argon batch price listed by Google). The output cap stays at 16,384 tokens (§4.4).
  - C16 (§4.4). Order: blocks of §4.2 (r1: per model, run 1 S0 then S1, then runs 2 and 3), so that a budget stop can only cut search-on runs.
  - C17 (§2.6, §4.5). Budget guard from actual usage: hard stop at $100, pause at $80, projection pause after S1 run 1; new manipulation check MC_Budget; the raw file records the usage and cost of every billed request.
  - C18 (§5.4). Drop rule: expected calls per model × condition are 202 (S0) and 90 (S1); if any N3 model is excluded in S0, `H_Gen_Presence` and `H_Gen_Phi` are UNDETERMINED (r1's C3 fallback, C3 above, no longer exists).
  - C19 (§4.5). r1's budget paragraph ($400, hard stop $900) is replaced. Gemini 4 Argon's price is now verified on Google's own page ($2/$10 through 2026-11-30; $4/$20 from 2026-12-01); search and grounding fees are included in the estimate and in the guard.
  - C20 (scripts). `acquire_v0_42.py` (regenerated by `_assemble_acquire_v0_42.py`): the copied v0.39 call functions and retry policy are byte-identical to r1's; the wrapper implements the r2 matrix and order, the Message Batches path (`anthropic_params`, `parse_anthropic_blocks`, `run_anthropic_batch`), per-request usage and cost, and the guard. New: `budget_v0_42.py` (prices, cost from usage, guard) and `cost_estimate_v0_42.py` (§4.5). `score_v0_42.py`: N3 only, `H_Version_Presence` and C3 removed, r2 expected counts and drop rule, calls outside the design not analysed, cost descriptive from recorded usage (SCORER_NOTES N6, N8, N12, N15). `code_t4_v0_42.py` is unchanged (git blob `2d36735d512cf9e13b74010ba5a7f655fc7de0bc`), so P2 stands; P1 is re-run by the tests. Tests: `test_score_v0_42.py` (50) and the new `test_acquire_v0_42.py` (19, local fakes only; no request leaves the machine).
  - C21 (header, §9). The lock tag keeps the name `v0.42-prereg-r1` (r1 was never locked; the coder and the acquisition guard pin that name); the text it will lock is revision r2.
  - C22 (§8, clarification). The programme's correction of record concerning the v0.19 registry's Denon unit (November 10, 2026) is added verbatim to the conflict-of-interest declaration. No registry, probe or rule changes.
  - C23 (§8, clarification). The "Use of AI tools" statement is replaced by the programme's statement of November 10, 2026, verbatim.
  - C24 (§2.2, §7, clarification). "Two to three days" between t₃ and t₄ becomes "a few days": with the r2 lock, t₄ falls after 2026-11-11 and before 2026-11-17.
