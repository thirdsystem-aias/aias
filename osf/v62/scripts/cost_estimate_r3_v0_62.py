#!/usr/bin/env python3
"""AIAS v0.62 r3: the cost estimate re-based on t4's RECORDED usage (pre-registration r3, section 6). No model is called.

r2 (section 6.2) fixed that "at the final pre-registration the English basis is replaced by t4's recorded usage (S0, per
model and question type) times these factors". t4 is now collected (v0.42, tag v0.42-acquisition-locked -> a790bb1:
876/876 calls answered, 990 raw lines, recorded spend $67.9551 incl. the $0.50 judge reserve), so r3 does it now.

Source (read only, pinned): osf/v42/data/t4_raw.jsonl and t4_batches.jsonl at tag v0.42-acquisition-locked, read with
`git show` from the v0.42 repository and checked by SHA-256. ONLY USAGE FIELDS are kept from each raw line (USAGE_FIELDS
below); the answer text, the prompt and the search record are dropped when the line is parsed and are never printed or
stored. Of t4_batches.jsonl only event types, batch IDs and request counts are used.

Basis: the answered S0 lines per model x question type: B = the 30 category questions (3 runs: 90 lines per model);
A_yn = the 88 yes/no brand questions (v0.19-v0.22); A_open = the 24 open brand questions (v0.23). At t4 each answered S0
line was one billed request (no re-send, no transient failure at S0). Rules of v0.42 r2's estimate
(osf/v42/scripts/cost_estimate_v0_42.py), now applied to t4's own usage of the same three models:
  central per call = mean recorded tokens (input, output, thinking), costed by budget_v0_62.part_cost, x 1.02 (re-sends);
  high per call    = 90th percentile (statistics.quantiles, n=10, inclusive) of each token field, costed together, x 1.10.
v0.42 r2's proxies (Claude Fable 5.2 = Claude Opus 5.5's v0.39 tokens x 2 / x 3; Gemini output x 1.5 for thinking that
v0.39 did not record) are not used: t4 recorded Claude Fable 5.2 itself, and Gemini 4 Argon reported no thinking tokens
on any S0 call (thoughts_token_count absent; it reported them on 7 search-on calls).
Language factors (planning assumptions, NOT measured; unchanged from r2, section 6.2), on the whole per-call cost:
  central ES 1.25, KO 1.75, ZH 1.50; high ES 1.50, KO 2.50, ZH 2.25.
Prices (budget_v0_62.TOKEN_PRICES / PRICE_CHANGES; vendor pages re-read 2026-11-11 about 14:35 UTC, unchanged; PRICES_READ):
  Claude Fable 5.2 Message Batches 4 / 20 per 1M tokens in / out; GPT-6 Astra standard 10 / 50; Gemini 4 Argon standard
  2 / 10 through 2026-11-30 and 4 / 20 from 2026-12-01 (the guard prices each request at the UTC date it starts).
Price days: NOV = a block collected on 2026-11-29/30 (the window opens 2026-11-29 00:00 CT = 06:00 UTC; December starts
2026-11-30 18:00 CT); DEC = a block collected 2026-12-01/02. CENTRAL (headline) = NOV prices for every block, i.e.
collection starting on 2026-11-29 as planned (t4's 876 calls took under 7 hours); CONSERVATIVE HIGH = high basis x high
factors at DEC prices for every block (any slip inside the window).
Judge reserve (block 5 only): budget_v0_62.JUDGE_RESERVE_USD = 216 x (3,750 x $3 + 10 x $15) / 1e6 = $2.4624; $3 / $15
is the higher of t5's two successor-judge candidates (Claude Sonnet 5.5 $2 / $10, Claude Sonnet 4.6 $3 / $15).

r3 update (2026-11-12; pre-registrant's decision of 2026-11-12 00:48 CT, section 9 item 7 (b): the 88 yes/no brand
questions, block 4, collected last): same pinned source, same rules, every r3 number unchanged; ADDED: the projection
ratio of "core + block 4" for each headphones option (projection_core_plus_yn; acquire_v0_62.projection_ratio reads it)
and the guard on core + block 4 in each scenario (guard_core_plus_yn: spend at the end of each block, where the $80
pause and the $100 stop fall, and how many of Claude Fable 5.2's 264 block-4 requests the worst-case reservations of
the $100 rule allow in its first batch).

Run: python3 osf/v62/scripts/cost_estimate_r3_v0_62.py [--repo ~/aias/_worktrees/v0.42]
     -> osf/v62/prereg/cost_estimate_v0_62_r3.json and .txt
"""
import argparse
import hashlib
import json
import statistics as st
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
V62 = HERE.parent
sys.path.insert(0, str(HERE))
import budget_v0_62 as BG  # noqa: E402

TAG, TAG_COMMIT = "v0.42-acquisition-locked", "a790bb1ac552adfc6615b0bcb49430aa95e7bc16"
RAW = ("osf/v42/data/t4_raw.jsonl", "f3109091f51af7899098d83a1d7b2080a26a06824caa5f6fc0486f3d6196d4bf")
BATCHES = ("osf/v42/data/t4_batches.jsonl", "d73b8e81fc6402e81860222737b6a211a8cd394c4c3687bb577955bb6e39298c")
RECORDED_SPEND_USD, T4_JUDGE_RESERVE_USD = 67.9551, 0.50
USAGE_FIELDS = ("call_id", "model_requested", "substrate", "phase", "condition", "status", "error", "mode", "attempts",
                "empty_retry", "started_utc", "usage_parts", "cost_usd", "batch_id")
MODELS = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
MODE = {"claude-fable-5-2": "batch", "gpt-6-astra": "standard", "gemini-4-argon": "standard"}
LANGS = ["es", "ko", "zh"]
KINDS = ["B", "A_yn", "A_open"]
N_PER_LANG = {"B": 30, "A_yn": 88, "A_open": 24}       # per language and run (t4 probe file: 142 = 30 + 88 + 24)
FACTOR = {"central": {"es": 1.25, "ko": 1.75, "zh": 1.50}, "high": {"es": 1.50, "ko": 2.50, "zh": 2.25}}
RESEND = {"central": 1.02, "high": 1.10}
DAY = {"nov": "2026-11-30T12:00:00+00:00", "dec": "2026-12-01T12:00:00+00:00"}
BLOCKS = [("1", "B", "category questions, run 1"), ("2", "B", "category questions, run 2"),
          ("3", "B", "category questions, run 3"), ("4", "A_yn", "brand questions yes/no (v0.19-v0.22), run 1"),
          ("5", "A_open", "brand questions open (v0.23), run 1")]
CORE, PAUSE, CAP = ("1", "2", "3"), BG.PAUSE_AT_USD, BG.BUDGET_CAP_USD
PRICES_READ = {
    "read_utc": "2026-11-11T14:35Z (about; 08:35 US Central)",
    "anthropic": ("https://platform.claude.com/docs/about-claude/pricing",
                  "Claude Fable 5.2 $8 / $40 base, Batch $4 / $20; Claude Sonnet 5.5 $2 / $10; Claude Sonnet 4.6 $3 / $15; "
                  "'50 percent discount on both input and output tokens' (Batch API); no dated change shown"),
    "openai": ("https://developers.openai.com/api/docs/pricing",
               "gpt-6-astra Standard $10.00 input / $50.00 output (Batch tab $5 / $25, not used); no dated change for "
               "gpt-6-astra; reasoning tokens 'billed as output tokens' (https://developers.openai.com/api/docs/guides/reasoning)"),
    "google": ("https://ai.google.dev/gemini-api/docs/latest-model",
               "gemini-4-argon input $2.00 ($4.00 starting December 1, 2026); output including thinking tokens $10.00 "
               "($20.00 starting December 1, 2026); page 'Last updated 2026-10-27 UTC'; "
               "https://ai.google.dev/gemini-api/docs/pricing does not list the model"),
}


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def load_pinned(repo):
    """(commit, raw bytes, batches bytes) at the pinned tag; refuses on any tag or SHA-256 mismatch."""
    commit = git(repo, "rev-parse", TAG + "^{commit}").decode().strip()
    if commit != TAG_COMMIT:
        raise SystemExit(f"tag {TAG} -> {commit}, expected {TAG_COMMIT}")
    out = []
    for path, want in (RAW, BATCHES):
        b = git(repo, "show", f"{TAG}:{path}")
        got = hashlib.sha256(b).hexdigest()
        if got != want:
            raise SystemExit(f"{path} at {TAG}: sha256 {got}, expected {want}")
        out.append(b)
    return commit, out[0], out[1]


def usage_lines(raw_bytes):
    """The raw lines with USAGE FIELDS ONLY (answer text, prompt and search record dropped here)."""
    recs = []
    for line in raw_bytes.decode("utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            recs.append({k: r.get(k) for k in USAGE_FIELDS})
    return recs


def kind_of(rec):
    if rec["phase"] == "B":
        return "B"
    return "A_open" if rec["substrate"] in ("v23", "v0.23") else "A_yn"


def p90(v):
    v = sorted(v)
    return float(v[0]) if len(v) == 1 else float(st.quantiles(v, n=10, method="inclusive")[-1])


def basis(recs):
    """{(model, kind): token statistics} over the answered S0 lines (one usage part each at t4)."""
    groups = defaultdict(list)
    for r in recs:
        if r["condition"] != "S0" or r["status"] != "ok":
            continue
        parts = r["usage_parts"] or []
        if len(parts) != 1:
            raise SystemExit(f"{r['call_id']}: {len(parts)} usage parts (expected 1 at S0)")
        p = parts[0]
        groups[(r["model_requested"], kind_of(r))].append(
            (p.get("input_tokens") or 0, p.get("output_tokens") or 0, p.get("thinking_tokens") or 0, p.get("mode"),
             r["attempts"], bool(r["empty_retry"]), r["cost_usd"]))
    out = {}
    for key, v in groups.items():
        f = {"in": [x[0] for x in v], "out": [x[1] for x in v], "think": [x[2] for x in v]}
        out[key] = {"n": len(v), "modes": sorted({x[3] for x in v}), "resent_or_retried": sum(1 for x in v if x[4] > 1 or x[5]),
                    "recorded_usd": sum(x[6] for x in v),
                    **{f"{k}_mean": st.mean(x) for k, x in f.items()}, **{f"{k}_p90": p90(x) for k, x in f.items()},
                    **{f"{k}_max": max(x) for k, x in f.items()}}
    return out


def per_call(b, model, kind, level, month):
    """US$ per call for an English prompt: central = mean tokens x 1.02; high = p90 tokens x 1.10."""
    q = "mean" if level == "central" else "p90"
    x = b[(model, kind)]
    part = {"mode": MODE[model], "input_tokens": x[f"in_{q}"], "output_tokens": x[f"out_{q}"],
            "thinking_tokens": x[f"think_{q}"], "n_searches": 0}
    return BG.part_cost(model, part, DAY[month]) * RESEND[level]


def cells(b, kind, level, month, langs=LANGS, n=None):
    """[(language, model, calls, usd)] for one run of `kind` in each of `langs`."""
    n = N_PER_LANG[kind] if n is None else n
    return [(lg, m, n, n * per_call(b, m, kind, level, month) * FACTOR[level][lg]) for lg in langs for m in MODELS]


def block_table(b):
    """{block: {calls, central_nov, central_dec, high_nov, high_dec}} (+ judge reserve row)."""
    t = {}
    for blk, kind, label in BLOCKS:
        row = {"kind": kind, "label": label, "calls": sum(c[2] for c in cells(b, kind, "central", "nov"))}
        for level in ("central", "high"):
            for month in ("nov", "dec"):
                row[f"{level}_{month}"] = sum(c[3] for c in cells(b, kind, level, month))
        t[blk] = row
    return t


def total(t, blocks, level, month, judge=False):
    return sum(t[k][f"{level}_{month}"] for k in blocks) + (BG.JUDGE_RESERVE_USD if judge else 0.0)


OPTION_N = {"A": {"B": 30, "A_yn": 88, "A_open": 24}, "B": {"B": 30, "A_yn": 87, "A_open": 24},
            "C": {"B": 24, "A_yn": 72, "A_open": 24}}


def design(b, level, month, kinds_runs, option="A", judge=False):
    """(calls, US$) of a design: kinds_runs = [(kind, runs)], headphones option A/B/C (call counts as r2)."""
    calls, usd = 0, 0.0
    for kind, runs in kinds_runs:
        for _lg, _m, n, c in cells(b, kind, level, month, n=OPTION_N[option][kind]):
            calls, usd = calls + n * runs, usd + c * runs
    return calls, usd + (BG.JUDGE_RESERVE_USD if judge else 0.0)


FULL = [("B", 3), ("A_yn", 1), ("A_open", 1)]
DESIGNS = {"core": ([("B", 3)], False), "core_plus_yn": ([("B", 3), ("A_yn", 1)], False),
           "core_plus_open": ([("B", 3), ("A_open", 1)], True), "full": (FULL, True), "block1": ([("B", 1)], False)}


def projections(b):
    """Projection-pause ratio = central(design) / central(block 1), as r2 (judge reserve in the numerator)."""
    out = {"by_option_full_design": {}, "by_design_option_A": {}}
    for o in "ABC":
        out["by_option_full_design"][o] = {m: design(b, "central", m, FULL, o, True)[1] /
                                           design(b, "central", m, [("B", 1)], o)[1] for m in ("nov", "dec")}
    for k, (kr, j) in DESIGNS.items():
        out["by_design_option_A"][k] = {m: design(b, "central", m, kr, "A", j)[1] / design(b, "central", m, [("B", 1)])[1]
                                        for m in ("nov", "dec")}
    # r3 update: core + block 4 (the adopted design, section 9 item 7 (b)) for every headphones option
    kr = DESIGNS["core_plus_yn"][0]
    out["by_option_core_plus_yn"] = {o: {m: design(b, "central", m, kr, o)[1] / design(b, "central", m, [("B", 1)], o)[1]
                                         for m in ("nov", "dec")} for o in "ABC"}
    return out


def reconcile(recs, batches_bytes):
    s0 = [r for r in recs if r["condition"] == "S0"]
    diffs = [abs(BG.record_cost(r) - (r["cost_usd"] or 0.0)) for r in s0]
    ev = [json.loads(x) for x in batches_bytes.decode("utf-8").splitlines() if x.strip()]
    created = {e["batch_id"]: len(e.get("requests") or []) for e in ev if e.get("event") == "created"}
    fable_ok = [r for r in recs if r["model_requested"] == "claude-fable-5-2" and r["status"] == "ok"]
    s0_ok = [r for r in s0 if r["status"] == "ok"]
    return {
        "raw_lines": len(recs),
        "recorded_cost_usd_sum": round(sum(r["cost_usd"] or 0.0 for r in recs), 4),
        "recorded_plus_t4_judge_reserve": round(sum(r["cost_usd"] or 0.0 for r in recs) + T4_JUDGE_RESERVE_USD, 4),
        "matches_recorded_spend": abs(sum(r["cost_usd"] or 0.0 for r in recs) + T4_JUDGE_RESERVE_USD - RECORDED_SPEND_USD) < 5e-5,
        "s0_recorded_usd": round(sum(r["cost_usd"] or 0.0 for r in s0), 4),
        "s0_recomputed_usd_budget_v0_62_at_t4_dates": round(sum(BG.record_cost(r) for r in s0), 4),
        "s0_max_line_difference_usd": max(diffs),
        "s0_answered_lines": len(s0_ok),
        "s0_lines_not_answered": dict(Counter(f"{r['model_requested']} {r['status']}: {(r['error'] or '')[:36]}"
                                              for r in s0 if r["status"] != "ok")),
        "s0_answered_with_resend_or_retry": sum(1 for r in s0_ok if (r["attempts"] or 1) > 1 or r["empty_retry"]),
        "status_by_model_condition": {f"{m} {c} {s}": n for (m, c, s), n in
                                      sorted(Counter((r["model_requested"], r["condition"], r["status"]) for r in recs).items())},
        "batches_created": len(created), "requests_in_created_batches": sum(created.values()),
        "fable_answered_lines": len(fable_ok),
        "fable_answered_in_a_recorded_batch": sum(1 for r in fable_ok if r["batch_id"] in created),
        "first_and_last_answered_start_utc": [min(r["started_utc"] for r in s0_ok + fable_ok),
                                              max(r["started_utc"] for r in recs if r["status"] == "ok")],
    }


def brand_option(b, t):
    """Task r3-2: which of the 112 brand questions fit under the $80 pause in the conservative-high case."""
    core_hi = total(t, CORE, "high", "dec")
    core_c = {m: total(t, CORE, "central", m) for m in ("nov", "dec")}
    subsets = [("yes_no_88", "the 88 yes/no brand questions (block 4; v0.19-v0.22), 3 languages", ("4",), False),
               ("open_24", "the 24 open brand questions (block 5; v0.23) + judge reserve", ("5",), True),
               ("all_112", "all 112 brand questions (blocks 4-5) + judge reserve", ("4", "5"), True)]
    rows = []
    for key, label, blks, judge in subsets:
        hi = total(t, blks, "high", "dec", judge)
        rows.append({"key": key, "label": label, "calls": sum(t[k]["calls"] for k in blks),
                     "high_dec": hi, "central_nov": total(t, blks, "central", "nov", judge),
                     "central_dec": total(t, blks, "central", "dec", judge),
                     "fits_under_80_conservative_high": core_hi + hi <= PAUSE,
                     "smallest_budget_conservative_high": core_hi + hi,
                     "fits_under_80_central_nov": core_c["nov"] + total(t, blks, "central", "nov", judge) <= PAUSE,
                     "fits_under_80_central_dec": core_c["dec"] + total(t, blks, "central", "dec", judge) <= PAUSE})
    per_lang = {}
    for kind in ("A_yn", "A_open"):
        for lg in LANGS:
            c = cells(b, kind, "high", "dec", langs=[lg])
            per_lang[f"{kind}_{lg}"] = {"calls": sum(x[2] for x in c), "high_dec": sum(x[3] for x in c)}
    return {"core_high_dec": core_hi, "room_under_80": PAUSE - core_hi, "room_under_100": CAP - core_hi,
            "any_fits": any(r["fits_under_80_conservative_high"] for r in rows), "subsets": rows,
            "per_language_high_dec": per_lang}


def guard_path(t, level="high", month="dec"):
    """The guard on the core in a scenario: block-1 spend, projection (x 3.0), where $80 and $100 fall."""
    blk = t["1"][f"{level}_{month}"]
    pause_at, stop_at = PAUSE / blk, CAP / blk
    return {"block1_usd": blk, "projection_after_block1_usd": 3.0 * blk, "projection_pause": 3.0 * blk > PAUSE,
            "runs_at_80": pause_at, "runs_at_100": stop_at}


def guard_path_yn(t, ratio, level, month):
    """r3 update (section 9 item 7 (b)): the guard on core + block 4, block 4 last (no judge reserve: block 5 is not
    collected). Spend at the end of each block; projection after block 1 (block-1 spend x the central ratio of core +
    block 4); the block in which the $80 pause and the $100 stop fall (before in-flight reservations); and, at the end of
    block 3, how many of Claude Fable 5.2's block-4 requests one batch may carry under the $100 rule's worst-case
    reservations (without and with the two synchronous workers each holding its reservation of two worst cases)."""
    ends, cum = {}, 0.0
    for k in ("1", "2", "3", "4"):
        cum += t[k][f"{level}_{month}"]
        ends[k] = cum
    blk1, day = t["1"][f"{level}_{month}"], DAY[month]
    per = BG.worst_case("claude-fable-5-2", "S0", "batch", day)
    sync = BG.sync_reservation("gpt-6-astra", "S0", day) + BG.sync_reservation("gemini-4-argon", "S0", day)
    n4 = t["4"]["calls"] // len(MODELS)
    room = CAP - ends["3"]
    return {"block_end_spend_usd": ends, "block1_usd": blk1, "projection_ratio": ratio,
            "projection_after_block1_usd": ratio * blk1, "projection_pause": ratio * blk1 > PAUSE,
            "pause_80_falls_in_block": next((k for k in ends if ends[k] >= PAUSE), None),
            "stop_100_falls_in_block": next((k for k in ends if ends[k] > CAP), None),
            "runs_at_80": PAUSE / blk1, "runs_at_100": CAP / blk1,
            "fable_block4_requests": n4, "fable_worst_case_per_request_usd": per,
            "fable_block4_first_batch_max": max(0, min(n4, int(room // per))) if room > 0 else 0,
            "fable_block4_first_batch_max_with_sync_reserved": max(0, min(n4, int((room - sync) // per))) if room > sync else 0}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default=str(Path.home() / "aias" / "_worktrees" / "v0.42"), help="v0.42 repository (read only)")
    ap.add_argument("--out", default=str(V62 / "prereg" / "cost_estimate_v0_62_r3"))
    a = ap.parse_args(argv)
    commit, raw_b, bat_b = load_pinned(a.repo)
    recs = usage_lines(raw_b)
    del raw_b
    rec = reconcile(recs, bat_b)
    if not rec["matches_recorded_spend"] or rec["s0_max_line_difference_usd"] > 1e-9:
        raise SystemExit(f"reconciliation failed: {rec}")
    b = basis(recs)
    if sorted(b) != sorted((m, k) for m in MODELS for k in KINDS) or any(b[(m, k)]["n"] != {"B": 90, "A_yn": 88,
                                                                          "A_open": 24}[k] for m, k in b):
        raise SystemExit("unexpected S0 basis: " + json.dumps({f"{m}|{k}": v["n"] for (m, k), v in b.items()}))
    t = block_table(b)
    ref = {blk: sum(n * BG.part_cost(m, {"mode": MODE[m], "input_tokens": b[(m, kind)]["in_mean"],
                                         "output_tokens": b[(m, kind)]["out_mean"],
                                         "thinking_tokens": b[(m, kind)]["think_mean"], "n_searches": 0}, DAY["dec"])
                    * RESEND["high"] * FACTOR["high"][lg] for lg in LANGS for m in MODELS
                    for n in [N_PER_LANG[kind]]) for blk, kind, _ in BLOCKS}
    proj = projections(b)
    opt = brand_option(b, t)
    gp = {"conservative_high_dec": guard_path(t, "high", "dec"), "central_nov": guard_path(t, "central", "nov"),
          "central_dec": guard_path(t, "central", "dec")}
    designs = {}
    for o in "ABC":
        for mo in ("nov", "dec"):
            c, cc = design(b, "central", mo, FULL, o, True)
            _, hh = design(b, "high", mo, FULL, o, True)
            designs[f"option_{o}_{mo}"] = {"calls": c, "central": cc, "high": hh, "label": f"full design (blocks 1-5), option {o}"}
    for k, (kr, j) in DESIGNS.items():
        for mo in ("nov", "dec"):
            c, cc = design(b, "central", mo, kr, "A", j)
            _, hh = design(b, "high", mo, kr, "A", j)
            designs[f"{k}_{mo}"] = {"calls": c, "central": cc, "high": hh}
    r2 = json.loads((V62 / "prereg" / "cost_estimate_v0_62_r2.json").read_text(encoding="utf-8"))["designs"]
    basis_out = {}
    for (m, k), v in sorted(b.items()):
        basis_out[f"{m}|{k}"] = dict(v, per_call_usd={f"{lv}_{mo}": per_call(b, m, k, lv, mo)
                                                      for lv in ("central", "high") for mo in ("nov", "dec")})
    out = {"revision": "r3", "script": "osf/v62/scripts/cost_estimate_r3_v0_62.py", "no_model_called": True,
           "source": {"repo_tag": TAG, "commit": commit, "t4_raw": {"path": RAW[0], "sha256": RAW[1]},
                      "t4_batches": {"path": BATCHES[0], "sha256": BATCHES[1]},
                      "fields_read": list(USAGE_FIELDS), "answer_text_read": False},
           "prices_read": PRICES_READ, "price_days_utc": DAY, "language_factor_assumption": FACTOR, "resend_overhead": RESEND,
           "judge_reserve_usd": BG.JUDGE_RESERVE_USD, "pause_usd": PAUSE, "cap_usd": CAP,
           "reconciliation": rec, "basis_t4_s0": basis_out, "blocks": t,
           "reference_high_factor_on_mean_tokens_dec": ref, "designs": designs,
           "projection": proj["by_option_full_design"], "projection_by_design": proj["by_design_option_A"],
           "guard_core": gp, "brand_question_option": opt,
           "projection_core_plus_yn": proj["by_option_core_plus_yn"],
           "guard_core_plus_yn": {key: guard_path_yn(t, proj["by_option_core_plus_yn"]["A"][mo], lv, mo)
                                  for key, lv, mo in (("conservative_high_dec", "high", "dec"),
                                                      ("central_nov", "central", "nov"), ("central_dec", "central", "dec"))},
           "r2_for_comparison": {k: {"calls": r2[k]["calls"], "central": r2[k]["central"], "high": r2[k]["high"]}
                                 for k in ("phase_b_only_dec", "phase_b_only_nov", "adopted_dec", "b_plus_ayn_dec")}}
    Path(a.out + ".json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    txt = render(out)
    Path(a.out + ".txt").write_text(txt, encoding="utf-8")
    print(txt, end="")
    return 0


def render(o):
    rc, t, opt, gp = o["reconciliation"], o["blocks"], o["brand_question_option"], o["guard_core"]
    L = ["AIAS v0.62 cost estimate r3 (no model called): re-based on t4's RECORDED usage, "
         f"v0.42 tag {TAG} -> {o['source']['commit'][:7]}.",
         f"Source: t4_raw.jsonl sha256 {RAW[1][:12]} ({rc['raw_lines']} lines; usage fields only, no answer text read), "
         f"t4_batches.jsonl sha256 {BATCHES[1][:12]} ({rc['batches_created']} batches, {rc['requests_in_created_batches']} requests).",
         f"Reconciliation: recorded cost ${rc['recorded_cost_usd_sum']:.4f} + t4 judge reserve $0.50 = "
         f"${rc['recorded_plus_t4_judge_reserve']:.4f} (record: ${RECORDED_SPEND_USD:.4f}) -> "
         f"{'OK' if rc['matches_recorded_spend'] else 'MISMATCH'}; S0 recorded ${rc['s0_recorded_usd']:.4f}, recomputed by "
         f"budget_v0_62 at t4's dates ${rc['s0_recomputed_usd_budget_v0_62_at_t4_dates']:.4f} "
         f"(max line difference {rc['s0_max_line_difference_usd']:.1e}).",
         f"t4 S0: {rc['s0_answered_lines']} answered lines, {rc['s0_answered_with_resend_or_retry']} with a re-send or retry; "
         f"not answered: {json.dumps(rc['s0_lines_not_answered'])} (non-transient, not billed, re-run).",
         f"Prices (read {PRICES_READ['read_utc']}): Fable 5.2 Batch 4/20; GPT-6 Astra 10/50; Gemini 4 Argon 2/10 to "
         "2026-11-30, 4/20 from 2026-12-01 (US$ per 1M tokens in/out). Sources: " +
         "; ".join(PRICES_READ[k][0] for k in ("anthropic", "openai", "google")),
         "Language factors (assumption, not measured): central ES 1.25 KO 1.75 ZH 1.50; high ES 1.50 KO 2.50 ZH 2.25.",
         "Per call: central = t4 mean tokens x 1.02 (re-sends); conservative high = t4 p90 tokens x 1.10.", "",
         "Basis: t4 S0 answered, per English call (tokens mean / p90 / max; US$ central | high, Nov / Dec):"]
    for k, v in o["basis_t4_s0"].items():
        pc = v["per_call_usd"]
        L.append(f"  {k:24s} n {v['n']:3d}  in {v['in_mean']:6.1f}/{v['in_p90']:6.1f}/{v['in_max']:4d}  "
                 f"out {v['out_mean']:7.1f}/{v['out_p90']:7.1f}/{v['out_max']:5d}  think(GPT, incl. in out) "
                 f"{v['think_mean']:6.1f}  ${pc['central_nov']:.5f}/{pc['central_dec']:.5f} | "
                 f"${pc['high_nov']:.5f}/{pc['high_dec']:.5f}")
    L += ["", "Per block, all three languages and models (US$):",
          f"  {'block':54s} {'calls':>5s} {'central Nov':>11s} {'central Dec':>11s} {'high Nov':>9s} {'high Dec':>9s}"]
    for k, v in t.items():
        L.append(f"  {k + '. ' + v['label']:54s} {v['calls']:5d} {v['central_nov']:11.2f} {v['central_dec']:11.2f} "
                 f"{v['high_nov']:9.2f} {v['high_dec']:9.2f}")
    j = BG.JUDGE_RESERVE_USD
    L.append(f"  {'judge reserve (only with block 5)':54s} {'(216)':>5s} {j:11.2f} {j:11.2f} {j:9.2f} {j:9.2f}")
    for lab, blks, judge in (("CORE: blocks 1-3", CORE, False), ("ADOPTED (r3 update): core + block 4", CORE + ("4",), False),
                             ("core + block 5 + judge reserve", CORE + ("5",), True),
                             ("full: blocks 1-5 + judge reserve", CORE + ("4", "5"), True)):
        L.append(f"  {lab:54s} {sum(t[k]['calls'] for k in blks):5d} " + " ".join(
            f"{total(t, blks, lv, mo, judge):{w}.2f}" for lv, mo, w in (("central", "nov", 11), ("central", "dec", 11),
                                                                       ("high", "nov", 9), ("high", "dec", 9))))
    core_ref = sum(o["reference_high_factor_on_mean_tokens_dec"][k] for k in CORE)
    r2 = o["r2_for_comparison"]
    L += ["", f"Headline (core, 810 calls): central ${total(t, CORE, 'central', 'nov'):.2f} if collected 2026-11-29/30 as planned "
          f"(${total(t, CORE, 'central', 'dec'):.2f} at December prices); conservative high ${total(t, CORE, 'high', 'dec'):.2f} "
          f"(December prices). r2 (proxy basis, December): ${r2['phase_b_only_dec']['central']:.2f} / ${r2['phase_b_only_dec']['high']:.2f}.",
          f"Reference: high language factors on t4 MEAN tokens x 1.10, December: core ${core_ref:.2f} (shows that the p90 "
          "tokens, not only the factors, drive the conservative high).", ""]
    g = gp["conservative_high_dec"]
    L.append(f"Guard on the core, conservative high (Dec): block 1 ${g['block1_usd']:.2f}; projection after block 1 "
             f"x 3.0 = ${g['projection_after_block1_usd']:.2f} -> {'PAUSE for the pre-registrant' if g['projection_pause'] else 'no pause'}; "
             f"if continued, the $80 pause falls after {g['runs_at_80']:.2f} runs and the $100 stop after {g['runs_at_100']:.2f} "
             "runs (before in-flight reservations).")
    for key in ("central_nov", "central_dec"):
        g = gp[key]
        L.append(f"Guard on the core, {key.replace('_', ' ')}: block 1 ${g['block1_usd']:.2f}; projection "
                 f"${g['projection_after_block1_usd']:.2f} -> {'PAUSE' if g['projection_pause'] else 'no pause'}.")
    L += ["", f"Brand questions (112) in the conservative-high case: core ${opt['core_high_dec']:.2f}; room under the $80 pause "
          f"${opt['room_under_80']:.2f}; under the $100 cap ${opt['room_under_100']:.2f}. Any subset fits under $80: "
          f"{'YES' if opt['any_fits'] else 'NO'}."]
    for r in opt["subsets"]:
        L.append(f"  {r['label']}: {r['calls']} calls; high ${r['high_dec']:.2f} (Dec), central ${r['central_nov']:.2f} (Nov) / "
                 f"${r['central_dec']:.2f} (Dec); fits under $80 at the conservative high: {r['fits_under_80_conservative_high']}; "
                 f"smallest budget covering core + this at the conservative high: ${r['smallest_budget_conservative_high']:.2f}; "
                 f"core + this under $80 at central: Nov {r['fits_under_80_central_nov']}, Dec {r['fits_under_80_central_dec']}.")
    L.append("  per language, high Dec: " + "; ".join(f"{k} {v['calls']} calls ${v['high_dec']:.2f}"
                                                     for k, v in opt["per_language_high_dec"].items()))
    L += ["", "Projection-pause ratio (central design / central block 1): full design, option A: "
          f"Nov {o['projection']['A']['nov']:.4f}, Dec {o['projection']['A']['dec']:.4f}; core 3.0000; core + block 4: "
          f"Nov {o['projection_by_design']['core_plus_yn']['nov']:.4f}, Dec {o['projection_by_design']['core_plus_yn']['dec']:.4f}."]
    y4 = CORE + ("4",)
    L += ["", "r3 update (2026-11-12): ADOPTED DESIGN = core + block 4 (the 88 yes/no brand questions per language, 792 calls, "
          "collected last; pre-registrant's decision of 2026-11-12 00:48 CT, section 9 item 7 (b)); block 5 and the judge "
          "reserve are not collected.",
          f"Headline (core + block 4, {sum(t[k]['calls'] for k in y4)} calls): central ${total(t, y4, 'central', 'nov'):.2f} "
          f"if collected 2026-11-29/30 as planned (${total(t, y4, 'central', 'dec'):.2f} at December prices); conservative "
          f"high ${total(t, y4, 'high', 'dec'):.2f} (December prices). Block 4 alone: central ${t['4']['central_nov']:.2f} "
          f"(Nov) / ${t['4']['central_dec']:.2f} (Dec), conservative high ${t['4']['high_dec']:.2f}.",
          "Projection-pause ratio of core + block 4 by headphones option (Nov / Dec): " + "; ".join(
              f"{k} {v['nov']:.4f} / {v['dec']:.4f}" for k, v in o["projection_core_plus_yn"].items()) + "."]
    for key, g in o["guard_core_plus_yn"].items():
        e = g["block_end_spend_usd"]
        reached = g["stop_100_falls_in_block"] is None and g["pause_80_falls_in_block"] in (None, "4")
        L.append(f"Guard on core + block 4, {key.replace('_', ' ')}: spend at the end of blocks 1-4 "
                 + " / ".join(f"${e[k]:.2f}" for k in ("1", "2", "3", "4"))
                 + f"; projection after block 1 ${g['block1_usd']:.2f} x {g['projection_ratio']:.4f} = "
                 f"${g['projection_after_block1_usd']:.2f} -> {'PAUSE for the pre-registrant' if g['projection_pause'] else 'no pause'}; "
                 f"$80 pause falls in block {g['pause_80_falls_in_block'] or '- (never)'}; $100 stop falls in block "
                 f"{g['stop_100_falls_in_block'] or '- (never)'}; block 4 "
                 + (f"reached; Claude Fable 5.2's block-4 batch: at most {g['fable_block4_first_batch_max']} of "
                    f"{g['fable_block4_requests']} requests in its first batch under the $100 rule's worst-case reservations "
                    f"(${g['fable_worst_case_per_request_usd']:.4f} each; {g['fable_block4_first_batch_max_with_sync_reserved']} "
                    "while both synchronous workers hold their reservations); the rest go in later batches." if reached
                    else "not reached (the $100 stop falls inside the category-question runs) unless the pre-registrant "
                         "approves past the pauses and raises the cap."))
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main())
