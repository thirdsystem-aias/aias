# AIAS v1.12 — Coverage, Paper A: instrument, cross-category baseline, separability gate

AIAS™ Measurement Program — Third System™. Pre-registration **DRAFT r1, sent to Pablo for the 24-hour review (2026-11-10).** Not locked. Nothing collected, nothing spent.

Files: this document; `cep_sets_v1_12.md` (CEP sets and the procedure that produced them); `probes_v1_12.md` and `probes_v1_12.jsonl` (exact wording; 75 probes); `cost_v1_12.csv` (cost table); `build_probes_v1_12.py` (generates the probe files and the cost table; no network); `calibration_N1_v1_12.json` (calibration N1, §2.4); `dry_run_acquire_v1_12.txt` (acquisition dry run). Scripts in `osf/methodology/v1_12/scripts/`: `score_v1_12.py` (scorer) with `tests/test_score_v1_12.py`, and `acquire_v1_12.py` (acquisition).

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.12 |
| PHASE_TYPE | methodology lock with **new acquisition** (paid model calls after the lock; hard cap §6.6) |
| Status | DRAFT r1 on branch `v1.12` (from `aias-2.0` @ `894ccee`); r0 written by the runner's sub-agent; r1 applies the runner's decisions of 2026-11-10 (§13) and the Cov* redesign that calibration N1 required (§2.4, §12) |
| Locks on | Pablo receives the draft → **24 hours** (program rule for new collections, Nov 9) → content lock → commit → tag `v1.12-prereg-r1` → push → OSF deposit of `osf/methodology/v1_12/prereg/` + `anchor/` (tag, commit, SHA-256 of every locked file) → only then `acquire_v1_12.py --collect` (refuses to run otherwise; §6.5) |
| Locked inputs | Presence: protocol v1.6. Consistency: v1.8 φ, v1.9 C* (rated at ≥ 6 mentions). Values for the gate come from the t4 wave (v0.42, newest models, Nov 11–13) as defined in §2.6; published AIAS 2.0 values (`osf/aias_2_0/aias_2_0_profiles.csv`) for the secondary cross-panel leg |
| Conditional inputs | Ranking R* (v1.10) and Sentiment S (v1.11): legs active only if those pre-registrations lock first (§3, activation rule) |
| Feeds forward | Coverage Paper B (only after PASS, or MARGINAL with Pablo's recorded decision); the component calibration after Ranking, Sentiment and Coverage |

**Lineage.** AIAS 2.0 (Nov 10, 2026; branch `aias-2.0`) showed Consistency separable from Presence (within-category |ρ(C*, P)| = 0.073, 0.082, 0.189 at t1–t3). The first Consistency instrument (v1.7 CV-CPC) failed its gate because it moved with how often a brand is named (pooled ρ = 0.766 against a 0.50 ceiling). Plan of record (Pablo, Nov 9): Paper A = instrument specification + cross-category baseline + separability gate against Presence, Consistency and the other components (bands: within-category |ρ| ≤ 0.30 CONFIRMED separable, ≥ 0.50 FALSIFIED, between MARGINAL). The archive inventory (Nov 10) found no designed buying-situation set in the archive (only six frames per category), so Coverage needs this new collection.

**Construct.** Coverage = in how many of a category's buying situations (category entry points, CEPs, after Romaniuk & Sharp 2016; the cue list is the program's own operationalisation, seven cue types labelled W, `cep_sets_v1_12.md` §1) AI answers name the brand. Presence asks whether the brand is named in general category questions; Consistency asks whether models agree; Coverage asks whether the brand's naming **spreads across situations or is tied to a few**, given how often it is named. In the Ehrenberg-Bass record, CEP linkage follows Double Jeopardy (bigger brands are linked to more CEPs), so a raw count of covered situations is expected to track Presence; the component score is therefore the rate-adjusted breadth Cov* (§2.4), and the raw share is reported beside it.

## 1. Research questions

- **RQ1 (instrument).** Do neutral, brand-free CEP questions change which registry brands AI answers name (MC_Situation), with a usable answer and registry-mention rate?
- **RQ2 (gate: separability).** Within category, is Cov* separable from Presence, from Consistency, from the brand's own naming rate in the Coverage answers, and (when locked) from Ranking and Sentiment?
- **RQ3 (gate: reliability).** Does Cov* order brands alike on two disjoint halves of the CEP set?
- **RQ4 (baseline).** What do raw coverage and Cov* look like per category, per model and per cue type (W) on the newest models?

## 2. Definitions

### 2.1 Units, categories, registries
The five omnibus categories and their **112 brand units** (16 + 24 + 24 + 24 + 24), unchanged: v0.19 audiophile headphones (`osf/v19/panel_registry_v0_19.csv`), v0.20 skincare (`prereg/v0_20_registry.json`), v0.21 cosmetics (`prereg/v0_21_registry.json`), v0.22 automotive (`prereg/v0_22_registry.json`, detector `prereg/v0_22_automotive_content.py`), v0.23 premium spirits (S01–S24, `scripts/acquire_v0_23.py` / `scripts/score_v0_23.py`). Same units as `aias_2_0_profiles.csv` and v0.42. Rare Beauty appears in v0.20 and v0.21 as two units, as before. No brand is added, removed or renamed.

### 2.2 Panels and condition
- **N3 (primary):** Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`), Gemini 4 Argon (`gemini-4-argon`) — the newest generally available flagship of each provider, verified Nov 10 from vendor docs (v0.42 §4.3). **C3 (continuity):** Claude Opus 5.5 (`claude-opus-5-5`), GPT-6 Astra, Gemini 4 Argon. **A4:** all four (descriptive only). Same model IDs as t4.
- **S0 only:** no tools. S1 (web search) is not collected in Paper A (§6.3).

### 2.3 Mentions and raw coverage
- **CEPs.** J = 14 per category (2 per W × 7 W; `cep_sets_v1_12.md`); halves A and B of 7 CEPs each (one per W). R = 3 runs per cell.
- **y_{b,m,j,r} ∈ {0, 1}:** model m's answer to CEP j in run r names brand b, by the substrate's certified detector applied to the visible answer text with URLs removed, exactly as v0.42 §5.1 (v0.20–v0.22 `detect_mention`; v0.19 `acquire_v0_19.parse_phase_b`; v0.23 the deterministic matching of `score_v0_23.score_phase_b`, no LLM step). The coder is v0.42's `osf/v42/scripts/code_t4_v0_42.py`, used unchanged: git blob `2d36735d512cf9e13b74010ba5a7f655fc7de0bc` on branch `v0.42` (commit `4e86dd9`; SHA-256 `d0e4e685b5e3e1d983190726b5e88ef2b841b4589d5802ba67b86e31e4148220`). v0.42 locks on 2026-11-10; the blob is re-checked against tag `v0.42-prereg-r1` at the v1.12 lock, and any difference is logged before the lock.
- **Missing cells.** A call without a valid answer after retries (§6.5) is missing: it enters no denominator and is never read as "not named".
- **Model coverage:** m covers (b, j) if y = 1 in at least 2 of its 3 runs (majority; with a missing run, in more than half of the answered runs).
- **Raw coverage (headline, reported):** **Cov_b = share of the category's 14 CEPs in which at least k = 2 of the 3 N3 models cover b** (0–100%). Sensitivities: k = 1 and k = 3. Cov is expected to move with Presence (Double Jeopardy); it is **not** the gate statistic and is reported with that warning.
- **Naming rate in the Coverage answers:** **π_cov,b** = share of the panel's answered CEP answers in b's category that name b.

### 2.4 Coverage breadth Cov* (component score; gate statistic)
Breadth is measured **within each model** (so between-model differences, which are Consistency, do not enter) and **against the spread that situation-blind naming with the same number of mentions would give** (so the brand's naming rate does not enter).

For brand b and model m in b's category:
- slots = m's answered CEP answers (normally 14 × 3 = 42); s_j = answered runs of CEP j;
- n = n_{b,m} = Σ_j Σ_r y (answers naming b); c = c_{b,m} = number of CEPs with Σ_r y ≥ 1 (CEPs touched);
- **Situation-blind null (Rasch-type).** Per model and category, P(y_{b,m,s} = 1) = logistic(θ_b + δ_{m,j(s)}) for slot s (one answered CEP answer: CEP j, run r), with no brand × CEP interaction: a CEP may draw longer or shorter lists of registry brands, but no brand is tied to a situation. Given n, b's named slots then follow the conditional Bernoulli law P(Y) ∝ Π_s exp(δ_{m,j(s)})^{y_s} with Σ y = n, which does not depend on θ_b.
- **δ̂^{(−b)}_{m,j}:** joint maximum-likelihood logistic fit with brand fixed effects and CEP effects (sum to zero over the answered CEPs) on the **other** registry brands of b's category in model m's answers; brands named in none or in all of the slots carry no information on δ and are left out. Refitted for every brand b (leave-b-out) by deterministic Newton steps, with no random draws. A fit that does not converge (100 steps, or a parameter beyond ±25) or has no informative brand gets δ = 0 for that (b, m); such events are counted and reported.
- **E = E_{b,m} = E0[C | n]**, from the exact null distribution of C (CEPs touched) given n: the generating function Π_j Σ_{k=0..s_j} C(s_j, k) e^{k·δ̂_j} x^k z^{[k ≥ 1]}, its x^n coefficient normalised over z. There is no Monte Carlo step: r0's master seed 112100 is no longer used by Cov*. Sensitivity S3: equal weights (δ = 0), where E = Σ_j [1 − C(S − s_j, n) / C(S, n)].
- c_max = min(n, number of CEPs with an answered run) (normally min(14, n)); c_min = the fewest CEPs that can hold n mentions (fill CEPs with the most answered runs first; normally ⌈n / 3⌉).
- **β_{b,m} = (c − E) / (c_max − c_min) when c_max > c_min, else 0** (n = 1, or so many mentions that every CEP must be touched). One linear normalisation, so its null mean is (E0[c] − E) / (c_max − c_min) = 0 at every n. β > 0: spread over more situations than situation-blind naming with the same mentions; β < 0: packed into fewer.
- **Cov*_b = 50 · (1 + mean of β_{b,m} over the panel's models with n_{b,m} ≥ 1)**, 0–100; 50 = situation-blind.
- **Rating floor:** Cov* is **rated iff n_b = Σ_m n_{b,m} ≥ 14** (at least one mention per CEP on average) **and at least 2 of the 3 panel models have n_{b,m} ≥ 1**; otherwise NOT RATED (no shrinkage, no imputation; never-named brands carry Presence's information, not Coverage's). Sensitivities S2: floor 6 (the v1.9 C* floor) and 28.
- **Sensitivity S8 (mid-p):** β_mid = 2 · [P0(C < c) + 0.5 · P0(C = c)] − 1 from the same exact null distribution; it also has zero null mean at every n. Cov*_mid = 50 · (1 + mean β_mid), same floors.
- **Why Cov* is not expected to move with the naming rate:** under situation-blind naming of the form above, E is the exact expected number of CEPs touched given n and β is linear in c, so β has zero expectation at every n, whatever the brand's naming rate; brand b's own answers do not enter its δ̂. Two things remain: the estimation noise in δ̂ (from the other brands' answers), which calibration N1 measures, and departures of real answers from the null's form, which H3 tests on the real answers.
- **Calibration N1 (before the lock; passed at r1).** Synthetic situation-blind data: 1,000 synthetic categories of 24 brands; naming rates p_b ~ Uniform(0.02, 0.98); unequal list lengths across CEPs through a shift d_j ~ Uniform(−1, 1) on the logit scale, common to every brand, model and run (brand b is named in an answer to CEP j with probability logistic(logit p_b + d_j)); 3 models, 14 CEPs × 3 runs, no missing cells; generator seed 112200. Rule: **|pooled centred ρ_w(Cov*, π_cov)| ≤ 0.05 over all rated synthetic units, and the mean Cov* of every naming-rate decile (0.1-wide bins of π_cov) within 50 ± 2.5.** Result (`calibration_N1_v1_12.json`, scorer SHA-256 `d97c46f7…`): pooled centred ρ_w = −0.0317; largest decile deviation 0.92 (decile means 50.04 to 50.92); mean signed per-category ρ = −0.0326; 22,005 rated units; no δ fit set to 0: **PASS**. Reported beside it: S8, ρ_w = −0.0533 with largest decile deviation 3.56; S3, ρ_w = 0.1604 (equal weights ignore list length); S9 (uncentred), ρ_w = −0.0197. Two earlier versions of Cov* failed N1 (§12).

### 2.5 Statistics
- **ρ_w:** pooled within-category Spearman: values ranked within category (average ranks), each category's ranks **centred on its mean rank** (r − (m_c + 1)/2), then Pearson r of the centred ranks over all units pooled. Centring removes the between-category component that uncentred pooling adds when categories contribute different numbers of units (found in the v1.10 work and confirmed on the published AIAS 2.0 values). Sensitivity **S9**: the uncentred v0.37–v0.41 convention (`pooled_within_rho`), reported, never changing a verdict. Only categories with ≥ 5 units in the comparison enter. Values compared unrounded.
- **Permutation p:** y permuted within category, 10,000 draws, p = (1 + hits) / 10,001; two-sided for separability, one-sided for reliability.
- **Bootstrap:** units resampled within category, 10,000 resamples, percentile 95% interval (reported; verdicts use point estimates).
- **Seeds:** 112001 (H1), 112002 (H2), 112003 (H3), 112004 (H4), 112005 (H5), 112006 (H6), 112007 (H7), 112008 (H8), 112020 (bootstrap), 112200 (N1 calibration). Seed 112100 (r0's Monte Carlo null draws) is no longer used.
- **n floor per test:** UNDETERMINED with fewer than **30** rated units pooled or fewer than **3** categories with ≥ 5 rated units.

### 2.6 Comparators (same panel, same week: t4 = v0.42, N3, S0)
- **P_N3:** v1.6 Presence on N3 = 100 · (C_P / 3 + 2 · π̂) / 3, with π̂ = v0.42's recall Presence π̂_{b,N3,S0} and C_P = number of N3 models whose v0.42 recognition code is "recognized" in a majority of their three S0 runs. Declared adaptation of v1.6's C_P/6 to a three-model panel: v0.42 defines recall Presence π̂ (§2.1) and recognition coding (§5.1) on the newest panel but no composite P and no C_P, so the adaptation stands (§13, item 2).
- **C*_N3:** 100 · (1 − φ_{b,N3,S0} / 9), φ as v0.42 §2.1 defines it (mean over defined runs); 9 = φ's maximum for 3 models × 6 frames (6M/(M − 1)); rated iff ≥ 6 total recall mentions (v1.9 rule). ρ is invariant to this rescaling.
- **π̂_N3** (recall arm alone) reported next to P_N3.
- **Fallback:** if t4 is not scored by the v1.12 analysis date, or N3 fails v0.42's drop rule, H1 and H2 use the published AIAS 2.0 t3 values (legacy panel) and are labelled cross-panel.

## 3. Hypotheses and verdict rules

Bands for every separability row: **CONFIRMED iff |ρ_w| ≤ 0.30; FALSIFIED iff |ρ_w| ≥ 0.50; MARGINAL otherwise; UNDETERMINED below the n floor (§2.5).** All on N3, S0, rated units.

| Tag | Tier | Statement | Statistic and data |
|---|---|---|---|
| **H1_Sep_Presence** | PRIMARY (gate) | Coverage breadth is separable from Presence. | ρ_w(Cov*, P_N3); units with Cov* rated; seed 112001 |
| **H2_Sep_Consistency** | PRIMARY (gate) | Coverage breadth is separable from Consistency. | ρ_w(Cov*, C*_N3); units with both rated; seed 112002 |
| **H3_Sep_NamingRate** | PRIMARY (gate; the v1.7 test inside the collection) | Cov* does not move with how often the brand is named in the same answers. | ρ_w(Cov*, π_cov); seed 112003 |
| **H4_Reliability** | PRIMARY (gate: reliability leg) | Cov* orders brands alike on the two CEP halves. | r = ρ_w(Cov*_A, Cov*_B), each half computed as §2.4 on its 7 CEPs (floor 7 mentions per half); rel = 2r / (1 + r). **CONFIRMED iff rel ≥ 0.50 and one-sided p < 0.05; FALSIFIED iff rel < 0.30 or p ≥ 0.05; MARGINAL otherwise**; seed 112004 |
| **H5_Sep_Ranking** | PRIMARY, **conditional** | Cov* is separable from Ranking. | ρ_w(Cov*, R*), R* = v1.10's locked statistic, extractor and floor applied to the t4 N3 S0 Phase B answers; seed 112005 |
| **H6_Sep_Sentiment** | PRIMARY, **conditional** | Cov* is separable from Sentiment. | ρ_w(Cov*, S), S = v1.11's locked score on the newest-model answers if a locked newest-model S exists at analysis; otherwise v1.11's locked omnibus S at t3, labelled cross-panel; seed 112006 |
| H7_Sep_Presence_Legacy | SECONDARY (downgrade only) | Separability holds against the published Presence. | ρ_w(Cov*, P_AIAS2.0,t3) (legacy panel, Nov 9); seed 112007 |
| H8_Panel_Replication | SECONDARY | Cov* replicates when Claude Opus 5.5 replaces Claude Fable 5.2. | ρ_w(Cov*_N3, Cov*_C3), units rated on both. **CONFIRMED iff ρ ≥ 0.70 and one-sided p < 0.05; FALSIFIED iff ρ < 0.50; MARGINAL otherwise**; seed 112008 |

**Activation rule (H5, H6).** Active only if tag `v1.10-prereg-r1` (H5) / `v1.11-prereg-r1` (H6), or a later revision, is pushed **before** the v1.12 lock commit; the v1.12 lock then records that tag, its commit and the file defining the score, which is used exactly as locked (its own unit, floor and rated set). Otherwise the leg is INACTIVE (no verdict) and may be tested only under a later pre-registration.

**GATE (Paper A verdict).**
1. **INSTRUMENT FAIL** if MC_Situation fails (§4): the situations do not change which brands are named, so Coverage cannot differ from Presence. Reported as a negative result; H1–H8 still computed for the record.
2. else **FAIL** if any of H1–H4 or an active H5/H6 is FALSIFIED → negative result with the same prominence as a pass (the v1.7 precedent); no Paper B on this instrument.
3. else **UNDETERMINED** if any of those is UNDETERMINED → data cause fixed and reported; no Paper B.
4. else **PASS** if all are CONFIRMED — downgraded to **MARGINAL** if H7 is FALSIFIED. A CONFIRMED H6 computed cross-panel is labelled so in the verdict.
5. else **MARGINAL** → Paper B only on Pablo's recorded decision, with the marginal leg as Paper B's first confirmatory test.

Secondary hypotheses never turn a FAIL into a PASS. The gate is repeated on C3 and on A4 (reported, no verdict change).

## 4. Manipulation and data-quality checks (numbers fixed)

| Id | Check | Rule |
|---|---|---|
| MC_BrandFree | No probe names a registry brand | 0 alias matches in all 75 probes (all registry aliases, at lock); a hit blocks the lock |
| MC_Complete | Answers obtained | ≥ 98% of the 900 calls answered (non-empty text, accepted served ID) after retries; a model below **90%** leaves the panel statistics (drop rule §7.3) |
| MC_Served | Served model = requested | any other ID: excluded, re-run in the re-run pass, logged |
| MC_Settings | Decoding settings as pre-registered | 100% of calls carry the recorded default settings (§6.4: no temperature, top-p, top-k or reasoning-effort parameter sent; maximum output 16,384 tokens; no system prompt; no tools); reasoning tokens reported per model |
| MC_Truncation | Output cap | > 5% of a model's calls ending at the output cap is flagged |
| MC_RegistryShare | Answers name registry brands | share of CEP answers naming ≥ 1 registry brand, per category; < 0.50 flags that category (its registry may not represent situation answers) |
| **MC_Situation** | Situations change the brand set (instrument gate) | per model × run × category: J_between = mean Jaccard of registry-brand sets between answers to different CEPs; J_within = mean Jaccard between runs of the same CEP (same model). **Pass iff pooled mean (J_within − J_between) ≥ 0.10 and pooled mean J_between ≤ 0.60.** Also reported: mean Jaccard of each CEP answer with the same model-run's control C0 answer |
| MC_Defunct | Known-group check | v0.22 cell D brands (Pontiac, Oldsmobile, Plymouth, Mercury, Saturn) named in ≤ 5% of automotive CEP answers; above it, flagged (phantom contamination; Paper B) |
| MC_Positive | Gate sensitivity | raw Cov must give |ρ_w(Cov, π_cov)| ≥ 0.50; otherwise the gate's sensitivity is flagged |
| MC_Window | Timing | all calls within 72 hours, none during 2026-11-17 to 2026-11-21, none overlapping t4 (§6.7) |

## 5. Cross-category baseline (descriptive; no verdicts)

Per category, model and panel: answers, missing cells, words per answer, registry brands named per answer, non-registry brand mentions (count only); raw Cov (k = 1, 2, 3) and Cov* distributions (median, IQR, range), rated counts; per-W coverage (which cue types each brand is named for); share of CEPs in which no registry brand is named; **run-to-run reliability** of the cell-level naming per model (rel1 = mean ρ_w over the three run pairs of each brand's per-run covered-CEP share; rel3 = 3·rel1 / (1 + 2·rel1)) — the noise floor for Paper B; agreement of the CEP answers with the control C0 answers; tokens and spend per model.

## 6. Collection

### 6.1 Probes
`probes_v1_12.jsonl`: 75 probes = 70 CEP probes (14 per category) + 5 control probes (C0). Template: `<situation> Which <noun> brands would you suggest? Name several brands.`; automotive asks `…would you suggest buying new?…` (rule R8). No probe names a brand, uses a superlative or repeats a Presence frame (`cep_sets_v1_12.md`, R4–R6). No system prompt.

### 6.2 Design
4 models × 75 probes × 3 runs = **900 calls**, each independent (no conversation state). N3 is the primary panel; Claude Opus 5.5 is collected for continuity (C3) and for the A4 descriptives.

### 6.3 Search: S0 only (S1 not justified in Paper A)
(1) The gate's comparators (P, C* from t4) are S0 measures; (2) Coverage is a memory-based availability construct, and search-on answers belong to Grounding (v1.13), which owns search; (3) S1 answers depend on the web on the day; (4) an S1 call carries about 15,000 to 40,000 input tokens (v0.39; v0.42 feasibility) against about 80 for an S0 call here. S1 Coverage is a Paper B study.

### 6.4 Decoding (as t4)
Exactly as t4 (v0.42 §4.4): temperature, top-p and reasoning effort are left at provider defaults; no temperature, top-p, top-k or effort parameter is sent. Claude Fable 5.2 accepts no temperature, top-p or top-k; its adaptive thinking is always on (default effort high). Maximum output **16,384 tokens** (the t4 cap). The gate's comparators (P, C* from t4) and this collection therefore share their settings. The settings sent are written to every call record (MC_Settings).

### 6.5 Order, retries, record
One worker per model, four in parallel; within a model: run 1 (probes in file order), then run 2, then run 3. Transient errors and empty answers are retried under the v0.39 policy (`_call_with_retry`), as in t4; calls still failing get one logged re-run pass inside the window. Resumable; every attempt logged. Record `osf/methodology/v1_12/data/v112_raw.jsonl`, one line per call: call ID, substrate, probe ID, W, half, requested and served model, run, prompt, answer text, finish reason, input, output and reasoning tokens, the decoding settings sent, start and end times (UTC), error, attempt count, and the tokens and list-price cost of every billed request. `osf/methodology/v1_12/scripts/acquire_v1_12.py` writes it: a fork of v0.42's acquisition script (git blob `c40bb5f2`), whose call functions and retry policy it copies byte for byte. It refuses to collect unless tag `v1.12-prereg-r1` is on origin and `osf/methodology/v1_12/anchor/osf_anchor_v1_12.json` names its commit, sends only inside the §6.7 windows, and sends a call in at most two passes (the main pass and one re-run pass). Its dry run (`dry_run_acquire_v1_12.txt`) makes no network call.

### 6.6 Cost and hard cap
Prices per 1M tokens in/out (verified Nov 10): Fable 5.2 $8/$40; Opus 5.5 $4/$20; GPT-6 Astra $10/$50; Gemini 4 Argon $2/$10 through Nov 30 and $4/$20 from Dec 1. Per model 225 calls; 80 input tokens per call (assumption: no system prompt; situation + question ≈ 30 words). Output tokens per call at provider defaults, reasoning included: the v0.39 current arm's S0 calls (30 per model; `osf/v39/data/v39_raw.json`, field `tokens_out`), as summarised in `osf/v42/prereg/cost_inputs_v0_42.txt` (mean; p90): Claude Opus 5.5 1,636.9; 2,234.5. GPT-6 Astra 619.0; 911.1 (reasoning mean 176.1 included). Gemini 4 Argon 1,165.8; 1,577.7 (thinking not recorded at S0). Claude Fable 5.2 has no such record (its only S0 record is v0.42's feasibility call), so it keeps the r0 scenarios of 1,000 and 2,500 tokens.

| Model | Calls | Expected (mean) | High (p90) | Worst (all at cap) |
|---|---|---|---|---|
| Claude Fable 5.2 (scenarios) | 225 | $9.14 | $22.64 | $147.60 |
| Claude Opus 5.5 | 225 | $7.44 | $10.13 | $73.80 |
| GPT-6 Astra | 225 | $7.14 | $10.43 | $184.50 |
| Gemini 4 Argon ($2/$10 through Nov 30) | 225 | $2.66 | $3.59 | $36.90 |
| **Total** | **900** | **$26.38** | **$46.79** | **$442.80** |
| Total if Argon at $4/$20 (from Dec 1) | 900 | $29.04 | $50.37 | $479.70 |

`cost_v1_12.csv` holds the table (`build_probes_v1_12.py`). The estimate is not a rule; the cap and the pause are. No coding cost: mention coding is deterministic (no judge). **Hard cap: US$120 for all v1.12 calls including retries.** Before each request the guard adds that request's worst case (200 input and 16,384 output tokens at list price) to the spend so far and to the requests in flight, and does not send it if the sum passes $120; once the recorded spend reaches **$80**, collection pauses and Pablo is asked before anything else is spent (`--approve-past-80`, logged). If every request ended at the cap, the guard would pause after 163 calls ($80.64) and stop after 242 calls ($119.24) (dry run). Unsent calls are missing cells.

### 6.7 Timing
- Pablo receives this draft → at least **24 hours** → lock and OSF anchor.
- One paid collection on the Mac at a time: v1.12 starts **only after t4's last call is logged** (v0.42 collects Nov 11–13).
- Never during **2026-11-17 to 2026-11-21** (v0.40).
- **Earliest collection: 2026-11-14 00:00 UTC**, to end by **2026-11-16 23:59 UTC** (900 calls need hours, not days). If that window is missed: **2026-11-22 12:00 UTC to 2026-11-29 23:59 UTC** (after v0.40 in any US time zone, before Argon's price change and before t5's target of Dec 3).

## 7. Analysis plan

### 7.1 Computation
All statistics by `osf/methodology/v1_12/scripts/score_v1_12.py`, unit-tested on synthetic data (`tests/test_score_v1_12.py`: 46 tests at r1, all pass) and calibrated (N1, §2.4); SHA-256 in the lock manifest; run once after the parity gates. At r1 the scorer holds the core: β and Cov* with the Rasch-type and equal-weight nulls, S8, the floors, ρ_w (centred; S9 uncentred), permutation p, bootstrap, the §3 verdicts and gate, MC_Situation and N1. The coding step (v0.42's coder, §2.3), the comparators of §2.6, the other §4 checks, the §5 descriptives and the remaining §7.4 sensitivities are added and tested before the lock. Choices where this document is silent are listed in the scorer's SCORER_NOTES.

### 7.2 Parity gates (before any v1.12 statistic)
- **P1.** The v1.12 coder, applied to the t3 omnibus Phase B answers, reproduces the locked t3 mention codes exactly (as v0.42 P2).
- **P2.** P_N3 and C*_N3 are recomputed from v0.42's locked outputs and match v0.42's π̂ and φ exactly.
- **P3.** Probe parity: the probes sent equal `probes_v1_12.jsonl` byte for byte.
A failed gate stops scoring; the fix is logged in `osf/methodology/v1_12/anchor/DEVIATIONS.md` first.

### 7.3 Drop rule and missing data
A model with fewer than 90% of its calls answered leaves the panel statistics (reported). If Claude Fable 5.2 drops, C3 replaces N3 (declared fallback); if GPT-6 Astra or Gemini 4 Argon drops, H1–H4 are computed on the remaining models and labelled two-model (gate at most MARGINAL). No imputation.

### 7.4 Sensitivity analyses (reported; never change a verdict)
S1 raw Cov through H1–H3 (expected to fail; reported beside the gate). S2 rating floors 6 and 28. S3 equal-weight null. S4 β computed only for models with room to vary (c_max > c_min). S5 leave-one-category-out ranges. S6 leave-one-W-out Cov* (does one cue type drive breadth?). S7 comparators π̂_N3 and total t4 mentions in place of P_N3. S8 mid-p β (§2.4). S9 uncentred ρ_w (§2.5). S10 H1–H4 without the brands that the 2026-11-10 COI re-check flags (§8). Verdict changes under any sensitivity are listed next to the verdict.

## 8. Declarations

**Conflict of interest.** The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Samsung does not market brands in skincare, cosmetics, passenger cars or premium spirits. In audiophile headphones, Samsung's subsidiary Harman International owns brands in the category; v0.19 substituted Denon for AKG at its lock (record quoted below). v1.12 performs no new brand selection: it uses the registries fixed in v0.19–v0.23, and each keeps its source-phase handling. A 2026-11-10 re-check of the current ownership of the registry brands awaits the author's decision on its handling; its result and handling are recorded here before the lock, and every gate statistic is also reported without any brand it flags (sensitivity S10). The CEPs name no brand; headphone situations stay inside audiophile listening (rule R8b) because consumer, sport and true-wireless uses are where Samsung-owned brands compete. Non-registry brands named in answers (which may include Samsung-owned brands) are not scored; their mention counts are reported as a count only. The two source records, verbatim:

> v0.19 (`osf/v19/PRE_REGISTRATION_v0_19.md`, §2.3): "**AKG removed from Cell A short-list; Denon substituted.** AKG is Samsung-owned since 2016. The author's COI declaration names Samsung; including AKG would invite the kind of reviewer suspicion AIAS™ 1.0 does not need to absorb. Denon carries comparable heritage stature (founded 1910; AH-D7000 → D9200 audiophile line) and removes the question. Decision rationale recorded here for audit trail."

> v0.22 (`prereg/v0_22_mega_prompt.md`, DEVIATIONS Entry 0, Part B — COI screen): "**Screen result:** Three of the 24 brands in the locked v0.22 registry have tier-2/3 supply relationships with Samsung Electronics America (author's primary employer) via Samsung subsidiaries: BMW (Harman audio + Samsung SDI batteries + Samsung Display infotainment), Mercedes-Benz (Harman audio + Samsung Display infotainment), and Volkswagen Group brands including Bentley and Porsche (Samsung SDI battery supply to Stellantis-adjacent platforms). Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are all tier-2/3 non-competitive supply relationships, not brand-level competition. Samsung Electronics America does not produce or market passenger car brands. The COI relationship does not affect brand recognition or recall measurement by LLM panel and does not impose operational restriction on registry composition."

Acquisition, coding and scoring are automated against the locked registries; this pre-registration is locked and deposited before any v1.12 call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

**Funding.** Self-funded. **Ethics.** Not applicable; no human subjects.

**Use of AI tools.** The author used Anthropic's Claude to assist with analysis code, drafting and editing of text, and figure production. The study design, pre-registered hypotheses and decision rules, and all interpretations are the author's; the author reviewed all content and takes full responsibility for it. The CEP sets were drafted with Claude Opus 5.5, which is also a panel model (`cep_sets_v1_12.md`, R10).

## 9. Limitations

1. One CEP set of 14 situations per category, drafted by one procedure (and by a model that is also a panel arm); sensitivity to the set is Paper B's first study.
2. Coverage is measured among registry brands only (16–24 per category); answers also name other brands.
3. Three runs per cell estimate within-situation noise only coarsely; Cov* needs all three (it uses runs as replicates), so its reliability is judged across CEP halves of 7, which is conservative.
4. N3 and C3 share two models; φ and C* on three models are noisier than on six.
5. One market and language (US English), S0 only; no CEP is weighted by how common it is among buyers (Ehrenberg-Bass practice weights CEPs by prevalence; that needs buyer data).
6. Cov*'s null is a logistic model without brand × situation interaction, estimated from the other registry brands; N1 checks it on synthetic data of that form only.

## 10. What Paper B inherits (not pre-registered here)

Only after PASS (or MARGINAL with Pablo's recorded decision): the frozen CEP sets, probe files, coder and scorer; per-answer mention tables (SHA-256 pinned); Cov and Cov* per unit next to P, C*, R* and S for the **typology** (broad vs situation-bound brands; deviations from Double Jeopardy); the studies — **CEP-set sensitivity** (an independently, human-authored parallel set; leave-one-W-out; CEP weights from buyer data), **phrasing** (fixed list length, "best for…" wording, second person, a market cue), **phantom** (v0.22 cell D and Fisker in situation answers; phantom-brand bands), **identity load** (situations by cue type against the registries' identity cells), **S1** Coverage with Grounding (v1.13), model-version stability (Fable vs Opus), and re-asks at t5/t6 for temporal stability; plus the MC_Situation, N1 and permutation null distributions and the Paper A verdict file.

## 11. Predictions (before any v1.12 answer exists)

MC_Situation lean pass (situations visibly change lists). Raw Cov tracks Presence (|ρ| ≥ 0.50, as Double Jeopardy predicts). H1 lean MARGINAL: big brands are named in nearly every situation, which compresses their β toward 0 while niche brands spread both ways. H2 lean CONFIRMED. H3 lean CONFIRMED (β has zero null mean at every n; N1 passed). H4 lean MARGINAL (7 CEPs per half). H8 lean CONFIRMED.

## 12. Lock procedure and change log

Between sending and lock, clarifications that change no hypothesis, threshold, panel, probe or decision rule are logged here; any other change restarts the 24 hours. Lock: refresh `LOCK_MANIFEST_v1_12.sha256` (this file, CEP and probe files, cost table, builder, N1 and dry-run records, scorer, acquisition script and tests); commit; tag `v1.12-prereg-r1`; push; deposit `osf/methodology/v1_12/prereg/` and `anchor/` at OSF and verify their SHA-256 there; only then collect.

**Change log.**
- 2026-11-10: r0 drafted (not sent).
- 2026-11-10: r1 — runner decisions on §13 applied; sent to Pablo.
- 2026-11-10, r1, before sending: r0's beta failed calibration N1 (mean per-category |rho| 0.5234; its two-sided normalisation has a non-zero null mean); r1 replaces it by a single linear normalisation and restates N1 as a pooled statistic, because the per-category mean |rho| has a noise floor of about 0.18. A first r1 version that kept r0's length-weighted Monte Carlo null also failed the restated N1 (pooled centred ρ_w 0.1732): list-length weights do not reproduce how a situation-blind brand spreads across CEPs. r1 therefore uses the Rasch-type null of §2.4, which passed (pooled centred ρ_w −0.0317; every decile mean within 50 ± 0.92). ρ_w is now centred within category (§2.5; S9 uncentred). The two failed runs are kept in `calibration_N1_v1_12.json` (history).

## 13. Settled before sending (runner, 2026-11-10)

1. **Decoding:** provider defaults exactly as t4 (§6.4); no program rule requires the lowest effort. MC_Effort replaced by MC_Settings (§4); r0's Limitation 5 removed; cost re-estimated at defaults (§6.6). Cap US$120, pause at $80.
2. **P on three models:** v0.42 defines recall π̂ (§2.1) and recognition coding (§5.1) for the newest panel but no composite P or C_P, so the C_P/3 adaptation is kept (§2.6).
3. **Floors:** Cov* floor 14 and per-half floor 7 kept.
4. **β:** kept as the within-model, rate-adjusted breadth score; its normalisation and null were changed when calibration N1 failed (§2.4, §12).
5. **MC_Situation thresholds:** kept (difference ≥ 0.10; J_between ≤ 0.60).
6. **Scripts:** `score_v1_12.py` core with 46 unit tests (all pass) and N1 (PASS); `acquire_v1_12.py` with its dry run; v0.42's coder pinned by blob (§2.3) and re-checked at the v1.12 lock.
7. **H5 data:** R* on the t4 N3 S0 Phase B answers, as drafted.
8. **H6:** the cross-panel fallback is accepted.
9. **Category nouns:** each substrate's first Phase B frame (R7), so "cosmetics" for v0.21; the automotive "buying new" wording kept (R8).
10. **Headphones COI care:** rule R8b and count-only reporting of non-registry brands kept.
11. **CEP review and cue list:** Pablo reviews the 70 situations during the 24 hours; the cue list is described as the program's own operationalisation after Romaniuk & Sharp's category entry points, with no claim about a "7W" source.
12. **"Phase Q's taxonomy step":** not needed for Paper A.
13. **Window:** as drafted (§6.7).

**For Pablo (24-hour review).**
- Review the 70 situations: `cep_sets_v1_12.md` §3, with the known soft spots in §4. Edits keep R1–R10 and the two-per-W balance and are logged (R11).
- v0.21's own Phase B frames split three and three: "cosmetics" in q1, q3 and q4, "makeup" in q2, q5 and q6 (`prereg/v0_21_registry.json`, `phase_b_frames`). The probes use "cosmetics", the noun of the first frame; say if you prefer "makeup".
- Cov* changed twice before sending (§2.4, §12): r0's score failed its own calibration, and so did a first fix; the version here passed. §2.4 is the paragraph to read.
- Claude Fable 5.2's cost at defaults is a scenario, not a record (§6.6); the cap and the pause hold whatever the estimate.
