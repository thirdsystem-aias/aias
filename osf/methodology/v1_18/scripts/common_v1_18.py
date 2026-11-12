"""AIAS v1.18 -- Grounding under four competing definitions (exploratory re-analysis beside v1.13).

Shared code. Re-uses v1.13's frozen URL rule (U1-U6), record selection (dedupe, answered, N3, S1, Phase B),
coder index and D_b loader by importing score_v1_13.py from osf/methodology/v1_13 on this branch (byte-identical
to v1.13 @ 1b58837). Nothing in v1.13 is modified or re-run.
"""
import csv
import hashlib
import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent                                   # osf/methodology/v1_18
METH = PHASE.parent                                   # osf/methodology
V113_SCORER = METH / "v1_13" / "scripts" / "score_v1_13.py"
V113_CLASSES = METH / "v1_13" / "prereg" / "source_classes_v1_13.md"
V113_DOMAINS = METH / "v1_13" / "registries" / "brand_domains_v1_13.csv"
DOMAIN_TABLE = PHASE / "registries" / "domain_table_v1_18.csv"
PREREG_TAG = "v1.18-prereg-r1"

PRIMARY_FIELD, SENS_FIELD = "citations", "sources"
FLOOR, FLOOR_SENS = 6, (3, 10)                        # grounded answers naming b (v1.13's G* floor); sensitivity
N_BOOT, CI_LEVEL = 2000, 90.0
SEEDS = {"bootstrap": 118001, "bootstrap_sens": 118002, "audit_sample": 118003, "synthetic": 118004}
DELTA_PRIMARY, DELTA_SECONDARY = 25.0, (10.0, 50.0)   # percentage points
AUDIT_N = 60                                          # audit sample of classified table rows (prereg section 4.4)

CLASSES = ("company", "listing", "review_social", "editorial_other")
TABLE_STATUSES = CLASSES + ("UNRESOLVED",)
FIVE = ("focal",) + CLASSES
# The four definitions: the classes of a cited domain that count toward brand b's share.
# "focal" = the domain is in D_b (v1.13's frozen list); every other domain takes its table class.
DEFINITIONS = {
    "K_own_domain": frozenset({"focal"}),                                   # Kumar
    "P_any_company": frozenset({"focal", "company"}),                       # Profound
    "Y_own_plus_listings": frozenset({"focal", "listing"}),                 # Yext
    "M_not_owned": frozenset({"company", "listing", "review_social", "editorial_other"}),  # Muck Rack
}
DEF_ORDER = ("K_own_domain", "P_any_company", "Y_own_plus_listings", "M_not_owned")
PAIRS = [(a, b) for i, a in enumerate(DEF_ORDER) for b in DEF_ORDER[i + 1:]]
IDENTITY_PAIRS = {("K_own_domain", "M_not_owned")}    # M = 100 - K by construction (common denominator)


def load_v113():
    spec = importlib.util.spec_from_file_location("score_v1_13", V113_SCORER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_domain_table(path=DOMAIN_TABLE):
    """{domain: {"cls": class or UNRESOLVED, "retailer": bool, "alias_of": str}}."""
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = r["domain"].strip().lower()
            if d in out:
                raise ValueError(f"duplicate domain {d}")
            c = r["class"].strip()
            if c not in TABLE_STATUSES:
                raise ValueError(f"{d}: unknown class {c!r}")
            out[d] = {"cls": c, "retailer": r.get("retailer", "").strip() == "1",
                      "alias_of": (r.get("alias_of") or "").strip()}
    return out


# =========================================================================== answers and classes (prereg section 3)
def make_answer(call_id, substrate, model, cell, run, named, domains):
    """named: set of unit keys; domains: set of resolved registrable domains of the answer (one field)."""
    return {"call_id": call_id, "substrate": substrate, "model": model, "cell": cell, "run": run,
            "named": set(named), "domains": set(domains)}


def answers_from_records(records, named_idx, classes, v113, field=PRIMARY_FIELD):
    out = []
    for r in records:
        doms = set()
        for e in ((r.get("search") or {}).get(field) or []):
            if isinstance(e, dict):
                src = v113.resolve_source(e.get("url"), e.get("title"), classes)
                if src is not None:
                    doms.add(src["domain"])
        cell = (r["substrate"], r["model_requested"], r.get("probe_id"), r.get("frame_id"))
        out.append(make_answer(r["call_id"], r["substrate"], r["model_requested"], cell, int(r["run"]),
                               named_idx.get(r["call_id"], set()), doms))
    return out


def domain_class(dom, unit_domains, all_db, table, opts):
    """Five-class label of one cited domain relative to brand b (unit_domains = D_b)."""
    if dom in unit_domains:
        return "focal"
    t = table.get(dom)
    if opts.get("alias_focal") and t and t["cls"] == "company" and opts.get("unit") in t["alias_of"].split(";"):
        return "focal"
    if dom in all_db:
        return "company"
    if t is None:
        raise KeyError(f"domain not in the domain table: {dom}")
    if opts.get("retailer_as_company") and t["retailer"]:
        return "company"
    return t["cls"]


def pair_shares(doms, unit, unit_domains, all_db, table, opts):
    """{definition: share in [0,1]} for one (answer, brand) pair, or None if no classified domain.
    Denominator: the answer's distinct resolved domains minus table-UNRESOLVED ones (primary), or all of them
    (opts['unresolved'] = 'out' -> counted outside every class; 'in' -> inside P and Y's classes too)."""
    labels = [domain_class(d, unit_domains, all_db, table, dict(opts, unit=unit)) for d in sorted(doms)]
    mode = opts.get("unresolved", "drop")
    if mode == "drop":
        labels = [x for x in labels if x != "UNRESOLVED"]
    if not labels:
        return None
    out = {}
    for name in DEF_ORDER:
        cls = DEFINITIONS[name]
        hit = 0
        for x in labels:
            if x == "UNRESOLVED":
                # never focal (D_b domains are never UNRESOLVED), so not owned: counts for M always;
                # for P and Y only under 'in'
                hit += (name == "M_not_owned") or (mode == "in" and name in ("P_any_company", "Y_own_plus_listings"))
            else:
                hit += x in cls
        out[name] = hit / len(labels)
    out["_mix"] = {k: sum(1 for x in labels if x == k) / len(labels) for k in FIVE + ("UNRESOLVED",)}
    return out


# =========================================================================== estimands (prereg section 5)
def brand_shares(answers, units, all_db, table, opts=None, floor=FLOOR, exclude=()):
    """{unit: {g, rated, K..M (0-100 or None)}} and the list of (unit, pair-share dict) for program level."""
    opts = opts or {}
    per, pairs = {}, []
    for a in answers:
        for u in a["named"]:
            if u in exclude:
                continue
            unit = units[u]
            if unit["status"] != "RESOLVED":
                continue                               # NONE: no own domain -> not rated (as v1.13)
            ps = pair_shares(a["domains"], f'{u[0]}:{u[1]}', unit["domains"], all_db, table, opts)
            if ps is None:
                continue
            per.setdefault(u, []).append(ps)
            pairs.append((u, ps))
    out = {}
    for u, lst in per.items():
        g = len(lst)
        rated = g >= floor
        row = {"g": g, "rated": rated, "substrate": u[0]}
        for d in DEF_ORDER:
            row[d] = 100.0 * sum(p[d] for p in lst) / g if rated else None
        out[u] = row
    return out, pairs


def program_level(stats, pairs):
    """Pair-weighted (primary) and brand-weighted program-level share per definition, and the five-class mix."""
    res = {"pair_weighted": {}, "brand_weighted": {}, "n_pairs": len(pairs),
           "n_rated": sum(1 for r in stats.values() if r["rated"])}
    for d in DEF_ORDER:
        res["pair_weighted"][d] = 100.0 * sum(p[d] for _, p in pairs) / len(pairs) if pairs else None
        vals = [r[d] for r in stats.values() if r["rated"]]
        res["brand_weighted"][d] = sum(vals) / len(vals) if vals else None
    res["mix_pair_weighted"] = {k: (100.0 * sum(p["_mix"][k] for _, p in pairs) / len(pairs) if pairs else None)
                                for k in FIVE + ("UNRESOLVED",)}
    return res


def _avg_ranks(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


def rho_w(xd, yd, min_per_sub=5):
    """Pooled within-substrate Spearman, ranks centred on the substrate mean rank (v1.13 section 3 convention);
    xd, yd: {unit: value}; units keyed (substrate, brand_id); substrates with < min_per_sub paired units dropped."""
    keys = [k for k in xd if k in yd and xd[k] is not None and yd[k] is not None]
    by = {}
    for k in keys:
        by.setdefault(k[0], []).append(k)
    xs, ys = [], []
    for sub, ks in sorted(by.items()):
        if len(ks) < min_per_sub:
            continue
        rx, ry = _avg_ranks([xd[k] for k in ks]), _avg_ranks([yd[k] for k in ks])
        c = (len(ks) + 1) / 2.0
        xs += [v - c for v in rx]
        ys += [v - c for v in ry]
    n = len(xs)
    if n < 3:
        return None, n
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return None, n
    return sxy / math.sqrt(sxx * syy), n


def agreement(stats, delta=DELTA_PRIMARY, secondary=DELTA_SECONDARY):
    """Per pair of definitions: rho_w of rated brands' shares; share of rated brands whose share differs by > delta."""
    out = {}
    rated = {u: r for u, r in stats.items() if r["rated"]}
    for a, b in PAIRS:
        xd = {u: r[a] for u, r in rated.items()}
        yd = {u: r[b] for u, r in rated.items()}
        rho, n = rho_w(xd, yd)
        diffs = [abs(r[a] - r[b]) for r in rated.values()]
        out[f"{a}~{b}"] = {"rho_w": rho, "n_rho": n, "identity": (a, b) in IDENTITY_PAIRS, "n": len(diffs),
                           "share_changed": (sum(d > delta for d in diffs) / len(diffs)) if diffs else None,
                           "share_changed_secondary": {str(t): (sum(d > t for d in diffs) / len(diffs)) if diffs
                                                       else None for t in secondary}}
    return out


def percentile(vals, q):
    v = sorted(vals)
    if not v:
        return None
    pos = (len(v) - 1) * q / 100.0
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    return v[lo] + (v[hi] - v[lo]) * (pos - lo)


def estimate(answers, units, all_db, table, opts=None, floor=FLOOR, exclude=()):
    stats, pairs = brand_shares(answers, units, all_db, table, opts, floor, exclude)
    return {"brands": stats, "program": program_level(stats, pairs), "agreement": agreement(stats)}


def cluster_bootstrap(answers, units, all_db, table, opts=None, seed=SEEDS["bootstrap"], n_boot=N_BOOT,
                      floor=FLOOR, exclude=()):
    """Cells (substrate x model x question; the three runs stay together) resampled with replacement within
    substrate; every estimand recomputed per draw; 90% percentile intervals. Brands not rated in a draw are
    absent from that draw."""
    rng = random.Random(seed)
    cells = {}
    for a in answers:
        cells.setdefault(a["substrate"], {}).setdefault(a["cell"], []).append(a)
    keys = {s: sorted(c, key=str) for s, c in cells.items()}
    draws = {"brand": {}, "program": {d: [] for d in DEF_ORDER}, "rho": {}, "changed": {}}
    lo_q, hi_q = (100 - CI_LEVEL) / 2, 100 - (100 - CI_LEVEL) / 2
    for _ in range(n_boot):
        sample = []
        for s in sorted(keys):
            ks = keys[s]
            for _k in range(len(ks)):
                sample += cells[s][ks[rng.randrange(len(ks))]]
        est = estimate(sample, units, all_db, table, opts, floor, exclude)
        for u, r in est["brands"].items():
            if r["rated"]:
                for d in DEF_ORDER:
                    draws["brand"].setdefault((u, d), []).append(r[d])
        for d in DEF_ORDER:
            v = est["program"]["pair_weighted"][d]
            if v is not None:
                draws["program"][d].append(v)
        for p, v in est["agreement"].items():
            if v["rho_w"] is not None:
                draws["rho"].setdefault(p, []).append(v["rho_w"])
            if v["share_changed"] is not None:
                draws["changed"].setdefault(p, []).append(v["share_changed"])
    ci = lambda xs: [percentile(xs, lo_q), percentile(xs, hi_q), len(xs)]  # noqa: E731
    return {"brand": {f"{u[0]}:{u[1]}|{d}": ci(v) for (u, d), v in draws["brand"].items()},
            "program_pair_weighted": {d: ci(v) for d, v in draws["program"].items()},
            "rho_w": {p: ci(v) for p, v in draws["rho"].items()},
            "share_changed": {p: ci(v) for p, v in draws["changed"].items()},
            "seed": seed, "n_boot": n_boot, "level": CI_LEVEL}
