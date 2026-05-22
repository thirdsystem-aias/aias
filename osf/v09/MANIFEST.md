# MANIFEST — v0.9 OSF Deposit

File-by-file index of the v0.9 deposit. Read alongside `README.md` for orientation.

## /papers/

| File | Description |
|---|---|
| `v09_ssrn_paper_v3.pdf` | SSRN working paper (rendered). ~5,955 body words, blind-review compliant, Carlito 11pt, 9 figures embedded with narrative captions. |
| `v09_ssrn_paper_v3.md` | Source markdown for the SSRN paper. Pandoc + xelatex render pipeline; YAML front-matter specifies Carlito 11pt, setspace `\setstretch{1.36}`, body `\parskip=8pt`, captionsetup `labelfont={bf,it} textfont=it raggedright`. |
| `PRE_REGISTRATION_v09_rebaseline_v1.0.md` | Pre-registration document. Locked at git commit `f8cebbd` (tag `v0.9-prereg-locked`) prior to any t₂ data collection. Contains hypothesis statements with numerical thresholds, registry-freeze convention, matched-subset definition, and sensitivity-check protocol. |

## /reports/

| File | Description |
|---|---|
| `v09_longitudinal_rebaseline.pdf` | Third System brand-format report (rendered). Cover, lead spread, summary spread (pattern matrix), executive summary, methodology, 7 Findings, hypothesis scoring table, hypothesis details, limitations, what's next, closing matter. Akkurat Pro typeface, Indigo `#37237B` brand primary. |

## /figures/

All charts rendered at native figsize per `chart_construction_rules` — no rescaling. Each chart filename encodes the column span (`6col` = full 6-column hero; `4col` = small inline). Chart number (h1–h6 plus pattern1, mode_distribution, pattern_matrix) corresponds to the relevant SSRN paper section.

| File | Figsize (in) | Subject |
|---|---|---|
| `chart_v09_h1_drift_scatter_6col.pdf` | 7.50 × 4.75 | H1 — Per-brand t₁→t₂ drift scatter across all 5 categories on the matched subset. |
| `chart_v09_h2_leaderboard_6col.pdf` | 7.50 × 6.50 | H2 — Top-of-leaderboard composition at t₁ and t₂, one panel per category, t₁-top-three brands marked. |
| `chart_v09_h3_within_cat_variance_6col.pdf` | 7.50 × 4.10 | H3 — Within-category brand-presence stdev at t₁ vs t₂; categories sorted by t₂ variance. |
| `chart_v09_h4_mint_persistence_4col.pdf` | 3.55 × 3.20 | H4 — Mint phantom-brand persistence at gross Presence, with ±5pp stability band shaded. |
| `chart_v09_h5_pattern4_sensitivity_6col.pdf` | 7.50 × 4.40 | H5 — Pattern 4 sensitivity: strict Spanish vs +Graza inclusive vs K-beauty cohorts against thresholds. |
| `chart_v09_h6_cross_model_spread_6col.pdf` | 7.50 × 4.00 | H6 — Per-brand cross-model spread Pearson correlation between t₁ and t₂ by category. |
| `chart_v09_pattern1_spread_6col.pdf` | 7.50 × 4.20 | Post-hoc Pattern 1 — Per-category mean cross-model spread at t₁ and t₂ with v0.6 narrative ordering reference. |
| `chart_v09_mode_distribution_6col.pdf` | 7.50 × 4.50 | Exploratory — Five-mode-taxonomy distribution shifts on the matched subset, t₁ left vs t₂ right per category. |
| `chart_v09_pattern_matrix_6col.pdf` | 7.50 × 4.75 | Summary — v0.6 framework patterns directly tested at v0.9 (Pattern 1, 4, 6) plus brand-mode-share row at t₂; columns are the five categories. |

## /code/

| File | Description |
|---|---|
| `build_charts_v09_rebaseline.py` | Chart generator. Produces all nine `chart_v09_*.pdf` files using matplotlib with mathtext fontset `stix`, brand palette from `third_system_brand.json`. |
| `build_report_v09.py` | Brand-format report builder. ReportLab + pypdf two-pass: pass 1 lays out body with chart-slot reservations at locked figsizes; pass 2 overlays chart PDFs at native resolution. Forks `build_report_v08.py` with v0.9-specific edits to `_slot_lookup`, `HERO_FIGURE_CAPTIONS`, `CHART_FIGSIZE_IN`, header right text, citation, and output filename. |
| `v09_rebaseline_content.py` | Structured content for the brand-format report. Top-level dicts: `COVER`, `STANDFIRST`, `LEAD_DECK`, `EXEC_SUMMARY`, `WHAT_WE_MEASURED`, `PATTERNS` (7 Findings), `HYPOTHESIS_SCORING`, `HYPOTHESIS_DETAILS`, `LIMITATIONS`, `WHATS_NEXT`, `CLOSING`. ReportLab Paragraph HTML markup throughout (`<sub>`, `<font>`, `<b>`, `<i>`). |
| `analyze_v09.py` | Hypothesis scoring against the locked pre-registration. Computes H1 drift bands, H2 leaderboard preservation, H3 within-category variance Spearman ρ, H4 Mint matched-subset gross Presence delta, H5 strict and inclusive Spanish/K-beauty aggregates, H6 cross-model spread Pearson r per category. Writes structured outcome JSON. |
| `analyze_v09_posthoc_pattern1.py` | Post-hoc Pattern 1 replication test. Computes per-category mean absolute |Sonnet − gpt-5.4-mini| Presence per wave, ranks categories, reports Spearman ρ between t₁ and t₂ rankings and between t₂ ranking and v0.6 narrative ordering. |
| `extract_v09.py` | Brand-mention extraction. gpt-5.4-mini at temperature 0 with structured-output classification against the locked v0.6 final-state registries. Produces canonical brand mentions per response. |
| `smoke_providers_v09.py` | Provider availability smoke test. Confirms all six models are reachable via their respective APIs before measurement runs commit. |

## /registries/

Five category registries, frozen at v0.6 final state to support direct longitudinal comparison. Each is a JSON document listing canonical brand names and known aliases.

| File | Brands |
|---|---|
| `brands_pmsoftware.json` | Project management software registry — Asana, Trello, Jira, Monday.com, Notion, ClickUp, etc. |
| `brands_runningshoes.json` | Premium running shoes registry — Nike, Adidas, Brooks, Hoka, On, Saucony, etc. |
| `brands_oliveoil.json` | Premium olive oil registry — Italian, Spanish, Greek, Californian producers. Spanish strict cohort (Castillo de Canena, Núñez de Prado) and Graza diagnostic identified for the H5 sensitivity check. |
| `brands_skincare.json` | Premium facial skincare registry — luxury, dermatology-led, K-beauty, J-beauty cohorts. K-beauty cohort (Beauty of Joseon as the single registered representative) identified for the H5 K-beauty side. |
| `brands_personalfinance.json` | Personal finance applications registry — Mint (phantom-brand subject of H4), YNAB, Quicken, Personal Capital/Empower, Monarch, etc. |

Note on the personal finance registry: the v0.6 measurement carries the `brand_registry_version` stamp `v2-skincare`, inherited from the prior session's module-level constant. The metadata is cosmetic; raw-response inspection confirms the personal finance prompts and registry fired. Disclosed for transparency.

## /data/

### /data/raw/

Raw responses from each model. Organized as `<category>/<model>/<prompt>/<wave>/run_NN.json`. Contains the verbatim model output along with metadata: timestamp, model identifier, prompt class, sampling parameters (temperature 0.7 where supported), token counts, latency.

| Subdirectory | Volume |
|---|---|
| `pmsoftware/` | 6 prompts × 6 models × 8 runs × 2 waves where applicable = up to 576 responses |
| `runningshoes/` | (same) |
| `oliveoil/` | (same) |
| `skincare/` | (same) |
| `personalfinance/` | (same) |

Total raw responses across the deposit: 1,920 (1,440 successful unique × backup retries archived for transparency).

### /data/extracted/

Canonical brand-mention extractions per response. Schema: `{response_id, model, prompt, wave, category, brands_mentioned: [...], brands_unknown: [...]}`. Produced by `extract_v09.py` using gpt-5.4-mini at temperature 0 with structured-output classification.

### /data/mode_classified/

Five-mode-taxonomy classifications per response. Each response is labeled along the brand / mixed / component / authority / refusal taxonomy per AIAS Protocol v1.1 §3.4. v0.6 responses retroactively classified against the same classifier per the methodology decision locked at git commit `e6428a4`.

### /data/scoring/

Hypothesis scoring outputs. Per-hypothesis JSON with the input variables, the computed test statistic, the pre-registered threshold, and the boolean confirm/disconfirm decision. The H5 strict and H5 inclusive readings are reported as separate scoring outputs to preserve transparency.

| File | Description |
|---|---|
| `h1_drift_outcome.json` | Per-brand drift bins, per-category breakdowns, top movers. |
| `h2_leaderboard_outcome.json` | Per-category t₁ top-3 brands and their t₂ rank, with a confirm-by-category boolean. |
| `h3_within_category_variance_outcome.json` | Per-category brand-presence stdev at each wave plus the cross-wave Spearman ρ. |
| `h4_mint_persistence_outcome.json` | Mint matched-subset gross Presence at each wave plus the delta and ±5pp band check. |
| `h5_pattern4_outcome.json` | Spanish strict, Spanish inclusive (with Graza), and K-beauty aggregate Presence values plus per-cohort threshold check. |
| `h6_cross_model_spread_outcome.json` | Per-category Pearson r between t₁ and t₂ on the per-brand Sonnet−mini spread, plus the ≥4 of 5 confirmation. |
| `pattern1_posthoc_outcome.json` | Post-hoc Pattern 1 ranking: per-category mean cross-model spread at each wave, the rank ordering, plus Spearman ρ between t₁ and t₂ rankings and between t₂ ranking and v0.6 narrative ordering. |

## Cross-references

This deposit is part of the AIAS measurement program. Adjacent OSF deposits and their SSRN cross-citations:

| Program element | SSRN abstract |
|---|---|
| AI Availability foundational paper | `6659000` |
| AIAS Presence Measurement Protocol v1.1 (the methodology spine) | `6722319` |
| v0.6 Cross-Category Findings (the t₁ baseline this study re-measures) | `6720959` |
| v0.7 Phantom-Brand Persistence Phase 2 BBB | `6721779` |
| v0.8 Discourse-Language Knives | `6728000` |
| **v0.9 Longitudinal Re-Baseline (this deposit)** | *to be assigned* |

## Provenance

| Lock point | Git commit | Tag |
|---|---|---|
| Methodology decisions (matched-subset convention, retroactive v0.6 mode classification, registry freeze) | `e6428a4` | — |
| Pre-registration (H1–H6 with thresholds, sensitivity protocol) | `f8cebbd` | `v0.9-prereg-locked` |
| Published deposit (this state) | *commit hash at tag* | `v0.9-published` |

---

*Deposit assembled 8 May 2026. For corrections or extensions, contact pablou@pablou.com.*
