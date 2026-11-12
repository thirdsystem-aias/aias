#!/usr/bin/env python3
"""
AIAS AIAS 6.0 Preview (AIAS 6.0 Preview) -- paper builder (thin pandoc wrapper; forked from the t4-paper builder).
Reads the FILLED paper (papers/aias_6_0_preview/aias_6_0_preview_paper_draft.md, written by papers/aias_6_0_preview/fill_paper_aias_6_0_preview.py),
applies the Unicode->LaTeX substitutions for Carlito glyph gaps, runs pandoc + xelatex, writes the PDF.

Refuses to build a source that still contains template syntax ({{, {%), and refuses a source whose filled
provenance says it is synthetic unless --watermark is given (the stamp goes on every page).

Usage (real run):
  python3 scripts/build_paper_aias_6_0_preview.py
Synthetic test:
  python3 scripts/build_paper_aias_6_0_preview.py --source /tmp/aias6_pipeline_test/paper/aias_6_0_preview_paper_draft.md \
      --output /tmp/aias6_pipeline_test/paper/aias_6_0_preview_paper.pdf --watermark "SYNTHETIC TEST — NOT RESULTS"
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER_DIR = ROOT / "papers" / "aias_6_0_preview"
sys.path.insert(0, str(ROOT / "scripts"))

# Unicode -> LaTeX substitutions (Carlito glyph gaps): the v0.41/v0.42 list, plus ₄ ₅ ₆ for t4-t6.
# Curly quotes ‘ ’ “ ” are deliberately NOT substituted: Carlito has the glyphs, and the old ` / `` / '' forms
# were read by pandoc as code-span openers (quoted words garbled, text swallowed).
UNICODE_SUBS = [
    (" ", r"\,"),
    ("–", "--"),
    ("—", "---"),
    ("…", r"\ldots{}"),
    ("™", r"\textsuperscript{TM}"),
    ("×", r"$\times$"),
    ("≥", r"$\geq$"),
    ("≤", r"$\leq$"),
    ("≠", r"$\neq$"),
    ("∞", r"$\infty$"),
    ("∈", r"$\in$"),
    ("⊆", r"$\subseteq$"),
    ("▶", r"$\blacktriangleright$"),
    ("∧", r"$\wedge$"),
    ("✓", r"\checkmark"),
    ("ρ", r"$\rho$"),
    ("Δ", r"$\Delta$"),
    ("·", r"$\cdot$"),
    ("μ", r"$\mu$"),
    ("′", r"$'$"),
    ("−", "-"),
    ("≫", r"$\gg$"),
    ("→", r"$\rightarrow$"),
    ("≈", r"$\approx$"),
    ("±", r"\textpm{}"),
    ("₁", r"$_{1}$"),
    ("₂", r"$_{2}$"),
    ("₃", r"$_{3}$"),
    ("₄", r"$_{4}$"),
    ("₅", r"$_{5}$"),
    ("₆", r"$_{6}$"),
    ("ₜ", r"$_{t}$"),
    ("φ", r"$\varphi$"),
    ("π̂", r"$\hat\pi$"),
    ("⁻", "-"),
    ("β", r"$\beta$"),
    ("δ", r"$\delta$"),
    ("θ", r"$\theta$"),
    ("π", r"$\pi$"),
]


def apply_subs(text: str) -> str:
    """Substitutions apply to the body only: the YAML header (title, subtitle) keeps ™ for the PDF metadata."""
    m = re.match(r"\A---\n.*?\n---\n", text, re.DOTALL)
    head, body = (text[:m.end()], text[m.end():]) if m else ("", text)
    for old, new in UNICODE_SUBS:
        body = body.replace(old, new)
    return head + body


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the AIAS 6.0 Preview AIAS 6.0 Preview PDF")
    ap.add_argument("--source", type=Path, default=PAPER_DIR / "aias_6_0_preview_paper_draft.md")
    ap.add_argument("--output", type=Path, default=PAPER_DIR / "aias_6_0_preview_paper.pdf")
    ap.add_argument("--watermark", default=None)
    a = ap.parse_args(argv)
    if not a.source.exists():
        sys.exit(f"ERROR: source not found: {a.source}")
    raw = a.source.read_text(encoding="utf-8")
    for bad in ("{{", "{%"):
        if bad in raw:
            sys.exit(f"ERROR: {a.source} still contains template syntax {bad!r}; run fill_paper_aias_6_0_preview.py first")
    prov = Path(str(a.source).replace(".md", "_provenance.json"))
    synthetic = json.loads(prov.read_text())["synthetic"] if prov.exists() else False
    if synthetic and not a.watermark:
        sys.exit("ERROR: synthetic source: --watermark is required")
    a.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = a.output.parent / "_build_tmp_aias_6_0_preview.md"
    tmp.write_text(apply_subs(raw), encoding="utf-8")
    cmd = ["pandoc", str(tmp), "-o", str(a.output), "--pdf-engine=xelatex",
           f"--resource-path={PAPER_DIR}:{a.source.parent}", "--standalone",
           f"--lua-filter={PAPER_DIR / 'tables_as_tabular.lua'}"]
    print(f"Building: {a.source} -> {a.output}")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PAPER_DIR))
    tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        print(f"ERROR: pandoc failed (exit {r.returncode})\n{r.stderr}")
        sys.exit(1)
    missing = sorted(set(re.findall(r"Missing character: There is no (.) ", r.stderr)))
    if missing:
        print(f"WARNING: Carlito glyph gaps (add to UNICODE_SUBS): {missing}")
    if a.watermark:
        import watermark_aias6
        n = watermark_aias6.stamp(a.output, a.output, a.watermark)
        print(f"  watermark on {n} pages: {a.watermark}")
    from pypdf import PdfReader
    print(f"Built: {a.output} ({a.output.stat().st_size / 1024:.0f} KB, {len(PdfReader(str(a.output)).pages)} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
