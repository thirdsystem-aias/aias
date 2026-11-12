#!/usr/bin/env python3
"""
AIAS 2.0 synthesis report, revision r3: the Tier 1 restyle in report design system v2.

Pablo's decision (Nov 11, 2026, 6:35 pm): the published AIAS 2.0 report gets the new design
as a Tier 1 flagship, as a new revision with every word of substance, number and figure
unchanged; r2 stays on OSF for the record and the website shows the new one.

Text comes from the r2 pipeline itself: aias_2_0_content.py as reshaped by
build_report_aias_2_0.py's content adapter, its chart captions (HERO_FIGURE_CAPTIONS) and its
closing-page wording, so no r2 sentence is retyped here. Charts are r2's chart PDFs in
reports/figs/aias_2_0/report/, merged unchanged (two-pass: chart footprints are reserved
from the PDF mediaboxes in pass 1, the PDFs are overlaid in pass 2). Layout is
reports/ts_layout.py.

New presentational strings (kickers, part titles, contents, the running header, the
At a glance labels and sources) are all in PRESENTATIONAL below; the At a glance numbers,
labels and sources quote r2.

Review draft r3b (Pablo's notes of Nov 11, 11:32 pm, and Nov 12, 12:48 am):
  (a) the closing page keeps the large closing statement, sets the six admin blocks as a quiet
      colophon lower on the page and ends on an Indigo band (Third System, thirdsystem.ai, one
      line) that echoes the cover; the citation points to OSF and thirdsystem.ai instead of
      "SSRN pending"; "About Third System" / "Third System describes" (no "the").
  (b) data-viz colour roles in charts 2 and 5 (report-only copies, build_charts_aias_2_0_report_r3.py).
Approved by Pablo on Nov 12, 2026, 6:57 am, with one change: Consistency in Rust #BD4718 (p.7, and
the current measure on p.8, chart 3, whose first measure stays grey); cover A18; README defaults.
  (c) chart 2's source line cites v0.41 by its thirdsystem.ai/OSF copy (7685100 is not posted).
Every other word, number and figure is r3's, which is r2's.

Run:
    AIAS_ROOT=<worktree> python3 reports/build_report_aias_2_0_r3.py --output <pdf>
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import build_report_aias_2_0 as r2  # noqa: E402  (content adapter + r2 wording)
import ts_layout as L  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

content = r2.content
AIAS_ROOT = r2.AIAS_ROOT
CHART_DIR = AIAS_ROOT / "reports" / "figs" / "aias_2_0" / "report"
# Charts redrawn for r3, source line only: chart 1 cited Methodology v1.9 as SSRN 7685126, which
# SSRN declined; CLAUDE.md's SSRN rule (Nov 11, 2026) moves the AIAS 2.0 report to the
# thirdsystem.ai/OSF citation at this revision. Built by build_charts_aias_2_0_report_r3.py.
R3_CHART_DIR = AIAS_ROOT / "reports" / "figs" / "aias_2_0" / "report_r3"
R3_CHARTS = {"report_fig_01_link_between_scores.pdf",   # source line (v1.9)
             "report_fig_02_brand_order_kept.pdf",      # colour roles; source line (v0.41), r3b
             "report_fig_03_agreement_vs_naming.pdf",   # current measure in Rust (Nov 12)
             "report_fig_05_combined_scores.pdf"}       # wave tints, r3b
REPORT_ID = "AIAS 2.0 synthesis report, revision r3 (Tier 1 restyle)"
# Proposed, pending Pablo's choice: A02 (first draft) is v0.17's photo on the website, so the
# Tier 1 rule rules it out; A17 and A18 are the only free print photos allowed on a C2 cover.
COVER_PHOTO = "A18"

# ---------------------------------------------------------------------------
# New presentational strings (everything else on the page is r2 text)
# ---------------------------------------------------------------------------
RUNNING_LABEL = "AIAS™ 2.0 Synthesis · November 2026"
PRESENTATIONAL = {
    "running_header": RUNNING_LABEL,
    "cover_kicker": RUNNING_LABEL,
    "cover_byline": "Pablo Ulpiano González Castro · thirdsystem.ai",
    "glance_kicker": "AT A GLANCE",
    "contents_kicker": "CONTENTS",
    "intro_kicker": "INTRODUCTION",
    "part_1": ("PART 1", "Five results"),
    "part_2": ("PART 2", "Limitations and what’s next"),
    "finding_kicker": "FINDING {nn} · {verdict}",
    "contents_rows": "At a glance; Introduction; Part 1 Five results; findings 01-05 by headline; "
                     "The five propositions, scored; Part 2 Limitations and what’s next; "
                     "Limitations and what’s next; About Third System",
    "about_heading": "About Third System",  # r3: "About the Third System" (Pablo, Nov 11, 11:32 pm)
    "closing_band": "thirdsystem.ai",        # with the wordmark, on the closing page's Indigo band
}

# Closing page geometry (approved Nov 12, 2026): report_specs.json
# section_template.page_templates.closing_page. Colours are tokens.
_CLOSING_SPEC = L.Tokens(AIAS_ROOT).specs["section_template"]["page_templates"]["closing_page"]
CLOSING_PAGE = {k: v for k, v in _CLOSING_SPEC.items() if k not in ("_note", "band_fill")}
assert CLOSING_PAGE == {
    "band_height_pt": 96, "band_baseline_from_bottom_pt": 42, "colophon_gap_above_band_pt": 34,
    "colophon_rule_gap_pt": 14, "colophon_size_pt": 7.2, "colophon_leading_pt": 9.9,
    "colophon_space_after_pt": 2.2, "colophon_block_gap_pt": 8, "min_gap_below_statement_pt": 30,
}, CLOSING_PAGE
# Pablo, Nov 11, 11:32 pm: SSRN is paused, so the citation points to OSF and thirdsystem.ai:
# the OSF project (the report and data sit in its folder aias_2_0) and the live study page
# (slug "aias-2-0" in the website's src/generated/studies.json, site commit e6d9b6f).
CITATION_TEXT = ("González Castro, P. U. (2026). <i>Presence and Consistency: A Two-Component "
                 "Measurement of AI Availability (The AIAS™ 2.0 Synthesis)</i>. Third System. "
                 "osf.io/ec6wh (folder aias_2_0); thirdsystem.ai/studies/aias-2-0")


def _system_overview() -> str:
    """r2's 'About' paragraph with 'Third System' used as a name (Pablo, Nov 11, 11:32 pm)."""
    text = r2.boilerplate.SYSTEM_OVERVIEW["medium"]
    if not text.startswith("The Third System describes") or text.count("Third System") != 1:
        raise SystemExit("SYSTEM_OVERVIEW changed; check the 'Third System' wording by hand")
    return text.replace("The Third System describes", "Third System describes", 1)


def closing_page(c, t, *, label: str, page_no: int, statement: str, left, right) -> dict:
    """r3b closing page: running header, r2's closing statement large, a quiet two-column colophon
    set low on the page, and a full-bleed Indigo band with one line (wordmark, thirdsystem.ai, page
    number) in place of the footer, echoing the C2 cover's title block."""
    cp = CLOSING_PAGE
    tp = t.pages["text_page"]
    L._paper(c, t)
    rh = t.pages["running_header"]
    st = t.scale["running_header"]
    hb = t.y(rh["baseline_from_top_pt"])
    L.wordmark(c, t, rh["x_pt"], hb, st["wordmark"]["size_pt"])
    L._caps(c, t, t.page_w - t.margin, hb, label, st["label"], align="right")
    band_top = float(cp["band_height_pt"])
    # closing statement: r2's paragraph in the standfirst style, as in r3
    stop = t.y(tp["heading_top_from_top_pt"])
    sbot = L._block(c, lambda: [L._para(t, statement, t.style("standfirst"))], t.margin, stop, t.content_w,
                    band_top, "closing statement", runt=True)
    # colophon: two columns, top-aligned, its lowest line cp["colophon_gap_above_band_pt"] above the band
    gw = tp["gutter_pt"]
    colw = (t.content_w - gw) / 2
    hl, hr = L._height(left, colw), L._height(right, colw)
    ctop = band_top + cp["colophon_gap_above_band_pt"] + max(hl, hr)
    rule_y = ctop + cp["colophon_rule_gap_pt"]
    if rule_y > sbot - cp["min_gap_below_statement_pt"]:
        raise L.LayoutOverflow(f"closing colophon reaches the statement ({sbot - rule_y:.0f} pt apart)")
    ft = t.pages["footer"]
    c.setStrokeColor(t.colour(ft["rule_color"]))
    c.setLineWidth(ft["rule_stroke_pt"])
    c.line(t.margin, rule_y, t.page_w - t.margin, rule_y)
    bl = L._block(c, left, t.margin, ctop, colw, band_top, "colophon left")
    br = L._block(c, right, t.margin + colw + gw, ctop, colw, band_top, "colophon right")
    # Indigo band: the C2 title block's fill, white wordmark, Lavender Grey caps (the C2 kicker style)
    c.setFillColor(t.colour(t.covers["C2"]["title_block"]["fill"]))
    c.rect(0, 0, t.page_w, band_top, stroke=0, fill=1)
    base = float(cp["band_baseline_from_bottom_pt"])
    wm = t.covers["lockup"]["line1"]["size_pt"]
    ww = L.wordmark(c, t, t.margin, base, wm, dark=True)
    kspec = t.style("cover_kicker", "C2")
    L._caps(c, t, t.margin + ww + 1.5 * wm, base, PRESENTATIONAL["closing_band"], kspec)
    L._caps(c, t, t.page_w - t.margin, base, str(page_no), kspec, align="right")
    return {"statement_bottom": sbot, "colophon": {"rule_y": rule_y, "top": ctop, "bottom": min(bl, br)},
            "band": {"top": band_top, "baseline": base}}


def _colophon_styles(t):
    cp = CLOSING_PAGE
    body = {"weight": "Regular", "size_pt": cp["colophon_size_pt"], "leading_pt": cp["colophon_leading_pt"],
            "color": "soft_black"}
    head = dict(body, weight="Bold", color="indigo")

    def p(text, kind="body", before=0.0, after=None):
        spec = head if kind == "head" else body
        return L._para(t, text, spec, spaceBefore=before,
                       spaceAfter=cp["colophon_space_after_pt"] if after is None else after)
    return p

# At a glance: three numbers r2 states, labels and sources quoted from r2.
GLANCE_NUMBERS = [
    {"value": "0.19", "unit": "", "label": "Link between the two scores",
     "source": "November; 0.30 pass mark", "icon": None,
     "r2": "P1: 'The link was 0.07 in May, 0.08 in June and 0.19 in November ... against a pass "
           "mark of 0.30.' Chart 1 title 'Link between the two scores, by wave'; chart label '0.30 pass mark'."},
    {"value": "0.65", "unit": "", "label": "Consistency kept its order",
     "source": "June to November; pass mark 0.50", "icon": None,
     "r2": "P2: 'Consistency kept its order at 0.65 across the 52 brands rated in both waves, "
           "against a pass mark of 0.50.' Chart 2 label 'pass mark 0.50'; 'from June to November'."},
    {"value": "8", "unit": "of 8", "label": "pre-set combined scores failed",
     "source": "Methodology v1.9 calibration record", "icon": None,
     "r2": "Scored table P5: 'DECIDED — 8 of 8 pre-set combined scores failed'. Chart 5 source "
           "'Methodology v1.9 calibration record'."},
]


def _sentences(text: str, n: int) -> str:
    """The first n sentences of an r2 paragraph, verbatim."""
    import re
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z])", text)
    return " ".join(parts[:n])


def build(output: Path, chart_dir: Path = CHART_DIR, photo_id: str = COVER_PHOTO) -> dict:
    t = L.Tokens(AIAS_ROOT)
    L.register_fonts()
    used = L.photo_in_use(t, photo_id, exclude_report=REPORT_ID)
    if used:
        raise SystemExit(f"cover photo {photo_id} already used by {used}")
    if not any(u["report"] == REPORT_ID and u["photo"] == photo_id for u in t.photography["usage_record"]):
        raise SystemExit(f"record {photo_id} for this report in photography.usage_record first")

    brand = t.brand
    findings = content.PATTERNS
    scoring = content.HYPOTHESIS_SCORING
    verdicts = [row[2].split(" — ")[0] for row in scoring["rows"]]
    wwm = content.WHAT_WE_MEASURED
    lim, nxt, clo = content.LIMITATIONS, content.WHATS_NEXT, content.CLOSING

    # Page plan (1-based page numbers)
    plan = ["cover", "glance", "contents", "intro", "part1"] + [f"f{i}" for i in range(1, 6)] + \
           ["scored", "part2", "limits", "closing"]
    pno = {k: i + 1 for i, k in enumerate(plan)}

    fd, base_pdf = tempfile.mkstemp(suffix=".pdf", prefix="aias20_r3_base_")
    os.close(fd)
    c = Canvas(base_pdf, pagesize=(t.page_w, t.page_h))
    c.setTitle(f"{content.COVER['title']} — AIAS™ 2.0 synthesis")
    c.setAuthor("Pablo Ulpiano González Castro")
    c.setSubject("Independent measurement for the AI mediation layer.")
    slots: list = []
    pages: list[dict] = []

    def done(kind: str, info: dict | None = None, elements: tuple = (), words: int | None = None, note: str = ""):
        pages.append({"page": len(pages) + 1, "kind": kind, "elements": list(elements),
                      "words": words, "note": note, "info": info or {}})
        c.showPage()

    # 1 Cover (C2)
    g = L.cover_c2(c, t, photo_path=L.pool_photo(t, photo_id, cover="C2"), kicker=PRESENTATIONAL["cover_kicker"],
                   title=content.COVER["title"], deck=content.COVER["subtitle"],
                   byline=PRESENTATIONAL["cover_byline"])
    done("cover C2", g, note=f"photo {photo_id}")

    # 2 At a glance
    measured = _sentences(wwm["paragraphs"][0], 2)
    g = L.at_a_glance(c, t, label=RUNNING_LABEL, page_no=pno["glance"], standfirst=content.LEAD_DECK,
                      numbers=GLANCE_NUMBERS, measured=measured, summary=[content.EXEC_SUMMARY[0]],
                      kicker=PRESENTATIONAL["glance_kicker"], measured_heading=wwm["heading"].upper(),
                      icons=False)  # this revision carries no icons (none approved yet)
    gw = g["words"]
    done("at a glance", g, ("number_row",), sum(gw.values()),
         note=f"excluding summary {gw['kicker'] + gw['standfirst'] + gw['numbers'] + gw['measured']} (target about 270); summary {gw['summary']}")

    # 3 Contents
    rows = [
        {"kind": "entry", "label": "", "title": "At a glance", "page": pno["glance"]},
        {"kind": "entry", "label": "", "title": "Introduction", "page": pno["intro"]},
        {"kind": "part", "label": PRESENTATIONAL["part_1"][0], "title": PRESENTATIONAL["part_1"][1], "page": pno["part1"]},
    ]
    for i, f in enumerate(findings, start=1):
        rows.append({"kind": "entry", "label": f"{i:02d}", "title": f["title"], "page": pno[f"f{i}"]})
    rows.append({"kind": "entry", "label": "", "title": scoring["heading"], "page": pno["scored"]})
    rows.append({"kind": "part", "label": PRESENTATIONAL["part_2"][0], "title": PRESENTATIONAL["part_2"][1], "page": pno["part2"]})
    rows.append({"kind": "entry", "label": "", "title": f"{lim['heading']} · {nxt['heading']}", "page": pno["limits"]})
    rows.append({"kind": "entry", "label": "", "title": PRESENTATIONAL["about_heading"], "page": pno["closing"]})
    L.contents_page(c, t, label=RUNNING_LABEL, page_no=pno["contents"], rows=rows,
                    kicker=PRESENTATIONAL["contents_kicker"])
    done("contents", words=sum(L.count_words(r["title"]) for r in rows) + 1)

    # 4 Introduction: r2 standfirst, the second summary paragraph, What we measured
    def intro_flow():
        fl = [L.paragraph(t, content.EXEC_SUMMARY[1], "body", space_after=6.5),
              L.paragraph(t, wwm["heading"], "subheading", space_after=4, space_before=8)]
        fl += [L.paragraph(t, p, "body", space_after=6.5) for p in wwm["paragraphs"]]
        return fl
    g = L.text_page(c, t, label=RUNNING_LABEL, page_no=pno["intro"], kicker=PRESENTATIONAL["intro_kicker"],
                    lead=content.STANDFIRST,
                    sections=[{"rule": True, "flowables": intro_flow, "paras": [], "columns": 2}])
    iw = (L.count_words(content.STANDFIRST) + L.count_words(content.EXEC_SUMMARY[1]) +
          L.count_words(wwm["heading"]) + sum(L.count_words(p) for p in wwm["paragraphs"]) + 1)
    done("intro", g, ("section_opener",), iw)

    # 5 Part 1 opener
    L.section_opener(c, t, part=1, title=PRESENTATIONAL["part_1"][1], part_label=PRESENTATIONAL["part_1"][0])
    done("section opener", words=0)

    # 6-10 Findings, one page each (r2 has one chart per finding; no evidence pages)
    for i, f in enumerate(findings, start=1):
        fname, _ = r2._slot_lookup(f["chart_slot"])
        chart_path = (R3_CHART_DIR if fname in R3_CHARTS else chart_dir) / fname
        if not chart_path.is_file():
            raise SystemExit(f"missing chart {chart_path}")
        caption = r2.HERO_FIGURE_CAPTIONS[f["chart_slot"]]
        kicker = PRESENTATIONAL["finding_kicker"].format(nn=f"{i:02d}", verdict=verdicts[i - 1])
        g = L.finding_page(c, t, label=RUNNING_LABEL, page_no=pno[f"f{i}"], page_index=pno[f"f{i}"] - 1,
                           number=i, kicker=kicker, headline=f["title"], chart_path=chart_path,
                           caption=caption, body=f["paragraphs"], slots=slots)
        el = L.chart_element(t, g["chart"]["w"], g["chart"]["h"])
        w = g["words"]
        done(f"finding {i:02d}", g, ("section_opener", el), w["head"] + w["body"],
             note=f"caption {w['caption']} words counted with the chart; chart {g['chart']['h']:.0f} pt tall")

    # 11 Scored table
    rows_t = []
    for h_id, prop, status, cls in scoring["rows"]:
        st = f"<b>{status}</b>" if cls == "confirmed" else (f"<i>{status}</i>" if cls == "descriptive" else status)
        rows_t.append([h_id, prop, st])
    tbl = lambda: [L.table_flowable(t, ["<b>#</b>", "<b>Proposition</b>", "<b>Status</b>"], rows_t, [44, 300, 196])]
    g = L.text_page(c, t, label=RUNNING_LABEL, page_no=pno["scored"],
                    sections=[{"heading": scoring["heading"], "paras": [], "flowables":
                               lambda: [L.paragraph(t, scoring["intro"], "body", space_after=10)] + tbl(),
                               "columns": 1}])
    sw = L.count_words(scoring["heading"]) + L.count_words(scoring["intro"]) + 3 + \
        sum(L.count_words(" ".join(r[:3])) for r in scoring["rows"])
    done("scored table", g, ("section_opener",), sw)

    # 12 Part 2 opener
    L.section_opener(c, t, part=2, title=PRESENTATIONAL["part_2"][1], part_label=PRESENTATIONAL["part_2"][0])
    done("section opener", words=0)

    # 13 Limitations and What's next
    g = L.text_page(c, t, label=RUNNING_LABEL, page_no=pno["limits"],
                    sections=[{"heading": lim["heading"], "paras": lim["paragraphs"], "columns": 2, "gap_after": 26},
                              {"heading": nxt["heading"], "paras": nxt["paragraphs"], "columns": 2}])
    done("limitations, what's next", g, ("section_opener",), g["words"])

    # 14 Closing: r2's closing statement, About, Authored by, Citation, Methodology, datasets
    methodology_text = brand["disclaimers"]["methodology_standard"].replace(
        "(current: v0.3)", "(current: Presence v1.6; Consistency v1.8, v1.9)").replace(
        "Gonzalez Castro", "González Castro")
    citation_text = CITATION_TEXT
    overview = _system_overview()
    about = PRESENTATIONAL["about_heading"]
    cpara = _colophon_styles(t)
    gap = CLOSING_PAGE["colophon_block_gap_pt"]
    left = lambda: ([cpara(about, "head"), cpara(overview, after=gap), cpara("Authored by", "head")] +
                    [cpara(ln) for ln in clo["byline_long"]] +
                    [cpara("Citation", "head", before=gap - CLOSING_PAGE["colophon_space_after_pt"]),
                     cpara(citation_text),
                     cpara("Declarations, including conflicts of interest, are in the paper.", after=0)])
    right = lambda: ([cpara("Methodology", "head"), cpara(methodology_text, after=gap), cpara("Underlying datasets", "head")] +
                     [cpara(ds) for ds in clo["datasets"]] +
                     [cpara(f"<b>Methodology log:</b> {clo['methodology_log']}.", before=gap - CLOSING_PAGE["colophon_space_after_pt"]),
                      cpara("<b>Inquiries:</b> hello@thirdsystem.ai", after=0)])
    cw = (L.count_words(clo["closing_text"]) + L.count_words(about) + L.count_words(overview) +
          2 + sum(L.count_words(x) for x in clo["byline_long"]) + 1 + L.count_words(citation_text) +
          L.count_words("Declarations, including conflicts of interest, are in the paper.") + 1 +
          L.count_words(methodology_text) + 2 + sum(L.count_words(x) for x in clo["datasets"]) +
          L.count_words(f"Methodology log: {clo['methodology_log']}.") + 2 +
          L.count_words(f"Third System {PRESENTATIONAL['closing_band']}"))
    g = closing_page(c, t, label=RUNNING_LABEL, page_no=pno["closing"], statement=clo["closing_text"],
                     left=left, right=right)
    done("closing", g, ("section_opener",), cw,
         note=f"statement ends {t.page_h - g['statement_bottom']:.0f} pt from the top; colophon rule at "
              f"{t.page_h - g['colophon']['rule_y']:.0f} pt; band top {t.page_h - g['band']['top']:.0f} pt")

    c.save()
    output.parent.mkdir(parents=True, exist_ok=True)
    L.overlay_charts(base_pdf, slots, output)
    os.unlink(base_pdf)

    budget = []
    for p in pages:
        if p["words"] is None or p["kind"] in ("cover C2", "section opener"):
            budget.append({**p, "budget": None, "ok": True})
            continue
        chk = L.check_page_budget(t, p["words"], p["elements"])
        budget.append({**p, "budget": chk["budget"], "ok": chk["ok"], "over_by": chk["over_by"]})
    return {"output": str(output), "pages": len(pages), "budget": budget,
            "slots": [(s.page_index + 1, f"{s.chart_path.parent.name}/{s.chart_path.name}", round(s.scale, 4))
                      for s in slots],
            "presentational": PRESENTATIONAL, "glance_numbers": GLANCE_NUMBERS, "photo": photo_id}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--output", type=Path, default=AIAS_ROOT / "reports" / "output" / "aias_2_0_report_r3.pdf")
    ap.add_argument("--chart-dir", type=Path, default=CHART_DIR)
    ap.add_argument("--report-json", type=Path, default=None, help="write the page/word-budget record here")
    a = ap.parse_args()
    res = build(a.output, a.chart_dir)
    for b in res["budget"]:
        flag = "" if b["ok"] else f"  OVER BUDGET by {b.get('over_by')}"
        print(f"p{b['page']:>2} {b['kind']:<28} words={b['words']!s:>4} budget={b['budget']!s:>4} "
              f"{','.join(b['elements'])}{flag}  {b['note']}")
    print("charts:", res["slots"])
    print("wrote", res["output"], res["pages"], "pages")
    if a.report_json:
        slim = {k: v for k, v in res.items()}
        slim["budget"] = [{k: v for k, v in b.items() if k != "info"} for b in res["budget"]]
        a.report_json.write_text(json.dumps(slim, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
