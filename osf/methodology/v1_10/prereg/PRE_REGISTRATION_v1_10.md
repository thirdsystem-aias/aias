# AIAS v1.10 — Ranking, Paper A: instrument, cross-category baseline, separability gate

AIAS™ Measurement Program — Third System™. Pre-registration **r2** (2026-11-10). Locked at git tag `v1.10-prereg-r2` (r1, tagged the same morning, was superseded before any computation; DEVIATIONS Entry 1) and deposited on OSF before any rank statistic was computed on confirmatory data.

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.10 |
| PHASE_TYPE | methodology lock; **re-analysis of archived answers** (no new acquisition, no model calls, no spend) |
| Status | r2 (r1 superseded before any computation, §15 item 17). Drafted by the runner's sub-agent on branch `v1.10` (from `aias-2.0`, commit `894ccee`); open questions settled by the runner on 2026-11-10 (§15). A re-analysis of archived answers: it locks without waiting for the author's read (program rule, Nov 9); any later correction is logged in DEVIATIONS. |
| Locks on | content lock → `prereg/LOCK_MANIFEST_v1_10.sha256` → commit → tag `v1.10-prereg-r2` → push branch and tag to GitHub → `anchor/git_anchor_v1_10.json` (tag object, commit, tree, UTC time, SHA-256 of every locked file) → OSF deposit of `osf/methodology/v1_10/prereg/`, `registries/` and `anchor/`, SHA-256 verified on OSF → only then the first confirmatory computation (`score_v1_10.py --stage S`), which refuses to run without the tag and the anchor file. |
| Locked inputs | Presence: protocol v1.6 (P = 100·(C_P/6 + 2·π̂)/3). Consistency: v1.8 φ, scaled by v1.9 to C_φ = 100(1 − φ/7.2), rated only with ≥ 6 total mentions (C*). Both read from `osf/aias_2_0/aias_2_0_profiles.csv`; neither is recomputed or re-weighted here. |
| Feeds forward | Ranking Paper B (only if the gate passes); the three-component calibration (Presence × Consistency × Ranking) at the AIAS 3.0 release. Numbering follows the FAST TRACK plan (Nov 9): v1.11 is Sentiment Paper A, so v1.9's forward reference to a "v1.11" calibration is superseded. |

**Lineage.** AIAS 2.0 (published 2026-11-10; tag `aias-2-0-paper-locked`) showed Consistency separable from Presence: within-category |ρ(C*, P)| = 0.073 (t1), 0.082 (t2), 0.189 (t3) (as published, under the uncentred pooled-rank convention that §7 replaces). The program's first Consistency instrument (v1.7 CV-CPC) failed its gate because it moved with recall (pooled ρ = 0.766 against a 0.50 ceiling). v1.10 applies the same discipline to Ranking before any rank statistic is computed on confirmatory data. Plan of record: Pablo, 2026-11-09 (Paper A = instrument specification + cross-category baseline + separability gate; Paper B later, only if A passes).

**Construct.** Ranking = where a brand sits in an answer's ordered list of brands, **given that the brand is named**. Whether a brand is named at all is Presence; how evenly models name it is Consistency. Ranking must add information neither carries, or it is not a component.

## 1. Research questions

- **RQ1 (instrument).** Can a deterministic, registry-based extractor recover each named brand's position in archived long-form answers (lists and prose) at a parse rate high enough to score brands across 13+ categories and two panels?
- **RQ2 (selection).** Which candidate rank statistic is most reliable within a panel, chosen by a rule fixed now and blind to Presence and Consistency?
- **RQ3 (gate: separability).** Within category, is the selected Ranking score separable from Presence (P) and from Consistency (C*) by the program's bands (|ρ| ≤ 0.30 CONFIRMED, ≥ 0.50 FALSIFIED)?
- **RQ4 (gate: reliability).** Does brand rank order hold across waves (3 weeks; 5 months) beyond what list composition alone produces? A score that is separable only because it is noise does not pass.
- **RQ5 (baseline).** What does Ranking look like per category and per panel (list lengths, how concentrated first positions are, score distributions)?

## 2. Frozen inputs

Source: `archive_inventory_scan.csv` (Nov 10, 2026; 67 answer sets). Every file below is pinned in `osf/methodology/v1_10/registries/INPUTS_MANIFEST_v1_10.json` (111 files: path, role, git blob SHA-1, SHA-256, bytes; base commit `894ccee9c65e3341c541191ac7ec1de48313a72a` on `aias-2.0`; all 111 present). The scorer reads only files pinned there. Blobs below are the first 10 hex digits; the manifest holds the full values. Answer counts are answers with text.

### 2.1 Primary gate set — OMNI (legacy six panel: claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite)

Phase B frame answers only (3 category-recall + 3 cultural/identity frames × 6 models = 36 per category per wave). Phase A files are yes/no probes or single-brand recognition and are not used.

| Substrate | t1 (May 20–26) | t2 (Jun 10; `osf/v34/data`) | t3 (Nov 9; `osf/v41/data`) | Answers |
|---|---|---|---|---|
| v0.19 audiophile headphones | `osf/v19/phase_b_responses.jsonl` 8d43ec8aad | 2aa30163db | 9822c31d08 | 3 × 36 |
| v0.20 skincare | `osf/v20/phase_b_results.csv` 9ed9ffeba2 | 121bb09786 | 56bdf1ae41 | 3 × 36 |
| v0.21 cosmetics | `osf/v21/phase_b_results.csv` 70c008262a | c81091aae9 | 439e7be44c | 3 × 36 |
| v0.22 (automotive registry) | `osf/v22/phase_b_results.csv` 8e9cab2fb3 | e55110bbc6 | 39c6104ec3 | 3 × 36 |
| v0.23 premium spirits | `osf/v23/data/v23_phase_b_raw.json` 5dd93b3fd6 | ffcb67d352 | a0c829a721 | 3 × 36 |
| **Total** | 180 | 180 | 180 | **540** |

Also pinned: certified mention files for parity (`v19/phase_b_results.csv`, `v23_phase_b_scored.json`, each wave); registries (`osf/v19/panel_registry_v0_19.csv`, `prereg/v0_20_registry.json`, `prereg/v0_21_registry.json`, `prereg/v0_22_automotive_content.py`; v0.23's inline registry written to `registries/v0_23_registry_v1_10.json` by `registries/build_registry_inputs_v1_10.py`: 24 brands, 62 aliases, from `scripts/score_v0_23.py`, cross-checked against `scripts/acquire_v0_23.py`); certified detectors (`scripts/score_v20.py`, `score_v21.py`, `score_v22.py`, `score_v0_31.py`, `score_v33.py`); **P and C\*** from `osf/aias_2_0/aias_2_0_profiles.csv` (336 rows = 112 units × 3 waves; C\* rated 55 / 54 / 54).

### 2.2 Selection and replication set — EARLY-6 (claude-sonnet-4-6, claude-opus-4-7, gpt-5.4-mini, gpt-5.5, gemini-2.5-flash, grok-4-1-fast)

Six prompt types (functional, contextual, constraint, identity, discovery, comparison) × 6 models × 8 runs (`run_idx` 1–8) per category, except v0.16 kitchen knives (row below). Nine sets: v1.0 knives and v0.16 kitchen knives are kept apart.

| Set | File | Blob | Answers |
|---|---|---|---|
| v0.9 PM software | `data/pm/results_enriched_v09_20260507_181205.csv` | ddd777a812 | 288 |
| v0.9 personal finance | `data/finance/results_enriched_v09_20260507_190816.csv` | 0c20f9bb9e | 288 |
| v0.9 olive oil | `data/oliveoil/results_enriched_v09_20260507_184159.csv` | 85b37c8c24 | 288 |
| v0.9 running shoes | `data/running/results_enriched_v09_20260507_183238.csv` | ce551cf057 | 288 |
| v0.9 skincare | `data/skincare/results_enriched_v09_20260507_185427.csv` | a2ce7bc8e1 | 288 |
| v1.0 household retail | `data/household/results_v2_household_v1.0_final.csv` (the file the phase scored) | in the manifest | 288 |
| v1.0 knives | `data/knives/results_v2_knives_v1.0_final.csv` | 65e55a4839 | 288 |
| v0.14 premium tea | `data/premium_tea/results_v2_premium_tea_20260512_161817_filled.csv` | 18614fb2bc | 288 |
| v0.16 kitchen knives | `data/kitchen_knives/results_v2_kitchen_knives_20260516_212400.csv` (11 prompts in 3 CEP groups × 6 models × 8 runs = 528 cells; 515 rows) | 1d68cd05f8 | 334 of 515 |
| **Total** | | | **2,638** |

Registries: for each set, the registry file that the source phase's extraction applied to that answer file (evidence per set in `registries/REGISTRY_CHOICES_v1_10.md`): `osf_staging/v09/registries/brands_<cat>.json` (v0.9 and v0.6; byte-identical to `registries/brands_<cat>.json`, commit 179b3d7), `registries/brands_household.json`, `registries/brands_knives_v1.0.json` (the file the knives runner loaded), `osf/v14/registries/brands_premium_tea.json` (the version `enrich.py` used), and for v0.16 kitchen knives the legacy adapter `registries/brands_kitchen_knives.json` (the file the runner and `enrich.py` loaded, matching the rows' registry stamp; the v0.16 panel file stays pinned but is not loaded). **Note:** `registries/brands_premium_tea.json` is a committed *symlink* to an absolute path in the main working tree, so git pins only the link text; the loader reads the tracked copy `osf/v14/registries/brands_premium_tea.json` (blob f0343b9252) instead, and the manifest records both.

### 2.3 Other confirmatory-period sets

| Set | Role in Paper A | File | Blob | Answers |
|---|---|---|---|---|
| EARLY-2 v0.6 (2 models: claude-sonnet-4-6, gpt-5.4-mini; 5 categories; Apr 29–30) | H6 early stability v0.6 → v0.9 (conditional on prompt parity, MQ8); baseline | `data/{pm,finance,running,skincare}/results_v2_2026043*` / `0429*`, `data/oliveoil/results_v2_20260430_091539.csv` (the canonical run, which v0.9 used as its t1) | in the manifest | 480 |
| COI-HOLD v0.28 frames (legacy six, one wave) | pinned and parse-checked only (MQ1); no statistic, because its technology panel needs its own COI screen first (as v0.43 decided) | `osf/v28/data/phase_b_results.csv` | f8d2bfb740 | 36 |
| PAPER-B v0.32 arms A / B (model-version pair, v0.22 registry) | **frozen now, not analysed in Paper A** (model-version stability is Paper B) | `osf/v32/data/phase_b_A.csv`, `phase_b_B.csv` | 8d5e57736a, e2a867603b | 36 + 36 |

Confirmatory-period answer total: 540 (OMNI) + 2,638 (EARLY-6) + 480 (EARLY-2) = **3,658**, plus 36 parse-checked only (v0.28) and 72 reserved for Paper B: 3,766 answers with text in the 32 pinned sets (§9a).

### 2.4 Development sample (excluded from every confirmatory analysis)

v0.17 phase B (18 answers, `osf/v17/data/phaseB_queries/*/slot_*.json`) and v0.18 phase B (18 answers, `data/phase_b/v0.18/phase_b_results.json`, blob b4d20ed12a). Used only for the declared parsing-feasibility note (`feasibility_v1_10.md`).

### 2.5 Excluded

v0.5 `archive/old_data` (pre-program, category uncertain); v0.10 `responses_mint.csv` (duplicates v0.6/v0.9 finance text); all yes/no recognition probes (v0.18–v0.22, v0.26, v0.28, v0.32 phase A); v0.23 phase A open recognition (one brand per answer: Sentiment's input, no list); v0.24 phase A (cut at 300 characters); v0.24 phase B (on branch v0.36 only, mixed panel: Q5); `osf/v41/data/_interrupted_v23_2026-11-09` (superseded by the complete rerun); `sandbox/tcl_prep` (not a program study); the program's two held studies (held studies are never made public, and this paper will be); the v0.6 olive-oil first run (`data/oliveoil/_pre_revision/results_v2_20260430_085246.csv`, superseded by the canonical run) and the v1.0 household merged file (superseded by the final file the phase scored). Raw first-pass files that the merged early files supersede are not read.

## 3. Order of operations (enforced by the scorer)

The scorer refuses Stage S and Stage C unless tag `v1.10-prereg-r2` and `anchor/git_anchor_v1_10.json` exist; `--dry-run` runs the whole pipeline on synthetic replicas of every file format only (`dryrun/`).

1. `verify_manifest()`: every file matches its SHA-256 and git blob, else **halt**.
2. Rank extraction (Section 4) on every frozen set; per-answer rank table written with its SHA-256.
3. Data-quality checks MQ1–MQ5 (Section 9). A failed halt condition stops the run.
4. **Stage S** (Section 6): statistic selection on EARLY-6 only, from rank tables only. `selection_v1_10.json` is written and hashed.
5. Only then does the scorer read the P and C\* values of `aias_2_0_profiles.csv` (the function refuses before step 4 exists; unit-tested). The 1:1 join on key columns (substrate, brand) ran before the lock (§9a) and runs again as Stage C's first act; a failed join halts Stage C.
6. **Stage C**: H1–H6, controls MQ6–MQ7, baseline, sensitivities. Verdicts written to `v1_10_verdicts.json`.

## 4. Rank extraction (rules E0–E7; implemented in `scripts/score_v1_10.py`, unit-tested)

- **E0 Unit of extraction.** One answer = one model response to one prompt (frame) in one run. Empty answers, API errors and rows without text are **missing cells**: they enter no denominator and are never read as "no brand named" (MQ4).
- **E1 Normalisation.** v1.4 canonical: Unicode NFKD, combining marks removed, lower case. All offsets are taken on the normalised text.
- **E2 Aliases and detection.** Each phase's own registry supplies canonical names and aliases (2.1–2.3); the canonical name is always an alias. Pattern = `\b` + escaped alias + `\b`, identical to the certified detectors (`score_v20/21/22.detect_mention`), including their known edge cases (an alias ending in a non-word character), which are listed, not fixed, so that the set of brands named in an answer is exactly the set Presence counted. v0.19 and v0.23 have coded mention files rather than a regex detector; their parity is checked in MQ2. The EARLY phases extracted brands with a model and have no certified regex detector: the same rule is applied with the registry each of them used (§2.2). No NER, no model-based extraction. Brands outside the registry are not ranked (rank is among registry brands).
- **E3 List items.** A list item is a line, indented at most 3 spaces, that starts with a number (`1.` or `1)`), a bullet (`-`, `*`, `+`, `•`, `–`), a Markdown heading (`#`–`######`) or a bold run (`**…**`). Top-level items are headings plus the non-heading item lines at the smallest indentation in the answer; deeper lines belong to their parent item. An item runs to the next top-level item; the last runs to the end of the answer.
- **E4 Brands named twice.** Only the first occurrence fixes a brand's first-mention offset; later repeats are ignored (v1.4 first-occurrence-wins). In a list, a brand **leads** an item when its earliest match inside the item precedes every other registry brand's match in that item.
- **E5 Rankable answers.** An answer is rankable iff it names **≥ 2** registry brands. Answers naming 0 or 1 contribute nothing to Ranking (counted in the baseline).
- **E6 Position rule (primary, "lead-item").** An answer is *list-structured* iff ≥ 2 of its top-level items are led by a registry brand. In a list-structured answer, brands are ordered by the index of the first item they lead; brands that lead no item (named only in passing, an intro or a closing line) follow all leading brands, in first-mention order. In an answer that is not list-structured (prose, or a list whose items carry no registry brand), brands are ordered by first mention. **Sensitivity S1 ("first-mention")**: first-mention order in every answer.
- **E7 Ties.** Brands with equal sort keys (in practice: identical first-match offsets, e.g. one brand's alias nested in another's, or two brands leading one item at the same offset) are tied: they receive the **mid-rank** (k_mid, average of the positions they occupy) and the **competition min-rank** (k_min). Nested-match events are logged (MQ5).
- **Output per (answer, brand named)**: k_mid, k_min, n (registry brands named), list_structured, rule. Normalised position q = (k_mid − 1)/(n − 1) ∈ [0, 1], 0 = first, 1 = last.

Feasibility on the development sample (Section 2.4; `feasibility_v1_10.md`) informed E3, E4 and E6: lists dominate (72–100% of answers list-structured), repeats are frequent (13–55% of brand-answer pairs), and the two rules disagree in 0–11% of rankable answers (mean Kendall τ 0.96–1.00).

## 5. Candidate statistics, rating floor and never-named brands

For brand b in category c (within one panel and wave), over its rankable answers A_b (n_b = |A_b|), all oriented so that **higher = nearer the top**:

| Id | Statistic | Definition |
|---|---|---|
| MNP | mean normalised position | R = 100 · (1 − mean_a q_ab) (0–100; 100 = always first) |
| IRW | inverse-rank weight | mean_a 1/k_mid |
| TOP3 | top-3 share | share of A_b with k_min ≤ 3 |
| MR | mean rank | −mean_a k_mid |
| TOP1 | named-first share | share of A_b with k_min = 1 |
| MODE | modal rank | −(modal k_min; the smallest mode when several) |

- **Rating floor.** A brand's Ranking score is **rated (R\*) iff n_b ≥ 6** rankable mentions in that panel × wave × category (the v1.9 C\* floor). Otherwise it is NOT RATED.
- **Never-named brands** (n_b = 0) are **NOT RATED**: absence is Presence's information, not a position. No penalty rank is imputed in any confirmatory statistic. The penalised variant (never-named and unnamed-in-answer brands scored q = 1) exists only as the positive control MQ6, because it builds Presence into Ranking by construction (the CV-CPC trap).
- **Unit.** (panel, wave, category, brand). OMNI units match the 112 brand units of `aias_2_0_profiles.csv` by substrate and canonical brand name (MQ2 asserts the join is 1:1).

## 6. Selection rule (Stage S), fixed in advance, blind to Presence and Consistency

1. Data: EARLY-6 rank tables only (no P, no C, no OMNI data).
2. For each candidate s and each EARLY-6 category, compute brand scores separately on **odd** and **even** `run_idx` answers (runs 1, 3, 5, 7 vs 2, 4, 6, 8). Units: brands rated (≥ 6 rankable mentions) in both halves; categories with ≥ 5 such units.
3. r_s = pooled within-category Spearman between halves (ρ_w as defined in §7, with centred ranks); reliability = Spearman–Brown 2r/(1 + r).
4. Eligible: reliability ≥ **0.50**. Select the eligible candidate with the highest reliability; candidates within **0.02** of the best are tied and the tie goes to the first in the order **MNP, IRW, TOP3, MR, TOP1, MODE** (normalised before raw, continuous before coarse).
5. If no candidate reaches 0.50: Paper A reports **INSTRUMENT FAIL** (no reliable rank statistic), Stage C is still run for the record with MNP, and the instrument is redesigned.
6. MQ7 (negative control) runs alongside: with positions shuffled within each answer (2,000 draws, seed 110030), the selected statistic's mean split-half reliability must stay **< 0.20**; otherwise the selection is flagged as list-composition-driven (reported, verdicts unchanged).
7. Reported next to the selection, never changing it: S8 (reliabilities without v1.0 knives and v0.16 kitchen knives, whose registries carry ordinary-word aliases; MQ5) and S9 (the uncentred ρ_w convention, §7).

Rationale: selecting on reliability can only make the separability gate harder to pass (a more reliable score has less attenuation against P), and EARLY-6 is a different panel from the gate set.

## 7. Hypotheses, statistics, nulls and verdicts (Stage C)

Conventions. ρ_w = pooled within-category Spearman: average ranks are computed within each category and **centred on the category's mean rank (m_c + 1)/2**; ρ_w is the Pearson correlation of the pooled centred ranks. Centring changes the v0.37 / v0.41 convention, which pooled uncentred ranks: when categories contribute different numbers of units, uncentred pooling adds a between-category component, so that statistic is above 0 in expectation even with no association inside any category (found while implementing this scorer, Nov 10). The within-category permutation and shuffle nulls are valid under either convention; the absolute bands are not. The uncentred value is reported as sensitivity S9. Only categories with ≥ 5 units in the comparison enter. Values are compared unrounded. Permutation p = (hits + 1)/(N + 1); H1 and H2 use one seed at every wave. Bootstrap: units resampled within category, 2,000 draws, seed 110020, 90% percentile CI (reported, not a verdict input). R\* = the Stage S statistic, rated units only.

| Tag | Tier | Statement | Statistic and data | Null | CONFIRMED iff | FALSIFIED iff | MARGINAL | UNDETERMINED iff |
|---|---|---|---|---|---|---|---|---|
| **H1_Sep_Presence** | PRIMARY (gate) | Ranking is separable from Presence. | ρ_w(R\*, P) per OMNI wave t1, t2, t3; units with R\* rated; P from `aias_2_0_profiles.csv` | R\* permuted within substrate, 10,000 draws, seed 110001, two-sided (p reported) | \|ρ\| ≤ 0.30 at every wave meeting the floor | \|ρ\| ≥ 0.50 at any wave meeting the floor | otherwise | fewer than 2 waves with ≥ 30 rated units |
| **H2_Sep_Consistency** | PRIMARY (gate) | Ranking is separable from Consistency. | ρ_w(R\*, C\*) per OMNI wave; units with R\* and C\* both rated | as H1, seed 110002 | \|ρ\| ≤ 0.30 at every wave meeting the floor | \|ρ\| ≥ 0.50 at any wave meeting the floor | otherwise | fewer than 2 waves with ≥ 30 units |
| **H3_Rank_Stability** | PRIMARY (gate: reliability leg) | Brand rank order holds over 3 weeks beyond list composition. | ρ_w(R\*_t1, R\*_t2), OMNI, units rated in both waves | (a) R\*_t2 permuted within substrate, 10,000 draws, seed 110003, one-sided; (b) within-answer order shuffle of both waves, 10,000 draws, seed 110010, one-sided | ρ ≥ 0.50 AND p_perm < 0.05 AND p_shuffle < 0.05 | ρ < 0.30 OR p_perm ≥ 0.05 OR p_shuffle ≥ 0.05 | otherwise | n < 30 |
| H4_Sep_Presence_Early | SECONDARY (gate downgrade only) | Separability replicates in the other panel. | ρ_w(R\*, π̂) on EARLY-6, π̂ = share of the category's answers with text naming the brand (Presence's recall arm; no recognition probes exist for these studies) | R\* permuted within category, 10,000, seed 110004, two-sided | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise | n < 30 |
| H5_Rank_LongHorizon | SECONDARY | Rank order holds over 5 months. | ρ_w(R\*_t2, R\*_t3), OMNI; t1 → t3 reported descriptively | as H3, seeds 110005 / 110010 | as H3 | as H3 | as H3 | n < 30 |
| H6_Early_Stability | SECONDARY (conditional on MQ8) | Rank order holds over 8 days in the early panel. | ρ_w(R\*_v0.6, R\*_v0.9) on the two shared models (claude-sonnet-4-6, gpt-5.4-mini), 5 categories, units rated in both | as H3, seed 110006 | as H3 | as H3 | as H3 | n < 30, or MQ8 fails |

**GATE (Paper A verdict).**
- **FAIL** if Stage S ends in INSTRUMENT FAIL, or any of H1, H2, H3 is FALSIFIED → reported as a negative result (the v1.7 precedent); the instrument is redesigned under a new pre-registration; no Paper B on this instrument.
- else **UNDETERMINED** if any of H1–H3 is UNDETERMINED → data cause fixed and reported; no Paper B.
- else **PASS** if H1, H2 and H3 are all CONFIRMED — downgraded to **MARGINAL** if H4 is FALSIFIED (separability depends on the panel).
- else **MARGINAL** → reported as is; Paper B only on Pablo's recorded decision, with the marginal leg as Paper B's first confirmatory test.

Secondary hypotheses never turn a FAIL into a PASS. MQ6/MQ7 flags are printed next to the gate verdict.

## 8. Cross-category baseline (descriptive, stratified by panel)

Strata, never pooled across panels without the split: **EARLY-6** (9 sets), **EARLY-2** (v0.6, 5 categories), **LEGACY-6** (OMNI by wave). The newest models enter with t4 (Paper B). Per stratum × category (× wave):

1. answers, missing cells, rankable share, list-structured share, numbered-list share;
2. registry brands named per rankable answer (median, IQR, max);
3. brands rated / registry size; per model, the share of rated brands it names in at least one rankable answer (model style);
4. R\* distribution of the selected statistic and of MNP (median, IQR, range);
5. leader concentration: share of rankable answers led by the most frequent first-named brand (first-named = k_min = 1), and the Herfindahl index of first-named brands (tied leaders split the weight);
6. per model: mean list length (registry brands named per rankable answer) and list-structured share;
7. the three highest-R\* brands per category.

## 9. Manipulation and data-quality checks

| Id | Check | Rule (numbers fixed) |
|---|---|---|
| MQ1 | Parse rate | extractor completes on 100% of answers with text (an exception halts); rankable share reported per set, sets below 0.50 flagged |
| MQ2 | Mention parity + join | v0.20–v0.22: extractor's named set = certified detector's on 100% of (answer, brand) cells, else halt and fix before Stage S. v0.19, v0.23 (coded files): agreement ≥ 0.98 per wave, else that substrate leaves H1–H3 at every wave (deviation entry). Join to `aias_2_0_profiles.csv`: 112 units per wave, 1:1 |
| MQ3 | Concordance with archived LLM extraction | EARLY sets: median per-answer Kendall τ between the E6 order and the archived `brands_ranked` (function calling), common brands; < 0.60 flags an extraction review (no change without a deviation entry) |
| MQ4 | Missing cells | listed, never imputed: v0.16 kitchen knives 181 of 515 rows without text (`missing_cells_v16.csv` lists 445 cells; no filled file found; per model gemini 83, grok 80 of 88); 13 of its 528 design cells have no row; v1.0 household (final file) 288 of 288 with text; OMNI expected 36 per category per wave (shortfalls listed) |
| MQ5 | Overlap and alias log | nested-match events, aliases shared by two brands, aliases and canonical names ending in a non-word character (two names in the kitchen-knives adapter end in ")" and cannot match), and aliases that are ordinary words (v1.0 knives: global, mac, made in; kitchen-knives adapter: those three plus dick, kramer, new west): listed and counted per set |
| MQ6 | Positive control | penalised MNP (unnamed brands at q = 1, a brand named alone at q = 0, all answers with text) must give \|ρ_w(R_pen, P)\| ≥ 0.50 at every OMNI wave; otherwise the gate's sensitivity is flagged |
| MQ7 | Negative control | within-answer order shuffle: mean split-half reliability of the selected statistic < 0.20 (2,000 draws, seed 110030) |
| MQ8 | Prompt parity v0.6 / v0.9 | identical prompt ids and prompt texts per category (v0.6 `prompt_set_version` "v2" vs v0.9 "<cat>_v1.0"); otherwise H6 is not run |
| MQ9 | Truncation | descriptive only: no analysed set stores finish reasons or the token cap; caps are taken from each phase's pre-registration and scripts and reported per set |

### 9a. Pre-lock parity (declared; no rank position or statistic computed)

Run on 2026-11-10 with `score_v1_10.py --parity`, which never calls the rank extractor and reads only the key columns of the profiles table (`prereg/parity_v1_10.json`): MQ1 parse completion 100% on all 32 pinned sets (3,766 answers with text; v1.0 household 288 of 288, v0.6 olive oil 96 of 96, v0.16 kitchen knives 334 of 515); MQ2 for v0.20, v0.21 and v0.22 against their certified detectors 864/864 = 1.0000 at t1, t2 and t3; v0.19 against its coded files 576/576 = 1.0000 and v0.23 864/864 = 1.0000 at every wave; join to `aias_2_0_profiles.csv` 112/112 units, 1:1, at t1, t2 and t3. The scorer passes 61 unit tests and runs end to end on synthetic replicas of every file format (`dryrun/`).

## 10. Sensitivity analyses (reported; never change a verdict)

S1 first-mention rule (E6). S2 rating floor 3 and 10. S3 all six candidates through H1–H3 (full table). S4 leave-one-substrate-out ranges for H1–H3. S5 recall arm: ρ_w(R\*, π̂) and ρ_w(R\*, total mentions) next to ρ_w(R\*, P). S6 OMNI without the models whose served snapshot v0.41 MC_Snapshot flags (it flags none, so S6 is reported as identical to the primary analysis). S7 H1–H3 without the brands that the COI re-check of DEVIATIONS Entry 0 flags (`anchor/coi_flags_v1_10.json`, written by a dated DEVIATIONS entry before Stage C; units removed from every correlation, answers not re-ranked; reported as "no flagged brands" if the file is absent). S8 Stage S without the two knife sets (§6). S9 every pooled statistic under the uncentred v0.37–v0.41 convention (§7). Verdict changes under any sensitivity are listed next to the verdict.

## 11. Predictions (written before any rank statistic on confirmatory data)

Stage S lean: MNP or IRW. H1 lean MARGINAL: conditioning on mention removes the mechanical link, but the most-recalled brands are plausibly also named first (a Double-Jeopardy-like pattern), which is the main risk to the gate. H2 lean CONFIRMED (C\* barely tracks P). H3 lean CONFIRMED over three weeks; H5 lean MARGINAL over five months. MQ6 lean passes (the penalised variant should track P strongly).

## 12. Limitations

- Re-analysis of answers already in the record: P and C\* are published (AIAS 2.0). To the runner's knowledge no rank statistic of this kind has been computed on these answers for the program's papers, but archived position data exist: the early files carry `brands_ranked` and `primary_recommendation` columns from model-based extraction (the v0.7 and v0.8 papers describe extracting rank and primary-recommendation flags), the v0.19 coded files carry a per-mention `rank` column and the v0.23 scored files `slot_positions`. v1.10 never reads them (`brands_ranked` only for the MQ3 concordance). The lock fixes everything before Stage S runs.
- Rank is among **registry** brands only. In the development sample 51–66% of top-level list items carry no registry brand (product lines, retailers, unregistered brands, section headings), so an answer's absolute list position and the registry rank differ.
- The rating floor restricts the range of P among rated brands, which can lower |ρ| (MQ6 and S2 address this).
- OMNI is small per category (16–24 brand units, 36 answers per wave); EARLY sets have one wave each (H6 is the only early stability test).
- Position in text is not visual prominence; the lead-item parser relies on Markdown conventions (headings, bold, numbers).
- One legacy panel carries the gate; the newest models enter with t4 (Paper B).

## 13. Deviations policy

`osf/methodology/v1_10/anchor/DEVIATIONS.md` opens with **Entry 0 (ex ante)**: COI screen (no new brand selection; each substrate keeps its source-phase COI handling, quoted verbatim from the source records: the v0.22 tier-2/3 Harman / Samsung SDI / Samsung Display disclosure and the v0.19 AKG → Denon substitution), the 2026-11-10 re-check of registry-brand ownership (its handling awaits the author's decision and is entered in the log before any v1.10 result is reported; S7), the pre-lock record, and the anchor sequence of Section 0. After the lock:

1. Every change gets an entry: id, date, ex ante / ex post, what changed, why, effect on inference.
2. A frozen-input hash mismatch **halts** the run; no substitute file is used without an entry.
3. An extractor bug fix is allowed only if it restores a rule as written here; verdicts are reported both before and after the fix.
4. Thresholds, the candidate set, the selection rule, n floors, seeds and the gate rule do not change after the lock. Anything added later is labelled exploratory.
5. A failed gate is published as a negative result with the same prominence as a pass.

## 14. What Paper B inherits (not pre-registered here)

Paper B is pre-registered separately and only after a PASS (or a MARGINAL with Pablo's recorded decision). Paper A hands it:
- the locked extractor (E0–E7), `scripts/score_v1_10.py` and its tests; the selected statistic and the rating floor;
- per-answer rank tables (SHA-256 pinned) for every frozen set, including the **v0.32 arms** (frozen now, unanalysed) for **model-version stability**;
- OMNI R\* per wave (t1, t2, t3) next to P and C\* for the **typology**; frame labels (category vs cultural) and EARLY prompt types for **phrasing stability**; the OMNI cells for **identity load**;
- registry flags for phantom brands, for the **phantom-brand bands**;
- the t4 wave (v0.42, newest models, three runs per cell) for the newest-model baseline;
- a note that the **Light Buyer Paradox** test needs a buyer-weight variable that Paper B must define first;
- the MQ6 / MQ7 null distributions and the Paper A verdict file.

## 15. Decisions settled before the lock (runner, 2026-11-10)

1. Primary position rule: lead-item (E6); first-mention is S1.
2. Floors unchanged: R\* rated at ≥ 6 rankable mentions (the v1.9 C\* floor); n floor 30 units; ≥ 5 units per category.
3. Stage S runs mechanically after the lock.
4. Registry per early set: the file the source phase's extraction applied (§2.2; `registries/REGISTRY_CHOICES_v1_10.md`). Two answer files were replaced by the files their phases actually used: v0.6 olive oil (canonical run) and v1.0 household (final file).
5. v0.24 phase B stays excluded.
6. The gate's reliability leg is t1 → t2 (H3); t2 → t3 is H5 (secondary).
7. A MARGINAL gate goes to Pablo's recorded decision (§7).
8. v0.19 / v0.23 parity floor 0.98 kept (both reached 1.0000 before the lock, §9a); v0.23's inline registry is pinned as a file (§2.1).
9. The archived `brands_ranked` is a concordance check only (MQ3), never a fallback extractor.
10. Numbering: v1.11 is Sentiment Paper A (FAST TRACK, Nov 9).
11. The program's two held studies are excluded from v1.10 entirely; v0.28 is pinned and parse-checked only, pending its own COI screen.
12. Earlier position data are declared in §12.
13. Loaders and the full pipeline are implemented, unit-tested (61 tests) and dry-run on synthetic replicas; on real files only the parity checks of §9a ran before the lock.
14. Shuffle nulls of H3, H5 and H6: 10,000 draws; MQ7 keeps 2,000 (a control).
15. The v0.5 archive stays excluded.
16. Added before the lock: centred ρ_w (§7) with S9; S7 (COI re-check); S8 (knife sets at Stage S); H4 two-sided; MQ5 alias lists.
17. r2 (2026-11-10, before any computation): r1's input manifest pinned the pre-edit hash of the documentation file `registries/REGISTRY_CHOICES_v1_10.md`, whose header line was changed at the content lock; Stage S halted at manifest verification, as designed, before any extraction. r2 rebuilds the input manifest and the parity record and moves the tag; no rule, threshold, input data file or analysis step changed.
