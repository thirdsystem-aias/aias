#!/usr/bin/env python3
"""Arm A: one DataForSEO Historical Rank Overview pull (pre-registration r4, sections 4.1, 5.2-5.4, 6.1).

  python3 osf/arm_a/scripts/pull_arm_a.py --pull 1 --plan        # cost plan only; no request, no key needed
  python3 osf/arm_a/scripts/pull_arm_a.py --pull 1 --collect     # the pull (refuses before the lock anchor exists)

Rules implemented (each is unit-tested with a fake transport; tests/test_pull_arm_a.py):
  * The pull starts only if the lock anchor exists, no other paid collection is running (one-off exception: pull 1
    on 2026-12-01, params_arm_a.CONCURRENT_OK), the published price read
    before the pull equals $0.12 per request + $0.0012 per month, and the whole pull's expected cost fits under the
    per-pull limit ($13.00) and, with everything already spent, under the $48.00 hard stop. Otherwise nothing is sent.
  * Before every request (retries included): cumulative spend + this request's expected cost <= $48.00, and this
    pull's spend + expected cost <= $13.00; otherwise the pull stops.
  * After the first request of the pull: stop if its cost differs from 0.12 + 0.0012 x months returned by more than
    $0.005, or its months returned differ from the plan. After every request: stop if it cost more than $0.20.
  * A failed request (status_message other than "Ok." or no items) is retried once after 60 s; its cost counts. A
    domain failing twice is PULL_FAILED for this pull.
  * Every response is saved exactly as returned, one file per request, never overwritten; a manifest row per request
    (pull, brand ID, domain, request body, HTTP status, status_message, cost, months returned, UTC time, price read,
    SHA-256 of the file). The API key comes from the environment and is never written anywhere.
Exit codes: 0 pull complete; 2 refused before any request; 3 stopped by a limit or check (case goes to Pablo).
"""
import argparse
import base64
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import params_arm_a as P   # noqa: E402

PAID_PATTERNS = ("acquire_v0_", "acquire_v1_", "run_acquisition_v", "ai_checks_v0_")   # other paid collections
MANIFEST_COLS = ["pull", "seq", "attempt", "brand_id", "domain", "request_body", "http_status", "status_message",
                 "cost", "months_returned", "months_planned", "sent_utc", "received_utc", "price_per_request",
                 "price_per_month", "file", "sha256", "outcome"]


class Stop(Exception):
    """A limit or check stopped the pull; the reason goes to Pablo."""


class Refuse(Exception):
    """The pull did not start; nothing was sent."""


def months_inclusive(date_from, pull_day):
    y0, m0 = int(date_from[:4]), int(date_from[5:7])
    return (pull_day.year - y0) * 12 + (pull_day.month - m0) + 1


def request_cost(months):
    return round(P.PRICE_PER_REQUEST + P.PRICE_PER_MONTH * months, 6)


def plan(pull, pull_day, n=P.N_DOMAINS):
    spec = P.PULLS[pull]
    months = months_inclusive(spec["date_from"], pull_day)
    per = request_cost(months)
    return {"pull": pull, "pull_day": pull_day.isoformat(), "date_from": spec["date_from"], "mode": spec["mode"],
            "months": months, "per_request": per, "n_domains": n, "expected": round(n * per, 6)}


def load_domains(path=None):
    path = path or (P.REG / "arm_a_domains_r1.csv")
    with open(path, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["status"] == "RESOLVED"]
    return sorted(rows, key=lambda r: int(r["pull_order"]))


# --- checks before the pull -------------------------------------------------------------------------------------
def parse_price(html):
    """'$0.12 + $0.0012' as DataForSEO's Historical Rank pricing page shows it (read 2026-11-24)."""
    text = re.sub(r"<[^>]+>", " ", html)
    m = re.search(r"\$\s*(0\.\d+)\s*\+\s*\$\s*(0\.\d+)", text)
    return (float(m.group(1)), float(m.group(2))) if m else None


def read_price(fetch=None):
    if fetch is None:
        req = urllib.request.Request(P.PRICE_PAGE, headers={"User-Agent": "AIAS-research-pull/1.0"})
        with urllib.request.urlopen(req, timeout=40) as r:
            html = r.read().decode("utf-8", "replace")
    else:
        html = fetch(P.PRICE_PAGE)
    return parse_price(html)


def other_paid_collections(ps_lines=None):
    if ps_lines is None:
        import subprocess
        ps_lines = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout.splitlines()
    me = str(os.getpid())
    out = []
    for ln in ps_lines:
        parts = ln.strip().split(None, 1)
        if len(parts) == 2 and parts[0] != me and any(p in parts[1] for p in PAID_PATTERNS):
            out.append(ln.strip())
    return out


def manifest_path(pull):
    return P.RAW / f"pull{pull}" / f"manifest_pull{pull}.csv"


def read_manifest(pull):
    p = manifest_path(pull)
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def spent(pull=None):
    """Sum of the `cost` field of every recorded response (all pulls, or one pull)."""
    pulls = [pull] if pull is not None else list(P.PULLS)
    return round(sum(float(r["cost"] or 0) for p in pulls for r in read_manifest(p)), 6)


def preflight(pull, pull_day, price, ps_lines=None, n=P.N_DOMAINS):
    """Raise Refuse unless every start condition holds; return the plan."""
    if not P.ANCHOR.exists():
        raise Refuse(f"lock anchor missing: {P.ANCHOR} (the pull runs only after the lock is pushed and deposited)")
    spec = P.PULLS[pull]
    if not (spec["planned"] <= pull_day.isoformat() <= spec["latest"]):
        raise Refuse(f"pull {pull} date {pull_day} outside its window {spec['planned']}..{spec['latest']}")
    if read_manifest(pull):
        raise Refuse(f"pull {pull} already has a manifest; a pull runs whole or not at all")
    if price is None:
        raise Refuse("published price could not be read; the case goes to Pablo")
    if abs(price[0] - P.PRICE_PER_REQUEST) > 1e-9 or abs(price[1] - P.PRICE_PER_MONTH) > 1e-9:
        raise Refuse(f"published price {price} differs from $0.12 + $0.0012 per month; the case goes to Pablo")
    others = other_paid_collections(ps_lines)
    allowed = P.CONCURRENT_OK.get(pull) == pull_day.isoformat()   # section 5.4: pull 1 on 2026-12-01 only
    if others and not allowed:
        raise Refuse("another paid collection is running: " + "; ".join(others)[:300])
    pl = plan(pull, pull_day, n)
    if others:
        pl["concurrent_paid_collections"] = others   # recorded; allowed only by the one-off exception
    if pl["expected"] > P.PER_PULL_LIMIT:
        raise Refuse(f"expected ${pl['expected']:.4f} above the per-pull limit ${P.PER_PULL_LIMIT:.2f}")
    if spent() + pl["expected"] > P.HARD_STOP:
        raise Refuse(f"spent ${spent():.4f} + expected ${pl['expected']:.4f} above the hard stop ${P.HARD_STOP:.2f}")
    return pl


# --- transport ----------------------------------------------------------------------------------------------------
def live_post(body):
    """POST one task; returns (http_status, raw bytes as received). Credentials only from the environment."""
    login, pw = os.environ["DATAFORSEO_LOGIN"], os.environ["DATAFORSEO_PASSWORD"]
    auth = base64.b64encode(f"{login}:{pw}".encode()).decode()
    req = urllib.request.Request(P.API_HOST + P.ENDPOINT, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": "Basic " + auth, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def utcnow():
    return datetime.now(timezone.utc)


def parse_response(raw):
    """(status_message, cost or None, months returned) from one raw response."""
    try:
        resp = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return "UNPARSEABLE", None, 0
    cost = resp.get("cost")
    tasks = resp.get("tasks") or [{}]
    t = tasks[0] or {}
    msg = t.get("status_message") or resp.get("status_message") or "NO_STATUS"
    res = (t.get("result") or [None])[0] or {}
    return msg, (float(cost) if cost is not None else None), len(res.get("items") or [])


def write_manifest(pull, rows):
    p = manifest_path(pull)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLS)
        w.writeheader()
        w.writerows(rows)


def save_raw(folder, domain, when, raw):
    stem = f"hro_{domain}_{when.strftime('%Y%m%dT%H%M%S%fZ')}"
    path, k = folder / f"{stem}.json", 1
    while path.exists():                      # never overwrite
        path, k = folder / f"{stem}_{k}.json", k + 1
    path.write_bytes(raw)
    return path, hashlib.sha256(raw).hexdigest()


# --- the pull -------------------------------------------------------------------------------------------------------
def run_pull(pull, pull_day, post, price, sleep=time.sleep, now=utcnow, domains=None, ps_lines=None):
    """Run one pull. Returns a summary dict; raises Refuse before any request, records a stop in the summary."""
    domains = domains if domains is not None else load_domains()
    pl = preflight(pull, pull_day, price, ps_lines, n=len(domains))
    folder = P.RAW / f"pull{pull}"
    folder.mkdir(parents=True, exist_ok=True)
    before = spent()
    rows, failed, stop, seq, pull_spent, first_checked = [], [], None, 0, 0.0, False
    try:
        for d in domains:
            ok = False
            for attempt in range(1, P.MAX_RETRIES + 2):
                exp = pl["per_request"]
                if before + pull_spent + exp > P.HARD_STOP + 1e-9:
                    raise Stop(f"hard stop: ${before + pull_spent:.4f} spent + ${exp:.4f} > ${P.HARD_STOP:.2f}")
                if pull_spent + exp > P.PER_PULL_LIMIT + 1e-9:
                    raise Stop(f"per-pull limit: ${pull_spent:.4f} + ${exp:.4f} > ${P.PER_PULL_LIMIT:.2f}")
                body = [{"target": d["domain"], "location_code": P.LOCATION_CODE, "language_code": P.LANGUAGE_CODE,
                         "date_from": pl["date_from"]}]
                seq += 1
                sent = now()
                try:
                    status, raw = post(body)
                except Exception as e:                                   # network failure: no response body
                    status, raw = None, json.dumps({"transport_error": repr(e)}).encode()
                recv = now()
                path, digest = save_raw(folder, d["domain"], recv, raw)
                msg, cost, months = parse_response(raw)
                counted = cost if cost is not None else exp              # unknown cost counted at the expected cost
                pull_spent = round(pull_spent + counted, 6)
                ok = (msg == "Ok." and months > 0)
                rows.append({"pull": pull, "seq": seq, "attempt": attempt, "brand_id": d["brand_id"],
                             "domain": d["domain"], "request_body": json.dumps(body), "http_status": status,
                             "status_message": msg, "cost": counted, "months_returned": months,
                             "months_planned": pl["months"], "sent_utc": sent.isoformat(),
                             "received_utc": recv.isoformat(), "price_per_request": price[0],
                             "price_per_month": price[1], "file": path.relative_to(P.ROOT).as_posix(),
                             "sha256": digest, "outcome": "OK" if ok else "FAILED"})
                write_manifest(pull, rows)
                if counted > P.MAX_REQUEST_COST + 1e-9:
                    raise Stop(f"request {seq} ({d['domain']}) cost ${counted:.4f} > ${P.MAX_REQUEST_COST:.2f}")
                if ok and not first_checked:
                    first_checked = True
                    if abs(counted - request_cost(months)) > P.FIRST_COST_TOL + 1e-9:
                        raise Stop(f"first request cost ${counted:.4f} vs ${request_cost(months):.4f} for "
                                   f"{months} months (tolerance ${P.FIRST_COST_TOL})")
                    if months != pl["months"]:
                        raise Stop(f"first request returned {months} months, plan {pl['months']}")
                if ok:
                    if months != pl["months"]:
                        rows[-1]["outcome"] = "OK_MONTHS_DIFFER"
                        write_manifest(pull, rows)
                    break
                if attempt <= P.MAX_RETRIES:
                    sleep(P.RETRY_WAIT_S)
            if not ok:
                rows[-1]["outcome"] = "PULL_FAILED"
                write_manifest(pull, rows)
                failed.append(d["domain"])
    except Stop as e:
        stop = str(e)
    summary = {"plan": pl, "price_read": list(price), "requests": seq, "pull_spent": pull_spent,
               "cumulative_spent": round(before + pull_spent, 6), "pull_failed": failed, "stopped": stop,
               "finished_utc": now().isoformat()}
    (folder / f"summary_pull{pull}.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    return summary


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--pull", type=int, required=True, choices=sorted(P.PULLS))
    ap.add_argument("--plan", action="store_true", help="print the cost plan for the planned date; no request")
    ap.add_argument("--collect", action="store_true", help="run the pull (only after the lock anchor exists)")
    a = ap.parse_args(argv)
    if a.plan or not a.collect:
        day = date.fromisoformat(P.PULLS[a.pull]["planned"])
        print(json.dumps(plan(a.pull, day), indent=1))
        return 0
    try:
        summary = run_pull(a.pull, date.today(), live_post, read_price())
    except Refuse as e:
        print("REFUSED (nothing sent):", e)
        return 2
    print(json.dumps(summary, indent=1))
    return 3 if summary["stopped"] else 0


if __name__ == "__main__":
    sys.exit(main())
