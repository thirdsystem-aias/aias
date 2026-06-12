# AIAS™ v0.36 — Mega-Prompt: NOT APPLICABLE (No-Acquisition Re-Analysis)

**Phase:** v0.36 — CPC Regime Emergence
**Lock tag:** v0.36-prereg-r2 (supersedes r1; r1 remains the deposited record)

This phase issues **no LLM acquisition calls**. It is a fully retrospective
re-analysis (v0.33 / v0.35 pattern) of frozen quantities:

- Per-brand 6-dim per-model CPC vector (CV-CPC = 1/(1+CV), v1.7 computation;
  characterization quantity, not adopted), z-scored within substrate per model —
  from `osf/v33/data/v33_eta2.csv` (all 112 units, v0.19–v0.23).
- Per-brand v0.23 Presence-quartile **regime** label (Dominant/Established/
  Emerging/Absent) and **composite_presence** — read as frozen fields from
  `osf/v23/v23_verdicts.json` `brand_details[]` (v0.23 only, 24 units).

**Construct-identity note (r2):** "regime" is overloaded in this program. The
v0.36 operative target is the v0.23 **per-brand Presence-quartile** regime —
**not** the Protocol v1.2 substrate-level AI-Presence×Google-Trends Four-Regime
Taxonomy (SSRN 6761698), which is not per-brand, not in the CPC frozen data, and
unassigned for the CPC substrates. See `REGIME_DISAMBIGUATION` and DEVIATIONS
Entry 0 in the content module.

No prompts are defined for this phase. There is **no brand registry** this
phase; the analysis sets are enumerated in the locked content module.

Design, feature space, clustering procedure, hypotheses, criteria (with
per-hypothesis scope), verdict matrix, predictions, guardrails: see
`prereg/v0_36_cpc_regime_emergence_content.py` (the locked artifact).
