#!/usr/bin/env python3
"""Tests for audit_v1_13.py: the 8 SDRI indicators, SDRI arithmetic, page selection, robots, rate, redirects,
the QID rule, the no-network guard and the --collect refusal. Synthetic inputs only (hosts under .test);
nothing is fetched. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/scripts/tests -v
"""
import json
import socket
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audit_v1_13 as A  # noqa: E402
import score_v1_13 as S  # noqa: E402

MS = S.load_classes()["multi_suffix"]
P31_WORDS, DESC_WORDS = A.load_type_words()


def sd(html):
    return A.extract_structured_data(html)


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj)}</script>'


ORG_HOME = "<html><head>" + ld({"@context": "https://schema.org", "@type": "Organization", "name": "X",
                                "sameAs": ["https://www.wikidata.org/wiki/Q00001"]}) + "</head></html>"
EMPTY = "<html><body><p>nothing</p></body></html>"


class TestSiteIndicators(unittest.TestCase):
    """Indicators (1)-(5): each with a case that sets it and a case that does not."""

    def ind(self, home_html, *other_html):
        home = sd(home_html)
        return A.site_indicators(home, [home] + [sd(h) for h in other_html])

    def test_i1_organization_on_home_page(self):
        self.assertEqual(self.ind(ORG_HOME)["i1"], 1)
        self.assertEqual(self.ind("<html>" + ld({"@type": "Corporation"}) + "</html>")["i1"], 1)    # subtype
        self.assertEqual(self.ind(EMPTY, ORG_HOME)["i1"], 0)        # Organization only on another page
        self.assertEqual(self.ind('<div itemscope itemtype="https://schema.org/Organization"></div>')["i1"], 1)

    def test_i2_brand_on_any_page(self):
        prod = "<html>" + ld({"@type": "Product", "brand": {"@type": "Brand", "name": "X"}}) + "</html>"
        self.assertEqual(self.ind(EMPTY, prod)["i2"], 1)            # nested Brand on P3
        self.assertEqual(self.ind(EMPTY, "<html>" + ld({"@type": ["Brand"]}) + "</html>")["i2"], 1)
        self.assertEqual(self.ind(ORG_HOME)["i2"], 0)

    def test_i3_product_or_subtype(self):
        self.assertEqual(self.ind(EMPTY, "<html>" + ld({"@type": "Car"}) + "</html>")["i3"], 1)
        self.assertEqual(self.ind('<div itemscope itemtype="http://schema.org/Product"></div>')["i3"], 1)
        self.assertEqual(self.ind(EMPTY, '<div vocab="https://schema.org/" typeof="ProductModel"></div>')["i3"], 1)
        self.assertEqual(self.ind(ORG_HOME)["i3"], 0)

    def test_i4_same_as_on_organization_or_brand(self):
        self.assertEqual(self.ind(ORG_HOME)["i4"], 1)
        on_product = "<html>" + ld({"@type": "Product", "sameAs": "https://www.wikidata.org/wiki/Q00002"}) + "</html>"
        self.assertEqual(self.ind(on_product)["i4"], 0)             # sameAs on a Product node does not count
        micro = ('<div itemscope itemtype="https://schema.org/Organization">'
                 '<link itemprop="sameAs" href="https://www.instagram.com/x"></div>')
        self.assertEqual(self.ind(micro)["i4"], 1)
        outside = ('<div itemscope itemtype="https://schema.org/Organization"></div>'
                   '<link itemprop="sameAs" href="https://www.instagram.com/x">')
        self.assertEqual(self.ind(outside)["i4"], 0)                # outside the Organization scope

    def test_i5_same_as_to_wikidata_or_wikipedia(self):
        self.assertEqual(self.ind(ORG_HOME)["i5"], 1)
        wp = "<html>" + ld({"@type": "Brand", "sameAs": ["https://en.wikipedia.org/wiki/X"]}) + "</html>"
        self.assertEqual(self.ind(EMPTY, wp)["i5"], 1)
        insta = "<html>" + ld({"@type": "Organization", "sameAs": "https://www.instagram.com/x"}) + "</html>"
        self.assertEqual(self.ind(insta)["i5"], 0)
        trick = "<html>" + ld({"@type": "Organization", "sameAs": "https://x.test/?ref=wikidata.org"}) + "</html>"
        self.assertEqual(self.ind(trick)["i5"], 0)                  # host-based, not a substring test

    def test_broken_json_ld_contributes_nothing(self):
        d = sd('<script type="application/ld+json">{ "@type": "Organization", broken </script>')
        self.assertEqual((d["ld_errors"], d["types"]), (1, set()))

    def test_empty_page(self):
        self.assertEqual(self.ind(EMPTY), {"i1": 0, "i2": 0, "i3": 0, "i4": 0, "i5": 0})


class TestKgIndicators(unittest.TestCase):
    """Indicators (6)-(8)."""
    D_B = {"brand-x.test"}

    def kg(self, **k):
        return A.kg_indicators(dict({"status": "chosen", "qid": "Q00001", "p856": [], "sitelinks": []}, **k),
                               self.D_B, MS)

    def test_i6_item_exists(self):
        self.assertEqual(self.kg()["i6"], 1)
        self.assertEqual(A.kg_indicators({"status": "none", "qid": None}, self.D_B, MS), {"i6": 0, "i7": 0, "i8": 0})

    def test_i7_official_website_in_d_b(self):
        self.assertEqual(self.kg(p856=["https://www.brand-x.test/en-us"])["i7"], 1)
        self.assertEqual(self.kg(p856=["https://brand-x-group.test/"])["i7"], 0)
        self.assertEqual(self.kg(p856=[])["i7"], 0)

    def test_i8_enwiki_sitelink(self):
        self.assertEqual(self.kg(sitelinks=["dewiki", "enwiki"])["i8"], 1)
        self.assertEqual(self.kg(sitelinks=["frwiki"])["i8"], 0)

    def test_error_not_rated(self):
        self.assertEqual(A.kg_indicators({"status": "error"}, self.D_B, MS), {"i6": None, "i7": None, "i8": None})


class TestSdri(unittest.TestCase):
    def test_arithmetic(self):
        ind = {"i1": 1, "i2": 1, "i3": 1, "i4": 1, "i5": 1, "i6": 1, "i7": 0, "i8": 1}
        a, s, k = A.sdri(ind)
        self.assertAlmostEqual(a, 87.5)
        self.assertAlmostEqual(s, 100.0)
        self.assertAlmostEqual(k, 200.0 / 3)
        ind["i1"] = None                       # P1 not fetched: SDRI_site and SDRI NOT RATED, SDRI_kg kept
        self.assertEqual(A.sdri(ind)[:2], (None, None))
        self.assertAlmostEqual(A.sdri(ind)[2], 200.0 / 3)

    def test_tie_needs_adjudication(self):
        rec = {"substrate": "v22", "brand_id": "X", "site": None,
               "kg": {"status": "tie", "tied": ["Q00004", "Q00005"], "tied_p856": {"Q00004": []},
                      "tied_sitelinks": {"Q00004": ["enwiki"]}}}
        with self.assertRaises(ValueError):
            A.indicators_of(rec, None, MS, set())
        with self.assertRaises(ValueError):
            A.indicators_of(rec, "Q00009", MS, set())
        self.assertEqual(A.indicators_of(rec, "Q00004", MS, set())["i8"], 1)
        self.assertEqual(A.indicators_of(rec, "none", MS, set())["i6"], 0)


class TestPageSelection(unittest.TestCase):
    def test_pick_links(self):
        links = ["#top", "mailto:a@x.test", "/us/login", "https://other.test/about", "/us/account/history",
                 "/us/about-us", "/us/company/history", "/us/cart", "/us/products/hd-1", "/us/shop-all"]
        p2, p3 = A.pick_links(links, "https://www.brand-x.test/us/", MS)
        self.assertEqual(p2, "https://www.brand-x.test/us/about-us")
        self.assertEqual(p3, "https://www.brand-x.test/us/products/hd-1")

    def test_same_site_subdomain_and_missing(self):
        p2, p3 = A.pick_links(["https://shop.brand-x.test/collections/a"], "https://brand-x.test/", MS)
        self.assertEqual((p2, p3), (None, "https://shop.brand-x.test/collections/a"))
        self.assertEqual(A.pick_links([], "https://brand-x.test/", MS), (None, None))

    def test_path_matches(self):
        self.assertTrue(A.path_matches("/en/About-Us/", A.ABOUT_TOKENS))
        self.assertTrue(A.path_matches("/history.html", A.ABOUT_TOKENS))
        self.assertFalse(A.path_matches("/aboutface", A.ABOUT_TOKENS))
        self.assertTrue(A.path_matches("/whisky/single-malt", A.PRODUCT_TOKENS))


class FakeFetcher:
    def __init__(self, responses):
        self.r, self.calls = responses, []

    def get(self, url):
        self.calls.append(url)
        spec = self.r.get(url, (404, {}, b""))
        if isinstance(spec, str):
            return A.Response(None, {}, b"", spec)
        st, h, b = spec
        return A.Response(st, h, b)


def ctx_with(responses):
    return A.Ctx(FakeFetcher(responses), A.SimClock(datetime(2026, 11, 14, tzinfo=timezone.utc)), MS)


HTML = {"content-type": "text/html; charset=utf-8"}


class TestFetchRules(unittest.TestCase):
    def test_user_agent(self):
        self.assertEqual(A.USER_AGENT, "AIAS research crawler; https://thirdsystem.ai")
        self.assertNotIn("@", A.USER_AGENT)
        self.assertEqual((A.MAX_PAGES, A.HOST_GAP_S, A.MAX_REDIRECTS), (3, 10.0, 5))

    def test_robots(self):
        ctx = ctx_with({"https://a.test/robots.txt": (200, {}, b"User-agent: *\nDisallow: /private/\n"),
                        "https://b.test/robots.txt": (404, {}, b""),
                        "https://c.test/robots.txt": (503, {}, b"")})
        self.assertEqual(A.robots_decision("https://a.test/private/x", ctx), "robots_disallowed")
        self.assertEqual(A.robots_decision("https://a.test/ok", ctx), "allowed")
        self.assertEqual(A.robots_decision("https://b.test/anything", ctx), "allowed")
        self.assertEqual(A.robots_decision("https://c.test/", ctx), "robots_unavailable")
        self.assertEqual(ctx.fetcher.calls.count("https://a.test/robots.txt"), 1)          # once per host
        self.assertEqual(ctx.fetcher.calls.count("https://c.test/robots.txt"), 2)          # one retry on 5xx
        page = A.fetch_page("https://c.test/", ctx)
        self.assertEqual(page["outcome"], "robots_unavailable")
        self.assertNotIn("https://c.test/", ctx.fetcher.calls)                             # never requested

    def test_rate_limits(self):
        ctx = ctx_with({"https://a.test/robots.txt": (404, {}, b""), "https://a.test/": (200, HTML, b"<html></html>"),
                        "https://a.test/x": (200, HTML, b"<html></html>"), "https://b.test/robots.txt": (404, {}, b"")})
        A.fetch_page("https://a.test/", ctx)
        A.fetch_page("https://b.test/", ctx)
        A.fetch_page("https://a.test/x", ctx)
        per, glob = ctx.limiter.min_gaps()
        self.assertGreaterEqual(per["a.test"], 10.0)
        self.assertGreaterEqual(glob, 1.0)

    def test_redirect_cap_and_blocked(self):
        r = {"https://a.test/robots.txt": (404, {}, b"")}
        for i in range(7):
            r[f"https://a.test/r{i}"] = (302, {"location": f"/r{i + 1}"}, b"")
        r["https://a.test/blocked"] = (429, {}, b"")
        ctx = ctx_with(r)
        page = A.fetch_page("https://a.test/r0", ctx)
        self.assertEqual(page["outcome"], "too_many_redirects")
        self.assertEqual(len(page["chain"]), 6)
        self.assertEqual(A.fetch_page("https://a.test/blocked", ctx)["outcome"], "blocked")

    def test_retry_once_then_error(self):
        ctx = ctx_with({"https://a.test/robots.txt": (404, {}, b""), "https://a.test/": "timeout"})
        self.assertEqual(A.fetch_page("https://a.test/", ctx)["outcome"], "error")
        self.assertEqual(ctx.fetcher.calls.count("https://a.test/"), 2)

    def test_non_html_not_parsed(self):
        ctx = ctx_with({"https://a.test/robots.txt": (404, {}, b""),
                        "https://a.test/": (200, {"content-type": "application/pdf"}, b"%PDF")})
        self.assertEqual(A.fetch_page("https://a.test/", ctx)["outcome"], "not_html")


class TestQidRule(unittest.TestCase):
    def ents(self, **e):
        return {q: {"claims": {p: [{"mainsnak": {"datavalue": {"value": ({"id": v} if p == "P31" else v)}}}
                                   for v in vals] for p, vals in d.get("claims", {}).items()},
                    "sitelinks": {s: {} for s in d.get("sitelinks", [])},
                    "descriptions": {"en": {"value": d.get("description", "")}}} for q, d in e.items()}

    def choose(self, search, ents, labels, d_b=("brand-x.test",), sub="v19"):
        return A.choose_qid("Brand X", sub, set(d_b), search, ents, labels, P31_WORDS, DESC_WORDS, MS)

    def test_p856_preferred(self):
        e = self.ents(Q01={"claims": {"P31": ["Q10"], "P856": ["https://www.brand-x.test/"]}},
                      Q02={"claims": {"P31": ["Q10"]}, "sitelinks": ["enwiki"], "description": "headphone maker"})
        r = self.choose([{"id": "Q01", "label": "Brand X"}, {"id": "Q02", "label": "brand x"}], e, {"Q10": "brand"})
        self.assertEqual((r["status"], r["qid"], r["rule"]), ("chosen", "Q01", "p856_in_D_b"))

    def test_description_fallback_tie_none_and_type_filter(self):
        e = self.ents(Q01={"claims": {"P31": ["Q10"]}, "sitelinks": ["enwiki"], "description": "audio company"},
                      Q02={"claims": {"P31": ["Q11"]}, "sitelinks": ["enwiki"], "description": "audio engineer"})
        lab = {"Q10": "audio equipment manufacturer", "Q11": "human"}
        search = [{"id": "Q01", "label": "Brand X"}, {"id": "Q02", "label": "Brand X"}]
        self.assertEqual(self.choose(search, e, lab)["qid"], "Q01")          # Q02 fails the P31 filter
        lab2 = dict(lab, Q11="business")
        self.assertEqual(self.choose(search, e, lab2)["status"], "tie")
        self.assertEqual(self.choose(search, e, lab, sub="v22")["status"], "none")   # no category word for cars
        self.assertEqual(self.choose([{"id": "Q03", "label": "Brand Y"}], e, lab)["status"], "none")


class TestNoNetworkAndGuards(unittest.TestCase):
    def test_no_network_blocks_connections(self):
        with A.no_network() as attempts:
            s = socket.socket()
            try:
                with self.assertRaises(RuntimeError):
                    s.connect(("127.0.0.1", 9))
                with self.assertRaises(RuntimeError):
                    socket.getaddrinfo("fixture.test", 443)
            finally:
                s.close()
        self.assertEqual(len(attempts), 2)

    def test_dry_run_passes_without_network(self):
        self.assertEqual(A.dry_run(record_path=None), 0)

    def test_collect_refused_before_any_network(self):
        calls = []
        real = A._git

        def spy(args):
            calls.append(args[0])
            return real(args)
        A._git = spy
        try:
            with self.assertRaises(SystemExit) as cm:
                A.collect_guard(datetime(2026, 11, 13, tzinfo=timezone.utc))
        finally:
            A._git = real
        self.assertIn("REFUSED", str(cm.exception))
        self.assertNotIn("ls-remote", calls)
        with self.assertRaises(SystemExit) as cm:
            A.collect_guard(datetime(2026, 11, 18, tzinfo=timezone.utc))
        self.assertIn("blackout", str(cm.exception))

    def test_units_refuse_unresolved(self):
        import tempfile
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = Path(tmp.name) / "dom.csv"
        p.write_text("substrate,brand_id,brand,coder_key,status,domain,aliases,source,ambiguity,runner_decision\n"
                     "v19,A,A,A,RESOLVED,brand-a.test,,s,,\nv19,B,B,B,UNRESOLVED,,,s,,\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            A.units_from_domains(p)
        p.write_text("substrate,brand_id,brand,coder_key,status,domain,aliases,source,ambiguity,runner_decision\n"
                     "v19,A,A,A,RESOLVED,brand-a.test,,s,,\nv22,D.1,P,P,NONE,,,s,,runner\n", encoding="utf-8")
        units = {(u["substrate"], u["brand_id"]): u for u in A.units_from_domains(p)}
        self.assertEqual(units[("v19", "A")]["primary_domain"], "brand-a.test")
        self.assertTrue(units[("v22", "D.1")]["phantom"])
        self.assertIsNone(units[("v22", "D.1")]["primary_domain"])


if __name__ == "__main__":
    unittest.main()
