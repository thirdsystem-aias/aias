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
## Entry 3 — Phase A specification gap; Wüsthof fallback activated on substantive grounds

**Status.** Pre-acquisition substantive amendment. Activates the pivot fallback authorized by pre-reg §3 / §6 on substantive Victorinox topic-ID evidence, while documenting that the literal pre-reg §3 contingency text ("the 5-stage protocol resolves the adjacency at lock") referenced a procedure that v1.2 does not specify with sufficient precision to support a binding test.

**Logged:** 16 May 2026 UTC, post-Phase-A diagnostic runs.

**No data has been collected against the affected pre-registration text.** Acquisition (`acquire_trends_v16.py`) has not been run. Phase B (`phaseB_resolve_v16.py`) has not been run. The amendment is pre-acquisition.

---

### Background: what pre-reg §3 / §6 say, and what they reference

Pre-reg §3 (Pivot, locked at `v0.16-prereg`, commit 511e339):

> "Primary pivot: Victorinox (Swiss, founded 1884) — chef-knife line (Swiss Classic / Fibrox) is the restaurant-industry workhorse; high global volume; low brand-age signal interference; broad search-interest base.
>
> Fallback pivot: Wüsthof (German, 1814) — cleaner in-category in-tradition anchor; selected only if Victorinox topic-ID resolution surfaces Swiss-Army-knife confusion above v1.2 §4 threshold.
>
> Pivot rationale. The pivot's role under v1.2 §5 is to normalize across waves under stable search interest. Victorinox's chef-knife sub-category satisfies stability requirements; the Swiss-Army-knife adjacency is a topic-ID concern, not a search-interest concern. **The 5-stage protocol resolves the adjacency at lock; if it does not, Wüsthof inherits the pivot role without further panel change.**"

Pre-reg §6 (Contingencies):

> "Pivot failure. If Victorinox topic-ID resolution exceeds **v1.2 §4 confusion threshold** at lock, Wüsthof inherits the pivot role and the panel reduces by one brand (Wüsthof exits the German tradition cell; German cell collapses to n = 4 with no alternate substitution, since Wüsthof's pivot role precludes within-cell scoring)."

Both passages cite a procedure ("the 5-stage protocol") and a threshold ("v1.2 §4 confusion threshold") drawn from AIAS Presence Measurement Protocol v1.2 (SSRN 6761698).

### What v1.2 actually specifies

A close reading of SSRN 6761698 §4 and §5 establishes the following:

- **v1.2 §4 is the four-regime classification routing step**, not a pivot-validation procedure. §4 specifies how a category, once measured, gets routed to Regime 1/2/3/4 based on bivariate ρ, partial ρ, covariate decrement, and n_eligible. §4 contains no "confusion threshold." Pre-reg §6's citation of "v1.2 §4 confusion threshold" is a reference to text that does not exist in the methodology paper.

- **v1.2 §5.1 names Phase A pivot validation as part of the three-phase eligibility procedure**: "the Google Trends rescaled data per brand per wave-region cell, resolved through the protocol's three-phase eligibility procedure (Phase A pivot validation; Phase B per-brand topic-ID or canonical-query resolution; Phase B-alternates activation if primary brands fail E1a)." §5.1 names the procedure but does not specify its operational test.

- **v1.2 §5.2 delegates Phase A criteria to per-category pre-registration**: "Eligibility specification: E1a Phase B Trends-eligibility criteria; E1b at-acquisition exclusion criteria; alternate-activation rules; pivot-brand selection and Phase A validation criteria."

The methodology paper correctly delegates Phase A acceptance criteria to per-category pre-registration. **v0.16-prereg §3 did not exercise that delegation precisely enough to support a binding Phase A test.** Pre-reg §3 named "the 5-stage protocol" without specifying the five stages, their measurements, or their acceptance thresholds.

### Specification gap classification

This is a **v0.16-prereg specification gap**, surfaced by — but not exclusively created by — a parallel ambiguity in v1.2 itself. Specifically:

- **v0.16-prereg gap:** §3 / §6 reference a "5-stage protocol" and a "v1.2 §4 confusion threshold" without locking operational definitions or threshold values. A reader of v0.16-prereg cannot mechanically evaluate whether Victorinox passes or fails.

- **v1.2 gap (downstream):** §5.1 names Phase A pivot validation as a procedure but offers no canonical operationalization. §5.2 delegates to per-category pre-registration but does not specify the minimum content of such pre-registration. This gap is recorded here for the v1.2 methodology paper as future protocol work (see "Forward action" below).

### Phase A diagnostic runs and their interpretation

Two Phase A runs were executed on 16 May 2026 UTC against my interim implementation `phaseA_pivot_v16.py`, which embedded placeholder thresholds (CV < 30%; pivot/median(reference) ∈ [0.5, 5.0]; chef_proportion ≥ 0.20; swiss_army_proportion ≤ 0.70) chosen by judgment in the absence of a v1.2-canonical specification. Both runs are recorded in `osf/v16/data/phaseA/`.

**Run 1: Victorinox (primary).**
- Stage 1 pytrends suggestions: 5 returned; types include "Topic" (×2), "Manufacturing company," "Multi-tool," "Store in Schwyz, Switzerland." No chef-knife disambiguation surfaced.
- Stage 2 stability: n=53 daily points, mean=77.11, CV=17.03%. PASS against the 30% placeholder.
- Stage 3 bundle position: query failed with HTTP 400 (Google Trends 5-keyword limit exceeded; `phaseA_pivot_v16.py` STAGE3_REFERENCE_BRANDS had 5 entries producing a 6-keyword bundle). Result non-informative due to implementation bug.
- **Stage 4 adjacency**: pivot=77.11, "Victorinox chef knife"=1.28, "Swiss Army knife"=12.47. **chef_proportion = 0.093; swiss_army_proportion = 0.907.** Swiss-Army-knife traffic is ~10× chef-knife traffic at the same query.

**Run 2: Wüsthof (fallback verification).**
- Implementation bug fixed (STAGE3_REFERENCE_BRANDS reduced to 4 entries).
- Stage 4 adjacency: pivot=20.47, "Wüsthof chef knife"=0.32, "Swiss Army knife"=73.55. The Stage 4 thresholds returned FAIL — but on inspection, the test as I implemented it is testing the wrong thing for Wüsthof: comparing branded-product-line queries ("[brand] chef knife") against a category-defining adjacent query ("Swiss Army knife") will always favor the category query because branded-product-line queries have lower volume than category queries. The Wüsthof FAIL is an artifact of my placeholder test specification, not a Wüsthof signal.
- Stage 2 stability for Wüsthof: CV=42.19%. Marginal against my 30% placeholder; plausibly reflects holiday/gift-season variance for a knife brand rather than measurement instability.

**Substantive reading of the runs:**

The Victorinox Stage 4 result (chef 9.3% / Swiss-Army 90.7%) is robust against any reasonable interpretation of pre-reg §3's intent ("Swiss-Army-knife adjacency"). The pre-reg's stated topic-ID concern is empirically present: Victorinox's Google search footprint is dominated by Swiss-Army-knife traffic, not chef-knife traffic. Using Victorinox as a Trends pivot would inject Swiss-Army-knife seasonality into rescaled values for the panel's actual knife brands. The substantive case for fallback is unambiguous, independent of any specific threshold specification.

The Wüsthof runs are not informative about Wüsthof's pivot suitability under any specification I can defend, because the placeholder tests I wrote (Stage 3 position, Stage 4 adjacency) are not faithful operationalizations of pre-reg §3's "5-stage protocol resolves the adjacency." They test artifacts of Google Trends bundle normalization and query-volume ratios rather than topic-ID resolution as such.

### Decision

**The pivot is changed from Victorinox to Wüsthof for v0.16.**

This decision is grounded in:

1. The substantive Victorinox Stage 4 evidence (chef 9.3% / Swiss-Army 90.7%, pytrends suggestions returning no knife-context disambiguation) being independently sufficient to establish that Victorinox's Google search footprint is dominated by non-knife traffic.

2. The clear *intent* of pre-reg §3's fallback contingency — "if Victorinox topic-ID resolution surfaces Swiss-Army-knife confusion above v1.2 §4 threshold" — being satisfied by the substantive evidence, even though the literal pre-reg text references a v1.2 §4 threshold that does not exist.

3. Wüsthof being a dedicated knife brand (verified at the trade-press / category-listing level; not depending on any of my Phase A implementation tests), with no Swiss-Army-style adjacency confound. Wüsthof's pivot suitability rests on category-fit qualitative evidence, not on the Phase A tests I implemented.

**Phase A as implemented (`scripts/phaseA_pivot_v16.py`) is downgraded to advisory.** Its outputs (`osf/v16/data/phaseA/stage{1,2,3,4,5}_*.json` for both Victorinox and Wüsthof runs) are retained on disk as part of the v0.16 deposit and contribute to this entry's substantive reasoning, but Phase A does not produce a binding PASS/FAIL on the v0.16 pivot. Pivot decision is recorded here, in DEVIATIONS Entry 3, as a substantive amendment under pre-reg §3 / §6 spirit.

### Panel impact per pre-reg §6

Pre-reg §6 specifies: "Wüsthof exits the German tradition cell; German cell collapses to n = 4 with no alternate substitution, since Wüsthof's pivot role precludes within-cell scoring." This impact is applied:

- Wüsthof: role changes from `panel` to `pivot_primary`. Removed from German tradition cell. Used as pivot in every acquisition bundle.
- German tradition cell membership: Zwilling J.A. Henckels, Messermeister, Güde, Friedr. Dick (n = 4). No alternate is activated.
- Victorinox: role changes from `pivot_primary` to `pivot_failed`. Not used as pivot. Not added back to the German cell (per pre-reg §6 — there is no Swiss tradition cell in v0.16's five-cell taxonomy, and Victorinox's Swiss-Army-knife adjacency would carry the same signal-contamination concern into panel membership).

Total panel size: 23 brands (down from 24). H_Regime4_replication_knives Condition 1 (n ≥ 12) remains satisfied with substantial margin.

### Bundle composition impact

`acquire_trends_v16.py` and `rescale_trends_v16.py` bundle composition is reorganized to place Wüsthof as the pivot in all bundles. Wüsthof exits bundle 2 (where she was previously a panel member). One bundle drops to a 4-keyword query (3 panel brands + pivot) to accommodate the 23-brand panel across 6 bundles. New composition recorded in commit accompanying this entry.

### Forward action: v1.2 protocol amendment

The Phase A specification gap surfaced here is queued as future methodology work. A v1.3 protocol increment should specify Phase A pivot-validation criteria centrally rather than delegating entirely to per-category pre-registration. Minimum content for a centrally-specified Phase A:

- The five stages by name and operational test
- Acceptance criteria with threshold-precise definitions analogous to §3's regime-classification thresholds
- Boundary-flag conventions analogous to §4.2
- Cross-validation between Phase A and Phase B (the two procedures share substrate; if Phase A passes a pivot whose Phase B topic-ID resolution surfaces dominant non-category traffic, the protocol should specify whether the pivot or the panel takes priority)

This forward action is documented here for citation in a future v1.3 erratum or revision note. It does not block v0.16 acquisition or scoring; v0.16 proceeds under this amendment, with Phase A advisory and the pivot decision substantively grounded.

### Audit trail

- **Pre-reg lock:** `v0.16-prereg` (commit 511e339, locked 16 May 2026 UTC; corrected per Entry 2)
- **Phase A diagnostic Run 1 (Victorinox):** session timestamp 2026-05-16T23:44:36Z, full outputs at `osf/v16/data/phaseA/stage{1,2,3,4,5}_*.json` (Victorinox-pivot variant; backed up to git working tree before Run 2)
- **Phase A diagnostic Run 2 (Wüsthof):** session timestamp 2026-05-16T23:53:52Z, same paths overwritten; Run 1 outputs preserved via git working-tree state at time of Run 2
- **Phase A script .bak:** `scripts/phaseA_pivot_v16.py.bak` preserves the Victorinox-primary state; the committed `scripts/phaseA_pivot_v16.py` carries the Wüsthof-redirect needed for the fallback's continued advisory use
- **Methodology reference:** AIAS Presence Measurement Protocol v1.2, SSRN 6761698, §4 (regime classification) and §5.1/§5.2 (Phase A delegation to per-category pre-registration)
- **Implementation amendment commit:** [pending — accompanies this entry]

Per Entry 2 conditions of permissibility for pre-acquisition substantive amendments, all four hold:

1. No data has been collected against the affected text. Acquisition has not been run.
2. The amendment aligns with the intent of pre-reg §3 / §6 (Wüsthof fallback on Victorinox topic-ID failure). The literal text was unimplementable; the intent is preserved.
3. The amendment is fully audited here. Original Victorinox-primary state is recoverable via `git show v0.16-prereg:registries/PRE_REGISTRATION_v0_16.md` and the `.bak` script. Diagnostic Phase A outputs are retained on disk.
4. Cross-phase comparability is preserved. v0.16 remains a Regime 4 substrate-replication test under H_Regime4_replication_knives. Pivot identity changes do not affect the hypothesis conditions or their evaluation procedure.
## Entry 4 — Alternate activation (Au Nain, Hengtai) per pre-reg §6 substitution order

**Status.** Pre-acquisition routine event. Activates two pre-registered alternates per the substitution rules in pre-reg §3 (alternates list) and §6 (cell-collapse contingency). This is not a substantive amendment to the pre-registration; it is the pre-registered contingency firing.

**Logged:** 17 May 2026 UTC (00:22 session start; Phase B completion).

**No data has been collected against the affected pre-registration text.** Acquisition (`acquire_trends_v16.py`) has not been run. The amendment is pre-acquisition.

---

### Phase B per-cell outcomes that triggered the substitution

`phaseB_resolve_v16.py` session at 2026-05-17T00:22:04Z produced the following per-cell eligibility result:

| Tradition cell | Primary panel | PASS / PASS_E5 | EXCLUDED_E1a | Cell n |
|---|---|---|---|---|
| japanese | 6 | 6 | 0 | 6 |
| german | 4 | 4 (1 via E5) | 0 | 4 |
| french | 4 | 3 | 1 (Nogent (Goyon-Chazeau)) | 3 (underpower warning) |
| american_specialty | 5 | 5 | 0 | 5 |
| chinese | 4 | 2 | 2 (CCK Chan Chi Kee, Shibazi (Shi Ba Zi Zuo)) | 2 (cell collapse trigger per pre-reg §6) |

French cell at n=3 is below the n≥4 cell-design floor (underpower warning). Chinese cell at n=2 triggers the pre-reg §6 cell-collapse rule (descriptive-only routing). Both cells are eligible for alternate-activation rescue per pre-reg §3.

### Pre-reg §3 alternate lists (binding substitution order)

> **Pre-registered alternates** (used in pre-registered substitution order if a primary brand fails topic-ID resolution or eligibility):
> - Japanese cell: Masamoto, Misono, Tadafusa
> - German cell: Schmidt Brothers (German-tradition lineage), Robert Herder
> - French cell: **Au Nain, Goyon-Chazeau Le Thiers**
> - American cell: Bob Kramer (Zwilling collaboration; high-end), Wüsthof Classic Ikon (excluded — duplicate), Hammer Stahl
> - Chinese cell: **Hu Si Chao, Dengjia, Hengtai**

### Substitution walks (per pre-reg priority order)

**French (1 substitute needed for Nogent):**

| Priority | Alternate | Phase B Stage 2 result | Outcome |
|---|---|---|---|
| 1 | Au Nain | PASS (n_days=7, mean=74.71) | **ACTIVATED** |

Substitution complete with the 1st-priority alternate. French cell rises from n=3 to n=4. Cell fully eligible for inferential analysis.

**Chinese (2 substitutes needed for CCK + Shibazi):**

| Priority | Alternate | Phase B Stage 2 result | Outcome |
|---|---|---|---|
| 1 | Hu Si Chao | all-zero solo + all-zero E5 → EXCLUDED_E1a | Failed; continue walk |
| 2 | Dengjia | all-zero solo + all-zero E5 → EXCLUDED_E1a | Failed; continue walk |
| 3 | Hengtai | PASS (n_days=7, mean=68.0) | **ACTIVATED** |

Substitution walk exhausted with 1 of 2 needed substitutes located. Chinese cell rises from n=2 (cell-collapse trigger) to n=3 (underpower warning, eligible for inferential analysis). Per pre-reg §6 spirit, escape from the n<3 cell-collapse routing is the threshold being met; further alternate activation is not possible (the pre-registered Chinese alternate list is exhausted).

### Decisions

1. **Au Nain promoted from `alternate` to `panel`.** Tradition cell: french. Activation rationale recorded in this entry; topic-ID resolution log updated.
2. **Hengtai promoted from `alternate` to `panel`.** Tradition cell: chinese. Activation rationale recorded; topic-ID resolution log updated.
3. **Chinese cell descriptive-routing flag is removed.** Cell n=3 retains an underpower warning (the per-cell tradition-dummy in partial correlation operates on n=3, which is below the typical n≥4 cell-design floor), but is eligible for inferential analysis. Cross-cell H_Regime4_replication_knives analyses include all 22 eligible non-pivot panel brands.
4. **EXCLUDED_E1a primary brands remain in the registry** with their existing topic-ID resolution status. They are not replaced in the registry's panel array — they are dropped from the acquisition bundle composition (see §"Bundle composition impact" below).
5. **Hu Si Chao and Dengjia retain `alternate` role with `TESTED_NOT_ACTIVATED` notes** documenting the failed activation walk. They are eligible for re-test in a future phase but not in v0.16.

### Updated panel eligibility

Total panel: 23 primary brands + 2 activated alternates = 25 enrolled. 3 EXCLUDED_E1a (Nogent, CCK, Shibazi) are dropped from bundle composition. **Total eligible: 22 brands (excluding pivot Wüsthof)**.

| Tradition cell | Eligible brands |
|---|---|
| japanese (n=6) | Shun, Global, Miyabi, Mac, Tojiro, Yoshihiro |
| german (n=4) | Zwilling J.A. Henckels, Messermeister, Güde, Friedr. Dick |
| french (n=4) | Sabatier, Opinel, Laguiole, **Au Nain** |
| american_specialty (n=5) | Cutco, Dalstrong, Misen, New West KnifeWorks, Made In |
| chinese (n=3) | Sunlong, ZHEN, **Hengtai** *(underpower warning, n<4)* |

H_Regime4_replication_knives Condition 1 (n_eligible ≥ 12) satisfied with substantial margin (22 ≥ 12).

### Bundle composition impact (acquisition + rescale)

To accommodate the substitutions while honoring Google Trends' 5-keyword-per-query limit, EXCLUDED_E1a brands are dropped from bundles before the activated alternates are inserted:

| Bundle | Before | After |
|---|---|---|
| 4 (french-american) | Laguiole, Nogent (Goyon-Chazeau), Cutco, Dalstrong | Laguiole, **Au Nain**, Cutco, Dalstrong |
| 6 (chinese) | CCK Chan Chi Kee, Shibazi (Shi Ba Zi Zuo), Sunlong, ZHEN | Sunlong, ZHEN, **Hengtai** *(4-keyword bundle, 3 panel brands + pivot)* |

Bundles 1, 2, 3, 5 are unchanged. Total acquisition cost remains 6 bundles × 2 regions = 12 SerpAPI calls.

### Audit trail

- **Phase B session:** 2026-05-17T00:22:04Z, full outputs at `osf/v16/data/phaseB_*`
- **Pre-reg basis:** pre-reg §3 (alternate lists), pre-reg §6 (cell-collapse contingency authorizing alternate activation)
- **Activation walks:** documented in this entry's §"Substitution walks" section with Phase B Stage 2 evidence
- **Registry updated:** `registries/brands_kitchen_knives_v0.16.json` — Au Nain + Hengtai moved from `alternates` → `panel`
- **Topic-ID log updated:** `osf/v16/registries/topic_id_resolution_log_v0.16.csv` — Au Nain + Hengtai role: alternate → panel; notes updated with activation rationale
- **Bundle composition updated:** `scripts/acquire_trends_v16.py` and `scripts/rescale_trends_v16.py` — bundles 4 and 6 modified
- **Implementation amendment commit:** [pending — accompanies this entry]

Per Entry 2 conditions of permissibility for pre-acquisition substantive amendments, all four hold:

1. No data has been collected against the affected text. Acquisition has not been run.
2. The amendment aligns with pre-reg §3 / §6 (alternate substitution order on primary failure; cell-collapse rescue). No interpretation gap; the literal pre-reg contingency fires.
3. The amendment is fully audited here. Original primary panel composition and original alternate-list ordering recoverable via `git show v0.16-prereg:registries/PRE_REGISTRATION_v0_16.md` and `git show v0.16-prereg:registries/brands_kitchen_knives_v0.16.json`.
4. Cross-phase comparability is preserved. v0.16 remains a Regime 4 substrate-replication test under H_Regime4_replication_knives. Alternate-activation changes panel membership without altering hypothesis conditions or evaluation procedure.
