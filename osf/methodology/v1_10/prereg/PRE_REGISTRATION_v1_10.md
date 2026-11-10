# AIAS v1.10 — Ranking, Paper A: instrument, cross-category baseline, separability gate

AIAS™ Measurement Program — Third System™. Pre-registration **DRAFT r1** (2026-11-10). **Not locked.**

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | v1.10 |
| PHASE_TYPE | methodology lock; **re-analysis of archived answers** (no new acquisition, no model calls, no spend) |
| Status | DRAFT r1, written by the runner's sub-agent on branch `v1.10` (from `aias-2.0`, commit `894ccee`). Not reviewed by Pablo. |
| Locks on | content lock → commit → tag `v1.10-prereg-r1` → OSF deposit of `osf/methodology/v1_10/prereg/` + `registries/INPUTS_MANIFEST_v1_10.json` + `git_anchor_v1_10.json` (tag object, commit, tree, SHA-256 of every locked file) → both anchors verified → only then the first confirmatory computation (`score_v1_10.py --stage S`). Push to GitHub when access exists (v1.9 DEVIATIONS Entry 1 precedent). |
| Locked inputs | Presence: protocol v1.6 (P = 100·(C_P/6 + 2·π̂)/3). Consistency: v1.8 φ, scaled by v1.9 to C_φ = 100(1 − φ/7.2), rated only with ≥ 6 total mentions (C*). Both read from `osf/aias_2_0/aias_2_0_profiles.csv`; neither is recomputed or re-weighted here. |
| Feeds forward | Ranking Paper B (only if the gate passes); the three-component calibration (Presence × Consistency × Ranking) that v1.9 names as v1.11 (numbering to settle: the archive inventory names Sentiment v1.11; open question 10). |

**Lineage.** AIAS 2.0 (published 2026-11-10; tag `aias-2-0-paper-locked`) showed Consistency separable from Presence: within-category |ρ(C*, P)| = 0.073 (t1), 0.082 (t2), 0.189 (t3). The program's first Consistency instrument (v1.7 CV-CPC) failed its gate because it moved with recall (pooled ρ = 0.766 against a 0.50 ceiling). v1.10 applies the same discipline to Ranking before any rank statistic is computed on confirmatory data. Plan of record: Pablo, 2026-11-09 (Paper A = instrument specification + cross-category baseline + separability gate; Paper B later, only if A passes).

**Construct.** Ranking = where a brand sits in an answer's ordered list of brands, **given that the brand is named**. Whether a brand is named at all is Presence; how evenly models name it is Consistency. Ranking must add information neither carries, or it is not a component.

## 1. Research questions

- **RQ1 (instrument).** Can a deterministic, registry-based extractor recover each named brand's position in archived long-form answers (lists and prose) at a parse rate high enough to score brands across 13+ categories and two panels?
- **RQ2 (selection).** Which candidate rank statistic is most reliable within a panel, chosen by a rule fixed now and blind to Presence and Consistency?
- **RQ3 (gate: separability).** Within category, is the selected Ranking score separable from Presence (P) and from Consistency (C*) by the program's bands (|ρ| ≤ 0.30 CONFIRMED, ≥ 0.50 FALSIFIED)?
- **RQ4 (gate: reliability).** Does brand rank order hold across waves (3 weeks; 5 months) beyond what list composition alone produces? A score that is separable only because it is noise does not pass.
- **RQ5 (baseline).** What does Ranking look like per category and per panel (list lengths, how concentrated first positions are, score distributions)?

## 2. Frozen inputs

Source: `archive_inventory_scan.csv` (Nov 10, 2026; 67 answer sets). Every file below is pinned in `osf/methodology/v1_10/registries/INPUTS_MANIFEST_v1_10.json` (88 files: path, role, git blob SHA-1, SHA-256, bytes; base commit `894ccee9c65e3341c541191ac7ec1de48313a72a` on `aias-2.0`; all 88 present). Blobs below are the first 10 hex digits; the manifest holds the full values. Answer counts are answers with text.

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

Also pinned: certified mention files for parity (`v19/phase_b_results.csv`, `v23_phase_b_scored.json`, each wave); registries (`osf/v19/panel_registry_v0_19.csv`, `prereg/v0_20_registry.json`, `prereg/v0_21_registry.json`, `prereg/v0_22_automotive_content.py`, v0.23 inline); certified detectors (`scripts/score_v20.py`, `score_v21.py`, `score_v22.py`, `score_v0_31.py`, `score_v33.py`); **P and C\*** from `osf/aias_2_0/aias_2_0_profiles.csv` (336 rows = 112 units × 3 waves; C\* rated 55 / 54 / 54).

### 2.2 Selection and replication set — EARLY-6 (claude-sonnet-4-6, claude-opus-4-7, gpt-5.4-mini, gpt-5.5, gemini-2.5-flash, grok-4-1-fast)

Six prompt types (functional, contextual, constraint, identity, discovery, comparison) × 6 models × 8 runs (`run_idx` 1–8) per category.

| Set | File | Blob | Answers |
|---|---|---|---|
| v0.9 PM software | `data/pm/results_enriched_v09_20260507_181205.csv` | ddd777a812 | 288 |
| v0.9 personal finance | `data/finance/results_enriched_v09_20260507_190816.csv` | 0c20f9bb9e | 288 |
| v0.9 olive oil | `data/oliveoil/results_enriched_v09_20260507_184159.csv` | 85b37c8c24 | 288 |
| v0.9 running shoes | `data/running/results_enriched_v09_20260507_183238.csv` | ce551cf057 | 288 |
| v0.9 skincare | `data/skincare/results_enriched_v09_20260507_185427.csv` | a2ce7bc8e1 | 288 |
| v1.0 household retail | `data/household/results_v2_household_v1.0_merged.csv` | dee9cd0a7f | 250 of 288 |
| v1.0 knives | `data/knives/results_v2_knives_v1.0_final.csv` | 65e55a4839 | 288 |
| v0.14 premium tea | `data/premium_tea/results_v2_premium_tea_20260512_161817_filled.csv` | 18614fb2bc | 288 |
| v0.16 kitchen knives | `data/kitchen_knives/results_v2_kitchen_knives_20260516_212400.csv` | 1d68cd05f8 | 334 of 515 |
| **Total** | | | **2,600** |

Registries: `osf_staging/v09/registries/brands_<cat>.json` (v0.9), `registries/brands_household.json`, `brands_knives_v1.0.json`, `brands_premium_tea.json`, `brands_kitchen_knives_v0.16.json` (open question 4 on the +v1.1 / +v0.15 variants). **Note:** `registries/brands_premium_tea.json` is a committed *symlink* to an absolute path in the main working tree (`/Users/pablou/aias/osf/v14/registries/…`), so git pins only the link text. The loader reads the tracked copy `osf/v14/registries/brands_premium_tea.json` (blob f0343b9252, identical content today) instead, and the manifest records both.

### 2.3 Other confirmatory-period sets

| Set | Role in Paper A | File | Blob | Answers |
|---|---|---|---|---|
| EARLY-2 v0.6 (2 models: claude-sonnet-4-6, gpt-5.4-mini; 5 categories; Apr 29–30) | H6 early stability v0.6 → v0.9 (conditional on prompt parity, MQ8); baseline | `data/{pm,finance,running,skincare}/results_v2_2026043*` / `0429*`, `data/oliveoil/_pre_revision/results_v2_20260430_085246.csv` | 606ab0f21a, 9a1852bc8d, 984a650412, 43f9ddaca8, e652b81614 | 480 |
| HELD v0.38 home coffee roasters (legacy six) | baseline only; **analysed, never published on the website** | `osf/v38/data/v38_raw.json` | 41924db725 | 132 |
| HELD v0.39 commercial roasters (legacy six + claude-opus-5-5, gpt-6-astra, gemini-4-argon; search off/on) | baseline only, stratified by arm and search condition; never on the website | `osf/v39/data/v39_raw.json` | 447ee7ba63 | 360 |
| BASELINE v0.28 frames (legacy six, one wave) | baseline only | `osf/v28/data/phase_b_results.csv` | f8d2bfb740 | 36 |
| PAPER-B v0.32 arms A / B (model-version pair, v0.22 registry) | **frozen now, not analysed in Paper A** (model-version stability is Paper B) | `osf/v32/data/phase_b_A.csv`, `phase_b_B.csv` | 8d5e57736a, e2a867603b | 36 + 36 |

Confirmatory-period answer total: 540 (OMNI) + 2,600 (EARLY-6) + 480 (EARLY-2) + 528 (HELD, BASELINE) = **4,148**, plus 72 reserved for Paper B.

### 2.4 Development sample (excluded from every confirmatory analysis)

v0.17 phase B (18 answers, `osf/v17/data/phaseB_queries/*/slot_*.json`) and v0.18 phase B (18 answers, `data/phase_b/v0.18/phase_b_results.json`, blob b4d20ed12a). Used only for the declared parsing-feasibility note (`feasibility_v1_10.md`).

### 2.5 Excluded

v0.5 `archive/old_data` (pre-program, category uncertain); v0.10 `responses_mint.csv` (duplicates v0.6/v0.9 finance text); all yes/no recognition probes (v0.18–v0.22, v0.26, v0.28, v0.32 phase A); v0.23 phase A open recognition (one brand per answer: Sentiment's input, no list); v0.24 phase A (cut at 300 characters); v0.24 phase B (on branch v0.36 only, mixed panel: Q5); `osf/v41/data/_interrupted_v23_2026-11-09` (superseded by the complete rerun); `sandbox/tcl_prep` (not a program study). Raw first-pass files that the merged early files supersede are not read.

## 3. Order of operations (enforced by the scorer)

1. `verify_manifest()`: every file matches its SHA-256 and git blob, else **halt**.
2. Rank extraction (Section 4) on every frozen set; per-answer rank table written with its SHA-256.
3. Data-quality checks MQ1–MQ5 (Section 9). A failed halt condition stops the run.
4. **Stage S** (Section 6): statistic selection on EARLY-6 only, from rank tables only. `selection_v1_10.json` is written and hashed.
5. Only then does the scorer open `aias_2_0_profiles.csv` (the function refuses before step 4 exists; unit-tested).
6. **Stage C**: H1–H6, controls MQ6–MQ7, baseline, sensitivities. Verdicts written to `v1_10_verdicts.json`.

## 4. Rank extraction (rules E0–E7; implemented in `scripts/score_v1_10.py`, unit-tested)

- **E0 Unit of extraction.** One answer = one model response to one prompt (frame) in one run. Empty answers, API errors and rows without text are **missing cells**: they enter no denominator and are never read as "no brand named" (MQ4).
- **E1 Normalisation.** v1.4 canonical: Unicode NFKD, combining marks removed, lower case. All offsets are taken on the normalised text.
- **E2 Aliases and detection.** Each phase's own registry supplies canonical names and aliases (2.1–2.3); the canonical name is always an alias. Pattern = `\b` + escaped alias + `\b`, identical to the certified detectors (`score_v20/21/22.detect_mention`), including their known edge cases (an alias ending in a non-word character), which are listed, not fixed, so that the set of brands named in an answer is exactly the set Presence counted. v0.19 and v0.23 have coded mention files rather than a regex detector; their parity is checked in MQ2. No NER, no model-based extraction. Brands outside the registry are not ranked (rank is among registry brands).
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
3. r_s = pooled within-category Spearman between halves (Pearson of within-category average ranks); reliability = Spearman–Brown 2r/(1 + r).
4. Eligible: reliability ≥ **0.50**. Select the eligible candidate with the highest reliability; candidates within **0.02** of the best are tied and the tie goes to the first in the order **MNP, IRW, TOP3, MR, TOP1, MODE** (normalised before raw, continuous before coarse).
5. If no candidate reaches 0.50: Paper A reports **INSTRUMENT FAIL** (no reliable rank statistic), Stage C is still run for the record with MNP, and the instrument is redesigned.
6. MQ7 (negative control) runs alongside: with positions shuffled within each answer (2,000 draws, seed 110030), the selected statistic's mean split-half reliability must stay **< 0.20**; otherwise the selection is flagged as list-composition-driven (reported, verdicts unchanged).

Rationale: selecting on reliability can only make the separability gate harder to pass (a more reliable score has less attenuation against P), and EARLY-6 is a different panel from the gate set.

## 7. Hypotheses, statistics, nulls and verdicts (Stage C)

Conventions. ρ_w = pooled within-category Spearman: Pearson correlation of within-category average ranks (v0.37 / v0.41 convention); only categories with ≥ 5 units in the comparison enter. Values are compared unrounded. Permutation p = (hits + 1)/(N + 1). Bootstrap: units resampled within category, 2,000 draws, seed 110020, 90% percentile CI (reported, not a verdict input). R\* = the Stage S statistic, rated units only.

| Tag | Tier | Statement | Statistic and data | Null | CONFIRMED iff | FALSIFIED iff | MARGINAL | UNDETERMINED iff |
|---|---|---|---|---|---|---|---|---|
| **H1_Sep_Presence** | PRIMARY (gate) | Ranking is separable from Presence. | ρ_w(R\*, P) per OMNI wave t1, t2, t3; units with R\* rated; P from `aias_2_0_profiles.csv` | R\* permuted within substrate, 10,000 draws, seed 110001, two-sided (p reported) | \|ρ\| ≤ 0.30 at every wave meeting the floor | \|ρ\| ≥ 0.50 at any wave meeting the floor | otherwise | fewer than 2 waves with ≥ 30 rated units |
| **H2_Sep_Consistency** | PRIMARY (gate) | Ranking is separable from Consistency. | ρ_w(R\*, C\*) per OMNI wave; units with R\* and C\* both rated | as H1, seed 110002 | \|ρ\| ≤ 0.30 at every wave meeting the floor | \|ρ\| ≥ 0.50 at any wave meeting the floor | otherwise | fewer than 2 waves with ≥ 30 units |
| **H3_Rank_Stability** | PRIMARY (gate: reliability leg) | Brand rank order holds over 3 weeks beyond list composition. | ρ_w(R\*_t1, R\*_t2), OMNI, units rated in both waves | (a) R\*_t2 permuted within substrate, 10,000 draws, seed 110003, one-sided; (b) within-answer order shuffle of both waves, 2,000 draws, seed 110010, one-sided | ρ ≥ 0.50 AND p_perm < 0.05 AND p_shuffle < 0.05 | ρ < 0.30 OR p_perm ≥ 0.05 OR p_shuffle ≥ 0.05 | otherwise | n < 30 |
| H4_Sep_Presence_Early | SECONDARY (gate downgrade only) | Separability replicates in the other panel. | ρ_w(R\*, π̂) on EARLY-6, π̂ = share of the category's answers with text naming the brand (Presence's recall arm; no recognition probes exist for these studies) | R\* permuted within category, 10,000, seed 110004 | \|ρ\| ≤ 0.30 | \|ρ\| ≥ 0.50 | otherwise | n < 30 |
| H5_Rank_LongHorizon | SECONDARY | Rank order holds over 5 months. | ρ_w(R\*_t2, R\*_t3), OMNI; t1 → t3 reported descriptively | as H3, seeds 110005 / 110010 | as H3 | as H3 | as H3 | n < 30 |
| H6_Early_Stability | SECONDARY (conditional on MQ8) | Rank order holds over 8 days in the early panel. | ρ_w(R\*_v0.6, R\*_v0.9) on the two shared models (claude-sonnet-4-6, gpt-5.4-mini), 5 categories, units rated in both | as H3, seed 110006 | as H3 | as H3 | as H3 | n < 30, or MQ8 fails |

**GATE (Paper A verdict).**
- **FAIL** if Stage S ends in INSTRUMENT FAIL, or any of H1, H2, H3 is FALSIFIED → reported as a negative result (the v1.7 precedent); the instrument is redesigned under a new pre-registration; no Paper B on this instrument.
- else **UNDETERMINED** if any of H1–H3 is UNDETERMINED → data cause fixed and reported; no Paper B.
- else **PASS** if H1, H2 and H3 are all CONFIRMED — downgraded to **MARGINAL** if H4 is FALSIFIED (separability depends on the panel).
- else **MARGINAL** → reported as is; Paper B only on Pablo's recorded decision, with the marginal leg as Paper B's first confirmatory test.

Secondary hypotheses never turn a FAIL into a PASS. MQ6/MQ7 flags are printed next to the gate verdict.

## 8. Cross-category baseline (descriptive, stratified by panel)

Strata, never pooled across panels without the split: **EARLY-6** (8 categories), **EARLY-2** (v0.6, 5 categories), **LEGACY-6** (OMNI by wave; v0.28; v0.38; v0.39 legacy arm), **NEWEST-3** (v0.39 arm C), and v0.39 search-on vs search-off. Per stratum × category (× wave):

1. answers, missing cells, rankable share, list-structured share, numbered-list share;
2. registry brands named per rankable answer (median, IQR, max);
3. brands rated / registry size; share of rated brands per model (model style);
4. R\* distribution of the selected statistic and of MNP (median, IQR, range);
5. leader concentration: share of rankable answers led by the most frequent first-named brand, and the Herfindahl index of first-named brands;
6. per model: mean list length and list-structured share;
7. the three highest-R\* brands per category (held studies v0.38/v0.39: in the paper and OSF only, **never on the website**).

## 9. Manipulation and data-quality checks

| Id | Check | Rule (numbers fixed) |
|---|---|---|
| MQ1 | Parse rate | extractor completes on 100% of answers with text (an exception halts); rankable share reported per set, sets below 0.50 flagged |
| MQ2 | Mention parity + join | v0.20–v0.22: extractor's named set = certified detector's on 100% of (answer, brand) cells, else halt and fix before Stage S. v0.19, v0.23 (coded files): agreement ≥ 0.98 per wave, else that substrate leaves H1–H3 (deviation entry). Join to `aias_2_0_profiles.csv`: 112 units per wave, 1:1 |
| MQ3 | Concordance with archived LLM extraction | EARLY sets: median per-answer Kendall τ between the E6 order and the archived `brands_ranked` (function calling), common brands; < 0.60 flags an extraction review (no change without a deviation entry) |
| MQ4 | Missing cells | listed, never imputed: v0.16 kitchen knives 181 of 515 rows without text (`missing_cells_v16.csv` lists 445 cells; no filled file found; per model gemini 83, grok 80 of 88); v1.0 household 38 of 288 without text; OMNI expected 36 per category per wave (shortfalls listed) |
| MQ5 | Overlap and alias log | nested-match events, aliases shared by two brands, aliases ending in a non-word character: counts per set |
| MQ6 | Positive control | penalised MNP (unnamed brands at q = 1, all answers with text) must give \|ρ_w(R_pen, P)\| ≥ 0.50 at every OMNI wave; otherwise the gate's sensitivity is flagged |
| MQ7 | Negative control | within-answer order shuffle: mean split-half reliability of the selected statistic < 0.20 (2,000 draws, seed 110030) |
| MQ8 | Prompt parity v0.6 / v0.9 | identical prompt ids and prompt texts per category (v0.6 `prompt_set_version` "v2" vs v0.9 "<cat>_v1.0"); otherwise H6 is not run |
| MQ9 | Truncation | v0.38: 20 answers end MAX_TOKENS (Gemini); kept (positions before the cut are valid), sensitivity without them; no other set stores finish reasons, and none stores the token cap (taken from each phase's pre-registration and scripts) |

## 10. Sensitivity analyses (reported; never change a verdict)

S1 first-mention rule (E6). S2 rating floor 3 and 10. S3 all six candidates through H1–H3 (full table). S4 leave-one-substrate-out ranges for H1–H3. S5 recall arm: ρ_w(R\*, π̂) and ρ_w(R\*, total mentions) next to ρ_w(R\*, P). S6 OMNI without the dated-alias models that v0.41 MC_Snapshot flags. Verdict changes under any sensitivity are listed next to the verdict.

## 11. Predictions (written before any rank statistic on confirmatory data)

Stage S lean: MNP or IRW. H1 lean MARGINAL: conditioning on mention removes the mechanical link, but the most-recalled brands are plausibly also named first (a Double-Jeopardy-like pattern), which is the main risk to the gate. H2 lean CONFIRMED (C\* barely tracks P). H3 lean CONFIRMED over three weeks; H5 lean MARGINAL over five months. MQ6 lean passes (the penalised variant should track P strongly).

## 12. Limitations

- Re-analysis of answers already in the record: P and C\* are published (AIAS 2.0). To the runner's knowledge no rank statistic has been computed on these answers for the program's papers, but the early files carry `brands_ranked` and `primary_recommendation` columns from function-calling extraction, and early phase reports may have shown first-recommendation shares (Q12). The lock fixes everything before Stage S runs.
- Rank is among **registry** brands only. In the development sample 51–66% of top-level list items carry no registry brand (product lines, retailers, unregistered brands, section headings), so an answer's absolute list position and the registry rank differ.
- The rating floor restricts the range of P among rated brands, which can lower |ρ| (MQ6 and S2 address this).
- OMNI is small per category (16–24 brand units, 36 answers per wave); EARLY sets have one wave each (H6 is the only early stability test).
- Position in text is not visual prominence; the lead-item parser relies on Markdown conventions (headings, bold, numbers).
- One legacy panel carries the gate; the newest models enter only through v0.39 arm C (baseline) and later t4 (Paper B).

## 13. Deviations policy

`osf/methodology/v1_10/anchor/DEVIATIONS.md` opens with **Entry 0 (ex ante)**: COI screen (no new brand selection; each substrate keeps its source-phase COI handling, including the v0.22 Harman / Samsung SDI / Samsung Display disclosure and the v0.19 AKG → Denon substitution) and the anchor sequence of Section 0. After the lock:

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
- v0.39 arm C and search-on strata, and the t4 wave (v0.42, newest models, three runs per cell) for the newest-model baseline;
- a note that the **Light Buyer Paradox** test needs a buyer-weight variable that Paper B must define first;
- the MQ6 / MQ7 null distributions and the Paper A verdict file.

## 15. Open questions to settle before the lock

1. Primary position rule: lead-item (E6) or first-mention (S1)? The development sample shows the rules disagree in 2 of 18 rankable v0.17 answers and 0 of 14 in v0.18.
2. R\* floor 6 rankable mentions and the n floor of 30 units per wave: with 36 answers per category-wave, R\* coverage may sit near the floor (C\* rated: 55 / 54 / 54). Keep, or lower to 5 / 25?
3. Stage S timing: mechanically after the lock (this draft) or before it as declared calibration (the v1.9 Stage 1 precedent)?
4. Canonical registry per early set: knives `brands_knives_v1.0.json` vs +v1.1; premium tea +v0.15; v0.6 registries (`registries/brands_<cat>.json`) vs v0.9's `osf_staging/v09/registries/`.
5. v0.24 phase B (72 frame answers, branch v0.36 only, mixed panel): include in the baseline (file and registry pinned from v0.36) or keep excluded?
6. H3 horizon: t1 → t2 alone as the gate's reliability leg, or both t1 → t2 and t2 → t3?
7. Gate treatment of a MARGINAL H2 alone: Pablo's decision (this draft) or FAIL?
8. v0.19 / v0.23 parity floor 0.98 against coded mention files; v0.23's inline registry should be written to a pinned file before the lock.
9. Confirm the archived LLM `brands_ranked` is a concordance check only, never a fallback extractor.
10. Phase numbering: v1.9 names v1.11 as the three-component calibration; the archive inventory names Sentiment Paper A v1.11.
11. v0.39 arm C model IDs ("as recorded") and the held-study rule in the paper (OSF yes, website no): confirm.
12. Check whether any early phase report already showed first-recommendation (`primary_recommendation`) shares; if so, declare it in Limitations.
13. Loaders in `score_v1_10.py` are TODO; an end-to-end dry run on a synthetic replica of each file format must pass before the lock (running on the real files would compute the statistics).
14. Shuffle null at 2,000 draws vs the program's 10,000 convention (compute time).
15. The development sample covers only legacy-panel frames; EARLY prompt types (identity, comparison) are not represented. The excluded v0.5 archive (67 answers) could serve as an EARLY-style parsing check if declared now.
