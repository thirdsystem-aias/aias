#!/usr/bin/env python3
"""
AIAS v0.39 — scoring. Locked at tag v0.39-prereg-r1 BEFORE acquisition.
Implements PRE_REGISTRATION_v0_39.md sections 2, 3.3, 3.4 and 5. Forked from scripts/score_v0_38.py.

Inputs : osf/v39/data/v39_raw.json
         osf/v39/registries/brands_commercial_roasters_v0.39.json
         osf/v39/prereg/probes_v0_39.json
         osf/v39/data/v39_audit_commonnoun.json   section 3.3 audit of every Bellwether/Stronghold match
Outputs: osf/v39/data/v39_coded.csv      one row per response
         osf/v39/data/v39_mentions.csv   one row per response x registry brand mentioned
         osf/v39/data/v39_tables.json    aggregates used by figures and report
         osf/v39/v39_verdicts.json       confirmatory verdicts + manipulation checks

The section 3.3 audit file lists every response key that contains a Bellwether (B01) or Stronghold (B06)
match ("audited_keys") and the match offsets judged common-noun uses ("removals"). If the file is missing
or does not cover every such response, all verdicts are written with status PROVISIONAL.

Usage: python3 scripts/score_v0_39.py [--raw PATH] [--audit PATH] [--outdir PATH]
"""
import argparse
import csv
import json
import math
import os
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(os.environ.get("AIAS_ROOT", "/Users/pablou/aias"))
REGISTRY_PATH = ROOT / "osf/v39/registries/brands_commercial_roasters_v0.39.json"
PROBES_PATH = ROOT / "osf/v39/prereg/probes_v0_39.json"
LEGACY_SLOTS = ["M1", "M2", "M3", "M4", "M5", "M6"]
CURRENT_SLOTS = ["C1", "C2", "C3"]
PRE_BOUNDARY = {"M3", "M4"}           # GPT-4o, GPT-4o-mini: Oct 2023 cutoff, before the Shop Roaster (2024-03-07)
SEED, N_PERM = 39, 10000
FOCAL = "B01"
AUDITED = ("B01", "B06")
REC_TIERS = ("G", "C", "R")

# ---- thresholds (pre-registration section 2) ----
CEP_DELTA_MIN, ALPHA = 0.20, 0.05
DEFAULT_MARGIN_MIN = 0.10
FRAME_VENT_MIN, FRAME_VENTLESS_MAX = 0.50, 0.10
SEARCH_DELTA_MIN = 0.20
MC_CONSTRAINT_MIN = 0.20
MC_MAX_SHOP_SHARE = 0.10

QTY = re.compile(r"(\d+(?:\.\d+)?)\s*(kg|kilograms?|kilos?|g|grams?|lbs?|pounds?)\b", re.I)
PRICE = re.compile(r"\b(expensive|pricey|pricy|costly|investment|splurge|budget|price[ds]?|cost[s]?)\b|\$\s?\d", re.I)
POWER = re.compile(r"\b(?:200|208|220|230|240)\s?-?\s?(?:V|VAC|volts?)\b|\b(?:30|50)\s?-?\s?(?:A|amps?|amperes?)\b", re.I)
UNIQUE = re.compile(r"\b(?:only|first|sole|unique(?:ly)?|no other|one of the few)\b", re.I)
VINTAGE = re.compile(r"vintage|antique|no longer (?:made|produced|manufactured)|discontinu|historic|restor|used market|out of production", re.I)


def _rx(a):
    return re.compile(a["pattern"], 0 if a["flags"] == "" else re.I)


def key_of(r):
    return f'{r["probe_id"]}|{r["model_slot"]}|{r.get("condition", "S0")}'


class Coder:
    def __init__(self, registry):
        self.brands = []
        for b in registry["brands"]:
            self.brands.append({
                "id": b["id"], "brand": b["brand"], "stratum": b["stratum"], "segment": b["segment"],
                "aliases": [_rx(a) for a in b["aliases"]],
                "exclusions": [(re.compile(e["pattern"], re.I), e["window"]) for e in b["exclusions"]],
            })
        g = registry["bellwether_generation_coding"]
        self.anchors = [_rx(a) for a in g["anchors"]]
        self.preshop = [_rx(a) for a in g["preshop_tokens"]]
        self.shop = [_rx(a) for a in g["shop_tokens"]]
        self.markers = [_rx(a) for a in g["model_2026_markers"]]
        self.window = int(g["attribution_window_chars"])
        lx = registry["frame_lexicons"]
        self.vent = [re.compile(p, re.I) for p in lx["venting"]]
        self.ventless = [re.compile(p, re.I) for p in lx["ventless"]]

    def brand_matches(self, text):
        """{brand_id: sorted [(start, end)]} after context exclusions."""
        out = {}
        for b in self.brands:
            spans = set()
            for rx in b["aliases"]:
                for m in rx.finditer(text):
                    s, e = m.span()
                    if any(ex.search(text[max(0, s - w): e + w]) for ex, w in b["exclusions"]):
                        continue
                    spans.add((s, e))
            if spans:
                out[b["id"]] = sorted(spans)
        return out

    @staticmethod
    def first_mention_order(matches):
        return [bid for bid, _ in sorted(matches.items(), key=lambda kv: kv[1][0][0])]

    def anchor_spans(self, text):
        return sorted({m.span() for rx in self.anchors for m in rx.finditer(text)})

    def generation(self, text, matches):
        """Section 3.4: attribute pre-Shop / Shop tokens to Bellwether. Returns (code, preshop_tokens, shop_tokens)."""
        if FOCAL not in matches:
            return "Absent", [], []
        anchors = [a for a in self.anchor_spans(text) if a in set(matches[FOCAL])]
        others = [sp for bid, sps in matches.items() if bid != FOCAL for sp in sps]

        def attributed(tok_start):
            cands = [a for a in anchors if a[1] <= tok_start and tok_start - a[1] <= self.window]
            if not cands:
                return False
            a_end = max(c[1] for c in cands)
            return not any(s >= a_end and e <= tok_start for s, e in others)

        pre = [m.group(0) for rx in self.preshop for m in rx.finditer(text) if attributed(m.start())]
        shop = [m.group(0) for rx in self.shop for m in rx.finditer(text) if attributed(m.start())]
        if pre and shop:
            code = "Both"
        elif pre:
            code = "PreShop-only"
        elif shop:
            code = "Shop-only"
        else:
            code = "Unspecified"
        return code, pre, shop

    def windows(self, text, spans, half):
        return [text[max(0, s - half): e + half] for s, e in spans]

    def frame(self, text):
        return (int(any(r.search(text) for r in self.vent)), int(any(r.search(text) for r in self.ventless)))

    def has_ventless(self, text):
        return any(r.search(text) for r in self.ventless)

    def markers_2026(self, text):
        return [m.group(0) for r in self.markers for m in r.finditer(text)]


def to_kg(v, unit):
    u = unit.lower()
    if u.startswith("kg") or u.startswith("kilo"):
        return v
    if u in ("g", "gram", "grams"):
        return v / 1000.0
    return v * 0.453592  # lb / lbs / pound(s)


def k5_class(kg):
    if kg is None:
        return ""
    if 1.4 <= kg <= 1.6:
        return "Shop Roaster"
    if 2.5 <= kg <= 2.9:
        return "Series 2"
    return "other"


def k3_candidate(coder, text):
    """Automated candidate for D2 (audited): does the K3 answer say no venting is needed?"""
    ventless = coder.has_ventless(text)
    vent, _ = coder.frame(text)
    if ventless:
        return "no-venting-claimed"
    if vent:
        return "venting-mentioned"
    return "neither"


def wilson(k, n, z=1.959964):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 4), round(c + h, 4))


def share(k, n):
    return round(k / n, 4) if n else None


def stratified_permutation(rows, label_fn, y_key, n_perm=N_PERM, seed=SEED):
    """One-sided test of mean(y | label=1) - mean(y | label=0); labels shuffled within model_slot."""
    by_model = defaultdict(list)
    for r in rows:
        by_model[r["model_slot"]].append((label_fn(r), r[y_key]))

    def delta(groups):
        a = [y for g in groups.values() for t, y in g if t == 1]
        b = [y for g in groups.values() for t, y in g if t == 0]
        return (sum(a) / len(a)) - (sum(b) / len(b))

    obs = delta(by_model)
    rng = random.Random(seed)
    ge = 0
    for _ in range(n_perm):
        perm = {}
        for m, g in by_model.items():
            labels = [t for t, _ in g]
            rng.shuffle(labels)
            perm[m] = [(labels[i], g[i][1]) for i in range(len(g))]
        if delta(perm) >= obs - 1e-12:
            ge += 1
    return obs, (1 + ge) / (1 + n_perm)


def mcnemar_one_sided(b, c):
    """P(X >= b), X ~ Binomial(b + c, 0.5); p = 1 when there are no discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    return sum(math.comb(n, k) for k in range(b, n + 1)) / 2 ** n


def verdict_effect(d, p, dmin):
    if d <= 0:
        return "FALSIFIED"
    if p >= ALPHA:
        return "UNDETERMINED"
    return "CONFIRMED" if d >= dmin else "PARTIAL"


def load_audit(path, coded_keys_needing_audit):
    """Returns (removals {key: {brand: set(starts)}}, complete, missing_keys)."""
    removals = defaultdict(lambda: defaultdict(set))
    if not path or not Path(path).exists():
        return removals, False, sorted(coded_keys_needing_audit)
    a = json.loads(Path(path).read_text(encoding="utf-8"))
    for x in a.get("removals", []):
        removals[x["key"]][x["brand_id"]].add(int(x["start"]))
    audited = set(a.get("audited_keys", []))
    missing = sorted(set(coded_keys_needing_audit) - audited)
    return removals, not missing, missing


def domain(u):
    try:
        h = urlparse(u or "").netloc.lower()
        return h[4:] if h.startswith("www.") else h
    except Exception:
        return ""


GOOGLE_REDIRECT = "vertexaisearch.cloud.google.com"


def source_domain(item):
    """Domain of a cited or consulted source. Gemini grounding URLs are Google redirects whose title carries the
    source domain (observed in the pre-lock feasibility check), so the title is used for those."""
    item = item or {}
    dom = domain(item.get("url"))
    if dom == GOOGLE_REDIRECT or dom.endswith("." + GOOGLE_REDIRECT):
        t = (item.get("title") or "").strip().lower()
        return t[4:] if t.startswith("www.") else t
    return dom


def score(raw, registry, probes, audit_path=None):
    coder = Coder(registry)
    names = {b["id"]: b["brand"] for b in registry["brands"]}
    stratum = {b["id"]: b["stratum"] for b in registry["brands"]}
    seg = {b["id"]: b["segment"] for b in registry["brands"]}
    show_floor = {bid for bid, s in stratum.items() if s == "S"}
    legacy_brands = [b["id"] for b in registry["brands"] if b["segment"] == "legacy"]

    # pass 1: raw matches, to know which responses need the section 3.3 audit
    pre = []
    for r in raw:
        text = r.get("response") or ""
        ok = r.get("status") == "ok"
        pre.append((r, text, ok, coder.brand_matches(text) if ok else {}))
    need = {key_of(r) for r, _, ok, mt in pre if ok and any(b in mt for b in AUDITED)}
    removals, audit_complete, unaudited = load_audit(audit_path, need)

    coded, mentions = [], []
    for r, text, ok, mt in pre:
        k = key_of(r)
        for bid in AUDITED:  # section 3.3: remove common-noun uses judged in the audit
            if bid in mt and removals.get(k, {}).get(bid):
                kept = [sp for sp in mt[bid] if sp[0] not in removals[k][bid]]
                if kept:
                    mt[bid] = kept
                else:
                    del mt[bid]
        order = coder.first_mention_order(mt)
        gen, pre_t, shop_t = coder.generation(text, mt) if ok else ("Missing", [], [])
        vent, vless = coder.frame(text) if ok else (0, 0)
        fw = coder.windows(text, mt.get(FOCAL, []), 200)
        joined = " ".join(fw)
        qty = [round(to_kg(float(v), u), 3) for v, u in QTY.findall(joined)] if fw else []
        kmax = max(qty) if qty else None
        uniq = int(bool(fw) and any(UNIQUE.search(w) and coder.has_ventless(w) for w in coder.windows(text, mt.get(FOCAL, []), 150)))
        other_ventless = sorted({bid for bid, sps in mt.items() if bid != FOCAL
                                 and any(coder.has_ventless(w) for w in coder.windows(text, sps, 150))})
        srch = r.get("search") or {}
        cites = [source_domain(c) for c in (srch.get("citations") or [])]
        sources = [s.get("url") for s in (srch.get("sources") or [])]
        row = {
            "key": k, "probe_id": r["probe_id"], "tier": r["tier"], "kind": r["kind"],
            "arm": r.get("arm", "L"), "condition": r.get("condition", "S0"),
            "model_slot": r["model_slot"], "model_name": r["model_name"], "boundary": r.get("boundary"),
            "status": r.get("status"), "served_model": r.get("served_model"), "finish_reason": r.get("finish_reason"),
            "n_brands": len(mt), "brands_in_order": ";".join(order),
            "bellwether": int(FOCAL in mt), "bellwether_first_pos": (order.index(FOCAL) + 1) if FOCAL in mt else "",
            "show_floor_any": int(any(b in show_floor for b in mt)),
            "gen_code": gen, "preshop_tokens": ";".join(pre_t), "shop_tokens": ";".join(shop_t),
            "series1_named": int(any(re.match(r"(?i)series\s?(?:1|one)$", t) for t in pre_t)),
            "markers_2026": ";".join(coder.markers_2026(text)) if ok else "",
            "vent": vent, "ventless": vless,
            "k3_candidate": k3_candidate(coder, text) if ok and r["probe_id"] == "K3" else "",
            "k5_qty_kg": kmax if (ok and r["probe_id"] == "K5" and kmax is not None) else "",
            "k5_class": k5_class(kmax) if (ok and r["probe_id"] == "K5") else "",
            "power_claim": int(bool(POWER.search(joined))) if fw else "",
            "price_caveat": int(bool(PRICE.search(joined))) if fw else "",
            "unique_claim_candidate": uniq if fw else "",
            "ventless_other_brands": ";".join(other_ventless),
            "n_searches": srch.get("n_searches", "") if r.get("condition") == "S1" else "",
            "n_sources": len(sources) if r.get("condition") == "S1" else "",
            "cites_bellwether_domain": int(any(dm.endswith("bellwethercoffee.com") for dm in cites)) if r.get("condition") == "S1" else "",
            "response_chars": len(text),
        }
        coded.append(row)
        for pos, bid in enumerate(order, 1):
            mentions.append({"key": k, "probe_id": r["probe_id"], "tier": r["tier"], "arm": row["arm"],
                             "condition": row["condition"], "model_slot": r["model_slot"], "brand_id": bid,
                             "brand": names[bid], "stratum": stratum[bid], "segment": seg[bid], "position": pos})

    okrows = [c for c in coded if c["status"] == "ok"]

    def sel(arm=None, cond=None, tiers=None, slots=None, kind=None):
        return [c for c in okrows if (arm is None or c["arm"] == arm) and (cond is None or c["condition"] == cond)
                and (tiers is None or c["tier"] in tiers) and (slots is None or c["model_slot"] in slots)
                and (kind is None or c["kind"] == kind)]

    def presence_table(rows):
        n = len(rows)
        cnt = Counter(b for c in rows for b in filter(None, c["brands_in_order"].split(";")))
        return {"n": n, "presence": {bid: share(cnt[bid], n) for bid in names}}

    tables = {"n_records": len(coded), "n_ok": len(okrows), "audit_complete": audit_complete,
              "unaudited_keys": unaudited}
    cells = (("L", "S0"), ("C", "S0"), ("C", "S1"))
    pres = {}
    for arm, cond in cells:
        for tk, tiers in (("F", ("F",)), ("G", ("G",)), ("C", ("C",)), ("R", ("R",)), ("GC", ("G", "C")),
                          ("REC", REC_TIERS), ("K", ("K",))):
            pres[f"{arm}|{cond}|{tk}"] = presence_table(sel(arm, cond, tiers))
    tables["presence"] = pres
    focal_by_model = {}
    for arm, cond in cells:
        for m in (LEGACY_SLOTS if arm == "L" else CURRENT_SLOTS):
            for tk in ("F", "G", "C", "R"):
                rows = sel(arm, cond, (tk,), (m,))
                focal_by_model[f"{arm}|{cond}|{m}|{tk}"] = {"k": sum(c["bellwether"] for c in rows), "n": len(rows)}
    tables["bellwether_by_model_tier"] = focal_by_model

    # ================= confirmatory =================
    status = "FINAL" if audit_complete else "PROVISIONAL"
    verdicts = {"phase": "v0.39", "prereg_tag": "v0.39-prereg-r1", "status": status,
                "audit_complete": audit_complete, "n_unaudited": len(unaudited)}

    # H_CEP (legacy arm, C vs G, stratified permutation within model)
    gc = sel("L", "S0", ("G", "C"))
    if gc and any(c["tier"] == "C" for c in gc) and any(c["tier"] == "G" for c in gc):
        d_obs, p_val = stratified_permutation(gc, lambda c: 1 if c["tier"] == "C" else 0, "bellwether")
    else:
        d_obs, p_val = 0.0, 1.0
    per_model = {}
    for m in LEGACY_SLOTS:
        a, b = focal_by_model[f"L|S0|{m}|C"], focal_by_model[f"L|S0|{m}|G"]
        if a["n"] and b["n"]:
            per_model[m] = round(a["k"] / a["n"] - b["k"] / b["n"], 4)
    verdicts["H_CEP"] = {"verdict": verdict_effect(d_obs, p_val, CEP_DELTA_MIN), "delta": round(d_obs, 4),
                         "p_one_sided": round(p_val, 5),
                         "presence_G": pres["L|S0|G"]["presence"][FOCAL], "presence_C": pres["L|S0|C"]["presence"][FOCAL],
                         "n_G": pres["L|S0|G"]["n"], "n_C": pres["L|S0|C"]["n"], "per_model_delta": per_model,
                         "models_positive": sum(1 for x in per_model.values() if x > 0),
                         "current_arm_descriptive": {cond: {"G": pres[f"C|{cond}|G"]["presence"][FOCAL],
                                                            "C": pres[f"C|{cond}|C"]["presence"][FOCAL]} for cond in ("S0", "S1")},
                         "rule": "CONFIRMED d>=0.20 & p<.05; PARTIAL 0<d<0.20 & p<.05; UNDETERMINED d>0 & p>=.05; FALSIFIED d<=0"}

    # H_CEPDefault (legacy arm, tier C ranking)
    def ranking(ptab):
        pr = {b: (v or 0) for b, v in ptab["presence"].items()}
        ranked = sorted(pr.items(), key=lambda kv: (-kv[1], kv[0]))
        top = ranked[0][1] if ranked else 0
        best_other = max(v for b, v in pr.items() if b != FOCAL)
        return pr, ranked, top, round(pr[FOCAL] - best_other, 4)

    pr, ranked, top, margin = ranking(pres["L|S0|C"])
    if pr[FOCAL] == top and pr[FOCAL] > 0 and margin >= DEFAULT_MARGIN_MIN:
        v = "CONFIRMED"
    elif pr[FOCAL] == top and pr[FOCAL] > 0:
        v = "PARTIAL"
    else:
        v = "FALSIFIED"
    cl = sel("L", "S0", ("C",))
    firsts = Counter(c["brands_in_order"].split(";")[0] for c in cl if c["brands_in_order"])
    pos = [int(c["bellwether_first_pos"]) for c in cl if c["bellwether_first_pos"] != ""]
    current_rank = {}
    for cond in ("S0", "S1"):
        p2, r2, t2, m2 = ranking(pres[f"C|{cond}|C"])
        current_rank[cond] = {"bellwether_presence": p2[FOCAL], "rank": 1 + sum(1 for b, x in p2.items() if x > p2[FOCAL]),
                              "top5": [(names[b], x) for b, x in r2[:5]]}
    verdicts["H_CEPDefault"] = {"verdict": v, "bellwether_presence_C": pr[FOCAL], "margin_over_next": margin,
                                "rank": 1 + sum(1 for b, x in pr.items() if x > pr[FOCAL]),
                                "top5": [(names[b], x) for b, x in ranked[:5]],
                                "first_mention_share_C": share(firsts[FOCAL], len(cl)),
                                "mean_first_pos_C": round(sum(pos) / len(pos), 3) if pos else None,
                                "current_arm_descriptive": current_rank,
                                "rule": "CONFIRMED rank 1 & margin>=0.10; PARTIAL rank 1 (incl. tie) & margin<0.10; FALSIFIED not rank 1"}

    # H_Frame (legacy arm, tier F)
    fl = sel("L", "S0", ("F",))
    vs, vls = share(sum(c["vent"] for c in fl), len(fl)), share(sum(c["ventless"] for c in fl), len(fl))
    c1 = vs is not None and vs >= FRAME_VENT_MIN
    c2 = vls is not None and vls <= FRAME_VENTLESS_MAX
    verdicts["H_Frame"] = {"verdict": "CONFIRMED" if (c1 and c2) else ("PARTIAL" if (c1 or c2) else "FALSIFIED"),
                           "vent_share": vs, "ventless_share": vls, "n": len(fl),
                           "vent_wilson95": wilson(sum(c["vent"] for c in fl), len(fl)),
                           "ventless_wilson95": wilson(sum(c["ventless"] for c in fl), len(fl)),
                           "current_arm_descriptive": {cond: {"vent_share": share(sum(c["vent"] for c in sel("C", cond, ("F",))), len(sel("C", cond, ("F",)))),
                                                              "ventless_share": share(sum(c["ventless"] for c in sel("C", cond, ("F",))), len(sel("C", cond, ("F",))))}
                                                       for cond in ("S0", "S1")},
                           "rule": "CONFIRMED vent>=0.50 & ventless<=0.10; PARTIAL exactly one; FALSIFIED neither"}

    # H_Search (current arm, G u C, paired S1 vs S0)
    s0 = {(c["probe_id"], c["model_slot"]): c["bellwether"] for c in sel("C", "S0", ("G", "C"))}
    s1 = {(c["probe_id"], c["model_slot"]): c["bellwether"] for c in sel("C", "S1", ("G", "C"))}
    pairs = sorted(set(s0) & set(s1))
    b = sum(1 for p in pairs if s1[p] == 1 and s0[p] == 0)
    c_ = sum(1 for p in pairs if s1[p] == 0 and s0[p] == 1)
    d_s = (sum(s1[p] for p in pairs) - sum(s0[p] for p in pairs)) / len(pairs) if pairs else 0.0
    p_s = mcnemar_one_sided(b, c_)
    per_model_s = {}
    for m in CURRENT_SLOTS:
        mp = [p for p in pairs if p[1] == m]
        if mp:
            per_model_s[m] = round((sum(s1[p] for p in mp) - sum(s0[p] for p in mp)) / len(mp), 4)
    verdicts["H_Search"] = {"verdict": verdict_effect(d_s, p_s, SEARCH_DELTA_MIN), "delta": round(d_s, 4),
                            "p_one_sided": round(p_s, 5), "n_pairs": len(pairs), "b_s1_only": b, "c_s0_only": c_,
                            "presence_S0": share(sum(s0[p] for p in pairs), len(pairs)),
                            "presence_S1": share(sum(s1[p] for p in pairs), len(pairs)),
                            "per_model_delta": per_model_s,
                            "rule": "exact one-sided McNemar; CONFIRMED d>=0.20 & p<.05; PARTIAL 0<d<0.20 & p<.05; UNDETERMINED d>0 & p>=.05; FALSIFIED d<=0"}

    # MC_Constraint (legacy arm)
    gl, cl2 = sel("L", "S0", ("G",)), sel("L", "S0", ("C",))
    vg, vc = share(sum(c["ventless"] for c in gl), len(gl)), share(sum(c["ventless"] for c in cl2), len(cl2))
    diff = round((vc or 0) - (vg or 0), 4)
    verdicts["MC_Constraint"] = {"pass": diff >= MC_CONSTRAINT_MIN, "ventless_share_G": vg, "ventless_share_C": vc,
                                 "difference": diff, "rule": "pass if ventless share C - G >= 0.20 (legacy arm)"}

    # Shop-awareness (per model x condition) from K1/K2
    spec = {"PreShop-only", "Shop-only", "Both"}
    aware = {}
    for c in okrows:
        if c["probe_id"] in ("K1", "K2"):
            mk = f'{c["model_slot"]}|{c["condition"]}'
            aware[mk] = aware.get(mk, False) or c["gen_code"] in ("Shop-only", "Both")
    tables["shop_aware"] = aware

    # MC_Boundary (pre-boundary pair, all probes)
    allpre = [c for c in okrows if c["model_slot"] in PRE_BOUNDARY and c["gen_code"] in spec]
    k_shop = sum(c["gen_code"] in ("Shop-only", "Both") for c in allpre)
    shop_share = share(k_shop, len(allpre))
    verdicts["MC_Boundary"] = {"pass": (k_shop == 0) or (shop_share is not None and shop_share <= MC_MAX_SHOP_SHARE),
                               "shop_share": shop_share, "k_shop": k_shop, "n_specified": len(allpre),
                               "pre_boundary_shop_aware": {m: aware.get(f"{m}|S0", False) for m in sorted(PRE_BOUNDARY)},
                               "rule": "pass if Shop-only/Both share <= 0.10 (or zero Shop tokens) among pre-boundary generation-specified responses"}

    # ================= descriptives =================
    d = {}
    leg_rows = [c for c in okrows if (c["kind"] == "recommendation" or c["probe_id"] == "K4")
                and aware.get(f'{c["model_slot"]}|{c["condition"]}', False) and c["gen_code"] in spec]
    k_leg = sum(c["gen_code"] == "PreShop-only" for c in leg_rows)
    d["D1_generation"] = {
        "k_probe_codes": {c["key"]: c["gen_code"] for c in okrows if c["probe_id"] in ("K1", "K2", "K4")},
        "shop_aware": aware,
        "legacy_share_shop_aware": {"k": k_leg, "n": len(leg_rows), "share": share(k_leg, len(leg_rows)),
                                    "wilson95": wilson(k_leg, len(leg_rows))},
        "series1_named": {"k": sum(c["series1_named"] for c in okrows), "n_bellwether": sum(c["bellwether"] for c in okrows)},
        "gen_codes_by_cell": {f"{arm}|{cond}": dict(Counter(c["gen_code"] for c in sel(arm, cond) if c["bellwether"]))
                              for arm, cond in cells},
    }
    d["D2_grounding_candidates"] = {
        "k3": {c["key"]: c["k3_candidate"] for c in okrows if c["probe_id"] == "K3"},
        "k5": {c["key"]: {"kg": c["k5_qty_kg"], "class": c["k5_class"], "gen_code": c["gen_code"]} for c in okrows if c["probe_id"] == "K5"},
        "power_claims": sum(1 for c in okrows if c["power_claim"] == 1),
        "note": "automated candidates only; the report uses the audited classification (section 5.7)"}
    bw = [c for c in okrows if c["bellwether"]]
    d["D3_claim_reproduction_candidates"] = {"k": sum(1 for c in bw if c["unique_claim_candidate"] == 1), "n": len(bw),
                                             "keys": [c["key"] for c in bw if c["unique_claim_candidate"] == 1]}
    va = Counter(b for c in okrows for b in filter(None, c["ventless_other_brands"].split(";")))
    d["D4_ventless_attribution_candidates"] = {names[b]: n for b, n in va.most_common()}
    d5 = {}
    for arm, cond in cells:
        rows = sel(arm, cond, REC_TIERS)
        ments = [m for m in mentions if m["arm"] == arm and m["condition"] == cond and m["tier"] in REC_TIERS
                 and any(c["key"] == m["key"] and c["status"] == "ok" for c in rows)]
        ptab = presence_table(rows)
        non_s = sorted(((b, v or 0) for b, v in ptab["presence"].items() if b not in show_floor), key=lambda kv: -kv[1])
        d5[f"{arm}|{cond}"] = {"n": len(rows), "share_responses_with_show_floor_brand": share(sum(c["show_floor_any"] for c in rows), len(rows)),
                               "share_mentions_to_show_floor": share(sum(1 for m in ments if m["stratum"] == "S"), len(ments)),
                               "show_floor_presence": {names[b]: ptab["presence"][b] for b in sorted(show_floor)},
                               "top_non_show_floor": [(names[b], v) for b, v in non_s[:5]]}
    d["D5_show_floor_vs_ai_shelf"] = d5
    s1rows = sel("C", "S1")
    dom = Counter(dm for r in raw if r.get("condition") == "S1" and r.get("status") == "ok"
                  for dm in {source_domain(c) for c in ((r.get("search") or {}).get("citations") or [])} if dm)
    d["D7_retrieval"] = {"n_s1": len(s1rows),
                         "mean_searches": round(sum(int(c["n_searches"] or 0) for c in s1rows) / len(s1rows), 3) if s1rows else None,
                         "share_citing_bellwethercoffee": share(sum(int(c["cites_bellwether_domain"] or 0) for c in s1rows), len(s1rows)),
                         "top_cited_domains": dom.most_common(15),
                         "markers_2026_in_K1_K2": {c["key"]: c["markers_2026"] for c in okrows if c["probe_id"] in ("K1", "K2") and c["markers_2026"]}}
    coder2 = coder
    leg = {}
    for bid in legacy_brands:
        flagged = unflagged = 0
        for r in raw:
            if r.get("status") != "ok" or r["kind"] != "recommendation":
                continue
            for s, e in coder2.brand_matches(r["response"]).get(bid, []):
                if VINTAGE.search(r["response"][max(0, s - 150): e + 150]):
                    flagged += 1
                else:
                    unflagged += 1
        leg[names[bid]] = {"responses": sum(1 for c in okrows if bid in c["brands_in_order"].split(";")),
                           "flagged": flagged, "unflagged": unflagged}
    d["D8_legacy_brands"] = leg
    bwrec = [c for c in okrows if c["bellwether"] and c["kind"] == "recommendation"]
    d["D9_price_caveat"] = {"k": sum(1 for c in bwrec if c["price_caveat"] == 1), "n": len(bwrec)}

    # D10: five-model sensitivity, legacy arm without M5 (Gemini 2.5 Flash shares its 2,048-token cap with
    # thinking tokens; v0.38 DEVIATIONS Note 1). Descriptive only; verdicts stay on six models.
    five = [m for m in LEGACY_SLOTS if m != "M5"]
    gc5 = sel("L", "S0", ("G", "C"), five)
    if gc5 and any(c["tier"] == "C" for c in gc5) and any(c["tier"] == "G" for c in gc5):
        d5_obs, p5 = stratified_permutation(gc5, lambda c: 1 if c["tier"] == "C" else 0, "bellwether")
    else:
        d5_obs, p5 = 0.0, 1.0
    pr5, ranked5, top5, margin5 = ranking(presence_table(sel("L", "S0", ("C",), five)))
    f5 = sel("L", "S0", ("F",), five)
    m5 = [c for c in coded if c["arm"] == "L" and c["model_slot"] == "M5" and c["status"] == "ok"]
    d["D10_five_model_sensitivity"] = {
        "models": five,
        "H_CEP": {"delta": round(d5_obs, 4), "p_one_sided": round(p5, 5)},
        "H_CEPDefault": {"bellwether_presence_C": pr5[FOCAL], "rank": 1 + sum(1 for b, x in pr5.items() if x > pr5[FOCAL]),
                         "margin_over_next": margin5},
        "H_Frame": {"vent_share": share(sum(c["vent"] for c in f5), len(f5)),
                    "ventless_share": share(sum(c["ventless"] for c in f5), len(f5)), "n": len(f5)},
        "m5_capped_share": share(sum(1 for c in m5 if "MAX_TOKENS" in str(c["finish_reason"] or "")), len(m5)),
        "note": "descriptive; verdicts are computed on the six-model panel"}
    tables["descriptives"] = d
    return coded, mentions, tables, verdicts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(ROOT / "osf/v39/data/v39_raw.json"))
    ap.add_argument("--audit", default=str(ROOT / "osf/v39/data/v39_audit_commonnoun.json"))
    ap.add_argument("--outdir", default=str(ROOT / "osf/v39"))
    args = ap.parse_args()
    raw = json.loads(Path(args.raw).read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    probes = json.loads(PROBES_PATH.read_text(encoding="utf-8"))
    coded, mentions, tables, verdicts = score(raw, registry, probes, args.audit)
    out = Path(args.outdir)
    (out / "data").mkdir(parents=True, exist_ok=True)
    with open(out / "data/v39_coded.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(coded[0].keys()))
        w.writeheader()
        w.writerows(coded)
    with open(out / "data/v39_mentions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["key", "probe_id", "tier", "arm", "condition", "model_slot", "brand_id",
                                          "brand", "stratum", "segment", "position"])
        w.writeheader()
        w.writerows(mentions)
    (out / "data/v39_tables.json").write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "v39_verdicts.json").write_text(json.dumps(verdicts, indent=2, ensure_ascii=False), encoding="utf-8")
    tag = "" if verdicts["status"] == "FINAL" else f"  [PROVISIONAL: {verdicts['n_unaudited']} responses not yet audited]"
    for h in ("H_CEP", "H_CEPDefault", "H_Frame", "H_Search"):
        print(f"{h:14s} {verdicts[h]['verdict']}{tag}")
    for mc in ("MC_Constraint", "MC_Boundary"):
        print(f"{mc:14s} {'PASS' if verdicts[mc]['pass'] else 'FAIL'}{tag}")


if __name__ == "__main__":
    main()
