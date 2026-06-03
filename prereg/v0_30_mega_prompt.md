# v0.30 (CPC.01) — CPC Consistency Instrument Analysis Protocol

> **Instrument-specification pilot (analysis pre-registration).** v0.30 specifies
> and stress-tests a coefficient-of-variation Consistency instrument (CPC) on
> existing anchored data, to recommend a normalization choice to the **v1.7**
> methodology lock. Confirmatory scope = **CPC_model** (cross-model dispersion of
> recall across the fixed six-model panel). CPC_platform is defined but **not**
> measured. **No new LLM calls. No brand selection. No acquisition.** This is an
> analysis pre-registration: locked at a git tag *before any scoring code runs*.

---

## Overview

**Objective:** Specify CPC — a cross-model dispersion measure of recall — and
stress-test it on reused anchored data, to hand the v1.7 lock a validated
normalization. The designed result is **F2-then-F3**: show raw cross-model CV is
contaminated by Presence level, then show a level-correction neutralizes it.

**Protocol lock:** v1.6 (reused data sits under v1.6-era locks). The deliverable
is a normalization **recommendation to the v1.7 lock**.

**Data (reused verbatim — single source, do not re-acquire):** the locked
24-brand registries and the already-deposited Phase A recognition + Phase B
two-channel recall CSVs from:

| Phase | Substrate | SSRN |
|---|---|---|
| v0.18 | indie fragrance | 6806558 |
| v0.22 | automotive (heritage ceiling) | 6829118 |
| v0.24 | B2B SaaS | 6838802 |

**Reference panel (fixed from v0.17 onward, six models — the FULL reference
population):** claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini,
gemini-2.5-flash, gemini-2.5-flash-lite. Panel dispersion uses **population SD
(÷6)**.

---

## Scope lock (non-negotiable)

- **No new LLM calls.** Every input already exists in the v0.18 / v0.22 / v0.24
  deposits. Do not run acquisition; do not call any model.
- **No brand selection, no acquisition.** Registries are reused verbatim.
- **Recall is the primary CPC input.** Recognition enters only as (i) the F1
  coverage comparator and (ii) the independent level variable L(b) = Phase A
  Presence C_P.
- **CPC_platform deferred.** Specified for completeness; not measured (no
  platform harness in the pipeline).

---

## Operational definitions

- **Per-cell recall signal** s(b,m) = fraction of Phase B recall probe-channel
  opportunities (6 probes × 2 channels) in which brand b surfaced in model m's
  response. Bounded [0,1]. Each brand → a 6-vector across the panel models.
- **Panel dispersion** uses **population SD (÷6)** — the six models are the full
  reference population, not a sample.
- **CPC_raw** = SD_m[s] / mean_m[s] — cross-model CV of recall; lower = more
  consistent.
- **CPC_corr (primary, level-corrected)** = SD_m[s] / √(μ(1−μ)), μ = mean_m[s].
  The denominator is the maximum attainable SD for any [0,1] variable with mean
  μ (Bhatia–Davis), so **CPC_corr ∈ [0,1]** = dispersion as a fraction of the
  maximum possible at that level.
- **Robustness variant (reported, not primary):** level-residualized CV (CV
  regressed on μ, residuals retained).
- **Level variable** L(b) = Phase A Presence C_P (recognition-based AIAS 1.0
  score) — deliberately a *different* signal than the recall mean inside CPC, so
  the confound test is non-tautological (tests whether CPC is redundant with
  Presence).
- **Degenerate-cell rule:** a brand is **CPC-UNDEFINED** if μ = 0 (recall floor)
  or μ ≥ 0.98 (recall ceiling); excluded from CPC distributions. The **coverage
  rate** (share of brands with defined CPC) is itself a primary outcome (F1).
- **CPC_platform (specified, deferred):** the same dispersion taken across
  deployment surfaces (consumer app vs API, with their retrieval / system-prompt
  augmentation) rather than across model weights. Needs a platform harness not in
  the pipeline; deferred.

---

## Hypotheses + falsification

All four are **confirmatory** (CPC_model scope). F2-then-F3 is the load-bearing
pair.

- **H_CPC_Computable (F1):** recall yields usable consistency where recognition
  saturates. **CONFIRM** if recall CPC-coverage ≥ 50% of brands in all three
  substrates AND recall coverage > recognition coverage on automotive.
  **FALSIFIED** if recall coverage < 50% in any substrate, or recall ≤
  recognition coverage on automotive.
- **H_CPC_LevelConfound (F2):** raw CV is contaminated by Presence level.
  **CONFIRM** if significant |ρ(CPC_raw, L)| ≥ 0.30 in ≥ 2 of 3 substrates.
  **FALSIFIED** if not significant or |ρ| < 0.30 across.
- **H_CPC_LevelCorrected (F3, headline):** the correction removes the confound.
  **CONFIRM** if |ρ(CPC_corr, L)| < 0.20 AND ≥ 50% attenuation vs CPC_raw, in
  ≥ 2 of 3 substrates. **FALSIFIED** if attenuation < 30% or corrected ρ remains
  significant at raw magnitude.
- **H_CPC_SubstrateVariation (F4):** consistency is substrate-conditioned.
  **CONFIRM** if Kruskal–Wallis across the 3 substrates' CPC_corr is significant
  at p < .05. **FALSIFIED** if no significant difference.
- **Exploratory (non-confirmatory, no figure):** recognition-vs-recall CPC rank
  concordance, to inform the v1.7 channel decision.

---

## Registered predictions

- **Designed outcome:** F2 confirms then F3 confirms — demonstrate the confound,
  then neutralize it, handing v1.7 a validated normalization.
- **Fallback (pre-committed):** if F3 FAILS, the recommendation to v1.7 is the
  residualized-CV variant or an ICC / agreement-coefficient reformulation; that
  failure path is a legitimate publishable result.
- **Substrate:** automotive (heritage ceiling) predicted to show the largest
  recognition→recall coverage gap (F1) and the highest raw-CV inflation.

---

## Scoring (downstream, automated)

`scripts/score_v30.py` reads the reused Phase A + Phase B CSVs for the three
substrates and applies the locked decision rules — **no acquisition step**:

1. Build s(b,m) per cell; compute μ and population SD (÷6); apply the
   degenerate-cell rule; record defined-CPC coverage per substrate (**F1**).
2. CPC_raw = SD/μ; CPC_corr = SD/√(μ(1−μ)); residualized-CV variant.
3. **F2:** Spearman ρ(CPC_raw, L) per substrate (L = Phase A Presence C_P);
   confound present if |ρ| ≥ 0.30 in ≥ 2/3 substrates.
4. **F3:** Spearman ρ(CPC_corr, L) + attenuation vs raw; neutralized if
   |ρ| < 0.20 AND attenuation ≥ 50% in ≥ 2/3 substrates.
5. **F4:** Kruskal–Wallis across the 3 substrates' CPC_corr (α = .05).
6. Exploratory recognition-vs-recall CPC rank concordance (no figure).
7. BCa 95% CIs (10k, seed 280400) on the confound correlations; write
   `osf/v30/v30_cpc_verdicts.json` and `osf/v30/data/v30_cpc.csv`.

---

## Validation checks (post-analysis)

1. **Input integrity:** sha256 + row/column counts of every reused v0.18 / v0.22
   / v0.24 Phase A + Phase B CSV match the deposited files.
2. **Panel membership:** all six reference-panel models present in every reused
   CSV.
3. **Coverage + degenerate cells:** defined-CPC coverage rate and degenerate-cell
   counts (μ = 0 / μ ≥ 0.98) independently re-derived per substrate.
4. **No-new-calls attestation:** confirm no acquisition ran and no model was
   called; the analysis consumed reused data only.
5. **CPC_corr range:** all defined CPC_corr ∈ [0,1] (Bhatia–Davis bound).
