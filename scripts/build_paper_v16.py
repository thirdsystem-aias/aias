#!/usr/bin/env python3
"""Build the v0.16 SSRN paper PDF via pandoc + xelatex.

Inputs:
    ~/aias/papers/v16_ssrn_paper_draft.md   — source markdown (Carlito YAML)
    ~/aias/osf/v16/figures/*.pdf             — embedded figures

Outputs:
    ~/aias/papers/v16/v16_ssrn_paper.pdf     — final PDF
    ~/aias/papers/v16/preamble_v16.tex       — generated LaTeX preamble
    ~/aias/papers/v16/v16_ssrn_paper_build.md — patched source (figure paths)

Visual identity matches v0.7-v0.14 SSRN papers:
    - Carlito mainfont, 11pt
    - 1.36 line spacing (setstretch)
    - 8pt parskip, 0pt parindent (inline LaTeX in source)
    - Figure placement [H] (float package; figures stay where placed)
    - Figure captions: bold italic label, italic text, raggedright

The figure-path rewrite step is needed because the draft uses ../figures/...
relative paths, but the v0.16 source lives in ~/aias/papers/ alongside the
v0.14 source. Build rewrites to figures/... and adds ~/aias/osf/v16/ to
pandoc's --resource-path search list.

Run:
    python ~/aias/scripts/build_paper_v16.py

To force a rebuild of the figures themselves first:
    python ~/aias/scripts/build_charts_v16.py && python ~/aias/scripts/build_paper_v16.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------

HOME = Path.home()
PAPERS_DIR = HOME / "aias" / "papers"
V15_DIR = PAPERS_DIR / "v16"
V15_DIR.mkdir(parents=True, exist_ok=True)

SOURCE = PAPERS_DIR / "v16_ssrn_paper_draft.md"
RESOURCE_BASE = HOME / "aias" / "osf" / "v16"  # figures live at RESOURCE_BASE/figures/

OUT_PDF = V15_DIR / "v16_ssrn_paper.pdf"
PREAMBLE = V15_DIR / "preamble_v16.tex"
BUILD_MD = V15_DIR / "v16_ssrn_paper_build.md"  # patched source

# ----------------------------------------------------------------------------
# Step 1: Sanity check
# ----------------------------------------------------------------------------

if not SOURCE.exists():
    sys.exit(f"Source not found: {SOURCE}\n"
             f"Expected the v0.16 paper draft at this path.")

figures_dir = RESOURCE_BASE / "figures"
if not figures_dir.is_dir():
    sys.exit(f"Figures directory not found: {figures_dir}\n"
             f"Run scripts/build_charts_v16.py first.")

n_figures = len(list(figures_dir.glob("chart_v16_*.pdf")))
print(f"Source markdown: {SOURCE}")
print(f"Figures directory: {figures_dir} ({n_figures} PDFs)")
print(f"Output directory: {V15_DIR}")
print()

# ----------------------------------------------------------------------------
# Step 2: Patch figure paths and Unicode characters in the markdown
# ----------------------------------------------------------------------------

UNICODE_SUBS = {
    # PAPER_V16_EXTRA_UNICODE_SUBS — added ρ, ≥, ∧ for v0.16 (LMR fallback)
    "⊆": r"$\subseteq$",
    "▶": r"$\blacktriangleright$",
    "ₜ": r"$_{t}$",
    "∈": r"$\in$",
    "ρ": r"$\rho$",            # Greek rho — used throughout v0.16 paper
    "≥": r"$\geq$",            # greater-than-or-equal — used in decision rules
    "∧": r"$\land$",           # logical AND — used in decision rules
    "≤": r"$\leq$",            # for completeness
    "×": r"$\times$",          # times sign
    "≠": r"$\neq$",            # not-equal
    "·": r"$\cdot$",           # middle dot (used in correspondence line)
}

md = SOURCE.read_text()
n_orig_fig = md.count("../figures/")
patched = md.replace("../figures/", "figures/")
n_unicode_subs = 0
for src_char, tex_repl in UNICODE_SUBS.items():
    count = patched.count(src_char)
    if count:
        patched = patched.replace(src_char, tex_repl)
        n_unicode_subs += count
        print(f"  Unicode patch: {count} occurrences of '{src_char}' → {tex_repl!r}")

BUILD_MD.write_text(patched)
print(f"Patched source written: {BUILD_MD}")
print(f"  Figure path references rewritten: {n_orig_fig} occurrences of "
      f"'../figures/' → 'figures/'")
if n_unicode_subs:
    print(f"  Unicode→LaTeX substitutions: {n_unicode_subs} total")
print()

# ----------------------------------------------------------------------------
# Step 3: Write preamble
# ----------------------------------------------------------------------------

preamble = r"""% v0.16 SSRN paper preamble — matches v0.7-v0.14 visual identity
\usepackage{float}
\floatplacement{figure}{H}

\usepackage{caption}
\captionsetup{
    labelfont={bf,it},
    textfont=it,
    justification=raggedright,
    singlelinecheck=false,
    skip=4pt
}

\usepackage{setspace}
\setstretch{1.36}

\usepackage{booktabs}

% Reduce widow/orphan lines
\widowpenalty10000
\clubpenalty10000
"""
PREAMBLE.write_text(preamble)
print(f"Preamble written: {PREAMBLE}")
print()

# ----------------------------------------------------------------------------
# Step 4: Invoke pandoc
# ----------------------------------------------------------------------------

# PAPER_V16_CITEPROC_BIB — citeproc + references.bib wired in
BIB_PATH = PAPERS_DIR / "references.bib"
cmd = [
    "pandoc",
    "--pdf-engine=xelatex",
    f"--include-in-header={PREAMBLE}",
    f"--resource-path={V15_DIR}:{RESOURCE_BASE}",
    "--citeproc",
    f"--bibliography={BIB_PATH}",
    str(BUILD_MD),
    "-o", str(OUT_PDF),
]

print("Running pandoc...")
print(f"  {' '.join(cmd)}")
print()

result = subprocess.run(cmd, capture_output=True, text=True)

# ----------------------------------------------------------------------------
# Step 5: Report
# ----------------------------------------------------------------------------

if result.stdout:
    print("STDOUT:")
    print(result.stdout)

if result.stderr:
    print("STDERR:")
    print(result.stderr)

if result.returncode != 0:
    sys.exit(f"pandoc failed with exit code {result.returncode}")

if not OUT_PDF.exists():
    sys.exit(f"pandoc returned 0 but output PDF not found at {OUT_PDF}")

size_kb = OUT_PDF.stat().st_size / 1024
print()
print(f"✓ PDF built: {OUT_PDF}")
print(f"  Size: {size_kb:.1f} KB")
print()
print(f"Open with:  open {OUT_PDF}")
