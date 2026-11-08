#!/usr/bin/env python3
"""
AIAS v0.39 — independent re-computation of the confirmatory numbers (check step; NOT part of the locked scoring).

Recomputes every verdict input from the raw responses, the registry and the section 3.3 audit file WITHOUT
importing scripts/score_v0_39.py: brand matching, Bellwether presence, frame lexicons, the stratified
permutation (own RNG stream) and the exact McNemar test are re-implemented here, then compared with
osf/v39/v39_verdicts.json. Any mismatch is printed and the exit code is 1.

Usage: AIAS_ROOT=<repo> python3 scripts/verify_v0_39.py
"""
import csv
import json
import math
import os
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", "/Users/pablou/aias"))
V = ROOT / "osf/v39"
raw = json.loads((V / "data/v39_raw.json").read_text(encoding="utf-8"))
reg = json.loads((V / "registries/brands_commercial_roasters_v0.39.json").read_text(encoding="utf-8"))
audit = json.loads((V / "data/v39_audit_commonnoun.json").read_text(encoding="utf-8"))
verd = json.loads((V / "v39_verdicts.json").read_text(encoding="utf-8"))
with open(V / "data/v39_coded.csv", encoding="utf-8") as f:
    coded = {r["key"]: r for r in csv.DictReader(f)}

fails = []


def check(label, mine, theirs, tol=1e-9):
    same = (abs(mine - theirs) <= tol) if isinstance(mine, (int, float)) and isinstance(theirs, (int, float)) else mine == theirs
    print(f"  [{'OK ' if same else 'XX '}] {label}: independent={mine} scorer={theirs}")
    if not same:
        fails.append(label)


def key(r):
    return f'{r["probe_id"]}|{r["model_slot"]}|{r.get("condition", "S0")}'


# ---- brand matching, re-implemented from the registry ----
brands = []
for b in reg["brands"]:
    brands.append((b["id"], [re.compile(a["pattern"], 0 if a["flags"] == "" else re.I) for a in b["aliases"]],
                   [(re.compile(e["pattern"], re.I), e["window"]) for e in b["exclusions"]]))
removed = defaultdict(set)
for x in audit.get("removals", []):
    removed[(x["key"], x["brand_id"])].add(int(x["start"]))


def present(text, k):
    out = set()
    for bid, aliases, excl in brands:
        starts = set()
        for rx in aliases:
            for m in rx.finditer(text):
                s, e = m.span()
                if any(ex.search(text[max(0, s - w): e + w]) for ex, w in excl):
                    continue
                starts.add(s)
        starts -= removed.get((k, bid), set())
        if starts:
            out.add(bid)
    return out


lx = reg["frame_lexicons"]
VENT = [re.compile(p, re.I) for p in lx["venting"]]
LESS = [re.compile(p, re.I) for p in lx["ventless"]]

rows = []
for r in raw:
    if r.get("status") != "ok":
        continue
    t = r.get("response") or ""
    k = key(r)
    rows.append({"key": k, "probe": r["probe_id"], "tier": r["tier"], "arm": r.get("arm", "L"),
                 "cond": r.get("condition", "S0"), "slot": r["model_slot"], "brands": present(t, k),
                 "vent": any(x.search(t) for x in VENT), "less": any(x.search(t) for x in LESS)})
print(f"ok responses: {len(rows)} of {len(raw)} records")

# ---- per-response agreement with the coded table ----
mis = [r["key"] for r in rows if int("B01" in r["brands"]) != int(coded[r["key"]]["bellwether"])]
check("Bellwether presence, per-response disagreements", len(mis), 0)
mis_v = [r["key"] for r in rows if int(r["vent"]) != int(coded[r["key"]]["vent"]) or int(r["less"]) != int(coded[r["key"]]["ventless"])]
check("frame flags, per-response disagreements", len(mis_v), 0)


def sel(arm, cond, tiers, slots=None):
    return [r for r in rows if r["arm"] == arm and r["cond"] == cond and r["tier"] in tiers and (slots is None or r["slot"] in slots)]


def pres(rs, bid="B01"):
    return sum(bid in r["brands"] for r in rs) / len(rs) if rs else None


# ---- H_CEP ----
G, C = sel("L", "S0", ("G",)), sel("L", "S0", ("C",))
d = pres(C) - pres(G)
check("H_CEP presence G", round(pres(G), 4), verd["H_CEP"]["presence_G"])
check("H_CEP presence C", round(pres(C), 4), verd["H_CEP"]["presence_C"])
check("H_CEP delta", round(d, 4), verd["H_CEP"]["delta"])
by = defaultdict(list)
for r in G + C:
    by[r["slot"]].append((r["tier"] == "C", "B01" in r["brands"]))
rng = random.Random(2039)  # own stream, deliberately not the locked seed
ge, N = 0, 20000
for _ in range(N):
    a = b = na = nb = 0
    for g in by.values():
        lab = [t for t, _ in g]
        rng.shuffle(lab)
        for t, (_, y) in zip(lab, g):
            if t:
                a += y; na += 1
            else:
                b += y; nb += 1
    if a / na - b / nb >= d - 1e-12:
        ge += 1
p_ind = (1 + ge) / (1 + N)
print(f"  [info] H_CEP permutation p (independent stream, {N} perms) = {p_ind:.5f}; scorer p = {verd['H_CEP']['p_one_sided']}")
same_side = (p_ind < 0.05) == (verd["H_CEP"]["p_one_sided"] < 0.05)
check("H_CEP significance at .05 agrees", same_side, True)


def effect(dd, p, dmin):
    return "FALSIFIED" if dd <= 0 else ("UNDETERMINED" if p >= 0.05 else ("CONFIRMED" if dd >= dmin else "PARTIAL"))


check("H_CEP verdict", effect(d, p_ind, 0.20), verd["H_CEP"]["verdict"])

# ---- H_CEPDefault ----
cnt = Counter(b for r in C for b in r["brands"])
pr = {b[0]: cnt[b[0]] / len(C) for b in brands}
top = max(pr.values())
other = max(v for b, v in pr.items() if b != "B01")
margin = pr["B01"] - other
v = ("CONFIRMED" if pr["B01"] == top and pr["B01"] > 0 and margin >= 0.10 else
     "PARTIAL" if pr["B01"] == top and pr["B01"] > 0 else "FALSIFIED")
check("H_CEPDefault margin", round(margin, 4), verd["H_CEPDefault"]["margin_over_next"])
check("H_CEPDefault verdict", v, verd["H_CEPDefault"]["verdict"])

# ---- H_Frame ----
F = sel("L", "S0", ("F",))
vs, ls = sum(r["vent"] for r in F) / len(F), sum(r["less"] for r in F) / len(F)
check("H_Frame vent share", round(vs, 4), verd["H_Frame"]["vent_share"])
check("H_Frame ventless share", round(ls, 4), verd["H_Frame"]["ventless_share"])
c1, c2 = vs >= 0.50, ls <= 0.10
check("H_Frame verdict", "CONFIRMED" if c1 and c2 else ("PARTIAL" if c1 or c2 else "FALSIFIED"), verd["H_Frame"]["verdict"])

# ---- H_Search ----
s0 = {(r["probe"], r["slot"]): "B01" in r["brands"] for r in sel("C", "S0", ("G", "C"))}
s1 = {(r["probe"], r["slot"]): "B01" in r["brands"] for r in sel("C", "S1", ("G", "C"))}
pairs = sorted(set(s0) & set(s1))
b = sum(1 for q in pairs if s1[q] and not s0[q])
c = sum(1 for q in pairs if s0[q] and not s1[q])
ds = (sum(s1[q] for q in pairs) - sum(s0[q] for q in pairs)) / len(pairs)
ps = 1.0 if b + c == 0 else sum(math.comb(b + c, i) for i in range(b, b + c + 1)) / 2 ** (b + c)
check("H_Search pairs", len(pairs), verd["H_Search"]["n_pairs"])
check("H_Search b (S1 only)", b, verd["H_Search"]["b_s1_only"])
check("H_Search c (S0 only)", c, verd["H_Search"]["c_s0_only"])
check("H_Search delta", round(ds, 4), verd["H_Search"]["delta"])
check("H_Search p", round(ps, 5), verd["H_Search"]["p_one_sided"])
check("H_Search verdict", effect(ds, ps, 0.20), verd["H_Search"]["verdict"])

# ---- MC_Constraint ----
lg = sum(r["less"] for r in G) / len(G)
lc = sum(r["less"] for r in C) / len(C)
check("MC_Constraint difference", round(lc - lg, 4), verd["MC_Constraint"]["difference"])
check("MC_Constraint pass", (lc - lg) >= 0.20, verd["MC_Constraint"]["pass"])

# ---- audit coverage ----
cover = set(audit.get("audited_keys", []))
raw_need = set()
for r in raw:
    if r.get("status") != "ok":
        continue
    t = r["response"]
    for bid, aliases, excl in brands:
        if bid not in ("B01", "B06"):
            continue
        for rx in aliases:
            for m in rx.finditer(t):
                s, e = m.span()
                if not any(ex.search(t[max(0, s - w): e + w]) for ex, w in excl):
                    raw_need.add(key(r))
check("audit covers every response with a B01/B06 match (after exclusions)", sorted(raw_need - cover), [])
n_rm = len(audit.get("removals", []))
print(f"  [info] section 3.3 audit: {len(cover)} responses audited; {n_rm} match(es) removed as common-noun uses")
check("verdict status", "FINAL" if not (raw_need - cover) else "PROVISIONAL", verd["status"])

print("\nRESULT:", "all independent checks agree" if not fails else f"{len(fails)} mismatches: {fails}")
sys.exit(1 if fails else 0)
