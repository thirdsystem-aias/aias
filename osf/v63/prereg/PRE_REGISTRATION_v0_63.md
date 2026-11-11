# AIAS v0.63 — Panel-construction sensitivity: do the Recognition × Recall verdicts survive other ways of building the panel?

AIAS™ Measurement Program — Third System™. Pre-registration **r1** (draft of 2026-11-11, revised the same day after the coordinator's review of commit `986dedd`; §16). To be locked at git tag `v0.63-prereg-r1` and deposited on OSF (`osf.io/ec6wh/v63/`) before any statistic named in §6 is computed on the archive.

**Pre-registrant:** Pablo Ulpiano González Castro

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v0.63 (roadmap study #54, Phase P "Cross-cutting expansion", `Try system book/aias_roadmap_ssot.md` line 107: "Panel-construction sensitivity study: vary panel-build rules, test Recognition × Recall verdict stability"). Shares a cross-cutting paper with #55 (cross-cultural Identity Load) later. |
| PHASE_TYPE | Pre-registered **re-analysis** of archived answers. No collection, no model call, no network, no spend. |
| Number | Phase P slots into v0.62–v0.68 (roadmap line 103). v0.62 is taken (non-English wave; local branch `v0.62`, tip `4f3a226`). On 2026-11-11 no `v0.63` branch or tag existed locally or on origin (`git branch -a`, `git tag -l`, `git ls-remote --heads --tags origin`), and the OSF project's top-level folders ended at `v44` (read-only listing of `api.osf.io/v2/nodes/ec6wh/files/osfstorage/`). |
| Branch and base | `v0.63`, from `v1.14` @ `ceb706d`. `ceb706d` is a strict superset of `v1.10` @ `bad8c41` (`git merge-base --is-ancestor bad8c41 ceb706d` holds; `bad8c41..ceb706d` only adds `osf/methodology/v1_14/` and `scripts/score_v1_14.py` / its tests). It carries every omnibus answer file of t1, t2 (`osf/v34/data/`) and t3 (`osf/v41/data/`), the certified three-wave loader `osf/v41/scripts/score_v41.py`, the registries, the v1.10 loaders and the v1.14 lock/anchor pattern. |
| Status | r1 draft, not locked. Parity run on 2026-11-11 (§7, all eight checks pass). No §6 statistic and no alternative-panel verdict has been computed on the archive. |
| Locks on | content lock → `prereg/LOCK_MANIFEST_v0_63.sha256` → commit → tag `v0.63-prereg-r1` → push branch and tag → OSF deposit of `osf/v63/` (prereg, registries, scripts, anchor/DEVIATIONS) → `--write-anchor` (`anchor/git_anchor_v0_63.json`) → `--run`, once (§10, `LOCK_STEPS.md`). |
| Locked method | Recognition × Recall instrument of v1.4 (SSRN 6799479) with the v1.5 C2 rule (SSRN 6810758) and the v1.6 Increment 1 pre-screen (SSRN 6816340), thresholds as frozen in `prereg/v0_21_registry.json` key `thresholds` (§5). |

## 1. The question, and what the archive can and cannot answer

Every Recognition × Recall verdict the program has published was computed on one hand-built panel per substrate: tiered cells chosen by the author (heritage / boutique; prestige / celebrity-DTC / mass; heritage / disruptor / mass / defunct), filled in a cascade order, screened for conflicts of interest and, in places, flagged as borderline or cross-cultural. This study asks whether the verdicts depend on those choices.

**A structural fact fixes what can vary.** The archived Phase A probes ask about one brand at a time ("Is the brand X commonly recognized as …?") and the Phase B frames never list brands (`osf/v19/thresholds_v0_19.json` keys `phase_a.probe_template`, `phase_b.frames`; `prereg/v0_21_registry.json` keys `phase_a_probe_template`, `phase_b_frames`). A brand's C_P, R_cat and R_cult, and hence its Iwachu / Type 1 / Type 2 membership, are therefore the same whatever else is on the panel. Panel construction can only move the **panel-relative** results: the substrate-level verdicts that aggregate over cells (Regime 4 routing, Type 2 emergence, dissociation generalisation) and the within-panel quartile regime of each brand. This study tests those; brand-level invariance is checked, not tested (MC1).

**What the archive cannot answer.** (a) Whether the answers themselves would change with a different panel (the archived prompts carry no panel context); (b) panels containing brands that were never probed for Recognition (off-panel brands named in Phase B answers have Recall but no C_P); (c) any model generation other than the legacy six. The strongest archive version is pre-registered here; the smallest new collection that would answer (a) and (b) is proposed separately in §13, outside this lock.

## 2. Research questions

- RQ1. Do the substrate-level Recognition × Recall verdicts keep their value when the panel is rebuilt under each alternative rule the program has itself used or recorded?
- RQ2. Do brands keep their within-panel regime when a quarter of each cell is removed at random?
- Scope: the five omnibus substrates at three waves and v0.18 (indie fragrance) at t1; v0.17 cannot enter (§3).
- RQ3. Are purposive (substantively motivated) rebuilds more disruptive than random removals of the same number of brands?
- RQ4. Are the three disclosed panel-handling choices (defunct-brand cell, the brand flagged in the conflict-of-interest record, cross-cultural flags) verdict-neutral?

## 3. Data (archived; nothing new)

The legacy six-model panel (claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite) on the five omnibus substrates at three waves (dates from `osf/v41/v41_verdicts.json` key `delta_t`) and on v0.18 at one wave (acquired 2026-05-20, `osf/v18/data/phase_b_results.json` key `acquired_at_utc`):

| Substrate | Registry (frozen) | Brands | Cells (brands) | t1 | t2 | t3 |
|---|---|---|---|---|---|---|
| v0.19 audiophile headphones | `osf/v19/panel_registry_v0_19.csv` | 16 | A_Heritage 8, B_Boutique 8 | 2026-05-20 | 2026-06-10 | 2026-11-09 |
| v0.20 skincare | `prereg/v0_20_registry.json` | 24 | A 8, B 8, C 8 | 2026-05-21 | 2026-06-10 | 2026-11-09 |
| v0.21 cosmetics | `prereg/v0_21_registry.json` | 24 | A 8, B 8, C 8 | 2026-05-22 | 2026-06-10 | 2026-11-09 |
| v0.22 automotive | `prereg/v0_22_automotive_content.py` (`REGISTRY`) | 24 | A 7, B 5, C 7, D_Defunct 5 | 2026-05-25 | 2026-06-10 | 2026-11-09 |
| v0.23 premium spirits | `osf/methodology/v1_10/registries/v0_23_registry_v1_10.json` | 24 | none | 2026-05-26 | 2026-06-10 | 2026-11-09 |
| v0.18 indie fragrance (single wave) | `REGISTRY` of `osf/v18/scripts/acquire_phase_a_v18.py` (cascade order = list order, v0.18 pre-registration §1.4) | 24 | A designer-niche 8, B indie-artisan 8, C mass-prestige 8 | 2026-05-20 | — | — |

Omnibus: 112 brand units per wave, 336 brand-waves, 15 substrate-waves; with v0.18: 136 brands, 360 brand-waves, **16 substrate-waves**. Per omnibus substrate-wave: 6 Phase A answers per brand (C_P 0–6) and 36 Phase B answers (6 models × 6 frames; R_cat and R_cult each 0–18; for v0.23 the EA frames are the category channel and the CC frames the cultural channel). v0.18 (v1.4 single-channel design): 6 Phase A answers per brand and 18 Phase B answers (6 models × 3 category frames, q1_niche, q2_independent, q3_perfumistas); R_cat 0–18, no cultural channel (R_cult = 0). Answer files: t1 `osf/v19/`, `osf/v20/`–`osf/v22/` (`phase_a_results.csv`, `phase_b_results.csv`), `osf/v23/data/` (`v23_phase_a_scored.json`, `v23_phase_b_scored.json`); t2 the same names under `osf/v34/data/`; t3 under `osf/v41/data/` (30 files, all pinned in the lock manifest). They are read only through the certified loader `load_wave` of `osf/v41/scripts/score_v41.py` (which imports `scripts/score_v0_31.py`, `scripts/score_v33.py` and the v0.20–v0.22 matchers), the lineage that produced the published three-wave table. v0.18 is read by a loader written for this study (`load_v18` in the scorer): Recognition from the per-model yes/no codes of `osf/v18/data/phase_a_results.json`; Recall **re-detected from the 18 raw answers** (`phase_b_results.json` key `_raw_query_records`) with v0.18's own parser (`osf/v18/scripts/protocol/parse.py`) and alias map (`BRAND_ALIASES` in `osf/v18/scripts/acquire_phase_b_v18.py`, read without importing the acquisition module).

**Out of scope, and why.** v0.38 and v0.39 are held studies (CLAUDE.md, "Category studies"). v0.28's technology panel is held for its COI screen (v1.10 treats it as parse-only, `scripts/score_v1_10.py` `PARSE_ONLY_ROLES`); it is not loaded here at all. v0.32 arms (a model-version pair, different panel generation), the early categories (v0.6–v1.0, v0.14, v0.16: no yes/no Recognition arm comparable to the omnibus) and the t4 wave (v0.42) are out. **v0.17 (premium kitchenware) cannot enter.** Its Phase A probed only the cell pivots in its cascade (`osf/v17/data/phase_a/`: 24 answers for 4 brands, Le Creuset, All-Clad, Vermicular and Iwachu; `osf/v17/phase_b_lock.md` lines 19–35 list the Phase A role of each of its 15 panel brands), so a per-brand C_P exists for 3 of the 15 panel brands (Vermicular was replaced by Iwachu). No Recognition × Recall family (§5) and no regime (F4) can be computed, and there is no per-brand Recognition value to reproduce, so no loader was written; v0.17 is reported as not measurable on the archive (§13 covers it). Its Phase B (18 answers, three frames) has published per-brand mention counts (`phase_b_lock.md` lines 21–35) that a Recall-only loader could reproduce, but Recall alone carries none of this study's verdicts. The v0.23 Recognition arm is judge-coded (`osf/v23/ERRATA.md`, `scripts/score_v0_23.py`); its C_P is taken as the certified loader returns it.

**Conflict-of-interest handling of the included registries.** Denon (v0.19, Cell A) is the brand flagged in the conflict-of-interest record (Declarations). It stays in the canonical panel R0, as in every earlier study; rule R2 removes it, H4 tests whether that changes anything, and sensitivity S1 repeats H1, H2 and H4 without Denon in any v0.19 panel. AKG and JBL are in none of the six registries (checked by text search of the registry files). The v0.22 registry carries the tier-2/3 supply relationships stated in the Declarations; no v0.22 brand is removed for them. The v0.18 records hold no registry screen: its DEVIATIONS file has no Entry 0, and its paper's Declaration of interest makes no brand-level statement (`papers/v0_18/v0_18_ssrn_paper_draft.md` line 317; Declarations below). Its registry is carried as locked; this study adds no screen of its own (§16). The v0.17 records likewise hold no Entry 0 (`papers/v0_17/v0_17_ssrn_paper_draft.md` line 292 is its declaration); as asked, its panel was checked for appliance makers: one brand, Hestan (American cell), is also known for cooking appliances (the drafting lane's general knowledge, not checked against a cited source). v0.17 is not analysed, so no handling is needed here; the finding is recorded for the program (§16).

## 4. Panel-build rules (finite, fixed here)

Each rule maps a locked registry to a sub-panel. Only sub-panels that differ from R0 and from every earlier rule's sub-panel for the same substrate-wave are comparisons (a duplicate is counted once, under the first rule in this order). Structural rules (R1–R6, R11) read the registries only; their application is frozen in `registries/panel_rules_v0_63.json` (written by `--rules` before any answer was read; MC3 checks it at `--run`).

| Rule | Sub-panel | Motivation in the program's own records | Applies to (brands kept) |
|---|---|---|---|
| R0 CANONICAL | the locked registry | as published | all |
| R1 DROP_DEFUNCT | remove Cell D_Defunct | v0.22 built a dedicated phantom cell of brands closed 2001–2010 (`prereg/v0_22_automotive_content.py` `REGISTRY`, lines 143–148 comments) | v0.22 (19) |
| R2 DROP_COI_FLAGGED | remove Denon | the AKG → Denon substitution and the Nov 10 Denon/Harman correction (Declarations) | v0.19 (15) |
| R3 DROP_CROSS_CULTURAL | remove brands flagged cross-cultural | v0.19 DEVIATIONS rule 6 (`thresholds_v0_19.json` `deviations_rules.rule_6_cross_cultural_robustness_required`; `cross_cultural_robustness.exclusion_brands` = Stax, HiFiMan) | v0.19 (14) |
| R4 DROP_BORDERLINE | remove brands flagged borderline | v0.19 `borderline_flag` (Focal, Final Audio; rule 5); v0.20 / v0.21 `borderline_classification` (4 and 6 brands); v0.18 pre-registration §1.5 (Le Labo, Frederic Malle, Byredo) | v0.19 (14), v0.20 (20), v0.21 (18), v0.18 (21) |
| R5 CASCADE_TOP5 | per cell, the first 5 brands in cascade order | v1.3/v1.4 cascade construction; C3's per-cell floor n ≥ 5 (`thresholds.n_floor_per_cell_for_C3`) | v0.19 (10), v0.20 (15), v0.21 (15), v0.22 (20; order of `REGISTRY`), v0.18 (15; cascade of v0.18 §1.4) |
| R6 LEAVE_ONE_CELL_OUT | remove one cell (one variant per cell) | the tier design itself: each cell is an author-chosen tier | v0.19 (2 × 8), v0.20, v0.21, v0.18 (3 × 16 each), v0.22 (A, B, C; D duplicates R1) |
| R7 RECOGNITION_ANCHORED | keep brands with C_P ≥ 5 | v1.3/v1.4 Phase A anchoring at the 5/6 supermajority (`papers/v1_4_methodology/v1_4_methodology_paper_draft.md` line 67) | data-dependent |
| R8 RECALL_SOURCED_XWAVE | keep brands named at least once (R_cat + R_cult ≥ 1) in the **other** wave (t1 ← t2, t2 ← t1, t3 ← t2) | panels sourced from what models name (v0.16 stage-1 suggestions, `osf/v16/data/phaseA/stage1_suggestions.json`) and Phase B attrition (v0.17, v1.4 paper line 236); the other wave avoids scoring a panel on the answers that built it | data-dependent; omnibus only (v0.18 has one wave) |
| R9 RANDOM_75 | per cell, ⌈0.75 n_cell⌉ brands at random, 500 draws, seed 630009 (one stratum for v0.23) | v0.19's 25% attrition margin (`thresholds_v0_19.json` `c1_panel_adequacy.rationale`) | all 16 substrate-waves |
| R10 RANDOM_SIZE_MATCHED | a random sub-panel of the same total size as each R1–R8 sub-panel (cells not preserved), seed 630003 | the null of H3 | as R1–R8 |
| R11 INDEPENDENT_ONLY | v0.23 brands without a conglomerate parent | v0.23 H_ConglomeratePortfolio (registry key `conglomerate`) | v0.23 (10); F4 only, descriptive |

Structural comparisons available to H1 (R1–R6, families comparable by structure, all substrate-waves): **160** (150 omnibus + 10 v0.18; `registries/panel_rules_v0_63.json` key `structural_comparisons_upper_bound_H1`). R7 adds up to 2 per substrate-wave with F1/F3 (3 with F2), R8 the same on the omnibus only; uncomparable verdicts (§6.5) remove some.

## 5. The Recognition × Recall instrument (unchanged; applied identically to every panel)

Per brand: C_P = Phase A "yes" answers (0–6); R_cat = (model, frame) cells of frames q1–q3 (EA for v0.23; the three v0.18 frames) naming the brand; R_cult = the same for q4–q6 (CC); 0 for v0.18, which has no cultural channel. Classes (thresholds of `prereg/v0_21_registry.json` key `thresholds`): Iwachu C_P ≥ 5 ∧ R_cat ≤ 2; Type 1 R_cat ≥ 5 ∧ R_cult ≤ 2; Type 2 R_cat ≤ 2 ∧ R_cult ≥ 5.

### 5.1 Substrate-level families (F1–F3), on the cells of the sub-panel

- **F1 Regime 4 routing** (v0.19–v0.22, v0.18). v1.6 Increment 1 first: if every cell has one distinct C_P value → `REGIME-4-UNAVAILABLE-AT-RECOGNITION` (`papers/v1_6/v1_6_ssrn_paper_draft.md` lines 87, 111). Else the v1.5 sequence of `scripts/score_v21.py` `resolve_h_regime4`: C1 panel n ≥ 12 (failure → INADEQUATE, §6.5); C2 per cell distinct C_P ≥ 3 ∧ modal share ≤ 0.625 — two or more failing cells FALSIFIED, one PARTIAL; IL guard (v0.20–v0.22 and v0.18, whose published design defines the same B-versus-C guard, `osf/v18/scripts/protocol/thresholds.py` `C2_IL_GRADIENT_SEPARATION_MIN`; applied when B and C are both present): top-2 R_cat share of B minus that of C ≥ 0.10, else PARTIAL; C3: cells with n ≥ 5 and Spearman ρ(C_P, R_cat) ≥ 0.50 — at least 2 → CONFIRMED, else PARTIAL. One shared rule for all four substrates (v0.19 published under its own v1.4.x rule set; open question 3).
- **F2 Type 2 emergence** (v0.20–v0.22; not defined for v0.19, whose cells are not an IL gradient, or v0.18, whose design has no cultural channel). Type 2 count in Cell B: ≥ 3 EMERGED, 1–2 PARTIAL, 0 FALSIFIED; Cell B absent or n_B < 5 → UNDETERMINED (§6.5).
- **F3 Dissociation generalisation** (v0.19–v0.22, v0.18). Cells holding an Iwachu case: ≥ 2 GENERALIZED, 1 PARTIAL, 0 NARROWED; fewer than 2 cells → undefined.

### 5.2 Brand-level regime (F4), all five substrates

v1.4's primary (recall-leaning) composite A = 0.3·R + 0.7·C with R = 1[C_P ≥ 5] and C = the recall rate, (R_cat + R_cult)/36 on the omnibus and R_cat/18 on v0.18 (v1.4 paper lines 313–323); C_P < 5 is descoped (line 317). Regime by the quartiles of A over the non-descoped brands of the sub-panel, rule of `scripts/score_v0_23.py` lines 336–356 (linear-interpolation percentiles; A ≥ q75 Dominant, ≥ q50 Established, ≥ q25 Emerging, else Absent; descoped → Absent). Fewer than 4 non-descoped brands → every regime undefined.

## 6. Hypotheses, statistics and verdict rules

Verdict vocabulary: CONFIRMED / MARGINAL / FALSIFIED / UNDETERMINED.

### 6.1 H1 (primary) — substrate-level verdict stability under the deterministic rules

Unit: a comparison = (wave, substrate, R1–R8 sub-panel, family F1–F3) whose canonical and alternative values are both comparable (§6.5). Statistic: A = share of comparisons whose alternative value equals the canonical value. Test: exact one-sided binomial test of π ≤ 0.60 (integer arithmetic, `binom_sf`).

- CONFIRMED: A ≥ 0.80 and p < 0.025.
- FALSIFIED: A < 0.60.
- MARGINAL: otherwise (0.60 ≤ A < 0.80, or A ≥ 0.80 with p ≥ 0.025).
- UNDETERMINED: fewer than 15 comparable comparisons.

Reported beside it (never changing it): A by rule, family, substrate and wave; A leaving one substrate out; the number of uncomparable comparisons by rule.

### 6.2 H2 (primary) — brand regime stability under random removal

For each substrate-wave with a defined canonical F4, 500 R9 draws; per draw, the share of kept brands (both regimes defined) whose regime equals the canonical one; s = mean over draws; **S** = mean of s over substrate-waves. Test: permutation null (seed 630002, 1,000 replicates): in each replicate the subset regimes are permuted among the kept brands of every draw; p = (1 + #{S_null ≥ S}) / (1 + 1,000).

- CONFIRMED: S ≥ 0.90 and p < 0.025. FALSIFIED: S < 0.75. MARGINAL: otherwise. UNDETERMINED: fewer than 10 substrate-waves with a defined S. (Bars aligned with H4's F4 bars on review: a fifth of the brands changing regime after a random 25% removal is not stability, and 0.90 / 0.75 already define "neutral" in H4.)

### 6.3 H3 (secondary) — purposive rules versus random removal of the same size

f_obs = 1 − A (H1's flip rate). Null: 2,000 Monte Carlo replicates (seed 630003); in each, every R1–R8 sub-panel is replaced by a random sub-panel of the same total size from the same substrate-wave, and the flip rate is computed over the families comparable for that sub-panel. p = (1 + #{f_null ≥ f_obs}) / (1 + replicates).

- CONFIRMED (purposive rebuilds flip more than random removal): f_obs > mean f_null and p < 0.05. MARGINAL: f_obs > mean f_null and p ≥ 0.05. FALSIFIED: f_obs ≤ mean f_null. UNDETERMINED: as H1.

### 6.4 H4 (secondary) — disclosed panel-handling choices are verdict-neutral

Rules R1, R2, R3 (pooled; each also reported alone). Flips = comparable F1–F3 comparisons that change; F4 agreement = share of kept brands keeping their regime.

- CONFIRMED: 0 flips and F4 agreement ≥ 0.90. FALSIFIED: ≥ 2 flips or F4 agreement < 0.75. MARGINAL: otherwise. UNDETERMINED: no comparable comparison and no defined F4.

### 6.5 Undefined statistics (fixed here)

Not comparable, so outside every denominator and counted separately: F1 or F3 on a sub-panel with fewer than 2 cells (undefined); F1 resolved at C1 (n < 12, INADEQUATE: a too-small panel says nothing about stability); F2 with Cell B absent or n_B < 5 (UNDETERMINED); a canonical value that is itself one of these. A Spearman ρ on a constant vector or n < 2 is undefined and fails C3 for that cell (as `score_v21.py`). F4 is undefined for a brand with fewer than 4 non-descoped brands in the panel. An empty sub-panel is not a comparison. Ties: ranks are averaged (ρ); quartile ties go to the higher regime (≥).

### 6.6 Multiplicity

Primary family {H1, H2}: Bonferroni, α = 0.025 each. Secondary: H3 is the only secondary with a p-value (α = 0.05); H4 is a deterministic count. Descriptives and sensitivities carry no test.

### 6.7 Sensitivity S1 (COI)

H1, H2 and H4 recomputed with Denon removed from every v0.19 panel (canonical and alternative). Reported next to each verdict; never replaces it.

### 6.8 Sensitivity S2 (uncomparable outcomes as flips)

The primary H1 and H4 keep uncomparable outcomes (§6.5) out of their denominators. S2 recomputes H1 and H4 with every uncomparable outcome (INADEQUATE, UNDETERMINED, undefined) counted as a flip, under the same bars. Reported beside the verdicts, with the uncomparable counts by rule; never replaces them.

## 7. Pre-lock parity (run 2026-11-11; `prereg/parity_v0_63.json`, `passed: true`, eight checks)

Allowed before the lock: reproducing published values. Nothing else was computed.

| Check | Reference (file, key) | Expected | Reproduced |
|---|---|---|---|
| P1 C_P and per-model recall, all waves | `osf/v41/v41_three_wave_table.csv`, columns `C_P`, `k_per_model` | 336 rows | 336 / 336 rows, 672 values identical |
| P2 t1 per-brand C_P, R_cat, R_cult (v0.20–v0.22) | `osf/v2{0,1,2}/v2{0,1,2}_verdicts.json` `phase_a.per_brand.*.cp`, `phase_b.per_brand.*.r_cat` / `r_cult` | 216 values | 216 / 216 |
| P3 t1 v0.23 recall | `osf/v23/v23_verdicts.json` `brand_details[].recall_total` / `recall_ea` / `recall_cc` | 72 values | 72 / 72 |
| P4 t1 v0.19 cases | `osf/v19/scoring_output_v0_19.txt` | Iwachu ZMF Headphones 6/1, Spirit Torino 5/0, Final Audio 6/0; Type 1 Audeze 13/2, HiFiMan 12/1, Dan Clark Audio 5/0; C_P modal share A 0.500, B 0.875 | identical |
| P5 t1 published verdicts and statistics | `v20_verdicts.json`, `v21_verdicts.json`, `v22_verdicts.json`: `hypotheses.H_Regime4_*`, `H_Type2_emergence`, `H_Dissoc*_substrate_generalization`, `v1_5_c2_per_cell`, `il_gradient_guard.separation` | Regime 4 FALSIFIED / FALSIFIED / FALSIFIED; Type 2 PARTIAL (v0.20), EMERGED (v0.21); dissociation GENERALIZED × 3; IL separation 0.5862 / −0.0726 / 0.3333; every cell's distinct C_P and modal share | identical (F1 run with the v1.5 rule, without the v1.6 pre-screen, as published) |
| P6 v1.6 Increment 1 | `papers/v1_6/v1_6_ssrn_paper_draft.md` lines 136–137, 256 | v0.20 distinct (2, 3, 1), modal (0.750, 0.625, 1.000), differential; v0.21 (1, 1, 1), (1.000, 1.000, 1.000), uniform-saturation → REGIME-4-UNAVAILABLE-AT-RECOGNITION | identical |
| P7 v0.22's own pre-screen | `v22_verdicts.json` `hypotheses.H_SubstrateRecognition_PreScreen.verdict` | UNIFORM SATURATION | identical |
| P8 v0.18 per-brand values | `osf/v18/data/phase_a_results.json` `cells.*.per_brand[].c_p_score`; `osf/v18/data/phase_b_results.json` `cells.*.per_brand[].mention_count` and `per_frame_per_model` | 24 C_P, 24 mention counts, 432 frame × model codes | 480 / 480 (Recall re-detected from the raw answers) |
| P8 v0.18 published verdicts (its own rules, `osf/v18/scripts/score_v18.py`) | `osf/v18/data/verdicts/v0_18_verdict.json` `verdicts.H_Regime4_indie_fragrance` (`cell_diagnostics`, `C2_within_cell_check`, `C2_il_gradient_check`, `C3_check`, `verdict`) and `verdicts.H_Recognition_Recall_dissociation_generalization` (`cases_per_cell`, `verdict`) | n 8/8/8; top-2 share 0.4464 / 1.0 / 0.6875; Phase D ρ 0.2474 / 0.4336 / 0.6151; IL separation 0.3125; C2 cells B, C; C3 cell C; Regime 4 PARTIAL; Iwachu cases A: Comme des Garçons Parfums 5/2, Etat Libre d'Orange 6/1, Memo Paris 6/0; B: Boy Smells 5/0, D.S. & Durga 6/2, Heretic Parfum 6/0, Phlur 5/0, Snif 5/0, Vyrao 6/0; C: none; DISSOCIATION_PARTIAL | identical (values to 10 decimals) |

## 8. Manipulation checks (each failure halts `--run`)

MC1 brand-level invariance: every brand's (C_P, R_cat, R_cult, classes) is identical in every sub-panel and in R0. MC2 the parity file records a pass and is unchanged (lock manifest). MC3 the structural rule applications equal `registries/panel_rules_v0_63.json`. MC4 every substrate-wave holds exactly its registry's brands (16/24/24/24/24 omnibus, 24 for v0.18 at t1 only, no other v0.18 wave) with the registry's cells, R_cat + R_cult equals the certified per-model recall for every omnibus brand, and v0.18 has exactly 18 raw Phase B answers.

## 9. Power and sensitivity (synthetic only; `prereg/power_v0_63.json`, seed 630090)

H1 operating characteristics (1,000 simulations; 5 substrate clusters; between-substrate intra-cluster correlation icc): with 90 comparisons and icc = 0, P(CONFIRMED) = 0.570 at a true agreement of 0.80, 0.923 at 0.85, 0.999 at 0.90; P(FALSIFIED) = 0.463 at 0.60. With icc = 0.2 these are 0.548, 0.761, 0.915 and 0.471. With 135 comparisons, icc = 0: 0.554, 0.956, 1.000. H3 (exact binomial against a fixed random flip rate of 0.10, 90 comparisons): power 0.821 for a difference of 0.10, 0.978 for 0.15 (0.951 and 0.999 at 135). With 135 and 180 comparisons (the structural count is 160): P(CONFIRMED) at 0.85 is 0.956 and 0.980 (icc 0), 0.782 and 0.788 (icc 0.2); at 0.60, P(FALSIFIED) is 0.495 and 0.469 (icc 0). H2 on three synthetic score shapes (24 brands, 3 cells, 75% subsets): S = 0.887 (spread recall) and 0.823 (60% zero recall) fall in MARGINAL, 0.905 (recall near zero, varying Recognition) reaches the CONFIRMED level: at the 0.90 / 0.75 bars the H2 verdict discriminates between generic score shapes instead of passing all of them, as the earlier 0.80 bar did.

## 10. Order of operations (enforced by `osf/v63/scripts/score_v0_63.py`; see `LOCK_STEPS.md`)

`--rules` (registries only) → `--parity` (published values only) → `--power` (synthetic) → `--lock-manifest` → commit → tag → push → OSF deposit → `--write-anchor` → `--run` once. `--run` refuses unless the tag exists, the anchor file exists, every locked file matches the manifest and the parity file records a pass; a second `--run` refuses (outputs exist). Outputs: `osf/v63/outputs/v0_63_verdicts.json` and `v0_63_comparisons.csv`.

## 11. Deviations policy

`anchor/DEVIATIONS.md` opens with Entry 0 (ex ante). After the lock every change gets an entry (id, date, ex ante / ex post, what, why, effect); a hash mismatch halts; the rules, families, thresholds, seeds, draws and tests do not change; anything added later is exploratory; a FALSIFIED or UNDETERMINED verdict is published with the same prominence as a CONFIRMED one.

## 12. Limitations

Comparisons share substrates and waves, so the binomial test of H1 treats dependent comparisons as independent; the leave-one-substrate-out values and the icc = 0.2 simulations show how much that matters. Rules R1–R4 apply to one or two substrates each, so H4 rests on few comparisons. All rules are removals from probed panels; additions are impossible on the archive (§1). One model generation (the legacy six) and English only. R8 uses the other wave's answers, which share models and frames with the scored wave. v0.18 contributes one wave and one channel (no F2), so it weighs less than an omnibus substrate.

## 13. Separate proposal, outside this lock: the smallest new collection

What the archive cannot answer (§1 a, b), and v0.17's missing per-brand Recognition, need new answers. Smallest design, on the current arm with search off (Claude Opus 5.5, GPT-6 Astra, Gemini 4 Argon), five omnibus categories: (i) Phase A yes/no probes for the 112 registry brands plus up to 10 off-panel brands per category already named in the archived Phase B answers (at most 162 brands × 3 models = 486 calls, output cap 16 tokens); (ii) the six Phase B frames verbatim, 3 runs (270 calls, cap 2,048 tokens); (iii) a panel-context arm: the three category frames with the candidate list built under R0, R1/R6 and R5 (5 × 3 × 3 models × 3 runs × 3 frames = 405 calls, cap 2,048). Upper bound at the caps and the standard prices recorded in CLAUDE.md "Collection budget" (Nov 10, 2026; US$ per 1M output tokens: Opus 5.5 20, GPT-6 Astra 50, Gemini 4 Argon 10 through Nov 30): (ii) 90 calls and at most 184,320 output tokens per model → $3.69 (Opus 5.5) + $9.22 (GPT-6 Astra) + $1.84 (Gemini 4 Argon); (iii) 135 calls and at most 276,480 output tokens per model → $5.53 + $13.82 + $2.76; (i) and all inputs (at most about 0.14M input tokens) under $1: **about $38 at most**, roughly half with batch pricing (Gemini 4 Argon's price doubles from Dec 1: +$4.60), well under the $100 cap (pause at $80, stop at $100, per the budget rule). Prices to be re-read at that study's own pre-registration, which follows the 24-hour rule.

## 14. Declarations

### Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This study re-analyses archived answers against brand registries fixed in earlier phases; it performs no new brand selection, and each registry carries its source-phase conflict-of-interest handling forward (v1.10 DEVIATIONS Entry 0; v1.14 DEVIATIONS Entry 0; v0.63 DEVIATIONS Entry 0). Two items of record apply to the registries used, and a note on v0.18. (Wording copied from the latest locked pre-registration, `osf/methodology/v1_14/prereg/PRE_REGISTRATION_v1_14.md`, Declarations, lines 187–193, tag `v1.14-prereg-r2`. The two quoted records, the Denon/Harman correction with its source, and the closing sentence are verbatim; adapted to this study's design: the description of the study in this paragraph, the last sentence of the v0.19 item, and "for them" in the last sentence of the v0.22 item.)

*Audiophile headphones (v0.19).* The v0.19 record states: “The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock.” (v0.19 paper, Declaration of interest; see also v0.19 pre-registration §2.3 and v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN, “HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership”, press release, Business Wire, September 23, 2025. In this study Denon remains in the canonical panel; rule R2 removes it as a pre-specified alternative panel, H4 tests whether that changes any verdict, and sensitivity S1 reports H1, H2 and H4 without Denon in any v0.19 panel.

*Automotive (v0.22).* The v0.22 record states: “Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed.” (v0.22 paper, Conflict of interest.) These are supply relationships, not ownership; no v0.22 brand is removed for them in this study.

*Indie fragrance (v0.18).* The v0.18 records contain no brand-level conflict-of-interest screen (its DEVIATIONS file has no Entry 0). Its declaration states: “The author is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS™ Presence Measurement Protocol and the work reported here are the author's independent academic research, conducted outside the scope of employment, in the author's role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System™. Samsung had no role in the design, execution, analysis, or interpretation of this work.” (v0.18 paper, Declaration of interest, `papers/v0_18/v0_18_ssrn_paper_draft.md` line 317.) The v0.18 registry is used as locked; this study makes no statement about the ownership of its brands beyond the v0.18 pre-registration's own borderline notes (§1.5).

Extraction and scoring are automated against the locked registries and this pre-registration. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

### Funding {-}

Self-funded. No external funding supported this research.

### Ethics {-}

Not applicable; no human subjects. The study analyses responses of large language models queried under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 15. Files

`prereg/PRE_REGISTRATION_v0_63.md` (this file); `prereg/LOCK_MANIFEST_v0_63.sha256`; `prereg/parity_v0_63.json`; `prereg/power_v0_63.json`; `registries/panel_rules_v0_63.json`; `anchor/DEVIATIONS.md`; `LOCK_STEPS.md`; `README.md`; `scripts/score_v0_63.py` and `scripts/test_score_v0_63.py` (30 tests on synthetic data and the registries); pinned and unchanged: the six registries, the certified loader and the modules it imports, the parity references, the 30 omnibus answer files, the two v0.18 answer files, its verdict file, parser, alias map and pre-registration (all in the lock manifest).

## 16. Choices made in drafting, and the coordinator's decisions on the r1 draft (review of commit `986dedd`)

1. One shared verdict rule (v1.5 C2 + v1.6 pre-screen, `v0_21_registry.json` thresholds) for all substrates and waves, rather than each phase's own published rule set (v0.19 used a 0.50 modal-share rule and a different matrix; v0.22 a modal-C_P pre-screen; v0.18 a top-2-share C2). The published t1 verdicts are reproduced under their own rules in §7. **Confirmed by the coordinator (recorded as decided on Nov 10).**
2. v0.17 and v0.18 as single-wave (t1) strata: **asked by the coordinator.** v0.18 is added (loader, parity P8, rules, counts, MC4, power, files). v0.17 is left out because its archive has no per-brand Recognition for 12 of its 15 panel brands (§3).
3. Uncomparable outcomes stay out of the denominators; **sensitivity S2 added at the coordinator's request** (§6.8).
4. H2 bars **changed by the coordinator** from 0.80 / 0.60 to 0.90 / 0.75, aligned with H4 (§6.2, §9).
5. R8 sources t1 from t2 and t3 from t2 (the nearer wave). **Confirmed by the coordinator (recorded as decided on Nov 10).**
6. Open: the v0.18 registry has no recorded conflict-of-interest screen, and v0.17's panel includes a brand also known for cooking appliances (Hestan; not verified against a cited source). Neither changes this study (v0.18 is used as locked; v0.17 is not analysed); both are for the coordinator to log for the program.
