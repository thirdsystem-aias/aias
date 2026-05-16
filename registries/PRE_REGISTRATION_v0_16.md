# AIAS™ Measurement Programme — v0.16 Pre-Registration

**Lock date:** [TBD — target before LLM acquisition]
**Acquisition target:** [TBD]
**Git tag:** `v0.16-prereg`
**Carry-forward base:** v0.15 (SSRN 6768059, git tag `v0.15-published`, commit [TBD])
**Methodology base:** AIAS Presence Measurement Protocol v1.2 (SSRN 6761698)
**Lineage extension:** v0.8 Discourse-Language Knives (SSRN 6728000)
**Category:** kitchen knives (chef's knife and adjacent kitchen cutlery)

---

## 1. Strategic context

v0.16 brings the v1.2-formalized construct-validity panel — developed across v0.11–v0.15 — to the kitchen-knives substrate, completing a programme arc that began in v0.8 Discourse-Language Knives. That earlier paper surfaced a discourse-language finding on knives before the construct-validity panel and the four-regime taxonomy had been formalized. v0.16 returns to the same substrate with the canonical protocol, testing two independent claims in a single measurement wave.

**Strategic position in the AIAS 1.0 critical path.** Premium facial skincare (v0.11), personal finance apps (v0.13), and premium tea (v0.14, v0.15) constitute the current Regime 4 (Covariate-saturated weak) empirical foundation — three substrates, four phases. v0.16 tests Regime 4 replication on a fourth substrate. A confirmed replication moves the methodology paper from a three-substrate floor to a four-substrate floor before Phase 4 begins. A productive falsification (knives lands Regime 1, 2, or 3) ships the result and documents the regime boundary.

**Identity-load consideration.** Kitchen knives carry medium identity-load — a clearer connoisseurship signal than tea, finance, or skincare, but well below fragrance or luxury watches. This makes knives a productive Regime 4 test case: a confirmed classification would extend the regime's empirical floor *across identity-load conditions*, not only at the low-identity-load floor where the regime was established. A falsified classification would directly support the hypothesis that Regime 4 is bounded by identity-load below a threshold yet to be specified — an empirically meaningful result either way.

**Selection rationale (knives over specialty coffee).** Specialty coffee remains a v0.17 candidate. Knives is selected for v0.16 on three grounds: (a) it extends a documented programme lineage (v0.8) and closes a methodological arc on a substrate already in the published record; (b) the tradition-cell stratification (Japanese, German, French, American/specialty, Chinese) maps cleanly onto the v0.14/v0.15 stratification logic the pipeline now handles; (c) the cross-lingual prompt structure required for H_Discourse_Language_carryforward is the same structure required for full v1.2 protocol execution — no additional protocol engineering.

---

## 2. Pre-registered hypotheses

### H_Regime4_replication_knives

**Statement.** Brand AI Presence on the kitchen-knives substrate exhibits the canonical Regime 4 (Covariate-saturated weak) signature established on premium facial skincare (v0.11), personal finance apps (v0.13), and premium tea (v0.14, v0.15).

**Decision rules (pre-registered).**

| Verdict | Conditions (must hold at both waves t₁ and t₂) |
|---|---|
| **CONFIRMED** | (1) n_eligible ≥ 12 ∧ (2) bivariate ρ(brand_age, AI_presence) ∈ (−1, +0.35) ∧ (3) sign(ρ_t₁) = sign(ρ_t₂) ∧ (4) residual partial ρ(brand_age, AI_presence \| tier, tradition_cell) < 0 |
| **PARTIAL** | Conditions (1), (2), (3) hold but (4) fails (positive partial after controls) — non-saturated weak signature; productive Regime-classification reassignment |
| **FALSIFIED** | Condition (1) fails (n_eligible < 12) OR condition (2) fails (bivariate ρ ≥ 0.35) — productive falsification; methodology paper retains three-substrate Regime 4 floor (skincare, finance, tea) |

### H_Discourse_Language_carryforward

**Statement.** The v0.8 Discourse-Language Bias finding on knives — that non-English-discourse-anchored brands (the Japanese tradition cell in particular) underperform in English-language prompt conditions relative to discourse-language-matched conditions — holds under v1.2 protocol with the corrected eligibility filtering.

**Decision rules (pre-registered).** Computed on the Japanese tradition cell (anchor cell for the v0.8 finding):

| Verdict | Condition |
|---|---|
| **CARRY-FORWARD CONFIRMED** | n_eligible_japanese ≥ 5 ∧ ρ_(English, native-language)(per-brand AI Presence) < 0.85 at both waves |
| **CARRY-FORWARD WEAKENED** | n_eligible_japanese ≥ 5 ∧ ρ_(English, native-language) ∈ [0.85, 0.95) — finding survives but at attenuated magnitude under v1.2 eligibility filtering |
| **CARRY-FORWARD FALSIFIED-favorable** | n_eligible_japanese ≥ 5 ∧ ρ_(English, native-language) ≥ 0.95 — the v0.8 finding was a pre-v1.2 protocol artifact corrected by v1.2 eligibility filtering. Productive falsification |
| **INCONCLUSIVE** | n_eligible_japanese < 5 — insufficient cell coverage to evaluate |

Note. CARRY-FORWARD FALSIFIED-favorable is methodologically informative even if substantively against the v0.8 finding — it strengthens v1.2 protocol credibility by demonstrating that the eligibility-filtering correction has measurable effects.

---

## 3. Brand panel (pre-registered, ~24 brands across 5 tradition cells)

### Cell 1: Japanese tradition (n = 6)
- Shun (Kai Group, founded 1908; Seki, Japan)
- Global (Yoshikin, founded 1985; Niigata, Japan)
- Miyabi (Zwilling subsidiary, Seki tradition)
- Mac (Mac Knife, founded 1964; Seki, Japan)
- Tojiro (founded 1953; Niigata, Japan)
- Yoshihiro (Sakai tradition; multi-generational)

### Cell 2: German tradition (n = 5)
- Wüsthof (founded 1814; Solingen)
- Zwilling J.A. Henckels (founded 1731; Solingen)
- Messermeister (founded 1981; German-tradition lineage, US headquarters)
- Güde (founded 1910; Solingen)
- Friedr. Dick (founded 1778; Esslingen)

### Cell 3: French tradition (n = 4)
- Sabatier — **flagged for topic-ID care; generic French mark used by multiple Thiers producers**; pre-registered topic-ID resolution per v1.2 §4 5-stage protocol
- Opinel (founded 1890; Savoie) — primarily folding/utility, included for tradition representation; topic-ID resolution must filter to kitchen-cutlery context
- Laguiole — **flagged for topic-ID care; generic regional mark**; topic-ID resolution per v1.2 §4
- Nogent (Goyon-Chazeau; Thiers)

### Cell 4: American / specialty (n = 5)
- Cutco (founded 1949; Olean, NY)
- Dalstrong (founded 2012; Toronto, sold globally)
- Misen (founded 2015; direct-to-consumer)
- New West KnifeWorks (founded 1997; Jackson, WY)
- Made In (founded 2017; Austin, TX) — cookware-primary brand inclusive of cutlery; flagged for category-coverage check

### Cell 5: Chinese tradition (n = 4)
- CCK Chan Chi Kee (founded 1947; Hong Kong)
- Shibazi (Shi Ba Zi Zuo; Yangjiang)
- Sunlong
- ZHEN (Chinese-tradition, US distribution)

**Pre-registered alternates** (used in pre-registered substitution order if a primary brand fails topic-ID resolution or eligibility):
- Japanese cell: Masamoto, Misono, Tadafusa
- German cell: Schmidt Brothers (German-tradition lineage), Robert Herder
- French cell: Au Nain, Goyon-Chazeau Le Thiers
- American cell: Bob Kramer (Zwilling collaboration; high-end), Wüsthof Classic Ikon (excluded — duplicate), Hammer Stahl
- Chinese cell: Hu Si Chao, Dengjia, Hengtai

### Pivot

- **Primary pivot:** Victorinox (Swiss, founded 1884) — chef-knife line (Swiss Classic / Fibrox) is the restaurant-industry workhorse; high global volume; low brand-age signal interference; broad search-interest base.
- **Fallback pivot:** Wüsthof (German, 1814) — cleaner in-category in-tradition anchor; selected only if Victorinox topic-ID resolution surfaces Swiss-Army-knife confusion above v1.2 §4 threshold.

Pivot rationale. The pivot's role under v1.2 §5 is to normalize across waves under stable search interest. Victorinox's chef-knife sub-category satisfies stability requirements; the Swiss-Army-knife adjacency is a topic-ID concern, not a search-interest concern. The 5-stage protocol resolves the adjacency at lock; if it does not, Wüsthof inherits the pivot role without further panel change.

---

## 4. Pre-registered measurement specification

Inherit v1.2 protocol unchanged:

- LLM panel: 14 models across vendors per v1.2 §3
- Waves: 2 at locked timestamps, separation per v1.2 §3.4
- Prompt set: cross-lingual (English baseline + tradition-language conditions for Japanese, German, French, Chinese cells)
- Topic-ID resolution: 5-stage protocol per v1.2 §4
- Eligibility filtering: per v1.2 §4.3
- Bundled-E5 rescue: per v1.2 §4.4

**Discourse-language condition (specific to v0.16).** The cross-lingual prompt set must include, at minimum, the following pairings to enable H_Discourse_Language_carryforward:

| Tradition cell | English condition | Native-language condition |
|---|---|---|
| Japanese | "best Japanese chef knives" (en) | 「最高の日本の包丁」(ja) |
| German | "best German chef knives" (en) | "beste deutsche Küchenmesser" (de) |
| French | "best French chef knives" (en) | "meilleurs couteaux de cuisine français" (fr) |
| Chinese | "best Chinese kitchen knives" (en) | "最好的中国菜刀" (zh) |

Exact prompt wording locks at Phase 1 prompt-set commit (separate file: `prompts_knives_v0.16.json`).

---

## 5. Pre-registered analysis plan

Carry-forward from v0.15 unchanged:

1. AI Presence Index computed per v1.2 §5
2. Pivot-normalized brand-day matrices
3. Spearman ρ analysis per H_Regime4_replication_knives decision rules — bivariate and partial (controls: brand_age, tier, tradition_cell)
4. Rank-correlation analysis per H_Discourse_Language_carryforward decision rules — Japanese tradition cell, English vs native-language conditions
5. Per-cell construct-validity diagnostics (n_eligible, mention dispersion, topic-ID resolution rate)
6. Cross-wave stability check (carryover from H2 lineage)

---

## 6. Pre-registered contingencies

**Topic-ID failure.** If Sabatier, Laguiole, or any other panel brand fails the v1.2 §4 5-stage protocol (e.g., undecidable producer attribution, hunting/folding-knife confusion above threshold), the brand is replaced with the next pre-registered alternate from the same tradition cell. Substitution is documented in the published methodology log.

**Cell collapse.** If any tradition cell falls below n_eligible = 3 after pre-registered alternate exhaustion, the cell is treated per the v0.15 chinese-cell precedent: retained for descriptive reporting with explicit underpower flag; excluded from inferential analysis. The Regime 4 verdict is computed on the surviving panel.

**Identity-load contamination.** If topic-ID resolution surfaces hunting-knife, folding-knife, or tactical-knife confusion for any kitchen-knife brand above v1.2 §4 threshold, that brand is excluded and a pre-registered alternate substitutes. Documented in the methodology log.

**Bundled-E5 rescue.** If a brand fails individual-prompt eligibility but satisfies bundled-prompt eligibility, the brand is retained with a bundled-E5 flag per v1.2 §4.4 (precedent: v0.15 new french cell).

**Pivot failure.** If Victorinox topic-ID resolution exceeds v1.2 §4 confusion threshold at lock, Wüsthof inherits the pivot role and the panel reduces by one brand (Wüsthof exits the German tradition cell; German cell collapses to n = 4 with no alternate substitution, since Wüsthof's pivot role precludes within-cell scoring).

---

## 7. Deliverables (this phase)

1. **Brand-format report** (Third System™ brand template): `v0.16_brand_format_report.pdf`
2. **SSRN working paper**: *Construct Validity and Regime 4 Replication on the Kitchen-Knives Substrate: AIAS Presence Measurement Programme v0.16*
3. **OSF deposit** at `/v16/` (raw responses, analysis code, charts, report, paper, manifest)
4. **SSRN abstract ID** and cross-citation update to MSI WP bibliography (alongside the pending v0.13, v0.14, v0.15, methodology-paper updates)
5. **Git tag** `v0.16-published` at commit of methodology lock

---

## 8. Sign-off

Author: Pablo Ulpiano González Castro
ORCID: 0009-0003-8968-9990
Pre-registration drafted: 16 May 2026
Lock target: [TBD]
Commit hash at lock: [TBD]

---

*This pre-registration is a working document until git-committed and tagged at* `v0.16-prereg`. *Tag commit is the canonical lock; this file's contents at tag are the binding pre-registration.*
