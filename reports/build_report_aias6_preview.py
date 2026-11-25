#!/usr/bin/env python3
"""
AIAS 6.0 Preview report (Tier 1, report design system v2), managerial register (P1-P5). DRAFT BUILDER, pre-data
(branch preview-6.0-draft, Nov 25, 2026).

Forked from reports/build_report_v44_r1.py (branch v0.44-report, TS-FL-v0.44-r1): same layout module
(reports/ts_layout.py: C2 cover, at a glance, contents, intro, Indigo section openers, one finding page per finding
with its chart, scored table, limitations with the small-print Disclosures block, closing page with colophon and
Indigo band), same two-pass chart overlay, same pre-flight (report_code.preflight, small_print.check_pdf_min_size,
word budgets). What changes:
  - Text: reports/aias6_preview_report_content.py; every {{v:KEY}} is resolved by
    papers/aias_6_0_preview/tokens_aias6.py from the locked scorer's four outputs and the paper fill's own values, so
    report and paper print one outcome in the same words. Items with "requires" are kept only when the paper fill's
    flags hold (the outcome selects the findings, their titles and sentences); nothing is typed.
  - Charts: scripts/build_charts_aias6_report.py (one per finding; only those the outcome keeps).
  - SYNTHETIC mode (outputs marked synthetic_fixture or without a verified MQ_Lock): the running label starts with
    "SYNTHETIC TEST", the cover has a plain placeholder instead of a photo, every page is stamped
    (scripts/watermark_aias6.py: diagonal, header and footer lines), the file name starts with SYNTHETIC_, and the
    output folder must be outside the repository. Real mode refuses synthetic outputs; its cover is COVER in the
    content module (A04, Pablo's call 9 of Wed 2026-11-25, 7:15 am CT) unless --cover-photo names another.

Report code: REPORT_CODE in the content module (TS-SY-AIAS6.0Preview-r1, Pablo's call 5 of Wed 2026-11-25). The
catalogue entry and the cover's usage_record entry are added after the real build only.

  AIAS_ROOT=$PWD ~/aias/venv/bin/python reports/build_report_aias6_preview.py --outputs DIR --charts DIR \
      --out-dir DIR [--synthetic] [--cover-photo ID]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AIAS_ROOT") or SCRIPT_DIR.parent).resolve()
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(ROOT / "papers/aias_6_0_preview"))
sys.path.insert(0, str(ROOT / "scripts"))

import report_code as RCODE  # noqa: E402
import small_print as SP  # noqa: E402
import ts_layout as L  # noqa: E402
import tokens_aias6 as T  # noqa: E402
import aias6_values as VV  # noqa: E402
import watermark_aias6 as WM  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

_spec = importlib.util.spec_from_file_location("aias6_report_content",
                                               ROOT / "reports" / "aias6_preview_report_content.py")
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

REPORT_ID = "AIAS 6.0 Preview"
CITATION_WHERE = "osf.io/ec6wh (folder aias_6_0_preview); thirdsystem.ai"
PDF_SUBJECT = "Independent measurement for the AI mediation layer."
WATERMARK = "SYNTHETIC TEST — NOT RESULTS"
NUMBER_WORDS = ["", "One", "Two", "Three", "Four", "Five", "Six"]


class BuildError(SystemExit):
    pass


def one_text(items, what):
    """A content list of alternatives ({"requires", "text"} dicts or plain strings), filled: exactly one survives."""
    out = [x["text"] if isinstance(x, dict) else x for x in items]
    if len(out) != 1:
        raise BuildError(f"{what}: {len(out)} alternatives hold for this outcome, expected one")
    return out[0]


def texts(items):
    """A filled content list of strings and {"text"} dicts -> strings."""
    return [x["text"] if isinstance(x, dict) else x for x in items]


def placeholder_cover(w_px=3072, h_px=2048) -> str:
    """Synthetic builds only: a plain warm-grey frame instead of a photo (no image is chosen for the Preview)."""
    from PIL import Image
    fd, p = tempfile.mkstemp(suffix=".jpg", prefix="aias6_syn_cover_")
    os.close(fd)
    Image.new("RGB", (w_px, h_px), (196, 192, 186)).save(p, quality=90)
    return p


def fill_all(ctx):
    """Every content item filled for this outcome; the keys used are recorded."""
    used: set = set()
    F = {name: T.fill_content(getattr(C, name), ctx, used)
         for name in ("DECK", "STANDFIRST", "GLANCE_NUMBERS", "MEASURED", "SUMMARY", "INTRO_LEAD", "INTRO",
                      "MEASURED_HEAD", "MEASURED_PARAS", "CHARTS", "FINDINGS", "SCORED_HEAD", "SCORED_INTRO",
                      "SCORED_ROWS", "LIMITS_HEAD", "LIMITS", "NEXT_HEAD", "NEXT", "DISCLOSURES", "CLOSING_STATEMENT")}
    findings = []
    for fi in F["FINDINGS"]:
        title = fi["title"] if "title" in fi else one_text(fi["title_by_class"], "finding title")
        findings.append({"title": title, "verdict": fi["verdict"], "chart": fi["chart"], "caption": fi["caption"],
                         "body": texts(fi["body"])})
    F["FINDINGS"] = findings
    F["STANDFIRST"] = one_text(F["STANDFIRST"], "standfirst")
    F["SUMMARY"] = texts(F["SUMMARY"])
    F["CLOSING_STATEMENT"] = one_text(F["CLOSING_STATEMENT"], "closing statement")
    F["SCORED_ROWS"] = [r["row"] if isinstance(r, dict) else r for r in F["SCORED_ROWS"]]
    return F, used


def build(outputs: Path, charts: Path, out_dir: Path, synthetic: bool = False, code: str | None = None,
          cover_photo: str | None = None) -> dict:
    code = code or C.REPORT_CODE
    out_dir = Path(out_dir).resolve()
    if synthetic and str(out_dir).startswith(str(ROOT)):
        raise BuildError(f"REFUSED: a synthetic report must be written outside the repository ({out_dir})")
    if not synthetic:
        cover_photo = cover_photo or C.COVER               # call 9: the next unused A-pool image (A04)
        if not re.fullmatch(r"A\d\d", cover_photo or ""):
            raise BuildError(f"REFUSED: the Preview's cover is an A-pool image (call 9), not {cover_photo!r}")
    ctx = T.context(outputs, synthetic=synthetic)          # the paper fill's refusals apply (mode, class C, ...)
    if ctx["src"]["results"]["structure"]["wording_class"] == "C":
        raise BuildError("REFUSED: class C has no report; drafting pauses (pre-registration section 6.6)")
    F, used = fill_all(ctx)
    title_tok = T.resolve("pv.title", ctx)
    label = ("SYNTHETIC TEST · " if synthetic else "") + title_tok
    year = str(ctx["src"]["results"].get("created_utc") or "")[:4] or "n.d."

    t = L.Tokens(ROOT)
    L.register_fonts()
    SP.preflight_styles(t)
    RCODE.check_code(code, t.catalogue)
    name = RCODE.file_name(code, C.TITLE)
    if not synthetic:
        used_by = L.photo_in_use(t, cover_photo, exclude_report=REPORT_ID)
        if used_by:
            raise BuildError(f"cover photo {cover_photo} already used by {used_by}")
        photo = L.pool_photo(t, cover_photo, cover="C2")
    else:
        photo = placeholder_cover()

    findings = F["FINDINGS"]
    nf = len(findings)
    plan = ["cover", "glance", "contents", "intro", "part1"] + [f"f{i}" for i in range(1, nf + 1)] + \
           ["scored", "part2", "limits", "closing"]
    pno = {k: i + 1 for i, k in enumerate(plan)}
    part1_title = f"{NUMBER_WORDS[nf]} result{'s' if nf != 1 else ''}"

    work = Path(tempfile.mkdtemp(prefix="aias6_report_"))
    base_pdf = work / "base.pdf"
    built = work / name                                    # pre-flight runs on the canonical file name
    c = Canvas(str(base_pdf), pagesize=(t.page_w, t.page_h))
    c.setTitle(("SYNTHETIC TEST — " if synthetic else "") + f"{C.TITLE} — {title_tok}")
    c.setAuthor("Pablo Ulpiano González Castro")
    c.setSubject(RCODE.pdf_subject(code, PDF_SUBJECT))
    c.setKeywords(RCODE.pdf_keywords(code, "Third System", "AIAS 6.0 Preview", t.website))
    slots: list = []
    pages: list[dict] = []

    def done(kind, elements=(), words=None, note=""):
        pages.append({"page": len(pages) + 1, "kind": kind, "elements": list(elements), "words": words, "note": note})
        c.showPage()

    # 1 Cover (C2)
    L.cover_c2(c, t, photo_path=photo, kicker=label, title=C.TITLE, deck=F["DECK"],
               byline="Pablo Ulpiano González Castro · thirdsystem.ai", code=code)
    done("cover C2", note="placeholder (synthetic)" if synthetic else f"photo {cover_photo}")

    # 2 At a glance
    g = L.at_a_glance(c, t, label=label, page_no=pno["glance"], standfirst=F["STANDFIRST"],
                      numbers=[dict(n, icon=None) for n in F["GLANCE_NUMBERS"]], measured=F["MEASURED"],
                      summary=F["SUMMARY"], measured_heading=C.MEASURED_HEAD.upper(), icons=False)
    done("at a glance", ("number_row",), sum(g["words"].values()))

    # 3 Contents
    rows = [{"kind": "entry", "label": "", "title": "At a glance", "page": pno["glance"]},
            {"kind": "entry", "label": "", "title": "Introduction", "page": pno["intro"]},
            {"kind": "part", "label": "PART 1", "title": part1_title, "page": pno["part1"]}]
    for i, fi in enumerate(findings, start=1):
        if len(fi["title"]) >= 58:
            raise BuildError(f"finding title too long for the contents: {fi['title']}")
        rows.append({"kind": "entry", "label": f"{i:02d}", "title": fi["title"], "page": pno[f"f{i}"]})
    rows += [{"kind": "entry", "label": "", "title": F["SCORED_HEAD"], "page": pno["scored"]},
             {"kind": "part", "label": "PART 2", "title": "Limits and what's next", "page": pno["part2"]},
             {"kind": "entry", "label": "", "title": "Limitations · What's next · Disclosures", "page": pno["limits"]},
             {"kind": "entry", "label": "", "title": "About Third System", "page": pno["closing"]}]
    L.contents_page(c, t, label=label, page_no=pno["contents"], rows=rows)
    done("contents")

    # 4 Introduction
    def intro_flow():
        fl = [L.paragraph(t, p, "body", space_after=6.5) for p in F["INTRO"]]
        fl.append(L.paragraph(t, F["MEASURED_HEAD"], "subheading", space_after=4, space_before=8))
        fl += [L.paragraph(t, p, "body", space_after=6.5) for p in F["MEASURED_PARAS"]]
        return fl
    g = L.text_page(c, t, label=label, page_no=pno["intro"], kicker="INTRODUCTION", lead=F["INTRO_LEAD"],
                    sections=[{"rule": True, "flowables": intro_flow, "paras": [], "columns": 2}])
    done("intro", ("section_opener",), g["words"])

    # 5 Part 1 opener
    L.section_opener(c, t, part=1, title=part1_title, part_label="PART 1")
    done("section opener")

    # Findings: one chart each (the SYNTHETIC_ file in synthetic mode)
    for i, fi in enumerate(findings, start=1):
        chart = Path(charts) / (("SYNTHETIC_" if synthetic else "") + fi["chart"])
        if not chart.is_file():
            raise BuildError(f"missing chart {chart}")
        kicker = f"FINDING {i:02d}" + (f" · {fi['verdict']}" if fi["verdict"] else "")
        g = L.finding_page(c, t, label=label, page_no=pno[f"f{i}"], page_index=pno[f"f{i}"] - 1, number=i,
                           kicker=kicker, headline=fi["title"], chart_path=chart, caption=fi["caption"],
                           body=fi["body"], slots=slots)
        el = L.chart_element(t, g["chart"]["w"], g["chart"]["h"])
        done(f"finding {i:02d}", ("section_opener", el), g["words"]["head"] + g["words"]["body"])

    # Scored table
    rows_t = [[r[0], r[1], f"<b>{r[2]}</b>" if r[2].startswith("CONFIRMED") else r[2]] for r in F["SCORED_ROWS"]]
    tbl = lambda: [L.table_flowable(t, ["<b>#</b>", "<b>What we tested</b>", "<b>Outcome</b>"], rows_t,  # noqa: E731
                                    [36, 250, 254])]
    L.text_page(c, t, label=label, page_no=pno["scored"],
                sections=[{"heading": F["SCORED_HEAD"], "paras": [], "columns": 1,
                           "flowables": lambda: [L.paragraph(t, F["SCORED_INTRO"], "body", space_after=10)] + tbl()}])
    done("scored table")

    # Part 2 opener
    L.section_opener(c, t, part=2, title="Limits and what's next", part_label="PART 2")
    done("section opener")

    # Limitations, What's next, Disclosures (small print at the foot)
    L.running_chrome(c, t, label, pno["limits"])
    tp = t.pages["text_page"]
    fb = SP.foot_blocks(c, t, disclosures=F["DISCLOSURES"])
    bottom = fb["body_bottom"]
    y = t.y(tp["heading_top_from_top_pt"])
    colw = (t.content_w - tp["gutter_pt"]) / 2
    xs = [t.margin, t.margin + colw + tp["gutter_pt"]]
    for head, paras in ((F["LIMITS_HEAD"], F["LIMITS"]), (F["NEXT_HEAD"], F["NEXT"])):
        y = L._block(c, lambda h=head: [L._para(t, h, t.style("finding_headline"))], t.margin, y, t.content_w,
                     bottom, "heading", runt=True) - 12
        res = L._columns(c, lambda ps=paras: L._body_paras(t, ps), y, bottom, xs, colw, head)
        y = res["bottom"] - 22
    done("limitations, what's next, disclosures")

    # Closing
    cp = L.colophon_paragraphs(t)
    CLOSING = t.pages["closing_page"]
    gap = CLOSING["colophon_block_gap_pt"]
    cite = RCODE.cite(f"González Castro, P. U. ({year}).", f"{C.TITLE}: {title_tok}", code, CITATION_WHERE)
    about = ("Third System is an independent research entity that measures how AI answers represent brands. It does "
             "not accept compensation contingent on improving a brand's AI Availability Score or securing favorable "
             "AI recommendations.")
    meth = (f"Pre-registered synthesis, locked at git tag {T.resolve('pv.prereg_tag', ctx)} and deposited on OSF "
            "before any score on the newest models existed. Every result number and outcome word in this report is "
            "read from the locked scorer's outputs (results, gates, inputs and profile files), through the same "
            "values as the academic paper, which gives every test in full.")
    data = ("Plan, scorer, outputs and deviations record: OSF ec6wh, folder aias_6_0_preview; the brand-level profile "
            "(one row per brand, every part side by side) is deposited there. Code: github.com/thirdsystem-aias/aias.")
    left = lambda: [cp("About Third System", "head"), cp(about, after=gap), cp("Authored by", "head"),  # noqa: E731
                    cp("Pablo Ulpiano González Castro"),
                    cp("School of Visual Arts, MPS Branding Program, New York (primary academic affiliation)"),
                    cp("Citation", "head", before=gap - CLOSING["colophon_space_after_pt"]), cp(cite, after=0)]
    credit = ("Synthetic test build: no cover image." if synthetic else "Cover image: licensed photograph.")
    right = lambda: [cp("Methodology", "head"), cp(meth, after=gap), cp("Underlying data", "head"),  # noqa: E731
                     cp(data), cp(credit, before=gap - CLOSING["colophon_space_after_pt"]),
                     cp("<b>Inquiries:</b> hello@thirdsystem.ai", after=0)]
    L.closing_page(c, t, label=label, page_no=pno["closing"], statement=F["CLOSING_STATEMENT"], left=left,
                   right=right, code=code)
    done("closing")

    c.save()
    L.overlay_charts(str(base_pdf), slots, built)
    pf = RCODE.preflight(built, code, C.TITLE, t.catalogue, t.website)
    sizes = SP.check_pdf_min_size(built)
    budget = []
    for p in pages:
        if p["words"] is None:
            budget.append({**p, "budget": None, "ok": True})
            continue
        chk = L.check_page_budget(t, p["words"], p["elements"])
        budget.append({**p, "budget": chk["budget"], "ok": chk["ok"]})
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / (("SYNTHETIC_" if synthetic else "") + name)
    if synthetic:
        WM.stamp(built, final, WATERMARK)
        os.unlink(photo)
    else:
        built.replace(final)
    for p in work.iterdir():
        p.unlink()
    work.rmdir()
    return {"output": str(final), "pages": len(pages), "plan": plan, "budget": budget, "preflight": pf,
            "min_size": sizes, "value_keys": sorted(used), "synthetic": synthetic}


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS 6.0 Preview report (draft builder)")
    ap.add_argument("--outputs", type=Path, default=VV.OUTDIR)
    ap.add_argument("--charts", type=Path, default=ROOT / "reports/figs/aias6/report")
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--code", default=None)
    ap.add_argument("--cover-photo", default=None)
    a = ap.parse_args(argv)
    res = build(a.outputs, a.charts, a.out_dir, a.synthetic, a.code, a.cover_photo)
    for b in res["budget"]:
        print(f"p{b['page']:>2} {b['kind']:<40} words={b['words']!s:>4} budget={b['budget']!s:>4} "
              f"{'' if b['ok'] else 'OVER'}")
    print("pre-flight:", "PASS" if res["preflight"]["ok"] else "FAIL", res["preflight"]["problems"] or "")
    print("min text size:", res["min_size"])
    print("value keys:", len(res["value_keys"]))
    out = Path(res["output"])
    (out.parent / (out.stem + "_value_keys.json")).write_text(json.dumps(res["value_keys"], indent=1) + "\n")
    print("wrote", res["output"], res["pages"], "pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
