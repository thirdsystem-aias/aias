# AIAS v1.14 — Ranking, redesigned measure: the modal-position statistic, confirmed blind on t4 and t5

AIAS™ Measurement Program — Third System™. Pre-registration **r2** (2026-11-10). To be locked at git tag `v1.14-prereg-r2` (r1, locked at `v1.14-prereg-r1` the same day, was superseded before any t4 answer existed; DEVIATIONS Entry 1) and deposited on OSF before any rank position is computed on a t4 answer.

**Pre-registrant:** Pablo Ulpiano González Castro

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.14 |
| PHASE_TYPE | methodology lock; calibration on archived answers (allowed before the lock) and **confirmation on two unseen waves**: t4 (v0.42) and t5 (the next repeat wave). No collection of its own, no model call, no spend. |
| Decision of record | Pablo, control panel, Tue Nov 10, 2026, 12:27 pm (“ranking redesign — do as you suggest”): “(1) pre-register a new Ranking measure (v1.14) with the modal-position statistic as the declared candidate, stating openly that it was found in v1.10's sensitivity check on the three archived waves; (2) because it was chosen after seeing those waves, its separability and reliability gates are confirmed blind on data it has not seen: the t4 wave (and t5 for retest), scored once after the lock, the v1.9 pattern; the archived waves are reported as calibration only; (3) no Ranking Paper B and no AIAS 3.0 calibration until the redesigned measure passes; if it fails too, report it and bring the options here. The v1.10 Paper A stays published as the negative result.” |
| Status | r2 on branch `v1.14` (from `v1.10` @ `bad8c41`); r1 (tag `v1.14-prereg-r1`, commit `20fbc342`) was superseded before any t4 answer existed by a crash fix in Stage 1's unit listing (DEVIATIONS Entry 1). Calibration run on 2026-11-10 (§4). Not locked; no t4 answer exists (v0.42 locks Wed Nov 11 ~11 am CT and collects Nov 11–13). |
| Locks on | content lock → `prereg/LOCK_MANIFEST_v1_14.sha256` → commit → tag `v1.14-prereg-r2` → push branch and tag → `anchor/git_anchor_v1_14.json` (tag object, commit, tree, UTC time, SHA-256 of every locked file, activation record of §5.4) → OSF deposit of `osf/methodology/v1_14/prereg/`, `calibration/`, `anchor/`, SHA-256 verified on OSF → Stage 1 only after tag `v0.42-acquisition-locked` exists (§9). |
| Locked inputs | Extractor E0–E7, registries, rating floor, ρ_w convention, nulls, bands and seeds: v1.10 (tag `v1.10-prereg-r2`), imported unchanged from `scripts/score_v1_10.py` (git blob `0f8b981b…`, byte-identical to the tag). Presence and Consistency at t4: the definition v1.12 and v1.13 share (§5.2). |
| Feeds forward | Only after a PASS (§8): Ranking Paper B and the Presence × Consistency × Ranking calibration of AIAS 3.0, each under its own pre-registration. |

**Lineage.** v1.10 (Ranking Paper A, locked at `v1.10-prereg-r2`, published as a negative result) selected the mean normalised position (MNP) at Stage S on the early panel and tested it on the three archived omnibus waves. Its gate was MARGINAL: H1 ρ_w(R\*, P) = 0.275 / 0.366 / 0.307 at t1 / t2 / t3 against a confirmation bar of 0.30; H2 CONFIRMED; H3 0.897; H4 0.663 FALSIFIED; H5 0.846; H6 0.830 (`osf/methodology/v1_10/outputs/v1_10_verdicts.json`). Construct (unchanged): Ranking = where a brand sits in an answer's ordered list of registry brands, **given that the brand is named**.

## 1. Selection history (stated openly)

The statistic pre-registered here was **not** chosen blind. v1.10 pre-registered six candidate statistics (MNP, IRW, TOP3, MR, TOP1, MODE) and, as sensitivity S3, ran all six through its gate tests H1–H3 on the three archived omnibus waves (t1 May 20–26, t2 Jun 10, t3 Nov 9, 2026). Only the modal rank (MODE) kept H1 inside the confirmation band at every wave: ρ_w(R\*, P) = 0.093 / 0.247 / 0.206, with H2 0.191 / 0.042 / 0.099 and H3 0.858 (v1.10 verdicts file, `sensitivities.S3_candidate_MODE`; v1.10 paper §7.3). The v1.10 paper notes that MODE is the least reliable of the six candidates (Stage S split-half 0.889) and that its separation may partly reflect its coarseness.

Because MODE was chosen **after** seeing how every candidate behaved on t1–t3, those three waves cannot confirm it. They are reported here as **calibration only** (§4). Its separability and reliability gates are confirmed on data that neither the statistic nor this document has seen: **t4** (v0.42, Stage 1, separability) and **t5** (Stage 2, retest reliability), each scored once, after the lock, as v1.9 did with its t3 confirmation. No other candidate is carried forward, and no other choice is made after seeing data: every rule other than the statistic is v1.10's, changed only where t4's design forces it (§3.3).

v1.10 Paper A stays published as the negative result for MNP; v1.14 does not revise it.

## 2. Research questions

- **RQ1 (separability at t4).** On the newest models, is the modal-position Ranking score separable from Presence and from Consistency (and from the other components whose locked scores exist on the same panel) by v1.10's bands?
- **RQ2 (reliability t4 → t5).** Does the brand order by modal position hold over about three weeks, beyond what list composition alone produces?
- **RQ3 (calibration).** How does the statistic behave on the archived waves under every v1.10 test (declared calibration; no verdict rests on it)?

## 3. The statistic

### 3.1 Definition

For brand b in category c, within one panel × wave × condition, over its **rankable mentions** (answers naming ≥ 2 registry brands that name b; v1.10 E5):

**R\*_b = − min { k : k is a most frequent value of k_min over b's rankable mentions }**

- k_min is the brand's **competition min-rank** in an answer (v1.10 E7): brands with equal sort keys share the smallest position they occupy (two brands tied for 2nd both get k_min = 2).
- **Ties between modes:** when several positions are equally frequent, the smallest (nearest the top) is taken.
- **Orientation:** higher = nearer the top; R\* = −1 means the brand's most frequent position is first.
- **Rating floor:** R\* is **rated** iff the brand has **≥ 6 rankable mentions** (v1.10 floor, the v1.9 C\* floor); otherwise NOT RATED. Never-named brands are NOT RATED (absence is Presence's information).
- **Pooling over runs, models and questions:** all rankable mentions of the brand in the panel × wave × condition are pooled — at t4: 3 models × 3 runs × the 6 category questions of its substrate (up to 54 answers per substrate in S0) — and **one** mode is taken over the pooled k_min values. No mode of modes, no per-model or per-run statistic enters R\*. This is v1.10's rule (it pooled 6 models × 6 questions × 1 run per wave).
- **Position:** the lead-item rule (v1.10 E6, primary): in a list-structured answer brands are ordered by the first item they lead; otherwise by first mention. First-mention order everywhere is sensitivity S1.
- **Condition:** the primary R\* uses the **search-off** answers (S0). The search-on answers (S1) give a separate R\*_S1 used only by the replication leg H4_S1 and descriptives (§5.3).
- Implementation: `score_v1_10.brand_scores(...)["MODE"]`; `score_v1_14.modal_position` is tested to give identical values (test `test_modal_position_equals_v1_10_MODE`).

### 3.2 Kept from v1.10 unchanged

Extraction rules E0–E7 (normalisation, `\b`-alias matching, list items, lead-item rule, first occurrence wins, ≥ 2 brands rankable, mid- and min-ranks); the five omnibus registries exactly as v1.10 loads them (files pinned in `osf/methodology/v1_10/registries/INPUTS_MANIFEST_v1_10.json`, verified before use); unit = (substrate, brand), 112 units; rating floor 6; ρ_w = pooled within-category Spearman with ranks **centred** on the category mean rank, only categories with ≥ 5 units, values compared unrounded; permutation p = (hits + 1)/(N + 1), R\* permuted within substrate, 10,000 draws; within-answer order shuffle null for reliability, 10,000 draws; bootstrap 90% percentile CI (2,000 draws, seed 110020; reported, not a verdict input); bands (separability |ρ| ≤ 0.30 CONFIRMED, ≥ 0.50 FALSIFIED; reliability ρ ≥ 0.50 with both p < 0.05 CONFIRMED, ρ < 0.30 or either p ≥ 0.05 FALSIFIED); n floor 30 units; seeds 110001 (H1), 110002 (H2), 110003 (H3), 110010 (shuffle), 110020 (bootstrap), 110030 (MQ7); the positive control MQ6 and the negative control MQ7.

### 3.3 Changes forced by t4's design (and why)

1. **One wave per separability test.** v1.10's H1/H2 needed |ρ| ≤ 0.30 at each of three waves (UNDETERMINED with fewer than two determined waves). t4 is one wave, so H1 and H2 are verdicts on a **single estimate** with the same bands and the same n floor (v1.10's `verdict_single_separability`, the rule of its H4).
2. **Presence and Consistency at t4** are not the published AIAS 2.0 values (legacy panel) but the t4 definition v1.12 and v1.13 share on v0.42's analysis set (§5.2), because t4 asks each brand question once and on three models.
3. **Reliability is a retest across waves (t4 → t5)**, as v1.10's H3 was (t1 → t2), on the three N3 models.
4. **No early panel at t4.** v1.10's downgrade-only replication leg H4 (separability on the early panel) has no t4 counterpart; its place is taken by the only second arm t4 has, the search-on answers (H4_S1, downgrade-only).
5. **URL removal.** As v0.42 §5.1 does for mention coding, `https?://` addresses and Markdown link targets are removed before matching (link text kept), so a brand reached only through a URL is not named and has no position. The archived answers are scored as v1.10 scored them.
6. **New rows to the gate where they exist:** separability against the other components (Coverage, Grounding, Sentiment) on the same panel (§5.4), per the program plan (Nov 9: Paper A = separability vs Presence, Consistency and the other components).
7. **Degeneracy check MQ9 (new).** Because MODE is coarse (integer positions), separability is UNDETERMINED, not CONFIRMED, if more than 80% of rated units share one R\* value or if every rated unit of a substrate shares one value in ≥ 3 of the 5 substrates (§5.5). On the archived waves the most common value is held by 24–28% of rated units and every substrate has spread (calibration, `MQ9_degeneracy`).

## 4. Calibration on the archived waves (declared calibration; no verdict)

Computed on 2026-11-10 from v1.10's 31 hashed rank tables (SHA-256 checked against `v1_10_verdicts.json`) and the locked `osf/aias_2_0/aias_2_0_profiles.csv` (SHA-256 checked against v1.10's input manifest). Command: `python3 scripts/score_v1_14.py --calibration` → `calibration/calibration_v1_14.json` (log `calibration/calibration_run_v1_14.log`).

**Reproduction.** The calibration reproduces v1.10's sensitivity check S3 for MODE exactly: every ρ, n and permutation p of H1 and H2 at t1–t3, and ρ, n, p_perm and p_shuffle of H3, are bit-identical (`reproduction_of_v1_10_S3_MODE.all_identical = true`). Two reader checks also reproduce v1.10's own values exactly: H4 with MNP (0.6626, p 0.0001) and the Stage S split-half reliabilities of all six candidates (MODE 0.8888, n 138).

| Test (v1.10 definition), MODE | t1 | t2 | t3 | Reading under v1.10's bands |
|---|---|---|---|---|
| H1 ρ_w(R\*, P) (n; p; 90% CI) | 0.093 (55; 0.551; −0.154 to 0.330) | 0.247 (54; 0.110; −0.026 to 0.493) | 0.206 (54; 0.182; −0.013 to 0.411) | ≤ 0.30 at every wave |
| H2 ρ_w(R\*, C\*) (n; p) | 0.191 (55; 0.208) | 0.042 (54; 0.785) | 0.099 (54; 0.520) | ≤ 0.30 at every wave |
| H3 t1 → t2 | 0.858 (n 53; p_perm 0.0001; p_shuffle 0.0001; CI 0.725 to 0.935) | | | ≥ 0.50 |
| H5 t2 → t3; t1 → t3 descriptive | 0.901 (n 52; both p 0.0001); 0.855 (n 52) | | | ≥ 0.50 |
| H4 early panel ρ_w(R\*, π̂) | 0.462 (n 154; p 0.0001; CI 0.297 to 0.583) | | | MARGINAL (MNP: 0.663, FALSIFIED) |
| MQ7 shuffled split-half (early panel) | 0.123 (unshuffled 0.889; 138 units) | | | < 0.20, no flag |

Sensitivities: without the COI-flagged Denon unit (S7) every value is unchanged (Denon is never rated); rating floor 3: H1 0.145 / 0.230 / 0.292; rating floor 10: H1 0.387 / 0.177 / −0.003 (31–34 units; MNP at floor 10 reached 0.558 and 0.635); uncentred ranks (S9): H1 0.206 / **0.351** / 0.295, H2 0.291 / 0.174 / 0.199, H3 0.876.

**Reading.** Under v1.10's gate rule MODE's archived values would read H1, H2, H3 CONFIRMED and H4 MARGINAL (not FALSIFIED): a PASS. (v1.10's S3 row printed “MARGINAL” for MODE because it carried MNP's H4 verdict.) These numbers were seen before MODE was chosen, or were computed on the same waves after it was chosen; they are calibration, not evidence. Because MODE was the one candidate of six that stayed within the H1 band, its archived H1 values are expected to be optimistic (selection on the outcome): the confirmatory t4 value may be higher.

## 5. Stage 1 — t4 separability (scored once, after the lock)

### 5.1 Data

t4 = v0.42 (pre-registration r2, tag `v0.42-prereg-r1`): the 30 category questions (Phase B; 6 per substrate) asked of Claude Fable 5.2 (`claude-fable-5-2`, Anthropic Message Batches API), GPT-6 Astra (`gpt-6-astra`) and Gemini 4 Argon (`gemini-4-argon`), without (S0) and with (S1) the provider's web search, three runs each: 54 answers per substrate and condition, 540 Phase B answers in all; the 112 brand questions (Phase A, S0, one run) enter only through Presence. Files, read with `git show` from the tag `v0.42-acquisition-locked` (raw answers) and from the v0.42 commit that holds its scored outputs (`--v042-scored-ref`; coded tables, brand table, verdicts), each read logged with its git blob and SHA-256:

- `osf/v42/data/t4_raw.jsonl` (one line per attempt, append-only); the raw file at the scored ref must equal the acquisition-locked file;
- `osf/v42/data/coded/{v19..v23}_phase_{a,b}.csv` (v0.42's certified coder, `code_t4_v0_42.py`, git blob `2d36735d…`, checked at the acquisition-locked tag);
- `osf/v42/v42_brand_table.csv` (`pi_N3_S0`, `phi_N3_S0`, `phi_partition_N3_S0` and the S1 columns) and `osf/v42/v42_verdicts.json` (drop rule).

**Analysis set** (v0.42's, as v1.12 and v1.13 use it): one record per call (the last answered attempt, else the last attempt; `code_t4_v0_42.dedupe_calls`); calls outside v0.42's design and answered calls served by another model ID are excluded (a dated snapshot of the requested ID is accepted; a missing served ID is not excluded); an unanswered call is a missing cell (E0), never “no brand named”. If v0.42's drop rule excludes any N3 model in S0, H1 and H2 are UNDETERMINED (as v0.42's own primary test).

### 5.2 Presence and Consistency at t4 (the definition shared with v1.12 and v1.13)

- **P_c** = 100 · (C_P/3 + 2 · π̂_c)/3, with π̂_c = v0.42's recall Presence on N3 in condition c (brand table `pi_N3_c`) and C_P/3 = the share of N3 models whose v0.42 recognition code for the brand is “recognized” in their one S0 Phase A answer (models without a coded answer leave the denominator; none coded → P not computed). P_S0 is Presence for H1; P_S1 (same S0 recognition share) for H4_S1.
- **C\*_c** = 100 · (1 − φ_c/9) when v0.42's partition is `defined`; 100 when `saturated`; NOT RATED when `zero` or `undefined`; rated only with ≥ 6 N3 Phase B mentions in condition c. 9 = φ_max for 6 frames and 3 models.
- **MQ8 (comparator parity, halts):** π̂ and φ (with partition) recomputed from v0.42's coded Phase B table equal the brand table exactly in both conditions (v1.12's P2).

### 5.3 Hypotheses (Stage 1)

R\* = the modal position of §3.1 on t4 (N3), rated units only. Bands as v1.10; UNDETERMINED below 30 units.

| Tag | Tier | Statement | Statistic and data | Null / seed | CONFIRMED iff | FALSIFIED iff | MARGINAL |
|---|---|---|---|---|---|---|---|
| **H1_Sep_Presence** | PRIMARY (gate) | Ranking is separable from Presence at t4. | ρ_w(R\*_S0, P_S0); units with R\* rated and P computed | R\* permuted within substrate, 10,000, seed 110001, two-sided | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise |
| **H2_Sep_Consistency** | PRIMARY (gate) | Ranking is separable from Consistency at t4. | ρ_w(R\*_S0, C\*_S0); units with both rated | as H1, seed 110002 | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise |
| **H_Sep_Coverage / Grounding / Sentiment** | PRIMARY (gate), **conditional** (§5.4) | Ranking is separable from each other component on the same panel. | ρ_w(R\*_S0, X), X = that component's locked score, its own rated set | as H1, seeds 114002 / 114003 / 114004 | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise |
| H4_Sep_Presence_S1 | SECONDARY (gate downgrade only) | Separability replicates with search on. | ρ_w(R\*_S1, P_S1) | as H1, seed 114001 | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise |

### 5.4 Other components (activation)

A component leg is **active** only if that component's pre-registration tag (v1.12 Coverage, v1.13 Grounding, v1.11 Sentiment, or a later revision) is pushed **before the v1.14 lock commit**, and the leg is defined on the same 112 units and the N3 panel: Coverage = v1.12's locked Cov\* on its own N3, S0 collection (same units, Nov 14–16); Grounding = v1.13's locked G\* on t4's S1 answers; Sentiment = a locked Sentiment score on the t4 N3 answers (v1.11's locked score is defined on the archived waves only, so the Sentiment leg is inactive unless such a score is pre-registered). The anchor file records, for each component, the tag, its commit and whether the leg is active. An active leg is computed at Stage 1 if its locked score exists then (`--component NAME=file.csv`, columns substrate, brand, value; the file's SHA-256 is recorded), otherwise at Stage 2 from Stage 1's stored R\*; if it does not exist by Stage 2 it is reported as PENDING and computed, with the same frozen R\*, as soon as the score exists, before any calibration that combines Ranking with that component. At this draft: `v1.11-prereg-r1` is pushed (Sentiment leg inactive for the reason above); v1.12 and v1.13 have no tag.

### 5.5 Checks

| Id | Check | Rule |
|---|---|---|
| MQ1 | Parse | extractor completes on 100% of answers with text (an exception halts) |
| MQ2 | Mention parity | extractor's named set (URL-stripped) = v0.42's coded Phase B table on 100% of cells for v0.20–v0.22 (else halt); ≥ 0.98 for v0.19 and v0.23 (else that substrate leaves the gate legs; DEVIATIONS entry); every answered call has coded rows (else halt) |
| join | Units | the 112 v1.10 registry units match v0.42's brand table 1:1 (else halt) |
| MQ4 | Missing cells | listed per substrate × condition against 54 expected; never imputed |
| MQ6 | Positive control | penalised MNP (unnamed brands q = 1) must reach \|ρ_w(·, P_S0)\| ≥ 0.50; otherwise the gate's sensitivity is flagged |
| MQ7 | Negative control | within-answer order shuffle (2,000 draws, seed 110030) of the run-pair reliability D2: mean rel3 < 0.20; otherwise flagged as list-composition-driven |
| MQ8 | Comparator parity | §5.2 (halts) |
| MQ9 | Degeneracy | > 0.80 of rated units share one R\* value, or no spread in ≥ 3 substrates → H1, H2 and active component legs UNDETERMINED |

### 5.6 Descriptives and sensitivities (reported; never change a verdict)

D1 per substrate × condition and per model × condition: answers, missing cells, rankable share, list-structured share, brands named per rankable answer, units rated, R\* distribution and value counts. D2 run-pair reliability: R\* per run (rated at ≥ 3 rankable mentions in the run), ρ_w over the units rated in both runs of each pair, rel1 = mean over pairs with ≥ 30 units, rel3 = 3·rel1/(1 + 2·rel1). D3 ρ_w(R\*_S0, R\*_S1). D4 ρ_w(MODE, MNP) at t4. Sensitivities of H1 and H2: S1 first-mention rule; S2 floors 3 and 10; S3 all six v1.10 candidates; S4 leave one substrate out; S5 recall arm (ρ_w(R\*, π̂_S0), ρ_w(R\*, mentions)); S7 without the Denon unit (COI correction, Declarations); S9 uncentred ranks. Every verdict change under a sensitivity is listed next to the verdict.

## 6. Stage 2 — t4 → t5 retest reliability

**H3_Retest_Reliability** (PRIMARY, gate: reliability leg). Brand order by modal position holds over about three weeks beyond list composition. ρ_w(R\*_t4, R\*_t5), S0, units rated in both waves (categories with ≥ 5 such units); nulls (a) R\*_t5 permuted within substrate, 10,000, seed 110003, one-sided, and (b) within-answer order shuffle of both waves, 10,000, seed 110010, one-sided; bootstrap CI. **CONFIRMED iff ρ ≥ 0.50 and p_perm < 0.05 and p_shuffle < 0.05; FALSIFIED iff ρ < 0.30 or p_perm ≥ 0.05 or p_shuffle ≥ 0.05; MARGINAL otherwise; UNDETERMINED if n < 30.** (v1.10's H3, unchanged.)

**What t5 must repeat** (v0.42 §6 plans it; t5 is not yet pre-registered): the 30 Phase B category questions **verbatim** (substrate, probe ID, frame and prompt identical to `osf/v42/prereg/probes_v0_42.jsonl`; the scorer halts otherwise); the same model IDs (`claude-fable-5-2`, `gpt-6-astra`, `gemini-4-argon`) where still available; **search off (S0)**; **three runs**; the same decoding (provider defaults, output cap 16,384 tokens), call modes and call policy; the same raw-file schema (`t4_raw.jsonl` fields). A newer model added to t5 as an extra arm does not enter H3. A model enters the retest iff it was retained at t4 and ≥ 90% of its t5 S0 Phase B calls are answered; with fewer than three such models H3 is computed on those common to both waves and labelled reduced panel; with fewer than two, H3 is UNDETERMINED. S1 at t5 is not required; if collected, the S1 retest is descriptive. Stage 2 re-extracts t4 from the acquisition-locked tag and halts unless the rank table equals Stage 1's (SHA-256).

## 7. Precision and power

At t4, R\* is pooled over up to 54 S0 answers per substrate (36 per wave at t1–t3), on three models instead of six; the number of rated units cannot be fixed in advance (t1–t3: 54–55 of 112). Approximate sampling distribution of a single-wave ρ_w (Fisher z with the Bonett–Wright variance (1 + ρ²/2)/(n − 3); analytic, `calibration_v1_14.json` → `precision_note`):

| Rated units n | 90% CI half-width at ρ = 0.2 | P(CONFIRMED) if true ρ = 0 / 0.10 / 0.20 / 0.25 | P(FALSIFIED) if true ρ = 0.25 |
|---|---|---|---|
| 40 | 0.27 | 0.94 / 0.89 / 0.74 / 0.63 | 0.04 |
| 55 | 0.23 | 0.97 / 0.93 / 0.78 / 0.65 | 0.02 |
| 70 | 0.20 | 0.99 / 0.96 / 0.81 / 0.67 | 0.01 |

MODE's archived H1 values average 0.18 (0.093, 0.247, 0.206). If its true separation from Presence at t4 is of that size, a single t4 wave confirms H1 with probability about 0.75–0.8 and returns MARGINAL otherwise; it falsifies H1 (|ρ| ≥ 0.50) with probability below 0.05 unless the true value is well above 0.25. For H3, with n = 40 and a true retest ρ of 0.70 (archived t1 → t2: 0.858), P(ρ̂ ≥ 0.50) ≈ 0.96 (0.79 at a true 0.60). The run-to-run and model differences of the newest models are unknown until t4 (v0.42 §2.7 reports them).

## 8. Gate and verdict matrix

**Interim verdict after Stage 1:** FAIL if H1, H2 or an active component leg is FALSIFIED; else UNDETERMINED if any is UNDETERMINED; else SEPARABLE (Stage 2 pending) if all are CONFIRMED (MARGINAL if H4_S1 is FALSIFIED); else MARGINAL. Stage 2 is run for the record whatever the interim verdict.

**GATE (final, after Stage 2):**

| Condition | Verdict | Consequence |
|---|---|---|
| any of H1, H2, H3 or an active component leg FALSIFIED | **FAIL** | negative result, published with the prominence of a pass; options back to Pablo; no Paper B, no AIAS 3.0 calibration with Ranking |
| else any UNDETERMINED | **UNDETERMINED** | data cause fixed and reported; options back to Pablo; no Paper B, no calibration |
| else all CONFIRMED and H4_S1 not FALSIFIED | **PASS** | Ranking Paper B and the AIAS 3.0 calibration may be pre-registered (each separately); a PENDING component leg must be computed before any calibration that combines Ranking with that component, and a FALSIFIED result there turns the PASS into FAIL |
| else (all CONFIRMED but H4_S1 FALSIFIED, or any MARGINAL) | **MARGINAL** | reported as is; options back to Pablo; no Paper B, no AIAS 3.0 calibration until a measure passes |

Secondary results (other than H4_S1's downgrade), descriptives, sensitivities and the calibration never turn a FAIL or MARGINAL into a PASS. MQ6 and MQ7 flags are printed next to the gate. Unlike v1.10, a MARGINAL gate does not open Paper B on a recorded decision: under Pablo's decision of Nov 10 only a PASS does; any other route needs a new decision and a new pre-registration.

## 9. Order of operations (enforced by `scripts/score_v1_14.py`)

1. Now (allowed): `--calibration` on the archived waves (§4).
2. Lock (§0). The lock should precede the end of t4's collection (Nov 13). If it is later, the lock record states that no rank position or Ranking statistic had been computed on a t4 answer by any program script. To keep Stage 1 blind, no Ranking statistic is computed on a t4 answer before it, including v1.12's H5 and v1.13's H4, which apply v1.10's MNP to t4 answers if active.
3. **Stage 1** (`--stage 1 --v042-scored-ref <ref>`): refuses unless tag `v1.14-prereg-r2` and `anchor/git_anchor_v1_14.json` exist, tag `v0.42-acquisition-locked` exists, every file in `LOCK_MANIFEST_v1_14.sha256` is unchanged, and v0.42's coder blob at the acquisition tag equals the pin; **runs once** (refuses if `outputs/stage1/stage1_v1_14.json` exists). Writes the verdicts, the hashed t4 rank table and the unit table with R\*_S0.
4. **Stage 2** (`--stage 2 --t5-ref <tag> --t5-raw <path> --t5-probes <path>`): refuses before Stage 1, without the lock files, or unless the t5 tag ends in `-acquisition-locked` and exists; checks question parity and the t4 rank-table hash; runs once.

## 10. Deviations policy

`anchor/DEVIATIONS.md` opens with Entry 0 (ex ante: selection history, COI carry-forward with the Denon correction, the anchor sequence). After the lock: every change gets an entry (id, date, ex ante / ex post, what, why, effect on inference); a hash mismatch halts; an extractor fix is allowed only to restore a rule as written, with verdicts reported before and after; the statistic, floors, bands, seeds, nulls and gate rule do not change; anything added later is exploratory; a failed gate is published with the same prominence as a pass. If t5 cannot repeat t4 as §6 requires, Stage 2 is not run under this pre-registration and the options go to Pablo.

## 11. Limitations

The statistic was selected after seeing the archived waves (§1); only t4 and t5 can confirm it. MODE is coarse: integer positions with many ties, so its correlations rest on fewer distinct values than MNP's (MQ9 guards against the degenerate case only). One t4 wave carries the separability test (§7). t4 and t5 are three models, one per provider, answering with provider-default settings; the gate is about the newest panel, not the legacy panel. Rank is among registry brands only; position in text is not visual prominence; the lead-item parser relies on Markdown conventions. Five categories, US English. The comparators at t4 rest on one recognition answer per model (v0.42 §9 C13).

## 12. Declarations

### Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses archived answers and scores the t4 and t5 answers against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.10 DEVIATIONS Entry 0; v1.14 DEVIATIONS Entry 0). Two items of record apply to the registries used.

*Audiophile headphones (v0.19).* The v0.19 record states: “The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock.” (v0.19 paper, Declaration of interest; see also v0.19 pre-registration §2.3 and v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN, “HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership”, press release, Business Wire, September 23, 2025. In this study Denon remains in the locked registry and in the primary analysis; every gate statistic is also reported without the Denon unit (sensitivity S7).

*Automotive (v0.22).* The v0.22 record states: “Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed.” (v0.22 paper, Conflict of interest.) These are supply relationships, not ownership; no v0.22 brand is removed in this study.

Extraction and scoring are automated against the locked registries and this pre-registration. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

### Funding {-}

Self-funded. No external funding supported this research.

### Ethics {-}

Not applicable; no human subjects. The study analyses responses of large language models queried under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 13. Files

`prereg/PRE_REGISTRATION_v1_14.md` (this file); `prereg/LOCK_MANIFEST_v1_14.sha256`; `calibration/calibration_v1_14.json` and its run log; `anchor/DEVIATIONS.md`; `README.md`; `scripts/score_v1_14.py` and `scripts/test_score_v1_14.py` (32 tests: synthetic t4-shaped data for Stage 1 and Stage 2, and the exact reproduction of v1.10's S3 for MODE); `scripts/score_v1_10.py` (imported unchanged) with v1.10's input manifest, the five omnibus registry files, v1.10's verdicts file (which pins its rank tables), its COI flag file and the profiles table, all listed in the lock manifest.

## 14. Choices made in drafting (for the pre-registrant)

1. Primary R\* on search-off answers; search-on R\* only as a downgrade-only replication leg (H4_S1), in place of v1.10's early-panel H4.
2. Single-wave bands at t4 (v1.10's single-estimate rule), because t4 is one wave.
3. Component legs gate when active (v1.12's rule), with PENDING legs completed before any combined calibration.
4. MQ9 degeneracy rule added for a coarse statistic.
5. Only a PASS opens Paper B and the AIAS 3.0 calibration (Pablo, Nov 10); a MARGINAL no longer opens Paper B on a recorded decision.
6. The run-pair reliability (D2) at t4 is descriptive, with MQ7 as its control; the reliability gate is the t4 → t5 retest only.
