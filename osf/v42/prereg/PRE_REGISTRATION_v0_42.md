# AIAS™ Presence Measurement Protocol — Pre-Registration v0.42 (revision r1, draft for review)

**Study:** The t₄ wave on the newest models — model-version and cross-generation stability of AIAS Presence and Consistency, and the baseline of the t₄ → t₅ → t₆ series.
**Design:** Re-asks, verbatim, the 142 questions of the five-substrate omnibus (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units) to the newest generally available flagship model of each provider and to the current arm, each without and with the provider's own web search, three independent runs per question: 4 models × 2 conditions × 3 runs × 142 questions = 3,408 calls. Compares the answers with the t₃ wave on the retiring six-model panel, collected on 2026-11-09 (v0.41), two to three days earlier.
**Programme position:** First wave on the programme's next reference panel. It is (i) the model-version study of the plan (study list #56 and #58), (ii) the baseline of the short-term (t₅, about +3 weeks) and three-month (t₆) stability waves, and (iii) a stored corpus of answers for the four new components (Ranking, Sentiment, Coverage, Grounding), whose analyses are pre-registered in their own papers (§6).
**Protocol version:** Recall Presence (π̂), recognition and Consistency (φ, Methodology v1.8, SSRN 6963359) as locked for the omnibus and implemented in the v0.41 scorer (`osf/v41/scripts/score_v41.py`; v0.41, SSRN 7685100). Mention detection and recognition coding by each substrate's certified t₁ functions (§5.1).
**Lock target:** git tag `v0.42-prereg-r1` on branch `v0.42`, pushed to `origin`. **External anchor (pre-declared):** deposit of this pre-registration, the probe file, the parity and feasibility records, the scripts and the lock manifest at OSF `ec6wh` → `v42/prereg/`, with `v42/anchor/` naming the tag's commit, before any study probe is sent. `acquire_v0_42.py --collect` refuses to run until the tag is on `origin` and the anchor file exists.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r1 draft, sent to the pre-registrant for review on 2026-11-10 UTC (Nov 9, late evening, US Central) and deposited on OSF at `v42/prereg/draft/`. Locks 24 hours after it reached him unless he objects (programme rule for new collections, Nov 9, 2026). No study probe has been sent.
**Pre-lock feasibility check (non-acquisition):** on 2026-11-10 at 05:13 UTC each of the four models received the neutral prompt "Reply with the single word: ready" without tools, and the two neutral search-enabled prompts of v0.39 (today's date in UTC; the current top headline on bbc.com) with its provider's web search. 11 of 12 calls returned ok, and every model served its requested ID (`claude-fable-5-2`, `claude-opus-5-5`, `gpt-6-astra`, `gemini-4-argon`). Claude Fable 5.2 ended the headline prompt with an empty answer after a tool call (finish reason `tool_use`) despite the script's one retry; a single diagnostic re-send of the same neutral prompt, outside the record, ended normally after 4 searches. Gemini 4 Argon answered the date prompt without searching. Record: `osf/v42/prereg/feasibility_v0_42.json`. No study probe was sent.
**Collection window:** after the lock; all 3,408 calls within 72 hours. It must not overlap v0.40's collection (2026-11-17 to 2026-11-21): one paid collection at a time on the collection machine. The v0.23 recognition coding uses Claude Sonnet 4.5 and must finish before that model's scheduled retirement on 2026-11-30.

---

## §1 Context

The six-model panel used since v0.17 is retiring: Claude Opus 4.5 not sooner than 2026-11-24, Claude Sonnet 4.5 on 2026-11-30, the GPT-4o and GPT-4o mini snapshots on 2027-01-14 (`osf/v40/registries/model_cutoffs.csv`). v0.41 took its last wave (t₃) on 2026-11-09. Over the 152 days from t₂ to t₃ both components held on that panel: recall Presence ρ = 0.93–0.98 in all five substrates, and φ ρ = 0.681 (n = 80). From now on every new collection runs on current models.

Three questions follow before the programme builds its next components on those models:

1. **Generation.** Does the ordering of brands by AI availability carry over from the 2024–25 model generation to the 2026 generation? If it does, the programme's record on the legacy panel can be bridged to the new panel; if it does not, the new panel starts its own series.
2. **Version.** Within one provider, do two current model versions order brands alike, once each model's run-to-run noise is allowed for?
3. **Series.** How much do the new models' answers vary from run to run? That noise floor is what the t₅ and t₆ stability waves will be judged against.

Panel rule (Pablo, Nov 9, 2026): the newest generally available flagship model of each provider (Anthropic, OpenAI, Google), verified from the vendor's own model documentation when the pre-registration is written, alongside the current arm (since v0.38) for continuity; restricted or pre-release models are out. §4.3 records the verification.

---

## §2 Pre-registered hypotheses

### §2.1 Definitions (used by every test)

- **Brand units.** The 112 brands of the five omnibus registries (16 + 24 + 24 + 24 + 24), unchanged from t₁–t₃.
- **Phase B (recall).** Six category questions per substrate (30 in all). **Phase A (recognition).** One question per brand (112).
- **k_{b,m,r}.** Number of the six Phase B questions of brand b's substrate in which model m's answer in run r mentions b (§5.1). At t₃: one run, the locked v0.41 counts (`osf/v41/v41_three_wave_table.csv`, column `k_per_model`, wave t3).
- **Recall Presence** of brand b on panel P: π̂_{b,P} = Σ_{m∈P} Σ_r k_{b,m,r} ÷ (6 · |P| · R), with R runs. At t₃ (P = L6, R = 1) this is the locked v0.41 `pi_hat`. Rates use the answered calls as the denominator (§5.4).
- **Consistency.** φ_{b,P,r} = the v1.8 formula on panel P in run r, φ = [1/(M − 1)] · Σ_m (k_m − 6π̂)² ÷ [6π̂(1 − π̂)] with M = |P| and π̂ the run's recall rate, with the locked partitions (π̂ = 0 → zero; π̂ = 1 → saturated; otherwise defined) and the v0.41 reduced-panel kernel `phi_m`. Higher φ = less consistent. At t₄, φ_{b,P} = the mean of φ_{b,P,r} over the runs whose partition is defined; undefined if fewer than 2 of the 3 runs are defined. At t₃: the locked v0.41 `phi` (defined partition only).
- **Panels.** L6 = the six legacy models at t₃ (Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o mini, Gemini 2.5 Flash, Gemini 2.5 Flash-Lite). N3 = the newest generally available flagship of each provider: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon. C3 = the current arm: Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon. GPT-6 Astra and Gemini 4 Argon belong to both N3 and C3 (§4.3).
- **Conditions.** S0 = no tools; S1 = the provider's own web search (§4.4).
- **ρ_pw(x, y).** Pooled within-substrate Spearman correlation: values ranked within substrate (average ranks for ties), then Pearson's r of those ranks over all brands pooled (`pooled_within_rho` in `score_v41.py`).
- **Permutation p.** One-sided; y shuffled within substrate; ρ_pw recomputed on each draw exactly as observed (within-substrate ranks); 10,000 draws; p = (1 + #{ρ_perm ≥ ρ_obs}) ÷ 10,001.
- **Bootstrap.** Brands resampled with replacement within substrate; 10,000 resamples; percentile 95% interval.
- **Seeds.** 420041 (H_Gen_Presence), 420042 (H_Version_Presence), 420043 (H_Gen_Phi), 420044 (H_Search_Presence), 420045 (descriptives).
- **α.** 0.05 per test, no multiplicity correction; verdicts rest on pre-set effect-size thresholds, and every test is reported.

### §2.2 PRIMARY: `H_Gen_Presence` — Presence carries over to the new model generation

**Statement.** On the newest models (N3, S0, t₄), recall Presence orders brands as it did on the retiring panel (L6, t₃) two to three days earlier.

**Operationalisation.** x = π̂_{b,L6} at t₃; y = π̂_{b,N3,S0} at t₄; all 112 brands.

**Test.** ρ_gen = ρ_pw(x, y); permutation p (seed 420041); bootstrap interval.

**Verdict rule.** CONFIRMED if ρ_gen ≥ 0.70 and p < 0.05 · FALSIFIED if ρ_gen < 0.50 · MARGINAL otherwise.

**Rationale.** 0.70 is the programme's stability bar (v0.34). The legacy panel held 0.93–0.98 over five months (v0.41), so a value below 0.70 across two days is attributable to the change of model generation, not to time. Below 0.50 the two generations order brands too differently for the legacy record to be bridged quantitatively, and the new panel starts its own series. Thresholds are set before any t₄ answer exists; the t₃ values are already published.

**Reported alongside.** Per-substrate ρ; the same test with C3 in place of N3, and with S1 in place of S0; per-provider generation pairs, each the ρ_pw between the provider's two legacy models pooled and its new model (Anthropic: Claude Opus 4.5 + Claude Sonnet 4.5 → Claude Fable 5.2, and → Claude Opus 5.5; OpenAI: GPT-4o + GPT-4o mini → GPT-6 Astra; Google: Gemini 2.5 Flash + Flash-Lite → Gemini 4 Argon); the level shift Δ = mean(y − x) with its bootstrap interval.

### §2.3 PRIMARY: `H_Version_Presence` — Presence does not depend on the model version within a provider

**Statement.** Two current versions of one provider's model, Claude Fable 5.2 (released 2026-11-09) and Claude Opus 5.5, order brands by recall Presence alike once each model's run-to-run noise is allowed for.

**Operationalisation.** S0. y_{b,m} = Σ_r k_{b,m,r} ÷ 18 for m ∈ {Claude Fable 5.2, Claude Opus 5.5}. Run reliability of model m: rel1_m = the mean of ρ_pw over the three run pairs of k_{b,m,r} ÷ 6; rel3_m = 3 · rel1_m ÷ (1 + 2 · rel1_m) (Spearman–Brown, three-run mean).

**Test.** ρ_FO = ρ_pw(y_Fable, y_Opus); disattenuated ρ* = ρ_FO ÷ √(rel3_Fable · rel3_Opus); bootstrap intervals for both (seed 420042). ρ* is reported and judged as computed (not capped at 1).

**Verdict rule.** UNDETERMINED if rel1 ≤ 0.20 for either model (its runs agree too little to judge versions) · CONFIRMED (version-invariant) if ρ* ≥ 0.80 and ρ_FO ≥ 0.60 · FALSIFIED (version-dependent) if ρ* < 0.60 · MARGINAL otherwise.

**Reported alongside.** The same with S1; recognition agreement between the two versions (share of brands coded alike in a majority of runs). OpenAI and Google had no newer flagship than the current arm at verification (§4.3), so this contrast exists for Anthropic only.

### §2.4 SECONDARY: `H_Gen_Phi` — Consistency carries over to the new model generation

**Statement.** On the newest models (N3, S0, t₄), φ orders brands as it did on the retiring panel at t₃.

**Operationalisation.** x = φ_{b,L6} at t₃; y = φ_{b,N3,S0} at t₄ (§2.1); brands with φ defined on both.

**Test.** ρ_pw; permutation p (seed 420043); bootstrap interval.

**Verdict rule.** UNDETERMINED if n < 40 · CONFIRMED if ρ ≥ 0.50 and p < 0.05 · FALSIFIED if ρ < 0.30 · MARGINAL otherwise (the thresholds and n floor of v0.41's `H_Phi_LongHorizon`).

**Declared.** φ on three models carries less information per brand than on six; that is why this test is secondary.

**Reported alongside.** The same with C3; mean-independence on N3 and C3 (|ρ_pw(φ, π̂)|, flagged if ≥ 0.50, the v1.7 ceiling); partition counts (zero, saturated, defined) per panel and condition.

### §2.5 SECONDARY: `H_Search_Presence` — what web search does to Presence

**Statement (two-sided question).** Turning on each provider's web search leaves the Presence ordering of brands intact.

**Operationalisation.** N3; x = π̂_{b,N3,S0}; y = π̂_{b,N3,S1}.

**Statistic.** ρ_S = ρ_pw(x, y) with its bootstrap interval (seed 420044); level shift Δ = mean(y − x) with its interval.

**Reading (pre-declared labels; no confirm or falsify).** Search-robust if the interval's lower bound ≥ 0.80 · search-dominated if its upper bound < 0.50 · search-sensitive otherwise.

**Reported alongside.** Per model and per substrate; the same for C3.

### §2.6 Manipulation checks

- **MC_Complete.** At least 98% of the 3,408 calls end with non-empty answer text after the retry policy (§4.4). A model × condition below 90% triggers the model drop rule (§5.4).
- **MC_Served.** Every served model ID equals the requested ID (a dated snapshot of it is recorded and accepted). Any other ID: the call is excluded and re-run, and logged.
- **MC_Search.** Share of S1 calls with at least one web search, per model. Below 25% flags that model's S1 as "search rarely used" in every S1 result.
- **MC_Truncation.** Share of calls that end at the output cap, per model × condition; above 5% is flagged.
- **MC_Window.** First and last call times; all calls within 72 hours.
- **MC_Parity.** Gates P1–P3 (§5.3) pass before any t₄ statistic is computed.

### §2.7 Pre-registered descriptives (no verdicts)

1. Run-to-run reliability per model × condition: rel1 and rel3 of recall; recognition agreement across runs. These are the noise floor for t₅.
2. Recognition: share of brands coded as recognized, per model × condition, beside each legacy model at t₃.
3. Floor persistence: of the brands below v0.41's recall floor at t₃ (mean k per model < 1), the share still below it on N3, S0, at t₄ (mean k per model-run < 1); and the reverse.
4. Answer form: words per answer; registry brands named per Phase B answer; finish reasons; non-answers (a v0.19–v0.22 Phase A answer with no yes or no; refusals).
5. Search (S1): searches, sources and citations per call; share of answers with at least one citation; the 20 most-cited domains per model.
6. Cost: tokens and estimated spend per model × condition.

---

## §3 Brand registries

Unchanged from t₁–t₃: the five omnibus registries and their probe artefacts, SHA-256-checked against the v0.41 acquisition manifest (8 of 8 match; `osf/v42/prereg/probe_parity_v0_42.json`). No brand is added, removed or renamed. Each registry's conflict-of-interest handling is carried forward unchanged (§8).

---

## §4 Probes and collection

### §4.1 Probe file

`osf/v42/prereg/probes_v0_42.jsonl`: 142 lines (Phase A 112, Phase B 30), built by `osf/v42/scripts/export_probes_v0_42.py`, which runs each legacy runner's own prompt-building code with the provider call stubbed out (no prompt is retyped). No probe carries a system prompt. Phase A for v0.19–v0.22 asks whether a named brand is commonly recognized as a brand of the category and asks for yes or no (for example, "Is the brand Mercedes-Benz commonly recognized as a car brand? Answer yes or no."); Phase A for v0.23 asks an open question about the brand. Phase B asks six category questions per substrate (for v0.19–v0.22 the first is of the form "What are the best skincare brands? List several with descriptions."; v0.23 uses three expert-acclaim frames, EA-1 to EA-3, and three cultural-community frames, CC-1 to CC-3).

**Parity with t₃** (`probe_parity_v0_42.json`): for v0.20–v0.23 every prompt recorded at t₃ (720 of 720 records) equals the exported prompt byte for byte. v0.19 recorded no prompt text at t₃; its parity rests on the artefact checksums (8 of 8 match) and on the query IDs (the 132 recorded IDs equal the artefact's).

### §4.2 Design

4 models × 2 conditions × 3 runs × 142 probes = 3,408 calls. Each call is independent (no conversation state carried between calls).

### §4.3 Panel (verified on 2026-11-10 from each vendor's own documentation)

| Provider | Newest generally available flagship (N3) | Current arm (C3, since v0.38) | Verification |
|---|---|---|---|
| Anthropic | Claude Fable 5.2, `claude-fable-5-2` | Claude Opus 5.5, `claude-opus-5-5` | Claude Fable 5.2 model page (platform.claude.com): status "Active (latest)", released November 9, 2026, retirement not sooner than November 9, 2027. Claude Mythos 5.2, with the same capabilities, is available only to organizations verified through Anthropic's verification programs: restricted, so excluded. |
| OpenAI | GPT-6 Astra, `gpt-6-astra` | GPT-6 Astra, `gpt-6-astra` | GPT-6 Astra model page (developers.openai.com): "Our most capable model for the most demanding work"; the latest-model guide lists GPT-6.1 Sol ("Balanced speed, cost, and intelligence") and GPT-6.1 Terra ("Fast and efficient") below it. No dated snapshot is listed. |
| Google | Gemini 4 Argon, `gemini-4-argon` | Gemini 4 Argon, `gemini-4-argon` | Gemini API changelog: "Gemini 4 Argon (`gemini-4-argon`) generally available (GA)" on October 13, 2026; model page lists it as stable; no newer stable model listed. |

**Note on the candidate list.** The plan of Nov 9 named GPT-6.1 Terra as OpenAI's candidate. OpenAI's own documentation places GPT-6.1 Terra two tiers below GPT-6 Astra, so the rule ("the newest generally available flagship") selects GPT-6 Astra. N3 and C3 therefore share two models, and the within-provider version contrast exists for Anthropic only.

### §4.4 Conditions, decoding and call policy

- **S0:** no tools. **S1:** the provider's own web search, configured exactly as in v0.39 (Anthropic `web_search_20250305`, at most 5 uses; OpenAI Responses API `web_search`, search context size medium, sources included; Google Search grounding). S1 records every search query, consulted source and citation.
- **Decoding.** Temperature, top-p and reasoning effort are left at provider defaults. Claude Fable 5.2 accepts no temperature, top-p or top-k; its adaptive thinking is always on (default effort high). Maximum output 16,384 tokens (the v0.38–v0.40 current-arm cap).
- **Order.** One worker per model, the four in parallel; within a model: run 1 (S0 then S1, probes in file order), then run 2, then run 3.
- **Retries.** Transient errors and empty answers are retried under the v0.39 policy (`_call_with_retry`); an Anthropic `pause_turn` is continued once with identical tools. Calls still failing after the main pass get one logged re-run pass inside the window. The run is resumable; every attempt is logged.
- **Legacy settings that do not carry over (declared).** The t₁–t₃ runners used temperature 0.0 where they set it, output caps of 64 to 2,048 tokens, no tools, and, for v0.19–v0.22, the deprecated `google.generativeai` SDK (`probe_parity_v0_42.json`). The generation contrast is therefore a contrast of model generation together with its default serving settings, as a user meets it.
- **Artefact.** `osf/v42/data/t4_raw.jsonl`, one line per call: call ID, substrate, phase, probe ID, brand or frame ID, requested and served model, condition, run, prompt, answer text, finish reason, input, output and thinking tokens where reported, S1 search record (queries, sources, citations, errors), pause continuation, start and end times (UTC), error, attempt count.

### §4.5 Budget

Estimated at about US$400 at the vendors' list prices (plausible range $250–700), plus per-search tool fees. Basis: the v0.39 current-arm token means per call (Claude Opus 5.5: S1 ≈ 14,800 input and 1,600 output tokens; GPT-6 Astra: S1 ≈ 19,200 input and 750 output) and the Claude Fable 5.2 feasibility call (≈ 40,000 input tokens for one searched prompt), at the list prices on the vendors' model pages of $8/$40 (Fable 5.2), $4/$20 (Opus 5.5) and $10/$50 (GPT-6 Astra) per million input/output tokens. Gemini 4 Argon's price is not on Google's pricing page as read on 2026-11-10; the estimate uses $2/$10 as reported elsewhere (unverified), which puts Gemini at about $10 of the total because its searched answers carried only about 230 input tokens at v0.39. The estimate leans high: 88 of the 142 questions (Phase A for v0.19–v0.22) ask for a yes or no. **Hard stop:** if the running estimate passes $900, collection pauses and the pre-registrant is asked before anything else is spent.

---

## §5 Analysis plan

### §5.1 Coding

- **Mentions (Phase B).** Each substrate's certified function, unchanged: v0.20–v0.22, the content module's `detect_mention` (as called in `score_v41.load_wave`); v0.19, `acquire_v0_19.parse_phase_b`; v0.23, `score_v0_23.score_phase_b`. Applied to the visible answer text. In both conditions URLs are removed before matching (`https?://` addresses and the targets of Markdown links; link text is kept), so a brand counts only when the answer names it, not when a cited address contains it. Citation records are kept separately (§2.7, item 5).
- **Recognition (Phase A).** v0.19–v0.22: the same yes/no parsers as at t₁–t₃. v0.23: the t₁–t₃ recognition judge (`score_v0_23.score_phase_a`, Claude Sonnet 4.5), which is coding, not acquisition; it must finish before 2026-11-30.

### §5.2 Computation

All statistics are computed by `osf/v42/scripts/score_v0_42.py`, written and tested on synthetic data before the lock (its SHA-256 is in the lock manifest), and run once after the parity gates.

### §5.3 Parity gates (before any t₄ statistic)

- **P1.** `score_v0_42.py`, run on the locked t₃ data, reproduces v0.41's t₃ k, π̂ and φ for all 112 brands exactly (`osf/v41/v41_three_wave_table.csv`).
- **P2.** The t₄ coder, applied to the t₃ raw answers, reproduces the locked t₃ mention and recognition codes exactly with URL removal switched off; with it on, any changed t₃ code is listed.
- **P3.** Probe parity (§4.1); passed at draft.

A failed gate stops scoring; the fix is logged in `osf/v42/DEVIATIONS.md` before scoring resumes.

### §5.4 Model drop rule and missing data

A model × condition with fewer than 90% of its calls answered after the re-run pass is excluded from that condition's panel statistics and reported. `H_Gen_Presence` and `H_Gen_Phi` need all three N3 models: if Claude Fable 5.2 is excluded, C3 replaces N3 (declared fallback); if GPT-6 Astra or Gemini 4 Argon is excluded, both hypotheses are UNDETERMINED. `H_Version_Presence` needs both Claude models. Rates use the answered calls as the denominator; a model-run missing a Phase B answer in a substrate yields no φ for that substrate's brands in that run. No imputation.

### §5.5 Reporting

Every test, including failures and undetermined results, with per-substrate breakdowns. Results go to the t₄ paper (model-version study) and its OSF deposit; the run-to-run descriptives also go to the t₅ pre-registration.

---

## §6 The stored answers and the series

- **New components.** The 3,408 answers and their S1 search records are the t₄ corpus for Ranking (the order of brands in Phase B lists), Sentiment (how brands are described), Coverage and Grounding (sources and citations in S1). v0.42 runs none of these analyses. Each component's own pre-registration (Paper A and Paper B: v1.10 Ranking, v1.11 Sentiment, v1.12 Coverage, v1.13 Grounding) declares its use of these answers before computing anything from them.
- **Series.** t₅ (target 2026-12-03) and t₆ (target 2027-02-12) re-ask the same 142 probes to the same four model IDs, with the same conditions, runs and call policy, each under its own pre-registration. A newer flagship released before t₅ or t₆ is added as an extra arm, never substituted. If a model is retired or changed, the series continues on the remaining models and says so. Claude Sonnet 4.5, the v0.23 recognition judge, retires on 2026-11-30, so t₅ needs a successor judge with a parity check against the t₄ codes.

---

## §7 Limitations

1. Model generation is confounded with serving settings (temperature, output cap, thinking) and with knowledge cut-off; `H_Gen_Presence` tests the bundle as a user meets it.
2. N3 and C3 share two models, so they are not independent replications.
3. Three runs estimate run-to-run noise only coarsely.
4. φ on three models is noisier than on six.
5. S1 answers depend on the web on the day; they are reproducible only as recorded.
6. One market and language (US English); five categories chosen in May 2026.
7. t₃ and t₄ are two to three days apart, not simultaneous.

---

## §8 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks questions against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Acquisition, coding and scoring are fully automated against the locked registries, and this pre-registration is locked and deposited before any t₄ call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects.

**Use of AI tools.** The author used Anthropic's Claude to assist with analysis code, drafting and editing of text, and figure production. The study design, pre-registered hypotheses and decision rules, and all interpretations are the author's; the author reviewed all content and takes full responsibility for it.

---

## §9 Lock procedure and change log

- **r1 draft** sent to the pre-registrant on 2026-11-10. It locks 24 hours after it reached him unless he objects.
- **Between sending and lock:** clarifications that change no hypothesis, threshold, panel, probe or decision rule are logged below; any other change restarts the 24 hours.
- **Lock:** refresh `LOCK_MANIFEST_v0_42.sha256` (this file, the probe file, the parity and feasibility records, the export, acquisition and scoring scripts and their tests); commit; tag `v0.42-prereg-r1`; push branch and tag; deposit `osf/v42/prereg/` and `osf/v42/anchor/` at OSF `v42/` and verify their SHA-256 there. Only then `acquire_v0_42.py --collect`.

**Change log**

- **2026-11-10, clarifications C1–C9 (no hypothesis, threshold, panel, probe or decision rule changed; found while writing and testing the scorer, before any t₄ answer exists).**
  - C1 (§5.1). v0.23 Phase B mentions are coded by the deterministic brand matching of `score_v0_23.score_phase_b`; its optional LLM elaboration step enters no v0.42 statistic and is not run (`dry_run=True`). Parity gate P2 shows the deterministic codes reproduce t₃ exactly.
  - C2 (§2.7, item 3). "The reverse" = the share of brands above the floor at t₃ that fall below it at t₄. Also reported: the share of brands below the floor at t₄ that were below it at t₃.
  - C3 (§5.4). The C3 fallback applies per condition: S0 for `H_Gen_Presence` and `H_Gen_Phi`, S1 in their S1 variants.
  - C4 (§2.3). Every bootstrap resample recomputes rel1, rel3, ρ_FO and ρ*; all statistics of one test share the same resamples.
  - C5 (§2.6, MC_Served). The re-run of a call served by another model happens in the collection's re-run pass; the scorer excludes any such call that remains.
  - C6 (§2.7, item 4). A refusal = a call whose finish reason or content flag marks a refusal or a safety block (Anthropic `refusal`; OpenAI refusal content; Google `SAFETY` or a blocked prompt); a non-answer = a v0.19–v0.22 Phase A answer that the yes/no parser cannot code.
  - C7 (§2.7, item 1). Recognition agreement across runs = for each brand, the share of run pairs with the same code, averaged over brands.
  - C8 (§2.3). In the version recognition agreement, a brand with no majority (possible only when a run is missing) is left out and counted.
  - C9 (§5.3, P2). For v0.20–v0.22 the t₃ mention codes exist only as the frame sets that `score_v41.load_wave` derives from the t₃ answers; P2 compares the t₄ coder with those. "Answered" (§5.4) = status ok, non-empty text and an accepted served ID. A permutation draw counts as a hit if ρ_perm ≥ ρ_obs − 10⁻¹². Seed 420045 is recorded; no descriptive needs a random draw.
- **2026-11-10, scorer built and parity gates run on t₃ only.** `code_t4_v0_42.py`, `score_v0_42.py` and 55 unit tests (all pass). P1: the scorer reproduces v0.41's t₃ k, π̂ and φ for 112 of 112 brands exactly (φ defined for 83). P2: the t₄ coder recodes all 852 t₃ answers with 0 mismatches (4,032 mention cells, 672 recognition cells; the v0.23 judge replayed from its locked t₃ outputs, not re-run); URL removal changes no t₃ code (no t₃ answer contains a URL). Records: `osf/v42/prereg/parity_P1_v0_42.json`, `parity_P2_v0_42.json`.
