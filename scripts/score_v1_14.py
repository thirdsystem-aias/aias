#!/usr/bin/env python3
"""
score_v1_14.py - AIAS v1.14, Ranking (redesigned measure): the modal-position statistic,
pre-registered after v1.10's sensitivity check, confirmed blind on the t4 and t5 waves.

STATUS: r1 draft (2026-11-10), to be locked at tag v1.14-prereg-r1. Rules transcribed from
osf/methodology/v1_14/prereg/PRE_REGISTRATION_v1_14.md (section cited inline).

What is new here and what is reused
  * The extractor (rules E0-E7), the registries of the five omnibus substrates, the rating floor,
    the pooled within-category Spearman (centred ranks), the permutation, shuffle and bootstrap
    machinery, the verdict bands and the seeds of the carried-over tests are v1.10's, imported
    unchanged from scripts/score_v1_10.py (locked at tag v1.10-prereg-r2).
  * The statistic is v1.10's sixth candidate, MODE (modal position): R* = -(the smallest modal
    competition min-rank k_min over the brand's rankable mentions), section 3.
  * The archived waves (t1-t3, EARLY-6) are CALIBRATION ONLY (section 4): they are read from
    v1.10's hashed rank tables, and the calibration must reproduce v1.10's sensitivity check S3
    (candidate MODE) exactly.
  * Stage 1 (section 5): t4 (v0.42, N3) separability, scored ONCE after v0.42's
    acquisition-locked tag and v1.14's anchor file exist.
  * Stage 2 (section 6): t4 -> t5 retest reliability, after Stage 1 and after the t5
    acquisition-locked tag exists.

Modes
  --calibration          archived waves (allowed before the lock); writes osf/methodology/v1_14/calibration/
  --stage 1              t4 separability (refuses before the lock; once only)
  --stage 2              t4 -> t5 retest (refuses before Stage 1 and the t5 tag)
  --lock-manifest        computes prereg/LOCK_MANIFEST_v1_14.sha256 (does not tag)
  --dry-run              Stage 1 / Stage 2 on a synthetic directory (--t4-dir / --t5-dir); bypasses the
                         lock refusal, writes to osf/methodology/v1_14/dryrun/outputs/
No network, no model calls.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_v1_10 as R  # noqa: E402  (v1.10's locked code, imported unchanged)

# ===========================================================================
# TRANSCRIBED CONSTANTS
# ===========================================================================
PHASE_ID = "v1.14"
PREREG_TAG = "v1.14-prereg-r1"
ROOT = Path(__file__).resolve().parents[1]
V114 = "osf/methodology/v1_14"
V110 = R.V110
ANCHOR_FILE = ROOT / V114 / "anchor/git_anchor_v1_14.json"
LOCK_MANIFEST = ROOT / V114 / "prereg/LOCK_MANIFEST_v1_14.sha256"
CAL_DIR = ROOT / V114 / "calibration"
CAL_FILE = CAL_DIR / "calibration_v1_14.json"
OUT_DIR = ROOT / V114 / "outputs"
DRY_OUT_DIR = ROOT / V114 / "dryrun/outputs"
V110_VERDICTS = ROOT / V110 / "outputs/v1_10_verdicts.json"
V110_OUTPUTS = ROOT / V110 / "outputs"
V110_COI = ROOT / V110 / "anchor/coi_flags_v1_10.json"

STAT = "MODE"                     # section 3: the declared statistic (v1.10 candidate 6)
RATING_FLOOR = R.RATING_FLOOR     # 6 rankable mentions (v1.10 section 5; v1.9 C* floor)
RUN_FLOOR = 3                     # per-run rating floor of the descriptive run reliability (D2, MQ7)
SEP_CONF, SEP_FALS = R.SEP_CONF, R.SEP_FALS          # 0.30 / 0.50
STAB_CONF, STAB_FALS = R.STAB_CONF, R.STAB_FALS      # 0.50 / 0.30
N_FLOOR_UNITS = R.N_FLOOR_UNITS   # 30
SEEDS = dict(R.SEEDS)             # H1 110001, H2 110002, H3 110003, SHUFFLE 110010, BOOT 110020, MQ7 110030
SEEDS.update({"H4_S1": 114001, "COMP_Coverage": 114002, "COMP_Grounding": 114003,
              "COMP_Sentiment": 114004})
COMPONENTS = ["Coverage", "Grounding", "Sentiment"]

# t4 = v0.42 (pre-registration r2, tag v0.42-prereg-r1) and the t5 repeat wave
V042_ACQ_TAG = "v0.42-acquisition-locked"
V042_CODER_PATH = "osf/v42/scripts/code_t4_v0_42.py"
V042_CODER_BLOB = "2d36735d512cf9e13b74010ba5a7f655fc7de0bc"   # v0.42 r2 section 5.1 (unchanged from r1)
T4_FILES = {"raw": "osf/v42/data/t4_raw.jsonl", "probes": "osf/v42/prereg/probes_v0_42.jsonl",
            "brand_table": "osf/v42/v42_brand_table.csv", "verdicts": "osf/v42/v42_verdicts.json",
            "coded_dir": "osf/v42/data/coded"}
N3 = ["claude-fable-5-2", "gpt-6-astra", "gemini-4-argon"]
CONDS = ["S0", "S1"]
RUNS = (1, 2, 3)
SUB_MAP = {"v19": "v0.19", "v20": "v0.20", "v21": "v0.21", "v22": "v0.22", "v23": "v0.23"}
FRAMES_PER_SUB = 6
EXPECTED_B_PER_SUB_COND = FRAMES_PER_SUB * len(N3) * len(RUNS)    # 54
C_STAR_DIVISOR, C_STAR_MIN_MENTIONS = 9.0, 6                      # shared P/C* definition (v1.12 2.6, v1.13 2.1)
DENON = ("v0.19", "Denon")

# v0.42 section 5.1: URLs removed before brand matching (copied verbatim from code_t4_v0_42.py)
MD_LINK_RE = re.compile(
    r"\[([^\]]*)\]\(\s*(?:<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
URL_RE = re.compile(r"https?://[^\s<>\"'\])]+", re.I)


class Halt(RuntimeError):
    """A pre-registered halt (hash mismatch, failed parity, order violation, refused stage)."""


def strip_urls(text):
    """= code_t4_v0_42.strip_urls: remove http(s) addresses and Markdown link targets (link text kept)."""
    if not text:
        return text or ""
    t = MD_LINK_RE.sub(r"\1", text)
    return URL_RE.sub(" ", t)


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob_bytes(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


# ===========================================================================
# THE STATISTIC (section 3)
# ===========================================================================


def modal_position(kmins) -> float:
    """R* = -(modal competition min-rank k_min over the brand's rankable mentions; the smallest
    mode, i.e. the position nearest the top, when several positions are equally frequent).
    Identical to v1.10's candidate MODE (score_v1_10.brand_scores). Higher = nearer the top."""
    k = np.asarray(list(kmins), int)
    if not len(k):
        return float("nan")
    vals, cnt = np.unique(k, return_counts=True)
    return float(-vals[cnt == cnt.max()].min())


def unit_scores(rows, floor: int = RATING_FLOOR) -> dict:
    """{(category, brand): {"n_ranked", "MODE", ..., "rated"}} for the rows of ONE panel x wave
    (x condition). All rankable mentions of the unit are pooled (models x runs x questions)."""
    return R.units_cat_brand(rows, floor)


# ===========================================================================
# CALIBRATION ON THE ARCHIVED WAVES (section 4) - allowed before the lock
# ===========================================================================


def read_rank_table(path: Path) -> dict:
    """One v1.10 per-answer rank table -> rows per rule (the input of every rank statistic,
    exactly as score_v1_10.rank_rows builds them), answers with text, and named sets."""
    rows = {rule: [] for rule in R.RULES}
    ok, named, meta = [], collections.defaultdict(set), {}
    seen_ok = set()
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            aid = r["answer_id"]
            if r["status"] != "ok":
                continue
            if aid not in seen_ok:
                seen_ok.add(aid)
                ok.append(aid)
                meta[aid] = r
            if r["brand"] and r["rule"] == "lead_item":
                named[aid].add(r["brand"])
            if r["brand"] and r["k_mid"] != "" and r["rankable"] == "1":
                rows[r["rule"]].append({
                    "panel": r["panel"], "wave": r["wave"], "category": r["category"], "answer_id": aid,
                    "model": r["model"], "run_idx": int(r["run_idx"]) if r["run_idx"] != "" else None,
                    "brand": r["brand"], "k_mid": float(r["k_mid"]), "k_min": int(r["k_min"]),
                    "n": int(r["n_named"])})
    return {"rows": rows, "answers_ok": ok, "named": named, "meta": meta}


def load_v110_tables(verdicts_path: Path = V110_VERDICTS, outputs: Path = V110_OUTPUTS) -> tuple[dict, dict]:
    """v1.10's hashed rank tables, verified against the SHA-256 recorded in its Stage C verdicts
    file (a mismatch halts). Returns ({set name: table}, verdicts) in v1.10's set order."""
    v = json.loads(Path(verdicts_path).read_text(encoding="utf-8"))
    tables = {}
    for name, e in v["rank_tables"].items():
        p = Path(outputs) / e["path"]
        if sha256_bytes(p.read_bytes()) != e["sha256"]:
            raise Halt(f"rank table hash mismatch: {p}")
        tables[name] = read_rank_table(p)
    return tables, v


def _set_role(name: str) -> str:
    return {"OMNI": "omni", "EARLY-6": "early6", "EARLY-2": "early2", "PAPER-B": "paperB"}[name.split()[0]]


def _omni_rows(tables, wave, rule="lead_item"):
    return [r for n, t in tables.items() if _set_role(n) == "omni" and n.split()[1] == wave for r in t["rows"][rule]]


def h4_from_tables(tables, stat, floor=RATING_FLOOR, boot=True) -> dict:
    """= score_v1_10.h4_block on the rank tables (EARLY-6, pi_hat = share of the set's answers with
    text naming the brand), in v1.10's set and unit order (so the permutation p reproduces)."""
    x, y, g = [], [], []
    for name, t in tables.items():
        if _set_role(name) != "early6":
            continue
        U = R.units_cat_brand(t["rows"]["lead_item"], floor)
        T = t["answers_ok"]
        for k, s in sorted(U.items()):
            if s["rated"]:
                x.append(sum(1 for a in T if k[1] in t["named"][a]) / len(T))
                y.append(s[stat])
                g.append(k[0])
    res = R.corr_test(x, y, g, R.SEEDS["H4"], "two", boot=boot)
    res["verdict"] = R.verdict_single_separability(res["rho"], res["n"])
    return res


def precision_note(ns=(30, 40, 55, 70, 90), rhos=(0.0, 0.10, 0.20, 0.25)) -> dict:
    """Section 7: approximate sampling distribution of a single-wave rho_w for n rated units:
    Fisher z with the Bonett-Wright variance (1 + r^2/2)/(n - 3). Analytic; no random draw.
    P(CONFIRMED) = P(|rho_hat| <= .30); P(FALSIFIED) = P(|rho_hat| >= .50)."""
    from math import atanh, erf, sqrt

    def Phi(z):
        return 0.5 * (1 + erf(z / sqrt(2)))
    out = {"method": "Fisher z, Bonett-Wright variance (1 + rho^2/2)/(n - 3); single wave; analytic",
           "separability": [], "retest": []}
    for n in ns:
        for rho in rhos:
            sd = sqrt((1 + rho * rho / 2) / (n - 3))
            mu = atanh(rho)
            pc = Phi((atanh(SEP_CONF) - mu) / sd) - Phi((-atanh(SEP_CONF) - mu) / sd)
            pf = 1 - Phi((atanh(SEP_FALS) - mu) / sd) + Phi((-atanh(SEP_FALS) - mu) / sd)
            out["separability"].append({"n": n, "true_rho": rho, "P_confirmed": pc, "P_falsified": pf,
                                        "ci90_halfwidth_at_rho": 1.645 * sd})
        for rho in (0.60, 0.70, 0.80, 0.86):
            sd = sqrt((1 + rho * rho / 2) / (n - 3))
            pc = 1 - Phi((atanh(STAB_CONF) - atanh(rho)) / sd)
            out["retest"].append({"n": n, "true_rho": rho, "P_rho_hat_ge_0.50": pc})
    return out


DEGEN_SHARE = 0.80        # MQ9: > 80% of rated units share one value -> separability UNDETERMINED
DEGEN_ZERO_SD_SUBS = 3    # MQ9: zero within-substrate spread in >= 3 of the 5 substrates -> UNDETERMINED


def degeneracy(U: dict, stat: str = STAT) -> dict:
    """MQ9 (section 5.5): a coarse statistic could pass the separability bands by having almost no spread.
    Over rated units: the share holding the most common value, and the substrates where every rated unit
    holds the same value."""
    vals = collections.defaultdict(list)
    for (c, _b), s in U.items():
        if s["rated"]:
            vals[c].append(s[stat])
    allv = [v for vs in vals.values() for v in vs]
    cnt = collections.Counter(allv)
    share = (max(cnt.values()) / len(allv)) if allv else float("nan")
    zero = sorted(c for c, vs in vals.items() if len(set(vs)) <= 1)
    return {"rated_units": len(allv), "value_counts": {str(k): v for k, v in sorted(cnt.items())},
            "share_most_common_value": share, "substrates_without_spread": zero,
            "flag_degenerate": bool(allv) and (share > DEGEN_SHARE or len(zero) >= DEGEN_ZERO_SD_SUBS)}


def _equal(a, b) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return float(a) == float(b)


def calibration(log=print, verdicts_path: Path = V110_VERDICTS, outputs: Path = V110_OUTPUTS,
                profiles: Path | None = None, coi_path: Path = V110_COI, full: bool = True) -> dict:
    """Section 4. MODE through v1.10's tests on the archived waves, from v1.10's hashed rank tables
    and the locked P / C* table. `full` adds H4, H5, MQ7, Stage S reliability, S7 and S9."""
    tables, v110 = load_v110_tables(verdicts_path, outputs)
    profiles = profiles or (ROOT / R.PROFILES_REL)
    man = json.loads((ROOT / V110 / "registries/INPUTS_MANIFEST_v1_10.json").read_text())
    pin = {e["path"]: e["sha256"] for e in man["files"]}
    if sha256_bytes(Path(profiles).read_bytes()) != pin.get(R.PROFILES_REL):
        raise Halt("profiles table differs from v1.10's pinned copy")
    with open(profiles, newline="", encoding="utf-8") as fh:
        prof_rows = list(csv.DictReader(fh))
    P, C, NM = R.parse_profiles(prof_rows)
    ow = {w: _omni_rows(tables, w) for w in R.WAVES}
    log(f"[v1.14] calibration: {sum(len(t['answers_ok']) for t in tables.values())} answers with text in "
        f"{len(tables)} v1.10 rank tables (hashes verified); OMNI rankable rows "
        + ", ".join(f"{w} {len(ow[w])}" for w in R.WAVES))
    excl = tuple(v110.get("gate_excluded_substrates", []))
    res = {"phase": PHASE_ID, "kind": "calibration on archived waves (declared calibration, not confirmatory)",
           "created_utc": _now(), "statistic": STAT,
           "inputs": {"v1_10_verdicts_sha256": sha256_bytes(Path(verdicts_path).read_bytes()),
                      "profiles_sha256": sha256_bytes(Path(profiles).read_bytes()),
                      "rank_tables": {n: e["sha256"] for n, e in v110["rank_tables"].items()}},
           "seeds": SEEDS}
    log("  H1-H3 with MODE (v1.10 S3 reproduction; bootstrap CIs added) ...")
    blk = R.gate_block(ow, STAT, RATING_FLOOR, P, C, excl, boot=True)
    res["H1_Sep_Presence"], res["H2_Sep_Consistency"], res["H3_Rank_Stability"] = blk["H1"], blk["H2"], blk["H3"]
    s3 = v110["sensitivities"]["S3_candidate_MODE"]["detail"]
    rep = {}
    for h in ("H1", "H2"):
        for w in R.WAVES:
            a, b = blk[h]["per_wave"][w], s3[h]["per_wave"][w]
            rep[f"{h}_{w}"] = {"v1_10_rho": b["rho"], "v1_14_rho": a["rho"], "v1_10_p": b["p_perm"],
                               "v1_14_p": a["p_perm"], "v1_10_n": b["n"], "v1_14_n": a["n"],
                               "identical": _equal(a["rho"], b["rho"]) and _equal(a["p_perm"], b["p_perm"])
                               and a["n"] == b["n"]}
    a, b = blk["H3"], s3["H3"]
    rep["H3"] = {"v1_10_rho": b["rho"], "v1_14_rho": a["rho"], "v1_10_p_perm": b["p_perm"], "v1_14_p_perm": a["p_perm"],
                 "v1_10_p_shuffle": b["p_shuffle"], "v1_14_p_shuffle": a["p_shuffle"], "v1_10_n": b["n"],
                 "v1_14_n": a["n"], "identical": _equal(a["rho"], b["rho"]) and _equal(a["p_perm"], b["p_perm"])
                 and _equal(a["p_shuffle"], b["p_shuffle"]) and a["n"] == b["n"]}
    res["reproduction_of_v1_10_S3_MODE"] = {"items": rep, "all_identical": all(x["identical"] for x in rep.values()),
                                            "v1_10_S3_verdicts": v110["sensitivities"]["S3_candidate_MODE"]["verdicts"]}
    res["verdicts_as_v1_10_would_read_them"] = {h: blk[h]["verdict"] for h in ("H1", "H2", "H3")}
    if full:
        log("  H5 (t2 -> t3) and t1 -> t3 with MODE ...")
        res["H5_Rank_LongHorizon"] = R.stability(ow["t2"], ow["t3"], STAT, RATING_FLOOR, R.SEEDS["H5"])
        res["H5_t1_t3_descriptive"] = R.stability(ow["t1"], ow["t3"], STAT, RATING_FLOOR, None, nulls=False)
        log("  H4 (EARLY-6, pi_hat) with MODE; MNP re-computed as a check of the reader ...")
        res["H4_Sep_Presence_Early"] = h4_from_tables(tables, STAT)
        h4m = h4_from_tables(tables, "MNP", boot=False)
        res["check_H4_MNP_equals_v1_10"] = {"v1_10": v110["H4_Sep_Presence_Early"]["rho"], "v1_14": h4m["rho"],
                                            "v1_10_p": v110["H4_Sep_Presence_Early"]["p_perm"], "v1_14_p": h4m["p_perm"],
                                            "identical": _equal(h4m["rho"], v110["H4_Sep_Presence_Early"]["rho"])
                                            and _equal(h4m["p_perm"], v110["H4_Sep_Presence_Early"]["p_perm"])}
        e6 = [r for n, t in tables.items() if _set_role(n) == "early6" for r in t["rows"]["lead_item"]]
        rel, nun = R._reliabilities(e6)
        res["StageS_split_half_reliability"] = {"reliability": rel, "n_units": nun,
                                                "v1_10_reliability": v110["selection"]["reliability"],
                                                "identical": all(_equal(rel[s], v110["selection"]["reliability"][s])
                                                                 for s in R.CANDIDATES)}
        log("  MQ7 (within-answer shuffle, 2,000 draws) with MODE ...")
        res["MQ7_MODE"] = R.mq7_negative_control(e6, STAT)
        flagged = set()
        if Path(coi_path).exists():
            for f in json.loads(Path(coi_path).read_text(encoding="utf-8")).get("flagged", []):
                flagged.add((f["substrate"], f["brand"]))
        log(f"  S7 without COI-flagged units {sorted(flagged)} ...")
        b7 = R.gate_block(ow, STAT, RATING_FLOOR, P, C, excl, excl_units=flagged, boot=False)
        res["S7_without_coi_flagged"] = {"flagged": sorted(flagged), "verdicts": {h: b7[h]["verdict"] for h in b7},
                                         "detail": b7}
        log("  S9 uncentred ranks ...")
        with R.uncentred():
            b9 = R.gate_block(ow, STAT, RATING_FLOOR, P, C, excl, boot=False)
        res["S9_uncentred"] = {"verdicts": {h: b9[h]["verdict"] for h in b9}, "detail": b9}
        log("  S2 rating floors 3 and 10 ...")
        for fl in (3, 10):
            b2 = R.gate_block(ow, STAT, fl, P, C, excl, boot=False)
            res[f"S2_floor_{fl}"] = {"verdicts": {h: b2[h]["verdict"] for h in b2}, "detail": b2}
        res["MQ9_degeneracy"] = {w: degeneracy(R.units_cat_brand(ow[w], RATING_FLOOR)) for w in R.WAVES}
        res["precision_note"] = precision_note()
    for h in ("H1", "H2"):
        log(f"  {h} MODE: " + "  ".join(f"{w} rho={blk[h]['per_wave'][w]['rho']:.4f} n={blk[h]['per_wave'][w]['n']} "
                                         f"p={blk[h]['per_wave'][w]['p_perm']:.4f}" for w in R.WAVES))
    log(f"  H3 MODE: rho={blk['H3']['rho']:.4f} n={blk['H3']['n']} p_perm={blk['H3']['p_perm']:.4f} "
        f"p_shuffle={blk['H3']['p_shuffle']:.4f}")
    log(f"  reproduction of v1.10 S3 (MODE): all identical = {res['reproduction_of_v1_10_S3_MODE']['all_identical']}")
    return res


def run_calibration(log=print, out_file: Path = CAL_FILE) -> dict:
    res = calibration(log=log)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(R._clean(res), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"[v1.14] calibration written: {out_file} (sha256 {sha256_bytes(out_file.read_bytes())[:16]}...)")
    return res


# ===========================================================================
# t4 / t5 INPUTS (section 5.1): read from git refs (real) or a directory (dry run, tests)
# ===========================================================================


class Source:
    """Files of a wave, read either from a git ref of this repository (`git show ref:path`; real runs:
    the acquisition-locked tag) or from a directory (dry runs and tests). Every read is logged with its
    git blob id and SHA-256."""

    def __init__(self, ref: str | None = None, base: Path | None = None, repo: Path = ROOT):
        if (ref is None) == (base is None):
            raise ValueError("Source needs exactly one of ref / base")
        self.ref, self.base, self.repo = ref, (Path(base) if base else None), repo
        self.log = {}

    def exists(self, rel: str) -> bool:
        if self.base is not None:
            return (self.base / rel).exists()
        r = subprocess.run(["git", "-C", str(self.repo), "cat-file", "-e", f"{self.ref}:{rel}"], capture_output=True)
        return r.returncode == 0

    def read_bytes(self, rel: str) -> bytes:
        if self.base is not None:
            p = self.base / rel
            if not p.exists():
                raise Halt(f"missing input: {p}")
            b = p.read_bytes()
        else:
            r = subprocess.run(["git", "-C", str(self.repo), "show", f"{self.ref}:{rel}"], capture_output=True)
            if r.returncode != 0:
                raise Halt(f"cannot read {self.ref}:{rel}: {r.stderr.decode()[:200]}")
            b = r.stdout
        self.log[rel] = {"git_blob": git_blob_bytes(b), "sha256": sha256_bytes(b), "bytes": len(b),
                         "source": f"git:{self.ref}" if self.ref else str(self.base)}
        return b

    def text(self, rel: str) -> str:
        return self.read_bytes(rel).decode("utf-8")

    def blob(self, rel: str) -> str | None:
        return git_blob_bytes(self.read_bytes(rel)) if self.exists(rel) else None


def read_jsonl_text(text: str) -> list[dict]:
    out = []
    for line in text.splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue      # = code_t4_v0_42.read_raw (a torn last line of an append-only file is skipped)
    return out


def is_answered(rec) -> bool:
    """= code_t4_v0_42.is_answered."""
    return rec.get("status") == "ok" and bool((rec.get("text") or "").strip()) and not rec.get("error")


def dedupe_calls(records) -> list[dict]:
    """= code_t4_v0_42.dedupe_calls: one record per call_id, the LAST answered attempt if any, else the
    last attempt."""
    best = {}
    for r in records:
        cid = r["call_id"]
        if cid not in best or is_answered(r) or not is_answered(best[cid]):
            best[cid] = r
    return list(best.values())


def served_ok(requested, served) -> bool:
    """= score_v0_42.served_ok (a dated snapshot of the requested ID is accepted)."""
    s = (served or "").strip().removeprefix("models/")
    return s == requested or re.fullmatch(re.escape(requested) + r"-(\d{4}-\d{2}-\d{2}|\d{8})", s) is not None


def in_design(rec, models=N3) -> bool:
    """= score_v0_42.in_design (r2): N3 models; Phase B in S0/S1, runs 1-3; Phase A in S0, run 1."""
    if rec.get("model_requested") not in models or rec.get("condition") not in CONDS:
        return False
    if rec.get("phase") == "B":
        return rec.get("run") in RUNS
    if rec.get("phase") == "A":
        return (rec.get("condition"), rec.get("run")) == ("S0", 1)
    return False


def excluded_calls(calls, models=N3) -> set:
    """= v1.12 t4_excluded (the shared t4 analysis set): calls outside the design, and answered calls
    served by another model ID (a missing served ID is not excluded)."""
    ex = set()
    for r in calls:
        if not in_design(r, models):
            ex.add(r["call_id"])
        elif is_answered(r) and r.get("served_model") and not served_ok(r["model_requested"], r["served_model"]):
            ex.add(r["call_id"])
    return ex


def phase_b_answers(raw_records, wave: str, models=N3) -> tuple[list[dict], dict]:
    """Phase B calls of a wave in the analysis set -> answers (E0: unanswered = missing cell)."""
    calls = dedupe_calls(raw_records)
    ex = excluded_calls(calls, models)
    out, counts = [], collections.Counter()
    for r in calls:
        if r.get("phase") != "B" or r["call_id"] in ex:
            continue
        sub = SUB_MAP.get(r["substrate"], r["substrate"])
        ans = is_answered(r)
        counts[(sub, r["condition"], "answered" if ans else "missing")] += 1
        # answer_id carries the wave: t4 and t5 repeat the same call_ids, and the retest's shuffle null
        # groups rows by answer (score_v1_10.RankMatrix)
        out.append({"answer_id": f"{wave}::{r['call_id']}", "call_id": r["call_id"], "panel": "N3", "wave": wave,
                    "category": sub,
                    "model": r["model_requested"], "frame": r.get("frame_id") or r["probe_id"],
                    "run_idx": int(r["run"]), "condition": r["condition"],
                    "text": r["text"] if ans else None, "missing_reason": None if ans else (r.get("status") or "missing")})
    out.sort(key=lambda a: a["answer_id"])
    return out, {"excluded_call_ids": sorted(ex), "counts": {"|".join(k): v for k, v in sorted(counts.items())},
                 "calls_after_dedupe": len(calls), "attempt_lines": len(raw_records)}


def extract_wave(answers, registries) -> list[dict]:
    """E0-E7 (v1.10, unchanged) on the URL-stripped visible text (v0.42 section 5.1), both rules.
    registries: {substrate: (registry, unit map)}."""
    pats = {s: R.compile_registry(reg) for s, (reg, _u) in registries.items()}
    infos = []
    for a in answers:
        info = {k: a[k] for k in ("answer_id", "call_id", "panel", "wave", "category", "model", "frame", "run_idx",
                                  "condition")}
        if a["text"] is None:
            info.update(status="missing", named=[], n_named=0, rankable=False, list_structured=False,
                        ranks={r: {} for r in R.RULES})
            infos.append(info)
            continue
        unit = registries[a["category"]][1]
        txt = strip_urls(a["text"])
        try:
            hits = R.find_mentions(R.normalize(txt), pats[a["category"]])
            ranks, ls = {}, False
            for rule in R.RULES:
                res = R.rank_answer(txt, pats[a["category"]], rule)
                ranks[rule] = {unit[b]: v for b, v in res["ranks"].items()}
                if rule == "lead_item":
                    ls = res["list_structured"]
        except Exception as e:  # MQ1: an exception halts
            raise Halt(f"MQ1: extractor failed on {a['answer_id']}: {type(e).__name__}: {e}")
        info.update(status="ok", named=sorted(unit[b] for b in hits), n_named=len(hits),
                    rankable=len(hits) >= R.MIN_NAMED_RANKABLE, list_structured=ls, ranks=ranks)
        infos.append(info)
    return infos


def wave_rows(infos, rule="lead_item", condition="S0", models=None) -> list[dict]:
    """Rankable (answer, brand) rows: the input of every rank statistic (= score_v1_10.rank_rows)."""
    out = []
    for i in infos:
        if i["status"] != "ok" or not i["rankable"] or i["condition"] != condition:
            continue
        if models is not None and i["model"] not in models:
            continue
        for b, (km, kn) in i["ranks"][rule].items():
            out.append({"panel": i["panel"], "wave": i["wave"], "category": i["category"], "answer_id": i["answer_id"],
                        "model": i["model"], "run_idx": i["run_idx"], "brand": b, "k_mid": km, "k_min": kn,
                        "n": i["n_named"]})
    return out


RANK_COLS = ["answer_id", "wave", "condition", "category", "model", "frame", "run_idx", "status", "n_named",
             "rankable", "list_structured", "rule", "brand", "k_mid", "k_min"]


def rank_table_bytes(infos) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(RANK_COLS)
    for i in infos:
        base = [i["answer_id"], i["wave"], i["condition"], i["category"], i["model"], i["frame"], i["run_idx"],
                i["status"], i["n_named"], int(i["rankable"]), int(i["list_structured"])]
        if i["status"] != "ok":
            w.writerow(base + ["", "", "", ""])
            continue
        for rule in R.RULES:
            if not i["named"]:
                w.writerow(base + [rule, "", "", ""])
            for b in i["named"]:
                kv = i["ranks"][rule].get(b)
                w.writerow(base + [rule, b] + (["", ""] if kv is None else [repr(float(kv[0])), kv[1]]))
    return buf.getvalue().encode("utf-8")


def load_registries_v110() -> dict:
    """The five omnibus registries exactly as v1.10 loads them (files pinned in v1.10's input manifest,
    verified before use)."""
    bad = R.verify_manifest()
    if bad:
        raise Halt("v1.10 input manifest verification failed: " + "; ".join(bad[:5]))
    ctx = R.Ctx()
    return {sub: R.load_registry(ctx, rel, fmt)[:2] for sub, (rel, fmt) in R.OMNI_REG.items()}


# ===========================================================================
# PRESENCE AND CONSISTENCY AT t4 (section 5.2): the definition shared with v1.12 and v1.13
# ===========================================================================


def _num(v):
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if math.isfinite(f) else None


def read_coded(src: Source, coded_dir: str = T4_FILES["coded_dir"]) -> tuple[list, list]:
    """v0.42's coded tables ({v19..v23}_phase_{a,b}.csv), ints restored (= v1.12 read_t4_coded)."""
    A, B = [], []
    for raw in SUB_MAP:
        for ph, acc in (("a", A), ("b", B)):
            rel = f"{coded_dir}/{raw}_phase_{ph}.csv"
            if not src.exists(rel):
                continue
            for r in csv.DictReader(io.StringIO(src.text(rel))):
                r["run"] = int(r["run"])
                if ph == "a":
                    r["recognized"] = None if r["recognized"] in ("", None) else int(r["recognized"])
                else:
                    r["mentioned"] = int(r["mentioned"])
                acc.append(r)
    return A, B


def comparators(brand_table, coded_a, coded_b, excluded, cond="S0", models=N3) -> dict:
    """P and C* at t4 in condition `cond` (v1.12 section 2.6 = v1.13 section 2.1; one shared definition):
    P = 100 (C_P/3 + 2 pi_hat_cond) / 3, C_P/3 = share of N3 models coding b as recognized in their one S0
    Phase A answer (models without a coded answer leave the denominator; none coded -> P not computed);
    C* = 100 (1 - phi_cond / 9) if v0.42's partition is 'defined', 100 if 'saturated', NOT RATED if 'zero'
    or 'undefined'; rated only with >= 6 N3 Phase B mentions in `cond`."""
    pi, phi = {}, {}
    for r in brand_table:
        u = (r["substrate"], r["brand"])
        pi[u] = _num(r.get(f"pi_N3_{cond}"))
        part = (r.get(f"phi_partition_N3_{cond}") or "").strip()
        v = _num(r.get(f"phi_N3_{cond}"))
        phi[u] = v if (part == "defined" and v is not None) else (0.0 if part == "saturated" else None)
    rec = collections.defaultdict(lambda: [0, 0])
    for r in coded_a:
        if r["condition"] != "S0" or r["model"] not in models or r["call_id"] in excluded or r["recognized"] is None:
            continue
        t = rec[(r["substrate"], r["brand"])]
        t[0] += int(r["recognized"])
        t[1] += 1
    ment = collections.Counter()
    for r in coded_b:
        if r["condition"] == cond and r["model"] in models and r["call_id"] not in excluded and r["run"] in RUNS:
            ment[(r["substrate"], r["brand"])] += int(r["mentioned"])
    P, C = {}, {}
    for u in pi:
        n_rec = rec[u][1] if u in rec else 0
        P[u] = 100.0 * (rec[u][0] / n_rec + 2.0 * pi[u]) / 3.0 if (pi[u] is not None and n_rec) else None
        C[u] = (100.0 * (1.0 - phi[u] / C_STAR_DIVISOR)
                if (phi[u] is not None and ment[u] >= C_STAR_MIN_MENTIONS) else None)
    return {"P": P, "C": C, "pi_hat": pi, "mentions": {u: int(ment[u]) for u in pi}}


def phi_m_reduced(k):
    """v0.41 phi_m on a reduced panel (= v1.12 phi_m_reduced): (phi or None, pi, partition)."""
    k = np.asarray(k, float)
    m = len(k)
    pi = float(k.sum() / (m * FRAMES_PER_SUB))
    if pi <= 0.0:
        return None, pi, "zero"
    if pi >= 1.0:
        return None, pi, "saturated"
    return float(((k - FRAMES_PER_SUB * pi) ** 2).sum() / (FRAMES_PER_SUB * pi * (1.0 - pi)) / (m - 1)), pi, "defined"


def comparator_parity(brand_table, coded_b, excluded, cond="S0", models=N3) -> dict:
    """MQ8: pi_hat and phi (partition) recomputed from v0.42's coded Phase B table equal the brand table's
    pi_N3_cond / phi_N3_cond / phi_partition_N3_cond exactly (v1.12's P2)."""
    k, ans = collections.defaultdict(int), collections.defaultdict(set)
    for r in coded_b:
        if r["call_id"] in excluded or r["condition"] != cond:
            continue
        ans[(r["model"], r["run"], r["substrate"])].add(r["call_id"])
        k[(r["model"], r["run"], r["substrate"], r["brand"])] += int(r["mentioned"])
    bad = []
    for row in brand_table:
        s, b = row["substrate"], row["brand"]
        num = sum(k.get((m, r, s, b), 0) for m in models for r in RUNS)
        den = sum(len(ans.get((m, r, s), ())) for m in models for r in RUNS)
        pi = num / den if den else None
        runs = []
        for r in RUNS:
            if any(len(ans.get((m, r, s), ())) != FRAMES_PER_SUB for m in models):
                runs.append((None, "missing"))
                continue
            ph, _p, part = phi_m_reduced([k.get((m, r, s, b), 0) for m in models])
            runs.append((ph, part))
        vals = [p for p, part in runs if part == "defined"]
        parts = [part for _, part in runs]
        if len(vals) >= 2:
            phi, part = float(np.mean(vals)), "defined"
        elif parts and all(p == "zero" for p in parts):
            phi, part = None, "zero"
        elif parts and all(p == "saturated" for p in parts):
            phi, part = None, "saturated"
        else:
            phi, part = None, "undefined"
        tab = (_num(row.get(f"pi_N3_{cond}")), _num(row.get(f"phi_N3_{cond}")),
               (row.get(f"phi_partition_N3_{cond}") or "").strip())
        if tab != (pi, phi, part):
            bad.append({"unit": [s, b], "table": list(tab), "recomputed": [pi, phi, part]})
    return {"condition": cond, "units": len(brand_table), "mismatches": len(bad), "examples": bad[:10],
            "passes": bool(brand_table) and not bad}


# ===========================================================================
# STAGE 1 ANALYSIS (section 5): t4 separability, once
# ===========================================================================


def mq2_parity_t4(infos, coded_b, excluded) -> dict:
    """MQ2 at t4: the extractor's named set (URL-stripped text) against v0.42's certified coded Phase B
    table, cell by cell (answer x registry brand). v0.20-v0.22 must agree on 100% of cells (else halt);
    v0.19 / v0.23 at >= 0.98 (else that substrate leaves the gate legs; deviation entry), as in v1.10."""
    named = {i["call_id"]: set(i["named"]) for i in infos if i["status"] == "ok"}
    per = collections.defaultdict(lambda: [0, 0])
    dis = collections.defaultdict(list)
    for r in coded_b:
        aid = r["call_id"]
        if aid in excluded or aid not in named:
            continue
        ext = r["brand"] in named[aid]
        per[r["substrate"]][0] += 1
        per[r["substrate"]][1] += int(ext == bool(r["mentioned"]))
        if ext != bool(r["mentioned"]):
            dis[r["substrate"]].append({"answer_id": aid, "brand": r["brand"], "coded": r["mentioned"], "extractor": ext})
    coded_ids = {r["call_id"] for r in coded_b}
    answered_uncoded = sorted(a for a in named if a not in coded_ids)
    out = {"per_substrate": {}, "halt": [], "excluded_from_gate": [], "answers_without_coded_rows": answered_uncoded}
    if answered_uncoded:
        out["halt"].append(f"{len(answered_uncoded)} answered Phase B calls have no coded row")
    for sub in SUB_MAP.values():
        cells, agree = per[sub]
        req = 1.0 if sub in ("v0.20", "v0.21", "v0.22") else R.PARITY_FLOOR_CODED
        share = agree / cells if cells else float("nan")
        ok = bool(cells) and share >= req
        out["per_substrate"][sub] = {"cells": cells, "agree": agree, "agreement": share, "required": req,
                                     "passes": ok, "disagreements": dis[sub][:50]}
        if not ok and req == 1.0:
            out["halt"].append(sub)
        elif not ok:
            out["excluded_from_gate"].append(sub)
    return out


def join_units(registries, brand_table, expected: int = R.N_BRAND_UNITS) -> dict:
    """The 112 registry units of v1.10 and the rows of v0.42's brand table must match 1:1."""
    reg_units = {(s, u) for s, (_r, unit) in registries.items() for u in unit.values()}
    tab = collections.Counter((r["substrate"], r["brand"]) for r in brand_table)
    dup = sorted(k for k, c in tab.items() if c > 1)
    return {"registry_units": len(reg_units), "table_units": len(tab), "matched": len(reg_units & set(tab)),
            "only_in_registries": sorted(reg_units - set(tab)), "only_in_table": sorted(set(tab) - reg_units),
            "duplicates": dup, "one_to_one": not dup and reg_units == set(tab) and len(reg_units) == expected}


def single_wave_sep(U, Y, stat, seed, excl_sub=(), excl_units=(), boot=True) -> dict:
    """rho_w(R*, Y) on one wave; units with R* rated and Y defined; categories with >= 5 units;
    verdict on the single estimate (v1.10's bands; UNDETERMINED below 30 units)."""
    keys = sorted(k for k, s in U.items() if s["rated"] and k[0] not in excl_sub and k not in excl_units
                  and Y.get(k) is not None and math.isfinite(Y[k]))
    res = R.corr_test([Y[k] for k in keys], [U[k][stat] for k in keys], [k[0] for k in keys], seed, "two", boot=boot)
    res["verdict"] = R.verdict_single_separability(res["rho"], res["n"])
    return res


def penalised_mnp(infos, P, condition="S0") -> dict:
    """MQ6 positive control (v1.10): penalised MNP over all answers with text (unnamed brand q = 1,
    named alone q = 0) must reach |rho_w| >= .50 with P; else the gate's sensitivity is flagged."""
    by_sub = collections.defaultdict(list)
    for i in infos:
        if i["status"] == "ok" and i["condition"] == condition:
            by_sub[i["category"]].append(i)
    x, y, g = [], [], []
    for (s, b) in sorted(k for k in P if P[k] is not None):
        T = by_sub.get(s, [])
        if not T:
            continue
        qs = []
        for i in T:
            if b not in i["named"]:
                qs.append(1.0)
            elif i["rankable"]:
                qs.append((i["ranks"]["lead_item"][b][0] - 1.0) / (i["n_named"] - 1.0))
            else:
                qs.append(0.0)
        x.append(P[(s, b)])
        y.append(100.0 * (1.0 - float(np.mean(qs))))
        g.append(s)
    res = R._rho_only(x, y, g)
    res["passes"] = bool(np.isfinite(res["rho"]) and abs(res["rho"]) >= R.POS_CONTROL_MIN)
    res["flag_gate_sensitivity"] = not res["passes"]
    return res


def run_reliability(rows, stat=STAT, floor=RUN_FLOOR, n_draws=0, seed=None) -> dict:
    """D2 / MQ7 at t4: R*_r per run (rated iff >= `floor` rankable mentions in that run); for each run
    pair, rho_w over units rated in both (categories with >= 5 units); rel1 = mean over pairs with >= 30
    units; rel3 = 3 rel1 / (1 + 2 rel1). With n_draws > 0 the same is computed under the within-answer
    order shuffle (MQ7: mean rel3 must stay below 0.20)."""
    RM = R.RankMatrix(rows, unit_of=lambda r: (int(r["run_idx"]), r["category"], r["brand"]))
    pairs = []
    for a, b in ((1, 2), (1, 3), (2, 3)):
        keys = sorted({u[1:] for u in RM.units if u[0] == a} & {u[1:] for u in RM.units if u[0] == b})
        keys = [k for k in keys if RM.count[RM.uidx[(a,) + k]] >= floor and RM.count[RM.uidx[(b,) + k]] >= floor]
        g = np.array([k[0] for k in keys])
        m = R.keep_categories(g) if len(g) else np.zeros(0, bool)
        keys = [k for k, ok in zip(keys, m) if ok]
        ia = np.array([RM.uidx[(a,) + k] for k in keys], np.int64)
        ib = np.array([RM.uidx[(b,) + k] for k in keys], np.int64)
        pairs.append(((a, b), ia, ib, R._group_index(g[m]) if len(g) else []))

    def rel(v):
        rhos = {}
        for (ab, ia, ib, gidx) in pairs:
            rhos[f"{ab[0]}-{ab[1]}"] = (R._pearson(R._within_ranks_idx(v[ia], gidx), R._within_ranks_idx(v[ib], gidx))
                                        if len(ia) >= 3 else float("nan"), int(len(ia)))
        ok = [r for r, n in rhos.values() if n >= N_FLOOR_UNITS and np.isfinite(r)]
        r1 = float(np.mean(ok)) if ok else float("nan")
        return r1, (3 * r1 / (1 + 2 * r1) if np.isfinite(r1) and r1 > -0.5 else float("nan")), rhos
    r1, r3, rhos = rel(RM.stat(stat))
    out = {"statistic": stat, "floor_per_run": floor, "pairs": {k: {"rho": v[0], "n": v[1]} for k, v in rhos.items()},
           "rel1": r1, "rel3": r3, "pairs_used": sum(1 for v in rhos.values() if v[1] >= N_FLOOR_UNITS)}
    if n_draws:
        rng = np.random.default_rng(SEEDS["MQ7"] if seed is None else seed)
        vals = []
        for _ in range(n_draws):
            km, kn = RM.shuffled(rng)
            vals.append(rel(RM.stat(stat, km, kn))[1])
        mean = float(np.nanmean(vals)) if np.isfinite(vals).any() else float("nan")
        out.update(shuffle_draws=n_draws, shuffle_seed=SEEDS["MQ7"] if seed is None else seed,
                   shuffled_mean_rel3=mean, threshold=R.NEG_CONTROL_MAX,
                   flag_list_composition_driven=bool(np.isfinite(mean) and mean >= R.NEG_CONTROL_MAX))
    return out


VERDICTS = ("CONFIRMED", "MARGINAL", "FALSIFIED", "UNDETERMINED")


def stage1_verdict(h1: str, h2: str, comps: dict, h4_s1: str | None) -> str:
    """Interim verdict after Stage 1 (section 8): separability legs only."""
    legs = [h1, h2] + [v for v in comps.values() if v in VERDICTS]
    if "FALSIFIED" in legs:
        return "FAIL"
    if "UNDETERMINED" in legs:
        return "UNDETERMINED"
    if all(v == "CONFIRMED" for v in legs):
        return "MARGINAL" if h4_s1 == "FALSIFIED" else "SEPARABLE (Stage 2 pending)"
    return "MARGINAL"


def final_gate(h1: str, h2: str, h3: str, comps: dict, h4_s1: str | None) -> str:
    """GATE (section 8) = v1.10's rule with the t4/t5 legs: FAIL if any gate leg FALSIFIED; else
    UNDETERMINED if any UNDETERMINED; else PASS if all CONFIRMED (MARGINAL if the S1 replication leg is
    FALSIFIED); else MARGINAL. Active component legs not yet computed are listed, never assumed."""
    legs = [h1, h2, h3] + [v for v in comps.values() if v in VERDICTS]
    if "FALSIFIED" in legs:
        return "FAIL"
    if "UNDETERMINED" in legs:
        return "UNDETERMINED"
    if all(v == "CONFIRMED" for v in legs):
        return "MARGINAL" if h4_s1 == "FALSIFIED" else "PASS"
    return "MARGINAL"


def _models_dropped(v042_verdicts: dict, cond: str) -> list:
    """N3 models v0.42's drop rule excludes in `cond` (= v1.12 choose_comparators)."""
    out = []
    for x in (v042_verdicts or {}).get("models_excluded_condition", []):
        parts = str(x).split("|")
        if parts[0] in N3 and parts[-1] == cond:
            out.append(parts[0])
    return out


def _dist(v):
    v = [x for x in v if x is not None and np.isfinite(x)]
    if not v:
        return None
    a = np.asarray(v, float)
    return {"median": float(np.median(a)), "q25": float(np.quantile(a, .25)), "q75": float(np.quantile(a, .75)),
            "min": float(a.min()), "max": float(a.max()), "n": int(len(a))}


def descriptives(infos, U0, U1) -> dict:
    out = {"per_substrate_condition": {}, "per_model_condition": {}}
    for cond in CONDS:
        for sub in SUB_MAP.values():
            I = [i for i in infos if i["category"] == sub and i["condition"] == cond]
            T = [i for i in I if i["status"] == "ok"]
            Rk = [i for i in T if i["rankable"]]
            U = U0 if cond == "S0" else U1
            rated = [s[STAT] for (c, b), s in U.items() if c == sub and s["rated"]]
            out["per_substrate_condition"][f"{sub}|{cond}"] = {
                "answers": len(I), "expected": EXPECTED_B_PER_SUB_COND, "missing": len(I) - len(T),
                "rankable_share": len(Rk) / len(T) if T else None,
                "list_structured_share": sum(i["list_structured"] for i in T) / len(T) if T else None,
                "brands_named_per_rankable_answer": _dist([i["n_named"] for i in Rk]),
                "units_rated": len(rated), "R_star_distribution": _dist(rated),
                "R_star_value_counts": dict(collections.Counter(str(int(v)) for v in rated))}
        for m in N3:
            T = [i for i in infos if i["model"] == m and i["condition"] == cond and i["status"] == "ok"]
            Rk = [i for i in T if i["rankable"]]
            out["per_model_condition"][f"{m}|{cond}"] = {
                "answers_with_text": len(T), "rankable": len(Rk),
                "mean_list_length": float(np.mean([i["n_named"] for i in Rk])) if Rk else None,
                "list_structured_share": sum(i["list_structured"] for i in T) / len(T) if T else None}
    return out


def stage1_core(raw_records, brand_table, coded_a, coded_b, v042_verdicts, registries, activation=None,
                components=None, log=print, boot=True, shuffle_draws=None, expected_units=R.N_BRAND_UNITS) -> dict:
    """Section 5. Everything Stage 1 computes, from v0.42's locked files and v1.10's registries."""
    activation, components = activation or {}, components or {}
    answers, meta = phase_b_answers(raw_records, "t4")
    infos = extract_wave(answers, registries)                                       # MQ1 halts on exception
    join = join_units(registries, brand_table, expected_units)
    if not join["one_to_one"]:
        raise Halt(f"unit join: registry units and v0.42's brand table differ: {join}")
    excluded = set(meta["excluded_call_ids"])
    mq2 = mq2_parity_t4(infos, coded_b, excluded)
    if mq2["halt"]:
        raise Halt(f"MQ2: extractor named set != v0.42 coded table on {mq2['halt']}")
    mq8 = {c: comparator_parity(brand_table, coded_b, excluded, c) for c in CONDS}
    if not all(v["passes"] for v in mq8.values()):
        raise Halt(f"MQ8: v0.42's brand table does not match its coded table: "
                   f"{ {c: v['mismatches'] for c, v in mq8.items()} }")
    comp = {c: comparators(brand_table, coded_a, coded_b, excluded, c) for c in CONDS}
    dropped = {c: _models_dropped(v042_verdicts, c) for c in CONDS}
    excl_sub = tuple(mq2["excluded_from_gate"])
    rows = {c: wave_rows(infos, "lead_item", c) for c in CONDS}
    U = {c: unit_scores(rows[c]) for c in CONDS}
    log(f"[v1.14] Stage 1: {len(answers)} Phase B answers in the analysis set; rankable rows "
        + ", ".join(f"{c} {len(rows[c])}" for c in CONDS) + f"; units rated (S0) "
        f"{sum(s['rated'] for s in U['S0'].values())}")
    res = {"statistic": STAT, "rating_floor": RATING_FLOOR, "analysis_set": meta, "unit_join": join,
           "MQ2_mention_parity": mq2, "MQ8_comparator_parity": mq8, "models_dropped_by_v0_42": dropped,
           "gate_excluded_substrates": list(excl_sub)}
    h1 = single_wave_sep(U["S0"], comp["S0"]["P"], STAT, SEEDS["H1"], excl_sub, boot=boot)
    h2 = single_wave_sep(U["S0"], comp["S0"]["C"], STAT, SEEDS["H2"], excl_sub, boot=boot)
    if dropped["S0"]:
        for h in (h1, h2):
            h["verdict"] = "UNDETERMINED"
            h["reason"] = f"N3 model(s) excluded by v0.42's drop rule in S0: {dropped['S0']}"
    mq9 = degeneracy(U["S0"])
    res["MQ9_degeneracy"] = mq9
    if mq9["flag_degenerate"]:
        for h in (h1, h2):
            h["verdict"] = "UNDETERMINED"
            h["reason"] = (h.get("reason", "") + "; " if h.get("reason") else "") + "MQ9: R* degenerate at t4"
    h4 = single_wave_sep(U["S1"], comp["S1"]["P"], STAT, SEEDS["H4_S1"], excl_sub, boot=boot)
    if dropped["S1"]:
        h4["note"] = f"reduced S1 panel: v0.42 drop rule excluded {dropped['S1']} (scored on the answers kept)"
    res.update(H1_Sep_Presence=h1, H2_Sep_Consistency=h2, H4_Sep_Presence_S1=h4)
    comp_res, comp_v = {}, {}
    for name in COMPONENTS:
        act = bool(activation.get(name, {}).get("active"))
        if not act:
            comp_res[name], comp_v[name] = {"verdict": "INACTIVE", "activation": activation.get(name)}, "INACTIVE"
        elif name not in components:
            comp_res[name], comp_v[name] = {"verdict": "PENDING", "activation": activation.get(name),
                                            "note": "active; the component's locked score does not exist yet"}, "PENDING"
        else:
            r = single_wave_sep(U["S0"], components[name]["values"], STAT, SEEDS[f"COMP_{name}"], excl_sub, boot=boot)
            r.update(activation=activation.get(name), score_file=components[name].get("file"),
                     score_sha256=components[name].get("sha256"))
            if mq9["flag_degenerate"]:
                r["verdict"], r["reason"] = "UNDETERMINED", "MQ9: R* degenerate at t4"
            comp_res[name], comp_v[name] = r, r["verdict"]
    res["H_Sep_Components"] = comp_res
    res["MQ6_positive_control"] = penalised_mnp(infos, comp["S0"]["P"])
    log("  run reliability and MQ7 (2,000 within-answer shuffles) ...")
    res["D2_run_reliability_and_MQ7"] = run_reliability(rows["S0"], n_draws=R.N_SHUFFLE_MQ7 if shuffle_draws is None
                                                        else shuffle_draws)
    sens = {}
    fm = unit_scores(wave_rows(infos, "first_mention", "S0"))
    sens["S1_first_mention"] = {h: single_wave_sep(fm, comp["S0"][y], STAT, SEEDS[h], excl_sub, boot=False)
                                for h, y in (("H1", "P"), ("H2", "C"))}
    for fl in (3, 10):
        Uf = unit_scores(rows["S0"], fl)
        sens[f"S2_floor_{fl}"] = {h: single_wave_sep(Uf, comp["S0"][y], STAT, SEEDS[h], excl_sub, boot=False)
                                  for h, y in (("H1", "P"), ("H2", "C"))}
    for s in R.CANDIDATES:
        sens[f"S3_candidate_{s}"] = {h: single_wave_sep(U["S0"], comp["S0"][y], s, SEEDS[h], excl_sub, boot=False)
                                     for h, y in (("H1", "P"), ("H2", "C"))}
    for sub in SUB_MAP.values():
        sens[f"S4_leave_out_{sub}"] = {h: single_wave_sep(U["S0"], comp["S0"][y], STAT, SEEDS[h],
                                                          tuple(set(excl_sub) | {sub}), boot=False)
                                       for h, y in (("H1", "P"), ("H2", "C"))}
    keys = sorted(k for k, s in U["S0"].items() if s["rated"] and k[0] not in excl_sub)
    sens["S5_recall_arm"] = {
        "rho_R_pi_hat": R._rho_only([comp["S0"]["pi_hat"].get(k) if comp["S0"]["pi_hat"].get(k) is not None
                                     else float("nan") for k in keys], [U["S0"][k][STAT] for k in keys],
                                    [k[0] for k in keys]),
        "rho_R_mentions": R._rho_only([comp["S0"]["mentions"].get(k, float("nan")) for k in keys],
                                      [U["S0"][k][STAT] for k in keys], [k[0] for k in keys])}
    sens["S7_without_Denon"] = {h: single_wave_sep(U["S0"], comp["S0"][y], STAT, SEEDS[h], excl_sub, (DENON,),
                                                   boot=False) for h, y in (("H1", "P"), ("H2", "C"))}
    with R.uncentred():
        sens["S9_uncentred"] = {h: single_wave_sep(U["S0"], comp["S0"][y], STAT, SEEDS[h], excl_sub, boot=False)
                                for h, y in (("H1", "P"), ("H2", "C"))}
    res["sensitivities"] = sens
    res["verdict_changes_under_sensitivities"] = [
        {"sensitivity": n, "hypothesis": h, "primary": res[f"{h}_Sep_{'Presence' if h == 'H1' else 'Consistency'}"]["verdict"],
         "under_sensitivity": v["verdict"]}
        for n, blk in sens.items() if isinstance(blk, dict) and "H1" in blk for h, v in blk.items()
        if v["verdict"] != res[f"{h}_Sep_{'Presence' if h == 'H1' else 'Consistency'}"]["verdict"]]
    both = sorted(k for k in U["S0"] if U["S0"][k]["rated"] and k in U["S1"] and U["S1"][k]["rated"])
    res["D1_descriptives"] = descriptives(infos, U["S0"], U["S1"])
    res["D3_R_S0_vs_R_S1"] = R._rho_only([U["S0"][k][STAT] for k in both], [U["S1"][k][STAT] for k in both],
                                         [k[0] for k in both])
    res["D4_MODE_vs_MNP_S0"] = R._rho_only([U["S0"][k]["MNP"] for k in keys], [U["S0"][k][STAT] for k in keys],
                                           [k[0] for k in keys])
    res["STAGE1_VERDICT"] = stage1_verdict(h1["verdict"], h2["verdict"], comp_v, h4["verdict"])
    res["component_legs"] = comp_v
    res["units"] = [{"substrate": k[0], "brand": k[1], "n_ranked_S0": U["S0"][k]["n_ranked"],
                     "rated_S0": U["S0"][k]["rated"], "R_star_S0": U["S0"][k][STAT],
                     "n_ranked_S1": U["S1"].get(k, {}).get("n_ranked", 0),
                     "R_star_S1": U["S1"].get(k, {}).get(STAT), "P_S0": comp["S0"]["P"].get(k),
                     "C_star_S0": comp["S0"]["C"].get(k), "P_S1": comp["S1"]["P"].get(k)}
                    for k in sorted(set(U["S0"]) | set(U["S1"]))]
    res["_infos"] = infos
    log(f"  H1 rho={h1['rho']:.4f} n={h1['n']} -> {h1['verdict']};  H2 rho={h2['rho']:.4f} n={h2['n']} -> "
        f"{h2['verdict']};  H4(S1) rho={h4['rho']:.4f} -> {h4['verdict']};  components {comp_v}")
    log(f"  STAGE 1: {res['STAGE1_VERDICT']}")
    return res


# ===========================================================================
# STAGE 2 (section 6): t4 -> t5 retest reliability
# ===========================================================================


def retained_models(infos, models, share=0.90, per_model=len(RUNS) * 30) -> list:
    """A model enters the retest iff >= 90% of its S0 Phase B calls in the wave are answered."""
    cnt = collections.Counter(i["model"] for i in infos if i["condition"] == "S0" and i["status"] == "ok")
    return [m for m in models if cnt[m] >= share * per_model]


def probe_parity(t4_probes_text: str, t5_probes_text: str) -> dict:
    """t5 must repeat t4's 30 category questions verbatim (substrate, probe_id, frame, prompt, system)."""
    def b(text):
        return sorted((p["substrate"], p["probe_id"], p.get("frame_id"), p["prompt"], p.get("system"))
                      for p in read_jsonl_text(text) if p.get("phase") == "B")
    a, c = b(t4_probes_text), b(t5_probes_text)
    return {"t4_phase_b": len(a), "t5_phase_b": len(c), "identical": a == c and len(a) == 30}


def stage2_core(t4_infos, t5_raw, registries, t4_models, log=print, boot=True) -> dict:
    t5_answers, meta5 = phase_b_answers(t5_raw, "t5")
    t5_infos = extract_wave(t5_answers, registries)
    models = [m for m in retained_models(t5_infos, t4_models)]
    res = {"t5_analysis_set": meta5, "models_t4": t4_models, "models_in_retest": models}
    rows4 = wave_rows(t4_infos, "lead_item", "S0", models)
    rows5 = wave_rows(t5_infos, "lead_item", "S0", models)
    if len(models) < 2:
        h3 = {"verdict": "UNDETERMINED", "reason": f"fewer than 2 N3 models answered in both waves: {models}"}
    else:
        h3 = R.stability(rows4, rows5, STAT, RATING_FLOOR, SEEDS["H3"], boot=boot)
        if len(models) < len(N3):
            h3["note"] = f"reduced panel: {models}"
    res["H3_Retest_Reliability"] = h3
    res["descriptive_S1_retest"] = R.stability(wave_rows(t4_infos, "lead_item", "S1", models),
                                               wave_rows(t5_infos, "lead_item", "S1", models), STAT,
                                               RATING_FLOOR, None, nulls=False) if len(models) >= 2 else None
    res["descriptive_MNP_retest"] = R.stability(rows4, rows5, "MNP", RATING_FLOOR, None, nulls=False) \
        if len(models) >= 2 else None
    res["_t5_infos"] = t5_infos
    log(f"  H3 (t4 -> t5): {h3.get('verdict')}  rho={h3.get('rho')} n={h3.get('n')}")
    return res


# ===========================================================================
# ORDER OF OPERATIONS AND REFUSALS (section 9)
# ===========================================================================
LOCKED_FILES = [
    V114 + "/prereg/PRE_REGISTRATION_v1_14.md",
    V114 + "/README.md",
    V114 + "/anchor/DEVIATIONS.md",
    V114 + "/calibration/calibration_v1_14.json",
    "scripts/score_v1_14.py",
    "scripts/test_score_v1_14.py",
    "scripts/score_v1_10.py",
    V110 + "/registries/INPUTS_MANIFEST_v1_10.json",
    *[rel for rel, _f in R.OMNI_REG.values()],
    V110 + "/outputs/v1_10_verdicts.json",
    V110 + "/anchor/coi_flags_v1_10.json",
    R.PROFILES_REL,
]


def tag_exists(tag: str) -> bool:
    return R._tag_exists(tag, ROOT)


def lock_manifest_text(files=LOCKED_FILES, root: Path = ROOT) -> str:
    return "".join(f"{sha256_bytes((root / f).read_bytes())}  {f}\n" for f in files)


def verify_lock_manifest(path: Path = LOCK_MANIFEST, root: Path = ROOT) -> list[str]:
    if not path.exists():
        return [f"lock manifest missing: {path}"]
    bad = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        h, f = line.split("  ", 1)
        p = root / f
        if not p.exists() or sha256_bytes(p.read_bytes()) != h:
            bad.append(f"changed since the lock: {f}")
    return bad


def lock_status(anchor: Path = ANCHOR_FILE) -> tuple[bool, list[str]]:
    """Stage 1 and Stage 2 on real data need: tag v1.14-prereg-r1, the anchor file (written after the push
    and the OSF deposit), tag v0.42-acquisition-locked, and every locked file unchanged."""
    why = []
    if not tag_exists(PREREG_TAG):
        why.append(f"git tag {PREREG_TAG} does not exist")
    if not Path(anchor).exists():
        why.append(f"anchor file {anchor} does not exist")
    if not tag_exists(V042_ACQ_TAG):
        why.append(f"git tag {V042_ACQ_TAG} does not exist (t4 not acquisition-locked)")
    if not why:
        why += verify_lock_manifest()
    return (not why), why


COMPONENT_TAGS = {"Coverage": "v1.12-prereg-r", "Grounding": "v1.13-prereg-r", "Sentiment": "v1.11-prereg-r"}


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise Halt(f"git {' '.join(args)} failed: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def write_anchor(osf_note: str = "", anchor: Path = ANCHOR_FILE) -> dict:
    """Section 0 / 5.4: written right after the tag is pushed and before Stage 1. Records the tag object,
    commit, tree, remote ref, the SHA-256 and git blob of every locked file, and the activation of the
    component legs (a leg is active iff that component's pre-registration tag is on origin now, i.e. before
    the v1.14 lock commit was anchored, and its score is defined on the N3 panel at t4; the Sentiment
    leg is inactive: v1.11's locked score is defined on the archived waves only)."""
    if anchor.exists():
        raise Halt(f"anchor already written: {anchor}")
    bad = verify_lock_manifest()
    if bad:
        raise Halt("lock manifest does not verify: " + "; ".join(bad))
    remote = _git("ls-remote", "--tags", "origin", PREREG_TAG)
    if f"refs/tags/{PREREG_TAG}" not in remote:
        raise Halt(f"tag {PREREG_TAG} is not on origin")
    commit = _git("rev-parse", f"{PREREG_TAG}^{{commit}}")
    if _git("rev-parse", "HEAD") != commit:
        raise Halt("HEAD is not the tagged commit")
    remote_tags = _git("ls-remote", "--tags", "origin")
    act = {}
    for name, prefix in COMPONENT_TAGS.items():
        tags = sorted({ln.split("refs/tags/")[1].removesuffix("^{}") for ln in remote_tags.splitlines()
                       if f"refs/tags/{prefix}" in ln})
        defined_on_t4 = name != "Sentiment"
        act[name] = {"tags_on_origin": tags, "latest": tags[-1] if tags else None,
                     "commit": _git("rev-parse", f"{tags[-1]}^{{commit}}") if tags else None,
                     "score_defined_on_N3_at_t4": defined_on_t4, "active": bool(tags) and defined_on_t4}
    files = {}
    for line in LOCK_MANIFEST.read_text().splitlines():
        h, f = line.split("  ", 1)
        files[f] = {"sha256": h, "git_blob": git_blob_bytes((ROOT / f).read_bytes())}
    doc = {"tag": PREREG_TAG, "tag_object": _git("rev-parse", PREREG_TAG), "commit": commit,
           "tree": _git("rev-parse", f"{commit}^{{tree}}"), "branch": "v1.14",
           "tagger_date": _git("for-each-ref", f"refs/tags/{PREREG_TAG}", "--format=%(taggerdate:iso-strict)"),
           "remote_tag_ref": remote.splitlines()[0], "recorded_utc": _now(),
           "repository": "https://github.com/thirdsystem-aias/aias", "osf_deposit": osf_note,
           "lock_manifest_sha256": sha256_bytes(LOCK_MANIFEST.read_bytes()), "locked_files": files,
           "activation": act}
    _write_json(anchor, doc)
    return doc


def read_components(specs) -> dict:
    """--component NAME=path.csv (columns substrate, brand, value): a component's locked score per unit."""
    out = {}
    for s in specs or []:
        name, path = s.split("=", 1)
        if name not in COMPONENTS:
            raise Halt(f"unknown component {name}")
        p = Path(path)
        vals = {(r["substrate"], r["brand"]): _num(r.get("value")) for r in csv.DictReader(open(p, encoding="utf-8"))}
        out[name] = {"values": vals, "file": str(p), "sha256": sha256_bytes(p.read_bytes())}
    return out


def _write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(R._clean(obj), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_t4(src_raw: Source, src_scored: Source):
    raw = read_jsonl_text(src_raw.text(T4_FILES["raw"]))
    brand_table = list(csv.DictReader(io.StringIO(src_scored.text(T4_FILES["brand_table"]))))
    coded_a, coded_b = read_coded(src_scored)
    verdicts = json.loads(src_scored.text(T4_FILES["verdicts"]))
    return raw, brand_table, coded_a, coded_b, verdicts


def run_stage1(dry: bool = False, t4_dir=None, scored_ref=None, component_specs=None, activation=None,
               outdir: Path | None = None, registries=None, log=print, shuffle_draws=None, boot=True,
               expected_units: int = R.N_BRAND_UNITS) -> dict:
    outdir = Path(outdir) if outdir else ((DRY_OUT_DIR if dry else OUT_DIR) / "stage1")
    out_json = outdir / "stage1_v1_14.json"
    if out_json.exists():
        raise Halt(f"Stage 1 is scored once: {out_json} already exists")
    if dry:
        if t4_dir is None:
            raise Halt("--dry-run needs --t4-dir")
        src_raw = src_scored = Source(base=t4_dir)
        provenance = {"dry_run": True, "t4_dir": str(t4_dir)}
    else:
        ok, why = lock_status()
        if not ok:
            raise Halt("refusing Stage 1 before the lock: " + "; ".join(why))
        if not scored_ref:
            raise Halt("Stage 1 needs --v042-scored-ref (the v0.42 commit or tag holding its coded tables, "
                       "brand table and verdicts)")
        src_raw = Source(ref=V042_ACQ_TAG)
        src_scored = Source(ref=scored_ref)
        coder = src_raw.blob(V042_CODER_PATH)
        if coder != V042_CODER_BLOB:
            raise Halt(f"v0.42 coder at {V042_ACQ_TAG} is {coder}, not the pinned {V042_CODER_BLOB}")
        a, b = src_raw.blob(T4_FILES["raw"]), src_scored.blob(T4_FILES["raw"])
        if b is not None and a != b:
            raise Halt(f"t4_raw.jsonl at {scored_ref} differs from the acquisition-locked file")
        anchor = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
        activation = anchor.get("activation", {})
        provenance = {"dry_run": False, "raw_ref": V042_ACQ_TAG, "scored_ref": scored_ref,
                      "anchor_sha256": sha256_bytes(ANCHOR_FILE.read_bytes())}
    registries = registries or (load_registries_v110() if not dry else None)
    if registries is None:
        raise Halt("dry run needs registries (tests pass synthetic ones)")
    raw, bt, ca, cb, v42 = load_t4(src_raw, src_scored)
    comps = read_components(component_specs)
    res = stage1_core(raw, bt, ca, cb, v42, registries, activation, comps, log, boot=boot, shuffle_draws=shuffle_draws,
                      expected_units=expected_units)
    infos = res.pop("_infos")
    rt = rank_table_bytes(infos)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "rank_table_t4_v1_14.csv").write_bytes(rt)
    doc = {"phase": PHASE_ID, "stage": "1", "created_utc": _now(), "prereg_tag": PREREG_TAG, **provenance,
           "inputs_read": {**src_raw.log, **({} if src_scored is src_raw else
                                             {f"{scored_ref}:{k}": v for k, v in src_scored.log.items()})},
           "rank_table_t4_sha256": sha256_bytes(rt), "seeds": SEEDS, **res}
    _write_json(out_json, doc)
    log(f"[v1.14] Stage 1 written: {out_json}")
    return doc


def run_stage2(dry: bool = False, t4_dir=None, t5_dir=None, t5_ref=None, t5_raw_path=None, t5_probes_path=None,
               component_specs=None, outdir: Path | None = None, stage1_file: Path | None = None, registries=None,
               log=print, boot=True) -> dict:
    base = DRY_OUT_DIR if dry else OUT_DIR
    stage1_file = Path(stage1_file) if stage1_file else base / "stage1/stage1_v1_14.json"
    outdir = Path(outdir) if outdir else base / "stage2"
    out_json = outdir / "stage2_v1_14.json"
    if not stage1_file.exists():
        raise Halt("ORDER: Stage 1 has not been scored; Stage 2 refuses")
    if out_json.exists():
        raise Halt(f"Stage 2 is scored once: {out_json} already exists")
    s1 = json.loads(stage1_file.read_text(encoding="utf-8"))
    if dry:
        src4, src5 = Source(base=t4_dir), Source(base=t5_dir)
        raw5_rel, probes5_rel = T4_FILES["raw"], T4_FILES["probes"]
    else:
        ok, why = lock_status()
        if not ok:
            raise Halt("refusing Stage 2 before the lock: " + "; ".join(why))
        if not (t5_ref and t5_ref.endswith("-acquisition-locked") and tag_exists(t5_ref) and t5_ref != V042_ACQ_TAG):
            raise Halt(f"Stage 2 needs the t5 acquisition-locked tag (got {t5_ref!r})")
        if not (t5_raw_path and t5_probes_path):
            raise Halt("Stage 2 needs --t5-raw and --t5-probes (paths inside the t5 tag)")
        src4, src5 = Source(ref=V042_ACQ_TAG), Source(ref=t5_ref)
        raw5_rel, probes5_rel = t5_raw_path, t5_probes_path
    pp = probe_parity(src4.text(T4_FILES["probes"]), src5.text(probes5_rel))
    if not pp["identical"]:
        raise Halt(f"t5 does not repeat t4's 30 category questions verbatim: {pp}")
    registries = registries or (load_registries_v110() if not dry else None)
    raw4 = read_jsonl_text(src4.text(T4_FILES["raw"]))
    t4_answers, _m = phase_b_answers(raw4, "t4")
    t4_infos = extract_wave(t4_answers, registries)
    if sha256_bytes(rank_table_bytes(t4_infos)) != s1["rank_table_t4_sha256"]:
        raise Halt("re-extracted t4 rank table differs from Stage 1's")
    t4_models = [m for m in N3 if m not in s1.get("models_dropped_by_v0_42", {}).get("S0", [])]
    res = stage2_core(t4_infos, read_jsonl_text(src5.text(raw5_rel)), registries, t4_models, log, boot=boot)
    t5_infos = res.pop("_t5_infos")
    comps = read_components(component_specs)
    comp_v = dict(s1.get("component_legs", {}))
    comp_late = {}
    for name, c in comps.items():
        if comp_v.get(name) == "PENDING":
            U = {(u["substrate"], u["brand"]): {"rated": u["rated_S0"], STAT: u["R_star_S0"]} for u in s1["units"]}
            r = single_wave_sep(U, c["values"], STAT, SEEDS[f"COMP_{name}"], tuple(s1["gate_excluded_substrates"]),
                                boot=boot)
            r.update(score_file=c["file"], score_sha256=c["sha256"])
            comp_late[name], comp_v[name] = r, r["verdict"]
    gate = final_gate(s1["H1_Sep_Presence"]["verdict"], s1["H2_Sep_Consistency"]["verdict"],
                      res["H3_Retest_Reliability"]["verdict"], comp_v, s1["H4_Sep_Presence_S1"]["verdict"])
    rt5 = rank_table_bytes(t5_infos)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "rank_table_t5_v1_14.csv").write_bytes(rt5)
    doc = {"phase": PHASE_ID, "stage": "2", "created_utc": _now(), "dry_run": dry, "t5_ref": t5_ref,
           "stage1_sha256": sha256_bytes(stage1_file.read_bytes()), "probe_parity": pp,
           "inputs_read": {**src4.log, **{f"t5:{k}": v for k, v in src5.log.items()}},
           "rank_table_t5_sha256": sha256_bytes(rt5), **res, "component_legs_completed_at_stage2": comp_late,
           "component_legs": comp_v,
           "component_legs_pending": [n for n, v in comp_v.items() if v == "PENDING"],
           "GATE": gate}
    _write_json(out_json, doc)
    log(f"[v1.14] GATE: {gate}   (pending component legs: {doc['component_legs_pending']})")
    log(f"[v1.14] Stage 2 written: {out_json}")
    return doc


# ===========================================================================
# MAIN
# ===========================================================================


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--calibration", action="store_true")
    ap.add_argument("--stage", choices=["1", "2"])
    ap.add_argument("--lock-manifest", action="store_true", help="write prereg/LOCK_MANIFEST_v1_14.sha256")
    ap.add_argument("--verify-lock", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--t4-dir"), ap.add_argument("--t5-dir")
    ap.add_argument("--v042-scored-ref")
    ap.add_argument("--t5-ref"), ap.add_argument("--t5-raw"), ap.add_argument("--t5-probes")
    ap.add_argument("--component", action="append", help="NAME=path.csv (substrate, brand, value)")
    ap.add_argument("--write-anchor", action="store_true", help="after the tag is pushed: anchor/git_anchor_v1_14.json")
    ap.add_argument("--osf-note", default="", help="OSF deposit location, recorded in the anchor")
    a = ap.parse_args(argv)
    try:
        if a.write_anchor:
            d = write_anchor(a.osf_note)
            print(json.dumps({k: d[k] for k in ("tag", "tag_object", "commit", "tree", "activation")}, indent=1))
            return 0
        if a.calibration:
            run_calibration()
            return 0
        if a.lock_manifest:
            LOCK_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
            LOCK_MANIFEST.write_text(lock_manifest_text())
            print(LOCK_MANIFEST.read_text(), end="")
            return 0
        if a.verify_lock:
            bad = verify_lock_manifest()
            print("lock manifest OK" if not bad else "\n".join(bad))
            return 0 if not bad else 1
        if a.stage == "1":
            if a.dry_run:
                print("[v1.14] --dry-run of Stage 1 runs from the tests (synthetic registries); see "
                      "scripts/test_score_v1_14.py", file=sys.stderr)
                return 2
            run_stage1(scored_ref=a.v042_scored_ref, component_specs=a.component)
            return 0
        if a.stage == "2":
            if a.dry_run:
                print("[v1.14] --dry-run of Stage 2 runs from the tests (synthetic registries)", file=sys.stderr)
                return 2
            run_stage2(t5_ref=a.t5_ref, t5_raw_path=a.t5_raw, t5_probes_path=a.t5_probes, component_specs=a.component)
            return 0
    except Halt as e:
        print(f"[v1.14] HALT: {e}", file=sys.stderr)
        return 3
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
