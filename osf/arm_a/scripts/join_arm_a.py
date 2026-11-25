#!/usr/bin/env python3
"""Arm A: read one pull as it stood, build the monthly Google panel, flag index breaks and join to brands by
brand-master ID (pre-registration r4, sections 2.1, 6.1-6.4). No API call.

Rules (unit-tested in tests/test_join_arm_a.py, run before the lock on simulated data only):
  * Each domain's value for a pull comes from its last successful response in that pull's manifest; the file's
    SHA-256 must equal the manifest's (data as it stood). PULL_FAILED domains have no series in that pull.
  * Complete month = any month before the pull month (the month of the request); the partial pull month is dropped.
  * g = ln(1 + etv); secondary: ln(1 + count), ln(1 + pos_1 + pos_2_3 + pos_4_10).
  * Break flags (section 6.2), once per pull over all pulled domains, before any AIAS variable is joined: month m is
    flagged if |median dg(m)| > 0.40 or at least 80% of domains move by more than 0.2 in the same direction.
  * Window mean = mean over the three complete months ending with the wave month; needs at least 2 of 3 present.
    With flagged months dropped (robustness), the three nearest unflagged complete months at or before the wave.
  * A domain with etv = 0 or missing in more than half of the months of a test's windows is excluded from that test.
  * Joins are by brand-master ID; the brand's primary domain is used, its R1 domain is the sensitivity.
  * A domain shared by two brands of the same category excludes both from that category's tests.
"""
import csv
import hashlib
import json
import math
import statistics
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_arm_a as P   # noqa: E402

MEASURES = ("g", "count", "top10")


def ym_add(ym, k):
    y, m = ym
    t = y * 12 + (m - 1) + k
    return (t // 12, t % 12 + 1)


def window(end, k=3):
    return [ym_add(end, -i) for i in range(k - 1, -1, -1)]


def read_manifest(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_pull(pull, raw_root=None, root=None):
    """{domain: {(y, m): {'etv', 'g', 'count', 'top10'}}}, {domain: status}, pull month (y, m)."""
    raw_root = Path(raw_root or P.RAW)
    root = Path(root or P.ROOT)
    rows = read_manifest(raw_root / f"pull{pull}" / f"manifest_pull{pull}.csv")
    last_ok, status = {}, {}
    for r in rows:
        if r["outcome"] in ("OK", "OK_MONTHS_DIFFER"):
            last_ok[r["domain"]] = r
            status[r["domain"]] = "OK"
        elif r["outcome"] == "PULL_FAILED" and r["domain"] not in last_ok:
            status[r["domain"]] = "PULL_FAILED"
    panel, pull_month = {}, None
    for dom, r in last_ok.items():
        raw = (root / r["file"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != r["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {r['file']}: the file is not as it stood")
        sent = datetime.fromisoformat(r["sent_utc"])
        pm = (sent.year, sent.month)
        pull_month = pm if pull_month is None else min(pull_month, pm)
        resp = json.loads(raw.decode("utf-8"))
        items = resp["tasks"][0]["result"][0]["items"]
        series = {}
        for it in items:
            ym = (int(it["year"]), int(it["month"]))
            if ym >= pm:
                continue                                     # partial pull month (and anything later) dropped
            o = it["metrics"]["organic"]
            etv = o.get("etv")
            if etv is None:
                continue
            top = sum(int(o.get(k) or 0) for k in ("pos_1", "pos_2_3", "pos_4_10"))
            series[ym] = {"etv": float(etv), "g": math.log1p(float(etv)), "count": math.log1p(float(o.get("count") or 0)),
                          "top10": math.log1p(top)}
        panel[dom] = series
    return panel, status, pull_month


def break_flags(panel):
    """{(y, m): {'median_dg', 'share_up', 'share_down', 'n', 'flagged'}} over all pulled domains (section 6.2)."""
    months = sorted({ym for s in panel.values() for ym in s})
    out = {}
    for ym in months:
        prev = ym_add(ym, -1)
        dgs = [s[ym]["g"] - s[prev]["g"] for s in panel.values() if ym in s and prev in s]
        if not dgs:
            continue
        med = statistics.median(dgs)
        up = sum(d > P.BREAK_MOVE for d in dgs) / len(dgs)
        down = sum(d < -P.BREAK_MOVE for d in dgs) / len(dgs)
        out[ym] = {"median_dg": med, "share_up": up, "share_down": down, "n": len(dgs),
                   "flagged": abs(med) > P.BREAK_MEDIAN or up >= P.BREAK_SHARE or down >= P.BREAK_SHARE}
    return out


def window_months(series_months, end, flagged=frozenset(), k=3):
    """The window's months: the k months ending at `end`; with flagged months dropped, the k nearest unflagged
    months at or before `end` among the complete months of the pull."""
    if not flagged:
        return window(end, k)
    cand = sorted((ym for ym in series_months if ym <= end and ym not in flagged), reverse=True)
    return sorted(cand[:k])


def window_mean(series, end, measure="g", flagged=frozenset(), all_months=None, k=3):
    months = window_months(all_months if all_months is not None else series.keys(), end, flagged, k)
    vals = [series[ym][measure] for ym in months if ym in series]
    if len(vals) < 2:
        return None
    return sum(vals) / len(vals)


def usable(series, windows):
    """False if etv = 0 or missing in more than half of the months of the test's windows (section 6.4)."""
    months = sorted({ym for w in windows for ym in w})
    bad = sum(1 for ym in months if ym not in series or series[ym]["etv"] == 0)
    return bad <= len(months) / 2


def summed_etv(series, months):
    vals = [series[ym]["etv"] for ym in months if ym in series]
    return sum(vals) if len(vals) == len(months) else None


def load_domains(path=None):
    with open(path or (P.REG / "arm_a_domains_r1.csv"), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def brand_domains(rows, role="primary"):
    """{brand_id: (category, domain)} for the given role; a brand without a domain of that role uses its primary.
    Brands whose domain is shared with another brand of the same category are dropped (section 6.4)."""
    prim = {r["brand_id"]: (r["category"], r["domain"]) for r in rows if r["role"] == "primary"}
    out = dict(prim)
    if role == "sensitivity":
        for r in rows:
            if r["role"] == "sensitivity":
                out[r["brand_id"]] = (r["category"], r["domain"])
    seen = {}
    for b, (c, d) in out.items():
        seen.setdefault((c, d), []).append(b)
    shared = {b for bs in seen.values() if len(bs) > 1 for b in bs}
    return {b: v for b, v in out.items() if b not in shared}


def demeaned_change(values_by_brand, category_of):
    """dg minus the median dg of the brand's category (category-month demeaning; section 2.1)."""
    by_cat = {}
    for b, v in values_by_brand.items():
        if v is not None:
            by_cat.setdefault(category_of[b], []).append(v)
    med = {c: statistics.median(vs) for c, vs in by_cat.items()}
    return {b: (v - med[category_of[b]]) if v is not None else None for b, v in values_by_brand.items()}


def restatement(panel_a, panel_b):
    """Share of shared domain-months whose etv changed by more than 1% and by more than 10% (section 6.1)."""
    n = small = big = 0
    for d, sa in panel_a.items():
        sb = panel_b.get(d, {})
        for ym, va in sa.items():
            if ym in sb:
                a, b = va["etv"], sb[ym]["etv"]
                rel = abs(b - a) / a if a else (0.0 if b == 0 else float("inf"))
                n += 1
                small += rel > P.RESTATE_SMALL
                big += rel > P.RESTATE_BIG
    return {"domain_months": n, "share_gt_1pct": small / n if n else None, "share_gt_10pct": big / n if n else None,
            "rerun_on_pull3": bool(n) and big / n > P.RESTATE_SHARE}


def write_flags(pull, raw_root=None, root=None):
    """Section 6.2: the pull's break flags, written beside its manifest before any AIAS variable is joined."""
    panel, _status, _pm = load_pull(pull, raw_root, root)
    fl = {f"{y}-{m:02d}": v for (y, m), v in break_flags(panel).items()}
    out = Path(raw_root or P.RAW) / f"pull{pull}" / f"break_flags_pull{pull}.json"
    out.write_text(json.dumps(fl, indent=1) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--flags", type=int, required=True, choices=sorted(P.PULLS))
    print(write_flags(ap.parse_args().flags))
