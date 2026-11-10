#!/usr/bin/env python3
"""
AIAS v1.10 (Ranking, Paper A) — SSRN paper builder.
Thin pandoc wrapper (canonical pattern of v0.20/v0.21/v1.6/v0.22/v1.9): reads the source
.md, applies the Unicode -> LaTeX substitutions for Carlito glyph gaps, runs pandoc with
xelatex and writes the PDF next to the source.

Usage (from any directory):
  python3 papers/v1_10/build_paper_v1_10.py
Paths resolve from this file, so the build stays inside the checkout it is run from
(the v1.10 worktree), never the main working tree.
"""

import subprocess
import sys
from pathlib import Path

PAPER_DIR = Path(__file__).resolve().parent
SOURCE_MD = PAPER_DIR / "v1_10_ssrn_paper_draft.md"
OUTPUT_PDF = PAPER_DIR / "v1_10_ssrn_paper.pdf"

# Unicode -> LaTeX substitutions (Carlito glyph gaps; canonical dict of CLAUDE.md plus
# the v1.9 additions). Extend on every new xelatex "Missing character" warning.
UNICODE_SUBS = [
    (" ", r"\,"),                     # thin space
    ("–", "--"),                      # en dash
    ("—", "---"),                     # em dash
    ("‘", "`"),                       # left single quote
    ("’", "'"),                       # right single quote / apostrophe
    ("“", "``"),                      # left double quote
    ("”", "''"),                      # right double quote
    ("…", r"\ldots{}"),               # ellipsis
    ("™", r"\textsuperscript{TM}"),   # trademark
    ("×", r"$\times$"),               # multiplication sign
    ("≥", r"$\geq$"),                 # >=
    ("≤", r"$\leq$"),                 # <=
    ("≠", r"$\neq$"),                 # !=
    ("∞", r"$\infty$"),               # infinity
    ("∈", r"$\in$"),                  # element of
    ("⊆", r"$\subseteq$"),            # subset or equal
    ("∧", r"$\wedge$"),               # logical and
    ("∶", r"$:$"),                    # ratio
    ("✓", r"\checkmark"),             # check mark
    ("✗", r"$\times$"),               # ballot x
    ("▶", r"$\blacktriangleright$"),  # black right triangle
    ("ₜ", r"$_{t}$"),                 # subscript t
    ("π̂", r"$\hat\pi$"),                   # pi-hat (before the bare pi)
    ("ρ", r"$\rho$"),                      # Carlito has no Greek
    ("φ", r"$\varphi$"),
    ("τ", r"$\tau$"),
    ("μ", r"$\mu$"),
    ("Δ", r"$\Delta$"),
    ("·", r"$\cdot$"),                     # middle dot
    ("′", r"$'$"),                         # prime
    ("−", "-"),                            # minus sign -> hyphen
    ("≫", r"$\gg$"),
    ("→", r"$\rightarrow$"),
    ("≈", r"$\approx$"),
    ("±", r"\textpm{}"),
    ("₁", r"$_{1}$"),
    ("₂", r"$_{2}$"),
    ("₃", r"$_{3}$"),
    ("⁻", "-"),
    ("⁰", r"$^{0}$"), ("¹", r"$^{1}$"), ("²", r"$^{2}$"), ("³", r"$^{3}$"), ("⁴", r"$^{4}$"),
    ("⁵", r"$^{5}$"), ("⁶", r"$^{6}$"), ("⁷", r"$^{7}$"), ("⁸", r"$^{8}$"), ("⁹", r"$^{9}$"),
]


def apply_subs(text: str) -> str:
    for old, new in UNICODE_SUBS:
        text = text.replace(old, new)
    return text


def main() -> int:
    if not SOURCE_MD.exists():
        print(f"ERROR: source not found: {SOURCE_MD}")
        return 1
    tmp = PAPER_DIR / "_build_tmp.md"
    tmp.write_text(apply_subs(SOURCE_MD.read_text(encoding="utf-8")), encoding="utf-8")
    cmd = ["pandoc", str(tmp), "-o", str(OUTPUT_PDF), "--pdf-engine=xelatex",
           f"--resource-path={PAPER_DIR}", "--standalone"]
    print(f"Building: {SOURCE_MD.name} -> {OUTPUT_PDF.name}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    tmp.unlink(missing_ok=True)
    if result.stderr:
        missing = [l for l in result.stderr.splitlines() if "Missing character" in l]
        print("\n".join(missing) if missing else result.stderr[-3000:])
    if result.returncode != 0:
        print(f"ERROR: pandoc failed (exit {result.returncode})")
        return 1
    print(f"Built: {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
