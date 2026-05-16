# v0.16 Deviations Log

Pre-registration: `v0.16-prereg` (commit `a5b50c7`, locked 16 May 2026).
This file records procedural notes, empirical findings, and any departures
from the locked pre-registered protocol that arise during data acquisition,
scoring, and analysis.

---

## Entry 1 — Bare-canonical Phase B queries (inherited from v0.15 / v0.14)

**Date inherited:** 16 May 2026 (carry-forward from v0.15 DEVIATIONS Entry 1,
which itself inherited from v0.14 DEVIATIONS Entry 1).
**Stage:** Phase B (topic-ID resolution + solo/E5 validation).
**Status:** Methodology carried forward unchanged from v0.15. Not a v0.16
deviation; recorded here for protocol completeness and to maintain the
cross-phase audit chain.

Phase B Stage 2 (solo SerpAPI) and Stage 3 (bundled E5 rescue) query
SerpAPI using the bare canonical brand name for ALL brands, not
pytrends-derived Knowledge Graph MIDs. v0.14 Phase B v1 results showed
pytrends.suggestions() frequently surfaced product-variant or location
entities rather than brand-level entities. The bare-canonical convention
aggregates Trends signal across all brand products and avoids the failure
mode.

For v0.16 kitchen knives, the bare-canonical convention applies with
particular emphasis on the high-risk brand subset flagged in
`PRE_REGISTRATION_v0_16.md` Tables and §6: Sabatier, Laguiole, Mac, ZHEN,
Made In, Friedr. Dick, CCK, Global, and Güde. The v1.2 §4 5-stage protocol
resolves topic-ID at acquisition lock; any brand failing §4 confusion
threshold activates the pre-registered alternate per §6 substitution order.

See `~/aias/osf/v15/DEVIATIONS.md` §1 and `~/aias/osf/v14/DEVIATIONS.md` §1
for full rationale, root-cause analysis, and pre-registration scope
justification.

---

## Entry 2 — [reserved for first v0.16-specific entry]

[To be populated during Phase A pivot validation or Phase B topic-ID
resolution. Standard pattern: Date, Stage, Status (deviation /
procedural-note / empirical-finding), prose rationale, cross-references.]

---

## Audit notes

Pre-registration package locked at `a5b50c7` includes:
- `registries/brands_kitchen_knives_v0.16.json` (24 panel brands +
  12 alternates; 5 tradition cells; brand-mark public introduction date
  convention applied to 5 brands per top-level `brand_age_convention` block)
- `registries/PRE_REGISTRATION_v0_16.md` (two pre-registered hypotheses:
  H_Regime4_replication_knives and H_Discourse_Language_carryforward)
- `prompts/prompts_knives_v0.16.json` (20 prompts: 4 general English, 4
  use-case English, 4 tradition-anchored English, 4 tradition-native, 4
  specificity variants; 4 discourse-language pairs anchoring H2)
- `osf/v16/registries/brand_age_sources_v0.16.csv` (36 rows: 24 panel +
  12 alternates; 4 `verify_needed` flags remaining at lock — Sabatier,
  Laguiole, Sunlong, ZHEN)

Methodology base: AIAS Presence Measurement Protocol v1.2 (SSRN 6761698).
Carry-forward base: v0.15 (SSRN 6768059, tag `v0.15-published`).
Lineage extension: v0.8 Discourse-Language Knives (SSRN 6728000).
