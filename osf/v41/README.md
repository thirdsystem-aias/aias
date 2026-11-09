# AIAS v0.41 — Longitudinal T3 Omnibus

OSF deposit for AIAS™ Presence Measurement Protocol, v0.41.

**Status:** scaffolded by `aias_new_phase.py` on phase kickoff. Pre-registration not yet locked; acquisition not yet run.

## Tree

- `data/` — Phase A and Phase B acquisition CSVs
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs (chart_01..04)
- `scripts/` — scoring code
- `registries/` — locked 24-brand registry

## Pipeline

1. Author pre-registration in `prereg/v0_41_longitudinal_t3_omnibus_content.py`
2. Lock at git tag `v0.41-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v41.py`
4. Score: `python3 scripts/score_v41.py`
5. Build report: `python3 reports/build_report_v41.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_41.py`
7. Submit per `papers/v0_41/ssrn_submission_packet_v0_41.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v41 v41`
