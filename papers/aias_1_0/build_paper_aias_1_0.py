#!/usr/bin/env python3
"""
build_paper_aias_1_0.py — AIAS 1.0 synthesis paper PDF builder.

Compiles papers/aias_1_0/aias_1_0_synthesis_paper_draft.md →
papers/aias_1_0/aias_1_0_synthesis_paper.pdf via pandoc + xelatex with the
Carlito-tuned preamble carried in the .md YAML.

Pipeline mirrors build_paper_v1_6.py:
  1. Read source .md
  2. Apply Unicode → LaTeX substitutions for Carlito glyph gaps (defensive)
  3. Write pre-processed temp .md
  4. Invoke pandoc with --pdf-engine=xelatex and --resource-path
  5. Output PDF

The synthesis paper carries six chart figures (chart_01 through chart_06) at
reports/figs/aias_1_0/, so resource_path includes the figures directory in
addition to the paper directory. Otherwise identical to v1.6.

Usage:
  python build_paper_aias_1_0.py
  python build_paper_aias_1_0.py --keep-temp
  python build_paper_aias_1_0.py --source <path> --output <path>
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

AIAS_ROOT = Path.home() / "aias"
PAPER_DIR = AIAS_ROOT / "papers" / "aias_1_0"
FIGS_DIR  = AIAS_ROOT / "reports" / "figs" / "aias_1_0"

DEFAULT_SOURCE = PAPER_DIR / "aias_1_0_synthesis_paper_draft.md"
DEFAULT_OUTPUT = PAPER_DIR / "aias_1_0_synthesis_paper.pdf"
DEFAULT_TEMP   = PAPER_DIR / "_aias_1_0_synthesis_paper_pre.md"

RESOURCE_PATH = f"{PAPER_DIR}:{FIGS_DIR}"


# --- Unicode → LaTeX substitutions (Carlito glyph-gap defense) --------------
# Canonical dict from build_paper_v1_6.py.

UNICODE_SUBS = {
    "ₜ": r"$_{t}$",
    "∈": r"$\in$",
    "∉": r"$\notin$",
    "∧": r"$\wedge$",
    "∨": r"$\vee$",
    "∶": r"$:$",
    "⊆": r"$\subseteq$",
    "⊇": r"$\supseteq$",
    "∩": r"$\cap$",
    "∪": r"$\cup$",
    "✓": r"\checkmark",
    "✗": r"$\times$",
    "▶": r"$\blacktriangleright$",
    "◀": r"$\blacktriangleleft$",
    "⁰": r"$^{0}$",
    "⁴": r"$^{4}$",
    "⁵": r"$^{5}$",
    "⁶": r"$^{6}$",
    "⁷": r"$^{7}$",
    "⁸": r"$^{8}$",
    "⁹": r"$^{9}$",
    "⁻": r"-",
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
    print("[build_paper_aias_1_0] invoking pandoc:")
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AIAS 1.0 synthesis paper PDF builder (pandoc + xelatex + Carlito)"
    )
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--temp",   default=str(DEFAULT_TEMP))
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    source = Path(args.source).expanduser()
    output = Path(args.output).expanduser()
    temp   = Path(args.temp).expanduser()

    if not source.exists():
        print(f"ERROR: source .md not found at {source}", file=sys.stderr)
        return 2

    print(f"[build_paper_aias_1_0] source: {source}")
    print(f"[build_paper_aias_1_0] output: {output}")
    print(f"[build_paper_aias_1_0] resource path: {RESOURCE_PATH}")

    text = source.read_text(encoding="utf-8")
    text, sub_report = apply_unicode_subs(text)
    if sub_report:
        print("[build_paper_aias_1_0] Unicode → LaTeX substitutions applied:")
        for ch, count in sub_report.items():
            print(f"  U+{ord(ch):04X} ({ch}) × {count}")
    else:
        print("[build_paper_aias_1_0] no Carlito glyph-gap chars detected")

    temp.parent.mkdir(parents=True, exist_ok=True)
    temp.write_text(text, encoding="utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    rc = run_pandoc(temp, output, RESOURCE_PATH)
    if rc != 0:
        print(f"[build_paper_aias_1_0] pandoc returned {rc}", file=sys.stderr)
        return rc

    if not args.keep_temp:
        temp.unlink(missing_ok=True)

    final_pages = "?"
    try:
        from pypdf import PdfReader
        final_pages = len(PdfReader(str(output)).pages)
    except Exception:
        pass
    print(f"[build_paper_aias_1_0] ✓ PDF written: {output}  ({final_pages} pages)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
