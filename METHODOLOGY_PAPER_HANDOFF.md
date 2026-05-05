# Methodology Paper — Chat Handoff

**Purpose:** Open a new chat, paste the prompt below, attach the five files listed in §2. The receiving Claude will produce a venue recommendation, section structure, drafted introduction and methods (~2,300 words), research-log gap analysis, and an analysis of how recommendation-slot persistence relates to H1/H2 in the Tri-System paper.

**When to run this:** When you have headspace for a sustained writing project. The methodology paper is a multi-week effort; this handoff produces the first session's output, which becomes the working draft.

---

## 1. The prompt

Paste everything between the markers below into the new chat.

```
[BEGIN PROMPT]

I'm Pablo Ulpiano Gonzalez Castro, founder of Third System (thirdsystem.ai),
Director of Corporate Brand Creative and Governance at Samsung Electronics
America, and Faculty in the MPS Branding Program at the School of Visual Arts.

I run an AI brand-visibility measurement program called the AI Availability
Score (AIAS). I need to draft a methodology paper titled tentatively
"Measuring AI Availability: Methodological Notes from the AIAS Protocol"
suitable for a research-output venue (likely Journal of Brand Management,
Journal of Marketing Research, or SSRN preprint).

The empirical foundation is two reports plus an operational protocol:

- v0.6 cross-category report: AI Presence measured across five diverse
  categories (PM software, running shoes, premium olive oil, premium facial
  skincare, personal finance applications). Six framework patterns hold
  across the five-category baseline, including the v0.6 Mint phantom-brand
  observation (44% Presence on a brand decommissioned 25 months earlier).

- v0.7 designed-for-test report on Bed Bath & Beyond, the Phase 2
  replication test for the v0.6 phantom finding. Eight pre-registered
  hypotheses, six prompts × six models from four labs × eight runs = 288
  measurements, with Pier 1 as a structural comparator. The phantom
  replicates (BBB at 38.2% raw Presence, Pier 1 at exactly 0.0%) but
  manual valence review of every BBB mention forces a structural reframe:
  in 88% of BBB mentions, AI demonstrates knowledge that the entity has
  changed and surfaces the brand anyway, with disclaimer. The
  naive-phantom rate (AI presents BBB as fully live with no caveat) is
  1.7%. The phantom is not a knowledge gap. It is a recommendation slot.

THE PAPER'S CENTRAL THESIS:

AI brand visibility is structurally different from any prior
brand-visibility metric. It is not consumer awareness, not a lagged
indicator of consumer behavior, but a property of how AI mediation
composes recommendation sets. Brand-mention pathways become
reinforcement-encoded structures that persist beyond entity changes
— what we call recommendation-slot persistence. The AIAS protocol
operationalizes the measurement of this property. v0.6 establishes
that the framework holds across five categories with diverse
properties. v0.7 demonstrates the central thesis directly through the
BBB/Pier 1 contrast and the valence decomposition. Construct validity
— whether AI Presence correlates with consumer consideration,
purchase intent, or sales — remains open and is the subject of
Phase 3.

What I need from you in this session:

1. SECTION STRUCTURE. Propose a section structure suited to JBM
   conventions (or other venue you recommend in §5 below). Standard
   IMRaD adapted for a methods-and-findings paper, with the
   recommendation-slot reframe as the discussion's central claim.
   Approximate word counts per section. Note where v0.6 material lives
   vs where v0.7 material lives.

2. INTRODUCTION AND METHODS DRAFT. Draft an introduction (~800 words)
   and methods section (~1,500 words). Pull from the protocol document
   verbatim where appropriate (it is structured to double as the paper's
   spine) and adapt where the paper needs different framing for an
   academic audience. The introduction should establish the gap in
   prior brand-visibility measurement that AIAS fills, frame the
   recommendation-slot thesis as the paper's central claim, and state
   explicitly that the thesis emerged from designed-for-test
   measurement rather than from prior theory. The methods section
   should describe the protocol, the v0.6 baseline measurement, and
   the v0.7 designed-for-test methodology including pre-registration,
   manual valence review, and the BBB/Pier 1 structural comparator.

3. RESEARCH LOG GAPS. Read RESEARCH_LOG.md carefully — particularly
   the 2026-05-04 v0.7 entry and the v0.6 retrospective. Flag where
   entries are thin and what observations I should add before
   submission. The log has [FILL] markers where I know things are
   missing; focus on additional gaps the log itself does not flag,
   especially anywhere the paper would benefit from methodological
   detail the log doesn't currently capture.

4. RELATIONSHIP TO TRI-SYSTEM PAPER. The parent paper (Gonzalez Castro
   2026, JBM submission, attached) introduces AIAS conceptually and
   formalizes two hypotheses: H1 Conditional Reweighting and H2
   Default Reinforcement. The recommendation-slot persistence finding
   from v0.7 is structurally adjacent to H2 but distinct — it is
   specifically about how reinforcement-encoded brand-mention pathways
   persist beyond entity changes, not about how reinforcement
   intensifies under prompt-discourse alignment. Identify how
   recommendation-slot persistence relates to H1/H2: is it a
   refinement of H2, a new H3, or an empirical instantiation of H2
   under a specific boundary condition (entity disruption)? Make a
   recommendation and explain the reasoning. The answer determines
   whether the methodology paper proposes a theoretical extension or
   reports a confirmed instantiation.

5. VENUE RECOMMENDATION. Given the v0.7 reframe now anchors the paper
   as a theoretical contribution rather than a pure methods report,
   recommend the appropriate venue. Candidates: Journal of Brand
   Management (parent paper's target), Journal of Marketing Research
   (more empirical, faster review), International Journal of Research
   in Marketing (hybrid), SSRN preprint (no venue gate, fastest, no
   peer-review signal). Trade-offs?

POSITIONING CONSTRAINTS:

- SVA faculty research output is the primary affiliation framing.
- Samsung Electronics America is disclosed as conflict of interest
  in author note; the paper is independent research, not Samsung
  research.
- Third System is the principal-researcher venue, where the data and
  protocol are hosted, but the paper is not a Third System product
  description. It is a methodological contribution to the brand-
  measurement literature.
- The recommendation-slot reframe should be presented as exploratory
  finding (it emerged during manual review of v0.7, not from prior
  theory or pre-registered hypothesis) and the paper should be
  honest about that. Pre-registered confirmatory findings (H1, H2,
  H7, H8) are reported as confirmatory; the recommendation-slot
  reframe is reported as exploratory and Phase 3-testable.

ATTACHED FILES:

- MEASUREMENT_PROTOCOL_v1_1.md — the canonical operational protocol,
  structured to double as the paper's spine. v1.1 adds Phase 2
  methodology (pre-registration §6.4, manual valence review §6.5,
  designed-for-test category pattern §6.6).
- RESEARCH_LOG.md — methodological observations accumulated through
  v0.1 → v0.7. Includes a citation tracking table mapping log
  entries to methodology paper sections.
- v06_cross_category.pdf — the published v0.6 cross-category report
  (the worked example for the protocol applied across diverse
  categories).
- v07_phantom_persistence.pdf — the published v0.7 BBB designed-for-
  test report (the worked example for the protocol applied to a
  designed-for-test category, and the empirical anchor for the
  recommendation-slot thesis).
- Tri-System_Brand_Growth.docx — the parent paper that defines the
  AIAS framework and formalizes H1/H2 (for context on §4 above).

OUTPUT FORMAT:

A single Markdown document with five numbered sections (one per ask
above). Section 2 (introduction and methods draft) is the largest and
should be drafted as polished prose, not bullet points or outline.
Sections 1, 3, 4, 5 can be more analytical — bullets are fine where
they aid clarity.

Let's start with section 5, the venue recommendation. The other four
sections depend on it (target word count, target audience, what
counts as in-scope vs supplementary). Walk me through the trade-offs
before committing.

[END PROMPT]
```

---

## 2. Files to attach

| # | Filename | Source | Role |
|---|---|---|---|
| 1 | `MEASUREMENT_PROTOCOL_v1_1.md` | This session's outputs | Paper's spine — methods text comes from here |
| 2 | `RESEARCH_LOG.md` | This session's outputs | Methodological observations + citation map for log → paper traceability |
| 3 | `v06_cross_category.pdf` | The corrected version with Gonzalez Castro byline | v0.6 empirical material, worked example #1 |
| 4 | `v07_phantom_persistence.pdf` | The Phase 2 BBB report | v0.7 empirical material, worked example #2, anchor for hero finding |
| 5 | `Tri-System_Brand_Growth.docx` | Latest version on your machine | Parent paper, needed for §4 H1/H2 hypothesis-relationship analysis |

---

## 3. What the receiving chat should produce

A single Markdown document with five sections:

1. Section structure for the paper, with word-count targets
2. Drafted introduction (~800 words) and methods (~1,500 words) as polished prose
3. Research-log gap analysis
4. Analysis of how recommendation-slot persistence relates to H1/H2 with a concrete recommendation (refinement of H2, new H3, or empirical instantiation)
5. Venue recommendation with trade-offs

This is approximately a 90-minute working session for the receiving Claude. Expect the output to be a substantive starting draft, not a finished paper. Drafting iteratively over weeks from this base is the realistic path.

---

## 4. What changed from the earlier prompt

If you compare this to the prompt from the prior session (before v0.7 ran), three things shifted:

- **Argument pivots.** v0.6 framed the paper as "six findings replicate across categories." v0.7's recommendation-slot reframe is now the central thesis — a stronger structural claim than naive lag.
- **Empirical base doubles.** v0.6 + v0.7 instead of v0.6 alone. The paper now has both a baseline study and a designed-for-test study as worked examples.
- **Two new asks.** §4 (relationship to H1/H2 in the parent paper) and §5 (venue recommendation given the theoretical lift). These exist because v0.7 changed what kind of paper this is — from a pure methods report to a theoretical contribution that could plausibly target JMR or JCR rather than JBM.

Plus filenames now match real files (`MEASUREMENT_PROTOCOL_v1_1.md` not `_v1.0_FINAL.md`, no fictional `v06_source_text.md`).
