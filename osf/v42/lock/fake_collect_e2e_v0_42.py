#!/usr/bin/env python3
"""End-to-end rehearsal of the v0.42 lock-and-collect path on LOCAL FAKES (osf/v42/LOCK_STEPS.md step R).

Copies osf/v42/{prereg,scripts,lock} into a scratch repository with a local bare `origin`, then runs the REAL
`acquire_v0_42.py --collect` (and write_anchor_v0_42.py) as subprocesses with PYTHONPATH=osf/v42/lock/fakes, where
`anthropic`, `openai` and `google.genai` are local fakes that bill to a file instead of a provider. Fake API keys;
HTTPS_PROXY/HTTP_PROXY and the SDK base URLs point at 127.0.0.1:9, so even a missed fake could not reach a provider.
Nothing is pushed to the real origin, nothing is written in the worktree.

Scenarios: anchor, normal, pause80, projection, interrupt, onecollection, window (default: all).
Usage: python3 osf/v42/lock/fake_collect_e2e_v0_42.py [--scratch DIR] [scenario ...]   (about 1-3 minutes)
"""
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WT / "osf/v42/scripts"))
import budget_v0_42 as BG  # noqa: E402

TAG = "v0.42-prereg-r1"
RESULTS = []


def sh(cmd, cwd, check=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=isinstance(cmd, str))
    if check and r.returncode:
        raise RuntimeError(f"{cmd}: {r.stderr}")
    return r


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""), flush=True)


class Repo:
    def __init__(self, base):
        self.base = Path(base)
        self.root = self.base / "repo"
        self.origin = self.base / "origin.git"
        for d in ("prereg", "scripts", "lock"):
            shutil.copytree(WT / "osf/v42" / d, self.root / "osf/v42" / d,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        sh("git init -q -b v0.42 && git add -A && git -c user.name=fake -c user.email=fake@example.invalid "
           "commit -qm 'scratch copy for the fake rehearsal'", self.root)
        sh(f"git init -q --bare {self.origin}", self.base)
        sh(f"git remote add origin {self.origin} && git push -q origin v0.42", self.root)
        self.script = self.root / "osf/v42/scripts/acquire_v0_42.py"
        for rel in ("osf/v42/scripts/acquire_v0_42.py", "osf/v42/scripts/budget_v0_42.py"):
            same = hashlib.sha256((WT / rel).read_bytes()).digest() == hashlib.sha256((self.root / rel).read_bytes()).digest()
            assert same, rel

    def tag_and_push(self):
        sh(f"git -c user.name=fake -c user.email=fake@example.invalid tag -a {TAG} -m fake HEAD && "
           f"git push -q origin refs/tags/{TAG}", self.root)

    def env(self, state, **extra):
        e = dict(os.environ)
        e.update({"AIAS_ROOT": str(self.root), "PYTHONPATH": str(WT / "osf/v42/lock/fakes"), "PYTHONDONTWRITEBYTECODE": "1",
                  "FAKE_STATE": str(state), "FAKE_FAST": "1", "ANTHROPIC_API_KEY": "fake", "OPENAI_API_KEY": "fake",
                  "GOOGLE_API_KEY": "fake", "HTTPS_PROXY": "http://127.0.0.1:9", "HTTP_PROXY": "http://127.0.0.1:9",
                  "ANTHROPIC_BASE_URL": "http://127.0.0.1:9", "OPENAI_BASE_URL": "http://127.0.0.1:9"})
        e.pop("GEMINI_API_KEY", None)
        e.update({k: str(v) for k, v in extra.items()})
        return e

    def collect(self, state, *args, **extra):
        r = subprocess.run([sys.executable, str(self.script), "--collect", *args], cwd=self.root,
                           env=self.env(state, **extra), capture_output=True, text=True, timeout=900)
        return r.returncode, r.stdout + r.stderr

    def reset_data(self):
        shutil.rmtree(self.root / "osf/v42/data", ignore_errors=True)

    @property
    def raw(self):
        return self.root / "osf/v42/data/t4_raw.jsonl"

    def lines(self):
        return [json.loads(l) for l in self.raw.read_text().splitlines()] if self.raw.exists() else []

    def journal(self):
        p = self.root / "osf/v42/data/t4_batches.jsonl"
        return [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []


def bill(state):
    p = Path(state) / "bill.jsonl"
    rows = [json.loads(l) for l in p.read_text().splitlines()] if p.exists() else []
    return rows, sum(BG.part_cost(r["model"], r) for r in rows)


def summarize(repo, state):
    lines = repo.lines()
    ok = {r["call_id"] for r in lines if r["status"] == "ok"}
    rec = sum(r["cost_usd"] for r in lines)
    rows, billed = bill(state)
    batches = sorted((Path(state) / "batches").glob("*.json")) if (Path(state) / "batches").exists() else []
    sizes = [len(json.loads(b.read_text())["requests"]) for b in batches]
    return {"lines": len(lines), "ok_calls": len(ok), "recorded_usd": round(rec, 4), "billed_usd": round(billed, 4),
            "billed_requests": len(rows), "batches": sizes,
            "blocks": sorted({(r["phase"], r["condition"], r["run"]) for r in lines})}


def scen_anchor(repo, tmp):
    st = tmp / "s_anchor"
    rc, out = repo.collect(st)
    check("anchor: refused before the tag is on origin", rc != 0 and "not found on origin" in out, out.strip()[-90:])
    repo.tag_and_push()
    rc, out = repo.collect(st)
    check("anchor: refused with the tag but no anchor file", rc != 0 and "anchor file missing" in out, out.strip()[-90:])
    anchor = repo.root / "osf/v42/anchor/osf_anchor_v0_42.json"
    anchor.parent.mkdir(parents=True, exist_ok=True)
    anchor.write_text(json.dumps({"tag": TAG, "commit": "0" * 40}))
    rc, out = repo.collect(st)
    check("anchor: refused when the anchor names another commit", rc != 0 and "does not name the commit" in out,
          out.strip()[-90:])
    anchor.unlink()
    r = subprocess.run([sys.executable, str(repo.root / "osf/v42/lock/write_anchor_v0_42.py")], cwd=repo.root,
                       env=repo.env(st), capture_output=True, text=True)
    commit = sh(f"git rev-parse {TAG}^{{commit}}", repo.root).stdout.strip()
    ok = r.returncode == 0 and commit in anchor.read_text()
    check("anchor: write_anchor_v0_42.py writes an anchor naming the tag's commit", ok, (r.stdout + r.stderr).strip()[-120:])
    check("anchor: no request was sent by the refused runs", not (st / "bill.jsonl").exists())
    if not ok:
        sys.exit("no anchor: the other scenarios cannot run")


def scen_normal(repo, tmp):
    repo.reset_data()
    st = tmp / "s_normal"
    rc, out = repo.collect(st)
    s = summarize(repo, st)
    check("normal: full run exits 0", rc == 0, f"rc={rc}")
    check("normal: 876 calls answered, one line each", s["ok_calls"] == 876 and s["lines"] == 876,
          f"lines {s['lines']}, answered {s['ok_calls']}")
    check("normal: Fable sent as 7 batches of 30,30,30,112,30,30,30", s["batches"] == [30, 30, 30, 112, 30, 30, 30], str(s["batches"]))
    check("normal: every billed request recorded at the same cost", abs(s["recorded_usd"] - s["billed_usd"]) < 1e-6
          and s["billed_requests"] == 876, f"recorded ${s['recorded_usd']} billed ${s['billed_usd']}")
    check("normal: no pause (spend < $80, projection < $100)", rc == 0 and "PAUSE" not in out and "HALT" not in out,
          f"spend ${s['recorded_usd'] + BG.JUDGE_RESERVE_USD:.2f} incl. judge reserve")
    check("normal: journal shows every batch recorded", all(e["event"] in ("created", "recorded") for e in repo.journal())
          and sum(e["event"] == "created" for e in repo.journal()) == sum(e["event"] == "recorded" for e in repo.journal()) == 7)
    rc2, out2 = repo.collect(st)
    s2 = summarize(repo, st)
    check("normal: a second --collect sends nothing (resumable, all done)", rc2 == 0 and s2["billed_requests"] == 876
          and s2["lines"] == 876, f"rc={rc2}")
    return s


def scen_pause80(repo, tmp):
    repo.reset_data()
    st = tmp / "s_pause80"
    rc, out = repo.collect(st, FAKE_SCALE=1.5)
    s = summarize(repo, st)
    spend = s["recorded_usd"] + BG.JUDGE_RESERVE_USD
    check("pause80: run pauses (exit 5) on the $80 rule from recorded usage", rc == 5 and ">= $80" in out,
          f"rc={rc}, spend ${spend:.2f}, lines {s['lines']}, blocks reached {len(s['blocks'])}")
    check("pause80: recorded = billed at the pause (nothing in flight unrecorded)",
          rc == 5 and abs(s["recorded_usd"] - s["billed_usd"]) < 1e-6, f"recorded ${s['recorded_usd']:.4f}")
    rc, out = repo.collect(st, FAKE_SCALE=1.5)
    s2 = summarize(repo, st)
    check("pause80: re-run without approval sends nothing and pauses again", rc == 5 and s2["billed_requests"] == s["billed_requests"])
    rc, out = repo.collect(st, "--approve-past-80", "FAKE rehearsal approval", FAKE_SCALE=1.5)
    s3 = summarize(repo, st)
    spend3 = s3["billed_usd"] + BG.JUDGE_RESERVE_USD
    check("pause80: with --approve-past-80 it continues and the $100 cap holds", rc in (0, 6) and spend3 <= 100.0 + 1e-9,
          f"rc={rc}, billed+reserve ${spend3:.2f}, ok calls {s3['ok_calls']}, " + ("hard stop" if rc == 6 else "done"))
    return s, s3, rc


def scen_projection(repo, tmp):
    repo.reset_data()
    st = tmp / "s_proj"
    rc, out = repo.collect(st, FAKE_S1_SCALE=2.2)
    s = summarize(repo, st)
    spend = s["recorded_usd"] + BG.JUDGE_RESERVE_USD
    blocks = s["blocks"]
    check("projection: pauses (exit 5) after block B-S1 run 1, before S1 run 2", rc == 5 and "projection" in out
          and ("B", "S1", 1) in [tuple(b) for b in blocks] and ("B", "S1", 2) not in [tuple(b) for b in blocks],
          f"rc={rc}, spend ${spend:.2f}; " + next((l.strip()[:150] for l in out.splitlines() if "PAUSE (projection)" in l), ""))
    rc2, out2 = repo.collect(st, FAKE_S1_SCALE=2.2)
    s2 = summarize(repo, st)
    check("projection: re-run without approval sends nothing and pauses again", rc2 == 5 and s2["billed_requests"] == s["billed_requests"])
    rc3, out3 = repo.collect(st, "--approve-projection", "FAKE rehearsal approval", FAKE_S1_SCALE=2.2)
    s3 = summarize(repo, st)
    check("projection: with --approve-projection it continues (then the $80/$100 rules apply)", s3["billed_requests"] > s["billed_requests"],
          f"rc={rc3}, spend ${s3['recorded_usd'] + BG.JUDGE_RESERVE_USD:.2f}, " + ("$80 pause" if rc3 == 5 else "stop" if rc3 == 6 else "done"))


def scen_interrupt(repo, tmp):
    repo.reset_data()
    st = tmp / "s_int"
    p = subprocess.Popen([sys.executable, str(repo.script), "--collect"], cwd=repo.root,
                         env=repo.env(st, FAKE_BATCH_SECONDS=100000), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    t0 = time.time()
    while time.time() - t0 < 60 and not any(e["event"] == "created" for e in repo.journal()):
        time.sleep(0.2)
    time.sleep(1.0)
    p.send_signal(signal.SIGKILL)                       # crash while the first Fable batch is in flight
    p.wait()
    s = summarize(repo, st)
    fable_lines = sum(1 for r in repo.lines() if r["model_requested"] == "claude-fable-5-2")
    check("interrupt: killed with a Fable batch in flight (30 billed, 0 recorded)", s["batches"] == [30] and fable_lines == 0,
          f"billed ${s['billed_usd']:.4f} vs recorded ${s['recorded_usd']:.4f}")
    rc, out = repo.collect(st)
    s2 = summarize(repo, st)
    check("interrupt: resume recovers the batch before any new request", "recovering batch msgbatch_0001" in out, "")
    check("interrupt: resumed run completes; Fable batches created = 7 (nothing re-sent)", rc == 0 and len(s2["batches"]) == 7
          and s2["ok_calls"] == 876, f"rc={rc}, batches {s2['batches']}")
    gap = s2["billed_usd"] - s2["recorded_usd"]
    check("interrupt: recorded spend = billed spend except synchronous requests killed mid-call",
          rc == 0 and 0 <= gap < 2 * max(BG.worst_case("gpt-6-astra", "S0"), BG.worst_case("gemini-4-argon", "S0")) + 1e-9,
          f"billed ${s2['billed_usd']:.4f}, recorded ${s2['recorded_usd']:.4f}, unrecorded ${gap:.4f}; "
          f"billed requests {s2['billed_requests']} for 876 calls")


def scen_onecollection(repo, tmp):
    repo.reset_data()
    st = tmp / "s_one"
    launcher = (f"cd {repo.root} && exec caffeinate -dimsu {sys.executable} {repo.script} --collect")
    p = subprocess.Popen(["/bin/zsh", "-c", launcher], env=repo.env(st, FAKE_BATCH_SECONDS=100000),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    t0 = time.time()
    while time.time() - t0 < 60 and not any(e["event"] == "created" for e in repo.journal()):
        time.sleep(0.2)
    alive = p.poll() is None
    check("one: a collection started as `caffeinate <python> acquire --collect` does not refuse itself", alive,
          "running" if alive else (p.stdout.read() or "")[-200:])
    rc, out = repo.collect(tmp / "s_one_b")
    check("one: a second v0.42 --collect is refused while the first runs", rc != 0 and "another paid collection" in out,
          out.strip().splitlines()[-1][:160] if out.strip() else "")
    probe = ("import sys, datetime; sys.path.insert(0, '/Users/pablou/aias/_worktrees/v1.12/osf/methodology/v1_12/scripts');"
             "import acquire_v1_12 as A\ntry:\n    A.other_collection_guard(); print('V112 GUARD PASSED')\n"
             "except SystemExit as e:\n    print('V112', str(e)[:160])")
    r = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True)
    check("one: v1.12's own guard sees the running v0.42 collection", "REFUSED: another paid collection" in r.stdout,
          r.stdout.strip()[:160])
    for q in subprocess.run(["pgrep", "-f", str(repo.script)], capture_output=True, text=True).stdout.split():
        os.kill(int(q), signal.SIGKILL)
    p.wait()


def scen_window(repo, tmp):
    repo.reset_data()
    st = tmp / "s_win"
    (repo.root / "osf/v42/data").mkdir(parents=True, exist_ok=True)
    old = {"call_id": "v20|B|x|gpt-6-astra|S0|1", "phase": "B", "condition": "S0", "run": 1, "status": "error",
           "text": "", "error": "fake", "model_requested": "gpt-6-astra", "started_utc": "2026-11-06T00:00:00+00:00",
           "finished_utc": "2026-11-06T00:00:01+00:00", "usage_parts": [], "cost_usd": 0.0}
    repo.raw.write_text(json.dumps(old) + "\n")
    rc, out = repo.collect(st)
    check("window: a run whose first call is > 72 h old sends nothing and stops (exit 6)", rc == 6
          and not (st / "bill.jsonl").exists() and "window" in out, f"rc={rc}")


SCEN = {"anchor": scen_anchor, "normal": scen_normal, "pause80": scen_pause80, "projection": scen_projection,
        "interrupt": scen_interrupt, "onecollection": scen_onecollection, "window": scen_window}


def main():
    args = sys.argv[1:]
    base = None
    if args[:1] == ["--scratch"]:
        base, args = Path(args[1]), args[2:]
    names = args or list(SCEN)
    tmp = Path(base or tempfile.mkdtemp(prefix="v42_fake_e2e_"))
    tmp.mkdir(parents=True, exist_ok=True)
    print(f"scratch: {tmp}", flush=True)
    repo = Repo(tmp)
    r = subprocess.run([sys.executable, "-c", "from google import genai; import anthropic, openai; "
                        "print(genai.__file__); print(anthropic.__file__); print(openai.__file__)"],
                       env=repo.env(tmp / "s_import"), capture_output=True, text=True, cwd=repo.root)
    fakes = str(WT / "osf/v42/lock/fakes")
    paths = r.stdout.split()
    if len(paths) != 3 or not all(p.startswith(fakes) for p in paths):
        sys.exit(f"ABORT: the provider SDKs do not resolve to the local fakes: {paths} {r.stderr[-200:]}")
    check("setup: anthropic, openai and google.genai resolve to the local fakes", True)
    if "anchor" not in names:
        scen_anchor(repo, tmp)
    for n in names:
        print(f"--- {n}", flush=True)
        SCEN[n](repo, tmp)
    bad = [r for r in RESULTS if not r[1]]
    print(f"\n{len(RESULTS) - len(bad)} of {len(RESULTS)} checks PASS" + (f"; FAILED: {[b[0] for b in bad]}" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
