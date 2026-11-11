#!/usr/bin/env python3
"""
judge_v1_15.py - AIAS v1.15 (Sentiment on t4): the judge run, the only paid calls of v1.15.

STATUS: r0 draft (2026-11-10/11), not locked. PRE_REGISTRATION_v1_15.md sections 4, 6 and 7.

Derived from scripts/judge_v1_11.py WITHOUT editing it: that file (byte-identical to tag v1.11-prereg-r1, git blob
85ad069c...) is imported and run with v1.15's own paths, blackout windows, pre-registration guard and process
check. Everything else is v1.11's code, unchanged: the judges (J1 claude-opus-5-5 on Anthropic's Message Batches
API, J2 gpt-6.1-sol on OpenAI's Batch API, alternate gemini-4-argon), the request (no sampling parameter, effort
"low", output cap 4,096 tokens, prompt-only JSON), the batch path (<= 500 requests per batch, journal of every
submitted batch, re-attachment after an interruption, never resent), the cost guard (worst case reserved before
every call / batch; hard stop US$100; pause at US$80 of recorded spend until --approve-past-pause; 30,000 calls),
calibration (first 200 calls per judge) and the binding projection, the alternate's replacement rule.
v1.15 has its own US$100 cap: spend is read from v1.15's own raw file only.

Window rule (section 6). A batch is submitted only if its whole 24-hour processing window lies inside an allowed
window: (a) from t4's completion (tag v0.42-acquisition-locked on origin) to 2026-11-14 00:00 UTC (Coverage's
collection), or (b) from t5's completion (its acquisition tag on origin, and not before 2026-12-06 00:00 UTC) to
2026-12-10 00:00 UTC. Never November 17-21. A run not finished at the end of (a) stops and resumes in (b) with the
same plan and unit table.

Modes: --dry-run (no network, no SDK import), --simulate (fake judge + fake batch service on a synthetic t4 unit
table), --run, --freeze, --replace ROLE=ALT --reason.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_v1_15 as T  # noqa: E402

S = T.S
sys.path.insert(0, str(T.ROOT / "scripts"))
import judge_v1_11 as J  # noqa: E402  (byte-identical to v1.11-prereg-r1:scripts/judge_v1_11.py)

V = S.V
UTC = timezone.utc
RAW_NAME, FROZEN_NAME = "judge_raw_v1_15.jsonl", "judge_outputs_frozen_v1_15.json"
COVERAGE_START = datetime(2026, 11, 14, 0, 0, tzinfo=UTC)
T5_EARLIEST = datetime(2026, 12, 6, 0, 0, tzinfo=UTC)
WINDOW_B_END = datetime(2026, 12, 10, 0, 0, tzinfo=UTC)
FAR_PAST, FAR_FUTURE = datetime(2026, 1, 1, tzinfo=UTC), datetime(2099, 1, 1, tzinfo=UTC)
T4_DONE_TAG = T.V042_RAW_TAG                     # "v0.42-acquisition-locked"
T5_DONE_TAG = "v0.45-acquisition-locked"         # t5 = v0.45 r0 (open question O3: confirm at the lock)
OTHER_COLLECTION = re.compile(J.OTHER_COLLECTION.pattern + r"|judge_v\d+_\d+\.py")


def blackouts(t4_done: datetime | None, t5_done: datetime | None) -> list:
    """The complement of the allowed windows (a) and (b), as v1.11's (name, start, end) list; t4_done / t5_done
    are the completion times (None = not complete). Nov 17-21 lies inside the second interval in every case."""
    b_open = max(t5_done, T5_EARLIEST) if t5_done else FAR_FUTURE
    a_open = t4_done if t4_done and t4_done < COVERAGE_START else COVERAGE_START
    return [("before window (a): t4 collection not complete", FAR_PAST, a_open),
            ("between windows (a) and (b): Coverage, Nov 17-21, v1.11's judge run, t5 collection", COVERAGE_START, b_open),
            ("after window (b): S_t4 must exist before the Preview's data lock (Dec 11)", WINDOW_B_END, FAR_FUTURE)]


def remote_tag(tag: str, ls_remote_out: str | None = None) -> dict:
    """{ref: sha} for refs/tags/TAG and refs/tags/TAG^{} on origin. Uses the pattern `refs/tags/TAG*`, because
    `git ls-remote --tags origin TAG` drops the peeled `^{}` line under git 2.54."""
    if ls_remote_out is None:
        r = subprocess.run(["git", "-C", str(T.ROOT), "ls-remote", "origin", f"refs/tags/{tag}*"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"REFUSED: git ls-remote failed: {r.stderr.strip()[:200]}")
        ls_remote_out = r.stdout
    out = {}
    for line in ls_remote_out.splitlines():
        if "\t" in line:
            sha, ref = line.split("\t", 1)
            if ref in (f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"):
                out[ref] = sha
    return out


def tag_time(tag: str):
    """Commit time (UTC) of a tag that exists on origin, else None (read-only: git ls-remote, git log)."""
    if f"refs/tags/{tag}" not in remote_tag(tag):
        return None
    c = subprocess.run(["git", "-C", str(T.ROOT), "log", "-1", "--format=%cI", f"{tag}^{{commit}}"],
                       capture_output=True, text=True)
    return datetime.fromisoformat(c.stdout.strip()).astimezone(UTC) if c.returncode == 0 and c.stdout.strip() else None


class Paths(J.Paths):
    """v1.11's Paths with v1.15's files (prereg: unit table and U0; data: raw, plan, journal; outputs: frozen)."""

    def __init__(self, dry: bool, base: Path | None = None):
        self.dry = dry
        b = Path(base) if base else None
        self.prereg = b or T.PREREG_DIR
        self.data = b or T.DATA_DIR
        self.out = b or T.OUTDIR
        self.units, self.u0 = self.prereg / T.UNITS_NAME, self.prereg / T.U0_NAME
        self.raw, self.plan = self.data / RAW_NAME, self.data / "plan_v1_15.json"
        self.roles = self.data / "roles_v1_15.json"
        self.guard_log, self.frozen = self.data / "guard_log_v1_15.jsonl", self.out / FROZEN_NAME
        self.batches = self.data / "batches_v1_15.jsonl"
        self.dry_txt = self.prereg / "dry_run_judge_v1_15.txt"
        self.cost_json = self.prereg / "cost_projection_v1_15.json"


def prereg_guard() -> str:
    """Refuse unless tag v1.15-prereg-r1 is on origin and anchor/git_anchor_v1_15.json anchors it with a non-empty
    osf_deposit (the check of score_v1_11.anchor_problems, applied to v1.15's anchor)."""
    shas = remote_tag(T.PREREG_TAG)
    ref = f"refs/tags/{T.PREREG_TAG}"
    if ref not in shas:
        sys.exit(f"REFUSED: tag {T.PREREG_TAG} not found on origin")
    if not T.ANCHOR_FILE.exists():
        sys.exit(f"REFUSED: anchor file missing: {T.ANCHOR_FILE}")
    anchor = json.loads(T.ANCHOR_FILE.read_text(encoding="utf-8"))
    commit = shas.get(ref + "^{}", shas[ref])
    bad = [f"anchor field missing: {k}" for k in S.ANCHOR_FIELDS if k not in anchor]
    if anchor.get("tag") != T.PREREG_TAG or anchor.get("commit") != commit:
        bad.append("anchor does not name the tag's commit")
    if not str(anchor.get("osf_deposit") or "").strip():
        bad.append("anchor has an empty osf_deposit")
    if bad:
        sys.exit("REFUSED: " + "; ".join(bad))
    return commit


def other_collections(ps_text: str | None = None, me: str = "") -> list:
    out = ps_text if ps_text is not None else subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True,
                                                               text=True).stdout
    return [line.strip() for line in out.splitlines()
            if OTHER_COLLECTION.search(line) and line.split()[0] != me and "judge_v1_15" not in line]


def freeze(P: Paths, log=print) -> int:
    if P.frozen.exists():
        log("REFUSED: already frozen")
        return 3
    if J.open_batches(P):
        log("REFUSED: batches are still in flight; run --run again to collect them first")
        return 3
    u0, _units = J.load_units(P)
    roles = J.current_roles(P)
    recs = J.read_raw(P.raw)
    oc = S.outcomes(recs, roles)
    doc = {"phase": T.PHASE_ID, "frozen_utc": J._now_dt().isoformat(), "raw_file": RAW_NAME,
           "raw_sha256": V.sha256(P.raw), "records": len(recs), "roles": roles,
           "batches_sha256": V.sha256(P.batches) if P.batches.exists() else None,
           "plan_sha256": V.sha256(P.plan), "units_sha256": u0["units_file"]["sha256"], "u0_refs": u0.get("refs", {}),
           "spend_usd": sum(float(r.get("usd") or 0) for r in recs),
           "outcomes": {f"{r} {p}": dict(Counter(v["status"] for k, v in oc.items() if k[0] == r and k[2] == p))
                        for r in ("J1", "J2") for p in ("main", "repeat")},
           "sampling_parameters_sent": sorted({w for r in recs for w in r.get("sampling_parameters_sent", [])}),
           "served_models": dict(Counter(r.get("served_model") for r in recs))}
    P.frozen.parent.mkdir(parents=True, exist_ok=True)
    P.frozen.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    log(f"[v1.15] frozen: {len(recs)} records, spend ${doc['spend_usd']:.2f}")
    return 0


def dry_run(P: Paths, log=print) -> int:
    """No network, no SDK import: every request built, sampling-parameter check, planning projection."""
    _u0, units = J.load_units(P)
    jobs, by = J.jobs_for(units, S.DEFAULT_PLAN)
    roles = dict(J.DEFAULT_ROLES)
    bad = 0
    for j in jobs:
        u = by[j["unit_id"]]
        req = S.build_request(u)
        kw = J.request_kwargs(roles[j["role"]], J.provider_of_model(roles[j["role"]]), req["system"], req["user"])
        bad += bool(J.sampling_params_sent(kw))
    ipc = {r: S.plan_tokens_per_char(J.provider_of_model(m)) for r, m in roles.items()}
    opc = {r: float(S.PLAN_OUT_VISIBLE + S.PLAN_REASONING) for r in roles}
    proj = J.project_jobs(jobs, by, roles, ipc, opc, datetime(2026, 12, 7, tzinfo=UTC))
    lines = [f"jobs {len(jobs)} ({dict(Counter((j['role'], j['phase']) for j in jobs))})",
             f"requests with a sampling parameter: {bad}",
             f"planning projection (characters/4 x vendor factor, r = {S.PLAN_REASONING}): "
             f"${proj['usd']:.2f}; with overhead ${proj['usd_with_overhead']:.2f}",
             f"provider SDKs imported: {[m for m in ('anthropic', 'openai', 'google.genai') if m in sys.modules] or 'none'}"]
    P.dry_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for x in lines:
        log(x)
    return 0 if bad == 0 else 1


def simulate(base: Path, log=print, max_new_calls=None) -> int:
    """End-to-end on a synthetic t4 unit table already written to `base` (tests): fake judge, fake batches,
    interruption with a batch in flight, re-attachment, freeze. No network."""
    P = Paths(dry=True, base=base)
    fake = J.FakeJudge()
    dispatch = {k: fake(k) for k in ("anthropic", "openai", "google")}
    bc = J.FakeBatchClient(fake, interrupt_after=2)
    rc1 = J.run(P, dispatch, sim=True, log=log, bc=bc, max_new_calls=max_new_calls)
    rc2 = J.run(P, dispatch, sim=True, log=log, bc=bc)
    rcf = freeze(P, log)
    sent = Counter(bc.submitted)
    return {"rc": [rc1, rc2, rcf], "batches": bc.n_submits, "resent": any(v > 1 for v in sent.values()),
            "records": len(J.read_raw(P.raw))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="AIAS v1.15 Sentiment on t4: judge run")
    m = ap.add_mutually_exclusive_group(required=True)
    m.add_argument("--dry-run", action="store_true")
    m.add_argument("--run", action="store_true")
    m.add_argument("--freeze", action="store_true")
    m.add_argument("--replace", metavar="ROLE=ALT")
    ap.add_argument("--reason")
    ap.add_argument("--approve-past-pause", metavar="WHO_WHEN")
    ap.add_argument("--no-other-collection", metavar="WHO_WHEN")
    a = ap.parse_args(argv)
    P = Paths(dry=False)
    if a.dry_run:
        return dry_run(P)
    if a.freeze:
        return freeze(P)
    if a.replace:
        if not a.reason:
            ap.error("--replace needs --reason")
        return J.replace(P, a.replace, a.reason)
    commit = prereg_guard()
    J.BLACKOUTS[:] = blackouts(tag_time(T4_DONE_TAG), tag_time(T5_DONE_TAG))
    b = J.blackout_within(J._now_dt())
    if b:
        sys.exit(f"REFUSED: outside the allowed windows ({b})")
    oc = other_collections(me=str(__import__('os').getpid()))
    if oc:
        sys.exit("REFUSED: another collection or judge process is running: " + "; ".join(x[:100] for x in oc))
    if not a.no_other_collection:
        sys.exit('REFUSED: give --no-other-collection "<who, when>"')
    J.require_keys(J.current_roles(P))
    u0refs = json.loads(P.u0.read_text(encoding="utf-8")).get("refs", {})
    J.log_guard(P, {"event": "run started", "attestation": a.no_other_collection, "prereg_commit": commit,
                    "u0_refs": u0refs,
                    "blackouts": [(n, x.isoformat(), y.isoformat()) for n, x, y in J.BLACKOUTS],
                    "environment": J.sdk_versions()})
    return J.run(P, J.DISPATCH, approval=a.approve_past_pause, bc=J.RealBatchClient())


if __name__ == "__main__":
    sys.exit(main())
