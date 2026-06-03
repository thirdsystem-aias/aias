# AIAS™ Program — Standard Project Kickoff Prompt

> Copy this into each new chat. Fill in the two placeholders at the top (`{PROJECT_ID}` and `{ONE-LINE DESCRIPTION FROM SSOT}`). Everything else is constant.

---

## This chat's project

**Project ID:** {PROJECT_ID}
**Description:** {ONE-LINE DESCRIPTION FROM SSOT}

(SSOT reference: AIAS 2.0 → 6.0 roadmap, ~108 sequential projects across PHASES A–M. This is one of them.)

---

## Program context

I'm Pablo Ulpiano González Castro — Director, Corporate Brand Creative & Governance at Samsung Electronics America; Faculty in Creative Strategy at SVA MPS Branding Program; founder of Third System™ (thirdsystem.ai · hello@thirdsystem.ai), the research entity that serves as my data archive and methodology venue.

This chat continues the AIAS™ (AI Availability Score) Measurement Program. AIAS™ 1.0 (Presence component) shipped May 2026 as SSRN 6817841, anchored on a 6-substrate base (kitchen knives, kitchenware, indie fragrance, audiophile headphones, skincare, cosmetics, automotive) under Protocol v1.6. The program is now executing the AIAS™ 2.0 → 6.0 arc.

## Division of labor

- **This chat (claude.ai):** strategic reasoning, scope locking, hypothesis specification, content drafting (paper sections, content modules, abstracts, brand-format report copy), checkpoint reviews, voice-register checks, copy-paste command generation.
- **Claude Code (separate, local):** file system operations, build executions, git tag/commit operations, OSF uploads. I execute Claude-Code-paste-able instructions there.

Generate Claude Code instructions wherever execution is required. Do not assume file system access from this chat.

## Working environment (local, executed via Claude Code)

- Pipeline root: `/Users/pablou/aias/`
- Reports: `/Users/pablou/aias/reports/` — three-file set per phase: `build_report_vNN.py`, `vNN_<topic>_content.py`, plus `scripts/build_charts_vNN.py`
- Papers: `/Users/pablou/aias/papers/v0_NN/` — self-contained `.md` source (YAML preamble + custom `\begin{titlepage}` block + body); build via thin pandoc wrapper at `scripts/build_paper_v0_NN.py`
- Brand tokens: `/Users/pablou/aias/brand/third_system_brand.json` (Indigo #37237B primary)
- Fonts:
  - **Akkurat Pro** (brand-format reports) from `~/.fonts/Akkurat` and `~/Library/Fonts` — register via `matplotlib.font_manager.fontManager.addfont()` at module top; `plt.rcParams['font.family']=['Akkurat Pro','sans-serif']`
  - **Carlito** (SSRN papers) — system-installed; pandoc YAML carries `mainfont: "Carlito"`
- Python 3.14 — openai/anthropic/google generative-language SDKs for acquisition; matplotlib, reportlab, pypdf, pdf2image for builds; pandoc + xelatex for SSRN papers
- Git repo at pipeline root; OSF project ec6wh (`~/aias/scripts/osf_upload.py` with `OSF_TOKEN` env var; project ID hardcoded)

## Conventions (non-negotiable)

- **Single unified build pipelines, no toggles.** Each phase clones prior build files via the scaffolder (see Automation Scripts) with new version prefix and new registry. Prior phases untouched.
- **Pre-registration discipline.** Pre-reg at git commit before any data collection. Tag format: `vNN-prereg-rN`. Methodology locked at pre-reg. r1 → r2 amendments are normal practice when methodology defects are caught pre-acquisition (DEVIATIONS Entry 0 documents the amendment).
- **Surgical precision over broad rewrites.** Edits scoped tightly; verify scope before executing major changes.
- **Two-register discipline.** Academic papers use H_* hypothesis framing (H_Phantom_Defunct, H_Regime4, etc.) and academic prose. Managerial reports use P1–P5 propositional framing and brand-format editorial voice. Same underlying findings, intentionally divergent registers for different audiences.
- **Trademark convention.** Third System™ and AIAS™ marked on first prominent mention in formal documents (papers, proposals, websites). Subsequent mentions unmarked. Skip in casual conversation and internal notes.
- **Samsung COI** disclosed in §COI only — never in author block. SVA MPS Branding is primary affiliation; Third System is secondary research entity.
- **Layout verification before declaring done.** For any chart/report/PDF layout work: render PDF → rasterize via pdf2image → view inspected pages. Never reason from sizing math alone. This applies to chart_vNN scripts, report_vNN builders, and SSRN paper PDFs.

## SSRN author block standard

Pablo Ulpiano González Castro (accent on á)
SVA, MPS Branding Program, New York, NY *(primary academic affiliation)*
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked)

---

## Automation scripts (use these, don't reinvent)

The program has a build pipeline that handles most mechanical work. Direct phase chats to use these rather than improvising:

### `scripts/aias_new_phase.py` — phase scaffolder

One command clones the entire build pipeline from the prior phase with version strings swapped throughout:

```bash
python3 scripts/aias_new_phase.py --from vNN --to vMM --substrate "substrate name" [--dry-run]
```

Generates 11 files + 9 directories: build pipeline scripts (charts, report, paper), content modules (brand-format + pre-reg), mega-prompt, SSRN paper draft, submission packet template, OSF tree with README. Eliminates the build-pipeline-drift class of errors. Always preview with `--dry-run` first.

### `scripts/generate_ssrn_packet.py` — submission packet auto-emitter

Reads the phase's paper draft and emits a paste-ready SSRN submission packet:

```bash
python3 scripts/generate_ssrn_packet.py --phase vNN
```

Extracts title / subtitle / abstract / keywords / JEL codes / COI / data-availability from the paper YAML and Declarations section. Combines with program constants (subject classifications, author block, funder, ethics) to produce `papers/v0_NN/ssrn_submission_packet_v0_NN.md`. Idempotent — rerun anytime the paper draft evolves.

### `scripts/build_paper_v0_NN.py` — SSRN paper builder

Thin ~150-line pandoc wrapper (canonical pattern locked in v0.20/v0.21/v1.6/v0.22). Reads source `.md`, applies Unicode→LaTeX substitutions for Carlito glyph gaps, invokes pandoc with `--pdf-engine=xelatex --resource-path=PAPER_DIR`, outputs PDF. **Do not modify the script's structure — copy from prior phase, only version strings change.** All preamble, titlepage, abstract, sections live in the source `.md`.

### `scripts/osf_upload.py` — OSF deposit

```bash
python3 ~/aias/scripts/osf_upload.py ~/aias/osf/vNN vNN
```

Uses WaterButler API directly with `OSF_TOKEN` env var. Deposits the full vNN tree to osf.io/ec6wh/vNN/.

---

## 7-step phase workflow

1. **Scaffold + pre-reg.** Run `aias_new_phase.py` to clone prior phase. Author pre-reg content (hypotheses H_*, registry, thresholds, predictions) in the generated `prereg/v0_NN_<substrate>_content.py` and `prereg/v0_NN_mega_prompt.md`. Commit and tag at `vNN-prereg-rN`. If a methodology defect surfaces pre-acquisition, amend at r2 with DEVIATIONS Entry 0 documenting the change.

2. **Measurement.** Run Phase A (Recognition: 24 brands × 6 LLMs = 144 probes) and Phase B (two-channel Recall: 6 probes × 24 brands × 6 LLMs = 36 queries) against the locked registry. Six-model reference panel held fixed from v0.17 onward: Claude Opus 4.5, Claude Sonnet 4.5, GPT-4o, GPT-4o-mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite.

3. **Canonical scoring.** Run scoring per locked methodology version. Outputs `osf/vNN/vNN_verdicts.json` with per-hypothesis verdicts against locked matrices.

4. **Third System brand-format report PDF.**
   - Stack: ReportLab + pypdf two-pass (Pass 1 body layout with chart reservations; Pass 2 overlay chart PDFs at locked figsize)
   - Font: Akkurat Pro registered at module top
   - Subscripts use `<sub size='6'>1</sub>` body / `<sub size='10'>1</sub>` cover/18pt (NOT Unicode ₁ ₂ — Akkurat lacks them)
   - Wrap arrow connectors with `\u00a0` (NBSP) to prevent line-splits like "t₁ → t₂"
   - matplotlib xlabel sits ~30pt below add_axes bottom (labelpad + tick label height); verdict-text on charts must clear xlabel AND have ≥20pt to source line below
   - `ChartReservation` auto-sizes to actual chart PDF aspect via `PdfReader(chart_path).mediabox` to prevent dead-space-below-chart when `bbox_inches='tight'` produces variable mediabox
   - **Always render → rasterize → view before claiming layout is done**

5. **SSRN academic paper.** Use the canonical pattern:
   - Build script is the thin pandoc wrapper (copy from prior phase, swap version strings only — never improvise)
   - Source `.md` is **self-contained**: YAML frontmatter carries all preamble (`mainfont: Carlito`, `fontsize: 11pt`, header-includes with `setspace`/`float`/`caption`/`titlesec` packages, `\setstretch{1.36}`, `\parskip 8pt`, `\parindent 0pt`, `\renewcommand{\maketitle}{}`, `\providecommand{\xmpquote}[1]{#1}` stub)
   - Custom `\begin{titlepage}...\end{titlepage}` block is **first body content** with local `\setstretch{1.0}` + `\setlength{\parskip}{0pt}` overrides (one-page-fit rule)
   - Abstract on page 2 via `# Abstract {-}` markdown header — **NOT in titlepage**
   - Keywords + JEL codes + Paper status as inline bold paragraphs immediately after Abstract
   - Figures inline in §3 Results: `![cap](../../reports/figs/vNN/chart_NN_<topic>.pdf){#fig:label width=100%}` (use full filenames, not short names)
   - Unicode→LaTeX subs for Carlito gaps (handled automatically by build script): ₜ→`$_{t}$`, ∈→`$\in$`, ⊆→`$\subseteq$`, ▶→`$\blacktriangleright$`, ∧→`$\wedge$`, ✓→`\checkmark`, etc.
   - Compound forms like 10⁻⁴ → rewrite to decimal (0.0001) in source

6. **OSF deposit** at `osf.io/ec6wh/vNN/` — README, data/ (Phase A + Phase B CSVs), prereg/ (locked artifacts), reports/ (brand-format PDF), figures/ (chart PDFs), scripts/ (scoring code), registries/ (locked 24-brand list).

7. **SSRN submission.** Run `generate_ssrn_packet.py --phase vNN` to emit paste-ready packet. Submit via webform. On abstract ID return: backfill memory with the ID, update CLAUDE.md cross-citation registry, queue next phase's bibliography citation to upstream-phases line.

---

## SSRN submission flow (automated via `generate_ssrn_packet.py`)

The packet emitter handles Steps 3–6 automatically by reading the paper YAML. Standing constants the script applies (no per-phase work):

- **Step 4 — Subject classifications** (up to 7, identical across all AIAS phases): Marketing, Marketing Strategy, Consumer Behavior, Advertising & Marketing Communication, Information Systems, Artificial Intelligence, Decision-Making Under Risk eJournals
- **Step 5 — Funder:** "Self-funded"
- **Step 5 — Ethics:** "Not applicable; no human subjects; public APIs + LLM prompts"
- **JEL codes** (in paper YAML): M31 primary; L86, L15, D83, M37 secondary

Per-phase content (the packet emitter reads these from the paper):
- Title, subtitle, abstract, keywords (from paper YAML + Abstract section)
- Conflict of interest statement (from paper Declarations §COI — Samsung tier-2/3 disclosure customized per substrate)
- Data and code availability (from paper Declarations)

---

## Canonical methodology citation set (current lock: v1.6)

SSRN 6761698 (v1.2 Four-Regime Taxonomy) · 6797679 (v1.3 Phase A Pivot-Validation) · 6799479 (v1.4 multi-component construct) · 6810758 (v1.5 multi-statistic C2 + two-channel recall) · 6816340 (v1.6 substrate Recognition pre-screen + IL Direct + Phantom Brand Persistence).

## SSRN abstract ID registry (for cross-citation)

**Foundational:** 6659000
**Phase papers:** v0.6=6720959 · v0.7=6721779 · v0.8=6728000 · v0.9=6736878 · v0.10=6741163 · v0.11=6745040 · v0.12=6748341 · v0.13=6750498 · v0.14=6755621 · v0.15=6768059 · v0.16=6791999 · v0.17=6802261 · v0.18=6806558 · v0.19=6809182 · v0.20=6811441 · v0.21=6815378 · v0.22=6829118 · v0.23=6834298 · v0.24=6838802 · v0.25=6842138 · v0.26=6847678 · v0.27=6854758 · v0.28=6865478 · v0.29=6870778 · v0.30=6875319
**Methodology:** v1.1=6722319 · v1.2=6761698 · v1.3=6797679 · v1.4=6799479 · v1.5=6810758 · v1.6=6816340
**Synthesis:** AIAS™ 1.0=6817841
URL pattern: `https://ssrn.com/abstract={id}`

---

## Task for this chat

Execute {PROJECT_ID} end-to-end through to ready-for-Claude-Code state:

1. **Scope checkpoint.** Confirm what this project is and isn't. Surface any locking decisions needed before pre-reg (substrate choice, hypothesis specification, instrument choice, measurement scope, cell architecture). Wait for explicit lock before proceeding.

2. **Scaffold trigger.** Generate the `aias_new_phase.py` command. I run it via Claude Code; the build pipeline is then in place automatically.

3. **Pre-reg draft.** Hypotheses (H_*), registry spec, scoring rules, falsification criteria, predictions. Draft inline in chat. I review and lock; you generate the Claude Code commit + tag commands.

4. **Content modules + chart specs.** Draft the brand-format report content module (`reports/vNN_<topic>_content.py` — 11 attributes: COVER, STANDFIRST, LEAD_DECK, EXEC_SUMMARY, WHAT_WE_MEASURED, PATTERNS, LIMITATIONS, WHATS_NEXT, HYPOTHESIS_SCORING, HYPOTHESIS_DETAILS, CLOSING). Chart specs separately if non-trivial. I approve module-by-module.

5. **Paper draft.** Chunked checkpoints (intro / method / results / discussion / limitations / future research) per the canonical SSRN paper structure. Voice-register clean throughout — academic third-person, H_* hypothesis framing, no first-person plural. Figures inline in §3.

6. **Packet emit + pre-flight.** Run `generate_ssrn_packet.py --phase vNN`. Review the emitted packet. Final checks before SSRN submission.

7. **OSF deposit manifest + Claude Code instructions** for upload.

8. **Cross-citation update package** — Claude Code commands to update CLAUDE.md, the next-phase bibliography upstream-phases line, and the kickoff prompt's SSRN abstract ID registry.

Use `/THINK` for strategic reasoning. Surface decisions before assuming defaults. Keep voice register clean (no first-person plural in academic papers; P1–P5 propositional in managerial reports). Verify all layout work via render → rasterize → view before declaring done.

**Begin with the scope checkpoint.**
