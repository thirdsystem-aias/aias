# v0.25 — B2B SaaS Construct Validity
# Acquisition + Analysis Protocol (Mega Prompt)

> **Note:** v0.25 has no LLM probing phase. The "mega prompt" for this study
> is the Google Trends acquisition and analysis protocol. All AI Presence
> data is inherited from v0.24 (SSRN 6838802).

---

## 1. Study overview

**What:** Test whether AIAS Presence scores (from v0.24 B2B SaaS, Protocol v1.6)
predict Google Trends search interest at the brand level.

**Why:** The AIAS 1.0 Synthesis (SSRN 6817841) established AI Presence as a
measurable construct across 6 substrates. The programme's central empirical
limitation is that AI Presence has unverified consumer-level predictive value.
v0.25 begins to close that gap for the v1.6-era measurement base, superseding
the earlier v0.11/v0.12 construct validity work (pre-v1.6 data).

**How:** Correlate brand-level AIAS Presence composite with Google Trends
search interest across all 24 brands in the v0.24 B2B SaaS registry.

---

## 2. Input data (no new LLM calls)

Source: v0.24 B2B SaaS (SSRN 6838802), deposited at OSF osf.io/ec6wh/v24/.

### Phase A — Recognition (C_P)
- 24 brands × 6 LLMs = 144 probes
- C_P per brand: count of models that recognised the brand (0–6)
- Data file: `v24/data/phase_a_recognition.csv`

### Phase B — Recall (R_cat, R_cult)
- 6 probes × 24 brands × 6 LLMs = 36 outputs per channel
- R_cat: category-channel mentions per brand (0–36)
- R_cult: cultural-channel mentions per brand (0–36)
- Data file: `v24/data/phase_b_recall.csv`

### Derived — AIAS Presence composite
- Per brand: mean of C_P_scaled, R_cat_scaled, R_cult_scaled
- C_P_scaled = (C_P / 6) × 100
- R_cat_scaled = (R_cat / 36) × 100
- R_cult_scaled = (R_cult / 36) × 100

### Derived — Identity Load
- Per brand: IL = R_cult − R_cat (signed)
- Used only for H_CV_Discriminant_IL

---

## 3. Google Trends acquisition protocol

### 3.1 Topic-ID resolution

For each of the 24 brands, resolve a Google Trends topic ID (mid) via the
pytrends suggestions API. This disambiguates brand names from homonyms
(e.g., "Stride" the gum vs. "Stride" the Atlassian product).

```python
from pytrends.request import TrendReq
pytrends = TrendReq()
suggestions = pytrends.suggestions(keyword="Salesforce")
# Select the topic mid that matches the B2B SaaS product
```

Deposit raw suggestion outputs to `osf/v25/data/trends_suggestions/`.

**Known disambiguation cases from v0.24:**
- Stride: Atlassian product (not Stride gum) — name collision documented in v0.24
- Slack: Slack Technologies (not the adjective)
- Linear: Linear app (not the mathematical concept)
- Miro: Miro collaboration tool (not Joan Miró the artist)

### 3.2 Pre-acquisition validation

Before locking the acquisition, run a validation pass on an out-of-sample
7-day window (1 week prior to the target acquisition window):

- Active brands (Cells A, B, C): confirm non-zero Trends signal
- Phantom brands (Cell D): confirm near-zero signal (validates disambiguation)
- Pivot brand (Salesforce): confirm stable, high signal

Deposit validation outputs to `osf/v25/data/trends_validation/`.

If any active brand returns zero, investigate topic-ID resolution.
If any Phantom brand returns unexpectedly high signal, investigate whether
the topic ID is resolving to a different entity.

### 3.3 Bundling

Google Trends allows up to 5 comparison terms per query. With 24 brands
and 1 pivot (Salesforce), the remaining 23 brands are distributed across
6 bundles:

| Bundle | Brands (+ Salesforce pivot) |
|--------|----------------------------|
| 1      | Slack, HubSpot, Workday, SAP |
| 2      | Oracle, Notion, Figma, Linear |
| 3      | Airtable, Miro, Cloudflare, ServiceNow |
| 4      | Snowflake, Zendesk, Datadog, Stripe |
| 5      | MongoDB, Twilio, Quip, Yammer |
| 6      | Wunderlist, HipChat, Stride |

Bundle 6 has 3 brands + pivot = 4 terms.

Bundling logic: Cell D (Phantom) brands are spread across bundles 5–6 to
avoid an all-zero bundle that could distort normalization. Enterprise
incumbents (Cell A) are in bundles 1–2 for signal stability.

### 3.4 Acquisition

Engine: SerpAPI Google Trends
Geography: US
Window: 7-day, contemporaneous with v0.24 LLM measurement
Timestamp: locked UTC timestamp captured at acquisition start

```bash
# Per bundle, via SerpAPI:
# engine=google_trends, q=brand1,brand2,...,Salesforce, geo=US, date=YYYY-MM-DD YYYY-MM-DD
```

Deposit raw JSON responses to `osf/v25/data/trends_raw/`.

### 3.5 Cross-bundle normalization

Salesforce appears in every bundle. Per-brand normalized score:

```
brand_normalized = (brand_raw / salesforce_raw_in_bundle) × salesforce_anchor
```

Where `salesforce_anchor` = Salesforce's raw score in Bundle 1 (set as the
reference). This chains all bundles onto a common scale.

---

## 4. Scoring protocol

### 4.1 Correlation computation

For each hypothesis requiring Spearman ρ:

```python
from scipy.stats import spearmanr
from scipy.stats import bootstrap
import numpy as np

def spearman_statistic(x, y, axis=None):
    return spearmanr(x, y).statistic

# Point estimate
rho, p = spearmanr(presence_scores, trends_scores)

# BCa bootstrap CI
result = bootstrap(
    (presence_scores, trends_scores),
    statistic=spearman_statistic,
    n_resamples=10_000,
    method='BCa',
    paired=True,
    random_state=BOOTSTRAP_SEED,
)
ci_lower, ci_upper = result.confidence_interval.low, result.confidence_interval.high
```

### 4.2 Hypothesis evaluation

| Hypothesis | Measure 1 | Measure 2 | Statistic | Confirmed if | Falsified if |
|------------|-----------|-----------|-----------|-------------|-------------|
| H_CV_Primary | Presence composite | Trends | Spearman ρ | CI_low > 0 | ρ ≤ 0 |
| H_CV_Recognition | C_P | Trends | Spearman ρ | CI_low > 0 | ρ ≤ 0 |
| H_CV_Recall | R_cat | Trends | Spearman ρ | CI_low > 0 | ρ ≤ 0 |
| H_CV_Phantom | Presence + Trends | Cell D vs. A+B+C | Mean sep + CI | Non-overlap | Direction reversal |
| H_CV_CellOrder | Cell means | Cell means | Kendall τ | τ = 1.0 | τ ≤ 0 |
| H_CV_Discriminant_IL | IL | Trends | Spearman ρ | CI includes 0 | CI excludes 0 |

### 4.3 Output artifacts

- `osf/v25/v25_verdicts.json` — per-hypothesis verdicts with statistics
- `reports/figs/v25/chart_25_scatter_presence_trends.pdf` — scatterplot (headline figure)
- `reports/figs/v25/chart_25_correlation_matrix.pdf` — correlation matrix heatmap
- `reports/figs/v25/chart_25_cell_comparison.pdf` — cell-level mean comparison

---

## 5. Step sequence

1. **Topic-ID resolution.** Run pytrends suggestions for all 24 brands.
   Deposit to `osf/v25/data/trends_suggestions/`. Review disambiguation.

2. **Pre-acquisition validation.** SerpAPI query on out-of-sample 7-day
   window. Deposit to `osf/v25/data/trends_validation/`. Confirm signal
   patterns.

3. **Lock.** Commit pre-reg content + mega prompt + resolved topic IDs.
   Tag `v0.25-prereg-r1`.

4. **Trends acquisition.** SerpAPI query on target 7-day window. Deposit
   raw JSON to `osf/v25/data/trends_raw/`.

5. **Scoring.** Run cross-bundle normalization. Compute Presence composites
   from v0.24 data. Run all six hypothesis tests. Emit verdicts JSON.

6. **Charts.** Build three figures per chart convention (Akkurat Pro,
   Indigo #37237B, Third System brand format).

7. **Paper.** SSRN paper draft (Carlito, pandoc + xelatex). H_* framing.

8. **Report.** Third System brand-format report (Akkurat Pro, ReportLab).
   P1–P5 propositional register.

9. **OSF deposit.** Full v25 tree to osf.io/ec6wh/v25/.

10. **SSRN submission.** Run `generate_ssrn_packet.py --phase v0.25`.
    Submit. Backfill abstract ID.

---

## 6. Deviations

None at pre-registration. If methodology defects surface pre-acquisition,
amend at `v0.25-prereg-r2` with DEVIATIONS Entry 0 documenting the change.
