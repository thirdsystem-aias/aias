# DEVIATIONS — v0.14 (premium tea, Regime 4 third datapoint)

Pre-registration: `v0.14-prereg` (commit b0ef30a, 2026-05-12)

This file logs post-lock operational deviations from the v0.14 pre-registration.
Each entry documents the observation, root cause, methodology amendment (if
any), pre-registration scope justification, audit-trail preservation, and
impact on hypothesis evaluation.

Per pre-reg §7: deviations do not modify pre-registered hypothesis tests.

---

## Entry 1 — Phase B v1 topic-ID resolution: bare canonical query methodology amendment

**Date raised:** 2026-05-12
**Status:** Resolved — Phase B v2 re-run with bare canonical queries
**Pre-reg sections referenced:** §2 (brand panel, Chinese-cell alternates), §6 (Methods — 5-stage topic-ID resolution protocol inheritance from v0.13)

### §1.1 Observation

Phase B v1 ran on 2026-05-12T13:08 UTC against the locked v0.14 brand panel
(22 premium tea brands). Outcome:

| Result tier | Count |
|---|---|
| Solo PASS | 9 |
| PASS_E5 (bundled rescue) | 1 |
| EXCLUDED_E1a | 12 |
| **Total eligible** | **10 / 22** |

Per-tradition breakdown:

| Tradition | Total | Eligible | Excluded |
|---|---|---|---|
| chinese | 4 | 2 | 2 (alternate activation triggered per pre-reg §2) |
| japanese | 4 | 2 | 2 |
| british | 5 | 2 | 3 |
| indian | 4 | 2 | 2 |
| us_specialty | 5 | 2 | 3 |

Total eligible (10) is below the n_eligible ≥ 12 threshold (H_Regime4_replication
condition 1). The pre-registered Chinese-cell alternate activation rule is
triggered. Maximum achievable eligible after activating all three alternates
(Wang De Chuan, In Pursuit of Tea, Yunnan Sourcing) is 13.

### §1.2 Root cause

Inspection of the Stage 1 pytrends-chosen suggestions reveals that the
category-keyword filter — `["tea", "brand", "beverage", "drink", "food",
"company", "specialty", "retail", "store"]` — accepted suggestions whose
type strings contained these keywords but whose underlying entities were
**not** brand-level entities.

Of the 9 solo PASS brands, only 4 had a clean brand-level chosen MID:
Twinings (canonical, forced via pivot logic), Ten Ren's Tea
("Food and beverage company"), Harney & Sons ("Company"), Ito En
("Drink company").

The other 5 PASSes had chosen MIDs pointing to wrong entities:

| Brand | Chosen MID title | Chosen MID type | Solo mean |
|---|---|---|---|
| Republic of Tea | Republic of Ireland national football team | Soccer team | 47.14 |
| Jing Tea | Longjing tea (Chinese tea variety) | Tea | 86.14 |
| Makaibari | Taj Chia Kutir Resort & Spa | Hotel in Makai Bari Tea Garden | 27.57 |
| Fortnum & Mason | The Diamond Jubilee Tea Salon at Fortnum & Mason | Tea house in London, England | 14.29 |
| Ippodo Tea | Ippodo Tea (Kyoto Since 1717) Sayaka — Rich Matcha (40g Can) | Tea | 63.86 |

These MIDs passed E1a because their underlying entities (a football team, a
tea variety, a hotel near the brand's plantation, a salon location, a
specific product) carry non-trivial Google Trends signal — but the signal is
not the brand's signal. The Republic of Tea case is the most severe: its
chosen MID matched the keyword "team" via a Knowledge Graph adjacency that
the keyword filter could not screen.

Of the 13 solo FAIL brands, similar pattern in the opposite direction:
chosen MIDs pointed to narrow product-variant entities or specific physical
locations that lacked Trends signal. Examples: "Vahdam, Organic Turmeric +
Ashwagandha Superfood Herbal Tea" for Vahdam Teas; "TWG Tea at ION Orchard"
for TWG Tea; "Marukyu Koyamaen Aoarashi, Ceremonial Grade Matcha, 40 Gram"
for Marukyu Koyamaen.

The root cause is structural: pytrends' suggestion ranking surfaces
product-variant and physical-location entities for tea brands ahead of the
brand entity itself. v0.13 (skincare/finance) did not encounter this failure
mode because skincare/finance product-variant MIDs (e.g., "CeraVe Cleanser
Hydrating") carry substantial Trends signal of their own — tea product
variants generally do not.

### §1.3 Methodology amendment

Switch Phase B Stage 2 `solo_query` and Stage 3 E5 pivot query from
pytrends-derived MIDs to **bare canonical brand names** for all brands. This
matches the treatment Twinings already received in v1 via the
`PIVOTS_CANONICAL` branch (which produced its clean Phase A PASS at
mean=88.14 with canonical query "Twinings").

Stage 1 pytrends.suggestions() continues to run unchanged, and its output
(suggestions list, chosen MID/title/type, rationale) is preserved as
audit trail in the suggestions JSON and the
`pytrends_chosen_{mid,title,type}` columns of the resolution log. Stage 2
no longer gates on it.

The bare-canonical approach trades pytrends' (failed) entity-disambiguation
attempt for the brand-name aggregate signal across all products and
locations. This is the conservative substitution given the v1 evidence.

### §1.4 Pre-registration scope justification

The pre-registration §6 Methods clause states "5-stage topic-ID resolution
protocol per brand (no methodological changes)" inheriting v0.13's protocol.
The amendment here is a **runtime adaptation to a category-specific failure
mode**, not a change to the underlying protocol:

- pytrends suggestions still run at Stage 1 (unchanged)
- E1a / E5 logic is unchanged (same PASS / PASS_E5 / EXCLUDED_E1a taxonomy)
- Out-of-sample window unchanged (2026-04-13 to 2026-04-19)
- Stratification and Chinese-cell alternate activation rule unchanged

What changes is the source of the `solo_query` candidate string at Stage 2.
This is the kind of discrete operational adaptation DEVIATIONS entries are
intended to capture.

H_Regime4_replication condition 1 (n_eligible ≥ 12) is **not** modified by
this amendment. If the v2 re-run produces n_eligible < 12, the Regime 4
classification is falsified per pre-reg — that outcome ships regardless.

### §1.5 Audit-trail preservation

All v1 outputs are preserved in v1-suffixed locations before v2 runs:

- `osf/v14/data/phaseB_suggestions/v1_pytrends_mid/` — retained at top level since suggestions don't change between v1 and v2 and the script reuses them as cache
- `osf/v14/data/phaseB_validation/solo/v1_pytrends_mid/` — 22 brand solo validation JSONs (moved; v2 wrote fresh files)
- `osf/v14/data/phaseB_validation/bundled/v1_pytrends_mid/` — 4 E5 bundle JSONs (moved)
- `osf/v14/registries/topic_id_resolution_log_v0.14_v1.csv` — original CSV (renamed)

Phase B v2 re-run wrote fresh outputs to the standard top-level locations.
The v2 CSV at `osf/v14/registries/topic_id_resolution_log_v0.14.csv` is the
canonical input to acquisition.

### §1.6 Impact on hypothesis evaluation

No pre-registered hypothesis status is modified by this deviation:

- H1–H4 per category, H2 cross-wave stability, H7 four-regime classification, H_Regime4_replication: thresholds, decision rules, and evaluation logic all unchanged.
- The amendment improves measurement validity by reducing topic-ID errors (e.g., Republic of Tea no longer measured against Irish football team Trends data) without altering pre-registered thresholds.

### §1.7 Outcome (v2 re-run, 2026-05-12T15:32 UTC)

| Result tier | Count |
|---|---|
| Solo PASS | 16 |
| PASS_E5 | 0 |
| EXCLUDED_E1a | 6 |
| **Total eligible (primary panel)** | **16 / 22** |

n_eligible = 16, comfortably above the 12 threshold (H_Regime4_replication
condition 1 satisfied for the pooled panel). Per-tradition breakdown:

| Tradition | Eligible | Excluded |
|---|---|---|
| chinese | 2 | 2 (alternate activation still triggers — see Entry 2) |
| japanese | 4 | 0 |
| british | 4 | 1 |
| indian | 1 | 3 |
| us_specialty | 5 | 0 |

Two operational flags noted for the eventual paper's limitations section:

- Tea Box solo mean of 88 is suspiciously high for a small Indian online retailer; bare canonical query may be matching generic "tea box / tea gift box" search phrases. Acceptable per pre-reg (brand registered as such); flag for limitations.
- Indian cell at 1 eligible falls below the 3-brand per-cell floor for regime call (pre-reg §1.5). Stratified robustness reports Indian as descriptive only.

---

## Entry 2 — Chinese-cell alternate activation outcome

**Date raised:** 2026-05-12
**Status:** Resolved — 1 of 3 alternates activated (Yunnan Sourcing); Chinese cell lands at 3 eligible
**Pre-reg sections referenced:** §2 (Chinese-cell alternate activation rule, pre-registered floor for per-cell regime call)

### §2.1 Trigger

Phase B v2 left the Chinese tradition cell at 2 eligible brands (TWG Tea,
Jing Tea) with 2 excluded (Ten Ren's Tea, TenFu's Tea — both failed solo
with SerpAPI `notEnoughSearchVolume`-equivalent error under bare canonical
query). Pre-reg §2 activation rule triggers at ≥ 2 Chinese-cell exclusions;
gap to fill = 2 brands (target 4 eligible).

### §2.2 Method

`phaseB_alternates_v14.py` ran on 2026-05-12T15:44 UTC, applying the same
DEVIATIONS Entry 1 methodology (bare canonical queries) used in the primary
Phase B v2 run. All three pre-registered alternates were tested in
activation order (A1 → A2 → A3) through Stage 1 (pytrends audit), Stage 2
(solo SerpAPI), and Stage 3 (E5 bundled rescue for solo failures).

### §2.3 Outcomes

| Order | Brand | Founded | Solo result | E5 result | Final tier | Activation status |
|---|---|---|---|---|---|---|
| A1 | Wang De Chuan | 1862 | FAIL_API | ALL_ZERO | EXCLUDED_E1a | Not activated (failed) |
| A2 | In Pursuit of Tea | 2002 | FAIL_API | ALL_ZERO | EXCLUDED_E1a | Not activated (failed) |
| A3 | Yunnan Sourcing | 2004 | PASS (mean=28.43) | — | PASS | **ACTIVATED** |

Yunnan Sourcing is the sole alternate to clear E1a. Wang De Chuan and In
Pursuit of Tea failed both solo and E5 bundled validation, mirroring the
pattern observed for primary Chinese-cell brands Ten Ren's Tea and TenFu's
Tea — Chinese-tradition brands with limited English-language Google Trends
signal even under bare canonical queries.

### §2.4 Final Chinese-cell eligibility

Primary eligible (2) + Activated alternate (1) = **3 eligible total** in
Chinese tradition cell. Target of 4 was not reachable (only 1 of 3
alternates was viable). The cell sits exactly at the pre-reg §1.5 per-cell
floor of 3, retaining eligibility for the stratified-by-tradition regime
call as a descriptive supplement.

### §2.5 Activation rule interpretation

Pre-reg §2 specifies activation "in order until the cell returns to four
eligible brands". Because only 1 of 3 alternates was viable, the cell could
not return to 4. All three alternates were nonetheless tested — A1 and A2
were necessary to reach A3 in pre-reg order, since the rule does not permit
skipping to the next alternate without first testing the preceding one.

There are no `TESTED_NOT_ACTIVATED` rows in the outcome (would have applied
only if an alternate passed but was not needed to fill the gap). All three
alternates' data is preserved in the canonical phaseB outputs.

### §2.6 Impact on hypothesis evaluation

- **Pooled panel n_eligible = 17** (16 primary PASS + 1 activated alternate). H_Regime4_replication condition 1 satisfied for the primary (pooled) analysis.
- **Per-tradition regime calls available**: Chinese (n=3), Japanese (n=4), British (n=4), US-specialty (n=5). Indian cell (n=1) is below floor and reported descriptive-only per pre-reg §1.5.
- **No pre-registered hypothesis modified.** The activation outcome is the documented operationalization of pre-reg §2; it changes the eligible panel composition but not the thresholds or decision rules.

### §2.7 Audit trail

- Three alternate brand suggestion JSONs at `osf/v14/data/phaseB_suggestions/{Wang_De_Chuan,In_Pursuit_of_Tea,Yunnan_Sourcing}.json`
- Three alternate solo validation JSONs at `osf/v14/data/phaseB_validation/solo/{Wang_De_Chuan,In_Pursuit_of_Tea,Yunnan_Sourcing}.json`
- E5 alternates bundle JSON at `osf/v14/data/phaseB_validation/bundled/premium_tea_e5_alternates.json`
- Three alternate rows appended to `osf/v14/registries/topic_id_resolution_log_v0.14.csv` with `notes` column flagging activation status

---
