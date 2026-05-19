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

**Audit trail.** The original pre-registration (with the misaligned protocol references) is preserved in the repository at commit `c013ac1`, tag `v0.17-prereg`. The revised pre-registration is committed at `3ebe426`, tagged `v0.17-prereg-r1`. Both tags remain on `origin/v0.11-phase3-pilot`.

**Discipline invariant.** The pre-acquisition lock invariant is preserved: no v0.17 LLM acquisition has occurred between the original lock at c013ac1 and this revision at `3ebe426`. The corrected pre-registration sits ahead of any v0.17 data event in the operational sequence.

**Operator.** Pablo Ulpiano González Castro.
**Detection method.** Routine reconciliation of pre-registration against canonical classifier `scripts/classify_phase_a_v1_3.py` during Phase A pipeline setup.

---

## Entry 2 — Google API integration patch (2026-05-19)

**Event.** First-run live acquisition via `scripts/acquire_phase_a_v1_3.py --live` (commit `04b624f`) succeeded for 4 of 6 slots per brand (12 of 18 total calls across the 3 primary pivots Le Creuset, All-Clad, Vermicular). Anthropic slots (claude-opus-4-5, claude-sonnet-4-5) and OpenAI slots (gpt-4o, gpt-4o-mini) completed without error. Google slots failed across all three brands:

- Slot 5 (`gemini-1.5-pro`): `NotFound: 404 models/gemini-1.5-pro is not found for API version v1beta`
- Slot 6 (`gemini-1.5-flash`): `NotFound: 404 models/gemini-1.5-flash is not found for API version v1beta`

A `FutureWarning` from `google.generativeai` also surfaced indicating the legacy package was sunset on 2025-11-30; the supported successor is `google.genai`.

**Detection.** Live acquisition output surfaced both issues simultaneously. The `gemini-1.5-*` model identifiers used in the v0.17 acquire-script `SLOTS` list were sunset by Google between the v1.3 methodology paper draft window and v0.17 acquisition timestamp, and the legacy SDK no longer maps to current generation models.

**Resolution.** Patched `scripts/acquire_phase_a_v1_3.py`:

- Package: `google.generativeai` (sunset) → `google.genai` (currently-supported successor). Import line and `call_google` function rewritten against the new SDK's `genai.Client().models.generate_content(model=..., contents=...)` API.
- Slot 5 `model_id`: `gemini-1.5-pro` → `gemini-2.5-flash` (current production-GA).
- Slot 6 `model_id`: `gemini-1.5-flash` → `gemini-2.0-flash` (current production-GA).
- Other slots (claude-opus-4-5, claude-sonnet-4-5, gpt-4o, gpt-4o-mini) unchanged.
- Prerequisite added to docstring: `pip install --upgrade google-genai`.

**Methodological impact on v1.3 §6.4.2 C_P anchoring.** The reference-set composition has changed at the Google-tier slots. The 6-slot count is preserved, and the 3-provider × 2-tier balance is preserved structurally, but the Google tier is degraded: both updated Google slots are flash-tier rather than the original pro+flash pairing. This is a tooling-driven deviation, not a methodological design choice — the original `gemini-1.5-pro` slot is no longer accessible on the GOOGLE_API_KEY associated with this acquisition (404, not 403, indicating model-availability rather than authorisation). The C_P supermajority threshold (5/6) is unchanged. Methodological re-evaluation of the canonical reference-set definition deferred to v0.18 Methodology re-cut; v1.3 §5.2 will be revisited if cross-phase comparability suffers.

**Acquisition status post-patch.** Slot files 1-4 for all three primary pivots were successfully written to disk during the first acquisition pass (12 successful slot files). The script's skip-existing-file logic ensures the second pass will attempt only slots 5-6 for each brand — 6 additional API calls rather than re-running the full 18-call panel. Existing successful slot data is preserved unchanged.

**Discipline invariant.** This deviation occurred during Phase A acquisition, before any Phase B / Phase D operations. Pre-registration hypotheses §2.1, §2.2, §2.3 and panel composition §3.2 are unaffected. The deviation is documented contemporaneously per v1.3 §6.4.7.4 audit-log discipline.

**Audit trail.** Patched script will be committed at `12e66db` on `v0.11-phase3-pilot`. Original (failing) script preserved in git history at commit `3ebe426`.

---

## Entry 3 — Google slot 6 second patch (`gemini-2.0-flash` → `gemini-2.5-flash-lite`) (2026-05-19)

**Event.** Second-pass acquisition (script commit `12e66db`) succeeded on slot 5 (`gemini-2.5-flash`) for all three primary pivots Le Creuset, All-Clad, Vermicular (3/3 calls). Slot 6 (`gemini-2.0-flash`) failed for all three brands with `ClientError: 404 NOT_FOUND` and the error message: *"This model models/gemini-2.0-flash is no longer available to new users. Please update your code to use a newer model for the latest features and improvements."* Google is restricting `gemini-2.0-flash` access to existing-account users; the `GOOGLE_API_KEY` associated with this acquisition is treated as a new-user account and cannot reach the model.

Distinct failure mode from Entry 2: the prior failure was a sunset model identifier (no model at that path); this failure is an access-restriction on a still-existent model identifier. Both yield the same surface error code (404) but reflect different deprecation mechanics.

**Detection.** Three sequential slot 6 attempts surfaced identical error wording. The fix path is explicitly stated in Google's error message: migrate to a newer model.

**Resolution.** Patched `scripts/acquire_phase_a_v1_3.py` SLOTS row 6:

- `model_id`: `gemini-2.0-flash` → `gemini-2.5-flash-lite`

`gemini-2.5-flash-lite` is the current production-GA efficiency variant in the same model family as slot 5's `gemini-2.5-flash`. Same generation, lighter tier — closest natural successor in the flash branch.

**Cumulative Google-tier degradation since original reference-set definition:**

| Slot | Original (v1.3 design) | Entry 2 patch | Entry 3 patch |
|---|---|---|---|
| 5 | `gemini-1.5-pro` (high) | `gemini-2.5-flash` (mid) | `gemini-2.5-flash` (mid) |
| 6 | `gemini-1.5-flash` (mid) | `gemini-2.0-flash` (mid) | `gemini-2.5-flash-lite` (efficient) |

The 6-slot count is preserved. Provider diversity (Anthropic, OpenAI, Google) is preserved. The 3-provider × 2-tier balance is broken at the Google tier: Anthropic retains Opus+Sonnet (high+mid); OpenAI retains GPT-4o + GPT-4o-mini (high+mid); Google is now `gemini-2.5-flash` + `gemini-2.5-flash-lite` (mid+efficient, both flash-family). The C_P supermajority threshold (5/6) is unchanged in count but the underlying reference-set composition is structurally different from the v1.3 design intent.

**Methodological note for cross-phase comparability.** If the v0.17 C_P verdicts surface tier-correlated anchoring patterns — i.e., flash-family Gemini systematically anchors differently than would have a pro-family Gemini — this becomes a methodological signal worth surfacing in the v1.4 Methodology re-cut. The v0.16 retrospective scoring used a different (and now-unreachable) reference set; cross-phase C_P comparison should be interpreted with this composition shift documented in the published v0.17 paper.

**Acquisition status post-patch.** Slot files 1-5 for all three primary pivots are now on disk (15 successful slot files). The script's skip-existing logic ensures the third acquisition pass will attempt only slot 6 across the three brands — 3 additional API calls.

**Discipline invariant.** Deviation occurred during Phase A acquisition, before any Phase B / Phase D operations. Pre-registration hypotheses §2.1, §2.2, §2.3 and panel composition §3.2 are unaffected.

**Audit trail.** Patched script will be committed at `b5efea3`. Prior failing version preserved at git commit `12e66db` (Entry 2 patch).

---

## Entry 4 — Automation of Phase A C_P classification: v1.3 operator-judgement → provisional v1.4 LLM classifier (2026-05-19)

**Event.** The v1.3 §6.4.2 Phase A C_P scoring rule specifies operator-judgement classification: the operator reads each row's `first_100_tokens` and assigns `anchored` ∈ {0, 1}. For v0.17 acquisition this would require 18 operator judgement calls (3 brands × 6 slots), scaling linearly with panel size and cascade depth in subsequent phases. Cross-phase scalability for the AIAS 1.0 programme requires removing operator-judgement from the Phase A loop.

**Resolution.** Phase A C_P classification is automated via `scripts/classify_phase_a_auto_v1_4.py`. The script substitutes the v1.3 §6.4.2 operator step with a locked LLM classifier.

**Locked classifier configuration:**

| Parameter | Value |
|---|---|
| Model | `claude-opus-4-7` |
| Temperature | `0` |
| Max output tokens | `200` |
| Prompt template | `CLASSIFIER_PROMPT_TEMPLATE` in `scripts/classify_phase_a_auto_v1_4.py` |
| Output schema | `ANCHORED: <0\|1>\nRATIONALE: <≤25-word sentence>` |

The classifier model, prompt, temperature, and output schema are the methodologically-locked elements. Any change to any of them in subsequent phases constitutes a further DEVIATIONS entry.

**Departure from v1.3 §6.4.2 — explicit record.** v1.3 §6.4.2 as published reads (operationally): "Operator judgement is the canonical classifier per v1.3 §6.4.2 — no automated classification is specified." This Entry supersedes that step for v0.17 acquisition and all subsequent phases pending the v1.4 Methodology paper. The v1.4 paper (successor increment to SSRN 6797679) will formalise the automated-classifier rule as canonical Phase A protocol and retire the operator-judgement specification.

**Methodological rationale.**

1. **Cross-phase scalability.** Manual N-row classification is the binding constraint on per-phase throughput. v0.17 = 18 rows; v0.18 panel + cascade = 30–50 rows; v0.19+ similarly. Automation removes the linear cost.
2. **Reproducibility.** Operator judgement is non-deterministic across sessions and across operators. A locked classifier (model + prompt + temperature) produces stable calls modulo upstream model changes — and upstream model changes are themselves documented as DEVIATIONS.
3. **Audit-trail richness.** Each row's `anchoring_note` records the classifier's per-row one-sentence rationale, producing a structured audit trail superior to typical operator notes.
4. **Cross-rater check capability.** The locked-prompt design enables future inter-rater reliability checks against alternative classifier models (e.g., gpt-4o, gemini-2.5-flash) as a robustness extension in v1.4 or v1.5.

**Pre-reg §6.1 step 4 — supersession.** Pre-registration v0.17 r1 (commit `3ebe426`, tag `v0.17-prereg-r1`) §6.1 step 4 reads: *"Operator judgement is the canonical classifier per v1.3 §6.4.2 — no automated classification is specified."* This DEVIATIONS Entry 4 supersedes that step. Substantive hypotheses §2.1, §2.2, §2.3 and panel composition §3.2 remain unchanged. The C_P supermajority threshold (5/6) and CONFIRMED/PARTIAL/FALSIFIED verdict structure are unchanged. The v0.17 paper's Methods section will reference DEVIATIONS Entry 4 alongside the canonical methodology citations (SSRN 6761698, SSRN 6797679, plus the forthcoming v1.4 paper).

**Forward action for v1.4 Methodology paper:**

1. Promote the automated classifier from "provisional" to canonical Phase A specification.
2. Lock the classifier model + prompt + temperature as published-protocol artefacts.
3. Run a v0.16 retrospective re-classification through the automated classifier to confirm continuity with the v1.3 Victorinox/Wüsthof worked example; report any divergence.
4. Specify inter-rater reliability check option (second classifier model for robustness).
5. Specify confidence-threshold / operator-override interface for genuine boundary cases the classifier flags as uncertain (deferred; not implemented at v0.17).

**Reproducibility note.** Anthropic temperature=0 inference is low-variance but not strictly bit-deterministic at infrastructure level. Re-running the classifier against the same slot files should produce identical `anchored` values on stable classification cases; genuinely borderline rows may flip on rare occasions. Methodological assessment of re-run variance is a v1.4 follow-up.

**Audit trail.** Script committed at `<HASH_AUTO_4>`. Filled ledger (after running the classifier) committed in same commit. Empty-ledger snapshot preserved at commit `2b31253` for re-derivation under any future protocol revision.
