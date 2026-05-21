#!/usr/bin/env python3
"""
v0.18 SSRN paper build pipeline (pandoc + xelatex + Carlito).

Reads:   papers/v0_18/v0_18_ssrn_paper_draft.md
Writes:  papers/v0_18/v0_18_ssrn_paper.pdf

Applies Unicode → LaTeX substitutions for glyphs Carlito lacks. The
substitution table is exhaustive for the glyphs likely to appear in
AIAS papers; safe to copy-forward to v0.19+.

Carlito glyph gaps requiring substitution (per program convention):
  - ≥ U+2265  → $\\geq$
  - ≤ U+2264  → $\\leq$
  - ρ U+03C1  → $\\rho$ (Greek rho — used for Spearman correlation)
  - ∧ U+2227  → $\\land$ (logical AND — used in Iwachu-pattern threshold)
  - → U+2192  → $\\to$ (cascade arrows)
  - × U+00D7  → $\\times$ (Recognition × Recall)
  - ₜ U+209C  → $_{t}$ (subscript t)
  - ∈ U+2208  → $\\in$
  - ⊆ U+2286  → $\\subseteq$
  - ▶ U+25B6  → $\\blacktriangleright$
  - Greek letters, math superscripts/subscripts as needed

Carlito glyphs that DO exist (no substitution required):
  - · U+00B7 middle dot
  - – U+2013, — U+2014 dashes
  - ™ U+2122 trademark
  - § U+00A7 section sign

Run from project root:
    cd ~/aias
    python3 reports/build_paper_v18.py

Or explicitly:
    python3 reports/build_paper_v18.py \\
        --input papers/v0_18/v0_18_ssrn_paper_draft.md \\
        --output papers/v0_18/v0_18_ssrn_paper.pdf
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Substitution table (ordered — longer/more-specific patterns first)
# ---------------------------------------------------------------------------

UNICODE_TO_LATEX = [
    # --- Math operators / relations ---
    ('≥', r'$\geq$'),
    ('≤', r'$\leq$'),
    ('≠', r'$\neq$'),
    ('≈', r'$\approx$'),
    ('∼', r'$\sim$'),
    ('±', r'$\pm$'),
    ('∓', r'$\mp$'),
    ('∝', r'$\propto$'),

    # --- Math symbols ---
    ('×', r'$\times$'),
    ('÷', r'$\div$'),
    ('⋅', r'$\cdot$'),
    ('∧', r'$\land$'),    # logical AND (Iwachu-pattern threshold)
    ('∨', r'$\lor$'),     # logical OR
    ('¬', r'$\neg$'),

    # --- Set theory ---
    ('∈', r'$\in$'),
    ('∉', r'$\notin$'),
    ('⊆', r'$\subseteq$'),
    ('⊂', r'$\subset$'),
    ('⊇', r'$\supseteq$'),
    ('∪', r'$\cup$'),
    ('∩', r'$\cap$'),
    ('∅', r'$\emptyset$'),
    ('∀', r'$\forall$'),
    ('∃', r'$\exists$'),

    # --- Arrows ---
    ('→', r'$\to$'),
    ('←', r'$\gets$'),
    ('↔', r'$\leftrightarrow$'),
    ('⇒', r'$\Rightarrow$'),
    ('⇐', r'$\Leftarrow$'),
    ('⇔', r'$\Leftrightarrow$'),
    ('▶', r'$\blacktriangleright$'),
    ('▷', r'$\triangleright$'),

    # --- Greek lowercase (commonly used in stats) ---
    ('α', r'$\alpha$'),
    ('β', r'$\beta$'),
    ('γ', r'$\gamma$'),
    ('δ', r'$\delta$'),
    ('ϵ', r'$\epsilon$'),
    ('ε', r'$\varepsilon$'),
    ('ζ', r'$\zeta$'),
    ('η', r'$\eta$'),
    ('θ', r'$\theta$'),
    ('ι', r'$\iota$'),
    ('κ', r'$\kappa$'),
    ('λ', r'$\lambda$'),
    ('μ', r'$\mu$'),
    ('ν', r'$\nu$'),
    ('ξ', r'$\xi$'),
    ('π', r'$\pi$'),
    ('ρ', r'$\rho$'),     # Spearman correlation — heavily used in AIAS
    ('σ', r'$\sigma$'),
    ('τ', r'$\tau$'),
    ('υ', r'$\upsilon$'),
    ('φ', r'$\varphi$'),
    ('χ', r'$\chi$'),
    ('ψ', r'$\psi$'),
    ('ω', r'$\omega$'),

    # --- Greek uppercase ---
    ('Α', r'A'),  # use Latin A; ASCII identical visually
    ('Β', r'B'),
    ('Γ', r'$\Gamma$'),
    ('Δ', r'$\Delta$'),
    ('Θ', r'$\Theta$'),
    ('Λ', r'$\Lambda$'),
    ('Π', r'$\Pi$'),
    ('Σ', r'$\Sigma$'),
    ('Φ', r'$\Phi$'),
    ('Ω', r'$\Omega$'),

    # --- Subscripts (commonly missing in Carlito) ---
    ('ₐ', r'$_{a}$'),
    ('ₑ', r'$_{e}$'),
    ('ᵢ', r'$_{i}$'),
    ('ₒ', r'$_{o}$'),
    ('ₜ', r'$_{t}$'),
    ('ₓ', r'$_{x}$'),
    ('₀', r'$_{0}$'),
    ('₁', r'$_{1}$'),
    ('₂', r'$_{2}$'),
    ('₃', r'$_{3}$'),
    ('₄', r'$_{4}$'),
    ('₅', r'$_{5}$'),
    ('₆', r'$_{6}$'),
    ('₇', r'$_{7}$'),
    ('₈', r'$_{8}$'),
    ('₉', r'$_{9}$'),
    ('₊', r'$_{+}$'),
    ('₋', r'$_{-}$'),

    # --- Superscripts ---
    ('⁰', r'$^{0}$'),
    ('¹', r'$^{1}$'),
    ('²', r'$^{2}$'),
    ('³', r'$^{3}$'),
    ('⁴', r'$^{4}$'),
    ('⁵', r'$^{5}$'),
    ('⁶', r'$^{6}$'),
    ('⁷', r'$^{7}$'),
    ('⁸', r'$^{8}$'),
    ('⁹', r'$^{9}$'),
    ('⁻', r'$^{-}$'),
    ('⁺', r'$^{+}$'),
]


def substitute_glyphs(text: str) -> tuple[str, dict]:
    """Apply Carlito-safe Unicode → LaTeX substitutions to the *body* only.

    YAML frontmatter (delimited by `---` lines at the start of the file) is
    skipped: YAML double-quoted strings interpret `\\t`, `\\n`, etc. as escape
    sequences, so substituting `×` → `$\\times$` inside a YAML title corrupts
    it (yielding `$ imes$` after YAML strips the `\\t`). Substitutions in the
    YAML frontmatter were never necessary anyway — title / subtitle text is
    rendered by pandoc / xelatex with Carlito directly, and Carlito has
    native glyphs for most punctuation including ×, ≥, ≤, →, ≈, ·, §, ™.

    Returns (substituted_text, counts) where counts maps each substituted
    glyph to the number of times it was replaced (for logging).
    """
    counts: dict = {}

    # Detect YAML frontmatter: `---\n` at file start, second `---\n` closes it.
    yaml_prefix = ""
    body = text
    if text.startswith("---\n") or text.startswith("---\r\n"):
        match = re.search(r"^---\s*\n.*?^---\s*\n", text, re.DOTALL | re.MULTILINE)
        if match:
            yaml_prefix = text[: match.end()]
            body = text[match.end():]

    # Apply substitutions to body only
    for unicode_char, latex_replacement in UNICODE_TO_LATEX:
        n = body.count(unicode_char)
        if n > 0:
            counts[unicode_char] = n
            body = body.replace(unicode_char, latex_replacement)

    return yaml_prefix + body, counts


def check_pandoc_available() -> str:
    """Verify pandoc and xelatex are on PATH; return pandoc version."""
    try:
        result = subprocess.run(
            ['pandoc', '--version'],
            capture_output=True, text=True, check=True,
        )
        first_line = result.stdout.splitlines()[0]
        return first_line
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        sys.exit(
            f"ERROR: pandoc not found on PATH.\n"
            f"Install via: brew install pandoc\n"
            f"Underlying error: {e}"
        )


def check_xelatex_available() -> None:
    """Verify xelatex is on PATH."""
    try:
        subprocess.run(
            ['xelatex', '--version'],
            capture_output=True, text=True, check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        sys.exit(
            f"ERROR: xelatex not found on PATH.\n"
            f"Install via: brew install --cask mactex (full ~4GB) or "
            f"brew install --cask basictex (smaller, may need additional packages)\n"
            f"Underlying error: {e}"
        )


def build_paper(md_path: Path, pdf_path: Path, verbose: bool = True) -> None:
    """Build the v0.18 SSRN paper PDF via pandoc + xelatex."""
    if not md_path.exists():
        sys.exit(f"ERROR: input markdown not found: {md_path}")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    # --- Apply Unicode → LaTeX substitutions ---
    src = md_path.read_text(encoding='utf-8')
    substituted, counts = substitute_glyphs(src)

    if verbose:
        print(f"[build_paper_v18] input:  {md_path}")
        print(f"[build_paper_v18] output: {pdf_path}")
        if counts:
            print(f"[build_paper_v18] Unicode → LaTeX substitutions applied:")
            for char, n in sorted(counts.items(), key=lambda kv: -kv[1]):
                latex = dict(UNICODE_TO_LATEX).get(char, '?')
                print(f"  {n:>4}x  {char}  →  {latex}")
        else:
            print(f"[build_paper_v18] No Unicode substitutions needed.")

    # --- Write to temp file (pandoc reads from disk) ---
    temp_md = md_path.with_name(md_path.stem + '.build.md')
    temp_md.write_text(substituted, encoding='utf-8')

    try:
        # --- Pandoc invocation ---
        # The YAML frontmatter in v0_18_ssrn_paper_draft.md carries
        # mainfont, fontsize, header-includes, etc. — pandoc reads them
        # and constructs the xelatex preamble. No need to repeat here.
        cmd = [
            'pandoc',
            str(temp_md),
            '-o', str(pdf_path),
            '--pdf-engine=xelatex',
            '--variable', 'geometry:margin=1in',
            '--variable', 'linkcolor:black',
            '--variable', 'urlcolor:black',
            # Resolve relative image paths (e.g. ../../reports/figs/v18/*.pdf)
            # from the markdown file's directory rather than CWD. Pandoc's
            # default behavior is to resolve from CWD, which breaks when the
            # build is invoked from project root but the markdown sits two
            # levels down. Setting resource-path to the markdown's parent
            # directory makes `../../reports/figs/v18/chart_NN.pdf` resolve
            # correctly to <project_root>/reports/figs/v18/chart_NN.pdf.
            '--resource-path', str(md_path.parent),
            '--standalone',
            # Leave --toc off: the v0.18 paper is short enough that a TOC
            # adds friction rather than help. Add later if needed.
        ]

        if verbose:
            print(f"[build_paper_v18] pandoc command:")
            print(f"  {' '.join(cmd)}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("ERROR: pandoc + xelatex failed", file=sys.stderr)
            print("--- stdout ---", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print("--- stderr ---", file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)

        if verbose and result.stderr.strip():
            # pandoc warnings often go to stderr without being fatal;
            # surface them but don't treat as errors.
            print(f"[build_paper_v18] pandoc warnings:")
            for line in result.stderr.splitlines():
                if line.strip():
                    print(f"  {line}")

        pdf_size_kb = pdf_path.stat().st_size / 1024
        print(f"[build_paper_v18] ✓ PDF written: {pdf_path}  ({pdf_size_kb:.1f} KB)")

        # --- Page count sanity check ---
        try:
            from pypdf import PdfReader
            page_count = len(PdfReader(str(pdf_path)).pages)
            print(f"[build_paper_v18] page count: {page_count}")
            if page_count < 8 or page_count > 30:
                print(f"[build_paper_v18] WARNING: page count outside the 8–30 expected band")
        except ImportError:
            print(f"[build_paper_v18] (pypdf not installed; page count check skipped)")

    finally:
        # Keep temp_md by default so xelatex error messages are reproducible.
        # Uncomment to clean up:
        # temp_md.unlink(missing_ok=True)
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Build v0.18 SSRN paper PDF via pandoc + xelatex + Carlito",
    )
    parser.add_argument(
        '--input', type=Path,
        default=Path('papers/v0_18/v0_18_ssrn_paper_draft.md'),
        help='Path to the markdown source (default: papers/v0_18/v0_18_ssrn_paper_draft.md)',
    )
    parser.add_argument(
        '--output', type=Path,
        default=Path('papers/v0_18/v0_18_ssrn_paper.pdf'),
        help='Path to the output PDF (default: papers/v0_18/v0_18_ssrn_paper.pdf)',
    )
    parser.add_argument(
        '--quiet', action='store_true',
        help='Suppress per-glyph substitution log',
    )
    args = parser.parse_args()

    print(f"[build_paper_v18] {check_pandoc_available()}")
    check_xelatex_available()

    build_paper(args.input, args.output, verbose=not args.quiet)


if __name__ == '__main__':
    main()
