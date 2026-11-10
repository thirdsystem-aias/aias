# AIAS v1.10 — Ranking, Paper A (instrument, cross-category baseline, separability gate)

Methodology lock and re-analysis of archived answers. No new data collection, no model calls. Status: pre-registration **DRAFT r1** (2026-11-10), **not locked**.

- `prereg/PRE_REGISTRATION_v1_10.md`: the draft (inputs, extraction rules, candidates, selection rule, hypotheses H1–H6, gate, checks, open questions).
- `prereg/feasibility_v1_10.md`: declared parsing feasibility on the development sample (v0.17 and v0.18 phase B; excluded from every confirmatory analysis).
- `scoping/feasibility_v1_10.py` and `.json`: the script behind the note, and its output.
- `registries/INPUTS_MANIFEST_v1_10.json` (built by `build_inputs_manifest_v1_10.py`): 88 frozen files, each with its git blob and SHA-256.
- `anchor/DEVIATIONS.md`: Entry 0 (ex ante).
- Scorer: `scripts/score_v1_10.py` (skeleton; the loaders are TODO). Tests: `scripts/test_score_v1_10.py` (synthetic data only).

Lock sequence: settle the open questions (§15) → content lock → commit → tag `v1.10-prereg-r1` → OSF deposit → verify both anchors → Stage S → Stage C.
