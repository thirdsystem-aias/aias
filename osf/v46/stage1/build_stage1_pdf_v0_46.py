#!/usr/bin/env python3
"""build_stage1_pdf_v0_46.py -- AIAS(TM) v0.46 (#76) Stage 1 Registered Report PDF builder (PCI RR).

Compiles osf/v46/stage1/stage1_manuscript_rN.md -> stage1_manuscript_rN.pdf with the house academic
pipeline (CLAUDE.md, "SSRN paper build": pandoc + xelatex + Carlito, 11pt, letterpaper, 1in margins,
\\setstretch{1.36}, \\parskip 8pt, \\parindent 0pt, booktabs/caption/float), plus continuous line numbers
(lineno), which PCI RR asks for so reviewers can cite lines.

The manuscript is not changed: its YAML carries only title, author and date; everything else (fonts,
geometry, packages) is passed here on the pandoc command line and in a generated header file.
The headings already carry their own numbers, so pandoc's section numbering stays off.
Reader extensions: tex_math_dollars off (every $ in the text is money, US$); raw_html off (the probes'
"CHOICE: <brand name>" must print, not vanish as an HTML tag); hard_line_breaks on (the probe texts of
Section 3.5 and the affiliation block are line-for-line; every other paragraph is one source line);
lists_without_preceding_blankline on (several lists follow their lead-in line directly).

No model is called; nothing is read but the manuscript.

Usage:
  python3 build_stage1_pdf_v0_46.py                       # r2 (default)
  python3 build_stage1_pdf_v0_46.py --source stage1_manuscript_r2.md --output stage1_manuscript_r2.pdf
  python3 build_stage1_pdf_v0_46.py --keep-temp           # keep the pre-processed .md and header .tex
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE / "stage1_manuscript_r2.md"

MAINFONT = "Carlito"           # house academic font (CLAUDE.md, SSRN paper build)
MONOFONT = "Menlo"             # covers the Unicode used inside code spans; Latin Modern Mono does not

# Carlito glyph-gap defence (house dict, CLAUDE.md / build_paper_v1_7.py), restricted to characters that
# xelatex reports missing for this manuscript. Applied outside code spans only.
UNICODE_SUBS = {
    "d̄": r"\ensuremath{\bar{d}}",       # d + combining macron (H5's mean difference)
    "π̂": r"\ensuremath{\hat{\pi}}",  # pi + combining circumflex (recall Presence)
    "∈": r"\ensuremath{\in}",
}

HEADER_TEX = r"""
\usepackage{setspace}
\setstretch{1.36}
\setlength{\parskip}{8pt}
\setlength{\parindent}{0pt}
\usepackage{float}
\floatplacement{figure}{H}
\usepackage{booktabs}
\usepackage{caption}
\captionsetup{labelfont={bf,it},textfont=it,justification=raggedright,singlelinecheck=false,skip=4pt}
\usepackage{lineno}
\renewcommand\linenumberfont{\normalfont\scriptsize\sffamily\color{gray}}
\usepackage{xcolor}
\AtBeginDocument{\linenumbers}
\widowpenalty10000
\clubpenalty10000
\sloppy
\setlength{\emergencystretch}{3em}
\usepackage{pdflscape}
\newcommand{\blandscape}{\begin{landscape}}
\newcommand{\elandscape}{\end{landscape}}
"""

# Layout only (no text changes). The seven-column study design table (PCI RR's required table) is set on a
# landscape page in footnotesize; tables whose columns differ much in length get relative widths (pandoc reads
# them from the dash counts of the separator row).
LANDSCAPE_SECTIONS = ["## 6. Study design summary table"]
TABLE_WIDTHS = {  # header row prefix -> dash counts per column
    "| # | Question | Decision": [3, 14, 60, 16],
}


def layout(text: str) -> str:
    lines = text.split("\n")
    for head, widths in TABLE_WIDTHS.items():
        idx = [i for i, l in enumerate(lines) if l.startswith(head)]
        assert len(idx) == 1, head
        sep = lines[idx[0] + 1]
        assert sep.startswith("|-") and sep.count("|") == len(widths) + 1, sep
        lines[idx[0] + 1] = "|" + "|".join("-" * w for w in widths) + "|"
    for head in LANDSCAPE_SECTIONS:
        i = lines.index(head)
        j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith("|"))
        k = next(k for k in range(j, len(lines)) if not lines[k].startswith("|"))
        lines[k:k] = ["", r"\normalsize", r"\elandscape", ""]
        lines[j:j] = [r"\footnotesize", ""]
        lines[i:i] = [r"\blandscape", ""]
    return "\n".join(lines)


CODE_SPAN = re.compile(r"(`[^`\n]+`)")


def apply_subs(text: str) -> tuple[str, dict]:
    report: dict = {}
    parts = CODE_SPAN.split(text)
    for i, part in enumerate(parts):
        if i % 2 == 1:          # inside a code span: leave untouched
            continue
        for ch, rep in UNICODE_SUBS.items():
            n = part.count(ch)
            if n:
                part = part.replace(ch, rep)
                report[ch] = report.get(ch, 0) + n
        parts[i] = part
    return "".join(parts), report


def build(source: Path, output: Path, keep_temp: bool) -> int:
    if shutil.which("pandoc") is None or shutil.which("xelatex") is None:
        print("ERROR: pandoc and xelatex are required", file=sys.stderr)
        return 2
    text, rep = apply_subs(layout(source.read_text(encoding="utf-8")))
    for ch, n in rep.items():
        cps = " ".join(f"U+{ord(c):04X}" for c in ch)
        print(f"[stage1-pdf] {cps} ({ch}) x {n} substituted")
    temp_md = output.with_name("_" + output.stem + "_pre.md")
    header = output.with_name("_" + output.stem + "_header.tex")
    temp_md.write_text(text, encoding="utf-8")
    header.write_text(HEADER_TEX, encoding="utf-8")
    cmd = [
        "pandoc", str(temp_md),
        "--from=markdown-tex_math_dollars-raw_html+hard_line_breaks+lists_without_preceding_blankline",
        "--pdf-engine=xelatex",
        f"--resource-path={source.parent}",
        "-H", str(header),
        "-V", f"mainfont={MAINFONT}",
        "-V", f"monofont={MONOFONT}",
        "-V", "monofontoptions=Scale=0.85",
        "-V", "fontsize=11pt",
        "-V", "geometry=letterpaper,margin=1in",
        "-V", "colorlinks=true",
        "-V", "linkcolor=black", "-V", "urlcolor=blue",
        "-o", str(output),
    ]
    print("[stage1-pdf] $ " + " ".join(cmd))
    rc = subprocess.run(cmd).returncode
    if not keep_temp:
        temp_md.unlink(missing_ok=True)
        header.unlink(missing_ok=True)
    if rc != 0:
        print(f"[stage1-pdf] pandoc returned {rc}", file=sys.stderr)
        return rc
    try:
        from pypdf import PdfReader
        print(f"[stage1-pdf] {output} ({len(PdfReader(str(output)).pages)} pages)")
    except ImportError:
        print(f"[stage1-pdf] {output}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="AIAS v0.46 (#76) Stage 1 manuscript PDF (PCI RR; pandoc + xelatex + Carlito)")
    ap.add_argument("--source", default=str(DEFAULT_SOURCE))
    ap.add_argument("--output", default=None, help="default: the source name with .pdf")
    ap.add_argument("--keep-temp", action="store_true")
    a = ap.parse_args()
    src = Path(a.source)
    if not src.is_absolute():
        src = (HERE / src) if (HERE / src).exists() else src.resolve()
    if not src.exists():
        print(f"ERROR: source not found: {src}", file=sys.stderr)
        return 2
    out = Path(a.output) if a.output else src.with_suffix(".pdf")
    if not out.is_absolute():
        out = HERE / out
    return build(src, out, a.keep_temp)


if __name__ == "__main__":
    sys.exit(main())
