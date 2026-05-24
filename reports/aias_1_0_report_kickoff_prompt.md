# AIAS™ 1.0 Brand-Format Report — Claude Code Kickoff Prompt

**Save location:** `~/aias/reports/aias_1_0_report_kickoff_prompt.md`

**Usage:** Copy the fenced markdown block below and paste into a fresh Claude Code session opened in `~/aias/`. The session reads `CLAUDE.md` first, then this prompt drives the work.

---

```markdown
We're working on the AIAS™ 1.0 brand-format Third System™ report — the 
parallel managerial deliverable for the synthesis paper (SSRN 6817841). 
Two-week stagger after SSRN abstract ID landed; held-out from the synthesis 
paper sprint per D6 in the outline.

═══════════════════════════════════════════════════════════════════════════════
BEFORE WRITING ANY PROSE — READ THESE IN ORDER
═══════════════════════════════════════════════════════════════════════════════

1. CLAUDE.md (project conventions; two-register discipline; report build 
   pipeline patterns)
2. papers/aias_1_0/aias_1_0_synthesis_paper_draft.md (the academic source 
   for substantive content)
3. papers/aias_1_0/aias_1_0_synthesis_outline.md §6 D6 + §8 figure inventory 
   (the report deliverable spec including the content-module scope flag: 
   ~1500–2200 lines vs. ~600–800 for a phase report; scaffolding may need 
   refactoring rather than direct copy)
4. reports/build_report_v21.py + reports/v21_cosmetics_content.py + 
   reports/build_charts_v21.py (the v0.21 phase-report pattern to fork)

═══════════════════════════════════════════════════════════════════════════════
GOAL
═══════════════════════════════════════════════════════════════════════════════

Ship the AIAS™ 1.0 brand-format Third System™ report — the managerial 
deliverable that consolidates the five-family anchor base in P1–P5 
propositional register for brand strategy practitioners and marketing 
managers.

What it IS:
- Managerial register (P1–P5 propositional framing, executive-readable)
- Brand-format Third System™ identity (Akkurat Pro, Indigo #37237B primary)
- Consolidates synthesis paper findings from §4.5 / §5.5 / §5.6 / §6.2 
  into managerial-register prose
- Three-file set in reports/ following v0.21 pattern, scaled per D6 scope flag

What it is NOT:
- Not a phase-report scope (this is the program's first synthesis-scale 
  brand-format event)
- Not the SSRN paper voice — distinct two-register discipline; do not 
  collapse academic and managerial registers into one artifact
- Not a six-component AIAS composite claim — Presence component only, 
  mirroring SSRN paper L7 scope
- Not a construct-validity or behavioral-correlate claim

═══════════════════════════════════════════════════════════════════════════════
HEADLINE MANAGERIAL FINDINGS — Surface in this order
═══════════════════════════════════════════════════════════════════════════════

1. Five-substrate empirical anchor base complete (program milestone framing)
2. Phantom channel signature (Estée Lauder / Clinique canonical-pure vs. 
   Glossier cultural-pure as the textbook managerial case)
3. Rare Beauty 1:17 as the textbook brand-diagnostic case
4. IL Direct CONFIRMED — first CONFIRMED moderator verdict at any layer; 
   managerial framing: "Identity Load now empirically tracks AI channel 
   asymmetry"
5. Three v1.6 protocol increments as managerial methodology framing

═══════════════════════════════════════════════════════════════════════════════
FIRST TASK — DRAFT THE CONTENT-MODULE OUTLINE
═══════════════════════════════════════════════════════════════════════════════

Create reports/aias_1_0_content_outline.md before writing any content-module 
prose. Outline structure:

1. Positioning — what the report IS / what it is NOT (mirroring the kickoff 
   above but in managerial-register voice)
2. Headline managerial findings (the five above, with one-paragraph framing 
   per finding)
3. P1–P5 propositional framework — name the five propositions the report 
   will carry, with each proposition's supporting evidence anchor
4. Content-module section structure (STANDFIRST, EXEC_SUMMARY, FINDINGS, 
   HYPOTHESIS_DETAILS replaced with PROPOSITION_DETAILS, PATTERNS, 
   LIMITATIONS, WHATS_NEXT — mirroring v0.21 schema but adapted to 
   synthesis scope)
5. Chart inventory — which figures from synthesis paper to reuse vs. 
   brand-format-specific new charts
6. Build-script scaffolding decisions — direct copy from v0.21 vs. refactor 
   per D6 scope flag
7. Estimated content-module size (per D6: ~1500–2200 lines)
8. Decisions needed before drafting (recommend each)
9. Open questions

═══════════════════════════════════════════════════════════════════════════════
DECISIONS NEEDED BEFORE PROSE — Recommend each in the outline, gate drafting
═══════════════════════════════════════════════════════════════════════════════

D1. P1–P5 propositional content. What are the five propositions? Recommend 
    with one-sentence framing per proposition. Anchor each to synthesis 
    paper §4 or §5 evidence.

D2. Cover layout. Synthesis-scale event — does the cover follow v0.21 
    pattern (single STANDFIRST on lead page) or scale up (e.g., five-panel 
    anchor-base visual + STANDFIRST)? Recommend with rationale.

D3. Chart strategy. Reuse all 6 synthesis paper charts directly, brand-style 
    them with Akkurat / Indigo, or build managerial-register replacements 
    (e.g., Fig 6 phantom channel signature is the most managerial-relevant 
    chart; may warrant a brand-format upgrade)? Recommend per chart.

D4. STANDFIRST length. Phase reports use ~570 chars in the narrow lead_top 
    frame. Synthesis-scale event may justify a multi-paragraph standfirst 
    or a different lead-page layout. Recommend.

D5. Content-module size. ~1500–2200 lines is the D6 estimate. Locks in the 
    scaffolding decision (refactor vs. direct copy from v0.21).

D6. Output filename and path. Recommend: 
    reports/aias_1_0_brand_format_report.pdf (consistent with the 
    v21_cosmetics.pdf pattern).

D7. Pre-registration handling. Brand-format reports historically don't 
    require pre-reg (managerial deliverable, not measurement artifact). 
    Confirm same convention applies here, or recommend deviation if the 
    synthesis-scale event warrants formal pre-reg of the managerial framing.

═══════════════════════════════════════════════════════════════════════════════
WORK ORDER (once outline + D1–D7 resolved)
═══════════════════════════════════════════════════════════════════════════════

1. Draft outline → walk through D1–D7 with Pablo → lock outline (no git tag 
   required unless D7 says otherwise)
2. Build aias_1_0_content.py (the content module; the heaviest work; 
   ~1500–2200 lines)
3. Build build_charts_aias_1_0_report.py — likely a thin wrapper around 
   the synthesis paper's chart builder with brand-format styling overrides, 
   OR a fresh chart builder if D3 calls for managerial-register replacements
4. Build build_report_aias_1_0.py — main report builder; refactor or copy 
   from build_report_v21.py per D5
5. Render PDF; pre-flight checks (page count, voice register, chart 
   placement, brand-format identity)
6. OSF deposit at osf.io/ec6wh/aias_1_0/report/ (per existing OSF tree)

═══════════════════════════════════════════════════════════════════════════════
CONVENTIONS / DO-NOTS
═══════════════════════════════════════════════════════════════════════════════

- Two-register discipline: managerial P1–P5 voice throughout; NO H1/H2 
  hypothesis labels; NO academic-paper voice leakage from the synthesis 
  paper. Drawing on synthesis paper §4.5 / §5.5 / §5.6 / §6.2 as substantive 
  source means TRANSLATING the content to managerial register, not 
  copy-pasting.
- AIAS™ Presence Measurement Protocol and Third System™ trademark convention 
  per CLAUDE.md: first prominent mention marked with ™, subsequent unmarked.
- Samsung disclosed only if a Declarations or About section requires it. 
  Most brand-format reports have a "Methodology" footer block rather than 
  a Declarations section; verify pattern from v0.21 report.
- Akkurat Pro registered at module top of every chart-building script. 
  Indigo #37237B as primary; cell colors per the established convention.
- Subscript rule for Akkurat (ReportLab + Akkurat lack ₁/₂ glyphs): use 
  <sub size='6'>N</sub> markup, not Unicode subscripts. NBSP-wrap arrow 
  connectors to prevent line-splits.
- Don't claim construct validity, six-component composite, or 
  behavioral-correlate predictions. Same scope discipline as the SSRN paper.

═══════════════════════════════════════════════════════════════════════════════
START HERE
═══════════════════════════════════════════════════════════════════════════════

Read the four files listed at the top. Then draft 
reports/aias_1_0_content_outline.md. When the outline is ready, walk me 
through D1–D7 with your recommendations. Don't draft any content-module 
prose before those decisions are locked.
```

---

## Notes for Pablo (not part of the prompt)

**Estimated effort:** 10–15 working sessions per outline §9 (revised at OQ6 effort realism). Roughly half the SSRN paper's effort, but front-loaded on the content module which is structurally heavier than any phase-report content module the program has shipped.

**Voice translation is the substantive work.** Most of the synthesis paper's empirical findings live at the right managerial level already — Rare Beauty 1:17 reads as a diagnostic case in either register; the phantom channel signature is interpretable to either audience. The translation work is in §3 methodology condensation (managerial readers don't need v1.4 → v1.6 lineage) and §5 / §6 framing (P1–P5 propositional voice replaces H1/H2 hypothesis voice). Watch for register leakage at every checkpoint.

**This is the program's first synthesis-scale brand-format event.** All prior brand-format reports were phase-scale (v0.6 through v0.21). The scaffolding refactor question (D5) is real — phase-report scaffolding assumes one substrate, one finding cluster, one pre-reg verdict matrix. Synthesis scaffolding spans five substrates, multiple finding clusters, the construct claim itself. Direct copy probably won't hold; expect a refactor.

**Save the prompt and reuse it.** This prompt + CLAUDE.md + the synthesis outline form your restart context for the brand-format report build across sessions. Context windows will roll over.
