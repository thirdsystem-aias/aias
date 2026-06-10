# v0.34 — Acquisition Manifest (t₂ re-acquisition)

**Phase:** v0.34 — CPC Longitudinal t₁→t₂ Stability
**Generated:** 2026-06-10T12:31:47Z · **Branch base commit:** `2b483cb` (program-docs == v0.33 after FF)
**Status:** PRE-EXECUTION RECORD. No t₂ runner has executed. This manifest is the binding
pre-acquisition lock of *which* t₁ probe set each substrate re-uses, its byte-checksum, the
planned invocation, and the expected output schema. It is anchored with the pre-reg
(`v0.34-prereg-r1`) **before** the first API call.

## Probe-set provenance + checksums (SHA-256)

The "locked artifact" is the file that holds each substrate's t₁ probe text (Phase A
recognition template + Phase B frames, and brand registry where the runner reads frames from
the registry). At t₂ the probe text must reproduce these byte-for-byte; the checksums below are
the t₁ reference values to re-verify immediately before each runner executes.

| Substrate | t₁ runner | Probe-set artifact(s) | SHA-256 |
|---|---|---|---|
| v0.19 audiophile headphones (16) | `osf/v19/run_v0_19.py` (queries gen by `osf/v19/acquire_v0_19.py`) | `osf/v19/phase_a_queries.jsonl` | `276f8f5c16a9b28e813842601b5ecc416b78e6948bfefdf2df7d617b658c687e` |
| | | `osf/v19/phase_b_queries.jsonl` | `75e4838dee08d6862118b6d4ef19d3f38b2d061e8059afc402eab88f874c4188` |
| | | `osf/v19/thresholds_v0_19.json` (probe_template + frames source) | `542fd89b9406d18bb8635baa64d99fa1ce0999cd183f16aa56d3fb023cf6aa61` |
| v0.20 skincare (24) | `scripts/run_acquisition_v20.py` | `prereg/v0_20_registry.json` (`phase_a_probe_template`, `phase_b_frames`) | `eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782` |
| v0.21 cosmetics (24) | `scripts/run_acquisition_v21.py` | `prereg/v0_21_registry.json` (`phase_a_probe_template`, `phase_b_frames`) | `45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3` |
| v0.22 automotive (24) | `scripts/run_acquisition_v22.py` | `prereg/v0_22_automotive_content.py` (`REGISTRY`) | `431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9` |
| | | `scripts/run_acquisition_v22.py` (`PHASE_A_PROBE_TEMPLATE`, `PHASE_B_FRAMES` embedded) | `59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe` |
| v0.23 premium spirits (24) | `scripts/acquire_v0_23.py` | `scripts/acquire_v0_23.py` (`REGISTRY` + prompt embedded) | `7056f4fa88a9c2e353421f9a967470375db77f5f4a17603115810681b87152da` |

**112 brand units total.** v0.19 frames are pre-materialized into `phase_*_queries.jsonl`;
v0.20/0.21 read template+frames from their registry JSON; v0.22 reads brands from its content
module and frames embedded in the runner; v0.23 carries both registry and prompt inline.

## Planned t₂ invocations + expected output schema

Runners are re-pointed to `osf/v34/data/` at acquisition time (anchor-time edit; not done in
kickoff). Output schema must match t₁ exactly per substrate.

| Substrate | Planned invocation (output → `osf/v34/data/`) | Expected output schema (t₁ parity) |
|---|---|---|
| v0.19 | `python3 osf/v19/run_v0_19.py phase-a` / `phase-b` (paths re-pointed to v34) | jsonl responses → `phase_{a,b}_results.csv`: `brand, panel_model, frame, mentioned, rank` |
| v0.20 | `python3 scripts/run_acquisition_v20.py --registry prereg/v0_20_registry.json --out osf/v34/data/v34_v20_phase_{a,b}.csv` | `model, frame_id, channel, frame_text, response_text` (brand not pre-coded; matcher at scoring) |
| v0.21 | `python3 scripts/run_acquisition_v21.py --registry prereg/v0_21_registry.json --out osf/v34/data/v34_v21_phase_{a,b}.csv` | same as v0.20 |
| v0.22 | `python3 scripts/run_acquisition_v22.py --out osf/v34/data/v34_v22_phase_{a,b}.csv` | same as v0.20 (registry+frames assembled in-runner) |
| v0.23 | `python3 scripts/acquire_v0_23.py --out osf/v34/data/` | JSON: `brand_id (S01–S24), brand_name, model_id, response_text, brand_mentions` |

*(Exact `--out`/path flags to be confirmed against each runner's argparse at forwarding time;
v0.22 hardcodes `osf/v22/` and v0.19 uses `SCRIPT_DIR`-relative paths, so both need a small
re-point edit — verbatim probe text, changed output target only.)*

## Δt covariate (descriptive; no Δt-dependent hypothesis)

t₁ acquisition dates from phase tags; t₂ = first v0.34 acquisition call (≈ 2026-06-10, recorded
exactly at run time).

| Substrate | t₁ acquisition (tag) | t₂ (planned) | Δt (days, approx) |
|---|---|---|---|
| v0.19 | 2026-05-20 (`v0.19-acquired`) | ≈2026-06-10 | ≈21 |
| v0.20 | 2026-05-21 (`v0.20-acquisition-locked`) | ≈2026-06-10 | ≈20 |
| v0.21 | 2026-05-22 (`v0.21-prereg-r1`; no acq-lock tag) | ≈2026-06-10 | ≈19 |
| v0.22 | 2026-05-25 (`v0.22-acquisition-locked`) | ≈2026-06-10 | ≈16 |
| v0.23 | 2026-05-26 (`v0.23-scoring-locked`) | ≈2026-06-10 | ≈15 |

## OPEN DESIGN FORK — model-ID pinning (needs ruling before lock)

All five t₁ runners pin **alias** IDs (`claude-opus-4-5`, `claude-sonnet-4-5`, `gpt-4o`,
`gpt-4o-mini`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`), **not** dated snapshots. At t₂
(checked 2026-06-10) the aliases resolve to:

- `claude-opus-4-5` → `claude-opus-4-5-20251101`
- `claude-sonnet-4-5` → `claude-sonnet-4-5-20250929`
- `gpt-4o`, `gpt-4o-mini`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` → alias (no dated form surfaced)

This collides with the design phrase "panel pinned to **t₁ version IDs**":

- **(a) Re-run verbatim (aliases):** literally "identical to the locked t₁ pipeline." Captures
  real-world drift — the same name a caller would use, resolving to whatever snapshot is live.
  Temporal-stability verdict then *includes* silent version drift.
- **(b) Pin t₁ dated snapshots:** isolates prompt/sampling temporal variance from version drift —
  but is **INFEASIBLE**. The t₁ substrate data captured **only the alias** (`model`/`model_id`/
  `panel_model`); no substrate recorded a provider-returned dated version
  (`v23_phase_a_scored.json` keys, `v20` CSV headers, `v19` headers all confirmed — no
  `returned_model`/`model_version`/`response_model` field). There is no record of what the
  aliases resolved to in May 2026, so the t₁ dated IDs cannot be reconstructed.

**RESOLUTION → (a) re-run verbatim with the t₁ aliases.** This is both the only feasible path
and the most faithful to "identical to the locked t₁ pipeline." Silent version drift between t₁
and t₂ (e.g. `claude-opus-4-5` → a newer dated snapshot) is therefore **part of** the measured
(in)stability and must be named explicitly in the pre-reg Limitations and panel-status table.
At t₂ the runner **will** capture the provider-returned dated ID per call (a forward improvement
over t₁), recorded as a descriptive provenance column — establishing the dated baseline for any
future t₃ wave. (Subject to user confirmation at the review pause.)
