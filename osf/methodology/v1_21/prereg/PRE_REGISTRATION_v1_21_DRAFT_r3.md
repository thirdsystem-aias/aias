# AIAS v1.21 — Sentiment, redesigned measure: co-mention tone, confirmed blind on t5

AIAS™ Measurement Program — Third System™. **Status: DRAFT r3 (2026-11-23), not locked, not deposited.** Branch `sentiment-redesign` (from `sentiment-successor` @ `6efbd33`, which holds v1.20's scored outputs and continued DEVIATIONS). r2 applies the author's decisions of Sun 2026-11-22, 4:38 pm CT ("ok v1.21, Cheil on"), which accepted all eight recommended answers of r1's open questions; each is recorded in §16 as decided Sun 11/22 by the author, and no question remains open. The 24-hour rule before the lock runs from the time r2 reaches Pablo. Lock target: tag `v1.21-prereg-r1`, pushed, with `anchor/git_anchor_v1_21.json` and the OSF deposit of `osf/methodology/v1_21/prereg/`, `dryrun/` and `anchor/`, **before the first t5 call** (v0.45 window opens Thu 2026-12-03 06:00 UTC) and therefore before any t5 answer is coded or judged.

**r2 → r3 (2026-11-23), wording only.** r3 writes into the text 16 choices that r2 left to the code and that the draft scorer (`scripts/score_v1_21.py`) had already taken; each now reads as the code does (§19 lists them). Two places where the draft scorer did less than r2 promised were brought up to r2 in the code, and r3 names the files involved: n_named takes U0's extraction misses from U0's record `prereg/u0_v1_21.json` (§4.2, §6), and Pins checks v0.45's raw, coded and scored files at named paths (§9). No hypothesis, threshold, band, gate, floor, seed, sample, cost, decision of §16 or the COI paragraph changes. r2 is kept unchanged beside r3.

**Pre-registrant:** Pablo Ulpiano González Castro

Nothing in this draft was computed on data. Every number below is copied from a named file in the repository (§15 lists them). No model call, no data acquisition and no scoring was done to write it.

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.21 (decided Sun 11/22 by the author; §0 note) |
| PHASE_TITLE | Sentiment redesign: co-mention tone (TONE), separability from Presence confirmed once on the unseen t5 wave |
| PHASE_TYPE | methodology lock; paid judge calls on t5 answers only (no answer collection of its own; t5 is collected by v0.45 under its own pre-registration) |
| Decision of record | Pablo, Sun 2026-11-22, 12:34 pm CT: "Yes sentiment needs redesign. The difference was minimal." Design decisions: Pablo, Sun 2026-11-22, 4:38 pm CT: "ok v1.21, Cheil on" (all eight recommended answers; §16) |
| Redesign precedent | Ranking: v1.14 (modal position, confirmed blind on t4 and t5) and v1.16 (co-mention precedence, justified in advance from the method; tag `v1.16-prereg-r1`) |
| Confirmatory data | t5 = v0.45 (tag `v0.45-prereg-r1`; collection from Thu 2026-12-03 00:00 CT, at most 72 hours), N3 panel, search off (S0), category answers (Phase B) |
| Judge | v1.11's judge, prompt and call parameters, unchanged, with v1.20's reply-extraction rule declared in advance (§5) |
| Gate | v1.11's separability bands, unchanged: \|ρ\| ≤ 0.30 CONFIRMED, \|ρ\| ≥ 0.50 FALSIFIED, between MARGINAL (§7) |
| LABEL | Sentiment stays **provisional** (AI-judged) until Paper B's human-label validation (on hold); §11 |

**Id.** Methodology studies take the next v1.N id (CLAUDE.md, pre-registration discipline: tag `v1.N-prereg-rN`). On 2026-11-22 the repository has `osf/methodology/` folders and branches up to v1.20 on every local branch, tags up to `v1.20-prereg-r1`, and no ref or folder named v1.21; the only occurrence of the string "v1.21" is a deliberately invalid value in a unit test (`scripts/test_score_v1_20.py`, line 271). `brand/report_specs.json` defines document types, not study numbers, and has no entry to check. v1.21 is therefore the next free id; the id v1.21 was decided Sun 11/22 by the author (§16, decision 1).

### 0.1 Lineage and the result that triggers the redesign

- **v1.11** (Sentiment Paper A, tag `v1.11-prereg-r1`): AI-judged valence of mention windows, S = mean unit score over a brand's windows, rated at n ≥ 6. Its Stage J halted on JUDGE_FAIL (case B; v1.11 DEVIATIONS continued Entry 3).
- **v1.20** (tag `v1.20-prereg-r1`, the pre-registered successor re-scoring; Sentiment Paper A's result in case B): `osf/methodology/v1_20/outputs/v1_20_verdicts.json`:
  - H1 judge agreement CONFIRMED: ordinal α 0.8735 over 3,650 units judged by both; brand ρ_w 0.8741 (n 163).
  - H2 separability from Presence **FALSIFIED**: ρ_w(S, P) 0.4771 (t1, n 55), 0.4477 (t2, n 54), **0.5013 (t3, n 54)**; the three-wave rule falsifies at any wave ≥ 0.50.
  - H3 separability from Consistency CONFIRMED: 0.0600 / −0.0156 / 0.1489.
  - H4 stability t1 → t2 CONFIRMED, ρ 0.7345 (n 53); H6 t2 → t3 CONFIRMED, ρ 0.7431 (n 52).
  - H5 separability from Ranking (MNP) MARGINAL: 0.4397 / 0.3855 / 0.4182.
  - H7 naming frequency in the eight early categories FALSIFIED: \|ρ_w(S, n_named)\| 0.5323 (n 136).
  - H8 recognition score vs Presence MARGINAL: 0.2304 / 0.3415 / 0.2674 (n 24 each).
  - Sensitivity verdict changes (same file, `sensitivities.verdict_changes`): H2 FALSIFIED → MARGINAL without cut answers (S-CUT) and without cut cells (S-CUT-M). Under v1.11 §5.1 and v1.20 §4 a sensitivity never changes a verdict.
- **Integrity statement.** H2 missed CONFIRMED at every wave (all three values are above 0.30) and crossed the FALSIFIED line by 0.0013 at one wave. A narrow miss of the 0.50 line is not a reason to move it, and this draft does not move it (§7). The redesign is a new measure, justified from the method before any value of it exists, and tested once on answers that the failed test never saw.

## 1. Diagnosis, and the reasons for each design choice (written before any data is touched)

### 1.1 What S already is

v1.11's S is already **conditional on being named**: an F unit exists only for a (answer, brand) pair in which the certified mention record says the answer names the brand (v1.11 §4.1), and S is the mean over those units. "Tone among answers that name the brand" is therefore v1.11's S itself, and it is the measure that failed H2. It cannot be the redesign. It is kept as a reference secondary (S_ref, §3.4) so that the failed measure is re-measured on the new wave.

### 1.2 Channels through which naming frequency can enter S without being tone

Mirroring v1.16 §1.1 for Ranking: S averages a brand's unit scores over the answers that name it. That sampling frame lets how often a brand is named enter S through properties of the average, not of how the brand is described:

1. **Answer register.** All brands in one answer share that answer's register: a model's warm "best of" answer describes every brand it names more warmly than a terse list does. A brand named in many answers averages over many registers; a rarely named brand appears mainly where a model goes further down a list. The near-neutral rule scores a bare window 0 (50 on the unit scale) and keeps it (v1.11 §4.3); bare windows were 223 of 2,781 F windows, 8.0% (v1.11 §4.1, U0, `prereg/u0_v1_11.json`).
2. **Model and run mix.** Answering models differ in how warmly they write (v1.11 descriptive 6.3, mean u by answering model). A brand's mix of answering models and runs follows how often each model names it.
3. **Substance.** Models may describe the brands they name most as the best. This is the question, not an artefact.

Channels 1 and 2 are construction; channel 3 is what the gate asks about. S cannot tell them apart. Two archived readings are consistent with channel 1 carrying part of the overlap, without proving it: with NV (mean unit score among evaluative units only) in place of S, ρ_w(NV, P) is 0.5094 / 0.3234 / 0.3849 (t1 / t2 / t3; `v1_20_verdicts.json`, `sensitivities.S_NV_in_place_of_S.H2`), lower than S at t2 and t3 but not at t1; and in the early panel S tracks the count of answers naming the brand at 0.5323 (H7). These readings motivate the design; they are not evidence for it, and the new measure is not fitted to them.

### 1.3 Pablo's three candidates, judged on principle

| Candidate | What it is | Judgement (reason) |
|---|---|---|
| (a) Conditional tone: tone among answers that name the brand only | v1.11's S (§1.1) | Not a redesign: it is the failed measure. Kept as reference secondary S_ref. |
| (b) Tone relative to the category mean | S minus its category's mean S | **Cannot change the gate.** ρ_w is computed on ranks within each category (v1.11 §5 conventions); subtracting a category constant leaves every within-category rank, and so every ρ_w, unchanged. It changes only the published level (comparability across categories). Reported as a presentation format only (S_cat, §3.4), never as a test. |
| (c) Residualised tone: S with its linear dependence on P removed | residual of S regressed on P within category | **Passes the in-sample gate by construction** (the residual is uncorrelated with P on the data that fitted it), so the gate would test nothing; it also defines the overlap away instead of measuring how a brand is described. Kept as a secondary only in an out-of-sample form (coefficients fitted at t4, applied at t5; S_res, §3.4), with no gate role. |
| (d) **Co-mention tone (TONE), primary** (decided Sun 11/22 by the author) | for every pair of brands named in the same answer, which one the judge rated more warmly; one strength per brand from all such head-to-heads in the category | Removes channels 1 and 2 by construction (§1.4); leaves channel 3, which is the question. The Sentiment analogue of v1.16's PREC. |

### 1.4 The primary measure: co-mention tone (TONE)

**Definition in one sentence.** TONE_b is the Bradley–Terry log-strength of brand b in "described more warmly than", estimated from every pair of registry brands named in the same t5 S0 answer, where the outcome of each pair is decided by the two windows' J1 unit scores.

**Why this, and not something simpler.** Comparing two brands inside one answer holds fixed everything the two windows share: the answering model, the run, the question and frame, the answer's register and its length. So:

- answer register and model mix (channels 1 and 2) do not enter the **direction** of a comparison: a model that writes every window warmly gives warm scores to both members of every pair in that answer;
- naming frequency changes only the **number** of comparisons a brand has (the precision of its estimate), not their expected outcome (to be shown by unit tests on synthetic data before the lock, as v1.16's `test_frequency_does_not_enter_direction`);
- the rival mix is modelled, not averaged over. A plain within-answer contrast (a brand's score minus the mean of its co-named rivals) does not do this: a rarely named brand appears mostly next to the most-named brands, so its contrast would depend on how those leaders are described. Bradley–Terry adjusts every head-to-head for the rival's strength. The plain contrast is kept as secondary CONTRAST (§3.4) so that the effect of the adjustment is visible.

What TONE cannot remove is channel 3, and it should not: if the brands models name most are also the ones they describe more warmly than the brands named beside them, TONE will track Presence, and that overlap is substantive (v1.16 §1.2, same logic). Then Sentiment, as described in AI answers, is not separable from Presence, and the consequence clause applies (§8).

**Why the judge task does not change.** The judge still rates one window at a time, blind to the other brands' windows, on v1.11's five-point anchored scale. The pairs are formed afterwards, from independent unit judgements. So there is no new judge, no new prompt and no new unit, and Paper B's human labels (on hold), which validate the unit judgements, validate TONE's inputs too.

**Why Bradley–Terry with v1.16's estimator.** It is the estimator of the program's locked co-mention measure (v1.16 §3.2), already implemented and tested (`score_v1_16.fit_bt`, tag `v1.16-prereg-r1`: λ = 1 virtual comparison per brand against a reference of log-strength 0, Newton–Raphson with step halving, tolerance 10⁻¹⁰, at most 500 iterations). Importing it unchanged avoids writing and tuning a new estimator after the failure. Ties (equal unit scores) give half a win to each brand, as in v1.16.

**Why pairs are decided by the order of the unit scores, not by the size of the difference.** The valence scale is ordinal (H1's α is ordinal; v1.11 §4.2), so only "warmer, equal, cooler" is used. A neutral window beside a positive one is a loss: being described plainly next to a brand described warmly is the comparative fact TONE measures.

## 2. Research questions

- **RQ1.** Is co-mention tone separable from Presence (and from Consistency) on the t5 wave, which no Sentiment test has seen?
- **RQ2.** Is it reliable: does the brand order by co-mention tone hold from t4 to t5 beyond what list composition produces?
- **RQ3 (exploratory, after the lock).** On the archived legacy waves t1–t3, how does TONE relate to Presence compared with S?

## 3. The statistic

### 3.1 Comparisons

Within one wave and one category (substrate), every answer that has **valid J1 judgements for at least two registry brands** contributes, for every pair of those brands, one comparison:

- **unit score** u = 25·(valence + 2) ∈ {0, 25, 50, 75, 100} from J1's judgement (v1.11 §4.4); units with `refers_to_brand = false`, JUDGE_FAIL or UNJUDGED do not enter (v1.11 §4.3, §4.2);
- the brand with the higher u wins; equal u is a tie, half a win to each;
- every comparison has weight 1 (an answer with k valid brands gives k(k − 1)/2 comparisons; v1.16 primary). Weight 1/(k − 1) per comparison is sensitivity S_w;
- comparisons are pooled over models, runs and questions of the category and wave into one win matrix W (W_ij = weighted wins of i over j), as v1.16 §3.1 pools.

An answer that names one brand gives no comparison. Its window is still judged (H1 uses it) and still enters S_ref.

### 3.2 Estimation and scale

TONE_b = θ_b from `score_v1_16.fit_bt(W, prior=1.0)`, imported unchanged from tag `v1.16-prereg-r1`; the objective is v1.16 §3.2's (Bradley–Terry log-likelihood plus λ = 1 virtual comparison per brand, half won and half lost, against a reference of log-strength 0). Higher TONE = described more warmly than the brands it is named with. λ = 0.1 and λ = 10 are sensitivity S_prior. Brands below the rating floor enter the fit as rivals. For publication only, TONE may be mapped to 0–100 by 100·σ(θ_b) (the modelled probability of being described more warmly than a reference brand); the mapping is monotone and changes no test.

### 3.3 Rating

A unit (category, brand) is **rated** at a wave iff it has **≥ 6 answers contributing a comparison** (v1.11's n ≥ 6 floor, applied to the answers that carry TONE's information) **and** lies in the largest connected component of the category's comparison graph (v1.16 §3.3). Never-named brands are not rated (absence is Presence's information). Floors 3 and 10 are sensitivity S_floor. Units at the floor outside the main component are counted (check MQ9, §9).

### 3.4 Pre-declared secondary measures (reported beside TONE; none has a gate role)

| Id | Measure | Why it is reported |
|---|---|---|
| CONTRAST | mean over the brand's contributing answers of (u_b − mean u of the other valid brands in that answer); same floor (rated iff ≥ 6 contributing answers; no connected-component condition, since CONTRAST is not a fitted strength) | shows what the rival-strength adjustment of TONE does |
| S_ref | v1.11's S (mean u over all the brand's valid windows, n ≥ 6), with v1.11's code | the failed measure, re-measured on the unseen wave; its H2_t5 value is reported as a replication of v1.20's H2, with no gate role |
| S_cat | S_ref minus the mean S_ref of its category's rated units at the same wave | a presentation format (§1.3 b); within-category ranks equal S_ref's, so every ρ_w equals S_ref's; the scorer checks this identity, nothing is tested |
| S_res | t5 residual of S_ref on P_S0 within category, with intercept and slope per category **fitted at t4** and applied at t5: least squares on the t4 units rated on S_ref that have P_S0, then S_res = S_ref,t5 − (a_c + b_c·P_S0,t5); a category whose t4 fit has fewer than 2 units or no spread in P has no S_res (counted) | the only form of candidate (c) whose correlation with P is not zero by construction; no gate role (§1.3 c) |
| TONE_NV | TONE from pairs in which both windows are evaluative (`evaluative = true`) | removes the near-neutral channel (§1.2 item 1) entirely, at a loss of pairs |

## 4. Data and inputs

### 4.1 Waves and answers

- **t5 (confirmatory).** v0.45's S0 category answers (Phase B, search off): 3 models (N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon) × 30 questions (6 per omnibus category) × 3 runs = 270 answers, 54 per category (v0.45 §4.2, tag `v0.45-prereg-r1`; v1.15 §2 for the same design at t4), read at tag `v0.45-acquisition-locked`, after v0.45's analysis-set and model-drop rules (v0.42's functions, as v1.15 §2 applies them at t4). Mention record: v0.45's coded Phase B tables (certified coder; as v1.15 §3 at t4). Five omnibus registries (v0.19–v0.23, 112 brand units).
- **t4 (secondary and retest).** v1.15's frozen J1 and J2 replies on the 1,547 judged t4 S0 windows (`osf/methodology/v1_15/outputs/judge_outputs_frozen_v1_15.json`, branch v1.15: 3,353 records; raw SHA-256 `926ed9b0505608a273a089d6395fc63b4d235f142247b00718191c4f9a9db01a`), re-scored under v1.20's extraction rule (§5). v1.15's own halt stands, and no v1.15 file changes. No S, TONE or other Sentiment score has ever been computed on t4 (v1.15 halted at Stage J before scoring; v1.20 §10 used those replies for format counts only), so t4 is also unseen by the failed test. Its use (the stored replies, US$0, for the t4 → t5 retest H4 and the downgrade-only check H5_t4) was decided Sun 11/22 by the author (§16, decision 4).
- **t1–t3 (exploratory only, after the lock).** v1.11's frozen J1 judgements as v1.20 scored them (`osf/methodology/v1_20/outputs/unit_outcomes_v1_20.csv`; answer ids from `osf/methodology/v1_11/prereg/units_v1_11.csv`, column `answer_id`). Used only for RQ3, only after the lock is anchored, labelled exploratory, never in a verdict (§10). These waves produced the failed H2; any TONE value on them is a description, not a test.

### 4.2 Units and windows at t5

v1.11's F rules unchanged (v1.11 §4.1; v1.15 §3): one brand-block window per (answer, brand) for every brand the certified record says the answer names, matching on the whole answer, cap 1,500 characters, extraction misses counted (> 5% of a category's mentions halts before any judge call). **Window cap per brand:** v1.11's 36 windows per brand × set × wave drops windows and so breaks pairs; at t4 it removed 97 of 1,644 windows (`osf/methodology/v1_15/prereg/u0_v1_15.json`, `units`). At t5 every window is judged (no cap), because TONE needs every co-mention and the cost is small (§12); decided Sun 11/22 by the author (§16, decision 5). The cap is removed at t5 only: the t4 replies are v1.15's frozen record as judged under v1.11's cap, and no t4 window is added or re-sent. U0 (unit build) runs after `v0.45-acquisition-locked` and v0.45's coding, before any judge call, and fixes the unit table's SHA-256. The t5 files take v1.15's names and v1.11's unit and record formats, in the t5 folder given to Stage J: `prereg/units_v1_21.csv` (U0 unit table), `prereg/u0_v1_21.json` (U0's record, in v1.15's `u0_v1_15.json` format: per-set mentions, windows and misses, the unit table's SHA-256 under `units_file`, and the list `extraction_misses` of every (answer, brand) the certified record names without a window, written as an empty list when there is none), `outputs/judge_outputs_frozen_v1_21.json` (frozen judge record, holding the unit table's and the raw file's SHA-256) and `data/judge_raw_v1_21.jsonl` (stored replies). Stage J refuses if U0's record is absent, has no `extraction_misses` list or names another unit table, and re-applies the 5% miss check from its per-set counts. J2 judges every t5 window (v1.11's F rule); the self-consistency repeat is v1.11's 5% sample (seed 111003's rule, new seed §6).

### 4.3 Presence, Consistency and Ranking at t5 and t4

- **P_S0 and C\*_S0 at t5:** the program's shared N3 definitions (as v1.15 §5.2 uses them at t4), computed by v0.42's own functions as imported by `osf/v45/scripts/score_v0_45.py`, read from v0.45's scored output with its SHA-256. That output is v0.45's scored unit table (`osf/v45/v45_unit_table.csv`): P_S0 is its column `P_t5_S0`; it holds φ, not C\*, so C\*_S0 at t5 is v0.45's own transform 100·(1 − φ/9) of `phi_t5_S0` where `phi_partition_t5_S0` is `defined`, 100 where it is `saturated`, and missing otherwise (`score_v0_45.h_stab_consistency`, `C_star_alongside`), with no C\* rating floor applied. If v0.45 has not been scored when Stage C is due, Stage C waits; it never computes its own P.
- **P_S0 and C\*_S0 at t4:** v1.14 Stage 1's units (`stage1_v1_14.json`, `units[]`: `P_S0`, `C_star_S0`), as v1.15 §5.2.
- **Ranking.** v1.16's gate did not pass: "NOT PASS: Ranking is reported as part of Presence and not as a separate AIAS component. There is no further Ranking redesign." (`osf/methodology/v1_16/outputs/results_v1_16.json`, `CONSEQUENCE`, branch v1.16). Separability from Presence therefore covers it; ρ_w(TONE, R\*) with v1.14's modal position at t5 (v1.14 Stage 2's rank table, when it exists) is reported as a descriptive only, with no gate role (decided Sun 11/22 by the author; §16, decision 6).
- **Opening order.** P, C\* and R\* are opened only at Stage C, after Stage J (judge gate, TONE values) is written and hashed (§13).

### 4.4 What was looked at before this draft (declared)

Read, as text: the pre-registrations of v1.11, v1.14 (headings), v1.15, v1.16 (§0–§9), v1.20 and v0.45 (summary, §2.1, §2.6, §4.1–4.2, §4.6, §6); the aggregate verdict file of v1.20 (`v1_20_verdicts.json`: verdicts, per-wave ρ, sensitivity summaries); v1.15's frozen-output summary and U0 counts; v1.16's results file (gate, consequence, H1 summary); the column headers of v1.11's unit table and of v1.20's unit-outcome file; the master documents (both CLAUDE.md files; STATUS.md lines on t5). **Not read or computed:** any judge reply text, any per-unit valence, any TONE or contrast value on any wave, any t5 material (none exists).

## 5. Judge (v1.20's, reused; no new judge)

- **Reused unchanged from v1.11** (`osf/methodology/v1_11/prereg/judge_prompt_v1_11.md`; `scripts/judge_v1_11.py`, `scripts/score_v1_11.py` at tag `v1.11-prereg-r1`): J1 Claude Opus 5.5 (`claude-opus-5-5`, Message Batches API), J2 GPT-6.1 Sol (`gpt-6.1-sol`, Batch API, `/v1/responses`), alternate Gemini 4 Argon (`gemini-4-argon`) under v1.11's replacement rule; the same prompt, no sampling parameter, lowest effort ("low"), output cap 4,096 tokens, prompt-only JSON, no tools; blinding (the judge never sees the answering model, the wave, any other brand's window or any P, C\* or R value); served-model check; 2 retries on invalid output; phase order and shuffle.
- **Extraction rule: v1.20's, declared in advance** (`scripts/score_v1_20.py`, `parse_reply` and `outcomes`, tag `v1.20-prereg-r1`; v1.20 §3–§4 with its switches as Pablo set them in `prereg/config_v1_20.json`): a reply counts when it holds exactly one complete JSON object that passes v1.11's checks; surrounding text is ignored; two or more objects, a cap-cut reply or no object are invalid; the first stored reply that counts is the judgement. This applies the program rule "LLM judges and strict JSON" (CLAUDE.md, Nov 12, 2026) to a study not yet locked. JUDGE_FAIL above 2% of any category's units per judge halts before scoring (v1.11 §4.2), at both scored waves (t5 and the re-scored t4; §9).
- **Why no new judge.** H1 passed with α 0.8735 and brand ρ 0.8741 (`v1_20_verdicts.json`); TONE uses the same unit judgements as S, so the instrument that produced them is not what failed. A new judge is needed only if J1 or J2 is unavailable at the run (then v1.11's alternate rule applies) or if H1_t5 is not CONFIRMED (then the gate reads accordingly, §8; no judge is swapped after seeing results).
- **Availability.** Claude Opus 5.5: "Tentative retirement date: Not sooner than September 22, 2027" (Anthropic's deprecations page as quoted in v1.15 §4, read 2026-11-11). Both judges' pages and prices are re-read on the lock day and the first run day; a change is a DEVIATIONS entry before any call.
- **t4 replies** are not re-sent; they are re-read from v1.15's frozen record and scored under the same v1.20 rule (§4.1).

## 6. Hypotheses, statistics and decision rules

**Conventions (v1.11 §5, unchanged).** ρ_w = pooled within-category Spearman on ranks centred on each category's mean rank (`score_v1_10.pooled_within_rho`, imported unchanged; computed unrounded). A category enters a pooled statistic with ≥ 4 units; a statistic is UNDETERMINED with fewer than 20 units pooled or fewer than 3 categories entering. 95% bootstrap intervals (units resampled within category, 10,000 draws) are reported and never enter a verdict. Permutation p = (hits + 1)/(N + 1). **Single wave:** as v1.15 §5.2, a separability row on one wave uses v1.11's per-wave statistic, floors and bands at that wave (the three-wave rule's literal output would be UNDETERMINED by construction). **Seeds (new for v1.21):** unit order 121000; self-consistency sample 121003; shuffle null 121010; H4 permutation 121011; bootstrap 121020.

**Noise guard (v1.11 §5, unchanged).** A noisy measure is separable from everything: if H1_t5 or H4 is FALSIFIED, H2_t5, H3_t5 and H5_t4 are reported as UNDETERMINED (statistics shown as descriptive only).

| Tag | Tier | Statement | Statistic and data | CONFIRMED iff | FALSIFIED iff |
|---|---|---|---|---|---|
| **H1_t5_Judge_Agreement** | PRIMARY (instrument gate) | The two judges agree on the t5 windows. | Krippendorff α (ordinal) on valence over every t5 window with valid J1 and J2 outputs (refers_to_brand either way, as v1.11's H1); brand ρ_w(TONE_J1, TONE_J2), groups = category, units rated under both; UNDETERMINED unless the brand row is determinable and ≥ 20 windows enter α | α ≥ 0.667 AND brand ρ ≥ 0.80 | α < 0.50 OR brand ρ < 0.60 |
| **H2_t5_Sep_Presence** | PRIMARY (the gate that failed) | Co-mention tone is separable from Presence. | \|ρ_w(TONE_t5, P_S0,t5)\|, rated units with P | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 |
| **H3_t5_Sep_Consistency** | PRIMARY | Co-mention tone is separable from Consistency. | \|ρ_w(TONE_t5, C\*_S0,t5)\|, units rated on both | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 |
| **H4_Retest_t4_t5** | PRIMARY (reliability) | The brand order by co-mention tone holds over about three weeks (t4 Nov 10–11 → t5 Dec 3–6), beyond list composition. | ρ_w(TONE_t4, TONE_t5), units rated at both; (a) TONE_t5 permuted within category, one-sided, 10,000 draws, seed 121011; (b) within-answer shuffle null: at both waves each answer's valid unit scores are shuffled among the brands it names (the answer's set of scores kept), TONE refitted, 10,000 draws, seed 121010, one-sided | ρ ≥ 0.50 AND p_perm < .05 AND p_shuffle < .05 | ρ < 0.30 OR p_perm ≥ .05 OR p_shuffle ≥ .05 |
| H5_t4_Sep_Presence | SECONDARY (gate downgrade only) | Separability from Presence replicates on t4. | \|ρ_w(TONE_t4, P_S0,t4)\| | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 |
| H6_t5_Naming_Frequency | SECONDARY (reported) | TONE does not track how often a brand is named. | \|ρ_w(TONE_t5, n_named)\|, n_named = t5 S0 answers naming the brand (v1.11 H7's statistic on t5), counted from the certified record: answers with a window for the brand in the t5 U0 unit table (any judge outcome), plus that brand's U0 extraction misses from `prereg/u0_v1_21.json` (§4.2; an empty list is 0 misses, and the scorer refuses without the file) | ≤ 0.30 | ≥ 0.50 |
| H7_t5_Self_Preference | SECONDARY (reported) | J1 does not favour answers written by its own provider's model. | v1.11 H9's Δ on t5 windows | \|Δ\| ≤ 5 points | \|Δ\| ≥ 10 points |

MARGINAL = otherwise, for every row; UNDETERMINED as defined above. H4's rule is v1.11's H4 rule (ρ ≥ 0.50 and p < .05) with v1.16's within-answer shuffle null added, because TONE, like PREC, is built from within-answer comparisons and must beat what an answer's mix of scores alone would produce.

**Why H5_t4 is not PRIMARY.** The task fixes t5 as the confirmatory wave. t4's replies were collected and partly handled (format counts, v1.20 §10) before this design, so t4 is kept as a downgrade-only replication, as v1.16 kept its search-on leg (v1.16 §6, H4_S1).

## 7. The bands, and precision (stated before any data)

**The bands do not move.** CONFIRMED ≤ 0.30, FALSIFIED ≥ 0.50, compared unrounded, as in v1.11 §5 and v1.20. The 0.50 line that v1.20's H2 crossed at t3 by 0.0013 is the line H2_t5 faces. A pooled or averaged rule across waves is not used (v1.16 §6 gives the reason: it would be looser than the bar earlier measures faced).

**Precision.** No new power computation was made for this draft. The closest file-based reference is v1.16 §7 (`prereg/precision_note_v1_16.json`, branch v1.16): on t4's N3 S0 answers, with a 6-mention floor, PREC had n 71 rated units; at that n, P(\|ρ̂\| ≤ 0.30) for one wave is 0.99 / 0.96 / 0.90 / 0.81 / 0.67 / 0.50 at a true ρ of 0.00 / 0.10 / 0.15 / 0.20 / 0.25 / 0.30 (Fisher z with the Bonett–Wright variance). TONE's rated n at t5 is not known before U0; the scorer writes the same analytic table at the realised n into the Stage J output, before P is opened; that n is the number of units rated on TONE at t5 in categories with ≥ 4 rated units (the units a pooled t5 statistic can use before P is matched). A single-wave test is easier to pass than v1.11's three-wave rule at the same true ρ; that is why H4 (reliability) and H5_t4 (replication) carry gate roles (§8).

## 8. Gate and the consequence clause

**GATE:** FAIL if any of H1_t5, H2_t5, H3_t5, H4 is FALSIFIED; else UNDETERMINED if any of them is UNDETERMINED; else PASS if all four are CONFIRMED and H5_t4 is not FALSIFIED; else MARGINAL. (v1.16 §8's gate form, with H5_t4 in the downgrade-only role of v1.16's H4_S1.) Only a FALSIFIED H5_t4 downgrades: an H5_t4 that is CONFIRMED, MARGINAL or UNDETERMINED leaves a PASS standing.

| Gate | Consequence (decided Sun 11/22 by the author: this is the last Sentiment redesign, as v1.16 was for Ranking; §16, decision 3) |
|---|---|
| **PASS** | TONE may be reported as the AIAS Sentiment component, labelled provisional until Paper B. Its t4 and t5 values are the "locked Sentiment score on the N3 answers" that v0.45 §2.6's Sentiment leg waits for. Before any calibration that combines Sentiment with another component, ρ_w(TONE, that component) is computed on the same units under the same bands; FALSIFIED there turns PASS into FAIL. |
| **FAIL, MARGINAL or UNDETERMINED** | Sentiment is reported as not separable from Presence and not as a separate AIAS component, and there is no further Sentiment redesign: no new Sentiment statistic, no re-run with other settings, and no sensitivity, secondary result, exploratory analysis or later wave (t6 included) turns this verdict into a PASS. The result is published with the prominence of a pass. Sentiment results (v1.20, v1.21) remain available as descriptions. |

Secondary results, descriptives, exploratory analyses and sensitivities never change the gate.

## 9. Checks

| Id | Check | Rule |
|---|---|---|
| Pins | every pinned input (v1.11 and v1.20 scorers, v1.16's `fit_bt`, v1.10's `pooled_within_rho`, v1.15's frozen raw file, v0.45's raw and coded files, P and C\* sources) matches its git blob and SHA-256. v0.45's files, in the v0.45 checkout whose `osf/v45/v45_unit_table.csv` is given to Stage C: `osf/v45/data/t5_raw.jsonl` (the blob at tag `v0.45-acquisition-locked`), the ten coded tables `osf/v45/data/coded/{v19,v20,v21,v22,v23}_phase_{a,b}.csv` and `osf/v45/v45_unit_table.csv` (t5 P and C\*), each the blob committed at that checkout's HEAD, with SHA-256 and blob recorded in the verdicts file; t4's P and C\* source `stage1_v1_14.json` against its pinned SHA-256 | halt |
| U0 | extraction misses ≤ 5% of a category's mentions (v1.11 §4.1) | halt before any judge call |
| JUDGE_FAIL | ≤ 2% of any category's units per judge under the v1.20 rule (v1.11 §4.2), at each scored wave (t5 and the re-scored t4); share = JUDGE_FAIL / (valid + JUDGE_FAIL) per wave × category × judge, unjudged windows not counted | halt before scoring |
| Identity | ρ_w of S_cat equals ρ_w of S_ref for every row (§3.4) | halt (scorer bug) |
| MQ6 positive control | the gate can detect overlap with Presence: ρ_w(n_named, P_S0) at t5 is printed | printed |
| MQ7 negative control | the mean of H4's 10,000 shuffled retest ρ stays below 0.20 | flag "list-composition-driven" if ≥ 0.20 |
| MQ9 identification | units at the floor outside the main comparison component, per wave | printed; flag if > 10% of the units at the floor |

## 10. Sensitivities, descriptives and exploratory analyses (reported; never change a verdict)

- **Sensitivities** (every gate statistic recomputed): SD without Denon (v0.19), as v1.11 §5.1; S-COI without Denon and the five omnibus brands named in the agency-work sentence of the Declarations (§17: Chevrolet, BMW, Bentley, Jack Daniel's, Eucerin; v0.62 DEVIATIONS Entry 0, Part F; v0.62's and v1.19's sensitivity S-COI), decided Sun 11/22 by the author (§16, decision 7); under SD and S-COI the excluded brands leave every correlation and H1_t5's α windows but stay in the Bradley–Terry fits as rivals (TONE is not refitted; v1.16's handling of excluded units); SU uncentred ranks; S_w (pair weight 1/(k − 1)); S_prior (λ 0.1 and 10); S_floor (3 and 10, applied to TONE's rating rule only); TONE scored on J2 (TONE_J2: TONE refitted on J2's unit scores for H2_t5, H3_t5, H4 and H5_t4; H1_t5 stays the primary's, since it already compares the two judges); S-ATT (v1.20's alternative attempt rule).
- **Secondary measures** of §3.4 (CONTRAST, S_ref, S_cat, S_res, TONE_NV): H2_t5, H3_t5 and H4 statistics for each, labelled (H4 with the same permutation and within-answer shuffle nulls as TONE's); S_res has H2_t5 and H3_t5 only, because it exists at t5 only (its coefficients are fitted at t4); S_ref's H2_t5 is printed beside v1.20's H2 values as the replication of the failed measure.
- **Descriptives:** pairs per category, share of tied pairs, answers with ≥ 2 valid brands, rated units; TONE distribution per category; mean u by answering model; α per category, κ on `evaluative`, J1 × J2 confusion; self-consistency (5% sample, flag below 0.90 exact agreement); served-model and finish-reason counts; ρ_w(TONE, v1.14's modal position) at t5 when v1.14 Stage 2's table exists (Ranking is reported as part of Presence; §4.3).
- **Exploratory, after the lock only (RQ3).** On v1.11's archived waves t1–t3, TONE and CONTRAST computed from v1.20's unit outcomes, and their ρ_w with P and C\* per wave, beside v1.20's S values. These waves produced the failed test and were seen in aggregate; their values are described, never tested, never used to choose between measures, and computed only after the lock is anchored (the scorer refuses earlier). Same for the eight early categories (E block), which have no P or C\*: their TONE and CONTRAST values are described only.

## 11. Paper B (unchanged; on hold)

The students' human labels (SVA MPS Branding) remain Paper B's validation of the unit judgements, under Paper B's own pre-registration (tag `v1.11-paperB-prereg-r1`), which this study does not change. Paper B is on hold. Because TONE is built from the same unit judgements, Paper B's labels validate TONE's inputs; whether label-based TONE agrees with judge-based TONE is a question for Paper B's own pre-registration, not added here. Sentiment stays provisional until Paper B reports.

## 12. Cost, cap and pause

**Planning figure, from recorded spend only (no estimate model).** v1.15 judged 1,547 t4 S0 windows with both judges, the 5% repeat and the retries, for a recorded spend of US$7.514511 (J1 $5.83, J2 $1.68; 3,353 records; `osf/methodology/v1_15/outputs/judge_outputs_frozen_v1_15.json` and `postlock/DEVIATIONS_continued_v1_15.md`, Entry 2, branch v1.15), at batch prices Claude Opus 5.5 $2 / $10 and GPT-6.1 Sol $1 / $5 per million tokens (v1.15 §4, read 2026-11-11). t5 repeats t4's design (v0.45 §4.2). Planning figure with the window cap dropped at t5 (decided Sun 11/22 by the author; §4.2, §16 decision 5), arithmetic on the cited figures only:

| Step | Arithmetic | US$ |
|---|---|---|
| t4 spend per judged window (both judges, 5% repeat, retries) | 7.514511 / 1,547 | 0.0048575 |
| t5 at t4's density with the 36-per-brand cap (1,547 windows) | 0.0048575 × 1,547 | 7.51 |
| t5 at t4's density with no cap (1,644 windows, `u0_v1_15.json`) | 7.514511 × 1,644 / 1,547 | **7.99** (7.9857) |
| of which added by dropping the cap (the 97 windows the cap removed at t4; 1,644 − 1,547 = 97) | 7.514511 × 97 / 1,547 | 0.47 (0.4712) |

The planning figure for the t5 judge run is therefore US$7.99 in total, about US$0.47 more than a capped run would cost; t5's real window count is known only at U0. v1.15's own planning table (v1.15 §7) puts its largest scenario, 4,032 windows with long requests, at US$53.61 with overhead. The t4 records include v1.11-rule retries that v1.20's rule makes unnecessary for prose-wrapped replies, so the figure is, if anything, high. t4 re-scoring and the t1–t3 exploratory analysis cost US$0.

**Cap.** Pablo's budget rule (v1.11 §7, quoted there verbatim, 2026-11-10, 8:03 am): at most US$100 of paid model calls per paper, hard cap, with the pause at US$80, enforced by v1.11's guard unchanged (worst case reserved before every call and batch; spend from recorded usage at list batch price). Prices are re-read on the lock day; a change is recorded before any call.

## 13. Order of operations and timing

1. **Before the lock (no model call, no data):** scorer `scripts/score_v1_21.py` and tests (`tests/test_score_v1_21.py`, synthetic fixtures in `tests/fixtures/`); unit tests on synthetic data for the by-construction properties (`test_frequency_does_not_enter_direction`, `test_answer_register_does_not_enter`, `test_s_cat_identity`); an end-to-end dry run on synthetic replicas with a known answer (v1.16 §11), recorded in `dryrun/`. Lock manifest last.
2. **Lock** (by Wed 2026-12-02, decided Sun 11/22 by the author, §16 decision 8; at least 24 hours after r2 reaches Pablo, so that the 24-hour rule is met, and the lock precedes v0.45's first call at Thu 2026-12-03 06:00 UTC): content lock → `--lock-manifest` → commit → tag `v1.21-prereg-r1` → push (Pablo's gate) → OSF deposit (Pablo's gate) → `--write-anchor`.
3. **t5 collection** by v0.45 (Dec 3–6); tag `v0.45-acquisition-locked`; v0.45's coding.
4. **U0 on t5** (windows, unit table SHA-256), before any judge call.
5. **Judge run** (J1, J2, repeats): only after U0, not during any other paid collection, no batch whose 24-hour window overlaps one (v1.11's batch rule); from Mon 2026-12-07 06:00 UTC, after v0.45's hard end (v0.45 §4.6; decided Sun 11/22 by the author, §16 decision 8).
6. `--freeze` → **Stage J** (JUDGE_FAIL check; TONE and secondaries at t5 and t4; H1_t5; self-consistency; precision table at the realised n; reads no P, C\* or R) → **Stage C** (opens P, C\*; H2–H7, gate, sensitivities, descriptives) → only then the **exploratory t1–t3 analysis** (§10). One-shot scoring; each stage runs once.

## 14. Deviations policy, limitations and predictions

**Deviations.** `anchor/DEVIATIONS.md` opens with Entry 0 (ex ante: this draft's reads, §4.4; the COI handling, §17). After the lock, as v1.11 §13: every change gets an entry (id, date, ex ante or ex post, what, why, effect on inference); a frozen-input hash mismatch halts; a code fix only restores a rule as written, with results before and after; the measure, judges, parameters, bands, floors, seeds, the extraction rule and the hypotheses do not change; anything added later is exploratory; a failed gate is published with the prominence of a pass.

**Limitations.** The measure is chosen after the predecessor failed; the diagnosis (§1.2) uses archived aggregates, and the design is fixed before any TONE value exists on any wave. One confirmatory wave on one panel (N3, three answering models); the legacy panel enters only as exploration. TONE uses only answers that name at least two brands; brands named mostly alone are rated less often. Ties are common on a five-point scale, which lowers TONE's resolution (reported as the tied-pair share). AI-judged and provisional until Paper B; every judge provider also supplied an answering model (H7_t5). TONE measures how a brand is described relative to the brands named beside it in AI answers, not consumer sentiment.

**Predictions (stated before any TONE value exists).** P1: TONE correlates positively with Presence (channel 3), less than S_ref does; whether it stays within 0.30 is H2_t5's question, and no band is predicted. P2: H4's retest is lower than S's archived t1 → t2 value (0.7345) because TONE drops the between-answer variation that S averages. P3: H3_t5 CONFIRMED, as v1.20's H3. P4: S_ref's H2_t5 lies in the same region as v1.20's H2 values.

## 15. Source of every number in this draft

| Numbers | File (branch or tag) |
|---|---|
| v1.20 verdicts; H1 α 0.8735, 3,650 units, brand ρ 0.8741 (n 163); H2 0.4771 / 0.4477 / 0.5013 (n 55 / 54 / 54); H3 0.0600 / −0.0156 / 0.1489; H4 0.7345 (n 53); H6 0.7431 (n 52); H5 0.4397 / 0.3855 / 0.4182; H7 0.5323 (n 136); H8 0.2304 / 0.3415 / 0.2674 (n 24); NV sensitivity 0.5094 / 0.3234 / 0.3849; sensitivity verdict changes | `osf/methodology/v1_20/outputs/v1_20_verdicts.json` (sentiment-successor @ 6efbd33) |
| bare windows 223 of 2,781 (8.0%); n ≥ 6 floor; bands 0.30 / 0.50; H1 thresholds 0.667 / 0.50 / 0.80 / 0.60; floors 4 units, 20 units, 3 categories; US$100 cap and US$80 pause | `osf/methodology/v1_11/prereg/PRE_REGISTRATION_v1_11.md` §4.1, §4.4, §5, §7 (and `u0_v1_11.json`) |
| t4: 1,547 judged windows, 1,644 windows, 97 capped out; 3,353 records; spend US$7.514511 (J1 $5.83, J2 $1.68); raw SHA-256 | `osf/methodology/v1_15/prereg/u0_v1_15.json`; `outputs/judge_outputs_frozen_v1_15.json`; `postlock/DEVIATIONS_continued_v1_15.md` Entry 2 (branch v1.15) |
| batch prices $2 / $10 and $1 / $5; Opus 5.5 retirement not sooner than 2027-09-22; largest planning scenario 4,032 windows, US$53.61 | `osf/methodology/v1_15/prereg/PRE_REGISTRATION_v1_15.md` §4, §7 (tag `v1.15-prereg-r1`) |
| t5 design: 3 models × 30 questions × 3 runs = 270 S0 answers, 54 per category; 112 units; window from 2026-12-03 06:00 UTC, hard end 2026-12-07 05:59:59 UTC | `osf/v45/prereg/PRE_REGISTRATION_v0_45.md` (tag `v0.45-prereg-r1`) |
| precision at n 71: 0.99 / 0.96 / 0.90 / 0.81 / 0.67 / 0.50; Bradley–Terry settings (λ 1, tolerance 10⁻¹⁰, 500 iterations); Ranking consequence text | `osf/methodology/v1_16/prereg/PRE_REGISTRATION_v1_16.md` §3.2, §7; `osf/methodology/v1_16/outputs/results_v1_16.json` (tag `v1.16-prereg-r1`, branch v1.16) |
| US$7.99; US$0.47; US$0.0048575 per window | arithmetic: 7.514511 × 1,644 / 1,547; 7.514511 × 97 / 1,547; 7.514511 / 1,547, from the v1.15 files above (§12) |
| agency-work sentence in §17 (five brands, 28.43%) | `osf/methodology/v1_19/prereg/PRE_REGISTRATION_v1_19.md` §14 Declarations (branch v1.19), quoted verbatim; also verbatim in `papers/v1_19/v1_19_ssrn_paper_draft.md` (branch v1.19-paper); source screen v0.62 DEVIATIONS Entry 0, Part F |
| "v1.21" in a test, line 271 | `scripts/test_score_v1_20.py` |

## 16. Decisions on r1's open questions (all decided Sun 11/22 by the author)

Pablo, Sun 2026-11-22, 4:38 pm CT: "ok v1.21, Cheil on". Each of r1's eight questions was answered with its recommended answer; none remains open. The text of the sections named applies each decision.

1. **Study id:** v1.21, the next free methodology id (§0). Decided Sun 11/22 by the author.
2. **Primary measure:** co-mention tone (TONE, Bradley–Terry, rival-adjusted) is primary; the plain within-answer contrast (CONTRAST) is secondary (§1.4, §3.4). Decided Sun 11/22 by the author.
3. **Consequence clause:** this is the last Sentiment redesign, as v1.16 was for Ranking; a not-PASS reports Sentiment as not separable from Presence (§8). Decided Sun 11/22 by the author.
4. **t4:** v1.15's stored t4 judge replies (US$0, under v1.20's rule) are used for the t4 → t5 retest (H4, PRIMARY reliability) and for H5_t4 (downgrade-only replication) (§4.1, §6). Decided Sun 11/22 by the author.
5. **Window cap at t5:** v1.11's 36-windows-per-brand cap is dropped at t5; every t5 window is judged. Planning figure US$7.99 in total for the t5 judge run, of which about US$0.47 is added by dropping the cap (§4.2, §12). Decided Sun 11/22 by the author.
6. **Ranking row:** separability from Ranking has no gate role; ρ_w(TONE, modal position) is reported as a descriptive only (§4.3, §10). Decided Sun 11/22 by the author.
7. **COI:** sensitivity S-COI (without Denon and the five omnibus brands named in §17) is added beside SD (§10); the existing COI paragraph stays verbatim, and the agency-work sentence is added to the Declarations in the wording of v1.19's locked pre-registration (§17). Decided Sun 11/22 by the author.
8. **Lock timing and judge window:** lock by Wed 2026-12-02, before t5's first call (Thu 2026-12-03); judge run from Mon 2026-12-07 06:00 UTC, after t5's hard end (§13). Decided Sun 11/22 by the author.

Unchanged by these decisions: the gate and its 0.30 / 0.50 lines (§7, §8); the confirmatory test is blind on t5 (collection from Thu 2026-12-03); the lock (tag, push, OSF deposit) precedes any coding or judging of a t5 answer; t1–t3 are exploratory only and analysed only after the lock (§10); the 24-hour rule before the lock runs from the time r2 reaches Pablo.

## 17. Declarations

**Conflict of interest.** Copied verbatim from the existing Sentiment pre-registration (v1.11 PRE_REGISTRATION §14, tag `v1.11-prereg-r1`; also quoted verbatim in v1.20 §14). This study judges t5 answers collected against the five omnibus registries of v0.19–v0.23, a subset of the thirteen registries named below, and makes no brand selection of its own; sensitivities SD and S-COI apply (§10). Quoted text: "The author is Director, Corporate Brand Creative and Governance, at Samsung Electronics America. This study re-analyses answers collected against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source phase's conflict-of-interest handling forward unchanged (the source records are quoted verbatim in DEVIATIONS Entry 0). Two items of record apply. In the automotive registry (v0.22), Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands — Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) — characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). In the audiophile-headphones registry (v0.19), AKG was substituted with Denon before the v0.19 pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary (v0.19 PRE_REGISTRATION §2.3; v0.19 paper, DEVIATIONS Entry 1). Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Every gate statistic is therefore also reported without Denon (sensitivity SD, §5.1). A string screen of all thirteen registries on 2026-11-10, for Samsung, Harman and the Harman and Sound United brand names listed in DEVIATIONS Entry 0, matched Denon (v0.19) only. Valence judging adds no brand choice and is fully automated against the locked registries and units, and this pre-registration is locked and deposited before any judge call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work."

Agency work (added in r2 on the author's decision of Sun 2026-11-22; sentence copied verbatim from v1.19 PRE_REGISTRATION §14, Declarations, branch v1.19, as also carried verbatim in the v1.19 paper): "Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). (Conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F.) As Denon, these five brands stay in every analysis, and every test is also reported without them and Denon (sensitivity S-COI)."

**Funding.** Self-funded.

**Ethics.** Not applicable: no human subjects (AI answers judged by AI models). Paper B's human labelling is governed by Paper B's own pre-registration.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 18. Files (at the lock; drafts r1, r2 and r3, the draft scorer, its tests and the dry run exist, none locked)

This document; `prereg/LOCK_MANIFEST_v1_21.sha256`; `scripts/score_v1_21.py`; `tests/test_score_v1_21.py` and the synthetic fixtures `tests/fixtures/` (built by `tests/fixtures/build_fixtures_v1_21.py`); `dryrun/` (synthetic replicas and record); `anchor/DEVIATIONS.md` (Entry 0); `anchor/git_anchor_v1_21.json`.

## 19. Change log

- r1, 2026-11-22: first draft (runner lane), proposed, not locked. No code, no data, no model call.
- r2, 2026-11-22 (r1 kept unchanged beside it): applies the author's decisions of Sun 2026-11-22, 4:38 pm CT ("ok v1.21, Cheil on"; all eight recommended answers). Not locked; no code, no data, no model call.
  - §16: the open-questions list is replaced by the eight decisions, each marked "decided Sun 11/22 by the author"; status line, §0 (id, decision of record), §1.3 (TONE primary), §4.1 (t4 use), §4.2 (cap), §4.3 (Ranking descriptive), §8 (last Sentiment redesign, as v1.16 for Ranking), §10 (S-COI) and §13 (lock by Wed 2026-12-02, judge from Mon 2026-12-07 06:00 UTC) now state the decisions instead of pointing to questions.
  - §4.2, §12: the 36-windows-per-brand cap is dropped at t5 only (t4 stays v1.15's frozen, capped record). §12 shows the arithmetic: US$7.514511 / 1,547 = US$0.0048575 per judged window; uncapped t5 at t4's density 7.514511 × 1,644 / 1,547 = US$7.99 in total; the part added by dropping the cap 7.514511 × 97 / 1,547 = US$0.47. r1's "about US$7.99" was the total for the run, not the increment.
  - §17: the agency-work sentence is added after the COI paragraph, verbatim from v1.19 PRE_REGISTRATION §14 (branch v1.19); the COI paragraph and the AI-use statement are unchanged (checked by string comparison against r1 and CLAUDE.md). §10 no longer names the company outside the Declarations.
  - §15: sources added for the new arithmetic and for the agency-work sentence; §18 notes the two drafts.
  - Unchanged: the measure, judges, extraction rule, hypotheses, gate and its 0.30 / 0.50 lines, floors, seeds, the blind confirmatory test on t5, lock before any t5 answer is coded, t1–t3 exploratory after the lock. The 24-hour rule runs from r2 reaching Pablo.
- r3, 2026-11-23 (r1 and r2 kept unchanged beside it): wording only. Writing the draft scorer (`scripts/score_v1_21.py`, commits 8d3c95f and e95c6a6) showed 16 places where r2 left a choice to the code; r3 writes each choice into the text as the code takes it (items 1–16). Items 17–18 name files r2 left unnamed where the scorer has been brought up to r2's text. Not locked; no data, no model call.
  1. §3.4 CONTRAST: "same floor" = rated iff ≥ 6 contributing answers, with no connected-component condition.
  2. §3.4 S_cat: centred on the mean S_ref of the category's rated units at the same wave.
  3. §3.4 S_res: least-squares fit on the t4 units rated on S_ref that have P_S0; a category with fewer than 2 such units or no spread in P has no S_res (counted).
  4. §4.2: the t5 U0 unit table, frozen judge record and raw replies are named (`prereg/units_v1_21.csv`, `outputs/judge_outputs_frozen_v1_21.json`, `data/judge_raw_v1_21.jsonl`, v1.15's names and v1.11's formats).
  5. §4.3: t5 P_S0 is column `P_t5_S0` of `osf/v45/v45_unit_table.csv`; t5 C\*_S0 is v0.45's own transform 100·(1 − φ/9) (100 if saturated, missing otherwise), with no C\* floor. Checked against `osf/v45/scripts/score_v0_45.py` (v0.45 branch, f754bff): it writes `P_t5_S0`, `phi_t5_S0` and `phi_partition_t5_S0` (defined / saturated / undefined, from v0.42's `phi_panel`) to `osf/v45/v45_unit_table.csv`, and `h_stab_consistency` uses exactly this C\* transform.
  6. §5, §9 JUDGE_FAIL: applied at both scored waves (t5 and the re-scored t4); the share is JUDGE_FAIL / (valid + JUDGE_FAIL) per wave × category × judge.
  7. §6 H1_t5: α over windows with valid J1 and J2 outputs whatever refers_to_brand says; brand ρ over units rated under both; UNDETERMINED unless the brand row is determinable and ≥ 20 windows enter α.
  8. §6 H6_t5: n_named counted as answers with a t5 window in the U0 unit table (any judge outcome), plus that brand's U0 extraction misses from U0's record (item 18).
  9. §7: the realised n of the precision table = units rated on TONE at t5 in categories with ≥ 4 rated units.
  10. §8: only a FALSIFIED H5_t4 downgrades a PASS; MARGINAL or UNDETERMINED does not.
  11. §10 SD, S-COI: excluded brands leave the correlations and H1_t5's α windows but stay in the Bradley–Terry fits as rivals.
  12. §10 S_floor: applies to TONE's rating rule only.
  13. §10 TONE_J2: TONE refitted on J2 for H2_t5, H3_t5, H4 and H5_t4; H1_t5 stays the primary's.
  14. §10 secondaries: their H4 uses TONE's permutation and within-answer shuffle nulls; S_res has no H4 (it exists at t5 only).
  15. §10 exploratory E block: the eight early categories have no P or C\*; their TONE and CONTRAST values are described only.
  16. §13, §18: the tests and fixtures are in `tests/` (`tests/test_score_v1_21.py`, `tests/fixtures/`), not `scripts/`.
  Two places where the draft scorer did less than r2's text promised; the code was brought up to r2 (no design change) and r3 names the files:
  17. §9 Pins: r2 lists v0.45's raw and coded files and the P and C\* sources but did not name them, and the draft scorer recorded only the scored table's SHA-256. r3 names them (`osf/v45/data/t5_raw.jsonl`, the ten `osf/v45/data/coded/{v19,…,v23}_phase_{a,b}.csv`, `osf/v45/v45_unit_table.csv`); Stage C now records each file's SHA-256 and git blob and halts if a file is missing, differs from the blob committed at the v0.45 checkout's HEAD, or (raw record) differs from the blob at tag `v0.45-acquisition-locked`, before P or C\* is read.
  18. §4.2, §6: U0's record `prereg/u0_v1_21.json` (v1.15's u0 format) is named beside the unit table. r2's U0 counts extraction misses and v1.11 counts them into n_named, but the draft Stage C never passed them. Stage J now reads the record (refusing if it is absent, lacks the `extraction_misses` list or names another unit table; an empty list records 0 misses explicitly), re-applies the 5% check from its per-set counts and stores the misses; Stage C adds them to n_named and refuses if Stage J holds none.
  - Unchanged: every hypothesis, threshold, band, gate, floor, seed, sample, the cost and cap, the decisions of §16, the COI paragraph and the agency-work sentence, the lock order and the 24-hour rule's wording.
