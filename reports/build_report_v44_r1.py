#!/usr/bin/env python3
"""
v0.44 flagship report (Tier 1, report design system v2), revision r1. Managerial register (P1-P5).

Forked from reports/build_report_v40_r1.py (branch v0.40-paper-r2, TS-FL-v0.40-r1): same layout module
(reports/ts_layout.py: C2 cover, at a glance, contents, intro, Indigo section openers, one finding page per finding
with its chart, scored table, limitations with the small-print Disclosures block, closing page with colophon and
Indigo band). Text: reports/v44_report_content.py; every number in it is a {{v:KEY}} placeholder filled here from
papers/v0_44/v44_values.json (the paper's values file) and reports/v44_report_values.json (v44_report_values.py),
merged with no key in both (unknown key -> KeyError). Charts: scripts/build_charts_v44_report.py, merged two-pass
(footprints reserved from the chart mediaboxes, PDFs overlaid).

Report code (decision 14): TS-FL-v0.44-r1, the study's first FL revision. The catalogue entry is added after the
build (check_code refuses a registered code without the PDF's SHA-256); remove it before any rebuild.

Run from the repo or worktree root:
    AIAS_ROOT=$PWD ~/aias/venv/bin/python reports/build_report_v44_r1.py [--code TS-FL-v0.44-r1] [--out-dir DIR]
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
ROOT = Path(os.environ.get("AIAS_ROOT") or SCRIPT_DIR.parent)
sys.path.insert(0, str(SCRIPT_DIR))

import report_code as RC  # noqa: E402
import small_print as SP  # noqa: E402
import ts_layout as L  # noqa: E402
import v44_report_content as C  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

CHART_DIR = ROOT / "reports/figs/v44/report"
REPORT_ID = "v0.44 flagship"
COVER_PHOTO = "v0.44_clothing-department-stores"
CITATION_WHERE = "osf.io/ec6wh (folder v44); thirdsystem.ai"
PDF_SUBJECT = "Independent measurement for the AI mediation layer."
VALUE_FILES = ("papers/v0_44/v44_values.json", "reports/v44_report_values.json")
VALUES: dict = {}
for _vf in VALUE_FILES:
    _vals = json.loads((ROOT / _vf).read_text(encoding="utf-8"))["values"]
    _dup = set(VALUES) & set(_vals)
    if _dup:
        raise SystemExit(f"key in both values files: {sorted(_dup)[:5]}")
    VALUES.update(_vals)
USED_KEYS: set = set()
RUNNING_LABEL = f"AIAS™ v0.44 · {VALUES['rv.collection_month']['display']}"


def _fill(s: str) -> str:
    def rep(m):
        k = m.group(1).strip()
        if k not in VALUES:
            raise KeyError(k)
        USED_KEYS.add(k)
        return VALUES[k]["display"]
    return re.sub(r"\{\{v:([^}]+)\}\}", rep, s)


def f(x):
    """Fill {{v:KEY}} placeholders in a string, list or dict, recording the keys used."""
    if isinstance(x, str):
        out = _fill(x)
        if "{{" in out:
            raise SystemExit(f"unfilled template syntax: {out[:80]}")
        return out
    if isinstance(x, list):
        return [f(i) for i in x]
    if isinstance(x, dict):
        return {k: f(v) for k, v in x.items()}
    return x


def build(output: Path, code: str) -> dict:
    t = L.Tokens(ROOT)
    L.register_fonts()
    SP.preflight_styles(t)
    RC.check_code(code, t.catalogue)
    want = RC.file_name(code, C.TITLE)
    if output.name != want:
        raise SystemExit(f"the PDF must be named {want}, not {output.name}")
    used = L.photo_in_use(t, COVER_PHOTO, exclude_report=REPORT_ID)
    if used:
        raise SystemExit(f"cover photo {COVER_PHOTO} already used by {used}")

    findings = f(C.FINDINGS)
    nf = len(findings)
    plan = ["cover", "glance", "contents", "intro", "part1"] + [f"f{i}" for i in range(1, nf + 1)] + \
           ["scored", "part2", "limits", "closing"]
    pno = {k: i + 1 for i, k in enumerate(plan)}
    part1_title = f"{['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six'][nf]} results"
    scored_head = f(C.SCORED_HEAD)

    fd, base_pdf = tempfile.mkstemp(suffix=".pdf", prefix="v44_r1_base_")
    os.close(fd)
    c = Canvas(base_pdf, pagesize=(t.page_w, t.page_h))
    c.setTitle(f"{C.TITLE} — AIAS™ v0.44")
    c.setAuthor("Pablo Ulpiano González Castro")
    c.setSubject(RC.pdf_subject(code, PDF_SUBJECT))
    c.setKeywords(RC.pdf_keywords(code, "Third System", "AIAS v0.44", t.website))
    slots: list = []
    pages: list[dict] = []

    def done(kind, info=None, elements=(), words=None, note=""):
        pages.append({"page": len(pages) + 1, "kind": kind, "elements": list(elements), "words": words, "note": note})
        c.showPage()

    # 1 Cover (C2): library photo; the AI credit is in the colophon
    g = L.cover_c2(c, t, photo_path=L.pool_photo(t, COVER_PHOTO, cover="C2"), kicker=RUNNING_LABEL,
                   title=C.TITLE, deck=f(C.DECK), byline="Pablo Ulpiano González Castro · thirdsystem.ai", code=code)
    done("cover C2", g, note=f"photo {COVER_PHOTO}")

    # 2 At a glance
    g = L.at_a_glance(c, t, label=RUNNING_LABEL, page_no=pno["glance"], standfirst=f(C.STANDFIRST),
                      numbers=[dict(n, icon=None) for n in f(C.GLANCE_NUMBERS)], measured=f(C.MEASURED),
                      summary=f(C.SUMMARY), measured_heading=C.MEASURED_HEAD.upper(), icons=False)
    done("at a glance", g, ("number_row",), sum(g["words"].values()))

    # 3 Contents
    rows = [{"kind": "entry", "label": "", "title": "At a glance", "page": pno["glance"]},
            {"kind": "entry", "label": "", "title": "Introduction", "page": pno["intro"]},
            {"kind": "part", "label": "PART 1", "title": part1_title, "page": pno["part1"]}]
    for i, fi in enumerate(findings, start=1):
        if len(fi["title"]) >= 58:
            raise SystemExit(f"finding title too long for the contents: {fi['title']}")
        rows.append({"kind": "entry", "label": f"{i:02d}", "title": fi["title"], "page": pno[f"f{i}"]})
    rows += [{"kind": "entry", "label": "", "title": scored_head, "page": pno["scored"]},
             {"kind": "part", "label": "PART 2", "title": "Limits and what's next", "page": pno["part2"]},
             {"kind": "entry", "label": "", "title": "Limitations · What's next · Disclosures", "page": pno["limits"]},
             {"kind": "entry", "label": "", "title": "About Third System", "page": pno["closing"]}]
    L.contents_page(c, t, label=RUNNING_LABEL, page_no=pno["contents"], rows=rows)
    done("contents")

    # 4 Introduction
    def intro_flow():
        fl = [L.paragraph(t, p, "body", space_after=6.5) for p in f(C.INTRO)]
        fl.append(L.paragraph(t, C.MEASURED_HEAD, "subheading", space_after=4, space_before=8))
        fl += [L.paragraph(t, p, "body", space_after=6.5) for p in f(C.MEASURED_PARAS)]
        return fl
    g = L.text_page(c, t, label=RUNNING_LABEL, page_no=pno["intro"], kicker="INTRODUCTION", lead=f(C.INTRO_LEAD),
                    sections=[{"rule": True, "flowables": intro_flow, "paras": [], "columns": 2}])
    done("intro", g, ("section_opener",), g["words"])

    # 5 Part 1 opener
    L.section_opener(c, t, part=1, title=part1_title, part_label="PART 1")
    done("section opener")

    # Findings
    for i, fi in enumerate(findings, start=1):
        chart = CHART_DIR / fi["chart"]
        if not chart.is_file():
            raise SystemExit(f"missing chart {chart}")
        g = L.finding_page(c, t, label=RUNNING_LABEL, page_no=pno[f"f{i}"], page_index=pno[f"f{i}"] - 1, number=i,
                           kicker=f"FINDING {i:02d} · {fi['verdict']}", headline=fi["title"], chart_path=chart,
                           caption=fi["caption"], body=fi["body"], slots=slots)
        el = L.chart_element(t, g["chart"]["w"], g["chart"]["h"])
        done(f"finding {i:02d}", g, ("section_opener", el), g["words"]["head"] + g["words"]["body"])

    # Scored table
    rows_t = [[r[0], r[1], f"<b>{r[2]}</b>" if r[2].startswith(("CONFIRMED",)) else r[2]] for r in f(C.SCORED_ROWS)]
    tbl = lambda: [L.table_flowable(t, ["<b>#</b>", "<b>What we tested</b>", "<b>Outcome</b>"], rows_t, [36, 250, 254])]
    g = L.text_page(c, t, label=RUNNING_LABEL, page_no=pno["scored"],
                    sections=[{"heading": scored_head, "paras": [], "columns": 1,
                               "flowables": lambda: [L.paragraph(t, f(C.SCORED_INTRO), "body", space_after=10)] + tbl()}])
    done("scored table", g)

    # Part 2 opener
    L.section_opener(c, t, part=2, title="Limits and what's next", part_label="PART 2")
    done("section opener")

    # Limitations, What's next, Disclosures (small print at the foot)
    L.running_chrome(c, t, RUNNING_LABEL, pno["limits"])
    tp = t.pages["text_page"]
    fb = SP.foot_blocks(c, t, disclosures=f(C.DISCLOSURES))
    bottom = fb["body_bottom"]
    y = t.y(tp["heading_top_from_top_pt"])
    colw = (t.content_w - tp["gutter_pt"]) / 2
    xs = [t.margin, t.margin + colw + tp["gutter_pt"]]
    for head, paras in ((C.LIMITS_HEAD, f(C.LIMITS)), (C.NEXT_HEAD, f(C.NEXT))):
        y = L._block(c, lambda h=head: [L._para(t, h, t.style("finding_headline"))], t.margin, y, t.content_w,
                     bottom, "heading", runt=True) - 12
        res = L._columns(c, lambda ps=paras: L._body_paras(t, ps), y, bottom, xs, colw, head)
        y = res["bottom"] - 22
    done("limitations, what's next, disclosures")

    # Closing
    cp = L.colophon_paragraphs(t)
    CLOSING = t.pages["closing_page"]
    gap = CLOSING["colophon_block_gap_pt"]
    cite = RC.cite(f"González Castro, P. U. ({VALUES['rv.collection_month']['value'][:4]}).", f"{C.TITLE}: AIAS™ v0.44", code, CITATION_WHERE)
    about = ("Third System is an independent research entity that measures how AI answers represent brands. It does "
             "not accept compensation contingent on improving a brand's AI Availability Score or securing favorable "
             "AI recommendations.")
    meth = f("Pre-registered study, locked at git tag v0.44-prereg-r1 and deposited on OSF before the first question. "
             "Every result number in this report is read from the study's values files (papers/v0_44/v44_values.json "
             "and reports/v44_report_values.json, written by code from the scored data); dates come from the "
             "collection record and the DEVIATIONS log. The academic paper gives every test in full.")
    left = lambda: [cp("About Third System", "head"), cp(about, after=gap), cp("Authored by", "head"),
                    cp("Pablo Ulpiano González Castro"),
                    cp("School of Visual Arts, MPS Branding Program, New York (primary academic affiliation)"),
                    cp("Citation", "head", before=gap - CLOSING["colophon_space_after_pt"]), cp(cite, after=0)]
    right = lambda: [cp("Methodology", "head"), cp(meth, after=gap), cp("Underlying data", "head"),
                     cp("Tier sources: NAIC, ScrapeHero, HOTELS 325, NRF Top 100 Retailers, QSR 50, Drug Channels "
                        "Institute, CSP Top 40, Interbrand Best Global Brands, Lyst Index. Plan and registries: OSF "
                        "ec6wh, folder v44; answers, coding and logs: v44/data; verdicts and unit table: "
                        "v44/scoring; values files: github.com/thirdsystem-aias/aias, branch v0.44."),
                     cp("Cover image generated with AI.", before=gap - CLOSING["colophon_space_after_pt"]),
                     cp("<b>Inquiries:</b> hello@thirdsystem.ai", after=0)]
    g = L.closing_page(c, t, label=RUNNING_LABEL, page_no=pno["closing"], statement=f(C.CLOSING_STATEMENT),
                       left=left, right=right, code=code)
    done("closing", g)

    c.save()
    output.parent.mkdir(parents=True, exist_ok=True)
    L.overlay_charts(base_pdf, slots, output)
    os.unlink(base_pdf)
    pf = RC.preflight(output, code, C.TITLE, t.catalogue, t.website)
    sizes = SP.check_pdf_min_size(output)
    budget = []
    for p in pages:
        if p["words"] is None:
            budget.append({**p, "budget": None, "ok": True})
            continue
        chk = L.check_page_budget(t, p["words"], p["elements"])
        budget.append({**p, "budget": chk["budget"], "ok": chk["ok"]})
    return {"output": str(output), "pages": len(pages), "budget": budget, "preflight": pf, "min_size": sizes,
            "value_keys": sorted(USED_KEYS)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default="TS-FL-v0.44-r1")
    ap.add_argument("--out-dir", type=Path, default=ROOT / "reports" / "output")
    a = ap.parse_args()
    out = a.out_dir / RC.file_name(a.code, C.TITLE)
    res = build(out, a.code)
    for b in res["budget"]:
        print(f"p{b['page']:>2} {b['kind']:<40} words={b['words']!s:>4} budget={b['budget']!s:>4} "
              f"{'' if b['ok'] else 'OVER'}")
    print("pre-flight:", "PASS" if res["preflight"]["ok"] else "FAIL", res["preflight"]["problems"] or "")
    print("min text size:", res["min_size"])
    print("value keys:", len(res["value_keys"]))
    (ROOT / "reports/output").mkdir(parents=True, exist_ok=True)
    (out.parent / (out.stem + "_value_keys.json")).write_text(json.dumps(res["value_keys"], indent=1) + "\n")
    print("wrote", res["output"], res["pages"], "pages")


if __name__ == "__main__":
    main()
