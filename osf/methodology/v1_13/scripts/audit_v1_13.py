#!/usr/bin/env python3
"""
audit_v1_13.py -- AIAS(TM) v1.13 Grounding Paper A, Part II: structured-data audit of the registry brands' own
websites and of their public Wikidata records (prereg/website_audit_protocol_v1_13.md).
DRAFT r1, sent to Pablo for the 24-hour review (2026-11-10). Nothing has been fetched while writing this file.

Stdlib only. No model, no API key, no spend.

Modes
  --dry-run   the whole audit on the synthetic fixtures in scripts/fixtures/audit/ (sites under the reserved .test
              top-level domain; fake Wikidata items). NO NETWORK: socket connections and name lookups are refused
              for the whole run and every response comes from the fixture file. Writes
              prereg/dry_run_audit_v1_13.txt (--record PATH to change; --no-record to skip).
  --collect   the real audit, Stage A (--pass 1: P1-P3 and Wikidata; --pass 2: P1 only, 7 days later). REFUSES
              unless every condition of protocol section 8 holds; the local conditions are checked first and the
              network is touched only after they pass.
  --sdri      offline: computes v1_13_sdri.csv from the pass-1 records and the runner's QID adjudications.

AUDIT_NOTES (choices where the protocol is silent)
 A1  Page selection: links are the href of <a> elements in document order, resolved against P1's final URL,
     fragment dropped. Same-site = same registrable domain as P1's final URL (U2/U4 of source_classes_v1_13.md).
     A path matches a token list when one of its segments equals a token or starts with the token followed by
     "-", "_" or ".". Links whose path matches login, log-in, signin, sign-in, account, cart, checkout or
     register are never selected. P3 is never the same URL as P1 or P2.
 A2  Redirects are followed one hop at a time (at most 5 per page); each hop is a request under the robots and
     rate rules of its own host. robots.txt is fetched once per scheme+host before the first other request to
     that host and follows at most 5 redirects itself.
 A3  robots.txt: 2xx parsed with urllib.robotparser for this User-Agent; 4xx = allowed; 5xx, timeout or error =
     robots_unavailable (no request to that host). One retry after 60 s on 5xx, timeout or connection error, for
     every request (no retry on 4xx).
 A4  Responses: the first 5,000,000 bytes are read (truncated flagged); only text/html or application/xhtml+xml
     is parsed; the charset of the Content-Type header is used, else UTF-8 (errors replaced).
 A5  Wikidata: wbsearchentities (language en, the API's default result list), exact label or matched alias equal
     to the registry name after NFKC, case folding and straight apostrophes; candidates kept if an English label
     of one of their P31 values contains a word of registries/wikidata_types_v1_13.csv (kind p31_word). Then the
     protocol's rule: exactly one kept candidate with a P856 domain in D_b; else exactly one with an enwiki
     sitelink whose English description has a word starting with a category word of the unit's substrate (kind
     description_word); several -> tie (runner adjudicates, logged, before --sdri); none -> qid none.
 A6  Timing: per-host gap 10 s and global gap 1 s are enforced on the clock before every request; the Wikidata
     API host gets the 1 s gap only (protocol section 4).
"""
import argparse
import contextlib
import csv
import hashlib
import json
import re
import socket
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
sys.path.insert(0, str(HERE))
import score_v1_13 as S  # noqa: E402  (U2/U4 helpers, D_b loader)

USER_AGENT = "AIAS research crawler; https://thirdsystem.ai"
MAX_PAGES, MAX_REDIRECTS, MAX_BYTES = 3, 5, 5_000_000
HOST_GAP_S, GLOBAL_GAP_S, WIKIDATA_GAP_S = 10.0, 1.0, 1.0
TIMEOUT_S, RETRY_WAIT_S = 20.0, 60.0
AUDIT_TAG, RECEIPT_MIN_HOURS, WINDOW_HOURS = "v1.13-audit-r1", 24, 72
BLACKOUT_UTC = (datetime(2026, 11, 17, 0, 0, tzinfo=timezone.utc), datetime(2026, 11, 22, 12, 0, tzinfo=timezone.utc))
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
TYPES_CSV = PHASE / "registries" / "wikidata_types_v1_13.csv"
FIXTURES = HERE / "fixtures" / "audit"
AUDIT_DIR = PHASE / "audit"
AUDIT_ANCHOR = PHASE / "anchor" / "audit_anchor_v1_13.json"
AUDIT_RECEIPT = PHASE / "anchor" / "audit_receipt_v1_13.json"
DRY_RUN_RECORD = PHASE / "prereg" / "dry_run_audit_v1_13.txt"
PHANTOM_UNITS = {("v22", f"D.{i}") for i in range(1, 6)}       # v0.22 cell D 'Defunct' (protocol section 1)
ABOUT_TOKENS = ("about", "about-us", "our-story", "company", "heritage", "history", "who-we-are")
PRODUCT_TOKENS = ("product", "products", "shop", "collections", "models", "vehicles", "lineup", "spirits", "whisky",
                  "whiskey", "skincare", "makeup", "headphones")
EXCLUDE_TOKENS = ("login", "log-in", "signin", "sign-in", "account", "cart", "checkout", "register")
ORG_TYPES = {"Organization", "Corporation", "LocalBusiness", "OnlineStore", "OnlineBusiness", "AutoDealer",
             "AutomotiveBusiness", "Store", "NGO", "EducationalOrganization", "SportsOrganization"}
PRODUCT_TYPES = {"Product", "ProductModel", "ProductGroup", "IndividualProduct", "SomeProducts", "Car", "Vehicle",
                 "Motorcycle"}
HTML_TYPES = ("text/html", "application/xhtml+xml")
REDIRECT_CODES = (301, 302, 303, 307, 308)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
_SCHEMA_PREFIXES = ("https://schema.org/", "http://schema.org/", "schema:")


class Refused(SystemExit):
    pass


# =========================================================================== structured data (protocol section 5)
def _type_name(t):
    t = str(t).strip()
    for p in _SCHEMA_PREFIXES:
        if t.startswith(p):
            return t[len(p):].strip("/")
    return t


def _is_same_as(prop):
    return _type_name(prop) == "sameAs"


class _SDParser(HTMLParser):
    """JSON-LD blocks; microdata itemscope/itemtype and RDFa typeof scopes with their sameAs properties; <a> links."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_ld, self.buf, self.blocks = False, [], []
        self.types, self.same_as, self.links, self.stack = set(), [], [], []

    def _enclosing(self):
        for _tag, scope in reversed(self.stack):
            if scope:
                return scope
        return set()

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "script" and a.get("type", "").lower().strip().startswith("application/ld+json"):
            self.in_ld, self.buf = True, []
        if tag == "a" and a.get("href"):
            self.links.append(a["href"].strip())
        props = (a.get("itemprop", "") + " " + a.get("property", "")).split()
        if any(_is_same_as(p) for p in props):
            val = a.get("href") or a.get("content") or a.get("resource") or a.get("src")
            if val and self._enclosing() & (ORG_TYPES | {"Brand"}):
                self.same_as.append(val.strip())
        scope = set()
        if "itemscope" in a and a.get("itemtype"):
            scope |= {_type_name(t) for t in a["itemtype"].split()}
        if a.get("typeof"):
            scope |= {_type_name(t) for t in a["typeof"].split()}
        self.types |= scope
        if tag not in VOID:
            self.stack.append((tag, scope))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "script" and self.in_ld:
            self.in_ld = False
            self.blocks.append("".join(self.buf))
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.in_ld:
            self.buf.append(data)


def _walk_ld(node, types, same_as):
    if isinstance(node, list):
        for n in node:
            _walk_ld(n, types, same_as)
        return
    if not isinstance(node, dict):
        return
    t = node.get("@type")
    ts = {_type_name(x) for x in (t if isinstance(t, list) else [t]) if isinstance(x, str)}
    types |= ts
    if ts & (ORG_TYPES | {"Brand"}):
        for k, v in node.items():
            if _is_same_as(k):
                for x in (v if isinstance(v, list) else [v]):
                    if isinstance(x, str):
                        same_as.append(x.strip())
                    elif isinstance(x, dict) and isinstance(x.get("@id"), str):
                        same_as.append(x["@id"].strip())
    for k, v in node.items():
        if not _is_same_as(k) and isinstance(v, (dict, list)):
            _walk_ld(v, types, same_as)


def extract_structured_data(html):
    """-> {types: set, same_as: list (Organization/Brand nodes only), ld_blocks, ld_errors, links}."""
    p = _SDParser()
    p.feed(html or "")
    p.close()
    types, same_as, errors = set(p.types), list(p.same_as), 0
    for b in p.blocks:
        try:
            _walk_ld(json.loads(b), types, same_as)
        except (ValueError, TypeError):
            errors += 1                            # AQ3: a block that does not parse contributes nothing
    return {"types": types, "same_as": [s for s in same_as if s], "ld_blocks": len(p.blocks), "ld_errors": errors,
            "links": list(p.links)}


# =========================================================================== indicators and SDRI
def _host(url):
    try:
        return (urllib.parse.urlsplit((url or "").strip()).hostname or "").lower().rstrip(".")
    except ValueError:
        return ""


def _is_kg_link(url):
    h = _host(url)
    return h in ("wikidata.org", "wikipedia.org") or h.endswith((".wikidata.org", ".wikipedia.org"))


def site_indicators(home, pages):
    """(1)-(5). home: extract_structured_data of P1; pages: all fetched pages (P1 included)."""
    all_types = set().union(*(p["types"] for p in pages)) if pages else set()
    same = [s for p in pages for s in p["same_as"]]
    return {"i1": int(bool(home["types"] & ORG_TYPES)), "i2": int("Brand" in all_types),
            "i3": int(bool(all_types & PRODUCT_TYPES)), "i4": int(len(same) > 0),
            "i5": int(any(_is_kg_link(s) for s in same))}


def registrable(url_or_host, multi_suffix):
    h = _host(url_or_host) if "/" in (url_or_host or "") else (url_or_host or "").lower()
    return S.registrable_domain(S.normalize_host(h), multi_suffix)


def kg_indicators(kg, d_b, multi_suffix):
    """(6)-(8) from the adjudicated Wikidata record kg = {status, qid, p856: [...], sitelinks: [...]}.
    status 'error' -> not rated (None)."""
    if kg is None or kg.get("status") == "error":
        return {"i6": None, "i7": None, "i8": None}
    if not kg.get("qid"):
        return {"i6": 0, "i7": 0, "i8": 0}
    doms = {registrable(u, multi_suffix) for u in kg.get("p856") or []}
    return {"i6": 1, "i7": int(bool(doms & set(d_b))), "i8": int("enwiki" in (kg.get("sitelinks") or []))}


def sdri(ind):
    """SDRI = 100 x (sum of 1-8) / 8; SDRI_site = (1)-(5) / 5; SDRI_kg = (6)-(8) / 3; None = NOT RATED."""
    site = [ind.get(f"i{k}") for k in range(1, 6)]
    kg = [ind.get(f"i{k}") for k in range(6, 9)]
    s_site = None if any(v is None for v in site) else 100.0 * sum(site) / 5
    s_kg = None if any(v is None for v in kg) else 100.0 * sum(kg) / 3
    s_all = None if (s_site is None or s_kg is None) else 100.0 * (sum(site) + sum(kg)) / 8
    return s_all, s_site, s_kg


# =========================================================================== page selection (AUDIT_NOTES A1)
def _segments(path):
    return [s for s in (path or "").lower().split("/") if s]


def path_matches(path, tokens):
    for seg in _segments(path):
        for t in tokens:
            if seg == t or any(seg.startswith(t + c) for c in "-_."):
                return True
    return False


def pick_links(links, base_url, multi_suffix):
    """-> (P2 url or None, P3 url or None) from P1's links in document order."""
    site = registrable(base_url, multi_suffix)
    base = urllib.parse.urldefrag(base_url)[0]
    seen, cands = set(), []
    for href in links:
        if href.lower().startswith(("mailto:", "tel:", "javascript:", "#", "data:")):
            continue
        u = urllib.parse.urldefrag(urllib.parse.urljoin(base_url, href))[0]
        parts = urllib.parse.urlsplit(u)
        if parts.scheme not in ("http", "https") or u in seen or u == base:
            continue
        seen.add(u)
        if registrable(u, multi_suffix) != site or path_matches(parts.path, EXCLUDE_TOKENS):
            continue
        cands.append((u, parts.path))
    p2 = next((u for u, p in cands if path_matches(p, ABOUT_TOKENS)), None)
    p3 = next((u for u, p in cands if path_matches(p, PRODUCT_TOKENS) and u != p2), None)
    return p2, p3


# =========================================================================== fetching (protocol section 4)
class Response:
    def __init__(self, status=None, headers=None, body=b"", error=None, truncated=False):
        self.status, self.headers, self.body = status, {k.lower(): v for k, v in (headers or {}).items()}, body
        self.error, self.truncated = error, truncated


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None                                 # redirects are followed by fetch_page, hop by hop


class UrllibFetcher:
    """The real fetcher (used only by --collect): GET, no cookies, no redirects, this User-Agent, 20 s timeout."""

    def __init__(self):
        self.opener = urllib.request.build_opener(_NoRedirect())
        self.calls = []

    def get(self, url):
        self.calls.append(url)
        req = urllib.request.Request(url, method="GET", headers={
            "User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.1",
            "Accept-Language": "en-US,en;q=0.8"})
        try:
            with self.opener.open(req, timeout=TIMEOUT_S) as r:
                body = r.read(MAX_BYTES + 1)
                return Response(r.status, dict(r.headers), body[:MAX_BYTES], None, len(body) > MAX_BYTES)
        except urllib.error.HTTPError as e:
            body = e.read(MAX_BYTES + 1) if e.fp else b""
            return Response(e.code, dict(e.headers or {}), body[:MAX_BYTES], None, len(body) > MAX_BYTES)
        except (urllib.error.URLError, socket.timeout, TimeoutError, OSError, ValueError) as e:
            return Response(None, {}, b"", f"{type(e).__name__}: {e}"[:300])


class FixtureFetcher:
    """Dry run: every response comes from the fixture manifest; Wikidata API requests are answered from its
    'wikidata' block. Unknown URLs get a 404."""

    def __init__(self, manifest, root=FIXTURES):
        self.m, self.root, self.calls, self.attempts = manifest, Path(root), [], {}

    def get(self, url):
        self.calls.append(url)
        n = self.attempts[url] = self.attempts.get(url, 0) + 1
        if url.startswith(WIKIDATA_API):
            return self._wikidata(url)
        spec = self.m["responses"].get(url)
        if spec is None:
            return Response(404, {"content-type": "text/plain"}, b"")
        if spec.get("fail_first") and n == 1:
            return Response(None, {}, b"", "timeout (fixture)")
        if spec.get("error"):
            return Response(None, {}, b"", spec["error"])
        body = (self.root / spec["file"]).read_bytes() if spec.get("file") else spec.get("body", "").encode("utf-8")
        headers = dict(spec.get("headers") or {})
        headers.setdefault("content-type", "text/html; charset=utf-8" if spec.get("file") else "text/plain")
        return Response(spec.get("status", 200), headers, body)

    def _wikidata(self, url):
        q = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url).query))
        wd = self.m["wikidata"]
        if q.get("action") == "wbsearchentities":
            res = wd["search"].get(q.get("search"), [])
            if res == "error":
                return Response(500, {}, b"")
            out = {"search": res}
        elif q.get("action") == "wbgetentities":
            ents = {}
            for i in q.get("ids", "").split("|"):
                if q.get("props") == "labels":
                    ents[i] = {"labels": {"en": {"value": wd["labels"].get(i, "")}}}
                    continue
                e = wd["entities"].get(i, {})
                ents[i] = {"claims": {p: [{"mainsnak": {"datavalue": {"value": ({"id": v} if p == "P31" else v)}}}
                                          for v in vals] for p, vals in e.get("claims", {}).items()},
                           "sitelinks": {s: {"site": s} for s in e.get("sitelinks", [])},
                           "descriptions": {"en": {"value": e.get("description", "")}}}
            out = {"entities": ents}
        else:
            return Response(400, {}, b"")
        return Response(200, {"content-type": "application/json"}, json.dumps(out).encode("utf-8"))


class RealClock:
    def now(self):
        return time.monotonic()

    def sleep(self, s):
        time.sleep(max(0.0, s))

    def utc(self):
        return datetime.now(timezone.utc)


class SimClock:
    """Dry run: simulated time; sleeping advances the clock instantly."""

    def __init__(self, start_utc):
        self.t, self.start = 0.0, start_utc

    def now(self):
        return self.t

    def sleep(self, s):
        self.t += max(0.0, s)

    def utc(self):
        return self.start + timedelta(seconds=self.t)


class Limiter:
    """>= 10 s between requests to one host (Wikidata API: 1 s) and >= 1 s between any two requests."""

    def __init__(self, clock):
        self.clock, self.last_host, self.last_any, self.log = clock, {}, None, []

    def wait(self, host, gap=HOST_GAP_S):
        now = self.clock.now()
        t = now
        if host in self.last_host:
            t = max(t, self.last_host[host] + gap)
        if self.last_any is not None:
            t = max(t, self.last_any + GLOBAL_GAP_S)
        if t > now:
            self.clock.sleep(t - now)
        now = self.clock.now()
        self.last_host[host], self.last_any = now, now
        self.log.append((host, now))

    def min_gaps(self):
        per, glob, last, prev = {}, None, {}, None
        for host, t in self.log:
            if host in last:
                per[host] = min(per.get(host, float("inf")), t - last[host])
            if prev is not None:
                glob = t - prev if glob is None else min(glob, t - prev)
            last[host], prev = t, t
        return per, glob


class Ctx:
    def __init__(self, fetcher, clock, multi_suffix):
        self.fetcher, self.clock, self.limiter = fetcher, clock, Limiter(clock)
        self.robots, self.requests, self.retries, self.ms = {}, 0, 0, multi_suffix


def request(url, ctx, gap=HOST_GAP_S):
    """One GET under the rate rules; one retry after 60 s on 5xx or timeout/error; no retry on 4xx."""
    host = _host(url)
    ctx.limiter.wait(host, gap)
    resp = ctx.fetcher.get(url)
    ctx.requests += 1
    if resp.error or (resp.status is not None and resp.status >= 500):
        ctx.retries += 1
        ctx.clock.sleep(RETRY_WAIT_S)
        ctx.limiter.wait(host, gap)
        resp = ctx.fetcher.get(url)
        ctx.requests += 1
    return resp


def robots_decision(url, ctx):
    """'allowed' | 'robots_disallowed' | 'robots_unavailable' (AUDIT_NOTES A2, A3)."""
    parts = urllib.parse.urlsplit(url)
    key = (parts.scheme, parts.netloc.lower())
    if key not in ctx.robots:
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        resp, hops = None, 0
        while True:
            resp = request(robots_url, ctx)
            loc = resp.headers.get("location")
            if resp.status in REDIRECT_CODES and loc and hops < MAX_REDIRECTS:
                robots_url, hops = urllib.parse.urljoin(robots_url, loc), hops + 1
                continue
            break
        if resp.status is not None and 200 <= resp.status < 300:
            rp = urllib.robotparser.RobotFileParser()
            rp.parse(resp.body.decode("utf-8", errors="replace").splitlines())
            ctx.robots[key] = ("parsed", rp, resp.status)
        elif resp.status is not None and 400 <= resp.status < 500:
            ctx.robots[key] = ("allow_all", None, resp.status)
        else:
            ctx.robots[key] = ("unavailable", None, resp.status if resp.status is not None else resp.error)
    kind, rp, _ = ctx.robots[key]
    if kind == "unavailable":
        return "robots_unavailable"
    if kind == "allow_all" or rp.can_fetch(USER_AGENT, url):
        return "allowed"
    return "robots_disallowed"


def _decode(resp):
    ctype = resp.headers.get("content-type", "")
    m = re.search(r"charset=([\w-]+)", ctype, flags=re.I)
    try:
        return resp.body.decode(m.group(1) if m else "utf-8", errors="replace")
    except LookupError:
        return resp.body.decode("utf-8", errors="replace")


def fetch_page(url, ctx):
    """Follow at most 5 redirects hop by hop under robots and rate rules. -> page record (no HTML kept in it)."""
    chain, current = [], url
    for hop in range(MAX_REDIRECTS + 1):
        dec = robots_decision(current, ctx)
        if dec != "allowed":
            return {"requested": url, "final": current, "outcome": dec, "status": None, "chain": chain, "html": None}
        resp = request(current, ctx)
        chain.append({"url": current, "status": resp.status, "error": resp.error, "utc": ctx.clock.utc().isoformat()})
        loc = resp.headers.get("location")
        if resp.status in REDIRECT_CODES and loc:
            if hop == MAX_REDIRECTS:
                return {"requested": url, "final": current, "outcome": "too_many_redirects", "status": resp.status,
                        "chain": chain, "html": None}
            current = urllib.parse.urljoin(current, loc)
            continue
        out = {"requested": url, "final": current, "status": resp.status, "chain": chain, "html": None,
               "truncated": resp.truncated}
        if resp.error:
            out["outcome"] = "error"
        elif resp.status in (403, 429):
            out["outcome"] = "blocked"
        elif resp.status is not None and resp.status >= 400:
            out["outcome"] = f"http_{resp.status}"
        elif not resp.headers.get("content-type", "").lower().startswith(HTML_TYPES):
            out["outcome"] = "not_html"
        else:
            html = _decode(resp)
            out.update(outcome="ok", html=html, sha256=hashlib.sha256(resp.body).hexdigest())
        return out
    raise AssertionError("unreachable")


# =========================================================================== Wikidata (protocol section 4; A5)
def load_type_words(path=TYPES_CSV):
    p31, desc = [], {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            w = r["word"].strip().lower()
            if r["kind"] == "p31_word":
                p31.append(w)
            elif r["kind"] == "description_word":
                desc.setdefault(r["substrate"].strip(), []).append(w)
    return p31, desc


def _norm_name(s):
    s = unicodedata.normalize("NFKC", s or "").replace("’", "'").replace("‘", "'")
    return s.casefold().strip()


def _api(params, ctx):
    url = WIKIDATA_API + "?" + urllib.parse.urlencode(params)
    resp = request(url, ctx, WIKIDATA_GAP_S)
    if resp.error or resp.status != 200:
        raise IOError(f"Wikidata API {params.get('action')}: {resp.status or resp.error}")
    return json.loads(resp.body.decode("utf-8"))


def _claim_values(entity, prop):
    out = []
    for c in (entity.get("claims") or {}).get(prop, []):
        v = ((c.get("mainsnak") or {}).get("datavalue") or {}).get("value")
        out.append(v.get("id") if isinstance(v, dict) else v)
    return [v for v in out if v]


def choose_qid(name, substrate, d_b, search, entities, labels, p31_words, desc_words, multi_suffix):
    """Protocol section 4 QID rule (A5), on API results already fetched. -> kg record."""
    target = _norm_name(name)
    cands = [c["id"] for c in search
             if _norm_name(c.get("label")) == target or _norm_name((c.get("match") or {}).get("text")) == target]
    typed = []
    for q in dict.fromkeys(cands):
        p31 = [labels.get(t, "").lower() for t in _claim_values(entities.get(q, {}), "P31")]
        if any(w in lab for lab in p31 for w in p31_words):
            typed.append(q)

    def rec(q, rule):
        e = entities.get(q, {})
        return {"status": "chosen", "qid": q, "rule": rule, "p856": _claim_values(e, "P856"),
                "sitelinks": sorted((e.get("sitelinks") or {}).keys()), "candidates": cands, "typed": typed}

    def tie(qs, rule):
        return {"status": "tie", "qid": None, "rule": rule, "tied": qs, "candidates": cands, "typed": typed,
                "tied_p856": {q: _claim_values(entities.get(q, {}), "P856") for q in qs},
                "tied_sitelinks": {q: sorted((entities.get(q, {}).get("sitelinks") or {}).keys()) for q in qs}}
    by_site = [q for q in typed if {registrable(u, multi_suffix) for u in _claim_values(entities.get(q, {}), "P856")}
               & set(d_b)]
    if len(by_site) == 1:
        return rec(by_site[0], "p856_in_D_b")
    if len(by_site) > 1:
        return tie(by_site, "p856_in_D_b")
    words = desc_words.get(substrate, [])
    def desc_hit(q):
        d = (((entities.get(q, {}).get("descriptions") or {}).get("en") or {}).get("value") or "").lower()
        return any(re.search(r"\b" + re.escape(w), d) for w in words)
    by_desc = [q for q in typed if "enwiki" in (entities.get(q, {}).get("sitelinks") or {}) and desc_hit(q)]
    if len(by_desc) == 1:
        return rec(by_desc[0], "enwiki_and_description")
    if len(by_desc) > 1:
        return tie(by_desc, "enwiki_and_description")
    return {"status": "none", "qid": None, "rule": "no candidate", "candidates": cands, "typed": typed}


def wikidata_lookup(name, substrate, d_b, ctx, p31_words, desc_words):
    """At most three API requests: search, the candidates' entities, the English labels of their P31 values."""
    try:
        search = _api({"action": "wbsearchentities", "search": name, "language": "en", "uselang": "en",
                       "type": "item", "format": "json"}, ctx).get("search", [])
        ids = [c["id"] for c in search if _norm_name(c.get("label")) == _norm_name(name)
               or _norm_name((c.get("match") or {}).get("text")) == _norm_name(name)]
        entities, labels = {}, {}
        if ids:
            entities = _api({"action": "wbgetentities", "ids": "|".join(dict.fromkeys(ids)),
                             "props": "claims|sitelinks|descriptions", "languages": "en", "format": "json"},
                            ctx).get("entities", {})
            targets = sorted({t for q in entities for t in _claim_values(entities[q], "P31")})
            if targets:
                lab = _api({"action": "wbgetentities", "ids": "|".join(targets), "props": "labels",
                            "languages": "en", "format": "json"}, ctx).get("entities", {})
                labels = {t: ((v.get("labels") or {}).get("en") or {}).get("value", "") for t, v in lab.items()}
    except (IOError, ValueError, KeyError) as e:
        return {"status": "error", "qid": None, "error": str(e)[:300]}
    out = choose_qid(name, substrate, d_b, search, entities, labels, p31_words, desc_words, ctx.ms)
    out["snapshot_utc"] = ctx.clock.utc().isoformat()
    return out


# =========================================================================== one brand, the whole audit
def audit_unit(unit, ctx, p31_words, desc_words, raw_dir=None, pages_only_p1=False):
    """unit: {substrate, brand_id, brand, domains (set), primary_domain, phantom}. -> record."""
    rec = {"substrate": unit["substrate"], "brand_id": unit["brand_id"], "brand": unit["brand"],
           "phantom": bool(unit["phantom"]), "domain": unit.get("primary_domain"), "pages": {}, "site": None}
    if unit.get("primary_domain") and not unit["phantom"]:
        p1 = fetch_page(f"https://{unit['primary_domain']}/", ctx)
        pages = {"P1": p1}
        if p1["outcome"] == "ok" and not pages_only_p1:
            p2, p3 = pick_links(extract_structured_data(p1["html"])["links"], p1["final"], ctx.ms)
            pages["P2"] = fetch_page(p2, ctx) if p2 else {"outcome": "not_found"}
            pages["P3"] = fetch_page(p3, ctx) if p3 else {"outcome": "not_found"}
        sds = {}
        for k, pg in pages.items():
            if pg.get("outcome") == "ok":
                sds[k] = extract_structured_data(pg["html"])
                if raw_dir is not None:
                    (Path(raw_dir) / f"{unit['substrate']}_{unit['brand_id']}_{k}.html").write_text(pg["html"],
                                                                                                    encoding="utf-8")
            rec["pages"][k] = {kk: vv for kk, vv in pg.items() if kk != "html"}
            if k in sds:
                rec["pages"][k].update(types=sorted(sds[k]["types"]), same_as=sds[k]["same_as"],
                                       ld_blocks=sds[k]["ld_blocks"], ld_errors=sds[k]["ld_errors"])
        if "P1" in sds:
            rec["site"] = site_indicators(sds["P1"], list(sds.values()))
            rec["verified_alias"] = registrable(p1["final"], ctx.ms)
    if not pages_only_p1:
        rec["kg"] = wikidata_lookup(unit["brand"], unit["substrate"], unit["domains"], ctx, p31_words, desc_words)
    return rec


def indicators_of(rec, adjudication, multi_suffix, d_b):
    """Merge site and adjudicated KG indicators. adjudication: None, 'none' or a QID chosen among the tied."""
    site = rec.get("site") or {f"i{k}": None for k in range(1, 6)}
    kg = dict(rec.get("kg") or {})
    if kg.get("status") == "tie":
        if adjudication is None:
            raise ValueError(f"{rec['substrate']}|{rec['brand_id']}: QID tie needs the runner's adjudication")
        if adjudication != "none" and adjudication not in kg.get("tied", []):
            raise ValueError(f"{rec['substrate']}|{rec['brand_id']}: adjudicated QID is not among the tied")
        kg = {"status": "adjudicated", "qid": None if adjudication == "none" else adjudication,
              "p856": (kg.get("tied_p856") or {}).get(adjudication, []),
              "sitelinks": (kg.get("tied_sitelinks") or {}).get(adjudication, [])}
    ind = dict(site, **kg_indicators(kg, d_b, multi_suffix))
    s_all, s_site, s_kg = sdri(ind)
    return dict(ind, SDRI=s_all, SDRI_site=s_site, SDRI_kg=s_kg, qid=kg.get("qid"))


# =========================================================================== units, outputs
def units_from_domains(domains_csv=S.DOMAINS_CSV):
    """Audit units from the frozen D_b list (refuses UNRESOLVED rows)."""
    units = S.load_brand_domains(domains_csv)
    if S.unresolved_units(units):
        raise Refused(f"REFUSED: {len(S.unresolved_units(units))} rows of brand_domains_v1_13.csv are UNRESOLVED")
    rows = {(r["substrate"], r["brand_id"]): r for r in S.read_csv(domains_csv)}
    out = []
    for k, u in units.items():
        out.append({"substrate": k[0], "brand_id": k[1], "brand": u["brand"], "domains": u["domains"],
                    "primary_domain": (rows[k].get("domain") or "").strip().lower() or None,
                    "phantom": k in PHANTOM_UNITS})
    return out


SDRI_FIELDS = ["substrate", "brand_id", "brand", "phantom", "p1_outcome", "i1", "i2", "i3", "i4", "i5", "i6", "i7",
               "i8", "SDRI", "SDRI_site", "SDRI_kg", "qid", "verified_alias"]


def sdri_rows(records, adjudications, multi_suffix, d_b_of):
    rows = []
    for r in records:
        key = f"{r['substrate']}|{r['brand_id']}"
        ind = indicators_of(r, adjudications.get(key), multi_suffix, d_b_of(r))
        rows.append(dict({k: ind.get(k) for k in SDRI_FIELDS if k in ind}, substrate=r["substrate"],
                         brand_id=r["brand_id"], brand=r["brand"], phantom=int(r["phantom"]),
                         p1_outcome=(r["pages"].get("P1") or {}).get("outcome"), verified_alias=r.get("verified_alias")))
    return rows


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fields})


@contextlib.contextmanager
def no_network():
    """Refuse every socket connection and name lookup inside the block; count the attempts."""
    attempts = []

    def refuse(*a, **k):
        attempts.append(a[:1])
        raise RuntimeError("network disabled (dry run)")
    saved = (socket.socket.connect, socket.socket.connect_ex, socket.create_connection, socket.getaddrinfo)
    socket.socket.connect = refuse
    socket.socket.connect_ex = refuse
    socket.create_connection = refuse
    socket.getaddrinfo = refuse
    try:
        yield attempts
    finally:
        socket.socket.connect, socket.socket.connect_ex, socket.create_connection, socket.getaddrinfo = saved


# =========================================================================== dry run
def dry_run(record_path=DRY_RUN_RECORD, fixtures=FIXTURES):
    manifest = json.loads((Path(fixtures) / "manifest.json").read_text(encoding="utf-8"))
    classes = S.load_classes()
    p31_words, desc_words = load_type_words()
    lines, failures = [], []
    with no_network() as attempts, tempfile.TemporaryDirectory() as tmp:
        clock = SimClock(datetime(2026, 11, 14, 0, 0, tzinfo=timezone.utc))   # simulated time only
        ctx = Ctx(FixtureFetcher(manifest, fixtures), clock, classes["multi_suffix"])
        records = []
        for u in manifest["units"]:
            unit = dict(u, domains=set(u.get("domains") or []), primary_domain=u.get("domain"))
            records.append(audit_unit(unit, ctx, p31_words, desc_words, raw_dir=tmp))
        rows = sdri_rows(records, manifest.get("adjudications", {}), classes["multi_suffix"],
                         lambda r: next(set(u.get("domains") or []) for u in manifest["units"]
                                        if (u["substrate"], u["brand_id"]) == (r["substrate"], r["brand_id"])))
        raw_files = len(list(Path(tmp).iterdir()))
    per_host, glob = ctx.limiter.min_gaps()
    min_host = min((v for h, v in per_host.items() if h != _host(WIKIDATA_API)), default=None)
    lines.append("AIAS v1.13 Part II -- audit_v1_13.py --dry-run (synthetic fixtures; nothing fetched)")
    lines.append(f"run (real clock, UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}; "
                 f"Python {sys.version.split()[0]}; audit_v1_13.py SHA-256 {S.sha256_file(Path(__file__))}; "
                 f"fixtures/audit/manifest.json SHA-256 {S.sha256_file(Path(fixtures) / 'manifest.json')}")
    lines.append(f"User-Agent: {USER_AGENT}")
    lines.append(f"fixture units: {len(manifest['units'])}; simulated requests: {ctx.requests} (retries {ctx.retries}); "
                 f"socket/DNS attempts blocked: {len(attempts)}")
    lines.append(f"minimum gap between requests to one site host: {min_host} s (rule >= {HOST_GAP_S}); "
                 f"to the Wikidata API: {per_host.get(_host(WIKIDATA_API))} s (rule >= {WIKIDATA_GAP_S}); "
                 f"between any two requests: {glob} s (rule >= {GLOBAL_GAP_S})")
    lines.append(f"simulated duration: {clock.t:.0f} s; raw HTML files written (temporary, deleted): {raw_files}")
    lines.append("")
    lines.append("unit | P1 outcome | P2 | P3 | robots decisions | i1..i8 | SDRI / site / kg | qid")
    for r, row, u in zip(records, rows, manifest["units"]):
        pg = r["pages"]
        robots = sorted({p.get("outcome") for p in pg.values() if str(p.get("outcome", "")).startswith("robots")})
        ind = [row.get(f"i{k}") for k in range(1, 9)]
        lines.append(f"{r['substrate']}|{r['brand_id']} {r['brand']} | {(pg.get('P1') or {}).get('outcome')} | "
                     f"{(pg.get('P2') or {}).get('outcome')} | {(pg.get('P3') or {}).get('outcome')} | "
                     f"{','.join(robots) or '-'} | {ind} | {row['SDRI']} / {row['SDRI_site']} / {row['SDRI_kg']} | "
                     f"{row.get('qid')} ({(r.get('kg') or {}).get('status')}"
                     f"{', adjudicated' if (r.get('kg') or {}).get('status') == 'tie' else ''})")
        exp = u.get("expect") or {}
        got = {f"i{k}": row.get(f"i{k}") for k in range(1, 9)}
        for k, v in exp.items():
            if got.get(k) != v:
                failures.append(f"{r['brand_id']} {k}: expected {v}, got {got.get(k)}")
    checks = {"no network attempt": not attempts, "host gap >= 10 s": min_host is None or min_host >= HOST_GAP_S,
              "global gap >= 1 s": glob is None or glob >= GLOBAL_GAP_S,
              "all requests from fixtures": all(c.endswith(".test/") or ".test/" in c or c.startswith(WIKIDATA_API)
                                                for c in ctx.fetcher.calls),
              "indicators as the fixtures expect": not failures}
    lines.append("")
    for k, v in checks.items():
        lines.append(f"check: {k}: {'PASS' if v else 'FAIL'}")
    for f in failures:
        lines.append(f"  mismatch: {f}")
    text = "\n".join(lines) + "\n"
    if record_path:
        Path(record_path).write_text(text, encoding="utf-8")
    print(text)
    return 0 if all(checks.values()) else 1


# =========================================================================== --collect guard and modes
def _git(args):
    return subprocess.run(["git"] + args, cwd=str(PHASE), capture_output=True, text=True)


def collect_guard(now_utc, pass_no=1):
    """Protocol section 8. Local conditions first; the network (git ls-remote) only after they pass."""
    why = []
    tag_commit = _git(["rev-list", "-n", "1", AUDIT_TAG]).stdout.strip()
    if not tag_commit:
        why.append(f"tag {AUDIT_TAG} does not exist")
    anchor = json.loads(AUDIT_ANCHOR.read_text(encoding="utf-8")) if AUDIT_ANCHOR.exists() else None
    if anchor is None:
        why.append(f"{AUDIT_ANCHOR.name} missing")
    elif tag_commit and anchor.get("commit") != tag_commit:
        why.append("anchor does not name the tag's commit")
    receipt = json.loads(AUDIT_RECEIPT.read_text(encoding="utf-8")) if AUDIT_RECEIPT.exists() else None
    if receipt is None:
        why.append(f"{AUDIT_RECEIPT.name} missing (when Pablo received the locked text)")
    elif now_utc < datetime.fromisoformat(receipt["received_utc"]) + timedelta(hours=RECEIPT_MIN_HOURS):
        why.append("fewer than 24 hours since Pablo received the locked text")
    if BLACKOUT_UTC[0] <= now_utc < BLACKOUT_UTC[1]:
        why.append("inside the 2026-11-17 to 2026-11-21 blackout (v0.40)")
    if pass_no == 1 and now_utc < BLACKOUT_UTC[0] < now_utc + timedelta(hours=WINDOW_HOURS):
        why.append("pass 1 could not finish its 72-hour window before the blackout")
    if anchor is not None and S.sha256_file(S.DOMAINS_CSV) != anchor.get("brand_domains_sha256"):
        why.append("brand_domains_v1_13.csv differs from the anchored SHA-256")
    if S.unresolved_units(S.load_brand_domains()):
        why.append("brand_domains_v1_13.csv has UNRESOLVED rows")
    if why:
        raise Refused("REFUSED: " + "; ".join(why))
    remote = _git(["ls-remote", "--tags", "origin", AUDIT_TAG])
    if remote.returncode != 0 or AUDIT_TAG not in remote.stdout:
        raise Refused(f"REFUSED: tag {AUDIT_TAG} is not on origin")
    return anchor


def collect(pass_no):
    now = datetime.now(timezone.utc)
    collect_guard(now, pass_no)
    classes = S.load_classes()
    p31_words, desc_words = load_type_words()
    raw = AUDIT_DIR / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    (raw / ".gitignore").write_text("*\n", encoding="utf-8")         # raw HTML is never committed or deposited
    ctx = Ctx(UrllibFetcher(), RealClock(), classes["multi_suffix"])
    out = AUDIT_DIR / ("v1_13_audit_records.jsonl" if pass_no == 1 else "v1_13_audit_records_pass2.jsonl")
    start = now.isoformat()
    with open(out, "w", encoding="utf-8") as f:
        for u in units_from_domains():
            f.write(json.dumps(audit_unit(u, ctx, p31_words, desc_words, raw_dir=raw, pages_only_p1=(pass_no == 2)),
                               default=sorted) + "\n")
            f.flush()
    (AUDIT_DIR / f"window_pass{pass_no}.json").write_text(json.dumps(
        {"start_utc": start, "end_utc": datetime.now(timezone.utc).isoformat(), "requests": ctx.requests,
         "retries": ctx.retries, "user_agent": USER_AGENT}, indent=2), encoding="utf-8")
    return 0


def compute_sdri():
    """--sdri (offline): v1_13_sdri.csv from pass-1 records and audit/qid_adjudication_v1_13.csv."""
    classes = S.load_classes()
    recs = [json.loads(l) for l in (AUDIT_DIR / "v1_13_audit_records.jsonl").read_text(encoding="utf-8").splitlines()
            if l.strip()]
    adj_path = AUDIT_DIR / "qid_adjudication_v1_13.csv"
    adj = {f"{r['substrate']}|{r['brand_id']}": r["decision"].strip() for r in S.read_csv(adj_path)} \
        if adj_path.exists() else {}
    units = S.load_brand_domains()
    rows = sdri_rows(recs, adj, classes["multi_suffix"], lambda r: units[(r["substrate"], r["brand_id"])]["domains"])
    write_csv(AUDIT_DIR / "v1_13_sdri.csv", rows, SDRI_FIELDS)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v1.13 Part II structured-data audit")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--collect", action="store_true")
    g.add_argument("--sdri", action="store_true")
    ap.add_argument("--pass", dest="pass_no", type=int, choices=[1, 2], default=1)
    ap.add_argument("--record", default=str(DRY_RUN_RECORD))
    ap.add_argument("--no-record", action="store_true")
    a = ap.parse_args(argv)
    if a.dry_run:
        return dry_run(None if a.no_record else a.record)
    if a.collect:
        return collect(a.pass_no)
    return compute_sdri()


if __name__ == "__main__":
    sys.exit(main())
