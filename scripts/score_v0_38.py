#!/usr/bin/env python3
"""
AIAS v0.38 — scoring. Locked at tag v0.38-prereg-r1 BEFORE acquisition.
Implements PRE_REGISTRATION_v0_38.md sections 2, 3.3 and 5 exactly.

Inputs : osf/v38/data/v38_raw.json
         osf/v38/registries/brands_home_roasters_v0.38.json
         osf/v38/prereg/probes_v0_38.json
Outputs: osf/v38/data/v38_coded.csv      one row per response
         osf/v38/data/v38_mentions.csv   one row per response x registry brand mentioned
         osf/v38/data/v38_tables.json    aggregates used by figures and report
         osf/v38/v38_verdicts.json       confirmatory verdicts + manipulation check

Usage: python3 scripts/score_v0_38.py [--raw PATH] [--outdir PATH]
"""
import argparse
import csv
import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path("/Users/pablou/aias")
REGISTRY_PATH = ROOT / "osf/v38/registries/brands_home_roasters_v0.38.json"
PROBES_PATH = ROOT / "osf/v38/prereg/probes_v0_38.json"
SLOTS = ["M1", "M2", "M3", "M4", "M5", "M6"]
PRE_BOUNDARY = {"M3", "M4"}           # GPT-4o, GPT-4o-mini: Oct 2023 cutoff
SEED, N_PERM = 38, 10000
FOCAL = "R01"

# ---- thresholds (pre-registration section 2) ----
TIER_DELTA_MIN, ALPHA = 0.20, 0.05
DEFAULT_MARGIN_MIN = 0.10
LEGACY_CONFIRM, LEGACY_PARTIAL, LEGACY_MIN_N = 0.50, 0.20, 10
MC_MAX_R2_SHARE = 0.10

HEATING_RIGHT = re.compile(r"\binduction\b", re.I)
HEATING_WRONG = re.compile(r"\b(gas|propane|convection|hot[- ]air|fluid[- ]bed|radiant|infrared|halogen)\b", re.I)
QTY = re.compile(r"(\d+(?:\.\d+)?)\s*(kg|kilograms?|kilos?|g|grams?|lbs?|pounds?)\b", re.I)
PRICE = re.compile(r"\b(expensive|pricey|pricy|costly|investment|splurge|budget)\b|\$\s?\d", re.I)
DISC_FLAG = re.compile(r"discontinu|no longer|out of production|hard to find|used market|vintage|recall", re.I)
K4_CHANGED = re.compile(r"discontinu\w*|no longer (?:in production|produced|made|manufactured|sold|available)|"
                        r"(?:replaced|succeeded|superseded) by|successor|phased out|end of (?:production|life)", re.I)
K4_CURRENT = re.compile(r"still (?:in production|being (?:made|produced|manufactured|sold)|available|sold|produced|manufactured|in stock)", re.I)


def _rx(a):
    return re.compile(a["pattern"], 0 if a["flags"] == "" else re.I)


class Coder:
    def __init__(self, registry):
        self.brands = []
        for b in registry["brands"]:
            self.brands.append({
                "id": b["id"], "brand": b["brand"], "segment": b["segment"],
                "aliases": [_rx(a) for a in b["aliases"]],
                "exclusions": [(re.compile(e["pattern"], re.I), e["window"]) for e in b["exclusions"]],
            })
        g = registry["aillio_generation_coding"]
        self.anchors = [_rx(a) for a in g["anchors"]]
        self.r1 = [_rx(a) for a in g["r1_family_tokens"]]
        self.r2 = [_rx(a) for a in g["r2_family_tokens"]]
        self.window = int(g["attribution_window_chars"])

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
        """Section 3.3: attribute R1/R2-family tokens to Aillio. Returns (code, r1_tokens, r2_tokens)."""
        if FOCAL not in matches:
            return "Absent", [], []
        anchors = self.anchor_spans(text)
        others = [sp for bid, sps in matches.items() if bid != FOCAL for sp in sps]

        def attributed(tok_start):
            cands = [a for a in anchors if a[1] <= tok_start and tok_start - a[1] <= self.window]
            if not cands:
                return False
            a_end = max(c[1] for c in cands)
            return not any(s >= a_end and e <= tok_start for s, e in others)

        r1 = [m.group(0) for rx in self.r1 for m in rx.finditer(text) if attributed(m.start())]
        r2 = [m.group(0) for rx in self.r2 for m in rx.finditer(text) if attributed(m.start())]
        if r1 and r2:
            code = "Both"
        elif r1:
            code = "R1-only"
        elif r2:
            code = "R2-only"
        else:
            code = "Unspecified"
        return code, r1, r2

    def aillio_windows(self, text, half=200):
        return [text[max(0, s - half): e + half] for s, e in self.anchor_spans(text)]


def k4_code(text):
    if K4_CHANGED.search(text):
        return "Superseded"
    if K4_CURRENT.search(text):
        return "Current"
    return "Unclear"


def to_kg(v, unit):
    u = unit.lower()
    if u.startswith("kg") or u.startswith("kilo"):
        return v
    if u in ("g", "gram", "grams"):
        return v / 1000.0
    return v * 0.453592  # lb / lbs / pound(s)


def grounding(coder, text):
    """D4 candidates (exploratory; audited). heating in {correct, incorrect-candidate, none}; batch = max kg stated near Aillio."""
    wins = coder.aillio_windows(text)
    joined = " ".join(wins)
    if not wins:
        return None, None, []
    heating = "correct" if HEATING_RIGHT.search(joined) else ("incorrect-candidate" if HEATING_WRONG.search(joined) else "none")
    qty = [round(to_kg(float(v), u), 3) for v, u in QTY.findall(joined)]
    batch = None
    if qty:
        mx = max(qty)
        batch = "correct" if 0.9 <= mx <= 1.3 else "incorrect-candidate"
    return heating, batch, qty


def wilson(k, n, z=1.959964):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 4), round(c + h, 4))


def tier_permutation(rows, n_perm=N_PERM, seed=SEED):
    """One-sided stratified permutation test of Presence(E u P) - Presence(B); labels shuffled within model."""
    by_model = defaultdict(list)
    for r in rows:
        by_model[r["model_slot"]].append((1 if r["tier"] in ("E", "P") else 0, r["aillio"]))

    def delta(groups):
        ep = [y for g in groups.values() for t, y in g if t == 1]
        b = [y for g in groups.values() for t, y in g if t == 0]
        return (sum(ep) / len(ep)) - (sum(b) / len(b))

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


def score(raw, registry, probes):
    coder = Coder(registry)
    names = {b["id"]: b["brand"] for b in registry["brands"]}
    seg = {b["id"]: b["segment"] for b in registry["brands"]}
    coded, mentions = [], []
    for r in raw:
        text = r.get("response") or ""
        ok = r.get("status") == "ok"
        mt = coder.brand_matches(text) if ok else {}
        order = coder.first_mention_order(mt)
        gen, r1, r2 = coder.generation(text, mt) if ok else ("Missing", [], [])
        heat, batch, qty = grounding(coder, text) if ok and r["kind"] == "recommendation" and FOCAL in mt else (None, None, [])
        price = bool(PRICE.search(" ".join(coder.aillio_windows(text)))) if ok and FOCAL in mt else None
        row = {
            "probe_id": r["probe_id"], "tier": r["tier"], "kind": r["kind"], "model_slot": r["model_slot"],
            "model_name": r["model_name"], "boundary": r["boundary"], "status": r.get("status"),
            "served_model": r.get("served_model"), "finish_reason": r.get("finish_reason"),
            "n_brands": len(mt), "brands_in_order": ";".join(order),
            "aillio": int(FOCAL in mt), "aillio_first_pos": (order.index(FOCAL) + 1) if FOCAL in mt else "",
            "gen_code": gen, "r1_tokens": ";".join(r1), "r2_tokens": ";".join(r2),
            "k4_code": k4_code(text) if ok and r["probe_id"] == "K4" else "",
            "price_caveat": "" if price is None else int(price),
            "heating_claim": heat or "", "batch_claim": batch or "", "batch_qty_kg": ";".join(map(str, qty)),
            "response_chars": len(text),
        }
        coded.append(row)
        for pos, bid in enumerate(order, 1):
            mentions.append({"probe_id": r["probe_id"], "tier": r["tier"], "model_slot": r["model_slot"],
                             "brand_id": bid, "brand": names[bid], "segment": seg[bid], "position": pos})

    rec = [c for c in coded if c["kind"] == "recommendation" and c["status"] == "ok"]
    probe_rows = [c for c in coded if c["kind"] == "aillio_probe" and c["status"] == "ok"]
    tables = {"n_records": len(coded), "n_ok": sum(c["status"] == "ok" for c in coded)}

    # --- Presence by brand x tier (pooled) and by model ---
    pres = {}
    for tier_key, tiers in (("B", {"B"}), ("E", {"E"}), ("P", {"P"}), ("EP", {"E", "P"}), ("ALL", {"B", "E", "P"})):
        sub = [c for c in rec if c["tier"] in tiers]
        n = len(sub)
        counts = defaultdict(int)
        for c in sub:
            for bid in filter(None, c["brands_in_order"].split(";")):
                counts[bid] += 1
        pres[tier_key] = {"n": n, "presence": {bid: round(counts[bid] / n, 4) if n else None for bid in names}}
    tables["presence_pooled"] = pres
    aillio_by_model = {}
    for m in SLOTS:
        aillio_by_model[m] = {}
        for t in ("B", "E", "P", "EP"):
            tiers = {"E", "P"} if t == "EP" else {t}
            sub = [c for c in rec if c["model_slot"] == m and c["tier"] in tiers]
            aillio_by_model[m][t] = {"k": sum(c["aillio"] for c in sub), "n": len(sub)}
    tables["aillio_by_model_tier"] = aillio_by_model

    # --- first-mention statistics (E u P) ---
    ep = [c for c in rec if c["tier"] in ("E", "P")]
    first_counts = defaultdict(int)
    for c in ep:
        o = [b for b in c["brands_in_order"].split(";") if b]
        if o:
            first_counts[o[0]] += 1
    tables["first_mention_share_EP"] = {bid: round(first_counts[bid] / len(ep), 4) if ep else None for bid in names}
    pos = [int(c["aillio_first_pos"]) for c in ep if c["aillio_first_pos"] != ""]
    tables["aillio_mean_first_pos_EP"] = round(sum(pos) / len(pos), 3) if pos else None

    # --- generation codes ---
    gen_by_model = {m: defaultdict(int) for m in SLOTS}
    for c in rec:
        gen_by_model[c["model_slot"]][c["gen_code"]] += 1
    tables["gen_codes_recommendation_by_model"] = {m: dict(v) for m, v in gen_by_model.items()}
    tables["aillio_probe_codes"] = {f'{c["probe_id"]}|{c["model_slot"]}': {"gen_code": c["gen_code"], "k4_code": c["k4_code"]} for c in probe_rows}

    # ================= confirmatory =================
    verdicts = {"phase": "v0.38", "prereg_tag": "v0.38-prereg-r1"}

    # H_Tier
    rows = [{"model_slot": c["model_slot"], "tier": c["tier"], "aillio": c["aillio"]} for c in rec]
    d_obs, p_val = tier_permutation(rows)
    per_model_delta = {}
    for m in SLOTS:
        a = aillio_by_model[m]
        if a["B"]["n"] and a["EP"]["n"]:
            per_model_delta[m] = round(a["EP"]["k"] / a["EP"]["n"] - a["B"]["k"] / a["B"]["n"], 4)
    if d_obs <= 0:
        v = "FALSIFIED"
    elif p_val >= ALPHA:
        v = "UNDETERMINED"
    elif d_obs >= TIER_DELTA_MIN:
        v = "CONFIRMED"
    else:
        v = "PARTIAL"
    verdicts["H_Tier"] = {"verdict": v, "delta": round(d_obs, 4), "p_one_sided": round(p_val, 5),
                          "presence_B": pres["B"]["presence"][FOCAL], "presence_E": pres["E"]["presence"][FOCAL],
                          "presence_P": pres["P"]["presence"][FOCAL], "presence_EP": pres["EP"]["presence"][FOCAL],
                          "n_B": pres["B"]["n"], "n_EP": pres["EP"]["n"], "per_model_delta": per_model_delta,
                          "models_positive": sum(1 for x in per_model_delta.values() if x > 0),
                          "rule": "CONFIRMED d>=0.20 & p<.05; PARTIAL 0<d<0.20 & p<.05; UNDETERMINED d>0 & p>=.05; FALSIFIED d<=0"}

    # H_Default
    ep_pres = pres["EP"]["presence"]
    ranked = sorted(ep_pres.items(), key=lambda kv: (-(kv[1] or 0), kv[0]))
    top = ranked[0][1]
    leaders = [bid for bid, pv in ranked if pv == top]
    best_other = max(pv for bid, pv in ep_pres.items() if bid != FOCAL)
    margin = round(ep_pres[FOCAL] - best_other, 4)
    if ep_pres[FOCAL] == top and margin >= DEFAULT_MARGIN_MIN:
        v = "CONFIRMED"
    elif ep_pres[FOCAL] == top:
        v = "PARTIAL"
    else:
        v = "FALSIFIED"
    verdicts["H_Default"] = {"verdict": v, "aillio_presence_EP": ep_pres[FOCAL], "margin_over_next": margin,
                             "leaders": leaders, "top5": [(names[b], pv) for b, pv in ranked[:5]],
                             "aillio_first_mention_share_EP": tables["first_mention_share_EP"][FOCAL],
                             "aillio_mean_first_pos_EP": tables["aillio_mean_first_pos_EP"],
                             "rule": "CONFIRMED rank 1 & margin>=0.10; PARTIAL rank 1 (incl. tie) & margin<0.10; FALSIFIED not rank 1"}

    # R2-awareness from K1/K2
    aware = {}
    for m in SLOTS:
        codes = [c["gen_code"] for c in probe_rows if c["model_slot"] == m and c["probe_id"] in ("K1", "K2")]
        aware[m] = any(g in ("R2-only", "Both") for g in codes)
    tables["r2_aware"] = aware

    # H_LegacySlot
    spec = {"R1-only", "R2-only", "Both"}
    aset = [c for c in rec if aware[c["model_slot"]] and c["gen_code"] in spec]
    k_leg = sum(c["gen_code"] == "R1-only" for c in aset)
    n_leg = len(aset)
    share = round(k_leg / n_leg, 4) if n_leg else None
    if not any(aware.values()) or n_leg < LEGACY_MIN_N:
        v = "UNDETERMINED"
    elif share >= LEGACY_CONFIRM:
        v = "CONFIRMED"
    elif share >= LEGACY_PARTIAL:
        v = "PARTIAL"
    else:
        v = "FALSIFIED"
    per_model_leg = {}
    for m in SLOTS:
        s = [c for c in rec if c["model_slot"] == m and c["gen_code"] in spec]
        per_model_leg[m] = {"k_r1_only": sum(c["gen_code"] == "R1-only" for c in s), "n_specified": len(s),
                            "n_both": sum(c["gen_code"] == "Both" for c in s), "n_r2_only": sum(c["gen_code"] == "R2-only" for c in s)}
    ctrl = [c for c in rec if c["model_slot"] in PRE_BOUNDARY and c["gen_code"] in spec]
    verdicts["H_LegacySlot"] = {"verdict": v, "legacy_share": share, "k": k_leg, "n": n_leg, "wilson95": wilson(k_leg, n_leg),
                                "r2_aware_models": [m for m in SLOTS if aware[m]], "per_model": per_model_leg,
                                "control_pre_boundary": {"k": sum(c["gen_code"] == "R1-only" for c in ctrl), "n": len(ctrl)},
                                "rule": "R2-aware models only; CONFIRMED >=0.50; PARTIAL 0.20-0.50; FALSIFIED <0.20; UNDETERMINED n<10 or no aware model"}

    # MC_Boundary (all 22 probes, pre-boundary pair)
    allpre = [c for c in coded if c["status"] == "ok" and c["model_slot"] in PRE_BOUNDARY and c["gen_code"] in spec]
    k_r2 = sum(c["gen_code"] in ("R2-only", "Both") for c in allpre)
    r2_share = round(k_r2 / len(allpre), 4) if allpre else None
    passed = (k_r2 == 0) or (r2_share is not None and r2_share <= MC_MAX_R2_SHARE)
    verdicts["MC_Boundary"] = {"pass": passed, "r2_share": r2_share, "k_r2": k_r2, "n_specified": len(allpre),
                               "pre_boundary_r2_aware": {m: aware[m] for m in sorted(PRE_BOUNDARY)},
                               "rule": "pass if R2-family share <= 0.10 (or zero R2 tokens) among pre-boundary generation-specified responses"}

    # ================= descriptives =================
    d = {}
    d["D1_K3_gen_code"] = {c["model_slot"]: c["gen_code"] for c in probe_rows if c["probe_id"] == "K3"}
    d["D2_K4_code"] = {c["model_slot"]: c["k4_code"] for c in probe_rows if c["probe_id"] == "K4"}
    gap = {}
    for m in SLOTS:
        kk = [c for c in probe_rows if c["model_slot"] == m and c["probe_id"] in ("K1", "K2")]
        know = sum(c["gen_code"] in ("R2-only", "Both") for c in kk) / len(kk) if kk else None
        s = per_model_leg[m]
        recr2 = (s["n_r2_only"] + s["n_both"]) / s["n_specified"] if s["n_specified"] else None
        gap[m] = {"knowledge_r2_rate": know, "recommendation_r2_rate": recr2,
                  "gap": round(know - recr2, 4) if (know is not None and recr2 is not None) else None}
    d["D3_knowledge_recommendation_gap"] = gap
    am = [c for c in rec if c["aillio"]]
    d["D4_grounding_candidates"] = {
        "n_aillio_rec": len(am),
        "heating": {k: sum(c["heating_claim"] == k for c in am) for k in ("correct", "incorrect-candidate", "none")},
        "batch": {k: sum(c["batch_claim"] == k for c in am) for k in ("correct", "incorrect-candidate", "")},
        "note": "automated candidates only; report uses audited classification (section 5.6)"}
    d["D5_price_caveat"] = {"k": sum(c["price_caveat"] == 1 for c in am), "n": len(am)}
    phantom = {}
    for bid in ("R29", "R30"):
        hit = [c for c in rec if bid in c["brands_in_order"].split(";")]
        phantom[bid] = {"brand": names[bid], "k": len(hit), "n": len(rec)}
    d["D7_phantom_comparators"] = phantom
    tables["descriptives"] = d
    return coded, mentions, tables, verdicts


def disc_flags(raw, registry):
    """D7 framing: mentions of discontinued brands flagged within +/-150 chars."""
    coder = Coder(registry)
    out = defaultdict(lambda: {"flagged": 0, "unflagged": 0})
    for r in raw:
        if r.get("status") != "ok" or r["kind"] != "recommendation":
            continue
        t = r["response"]
        mt = coder.brand_matches(t)
        for bid in ("R29", "R30"):
            for s, e in mt.get(bid, []):
                key = "flagged" if DISC_FLAG.search(t[max(0, s - 150): e + 150]) else "unflagged"
                out[bid][key] += 1
    return dict(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(ROOT / "osf/v38/data/v38_raw.json"))
    ap.add_argument("--outdir", default=str(ROOT / "osf/v38"))
    args = ap.parse_args()
    raw = json.loads(Path(args.raw).read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    probes = json.loads(PROBES_PATH.read_text(encoding="utf-8"))
    coded, mentions, tables, verdicts = score(raw, registry, probes)
    tables["descriptives"]["D7_framing"] = disc_flags(raw, registry)
    out = Path(args.outdir)
    (out / "data").mkdir(parents=True, exist_ok=True)
    with open(out / "data/v38_coded.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(coded[0].keys()))
        w.writeheader()
        w.writerows(coded)
    with open(out / "data/v38_mentions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["probe_id", "tier", "model_slot", "brand_id", "brand", "segment", "position"])
        w.writeheader()
        w.writerows(mentions)
    (out / "data/v38_tables.json").write_text(json.dumps(tables, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "v38_verdicts.json").write_text(json.dumps(verdicts, indent=2, ensure_ascii=False), encoding="utf-8")
    for h in ("H_LegacySlot", "H_Tier", "H_Default"):
        print(f"{h:14s} {verdicts[h]['verdict']}")
    print(f"MC_Boundary    {'PASS' if verdicts['MC_Boundary']['pass'] else 'FAIL'}")


if __name__ == "__main__":
    main()
