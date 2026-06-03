# v0.30 (CPC.01) — Scoring Run Log

Pre-reg lock: **v0.30-prereg-r1** (commit 776506b, tag pushed).
Status: **PAUSED at STEP 1** — premise blocker on v0.24 model panel (see below).
No scorer written, no analysis run.

---

## STEP 1 — reused-input certification

Fills the r1 `VERIFICATION.reused_csv_sha256` `TBD-at-lock` placeholder. Immaterial
to the lock: these are already-deposited immutable upstream files.

| Substrate | Phase | Path | Format | sha256 | rows (logical) | cols |
|---|---|---|---|---|---|---|
| v0.18 | A | `osf/v18/data/phase_a_results.json` | JSON | `f8d8b416fd0241b179acf146dde033d36f338a47f3f06622744a39059537fa31` | 3 cells / 24 brands | — |
| v0.18 | B | `osf/v18/data/phase_b_results.json` | JSON | `8d9ea35a6b2ac2816ec7d70575421216404dd37003b15fd86f064196e6490d12` | 24 brands × 3 frames | — |
| v0.22 | A | `osf/v22/phase_a_results.csv` | CSV | `93c1b147c44b9031bfad3eb5806d50fd26404cf9c9b7cea95f2fd8a7a00c246a` | 144 | 9 |
| v0.22 | B | `osf/v22/phase_b_results.csv` | CSV | `e61dff692ed5eee34a3719067fb07328e4bb3035247c78b703e01d07097fce35` | 36 | 7 |
| v0.24 | A | `osf/v24/data/v24_phase_a.csv` | CSV | `a1358f3b86ddb06aad6a59326648286df8dfe0115e40a913e44769606d44ea5b` | 144 | 7 |
| v0.24 | B | `osf/v24/data/v24_phase_b.csv` | CSV | `9af2860b476ca9c39c361ed81728965af35e724b72d7fb66ccc787ef81e13e0f` | 72 | 8 |

All three substrates carry 24 brands in Phase A.

### Model sets (per data, distinct)

| Substrate | Models present | Matches locked REFERENCE_PANEL (opus-4-5, sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite)? |
|---|---|---|
| v0.18 | opus-4-5, sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite | ✅ all 6 |
| v0.22 | opus-4-5, sonnet-4-5, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite | ✅ all 6 |
| v0.24 | **opus-4-7, sonnet-4-6**, gpt-4o, gpt-4o-mini, gemini-2.5-flash, gemini-2.5-flash-lite | ❌ 4/6 — both Claude slots are newer generations |

### Recall (Phase B) structure

| Substrate | Channels | Frames | Recall frames/model | Per-brand mentions in deposit |
|---|---|---|---|---|
| v0.18 | 1 (no split) | 3 (`q1_niche, q2_independent, q3_perfumistas`) | 3 | pre-computed booleans (`cells[*].per_brand[*].per_frame_per_model`) |
| v0.22 | 2 (R_cat / R_cult) | 6 (q1–q3 / q4–q6; 3 per channel — canonical v1.6) | 6 | **NOT extracted — raw `response_text` only** |
| v0.24 | 2 (R_cat / R_cult) | 12 (1–6 / 1–6; 6 per channel — non-canonical) | 12 | pre-extracted `brands_mentioned` (brand_ids) |

Data-derived recall denominator (per STEP 2 spec) absorbs the 3/6/12-frame difference.
v0.18 has **no R_cult channel** — its s(b,m) is a single-channel recall fraction.

### Phase A recognition encoding (for L(b) = C_P, 0–6)

- v0.18: `c_p_score` per brand (0–6) + per-model `recognized` bool.
- v0.22: `recognized` ∈ {yes, no} → count "yes" across 6 models.
- v0.24: `recognized` ∈ {1, 0} → sum across 6 models.

### Brand registries

- v0.24: `osf/v24/registries/v24_registry.json` (maps brand_id → name; needed to resolve `brands_mentioned`).
- v0.18: brands embedded in `phase_a_results.json` cells (+ `PRE_REGISTRATION_v0_18.md`).
- v0.22: brands derivable from Phase A `brand` column (24 distinct); standalone registry file not located.

### v0.22 brand-mention matcher (for resume)

`scripts/score_v22.py` contains v0.22's original canonical brand-mention detection
(raw `response_text` → per-brand mentions). Decision: **reuse this matcher** rather
than reimplement, so v0.30 detection is identical to v0.22's own scoring.

---

## BLOCKER (premise) — STEP 1 halt

**v0.24 was acquired on Claude Opus 4.7 + Sonnet 4.6, not the locked panel's
Opus 4.5 + Sonnet 4.5.** The r1 pre-reg asserts a single fixed six-model panel
"fixed from v0.17 onward" and "present in every CSV." That is literally false for
v0.24: two of the six cross-model dispersion inputs are a different Claude
generation. Since CPC = cross-model dispersion across the fixed panel, this is a
lock-premise issue, not a scoring detail.

**Decision (user, this run): PAUSE.** Do not score. The user will decide whether to
amend the lock (e.g. r2 slot-based + commensurability caveat), swap the substrate,
or re-acquire v0.24 on the 4-5 panel, before any analysis runs.

No `scripts/score_v30.py` was written. No `osf/v30/data/v30_cpc.csv` or
`osf/v30/v30_cpc_verdicts.json` produced. **[Superseded by r2 — see below.]**

---

## STEP 1b — r2 resolution + v0.20 / v0.21 certification

Blocker resolved by **r2 substrate-set amendment** (DEVIATIONS Entry 1, tag
`v0.30-prereg-r2`): trio = **v0.20 skincare + v0.21 cosmetics + v0.22 automotive**
(dropped v0.18 single-channel, v0.24 off-panel). Swap-in inputs certified:

| Substrate | Phase | Path | sha256 |
|---|---|---|---|
| v0.20 | A | `osf/v20/phase_a_results.csv` | `c8ad6335c982ec95883fffa6c3cb185170b3cdd80b8694377c9fb8afb47d390e` |
| v0.20 | B | `osf/v20/phase_b_results.csv` | `4791113a93b8a25866099fa16ea3a8d14c6f82d6e6c24894609506ad25225828` |
| v0.21 | A | `osf/v21/phase_a_results.csv` | `d470940aa497f55588588536173a128a3394af2a6f0bb6e94825738622167d0d` |
| v0.21 | B | `osf/v21/phase_b_results.csv` | `45e4c3acca67f8c6d6ddfe94bd08215bf6287e4b5af194b81eef47f427440ee1` |
| v0.22 | A | `osf/v22/phase_a_results.csv` | `93c1b147c44b9031bfad3eb5806d50fd26404cf9c9b7cea95f2fd8a7a00c246a` (STEP 1) |
| v0.22 | B | `osf/v22/phase_b_results.csv` | `e61dff692ed5eee34a3719067fb07328e4bb3035247c78b703e01d07097fce35` (STEP 1) |

All three: 4.5 Claude pair + four shared non-Claude models; two-channel canonical
recall (3 frames/channel, 6/model); 24 brands. Recall mentions extracted by
**reusing each phase's own matcher** (`score_v20/21/22.py :: detect_mention`,
v1.4 canonical rules).

## STEP 2/3 — scoring (against v0.30-prereg-r2)

Ran `scripts/score_v30.py` (thresholds single-sourced from the pre-reg `SCORING`
dict). Outputs: `osf/v30/data/v30_cpc.csv`, `osf/v30/v30_cpc_verdicts.json`.

| F | Hypothesis | Verdict | Basis |
|---|---|---|---|
| F1 | H_CPC_Computable | **CONFIRM** | recall coverage 79% / 79% / 62% (all ≥ 50%); automotive recall 62% ≫ recognition 4% |
| F2 | H_CPC_LevelConfound | **UNDETERMINED** | testable only in skincare (1/1 confirms, ρ_raw=−0.472, p=.041); cosmetics & automotive: L=C_P saturated → ρ undefined |
| F3 | H_CPC_LevelCorrected | **UNDETERMINED** | skincare confirms (ρ_corr=−0.131, p=.59; 72% attenuation); < 2 testable substrates → cannot reach ≥2/3 bar |
| F4 | H_CPC_SubstrateVariation | **CONFIRM** | Kruskal–Wallis H=14.245, p=0.00081 |
| — | recognition×recall concordance (exploratory) | not computable | recognition-CPC defined for < 3 brands total (saturation) |

**Key finding (v1.7-forward):** the level variable L = Phase A recognition C_P is
**saturated** (C_P = 6 for all 24 cosmetics brands; 23/24 automotive), so the
headline confound test (F2/F3) is mathematically undefined in 2 of 3 substrates.
The r2 swap to a doubly-homogeneous **mid-to-high-IL** trio — which made F4
confound-free — is the same choice that removed recognition-level variance and
made F2/F3 untestable. Apparatus-homogeneity (F4) and level-variance (F2/F3) pull
in opposite directions on substrate selection. Where F2/F3 *could* be tested
(skincare), the designed F2-then-F3 pattern held cleanly.
