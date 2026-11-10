#!/usr/bin/env python3
"""v1.12 Coverage Paper A: build the CEP probe files and the cost table from the
frozen CEP table below. No network, no model calls. Run from anywhere:

    python3 osf/methodology/v1_12/prereg/build_probes_v1_12.py

Writes (next to this script): probes_v1_12.md, probes_v1_12.jsonl, cost_v1_12.csv,
and prints the brand-free check (MC_BrandFree) and word counts (rule R3).
"""
import csv, hashlib, json, os, re, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

# Category nouns: taken from each substrate's first Phase B frame (rule R8).
CATS = [
    ("v0.19", "HP", "audiophile headphones", "audiophile headphone"),
    ("v0.20", "SK", "skincare", "skincare"),
    ("v0.21", "CO", "cosmetics", "cosmetics"),
    ("v0.22", "AU", "automotive", "car"),
    ("v0.23", "SP", "premium spirits", "premium spirits"),
]
W_ORDER = ["WHY", "WHEN", "WHERE", "WHILE", "WHOM", "WHAT", "FEEL"]
W_LABEL = {"WHY": "why", "WHEN": "when", "WHERE": "where", "WHILE": "while",
           "WHOM": "with whom", "WHAT": "with what", "FEEL": "how feeling"}

CEPS = {
 "HP": {
  "WHY":   ["I want to hear every detail in my high-resolution music files.",
            "I want my first serious pair of headphones without spending a fortune."],
  "WHEN":  ["I do most of my listening late at night when the house is quiet.",
            "I'm upgrading after several years with entry-level headphones."],
  "WHERE": ["I want headphones for long listening sessions in a quiet room at home.",
            "I need headphones for a small home recording studio."],
  "WHILE": ["I want headphones to wear while working at my desk all day.",
            "I want headphones for watching films at night without disturbing anyone."],
  "WHOM":  ["I'm buying a gift for a relative who loves classical music.",
            "I listen on my own for hours at a time, so comfort matters a lot to me."],
  "WHAT":  ["I'm pairing them with a dedicated headphone amplifier and DAC.",
            "I'll plug them into a turntable and a vintage stereo receiver."],
  "FEEL":  ["I'm tired of headphones that sound harsh and fatigue my ears.",
            "I want to treat myself after a long, stressful year."],
 },
 "SK": {
  "WHY":   ["My skin is sensitive and reacts easily to new products.",
            "I want to start a simple skincare routine on a tight budget."],
  "WHEN":  ["Winter has arrived and my skin gets very dry.",
            "My wedding is in three months and I want my skin to look its healthiest."],
  "WHERE": ["I spend long days outdoors and need to protect my skin from the sun.",
            "I travel often and need products that fit in a carry-on bag."],
  "WHILE": ["I want a routine I can finish in five minutes while getting ready for work.",
            "I work out every day and need skincare that keeps up with sweat and showers."],
  "WHOM":  ["I'm buying a gift for my mother, who loves a pampering routine.",
            "My teenage son is starting his first skincare routine."],
  "WHAT":  ["I want skincare that works well under my makeup.",
            "I already use a retinol and want products that pair well with it."],
  "FEEL":  ["Lately my skin looks tired and dull.",
            "I want to feel pampered and indulge myself a little."],
 },
 "CO": {
  "WHY":   ["I want long-lasting makeup that stays put through a full working day.",
            "I'm a student and need affordable makeup basics."],
  "WHEN":  ["I'm doing my own makeup for my wedding day.",
            "I'm getting ready for a night out this weekend."],
  "WHERE": ["I need makeup that holds up in hot, humid weather on a beach holiday.",
            "I want a polished, natural look for the office."],
  "WHILE": ["I need to touch up my makeup on the go during busy days.",
            "I film videos for social media and need makeup that looks good on camera."],
  "WHOM":  ["I'm buying a first makeup gift for my teenage daughter.",
            "I'm putting together a kit to do my friends' makeup for special events."],
  "WHAT":  ["I want makeup that layers well over my daily skincare and sunscreen.",
            "I want a bold eye and lip look to go with a black-tie outfit."],
  "FEEL":  ["I want to feel confident before a big job interview.",
            "I'm in the mood to try something bold and playful."],
 },
 "AU": {
  "WHY":   ["I need a dependable car that will be cheap to run for many years.",
            "I want a car that is fun to drive on winding roads."],
  "WHEN":  ["Our first child is due in a few months.",
            "I'm about to retire and want a comfortable car for long road trips."],
  "WHERE": ["I live in a big city and need something easy to park.",
            "Where I live, winters bring heavy snow and icy roads."],
  "WHILE": ["I commute more than an hour each way on the highway.",
            "I need to tow a small boat on weekends."],
  "WHOM":  ["I'm buying a first car for my newly licensed teenager.",
            "We are a family of five with a large dog."],
  "WHAT":  ["I have solar panels at home and can charge a car in my garage.",
            "I need room for camping gear and two bikes."],
  "FEEL":  ["After a recent accident, feeling safe matters more to me than anything else.",
            "I want a car that feels calm and quiet after stressful workdays."],
 },
 "SP": {
  "WHY":   ["I want a bottle to sip slowly and enjoy neat.",
            "I want something good for mixing cocktails at home without overspending."],
  "WHEN":  ["I'm celebrating a big promotion this weekend.",
            "It's the holiday season and I'm stocking up for the month."],
  "WHERE": ["I'm bringing a bottle to a backyard barbecue.",
            "I'm setting up a small home bar from scratch."],
  "WHILE": ["I want something to enjoy while watching the big game.",
            "I want something to sip while listening to records in the evening."],
  "WHOM":  ["I'm buying a gift for my father-in-law, who appreciates fine spirits.",
            "I'm hosting friends who like to try something new."],
  "WHAT":  ["I want a spirit to serve with dessert after dinner.",
            "I want something to go with a cheese and charcuterie board."],
  "FEEL":  ["I want something comforting on a cold winter night.",
            "I'm in the mood to treat myself to something special."],
 },
}

def question(code, noun):
    # Fixed question sentence (rule R3); automotive adds "buying new" (rule R8).
    if code == "AU":
        return "Which car brands would you suggest buying new? Name several brands."
    return f"Which {noun} brands would you suggest? Name several brands."

def probes():
    out = []
    for sub, code, cat, noun in CATS:
        for w in W_ORDER:
            for half, sit in zip(("A", "B"), CEPS[code][w]):
                pid = f"{code}-{w}-{half}"
                out.append(dict(probe_id=pid, substrate=sub, category=cat, w=W_LABEL[w],
                                half=half, role="CEP", situation=sit,
                                prompt=f"{sit} {question(code, noun)}"))
        out.append(dict(probe_id=f"{code}-C0", substrate=sub, category=cat, w=None,
                        half=None, role="CONTROL", situation=None,
                        prompt=question(code, noun)))
    return out

# --- brand-free check (MC_BrandFree): canonical names of the 112 registry units ---
V23 = ["Johnnie Walker", "Hennessy", "Jack Daniel's", "Patrón", "Grey Goose", "Bacardi",
       "Bombay Sapphire", "Jameson", "Lagavulin", "Clase Azul", "Hendrick's",
       "Woodford Reserve", "Monkey 47", "The Balvenie", "Rémy Martin", "Casamigos",
       "Fortaleza", "Compass Box", "Nikka", "Del Maguey", "Fernet-Branca", "Redbreast",
       "St. George Spirits", "Mezcal Vago"]
EXTRA = ["Samsung", "Galaxy", "AKG", "JBL", "Harman", "Apple", "AirPods", "Bose", "Beats"]

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()

def registry_names():
    names = set(V23 + EXTRA)
    with open(os.path.join(ROOT, "osf/aias_2_0/aias_2_0_profiles.csv")) as f:
        for r in csv.DictReader(f):
            if r["substrate"] != "v0.23":
                names.add(r["brand"])
    return sorted(names)

def brand_free(ps):
    hits = []
    names = registry_names()
    for p in ps:
        t = norm(p["prompt"])
        for n in names:
            if re.search(r"\b" + re.escape(norm(n)) + r"\b", t):
                hits.append((p["probe_id"], n))
    return hits

# --- cost table (US$ per 1M tokens in/out, as verified from vendor docs on 2026-11-10) ---
PRICES = [  # model id, label, in, out, note
    ("claude-fable-5-2", "Claude Fable 5.2", 8, 40, ""),
    ("claude-opus-5-5", "Claude Opus 5.5", 4, 20, ""),
    ("gpt-6-astra", "GPT-6 Astra", 10, 50, ""),
    ("gemini-4-argon", "Gemini 4 Argon (to Nov 30)", 2, 10, "price until 2026-11-30"),
    ("gemini-4-argon", "Gemini 4 Argon (from Nov 30)", 4, 20, "price from 2026-11-30; fallback window only"),
]
SCEN = [("central", 80, 1000), ("high", 80, 2500), ("worst_cap", 80, 16384)]

def cost_rows(n_calls_per_model):
    rows = []
    for mid, lab, pin, pout, note in PRICES:
        row = dict(model_id=mid, model=lab, calls=n_calls_per_model, usd_per_M_in=pin,
                   usd_per_M_out=pout, note=note)
        for s, tin, tout in SCEN:
            per = tin * pin / 1e6 + tout * pout / 1e6
            row[f"tokens_in_{s}"] = tin
            row[f"tokens_out_{s}"] = tout
            row[f"usd_{s}"] = round(per * n_calls_per_model, 2)
        rows.append(row)
    return rows

def main():
    ps = probes()
    n_cep = sum(p["role"] == "CEP" for p in ps)
    n_ctl = sum(p["role"] == "CONTROL" for p in ps)
    assert n_cep == 70 and n_ctl == 5, (n_cep, n_ctl)
    hits = brand_free(ps)
    words = {p["probe_id"]: len(p["situation"].split()) for p in ps if p["situation"]}
    print("MC_BrandFree hits:", hits if hits else "none")
    print("situation words: max", max(words.values()), "min", min(words.values()))
    with open(os.path.join(HERE, "probes_v1_12.jsonl"), "w") as f:
        for p in ps:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    sha = hashlib.sha256(open(os.path.join(HERE, "probes_v1_12.jsonl"), "rb").read()).hexdigest()
    md = ["# v1.12 Coverage Paper A: exact probe wording", "",
          "DRAFT r0 (2026-11-10), not locked. Generated by `build_probes_v1_12.py` from its CEP table; "
          "`probes_v1_12.jsonl` holds the same 75 probes, one per line. Each probe is sent as the only user message, "
          "with no system prompt, no tools (S0) and no conversation state. The situations and the procedure that produced them: "
          "`cep_sets_v1_12.md`.", "",
          "Template (rule R3): `<situation> Which <noun> brands would you suggest? Name several brands.`  ",
          "Automotive (rule R8): `<situation> Which car brands would you suggest buying new? Name several brands.`  ",
          "Control probe C0 (one per category; manipulation check MC_Situation only, never part of Coverage): the question sentence alone.", "",
          f"Counts: {n_cep} CEP probes (14 per category: 2 per W x 7 W) + {n_ctl} control probes = {len(ps)} probes; "
          f"4 models x 3 runs x {len(ps)} = {12*len(ps)} calls. Brand-free check (MC_BrandFree, registry canonical names "
          f"+ Samsung/Harman and other listed names): "
          f"{'0 hits' if not hits else hits}. Situation length {min(words.values())} to {max(words.values())} words "
          "(rule R3: at most 20).", ""]
    for sub, code, cat, noun in CATS:
        md += [f"## {sub} {cat}", "", "| Probe ID | W | Half | Exact prompt |", "|---|---|---|---|"]
        for p in ps:
            if p["substrate"] == sub:
                md.append(f"| {p['probe_id']} | {p['w'] or 'control'} | {p['half'] or '-'} | {p['prompt']} |")
        md.append("")
    md += [f"SHA-256 of `probes_v1_12.jsonl` at this draft: `{sha}` (recomputed into the lock manifest at lock).", ""]
    with open(os.path.join(HERE, "probes_v1_12.md"), "w") as f:
        f.write("\n".join(md))
    rows = cost_rows(12 * len(ps) // 4)
    with open(os.path.join(HERE, "cost_v1_12.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader(); wr.writerows(rows)
    for s, _, _ in SCEN:
        nov = sum(r[f"usd_{s}"] for r in rows if "from Nov 30" not in r["model"])
        dec = sum(r[f"usd_{s}"] for r in rows if "to Nov 30" not in r["model"])
        print(f"cost {s}: Nov prices ${nov:.2f}; with Argon at Dec prices ${dec:.2f}")
    print("probes sha256", sha)

if __name__ == "__main__":
    main()
