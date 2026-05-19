# AIAS™ Presence Measurement Protocol — Pre-Registration v0.17 (revision r1)

**Substrate:** Premium kitchenware (cookware)
**Programme position:** Identity-load moderator test; single-substrate same-IL replication of v0.16 knives PARTIAL
**Protocol version:** Methodology v1.2 (SSRN 6761698; canonical four-regime taxonomy per §6) + v1.3 (SSRN 6797679; Phase A pivot-validation specification per §6.4.2 anchoring rule)
**Lock target:** git tag `v0.17-prereg-r1` at commit prior to LLM acquisition; original `v0.17-prereg` tag preserved at c013ac1 as audit trail
**Pre-registrant:** Pablo Ulpiano González Castro
**Revision note:** This is revision r1 of the v0.17 pre-registration. The original (commit c013ac1, tag `v0.17-prereg`) carried §3.3 and §6.1 content misaligned with v1.3 as published. See `osf/v17/DEVIATIONS.md` Entry 1 for the contemporaneous record of the revision and its scope.

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

- **C1 — Panel adequacy:** worldwide n ≥ 12 brands surviving the 14-day Trends floor and Phase A pivot validation per v1.3 §6.4.2.
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

### §3.3 14-day Trends floor: anticipated drop risk

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

### §3.4 Registry artefact

The canonical panel is committed to `~/aias/registries/brands_kitchenware_v0.17.json` at the same commit as this pre-registration. JSON schema mirrors `brands_knives_v0.16.json`: per-brand fields for `name`, `cell`, `pivot_ordinal`, `phase_a_role`, `hq_country`, `substrate_sub_tradition`, `worldwide_drop_risk`, `us_drop_risk`, and a per-cell `cascade_depth` integer. The JSON is authoritative; this §3 table is the human-readable rendering. The `stage_4_keywords` field present in the original registry is a vestige of the superseded §3.3 framing in the c013ac1 lock and is informational only — it has no operational role under v1.3 §6.4.2.

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

### §6.1 Phase A pivot validation per v1.3 §6.4.2

Phase A pivot validation proceeds per v1.3 §6.4.2 against the canonical substrate-anchoring rule. The protocol is LLM-acquisition-based and operator-judgement-mediated; no Trends-based numeric stages are specified at v1.3.

**Procedure per pivot candidate brand:**

1. **Acquisition.** The brand is queried at 6 LLM model slots per Protocol v1.2 §5.2 canonical reference set, with a single canonical disambiguation query. The query form is held constant across all brands and phases per v0.16 precedent. Acquisition is implemented in `scripts/acquire_phase_a_v1_3.py` and writes per-slot response JSON files to `osf/v17/data/phase_a/<brand-slug>/slot_<N>.json` in the schema `{"model_id": str, "query": str, "response": str, "timestamp_utc": str}`.

2. **Token truncation.** Each response is truncated to the first 100 whitespace-tokenised words. Whitespace tokenisation per v1.3 §6.4.2 is human-readable first-N-words slicing, not LLM-tokenisation.

3. **Classification ledger generation.** `scripts/classify_phase_a_v1_3.py` (with v0.17 brand and archive constants) writes a CSV ledger at `osf/v17/classification_ledger.csv` with one row per (brand, slot) pair, columns `[brand, slot, model_id, query, first_100_tokens, anchored, anchoring_note]`. The `anchored` and `anchoring_note` columns are operator-filled.

4. **Operator anchoring classification.** For each row, the operator reads `first_100_tokens` and judges: does the primary referent name a product, line, or attribute within the premium-cookware substrate? `anchored` column is filled as 1 (substrate-anchored) or 0 (not substrate-anchored). Optional rationale in `anchoring_note`. Operator judgement is the canonical classifier per v1.3 §6.4.2 — no automated classification is specified.

5. **C_P tally.** Re-running `classify_phase_a_v1_3.py` against the filled ledger produces per-brand C_P verdict:
   - **C_P PASSED:** anchoring count ≥ 5/6 (supermajority threshold per v1.3 §6.4.2)
   - **C_P FAILED:** anchoring count ≤ 4/6

A brand with `C_P PASSED` is eligible as Phase A pivot for its cell. A brand with `C_P FAILED` triggers the fallback cascade per §6.2.

### §6.2 Fallback activation per v1.3 §6.4.7

On `C_P FAILED` at the primary pivot candidate, fallback proceeds per v1.3 §6.4.7:

- **§6.4.7.1 Primary alternate activation.** First alternate in cell ordinal (Staub for European; Lodge for American; Iwachu for Japanese) activates as pivot candidate. New Phase A acquisition for the alternate brand; new ledger rows; new operator classification; new C_P tally.
- **§6.4.7.2 Bounded override.** If the first alternate also returns `C_P FAILED`, bounded override is available — one-time per cell per phase. Override invocation requires operator judgement on whether the failure mode reflects a methodological-edge artifact (e.g., ambiguous truncation, off-target LLM response) or substantive substrate-disqualification of the brand. The choice is documented at the time of decision in `osf/v17/DEVIATIONS.md` per §6.4.7.4.
- **§6.4.7.3 Cell collapse.** If bounded override is used and the next alternate also returns `C_P FAILED`, the cell collapses. Cell-collapse contingencies for v0.17:
  - European collapse: cell n=0; worldwide panel n=10; **C1 FAIL**; `H_Regime4_kitchenware` verdict FALSIFIED on panel inadequacy.
  - American collapse: cell n=0; worldwide panel n=10; **C1 FAIL**; same.
  - Japanese collapse: cell n=0; worldwide panel n=12; **C1 boundary HOLD** (exactly at n=12 floor); `H_Regime4_kitchenware` verdict proceeds on European + American panel; §2.3.2 tradition-cell reporting records Japanese cell as collapsed at Phase A.

### §6.3 DEVIATIONS log requirements per v1.3 §6.4.7.4

Every fallback event — alternate activation, bounded override invocation, cell collapse — generates a DEVIATIONS log entry at the time of the event. Entry fields: event timestamp, cell affected, primary brand C_P count and failure mode, alternate brand activated (or override invoked, or collapse triggered), operator judgement narrative if bounded override was used.

The v1.3 §6.4.7.4 audit-log requirements are mandatory; no fallback event proceeds without a contemporaneous DEVIATIONS entry. This is the v0.16 retrospective scoring precedent operationalised as standing protocol.

---

## §7 Deliverables

Standard programme-spec set. All artefacts versioned `v17` or `v0.17` per pipeline convention.

| Artefact | Path | Function |
|---|---|---|
| Phase A acquisition | `~/aias/scripts/acquire_phase_a_v1_3.py` | Fresh 6-slot LLM acquisition for pivot candidates |
| Phase A classifier | `~/aias/scripts/classify_phase_a_v1_3.py` | Ledger generation + C_P tally per v1.3 §6.4.2 |
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

Publication sequence: Phase A acquisition → ledger fill → C_P tally → cell-pivot lock → scoring → charts → report PDF → SSRN paper → OSF deposit → SSRN submission → SSRN abstract ID returned → git tag `v0.17-published` → push to `github.com/thirdsystem-aias/aias` → MSI WP cross-citation.

---

## §8 Sign-off

**Pre-registrant:** Pablo Ulpiano González Castro
**Primary academic affiliation:** SVA, MPS Branding Program, New York, NY
**Research entity:** Third System (data archive and methodology venue)
**Correspondence:** pablou@pablou.com · pablou.com
**ORCID:** 0009-0003-8968-9990

**Lock target:** git tag `v0.17-prereg-r1` at commit `<HASH_R1>` prior to any v0.17 LLM acquisition.
**Lock date:** `2026-05-19` (revision r1 date; original lock c013ac1 on 2026-05-19).

**Pre-registration declaration.** All §2 hypotheses, §3 panel, §5 analysis plan, and §6 contingencies are locked at the commit tagged `v0.17-prereg-r1`. Decision rules C1, C2, C3 in §2.1 and the §2.2 conditional verdict matrix are immutable post-lock. Operational deviations from this pre-registration are recorded contemporaneously in `osf/v17/DEVIATIONS.md` per Protocol v1.3 §6.4.7.4. No verdict reframing post-acquisition.

**Revision r1 declaration.** This revision corrects misalignment between the original v0.17 pre-registration (commit c013ac1, tag `v0.17-prereg`) and Protocol v1.3 as published at SSRN 6797679. §3.3 (Stage 4 adjacency keywords) removed and subsequent §3 subsections renumbered; §6.1 rewritten to specify v1.3 §6.4.2 C_P anchoring rule. Substantive hypotheses §2.1, §2.2, §2.3 and panel composition §3.2 are unchanged from the original lock. See `osf/v17/DEVIATIONS.md` Entry 1 for the contemporaneous record. The discipline invariant (pre-registration locked at git commit before any LLM acquisition) is preserved: no v0.17 LLM acquisition occurred between the original lock at c013ac1 and this revision.

**Declarations of interest.** The pre-registrant is employed by Samsung Electronics America in a corporate brand governance role. No Samsung-affiliated brands, no consumer-electronics brands, and no kitchenware-adjacent brands held by Samsung are included in the v0.17 panel. Samsung COI is disclosed in §Declarations of the published SSRN paper.

**Funding.** Self-funded.

**Ethics.** Not applicable. No human subjects; public APIs and LLM prompts.
