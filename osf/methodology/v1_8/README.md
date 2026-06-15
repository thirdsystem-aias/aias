# AIAS v1.8 — Consistency Instrument

OSF deposit for AIAS™ Presence Measurement Protocol, v1.8.

**Status:** scaffolded by `aias_new_phase.py` on phase kickoff. Pre-registration not yet locked; acquisition not yet run.

## Tree

- `data/` — Phase A and Phase B acquisition CSVs
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs (chart_01..04)
- `scripts/` — scoring code
- `registries/` — locked 24-brand registry

## Pipeline

1. Author pre-registration in `prereg/v1_8_consistency_instrument_content.py`
2. Lock at git tag `v1.8-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v1_8.py`
4. Score: `python3 scripts/score_v1_8.py`
5. Build report: `python3 reports/build_report_v1_8.py`
6. Build SSRN paper: `python3 scripts/build_paper_v1_8.py`
7. Submit per `papers/v1_8/ssrn_submission_packet_v1_8.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v1_8 v1_8`
