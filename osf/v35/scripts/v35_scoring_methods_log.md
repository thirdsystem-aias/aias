# v0.35 Scoring Methods Log

Phase: v0.35 — Naive-Phantom × CPC Omnibus
Lock: `v0.35-prereg-r1` @ `8b254f2` (immutable)
Scorer: `scripts/score_v35.py` (canonical) → copied to `osf/v35/scripts/score_v35.py`
Inputs: frozen t1 omnibus (v0.19–v0.23; 112 brand units; canonical 6-model panel).
No new LLM acquisition (v0.33 re-analysis pattern).

This log records implementation choices not fully specified by the lock. Per the operator
brief, choices with no analytic discretion are recorded as **methods notes**; choices that
rise to a genuine judgment call (resolving spec ambiguity in a way that changes the number)
are recorded as **DEVIATIONS** and surfaced in the verdicts JSON `deviations` array and the
report-back. The locked content-module `DEVIATIONS` block is immutable and was **not** touched.

---

## Contemporaneous DEVIATIONS (scoring-time judgment calls)

### D1 — Pooled Cliff's delta = within-substrate cross-pair pooling
The lock specifies "pooled Cliff's delta" with "within-substrate stratified permutation" but
does not pin the pooling rule. **Resolution:** the observed pooled δ is the stratum-pooled
statistic over **within-substrate cross pairs only**:

    δ = Σ_s [#{phantom > non-phantom} − #{phantom < non-phantom}]_s  /  Σ_s (n_phantom,s · n_non,s)

i.e. pair-count weighted across substrates, and the **observed statistic itself respects
strata** (no cross-substrate pairs are formed). The permutation null shuffles phantom/non-
phantom labels independently within each substrate, holding the per-stratum phantom count
fixed. Rejected alternative: pooling all 29×55 cross pairs ignoring substrate, which would
include pairs the within-substrate null can never generate and break exchangeability /
p-value validity. This is the load-bearing estimand choice.

### D2 — Rank-residualization fit population = all analyzable units
The gate residualizes CV-CPC on the control (C_P; recall-mean) within substrate. **Resolution:**
the rank regression is fit over **all analyzable units in the substrate (phantom + non-
phantom together)**, and the phantom-vs-non contrast is then taken on the residuals. Fitting
on non-phantoms only and projecting phantoms onto that line would change the estimand (a
leverage-sensitive extrapolation) and is not stratified-permutation-exchangeable. Fitting on
all analyzable units keeps the phantom contrast *in* the residual, which is what the gate tests.

### D3 — Cross-substrate per-substrate delta = the raw arm
`H_Phantom_Cross_Substrate` reports per-substrate δ; the lock does not say raw or residualized.
**Resolution:** the **raw arm (CV-CPC)** per-substrate δ. Rationale: the cross-substrate test
is a sign-coherence check on the same mechanical signal as the raw PRIMARY (manipulation
check), and the lock names it "per-substrate delta" without the residual qualifier. The exact
binomial sign test runs on the eligible (≥4 analyzable) substrates only; the full 5-substrate
δ table is reported regardless.

---

## Methods notes (no analytic discretion)

- **Metric.** CV-CPC = 1/(1+CV), CV = `sd_pop/mean` of the 6-model per-brand recall vector
  (population SD, ddof=0, per `score_v0_31`). Computed for **every non-all-zero unit, including
  below the v1.7 FLOOR=1.0**: per METRIC_DEFINITION + ENUMERATION_ATTRITION the floor governs
  *instrument adoption* only, not the *characterization* computation. Only all-zero recall
  (mean = 0 → CV undefined) is excluded. `cpc_score` is blank for `status=="undefined"` rows in
  `v31_cpc.csv` (suppressed by the floor), so phantom CV-CPC is **recomputed** from the
  re-extracted recall; defined-unit CV-CPC reproduces the frozen `cpc_score` exactly
  (max|err| = 0.00e+00 over 55 units).
- **C_P** = recognition count = Σ of the 6-model binary recognition vector, 0..6
  (`score_v33.recognition_vectors()` path).
- **Phantom flag** = `status=="undefined"` in `osf/v31/data/v31_cpc.csv`, the frozen v0.31
  archive flag (provenance only; v1.6 method anchor). Asserted equal to `(mean_r < FLOOR)` for
  all 112 units (0 disagreements). Equals v0.33 `H_Provider_Phantom` (`not defined`, n=57) and
  the v0.34 t1 phantom set.
- **Cliff's delta tie handling.** Ties contribute 0 to the numerator (standard); group1 =
  phantom, so the mechanism prediction (phantoms lower CV-CPC) is δ < 0.
- **Permutation p-value.** Two-sided via |δ|: p = (1 + #{|δ_perm| ≥ |δ_obs|}) / (N_MC + 1),
  Phipson–Smyth add-one, matching `score_v33`/`score_v34`. N_MC = 10,000.
- **Verdict thresholds.** CONFIRMED |δ| ≥ 0.30 & p < 0.05; FALSIFIED |δ| < 0.15 **or** sign
  opposite the mechanism at p < 0.05; else MARGINAL. Implementation precedence: opposite-
  direction significance is checked **before** the magnitude-CONFIRMED branch, so a significant
  wrong-direction effect cannot "confirm" a mechanism-predicted signature even if |δ| ≥ 0.30.
- **Rank residualization mechanics.** OLS of `rankdata(CV-CPC, 'average')` on
  `rankdata(covariate, 'average')` + intercept, within substrate, residuals taken; covariate
  with zero rank variance or n < 3 → centered ranks (no-op), mirroring `score_v34.residualize`.
  Saturation note: recognition is saturated (C_P constant among analyzable units) in v0.21,
  v0.22, v0.23 → the C_P control is a no-op there → residual ≈ raw signal; the recall-mean
  control removes exactly the axis that defines the phantom flag → strong attenuation. This is
  the structural driver of the observed control flip (gate UNDETERMINED), the pre-committed
  modal outcome ("the flip itself is the finding, routed to v1.8").
- **v0.22 pooled-only.** 1 analyzable phantom (Rivian) < the ≥4 floor → excluded from the
  per-substrate (cross-substrate) test, included in the pooled raw/gate arms per
  ENUMERATION_ATTRITION. Its stratum has min-cell-size 1 (1 phantom / 14 non-phantom): valid,
  low-information, coarsely quantized null (15 within-stratum states); pooled with the other
  four large strata the effect is negligible.
- **Cross-substrate underpower.** 4 eligible substrates → exact binomial cannot reach p < 0.05
  even at 4/4 concordance (4/4 → p = 0.125). Pre-acknowledged in the lock; reported regardless.
- **t2 stability (TERTIARY).** Same pooled contrasts on the v0.34 t2 wave (`score_v34.wave_t2()`);
  phantom membership **frozen at t1**, CV-CPC recomputed from t2 recall; units with all-zero t2
  recall drop from the t2 contrast. WALLED — descriptive only, no thresholds, quarantined from
  all PRIMARY/SECONDARY verdict logic.
- **RNG.** Base seed 280400 (program-canonical). Per-statistic derived seeds so each null is
  independent of execution order: raw 280400, gate-C_P 280410, gate-recall-mean 280420, t2
  280430; LOSO raw 280401+i, LOSO gate 280440+i (recall-mean arm +100). N_MC = 10,000 each.
- **Sensitivity.** LOSO on both PRIMARY verdicts (leave-one-substrate-out; fragile if the full
  verdict does not survive every leave-out). Threshold reruns re-decide the PRIMARY verdicts at
  CONFIRMED magnitude thresholds 0.20 and 0.40 (FALSIFIED threshold 0.15 and p held; statistic /
  null unchanged), descriptive.

---

## STEP 1 reconciliation gate — result

Binding, run before any contrast; any mismatch halts the phase. **PASS.**

1. **v0.33 deposit bit-for-bit** — sha256 of brand-sorted consumed per-model recall and
   recognition vectors vs `osf/v33/data/v33_eta2.csv`: match in all 5 substrates (112 units).
2. **v1.7 anchor** — v0.20/0.21/0.22 recall vs `v1_7_cpc.csv` `r_per_model` by model name
   (reused `score_v33.reconciliation_gate`): checked 72, mismatches 0.
3. **Phantom-flag consistency** — `status=="undefined"` ⟺ `mean_r < FLOOR`: 112 checked,
   0 disagreements.

Full hashes in `osf/v35/data/v35_reconciliation_log.txt`.

---

## Result summary (see `osf/v35/v35_verdicts.json`)

- **GATE H_Phantom_Beyond_Presence: UNDETERMINED (control flip).** C_P control CONFIRMED
  (δ_resid = −0.797, p < 1e-4); recall-mean control FALSIFIED (δ_resid = +0.068, p = 0.65).
  The flip is the finding; routed to v1.8. LOSO-stable (the flip persists across leave-outs).
- **RAW H_Phantom_CPC_Signature (manipulation check): CONFIRMED** (δ = −0.838, p < 1e-4;
  phantoms lower CV-CPC, mechanism direction). LOSO survives. Treated as confirming the
  pipeline reproduces the known mechanical recall-coupling, not as a Consistency-flavored
  signature.
- **SECONDARY H_Phantom_Cross_Substrate: UNINFORMATIVE** (4/4 concordant negative, p = 0.125;
  structurally underpowered). Per-substrate raw δ: v0.19 −0.938, v0.20 −0.956, v0.21 −0.886,
  v0.22 −1.000, v0.23 −0.622.
- **TERTIARY H_Phantom_t2_Stability: DESCRIPTIVE (walled)** — t2 raw δ = −0.815 (p < 1e-4);
  consistent with t1; no inferential weight.
