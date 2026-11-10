#!/usr/bin/env python3
"""Exercise audit_v1_13.collect_guard (protocol section 8) on simulated states and clocks (LOCK_STEPS.md step 1e).

No network and no write in the repository: git is replaced by a stub (tag present or absent, ls-remote answered
locally), the anchor and receipt are temporary files, and the clock is passed in. The real --collect is NOT run.
Exit 0 only if every scenario gives the expected outcome.
"""
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "osf/methodology/v1_13/scripts"))
sys.dont_write_bytecode = True
import audit_v1_13 as A  # noqa: E402

FAKE_COMMIT = "f" * 40
U = timezone.utc
RECEIPT = datetime(2026, 11, 11, 21, 30, tzinfo=U)       # example: Pablo receives the locked text Wed ~3:30 pm CT


def stub_git(tag_exists=True):
    def _git(args):
        if args[:2] == ["rev-list", "-n"]:
            return SimpleNamespace(returncode=0, stdout=(FAKE_COMMIT + "\n") if tag_exists else "", stderr="")
        if args[:2] == ["ls-remote", "--tags"]:
            return SimpleNamespace(returncode=0, stdout=f"{FAKE_COMMIT}\trefs/tags/{A.AUDIT_TAG}\n", stderr="")
        raise AssertionError(f"unexpected git call {args}")
    return _git


def run(now, *, tag=True, anchor=True, receipt=RECEIPT, commit=FAKE_COMMIT, domains_sha=None, pass_no=1):
    with tempfile.TemporaryDirectory() as td:
        A._git = stub_git(tag)
        A.AUDIT_ANCHOR = Path(td) / "audit_anchor_v1_13.json"
        A.AUDIT_RECEIPT = Path(td) / "audit_receipt_v1_13.json"
        if anchor:
            A.AUDIT_ANCHOR.write_text(json.dumps({"commit": commit, "brand_domains_sha256":
                                                  domains_sha or A.S.sha256_file(A.S.DOMAINS_CSV)}), encoding="utf-8")
        if receipt is not None:
            A.AUDIT_RECEIPT.write_text(json.dumps({"received_utc": receipt if isinstance(receipt, str)
                                                   else receipt.isoformat()}), encoding="utf-8")
        try:
            A.collect_guard(now, pass_no)
            return "PASSES"
        except A.Refused as e:
            return str(e)
        except Exception as e:                       # noqa: BLE001  (reported, not hidden)
            return f"CRASH {type(e).__name__}: {e}"


T = lambda *a: datetime(*a, tzinfo=U)  # noqa: E731
SCENARIOS = [
    ("no tag, no anchor, no receipt (today)", dict(now=T(2026, 11, 10, 21, 10), tag=False, anchor=False, receipt=None),
     "REFUSED"),
    ("tag, no anchor", dict(now=T(2026, 11, 13, 12), anchor=False), "audit_anchor_v1_13.json missing"),
    ("anchor names another commit", dict(now=T(2026, 11, 13, 12), commit="0" * 40), "anchor does not name"),
    ("tag + anchor, no receipt", dict(now=T(2026, 11, 13, 12), receipt=None), "audit_receipt_v1_13.json missing"),
    ("receipt + 23 h 59 min", dict(now=RECEIPT + timedelta(hours=23, minutes=59)), "fewer than 24 hours"),
    ("receipt + 24 h (Thu 2026-11-12 21:30Z)", dict(now=RECEIPT + timedelta(hours=24)), "PASSES"),
    ("pass 1 at 2026-11-13 23:59Z (72 h end before 11-17)", dict(now=T(2026, 11, 13, 23, 59)), "PASSES"),
    ("pass 1 at 2026-11-14 00:01Z (72 h would reach 11-17)", dict(now=T(2026, 11, 14, 0, 1)), "could not finish"),
    ("2026-11-17 00:00Z", dict(now=T(2026, 11, 17)), "blackout"),
    ("2026-11-19 12:00Z", dict(now=T(2026, 11, 19, 12)), "blackout"),
    ("2026-11-22 11:59Z", dict(now=T(2026, 11, 22, 11, 59)), "blackout"),
    ("2026-11-22 12:00Z", dict(now=T(2026, 11, 22, 12)), "PASSES"),
    ("pass 2 at 2026-11-16 12:00Z", dict(now=T(2026, 11, 16, 12), pass_no=2), "PASSES"),
    ("pass 2 at 2026-11-19 12:00Z", dict(now=T(2026, 11, 19, 12), pass_no=2), "blackout"),
    ("brand_domains differs from the anchor", dict(now=T(2026, 11, 13, 12), domains_sha="0" * 64), "differs from the anchored"),
    ("receipt written without UTC offset", dict(now=T(2026, 11, 13, 12), receipt="2026-11-11T21:30:00"), "CRASH TypeError"),
]

ok_all = True
for name, kw, expect in SCENARIOS:
    got = run(**kw)
    ok = (got == "PASSES") if expect == "PASSES" else (expect in got and (expect.startswith("CRASH") or got.startswith("REFUSED")))
    ok_all &= ok
    print(("OK   " if ok else "FAIL ") + f"{name}: {got}")
sys.exit(0 if ok_all else 1)
