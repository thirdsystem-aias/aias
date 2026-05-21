# AIAS v0.19 — OSF Deposit

**Phase:** v0.19 — C3 Rescue on Audiophile Headphones Substrate
**Methodology base:** AIAS™ Presence Measurement Protocol v1.4 (SSRN 6799479)
**Pre-reg tag:** `v0.19-prereg-r1`
**Pre-reg commit:** `2cbd36c6ed53b99c65490765d3d9f1a2eb49b890`
**Branch:** `v0.19-c3-rescue`
**Status (as of this deposit):** PRE-ACQUISITION — pre-registration locked; Phase A / Phase B acquisition pending.
**Author:** Pablo Ulpiano González Castro
**Author affiliations:** School of Visual Arts, MPS Branding Program (primary); Third System™ (research entity).

---

## Phase summary

v0.19 is the C3 rescue phase of the AIAS empirical program. Substrate: audiophile headphones, English-language anchored, split into two same-IL cells (Heritage / Boutique) by audiophile headphone product-line emergence year. Three pre-registered hypotheses:

- **H_C3_Within_Cell_Variance** (primary, load-bearing) — per-cell Spearman ρ between Phase A C_P and Phase B category-anchored mention count meets the C3 threshold in ≥ 1 of 2 cells.
- **H_Recognition_Recall_Dissociation_Replication** (secondary, load-bearing) — Iwachu-pattern cases (C_P ≥ 5/6 ∧ category-anchored mentions ≤ 2/18) replicate on a third substrate family beyond v0.17 Iwachu (Japanese-cell kitchenware) and v0.18 indie fragrance.
- **H_CulturalFootprint_Dissociation_Sensitivity** (descriptive, NOT load-bearing) — Type 1 (category-channel-preferred) and Type 2 (cultural-channel-preferred) dissociation cases documented for v1.5 methodology development.

Design pressure response: C3 has never been substantively cleared on the program; v0.18's IL-gradient cell design produced ceiling/floor effects in both Recognition and Recall. v0.19 selects an audiophile substrate engineered for within-cell variance in both dimensions, with the IL moderator question deferred to a future phase.

---

## Program context

v0.19 is the 9th empirical phase of the AIAS™ Presence Measurement Protocol, succeeding v0.16, v0.17, and v0.18 on the substantive track, and operating under methodology v1.4 (Recognition × Recall multi-component construct).

Empirical lineage:

| Phase | Substrate | SSRN | Verdict |
|---|---|---|---|
| v0.16 | Kitchen knives (cross-language EN/JP/FR) | 6791999 | PARTIAL |
| v0.17 | Premium kitchenware (Japanese cell) | 6802261 | FALSIFIED (panel inadequacy); Iwachu Recognition × Recall dissociation as methodological headline |
| v0.18 | Indie fragrance (EN, 3-cell IL gradient) | 6806558 | All three hypotheses PARTIAL |

Methodology lineage:

| Version | Increment | SSRN |
|---|---|---|
| v1.2 | Four-Regime Taxonomy | 6761698 |
| v1.3 | Phase A Pivot-Validation Specification | 6797679 |
| v1.4 | Recognition × Recall Decomposition + Multi-Component AI Availability | 6799479 |

---

## Deposit contents

### Pre-registration artifacts (locked at `v0.19-prereg-r1`)

- `PRE_REGISTRATION_v0_19.md` — canonical pre-registration document. Substrate definition, panel composition, hypothesis specifications, decision-rule cascades, verdict matrices, DEVIATIONS protocol carryforward + new rules.
- `panel_registry_v0_19.csv` — locked 16-brand panel (8 Heritage + 8 Boutique), with country, founding year, product-line start year, cross-cultural flags, borderline flags, cascade order.
- `thresholds_v0_19.json` — locked decision-rule thresholds in machine-readable form. C1 floor, C2 modal-share thresholds, C3 Spearman ρ + bootstrap CI, Iwachu pattern criteria, dissociation count thresholds, cultural-footprint K thresholds, cross-cultural robustness Δρ threshold, verdict matrices.

### Pre-registered analysis tooling

- `score_v0_19.py` — canonical scoring pipeline. Implements C1 panel adequacy check, C2 within-cell variance check, C3 Spearman ρ with 10,000-resample percentile bootstrap CI, Iwachu-pattern case identification, cross-cultural robustness Δρ analysis (DEVIATIONS Rule 6), cultural-footprint Type 1 / Type 2 sensitivity extraction. Verdict routing per §5 matrices. RNG seed 42 locked.
- `acquire_v0_19.py` — canonical acquisition tooling. Generates Phase A query batch (96 queries) and Phase B query batch (36 queries) from the locked panel and thresholds; parses raw model responses into the schemas expected by `score_v0_19.py`. Implements v1.4 canonical brand-mention detection rules (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins).

### Operations log

- `DEVIATIONS.md` — log of any departures from the pre-registered protocol during acquisition. Empty at pre-reg lock state; entries added with timestamp + commit reference if/as they arise during acquisition.

### Acquisition data (post-acquisition)

- `phase_a_queries.jsonl` — 96 Phase A queries (generated at pre-reg state for transparency)
- `phase_b_queries.jsonl` — 36 Phase B queries (generated at pre-reg state for transparency)
- `phase_a_responses.jsonl` — raw model responses (post-acquisition)
- `phase_b_responses.jsonl` — raw model responses (post-acquisition)
- `phase_a_results.csv` — parsed Phase A C_P data (post-acquisition)
- `phase_b_results.csv` — parsed Phase B mention data (post-acquisition)

### Post-acquisition shipping artifacts

- `Third_System_brand_format_report_v0_19.pdf` — Third System format report (post-acquisition)
- `v0_19_ssrn_paper_draft.md` — v0.19 SSRN paper draft (post-acquisition)
- `figures/` — scoring-output figures (post-acquisition)

---

## How to reproduce the v0.19 pipeline from this deposit

1. **Clone the pre-reg lock state.** Checkout commit `2cbd36c6ed53b99c65490765d3d9f1a2eb49b890` on branch `v0.19-c3-rescue`, or download the locked artifacts (pre-reg + registry + thresholds + scoring + acquisition tooling) from this OSF deposit.

2. **Generate query batches** against the locked panel:
   ```
   python3 acquire_v0_19.py gen-phase-a
   python3 acquire_v0_19.py gen-phase-b
   ```

3. **Execute queries** against the locked reference panel models (claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite) and capture responses in JSONL format preserving `query_id`, `phase`, `brand`/`frame`, `panel_model`, `response`.

4. **Parse responses** into the canonical analysis schemas:
   ```
   python3 acquire_v0_19.py parse-phase-a phase_a_responses.jsonl
   python3 acquire_v0_19.py parse-phase-b phase_b_responses.jsonl
   ```

5. **Run the canonical scoring pipeline**:
   ```
   python3 score_v0_19.py
   ```
   The script outputs verdict per §5 matrices of the pre-registration document.

The pipeline is deterministic up to LLM-provider variability between query runs. Bootstrap RNG seed is fixed at 42; given identical Phase A / Phase B results, the scoring output reproduces exactly.

---

## Declarations

**Declaration of interest.** Pablo Ulpiano González Castro is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS™ Presence Measurement Protocol is the author's independent academic research, conducted outside the scope of employment, in his role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System™. Samsung had no role in the design of this pre-registration or the v0.19 analysis. The panel substitution from AKG (Samsung-owned since 2016) to Denon is documented in the pre-registration §2.3 for audit trail.

**Funder.** Self-funded.

**Ethics.** Not applicable; no human subjects. The research uses publicly accessible LLM APIs queried with non-personal, category-anchored prompts.

**Trademark notice.** AIAS™ and Third System™ are trademarks of the research program.

**License (data and code).** Data and code deposited here are released under CC-BY 4.0 for data, MIT for code, unless superseded by OSF project-level license setting.

---

## Correspondence

pablou@pablou.com · pablou.com · ORCID: [0009-0003-8968-9990](https://orcid.org/0009-0003-8968-9990)
