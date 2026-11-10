#!/usr/bin/env python3
"""
AIAS combined v0.27 + v0.28 validity paper (program study 67) - SSRN paper builder.
Thin pandoc wrapper on the v0.28 template (scripts/build_paper_v0_28.py): reads the
source .md, applies the Carlito Unicode->LaTeX substitutions, runs pandoc with
xelatex, writes the PDF. No LaTeX is generated from Python.

The repository root is derived from this file's location (papers/v0_27_28/ ->
root), so the build writes into whichever checkout it is run from (here the
v0.27-28-combined worktree), never into a hard-coded /Users/pablou/aias.

Usage:
  python3 papers/v0_27_28/build_paper_v0_27_28.py
"""

import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (root = two levels above papers/v0_27_28/)
# ---------------------------------------------------------------------------
PAPER_DIR = Path(__file__).resolve().parent
PIPELINE_ROOT = PAPER_DIR.parents[1]
SOURCE_MD = PAPER_DIR / "v0_27_28_combined_validity_paper.md"
OUTPUT_PDF = PAPER_DIR / "v0_27_28_ssrn_paper.pdf"

# ---------------------------------------------------------------------------
# Unicode -> LaTeX substitutions (Carlito glyph gaps); v0.28 set, unchanged order
# ---------------------------------------------------------------------------
UNICODE_SUBS = [
    (" ", r"\,"),           # thin space
    ("–", "--"),            # en dash
    ("—", "---"),           # em dash
    ("‘", "`"),             # left single quote
    ("’", "'"),             # right single quote / apostrophe
    ("“", "``"),            # left double quote
    ("”", "''"),            # right double quote
    ("…", r"\ldots{}"),     # ellipsis
    ("™", r"\textsuperscript{TM}"),  # TM
    ("×", r"$\times$"),     # multiplication sign
    ("≥", r"$\geq$"),       # >=
    ("≤", r"$\leq$"),       # <=
    ("≠", r"$\neq$"),       # !=
    ("∞", r"$\infty$"),     # infinity
    ("∈", r"$\in$"),        # element of
    ("⊆", r"$\subseteq$"),  # subset or equal
    ("▶", r"$\blacktriangleright$"),
    ("∧", r"$\wedge$"),
    ("✓", r"\checkmark"),
    ("ρ", r"$\rho$"),       # rho (Carlito has no Greek)
    ("′", r"$'$"),          # prime (d-prime)
    ("−", "-"),             # minus sign -> ASCII hyphen
    ("≫", r"$\gg$"),        # much greater than
    ("→", r"$\rightarrow$"),
    ("≈", r"$\approx$"),
    ("±", r"\textpm{}"),    # plus-minus (text mode)
    ("₁", r"$_{1}$"),
    ("₂", r"$_{2}$"),
    ("₃", r"$_{3}$"),
    ("ₜ", r"$_{t}$"),
]


def apply_subs(text: str) -> str:
    for old, new in UNICODE_SUBS:
        text = text.replace(old, new)
    return text


def main() -> int:
    if not SOURCE_MD.exists():
        print(f"ERROR: source not found: {SOURCE_MD}")
        return 1
    processed = apply_subs(SOURCE_MD.read_text(encoding="utf-8"))
    tmp = PAPER_DIR / "_build_tmp.md"
    tmp.write_text(processed, encoding="utf-8")
    cmd = [
        "pandoc", str(tmp),
        "-o", str(OUTPUT_PDF),
        "--pdf-engine=xelatex",
        f"--resource-path={PIPELINE_ROOT}:{PAPER_DIR}",
        "--standalone",
    ]
    print(f"Building: {SOURCE_MD.name} -> {OUTPUT_PDF.name} (root {PIPELINE_ROOT})")
    # cwd = repo root so figure paths (papers/..., reports/figs/...) resolve
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PIPELINE_ROOT)
    tmp.unlink(missing_ok=True)
    if result.stderr:
        print(result.stderr)
    if result.returncode != 0:
        print(f"ERROR: pandoc failed (exit {result.returncode})")
        return 1
    print(f"Built: {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
