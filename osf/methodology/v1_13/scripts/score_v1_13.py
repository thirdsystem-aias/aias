#!/usr/bin/env python3
"""
score_v1_13.py -- AIAS(TM) v1.13 Grounding Paper A, Part I: scorer CORE
(DRAFT r1, sent to Pablo for the 24-hour review, 2026-11-10).

Stdlib only. No network, no model call. Transcribes PRE_REGISTRATION_v1_13.md section 2 (answers, P and C* at
t4, source classification, per-brand statistics), section 3 (rho_w, permutation, bootstrap, verdicts, gate,
activation of H4-H6, H7), section 4 (MQ1-MQ8), section 6 (baseline) and the section 7 sensitivities.
THE PRE-REGISTRATION PROSE IS AUTHORITATIVE; where it is silent the simplest faithful option is taken and
listed in SCORER_NOTES. Structured-data extraction and SDRI (Part II) live in audit_v1_13.py; this file reads
the SDRI table for H7 (Stage C2).

Stage C1/C2 refuse to run unless tag v1.13-prereg-r1 exists, the anchor file is present, the frozen lists match
their anchored SHA-256 and v0.42's coder and scorer match their pinned blobs at tag v0.42-prereg-r1 (MQ7), and no
row of brand_domains_v1_13.csv is UNRESOLVED, so nothing here can read t4 data by accident. The tests run the
core on synthetic records only.

Not in this core (added at the Part I lock, when the activation record names the files): readers for the
comparator scores of active H4-H6 (until then an active leg is UNDETERMINED, "score not available"); the S6 alias
merge from Part II's verified aliases (Stage C2).

SCORER_NOTES (choices where the pre-registration is silent)
 N1  Answered S1 answer = one record per call_id (the last answered attempt, else the last attempt, as v0.42's
     coder dedupes) with condition S1, status ok, non-empty text, no error and an accepted served ID (equal to the
     requested ID or a dated snapshot of it, "-YYYY-MM-DD" or "-YYYYMMDD"; a leading "models/" is ignored).
 N2  Evidence field: search.sources for every provider (primary, section 2.1); search.citations is S2. Entries
     without a URL are unresolved. U1-U6 as source_classes_v1_13.md; a source is "resolved" if its class is not
     unresolved. S9 adds the URLs written in the answer text (Markdown link targets and bare http(s) addresses).
 N3  Unit = (substrate, brand_id) row of brand_domains_v1_13.csv. "Names b" = a v0.42 coder Phase B row with
     mentioned = 1, matched on (coder substrate, coder_key). A unit whose status is not RESOLVED has no D_b: its
     G* is NOT RATED (reason recorded) and it adds no domain to the brand_owned class.
 N4  S1 (denominator m_b) keeps the rating rule g_b >= floor; only the share changes.
 N5  rho_w: average ranks within substrate, centred on the substrate mean rank (m + 1) / 2, Pearson over the
     pooled centred ranks; substrates with fewer than 5 units in the comparison are dropped first; n = units in
     the retained substrates. S10 = uncentred ranks (v0.37-v0.41 convention).
 N6  Permutation: the FIRST variable's ranks are permuted within substrate (H3: the second run of each pair);
     two-sided hit |r| >= |r_obs| - 1e-12, one-sided hit r >= r_obs - 1e-12; p = (hits + 1) / (draws + 1);
     Python random.Random(seed), a fresh generator per leg. Draws are reproducible on the same Python version.
 N7  Bootstrap: units resampled with replacement within each retained substrate, ranks recomputed on each draw,
     2,000 draws, 90% percentile interval (5th and 95th percentiles, linear interpolation); seed 113008, a fresh
     generator per leg; non-finite draws are dropped and counted.
 N8  H1/H2 verdict order: MQ5 failed -> UNDETERMINED; any leg with n >= 30 and |rho| >= 0.50 -> FALSIFIED; any
     leg below the n floor -> UNDETERMINED; both |rho| <= 0.30 -> CONFIRMED; else MARGINAL.
 N9  H3: G*_r per run with floor g_b,r >= 3; a run pair qualifies with >= 30 units rated in both runs; rel1 = mean
     rho_w over the qualifying pairs; rel3 = 3 rel1 / (1 + 2 rel1) (-inf if 1 + 2 rel1 <= 0); UNDETERMINED with
     fewer than 2 qualifying pairs; p: on every draw the second run's ranks are permuted within substrate in each
     qualifying pair and rel1 recomputed (one-sided).
 N10 H4-H6: INACTIVE unless the lock record marks the leg active (activation rule, section 3); an active leg
     whose comparator score does not exist is UNDETERMINED with that reason (handed to Paper B).
 N11 H7: one-sided; partial rho = Pearson of the pooled within-substrate residuals of the centred ranks of SDRI
     and of G*, each regressed on the centred ranks of P_S0 within substrate (units with all three values).
 N12 MQ5 on the primary G* map: share of rated units at 0 > 0.80, or >= 3 substrates whose rated units carry at
     most one distinct G* value. MQ2: share of a model's category answers with >= 1 entry in the primary field.
     MQ6 on the rated units.
 N13 P at t4: recognition share = recognized / coded N3 Phase A rows of b in condition c (v0.42 coder table,
     answered calls only); pi_hat = column pi_N3_<c> of v0.42's brand table; P = 100 (share + 2 pi_hat) / 3.
     C* = 100 (1 - phi / 7.2) from column phi_N3_<c>, rated iff phi is defined and the coded N3 Phase B rows of
     condition c carry >= 6 mentions of b.
 N14 Panel: N3 primary. A model dropped by MQ2 (< 0.10) or Gemini dropped by MQ4 (> 0.20 unresolved) leaves the
     primary G*; the gate is computed on the remaining models and labelled.
"""
import argparse
import csv
import hashlib
import json
import math
import random
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
CLASSES_MD = PHASE / "prereg" / "source_classes_v1_13.md"
DOMAINS_CSV = PHASE / "registries" / "brand_domains_v1_13.csv"
ANCHOR = PHASE / "anchor" / "git_anchor_v1_13.json"
PREREG_TAG = "v1.13-prereg-r1"
PHASE_ID = "v1.13"

PRIMARY_FIELD, CITED_FIELD = "sources", "citations"           # section 2.1 (runner decision 2); S2
FLOOR_G, FLOOR_G_RUN, FLOOR_SENS = 6, 3, (3, 10)               # G* floor, per-run floor (H3), S4
FLOOR_UNITS, MIN_UNITS_PER_SUB = 30, 5                          # n floors (section 3)
SEP_CONFIRM, SEP_FALSIFY = 0.30, 0.50
REL3_CONFIRM, REL3_FALSIFY, ALPHA = 0.50, 0.30, 0.05
H7_CONFIRM, H7_FALSIFY = 0.30, 0.10
N_PERM, N_BOOT, CI_LEVEL = 10_000, 2_000, 90.0
TOL = 1e-12
SEEDS = {"H1_Sep_Presence": 113001, "H2_Sep_Consistency": 113002, "H3_Run_Reliability": 113003,
         "H4_Sep_Ranking": 113004, "H5_Sep_Sentiment": 113005, "H6_Sep_Coverage": 113006,
         "H7_Struct_Gap": 113007, "bootstrap": 113008, "sensitivities": 113009, "reserved": 113010}
MQ2_FLAG, MQ2_DROP, MQ3_FLAG, MQ3_LOW, MQ4_DROP = 0.25, 0.10, 0.40, 0.60, 0.20
MQ5_ZERO_SHARE, MQ5_FLAT_SUBSTRATES, MQ6_FLAG = 0.80, 3, 0.50
C_STAR_DIVISOR, C_STAR_MIN_MENTIONS = 7.2, 6
FABLE, OPUS55, GPT6, GEM4 = "claude-fable-5-2", "claude-opus-5-5", "gpt-6-astra", "gemini-4-argon"
PANELS = {"N3": (FABLE, GPT6, GEM4), "C3": (OPUS55, GPT6, GEM4), "A4": (FABLE, OPUS55, GPT6, GEM4)}
SUBSTRATES = ("v19", "v20", "v21", "v22", "v23")
CODER_SUB = {"v19": "v0.19", "v20": "v0.20", "v21": "v0.21", "v22": "v0.22", "v23": "v0.23"}
DENON = ("v19", "Denon")                                        # S11 (COI, section 11)
GATE_LEGS = ("H1_Sep_Presence", "H2_Sep_Consistency", "H3_Run_Reliability")
CONDITIONAL_LEGS = ("H4_Sep_Ranking", "H5_Sep_Sentiment", "H6_Sep_Coverage")
ACTIVATION_TAG = {"H4_Sep_Ranking": "v1.10-prereg-r2", "H5_Sep_Sentiment": "v1.11-prereg-r1",
                  "H6_Sep_Coverage": "v1.12-prereg-r1"}        # or a later revision (section 3)
VERDICTS = {"CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED", "INACTIVE"}
STATUSES = ("RESOLVED", "UNRESOLVED", "NONE")
DROP_LABELS = ("www", "www2", "m", "amp", "mobile")
CLASS_ORDER = ["brand_owned", "reference", "forum_ugc", "news", "review_editorial", "retailer", "other", "unresolved"]
_TITLE_DOMAIN = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")
_IPV4 = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
_MD_LINK = re.compile(r"\]\((https?://[^)\s]+)\)")
_BARE_URL = re.compile(r"https?://[^\s<>\"'\)\]]+")
_SNAPSHOT = re.compile(r"-\d{4}-\d{2}-\d{2}|-\d{8}")


class Refused(SystemExit):
    pass


def _finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


# =========================================================================== class lists (source_classes_v1_13.md)
def load_classes(md_path=CLASSES_MD):
    """Parse the ```classes:<name> fenced blocks (the machine copy of the frozen lists)."""
    text = Path(md_path).read_text(encoding="utf-8")
    out = {}
    for name, body in re.findall(r"```classes:([a-z_]+)\n(.*?)```", text, flags=re.S):
        out[name] = body.split() if name != "path_overrides" else [l.split() for l in body.strip().splitlines() if l.strip()]
    plain, prefixes = {}, []                      # prefixes: (host+path prefix, class)
    for cls in ("reference", "forum_ugc", "news", "review_editorial", "retailer"):
        for e in out.get(cls, []):
            if "/" in e:
                prefixes.append((e, cls))
            else:
                plain.setdefault(e, cls)          # first class in precedence order wins
    for e, cls in out.get("path_overrides", []):
        prefixes.append((e, cls))
    prefixes.sort(key=lambda t: -len(t[0]))      # longest prefix first
    return {"multi_suffix": set(out.get("multi_suffix", [])), "redirect_hosts": set(out.get("redirect_hosts", [])),
            "plain": plain, "prefixes": prefixes, "raw": out}


# =========================================================================== U1-U6
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


def _raw_host(url):
    u = (url or "").strip()
    if not u:
        return ""
    if "://" not in u:
        u = "https://" + u
    try:
        return (urlsplit(u).hostname or "").lower().rstrip(".")
    except ValueError:
        return ""


def resolve_source(url, title, classes):
    """-> dict(host, path, domain, via_title) or None if unresolved (U1-U5)."""
    u = (url or "").strip()
    if not u:
        return None
    if "://" not in u:
        u = "https://" + u
    try:
        parts = urlsplit(u)
        hostname = parts.hostname
    except ValueError:
        return None
    host = normalize_host(hostname or "")
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


def classify(src, classes, substrate_brand_domains, all_brand_domains=None):
    """Precedence of source_classes_v1_13.md section 2. src from resolve_source or None."""
    if src is None:
        return "unresolved"
    host, path, dom = src["host"], src["path"], src["domain"]
    if dom in substrate_brand_domains:
        return "brand_owned"
    if dom == "wikipedia.org" or dom.endswith((".gov", ".edu", ".mil")) or dom in ("gov.uk", "ac.uk") \
            or host.endswith((".gov.uk", ".ac.uk")):
        return "reference"
    for prefix, cls in classes["prefixes"]:
        if (dom + path).startswith(prefix) or (host + path).startswith(prefix):
            return cls
    if host in classes["plain"]:                  # 3-label host entries (e.g. abcnews.go.com)
        return classes["plain"][host]
    if dom in classes["plain"]:
        return classes["plain"][dom]
    if host.startswith(("forum.", "forums.", "community.", "discuss.")):
        return "forum_ugc"
    if "wiki" in host:
        return "reference"
    any_db = substrate_brand_domains if all_brand_domains is None else all_brand_domains
    if host.startswith(("shop.", "store.")) and dom not in any_db:
        return "retailer"
    if host.startswith("news."):
        return "news"
    return "other"


def text_urls(text):
    """S9: URLs written in the answer text (Markdown link targets, then bare http(s) addresses)."""
    out = []
    for m in _MD_LINK.finditer(text or ""):
        out.append(m.group(1))
    for m in _BARE_URL.finditer(text or ""):
        out.append(m.group(0).rstrip(".,;:!?"))
    return out


def answer_sources(record, classes, substrate_brand_domains, field=PRIMARY_FIELD, all_brand_domains=None,
                   extra_urls=()):
    """Distinct classified sources of one S1 record (U6: by normalised host + path; unresolved by raw URL)."""
    search = record.get("search") or {}
    entries = [s for s in (search.get(field) or []) if isinstance(s, dict)]
    entries += [{"url": u, "title": None} for u in extra_urls]
    seen, out = set(), []
    for s in entries:
        src = resolve_source(s.get("url"), s.get("title"), classes)
        key = ("unresolved", s.get("url")) if src is None else (src["host"], src["path"])
        if key in seen:
            continue
        seen.add(key)
        out.append({"key": key, "domain": None if src is None else src["domain"],
                    "via_title": bool(src and src["via_title"]),
                    "redirect": _raw_host(s.get("url")) in classes["redirect_hosts"],
                    "cls": classify(src, classes, substrate_brand_domains, all_brand_domains)})
    return out


def resolved_domains(sources):
    return {s["domain"] for s in sources if s["cls"] != "unresolved"}


# =========================================================================== D_b (registries/brand_domains_v1_13.csv)
def load_brand_domains(path=DOMAINS_CSV):
    """{(substrate, brand_id): {substrate, brand_id, brand, coder_key, status, domains}}. RESOLVED rows carry a
    domain (aliases ';'-separated); UNRESOLVED rows await the runner's decision; NONE = no own domain."""
    units = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            key = (r["substrate"].strip(), r["brand_id"].strip())
            if key in units:
                raise ValueError(f"duplicate unit {key}")
            status = (r.get("status") or "").strip().upper()
            if status not in STATUSES:
                raise ValueError(f"{key}: unknown status {status!r}")
            doms = set()
            if status == "RESOLVED":
                doms = {d.strip().lower() for d in [r.get("domain") or ""] + (r.get("aliases") or "").split(";")
                        if d.strip()}
                if not (r.get("domain") or "").strip():
                    raise ValueError(f"{key}: RESOLVED without a domain")
            units[key] = {"substrate": key[0], "brand_id": key[1], "brand": r.get("brand", ""),
                          "coder_key": (r.get("coder_key") or "").strip(), "status": status, "domains": doms}
    return units


def unresolved_units(units):
    return sorted(k for k, u in units.items() if u["status"] == "UNRESOLVED")


def substrate_domains(units):
    out = {s: set() for s in SUBSTRATES}
    for u in units.values():
        out.setdefault(u["substrate"], set()).update(u["domains"])
    return out


# =========================================================================== t4 records (v0.42 section 4.4)
def served_ok(requested, served):
    if not requested or not served:
        return False
    s = served[len("models/"):] if served.startswith("models/") else served
    if s == requested:
        return True
    return s.startswith(requested) and bool(_SNAPSHOT.fullmatch(s[len(requested):]))


def is_answered(rec):
    return (rec.get("status") == "ok" and bool((rec.get("text") or "").strip()) and not rec.get("error")
            and served_ok(rec.get("model_requested"), rec.get("served_model")))


def dedupe_calls(records):
    """One record per call_id: the last answered attempt if any, else the last attempt."""
    best = {}
    for r in records:
        cid = r["call_id"]
        if cid not in best or is_answered(r) or not is_answered(best[cid]):
            best[cid] = r
    return list(best.values())


def read_jsonl(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def select_calls(records, models, condition="S1", phase="B"):
    """Answered records of one condition and phase for the given models (records already deduplicated)."""
    return [r for r in records if r.get("condition") == condition and r.get("phase") == phase
            and r.get("model_requested") in models and is_answered(r)]


def named_index(coded_b_rows, units):
    """{call_id: set(unit keys)} from the v0.42 coder's Phase B rows with mentioned = 1."""
    by_ck = {(CODER_SUB[u["substrate"]], u["coder_key"]): k for k, u in units.items()}
    out = {}
    for r in coded_b_rows:
        if int(r["mentioned"]) != 1:
            continue
        k = by_ck.get((r["substrate"], r["brand"]))
        if k is None:
            raise ValueError(f"coded brand not in the D_b list: {r['substrate']} {r['brand']}")
        out.setdefault(r["call_id"], set()).add(k)
    return out


def build_answers(records, named, units, classes, field=PRIMARY_FIELD, with_text_urls=False):
    """One dict per answered S1 category answer: call_id, substrate, model, provider, run, named, sources."""
    sub_doms = substrate_domains(units)
    all_doms = set().union(*sub_doms.values()) if sub_doms else set()
    out = []
    for r in records:
        sub = r["substrate"]
        extra = text_urls(r.get("text")) if with_text_urls else ()
        out.append({"call_id": r["call_id"], "substrate": sub, "model": r["model_requested"],
                    "provider": r.get("provider"), "run": int(r["run"]), "named": named.get(r["call_id"], set()),
                    "sources": answer_sources(r, classes, sub_doms.get(sub, set()), field, all_doms, extra)})
    return out


# =========================================================================== per-brand statistics (section 2.4)
def brand_stats(answers, units, floor=FLOOR_G, denominator="g"):
    """{unit: {m, g, o, G, G_star, rated, reason}}; G* = 100 o/g (S1: 100 o/m), rated iff D_b and g >= floor."""
    out = {}
    for key, u in units.items():
        m = g = o = 0
        has_db = u["status"] == "RESOLVED"
        for a in answers:
            if key not in a["named"]:
                continue
            m += 1
            doms = resolved_domains(a["sources"])
            if not doms:
                continue
            g += 1
            if has_db and doms & u["domains"]:
                o += 1
        den = g if denominator == "g" else m
        G = (o / den) if (has_db and den) else None
        rated = has_db and g >= floor
        reason = "rated" if rated else (f"no D_b ({u['status']})" if not has_db else "g_b below floor")
        out[key] = {"m": m, "g": g, "o": o if has_db else None, "G": G,
                    "G_star": None if G is None else 100.0 * G, "rated": rated, "reason": reason}
    return out


def gstar_map(stats):
    return {k: (v["G_star"] if v["rated"] else None) for k, v in stats.items()}


def per_run_maps(answers, units, runs=(1, 2, 3), floor=FLOOR_G_RUN):
    return {r: gstar_map(brand_stats([a for a in answers if a["run"] == r], units, floor)) for r in runs}


def source_mix(answer_sources_list):
    """Mean over answers of the share of distinct resolved domains per class (each answer weighs 1)."""
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


def brand_descriptives(answers, units, stats):
    """mix_b and d_b for every rated unit (section 2.4)."""
    out = {}
    for key, st in stats.items():
        if not st["rated"]:
            continue
        grounded = [a["sources"] for a in answers if key in a["named"] and resolved_domains(a["sources"])]
        d = [len(resolved_domains(s)) for s in grounded]
        out[key] = {"mix": source_mix(grounded), "d": (sum(d) / len(d)) if d else None}
    return out


def g_a_map(phase_a_answers, units, floor=FLOOR_G):
    """G_A: own-domain share over grounded Phase A answers about b (A4), rated iff >= floor grounded answers.
    phase_a_answers: dicts {unit, sources}."""
    out = {}
    for key, u in units.items():
        grounded = [a for a in phase_a_answers if a["unit"] == key and resolved_domains(a["sources"])]
        if u["status"] != "RESOLVED":
            out[key] = {"grounded": len(grounded), "own": None, "G_A": None, "rated": False}
            continue
        own = sum(1 for a in grounded if resolved_domains(a["sources"]) & u["domains"])
        rated = len(grounded) >= floor
        out[key] = {"grounded": len(grounded), "own": own, "rated": rated,
                    "G_A": (100.0 * own / len(grounded)) if grounded else None}
    return out


# =========================================================================== statistics (section 3 conventions)
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
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def _group_index(groups):
    idx = {}
    for i, g in enumerate(groups):
        idx.setdefault(g, []).append(i)
    return list(idx.values())


def within_ranks(values, groups, centred=True):
    """Average ranks within each group; centred on the group's mean rank (m + 1) / 2 unless centred=False."""
    out = [0.0] * len(values)
    for idx in _group_index(groups):
        r = avg_ranks([values[i] for i in idx])
        shift = (len(idx) + 1) / 2.0 if centred else 0.0
        for i, ri in zip(idx, r):
            out[i] = ri - shift
    return out


def paired(xd, yd, min_per_sub=MIN_UNITS_PER_SUB, exclude=()):
    """Units with both values finite; substrates with fewer than min_per_sub such units dropped."""
    keys = sorted(k for k in xd if k in yd and k not in exclude and _finite(xd[k]) and _finite(yd[k]))
    per = {}
    for k in keys:
        per[k[0]] = per.get(k[0], 0) + 1
    keep = {s for s, n in per.items() if n >= min_per_sub}
    keys = [k for k in keys if k[0] in keep]
    info = {"n": len(keys), "n_substrates": len(keep), "per_substrate": {s: per[s] for s in sorted(keep)},
            "dropped_substrates": {s: n for s, n in sorted(per.items()) if s not in keep}}
    return keys, [float(xd[k]) for k in keys], [float(yd[k]) for k in keys], [k[0] for k in keys], info


def rho_w(x, y, g, centred=True):
    if len(x) < 3:
        return None
    return pearson(within_ranks(x, g, centred), within_ranks(y, g, centred))


def _demean(v):
    m = sum(v) / len(v)
    return [a - m for a in v]


def _shuffled_within(vec, groups_idx, rng):
    out = list(vec)
    for idx in groups_idx:
        vals = [vec[i] for i in idx]
        rng.shuffle(vals)
        for i, v in zip(idx, vals):
            out[i] = v
    return out


def perm_p(x, y, g, obs, seed, sided, n_draws=N_PERM, centred=True):
    """Permutation p: the first variable's within-substrate ranks permuted within substrate (N6)."""
    if sided not in ("one", "two"):
        raise ValueError(sided)
    if obs is None or not n_draws:
        return None
    a = _demean(within_ranks(x, g, centred))
    b = _demean(within_ranks(y, g, centred))
    den = math.sqrt(sum(v * v for v in a) * sum(v * v for v in b))
    if den <= 0:
        return None
    gidx = _group_index(g)
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_draws):
        ap = _shuffled_within(a, gidx, rng)
        r = sum(u * v for u, v in zip(ap, b)) / den
        hits += (abs(r) >= abs(obs) - TOL) if sided == "two" else (r >= obs - TOL)
    return (hits + 1) / (n_draws + 1)


def percentile(vals, q):
    s = sorted(vals)
    if not s:
        return None
    pos = (len(s) - 1) * q / 100.0
    lo, hi = math.floor(pos), math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def bootstrap_ci(x, y, g, seed=SEEDS["bootstrap"], n_boot=N_BOOT, centred=True, level=CI_LEVEL):
    """Units resampled with replacement within substrate; rho_w recomputed; percentile interval (N7)."""
    if not n_boot:
        return None
    rng = random.Random(seed)
    gidx = _group_index(g)
    vals, dropped = [], 0
    for _ in range(n_boot):
        idx = [grp[rng.randrange(len(grp))] for grp in gidx for _k in grp]
        r = rho_w([x[i] for i in idx], [y[i] for i in idx], [g[i] for i in idx], centred)
        if _finite(r):
            vals.append(r)
        else:
            dropped += 1
    tail = (100.0 - level) / 2.0
    return {"level": level, "lo": percentile(vals, tail), "hi": percentile(vals, 100.0 - tail),
            "draws": len(vals), "dropped_nonfinite": dropped}


def sep_leg(xd, yd, seed, n_perm=N_PERM, n_boot=N_BOOT, centred=True, sided="two", exclude=()):
    """rho_w(x, y) on the paired units with the n floor, permutation p and bootstrap interval."""
    keys, x, y, g, info = paired(xd, yd, exclude=exclude)
    leg = dict(info, seed=seed, centred=centred, sided=sided, below_n_floor=info["n"] < FLOOR_UNITS)
    rho = rho_w(x, y, g, centred) if info["n"] >= 3 else None
    leg["rho_w"] = rho
    leg["p"] = perm_p(x, y, g, rho, seed, sided, n_perm, centred) if rho is not None else None
    leg["ci90"] = bootstrap_ci(x, y, g, SEEDS["bootstrap"], n_boot, centred) if rho is not None else None
    return leg


def sep_verdict(legs, mq5_failed=False):
    """H1/H2 (two legs) and H4-H6 (one leg): bands 0.30 / 0.50 with the n floor (N8)."""
    if mq5_failed:
        return "UNDETERMINED"
    ok = [l for l in legs if not l["below_n_floor"] and l["rho_w"] is not None]
    if any(abs(l["rho_w"]) >= SEP_FALSIFY for l in ok):
        return "FALSIFIED"
    if len(ok) < len(legs):
        return "UNDETERMINED"
    if all(abs(l["rho_w"]) <= SEP_CONFIRM for l in ok):
        return "CONFIRMED"
    return "MARGINAL"


def spearman_brown_3(rel1):
    if rel1 is None:
        return None
    den = 1 + 2 * rel1
    return float("-inf") if den <= 0 else 3 * rel1 / den


def reliability_test(run_maps, seed=SEEDS["H3_Run_Reliability"], n_perm=N_PERM, centred=True, exclude=()):
    """H3 (N9): rel1 over the qualifying run pairs, rel3, joint one-sided permutation p."""
    pairs, qual = [], []
    for a, b in ((1, 2), (1, 3), (2, 3)):
        keys, x, y, g, info = paired(run_maps.get(a, {}), run_maps.get(b, {}), exclude=exclude)
        rho = rho_w(x, y, g, centred) if info["n"] >= 3 else None
        ok = info["n"] >= FLOOR_UNITS and rho is not None
        pairs.append(dict(info, pair=(a, b), rho_w=rho, qualifies=ok))
        if ok:
            qual.append((x, y, g))
    rel1 = (sum(p["rho_w"] for p in pairs if p["qualifies"]) / len(qual)) if qual else None
    rel3 = spearman_brown_3(rel1)
    p = None
    if len(qual) >= 2 and n_perm:
        prep = []
        for x, y, g in qual:
            a_ = _demean(within_ranks(x, g, centred))
            b_ = _demean(within_ranks(y, g, centred))
            prep.append((a_, b_, math.sqrt(sum(v * v for v in a_) * sum(v * v for v in b_)), _group_index(g)))
        rng = random.Random(seed)
        hits = 0
        for _ in range(n_perm):
            tot = 0.0
            for a_, b_, den, gidx in prep:
                bp = _shuffled_within(b_, gidx, rng)
                tot += sum(u * v for u, v in zip(a_, bp)) / den
            hits += (tot / len(prep)) >= rel1 - TOL
        p = (hits + 1) / (n_perm + 1)
    return {"pairs": pairs, "n_qualifying_pairs": len(qual), "rel1": rel1, "rel3": rel3, "p": p, "seed": seed}


def reliability_verdict(t):
    if t["n_qualifying_pairs"] < 2 or t["rel3"] is None:
        return "UNDETERMINED"
    if t["rel3"] >= REL3_CONFIRM and t["p"] is not None and t["p"] < ALPHA:
        return "CONFIRMED"
    if t["rel3"] < REL3_FALSIFY:
        return "FALSIFIED"
    return "MARGINAL"


def partial_rho(xd, yd, zd, centred=True, exclude=()):
    """N11: within-substrate rank residuals of x and y on z; Pearson of the pooled residuals."""
    keys = [k for k in sorted(xd) if k in yd and k in zd and k not in exclude
            and _finite(xd[k]) and _finite(yd[k]) and _finite(zd[k])]
    per = {}
    for k in keys:
        per[k[0]] = per.get(k[0], 0) + 1
    keys = [k for k in keys if per[k[0]] >= MIN_UNITS_PER_SUB]
    if len(keys) < 3:
        return None
    g = [k[0] for k in keys]
    rx = within_ranks([xd[k] for k in keys], g, True)
    ry = within_ranks([yd[k] for k in keys], g, True)
    rz = within_ranks([zd[k] for k in keys], g, True)
    ex, ey = [0.0] * len(keys), [0.0] * len(keys)
    for idx in _group_index(g):
        szz = sum(rz[i] ** 2 for i in idx)
        bx = sum(rx[i] * rz[i] for i in idx) / szz if szz > 0 else 0.0
        by = sum(ry[i] * rz[i] for i in idx) / szz if szz > 0 else 0.0
        for i in idx:
            ex[i], ey[i] = rx[i] - bx * rz[i], ry[i] - by * rz[i]
    return pearson(ex, ey)


def struct_gap_verdict(leg, collected=True):
    """H7: CONFIRMED rho >= 0.30 and one-sided p < 0.05; FALSIFIED rho <= 0.10; UNDETERMINED below the floor or
    if Part II was not collected before Stage C2."""
    if not collected or leg is None or leg["below_n_floor"] or leg["rho_w"] is None:
        return "UNDETERMINED"
    if leg["rho_w"] >= H7_CONFIRM and leg["p"] is not None and leg["p"] < ALPHA:
        return "CONFIRMED"
    if leg["rho_w"] <= H7_FALSIFY:
        return "FALSIFIED"
    return "MARGINAL"


def mq5_degenerate(gstar):
    """MQ5 (N12): True if > 0.80 of rated units are at 0, or >= 3 substrates carry at most one distinct value."""
    vals = {k: v for k, v in gstar.items() if v is not None}
    if not vals:
        return {"failed": True, "zero_share": None, "flat_substrates": [], "n_rated": 0}
    zero_share = sum(1 for v in vals.values() if v == 0) / len(vals)
    by = {}
    for k, v in vals.items():
        by.setdefault(k[0], set()).add(v)
    flat = sorted(s for s, vs in by.items() if len(vs) <= 1)
    return {"failed": zero_share > MQ5_ZERO_SHARE or len(flat) >= MQ5_FLAT_SUBSTRATES,
            "zero_share": zero_share, "flat_substrates": flat, "n_rated": len(vals)}


def activation(lock_record):
    """{leg: bool} from the lock record: active iff the leg's tag (or a later revision) was pushed before the
    v1.13 lock commit, as recorded at the lock (section 3, activation rule)."""
    legs = (lock_record or {}).get("conditional_legs") or {}
    return {leg: bool((legs.get(leg) or {}).get("pushed_before_lock")) for leg in CONDITIONAL_LEGS}


def gate(verdicts, active):
    """Paper A verdict (section 3, gate rule; N8 order)."""
    for k, v in verdicts.items():
        if v not in VERDICTS:
            raise ValueError(f"{k}: unknown verdict {v!r}")
    h = {k: verdicts.get(k, "UNDETERMINED") for k in GATE_LEGS}
    notes = []
    if any(v == "FALSIFIED" for v in h.values()):
        verdict = "FAIL"
    elif "UNDETERMINED" in (h["H1_Sep_Presence"], h["H2_Sep_Consistency"]):
        verdict = "UNDETERMINED"
    elif all(v == "CONFIRMED" for v in h.values()):
        verdict = "PASS"
        bad = [leg for leg in CONDITIONAL_LEGS if active.get(leg) and verdicts.get(leg) == "FALSIFIED"]
        if bad:
            verdict = "MARGINAL"
            notes.append("PASS downgraded to MARGINAL: " + ", ".join(bad) + " FALSIFIED")
    else:
        verdict = "MARGINAL"
    if verdict == "MARGINAL":
        notes.append("Paper B only on Pablo's recorded decision")
    for leg in CONDITIONAL_LEGS:
        if not active.get(leg) and verdicts.get(leg, "INACTIVE") != "INACTIVE":
            raise ValueError(f"{leg} is inactive but carries a verdict")
    return {"verdict": verdict, "legs": h, "active": dict(active), "notes": notes}


# =========================================================================== manipulation and quality checks (section 4)
def mq2_search_use(answers, models):
    out = {}
    for m in models:
        a = [x for x in answers if x["model"] == m]
        k = sum(1 for x in a if x["sources"])
        share = (k / len(a)) if a else None
        out[m] = {"answers": len(a), "with_source": k, "share": share,
                  "flag_search_rarely_used": share is not None and share < MQ2_FLAG,
                  "dropped_from_g_star": share is not None and share < MQ2_DROP}
    return out


def mq3_class_coverage(answers):
    tot = oth = 0
    for a in answers:
        seen = set()
        for s in a["sources"]:
            k = s["domain"] if s["domain"] is not None else s["key"]
            if k in seen:
                continue
            seen.add(k)
            tot += 1
            oth += s["cls"] in ("other", "unresolved")
    share = (oth / tot) if tot else None
    return {"pairs": tot, "other_or_unresolved": oth, "share": share,
            "flag": share is not None and share > MQ3_FLAG, "low_coverage": share is not None and share > MQ3_LOW}


def mq4_google(answers, model=GEM4):
    n = via = unres = redirect = 0
    for a in answers:
        if a["model"] != model:
            continue
        for s in a["sources"]:
            n += 1
            redirect += s["redirect"]
            via += s["via_title"]
            unres += s["cls"] == "unresolved"
    share_unres = (unres / n) if n else None
    return {"sources": n, "redirect_urls": redirect, "via_title_share": (via / n) if n else None,
            "unresolved_share": share_unres, "drop_gemini": share_unres is not None and share_unres > MQ4_DROP}


def mq6_coupling(stats, pi_s1, seed=None, n_boot=0):
    g_map = {k: float(v["g"]) for k, v in stats.items() if v["rated"]}
    gs = gstar_map(stats)
    l1 = sep_leg(g_map, pi_s1, seed or 0, n_perm=0, n_boot=n_boot)
    l2 = sep_leg(gs, g_map, seed or 0, n_perm=0, n_boot=n_boot)
    return {"rho_g_pi_s1": l1["rho_w"], "rho_gstar_g": l2["rho_w"], "n": l2["n"],
            "flag": l2["rho_w"] is not None and abs(l2["rho_w"]) >= MQ6_FLAG}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def mq7_frozen_lists(anchor, files=(CLASSES_MD, DOMAINS_CSV)):
    """MQ7: SHA-256 of the frozen lists equal the anchored values; a mismatch halts."""
    locked = (anchor or {}).get("locked_files") or {}
    out = {}
    for p in files:
        rel = str(Path(p).resolve().relative_to(PHASE.parents[2].resolve())) if Path(p).is_absolute() else str(p)
        want = (locked.get(rel) or {}).get("sha256")
        got = sha256_file(p)
        out[rel] = {"anchored": want, "now": got, "match": want == got}
    return out


def mq8_citations_vs_sources(records, classes):
    """Per provider: share of answers with >= 1 citation; share of cited URLs also in sources."""
    out = {}
    for r in records:
        s = r.get("search") or {}
        prov = out.setdefault(r.get("provider"), {"answers": 0, "with_citations": 0, "cited": 0, "cited_in_sources": 0})
        prov["answers"] += 1
        cites = [c for c in (s.get("citations") or []) if isinstance(c, dict)]
        prov["with_citations"] += bool(cites)

        def key(e):
            src = resolve_source(e.get("url"), e.get("title"), classes)
            return ("u", e.get("url")) if src is None else (src["host"], src["path"])
        skeys = {key(e) for e in (s.get("sources") or []) if isinstance(e, dict)}
        ckeys = {key(e) for e in cites}
        prov["cited"] += len(ckeys)
        prov["cited_in_sources"] += len(ckeys & skeys)
    for v in out.values():
        v["share_with_citations"] = v["with_citations"] / v["answers"] if v["answers"] else None
        v["share_cited_in_sources"] = v["cited_in_sources"] / v["cited"] if v["cited"] else None
    return out


# =========================================================================== comparators (section 2.2) and other inputs
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _by_coder(units):
    return {(CODER_SUB[u["substrate"]], u["coder_key"]): k for k, u in units.items()}


def _num(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def pi_t4(brand_table, units, cond):
    """pi_hat_{b,N3,c}: column pi_N3_<c> of v0.42's brand table (MQ6)."""
    byc = _by_coder(units)
    return {byc[(r["substrate"], r["brand"])]: _num(r.get(f"pi_N3_{cond}")) for r in brand_table
            if (r["substrate"], r["brand"]) in byc}


def p_t4(brand_table, coded_a, units, cond, models, answered_ids=None):
    """N13: P_c = 100 (recognition share + 2 pi_hat) / 3 on N3 in condition c."""
    byc = _by_coder(units)
    pi = {byc[(r["substrate"], r["brand"])]: _num(r.get(f"pi_N3_{cond}")) for r in brand_table
          if (r["substrate"], r["brand"]) in byc}
    rec = {}
    for r in coded_a:
        if r["condition"] != cond or r["model"] not in models:
            continue
        if answered_ids is not None and r["call_id"] not in answered_ids:
            continue
        if r.get("recognized") in ("", None):
            continue
        k = byc.get((r["substrate"], r["brand"]))
        if k is None:
            continue
        t = rec.setdefault(k, [0, 0])
        t[0] += int(r["recognized"])
        t[1] += 1
    out = {}
    for k in units:
        if k in pi and pi[k] is not None and k in rec and rec[k][1]:
            out[k] = 100.0 * (rec[k][0] / rec[k][1] + 2.0 * pi[k]) / 3.0
        else:
            out[k] = None
    return out


def c_star_t4(brand_table, coded_b, units, cond, models, answered_ids=None):
    """N13: C* = 100 (1 - phi / 7.2), rated iff phi defined and >= 6 N3 Phase B mentions in condition c."""
    byc = _by_coder(units)
    phi = {byc[(r["substrate"], r["brand"])]: _num(r.get(f"phi_N3_{cond}")) for r in brand_table
           if (r["substrate"], r["brand"]) in byc}
    ment = {}
    for r in coded_b:
        if r["condition"] != cond or r["model"] not in models:
            continue
        if answered_ids is not None and r["call_id"] not in answered_ids:
            continue
        k = byc.get((r["substrate"], r["brand"]))
        if k is not None:
            ment[k] = ment.get(k, 0) + int(r["mentioned"])
    return {k: (100.0 * (1.0 - phi[k] / C_STAR_DIVISOR)
                if phi.get(k) is not None and ment.get(k, 0) >= C_STAR_MIN_MENTIONS else None) for k in units}


def legacy_t3(profiles_rows, units):
    """S7: P and C* at t3 from osf/aias_2_0/aias_2_0_profiles.csv (legacy panel; cross-panel)."""
    byc = _by_coder(units)
    P, C = {}, {}
    for r in profiles_rows:
        if r.get("wave") != "t3":
            continue
        k = byc.get((r["substrate"], r["brand"]))
        if k is None:
            continue
        P[k] = _num(r.get("P"))
        C[k] = _num(r.get("C_star")) if str(r.get("rated")).strip() == "1" else None
    return P, C


def read_sdri(path, units):
    """Stage C2: {unit: SDRI} from audit's v1_13_sdri.csv (phantom units and units without SDRI_site excluded)."""
    out = {}
    for r in read_csv(path):
        k = (r["substrate"], r["brand_id"])
        if k in units and str(r.get("phantom", "0")) != "1":
            out[k] = _num(r.get("SDRI"))
    return out


# =========================================================================== gate statistics, baseline, stages
def gate_statistics(answers, units, P, C, comparators=None, active=None, n_perm=N_PERM, n_boot=N_BOOT,
                    centred=True, exclude=(), floor=FLOOR_G, denominator="g", seeds=None):
    """H1-H6 legs, verdicts and gate on one set of category answers. P, C: {"S0": map, "S1": map}.
    comparators: {leg: map or None} for active H4-H6. exclude: unit keys left out of every correlation."""
    seeds = seeds or SEEDS
    active = active or {leg: False for leg in CONDITIONAL_LEGS}
    comparators = comparators or {}
    stats = brand_stats(answers, units, floor, denominator)
    gs = gstar_map(stats)
    mq5 = mq5_degenerate({k: v for k, v in gs.items() if k not in exclude})
    legs = {
        "H1_Sep_Presence": [sep_leg(gs, P[c], seeds["H1_Sep_Presence"], n_perm, n_boot, centred, exclude=exclude)
                            for c in ("S1", "S0")],
        "H2_Sep_Consistency": [sep_leg(gs, C[c], seeds["H2_Sep_Consistency"], n_perm, n_boot, centred,
                                       exclude=exclude) for c in ("S1", "S0")],
    }
    h3 = reliability_test(per_run_maps(answers, units), seeds["H3_Run_Reliability"], n_perm, centred, exclude)
    verdicts = {"H1_Sep_Presence": sep_verdict(legs["H1_Sep_Presence"], mq5["failed"]),
                "H2_Sep_Consistency": sep_verdict(legs["H2_Sep_Consistency"], mq5["failed"]),
                "H3_Run_Reliability": reliability_verdict(h3)}
    reasons = {}
    for leg in CONDITIONAL_LEGS:
        if not active.get(leg):
            verdicts[leg] = "INACTIVE"
            continue
        comp = comparators.get(leg)
        if comp is None:
            verdicts[leg], reasons[leg] = "UNDETERMINED", "comparator score not available (handed to Paper B)"
            continue
        legs[leg] = [sep_leg(gs, comp, seeds[leg], n_perm, n_boot, centred, exclude=exclude)]
        verdicts[leg] = sep_verdict(legs[leg])
    return {"stats": stats, "g_star": gs, "mq5": mq5, "legs": legs, "H3": h3, "verdicts": verdicts,
            "reasons": reasons, "gate": gate(verdicts, active)}


def _median_iqr(vals):
    v = [x for x in vals if x is not None]
    if not v:
        return {"n": 0, "median": None, "q1": None, "q3": None, "share_zero": None}
    return {"n": len(v), "median": percentile(v, 50), "q1": percentile(v, 25), "q3": percentile(v, 75),
            "share_zero": sum(1 for x in v if x == 0) / len(v)}


def baseline(answers, units, stats, top=20):
    """Section 6 descriptives (no verdicts), per substrate and model, on the answers given."""
    out = {}
    for sub in SUBSTRATES:
        for m in sorted({a["model"] for a in answers}):
            a = [x for x in answers if x["substrate"] == sub and x["model"] == m]
            if not a:
                continue
            grounded = [x for x in a if resolved_domains(x["sources"])]
            out[f"{sub}|{m}"] = {
                "answers": len(a), "share_with_source": sum(1 for x in a if x["sources"]) / len(a),
                "sources_per_answer": sum(len(x["sources"]) for x in a) / len(a),
                "domains_per_answer": sum(len(resolved_domains(x["sources"])) for x in a) / len(a),
                "mix": source_mix([x["sources"] for x in a]),
                "share_any_brand_owned": sum(1 for x in a if any(s["cls"] == "brand_owned" for s in x["sources"])) / len(a),
                "share_reference": sum(1 for x in a if any(s["cls"] == "reference" for s in x["sources"])) / len(a),
                "grounded": len(grounded)}
    counts = {}
    for x in answers:
        for d in resolved_domains(x["sources"]):
            counts[d] = counts.get(d, 0) + 1
    top_domains = sorted(counts.items(), key=lambda t: (-t[1], t[0]))[:top]
    by_sub = {}
    for sub in SUBSTRATES:
        keys = [k for k in stats if k[0] == sub]
        by_sub[sub] = dict(_median_iqr([stats[k]["G_star"] for k in keys if stats[k]["rated"]]),
                           units=len(keys), rated=sum(1 for k in keys if stats[k]["rated"]),
                           g_b=[stats[k]["g"] for k in keys])
    return {"per_substrate_model": out, "top_domains": top_domains, "g_star_by_substrate": by_sub}


def loso(answers, units, P, C, n_perm, centred=True):
    """S8: leave-one-substrate-out values of H1-H3 (no bootstrap)."""
    out = {}
    for sub in SUBSTRATES:
        ex = tuple(k for k in units if k[0] == sub)
        r = gate_statistics(answers, units, P, C, n_perm=n_perm, n_boot=0, centred=centred, exclude=ex,
                            seeds={k: SEEDS["sensitivities"] for k in SEEDS})
        out[sub] = {"rho": {h: [l["rho_w"] for l in r["legs"][h]] for h in ("H1_Sep_Presence", "H2_Sep_Consistency")},
                    "rel3": r["H3"]["rel3"], "verdicts": {h: r["verdicts"][h] for h in GATE_LEGS}}
    return out


def stage_c1(inp, n_perm=N_PERM, n_boot=N_BOOT, sensitivities=True):
    """Stage C1 on loaded inputs (dict): records (t4 raw), coded_a, coded_b, brand_table, units, classes,
    active, comparators (optional), profiles (optional, S7). Returns the verdict document."""
    units, classes = inp["units"], inp["classes"]
    if unresolved_units(units):
        raise Refused(f"REFUSED: {len(unresolved_units(units))} D_b rows are UNRESOLVED")
    recs = dedupe_calls(inp["records"])
    answered = {r["call_id"] for r in recs if is_answered(r)}
    named = named_index(inp["coded_b"], units)
    s1_all = [r for r in recs if r.get("condition") == "S1" and is_answered(r)]
    for r in s1_all:                                   # MQ1: every answered S1 record parses (exceptions halt)
        answer_sources(r, classes, set(), PRIMARY_FIELD)
        answer_sources(r, classes, set(), CITED_FIELD)
    cat_a4 = select_calls(recs, PANELS["A4"], "S1", "B")
    answers_a4 = build_answers(cat_a4, named, units, classes)
    mq2 = mq2_search_use(answers_a4, PANELS["A4"])
    mq4 = mq4_google(answers_a4)
    dropped = [m for m in PANELS["N3"] if mq2[m]["dropped_from_g_star"]]
    if mq4["drop_gemini"] and GEM4 not in dropped:
        dropped.append(GEM4)
    models = [m for m in PANELS["N3"] if m not in dropped]
    answers = [a for a in answers_a4 if a["model"] in models]
    n3 = PANELS["N3"]
    P = {c: p_t4(inp["brand_table"], inp["coded_a"], units, c, n3, answered) for c in ("S0", "S1")}
    C = {c: c_star_t4(inp["brand_table"], inp["coded_b"], units, c, n3, answered) for c in ("S0", "S1")}
    active = inp.get("active") or {leg: False for leg in CONDITIONAL_LEGS}
    comps = inp.get("comparators") or {}
    prim = gate_statistics(answers, units, P, C, comps, active, n_perm, n_boot)
    doc = {"phase": PHASE_ID, "stage": "C1", "primary_field": PRIMARY_FIELD, "panel_models": models,
           "dropped_models": dropped, "gate": prim["gate"], "verdicts": prim["verdicts"], "reasons": prim["reasons"],
           "legs": prim["legs"], "H3": prim["H3"], "MQ": {
               "MQ1_parsed_s1_records": len(s1_all), "MQ2": mq2, "MQ3": mq3_class_coverage(answers), "MQ4": mq4,
               "MQ5": prim["mq5"], "MQ6": mq6_coupling(prim["stats"], pi_t4(inp["brand_table"], units, "S1")),
               "MQ8": mq8_citations_vs_sources([r for r in cat_a4], classes)},
           "units": {f"{k[0]}|{k[1]}": v for k, v in prim["stats"].items()},
           "descriptives": {f"{k[0]}|{k[1]}": v for k, v in brand_descriptives(answers, units, prim["stats"]).items()},
           "baseline": baseline(answers_a4, units, brand_stats(answers_a4, units))}
    if not sensitivities:
        return doc
    sp = {k: SEEDS["sensitivities"] for k in SEEDS}
    sens = {}

    def run(name, ans, **kw):
        r = gate_statistics(ans, units, kw.pop("P", P), kw.pop("C", C), comps, active, n_perm, 0, seeds=sp, **kw)
        sens[name] = {"verdicts": r["verdicts"], "gate": r["gate"]["verdict"],
                      "rho": {h: [l["rho_w"] for l in r["legs"][h]] for h in r["legs"]}, "rel3": r["H3"]["rel3"]}
    run("S1_denominator_m", answers, denominator="m")
    run("S2_citations", build_answers([r for r in cat_a4 if r["model_requested"] in models], named, units, classes,
                                      CITED_FIELD))
    run("S3_A4", answers_a4)
    run("S3_C3", [a for a in answers_a4 if a["model"] in PANELS["C3"]])
    for fl in FLOOR_SENS:
        run(f"S4_floor_{fl}", answers, floor=fl)
    s5 = [m for m in PANELS["N3"] if m not in dropped or m == GEM4] if GEM4 in dropped else \
        [m for m in models if m != GEM4]
    run("S5_gemini_" + ("kept" if GEM4 in dropped else "dropped"), [a for a in answers_a4 if a["model"] in s5])
    if inp.get("profiles"):
        P3, C3 = legacy_t3(inp["profiles"], units)
        run("S7_legacy_t3", answers, P={"S0": P3, "S1": P3}, C={"S0": C3, "S1": C3})
    sens["S8_leave_one_substrate_out"] = loso(answers, units, P, C, n_perm)
    run("S9_text_urls", build_answers([r for r in cat_a4 if r["model_requested"] in models], named, units, classes,
                                      PRIMARY_FIELD, with_text_urls=True))
    run("S10_uncentred", answers, centred=False)
    run("S11_without_Denon", answers, exclude=(DENON,))
    doc["sensitivities"] = sens
    doc["verdict_changes"] = {name: {h: (v["verdicts"][h], prim["verdicts"][h]) for h in v.get("verdicts", {})
                                     if v["verdicts"][h] != prim["verdicts"][h]}
                              for name, v in sens.items() if "verdicts" in v}
    return doc


def stage_c2(doc_c1, answers, units, P_S0, sdri_map, collected, n_perm=N_PERM, n_boot=N_BOOT):
    """Stage C2: H7 and SDRI descriptives, appended with their own timestamp (by the caller)."""
    gs = gstar_map(brand_stats(answers, units))
    if not collected:
        return {"H7_Struct_Gap": "UNDETERMINED", "reason": "Part II not collected before Stage C2 (Paper B)"}
    leg = sep_leg(sdri_map, gs, SEEDS["H7_Struct_Gap"], n_perm, n_boot, sided="one")
    side = sep_leg(sdri_map, P_S0, SEEDS["H7_Struct_Gap"], 0, 0)
    return {"H7_Struct_Gap": struct_gap_verdict(leg, collected), "leg": leg, "rho_sdri_p_s0": side["rho_w"],
            "partial_rho_sdri_gstar_given_p_s0": partial_rho(sdri_map, gs, P_S0)}


# =========================================================================== guard and entry point
def _tag_exists(tag):
    r = subprocess.run(["git", "tag", "--list", tag], cwd=str(PHASE), capture_output=True, text=True)
    return r.stdout.strip() == tag


V042_TAG = "v0.42-prereg-r1"
V042_PINS = {"osf/v42/scripts/code_t4_v0_42.py": "2d36735d512cf9e13b74010ba5a7f655fc7de0bc",
             "osf/v42/scripts/score_v0_42.py": "884b02cd64438ec031f3967c6b2120c25bc286a3"}   # git blobs (section 0)


def v042_pins_ok():
    """MQ7: v0.42's coder and scorer at tag v0.42-prereg-r1 equal the blobs pinned in section 0 (local git only)."""
    out = {}
    for path, blob in V042_PINS.items():
        r = subprocess.run(["git", "rev-parse", f"{V042_TAG}:{path}"], cwd=str(PHASE), capture_output=True, text=True)
        out[path] = {"pinned": blob, "at_tag": r.stdout.strip() or None, "match": r.stdout.strip() == blob}
    return out


def guard(stage):
    """Refuse Stage C1/C2 unless tag v1.13-prereg-r1 and the anchor exist (checked before anything is read)."""
    if not (_tag_exists(PREREG_TAG) and ANCHOR.exists()):
        raise Refused(f"REFUSED: Stage {stage} needs tag {PREREG_TAG} and {ANCHOR.name} (not locked).")
    anchor = json.loads(ANCHOR.read_text(encoding="utf-8"))
    mq7 = mq7_frozen_lists(anchor)
    pins = v042_pins_ok()
    if not all(v["match"] for v in mq7.values()) or not all(v["match"] for v in pins.values()):
        raise Refused(f"HALT (MQ7): frozen input mismatch {mq7} {pins}")
    if unresolved_units(load_brand_domains()):
        raise Refused("REFUSED: brand_domains_v1_13.csv still has UNRESOLVED rows")
    return anchor


def _load_inputs(a, anchor):
    units, classes = load_brand_domains(), load_classes()
    coded_a, coded_b = [], []
    for sub in SUBSTRATES:
        for ph, acc in (("a", coded_a), ("b", coded_b)):
            p = Path(a.coded) / f"{sub}_phase_{ph}.csv"
            if p.exists():
                acc.extend(read_csv(p))
    return {"records": read_jsonl(a.t4), "coded_a": coded_a, "coded_b": coded_b,
            "brand_table": read_csv(a.brand_table), "units": units, "classes": classes,
            "active": activation(anchor), "comparators": {}}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--stage", choices=["C1", "C2"])
    ap.add_argument("--t4", help="osf/v42/data/t4_raw.jsonl")
    ap.add_argument("--coded", help="directory with the v0.42 coder tables")
    ap.add_argument("--brand-table", help="v0.42 brand table (pi_N3_<c>, phi_N3_<c>)")
    ap.add_argument("--sdri", default=str(PHASE / "audit" / "v1_13_sdri.csv"), help="Stage C2: audit output")
    ap.add_argument("--out", default=str(PHASE / "v1_13_verdicts.json"))
    a = ap.parse_args(argv)
    if not a.stage:
        print(__doc__)
        return 0
    anchor = guard(a.stage)
    inp = _load_inputs(a, anchor)
    if a.stage == "C1":
        doc = stage_c1(inp)
        Path(a.out).write_text(json.dumps(doc, indent=2, default=str), encoding="utf-8")
        print(f"Stage C1 gate: {doc['gate']['verdict']} -> {a.out}")
        return 0
    doc = json.loads(Path(a.out).read_text(encoding="utf-8"))          # Stage C2 appends to the C1 file
    units = inp["units"]
    recs = dedupe_calls(inp["records"])
    answered = {r["call_id"] for r in recs if is_answered(r)}
    answers = build_answers(select_calls(recs, doc["panel_models"], "S1", "B"),
                            named_index(inp["coded_b"], units), units, inp["classes"])
    p_s0 = p_t4(inp["brand_table"], inp["coded_a"], units, "S0", PANELS["N3"], answered)
    collected = Path(a.sdri).exists()
    c2 = stage_c2(doc, answers, units, p_s0, read_sdri(a.sdri, units) if collected else {}, collected)
    c2["appended_utc"] = datetime.now(timezone.utc).isoformat()
    doc["stage_C2"] = c2
    Path(a.out).write_text(json.dumps(doc, indent=2, default=str), encoding="utf-8")
    print(f"Stage C2 H7: {c2['H7_Struct_Gap']} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
