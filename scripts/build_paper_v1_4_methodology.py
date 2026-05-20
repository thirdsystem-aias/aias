#!/usr/bin/env python3
"""
build_paper_v1_4_methodology.py — Build v1.4 Methodology paper PDF.

Builds papers/v1_4_methodology/v1_4_methodology_paper_draft.md into a
publication-ready PDF using pandoc + xelatex.

Modeled on scripts/build_paper_presence_methodology.py (which built SSRN 6761698,
the v1.2 Methodology paper). Same styling foundation: Carlito mainfont, 11pt
body, 1.36 line stretch, 8pt parskip, 0 parindent, centered title page with
16pt bold title, float[H] placement, bold-italic caption labels, bold section
headings.

Unicode → LaTeX substitutions handle Carlito glyph gaps. The substitution table
is applied only to text outside math regions ($...$ inline math and $$...$$
display math), so LaTeX math expressions in the source are passed through
unchanged.

Output: papers/v1_4_methodology/v1_4_methodology_paper.pdf

Usage:
    python scripts/build_paper_v1_4_methodology.py
    python scripts/build_paper_v1_4_methodology.py --keep-tex   # preserve intermediates

Prerequisites:
    - pandoc (>= 2.0)
    - xelatex (TeX Live or MacTeX)
    - Carlito font (system-installed or in ~/Library/Fonts)
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


# ============================================================================
# Paths
# ============================================================================

ROOT         = Path.home() / "aias"
PAPER_DIR    = ROOT / "papers" / "v1_4_methodology"
SOURCE       = PAPER_DIR / "v1_4_methodology_paper_draft.md"
OUTPUT_PDF   = PAPER_DIR / "v1_4_methodology_paper.pdf"
HEADER_TEX   = PAPER_DIR / ".header_v1_4.tex"        # ephemeral
PROCESSED_MD = PAPER_DIR / ".v1_4_processed.md"       # ephemeral


# ============================================================================
# Unicode → LaTeX substitutions (applied outside math regions only)
# ============================================================================
#
# Carlito font lacks glyphs for some Unicode characters commonly used in
# scientific text. The substitution table converts these to LaTeX math-mode
# expressions where amsmath provides the rendering. Math-mode characters are
# always rendered via Computer Modern Math (or the configured math font),
# not Carlito, so glyph coverage is complete inside $...$ blocks.
#
# Adding a substitution: place the unicode character on the left, the LaTeX
# math expression (wrapped in $...$) on the right. Order matters — multi-char
# sequences must be listed before their single-char components.
# ============================================================================

UNICODE_SUBS = [
    # Subscripts (Carlito lacks the ₁–₉ glyphs entirely)
    ("ₜ", r"$_{t}$"),
    ("₁", r"$_{1}$"),
    ("₂", r"$_{2}$"),
    ("₃", r"$_{3}$"),
    ("₄", r"$_{4}$"),
    ("₅", r"$_{5}$"),
    # Superscripts
    ("⁻¹", r"$^{-1}$"),
    ("⁻²", r"$^{-2}$"),
    ("⁻³", r"$^{-3}$"),
    ("⁻⁴", r"$^{-4}$"),
    ("¹", r"$^{1}$"),
    ("²", r"$^{2}$"),
    ("³", r"$^{3}$"),
    # Set theory
    ("∈", r"$\in$"),
    ("∉", r"$\notin$"),
    ("⊆", r"$\subseteq$"),
    ("⊇", r"$\supseteq$"),
    ("⊂", r"$\subset$"),
    ("⊃", r"$\supset$"),
    ("∪", r"$\cup$"),
    ("∩", r"$\cap$"),
    ("∅", r"$\emptyset$"),
    # Inequalities
    ("≥", r"$\geq$"),
    ("≤", r"$\leq$"),
    ("≠", r"$\neq$"),
    ("≈", r"$\approx$"),
    # Operators
    ("×", r"$\times$"),
    ("÷", r"$\div$"),
    ("·", r"$\cdot$"),
    # Greek letters in body text (math-mode usage is left untouched)
    ("ρ", r"$\rho$"),
    ("σ", r"$\sigma$"),
    ("θ", r"$\theta$"),
    ("τ", r"$\tau$"),
    ("μ", r"$\mu$"),
    ("α", r"$\alpha$"),
    ("β", r"$\beta$"),
    ("γ", r"$\gamma$"),
    ("δ", r"$\delta$"),
    ("λ", r"$\lambda$"),
    # Triangles and markers
    ("▶", r"$\blacktriangleright$"),
    ("◀", r"$\blacktriangleleft$"),
    ("▲", r"$\blacktriangle$"),
    ("▼", r"$\blacktriangledown$"),
]


# ============================================================================
# LaTeX preamble — modeled on v1.2 Methodology paper build (SSRN 6761698)
# ============================================================================

PREAMBLE = r"""
% =====================================================================
% v1.4 Methodology paper preamble
% AIAS Presence Measurement Protocol — Recognition x Recall Decomposition
% =====================================================================

% --- Pandoc template fallbacks ----------------------------------------
% Pandoc's default LaTeX template references XMP metadata commands from
% the hyperxmp package (typically not in baseline MacTeX/BasicTeX). Define
% no-op fallbacks so the template compiles without requiring hyperxmp.
\providecommand{\xmpquote}[1]{#1}
\providecommand{\xmpcomma}{,}
\providecommand{\xmpcolon}{:}

% --- Line spacing (1.36 as specified by AIAS SSRN convention) ----------
\usepackage{setspace}
\setstretch{1.36}

% --- Body spacing: 8pt paragraph gap, no indent ------------------------
\setlength{\parskip}{8pt}
\setlength{\parindent}{0pt}

% --- Float placement: H = exact location (no floating) -----------------
\usepackage{float}
\floatplacement{figure}{H}
\floatplacement{table}{H}

% --- Caption styling: bold-italic label, italic text, ragged-right -----
\usepackage{caption}
\captionsetup{
    labelfont={bf,it},
    textfont=it,
    labelsep=period,
    justification=raggedright,
    singlelinecheck=false
}

% --- Section heading styling: bold ------------------------------------
\usepackage{titlesec}
\titleformat*{\section}{\large\bfseries}
\titleformat*{\subsection}{\normalsize\bfseries}
\titleformat*{\subsubsection}{\normalsize\bfseries\itshape}

% --- Math packages for formal definitions ------------------------------
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}

% --- Hyperref: no link decoration --------------------------------------
\usepackage[hidelinks]{hyperref}

% --- Microtype for typographic refinement ------------------------------
\usepackage{microtype}

% --- Lenient line breaking for paths/identifiers in body text ----------
% Long monospace strings (paths, constant names) don't break naturally.
% \sloppy and \emergencystretch let LaTeX use larger inter-word spacing
% when needed to avoid overfull boxes. This is the standard mitigation
% for technical-writing line overflow.
\sloppy
\setlength{\emergencystretch}{3em}

% --- Title formatting via titling package -----------------------------
% Avoid redefining \maketitle directly — pandoc's default template handles
% abstract emission separately (not via \@abstract), so a custom \maketitle
% that consumes \@abstract breaks the build. titling's pre/post hooks
% adjust title formatting without disturbing pandoc's template path.
\usepackage{titling}
\pretitle{\begin{center}\fontsize{16}{21.76}\selectfont\bfseries}
\posttitle{\par\end{center}\vskip 1.5em}
\preauthor{\begin{center}\normalsize}
\postauthor{\par\end{center}\vskip 1em}
\predate{\begin{center}}
\postdate{\par\end{center}\clearpage}

% --- Abstract styling (pandoc emits \begin{abstract}...\end{abstract} when
%     the YAML 'abstract' field is present; restyle that block).
\renewenvironment{abstract}
    {\begin{center}\textbf{\large Abstract}\end{center}%
     \begin{quote}\noindent\ignorespaces}
    {\end{quote}\vskip 1em}
"""


# ============================================================================
# Helpers
# ============================================================================

def apply_unicode_subs(text: str) -> str:
    """
    Apply Unicode → LaTeX substitutions to all non-math regions of the text.

    Math regions are protected: inline $...$ and display $$...$$ blocks are
    passed through unchanged. This prevents double-conversion of math symbols
    that are already in LaTeX form in the source.
    """
    # Split into alternating non-math / math chunks. The regex captures
    # display math ($$...$$) and inline math ($...$). Display math is matched
    # greedily first so $$ isn't mis-tokenized as two adjacent $.
    pattern = re.compile(r"(\$\$.*?\$\$|\$[^\$\n]+?\$)", re.DOTALL)
    parts = pattern.split(text)

    result = []
    for part in parts:
        if part.startswith("$"):
            # Math region: passthrough untouched.
            result.append(part)
            continue
        # Non-math region: apply Unicode → LaTeX substitutions.
        for unicode_char, latex_repl in UNICODE_SUBS:
            part = part.replace(unicode_char, latex_repl)
        result.append(part)

    return "".join(result)


def check_prereqs() -> None:
    """Verify pandoc and xelatex are installed and accessible on PATH."""
    missing = []
    for tool in ("pandoc", "xelatex"):
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        sys.exit(
            f"ERROR: required tool(s) not found on PATH: {', '.join(missing)}\n"
            f"  Install pandoc:  brew install pandoc\n"
            f"  Install xelatex: MacTeX (full) or BasicTeX (then `tlmgr install xelatex`)"
        )


def check_carlito() -> bool:
    """
    Heuristically check whether Carlito is installed. Returns True if found,
    False otherwise. False is non-fatal — xelatex's fontspec will produce a
    more authoritative error if Carlito is truly unavailable.
    """
    try:
        result = subprocess.run(
            ["fc-list", ":family"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return "Carlito" in result.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    # fc-list not available (common on macOS without fontconfig) — assume present.
    return True


# ============================================================================
# Main build pipeline
# ============================================================================

def build() -> None:
    if not SOURCE.exists():
        sys.exit(f"ERROR: paper source not found at {SOURCE}")

    check_prereqs()
    if not check_carlito():
        print("WARNING: Carlito font not detected via fc-list. "
              "If xelatex fails on font lookup, install Carlito system-wide "
              "or copy the .ttf files to ~/Library/Fonts/.")

    # Read source markdown, apply Unicode substitutions, write processed copy
    src_text = SOURCE.read_text(encoding="utf-8")
    processed_text = apply_unicode_subs(src_text)
    PROCESSED_MD.write_text(processed_text, encoding="utf-8")

    n_subs = sum(1 for u, _ in UNICODE_SUBS if u in src_text)
    print(f"Source:    {SOURCE.relative_to(ROOT)}")
    print(f"Processed: {PROCESSED_MD.relative_to(ROOT)} "
          f"(applied {n_subs} unique Unicode substitutions outside math regions)")

    # Write LaTeX preamble
    HEADER_TEX.write_text(PREAMBLE, encoding="utf-8")
    print(f"Preamble:  {HEADER_TEX.relative_to(ROOT)}")

    # Pandoc command
    cmd = [
        "pandoc",
        str(PROCESSED_MD),
        "-o", str(OUTPUT_PDF),
        "--pdf-engine=xelatex",
        "-V", "mainfont=Carlito",
        "-V", "fontsize=11pt",
        "-V", "geometry:margin=1in",
        "-V", "linkcolor=black",
        "-H", str(HEADER_TEX),
        "--standalone",
        "--from", "markdown+yaml_metadata_block+tex_math_dollars",
    ]

    print(f"\nRunning pandoc...")
    print(f"  {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("=" * 60)
        print("PANDOC FAILED")
        print("=" * 60)
        if result.stdout:
            print(f"\nstdout:\n{result.stdout}")
        if result.stderr:
            print(f"\nstderr:\n{result.stderr}")
        sys.exit(f"\nERROR: pandoc exited with code {result.returncode}")

    if not OUTPUT_PDF.exists():
        sys.exit(f"ERROR: pandoc reported success but {OUTPUT_PDF} was not created")

    size_kb = OUTPUT_PDF.stat().st_size / 1024
    print(f"Build complete.")
    print(f"  Output: {OUTPUT_PDF}")
    print(f"  Size:   {size_kb:.1f} KB")
    print(f"\nNext: open the PDF for visual proofread.")
    print(f"  open {OUTPUT_PDF}")


def cleanup(keep_tex: bool) -> None:
    if keep_tex:
        print(f"\n(--keep-tex set; intermediates preserved at {HEADER_TEX.name} "
              f"and {PROCESSED_MD.name})")
        return
    for f in (HEADER_TEX, PROCESSED_MD):
        if f.exists():
            f.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build v1.4 Methodology paper PDF (pandoc + xelatex + Carlito)",
    )
    parser.add_argument(
        "--keep-tex", action="store_true",
        help="Preserve intermediate .header_v1_4.tex and .v1_4_processed.md "
             "files for debugging.",
    )
    args = parser.parse_args()

    try:
        build()
    finally:
        cleanup(args.keep_tex)


if __name__ == "__main__":
    main()
