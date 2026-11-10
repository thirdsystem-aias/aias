
# AIAS™ Presence Measurement Protocol — Pre-Registration v0.45 (revision r0, draft for review)

**Study:** The t₅ wave — the t₄ wave on the newest models (v0.42) repeated, unchanged, three weeks later: short-term stability of the parts of AIAS from t₄ to t₅ (programme study #59, "short-term stability, all six parts, t₄ → t₅"), and the retest wave that v1.14 (Ranking, Stage 2), the AIAS 6.0 Preview (descriptive retests) and Grounding Paper B wait for.
**Design:** v0.42's design (pre-registration r2) repeated without change: the 142 probes of the five-substrate omnibus (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units), in a probe file byte-identical to t₄'s, asked of the same three model IDs (N3: Claude Fable 5.2 `claude-fable-5-2`, GPT-6 Astra `gpt-6-astra`, Gemini 4 Argon `gemini-4-argon`): the 30 category questions (Phase B) without search (S0), three runs; the 112 brand questions (Phase A), S0, one run; the 30 category questions with the provider's own web search (S1), three runs: 3 × (90 + 112 + 90) = 876 calls, in that order, with t₄'s decoding, call modes, call policy, budget guard and raw-record schema. Added: a successor to the v0.23 recognition judge (Claude Sonnet 4.5 retires on 2026-11-30), checked against the Sonnet 4.5 codes of t₃ and t₄ before it codes t₅ (§5.1).
**Budget:** at most US$100 of paid model calls, hard cap (programme rule, 2026-11-10), re-sends and the judge included. Estimate at t₅ prices on v0.42's token basis: $67.27 central and $142.60 high for the 876 calls, plus a $2.50 judge reserve (§4.5). At the central estimate all seven blocks fit below the $80 pause ($69.77). At the high estimate blocks 1–5 fit ($77.58) and the guard pauses before the last two search-on runs. Spend is computed from the recorded usage of every billed request; pause at $80, hard stop at $100.
**Programme position:** second wave on the newest-models panel (t₄ = v0.42, t₅ = this study, t₆ about three months after t₄). It is (i) the data of the short-term stability paper, whose tests are pre-registered here (§2); (ii) the retest wave of v1.14 Stage 2 (`H3_Retest_Reliability`, about Dec 7), which this design meets as v1.14 §6 specifies; (iii) the t₅ inputs the AIAS 6.0 Preview requires or wants (its §11.3); (iv) a stored corpus of search-on answers for Grounding Paper B's stability study (v1.13 §8).
**Protocol version:** as v0.42: recall Presence (π̂), recognition and Consistency (φ, Methodology v1.8, SSRN 6963359) as implemented in the v0.41 scorer and used by v0.42; every t₄ and t₅ statistic is computed by v0.42's own functions (`osf/v42/scripts/score_v0_42.py`, imported unchanged by `osf/v45/scripts/score_v0_45.py`).
**Lock target:** git tag `v0.45-prereg-r1` on branch `v0.45`, pushed to `origin`. **External anchor (pre-declared):** deposit of this pre-registration, the probe file, the cost estimate, the dry run, the scripts and the lock manifest at OSF `ec6wh` → `v45/prereg/`, with `v45/anchor/` naming the tag's commit, before any t₅ call. `acquire_v0_45.py --collect` refuses to run until the tag is on `origin` and the anchor file names its commit.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r0 draft, written on 2026-11-10 (between about 5 and 7 pm US Central) before any t₄ answer exists: v0.42 locks no earlier than Wed 2026-11-11 about 3 pm US Central and collects within 72 hours, ending before 2026-11-17. The hypotheses, thresholds, tests and seeds of §2 are fixed in this text, blind to t₄. No paid call was made for this draft (no feasibility check; models, status and prices were read on the vendors' pages). It locks 24 hours after it reaches the pre-registrant unless he objects (programme rule for new collections, Nov 9, 2026).
**Version number:** v0.45 is the next free phase number (branches v0.43, v0.44 and v0.62 exist; no v0.45 branch or tag on 2026-11-10). The roadmap's older list assigns "v0.45" to a Ranking × model-version study; that list's numbering is no longer followed (v0.43 and v0.44 are other studies), so its line needs updating.
**Collection window:** first call not before Thu 2026-12-03 06:00 UTC (00:00 US Central); every call within 72 hours of the first; no new request after Sun 2026-12-06 23:59:59 US Central (2026-12-07 05:59:59 UTC). One paid collection at a time on the collection machine (§4.6).
**Depends on:** t₄ (v0.42) locked, collected (tag `v0.42-acquisition-locked`), coded and scored. If t₄ is held or delayed, §4.6 says how t₅ moves.

---

## §1 Context

v0.42 declares t₄ the baseline of a series: "t₅ (target 2026-12-03) and t₆ (target 2027-02-12) re-ask the same probes to the same three model IDs with the same design (§4.2), conditions, runs, call modes, call policy and budget guard, each under its own pre-registration and its own $100 budget" (v0.42 §6). This document is t₅'s pre-registration. Five studies wait for t₅, and each states what it needs:

| Consumer | What it needs from t₅ | Source |
|---|---|---|
| Short-term stability paper (programme study #59) | every part of AIAS that both waves can measure, under one design | programme plan, Nov 9, 2026 |
| v1.14 Ranking redesign, Stage 2 | the 30 category questions verbatim (substrate, probe ID, frame and prompt identical to `osf/v42/prereg/probes_v0_42.jsonl`); the same model IDs where still available; S0; three runs; the same decoding (provider defaults, output cap 16,384 tokens), call modes and call policy; the same raw-file schema; an `-acquisition-locked` tag; a newer model only as an extra arm that does not enter its H3 | v1.14 §6, §9 |
| AIAS 6.0 Preview | required: as v1.14. Wanted (descriptive retests D6): the 112 brand questions in S0, one run, "with a successor to the v0.23 recognition judge and a parity check against the t4 codes", so that P exists at t₅; the category questions with search on, three runs, so that G\* can be retested. Not needed: a Coverage re-ask. If a block has to go, the S0 category block is kept first. | Preview §11.3 |
| Grounding (v1.13) Paper B | source-coverage stability over waves (t₄ → v0.40's search-on arm → t₅ → t₆), pre-registered in Paper B after a PASS (or a MARGINAL with the pre-registrant's decision) | v1.13 §8 |
| Coverage (v1.12) Paper B | re-asks of the Coverage probes "at t5/t6 for temporal stability", pre-registered in Paper B after a PASS | v1.12 §10 |

Two calendar facts shape the design. Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`), the v0.23 recognition judge since t₁, retires on 2026-11-30; Anthropic names `claude-sonnet-5-5` as its replacement (model deprecations page, read 2026-11-10). Gemini 4 Argon's list price doubles from 2026-12-01 ($2 / $10 to $4 / $20 per million input / output tokens; Google Cloud Vertex AI pricing page, read 2026-11-10), so t₅ costs more than t₄ for the same calls.

What t₅ adds to t₄'s design: only the successor judge, which P at t₅ needs. It adds no Coverage block (the Coverage re-ask does not fit beside t₄'s design under $100; §4.5), no Sentiment judging (that belongs to the study that scores Sentiment on the newest models, under its own budget) and no new model (§4.3).

---

## §2 Pre-registered hypotheses

### §2.1 Definitions (used by every test)

Everything in v0.42 §2.1 applies to both waves unchanged: the 112 brand units; Phase A and Phase B; k_{b,m,r}; recall Presence π̂_{b,P} = Σ_{m∈P} Σ_r k_{b,m,r} ÷ (6 · |P| · R) with the answered calls as denominator; φ by the v1.8 formula with the locked partitions and the rule "mean over the runs whose partition is defined; undefined if fewer than 2 of the 3 runs are defined"; S0 and S1; ρ_pw = Pearson's r of within-substrate average ranks centred on each substrate's mean rank, pooled over brands (v0.42 clarification C25); α = 0.05 per test, no multiplicity correction. In addition:

- **Waves.** t₄ = v0.42's answers (raw file at tag `v0.42-acquisition-locked`; coded tables and brand table at v0.42's scored commit). t₅ = this study's answers. Both waves are coded by the same coder (§5.1), and every statistic is computed by the same functions.
- **Common panel.** For a condition, the N3 models retained at both waves under v0.42's drop rule (§5.4). With three such models the panel is N3; with two, a test that allows it is computed on those two and labelled "reduced panel"; with fewer than two it is UNDETERMINED.
- **Permutation p.** One-sided; y shuffled within substrate; ρ_pw recomputed on every draw; 10,000 draws; p = (1 + #{ρ_perm ≥ ρ_obs}) ÷ 10,001 (v0.42).
- **Bootstrap.** Brands resampled with replacement within substrate; 10,000 resamples; percentile 95% interval (v0.42).
- **Seeds.** 450041 (`H_Stab_Presence`), 450043 (`H_Stab_Consistency`), 450044 (`H_Stab_Search_Presence`), 450045 (descriptives), 450046 (component legs). 450042 is not used. `H_Stab_Drift` uses an exact enumeration and no seed.
- **Verdict labels.** CONFIRMED, PARTIAL, FALSIFIED, UNDETERMINED. PARTIAL is the band between a test's confirmation and falsification thresholds (v0.42's MARGINAL), including a value at or above the confirmation threshold without significance.
- **Fixed before t₄.** Hypotheses, thresholds, tests and seeds are fixed in this r0 text, written before any t₄ answer exists. A later revision before the lock may change cost figures, the window and logistics; a change to anything in §2 restarts the 24 hours and is listed in §9.

### §2.2 PRIMARY: `H_Stab_Presence` — recall Presence holds over three weeks

**Statement.** On the same three models and the same questions, recall Presence orders brands at t₅ as it did at t₄.

**Operationalisation.** x = π̂_{b,N3,S0} at t₄; y = π̂_{b,N3,S0} at t₅ (three runs each); all 112 brands; common panel in S0.

**Test.** ρ_stab = ρ_pw(x, y); permutation p (seed 450041); bootstrap interval.

**Verdict rule.** CONFIRMED if ρ_stab ≥ 0.70 and p < 0.05 · FALSIFIED if ρ_stab < 0.50 · PARTIAL otherwise · UNDETERMINED if fewer than two N3 models are retained in S0 at both waves.

**Rationale.** 0.70 is the programme's stability bar (v0.34) and v0.42's bar for the generation contrast; 0.50 is its falsification bound. The legacy panel held per-substrate recall ρ of 0.93–0.98 over 152 days (v0.41), so the bar is not demanding for three weeks on the same models; `H_Stab_Drift` (§2.4) is the sharper test. Precision (approximate, not a verdict input): at n = 112 and ρ = 0.80 the Fisher-z 95% interval is about ±0.07.

**Reported alongside.** Per-substrate Spearman ρ; per-model ρ_pw (each model's own π̂); the level shift Δ = mean(y − x) with its bootstrap interval; v0.41's uncentred value; and the Presence score P_S0 = 100 · (C_P/3 + 2 · π̂)/3 (the definition v1.12, v1.13 and v1.14 share at t₄) at both waves with its ρ_pw. For P, the v0.23 recognition codes of both waves come from the successor judge if it passes J1 (judge held constant; §5.1); otherwise the 24 v0.23 units are left out of P.

### §2.3 SECONDARY: `H_Stab_Consistency` — Consistency holds over three weeks

**Statement.** On the same models, φ orders brands at t₅ as it did at t₄.

**Operationalisation.** x = φ_{b,N3,S0} at t₄; y = φ_{b,N3,S0} at t₅ (v0.42 §2.1); brands with φ defined at both waves. All three N3 models must be retained in S0 at both waves (φ on two models is a different quantity).

**Test.** ρ_pw; permutation p (seed 450043); bootstrap interval.

**Verdict rule.** UNDETERMINED if n < 40 or if an N3 model is dropped in S0 at either wave · CONFIRMED if ρ ≥ 0.50 and p < 0.05 · FALSIFIED if ρ < 0.30 · PARTIAL otherwise (the thresholds and n floor of v0.41's `H_Phi_LongHorizon` and v0.42's `H_Gen_Phi`).

**Reported alongside.** Partition counts (zero, saturated, defined, undefined) at both waves; the ρ_pw of C\* = 100 · (1 − φ/9), saturated brands at 100 (the Consistency score as v1.12–v1.14 define it at t₄).

### §2.4 SECONDARY: `H_Stab_Drift` — no change beyond run-to-run noise

**Statement.** For each model, a t₅ run orders brands no more differently from a t₄ run than two runs of the same wave do from each other.

**Statistic.** For model m in S0, the six runs (three per wave) give 15 run pairs; for each pair, ρ_pw of k/n (mentions over answered frames) over the brands answered in both runs. W_m = mean over the 6 within-wave pairs; X_m = mean over the 9 cross-wave pairs; D_m = W_m − X_m. D = mean of D_m over the common panel; SR = mean X_m ÷ mean W_m.

**Test (exact).** If nothing changed beyond run-to-run noise, a model's six runs are exchangeable between the waves. Every split of each model's six runs into two groups of three (20 per model; 20³ = 8,000 for three models) is enumerated, with no random draw; p_exact = the share of splits whose D is at least the observed D. The observed split and its mirror give the same D, so the smallest attainable p is 8 ÷ 8,000 = 0.001.

**Verdict rule.** UNDETERMINED if fewer than two N3 models are retained in S0 at both waves, if any run pair has no computable ρ_pw, or if the mean within-wave ρ is below 0.30 (runs too noisy to judge drift) · CONFIRMED (no drift beyond noise) if p_exact ≥ 0.05 and SR ≥ 0.90 · FALSIFIED (drift beyond noise) if p_exact < 0.05 and SR < 0.75 · PARTIAL otherwise.

**Rationale.** `H_Stab_Presence` can be CONFIRMED while the brand order still moved more than run-to-run noise; this test separates the two. SR ≥ 0.90 bounds the size of a change the test could miss; p < 0.05 with SR < 0.75 is a change a reader would notice.

**Reported alongside.** Per model: D_m, W_m, X_m, SR and the 6 × 6 run-pair matrix; rel1 and rel3 at both waves (§2.8, item 1).

### §2.5 SECONDARY: `H_Stab_Search_Presence` — the same with search on

As §2.2 with S1 in place of S0 (common panel in S1; seed 450044; the same thresholds and labels). S1 answers depend on the web on the day, so this test measures the stability of "model plus search results" over three weeks. It never changes §2.2's verdict.

### §2.6 The six parts

| Part | Score at both waves | t₄ → t₅ test | Where the verdict comes from |
|---|---|---|---|
| Presence | π̂ (and P) on N3 | `H_Stab_Presence` (PRIMARY), `H_Stab_Drift`, `H_Stab_Search_Presence` | this study |
| Consistency | φ (and C\*) on N3, S0 | `H_Stab_Consistency` | this study |
| Ranking | v1.14's R\* (modal position), S0 | v1.14 `H3_Retest_Reliability`: ρ_w(R\*_t₄, R\*_t₅), permutation and within-answer shuffle nulls; CONFIRMED iff ρ ≥ 0.50 and both p < 0.05 | carried from v1.14 Stage 2 and reported here; not re-tested (one test, one owner) |
| Grounding | v1.13's G\* on the S1 answers | component leg (below) | this study, if the leg is active; if Grounding Paper B pre-registers the same retest before t₅'s answers exist, its verdict is carried instead |
| Coverage | v1.12's Cov\* on the 75 Coverage probes | none in t₅: the Coverage re-ask does not fit the budget (§4.5) | NOT MEASURED, unless Coverage Paper B collects a re-ask; its verdict is then carried |
| Sentiment | a locked Sentiment score on the N3 answers (none is pre-registered yet; Preview §3.4) | component leg, if such a score is locked and the t₅ S0 answers are judged under that study's own budget | NOT MEASURED otherwise |

**Component legs (Grounding, Coverage, Sentiment).** Input: the component's locked score for the 112 units at t₄ and at t₅, computed by that component's locked scorer, rating floor and rated set, supplied as files whose SHA-256 is recorded. A leg is **active** if the component's Paper A gate is PASS or MARGINAL when this study is scored; otherwise its statistic is computed and reported as descriptive, with no verdict. Test: ρ_pw over the units rated at both waves; permutation p (seed 450046); bootstrap interval. Verdict: UNDETERMINED if n < 30 · CONFIRMED if ρ ≥ 0.50 and p < 0.05 · FALSIFIED if ρ < 0.30 · PARTIAL otherwise (the programme's reliability band, v1.10 and v1.14). No score at both waves: NOT MEASURED.

**No composite.** The paper reports one verdict per part as above and does not combine them.

### §2.7 Manipulation checks

- **MC_Complete, MC_Search, MC_Truncation, MC_Window:** as v0.42 §2.6, on t₅ (876 expected calls; 202 per model in S0, 90 in S1).
- **MC_Served:** as v0.42 §2.6 (a dated snapshot of the requested ID is accepted); in addition, for each model, whether the served ID at t₅ differs from t₄'s, flagged as a possible model change behind the same ID.
- **MC_Available:** before the first call, the availability record marks every N3 model available (§4.3); the script refuses otherwise.
- **MC_Probe_Parity:** the t₅ probe file equals t₄'s byte for byte, and every t₅ call's prompt equals t₄'s for its probe ID; scoring halts otherwise.
- **MC_Call_Parity:** the call functions, retry policy, Message Batches path and record builder are t₄'s; unit tests compare them with v0.42's source at commit `61515b4`.
- **MC_Gap:** median S0 call time at t₅ minus that at t₄, in days; 14 to 35 days expected; outside that range, flagged (no verdict changes).
- **MC_Judge (J1):** §5.1.
- **MC_Budget:** spend from recorded usage stays at or below $100, judge included; every pause, approval and stop is logged in `osf/v45/data/t5_budget_state.json` and reported, with the calls not sent.
- **MC_NoOverlap:** no other paid collection ran on the collection machine during the window (the script's guard refuses to start otherwise; the run log is kept).

### §2.8 Pre-registered descriptives (no verdicts)

1. Run-pair reliability rel1 and rel3 per model × condition at both waves (the noise floor), and a disattenuated per-model ρ\*_m = ρ_m ÷ √(rel3_t₄ · rel3_t₅).
2. Recognition: share of brands coded recognized per model at both waves (v0.23 with the successor judge at both waves).
3. Floor persistence: of the brands below the recall floor at t₄ (mean k per model-run < 1, S0), the share still below it at t₅; and the share above it at t₄ that fall below it at t₅.
4. Answer form at both waves: words per answer; registry brands named per Phase B answer; finish reasons; refusals and non-answers (v0.42 C6).
5. Search (S1) at both waves: searches, sources and citations per call per model; the overlap (Jaccard) of the 20 most-cited domains per model between t₄ and t₅.
6. Cost: tokens, searches and spend per model × block, from recorded usage.

---

## §3 Brand registries

Unchanged from t₁–t₄: the five omnibus registries, as t₄'s probe file and coder read them. No brand is added, removed or renamed. Each registry's conflict-of-interest handling is carried forward unchanged (§8).

---

## §4 Probes and collection

### §4.1 Probe file

`osf/v45/prereg/probes_v0_45.jsonl` is a byte copy of `osf/v42/prereg/probes_v0_42.jsonl` (142 lines: Phase A 112, Phase B 30). Both files have SHA-256 `7aa246ee1b28a9bf4f55b8a5c124f099a75bb4ca029c0e42bf2ba1459c6323aa`. Substrates, probe IDs, frame IDs, brand IDs and prompts are t₄'s; no probe carries a system prompt. t₄'s probe parity with t₃ (v0.42 §4.1) therefore carries over.

### §4.2 Design

| Block (collection order) | Phase | Condition | Run | Calls per model | Calls (N3) |
|---|---|---|---|---|---|
| 1–3 | B (30 category questions) | S0 | 1, 2, 3 | 90 | 270 |
| 4 | A (112 brand questions) | S0 | 1 | 112 | 336 |
| 5–7 | B | S1 | 1, 2, 3 | 90 | 270 |
| **Total** | | | | **292** | **876** |

Identical to v0.42 §4.2. Each call is independent (no conversation state). Blocks run in this order, the three models in parallel within a block, so the confirmatory answers (S0 category questions: `H_Stab_Presence`, `H_Stab_Consistency`, `H_Stab_Drift`, v1.14's H3) are complete first, the brand questions (P at t₅) second, and the costly search-on answers last. A budget stop can only cut search-on runs.

### §4.3 Panel, availability and the replacement rule

**Verification** (the vendors' own pages, read on 2026-11-10 between about 5:10 and 5:30 pm US Central):

| Provider | Model at t₄ and t₅ (call mode) | Status read |
|---|---|---|
| Anthropic | Claude Fable 5.2, `claude-fable-5-2` (Message Batches API) | Model deprecations page (https://platform.claude.com/docs/en/about-claude/model-deprecations): "Active"; tentative retirement "Not sooner than November 9, 2027". |
| OpenAI | GPT-6 Astra, `gpt-6-astra` (synchronous) | Model page (https://developers.openai.com/docs/models/gpt-6-astra): "Our most capable model for the most demanding work"; only `gpt-6-astra` under snapshots; no deprecation date. Deprecations page (https://developers.openai.com/api/docs/deprecations; newest entry 2026-11-10): no GPT-6 model is deprecated. |
| Google | Gemini 4 Argon, `gemini-4-argon` (synchronous) | Gemini API changelog (https://ai.google.dev/gemini-api/docs/changelog; newest entry October 30, 2026): generally available since October 13, 2026. Deprecations page (https://ai.google.dev/gemini-api/docs/deprecations): not listed. |

No newer generally available flagship was found. Google's model page (https://ai.google.dev/gemini-api/docs/latest-model, which now redirects to https://aistudio.google.com/docs/latest-model) lists Gemini 4 Carbon (`gemini-4-carbon`) beside Gemini 4 Argon. No Google page read on 2026-11-10 shows it generally available (no changelog or deprecations entry), and a secondary report (SmartScope, read the same day) describes access limited to selected cyber-defence users with no general-availability date. Under the panel rule (restricted or pre-release models are out) it is not eligible; its status is unverified on a Google page. Claude Mythos 5.2 stays excluded as restricted (v0.42 §4.3; not re-checked).

**Availability record (MC_Available).** On 2026-12-02 the coordinator reads the three vendors' model and deprecation pages again and writes `osf/v45/data/t5_availability_v0_45.json` (per model: available or not, the page, the date and time read, the quoted status). `acquire_v0_45.py --collect` refuses unless every panel model is marked available.

**Replacement rule** (applies only if a t₄ model is retired, shut down or no longer served under its ID before or during t₅):

1. A t₄ model is unavailable if its vendor's deprecation or model page shows it retired or shut down by the first t₅ call, if its calls fail with the vendor's model-not-found or retired error, or if MC_Served shows answers served by another model (not a dated snapshot of the requested ID), for example an automatic redirect of the ID to a successor.
2. Its provider's slot is filled by the replacement the vendor names on its deprecation page; if none is named, by that provider's newest generally available flagship under v0.42 §4.3's rule. The replacement is asked the t₅ design exactly (probes, conditions, runs, decoding, output cap, call policy); it uses a Batch API only if the vendor documents one for it, and for S1 only if the vendor documents its search tool in batch requests.
3. The replacement's answers enter no t₄ → t₅ test: those run on the common panel (§2.1), labelled reduced panel, and are UNDETERMINED with fewer than two common models; v1.14 applies its own rule to its H3. They are reported as a provider-continuity descriptive (ρ_pw of the replacement's π̂ at t₅ with the retired model's at t₄) and become the provider's model for t₆.
4. The replacement's price is read on its vendor's page and added to the price table before any of its calls; the guard and the block order are unchanged. If its estimate does not fit, its S1 blocks are dropped first.
5. The change is a pre-registered contingency: a DEVIATIONS entry (ex ante, before its first call), the lock manifest refreshed and re-deposited, and the pre-registrant told before the first call. The script change is limited to the panel entry and the price table.
6. A newer flagship released before t₅ while the t₄ models stay available is not added: t₅'s high estimate already exceeds $100, and v0.42 §6 allows an extra arm only if the wave still fits its budget (never as a substitute). It is recorded in the paper.

**Cheaper tiers.** Not used: the stability tests are about these three models, so a lower tier would change the question.

### §4.4 Conditions, decoding and call policy

Exactly v0.42 §4.4: S0 without tools; S1 with the provider's own web search configured as in v0.39 (Anthropic `web_search_20250305`, at most 5 uses; OpenAI Responses API `web_search`, search context size medium, sources included; Google Search grounding); temperature, top-p and reasoning effort left at provider defaults (never sent); maximum output 16,384 tokens; Claude Fable 5.2 through Anthropic's Message Batches API with the parameters of the synchronous call, GPT-6 Astra and Gemini 4 Argon synchronously; t₄'s retry policy (synchronous: v0.39's `_call_with_retry`, an empty answer re-sent once; batched: transient error types or expiry re-sent in a later batch, up to 3 attempts; `pause_turn` continued once with identical tools); one logged re-run pass inside the window; the batch journal and recovery, the one-collection guard and the window stop of v0.42 clarification C26.

`osf/v45/scripts/acquire_v0_45.py` is generated from v0.42's script (branch v0.42 at `61515b4`) by the listed text replacements of `_fork_v0_45.py`: paths (`osf/v45`), tag and anchor, batch request IDs (`v45-`), budget module, window, the availability guard, and the removal of the feasibility mode. Unit tests check that the call functions, the retry policy, the batch path and the record builder are identical to v0.42's source (MC_Call_Parity).

**Record.** `osf/v45/data/t5_raw.jsonl`, one line per attempt, with t₄'s schema (v0.42 §4.4); v1.14's Stage 2 reads it as its `--t5-raw`. Also `t5_budget_state.json` (approvals), `t5_batches.jsonl` (batch journal) and `t5_availability_v0_45.json`.

### §4.5 Budget

**Cap.** At most $100 of paid model calls for this paper, including re-sends and the judge (programme rule, 2026-11-10).

**Prices** (vendors' own pages, read again on 2026-11-10 for this draft; every value equals the one v0.42 r2 recorded the same day; machine copy in `osf/v45/scripts/budget_v0_45.py`):

| Model / item | Standard, US$ per 1M tokens in / out | Batch | Search fee | Source |
|---|---|---|---|---|
| Claude Fable 5.2 | 8 / 40 | 4 / 20 (used) | web search $10 per 1,000 searches, "plus standard token costs for search-generated content" | https://platform.claude.com/docs/about-claude/pricing |
| GPT-6 Astra | 10 / 50 | 5 / 25 (not used: t₄'s call mode is kept) | web search "$10.00 / 1k calls"; "Search content tokens billed at model rates" | https://developers.openai.com/api/docs/pricing ; https://developers.openai.com/docs/models/gpt-6-astra |
| Gemini 4 Argon | 2 / 10 promotional through 2026-11-30; **4 / 20 starting 2026-12-01** (Global) | none listed | grounding $14 per 1,000 grounding queries beyond 5,000 per month at no charge (allowance not assumed) | https://cloud.google.com/vertex-ai/generative-ai/pricing ; the AI Studio model page shows only "$2.00 / $10.00 (intro thru Nov 30)" |
| Claude Sonnet 5.5 (successor judge, first candidate) | 2 / 10 | 1 / 5 | — | https://platform.claude.com/docs/about-claude/pricing |
| Claude Sonnet 4.6 (successor judge, fallback) | 3 / 15 | 1.50 / 7.50 | — | same |

**Token basis.** Unchanged from v0.42 §4.5: measured means and 90th percentiles of v0.39's current arm (list-type questions for Phase B and v0.23 Phase A; brand probes for the v0.19–v0.22 yes/no questions); Claude Fable 5.2 at Claude Opus 5.5's basis × 2 (central) or × 3 (high); Gemini output × 1.5 at the high level for thinking tokens; re-sends +2% (central) and +10% (high). Script: `osf/v45/scripts/cost_estimate_v0_45.py` → `osf/v45/prereg/cost_estimate_v0_45_r0.json` and `.txt`.

**Estimate of the t₅ design** (US$, t₅ prices, Gemini 4 Argon at $4 / $20; central / high):

| Model (mode) | Phase B S0 ×3 (90) | Phase A S0 ×1 (112) | Phase B S1 ×3 (90) | Total (292 calls) |
|---|---|---|---|---|
| Claude Fable 5.2 (Batch API) | 6.75 / 13.41 | 4.83 / 10.52 | 19.20 / 53.91 | 30.78 / 77.84 |
| GPT-6 Astra (standard) | 3.14 / 4.60 | 2.54 / 3.73 | 23.68 / 40.12 | 29.36 / 48.45 |
| Gemini 4 Argon (standard) | 2.44 / 4.72 | 1.66 / 4.34 | 3.03 / 7.25 | 7.13 / 16.31 |
| **All (876 calls)** | **12.33 / 22.73** | **9.03 / 18.59** | **45.91 / 101.28** | **67.27 / 142.60** |

**By block, in collection order** (cumulative spend includes the $2.50 judge reserve):

| Block | Calls | Cost central / high | Cumulative central / high |
|---|---|---|---|
| 1 B-S0 run 1 | 90 | 4.11 / 7.58 | 6.61 / 10.08 |
| 2 B-S0 run 2 | 90 | 4.11 / 7.58 | 10.72 / 17.65 |
| 3 B-S0 run 3 | 90 | 4.11 / 7.58 | 14.83 / 25.23 |
| 4 A-S0 run 1 | 336 | 9.03 / 18.59 | 23.86 / 43.81 |
| 5 B-S1 run 1 | 90 | 15.30 / 33.76 | 39.16 / 77.58 |
| 6 B-S1 run 2 | 90 | 15.30 / 33.76 | 54.46 / 111.34 |
| 7 B-S1 run 3 | 90 | 15.30 / 33.76 | 69.77 / 145.10 |

**What fits under $100.** At the central estimate, all seven blocks ($69.77 with the judge reserve; below the $80 pause). At the high estimate, blocks 1–5 ($77.58): the projection rule after block 5 (spend + 2 × block 5's actual cost > $100) pauses the collection before runs 2–3 of S1 and asks the pre-registrant; collecting them would take about $67.52 more at the high estimate, which the cap does not allow. The confirmatory blocks (1–3, $25.23 high with the reserve) and the brand questions (block 4) fit in every case.

**Design trade-off** (same basis; full list in `cost_estimate_v0_45_r0.txt`):

| Design | Calls | t₅ central / high |
|---|---|---|
| **t₅ (adopted): t₄'s design repeated** | **876** | **67.27 / 142.60** |
| Blocks 1–3 only (S0 category questions: the confirmatory tests and v1.14's H3) | 270 | 12.33 / 22.73 |
| Blocks 1–4 (adds the brand questions, P at t₅) | 606 | 21.36 / 41.31 |
| S1 with two runs (blocks 1–6) | 786 | 51.96 / 108.84 |
| t₅ plus a Coverage re-ask (v1.12's 75 probes, N3, S0, three runs, Fable via Batch API) | 1,551 | 98.10 / 199.42 |
| Coverage re-ask alone, Fable via Batch API | 675 | 30.84 / 56.82 |
| Coverage re-ask alone, every model synchronous (v1.12's own call mode) | 675 | 47.72 / 90.35 |
| Claude Opus 5.5 continuity arm, S0 category questions × 3, Batch API (not adopted) | 90 | 1.69 / 2.24 |

**What does not fit, and the smallest budget for it.** (i) The Coverage re-ask: with t₅'s design it would cost $98.10 central and $199.42 high, past the $80 pause even at the central estimate. It is left to Coverage Paper B as its own collection with its own $100 cap; the smallest budget for it is $30.84 central / $56.82 high with Claude Fable 5.2 through the Batch API, or $47.72 / $90.35 in v1.12's synchronous call mode (on this token basis; v1.12's own estimate, on its own assumptions, is lower). (ii) Sentiment judging of the t₅ answers: a separate study with its own budget; the Preview's planning estimate for one wave of S0 category answers is $14.09 to $53.61 (Preview §12). (iii) Search-on runs 2–3 if the high estimate materialises: about $67.52 more, above the cap.

**Successor judge cost.** At most 288 calls per candidate (144 t₃ and 72 t₄ answers for J1, 72 t₅ answers), each at most 1,500 input and 10 output tokens: $0.89 on Claude Sonnet 5.5 and $1.34 on Claude Sonnet 4.6 if both are tried; reserve $2.50.

**Guard (computed from actual usage; unchanged from v0.42).** `budget_v0_45.Ledger`: spend = the judge reserve + the cost of every raw line already written (its `usage_parts` at the prices in force on the request's date, so Gemini 4 Argon at $4 / $20). Before a request is sent its worst case is reserved (output at the 16,384-token cap, 2,000 input tokens in S0 or 150,000 in S1, up to 10 searches; a batch is cut to the requests whose worst cases fit). (i) **Hard stop:** no request is sent if spend + reservations + its worst case would exceed $100. (ii) **Pause at $80:** once spend reaches $80, no new request starts until the pre-registrant's OK is recorded (`acquire_v0_45.py --collect --approve-past-80 "<who, when>"`). (iii) **Projection pause:** applied once, when block 5 (B-S1 run 1) is complete: if spend + 2 × that block's actual cost exceeds $100, collection pauses before runs 2–3 of S1 and the pre-registrant decides (`--approve-projection`); the hard stop still applies.

**Re-estimate from t₄.** Once v0.42's collection has ended, its recorded usage gives each model's actual cost per call in each block. Before this draft is sent (or as a logged clarification before the lock), §4.5 is re-estimated from those costs at t₅ prices. This changes figures, not the design. If the re-estimated central total with the reserve exceeds $80, the pre-registrant is asked before the lock whether to collect S1 with two runs (the default in that case) or keep three runs under the $80 pause.

### §4.6 Window, order and dependencies

- **Lock first.** The pre-registrant receives this text; at least 24 hours later it is locked and anchored (§9). Nothing is sent before.
- **Window.** First call not before Thu 2026-12-03 06:00 UTC (00:00 US Central). No new request after the earlier of 72 hours from the first recorded call and 2026-12-07 05:59:59 UTC (Sun Dec 6, 23:59:59 US Central). A request already sent completes and is recorded. Enforced by `acquire_v0_45.py`.
- **One paid collection at a time.** The script refuses to start while another `acquire_v*.py --collect` runs. The paid runs planned before t₅ (v1.12 Coverage, Nov 14–16 or Nov 22–29; v0.40, Nov 17–21; v0.44, costed in its draft for Nov 24–28; v0.62, by default Nov 29 to Dec 2; v1.11's judge batches from Nov 22) are scheduled before Dec 3; none may run during t₅'s window.
- **If t₄ is held or delayed.** t₅ stays on Dec 3 if t₄'s last call is at least 14 days earlier. Otherwise t₅ moves to 21 days after t₄'s last call (window and hard end shifted by the same amount) through a logged clarification before the lock, and the Preview takes Ranking as "retest pending" under its own §4.4 and §11.4. If t₄ is not collected at all, t₅ has no baseline and is not locked.
- **Order after the lock.** (1) After v0.42's coding: the J1 judge parity run (§5.1; at most 216 small paid calls per candidate, run when no other paid collection is running), record `osf/v45/data/judge_parity_J1_v0_45.json`. (2) Dec 2: the availability record. (3) From Dec 3: `acquire_v0_45.py --collect` under `caffeinate -w`. (4) After the last call: tag `v0.45-acquisition-locked`, pushed (v1.14 Stage 2 needs it). (5) Coding (§5.1). (6) Scoring once (§5.2). (7) v1.14 Stage 2 and the component scorers read t₅ on their own schedule; their outputs are read here when they exist (§2.6).

---

## §5 Analysis plan

### §5.1 Coding

- **Mentions, URL removal and v0.19–v0.22 recognition.** v0.42's certified coder, `osf/v42/scripts/code_t4_v0_42.py`, used unchanged (git blob `2d36735d512cf9e13b74010ba5a7f655fc7de0bc`, the pin of v0.42 §5.1; `code_t5_v0_45.py` refuses to code if the blob differs). t₄ and t₅ are therefore coded by the same functions.
- **v0.23 recognition (Phase A): successor judge.** The judge's system prompt, user template, 3,000-character truncation, R0–R3 rubric and label parser are v0.23's (`scripts/score_v0_23.py`), unchanged; only the model and, where the model requires it, the request settings change. `code_t5_v0_45.py` passes v0.23's own judge call through a client proxy:
  - **First candidate: Claude Sonnet 5.5 (`claude-sonnet-5-5`)**, Anthropic's recommended replacement for `claude-sonnet-4-5-20250929` (model deprecations page, read 2026-11-10); "Active (latest)", retirement not sooner than 2027-09-28 (model page). Its model page states that setting temperature, top_p or top_k "returns a 400 error" and that adaptive thinking is on by default; its migration guide states that `max_tokens` "covers thinking plus text" and that `thinking: {"type": "between_tools"}` is the lowest setting. v0.23's call (temperature 0.0, max_tokens 10, first content block read as text) would therefore fail on this model if only the model ID changed. The proxy sends no temperature, sends `thinking: {"type": "between_tools"}` and `output_config: {"effort": "low"}`, keeps max_tokens 10, and returns the first text block. These settings are taken from the vendor's pages and tested against local fakes only; J1 is their first real test.
  - **Fallback: Claude Sonnet 4.6 (`claude-sonnet-4-6`)**, Active, retirement not sooner than 2027-02-17 (deprecations page); runs without thinking when no thinking field is sent (migration guide). v0.23's call is sent unchanged except the model ID. Whether it accepts temperature 0.0 is not verified on a vendor page; if it does not, its calls return errors and it fails J1.
  - **J1 (judge parity), before any t₅ answer is coded.** The candidate judges the 144 t₃ v0.23 Phase A answers (Sonnet 4.5 codes locked in v0.41, `osf/v41/data/v23/v23_phase_a_scored.json`) and the 72 t₄ v0.23 Phase A answers (Sonnet 4.5 codes in v0.42's coded Phase A table). **PASS** if the binary code (recognized = R1–R3; not = R0; v0.42's `r_level_to_binary`) agrees with Sonnet 4.5's on at least 95% of all answers judged and on at least 90% of the t₄ answers, with no R_ERR left. Exact R-level agreement is reported. Candidates in order; the first that passes is the t₅ judge. `code_t5_v0_45.py --parity <model>` runs J1 (it refuses before the tag `v0.45-prereg-r1` is on `origin`) and writes every run to `osf/v45/data/judge_parity_J1_v0_45.json`; `--judge <model>` refuses to code t₅ with a model that has not passed J1.
  - **Judge held constant across waves.** The J1 winner's codes for the t₄ answers are the t₄ v0.23 recognition codes for every t₄ → t₅ comparison of P and recognition (§2.2, §2.8); v0.42's locked Sonnet 4.5 values are reported beside them.
  - **If no candidate passes J1:** v0.23 recognition is not coded at t₅; P is not computed for the 24 v0.23 units at either wave; the tests on π̂ and φ are unaffected. Reported as such.
- **Coder outputs.** `osf/v45/data/coded/{substrate}_phase_{a,b}.csv` in v0.42's format.

### §5.2 Computation

All statistics are computed by `osf/v45/scripts/score_v0_45.py`, which imports v0.42's scoring functions unchanged, was written and tested on synthetic data before the lock (its SHA-256 goes into the lock manifest), and runs once (it refuses if its output exists).

### §5.3 Gates (before any t₅ statistic)

- **G1 Probe parity.** The t₅ probe file equals t₄'s (passed at draft: equal SHA-256), and every t₅ call's prompt equals t₄'s for its probe ID (MC_Probe_Parity; checked on the raw file).
- **G2 Call parity.** The acquisition script's call functions, retry policy, batch path and record builder equal v0.42's source (unit tests; re-run at the lock).
- **G3 t₄ parity.** π̂ and φ (with partition) recomputed by `score_v0_45.py` from v0.42's coded t₄ tables equal v0.42's scored brand table exactly, N3, S0 and S1 (as v1.14's MQ8).
- **J1** gates only the v0.23 recognition codes (§5.1).

A failed G1–G3 stops scoring; the fix is logged in `osf/v45/anchor/DEVIATIONS.md` before scoring resumes.

### §5.4 Model drop rule and missing data

v0.42 §5.4 applies at each wave: a model × condition with fewer than 90% of its calls answered after the re-run pass (S0: 202 calls per model; S1: 90) is dropped from that wave's condition. Tests use the common panel (§2.1). Calls not sent because of a budget stop count as unanswered. Rates use the answered calls as the denominator; a model-run missing a Phase B answer in a substrate yields no φ for that substrate's brands in that run. No imputation.

### §5.5 Reporting

Every test, including failures and undetermined results, with per-substrate and per-model breakdowns, in the short-term stability paper and its OSF deposit. The Ranking row reports v1.14 Stage 2's verdict as carried, with its source file and SHA-256. Components not measured at t₅ are listed as such.

---

## §6 What t₅ provides to other studies

- **v1.14 Stage 2:** `osf/v45/data/t5_raw.jsonl` (t₄'s schema), `osf/v45/prereg/probes_v0_45.jsonl` (byte-identical to t₄'s) and the tag `v0.45-acquisition-locked`, all that v1.14 §6 and §9 ask for.
- **AIAS 6.0 Preview:** the required S0 category answers; the wanted brand answers with the successor judge and its parity check (J1); the wanted search-on answers in three runs (unless the projection pause stops them, §4.5).
- **Grounding Paper B:** the S1 answers with their search records (queries, sources, citations), as at t₄.
- **Sentiment:** the S0 answers, stored for a study that judges them under its own budget.
- **Coverage Paper B:** nothing; a re-ask is its own collection (§4.5).
- **t₆** (target 2027-02-12): the same design under its own pre-registration and budget; the J1 winner as the v0.23 judge (Claude Sonnet 4.6's retirement is not sooner than 2027-02-17, Claude Sonnet 5.5's not sooner than 2027-09-28).

---

## §7 Limitations

1. The same model IDs are not proof of the same models: `gpt-6-astra` and `gemini-4-argon` are undated IDs (no snapshot listed), and a vendor can change the model behind an ID between waves. MC_Served records served IDs but cannot see an undisclosed change; the tests measure stability of each model as served under its ID.
2. Three runs per wave estimate run-to-run noise coarsely; `H_Stab_Drift`'s exact test has 8,000 splits and a smallest p of 0.001.
3. S1 answers depend on the web on the day; they are reproducible only as recorded.
4. The v0.23 recognition judge changes between t₄ and t₅; J1 bounds the effect, and P is compared with one judge at both waves.
5. t₅ falls in early December (holiday season); a seasonal change in what the web says can enter S1, and t₅ cannot separate season from drift.
6. One market and language (US English); five categories chosen in May 2026.
7. Until t₄'s usage exists, the cost estimate rests on v0.39's token counts, with Claude Fable 5.2 inferred from Claude Opus 5.5's.
8. Only some of the six parts can be measured at t₅: Ranking's retest is v1.14's; Grounding's needs v1.13's gate; Coverage is not re-asked; Sentiment has no locked score on these models yet.
9. Claude Fable 5.2 is sent through the Message Batches API and the other two synchronously, as at t₄.
10. Two waves three weeks apart cannot separate short-term noise from a slow trend; t₆ (about three months) addresses that.

---

## §8 Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-asks questions against brand registries fixed in earlier phases (v0.19–v0.23); it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward unchanged. Two items of record apply. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry, AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Acquisition, coding and scoring are fully automated against the locked registries, and this pre-registration is locked and deposited before any t₅ call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded.

**Ethics.** Not applicable; no human subjects.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

---

## §9 Lock procedure and change log

- **r0 draft** (this text) written on 2026-11-10 by the AIAS runner and committed on branch `v0.45` (local; not pushed, not deposited, not sent). Before it is sent: §4.5 re-estimated from t₄'s recorded usage once v0.42's collection has ended (a logged clarification; figures only).
- **Sending.** The coordinator sends it to the pre-registrant; it locks 24 hours after it reaches him unless he objects. Recommended: send once t₄'s collection has ended (about Nov 14–16) and lock before Thanksgiving week.
- **Between sending and lock:** clarifications that change no hypothesis, threshold, test, seed, panel, probe or decision rule are logged below; any other change restarts the 24 hours.
- **Lock:** write `osf/v45/prereg/LOCK_MANIFEST_v0_45.sha256` (this file, the probe file, the cost estimate and dry run, the v0.45 scripts and tests, and the v0.42 files they import: `osf/v42/scripts/code_t4_v0_42.py`, `score_v0_42.py`, `acquire_v0_42.py` as the fork source, `scripts/score_v0_23.py`); commit; tag `v0.45-prereg-r1`; push branch and tag; write `osf/v45/anchor/osf_anchor_v0_45.json` (tag, commit, UTC time); deposit `osf/v45/prereg/` and `osf/v45/anchor/` at OSF `v45/` and verify their SHA-256 there. Only then J1 and, from Dec 3, `acquire_v0_45.py --collect`.

**Change log**

- **2026-11-10, r0.** Drafted before any t₄ answer exists. Design = v0.42 r2's, repeated; successor v0.23 judge with J1; hypotheses `H_Stab_Presence`, `H_Stab_Consistency`, `H_Stab_Drift`, `H_Stab_Search_Presence` and the component legs; prices and model status read again on the vendors' pages (§4.3, §4.5). Scripts: `_fork_v0_45.py` → `acquire_v0_45.py`; `budget_v0_45.py`; `cost_estimate_v0_45.py`; `code_t5_v0_45.py`; `score_v0_45.py`; tests `test_acquire_v0_45.py` (34) and `test_score_v0_45.py` (20): 54 of 54 pass on synthetic data and local fakes (no model request leaves the machine; one test checks that J1 refuses before the tag exists, which reads the tag list on `origin`). Dry run: `dry_run_v0_45.txt` (876 calls; nothing sent). Choices made in drafting are listed in §11.

---

## §10 Files

`osf/v45/prereg/`: `PRE_REGISTRATION_v0_45.md` (this file); `PLAIN_SUMMARY_v0_45.md`; `probes_v0_45.jsonl` and `probe_parity_v0_45.json`; `cost_estimate_v0_45_r0.json` and `.txt`; `dry_run_v0_45.txt`. `osf/v45/anchor/DEVIATIONS.md` (Entry 0, ex ante). `osf/v45/scripts/`: `_fork_v0_45.py`, `acquire_v0_45.py`, `budget_v0_45.py`, `cost_estimate_v0_45.py`, `code_t5_v0_45.py`, `score_v0_45.py`; `tests/` with `make_synthetic_t5.py`, `run_all_v0_45.py`, `test_acquire_v0_45.py`, `test_score_v0_45.py` (run as a script: `python3 osf/v45/scripts/tests/run_all_v0_45.py`; outputs under `/tmp`). Still to add before the lock: `LOCK_MANIFEST_v0_45.sha256` and `osf/v45/LOCK_STEPS.md` (the coordinator's lock steps), and the re-estimate of §4.5 from t₄'s recorded usage.

---

## §11 Choices made in drafting (for the pre-registrant; each has a recommended default)

1. **Repeat t₄ exactly** (876 calls; S0 category questions, brand questions, then search-on), the same three model IDs and call modes. Default: yes. Alternative: blocks 1–4 only ($21.36 central / $41.31 high), which loses the Grounding retest and the search-on stability test.
2. **No Coverage re-ask in t₅.** It does not fit beside t₄'s design ($98.10 central with it). Default: leave it to Coverage Paper B as its own collection after v1.12's gate ($30.84 / $56.82 with Fable through the Batch API). Alternative: drop the search-on blocks to make room (not recommended: the Preview and Grounding want them).
3. **Successor v0.23 judge.** Default: Claude Sonnet 5.5 (Anthropic's named replacement), with the request settings its pages require, then Claude Sonnet 4.6 as fallback, each passing J1 (≥ 95% binary agreement, ≥ 90% on t₄) before coding t₅.
4. **Newer flagship before Dec 3.** Default: not added (no budget room); recorded in the paper.
5. **Window.** Default: from Thu Dec 3, 00:00 US Central, at most 72 hours, hard end Sun Dec 6, 23:59 US Central.
6. **If the high estimate materialises.** Default: the projection pause after search-on run 1 stops the collection and asks you, as at t₄. Alternative: decide now to skip search-on runs 2–3 without asking.
7. **If t₄'s actual cost puts t₅'s central estimate above $80.** Default: search-on with two runs (G\* at t₅ then pools two runs, flagged). Alternative: three runs, with your OK at the $80 pause.
8. **Thresholds.** Default: the programme's bars (Presence 0.70 / 0.50; Consistency 0.50 / 0.30, n ≥ 40; components 0.50 / 0.30, n ≥ 30), with `H_Stab_Drift` as the stricter test for three weeks.
