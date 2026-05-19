# v0.17 DEVIATIONS Log

Operational deviations from `PRE_REGISTRATION_v0_17.md` (locked at commit c013ac1, tagged `v0.17-prereg`). Entries are written contemporaneously per Protocol v1.3 §6.4.7.4 at the time of the event, not retrospectively at publication.

---

## Entry 1 — Pre-registration revision (2026-05-19)

**Event.** The pre-registration locked at commit `c013ac1` and tagged `v0.17-prereg` contained §3.3 (Stage 4 adjacency keywords: `cookware` × `kitchen design`) and §6.1 (five-stage Phase A protocol with Trends-based numeric thresholds: `cv_pct ≤ 30.0`, `pivot_to_ref_ratio ∈ [0.5, 5.0]`, `substrate_proportion ≥ 0.2`, `adjacent_proportion ≤ 0.7`) that do not correspond to Protocol v1.3 (SSRN 6797679) as published. v1.3 §6.4.2 specifies the substrate-anchoring rule (C_P): each pivot candidate is queried at 6 LLM model slots per Protocol v1.2 §5.2 canonical reference set with a single canonical disambiguation query; each response is truncated to the first 100 whitespace tokens; operator classifies each as substrate-anchored (1) or not (0); per-brand `C_P PASSED` if anchoring count ≥ 5/6, `C_P FAILED` if ≤ 4/6. No Trends-based numeric stages are specified in v1.3.

**Detection.** During Phase A pipeline setup, inspection of the canonical v1.3 classifier `scripts/classify_phase_a_v1_3.py` confirmed that only the §6.4.2 anchoring rule is operationally implemented. The script's docstring ("Score §6.4.4 worked example against §6.4.2 anchoring rule"), constants (`TOKEN_LIMIT = 100`, `PASS_THRESHOLD = 5`, `TARGET_SLOTS = 6`), and error-message language ("Scenario A assumed v0.16 archived canonical disambiguation responses") all confirm the protocol as anchoring-based, LLM-acquisition-driven, and operator-judgement-mediated. The Trends-based numeric stages described in the v0.17 pre-registration as locked at c013ac1 do not appear in v1.3 §6.4 and were carried into the pre-reg from a prior framing that did not survive reconciliation with the published protocol.

**Resolution.** Revised pre-registration written to `registries/PRE_REGISTRATION_v0_17.md`:

- **§3.3 removed.** The original §3.3 (Stage 4 adjacency keywords) had no operational role under v1.3 §6.4.2. Subsequent §3 subsections renumbered: original §3.4 → §3.3 (drop risk), original §3.5 → §3.4 (registry artefact). The `stage_4_keywords` field in `registries/brands_kitchenware_v0.17.json` is retained as a vestige of the original lock but flagged informational-only in the revised §3.4; it has no operational role.
- **§6.1 rewritten.** Original §6.1 (Phase A pivot validation per v1.3 §6.4) specified five stages with Trends-based numeric thresholds. Revised §6.1 specifies the §6.4.2 C_P anchoring rule: 6-slot LLM acquisition, 100-token truncation, operator classification, supermajority 5/6 threshold. Acquisition implemented in new `scripts/acquire_phase_a_v1_3.py`; classification via existing `scripts/classify_phase_a_v1_3.py`.
- **§6.2 trigger condition updated.** Original §6.2 fallback activation was triggered on "Stage 5 FAIL"; revised §6.2 triggers on "C_P FAILED". Cascade structure (alternate activation → bounded override → cell collapse) and §6.4.7 references are unchanged.
- **§7 deliverables.** Added `scripts/acquire_phase_a_v1_3.py` and `scripts/classify_phase_a_v1_3.py` as explicit Phase A artefacts.
- **§8 sign-off.** Added "Revision r1 declaration" subsection documenting the relationship to the original c013ac1 lock and the preservation of the pre-acquisition invariant.

**Substantive impact on hypotheses.** None. §2.1 (`H_Regime4_kitchenware` C1/C2/C3 decision rules), §2.2 (`H_IdentityLoad_moderator` joint verdict matrix), and §2.3 (descriptive sensitivities) are unchanged. The panel composition in §3.2 (16 brands across European/American/Japanese cells with ordinal pivot priority) is unchanged.

**Audit trail.** The original pre-registration (with the misaligned protocol references) is preserved in the repository at commit `c013ac1`, tag `v0.17-prereg`. The revised pre-registration is committed at `<HASH_R1>`, tagged `v0.17-prereg-r1`. Both tags remain on `origin/v0.11-phase3-pilot`.

**Discipline invariant.** The pre-acquisition lock invariant is preserved: no v0.17 LLM acquisition has occurred between the original lock at c013ac1 and this revision at `<HASH_R1>`. The corrected pre-registration sits ahead of any v0.17 data event in the operational sequence.

**Operator.** Pablo Ulpiano González Castro.
**Detection method.** Routine reconciliation of pre-registration against canonical classifier `scripts/classify_phase_a_v1_3.py` during Phase A pipeline setup.
