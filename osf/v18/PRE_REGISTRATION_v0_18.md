# v0.18 Pre-Registration — Indie Fragrance / IL-Gradient Substrate

**Tag (intended):** `v0.18-prereg-r1`
**Commit (backfill at lock):** `[TBD]`
**Date:** 2026-05-20
**Substrate:** Indie Fragrance (IL-Gradient Design — three cells)
**Predecessors:** v0.17 Premium Kitchenware (SSRN 6802261), v0.16 Kitchen Knives (SSRN 6791999)
**Canonical methodology citation chain:** AIAS™ Presence Measurement Protocol v1.2 (SSRN 6761698), v1.3 (6797679), v1.4 (6799479)
**Foundational reference:** AI Availability — A Third System (SSRN 6659000)
**Research entity:** Third System™ (data archive and methodology venue)

---

## §1. Substrate and panel

### 1.1 Operational definition of indie fragrance

For the purposes of v0.18, "indie fragrance" is operationally extended beyond the strict pure-indie sense to encompass an **IL-gradient panel** spanning three tiers of Identity Load on the fragrance consumer-discovery surface. The substantive question is not whether a brand is independently owned but whether its position on the IL gradient produces the Regime 4 signature the moderator hypothesis predicts. Conglomerate ownership of designer-niche houses (EL, LVMH) is treated as a borderline classification (see §1.5), not an exclusion criterion.

The panel is entirely English-language-presence anchored. No cross-cultural cells. This removes the confound that contaminated v0.17's Japanese cell (Vermicular → Iwachu cascade) and isolates the IL moderator on equal LLM-coverage terms across cells.

### 1.2 Cell stratification rationale (IL gradient)

Three cells stratified by Identity Load on a monotonic gradient from medium IL (mass-prestige, anchor) through medium-high IL (designer-niche) to high IL (indie/artisan):

- **Cell A — Designer-niche, medium-high IL.** Selection process involves curatorial signaling and connoisseur-adjacent discovery but operates within the established prestige-fragrance retail surface.
- **Cell B — Indie/artisan, high IL.** Selection process is itself part of what the purchase accomplishes; perfumistas-native lexicon; small-house identity is part of the brand's signal.
- **Cell C — Mass-prestige, medium IL — comparison anchor.** Mainstream designer fragrance; signature-scent role; selection process more separable from product identity.

If `H_IdentityLoad_moderator` is true, the Regime 4 signature should strengthen monotonically C → A → B.

**Cell C internal-variance sensitivity note (r2).** Cell C spans iconic mass-prestige houses (Chanel, Dior) and mainstream-prestige houses (Marc Jacobs, Calvin Klein). The operational definition holding Cell C together is "mainstream designer fragrance houses with global mass-prestige distribution" — a defensible IL tier that nevertheless contains within-cell variance. If post-acquisition data shows Cell C splitting into icon-tier and mainstream-tier sub-clusters on the Regime 4 signature, this is reported as a descriptive sensitivity in §3 and does not retroactively re-stratify the cell.

### 1.3 Brand registry (24 brands locked at this draft; subject to one final review pass before commit)

**Cell A — Designer-niche (8):**

1. Maison Francis Kurkdjian (MFK)
2. Le Labo *(borderline — EL ownership 2014)*
3. Byredo *(borderline — LVMH ownership 2022)*
4. Frederic Malle *(borderline — EL ownership 2014)*
5. Diptyque
6. Comme des Garçons Parfums *(lower-prominence flag — possible Cell-B-style attrition)*
7. Memo Paris *(lower-prominence flag)*
8. Etat Libre d'Orange *(Paris house, founded 2006; established niche identity; r2 swap-in replacing Nasomatto for stronger LLM-coverage projection)*

**Cell B — Indie/artisan (8):**

1. D.S. & Durga
2. Snif *(US indie, founded 2020; well-funded DTC, strong recent press footprint; r2 swap-in replacing Régime des Fleurs for stronger LLM-coverage projection)*
3. Heretic Parfum
4. Ellis Brooklyn
5. Boy Smells
6. Vyrao
7. Henry Rose
8. Phlur *(lower-prominence flag)*

**Cell C — Mass-prestige (8):**

1. Chanel
2. Dior
3. YSL
4. Tom Ford *(unit-of-analysis note — house-level; Tom Ford Private Blend NOT split into Cell A per same-house collision rule)*
5. Marc Jacobs
6. Calvin Klein
7. Versace
8. Givenchy

**Inline brand concerns flagged at this draft:**

- Cell A's lower two registry slots (CdG Parfums, Memo Paris) sit closer to Cell B than to Cell A in terms of LLM coverage even if they sit in Cell A on IL. If their Phase B mention rates collapse to near-zero, Cell A attrition could approach Cell B's. Pre-registered cascade order (§1.4) places them mid-list so they fall before the r2 swap-in (Etat Libre d'Orange) is tested.
- Cell B's Phlur is now the weakest-coverage registry entry following the r2 swap (Régime des Fleurs → Snif); if Phlur fails Phase A C_P anchoring during cascade, the alternate list below is invoked.
- Tom Ford Private Blend and Chanel Les Exclusifs are *excluded* from Cell A despite their designer-niche brand identity, because their parent houses appear in Cell C. Same-house collision is a protocol violation under the v0.17 brand-house unit-of-analysis rule.
- Aesop is *not included* in Cell A despite the kickoff suggestion; its apparel-and-body-care adjacency makes its fragrance Phase A signal noisy, and the v0.17 protocol's `borderline_resolution_at: phase_b_topic_id` pattern doesn't cleanly handle a brand whose primary LLM-retrieval surface is non-fragrance.

### 1.4 Pivot ordering per cell (cascade)

Each cell's pivot must produce 6/6 C_P anchoring for the cell to proceed to Phase B (per v1.4 cascade protocol). If the primary pivot fails, cascade descends in prominence:

**Cell A cascade:** MFK → Le Labo → Diptyque → Frederic Malle → Byredo → CdG Parfums → Memo Paris → Etat Libre d'Orange

**Cell B cascade:** D.S. & Durga → Boy Smells → Heretic → Ellis Brooklyn → Vyrao → Henry Rose → Phlur → Snif

**Cell C cascade:** Chanel → Dior → YSL → Tom Ford → Givenchy → Versace → Marc Jacobs → Calvin Klein

Alternates outside the registry (invoked only if a full cell cascade fails Phase A, with DEVIATIONS entry):

- Cell A alternates: Atelier Cologne, Acqua di Parma *(LVMH)*, Nasomatto *(r2: moved from registry to alternates)*, Editions de Parfums Frédéric Malle *(same-house as #4)*, Maison Margiela Replica
- Cell B alternates: Sana Jardin, Floral Street, Imaginary Authors, Juliette Has a Gun, Régime des Fleurs *(r2: moved from registry to alternates)*
- Cell C alternates: Hugo Boss, Lancôme, Carolina Herrera, Paco Rabanne, Burberry

### 1.5 Borderline classifications

Per v0.17 protocol pattern, pre-register the following with `borderline_classification: true, borderline_resolution_at: phase_b_topic_id`:

- **Le Labo** — EL ownership since 2014, designer-niche brand identity retained
- **Frederic Malle** — EL ownership since 2014, designer-niche brand identity retained
- **Byredo** — LVMH ownership since 2022, designer-niche brand identity retained

Resolution rule: if Phase B retrieval surfaces these as designer-niche (under q1 "niche" frame) and *not* as mass-prestige (under q2/q3 frames), Cell A placement is canonical. If Phase B retrieval surfaces them under mass-prestige frames preferentially, the placement is re-classified post-hoc under the DEVIATIONS protocol (without retroactive registry change).

### 1.6 Reference panel (locked, six-slot)

Same panel as v0.16 / v0.17:

- claude-opus-4-5
- claude-sonnet-4-5
- gpt-4o
- gpt-4o-mini
- gemini-2.5-flash
- gemini-2.5-flash-lite

Provider model substitutions documented in DEVIATIONS as encountered.

### 1.7 Phase B category queries (three-frame structure)

Lexical anchor: **"niche"** (perfumista-native, IL-aligned vocabulary). Three frames mirror v0.17's tradition-agnostic format:

- **q1 (primary anchor):** "What are the best **niche** fragrances? List several with descriptions."
- **q2 (cross-frame):** "Recommend high-quality **independent** fragrance brands. Name several brands."
- **q3 (perfumista lexicon):** "What fragrances do **industry insiders and perfumistas** recommend? List several."

Phase B totals: 6 models × 3 queries = 18 Phase B observations per brand.

---

## §2. Hypotheses

### 2.1 H_Regime4_indie_fragrance (within-phase substantive)

The Cell C → A → B Regime 4 signature should strengthen monotonically along the IL gradient, with Cell B exhibiting the strongest signature.

Operationalized against the canonical Regime 4 conditions (calibrated to indie fragrance panel):

- **C1 (panel adequacy):** worldwide n ≥ 12 post-attrition across the full panel
- **C2 (Regime 4 retrieval signature):** per-cell mention concentration index meets pre-registered Regime 4 threshold
- **C3 (ranking coherence):** per-cell Phase B mention-rank order coherent with anchor-pivot prominence

Conditions verbatim from v0.17; C1 floor recalibrated to ≥ 12 (unchanged; 8/8/8 → n=24 pre-floor survives 50% attrition).

### 2.2 H_IdentityLoad_moderator (three-leg joint, v0.16 × v0.17 × v0.18)

Identity Load moderates the Regime 4 signature: higher-IL substrates produce stronger signatures than lower-IL substrates. Test is a three-leg joint over v0.16 (PARTIAL), v0.17 (FALSIFIED on panel inadequacy), and v0.18 (this phase).

The three-leg joint verdict matrix is specified ex-ante in §5.1.

### 2.3 H_Recognition_Recall_dissociation_generalization (primary co-hypothesis, novel for v0.18)

The Recognition × Recall dissociation pattern documented in v0.17 (Iwachu: Phase A C_P = 6/6, Phase B mention rate = 0/18) is tested for generalization to a same-language, IL-gradient substrate.

**Pre-registered dissociation threshold (Iwachu-pattern):** Any panel brand with Phase A C_P ≥ 5/6 (≥ 83% recognition) *and* Phase B mention rate ≤ 2/18 (≤ 11% recall across three frames) constitutes a dissociation case.

**Pre-registered Recognition–Recall correlation threshold (r3, closes §5.2 gap).** When zero Iwachu-pattern cases are observed across the panel, the §5.2 routing to DISSOCIATION_NARROWED requires the substrate-level Recognition–Recall correlation to be "strong." This is operationalized as follows:

- *Metric.* Spearman rank correlation ρ between Phase A C_P score (per brand) and Phase B mention count (per brand), pooled across all anchored brands (worldwide post-attrition n).
- *Strong-correlation threshold.* ρ ≥ 0.5 *and* the bootstrap 95% confidence interval lower bound for ρ > 0.3. Bootstrap: 10,000 resamples at the brand level with replacement; percentile method for CI construction.
- *Failure mode.* If ρ ≥ 0.5 but CI lower bound ≤ 0.3 (small-n inflation suspected), or if ρ < 0.5, the §5.2 routing returns DISSOCIATION_UNDETERMINED rather than DISSOCIATION_NARROWED.
- *Pre-registration scope.* The 0.5 / 0.3 thresholds, the bootstrap procedure (10,000 resamples, percentile method), and the brand-level resampling unit are all pre-registered ex-ante and do not change post-acquisition. Any deviation requires a DEVIATIONS entry and renders the §5.2 verdict UNDETERMINED rather than NARROWED.

Rationale: ρ ≥ 0.5 corresponds to Cohen's "large effect" convention and represents the threshold above which Recognition rank predicts Recall rank with substantial accuracy. The CI lower bound > 0.3 guard prevents small-n correlation inflation from spuriously routing to NARROWED — particularly relevant given that post-attrition pooled n may be in the 18–24 range where Spearman ρ point estimates are noisy.

This hypothesis is pre-registered as a **primary co-hypothesis**, on par with H_Regime4_indie_fragrance and H_IdentityLoad_moderator in the verdict matrix. v1.4's multi-component construct currently rests on the single Iwachu anchor; v0.18 is the first generalization test, and its verdict status is consequential for the canonical methodology layer that v1.0 will ship.

The dissociation generalization matrix is specified ex-ante in §5.2.

---

## §3. Descriptive sensitivities

Pre-registered descriptive analyses (no formal verdict commitment; reported as sensitivities in the v0.18 SSRN paper §3):

- **US / worldwide divergence** — for each cell, report mention rate divergence between US-locale-anchored Phase B and worldwide-anchored Phase B
- **Per-cell n** — pre- and post-attrition cell sizes, with attrition causes inventoried
- **Per-cell ρ** at n ≥ 5 (per Phase D pre-planning rule, §4)
- **Cross-frame divergence** — mention rate divergence across q1 / q2 / q3 within each cell (relevant to the dissociation analysis)

---

## §4. Decision rules

C1 / C2 / C3 verbatim from v0.17 protocol, with C1 floor n ≥ 12 (unchanged).

### 4.1 Phase D scoring plan (changed from v0.17)

v0.17 paper skipped Phase D ρ because the verdict resolved at C1. For v0.18, **Phase D ρ is planned from the start** — computed for each cell regardless of where C1 / C2 / C3 resolution occurs, provided post-attrition cell n ≥ 5.

Rationale: with dissociation pre-registered as primary co-hypothesis, Phase D ρ becomes the natural quantitative layer for the Recall component of the multi-component construct. Pre-registering Phase D as conditional while leaving dissociation as primary is internally inconsistent.

### 4.2 Bounded-override fallback (carry-forward from v1.3 §6.4)

Phase A pivot cascade per v1.3 five-stage spec. Alternate-also-fails invokes the bounded-override fallback rule documented in v1.3.

---

## §5. Joint verdict matrices

### 5.1 H_IdentityLoad_moderator three-leg joint matrix (ex-ante)

| v0.18 leg | Joint verdict (v0.16 PARTIAL × v0.17 FALSIFIED × v0.18) |
|---|---|
| **CONFIRMED** at v0.18 | **CONFIRMED** — higher-IL substrate produces stronger Regime 4 signature as moderator predicts; v0.17 reread as panel inadequacy artifact |
| **PARTIAL** at v0.18 | **PARTIAL** — moderator operates but bounded; substrate-specific qualifications required |
| **FALSIFIED** at v0.18 | **FALSIFIED** — Identity Load does not moderate AI Availability across this gradient |
| **NULL** at v0.18 (e.g., C1 inadequacy) | **AMBIGUOUS-deferred** → v0.19 with further substrate refinement |

### 5.2 H_Recognition_Recall_dissociation generalization matrix (ex-ante)

Anchor: Iwachu (v0.17), Phase A 6/6 × Phase B 0/18.

| v0.18 dissociation cases (Iwachu-pattern: Phase A C_P ≥ 5/6 ∧ Phase B mention rate ≤ 2/18) | Methodological verdict |
|---|---|
| ≥1 case per cell (cross-cell generalization) | **DISSOCIATION_GENERALIZED** — v1.4 multi-component claim strengthened across substrates |
| ≥1 case but cell-clustered (e.g., only Cell B) | **DISSOCIATION_PARTIAL** — v1.4 claim qualified; dissociation may be IL-dependent |
| 0 cases, Recognition–Recall correlation strong (per §2.3 threshold: ρ ≥ 0.5 ∧ bootstrap 95% CI lower bound > 0.3) | **DISSOCIATION_NARROWED** — Iwachu may be cross-cultural-substrate-specific artifact; v1.4 claim narrows |
| 0 cases, Recognition–Recall correlation NOT strong (ρ < 0.5 or CI lower bound ≤ 0.3) | **DISSOCIATION_UNDETERMINED** — pattern unclear; defer to v0.19+ |
| Panel inadequacy precludes test (worldwide post-attrition n < 12) | **DISSOCIATION_UNDETERMINED** — deferred to v0.19+ |

---

## §6. Borderline classifications (consolidated)

Per §1.5:
- Le Labo, Frederic Malle, Byredo — conglomerate-owned designer-niche; Cell A placement canonical; Phase B retrieval-frame resolution.

Per §1.3 same-house exclusions:
- Tom Ford Private Blend, Chanel Les Exclusifs — *excluded* from Cell A. Cell C parent-house registry holds.

---

## §7. Substrate property notes

Indie fragrance is a culturally and personally identity-bearing category; fragrance selection is itself part of what the purchase accomplishes. The substrate is therefore positioned at the high-IL end of the consumer-category spectrum, ahead of v0.16 (kitchen knives — medium IL) and v0.17 (premium kitchenware — medium IL). The IL-gradient design within v0.18 produces an additional within-phase test of the moderator that v0.16 and v0.17 did not afford (both were uniform-IL panels).

---

## §8. DEVIATIONS protocol carry-forward

All DEVIATIONS entries from v0.16 / v0.17 carry forward; new entries opened as encountered. Particular DEVIATIONS triggers to anticipate:

- Substrate substitution (e.g., LLM-substrate already canonical from v1.4)
- Provider model substitution (six-slot panel)
- Cell-internal attrition exceeding 50% triggering alternate cascade
- Same-house collision detection at Phase B (Tom Ford Private Blend retrieval as Cell A signal)

---

## §9. Commit and tag

- Branch: `v0.18-il-gradient` (new)
- Lock action: `git commit` of this pre-reg + `git tag v0.18-prereg-r1`
- Commit hash: backfilled into §header `Commit (backfill at lock)` after tagging
- No acquisition begins before tag is in place

---

## §10. Programmatic cross-references

Carry-forward citations for v0.18 SSRN paper Methods section and OSF v18/ README:

- **AI Availability foundational:** SSRN 6659000
- **Methodology chain:** v1.2 (6761698), v1.3 (6797679), v1.4 (6799479)
- **Predecessor phases:** v0.17 (6802261), v0.16 (6791999)
- **OSF project:** ec6wh; v0.18 deposit at `osf/v18/`
- **GitHub:** thirdsystem-aias/aias, branch `v0.18-il-gradient`

---

*End v0.18 pre-registration draft r3. Next action: final review by author; revisions tracked as r4 if needed; final lock at `git commit` + `git tag v0.18-prereg-r1` before any Phase A acquisition.*

---

## Appendix A — r1 → r2 → r3 changelog

### r2 → r3

Closed one pre-reg gap surfaced by drafting `score_v18.py` (the canonical scoring/verdict driver):

**§5.2 Recognition–Recall correlation threshold operationalized in §2.3.** r2's §5.2 routed 0-case outcomes to DISSOCIATION_NARROWED conditional on Recognition–Recall correlation being "strong" — a qualitative criterion that the scorer cannot evaluate without a numerical threshold. r3 closes this gap by pre-registering:

- *Metric:* Spearman ρ between Phase A C_P and Phase B mention count, pooled across all anchored brands
- *Threshold:* ρ ≥ 0.5 *and* bootstrap 95% CI lower bound > 0.3
- *Bootstrap procedure:* 10,000 resamples at brand level, percentile-method CI
- *Failure mode:* If ρ ≥ 0.5 but CI lower bound ≤ 0.3, route to DISSOCIATION_UNDETERMINED (not NARROWED) — guards against small-n inflation at post-attrition n in the 18–24 range
- *Locked ex-ante; no post-acquisition adjustment without DEVIATIONS entry rendering the §5.2 verdict UNDETERMINED*

§5.2 matrix updated to split the original "0 cases, correlation strong → NARROWED" row into two distinct rows (correlation strong → NARROWED; correlation NOT strong → UNDETERMINED), making the routing fully deterministic.

Two other gaps surfaced by `score_v18.py` are NOT new pre-reg gaps; they are carry-forward citations to v0.17's `score_v17.py`:
- `C2_REGIME4_MENTION_THRESHOLD` (Regime 4 concentration index threshold)
- `C3_RANKING_COHERENCE_THRESHOLD` (cell-internal ranking coherence operationalization)

These thresholds are protocol-canonical from v0.17 and are referenced rather than re-specified in this pre-reg. They are lifted into `score_v18.py` at wire-up time from `score_v17.py` source.

### r1 → r2

Three review items from r1 closed:

1. **Brand list — lower-prominence flags (Cell A / Cell B).** Two pre-emptive swaps applied within the same IL tier:
   - **Cell A:** Nasomatto → Etat Libre d'Orange (Paris house, founded 2006; established niche identity; stronger projected LLM coverage). Nasomatto moved to Cell A alternates.
   - **Cell B:** Régime des Fleurs → Snif (US indie, founded 2020; well-funded DTC, strong recent press footprint; stronger projected LLM coverage). Régime des Fleurs moved to Cell B alternates.
   - **Kept (moderate-risk, retained as stress tests):** CdG Parfums, Memo Paris in Cell A; Phlur in Cell B.
   - Rationale: light pre-emptive coverage-projected swaps are legitimate pre-reg moves under the v0.17 over-provisioning rule; heavier post-hoc optimization would leak data-conditional reasoning into the pre-reg.

2. **Dissociation threshold (§2.3).** Unchanged at C_P ≥ 5/6 ∧ Phase B mention rate ≤ 2/18. Tighter (literal Iwachu 6/6 ∧ 0/18) risks zero-case verdicts collapsing to DISSOCIATION_NARROWED informationally; looser (4/6 ∧ 3/18) admits sampling-variance false positives. The 5/6 ∧ 2/18 midpoint is the defensible epistemic anchor.

3. **Cell C composition (§1.2).** Marc Jacobs / Calvin Klein retained alongside Chanel / Dior / YSL / Tom Ford / Versace / Givenchy. Internal-variance sensitivity added to §1.2 acknowledging the icon-tier vs. mainstream-tier within-cell range; sensitivity reported descriptively under §3 if post-acquisition data shows sub-clustering. Operational definition "mainstream designer fragrance houses with global mass-prestige distribution" holds the cell together.
