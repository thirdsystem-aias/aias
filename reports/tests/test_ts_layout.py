"""Unit tests for reports/ts_layout.py (report design system v2).

Run from the repository root:
    python3 -m unittest discover -s reports/tests -v
"""
import io
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "reports"))

import ts_layout as L  # noqa: E402
from reportlab.pdfgen.canvas import Canvas  # noqa: E402

T = L.Tokens(ROOT)
L.register_fonts()
CHART = ROOT / "reports" / "figs" / "aias_2_0" / "report" / "report_fig_01_link_between_scores.pdf"
WORDS = ("Placeholder copy for layout tests only, with no study content in it at all. ") * 3


def _photo():
    from PIL import Image
    fd, p = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    Image.new("RGB", (1200, 800), (120, 120, 120)).save(p)
    return p


def _canvas():
    return Canvas(io.BytesIO(), pagesize=(T.page_w, T.page_h))


class TestTokens(unittest.TestCase):
    def test_versions_and_grid(self):
        self.assertEqual(T.brand["_meta"]["schema_version"], "1.6")
        self.assertEqual(T.specs["_meta"]["schema_version"], "1.2")
        self.assertEqual((T.page_w, T.page_h), (612.0, 792.0))
        self.assertEqual(T.margin, 36)
        self.assertAlmostEqual(T.col_w, 81.667, places=2)
        self.assertAlmostEqual(T.col_right(5), 484.333, places=2)

    def test_no_colour_literals_in_module(self):
        src = (ROOT / "reports" / "ts_layout.py").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"#[0-9A-Fa-f]{6}\b", src), [], "colours must come from the brand files")
        self.assertNotIn('HexColor("', src)

    def test_body_text_unchanged(self):
        body = T.style("body")
        self.assertEqual((body["size_pt"], body["leading_pt"]), (9.4, 13.2))


class TestCoverC2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p = _photo()
        cls.g = L.cover_c2(_canvas(), T, photo_path=p, kicker="Sample kicker", title="Sample title",
                           deck="Sample deck text for the cover.", byline="Sample byline")
        os.unlink(p)

    def test_photo_full_width_from_86pt_to_62_percent(self):
        ph = self.g["photo"]
        self.assertEqual((ph["x"], ph["w"]), (0, 612.0))
        self.assertAlmostEqual(ph["top_from_top"], 86.0, places=3)
        self.assertAlmostEqual(ph["bottom_from_top"], 0.62 * 792, places=3)

    def test_title_block_columns_1_to_5_and_206pt(self):
        b = self.g["block"]
        self.assertEqual(b["x0"], 0.0)
        self.assertAlmostEqual(b["x1"], T.col_right(5), places=3)
        self.assertAlmostEqual(b["h"], 206.0, places=3)

    def test_title_block_crosses_photo_bottom_edge(self):
        b, ph = self.g["block"], self.g["photo"]
        self.assertLess(b["top_from_top"], ph["bottom_from_top"])
        self.assertGreater(b["bottom_from_top"], ph["bottom_from_top"])
        # approved mock-up: 120 pt of the block hang below the photo, 86 pt sit over it
        self.assertAlmostEqual(b["below_photo"], 120.0, places=3)
        self.assertAlmostEqual(b["over_photo"], 86.0, places=3)

    def test_lockup_on_paper_above_photo(self):
        lk = self.g["lockup"]
        self.assertGreater(lk["bottom"], T.page_h - self.g["photo"]["top_from_top"])
        self.assertEqual(lk["line1"]["text"], "Third System")
        self.assertEqual(lk["line2"]["text"], "AI Presence Index")
        self.assertEqual((lk["line1"]["colour"], lk["line2"]["colour"]), ("indigo", "soft_black"))

    def test_text_inside_block_and_deck_below(self):
        b, t, d = self.g["block"], self.g["title"], self.g["deck"]
        self.assertLessEqual(t["top"], T.page_h - b["top_from_top"])
        self.assertGreaterEqual(t["bottom"], T.page_h - b["bottom_from_top"])
        self.assertLess(d["top"], T.page_h - b["bottom_from_top"])
        self.assertGreater(d["bottom"], self.g["byline_baseline"])


class TestCoverC3(unittest.TestCase):
    def test_geometry(self):
        p = _photo()
        g = L.cover_c3(_canvas(), T, photo_path=p, kicker="Sample kicker", title="Sample title",
                       deck="Sample deck.", byline="Sample byline")
        os.unlink(p)
        ph = g["photo"]
        self.assertEqual((ph["w"], ph["h"]), (540.0, 330.0))
        self.assertGreaterEqual(ph["x"], T.margin)
        self.assertLessEqual(ph["x"] + ph["w"], T.page_w - T.margin)
        self.assertEqual(ph["top_from_top"], 96)
        self.assertLess(g["title"]["top"], T.page_h - ph["bottom_from_top"])
        self.assertEqual(g["rule"]["w"], 60)
        self.assertLess(g["rule"]["y"], g["title"]["bottom"])
        self.assertGreater(g["deck"]["bottom"], g["byline_baseline"])
        self.assertGreater(g["lockup"]["bottom"], T.page_h - ph["top_from_top"])


class TestLockup(unittest.TestCase):
    def test_dark_ground_colours(self):
        lk = L.lockup(_canvas(), T, dark=True)
        self.assertEqual((lk["line1"]["colour"], lk["line2"]["colour"]), ("white", "lavender_grey"))
        self.assertTrue(lk["line1"]["font"].endswith("Bold"))
        self.assertTrue(lk["line2"]["font"].endswith("Regular"))


class TestWordBudget(unittest.TestCase):
    def test_deductions(self):
        self.assertEqual(L.word_budget(T, []), 600)
        cases = {"hero_6col": 250, "hero_6col_short": 330, "chart_4col": 420, "chart_3col": 490,
                 "number_row": 520, "section_opener": 480}
        for el, want in cases.items():
            self.assertEqual(L.word_budget(T, [el]), want, el)
        self.assertEqual(L.word_budget(T, ["section_opener", "hero_6col_short"]), 210)
        self.assertEqual(L.word_budget(T, ["chart_3col", "chart_3col"]), 380)
        with self.assertRaises(KeyError):
            L.word_budget(T, ["infographic"])

    def test_check_and_count(self):
        self.assertEqual(L.count_words("<b>Two</b> words &nbsp; · 0.95"), 3)
        r = L.check_page_budget(T, 251, ["hero_6col"])
        self.assertFalse(r["ok"])
        self.assertEqual(r["over_by"], 1)
        self.assertTrue(L.check_page_budget(T, 250, ["hero_6col"])["ok"])

    def test_chart_element_from_footprint(self):
        self.assertEqual(L.chart_element(T, 540, 216), "hero_6col_short")
        self.assertEqual(L.chart_element(T, 540, 270), "hero_6col_short")
        self.assertEqual(L.chart_element(T, 540, 346), "hero_6col")
        self.assertEqual(L.chart_element(T, T.span(1, 4), 200), "chart_4col")
        self.assertEqual(L.chart_element(T, T.span(1, 3), 200), "chart_3col")


class TestIcons(unittest.TestCase):
    def test_unapproved_icon_draws_nothing(self):
        self.assertEqual(T.pictograms["approved"], [])
        c = _canvas()
        before = len(c._code)
        for name in T.pictograms["set"]:
            self.assertFalse(L.icon(c, T, name, 100, 100, 26))
        self.assertEqual(len(c._code), before)

    def test_unknown_icon_raises(self):
        with self.assertRaises(KeyError):
            L.icon(_canvas(), T, "lightbulb", 0, 0)


class TestPages(unittest.TestCase):
    def test_finding_page_stack_has_no_overlaps(self):
        slots = []
        g = L.finding_page(_canvas(), T, label="Sample label", page_no=4, page_index=3, number=1,
                           kicker="Finding 01 · sample", headline="Sample headline", chart_path=CHART,
                           caption="Sample caption.", body=[WORDS, WORDS], slots=slots)
        self.assertGreater(g["headline_bottom"], g["rule_y"])
        self.assertLess(g["chart"]["top"], g["rule_y"])
        self.assertLess(g["caption"]["top"], g["chart"]["bottom"])
        self.assertLess(g["body"]["top"], g["caption"]["bottom"])
        self.assertGreaterEqual(g["body"]["bottom"], T.pages["finding_page"]["body"]["bottom_from_bottom_pt"] - 0.5)
        self.assertEqual(len(slots), 1)
        self.assertAlmostEqual(slots[0].w, 540.0, places=1)
        self.assertEqual(slots[0].scale, 1.0)

    def test_finding_page_overflow_raises(self):
        with self.assertRaises(L.LayoutOverflow):
            L.finding_page(_canvas(), T, label="x", page_no=1, page_index=0, number=1, kicker="k",
                           headline="h", chart_path=CHART, caption="c", body=[WORDS * 40], slots=[])

    def test_evidence_page_takes_at_most_two_3col_charts(self):
        slots = []
        L.finding_evidence_page(_canvas(), T, label="x", page_no=5, page_index=4, kicker="Evidence",
                                charts=[(CHART, "Caption one."), (CHART, "Caption two.")], body=[WORDS],
                                slots=slots)
        self.assertEqual(len(slots), 2)
        for s in slots:
            self.assertLessEqual(s.w, T.span(1, 3) + 0.01)
        self.assertLessEqual(slots[0].x + slots[0].w, slots[1].x)
        with self.assertRaises(ValueError):
            L.finding_evidence_page(_canvas(), T, label="x", page_no=5, page_index=4, kicker="E",
                                    charts=[(CHART, "a")] * 3, body=[], slots=[])

    def test_at_a_glance_never_spills(self):
        nums = [{"value": "1", "unit": "", "label": "Label", "source": "Source"}] * 3
        g = L.at_a_glance(_canvas(), T, label="x", page_no=2, standfirst="Sample standfirst.", numbers=nums,
                          measured="Sample method text.", summary=[WORDS])
        self.assertGreaterEqual(g["box"]["bottom"], T.pages["at_a_glance"]["box"]["bottom_from_bottom_pt"])
        with self.assertRaises(L.LayoutOverflow):
            L.at_a_glance(_canvas(), T, label="x", page_no=2, standfirst="Sample standfirst.", numbers=nums,
                          measured="Sample method text.", summary=[WORDS * 30])

    def test_section_opener(self):
        g = L.section_opener(_canvas(), T, part=3, title="Sample part title")
        self.assertAlmostEqual(g["part_baseline"], 0.62 * T.page_h, places=3)
        self.assertGreater(g["title"]["bottom"], T.pages["section_opener"]["numeral_baseline_from_bottom_pt"])

    def test_large_type_has_no_one_word_last_line(self):
        spec = T.style("finding_headline")
        make = lambda: [L._para(T, "Consistency is a measure of its own", spec)]
        w = L._runt_free_width(make, 410)
        _, last = L._last_line_words(make()[0], w)
        self.assertGreaterEqual(last, 2)


class TestPhotography(unittest.TestCase):
    def test_pool_and_treatment(self):
        ids = [p["id"] for p in T.photography["pool"]]
        self.assertEqual(sorted(ids), ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10",
                                       "A11", "A14", "A17", "A18"])
        self.assertEqual(sorted(p["id"] for p in T.photography["web_only"]), ["A15", "A16"])
        self.assertEqual(T.photography["treatment"]["contrast"], 1.08)
        self.assertIsNone(T.photography["treatment"]["tint"])
        for bad in ("A12", "A13", "A15", "A16"):
            with self.assertRaises(ValueError):
                L.pool_photo(T, bad)
        for road in ("A05", "A06"):
            with self.assertRaises(ValueError):
                L.pool_photo(T, road, cover="C2")
            self.assertTrue(L.pool_photo(T, road, cover="C3").name.startswith(road))

    def test_usage_record_rules(self):
        rec = T.photography["usage_record"]
        pool = [p["id"] for p in T.photography["pool"]] + [p["id"] for p in T.photography["web_only"]]
        for u in rec:
            self.assertIn(u["photo"], pool)
            if u["tier"] == 1:
                others = [v for v in rec if v is not u and v["photo"] == u["photo"]]
                self.assertEqual(others, [], "a Tier 1 photo is never reused")
        seen = set()
        for u in rec:
            if u["tier"] == 2:
                key = (u["photo"], u["recorded"][:4])
                self.assertNotIn(key, seen, "no Tier 2 photo repeated in a calendar year")
                seen.add(key)

    def test_treated_photo_is_greyscale_and_cropped(self):
        from PIL import Image
        p = _photo()
        out = L.treated_photo(T, p, 540, 330, dpi=72)
        with Image.open(out) as im:
            self.assertEqual(im.mode, "L")
            self.assertAlmostEqual(im.size[0] / im.size[1], 540 / 330, places=2)
        os.unlink(out)
        os.unlink(p)


if __name__ == "__main__":
    unittest.main()
