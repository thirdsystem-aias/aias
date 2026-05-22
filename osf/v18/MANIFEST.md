# MANIFEST — v0.18 OSF Deposit

Annotated inventory of files in this deposit. Every file is tracked in the
program repo at branch `v0.18-il-gradient` and tagged at `v0.18-prereg-r1`
(commit `183386c`) for the pre-registration artifacts.

---

## Top-level documents

| File | Purpose |
|---|---|
| `README.md` | Public-facing entry point. Phase summary, verdicts, deposit layout, reproduction instructions, citation chain. |
| `MANIFEST.md` | This file. |
| `PRE_REGISTRATION_v0_18.md` | The locked pre-registration. Includes substrate definition, panel, hypotheses, decision rules, verdict matrices, and revision history (Appendix A: r1 → r2 → r3 → r4). |
| `DEVIATIONS.md` | Deviations log opened during v0.18 acquisition. One entry: Cell C pivot cascade exhaustion at the "niche fragrance" Recognition probe, treated as substantive empirical finding. |

---

## `data/` — acquisition data and verdict outputs

| File | Format | Purpose |
|---|---|---|
| `data/phase_a_results.json` | JSON | Phase A Recognition acquisition. Per-cell, per-brand, per-model C_P responses (yes / no) and aggregated C_P score (0–6). Includes pivot cascade log and pivot anchoring outcomes. |
| `data/phase_b_results.json` | JSON | Phase B Recall acquisition. Per-frame, per-model raw response text, parsed brand mentions per brand, and aggregated mention counts (0–18) per brand. Three frames: niche, independent, perfumistas. |
| `data/verdicts/v0_18_verdict.json` | JSON | Machine-readable verdict structure. Three orthogonal verdicts (H_Regime4, H_IL_mod, H_dissoc) with cell diagnostics, condition-check results, resolution path, and dissociation case enumeration. |
| `data/verdicts/v0_18_verdict.md` | Markdown | Human-readable verdict with per-cell diagnostics tables, C1/C2/C3 condition checks (✓ / ✗), three-leg joint moderator routing, and the 9-case dissociation pool listing. |

---

## `figures/` — brand-format report figures

All three figures are produced by `scripts/build_charts_v18.py` at native figsize 7.5 × 5.5 inches (matplotlib + pypdf). Vector PDF output; print-compatible.

| File | Description |
|---|---|
| `figures/chart_01_mention_rate_distribution.pdf` | Phase B mention-rate distribution per cell. Box-and-whisker plots showing within-cell distribution of brand mention counts across 18 observations. Cell A shows distributed Recall; Cell B shows near-total Recall attrition (D.S. & Durga alone with 2/18); Cell C shows sparse cultural-footprint coverage. |
| `figures/chart_02_cell_attrition.pdf` | Cell attrition Phase A → Phase B. Light bars = registered panel (n = 8/cell); dark bars = brands with ≥ 1 mention across 18 Phase B observations. Cell A retains 7/8; Cell B retains 1/8; Cell C retains 4/8. |
| `figures/chart_03_dissociation_scatter.pdf` | Recognition × Recall dissociation scatter. C_P score (x-axis, 0–6) vs. Phase B mention count (y-axis, 0–18). Shaded Iwachu-pattern quadrant (C_P ≥ 5 and mentions ≤ 2). 9 v0.18 cases plotted in quadrant; black × marks v0.17 Iwachu reference. |

---

## `scripts/` — acquisition, scoring, and chart pipeline

| File | Purpose |
|---|---|
| `scripts/_path.py` | sys.path bootstrap so the `protocol/` package resolves when scripts are run directly. Import this once before any `from protocol import …`. |
| `scripts/acquire_phase_a_v18.py` | Phase A driver. For each brand in the locked panel, probes the 6-slot reference panel with the v1.4 C_P probe. Implements the per-cell pivot cascade: anchors at first brand achieving C_P = 6/6; continues to all brands in cell for dissociation analysis. Writes `data/phase_a_results.json`. |
| `scripts/acquire_phase_b_v18.py` | Phase B driver. Sends three query frames (q1 niche, q2 independent, q3 perfumistas) to each of the 6 reference panel models, scans responses for mentions of all 24 registry brands. Writes `data/phase_b_results.json`. |
| `scripts/score_v18.py` | Verdict scorer. Implements the H_Regime4 cascade (C1 → C2 within-cell → C2 IL-gradient → C3) per pre-reg r4 §4.0, the three-leg joint moderator routing, and the dissociation case enumeration. Emits `data/verdicts/v0_18_verdict.{json,md}`. |
| `scripts/build_charts_v18.py` | Renders the three brand-format charts at native 7.5 × 5.5 figsize. ReportLab-compatible vector PDF output. Each chart carries title, italic subtitle, source line, and Third System attribution chrome. |

## `scripts/protocol/` — canonical AIAS v1.4 implementation

The `protocol/` package is the shared canonical layer reused across phases. v0.18 is the first phase to fully exercise v1.4 C2/C3 numerical thresholds; v0.17 had FALSIFIED at C1 before reaching them.

| File | Purpose |
|---|---|
| `scripts/protocol/__init__.py` | Package init. Exports `PROTOCOL_VERSION = "v1.4"` and the canonical methodology citation chain. |
| `scripts/protocol/thresholds.py` | Locked numerical thresholds per pre-reg r4. C1 floor (n ≥ 12), C2 within-cell (top-2 share ≥ 0.50), C2 IL-gradient separation (Cell B − Cell C ≥ 0.10), C3 ranking coherence (ρ ≥ 0.50 in ≥ 2 of 3 cells at n ≥ 5), Iwachu-pattern threshold (C_P ≥ 5 ∧ mentions ≤ 2), bootstrap parameters (10,000 resamples, seed 20260520). |
| `scripts/protocol/providers.py` | Three-SDK dispatch (Anthropic, OpenAI, Google generative). Loads API keys from `.env` via python-dotenv with override=True. Retry/backoff on rate-limit errors. |
| `scripts/protocol/probe.py` | Two probe functions: `probe_brand(brand, model, category)` for Phase A C_P; `probe_frame(query, model)` for Phase B query response. |
| `scripts/protocol/parse.py` | v1.4 brand-mention detection. Case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication across the 24-brand registry. |

---

## `reports/` — brand-format report and typesetting pipeline

| File | Purpose |
|---|---|
| `reports/v18_indie_fragrance.pdf` | Brand-format report. 8–14 pages, Third System Indigo (#37237B) primary, Akkurat Pro typography. Cover + lead spread + methodology + 3 findings + limitations + what's next + hypothesis scoring + closing. |
| `reports/build_report_v18.py` | Two-pass ReportLab + pypdf typesetter. Pass 1: lays out body with chart slot reservations. Pass 2: overlays the three vector chart PDFs into reserved positions. Akkurat Pro auto-detection from `~/.fonts/Akkurat/` and `~/Library/Fonts/`. |
| `reports/v18_indie_fragrance_content.py` | Content module consumed by `build_report_v18.py`. Top-level constants: `COVER`, `STANDFIRST`, `LEAD_DECK`, `EXEC_SUMMARY`, `WHAT_WE_MEASURED`, `PATTERNS`, `HYPOTHESIS_SCORING`, `HYPOTHESIS_DETAILS`, `LIMITATIONS`, `WHATS_NEXT`, `CLOSING`. |

---

## Checksums

SHA-256 checksums of all deposit files are recorded at upload time and visible
in the OSF web UI's per-file view. To verify locally:

```bash
find osf/v18 -type f \( -name "*.md" -o -name "*.json" -o -name "*.py" -o -name "*.pdf" \) \
    -exec shasum -a 256 {} \; | sort
```

---

## Provenance

- **Repo:** github.com/pablou/aias (private; deposit copy here)
- **Branch:** `v0.18-il-gradient`
- **Pre-reg lock commit:** `183386c` (tag `v0.18-prereg-r1`)
- **r4 threshold lock commit:** `1195cb8`
- **Acquisition date:** 2026-05-20
- **Verdict scoring commit:** `91beefd` (`score_v18.py` C1/C2/C3 implementation)
- **Phase A data commit:** `de7c478`
- **Phase B + verdicts data commit:** `baf14c7`

---

*Last updated 2026-05-20. Subsequent updates to the deposit will be logged in `CHANGES.md`.*
