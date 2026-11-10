#!/usr/bin/env python3
"""AIAS v1.13 — Grounding Paper A scorer (SKELETON, DRAFT r1, 2026-11-10).

Stdlib only. Implements the pre-registered rules that can be fixed before data:
URL normalisation (U1-U6), source classification (reads the machine copy of the
lists from prereg/source_classes_v1_13.md), per-brand own-domain citation share
(G*), pooled within-substrate Spearman (rho_w), separability / reliability bands,
and the structured-data extraction + SDRI of the audit protocol.

NOT done (TODO before lock): t4 loaders, P/C* readers from score_v0_42 outputs,
permutation / bootstrap drivers, verdict file writer. Stage C1 refuses to run
unless the tag v1.13-prereg-r1 exists and the anchor file is present, so this
skeleton cannot read t4 data by accident. It makes no network call.
"""
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
CLASSES_MD = PHASE / "prereg" / "source_classes_v1_13.md"
ANCHOR = PHASE / "anchor" / "git_anchor_v1_13.json"
PREREG_TAG = "v1.13-prereg-r1"

SEP_CONFIRM, SEP_FALSIFY = 0.30, 0.50
FLOOR_G, FLOOR_G_RUN, FLOOR_UNITS, FLOOR_SUBSTRATE_UNITS = 6, 3, 30, 5
REL3_CONFIRM, REL3_FALSIFY = 0.50, 0.30
DROP_LABELS = ("www", "www2", "m", "amp", "mobile")
CLASS_ORDER = ["brand_owned", "reference", "forum_ugc", "news", "review_editorial", "retailer", "other", "unresolved"]
_TITLE_DOMAIN = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")
_IPV4 = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


# ---------------------------------------------------------------- class lists
def load_classes(md_path=CLASSES_MD):
    """Parse the ```classes:<name> fenced blocks of source_classes_v1_13.md."""
    text = Path(md_path).read_text(encoding="utf-8")
    out = {}
    for name, body in re.findall(r"```classes:([a-z_]+)\n(.*?)```", text, flags=re.S):
        out[name] = body.split() if name != "path_overrides" else [l.split() for l in body.strip().splitlines() if l.strip()]
    plain = {}
    prefixes = []  # (host+path prefix, class)
    for cls in ("reference", "forum_ugc", "news", "review_editorial", "retailer"):
        for e in out.get(cls, []):
            if "/" in e:
                prefixes.append((e, cls))
            else:
                plain.setdefault(e, cls)  # first class in precedence order wins
    for e, cls in out.get("path_overrides", []):
        prefixes.append((e, cls))
    prefixes.sort(key=lambda t: -len(t[0]))  # longest prefix first
    return {"multi_suffix": set(out.get("multi_suffix", [])), "redirect_hosts": set(out.get("redirect_hosts", [])),
            "plain": plain, "prefixes": prefixes, "raw": out}


# ---------------------------------------------------------------- U1-U6
def normalize_host(host):
    h = (host or "").strip().lower().rstrip(".")
    labels = h.split(".")
    while len(labels) > 2 and labels[0] in DROP_LABELS:
        labels = labels[1:]
    return ".".join(labels)


def registrable_domain(host, multi_suffix):
    if not host or "." not in host or _IPV4.match(host):
        return None
    labels = host.split(".")
    if len(labels) >= 3 and ".".join(labels[-2:]) in multi_suffix:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def resolve_source(url, title, classes):
    """-> dict(host, path, domain, via_title) or None if unresolved (U1-U5)."""
    u = (url or "").strip()
    if not u:
        return None
    if "://" not in u:
        u = "https://" + u
    try:
        parts = urlsplit(u)
    except ValueError:
        return None
    host = normalize_host(parts.hostname or "")
    path = (parts.path or "/").lower()
    if host in classes["redirect_hosts"]:
        t = normalize_host((title or "").strip().lower())
        if not _TITLE_DOMAIN.match(t or ""):
            return None
        dom = registrable_domain(t, classes["multi_suffix"])
        return None if dom is None else {"host": t, "path": "/", "domain": dom, "via_title": True}
    dom = registrable_domain(host, classes["multi_suffix"])
    if dom is None:
        return None
    return {"host": host, "path": path, "domain": dom, "via_title": False}


def classify(src, classes, substrate_brand_domains):
    """Precedence of source_classes_v1_13.md section 2. src from resolve_source or None."""
    if src is None:
        return "unresolved"
    host, path, dom = src["host"], src["path"], src["domain"]
    if dom in substrate_brand_domains:
        return "brand_owned"
    if dom == "wikipedia.org" or dom.endswith((".gov", ".edu", ".mil")) or dom in ("gov.uk", "ac.uk") \
            or host.endswith((".gov.uk", ".ac.uk")):
        return "reference"
    hp = dom + path
    for prefix, cls in classes["prefixes"]:
        if hp.startswith(prefix) or (host + path).startswith(prefix):
            return cls
    if host in classes["plain"]:  # 3-label host entries (e.g. abcnews.go.com)
        return classes["plain"][host]
    if dom in classes["plain"]:
        return classes["plain"][dom]
    if host.startswith(("forum.", "forums.", "community.", "discuss.")):
        return "forum_ugc"
    if "wiki" in host:
        return "reference"
    if host.startswith(("shop.", "store.")):
        return "retailer"
    if host.startswith("news."):
        return "news"
    return "other"


def answer_sources(record, classes, substrate_brand_domains, field="citations"):
    """Distinct classified sources of one S1 record (U6). Returns list of dicts."""
    search = record.get("search") or {}
    seen_url, out = set(), []
    for s in search.get(field) or []:
        src = resolve_source(s.get("url"), s.get("title"), classes)
        key = ("unresolved", s.get("url")) if src is None else (src["host"], src["path"])
        if key in seen_url:
            continue
        seen_url.add(key)
        out.append({"domain": None if src is None else src["domain"], "via_title": bool(src and src["via_title"]),
                    "cls": classify(src, classes, substrate_brand_domains)})
    return out


# ---------------------------------------------------------------- per-brand statistics
def brand_stats(answers, brand_domains, floor=FLOOR_G):
    """answers: list of dicts {substrate, named: set(brand_id), sources: list from answer_sources}.
    brand_domains: {brand_id: set(domains)}. Returns {brand_id: {m, g, o, G, G_star, rated}}."""
    out = {}
    for b, dset in brand_domains.items():
        m = g = o = 0
        for a in answers:
            if b not in a["named"]:
                continue
            m += 1
            doms = {s["domain"] for s in a["sources"] if s["cls"] != "unresolved"}
            if not doms:
                continue
            g += 1
            if doms & dset:
                o += 1
        G = (o / g) if g else None
        out[b] = {"m": m, "g": g, "o": o, "G": G, "G_star": None if G is None else 100.0 * G, "rated": g >= floor}
    return out


def source_mix(answer_sources_list):
    """Mean over answers of the share of distinct cited domains per class (each answer weighs 1)."""
    tot = {c: 0.0 for c in CLASS_ORDER}
    n = 0
    for srcs in answer_sources_list:
        by_dom = {}
        for s in srcs:
            if s["cls"] != "unresolved":
                by_dom.setdefault(s["domain"], s["cls"])
        if not by_dom:
            continue
        n += 1
        for c in by_dom.values():
            tot[c] += 1.0 / len(by_dom)
    return {c: (v / n if n else None) for c, v in tot.items()}


# ---------------------------------------------------------------- statistics
def avg_ranks(vals):
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


def pearson(x, y):
    n = len(x)
    if n < 2:
        return None
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return None
    return sxy / (sxx * syy) ** 0.5


def pooled_within_rho(x, y, groups, min_units=FLOOR_SUBSTRATE_UNITS):
    """Rank within group (average ranks), Pearson over pooled ranks; groups with < min_units dropped."""
    by = {}
    for xi, yi, gi in zip(x, y, groups):
        if xi is None or yi is None:
            continue
        by.setdefault(gi, []).append((xi, yi))
    rx, ry, n = [], [], 0
    for g, pairs in by.items():
        if len(pairs) < min_units:
            continue
        rx += avg_ranks([p[0] for p in pairs])
        ry += avg_ranks([p[1] for p in pairs])
        n += len(pairs)
    return pearson(rx, ry), n


def sep_verdict(rhos, n, min_n=FLOOR_UNITS, degenerate=False):
    """Separability bands over one or more rho legs (H1/H2: both legs must clear)."""
    if degenerate or n < min_n or any(r is None for r in rhos):
        return "UNDETERMINED"
    if any(abs(r) >= SEP_FALSIFY for r in rhos):
        return "FALSIFIED"
    if all(abs(r) <= SEP_CONFIRM for r in rhos):
        return "CONFIRMED"
    return "MARGINAL"


def spearman_brown_3(rel1):
    return None if rel1 is None else 3 * rel1 / (1 + 2 * rel1)


def reliability_verdict(rel1, p, n_pairs_ok):
    if n_pairs_ok < 2:
        return "UNDETERMINED"
    rel3 = spearman_brown_3(rel1)
    if rel3 is None:
        return "UNDETERMINED"
    if rel3 >= REL3_CONFIRM and p is not None and p < 0.05:
        return "CONFIRMED"
    if rel3 < REL3_FALSIFY:
        return "FALSIFIED"
    return "MARGINAL"


def degenerate(g_star_by_brand, substrate_of):
    """MQ5: > 0.80 of rated brands at 0, or SD 0 within >= 3 of 5 substrates."""
    vals = [v for v in g_star_by_brand.values() if v is not None]
    if not vals:
        return True
    if sum(1 for v in vals if v == 0) / len(vals) > 0.80:
        return True
    by = {}
    for b, v in g_star_by_brand.items():
        if v is not None:
            by.setdefault(substrate_of[b], []).append(v)
    flat = sum(1 for vs in by.values() if len(set(vs)) <= 1)
    return flat >= 3


# ---------------------------------------------------------------- audit: structured data
ORG_TYPES = {"Organization", "Corporation", "LocalBusiness", "OnlineStore", "OnlineBusiness", "AutoDealer",
             "AutomotiveBusiness", "Store", "NGO", "EducationalOrganization", "SportsOrganization"}
PRODUCT_TYPES = {"Product", "ProductModel", "ProductGroup", "IndividualProduct", "SomeProducts", "Car", "Vehicle",
                 "Motorcycle"}


def _strip_type(t):
    t = str(t)
    for p in ("https://schema.org/", "http://schema.org/", "schema:"):
        if t.startswith(p):
            return t[len(p):]
    return t


class _SDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_ld, self.buf, self.blocks, self.types = False, [], [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and (a.get("type") or "").lower().strip() == "application/ld+json":
            self.in_ld, self.buf = True, []
        for key in ("itemtype", "typeof"):
            if a.get(key):
                for t in a[key].split():
                    self.types.add(_strip_type(t.rstrip("/").split("/")[-1] if "schema.org" in t else t))

    def handle_endtag(self, tag):
        if tag == "script" and self.in_ld:
            self.in_ld = False
            self.blocks.append("".join(self.buf))

    def handle_data(self, data):
        if self.in_ld:
            self.buf.append(data)


def extract_structured_data(html):
    """-> {types: set, same_as: list (Organization/Brand nodes), ld_errors: int}."""
    p = _SDParser()
    p.feed(html or "")
    types, same_as, errors = set(p.types), [], 0

    def walk(node):
        if isinstance(node, list):
            for n in node:
                walk(n)
            return
        if not isinstance(node, dict):
            return
        t = node.get("@type")
        ts = {_strip_type(x) for x in (t if isinstance(t, list) else [t] if t else [])}
        types.update(ts)
        if ts & (ORG_TYPES | {"Brand"}):
            sa = node.get("sameAs")
            same_as.extend(sa if isinstance(sa, list) else [sa] if sa else [])
        for k, v in node.items():
            if k != "sameAs" and isinstance(v, (dict, list)):
                walk(v)

    for b in p.blocks:
        try:
            walk(json.loads(b))
        except (ValueError, TypeError):
            errors += 1
    return {"types": types, "same_as": [s for s in same_as if isinstance(s, str)], "ld_errors": errors}


def sdri(ind):
    """ind: dict of the 8 binary indicators i1..i8 (None = not rated). Returns (SDRI, SDRI_site, SDRI_kg)."""
    site = [ind.get(f"i{k}") for k in range(1, 6)]
    kg = [ind.get(f"i{k}") for k in range(6, 9)]
    s_site = None if any(v is None for v in site) else 100.0 * sum(site) / 5
    s_kg = None if any(v is None for v in kg) else 100.0 * sum(kg) / 3
    s_all = None if (s_site is None or s_kg is None) else 100.0 * (sum(site) + sum(kg)) / 8
    return s_all, s_site, s_kg


def site_indicators(home, pages):
    """home/pages: outputs of extract_structured_data (pages includes home)."""
    all_types = set().union(*(p["types"] for p in pages)) if pages else set()
    same = [s for p in pages for s in p["same_as"]]
    return {"i1": int(bool(home["types"] & ORG_TYPES)), "i2": int("Brand" in all_types),
            "i3": int(bool(all_types & PRODUCT_TYPES)), "i4": int(len(same) > 0),
            "i5": int(any(("wikidata.org" in s) or ("wikipedia.org" in s) for s in same))}


# ---------------------------------------------------------------- stage guard
def _tag_exists(tag):
    r = subprocess.run(["git", "tag", "--list", tag], cwd=str(PHASE), capture_output=True, text=True)
    return r.stdout.strip() == tag


def main(argv):
    if "--stage" not in argv:
        print(__doc__)
        return 0
    stage = argv[argv.index("--stage") + 1]
    if stage == "P":
        raise NotImplementedError("TODO: Stage P pilot on v0.39 search-on answers (declared pilot).")
    if stage in ("C1", "C2"):
        if not (_tag_exists(PREREG_TAG) and ANCHOR.exists()):
            sys.exit(f"REFUSED: Stage {stage} needs tag {PREREG_TAG} and {ANCHOR.name} (not locked).")
        raise NotImplementedError("TODO: t4 loaders, P/C* readers, permutation/bootstrap drivers.")
    sys.exit(f"unknown stage {stage}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
