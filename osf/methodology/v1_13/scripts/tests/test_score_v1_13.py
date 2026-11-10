#!/usr/bin/env python3
"""Synthetic tests for score_v1_13.py (no t4 data, no network). Run:
    python3 -m unittest discover -s osf/methodology/v1_13/scripts/tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import score_v1_13 as S  # noqa: E402

C = S.load_classes()
BRAND_DOMAINS = {"Sennheiser": {"sennheiser.com"}, "Focal": {"focal.com"}, "Grado": {"gradolabs.com"}}
SUB = set().union(*BRAND_DOMAINS.values())


def rec(provider, citations, sources=None):
    return {"provider": provider, "condition": "S1", "status": "ok", "text": "x",
            "search": {"n_searches": 1, "queries": ["q"], "sources": sources or [], "citations": citations, "errors": []}}


class TestLists(unittest.TestCase):
    def test_lists_parsed(self):
        for k in ("multi_suffix", "redirect_hosts", "reference", "forum_ugc", "news", "review_editorial", "retailer"):
            self.assertIn(k, C["raw"])
        self.assertIn("vertexaisearch.cloud.google.com", C["redirect_hosts"])
        self.assertEqual(C["plain"]["bloomberg.com"], "news")
        self.assertEqual(C["plain"]["crutchfield.com"], "retailer")


class TestNormalisation(unittest.TestCase):
    def test_www_utm_fragment(self):
        s = S.resolve_source("https://www.Sennheiser.com/en-us/catalog?utm_source=openai#:~:text=x", None, C)
        self.assertEqual((s["host"], s["domain"], s["path"]), ("sennheiser.com", "sennheiser.com", "/en-us/catalog"))

    def test_multi_suffix(self):
        self.assertEqual(S.resolve_source("https://shop.whathifi.co.uk/a", None, C)["domain"], "whathifi.co.uk")
        self.assertEqual(S.resolve_source("https://en.wikipedia.org/wiki/X", None, C)["domain"], "wikipedia.org")

    def test_no_scheme_and_bad(self):
        self.assertEqual(S.resolve_source("rtings.com/headphones", None, C)["domain"], "rtings.com")
        self.assertIsNone(S.resolve_source("http://192.168.0.1/x", None, C))
        self.assertIsNone(S.resolve_source("", None, C))

    def test_google_redirect_title(self):
        u = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AbC"
        self.assertEqual(S.resolve_source(u, "rtings.com", C)["domain"], "rtings.com")
        self.assertTrue(S.resolve_source(u, "www.reddit.com", C)["via_title"])
        self.assertIsNone(S.resolve_source(u, "Best headphones of 2026", C))


class TestClassify(unittest.TestCase):
    def cls(self, url, title=None):
        return S.classify(S.resolve_source(url, title, C), C, SUB)

    def test_precedence(self):
        self.assertEqual(self.cls("https://www.sennheiser.com/"), "brand_owned")
        self.assertEqual(self.cls("https://en.wikipedia.org/wiki/Sennheiser"), "reference")
        self.assertEqual(self.cls("https://www.reddit.com/r/headphones"), "forum_ugc")
        self.assertEqual(self.cls("https://www.nytimes.com/wirecutter/reviews/x"), "review_editorial")
        self.assertEqual(self.cls("https://www.nytimes.com/2026/01/01/x.html"), "news")
        self.assertEqual(self.cls("https://www.crutchfield.com/learn/x.html"), "review_editorial")
        self.assertEqual(self.cls("https://www.crutchfield.com/p_x.html"), "retailer")
        self.assertEqual(self.cls("https://www.fda.gov/x"), "reference")
        self.assertEqual(self.cls("https://abcnews.go.com/x"), "news")
        self.assertEqual(self.cls("https://forum.example-audio.com/t/1"), "forum_ugc")
        self.assertEqual(self.cls("https://www.example-audio.com/"), "other")
        self.assertEqual(S.classify(None, C, SUB), "unresolved")

    def test_brand_social_profile_not_owned(self):
        self.assertEqual(self.cls("https://www.instagram.com/sennheiser"), "forum_ugc")


class TestBrandStats(unittest.TestCase):
    def test_g_star_and_floor(self):
        answers = []
        # 8 answers naming Sennheiser; 6 grounded; 3 of those cite sennheiser.com
        for i in range(8):
            cites = [] if i >= 6 else [{"url": "https://rtings.com/x", "title": None}]
            if i < 3:
                cites.append({"url": f"https://www.sennheiser.com/p{i}", "title": None})
            answers.append({"substrate": "v19", "named": {"Sennheiser", "Focal"},
                            "sources": S.answer_sources(rec("anthropic", cites), C, SUB)})
        st = S.brand_stats(answers, BRAND_DOMAINS)
        self.assertEqual((st["Sennheiser"]["m"], st["Sennheiser"]["g"], st["Sennheiser"]["o"]), (8, 6, 3))
        self.assertAlmostEqual(st["Sennheiser"]["G_star"], 50.0)
        self.assertTrue(st["Sennheiser"]["rated"])
        self.assertEqual(st["Focal"]["o"], 0)
        self.assertEqual(st["Grado"]["m"], 0)
        self.assertFalse(st["Grado"]["rated"])

    def test_google_duplicate_citations_dedup(self):
        u = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/A"
        srcs = S.answer_sources(rec("google", [{"url": u, "title": "focal.com"}] * 4), C, SUB)
        self.assertEqual(len(srcs), 1)
        self.assertEqual(srcs[0]["cls"], "brand_owned")

    def test_unresolved_only_is_not_grounded(self):
        a = [{"substrate": "v19", "named": {"Focal"},
              "sources": S.answer_sources(rec("google", [{"url": "https://vertexaisearch.cloud.google.com/r/x",
                                                           "title": "Some page"}]), C, SUB)}]
        self.assertEqual(S.brand_stats(a, BRAND_DOMAINS)["Focal"]["g"], 0)

    def test_source_mix(self):
        srcs = S.answer_sources(rec("openai", [{"url": "https://rtings.com/a"}, {"url": "https://reddit.com/b"}]), C, SUB)
        mix = S.source_mix([srcs])
        self.assertAlmostEqual(mix["review_editorial"], 0.5)
        self.assertAlmostEqual(mix["forum_ugc"], 0.5)


class TestStats(unittest.TestCase):
    def test_avg_ranks(self):
        self.assertEqual(S.avg_ranks([10, 20, 20, 5]), [2.0, 3.5, 3.5, 1.0])

    def test_pooled_within_rho(self):
        x = [1, 2, 3, 4, 5, 10, 20, 30, 40, 50]
        y = [2, 4, 6, 8, 10, 50, 40, 30, 20, 10]
        g = ["a"] * 5 + ["b"] * 5
        r, n = S.pooled_within_rho(x, y, g)
        self.assertEqual(n, 10)
        self.assertAlmostEqual(r, 0.0)
        r2, n2 = S.pooled_within_rho(x[:5] + [1], y[:5] + [1], g[:5] + ["c"])
        self.assertEqual(n2, 5)  # group c (1 unit) dropped
        self.assertAlmostEqual(r2, 1.0)

    def test_sep_bands(self):
        self.assertEqual(S.sep_verdict([0.10, -0.29], 40), "CONFIRMED")
        self.assertEqual(S.sep_verdict([0.10, 0.31], 40), "MARGINAL")
        self.assertEqual(S.sep_verdict([0.10, -0.50], 40), "FALSIFIED")
        self.assertEqual(S.sep_verdict([0.10, 0.10], 29), "UNDETERMINED")
        self.assertEqual(S.sep_verdict([0.10, 0.10], 40, degenerate=True), "UNDETERMINED")

    def test_reliability(self):
        self.assertAlmostEqual(S.spearman_brown_3(0.25), 0.5)
        self.assertEqual(S.reliability_verdict(0.25, 0.01, 3), "CONFIRMED")
        self.assertEqual(S.reliability_verdict(0.25, 0.20, 3), "MARGINAL")
        self.assertEqual(S.reliability_verdict(0.10, 0.01, 3), "FALSIFIED")
        self.assertEqual(S.reliability_verdict(0.40, 0.01, 1), "UNDETERMINED")

    def test_degenerate(self):
        sub = {f"b{i}": f"s{i % 5}" for i in range(20)}
        self.assertTrue(S.degenerate({b: 0.0 for b in sub}, sub))
        self.assertFalse(S.degenerate({b: float(i) for i, b in enumerate(sub)}, sub))


HTML = """<html><head>
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[
 {"@type":"Organization","name":"Sennheiser","url":"https://www.sennheiser.com",
  "sameAs":["https://www.wikidata.org/wiki/Q0000000","https://www.instagram.com/sennheiser"]},
 {"@type":["Brand"],"name":"Sennheiser"}]}</script>
<script type="application/ld+json">{ broken json </script>
</head><body><div itemscope itemtype="https://schema.org/Product"></div></body></html>"""


class TestAudit(unittest.TestCase):
    def test_extract(self):
        sd = S.extract_structured_data(HTML)
        self.assertTrue({"Organization", "Brand", "Product"} <= sd["types"])
        self.assertEqual(len(sd["same_as"]), 2)
        self.assertEqual(sd["ld_errors"], 1)

    def test_sdri(self):
        sd = S.extract_structured_data(HTML)
        ind = S.site_indicators(sd, [sd])
        self.assertEqual(ind, {"i1": 1, "i2": 1, "i3": 1, "i4": 1, "i5": 1})
        ind.update({"i6": 1, "i7": 0, "i8": 1})
        a, s, k = S.sdri(ind)
        self.assertAlmostEqual(a, 87.5)
        self.assertAlmostEqual(s, 100.0)
        self.assertAlmostEqual(k, 200.0 / 3)
        ind["i1"] = None
        self.assertEqual(S.sdri(ind)[0], None)

    def test_empty_page(self):
        sd = S.extract_structured_data("<html></html>")
        self.assertEqual(S.site_indicators(sd, [sd]), {"i1": 0, "i2": 0, "i3": 0, "i4": 0, "i5": 0})


class TestGuard(unittest.TestCase):
    def test_stage_c1_refused_without_lock(self):
        with self.assertRaises(SystemExit) as cm:
            S.main(["--stage", "C1"])
        self.assertIn("REFUSED", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
