# AIAS v1.16 — Ranking, the last measure: co-mention precedence, tested once on the archived answers

AIAS™ Measurement Program — Third System™. Pre-registration **r1** (2026-11-12). To be locked at git tag `v1.16-prereg-r1` and deposited on OSF (`methodology/v1_16`) before any precedence value is computed on a real answer.

**Pre-registrant:** Pablo Ulpiano González Castro

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.16 |
| PHASE_TYPE | methodology lock and re-analysis of archived answers. No collection, no model call, no spend. |
| Decision of record | Pablo, Wed Nov 11, 2026, 11:22 pm: “RANKING: (c), with one condition: this is the last redesign. Report v1.14 as MARGINAL, let the next part that passes its gate make the next release, and pre-register one new Ranking measure, justified in advance from the method and the literature (SparkToro/Gumshoe; Boffa et al.), stating in that pre-registration that if it does not PASS, Ranking is reported as part of Presence and not as a separate AIAS component; no further redesigns.” |
| Status | r1 on branch `v1.16` (from `v1.14` @ `3129674`). Input parity and the synthetic dry run done (§4.3, §11). No precedence value has been computed on a real answer. |
| Locks on | content lock → `prereg/LOCK_MANIFEST_v1_16.sha256` → commit → tag `v1.16-prereg-r1` → push branch and tag → OSF deposit of `osf/methodology/v1_16/` (`prereg/`, `anchor/`, `dryrun/`, `README.md`), SHA-256 verified on OSF → `anchor/git_anchor_v1_16.json` (tag object, commit, tree, UTC time, SHA-256 of every locked file, OSF location) → the one confirmatory run (§12). |
| Inputs | Archived and already hashed (§4): v1.10's rank tables of the three omnibus waves, the locked P / C\* table of those waves, and v1.14 Stage 1's t4 rank table and unit table. No answer is re-extracted. |
| Consequence | §8: if the gate does not PASS, Ranking is reported as part of Presence and not as a separate AIAS component, and there is no further Ranking redesign. |

**Lineage.** Construct (unchanged since v1.10): Ranking = where a brand sits in an answer's ordered list of registry brands, **given that the brand is named**.

- **v1.10** (Ranking Paper A, tag `v1.10-prereg-r2`, published Nov 10 as a negative result): mean normalised position (MNP), centred within-category ranks. Reliability 0.951 (Stage S split-half); separable from Consistency (H2 CONFIRMED); not clearly separable from Presence: H1 ρ_w(R\*, P) = 0.275 / 0.366 / 0.307 at t1 / t2 / t3 against a bar of 0.30 (MARGINAL); early-panel H4 0.663 (FALSIFIED); gate MARGINAL (`osf/methodology/v1_10/outputs/v1_10_verdicts.json`). Brands named more often tend to be named earlier.
- **v1.14** (tag `v1.14-prereg-r2`): the modal position (MODE), confirmed once on t4 (Stage 1, Wed Nov 11, 7:43 pm): H1 ρ_w(R\*, P) = 0.369 (n 71; CONFIRMED needs |ρ| ≤ 0.30, FALSIFIED from 0.50) MARGINAL; H2 ρ = 0.132 (n 70) CONFIRMED; H4 with search on ρ = 0.496 (n 65) MARGINAL; Stage 1 MARGINAL (`osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json`). Two pre-set sensitivities (rating floor 10; the top-1 candidate) read H1 CONFIRMED; by v1.14's locked rule they cannot turn a MARGINAL into a pass. By Pablo's decision v1.14 is reported as MARGINAL; its Stage 2 (t5 retest, about Dec 7) runs for the record only. v1.16 revises neither study.

## 1. Why v1.10 and v1.14 fell short, the new measure, and what the method predicts

### 1.1 Diagnosis

MNP and MODE both summarise **a brand's own positions over the answers that name it**. That sampling frame lets how often a brand is named enter the score through channels that are properties of the statistic, not of a ranking:

1. **List length.** An absolute position (MODE, and also MR, TOP1, TOP3 of v1.10's candidates) is bounded by how many brands the answer names. A brand that models name rarely tends to appear when a model goes further down its list, that is, in longer answers, where positions are larger, whatever its standing against the brands it is named with. MNP removes the bound by dividing by list length but keeps the next channel.
2. **Rival mix.** A brand's position in an answer depends on which rivals happen to share it. A frequently named brand is compared, across its answers, with a different mix of rivals than a rarely named one, so its average or modal position partly reflects the company it keeps.
3. **Substance.** Models may list brands in the order of how strongly they associate them with the category, so that being named often and being named early are one fact.

Channels 1 and 2 are construction; channel 3 is the question. v1.10 and v1.14 cannot tell them apart: their H1 values (0.27–0.37) are compatible with any mixture. The program's literature check (Nov 11, 2026) placed it the same way: “where position is noise, a ranking signal falls back onto Presence.”

### 1.2 The measure: co-mention precedence (PREC)

PREC asks, **for every pair of registry brands named in the same answer, which one comes first**, and fits one strength per brand from all such head-to-head outcomes in the category (Bradley–Terry). It never uses an answer that names only one of the two brands, never uses a brand's absolute position, and adjusts each head-to-head for the strength of the rival. So, by construction:

- list length does not enter the direction of the score (appending brands after a pair leaves that pair's outcome unchanged);
- the rival mix is modelled, not averaged over;
- naming frequency changes only the **number** of comparisons (the precision of the estimate), not their **expected outcome** (unit tests `test_frequency_does_not_enter_direction`, `test_list_length_does_not_enter`).

What PREC cannot remove is channel 3, and it should not: if the brands models name most are also the brands they name first among those named together, PREC will track Presence, and that overlap is substantive. This is why this measure can be the last one. If PREC passes, Ranking carries information that Presence does not. If PREC fails on separability from Presence, the overlap is not an artefact of how position was summarised, and Ranking is reported as part of Presence (§8). If PREC fails on reliability, precedence among co-named brands is too unstable to score, which is the outside evidence's reading of position (§1.3), and the same consequence follows.

**Why pairs, not whole lists.** Plackett–Luce models the whole ordered list; its fitted strengths use the same orders. Breaking each answer into all its pairs and fitting Bradley–Terry is the simplest form in which the two by-construction properties above hold and can be tested directly, and it uses every co-mention. The Bradley–Terry and Plackett–Luce models are standard paired-comparison and ranking models; no source for them is cited here because the program's literature check has not verified one.

### 1.3 The outside evidence (cited only for what the program's literature check verified)

- **SparkToro with Gumshoe** (Rand Fishkin, Jan 27, 2026; research partner Patrick O'Donnell, Gumshoe.ai; the author notes it is not peer-reviewed; verified). 600 volunteers ran 12 prompts 2,961 times in ChatGPT, Claude and Google AI (consumer apps, default settings), Nov–Dec 2025; Gumshoe added plain API runs. The same brand list twice in fewer than 1 in 100 answers; the same list in the same order about 1 in 1,000; visibility share steadier than position (City of Hope in 69 of 71 ChatGPT answers, first in 25); smaller markets steadier; the authors advise asking 60–100 times.
- **Schulte, Bleeker and Kaufmann**, “Don't Measure Once: Measuring Visibility in AI Search (GEO)”, arXiv 2604.07585 (Apr 2026; verified): same-day brand overlap (Jaccard) 0.327–0.477; at least 7 runs per prompt per day for brand visibility (bootstrap standard error 0.081 at 7).
- **Boffa, Farronato, Fedele, Levi and Mantovani**, “An Empirical Audit of LLM Product Recommendations”, NET Institute Working Paper 26-09 (Aug 2026; **partly verified: EconPapers record and abstract only; the full text was not read**). From the abstract: six models (ChatGPT, Gemini, Claude, DeepSeek, Grok, Mistral), standardized prompts, repeated queries across 100 product and service categories; “In 20 of the 100 product and service categories, a single product is listed first in more than three quarters of responses”; large differences between models.

What this implies for the design. Whole lists and whole orders rarely repeat (SparkToro, Schulte), so a statistic built on a brand's full positions inherits that noise, and its steadiest part is how often the brand is named, which is Presence. But the top of the order can be concentrated (Boffa et al.: one product first in more than three quarters of answers in a fifth of categories; SparkToro: City of Hope first in 25 of 71). Head-to-head precedence uses exactly the part of the order that can be stable, and pools it over every answer of a category and wave (36 answers at t1–t3, 54 at t4), in line with the advice to measure many times (SparkToro; Schulte).

### 1.4 Predictions (stated before any PREC value exists)

- **P1 (Presence).** PREC correlates **positively** with Presence (v1.10: brands named more often tend to be named earlier; SparkToro's most-named example was also often first). Whether the correlation stays within |ρ| ≤ 0.30 at every wave is what H1 tests; no band is predicted.
- **P2 (reliability).** The t1 → t2 retest of PREC is lower than MODE's archived 0.858 (n 53) because PREC uses no frequency information, the steadiest part of the signal (SparkToro); it is higher in smaller categories (SparkToro) and in categories with higher first-position concentration (Boffa et al.). Whether it reaches 0.50 is what H3 tests.
- **P3 (Consistency).** PREC is separable from Consistency, as MNP and MODE were (v1.10 H2; v1.14 H2).

## 2. Research questions

- **RQ1.** Is co-mention precedence separable from Presence and from Consistency at every wave (t1, t2, t3, t4)?
- **RQ2.** Is it reliable: does the brand order by precedence hold from t1 to t2 beyond what list composition alone produces?
- **RQ3 (exploratory).** Does separability or reliability depend on category size or on first-position concentration?

## 3. The statistic

### 3.1 Comparisons

Within one panel × wave × condition and one category (substrate), every **rankable answer** (one that names ≥ 2 registry brands; v1.10 E5) contributes, for **every pair** of registry brands it names, one comparison:

- the brand with the smaller **competition min-rank** k_min (v1.10 E7) wins; equal k_min is a tie and gives half a win to each;
- positions come from the **lead-item rule** (v1.10 E6, primary): in a list-structured answer brands are ordered by the first item they lead, otherwise by first mention; first mention everywhere is sensitivity S1;
- every comparison has weight 1 (an answer naming k brands gives k(k − 1)/2 comparisons); weight 1/(k − 1) per comparison, so that every brand's comparisons in an answer sum to 1, is sensitivity S_w;
- all comparisons of the category in the panel × wave × condition are pooled over models, runs and questions (as v1.10 and v1.14 pool), into one win matrix W (W_ij = weighted wins of i over j).

### 3.2 Estimation

PREC_b = θ_b, the Bradley–Terry log-strength maximising

Σ_i Σ_j W_ij log σ(θ_i − θ_j) + Σ_b [ (λ/2) log σ(θ_b) + (λ/2) log σ(−θ_b) ],  σ(x) = 1/(1 + e^(−x)),

where the second sum gives every brand **λ = 1 virtual comparison** (half won, half lost) against a reference brand of log-strength 0. The virtual comparison keeps every estimate finite (a brand that always wins or always loses), anchors the scale, and makes the objective strictly concave, so the maximum is unique. It is computed by Newton–Raphson with step halving from θ = 0 until no coordinate moves by more than 10⁻¹⁰ (at most 500 iterations); `score_v1_16.fit_bt`. Higher PREC = named before the brands it is named with. Brands below the rating floor enter the fit as rivals. λ = 0.1 and λ = 10 are sensitivities (S_prior). The virtual comparison shrinks rarely compared brands toward the reference; it does not depend on which brand is more often named first.

### 3.3 Rating

A unit (substrate, brand) is **rated** in a panel × wave × condition iff it has **≥ 6 rankable mentions** (v1.10's floor, unchanged) **and** lies in the largest connected component of its category's comparison graph (brands linked by at least one co-mention; an isolated group has no common scale with the rest). Never-named brands are not rated (absence is Presence's information). Floors 3 and 10 are sensitivity S2. The count of units at the floor that fall outside the main component is reported (MQ9).

### 3.4 Condition and panels

Primary PREC uses the **search-off** answers (S0) of every wave; at t4 a separate PREC_S1 from the search-on answers enters only H4_S1 and the descriptive D3. No per-model or per-run statistic enters a verdict.

## 4. Data and inputs

### 4.1 Waves

| Wave | Source | Panel | Answers per category | Rankable answers | Rankable rows | Comparisons (pairs) | Units at floor (with P / with C\*) |
|---|---|---|---|---|---|---|---|
| t1 (May 20–26, 2026) | v1.10 rank tables `OMNI t1 v0.19…v0.23` | LEGACY-6, 6 questions, 1 run | 36 | 161 of 180 | 934 | 2,606 | 55 (55 / 55) |
| t2 (Jun 10, 2026) | `OMNI t2 …` | same | 36 | 161 of 180 | 923 | 2,547 | 54 (54 / 54) |
| t3 (Nov 9, 2026) | `OMNI t3 …` | same | 36 | 161 of 180 | 903 | 2,374 | 54 (54 / 54) |
| t4 S0 (v0.42, November 2026) | v1.14 Stage 1 rank table | N3: Claude Fable 5.2, GPT-6 Astra, Gemini 4 Argon; 6 questions; 3 runs | 54 | 262 of 270 | 1,641 | 4,925 | 71 (71 / 70) |
| t4 S1 | same | same, provider web search on | 54 | 241 of 270 | 1,375 | 3,806 | 65 |

Counts from `prereg/input_parity_v1_16.json` (§4.3). The n's of the confirmatory tests can be smaller than the units at the floor, because PREC also requires the main comparison component (§3.3). At t4, 540 Phase B answers form v0.42's analysis set (v1.14 §5.1).

### 4.2 Pinned files (SHA-256; the scorer halts on any mismatch)

| File | SHA-256 | Role |
|---|---|---|
| `osf/methodology/v1_10/outputs/v1_10_verdicts.json` | `d4250ba79a6acfb9e211dbc561311da9fc07581bebf871dea3dbe149d6bdcb28` | pins v1.10's 31 rank tables (each verified against it before use); the 15 OMNI tables are also in the lock manifest |
| `osf/aias_2_0/aias_2_0_profiles.csv` | `022ef56ecad9ddb60ad9ce0a2129698fd84ee9656630500e30b05f1e4b7e8c6e` | P and C\* at t1–t3 (the locked table v1.10 and v1.14 used) |
| `osf/methodology/v1_14/outputs/stage1/rank_table_t4_v1_14.csv` | `5e6286589f26c802da17b87db47b002707225dbea3950a093d1b63a6f1a0a23d` | t4 positions (S0, S1; both rules); must equal the SHA-256 that v1.14 Stage 1 recorded |
| `osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json` | `4de97fea86fd7c74f990ba4bdecd43c19aa52afc60278676624374a164f68e2f` | P_S0, C\*_S0, P_S1 at t4 (v1.14 §5.2, the definition shared with v1.12 and v1.13) |

The 15 OMNI rank tables and every other locked file are listed with their SHA-256 in `prereg/LOCK_MANIFEST_v1_16.sha256`.

**Sources and held studies.** These are the sources v1.14 used. v1.10's rank tables contain no answer from the program's held studies (v0.38, v0.39), which v1.10 excluded entirely; v0.28 entered v1.10 only as a parse-only set (MQ1 parse completion; it is held for the conflict-of-interest review) and is in no rank table; v1.16 reads neither. v1.10's early-panel tables (EARLY-6) are read only for the exploratory E3; its EARLY-2 and PAPER-B tables are hash-checked and not used. The t4 positions were extracted once, by v1.14 Stage 1, from v0.42's acquisition-locked raw answers with v1.10's extractor (URLs removed as v0.42 §5.1 does); no answer is re-extracted here.

### 4.3 What was looked at before the lock (declared)

- **Seen before v1.16 existed:** every statistic v1.10 and v1.14 published on these waves: MNP and all six v1.10 candidates through H1–H3 at t1–t3 (v1.10 sensitivity S3), MODE at t4 with its sensitivities (including all six candidates at t4), and the per-unit MODE values in v1.14's unit table. The design of PREC was motivated by those results (both position statistics track Presence), as §1.1 states.
- **Computed for v1.16 before the lock, on real data:** input parity only (`scripts/score_v1_16.py --parity`, 2026-11-12): pin verification; numbers of answers, rankable answers, rankable rows and co-mentioned pairs per wave; units at the rating floor and their joins with P and C\*. It reproduces every count v1.10 and v1.14 published for these inputs: t1–t3 n's 55 / 54 / 54 (P and C\*, v1.10 S3 for MODE); t4 540 answers, 1,641 S0 and 1,375 S1 rankable rows, 71 units at the floor, 71 with P and 70 with C\* (v1.14 Stage 1). The parity file contains no PREC value, no win count by brand, no correlation and no first-position concentration.
- **Not computed on any real answer before the lock:** PREC, any pairwise win record, any H1–H5 statistic, any moderator value.

## 5. Comparators

- **t1–t3:** P and C\* from the locked AIAS 2.0 profiles table, as v1.10 used them (`score_v1_10.parse_profiles`; C\* rated units only).
- **t4:** P_S0 = 100 · (C_P/3 + 2 · π̂_S0)/3 and C\*_S0 = 100 · (1 − φ_S0/9) (rated at ≥ 6 N3 Phase B mentions), P_S1 with π̂_S1, exactly as v1.14 §5.2 defines and computed them, read from v1.14 Stage 1's unit table (which v1.14 checked against v0.42's coded tables, MQ8).

## 6. Hypotheses, thresholds and verdict rules

ρ_w is v1.10's pooled within-category Spearman correlation: Pearson correlation of within-category average ranks **centred** on the category mean rank, over the categories with ≥ 5 units, values compared unrounded (`score_v1_10.pooled_within_rho`, imported unchanged). A wave is **determined** iff its n ≥ 30 units and ρ is finite. Permutation p = (hits + 1)/(N + 1), PREC permuted within category, 10,000 draws. Bootstrap 90% percentile CIs (2,000 draws, units resampled within category, seed 110020) are reported and never enter a verdict.

| Tag | Tier | Statement | Statistic and data | Null / seed | CONFIRMED iff | FALSIFIED iff | MARGINAL | UNDETERMINED |
|---|---|---|---|---|---|---|---|---|
| **H1_Sep_Presence** | PRIMARY (gate) | PREC is separable from Presence. | ρ_w(PREC, P) at t1, t2, t3 and t4 (S0); rated units with P | permutation, two-sided, seed 116001 (reported) | \|ρ\| ≤ 0.30 at **every** determined wave | \|ρ\| ≥ 0.50 at **any** determined wave | otherwise | fewer than 3 of the 4 waves determined |
| **H2_Sep_Consistency** | PRIMARY (gate) | PREC is separable from Consistency. | ρ_w(PREC, C\*) at t1–t4 (S0); units rated on both | as H1, seed 116002 | as H1 | as H1 | otherwise | as H1 |
| **H3_Retest_t1_t2** | PRIMARY (gate: reliability) | The brand order by precedence holds from t1 to t2 beyond list composition. | ρ_w(PREC_t1, PREC_t2), units rated at both waves (categories with ≥ 5 such units) | (a) PREC_t2 permuted within category, 10,000, seed 116003, one-sided; (b) within-answer order shuffle of both waves (every answer's named brands put in a uniformly random order, named set and length kept), PREC refitted, 10,000, seed 116010, one-sided | ρ ≥ 0.50 and p_perm < 0.05 and p_shuffle < 0.05 | ρ < 0.30 or p_perm ≥ 0.05 or p_shuffle ≥ 0.05 | otherwise | n < 30 |
| H4_Sep_Presence_t4_S1 | SECONDARY (gate downgrade only) | Separability from Presence replicates with web search on. | ρ_w(PREC_S1, P_S1) at t4 | seed 116004 | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise | n < 30 |
| H5_Retest_t2_t3 | SECONDARY (reported; no gate role) | The order holds over five months. | ρ_w(PREC_t2, PREC_t3) | as H3, seed 116005 (shuffle 116010) | as H3 | as H3 | as H3 | as H3 |

H1 and H2 use v1.10's multi-wave rule (every wave inside the band; one wave at 0.50 or above falsifies), applied to the four waves the archive holds, with “at least 3 of 4 determined” in place of v1.10's “at least 2 of 3”. H3 is v1.10's H3, unchanged in rule and data. H4_S1 is v1.14's search-on replication leg. The t1–t3 waves are the legacy panel; t4 is the newest panel; every separability verdict needs both.

## 7. Precision and power (analytic, before any data)

Fisher z with the Bonett–Wright variance (1 + ρ²/2)/(n − 3), at the n's of §4.1 (t1 55, t2 54, t3 54, t4 71; the rated n's can be a little smaller); `scripts/precision_note_v1_16.py` → `prereg/precision_note_v1_16.json`.

| True ρ(PREC, P) | P(\|ρ̂\| ≤ 0.30) per wave (t1 / t2 / t3 / t4) | P(all four CONFIRMED) if the waves were independent | P(any wave ≥ 0.50) if independent |
|---|---|---|---|
| 0.00 | 0.97 / 0.97 / 0.97 / 0.99 | 0.91 | < 0.001 |
| 0.10 | 0.93 / 0.93 / 0.93 / 0.96 | 0.77 | 0.002 |
| 0.15 | 0.87 / 0.87 / 0.87 / 0.90 | 0.59 | 0.007 |
| 0.20 | 0.78 / 0.77 / 0.77 / 0.81 | 0.38 | 0.023 |
| 0.25 | 0.65 / 0.65 / 0.65 / 0.67 | 0.18 | 0.064 |
| 0.30 | 0.50 / 0.50 / 0.50 / 0.50 | 0.06 | 0.156 |

The four waves score largely the same brands, so their estimates move together and the joint probability lies between the product (independence) and the single-wave value (full dependence). The rule is demanding on purpose: a separate component must be separable on the legacy and the newest panel alike. A measure whose true correlation with Presence is near 0.10 passes H1 with probability of about 0.77 to 0.93; one near 0.20 with about 0.38 to 0.77; one at 0.30 rarely. For H3 (n about 47–53; MODE had 53): P(ρ̂ ≥ 0.50) ≈ 0.97 at a true 0.70, 0.79–0.82 at 0.60, 0.50 at 0.50; P(ρ̂ < 0.30) ≈ 0.23–0.25 at a true 0.40.

## 8. Gate and the consequence clause

**GATE:** FAIL if any of H1, H2, H3 is FALSIFIED; else UNDETERMINED if any of them is UNDETERMINED; else PASS if all three are CONFIRMED and H4_S1 is not FALSIFIED; else MARGINAL. (v1.10's gate rule with the search-on leg in place of the early panel, as v1.14.)

**Consequence clause (Pablo's decision of Wed Nov 11, 2026, 11:22 pm).** If the gate does not PASS (FAIL, MARGINAL or UNDETERMINED), Ranking is reported as part of Presence and not as a separate AIAS component, and there is no further Ranking redesign.

| Gate | Consequence |
|---|---|
| **PASS** | Ranking (PREC) may be reported as a separate AIAS component. Ranking Paper B and the AIAS 3.0 calibration with Ranking may each be pre-registered. Before any calibration that combines Ranking with Coverage, Grounding or Sentiment, ρ_w(PREC, that component) is computed on the same units with the frozen PREC values under v1.10's single-estimate bands; a FALSIFIED result there turns the PASS into FAIL, and the consequence clause applies. |
| **FAIL, MARGINAL or UNDETERMINED** | Ranking is reported as part of Presence and not as a separate AIAS component. There is no further Ranking redesign: no new Ranking statistic, no re-run of v1.16 with other settings, and no sensitivity, secondary result or later wave (t5 included) turns this verdict into a PASS. The result is published with the prominence of a pass. Position results (v1.10, v1.14, v1.16) remain available as descriptions of Presence. |

Secondary results, descriptives, exploratory analyses and sensitivities never change the gate. MQ6, MQ7 and MQ9 flags are printed next to the gate. Release timing is not set here: under the same decision, the next part that passes its gate makes the next release.

## 9. Checks

| Id | Check | Rule |
|---|---|---|
| Pins | Every pinned file (§4.2) matches its SHA-256; every v1.10 rank table matches the SHA-256 in v1.10's verdicts file; the t4 rank table matches the SHA-256 v1.14 Stage 1 recorded | halt |
| Parity | The counts of §4.3 are reproduced (`--parity`, recorded before the lock; `--run` repeats it first) | halt if not all pass |
| MQ6 | Positive control: the gate can detect overlap with Presence. v1.10's penalised MNP reached ρ_w 0.909 / 0.901 / 0.918 with P at t1–t3 (n 112 each) and 0.930 at t4 (n 112) in v1.14 Stage 1 (published values, copied into the results file) | printed |
| MQ7 | Negative control: the mean of H3's 10,000 shuffled retest ρ must stay below 0.20 | flag “list-composition-driven” if ≥ 0.20 |
| MQ9 | Identification: units at the rating floor outside the main comparison component, per wave | printed; flag if more than 10% of the units at the floor in any wave |

## 10. Descriptives, exploratory analyses and sensitivities (reported; never change a verdict)

**Descriptives.** D1 per wave (and t4 S1): rankable answers, rankable rows, units with rows, units rated, comparisons, distribution of PREC over rated units. D2 per wave: ρ_w(PREC, MNP) and ρ_w(PREC, MODE) on units rated by both (how much of v1.10's and v1.14's statistics PREC shares). D3: ρ_w(PREC_S0, PREC_S1) at t4.

**E1, moderators (declared; RQ3).** Two moderators, fixed now:

- **Category size** = registry brand count of the substrate (v0.19: 16; v0.20–v0.23: 24 each; from the locked profiles table). With two distinct sizes this is a contrast of the headphones category against the other four, not a gradient.
- **First-position concentration (FPC)** of a category in a wave = over its rankable answers, the share in which the **modal first brand** (the brand most often at k_min = 1; ties broken alphabetically) is first (the literature check's definition: “share of runs where the modal first brand is first”). Computed per category × wave on S0.

Reported: for every category × wave (20 cells), FPC, the modal first brand, the within-category Spearman ρ(PREC, P) and its n; across cells with ≥ 5 rated units, the Spearman correlation of |ρ(PREC, P)| with category size and with FPC; the t1 → t2 retest per category with its n and category size. Expectations (§1.4, P2): retest higher in the smaller category and in higher-FPC categories; no directional expectation for separability. With five categories these are descriptions, not tests; Ranking Paper B, if the gate passes, pre-registers them as moderators on new data.

**E3, early panel.** ρ_w(PREC, π̂) on v1.10's EARLY-6 sets (v1.10's H4 data; π̂ = share of the set's answers naming the brand), permutation seed 116020; descriptive, as the closest analogue of v1.10's H4.

**E4, other components.** When locked Coverage, Grounding or Sentiment scores exist on the same units, ρ_w(PREC, that score) is computed from the frozen per-unit PREC table of the results file and reported (exploratory here; §8 makes it binding before any combined calibration after a PASS).

**Sensitivities of H1 and H2** (each recomputed at all four waves under the same rule; every verdict change is listed next to the verdict): S1 first-mention order; S2 rating floors 3 and 10; S7 without the Denon unit; S-COI without Denon and the five brands with Cheil Worldwide or Iris agency ties (§15; 106 units remain in the registries); S9 uncentred ranks; S_w comparison weight 1/(k − 1); S_prior λ = 0.1 and λ = 10; S4 leaving out each substrate in turn.

## 11. Dry run on synthetic data with a known answer (recorded before the lock)

`python3 scripts/score_v1_16.py --dry-run` (full draws: 10,000 permutations and 10,000 shuffles; bootstrap off) writes `dryrun/dryrun_v1_16.json` and `dryrun/dryrun_run_v1_16.log`. It builds three synthetic input sets in the formats of the real inputs (v1.10 rank tables for t1–t3 with 6 models × 6 questions per category, a profiles table, a v1.14-format t4 rank table with 3 models × 6 questions × 3 runs in S0 and S1, and a unit table), with the real category sizes (16, 24, 24, 24, 24) and list lengths of 0–10 brands, and runs the whole pipeline through the same loaders. Brands have a popularity u (inclusion in an answer by popularity) and a precedence v (order within the answer, with noise):

| World | Construction | Expected | Result |
|---|---|---|---|
| A, independent precedence | v balanced against u (no popularity trend) | PASS | **PASS.** H1 ρ 0.071 / 0.034 / −0.070 / 0.102 (n 53 / 60 / 57 / 69) CONFIRMED; H2 0.155 / 0.037 / −0.064 / 0.216 CONFIRMED; H3 0.948 (n 47; p_perm and p_shuffle 0.0001) CONFIRMED; H4_S1 0.029 (n 72) CONFIRMED |
| B, popularity order | v = u (position is Presence) | FAIL with H1 FALSIFIED | **FAIL.** H1 0.840 / 0.843 / 0.829 / 0.811 (n 55 / 58 / 52 / 66) FALSIFIED; H2 CONFIRMED; H3 0.863 (n 50) CONFIRMED; H4_S1 0.869 FALSIFIED |
| C, noise order | order uniformly random (no precedence) | FAIL with H3 FALSIFIED | **FAIL.** H3 −0.100 (n 52; p_perm 0.746; p_shuffle 0.752) FALSIFIED; H1 0.170 / 0.065 / 0.014 / −0.119 CONFIRMED; H2 MARGINAL (one wave 0.376 against a random C\*); H4_S1 0.046 |

All three worlds give the expected verdicts. Checks inside the record: PREC recovers the true precedence (ρ_w(PREC, v) = 0.936 / 0.939 / 0.969 / 0.930 in world A and 0.903 / 0.905 / 0.827 / 0.924 in world B); in world A the true ρ_w(v, P) on the rated units is 0.063 / 0.040 / −0.012 / 0.101, close to H1's estimates; the mean shuffled retest ρ (MQ7) is 0.001, 0.002 and 0.003; no MQ7 flag. For comparison, MODE's ρ_w with P in world C, where order carries no information, was 0.382 / 0.055 / −0.007 / 0.203 against PREC's 0.170 / 0.065 / 0.014 / −0.119: one illustration of the list-length channel of §1.1 on synthetic data, not evidence about the real waves. In world A two sensitivities (floor 10; leaving out v0.21) read H2 MARGINAL, by chance against a random C\*; they change no verdict.

Two earlier versions of world A are declared (both run with 100 shuffle and 200 permutation draws, same seed). The first drew precedence at random, independently of popularity: H1 ρ −0.375 / −0.198 / −0.576 / −0.141, FALSIFIED. The second made that draw exactly uncorrelated (Pearson) with popularity over all brands of each category: H1 −0.311 / −0.137 / −0.519 / −0.036, FALSIFIED. The reason was checked afterwards with the truth check (`dryrun/check_world_A_versions.py` → `.log`, synthetic data only): at that seed, among the rated units, the drawn precedence itself correlated with Presence at ρ_w −0.365 / −0.236 / −0.539 / −0.203 (first version) and −0.267 / −0.133 / −0.442 / −0.103 (second), so those worlds did not have the property they were meant to have, and PREC reported it (H1 estimate minus truth between −0.08 and +0.07). Over five further seeds of each version, the H1 estimate minus the truth ranged from −0.12 to +0.14 per wave (40 wave values; mean +0.009). World A was rebuilt so that precedence carries no popularity trend within any block of eight brands adjacent in popularity, and the truth check was added to the record. The scorer's statistic, rules and thresholds were not changed by these iterations. The other two worlds were not changed.

## 12. Order of operations (enforced by `scripts/score_v1_16.py`)

1. Before the lock (done): `--parity` (§4.3) and `--dry-run` (§11); unit tests.
2. Lock (§0): `--lock-manifest`, commit, tag `v1.16-prereg-r1`, push, OSF deposit with SHA-256 verified, then `--write-anchor --osf-note "<OSF location>"` (refuses without the tag or with a changed locked file).
3. `--run`: refuses unless the tag exists, the anchor file exists, every file of the lock manifest is unchanged and no results file exists; **runs once**; writes `outputs/results_v1_16.json` with the gate, the consequence, every test, check, descriptive, exploratory analysis and sensitivity, and the per-unit PREC table.

## 13. Deviations policy

`anchor/DEVIATIONS.md` opens with Entry 0 (ex ante). After the lock every change gets an entry (id, date, ex ante or ex post, what, why, effect on inference); a hash mismatch halts; a code fix is allowed only to restore a rule as written here, with results reported before and after; the statistic, prior, floors, bands, seeds, nulls, gate rule and consequence clause do not change; anything added later is exploratory; a failed gate is published with the prominence of a pass.

## 14. Limitations

- All four waves have been seen with other position statistics (§4.3); PREC is new, but the decision to build a frequency-free measure was taken after seeing that MNP and MODE track Presence. The thresholds, rules and data were fixed before any PREC value existed.
- PREC removes the list-length and rival-mix channels by construction, not the substantive channel (§1.1); a FAIL on H1 says that, on these data, precedence among co-named brands goes with how often brands are named, not why.
- Pooling over models assumes one precedence per brand per wave; models that disagree on order lower reliability (H3), which is part of what is tested. The t1 → t2 retest is on the legacy panel; the newest panel has no second wave inside the archive (its t5 retest belongs to v1.14 Stage 2, reported for the record only).
- The rating floor (6 mentions) leaves about half of the 112 units unrated at every wave; the result is about brands named often enough to have a position.
- Positions are among registry brands only; position in text is not visual prominence; the lead-item parser relies on Markdown conventions. Five categories, US English, provider-default settings. t4 Presence rests on one recognition answer per model (v0.42 §9 C13). The outside evidence is partly from a non-peer-reviewed study (SparkToro) and an abstract (Boffa et al.).

## 15. Declarations

### Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses archived answers already scored against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.10 DEVIATIONS Entry 0; v1.14 DEVIATIONS Entry 0; v1.16 DEVIATIONS Entry 0). Three items of record apply to the registries used.

*Audiophile headphones (v0.19).* The v0.19 record states: “The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock.” (v0.19 paper, Declaration of interest; see also v0.19 pre-registration §2.3 and v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN, “HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership”, press release, Business Wire, September 23, 2025. In this study Denon remains in the locked registry and in the primary analysis; every separability statistic is also reported without the Denon unit (sensitivity S7).

*Automotive (v0.22).* The v0.22 record states: “Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed.” (v0.22 paper, Conflict of interest.) These are supply relationships, not ownership; no v0.22 brand is removed in this study.

*Agency work (Cheil Worldwide and Iris).* Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024). (Conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F.) As Denon, these five brands stay in every analysis, and every separability statistic is also reported without them and Denon (sensitivity S-COI, 106 units).

Extraction and scoring are automated against the locked registries and this pre-registration. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

### Funding {-}

Self-funded. No external funding supported this research.

### Ethics {-}

Not applicable; no human subjects. The study analyses responses of large language models queried under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 16. Files

`prereg/PRE_REGISTRATION_v1_16.md` (this file); `prereg/LOCK_MANIFEST_v1_16.sha256`; `prereg/input_parity_v1_16.json` (§4.3); `prereg/precision_note_v1_16.json` and `scripts/precision_note_v1_16.py` (§7); `dryrun/dryrun_v1_16.json`, `dryrun/dryrun_run_v1_16.log`, `dryrun/check_world_A_versions.py` and its `.log` (§11); `anchor/DEVIATIONS.md`; `README.md`; `scripts/score_v1_16.py` and `scripts/test_score_v1_16.py` (repository root; 23 unit tests); `scripts/score_v1_10.py` and `scripts/score_v1_14.py` (imported unchanged); the pinned inputs of §4.2 and the 15 OMNI rank tables, all listed in the lock manifest.

## 17. Choices made in drafting (argued above; recorded for the reader)

1. The measure: Bradley–Terry precedence over co-mentions (§1.2), not a residualised position (a position score with Presence regressed out would pass H1 by construction and make the gate empty).
2. All pairs of an answer, weight 1; a virtual comparison λ = 1 for finiteness; rating floor 6 (v1.10) plus the main comparison component.
3. Every archived wave enters the gate: t1–t3 (legacy panel) and t4 (newest panel) for separability, with v1.10's every-wave rule; t1 → t2 for reliability (v1.10's H3); t4 search-on as a downgrade-only leg (v1.14). v0.38, v0.39 (held) out; v0.28 not read (parse-only in v1.10, conflict-of-interest hold).
4. Category size and first-position concentration are declared exploratory moderators (E1), not gate legs: five categories cannot carry a moderator test.
5. The consequence clause applies to every outcome other than PASS, UNDETERMINED included.
