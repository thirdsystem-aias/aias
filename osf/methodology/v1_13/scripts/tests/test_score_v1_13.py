#!/usr/bin/env python3
"""Synthetic tests for score_v1_13.py (no t4 data, no network; every brand and domain below is synthetic,
under the reserved .test top-level domain). Run:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s osf/methodology/v1_13/scripts/tests -v
"""
import csv
import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import score_v1_13 as S  # noqa: E402

C = S.load_classes()
DOM = {("v19", "BrandA"): "brand-a.test", ("v19", "BrandB"): "brand-b.test", ("v19", "BrandC"): "brand-c.test"}
SUB = set(DOM.values())
G_REDIRECT = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/"


def units_from(dom, extra=None):
    u = {k: {"substrate": k[0], "brand_id": k[1], "brand": k[1], "coder_key": k[1], "status": "RESOLVED",
             "domains": {d}} for k, d in dom.items()}
    u.update(extra or {})
    return u


def rec(provider, sources=None, citations=None, model="claude-fable-5-2", call_id="c1", run=1, sub="v19", text="x"):
    return {"call_id": call_id, "substrate": sub, "phase": "B", "probe_id": "q1", "condition": "S1", "run": run,
            "provider": provider, "model_requested": model, "served_model": model, "status": "ok", "text": text,
            "error": None, "search": {"n_searches": 1, "queries": ["q"], "sources": sources or [],
                                      "citations": citations or [], "errors": []}}


class TestLists(unittest.TestCase):
    def test_lists_parsed(self):
        for k in ("multi_suffix", "redirect_hosts", "reference", "forum_ugc", "news", "review_editorial", "retailer"):
            self.assertIn(k, C["raw"])
        self.assertIn("vertexaisearch.cloud.google.com", C["redirect_hosts"])
        self.assertEqual(C["plain"]["bloomberg.com"], "news")
        self.assertEqual(C["plain"]["crutchfield.com"], "retailer")


class TestNormalisation(unittest.TestCase):
    def test_www_utm_fragment(self):
        s = S.resolve_source("https://www.Brand-A.test/en-us/catalog?utm_source=openai#:~:text=x", None, C)
        self.assertEqual((s["host"], s["domain"], s["path"]), ("brand-a.test", "brand-a.test", "/en-us/catalog"))

    def test_multi_suffix(self):
        self.assertEqual(S.resolve_source("https://shop.whathifi.co.uk/a", None, C)["domain"], "whathifi.co.uk")
        self.assertEqual(S.resolve_source("https://en.wikipedia.org/wiki/X", None, C)["domain"], "wikipedia.org")

    def test_no_scheme_and_bad(self):
        self.assertEqual(S.resolve_source("rtings.com/headphones", None, C)["domain"], "rtings.com")
        self.assertIsNone(S.resolve_source("http://192.168.0.1/x", None, C))
        self.assertIsNone(S.resolve_source("", None, C))
        self.assertIsNone(S.resolve_source(None, None, C))

    def test_google_redirect_title(self):
        u = G_REDIRECT + "AbC"
        self.assertEqual(S.resolve_source(u, "rtings.com", C)["domain"], "rtings.com")
        self.assertTrue(S.resolve_source(u, "www.reddit.com", C)["via_title"])
        self.assertIsNone(S.resolve_source(u, "Best headphones of 2026", C))


class TestClassify(unittest.TestCase):
    def cls(self, url, title=None, all_db=None):
        return S.classify(S.resolve_source(url, title, C), C, SUB, all_db)

    def test_precedence(self):
        self.assertEqual(self.cls("https://www.brand-a.test/"), "brand_owned")
        self.assertEqual(self.cls("https://en.wikipedia.org/wiki/BrandA"), "reference")
        self.assertEqual(self.cls("https://www.reddit.com/r/headphones"), "forum_ugc")
        self.assertEqual(self.cls("https://www.nytimes.com/wirecutter/reviews/x"), "review_editorial")
        self.assertEqual(self.cls("https://www.nytimes.com/2026/01/01/x.html"), "news")
        self.assertEqual(self.cls("https://www.crutchfield.com/learn/x.html"), "review_editorial")
        self.assertEqual(self.cls("https://www.crutchfield.com/p_x.html"), "retailer")
        self.assertEqual(self.cls("https://www.fda.gov/x"), "reference")
        self.assertEqual(self.cls("https://abcnews.go.com/x"), "news")
        self.assertEqual(self.cls("https://forum.example-audio.test/t/1"), "forum_ugc")
        self.assertEqual(self.cls("https://www.example-audio.test/"), "other")
        self.assertEqual(S.classify(None, C, SUB), "unresolved")

    def test_brand_social_profile_not_owned(self):
        self.assertEqual(self.cls("https://www.instagram.com/branda"), "forum_ugc")

    def test_shop_host_rule_uses_every_d_b(self):
        self.assertEqual(self.cls("https://shop.other-maker.test/x"), "retailer")
        self.assertEqual(self.cls("https://shop.other-maker.test/x", all_db=SUB | {"other-maker.test"}), "other")


class TestDomainList(unittest.TestCase):
    def write(self, rows):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        p = Path(tmp.name) / "dom.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["substrate", "brand_id", "brand", "coder_key", "status", "domain", "aliases", "source",
                        "ambiguity", "runner_decision"])
            w.writerows(rows)
        return p

    def test_statuses(self):
        p = self.write([["v19", "BrandA", "BrandA", "BrandA", "RESOLVED", "brand-a.test", "brand-a-usa.test", "s", "", ""],
                        ["v19", "BrandB", "BrandB", "BrandB", "UNRESOLVED", "", "", "s", "", ""],
                        ["v19", "BrandC", "BrandC", "BrandC", "NONE", "", "", "s", "", "runner: none"]])
        u = S.load_brand_domains(p)
        self.assertEqual(u[("v19", "BrandA")]["domains"], {"brand-a.test", "brand-a-usa.test"})
        self.assertEqual(S.unresolved_units(u), [("v19", "BrandB")])
        self.assertEqual(u[("v19", "BrandC")]["domains"], set())

    def test_bad_rows(self):
        with self.assertRaises(ValueError):
            S.load_brand_domains(self.write([["v19", "A", "A", "A", "RESOLVED", "", "", "s", "", ""]]))
        with self.assertRaises(ValueError):
            S.load_brand_domains(self.write([["v19", "A", "A", "A", "MAYBE", "", "", "s", "", ""]]))
        with self.assertRaises(ValueError):
            S.load_brand_domains(self.write([["v19", "A", "A", "A", "NONE", "", "", "s", "", ""]] * 2))

    def test_frozen_list_shape(self):
        """The real list: 112 units, every RESOLVED row with a domain and a source (holds after the runner's
        decisions too)."""
        u = S.load_brand_domains()
        self.assertEqual(len(u), 112)
        self.assertEqual({s: sum(1 for k in u if k[0] == s) for s in S.SUBSTRATES},
                         {"v19": 16, "v20": 24, "v21": 24, "v22": 24, "v23": 24})
        self.assertIn(S.DENON, u)
        for r in S.read_csv(S.DOMAINS_CSV):
            if r["status"] == "RESOLVED":
                self.assertTrue(r["domain"].strip() and r["source"].strip(), r["brand"])
        for key, dom in ((("v20", "C.6"), "cetaphil.com"), (("v20", "B.7"), "augustinusbader.com")):
            if u[key]["status"] == "RESOLVED":
                self.assertIn(dom, u[key]["domains"])


class TestRecords(unittest.TestCase):
    def test_served_ok(self):
        self.assertTrue(S.served_ok("gpt-6-astra", "gpt-6-astra"))
        self.assertTrue(S.served_ok("gpt-6-astra", "gpt-6-astra-2026-10-01"))
        self.assertTrue(S.served_ok("gemini-4-argon", "models/gemini-4-argon"))
        self.assertFalse(S.served_ok("gpt-6-astra", "gpt-6-astra-mini"))
        self.assertFalse(S.served_ok("gpt-6-astra", None))

    def test_answered_and_dedupe(self):
        ok = rec("openai", call_id="c9")
        bad = dict(ok, status="error", text="", error="boom")
        self.assertTrue(S.is_answered(ok))
        self.assertFalse(S.is_answered(bad))
        self.assertFalse(S.is_answered(dict(ok, served_model="gpt-6-astra-mini")))
        self.assertIs(S.dedupe_calls([ok, bad])[0], ok)
        self.assertIs(S.dedupe_calls([bad, ok])[0], ok)

    def test_text_urls(self):
        t = "See [site](https://www.brand-a.test/x) and https://rtings.com/y."
        self.assertEqual(S.text_urls(t), ["https://www.brand-a.test/x", "https://www.brand-a.test/x",
                                          "https://rtings.com/y"])


class TestEvidenceAndBrandStats(unittest.TestCase):
    U = units_from(DOM)

    def answers(self, recs, field=S.PRIMARY_FIELD, named=None):
        named = named or {r["call_id"]: {("v19", "BrandA"), ("v19", "BrandB")} for r in recs}
        return S.build_answers(recs, named, self.U, C, field)

    def test_sources_primary_citations_sensitivity(self):
        r = rec("anthropic", sources=[{"url": "https://www.brand-a.test/p", "title": None},
                                      {"url": "https://rtings.com/x", "title": None}],
                citations=[{"url": "https://rtings.com/x", "title": None}])
        prim = S.brand_stats(self.answers([r]), self.U, floor=1)[("v19", "BrandA")]
        s2 = S.brand_stats(self.answers([r], S.CITED_FIELD), self.U, floor=1)[("v19", "BrandA")]
        self.assertEqual((prim["g"], prim["o"]), (1, 1))
        self.assertEqual((s2["g"], s2["o"]), (1, 0))

    def test_g_star_and_floor(self):
        recs = []
        for i in range(8):            # 8 answers name BrandA; 6 grounded; 3 of those retrieve brand-a.test
            src = [] if i >= 6 else [{"url": "https://rtings.com/x"}]
            if i < 3:
                src.append({"url": f"https://www.brand-a.test/p{i}"})
            recs.append(rec("anthropic", sources=src, call_id=f"c{i}"))
        st = S.brand_stats(self.answers(recs), self.U)
        a = st[("v19", "BrandA")]
        self.assertEqual((a["m"], a["g"], a["o"]), (8, 6, 3))
        self.assertAlmostEqual(a["G_star"], 50.0)
        self.assertTrue(a["rated"])
        self.assertEqual(st[("v19", "BrandB")]["o"], 0)
        self.assertFalse(st[("v19", "BrandC")]["rated"])
        m_den = S.brand_stats(self.answers(recs), self.U, denominator="m")[("v19", "BrandA")]
        self.assertAlmostEqual(m_den["G_star"], 37.5)

    def test_no_domain_not_rated(self):
        u = units_from(DOM, {("v19", "BrandD"): {"substrate": "v19", "brand_id": "BrandD", "brand": "BrandD",
                                                 "coder_key": "BrandD", "status": "NONE", "domains": set()}})
        recs = [rec("anthropic", sources=[{"url": "https://rtings.com/x"}], call_id=f"c{i}") for i in range(8)]
        named = {r["call_id"]: {("v19", "BrandD")} for r in recs}
        st = S.brand_stats(S.build_answers(recs, named, u, C), u)[("v19", "BrandD")]
        self.assertEqual((st["g"], st["o"], st["rated"]), (8, None, False))
        self.assertIn("no D_b", st["reason"])

    def test_google_duplicates_dedup_and_unresolved(self):
        srcs = S.answer_sources(rec("google", sources=[{"url": G_REDIRECT + "A", "title": "brand-c.test"}] * 4),
                                C, SUB)
        self.assertEqual(len(srcs), 1)
        self.assertEqual(srcs[0]["cls"], "brand_owned")
        self.assertTrue(srcs[0]["redirect"] and srcs[0]["via_title"])
        a = S.build_answers([rec("google", sources=[{"url": G_REDIRECT + "x", "title": "Some page"}])],
                            {"c1": {("v19", "BrandC")}}, self.U, C)
        self.assertEqual(S.brand_stats(a, self.U)[("v19", "BrandC")]["g"], 0)

    def test_source_mix(self):
        srcs = S.answer_sources(rec("openai", sources=[{"url": "https://rtings.com/a"}, {"url": "https://reddit.com/b"}]),
                                C, SUB)
        mix = S.source_mix([srcs])
        self.assertAlmostEqual(mix["review_editorial"], 0.5)
        self.assertAlmostEqual(mix["forum_ugc"], 0.5)

    def test_named_index(self):
        rows = [{"call_id": "c1", "substrate": "v0.19", "brand": "BrandA", "mentioned": "1"},
                {"call_id": "c1", "substrate": "v0.19", "brand": "BrandB", "mentioned": "0"}]
        self.assertEqual(S.named_index(rows, self.U), {"c1": {("v19", "BrandA")}})
        with self.assertRaises(ValueError):
            S.named_index([{"call_id": "c1", "substrate": "v0.19", "brand": "Nope", "mentioned": 1}], self.U)


# groups of 5 and 9 whose within-group rank correlation is exactly 0 (see test_centring)
XA, YA = [1, 2, 3, 4, 5], [2, 5, 3, 1, 4]
XB, YB = [1, 2, 3, 4, 5, 6, 7, 8, 9], [6, 1, 9, 2, 8, 4, 7, 3, 5]


class TestStats(unittest.TestCase):
    def test_avg_ranks(self):
        self.assertEqual(S.avg_ranks([10, 20, 20, 5]), [2.0, 3.5, 3.5, 1.0])

    def test_centring(self):
        x, y, g = XA + XB, YA + YB, ["a"] * 5 + ["b"] * 9
        self.assertAlmostEqual(S.rho_w(x, y, g, centred=True), 0.0, places=12)
        self.assertGreater(S.rho_w(x, y, g, centred=False), 0.1)   # between-substrate term of uncentred pooling

    def test_paired_drops_small_substrates(self):
        xd = {("a", i): float(i) for i in range(5)}
        xd.update({("b", i): float(i) for i in range(4)})
        keys, x, y, g, info = S.paired(xd, dict(xd))
        self.assertEqual((info["n"], info["dropped_substrates"]), (5, {"b": 4}))

    def test_permutation(self):
        rng = random.Random(3)
        xd = {(s, i): rng.random() for s in "abc" for i in range(12)}
        yd_pos = {k: v + 0.01 * rng.random() for k, v in xd.items()}
        yd_neg = {k: -v for k, v in xd.items()}
        lp = S.sep_leg(xd, yd_pos, 113001, n_perm=499, n_boot=0)
        self.assertLess(lp["p"], 0.01)
        self.assertEqual(lp["p"], S.sep_leg(xd, yd_pos, 113001, n_perm=499, n_boot=0)["p"])   # seeded
        ln = S.sep_leg(xd, yd_neg, 113001, n_perm=499, n_boot=0, sided="one")
        self.assertGreater(ln["p"], 0.9)
        indep = {k: rng.random() for k in xd}
        self.assertGreater(S.sep_leg(xd, indep, 113001, n_perm=499, n_boot=0)["p"], 0.002)

    def test_bootstrap(self):
        rng = random.Random(5)
        xd = {(s, i): rng.random() for s in "abc" for i in range(12)}
        yd = {k: v + 0.3 * rng.random() for k, v in xd.items()}
        leg = S.sep_leg(xd, yd, 1, n_perm=0, n_boot=300)
        ci = leg["ci90"]
        self.assertEqual(ci["level"], 90.0)
        self.assertLessEqual(ci["lo"], leg["rho_w"])
        self.assertGreaterEqual(ci["hi"], leg["rho_w"])

    def test_partial_rho(self):
        rng = random.Random(9)
        xd = {(s, i): rng.random() for s in "abcde" for i in range(8)}
        zd = {k: rng.random() for k in xd}
        self.assertAlmostEqual(S.partial_rho(xd, dict(xd), zd), 1.0)


def leg(rho, n=40):
    return {"rho_w": rho, "n": n, "below_n_floor": n < S.FLOOR_UNITS}


class TestVerdicts(unittest.TestCase):
    def test_sep_bands(self):
        self.assertEqual(S.sep_verdict([leg(0.10), leg(-0.29)]), "CONFIRMED")
        self.assertEqual(S.sep_verdict([leg(0.10), leg(0.31)]), "MARGINAL")
        self.assertEqual(S.sep_verdict([leg(0.10), leg(-0.50)]), "FALSIFIED")
        self.assertEqual(S.sep_verdict([leg(0.10), leg(0.10, n=29)]), "UNDETERMINED")
        self.assertEqual(S.sep_verdict([leg(0.60), leg(0.10, n=29)]), "FALSIFIED")
        self.assertEqual(S.sep_verdict([leg(0.10), leg(0.10)], mq5_failed=True), "UNDETERMINED")
        self.assertEqual(S.sep_verdict([leg(None)]), "UNDETERMINED")

    def test_reliability(self):
        self.assertAlmostEqual(S.spearman_brown_3(0.25), 0.5)
        self.assertEqual(S.spearman_brown_3(-0.6), float("-inf"))
        v = S.reliability_verdict
        self.assertEqual(v({"n_qualifying_pairs": 3, "rel3": 0.5, "p": 0.01}), "CONFIRMED")
        self.assertEqual(v({"n_qualifying_pairs": 3, "rel3": 0.6, "p": 0.20}), "MARGINAL")
        self.assertEqual(v({"n_qualifying_pairs": 3, "rel3": 0.2, "p": 0.01}), "FALSIFIED")
        self.assertEqual(v({"n_qualifying_pairs": 1, "rel3": 0.9, "p": 0.01}), "UNDETERMINED")

    def test_reliability_test(self):
        rng = random.Random(11)
        theta = {(s, i): rng.random() for s in ("v19", "v20", "v21", "v22", "v23") for i in range(8)}
        runs = {r: {k: 100 * min(1, max(0, t + 0.05 * rng.gauss(0, 1))) for k, t in theta.items()} for r in (1, 2, 3)}
        t = S.reliability_test(runs, n_perm=199)
        self.assertEqual(t["n_qualifying_pairs"], 3)
        self.assertEqual(S.reliability_verdict(t), "CONFIRMED")
        short = {1: runs[1], 2: {k: v for k, v in list(runs[2].items())[:20]}, 3: runs[3]}
        self.assertEqual(S.reliability_test(short, n_perm=99)["n_qualifying_pairs"], 1)
        self.assertEqual(S.reliability_verdict(S.reliability_test(short, n_perm=99)), "UNDETERMINED")

    def test_struct_gap(self):
        self.assertEqual(S.struct_gap_verdict(dict(leg(0.35), p=0.01)), "CONFIRMED")
        self.assertEqual(S.struct_gap_verdict(dict(leg(0.35), p=0.20)), "MARGINAL")
        self.assertEqual(S.struct_gap_verdict(dict(leg(0.05), p=0.60)), "FALSIFIED")
        self.assertEqual(S.struct_gap_verdict(dict(leg(0.50, n=20), p=0.01)), "UNDETERMINED")
        self.assertEqual(S.struct_gap_verdict(None, collected=False), "UNDETERMINED")

    def test_mq5(self):
        sub = {(f"v{19 + i % 5}", f"b{i}"): 0.0 for i in range(20)}
        self.assertTrue(S.mq5_degenerate(sub)["failed"])
        varied = {k: float(i) for i, k in enumerate(sub)}
        self.assertFalse(S.mq5_degenerate(varied)["failed"])
        flat3 = dict(varied)
        for k in flat3:
            if k[0] in ("v19", "v20", "v21"):
                flat3[k] = 10.0
        self.assertTrue(S.mq5_degenerate(flat3)["failed"])


class TestGate(unittest.TestCase):
    OFF = {l: False for l in S.CONDITIONAL_LEGS}

    def v(self, h1, h2, h3, **cond):
        d = {"H1_Sep_Presence": h1, "H2_Sep_Consistency": h2, "H3_Run_Reliability": h3}
        for l in S.CONDITIONAL_LEGS:
            d[l] = cond.get(l, "INACTIVE")
        return d

    def test_rules(self):
        g = lambda *a, act=None, **k: S.gate(self.v(*a, **k), act or self.OFF)["verdict"]
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED"), "PASS")
        self.assertEqual(g("CONFIRMED", "FALSIFIED", "CONFIRMED"), "FAIL")
        self.assertEqual(g("UNDETERMINED", "CONFIRMED", "FALSIFIED"), "FAIL")
        self.assertEqual(g("UNDETERMINED", "CONFIRMED", "CONFIRMED"), "UNDETERMINED")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "UNDETERMINED"), "MARGINAL")
        self.assertEqual(g("MARGINAL", "CONFIRMED", "CONFIRMED"), "MARGINAL")
        act = dict(self.OFF, H4_Sep_Ranking=True)
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", act=act, H4_Sep_Ranking="FALSIFIED"), "MARGINAL")
        self.assertEqual(g("CONFIRMED", "CONFIRMED", "CONFIRMED", act=act, H4_Sep_Ranking="UNDETERMINED"), "PASS")
        with self.assertRaises(ValueError):
            S.gate(self.v("CONFIRMED", "CONFIRMED", "CONFIRMED", H5_Sep_Sentiment="FALSIFIED"), self.OFF)

    def test_activation(self):
        rec_ = {"conditional_legs": {"H4_Sep_Ranking": {"tag": "v1.10-prereg-r2", "pushed_before_lock": True},
                                     "H6_Sep_Coverage": {"tag": "v1.12-prereg-r1", "pushed_before_lock": False}}}
        self.assertEqual(S.activation(rec_), {"H4_Sep_Ranking": True, "H5_Sep_Sentiment": False,
                                              "H6_Sep_Coverage": False})
        self.assertEqual(S.activation(None), {l: False for l in S.CONDITIONAL_LEGS})


PROVIDER = {"claude-fable-5-2": "anthropic", "claude-opus-5-5": "anthropic", "gpt-6-astra": "openai",
            "gemini-4-argon": "google"}


def synthetic_t4(seed=7, p_tracks_g=False):
    """5 substrates x 8 units (v19 includes a unit 'Denon'), the 3 N3 models x 3 runs x 6 frames, S0 and S1
    (Phase A rows in both conditions here; the scorer reads S0 recognition only)."""
    rng = random.Random(seed)
    units, theta = {}, {}
    for s in S.SUBSTRATES:
        for i in range(8):
            bid = "Denon" if (s == "v19" and i == 0) else f"B{i}"
            k = (s, bid)
            units[k] = {"substrate": s, "brand_id": bid, "brand": bid, "coder_key": bid, "status": "RESOLVED",
                        "domains": {f"{s}-{bid.lower()}.test"}}
            theta[k] = rng.uniform(0.05, 0.9)
    records, coded_a, coded_b, table = [], [], [], []
    for s in S.SUBSTRATES:
        keys = [k for k in units if k[0] == s]
        for m in S.PANELS["N3"]:
            for run in (1, 2, 3):
                for cond in ("S0", "S1"):
                    for f in range(6):
                        cid = f"{s}|B|q{f}|{m}|{cond}|{run}"
                        named = [k for k in keys if rng.random() < 0.85]
                        srcs = [{"url": "https://en.wikipedia.org/wiki/x", "title": None},
                                {"url": "https://rtings.com/r", "title": None}]
                        for k in named:
                            if rng.random() < theta[k]:
                                srcs.append({"url": f"https://www.{next(iter(units[k]['domains']))}/p", "title": None})
                        if m == "gemini-4-argon":
                            srcs = [{"url": G_REDIRECT + str(j), "title": S.resolve_source(e["url"], None, C)["domain"]}
                                    for j, e in enumerate(srcs)]
                        r = rec(PROVIDER[m], sources=srcs if cond == "S1" else None, citations=srcs[:1], model=m,
                                call_id=cid, run=run, sub=s)
                        r["condition"] = cond
                        if cond == "S0":
                            r["search"] = None
                        records.append(r)
                        for k in keys:
                            coded_b.append({"call_id": cid, "substrate": S.CODER_SUB[s], "brand": k[1], "model": m,
                                            "condition": cond, "run": str(run), "mentioned": str(int(k in named))})
                    for k in keys:
                        cid = f"{s}|A|{k[1]}|{m}|{cond}|{run}"
                        ra = rec(PROVIDER[m], model=m, call_id=cid, run=run, sub=s)
                        ra.update(phase="A", condition=cond, brand_id=k[1], search=None)
                        records.append(ra)
                        coded_a.append({"call_id": cid, "substrate": S.CODER_SUB[s], "brand": k[1], "model": m,
                                        "condition": cond, "run": str(run), "recognized": "1"})
        for k in keys:
            pi = theta[k] if p_tracks_g else rng.random()
            table.append({"substrate": S.CODER_SUB[s], "brand": k[1], "pi_N3_S0": str(pi), "pi_N3_S1": str(pi),
                          "phi_N3_S0": str(rng.uniform(0, 5)), "phi_N3_S1": str(rng.uniform(0, 5))})
    return {"records": records, "coded_a": coded_a, "coded_b": coded_b, "brand_table": table, "units": units,
            "classes": C, "active": {l: False for l in S.CONDITIONAL_LEGS}}


class TestStageC1Synthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = S.stage_c1(synthetic_t4(), n_perm=199, n_boot=50)

    def test_structure(self):
        d = self.doc
        self.assertEqual(d["primary_field"], "sources")
        self.assertEqual(d["panel_models"], list(S.PANELS["N3"]))
        self.assertIn(d["gate"]["verdict"], {"PASS", "FAIL", "MARGINAL", "UNDETERMINED"})
        self.assertEqual(d["verdicts"]["H3_Run_Reliability"], "CONFIRMED")   # G* driven by a stable brand trait
        self.assertEqual({d["verdicts"][l] for l in S.CONDITIONAL_LEGS}, {"INACTIVE"})
        self.assertFalse(d["MQ"]["MQ4"]["drop_gemini"])
        self.assertEqual(d["MQ"]["MQ4"]["unresolved_share"], 0.0)
        self.assertEqual(d["legs"]["H1_Sep_Presence"][0]["n"], 40)
        self.assertFalse(any(n.startswith("S3") for n in d["sensitivities"]))   # A4/C3 removed (t4 r2)
        for name in ("S1_denominator_m", "S2_citations", "S4_floor_3", "S4_floor_10",
                     "S5_gemini_dropped", "S8_leave_one_substrate_out", "S9_text_urls", "S10_uncentred",
                     "S11_without_Denon"):
            self.assertIn(name, d["sensitivities"])
        self.assertEqual(d["sensitivities"]["S11_without_Denon"]["verdicts"]["H3_Run_Reliability"], "CONFIRMED")

    def test_denon_excluded(self):
        inp = synthetic_t4()
        answers = S.build_answers(S.select_calls(S.dedupe_calls(inp["records"]), S.PANELS["N3"], "S1", "B"),
                                  S.named_index(inp["coded_b"], inp["units"]), inp["units"], C)
        r = S.gate_statistics(answers, inp["units"], {"S0": {}, "S1": {}}, {"S0": {}, "S1": {}}, n_perm=0, n_boot=0,
                              exclude=(S.DENON,))
        self.assertEqual(r["H3"]["pairs"][0]["n"], 39)
        self.assertNotIn(S.DENON, {k for k, v in r["g_star"].items() if v is None})

    def test_presence_tracking_fails_gate(self):
        doc = S.stage_c1(synthetic_t4(p_tracks_g=True), n_perm=99, n_boot=0, sensitivities=False)
        self.assertEqual(doc["verdicts"]["H1_Sep_Presence"], "FALSIFIED")
        self.assertEqual(doc["gate"]["verdict"], "FAIL")

    def test_refuses_unresolved(self):
        inp = synthetic_t4()
        k = next(iter(inp["units"]))
        inp["units"][k] = dict(inp["units"][k], status="UNRESOLVED", domains=set())
        with self.assertRaises(SystemExit):
            S.stage_c1(inp, n_perm=0, n_boot=0, sensitivities=False)

    def test_readers(self):
        inp = synthetic_t4()
        P = S.p_t4(inp["brand_table"], inp["coded_a"], inp["units"], "S0", S.PANELS["N3"])
        k = ("v20", "B3")
        row = next(r for r in inp["brand_table"] if r["substrate"] == "v0.20" and r["brand"] == "B3")
        self.assertAlmostEqual(P[k], 100 * (1 + 2 * float(row["pi_N3_S0"])) / 3)
        Cs = S.c_star_t4(inp["brand_table"], inp["coded_b"], inp["units"], "S1", S.PANELS["N3"])
        self.assertAlmostEqual(Cs[k], 100 * (1 - float(row["phi_N3_S1"]) / 9))

    def test_shared_p_definition_s0_recognition(self):
        """P_S1 uses the S0 Phase A recognition (t4 r2 has no Phase A in S1); C_P/3 = share of N3 models."""
        inp = synthetic_t4()
        k = ("v20", "B3")
        coded_a = [r for r in inp["coded_a"] if r["condition"] == "S0" and r["run"] == "1"]
        for r in coded_a:
            if r["substrate"] == "v0.20" and r["brand"] == "B3" and r["model"] == S.GEM4:
                r["recognized"] = "0"
        row = next(r for r in inp["brand_table"] if r["substrate"] == "v0.20" and r["brand"] == "B3")
        P1 = S.p_t4(inp["brand_table"], coded_a, inp["units"], "S1", S.PANELS["N3"])
        self.assertAlmostEqual(P1[k], 100 * (2 / 3 + 2 * float(row["pi_N3_S1"])) / 3)
        a_s1_only = [dict(r, condition="S1") for r in coded_a]
        self.assertIsNone(S.p_t4(inp["brand_table"], a_s1_only, inp["units"], "S1", S.PANELS["N3"])[k])
        miss = [r for r in coded_a if not (r["brand"] == "B3" and r["model"] == S.GPT6)]
        P2 = S.p_t4(inp["brand_table"], miss, inp["units"], "S0", S.PANELS["N3"])
        self.assertAlmostEqual(P2[k], 100 * (1 / 2 + 2 * float(row["pi_N3_S0"])) / 3)   # coded models only

    def test_c_star_partitions(self):
        inp = synthetic_t4()
        rows = [r for r in inp["brand_table"] if r["substrate"] == "v0.20"]
        rows[0].update(phi_partition_N3_S0="defined", phi_N3_S0="4.5")
        rows[1].update(phi_partition_N3_S0="saturated", phi_N3_S0="")
        rows[2].update(phi_partition_N3_S0="zero", phi_N3_S0="")
        rows[3].update(phi_partition_N3_S0="undefined", phi_N3_S0="")
        Cs = S.c_star_t4(inp["brand_table"], inp["coded_b"], inp["units"], "S0", S.PANELS["N3"])
        keys = [("v20", r["brand"]) for r in rows[:4]]
        self.assertAlmostEqual(Cs[keys[0]], 50.0)
        self.assertEqual(Cs[keys[1]], 100.0)
        self.assertIsNone(Cs[keys[2]])
        self.assertIsNone(Cs[keys[3]])
        self.assertEqual(S.C_STAR_DIVISOR, 6 * 3 / (3 - 1))

    def test_v042_pins(self):
        self.assertEqual(S.V042_PINS["osf/v42/scripts/code_t4_v0_42.py"], "2d36735d512cf9e13b74010ba5a7f655fc7de0bc")
        self.assertEqual(S.V042_PINS["osf/v42/scripts/score_v0_42.py"], "9e2c86c167d18981f0ac6c63ce8480f8c005205a")
        self.assertEqual(set(S.PANELS), {"N3"})
        self.assertFalse(hasattr(S, "g_a_map"))

    def test_house_portal_flag(self):
        self.assertEqual(S.HOUSE_PORTAL_UNITS, {("v20", "A.5"), ("v20", "A.6"), ("v23", "S09")})
        units = S.load_brand_domains()
        self.assertEqual({k: units[k]["domains"] & {"dior.com", "chanel.com", "malts.com"} for k in S.HOUSE_PORTAL_UNITS},
                         {("v20", "A.5"): {"dior.com"}, ("v20", "A.6"): {"chanel.com"}, ("v23", "S09"): {"malts.com"}})
        self.assertEqual(S.unresolved_units(units), [] if isinstance(S.unresolved_units(units), list) else set())


class TestGuard(unittest.TestCase):
    def test_stage_c1_refused_without_lock(self):
        with self.assertRaises(SystemExit) as cm:
            S.main(["--stage", "C1"])
        self.assertIn("REFUSED", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
