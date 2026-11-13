"""Unit tests for reports/report_code.py and the report-code pieces of reports/ts_layout.py
(decisions 13 and 14, Pablo, Nov 13, 2026).

Run from the repository root:
    python3 -m unittest discover -s reports/tests -v
"""
import io
import os
import re
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "reports"))

import report_code as RC  # noqa: E402
import ts_layout as L  # noqa: E402
from pypdf import PdfReader  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

T = L.Tokens(ROOT)
L.register_fonts()
ENTRIES = T.catalogue
SITE = T.website
R3_SHA = "3a4849de8274431e52c49c9a3571916e7ac4b2d3f3db21fda75ae256cb6316cb"  # AIAS 2.0 report r3 as published


def _entry(code):
    return next(e for e in ENTRIES if e["code"] == code)


def _pdf_text(draw, meta=None):
    """Draw one page with draw(c), save to memory and return (text of the page, reader)."""
    buf = io.BytesIO()
    c = Canvas(buf, pagesize=(T.page_w, T.page_h))
    for k, v in (meta or {}).items():
        getattr(c, k)(v)
    draw(c)
    c.showPage()
    c.save()
    r = PdfReader(io.BytesIO(buf.getvalue()))
    return re.sub(r"\s+", " ", r.pages[0].extract_text() or ""), r


def _colophon():
    p = L.colophon_paragraphs(T)
    left = lambda: [p("About Third System", "head"), p("Sample colophon text for the layout test."),
                    p("Citation", "head"), p(RC.cite("Author, A. (2026).", "Sample Title", "TS-FL-v0.40-r1",
                                                    "ThirdSystem.ai/studies/sample"))]
    right = lambda: [p("Inquiries", "head"), p("hello@thirdsystem.ai", after=0)]
    return left, right


class TestFormat(unittest.TestCase):
    def test_spec_examples_parse(self):
        for code, kind, study, rev in [("TS-FL-v0.40-r1", "FL", "v0.40", 1), ("TS-SY-AIAS2.0-r4", "SY", "AIAS2.0", 4),
                                       ("TS-CS-v0.22-r1", "CS", "v0.22", 1), ("TS-BR-v0.44-r1", "BR", "v0.44", 1),
                                       ("TS-DG-ACME01-r1", "DG", "ACME01", 1), ("TS-CS-v1.9-r12", "CS", "v1.9", 12)]:
            p = RC.parse_code(code)
            self.assertEqual((p["type"], p["study"], p["rev"]), (kind, study, rev), code)
            self.assertEqual(RC.make_code(kind, study, rev), code)

    def test_malformed_codes_refused(self):
        for bad in ["TS-XX-v0.22-r1", "TS-CS-v0.22-r0", "TS-CS-v0.22", "ts-cs-v0.22-r1", "TS-CS-v0-22-r1",
                    "TS-CS-v0.22-R1", "TS-CS--r1", "TS-CS-v0.22-r1 ", "TS-CS-v0.22-r01", "CS-v0.22-r1", "", None]:
            with self.assertRaises(RC.ReportCodeError, msg=repr(bad)):
                RC.parse_code(bad)

    def test_types_match_the_register(self):
        self.assertEqual(set(RC.TYPES), set(T.specs["report_catalogue"]["types"]))
        self.assertEqual(T.specs["report_catalogue"]["format"], "TS-{TYPE}-{STUDY}-{REV}")


class TestFileName(unittest.TestCase):
    def test_code_then_title_slug(self):
        self.assertEqual(RC.file_name("TS-SY-AIAS2.0-r4", "How Often, and How Evenly"),
                         "TS-SY-AIAS2.0-r4_how-often-and-how-evenly.pdf")
        self.assertEqual(RC.file_name("TS-CS-v0.22-r1", "Phantom Brand Persistence Has a Living-Brand Boundary"),
                         "TS-CS-v0.22-r1_phantom-brand-persistence-has-a-living-brand-boundary.pdf")

    def test_slug_is_plain_ascii(self):
        self.assertEqual(RC.title_slug("What AI Share-of-Voice Doesn’t Capture"), "what-ai-share-of-voice-doesnt-capture")
        self.assertEqual(RC.title_slug("AIAS™ 2.0 · González & <i>Co</i>"), "aias-2-0-gonzalez-and-co")
        long = RC.title_slug("word " * 40)
        self.assertLessEqual(len(long), 60)
        self.assertFalse(long.endswith("-"))

    def test_bad_input_refused(self):
        with self.assertRaises(RC.ReportCodeError):
            RC.file_name("TS-SY-AIAS2.0-r4", "™ · !")
        with self.assertRaises(RC.ReportCodeError):
            RC.file_name("not-a-code", "Title")


class TestRegister(unittest.TestCase):
    def test_register_is_sound(self):
        self.assertEqual(RC.validate_catalogue(ENTRIES), [])
        self.assertGreater(len(ENTRIES), 40)

    def test_revisions_run_from_r1_without_gaps_and_one_is_current(self):
        by_study = defaultdict(list)
        for e in ENTRIES:
            p = RC.parse_code(e["code"])
            self.assertEqual((e["type"], e["study"], e["rev"]), (p["type"], p["study"], f"r{p['rev']}"))
            by_study[p["study"]].append(e)
        for study, es in by_study.items():
            revs = sorted(RC.parse_code(e["code"])["rev"] for e in es)
            self.assertEqual(revs, list(range(1, len(revs) + 1)), study)
            self.assertEqual([e["status"] for e in es].count("current"), 1, study)

    def test_held_studies_never_on_the_website(self):
        held = sorted(e["study"] for e in ENTRIES if e["held"])
        self.assertEqual(held, ["v0.38", "v0.39"])
        for e in ENTRIES:
            if e["held"]:
                self.assertIsNone(e["website"])
                self.assertTrue(e["osf_path"])

    def test_aias_2_0_r3_backfilled(self):
        e = _entry("TS-SY-AIAS2.0-r3")
        self.assertEqual(e["sha256"], R3_SHA)
        self.assertEqual(e["git_tag"], "aias-2-0-report-locked-r3")
        self.assertEqual(e["osf_path"], "aias_2_0/report_r3/aias_2_0_synthesis_report_r3.pdf")
        self.assertEqual(e["tier"], 1)
        self.assertEqual(RC.next_revision("AIAS2.0", ENTRIES), 4)


class TestUniqueness(unittest.TestCase):
    def test_registered_code_refused_for_another_pdf(self):
        with self.assertRaises(RC.ReportCodeError):
            RC.check_code("TS-SY-AIAS2.0-r3", ENTRIES)  # a new render of a published code
        with self.assertRaises(RC.ReportCodeError):
            RC.check_code("TS-SY-AIAS2.0-r3", ENTRIES, sha256="0" * 64)
        self.assertEqual(RC.check_code("TS-SY-AIAS2.0-r3", ENTRIES, sha256=R3_SHA)["rev"], 3)

    def test_website_variant_is_the_same_pdf(self):
        e = _entry("TS-CS-v0.27-r1")
        self.assertNotEqual(e["website"]["sha256"], e["sha256"])
        RC.check_code("TS-CS-v0.27-r1", ENTRIES, sha256=e["website"]["sha256"])

    def test_new_code_is_the_next_revision(self):
        RC.check_code("TS-SY-AIAS2.0-r4", ENTRIES)
        RC.check_code("TS-FL-v0.40-r1", ENTRIES)
        for bad in ("TS-SY-AIAS2.0-r5", "TS-FL-v0.40-r2", "TS-CS-v0.22-r1"):
            with self.assertRaises(RC.ReportCodeError, msg=bad):
                RC.check_code(bad, ENTRIES)

    def test_a_registered_pdf_takes_no_second_code(self):
        with self.assertRaises(RC.ReportCodeError):
            RC.check_code("TS-SY-AIAS2.0-r4", ENTRIES, sha256=R3_SHA)

    def test_validator_catches_duplicates(self):
        e = dict(_entry("TS-CS-v0.22-r1"))
        self.assertTrue(any("used twice" in p for p in RC.validate_catalogue([e, dict(e)])))
        twin = dict(e, code="TS-CS-v0.22-r2", rev="r2")
        self.assertTrue(any("same PDF" in p for p in RC.validate_catalogue([e, twin])))
        self.assertTrue(any("Tier" in p for p in RC.validate_catalogue([dict(e, tier=1)])))


class TestWebsiteLowerCase(unittest.TestCase):
    def test_caps_keep_the_website_lower_case(self):
        self.assertEqual(SITE, "thirdsystem.ai")
        self.assertEqual(RC.upper_keep_website("Pablo Ulpiano González Castro · thirdsystem.ai", SITE),
                         "PABLO ULPIANO GONZÁLEZ CASTRO · thirdsystem.ai")
        self.assertEqual(RC.upper_keep_website("Write to Hello@ThirdSystem.ai today", SITE),
                         "WRITE TO hello@thirdsystem.ai TODAY")
        self.assertEqual(RC.website_lower("See THIRDSYSTEM.AI/Methodology.", SITE), "See thirdsystem.ai/methodology.")
        self.assertEqual(RC.upper_keep_website("At a glance", SITE), "AT A GLANCE")

    def test_footer_and_cover_byline_print_it_lower_case(self):
        self.assertIn("thirdsystem.ai", T.footer_text)
        text, _ = _pdf_text(lambda c: L.running_chrome(c, T, "Label with thirdsystem.ai", 3))
        self.assertIn("thirdsystem.ai/methodology", text)
        self.assertIn("LABEL WITH thirdsystem.ai", text)
        self.assertNotRegex(text, r"THIRDSYSTEM\.AI")
        from PIL import Image
        fd, photo = tempfile.mkstemp(suffix=".jpg")
        os.close(fd)
        Image.new("RGB", (900, 600), (120, 120, 120)).save(photo)
        try:
            text, _ = _pdf_text(lambda c: L.cover_c2(c, T, photo_path=photo, kicker="Kicker", title="Sample title",
                                                    deck="Sample deck.", byline="Sample Author · thirdsystem.ai"))
        finally:
            os.unlink(photo)
        self.assertIn("SAMPLE AUTHOR · thirdsystem.ai", text)
        self.assertNotRegex(text, r"THIRDSYSTEM\.AI")


class TestClosingBand(unittest.TestCase):
    def test_band_line_wordmark_website_code_page(self):
        left, right = _colophon()
        res = {}

        def draw(c):
            res.update(L.closing_page(c, T, label="Sample label", page_no=14, statement="A closing statement.",
                                      left=left, right=right, code="TS-SY-AIAS2.0-r4"))
        text, _ = _pdf_text(draw)
        b = res["band"]
        cp = T.pages["closing_page"]
        self.assertEqual(b["top"], cp["band_height_pt"])
        self.assertEqual(b["top"], 96)
        self.assertEqual(b["wordmark_size"], T.covers["lockup"]["line1"]["size_pt"])
        self.assertAlmostEqual(b["website"]["x"], b["wordmark_right"] + 1.5 * b["wordmark_size"], places=3)
        self.assertGreater(b["code"]["x"], b["website"]["x"] + b["website"]["w"])
        self.assertEqual(b["website"]["text"], "thirdsystem.ai")
        self.assertIn("thirdsystem.ai · TS-SY-AIAS2.0-r4", text)  # printed exactly as registered
        self.assertIn("thirdsystem.ai/studies/sample", text)            # colophon: website lower case
        self.assertIn("(Report TS-FL-v0.40-r1)", text)                   # citation carries the code
        self.assertNotRegex(text, r"THIRDSYSTEM\.AI|ThirdSystem\.ai")
        self.assertNotIn("© 2026", text)  # the band replaces the footer line on this page
        self.assertLess(res["colophon"]["rule_y"], res["statement_bottom"])
        self.assertGreater(res["colophon"]["bottom"], b["top"])

    def test_band_refuses_a_malformed_code(self):
        left, right = _colophon()
        with self.assertRaises(RC.ReportCodeError):
            L.closing_page(Canvas(io.BytesIO()), T, label="x", page_no=1, statement="s", left=left, right=right,
                           code="TS-SY-AIAS2.0")


class TestLastPageFooter(unittest.TestCase):
    def test_tier_2_3_last_page_footer_line(self):
        self.assertEqual(L.last_page_footer(T, "TS-CS-v0.22-r1"), "thirdsystem.ai · TS-CS-v0.22-r1")
        text, _ = _pdf_text(lambda c: L.text_page(c, T, label="Sample label", page_no=12, code="TS-CS-v0.22-r1",
                                                  sections=[{"heading": "Sample", "paras": ["Body text."], "columns": 1}]))
        self.assertIn("thirdsystem.ai · TS-CS-v0.22-r1", text)
        self.assertNotIn("Findings may be cited", text)
        text, _ = _pdf_text(lambda c: L.text_page(c, T, label="Sample label", page_no=11,
                                                  sections=[{"heading": "Sample", "paras": ["Body text."], "columns": 1}]))
        self.assertIn("Findings may be cited with attribution", text)
        with self.assertRaises(RC.ReportCodeError):
            L.last_page_footer(T, "TS-CS-v0.22")


class TestMetadataAndPreflight(unittest.TestCase):
    CODE, TITLE = "TS-FL-v0.40-r1", "Sample Flagship Title"

    def _render(self, folder, name=None, subject=True, band_site=None):
        left, right = _colophon()
        path = Path(folder) / (name or RC.file_name(self.CODE, self.TITLE))
        c = Canvas(str(path), pagesize=(T.page_w, T.page_h))
        if subject:
            c.setSubject(RC.pdf_subject(self.CODE, "Independent measurement for the AI mediation layer."))
            c.setKeywords(RC.pdf_keywords(self.CODE, "Third System", SITE))
        L.running_chrome(c, T, "Sample label", 1)
        if band_site:
            c.drawString(100, 400, band_site)
        c.showPage()
        L.closing_page(c, T, label="Sample label", page_no=2, statement="A closing statement.", left=left,
                       right=right, code=self.CODE)
        c.showPage()
        c.save()
        return path

    def test_subject_and_keywords_carry_the_code(self):
        self.assertTrue(RC.pdf_subject(self.CODE, "Subject line.").startswith(self.CODE))
        self.assertEqual(RC.pdf_keywords(self.CODE, "Third System", self.CODE).split(", "), [self.CODE, "Third System"])
        with tempfile.TemporaryDirectory() as d:
            meta = PdfReader(str(self._render(d))).metadata
            self.assertIn(self.CODE, meta["/Subject"])
            self.assertIn(self.CODE, meta["/Keywords"])

    def test_preflight_passes_and_catches_each_fault(self):
        with tempfile.TemporaryDirectory() as d:
            ok = RC.preflight(self._render(d), self.CODE, self.TITLE, ENTRIES, SITE)
            self.assertTrue(ok["ok"], ok)
            bad = RC.preflight(self._render(d, name="v40_report.pdf"), self.CODE, self.TITLE, ENTRIES, SITE)
            self.assertFalse(bad["checks"]["file_name"])
            bad = RC.preflight(self._render(d, subject=False), self.CODE, self.TITLE, ENTRIES, SITE)
            self.assertFalse(bad["checks"]["metadata_subject"])
            self.assertFalse(bad["checks"]["metadata_keywords"])
            bad = RC.preflight(self._render(d, band_site="THIRDSYSTEM.AI"), self.CODE, self.TITLE, ENTRIES, SITE)
            self.assertFalse(bad["checks"]["website_lower_case_throughout"])
            used = [dict(_entry("TS-CS-v0.22-r1"), code=self.CODE, study="v0.40", type="FL", tier=1)]
            bad = RC.preflight(self._render(d), self.CODE, self.TITLE, used, SITE)
            self.assertFalse(bad["checks"]["register"])  # the code is already in use for another PDF
            self.assertFalse(RC.preflight(self._render(d), "TS-FL-v0.40-r1", "Other Title", ENTRIES, SITE)["checks"]["file_name"])


if __name__ == "__main__":
    unittest.main()
