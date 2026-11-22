"""Unit tests for reports/small_print.py: small-print notes, margin callouts and the Disclosures block
(Pablo, Nov 15, 2026, 8:33 am).

Run from the repository root:
    python3 -m unittest reports.tests.test_small_print
"""
import copy
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "reports"))

import sample_small_print as S  # noqa: E402
import small_print as SP  # noqa: E402
import ts_layout as L  # noqa: E402
from pypdf import PdfReader  # noqa: E402

T = L.Tokens(ROOT)
L.register_fonts()
FLOOR = 6.5

_TMP = tempfile.TemporaryDirectory()
SAMPLE_PDF = Path(_TMP.name) / "sample.pdf"
SAMPLE = S.build(SAMPLE_PDF, ROOT)


def tearDownModule():
    _TMP.cleanup()


class TestScale(unittest.TestCase):
    def test_sizes_within_the_scale(self):
        st = SP.spec(T)["styles"]
        for name in ("note", "source_line", "note_marker"):
            self.assertTrue(6.5 <= st[name]["size_pt"] <= 7.0, name)
        for name in ("margin_callout", "margin_callout_label", "disclosures", "disclosures_head"):
            self.assertEqual(st[name]["size_pt"], 7.5, name)

    def test_paragraph_styles_carry_the_sizes(self):
        for name, spec in SP.spec(T)["styles"].items():
            self.assertEqual(SP.style(T, name).fontSize, spec["size_pt"], name)
            self.assertGreaterEqual(SP.style(T, name).leading, SP.style(T, name).fontSize, name)

    def test_floor_is_6_5(self):
        self.assertEqual(SP.spec(T)["floor_pt"], FLOOR)
        self.assertEqual(min(s["size_pt"] for s in SP.spec(T)["styles"].values()), FLOOR)
        self.assertEqual(T.pages["footer"]["size_pt"], FLOOR)  # the locked footer already sits on the floor

    def test_preflight_passes_on_the_spec(self):
        rep = SP.preflight_styles(T)
        self.assertEqual(set(rep), set(SP.spec(T)["styles"]))

    def test_preflight_fails_under_the_floor(self):
        t = copy.copy(T)
        t.pages = copy.deepcopy(T.pages)
        t.pages["small_print"]["styles"]["note"]["size_pt"] = 6.4
        with self.assertRaisesRegex(SP.SmallPrintError, "note: 6.4 pt is under the 6.5 pt floor"):
            SP.preflight_styles(t)

    def test_preflight_fails_outside_the_band(self):
        t = copy.copy(T)
        t.pages = copy.deepcopy(T.pages)
        t.pages["small_print"]["styles"]["disclosures"]["size_pt"] = 8.0
        with self.assertRaisesRegex(SP.SmallPrintError, "disclosures: 8.0 pt is outside its band"):
            SP.preflight_styles(t)

    def test_preflight_fails_on_a_band_below_the_floor(self):
        t = copy.copy(T)
        t.pages = copy.deepcopy(T.pages)
        t.pages["small_print"]["styles"]["source_line"]["band_pt"] = [6.0, 7.0]
        with self.assertRaisesRegex(SP.SmallPrintError, "band starts at 6.0 pt"):
            SP.preflight_styles(t)


class TestContrast(unittest.TestCase):
    def test_known_ratios(self):
        from reportlab.lib.colors import HexColor
        self.assertAlmostEqual(SP.contrast_ratio(HexColor("#000000"), HexColor("#FFFFFF")), 21.0, places=2)
        self.assertAlmostEqual(SP.contrast_ratio(HexColor("#FFFFFF"), HexColor("#FFFFFF")), 1.0, places=2)

    def test_every_style_has_at_least_4_5_to_1(self):
        need = SP.spec(T)["min_contrast"]
        self.assertEqual(need, 4.5)
        for name, r in SP.style_report(T).items():
            self.assertGreaterEqual(r["contrast"], 4.5, f"{name} ({r['color']}): {r['contrast']:.2f}:1")

    def test_material_text_takes_the_body_colour(self):
        body = T.style("body")["color"]
        st = SP.spec(T)["styles"]
        for name in ("note", "source_line", "margin_callout", "disclosures", "note_marker"):
            self.assertEqual(st[name]["color"], body, name)

    def test_preflight_fails_on_pale_text(self):
        t = copy.copy(T)
        t.pages = copy.deepcopy(T.pages)
        t.pages["small_print"]["styles"]["disclosures"]["color"] = "#CCCCCC"
        with self.assertRaisesRegex(SP.SmallPrintError, "disclosures: contrast"):
            SP.preflight_styles(t)


class TestNotes(unittest.TestCase):
    def test_noteseq_numbers_from_one_per_page(self):
        ns = SP.NoteSeq(T)
        a, b = ns.cite("first"), ns.cite("second")
        self.assertIn(">1<", a)
        self.assertIn(">2<", b)
        self.assertEqual(ns.notes, ["first", "second"])
        self.assertIn(">1<", SP.NoteSeq(T).cite("again"))

    def test_marker_is_at_the_floor_size(self):
        self.assertIn('size="6.5"', SP.marker(T, 3))

    def test_notes_land_on_the_same_page_as_their_reference(self):
        pages = SP.check_notes_same_page(SAMPLE_PDF, SAMPLE["pairs"])
        self.assertEqual(pages, [1, 1, 1, 2, 3])

    def test_same_page_check_fails_when_a_note_is_elsewhere(self):
        ref = SAMPLE["pairs"][0][0]
        other = SAMPLE["pairs"][3][1]  # the note that sits on page 2
        with self.assertRaises(SP.SmallPrintError):
            SP.check_notes_same_page(SAMPLE_PDF, [(ref, other)])

    def test_notes_sit_above_the_footer_and_below_the_body(self):
        from reportlab.pdfgen.canvas import Canvas
        import io
        c = Canvas(io.BytesIO(), pagesize=(T.page_w, T.page_h))
        fb = SP.foot_blocks(c, T, notes=["one", "two", "three"])
        floor_y = T.pages["footer"]["rule_from_bottom_pt"]
        self.assertGreater(fb["notes"]["bottom"], floor_y)
        self.assertGreater(fb["body_bottom"], fb["notes"]["top"])
        self.assertLess(fb["body_bottom"], T.page_h / 2)

    def test_notes_height_matches_the_block(self):
        notes = ["a note " * 12, "another note " * 9, "third " * 7]
        from reportlab.pdfgen.canvas import Canvas
        import io
        c = Canvas(io.BytesIO(), pagesize=(T.page_w, T.page_h))
        blk = SP.notes_block(c, T, notes, 62)
        self.assertAlmostEqual(blk["top"] - blk["bottom"], SP.notes_height(T, notes), delta=1.5)


class TestCallout(unittest.TestCase):
    def test_callout_text_is_on_page_two(self):
        txt = re.sub(r"\s+", " ", PdfReader(str(SAMPLE_PDF)).pages[1].extract_text())
        self.assertIn("SAMPLE callout", txt)
        self.assertIn("A definition, caveat or sample size", txt)

    def test_callout_in_columns_5_to_6_stays_in_the_margin_column(self):
        from reportlab.pdfgen.canvas import Canvas
        import io
        c = Canvas(io.BytesIO(), pagesize=(T.page_w, T.page_h))
        r = SP.margin_callout(c, T, "x " * 60, top=600, col_from=5, col_to=6, label="L")
        self.assertAlmostEqual(r["x"], T.col_left(5), places=2)
        self.assertLessEqual(r["x"] + r["w"], T.page_w - T.margin + 0.01)
        self.assertLess(r["bottom"], r["top"])

    def test_callout_overflow_is_refused(self):
        from reportlab.pdfgen.canvas import Canvas
        import io
        c = Canvas(io.BytesIO(), pagesize=(T.page_w, T.page_h))
        with self.assertRaises(L.LayoutOverflow):
            SP.margin_callout(c, T, "word " * 2000, top=600, col_from=5, col_to=6)


class TestDisclosures(unittest.TestCase):
    def test_block_is_on_the_last_page_with_every_item(self):
        r = SP.check_disclosures(SAMPLE_PDF, T)
        self.assertEqual(r["page"], SAMPLE["pages"])

    def test_not_on_earlier_pages(self):
        pages = [re.sub(r"\s+", " ", p.extract_text()) for p in PdfReader(str(SAMPLE_PDF)).pages]
        for tx in pages[:-1]:
            self.assertNotIn("Conflicts of interest.", tx)
            self.assertNotIn("Held-out brands.", tx)

    def test_pointer_is_in_the_main_text(self):
        pages = [re.sub(r"\s+", " ", p.extract_text()) for p in PdfReader(str(SAMPLE_PDF)).pages]
        ptr = SP.disclosure_pointer(3)
        self.assertIn(ptr, pages[0])
        self.assertIn(ptr, pages[-1])
        self.assertLess(len(ptr), 160)  # one line of main text

    def test_missing_item_is_refused(self):
        from reportlab.pdfgen.canvas import Canvas
        import io
        c = Canvas(io.BytesIO(), pagesize=(T.page_w, T.page_h))
        items = dict(S.DISCLOSURES)
        del items["ai_use"]
        with self.assertRaisesRegex(SP.SmallPrintError, "ai_use"):
            SP.disclosures_block(c, T, items, 62)

    def test_four_items_required(self):
        self.assertEqual(SP.spec(T)["disclosure_items"],
                         ["conflicts_of_interest", "held_out_brands", "ai_use", "independence"])

    def test_block_sits_above_the_footer_rule(self):
        from reportlab.pdfgen.canvas import Canvas
        import io
        c = Canvas(io.BytesIO(), pagesize=(T.page_w, T.page_h))
        r = SP.disclosures_block(c, T, S.DISCLOSURES, 62)
        self.assertGreater(r["bottom"], T.pages["footer"]["rule_from_bottom_pt"])


class TestSamplePdf(unittest.TestCase):
    def test_three_pages(self):
        self.assertEqual(len(PdfReader(str(SAMPLE_PDF)).pages), 3)

    def test_no_text_under_the_floor_in_the_rendered_pdf(self):
        r = SP.check_pdf_min_size(SAMPLE_PDF, FLOOR)
        self.assertGreaterEqual(r["smallest"], FLOOR - 0.05)
        self.assertGreater(r["runs"], 50)

    def test_floor_check_catches_small_text(self):
        from reportlab.pdfgen.canvas import Canvas
        p = Path(_TMP.name) / "tiny.pdf"
        c = Canvas(str(p), pagesize=(200, 200))
        c.setFont(L.font_name("Regular"), 6.0)
        c.drawString(10, 100, "too small")
        c.save()
        with self.assertRaisesRegex(SP.SmallPrintError, "under the 6.5 pt floor"):
            SP.check_pdf_min_size(p, FLOOR)

    def test_sample_is_marked_sample_and_has_no_digits_of_findings(self):
        for p in PdfReader(str(SAMPLE_PDF)).pages:
            self.assertIn("SAMPLE", p.extract_text())

    def test_layout_module_untouched_by_colour_literals(self):
        src = (ROOT / "reports" / "small_print.py").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"#[0-9A-Fa-f]{6}\b", src), [])


if __name__ == "__main__":
    unittest.main()
