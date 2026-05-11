# AIAS v0.12 — OSF Deposit Manifest

Project: `osf.io/ec6wh` (AIAS Measurement Program — Pre-registrations and supplementary materials)
Deposit folder: `/v12/`
Pre-registration lock: git commit **`ae4bd3a`** (tag **`v0.12-prereg`**), 11 May 2026 UTC, prior to any Google Trends acquisition call against the wave windows.
Acquisition lock: **2026-05-11T10:33:22Z** (single locked timestamp covering all 20 bundles × 2 regions).

---

## File inventory

### Top-level

| File | Approx. size | Description |
|---|---|---|
| `README.md` | ~6 KB | Deposit overview, headline finding, cross-references, reproducibility notes |
| `MANIFEST.md` | ~5 KB | This file |
| `PRE_REGISTRATION.md` | 40 KB | Full 14-section pre-registration, locked at `v0.12-prereg` |
| `DEVIATIONS.md` | 4 KB | Entry 1: olive oil Bundle 2 padding methodology lesson (non-design-altering) |

### `registries/` — Brand registry and pre-acquisition decision artifacts

| File | Approx. size | Description |
|---|---|---|
| `brand_age_sources_v0.12.csv` | 13 KB | 46 rows: founding year + age-as-of-2026 + source URLs per brand across 3 categories |
| `matched_subset_v0.12.json` | 2 KB | Per-category matched-subset brand lists from v0.9 |
| `topic_id_resolution_log_v0.12.csv` | 11 KB | 47 rows: Phase B locked acquisition query per brand (T1 / T2 / T3 tier or EXCLUDED_E1a) |
| `trends_query_strings_v0.12.json` | 21 KB | Per-brand T1/T2/T3 acquisition query specifications with Phase B disposition |
| `wave_windows_v0.12.json` | 2 KB | t₁ and t₂ wave window dates both regions |

### `data/phaseA_test/` — Pre-registration pivot validation

Validates that the chosen per-category pivot brand has stable Trends signal against the out-of-sample window (CV < 25% required per pre-reg §6.A).

| File | Description |
|---|---|
| `california_olive_ranch_topic_test_*.json` | Olive oil pivot — passed at mean 83.5, CV 12.4% |
| `asics_topic_test_*.json` | Running shoes pivot — passed at mean 84.5, CV 7.9% |

### `data/phaseB_suggestions/` — pytrends topic-mid resolution

| File | Description |
|---|---|
| `trends_suggestions_v0.12_*.json` | pytrends.suggestions() output for 26 non-pivot brands across olive oil + running (PM software inherited from v0.11 §5.2.1) |

### `data/phaseB_validation/` — Solo Phase B acquisition validation

Establishes E1a exclusions before pre-registration lock. 26 per-brand validation JSONs plus a summary file. Brands returning `notEnoughSearchVolume` / `noResults` from SerpAPI against the out-of-sample window are routed to bundled-validation E5 rescue.

| File | Description |
|---|---|
| `validation_<brand>.json` × 26 | Per-brand solo Trends acquisition against out-of-sample window |
| `validation_summary_*.json` | Aggregated disposition per brand (PASS / FAIL_API / FAIL_DATA) |

### `data/phaseB_bundled/` — Bundled-validation E5 rescue

For brands that fail solo Phase B, this diagnostic tests whether the brand returns non-zero signal when bundled with high-volume pivot terms. Per the post-tag amendment to E1a (§5.4): solo validation FAIL_API → run bundled validation; ALL_ZERO in bundle = E1a confirmed; nonzero in bundle = PASS_E5.

| File | Description |
|---|---|
| `bundle1_*.json` | Olive oil bundle 1 (incumbents + mid-tier) |
| `bundle2_*.json` | Olive oil bundle 2 (challengers + padding) |
| `bundled_summary_*.json` | E1a confirmation outcomes per E1a-candidate brand |

### `data/trends_raw/` — Google Trends acquisition (20 bundles × 2 regions = 20 files)

Locked timestamp 2026-05-11T10:33:22Z. Per-bundle SerpAPI Trends responses with 14-day daily time series for each bundle member.

Bundle composition:
- **PM software** — 5 bundles (incumbents; mid-tier I; mid-tier II; challengers; remainder + concept padding)
- **Olive oil** — 2 bundles (mixed-tier; challengers + category-generic padding [see DEVIATIONS.md Entry 1])
- **Running shoes** — 3 bundles (incumbents; mid-tier mixed; challengers)

Subdirectories: `worldwide/` (10 bundles) and `US/` (10 bundles).

### `data/trends_processed/` — Pivot-rescaled aggregations

| File | Approx. size | Description |
|---|---|---|
| `per_brand_per_day.csv` | 57 KB | 1092 rows: pivot-rescaled daily values per brand per category per region per wave |
| `per_brand_within_window.csv` | 10 KB | 78 rows: per-brand within-window mean/sd/min/max/E1b/raw-eligible/sparse flags |

### `data/trends_acquisition_log.csv`

| File | Approx. size | Description |
|---|---|---|
| `trends_acquisition_log.csv` | 7 KB | 20-row PASS manifest with per-bundle pivot mean range and acquisition timestamp |

### `analysis/` — Canonical scoring

| File | Approx. size | Description |
|---|---|---|
| `per_brand_paired.csv` | 9 KB | 56 rows: paired dataset with AI Presence + Trends + covariates + eligibility flags per brand per category |
| `canonical_scoring.json` | 21 KB | Full hypothesis evaluation: per-category H1–H4 + cross-category H5 + H6 + Category-Scale Mismatch + pooled sensitivity + all sensitivities |
| `canonical_scoring.csv` | 2 KB | Flat-table view of canonical scoring (one row per hypothesis × scope) |
| `category_scale_mismatch_table.csv` | 1 KB | 15 rows: matched-subset olive oil brands with AI Presence + Phase B disposition + Trends acquisition outcome |

### `figures/` — Chart deliverables (13 PDFs)

All PDFs use Akkurat Pro typography and the Third System brand palette (Indigo #37237B, Petro #6A6AB1, Copper Plate #F36C35). Subtitle text wrapped to fit each chart's figsize.

| File | Description |
|---|---|
| `chart_v12_h1_cross_category_scatter_t1.pdf` | F1 — Cross-category H1 scatter t₁ (3-panel headline: PM \| Running \| Olive) |
| `chart_v12_h1_cross_category_scatter_t2.pdf` | F2 — Same shape, t₂ |
| `chart_v12_h3_rank_shift_pmsoftware_t1.pdf` | F3 — PM rank-shift slope t₁ (v0.11 replication evidence) |
| `chart_v12_h3_rank_shift_pmsoftware_t2.pdf` | F4 — PM rank-shift slope t₂ |
| `chart_v12_h4_partial_residual_pmsoftware_t1.pdf` | F5 — PM partial residual t₁ (H4 visualisation) |
| `chart_v12_h4_partial_residual_pmsoftware_t2.pdf` | F6 — PM partial residual t₂ |
| `chart_v12_h3_rank_shift_running_t1.pdf` | F7 — Running rank-shift slope t₁ |
| `chart_v12_h3_rank_shift_running_t2.pdf` | F8 — Running rank-shift slope t₂ |
| `chart_v12_h4_partial_residual_running_t1.pdf` | F9 — Running partial residual t₁ (age + tier mediation visualisation) |
| `chart_v12_h4_partial_residual_running_t2.pdf` | F10 — Running partial residual t₂ |
| `chart_v12_h6_zones_t1.pdf` | F11 — H6 diagnostic zones t₁ (2-panel: PM \| Running with Linear-style and Todoist-style regions shaded) |
| `chart_v12_h6_zones_t2.pdf` | F12 — H6 diagnostic zones t₂ |
| `chart_v12_scale_mismatch_olive_oil.pdf` | F13 — Olive oil Category-Scale Mismatch matched-subset bars with Trends-state markers |

---

## Lineage map (raw → derived)

```
PRE_REGISTRATION.md (locked at v0.12-prereg, commit ae4bd3a)
     │
     ▼
registries/topic_id_resolution_log_v0.12.csv  ◀─── Phase A + Phase B (locked pre-acquisition)
     │
     ▼
data/trends_raw/{worldwide,US}/*_bundle_*.json  ◀─── SerpAPI acquisition at 2026-05-11T10:33:22Z
     │
     ▼ pivot-rescaling per §5.1
data/trends_processed/per_brand_per_day.csv
     │
     ▼ within-window aggregation + E1b/E5 flags
data/trends_processed/per_brand_within_window.csv
     │
     ▼ + v0.9 AI Presence + brand_age_sources_v0.12.csv
analysis/per_brand_paired.csv
     │
     ▼ canonical scoring (H1-H4 per category, H5/H6 cross-category, §10.2 Scale-Mismatch)
analysis/canonical_scoring.{csv,json}
analysis/category_scale_mismatch_table.csv
     │
     ▼ chart building (Akkurat Pro, brand palette)
figures/chart_v12_*.pdf
     │
     ▼ paper composition (Carlito 11pt, 1.36 linespacing, xelatex)
SSRN Working Paper (published separately on SSRN, not in this deposit)
```

---

## Cryptographic anchors

| Artifact | Hash anchor |
|---|---|
| Pre-registration lock | git commit `ae4bd3a` (tag `v0.12-prereg`) |
| Acquisition locked timestamp | 2026-05-11T10:33:22.535262+00:00 UTC |

The git repository the pre-registration was locked in is part of the AIAS Measurement Programme's private build environment; the public-facing artifacts are this OSF deposit and the SSRN paper. The pre-registration document text deposited here (`PRE_REGISTRATION.md`) is bit-identical to the version committed at `ae4bd3a`.
