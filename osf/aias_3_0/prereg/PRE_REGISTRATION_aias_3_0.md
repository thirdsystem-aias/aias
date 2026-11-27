# AIAS™ 3.0 — the Coverage release: calibration of three scores, three-score dissociation and reporting rules: pre-registration (analysis plan)

AIAS™ Measurement Program — Third System™. Pre-registration **r0b, draft for the 24-hour review** (r0 written 2026-11-26 on branch `aias-3.0-prereg`, from `aias-3.0-draft` @ `6f27101`; r0b the same day, dates only, change log at the end). To be locked at git tag `aias-3-0-prereg-r1` and deposited on OSF (`osf.io/ec6wh`, folder `aias_3_0/prereg/`, with `aias_3_0/anchor/`) **before any statistic of the release's own analyses (§4, §5) or of the quotes-normalised sensitivity (§10.2) exists.** None exists today: no release scorer has been written or run, and the counts of affected answers in §10.2 are a read-only count, not a statistic. The lock comes 24 hours after this draft reaches the pre-registrant unless he holds it (programme rule for new pre-registrations, CLAUDE.md "Current state").

**Pre-registrant:** Pablo Ulpiano González Castro

Every number below is copied from a locked or published record opened for this draft; each carries its file and commit. `[OPEN]` marks what is not known yet or needs the pre-registrant's decision (collected in §17).

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | AIAS 3.0 (release; the Coverage release) |
| PHASE_TYPE | Release synthesis of locked records plus two pre-registered re-analyses (calibration of three scores, §4; three-score dissociation, §5). **No collection, no model call, no spend** (§12). |
| Decisions of record | Pablo, Nov 9, 2026, 10:30 pm CT (CLAUDE.md, "Plan for speed"): per component, Paper A → Paper B if A passes → release (N → N+1 calibration + compact synthesis and report). Pablo, Thu Nov 12, 2026, 6:57 am (roadmap `aias_roadmap_ssot.md`, "Release names"): "AIAS 3.0 = the next part that passes its gate (Coverage first in line)"; Ranking "is reported as part of Presence". Pablo, Thu Nov 26, 2026, 6:52 am ("Ok to all"): D1 publish the 3.0 score set on the newest-models panel N3, bridged to AIAS 2.0 through v0.42; D2 no paid Coverage retest now, Coverage over time reported as a limitation; D3 register the predictive-validity leg now with its result pending; D4 the typographic-apostrophe miss handled as for t4 (locked coding primary, a pre-specified quotes-normalised sensitivity, a DEVIATIONS entry); #32b and #33 not in 3.0 ("no, later"). |
| Status | r0b draft. Not locked. Target release about Tue 2026-12-15 (Pablo, Thu 2026-11-26, 7:39 am, via the control chat; was Tue 2026-12-22 at r0) (schedule: `papers/aias_3_0/SCHEDULE_aias_3_0_release_DRAFT.md`). |
| Locks on | draft reaches the pre-registrant → 24 hours → content lock → `prereg/LOCK_MANIFEST_aias_3_0.sha256` → commit → tag `aias-3-0-prereg-r1` → push → `anchor/git_anchor_aias_3_0.json` (tag object, commit, tree, tagger date, SHA-256 of every locked file) → OSF deposit of `prereg/` and `anchor/`, SHA-256 verified. A lock in 2026 deposits to OSF `ec6wh` (CLAUDE.md, OSF upload, deposit convention from January 2027). |
| Consumes | Coverage Paper A (v1.12) and Paper B (v1.19), each as locked and scored; t4 (v0.42) for Presence and Consistency on N3; AIAS 2.0 (legacy two-score profile, for the bridge); the AIAS 6.0 Preview's locked structure tests on t4 (when its outputs exist); v0.43 (predictive validity; its §2.6 amendment rule); v0.45's t4 quotes-normalised tables (for §10.2). Each is used exactly as its own lock defines it. |
| Feeds forward | The AIAS 3.0 paper and Third System™ report (template and content on `aias-3.0-draft`, 39 placeholders, each filled from an output named here); the AIAS 4.0 release, which adds the next part that passes its gate. |

### 0.1 Locked records read for this draft (file and commit)

| Record | Commit (tag) | Files read |
|---|---|---|
| Coverage Paper A, pre-registration | `49efc47` (`v1.12-prereg-r1`) | `osf/methodology/v1_12/prereg/PRE_REGISTRATION_v1_12.md` |
| Coverage Paper A, scored once (2026-11-14) | `949be61` | `osf/methodology/v1_12/v112_verdicts.json`, `osf/methodology/v1_12/v112_unit_table.csv` (header) |
| Coverage Paper A, paper (Cheil revision, 20 pp) | `86b929a` | `papers/v1_12/v1_12_ssrn_paper_draft.md` (Declarations), `osf/methodology/v1_12/anchor/DEVIATIONS.md` |
| Coverage Paper B, pre-registration | `4bc4ce4` (`v1.19-prereg-r1`) | `osf/methodology/v1_19/prereg/PRE_REGISTRATION_v1_19.md` (headings) |
| Coverage Paper B, scored once (2026-11-14) | `6e8f157` | `osf/methodology/v1_19/outputs/v119_verdicts.json` |
| Coverage Paper B, paper (16 pp) | `b9e0d20` | `papers/v1_19/v1_19_ssrn_paper_draft.md`, `osf/methodology/v1_19/anchor/DEVIATIONS.md` |
| t4 (v0.42), scored once | `31c64c6` | `osf/v42/v42_verdicts.json`, `osf/v42/v42_brand_table.csv` (header) |
| t4 erratum, 2026-11-25 | `b3eb526` | `osf/v42/ERRATUM_2026-11-25.md` |
| t5 (v0.45) DEVIATIONS Entry 2 and t4 S-Q outputs | `47f1748` | `osf/v45/anchor/DEVIATIONS.md`, `osf/v45/sensitivity/t4_SQ/v42_verdicts_SQ.json` |
| t5 pre-registration | `f827d9d` (`v0.45-prereg-r1`) | `osf/v45/prereg/PRE_REGISTRATION_v0_45.md` (through the pre-build's source reader) |
| AIAS 2.0 outline | `f97db70` (`aias-2-0-outline-locked`) | `papers/aias_2_0/aias_2_0_synthesis_outline.md` |
| AIAS 2.0 synthesis data | `a425191` (`aias-2-0-paper-locked-r3`) | `osf/aias_2_0/aias_2_0_synthesis_data.json` |
| AIAS 6.0 Preview pre-registration | `598990b` (`aias-6-0-preview-prereg-r1`) | `osf/aias_6_0_preview/prereg/PRE_REGISTRATION_aias_6_0_preview.md` |
| Predictive validity (v0.43) | `8c96d9c` (`v0.43-prereg-r1`); Stage 1 scored `3ed9e1d` | `osf/v43/prereg/PRE_REGISTRATION_v0_43.md`; `osf/v43/v43_stage1_verdicts.json` |
| v1.9 calibration module | tag `v1.9-prereg-r1` | `osf/methodology/v1_9/prereg/v1_9_two_component_composite_content.py` (candidates, constraints, selection rule) |
| AIAS 3.0 pre-build | `6f27101` (`aias-3.0-draft`) | `papers/aias_3_0/STILL_NEEDS_aias_3_0.md`, `sources_aias3.py` (77 locked values, run on 2026-11-26), `tokens_aias3.py`, the paper template |

**Lineage.** Foundational: *AI Availability* (SSRN 6659000); framework: MSI Working Paper Report No. 26-132. Presence: protocol v1.2–v1.6, AIAS 1.0 (SSRN 6817841), construct validity v0.29 (SSRN 6870778). Consistency: v1.7 (SSRN 6878818), v1.8 (SSRN 6963359; φ), v1.9 (Third System and OSF copy; C\*, no composite), AIAS 2.0 (published 2026-11-10; Presence and Consistency side by side, no composite). Ranking: v1.10, v1.14 and v1.16 (gate MARGINAL; reported as part of Presence). Coverage: v1.12 Paper A (gate PASS) and v1.19 Paper B. The release follows the AIAS 2.0 outline (outcome-contingent wording locked before the deciding data) and the AIAS 6.0 Preview (gate reading, structure tests, deviations policy).

**Construct.** Coverage = in how many of a category's buying situations (category entry points; Romaniuk & Sharp 2016) AI answers name the brand, read against the spread that situation-blind naming with the same number of mentions would give (Cov\*, v1.12 §2.4). AIAS 3.0 asks two questions no single paper can: (i) on one panel and one week, does Coverage add information beyond Presence and Consistency **taken together**, not only pair by pair; (ii) does any combined score of the three both add information to Presence and keep each part separate (the v1.9 question, N = 2 → 3).

### 0.2 What is already known (and therefore not tested blind here)

The inputs of §4 and §5 are locked and public. The following statistics on them have been published and are **carried, not re-tested** (values from `sources_aias3.py`, run on 2026-11-26 against the commits shown):

- **Coverage Paper A gate (v1.12, `949be61`, `v112_verdicts.json`): PASS.** H1_Sep_Presence ρ_w = 0.055 (n = 51, CONFIRMED); H2_Sep_Consistency ρ_w = −0.060 (n = 47, CONFIRMED); H3_Sep_NamingRate ρ_w = 0.046 (n = 51, CONFIRMED); H4_Reliability split-half rel = 0.646 (n = 42, CONFIRMED); H7_Sep_Presence_Legacy ρ_w = −0.020; H8_Panel_Replication ρ_w = 0.853 (n = 51, CONFIRMED); H5_Sep_Ranking ρ_w = −0.063 (reported, not gating). MC_Situation: pooled mean (J_within − J_between) = 0.406. 900 of 900 calls answered. 51 of 112 brands rated on Cov\* (paper `86b929a`).
- **Coverage Paper B (v1.19, `6e8f157`, `v119_verdicts.json`):** H32_SetSampling MARGINAL (median split-half reliability over 64 balanced splits 0.459; 10th percentile 0.172; Paper A's split at the 93.75th percentile); H32_CueType CONFIRMED (1 of 7 cue types moved the order beyond the reference range); H34_Floor_Signature FALSIFIED (Cliff's δ = −0.062; 0.062 after Presence); defunct-brand occupancy 0 of 126 automotive answers; H35_IL_Coverage UNDETERMINED (26 eligible brands against a floor of 45, paper `b9e0d20`); H36_Profile_Replication FALSIFIED (mean ρ_w = −0.022, n = 44); H36_Structure "NO TYPOLOGY (profiles do not replicate); structure reported descriptively".
- **Bridge to the newest models (v0.42, `31c64c6`, `v42_verdicts.json`):** H_Gen_Presence ρ = 0.828 (unrounded 0.8284919892883065; n = 112; 95% interval 0.722 to 0.890; CONFIRMED); H_Gen_Phi ρ = 0.310 (unrounded 0.3095026294006812; n = 73; p_perm = 0.0056; MARGINAL). With the typographic quotes read as an apostrophe (`47f1748`, `osf/v45/sensitivity/t4_SQ/v42_verdicts_SQ.json`): 0.827 (unrounded 0.8273557953122223; interval 0.718 to 0.889; CONFIRMED) and 0.304 (unrounded 0.30415408165758184; p_perm = 0.0070; MARGINAL). Both verdicts unchanged (erratum `b3eb526`).
- **AIAS 2.0 (`a425191`, `aias_2_0_synthesis_data.json`):** class A; H_Dissociation_t3 ρ = 0.189 (n = 54); H_Consistency_Reliability ρ = 0.647 (n = 52); H_Presence_Score_Reliability ρ = 0.954 (n = 112); H_NoComposite_t3 ρ(A, P) = 0.969 against the K2 line 0.95.
- **Predictive validity, Stage 1 (v0.43, `3ed9e1d`, `v43_stage1_verdicts.json`):** H_Pred_Presence FALSIFIED; H_Pred_Consistency UNDETERMINED.

**Not computed by anyone, to the drafter's knowledge** (checked: no file under `osf/aias_3_0/` existed before this draft, and the pre-build's token map lists these as future inputs): the incremental separability of Cov\* from P and C\* together (§5.2), the three-score calibration table (§4), the bridge descriptives of §10.3, and every quotes-normalised statistic of v1.12 and v1.19 (§10.2). These are the release's own analyses. Because the pairwise statistics are public, §5.2 is pre-specified on public inputs rather than blind in the strict sense; the governing record of separability stays Paper A's gate, which was blind (§6).

## 1. Purpose and claims

### 1.1 What AIAS 3.0 will claim (each tied to the verdict that governs it)

- **C1 Three-score profile.** For each of the 112 omnibus brand units, AIAS 3.0 reports Presence P, Consistency C\* and Coverage Cov\* on the newest-models panel N3, in the t4 week, side by side, each with its rating rule. Governing: D1; §3.
- **C2 Coverage is a separate reading.** Cov\* is separable from Presence, from Consistency and from the brand's naming rate (governing: v1.12 GATE, PASS) and adds information beyond Presence and Consistency taken together (governing: H3_Cov_Joint, §5.2, read with the Preview's Coverage tests, §5.4). Wording: §6.
- **C3 Combined score.** Whether any combination of the three scores passes v1.9's constraints extended to three parts (§4). Governing: the calibration outcome (§4.5). Default reading if a candidate passes: reported as a candidate, not adopted (§4.6).
- **C4 Continuity with AIAS 2.0.** The published two-score series continues on N3 for Presence and partly for Consistency (governing: v0.42 H_Gen_Presence CONFIRMED, H_Gen_Phi MARGINAL; fixed sentence W2, §6.3).
- **C5 Predictive validity: registered, pending.** Coverage's predictive test is registered in v0.43's prospective stage before any of its outcome pulls (§8). Its result is not part of AIAS 3.0.

### 1.2 What AIAS 3.0 will not claim

Not stability over time for Coverage (one wave; D2; §7). Not predictive or behavioural validity for Coverage (§8). Not a typology, a phantom-brand signature or an identity-load effect for Coverage (v1.19: none found or not testable). Not panel-general (N3 only; three models, one per provider; search off). No level comparison of C\* with AIAS 2.0's published values (φ_max depends on the number of models; AIAS 2.0 outline, Claim 8 and D9). No model ranking. Not Ranking, Sentiment or Grounding as released parts (Ranking is reported within Presence; Sentiment and Grounding wait for their own releases). Not the situation-set extension #32b or the question-wording study #33 (§9).

### 1.3 Research questions

- **RQ1 (dissociation).** On N3 in the t4 week, among brands rated on all three scores, is Cov\* separable from Presence and Consistency taken together?
- **RQ2 (calibration).** Does any 0–100 combination of P, C\* and Cov\* both add information to P and keep each part separate, without crediting brands for one or two mentions (v1.9's K1–K3, extended)?
- **RQ3 (continuity, descriptive).** How do the N3 scores relate, brand by brand, to AIAS 2.0's published scores?
- **RQ4 (coding sensitivity).** Does reading the typographic apostrophe change any Coverage verdict of v1.12 or v1.19, or any statistic of this release?

## 2. Units, panel, wave and conventions

- **Units.** The 112 brand units of the five omnibus registries (v0.19 audiophile headphones 16; v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits 24 each), unchanged; Rare Beauty is two units (v0.20, v0.21), as in every source (v1.12 §2.1). No brand is added, removed or renamed. Unit key: (substrate, brand) as `v112_unit_table.csv` writes it.
- **Panel (D1).** N3 = Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`), Gemini 4 Argon (`gemini-4-argon`) (v1.12 §2.2; `v42_verdicts.json` `verdicts.H_Gen_Presence.models`, `31c64c6`). The continuity panel C3 (Claude Opus 5.5 in place of Claude Fable 5.2) enters only sensitivity SD (§10.1).
- **Wave.** "The t4 week": t4 (v0.42) category and brand answers and v1.12's own Coverage collection on the same models (window from 2026-11-14 00:00 UTC, v1.12 §6.7), treated as one wave, as in the Preview (§2 there). Condition: search off (S0).
- **ρ_w.** Pooled within-category Spearman with ranks centred on each category's mean rank (v1.12 §2.5), computed by the function v1.12's scorer uses (`osf/methodology/v1_12/scripts/score_v1_12.py` at `949be61`, imported unchanged and blob-checked against `prereg/LOCK_MANIFEST_v1_12.sha256` at tag `v1.12-prereg-r1`). A category enters a statistic only with ≥ 5 units in that comparison. Values compared unrounded.
- **n floor.** UNDETERMINED with fewer than 30 units pooled or fewer than 3 categories entering (v1.12 §2.5).
- **Separability bands (the programme's).** |ρ_w| ≤ 0.30 CONFIRMED; |ρ_w| ≥ 0.50 FALSIFIED; MARGINAL between (v1.12 §3).
- **Permutation p.** The first-named variable permuted within category, 10,000 draws, p = (1 + hits) / 10,001; two-sided for pairwise separability, one-sided (on R²) for the joint test. **Bootstrap:** units resampled within category, 10,000 resamples, percentile 95% interval; reported, never a verdict input.
- **Seeds.** 330001 (H3_Cov_Joint), 330002 (H3_Cov_P_U3), 330003 (H3_Cov_C_U3), 330004 (D_PC_U3), 330010 (calibration bootstrap), 330020 (dissociation bootstrap), 330021 (bridge bootstrap, D3), 330030–330036 (sensitivities, in the order of §10.1). No number from 330000 to 330099 appears on branches `aias-3.0-draft`, `v1.12`, `v0.45` or at tag `aias-6-0-preview-prereg-r1` (checked with `git grep` on 2026-11-26).
- **Orientation.** Higher P = named more; higher C\* = models agree more; higher Cov\* = named across more situations than its naming rate implies (50 = situation-blind). Separability verdicts use |ρ_w| and R_adj; signs are reported.

## 3. The three scores (read, not recomputed, except as parity checks)

| Score | Definition (locked) | Rated | Read from |
|---|---|---|---|
| **P** (P_N3) | 100 · (C_P/3 + 2 · π̂_N3,S0) / 3; C_P/3 = share of N3 models coding the brand "recognized" in their one S0 brand answer; π̂ = v0.42's recall Presence on N3, S0 (v1.12 §2.6) | every unit with a coded brand answer | `v112_unit_table.csv` column `P_comparator` at `949be61` (written from t4, `comparator_source` = "t4 (v0.42, N3, S0)") |
| **C\*** (C\*_N3) | 100 · (1 − φ_N3,S0 / 9) when v0.42's partition is `defined`; 100 when `saturated`; NOT RATED when `zero` or `undefined`; rated only with ≥ 6 N3 S0 recall mentions; 9 = φ_max for 6 frames and 3 models (v1.12 §2.6; v1.9 rule) | as defined | column `C_star_comparator` at `949be61` |
| **Cov\*** (Cov\*_N3) | 50 · (1 + mean over models with n_{b,m} ≥ 1 of β_{b,m}); β against the exact situation-blind (Rasch-type) null (v1.12 §2.4) | n_b ≥ 14 mentions and ≥ 2 of 3 models naming the brand (v1.12 §2.4) | columns `cov_star`, `rated` at `949be61` (51 of 112 rated) |

**Parity (MQ_Parity, §11).** Before any release statistic: P_comparator and C_star_comparator are recomputed from v0.42's files at `31c64c6` (brand table, coded Phase A tables) with the comparator function of `score_v1_12.py`, imported unchanged; Cov\* and its rated flag are recomputed from `osf/methodology/v1_12/data/coded/v112_mentions.csv` at `949be61` with v1.12's scorer functions; and ρ_w(Cov\*, P) and ρ_w(Cov\*, C\*) on v1.12's own unit sets must equal v1.12's H1 and H2 values within 10⁻⁹. Any difference halts the run and is logged in `anchor/DEVIATIONS.md` before anything else.

**C\* on N3 (D9 of the AIAS 2.0 outline).** AIAS 2.0's outline required C\* to be "recalibrated on the new reference panel before any post-legacy comparison". AIAS 3.0 keeps v1.9's rule (rated at ≥ 6 mentions) with the three-model φ_max = 9, and treats this as that recalibration only in two respects, both pre-specified: (a) its separation from Presence on N3 is tested (the Preview's H_PC_N3, carried, §5.4; the release's D_PC_U3 beside it); (b) only rank statistics bridge it to AIAS 2.0 (§10.3). No level of C\* is compared across panels.

## 4. Calibration of three scores (the N → N+1 step; v1.9's approach extended)

### 4.1 Status of this analysis

As v1.9 Stage 1 was for two scores, the calibration is a **declared calibration, not a hypothesis test**: its inputs are public, its candidates and constraints are fixed here, and its result decides how AIAS 3.0 reports the three scores. It is run once (`score_aias_3_0.py --calibration`), after the lock.

### 4.2 Coverage's scale and rating rule (CAL_RULE)

**Cov\* keeps v1.12's locked definition, scale (50 = situation-blind) and rating floor (n_b ≥ 14 and ≥ 2 of 3 models).** The release does not re-select the floor: v1.12 already published Cov\* at floors 6 and 28 (its sensitivity S2) and the mid-p variant (S8), so a choice among them now would not be blind. `selected.rule` = "Cov\* (v1.12 §2.4), floor 14, ≥ 2 models"; `selected.share_rated_112` = rated units / 112 (expected 51/112 from `v112_unit_table.csv` at `949be61`; the parity run confirms it). The floors 6 and 28 and Cov\*_mid are printed beside it, descriptive.

### 4.3 Candidates (eight; all computed, none dropped)

P and C\* enter as locked (§3). Three binary choices give 2 × 2 × 2 = 8 candidate combined scores, the size of v1.9's grid:

- **Coverage statistic:** Cov\* (v1.12 §2.4) or Cov\*_mid (v1.12 S8; column `cov_star_mid_S8`).
- **Low-count rule for Coverage:** FLOOR (Cov\* as rated in §3; NOT RATED below the floor) or SHRINK (Cov\*_shr = w · Cov\*_u + (1 − w) · 50 with w = n_b / (n_b + κ), κ = 14, the floor's own count; Cov\*_u = the §2.4 formula without the floor, computed by v1.12's scorer functions imported unchanged; defined for every unit with n_b ≥ 1 and ≥ 1 model naming it; 50 = situation-blind, no information). This mirrors v1.9's SHRINK (κ = one model's frame set, C_0 = scale midpoint).
- **Composite form:** ADD3: A = mean of the rated scores among P, C\*, Cov\* (P always present; a part not rated drops out of the mean; v1.9's ADD with its fallback). MOD3: A = P · (0.5 + 0.5 · C\*/100) · (0.5 + 0.5 · Cov\*/100), with a factor of 0.5 for a part not rated (v1.9's MOD extended: a brand cannot score on Consistency or Coverage alone).

C\* keeps v1.9's FLOOR in every candidate (the locked Consistency score). `candidates` = 8 (CAL_N_CANDIDATES).

### 4.4 Constraints (every candidate must pass all three)

- **K1_3 (separation).** |ρ_w(Cov\*_cand, P)| ≤ 0.50 **and** |ρ_w(Cov\*_cand, C\*)| ≤ 0.50, on the units where both members are rated (v1.9's K1 line, 0.50, applied to the new part; C\*'s own K1 is carried from the Preview's H_PC_N3 when it exists, else recomputed here as descriptive D_PC_U3). Under SHRINK, Cov\*_shr is rated wherever it is defined.
- **K2_3 (adds information).** |ρ_w(A, P)| ≤ 0.95 over all 112 units (v1.9's K2 line).
- **K3_3 (no windfall).** mean A over units with 1–2 N3 S0 recall mentions (`t4_mentions_N3_S0`) − mean A over units with none ≤ [the same difference in P] + 5 points (v1.9's K3).

### 4.5 Selection and outcome (CAL_COMPOSITE_SENTENCE, CAL_RHO_AP)

v1.9 selected by test-retest reliability. Coverage has one wave (D2), so the release substitutes the only reliability its data allow: **split-half reliability of A over the two locked halves of the situations** (v1.12 §2.3, halves A and B of 7 CEPs; A recomputed with Cov\* from each half, the per-half floor 7 of v1.12 H4 under FLOOR, κ = 7 under SHRINK; ρ_w(A_halfA, A_halfB) over all 112 units, Spearman–Brown stepped up as in v1.12 H4). Among candidates passing K1_3–K3_3, the one with the highest stepped-up reliability is selected; candidates within 0.01 of the best are tied, and ties go to the simpler choice in this order: Cov\* over Cov\*_mid, FLOOR over SHRINK, ADD3 over MOD3.

- **No candidate passes K1_3–K3_3 → NO COMPOSITE.** AIAS 3.0 reports three scores side by side (the AIAS 2.0 form). `composite.verdict` = NO COMPOSITE; `composite.best.rho_A_P` = the smallest |ρ_w(A, P)| among the eight (reported, with its candidate).
- **One or more candidates pass → CANDIDATE COMPOSITE.** The selected candidate is reported with its full table; under the default of §4.6 it is **not adopted** in AIAS 3.0.

The full 8-row table (each candidate, each constraint, the half-split reliability) is written to `osf/aias_3_0/outputs/aias_3_0_calibration.json` and printed in the paper whatever the outcome.

### 4.6 Why a passing candidate is not adopted in 3.0 (default; §17, choice 2)

v1.9 adopted nothing without a blind confirmation wave (t3). Coverage has no second wave and none is planned in this release (D2; t5 carries "no Coverage block", `osf/v45/prereg/PRE_REGISTRATION_v0_45.md` at `f827d9d`), and AIAS 2.0's descriptive check at t3 already showed the floored two-part composite ranking brands as Presence does (ρ(A, P) = 0.969 against 0.95). A passing candidate is therefore published as a candidate, named, with the statement that it is not adopted until a wave that re-measures Coverage confirms it under its own pre-registration.

## 5. Three scores on the same brands (dissociation)

### 5.1 Unit sets

- **U3 (complete-profile set):** units with P defined, C\* rated and Cov\* rated. This is the set of v1.12's H2_Sep_Consistency if P is defined for each of them; expected n = 47 (`v112_verdicts.json`, `legs.H2_Sep_Consistency.n`, `949be61`). The parity run reports the actual n.
- **Pairwise sets:** as v1.12 (H1: Cov\* rated, n = 51; H2: both rated, n = 47).

### 5.2 H3_Cov_Joint — PRIMARY (the release's own test)

**Statement.** Coverage adds information beyond Presence and Consistency taken together.

**Statistic (the Preview's I-test, §6.3 there, with j = 2).** On U3: within each category with ≥ 5 units in U3, the ranks of Cov\*, P and C\* are recomputed within U3 and centred on the category's mean rank; c = categories entering, n = units entering. The centred ranks of Cov\* are regressed by least squares on the centred ranks of P and C\* (no intercept). R² = 1 − SSR/SST; **R²_adj = 1 − (1 − R²) · (n − c) / (n − c − 2)**; **R_adj = √max(0, R²_adj)**. One-sided permutation p on R² (Cov\* ranks permuted within category; 10,000 draws; seed 330001), reported.

**Verdict.** CONFIRMED iff R_adj ≤ 0.30; FALSIFIED iff R_adj ≥ 0.50; MARGINAL otherwise; UNDETERMINED below the n floor (§2). (`joint.statistic` = R_adj; `joint.n` = n; DIS_JOINT, DIS_N.)

**Precision.** A synthetic-only note (`prereg/precision_aias_3_0.json`, written by `prereg/precision_aias_3_0.py`: the Preview's generator at tag `aias-6-0-preview-prereg-r1`, method unchanged, with j = 2, five categories, 4,000 replications per cell, seed 330040; no program data) gives, with no true overlap and these bands (0.30/0.50), CONFIRMED with probability 0.912 at n = 40 and 0.945 at n = 47, and FALSIFIED with probability 0.002 and 0.0003. The json also holds true R² = 0.04, 0.09, 0.25 and 0.49 and the 0.50/0.70 bands.

### 5.3 Pairwise rows on U3 — SECONDARY (they never set the class alone)

- **H3_Cov_P_U3:** ρ_w(Cov\*, P) on U3; seed 330002; bands of §2.
- **H3_Cov_C_U3:** ρ_w(Cov\*, C\*) on U3; seed 330003. If U3 equals v1.12's H2 set, this equals v1.12's H2 value (MQ_Parity) and is carried, not re-tested.
- **D_PC_U3 (descriptive):** ρ_w(P, C\*) on U3; seed 330004.

(`pairs.P_Cov.rho`, `pairs.C_Cov.rho` = DIS_RHO_P_COV, DIS_RHO_C_COV.)

### 5.4 The Preview's locked Coverage tests (carried, when they exist)

The AIAS 6.0 Preview (tag `aias-6-0-preview-prereg-r1`, locked 2026-11-11, before any t4 score) locks, on t4: the S-tests P × Cov\* (seed 600007, carried from v1.12 H1), C\* × Cov\* (600008, carried from v1.12 H2), R\* × Cov\*, S × Cov\*, Cov\* × G\*; the I-test of Cov\* on every earlier member of its included set K (seed 600024); Cov\*'s component status (DISTINCT, PARTLY DISTINCT, NOT DISTINCT, UNDETERMINED); and H_PC_N3 (P × C\* on N3, seed 600001). AIAS 3.0 reads these from `osf/aias_6_0_preview/outputs/results_aias_6_0_preview.json` as issued (primary coding) if they exist at the release's data lock (Preview data lock the day v1.14 Stage 2 exists, expected about Fri 2026-12-04 to Sat 12/5; public about Thu 2026-12-10, as soon as it is ready; Pablo, Thu 2026-11-26, 7:13 am and 7:39 am, via the control chat; r0 had data lock Fri 12/11 and public Tue 12/15 from STILL_NEEDS at `6f27101`), and prints them beside §5.2–5.3 (DIS_PREVIEW_SENTENCE). They are the Preview's verdicts, not the release's; they enter the class only as in §6.2. If they do not exist by the release's data lock, the release proceeds without them and adds them by a dated addendum before the paper lock (§11.4).

### 5.5 DIS_VERDICT

`verdicts.H3_Cov_Joint` (the word as the scorer writes it), printed with H3_Cov_P_U3, H3_Cov_C_U3, D_PC_U3 and the Preview's Coverage status where it exists.

## 6. Outcome-contingent wording (locked before the release's analyses; the AIAS 2.0 outline's §5 form)

### 6.1 Governing verdicts

- **G1 Coverage Paper A GATE** (v1.12): PASS, fixed (2026-11-14, `949be61`). It is the governing record of pairwise separability and is not re-opened.
- **G2 H3_Cov_Joint** (§5.2), the release's own test.
- **G3 the Preview's Cov\* status** (§5.4), when it exists at the data lock.
- **G4 the calibration outcome** (§4.5), which sets the composite sentence (W1) but not the class.

### 6.2 Classes (CLASS, HEADLINE, REPORT_HEADLINE)

The class is computed mechanically at the data lock from G2 and G3. Where G3 does not exist, it is read as "not issued" and the class rests on G2; a later G3 can only move the class by the addendum rule (§11.4).

| Class | Condition | HEADLINE (paper) | REPORT_HEADLINE (report; managerial register) | What changes |
|---|---|---|---|---|
| **A** | G2 CONFIRMED, and G3 DISTINCT or not issued | "On the newest models, AI Availability is measured on three separable components — Presence, Consistency and Coverage — reported side by side, from one week of answers." | "Being named, being named evenly across AI models, and being named across buying situations are three different readings of a brand." | full claim set |
| **B** | G2 MARGINAL, or G3 PARTLY DISTINCT (and neither of C's conditions) | "On the newest models, AI Availability is measured on three components; Coverage is separable from Presence and Consistency pair by pair and partly separable from the two together (R_adj = …), from one week of answers." | "Coverage adds a third reading of a brand, with some overlap with the other two." | the overlap and its size are printed in the abstract; Claim 3 carries "partly" |
| **C** | G2 FALSIFIED, or G3 NOT DISTINCT | none: **drafting pauses** | none | Claude writes a one-page options memo (for example: release Coverage with the overlap stated, hold 3.0 for a second Coverage wave, or return Cov\* to redesign); a change of direction, so Pablo decides |
| **U** | G2 UNDETERMINED (n or category floor), and G3 not NOT DISTINCT | "On the newest models, AI Availability is measured on three components; Coverage is separable from Presence and Consistency pair by pair, and whether it adds to the two together could not be determined: [cause]." | "Coverage adds a third reading of a brand; how far it overlaps the other two together is not yet known." | Claim 3 rests on Paper A alone, stated so |

If G2 and G3 disagree by more than one step (for example G2 CONFIRMED and G3 NOT DISTINCT), the class follows the less favourable of the two and the paper states both, with the reason the Preview's I-test differs (its predecessor set includes every included part before Coverage, §5.4).

### 6.3 Rules in every class

- **W1 Composite sentence (CAL_COMPOSITE_SENTENCE).** NO COMPOSITE: "No combination of the three scores both adds information to Presence and keeps each part separate, so AIAS 3.0 reports three scores side by side." CANDIDATE COMPOSITE: "One combined score ([candidate]) passed the calibration's constraints on one week of answers; it is reported as a candidate and is not adopted until a wave that re-measures Coverage confirms it." Either way the best |ρ_w(A, P)| is printed against 0.95 and AIAS 2.0's 0.969.
- **W2 Bridge sentence (CAL_BRIDGE_SENTENCE), fixed now because its governing verdicts exist.** "AIAS 3.0 publishes its scores on the newest-models panel. On it, Presence keeps the brand order of AIAS 2.0's panel (ρ = 0.828, n = 112; 0.827 with the apostrophe correction), and Consistency keeps it only partly (ρ = 0.310, n = 73; 0.304 corrected); Consistency levels are not comparable with AIAS 2.0's published values, because the scale's maximum depends on the number of models." Sources: `31c64c6` `osf/v42/v42_verdicts.json` (H_Gen_Presence, H_Gen_Phi); `47f1748` `osf/v45/sensitivity/t4_SQ/v42_verdicts_SQ.json`. The bridge descriptives of §10.3 are printed beside it and never change it.
- **W3 Coverage over time (RETEST_SENTENCE), fixed (D2).** "Coverage has been measured in one week of answers (November 2026). Whether a brand's Coverage holds over time has not been tested: the three-week repeat wave carries no Coverage block, and no Coverage retest is part of this release." RETEST_RHO, RETEST_N and RETEST_DAYS are not filled; the template's sentences that use them are replaced by W3 at the build (a build-file change, recorded in the data lock).
- **W4 Predictive validity (PRED_SENTENCE), fixed (D3).** "Coverage's predictive test, against the later change in US search interest, is registered in the programme's prospective predictive-validity study (v0.43, amendment deposited [PRED_AMENDMENT_DATE]); its result is due no earlier than 12 March 2027 and is not part of this release."
- **W5 Coding sensitivity (APOS_SENTENCE).** From §10.2: if no label changes: "Reading the typographic apostrophe in two brand names (a pre-specified sensitivity analysis) changes no Coverage verdict and no verdict of this release." Otherwise every test whose label differs is called "coding-sensitive" in the results and the abstract, with both labels. The number of Coverage answers affected is printed (§10.2).
- **W6 Reliability.** Every sentence on Cov\*'s reliability carries Paper B's result: reliability across samples of situations was marginal (median split-half 0.459 over 64 splits; H32_SetSampling MARGINAL, `6e8f157`).
- **W7 Status words.** Coverage is a "released component" in AIAS 3.0. It is never called "validated": its stability over time and its predictive validity are untested (W3, W4).
- **W8 No unregistered statistic in a confirmatory sentence.** Anything not pre-registered here or in the carried records is labelled exploratory and listed in the data lock before it is computed (AIAS 2.0 outline, rule R7; Preview W5).
- **W9 Sensitivities and descriptives never change the class** (§10).

## 7. Coverage over time (not measured in this release; D2)

No paid Coverage retest is part of AIAS 3.0. Nothing in the programme measures Cov\* over time today: t5 carries "no Coverage block" (`osf/v45/prereg/PRE_REGISTRATION_v0_45.md`, `f827d9d`), v1.19 did not re-ask, and t6 (target 2027-02-12, same file) repeats t4's design. Coverage over time is therefore a stated limitation (§13, item 1) and the fixed sentence W3. A later Coverage retest would be a new paid collection with its own pre-registration and the pre-registrant's go; it is not drafted here.

## 8. Predictive validity: the Coverage leg, registered now, result pending (D3)

### 8.1 Rule used

v0.43 §2.6 (tag `v0.43-prereg-r1`, `8c96d9c`): "Each component's predictive hypothesis is added to Stage 2 by a dated amendment to this pre-registration, deposited on OSF before the first Stage 2 outcome pull (§4.5), with this section's outcome, windows, statistic and verdict rule unchanged and Z = {L, P_new}. A component that failed its Paper A separability gate is not added." Coverage passed (G1). The amendment text is Appendix A; it is a v0.43 document, deposited to `v43/prereg/`, and is listed here so that AIAS 3.0 ships with the leg registered.

### 8.2 The hypothesis (summary; Appendix A governs)

- **H_Pred_Coverage_Confirm.** Among brands of the same category, the same November search level and the same newest-models Presence, those with higher Coverage in the t4 week gain more US search interest by March 2027.
- **Operationalisation.** X = Cov\* (v1.12, N3, S0, rated units; `v112_unit_table.csv` at `949be61`); Y = the change from W(2026-11-07) to W(2027-03-06) (v0.43 §2.4); Z = {L at W(2026-11-07), P_new at t4} (v0.43 §2.1, §2.6); ρ_pw|Z, one-sided permutation p (seed 430051; v0.43 uses 430041–430050, and 430051 does not occur in `osf/v43` on branch `v0.43`, checked 2026-11-26); bootstrap intervals as v0.43 §2.1.
- **Verdict rule (v0.43 §2.1, unchanged).** CONFIRMED if ρ_pw|Z ≥ 0.15 and p < 0.05; FALSIFIED if the upper end of the 90% bootstrap interval is below 0.10; MARGINAL if ρ_pw|Z > 0 and p < 0.10 and neither of the above; UNDETERMINED otherwise; REVERSED added when ρ < 0 with two-sided p < 0.05. **Minimum n:** 30 units with a defined outcome, the floor v0.43 sets for its rated-only (Consistency) tests, because Cov\* is rated for 51 of 112 units `[§17, choice 5]`.
- **Outcome data.** v0.43's own Stage 2 pulls: three pulls at least 24 hours apart, the first no earlier than Wednesday 2027-03-10 (v0.43 §4.5). No new request is added by this amendment. Result: not before Fri 2027-03-12 (the third pull at the earliest).
- **Reported beside it (never a verdict input):** the same test with Cov\* from the quotes-normalised coding (§10.2) and P_new from v0.45's t4 S-Q tables; the per-substrate values (v0.43 §2.8 item 1).
- **Where the result is reported.** v0.43's Stage 2 report, and the first AIAS release after it `[OPEN: AIAS 4.0 or 5.0, by date]`. It is never added to AIAS 3.0's paper after the paper lock.

### 8.3 Sales rank

Not registered here. Amazon sales rank comes only from a licensed source and never from scripted browsing of Amazon (CLAUDE.md, "Amazon data"; v0.43 §4.6). The plan of record is one licensed Keepa month in March 2027; **Keepa spending and its account need the pre-registrant's separate go**. If he gives it, a separate dated amendment to v0.43 (its own hypotheses, outcome definition, brand-to-product mapping, the categories with Amazon listings `[OPEN]`, cost under the $100 rule) is deposited before the Keepa pull. AIAS 3.0 says only that the sales-rank leg is planned and not registered.

## 9. Scope and exclusions

- **Not in AIAS 3.0 (pre-registrant, 2026-11-26, "no, later"):** #32b, the parallel situation set written independently with buyer weights, and #33, stability across question wording. Each needs a new paid collection and its own pre-registration (v1.19 §3.3 and §4). The paper names them as future research only.
- **Not in AIAS 3.0 (D2):** a Coverage retest wave (§7).
- **Not tested:** the identity-load moderator of Coverage (v1.19 H35_IL_Coverage UNDETERMINED: 26 eligible brands against a floor of 45); it is carried as UNDETERMINED.
- **Data.** Only the 112 omnibus units on N3 in the t4 week, the AIAS 2.0 legacy profiles for the bridge descriptives (§10.3), and the Preview's Coverage rows (§5.4). Not used: the continuity panel C3 and the four-model panel A4 except in sensitivity SD; search-on answers (Coverage was collected search off; search-on Coverage belongs with Grounding); Ranking, Sentiment and Grounding scores (other releases; the Preview prints them); any category study outside the five omnibus registries.
- **Units.** None excluded from the primary analysis. A unit a score does not rate leaves every statistic involving that score; nothing is imputed. The COI-flagged units stay in (Declarations) and every statistic is also reported without them (SA, S-COI).
- **Calls and models.** Each source's exclusions as that source locked them (v1.12 §7.3 drop rule: no model was dropped, 900 of 900 calls answered; v0.42's drop rule). The release re-decides none.

## 10. Sensitivities, the coding sensitivity S-Q, and descriptives

### 10.1 Sensitivities (reported beside every verdict; never change one; every label change is listed)

SA without the Denon unit (v0.19). S-COI without the six COI-flagged units (Declarations; as v1.19's S-COI; v1.12 reported its gate without Denon as S10). SB uncentred pooled ranks (v1.12 S9 convention). SC leave one category out (range of H3_Cov_Joint, the pairwise rows and the calibration's constraints). SD Cov\* from the continuity panel C3 (`cov_star_C3`) in place of Cov\*_N3, comparators unchanged. SE Cov\*_mid (`cov_star_mid_S8`) in place of Cov\*. SF Cov\* floors 6 and 28 (v1.12 S2). Seeds 330030–330036 in this order. S-Q (§10.2) is reported beside every one of them as well.

### 10.2 S-Q: the typographic apostrophe, quotes normalised (D4)

**What was found** (read-only; no statistic computed). v1.12 codes its answers with v0.42's coder, unchanged (v1.12 §2.3: `osf/v42/scripts/code_t4_v0_42.py`, git blob `2d36735d512cf9e13b74010ba5a7f655fc7de0bc`, pinned and re-checked at parity gate P1). That coder matches "Paula's Choice" (v0.20) and "L'Oréal Paris" (v0.21) only with a straight apostrophe (U+0027); these are the only two registry names that contain an apostrophe, and the v0.23 matcher already accepts both forms (v0.42 erratum, `b3eb526`). A read-only count recorded on 2026-11-26 in `papers/aias_3_0/STILL_NEEDS_aias_3_0.md` (`6f27101`), on the v1.12 raw answers and mentions file: **30 Coverage answers name Paula's Choice and 10 name L'Oréal Paris only with a typographic apostrophe, all coded "not mentioned" (GPT-6 Astra 12 + 4, Gemini 4 Argon 18 + 6).** Their effect on Cov\*, the gate legs, v1.19 and this release has not been computed. v1.12's comparators P and C\* come from t4's primary coding, which the same miss affected (46 cells; erratum `b3eb526`).

**Handling (as for t4, v0.45 DEVIATIONS Entry 2, `47f1748`).** The locked coding stays primary for v1.12, v1.19 and every statistic of this release. S-Q is a pre-specified sensitivity analysis, recorded in v1.12 and v1.19 DEVIATIONS entries before it is computed (draft text: `osf/aias_3_0/drafts/DEVIATIONS_entry2_v1_12_v1_19_apostrophe_DRAFT.md`).

**Definition (exact).**
1. *Text map.* In the answer text (the raw record's `text` field) of every call in `osf/methodology/v1_12/data/v112_raw.jsonl` (`949be61`; all four models, so N3, C3 and A4 are all covered), U+2019 RIGHT SINGLE QUOTATION MARK and U+2018 LEFT SINGLE QUOTATION MARK are replaced by U+0027 APOSTROPHE. No other character changes. The wrapper first counts every other apostrophe-like character (U+02BC, U+2032, U+FF07, U+201B) in the file and reports the count; it maps none of them.
2. *Both sides of every comparison together.* The comparators come from t4's existing S-Q tables (`47f1748`: `osf/v45/sensitivity/t4_SQ/v42_brand_table_SQ.csv`, SHA-256 `de8559cbe21db91e8922337c7ab5bdfaa7d1d2325f6bbe0870e6abcd812a5c4d`, and the S-Q coded tables in `t4_SQ/coded/`), read, not re-made; recognition (Phase A) codes are unchanged, as at t4. Mapping one side only would create a difference that is not in the answers (v0.45 Entry 2: on t3 → t4, mapping t3 alone moves H_Gen_Phi to 0.2960, mapping both gives 0.3056). H7's legacy comparator (AIAS 2.0's published t3 Presence) is kept as published, because no S-Q table of t3 is locked; this is stated beside H7.
3. *Coding.* v0.42's coder, imported unchanged and blob-checked against `2d36735d…`, codes the mapped text exactly as v1.12's primary run did.
4. *Scoring.* `score_v1_12.py` (`949be61`, blob-checked against v1.12's lock manifest), unchanged, with its seeds (112001–112008, 112020) and settings, on the S-Q tables: MC_Situation, H1–H8, the GATE, raw coverage and the descriptives. v1.12's H5 reads Ranking R\* as published (not re-coded) `[OPEN: whether v1.14's position extractor shares the miss is checked read-only by the wrapper and reported]`. Then `score_v1_19.py` (`6e8f157`), unchanged, on the S-Q tables of v1.12: every v1.19 hypothesis (H32_SetSampling, H32_CueType, H34_Floor_Signature, H34_Floor_BeyondPresence, H34_Defunct_Occupancy, H35_IL_Coverage, H35_IL_Robust, H35_IL_CueType, H36_Profile_Replication, H36_Structure). Then every statistic of §4 and §5 of this release on the S-Q inputs, in the same run as the primary.
5. *Reproduction first.* Before writing anything, the wrapper re-codes v1.12 with the locked coder and re-scores it with the locked scorers; it writes nothing unless 0 cells of the coded tables and 0 leaves of `v112_verdicts.json` and `v119_verdicts.json` differ from the published files (as v0.45's `--t4-correction` did for t4).
6. *When.* Once, after this pre-registration is locked and the DEVIATIONS entries are committed; the wrapper refuses to overwrite its outputs. Outputs: `osf/methodology/v1_12/sensitivity/` (coded S-Q tables, `v112_verdicts_SQ.json`, `v119_verdicts_SQ.json`, a cell-by-cell flips file by substrate, brand, model, panel, CEP and run, and the count of answers holding U+2019 or U+2018).
7. *Reporting.* Beside each v1.12, v1.19 and release statistic: the S-Q value, its label and whether the label is the same. A changed label is "coding-sensitive" (W5). S-Q never replaces a primary verdict, never changes the class, and never re-opens v1.12's GATE.

### 10.3 Descriptives (no verdicts)

D1 the per-unit profile (P, C\*, Cov\*, rated flags, labels; CSV). D2 rated counts per category and by within-category Presence tercile; the share of U3 among the 112 (every floor requires naming, so U3 leans to well-named brands). D3 bridge to AIAS 2.0 on units with both: ρ_w(P_AIAS2.0,t3, P_N3) with the mean level shift of P and its bootstrap interval (seed 330021), and ρ_w(C\*_AIAS2.0,t3, C\*_N3) without a level comparison; legacy values from `osf/aias_2_0/aias_2_0_profiles.csv` at tag `aias-2-0-data-locked` (`94f6618`) and `P_t3_legacy` in `v112_unit_table.csv`. D4 the joint distribution of the three scores on U3, by category. D5 the calibration table (§4.5).

## 11. Order of operations and checks

### 11.1 Before any release statistic

1. This pre-registration is locked and anchored (§0), with the v0.43 Coverage amendment (Appendix A) deposited to `v43/prereg/` in the same session (recommended: both deposits in 2026, on OSF).
2. The v1.12 and v1.19 DEVIATIONS entries (S-Q, §10.2) are committed on their branches and appended to their OSF anchors, dated, before the S-Q wrapper runs.
3. `score_aias_3_0.py` (calibration, dissociation, sensitivities, descriptives) and the S-Q wrapper are written to this text and tested on synthetic data only (scratch directories). Scorer notes record any choice where this text is silent; none may change a test, band, floor, seed or rule. Precedent: the AIAS 2.0 outline locked before its builder existed.

### 11.2 Checks (each halts unless stated)

| Id | Check | Rule |
|---|---|---|
| MQ_Lock | the lock | tag `aias-3-0-prereg-r1` and the anchor exist; every file in the lock manifest is unchanged (`anchor/DEVIATIONS.md` may only grow; its locked text stays an unchanged prefix) |
| MQ_Blind | order | the tag's date precedes the first commit of every release output (`osf/aias_3_0/outputs/`) and of every S-Q output of v1.12 and v1.19; otherwise the affected statistics are labelled exploratory, a DEVIATIONS entry records it and Pablo is told (no halt) |
| MQ_Inputs | locked inputs | every input is read with `git show` at the commit named in §0.1 and §3 and logged with its git blob and SHA-256 in `outputs/inputs_read_aias_3_0.json`; scorer blobs are checked against their own lock manifests |
| MQ_Join | units | `v112_unit_table.csv` carries the 112 unit keys, 1:1; the AIAS 2.0 profile table joins on the same keys |
| MQ_Parity | reproduction | §3's parity: P, C\*, Cov\* and the rated flags recomputed equal the unit table; v1.12's H1 and H2 ρ_w reproduced within 10⁻⁹ |
| MQ_SQ | S-Q reproduction | §10.2 step 5 |

### 11.3 Runs (each once; each refuses to overwrite its output)

`score_aias_3_0.py --calibration` → `outputs/aias_3_0_calibration.json`; `--dissociation` → `outputs/aias_3_0_dissociation.json` (primary and S-Q in the same run). Planned before Thu 2026-12-03 (t5 collects from that day, and no heavy Mac job runs beside a locked collection), else after t5 and its judge (schedule).

### 11.4 Data lock and addenda

**Data lock** (tag `aias-3-0-data-locked`; target right after the Preview's data lock, about Sat 2026-12-05 to Sun 12/6; Pablo, Thu 2026-11-26, 7:13 am and 7:39 am, via the control chat; r0 had Sat 2026-12-12): the class (§6.2) is computed mechanically from G2 and G3 and written to the output before any chart or text is drafted. If the Preview's outputs (§5.4) do not exist at that moment, G3 is "not issued" and the Preview rows are added by a **dated addendum, only before the paper lock**: the class is recomputed by the same rule; both the original and the updated class stay on record; nothing else is redone. Nothing changes after the paper lock.

## 12. Cost

No paid model call, no new collection: spend $0; the $100 rule (CLAUDE.md, "Collection budget") is not engaged. v0.43's Stage 2 pulls are v0.43's (SerpAPI, within its free plan, v0.43 §4.7); the amendment adds no request. A Keepa month (§8.3) is outside this pre-registration and needs its own go.

## 13. Limitations

1. **One wave for Coverage.** Cov\* is measured in one week; its stability over time is untested (D2; W3).
2. **Reliability depends on the situations sampled.** Paper B's set-sampling test was MARGINAL (median split-half 0.459 over 64 splits); one set of 14 situations per category, drafted by one procedure.
3. **One panel.** N3 (three models, one per provider), provider-default settings, search off, US English, five categories, 112 units with registries fixed in May 2026; the score set moves from AIAS 2.0's retiring panel to N3, and Consistency continues the published series only partly (W2).
4. **Two collections in one "wave".** P and C\* come from t4's answers, Cov\* from v1.12's own collection on the same models in the same week.
5. **Rated subsets.** Every floor requires naming, so U3 (expected 47 units) leans to well-named brands; correlations with Presence are computed on a restricted range (D2 shows it).
6. **Public inputs.** The dissociation and calibration run on data whose pairwise statistics are published; only the joint statistic and the calibration table are new (§0.2).
7. **No behavioural validity.** Coverage's predictive test is registered and pending (§8); no sales outcome is registered (§8.3).
8. **Coding.** A coder miss on two brand names is known and handled by S-Q (§10.2); S-Q covers U+2018 and U+2019 only.
9. **Verdicts rest on effect-size bands, not p-values**, with no multiplicity correction (the programme's convention); R_adj's bands are the Preview's, calibrated on synthetic data only.
10. Separability is not validity, and the release inherits every limitation of v1.12, v1.19, v0.42 and the Preview.

## 14. Deviations policy

`anchor/DEVIATIONS.md` opens with Entry 0 (ex ante: what was read before the lock; the COI carry-forward; the anchor sequence). After the lock every change gets an entry (id, date, ex ante or ex post, what, why, effect on inference); a hash mismatch halts; a scorer fix only restores a rule as written, with results before and after; tests, bands, floors, seeds, candidates, constraints, the selection rule and the wording rules do not change; anything added later is exploratory; an unfavourable class is published with the same prominence as a favourable one. A source's own deviation is recorded in that source's file (so S-Q's entries go to v1.12 and v1.19, §10.2). Every published correction gets a corrections-log row the same day (CLAUDE.md, S&P lessons, rule 2).

## 15. Declarations

### Conflict of interest {-}

This release selects no brands and makes no collection; it reads the records of Coverage Papers A and B, whose conflict-of-interest declaration applies unchanged and is reproduced here from Paper A (Methodology v1.12, revision of November 2026; `papers/v1_12/v1_12_ssrn_paper_draft.md` at `86b929a`):

> The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. Samsung does not market brands in skincare, cosmetics, passenger cars or premium spirits. In audiophile headphones, Samsung's subsidiary Harman International owns brands in the category; v0.19 substituted Denon for AKG before its pre-registration lock because AKG's parent, Harman International, is a Samsung subsidiary. This study performs no new brand selection: it uses the registries fixed in v0.19--v0.23, and each keeps its source-phase handling. In the automotive registry, Samsung subsidiaries hold tier-2/3 component supply relationships with several registry brands --- Harman International (audio systems), Samsung SDI (battery cells) and Samsung Display (infotainment) --- characterized in the source phase as non-competitive, with no brand-level overlap, and imposing no operational restriction on registry composition (v0.22 Declarations; screened in v0.22 DEVIATIONS Entry 0, Part B). Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN press release, Business Wire, September 23, 2025. Every gate statistic is also reported without Denon (sensitivity S10). Cheil Worldwide, a marketing company of the Samsung group in which Samsung Electronics holds 28.43%, or its agency Iris has done advertising, public-relations or search-marketing work for five registry brands: Chevrolet (for GM Korea, 2017), BMW (UK consumer public relations, 2018), Bentley (experiential agency of record in the Americas from 2021), Jack Daniel's (UK digital agency from 2022, since replaced) and Eucerin (search marketing for Beiersdorf from 2024) (conflict-of-interest screen of v0.62, DEVIATIONS Entry 0, Part F). These five brands stay in every analysis as locked. The situation questions name no brand; headphone situations stay inside audiophile listening, because consumer, sport and true-wireless uses are where Samsung-owned brands compete. Brands outside the registries named in answers, which may include Samsung-owned brands, are not scored and their mentions are not counted. Acquisition, coding and scoring are automated against the locked registries, and the pre-registration was locked and deposited before any v1.12 call. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

In this release Denon and the five brands above stay in every analysis; every statistic is also reported without Denon (SA) and without all six (S-COI). All statistics are computed automatically from locked inputs under this pre-registration.

### Funding {-}

Self-funded. No external funding supported this research.

### Ethics {-}

Not applicable; no human subjects. The release analyses scores computed from responses of large language models queried under their public interfaces.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 16. Files and lock steps

**In r0 and r0b (this draft, 2026-11-26):** `osf/aias_3_0/prereg/PRE_REGISTRATION_aias_3_0.md` (this file, with Appendix A); `osf/aias_3_0/anchor/DEVIATIONS.md` (Entry 0, draft); `osf/aias_3_0/drafts/DEVIATIONS_entry2_v1_12_v1_19_apostrophe_DRAFT.md` (draft text of the v1.12 and v1.19 entries for S-Q; not a locked file of this release); `papers/aias_3_0/SCHEDULE_aias_3_0_release_DRAFT.md` (dated steps to the release; not deposited).

**At the lock:** apply the pre-registrant's choices (§17) where he departs from a default; write `prereg/LOCK_MANIFEST_aias_3_0.sha256` (this file and `anchor/DEVIATIONS.md`); commit; tag `aias-3-0-prereg-r1`; push; write `anchor/git_anchor_aias_3_0.json`; deposit `prereg/` and `anchor/` to OSF `ec6wh/aias_3_0/`, SHA-256 verified; deposit Appendix A to `v43/prereg/` as v0.43's dated amendment (its own file, `AMENDMENT_v0_43_coverage.md` `[OPEN: file name per v0.43's convention]`), SHA-256 verified. Pushes and deposits are the runner's automatic steps after the 24 hours (CLAUDE.md, operating mode); none is done in r0.

**After the lock (§11):** the S-Q DEVIATIONS entries on v1.12 and v1.19; `osf/methodology/v1_12/sensitivity/quotes_v1_12.py` and its tests; `osf/aias_3_0/scripts/score_aias_3_0.py` and its tests; outputs under `osf/aias_3_0/outputs/`.

## 17. Choices and open items for the pre-registrant (each with a default; silence = default)

1. **Lock time.** 24 hours after this draft reaches him (expected Fri 2026-11-27 morning → lock Sat 2026-11-28 morning), unless he holds it. **Default: as stated.**
2. **A passing composite.** Not adopted in 3.0, reported as a candidate (§4.6) (**default**); or adopted as provisional with "one wave" on every use.
3. **The calibration's reliability criterion.** Split-half over the two locked situation halves (**default**, §4.5); or no selection at all (report the eight rows only).
4. **Precision note for H3_Cov_Joint.** Run a synthetic-only note (j = 2, n = 40 and 47, five categories, Preview's generator and bands) before the lock and add it as `prereg/precision_aias_3_0.json` (**default**; adds about one session and moves the lock only if it is not ready by the 24 hours) or lock without it. **Done 2026-11-27 (default): `prereg/precision_aias_3_0.json`, reported in §5.2.**
5. **Minimum n of the predictive Coverage test.** 30 units, v0.43's floor for its rated-only tests (**default**); or v0.43's general floor of 60, which Cov\*'s 51 rated units cannot meet (the test would be UNDETERMINED by construction).
6. **Tier of H_Pred_Coverage_Confirm in v0.43.** SECONDARY, like H_Pred_Presence_NewPanel on the same panel (**default**); or PRIMARY.
7. **Erratum notes for v1.12 and v1.19.** For t4, a dated erratum note and a corrections-log row followed the sensitivity (Nov 25). Here the default is: decide after S-Q is computed; if any published Coverage value or brand row is wrong under S-Q, a dated OSF note beside each paper and a corrections-log row the same day (S&P rule 2), papers unchanged.

**`[OPEN]` items** (facts not yet known): the file name of the v0.43 amendment (§16); which release reports the predictive result (§8.2); the categories with Amazon listings for any Keepa amendment (§8.3); whether v1.14's position extractor shares the apostrophe miss (§10.2); whether the Preview's outputs exist by the release's data lock (§5.4, §11.4); the actual n of U3 (expected 47; §5.1).

---

## Appendix A. Draft amendment to v0.43 (§2.6): the Coverage component in Stage 2

*To be deposited as v0.43's dated amendment, with the AIAS 3.0 lock, before the first Stage 2 outcome pull (no earlier than Wed 2027-03-10). It changes no locked text of v0.43; it adds one hypothesis under §2.6's rule.*

**Amendment, dated [date of deposit]: Coverage (v1.12) added to Stage 2.** Under §2.6 ("Each component's predictive hypothesis is added to Stage 2 by a dated amendment … with this section's outcome, windows, statistic and verdict rule unchanged and Z = {L, P_new}. A component that failed its Paper A separability gate is not added."), Coverage is added: its Paper A (Methodology v1.12, tag `v1.12-prereg-r1`) returned GATE PASS on 2026-11-14 (`osf/methodology/v1_12/v112_verdicts.json`, commit `949be61`).

- **`H_Pred_Coverage_Confirm` (SECONDARY).** X = Cov\* at the t4 week (N3, search off; v1.12 §2.4; column `cov_star` of `osf/methodology/v1_12/v112_unit_table.csv` at `949be61`; rated units only); Y = the change from W(2026-11-07) to W(2027-03-06) (§2.4); Z = {L at W(2026-11-07), P_new at t4} (§2.1); ρ_pw|Z (§2.1); one-sided permutation p, 10,000 draws, seed 430051; bootstrap intervals as §2.1; verdict rule of §2.1 unchanged, including the REVERSED label; minimum n 30 units with a defined outcome (the floor §2.1 sets for the rated-only Consistency tests).
- **Reported beside it (no verdict):** per substrate (§2.8 item 1); without the five defunct automotive brands (§2.8 item 2; Cov\* rates none of them unless named); the same test with Cov\* and P_new from the quotes-normalised coding (AIAS 3.0 pre-registration §10.2; v0.45 DEVIATIONS Entry 2).
- **Data.** Stage 2's three outcome pulls as §4.5 fixes them; no request is added. No sales-rank outcome is added (§4.6 unchanged).
- **Effect on the locked text.** None: no other hypothesis, window, statistic, threshold, seed or check changes.

---

## Change log

1. r0b: dates only, per Pablo's decision of Thu 11/26/2026, 7:39 am CT (Preview ~12/10; 3.0 data lock right after the Preview's; ship ~Tue 12/15). Changed: header (revision), §0 Status (target release), §5.4 (Preview data lock and publication), §11.4 (data-lock target), §16 (draft label); `papers/aias_3_0/SCHEDULE_aias_3_0_release_DRAFT.md` re-dated. No hypothesis, band, threshold, seed, analysis, check, wording rule or D1–D4 decision changed; the lock path (§0 Locks on, §17 choice 1) is unchanged.
