# v1.3 SSRN Submission Package

Copy-paste targets for each SSRN submission step. Title and abstract are byte-identical to the paper PDF; keywords and classifications are SSRN-formatted (semicolon-separated, multi-select). Once submitted, return the SSRN abstract ID to the userMemories registry.

---

## Step 1 — Title

```
The AIAS Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)
```

Note: SSRN title fields don't render trademark glyphs reliably across export targets. The ™ on AIAS is preserved in the PDF but omitted from the SSRN title field. SSRN's title-search indexing is improved by the absence of glyph noise.

---

## Step 2 — Author block

**Author name:** Pablo Ulpiano González Castro

**Affiliations:**
- School of Visual Arts, MPS Branding Program (primary academic affiliation)
- Third System (research entity; data archive and methodology venue)

**Correspondence:** pablou@pablou.com

**ORCID:** 0009-0003-8968-9990

Samsung Electronics America employment is disclosed in Step 5 (Declaration of Interest) only. Not in author block.

---

## Step 3 — Abstract, keywords, JEL

### Abstract (paste exactly as below)

```
The AIAS Presence Measurement Protocol (v1.2; SSRN 6761698) specified Phase A pivot validation as the step that establishes a brand's substrate-category fit before Phase B topic-ID resolution proceeds, but documented the validation at the level of intent only — the specific stages, thresholds, and contingency-handling rules used in operational practice were not centrally specified. v0.16 (kitchen knives; SSRN 6791999) surfaced the gap operationally: the pre-registered pivot Victorinox failed Phase A on canonical-query Trends eligibility, and the activated alternate Wüsthof failed all three numeric stages of the same protocol, yet was activated as the operational pivot under pre-reg §6 contingency through manual operator intervention. This methodological note specifies the Phase A pivot-validation procedure centrally. §6.4 formalizes the five-stage protocol used in practice: Stage 1 (Knowledge Graph entity-suggestion audit for the pivot brand), Stage 2 (baseline Trends stability check), Stage 3 (bundle position check against in-category reference brands), Stage 4 (adjacency check against the pre-registered substrate-vs-adjacent keyword pair), Stage 5 (verdict aggregation under stage-conjunction thresholds on Stages 2–4). The fallback activation rule (R_F) implements bounded override: when both the primary pivot and the activated alternate fail Stage 5, the operator may invoke a one-time bounded override per cell per phase with mandatory DEVIATIONS log entry. The v0.16 Victorinox/Wüsthof case is retrospectively scored against the v1.3 specification in §6.4.8. v1.3 is a v1.2 successor increment; §6.4 is added, all other Protocol v1.2 sections remain byte-identical.
```

Character count: approximately 1,650 (well under SSRN's 4,000-char abstract limit).

### Keywords (semicolon-separated for SSRN)

```
methodology; Phase A; pivot validation; Google Trends; Knowledge Graph entity suggestions; bounded override; pre-registration; AIAS Presence Measurement Protocol
```

8 keywords; SSRN accepts up to 12.

### JEL classifications

**Primary:** M31 (Marketing)
**Secondary:** L86 (Information and Internet Services; Computer Software); L15 (Information and Product Quality; Standardization and Compatibility); D83 (Search; Learning; Information and Knowledge; Communication; Belief; Unawareness); M37 (Advertising)

Paste-formatted for SSRN's JEL field (comma-separated):

```
M31, L86, L15, D83, M37
```

---

## Step 4 — Subject classifications (eJournals)

Select these from SSRN's network picker:

1. **Marketing eJournal** — core methodology venue
2. **Marketing Strategy eJournal** — pivot validation as brand-measurement methodology infrastructure
3. **Information Systems eJournal** — data pipeline / measurement infrastructure layer
4. **AI eJournal** — context for the broader AIAS programme that v1.3 supports

Skip Consumer Behavior, Advertising & Marketing Comm, and Decision-Making Under Risk — those are appropriate for the substrate-phase findings papers (v0.16, v0.17, etc.) but not for a pivot-validation methodology note.

4 of the 7 available slots used; leaving 3 unused keeps the classification focused rather than scattered.

---

## Step 5 — Declarations

### Declaration of Interest

```
The author is employed full-time at Samsung Electronics America (Director, Corporate Brand Creative and Governance). The AIAS Presence Measurement Protocol and the broader Third System programme are independent research conducted under the SVA MPS Branding Program affiliation and the Third System research entity. Samsung Electronics America did not commission, fund, or review this research. No Samsung products are measured in any AIAS programme phase to date; Samsung is not represented in any published or in-pipeline brand panel. The author declares no other competing interests.
```

### Funder

```
Self-funded. No external research funding or sponsorship.
```

### Ethics

```
Not applicable; no human subjects. Data collection uses public Google Trends API (via SerpAPI) and public LLM API endpoints under standard developer terms of service.
```

---

## Step 6 — File upload

**Primary file:** `~/aias/papers/v1_3/aias_methodology_v1_3.pdf`

Verify before upload:
- Title page renders centered with the author block intact
- Section/subsection headings bold without auto-numbering on top of the §-prefixes
- §6.4.6.x and §6.4.7.x sub-sub-sections render at the right weight
- All Unicode glyphs render (no missing-glyph boxes for ρ, ≥, ≤, etc.)
- No orphan/widow issues in the abstract or §1
- Total length lands at approximately 12–14 pages

No supplementary files for v1.3 (no OSF deposit; no data accompaniment).

---

## Step 7 — Post-submission

Once SSRN assigns the abstract ID (format: 7-digit number, e.g., 6791999):

**1. Update userMemories registry** with v1.3 entry:

```
Methodology v1.3 = [abstract_id]
URL: https://ssrn.com/abstract=[abstract_id]
```

**2. Update Tri-System MSI WP bibliography** to cross-cite v1.3 alongside v0.13, v0.14, v0.15, v0.16, and v1.2 (6761698).

**3. Update v0.17 pre-registration draft** (when we return to it) to reference v1.3 §6.4 directly in §6 contingencies — replacing the placeholder "if v1.3 ships, apply v1.3 methodology; otherwise document in DEVIATIONS" language with the locked v1.3 citation.

**4. Tag the v1.3 git commit:**

```
cd ~/aias
git tag v1.3-published [commit-hash]
git push origin v1.3-published
```

---

## SSRN submission anticipated timing

Methodology notes with no new data typically clear SSRN's editorial queue within 48–72 hours of submission. The v1.3 abstract should be live and citable by end of week.

Once live, the v1.3 SSRN URL becomes the canonical reference target for v0.17 and all subsequent phases' Phase A pre-registration sections.
