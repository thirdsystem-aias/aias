# AIAS v0.9 — Pre-registration

**Study:** Longitudinal re-baseline of v0.6 categories at t₂
**Categories:** pm, running, oliveoil, skincare, finance
**Pre-registration version:** v09_rebaseline_v1.0
**Lock date:** 2026-05-06
**Status:** Locked before data collection per AIAS Presence Measurement Protocol v1.1 §6.4
**Decision note:** docs/v09_DECISION_NOTE.md (commit e6428a4)

---

## 1. Purpose and design

This pre-registration covers the v0.9 re-measurement of the five v0.6 baseline categories at a second time point. It closes Phase 2 by giving each baseline category a t₂ and provides the data spine for Phase 3 (construct validity, requiring ≥3 categories at 2 time points).

Hypotheses are evaluated on the **matched 2-model subset** (claude-sonnet-4-6 and gpt-5.4-mini) per Decision #1. The four parallel-baseline models (claude-opus-4-7, gpt-5.5, gemini-2.5-flash, grok-4-1-fast) report as a parallel new baseline, outside the longitudinal frame.

## 2. Hypotheses

### H1 — Brand-level drift noise floor
On the matched subset, across all 5 categories: ≥70% of registry brands show a t₁→t₂ delta within ±5pp; ≥90% within ±10pp.

- Confirmed: both thresholds met
- Partial: one met
- Disconfirmed: neither

**Rationale:** ±5pp is half the v0.6 confidence band; ±10pp matches the band. Calibrated to the empirical noise floor observed at v0.6.

### H2 — Top-of-leaderboard stability
Per category on the matched subset: top-3 brands at t₁ remain in top-5 at t₂.

- Confirmed: 5/5 categories
- Partial: 3–4/5
- Disconfirmed: ≤2/5

**Rationale:** Position stability of dominant brands is a strong test of measurement reliability and the headline-finding artifact in AIAS reports.

### H3 — Pattern 1 replication (discourse coherence)
The variance-rank-order across the 5 categories at t₂ has Spearman ρ ≥ 0.7 with t₁.

- Confirmed: ρ ≥ 0.7
- Partial: 0.4 ≤ ρ < 0.7
- Disconfirmed: ρ < 0.4

**Rationale:** Operationalizes Pattern 1 (discourse coherence drives within-category variance) as preservation of relative variance ordering across categories. Treats the qualitative v0.6 pattern as a numerically testable claim.

### H4 — Pattern 6 phantom-brand decay (Mint, personal_finance)
Mint's matched-subset mention rate at t₂ vs t₁:

- Decay: ≤ −5pp
- Stability (predicted): within ±5pp
- Anti-decay: ≥ +5pp

**Rationale:** v0.6 documented phantom persistence as a corpus-aging mechanism; one additional time point shouldn't be enough to push Mint out. Stability is the predicted result. A clear decay would indicate retraining purges or a different mechanism than v0.6 hypothesized.

### H5 — Pattern 4 discourse-language bias replication
Spanish olive oil aggregate mention rate ≤ 25% of regional production share AND K-beauty aggregate mention rate in skincare ≤ 5%.

- Confirmed: both thresholds met
- Partial: one of two met
- Disconfirmed: neither met

**Rationale:** v0.8 established Pattern 4 via designed-for-test on knives. v0.9 provides triangulation against v0.6 categories where Pattern 4 was first observed.

### H6 — Cross-model spread stability
Per-brand spread between claude-sonnet-4-6 and gpt-5.4-mini at t₂ correlates with t₁ at Pearson r ≥ 0.7 within each category.

- Confirmed: r ≥ 0.7 in ≥4/5 categories
- Partial: r ≥ 0.7 in 2–3/5
- Disconfirmed: r ≥ 0.7 in 0–1/5

**Rationale:** Stable inter-model relative behavior implies divergent shifts within a brand are AI behavior changes rather than measurement noise.

## 3. Exploratory observation (not pre-registered)

**Mode distribution stability.** With retroactive mode classification of v0.6 data per Decision #2, the v0.9 analysis will compare mode-share distributions at t₁ vs t₂. This is treated as an exploratory observation rather than a formal hypothesis: the threshold for "meaningful shift" cannot be calibrated without prior longitudinal mode data, and a guessed threshold would be methodologically weaker than honest exploration. v0.10 may pre-register a mode-stability hypothesis with calibrated thresholds derived from v0.9 baselines.

## 4. Pre-registered methodological risks

- **v0.6 finance metadata stamp.** Carries `v2-skincare` due to pre-Phase-2 runner constant carryover. Verified cosmetic by raw_response inspection (decision note §3). If finance shows aberrant deltas, reported separately with the anomaly disclosed.
- **Undisclosed model updates.** If any matched-subset model has been silently updated between t₁ (April 29–30, 2026) and t₂ (May 2026), longitudinal claims for that model are compromised. model_version metadata is stamped in every row; any provider-side changes since the v0.6 measurement window are disclosed in the report.
- **Rate-limit / API failure.** Runner handles retries. Categories with <95% completion at end of run are re-run before analysis.
- **Parallel-baseline failure.** Independent of the longitudinal claim. If a parallel-baseline model fails to complete, that model's parallel baseline is deferred to a later wave.

## 5. Scoring rubric

For each hypothesis, the analysis script computes the test statistic and assigns one of {Confirmed, Partial, Disconfirmed} per the thresholds above. Results published as Table 1 in the v0.9 SSRN paper, mirroring the v0.7/v0.8 pre-reg outcomes-table format.

## 6. Lock

This pre-registration is locked in git as of the next commit, before any t₂ measurement runs. Any deviation after lock requires explicit amendment with rationale.
