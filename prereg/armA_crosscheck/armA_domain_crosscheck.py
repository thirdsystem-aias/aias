#!/usr/bin/env python3
"""Arm A (SEO) pre-lock task §3.4 item 3: blind model cross-check of the domain list.

Decided by Pablo, Tue 2026-11-24 7:29 am CT ("go arm A cross-check"). One OpenAI model (not Anthropic, since the
resolver was Wikidata plus a Claude lane), given ONLY the brand name, its category and the country (US), blind to
our domain, is asked for the brand's official US website domain. One call per brand (72 brands), no web search,
provider defaults (no temperature / reasoning effort sent), max_output_tokens capped.

Model: gpt-6-astra (OpenAI flagship used in the programme: t4 panel; v0.46 ai_checks_v0_46.py CHECKER).
Price: $10 / $50 per 1M input / output tokens (OpenAI pricing page as read 2026-11-24 and recorded in
osf/v46/scripts/ai_checks_v0_46.py, worktree v0.46-stage1); reasoning tokens are billed as output.
Budget: expected < $1; HARD CAP $2.00: before every call, spent + worst case of that call must be <= $2.00,
otherwise the run stops (remaining brands recorded NOT_RUN).
Key: read only from the environment (OPENAI_API_KEY); never printed or written.

MATCHING RULE (fixed here before any call):
  normalise: lower case, strip scheme, path, port, trailing dot, a leading 'www.' / 'wwwN.'.
  AGREE_EXACT  model host == one of our domains for the brand (primary or US-site extra / alternate).
  AGREE_SITE   same registrable domain (last two labels) as one of ours (e.g. us.hsbc.com vs hsbc.com).
  AGREE_REDIRECT  model host differs, but a free HTTPS request to it ends (after redirects) on one of our
               registrable domains (checked afterwards, no model involved; e.g. a legacy domain forwarding).
  DISAGREE     otherwise. Per r1 §3.4 item 3: on disagreement the domain is UNRESOLVED and not pulled
               (no human tiebreak). The reasoning per disagreement is listed for the coordinator.
  NO_ANSWER    empty, UNKNOWN or unparsable reply (treated as DISAGREE for the rule).
Usage: python3 armA_domain_crosscheck.py --dry-run | --run
"""
import argparse, csv, datetime as dt, json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = "gpt-6-astra"
PRICE_IN, PRICE_OUT = 10.0, 50.0          # USD per 1M tokens
MAX_OUT = 800
IN_BOUND = 400                            # generous bound on input tokens per call (prompt is ~100)
CAP = 2.00
WORST = IN_BOUND * PRICE_IN / 1e6 + MAX_OUT * PRICE_OUT / 1e6

SYSTEM = ("You answer questions about companies' official websites. Reply with exactly one host name "
          "(for example example.com or us.example.com), with no scheme, no path and no other text. "
          "If you do not know, reply UNKNOWN.")
PROMPT = ("Brand: {name}\nCategory: {cat}\nCountry: United States\n"
          "What is the domain of this brand's official website for customers in the United States?")

CARS, AIR, BANK, SW, SP = "passenger cars", "airlines", "retail banks", "B2B software", "premium spirits"
# (row, brand_id, name given to the model, category, our domains: primary first, then US-site extra / alternate)
BRANDS = [
    (1, "BR-00370", "Mercedes-Benz", CARS, ["mercedes-benz.com", "mbusa.com"]),
    (3, "BR-00376", "BMW", CARS, ["bmw.com", "bmwusa.com"]),
    (5, "BR-00372", "Cadillac", CARS, ["cadillac.com"]),
    (6, "BR-00375", "Porsche", CARS, ["porsche.com"]),
    (7, "BR-00371", "Jaguar", CARS, ["jaguar.com", "jaguarusa.com"]),
    (9, "BR-00373", "Rolls-Royce", CARS, ["rolls-roycemotorcars.com"]),
    (10, "BR-00374", "Bentley", CARS, ["bentleymotors.com"]),
    (11, "BR-00382", "Toyota", CARS, ["toyota.com"]),
    (12, "BR-00383", "Honda", CARS, ["honda.com"]),
    (13, "BR-00384", "Ford", CARS, ["ford.com"]),
    (14, "BR-00385", "Chevrolet", CARS, ["chevrolet.com"]),
    (15, "BR-00386", "Hyundai", CARS, ["hyundaiusa.com"]),
    (16, "BR-00387", "Volkswagen", CARS, ["vw.com"]),
    (17, "BR-00388", "Nissan", CARS, ["nissanusa.com"]),
    (18, "BR-00377", "Tesla", CARS, ["tesla.com"]),
    (19, "BR-00378", "Rivian", CARS, ["rivian.com"]),
    (20, "BR-00379", "Lucid", CARS, ["lucidmotors.com"]),
    (21, "BR-00380", "Polestar", CARS, ["polestar.com"]),
    (22, "BR-00488", "American Airlines", AIR, ["aa.com"]),
    (23, "BR-00489", "Delta Air Lines", AIR, ["delta.com"]),
    (24, "BR-00490", "United Airlines", AIR, ["united.com"]),
    (25, "BR-00491", "Southwest Airlines", AIR, ["southwest.com"]),
    (26, "BR-00492", "Alaska Airlines", AIR, ["alaskaair.com"]),
    (27, "BR-00493", "JetBlue", AIR, ["jetblue.com"]),
    (28, "BR-00494", "Frontier Airlines", AIR, ["flyfrontier.com"]),
    (29, "BR-00495", "Allegiant Air", AIR, ["allegiantair.com"]),
    (30, "BR-00496", "Breeze Airways", AIR, ["flybreeze.com"]),
    (31, "BR-00497", "Hawaiian Airlines", AIR, ["hawaiianairlines.com"]),
    (32, "BR-00498", "Sun Country Airlines", AIR, ["suncountry.com"]),
    (33, "BR-00463", "Chase", BANK, ["chase.com"]),
    (34, "BR-00464", "Bank of America", BANK, ["bankofamerica.com"]),
    (35, "BR-00465", "Wells Fargo", BANK, ["wellsfargo.com"]),
    (36, "BR-00466", "Citi", BANK, ["citi.com"]),
    (37, "BR-00467", "U.S. Bank", BANK, ["usbank.com"]),
    (38, "BR-00468", "Capital One", BANK, ["capitalone.com"]),
    (39, "BR-00469", "Morgan Stanley", BANK, ["morganstanley.com"]),
    (40, "BR-00470", "Goldman Sachs / Marcus", BANK, ["goldmansachs.com", "marcus.com"]),
    (42, "BR-00471", "PNC", BANK, ["pnc.com"]),
    (43, "BR-00472", "Truist", BANK, ["truist.com"]),
    (44, "BR-00473", "TD Bank", BANK, ["td.com"]),
    (45, "BR-00474", "Charles Schwab", BANK, ["schwab.com"]),
    (46, "BR-00475", "Fifth Third", BANK, ["53.com"]),
    (47, "BR-00476", "Huntington", BANK, ["huntington.com"]),
    (48, "BR-00477", "BMO", BANK, ["bmo.com"]),
    (49, "BR-00478", "Citizens", BANK, ["citizensbank.com"]),
    (50, "BR-00479", "First Citizens", BANK, ["firstcitizens.com"]),
    (51, "BR-00480", "M&T Bank", BANK, ["mtb.com"]),
    (52, "BR-00481", "American Express", BANK, ["americanexpress.com"]),
    (53, "BR-00482", "KeyBank", BANK, ["key.com"]),
    (54, "BR-00483", "Ally", BANK, ["ally.com"]),
    (55, "BR-00484", "HSBC", BANK, ["hsbc.com", "us.hsbc.com"]),
    (56, "BR-00485", "Regions", BANK, ["regions.com"]),
    (57, "BR-00486", "UBS", BANK, ["ubs.com"]),
    (58, "BR-00487", "Pinnacle", BANK, ["pnfp.com"]),
    (59, "BR-00521", "Discover", BANK, ["discover.com"]),
    (60, "BR-00418", "Salesforce", SW, ["salesforce.com"]),
    (61, "BR-00419", "HubSpot", SW, ["hubspot.com"]),
    (62, "BR-00420", "ServiceNow", SW, ["servicenow.com"]),
    (63, "BR-00421", "Workday", SW, ["workday.com"]),
    (64, "BR-00422", "SAP", SW, ["sap.com"]),
    (65, "BR-00423", "Oracle", SW, ["oracle.com"]),
    (66, "BR-00425", "Figma", SW, ["figma.com"]),
    (67, "BR-00428", "Datadog", SW, ["datadoghq.com"]),
    (68, "BR-00429", "Snowflake", SW, ["snowflake.com"]),
    (69, "BR-00431", "Twilio", SW, ["twilio.com"]),
    (70, "BR-00432", "Cloudflare", SW, ["cloudflare.com"]),
    (71, "BR-00433", "MongoDB", SW, ["mongodb.com"]),
    (72, "BR-00396", "Jack Daniel's", SP, ["jackdaniels.com"]),
    (73, "BR-00401", "Jameson", SP, ["jamesonwhiskey.com"]),
    (74, "BR-00398", "Grey Goose", SP, ["greygoose.com"]),
    (75, "BR-00395", "Hennessy", SP, ["hennessy.com"]),
    (76, "BR-00408", "Rémy Martin", SP, ["remymartin.com"]),
]
TO_CONFIRM = {"mbusa.com", "bmwusa.com", "jaguarusa.com", "marcus.com", "td.com", "bmo.com", "hsbc.com",
              "us.hsbc.com", "firstcitizens.com"}


def norm(h):
    h = (h or "").strip().strip("`'\"").lower()
    h = re.sub(r"^[a-z]+://", "", h)
    h = re.split(r"[/?#\s]", h, maxsplit=1)[0].split(":")[0].rstrip(".")
    h = re.sub(r"^www\d*\.", "", h)
    return h


def reg(h):
    p = h.split(".")
    return ".".join(p[-2:]) if len(p) >= 2 else h


def classify(model_host, ours):
    if not model_host or model_host in ("unknown",) or "." not in model_host:
        return "NO_ANSWER"
    if model_host in ours:
        return "AGREE_EXACT"
    if reg(model_host) in {reg(d) for d in ours}:
        return "AGREE_SITE"
    return "DISAGREE"


def final_host(host):
    """Free HTTPS request (curl, no model); returns the host of the final URL after redirects, or ''."""
    try:
        out = subprocess.run(["curl", "-sL", "-o", "/dev/null", "-m", "15", "-A", "Mozilla/5.0",
                              "-w", "%{url_effective} %{http_code}", "https://" + host],
                             capture_output=True, text=True, timeout=20).stdout.strip()
        url, code = (out.rsplit(" ", 1) + [""])[:2]
        return norm(url), code
    except Exception as e:  # noqa
        return "", "ERR"


def cost(tin, tout):
    return (tin or 0) * PRICE_IN / 1e6 + (tout or 0) * PRICE_OUT / 1e6


class OpenAICaller:
    def __init__(self):
        import openai
        self.client = openai.OpenAI()     # reads OPENAI_API_KEY from the environment

    def __call__(self, name, cat):
        r = self.client.responses.create(model=MODEL, instructions=SYSTEM,
                                         input=[{"role": "user", "content": PROMPT.format(name=name, cat=cat)}],
                                         max_output_tokens=MAX_OUT)
        u = r.usage
        det = getattr(u, "output_tokens_details", None)
        return {"text": r.output_text or "", "served_model": r.model, "status": r.status, "response_id": r.id,
                "tokens_in": u.input_tokens, "tokens_out": u.output_tokens,
                "tokens_reasoning": getattr(det, "reasoning_tokens", None) if det is not None else None,
                "raw": r.model_dump()}


class FakeCaller:
    def __call__(self, name, cat):
        return {"text": "example.com", "served_model": "fake", "status": "completed", "response_id": "fake",
                "tokens_in": 90, "tokens_out": 120, "tokens_reasoning": 100, "raw": {}}


def run(caller, raw_path, limit=None):
    done, spent = set(), 0.0
    if os.path.exists(raw_path):
        for ln in open(raw_path, encoding="utf-8"):
            d = json.loads(ln); done.add(d["brand_id"]); spent += d["cost_usd"]
    print(f"model {MODEL}; worst case per call ${WORST:.4f}; cap ${CAP:.2f}; already done {len(done)}, "
          f"spent ${spent:.4f}")
    n = 0
    with open(raw_path, "a", encoding="utf-8") as f:
        for row, bid, name, cat, ours in BRANDS:
            if bid in done:
                continue
            if limit is not None and n >= limit:
                break
            if spent + WORST > CAP:
                print(f"STOP before {bid}: spent ${spent:.4f} + worst ${WORST:.4f} > cap ${CAP:.2f}")
                break
            sent = dt.datetime.now(dt.timezone.utc).isoformat()
            try:
                rep = caller(name, cat)
                err = None
            except Exception as e:
                rep, err = {"text": "", "tokens_in": IN_BOUND, "tokens_out": MAX_OUT, "raw": {}}, repr(e)[:500]
            c = cost(rep.get("tokens_in"), rep.get("tokens_out"))
            spent += c; n += 1
            rec = {"row": row, "brand_id": bid, "brand": name, "category": cat, "country": "US",
                   "sent_utc": sent, "received_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                   "model_requested": MODEL, "system": SYSTEM, "prompt": PROMPT.format(name=name, cat=cat),
                   "max_output_tokens": MAX_OUT, "error": err, "cost_usd": round(c, 6),
                   "cost_basis": f"${PRICE_IN}/1M in, ${PRICE_OUT}/1M out (error rows charged at worst case)",
                   **{k: v for k, v in rep.items()}}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush()
            print(f"  {row:2d} {name:24s} -> {rep.get('text','')!r:28s} in {rep.get('tokens_in')} out "
                  f"{rep.get('tokens_out')} ${c:.4f} cum ${spent:.4f} {err or ''}")
            sys.stdout.flush()
    print(f"spent ${spent:.4f}")
    return spent


def compare(raw_path, csv_path, summary_path, http=True):
    recs = {}
    for ln in open(raw_path, encoding="utf-8"):
        d = json.loads(ln); recs[d["brand_id"]] = d
    rows, counts, spent = [], {}, 0.0
    for row, bid, name, cat, ours in BRANDS:
        d = recs.get(bid)
        if d is None:
            cls, mh, fh, code, ts = "NOT_RUN", "", "", "", ""
        else:
            spent += d["cost_usd"]
            mh = norm(d.get("text", "").splitlines()[0] if d.get("text") else "")
            cls, fh, code, ts = classify(mh, ours), "", "", d["received_utc"]
            if cls == "DISAGREE" and http:
                fh, code = final_host(mh)
                if fh and reg(fh) in {reg(x) for x in ours}:
                    cls = "AGREE_REDIRECT"
        counts[cls] = counts.get(cls, 0) + 1
        rows.append({"row": row, "brand_id": bid, "brand": name, "category": cat, "our_primary": ours[0],
                     "our_alternates": ";".join(ours[1:]), "model_domain": mh, "result": cls,
                     "model_domain_final_host": fh, "model_domain_http": code,
                     "to_confirm_involved": ";".join(x for x in ours if x in TO_CONFIRM),
                     "rule_outcome": "UNRESOLVED (r1 §3.4.3)" if cls in ("DISAGREE", "NO_ANSWER") else
                     ("NOT_RUN" if cls == "NOT_RUN" else "RESOLVED"),
                     "received_utc": ts})
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summ = {"model_requested": MODEL,
            "served_models": sorted({d.get("served_model") or "" for d in recs.values()}),
            "n_brands": len(BRANDS), "n_called": len(recs), "counts": counts,
            "agree_total": sum(v for k, v in counts.items() if k.startswith("AGREE")),
            "cost_usd": round(spent, 4), "cap_usd": CAP,
            "tokens_in": sum(d.get("tokens_in") or 0 for d in recs.values()),
            "tokens_out": sum(d.get("tokens_out") or 0 for d in recs.values()),
            "price": {"in_per_1M": PRICE_IN, "out_per_1M": PRICE_OUT,
                      "source": "OpenAI pricing page read 2026-11-24, recorded in v0.46 ai_checks_v0_46.py"},
            "compared_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "raw_file": os.path.basename(raw_path)}
    json.dump(summ, open(summary_path, "w"), indent=2)
    print(json.dumps(summ, indent=2))
    for r in rows:
        if r["result"] not in ("AGREE_EXACT",):
            print(f"  {r['row']:2d} {r['brand']:24s} ours {r['our_primary']}{'+' + r['our_alternates'] if r['our_alternates'] else ''}"
                  f" | model {r['model_domain']} | {r['result']} {r['model_domain_final_host']} {r['model_domain_http']}")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--run", action="store_true")
    g.add_argument("--compare", action="store_true")
    ap.add_argument("--raw", default=None)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    if a.dry_run:
        import tempfile
        tmp = tempfile.mkdtemp()
        p = os.path.join(tmp, "raw.jsonl")
        run(FakeCaller(), p, a.limit)
        compare(p, os.path.join(tmp, "c.csv"), os.path.join(tmp, "s.json"), http=False)
        return
    if a.run:
        if not os.environ.get("OPENAI_API_KEY"):
            sys.exit("OPENAI_API_KEY not set")
        raw = a.raw or os.path.join(HERE, "raw_responses_" + dt.datetime.now(dt.timezone.utc)
                                    .strftime("%Y%m%dT%H%M%SZ") + ".jsonl")
        print("raw file:", raw)
        run(OpenAICaller(), raw, a.limit)
        return
    stem = os.path.basename(a.raw).replace("raw_responses_", "").replace(".jsonl", "")
    compare(a.raw, os.path.join(HERE, f"crosscheck_{stem}.csv"), os.path.join(HERE, f"summary_{stem}.json"))


if __name__ == "__main__":
    main()
