# SSRN Submission Packet — AIAS™ v0.36

**Paper:** Does Cross-Platform Consistency Have Regime Structure?
**File to upload:** `papers/v0_36/v0_36_ssrn_paper.pdf`
**Submission target:** SSRN — papers.ssrn.com → Submit a paper
**Date prepared:** June 2026

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
Does Cross-Platform Consistency Have Regime Structure?: A Pre-Registered Clustering Test Against a Frozen Brand-Presence Classification
```

### Subtitle (titlepage only — SSRN has no separate subtitle field; folded into Title above)

```
A Pre-Registered Clustering Test Against a Frozen Brand-Presence Classification
```

### Abstract (paste verbatim — matches paper page 2)

```
Whether cross-platform consistency (CPC) — the uniformity of a brand's recall across large language models — carries diagnostic structure of its own, or merely reflects the brand-presence hierarchy, is an open question for AI-availability measurement. This study pre-registered a clustering test on fully frozen inputs: 112 brand-units across five consumer substrates, a fixed six-model panel, and the CV-based CPC characterization quantity assessed (and not adopted) by Protocol v1.7. Four hypotheses were locked before any statistic was computed: regime inheritance (H_RegimeInheritance), autonomous structure (H_RegimeAutonomy), residual structure after Presence removal (H_ResidualStructure), and saturation degeneracy (H_SaturationDegeneracy), with a four-cell verdict matrix predicting borrowed structure (Cell A). The result falsified the prediction: the phase landed in Cell D (unstructured). No hypothesis met its locked bar — inheritance was unevaluable at power after a CV computability floor removed 15 of 24 units in the label-bearing substrate; saturation reversed direction (saturated substrates exhibited greater CPC dispersion, Levene p = .003); omnibus structure (k = 3) fell just short of the silhouette threshold (0.2422 vs 0.25); and structure emerged only in a sensitivity arm that removed mean recall entirely. The failure modes converge on mean-coupling pathology in the CV instrument, motivating the v1.8 mean-independent specification. Pre-scoring amendments — three corrections (data-lineage, construct-identity, and scope-assignment) and a recognition-commensurability finding — are documented in the deposited record.
```

### Keywords (paste verbatim, semicolon-separated)

```
brand availability; large language models; cross-platform consistency; pre-registration; cluster analysis; construct validity; measurement; AI Availability; Ehrenberg-Bass; AIAS
```

### JEL codes (paste verbatim)

```
M31; L86; L15; D83; M37
```

**JEL rationale (for your reference):** M31; L86; L15; D83; M37

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
The author is employed full-time as Director, Corporate Brand Creative and Governance, at Samsung Electronics America. v0.36 reuses the v0.19–v0.23 registries and inherits their conflict-of-interest screen (pre-registration DEVIATIONS Entry 2). Samsung subsidiaries hold tier-2/3 component supply relationships with several brands in the reused registries: Harman International (audio systems), Samsung SDI (battery cells), and Samsung Display (infotainment). These are non-competitive supply relationships; Samsung Electronics America does not produce or market passenger car brands and has no brand-level competitive overlap with any registry entry. No operational restriction on registry composition was imposed. Separately, AKG was substituted with Denon before the v0.19 pre-registration lock (AKG owned by Harman International, a Samsung subsidiary, since 2016) to avoid any appearance of conflict; the substitution preserved Cell A_Heritage's eight-brand composition, occurred prior to lock, and was AKG only (not JBL). Samsung had no role in study design, analysis, or reporting. The author's primary academic affiliation for this research is the School of Visual Arts MPS Branding Program; the research entity maintaining the data archive and methodology venue is Third System™.
```

### Funder (paste verbatim)

```
Self-funded.
```

### Ethics statement (paste verbatim)

```
Not applicable; no human subjects; public APIs and LLM prompts only.
```

### Data and code availability (paste verbatim)

```
All pre-registration artifacts (tags `v0.36-prereg-r1`, `r2`, `r3`), the verdicts file, clustering intermediates, figures, the brand-format report, and the scoring code are deposited at osf.io/ec6wh (v36/). The CPC inputs originate in the v0.31 phase and are consumed as archived data via that phase's OSF deposit; the v0.31 SSRN abstract is withdrawn and is not cited as methodological authority. The regime target and Presence composite are read as frozen fields from the v0.23 deposit. Upstream phase and methodology papers are indexed in the cross-citation registry (see `_upstream_phases.md`).
```

---

## Step 7 — Final review & upload

- **File:** `papers/v0_36/v0_36_ssrn_paper.pdf`
- **Cover letter:** Not required for SSRN Working Paper submissions.
- **Suggested citation (post-submission, fill in SSRN abstract ID):**

```
González Castro, P. U. (2026). Does Cross-Platform Consistency Have Regime Structure?: A Pre-Registered Clustering Test Against a Frozen Brand-Presence Classification. SSRN Working Paper [ABSTRACT_ID].
```

---

## Post-submission checklist

1. **Capture SSRN abstract ID** when SSRN returns it (URL format: `https://ssrn.com/abstract={ID}`).
2. **Update memory:** add the v0.36 SSRN abstract ID entry to the recent_updates section of userMemories.
3. **Run final OSF deposit:** `python3 ~/aias/scripts/osf_upload.py ~/aias/osf/v36 v36`
4. **Cross-citation** in next phase: this v0.36 SSRN ID gets added to next phase's paper bibliography upstream-phases line.

---

**End of submission packet — v0.36 ready to upload.**
