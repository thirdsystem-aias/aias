# AIAS™ v0.39 — Commercial Coffee Roasters (Bellwether-focal)

Phase of the AIAS™ Measurement Program (Third System™). Focal-brand designed-for-test inside a full category registry,
with a two-arm panel (the fixed 2024–25 six-model panel; three current assistants asked with and without their
providers' web search): what does AI retrieval do to a brand whose proposition is that a category barrier — external
venting, ductwork and a gas line — no longer applies?

## Layout
- `prereg/` — PRE_REGISTRATION_v0_39.md, probes_v0_39.json, feasibility_v0_39.json, LOCK_MANIFEST_v0_39.sha256 (locked at tag `v0.39-prereg-r1` before acquisition)
- `registries/` — brands_commercial_roasters_v0.39.json (36 brands, alias patterns, Bellwether generation coding, frame lexicons, grounding fact sheet)
- `scripts/` — acquire_v0_39.py, score_v0_39.py, test_score_v0_39.py, build_registry_v0_39.py, check_registry_v0_39.py (locked); audit_worklist_v0_39.py and verify_v0_39.py (analysis aids written after acquisition; neither changes the coding)
- `data/` — v39_raw.json (acquisition, with search traces), v39_coded.csv, v39_mentions.csv, v39_tables.json (scoring), v39_audit_commonnoun.json (section 3.3 audit, binding), v39_coder_audit.json (section 5.7 audit)
- `v39_verdicts.json` — confirmatory verdicts and manipulation checks (status FINAL)
- `figures/`, `reports/` — charts and the brand-format report
- `DEVIATIONS.md` — contemporaneous deviations log

## Reproduce
```
python3 scripts/test_score_v0_39.py     # synthetic fixtures; no study data
python3 scripts/acquire_v0_39.py        # needs ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY
python3 scripts/score_v0_39.py          # reads data/v39_raw.json and data/v39_audit_commonnoun.json
python3 scripts/verify_v0_39.py         # independent re-computation of every verdict input
```
The scripts resolve paths from `AIAS_ROOT` (default `/Users/pablou/aias`); point it at a checkout of
github.com/thirdsystem-aias/aias with this folder at `osf/v39/`.
