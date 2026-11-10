#!/usr/bin/env python3
"""Shared Google Trends utilities for AIAS v0.43 (PRE_REGISTRATION_v0_43.md s2.1, s4, s5).

Weeks are Google Trends weeks, Sunday-Saturday, identified by their Sunday start date.
W(e) = the four complete weeks ending on Saturday e.
"""
import datetime as dt
import json
import math
import unicodedata
import re

D = dt.date

# ----------------------------------------------------------------------------- schedule
STAGES = {
    1: {"prior": D(2026, 2, 7), "base": D(2026, 6, 6), "end": D(2026, 11, 7),
        "range": (D(2025, 5, 4), D(2026, 11, 7))},
    2: {"prior": None, "base": D(2026, 11, 7), "end": D(2027, 3, 6),
        "range": (D(2025, 5, 4), D(2027, 3, 6))},
}
SIZING_RANGE = (D(2025, 9, 7), D(2026, 6, 6))
SIZING_E = D(2026, 6, 6)
YEAR_BACK = 52 * 7  # days


def is_sunday(d):
    return d.weekday() == 6


def is_saturday(d):
    return d.weekday() == 5


def window_starts(e):
    """Sunday start dates of the four complete weeks ending on Saturday e."""
    if not is_saturday(e):
        raise ValueError(f"{e} is not a Saturday")
    return [e - dt.timedelta(days=27 - 7 * i) for i in range(4)]


def shift_weeks(e, weeks):
    return e + dt.timedelta(days=7 * weeks)


def last_saturday_before(today):
    """Last Saturday strictly before `today`."""
    d = today - dt.timedelta(days=1)
    while not is_saturday(d):
        d -= dt.timedelta(days=1)
    return d


def parse_date(s):
    return D.fromisoformat(s) if isinstance(s, str) else s


# ----------------------------------------------------------------------------- parsing
class Series:
    """Parsed TIMESERIES response: weeks (Sunday start dates, in order), per-term values."""

    def __init__(self, weeks, partial, values, queries):
        self.weeks = weeks            # list[date]
        self.partial = partial        # list[bool]
        self.values = values          # list[dict[date -> float]] one per term position
        self.queries = queries        # list[str] as returned

    def n_terms(self):
        return len(self.values)


def _point_value(v):
    if v.get("extracted_value") is not None:
        return float(v["extracted_value"])
    raw = str(v.get("value", "")).strip()
    raw = raw.replace("<", "").replace(">", "")
    return float(raw)


def parse_timeseries(resp):
    """Parse a SerpAPI google_trends TIMESERIES JSON (dict). Returns Series or raises ValueError.

    The week of a point is the UTC date of its `timestamp` (unix seconds, string). Values are
    taken by position in the `values` list (SerpAPI returns them in the order of q).
    """
    try:
        pts = resp["interest_over_time"]["timeline_data"]
    except (KeyError, TypeError):
        raise ValueError("no interest_over_time.timeline_data")
    if not isinstance(pts, list) or not pts:
        raise ValueError("empty timeline")
    weeks, partial, queries = [], [], []
    values = None
    for p in pts:
        ts = int(float(p["timestamp"]))
        d = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()
        vs = p.get("values") or []
        if values is None:
            values = [dict() for _ in vs]
            queries = [v.get("query") for v in vs]
        if len(vs) != len(values):
            raise ValueError("inconsistent number of terms across points")
        weeks.append(d)
        partial.append(bool(p.get("partial_data", False)))
        for i, v in enumerate(vs):
            values[i][d] = _point_value(v)
    return Series(weeks, partial, values, queries)


def mc_weekly(series, declared_start, declared_end, windows_e=(), n_terms=None):
    """MC_Weekly. Returns (ok, reasons). Checks: weekly points with consecutive 7-day steps; every
    point starts on a Sunday; the points cover the declared range; no partial point inside any
    window W(e), e in windows_e; (optionally) the expected number of terms."""
    reasons = []
    w = series.weeks
    if n_terms is not None and series.n_terms() != n_terms:
        reasons.append(f"expected {n_terms} terms, got {series.n_terms()}")
    if not w:
        return False, ["no points"]
    for d in w:
        if not is_sunday(d):
            reasons.append(f"point {d} does not start on a Sunday")
            break
    for a, b in zip(w, w[1:]):
        if (b - a).days != 7:
            reasons.append(f"step {a}->{b} is {(b - a).days} days, not 7")
            break
    declared_start, declared_end = parse_date(declared_start), parse_date(declared_end)
    if not (w[0] <= declared_start and (declared_start - w[0]).days < 7):
        reasons.append(f"first point {w[0]} does not start the declared range {declared_start}")
    if not (w[-1] + dt.timedelta(days=6) >= declared_end and (w[-1] - declared_end).days <= 0):
        reasons.append(f"last point {w[-1]} does not cover declared end {declared_end}")
    inwin = set()
    for e in windows_e:
        inwin.update(window_starts(e))
    for d, p in zip(w, series.partial):
        if p and d in inwin:
            reasons.append(f"partial point {d} inside a window")
            break
    for e in windows_e:
        for d in window_starts(e):
            if d not in w:
                reasons.append(f"window week {d} missing")
                break
    return (not reasons), reasons


def window_sum(vals, e):
    """S(W(e)) for one term's {week_start: value}."""
    return sum(vals[d] for d in window_starts(e))


# ----------------------------------------------------------------------------- bundles
def sizing_order(names):
    """Alphabetical order of search names (case-insensitive, ties by exact string)."""
    return sorted(names, key=lambda n: (n.casefold(), n))


def first_sizing_bundle(ordered):
    return list(ordered[:5])


def next_sizing_bundle(ordered, n_placed, prev_largest):
    """Sizing s4.2: previous bundle's largest unit + the next four unplaced (alphabetical)."""
    nxt = ordered[n_placed:n_placed + 4]
    return [prev_largest] + list(nxt)


def largest_in_bundle(units, series, e=None):
    """Largest unit of a bundle by its sum over the whole returned range (ties: first listed)."""
    best, bs = None, -1.0
    for u, vals in zip(units, series.values):
        s = sum(vals.values())
        if s > bs:
            best, bs = u, s
    return best


def main_bundles(order_keys, sort_key_of):
    """Main bundles s4.3. `order_keys`: units; `sort_key_of(u)`: sortable key, descending size
    first (callers pass a key already such that ascending sort = size descending, ties
    alphabetical). Request 1 = units 1-5; each next = previous bundle's last unit + next four."""
    srt = sorted(order_keys, key=sort_key_of)
    bundles = [srt[:5]]
    placed = 5
    while placed < len(srt):
        bundles.append([bundles[-1][-1]] + srt[placed:placed + 4])
        placed += 4
    return bundles


# ----------------------------------------------------------------------------- chaining
def chain_factors(bundles, series_list):
    """Chain factors (s5.2). bundles: list of unit lists; series_list: list of Series or None
    (missing request). Link j->j+1 uses the shared unit bundles[j+1][0]; f_{j+1} = f_j*T_j/T_{j+1}
    with T the shared unit's sum over the full returned range. A link fails when either sum is zero
    or either request is missing; a failed link starts a new segment (factor restarts at 1).
    Returns list of (segment, f) per bundle (None for missing bundles) and list of link statuses."""
    info, links = [], []
    seg, f = 0, 1.0
    for j, (b, s) in enumerate(zip(bundles, series_list)):
        if s is None:
            info.append(None)
            if j > 0:
                links.append(False)
            continue
        if j == 0:
            info.append((0, 1.0))
            continue
        prev = series_list[j - 1]
        ok = False
        if prev is not None and info[j - 1] is not None:
            shared = b[0]
            if shared in bundles[j - 1]:
                tj = sum(prev.values[bundles[j - 1].index(shared)].values())
                tj1 = sum(s.values[0].values())
                if tj > 0 and tj1 > 0:
                    ok = True
                    seg, f = info[j - 1][0], info[j - 1][1] * tj / tj1
        if not ok:
            # new segment: after the last used segment
            used = [i[0] for i in info if i is not None]
            seg, f = (max(used) + 1 if used else 0), 1.0
        links.append(ok)
        info.append((seg, f))
    return info, links


def unit_levels(bundles, series_list, info, e):
    """Chained level of each unit at W(e): f_j x mean weekly index over W(e) in the first bundle
    holding it (with data). Returns {unit: (segment, level)}."""
    out = {}
    for b, s, inf in zip(bundles, series_list, info):
        if s is None or inf is None:
            continue
        for i, u in enumerate(b):
            if u in out:
                continue
            out[u] = (inf[0], inf[1] * window_sum(s.values[i], e) / 4.0)
    return out


def size_sort_key(seg_level, name):
    """Ascending sort = size descending: earlier segment first, larger level first, then name."""
    seg, level = seg_level
    return (seg, -level, name.casefold(), name)


def rank_levels(levels):
    """Within-substrate rank of chained levels (higher level -> higher rank; average ranks for
    exact ties; every unit of an earlier segment ranks above every unit of a later one)."""
    keys = {u: (-seg, lvl) for u, (seg, lvl) in levels.items()}
    items = sorted(keys.items(), key=lambda kv: kv[1])
    ranks, i, n = {}, 0, len(items)
    while i < n:
        j = i
        while j + 1 < n and items[j + 1][1] == items[i][1]:
            j += 1
        r = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            ranks[items[k][0]] = r
        i = j + 1
    return ranks


# ----------------------------------------------------------------------------- per pull
def _qual_change(vals, e_to, e_from):
    """ln((S_to+1)/(S_from+1)) with the definedness rule S_to + S_from >= 4. None if not."""
    s1, s0 = window_sum(vals, e_to), window_sum(vals, e_from)
    if s1 + s0 >= 4:
        return math.log((s1 + 1.0) / (s0 + 1.0))
    return None


def pull_stats(bundles, series_list, stage):
    """Per-unit statistics from one pull of one substrate.
    Returns dict: units -> {"Y","Yp","M": float|None, "rank_base", "rank_end", "level_base", ...},
    plus "links" (list of bools) for MC_Chain. For a unit in two bundles the mean of the values from
    the bundles that meet the S >= 4 rule is used (an assumption, see the kit notes)."""
    st = STAGES[stage] if isinstance(stage, int) else stage
    e_base, e_end, e_prior = st["base"], st["end"], st.get("prior")
    pb, pe = shift_weeks(e_base, -52), shift_weeks(e_end, -52)
    info, links = chain_factors(bundles, series_list)
    lv_base = unit_levels(bundles, series_list, info, e_base)
    lv_end = unit_levels(bundles, series_list, info, e_end)
    rk_base, rk_end = rank_levels(lv_base), rank_levels(lv_end)
    acc = {}
    for b, s in zip(bundles, series_list):
        if s is None:
            continue
        for i, u in enumerate(b):
            vals = s.values[i]
            a = acc.setdefault(u, {"Y": [], "Yp": [], "M": []})
            for key, args in (("Y", (e_end, e_base)), ("Yp", (pe, pb)),
                              ("M", (e_base, e_prior) if e_prior else None)):
                if args is None:
                    continue
                try:
                    v = _qual_change(vals, *args)
                except KeyError:
                    v = None
                if v is not None:
                    a[key].append(v)
    out = {}
    for u, a in acc.items():
        out[u] = {k: (sum(v) / len(v) if v else None) for k, v in a.items()}
        out[u]["rank_base"] = rk_base.get(u)
        out[u]["rank_end"] = rk_end.get(u)
        out[u]["level_base"] = lv_base.get(u)
    return {"units": out, "links": links}


def combine_pulls(pull_unit_dicts, min_pulls=2):
    """Combination over pulls (s5.2): value = mean over the pulls in which it is defined; undefined
    when defined in fewer than `min_pulls` pulls. L = mean over pulls of the within-substrate rank.
    pull_unit_dicts: list (one per pull) of {unit: stats}. Returns {unit: {...}}."""
    units = set()
    for d in pull_unit_dicts:
        units.update(d)
    res = {}
    for u in units:
        r = {}
        for k in ("Y", "Yp", "M"):
            vs = [d[u][k] for d in pull_unit_dicts if u in d and d[u].get(k) is not None]
            r[k] = (sum(vs) / len(vs)) if len(vs) >= min_pulls else None
            r[f"n_{k}"] = len(vs)
        for k in ("rank_base", "rank_end"):
            vs = [d[u][k] for d in pull_unit_dicts if u in d and d[u].get(k) is not None]
            r["L" if k == "rank_base" else "L_end"] = (sum(vs) / len(vs)) if vs else None
        r["Y_SA"] = (r["Y"] - r["Yp"]) if (r["Y"] is not None and r["Yp"] is not None) else None
        r["Y_pulls"] = [d[u]["Y"] if (u in d and d[u].get("Y") is not None) else None
                        for d in pull_unit_dicts]
        res[u] = r
    return res


# ----------------------------------------------------------------------------- term rule (s3.2)
SUBSTRATE_WORDS = {
    "all": ["company", "brand", "corporation", "manufacturer", "business"],
    "v0.19": ["audio", "headphone", "electronics", "loudspeaker"],
    "v0.20": ["cosmetic", "beauty", "skin", "makeup", "personal care", "fragrance", "perfume"],
    "v0.21": ["cosmetic", "beauty", "skin", "makeup", "personal care", "fragrance", "perfume"],
    "v0.22": ["auto", "car", "vehicle", "motor"],
    "v0.23": ["whisk", "bourbon", "scotch", "cognac", "brandy", "tequila", "mezcal", "gin", "rum",
              "vodka", "liqueur", "liquor", "spirit", "distill", "beverage", "drink"],
}


def normalise(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace("&", "and")
    return re.sub(r"[^a-z0-9]", "", s)


def type_matches(type_str, substrate):
    t = (type_str or "").lower()
    for kw in SUBSTRATE_WORDS["all"] + SUBSTRATE_WORDS[substrate]:
        if re.search(r"(?<![a-z0-9])" + re.escape(kw), t):
            return True
    return False


def choose_term(search_name, suggestions, substrate):
    """First suggestion, in returned order, whose normalised title begins with the normalised
    search name AND whose type contains a substrate word at the start of a word. Returns
    (term, kind, suggestion|None); kind 'topic' (topic ID = `mid`) or 'plain'."""
    nn = normalise(search_name)
    for sg in suggestions or []:
        if normalise(sg.get("title", "")).startswith(nn) and type_matches(sg.get("type", ""), substrate):
            mid = sg.get("mid") or (sg.get("q") if str(sg.get("q", "")).startswith("/") else None)
            if mid:
                return mid, "topic", sg
    return search_name, "plain", None


def dump_json(obj, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
