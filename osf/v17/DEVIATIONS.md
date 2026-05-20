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

**Audit trail.** Script committed at `2097c9f`. Filled ledger (after running the classifier) committed in same commit. Empty-ledger snapshot preserved at commit `2b31253` for re-derivation under any future protocol revision.

---

## Entry 5 — Classifier API change: `temperature` deprecated on `claude-opus-4-7` (2026-05-19)

**Event.** First live invocation of `scripts/classify_phase_a_auto_v1_4.py` (committed at `2097c9f` per Entry 4) failed on the first API call with `BadRequestError: 400 — temperature is deprecated for this model`. Anthropic deprecated the `temperature`, `top_p`, and `top_k` sampling parameters on `claude-opus-4-7` entirely (Anthropic API change April 2026); passing any value, including `0`, triggers a 400 invalid_request_error per Anthropic / AWS Bedrock model documentation.

**Detection.** Single LLM call attempt at the top of the 18-row classification queue surfaced the 400. The dry-run preceding it did not catch the issue because dry-run does not exercise the API path.

**Resolution.** Patched `scripts/classify_phase_a_auto_v1_4.py`:

- Removed the `temperature=CLASSIFIER_TEMPERATURE` keyword argument from the `client.messages.create(...)` call.
- Removed the `CLASSIFIER_TEMPERATURE = 0` constant.
- Updated the `anchoring_note` tag from `[auto-classified by claude-opus-4-7 @ T=0]` to `[auto-classified by claude-opus-4-7]` to reflect that sampling temperature is no longer operator-controlled.
- Updated docstring and startup banner to note that temperature is model-default (deprecated for this model) and that reproducibility commitments now rest on `(classifier model + prompt template)` constancy only.

**Methodological framing.**

Entry 4 specified `temperature = 0` as a methodological lock on classifier reproducibility. That lock is no longer enforceable for `claude-opus-4-7` via the API. Anthropic's documentation explicitly states that `temperature = 0` did not guarantee identical responses across invocations in any case — so the change is partly an honest API surface that matches the underlying non-determinism rather than an actual loss of guarantee. The reproducibility commitment for the AIAS Phase A automated classifier now reads:

> Phase A C_P classification is reproducible at the *(classifier model identifier, prompt template)* level. Two invocations of `classify_phase_a_auto_v1_4.py` against the same ledger with the same classifier model and same prompt template should produce identical anchoring calls on stable classification cases. Genuinely borderline rows may flip on rare re-runs; methodological inter-run variance is a v1.4 follow-up assessment.

This is the framing that will go into the v1.4 Methodology paper. Entry 4's "temperature = 0 / low-variance / deterministic" language is superseded by Entry 5.

**Locked classifier configuration (current state):**

| Parameter | Value | Notes |
|---|---|---|
| Model | `claude-opus-4-7` | Locked |
| Sampling | model-default | Not configurable — temperature/top_p/top_k deprecated for this model |
| Max output tokens | `200` | Locked |
| Prompt template | `CLASSIFIER_PROMPT_TEMPLATE` in script | Locked |
| Output schema | `ANCHORED: <0\|1>\nRATIONALE: <≤25-word sentence>` | Locked |

**Impact on pre-registration and substantive hypotheses.** None on the substance. §2.1, §2.2, §2.3, §3.2 are unchanged. Entry 5 supersedes the `temperature = 0` line of Entry 4 only; the substitution of LLM classifier for operator judgement (the substantive Entry 4 deviation) stands.

**Forward action for v1.4 Methodology paper.** Add inter-run reproducibility assessment to the v1.4 paper's §6.4.2 specification: re-run the v0.17 classifier against the same 18-row ledger on a separate occasion and report any anchoring disagreements as the empirical floor of classifier non-determinism. This becomes the canonical robustness check rather than a sampling-parameter lock.

**Audit trail.** Patched script committed at `9042dea`. Failing-version script preserved at commit `2097c9f`.

---

## Entry 6 — Vermicular C_P FAILED → Japanese cell cascade activated (Iwachu) (2026-05-19)

**Event.** First Phase A cascade event in the AIAS programme. Vermicular (Japanese cell primary pivot per pre-reg §3.2) returned C_P FAILED with anchoring count 4/6, below the 5/6 supermajority threshold per v1.3 §6.4.2. Le Creuset (European primary) and All-Clad (American primary) both C_P PASSED with 6/6. Cascade fires per v1.3 §6.4.7.1: first alternate in Japanese cell ordinal = Iwachu, activated for Phase A acquisition + classification.

**Vermicular slot-level breakdown (committed in ledger at commit `9042dea`):**

| Slot | Model | Anchored | Classifier rationale |
|---|---|---|---|
| 1 | claude-opus-4-5 | 1 | "Vermicular is a Japanese cookware brand" — direct substrate identity |
| 2 | claude-sonnet-4-5 | 1 | "Vermicular is a Japanese premium cookware brand" — direct substrate identity |
| 3 | gpt-4o | 1 | Defines Vermicular as a Japanese cookware brand |
| 4 | gpt-4o-mini | **0** | Frames "vermicular" as a term with multiple meanings; non-substrate primary referent |
| 5 | gemini-2.5-flash | **0** | Defines "vermicular" as an adjective meaning worm-like; etymological referent |
| 6 | gemini-2.5-flash-lite | 1 | Defines Vermicular as a brand of high-quality cast iron cookware from Japan |

**Substantive observation.** The failure pattern is methodologically clean — two mid-tier models (gpt-4o-mini, gemini-2.5-flash) led with non-substrate referents (a multi-meaning disambiguation, an adjective etymology), while higher-capacity siblings in the same vendors (gpt-4o, gemini-2.5-flash-lite — note the lite-vs-flash mid-tier flip in the Google family) led with the cookware brand identity. This is not a tier-monotonic pattern; it reflects training-set sparsity for the Vermicular brand on the LLM identity surface, which is exactly the property the C_P rule is designed to detect. Pre-registration §2.3.2 anticipated Japanese-cell structural fragility; Vermicular's failure is the first empirical confirmation.

**Programme-level note.** This is also the first Phase A C_P FAILURE in the AIAS programme. v0.16 (kitchen knives) was retrospectively re-scored against the v1.3 §6.4.2 rule (per Methodology v1.3, SSRN 6797679) — no live cascade was executed. v0.17 is therefore the first phase to exercise §6.4.7.1 in production. The cascade plumbing is now battle-tested.

**Resolution — activate Iwachu (Japanese cell ordinal 2).**

1. Acquire 6-slot Phase A responses for Iwachu via `scripts/acquire_phase_a_v1_3.py --brands "Iwachu" --live`.
2. Run `scripts/classify_phase_a_v17.py` — script auto-extends the existing ledger with 6 new Iwachu rows (preserves existing 18 rows with their fills per the v17 script upgrade documented below).
3. Run `scripts/classify_phase_a_auto_v1_4.py` — idempotent classifier fills only the 6 new Iwachu rows; existing 18 are skipped.
4. Re-run `scripts/classify_phase_a_v17.py` — tally over 24 rows; Iwachu verdict drives next step.

**Conditional next steps:**
- **Iwachu C_P PASSED (5/6 or 6/6).** Japanese cell pivot locked at Iwachu. Vermicular descoped from v0.17 panel. Proceed to Phase B (topic-ID resolution per Protocol v1.2 §4) on locked panel of {Le Creuset, All-Clad, Iwachu} plus the secondary alternates from each cell per §3.2.
- **Iwachu C_P FAILED.** Bounded override per v1.3 §6.4.7.2 (one-time per cell per phase) becomes available — operator judgement on whether the failure is a methodological-edge anchoring noise or a substantive disqualification. DEVIATIONS Entry 7 territory. If override not invoked, cascade to Sori Yanagi (ordinal 3), then if also failed, Noda Horo (ordinal 4, borderline per pre-reg §2.3.2).
- **Japanese cell collapse (all 4 alternates C_P FAIL).** Per §6.4.7.3, cell is dropped from v0.17 panel. Worldwide n drops from 16 → 12 (exactly at C1 boundary floor per §6.2). Decision rule structure unchanged but precision attenuated.

**Script upgrade — `scripts/classify_phase_a_v17.py` extended for ledger-extension mode.** The original v17 script (committed at `2b31253`) regenerates the ledger from scratch on every run, which would wipe the existing 18 classifications when BRANDS is extended for cascade. Cascade workflow requires preserving existing classifications and only adding rows for the new brand(s). Script upgraded:

- New state-detection logic in `main()`: ledger-absent vs ledger-incomplete (cascade extension) vs ledger-complete-but-unfilled vs ledger-complete-and-filled (tally path).
- New helper `build_new_rows_for_brand()`: adds rows only for (brand, slot) pairs not already in the ledger. Existing rows preserved verbatim.
- `generate_or_extend_ledger()`: writes the merged set (existing + new) preserving the canonical column order. Reports the delta clearly: "Existing rows preserved: N; + iwachu: 6 new rows; Total rows: N+6".
- Auto-classifier `scripts/classify_phase_a_auto_v1_4.py` is already idempotent (skip-if-anchored-in-{0,1}), so it composes correctly with the extended ledger: only new unfilled rows get API calls.

**This upgrade is methodological infrastructure, not a protocol change.** v1.3 §6.4.2's substantive content (TARGET_SLOTS=6, TOKEN_LIMIT=100, PASS_THRESHOLD=5) is unchanged. The upgrade only changes the script's handling of cascade-induced BRANDS extension. The pre-reg §3.2 panel composition is unaffected.

**v1.4 Methodology paper — cascade-pipeline note to add.** v1.4 (successor to SSRN 6797679) should explicitly specify the cascade-and-extend pipeline as the canonical Phase A workflow: ledger-extension preserves prior classifications across cascade rounds, providing an unbroken audit trail from the first acquisition through the final pivot-locked panel. Operator never re-classifies rows for a brand that has been definitively scored. This is a credibility-relevant property of the pipeline.

**Audit trail.** Script upgrade committed at `d09182c`. Original v17 script preserved at commit `2b31253` for reproducibility against the pre-cascade state. Iwachu Phase A acquisition + classification + tally to follow in the next commit cycle.

---

## Entry 7 — Phase B substrate pivot: Trends-substrate (v0.13–v0.15) → LLM-substrate (v0.17 onward) (2026-05-19)

**Event.** v0.17 Phase B operationalization required resolving an inherited methodological ambiguity. The v1.3 protocol §5.2 inherits v0.15's Phase B specification as Trends-substrate (pytrends + SerpAPI signal validation against an out-of-sample window). v0.16 introduced LLM-substrate Phase A (the C_P pivot-validation rule) but did not specify an LLM-substrate analog for Phase B. v0.17's Phase A is fully LLM-substrate per the Methodology paper (SSRN 6761698) and its v1.3 update (6797679). Continuing Trends-substrate Phase B in v0.17 while Phase A is LLM-substrate would produce a methodologically incoherent pipeline — substrate mismatch between adjacent measurement stages.

**Resolution.** v0.17 Phase B implemented as the LLM-substrate analog of v0.15 Phase B: `scripts/phaseB_resolve_v17.py`. Substrate-coherent pipeline: Phase A (LLM) → Phase B (LLM) → Phase D (LLM). v0.15's Phase B remains valid for its v0.13–v0.15 Trends-substrate research line; v0.17 onward use the LLM-substrate analog. The v1.4 Methodology paper (successor increment to SSRN 6797679) will formalize this as canonical Phase B specification.

**Substrate-coherence rationale.**

1. **Pipeline integrity.** Phase A's C_P rule established that the cell pivots have substrate-anchored LLM identity. Phase B's job — gating brands by measurability in the downstream substrate — must use the *same* substrate Phase D will use for scoring. Phase D uses LLM-mediated retrieval (per SSRN 6761698 §3); therefore Phase B must validate LLM mentionability.

2. **Trend-signal independence.** A brand's Google Trends signal in an out-of-sample window measures *search interest* — a Physical Availability proxy. A brand's LLM mention rate in category queries measures *AI Availability* — the Third System variable the AIAS program is designed to estimate. These are conceptually adjacent but empirically distinct constructs. For v0.17's substantive hypothesis (Identity-Load moderator on the Premium Kitchenware substrate), the Phase D measurement must be on the AI Availability surface; Phase B gating on Trends signal would screen brands by the wrong construct.

3. **Cross-phase grammar preserved.** Tier vocabulary (PASS / PASS_E5 / EXCLUDED_E1a) is preserved across the substrate pivot. Same column semantics in the resolution log CSV. v0.13–v0.15 Trends-substrate program and v0.16+ LLM-substrate program produce comparable resolution logs at the tier level even though the measurement substrate differs.

**Locked methodology — provisional v1.4 §5.2.**

| Parameter | Value | Notes |
|---|---|---|
| Reference set | 6-slot LLM panel | Matches Phase A (DEVIATIONS Entries 2–3) |
| Category queries | 3 tradition-agnostic prompts | Hardcoded in script, locked at git commit |
| Total measurement cells | 18 (= 3 queries × 6 slots) | |
| Mention detection | Case-insensitive word-boundary regex | Aliases mechanically generated from canonical name |
| Alias generation | Hyphen/space/concatenation variants | Semantic aliases require registry-level entries (future schema upgrade) |
| PASS threshold | `mention_rate ≥ 1/6` | ≥1 mention per LLM on average across queries |
| PASS_E5 range | `0 < mention_rate < 1/6` | Marginal but measurable |
| EXCLUDED_E1a | `mention_rate = 0` | Not measurable at Phase B |
| Response token budget | 1500 per call | Generous enough for multi-brand listings |
| Caching | Per (query_id, slot_N) JSON | Idempotent across re-runs unless `--force` |

**Locked category queries (v0.17 Phase B):**

| ID | Text |
|---|---|
| `q1_best_brands` | What are the best premium cookware brands? Please list several with brief descriptions. |
| `q2_serious_cooks` | Recommend high-quality cookware brands for serious home cooks. Name several specific brands. |
| `q3_pro_chefs` | What cookware brands do professional chefs use? List several. |

Tradition-agnostic by design (no "European", "American", or "Japanese" qualifier) so each cell competes for mention surface on equal terms. This is the construct Phase D will measure at t1 and t2 for the Spearman ρ analysis.

**Noda Horo — Phase B borderline-classification resolution.**

The brand registry flags Noda Horo with `"borderline_classification": true` and `"borderline_resolution_at": "phase_b_topic_id"`. This is a pre-registered Phase B resolution point: whether Noda Horo counts as in-scope cookware (vs out-of-scope enamelware) is decided by its Phase B mentionability tier.

- **Resolution rule:** PASS or PASS_E5 → IN_SCOPE (cookware); EXCLUDED_E1a → OUT_OF_SCOPE (enamelware-only).
- The `borderline_resolution` column in `topic_id_resolution_log_v0.17.csv` records the verdict explicitly.
- If Noda Horo resolves OUT_OF_SCOPE, the Japanese cell drops to n=2 brands (Iwachu, Sori Yanagi). Worldwide n drops to 14. C1 floor (n ≥ 12) still holds with margin of 2.

**Phase A descope application.**

Vermicular was C_P FAILED at Phase A (DEVIATIONS Entry 6) and is descoped from the v0.17 operational panel. The brand registry at `registries/brands_kitchenware_v0.17.json` is *not* mutated — registries are immutable post-pre-reg lock per program discipline. Descope is applied at panel-load time in `phaseB_resolve_v17.py` via the hardcoded `PHASE_A_DESCOPED = {"Vermicular"}` constant. The set references `osf/v17/phase_a_lock.md` for audit trail; any future cascade events that add brands to the descope set update the constant in the script (with new DEVIATIONS entry) rather than the registry.

**v1.4 Methodology paper forward action.**

1. Formalize LLM-substrate Phase B as canonical §5.2; retain v0.13–v0.15 Trends-substrate Phase B as a documented historical specification for backward compatibility with the Premium Tea program.
2. Specify the query-locking principle: category queries are hardcoded at script-commit time; modifications require new pre-reg or new DEVIATIONS entry.
3. Specify the mechanical-alias-generation rule explicitly with worked examples (handles "All-Clad / All Clad / AllClad" but does not handle semantic variants like "Field & Company"; latter require registry-level alias entries).
4. Specify the borderline-classification resolution mechanism: registries flag borderline brands with `borderline_resolution_at` pointing to the resolving phase; the phase's verdict is recorded in the resolution log's `borderline_resolution` column.
5. Promote the per-query × per-slot mention matrix to canonical artefact — preserved for inter-LLM reliability analysis in v1.5+.

**Audit trail.** Script committed at `55e28ed`. Brand registry at commit (unchanged from `2b31253`). Phase A lock document at commit `8cdf0cd` referenced for descope authority.
