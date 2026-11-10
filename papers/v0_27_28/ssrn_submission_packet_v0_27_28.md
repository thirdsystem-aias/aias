# SSRN Submission Packet — AIAS™ v0.27.28

**Paper:** AI Brand Presence against a Commercial Visibility Score and Human Brand Norms
**File to upload:** `papers/v0_27_28/v0_27_28_ssrn_paper.pdf`
**Submission target:** SSRN — papers.ssrn.com → Submit a paper
**Date prepared:** November 2026

---

## Step 1 — Paper type

- **Working Paper**

## Step 2 — Document Settings

- **Document type:** Article
- **License:** All rights reserved
- **Display abstract:** Yes
- **Allow citations:** Yes
- **Allow downloads:** Yes

---

## Step 3 — Paper details

### Title (paste verbatim — SSRN has one Title field; subtitle folded in)

```
AI Brand Presence against a Commercial Visibility Score and Human Brand Norms: Two pre-registered construct-validity tests of the AIAS™ Presence component
```

### Subtitle (titlepage only — SSRN has no separate subtitle field; folded into Title above)

```
Two pre-registered construct-validity tests of the AIAS™ Presence component
```

### Abstract (paste verbatim — matches paper page 2)

```
AI availability, the propensity of a brand to be surfaced when people ask large language models about its category, is measured in the AIAS program by a Presence component built from model recognition and two recall channels. This paper reports two pre-registered construct-validity tests of Presence, first written up separately, with every hypothesis and verdict as locked and no new analysis. Study 1 (convergent; 24 B2B SaaS brands) correlated a recall-share form of Presence with the Share-of-Voice score of a commercial AI-visibility instrument, the HubSpot AEO Grader. The primary hypothesis was falsified (Spearman ρ = 0.29, 95% CI [−0.17, 0.64]); neither pre-specified sensitivity changed that. Model recognition sat at ceiling for every brand, confirming the recognition-null control. An exploratory scan found recall share tracking the instrument's presence-quality (ρ = 0.80) and brand-recognition (ρ = 0.75) subscores; the Share-of-Voice gap is one of rank alignment, not restricted range. Study 2 (discriminant; 24 Technology brands drawn by seeded stratified sampling) correlated blind-acquired Presence with human brand norms from the BRAND database. Presence was discriminant from recognition sensitivity d′ (ρ = 0.38; the BCa interval stays below the 0.74 reducibility threshold), so that hypothesis was confirmed. Against familiarity the point estimate (ρ = 0.59) fell in the partial band, but the BCa interval [0.18, 0.83] spanned all three pre-registered bands, and the locked rule returned undetermined. Because recognition was saturated in Study 1 and recall floored for most brands in Study 2, the two studies tested different facets of Presence: recall in the first, recognition in the second. Convergence with a commercial visibility score was not established, and the familiarity question remains open at n = 24.
```

### Keywords (paste verbatim, semicolon-separated)

```
AI availability; brand availability; AIAS; pre-registration; Ehrenberg-Bass; construct validity; convergent validity; discriminant validity; large language models; AI visibility tools; brand familiarity; recognition memory
```

### JEL codes (paste verbatim)

```
M31; L86; L15; D83; M37
```

**JEL rationale (for your reference):** M31 (primary); L86; L15; D83; M37

---

## Step 4 — Subject classifications (select up to 7)

Select these networks/eJournals on the SSRN classification picker:

1. **Marketing eJournal**
2. **Marketing Strategy eJournal**
3. **Consumer Behavior eJournal**
4. **Advertising & Marketing Communication eJournal**
5. **Information Systems eJournal**
6. **Artificial Intelligence eJournal**
7. **Decision-Making Under Risk & Uncertainty eJournal**

(Same classification set as v0.16–v0.21 papers for consistency.)

---

## Step 5 — Authors, affiliations, contact

```
Pablo Ulpiano González Castro

School of Visual Arts (SVA), MPS Branding Program
New York, NY, United States

Third System™ (research entity; data archive and methodology venue)
thirdsystem.ai

Email: pablou@pablou.com
Website: pablou.com
ORCID: 0009-0003-8968-9990
```

---

## Step 6 — Declarations (Conflict of Interest, Funding, Ethics)

### Declaration of Interest (paste verbatim)

```
The author is employed by Samsung Electronics America. Samsung had no role in the design, conduct, analysis or reporting of either study. Neither panel contains a Samsung-group brand: in Study 2, Harman International, a Samsung subsidiary, was removed from the eligible sampling frame by a pre-registered screen before the seeded draw. The Study 2 Technology panel includes brands that compete with Samsung in some product categories (Apple, Dell Technologies, Google, Microsoft, Seagate Technology, Whirlpool) and one brand in which a Samsung subsidiary holds a significant minority equity stake (Corning, in which Samsung Display is a shareholder); other panel brands may have supplier, customer or channel relationships with Samsung group companies. The panel was drawn by a fixed random seed within familiarity tertiles, and no brand was selected or excluded by the author after the screen. Study 1 evaluates commercial AI-visibility instruments; Cheil Worldwide, a Samsung affiliate, sells AI-visibility services. The author develops the AIAS measurement program through Third System. The author declares no other competing interests.
```

### Funder (paste verbatim)

```
Self-funded.
```

### Ethics statement (paste verbatim)

```
Not applicable; no human subjects.
```

(Edited after generation: the generator's constant on this branch adds "public APIs and LLM prompts only", which is not accurate here because Study 2 uses published human-norm data and Study 1 a public web tool; replaced with the CLAUDE.md packet-template wording. The paper's Ethics section carries the full statement.)

### Data and code availability (paste verbatim)

```
Data, scoring code and verdict files for both studies are deposited at OSF (osf.io/ec6wh). Study 1 is under v27: instrument and AIAS-side data, the 24-brand registry, scoring and figure code, the verdict file, the report and the earlier paper. Study 2 is under v28: the pre-registration content module and prompt, panel and validator files, raw and composed acquisition data, scoring code, the verdict file, the report and the earlier paper. Study 1's pre-registration content module and its revisions r1 to r5 are held in the program's git repository at tags v0.27-prereg-r1 to v0.27-prereg-r5 and are not yet in the OSF v27 folder. The Study 2 validator file reproduces 24 brands' familiarity and d′ values from the BRAND database (ResearchBox 1892, https://researchbox.org/1892), which is distributed under a CC BY 4.0 licence; reuse requires attribution to Raffaelli et al. (2025).
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_27_28/v0_27_28_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). AI Brand Presence against a Commercial Visibility Score and Human Brand Norms: Two pre-registered construct-validity tests of the AIAS™ Presence component. SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v0.27.28 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v2728 v2728`
4. **Cross-citation** in next phase: this v0.27.28 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v0.27.28 ready to upload.**
