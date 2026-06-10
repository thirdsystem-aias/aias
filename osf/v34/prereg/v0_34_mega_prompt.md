# v0.34 — CPC Longitudinal t₁→t₂ Stability — Re-Acquisition Protocol

**AIAS™ Measurement Program · Third System™**
**Pre-registration tag:** `v0.34-prereg-r1` · **Phase type:** prospective longitudinal (full re-acquisition at t₂)
**Instrument:** CV-CPC (v0.30 origin, v1.7 definition, *not adopted* — walled) · **Presence:** C_P (v1.6)

> This phase **re-acquires** at t₂ (June 2026) the Phase A (Recognition) and Phase B
> (two-channel six-frame Recall) data for all five omnibus substrates, using each
> substrate's **t₁ acquisition runner verbatim** (re-pointed only at `osf/v34/data/`).
> Registries are bit-identical to the t₁ locks; probe wording is verbatim; the panel is
> the t₁ model aliases. Probe-set byte-fidelity is locked by five SHA-256 checksums in
> `osf/v34/prereg/acquisition_manifest_v34.md`. It is **not** a re-analysis — it produces
> its own t₂ data and compares it to the recomputed t₁ baseline.

---

## Scope

Test whether the CPC-family quantities are **temporally stable** across a ~2–3 week
interval at fixed registries, fixed wording, and the t₁ alias panel:

- **CV-CPC** rank stability (PRIMARY), and whether its drift carries structure **beyond
  Presence drift** (PRIMARY gate — the substantive core);
- **C_P (Presence)** rank stability (SECONDARY, the validated comparator);
- **phantom** persistence (TERTIARY, descriptive).

CV-CPC is analyzed as-computed; v1.7 found it Presence-coupled (|ρ| = 0.77) and did not
adopt it. This phase measures the temporal stability of that quantity, not its validity.

t₁ data lineage routes through the substrate phases (v0.19–v0.23) and the CPC methodology
through v1.7. **v0.31 (SSRN 6880959) is deliberately uncited** (by design); its extraction
*functions* are reused as a computational tool, but the citeable parity anchor is v1.7
`r_per_model`.

---

## Panel + model-ID pinning

Canonical six (3 providers × 2 models): Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o,
GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite. **All six resolved OK at the
2026-06-10 reachability probe** (min-viable-panel = 4; no drop in effect).

| Alias (t₁ pin) | Provider | t₂ resolved | Status |
|---|---|---|---|
| `claude-opus-4-5` | Anthropic | `claude-opus-4-5-20251101` | OK |
| `claude-sonnet-4-5` | Anthropic | `claude-sonnet-4-5-20250929` | OK |
| `gpt-4o` | OpenAI | `gpt-4o` (alias) | OK |
| `gpt-4o-mini` | OpenAI | `gpt-4o-mini` (alias) | OK |
| `gemini-2.5-flash` | Google | `models/gemini-2.5-flash` | OK |
| `gemini-2.5-flash-lite` | Google | `models/gemini-2.5-flash-lite` | OK |

**Pinning is by alias, verbatim.** t₁ ran on aliases and captured no provider-returned
dated snapshot, so dated-ID pinning at t₂ is infeasible. t₂ re-acquires on the same
aliases and writes the provider-returned dated ID per call to a **sidecar**
(`osf/v34/data/v34_provenance.csv`) — **runner output schemas are untouched**, preserving
the parity/smoke-test check (baseline for a future t₃). Silent version drift between waves
is therefore **part of** the measured (in)stability — see Limitations.

**Permitted runner edits (complete set):** (i) the output-directory constant; (ii) the
provenance-sidecar emission. Nothing else — probe text, frame ordering, registry, and the
runner's own output schema are byte-frozen against the t₁ checksums.

**Model-drop rule:** any alias
unavailable at t₂ is excluded pairwise (both waves) with a DEVIATIONS entry; below 4
models the phase halts for re-scope.

---

## Re-acquisition manifest (verbatim runners)

Per-wave call counts: **Phase A 672** (v19 16×6=96; v20–23 24×6=144 each) · **Phase B 180**
(5 × 6 frames × 6 models) · **852 total per wave**.

| Phase | Substrate | Brands | t₁ runner (verbatim) | Probe-set artifact (checksum-locked) | Path |
|---|---|---|---|---|---|
| v0.19 | audiophile headphones | 16 | `osf/v19/run_v0_19.py` | `phase_{a,b}_queries.jsonl`, `thresholds_v0_19.json` | A |
| v0.20 | skincare | 24 | `scripts/run_acquisition_v20.py` | `prereg/v0_20_registry.json` | B |
| v0.21 | cosmetics | 24 | `scripts/run_acquisition_v21.py` | `prereg/v0_21_registry.json` | B |
| v0.22 | automotive | 24 | `scripts/run_acquisition_v22.py` | `v0_22_automotive_content.py` + frames embedded in runner | B |
| v0.23 | premium spirits | 24 | `scripts/acquire_v0_23.py` | `acquire_v0_23.py` (REGISTRY + prompt embedded) | C |

Outputs re-pointed to `osf/v34/data/`. Checksums in `acquisition_manifest_v34.md` are
re-verified immediately before each runner runs. A `run_acquisition_v34.py` dispatcher, if
used, is a **logging shell only** (invoke-and-log; no probe/order/schema changes); default
is the five runners invoked directly under the manifest.

---

## Per-brand metric recovery (both waves, identical pipeline)

- **Path A (v0.19):** `panel_model` + `mentioned`/`rank` are per-model already; pivot to x_{b,m}.
- **Path B (v0.20–22):** brand not pre-coded — detect via the **v1.4 certified matcher**
  (`detect_mention`) against `response_text`, pivot per `model`.
- **Path C (v0.23):** parse `brand_mentions` per `model_id`; **normalize recognition
  `r_level` → binary** (R0→0, else→1) — identically in both waves.
- **CV-CPC**_b = 1/(1+CV(x_{b,1..6})), x = per-model Phase B recall 0..6; FLOOR mean<1.0 → undefined.
- **C_P**_b = count of panel models recognizing b in Phase A (0..6), v1.6.

**Parity (scoped — do not conflate):**
- **v0.20/0.21/0.22:** recomputed t₁ per-model recall **must reproduce
  `osf/methodology/v1_7/data/v1_7_cpc.csv` `r_per_model` bit-for-bit** (citeable anchor;
  `score_v33` gates 72/72). Mismatch → computational-reproducibility note in README, halt.
- **v0.19/0.23:** v1.7 anchor does **not** cover these. Parity = bit-for-bit reproduction
  of the frozen per-model t₁ inputs as consumed by the v0.31→v0.33 arc (`counts_v19`/
  `counts_v23` outputs); provenance-only, stated not overclaimed.

---

## Hypotheses + scoring

Per substrate, Spearman ρ over brands defined in **both** waves; null = Monte Carlo
permutation of t₂ labels, **≥10,000 draws/substrate**, one-sided.

- **H_CPC_Temporal_Stability (PRIMARY):** ρ(CV-CPC_t₁, CV-CPC_t₂). CONFIRMED ρ≥0.70 in
  ≥4/5; FALSIFIED ρ<0.50 in ≥3/5; else MARGINAL.
- **H_CPC_Drift_Beyond_Presence (PRIMARY gate):** (a) ρ(ΔCV-CPC, ΔC_P) across brands,
  reported for all 5; (b) residual-CV-CPC stability — within each wave regress CV-CPC on
  C_P, take residuals, then ρ(t₁-resid, t₂-resid). CONFIRMED iff residual ρ≥0.50 in ≥3/5.
  **Saturation caveat:** if C_P is near-constant among defined brands (flag if all six
  models recognize ≥90% of defined brands), residual-CV-CPC ≈ CV-CPC and the gate is
  *uninformative*, not confirmed — that substrate's gate contribution is down-weighted to
  MARGINAL. Directional lean: **FALSIFIED-or-marginal** (ρ=0.77 coupling; v0.33
  saturation-collapse).
- **H_Presence_Temporal_Stability (SECONDARY):** ρ(C_P_t₁, C_P_t₂). CONFIRMED ρ≥0.80 in
  ≥4/5; FALSIFIED ρ<0.60 in ≥3/5. The higher bar is deliberate — Presence is validated and
  is the comparator floor for the gate.
- **H_Phantom_Temporal_Persistence (TERTIARY, exploratory):** proportion of t₁ phantom-
  flagged brands retaining phantom status at t₂, per substrate + pooled. Descriptive only.

**Δt covariate (descriptive):** per-substrate t₁→t₂ interval (≈15–21 days; v19 21, v20 20,
v21 19, v22 16, v23 15) recorded in the design table; exact t₂ dates stamped at acquisition.
No Δt-dependent hypothesis; heterogeneity in Limitations.

Output `osf/v34/v34_verdicts.json`: per-hypothesis verdict against the locked criteria, plus
per-substrate ρ, permutation p, defined-brand counts, the ρ(ΔCV-CPC, ΔC_P) table,
residual-CV-CPC ρ with saturation flags, phantom persistence proportions, and the Δt table.

---

## Deviations

**Entry 0 (ex-ante, before any acquisition call):** (i) **COI handling carried forward** —
registries are bit-identical to t₁ and v0.34 performs no new brand selection, so each
substrate carries its source-phase COI handling forward unchanged (not a fresh "no
affiliation" assertion). Items of record, paraphrased faithfully from the source phases:
**v0.22 automotive** — the locked v0.22 Declarations §COI discloses that Samsung subsidiaries
hold **tier-2/3** component supply relationships with several registry brands (Harman
International — audio; Samsung SDI — battery cells; Samsung Display — infotainment),
characterized as non-competitive with no brand-level overlap and imposing no restriction on
registry composition (v0.22 DEVIATIONS Entry 0 Part B); **v0.19** — AKG was substituted with
Denon **before** the v0.19 pre-reg lock (AKG owned by Harman International, a Samsung
subsidiary, since 2016) to avoid appearance of conflict (v0.19 DEVIATIONS Entry 1). The v0.34
paper's Declarations §COI carries the v0.22 tier-2/3 language forward; no blanket "no Samsung
affiliation" claim is locked. (ii) **External-anchor preamble** — binding sequence: content lock → commit → tag `v0.34-prereg-r1` →
`git push origin v0.34 --tags` → `osf_upload.py osf/v34/prereg → osf.io/ec6wh/v34/prereg/`
→ verify both remotes → only then the first t₂ call; `OSF_TOKEN` confirmed present before
upload (no half-anchored state). No "Entry −1" — the anchor preamble lives within Entry 0,
per v0.30/v0.32 precedent.
