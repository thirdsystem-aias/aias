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

Report code (Pablo, Nov 13, 2026, decisions 13 and 14; reports/report_code.py): r3 is registered as
TS-SY-AIAS2.0-r3 (brand/report_specs.json report_catalogue). Any new render is a new revision and
takes the next code, TS-SY-AIAS2.0-r4: the code is printed in the closing band after
"thirdsystem.ai" (lower case), in the Citation block and in the PDF metadata (Subject, Keywords),
and names the file, TS-SY-AIAS2.0-r4_how-often-and-how-evenly.pdf. The website prints in lower case
everywhere, the cover byline included. A code already registered is refused, and so is an output
path that holds a registered (published) PDF. --test marks a check render with a code that is not
registered (it must be written outside osf/ and reports/output/). The pre-flight addition runs on
the written PDF.

Run:
    AIAS_ROOT=<worktree> python3 reports/build_report_aias_2_0_r3.py --code TS-SY-AIAS2.0-r4 --out-dir <dir> [--test]
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
import report_code as RC  # noqa: E402
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
    # the closing page's Indigo band: wordmark, the website in lower case, the report code, the page
    # number (decision 13 as updated Nov 13, 2026; drawn by ts_layout.closing_page())
    "closing_band": "thirdsystem.ai",
}

# Closing page geometry (approved Nov 12, 2026; band line Nov 13): report_specs.json
# section_template.page_templates.closing_page, drawn by ts_layout.closing_page().
CLOSING_PAGE = L.Tokens(AIAS_ROOT).pages["closing_page"]
# Pablo, Nov 11, 11:32 pm: SSRN is paused, so the citation points to OSF and thirdsystem.ai:
# the OSF project (the report and data sit in its folder aias_2_0) and the live study page
# (slug "aias-2-0" in the website's src/generated/studies.json, site commit e6d9b6f).
# Nov 13 (decision 14): the citation carries the report code after the title.
CITATION_TITLE = ("Presence and Consistency: A Two-Component Measurement of AI Availability "
                  "(The AIAS™ 2.0 Synthesis)")
CITATION_WHERE = "osf.io/ec6wh (folder aias_2_0); thirdsystem.ai/studies/aias-2-0"
PDF_SUBJECT = "Independent measurement for the AI mediation layer."


def citation_text(code: str) -> str:
    return RC.cite("González Castro, P. U. (2026).", CITATION_TITLE, code, CITATION_WHERE)


def _system_overview() -> str:
    """r2's 'About' paragraph with 'Third System' used as a name (Pablo, Nov 11, 11:32 pm)."""
    text = r2.boilerplate.SYSTEM_OVERVIEW["medium"]
    if not text.startswith("The Third System describes") or text.count("Third System") != 1:
        raise SystemExit("SYSTEM_OVERVIEW changed; check the 'Third System' wording by hand")
    return text.replace("The Third System describes", "Third System describes", 1)


# The closing page (statement, colophon, Indigo band with the report code) is ts_layout.closing_page();
# its colophon paragraphs come from ts_layout.colophon_paragraphs() (Nov 13, 2026: moved there from
# this builder unchanged, so v0.40 builds the same page).

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


def build(output: Path, code: str, chart_dir: Path = CHART_DIR, photo_id: str = COVER_PHOTO,
          test: bool = False) -> dict:
    t = L.Tokens(AIAS_ROOT)
    L.register_fonts()
    # Report code (decision 14): a code already in the catalogue is refused (a published PDF is never
    # re-rendered); a new code must be the next revision; the file is named after the code.
    RC.check_code(code, t.catalogue)
    want = RC.file_name(code, content.COVER["title"])
    if output.name != want:
        raise SystemExit(f"the PDF must be named {want} (decision 14), not {output.name}")
    if output.exists():
        registered = set().union(*(RC.registered_hashes(e) for e in t.catalogue)) if t.catalogue else set()
        if RC.sha256_file(output) in registered:
            raise SystemExit(f"{output} is a registered (published) PDF; it is never overwritten")
    if test:
        published_dirs = [AIAS_ROOT / "osf", AIAS_ROOT / "reports" / "output"]
        if any(output.resolve().is_relative_to(d.resolve()) for d in published_dirs):
            raise SystemExit("--test renders go to a scratch folder, not osf/ or reports/output/")
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
    c.setSubject(RC.pdf_subject(code, PDF_SUBJECT))
    c.setKeywords(RC.pdf_keywords(code, "Third System", "AIAS 2.0", t.website))
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
    cite = citation_text(code)
    overview = _system_overview()
    about = PRESENTATIONAL["about_heading"]
    cpara = L.colophon_paragraphs(t)
    gap = CLOSING_PAGE["colophon_block_gap_pt"]
    left = lambda: ([cpara(about, "head"), cpara(overview, after=gap), cpara("Authored by", "head")] +
                    [cpara(ln) for ln in clo["byline_long"]] +
                    [cpara("Citation", "head", before=gap - CLOSING_PAGE["colophon_space_after_pt"]),
                     cpara(cite),
                     cpara("Declarations, including conflicts of interest, are in the paper.", after=0)])
    right = lambda: ([cpara("Methodology", "head"), cpara(methodology_text, after=gap), cpara("Underlying datasets", "head")] +
                     [cpara(ds) for ds in clo["datasets"]] +
                     [cpara(f"<b>Methodology log:</b> {clo['methodology_log']}.", before=gap - CLOSING_PAGE["colophon_space_after_pt"]),
                      cpara("<b>Inquiries:</b> hello@thirdsystem.ai", after=0)])
    cw = (L.count_words(clo["closing_text"]) + L.count_words(about) + L.count_words(overview) +
          2 + sum(L.count_words(x) for x in clo["byline_long"]) + 1 + L.count_words(cite) +
          L.count_words("Declarations, including conflicts of interest, are in the paper.") + 1 +
          L.count_words(methodology_text) + 2 + sum(L.count_words(x) for x in clo["datasets"]) +
          L.count_words(f"Methodology log: {clo['methodology_log']}.") + 2 +
          L.count_words(f"Third System {t.website} {code}"))
    g = L.closing_page(c, t, label=RUNNING_LABEL, page_no=pno["closing"], statement=clo["closing_text"],
                       left=left, right=right, code=code)
    done("closing", g, ("section_opener",), cw,
         note=f"statement ends {t.page_h - g['statement_bottom']:.0f} pt from the top; colophon rule at "
              f"{t.page_h - g['colophon']['rule_y']:.0f} pt; band top {t.page_h - g['band']['top']:.0f} pt; "
              f"band: {g['band']['website']['text']} · {g['band']['code']['text']} at x={g['band']['website']['x']:.1f}")

    c.save()
    output.parent.mkdir(parents=True, exist_ok=True)
    L.overlay_charts(base_pdf, slots, output)
    os.unlink(base_pdf)
    # Pre-flight addition (decision 14): last page, file name, metadata, register.
    pf = RC.preflight(output, code, content.COVER["title"], t.catalogue, t.website)

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
            "presentational": PRESENTATIONAL, "glance_numbers": GLANCE_NUMBERS, "photo": photo_id,
            "code": code, "test": test, "preflight": pf,
            # the register entry to add at publication (git tag, OSF path and date are filled in then)
            "catalogue_entry": {"code": code, "title": content.COVER["title"], "date": None, "tier": 1,
                                "git_tag": None, "osf_path": None, "sha256": pf["sha256"],
                                "file": output.name, "test": test}}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--code", required=True, help="the report code of this render, e.g. TS-SY-AIAS2.0-r4")
    ap.add_argument("--test", action="store_true", help="a check render with a code that is not registered")
    ap.add_argument("--out-dir", type=Path, default=AIAS_ROOT / "reports" / "output")
    ap.add_argument("--output", type=Path, default=None, help="full path; its name must be CODE_<title-slug>.pdf")
    ap.add_argument("--chart-dir", type=Path, default=CHART_DIR)
    ap.add_argument("--report-json", type=Path, default=None, help="write the page/word-budget record here")
    a = ap.parse_args()
    output = a.output or a.out_dir / RC.file_name(a.code, content.COVER["title"])
    res = build(output, a.code, a.chart_dir, test=a.test)
    for b in res["budget"]:
        flag = "" if b["ok"] else f"  OVER BUDGET by {b.get('over_by')}"
        print(f"p{b['page']:>2} {b['kind']:<28} words={b['words']!s:>4} budget={b['budget']!s:>4} "
              f"{','.join(b['elements'])}{flag}  {b['note']}")
    print("charts:", res["slots"])
    print("wrote", res["output"], res["pages"], "pages", "(test render, code not registered)" if a.test else "")
    pf = res["preflight"]
    print("pre-flight:", "PASS" if pf["ok"] else "FAIL", pf["checks"], pf["problems"] or "")
    print("sha256:", pf["sha256"])
    if a.report_json:
        slim = {k: v for k, v in res.items()}
        slim["budget"] = [{k: v for k, v in b.items() if k != "info"} for b in res["budget"]]
        a.report_json.write_text(json.dumps(slim, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
