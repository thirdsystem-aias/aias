# AIAS v0.37 — Cpc_Identity_Load_Moderator

OSF deposit for AIAS™ Presence Measurement Protocol, v0.37.

**Status:** Pre-registration LOCKED at git tag `v0.37-prereg-r1` (2f381f7); acquisition not yet run. Design: Identity-Load × CPC — φ DV (v1.8 mean-independent), IL-Direct moderator, trio n=72.

## Tree

- `data/` — Phase A and Phase B acquisition CSVs
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs (chart_01..04)
- `scripts/` — scoring code
- `registries/` — locked 24-brand registry

## Pipeline

1. Author pre-registration in `prereg/v0_37_cpc_identity_load_moderator_content.py`
2. Lock at git tag `v0.37-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v37.py`
4. Score: `python3 scripts/score_v37.py`
5. Build report: `python3 reports/build_report_v37.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_37.py`
7. Submit per `papers/v0_37/ssrn_submission_packet_v0_37.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v37 v37`
