#!/usr/bin/env python3
"""Acquisition for AIAS v0.43 (PRE_REGISTRATION_v0_43.md s3.2, s4). Sub-commands:

  terms                  google_trends_autocomplete per distinct search name; applies the s3.2 rule
  size                   sizing pull (28 requests), range 2025-09-07 2026-06-06; fixes the bundles
  pull --n 1|2|3         main pull, range 2025-05-04 2026-11-07
  snapshot               monthly snapshot, range 2025-05-04 -> last Saturday before today
  stage2-pull --n 1|2|3  Stage 2 outcome pull, range 2025-05-04 2027-03-06 (not before 2027-03-10)

Every network sub-command refuses to run unless (1) git tag v0.43-prereg-r1 is on origin,
(2) osf/v43/anchor/osf_anchor_v0_43.json exists, (3) the UTC date is outside 2026-11-17..2026-11-21
(v0.40 collection window). Main/stage-2 pull n also requires pull n-1 stored >= 24 h earlier.
`--mock DIR` replaces the network with canned JSON (see mock_request); with it, `--tag-check
present|absent` and `--now ISO` may be used to test the guards.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trends_common_v0_43 as tc  # noqa: E402

TAG = "v0.43-prereg-r1"
API = "https://serpapi.com/search.json"
V040_WINDOW = (dt.date(2026, 11, 17), dt.date(2026, 11, 21))
STAGE2_NOT_BEFORE = dt.date(2027, 3, 10)
SUBSTRATES = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
MAX_ATTEMPTS = 3  # first send + 2 re-sends


class Refused(Exception):
    pass


class Failed(Exception):
    pass


def default_root():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))


def P(root, rel):
    return os.path.join(root, "osf/v43", rel)


# ------------------------------------------------------------------ units / terms / bundles
def load_units(root):
    with open(P(root, "registries/units_v0_43.csv"), newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    by = {s: [] for s in SUBSTRATES}
    for r in rows:
        by[r["substrate"]].append((r["unit"], r["search_name"]))
    return rows, by


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ------------------------------------------------------------------ mock backend
def mock_ts_name(q, date):
    return "ts_" + hashlib.sha1(f"{q}|{date}".encode()).hexdigest()[:12] + ".json"


def mock_ac_name(q):
    return "ac_" + hashlib.sha1(q.encode()).hexdigest()[:12] + ".json"


_MOCK_ATTEMPTS = {}


def sim_volume(sim, term, week):
    """Deterministic simulated volume of `term` in week-start date `week` (see tests)."""
    t = sim["terms"].get(term)
    if t is None:
        return 0.0
    wk = (week - dt.date(2025, 5, 4)).days // 7
    base, trend, amp = t["base"], t.get("trend", 0.0), t.get("season", 0.0)
    v = base * (1 + trend * wk) * (1 + amp * math.sin(2 * math.pi * wk / 52.0))
    h = hashlib.sha1(f"{sim.get('seed', 0)}|{term}|{week}".encode()).digest()
    u = int.from_bytes(h[:4], "big") / 2 ** 32 - 0.5
    v *= 1 + sim.get("noise", 0.0) * 2 * u
    return max(v, 0.0)


def sim_response(sim, q, date):
    a, b = date.split()
    a, b = dt.date.fromisoformat(a), dt.date.fromisoformat(b)
    terms = q.split(",")
    weeks = []
    d = a
    while d <= b:
        weeks.append(d)
        d += dt.timedelta(days=7)
    raw = {t: [sim_volume(sim, t, w) for w in weeks] for t in terms}
    mx = max(max(v) for v in raw.values()) or 1.0
    pts = []
    for i, w in enumerate(weeks):
        ts = int(dt.datetime(w.year, w.month, w.day, tzinfo=dt.timezone.utc).timestamp())
        pt = {"date": w.isoformat(), "timestamp": str(ts),
              "values": [{"query": t, "value": str(round(100 * raw[t][i] / mx)),
                          "extracted_value": round(100 * raw[t][i] / mx)} for t in terms]}
        if sim.get("partial_last") and i == len(weeks) - 1 and (w + dt.timedelta(days=6)) > b:
            pt["partial_data"] = True
        pts.append(pt)
    return {"search_metadata": {"status": "Success"}, "interest_over_time": {"timeline_data": pts}}


def mock_request(params, mockdir):
    """Returns (http_status, json|None). Looks for a canned file first (`ts_<hash>.json` /
    `ac_<hash>.json`; a file {"_attempts": [r1, r2, ...]} gives the i-th response to the i-th
    call, a response {"_http": 500} simulates an HTTP error), else generates from `_sim.json`."""
    if params["engine"] == "google_trends_autocomplete":
        fn = os.path.join(mockdir, mock_ac_name(params["q"]))
        if not os.path.exists(fn):
            return 404, None
        return 200, read_json(fn)
    key = (mockdir, params["q"], params["date"])
    fn = os.path.join(mockdir, mock_ts_name(params["q"], params["date"]))
    if os.path.exists(fn):
        obj = read_json(fn)
        if isinstance(obj, dict) and "_attempts" in obj:
            i = _MOCK_ATTEMPTS.get(key, 0)
            _MOCK_ATTEMPTS[key] = i + 1
            obj = obj["_attempts"][min(i, len(obj["_attempts"]) - 1)]
        if isinstance(obj, dict) and "_http" in obj:
            return obj["_http"], None
        return 200, obj
    sim_fn = os.path.join(mockdir, "_sim.json")
    if os.path.exists(sim_fn):
        return 200, sim_response(read_json(sim_fn), params["q"], params["date"])
    return 404, None


# ------------------------------------------------------------------ guards and clock
def now_utc(args):
    if args.now:
        if not args.mock:
            raise Refused("--now is only allowed together with --mock")
        t = dt.datetime.fromisoformat(args.now.replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
    return dt.datetime.now(dt.timezone.utc)


def tag_on_origin(args):
    if args.tag_check != "git":
        if not args.mock:
            raise Refused("--tag-check present|absent is only allowed together with --mock")
        return args.tag_check == "present"
    try:
        out = subprocess.run(["git", "ls-remote", "--tags", "origin", TAG], cwd=args.root,
                             capture_output=True, text=True, timeout=60)
    except Exception as e:  # pragma: no cover
        raise Refused(f"cannot query origin for tag {TAG}: {e}")
    if out.returncode != 0:
        raise Refused(f"git ls-remote failed: {out.stderr.strip()}")
    return f"refs/tags/{TAG}" in out.stdout


def check_guards(args, now):
    d = now.date()
    if V040_WINDOW[0] <= d <= V040_WINDOW[1]:
        raise Refused(f"UTC date {d} is inside v0.40's collection window "
                      f"{V040_WINDOW[0]}..{V040_WINDOW[1]}")
    if not tag_on_origin(args):
        raise Refused(f"git tag {TAG} is not on origin")
    if not os.path.exists(P(args.root, "anchor/osf_anchor_v0_43.json")):
        raise Refused("osf/v43/anchor/osf_anchor_v0_43.json does not exist")
    if not args.mock and not os.environ.get("SERPAPI_KEY"):
        raise Refused("SERPAPI_KEY is not set")


# ------------------------------------------------------------------ request layer
def send(params, args):
    """One network (or mock) call. Returns (http_status|None, json|None, error|None)."""
    if args.mock:
        st, js = mock_request(params, args.mock)
        return st, js, (None if st == 200 else f"HTTP {st}")
    import requests
    p = dict(params)
    p["api_key"] = os.environ["SERPAPI_KEY"]
    try:
        r = requests.get(API, params=p, timeout=90)
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}"
    try:
        js = r.json()
    except Exception:
        js = None
    err = None if r.status_code == 200 else f"HTTP {r.status_code}"
    if r.status_code == 200 and isinstance(js, dict) and js.get("error"):
        err = f"API error: {js['error']}"
    return r.status_code, js, err


def pause(args):
    if not args.mock and args.sleep:
        time.sleep(args.sleep)


# ------------------------------------------------------------------ terms
def cmd_terms(args, now):
    rows, by = load_units(args.root)
    path = P(args.root, "registries/terms_v0_43.json")
    store = read_json(path) if os.path.exists(path) else {"by_name": {}, "chosen": {}}
    names = sorted({n for s in SUBSTRATES for _, n in by[s]})
    for n in names:
        if n in store["by_name"]:
            continue
        err = None
        for att in range(MAX_ATTEMPTS):
            st, js, err = send({"engine": "google_trends_autocomplete", "q": n}, args)
            pause(args)
            if err is None and isinstance(js, dict):
                break
        if err is not None or not isinstance(js, dict):
            tc.dump_json(store, path)
            raise Failed(f"autocomplete failed for {n!r}: {err}")
        store["by_name"][n] = {"suggestions": js.get("suggestions", []), "fetched_utc": now_utc(args).isoformat()}
    store["chosen"] = {}
    for s in SUBSTRATES:
        for unit, n in by[s]:
            term, kind, sg = tc.choose_term(n, store["by_name"][n]["suggestions"], s)
            store["chosen"][f"{s}|{unit}"] = {"term": term, "kind": kind, "search_name": n,
                                              "suggestion": sg}
    topic = sum(1 for v in store["chosen"].values() if v["kind"] == "topic")
    store["summary"] = {"n_units": len(store["chosen"]), "n_topic": topic,
                        "share_topic": topic / len(store["chosen"]), "n_distinct_names": len(names)}
    tc.dump_json(store, path)
    print(f"terms: {len(names)} names, {topic}/{len(store['chosen'])} units by topic -> {path}")


# ------------------------------------------------------------------ pull machinery
def step_dir(root, step):
    return P(root, f"data/trends_raw/{step}")


def bundle_file(root, step, sub, j):
    return os.path.join(step_dir(root, step), f"{sub}_b{j}.json")


def windows_for(kind, stage=None, end=None):
    if kind == "sizing":
        return [tc.SIZING_E]
    if kind == "snapshot":
        return [end]
    st = tc.STAGES[stage]
    w = [st["base"], st["end"], tc.shift_weeks(st["base"], -52), tc.shift_weeks(st["end"], -52)]
    if st["prior"]:
        w.append(st["prior"])
    return w


def fetch_bundle(args, step, sub, j, units, terms, rng, windows):
    """Send one request with up to two re-sends; store raw record; return Series or None."""
    fn = bundle_file(args.root, step, sub, j)
    if os.path.exists(fn):
        rec = read_json(fn)
        if rec["units"] != units:
            raise Failed(f"stored {fn} has different units than expected")
        return series_of(rec), rec
    params = {"engine": "google_trends", "data_type": "TIMESERIES", "geo": "US", "tz": "0",
              "date": f"{rng[0].isoformat()} {rng[1].isoformat()}", "q": ",".join(terms)}
    attempts, final = [], None
    for att in range(MAX_ATTEMPTS):
        st, js, err = send(params, args)
        pause(args)
        a = {"utc": now_utc(args).isoformat(), "http_status": st, "error": err, "response": js}
        ser = None
        if err is None and isinstance(js, dict):
            try:
                ser = tc.parse_timeseries(js)
            except ValueError as e:
                a["error"] = f"no timeline: {e}"
        if ser is not None:
            ok, reasons = tc.mc_weekly(ser, rng[0], rng[1], windows, n_terms=len(terms))
            a["mc_weekly_ok"], a["mc_weekly_reasons"] = ok, reasons
            if ok:
                final = ser
        attempts.append(a)
        if final is not None:
            break
    rec = {"step": step, "substrate": sub, "bundle": j, "units": units, "terms": terms,
           "params": params, "status": "ok" if final is not None else "missing",
           "fetched_utc": attempts[-1]["utc"], "n_attempts": len(attempts), "attempts": attempts}
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    tc.dump_json(rec, fn)
    return final, rec


def series_of(rec):
    if rec["status"] != "ok":
        return None
    return tc.parse_timeseries(rec["attempts"][-1]["response"])


def cmd_size(args, now):
    bpath = P(args.root, "registries/bundles_v0_43.json")
    if os.path.exists(bpath):
        raise Refused("bundles_v0_43.json already exists: the sizing pull is done (one pull only)")
    tpath = P(args.root, "registries/terms_v0_43.json")
    if not os.path.exists(tpath):
        raise Refused("terms_v0_43.json missing: run `terms` first")
    terms = read_json(tpath)["chosen"]
    _, by = load_units(args.root)
    out = {"created_utc": now.isoformat(), "substrates": {}}
    for s in SUBSTRATES:
        sname = dict(by[s])
        ordered = sorted(sname, key=lambda u: (sname[u].casefold(), sname[u]))
        bundles, sers = [], []
        placed = 0
        prev_largest = None
        j = 0
        while placed < len(ordered):
            if j == 0:
                units = tc.first_sizing_bundle(ordered)
                placed = len(units)
            else:
                units = tc.next_sizing_bundle(ordered, placed, prev_largest)
                placed += len(units) - 1
            ts = [terms[f"{s}|{u}"]["term"] for u in units]
            ser, rec = fetch_bundle(args, "sizing", s, j, units, ts, tc.SIZING_RANGE,
                                    windows_for("sizing"))
            if ser is None:
                raise Failed(f"sizing request {s} b{j} is missing after {MAX_ATTEMPTS} attempts; "
                             "the next bundle cannot be formed (see ambiguity notes); stopping")
            prev_largest = tc.largest_in_bundle(units, ser)
            bundles.append(units)
            sers.append(ser)
            j += 1
        info, links = tc.chain_factors(bundles, sers)
        lv = tc.unit_levels(bundles, sers, info, tc.SIZING_E)
        main = tc.main_bundles(list(lv), lambda u: tc.size_sort_key(lv[u], sname[u]))
        out["substrates"][s] = {
            "sizing_bundles": bundles, "sizing_links": links,
            "sizes": {u: list(v) for u, v in lv.items()}, "main_bundles": main,
            "terms": {u: terms[f"{s}|{u}"]["term"] for u in sname}}
        print(f"size {s}: {len(bundles)} sizing bundles, {len(main)} main bundles, links held {sum(links)}/{len(links)}")
    tc.dump_json(out, bpath)


def prev_step_check(args, now, prev_step, bundles):
    for s in SUBSTRATES:
        for j in range(len(bundles[s]["main_bundles"])):
            if not os.path.exists(bundle_file(args.root, prev_step, s, j)):
                raise Refused(f"previous pull {prev_step} is not complete ({s} b{j} not stored)")
    latest = None
    for s in SUBSTRATES:
        for j in range(len(bundles[s]["main_bundles"])):
            t = dt.datetime.fromisoformat(read_json(bundle_file(args.root, prev_step, s, j))["fetched_utc"])
            latest = t if latest is None or t > latest else latest
    if now - latest < dt.timedelta(hours=24):
        raise Refused(f"previous pull {prev_step} was stored {(now - latest)} ago (< 24 h)")


def run_pull(args, now, step, rng, windows, prev_step=None):
    bpath = P(args.root, "registries/bundles_v0_43.json")
    if not os.path.exists(bpath):
        raise Refused("bundles_v0_43.json missing: run `size` first")
    bundles = read_json(bpath)["substrates"]
    if prev_step:
        prev_step_check(args, now, prev_step, bundles)
    nreq = nmiss = 0
    for s in SUBSTRATES:
        for j, units in enumerate(bundles[s]["main_bundles"]):
            ts = [bundles[s]["terms"][u] for u in units]
            ser, rec = fetch_bundle(args, step, s, j, units, ts, rng, windows)
            nreq += 1
            nmiss += ser is None
    print(f"{step}: {nreq} requests, {nmiss} missing")


def cmd_pull(args, now):
    n = args.n
    end = tc.STAGES[1]["end"]
    if now.date() <= end:
        raise Refused(f"range end {end} is not yet complete at {now.date()}")
    run_pull(args, now, f"main{n}", tc.STAGES[1]["range"], windows_for("main", 1),
             f"main{n - 1}" if n > 1 else None)


def cmd_snapshot(args, now):
    end = tc.last_saturday_before(now.date())
    run_pull(args, now, f"snapshot_{now.date().isoformat()}", (dt.date(2025, 5, 4), end),
             windows_for("snapshot", end=end))


def cmd_stage2(args, now):
    if now.date() < STAGE2_NOT_BEFORE:
        raise Refused(f"Stage 2 pulls are not allowed before {STAGE2_NOT_BEFORE} (UTC date {now.date()})")
    n = args.n
    run_pull(args, now, f"stage2_{n}", tc.STAGES[2]["range"], windows_for("main", 2),
             f"stage2_{n - 1}" if n > 1 else None)


# ------------------------------------------------------------------ cli
def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=default_root())
    common.add_argument("--mock", default=None, help="directory of canned JSON; replaces the network")
    common.add_argument("--tag-check", choices=["git", "present", "absent"], default="git",
                        help="mock only: override the origin tag check")
    common.add_argument("--now", default=None, help="mock only: override the UTC clock (ISO)")
    common.add_argument("--sleep", type=float, default=1.0)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("terms", parents=[common])
    sub.add_parser("size", parents=[common])
    sub.add_parser("snapshot", parents=[common])
    for name in ("pull", "stage2-pull"):
        p = sub.add_parser(name, parents=[common])
        p.add_argument("--n", type=int, choices=[1, 2, 3], required=True)
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        now = now_utc(args)
        check_guards(args, now)
        {"terms": cmd_terms, "size": cmd_size, "pull": cmd_pull, "snapshot": cmd_snapshot,
         "stage2-pull": cmd_stage2}[args.cmd](args, now)
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2
    except Failed as e:
        print(f"FAILED: {e}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
