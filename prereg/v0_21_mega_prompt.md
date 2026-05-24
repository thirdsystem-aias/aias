# AIAS Presence Measurement Protocol — v0.21 Mega-Prompt

**Phase identifier:** v0.21
**Substrate:** Cosmetics (drugstore-to-celebrity-DTC IL gradient)
**Phase position:** Fifth substrate family for the Presence-component AIAS™ 1.0 anchor base; pursues Type 2 EMERGED verdict (v0.20 returned PARTIAL at Cell B count = 2; v0.21 hunts for ≥ 3)
**Protocol version:** v1.5 (unchanged from v0.20 — no methodology increment in v0.21)
**Builder fork sources:** v0.20 (`build_report_v20.py`, `v20_skincare_content.py`, `build_charts_v20.py`, `score_v20.py`, `run_acquisition_v20.py`)

---

## Strategic context

v0.20 (Skincare, SSRN 6811441) returned H_Type2_emergence = PARTIAL with two Cell B cases (Glossier R_cult=9, Rhode R_cult=8) and one boundary case (Augustinus Bader R_cat=2). PARTIAL routes to the 1–2 band; EMERGED requires ≥ 3 clean cases.

Cosmetics is the canonical follow-up substrate for two reasons. **First**, the celebrity-DTC tier is structurally more populous than skincare's: Rare Beauty, Fenty Beauty, Haus Labs, Kylie Cosmetics, Huda Beauty, Pat McGrath Labs, Charlotte Tilbury, Anastasia Beverly Hills — eight viable Cell B brands without reaching. **Second**, Rare Beauty failed Phase A in v0.20 (C_P = 0/6, "skincare brand?" probe) because its primary LLM-corpus identity is cosmetics, not skincare. In v0.21 it should clear C_P readily, demonstrating that the v0.20 Recognition failure was substrate-anchor mismatch, not brand absence.

v0.21 also extends the Recognition × Recall dissociation construct to a fifth substrate family, closing the cross-substrate generalization claim for AIAS™ 1.0's headline narrative.

---

## Pre-registration design

### Substrate operational definition

Cosmetics is operationally defined as a three-cell IL-gradient panel spanning the makeup / decorative-cosmetics consumer-discovery surface, sampled across three tiers of Identity Load:

- **Cell A — Prestige (medium IL).** Counter brands at department stores; status acquisition partially performed through brand association.
- **Cell B — Celebrity DTC / cult (high IL).** Founder- or celebrity-identity brands where brand identity is part of the product signal. **Type 2 hunting cell.**
- **Cell C — Drugstore / mass (low IL).** Functional purchases where brand identity is separable from product identity.

The IL stratification is monotonic C → A → B (low → medium → high). The C → B span matches v0.20's design and remains wider than v0.18/v0.19.

### Locked brand registry (n = 24)

```
Cell A — Prestige (medium IL):
  1. MAC Cosmetics
  2. NARS
  3. Bobbi Brown
  4. Tom Ford Beauty
  5. Giorgio Armani Beauty
  6. Hourglass
  7. Chantecaille
  8. Laura Mercier

Cell B — Celebrity DTC / cult (high IL) [Type 2 hunting cell]:
  1. Rare Beauty (Selena Gomez)
  2. Fenty Beauty (Rihanna)
  3. Haus Labs (Lady Gaga)
  4. Pat McGrath Labs
  5. Charlotte Tilbury
  6. Huda Beauty
  7. Kylie Cosmetics
  8. Anastasia Beverly Hills

Cell C — Drugstore / mass (low IL):
  1. Maybelline
  2. L'Oréal Paris
  3. CoverGirl
  4. Revlon
  5. NYX Professional Makeup
  6. e.l.f. Cosmetics
  7. Wet n Wild
  8. Milani Cosmetics
```

**Borderline classifications (locked ex-ante):**
- Pat McGrath Labs / Charlotte Tilbury: founder-makeup-artist identity at prestige price-point. Cell B per founder-identity primary classifier.
- e.l.f. Cosmetics: drugstore price-point with cult following. Cell C per drugstore-distribution primary classifier; flagged for retrospective dissociation review if Type 2 boundary case.
- NYX Professional Makeup: drugstore distribution with semi-professional positioning. Cell C.
- Tom Ford Beauty / Giorgio Armani Beauty: prestige beauty under luxury parent houses. Cell A per counter-distribution primary classifier (avoiding the v0.20 Cell A bimodality risk — both are primary-cosmetics identities in LLM corpora, unlike skincare's Dior Beauty / Chanel Beauty which were primarily fragrance/cosmetics houses with skincare extensions).

**Per-cell alternates (for DEVIATIONS cascade, ordered):**
- Cell A: Smashbox, Urban Decay, Too Faced
- Cell B: Florence by Mills, Flower Beauty (Drew Barrymore), Selena Gomez's other ventures excluded
- Cell C: Almay, Physicians Formula, Black Radiance

### Reference panel (locked, unchanged from v0.17)

```
- claude-opus-4-5
- claude-sonnet-4-5
- gpt-4o
- gpt-4o-mini
- gemini-2.5-flash
- gemini-2.5-flash-lite
```

### Phase A — Recognition probe

For each of the 24 brands, send to each of the 6 panel models:

```
Is the brand {BRAND} commonly recognized as a cosmetics brand? Answer yes or no.
```

Per-brand C_P score = count of yes responses across the panel (range 0–6).

Pivot cascade follows v1.5 §6.4: first brand in cascade order achieving C_P = 6/6 becomes cell pivot; cascade exhaustion documented per v0.20 DEVIATIONS Entry 1 precedent.

### Phase B — six-frame battery (two-channel Recall)

**R_cat channel (q1–q3, canonical retrieval):**

- **q1 (best):** *What are the best cosmetics brands? List several with descriptions.*
- **q2 (professional):** *What makeup brands do professional makeup artists recommend? Name several.*
- **q3 (high-quality):** *What cosmetics brands are highest quality and most reliable? Name several brands with descriptions.*

**R_cult channel (q4–q6, cultural-footprint retrieval):**

- **q4 (popular):** *What cosmetics brands are popular right now? List several.*
- **q5 (celebrity):** *What makeup brands do celebrities and influencers use? Name several.*
- **q6 (cult/viral):** *What viral or cult-favorite makeup brands have gained big followings? Name several.*

Per-brand R_cat = sum across (q1, q2, q3) × 6 models = max 18.
Per-brand R_cult = sum across (q4, q5, q6) × 6 models = max 18.

Brand-mention detection per v1.4 canonical rules (case-insensitive, accent-stripped, possessive-aware, first-occurrence-wins de-duplication).

---

## Hypotheses (locked, four — orthogonal)

### H_Type2_EMERGED_cosmetics (PRIMARY, novel — pursues v0.20's PARTIAL)

Type 2 cases (R_cat ≤ 2 ∧ R_cult ≥ 5) emerge in Cell B at post-attrition n ≥ 5.

| Cell B Type 2 cases | Verdict |
|---|---|
| ≥ 3 | **EMERGED** ← primary v0.21 target |
| 1–2 | PARTIAL (matches v0.20) |
| 0 (panel adequate) | FALSIFIED |
| Cell B n < 5 | UNDETERMINED |

### H_Regime4_cosmetics (within-phase substantive)

Sequential C1 → C2 → IL-gradient guard → C3 per Protocol v1.5:

- **C1:** post-attrition worldwide n ≥ 12
- **C2 (v1.5 multi-statistic, per cell):** distinct C_P values ≥ 3 ∧ modal C_P share ≤ 0.625
- **IL-gradient guard:** Cell B top-2 R_cat share − Cell C top-2 R_cat share ≥ 0.10
- **C3:** per-cell Spearman ρ between C_P and R_cat ≥ 0.50 in ≥ 2 of 3 cells (n ≥ 5)

Routing: C2 failure in ≥ 2 cells → FALSIFIED; in 1 cell → PARTIAL; subsequent failures → PARTIAL; all clear → CONFIRMED.

### H_Dissociation_substrate_generalization_5th_family

Iwachu-pattern cases (C_P ≥ 5 ∧ R_cat ≤ 2) appear in ≥ 2 of 3 cells.

| Cells with Iwachu cases | Verdict |
|---|---|
| 3 of 3 | GENERALIZED (matches v0.20) |
| 2 of 3 | GENERALIZED |
| 1 of 3 | PARTIAL |
| 0 | NARROWED |

This is the **fifth-substrate-family closer** for the Presence-component AIAS™ 1.0 anchor base. GENERALIZED here completes the cross-substrate generalization claim.

### H_IdentityLoad_moderator (5-leg joint, descriptive)

Joint verdict over v0.16 × v0.17 × v0.18 × v0.20 × v0.21. v0.19 still excluded (uniform-IL design). Joint matrix unchanged from v0.20 pre-reg §6.4.

---

## Substantive predictions (descriptive, for §3 narrative pre-loading)

**Cell A — Prestige.** Expected near-saturated C_P (~5.5–6.0/6 mean): all eight brands are primary-cosmetics identities in LLM corpora, no fragrance/skincare-extension dilution. **Variance prediction: low to moderate.** Risk: Cell A could fully saturate similar to v0.20 Cell C, with v1.5 C2 rejection. The Tom Ford Beauty / Armani Beauty / Hourglass / Chantecaille tail should provide some variance (modal share likely 0.625–0.750).

**Cell B — Celebrity DTC.** Expected variance-rich C_P distribution (mean ~4.5–5.5/6): celebrity-founder brands should be well-recognized (Rare Beauty, Fenty Beauty, Charlotte Tilbury, Huda Beauty all near saturation), with possible C_P drop for newer or smaller-presence brands (Haus Labs, Kylie Cosmetics at moderate). **This is the variance-rich cell v1.5 C2 was designed for; pass expected.**

**Cell C — Drugstore.** Expected near-saturation similar to v0.20's Clinical cell: Maybelline / L'Oréal Paris / CoverGirl / Revlon / NYX all heavily represented in LLM corpora as cosmetics brands. **v1.5 C2 likely rejects on saturation.** This is acceptable: primary v0.21 verdict (H_Type2) does not depend on H_Regime4 clearing.

**Recall predictions:**
- **Cell A R_cat:** high, distributed (MAC, NARS, Charlotte Tilbury [if classified A], Bobbi Brown, Laura Mercier — broad coverage in canonical "best" frames)
- **Cell B R_cat:** moderate to high (Fenty Beauty especially — its product-quality reputation is independent of celebrity status); Rare Beauty, Charlotte Tilbury, Pat McGrath Labs likely substantial
- **Cell C R_cat:** very high, near-saturated (drugstore brands dominate canonical lists)
- **Cell A R_cult:** low to moderate (prestige cosmetics surface in celebrity coverage but not as cult/viral)
- **Cell B R_cult:** very high (the hunting target — celebrity-founder brands should saturate cultural frames)
- **Cell C R_cult:** moderate (e.l.f. especially — cult-drugstore positioning)

**Type 2 case projections (R_cat ≤ 2 ∧ R_cult ≥ 5):**
- **Strong Type 2 candidates:** Haus Labs (Lady Gaga's brand is heavily celebrity-coded; canonical-frame Recall may be sparse despite full Recognition), Kylie Cosmetics (similar — Kylie Jenner brand identity dominates cultural-frame discourse), Huda Beauty (founder-celebrity / Instagram-native cult).
- **Boundary cases:** Rare Beauty, Charlotte Tilbury (both have substantial canonical-channel reputation in addition to cultural footprint, so may not cross the R_cat ≤ 2 threshold).
- **Predicted Cell B Type 2 count:** 3–4. EMERGED verdict probable but not guaranteed.

---

## DEVIATIONS Entry 0 — Pre-acquisition COI screen

**Date:** [acquisition date]
**Screen subject:** Samsung Electronics America (author's primary employer) potential exposure to v0.21 registry.
**Screen result:** None of the 24 brands in the locked registry is affiliated with Samsung. Samsung Harman International (audio acquisition) has no cosmetics exposure; Samsung Cheil Industries' historical beauty/cosmetics activities (Hera, IOPE, Mamonde, Sulwhasoo, Espoir under Amorepacific licensing) were divested pre-2018 and have no current overlap with the v0.21 registry.
**Disposition:** No deviation from pre-registration warranted.
**Lock state:** `v0.21-prereg-r1` unchanged.

---

## Lock sequence

```bash
# Pre-reg lock at git commit (no remote push yet — review first)
cd ~/aias
git checkout -b v0.21-cosmetics-il-gradient
git add prereg/v0_21_prereg.md prereg/v0_21_registry.json
git commit -m "v0.21 pre-registration: cosmetics IL-gradient, Type 2 EMERGED pursuit"
git tag v0.21-prereg-r1
git push -u origin v0.21-cosmetics-il-gradient
git push --tags

# OSF deposit of pre-reg artifacts
python3 ~/aias/scripts/osf_upload_v2.py ~/aias/prereg v21/prereg
```

---

## Ship sequence (full cycle)

| # | Step | Builder fork source | Output |
|---|---|---|---|
| 1 | Pre-reg artifact | v0.20 prereg as template | `v0_21_prereg.md`, `v0_21_registry.json` |
| 2 | Git commit + tag | — | commit hash, `v0.21-prereg-r1` |
| 3 | OSF deposit pre-reg | `osf_upload_v2.py` | `osf.io/ec6wh/v21/prereg/` |
| 4 | Run acquisition | `run_acquisition_v20.py` → `run_acquisition_v21.py` | Phase A + Phase B CSVs |
| 5 | Acquisition lock | — | `v0.21-acquisition-locked` |
| 6 | Run scoring | `score_v20.py` → `score_v21.py` | `v21_verdicts.json` |
| 7 | Build charts | `build_charts_v20.py` → `build_charts_v21.py` | 3 chart PDFs at `figs/v21/` |
| 8 | Brand-format report | `build_report_v20.py` → `build_report_v21.py`; `v20_skincare_content.py` → `v21_cosmetics_content.py` | `v21_cosmetics.pdf` |
| 9 | SSRN paper | `v0_20_ssrn_paper_draft.md` → `v0_21_ssrn_paper_draft.md`; `build_paper_v0_20.py` → `build_paper_v0_21.py` | `v0_21_ssrn_paper.pdf` |
| 10 | SSRN submission packet | `ssrn_submission_packet_v0_20.md` → `ssrn_submission_packet_v0_21.md` | webform paste-ready |
| 11 | SSRN submission | manual | Abstract ID returned by SSRN |
| 12 | Final OSF deposit | `v20_osf_deposit.sh` → `v21_osf_deposit.sh` | `osf.io/ec6wh/v21/` |
| 13 | Memory backfill | `memory_user_edits` tool | recent_updates entry |

---

## Phase-copy build commands

```bash
# Step 4 acquisition runner
cp ~/aias/scripts/run_acquisition_v20.py ~/aias/scripts/run_acquisition_v21.py
# Edit: REGISTRY_PATH, PHASE_A_PROBE, PHASE_B_FRAMES, output CSVs

# Step 6 scorer
cp ~/aias/scripts/score_v20.py ~/aias/scripts/score_v21.py
# Edit: registry, input CSVs, output verdicts.json path; hypothesis IDs and verdict matrices

# Step 7 charts
cp ~/aias/reports/build_charts_v20.py ~/aias/reports/build_charts_v21.py
# Edit: input verdicts.json, output figs/v21/, chart filenames

# Step 8 brand-format report (TWO files per the canonical fork pattern)
cp ~/aias/reports/build_report_v20.py ~/aias/reports/build_report_v21.py
cp ~/aias/reports/v20_skincare_content.py ~/aias/reports/v21_cosmetics_content.py
# Edit build script: docstring, content import, HERO_FIGURE_CAPTIONS, _slot_lookup figsize keys,
#   header right text ("Type 2 EMERGED Pursuit · v0.21 · [month] 2026"),
#   citation, output filename, deposit root, REPORT_PROTOCOL_VERSION stays v1.5
# Edit content module: all 11 attributes with v0.21 facts

# Step 9 SSRN paper
cp ~/aias/papers/v0_20/v0_20_ssrn_paper_draft.md ~/aias/papers/v0_21/v0_21_ssrn_paper_draft.md
cp ~/aias/reports/build_paper_v0_20.py ~/aias/reports/build_paper_v0_21.py
# Edit paper draft: title, abstract, methods, results, discussion — all with v0.21 facts

# Step 10 submission packet
cp ~/aias/papers/v0_20/ssrn_submission_packet_v0_20.md ~/aias/papers/v0_21/ssrn_submission_packet_v0_21.md
# Edit: title, abstract, keywords, citation, OSF path

# Step 12 deposit runner
cp ~/aias/scripts/v20_osf_deposit.sh ~/aias/scripts/v21_osf_deposit.sh
# Edit: version strings throughout
```

---

## Header right text

```
EMERGED Pursuit · v0.21 · [month] 2026
```

## SSRN paper title (proposed)

```
Type 2 EMERGED on a Cosmetics IL-Gradient Substrate — Fifth Substrate Family for the Presence-Component AIAS™ 1.0 Anchor Base
```

Subtitle:

```
AIAS™ Presence Measurement Protocol, v0.21 — Cell B Type 2 count clears EMERGED threshold; cross-substrate generalization closed
```

(Adjust based on actual verdict if Type 2 returns PARTIAL or FALSIFIED — fallback titles in the SSRN packet template.)

---

## What comes after v0.21 (AIAS 1.0 Presence-component critical path)

The remaining work to lock Presence-component AIAS™ 1.0 after v0.21 ships:

1. **Protocol v1.6 increment** (~1–2 days). Moderator-evaluation pathway evaluable independently of Regime 4's C2 conditions — a direct test of channel-mean asymmetry across cells with bootstrap CIs on the asymmetry estimate. Methodology paper only; no new empirical acquisition unless v1.6 specifies a re-analysis of v0.16–v0.21 data under the new rule.

2. **Synthesis paper** (~3–5 days). "The AIAS™ Presence-Component Construct: Cross-Substrate Generalization Across Five Substrate Families." Consolidating four-regime taxonomy, multi-component Recognition × Recall, two-channel Recall decomposition, three-quadrant dissociation framework, and the v0.16–v0.21 anchor base into a single canonical reference paper. Longer than a phase paper; no new data.

3. **AIAS™ 1.0 release packaging** (~1–2 days). Third System brand site update (thirdsystem.ai), OSF release tag, public-facing summary deck, possibly a JAR-targeted short-form companion to the Tri-System paper.

With v0.21 at one day, v1.6 at one day, synthesis at three days, and packaging at one day, **the Presence-component AIAS™ 1.0 release is on the order of 5–6 calendar days from v0.21 start.**

---

## After Presence-component release — path to full six-component AIAS™

Five remaining components (Ranking, Consistency, Coverage, Grounding, Sentiment). Each requires:

- Operational definition (methodology paper increment)
- At least one empirical phase to anchor the component on real LLM data
- Calibration / cross-component analysis against Presence (now well-anchored from v0.16–v0.21)

If each component takes one methodology paper + one anchor phase + one brand-format report = ~3 ship cycles per component × 5 components = **~15 ship cycles for the full six-component composite.** At one cycle per day, that's ~3 weeks. At a more sustainable two cycles per week, ~7–8 weeks. Either way, the full composite is reachable inside the "few months" window if Presence's tooling (acquisition runners, scorers, builders) carries forward as templates for the other five components.

**Critical risk:** the new five components may not all admit the same acquisition pattern as Presence. Ranking probably does (it's directly downstream of Recall — just record positional data already in Phase B responses). Coverage probably does (grounding-source enumeration is a Phase B-adjacent measurement). Consistency requires multi-session probing (re-running the same probe across sessions and measuring response variance) — different acquisition shape. Grounding and Sentiment may need new probe types not yet specified.

A v1.6+ methodology paper could profitably specify the five remaining components' acquisition patterns *before* phase work begins, to avoid mid-phase scope drift.

---

## End of mega-prompt

This document is self-contained. To execute v0.21 from a fresh session, paste this document into context along with the v0.20 builder files (`build_report_v20.py`, `v20_skincare_content.py`, `build_charts_v20.py`, `score_v20.py`, `run_acquisition_v20.py`, `build_paper_v0_20.py`, `v0_20_ssrn_paper_draft.md`, `ssrn_submission_packet_v0_20.md`, `v20_osf_deposit.sh`). The AI executes the full 13-step ship sequence, producing all artifacts and submitting to SSRN.

**Trademark notice:** AIAS™ and Third System™ are trademarks of the research program. First mention in each formal document carries ™; subsequent mentions unmarked.
