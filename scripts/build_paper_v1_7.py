#!/usr/bin/env python3
"""
build_paper_v1_7.py — AIAS v1.7 methodology paper PDF builder.

Compiles papers/v1_7/v1_7_ssrn_paper_draft.md → papers/v1_7/v1_7_ssrn_paper.pdf
via pandoc + xelatex with the Carlito-tuned preamble carried in the .md YAML.

Pipeline mirrors build_paper_v21.py:
  1. Read source .md
  2. Apply Unicode → LaTeX substitutions for Carlito glyph gaps (defensive)
  3. Write pre-processed temp .md
  4. Invoke pandoc with --pdf-engine=xelatex and --resource-path
  5. Output PDF

The source .md carries YAML frontmatter (mainfont Carlito, fontsize 11pt,
\\setstretch{1.36}, letterpaper margin 1in, \\renewcommand{\\maketitle}{}) plus
a custom \\begin{titlepage}...\\end{titlepage} block with one-page-fit overrides
(\\setstretch{1.0} + \\setlength{\\parskip}{0pt} local).

This builder is for the v1.7 methodology paper — no chart figures, text +
tables only. resource_path is retained for build-pattern consistency with the
phase paper builders.

Required:
  - pandoc with xelatex backend
  - Carlito font installed system-wide
  - pypdf (optional; used for final page-count report)

Usage:
  python build_paper_v1_7.py
  python build_paper_v1_7.py --keep-temp
  python build_paper_v1_7.py --source <path> --output <path>
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

AIAS_ROOT = Path.home() / "aias"
PAPER_DIR = AIAS_ROOT / "papers" / "v1_7"

DEFAULT_SOURCE = PAPER_DIR / "v1_7_cpc_consistency.md"
DEFAULT_OUTPUT = PAPER_DIR / "v1_7_cpc_consistency.pdf"
DEFAULT_TEMP = PAPER_DIR / "_v1_7_cpc_consistency_pre.md"

RESOURCE_PATH = str(PAPER_DIR)


# --- Unicode → LaTeX substitutions (Carlito glyph-gap defense) --------------
# Canonical dict from build_paper_v21.py; v1.7 source uses heavier math notation
# (δ, ⩾, etc.) so a few additions over the v21 baseline.

UNICODE_SUBS = {
    "ₜ": r"$_{t}$",                  # ₜ subscript t
    "∈": r"$\in$",                    # ∈ element of
    "∉": r"$\notin$",                 # ∉ not element of
    "∧": r"$\wedge$",                 # ∧ logical AND
    "∨": r"$\vee$",                   # ∨ logical OR
    "∶": r"$:$",                      # ∶ RATIO mark
    "⊆": r"$\subseteq$",              # ⊆ subset of or equal to
    "⊇": r"$\supseteq$",              # ⊇ superset of or equal to
    "∩": r"$\cap$",                   # ∩ intersection
    "∪": r"$\cup$",                   # ∪ union
    "✓": r"\checkmark",               # ✓ CHECK MARK
    "✗": r"$\times$",                 # ✗ BALLOT X
    "▶": r"$\blacktriangleright$",    # ▶
    "◀": r"$\blacktriangleleft$",     # ◀
    "⁰": r"$^{0}$",                   # ⁰
    "⁴": r"$^{4}$",                   # ⁴
    "⁵": r"$^{5}$",                   # ⁵
    "⁶": r"$^{6}$",                   # ⁶
    "⁷": r"$^{7}$",                   # ⁷
    "⁸": r"$^{8}$",                   # ⁸
    "⁹": r"$^{9}$",                   # ⁹
    "⁻": r"-",                         # ⁻ superscript minus (naked)
}


def apply_unicode_subs(text: str) -> tuple[str, dict]:
    report = {}
    for ch, replacement in UNICODE_SUBS.items():
        count = text.count(ch)
        if count > 0:
            text = text.replace(ch, replacement)
            report[ch] = count
    return text, report


def run_pandoc(source: Path, output: Path, resource_path: str) -> int:
    cmd = [
        "pandoc",
        "--pdf-engine=xelatex",
        f"--resource-path={resource_path}",
        str(source),
        "-o", str(output),
    ]
    print("[build_paper_v1_7] invoking pandoc:")
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AIAS v1.7 methodology paper PDF builder (pandoc + xelatex + Carlito)"
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE),
                        help="Source .md path. Default: papers/v1_7/v1_7_ssrn_paper_draft.md")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="Output PDF path. Default: papers/v1_7/v1_7_ssrn_paper.pdf")
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

    print(f"[build_paper_v1_7] source: {source}")
    print(f"[build_paper_v1_7] output: {output}")

    text = source.read_text(encoding="utf-8")
    text, sub_report = apply_unicode_subs(text)
    if sub_report:
        print("[build_paper_v1_7] Unicode → LaTeX substitutions applied:")
        for ch, count in sub_report.items():
            print(f"  U+{ord(ch):04X} ({ch}) × {count}")
    else:
        print("[build_paper_v1_7] no Carlito glyph-gap chars detected")

    temp.parent.mkdir(parents=True, exist_ok=True)
    temp.write_text(text, encoding="utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    rc = run_pandoc(temp, output, RESOURCE_PATH)
    if rc != 0:
        print(f"[build_paper_v1_7] pandoc returned {rc}", file=sys.stderr)
        return rc

    if not args.keep_temp:
        temp.unlink(missing_ok=True)

    final_pages = "?"
    try:
        from pypdf import PdfReader
        final_pages = len(PdfReader(str(output)).pages)
    except Exception:
        pass
    print(f"[build_paper_v1_7] ✓ PDF written: {output}  ({final_pages} pages)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
