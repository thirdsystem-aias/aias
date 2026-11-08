"""Collision test bed for the v0.39 registry and battery (no v0.39 study data; v0.38 answers used only as a test bed).
Usage: python3 scripts/check_registry_v0_39.py osf/v39/registries/brands_commercial_roasters_v0.39.json osf/v39/prereg/probes_v0_39.json osf/v38/data/v38_raw.json
"""
import collections
import json
import re
import sys
from pathlib import Path

REG = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
BAT = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
RAW = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))


def rx(a):
    return re.compile(a["pattern"], re.I if a["flags"] == "i" else 0)


comp = {b["id"]: ([rx(a) for a in b["aliases"]],
                  [(re.compile(x["pattern"], re.I), x["window"]) for x in b["exclusions"]]) for b in REG["brands"]}
name = {b["id"]: b["brand"] for b in REG["brands"]}


def matches(bid, text):
    al, ex = comp[bid]
    out = []
    for r in al:
        for m in r.finditer(text):
            if any(e.search(text[max(0, m.start() - w): m.end() + w]) for e, w in ex):
                continue
            out.append(m)
    return out


# 1. probes must not name any registry brand, except K probes naming Bellwether only
print("== probe leakage ==")
bad = 0
for p in BAT["probes"]:
    hit = [bid for bid in comp if matches(bid, p["prompt"])]
    ok = (hit == ["B01"]) if p["tier"] == "K" else (hit == [])
    if not ok:
        bad += 1
        print("  LEAK", p["probe_id"], hit)
print("  probes clean" if not bad else f"  {bad} leaking probes")

# 2. collision test bed: registry over v0.38's 132 answers
print("== v0.38 answers: responses matching each brand ==")
cnt = collections.Counter()
ctx = collections.defaultdict(list)
for r in RAW:
    t = r.get("response") or ""
    for bid in comp:
        ms = matches(bid, t)
        if ms:
            cnt[bid] += 1
            m = ms[0]
            ctx[bid].append(f"{r['probe_id']}|{r['model_slot']}: …{t[max(0, m.start() - 50): m.end() + 50]}…".replace("\n", " "))
for bid in sorted(comp):
    if cnt[bid]:
        print(f"  {bid} {name[bid]:24s} {cnt[bid]}")
for bid in ["B03", "B06", "B13", "B15", "B17", "B18", "B19", "B20", "B21", "B23", "B25", "B28", "B31", "B32", "B33"]:
    for c in ctx[bid][:3]:
        print(f"   [{name[bid]}] {c}")

# 3. frame lexicons over v0.38 prosumer (P) answers = the pilot numbers quoted in §1
L = REG["frame_lexicons"]
vent = [re.compile(p, re.I) for p in L["venting"]]
vless = [re.compile(p, re.I) for p in L["ventless"]]
P = [r for r in RAW if r["tier"] == "P" and r["status"] == "ok"]
allok = [r for r in RAW if r["status"] == "ok"]
vs = sum(any(v.search(r["response"]) for v in vent) for r in P)
vl_p = sum(any(v.search(r["response"]) for v in vless) for r in P)
vl_all = sum(any(v.search(r["response"]) for v in vless) for r in allok)
bw_all = sum(bool(matches("B01", r["response"])) for r in allok)
print(f"== pilot (v0.38) == P answers: {len(P)} | venting lexicon: {vs}/{len(P)} | ventless lexicon: {vl_p}/{len(P)} | ventless in all ok: {vl_all}/{len(allok)} | Bellwether: {bw_all}/{len(allok)}")
hood = collections.Counter()
for r in P:
    for v in vent:
        for m in v.finditer(r["response"]):
            hood[m.group(0).lower()] += 1
print("  venting terms matched in P:", dict(hood.most_common()))

# 4. generation coding on synthetic sentences
G = REG["bellwether_generation_coding"]
anc = [rx(a) for a in G["anchors"]]
pre = [rx(a) for a in G["preshop_tokens"]]
shop = [rx(a) for a in G["shop_tokens"]]
others = [r for bid, (al, _) in comp.items() if bid != "B01" for r in al]


def gen_code(t):
    a = [m.end() for r in anc for m in r.finditer(t)]
    if not a:
        return "Absent"

    def attributed(m):
        for e in a:
            if 0 <= m.start() - e <= G["attribution_window_chars"]:
                between = t[e:m.start()]
                if not any(o.search(between) for o in others):
                    return True
        return False

    p = any(attributed(m) for r in pre for m in r.finditer(t))
    s = any(attributed(m) for r in shop for m in r.finditer(t))
    return {(True, True): "Both", (True, False): "PreShop-only", (False, True): "Shop-only"}.get((p, s), "Unspecified")


tests = {
    "Bellwether's newest model is the Shop Roaster, a 1.5 kg countertop machine.": "Shop-only",
    "Bellwether sells the Series 2, a 6 lb ventless roaster.": "PreShop-only",
    "Consider a Bellwether roaster; it is a popular shop roaster for cafés.": "Unspecified",
    "Bellwether Series 2 or the newer Shop Roaster": "Both",
    "Bellwether is ventless. The Probat Series 2 is gas.": "Unspecified",
    "Diedrich and Mill City are common choices.": "Absent",
}
for s, want in tests.items():
    got = gen_code(s)
    print(f"  gen {'OK ' if got == want else 'BAD'} {got:13s} <- {s}")
