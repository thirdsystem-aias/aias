#!/usr/bin/env python3
"""
build_paper_v0_20.py — Render v0.20 SSRN paper to PDF via pandoc + xelatex + Carlito.

Pipeline:
  1. Read v0_20_ssrn_paper_draft.md (source)
  2. Apply Unicode → LaTeX substitution table for glyphs Carlito lacks
  3. Write intermediate .build.md
  4. Invoke pandoc with xelatex backend + Carlito mainfont
  5. Output v0_20_ssrn_paper.pdf

Glyph substitutions:
  Carlito is missing several glyphs that appear in AIAS papers. These are
  replaced with LaTeX math-mode equivalents or fallback ASCII before pandoc
  parses the source. Critical substitutions:
    ₜ (U+209C subscript t)   → $_{t}$
    ∈ (U+2208)               → $\in$
    ⊆ (U+2286)               → $\subseteq$
    ▶ (U+25B6)               → $\\blacktriangleright$
    ⁻⁴ etc                   → math superscript fallback

The titlepage block is hand-authored in the source markdown (one-page-fit rule
per userMemories: local \\setstretch{1.0} + \\setlength{\\parskip}{0pt}
overrides inside \\begin{titlepage}). The header-includes block in the YAML
contains \\renewcommand{\\maketitle}{} to suppress pandoc's auto-titlepage.

Usage:
    python build_paper_v0_20.py
    python build_paper_v0_20.py --source <path>  --output <path>
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# --- Paths -------------------------------------------------------------------

DEFAULT_PAPER_DIR = Path.home() / "aias" / "papers" / "v0_20"
DEFAULT_SOURCE = DEFAULT_PAPER_DIR / "v0_20_ssrn_paper_draft.md"
DEFAULT_OUTPUT = DEFAULT_PAPER_DIR / "v0_20_ssrn_paper.pdf"
DEFAULT_RESOURCE_PATH = DEFAULT_PAPER_DIR  # for figure embeds


# --- Carlito glyph substitution table ---------------------------------------

# Carlito (the open-source Calibri metric-compatible font used by pandoc-xelatex
# in the AIAS pipeline) lacks several Unicode glyphs that appear in the paper.
# Replace with LaTeX equivalents (math-mode for math symbols; ASCII for noisy
# fallbacks) before pandoc parses the markdown source.

SUBSTITUTIONS = [
    # Subscripts / superscripts
    ("ₜ", r"$_{t}$"),
    ("₀", r"$_{0}$"),
    ("₁", r"$_{1}$"),
    ("₂", r"$_{2}$"),
    ("₃", r"$_{3}$"),
    ("₄", r"$_{4}$"),
    ("₅", r"$_{5}$"),
    ("₆", r"$_{6}$"),
    ("₇", r"$_{7}$"),
    ("₈", r"$_{8}$"),
    ("₉", r"$_{9}$"),
    ("⁻", r"$^{-}$"),
    ("⁰", r"$^{0}$"),
    ("¹", r"$^{1}$"),
    ("²", r"$^{2}$"),
    ("³", r"$^{3}$"),
    ("⁴", r"$^{4}$"),
    # Math relations / set theory
    ("∈", r"$\in$"),
    ("∉", r"$\notin$"),
    ("⊆", r"$\subseteq$"),
    ("⊂", r"$\subset$"),
    ("∧", r"$\wedge$"),
    ("∨", r"$\vee$"),
    ("∩", r"$\cap$"),
    ("∪", r"$\cup$"),
    ("≤", r"$\leq$"),
    ("≥", r"$\geq$"),
    ("≠", r"$\neq$"),
    ("≈", r"$\approx$"),
    ("±", r"$\pm$"),
    ("∞", r"$\infty$"),
    # Greek (only those Carlito lacks; lowercase Greek is generally present)
    ("ρ", r"$\rho$"),
    # Arrows / bullets / triangles
    ("▶", r"$\blacktriangleright$"),
    ("◀", r"$\blacktriangleleft$"),
    ("→", r"$\rightarrow$"),
    ("←", r"$\leftarrow$"),
    ("↔", r"$\leftrightarrow$"),
    ("⇒", r"$\Rightarrow$"),
    ("•", r"$\bullet$"),
    # Check / cross marks (used in v1.5 C2 verdict tables — Carlito gap)
    ("✓", r"$\checkmark$"),
    ("✗", r"$\times$"),
    # Math minus sign (U+2212), distinct from ASCII hyphen; Carlito gap
    ("−", r"$-$"),
    # Common quotes / dashes already render OK in Carlito; no substitution needed
]


def apply_substitutions(text: str) -> str:
    """Apply the Carlito-gap substitution table."""
    # Skip the YAML front-matter so the title and header-includes blocks
    # don't get mangled (LaTeX in those blocks is already escaped correctly).
    if text.startswith("---\n"):
        end_idx = text.find("\n---\n", 4)
        if end_idx > 0:
            front = text[: end_idx + 5]
            body = text[end_idx + 5 :]
        else:
            front, body = "", text
    else:
        front, body = "", text

    for src, dst in SUBSTITUTIONS:
        body = body.replace(src, dst)

    return front + body


# --- Pandoc invocation -------------------------------------------------------

def run_pandoc(source_path: Path, output_path: Path, resource_path: Path) -> int:
    """Invoke pandoc with the AIAS standard flag set."""
    if not shutil.which("pandoc"):
        print("ERROR: pandoc not found in PATH. Install via: brew install pandoc",
              file=sys.stderr)
        return 2

    cmd = [
        "pandoc",
        str(source_path),
        "-o", str(output_path),
        "--pdf-engine=xelatex",
        "--variable", "geometry:margin=1in",
        "--variable", "linkcolor:black",
        "--variable", "urlcolor:black",
        f"--resource-path={resource_path}",
        "--standalone",
    ]
    print("Running pandoc:")
    print("  " + " ".join(cmd))
    print()
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode


# --- Main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build v0.20 SSRN paper PDF from markdown source"
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE),
                        help=f"Source markdown (default: {DEFAULT_SOURCE})")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help=f"Output PDF (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--resource-path", default=None,
                        help="Resource path for figure embeds (default: source dir)")
    parser.add_argument("--keep-build-md", action="store_true",
                        help="Keep the intermediate .build.md file after rendering")
    args = parser.parse_args()

    source_path = Path(args.source).expanduser()
    output_path = Path(args.output).expanduser()
    resource_path = Path(args.resource_path).expanduser() if args.resource_path else source_path.parent

    if not source_path.exists():
        print(f"ERROR: source not found at {source_path}", file=sys.stderr)
        return 2

    print("AIAS v0.20 SSRN paper builder")
    print(f"  Source:   {source_path}")
    print(f"  Output:   {output_path}")
    print(f"  Figures:  {resource_path}")
    print()

    # Step 1: read source
    src_text = source_path.read_text(encoding="utf-8")
    print(f"  Source length: {len(src_text):,} chars")

    # Step 2: apply Carlito glyph substitutions
    build_text = apply_substitutions(src_text)
    if build_text != src_text:
        # Count substitutions (rough — diff of length doesn't capture all)
        print(f"  After substitutions: {len(build_text):,} chars")
    else:
        print(f"  No substitutions needed.")

    # Step 3: write intermediate .build.md
    build_path = source_path.with_suffix(".build.md")
    build_path.write_text(build_text, encoding="utf-8")
    print(f"  Intermediate: {build_path}")

    # Step 4: invoke pandoc
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print()
    rc = run_pandoc(build_path, output_path, resource_path)

    # Step 5: clean up
    if not args.keep_build_md and build_path.exists():
        try:
            build_path.unlink()
        except OSError:
            pass

    if rc == 0:
        print(f"\n✓ PDF written: {output_path}")
        print(f"  Size: {output_path.stat().st_size:,} bytes")
        print(f"\n  Eyeball check:")
        print(f"    open {output_path}")
        print(f"\n  Critical pages to verify:")
        print(f"    Page 1: titlepage fits on ONE page (no overflow to page 2)")
        print(f"    Page 2: abstract + keywords")
        print(f"    §3 Results: chart inclusions render at full width (if embedded)")
    else:
        print(f"\n✗ pandoc returned exit code {rc}")
        if build_path.exists():
            print(f"  Intermediate file preserved for debugging: {build_path}")

    return rc


if __name__ == "__main__":
    sys.exit(main())
