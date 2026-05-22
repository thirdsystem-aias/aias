# SSRN Submission Packet — v0.20

**Target:** papers.ssrn.com webform submission
**Paper PDF:** `~/aias/papers/v0_20/v0_20_ssrn_paper.pdf`
**Lock state at submission:** `v0.20-prereg-r1` (commit `4e5ab60`), `v0.20-acquisition-locked`

Work through the webform top-to-bottom; each section below maps to the corresponding webform step.

---

## Step 1 — Title

Paste-ready (single line):

```
Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate
```

Subtitle field (if SSRN exposes one):

```
AIAS™ Presence Measurement Protocol, v0.20 — Type 2 Quadrant Populated; v1.5 C2 First Prospective Calibrated
```

If subtitle field is unavailable, append to title with em-dash:

```
Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate — AIAS™ Presence Measurement Protocol, v0.20
```

---

## Step 2 — Authors

Single-author submission. Use the AIAS standard author block:

| Field | Value |
|---|---|
| First name | Pablo |
| Middle name | Ulpiano |
| Last name | González Castro |
| Email | pablou@pablou.com |
| ORCID | 0009-0003-8968-9990 |
| Primary affiliation | School of Visual Arts, MPS Branding Program, New York, NY |
| Secondary affiliation | Third System™ (research entity; data archive and methodology venue) |

**Reminder:** Samsung Electronics America goes in Declarations §COI only, never the author block.

---

## Step 3 — Abstract, Keywords, JEL

### Abstract (paste in full)

The AIAS™ Presence Measurement Protocol operationalizes AI Availability — the brand-level probability of retrieval, recommendation, or selection by an AI intermediary — as a measurable construct alongside Ehrenberg-Bass Mental Availability and Physical Availability. Protocol v1.5 (SSRN 6810758) closed the methodology layer for v1.4's multi-component Recognition × Recall construct by adding a C2 multi-statistic adequacy rule (distinct C_P values ≥ 3 ∧ modal share ≤ 0.625) and a two-channel Recall decomposition (R_cat for category-canonical retrieval, R_cult for cultural-footprint retrieval). v1.5's §6 flagged three open items: Type 2 cases (the cultural-channel-preferred quadrant) had not yet been empirically populated; the C2 rule had been calibrated retrospectively against joint v0.18 + v0.19 data but never tested prospectively; and the cumulative anchor base for the multi-component construct spanned only three substrate families. This paper reports v0.20, the first prospective phase pre-registered against the v1.5 thresholds, and the first acquisition to test the construct on a fourth substrate family.

The substrate is indie- and prestige-segmented skincare, sampled across three cells stratified by Identity Load on the consumer-discovery surface: Cell A (prestige, medium IL), Cell B (celebrity-DTC, high IL — the Type 2 hunting cell), and Cell C (clinical / dermatologist-recommended, low IL). Each cell carries 8 brands; worldwide n = 24 pre-floor. The reference panel is the locked six-slot v0.17 panel. Phase B uses a six-frame battery splitting cleanly across the v1.5 channels: q1–q3 anchor R_cat (best, dermatologist-recommended, effective); q4–q6 anchor R_cult (popular, celebrity, viral/cult). Four pre-registered hypotheses are tested orthogonally.

The four hypotheses returned heterogeneous verdicts. H_Type2_emergence — the primary novel hypothesis for v0.20 — returned PARTIAL with two Type 2 cases in Cell B (Glossier and Rhode, with Augustinus Bader at the threshold boundary), populating the v1.5 dissociation framework's third quadrant for the first time. H_Regime4_skincare, the first prospective exercise of v1.5 C2, returned FALSIFIED with C2 failures in two of three cells: Cell C fully saturated (modal C_P share = 1.000, distinct = 1 — the predicted Cell C cascade-saturation pattern) and Cell A failing on bimodal C_P distribution. Cell B passed C2 cleanly. H_Dissociation_substrate_generalization returned GENERALIZED, with Iwachu-pattern cases distributed across all three cells; the v1.4/v1.5 multi-component construct is now anchored across four substrate families. H_IdentityLoad_moderator (4-leg joint) returned NARROWED, driven by the v0.20 H_Regime4 falsification; the substantive IL channel asymmetry (Cell C R_cat-dominant 10.88 vs. R_cult 8.38; Cell B R_cult-dominant 5.38 vs. R_cat 1.62) remains visible in the raw data and is discussed as a substrate-specific moderator signature beneath the joint verdict.

For AIAS™ 1.0's foundational construct, v0.20's headline contribution is the empirical population of the Type 2 quadrant — the construct's three-quadrant dissociation framework is no longer hypothetical. The pre-registration discipline (commit 4e5ab60, tag v0.20-prereg-r1, deposited at osf.io/ec6wh/v20/) locks panel, hypotheses, decision rules, and verdict matrices ex-ante, with the v1.5 numerical thresholds locked at pre-reg r1 — the first phase to do so prospectively.

### Keywords (semicolon-separated, paste verbatim)

```
AI availability; brand availability; Type 2 dissociation; cultural-footprint Recall; Identity Load; skincare; LLM mediation; pre-registration; Spearman bootstrap; Ehrenberg-Bass; AIAS
```

### JEL Classifications (semicolon-separated)

```
M31; L86; L15; D83; M37
```

JEL code reference:
- **M31** — Marketing (primary)
- **L86** — Information and Internet Services
- **L15** — Information and Product Quality; Standardization and Compatibility
- **D83** — Search; Learning; Information and Knowledge
- **M37** — Advertising

---

## Step 4 — Subject Classifications (up to 7)

Select these eJournals from the SSRN subject browser:

1. **Marketing eJournal**
2. **Marketing Strategy eJournal**
3. **Consumer Behavior eJournal**
4. **Advertising & Marketing Communications eJournal**
5. **Information Systems & eBusiness eJournal**
6. **Artificial Intelligence eJournal**
7. **Decision-Making Under Risk & Uncertainty eJournal**

---

## Step 5 — Declarations

### Declaration of Interest (paste in full)

The author is employed by Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS™ Presence Measurement Protocol and the work reported here are the author's independent academic research, conducted outside the scope of employment, in the author's role as faculty at the School of Visual Arts MPS Branding Program and founder of Third System™. Samsung had no role in the design, execution, analysis, or interpretation of this work. None of the 24 brands in the v0.20 registry is affiliated with Samsung Electronics America (pre-acquisition COI screen documented as DEVIATIONS Entry 0).

### Funder

```
Self-funded
```

### Ethics

```
Not applicable; no human subjects. The research uses publicly accessible LLM APIs queried with non-personal, category-anchored prompts.
```

### Data and Code Availability (paste in full)

All pre-registration artifacts, acquisition data, scoring code, and verdict outputs are deposited under Open Science Framework project ec6wh at osf.io/ec6wh/v20/. The pre-registration is locked at commit 4e5ab60 on git tag v0.20-prereg-r1, branch v0.20-skincare-il-gradient. The acquisition is locked at git tag v0.20-acquisition-locked. All four hypothesis verdict matrices are specified ex-ante in prereg/v0_20_registry.json.

### Trademark Notice

```
AIAS™ and Third System™ are trademarks of the research program.
```

---

## Step 6 — File Upload

Upload:

```
~/aias/papers/v0_20/v0_20_ssrn_paper.pdf
```

Pre-flight before upload:

- [ ] PDF renders cleanly (titlepage on one page; §3.5 C2 table check/cross marks render correctly; all three charts embedded inline at §3.1 / §3.4 / §3.4)
- [ ] No tofu glyphs (▢) anywhere
- [ ] No line overflows past margin
- [ ] Author block does NOT mention Samsung
- [ ] Declarations §COI DOES mention Samsung
- [ ] All cited SSRN IDs in references resolve (6659000, 6761698, 6797679, 6799479, 6810758, 6791999, 6802261, 6806558, 6809182)

---

## Step 7 — Submit

Click submit. SSRN will assign an abstract ID within 1–3 business days (typically same day for established authors).

---

## Post-Submission Backfill

Once SSRN returns the abstract ID:

1. **Update memory.** Append to the userMemories recent_updates section:
   ```
   AIAS v0.20 Skincare SSRN abstract ID: {NEW_ID} (Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate, May 2026). Verdicts: H_Type2_emergence PARTIAL (2 Cell B cases: Glossier, Rhode); H_Regime4_skincare FALSIFIED (Cell C saturation, Cell A bimodal); H_Dissociation_substrate_generalization GENERALIZED (3 of 3 cells); H_IdentityLoad_moderator (4-leg joint) NARROWED. Pre-reg tag v0.20-prereg-r1 at commit 4e5ab60. OSF: osf.io/ec6wh/v20/. v1.5 first prospective phase. Cumulative anchor base now 4 substrate families.
   ```

2. **Update bibliography in dependent papers.** Add v0.20 SSRN ID to:
   - Tri-System MSI working paper (cross-cite v0.20 alongside v0.13, v0.14, methodology paper)
   - Future AIAS phase papers (v0.21+) will cite v0.20 as the Type 2 anchor

3. **OSF deposit final artifacts.** After SSRN assigns ID, deposit at `osf.io/ec6wh/v20/`:
   ```bash
   # Charts
   python ~/aias/scripts/osf_upload_v2.py ~/aias/reports/figs/v20 v20/figures
   
   # SSRN paper PDF
   python ~/aias/scripts/osf_upload_v2.py ~/aias/papers/v0_20 v20/paper
   
   # Verdicts JSON (already inside ~/aias/osf/v20)
   # If not yet deposited:
   python ~/aias/scripts/osf_upload_v2.py ~/aias/osf/v20 v20/scoring
   ```

4. **Brand-format report.** Per the ship sequence (step 8 — still pending), the Third System brand-format managerial PDF is the remaining deliverable for the v0.20 cycle. Build that after the SSRN submission is in flight.

---

## Quick Reference Card

| Field | Value |
|---|---|
| Title | Type 2 Emergence and First Prospective v1.5 C2 Calibration on a Skincare IL-Gradient Substrate |
| Subtitle | AIAS™ Presence Measurement Protocol, v0.20 — Type 2 Quadrant Populated; v1.5 C2 First Prospective Calibrated |
| Primary JEL | M31 |
| Primary eJournal | Marketing eJournal |
| Pre-reg tag | v0.20-prereg-r1 |
| Commit | 4e5ab60 |
| OSF path | osf.io/ec6wh/v20/ |
| Headline finding | Type 2 quadrant empirically populated (Glossier, Rhode in Cell B) |
| Cumulative anchor base post-v0.20 | 4 substrate families |
