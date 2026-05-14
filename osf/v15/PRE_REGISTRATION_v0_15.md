# AIAS Measurement Programme — v0.15 Pre-Registration

**Lock date:** [TBD — target before LLM acquisition]
**Acquisition target:** [TBD]
**Git tag:** `v0.15-prereg`
**Carry-forward base:** v0.14 (SSRN 6755621, git tag `v0.14-published`, commit `2f57c95`)
**Methodology base:** AIAS Presence Measurement Protocol v1.2 (SSRN 6761698)
**Category:** premium tea (registry expansion of v0.14)

---

## 1. Strategic context

v0.15 closes the registry coverage gap identified in v0.14 §3.6 and tests the v0.14 Regime 4 pure sub-type (4b) confirmation under panel expansion. Four high-mention brands surfaced in v0.14 LLM responses but absent from the v0.14 registry — Mariage Frères (144 mentions), Palais des Thés (82), White2Tea (83), and Rare Tea Company (74) — would have ranked at or near the top of AI Presence at the v0.14 wave-2 totals if included. Their absence reflected the timing of v0.14's registry construction (locked before mention frequencies were observed), not a methodological choice. v0.15 incorporates them as the central expansion plus two additional French luxury heritage brands (Kusmi Tea, Dammann Frères) selected to give the new french tradition cell stratified analytical depth.

**Selection rationale for premium tea expansion (vs. a fresh Regime 4 candidate category).** Premium tea is the AIAS programme's deepest 4b empirical foundation: v0.14 was the cleanest Regime 4 case to date, with bivariate ρ already negative at both waves and a near-zero covariate decrement (≈ 0.02). Expanding the panel directly tests whether the regime classification is robust to a substantively wider eligible brand set, which is the primary registry-coverage falsification path identified in v0.14 §6.5. A fresh Regime 4 candidate category (single-malt whisky, specialty coffee, traditional spirits) would generalise the taxonomy across categories but would not address the registry coverage gap specifically. v0.15 prioritises the panel-robustness test; cross-category 4b generalisation is queued for v0.16 or later.

**Selection rationale for the expansion brands.** The four named brands — Mariage Frères, Palais des Thés, White2Tea, and Rare Tea Company — are non-registry mentions surfaced in v0.14's matched-model LLM responses with mention counts above 70 (per v0.14 §3.6), indicating they are part of the category's LLM training-corpus footprint. They span both existing tradition cells (Rare Tea Company in british; White2Tea in chinese) and a new tradition cell (Mariage Frères and Palais des Thés both in french, a tradition not represented in the v0.14 panel). The two additional brands — Kusmi Tea (1867) and Dammann Frères (1925) — are selected to bring the new french cell to four brands, clearing the §5 three-brand threshold for per-cell regime calls and giving the cell stratified analytical depth comparable to other cells. The v0.14 non-registry mention log was a transient analysis output not preserved in the v0.14 OSF deposit; Kusmi and Dammann Frères are well-established French luxury heritage houses whose LLM training-corpus presence is empirically expected to be substantial. Their inclusion is documented in §7 as a methodologically transparent selection on stratified-analysis utility, distinct from but consistent with the four named brands' mention-count provenance.

**Falsification disposition.** If the expanded panel falls out of Regime 4 classification (any single H_Regime4_robustness condition violated), the registry coverage gap is methodologically material — registry composition can shift regime classification at the threshold level — and the result is reported as a productive falsification of v0.14's verdict robustness. If the expanded panel re-confirms Regime 4 under the canonical operational test, v0.14's verdict is registry-robust and the 4b pure sub-type confirmation is hardened on a wider panel. v0.15 ships the empirical result regardless of regime outcome.

---

## 2. Brand panel (locked)

28 brands (22 carried forward from v0.14 + 6 new), stratified across six production traditions. Edge-case classification rule (carried forward from v0.14): brands are assigned to the tradition cell reflecting their *production-tradition identity* (the heritage the brand markets), not legal incorporation or HQ geography.

### Chinese / Taiwanese tradition (5: 4 carried + 1 new)
1. TWG Tea — 2008
2. Ten Ren's Tea / 天仁 — 1953
3. TenFu's Tea / 天福 — 1993
4. Jing Tea — 2004
5. **White2Tea — 2013** *(new at v0.15; Yunnan pu'er specialty, online-direct)*

### Japanese tradition (4)
6. Ippodo Tea — 1717
7. Marukyu Koyamaen — 1704
8. Lupicia — 1994
9. Ito En — 1966

### British tradition (6: 5 carried + 1 new)
10. Twinings — 1706 *(pivot)*
11. Fortnum & Mason — 1707
12. Whittard of Chelsea — 1886
13. Tea Pigs — 2006
14. Postcard Teas — 2002
15. **Rare Tea Company — 2004** *(new at v0.15; British specialty, single-estate sourcing)*

### Indian tradition (4)
16. Makaibari — 1859
17. Glenburn Tea Estate — 1859
18. Vahdam Teas — 2015
19. Tea Box — 2012

### US-specialty tradition (5)
20. Harney & Sons — 1983
21. Rishi Tea — 1997
22. Numi Organic Tea — 1999
23. Smith Teamaker — 2009
24. Republic of Tea — 1992

### French tradition (4: new cell at v0.15)
25. **Mariage Frères — 1854** *(French luxury tea house, Paris)*
26. **Palais des Thés — 1986** *(French specialty, multi-region sourcing)*
27. **Kusmi Tea — 1867** *(French luxury specialty, Russian heritage → Paris 1917)*
28. **Dammann Frères — 1925** *(French luxury heritage, Maison Dammann lineage)*

### Pre-specified contingency: alternates

The v0.14 Chinese-cell alternates rule carries forward unchanged. No alternates are specified for any other cell at v0.15.

**Chinese-cell alternates (carried forward from v0.14, activation rules unchanged):**

- A1. Wang De Chuan / 王德傳 — 1862
- A2. In Pursuit of Tea — 2002
- A3. Yunnan Sourcing — 2004

Alternates are activated **only** by the Chinese-cell rule from v0.14 §2 (two or more primary Chinese-cell brands failing topic-ID). No post-hoc swapping is permitted for any other cell. If any tradition cell falls below three eligible brands after topic-ID resolution (even after Chinese-cell alternate activation), it is reported descriptively only per §5.

---

## 3. Pivot

**Twinings (1706)** — carried forward unchanged from v0.14. Selection criteria, pivot validation procedure, and locked fallback (Fortnum & Mason, 1707) all carry forward unchanged.

---

## 4. Hypotheses

### Carried forward from v0.14

**H1–H4** per category — construct validity tests on premium tea, evaluated on the v0.15 expanded panel.

**H2 cross-wave stability** — AI Presence stability across acquisition waves, on the v0.15 expanded panel.

**H7 four-regime classification** — pre-registered taxonomy is now the canonical four-regime structure of the AIAS Presence Measurement Protocol v1.2 (González Castro 2026m, SSRN 6761698). Premium tea expanded panel classifies into one of {Regime 1, Regime 2, Regime 3, Regime 4} per the v1.2 routing logic, or surfaces an Unassigned outcome under §4.1 step 5 of the protocol.

### New for v0.15

**H_Regime4_robustness** — premium tea's v0.14 Regime 4 (4b pure sub-type) classification is robust to the v0.15 registry expansion. The expanded panel satisfies the canonical Regime 4 condition logic specified in the AIAS Presence Measurement Protocol v1.2 §3.4.

Conditions (all three must hold on the pooled panel for Regime 4 classification):

| # | Condition | Threshold |
|---|---|---|
| 1 | Eligible-after-topic-ID panel size | n_eligible ≥ 12 |
| 2 | Bivariate Spearman correlation | \|ρ(AI Presence, Trends)\| < 0.35 |
| 3 | Residual partial correlation after age + tradition controls | ρ_partial < 0 |

Threshold provenance: \|ρ\| < 0.35 and ρ_partial < 0 are the canonical Regime 4 thresholds from AIAS Protocol v1.2 §3.4. n ≥ 12 is the universal hypothesis-evaluation floor.

**Wording fix from v0.14.** v0.14 pre-reg §4 specified condition 2 as `|ρ(AI Presence, brand age)| < 0.35`; the v0.14 paper §3.3 resolved the wording mismatch with the v0.13 framework and adopted `ρ(AI Presence, Trends)` going forward. v0.15 specifies `ρ(AI Presence, Trends)` directly, matching the methodology paper's canonical definition.

**Covariate control specification.** The partial correlation uses age (continuous years since founding) and tradition (six-level categorical: chinese, japanese, british, indian, us_specialty, french) as controls. v0.14 used age + premium-tier (three-level ordinal). The shift to tradition reflects the registry's stratification logic; tradition is the variable that the v0.14 paper §2.1 described as the registry's "premium-tier dimension" in operational substance. The partial-correlation computation treats tradition as a set of dummy variables in the rank-residual approach, with degrees-of-freedom correction k = 6 (one per dummy minus one reference).

**Falsification.** Any single condition violated → premium tea expanded panel does not classify as Regime 4 under v1.2. H7 classification rule then assigns Regime 1, 2, 3, or Unassigned from the pooled panel statistics. A regime shift from v0.14's Regime 4 verdict to a different regime on the expanded panel is reported as productive falsification of registry-coverage robustness.

**H_Coverage_Closure** — the v0.15 registry expansion materially shifts the within-category AI Presence ranking distribution relative to v0.14's panel.

Conditions:

| # | Condition | Threshold |
|---|---|---|
| 1 | Sample size of overlap brands (in both v0.14 and v0.15 eligible panels) | n_overlap ≥ 10 |
| 2 | Spearman rank correlation of AI Presence share on overlap brands, v0.14 vs v0.15 | ρ_overlap < 0.85 (material shift) |

Conditions evaluated independently of H_Regime4_robustness. A pre-registered ρ_overlap < 0.85 indicates that the new brands' inclusion measurably reshapes the AI Presence distribution among existing brands (e.g., by absorbing share that was previously distributed across registry brands), which would confirm that the v0.14 §3.6 registry coverage gap was substantively material. ρ_overlap ≥ 0.85 indicates that the new brands' addition leaves existing-brand rank structure largely intact, suggesting that AI Presence share is allocated to new brands without materially redistributing among existing ones.

H_Coverage_Closure is exploratory at v0.15 and does not have a pre-registered falsification disposition.

### Retired (already retired at v0.14, confirmed retired at v0.15)

**H5/H6 cross-category integrators** — falsified at 1-of-4 in v0.13 (PM-software-specific). No new cross-category regularity candidate is tested in v0.15.

---

## 5. Stratified robustness

The pooled-panel regime classification is the **primary** regime call.

Stratified-by-tradition analysis is reported as a **descriptive supplement**, applying the same three H_Regime4_robustness conditions per tradition cell across six cells (the v0.14 five-cell stratification plus the new french cell). Cells with fewer than 3 eligible brands after topic-ID resolution are descriptive only — no per-cell regime call. The french cell enters v0.15 with 4 primary brands, clearing the 3-brand threshold by construction.

The stratified analysis is not part of the primary hypothesis test. It is reported regardless of outcome and serves as a robustness reference for within-category heterogeneity in Regime 4. v0.15 supplements the v0.14 stratified output by adding the french-cell data and by re-running the five v0.14 cells with the new brands added where applicable (chinese: +White2Tea; british: +Rare Tea Company).

---

## 6. Methods (referenced from v0.14)

- 5-stage topic-ID resolution protocol per brand, no methodological changes from v0.14.
- Single locked acquisition timestamp (SerpAPI session, [TBD]).
- Pivot-normalised brand-day matrices.
- Hypothesis evaluation via `score_v15.py` (sibling to `score_v14.py`, no methodological changes; partial-correlation covariate set updated to age + tradition per §4 above).
- Charts: `build_charts_v15.py` → PDFs in `osf/v15/figures/`.
- Brand-format report: `build_report_v15.py` + `v15_premium_tea_content.py`.
- SSRN paper: `build_paper_v15.py` (pandoc + xelatex, Carlito; UNICODE_SUBS dict per established convention).
- OSF deposit: README, MANIFEST, data, analysis, figures, reports, papers, registries (with extended `brand_age_sources_v0.15.csv`).
- Prompts: `prompts/prompts_premium_tea.json` carried forward unchanged from v0.14 (same category = same decision-context prompts).

No methodological changes from v0.14 in scoring, topic-ID protocols, or regime decision rules. The covariate-control variable shift from premium-tier to tradition is a stratification alignment (the registry stratifies by tradition; partial correlation now uses the same variable), not a regime-definition change. Any required deviation is recorded in `DEVIATIONS.md` and does not modify pre-registered hypothesis tests.

---

## 7. Pre-registration discipline

- **No post-hoc brand swaps.** Brands failing topic-ID drop out without replacement, except for the pre-specified Chinese-cell alternates rule (§2). No alternates are specified for any other cell.
- **No threshold changes** after lock. The three H_Regime4_robustness conditions and the two H_Coverage_Closure conditions are fixed at this commit.
- **All outcomes reported.** Regardless of which regime the expanded panel classifies into, and regardless of H_Coverage_Closure outcome, v0.15 ships the result and the paper is submitted to SSRN.
- **DEVIATIONS.md** records any post-lock operational observations. Deviations do not modify pre-registered hypothesis tests.
- **Cross-citation update** to v0.14 and the AIAS Presence Measurement Protocol v1.2 (methodology paper, SSRN 6761698) in the v0.15 paper; v0.14 paper is not retroactively edited.
- **Registry-expansion transparency.** The v0.15 brand additions are documented in §2 with mention-count provenance for the four named brands from v0.14 §3.6. The two additional brands (Kusmi Tea, Dammann Frères) are selected on stratified-analysis utility (closing the french cell to four brands for per-cell regime eligibility), with the methodological tradeoff acknowledged at §1: the v0.14 non-registry mention log was not preserved in the OSF deposit, so the two additional brands are selected on substantive grounds rather than exact mention-count provenance, while remaining empirically defensible as well-established French luxury heritage houses.

---

## 8. Programme position

v0.15 sits in Phase 4 of the AIAS measurement programme, post-methodology paper:

1. ~~Tri-System paper (v15/v16) — MSI working paper venue~~ — separate track, cross-citation update queued for next Tri-System revision.
2. ~~AIAS methodology paper (Regime 4 formalization)~~ — **shipped 13 May 2026** as the AIAS Presence Measurement Protocol v1.2 (SSRN 6761698).
3. **v0.15 (this pre-registration)** — registry coverage closure + 4b sub-type robustness test.
4. v0.16+ — Phase 4 candidates: cross-category 4b generalisation (single-malt whisky, specialty coffee, traditional spirits); additional 4a confirmations (consumer electronics, fast food, big-pharma OTC); or initiating Phase 4 work on the five remaining AIAS components (Ranking, Consistency, Coverage, Grounding, Sentiment) per methodology paper §7.3.
5. External brand-tracking validation (Kantar BrandZ, YouGov BrandIndex) — queued post-Phase-4-components.

A confirmed v0.15 H_Regime4_robustness positions the v0.14 4b sub-type confirmation as registry-robust and supports the AIAS Protocol v1.2 four-regime taxonomy under the canonical operational test. A falsification advances the methodology paper's §6.5 limitation (substrate readings as post-hoc interpretations) by demonstrating that the Regime 4 condition signature is sensitive to registry composition at the threshold level — also a programme-material finding.

The H_Coverage_Closure outcome is independently informative for protocol design: ρ_overlap < 0.85 supports an explicit registry-coverage step in the AIAS Presence Measurement Protocol v1.3 (drift mitigation), whereas ρ_overlap ≥ 0.85 supports the protocol's existing eligibility rules as sufficient.

---

**Lock signature:** to be committed at git tag `v0.15-prereg`, [TBD] 2026.
