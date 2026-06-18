# AIAS™ Measurement Program — Methodology Phase v1.8
## CPC Consistency Instrument Redesign

**Status.** Pre-registration locked (`v1.8-prereg-r4`); results locked (`v1.8-results-r1`, commit `85d2202`); working paper public as SSRN 6963359.

### What this phase did

v1.8 redesigns Cross-model Presence Consistency (CPC) — the Consistency component of the AI Availability Score (AIAS™) — on a mean-independent basis. The prior coefficient-of-variation operationalization (CV-CPC) was falsified as a consistency instrument because the coefficient of variation of a low-rate count couples mechanically to its mean. v1.8 replaces it with φ, the between-model quasi-binomial dispersion (a Pearson χ²/df statistic), which divides out the binomial-expected variance and so removes the level coupling by construction rather than by post-hoc correction.

**No new data were acquired.** The phase re-scores a *frozen* five-substrate, six-model omnibus (112 brand-units; substrates v0.19–v0.23) under three pre-registered validation framings, so the test isolates the instrument from the data-generating process. The instrument definitions, framings, hypotheses, thresholds, and verdict matrix were locked at a version-controlled commit and externally anchored before any score was computed.

### Headline verdicts (sealed at `v1.8-results-r1`)

- **H_MeanIndependent — CONFIRMED.** Pooled |ρ(φ, μ)| = 0.091, against CV-CPC's 0.682 on the same base — roughly a seventh of the coupling the CV reproduces.
- **H_CV_Reproduces — CONFIRMED.** The CV mean-coupling recurs (|ρ| = 0.682), confirming the base carries the coupling φ must dissociate from.
- **H_LowRecallDefined — CONFIRMED.** φ extends defined coverage to 29 low-recall brands the floor-bearing CV cannot reach; 84 of 112 units are φ-defined, 28 are true-zeros, 0 sit at the saturation ceiling.
- **H_PositionalDissociation — CONFIRMED.** φ and the positional diagnostic J capture distinct facets (ρ(φ, J) = −0.403; 9 discordant units).
- Two-wave reproducibility ρ(φ_t1, φ_t2) = 0.645 (n = 83). Phantom-signature contrast: NULL. R_grad (graded recognition): carried as a forward specification — the frozen recognition channel is binary by probe design.

### Contents of this namespace

- Pre-registration — instrument definitions, framings, hypotheses, thresholds, verdict matrix
- Verdicts and instrument table — sealed scoring outputs
- Materialization manifest — pinned source records; the frozen omnibus is reproducible from it
- `scoring/score_v1_8.py` — canonical scorer
- `v1_8_ssrn_paper.pdf` — working paper (= SSRN 6963359)
- `v1_8_post_results_deviations.md` — post-results deviations log

### Reproducibility

The frozen omnibus is reproducible from the manifest's pinned records; no probes were re-issued in this phase.

---
AIAS™ Measurement Program · Third System™ · OSF project ec6wh (osf.io/ec6wh)
