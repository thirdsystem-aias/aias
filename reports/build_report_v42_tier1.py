#!/usr/bin/env python3
"""
v0.42 t4 wave report: Tier 1 flagship in report design system v2.

Text comes from the v0.42 pipeline itself: reports/v42_t4_generation_content.py (written before the data; every
number read from osf/v42/v42_verdicts.json through papers/v0_42/v42_values.py), as reshaped by
build_report_v42.py's content adapter and its chart captions (HERO_FIGURE_CAPTIONS). Charts are the report-register
copies in design system v2 colour roles, reports/figs/v42/report_v2/ (scripts/build_charts_v42_report_v2.py),
merged unchanged (two-pass: chart footprints reserved from the PDF mediaboxes in pass 1, PDFs overlaid in pass 2).
Layout is reports/ts_layout.py, following the AIAS 2.0 report r3 builder (build_report_aias_2_0_r3.py).

New presentational strings (kickers, part titles, contents, the running header, the At a glance labels and sources,
the colophon's dataset lines and citation) are in PRESENTATIONAL and below; the At a glance numbers are read from the
same verdicts the paper reports.

Report code (decision 14; reports/report_code.py): Tier 1 flagship, type FL, study v0.42: TS-FL-v0.42-rN, printed as
registered in the closing band (after "thirdsystem.ai", lower case), the Citation block, the PDF metadata and the
file name. The cover byline prints thirdsystem.ai in lower case.

Cover photo (photo library v2, Pablo, Nov 12, 2026): the image comes from the AI-generated library
(Try system book/photo_library_ai/selected/print/, library_manifest.json) and carries the AI credit in the colophon.
--photo takes the print file. The t4 wave has no library image yet (Nov 13); until Pablo generates one, only
--test renders are possible, with any stand-in image (they are never published).

Run:
    AIAS_ROOT=<worktree> python3 reports/build_report_v42_tier1.py --code TS-FL-v0.42-r1 --photo <print png> --out-dir <dir>
    ... --test --photo <stand-in> --out-dir <scratch dir>      # check render, never published
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
sys.path.insert(0, str(SCRIPT_DIR))

import build_report_v42 as r2  # noqa: E402  (content adapter + captions)
import report_code as RC  # noqa: E402
import ts_layout as L  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

content = r2.content
AIAS_ROOT = Path(os.environ.get("AIAS_ROOT", str(SCRIPT_DIR.parent)))
CHART_DIR = AIAS_ROOT / "reports" / "figs" / "v42" / "report_v2"
LIBRARY = Path.home() / "aias" / "Try system book" / "photo_library_ai" / "selected"
AI_CREDIT = "Cover image generated with AI; art direction by Third System."

RUNNING_LABEL = "AIAS™ Fourth Wave · v0.42 · November 2026"
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
    "about_heading": "About Third System",
}
CLOSING_PAGE = L.Tokens(AIAS_ROOT).pages["closing_page"]
CITATION_TITLE = "New Models, Same Standings? The AIAS™ fourth wave on the newest AI models (v0.42)"
CITATION_WHERE = "osf.io/ec6wh (folder v42); thirdsystem.ai"
PDF_SUBJECT = "Independent measurement for the AI mediation layer."
DATASETS = [
    "Pre-registration, probes and scripts: OSF ec6wh, folder v42/prereg (tag v0.42-prereg-r1)",
    "Answers with search records and usage, coded tables: folder v42/data",
    "Verdicts and brand table: v42/v42_verdicts.json, v42/v42_brand_table.csv",
    "Paper: folder v42/paper",
]
METHODOLOGY_LOG = "v0.42 (thirdsystem.ai; OSF ec6wh, folder v42)"

# At a glance: three numbers the paper and the content module state, read from the verdicts.
_G, _PH, _S = content.G, content.PH, content.S
GLANCE_NUMBERS = [
    {"value": content.r2(_G["rho"]), "unit": "", "label": "Presence order kept",
     "source": f"retiring vs newest models; {content.i0(_G['n'])} brands; bar 0.70", "icon": None},
    {"value": content.r2(_PH["rho"]), "unit": "", "label": "Consistency order kept",
     "source": f"{content.i0(_PH['n'])} brands; bar 0.50, change below 0.30", "icon": None},
    {"value": content.r2(_S["rho"]), "unit": "", "label": "Presence order, search off vs on",
     "source": "112 brands; unchanged if the range is 0.80 or more", "icon": None},
]


def _sentences(text: str, n: int) -> str:
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z])", text)
    return " ".join(parts[:n])


def citation_text(code: str) -> str:
    return RC.cite("González Castro, P. U. (2026).", CITATION_TITLE, code, CITATION_WHERE)


def _system_overview() -> str:
    text = r2.boilerplate.SYSTEM_OVERVIEW["medium"]
    if text.startswith("The Third System describes") and text.count("Third System") == 1:
        text = text.replace("The Third System describes", "Third System describes", 1)
    if "the Third System" in text or "The Third System" in text:
        raise SystemExit("SYSTEM_OVERVIEW changed; check the 'Third System' wording by hand")
    return text


def build(output: Path, code: str, photo: Path, chart_dir: Path = CHART_DIR, test: bool = False) -> dict:
    t = L.Tokens(AIAS_ROOT)
    L.register_fonts()
    RC.check_code(code, t.catalogue)
    if RC.parse_code(code)["type"] != "FL" or RC.parse_code(code)["study"] != "v0.42":
        raise SystemExit("the t4 wave report is a Tier 1 flagship: TS-FL-v0.42-rN")
    want = RC.file_name(code, content.COVER["title"])
    if output.name != want:
        raise SystemExit(f"the PDF must be named {want} (decision 14), not {output.name}")
    if output.exists():
        registered = set().union(*(RC.registered_hashes(e) for e in t.catalogue)) if t.catalogue else set()
        if RC.sha256_file(output) in registered:
            raise SystemExit(f"{output} is a registered (published) PDF; it is never overwritten")
    photo = Path(photo)
    from_library = LIBRARY.resolve() in photo.resolve().parents
    if test:
        published_dirs = [AIAS_ROOT / "osf", AIAS_ROOT / "reports" / "output"]
        if any(output.resolve().is_relative_to(d.resolve()) for d in published_dirs):
            raise SystemExit("--test renders go to a scratch folder, not osf/ or reports/output/")
    elif not (from_library and photo.parent.name == "print" and photo.is_file()):
        raise SystemExit("a published render takes its cover from the photo library's print/ folder (photo library v2)")

    findings = content.PATTERNS
    scoring = content.HYPOTHESIS_SCORING
    verdicts = [row[2].split(" — ")[0] for row in scoring["rows"]]
    wwm = content.WHAT_WE_MEASURED
    lim, nxt, clo = content.LIMITATIONS, content.WHATS_NEXT, content.CLOSING

    plan = ["cover", "glance", "contents", "intro", "part1"] + [f"f{i}" for i in range(1, 6)] + \
           ["scored", "part2", "limits", "closing"]
    pno = {k: i + 1 for i, k in enumerate(plan)}

    fd, base_pdf = tempfile.mkstemp(suffix=".pdf", prefix="v42_t1_base_")
    os.close(fd)
    c = Canvas(base_pdf, pagesize=(t.page_w, t.page_h))
    c.setTitle(f"{content.COVER['title']} — AIAS™ v0.42, fourth wave")
    c.setAuthor("Pablo Ulpiano González Castro")
    c.setSubject(RC.pdf_subject(code, PDF_SUBJECT))
    c.setKeywords(RC.pdf_keywords(code, "Third System", "AIAS v0.42", t.website))
    slots: list = []
    pages: list[dict] = []

    def done(kind, info=None, elements=(), words=None, note=""):
        pages.append({"page": len(pages) + 1, "kind": kind, "elements": list(elements),
                      "words": words, "note": note, "info": info or {}})
        c.showPage()

    # 1 Cover (C2)
    g = L.cover_c2(c, t, photo_path=photo, kicker=PRESENTATIONAL["cover_kicker"], title=content.COVER["title"],
                   deck=content.COVER["subtitle"], byline=PRESENTATIONAL["cover_byline"])
    done("cover C2", g, note=f"photo {photo.name}{' (library, AI)' if from_library else ' (TEST stand-in)'}")

    # 2 At a glance
    measured = _sentences(wwm["paragraphs"][0], 2)
    g = L.at_a_glance(c, t, label=RUNNING_LABEL, page_no=pno["glance"], standfirst=content.LEAD_DECK,
                      numbers=GLANCE_NUMBERS, measured=measured, summary=[content.EXEC_SUMMARY[0]],
                      kicker=PRESENTATIONAL["glance_kicker"], measured_heading=wwm["heading"].upper(), icons=False)
    gw = g["words"]
    done("at a glance", g, ("number_row",), sum(gw.values()),
         note=f"excluding summary {gw['kicker'] + gw['standfirst'] + gw['numbers'] + gw['measured']} (target about 270); summary {gw['summary']}")

    # 3 Contents
    rows = [{"kind": "entry", "label": "", "title": "At a glance", "page": pno["glance"]},
            {"kind": "entry", "label": "", "title": "Introduction", "page": pno["intro"]},
            {"kind": "part", "label": PRESENTATIONAL["part_1"][0], "title": PRESENTATIONAL["part_1"][1], "page": pno["part1"]}]
    for i, f in enumerate(findings, start=1):
        rows.append({"kind": "entry", "label": f"{i:02d}", "title": f["title"], "page": pno[f"f{i}"]})
    rows.append({"kind": "entry", "label": "", "title": scoring["heading"], "page": pno["scored"]})
    rows.append({"kind": "part", "label": PRESENTATIONAL["part_2"][0], "title": PRESENTATIONAL["part_2"][1], "page": pno["part2"]})
    rows.append({"kind": "entry", "label": "", "title": f"{lim['heading']} · {nxt['heading']}", "page": pno["limits"]})
    rows.append({"kind": "entry", "label": "", "title": PRESENTATIONAL["about_heading"], "page": pno["closing"]})
    L.contents_page(c, t, label=RUNNING_LABEL, page_no=pno["contents"], rows=rows, kicker=PRESENTATIONAL["contents_kicker"])
    done("contents", words=sum(L.count_words(r["title"]) for r in rows) + 1)

    # 4 Introduction: standfirst, the implication paragraph, What we measured
    def intro_flow():
        fl = [L.paragraph(t, p, "body", space_after=6.5) for p in content.EXEC_SUMMARY[1:]]
        fl.append(L.paragraph(t, wwm["heading"], "subheading", space_after=4, space_before=8))
        fl += [L.paragraph(t, p, "body", space_after=6.5) for p in wwm["paragraphs"]]
        return fl
    g = L.text_page(c, t, label=RUNNING_LABEL, page_no=pno["intro"], kicker=PRESENTATIONAL["intro_kicker"],
                    lead=content.STANDFIRST, sections=[{"rule": True, "flowables": intro_flow, "paras": [], "columns": 2}])
    iw = (L.count_words(content.STANDFIRST) + sum(L.count_words(p) for p in content.EXEC_SUMMARY[1:]) +
          L.count_words(wwm["heading"]) + sum(L.count_words(p) for p in wwm["paragraphs"]) + 1)
    done("intro", g, ("section_opener",), iw)

    # 5 Part 1 opener
    L.section_opener(c, t, part=1, title=PRESENTATIONAL["part_1"][1], part_label=PRESENTATIONAL["part_1"][0])
    done("section opener", words=0)

    # 6-10 Findings, one page each, one chart per finding
    for i, f in enumerate(findings, start=1):
        fname, _ = r2._slot_lookup(f["chart_slot"])
        chart_path = chart_dir / fname
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
                               lambda: [L.paragraph(t, scoring["intro"], "body", space_after=10)] + tbl(), "columns": 1}])
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

    # 14 Closing
    methodology_text = t.brand["disclaimers"]["methodology_standard"].replace(
        "(current: v0.3)", "(current: Presence v1.6; Consistency v1.8)").replace("Gonzalez Castro", "González Castro")
    cite = citation_text(code)
    overview = _system_overview()
    about = PRESENTATIONAL["about_heading"]
    cpara = L.colophon_paragraphs(t)
    gap = CLOSING_PAGE["colophon_block_gap_pt"]
    after_gap = gap - CLOSING_PAGE["colophon_space_after_pt"]
    decl = "Declarations, including conflicts of interest, are in the paper."
    credit = [cpara(AI_CREDIT, before=after_gap, after=0)] if from_library else []
    left = lambda: ([cpara(about, "head"), cpara(overview, after=gap), cpara("Authored by", "head")] +
                    [cpara(ln) for ln in clo["byline_long"]] +
                    [cpara("Citation", "head", before=after_gap), cpara(cite), cpara(decl, after=0)] + credit)
    right = lambda: ([cpara("Methodology", "head"), cpara(methodology_text, after=gap), cpara("Underlying datasets", "head")] +
                     [cpara(ds) for ds in DATASETS] +
                     [cpara(f"<b>Methodology log:</b> {METHODOLOGY_LOG}.", before=after_gap),
                      cpara("<b>Inquiries:</b> hello@thirdsystem.ai", after=0)])
    cw = (L.count_words(clo["closing_text"]) + L.count_words(about) + L.count_words(overview) + 2 +
          sum(L.count_words(x) for x in clo["byline_long"]) + 1 + L.count_words(cite) + L.count_words(decl) +
          (L.count_words(AI_CREDIT) if from_library else 0) + 1 + L.count_words(methodology_text) + 2 +
          sum(L.count_words(x) for x in DATASETS) + L.count_words(f"Methodology log: {METHODOLOGY_LOG}.") + 2 +
          L.count_words(f"Third System {t.website} {code}"))
    g = L.closing_page(c, t, label=RUNNING_LABEL, page_no=pno["closing"], statement=clo["closing_text"],
                       left=left, right=right, code=code)
    done("closing", g, ("section_opener",), cw,
         note=f"statement ends {t.page_h - g['statement_bottom']:.0f} pt from the top; colophon rule at "
              f"{t.page_h - g['colophon']['rule_y']:.0f} pt; band: {g['band']['website']['text']} · {g['band']['code']['text']}")

    c.save()
    output.parent.mkdir(parents=True, exist_ok=True)
    L.overlay_charts(base_pdf, slots, output)
    os.unlink(base_pdf)
    pf = RC.preflight(output, code, content.COVER["title"], t.catalogue, t.website)

    budget = []
    for p in pages:
        if p["words"] is None or p["kind"] in ("cover C2", "section opener"):
            budget.append({**p, "budget": None, "ok": True})
            continue
        chk = L.check_page_budget(t, p["words"], p["elements"])
        budget.append({**p, "budget": chk["budget"], "ok": chk["ok"], "over_by": chk["over_by"]})
    return {"output": str(output), "pages": len(pages), "budget": budget,
            "slots": [(s.page_index + 1, f"{s.chart_path.parent.name}/{s.chart_path.name}", round(s.scale, 4)) for s in slots],
            "presentational": PRESENTATIONAL, "glance_numbers": GLANCE_NUMBERS, "photo": str(photo),
            "photo_from_library": from_library, "code": code, "test": test, "preflight": pf,
            "catalogue_entry": {"code": code, "title": content.COVER["title"], "date": None, "tier": 1, "design": "v2",
                                "git_tag": None, "osf_path": None, "sha256": pf["sha256"], "file": output.name,
                                "test": test}}


def main() -> None:
    ap = argparse.ArgumentParser(description="v0.42 t4 wave report, Tier 1 flagship (design system v2)")
    ap.add_argument("--code", required=True, help="the report code of this render, TS-FL-v0.42-rN")
    ap.add_argument("--photo", type=Path, required=True, help="cover image: the library's print/ file (a stand-in only with --test)")
    ap.add_argument("--test", action="store_true", help="a check render, never published")
    ap.add_argument("--out-dir", type=Path, default=AIAS_ROOT / "reports" / "output")
    ap.add_argument("--chart-dir", type=Path, default=CHART_DIR)
    ap.add_argument("--report-json", type=Path, default=None)
    a = ap.parse_args()
    output = a.out_dir / RC.file_name(a.code, content.COVER["title"])
    res = build(output, a.code, a.photo, a.chart_dir, test=a.test)
    for b in res["budget"]:
        flag = "" if b["ok"] else f"  OVER BUDGET by {b.get('over_by')}"
        print(f"p{b['page']:>2} {b['kind']:<28} words={b['words']!s:>4} budget={b['budget']!s:>4} "
              f"{','.join(b['elements'])}{flag}  {b['note']}")
    print("charts:", res["slots"])
    print("wrote", res["output"], res["pages"], "pages", "(TEST render, never published)" if a.test else "")
    pf = res["preflight"]
    print("pre-flight:", "PASS" if pf["ok"] else "FAIL", pf["checks"], pf["problems"] or "")
    print("sha256:", pf["sha256"])
    if a.report_json:
        slim = dict(res)
        slim["budget"] = [{k: v for k, v in b.items() if k != "info"} for b in res["budget"]]
        a.report_json.write_text(json.dumps(slim, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


if __name__ == "__main__":
    main()
