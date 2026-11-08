#!/usr/bin/env python3
"""
AIAS v0.39 — audit reading lists (analysis aid; NOT part of the locked scoring).

Builds the analyst's reading lists for the pre-registered audits (PRE_REGISTRATION_v0_39.md §3.3, §5.7) from
the raw responses. It imports the locked Coder from scripts/score_v0_39.py, so every match offset listed here
is exactly the offset the scorer sees (pass 1, before audit removals). It writes reading lists only; the audit
judgments themselves are recorded by the analyst in osf/v39/data/v39_audit_commonnoun.json (binding, §3.3)
and osf/v39/data/v39_coder_audit.json (§5.7 b-c, descriptive).

  commonnoun.txt / commonnoun.json  (a) every Bellwether (B01) / Stronghold (B06) match, with context
  k_digest.txt                      (b) K1-K6 responses: sentences bearing on D1-D3
  f_digest.txt                      (c) F1-F6 responses: sentences with venting / ventless lexicon hits
  d_digest.txt                      D3 uniqueness windows, D4 ventless attributions, D2 power claims, D7 sources

Usage: AIAS_ROOT=<repo> python3 scripts/audit_worklist_v0_39.py [--raw PATH] [--out DIR]
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v0_39 as S  # noqa: E402  (locked scorer; imported, never modified)

SENT_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9*#\-\"(\[])|\n+")
REQUIRED = re.compile(r"\b(require[sd]?|need(?:s|ed)?|must|essential|necessary|mandatory|code[s]?|permit[s]?)\b", re.I)
GEN_WORDS = re.compile(r"\b(newest|latest|new|current(?:ly)?|lineup|line-up|launch(?:ed)?|announc\w+|unveil\w+|"
                       r"introduc\w+|discontinu\w+|support|20(?:18|2[0-7]))\b", re.I)
K3_WORDS = re.compile(r"\b(gas|hood|afterburner|smoke|catalytic|permit|code|electric|outlet|circuit)\b", re.I)
K6_WORDS = re.compile(r"\b(electric|afterburner|software|app|green|marketplace|subscription|carbon|emission)\b", re.I)
ELECTRIC = re.compile(r"\belectric\b", re.I)


def sentences(text):
    out, start = [], 0
    for m in SENT_BREAK.finditer(text):
        if m.start() > start:
            out.append((start, m.start()))
        start = m.end()
    if start < len(text):
        out.append((start, len(text)))
    return out


def clean(s, limit=280, focus=None):
    s = re.sub(r"[*#`]+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= limit:
        return s
    if focus is not None:
        i = max(0, min(len(s) - limit, focus - limit // 2))
        return ("…" if i else "") + s[i:i + limit] + ("…" if i + limit < len(s) else "")
    return s[:limit] + "…"


def pick(text, spans, preds, cap):
    """First `cap` sentences (in text order) for which any predicate matches."""
    got = []
    for s, e in spans:
        seg = text[s:e]
        if any(p(seg) for p in preds):
            got.append(clean(seg))
        if len(got) >= cap:
            break
    return got


def ctx(text, s, e, half=70):
    left = re.sub(r"\s+", " ", text[max(0, s - half):s])
    right = re.sub(r"\s+", " ", text[e:e + half])
    return f"…{left}[[{text[s:e]}]]{right}…"


# Section 3.3 triage (reading aid). The aliases are case-sensitive, so a common-noun use can only be a
# capitalised word at the start of a sentence, list item or heading, or inside a title-case phrase. A match
# followed by a brand-specific word, or sitting mid-sentence after a lower-case word or list punctuation,
# is a proper-noun use by construction; every other match is printed for individual reading.
FOLLOW = {
    "B01": re.compile(r"^(?:\*\*|\*)?\s*(?:Coffee|Shop\s+Roaster|Series|roasters?|Roasters?|['’]s?\b|app|App|"
                      r"system|machine|units?|models?|Marketplace|platform|website|team|technology|equipment|"
                      r"offering|lineup|line-up|roasting\s+system)"),
    "B06": re.compile(r"^(?:\*\*|\*)?\s*(?:S\s?\d|Technology|Tech\b|roasters?|Roasters?|['’]s?\b|machine|units?|"
                      r"models?|X\d|Pro\b|Surround|halogen|\()"),
}
PREV_LOWER = re.compile(r"(?:[a-z][a-z'’]*|[,/&(+]|\b(?:or|and|vs\.?|like|from|by|with|to|as|than))\s*(?:\*\*|\*|\")?\s*$")


def triage(text, s, e, bid):
    if FOLLOW[bid].search(text[e:e + 40]):
        return "brand-word-follows"
    before = text[max(0, s - 40):s]
    if PREV_LOWER.search(before) and not re.search(r"[.!?:]\s*(?:\*\*|\*|\")?\s*$|\n\s*(?:[-*#\d.)]+\s*)?(?:\*\*)?\s*$", before):
        return "mid-sentence"
    return "read"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=str(S.ROOT / "osf/v39/data/v39_raw.json"))
    ap.add_argument("--out", default=str(S.ROOT / "logs/v39/audit"))
    a = ap.parse_args()
    raw = json.loads(Path(a.raw).read_text(encoding="utf-8"))
    reg = json.loads(S.REGISTRY_PATH.read_text(encoding="utf-8"))
    coder = S.Coder(reg)
    names = {b["id"]: b["brand"] for b in reg["brands"]}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    ok = [r for r in raw if r.get("status") == "ok"]
    order = {p: i for i, p in enumerate(["F", "G", "C", "R", "K"])}
    ok.sort(key=lambda r: (order.get(r["tier"], 9), r["probe_id"], r.get("arm", "L"), r.get("condition", "S0"), r["model_slot"]))

    # (a) section 3.3 common-noun worklist
    cn, lines, nmatch, cls_n, to_read, others = {}, [], Counter(), Counter(), [], []
    for r in ok:
        t = r["response"]
        mt = coder.brand_matches(t)
        hits = {b: mt[b] for b in S.AUDITED if b in mt}
        if not hits:
            continue
        k = S.key_of(r)
        cn[k] = {b: [[s, e, triage(t, s, e, b), ctx(t, s, e)] for s, e in sp] for b, sp in hits.items()}
        lines.append(f"== {k}")
        for b, sp in hits.items():
            for s, e in sp:
                nmatch[b] += 1
                c = triage(t, s, e, b)
                cls_n[(b, c)] += 1
                lines.append(f"  {b} @{s:<5d} [{c}] {ctx(t, s, e, 55)}")
                (to_read if c == "read" else others).append(f"{k} {b} @{s} [{c}] {ctx(t, s, e, 90)}")
    (out / "commonnoun.json").write_text(json.dumps(cn, indent=1, ensure_ascii=False), encoding="utf-8")
    (out / "commonnoun.txt").write_text(
        f"# section 3.3 worklist: {len(cn)} responses; matches {dict(nmatch)}\n" + "\n".join(lines) + "\n", encoding="utf-8")
    import random
    rs = random.Random(39)
    spot = rs.sample(others, min(40, len(others)))
    (out / "commonnoun_read.txt").write_text(
        f"# triage counts {sorted(cls_n.items())}\n# {len(to_read)} matches to read individually\n"
        + "\n".join(to_read) + "\n\n# seeded spot-check sample (40) of matches triaged as proper-noun uses\n"
        + "\n".join(spot) + "\n", encoding="utf-8")

    # (b) K digest
    kl = []
    for r in ok:
        if r["tier"] != "K":
            continue
        t, pid = r["response"], r["probe_id"]
        mt = coder.brand_matches(t)
        gen, pre, shop = coder.generation(t, mt)
        sp = sentences(t)
        anchor = lambda seg: any(x.search(seg) for x in coder.anchors)
        gtok = lambda seg: any(x.search(seg) for x in coder.preshop + coder.shop + coder.markers)
        vent = lambda seg: any(x.search(seg) for x in coder.vent + coder.ventless)
        if pid in ("K1", "K2", "K4"):
            sel = pick(t, sp, [gtok, lambda g: anchor(g) and bool(GEN_WORDS.search(g))], 7)
        elif pid == "K3":
            sel = pick(t, sp, [vent, lambda g: bool(K3_WORDS.search(g))], 7)
        elif pid == "K5":
            sel = pick(t, sp, [lambda g: bool(S.QTY.search(g)), gtok], 6)
        else:
            sel = pick(t, sp, [lambda g: bool(S.UNIQUE.search(g)), lambda g: any(x.search(g) for x in coder.ventless),
                               lambda g: bool(K6_WORDS.search(g)) and anchor(g)], 7)
        extra = f" k3={S.k3_candidate(coder, t)}" if pid == "K3" else ""
        if pid == "K5":
            q = [round(S.to_kg(float(v), u), 2) for v, u in S.QTY.findall(t)]
            extra = f" qty_kg={q[:8]}"
        kl.append(f"== {S.key_of(r)}  gen={gen} pre={pre} shop={shop}{extra} chars={len(t)} fr={r.get('finish_reason')}")
        kl += [f"   - {x}" for x in sel] or ["   (no matching sentence)"]
    (out / "k_digest.txt").write_text("\n".join(kl) + "\n", encoding="utf-8")

    # (c) F digest
    fl = []
    for r in ok:
        if r["tier"] != "F":
            continue
        t = r["response"]
        mt = coder.brand_matches(t)
        v, vl = coder.frame(t)
        sp = sentences(t)
        less = pick(t, sp, [lambda g: any(x.search(g) for x in coder.ventless)], 3)
        req = pick(t, sp, [lambda g: any(x.search(g) for x in coder.vent) and bool(REQUIRED.search(g))], 3)
        anyv = [] if req else pick(t, sp, [lambda g: any(x.search(g) for x in coder.vent)], 2)
        el = pick(t, sp, [lambda g: bool(ELECTRIC.search(g))], 1)
        brands = [names[b] for b in coder.first_mention_order(mt)]
        fl.append(f"== {S.key_of(r)}  vent={v} ventless={vl} brands={brands}")
        for tag, xs in (("LESS", less), ("REQ", req), ("VENT", anyv), ("ELEC", el)):
            fl += [f"   {tag}: {x}" for x in xs]
    (out / "f_digest.txt").write_text("\n".join(fl) + "\n", encoding="utf-8")

    # D3 / D4 / D2-power / D7 digest
    dl = ["# D3 uniqueness windows (Bellwether anchor +/-150 with an 'only/first/unique...' word)"]
    d4 = ["# D4 ventless attributions to brands other than Bellwether (+/-150)"]
    pw = ["# D2 power claims within +/-200 of a Bellwether mention"]
    for r in ok:
        t = r["response"]
        mt = coder.brand_matches(t)
        k = S.key_of(r)
        for s, e in mt.get(S.FOCAL, []):
            w = t[max(0, s - 150): e + 150]
            if S.UNIQUE.search(w):
                dl.append(f"{k} @{s}: {clean(w, 330)}")
            w2 = t[max(0, s - 200): e + 200]
            if S.POWER.search(w2):
                pw.append(f"{k} @{s}: {clean(w2, 420)}")
        for bid, sps in mt.items():
            if bid == S.FOCAL:
                continue
            for s, e in sps:
                w = t[max(0, s - 150): e + 150]
                if coder.has_ventless(w):
                    d4.append(f"{k} {names[bid]} @{s}: {clean(w, 330)}")
    d7 = ["# D7 S1 sources whose URL or title mentions Bellwether, by response"]
    for r in ok:
        if r.get("condition") != "S1":
            continue
        srch = r.get("search") or {}
        items = (srch.get("citations") or []) + (srch.get("sources") or [])
        seen = set()
        for it in items:
            u, ti = it.get("url") or "", it.get("title") or ""
            if ("bellwether" in u.lower() or "bellwether" in ti.lower()) and (u, ti) not in seen:
                seen.add((u, ti))
                d7.append(f"{S.key_of(r)}: {S.source_domain(it)} | {ti[:90]} | {u[:140]}")
    (out / "d_digest.txt").write_text("\n".join(dl + [""] + d4 + [""] + pw + [""] + d7) + "\n", encoding="utf-8")
    print(f"ok responses {len(ok)}; section 3.3 responses {len(cn)}; matches {dict(nmatch)}; "
          f"K {sum(1 for r in ok if r['tier'] == 'K')}; F {sum(1 for r in ok if r['tier'] == 'F')} -> {out}")


if __name__ == "__main__":
    main()
