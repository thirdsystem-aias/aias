# AIAS v0.34 — CPC Longitudinal t₁→t₂ Stability

OSF deposit for AIAS™ Presence Measurement Protocol, v0.34.

**Phase type — prospective longitudinal (full re-acquisition at t₂).** Re-acquires Phase A
(Recognition) + Phase B (two-channel six-frame Recall) for the five panel-uniform omnibus
substrates first acquired at t₁ (v0.19–v0.23; 112 brand units), using each substrate's t₁
runner verbatim (re-pointed to `data/`), to test temporal stability of CV-CPC and C_P. CV-CPC
is walled per v1.7 (Presence-coupled, |ρ|=0.77; *not adopted*); the phase measures its
temporal stability, not its validity. t₁ lineage routes through the substrate phases and
v1.7; **v0.31 (SSRN 6880959) is deliberately uncited** (by design).

**Status:** scaffolded; pre-registration not yet locked; acquisition not yet run.

## Recompute parity (scoped — do not conflate)

- **v0.20/0.21/0.22:** recomputed t₁ per-model recall must reproduce
  `osf/methodology/v1_7/data/v1_7_cpc.csv` `r_per_model` **bit-for-bit** (citeable external
  anchor; `score_v33` gates 72/72). Mismatch → computational-reproducibility note, halt.
- **v0.19/0.23:** the v1.7 anchor does **not** cover these. Parity = bit-for-bit reproduction
  of the frozen per-model t₁ inputs as consumed by the v0.31→v0.33 arc (`counts_v19`/
  `counts_v23` outputs). Correctness rests on extraction-function provenance alone — stated,
  not overclaimed.

**v0.23 normalization footnote.** v0.23 recognition is scored as `r_level`; it is normalized
to binary (R0→0, else→1) for C_P, identically in both waves.

## Tree

- `data/` — Phase A and Phase B re-acquisition outputs (t₂), both waves' recomputed metrics
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt + `acquisition_manifest_v34.md`)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs
- `scripts/` — scoring code
- `registries/` — the five t₁ locked registries (bit-identical), referenced not re-locked

## Pipeline

1. Author pre-registration in `prereg/v0_34_longitudinal_t1_t2_omnibus_content.py`
2. Lock at git tag `v0.34-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v34.py`
4. Score: `python3 scripts/score_v34.py`
5. Build report: `python3 reports/build_report_v34.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_34.py`
7. Submit per `papers/v0_34/ssrn_submission_packet_v0_34.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v34 v34`
