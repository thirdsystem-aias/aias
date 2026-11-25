# SYNTHETIC TEST DATA — NOT RESULTS

Everything under this folder is invented: brand names (B01, B02, ...), scores and statistics come from the locked
scorer's own synthetic test fixture (`Synth` in `osf/aias_6_0_preview/scripts/tests/test_score_aias_6_0_preview.py`),
run with `require_lock=False` and reduced draws. Nothing here is a measurement, and nothing here is deposited,
published or copied to the website.

| Folder | What it exercises |
|---|---|
| `SYNTHETIC_nov25_inputs/` | The component states as they stood on Nov 25, 2026: Ranking MARGINAL (v1.14 Stage 1), Grounding MARGINAL (v1.13 gate), Sentiment NOT RUN (no S_t4), Coverage PASS (v1.12 gate). K = Presence, Consistency, Coverage; class A_k. Used by the report pipeline (`scripts/build_charts_aias6_report.py`, `reports/build_report_aias6_preview.py`) and its tests. |

Regenerate (about 10 s):

```
PYTHONDONTWRITEBYTECODE=1 python3 papers/aias_6_0_preview/tests/make_scenarios_aias6.py papers/aias_6_0_preview/synthetic SYNTHETIC_nov25_inputs
```

Every JSON output carries `synthetic_fixture`; the builders refuse these files in real mode, require the
"SYNTHETIC TEST — NOT RESULTS" watermark, prefix every file name with `SYNTHETIC_` and write only outside the
repository.
