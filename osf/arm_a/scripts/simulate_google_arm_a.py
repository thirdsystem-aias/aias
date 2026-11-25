#!/usr/bin/env python3
"""Arm A: simulated Google-visibility responses in DataForSEO's exact shape (pre-registration section 6.3: the join
and analysis scripts are run first on simulated Google data, never on real data, before the lock).

The shape is copied from a real response of the coordinator's paid feasibility test on a domain outside the study
(tests/fixtures/hro_datefrom_allrecipes.com_20261124T040453Z.json, 2026-11-24): every key, nesting level and the
item order (newest month first) are kept; only the target, the date range, the cost and the numbers change. No value
from that response is used as a study value. Nothing here calls any API.
"""
import copy
import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "tests" / "fixtures" / "hro_datefrom_allrecipes.com_20261124T040453Z.json"
POS_KEYS = ["pos_1", "pos_2_3", "pos_4_10", "pos_11_20", "pos_21_30", "pos_31_40", "pos_41_50", "pos_51_60",
            "pos_61_70", "pos_71_80", "pos_81_90", "pos_91_100"]


def load_template(path=TEMPLATE):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def month_list(date_from, pull_year, pull_month):
    y, m = int(date_from[:4]), int(date_from[5:7])
    out = []
    while (y, m) <= (pull_year, pull_month):
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def organic(template_metrics, etv, rng):
    o = copy.deepcopy(template_metrics)
    count = max(0, int(round(etv * rng.uniform(0.15, 0.35))))
    for k in POS_KEYS:
        o[k] = int(count * rng.uniform(0.01, 0.2))
    o.update({"etv": float(etv), "count": count, "estimated_paid_traffic_cost": float(etv) * rng.uniform(0.1, 0.5),
              "is_new": int(count * 0.4), "is_up": int(count * 0.2), "is_down": int(count * 0.25),
              "is_lost": int(count * 0.45), "clickstream_etv": None, "clickstream_gender_distribution": None,
              "clickstream_age_distribution": None})
    return o


def response(domain, date_from, pull_year, pull_month, etv_by_month, template=None, seed=0, cost=None,
             status_message="Ok.", drop_months=()):
    """One response dict. etv_by_month: {(y, m): etv}; months in drop_months are left out of `items`."""
    t = copy.deepcopy(template or load_template())
    rng = random.Random(seed)
    task = t["tasks"][0]
    res = task["result"][0]
    item0 = res["items"][0]
    months = [ym for ym in month_list(date_from, pull_year, pull_month) if ym not in set(drop_months)]
    items = []
    for (y, m) in sorted(months, reverse=True):                 # newest first, as the API returns them
        it = copy.deepcopy(item0)
        it["year"], it["month"] = y, m
        it["metrics"]["organic"] = organic(item0["metrics"]["organic"], etv_by_month.get((y, m), 0.0), rng)
        items.append(it)
    c = round(0.12 + 0.0012 * len(items), 4) if cost is None else cost
    t["cost"] = task["cost"] = c
    t["status_message"] = "Ok." if status_message == "Ok." else t["status_message"]
    task["status_message"] = status_message
    task["data"].update({"target": domain, "date_from": date_from})
    res.update({"target": domain, "total_count": len(items), "items_count": len(items), "items": items})
    if status_message != "Ok.":
        task["result"] = None
    return t


def latent_panel(domains, months, seed, level_sd=1.5, noise_sd=0.08, breaks=None):
    """Simulated etv per domain and month: log-normal brand level, small monthly noise, optional common breaks
    {(y, m): multiplicative factor applied from that month on}. Returns {domain: {(y, m): etv}}."""
    rng = random.Random(seed)
    out = {}
    for d in domains:
        lvl = rng.gauss(11.0, level_sd)
        series, f = {}, 1.0
        for ym in months:
            if breaks and ym in breaks:
                f *= breaks[ym]
            series[ym] = math.exp(lvl + rng.gauss(0, noise_sd)) * f
        out[d] = series
    return out
