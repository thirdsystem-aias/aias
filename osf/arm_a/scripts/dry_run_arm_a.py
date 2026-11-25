#!/usr/bin/env python3
"""Arm A dry run on simulated Google data only (pre-registration section 6.3). No API call, no key, nothing billed.

  python3 osf/arm_a/scripts/dry_run_arm_a.py [--perm N] [--boot N]   -> osf/arm_a/prereg/dry_run_arm_a.json + .txt

It runs the real pull script (pull 1 on 2026-12-01, pull 2 on 2027-01-04, pull 3 on 2027-03-01) in a temporary
sandbox against a fake transport that answers in DataForSEO's exact response shape (simulate_google_arm_a.py), then the
join and the full analysis on those files. AI-side inputs are the real registries (published Presence and Shift
counts); Google values and the airline, bank and software sales values are simulated. Results mean nothing; the run
shows the pipeline end to end.
"""
import argparse
import json
import random
import sys
import tempfile
import time
import zlib
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_arm_a as A           # noqa: E402
import join_arm_a as J              # noqa: E402
import params_arm_a as P            # noqa: E402
import pull_arm_a as PL             # noqa: E402
import simulate_google_arm_a as SIM  # noqa: E402

SIM_SEED = 20261125


def sandbox_pulls(tmp, latent, pulls=(1, 2, 3)):
    P.ROOT, P.RAW, P.ANCHOR = tmp, tmp / "raw", tmp / "anchor.json"
    P.ANCHOR.write_text("{}", encoding="utf-8")
    template = SIM.load_template()
    summaries = {}
    for pull in pulls:
        day = date.fromisoformat(P.PULLS[pull]["planned"])
        clock = [datetime(day.year, day.month, day.day, 15, 0, tzinfo=timezone.utc)]

        def now():
            clock[0] += timedelta(seconds=2)
            return clock[0]

        def post(body, _pull=pull, _day=day):
            t = body[0]
            raw = SIM.response(t["target"], t["date_from"], _day.year, _day.month, latent[t["target"]], template,
                               seed=zlib.crc32(f"{t['target']}|{_pull}".encode()))
            return 200, json.dumps(raw).encode()

        summaries[pull] = PL.run_pull(pull, day, post, (0.12, 0.0012), sleep=lambda s: None, now=now,
                                      ps_lines=[])
    return summaries


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--perm", type=int, default=P.N_PERM)
    ap.add_argument("--boot", type=int, default=P.N_BOOT)
    ap.add_argument("--out", default=str(P.ARM / "prereg" / "dry_run_arm_a.json"))
    a = ap.parse_args(argv)
    t0 = time.time()
    real_reg, real_root = P.REG, P.ROOT
    domains = J.load_domains()
    presence, shift = A.load_presence(), A.load_shift()
    months = SIM.month_list("2024-11-01", 2027, 3)
    latent = SIM.latent_panel([d["domain"] for d in domains], months, SIM_SEED, breaks={(2024, 12): 1.8})
    rng = random.Random(SIM_SEED + 1)
    sales = {d["brand_id"]: rng.lognormvariate(20, 1.5) for d in domains
             if d["category"] in ("airlines", "banks", "software")}
    # Shift counts and car sales simulated too, so that no file shows a quasi-result of real AI and sales values
    shift = {b: {"group": v["group"], "m_rec": rng.randint(0, 18), "sales_usd": rng.lognormvariate(23, 1.5)}
             for b, v in shift.items()}
    saved = (P.ROOT, P.RAW, P.ANCHOR)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        try:
            summaries = sandbox_pulls(tmp, latent)
            panels = {pull: J.load_pull(pull, raw_root=tmp / "raw", root=tmp) for pull in (1, 2, 3)}
        finally:
            P.ROOT, P.RAW, P.ANCHOR = saved
        res = A.analyse(panels, presence, shift, sales, a.perm, a.boot, domains=domains)
    res["pull_summaries"] = summaries
    res["note"] = "SIMULATED Google and sales data; real AI-side registries; no API call; results mean nothing"
    res["seconds"] = round(time.time() - t0, 1)
    out = Path(a.out)
    out.write_text(json.dumps(res, indent=1, default=str) + "\n", encoding="utf-8")
    v = res["primary"]["verdicts"]
    lines = [f"Arm A dry run (simulated Google data), {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
             f"permutations {a.perm}, bootstrap {a.boot}, {res['seconds']} s",
             "pulls: " + "; ".join(f"pull {k}: {s['requests']} requests, ${s['pull_spent']:.4f}, "
                                   f"cumulative ${s['cumulative_spent']:.4f}, failed {len(s['pull_failed'])}, "
                                   f"stopped {s['stopped']}" for k, s in summaries.items()),
             "break flags: " + json.dumps(res["break_flags"]),
             "verdicts (meaningless, simulated): " + json.dumps(v)]
    out.with_suffix(".txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
