# AIAS v0.40 — US airlines and retail banks

OSF deposit for AIAS™ Presence Measurement Protocol, v0.40.

**Status:** scaffolded by `aias_new_phase.py` on phase kickoff. Pre-registration not yet locked; acquisition not yet run.

## Tree

- `data/` — acquisition outputs; `data/raw/` holds the public BTS and FDIC files the registry is built from (not in git)
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs (chart_01..04)
- `scripts/` — registry builder (`build_registry_v0_40.py`), then acquisition and scoring code
- `registries/` — brand registry: hand-sourced inputs, builder outputs (`out/`) and raw-data checksums; frozen at the lock

## Pipeline

1. Author pre-registration in `prereg/v0_40_us_airlines_and_retail_banks_content.py`
2. Lock at git tag `v0.40-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v40.py`
4. Score: `python3 scripts/score_v40.py`
5. Build report: `python3 reports/build_report_v40.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_40.py`
7. Submit per `papers/v0_40/ssrn_submission_packet_v0_40.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v40 v40`
