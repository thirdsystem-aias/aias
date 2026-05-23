# AIAS Protocol v1.6 — Working Outline

**Status:** Decisions resolved; ready for pre-registration lock at `v1.6-prereg-r1`.
**Predecessor:** v1.5 (SSRN 6810758, May 2026)
**Empirical anchors:** v0.16–v0.21 corpus (retrospective scoring under v1.6)
**Prospective application:** v0.22+

---

## Positioning

Methodology paper, not phase paper. Closes three open items identified in v0.20 (SSRN 6811441) and v0.21 (SSRN 6815378) §6. Retrospectively scores the six-phase corpus under the new framework, mirroring the pattern v1.5 used (retrospective calibration on joint v0.18 + v0.19, prospective test on v0.20). Unblocks v0.22+ prospective phases under cleaner routing AND tightens the AIAS™ 1.0 synthesis paper before that synthesis ships.

## Working title (locked)

> The AIAS™ Presence Measurement Protocol: Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension (v1.6)

Locked at pre-reg r1. Long form matches v1.5 precedent (named-increments in title).

---

## The three increments

### Increment 1 — Substrate-level Recognition pre-screen

**Motivation.** v0.20 produced differential C2 outcomes (Cell A bimodal C_P, Cell B passing, Cell C saturated). v0.21 produced uniform C2 failure (all three cells at C_P = 6/6, distinct = 1, modal = 1.000). The verdict-routing matrix collapses both to FALSIFIED, but they carry different information about the substrate. v1.5 §6 flagged this distinction; v1.6 makes it operational.

**Proposal.** Insert a pre-C2 substrate classification step. Classify substrates by Phase A distribution shape across cells before invoking C2 routing.

**Classification rule (locked v1.6-prereg-r1).**

- **Uniform-saturation substrate** — distinct C_P count = 1 in all 3 cells. Single operational rule; strictest falsifiable form for the 6-LLM panel.
- **Differential substrate** — otherwise (default).

**Routing change (locked).**

- Uniform-saturation → bypass C2; the four cell-level Regime-4 verdicts collapse to a single substrate-level verdict `REGIME-4-UNAVAILABLE-AT-RECOGNITION` (distinct from FALSIFIED, see verdict-state lock below). The moderator hypothesis is evaluated via Increment 2's `H_IdentityLoad_Direct` independently. Type 1 / Type 2 quadrant population and Iwachu cases are reported as descriptive findings under this routing, not as pass/fail verdict components.
- Differential → standard C1 → C2 → IL-gradient guard → C3 sequence (v1.5 as-is).

**Fifth verdict state (locked).** `REGIME-4-UNAVAILABLE-AT-RECOGNITION` enters the Regime 4 verdict vocabulary. Distinct from FALSIFIED: FALSIFIED records differential-cell C2 failure; the new state records substrate-wide Recognition saturation that makes C2 ill-defined. Both states close Regime 4, but they carry different information for the AIAS™ 1.0 synthesis.

**Retrospective application.** v0.16 differential; v0.17 differential (within-cell variance plus panel inadequacy); v0.18 differential; v0.19 mixed (Cell A bimodal-ish, Cell B saturation-prone); v0.20 differential; v0.21 uniform-saturation. Only v0.21 routes via the new path under v1.6.

---

### Increment 2 — Independent moderator pathway

**Motivation.** H_IdentityLoad_moderator returned NARROWED in v0.20 and v0.21 despite increasingly strong substantive channel-asymmetry signals (v0.20 Cell C R_cat-dominant + Cell B R_cult-dominant; v0.21 Cell B R_cult-lead 2.83× — the program's strongest). The five-leg joint verdict is structurally pessimistic — when Regime 4 falsifies for substrate reasons, the moderator hypothesis backs off rather than incorporating the within-phase signal. v0.21 §4.4 flagged this; v1.6 unblocks it.

**Proposal.** Introduce `H_IdentityLoad_Direct` as a parallel hypothesis evaluable independently of Regime 4's C2 conditions.

**Test specification (locked v1.6-prereg-r1).**

- Per cell, compute mean R_cat and mean R_cult across the n brands.
- Compute channel-asymmetry estimate δ = mean(R_cult) − mean(R_cat) per cell.
- Bootstrap CIs on δ: n_bootstrap = 10,000; per-cell resampling with replacement; **percentile CI** (not BCa).
- Seed discipline: a single methodology-level seed (`SEED_V16_RETRO = 1621`) is used for retrospective scoring of v0.16–v0.21. Prospective phases v0.22+ set their own phase-level seed at phase pre-reg.
- IL-gradient prediction (substrate-aware): high-IL cell (B in standard panel design) shows δ > 0 with CI excluding zero; medium-IL cell (A) shows δ < 0 with CI excluding zero; low-IL cell (C) shows δ value bounded by the monotonic-gradient check below.

**Verdict matrix (locked).**

- **CONFIRMED** — monotonic asymmetry pattern matches IL gradient prediction: Cell B CI excludes zero (positive); Cell A CI excludes zero (negative); Cell C δ lies between Cell A δ and Cell B δ (monotonic-gradient check passes).
- **PARTIAL** — direction matches in both focal cells (A, B) but at least one CI overlaps zero, or Cell C monotonic-gradient check fails while focal-cell directions hold.
- **FALSIFIED** — Cell B δ ≤ 0 with CI excluding zero (opposite direction), OR Cell A δ ≥ 0 with CI excluding zero, OR monotonic-gradient check fails with both focal-cell CIs excluding zero (configuration that cannot be reconciled with the IL-gradient model).
- **INDETERMINATE** — brand-level `n_post_attrition < 5` in any focal cell (A or B). Attrition = brand removed for valid measurement reason (zero responses across all 18 canonical and 18 cultural Phase B mentions). Cell C post-attrition shortfall does not trigger INDETERMINATE on its own; the gradient check defaults to "not evaluable" and verdict resolves on focal cells only.

**Retrospective application.**

| Phase | Substrate | Cell B δ | Cell A δ | Verdict under H_IL_Direct |
|---|---|---|---|---|
| v0.16 | Kitchen knives | TBD | TBD | TBD |
| v0.17 | Premium kitchenware | TBD | TBD | TBD |
| v0.18 | Indie fragrance | TBD | TBD | TBD |
| v0.20 | Skincare | +3.00 | −1.50 (approx) | likely PARTIAL or CONFIRMED |
| v0.21 | Cosmetics | +7.12 | −3.13 | strong CONFIRMED candidate |

**Joint moderator verdict under v1.6.** Five-leg joint resolved via H_IdentityLoad_Direct rather than H_IdentityLoad_moderator (Regime 4–dependent). Expected uplift from NARROWED → PARTIAL or CONFIRMED based on the substantive signal v0.21 surfaced.

---

### Increment 3 — Phantom Brand Persistence Phase B extension

**Motivation.** v0.21 surfaced the strongest single Phantom Brand Persistence demonstration in the program — Glossier (a v0.20 Cell B panel brand, NOT on the v0.21 panel) appeared in cultural-channel frames for all six panel LLMs in q6 and three of six in q4 and q5. Estée Lauder (also not on the v0.21 panel) appeared in the canonical channel for all six models (R_cat = 13/18). The construct is documented at the case-study level in §4.5 but is not a measured component of AI Availability. v1.6 lifts it to measured status.

**Proposal.** Introduce `R_phantom` as a substrate-level construct measured against a curated reference vocabulary larger than the panel.

**Reference vocabulary construction (locked v1.6-prereg-r1).**

The reference vocabulary per substrate is the **union** of three exogenous sources:

1. **Panel** — the 24 panel brands for the substrate (3 cells × 8 brands).
2. **Top-50 market-share list** — substrate-specific top-50 brands by market share. Source pre-registered per substrate (e.g., NPD for cosmetics, Circana for skincare); citation locked at pre-reg, list snapshot frozen at acquisition.
3. **Cross-validated emergents** — brands that appeared in prior-phase Phase B response logs for the substrate AND also appear in the top-50 market-share list. Brands found only in Phase B logs (without market-share corroboration) are excluded.

This construction breaks the endogeneity hazard: the vocabulary cannot smuggle in phantoms discovered solely by the surface being measured. Glossier (the v0.21 anchor case) appears on cosmetics top-50 lists independently, so the rule retains it.

Vocabulary size: variable per substrate (panel 24 + market-share intersection, typically yielding 50–80 brands). Vocabulary held constant across cells within a substrate.

**Measurement.**

- For each Phase B response, scan the full reference vocabulary (not just the panel) for mentions.
- Per-brand phantom score R_phantom: count of mentions across all 36 Phase B responses (max 36). Decomposed as R_cat_phantom (max 18) and R_cult_phantom (max 18) per channel.
- Per-substrate phantom prevalence: count of *off-panel* reference-vocabulary brands with R_phantom ≥ K.

**Persistence threshold (locked).** K = 6 mentions across 36 Phase B responses, anchored to the v0.21 Glossier q6 demonstration (6/6 LLMs in a single cultural-frame query). Validity check at retrospective scoring: v0.21 Glossier must satisfy R_phantom ≥ 6 under v1.6 measurement. If it does not, the threshold is reopened via pre-reg amendment, not silently re-tuned post-hoc.

**Verdict matrix (locked).** `H_PhantomBrandPersistence` claims ≥ 1 off-panel brand in the reference vocabulary scores R_phantom ≥ K. CONFIRMED if ≥ 1 case. ABSENT if 0 cases.

**Retrospective application scope (locked).** Phantom increment ships as **prospective-only** from v0.22+, with **retrospective scoring on v0.21 only** (where the construct is empirically motivated and the acquisition logs are freshest). Retrospective construction of reference vocabularies for v0.16–v0.20 is deferred to a possible future methodology pass; not in v1.6 scope.

---

## Paper structure (draft)

1. **Abstract** — three increments named; retrospective scoring summary; 1.0-synthesis-enabler framing
2. **§1 Introduction** — what v1.5 did not address; what v0.20 and v0.21 surfaced; what v1.6 closes
3. **§2 Substrate-level Recognition pre-screen** — definition; threshold; routing change; retrospective classification across v0.16–v0.21
4. **§3 Independent moderator pathway** — definition; bootstrap test specification; verdict matrix; retrospective application table
5. **§4 Phantom Brand Persistence Phase B extension** — definition; reference vocabulary construction (locked exogenous-source rule); measurement; verdict matrix; retrospective application (v0.21 only; prospective-only from v0.22+)
6. **§5 Joint retrospective scoring of v0.16–v0.21 under v1.6** — single 6-row × 7-column table (schema locked): columns are Phase, Substrate, Routing(v1.5), Routing(v1.6), Moderator verdict(v1.5), Moderator verdict(v1.6 via `H_IdentityLoad_Direct`), Phantom verdict. Phantom column populates v0.21 only; v0.16–v0.20 cells marked `N/A (out of v1.6 retrospective scope)`. Before/after deltas highlighted in §5 prose.
7. **§6 Implications** — for v0.22+ prospective phases; for AIAS™ 1.0 synthesis; for the multi-component construct
8. **§7 Methodology log** — v1.5 → v1.6 increment trail; retrospective vs. prospective application boundaries (7-row × 4-column table: Inc 1 / Inc 2 / Inc 3 applicability per phase v0.16–v0.21 plus v0.22+ prospective row); pre-registration trajectory for v0.22+

   **Boundary application table (locked schema):**

   | Phase | Inc 1 (substrate pre-screen) | Inc 2 (`H_IdentityLoad_Direct`) | Inc 3 (Phantom) |
   |---|---|---|---|
   | v0.16 | applied (retrospective) | applied if δ computable | not applied |
   | v0.17 | applied (retrospective) | applied if δ computable | not applied |
   | v0.18 | applied (retrospective) | applied if δ computable | not applied |
   | v0.19 | applied (retrospective) | applied if δ computable | not applied |
   | v0.20 | applied (retrospective) | applied (δ computable) | not applied |
   | v0.21 | applied (retrospective) | applied (δ computable) | applied (calibration anchor) |
   | v0.22+ | prospective | prospective | prospective |
9. **References + Declarations** — extend citation chain to include v0.21 (SSRN 6815378) as direct upstream

---

## Required infrastructure work

**Code: `score_v1_6.py`** — a methodology-version scorer (not a phase scorer) that takes any phase's Phase A + Phase B raw outputs and applies the three v1.6 increments. ~200–300 lines. Reuses utilities from `score_vNN.py` series.

**Reference vocabularies (Increment 3 only).** Per-substrate JSON files in `~/aias/methodology/v1_6/reference_vocabs/`. Required for any retrospective Phantom scoring beyond v0.21.

**Pre-registration tag.** `v1.6-prereg-r1` locks the three increment specifications BEFORE the retrospective scoring is run. Standard pattern.

**OSF deposit path.** `osf.io/ec6wh/methodology/v1_6/` — distinct from phase-deposit paths.

---

## Locked decisions (v1.6-prereg-r1)

1. **Uniform-saturation threshold** — LOCKED: distinct C_P count = 1 in all 3 cells. Single operational rule. Strictest falsifiable form for the 6-LLM panel; catches v0.21 cleanly, rejects v0.20.

2. **Bootstrap specification** — LOCKED: n_bootstrap = 10,000; per-cell resampling with replacement; percentile CI (not BCa). Retrospective scoring uses methodology-level seed `SEED_V16_RETRO = 1621`; prospective phases v0.22+ set phase-level seeds at phase pre-reg.

3. **Phantom scope** — LOCKED: prospective-only from v0.22+ with retrospective scoring on v0.21 only. v0.16–v0.20 out of v1.6 retrospective scope (vocabulary construction cost prohibitive; v0.21 carries the empirical motivation).

4. **Paper packaging** — LOCKED: single paper covering all three increments. Matches v1.4 (Recognition + Recall) and v1.5 (multi-statistic C2 + two-channel Recall) precedents. >25pp split into v1.7 successor only if drafted length exceeds threshold.

5. **Naming convention** — LOCKED: `H_IdentityLoad_moderator` (Regime 4-dependent, retained from v1.5) and `H_IdentityLoad_Direct` (v1.6 introduction, evaluable independently of Regime 4 C2 conditions). Both names stay in the program; future phases pre-register either or both.

### Additional pre-reg locks (Batch B resolutions)

6. **Fifth verdict state** — LOCKED: `REGIME-4-UNAVAILABLE-AT-RECOGNITION` enters the Regime 4 verdict vocabulary, distinct from FALSIFIED. See Increment 1 routing change above.

7. **Recall-only pathway under uniform-saturation routing** — LOCKED: cell-level Regime-4 verdicts collapse to the single substrate-level verdict; `H_IdentityLoad_Direct` is the moderator-evaluation path; quadrant population and Iwachu cases are descriptive findings, not verdict components. See Increment 1.

8. **Increment 2 Cell C verdict logic** — LOCKED: monotonic-gradient check — Cell C δ must lie between Cell A δ and Cell B δ. Violation with both focal-cell CIs excluding zero → FALSIFIED. Failure with focal directions intact → PARTIAL. See Increment 2.

9. **Increment 2 INDETERMINATE rule** — LOCKED: brand-level `n_post_attrition < 5` in any focal cell (A or B). Cell C post-attrition shortfall defaults to "gradient check not evaluable" without forcing INDETERMINATE.

10. **Increment 3 reference vocabulary** — LOCKED: union of (panel) + (top-50 substrate market-share list, source pre-registered per substrate) + (prior-phase Phase B emergents cross-validated by market-share list). Phase-B-only candidates excluded. Breaks endogeneity hazard. See Increment 3.

11. **Increment 3 K threshold** — LOCKED: K = 6. Validity check: v0.21 Glossier R_phantom ≥ 6 required. Failure triggers pre-reg amendment, not silent re-tuning.

12. **Working title** — LOCKED: long form ("Substrate Pre-Screening, Independent Moderator Pathway, and Phantom Brand Persistence Phase B Extension"). Matches v1.5 named-increments title precedent.

13. **OSF deposit path** — LOCKED: `osf.io/ec6wh/methodology/v1_6/`. Distinct from phase-deposit paths.

14. **§5 table schema** — LOCKED: 6 rows × 7 columns. See §5 in paper structure above.

15. **§7 boundary application table** — LOCKED: 7 rows × 4 columns. See §7 in paper structure above.

---

## What v1.6 unblocks downstream

- v0.22+ phases under cleaner routing and independent moderator evaluation
- AIAS™ 1.0 synthesis paper under locked methodology
- Phantom Brand Persistence as a measured component of the multi-component AI Availability construct (rather than a discovery-level observation)
- Direct test of the IL moderator hypothesis with bootstrap confidence intervals
- Cleaner Regime 4 verdict semantics (FALSIFIED-on-uniform-saturation distinct from FALSIFIED-on-differential-cell-failure)

---

## Estimated effort

- **Outline finalization** — complete (15 locked decisions; v1.6-prereg-r1 ready)
- **Increment 1 drafting + retrospective classification** — 1–2 sessions
- **Increment 2 drafting + bootstrap implementation + retrospective scoring** — 2–3 sessions
- **Increment 3 drafting + reference vocab construction (v0.21 calibration only)** — 2–3 sessions
- **§5 joint retrospective scoring table** — 1 session
- **§6 implications + §7 methodology log** — 1 session
- **Build pipeline (`build_paper_v1_6.py`, .md, PDF)** — 1 session
- **SSRN deposit + memory backfill** — bundled

Total: ~10–13 working sessions to ship.

---

## Open questions — RESOLVED at v1.6-prereg-r1

All items in the prior "open questions" list resolved by the Locked Decisions section above. Nothing outstanding before pre-reg lock.

---

*Working notes; not for distribution.*
