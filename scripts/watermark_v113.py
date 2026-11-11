#!/usr/bin/env python3
"""
watermark_v113.py -- stamps a diagonal text on every page of a PDF (synthetic test outputs of the v1.13 pipeline; copied unchanged from watermark_v112.py, branch v1.12-paper).

  python3 scripts/watermark_v113.py IN.pdf OUT.pdf "SYNTHETIC TEST — NOT RESULTS"

Used by build_paper_v1_13.py when --watermark is given; never on a real build.
"""
import io
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.pdfgen.canvas import Canvas


def _stamp_page(w, h, text):
    buf = io.BytesIO()
    c = Canvas(buf, pagesize=(w, h))
    c.saveState()
    c.setFillColor(Color(0.95, 0.42, 0.21, alpha=0.30))
    size = min(w, h) / 13.0
    c.setFont("Helvetica-Bold", size)
    c.translate(w / 2.0, h / 2.0)
    c.rotate(35)
    c.drawCentredString(0, -size / 3.0, text)
    c.restoreState()
    c.setFillColor(Color(0.95, 0.42, 0.21, alpha=0.9))
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(w / 2.0, 10, text)
    c.drawCentredString(w / 2.0, h - 14, text)
    c.save()
    buf.seek(0)
    return PdfReader(buf).pages[0]


def stamp(pdf_in, pdf_out, text):
    reader = PdfReader(str(pdf_in))
    writer = PdfWriter()
    for page in reader.pages:
        w, h = float(page.mediabox.width), float(page.mediabox.height)
        page.merge_page(_stamp_page(w, h, text))
        writer.add_page(page)
    tmp = Path(str(pdf_out) + ".tmp")
    with open(tmp, "wb") as f:
        writer.write(f)
    tmp.replace(pdf_out)
    return len(reader.pages)


if __name__ == "__main__":
    n = stamp(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"stamped {n} pages -> {sys.argv[2]}")
