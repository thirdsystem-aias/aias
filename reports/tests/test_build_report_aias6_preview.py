"""Tests of the AIAS 6.0 Preview report builder (reports/build_report_aias6_preview.py) and its chart builder
(scripts/build_charts_aias6_report.py). SYNTHETIC DATA ONLY: the scenario of the inputs as they stood on Nov 25,
2026 (papers/aias_6_0_preview/synthetic/SYNTHETIC_nov25_inputs/) and the paper pipeline's fixtures. Every PDF is
written to a temporary folder outside the repository and deleted.

    AIAS_ROOT=$PWD ~/aias/venv/bin/python -m unittest reports.tests.test_build_report_aias6_preview -v
"""
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PAPER = ROOT / "papers/aias_6_0_preview"
SYN = PAPER / "synthetic"
SCEN = SYN / "SYNTHETIC_nov25_inputs"
FIX = PAPER / "tests/fixtures"
for p in (ROOT / "reports", ROOT / "scripts", PAPER, PAPER / "tests"):
    sys.path.insert(0, str(p))

import build_report_aias6_preview as B  # noqa: E402
import build_charts_aias6_report as CH  # noqa: E402
import tokens_aias6 as T  # noqa: E402
import aias6_values as VV  # noqa: E402
import make_scenarios_aias6 as MS  # noqa: E402

WM = "SYNTHETIC TEST — NOT RESULTS"
_TMP = tempfile.TemporaryDirectory(prefix="aias6_report_test_")
TMP = Path(_TMP.name)
BUILT = {}


def build(scenario_dir, tag):
    """charts + report for one synthetic scenario (cached per test run)."""
    if tag not in BUILT:
        charts = TMP / tag / "charts"
        made = CH.build(scenario_dir, charts, WM)
        res = B.build(scenario_dir, charts, TMP / tag / "report", synthetic=True)
        BUILT[tag] = (made, res)
    return BUILT[tag]


def pdf_text(path):
    return [p.extract_text() or "" for p in PdfReader(str(path)).pages]


class TestScenario(unittest.TestCase):
    """The Nov 25 scenario: what it covers, and that it cannot be mistaken for results."""

    def setUp(self):
        self.src = VV.load_sources(SCEN)
        self.res = self.src["results"]

    def test_stored_under_synthetic_and_labelled(self):
        self.assertEqual(SCEN.parent.name, "synthetic")
        self.assertTrue(SCEN.name.startswith("SYNTHETIC_"))
        for k in ("results", "gates", "inputs"):
            self.assertIn("SYNTHETIC TEST DATA - NOT RESULTS", self.src[k]["synthetic_fixture"])
        self.assertTrue(VV.is_synthetic(self.src))
        self.assertNotIn("SYNTHETIC_nov25_inputs", MS.SCENARIOS)        # never mixed into the paper fixtures
        self.assertFalse((FIX / "SYNTHETIC_nov25_inputs").exists())
        self.assertTrue((SYN / "README.md").is_file())

    def test_inputs_as_of_nov25(self):
        self.assertEqual(self.res["gate_states"], {"R": "MARGINAL", "S": "NOT_RUN", "Cov": "PASS", "G": "MARGINAL"})
        self.assertEqual(self.res["K"], ["P", "C", "Cov"])
        self.assertEqual(self.res["structure"]["wording_class"], "A_k")
        pairs = {tuple(t["pair"]) for t in self.res["structure"]["descriptive_marginal_pairs"].values()}
        self.assertTrue({("P", "R"), ("P", "G")} <= pairs)                # both parts under review shown below

    def test_real_mode_refuses_the_scenario(self):
        with self.assertRaises(Exception):
            T.context(SCEN, synthetic=False)


class TestTokenFill(unittest.TestCase):
    def test_every_key_resolves_on_the_scenario(self):
        ctx = T.context(SCEN, synthetic=True)
        for k, spec in T.TOKEN_MAP.items():
            when = spec[3] if len(spec) > 3 else None
            if when is None or ctx["flags"][when]:
                self.assertTrue(T.resolve(k, ctx), k)

    def test_fill_leaves_no_token_in_any_fixture(self):
        for s in list(MS.SCENARIOS) + ["SYNTHETIC_nov25_inputs"]:
            d = SCEN if s.startswith("SYNTHETIC_") else FIX / s
            ctx = T.context(d, synthetic=True)
            if ctx["src"]["results"]["structure"]["wording_class"] == "C":
                continue                                               # no report for class C (refusal tested)
            F, used = B.fill_all(ctx)
            text = json.dumps(F, ensure_ascii=False)
            self.assertNotIn("{{", text, s)
            self.assertNotIn("{%", text, s)
            self.assertTrue(used <= set(T.TOKEN_MAP), s)
            self.assertEqual(len(F["GLANCE_NUMBERS"]), 3, s)              # ts_layout.number_row takes three
            for fi in F["FINDINGS"]:
                self.assertLess(len(fi["title"]), 58, f"{s}: {fi['title']}")
                self.assertIn(fi["chart"], F["CHARTS"], s)
                self.assertIsNotNone(F["CHARTS"][fi["chart"]], s)


class TestCharts(unittest.TestCase):
    def test_one_chart_per_finding_all_labelled_synthetic(self):
        made, res = build(SCEN, "nov25")
        self.assertEqual(len(made), 5)
        for name, path in made.items():
            self.assertTrue(path.name.startswith("SYNTHETIC_"), path)
            text = " ".join(pdf_text(path))
            self.assertIn("SYNTHETIC TEST DATA", text, name)
            self.assertIn("provisional", text, name)

    def test_chart_titles_are_the_content_titles(self):
        made, _ = build(SCEN, "nov25")
        ctx = T.context(SCEN, synthetic=True)
        charts = T.fill_content(B.C.CHARTS, ctx)
        for name, path in made.items():
            flat = re.sub(r"\s+", " ", " ".join(pdf_text(path)))
            self.assertIn(charts[name]["title"], flat, name)

    def test_refusals(self):
        with self.assertRaises(SystemExit):                            # synthetic without the watermark
            CH.build(SCEN, TMP / "nowm", None)
        with self.assertRaises(SystemExit):                            # synthetic charts inside the repository
            CH.build(SCEN, ROOT / "reports/figs/aias6/report_synthetic_test", WM)
        self.assertFalse((ROOT / "reports/figs/aias6/report_synthetic_test").exists())


class TestReport(unittest.TestCase):
    def test_page_count_stable(self):
        _, res = build(SCEN, "nov25")
        self.assertEqual(res["pages"], 14)                             # 9 fixed pages + 5 findings
        self.assertEqual(len(PdfReader(res["output"]).pages), 14)
        self.assertEqual(res["plan"][:5], ["cover", "glance", "contents", "intro", "part1"])

    def test_no_unfilled_token_and_synthetic_on_every_page(self):
        _, res = build(SCEN, "nov25")
        self.assertTrue(Path(res["output"]).name.startswith("SYNTHETIC_"))
        for i, page in enumerate(pdf_text(res["output"]), start=1):
            self.assertNotIn("{{", page, f"p{i}")
            self.assertNotIn("{%", page, f"p{i}")
            self.assertIn("SYNTHETIC TEST", page, f"p{i}")

    def test_preflight_and_budgets(self):
        _, res = build(SCEN, "nov25")
        self.assertTrue(res["preflight"]["ok"], res["preflight"]["problems"])
        self.assertGreaterEqual(res["min_size"]["smallest"], 6.5)
        self.assertEqual([b["page"] for b in res["budget"] if not b["ok"]], [])

    def test_register_rules_in_the_pdf(self):
        _, res = build(SCEN, "nov25")
        text = " ".join(pdf_text(res["output"]))
        flat = re.sub(r"\s+", " ", text)
        for word in ("Samsung", "Harman", "Cheil", "v0.38", "v0.39"):
            self.assertNotIn(word, flat)
        self.assertIn("used AI tools (Anthropic's Claude) to assist with study design, analysis and writing", flat)
        self.assertIn("Ranking and Grounding are under review", flat)   # the section 6.6 headline, A_k

    def test_no_structure_outcome_builds_with_one_finding(self):
        ctx = T.context(FIX / "reduced_panel", synthetic=True)
        self.assertFalse(ctx["flags"]["STRUCT"])                       # section 4.3: no structure test
        _, res = build(FIX / "reduced_panel", "reduced_panel")
        self.assertEqual(res["pages"], 10)                             # 9 fixed pages + finding 03 only
        self.assertEqual(len(PdfReader(res["output"]).pages), 10)

    def test_every_fixture_outcome_builds(self):
        """Every outcome the paper fixtures cover (classes A, A_k, B, U; no structure test) lays out: page count is
        9 fixed pages plus one per kept finding, the pre-flight passes, no token is left."""
        for s in MS.SCENARIOS:
            ctx = T.context(FIX / s, synthetic=True)
            if ctx["src"]["results"]["structure"]["wording_class"] == "C":
                continue
            nf = len(B.fill_all(ctx)[0]["FINDINGS"])
            _, res = build(FIX / s, s)
            self.assertEqual(res["pages"], 9 + nf, s)
            pages = pdf_text(res["output"])
            self.assertEqual(len(pages), 9 + nf, s)
            self.assertTrue(res["preflight"]["ok"], (s, res["preflight"]["problems"]))
            self.assertFalse(any("{{" in p for p in pages), s)
            self.assertTrue(all("SYNTHETIC TEST" in p for p in pages), s)

    def test_refusals(self):
        made, _ = build(SCEN, "nov25")
        charts = Path(next(iter(made.values()))).parent
        with self.assertRaises(SystemExit):                            # synthetic report inside the repository
            B.build(SCEN, charts, ROOT / "reports/output_synthetic_test", synthetic=True)
        self.assertFalse((ROOT / "reports/output_synthetic_test").exists())
        with self.assertRaises(SystemExit):                            # the cover is an A-pool image (call 9)
            B.build(SCEN, charts, TMP / "real", synthetic=False, cover_photo="v0.40_airlines")
        with self.assertRaises(Exception):                             # synthetic outputs in real mode (cover A04)
            B.build(SCEN, charts, TMP / "real", synthetic=False)
        with self.assertRaises(Exception):                             # synthetic outputs in real mode
            B.build(SCEN, charts, TMP / "real", synthetic=False, cover_photo="A18")
        with self.assertRaises(SystemExit):                            # class C: no report
            B.build(FIX / "six_falsified", charts, TMP / "c", synthetic=True)


class TestPreviewCalls(unittest.TestCase):
    """Pablo's nine Preview calls (control panel, Wed 2026-11-25, 7:15 am CT, "Ok to all", as drafted)."""

    def test_code_title_cover(self):                                   # calls 5, 6, 9
        self.assertEqual(B.C.REPORT_CODE, "TS-SY-AIAS6.0Preview-r1")
        self.assertEqual(B.C.TITLE, "All the Parts at Once")
        self.assertEqual(B.C.COVER, "A04")
        import ts_layout as L
        t = L.Tokens(ROOT)
        pool = [p["id"] for p in t.photography["pool"]]
        self.assertIn("A04", pool)
        self.assertNotIn("A04", [u["photo"] for u in t.photography["usage_record"]])
        self.assertFalse(L.photo_in_use(t, "A04", exclude_report=B.REPORT_ID))
        self.assertTrue(L.pool_photo(t, "A04", cover="C2").name.startswith("A04"))
        # every pool id before A04 in pool order has been used (website category pages, Nov 11-12, 2026)
        replaced = {u.get("replaces") for u in t.photography["usage_record"]}
        self.assertTrue({"A01", "A02", "A03"} <= replaced)

    def test_sentiment_fallback_pending_and_ranking_within_presence(self):   # calls 1, 2, 3
        ctx = T.context(SCEN, synthetic=True)
        self.assertTrue(ctx["flags"]["W2"])
        self.assertTrue(ctx["flags"]["S_FALLBACK_PENDING"])
        F, _ = B.fill_all(ctx)
        body = " ".join(" ".join(f["body"]) for f in F["FINDINGS"])
        self.assertIn("The planned fallback, Sentiment on the older model panel, is pending", body)
        self.assertIn("the published score reports Ranking as part of Presence", body)
        self.assertIn("pending: v1.11 issued no verdict file", ctx["paper"]["W2_SENTENCE"])
        self.assertIn("The published score reports Ranking as part of Presence (v1.16).", ctx["paper"]["RANK_ABSTRACT"])

    def test_paper_text_on_the_scenario(self):                         # calls 1, 2, 4
        import fill_paper_aias6 as FP
        md, _, _, _ = FP.fill(SCEN, synthetic=True, class_c_draft=True)
        flat = re.sub(r"\s+", " ", md)
        self.assertIn("Exploratory note, dated November 25, 2026 (outside the locked plan)", flat)
        self.assertIn("v1.20 (a re-scoring of v1.11's judge replies) and v1.21", flat)
        self.assertIn("(sensitivity SG), is pending: v1.11 issued no verdict file", flat)
        self.assertIn("SG Sentiment, legacy panel | -- | pending: v1.11 issued no verdict file", flat)
        self.assertIn("Are the Six Parts of AI Availability Separate Readings of a Brand?", flat)
        self.assertIn("A Pre-Registered Structure Test of Six Provisional Components on the Newest Models", flat)


if __name__ == "__main__":
    unittest.main(verbosity=1)
