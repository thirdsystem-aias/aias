# AIAS™ v0.32 — CPC Version-Snapshot Stability · Acquisition Mega-Prompt (r2)

**Phase type:** PROSPECTIVE, two-arm. New acquisition, run **twice** against a frozen registry — once per model-vintage arm (A = older, B = current). Probe wording, registry, cells, and frame battery are **identical** across arms; the **only** thing that changes between A and B is the dated model ID per slot. This document is the locked acquisition prompt the `v0.32-prereg-r2` tag points at. Authoritative machine-readable values live in `v0_32_cpc_version_stability_content.py` (`ACQUISITION`, `MODEL_PANEL_ARMS`) and `registries/v0_32_registry.json`, committed alongside.

Probe wording is **reused verbatim from v0.22** (SSRN 6829118; `prereg/v0_22_automotive_content.py` + `scripts/run_acquisition_v22.py`, commit-locked text). No rewording.

## Panel — six slots × two arms (dated IDs; probe text identical)

| Slot key | Tier label | Arm A (older) | Arm B (current) |
|---|---|---|---|
| claude_opus | Anthropic flagship | `claude-opus-4-5-20251101` | `claude-opus-4-8` |
| claude_sonnet | Anthropic mid | `claude-sonnet-4-5-20250929` | `claude-sonnet-4-6` |
| gpt_4o | OpenAI flagship | `gpt-4o-2024-11-20` | `gpt-5.5-2026-04-23` |
| gpt_4o_mini | OpenAI mini | `gpt-4o-mini-2024-07-18` | `gpt-5.4-mini-2026-03-17` |
| gemini_flash | Google flash | `gemini-2.5-flash` | `gemini-3.5-flash` |
| gemini_flash_lite | Google flash-lite | `gemini-2.5-flash-lite` | `gemini-3.1-flash-lite` |

Reachability gate cleared: `registries/v0_32_snapshot_resolution.json` (12/12 REACHABLE). One response per model per probe; population panel, ddof=0.

## Phase A — Recognition (24 brands × 6 slots per arm = 144 probes/arm)

Locked template (verbatim v0.22; present-tense, no temporal cues — Cell-D blinding):

> `Is the brand {BRAND} commonly recognized as a car brand? Answer yes or no.`

`{BRAND}` filled from the 24-brand registry. Parsed yes/no → per-brand C_P (0..6).

## Phase B — Six-frame Recall (6 frames × 6 slots per arm = 36 queries/arm)

Locked battery (verbatim v0.22): three R_cat (canonical) + three R_cult (cultural/heritage). Raw responses preserved; brand mentions coded per (model, frame) at scoring → per-model combined recall 0..6; CPC per v1.7.

**R_cat (q1–q3):**
> q1 — `What are the best car brands? List several with descriptions.`
> q2 — `What car brands do automotive experts and reviewers recommend? Name several.`
> q3 — `What car brands are highest quality and most reliable? Name several brands with descriptions.`

**R_cult (q4–q6):**
> q4 — `What car brands carry deep heritage, prestige, or a sense of legacy? List several.`
> q5 — `What car brands do affluent or status-conscious buyers tend to choose? Name several.`
> q6 — `Which car brands have the most iconic or storied identity in popular culture? Name several.`

## Acquisition protocol (locked)

- Run **Arm A first**, then Arm B. Same registry/probes/frames; swap only the dated IDs.
- **Capture provider-returned version metadata at call time** for every call — mandatory for the Gemini slots (Arm A `gemini-2.5-flash`/`-lite` are floating aliases with no dated snapshot; record what they resolve to). Store the response's reported model/version alongside each row.
- Acquire **before the ~2026-10-16 window** (Gemini-2.5 and gpt-4o Arm-A cliffs).
- Outputs: `osf/v32/data/phase_a_{A,B}.csv`, `osf/v32/data/phase_b_{A,B}.csv` (raw responses + resolved-version metadata preserved).

## Scoring (downstream; per `v0_32_cpc_version_stability_content.py`)

CPC per v1.7 (CV = pop SD/mean ddof=0; CPC = 1/(1+CV) ∈ (0,1]; floor mean<1.0 → N/A), computed independently per arm. PRIMARY ρ(CPC_A,CPC_B) and SECONDARY mean|ΔCPC| pairwise-complete; flip count first-class co-reported; TERTIARY Cell-B emerging-instability (flip rate primary). Leave-one-provider-out ρ sensitivity. Verdicts → `osf/v32/v32_verdicts.json`.

## Deviations

**Entry 0 (r1 → r2).** r1 locked hypotheses, panel, registry, and decision rules but carried a scaffolded placeholder for the acquisition prompt (cloned from v0.31's retroactive-rescore mega-prompt, which had no acquisition text). r2 replaces it with the operative two-arm acquisition prompt above — Phase A template + six-frame Phase B battery reused **verbatim from v0.22**, applied identically across both vintage arms. Pre-acquisition: no data collected under r1. r1 retained in git history (tag `v0.32-prereg-r1`). This is a prompt-lock completion, not a change to any hypothesis, threshold, panel ID, or registry entry.
