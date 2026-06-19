# AIAS™ v0.37 — Mega-Prompt: NOT APPLICABLE (No-Acquisition Re-Analysis)

**Phase:** v0.37 — Identity-Load (IL-Direct) × CPC
**Lock tag:** v0.37-prereg-r1

This phase issues **no LLM acquisition calls**. It is a re-analysis (v0.33
pattern) of frozen per-brand t₁ quantities:

- Per-brand φ (v1.8 mean-independent consistency instrument; the DV)
- Per-brand IL-Direct δ = R_cult − R_cat (the moderator; `R_cult_total −
  R_cat_total` from `osf/methodology/v1_7/data/v1_7_cpc.csv`)
- Per-brand C_P (v1.6) + recall-mean (controls; SECONDARY robustness only)
- CV-CPC (v1.7) retained as comparator only, never as DV

Substrate scope: **v0.20 / v0.21 / v0.22 — 72 brand units (24×3), the canonical
two-channel trio** = intersection of φ-availability (all five) and continuous
IL-Direct availability (trio only). v0.19 excluded (single-channel, out of
construct); v0.23 = walled runtime-verify extension. TERTIARY test-retest check
additionally consumes the v0.34 t₂ wave only where it intersects the trio.

No prompts are defined for this phase. The cloned v0.34 acquisition
mega-prompt content was removed at scaffold trim (DEVIATIONS Entry 1).

Design, metric, moderator, hypotheses, decision rules, verdict matrix,
guardrails: see
`prereg/v0_37_cpc_identity_load_moderator_content.py` (the locked artifact).
