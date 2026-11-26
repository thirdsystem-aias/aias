#!/usr/bin/env python3
"""
build_aias3.py -- fill and build the AIAS 3.0 release paper from its template.

  draft  (now):  {{L:KEY}} filled from the locked records (sources_aias3.py); every {{P:KEY}} printed as a visible
                 yellow placeholder; every page stamped "DRAFT, PRE-DATA: PLACEHOLDERS". Output only outside the
                 repository (default ~/aias/_worktrees/_runner_tmp/aias3_draft/).
  final  (after the release data lock): every {{P:KEY}} filled from the values file
                 (osf/aias_3_0/outputs/aias_3_0_values.json); refuses a missing value, an unmapped token and any
                 token or template syntax left in the output; refuses a synthetic values file unless --synthetic
                 (then the output must be outside the repository and is stamped).

  python3 papers/aias_3_0/build_aias3.py --mode draft [--pdf]
  python3 papers/aias_3_0/build_aias3.py --mode final --values FILE --out DIR [--synthetic] [--pdf]

Writes <out>/aias_3_0_release_paper.md, its _provenance.json (every L value with commit, path and git blob; every
P key with the input that fills it) and, with --pdf, the PDF (pandoc + xelatex + Carlito, the v1.12 builder's
Unicode substitutions).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
import sources_aias3 as S  # noqa: E402
import tokens_aias3 as T  # noqa: E402

TEMPLATE = HERE / "aias_3_0_release_paper_template.md"
DRAFT_OUT = Path.home() / "aias" / "_worktrees" / "_runner_tmp" / "aias3_draft"
STAMP = "DRAFT, PRE-DATA: PLACEHOLDERS"


def _inside_repo(p):
    try:
        Path(p).resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def _draft_box(key, in_header):
    if in_header:
        return f"[P:{key}]"
    return r"\colorbox{yellow}{\texttt{P:" + key.replace("_", r"\_") + "}}"


def fill(template_text, mode, values=None):
    """Return (filled text, provenance). Raises T.TokenError / S.SourceError on any unmapped or missing value."""
    m = re.match(r"\A---\n.*?\n---\n", template_text, re.DOTALL)
    head_end = m.end() if m else 0
    used = {"L": {}, "P": {}}

    def rep(mm, in_header):
        kind, key = mm.group(1), mm.group(2)
        if kind == "L":
            used["L"][key] = S.provenance(key)
            return S.resolve(key)
        if key not in T.PENDING:
            raise T.TokenError(f"unmapped placeholder {{{{P:{key}}}}}")
        used["P"][key] = T.PENDING[key][0]
        if mode == "draft":
            return _draft_box(key, in_header)
        return T.resolve("P", key, "final", values)

    head = T.TOKEN.sub(lambda mm: rep(mm, True), template_text[:head_end])
    body = T.TOKEN.sub(lambda mm: rep(mm, False), template_text[head_end:])
    out = head + body
    if mode == "final" and T.ANY_TEMPLATE.search(out):
        raise T.TokenError("template syntax left in the final build: "
                           + T.ANY_TEMPLATE.search(out).string[T.ANY_TEMPLATE.search(out).start():][:60])
    return out, used


def build_pdf(md_path, pdf_path, stamp=None):
    import build_paper_v1_12 as B   # the v1.12 builder's Unicode -> LaTeX substitutions, unchanged
    tmp = md_path.parent / "_build_tmp_aias3.md"
    tmp.write_text(B.apply_subs(md_path.read_text(encoding="utf-8")), encoding="utf-8")
    lua = ROOT / "papers" / "v1_12" / "tables_as_tabular.lua"
    cmd = ["pandoc", str(tmp), "-o", str(pdf_path), "--pdf-engine=xelatex", f"--resource-path={HERE}",
           "--standalone", f"--lua-filter={lua}"]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(HERE))
    tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        raise SystemExit(f"pandoc failed ({r.returncode}):\n{r.stderr[-3000:]}")
    missing = sorted(set(re.findall(r"Missing character: There is no (.) ", r.stderr)))
    if missing:
        print(f"WARNING: Carlito glyph gaps: {missing}")
    if stamp:
        import watermark_v112
        watermark_v112.stamp(pdf_path, pdf_path, stamp)
    from pypdf import PdfReader
    return len(PdfReader(str(pdf_path)).pages)


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS 3.0 release paper: fill and build")
    ap.add_argument("--mode", choices=("draft", "final"), required=True)
    ap.add_argument("--values", type=Path, default=T.VALUES_DEFAULT)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args(argv)

    values = None
    if a.mode == "final":
        values = T.load_values(a.values)
        if values["synthetic"] and not a.synthetic:
            raise SystemExit("ERROR: synthetic values file in a real build")
        if a.synthetic and not values["synthetic"]:
            raise SystemExit("ERROR: --synthetic given but the values file is not marked synthetic")
    out = a.out or DRAFT_OUT
    if (a.mode == "draft" or a.synthetic) and _inside_repo(out):
        raise SystemExit("ERROR: draft and synthetic builds are written outside the repository")
    out.mkdir(parents=True, exist_ok=True)

    text, used = fill(TEMPLATE.read_text(encoding="utf-8"), a.mode, values)
    md = out / "aias_3_0_release_paper.md"
    md.write_text(text, encoding="utf-8")
    prov = {"mode": a.mode, "synthetic": bool(values and values["synthetic"]),
            "template_blob": subprocess.run(["git", "-C", str(ROOT), "hash-object", str(TEMPLATE)],
                                            capture_output=True, text=True).stdout.strip(),
            "locked": used["L"], "placeholders": used["P"]}
    (out / "aias_3_0_release_paper_provenance.json").write_text(json.dumps(prov, indent=1, ensure_ascii=False),
                                                                 encoding="utf-8")
    print(f"filled: {md} ({len(used['L'])} locked keys, {len(used['P'])} placeholder keys)")
    if a.pdf:
        stamp = STAMP if a.mode == "draft" else ("SYNTHETIC TEST — NOT RESULTS" if a.synthetic else None)
        n = build_pdf(md, out / "aias_3_0_release_paper.pdf", stamp)
        print(f"built: {out / 'aias_3_0_release_paper.pdf'} ({n} pages)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
