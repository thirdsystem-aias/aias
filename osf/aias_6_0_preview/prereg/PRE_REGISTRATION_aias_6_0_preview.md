# AIAS™ 6.0 Preview — the provisional six-part synthesis: pre-registration (analysis plan)

AIAS™ Measurement Program — Third System™. Pre-registration **r0, draft for review** (2026-11-10). To be locked at git tag `aias-6-0-preview-prereg-r1` and deposited on OSF (`osf.io/ec6wh`, folder `aias_6_0_preview/`) **before any t4-based component score exists** (§11). Nothing here reads a t4 answer or a t4 score: none exists (v0.42 locks no earlier than Wed 2026-11-11, about 3 pm CT, and collects after its lock).

**Pre-registrant:** Pablo Ulpiano González Castro

## 0. Status, scope and lineage

| Field | Value |
|---|---|
| PHASE_ID | AIAS 6.0 Preview (programme study list #68, per the coordinator's brief of 2026-11-10) |
| PHASE_TYPE | Synthesis of locked component scores with its own confirmatory structure tests. No collection, no model call, no spend (§12). |
| Decision of record | Pablo, Nov 9, 2026, 10:30 pm CT (CLAUDE.md, "Plan for speed"): per component, Paper A (instrument, baseline, separability gate) → Paper B only if A passes → release (calibration + synthesis); "The four Paper A's are built in parallel; an AIAS 6.0 Preview (provisional) follows them in December." Roadmap FAST TRACK (Nov 9): "a working six-part AIAS 6.0 Preview by ~Dec 18, 2026"; forecast "AIAS 6.0 Preview ~Dec 18–23, 2026". |
| Status | r0 draft on branch `aias-6.0-preview` (from `4643d56`, the v1.14 anchor commit). Not locked. Open items for r1 are listed in §16. |
| Locks on | content lock → `prereg/LOCK_MANIFEST_aias_6_0_preview.sha256` → commit → tag `aias-6-0-preview-prereg-r1` → push → `anchor/git_anchor_aias_6_0_preview.json` (tag object, commit, tree, tagger date, SHA-256 of every locked file) → OSF deposit of `prereg/`, `scoping/` and `anchor/`, SHA-256 verified → before the first t4-based component score (§11.1). |
| Consumes | t4 = v0.42 (Presence and Consistency on the newest models); v1.14 (Ranking, locked); v1.11 (Sentiment Paper A, locked) and a Sentiment score on the t4 answers that does not yet exist (§3.4); v1.12 (Coverage) and v1.13 (Grounding), both locking no earlier than Wed Nov 11 about 3 pm CT; AIAS 2.0 (legacy two-score profile); t5, the repeat of t4 (not yet pre-registered; §11.3). Each is used exactly as its own lock defines it. |
| Feeds forward | The Preview paper and Third System™ report (due about Dec 11–23, 2026); the calibration pre-registrations of the validated releases AIAS 3.0–6.0 (2027), which may cite the Preview's structure results but are not bound by them. |

**Lineage.** Foundational: *AI Availability* (SSRN 6659000); framework: MSI Working Paper 26-132. Presence: v1.2–v1.6 (SSRN 6761698, 6797679, 6799479, 6810758, 6816340), AIAS 1.0 (SSRN 6817841), construct validity v0.29 (SSRN 6870778). Consistency: v1.7 (SSRN 6878818; the instrument that moved with naming frequency), v1.8 (SSRN 6963359; φ), v1.9 (SSRN 7685126; C\*, no composite), v0.41 (SSRN 7685100; t3). **AIAS 2.0** (published 2026-11-10; tag `aias-2-0-paper-locked-r2`): Presence and Consistency reported as two scores side by side, no composite; its outline was deposited on OSF before any t3 score existed, the precedent this document follows. Ranking: v1.10 Paper A (gate MARGINAL, published as a negative result) and its redesign v1.14 (modal position; tag `v1.14-prereg-r1`, locked and deposited 2026-11-10). Sentiment: v1.11 (tag `v1.11-prereg-r1`; AI-judged, provisional until human labels). Coverage: v1.12. Grounding: v1.13.

**Construct.** The framework names six parts of AI Availability: whether a brand is named (Presence), how evenly models name it (Consistency), where it sits in an answer's list (Ranking), how answers describe it (Sentiment), across how many buying situations it is named (Coverage), and what the answers rest on when search is on (Grounding). Each part's Paper A tests it against Presence and Consistency (and, where locked in time, against the others). The Preview asks the question no Paper A can: **on one panel and one wave, are the parts that passed their own gates still separate from each other when all of them are measured on the same brands?** It is provisional by design: it comes before any Paper B and before the validated releases.

## 1. Purpose and claims

### 1.1 What the Preview will claim (each tied to the verdict that governs it)

- **C1 Profile.** For each of the 112 omnibus brand units, the Preview reports up to six provisional scores, measured on the newest models (panel N3) in the t4 week, each with the label its gate state gives it (§4, §5). Governing: the component gate states (§4.1).
- **C2 Structure.** The included components are separate readings of a brand, not copies of one another: stated as the number of separable parts and which overlap, if any. Governing: H_Structure (§6.5).
- **C3 AIAS 2.0 off the legacy panel.** Presence and Consistency stay separable on the newest models. Governing: H_PC_N3 (§6.2), the first test of AIAS 2.0's separability claim outside the retiring panel.
- **C4 Who carries a full profile.** Which units are rated on all included parts, and how that set is stratified (§8). Descriptive.

### 1.2 What the Preview will not claim

Not a validated component (each stays provisional until its Paper B and its release calibration); not a composite 0–100 score (§7); not a validity claim against behaviour (predictive validity is the 2027 validation track); not panel-general (N3 only; three models, one per provider); no level comparison with published AIAS 2.0 values (§7.3); no model ranking; no new instrument, floor or rating rule.

### 1.3 Research questions

- **RQ1 (structure).** On N3 at t4, is every included component separable from every other (pairwise), and does each add information beyond the components that precede it in the programme (incremental)?
- **RQ2 (carry-over).** Does AIAS 2.0's Presence–Consistency separability hold on N3?
- **RQ3 (coverage).** How many units carry a complete profile, and how is that set stratified by category, registry cell and Presence?
- **RQ4 (descriptive).** Would any equal-weight composite of the included parts pass v1.9's constraints on N3?
- **RQ5 (descriptive).** How do the scores move from t4 to t5 where t5 allows?

## 2. Units, panel, wave and conventions

- **Units.** The 112 brand units of the five omnibus registries (v0.19 audiophile headphones 16; v0.20 skincare, v0.21 cosmetics, v0.22 automotive, v0.23 premium spirits 24 each), unchanged since t1 and identical in v0.42, v1.12, v1.13 and v1.14. Rare Beauty is two units (v0.20 and v0.21), as in every source. No brand is added, removed or renamed. Unit key: (substrate, brand) as the sources write it; the Preview joins on it and halts unless every input carries the same 112 keys (MQ_Join, §11.2).
- **Panel.** N3 = Claude Fable 5.2 (`claude-fable-5-2`), GPT-6 Astra (`gpt-6-astra`), Gemini 4 Argon (`gemini-4-argon`), the newest generally available flagship of each provider, verified in v0.42 §4.3. The six-part profile exists on N3 only: the retiring six-model panel can never carry Coverage (no buying-situation questions were asked of it) or Grounding (it never searched).
- **Wave.** t4 = v0.42 (category and brand questions, collected after its lock, within 72 hours and before Nov 17; v0.42 r2). Coverage comes from v1.12's own collection on the same three models in the same week (window from 2026-11-14 00:00 UTC; v1.12 §6.7). The Preview calls both "the t4 week" and treats them as one wave; the gap is a limitation (§13).
- **Condition.** Search off (S0) for Presence, Consistency, Ranking, Sentiment and Coverage; search on (S1) for Grounding, which is defined on search-on answers (v1.13 §0). Search-on versions of the others are descriptive (§10, SH).
- **Orientation.** Every score is oriented so that higher means more of the reading: higher P = named more; higher C\* = models agree more; higher R\* = nearer the top of the list; higher S = described more favourably; higher Cov\* = named across more buying situations than its naming rate implies; higher G\* = answers rest more on the brand's own domain. Signs are reported; separability verdicts use |ρ|.
- **ρ_w.** Pooled within-category Spearman with ranks **centred** on each category's mean rank (v1.10 §7; v1.12 §2.5; v0.42 clarification C25), computed by `score_v1_10.pooled_within_rho`, imported unchanged (git blob `0f8b981b2895a325b50629c85f8e0e6ce8e876f5`, byte-identical to tag `v1.10-prereg-r2`). A category enters a statistic only with ≥ 5 units in that comparison. **n floor:** UNDETERMINED with fewer than 30 units pooled or fewer than 3 categories entering (v1.12 §2.5). Values compared unrounded.
- **Permutation p.** First-named variable permuted within category, 10,000 draws, p = (hits + 1)/(N + 1); two-sided for separability, one-sided for the I-tests (on R²). **Bootstrap:** units resampled within category, 2,000 draws, 90% percentile interval; reported, never a verdict input.
- **Seeds.** S-tests 600001–600015 (§6.2 table order); I-tests 600021–600025; bootstrap 600030; parallel analysis 600040; synthetic precision note 600900.
- **Bands (the programme's).** Separability: |ρ| ≤ 0.30 CONFIRMED, |ρ| ≥ 0.50 FALSIFIED, between MARGINAL. Retest (descriptive here): ρ ≥ 0.50 stable, < 0.30 not.

## 3. The six components: score, data, locked source

The Preview computes no component score of its own. It reads each unit-level score from that component's scored output, checks the file's SHA-256 against the component's own record (verdict file or output manifest), and uses the component's own rated set. Units a component leaves NOT RATED are never imputed. Presence and Consistency are the only scores the Preview recomputes, with v1.14's locked function, as a parity check (MQ_Parity, §11.2).

| Part | Score in the Preview | Data | Read from | Lock |
|---|---|---|---|---|
| **Presence** | P_S0 = 100·(C_P/3 + 2·π̂_N3,S0)/3; C_P/3 = share of N3 models coding the brand recognized in their one S0 brand answer (the definition shared by v1.12 §2.6, v1.13 §2.2 and v1.14 §5.2; `score_v1_14.comparators`). Defined for every unit with a coded brand answer. | t4 category answers S0 (3 models × 6 questions × 3 runs per category) and brand answers S0 (one run) | `osf/v42/v42_brand_table.csv` (`pi_N3_S0`) and `osf/v42/data/coded/*_phase_a.csv` at v0.42's scored commit; raw answers at tag `v0.42-acquisition-locked` | protocol v1.6; `v0.42-prereg-r1` (pending) |
| **Consistency** | C\*_S0 = 100·(1 − φ_N3,S0/9) when v0.42's partition is `defined`; 100 when `saturated`; NOT RATED when `zero` or `undefined`; rated only with ≥ 6 N3 S0 category-answer mentions (shared definition, as above) | as Presence | `osf/v42/v42_brand_table.csv` (`phi_N3_S0`, `phi_partition_N3_S0`) and `osf/v42/data/coded/*_phase_b.csv` | v1.8 φ; v1.9 C\* (tag `v1.9-prereg-r1`); `v0.42-prereg-r1` (pending) |
| **Ranking** | R\*_S0 = v1.14's modal position (higher = nearer the top), rated at ≥ 6 rankable mentions | t4 category answers S0 | `osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json`, `units[]` fields `R_star_S0`, `rated_S0` (Stage 1, scored once); the final gate from the Stage 2 output when it exists | `v1.14-prereg-r1` (locked 2026-11-10; anchor commit `4643d56`) |
| **Sentiment** | S_t4 = v1.11's score (mean unit score of the brand's mention windows, rated at ≥ 6 valid units) applied to the t4 answers, **if** a t4 Sentiment score is pre-registered and locked (§3.4); otherwise the Preview has no Sentiment score on N3 | t4 category answers S0 (proposed) | the t4 Sentiment study's own scored output (path fixed in its pre-registration) | `v1.11-prereg-r1` (instrument; locked); the t4 extension: not yet pre-registered |
| **Coverage** | Cov\* = v1.12 §2.4 (breadth across 14 buying situations against a situation-blind null; 50 = situation-blind), rated at ≥ 14 mentions and ≥ 2 of 3 models | v1.12's own S0 collection on the same models (75 probes; 900 calls including its Claude Opus 5.5 continuity arm; Cov\* uses the N3 answers) | v1.12's scored unit table (column `cov_star_N3`) and verdict file; exact paths pinned at r1 (§16) | `v1.12-prereg-r1` (pending) |
| **Grounding** | G\* = 100 × own-domain share of the grounded S1 answers naming the brand, rated at g_b ≥ 6 and only for units with a recorded own domain | t4 category answers S1 (their search records) | v1.13's `v1_13_verdicts.json` and unit table (Stage C1; Stage C2 appends); exact paths pinned at r1 (§16) | `v1.13-prereg-r1` (pending) |

### 3.1 What the Preview takes from each source and nothing else

The unit-level score, its rated flag, the component's gate verdict (§4.1) and, for the pairs a Paper A has already tested, that Paper A's statistic and verdict (§6.2). Floors, extractors, judges, nulls and drop rules are the sources'. If a source's scored output does not carry a unit-level score the Preview needs, the Preview does not compute it: the component is NOT RUN for the Preview until the source writes it (a deviation entry in the source, not here).

### 3.2 Presence and Consistency: the legacy series and the new panel

AIAS 2.0 published P and C\* on the retiring six-model panel (t1–t3). Its separability record (`osf/aias_2_0/aias_2_0_synthesis_data.json`, tag `aias-2-0-data-locked`, commit `94f6618`, SHA-256 `675b6963…`): ρ(C\*, P) = 0.073 (t1, n = 55), 0.082 (t2, n = 54), 0.189 (t3, n = 54), under the uncentred pooled-rank convention it published; C\* not rated for 0.509, 0.518 and 0.518 of the 112 units. On N3, P and C\* follow the shared definition above. C\*_N3 is scaled with φ_max = 9 (three models), not 7.2 (six), so its **levels** are not comparable with the published C\* (AIAS 2.0 outline, Claim 8); only rank statistics bridge the two (§7.3). Whether the brand order carries over is v0.42's question (H_Gen_Presence, PRIMARY; H_Gen_Phi, SECONDARY) and sets the bridge label (§4.1).

### 3.3 Ranking: which statistic

R\* is v1.14's modal position. v1.10's mean normalised position (MNP) failed to clear separability from Presence on the archived waves (gate MARGINAL: ρ_w(R\*, P) = 0.275, 0.366, 0.307 at t1, t2, t3, n = 55, 54, 54; `osf/methodology/v1_10/outputs/v1_10_verdicts.json`, branch `v1.10` commit `7b7377a`, SHA-256 `d4250ba7…`, pinned in the `v1.14-prereg-r1` lock manifest) and is not a Preview score; MNP at t4 enters only sensitivity SF. The modal position was chosen after its archived values were seen (v1.14 §1), so its t4 values are its first confirmatory evidence.

### 3.4 Sentiment on the newest models: a dependency

v1.11 scores the archived waves only (legacy six-model panel and the early-category panel). The v1.14 anchor records `"score_defined_on_N3_at_t4": false` for Sentiment (`osf/methodology/v1_14/anchor/git_anchor_v1_14.json`), and v1.12 (H6) and v1.13 (H5) withdrew their cross-panel fallback, keeping their Sentiment legs inactive until a Sentiment score on the t4 answers is pre-registered. A six-part profile on one panel therefore needs **a separate, small pre-registration** that applies v1.11's locked instrument unchanged (window rule, judge, prompt, scale, rating floor) to the t4 N3 S0 category answers, locked before its first judge call. It is not part of this document: it is paid work outside a locked study and needs Pablo's go (Choice 1, §17; cost estimate §12).

**Rule.** If S_t4 is locked and scored by the Preview's data lock, Sentiment is a full member of the profile with the gate state of §4.1. If not, Sentiment is reported beside the profile as a separate reading on the legacy panel (v1.11's S at t3), labelled "legacy panel; not on the Preview panel", and enters **no** structure test; the structure verdict then covers at most five parts and the headline says so (§6.6).

## 4. Gate-status rules

### 4.1 How the Preview reads each component's gate (fixed now, before any of these verdicts exists on t4)

- **Presence.** The published component (AIAS 1.0, protocol v1.6; construct-valid, v0.29). Always in the profile. **Bridge label** from v0.42's H_Gen_Presence: CONFIRMED → "continues the published series"; MARGINAL → "partly continues the published series"; FALSIFIED → "new series on the newest models; not comparable with published values"; UNDETERMINED → §4.3.
- **Consistency.** The AIAS 2.0 component (v1.9 Stage 2; AIAS 2.0 outcome class A). In the profile; its separability from Presence on N3 is the Preview's own test H_PC_N3 (§6.2). Bridge label from v0.42's H_Gen_Phi, worded as for Presence.
- **Ranking.** v1.14's final GATE (after Stage 2) if it exists at the Preview's data lock; otherwise v1.14's interim verdict after Stage 1, read as: SEPARABLE → **PASS, retest pending**; MARGINAL → MARGINAL; FAIL → FAIL; UNDETERMINED → UNDETERMINED.
- **Sentiment.** v1.11 states PRIMARY hypotheses but no single gate verdict. The Preview reads them with the rule its sister Paper A's use (v1.12 gate steps 2–5; v1.14 §8): **FAIL** if any of H1_Judge_Agreement, H2_Sep_Presence, H3_Sep_Consistency, H4_Stability_Short or H5_Sep_Ranking is FALSIFIED; else **UNDETERMINED** if any is UNDETERMINED; else **PASS** if all are CONFIRMED (H5 still PENDING under v1.11 §5 → **PASS, Ranking leg pending**); else **MARGINAL**. Every Sentiment PASS carries "AI-judged; human-label check pending" until Sentiment Paper B (human labels from SVA MPS Branding students; due Dec 4, 2026 on the timeline Pablo set on Nov 10, recorded in `STATUS.md`; v1.11 §9's planning date was about Jan 22, 2027) confirms the instrument under its own pre-registration. When Paper B's verdict exists (§4.4): a pass removes the "AI-judged" qualifier (row PASS); a failure moves Sentiment to the FAIL row (not shown; one sentence with Paper B's result); any other Paper B verdict leaves the qualifier and is printed beside it. Two further conditions, both fixed now: the S_t4 study (§3.4) must pass its own checks as its pre-registration states, and its separability from Presence and Consistency on N3 is tested here (§6.2), not assumed from the archived waves.
- **Coverage.** v1.12's GATE (INSTRUMENT FAIL, FAIL, UNDETERMINED, PASS, MARGINAL) as last issued before the data lock.
- **Grounding.** v1.13's GATE as last issued before the data lock (a Stage C2 re-issue can only downgrade it).

### 4.2 What the Preview does in each state

| Gate state at the data lock | In the profile | Label (§5) | Structure tests (§6) | Composite check (§7.2) |
|---|---|---|---|---|
| PASS | shown | provisional | included (confirmatory) | included |
| PASS, retest pending (Ranking before v1.14 Stage 2) | shown | provisional; retest pending | included | included, flagged |
| PASS, AI-judged (Sentiment before its human-label check) | shown | provisional; AI-judged, human-label check pending | included | included, flagged |
| MARGINAL | shown in a separate band below the profile | under review: the marginal leg named | computed and printed as descriptive; not counted in any verdict | excluded |
| FAIL or INSTRUMENT FAIL | not shown | none (one sentence in the text: negative result, with its paper) | excluded (its correlations printed in an appendix table, descriptive) | excluded |
| UNDETERMINED | not shown | "not determined", with the data cause | excluded | excluded |
| NOT RUN (no scored output by the data lock) | not shown | "pending" | completed in a dated addendum when the score exists, before the paper lock (§4.4) | excluded |

Presence and Consistency are always included. The **included set K** = {P, C\*} plus every component in one of the three PASS rows; k = |K|, at most 6.

### 4.3 Panel completeness

If v0.42's drop rule excludes any N3 model in S0 (fewer than 90% of its calls answered; v0.42 §5.4), v0.42's primary test and v1.14's Stage 1 are UNDETERMINED. The Preview then runs **no** structure test: it reports the AIAS 2.0 legacy profile, the Paper A verdicts and the cause, and H_Structure is UNDETERMINED. A reduced panel inside one component (v1.12 §7.3; v1.13 MQ2 or MQ4) travels with that component as the label "reduced panel"; it does not change the rules above.

### 4.4 Later verdicts (addenda)

A gate that changes after the data lock — v1.14's final gate after Stage 2, a v1.13 Stage C2 re-issue, Sentiment Paper B's validation verdict, a NOT RUN component's first score — produces a **dated addendum**, only before the paper lock: the component moves to its new row of §4.2, K is updated, every test of §6 that involves the changed component is computed or dropped, H_Structure is recomputed by the same rules, and both the original and the updated verdicts stay on record. No other analysis is redone, and nothing is changed after the paper lock (later changes go to the validated release).

### 4.5 Programme order

Where a rule needs an order, it is the order in which the components entered the programme and will be released: Presence (AIAS 1.0) → Consistency (2.0) → Ranking (3.0) → Sentiment (4.0) → Coverage (5.0) → Grounding (6.0) (roadmap, phases N–R). A later component has to add information to the earlier ones, as each Paper A requires of its component against Presence and Consistency; the earlier component keeps its place.

## 5. Provisional labels

- **Title of every output:** "AIAS™ 6.0 Preview (provisional)". Every table, figure caption and headline carries "provisional".
- **Component labels:** exactly the label column of §4.2, plus the bridge labels of §4.1 for Presence and Consistency and "reduced panel" where §4.3 applies.
- **Words.** The parts are "provisional components" (they are parts of the score, not study readings; messaging standard, Nov 9, 2026). The six-part 0–100 score is described only as what AIAS will be "when complete"; the Preview never calls any part validated and never prints a single AIAS 6.0 number per brand.
- **Validation status line** (printed once in every output): "Presence is the published AIAS component and Consistency its second (AIAS 2.0). Ranking, Sentiment, Coverage and Grounding are provisional: the profile shows each with the state of its first test; none has completed its validation."

## 6. Six-score structure analyses (confirmatory)

### 6.1 Unit sets

- **Pairwise-complete set** of a pair (X, Y): the units with both scores rated (P defined).
- **Incremental set U_≤X:** for the I-test of X (§6.3), the units rated on X and on every member of K that precedes X in programme order (§4.5). Later members do not restrict it, so each I-test uses every unit that can inform it. Each I-test has its own n floor (§2); below it, that I-test is UNDETERMINED.
- **Complete-profile set U_K:** the units rated on every member of K (= U_≤X for the last member of K). It is the set of "brands that carry the full profile" (§8) and the basis of descriptives D2–D3 and sensitivity SD.

### 6.2 Pairwise separability (S-tests)

Every pair of K is tested with ρ_w on its pairwise-complete set (§2 conventions and bands). **Carried pairs:** where a component's Paper A has issued a verdict on exactly the same statistic (same two scores, same condition, same rated units), the Preview carries that verdict and recomputes the statistic as a parity check (MQ_Parity: equal within 10⁻⁹, else the run halts). **Every other pair is the Preview's own PRIMARY test.** The (P, C\*) pair is named **H_PC_N3**.

| Seed | Pair | Expected source of the verdict (when both members are in K) |
|---|---|---|
| 600001 | P × C\* (**H_PC_N3**) | Preview (no Paper A tests it on N3; v0.42 reports only φ's mean-independence) |
| 600002 | P × R\* | carried: v1.14 H1_Sep_Presence |
| 600003 | C\* × R\* | carried: v1.14 H2_Sep_Consistency |
| 600004 | P × S | Preview |
| 600005 | C\* × S | Preview |
| 600006 | R\* × S | Preview |
| 600007 | P × Cov\* | carried: v1.12 H1_Sep_Presence |
| 600008 | C\* × Cov\* | carried: v1.12 H2_Sep_Consistency |
| 600009 | R\* × Cov\* | carried: v1.12 H5_Sep_Ranking when it gated (v1.14 Stage 1 SEPARABLE); else Preview |
| 600010 | S × Cov\* | Preview |
| 600011 | P × G\* | carried: v1.13 H1_Sep_Presence (its S0 leg is this pair; v1.13's verdict covers both legs and is the one carried) |
| 600012 | C\* × G\* | carried: v1.13 H2_Sep_Consistency (as above) |
| 600013 | R\* × G\* | Preview: v1.13 H4 pairs G\* with the search-on R\*_S1; the profile uses R\*_S0. v1.13 H4 is printed beside it |
| 600014 | S × G\* | Preview |
| 600015 | Cov\* × G\* | carried: v1.13 H6_Sep_Coverage when active and computed; else Preview |

S-test verdicts: CONFIRMED |ρ_w| ≤ 0.30; FALSIFIED |ρ_w| ≥ 0.50; MARGINAL otherwise; UNDETERMINED below the floor. Each row prints ρ_w, n, categories entering, two-sided permutation p and the 90% bootstrap interval.

### 6.3 Incremental separability (I-tests)

Pairwise separability can hold while a part is predictable from a combination of earlier parts. The I-test is the guard. For each X in K other than P, in programme order (§4.5): on U_≤X (§6.1), the centred within-category ranks of X (ranks recomputed within the set; categories with ≥ 5 units; c = categories entering) are regressed by least squares on the centred within-category ranks of the members of K that precede X (j predecessors; no intercept, the ranks are centred within category). R² = 1 − SSR/SST; **R²_adj = 1 − (1 − R²)·(n − c)/(n − c − j)**; **R_adj = √max(0, R²_adj)**. Verdict with the programme's separability bands: **CONFIRMED iff R_adj ≤ 0.30; FALSIFIED iff R_adj ≥ 0.50; MARGINAL otherwise; UNDETERMINED below the floor.** A one-sided permutation p (X's ranks permuted within category, 10,000 draws, seeds 600021–600025 for C\*, R\*, S, Cov\*, G\*) is reported. For C\* (j = 1), U_≤C is H_PC_N3's own set, and the I-test is the adjusted form of that correlation.

The bands are the pairwise ones on purpose: a part must be as separable from the earlier parts taken together as from any one of them. Because the adjustment charges every predecessor, one strong overlap can be diluted in the I-test; the S-tests catch single overlaps and the I-test catches combinations, and §6.4 reads them together.

### 6.4 Component status

For each X in K other than P (P is the anchor):

- **NOT DISTINCT** if an S-test between X and an **earlier** member of K is FALSIFIED, or X's I-test is FALSIFIED. A FALSIFIED pair marks only its later member (§4.5).
- **DISTINCT** if every S-test between X and an earlier member is CONFIRMED and X's I-test is CONFIRMED.
- **UNDETERMINED** if neither applies and at least one of those tests is UNDETERMINED.
- **PARTLY DISTINCT** otherwise (no FALSIFIED, none UNDETERMINED, at least one MARGINAL).

### 6.5 H_Structure (PRIMARY; the headline test)

Let d = the number of members of K that are DISTINCT or PARTLY DISTINCT, counting P as DISTINCT, and u = the number that are UNDETERMINED.

| Verdict | Condition |
|---|---|
| **UNDETERMINED** | §4.3 applies, or k < 3, or fewer than three members of K have a determined status (k − u < 3) |
| **CONFIRMED** | every member of K other than P is DISTINCT |
| **FALSIFIED** | d ≤ 2 and u = 0: the parts measured reduce to at most two separable readings on the newest models |
| **PARTIAL** | otherwise |

Printed with the verdict: k, d, the members in each status, and every MARGINAL, FALSIFIED or UNDETERMINED test behind them. MARGINAL components (§4.2) are not in K; their tests against K are printed as descriptive rows.

### 6.6 Wording fixed before t4 (the AIAS 2.0 outline's §5 pattern)

| Class | Condition | Headline wording | What changes in the paper and report |
|---|---|---|---|
| **A** | H_Structure CONFIRMED, k = 6 | "On the newest models, the six provisional parts of AI Availability are six separate readings of a brand." | full claim set |
| **A_k** | CONFIRMED, k < 6 | "On the newest models, the k provisional parts measured so far are separate readings of a brand; [parts] are [pending / under review / not passed]." | missing parts named with their state |
| **B** | PARTIAL | "On the newest models, d of the k parts measured are separate readings of a brand; [part] overlaps [part] (ρ = …)" and/or "[part] is only partly separable from [parts]". | every included part stays in the profile with its status; the overlaps become the first question of the next release calibration |
| **C** | FALSIFIED | none: **drafting pauses** | Claude writes a one-page options memo (for example a qualified Preview, a hold for t5, or the overlapping parts back to redesign); a change of direction, so Pablo decides |
| **U** | UNDETERMINED | "On the newest models, how the parts relate could not be determined: [cause]." | the profile is shown with its labels; no structure claim |

Rules in every class. **W1** H_PC_N3 is reported in every class: CONFIRMED → "Presence and Consistency stay separable on the newest models"; MARGINAL → "… separable, with moderate coupling (ρ = …)"; FALSIFIED → "on the newest models Consistency moves with Presence (ρ = …); AIAS 2.0's separability is shown on the retiring panel only". **W2** Without S_t4 (§3.4) the headline counts the parts on N3 and names Sentiment's separate legacy-panel reading. **W3** Every Ranking sentence carries "retest pending" until v1.14's final gate exists (§4.4). **W4** Sensitivities and descriptives never change the class (§10). **W5** No statistic beyond those pre-registered here enters a confirmatory sentence; anything else is labelled exploratory and listed in the data lock before it is computed (the AIAS 2.0 outline's rule R7).

### 6.7 Precision (synthetic; declared before any t4 value exists)

- **S-tests** (v1.14 §7, analytic, `osf/methodology/v1_14/calibration/calibration_v1_14.json` → `precision_note`, tag `v1.14-prereg-r1`): one ρ_w at n = 40 rated units is CONFIRMED with probability 0.94 / 0.89 / 0.74 / 0.63 when the true value is 0 / 0.10 / 0.20 / 0.25, and FALSIFIED with probability 0.04 at 0.25; at n = 55, 0.97 / 0.93 / 0.78 / 0.65 and 0.02.
- **I-tests** (`prereg/precision_aias_6_0_preview.json`, made by `scoping/precision_aias_6_0_preview.py`, synthetic data only, seed 600900, 4,000 replications per cell, five categories): with five predecessors and no true overlap, CONFIRMED with probability 0.821 (n = 40) and 0.903 (n = 55), FALSIFIED 0.016 and 0.003; when the predecessors jointly carry 9% of a part's rank variance, CONFIRMED 0.637 and 0.628, FALSIFIED 0.071 and 0.040; at 25%, FALSIFIED 0.303 and 0.292 (MARGINAL most often); at 49%, FALSIFIED 0.778 and 0.863. Looser bands (0.50 / 0.70) were computed in the same run and rejected: at 49% shared variance they would falsify with probability 0.18 and 0.17 only.
- **Consequence, stated in advance.** CONFIRMED needs every one of the Preview's own S-tests and every I-test in the CONFIRMED band. With seven pairs of its own (all with S_t4 in K) at a true ρ of 0.10 each and n = 40, the chance that all seven are CONFIRMED is about 0.89⁷ ≈ 0.44 if the tests were independent. PARTIAL is therefore a likely outcome even when every true overlap is small; the class-B wording names the marginal pairs with their values so that a reader can tell a small overlap from a large one (Choice 3, §17, offers a lenient rule instead).

## 7. The profile and the calibration question (building on AIAS 2.0; v1.9's approach)

### 7.1 A profile, as AIAS 2.0

AIAS 2.0 reports Presence and Consistency side by side and publishes no composite, because v1.9 Stage 1 found no 0–100 combination that both adds information to Presence and keeps Consistency separate. The Preview extends that form: **k scores side by side per brand, no composite.** Any composite is a decision for the validated releases (AIAS 3.0–6.0), each under its own calibration pre-registration with a blind confirmation wave, as v1.9 had t3.

### 7.2 v1.9's constraints, extended and computed as a descriptive check (never adopted)

- **A_K(b)** = the mean of brand b's rated scores over the members of K (P always present; members not rated for b drop out of the mean), v1.9's ADD rule with its fallback, on every unit with P defined.
- **K1_K (separation):** H_Structure not FALSIFIED and H_PC_N3 not FALSIFIED.
- **K2_K (adds information):** |ρ_w(A_K, P)| ≤ 0.95 over all units with P.
- **K3_K (no windfall):** mean A_K over units with 1–2 N3 S0 category-answer mentions minus mean A_K over units never named there ≤ the same difference in P plus 5 points.
- Also: A_K restricted to the complete-profile set (v1.9's FLOOR analogue) with K2 inside that set; and each member's share of A_K's within-category variance.
- Output: "would / would not pass v1.9's constraints", per constraint. No candidate is selected and nothing is adopted.

### 7.3 Continuity with the published two-score set (descriptive)

The AIAS 2.0 legacy profile (P and C\* at t3, `osf/aias_2_0/aias_2_0_profiles.csv`, tag `aias-2-0-data-locked`; SHA-256 `022ef56e…`, also pinned in the `v1.14-prereg-r1` lock manifest) is printed beside the N3 profile, never pooled with it. Bridge statistics on units with both: ρ_w(P_L6,t3, P_N3,t4) with the mean level shift of P (bootstrap interval), and ρ_w(C\*_L6,t3, C\*_N3,t4) without a level comparison (φ_max differs, §3.2). They are the score-level companions of v0.42's confirmatory bridge tests on π̂ and φ, whose verdicts set the labels (§4.1).

### 7.4 Why no composite in the Preview

(i) v1.9 Stage 1 found that floored composites rank brands almost exactly as Presence does: ρ(A, P) = 0.971–0.997 (`osf/methodology/v1_9/prereg/v1_9_two_component_composite_content.py`, `STAGE1_RESULT`, tag `v1.9-prereg-r1`), and the AIAS 2.0 data lock reproduced it at t3 (ρ(A, P) = 0.969, `aias_2_0_synthesis_data.json`, `summaries.t3.rho_A_P_descriptive`, tag `aias-2-0-data-locked`). Bounded parts that sit high on their scales average into a copy of Presence. (ii) Four of the six parts are provisional. (iii) A composite chosen on t4 would need a blind confirmation wave; t6 (target 2027-02-12, v0.42 §6) is available to the validated releases.

## 8. Brand coverage and stratification (descriptive)

- **Rated parts per unit:** 0 to k (and 0 to 6 including MARGINAL parts), per category and per registry cell where the registry records cells.
- **Who carries all six:** the list of units in U_K (and in the six-part set, if k = 6), by category.
- **Selection on Presence:** rated share of each part by within-category Presence tercile (P_S0); P and mention-count distributions of U_K against the 112. Every rating floor requires a brand to be named, so the complete-profile set leans to well-named brands; the S-tests are therefore also recomputed on U_K (sensitivity SD) to show what the restriction does.
- **Reported apart:** the COI-flagged unit of v0.19 (Declarations); the five v0.22 brands of the registry's "Defunct" cell, for which G\* is not rated by rule (v1.13 §2.3, D5); the two Rare Beauty units.
- **By model panel:** a table of which parts exist on which panel and wave (legacy six-model panel t1–t3: P, C\*, v1.10's Ranking statistic, v1.11's Sentiment; N3 t4 week: all six if S_t4 exists). Only N3 carries a six-part profile.

## 9. Exclusions

- **Data.** Only the 112 omnibus units on N3 in the t4 week, plus the AIAS 2.0 legacy profiles for the bridge (§7.3) and v1.11's legacy Sentiment if S_t4 does not exist (§3.4). Not used: the early-category panels of v1.10 and v1.11 (no Coverage or Grounding exists there); v0.40 (its own study; its search-on answers belong to Grounding Paper B); the technology panel of v0.28 (excluded pending its own COI screen, as in v1.11); the programme's two held studies (never made public); v0.44 and v0.62 (other studies, other brands).
- **Units.** None excluded from the primary analysis. A unit a part does not rate leaves every test involving that part; nothing is imputed. The COI-flagged v0.19 unit stays in the primary analysis, as in every source, and every structure statistic is also reported without it (SA).
- **Calls and models.** Each source's exclusions as that source locks them (unanswered calls as missing cells, served-model mismatches, drop rules). The Preview re-decides none.
- **Components.** By gate state (§4.2).

## 10. Descriptives and sensitivities

**Descriptives (no verdicts).** D1 rated counts and score distributions (median, IQR, range) per part and category. D2 the full k × k ρ_w matrix on pairwise-complete sets, with n and 90% intervals, and the same matrix on U_K. D3 eigenvalues of the U_K rank-correlation matrix, the effective number of dimensions (participation ratio (Σλ)²/Σλ²) and a parallel analysis (1,000 within-category permutations of each part, seed 600040); descriptive only. D4 the per-unit profile table (every part, its rated flag and label; CSV) and within-category rank profiles. D5 the bridge table (§7.3). D6 t4 → t5 retest of each part where t5 allows (R\*: v1.14 H3 as issued; P: π̂ retest, and P if t5 codes brand answers; C\*: if t5 has its three S0 runs; G\*: if t5 collects S1; Cov\*: none unless Coverage is re-asked under its Paper B). D7 the search-on profile (P_S1, C\*_S1, R\*_S1 with G\*) as a matrix. D8 the composite check (§7.2). D9 the coverage tables (§8).

**Sensitivities (reported next to the verdicts; never change one; every verdict change is listed beside the verdict).** SA without the COI-flagged v0.19 unit. SB uncentred pooled ranks (the v0.37–v0.41 convention). SC leave one category out (range of every S-test, I-test and of H_Structure). SD every S-test on U_K. SE H_Structure without Sentiment (the only AI-judged part), if Sentiment is in K. SF Ranking by v1.10's MNP at t4 (as v1.14's descriptives compute it) in place of R\*. SG Sentiment from the legacy panel (v1.11's S at t3) in place of S_t4, cross-panel and descriptive. SH search-on variants (P_S1, C\*_S1, R\*_S1) in place of the S0 scores, with G\* unchanged.

## 11. Order of operations and what must exist before the Preview runs

### 11.1 Lock (blind to t4)

This document is locked and anchored (§0) **before any t4-based component score exists**. The first such score is v0.42's own scoring of t4 (its scored commit: π̂ and φ on N3), followed by v1.14 Stage 1, v1.13 Stage C1 and v1.12's scoring. **Latest safe lock: the earlier of Sat 2026-11-14 (end of day, CT) and the first run of v0.42's scorer on t4 data.** Because t4 may finish collecting well inside its 72-hour window, the recommended lock is Wed Nov 11 or Thu Nov 12, with the other locks. The scorer checks blindness at run time (MQ_Blind below).

### 11.2 Inputs and checks at the data lock

Each input is read with `git show` from its scored reference and logged with its git blob and SHA-256 in `outputs/inputs_read_aias_6_0_preview.json`:

1. v0.42: tag `v0.42-acquisition-locked` (raw answers) and the scored commit (brand table, coded tables, `v42_verdicts.json`: H_Gen_Presence, H_Gen_Phi, drop rule).
2. v1.14: `stage1_v1_14.json` (interim verdict, units with R\*_S0, P_S0 and C\*_S0) and, when it exists, the Stage 2 output (final gate).
3. v1.12: its verdict file (GATE) and unit table with `cov_star_N3`.
4. v1.13: `v1_13_verdicts.json` (GATE; C2 appendix if issued) and its unit table with G\*.
5. v1.11: Stage J and Stage C outputs (H1–H5; for the gate reading of §4.1); Sentiment Paper B's verdict if it exists.
6. S_t4: the scored output of the t4 Sentiment study, if it is locked and scored (§3.4).
7. AIAS 2.0: `osf/aias_2_0/aias_2_0_profiles.csv` at tag `aias-2-0-data-locked` (§7.3).

Checks (each halts unless stated):

| Id | Check | Rule |
|---|---|---|
| MQ_Lock | The lock | tag `aias-6-0-preview-prereg-r1` and the anchor file exist; every file in the lock manifest is unchanged |
| MQ_Blind | Blind to t4 | the tag's date precedes the first commit of every t4-based input score file (v0.42's brand table, v1.14's Stage 1 output, v1.12's and v1.13's unit tables, S_t4). If not: the Preview's own tests on that input are labelled exploratory, a DEVIATIONS entry records it and Pablo is told (no halt) |
| MQ_Join | Units | every input carries the same 112 unit keys, 1:1 |
| MQ_Parity | Comparators | P_S0 and C\*_S0 recomputed with `score_v1_14.comparators` from v0.42's files equal the values in v1.14's Stage 1 units exactly; every carried pair's ρ_w (§6.2) equals the Paper A's value within 10⁻⁹ |
| MQ_Panel | Panel | v0.42's drop rule keeps all three N3 models in S0 (else §4.3; no halt) |
| MQ_Gate | Gate states | each component's gate state is read by §4.1 and written to the output before any structure statistic is computed |

### 11.3 What t5 must contain (t5 is not yet pre-registered)

- **Required by the Preview** (because v1.14's final gate needs it; v1.14 §6): the 30 category questions verbatim (`osf/v42/prereg/probes_v0_42.jsonl`); the same three model IDs where available; search off (S0); three runs; the same decoding (provider defaults, output cap 16,384 tokens), call modes, call policy and raw-file schema; an `-acquisition-locked` tag. A newer model may be an extra arm only.
- **Wanted for the descriptive retests (D6), not required:** the 112 brand questions in S0, one run, with a successor to the v0.23 recognition judge and a parity check against the t4 codes (Claude Sonnet 4.5 retires on 2026-11-30; v0.42 §6), so that P_t5 exists; the category questions with search on (S1), three runs, so that G\* can be retested (v1.13 §8 hands that stability study to Grounding Paper B).
- **Not needed:** a Coverage re-ask (Coverage Paper B), any judge call on t5 answers.
- **Budget:** v0.42 §6 estimates each repeat wave at $67 central and $143 high at the prices read on 2026-11-10 (Gemini 4 Argon at its December price), so t5 must be designed under the $100 cap; if a block has to go, the S0 category block (the one v1.14 needs) is kept first.

### 11.4 Data lock and scoring

1. **Data lock** (tag `aias-6-0-preview-data-locked`): after v1.14 Stage 2 if its output exists by Fri 2026-12-11; otherwise on Dec 11 with Ranking as "PASS, retest pending" (if its interim verdict allows) and Stage 2 entered by addendum (§4.4). Every other input is taken in the state it has at that moment.
2. **Scoring, once:** `score_aias_6_0_preview.py --run` refuses without MQ_Lock and refuses if its output exists.
3. **Addenda** (§4.4) only until the paper lock.
4. **Paper and report**: academic paper (pandoc + xelatex) and Third System brand-format report, both in the provisional register of §5.

## 12. Cost

**The Preview makes no paid model call.** It reads locked scores and computes statistics locally: spend $0. The $100 rule (Pablo, Nov 10, 2026, 8:03 am) is not engaged.

**The t4 Sentiment score (§3.4) is a separate study with its own pre-registration and its own $100 cap.** A planning estimate, so that Pablo can decide (Choice 1), from v1.11's locked cost model (`osf/methodology/v1_11/prereg/PRE_REGISTRATION_v1_11.md` §4.1, §4.2, §7 and `u0_v1_11.json`, tag `v1.11-prereg-r1`): judge J1 Claude Opus 5.5 and J2 GPT-6.1 Sol, both through batch APIs at $2/$10 and $1/$5 per million input/output tokens (vendor pages read 2026-11-10); planning multipliers 1.30 (Anthropic) and 1.10 (OpenAI) on o200k token counts; 100 visible output tokens plus r reasoning tokens per call; overhead ×1.15; a 5% self-consistency repeat; both judges on every unit; v1.11's window cap of 36 windows per brand per answer set. Units are mention windows in the 270 t4 S0 category answers (54 per category).

| Scenario | Windows | Calls per judge | Input tokens per request | r | Estimate (J1 + J2) |
|---|---|---|---|---|---|
| Archived naming density (5.15 windows per answer, v1.11 U0 for the omnibus answers) | 1,390 | 1,460 | 768 (v1.11's measured omnibus mean) | 270 | **$14.09** |
| same | 1,390 | 1,460 | 1,050 (a window at the 1,500-character cap) | 375 (largest reasoning count in the programme's probes) | $18.49 |
| Every brand named in ≥ 36 of its 54 answers (cap binds for all 112 units) | 4,032 | 4,234 | 768 | 270 | $40.86 |
| same, with requests at the window cap and r = 375 | 4,032 | 4,234 | 1,050 | 375 | **$53.61** |

Every scenario is below the $80 pause. The numbers are planning values, not t4 measurements (no t4 answer exists): the study's own pre-registration re-reads the prices, counts the real windows before the first call, and carries v1.11's guard (pause at $80, hard stop at $100 from recorded usage). Its judge batches must avoid the collection windows (none during Nov 17–21; v1.11 §8 gives the blackout rule) and could follow v1.11's own judge run, which starts no earlier than 2026-11-22 06:00 UTC.

## 13. Limitations

1. One wave carries the structure tests (t4 week); t5 adds only Ranking's retest and descriptive retests.
2. Three models, one per provider, at provider-default settings; model generation and serving settings are confounded (v0.42 §7).
3. Five categories, 112 units, US English; registries fixed in May 2026.
4. Every rating floor requires a brand to be named, so the complete-profile set leans to well-named brands; correlations with Presence are computed on a restricted Presence range (SD shows the effect).
5. Coverage comes from its own collection a few days after the t4 answers on the same models; Grounding from search-on answers, the others from search-off answers. The profile mixes two collections and two conditions within one week.
6. Sentiment is AI-judged; its human-label check (Sentiment Paper B) uses archived legacy-panel windows, so it validates the instrument, not the t4 scores themselves.
7. Ranking's statistic was chosen after its archived values were seen (v1.14 §1); t4 and t5 are its first confirmatory data.
8. The I-test's bands are new; no archived data carry six parts, so they could not be calibrated on real data, only on synthetic data (§6.7).
9. Fifteen pairs and five incremental tests: verdicts rest on fixed effect-size bands, not on p-values; no multiplicity correction (the programme's convention, v0.42 §2.1). CONFIRMED is demanding (§6.7).
10. Separability is not validity: no part is tested against behaviour here.
11. The Preview inherits every source's limitations; it cannot repair a component.

## 14. Deviations policy

`anchor/DEVIATIONS.md` opens with Entry 0 (ex ante: what was read and computed before the lock, the COI carry-forward with the Denon correction, the anchor sequence). After the lock every change gets an entry (id, date, ex ante / ex post, what, why, effect on inference); a hash mismatch halts; a scorer fix is allowed only to restore a rule as written, with results before and after; the inclusion rules, tests, bands, floors, seeds and the verdict and wording rules do not change; anything added later is exploratory; an unfavourable structure verdict is published with the same prominence as a favourable one. A component's own deviation is recorded in that component's file, not here.

## 15. Declarations

### Conflict of interest {-}

The author is Director, Corporate Brand Creative and Governance at Samsung Electronics America. This synthesis performs no brand selection and no collection: it reads scores that locked component studies compute on the five omnibus registries fixed in earlier phases, and each registry carries its source-phase conflict-of-interest handling forward unchanged (v1.10 DEVIATIONS Entries 0 and 2; v1.11 and v1.14 DEVIATIONS Entry 0). Two items of record apply to the registries used.

*Audiophile headphones (v0.19).* The v0.19 record states: “The panel substitution of AKG → Denon documented in §5 was made out of an abundance of caution given that Samsung's subsidiary Harman International owns AKG; the substitution occurred prior to pre-registration lock.” (v0.19 paper, Declaration of interest; see also v0.19 pre-registration §2.3 and v0.19 DEVIATIONS Entry 1.) Correction (November 10, 2026): Denon, which replaced AKG in the v0.19 registry, has itself been owned by Harman International, a wholly owned subsidiary of Samsung Electronics, since September 23, 2025, when Harman completed its acquisition of Sound United from Masimo; the v0.19 headphones registry therefore includes one Samsung-group brand. The substitution did not achieve its purpose, and this was not noticed until November 10, 2026. Source: HARMAN, “HARMAN Completes Sound United Acquisition to Expand Premium Audio Leadership”, press release, Business Wire, September 23, 2025. In this synthesis Denon remains in the registry and in the primary analysis, as in every component study; every structure statistic is also reported without the Denon unit (sensitivity SA).

*Automotive (v0.22).* The v0.22 record states: “Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the v0.22 registry: Harman International (audio systems) supplies Mercedes-Benz, BMW, and other premium automotive OEMs; Samsung SDI (battery cells) supplies BMW (i-series), Volkswagen Group brands including Bentley and Porsche (Stellantis-adjacent platforms), and others; Samsung Display (infotainment) supplies Mercedes-Benz and BMW. Tesla and Polestar also have tangential Samsung-component exposure at the parts level. These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any v0.22 registry entry. The COI was screened and documented in DEVIATIONS Entry 0 (Part B) of the pre-registration module; no operational restriction on registry composition was imposed.” (v0.22 paper, Conflict of interest.) These are supply relationships, not ownership; no v0.22 brand is removed.

All statistics are computed automatically from locked inputs under this pre-registration. Samsung Electronics had no role in the design, conduct, analysis or reporting of this work.

### Funding {-}

Self-funded. No external funding supported this research.

### Ethics {-}

Not applicable; no human subjects. The Preview analyses scores computed from responses of large language models queried under their public interfaces. The human labelling that validates Sentiment is governed by Sentiment Paper B's own pre-registration.

## Use of AI tools {-}

During the preparation of this work the author used AI tools (Anthropic's Claude) to assist with study design, analysis and writing. The author reviewed and edited all content and takes full responsibility for it.

## 16. Files, and what r1 must add before the lock

**In this draft (r0):** `prereg/PRE_REGISTRATION_aias_6_0_preview.md` (this file); `prereg/precision_aias_6_0_preview.json` and `scoping/precision_aias_6_0_preview.py` (synthetic precision note, §6.7); `scripts/score_aias_6_0_preview.py` (scorer skeleton: gate reading, inclusion, S-tests, I-tests, component status, H_Structure, wording class, composite check, carried-pair parity, sensitivities SA–SC, hashed reads from git references, MQ_Blind, lock-manifest text, synthetic dry run) and `scripts/tests/test_score_aias_6_0_preview.py` (29 synthetic-data tests, all passing at r0; outputs only to temporary directories); `anchor/DEVIATIONS.md` (Entry 0, draft); `README.md`; `PLAIN_SUMMARY_aias_6_0_preview_r0.md` (for Pablo; not deposited). The scorer imports `scripts/score_v1_10.py` unchanged (git blob `0f8b981b…`, byte-identical to tag `v1.10-prereg-r2`; a test asserts the blob); r1 adds `scripts/score_v1_14.py` (tag `v1.14-prereg-r1`) for the shared P and C\* function.

**r1, before the lock (after v1.12, v1.13 and v0.42 lock on Wed Nov 11):**

1. Pin the exact scored-output paths and column names of v1.12 (Cov\* unit table, verdict file), v1.13 (G\* unit table, `v1_13_verdicts.json`) and, if commissioned, the S_t4 study; record each lock tag, tag object and commit.
2. Record whether v1.13's H6 (Coverage) and v1.12's H5 / v1.13's H4 (Ranking) are active at their locks, which decides which rows of §6.2 are carried.
3. Wire the scorer's hashed readers to the pinned paths (v0.42, v1.12, v1.13, v1.14, S_t4, AIAS 2.0), add MQ_Lock, MQ_Join and the P and C\* recomputation with `score_v1_14.comparators` (MQ_Parity), the descriptives D1–D9 and the sensitivities SD–SH, with tests.
4. Write `prereg/LOCK_MANIFEST_aias_6_0_preview.sha256` with `--lock-manifest` (this file, the precision record and script, the scorer and its tests, DEVIATIONS, README, and the two imported scorers) and an anchor writer (`--write-anchor`, after v1.14's).
5. Apply Pablo's choices (§17).

## 17. Choices made in drafting (for the pre-registrant; each has a recommended default)

1. **Sentiment on the newest models.** (a) Commission a small, separately pre-registered t4 Sentiment score (v1.11's instrument unchanged on the t4 S0 category answers; about $14–54, §12), so the profile has all six parts on one panel. (b) Report Sentiment from the legacy panel beside the profile, with no structure test (a five-part structure verdict). **Default: (a)**, with (b) as the automatic fallback if (a) is not scored by the data lock.
2. **MARGINAL components.** Shown in an "under review" band below the profile, outside every verdict (**default**), or left out of the Preview.
3. **How strict CONFIRMED is.** Strict: every own pairwise test and every incremental test in the CONFIRMED band (**default**; the programme's reading of MARGINAL); or lenient: CONFIRMED unless a test is FALSIFIED, with marginal results listed. Strict makes PARTIAL likely even when overlaps are small (§6.7).
4. **Composite.** Profile only, with v1.9's constraints computed as a descriptive check (**default**); or a provisional equal-weight number per brand (not recommended: v1.9 showed such averages copy Presence).
5. **Ranking's retest.** Wait for v1.14 Stage 2 if its output exists by Dec 11 (**default**); otherwise go ahead with "retest pending" and add Stage 2 as an addendum.
6. **Reading Sentiment's gate.** All five PRIMARY hypotheses of v1.11 CONFIRMED = PASS, the sister papers' rule (**default**).
7. **Lock date.** Wed Nov 11 or Thu Nov 12 with the other locks (**default**); latest safe: the earlier of Sat Nov 14 and v0.42's first scoring run.
