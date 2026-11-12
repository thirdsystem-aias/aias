
# AIAS™ Presence Measurement Protocol — Pre-Registration v0.45 (revision r1, draft for review)

**Study:** The t₅ wave — the t₄ wave on the newest models (v0.42) repeated, unchanged, three weeks later: short-term stability of the parts of AIAS from t₄ to t₅ (programme study #59, "short-term stability, all six parts, t₄ → t₅"), and the retest wave that v1.14 (Ranking, Stage 2), the AIAS 6.0 Preview (descriptive retests) and Grounding Paper B wait for.
**Design:** v0.42's design (pre-registration r2) repeated without change: the 142 probes of the five-substrate omnibus (v0.19 audiophile headphones, v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits; 112 brand units), in a probe file byte-identical to t₄'s, asked of the same three model IDs (N3: Claude Fable 5.2 `claude-fable-5-2`, GPT-6 Astra `gpt-6-astra`, Gemini 4 Argon `gemini-4-argon`): the 30 category questions (Phase B) without search (S0), three runs; the 112 brand questions (Phase A), S0, one run; the 30 category questions with the provider's own web search (S1), three runs: 3 × (90 + 112 + 90) = 876 calls, in that order, with t₄'s decoding, call modes, call policy, budget guard and raw-record schema. Added: a successor to the v0.23 recognition judge (Claude Sonnet 4.5 retires on 2026-11-30), checked against the Sonnet 4.5 codes of t₃ and t₄ before it codes t₅ (§5.1).
**Budget:** at most US$100 of paid model calls, hard cap (programme rule, 2026-11-10), re-sends and the judge included. Estimate (r1) from t₄'s recorded usage (876 calls, $67.46 at t₄'s prices) re-priced at t₅'s prices: $70.40 central and $149.55 conservative high for the 876 calls, plus a $2.50 judge reserve (§4.5). At the central estimate all seven blocks fit below the $80 pause ($72.90 with the reserve; the pause would be reached only if t₅'s calls cost about 10% more than t₄'s at t₅ prices). At the high estimate blocks 1–5 fit ($71.86) and the projection rule pauses before the last two search-on runs. Spend is computed from the recorded usage of every billed request; pause at $80, hard stop at $100.
**Programme position:** second wave on the newest-models panel (t₄ = v0.42, t₅ = this study, t₆ about three months after t₄). It is (i) the data of the short-term stability paper, whose tests are pre-registered here (§2); (ii) the retest wave of v1.14 Stage 2 (`H3_Retest_Reliability`, about Dec 7), which this design meets as v1.14 §6 specifies; (iii) the t₅ inputs the AIAS 6.0 Preview requires or wants (its §11.3); (iv) a stored corpus of search-on answers for Grounding Paper B's stability study (v1.13 §8).
**Protocol version:** as v0.42: recall Presence (π̂), recognition and Consistency (φ, Methodology v1.8, SSRN 6963359) as implemented in the v0.41 scorer and used by v0.42; every t₄ and t₅ statistic is computed by v0.42's own functions (`osf/v42/scripts/score_v0_42.py`, imported unchanged by `osf/v45/scripts/score_v0_45.py`).
**Lock target:** git tag `v0.45-prereg-r1` on branch `v0.45`, pushed to `origin`. **External anchor (pre-declared):** deposit of this pre-registration, the probe file, the cost estimate, the dry run, the scripts and the lock manifest at OSF `ec6wh` → `v45/prereg/`, with `v45/anchor/` naming the tag's commit, before any t₅ call. `acquire_v0_45.py --collect` refuses to run until the tag is on `origin` and the anchor file names its commit.
**Pre-registrant:** Pablo Ulpiano González Castro
**Status:** r1 draft, written on 2026-11-11 (morning, US Central) for the pre-registrant's review. r0 was written on 2026-11-10 between about 5 and 7 pm US Central (commits 17:29–17:31 CT), before any t₄ answer existed (t₄'s first call: 2026-11-11 02:57 UTC = Nov 10, 8:57 pm CT); the hypotheses, thresholds, tests and seeds of §2 are r0's, fixed blind to t₄, and r1 changes none of them. r1 is written after t₄'s collection: it read only the usage fields (tokens, searches, cost) and call times of t₄'s raw file, never an answer, and computed nothing about answer content; it changes cost figures, code provenance, logistics and the J1 text (§9, r1). No paid call was made for r0 or r1 (models, status and prices were read on the vendors' pages; one free models-list request). It locks 24 hours after it reaches the pre-registrant unless he objects (programme rule for new collections, Nov 9, 2026).
**Version number:** v0.45 is the next free phase number (branches v0.43, v0.44 and v0.62 exist; no v0.45 branch or tag on 2026-11-10 or 2026-11-11). The roadmap line that used to carry "v0.45" (Ranking × model-version stability) reads "v0.NN … takes the next free number when scaffolded" since 2026-11-10.
**Collection window:** first call not before Thu 2026-12-03 06:00 UTC (00:00 US Central); every call within 72 hours of the first; no new request after Sun 2026-12-06 23:59:59 US Central (2026-12-07 05:59:59 UTC). One paid collection at a time on the collection machine (§4.6).
**Depends on:** t₄ (v0.42) locked, collected, coded and scored. State on 2026-11-11: locked (tag `v0.42-prereg-r1` → `58d1891`, 2026-11-11 02:53 UTC; the pre-registrant waived the 24-hour review); collected 2026-11-11 02:57–09:50 UTC, 876 of 876 calls answered (tag `v0.42-acquisition-locked` → `a790bb1`; recorded spend $67.9551 including its $0.50 judge reserve); coded (commit `c84f6fa`; the v0.23 Phase A judge, Claude Sonnet 4.5, through the legacy Anthropic organization's key, 72 of 72, no R_ERR); scoring pending (needed only for G3, §5.3). t₄'s last call is about 22 days before t₅'s window opens, so t₅ stays on Dec 3 (§4.6).

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

Two calendar facts shape the design. Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`), the v0.23 recognition judge since t₁, retires on 2026-11-30; Anthropic names `claude-sonnet-5-5` as its replacement (model deprecations page, read 2026-11-10 and again 2026-11-11). Gemini 4 Argon's list price doubles from 2026-12-01 ($2 / $10 to $4 / $20 per million input / output tokens; Google Cloud Vertex AI pricing page, read 2026-11-10 and again 2026-11-11), so t₅ costs more than t₄ for the same calls. A third fact (r1): the programme's Anthropic calls now come from a new organization (`c1080353-9fa2-4ead-b596-e062dde7c70a`), which does not serve Claude Sonnet 4.5 (HTTP 404 on 2026-11-11; t₄'s v0.23 coding therefore ran through the legacy organization's key, the pre-registrant's decision) and does serve `claude-sonnet-5-5` and `claude-sonnet-4-6` (free models list, 2026-11-11 08:38 CT). Sonnet 4.5 is thus not available to t₅ even before its retirement.

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
- **Fixed before t₄.** Hypotheses, thresholds, tests and seeds are fixed in the r0 text, written before any t₄ answer existed; r1 changes none of them. A later revision before the lock may change cost figures, the window and logistics; a change to anything in §2 restarts the 24 hours and is listed in §9.

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
- **MC_Call_Parity:** the call functions, retry policy, Message Batches path and record builder are t₄'s; unit tests compare them with v0.42's source at tag `v0.42-prereg-r1` (commit `58d1891`), the code t₄ ran (r1: r0 named `61515b4`, which preceded v0.42's clarifications C27–C28; the check itself is unchanged).
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

**Re-read for r1** (the same vendors' pages, 2026-11-11, 08:36–08:38 am US Central = 14:36–14:38 UTC): nothing changed for the panel, and no panel model has an announced retirement or shutdown before the window ends (2026-12-07 UTC). Anthropic deprecations page: `claude-fable-5-2` "Active", retirement "Not sooner than November 9, 2027"; `claude-sonnet-4-5-20250929` "Deprecated", retirement November 30, 2026, replacement `claude-sonnet-5-5`; `claude-sonnet-5-5` and `claude-sonnet-4-6` "Active" (not sooner than 2027-09-28 and 2027-02-17). OpenAI: the gpt-6-astra page still reads "Our most capable model for the most demanding work", lists only the `gpt-6-astra` snapshot and no deprecation date; the deprecations page (newest entry 2026-11-10) lists no GPT-6 model. Google: changelog entry of October 13, 2026, "Gemini 4 Argon (`gemini-4-argon`) generally available (GA)" (newest entry October 30); the deprecations page lists no Gemini 4 model; the Gemini API models page lists `gemini-4-argon` under "Stable" as "Our flagship reasoning model". Newer models, noted for the pre-registrant and not added (rule 6 below; t₅ is a stability repeat): OpenAI's pricing page now lists `gpt-6.1-sol` and `gpt-6.1-terra`; gpt-6.1-sol's own page calls it "Near-Astra performance for complex work at a lower cost" (a cheaper tier, not a newer flagship), and launch reports found by search (not an OpenAI page read for r1) describe gpt-6.1-terra as a lower-cost model. Google's AI Studio model page now shows Gemini 4 Carbon (`gemini-4-carbon`) with the same introductory price as Argon ("$2.00 / $10.00 (intro thru Nov 30)"), but it is absent from the Gemini API models page, changelog and deprecations page read the same morning; its general availability is still not shown on a Google page, so it stays ineligible. Anthropic lists no model above Claude Fable 5.2.

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

`osf/v45/scripts/acquire_v0_45.py` is generated from v0.42's script at tag `v0.42-prereg-r1` (commit `58d1891`: the code t₄ ran, with v0.42's clarifications C26–C28; r0 used `61515b4`, which preceded C27–C28) by the listed text replacements of `_fork_v0_45.py`: paths (`osf/v45`), tag and anchor, batch request IDs (`v45-`), budget module, window, the availability guard, and the removal of the feasibility mode. Unit tests check that the call functions, the retry policy, the batch path and the record builder are identical to v0.42's source at that commit, that the fork regenerates the script byte for byte, and that `budget_v0_45.py`'s functions equal t₄'s `budget_v0_42.py` (MC_Call_Parity). C28 is therefore part of t₅: billed searches are counted conservatively (OpenAI `open_page` and `find_in_page` actions; Anthropic `usage.server_tool_use.web_search_requests`), Gemini's `tool_use_prompt_token_count` is recorded and priced as input, and a synchronous request reserves two worst cases.

**Record.** `osf/v45/data/t5_raw.jsonl`, one line per attempt, with t₄'s schema (v0.42 §4.4, including C28's `tool_use_prompt_tokens`); v1.14's Stage 2 reads it as its `--t5-raw`. Also `t5_budget_state.json` (approvals), `t5_batches.jsonl` (batch journal) and `t5_availability_v0_45.json`.

### §4.5 Budget

**Cap.** At most $100 of paid model calls for this paper, including re-sends and the judge (programme rule, 2026-11-10).

**Prices** (vendors' own pages, read again on 2026-11-10 for r0 and on 2026-11-11, 08:36–08:38 am US Central, for r1; every value unchanged and equal to the one v0.42 r2 recorded on 2026-11-10; machine copy in `osf/v45/scripts/budget_v0_45.py`):

| Model / item | Standard, US$ per 1M tokens in / out | Batch | Search fee | Source |
|---|---|---|---|---|
| Claude Fable 5.2 | 8 / 40 | 4 / 20 (used) | web search $10 per 1,000 searches, "plus standard token costs for search-generated content" | https://platform.claude.com/docs/about-claude/pricing |
| GPT-6 Astra | 10 / 50 | 5 / 25 (not used: t₄'s call mode is kept) | web search "$10.00 / 1k calls"; "Search content tokens billed at model rates" | https://developers.openai.com/api/docs/pricing ; https://developers.openai.com/docs/models/gpt-6-astra |
| Gemini 4 Argon | 2 / 10 promotional through 2026-11-30; **4 / 20 starting 2026-12-01** (Global) | none listed | grounding $14 per 1,000 grounding queries beyond 5,000 per month at no charge (allowance not assumed) | https://cloud.google.com/vertex-ai/generative-ai/pricing ; the AI Studio model page shows only "$2.00 / $10.00 (intro thru Nov 30)" |
| Claude Sonnet 5.5 (successor judge, first candidate) | 2 / 10 | 1 / 5 | — | https://platform.claude.com/docs/about-claude/pricing |
| Claude Sonnet 4.6 (successor judge, fallback) | 3 / 15 | 1.50 / 7.50 | — | same |

**Estimate (r1): t₄'s recorded usage at t₅'s prices.** `osf/v45/scripts/reestimate_t4_v0_45.py` reads t₄'s raw file at tag `v0.42-acquisition-locked` (SHA-256 `f3109091f51af7899098d83a1d7b2080a26a06824caa5f6fc0486f3d6196d4bf`; 990 lines for 876 calls; the 114 error lines carry no billed usage) and keeps only usage and call metadata (never the answer text, the prompt, the search record or an error message); it writes `osf/v45/prereg/cost_estimate_v0_45_r1.json` and `.txt`. Priced on t₄'s own dates, it reproduces t₄'s recorded cost exactly ($67.4551; every line equal). *Central* = the same usage priced on the t₅ date: the same calls, models, call modes, tokens and searches three weeks later (re-sends need no extra factor: every billed request of t₄ is in the usage). *High (conservative)* = per model and question type (Phase B S0; Phase A yes/no, v0.19–v0.22; Phase A open, v0.23; Phase B S1), the 90th percentile of t₄'s per-call cost at t₅ prices × the number of calls × 1.10 for re-sends: the rule of r0 and v0.42 (every call at its 90th percentile) applied to t₄'s measured costs instead of v0.39's tokens. Only Gemini 4 Argon's price changes between the waves ($2 / $10 → $4 / $20 per 1M tokens; its grounding fee, and every other price, is unchanged).

US$ at t₅ prices, central / high; last column t₄'s actual cost at t₄'s prices:

| Model (mode) | Phase B S0 ×3 (90) | Phase A S0 ×1 (112) | Phase B S1 ×3 (90) | Total (292 calls) | t₄ actual |
|---|---|---|---|---|---|
| Claude Fable 5.2 (Batch API) | 2.32 / 6.94 | 2.13 / 2.79 | 15.73 / 33.48 | 20.18 / 43.22 | 20.18 |
| GPT-6 Astra (standard) | 3.79 / 8.95 | 4.66 / 5.83 | 35.38 / 81.83 | 43.83 / 96.61 | 43.83 |
| Gemini 4 Argon (standard) | 2.35 / 3.60 | 0.94 / 1.15 | 3.09 / 4.98 | 6.39 / 9.72 | 3.44 |
| **All (876 calls)** | **8.46 / 19.49** | **7.73 / 9.78** | **54.20 / 120.29** | **70.40 / 149.55** | **67.46** |

(Cells are rounded to the cent, so sums can differ by a cent.) Against r0's estimate on v0.39's token basis ($67.27 / $142.60), t₄'s usage makes Claude Fable 5.2 cheaper ($20.18 against $30.78 central) and GPT-6 Astra dearer ($43.83 against $29.36): its search-on calls carried about 30,000 input tokens each (search content is billed at model rates) and 3.3 billed searches.

**By block, in collection order** (cumulative spend includes the $2.50 judge reserve):

| Block | Calls | t₄ actual | t₅ central / high | Cumulative central / high |
|---|---|---|---|---|
| 1 B-S0 run 1 | 90 | 2.43 | 2.82 / 6.50 | 5.32 / 9.00 |
| 2 B-S0 run 2 | 90 | 2.37 | 2.77 / 6.50 | 8.09 / 15.49 |
| 3 B-S0 run 3 | 90 | 2.48 | 2.87 / 6.50 | 10.96 / 21.99 |
| 4 A-S0 run 1 | 336 | 7.26 | 7.73 / 9.78 | 18.69 / 31.77 |
| 5 B-S1 run 1 | 90 | 16.99 | 17.44 / 40.10 | 36.13 / 71.86 |
| 6 B-S1 run 2 | 90 | 17.63 | 18.05 / 40.10 | 54.18 / 111.96 |
| 7 B-S1 run 3 | 90 | 18.29 | 18.72 / 40.10 | 72.90 / 152.05 |

**What fits under $100 (r1).** At the central estimate, all seven blocks: $72.90 with the judge reserve, below the $80 pause, and the projection rule does not pause (after block 5: $36.13 + 2 × $17.44 = $71.00 ≤ $100). The $80 pause would be reached in block 7 only if t₅'s calls cost about 10% more than t₄'s usage at t₅ prices ($77.50 instead of $70.40); the projection pause only if block 5 cost more than $27.10 (55% above its central). At the high estimate, blocks 1–5 ($71.86): the projection rule after block 5 (spend + 2 × block 5's actual cost > $100; here $152.05) pauses the collection before runs 2–3 of S1 and asks the pre-registrant; collecting them would take about $80.19 more at the high estimate, which the cap does not allow. The confirmatory blocks (1–3, $21.99 high with the reserve) and the brand questions (block 4, $31.77 cumulative) fit in every case. The central estimate needs no design change (§11 item 7 does not arise).

**Design trade-off** (r1 basis for designs made of t₄'s questions; r0's v0.39 basis, `cost_estimate_v0_45_r0.txt`, for the rest):

| Design | Calls | t₅ central / high |
|---|---|---|
| **t₅ (adopted): t₄'s design repeated** | **876** | **70.40 / 149.55** |
| Blocks 1–3 only (S0 category questions: the confirmatory tests and v1.14's H3) | 270 | 8.46 / 19.49 |
| Blocks 1–4 (adds the brand questions, P at t₅) | 606 | 16.19 / 29.27 |
| S1 with two runs (blocks 1–6) | 786 | 51.68 / 109.46 |
| t₅ plus a Coverage re-ask (r1's t₅ + r0's Coverage figure, Fable via Batch API) | 1,551 | 101.24 / 206.37 |
| Coverage re-ask alone, Fable via Batch API (r0 basis) | 675 | 30.84 / 56.82 |
| Coverage re-ask alone, every model synchronous (v1.12's own call mode; r0 basis) | 675 | 47.72 / 90.35 |
| Claude Opus 5.5 continuity arm, S0 category questions × 3, Batch API (r0 basis; not adopted) | 90 | 1.69 / 2.24 |

**What does not fit, and the smallest budget for it.** (i) The Coverage re-ask: beside t₅'s design it would cost about $101 central and $206 high, past the $100 cap even at the central estimate. It is left to Coverage Paper B as its own collection with its own $100 cap; the smallest budget for it is $30.84 central / $56.82 high with Claude Fable 5.2 through the Batch API, or $47.72 / $90.35 in v1.12's synchronous call mode (r0's token basis; v1.12's own estimate, on its own assumptions, is lower). (ii) Sentiment judging of the t₅ answers: a separate study with its own budget; the Preview's planning estimate for one wave of S0 category answers is $14.09 to $53.61 (Preview §12). (iii) Search-on runs 2–3 if the high estimate materialises: about $80.19 more, above the cap (the whole design at the high estimate would need $152.05).

**r0's estimate, kept for the record.** r0 estimated t₅ on v0.42's token basis (v0.39's current arm; Claude Fable 5.2 at Claude Opus 5.5's basis × 2 or × 3; Gemini output × 1.5 at the high level; re-sends +2% or +10%): $67.27 central and $142.60 high for the 876 calls ($69.77 / $145.10 with the reserve), in `cost_estimate_v0_45_r0.json` and `.txt`, written by `cost_estimate_v0_45.py`, whose figure the dry run still prints. r1's estimate replaces it in this section.

**Successor judge cost.** At most 288 calls per candidate (144 t₃ and 72 t₄ answers for J1, 72 t₅ answers), each at most 1,500 input and 10 output tokens: $0.89 on Claude Sonnet 5.5 (J1 alone $0.67) and $1.34 on Claude Sonnet 4.6 (J1 alone $1.00), $2.23 if both are tried; reserve $2.50, counted as spent from t₅'s first call. J1 records its actual tokens and cost (§5.1).

**Guard (computed from actual usage; unchanged from v0.42).** `budget_v0_45.Ledger`: spend = the judge reserve + the cost of every raw line already written (its `usage_parts` at the prices in force on the request's date, so Gemini 4 Argon at $4 / $20). Before a request is sent its worst case is reserved (output at the 16,384-token cap, 2,000 input tokens in S0 or 150,000 in S1, up to 10 searches; a synchronous request reserves two worst cases, v0.42 C28; a batch is cut to the requests whose worst cases fit, and the rest follow in a later batch). (i) **Hard stop:** no request is sent if spend + reservations + its worst case would exceed $100. (ii) **Pause at $80:** once spend reaches $80, no new request starts until the pre-registrant's OK is recorded (`acquire_v0_45.py --collect --approve-past-80 "<who, when>"`). (iii) **Projection pause:** applied once, when block 5 (B-S1 run 1) is complete: if spend + 2 × that block's actual cost exceeds $100, collection pauses before runs 2–3 of S1 and the pre-registrant decides (`--approve-projection`); the hard stop still applies.

**Re-estimate from t₄.** r0 required §4.5 to be re-estimated from t₄'s recorded usage at t₅ prices before this draft is sent, changing figures, not the design, and the pre-registrant to be asked whether to collect S1 with two runs if the central total with the reserve exceeded $80. Done in r1 (above): $72.90, below $80, so the question does not arise; it remains the rule if the cost is re-estimated again before the lock.

### §4.6 Window, order and dependencies

- **Lock first.** The pre-registrant receives this text; at least 24 hours later it is locked and anchored (§9). Nothing is sent before.
- **Window.** First call not before Thu 2026-12-03 06:00 UTC (00:00 US Central). No new request after the earlier of 72 hours from the first recorded call and 2026-12-07 05:59:59 UTC (Sun Dec 6, 23:59:59 US Central). A request already sent completes and is recorded. Enforced by `acquire_v0_45.py`.
- **One paid collection at a time.** The script refuses to start while another `acquire_v*.py --collect` runs. The paid runs planned before t₅ (v1.12 Coverage, Nov 14–16 or Nov 22–29; v0.40, Nov 17–21; v0.44, costed in its draft for Nov 24–28; v0.62, by default Nov 29 to Dec 2; v1.11's judge batches from Nov 22) are scheduled before Dec 3; none may run during t₅'s window.
- **If t₄ is held or delayed.** t₅ stays on Dec 3 if t₄'s last call is at least 14 days earlier. Otherwise t₅ moves to 21 days after t₄'s last call (window and hard end shifted by the same amount) through a logged clarification before the lock, and the Preview takes Ranking as "retest pending" under its own §4.4 and §11.4. If t₄ is not collected at all, t₅ has no baseline and is not locked. (r1: t₄'s last call was 2026-11-11 09:50 UTC, 21.8 days before the window opens; t₅ stays on Dec 3.)
- **Order after the lock.** (1) J1 judge parity (§5.1; at most 216 small paid calls per candidate), once the lock and the OSF deposit are verified and before Dec 3 (v0.42's coding, which r0 waited for, was done on 2026-11-11, commit `c84f6fa`), when no other paid collection is running; record `osf/v45/data/judge_parity_J1_v0_45.json`. (2) Dec 2: the availability record. (3) From Dec 3: `acquire_v0_45.py --collect` under `caffeinate -w`. (4) After the last call: tag `v0.45-acquisition-locked`, pushed (v1.14 Stage 2 needs it). (5) Coding (§5.1). (6) Scoring once (§5.2). (7) v1.14 Stage 2 and the component scorers read t₅ on their own schedule; their outputs are read here when they exist (§2.6).

---

## §5 Analysis plan

### §5.1 Coding

- **Mentions, URL removal and v0.19–v0.22 recognition.** v0.42's certified coder, `osf/v42/scripts/code_t4_v0_42.py`, used unchanged (git blob `2d36735d512cf9e13b74010ba5a7f655fc7de0bc`, the pin of v0.42 §5.1; `code_t5_v0_45.py` refuses to code if the blob differs). t₄ and t₅ are therefore coded by the same functions.
- **v0.23 recognition (Phase A): successor judge.** The judge's system prompt, user template, 3,000-character truncation, R0–R3 rubric and label parser are v0.23's (`scripts/score_v0_23.py`), unchanged; only the model and, where the model requires it, the request settings change. `code_t5_v0_45.py` passes v0.23's own judge call through a client proxy:
  - **First candidate: Claude Sonnet 5.5 (`claude-sonnet-5-5`)**, Anthropic's recommended replacement for `claude-sonnet-4-5-20250929` (model deprecations page, read 2026-11-10); "Active (latest)", retirement not sooner than 2027-09-28 (model page). Its model page states that setting temperature, top_p or top_k "returns a 400 error" and that adaptive thinking is on by default; its migration guide states that `max_tokens` "covers thinking plus text" and that `thinking: {"type": "between_tools"}` is the lowest setting. v0.23's call (temperature 0.0, max_tokens 10, first content block read as text) would therefore fail on this model if only the model ID changed. The proxy sends no temperature, sends `thinking: {"type": "between_tools"}` and `output_config: {"effort": "low"}`, keeps max_tokens 10, and returns the first text block. These settings are taken from the vendor's pages and tested against local fakes only; J1 is their first real test.
  - **Fallback: Claude Sonnet 4.6 (`claude-sonnet-4-6`)**, Active, retirement not sooner than 2027-02-17 (deprecations page); runs without thinking when no thinking field is sent (migration guide). v0.23's call is sent unchanged except the model ID. Whether it accepts temperature 0.0 is not verified on a vendor page; if it does not, its calls return errors and it fails J1 (r1: Anthropic's deprecations page, read 2026-11-11, lists `temperature`, `top_p` and `top_k` as "Removed in API version 2026-10-21", with a 400 error in that version; whether the programme's SDK requests that version was not checked; an all-error run is void, not a FAIL, under the J1 rule below).
  - **J1 (judge parity), after the lock and before any t₅ answer is coded** (made concrete in r1; **Plan update suggested** to the pre-registrant: the v0.23 judge changes from Claude Sonnet 4.5 to Claude Sonnet 5.5, or to Claude Sonnet 4.6 as fallback, only through this check). *When:* once the tag `v0.45-prereg-r1` is on `origin` and the OSF deposit is verified (`code_t5_v0_45.py --parity <model>` refuses before the tag is on `origin`), and before Dec 3, so that the result is known before t₅'s collection; never while another paid collection runs. *What:* each candidate in turn, called through the programme's current Anthropic organization (which serves both; §1), judges (a) the 72 t₄ v0.23 Phase A answers (raw file at tag `v0.42-acquisition-locked`, SHA-256 `f3109091…`) against Claude Sonnet 4.5's labels in `osf/v42/data/coded/v23_phase_a.csv` at v0.42 commit `c84f6fa` (SHA-256 `52a1c9d7a32ab1bd176eb39af68559a3336ec0442bd2ba52a5ef4a464802358e`; 72 of 72 coded on 2026-11-11, 24 per model, no R_ERR), and (b) the 144 t₃ v0.23 Phase A answers against their Sonnet 4.5 codes locked in v0.41 (`osf/v41/data/v23/v23_phase_a_scored.json`). *Rule (r0's thresholds, unchanged):* **PASS** if the binary code (recognized = R1–R3; not = R0; v0.42's `r_level_to_binary`) agrees with Sonnet 4.5's on at least 95% of all answers judged (with 216 answers: at least 206) and on at least 90% of the t₄ answers (at least 65 of 72), with no R_ERR left. Exact R-level agreement is reported. Candidates in order; the first that passes is the t₅ judge, and its codes for the 72 t₄ answers are used for t₄ in every comparison (next item). *Void run:* a run in which no request returns a label (every request R_ERR: a request-settings error such as HTTP 400, or thinking that uses up the 10-token budget) measured no agreement; it is void, not a FAIL. That candidate's request settings may then be corrected once (system prompt, user template, truncation, rubric, parser and thresholds unchanged), with a DEVIATIONS entry written before the re-run; the re-run is final. Every other run is final. *Consequence of failure:* the next candidate is tried; if none passes, the rule below applies. *Record and cost:* `code_t5_v0_45.py --parity <model>` writes every run, with its agreement figures and its recorded tokens and cost, to `osf/v45/data/judge_parity_J1_v0_45.json`, and `--judge <model>` refuses to code t₅ with a model that has not passed J1; the result goes into DEVIATIONS (pre-registered contingency used) before t₅ is coded. J1 costs at most $0.67 on Claude Sonnet 5.5 and $1.00 on Claude Sonnet 4.6 (216 requests of at most 1,500 input and 10 output tokens), inside the $2.50 judge reserve (§4.5). The reserve covers both candidates' J1 with t₅ coding (at most $2.23), or the first candidate's J1, a billed void run and its t₅ coding ($1.56); a billed void run together with the fallback could exceed it (at most $3.67, with billed void runs on both candidates). MC_Budget reports the judge's recorded cost beside the reserve.
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
7. The cost estimate rests on t₄'s recorded usage three weeks earlier (r1); t₅'s answers can be longer or search more (the S1 calls carry most of the cost), which the guard handles from t₅'s own recorded usage (§4.5).
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

- **r0 draft** written on 2026-11-10 by the AIAS runner and committed on branch `v0.45` (local; not pushed, not deposited, not sent). Before it is sent: §4.5 re-estimated from t₄'s recorded usage once v0.42's collection has ended (a logged clarification; figures only). Done in **r1** (2026-11-11; this text; local, not pushed, not deposited).
- **Sending.** The coordinator sends it to the pre-registrant; it locks 24 hours after it reaches him unless he objects. t₄'s collection ended on 2026-11-11 (09:50 UTC), earlier than r0 assumed (about Nov 14–16), so r1 can be sent now and locked well before Thanksgiving week; the lock steps are in `osf/v45/LOCK_STEPS.md`.
- **Between sending and lock:** clarifications that change no hypothesis, threshold, test, seed, panel, probe or decision rule are logged below; any other change restarts the 24 hours.
- **Lock:** write `osf/v45/prereg/LOCK_MANIFEST_v0_45.sha256` (`lock_manifest_v0_45.py`: DEVIATIONS.md, every other file of `osf/v45/prereg/`, the v0.45 scripts and tests, and the files of earlier phases they import or read: `osf/v42/scripts/acquire_v0_42.py` as the fork source, `budget_v0_42.py`, `code_t4_v0_42.py`, `score_v0_42.py`, `osf/v42/prereg/probes_v0_42.jsonl`, `osf/v41/scripts/score_v41.py`, `osf/v41/v41_three_wave_table.csv`, `osf/v41/data/v23/v23_phase_a_scored.json`, `scripts/score_v0_23.py`, `scripts/score_v0_31.py`, `osf/v39/data/v39_raw.json`); commit; tag `v0.45-prereg-r1`; push branch and tag; write `osf/v45/anchor/osf_anchor_v0_45.json` (`osf/v45/lock/write_anchor_v0_45.py`: tag, commit, every locked file's SHA-256 and blob at the tag, the coder pin, t₄'s J1 inputs, UTC time); deposit `osf/v45/prereg/`, the scripts and `osf/v45/anchor/` at OSF `v45/` and verify their SHA-256 there (`osf/v45/lock/osf_verify_v0_45.py`). Only then J1 and, from Dec 3, `acquire_v0_45.py --collect`. Step by step: `osf/v45/LOCK_STEPS.md`.

**Change log**

- **2026-11-10, r0.** Drafted before any t₄ answer exists. Design = v0.42 r2's, repeated; successor v0.23 judge with J1; hypotheses `H_Stab_Presence`, `H_Stab_Consistency`, `H_Stab_Drift`, `H_Stab_Search_Presence` and the component legs; prices and model status read again on the vendors' pages (§4.3, §4.5). Scripts: `_fork_v0_45.py` → `acquire_v0_45.py`; `budget_v0_45.py`; `cost_estimate_v0_45.py`; `code_t5_v0_45.py`; `score_v0_45.py`; tests `test_acquire_v0_45.py` (34) and `test_score_v0_45.py` (20): 54 of 54 pass on synthetic data and local fakes (no model request leaves the machine; one test checks that J1 refuses before the tag exists, which reads the tag list on `origin`). Dry run: `dry_run_v0_45.txt` (876 calls; nothing sent). Choices made in drafting are listed in §11.
- **2026-11-11, r1** (before sending; written after t₄'s collection). No hypothesis, threshold, test or seed of §2 changed; the panel, probes, design, window, budget rules and decision rules are r0's. No t₄ answer text was read and no t₄ statistic computed: r1 read only the usage fields and call times of t₄'s raw file (an allowlist in `reestimate_t4_v0_45.py`) and the column names, row count and hashes of t₄'s coded v0.23 Phase A table. No paid call (one free models-list request). Changes:
  - (i) **Code provenance (§2.7 MC_Call_Parity, §4.4).** r0 forked v0.42 at `61515b4` (2026-11-10, 5:30 pm CT). v0.42 then logged C27 (scorer: the brand table's N3 columns always on the full panel; Gemini redirect domains in descriptive 5) and C28 (acquisition and budget: conservative billed-search counting, Gemini's `tool_use_prompt_tokens` as a new raw field, a two-request reservation for synchronous calls) before its lock, and t₄ ran that code. r1 merges tag `v0.42-prereg-r1` (`58d1891`) into branch `v0.45` (merge commit `026d6c2`; only `osf/v42/` files change; no t₄ data), regenerates `acquire_v0_45.py` from `58d1891` (the diff to r0's script is exactly C28 plus docstrings), ports C28 to `budget_v0_45.py` (its functions now equal t₄'s `budget_v0_42.py`), and points MC_Call_Parity and the tests at `58d1891`. Without this, t₅'s raw schema and guard would have differed from t₄'s. The dry run is unchanged.
  - (ii) **Cost (§4.5).** Re-estimated from t₄'s recorded usage (`reestimate_t4_v0_45.py` → `cost_estimate_v0_45_r1.json` and `.txt`; it reproduces t₄'s recorded $67.4551): $70.40 central and $149.55 high for the calls, $72.90 / $152.05 with the $2.50 judge reserve. Central: below the $80 pause, no projection pause. High: the projection pause after block 5 applies (as in r0). r0's estimate is kept for the record. Prices re-read on 2026-11-11, unchanged.
  - (iii) **Panel status (§4.3)** re-read on 2026-11-11: no panel model retires before the window ends; newer models noted (GPT-6.1 Sol and Terra, cheaper tiers; Gemini 4 Carbon, not shown generally available); none added.
  - (iv) **J1 (§5.1)** made concrete: t₄'s reference labels (`v23_phase_a.csv` at `c84f6fa`, SHA-256 `52a1c9d7…`), counts (≥ 206 of 216; ≥ 65 of 72), timing (after the lock, before Dec 3), a void-run rule for an all-error run, the record and the cost; marked "Plan update suggested". `code_t5_v0_45.py` now records J1's tokens and cost (`j1_usage`). The thresholds and the consequence of failure are r0's.
  - (v) **Facts** added to the header (t₄'s lock, collection and coding), §1 (the new Anthropic organization does not serve Claude Sonnet 4.5), §4.6 (t₄'s last call 21.8 days before the window; J1's timing) and §7 item 7.
  - (vi) **Lock files.** `lock_manifest_v0_45.py` → `prereg/LOCK_MANIFEST_v0_45.sha256`; `osf/v45/LOCK_STEPS.md`; helpers `osf/v45/lock/write_anchor_v0_45.py` (queries `refs/tags/<tag>*`: git 2.54 omits the peeled line for a bare tag name), `osf_verify_v0_45.py`, `status_v0_45.py` (not locked, not deposited).
  - Tests: 68 of 68 pass: `test_acquire_v0_45.py` 40 (r0's 34, one expectation changed by C28 as in v0.42, plus v0.42's four C28 tests, the fork's byte-for-byte regeneration and the budget-function parity), `test_score_v0_45.py` 20, `test_reestimate_lock_v0_45.py` 8 (the field allowlist, the SHA-256 refusal, the method on synthetic usage, the guard path, t₄'s locked file with the published figures, J1's cost, the manifest).
- **2026-11-12, clarification (logged; no design change).** Gemini 4 Carbon became generally available on Google Cloud on 2026-11-10 for verified enterprise customers in select regions (https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/4-carbon); t5 stays on Gemini 4 Argon, as an exact repeat of t4; no design change.
- **2026-11-12, noted, no change.** v1.15 (Nov 12) found Claude Opus 5.5 putting a sentence before a required JSON reply on 4.2% of first tries; t5's successor recognition judge (Claude Sonnet 5.5, at most 10 output tokens including any thinking, read by the R[0-3] pattern) is checked for this by J1 (one R_ERR fails it; pre-registered fallback Claude Sonnet 4.6).

---

## §10 Files

`osf/v45/prereg/`: `PRE_REGISTRATION_v0_45.md` (this file); `PLAIN_SUMMARY_v0_45.md`; `probes_v0_45.jsonl` and `probe_parity_v0_45.json`; `cost_estimate_v0_45_r0.json` and `.txt` (r0's estimate, v0.39 basis); `cost_estimate_v0_45_r1.json` and `.txt` (r1's estimate from t₄'s usage); `dry_run_v0_45.txt`; `LOCK_MANIFEST_v0_45.sha256`. `osf/v45/anchor/DEVIATIONS.md` (Entry 0, ex ante). `osf/v45/scripts/`: `_fork_v0_45.py`, `acquire_v0_45.py`, `budget_v0_45.py`, `cost_estimate_v0_45.py`, `reestimate_t4_v0_45.py`, `code_t5_v0_45.py`, `score_v0_45.py`, `lock_manifest_v0_45.py`; `tests/` with `make_synthetic_t5.py`, `run_all_v0_45.py`, `test_acquire_v0_45.py`, `test_score_v0_45.py`, `test_reestimate_lock_v0_45.py` (run as a script: `python3 osf/v45/scripts/tests/run_all_v0_45.py`; outputs under `/tmp`). Not locked: `osf/v45/LOCK_STEPS.md` (the coordinator's lock, J1 and collection steps) and the helpers in `osf/v45/lock/` (`write_anchor_v0_45.py`, `osf_verify_v0_45.py`, `status_v0_45.py`).

---

## §11 Choices made in drafting (for the pre-registrant; each has a recommended default)

1. **Repeat t₄ exactly** (876 calls; S0 category questions, brand questions, then search-on), the same three model IDs and call modes, on the code t₄ ran (r1). Default: yes ($70.40 central / $149.55 high, r1). Alternative: blocks 1–4 only ($16.19 central / $29.27 high, r1), which loses the Grounding retest and the search-on stability test.
2. **No Coverage re-ask in t₅.** It does not fit beside t₄'s design (about $101 central with it, r1). Default: leave it to Coverage Paper B as its own collection after v1.12's gate ($30.84 / $56.82 with Fable through the Batch API, r0 basis). Alternative: drop the search-on blocks to make room (not recommended: the Preview and Grounding want them).
3. **Successor v0.23 judge (Plan update suggested).** Claude Sonnet 4.5 retires on Nov 30 and the programme's current Anthropic organization does not serve it. Default: Claude Sonnet 5.5 (Anthropic's named replacement; served by the current organization), with the request settings its pages require, then Claude Sonnet 4.6 as fallback, each used only after passing J1 (§5.1: ≥ 95% binary agreement with Sonnet 4.5 over 216 earlier answers, ≥ 90% on t₄'s 72; run after the lock and before Dec 3; under $1 for the first candidate, inside the $2.50 judge reserve). If neither passes: no v0.23 recognition at t₅, and P without the 24 spirits brands at both waves.
4. **Newer flagship before Dec 3.** Default: not added (no budget room; t₅ is a stability repeat); recorded in the paper. Found on 2026-11-11: no newer flagship; OpenAI's GPT-6.1 Sol and Terra are cheaper tiers, and Google's Gemini 4 Carbon is listed with a price but not shown generally available (§4.3).
5. **Window.** Default: from Thu Dec 3, 00:00 US Central, at most 72 hours, hard end Sun Dec 6, 23:59 US Central.
6. **If the high estimate materialises.** Default: the projection pause after search-on run 1 stops the collection and asks you, as at t₄. Alternative: decide now to skip search-on runs 2–3 without asking.
7. **If t₄'s actual cost puts t₅'s central estimate above $80.** Default: search-on with two runs (G\* at t₅ then pools two runs, flagged). Alternative: three runs, with your OK at the $80 pause. r1: does not arise (central $72.90 with the reserve); if t₅ runs about 10% dearer than t₄, the $80 pause asks you during the last search-on run.
8. **Thresholds.** Default: the programme's bars (Presence 0.70 / 0.50; Consistency 0.50 / 0.30, n ≥ 40; components 0.50 / 0.30, n ≥ 30), with `H_Stab_Drift` as the stricter test for three weeks.
