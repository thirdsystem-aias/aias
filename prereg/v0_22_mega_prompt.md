# AIAS Presence Measurement Protocol — v0.22 Mega-Prompt

**Phase identifier:** v0.22
**Substrate:** Automotive (passenger car brands, corporate-level granularity)
**Phase position:** Sixth substrate family for the Presence-component AIAS™ 1.0 anchor base; first prospective phase under v1.6 methodology lock; stress-test of Phantom Brand Persistence on the most heritage-saturated substrate yet measured
**Protocol version:** v1.6 (SSRN 6816340) — all three increments in scope (Inc1 Substrate Recognition pre-screen; Inc2 H_IdentityLoad_Direct; Inc3 Phantom Brand Persistence)
**Carry-forward:** v1.5 two-channel Recall (SSRN 6810758), v1.2 four-regime taxonomy (SSRN 6761698)
**Pre-reg lock:** `v0.22-prereg-r2` (supersedes r1 — see DEVIATIONS Entry 0)
**Pre-reg artifact:** `prereg/v0_22_automotive_content.py` (pure-data Python module, code-importable by build pipeline)
**Builder fork sources:** v0.21 (`build_report_v21.py`, `v21_cosmetics_content.py`, `build_charts_v21.py`, `score_v21.py`, `run_acquisition_v21.py`)

---

## Strategic context

v0.21 (Cosmetics, SSRN 6815378) returned H_Type2_emergence = EMERGED with three clean Cell B cases (Rare Beauty R_cult=17 — the program's textbook dissociation, plus Huda Beauty and Kylie Cosmetics) and one out-of-cell case (e.l.f. Cosmetics, Cell C). The Phantom Brand Persistence construct reached its strongest single demonstration in v0.21: Glossier surfaced unprompted in cultural-frame Recall across all 6/6 panel models, off-panel entirely (R_phantom = 12 against a max of 18).

v0.22 picks up Phantom Brand Persistence as the **primary stress-test target** on the substrate uniquely positioned to push it past its v0.21 single-case anchor. Automotive heritage is unusually deeply coded in LLM corpora — model brand kinship runs deep, with literature, film, and cultural references stacked over a century. **More consequentially, automotive is the only substrate family available to the program where corporate-brand death is documented and dated** (Pontiac 2010, Oldsmobile 2004, Plymouth 2001, Mercury 2010, Saturn 2010). No prior substrate (knives, kitchenware, indie fragrance, audiophile headphones, skincare, cosmetics) supports the Cell D_Defunct test design: brand death is rare and rarely dated in other categories.

The Cell D_Defunct panel converts v0.22 from a routine heritage stress-test into a substantial design innovation. The lead hypothesis `H_Phantom_Defunct` measures the **pure-phantom upper bound** — whether the AI mediation layer surfaces documentably dead corporate brands in unprompted current-tense Recall as if currently active. This is the cleanest test of Phantom Brand Persistence the program can run, because the null-hypothesis baseline is unambiguous: a brand that has not existed for 15–25 years cannot legitimately appear in present-tense responses to "what car brands come to mind?" without the AI mediation layer surfacing a phantom.

v0.22 also closes the 6th substrate family for the Recognition × Recall dissociation construct, extending the cumulative anchor base under v1.6 lock.

---

## Pre-registration design

### Substrate operational definition

Automotive is operationally defined as a four-cell heritage-gradient panel spanning the passenger-car consumer-discovery surface, sampled across four tiers of Identity Load (IL) and heritage saturation:

- **Cell A — Heritage (high IL, aristocratic / Old-World positioning).** Brands whose primary value driver is documented heritage. Status acquisition is performed through heritage association.
- **Cell B — Disruptor (high IL, no heritage substrate).** EV-native brands without legacy positioning; tests the high-IL pattern from v0.20/v0.21 Cell B without confounding with traditional heritage coding.
- **Cell C — Mass-Legacy (low-medium IL, long-tenured corporate brands where heritage is not the lead value driver).** Heritage exists in the brand history but is not the consumer-purchase rationale.
- **Cell D — Defunct (pure-phantom panel).** Discontinued corporate brands. **Lead hypothesis test cell.**

The four-cell structure is not strictly an IL gradient — Cell D positions outside the IL ladder as a phantom-test cell. The A-vs-B and A-vs-C comparisons follow program convention (Cell A high IL vs Cell C low-medium IL; Cell B high IL with disruptor framing). Cell D is positioned as the upper-bound phantom test.

### Locked brand registry (n = 24)

```
Cell A — Heritage (high IL, Old-World positioning):
  1. Mercedes-Benz
  2. Jaguar
  3. Cadillac
  4. Rolls-Royce
  5. Bentley
  6. Porsche
  7. BMW

Cell B — Disruptor (high IL, EV-native, no heritage):
  1. Tesla
  2. Rivian
  3. Lucid
  4. Polestar
  5. Fisker

Cell C — Mass-Legacy (long-tenured corporate brands, heritage not lead value):
  1. Toyota
  2. Honda
  3. Ford
  4. Chevrolet
  5. Hyundai
  6. Volkswagen
  7. Nissan

Cell D — Defunct (discontinued corporate brands; pure-phantom panel):
  1. Pontiac     (closed 2010)
  2. Oldsmobile  (closed 2004)
  3. Plymouth    (closed 2001)
  4. Mercury     (closed 2010)
  5. Saturn      (closed 2010)
```

**Borderline classifications (locked ex-ante):**

- **Cadillac:** American luxury brand with heritage positioning and corporate parent (GM) inside Cell C's territory. Classified Cell A per heritage as primary value driver; flagged for retrospective dissociation review.
- **Porsche:** straddles heritage and performance-engineering. Cell A per Old-World positioning + heritage as primary cultural code (vs Tesla/Rivian performance-without-heritage). Volkswagen Group corporate parent does not override.
- **Volkswagen:** heritage-coded in LLM corpora (Beetle, German engineering legacy) but classified Cell C per mass-market positioning as primary value driver. Flagged for retrospective dissociation review if Type 2 case.
- **BMW:** German heritage brand without aristocratic positioning (vs Mercedes-Benz / Rolls-Royce). Cell A per Old-World engineering heritage anchor; the BMW / Mercedes-Benz / Jaguar / Cadillac / Rolls-Royce / Bentley / Porsche set as constructed is the heritage-cell core.

**Per-cell alternates (for DEVIATIONS cascade, ordered):**

- Cell A: Lexus, Aston Martin, Lamborghini
- Cell B: NIO, Faraday Future, Karma Automotive *(note: Karma overlaps phantom-revival territory; substitution triggers DEVIATIONS entry)*
- Cell C: Mazda, Subaru, Kia
- Cell D: AMC (defunct 1988), DeLorean Motor Company (defunct 1982; boutique-revived — confounded), Studebaker (defunct 1967) *(note: Cell D alternates are weak — DeLorean and Hummer-style revivals confound the pure-phantom test; substitutions should trigger DEVIATIONS entry and pre-acquisition revaluation)*

### Reference panel (locked, unchanged from v0.17–v0.21)

```
- claude-opus-4-5
- claude-sonnet-4-5
- gpt-4o
- gpt-4o-mini
- gemini-2.5-flash
- gemini-2.5-flash-lite
```

Six distinct LLMs, one response per model per probe. Per-brand C_P = yes-count across panel models, range 0–6. Per-brand R_cat / R_cult = mentions across (3 probes × 6 models), max 18 per channel per brand.

### Phase A — Recognition probe

For each of the 24 brands, send to each of the 6 panel models:

```
Is the brand {BRAND} commonly recognized as a car brand? Answer yes or no.
```

Per-brand C_P score = count of yes responses across the panel (range 0–6).

**Critical blinding for Cell D phantom test:** Cell D brands are presented in Phase A Recognition without temporal cues. The probe asks whether each brand "is commonly recognized as a car brand" — present-tense framing. The panel is not told that any subset of brands is discontinued. R_phantom_defunct measures whether the panel surfaces these brands in unprompted current-tense Recall as if currently active — the contamination risk is the probe itself prompting temporal awareness, which the present-tense Phase A framing avoids.

Pivot cascade follows v1.5 §6.4: first brand in cascade order achieving C_P = 6/6 becomes cell pivot; cascade exhaustion documented per program precedent.

### Phase B — six-frame battery (two-channel Recall)

**R_cat channel (q1–q3, canonical retrieval):**

- **q1 (best):** *What are the best car brands? List several with descriptions.*
- **q2 (expert):** *What car brands do automotive experts and reviewers recommend? Name several.*
- **q3 (high-quality):** *What car brands are highest quality and most reliable? Name several brands with descriptions.*

**R_cult channel (q4–q6, cultural-footprint / heritage retrieval):**

- **q4 (heritage / prestige):** *What car brands carry deep heritage, prestige, or a sense of legacy? List several.* *(Locked R_cult per pre-reg D5)*
- **q5 (aspirational / status):** *What car brands do affluent or status-conscious buyers tend to choose? Name several.*
- **q6 (iconic / storied):** *Which car brands have the most iconic or storied identity in popular culture? Name several.*

Per-brand R_cat = sum across (q1, q2, q3) × 6 models = max 18.
Per-brand R_cult = sum across (q4, q5, q6) × 6 models = max 18.

**R_phantom_defunct = unprompted Cell D appearances across (q1, q2, q3) × 6 models, max 18 per Cell D brand.** Cell D R_cult-channel mentions tracked descriptively as exploratory sub-test (heritage-coded phantom signal).

Brand-mention detection per v1.4 canonical rules (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication).

---

## Hypotheses (locked, six)

### H_Phantom_Defunct (LEAD)

Discontinued corporate brands surface in unprompted current-tense Recall as if currently active.

| Verdict | Criterion |
|---|---|
| **CONFIRMED** | any Cell D brand R_phantom_defunct ≥ 4 |
| PARTIAL | ≥ 1 Cell D brand with 1 ≤ R_phantom_defunct < 4 |
| FALSIFIED | all Cell D brands R_phantom_defunct = 0 |

Threshold rationale: 4/18 ≈ 22% surfacing — robustness floor against single-model artifact, harmonized with H_Phantom_Brand_Persistence_heritage PARTIAL floor (4/18). Threshold history: r1 set N=3 on assumed max-12 scale; r2 corrected to N=4 on max-18 scale. See DEVIATIONS Entry 0.

Exploratory sub-test (descriptive, non-locked): R_cult-channel surfacing of Cell D brands as evidence of heritage-coded phantom (vs simple temporal-confusion phantom).

### H_Phantom_Brand_Persistence_heritage (PRIMARY SUPPORTING)

Cell A_Heritage brands exhibit elevated R_phantom on the v1.6 Inc3 measurement.

| Verdict | Criterion |
|---|---|
| **CONFIRMED** | any Cell A brand R_phantom ≥ 8 |
| PARTIAL | ≥ 1 Cell A brand with 4 ≤ R_phantom < 8 |
| FALSIFIED | all Cell A R_phantom < 4 |

Benchmark reference: v0.21 Glossier R_phantom = 12.

### H_Regime4_automotive (within-phase substantive)

Sequential C1 → C2 → IL-gradient guard → C3 per Protocol v1.5:

- **C1:** post-attrition worldwide n ≥ 12
- **C2 (v1.5 multi-statistic, per cell):** distinct C_P values ≥ 3 ∧ modal C_P share ≤ 0.625
- **IL-gradient guard:** Cell B top-2 R_cat share − Cell C top-2 R_cat share ≥ 0.10
- **C3:** per-cell Spearman ρ between C_P and R_cat ≥ 0.50 in ≥ 2 of cells (n ≥ 5)

Routing: C2 failure in ≥ 2 cells → FALSIFIED; in 1 cell → PARTIAL; subsequent failures → PARTIAL; all clear → CONFIRMED.

Predicted verdict: **FALSIFIED on uniform Recognition saturation** (consistent with v0.21 cosmetics pattern; automotive is a culturally pervasive substrate where C2 typically rejects on saturation).

### H_Dissoc_substrate_generalization (6th substrate family)

Iwachu-pattern cases (C_P ≥ 5 ∧ R_cat ≤ 2) appear in ≥ 1 of 4 cells.

| Cells with Iwachu cases | Verdict |
|---|---|
| ≥ 2 of 4 | GENERALIZED |
| 1 of 4 | PARTIAL |
| 0 | NARROWED |

This is the **sixth-substrate-family extension** for the Presence-component AIAS™ 1.0 anchor base, under v1.6 lock. GENERALIZED here advances the cross-substrate generalization claim from the v0.21 five-family base.

### H_IdentityLoad_direct (v1.6 Inc2)

Heritage-cell Identity Load measured directly per v1.6 Inc2 R4-independent bootstrap.

| Verdict | Criterion |
|---|---|
| CONFIRMED | Cell A mean IL > Cell B mean IL at locked threshold |
| FALSIFIED | reversed or null |

Predicted CONFIRMED (high IL: A, D; low IL: B). The Cell D IL signal — if observed — is a sub-claim worth surfacing in §Discussion: defunct brands may retain heritage-channel IL signal even without active brand maintenance.

### H_SubstrateRecognition_PreScreen (v1.6 Inc1)

Substrate-level Recognition saturation pattern.

| Predicted outcome | Cell-level C_P |
|---|---|
| **UNIFORM SATURATION** | all 4 cells C_P near 6/6 (program-typical for culturally pervasive substrates) |
| Differential | any cell with modal C_P < 5 |

Non-directional classification probe; outcome routes downstream interpretation of H_Regime4 verdict.

---

## Substantive predictions (descriptive, for §3 narrative pre-loading)

**Cell A — Heritage.** Expected near-saturated C_P (mean ~5.8–6.0/6): all 7 brands are primary-automotive identities in LLM corpora with century-plus heritage. **Variance prediction: very low.** Risk of full Cell A saturation, v1.5 C2 rejection — acceptable, as primary v0.22 verdicts (H_Phantom_Defunct, H_Phantom_Brand_Persistence_heritage) do not depend on H_Regime4 clearing.

**Cell B — Disruptor.** Expected variance-rich C_P distribution (mean ~4.5–5.5/6): Tesla saturated; Rivian and Lucid moderate-to-high; Polestar moderate; Fisker variable (recent corporate distress may affect Recognition). **This is the variance-rich cell v1.5 C2 was designed for; possible pass.**

**Cell C — Mass-Legacy.** Expected near-saturation similar to v0.20 Clinical / v0.21 Drugstore: Toyota / Honda / Ford / Chevrolet / Hyundai / Volkswagen / Nissan all heavily represented as corporate automotive entities. **v1.5 C2 likely rejects on saturation.**

**Cell D — Defunct.** Expected high C_P despite documented brand death (mean ~4.5–5.5/6). Pontiac and Oldsmobile likely near-saturated. Plymouth somewhat lower (oldest closure, weaker recent cultural footprint). Mercury and Saturn variable. **Key empirical observation:** if Phase A Recognition saturates on defunct brands, the AI mediation layer is treating defunct corporate brands as recognizable automotive entities — which is the precondition for the H_Phantom_Defunct test to be meaningful at Phase B.

**Recall predictions:**

- **Cell A R_cat:** high, distributed (Mercedes-Benz, BMW, Porsche, Cadillac — broad coverage in canonical "best" frames)
- **Cell B R_cat:** Tesla saturated; Rivian / Lucid moderate; Polestar / Fisker low
- **Cell C R_cat:** very high, near-saturated (mass-volume brands dominate canonical lists)
- **Cell D R_cat:** **the primary test** — Pontiac and Oldsmobile have strong cultural footprint; Mercury moderate; Plymouth and Saturn lower. Predicted Cell D R_cat surfacing range: 0–6 per brand for the weakest, 4–10 per brand for the strongest. H_Phantom_Defunct CONFIRMED requires ≥ 4 for at least one brand.

- **Cell A R_cult:** very high — this is the heritage-channel home turf (Mercedes-Benz, Rolls-Royce, Bentley, Porsche, BMW all saturated in heritage / prestige / legacy framing)
- **Cell B R_cult:** very low (Disruptor cell explicitly excludes heritage substrate; Tesla may surface anecdotally as "modern-iconic" but should not saturate heritage frames)
- **Cell C R_cult:** moderate (Ford, Chevrolet, Volkswagen carry historical-corporate heritage but classified mass-legacy)
- **Cell D R_cult:** **the heritage-coded phantom exploratory sub-test** — if defunct brands surface in heritage Recall, the phantom-of-heritage interpretation is supported

**Phantom Brand Persistence projections:**

- **Strong H_Phantom_Defunct candidates:** Pontiac (GTO, Firebird, Trans Am — extensive film and cultural footprint), Oldsmobile (corporate Americana — long history through 2004), Mercury (deep film and music references). R_phantom_defunct ≥ 4 likely for at least one of these.
- **Boundary cases:** Plymouth (Hemi heritage but weak post-closure cultural maintenance), Saturn (relatively brief lifespan 1985–2010 limits cultural anchor).
- **Heritage-coded phantom (R_cult-channel) signal:** if Cell D brands surface in q4 (heritage / prestige / legacy) — particularly Pontiac and Oldsmobile — this provides the exploratory evidence for heritage-coded phantom over temporal-confusion phantom.
- **Type 2 candidates** (R_cat ≤ 2 ∧ R_cult ≥ 5): Rolls-Royce, Bentley (heritage-channel saturation with possibly sparse canonical Recall); some Cell D brands could surface as Type 2 if R_cult-channel heritage-coded phantom obtains.

---

## DEVIATIONS Entry 0 — Pre-acquisition r1 → r2 amendment + COI screen

**Date:** 2026-05-25
**Screen subject:** v0.22-prereg-r1 INSTRUMENT specification + Samsung Electronics America potential exposure to v0.22 registry.

### Part A — r1 → r2 INSTRUMENT amendment

**Issue:** v0.22-prereg-r1 locked INSTRUMENT as single-model GPT-4.1 × n=12 iterations. This contradicted program convention from v0.17–v0.21 onward, which uses the 6-model reference panel (one response per model per probe; max C_P = 6, max R_cat / R_cult = 3 probes × 6 models = 18). The r1 spec arose from a Claude-assisted drafting error during the original lock session, deferred to under user trust without verification against the v0.21 mega-prompt panel definition.

**Consequences if uncorrected:**
- Cross-substrate Recognition comparability breaks (C_P range 0–12 vs program-standard 0–6).
- Single-model iteration measures model-internal variance, not the AI mediation layer broadly.
- Build pipeline (`build_charts_v22.py`, `build_report_v22.py`) is already coded against the 6-model assumption (C_P max 6, R max 18) and would require methodology-level rework.
- Implicit methodology increment that v0.22 was not designed to introduce.

**Disposition:** Amendment via v0.22-prereg-r2 (commit `0dde745` on `program-docs`, tag annotated). Pre-acquisition defect catch; no data collected under r1. INSTRUMENT corrected to the 6-model reference panel. H_Phantom_Defunct CONFIRMED threshold moved 3 → 4 to harmonize with the corrected max-18 scale (matches H_Phantom_Brand_Persistence_heritage PARTIAL floor at 4/18 ≈ 22%). r1 retained in git history (tag `v0.22-prereg-r1` at commit `edc61f3`) for audit trail.

**Lock state:** `v0.22-prereg-r2` is the operative pre-registration lock for v0.22 acquisition.

### Part B — COI screen

**Screen result:** Three of the 24 brands in the locked v0.22 registry have tier-2/3 supply relationships with Samsung Electronics America (author's primary employer) via Samsung subsidiaries: BMW (Harman audio + Samsung SDI batteries + Samsung Display infotainment), Mercedes-Benz (Harman audio + Samsung Display infotainment), and Volkswagen Group brands including Bentley and Porsche (Samsung SDI battery supply to Stellantis-adjacent platforms). Tesla and Polestar also have tangential Samsung-component exposure at the parts level.

These are all tier-2/3 non-competitive supply relationships, not brand-level competition. Samsung Electronics America does not produce or market passenger car brands. The COI relationship does not affect brand recognition or recall measurement by LLM panel and does not impose operational restriction on registry composition.

**Disposition:** No deviation from pre-registration warranted. COI disclosed in §COI of the v0.22 SSRN paper per program standard.

**Lock state:** `v0.22-prereg-r2` unchanged by COI screen.

---

## Lock sequence

```bash
# v0.22 pre-reg r1 → r2 amendment already committed:
#   - commit edc61f3 = v0.22-prereg-r1 (single-model INSTRUMENT error)
#   - commit 0dde745 = v0.22-prereg-r2 (6-model panel corrected)
#   Both tags annotated; r2 supersedes r1.

# Push to origin (when ready)
cd ~/aias
git push origin program-docs
git push origin v0.22-prereg-r1
git push origin v0.22-prereg-r2

# OSF deposit of pre-reg artifacts
python3 ~/aias/scripts/osf_upload.py ~/aias/prereg v22/prereg
```

---

## Ship sequence (full cycle)

| # | Step | Builder fork source | Output |
|---|---|---|---|
| 1 | Pre-reg artifact (Python module) | drafted in chat; new pattern for v0.22 | `prereg/v0_22_automotive_content.py` |
| 2 | Pre-reg commit + r1 tag | — | commit `edc61f3`, tag `v0.22-prereg-r1` |
| 3 | Pre-reg r2 amendment + tag | INSTRUMENT correction | commit `0dde745`, tag `v0.22-prereg-r2` |
| 4 | Mega-prompt artifact | `v0_21_mega_prompt.md` → this file | `prereg/v0_22_mega_prompt.md` |
| 5 | OSF deposit pre-reg | `osf_upload.py` | `osf.io/ec6wh/v22/prereg/` |
| 6 | Run acquisition | `run_acquisition_v21.py` → `run_acquisition_v22.py` | Phase A + Phase B CSVs |
| 7 | Acquisition lock | — | `v0.22-acquisition-locked` |
| 8 | Run scoring | `score_v21.py` → `score_v22.py` | `v22_verdicts.json` |
| 9 | Build charts | `build_charts_v21.py` → `build_charts_v22.py` *(already done — 4 chart PDFs incl. chart_04_phantom_defunct)* | 4 chart PDFs at `figs/v22/` |
| 10 | Brand-format report | `build_report_v21.py` → `build_report_v22.py` *(already done)* + `v21_cosmetics_content.py` → `v22_automotive_content.py` *(post-acquisition)* | `v22_automotive.pdf` |
| 11 | SSRN paper | `v0_21_ssrn_paper_draft.md` → `v0_22_ssrn_paper_draft.md`; `build_paper_v0_21.py` → `build_paper_v0_22.py` | `v0_22_ssrn_paper.pdf` |
| 12 | SSRN submission packet | `ssrn_submission_packet_v0_21.md` → `ssrn_submission_packet_v0_22.md` | webform paste-ready |
| 13 | SSRN submission | manual | Abstract ID returned by SSRN |
| 14 | Final OSF deposit | `v21_osf_deposit.sh` → `v22_osf_deposit.sh` | `osf.io/ec6wh/v22/` |
| 15 | Memory backfill | `memory_user_edits` tool | recent_updates entry |

---

## Phase-copy build commands

Build triad (charts + report) is **already in place** from earlier in this v0.22 cycle:

- `scripts/build_charts_v22.py` (4 charts including chart_04_phantom_defunct) — committed at `cab9218`
- `reports/build_report_v22.py` — committed at `cab9218`

Remaining phase-copy commands:

```bash
# Step 6 acquisition runner
cp ~/aias/scripts/run_acquisition_v21.py ~/aias/scripts/run_acquisition_v22.py
# Edit: registry path (prereg/v0_22_automotive_content.py — import REGISTRY, PROBES, INSTRUMENT directly);
#   Phase A probe template (cosmetics → car); Phase B q1–q6 templates per §Phase B above;
#   add R_phantom_defunct unprompted-mention detection on Cell D brands across R_cat responses;
#   output CSV paths (acquisitions/v22_phase_a.csv, acquisitions/v22_phase_b.csv)

# Step 8 scorer
cp ~/aias/scripts/score_v21.py ~/aias/scripts/score_v22.py
# Edit: import prereg/v0_22_automotive_content.py for REGISTRY + HYPOTHESES + verdict criteria;
#   input CSVs from step 6; output verdicts.json at osf/v22/v22_verdicts.json;
#   add H_Phantom_Defunct scoring block per the locked operationalization;
#   add R_phantom_defunct and R_cult-channel phantom exploratory sub-test scoring;
#   four-cell adaptations throughout (C_P per-cell stats, Iwachu detection across 4 cells, etc.)

# Step 10 content module — POST-ACQUISITION
cp ~/aias/reports/v21_cosmetics_content.py ~/aias/reports/v22_automotive_content.py
# Edit all 11 attributes (COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED, PATTERNS,
#   LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING, HYPOTHESIS_DETAILS, CLOSING) with v0.22 facts
#   from v22_verdicts.json; 4 findings (vs v0.21's 3 — adds phantom_defunct as Finding 4)

# Step 11 SSRN paper
cp ~/aias/papers/v0_21/v0_21_ssrn_paper_draft.md ~/aias/papers/v0_22/v0_22_ssrn_paper_draft.md
cp ~/aias/reports/build_paper_v0_21.py ~/aias/reports/build_paper_v0_22.py
# Edit paper draft: title, abstract, methods (incl. r1 → r2 amendment in §Methods),
#   results, discussion — all with v0.22 facts

# Step 12 submission packet
cp ~/aias/papers/v0_21/ssrn_submission_packet_v0_21.md ~/aias/papers/v0_22/ssrn_submission_packet_v0_22.md
# Edit: title, abstract, keywords, citation, OSF path

# Step 14 deposit runner
cp ~/aias/scripts/v21_osf_deposit.sh ~/aias/scripts/v22_osf_deposit.sh
# Edit: version strings throughout
```

---

## Header right text

```
Phantom Brand Persistence · v0.22 · May 2026
```

*(Already locked in `build_report_v22.py` at `cab9218`.)*

## SSRN paper title (proposed)

```
Phantom Brand Persistence on a Heritage-Saturated Automotive Substrate — Cell D_Defunct as Pure-Phantom Upper-Bound Test
```

Subtitle:

```
AIAS™ Presence Measurement Protocol, v0.22 — Sixth substrate family for the Presence-component AIAS™ 1.0 anchor base; first prospective phase under v1.6 lock
```

(Adjust based on actual verdict if H_Phantom_Defunct returns PARTIAL or FALSIFIED — fallback titles in the SSRN packet template.)

---

## What comes after v0.22 — AIAS™ 2.0 component expansion arc

AIAS™ 1.0 (Presence-component) was released at SSRN 6817841 in May 2026, anchored on five substrate families (v0.16–v0.21) under v1.6 lock. v0.22 closes the **6th anchor family** for the Presence-component construct, primarily as a Phantom Brand Persistence stress-test — not as a new methodology phase.

After v0.22, the natural critical path is the **AIAS™ 2.0 component expansion** (the remaining five components beyond Presence):

1. **Ranking** — positional data already captured in Phase B Recall; minimal new acquisition shape required. Likely first 2.0 component to anchor.
2. **Consistency** — multi-session probing (re-run same probes across sessions, measure response variance). Different acquisition shape than Presence.
3. **Coverage** — grounding-source enumeration; Phase B-adjacent measurement.
4. **Grounding** — citation and source-attribution behavior; new probe types required.
5. **Sentiment** — affective valence in unprompted Recall; new probe types required.

Each component requires: operational definition (methodology paper increment) + at least one empirical phase to anchor + calibration / cross-component analysis against Presence.

A v1.7+ methodology paper could profitably specify the five remaining components' acquisition patterns *before* phase work begins, to avoid mid-phase scope drift. Estimated timeline: at one ship cycle per week, the full six-component composite is reachable in 4–6 months.

**Critical risk for the 2.0 arc:** Ranking and Coverage likely admit Presence-shaped acquisition. Consistency, Grounding, and Sentiment likely do not. Phase 1 (Ranking + Coverage) is therefore the natural 2.0 launch; Phases 2–3 will require methodology innovation beyond Presence's pattern.

---

## End of mega-prompt

This document is self-contained. To execute v0.22 from a fresh session, paste this document into context along with:

- `prereg/v0_22_automotive_content.py` (the locked Python pre-reg module; r2)
- v0.21 builder files (`build_report_v21.py`, `v21_cosmetics_content.py`, `build_charts_v21.py`, `score_v21.py`, `run_acquisition_v21.py`, `build_paper_v0_21.py`, `v0_21_ssrn_paper_draft.md`, `ssrn_submission_packet_v0_21.md`, `v21_osf_deposit.sh`)
- v0.22 build files already in place: `scripts/build_charts_v22.py`, `reports/build_report_v22.py` (committed at `cab9218`)

The AI executes the remaining ship sequence (steps 5–15), producing all artifacts and submitting to SSRN.

**Trademark notice:** AIAS™ and Third System™ are trademarks of the research program. First mention in each formal document carries ™; subsequent mentions unmarked.
