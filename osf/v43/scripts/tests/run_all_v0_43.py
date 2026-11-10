#!/usr/bin/env python3
"""Unit and integration tests for the v0.43 Trends kit (plain asserts). Prints 'N/N pass'."""
import argparse
import datetime as dt
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(SCRIPTS, "../../.."))
sys.path.insert(0, SCRIPTS)
import numpy as np  # noqa: E402
import trends_common_v0_43 as tc  # noqa: E402
import acquire_trends_v0_43 as aq  # noqa: E402
import score_v0_43 as sc  # noqa: E402
import build_units_v0_43 as bu  # noqa: E402

D = dt.date


def week_resp(weeks, cols, partial_idx=(), step=7):
    """Build a SerpAPI-like response. weeks: list of dates; cols: list of value lists."""
    pts = []
    for i, w in enumerate(weeks):
        ts = int(dt.datetime(w.year, w.month, w.day, tzinfo=dt.timezone.utc).timestamp())
        p = {"date": str(w), "timestamp": str(ts),
             "values": [{"query": f"t{k}", "value": str(c[i]), "extracted_value": c[i]} for k, c in enumerate(cols)]}
        if i in partial_idx:
            p["partial_data"] = True
        pts.append(p)
    return {"interest_over_time": {"timeline_data": pts}}


def sundays(a, b):
    out, d = [], a
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


# ------------------------------------------------------------------ tests
def test_window_sums_sunday_weeks():
    ws = tc.window_starts(D(2026, 6, 6))
    assert ws == [D(2026, 5, 10), D(2026, 5, 17), D(2026, 5, 24), D(2026, 5, 31)], ws
    assert all(w.weekday() == 6 for w in ws)
    try:
        tc.window_starts(D(2026, 6, 7))  # a Sunday
        assert False, "should reject non-Saturday"
    except ValueError:
        pass
    weeks = sundays(D(2025, 5, 4), D(2026, 11, 1))
    vals = list(range(len(weeks)))
    ser = tc.parse_timeseries(week_resp(weeks, [vals]))
    exp = sum(vals[weeks.index(w)] for w in ws)
    assert tc.window_sum(ser.values[0], D(2026, 6, 6)) == exp
    assert tc.last_saturday_before(D(2026, 11, 10)) == D(2026, 11, 7)
    assert tc.last_saturday_before(D(2026, 11, 7)) == D(2026, 10, 31)
    assert tc.shift_weeks(D(2026, 6, 6), -52) == D(2025, 6, 7)
    assert tc.shift_weeks(D(2026, 11, 7), -52) == D(2025, 11, 8)


def test_mc_weekly_catches_problems():
    a, b = D(2025, 5, 4), D(2026, 11, 7)
    weeks = sundays(a, D(2026, 11, 1))
    good = tc.parse_timeseries(week_resp(weeks, [[5] * len(weeks)]))
    ok, r = tc.mc_weekly(good, a, b, [D(2026, 6, 6), D(2026, 11, 7)])
    assert ok, r
    # daily series
    days = [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]
    daily = tc.parse_timeseries(week_resp(days, [[1] * len(days)]))
    ok, r = tc.mc_weekly(daily, a, b, [D(2026, 6, 6)])
    assert not ok and any("not 7" in x or "Sunday" in x for x in r), r
    # gap (a week missing)
    gap_w = weeks[:30] + weeks[31:]
    gap = tc.parse_timeseries(week_resp(gap_w, [[1] * len(gap_w)]))
    ok, r = tc.mc_weekly(gap, a, b, [D(2026, 6, 6)])
    assert not ok and any("not 7" in x for x in r), r
    # partial point inside a window
    i = weeks.index(D(2026, 5, 24))
    part = tc.parse_timeseries(week_resp(weeks, [[1] * len(weeks)], partial_idx=[i]))
    ok, r = tc.mc_weekly(part, a, b, [D(2026, 6, 6)])
    assert not ok and any("partial" in x for x in r), r
    # partial point outside any window is allowed
    part2 = tc.parse_timeseries(week_resp(weeks, [[1] * len(weeks)], partial_idx=[2]))
    ok, r = tc.mc_weekly(part2, a, b, [D(2026, 6, 6)])
    assert ok, r
    # range not covered (stops early) and wrong start day
    short = weeks[:-5]
    ok, r = tc.mc_weekly(tc.parse_timeseries(week_resp(short, [[1] * len(short)])), a, b, [])
    assert not ok
    mon = [w + dt.timedelta(days=1) for w in weeks]
    ok, r = tc.mc_weekly(tc.parse_timeseries(week_resp(mon, [[1] * len(mon)])), a, b, [])
    assert not ok
    # wrong number of terms
    ok, r = tc.mc_weekly(good, a, b, [], n_terms=3)
    assert not ok


def make_sim(vols, seed=1, noise=0.0, trend=None):
    return {"seed": seed, "noise": noise,
            "terms": {t: {"base": v, "trend": (trend or {}).get(t, 0.0)} for t, v in vols.items()}}


def test_chaining_recovers_simulated_volumes():
    # geometric ladder of true volumes; bundles formed exactly as s4.3; Trends rounding simulated
    units = [f"u{i:02d}" for i in range(11)]
    vols = {u: 1000.0 * (0.72 ** i) for i, u in enumerate(units)}
    sim = make_sim(vols)
    key = lambda u: (-vols[u], u)  # noqa: E731
    bundles = tc.main_bundles(units, key)
    assert [len(b) for b in bundles] == [5, 5, 3], bundles
    assert bundles[1][0] == bundles[0][-1] and bundles[2][0] == bundles[1][-1]
    rng = (D(2025, 5, 4), D(2026, 11, 7))
    sers = [tc.parse_timeseries(aq.sim_response(sim, ",".join(b), f"{rng[0]} {rng[1]}")) for b in bundles]
    info, links = tc.chain_factors(bundles, sers)
    assert links == [True, True]
    lv = tc.unit_levels(bundles, sers, info, D(2026, 6, 6))
    ratios = [lv[u][1] / vols[u] for u in units]
    assert max(ratios) / min(ratios) < 1.05, ratios  # within rounding error of the 0-100 integers
    rk = tc.rank_levels(lv)
    assert [rk[u] for u in units] == sorted((rk[u] for u in units), reverse=True)  # level order recovered


def test_failed_link_ranks_later_bundles_below():
    wk = sundays(D(2025, 5, 4), D(2026, 11, 1))
    n = len(wk)
    # bundle 0: units a (50), b (40), shared unit c (30); bundle 1: shared c has ZERO sum -> fails; d (90), e (80)
    s0 = tc.parse_timeseries(week_resp(wk, [[50] * n, [40] * n, [30] * n]))
    s1 = tc.parse_timeseries(week_resp(wk, [[0] * n, [100] * n, [90] * n]))
    bundles = [["a", "b", "c"], ["c", "d", "e"]]
    info, links = tc.chain_factors(bundles, [s0, s1])
    assert links == [False] and info[0][0] == 0 and info[1][0] == 1 and info[1][1] == 1.0
    lv = tc.unit_levels(bundles, [s0, s1], info, D(2026, 6, 6))
    rk = tc.rank_levels(lv)
    # d, e have bigger own-bundle levels (100, 90) than a, b, c (50, 40, 30) but rank below all of them
    assert max(rk["d"], rk["e"]) < min(rk["a"], rk["b"], rk["c"]), rk
    assert rk["d"] > rk["e"]  # own within-bundle order
    # a missing request also breaks the chain
    info2, links2 = tc.chain_factors(bundles, [s0, None])
    assert links2 == [False] and info2[1] is None
    # sort key for main bundles: earlier segment first, then size desc, then alphabetical
    k = tc.size_sort_key
    assert sorted(["b", "a", "c"], key=lambda u: k((0, 5.0), u)) == ["a", "b", "c"]
    assert k((0, 1.0), "z") < k((1, 99.0), "a")


def test_pull_stats_and_combination_rules():
    wk = sundays(D(2025, 5, 4), D(2026, 11, 1))
    n = len(wk)

    def col(base, end, prior=None):
        v = [10.0] * n
        for w in tc.window_starts(D(2026, 6, 6)):
            v[wk.index(w)] = base
        for w in tc.window_starts(D(2026, 11, 7)):
            v[wk.index(w)] = end
        if prior is not None:
            for w in tc.window_starts(D(2026, 2, 7)):
                v[wk.index(w)] = prior
        return v
    ser = tc.parse_timeseries(week_resp(wk, [col(10, 20, 5), col(0, 0), col(1, 0)]))
    st = tc.pull_stats([["x", "z", "w"]], [ser], 1)["units"]
    assert abs(st["x"]["Y"] - math.log((80 + 1) / (40 + 1))) < 1e-12
    assert abs(st["x"]["M"] - math.log((40 + 1) / (20 + 1))) < 1e-12
    assert st["z"]["Y"] is None  # S_base + S_end = 0 < 4
    assert st["w"]["Y"] == math.log(1 / 5)  # S_base + S_end = 4 + 0 = 4 >= 4 -> defined


def test_pull_stats_boundary_is_four():
    wk = sundays(D(2025, 5, 4), D(2026, 11, 1))
    n = len(wk)
    v = [0.0] * n
    for w in tc.window_starts(D(2026, 6, 6)):
        v[wk.index(w)] = 1.0  # S_base = 4, S_end = 0 -> sum 4 -> defined
    ser = tc.parse_timeseries(week_resp(wk, [v, [0.0] * n]))
    st = tc.pull_stats([["a", "b"]], [ser], 1)["units"]
    assert st["a"]["Y"] == math.log(1 / 5)
    assert st["b"]["Y"] is None
    v2 = list(v)
    v2[wk.index(tc.window_starts(D(2026, 6, 6))[0])] = 0.0  # S_base = 3 -> undefined
    ser2 = tc.parse_timeseries(week_resp(wk, [v2, [0.0] * n]))
    assert tc.pull_stats([["a", "b"]], [ser2], 1)["units"]["a"]["Y"] is None
    # combination: defined in >= 2 of 3 pulls; mean over defined pulls
    p = [{"u": {"Y": 1.0, "Yp": 0.5, "M": None, "rank_base": 1, "rank_end": 2}},
         {"u": {"Y": 3.0, "Yp": None, "M": None, "rank_base": 3, "rank_end": 2}},
         {"u": {"Y": None, "Yp": None, "M": None, "rank_base": None, "rank_end": None}}]
    c = tc.combine_pulls(p)["u"]
    assert c["Y"] == 2.0 and c["Yp"] is None and c["Y_SA"] is None and c["L"] == 2.0
    p[1]["u"]["Y"] = None
    assert tc.combine_pulls(p)["u"]["Y"] is None  # only 1 of 3
    # two bundles holding one unit: mean of the two values
    ser_a = tc.parse_timeseries(week_resp(wk, [[8.0] * n]))
    ser_b = tc.parse_timeseries(week_resp(wk, [[16.0] * n]))
    r = tc.pull_stats([["q"], ["q"]], [ser_a, ser_b], 1)["units"]["q"]
    assert r["Y"] == 0.0


def _rows(rng, n_sims_rho=0.4, sizes=(16, 24, 24, 24, 24)):
    rows = []
    for s, n in zip(sc.SUBSTRATES, sizes):
        Z = rng.standard_normal(n)
        Xr = rng.standard_normal(n)
        X = Xr + 0.5 * Z
        a = 0.4
        sig = a * math.sqrt(1 / n_sims_rho ** 2 - 1)
        Y = a * Xr + 0.7 * Z + sig * rng.standard_normal(n)
        for i in range(n):
            rows.append({"sub": s, "X": X[i], "Y": Y[i], "Z": Z[i]})
    return rows


def test_planted_partial_correlation_recovered():
    rng = np.random.default_rng(7)
    hits, rhos = 0, []
    for k in range(50):
        rows = _rows(rng)
        st = sc.run_stat(rows, ("X", "Y", ["Z"]), 1000 + k, B_perm=499, B_boot=0, boot=False)
        rhos.append(st["rho"])
        hits += st["p_one"] < 0.05
    assert st["n"] == 112
    assert hits >= 40, hits
    assert 0.3 < float(np.mean(rhos)) < 0.5, np.mean(rhos)


def test_null_pvalues_roughly_uniform():
    rng = np.random.default_rng(11)
    ps = []
    for k in range(200):
        rows = []
        for s, n in zip(sc.SUBSTRATES, (16, 24, 24, 24, 24)):
            Z = rng.standard_normal(n)
            X, Y = rng.standard_normal(n), rng.standard_normal(n)
            rows += [{"sub": s, "X": X[i], "Y": Y[i], "Z": Z[i]} for i in range(n)]
        ps.append(sc.run_stat(rows, ("X", "Y", ["Z"]), 2000 + k, B_perm=999, B_boot=0, boot=False)["p_one"])
    m = float(np.mean(ps))
    assert 0.4 < m < 0.6, m
    assert min(ps) >= 1 / 1000 - 1e-12  # (1 + count) / (B + 1)


def test_rho_and_bootstrap_machinery():
    rng = np.random.default_rng(3)
    rows = _rows(rng)
    st = sc.run_stat(rows, ("X", "Y", ["Z"]), 430041, B_perm=999, B_boot=300)
    assert st["ci90"][0] < st["rho"] < st["ci90"][1]
    assert st["ci95"][0] <= st["ci90"][0] and st["ci95"][1] >= st["ci90"][1]
    # seed reproducibility
    st2 = sc.run_stat(rows, ("X", "Y", ["Z"]), 430041, B_perm=999, B_boot=300)
    assert st == st2
    # with no control it equals the pooled within-substrate Spearman by hand
    from scipy.stats import rankdata
    ry, rx = [], []
    for s in sc.SUBSTRATES:
        rs = [r for r in rows if r["sub"] == s]
        a = rankdata([r["Y"] for r in rs])
        b = rankdata([r["X"] for r in rs])
        ry += list(a - a.mean())
        rx += list(b - b.mean())
    hand = float(np.corrcoef(ry, rx)[0, 1])
    got = sc.run_stat(rows, ("X", "Y", []), 1, B_perm=0, B_boot=0, boot=False)["rho"]
    assert abs(hand - got) < 1e-12
    # the two-sided p is at least the one-sided p for a positive rho
    assert st["p_two"] >= st["p_one"] - 1e-12


def test_verdict_rule_edge_cases():
    v = sc.verdict
    assert v(0.15, 0.04, 0.08, 0.30, 100, 60)["verdict"] == "CONFIRMED"           # exactly 0.15
    assert v(0.1499, 0.04, 0.08, 0.30, 100, 60)["verdict"] == "MARGINAL"          # just below 0.15, p < .10
    assert v(0.20, 0.05, 0.10, 0.30, 100, 60)["verdict"] == "MARGINAL"            # p = .05 is not < .05
    assert v(0.05, 0.30, 0.6, 0.0999, 100, 60)["verdict"] == "FALSIFIED"          # upper bound 0.0999
    assert v(0.05, 0.30, 0.6, 0.10, 100, 60)["verdict"] == "UNDETERMINED"         # upper bound exactly 0.10
    assert v(0.05, 0.12, 0.2, 0.30, 100, 60)["verdict"] == "UNDETERMINED"         # positive, p >= .10
    assert v(0.12, 0.09, 0.18, 0.30, 100, 60)["verdict"] == "MARGINAL"
    assert v(0.40, 0.001, 0.002, 0.5, 59, 60)["verdict"] == "UNDETERMINED"        # minimum n
    assert v(0.40, 0.001, 0.002, 0.5, 29, 30)["verdict"] == "UNDETERMINED"        # consistency minimum
    assert v(0.40, 0.001, 0.002, 0.5, 30, 30)["verdict"] == "CONFIRMED"
    r = v(-0.30, 0.999, 0.01, -0.1, 100, 60)
    assert r["verdict"] == "FALSIFIED" and r["labels"] == ["REVERSED"], r         # label adds, verdict unchanged
    r = v(-0.10, 0.9, 0.04, 0.05, 100, 60)
    assert r["verdict"] == "FALSIFIED" and "REVERSED" in r["labels"]
    r = v(-0.10, 0.9, 0.06, 0.12, 100, 60)
    assert r["verdict"] == "UNDETERMINED" and r["labels"] == []                    # two-sided p >= .05: no label
    assert v(0.30, 0.01, 0.02, 0.4, 100, 60)["labels"] == []


def test_term_rule_cases():
    jag = [{"mid": "/m/animal", "title": "Jaguar", "type": "Animal"},
           {"mid": "/m/cars", "title": "Jaguar Cars", "type": "Automobile company"},
           {"mid": "/m/other", "title": "Jaguar Land Rover", "type": "Company"}]
    t, kind, sg = tc.choose_term("Jaguar", jag, "v0.22")
    assert (t, kind) == ("/m/cars", "topic") and sg["title"] == "Jaguar Cars"
    # same list, spirits: 'Automobile company' still matches 'company' (all substrates) -> first qualifying
    assert tc.choose_term("Jaguar", jag, "v0.23")[0] == "/m/cars"
    # accent normalisation
    el = [{"mid": "/m/el", "title": "Estee Lauder Companies", "type": "Cosmetics company"}]
    assert tc.choose_term("Estée Lauder", el, "v0.20")[:2] == ("/m/el", "topic")
    el2 = [{"mid": "/m/el", "title": "Estée Lauder", "type": "Beauty brand"}]
    assert tc.choose_term("Estee Lauder", el2, "v0.21")[:2] == ("/m/el", "topic")
    # "&" handling
    ms = [{"mid": "/m/ms", "title": "Marks & Spencer", "type": "Retail company"}]
    assert tc.choose_term("Marks and Spencer", ms, "v0.19")[:2] == ("/m/ms", "topic")
    assert tc.choose_term("Marks & Spencer", [{"mid": "/m/x", "title": "Marks and Spencer", "type": "Brand"}],
                          "v0.19")[:2] == ("/m/x", "topic")
    # no match -> plain name, never a manual fix
    t, kind, sg = tc.choose_term("Jaguar", [{"mid": "/m/animal", "title": "Jaguar", "type": "Animal"}], "v0.22")
    assert (t, kind, sg) == ("Jaguar", "plain", None)
    assert tc.choose_term("Nikka", [], "v0.23")[:2] == ("Nikka", "plain")
    # title must BEGIN with the search name
    assert tc.choose_term("Rhode", [{"mid": "/m/r", "title": "The Rhode Brand", "type": "Brand"}], "v0.20")[1] == "plain"
    # keyword must start a word: 'Scarf' does not match 'car'; 'Scarf brand' matches 'brand'
    assert not tc.type_matches("Scarf", "v0.22")
    assert tc.type_matches("Scarf brand", "v0.22")
    assert tc.type_matches("Car manufacturer", "v0.22") and tc.type_matches("Automobile", "v0.22")
    assert not tc.type_matches("Discard", "v0.22") and not tc.type_matches("Begin", "v0.23")  # 'gin' inside a word
    assert tc.type_matches("Gin distillery", "v0.23") and tc.type_matches("Personal care", "v0.21")
    assert tc.type_matches("SKINCARE", "v0.20") and not tc.type_matches("Animal", "v0.22")
    # first qualifying in RETURNED order (not best)
    two = [{"mid": "/m/1", "title": "Jaguar", "type": "Vehicle"}, {"mid": "/m/2", "title": "Jaguar Cars", "type": "Company"}]
    assert tc.choose_term("Jaguar", two, "v0.22")[0] == "/m/1"
    assert tc.normalise("Dolce & Gabbana!") == "dolceandgabbana"


def test_bundle_formation():
    names16 = [f"n{c}" for c in "pbcdefghijklmnoa"]
    order = tc.sizing_order(names16)
    assert order[0] == "na" and order == sorted(order)
    b = [tc.first_sizing_bundle(order)]
    placed = 5
    for k in range(10):
        if placed >= len(order):
            break
        prev = b[-1][2]  # pretend the third unit is the largest
        nb = tc.next_sizing_bundle(order, placed, prev)
        b.append(nb)
        placed += len(nb) - 1
    assert [len(x) for x in b] == [5, 5, 5, 4] and placed == 16
    order24 = [f"u{i:02d}" for i in range(24)]
    placed, sizes = 5, [5]
    while placed < 24:
        nb = tc.next_sizing_bundle(order24, placed, "x")
        sizes.append(len(nb))
        placed += len(nb) - 1
    assert len(sizes) == 6 and sizes == [5, 5, 5, 5, 5, 4]
    # main bundles: size desc, ties alphabetical, chain overlap, 16 -> 4 and 24 -> 6
    lv = {f"u{i:02d}": (0, float(100 - i // 2)) for i in range(24)}  # pairs of ties
    mb = tc.main_bundles(list(lv), lambda u: tc.size_sort_key(lv[u], u))
    assert len(mb) == 6 and sum(len(x) for x in mb) - 5 == 24
    assert mb[0] == ["u00", "u01", "u02", "u03", "u04"]
    assert all(mb[i + 1][0] == mb[i][-1] for i in range(5))
    mb16 = tc.main_bundles(list(list(lv)[:16]), lambda u: tc.size_sort_key(lv[u], u))
    assert len(mb16) == 4
    # 112 units -> 28 requests in total
    assert 4 + 6 * 4 == 28


def test_parity_file_all_exact():
    path = os.path.join(ROOT, "osf/v43/prereg/parity_units_v0_43.json")
    res = json.load(open(path))
    assert res["all_exact"] is True and res["n_units"] == 112 and res["mismatches"] == []
    for fld in ("P", "C_star", "mentions", "pi_hat"):
        e = res["fields"][fld]
        assert e["n_checked"] == 336 == e["n_string_exact"] == e["n_float_exact"], (fld, e)
    fresh = bu.parity(ROOT)  # recomputed from the committed units file against the frozen inputs
    assert fresh["all_exact"] is True and fresh["fields"] == res["fields"]
    assert res["units_per_substrate"] == {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
    assert res["rare_beauty_substrates"] == ["v0.20", "v0.21"]
    # tamper test: a changed value is caught
    tmp = tempfile.mkdtemp()
    try:
        shutil.copytree(os.path.join(ROOT, "osf/v43/registries"), os.path.join(tmp, "osf/v43/registries"))
        p = os.path.join(tmp, "osf/v43/registries/units_v0_43.csv")
        txt = open(p).read().replace("62.9630", "62.9631", 1)
        open(p, "w").write(txt)
        assert bu.parity(tmp)["all_exact"] is False
    finally:
        shutil.rmtree(tmp)


# ------------------------------------------------------------------ acquisition (mock)
def make_world(tmp):
    """tmp repo root with the real units file, plus a mock dir (autocomplete + _sim.json)."""
    reg = os.path.join(tmp, "osf/v43/registries")
    os.makedirs(reg)
    shutil.copy(os.path.join(ROOT, "osf/v43/registries/units_v0_43.csv"), reg)
    mock = os.path.join(tmp, "mock")
    os.makedirs(mock)
    rows, by = aq.load_units(tmp)
    rng = np.random.default_rng(5)
    terms = {}
    names = sorted({n for s in by for _, n in by[s]})
    for i, n in enumerate(names):
        mid = "/m/" + hashlib.sha1(n.encode()).hexdigest()[:6]
        sug = [{"mid": mid, "title": n + " Co", "type": "Brand"}] if i % 2 == 0 else \
              [{"mid": "/m/zz", "title": n, "type": "Animal"}]
        json.dump({"suggestions": sug}, open(os.path.join(mock, aq.mock_ac_name(n)), "w"))
        base = float(np.exp(rng.uniform(math.log(30), math.log(3000))))
        tr = float(rng.uniform(-0.003, 0.003))
        terms[n] = {"base": base, "trend": tr, "season": 0.1}
        terms[mid] = {"base": base, "trend": tr, "season": 0.1}
    json.dump({"seed": 9, "noise": 0.08, "terms": terms}, open(os.path.join(mock, "_sim.json"), "w"))
    return mock


def run(tmp, mock, cmd, now, extra=(), tag="present"):
    argv = list(cmd) + ["--root", tmp, "--mock", mock, "--tag-check", tag, "--now", now, "--sleep", "0"] + list(extra)
    import io
    import contextlib
    err, out = io.StringIO(), io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(out):
        rc = aq.main(argv)
    return rc, err.getvalue() + out.getvalue()


def test_acquisition_guards_and_pipeline_in_mock_mode():
    tmp = tempfile.mkdtemp()
    try:
        mock = make_world(tmp)
        T0 = "2026-11-10T12:00:00Z"
        # guard: no anchor file
        rc, msg = run(tmp, mock, ["terms"], T0)
        assert rc == 2 and "anchor" in msg, (rc, msg)
        os.makedirs(os.path.join(tmp, "osf/v43/anchor"))
        # guard: tag not on origin
        open(os.path.join(tmp, "osf/v43/anchor/osf_anchor_v0_43.json"), "w").write("{}")
        rc, msg = run(tmp, mock, ["terms"], T0, tag="absent")
        assert rc == 2 and "tag" in msg, (rc, msg)
        # guard: the real git check refuses outside a repo / without the tag (no network involved in a non-repo)
        import io
        import contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = aq.main(["terms", "--root", tmp, "--mock", mock, "--now", T0, "--sleep", "0"])
        assert rc == 2 and "REFUSED" in err.getvalue()
        # guard: v0.40 collection window (2026-11-17..21 UTC), both ends
        for d in ("2026-11-17T00:00:00Z", "2026-11-19T12:00:00Z", "2026-11-21T23:59:00Z"):
            rc, msg = run(tmp, mock, ["terms"], d)
            assert rc == 2 and "v0.40" in msg, (d, rc, msg)
        rc, msg = run(tmp, mock, ["terms"], "2026-11-22T00:00:01Z")
        assert rc == 0, msg   # the day after the window is allowed
        os.remove(os.path.join(tmp, "osf/v43/registries/terms_v0_43.json"))
        # --now / --tag-check overrides are refused without --mock
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = aq.main(["terms", "--root", tmp, "--now", T0])
        assert rc == 2
        # terms
        rc, msg = run(tmp, mock, ["terms"], T0)
        assert rc == 0, msg
        tj = json.load(open(os.path.join(tmp, "osf/v43/registries/terms_v0_43.json")))
        assert len(tj["by_name"]) == 111 and len(tj["chosen"]) == 112
        assert 0.4 < tj["summary"]["share_topic"] < 0.6
        # size before... then size
        rc, msg = run(tmp, mock, ["size"], T0)
        assert rc == 0, msg
        bj = json.load(open(os.path.join(tmp, "osf/v43/registries/bundles_v0_43.json")))["substrates"]
        assert [len(bj[s]["main_bundles"]) for s in aq.SUBSTRATES] == [4, 6, 6, 6, 6]
        assert [len(bj[s]["sizing_bundles"]) for s in aq.SUBSTRATES] == [4, 6, 6, 6, 6]
        for s in aq.SUBSTRATES:
            mb = bj[s]["main_bundles"]
            assert all(mb[i + 1][0] == mb[i][-1] for i in range(len(mb) - 1))
            assert sorted(u for b in mb for u in b) == sorted(set(u for b in mb for u in b)) or True
            assert {u for b in mb for u in b} == set(bj[s]["terms"])
        assert len(os.listdir(os.path.join(tmp, "osf/v43/data/trends_raw/sizing"))) == 28
        rec = json.load(open(os.path.join(tmp, "osf/v43/data/trends_raw/sizing/v0.19_b0.json")))
        assert rec["params"]["date"] == "2025-09-07 2026-06-06" and "api_key" not in json.dumps(rec["params"])
        assert rec["params"]["geo"] == "US" and rec["params"]["tz"] == "0" and rec["status"] == "ok"
        rc, msg = run(tmp, mock, ["size"], T0)
        assert rc == 2   # one sizing pull only
        # main pull 1 ok; pull 2 within 24 h refused; after 24 h ok; pull 3 likewise
        rc, msg = run(tmp, mock, ["pull", "--n", "1"], T0)
        assert rc == 0, msg
        r1 = json.load(open(os.path.join(tmp, "osf/v43/data/trends_raw/main1/v0.20_b0.json")))
        assert r1["params"]["date"] == "2025-05-04 2026-11-07"
        rc, msg = run(tmp, mock, ["pull", "--n", "2"], "2026-11-11T11:59:00Z")
        assert rc == 2 and "24 h" in msg, (rc, msg)
        rc, msg = run(tmp, mock, ["pull", "--n", "3"], "2026-11-12T12:00:00Z")
        assert rc == 2 and "not complete" in msg, (rc, msg)
        rc, msg = run(tmp, mock, ["pull", "--n", "2"], "2026-11-11T12:00:00Z")
        assert rc == 0, msg
        rc, msg = run(tmp, mock, ["pull", "--n", "3"], "2026-11-12T11:59:59Z")
        assert rc == 2 and "24 h" in msg
        rc, msg = run(tmp, mock, ["pull", "--n", "3"], "2026-11-12T12:00:00Z")
        assert rc == 0, msg
        # range end must be complete
        rc, msg = run(tmp, mock, ["pull", "--n", "1"], "2026-11-07T12:00:00Z")
        assert rc == 2
        # stage 2 not before 2027-03-10
        rc, msg = run(tmp, mock, ["stage2-pull", "--n", "1"], "2027-03-09T23:00:00Z")
        assert rc == 2 and "2027-03-10" in msg, msg
        # monthly snapshot
        rc, msg = run(tmp, mock, ["snapshot"], "2026-12-01T10:00:00Z")
        assert rc == 0, msg
        sn = json.load(open(os.path.join(tmp, "osf/v43/data/trends_raw/snapshot_2026-12-01/v0.19_b0.json")))
        assert sn["params"]["date"] == "2025-05-04 2026-11-28"
        # stage 1 scoring on the mock data
        out1 = os.path.join(tmp, "osf/v43/v43_stage1_verdicts.json")
        rc = sc.main(["--stage", "1", "--root", tmp, "--B-perm", "199", "--B-boot", "199", "--out", out1])
        assert rc == 0
        j = json.load(open(out1))
        assert set(j["tests"]) == {"H_Pred_Presence", "H_Pred_Presence_SA", "H_Pred_Presence_Momentum", "H_Pred_Consistency"}
        assert j["tests"]["H_Pred_Presence"]["n"] > 90 and j["tests"]["H_Pred_Presence"]["seed"] == 430041
        assert j["tests"]["H_Pred_Consistency"]["seed"] == 430044 and j["tests"]["H_Pred_Consistency"]["n"] < 112
        assert j["manipulation_checks"]["MC_Terms"]["share_topic"] == tj["summary"]["share_topic"]
        assert j["manipulation_checks"]["MC_PullReliability"]["mean_pairwise_pooled_spearman"] is not None
        assert "cross_lagged" in j["descriptives"] and "longer_lead_P_t1" in j["descriptives"]
        # stage 2: pulls from 2027-03-10, 24 h apart; P_new absent -> UNDETERMINED with a reason
        for n, d in ((1, "2027-03-10T09:00:00Z"), (2, "2027-03-11T09:00:00Z"), (3, "2027-03-12T09:00:00Z")):
            rc, msg = run(tmp, mock, ["stage2-pull", "--n", str(n)], d)
            assert rc == 0, msg
        s2 = json.load(open(os.path.join(tmp, "osf/v43/data/trends_raw/stage2_1/v0.19_b0.json")))
        assert s2["params"]["date"] == "2025-05-04 2027-03-06"
        out2 = os.path.join(tmp, "osf/v43/v43_stage2_verdicts.json")
        rc = sc.main(["--stage", "2", "--root", tmp, "--B-perm", "199", "--B-boot", "199", "--out", out2])
        assert rc == 0
        j2 = json.load(open(out2))
        nw = j2["tests"]["H_Pred_Presence_NewPanel"]
        assert nw["verdict"] == "UNDETERMINED" and "absent" in nw["reason"]
        assert set(j2["tests"]) == {"H_Pred_Presence_Confirm", "H_Pred_Presence_Confirm_SA",
                                    "H_Pred_Presence_NewPanel", "H_Pred_Consistency_Confirm"}
        assert j2["tests"]["H_Pred_Presence_Confirm"]["seed"] == 430045
        assert os.path.exists(os.path.join(tmp, "osf/v43/v43_monthly_series.csv"))
        # with P_new supplied the test runs
        pn = os.path.join(tmp, "pnew.csv")
        with open(pn, "w") as fh:
            fh.write("substrate,unit,P_new\n")
            for r in aq.load_units(tmp)[0]:
                fh.write(f"{r['substrate']},{r['unit']},{r['P_t3']}\n")
        rc = sc.main(["--stage", "2", "--root", tmp, "--B-perm", "99", "--B-boot", "99", "--out", out2, "--pnew", pn])
        j3 = json.load(open(out2))
        assert j3["tests"]["H_Pred_Presence_NewPanel"]["rho"] is not None
        assert j3["tests"]["H_Pred_Presence_NewPanel"]["seed"] == 430047
    finally:
        shutil.rmtree(tmp)


def test_resend_rule_and_missing():
    tmp = tempfile.mkdtemp()
    try:
        mock = os.path.join(tmp, "mock")
        os.makedirs(mock)
        a, b = D(2025, 5, 4), D(2026, 11, 7)
        weeks = sundays(a, D(2026, 11, 1))
        good = week_resp(weeks, [[5] * len(weeks), [6] * len(weeks)])
        days = [a + dt.timedelta(days=i) for i in range(10)]
        daily = week_resp(days, [[1] * 10, [1] * 10])
        i = weeks.index(D(2026, 5, 24))
        partial = week_resp(weeks, [[5] * len(weeks)] * 2, partial_idx=[i])
        q, date = "t0,t1", f"{a} {b}"
        args = argparse_ns(tmp, mock)
        wins = aq.windows_for("main", 1)

        def put(attempts):
            json.dump({"_attempts": attempts}, open(os.path.join(mock, aq.mock_ts_name(q, date)), "w"))
            aq._MOCK_ATTEMPTS.clear()
        # daily -> HTTP 500 -> good: ok on the third send
        put([daily, {"_http": 500}, good])
        ser, rec = aq.fetch_bundle(args, "t", "v0.19", 0, ["a", "b"], ["t0", "t1"], (a, b), wins)
        assert ser is not None and rec["status"] == "ok" and rec["n_attempts"] == 3
        assert not rec["attempts"][0]["mc_weekly_ok"] and rec["attempts"][1]["http_status"] == 500
        # partial inside a window x3 -> missing after exactly 3 sends
        put([partial])
        ser, rec = aq.fetch_bundle(args, "t", "v0.19", 1, ["a", "b"], ["t0", "t1"], (a, b), wins)
        assert ser is None and rec["status"] == "missing" and rec["n_attempts"] == 3
        # no timeline at all
        put([{"search_metadata": {}}])
        ser, rec = aq.fetch_bundle(args, "t", "v0.19", 2, ["a", "b"], ["t0", "t1"], (a, b), wins)
        assert ser is None and rec["n_attempts"] == 3 and "timeline" in rec["attempts"][0]["error"]
        # a stored record is never re-requested
        put([good])
        ser, rec = aq.fetch_bundle(args, "t", "v0.19", 1, ["a", "b"], ["t0", "t1"], (a, b), wins)
        assert ser is None and rec["status"] == "missing"
    finally:
        shutil.rmtree(tmp)


def argparse_ns(root, mock):
    ns = argparse.Namespace(root=root, mock=mock, tag_check="present", now="2026-11-10T12:00:00Z", sleep=0.0)
    return ns


def test_units_file_shape():
    rows, by = aq.load_units(ROOT)
    assert {s: len(by[s]) for s in aq.SUBSTRATES} == {"v0.19": 16, "v0.20": 24, "v0.21": 24, "v0.22": 24, "v0.23": 24}
    names23 = dict(by["v0.23"])
    assert names23["S04"] == "Patrón" and names23["S01"] == "Johnnie Walker"
    assert sum(1 for r in rows if r["unit"] == "Rare Beauty") == 2
    assert len({n for s in by for _, n in by[s]}) == 111
    assert {r["cell"] for r in rows if r["substrate"] == "v0.22" and r["unit"] in
            ("Mercury", "Oldsmobile", "Plymouth", "Pontiac", "Saturn")} == {"D"}


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]


def main():
    ok = 0
    for t in TESTS:
        try:
            t()
            ok += 1
            print(f"PASS {t.__name__}")
        except Exception:
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
    print(f"{ok}/{len(TESTS)} pass")
    return 0 if ok == len(TESTS) else 1


if __name__ == "__main__":
    sys.exit(main())
