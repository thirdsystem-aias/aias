#!/usr/bin/env python3
"""
Sentiment Paper A brief (AIAS™ Methodology v1.11 scored under v1.20), report code TS-CS-v1.20-r1.

First short designed brief for a method/validity paper (Pablo, Sun Nov 22, 2026, 8:22 am): 1-2 pages, report design
system v2 (brand v1.6 / report specs v1.2, reports/ts_layout.py), Tier 3 elements (no cover; title block, standfirst,
three numbers, one chart), managerial register, small-print notes and a Disclosures block (reports/small_print.py),
the registered report code on the last page, in the PDF metadata and in the file name (reports/report_code.py).

ts_layout has no Tier 3 page function yet; this builder composes the two pages from its shared pieces
(running_chrome, number_row, reserve_chart/overlay_charts, _block/_columns) without changing the module.

Numbers: reports/brief_v1_20_values.py (read by code from osf/methodology/v1_20/outputs and the locked scorer's
constants); text: reports/brief_v1_20_content.py with {KEY} placeholders; chart:
scripts/build_chart_brief_v1_20.py. After the build, every digit group in the PDF's text is matched to a value in
the provenance or to a listed non-result token (versions, model names, dates, code, page numbers, axis ticks).

Run from the worktree root:
    AIAS_ROOT=$PWD ~/aias/venv/bin/python reports/build_brief_v1_20.py [--code TS-CS-v1.20-r1] [--out-dir DIR]
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

import brief_v1_20_content as C  # noqa: E402
import brief_v1_20_values as BV  # noqa: E402
import report_code as RC  # noqa: E402
import small_print as SP  # noqa: E402
import ts_layout as L  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

CHART = ROOT / "reports/figs/v120/brief/brief_fig_01_presence_overlap.pdf"
OUT_DIR = ROOT / "reports/briefs/v1_20"
PDF_SUBJECT = "Brief: Sentiment Paper A (AIAS Methodology v1.11 scored under v1.20)."


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
        raise SystemExit(f"missing chart {CHART}; run scripts/build_chart_brief_v1_20.py")

    fd, base_pdf = tempfile.mkstemp(suffix=".pdf", prefix="brief_v120_base_")
    os.close(fd)
    c = Canvas(base_pdf, pagesize=(t.page_w, t.page_h))
    c.setTitle(f"{C.TITLE} — AIAS™ Methodology v1.20")
    c.setAuthor("Pablo Ulpiano González Castro")
    c.setSubject(RC.pdf_subject(code, PDF_SUBJECT))
    c.setKeywords(RC.pdf_keywords(code, "Third System", "AIAS Methodology v1.20", "Sentiment Paper A", t.website))
    slots, pages = [], []
    ap = t.pages["at_a_glance"]
    fp = t.pages["finding_page"]

    # ---------------------------------------------------------------- page 1: title block, standfirst, numbers, chart
    L.running_chrome(c, t, C.RUNNING_LABEL, 1)
    ns1 = SP.NoteSeq(t)
    marks = [ns1.cite(F(n)) for n in C.NOTES_P1]
    L._caps(c, t, t.margin, t.y(ap["kicker_baseline_from_top_pt"]), C.KICKER, t.style("kicker"))
    hspec = t.style("finding_headline")
    y = L._block(c, lambda: [L._para(t, C.TITLE, hspec)], t.margin, t.y(fp["kicker_baseline_from_top_pt"] + 8),
                 t.content_w, t.page_h / 2, "brief title", runt=True)
    sspec = dict(t.style("standfirst"), size_pt=13.5, leading_pt=18.5)  # brief standfirst: below the title's size
    standfirst = F(C.STANDFIRST, marks)
    y = L._block(c, lambda: [L._para(t, standfirst, sspec)], t.margin, y - 12, ap["standfirst_width_pt"],
                 t.page_h / 2, "brief standfirst", runt=True)
    nr = ap["number_row"]
    numbers = [{k: F(x) for k, x in n.items()} for n in C.NUMBERS]
    row = L.number_row(c, t, t.margin, y - 20, t.content_w, numbers)
    fb1 = SP.foot_blocks(c, t, notes=ns1.notes)
    cw, ch, sc = L.reserve_chart(CHART, t.content_w)
    ctop = row["bottom"] - 16
    pointer = SP.disclosure_pointer(2)
    pbot = ctop - ch - 10
    py = L._block(c, lambda: [L.paragraph(t, pointer, "small")], t.margin, pbot, t.content_w, fb1["body_bottom"],
                  "pointer line")
    if py < fb1["body_bottom"]:
        raise L.LayoutOverflow("page 1 runs into its notes")
    slots.append(L.ChartSlot(0, CHART, t.margin + (t.content_w - cw) / 2, ctop - ch, cw, ch, sc))
    w1 = (L.count_words(C.KICKER) + L.count_words(C.TITLE) + L.count_words(standfirst)
          + sum(L.count_words(" ".join([n["value"], n["label"], n["source"]])) for n in numbers)
          + L.count_words(pointer))
    pages.append({"page": 1, "words": w1, "elements": ["number_row", L.chart_element(t, cw, ch)],
                  "free_pt_above_notes": round(py - fb1["body_bottom"], 1)})
    c.showPage()

    # ---------------------------------------------------------------- page 2: findings in words, notes, Disclosures
    L.running_chrome(c, t, C.RUNNING_LABEL, 2, code=code)
    ns2 = SP.NoteSeq(t)
    for n in C.NOTES_P2:
        ns2.cite(F(n))
    disclosures = {k: F(x) for k, x in C.DISCLOSURES.items()}
    if "Samsung" in json.dumps(disclosures):
        raise SystemExit("the employer is named only in the paper's Declarations")
    tp = t.pages["text_page"]
    L._caps(c, t, t.margin, t.y(tp["kicker_baseline_from_top_pt"]), C.KICKER_P2, t.style("kicker"))
    fb2 = SP.foot_blocks(c, t, notes=ns2.notes, source_line=C.SOURCE_LINE, disclosures=disclosures)
    marks2 = [SP.marker(t, i) for i in range(1, len(ns2.notes) + 1)]
    secs = [(h, [F(p) for p in ps]) for h, ps in C.SECTIONS]
    # note markers: data note on the first section heading, OSF note on "How the result was reached"
    secs[0] = (secs[0][0] + marks2[0], secs[0][1])
    secs[2] = (secs[2][0] + marks2[1], secs[2][1])

    def flow(sel):
        fl = []
        for i in sel:
            h, ps = secs[i]
            fl.append(L.paragraph(t, h, "subheading", space_after=3, space_before=0 if i == sel[0] else 7))
            fl += [L.paragraph(t, p, "body", space_after=5) for p in ps]
        return fl
    colw = tp["column_width_pt"]
    xs = [t.margin, t.margin + colw + tp["gutter_pt"]]
    top2 = t.y(tp["heading_top_from_top_pt"])
    # left column: what we found; right column: what it means, how the result was reached, what comes next
    lb = L._block(c, lambda: flow([0]), xs[0], top2, colw, fb2["body_bottom"], "brief page 2, left column")
    rb = L._block(c, lambda: flow(list(range(1, len(secs)))), xs[1], top2, colw, fb2["body_bottom"],
                  "brief page 2, right column")
    cols = {"bottom": min(lb, rb)}
    w2 = L.count_words(C.KICKER_P2) + sum(L.count_words(h) + sum(L.count_words(p) for p in ps) for h, ps in secs)
    pages.append({"page": 2, "words": w2, "elements": [], "free_pt_above_notes": round(cols["bottom"] - fb2["body_bottom"], 1)})
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
    "versions": r"v\d+\.\d+(?:-prereg-r\d+)?", "code": r"TS-CS-v1\.20-r1", "osf": r"ec6wh", "files": r"v1_20|v1_20_verdicts",
    "models": r"(?:Opus|Sol|GPT-6\.1|Opus 5\.5|5\.5|6\.1)", "years": r"\b20(?:17|18|21|22|24|25|26)\b",
    "dates": r"September 23|November 10", "tier": r"tier 2/3", "intervals": r"95%",
}


def digit_audit(pdf, v) -> dict:
    """Every digit group in the PDF text is a provenance value, a value plotted on the chart (verdict file), a chart
    axis tick, a page number, or one of the NON_RESULT tokens. Raises on anything else."""
    from pypdf import PdfReader
    src_vals = set(v.vals.values())
    _, srcs = BV.load()
    chart_vals = {BV.r3(r["rho"]).replace("-", "−") for rs in BV.chart_data(srcs).values() for r in rs}
    chart_vals |= {BV.i0(r["n"]) for rs in BV.chart_data(srcs).values() for r in rs}
    ticks = {"0", "0.25", "−0.25", "0.50", "0.75"}
    found, unknown = [], []
    for pno, page in enumerate(PdfReader(str(pdf)).pages, 1):
        text = re.sub(r"\s+", " ", page.extract_text())
        text = re.sub(r"(?<![\d.])(\d\.) (\d)", r"\1\2", text)  # pypdf splits some chart labels ("0. 149")
        for pat in NON_RESULT.values():
            text = re.sub(pat, " ", text, flags=re.I)
        for m in re.finditer(r"[−-]?\d+(?:[.,]\d+)*%?", text):
            tok = m.group(0).rstrip(".,")
            ok = (tok in src_vals or tok.lstrip("−-") in src_vals or tok in chart_vals or tok in ticks
                  or tok == str(pno) or ("US$" + tok) in src_vals or tok in {"1", "2", "3"})
            (found if ok else unknown).append((pno, tok))
    if unknown:
        raise SystemExit(f"digit groups without a source: {unknown}")
    return {"checked": len(found), "unknown": unknown}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default="TS-CS-v1.20-r1")
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
