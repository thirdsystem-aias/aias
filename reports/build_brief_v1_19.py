#!/usr/bin/env python3
"""
Coverage Paper B brief (AIAS™ Methodology v1.19), report code TS-BR-v1.19-r1 (Tier 3 brief).

Third short designed brief, in the format Pablo approved on Sun Nov 22, 2026, 10:47 am (decisions 1-7): 2 pages,
report design system v2 (brand v1.6 / report specs v1.2), Tier 3 elements (no cover; title block, standfirst, three
numbers, one chart), managerial register, small-print notes and a Disclosures block (reports/small_print.py), the
registered report code on the last page, in the PDF metadata and in the file name (reports/report_code.py).

Both pages are drawn by ts_layout.brief_page() (decision 2): kind="front" and kind="text"; geometry in
report_specs page_templates.brief_page, standfirst style typography.number_scale.brief_standfirst (decision 3).

Numbers: reports/brief_v1_19_values.py (read by code from osf/methodology/v1_19/outputs/v119_verdicts.json and the
locked scorer's constants); text: reports/brief_v1_19_content.py with {KEY} placeholders; chart:
scripts/build_chart_brief_v1_19.py. After the build, every digit group in the PDF's text is matched to a value in
the provenance or to a listed non-result token (versions, model names, dates, code, page numbers, axis ticks).

Run from the worktree root:
    AIAS_ROOT=$PWD ~/aias/venv/bin/python reports/build_brief_v1_19.py [--code TS-BR-v1.19-r1] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AIAS_ROOT") or SCRIPT_DIR.parent).resolve()
os.environ["AIAS_ROOT"] = str(ROOT)
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

import brief_v1_19_content as C  # noqa: E402
import brief_v1_19_values as BV  # noqa: E402
import report_code as RC  # noqa: E402
import small_print as SP  # noqa: E402
import ts_layout as L  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

CHART = ROOT / "reports/figs/v119/brief/brief_fig_01_split_reliability.pdf"
OUT_DIR = ROOT / "reports/briefs/v1_19"
PDF_SUBJECT = "Brief: Coverage Paper B (AIAS Methodology v1.19)."


class Filler:
    def __init__(self, vals):
        self.vals = vals
        self.used = set()

    def __call__(self, text, notes=None):
        def rep(m):
            k = m.group(1)
            if re.fullmatch(r"N\d+", k):
                if notes is None:
                    raise KeyError(f"note marker {k} outside a page")
                return notes[int(k[1:]) - 1]
            self.used.add(k)
            return self.vals[k]
        return re.sub(r"\{([A-Za-z0-9_]+)\}", rep, text)


def build(output: Path, code: str) -> dict:
    v, src = BV.load()
    F = Filler(v.vals)
    t = L.Tokens(ROOT)
    L.register_fonts()
    SP.preflight_styles(t)
    RC.check_code(code, t.catalogue)
    want = RC.file_name(code, C.TITLE)
    if output.name != want:
        raise SystemExit(f"the PDF must be named {want}, not {output.name}")
    if not CHART.is_file():
        raise SystemExit(f"missing chart {CHART}; run scripts/build_chart_brief_v1_19.py")

    fd, base_pdf = tempfile.mkstemp(suffix=".pdf", prefix="brief_v1_19_base_")
    os.close(fd)
    c = Canvas(base_pdf, pagesize=(t.page_w, t.page_h))
    c.setTitle(f"{C.TITLE} — AIAS™ Methodology v1.19")
    c.setAuthor("Pablo Ulpiano González Castro")
    c.setSubject(RC.pdf_subject(code, PDF_SUBJECT))
    c.setKeywords(RC.pdf_keywords(code, "Third System", "AIAS Methodology v1.19", "Coverage Paper B", t.website))
    slots, pages = [], []

    # ---------------------------------------------------------------- page 1: title block, standfirst, numbers, chart
    ns1 = SP.NoteSeq(t)
    marks = [ns1.cite(F(n)) for n in C.NOTES_P1]
    standfirst = F(C.STANDFIRST, marks)
    numbers = [{k: F(x) for k, x in n.items()} for n in C.NUMBERS]
    g1 = L.brief_page(c, t, kind="front", label=C.RUNNING_LABEL, page_no=1, kicker=C.KICKER, title=C.TITLE,
                      standfirst=standfirst, numbers=numbers, chart=CHART, pointer=SP.disclosure_pointer(2),
                      foot=lambda: SP.foot_blocks(c, t, notes=ns1.notes))
    slots.append(g1["slot"])
    pages.append({"page": 1, "words": g1["words"], "elements": g1["elements"],
                  "free_pt_above_notes": g1["free_pt_above_notes"]})
    c.showPage()

    # ---------------------------------------------------------------- page 2: findings in words, notes, Disclosures
    ns2 = SP.NoteSeq(t)
    for n in C.NOTES_P2:
        ns2.cite(F(n))
    disclosures = {k: F(x) for k, x in C.DISCLOSURES.items()}
    if "Samsung" in json.dumps(disclosures):
        raise SystemExit("the employer is named only in the paper's Declarations")
    marks2 = [SP.marker(t, i) for i in range(1, len(ns2.notes) + 1)]
    secs = [(h, [F(p) for p in ps]) for h, ps in C.SECTIONS]
    # note markers: data note on the first section heading, OSF note on "How the result was reached"
    secs[0] = (secs[0][0] + marks2[0], secs[0][1])
    hi = [h for h, _ in secs].index("How the result was reached")
    secs[hi] = (secs[hi][0] + marks2[1], secs[hi][1])
    # left column: what we found; right column: what it means, how the result was reached, what comes next
    g2 = L.brief_page(c, t, kind="text", label=C.RUNNING_LABEL, page_no=2, kicker=C.KICKER_P2, sections=secs,
                      split=1, code=code,
                      foot=lambda: SP.foot_blocks(c, t, notes=ns2.notes, source_line=C.SOURCE_LINE,
                                                  disclosures=disclosures))
    pages.append({"page": 2, "words": g2["words"], "elements": [], "free_pt_above_notes": g2["free_pt_above_notes"]})
    c.showPage()
    c.save()

    output.parent.mkdir(parents=True, exist_ok=True)
    L.overlay_charts(base_pdf, slots, output)
    os.unlink(base_pdf)

    # ---------------------------------------------------------------- checks
    pf = RC.preflight(output, code, C.TITLE, t.catalogue, t.website)
    sizes = SP.check_pdf_min_size(output)
    disc = SP.check_disclosures(output, t)
    notes_ok = SP.check_notes_same_page(output, [(C.SOURCE_LINE[:60], C.SOURCE_LINE[:60])])
    for p in pages:
        chk = L.check_page_budget(t, p["words"], p["elements"])
        p.update(budget=chk["budget"], ok=chk["ok"])
    digits = digit_audit(output, v)
    prov = BV.write_provenance(v, {"report_code": code, "pdf": str(output.relative_to(ROOT)),
                                   "keys_used_in_text": sorted(F.used),
                                   "digit_audit": digits})
    return {"output": str(output), "pages": pages, "preflight": pf, "min_size": sizes, "disclosures": disc,
            "notes": notes_ok, "digits": digits, "provenance": str(prov), "unused": sorted(set(v.vals) - F.used)}


# Digit groups that are not results: identifiers, model names, dates, page numbers, chart axis ticks, the code.
NON_RESULT = {
    "code": r"TS-BR-v1\.19-r1", "versions": r"v\d+\.\d+(?:-prereg-r\d+)?", "osf": r"ec6wh", "files": r"v1_19|v119_verdicts",
    "models": r"Fable 5\.2|GPT-6|Gemini 4|Opus 5\.5", "years": r"\b20(?:17|18|21|22|24|25|26)\b",
    "dates": r"September 23|November 10", "tier": r"tier 2/3", "formula": r"2r/\(1\+r\)",
}


def digit_audit(pdf, v) -> dict:
    """Every digit group in the PDF text is a provenance value, a chart axis tick, a page number or note marker, or
    one of the NON_RESULT tokens. Raises on anything else. Returns counts per kind of match."""
    from pypdf import PdfReader
    src_vals = set(v.vals.values())
    ticks = {"−0.25", "0", "0.25", "0.50", "0.75"}
    found, unknown, kinds, nonres = [], [], {}, {}
    for pno, page in enumerate(PdfReader(str(pdf)).pages, 1):
        text = re.sub(r"\s+", " ", page.extract_text())
        text = re.sub(r"(?<![\d.])(\d\.) (\d)", r"\1\2", text)  # pypdf splits some chart labels ("0. 149")
        for name, pat in NON_RESULT.items():
            nonres[name] = nonres.get(name, 0) + len(re.findall(pat, text, flags=re.I))
            text = re.sub(pat, " ", text, flags=re.I)
        for m in re.finditer(r"[−-]?\d+(?:[.,]\d+)*%?", text):
            tok = m.group(0).rstrip(".,")
            if tok in src_vals or tok.lstrip("−-") in src_vals:
                kind = "provenance value"
            elif tok in ticks:
                kind = "chart axis tick"
            elif tok == str(pno) or tok in {"1", "2", "3"}:
                kind = "page number or note marker"
            else:
                kind = None
            if kind:
                found.append((pno, tok))
                kinds[kind] = kinds.get(kind, 0) + 1
            else:
                unknown.append((pno, tok))
    if unknown:
        raise SystemExit(f"digit groups without a source: {unknown}")
    return {"checked": len(found), "unknown": unknown, "by_kind": kinds, "non_result_tokens_removed": nonres}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default="TS-BR-v1.19-r1")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    a = ap.parse_args()
    out = a.out_dir / RC.file_name(a.code, C.TITLE)
    res = build(out, a.code)
    for p in res["pages"]:
        print(f"p{p['page']} words={p['words']} budget={p['budget']} {'ok' if p['ok'] else 'OVER'} "
              f"free above notes={p['free_pt_above_notes']} pt")
    print("pre-flight:", "PASS" if res["preflight"]["ok"] else "FAIL", res["preflight"]["problems"] or "",
          res["preflight"]["sha256"])
    print("min text size:", res["min_size"], "| disclosures:", res["disclosures"], "| digits checked:",
          res["digits"]["checked"])
    print("values not printed:", res["unused"])
    print("wrote", res["output"])


if __name__ == "__main__":
    main()
