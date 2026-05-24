#!/usr/bin/env python3
"""
build_paper_v21.py — AIAS v0.21 SSRN paper PDF builder.

Compiles papers/v0_21/v0_21_ssrn_paper_draft.md → papers/v0_21/v0_21_ssrn_paper.pdf
via pandoc + xelatex with the Carlito-tuned preamble carried in the .md YAML.

Pipeline:
  1. Read source .md
  2. Apply Unicode → LaTeX substitutions for Carlito glyph gaps (defensive)
  3. Write pre-processed temp .md
  4. Invoke pandoc with --pdf-engine=xelatex and --resource-path
  5. Output PDF to papers/v0_21/v0_21_ssrn_paper.pdf

The source .md carries:
  - YAML frontmatter (mainfont Carlito, fontsize 11pt, \\setstretch{1.36},
    \\parskip 8pt, \\parindent 0pt, float/caption/titlesec packages,
    \\renewcommand{\\maketitle}{})
  - Custom \\begin{titlepage}...\\end{titlepage} block with one-page-fit
    overrides (\\setstretch{1.0} + \\setlength{\\parskip}{0pt} local)
  - Inline figure references at section 3 Results:
    ![cap](../../reports/figs/v21/chart_NN.pdf){#fig:label width=100%}
  - Inline bibliography (no external .bib)

Required:
  - pandoc with xelatex backend
  - Carlito font installed system-wide (macOS: Font Book; Linux: fonts-carlito)
  - pypdf (optional; used for final page-count report)

Usage:
  python build_paper_v21.py                                   # default paths
  python build_paper_v21.py --keep-temp                       # retain pre-processed .md
  python build_paper_v21.py --source <path> --output <path>   # override paths
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# --- Configuration -----------------------------------------------------------

AIAS_ROOT = Path.home() / "aias"
PAPER_DIR = AIAS_ROOT / "papers" / "v0_21"

DEFAULT_SOURCE = PAPER_DIR / "v0_21_ssrn_paper_draft.md"
DEFAULT_OUTPUT = PAPER_DIR / "v0_21_ssrn_paper.pdf"
DEFAULT_TEMP = PAPER_DIR / "_v0_21_ssrn_paper_pre.md"

# Pandoc resource path — figure refs in the .md use ../../reports/figs/v21/...
# pandoc resolves these relative to --resource-path.
RESOURCE_PATH = str(PAPER_DIR)

# --- Unicode → LaTeX substitutions (Carlito glyph-gap defense) --------------
#
# Carlito ships without these glyphs; xelatex would emit tofu (▢) if it
# encountered them in a Carlito text run. The substitution lifts them into
# math mode where the math font supplies the glyph.
#
# This is a defensive layer — the canonical v0.20 source had none of these
# present. But the construct (e.g., t-subscripts, set notation, ranked-list
# triangles) can creep in via copy-paste from notebooks or LLM outputs, so
# we sub at build time rather than relying on author discipline.

UNICODE_SUBS = {
    "\u209C": r"$_{t}$",                  # ₜ subscript t
    "\u2208": r"$\in$",                    # ∈ element of
    "\u2209": r"$\notin$",                 # ∉ not element of
    "\u2227": r"$\wedge$",                 # ∧ logical AND  (hypothesis defs)
    "\u2228": r"$\vee$",                   # ∨ logical OR
    "\u2236": r"$:$",                      # ∶ RATIO mark   (channel splits)
    "\u2286": r"$\subseteq$",              # ⊆ subset of or equal to
    "\u2287": r"$\supseteq$",              # ⊇ superset of or equal to
    "\u2229": r"$\cap$",                   # ∩ intersection
    "\u222A": r"$\cup$",                   # ∪ union
    "\u2713": r"\checkmark",               # ✓ CHECK MARK   (table pass marker)
    "\u2717": r"$\times$",                 # ✗ BALLOT X     (table fail marker)
    "\u25B6": r"$\blacktriangleright$",    # ▶ play-style triangle
    "\u25C0": r"$\blacktriangleleft$",    # ◀
    "\u2070": r"$^{0}$",                   # ⁰ superscript zero
    "\u2074": r"$^{4}$",                   # ⁴
    "\u2075": r"$^{5}$",                   # ⁵
    "\u2076": r"$^{6}$",                   # ⁶
    "\u2077": r"$^{7}$",                   # ⁷
    "\u2078": r"$^{8}$",                   # ⁸
    "\u2079": r"$^{9}$",                   # ⁹
    "\u207B": r"-",                         # ⁻ superscript minus (naked)
    # Compound forms like 10⁻⁴ are better handled in the .md by rewriting to
    # decimal (0.0001) or scientific (1e-4); the naked-⁻ sub above is a
    # last-resort fallback.
}


def apply_unicode_subs(text: str) -> tuple[str, dict]:
    """Apply defensive Unicode → LaTeX substitutions. Returns (text, report)."""
    report = {}
    for ch, replacement in UNICODE_SUBS.items():
        count = text.count(ch)
        if count > 0:
            text = text.replace(ch, replacement)
            report[ch] = count
    return text, report


# --- Pandoc invocation -------------------------------------------------------

def run_pandoc(source: Path, output: Path, resource_path: str) -> int:
    """Invoke pandoc with the canonical AIAS SSRN flags."""
    cmd = [
        "pandoc",
        "--pdf-engine=xelatex",
        f"--resource-path={resource_path}",
        str(source),
        "-o", str(output),
    ]
    print(f"[build_paper_v21] invoking pandoc:")
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


# --- Main --------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="AIAS v0.21 SSRN paper PDF builder (pandoc + xelatex + Carlito)"
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE),
                        help="Source .md path. Default: papers/v0_21/v0_21_ssrn_paper_draft.md")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="Output PDF path. Default: papers/v0_21/v0_21_ssrn_paper.pdf")
    parser.add_argument("--temp", default=str(DEFAULT_TEMP),
                        help="Pre-processed temp .md path.")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Retain the pre-processed temp .md for debugging.")
    args = parser.parse_args()

    source = Path(args.source).expanduser()
    output = Path(args.output).expanduser()
    temp = Path(args.temp).expanduser()

    if not source.exists():
        print(f"ERROR: source .md not found at {source}", file=sys.stderr)
        return 2

    print(f"[build_paper_v21] source: {source}")
    print(f"[build_paper_v21] output: {output}")

    # Stage 1 — Unicode subs
    text = source.read_text(encoding="utf-8")
    text, sub_report = apply_unicode_subs(text)
    if sub_report:
        print(f"[build_paper_v21] Unicode → LaTeX substitutions applied:")
        for ch, count in sub_report.items():
            print(f"  U+{ord(ch):04X} ({ch}) × {count}")
    else:
        print(f"[build_paper_v21] no Carlito glyph-gap chars detected")

    temp.parent.mkdir(parents=True, exist_ok=True)
    temp.write_text(text, encoding="utf-8")

    # Stage 2 — pandoc
    output.parent.mkdir(parents=True, exist_ok=True)
    rc = run_pandoc(temp, output, RESOURCE_PATH)
    if rc != 0:
        print(f"[build_paper_v21] pandoc returned {rc}", file=sys.stderr)
        return rc

    # Stage 3 — cleanup
    if not args.keep_temp:
        temp.unlink(missing_ok=True)

    # Final report
    final_pages = "?"
    try:
        from pypdf import PdfReader
        final_pages = len(PdfReader(str(output)).pages)
    except Exception:
        pass
    print(f"[build_paper_v21] ✓ PDF written: {output}  ({final_pages} pages)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
