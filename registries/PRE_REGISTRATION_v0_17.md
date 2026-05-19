# AIAS™ Presence Measurement Protocol — Pre-Registration v0.17

**Substrate:** Premium kitchenware (cookware)
**Programme position:** Identity-load moderator test; single-substrate same-IL replication of v0.16 knives PARTIAL
**Protocol version:** Methodology v1.2 (SSRN 6761698; canonical four-regime taxonomy per §6) + v1.3 (SSRN 6797679; Phase A pivot validation per §6.4)
**Lock target:** git tag `v0.17-prereg` at commit prior to LLM acquisition
**Pre-registrant:** Pablo Ulpiano González Castro

---

## §1 Strategic context

v0.16 (kitchen knives; SSRN 6791999) returned `H_Regime4_replication_knives` PARTIAL: worldwide bivariate ρ within the C2 band (|ρ| < 0.35) but partial ρ after age+tradition controls positive (+0.101/+0.080), failing C3. The verdict surfaced a productive boundary finding rather than a fourth-substrate canonical confirmation of Regime 4. The candidate explanation that emerged — and now requires explicit pre-registered testing — is that **Identity Load moderates the rate at which a category reweights toward AI Availability under Conditional Reweighting**.

The Regime 4 cluster established to date (skincare, finance, premium tea) is low-Identity-Load: the selection process is separable from the product, and AI-mediated retrieval substitutes cleanly for human deliberation. Knives sit at medium Identity Load: the selection process carries craft signal, tradition affiliation, and (for a subset of buyers) ritual weight that the AI intermediary cannot fully discharge. The PARTIAL verdict at knives is consistent with the prediction that medium-IL substrates exhibit weak-signature Regime 4 patterns rather than saturated ones — but a single observation does not establish a moderator.

v0.17 tests whether the v0.16 PARTIAL is **knives-specific** (idiosyncratic to the substrate) or **Identity-Load-class** (a structural feature of medium-IL categories). The substrate selected is **premium kitchenware** — held constant on Identity Load at the medium tier (cookware shares the craft-signal and tradition-affiliation features of knives), varied on substrate (different brand panel, different tradition-cell mix, different functional category). The design is a same-IL replication intended to isolate the Identity-Load moderator from substrate idiosyncrasy.

Two alternative substrates were considered and parked for later phases. Specialty coffee (low-to-medium Identity Load) was projected to confirm Regime 4 canonically; it extends the Regime 4 cluster without advancing the moderator question and is held for v0.19 or later as a Regime 4 thickness check. Indie fragrance (high Identity Load) is the natural upper-bound test of the moderator hypothesis and is pre-positioned for v0.18 conditional on v0.17's read.

The programme arc this phase advances:

| Phase | Substrate | Identity Load tier | Function |
|---|---|---|---|
| v0.14–v0.15 | Premium tea | Low | Regime 4 confirmation |
| v0.16 | Kitchen knives | Medium | PARTIAL (single observation) |
| **v0.17** | **Premium kitchenware** | **Medium** | **Same-IL replication; moderator candidate test** |
| v0.18 (projected) | Indie fragrance | High | Upper-bound test |

A PARTIAL verdict on kitchenware would constitute the second medium-IL observation and establish Identity Load as a credible moderator candidate warranting v0.18's upper-bound test. A CONFIRMED or FALSIFIED verdict on kitchenware would weaken the Identity-Load story by demonstrating substrate-level variance within the medium-IL tier; the moderator hypothesis would lose its claim on the v0.16 PARTIAL and that verdict would revert to substrate idiosyncrasy.

---

## §2 Pre-registered hypotheses

### §2.1 Primary: `H_Regime4_kitchenware`

**Statement.** Premium kitchenware, classified per Protocol v1.2 §6 canonical four-regime taxonomy, lands in Regime 4 (AI-mediated substitution for cognitive labour; weak Trends signature; brand-asymmetric AIAS Presence).

**Decision rules** (locked from v0.16):

- **C1 — Panel adequacy:** worldwide n ≥ 12 brands surviving the 14-day Trends floor and Phase A pivot validation.
- **C2 — Bivariate band:** worldwide |ρ(AIAS Presence, Trends)| < 0.35 at both t1 and t2.
- **C3 — Partial sign:** worldwide partial ρ(AIAS Presence, Trends | age, tradition) < 0 at both t1 and t2.

**Verdict tiers:**

- **CONFIRMED:** C1 ∧ C2 ∧ C3
- **PARTIAL:** C1 ∧ C2 ∧ ¬C3 (positive partial after controls; weak-signature boundary case)
- **FALSIFIED:** ¬C1 ∨ ¬C2

### §2.2 Secondary: `H_IdentityLoad_moderator`

**Statement.** The PARTIAL verdict observed at v0.16 (kitchen knives, medium Identity Load) reflects an Identity-Load class property of Regime 4 dynamics rather than a substrate-idiosyncratic feature of the knives category.

**Conditional decision rule** (resolves mechanically from the joint v0.16 / v0.17 verdict matrix):

| v0.16 (knives) | v0.17 (kitchenware) | Verdict on `H_IdentityLoad_moderator` |
|---|---|---|
| PARTIAL | PARTIAL | **SUPPORTED** — second medium-IL observation; Identity Load advanced as moderator candidate for v0.18 |
| PARTIAL | CONFIRMED | **WEAKENED** — kitchenware Regime 4 canonical; knives PARTIAL reverts to substrate idiosyncrasy |
| PARTIAL | FALSIFIED | **AMBIGUOUS** — kitchenware fails C1 or C2; `H_IdentityLoad_moderator` inconclusive pending v0.18 indie fragrance |

A SUPPORTED verdict on `H_IdentityLoad_moderator` is **not** evidence that Identity Load is the operative moderator — only that the substrate-idiosyncrasy alternative is weakened by a second medium-IL observation. Establishing Identity Load as the moderator requires the upper-bound test pre-positioned for v0.18.

### §2.3 Pre-registered descriptive sensitivities

Two descriptive sensitivities are pre-registered ahead of acquisition. Neither carries a hypothesis verdict; both are reported as standard sections in the published findings.

**§2.3.1 US-vs-worldwide divergence.** Per the v0.16 SECOND APERTURE finding (US/worldwide divergence on knives: worldwide ρ = +0.022 vs US ρ = −0.881), the kitchenware substrate is expected to surface similar registry-coverage asymmetry. European cookware (Le Creuset, Staub, Mauviel, Demeyere) and any Japanese cell members may drop from US-eligibility at the 14-day Trends floor. Worldwide and US sub-panels are reported separately as descriptive sensitivities; only the worldwide panel resolves the primary hypothesis decision rules.

**§2.3.2 Tradition-cell richness.** Cookware brand-panel tradition-cell distribution (european / american / japanese, with chinese excluded as too thin at this tier) is reported with per-cell n and per-cell Regime classification. No moderator hypothesis is pre-registered at the tradition-cell level for this phase; cell-level patterns are descriptive.

---

## §3 Brand panel

### §3.1 Panel construction logic

The v0.17 brand panel is constructed against three constraints: (i) the C1 worldwide floor of n ≥ 12 brands surviving 14-day Trends and Phase A pivot validation per §2.1; (ii) the tradition-cell descriptive sensitivity pre-registered at §2.3.2; (iii) the v1.3 §6.4.7 cascade structure, under which each tradition cell requires a primary Phase A pivot candidate with a pre-registered ordinal alternate sequence deep enough that bounded override (§6.4.7.2) and cell collapse (§6.4.7.3) remain rare events rather than routine panel-management mechanics.

The panel is stratified into three tradition cells — European, American, Japanese — with Chinese excluded as too thin at the premium-cookware tier to support a viable cell even with maximal bench depth. Each cell is composed of brands measured directly through Phase B onwards; the ordinal pivot priority within the cell defines the Phase A cascade. The primary pivot for each cell is selected on the basis of (a) baseline Trends stability under worldwide and US queries, (b) substrate-keyword salience in publicly observable LLM training distributions as of v0.16, and (c) tradition-prototypicality for the cell as a whole.

The panel is intentionally over-provisioned against C1. Worldwide n = 16 pre-floor; conservative Trends-floor attrition (1–3 brands, concentrated in European and Japanese cells per §2.3.1) leaves a post-floor floor of n = 13–15, comfortably above C1's n ≥ 12 requirement. Worldwide panel adequacy holds even under full Japanese cell collapse (n_after_Japanese_collapse = 12, exactly at C1).

### §3.2 Tradition cells and Phase A pivot ordinal

| Cell | Ordinal | Brand | Phase A role | HQ | Sub-tradition |
|---|---|---|---|---|---|
| European | 1 | Le Creuset | Primary pivot | France | Enamelled cast iron |
| European | 2 | Staub | Alternate 1 | France (Zwilling group) | Enamelled cast iron |
| European | 3 | Mauviel | Alternate 2 | France | Copper |
| European | 4 | Demeyere | Alternate 3 | Belgium (Zwilling group) | Multi-ply stainless |
| European | 5 | Fissler | Alternate 4 | Germany | Multi-ply stainless |
| European | 6 | de Buyer | Alternate 5 | France | Carbon steel |
| American | 1 | All-Clad | Primary pivot | USA (Groupe SEB) | Multi-ply stainless |
| American | 2 | Lodge | Alternate 1 | USA | Cast iron |
| American | 3 | Made In | Alternate 2 | USA | DTC multi-ply |
| American | 4 | Field Company | Alternate 3 | USA | Cast iron (refined) |
| American | 5 | Smithey | Alternate 4 | USA | Cast iron (heritage) |
| American | 6 | Hestan | Alternate 5 | USA | Multi-ply premium |
| Japanese | 1 | Vermicular | Primary pivot | Japan (Aichi Dobby) | Enamelled cast iron |
| Japanese | 2 | Iwachu | Alternate 1 | Japan | Nambu Tekki cast iron |
| Japanese | 3 | Sori Yanagi | Alternate 2 | Japan | Designer stainless |
| Japanese | 4 | Noda Horo | Alternate 3 | Japan | Enamelware (borderline) |

Noda Horo is a borderline inclusion — premium Japanese enamelware brand with cookware overlap (saucepans, kettles) but also storage-vessel overlap. Carried as Japanese alternate 3 to give the cell depth ≥ 3 and a non-trivial cascade option before bounded override. Excluded from canonical Regime classification reporting if the brand's Phase B topic-ID resolution shows storage-vessel co-occurrence dominating substrate co-occurrence. Decision documented at Phase B per pre-reg.

**Cell collapse risk per v1.3 §6.4.7.3:**

- European: very low (5-deep cascade; bounded override available at ordinal 3).
- American: very low (5-deep cascade; bounded override available at ordinal 3).
- Japanese: moderate (3-deep cascade; bounded override available at ordinal 3; full collapse if all four brands fail Phase A).

### §3.3 Stage 4 adjacency keywords

Per v1.3 §6.4.5, Stage 4 adjacency keywords are pre-registered per substrate ahead of pivot validation. The kitchenware substrate's strongest adjacency-drift risk is the design/aesthetic-object overlap that surrounds premium cookware in lifestyle and interior coverage. The pre-registered keyword pair:

- **Substrate keyword:** `cookware`
- **Adjacent category keyword:** `kitchen design`

Rationale. "Cookware" is the cleanest substrate-distinctive token across the panel (covers cast iron, multi-ply stainless, copper, carbon steel, enamelled sub-traditions without favoring any). "Kitchen design" captures the genuine adjacent-category drift risk for premium cookware: Le Creuset's well-known colour/aesthetic-object positioning, Staub's heritage-France design coupling, and (less acutely) Mauviel's copper-as-décor overlap. A high adjacent_proportion on this keyword would signal that the pivot brand's Trends signal is being driven by interior-design-context co-occurrence rather than cookware-substrate relevance, which is the discriminating test the Stage 4 mechanism is designed to enforce.

The brand-specific adjacency drifts are not pre-registered as Stage 4 keywords because Stage 4 operates at the substrate level. Brand-specific drift is captured indirectly through Stage 3 bundle position (§6.4.4) where pivot_to_ref ratio outside [0.5, 5.0] surfaces brands whose Trends signal is dominated by non-substrate context.

### §3.4 14-day Trends floor: anticipated drop risk

Per §2.3.1, US/worldwide divergence is expected. Pre-registered drop-risk assessment:

| Brand | Worldwide drop risk | US drop risk |
|---|---|---|
| Mauviel | Low | Moderate |
| Demeyere | Low | Moderate |
| Fissler | Low | Moderate |
| de Buyer | Moderate | High |
| Field Company | Low | Low |
| Smithey | Low | Low |
| Hestan | Low | Low |
| Vermicular | Moderate | High |
| Iwachu | Moderate | High |
| Sori Yanagi | Moderate | High |
| Noda Horo | High | High |

Worldwide post-floor n expected at 13–15. US sub-panel post-floor n expected at 9–12, with foreign-tradition concentration. The US sub-panel may fall below C1 on its own — this is anticipated and is the precise mechanism that produces §2.3.1's pre-registered US/worldwide divergence reporting, not a panel-design failure.

### §3.5 Registry artefact

The canonical panel is committed to `~/aias/registries/brands_kitchenware_v0.17.json` at the same commit as this pre-registration. JSON schema mirrors `brands_knives_v0.16.json`: per-brand fields for `name`, `cell`, `pivot_ordinal`, `hq_country`, `substrate_sub_tradition`, `worldwide_drop_risk`, `us_drop_risk`, and a per-cell `cascade_depth` integer. The JSON is authoritative; this §3 table is the human-readable rendering.

---

## §4 Discourse-language condition

No discourse-language hypothesis is pre-registered at v0.17. The v0.16 Japanese-prompt carry-forward test (`H_Discourse_Language_carryforward`, CARRY-FORWARD CONFIRMED at n=6) established discourse-language behaviour under canonical protocol on the medium-Identity-Load substrate adjacent to v0.17. The Japanese cookware cell at v0.17 is structurally thinner (n=4 with one borderline brand) and would not support a powered replication; running the test under a fragile cell would degrade rather than strengthen the discourse-language finding.

Discourse-language testing resumes at v0.18 indie fragrance per pre-registered programme arc. The Francophone register on indie fragrance (Le Labo, Diptyque, D.S. & Durga, Maison Margiela, Byredo's Francophone-leaning naming conventions) is structurally richer than the Japanese cookware register and provides a discourse-language cell adequate to support the next replication.

---

## §5 Analysis plan

The analysis follows the v0.16 canonical Phase D scoring spine with substrate-token substitution. No methodological revision.

### §5.1 Primary specification

For each measurement window `t ∈ {t1, t2}` and each panel `P ∈ {worldwide, US}`:

- **Bivariate:** Spearman `ρ(AIAS Presence, Trends)` over all P-eligible brands.
- **Partial:** Spearman partial `ρ(AIAS Presence, Trends | age, tradition)` over all P-eligible brands. Age = brand-founding-year decade bucket; tradition = European / American / Japanese cell membership.

Decision rules per §2.1 apply against the **worldwide panel only**. The US panel is reported as descriptive sensitivity per §2.3.1 and does not enter the primary verdict.

### §5.2 Measurement windows

`t1` and `t2` are pre-registered as separated by ≥ 30 days, with `t1` locked at the LLM-acquisition timestamp and `t2` locked at the second-acquisition timestamp. Trends pulls bracket each LLM acquisition within ± 24 hours per v0.16 precedent.

### §5.3 Descriptive sensitivities

Both descriptive sensitivities pre-registered in §2.3 are computed and reported alongside the primary verdict:

- **§2.3.1 US/worldwide divergence:** primary specification rerun on the US-eligibility sub-panel; `ρ_worldwide − ρ_US` reported at t1 and t2 for both bivariate and partial.
- **§2.3.2 Tradition-cell richness:** per-cell n (European / American / Japanese) at post-floor; per-cell Regime classification per Protocol v1.2 §6 four-regime taxonomy; per-cell `ρ` if cell n ≥ 5 (else reported as "cell n below ρ-reporting floor"). No moderator hypothesis is tested at the cell level.

### §5.4 Joint v0.16 + v0.17 verdict resolution

`H_IdentityLoad_moderator` (§2.2) resolves mechanically from the joint verdict matrix at the conclusion of v0.17 Phase D scoring. No further computation required beyond the matrix lookup.

### §5.5 Scoring artefact

Scoring is committed to `~/aias/scripts/score_v17.py`, structured as `score_v16.py` with substrate-token substitution (`knives` → `kitchenware`) and panel-registry substitution (`brands_knives_v0.16.json` → `brands_kitchenware_v0.17.json`). Decision rules (C1, C2, C3) are coded against §2.1 thresholds and are immutable post-lock. Output: canonical verdict JSON + per-window per-panel ρ table.

---

## §6 Pre-registered contingencies

### §6.1 Phase A pivot validation

Phase A pivot validation proceeds per v1.3 §6.4 against the canonical five-stage protocol on the European, American, and Japanese cells in parallel. Per-cell validation operates on the cell's primary pivot candidate (Le Creuset, All-Clad, Vermicular respectively) under the canonical thresholds locked at v1.3 §6.4.6.3:

- Stage 1 (§6.4.2): KG entity-suggestion audit; diagnostic only.
- Stage 2 (§6.4.3): baseline Trends stability; `cv_pct ≤ 30.0`.
- Stage 3 (§6.4.4): bundle position; `pivot_to_ref_ratio ∈ [0.5, 5.0]`.
- Stage 4 (§6.4.5): adjacency on pre-registered keyword pair `cookware` × `kitchen design`; `substrate_proportion ≥ 0.2` AND `adjacent_proportion ≤ 0.7`.
- Stage 5 (§6.4.6.1): conjunction rule on Stages 2, 3, 4 — all three must pass for cell pivot lock.

### §6.2 Fallback activation per v1.3 §6.4.7

On Stage 5 FAIL at the primary pivot candidate, fallback proceeds per v1.3 §6.4.7:

- **§6.4.7.1 Primary alternate activation.** First alternate in cell ordinal (Staub for European; Lodge for American; Iwachu for Japanese) activates as pivot candidate. Stages 2–4 re-run.
- **§6.4.7.2 Bounded override.** If first alternate also fails Stage 5, bounded override is available — one-time per cell per phase. Override invocation requires operator judgement on whether the failure mode is methodological-edge or substantive-disqualification; the choice is documented at the time of decision in DEVIATIONS log per §6.4.7.4.
- **§6.4.7.3 Cell collapse.** If bounded override is used and the next alternate also fails Stage 5, the cell collapses. Cell-collapse contingencies for v0.17:
  - European collapse: cell n=0; worldwide panel n=10; **C1 FAIL**; `H_Regime4_kitchenware` verdict FALSIFIED on panel inadequacy.
  - American collapse: cell n=0; worldwide panel n=10; **C1 FAIL**; same.
  - Japanese collapse: cell n=0; worldwide panel n=12; **C1 boundary HOLD** (exactly at n=12 floor); `H_Regime4_kitchenware` verdict proceeds on European + American panel; §2.3.2 tradition-cell reporting records Japanese cell as collapsed at Phase A.

### §6.3 DEVIATIONS log requirements per v1.3 §6.4.7.4

Every fallback event — alternate activation, bounded override invocation, cell collapse — generates a DEVIATIONS log entry at the time of the event. Entry fields: event timestamp, cell affected, primary brand failure mode (Stage 2/3/4 metric value and threshold), alternate brand activated (or override invoked, or collapse triggered), operator judgement narrative if bounded override was used.

The v1.3 §6.4.7.4 audit-log requirements are mandatory; no fallback event proceeds without a contemporaneous DEVIATIONS entry. This is the v0.16 precedent (Entry 3 documented the Victorinox → Wüsthof → bounded override cascade) operationalised as standing protocol.

---

## §7 Deliverables

Standard programme-spec set. All artefacts versioned `v17` or `v0.17` per pipeline convention.

| Artefact | Path | Function |
|---|---|---|
| Scoring | `~/aias/scripts/score_v17.py` | Canonical verdict against §2.1 decision rules |
| Charts | `~/aias/scripts/build_charts_v17.py` | Five figures: panel composition; Trends t1/t2 stability; AIAS Presence distribution; ρ at t1 and t2 (bivariate + partial); per-cell ρ |
| Report content | `~/aias/reports/v17_kitchenware_content.py` | Brand-format report copy |
| Report builder | `~/aias/reports/build_report_v17.py` | Third System™-format PDF; ReportLab + pypdf two-pass per pipeline standard |
| Paper draft | `~/aias/papers/v17_ssrn_paper_draft.md` | Academic SSRN paper, H1/H2 register |
| Paper builder | `~/aias/scripts/build_paper_v17.py` | Pandoc + xelatex; Carlito; per typography rules |
| OSF deposit | `~/aias/osf/v17/` | README, MANIFEST, data, registries, figures, code |
| OSF upload | `~/aias/scripts/osf_upload.py` | Direct WaterButler API to project ec6wh, path `/v17/` |
| Git tag (post-pub) | `v0.17-published` | Tagged at commit carrying SSRN abstract ID in CHANGELOG |
| Programme update | MSI WP bibliography | Cross-citation of v0.17 SSRN abstract ID + canonical methodology pair (6761698, 6797679) |

Publication sequence: scoring → charts → report PDF → SSRN paper → OSF deposit → SSRN submission → SSRN abstract ID returned → git tag `v0.17-published` → push to `github.com/thirdsystem-aias/aias` → MSI WP cross-citation.

---

## §8 Sign-off

**Pre-registrant:** Pablo Ulpiano González Castro
**Primary academic affiliation:** SVA, MPS Branding Program, New York, NY
**Research entity:** Third System (data archive and methodology venue)
**Correspondence:** pablou@pablou.com · pablou.com
**ORCID:** 0009-0003-8968-9990

**Lock target:** git tag `v0.17-prereg` at commit `<HASH>` prior to any v0.17 LLM acquisition.
**Lock date:** `<YYYY-MM-DD>` (populated at commit).

**Pre-registration declaration.** All §2 hypotheses, §3 panel, §5 analysis plan, and §6 contingencies are locked at the commit tagged `v0.17-prereg`. Decision rules C1, C2, C3 in §2.1 and the §2.2 conditional verdict matrix are immutable post-lock. Operational deviations from this pre-registration are recorded contemporaneously in `DEVIATIONS.md` per Protocol v1.3 §6.4.7.4. No verdict reframing post-acquisition.

**Declarations of interest.** The pre-registrant is employed by Samsung Electronics America in a corporate brand governance role. No Samsung-affiliated brands, no consumer-electronics brands, and no kitchenware-adjacent brands held by Samsung are included in the v0.17 panel. Samsung COI is disclosed in §Declarations of the published SSRN paper.

**Funding.** Self-funded.

**Ethics.** Not applicable. No human subjects; public APIs and LLM prompts.
