# AIAS v0.32 — Cpc Version Stability

OSF deposit for AIAS™ Presence Measurement Protocol, v0.32.

**Status:** scaffolded by `aias_new_phase.py` on phase kickoff. Pre-registration not yet locked; acquisition not yet run.

## Tree

- `data/` — Phase A and Phase B acquisition CSVs
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs (chart_01..04)
- `scripts/` — scoring code
- `registries/` — locked 24-brand registry

## Pipeline

1. Author pre-registration in `prereg/v0_32_cpc_version_stability_content.py`
2. Lock at git tag `v0.32-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v32.py`
4. Score: `python3 scripts/score_v32.py`
5. Build report: `python3 reports/build_report_v32.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_32.py`
7. Submit per `papers/v0_32/ssrn_submission_packet_v0_32.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v32 v32`
