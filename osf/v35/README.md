# AIAS v0.35 — Phantom-Cpc Omnibus

OSF deposit for AIAS™ Presence Measurement Protocol, v0.35.

**Status:** scaffolded by `aias_new_phase.py` on phase kickoff. Pre-registration not yet locked; acquisition not yet run.

## Tree

- `data/` — Phase A and Phase B acquisition CSVs
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs (chart_01..04)
- `scripts/` — scoring code
- `registries/` — locked 24-brand registry

## Pipeline

1. Author pre-registration in `prereg/v0_35_phantom_cpc_omnibus_content.py`
2. Lock at git tag `v0.35-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v35.py`
4. Score: `python3 scripts/score_v35.py`
5. Build report: `python3 reports/build_report_v35.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_35.py`
7. Submit per `papers/v0_35/ssrn_submission_packet_v0_35.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v35 v35`
