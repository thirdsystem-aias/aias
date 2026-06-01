# AIAS v0.28 — Tech (Brand Discriminant) — CV.04

OSF deposit for AIAS™ Presence Measurement Protocol, v0.28 (CV.04 discriminant
construct validity: AIAS Presence vs BRAND familiarity & d′, Tech stratified-24).

**Status:** Pre-registration LOCKED at git tag `v0.28-prereg-r1` (commit 563222b).
Acquisition not yet run (`data/` empty by design).

## Pre-deposit drift check (reproducible)

`grep -riE 'bsr|amazon|H_PV_|120 brands|5.?x.?24|yougov|mental availability'` plus
word-boundary `\bCEP\b` over `osf/v28/` returns hits ONLY in three allow-listed,
legitimate buckets — no wrong-study (v0.26 BSR) contamination:

- **(a)** `scripts/score_v28.py` lock-guard docstring — names the drift tokens it
  detects and rejects, by design.
- **(b)** `prereg/…content.py` DEVIATIONS Entry 1 — required to document the
  pre-acquisition scope amendment (CV.04 reframed away from YouGov/CEP Mental
  Availability).
- **(c)** the v0.26 MTMM companion citation ("v0.26 (CV.02) Amazon BSR
  discriminant") in the content module's CV-chain list and `PAIRS_WITH` map.
- **(d)** this drift-check record itself — the block quotes the search pattern and
  enumerates buckets (a)–(d), so its own lines necessarily contain the tokens.

Verified: every hit maps to (a), (b), (c), or (d); none is wrong-study content.

## Tree

- `data/` — Phase A and Phase B acquisition CSVs
- `prereg/` — locked pre-registration artifacts (content module + mega-prompt)
- `reports/` — brand-format report PDF
- `figures/` — chart PDFs (chart_01..04)
- `scripts/` — scoring code
- `registries/` — locked 24-brand registry

## Pipeline

1. Author pre-registration in `prereg/v0_28_tech_brand_discriminant_content.py`
2. Lock at git tag `v0.28-prereg-r1`
3. Run acquisition: `python3 scripts/run_acquisition_v28.py`
4. Score: `python3 scripts/score_v28.py`
5. Build report: `python3 reports/build_report_v28.py`
6. Build SSRN paper: `python3 scripts/build_paper_v0_28.py`
7. Submit per `papers/v0_28/ssrn_submission_packet_v0_28.md`
8. Final OSF deposit: `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v28 v28`
