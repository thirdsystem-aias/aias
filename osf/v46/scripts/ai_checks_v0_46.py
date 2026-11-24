#!/usr/bin/env python3
"""
AIAS v0.46 (#76) Stage 1 -- the two open AI checks before the lock (stage1_manuscript_r2.md Appendix B items 3, 14).

D7 (Fisker; section 3.2): "an AI check with a dated source, not a manual one", logged as the record whose schema and
rule are build_probes_v0_46.validate_d7 / d7_outcome (code r3, commit 2d82cec). This script asks one model, with web
search on, whether Fisker sells new cars in the US as of the check date; the model must return each source with its
URL and date; every URL it cites must be one the search tool actually returned; the record is validated by
validate_d7 and written to build_probes_v0_46.D7_PATH only if valid. No valid answer after MAX_TRIES -> no record
(D7 stays pending, acquisition keeps refusing).

P1 (quotation; section 1.2, item 14): the quotation of proposition P1 in section 1.2 is checked "against the posted
working paper by an AI check against the PDF". The checker gets the PDF only and is asked to copy P1 verbatim; it is
blind to the manuscript's quotation (the comparison is done here, by code, after the call). Outcome: match / mismatch
/ not_found, written to P1_PATH with the PDF's SHA-256 and public URL.

Standing rule (CLAUDE.md, "No manual checks by Pablo", 2026-11-21): checker of another provider than the drafter
(the manuscript and its quotation were drafted by Claude, Anthropic) -> default checker OpenAI gpt-6-astra; blind to
the first output; decision rule without a human tiebreak; cost and cap inside #76's US$100; limit "no human check".

DEFAULTS NOT YET IN THE MANUSCRIPT (proposed; see the lane report): checker model, prompts, P1 mismatch rule,
per-check caps. Prices: OpenAI pricing page read 2026-11-24 (gpt-6-astra $10 / $50 per 1M in/out; web search
$10 / 1k calls + search content tokens at model rates): https://developers.openai.com/api/docs/pricing

Modes:
  --dry-run          both checks against a local fake client, keyless, temp files only; no model called
  --run d7|p1        real call (needs OPENAI_API_KEY); refused if the study is locked (then a dated DEVIATIONS entry
                     is required first) or if the projected cost exceeds --cap. P1 also needs --pdf and --pdf-url.
NO MODEL IS CALLED except under --run.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parents[2])))
sys.path.insert(0, str(HERE))
import build_probes_v0_46 as BP  # noqa: E402

V46 = ROOT / "osf" / "v46"
MANUSCRIPT = V46 / "stage1" / "stage1_manuscript_r2.md"
P1_PATH = V46 / "prereg" / "p1_quote_check_v0_46.json"
LOG_PATH = V46 / "data" / "ai_checks_raw_v0_46.jsonl"

CHECKER = "gpt-6-astra"            # DEFAULT (proposed): OpenAI flagship already priced in budget_v0_45
PRICE = {"gpt-6-astra": (10.0, 50.0)}   # USD per 1M tokens in / out (standard), read 2026-11-24
SEARCH_FEE = 0.010                 # USD per web_search call (OpenAI, read 2026-11-24)
MAX_OUT = 8000                     # output cap per call (reasoning + text)
MAX_TOOL_CALLS = 8                 # D7: web_search calls per request
D7_INPUT_BOUND = 60000             # D7: assumed upper bound on input incl. search content tokens (not measured)
CAP = {"d7": 2.00, "p1": 3.00}     # DEFAULT (proposed) per-check caps, USD, both tries included
MAX_TRIES = 2

D7_QUESTION = ("As of {date}, does the car brand Fisker (Fisker Inc., or any company now selling Fisker-branded "
               "vehicles) sell new cars to consumers in the United States?")
D7_SYSTEM = ("You check one fact for a research record. Use web search and rely only on sources you found. "
             "Reply with exactly one JSON object and nothing else.")
D7_PROMPT = (D7_QUESTION + "\n\nSearch the web for current sources that carry a date. Reply with one JSON object:\n"
             '{{"sells_new_cars_us": true or false, "finding": "two sentences stating what the sources show", '
             '"sources": [{{"url": "...", "title": "...", "source_date": "YYYY-MM-DD"}}]}}\n'
             "Give at least one source. source_date is the publication or last-update date shown by that source; "
             "leave out any source whose date you cannot read.")

P1_SYSTEM = ("You copy text exactly from a document for a citation check. Reply with exactly one JSON object and "
             "nothing else.")
P1_PROMPT = ("The attached PDF is a working paper that states numbered propositions (P0, P1, P2 and so on). Copy the "
             "full statement of proposition P1 exactly as printed: same words, spelling and punctuation, no "
             "paraphrase, no correction. Join lines broken by the page layout with single spaces and leave out the "
             "label (for example \"P1\" and any short title before the statement). Reply with one JSON object:\n"
             '{"found": true or false, "p1_verbatim": "the statement, or empty if not found", '
             '"page": the PDF page number where it appears, or null}')


class Refused(RuntimeError):
    pass


def now_utc():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def cost(model, tin, tout, n_search=0):
    pin, pout = PRICE[model]
    return round((tin or 0) * pin / 1e6 + (tout or 0) * pout / 1e6 + (n_search or 0) * SEARCH_FEE, 4)


def parse_json_reply(text):
    """The single JSON object in a reply (code fences tolerated). -> dict or None"""
    t = (text or "").strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    a, b = t.find("{"), t.rfind("}")
    if a < 0 or b <= a:
        return None
    try:
        o = json.loads(t[a:b + 1])
    except ValueError:
        return None
    return o if isinstance(o, dict) else None


def _norm_url(u):
    u = re.sub(r"[?#].*$", "", str(u or "").strip())
    return u.rstrip("/").lower().replace("http://", "https://").replace("://www.", "://")


def norm_text(s):
    """Typography-insensitive form for the P1 comparison (quotes, dashes, spaces, soft hyphens, ligatures)."""
    s = unicodedata.normalize("NFKC", str(s or ""))
    s = s.replace("­", "")
    for a, b in (("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-")):
        s = s.replace(a, b)
    s = re.sub(r"\s+", " ", s).strip()
    return s.strip('"').strip()


# ----------------------------------------------------------------------------------------- callers (real / fake)
class OpenAICaller:
    """OpenAI Responses API. respond(kind, model, system, content, search) -> dict; count_input(...) -> int."""

    def __init__(self):
        import openai
        self.client = openai.OpenAI()

    def _kw(self, model, system, content, search):
        kw = {"model": model, "instructions": system, "input": [{"role": "user", "content": content}]}
        if search:
            kw["tools"] = [{"type": "web_search", "search_context_size": "medium",
                            "user_location": {"type": "approximate", "country": "US"}}]
            kw["include"] = ["web_search_call.action.sources"]
        return kw

    def count_input(self, model, system, content, search=False):
        return int(self.client.responses.input_tokens.count(**self._kw(model, system, content, search)).input_tokens)

    def respond(self, model, system, content, search=False):
        kw = self._kw(model, system, content, search)
        kw["max_output_tokens"] = MAX_OUT
        if search:
            kw["max_tool_calls"] = MAX_TOOL_CALLS
        r = self.client.responses.create(**kw)
        urls, n_calls = [], 0
        for item in (r.output or []):
            d = item.model_dump() if hasattr(item, "model_dump") else {}
            if d.get("type") == "web_search_call":
                n_calls += 1
                a = d.get("action") or {}
                urls += [s.get("url") for s in (a.get("sources") or []) if s.get("url")]
                if a.get("url"):
                    urls.append(a["url"])
            elif d.get("type") == "message":
                for c in (d.get("content") or []):
                    urls += [x.get("url") for x in (c.get("annotations") or []) if x.get("type") == "url_citation"]
        u = r.usage
        return {"text": r.output_text or "", "served_model": r.model, "status": r.status, "response_id": r.id,
                "tokens_in": u.input_tokens, "tokens_out": u.output_tokens, "search_calls": n_calls,
                "search_urls": urls}


class FakeCaller:
    """Keyless stand-in: canned replies in order; records every request."""

    def __init__(self, replies, input_tokens=25000):
        self.replies, self.requests, self.input_tokens = list(replies), [], input_tokens

    def count_input(self, model, system, content, search=False):
        return self.input_tokens

    def respond(self, model, system, content, search=False):
        self.requests.append({"model": model, "system": system, "content": content, "search": search})
        rep = self.replies.pop(0)
        return dict({"served_model": model, "status": "completed", "response_id": "fake", "tokens_in": 30000,
                     "tokens_out": 1500, "search_calls": 3 if search else 0}, **rep)


def _log(path, rec):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ----------------------------------------------------------------------------------------------------- D7 (Fisker)
def d7_record_from_reply(reply, checked, model):
    """Build the D7 record from one reply. -> (record or None, problems). Sources the search tool did not return
    are dropped (a source must be one the checker found, not one it recalled); a source dated after the check too."""
    o = parse_json_reply(reply.get("text"))
    if o is None:
        return None, ["reply is not one JSON object"]
    found = {_norm_url(u) for u in (reply.get("search_urls") or [])}
    kept, probs = [], []
    for s in (o.get("sources") or []):
        s = s if isinstance(s, dict) else {}
        if _norm_url(s.get("url")) not in found:
            probs.append(f"source dropped, not returned by the search tool: {s.get('url')}")
            continue
        try:
            if dt.date.fromisoformat(str(s.get("source_date"))) > checked.date():
                probs.append(f"source dropped, dated after the check: {s.get('url')}")
                continue
        except ValueError:
            pass                                              # validate_d7 reports the bad date
        kept.append({"url": s.get("url"), "title": s.get("title"), "source_date": s.get("source_date")})
    sells = o.get("sells_new_cars_us")
    rec = {"unit": "Fisker", "question": D7_QUESTION.format(date=checked.date().isoformat()),
           "checked_utc": checked.isoformat(), "method": BP.D7_METHOD, "checker": reply.get("served_model") or model,
           "sources": kept, "sells_new_cars_us": sells,
           "decision": ("live" if sells else "cell_d") if isinstance(sells, bool) else None,
           "finding": o.get("finding"), "response_id": reply.get("response_id"),
           "limits": "AI check, no human check; one model (OpenAI), web search on; sources are those the search "
                     "tool returned, dated by the checker"}
    bad = BP.validate_d7(rec)
    return (None if bad else rec), probs + bad


def run_d7(caller, model=CHECKER, cap=CAP["d7"], out=None, log_path=LOG_PATH, log=print):
    """One D7 check (up to MAX_TRIES). -> (record or None, spent USD). Writes `out` only if valid."""
    out = Path(BP.D7_PATH if out is None else out)
    if out.exists():
        raise Refused(f"D7 record already exists: {out}")
    worst = cost(model, D7_INPUT_BOUND, MAX_OUT, MAX_TOOL_CALLS)
    spent = 0.0
    for t in range(1, MAX_TRIES + 1):
        if spent + worst > cap:
            log(f"  D7 try {t} not sent: spent {spent:.2f} + worst case {worst:.2f} > cap {cap:.2f}")
            break
        checked = now_utc()
        rep = caller.respond(model, D7_SYSTEM, D7_PROMPT.format(date=checked.date().isoformat()), search=True)
        c = cost(model, rep["tokens_in"], rep["tokens_out"], rep["search_calls"])
        spent += c
        rec, probs = d7_record_from_reply(rep, checked, model)
        _log(log_path, {"check": "D7", "try": t, "sent_utc": checked.isoformat(), "model": model, "cost_usd": c,
                        "reply": rep, "problems": probs, "valid": rec is not None})
        log(f"  D7 try {t}: {'valid' if rec else 'invalid'}; cost {c:.4f}; " + "; ".join(probs)[:300])
        if rec:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            return rec, round(spent, 4)
    return None, round(spent, 4)


# ------------------------------------------------------------------------------------------------ P1 (quotation)
def manuscript_p1_quote(path=MANUSCRIPT):
    """The quoted P1 statement of section 1.2 (the text inside the quotation marks on the '- **P1,' line)."""
    for ln in Path(path).read_text(encoding="utf-8").splitlines():
        if ln.startswith("- **P1,"):
            m = re.search(r"[\"“](.+)[\"”]\s*$", ln.strip())
            if m:
                return m.group(1)
    raise Refused(f"no quoted P1 line in {Path(path).name}")


def p1_outcome(extracted, quote, found=True):
    """match: equal after norm_text; contained: the manuscript's quotation is a verbatim part of the PDF statement;
    mismatch: neither; not_found: the checker found no P1."""
    if not found or not str(extracted or "").strip():
        return "not_found"
    e, q = norm_text(extracted), norm_text(quote)
    if e == q:
        return "match"
    return "contained" if q and q in e else "mismatch"


P1_DECISION = {   # DEFAULT (proposed) rule, applied by code; no human tiebreak
    "match": "quotation stands; add the paper's public URL to the reference",
    "contained": "quotation stands as a verbatim part of P1; add the public URL",
    "mismatch": "replace the quotation in section 1.2 with the checker's verbatim text; add the public URL",
    "not_found": "quotation unverified: section 1.2 paraphrases P1 without quotation marks; add the public URL"}


def pdf_content(pdf_bytes, filename, prompt=P1_PROMPT):
    import base64
    return [{"type": "input_file", "filename": filename,
             "file_data": "data:application/pdf;base64," + base64.b64encode(pdf_bytes).decode("ascii")},
            {"type": "input_text", "text": prompt}]


def run_p1(caller, pdf, pdf_url, model=CHECKER, cap=CAP["p1"], out=None, manuscript=MANUSCRIPT, log_path=LOG_PATH,
           log=print):
    """One P1 check (up to MAX_TRIES). The checker never sees the manuscript's quotation. -> (record, spent)"""
    out = Path(P1_PATH if out is None else out)
    if out.exists():
        raise Refused(f"P1 record already exists: {out}")
    if not re.match(r"https?://\S+$", str(pdf_url or "")):
        raise Refused("P1 needs --pdf-url (the paper's public URL, http/https)")
    data = Path(pdf).read_bytes()
    if not data.startswith(b"%PDF"):
        raise Refused(f"{pdf} is not a PDF")
    quote = manuscript_p1_quote(manuscript)
    content = pdf_content(data, Path(pdf).name)
    n_in = caller.count_input(model, P1_SYSTEM, content)
    worst = cost(model, n_in, MAX_OUT)
    log(f"  P1 input {n_in} tokens (counted); worst case per try {worst:.4f} USD")
    spent, rec = 0.0, None
    for t in range(1, MAX_TRIES + 1):
        if spent + worst > cap:
            log(f"  P1 try {t} not sent: spent {spent:.2f} + worst case {worst:.2f} > cap {cap:.2f}")
            break
        checked = now_utc()
        rep = caller.respond(model, P1_SYSTEM, content)
        c = cost(model, rep["tokens_in"], rep["tokens_out"])
        spent += c
        o = parse_json_reply(rep.get("text"))
        _log(log_path, {"check": "P1", "try": t, "sent_utc": checked.isoformat(), "model": model, "cost_usd": c,
                        "reply": rep, "parsed": o is not None})
        log(f"  P1 try {t}: {'parsed' if o else 'unparsable'}; cost {c:.4f}")
        if o is None:
            continue
        oc = p1_outcome(o.get("p1_verbatim"), quote, o.get("found") is True)
        rec = {"item": "P1 quotation (Appendix B item 14)", "checked_utc": checked.isoformat(),
               "method": "ai_check_against_pdf", "checker": rep.get("served_model") or model,
               "pdf_url": pdf_url, "pdf_sha256": hashlib.sha256(data).hexdigest(), "pdf_bytes": len(data),
               "checker_found": o.get("found"), "checker_page": o.get("page"), "checker_text": o.get("p1_verbatim"),
               "manuscript_quote": quote, "outcome": oc, "decision": P1_DECISION[oc],
               "response_id": rep.get("response_id"),
               "limits": "AI check, no human check; one model (OpenAI) reading the PDF, blind to the manuscript's "
                         "quotation; compared by code after typographic normalisation"}
        break
    if rec:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return rec, round(spent, 4)


# ------------------------------------------------------------------------------------------- guards, dry run, CLI
LOCK_TAG = "v0.46-stage1-ipa"
LOCK_ANCHOR = V46 / "anchor" / "osf_anchor_v0_46.json"


def locked():
    import subprocess
    tags = subprocess.run(["git", "-C", str(ROOT), "tag", "-l", LOCK_TAG], capture_output=True, text=True).stdout
    return bool(tags.strip()) or LOCK_ANCHOR.exists()


def _block_keys_and_clients():
    import types
    for k in list(os.environ):
        if "API_KEY" in k or k.endswith("_KEY") or k.endswith("_TOKEN"):
            del os.environ[k]

    def _refuse(*_a, **_k):
        raise Refused("no-call guard: an API client was requested during a dry run")
    stub = types.ModuleType("openai")
    stub.OpenAI = _refuse
    stub.__no_call_stub__ = True
    sys.modules["openai"] = stub


def dry_run(log=print):
    fails = []
    tmp = Path(tempfile.mkdtemp(prefix="v46_aichk_"))
    try:
        OpenAICaller()
        fails.append("no-call guard not in place")
    except Refused:
        pass
    # D7: try 1 cites a URL the search did not return (dropped -> no source -> invalid); try 2 valid.
    good_src = {"url": "https://news.example.org/fisker-status", "title": "t", "source_date": "2026-11-20"}
    r1 = {"text": json.dumps({"sells_new_cars_us": False, "finding": "x", "sources": [
        {"url": "https://recalled.example.org/a", "title": "t", "source_date": "2026-11-01"}]}),
        "search_urls": ["https://news.example.org/fisker-status"]}
    r2 = {"text": "```json\n" + json.dumps({"sells_new_cars_us": False, "finding": "x", "sources": [good_src]}) + "\n```",
          "search_urls": ["https://www.news.example.org/fisker-status/?utm=1"]}
    fake = FakeCaller([r1, r2])
    rec, spent = run_d7(fake, out=tmp / "d7.json", log_path=tmp / "log.jsonl", log=log)
    if not rec or len(fake.requests) != 2 or not all(q["search"] for q in fake.requests):
        fails.append("D7: expected an invalid first try, a valid second try, search on")
    elif BP.d7_outcome(tmp / "d7.json")[0] is not True:
        fails.append("D7: written record does not read back as fisker_defunct=True")
    if "Cell D" in json.dumps(fake.requests) or "Defunct" in json.dumps(fake.requests):
        fails.append("D7: prompt is not blind (mentions the study's classes)")
    log(f"  D7 fake: record {'valid' if rec else 'none'}, decision {rec and rec['decision']}, spent {spent} (fake usage)")
    # P1: blind request; the fake checker returns a statement that contains the manuscript's quotation.
    quote = manuscript_p1_quote()
    pdf = tmp / "paper.pdf"
    pdf.write_bytes(b"%PDF-1.4\n% fake\n%%EOF\n")
    fp = FakeCaller([{"text": json.dumps({"found": True, "page": 7, "p1_verbatim": "Reinforcement. " +
                                          quote.replace("'", "’")})}])
    rec, spent = run_p1(fp, pdf, "https://example.org/paper", out=tmp / "p1.json", log_path=tmp / "log.jsonl", log=log)
    if norm_text(quote)[:60] in norm_text(json.dumps(fp.requests)):
        fails.append("P1: the manuscript's quotation was sent to the checker (not blind)")
    if not rec or rec["outcome"] != "contained":
        fails.append(f"P1: outcome {rec and rec['outcome']} != contained")
    log(f"  P1 fake: outcome {rec and rec['outcome']}, spent {spent} (fake usage)")
    if p1_outcome("Other words.", quote) != "mismatch" or p1_outcome("", quote, False) != "not_found":
        fails.append("P1: outcome rule")
    log(f"  projected worst case per try (gpt-6-astra): D7 {cost(CHECKER, D7_INPUT_BOUND, MAX_OUT, MAX_TOOL_CALLS):.2f} "
        f"USD (input bound {D7_INPUT_BOUND}), P1 {cost(CHECKER, 25000, MAX_OUT):.2f} USD at 25,000 input tokens")
    return fails


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--run", choices=("d7", "p1"))
    ap.add_argument("--model", default=CHECKER, choices=sorted(PRICE))
    ap.add_argument("--cap", type=float)
    ap.add_argument("--pdf")
    ap.add_argument("--pdf-url")
    a = ap.parse_args(argv)
    try:
        if a.dry_run:
            _block_keys_and_clients()
            print("[v46] AI checks dry run (fake client; keyless; no model called)")
            fails = dry_run()
            print(f"[v46] AI checks dry run {'PASS' if not fails else 'FAIL: ' + '; '.join(fails)}")
            return 1 if fails else 0
        if not a.run:
            ap.error("--dry-run or --run d7|p1")
        if locked():
            raise Refused("study is locked: a dated DEVIATIONS entry must come before this check (CLAUDE.md rule)")
        if not os.environ.get("OPENAI_API_KEY"):
            raise Refused("OPENAI_API_KEY not set")
        cap = a.cap if a.cap is not None else CAP[a.run]
        if cap > CAP[a.run]:
            raise Refused(f"--cap {cap} above the stated cap {CAP[a.run]}")
        if a.run == "d7":
            rec, spent = run_d7(OpenAICaller(), a.model, cap)
        else:
            if not a.pdf:
                ap.error("--run p1 needs --pdf and --pdf-url")
            rec, spent = run_p1(OpenAICaller(), a.pdf, a.pdf_url, a.model, cap)
        print(f"[v46] {a.run.upper()} {'recorded' if rec else 'NOT recorded (still pending)'}; spent {spent:.4f} USD")
        return 0 if rec else 4
    except Refused as e:
        print(f"[v46] REFUSED: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
