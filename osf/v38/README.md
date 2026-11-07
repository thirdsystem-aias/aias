# AIAS™ v0.38 — Home Coffee Roasters (Aillio-focal)

Phase of the AIAS™ Measurement Program (Third System™). Focal-brand designed-for-test inside a
full category registry: does an AI recommendation slot attach to a superseded product generation
(Aillio Bullet R1 → R2/R2 Pro, July 2024) of a living brand?

## Layout
- `prereg/` — PRE_REGISTRATION_v0_38.md, probes_v0_38.json, LOCK_MANIFEST_v0_38.sha256 (locked at tag `v0.38-prereg-r1` before acquisition)
- `registries/` — brands_home_roasters_v0.38.json (32 brands, alias patterns, Aillio generation coding, Grounding fact sheet)
- `scripts/` — copies of acquire_v0_38.py, score_v0_38.py, test_score_v0_38.py at the state used
- `data/` — v38_raw.json (acquisition), v38_coded.csv, v38_mentions.csv, v38_tables.json (scoring)
- `v38_verdicts.json` — confirmatory verdicts and manipulation check
- `figures/`, `reports/` — charts and the brand-format report
- `DEVIATIONS.md` — contemporaneous deviations log

## Reproduce
```
python3 scripts/test_score_v0_38.py     # synthetic fixtures
python3 scripts/acquire_v0_38.py        # needs ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY
python3 scripts/score_v0_38.py
```
