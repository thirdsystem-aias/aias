"""
sample_small_print.py - a three-page SAMPLE report that exercises the small-print styles
(reports/small_print.py): numbered notes at the foot of the same page, a margin callout, the
one-line Disclosures pointer in the main text and the Disclosures block on the last page.

Every word is placeholder text marked SAMPLE; there are no findings and no numbers.

    AIAS_ROOT=<worktree> python3 reports/sample_small_print.py <out.pdf>

build() takes the repository root explicitly (or AIAS_ROOT); it never writes outside out_pdf.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

if __package__:
    from . import small_print as SP, ts_layout as L
else:
    import small_print as SP
    import ts_layout as L

CODE = "TS-BR-SAMPLE-r1"
LABEL = "SAMPLE - placeholder text"

DISCLOSURES = {
    "conflicts_of_interest": "SAMPLE placeholder. The text a real report would put here names any financial or "
                             "commercial tie between Third System and a brand, client or funder named in the report.",
    "held_out_brands": "SAMPLE placeholder. A real report lists the brands held out of the model-tuning set and "
                       "says how they were chosen.",
    "ai_use": "SAMPLE placeholder. A real report says which AI models produced or checked which part of the work.",
    "independence": "SAMPLE placeholder. A real report says who paid for the study and that the sponsor had no "
                    "say over its method or its conclusions.",
}

FILLER = ("SAMPLE placeholder sentence in the report's body type, standing in for the findings a real report would "
          "state in plain, light prose. ")


def _body(t: L.Tokens, paras: list[str]):
    return lambda: L._body_paras(t, paras)


def _page(c, t, n, *, ns, kicker, heading, paras, callout=None, foot=None, last=False):
    L.running_chrome(c, t, LABEL, n, CODE if last else None)
    tp = t.pages["text_page"]
    y = t.y(tp["heading_top_from_top_pt"])
    L._caps(c, t, t.margin, t.y(tp["kicker_baseline_from_top_pt"]), kicker, t.style("kicker"))
    fb = SP.foot_blocks(c, t, notes=ns.notes, **(foot or {}))
    bottom = fb["body_bottom"]
    y = L._block(c, lambda: [L._para(t, heading, t.style("finding_headline"))], t.margin, y, t.content_w, bottom,
                 "heading", runt=True) - 12
    if callout:
        # body in grid columns 1-4, callout in columns 5-6
        w = t.span(1, 4)
        colw = (w - tp["gutter_pt"]) / 2
        res = L._columns(c, _body(t, paras), y, bottom, [t.margin, t.margin + colw + tp["gutter_pt"]], colw, "body")
        SP.margin_callout(c, t, callout["text"], top=y, col_from=5, col_to=6, label=callout["label"], bottom_limit=bottom)
        return res
    colw = (t.content_w - tp["gutter_pt"]) / 2
    return L._columns(c, _body(t, paras), y, bottom, [t.margin, t.margin + colw + tp["gutter_pt"]], colw, "body")


def build(out_pdf: Path | str, root: Path | str | None = None) -> dict:
    """Render the sample to out_pdf. Returns {'pairs': [(reference sentence, note text)], 'pages': 3}."""
    from reportlab.pdfgen.canvas import Canvas

    t = L.Tokens(root)
    L.register_fonts()
    SP.preflight_styles(t)
    c = Canvas(str(out_pdf), pagesize=(t.page_w, t.page_h))
    c.setTitle("SAMPLE small-print report")
    c.setSubject(f"{CODE} · SAMPLE small-print styles")
    c.setKeywords(CODE)
    pairs = []

    def claim(ns, sentence, note):
        pairs.append((sentence, note))
        return f"{sentence}{ns.cite(note)}"

    # page 1: two columns, three notes, a source line, the pointer
    ns = SP.NoteSeq(t)
    s1 = claim(ns, "SAMPLE claim alpha stands where a method note would hang", "SAMPLE note alpha: how the figure was sourced.")
    s2 = claim(ns, "SAMPLE claim beta stands where a definition would hang", "SAMPLE note beta: what the term means.")
    s3 = claim(ns, "SAMPLE claim gamma stands where a sample size would hang", "SAMPLE note gamma: the sample size and the model list.")
    p1 = [f"{s1}. {FILLER * 3}", f"{s2}. {FILLER * 3}", f"{s3}. {FILLER * 3}" + SP.disclosure_pointer(3)]
    _page(c, t, 1, ns=ns, kicker="Sample page one", heading="SAMPLE: the main text stays light and the notes sit at the foot",
          paras=p1, foot={"source_line": "Source: SAMPLE placeholder, not a real source."})
    c.showPage()

    # page 2: body in four columns of the grid, a margin callout in the other two
    ns = SP.NoteSeq(t)
    s4 = claim(ns, "SAMPLE claim delta carries one note on this page", "SAMPLE note delta: a caveat that belongs to this page.")
    p2 = [f"{s4}. {FILLER * 4}", FILLER * 5]
    _page(c, t, 2, ns=ns, kicker="Sample page two", heading="SAMPLE: a margin callout beside the text", paras=p2,
          callout={"label": "SAMPLE callout",
                   "text": "A definition, caveat or sample size that the main text does not need to carry. "
                           "SAMPLE placeholder only."})
    c.showPage()

    # page 3 (last): a note and the Disclosures block, code on the footer line
    ns = SP.NoteSeq(t)
    s5 = claim(ns, "SAMPLE claim epsilon closes the report", "SAMPLE note epsilon: a note on the last page.")
    p3 = [f"{s5}. {FILLER * 3}", SP.disclosure_pointer(3)]
    _page(c, t, 3, ns=ns, kicker="Sample page three", heading="SAMPLE: the Disclosures block closes the report",
          paras=p3, foot={"disclosures": DISCLOSURES}, last=True)
    c.showPage()
    c.save()
    return {"pairs": pairs, "pages": 3}


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    print(build(out, os.environ.get("AIAS_ROOT") or Path(__file__).resolve().parent.parent))
