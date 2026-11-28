#!/usr/bin/env python3
"""
panel_check_v0_46.py -- AIAS v0.46 (#76): the automated panel check of Stage 1 manuscript r10, Section 3.3
(DEVIATIONS Entry 3; added after the lock, ex ante: no #76 data exist).

Rule (Section 3.3, locked): one model per provider (Anthropic, OpenAI, Google): the provider's newest generally
available flagship model, served through the public API, as the provider's own pages state it on the day the rule is
applied. Flagship = the model the provider's documentation presents as its most capable generally available model
("Latest models", listed first; "Our most capable model"; the top of the "flagship" pricing group). Generally
available = stated as such, or listed without qualification on the models and pricing pages; restricted (verified
organisations only), preview, experimental and pre-release models are excluded; "available on the paid tier" alone
does not count.

What it does (no model is called; network only, plain HTTPS GET): for each provider it fetches the models overview,
the candidate's model page, the changelog and the pricing page; records for each page the URL asked, the URL served,
UTC date and time, HTTP status, SHA-256 of the bytes and the wording relied on; applies the text tests below; and
writes osf/v46/data/v46_panel_verification.json in the form acquire_v0_46.panel_guard reads
({"models": {slot: {"model_id", "available", ...}}}). No step is manual: the candidate is read from the pages.

Text tests (per provider; every one must pass for "available": true):
  T1 flagship   the candidate is the one the models overview presents first / as most capable (provider-specific
                extractor below; the extracted wording is recorded)
  T2 model page the candidate's own model page answers 200 and names the model ID
  T3 GA         stated GA in the changelog, or listed without qualification on the models and pricing pages
  T4 priced     the pricing page lists the model ID or name with a per-token price
  T5 no qualifier  no "preview / experimental / pre-release / verified organisations only / limited access" wording
                is attached to the candidate (nearest model name in the same sentence) on the overview, model or
                pricing page; the model ID itself contains no preview/exp marker. Listings of the model on
                third-party clouds (THIRD_PARTY) are recorded, not tested: the rule concerns the provider's public API
Modes: --run (fetch, test, write the record; exit 0 if every slot is available, 3 otherwise), --offline DIR (test pages
saved earlier as DIR/<key>.html; for tests), default output path overridable with --out.
"""
import argparse
import hashlib
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
V46 = HERE.parent
OUT_DEFAULT = V46 / "data" / "v46_panel_verification.json"
UA = "Mozilla/5.0 (compatible; aias-v046-panel-check)"
SLOTS = {"M1_anthropic": "anthropic", "M2_openai": "openai", "M3_google": "google"}

PAGES = {
    "anthropic": {"overview": "https://platform.claude.com/docs/en/about-claude/models/overview",
                  "changelog": "https://platform.claude.com/docs/en/release-notes/overview",
                  "pricing": "https://platform.claude.com/docs/en/about-claude/pricing",
                  "model": "https://platform.claude.com/docs/en/models/{slug}/overview"},
    "openai": {"overview": "https://developers.openai.com/api/docs/models",
               "changelog": "https://developers.openai.com/api/docs/changelog",
               "pricing": "https://developers.openai.com/api/docs/pricing",
               "model": "https://developers.openai.com/api/docs/models/{id}"},
    "google": {"overview": "https://ai.google.dev/gemini-api/docs/models",
               "changelog": "https://ai.google.dev/gemini-api/docs/changelog",
               "pricing": "https://ai.google.dev/gemini-api/docs/pricing",
               "model": "https://ai.google.dev/gemini-api/docs/models/{id}",
               "deprecations": "https://ai.google.dev/gemini-api/docs/deprecations"},
}
NAME_RX = {"anthropic": r"Claude [A-Z][a-z]+ \d+(?:\.\d+)?",
           "openai": r"GPT-\d+(?:\.\d+)? [A-Z][a-z]+",
           "google": r"Gemini \d+(?:\.\d+)? [A-Z][a-z]+"}
QUALIFIER = re.compile(r"\b(research preview|preview|experimental|pre-release|prerelease|only to organi[sz]ations verified|"
                       r"verified organi[sz]ations only|limited access|waitlist|alpha|beta)\b", re.I)
FEATURE_PREVIEW = re.compile(r"Supported \(Preview\)|\(beta\)\*?|public beta|Flex \(beta\)", re.I)
# Availability through third-party clouds (e.g. OpenAI's "Cloud providers" table) is not the provider's public API
# (Section 3.3: "served through the provider's public API"); such listings are recorded but not tested by T5.
THIRD_PARTY = re.compile(r"Cloud providers Model IDs across cloud providers\..*?(?=Rate limits|$)", re.S)


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def text_of(raw):
    """Visible text of a page: scripts/styles and tags removed, entities decoded, whitespace collapsed."""
    s = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def fetch(url, opener=None):
    """-> page dict (bytes kept under '_raw', not written). Plain GET; no cookies, no key."""
    rec = {"url": url, "utc": now_utc()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with (opener or urllib.request.urlopen)(req, timeout=40) as r:
            b = r.read()
            rec.update(status=r.status, served_url=r.geturl())
    except Exception as e:  # recorded, never hidden
        rec.update(status=getattr(e, "code", None), error=f"{type(e).__name__}: {e}"[:300], served_url=None)
        b = b""
    rec.update(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), _raw=b)
    return rec


def snippet(t, m, before=120, after=200):
    return t[max(0, m.start() - before): m.end() + after].strip()


def name_of(provider, model_id):
    """Display name from the model ID (claude-fable-5-2 -> Claude Fable 5.2; gpt-6.2-astra -> GPT-6.2 Astra;
    gemini-4-carbon -> Gemini 4 Carbon)."""
    if provider == "anthropic":
        m = re.fullmatch(r"claude-([a-z]+)-(\d+)(?:-(\d+))?", model_id)
        return m and f"Claude {m[1].title()} {m[2]}" + (f".{m[3]}" if m[3] else "")
    if provider == "openai":
        m = re.fullmatch(r"gpt-(\d+(?:\.\d+)?)-([a-z]+)", model_id)
        return m and f"GPT-{m[1]} {m[2].title()}"
    m = re.fullmatch(r"gemini-(\d+(?:\.\d+)?)-([a-z]+)", model_id)
    return m and f"Gemini {m[1]} {m[2].title()}"


# ----------------------------------------------------------------- T1: the flagship, read from the overview
def flagship_anthropic(ov):
    m = re.search(r"Latest models.{0,4000}?Claude API ID\s+(claude-[a-z]+-\d+(?:-\d+)?)", ov, re.S)
    if not m:
        return None, []
    first = re.search(r"Latest models.{0,400}", ov)
    return m[1], [first[0][:400] if first else "", snippet(ov, re.search(r"Claude API ID\s+" + re.escape(m[1]), ov), 0, 120)]


def flagship_openai(ov):
    m = re.search(r"Flagship models.{0,600}?Model ID\s+(gpt-[\w.-]+)", ov, re.S)
    if not m:
        return None, []
    words = [snippet(ov, m, 0, 0)[:700]]
    lead = re.search(r"use (GPT-[\d.]+ [A-Z][a-z]+) ?, our flagship model[^.]*\.", ov)
    if lead:
        words.insert(0, lead[0])
    return m[1], words


def flagship_google(ov):
    m = re.search(r'description="(Our (?:strongest|most capable)[^"]*)" title="(Gemini [^"]+)"', ov)
    if not m:
        return None, []
    code = re.search(r"Model code\* \*\*([\w.-]+)\*\*", ov[m.end():])
    return (code[1] if code else None), [f'{m[2]}: "{m[1]}"', code[0] if code else ""]


FLAGSHIP = {"anthropic": flagship_anthropic, "openai": flagship_openai, "google": flagship_google}


# ----------------------------------------------------------------- T3 / T4 / T5
def ga_statement(provider, changelog, model_page, model_id, name):
    """Stated GA (Google changelog 'generally available (GA)' entry; model page 'Stable: <id>'), with the dated
    changelog heading the entry sits under. -> (stated: bool, wording list)."""
    words, stated = [], False
    m = re.search(r"\*\*" + re.escape(name) + r" \(`" + re.escape(model_id) + r"`\) generally available \(GA\)\*\*", changelog)
    if m:
        heads = list(re.finditer(r"## ([A-Z][a-z]+ \d{1,2}, \d{4})", changelog[:m.start()]))
        words.append((f"changelog heading {heads[-1][1]}: " if heads else "") + snippet(changelog, m, 0, 160))
        stated = True
    s = re.search(r"Stable: `" + re.escape(model_id) + r"`", model_page)
    if s:
        words.append(s[0])
    return stated, words


def changelog_mentions(changelog, model_id, name):
    m = re.search(re.escape(model_id) + "|" + re.escape(name), changelog)
    return [snippet(changelog, m, 60, 240)] if m else []


def price_wording(provider, pricing, model_id, name):
    """T4: the price text on the pricing page (standard first; batch where the page lists it)."""
    if provider == "anthropic":
        rx = re.escape(name) + r"[^$]{0,120}\$(\d+(?:\.\d+)?) / MTok \$(\d+(?:\.\d+)?) / MTok"
        hits = [snippet(pricing, m, 0, 0) for m in re.finditer(rx, pricing)]
        bm = re.search(r"Batch processing.{0,400}?" + rx, pricing, re.S)
        return {"standard": hits[0] if hits else None, "batch": (bm[0][-200:] if bm else None)}
    if provider == "openai":
        rx = re.escape(model_id) + r" \$(\d+\.\d+) \$(\d+\.\d+)"
        hits = list(re.finditer(rx, pricing))
        return {"standard": hits[0][0] if hits else None, "batch": hits[1][0] if len(hits) > 1 else None,
                "group": "Flagship models" if hits and "Flagship models" in pricing[:hits[0].start()] else None}
    h = re.search(r"## " + re.escape(name) + r" \{% id=\"" + re.escape(model_id) + r"\"", pricing)
    if not h:
        return {"standard": None}
    seg = pricing[h.end(): h.end() + 4000]
    inp = re.search(r"Input price \* Not available \* ([^*]+?) ---", seg)
    out = re.search(r"Output price \(including thinking tokens\) \* Not available \* ([^*]+?) ---", seg)
    lead = re.search(r"Our most capable[^.]*\.", seg)
    note = re.search(re.escape(name) + r" is not available on the Free tier\.[^{]*", seg)
    return {"standard": f"input: {inp[1].strip()} | output (including thinking tokens): {out[1].strip()}" if inp and out else None,
            "lead": lead[0] if lead else None, "note": note[0].strip() if note else None}


def qualifiers(text, provider, model_id, name):
    """T5: qualifier words whose nearest model name (same sentence, within 200 characters) is the candidate."""
    found = []
    names = re.compile(NAME_RX[provider] + "|" + {"anthropic": r"claude-[a-z]+-\d+(?:-\d+)?", "openai": r"gpt-[\w.-]+",
                                                  "google": r"gemini-[\w.-]+"}[provider])
    for sent in re.split(r"(?<=[.!?])\s+|\s\*\s|\s---\s|\{%|%\}", text):
        if FEATURE_PREVIEW.search(sent):
            sent = FEATURE_PREVIEW.sub(" ", sent)
        for q in QUALIFIER.finditer(sent):
            near = None
            for n in names.finditer(sent):
                d = min(abs(n.start() - q.end()), abs(q.start() - n.end()))
                if d <= 200 and (near is None or d < near[0]):
                    near = (d, n[0])
            if near and near[1] in (model_id, name):
                found.append(sent.strip()[:300])
    return found


def check_provider(provider, get):
    """Apply the rule for one provider. `get(key, url)` returns a page dict (see fetch). -> slot entry."""
    urls = PAGES[provider]
    pages = {k: get(k, u) for k, u in urls.items() if k != "model"}
    txt = {k: text_of(p["_raw"]) for k, p in pages.items()}
    model_id, t1_words = FLAGSHIP[provider](txt["overview"])
    entry = {"provider": provider, "model_id": model_id, "available": False, "tests": {}, "wording": {}}
    if not model_id:
        entry["tests"]["T1_flagship"] = False
        entry["why_not"] = "no flagship found on the models overview by the extractor"
    else:
        name = name_of(provider, model_id)
        slug = model_id.replace("claude-", "", 1)
        pages["model"] = get("model", urls["model"].format(id=model_id, slug=slug))
        txt["model"] = text_of(pages["model"]["_raw"])
        stated, ga_words = ga_statement(provider, txt["changelog"], txt["model"], model_id, name)
        price = price_wording(provider, txt["pricing"], model_id, name)
        third = {k: THIRD_PARTY.findall(txt[k]) for k in ("overview", "model", "pricing")}
        quals = {k: qualifiers(THIRD_PARTY.sub(" ", txt[k]), provider, model_id, name)
                 for k in ("overview", "model", "pricing")}
        t = {"T1_flagship": True,
             "T2_model_page": pages["model"].get("status") == 200 and model_id in txt["model"],
             "T4_priced": bool(price.get("standard")),
             "T5_no_qualifier": not any(quals.values()) and not re.search(r"preview|exp|alpha|beta", model_id)}
        t["T3_generally_available"] = stated or (t["T1_flagship"] and t["T4_priced"] and t["T5_no_qualifier"])
        t["all_pages_200"] = all(p.get("status") == 200 for p in pages.values())
        entry.update(name=name, tests=t, available=all(t.values()),
                     ga_basis="stated GA in the provider's changelog" if stated else
                     "listed without qualification on the models and pricing pages",
                     wording={"T1_flagship": t1_words, "T3_ga": ga_words, "T4_price": price,
                              "T5_qualifiers_found": quals,
                              "T5_third_party_listings_not_tested": {k: v for k, v in third.items() if v},
                              "changelog": changelog_mentions(txt["changelog"], model_id, name)})
        if provider == "google" and "deprecations" in txt:
            d = re.search(r"`" + re.escape(model_id) + r"` \* ([^*]+?) \* ([^*]+?) \*", txt["deprecations"])
            entry["wording"]["deprecations_row"] = d[0] if d else None
        if not entry["available"]:
            entry["why_not"] = "failed: " + ", ".join(k for k, v in t.items() if not v)
    entry["pages"] = [{k2: v for k2, v in dict(p, key=k).items() if k2 != "_raw"} for k, p in pages.items()]
    return entry


def run(get=None, out=OUT_DEFAULT, write=True, log=print):
    get = get or (lambda key, url: fetch(url))
    started = now_utc()
    models = {slot: check_provider(prov, get) for slot, prov in SLOTS.items()}
    rec = {"study": "v0.46 (#76)", "record": "panel verification, Stage 1 manuscript r10 Section 3.3 (DEVIATIONS Entry 3)",
           "script": "osf/v46/scripts/panel_check_v0_46.py", "started_utc": started, "finished_utc": now_utc(),
           "rule": "newest generally available flagship per provider, as the provider's own pages state it on the day",
           "manual_steps": "none", "panel": {s: e["model_id"] for s, e in models.items()},
           "all_available": all(e["available"] for e in models.values()), "models": models}
    if write:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(json.dumps(rec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for s, e in models.items():
        log(f"{s}: {e['model_id']} available={e['available']} tests={e['tests']} {e.get('why_not', '')}")
    return rec


def offline_getter(directory):
    """Pages saved as DIR/<provider>_<key>.html (tests); the provider is taken from the URL host."""
    d = Path(directory)

    def get(key, url):
        prov = "anthropic" if "claude.com" in url else ("openai" if "openai.com" in url else "google")
        p = d / f"{prov}_{key}.html"
        b = p.read_bytes() if p.exists() else b""
        return {"url": url, "utc": now_utc(), "status": 200 if p.exists() else 404, "served_url": url,
                "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "_raw": b}
    return get


def main(argv=None):
    ap = argparse.ArgumentParser(description="v0.46 Section 3.3 panel check (network only; no model call)")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--offline", metavar="DIR")
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    a = ap.parse_args(argv)
    if not (a.run or a.offline):
        ap.error("choose --run or --offline DIR")
    rec = run(get=offline_getter(a.offline) if a.offline else None, out=a.out)
    print(f"panel: {rec['panel']}; all available: {rec['all_available']}; written {a.out}")
    return 0 if rec["all_available"] else 3


if __name__ == "__main__":
    sys.exit(main())
