# v0.41 — Acquisition Manifest (t₃ re-acquisition)

**Phase:** v0.41 — Long-Horizon Stability t₁→t₂→t₃ (last wave on the retiring six-model panel)
**Prepared:** 2026-11-09 · **Branch base:** `66db425` (branch v0.39 tip, the v0.23 erratum commit)
**Status:** PRE-EXECUTION RECORD (locked r1, 2026-11-09). No t₃ runner has executed. Anchored with
the pre-registration (`v0.41-prereg-r1`) before the first study call.

## Probe-set provenance + checksums (SHA-256)

Same eight artifacts as the t₂ manifest (`osf/v34/prereg/acquisition_manifest_v34.md`). Each
must reproduce its t₁ value byte-for-byte immediately before its runner runs.

| Substrate | t₁ runner | Probe-set artifact | SHA-256 (computed 2026-11-09 on `66db425`) | vs t₁ |
|---|---|---|---|---|
| v0.19 audiophile headphones (16) | `osf/v19/run_v0_19.py (Gemini via protocol/providers.py)` | `osf/v19/phase_a_queries.jsonl` | `276f8f5c16a9b28e813842601b5ecc416b78e6948bfefdf2df7d617b658c687e` | match |
|  |  | `osf/v19/phase_b_queries.jsonl` | `75e4838dee08d6862118b6d4ef19d3f38b2d061e8059afc402eab88f874c4188` | match |
|  |  | `osf/v19/thresholds_v0_19.json` | `542fd89b9406d18bb8635baa64d99fa1ce0999cd183f16aa56d3fb023cf6aa61` | match |
| v0.20 skincare (24) | `scripts/run_acquisition_v20.py` | `prereg/v0_20_registry.json` | `eb9559eaa6595eaf588dc5ec26c5c742d14c91d4ea93aaedd1e4577e3fa25782` | match |
| v0.21 cosmetics (24) | `scripts/run_acquisition_v21.py` | `prereg/v0_21_registry.json` | `45efbae5db983c24e00ad30d4b66369e685857295e8fd292a0ee0ca73349b5d3` | match |
| v0.22 automotive (24) | `scripts/run_acquisition_v22.py` | `prereg/v0_22_automotive_content.py` | `431f919c809c6260815b9a7a10fe14cb915ae2ce67660aaa6ef48227783d66b9` | match |
|  |  | `scripts/run_acquisition_v22.py` | `59f711b82efb0846f8305e7d84423667571e819aa80ad071edb01c9b1c883cfe` | match |
| v0.23 premium spirits (24) | `scripts/acquire_v0_23.py` | `scripts/acquire_v0_23.py` | `7056f4fa88a9c2e353421f9a967470375db77f5f4a17603115810681b87152da` | match |

**8/8 match the t₁ values recorded in the v0.34 manifest.** 112 brand units; 852 calls per wave
(Phase A 672 + Phase B 180).

## Invocation (t₃)

One dispatcher, a logging shell over the verbatim runners (fork of `run_acquisition_v34.py`):

```
zsh -ic 'cd <v0.41 checkout> && AIAS_ROOT=$PWD ~/aias/.venv-v41/bin/python osf/v41/scripts/run_acquisition_v41.py --substrate all'
```

Outputs per substrate under `osf/v41/data/<sub>/`, schemas identical to t₁/t₂. Provenance sidecar
`osf/v41/data/v41_provenance.csv`: substrate, phase, call_index, alias, returned_model_id,
finish_reason, output_tokens, thinking_tokens, timestamp. v0.19 responses are parsed to
`phase_{a,b}_results.csv` afterwards, as at t₂; v0.23 recognition is coded by the same judge
(`claude-sonnet-4-5`), as at t₁ and t₂ (coding, not acquisition).

## Environment

Mac, isolated venv `~/aias/.venv-v41`: Python 3.14.4, anthropic 0.97.0, openai 2.33.0,
google-genai 1.74.0, google-generativeai 0.8.6 (deprecated upstream; required by the verbatim
v0.19–v0.22 runners; reached both Gemini aliases on 2026-11-09). Keys from the login shell.

## Pre-lock technical check (non-acquisition)

2026-11-09 05:23 UTC, `osf/v41/scripts/feasibility_v0_41.py`: the neutral prompt "Reply with
the single word: ready" to each of the six aliases through each of the three runner call paths
(protocol/providers.py for v0.19; `call_llm` in run_acquisition_v20.py for v0.20–v0.22; the
v0.23 runner's own calls). 18/18 ok. Served ids: claude-opus-4-5-20251101,
claude-sonnet-4-5-20250929, gpt-4o-2024-08-06, gpt-4o-mini-2024-07-18 (identical to t₂),
gemini-2.5-flash and gemini-2.5-flash-lite (undated, as at t₂). No study probe sent.

## Δt

| Substrate | t₁ | t₂ | t₃ | t₂→t₃ (days) |
|---|---|---|---|---|
| v0.19 | 2026-05-20 | 2026-06-10 | 2026-11-09 | 152 |
| v0.20 | 2026-05-21 | 2026-06-10 | 2026-11-09 | 152 |
| v0.21 | 2026-05-22 | 2026-06-10 | 2026-11-09 | 152 |
| v0.22 | 2026-05-25 | 2026-06-10 | 2026-11-09 | 152 |
| v0.23 | 2026-05-26 | 2026-06-10 | 2026-11-09 | 152 |

Deadline: complete before 2026-11-24 (earliest Claude Opus 4.5 retirement).
