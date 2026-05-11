# AIAS v0.12 — Cross-Category Construct-Validity Expansion

Three-category extension of the v0.11 construct-validity pilot, testing whether the project management software boundary-mismatch finding generalises across categories with structurally different consumer search and AI recommendation patterns. Adds premium running shoes (a high-volume B2C consumer durable category) and premium olive oil (a premium consumer packaged goods category with non-English production origins) to PM software (retained as replication).

Locked acquisition timestamp: **2026-05-11T10:33:22Z**.
Pre-registration tag: **`v0.12-prereg`** (git commit `ae4bd3a`).

---

## What this deposit contains

| Path | Contents |
|---|---|
| `PRE_REGISTRATION.md` | Full 14-section pre-registration document locked prior to any Google Trends acquisition |
| `DEVIATIONS.md` | Methodology notes accumulated during acquisition (Bundle 2 olive oil padding lesson — non-design-altering) |
| `registries/` | Brand registry artifacts (matched subset, topic ID resolution log, brand age sources, Trends query strings, wave windows) |
| `data/phaseA_test/` | Pre-registration pivot validation against the out-of-sample window (California Olive Ranch, Asics) |
| `data/phaseB_suggestions/` | Pre-acquisition topic-mid suggestion logs from pytrends |
| `data/phaseB_validation/` | Solo Phase B validation per brand — establishes E1a exclusions before lock |
| `data/phaseB_bundled/` | Bundled-validation E5 rescue diagnostic for solo-validation failures |
| `data/trends_raw/` | 20 raw SerpAPI Trends bundles (10 bundles × 2 regions, single locked timestamp) |
| `data/trends_processed/` | Per-day pivot-rescaled values and per-brand within-window aggregations with E1b/E5 flags |
| `data/trends_acquisition_log.csv` | 20-row PASS manifest for the acquisition session |
| `analysis/` | Paired dataset, canonical scoring (CSV + JSON), Category-Scale Mismatch table |
| `figures/` | 13 PDF charts (cross-category scatter, per-category rank-shift, per-category partial residual, H6 zones, Scale-Mismatch viz) |

The build-pipeline source code (acquisition scripts, rescaling, scoring, chart builds, paper build) is tracked in the program's git repository alongside the OSF deposit; it is not duplicated here.

---

## Headline finding

The pre-registered prediction was that the v0.11 single-category boundary-mismatch finding would generalise across categories. The prediction is **falsified** at both the H5 magnitude bar (0 of 2 applicable categories show the full v0.11 signature) and the H6 diagnostic-case bar (1 of 2 categories show both Linear-style and Todoist-style brands). The falsifications, however, organise into a sharper substantive finding: the empirical relationship between AI Availability and Mental Availability is category-dependent, with three distinct empirical regimes observable in the v0.12 sample.

**Regime 1 — Marginal correlation with bidirectional boundary mismatch (PM software).** The v0.11 result reproduces with high precision: Spearman ρ = 0.506 at t₁, 0.482 at t₂ (within 0.010 of v0.11's 0.496 and 0.476); H3 falsifies identically at 1 of 3 both waves; H6 confirms with Linear and Todoist as the same diagnostic cases.

**Regime 2 — Strong age-mediated correlation with asymmetric boundary mismatch (premium running shoes).** Spearman ρ = 0.808 at t₁, 0.786 at t₂ — both well above the moderate-to-strong threshold. After age + tier control, partial ρ drops to 0.466 and 0.488 (age + tier mediates approximately 40 percent of the bivariate correlation). H3 falsifies (2 of 3 both waves); H6 falsifies asymmetrically — Linear-style brands surface (Brooks at t₁, Hoka at t₂) but no Todoist-style brand surfaces in either wave.

**Regime 3 — Category-Scale Mismatch (premium olive oil).** Routes to descriptive-only per pre-reg §3.4a (n = 8 at Worldwide, n = 7 at US, both below the hard floor of 10). 7 of 15 matched-subset olive oil brands (46.7 percent) have AI Presence rates ≥ 5 percent at either wave but Trends signal below the platform's display threshold — the two constructs cannot be placed on the same scale at all for nearly half the matched subset.

What unifies the three regimes is the persistence of category-boundary mismatch (H3 falsified in both confirmatory-eligible categories). What differentiates them is magnitude and structural source: direct construct relation (PM software); age-mediated joint variation (running shoes); scale incommensurability (olive oil).

The Tri-System Brand Growth framework's separability claim — that AI Availability is empirically distinct from Mental Availability — is supported across three structurally different categories in three different ways.

---

## Cross-references

**Foundational theoretical paper.** *AI Availability: Extending Mental and Physical Availability into Algorithmic Retrieval.* SSRN [6659000](https://ssrn.com/abstract=6659000).

**Methodological reference.** *AIAS Presence Measurement Protocol v1.1.* SSRN [6722319](https://ssrn.com/abstract=6722319).

**v0.11 construct-validity pilot (direct predecessor).** *A Construct-Validity Pilot for AI Presence Against External Behavioural Data.* SSRN [6745040](https://ssrn.com/abstract=6745040).

**v0.9 AI Presence rates input (matched subset).** *AI Presence Drift: A Longitudinal Re-Baseline of Five Brand Categories.* SSRN [6736878](https://ssrn.com/abstract=6736878).

**Earlier programme papers.** v0.6 cross-category baseline ([6720959](https://ssrn.com/abstract=6720959)); v0.7 phantom-brand designed-for-test ([6721779](https://ssrn.com/abstract=6721779)); v0.8 discourse-language bias designed-for-test ([6728000](https://ssrn.com/abstract=6728000)); v0.10 naive-phantom rate longitudinal stability ([6741163](https://ssrn.com/abstract=6741163)).

---

## Reproducibility

**Pre-registration lock.** PRE_REGISTRATION.md was committed at git commit `ae4bd3a` (tag `v0.12-prereg`) on 11 May 2026 UTC prior to any Google Trends acquisition call against the wave windows. All hypothesis specifications, thresholds, routing rules, n-floors, and at-acquisition exclusion rules are fixed at that commit.

**Acquisition timestamp.** All 20 Trends bundles were acquired in a single locked session at 2026-05-11T10:33:22Z. The per-bundle raw responses (`data/trends_raw/`) are timestamped with this value.

**Computation lineage.** From `data/trends_raw/` through `data/trends_processed/` (pivot-rescaling per pre-reg §5.1) to `analysis/canonical_scoring.json` (hypothesis evaluation), every intermediate file is provided as a row-level CSV or JSON deposit. To reproduce: the acquisition script consumes `registries/topic_id_resolution_log_v0.12.csv` and `registries/wave_windows_v0.12.json`; the rescaling script consumes `data/trends_raw/`; the scoring script consumes `data/trends_processed/per_brand_within_window.csv`, `registries/brand_age_sources_v0.12.csv`, the v0.9 AI Presence rates input (deposited at the v0.9 publication, SSRN [6736878](https://ssrn.com/abstract=6736878)), and the brand registry per category (frozen at v0.6's final state).

**Deviations from design.** None modify any pre-registered hypothesis, threshold, or routing rule. DEVIATIONS.md Entry 1 documents the olive oil Bundle 2 padding methodology lesson ("extra virgin olive oil" generic-term padding swamped the bundle scale, producing quantization noise in the descriptive-arm Trends signal for Brightland / Graza / Kosterina). The lesson is logged for v0.13+ acquisition design; the v0.12 olive oil routing to descriptive-only per pre-reg §3.4a is independent of this observation.

---

## Citation

González Castro, P. U. (2026). *AI Availability and Mental Availability Across Three Categories: A Cross-Category Construct-Validity Expansion of the v0.11 Boundary-Mismatch Finding.* SSRN Working Paper.

---

*This deposit is part of the AIAS Measurement Programme maintained by Third System™. For questions: <pablou@pablou.com>. ORCID: <https://orcid.org/0009-0003-8968-9990>.*
