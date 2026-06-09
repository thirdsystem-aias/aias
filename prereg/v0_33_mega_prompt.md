# v0.33 - Provider-Asymmetric CPC - Re-Analysis Protocol

**AIAS™ Measurement Program · Third System™**
**Pre-registration tag:** `v0.33-prereg-r1` · **Phase type:** re-analysis (secondary analysis; no LLM acquisition)
**Frozen source:** v0.31 (SSRN 6880959) · **Instrument:** CV-CPC (v0.30 origin, v1.7 lock, *not adopted* - walled)

> This phase runs **no acquisition**. There is no Phase A recognition probe set and no
> Phase B recall query set. The cloned measurement sections (`## Phase A — Recognition`,
> `## Phase B — Recall`, `## Acquisition protocol`) are removed; the recompute manifest
> below replaces them. There is **no reachability / snapshot-resolution gate** in a
> re-analysis - the frozen-input manifest is the registry.

---

## Scope

Test whether the v0.31 CV-CPC quantity carries systematic **between-provider** structure,
and - the gating question - whether that structure **exceeds the provider structure already
present in Presence**. CV-CPC is analyzed strictly as computed in v0.31; no claim that it is
a valid Consistency instrument (v1.7 falsified it as Presence-coupled, rho = 0.77).

Distinct from v0.32: v0.32 tested *within-provider* CPC fragility *across versions over time*
(gpt-4o -> gpt-5.x). v0.33 tests *between-provider* CPC asymmetry at a *fixed snapshot*
(gpt-4o, the canonical six). Orthogonal dimensions; do not conflate.

---

## Frozen-input manifest

Five panel-uniform omnibus substrates (the only ones carrying the canonical six-model panel);
**112 brand units** total:

| Phase | Substrate | Brands | Input file | Shape | Path |
|---|---|---|---|---|---|
| v0.19 | audiophile headphones | 16 | `osf/v19/phase_b_results.csv` | brand, panel_model, frame, mentioned, rank | A |
| v0.20 | skincare | 24 | `osf/v20/phase_b_results.csv` | model, frame_id, channel, frame_text, response_text (brand not pre-coded) | B |
| v0.21 | cosmetics | 24 | `osf/v21/phase_b_results.csv` | (as v0.20) | B |
| v0.22 | automotive | 24 | `osf/v22/phase_b_results.csv` | (as v0.20) | B |
| v0.23 | premium spirits | 24 | `osf/v23/data/v23_phase_b_scored.json` | model_id, brand_mentions{brand_id:0/1}; recognition as r_level | C |

**Descriptive-only (walled):** v0.18 indie fragrance (canonical-6 but 3-frame geometry).
**Excluded:** v0.16 (14-model legacy, no per-model recall); v0.17 (unscored); v0.24 (off-panel models).

---

## Per-model recompute (3 extraction paths + brand matcher)

v0.31's published outputs are brand-collapsed (`v31_cpc.csv` has `mean_r`, `cpc_score`, no
per-model vector). Both **per-model recall** and **per-model Presence (C_P)** must be
recomputed from the raw files above by re-running v0.31's extraction:

- **Path A (v0.19):** `panel_model` + `mentioned`/`rank` are per-model already; pivot to x_{b,m}.
- **Path B (v0.20-22):** brand is *not* pre-coded - detect via **v0.31's certified brand
  matcher** (carried-forward dependency) against `response_text`, then pivot per `model`.
- **Path C (v0.23):** parse `brand_mentions` per `model_id`; **normalize recognition `r_level`
  to binary** (same normalization the Presence path needs).
- **Presence (C_P):** recompute per-model from Phase A recognition - v0.19 `recognition_yes`,
  v0.20-22 `recognized`, v0.23 `r_level`->binary. Gating input for Beyond_Presence.

**Reconciliation guardrail.** Recomputed v0.20/0.21/0.22 per-model recall vectors **must
reproduce `osf/methodology/v1_7/data/v1_7_cpc.csv` `r_per_model` bit-for-bit.** Mismatch = a
computational-reproducibility note in the OSF README (not a DEVIATIONS entry); halt until
resolved. **Scope limit:** this anchor covers only v0.20/0.21/0.22. v0.19 and v0.23 have no
independent external anchor - correctness rests on v0.31's extraction-function provenance alone
(state in the README; do not overclaim).

---

## Decomposition

Per brand b: per-model values x_{b,m} over the six models; provider p(m) in {Anthropic, OpenAI,
Google}. One-way layout, provider as 3-level factor, 2 replicates/level.

- **Between-provider variance share:** eta^2_b = SS_between(provider) / SS_total. Summarize as
  mean eta^2 over the 112 brand units and per-substrate.
- **Within-provider CPC:** within-pair agreement = 1 - normalized |x_m1 - x_m2| per provider,
  averaged over brands per substrate.
- **Presence guardrail (gate):** identical eta^2 decomposition on raw Presence (C_P);
  **delta_eta2 = eta^2_CVCPC - eta^2_CP** is the decisive statistic.

---

## Null + robustness

- **PRIMARY null:** per-brand label space is exactly enumerable (6 models -> 3 labeled pairs =
  6!/(2!2!2!) = 90). Population test = Monte Carlo resampling from the per-brand exact null
  spaces, >= 10,000 draws, one-sided. Same null applied to delta_eta2.
- **Ordinal null:** Kendall's W across the 5 substrates; exact null (6^5 = 7,776 joint rank
  arrangements). Report raw W + provider rank table descriptively (a null W is uninformative at N=5).
- **Robustness:** leave-one-substrate-out (LOSO) over the 5 substrates for the PRIMARY verdict.

---

## Scoring

Outputs `osf/v33/v33_verdicts.json`: per-hypothesis verdict against the locked criteria in the
content module's `HYPOTHESES`; plus eta^2_CVCPC, eta^2_CP, delta_eta2, permutation p-values,
Kendall's W, and LOSO robustness. Verdicts: CONFIRMED / FALSIFIED / UNDETERMINED.

---

## Deviations

*(empty at r1 - the substrate set was corrected to the 5-substrate omnibus before lock; no Entry 0.)*
