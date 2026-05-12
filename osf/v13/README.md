# AIAS Measurement Programme · v0.13

**Four Empirical Regimes in AI-Mediated Brand Visibility**
*A Five-Category Construct-Validity Expansion of the v0.12 Three-Empirical-Regimes Finding*

**Author** &nbsp; Pablo Ulpiano González Castro
**Version** &nbsp; v0.13
**Date** &nbsp; 12 May 2026
**Pre-registration** &nbsp; locked at git commit `1a6294d` (tag `v0.13-prereg`), 11 May 2026 UTC, prior to data collection
**SSRN companion paper** &nbsp; <https://ssrn.com/abstract=6750498>
**OSF project root** &nbsp; <https://osf.io/ec6wh/>

---

## What this is

The AIAS Measurement Programme tracks **AI Presence** — the rate at which each brand appears in matched large-language-model responses to category-recommendation prompts — and tests its construct validity against external behavioural validators (in this version: Google Trends search-interest rank). The programme is published openly across SSRN (academic papers), OSF (data and analysis archives), and Third System brand-format reports (industry-readable summaries).

v0.13 extends the construct-validity arc to **five product categories at two waves**, eight days apart:

- Project management software (18 brands; pivot Asana; carry-forward from v0.12)
- Premium running shoes (17 brands; pivot Asics; carry-forward from v0.12)
- Premium olive oil (20 brands; pivot California Olive Ranch; carry-forward from v0.12; descriptive-only routing inherited per pre-reg §3.6a)
- Premium facial skincare (31 brands; pivot CeraVe; **new in v0.13**)
- Personal finance apps (16 brands; pivot YNAB; **new in v0.13**)

Eight pre-registered hypotheses (H1–H8) evaluate per-category construct validity, two cross-category integrators of v0.12's marginal-direct signature, the three-regime taxonomy as a classification test against a wider panel, and a phantom-persistence diagnostic anchored on Mint (the Intuit personal-finance app shut down September 2025).

---

## Findings overview

**H7 — Three-regime clean classification: FALSIFIED at 3-of-5 (productive falsification).**
Three categories classify into the pre-registered regimes: PM software → Regime 1 (Marginal direct, ρ ≈ 0.50); running shoes → Regime 2 (Age-mediated strong, ρ ≈ 0.80, large covariate decrement; boundary-flagged at t₂); olive oil → Regime 3 (Scale-mismatch via the n-floor descriptive route). The two new categories — skincare and finance — sit in a region the taxonomy does not anticipate. A provisional fourth regime is named: **Covariate-saturated weak** (sufficient n, weak bivariate ρ, residual partial ρ negative after age + tier control).

**H8 — Mint phantom-persistence: CONFIRMED canonically.**
Mint retains 44.79% / 41.67% AI Presence across the two May 2026 waves (seven to nine months post-shutdown), ranks fifth in personal-finance recommendations at both waves, and records zero Google Trends signal in both regions at both waves. The cleanest phantom-persistence signature observed across the programme to date. The Phantom Brand Persistence regularity now spans five programme phases.

**H5, H6 — v0.12's cross-category signatures: FALSIFIED at 1-of-4 each.**
Both replicate only in PM software. What looked like candidate cross-category regularities in the v0.12 three-category panel turn out to be project-management-software-specific structural properties.

**Pooled cross-category alignment.**
Pooled rank-within-category Spearman ρ = 0.459 at t₁ (p = 0.0001) and 0.475 at t₂ (p < 0.0001), n ≈ 70 — the aggregate signal survives the per-category heterogeneity.

---

## Deposit structure

```
v13/
├── README.md                          (this file)
├── MANIFEST.md                        file inventory + lineage
├── PRE_REGISTRATION_v0_13.md          14-section pre-registration document, locked at v0.13-prereg
├── DEVIATIONS.md                      Entries 1-3: pre-lock amendments + Regime 4 post-acquisition note
│
├── data/                              raw + processed Trends data
│   ├── pivot_bundles/                 SerpAPI Trends responses, 2 regions × 2 waves
│   ├── phaseB_resolution/             topic-ID resolution logs per category
│   ├── rescaled/                      pivot-normalised brand-day matrices
│   └── acquisition_log.json           single-timestamp acquisition session metadata
│
├── registries/                        locked at v0.13-prereg
│   ├── brands_pmsoftware.json         (carry-forward from v0.6)
│   ├── brands_running.json            (carry-forward from v0.6)
│   ├── brands_oliveoil.json           (carry-forward from v0.6)
│   ├── brands_skincare.json           (new in v0.13)
│   ├── brands_finance.json            (new in v0.13)
│   └── brand_age_sources_v0.13.csv    93 brands (46 v0.12 carry-forward + 47 v0.13-new DRAFT)
│
├── analysis/                          canonical scoring outputs
│   ├── canonical_scoring.json         per-category + cross-category H1-H8 outcomes
│   ├── per_brand_paired.csv           per-brand AI Presence × Trends paired table
│   └── partial_correlation_details/   per-category partial-Spearman intermediate outputs
│
├── figures/                           4 chart PDFs (Akkurat Pro + STIX mathtext)
│   ├── chart_v13_h7_fourregime_classification.pdf    (HEADLINE)
│   ├── chart_v13_h8_mint_phantom.pdf
│   ├── chart_v13_per_category_rho_comparison.pdf
│   └── chart_v13_pooled_rank_scatter.pdf
│
├── reports/
│   └── v13_fourregimes.pdf            Third System™ brand-format report
│
└── papers/
    └── v13_ssrn_paper.pdf             SSRN working paper (Carlito, full Declarations)
```

---

## Reproduction

The canonical scoring (H1–H8 outcomes in `analysis/canonical_scoring.json`) reproduces in under 30 seconds from the deposit:

```bash
git clone <programme-repo>      # (programme code repository, see below)
git checkout v0.13-prereg       # locks at pre-registration state (commit 1a6294d)
cd aias
python scripts/score_v13.py     # reads from this OSF deposit's registries/ and data/rescaled/
```

The chart and report rebuilds run from the same state:

```bash
python scripts/build_charts_v13.py   # writes 4 PDFs to figures/
python reports/build_paper_v13.py    # writes SSRN paper PDF
python reports/build_report_v13.py   # writes brand-format report PDF
```

Build-script code is held in the AIAS programme git repository (committed alongside the pre-registration tag) and is not redundantly redeposited at OSF.

---

## Citation

**Suggested citation (full):**
> González Castro, P. U. (2026). *AI Availability and Mental Availability Across Five Categories: A Construct-Validity Expansion of the v0.12 Three-Empirical-Regimes Finding*. Third System™. AI Presence Index v0.13. SSRN: <https://ssrn.com/abstract=6750498>.

**OSF deposit citation:**
> González Castro, P. U. (2026). AIAS Measurement Programme v0.13 — Four Empirical Regimes [data archive]. Open Science Framework. <https://osf.io/ec6wh/>

---

## Cross-references

Prior programme phases (chronological):

| Version | Title | SSRN | Date |
|---|---|---|---|
| v0.6 | Cross-Category Findings | [6720959](https://ssrn.com/abstract=6720959) | April 2026 |
| v0.7 | Phantom-Brand Persistence BBB | [6721779](https://ssrn.com/abstract=6721779) | May 2026 |
| v0.8 | Discourse-Language Knives | [6728000](https://ssrn.com/abstract=6728000) | May 2026 |
| v0.9 | Longitudinal Re-Baseline | [6736878](https://ssrn.com/abstract=6736878) | May 2026 |
| v0.10 | Naive-Phantom Rate Stability | [6741163](https://ssrn.com/abstract=6741163) | May 2026 |
| v0.11 | PM × Trends Construct Validity Pilot | [6745040](https://ssrn.com/abstract=6745040) | May 2026 |
| v0.12 | Three Empirical Regimes | [6748341](https://ssrn.com/abstract=6748341) | May 2026 |
| **v0.13** | **Four Empirical Regimes** | **[6750498](https://ssrn.com/abstract=6750498)** | **May 2026** |

Theoretical anchor:

- **AI Availability foundational paper** — *Extending Mental and Physical Availability into Algorithmic Retrieval* — SSRN [6659000](https://ssrn.com/abstract=6659000)
- **AIAS Presence Measurement Protocol v1.1** — SSRN [6722319](https://ssrn.com/abstract=6722319)

---

## Declarations

**Conflict of interest.** The author serves as Director, Corporate Brand Creative and Governance at Samsung Electronics America. The research presented here is independent of Samsung Electronics America and does not constitute Samsung research. No Samsung Electronics America data, personnel, or commercial interests influenced the design, conduct, analysis, or reporting of this study. The brand populations evaluated in this study (PM software, running shoes, olive oil, skincare, personal finance) do not include Samsung product lines.

**Funding.** Self-funded. No external funding sources contributed to this research. The AIAS Measurement Programme is operated independently under the Third System research entity.

**Ethics approval.** Not applicable. This study does not involve human subjects, patient data, or biological samples. All measurements derive from publicly accessible APIs (Google Trends via SerpAPI) and standardised prompts to commercially deployed large language models (Anthropic Claude Sonnet 4.6, OpenAI GPT-5.4-mini). No human participants were enrolled, no personally identifiable data were collected, and ethics approval was therefore not required.

**Licence.** Data and findings: CC BY 4.0. Build-pipeline code (held in the programme git repository): open source under permissive licence pending Phase 4 release.

---

## Contact

Pablo Ulpiano González Castro · pablou@pablou.com · pablou.com
ORCID: [0009-0003-8968-9990](https://orcid.org/0009-0003-8968-9990)
Third System™ · <https://thirdsystem.ai> · hello@thirdsystem.ai
