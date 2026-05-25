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

This chat continues the AIAS™ (AI Availability Score) Measurement Program. AIAS™ 1.0 (Presence component) shipped May 2026 as SSRN 6817841, anchored on a 5-substrate base under Protocol v1.6. The program is now executing the AIAS™ 2.0 → 6.0 arc.

## Division of labor

- **This chat (claude.ai):** strategic reasoning, scope locking, hypothesis specification, content drafting (paper sections, content modules, abstracts, brand-format report copy), checkpoint reviews, voice-register checks, copy-paste command generation.
- **Claude Code (separate, local):** file system operations, build executions, git tag/commit operations, OSF uploads. I execute Claude-Code-paste-able instructions there.

Generate Claude Code instructions wherever execution is required. Do not assume file system access from this chat.

## Working environment (local, executed via Claude Code)

- Pipeline root: `/Users/pablou/aias/`
- Reports: `/Users/pablou/aias/reports/` — three-file set per phase: `build_report_vNN.py`, `vNN_<topic>_content.py`, `build_charts_vNN_<topic>.py`
- Papers: `/Users/pablou/aias/papers/v0_NN/` — pandoc + xelatex + Carlito; build cmd uses `--resource-path=papers/v0_NN`
- Brand tokens: `/Users/pablou/aias/brand/third_system_brand.json` (Indigo #37237B primary)
- Fonts: Akkurat Pro from `~/.fonts/Akkurat` and `~/Library/Fonts` (register via `matplotlib.font_manager.fontManager.addfont()` at module top; `plt.rcParams['font.family']=['Akkurat Pro','sans-serif']`)
- Python 3.14 — openai, matplotlib, reportlab, pypdf for builds; pandoc + xelatex for SSRN papers
- Git repo at pipeline root; OSF project ec6wh (`~/aias/scripts/osf_upload.py` with `OSF_TOKEN` env var; project ID ec6wh hardcoded)

## Conventions (non-negotiable)

- **Single unified build pipelines, no toggles.** Each phase forks prior build files with new version prefix, new registry. Prior phases untouched.
- **Pre-registration discipline.** Pre-reg at git commit before any data collection. Tag format: `vNN-prereg-rN`. Methodology locked at pre-reg.
- **Surgical precision over broad rewrites.** Edits scoped tightly; verify scope before executing major changes.
- **Two-register discipline.** Academic papers use H1/H2/H3 hypothesis framing. Managerial reports use P1–P5 propositional framing. Intentionally divergent registers.
- **Trademark convention.** Third System™ and AIAS™ marked on first prominent mention in formal documents. Subsequent mentions unmarked.
- **Samsung COI** disclosed in §COI only — never in author block. SVA MPS Branding is primary affiliation; Third System is secondary research entity.

## SSRN author block standard

Pablo Ulpiano González Castro (accent on á)
SVA, MPS Branding Program, New York, NY *(primary academic affiliation)*
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked)

## 7-step phase workflow

1. **Pre-reg at git commit** — methodology locked; tag `vNN-prereg-rN`.
2. **Measurement** against locked registry.
3. **Canonical scoring** + hypothesis status per locked methodology.
4. **Third System brand-format report PDF** (ReportLab + pypdf two-pass; Akkurat Pro; `<sub size='6'>1</sub>` for body subscripts, `<sub size='10'>1</sub>` for cover/18pt; wrap arrow connectors with `\u00a0` to prevent line-splits).
5. **SSRN academic paper** (pandoc + xelatex + Carlito 11pt; `\setstretch{1.36}`; `\parskip=8pt`; `\parindent=0pt`; titlepage with local `\setstretch{1.0}` + `\setlength{\parskip}{0pt}` overrides to fit one page; `\renewcommand{\maketitle}{}` to suppress pandoc auto-maketitle; figures inline in §3 Results via `![cap](../../reports/figs/vNN/chart_NN.pdf){#fig:label width=100%}`; Unicode→LaTeX subs for Carlito glyph gaps: ₜ→`$_{t}$`, ∈→`$\in$`, 10⁻⁴ → decimal).
6. **OSF deposit** at `osf.io/ec6wh/vNN/` — README, MANIFEST, data, registries, figures, code.
7. **SSRN submission** → abstract ID → cross-citation in program (update CLAUDE.md + bibliographies).

## SSRN submission checklist

- **Step 3:** abstract + keywords (semicolon-separated) + JEL codes (M31 primary; L86, L15, D83, M37 secondary)
- **Step 4:** up to 7 subject classifications (Marketing, Marketing Strategy, Consumer Behavior, Advertising & Marketing Comm, Information Systems, AI, Decision-Making Under Risk eJournals)
- **Step 5:** Declaration of Interest (Samsung COI); Funder ("Self-funded"); Ethics ("Not applicable; no human subjects; public APIs + LLM prompts")

## Canonical methodology citation set (current lock: v1.6)

SSRN 6761698 (v1.2 Four-Regime Taxonomy), 6797679 (v1.3 Phase A Pivot-Validation), 6799479 (v1.4 multi-component construct), 6810758 (v1.5 multi-statistic C2 + two-channel recall), 6816340 (v1.6 substrate Recognition pre-screen + IL Direct + Phantom Brand Persistence).

## SSRN abstract ID registry (for cross-citation)

**Foundational:** 6659000
**Phase papers:** v0.6=6720959 · v0.7=6721779 · v0.8=6728000 · v0.9=6736878 · v0.10=6741163 · v0.11=6745040 · v0.12=6748341 · v0.13=6750498 · v0.14=6755621 · v0.15=6768059 · v0.16=6791999 · v0.17=6802261 · v0.18=6806558 · v0.19=6809182 · v0.20=6811441 · v0.21=6815378
**Methodology:** v1.1=6722319 · v1.2=6761698 · v1.3=6797679 · v1.4=6799479 · v1.5=6810758 · v1.6=6816340
**Synthesis:** AIAS™ 1.0=6817841
URL pattern: `https://ssrn.com/abstract={id}`

---

## Task for this chat

Execute {PROJECT_ID} end-to-end through to ready-for-Claude-Code state:

1. **Scope checkpoint.** Confirm what this project is and isn't. Surface any locking decisions I need to make before pre-reg (substrate choice, hypothesis specification, instrument choice, measurement scope, etc.). Wait for my explicit lock before proceeding.

2. **Pre-reg draft.** Hypotheses (H_*), registry spec, scoring rules, falsification criteria. I'll review and lock; you'll then generate the Claude Code commands to commit + tag at pre-reg.

3. **Build pipeline draft.** Three-file set scaffold (or appropriate deliverable set for non-phase-paper projects). I'll review structure before Claude Code executes.

4. **Content modules + chart specs.** Draft inline in chat. I review and approve module-by-module.

5. **Paper draft.** Chunked checkpoints (intro/method/results/discussion/§7) per the 1.0 cadence. Voice-register clean throughout.

6. **Abstract + pre-flight.** Final checks before SSRN submission.

7. **OSF deposit manifest + Claude Code instructions** for upload.

8. **Cross-citation update package** — what to add to CLAUDE.md, MSI WP bibliography, in-repo bibliography, kickoff prompt registry.

Use `/THINK` for strategic reasoning. Surface decisions before assuming defaults. Keep voice register clean (no first-person plural in academic papers; P1–P5 propositional in managerial reports).

**Begin with the scope checkpoint.**
