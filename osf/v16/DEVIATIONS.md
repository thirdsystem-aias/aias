# v0.16 Deviations Log

Pre-registration: `v0.16-prereg` (re-tagged after pre-acquisition correction;
see Entry 2 for audit chain). Originally tagged at commit `a5b50c7` on
16 May 2026; corrected and re-tagged on 16 May 2026 (same day, pre-acquisition).
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

## Entry 2 — H_Regime4_replication_knives Condition 2/3 alignment to v0.15 canonical (pre-acquisition correction)

**Date of correction:** 16 May 2026 (same day as original tag).
**Stage:** Pre-acquisition (no Trends data, no LLM data, no scoring runs
executed against the v0.16 pre-reg prior to correction).
**Status:** Pre-acquisition typographic correction to align Condition 2
operationalization and Condition 3 control variables with the v0.15
canonical (commit `cc9df0d`, tag `v0.15-prereg`) and the AIAS Presence
Measurement Protocol v1.2 §3.4 (SSRN 6761698). Original tag preserved in
git history at commit `a5b50c7`; tag `v0.16-prereg` re-created at the
post-correction commit. Full audit chain follows.

### What changed

The original v0.16 pre-registration (commit `a5b50c7`,
`registries/PRE_REGISTRATION_v0_16.md` as of that commit) specified
H_Regime4_replication_knives Condition 2 as:

> bivariate ρ(brand_age, AI_presence) ∈ (−1, +0.35)

and Condition 4 (residual partial) as:

> partial ρ(brand_age, AI_presence | tier, tradition_cell) < 0

The corrected v0.16 pre-registration aligns to the v0.15 canonical:

> Condition 2: |ρ(AI_presence, Trends)| < 0.35
> Condition 3: partial ρ(AI_presence, Trends | brand_age, tradition_cell) < 0

Specifically:

1. **Condition 2 variable.** The canonical bivariate correlation tests
   AI Presence against Google Trends search interest (the substrate market
   signal), not against brand age. Brand age moves to Condition 3's partial
   correlation as a control variable.
2. **Condition 2 threshold form.** Symmetric |ρ| < 0.35 replaces asymmetric
   (−1, +0.35). The asymmetric form would have permitted strongly negative
   bivariate ρ to satisfy the condition, contrary to the "weak relationship"
   semantics of Regime 4.
3. **Condition 3 controls.** brand_age (continuous, rank-transformed) +
   tradition_cell (categorical, dummy-encoded) replaces tier + tradition_cell.
   v0.15 (`score_v15.py` lines 287–388, 537–603) does not use tier as a
   control; v0.14 used premium_tier and v0.15 explicitly retired that
   control in favor of tradition. v0.16 inherits the v0.15-canonical
   control set.
4. **Condition consolidation.** The original Condition 3 (sign consistency
   across waves) is removed as a separate condition; sign consistency is
   implicit in the v0.15-canonical "both waves" requirement on Conditions 2
   and 3.
5. **PARTIAL verdict preserved as v0.16 refinement.** v0.15 is binary
   CONFIRMED / FALSIFIED. v0.16 retains PARTIAL as a strict
   sub-classification of v0.15-canonical FALSIFIED — covers the case where
   bivariate weakness holds but the residual partial is positive
   (non-saturated weak). This is a refinement, not a contradiction.

### Why the original was wrong

The original pre-reg used the v0.14 wording of H_Regime4_replication.
v0.15 (`cc9df0d`, `score_v15.py` docstring lines 5–9) explicitly canonicalized
the condition wording: ρ(AI, brand_age) → ρ(AI, Trends), per AIAS Protocol
v1.2 §3.4, correcting v0.14 §3.3 ambiguity. The v0.16 draft inadvertently
carried forward the v0.14 wording rather than the v0.15-canonical
operationalization. The error is typographic — wrong-version carry-forward
— not a substantive deviation from the programme's measurement design.

### Why correction is permissible

Pre-registration discipline permits correction of typographic and
operationalization errors when ALL the following hold (this case satisfies
all four):

1. **No data has been collected against the original pre-reg.** Phase A
   pivot validation, Phase B topic-ID resolution, and acquisition session
   have not been executed for v0.16. No analytic run has used the original
   Condition 2/4 wording.
2. **The correction aligns with a previously-canonicalized specification.**
   v0.15-prereg (`cc9df0d`) and AIAS Protocol v1.2 §3.4 (SSRN 6761698) are
   the canonical sources; the corrected v0.16 wording matches them
   verbatim in operationalization.
3. **The correction is fully audited.** The original commit (`a5b50c7`)
   remains in git history, the original wording is reproduced verbatim in
   this Entry, the rationale is explicit, and the tag movement is
   documented with both pre- and post-correction commit hashes.
4. **Cross-phase comparability is preserved.** The corrected v0.16
   pre-reg specifies the same Regime 4 conditions as v0.15. Without
   correction, v0.16's verdict would not be directly comparable to v0.14
   or v0.15 verdicts, breaking the empirical floor of the Regime 4
   programme claim.

### Audit chain

- Original tag: `v0.16-prereg` @ `a5b50c7` (deleted 16 May 2026,
  pre-acquisition)
- Correction commit: [populates at re-tag commit hash]
- Re-created tag: `v0.16-prereg` @ [post-correction commit hash]
- Original wording recoverable via:
  `git show a5b50c7:registries/PRE_REGISTRATION_v0_16.md`

H_Discourse_Language_carryforward decision rules were NOT affected by this
correction and remain unchanged from the original tag.

---

## Audit notes

Pre-registration package locked at the re-created `v0.16-prereg` tag includes:
- `registries/brands_kitchen_knives_v0.16.json` (24 panel brands +
  12 alternates; 5 tradition cells; brand-mark public introduction date
  convention applied to 5 brands per top-level `brand_age_convention` block)
- `registries/PRE_REGISTRATION_v0_16.md` (two pre-registered hypotheses:
  H_Regime4_replication_knives — corrected per Entry 2 to v0.15-canonical
  operationalization — and H_Discourse_Language_carryforward — unchanged
  from original tag)
- `prompts/prompts_knives_v0.16.json` (20 prompts: 4 general English, 4
  use-case English, 4 tradition-anchored English, 4 tradition-native, 4
  specificity variants; 4 discourse-language pairs anchoring H2)
- `osf/v16/registries/brand_age_sources_v0.16.csv` (36 rows: 24 panel +
  12 alternates; 4 `verify_needed` flags remaining at lock — Sabatier,
  Laguiole, Sunlong, ZHEN)
- `osf/v16/registries/topic_id_resolution_log_v0.16.csv` (37 rows
  skeleton; Phase B populates fillable columns Monday morning)

Methodology base: AIAS Presence Measurement Protocol v1.2 (SSRN 6761698).
Carry-forward base: v0.15 (SSRN 6768059, tag `v0.15-published`,
commit `cc9df0d` for pre-reg canonical).
Lineage extension: v0.8 Discourse-Language Knives (SSRN 6728000).
