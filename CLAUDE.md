# AIAS Presence Measurement Protocol — Project Context

**This file auto-loads at the start of every Claude Code session run from `~/aias/`. It is the durable project-scoped context for the AIAS research program.**

---

## Project identity

**AIAS™ (AI Availability Score)** is an independent academic research program operationalizing AI Availability — the brand-level probability of retrieval, recommendation, or selection by an AI intermediary — as a measurable construct alongside Ehrenberg-Bass Mental Availability and Physical Availability. The program is led by Pablo Ulpiano González Castro, Faculty in the MPS Branding Program at the School of Visual Arts (SVA), founder of Third System™, and Director of Corporate Brand Creative & Governance at Samsung Electronics America.

**Samsung is the author's employer; it has no role in AIAS research.** Samsung is disclosed only in Declarations §Conflict of Interest, never in author blocks, abstracts, or body content.

**Two parallel academic tracks run cross-referencing but independent:**
1. **Tri-System Brand Growth** (theoretical) — MSI Working Paper, JAR short-form target
2. **AIAS™ Presence Measurement Protocol** (methodological/empirical) — the work in this repository

The full AIAS™ composite spans six components: **Presence** (current focus), Ranking, Consistency, Coverage, Grounding, Sentiment. Methodology paper v1.2 §7.4 frames the full composite as a multi-year arc, but **the current strategic target is to ship AIAS™ 1.0 (full six-component composite) within months, not years**, at a pace of approximately one phase per day. Treat this as the active operating tempo.

---

## Critical operating rules

These rules are non-negotiable. Violating them is a serious failure mode and will require throwing away work.

### 1. Fork-don't-rebuild

**Each new phase forks from the prior phase, surgically.** Never rebuild build scripts, content modules, or layouts from scratch. The established Third System editorial design has shipped across 14+ reports (v0.6 through v0.20) with a consistent layout, typography, brand palette, page templates, and section structure. New phases inherit all of that by direct file copy + surgical text-level edits.

**The phase-copy pattern (canonical):**

```bash
cp ~/aias/reports/build_report_vXX.py    ~/aias/reports/build_report_vYY.py
cp ~/aias/reports/vXX_topic_content.py   ~/aias/reports/vYY_topic_content.py
cp ~/aias/reports/build_charts_vXX.py    ~/aias/reports/build_charts_vYY.py
cp ~/aias/scripts/run_acquisition_vXX.py ~/aias/scripts/run_acquisition_vYY.py
cp ~/aias/scripts/score_vXX.py           ~/aias/scripts/score_vYY.py
cp ~/aias/papers/v0_XX/v0_XX_ssrn_paper_draft.md  ~/aias/papers/v0_YY/
cp ~/aias/reports/build_paper_v0_XX.py   ~/aias/reports/build_paper_v0_YY.py
# Edit each with str_replace for: version strings, content imports,
# chart filenames, citation, output filename, deposit root.
# Leave structural code (layout, typography, brand colors, page templates) untouched.
```

**Prior phases stay untouched.** Never edit `build_report_v19.py` to add v0.20 logic. Always copy → rename → edit the new file. The historical record matters.

### 2. Surgical precision over broad rewrites

Use `str_replace` for targeted edits. Never write a build script from scratch. Never use broad rewrites that touch sections beyond what the change requires. If you find yourself rewriting more than 20% of a file's lines for a phase fork, you're doing it wrong — stop and re-anchor on the prior phase.

### 3. Pre-registration discipline is non-negotiable

Every phase's design (registry, hypotheses, decision rules, thresholds, verdict matrices) is locked at a **git commit + tag** before any data acquisition begins. Pre-reg artifacts live at `prereg/v0_NN_prereg.md` and `prereg/v0_NN_registry.json`. Tag pattern: `v0.NN-prereg-r1` (r2, r3 if revisions before first acquisition).

Never modify pre-registration content after the git tag is pushed. Any changes after lock are documented as DEVIATIONS entries with explicit dispositions.

### 4. Trademark convention

Place `™` superscript after both "Third System" and "AIAS" on first prominent mention in formal documents, papers, proposals, applications, and websites. Subsequent mentions in the same document remain unmarked. Do not use ™ in casual conversation, internal notes, or after the first marked use within the same document.

### 5. Samsung in Declarations only

Author blocks in SSRN papers list **two affiliations only**:
1. School of Visual Arts, MPS Branding Program, New York, NY (primary academic affiliation)
2. Third System™ (research entity; data archive and methodology venue)

Samsung Electronics America is disclosed in Declarations §Conflict of Interest. Never in author block, never in abstract, never in body content.

---

## File structure

```
~/aias/
├── CLAUDE.md                                # This file
├── brand/
│   ├── third_system_brand.json              # v1.5 brand tokens (Indigo #37237B primary)
│   ├── design_tokens_template.json          # IDML extract for paragraph styles
│   ├── report_specs.json                    # Specs for brand-format report
│   ├── THIRDSYSTEM_Logo.svg                 # Wordmark
│   └── THIRDSYSTEM_AIPT_Logo.svg            # AIPT lockup
├── prereg/                                  # Pre-registration artifacts per phase
│   ├── v0_20_prereg.md
│   ├── v0_20_registry.json
│   ├── v0_21_mega_prompt.md                 # The v0.21 phase prompt
│   └── ...
├── scripts/
│   ├── osf_upload_v2.py                     # OSF deposit (nested-folder safe)
│   ├── run_acquisition_vNN.py               # Per-phase Phase A + Phase B runners
│   ├── score_vNN.py                         # Per-phase scoring + verdict resolution
│   ├── vNN_osf_deposit.sh                   # Per-phase final deposit runner
│   └── ...
├── reports/
│   ├── build_report_vNN.py                  # Per-phase brand-format report builder
│   ├── vNN_topic_content.py                 # Per-phase content module (11 attributes)
│   ├── build_charts_vNN.py                  # Per-phase matplotlib chart generator
│   ├── tsboilerplate.py                     # Shared "About the Third System" copy
│   ├── output/                              # Build intermediates (not committed)
│   └── figs/
│       ├── v19/chart_01_*.pdf
│       ├── v20/chart_01_*.pdf
│       └── ...
├── papers/                                  # SSRN paper sources per phase
│   ├── v0_20/
│   │   ├── v0_20_ssrn_paper_draft.md
│   │   ├── v0_20_ssrn_paper.pdf
│   │   ├── build_paper_v0_20.py
│   │   └── ssrn_submission_packet_v0_20.md
│   └── ...
├── osf/                                     # Local mirror of OSF deposits
│   ├── vNN/
│   │   ├── phase_a_results.csv
│   │   ├── phase_b_results.csv
│   │   ├── vNN_verdicts.json
│   │   └── reports/vNN_topic.pdf
│   └── ...
└── tomorrow.md                              # Running task list for next session
```

---

## The 13-step ship sequence

Every phase follows this sequence end-to-end. Each step has a canonical fork source.

| # | Step | Fork source | Lock point |
|---|---|---|---|
| 1 | Pre-reg artifact | Prior phase prereg/*.md | Author the new pre-reg document |
| 2 | Git commit + tag | — | `git tag v0.NN-prereg-r1` |
| 3 | OSF deposit pre-reg | `osf_upload_v2.py` | Files at `osf.io/ec6wh/vNN/prereg/` |
| 4 | Run acquisition | `run_acquisition_vXX.py` | Phase A (n_brands × 6 models probes) + Phase B (6 frames × 6 models queries) |
| 5 | Acquisition lock | — | `git tag v0.NN-acquisition-locked` |
| 6 | Run scoring | `score_vXX.py` | Hypothesis verdicts written to `osf/vNN/vNN_verdicts.json` |
| 7 | Build charts | `build_charts_vXX.py` | Three PDFs at `reports/figs/vNN/` |
| 8 | Brand-format report | `build_report_vXX.py` + `vXX_topic_content.py` | `osf/vNN/reports/vNN_topic.pdf` |
| 9 | SSRN paper draft + PDF | `v0_XX_ssrn_paper_draft.md` + `build_paper_v0_XX.py` | `papers/v0_NN/v0_NN_ssrn_paper.pdf` |
| 10 | SSRN submission packet | `ssrn_submission_packet_v0_XX.md` | Webform paste-ready document |
| 11 | SSRN submission | Manual webform submission | SSRN assigns abstract ID (1–3 days, typically same-day) |
| 12 | Final OSF deposit | `vXX_osf_deposit.sh` | Charts + paper + scoring + report on `osf.io/ec6wh/vNN/` |
| 13 | Memory backfill | Manual update to userMemories | Record SSRN ID, verdicts, commit hash |

---

## Typography rules

### Brand-format reports (ReportLab + Akkurat Pro)

- Detect Akkurat Pro at `~/.fonts/Akkurat/` and `~/Library/Fonts/`. Inter is fallback; Helvetica is hard fallback (emits HARD WARNING).
- OTF→TTF conversion via fontTools is automatic when needed; cached at `~/.cache/third_system_reports/fonts/`.
- Subscripts use `<sub>N</sub>` markup, not Unicode ₁/₂ glyphs (Akkurat lacks them). Body: `<sub size='6'>1</sub>`; cover/18pt: `<sub size='10'>1</sub>`.
- Wrap arrow connectors in NBSP (`\u00a0`) to prevent line splits.
- Brand primary: Indigo `#37237B`.

### SSRN papers (pandoc + xelatex + Carlito)

- YAML: `mainfont: Carlito`, `fontsize: 11pt`.
- Header includes: `\setstretch{1.36}`, `\parskip=8pt`, `\parindent=0pt`, `\usepackage{amssymb}` (for `$\checkmark$` and `$\times$` in verdict tables), `\renewcommand{\maketitle}{}` (suppresses pandoc's auto-titlepage).
- Custom `\begin{titlepage}...\end{titlepage}` block with LOCAL `\setstretch{1.0}` + `\setlength{\parskip}{0pt}` overrides — without these the titlepage inflates ~35% and bleeds to page 2. This is the v0.19+ one-page-fit rule.
- Title page centered with `\fontsize{16}{21.76}\selectfont\bfseries`; local `\parskip=10.36pt`.
- `\floatplacement{figure}{H}`; `\captionsetup{labelfont={bf,it}, textfont=it, justification=raggedright}`.
- `\titleformat{\section}{\bfseries\large}{\thesection}{1em}{}`; same pattern for subsection.

**Carlito glyph gaps requiring Unicode→LaTeX substitution in build_paper_vNN.py:**

| Unicode | Replacement |
|---|---|
| `ₜ` (U+209C subscript t) | `$_{t}$` |
| `∈` (U+2208) | `$\in$` |
| `⊆` (U+2286) | `$\subseteq$` |
| `▶` (U+25B6) | `$\blacktriangleright$` |
| `→`, `←`, `↔`, `⇒` | `$\rightarrow$`, etc. |
| `✓`, `✗` | `$\checkmark$`, `$\times$` |
| `−` (U+2212 math minus) | `$-$` |
| `⁻⁴` etc | `$^{-4}$` (rewrite compounds to decimal if possible) |
| `ρ` | `$\rho$` |

The substitution function should skip the YAML front-matter so escaped LaTeX in `header-includes` isn't double-processed.

---

## Charts (matplotlib editorial format)

Per the Third System chart convention:
- Title: bold, top-left, GRAY_TITLE
- Subtitle: gray, immediately below title
- Thin indigo (#37237B) separator rule below subtitle
- Source line: italic gray at bottom, citing upstream SSRN IDs
- Font: Akkurat Pro registered via `matplotlib.font_manager.fontManager.addfont()` from `~/.fonts/Akkurat/` and `~/Library/Fonts/`. Set `plt.rcParams['font.family'] = ['Akkurat Pro', 'sans-serif']`. Sans-serif fallback only when font unavailable.
- Native figsize for v0.20 charts: `(7.5, 5.5)` inches (76 DPI default). This figsize key is preserved in `CHART_FIGSIZE_IN` in build_report_vNN.py for cross-version reuse.

---

## SSRN submission standards

### Author block

```
Pablo Ulpiano González Castro (note: á carries acute accent)
School of Visual Arts, MPS Branding Program, New York, NY
(primary academic affiliation)
Third System™ (research entity; data archive and methodology venue)
Correspondence: pablou@pablou.com · pablou.com
ORCID: 0009-0003-8968-9990 (linked)
```

### JEL codes

- **M31** — Marketing (primary)
- **L86** — Information and Internet Services
- **L15** — Information and Product Quality
- **D83** — Search; Learning; Information and Knowledge
- **M37** — Advertising

### Subject classifications (up to 7 eJournals)

1. Marketing eJournal
2. Marketing Strategy eJournal
3. Consumer Behavior eJournal
4. Advertising & Marketing Communications eJournal
5. Information Systems & eBusiness eJournal
6. Artificial Intelligence eJournal
7. Decision-Making Under Risk & Uncertainty eJournal

### Declarations

- **COI:** Standard Samsung disclosure (employer; no role in research; pre-acquisition COI screen documented as DEVIATIONS Entry 0)
- **Funder:** Self-funded
- **Ethics:** Not applicable; no human subjects; public LLM APIs
- **Data/code availability:** OSF `osf.io/ec6wh/vNN/` with commit hash and tag references

---

## SSRN abstract ID registry

| Phase | SSRN ID | Notes |
|---|---|---|
| Foundational | 6659000 | AI Availability — A Third System in Brand Availability Theory |
| v1.2 (Methodology) | 6761698 | Presence Measurement Protocol: Construct Validity, Four-Regime Taxonomy |
| v1.3 (Methodology) | 6797679 | Phase A Pivot-Validation Specification |
| v1.4 (Methodology) | 6799479 | Recognition × Recall Decomposition (multi-component) |
| v1.5 (Methodology) | 6810758 | Multi-Statistic C2 + Two-Channel Recall |
| v0.16 (Kitchen knives) | 6791999 | Regime 4 Boundary + Discourse-Language Carryforward |
| v0.17 (Premium kitchenware) | 6802261 | Panel Inadequacy + Recognition × Recall Dissociation anchor (Iwachu) |
| v0.18 (Indie fragrance) | 6806558 | IL Moderator + Dissociation Generalization (second family) |
| v0.19 (Audiophile electronics) | 6809182 | C3 Rescue + Dissociation Replication (third family) |
| v0.20 (Skincare) | 6811441 | Type 2 Emergence + first prospective v1.5 C2 (fourth family) |
| v0.21 (Cosmetics) | pending | Type 2 EMERGED pursuit (fifth family) |

URL pattern: `https://ssrn.com/abstract={id}`

---

## Current state

**Just shipped:** v0.20 (Skincare, SSRN 6811441, May 2026). Type 2 quadrant empirically populated for the first time (Glossier and Rhode in Cell B). First prospective v1.5 phase. Four substrate families anchored.

**Next:** v0.21 (Cosmetics). Mega-prompt at `prereg/v0_21_mega_prompt.md`. Pursues Type 2 EMERGED to close the Presence-component AIAS™ 1.0 anchor base at five substrate families.

**After v0.21:**
1. Protocol v1.6 (moderator pathway independent of Regime 4) — ~1 day
2. Synthesis paper consolidating five-family anchor base — ~3–5 days
3. AIAS™ 1.0 Presence-component release packaging — ~1 day
4. Pivot to remaining five composite components (Ranking, Consistency, Coverage, Grounding, Sentiment) — multi-week, methodology + empirical per component

---

## Pre-flight checklist before any ship cycle

Before starting a new phase:

- [ ] Confirm I'm on a clean working tree (`git status`), or stash unrelated changes (`git stash push -u`)
- [ ] Confirm I'm on the right branch (typically a new phase branch: `git checkout -b v0.NN-topic`)
- [ ] Confirm API keys are loaded: `~/.api_keys` exports `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`
- [ ] Confirm `OSF_TOKEN` is loaded in shell env (for the OSF deposit steps)
- [ ] Confirm prior phase fork sources exist at `~/aias/reports/build_report_vXX.py` etc.

---

## DON'T-DO list

These are failure modes that have occurred and must not recur:

1. **Don't rebuild build scripts from scratch.** Always fork from the prior phase. The established design has shipped 14+ times; new phases inherit it.
2. **Don't mention Samsung outside Declarations §COI.** Not in author block, not in abstract, not in body content, not in OSF metadata.
3. **Don't modify pre-registration after the git tag.** All post-tag changes are DEVIATIONS entries with explicit dispositions.
4. **Don't push to main without review.** Phase work lives on phase branches; main is for shipped phases only.
5. **Don't skip the COI screen.** Every phase opens with DEVIATIONS Entry 0 documenting the Samsung screen result before acquisition begins.
6. **Don't generate Akkurat-incompatible glyphs in ReportLab.** Use `<sub>N</sub>`, not Unicode subscripts.
7. **Don't generate Carlito-incompatible glyphs in pandoc paper builds without the substitution table.** Math symbols, checkmarks, math minus, subscripts all require LaTeX equivalents.
8. **Don't store API keys in committed files.** They live in `~/.api_keys` (chmod 0600) or shell env, never in git.
9. **Don't run scripts with broad `git add .`.** Always specify paths; the working tree often has uncommitted changes across multiple phase branches.
10. **Don't assume verdicts before they're computed.** Pre-reg states predictions in §8 "Substantive predictions" as descriptive only; the actual verdicts come from the scorer's resolution of the locked verdict matrices, not from authorial expectation.

---

## How to use this file

When starting any Claude Code session in `~/aias/`:

1. This file loads automatically; the assistant should treat its conventions as binding.
2. For a specific phase ship cycle, paste or reference the phase-specific mega-prompt (e.g. `prereg/v0_21_mega_prompt.md`).
3. For ad-hoc questions, the assistant should anchor on the file structure, conventions, and registry sections above.
4. Updates to this file land in commits with the message prefix `[CLAUDE.md]`.

The assistant should ask the user before making changes to this file. The user can also amend it directly between sessions.
