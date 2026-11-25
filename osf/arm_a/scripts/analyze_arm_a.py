#!/usr/bin/env python3
"""Arm A analysis: H_A1-H_A7, Holm families, S-COI, flagged-month robustness and R1-domain sensitivity
(pre-registration r4, sections 2.1-2.13, 6.1-6.7). Reads only the join's outputs and the registries; no API call.

Before the lock this runs only on simulated Google data (scripts/dry_run_arm_a.py); after the lock, on the pulls.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import join_arm_a as J      # noqa: E402
import params_arm_a as P    # noqa: E402
import stats_arm_a as S     # noqa: E402

CATS_A1 = ("cars", "airlines", "banks", "software")
W = {"t1": (2026, 5), "pre_end": (2026, 2), "post": (2026, 11), "placebo_start": (2025, 1), "pull3_end": (2027, 2)}
YEAR_2025 = [(2025, m) for m in range(1, 13)]
PRE_PERIOD = [J.ym_add((2024, 11), k) for k in range(16)]          # Nov 2024 .. Feb 2026


def nanless(v):
    return v is not None and not (isinstance(v, float) and math.isnan(v))


class Inputs:
    """AI-side and sales inputs (registries) plus the Google panels by pull."""

    def __init__(self, panels, presence, shift, sales=None, domains=None, exclude=(), role="primary",
                 flagged_drop=False):
        self.panels = panels                      # {pull: (panel, status, pull_month)}
        self.presence = presence                  # {(category, brand_id, wave): P}
        self.shift = shift                        # {brand_id: {"group", "m_rec", "sales_usd"}}
        self.sales = sales or {}                  # {brand_id: value} for airlines, banks, software
        self.domains = domains if domains is not None else J.load_domains()
        self.exclude = set(exclude)
        self.bd = J.brand_domains(self.domains, role)
        self.cat_of = {b: c for b, (c, _) in self.bd.items()}
        self.flagged = {}
        for pull, (panel, _s, _m) in panels.items():
            fl = J.break_flags(panel)
            self.flagged[pull] = frozenset(ym for ym, v in fl.items() if v["flagged"]) if flagged_drop else frozenset()

    def series(self, pull, brand):
        if brand in self.exclude or brand not in self.bd or pull not in self.panels:
            return None
        return self.panels[pull][0].get(self.bd[brand][1])

    def gbar(self, pull, brand, end, measure="g", windows_for_usable=None):
        s = self.series(pull, brand)
        if s is None:
            return None
        ends = windows_for_usable or [end]
        if not J.usable(s, [J.window(e) for e in ends]):
            return None
        return J.window_mean(s, end, measure, self.flagged[pull], all_months=sorted(s))

    def brands(self, category):
        return sorted(b for b, c in self.cat_of.items() if c == category and b not in self.exclude)

    def P(self, category, brand, wave):
        return self.presence.get((category, brand, wave))


def load_presence(path=None):
    out = {}
    with open(path or (P.REG / "arm_a_presence_r1.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[(r["category"], r["brand_id"], r["wave"])] = float(r["P"])
    return out


def load_shift(path=None):
    with open(path or (P.REG / "arm_a_shift_r1.csv"), newline="", encoding="utf-8") as f:
        return {r["brand_id"]: {"group": r["group"], "m_rec": int(r["m_rec"]), "sales_usd": float(r["sales_usd"])}
                for r in csv.DictReader(f)}


# --- H_A1 ------------------------------------------------------------------------------------------------------------
def a1_data(I, measure="g", pull=1):
    data = {}
    for c in CATS_A1:
        wave = P.CATEGORY_WAVE[c]
        end = P.WAVE_MONTH[wave]
        xs, ys, ids = [], [], []
        for b in I.brands(c):
            p = I.P(c, b, wave)
            g = I.gbar(pull, b, end, measure)
            if nanless(p) and nanless(g):
                xs.append(p), ys.append(g), ids.append(b)
        data[c] = (np.array(xs), np.array(ys), ids)
    return data


def pooled_rho(data):
    cats = [c for c, (x, _y, _i) in data.items() if len(x) >= P.MIN_POOL_N]
    rhos = {c: S.spearman(data[c][0], data[c][1]) for c in data if len(data[c][0]) >= 3}
    use = [c for c in cats if nanless(rhos.get(c))]
    pooled = S.fisher_pool([rhos[c] for c in use], [len(data[c][0]) for c in use]) if use else float("nan")
    return pooled, rhos, use


def h_a1(I, n_perm=P.N_PERM, n_boot=P.N_BOOT, measure="g", seed=P.SEEDS["H_A1"]):
    data = a1_data(I, measure)
    obs, rhos, use = pooled_rho(data)
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_perm):
        d2 = {c: (rng.permutation(x), y, i) for c, (x, y, i) in data.items()}
        null.append(pooled_rho(d2)[0])
    p = S.perm_p(obs, null) if nanless(obs) else None
    rngb = np.random.default_rng(P.SEEDS["boot_A1"])
    boots = []
    for _ in range(n_boot):
        d2 = {}
        for c, (x, y, i) in data.items():
            k = rngb.integers(0, len(x), len(x)) if len(x) else np.array([], int)
            d2[c] = (x[k], y[k], i)
        boots.append(pooled_rho(d2)[0])
    ci = S.percentile_ci(boots)
    return {"rho_bar": obs, "rho_c": rhos, "n_c": {c: len(v[0]) for c, v in data.items()}, "pooled_categories": use,
            "p": p, "ci95": ci, "analysable_categories": len(use)}


def verdict_a1(r, p_holm):
    if r["analysable_categories"] < P.MIN_CATEGORIES_A1 or p_holm is None:
        return "UNDETERMINED"
    if r["rho_bar"] >= P.THRESHOLD and p_holm < P.ALPHA:
        return "CONFIRMED"
    if r["ci95"][1] < P.THRESHOLD:
        return "FALSIFIED"
    if p_holm < P.ALPHA:
        return "MARGINAL"
    return "UNDETERMINED"


# --- H_A2, H_A3 (cars, t1) -----------------------------------------------------------------------------------------
def cars_t1(I, pull=1):
    """Analysable car brands with m (mentions), S (2025 sales) and the mean monthly 2025 etv (Gs basis)."""
    out = []
    for b in I.brands("cars"):
        sh = I.shift.get(b)
        s = I.series(pull, b)
        if sh is None or s is None or not J.usable(s, [YEAR_2025]):
            continue
        vals = [s[ym]["etv"] for ym in YEAR_2025 if ym in s]
        g = sum(vals) / len(vals)
        if g <= 0 or sh["sales_usd"] <= 0:
            continue
        out.append({"brand_id": b, "group": sh["group"], "m": sh["m_rec"], "S": sh["sales_usd"], "G": g})
    return out


def fl_test(y, x, z, groups, n_perm, seed, per_group=False):
    """Freedman-Lane: reduced model y ~ z, residuals permuted within group, partial corr of y* with x given z."""
    obs = S.partial_corr(y, x, z)
    e, fit = S.residuals(y, S.design(z, groups, per_group))
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_perm):
        k = S.within_group_permutation(rng, groups)
        null.append(S.partial_corr(fit + e[k], x, z))
    undefined = sum(1 for v in null if math.isnan(v))
    return obs, S.perm_p(obs, null), undefined


def h_a2(I, n_perm=P.N_PERM, seed=P.SEEDS["H_A2"]):
    rows = cars_t1(I)
    if len(rows) < 4:
        return {"n": len(rows), "partial_r": None, "p": None}
    groups = [r["group"] for r in rows]

    def logs(off):
        r = S.centre_within(np.log(np.array([x["m"] for x in rows], float) + off), groups)
        s = S.centre_within(np.log([x["S"] for x in rows]), groups)
        gs = S.centre_within(np.log([x["G"] for x in rows]), groups)
        return r, s, gs

    r, s, gs = logs(P.ZERO_OFFSET)
    obs, p, und = fl_test(r, s, gs, groups, n_perm, seed)
    out = {"n": len(rows), "partial_r": obs, "p": p, "groups": {g: groups.count(g) for g in set(groups)}}
    sens = {}
    rk = [S.norm_ranks_within([x[k] for x in rows], groups) for k in ("m", "S", "G")]
    o, pp, u = fl_test(rk[0], rk[1], rk[2], groups, n_perm, seed)
    sens["i_ranks"] = {"partial": o, "p": pp, "undefined_perms": u}
    o, pp, u = fl_test(r, s, gs, groups, n_perm, seed, per_group=True)
    sens["ii_per_group_slopes"] = {"partial": o, "p": pp}
    for off in P.ZERO_OFFSETS_SENS:
        r2, s2, g2 = logs(off)
        o, pp, u = fl_test(r2, s2, g2, groups, n_perm, seed)
        sens[f"iii_offset_{off}"] = {"partial": o, "p": pp}
    out["sensitivity"] = sens
    out["headline"] = headline_pair(rows)
    return out


def headline_pair(rows):
    """Of the brands whose AI share exceeds their Google share within group, the share whose sales share exceeds
    their Google share, against the same share for the other brands (section 2.3)."""
    tot = {}
    for x in rows:
        t = tot.setdefault(x["group"], {"m": 0, "S": 0.0, "G": 0.0})
        t["m"] += x["m"]; t["S"] += x["S"]; t["G"] += x["G"]
    ai_over, other = [], []
    for x in rows:
        t = tot[x["group"]]
        r_sh = x["m"] / t["m"] if t["m"] else 0.0
        (ai_over if r_sh > x["G"] / t["G"] else other).append(x["S"] / t["S"] > x["G"] / t["G"])
    frac = lambda v: (sum(v) / len(v)) if v else None   # noqa: E731
    return {"ai_over_google": {"n": len(ai_over), "share_sales_over_google": frac(ai_over)},
            "other": {"n": len(other), "share_sales_over_google": frac(other)}}


def verdict_a2(r, p_holm):
    if r.get("partial_r") is None or p_holm is None:
        return "UNDETERMINED"
    if r["partial_r"] >= P.THRESHOLD and p_holm < P.ALPHA:
        return "CONFIRMED"
    if r["partial_r"] <= 0:
        return "FALSIFIED"
    return "UNDETERMINED"


def h_a3(I, n_boot=P.N_BOOT, seed=P.SEEDS["boot_A3"]):
    rows = cars_t1(I)
    groups = [r["group"] for r in rows]

    def stat(rs, gr):
        rk = {k: S.norm_ranks_within([x[k] for x in rs], gr) for k in ("m", "S", "G")}
        a, b = S.pearson(rk["G"], rk["S"]), S.pearson(rk["m"], rk["S"])
        return a, b, a - b

    a, b, d = stat(rows, groups)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        rs = []
        for g in sorted(set(groups)):
            pos = [i for i, gg in enumerate(groups) if gg == g]
            rs += [rows[i] for i in rng.choice(pos, len(pos), replace=True)]
        boots.append(stat(rs, [x["group"] for x in rs])[2])
    ci = S.percentile_ci(boots)
    bb = np.array([v for v in boots if not math.isnan(v)])
    p = min(1.0, 2 * min((bb <= 0).mean(), (bb >= 0).mean())) if len(bb) else None
    if ci[0] > 0:
        v = "Google tracks sales better"
    elif ci[1] < 0:
        v = "AI tracks sales better"
    else:
        v = "no difference detected"
    return {"rho_Gs_S": a, "rho_R_S": b, "diff": d, "ci95": ci, "p_boot_two_sided": p, "reading": v,
            "n": len(rows)}


# --- H_A4, H_A5 (cars, pull 1) ---------------------------------------------------------------------------------------
def car_changes(I, end_a, end_b, pull=1):
    """Category-demeaned dg between the window ending end_a and the window ending end_b, per car brand."""
    raw = {}
    for b in I.brands("cars"):
        ga = I.gbar(pull, b, end_a, windows_for_usable=[end_a, end_b])
        gb = I.gbar(pull, b, end_b, windows_for_usable=[end_a, end_b])
        raw[b] = (gb - ga) if nanless(ga) and nanless(gb) else None
    return {b: v for b, v in J.demeaned_change(raw, {b: "cars" for b in raw}).items() if v is not None}


def terciles(scores):
    """Bands 0 (bottom), 1 (middle), 2 (top) by score; ties broken by brand ID; extras go to the middle band."""
    order = sorted(scores, key=lambda b: (scores[b], b))
    n, k = len(order), len(order) // 3
    return {b: (0 if i < k else (2 if i >= n - k else 1)) for i, b in enumerate(order)}


def spread(outcome, band, ids):
    top = [outcome[b] for b in ids if band[b] == 2]
    bot = [outcome[b] for b in ids if band[b] == 0]
    return (sum(top) / len(top) - sum(bot) / len(bot)) if top and bot else float("nan")


def h_a4(I, n_perm=P.N_PERM, n_boot=P.N_BOOT, seed=P.SEEDS["H_A4"]):
    out_ = car_changes(I, W["t1"], W["post"])
    pres = {b: I.P("cars", b, "t1") for b in out_ if nanless(I.P("cars", b, "t1"))}
    ids = sorted(pres)
    if len(ids) < 6:
        return {"n": len(ids), "p": None}
    band = terciles(pres)
    vals = lambda o, bd: [[o[b] for b in ids if bd[b] == k] for k in range(3)]   # noqa: E731
    J_obs = S.jonckheere(vals(out_, band))
    rng = np.random.default_rng(seed)
    y = np.array([out_[b] for b in ids])
    null = []
    for _ in range(n_perm):
        yp = dict(zip(ids, rng.permutation(y)))
        null.append(S.jonckheere(vals(yp, band)))
    p = S.perm_p(J_obs, null)
    means = [float(np.mean(v)) for v in vals(out_, band)]
    med = float(np.median(y))
    hit = float(np.mean([out_[b] > med for b in ids if band[b] == 2]))
    # reversion baseline (a): bands by own pre-period Google level
    pre = {}
    for b in ids:
        s = I.series(1, b)
        v = [s[ym]["g"] for ym in PRE_PERIOD if s and ym in s]
        if len(v) * 2 > len(PRE_PERIOD):
            pre[b] = sum(v) / len(v)
    band_a = terciles(pre) if len(pre) == len(ids) else None
    # placebo (b): t1 bands against the past change, Nov 2024-Jan 2025 -> Mar-May 2026
    past = car_changes(I, W["placebo_start"], W["t1"])
    rngb = np.random.default_rng(P.SEEDS["boot_A4"])
    bs, bd_, bp = [], [], []
    for _ in range(n_boot):
        k = list(rngb.choice(ids, len(ids), replace=True))
        sp = spread(out_, band, k)
        bs.append(sp)
        if band_a:
            bd_.append(sp - spread(out_, band_a, k))
        if all(b in past for b in k):
            bp.append(spread(past, band, k))
    sp_obs = spread(out_, band, ids)
    res = {"n": len(ids), "J": J_obs, "p": p, "band_means": means, "best_band": int(np.argmax(means)),
           "spread": sp_obs, "spread_ci95": S.percentile_ci(bs), "hit_rate_top": hit,
           "band_n": [sum(1 for b in ids if band[b] == k) for k in range(3)]}
    res["baseline_a"] = ({"spread": spread(out_, band_a, ids), "diff": sp_obs - spread(out_, band_a, ids),
                          "diff_ci95": S.percentile_ci(bd_)} if band_a else None)
    res["placebo_b"] = ({"spread": spread(past, band, [b for b in ids if b in past]),
                         "spread_ci95": S.percentile_ci(bp)} if past else None)
    return res


def verdict_a4(r, p_holm):
    if r.get("p") is None or p_holm is None:
        return "NOT SUPPORTED"
    rise = p_holm < P.ALPHA
    beats = r["baseline_a"] is not None and r["baseline_a"]["diff_ci95"][0] > 0
    if rise and r["spread_ci95"][0] > 0 and beats and r["best_band"] == 2:
        v = "SUPPORTED"
    elif rise:
        v = "PARTIAL"
    else:
        v = "NOT SUPPORTED"
    if r["placebo_b"] and r["placebo_b"]["spread_ci95"][0] > 0 and v != "NOT SUPPORTED":
        v += " (not distinguishable from trend)"
    return v


def change_test(dP, dg, n_perm, seed):
    ids = sorted(set(dP) & set(dg))
    if len(ids) < 4:
        return {"n": len(ids), "rho": None, "p": None}
    x, y = np.array([dP[b] for b in ids]), np.array([dg[b] for b in ids])
    rho = S.spearman(x, y)
    rng = np.random.default_rng(seed)
    null = [S.spearman(rng.permutation(x), y) for _ in range(n_perm)]
    return {"n": len(ids), "rho": rho, "p": S.perm_p(rho, null)}


def h_a5(I, n_perm=P.N_PERM, seed=P.SEEDS["H_A5"]):
    dg = car_changes(I, W["t1"], W["post"])
    dP = {b: I.P("cars", b, "t3") - I.P("cars", b, "t1") for b in I.brands("cars")
          if nanless(I.P("cars", b, "t3")) and nanless(I.P("cars", b, "t1"))}
    return change_test(dP, dg, n_perm, seed)


def verdict_change(r, p_holm):
    return "SUPPORTED" if r.get("rho") is not None and r["rho"] > 0 and p_holm is not None and p_holm < P.ALPHA \
        else "NOT SUPPORTED"


# --- H_A6 (airlines, banks, software), H_A7 (cars, pull 3) ---------------------------------------------------------
def h_a6(I, category, n_perm=P.N_PERM, seed=P.SEEDS["H_A6"]):
    wave = P.CATEGORY_WAVE[category]
    end = P.WAVE_MONTH[wave]
    rows = []
    for b in I.brands(category):
        p, g, s = I.P(category, b, wave), I.gbar(1, b, end), I.sales.get(b)
        if nanless(p) and nanless(g) and nanless(s) and s > 0:
            rows.append((b, p, g, s))
    if len(rows) < 5:
        return {"category": category, "n": len(rows), "partial": None, "p": None}
    _, p, g, s = (np.array(v) for v in zip(*rows))
    rp, rg, rs = S.rankdata(p), S.rankdata(g), S.rankdata(s)
    obs, pv, und = fl_test(rp, rs, rg, ["all"] * len(rows), n_perm, seed)
    return {"category": category, "n": len(rows), "rho_g_sales": S.spearman(g, s), "rho_P_sales": S.spearman(p, s),
            "partial": obs, "p": pv}


def h_a7(I, n_perm=P.N_PERM, seed=P.SEEDS["H_A7"], t6_same_panel=None, t6_collected_by_deadline=None):
    """Primary: dP (t6 - t4) against demeaned dg (Dec 2026-Feb 2027 window minus Sep-Nov 2026 window), pull 3."""
    dg = car_changes(I, W["post"], W["pull3_end"], pull=3) if 3 in I.panels else {}
    have_t6 = any(k[2] == "t6" for k in I.presence)
    if not (have_t6 and t6_same_panel and t6_collected_by_deadline) or not dg:
        dg5 = car_changes(I, W["post"], (2026, 12), pull=3) if 3 in I.panels else {}
        dP5 = {b: I.P("cars", b, "t5") - I.P("cars", b, "t4") for b in I.brands("cars")
               if nanless(I.P("cars", b, "t5")) and nanless(I.P("cars", b, "t4"))}
        return {"status": "UNDETERMINED", "p": None, "rho": None,
                "exploratory_t4_t5": change_test(dP5, dg5, n_perm, seed) if dP5 and dg5 else None}
    dP = {b: I.P("cars", b, "t6") - I.P("cars", b, "t4") for b in I.brands("cars")
          if nanless(I.P("cars", b, "t6")) and nanless(I.P("cars", b, "t4"))}
    r = change_test(dP, dg, n_perm, seed)
    r["status"] = "TESTED"
    return r


# --- all tests, Holm families, S-COI and robustness ----------------------------------------------------------------
def run_tests(I, n_perm=P.N_PERM, n_boot=P.N_BOOT, confirmatory_a6=("airlines", "banks", "software"), a7_opts=None):
    a7_opts = a7_opts or {}
    R = {"H_A1": h_a1(I, n_perm, n_boot), "H_A2": h_a2(I, n_perm), "H_A3": h_a3(I, n_boot),
         "H_A4": h_a4(I, n_perm, n_boot), "H_A5": h_a5(I, n_perm), "H_A7": h_a7(I, n_perm, **a7_opts)}
    R["H_A6"] = {c: h_a6(I, c, n_perm) for c in ("airlines", "banks", "software")}
    prim = S.holm([R["H_A1"]["p"], R["H_A2"]["p"]])
    sec_keys = ["H_A3", "H_A4", "H_A5", "H_A7"] + [f"H_A6_{c}" for c in confirmatory_a6]
    sec_p = [R["H_A3"]["p_boot_two_sided"], R["H_A4"].get("p"), R["H_A5"].get("p"), R["H_A7"].get("p")] + \
            [R["H_A6"][c]["p"] for c in confirmatory_a6]
    sec = dict(zip(sec_keys, S.holm(sec_p)))
    V = {"H_A1": verdict_a1(R["H_A1"], prim[0]), "H_A2": verdict_a2(R["H_A2"], prim[1]),
         "H_A3": R["H_A3"]["reading"], "H_A4": verdict_a4(R["H_A4"], sec["H_A4"]),
         "H_A5": verdict_change(R["H_A5"], sec["H_A5"]),
         "H_A7": "UNDETERMINED" if R["H_A7"]["status"] != "TESTED" else verdict_change(R["H_A7"], sec["H_A7"])}
    for c in confirmatory_a6:
        r = R["H_A6"][c]
        V[f"H_A6_{c}"] = ("SUPPORTED" if r["partial"] is not None and r["partial"] > 0 and sec[f"H_A6_{c}"] is not None
                          and sec[f"H_A6_{c}"] < P.ALPHA else "NOT SUPPORTED")
    return {"results": R, "holm_primary": {"H_A1": prim[0], "H_A2": prim[1]}, "holm_secondary": sec, "verdicts": V}


def analyse(panels, presence, shift, sales=None, n_perm=P.N_PERM, n_boot=P.N_BOOT, a7_opts=None, domains=None):
    """Pre-registered results plus the declared checks (no verdict): S-COI, flagged months dropped, R1 domains."""
    base = Inputs(panels, presence, shift, sales, domains)
    out = {"primary": run_tests(base, n_perm, n_boot, a7_opts=a7_opts), "size_weighted_A1": size_weighted_a1(base)}
    for label, kw in (("S-COI", {"exclude": P.COI_FLAGGED}), ("flagged_months_dropped", {"flagged_drop": True}),
                      ("R1_domains", {"role": "sensitivity"})):
        I = Inputs(panels, presence, shift, sales, domains, **kw)
        out[label] = run_tests(I, n_perm, n_boot, a7_opts=a7_opts)
        out[label]["label"] = "robustness or sensitivity; no verdict"
    out["break_flags"] = {pull: {f"{y}-{m:02d}": v for (y, m), v in J.break_flags(pn).items() if v["flagged"]}
                          for pull, (pn, _s, _m) in panels.items()}
    if 1 in panels and 3 in panels:
        out["restatement_pull1_pull3"] = J.restatement(panels[1][0], panels[3][0])
    return out


def size_weighted_a1(I, sales_cars=None):
    """Section 2.7: H_A1's within-category rho weighted by the sales measure (cars: 2025 sales; others: their
    measure), else by the brand's pre-period mean etv. Reported beside the equal-weighted result; no test."""
    data = a1_data(I)
    out = {}
    for c, (x, y, ids) in data.items():
        if len(x) < 3:
            continue
        w = []
        for b in ids:
            v = I.shift[b]["sales_usd"] if c == "cars" and b in I.shift else I.sales.get(b)
            if not nanless(v):
                s = I.series(1, b) or {}
                pv = [s[ym]["etv"] for ym in PRE_PERIOD if ym in s]
                v = sum(pv) / len(pv) if pv else None
            w.append(v)
        if all(nanless(v) and v > 0 for v in w):
            out[c] = S.weighted_spearman(x, y, w)
    return out


def load_sales(path=None):
    path = Path(path or (P.DATA / "sales" / "arm_a_sales_values.csv"))
    if not path.exists():
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r["brand_id"]: float(r["value"]) for r in csv.DictReader(f)}


def main(argv=None):
    """After the lock and the pulls: python3 osf/arm_a/scripts/analyze_arm_a.py [--t6-same-panel] [--t6-by-deadline]"""
    import argparse
    import json
    ap = argparse.ArgumentParser()
    ap.add_argument("--t6-same-panel", action="store_true")
    ap.add_argument("--t6-by-deadline", action="store_true")
    a = ap.parse_args(argv)
    if not P.ANCHOR.exists():
        print("REFUSED: no lock anchor; before the lock only scripts/dry_run_arm_a.py (simulated data) runs")
        return 2
    pulls = [p for p in P.PULLS if (P.RAW / f"pull{p}" / f"manifest_pull{p}.csv").exists()]
    for p in pulls:                                    # section 6.2: flags first, before any AIAS variable is joined
        if not (P.RAW / f"pull{p}" / f"break_flags_pull{p}.json").exists():
            J.write_flags(p)
    panels = {p: J.load_pull(p) for p in pulls}
    res = analyse(panels, load_presence(), load_shift(), load_sales(),
                  a7_opts={"t6_same_panel": a.t6_same_panel, "t6_collected_by_deadline": a.t6_by_deadline})
    out = P.ARM / "arm_a_verdicts.json"
    out.write_text(json.dumps(res, indent=1, default=str) + "\n", encoding="utf-8")
    print(json.dumps(res["primary"]["verdicts"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
