#!/usr/bin/env python3
"""
AIAS v0.33 — SSRN Paper Builder
Thin pandoc wrapper (canonical pattern from v0.20/v0.21/v1.6/v0.22).
Reads source .md, applies Unicode→LaTeX substitutions, invokes pandoc
with xelatex, outputs PDF.

Usage:
  cd /Users/pablou/aias
  python3 scripts/build_paper_v0_33.py
"""

import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PIPELINE_ROOT = Path("/Users/pablou/aias")
PAPER_DIR = PIPELINE_ROOT / "papers" / "v0_33"
SOURCE_MD = PAPER_DIR / "v0_33_ssrn_paper_draft.md"
OUTPUT_PDF = PAPER_DIR / "v0_33_ssrn_paper.pdf"

# ---------------------------------------------------------------------------
# Unicode → LaTeX substitutions (Carlito glyph gaps)
# ---------------------------------------------------------------------------
UNICODE_SUBS = [
    ("\u2009", r"\,"),           # thin space
    ("\u2013", "--"),            # en dash
    ("\u2014", "---"),           # em dash
    ("\u2018", "`"),             # left single quote
    ("\u2019", "'"),             # right single quote / apostrophe
    ("\u201C", "``"),            # left double quote
    ("\u201D", "''"),            # right double quote
    ("\u2026", r"\ldots{}"),     # ellipsis
    ("\u2122", r"\textsuperscript{TM}"),  # ™
    ("\u00D7", r"$\times$"),    # ×
    ("\u2265", r"$\geq$"),      # ≥
    ("\u2264", r"$\leq$"),      # ≤
    ("\u2260", r"$\neq$"),      # ≠
    ("\u221E", r"$\infty$"),    # ∞
    ("\u2208", r"$\in$"),       # ∈
    ("\u2286", r"$\subseteq$"), # ⊆
    ("\u25B6", r"$\blacktriangleright$"),  # ▶
    ("\u2227", r"$\wedge$"),    # ∧
    ("\u2713", r"\checkmark"),   # ✓
    # CV.04 glyph gaps surfaced by xelatex/Carlito on the v0.33 source:
    ("ρ", r"$\rho$"),       # rho (19x; Carlito has no Greek)
    ("Δ", r"$\Delta$"),     # Delta (ΔCPC throughout; Carlito has no Greek)
    ("·", r"$\cdot$"),      # middle dot (0.5·SD tolerance)
    ("μ", r"$\mu$"),        # mu (CPC level/mean; Carlito has no Greek) — prose only; math uses \mu
    ("′", r"$'$"),          # prime (d-prime recognition sensitivity)
    ("−", "-"),             # minus sign -> ASCII hyphen
    ("≫", r"$\gg$"),        # much-greater-than
    ("→", r"$\rightarrow$"),# rightwards arrow
    ("≈", r"$\approx$"),    # almost-equal
    ("±", r"\textpm{}"),    # plus-minus (text-mode; $\pm$ breaks when followed by a digit in pandoc)
    ("₁", r"$_{1}$"),
    ("₂", r"$_{2}$"),
    ("₃", r"$_{3}$"),
    ("ₜ", r"$_{t}$"),
]


def apply_subs(text: str) -> str:
    """Apply Unicode→LaTeX substitutions."""
    for old, new in UNICODE_SUBS:
        text = text.replace(old, new)
    return text


def main():
    if not SOURCE_MD.exists():
        print(f"ERROR: Source not found: {SOURCE_MD}")
        sys.exit(1)

    # Read source
    raw = SOURCE_MD.read_text(encoding="utf-8")

    # Apply substitutions
    processed = apply_subs(raw)

    # Write temp file
    tmp = PAPER_DIR / "_build_tmp.md"
    tmp.write_text(processed, encoding="utf-8")

    # Invoke pandoc
    cmd = [
        "pandoc",
        str(tmp),
        "-o", str(OUTPUT_PDF),
        "--pdf-engine=xelatex",
        f"--resource-path={PAPER_DIR}",
        "--standalone",
    ]

    print(f"Building: {SOURCE_MD.name} → {OUTPUT_PDF.name}")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Clean up temp
    tmp.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"ERROR: pandoc failed (exit {result.returncode})")
        if result.stderr:
            print(result.stderr)
        sys.exit(1)

    print(f"✓ Built: {OUTPUT_PDF}")
    print(f"  Size: {OUTPUT_PDF.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
