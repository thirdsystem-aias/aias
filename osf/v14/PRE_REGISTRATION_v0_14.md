# AIAS Measurement Programme — v0.14 Pre-Registration

**Lock date:** 12 May 2026
**Acquisition target:** 13 May 2026
**Git tag:** `v0.14-prereg`
**Carry-forward base:** v0.13 (SSRN 6750498, git tag `v0.13-published`, commit `af16fbf`)
**Category:** premium tea

---

## 1. Strategic context

v0.14 pursues a third empirical datapoint for **Regime 4 (Covariate-saturated weak)**, the provisional fourth cell in the AIAS™ four-regime taxonomy named in v0.13. Regime 4 currently rests on two categories (skincare, finance). Formalizing a four-regime taxonomy in the AIAS methodology paper on two datapoints would undercut the pre-registration credibility the programme rests on; three datapoints is a defensible empirical floor.

**Selection rationale for premium tea:** highest-probability Regime 4 candidate in the queued pool, on four criteria — cross-lingual production traditions, high brand-age dispersion (~310 years), established English-language discourse, low consumer identity load relative to other queued categories.

**Falsification disposition:** if premium tea classifies into Regime 1, 2, or 3 instead, v0.14 reports the result as productive falsification and the methodology paper queue advances by one further phase. v0.14 ships the empirical result regardless of regime outcome.

---

## 2. Brand panel (locked)

22 brands, stratified across five production traditions. Listed with founding year. Edge-case classification rule: brands are assigned to the tradition cell reflecting their *production-tradition identity* (the heritage the brand markets), not legal incorporation or HQ geography.

### Chinese / Taiwanese tradition (4)
1. TWG Tea — 2008
2. Ten Ren's Tea / 天仁 — 1953
3. TenFu's Tea / 天福 — 1993
4. Jing Tea — 2004

### Japanese tradition (4)
5. Ippodo Tea — 1717
6. Marukyu Koyamaen — 1704
7. Lupicia — 1994
8. Ito En — 1966

### British tradition (5)
9. Twinings — 1706 *(pivot)*
10. Fortnum & Mason — 1707
11. Whittard of Chelsea — 1886
12. Tea Pigs — 2006
13. Postcard Teas — 2002

### Indian tradition (4)
14. Makaibari — 1859
15. Glenburn Tea Estate — 1859
16. Vahdam Teas — 2015
17. Tea Box — 2012

### US-specialty (5)
18. Harney & Sons — 1983
19. Rishi Tea — 1997
20. Numi Organic Tea — 1999
21. Smith Teamaker — 2009
22. Republic of Tea — 1992

### Pre-specified contingency: Chinese-cell alternates

The Chinese tradition cell has the highest expected topic-ID failure rate due to weaker English-language LLM training corpus representation. If two or more Chinese-cell primary brands fail topic-ID resolution, the following alternates are activated in order until the cell returns to four eligible brands:

- A1. Wang De Chuan / 王德傳 — 1862
- A2. In Pursuit of Tea — 2002
- A3. Yunnan Sourcing — 2004

Alternates are activated **only** by the rule above. No post-hoc swapping is permitted for any other cell. If the Chinese cell falls below three eligible brands even after alternate activation, it is reported descriptively only (no per-cell regime call); the pooled-panel primary analysis proceeds with the eligible brands.

---

## 3. Pivot

**Twinings (1706)** — selected on three criteria:
- Strongest simultaneous retail presence across all five tradition markets (British, US, Indian, East Asian, Chinese)
- Mainstream premium positioning (not boutique-niche, not mass-discount)
- Highest expected eligible response rate across LLM providers for pivot validation

Pivot validation follows v0.13 Phase A protocol against the out-of-sample window. If Twinings fails pivot validation, the locked fallback is **Fortnum & Mason (1707)** — same tradition cell, comparable global retail reach, comparable founding age.

---

## 4. Hypotheses

### Carried forward from v0.13

**H1–H4** per category — construct validity tests on premium tea.

**H2 cross-wave stability** — AI Presence stability across acquisition waves.

**H7 four-regime classification** — pre-registered taxonomy now includes Regime 4 (Covariate-saturated weak) as the provisional fourth cell. Premium tea classifies into one of {Regime 1, Regime 2, Regime 3, Regime 4} per the v0.13 decision rule, or surfaces a fifth pattern requiring new naming.

### New for v0.14

**H_Regime4_replication** — premium tea replicates the Regime 4 signature observed in skincare and finance in v0.13.

Conditions (all three must hold on the pooled panel for Regime 4 classification):

| # | Condition | Threshold |
|---|---|---|
| 1 | Eligible-after-topic-ID panel size | n_eligible ≥ 12 |
| 2 | Bivariate Spearman correlation | \|ρ(AI Presence, brand age)\| < 0.35 |
| 3 | Residual partial correlation after age + premium-tier controls | ρ_partial < 0 |

Threshold provenance: \|ρ\| < 0.35 follows the v0.13 Regime 3/4 boundary. n ≥ 12 is the minimum for stable partial correlation estimation. ρ_partial < 0 reflects the v0.13 Regime 4 signature (negative covariate-conditioned association).

**Falsification:** any single condition violated → premium tea does not classify as Regime 4. H7 classification rule then assigns Regime 1, 2, or 3 from the pooled panel statistics. A fifth distinct pattern not fitting Regimes 1–4 is reported as a new candidate regime, name TBD post-result.

### Retired

**H5/H6 cross-category integrators** — falsified at 1-of-4 in v0.13 (PM-software-specific). No new cross-category regularity candidate is tested in v0.14.

---

## 5. Stratified robustness

The pooled-panel regime classification is the **primary** regime call.

Stratified-by-tradition analysis is reported as a **descriptive supplement**, applying the same three H_Regime4_replication conditions per tradition cell. Cells with fewer than 3 eligible brands after topic-ID resolution are descriptive only — no per-cell regime call.

The stratified analysis is not part of the primary hypothesis test. It is reported regardless of outcome and serves as a robustness reference for the eventual methodology paper's treatment of within-category heterogeneity in Regime 4.

---

## 6. Methods (referenced from v0.13)

- 5-stage topic-ID resolution protocol per brand (no methodological changes)
- Single locked acquisition timestamp (SerpAPI session, 13 May 2026)
- Pivot-normalised brand-day matrices
- H1–H8 evaluation via `score_v14.py` (sibling to v0.13 scorer, no methodological changes)
- Charts: `build_charts_v14.py` → 4 PDFs in `osf/v14/figures/`
- Brand-format report: `build_report_v14.py` + `v14_premium_tea_content.py`
- SSRN paper: `build_paper_v14.py` (pandoc + xelatex, Carlito; UNICODE_SUBS dict per established convention)
- OSF deposit: README, MANIFEST, data, analysis, figures, reports, papers

No methodological changes from v0.13 in scoring, topic-ID protocols, or regime decision rules. Any required deviation is recorded in `DEVIATIONS.md` and does not modify pre-registered hypothesis tests.

---

## 7. Pre-registration discipline

- **No post-hoc brand swaps.** Brands failing topic-ID drop out without replacement, except for the pre-specified Chinese-cell alternates rule (§2).
- **No threshold changes** after lock. The three H_Regime4_replication conditions are fixed at this commit.
- **All outcomes reported.** Regardless of which regime premium tea classifies into, v0.14 ships the result and the paper is submitted to SSRN.
- **DEVIATIONS.md** records any post-lock operational observations. Deviations do not modify pre-registered hypothesis tests.
- **Cross-citation update** to v0.13 in the v0.14 paper; v0.13 paper is not retroactively edited.

---

## 8. Programme position

v0.14 sits on the AIAS 1.0 critical path:

1. Tri-System paper (v15/v16) — MSI working paper venue, JAR natural short-form next stop
2. **AIAS methodology paper (Regime 4 formalization)** — keystone next deliverable, queued behind v0.14
3. Phase 4 components beginning with Ranking
4. External brand-tracking validation

A confirmed v0.14 Regime 4 replication unblocks the methodology paper draft. A falsification advances the methodology paper queue by one further phase, and v0.14 ships the empirical finding regardless.

---

**Lock signature:** to be committed at git tag `v0.14-prereg`, 12 May 2026.
