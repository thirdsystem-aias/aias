# AIAS v0.37 — Identity-Load × CPC

OSF deposit for the AIAS™ Presence Measurement Protocol, phase v0.37.

**Status:** Scored and results-locked. A frozen re-analysis (no new model acquisition) of
the canonical two-channel trio — v0.20 skincare, v0.21 cosmetics, v0.22 automotive; 72
brand units, 53 analyzable after the pre-specified true-zero/saturation partition.
Pre-registration locked at git tag `v0.37-prereg-r2` (87ee3c2), amending r1 (2f381f7,
frozen); results locked at `v0.37-results-locked` (275b516).

**Primary result — H_IL_Consistency: FALSIFIED → CLEAN-NULL.** The pooled within-substrate
rank association between continuous Identity-Load (IL-Direct) and the mean-independent
consistency instrument φ is null: ρ = −0.008 (stratified-permutation p = 0.955; n = 53,
above the pre-registered power floor of 45), and remains null under a presence-controlled
partial (ρ = +0.004) — the verdict matrix's clean-null cell, not the suppression cell.
Read against IL-Direct's confirmed effect on Presence (Protocol v1.6, H_IdentityLoad_Direct),
this is a component dissociation: identity load moves *whether* a brand is surfaced by the
model panel, not *how consistently* it is surfaced across models.

## Tree

- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `v37_verdicts.json` — scored verdicts (single source of truth for every reported number)
- `v37_il_phi_analysis_set.csv` — the 53-unit analysis set
- `figures/` — paper confirmatory figure set: `chart_01_floor_not_ceiling`,
  `chart_02_precise_null`, `chart_03_dissociation`
- `reports/` — Third System™ brand-format report PDF (managerial register)
- `reports/figures/` — report-register figures (`report_fig_01..04`; managerial vocabulary;
  the cross-substrate figure, `report_fig_03`, is report-only and carries no inferential claim)
- `scripts/` — scorer (`score_v0_37.py`), dual-register chart builder (`build_charts_v37.py`),
  report builder (`build_report_v37.py`), and the report content module

**Input-integrity baseline (in repo, not in this deposit).** The IL-Direct moderator axis
is anchored by a SHA-256 baseline (`.v37_il_direct_baseline.sha256`) that the scorer checks
on every run (clause-3 halt-on-mismatch, so a re-run aborts if the source CSV drifts from the
locked input). Because it is a dotfile, it is not part of this OSF deposit; it lives in the
program git repository at the locked tag (`v0.37-prereg-r2`), where a reproducer can retrieve
it to confirm their input matches the locked source.

## Pipeline (frozen re-analysis — no new acquisition)

1. Pre-registration locked at `v0.37-prereg-r1`, amended to `v0.37-prereg-r2` (pre-acquisition
   verdict-matrix exhaustiveness completion of the FALSIFIED row; DEVIATIONS Entry 2 — no
   verdict scored at amendment)
2. Score the frozen trio inputs: `python3 scripts/score_v0_37.py`
3. Build figures (paper + report registers): `python3 scripts/build_charts_v37.py`
4. Build the brand-format report: `python3 reports/build_report_v37.py`

The SSRN academic paper for this phase is deposited separately upon submission.
