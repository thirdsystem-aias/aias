# v0.29 — Synthesis Assembly Spec
### (replaces the cloned acquisition mega-prompt; locked at `v0.29-prereg-r1`)

**There is no acquisition.** v0.29 (CV.05) is a synthesis. It assembles a
Campbell-Fiske convergent–discriminant matrix from two already-locked component
verdicts and computes one new quantity — the C3 gap. **No LLM probes are run.**
The six-model reference panel and both external instruments are inherited as
published. This file documents the assembly procedure that stands in for the
Phase A / Phase B acquisition prompt.

## Inputs (inherited, locked)
- **Convergent** — `osf/v25/v25_verdicts.json`
  ρ(C_P, Google Trends) = 0.74, p < 0.001  ·  v0.25, SSRN 6842138  ·  `H_CV_Primary` CONFIRMED
- **Discriminant** — `osf/v26/v26_verdicts.json`
  ρ(C_P, Amazon BSR) near-zero / non-significant  ·  v0.26, SSRN 6847678  ·  `H_PV_Primary` FALSIFIED (the falsification *is* the discriminant evidence)

## Procedure
1. Load both `verdicts.json`; extract the two Spearman coefficients and their p-values.
2. Assemble the 2×2 MTMM matrix — monotrait-heteromethod cell = convergent (Presence × Trends); heterotrait cell = discriminant (Presence × BSR).
3. Compute **C3 = abs(ρ_convergent) − abs(ρ_discriminant)**.
4. Check the significance asymmetry: convergent **significant** AND discriminant **non-significant**.
5. Emit the `H_CV_Baseline` verdict per the SCORING rules in `v0_29_cv_baseline_content.py` → `osf/v29/v29_verdicts.json`.

## What does NOT happen
- No probe generation, no model calls, no new 24-brand registry, no Phase A / Phase B.
- The cloned `build_charts_v29.py` / `build_paper_v0_29.py` / `build_report_v29.py`
  carry v0.26 BSR wiring and chart references (`chart_26_*`, `v26_*`); these get
  surgically rewired at the chart/report/paper stages — **not** by re-measuring.

## Lock
Tagged `v0.29-prereg-r1` at the commit containing this file and
`v0_29_cv_baseline_content.py`. No measurement follows the tag; scoring runs
directly against the two inherited verdicts files above.
