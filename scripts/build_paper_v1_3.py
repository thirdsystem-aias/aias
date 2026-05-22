#!/usr/bin/env python3
r"""
build_paper_v1_3.py — Build AIAS Methodology Paper v1.3 PDF

Adapted from build_paper_v16.py. v1.3 is a methodological note with no
figures, so the two-pass chart-overlay rendering is removed; this is a
single-pass build: markdown -> pandoc -> xelatex -> PDF.

Typography settings per AIAS canonical convention:
  - Carlito body, 11pt
  - \setstretch{1.36}, \parskip=8pt, \parindent=0pt
  - Title page centered, 16/21.76 bold, local \parskip=10.36pt
  - secnumdepth=-1 suppresses LaTeX auto-numbering (headings carry their
    own section prefixes; double-numbering avoided)
  - float package \floatplacement{figure}{H} (no figures in v1.3, retained
    for parity with v16 pipeline)
  - captionsetup labelfont={bf,it} textfont=it raggedright
  - titlesec bold section/subsection headings

Usage:
    python3 build_paper_v1_3.py

Output:
    papers/v1_3/aias_methodology_v1_3.pdf
"""

import re
import subprocess
import sys
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "papers"
SRC = PAPER_DIR / "v1_3_ssrn_paper_draft.md"
BUILD_DIR = PAPER_DIR / "v1_3"
PREPROCESSED = BUILD_DIR / "v1_3_preprocessed.md"
OUTPUT_PDF = BUILD_DIR / "aias_methodology_v1_3.pdf"


# ---------------------------------------------------------------------------
# YAML front-matter and LaTeX preamble
# ---------------------------------------------------------------------------
# Author block uses \\ (LaTeX explicit line break) at end of each line rather
# than single-\ trailing continuation. Inside the custom \maketitle's
# \centering block, single-\ + newline triggers "There's no line here to end".

YAML_HEADER = r"""---
title: "The AIAS™ Presence Measurement Protocol: Phase A Pivot-Validation Specification (v1.3)"
author: |
  Pablo Ulpiano González Castro \\
  \small SVA, MPS Branding Program, New York, NY \\
  \small (primary academic affiliation) \\
  \small Third System™ (research entity; data archive and methodology venue) \\
  \vspace{0.3cm}
  \small Correspondence: pablou@pablou.com · pablou.com \\
  \small ORCID: 0009-0003-8968-9990
date: \today
mainfont: Carlito
fontsize: 11pt
geometry: margin=1in
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes:
  - \usepackage{setspace}
  - \setstretch{1.36}
  - \setlength{\parskip}{8pt}
  - \setlength{\parindent}{0pt}
  - \setcounter{secnumdepth}{-1}
  - \usepackage{float}
  - \floatplacement{figure}{H}
  - \usepackage{caption}
  - \captionsetup{labelfont={bf,it}, textfont=it, justification=raggedright, singlelinecheck=false}
  - \usepackage{titlesec}
  - \titleformat{\section}{\bfseries\large}{}{0pt}{}
  - \titleformat{\subsection}{\bfseries\normalsize}{}{0pt}{}
  - \titleformat{\subsubsection}{\bfseries\small}{}{0pt}{}
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \makeatletter
  - \renewcommand{\maketitle}{\begin{titlepage}\centering\vspace*{2cm}{\fontsize{16}{21.76}\selectfont\bfseries\setlength{\parskip}{10.36pt}\@title\par}\vspace{1.5cm}\@author\par\vfill\@date\end{titlepage}}
  - \makeatother
---
"""


# ---------------------------------------------------------------------------
# Unicode -> LaTeX substitutions for Carlito glyph gaps
# ---------------------------------------------------------------------------

UNICODE_SUBS = [
    # Math symbols missing in Carlito
    ("≥", r"$\geq$"),
    ("≤", r"$\leq$"),
    ("≠", r"$\neq$"),
    ("≈", r"$\approx$"),
    ("∧", r"$\land$"),
    ("∨", r"$\lor$"),
    ("¬", r"$\neg$"),
    ("∈", r"$\in$"),
    ("⊆", r"$\subseteq$"),
    ("∅", r"$\emptyset$"),
    # Greek letters (Carlito lacks Greek block)
    ("ρ", r"$\rho$"),
    ("α", r"$\alpha$"),
    ("β", r"$\beta$"),
    ("σ", r"$\sigma$"),
    ("μ", r"$\mu$"),
    ("π", r"$\pi$"),
    ("Δ", r"$\Delta$"),
    # Subscripts
    ("ₜ", r"$_{t}$"),
    ("₁", r"$_{1}$"),
    ("₂", r"$_{2}$"),
    ("₃", r"$_{3}$"),
    # Superscripts (compounds typically rewritten ahead of this pass)
    ("⁻", r"$^{-}$"),
    # Arrows and shapes
    ("▶", r"$\blacktriangleright$"),
    ("→", r"$\rightarrow$"),
    ("←", r"$\leftarrow$"),
    # Unicode minus -> LaTeX minus
    ("−", r"$-$"),
]


# ---------------------------------------------------------------------------
# Symbol-name preprocessing
# ---------------------------------------------------------------------------
# The v1.3 source uses $C_P$ / $R_F$ math notation directly; no underscore
# rewriting needed. Table retained for parity with v16 pipeline.

SYMBOL_NAMES = []


# ---------------------------------------------------------------------------
# Compound rewrites (run BEFORE Unicode subs so e.g. 10⁻⁴ becomes 10^{-4}
# as a single LaTeX expression rather than 10$^{-}$4)
# ---------------------------------------------------------------------------

COMPOUND_REWRITES = [
    (r"10⁻⁴", r"$10^{-4}$"),
    (r"10⁻³", r"$10^{-3}$"),
    (r"10⁻²", r"$10^{-2}$"),
    (r"10⁻¹", r"$10^{-1}$"),
]


# ---------------------------------------------------------------------------
# Preprocessing pipeline
# ---------------------------------------------------------------------------

def preprocess_markdown(src_text: str) -> str:
    text = src_text

    # 1. Compound rewrites (specific multi-character patterns first)
    for pattern, replacement in COMPOUND_REWRITES:
        text = text.replace(pattern, replacement)

    # 2. Symbol names — whole-word boundary to avoid mid-word matches
    for pattern, replacement in SYMBOL_NAMES:
        text = re.sub(r"\b" + re.escape(pattern) + r"\b", replacement, text)

    # 3. Unicode -> LaTeX
    for char, replacement in UNICODE_SUBS:
        text = text.replace(char, replacement)

    return text


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build() -> None:
    if not SRC.exists():
        sys.exit(f"Source not found: {SRC}")

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    src_text = SRC.read_text(encoding="utf-8")
    processed = preprocess_markdown(src_text)

    full_md = YAML_HEADER + "\n" + processed
    PREPROCESSED.write_text(full_md, encoding="utf-8")
    print(f"Wrote preprocessed markdown: {PREPROCESSED}")

    cmd = [
        "pandoc",
        str(PREPROCESSED),
        "-o", str(OUTPUT_PDF),
        "--pdf-engine=xelatex",
        "--standalone",
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"pandoc/xelatex stderr:\n{result.stderr}", file=sys.stderr)
        sys.exit(f"Build failed (exit {result.returncode})")

    print(f"Built: {OUTPUT_PDF}")


if __name__ == "__main__":
    build()
