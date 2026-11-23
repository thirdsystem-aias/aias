#!/usr/bin/env python3
"""
score_v1_21.py - AIAS v1.21, Sentiment redesigned: co-mention tone (TONE), confirmed blind on t5.

STATUS: DRAFT scorer (2026-11-23) written for PRE_REGISTRATION_v1_21_DRAFT_r2.md (osf/methodology/v1_21/prereg/);
to be locked with it at tag v1.21-prereg-r1. Rules are transcribed from that draft; each section is cited inline.
Where the draft leaves a choice to the code, the most literal reading is taken and marked "READING (section):".

What is reused, unchanged (section 5, section 6 conventions)
  * v1.10's correlation machinery (scripts/score_v1_10.py): pooled within-category Spearman on centred ranks,
    within-category permutation null, bootstrap percentile CI, the uncentred switch (sensitivity SU).
  * v1.11's locked scorer (scripts/score_v1_11.py): unit score u = 25(valence + 2), brand_score (S_ref), the
    Krippendorff alpha (ordinal), Cohen's kappa, the band / judge-agreement / self-preference verdict rules,
    v1.11's outcome rule (sensitivity S-ATT) and provider_of.
  * v1.20's extraction rule (scripts/score_v1_20.py: parse_reply / outcomes, switches in config_v1_20.json).
  * v1.16's Bradley-Terry estimator fit_bt and its component labeller _components, read from tag
    v1.16-prereg-r1 (scripts/score_v1_16.py, git blob pinned below) and executed from their own source text,
    unchanged (that module imports score_v1_14, which is not on this branch, so the module itself is not imported).

New here: comparisons from co-mentions decided by the order of J1 unit scores (section 3.1), TONE and its rating
rule (sections 3.2-3.3), the secondaries (section 3.4), H1_t5 ... H7_t5, the noise guard, the gate and its
consequence clause (sections 6-8), the checks (section 9) and the sensitivities (section 10).

Inputs (section 4). The scorer works on one canonical unit-outcome table per wave (UNIT_COLS below; one row per
judged window = (answer, brand)), which Stage J builds from a wave's unit table and frozen judge record
(v1.11 / v1.15 formats) with v1.20's rule, writes once and hashes. Stage C opens P and C* (t5: v0.45's
v45_unit_table.csv; t4: v1.14 Stage 1's stage1_v1_14.json units[]).

Modes (repository root; PYTHONDONTWRITEBYTECODE=1 python3 osf/methodology/v1_21/scripts/score_v1_21.py ...)
  --stage J --t4-dir D4 --t5-dir D5    unit outcomes, JUDGE_FAIL check, TONE and secondaries at t4 and t5,
                                       H1_t5, self-consistency, precision table. Reads no P, C* or R*.
  --stage C --t4-stage1 F --t5-presence F
                                       opens P and C*: H2-H7, noise guard, gate, sensitivities, checks,
                                       descriptives -> v1_21_verdicts.json and values_v1_21.json.
  --exploratory                        RQ3 on t1-t3 (refuses before the lock is anchored; section 10).
  --fixture DIR --out DIR [--draws N]  both stages on a synthetic fixture folder (tests and the dry run only).
  --lock-manifest                      prints the draft lock manifest (prereg/LOCK_MANIFEST_v1_21.sha256 format).
Real stages refuse before tag v1.21-prereg-r1 exists, and each runs once (an existing output refuses).
No network, no model call, no paid API.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import math
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                     # osf/methodology/v1_21/scripts -> repository root
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_10 as V    # noqa: E402  v1.10's locked correlation machinery (as v1.11 imports it)
import score_v1_11 as S    # noqa: E402  v1.11's locked scorer (tag v1.11-prereg-r1)
import score_v1_20 as R20  # noqa: E402  v1.20's extraction rule (tag v1.20-prereg-r1)

# ======================================================================================
# 0. TRANSCRIBED CONSTANTS
# ======================================================================================
PHASE_ID = "v1.21"
PREREG_TAG = "v1.21-prereg-r1"
STATUS = "DRAFT (2026-11-23), not locked"
V121 = "osf/methodology/v1_21"
PREREG_REL = V121 + "/prereg/PRE_REGISTRATION_v1_21_DRAFT_r2.md"
OUT_DIR = ROOT / V121 / "outputs"
ANCHOR_FILE = ROOT / V121 / "anchor/git_anchor_v1_21.json"
STAGE_J_NAME = "stage_j_v1_21.json"
VERDICTS_NAME = "v1_21_verdicts.json"
VALUES_NAME = "values_v1_21.json"
OUTCOMES_NAME = {"t4": "unit_outcomes_t4_v1_21.csv", "t5": "unit_outcomes_t5_v1_21.csv"}
EXPLORATORY_NAME = "exploratory_t1_t3_v1_21.json"

WAVES = ("t4", "t5")
VALID, FAIL, UNJUDGED = S.VALID, S.FAIL, S.UNJUDGED
FLOOR = S.N_FLOOR                          # 6 answers contributing a comparison (section 3.3)
FLOOR_SENS = (3, 10)                       # S_floor (section 3.3)
PRIOR = 1.0                                # lambda (section 3.2)
PRIOR_SENS = (0.1, 10.0)                   # S_prior
BAND_CONF, BAND_FALS = S.BAND_CONFIRMED_MAX, S.BAND_FALSIFIED_MIN          # 0.30 / 0.50, unrounded (section 7)
STAB_CONF, STAB_FALS = S.STAB_CONFIRMED_MIN, S.STAB_FALSIFIED_BELOW        # 0.50 / 0.30 (H4)
ALPHA_P = S.ALPHA_P                        # .05
MIN_UNITS_POOLED, MIN_GROUPS, MIN_UNITS_PER_GROUP = S.MIN_UNITS_POOLED, S.MIN_GROUPS, S.MIN_UNITS_PER_GROUP  # 20 / 3 / 4
N_PERM = N_SHUFFLE = N_BOOT = 10_000
CI_LEVEL = 0.95
JUDGE_FAIL_HALT_SHARE = S.JUDGE_FAIL_HALT_SHARE          # 0.02 (section 9)
EXTRACTION_MISS_HALT_SHARE = S.EXTRACTION_MISS_HALT_SHARE  # 0.05 (section 9, U0)
SELFCON_MIN_EXACT = S.SELFCON_MIN_EXACT                  # 0.90
MQ7_MAX = 0.20
MQ9_MAX_SHARE = 0.10
SEEDS = {"unit_order": 121000, "selfcon": 121003, "shuffle": 121010, "H4_perm": 121011, "boot": 121020}
PRECISION_TRUE_RHO = (0.00, 0.10, 0.15, 0.20, 0.25, 0.30)   # section 7 table
DENON = ("v0.19", "Denon")
# S-COI (section 10, section 17): Denon and the five agency-work brands, in the registry keys of the unit tables
# (v1.16's COI_CHEIL; in the v0.23 registry key Jack Daniel's is S03, as in units_v1_15.csv).
COI = (DENON, ("v0.20", "Eucerin"), ("v0.22", "BMW"), ("v0.22", "Bentley"), ("v0.22", "Chevrolet"), ("v0.23", "S03"))
GATE_ROWS = ("H1_t5", "H2_t5", "H3_t5", "H4")
NOISE_GUARDED = ("H2_t5", "H3_t5", "H5_t4")               # section 6, noise guard
CONSEQUENCE_PASS = ("PASS: TONE may be reported as the AIAS Sentiment component, labelled provisional until Paper B; "
                    "its t4 and t5 values are the locked Sentiment score on the N3 answers. Before any calibration "
                    "that combines Sentiment with another component, rho_w(TONE, that component) is computed on the "
                    "same units under the same bands; FALSIFIED there turns PASS into FAIL.")
CONSEQUENCE_NOT_PASS = ("NOT PASS: Sentiment is reported as not separable from Presence and not as a separate AIAS "
                        "component. There is no further Sentiment redesign.")
V120_VERDICTS_REL = "osf/methodology/v1_20/outputs/v1_20_verdicts.json"

# Pinned inputs (section 9, Pins). SHA-256 of files in this repository / of v1.15's and v1.14's frozen files.
V116_TAG, V116_PATH = "v1.16-prereg-r1", "scripts/score_v1_16.py"
V116_BLOB = "6f14cf84a78f83ebbcad22f6f43bdd588a7fa796"     # git blob of scripts/score_v1_16.py at the tag
CODE_PINS = {   # as locked in LOCK_MANIFEST_v1_20.sha256 (tag v1.20-prereg-r1)
    "scripts/score_v1_10.py": "651cb8c240e914e2a82f9b31aa5e46eb5d9d61dbb7a8b4d7072b91d2997975a5",
    "scripts/score_v1_11.py": "9cea3b59697acd713c8a432cb54dbf92949bc51a58cac1c96185a54fc4745d1d",
    "scripts/score_v1_20.py": "ef89d1ddf363f63fb5ca9f562dd5c8e49e3398d4640e89e215213e3f0c59a544",
    "osf/methodology/v1_20/prereg/config_v1_20.json": "015adfadd6923e8631ac16346c31a82bd1bc8f5d3e4f7ede4b34c2c762e2312f",
}
T4_PINS = {     # section 4.1: v1.15's frozen record (branch v1.15) and v1.14 Stage 1 (pinned in v1.16)
    "raw_sha256": "926ed9b0505608a273a089d6395fc63b4d235f142247b00718191c4f9a9db01a",
    "units_sha256": "2fb080fb982256265657244938a0c9c3e2eda09115f20ea3394b1b03bfa6e1ce",
    "stage1_sha256": "4de97fea86fd7c74f990ba4bdecd43c19aa52afc60278676624374a164f68e2f",
    "roles": {"J1": "claude-opus-5-5", "J2": "gpt-6.1-sol"},
}

Halt = S.Halt
NAN = float("nan")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(p) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ======================================================================================
# 1. v1.16's ESTIMATOR, read from its tag and run from its own source text (section 3.2)
# ======================================================================================
def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load_v116(root: Path = ROOT) -> Dict[str, Callable]:
    """fit_bt and _components from `git show v1.16-prereg-r1:scripts/score_v1_16.py`, after checking the blob
    against V116_BLOB (a mismatch halts). Only these two function definitions are executed, from their exact
    source segments, in a namespace holding numpy and v1.16's PRIOR (= 1.0, checked in the source)."""
    try:
        data = subprocess.run(["git", "-C", str(root), "show", f"{V116_TAG}:{V116_PATH}"],
                              capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        raise Halt(f"Pins: cannot read {V116_PATH} at {V116_TAG}: {e}") from e
    if _git_blob_sha1(data) != V116_BLOB:
        raise Halt(f"Pins: {V116_PATH} at {V116_TAG} is not blob {V116_BLOB}")
    src = data.decode("utf-8")
    if "\nPRIOR = 1.0 " not in src:
        raise Halt("Pins: v1.16's PRIOR is not 1.0")
    tree = ast.parse(src)
    ns: dict = {"np": np, "PRIOR": 1.0}
    found = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in ("fit_bt", "_components"):
            exec(compile(ast.get_source_segment(src, node), f"{V116_TAG}:{V116_PATH}", "exec"), ns)  # noqa: S102
            found[node.name] = ns[node.name]
    if set(found) != {"fit_bt", "_components"}:
        raise Halt("Pins: fit_bt / _components not found in v1.16's scorer")
    return found


_V116 = load_v116()
fit_bt = _V116["fit_bt"]
_components = _V116["_components"]


# ======================================================================================
# 2. THE CANONICAL UNIT-OUTCOME TABLE (one row per judged window; section 4.2)
# ======================================================================================
ROLES_ALL = ("J1", "J2", "J1att", "J2att")      # J*att = sensitivity S-ATT (v1.20's alternative attempt rule)
UNIT_COLS = (["unit_id", "wave", "category", "brand", "answer_id", "model", "provider"]
             + [f"{r}_{f}" for r in ROLES_ALL[:2] for f in ("status", "valence", "evaluative", "refers")]
             + ["J1_rep_status", "J1_rep_valence", "J2_rep_status", "J2_rep_valence"]
             + [f"{r}_{f}" for r in ROLES_ALL[2:] for f in ("status", "valence", "evaluative", "refers")])


def _b(x) -> bool:
    return str(x).strip().lower() in ("1", "true")


def parse_unit_rows(text: str) -> List[dict]:
    """Canonical table (CSV text) -> typed rows. A judge view is {status, valence, evaluative, refers}."""
    rd = csv.DictReader(io.StringIO(text))
    missing = [c for c in UNIT_COLS if c not in (rd.fieldnames or [])]
    if missing:
        raise Halt(f"unit-outcome table lacks columns {missing}")
    out = []
    for r in rd:
        row = {k: r[k] for k in ("unit_id", "wave", "category", "brand", "answer_id", "model", "provider")}
        for role in ROLES_ALL:
            st = r[f"{role}_status"] or UNJUDGED
            val = r[f"{role}_valence"]
            row[role] = {"status": st, "valence": int(val) if st == VALID else None,
                         "evaluative": _b(r[f"{role}_evaluative"]) if st == VALID else False,
                         "refers": _b(r[f"{role}_refers"]) if st == VALID else False}
        for role in ("J1", "J2"):
            st = r[f"{role}_rep_status"]
            row[f"{role}rep"] = {"status": st or None,
                                 "valence": int(r[f"{role}_rep_valence"]) if st == VALID else None}
        out.append(row)
    ids = Counter(x["unit_id"] for x in out)
    dup = [k for k, c in ids.items() if c > 1]
    if dup:
        raise Halt(f"duplicate unit_id in unit-outcome table: {dup[:3]}")
    return out


def unit_rows_csv_bytes(rows: List[dict]) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(UNIT_COLS)
    for r in sorted(rows, key=lambda x: x["unit_id"]):
        line = [r[k] for k in ("unit_id", "wave", "category", "brand", "answer_id", "model", "provider")]
        for role in ROLES_ALL[:2]:
            j = r[role]
            ok = j["status"] == VALID
            line += [j["status"], j["valence"] if ok else "", int(j["evaluative"]) if ok else "",
                     int(j["refers"]) if ok else ""]
        for role in ("J1", "J2"):
            j = r[f"{role}rep"]
            line += [j["status"] or "", j["valence"] if j["status"] == VALID else ""]
        for role in ROLES_ALL[2:]:
            j = r[role]
            ok = j["status"] == VALID
            line += [j["status"], j["valence"] if ok else "", int(j["evaluative"]) if ok else "",
                     int(j["refers"]) if ok else ""]
        w.writerow(line)
    return buf.getvalue().encode("utf-8")


def _view(o: Optional[dict]) -> dict:
    if not o or o["status"] != VALID:
        return {"status": (o or {}).get("status", UNJUDGED), "valence": None, "evaluative": False, "refers": False}
    j = o["out"]
    return {"status": VALID, "valence": int(j["valence"]), "evaluative": bool(j["evaluative"]),
            "refers": bool(j["refers_to_brand"])}


def build_unit_rows(units: List[dict], records: List[dict], roles: Dict[str, str], wave: str) -> List[dict]:
    """A wave's unit table (v1.11 / v1.15 UNIT columns) + its stored judge records -> canonical rows.
    Primary outcomes: v1.20's rule (R20.outcomes, config_v1_20.json switches). S-ATT: v1.20's
    outcomes_v111_first (v1.11's own judgement where it yields one). Only judged windows (judged = 1)."""
    oc = R20.outcomes(records, roles)
    att = R20.outcomes_v111_first(S.outcomes(records, roles), oc)
    out = []
    for u in units:
        if not _b(u["judged"]):
            continue
        if u["wave"] != wave:
            raise Halt(f"unit {u['unit_id']} has wave {u['wave']}, expected {wave}")
        uid = u["unit_id"]
        row = {k: u[k] for k in ("unit_id", "wave", "category", "brand", "answer_id", "model", "provider")}
        row["J1"], row["J2"] = _view(S._oc(oc, "J1", uid)), _view(S._oc(oc, "J2", uid))
        row["J1att"], row["J2att"] = _view(S._oc(att, "J1", uid)), _view(S._oc(att, "J2", uid))
        for role in ("J1", "J2"):
            rep = S._oc(oc, role, uid, "repeat")
            sel = _b(u.get("selfcon", 0))
            row[f"{role}rep"] = {"status": rep["status"] if sel else None,
                                 "valence": rep["out"]["valence"] if sel and rep["status"] == VALID else None}
        out.append(row)
    return out


# ======================================================================================
# 3. COMPARISONS AND THE MEASURES (sections 3.1-3.4)
# ======================================================================================
class Comps:
    """The comparisons of ONE category at ONE wave from one judge view (section 3.1). Every answer with valid
    judgements (status VALID, refers_to_brand true) for >= 2 registry brands gives, for every pair of them, one
    comparison won by the higher unit score u (equal u: half a win each). Weight 1 per comparison ('pairs',
    primary) or 1/(k - 1) ('per_answer', sensitivity S_w). nv=True keeps only evaluative windows (TONE_NV).
    Rows (one per valid window) are ordered by answer, then brand, so the within-answer shuffle is a lexsort."""

    def __init__(self, rows: List[dict], role: str = "J1", weighting: str = "pairs", nv: bool = False):
        by_ans: Dict[str, Dict[str, float]] = defaultdict(dict)
        for r in rows:
            j = r[role]
            if j["status"] != VALID or not j["refers"] or (nv and not j["evaluative"]):
                continue
            if r["brand"] in by_ans[r["answer_id"]]:
                raise Halt(f"two windows for one (answer, brand): {r['answer_id']} {r['brand']}")
            by_ans[r["answer_id"]][r["brand"]] = S.unit_score(j["valence"])
        self.brands = sorted({b for a in by_ans.values() for b in a})
        self.idx = {b: i for i, b in enumerate(self.brands)}
        nb = len(self.brands)
        ans, bi, u, ra, rb, wt = [], [], [], [], [], []
        self.n_contrib = np.zeros(nb, int)        # answers contributing a comparison that include the brand
        self.n_windows = np.zeros(nb, int)        # valid windows (S_ref's n)
        self.n_answers_ge2 = 0
        for ai, aid in enumerate(sorted(by_ans)):
            items = sorted(by_ans[aid].items())
            base = len(u)
            for b, x in items:
                ans.append(ai); bi.append(self.idx[b]); u.append(x)
                self.n_windows[self.idx[b]] += 1
            m = len(items)
            if m < 2:
                continue
            self.n_answers_ge2 += 1
            w = 1.0 if weighting == "pairs" else 1.0 / (m - 1)
            for p in range(m):
                self.n_contrib[self.idx[items[p][0]]] += 1
                for q in range(p + 1, m):
                    ra.append(base + p); rb.append(base + q); wt.append(w)
        self.n_answers = len(by_ans)
        self.ans = np.array(ans, np.int64)
        self.bi = np.array(bi, np.int64)
        self.u = np.array(u, float)
        self.ra, self.rb, self.wt = np.array(ra, np.int64), np.array(rb, np.int64), np.array(wt, float)
        self.m_of_row = np.bincount(self.ans, minlength=self.n_answers)[self.ans] if len(self.ans) else np.zeros(0, int)
        self._main = None

    def win_matrix(self, u: Optional[np.ndarray] = None) -> np.ndarray:
        u = self.u if u is None else u
        n = len(self.brands)
        if not len(self.ra):
            return np.zeros((n, n))
        ua, ub = u[self.ra], u[self.rb]
        a_win = (ua > ub).astype(float) + 0.5 * (ua == ub)
        ia, ib = self.bi[self.ra], self.bi[self.rb]
        W = np.bincount(ia * n + ib, weights=self.wt * a_win, minlength=n * n)
        W += np.bincount(ib * n + ia, weights=self.wt * (1.0 - a_win), minlength=n * n)
        return W.reshape(n, n)

    def shuffled_u(self, rng) -> np.ndarray:
        """H4 null (b): each answer's valid unit scores shuffled among the brands it names (the answer's set
        of scores kept). One rng.random draw per valid window; rows are grouped by answer."""
        order = np.lexsort((rng.random(len(self.u)), self.ans))
        return self.u[order]

    def main_component(self) -> np.ndarray:
        if self._main is None:
            n = len(self.brands)
            adj = np.zeros((n, n), bool)
            if len(self.ra):
                ia, ib = self.bi[self.ra], self.bi[self.rb]
                adj[ia, ib] = True
                adj[ib, ia] = True
            if not n:
                self._main = np.zeros(0, bool)
            else:
                lab = _components(adj)
                self._main = lab == int(np.argmax(np.bincount(lab)))   # equal largest: lowest label (v1.16)
        return self._main

    def tied_share(self) -> Optional[float]:
        if not len(self.ra):
            return None
        return float(np.mean(self.u[self.ra] == self.u[self.rb]))


KINDS = ("TONE", "TONE_NV", "CONTRAST", "S_ref", "S_cat")


def cat_values(c: Comps, kind: str, floor: int = FLOOR, prior: float = PRIOR,
               u: Optional[np.ndarray] = None) -> Dict[str, dict]:
    """{brand: {value, rated, ...}} for one category. TONE / TONE_NV: fit_bt(W, prior); rated iff >= floor
    contributing answers AND in the largest connected component (section 3.3). CONTRAST: mean over contributing
    answers of u_b - mean u of the other valid brands of that answer; READING (3.4 'same floor'): rated iff
    >= floor contributing answers (no component condition, CONTRAST is not a fitted strength). S_ref: mean u
    over all valid windows, rated iff >= floor windows (v1.11's n >= 6, brand_score). S_cat: S_ref minus the
    mean S_ref of the category's rated units."""
    u = c.u if u is None else u
    out: Dict[str, dict] = {}
    if kind in ("TONE", "TONE_NV"):
        th = fit_bt(c.win_matrix(u), prior)
        mc = c.main_component()
        W = c.win_matrix(u)
        ncomp = (W + W.T).sum(1) if len(c.brands) else np.zeros(0)
        for b, i in c.idx.items():
            out[b] = {"value": float(th[i]), "rated": bool(c.n_contrib[i] >= floor and mc[i]),
                      "n_contrib": int(c.n_contrib[i]), "main_component": bool(mc[i]),
                      "n_comparisons": float(ncomp[i])}
        return out
    if kind == "CONTRAST":
        nb = len(c.brands)
        tot = np.bincount(c.ans, weights=u, minlength=c.n_answers) if len(u) else np.zeros(0)
        m = c.m_of_row
        keep = m >= 2
        d = np.where(keep, u - (tot[c.ans] - u) / np.maximum(m - 1, 1), 0.0) if len(u) else np.zeros(0)
        s = np.bincount(c.bi[keep], weights=d[keep], minlength=nb) if len(u) else np.zeros(nb)
        for b, i in c.idx.items():
            n = int(c.n_contrib[i])
            out[b] = {"value": float(s[i] / n) if n else None, "rated": bool(n >= floor and n > 0), "n_contrib": n}
        return out
    if kind in ("S_ref", "S_cat"):
        nb = len(c.brands)
        s = np.bincount(c.bi, weights=u, minlength=nb) if len(u) else np.zeros(nb)
        for b, i in c.idx.items():
            n = int(c.n_windows[i])
            out[b] = {"value": float(s[i] / n) if n >= floor else None, "rated": bool(n >= floor), "n": n}
        if kind == "S_cat":
            rated = [v["value"] for v in out.values() if v["rated"]]
            mu = float(np.mean(rated)) if rated else 0.0
            for v in out.values():
                if v["rated"]:
                    v["value"] = v["value"] - mu
        return out
    raise ValueError(kind)


class Wave:
    """All judged windows of one wave, grouped by category; Comps cached per (role, weighting, nv)."""

    def __init__(self, name: str, rows: List[dict]):
        self.name = name
        self.rows = sorted(rows, key=lambda r: r["unit_id"])
        self.by_cat: Dict[str, List[dict]] = defaultdict(list)
        for r in self.rows:
            if r["wave"] != name:
                raise Halt(f"row {r['unit_id']} has wave {r['wave']} in wave {name}")
            self.by_cat[r["category"]].append(r)
        self.cats = sorted(self.by_cat)
        self._cache: Dict[tuple, Dict[str, Comps]] = {}

    def comps(self, role: str = "J1", weighting: str = "pairs", nv: bool = False) -> Dict[str, Comps]:
        k = (role, weighting, nv)
        if k not in self._cache:
            self._cache[k] = {c: Comps(self.by_cat[c], role, weighting, nv) for c in self.cats}
        return self._cache[k]


def wave_values(comps: Dict[str, Comps], kind: str, floor: int = FLOOR, prior: float = PRIOR,
                u_by_cat: Optional[Dict[str, np.ndarray]] = None) -> Dict[Tuple[str, str], dict]:
    out = {}
    for cat in sorted(comps):
        for b, v in cat_values(comps[cat], kind, floor, prior, None if u_by_cat is None else u_by_cat[cat]).items():
            out[(cat, b)] = v
    return out


def measure(w: Wave, kind: str, role: str = "J1", weighting: str = "pairs", floor: int = FLOOR,
            prior: float = PRIOR) -> Dict[Tuple[str, str], dict]:
    nv = kind == "TONE_NV"
    return wave_values(w.comps(role, weighting, nv), kind, floor, prior)


def s_ref_v111(w: Wave, role: str = "J1", floor: int = FLOOR) -> Dict[Tuple[str, str], dict]:
    """S_ref with v1.11's own brand_score (section 3.4: 'with v1.11's code'); JUDGE_FAIL enters as None and
    refers_to_brand false is excluded inside brand_score; UNJUDGED windows are not passed (score_map)."""
    groups: Dict[tuple, list] = defaultdict(list)
    for r in w.rows:
        j = r[role]
        if j["status"] == UNJUDGED:
            continue
        groups[(r["category"], r["brand"])].append(
            None if j["status"] == FAIL else {"refers_to_brand": j["refers"], "valence": j["valence"],
                                              "evaluative": j["evaluative"]})
    out = {}
    for k, js in groups.items():
        bs = S.brand_score(js, floor)
        out[k] = {"value": bs.S, "rated": bs.S is not None, "n": bs.n}
    return out


# ======================================================================================
# 4. STATISTICS (section 6 conventions: v1.11 section 5, unchanged)
# ======================================================================================
class Draws:
    """Resampling draw counts. The pre-registered values are 10,000 each; tests and the dry run may lower them
    (recorded in every output)."""

    def __init__(self, perm: int = N_PERM, shuffle: int = N_SHUFFLE, boot: int = N_BOOT):
        self.perm, self.shuffle, self.boot = int(perm), int(shuffle), int(boot)

    def as_dict(self) -> dict:
        return {"perm": self.perm, "shuffle": self.shuffle, "boot": self.boot, "ci": CI_LEVEL,
                "preregistered": self.perm == N_PERM and self.shuffle == N_SHUFFLE and self.boot == N_BOOT}


def ptest(x, y, groups, draws: Draws, boot: bool = True, perm_seed: Optional[int] = None) -> dict:
    """v1.11's pooled_test with explicit draw counts: categories with >= 4 units enter; determinable iff >= 20
    units from >= 3 categories and rho finite; 95% bootstrap (units resampled within category, seed 121020,
    reported only); optional within-category permutation p (y permuted, one-sided)."""
    x, y, g = np.asarray(x, float), np.asarray(y, float), np.asarray([str(v) for v in groups])
    if len(g):
        m = V.keep_categories(g, MIN_UNITS_PER_GROUP)
        x, y, g = x[m], y[m], g[m]
    n, ng = int(len(g)), len(set(g.tolist()))
    rho = V.pooled_within_rho(x, y, g) if n >= 3 else NAN
    out = {"rho": rho, "abs_rho": abs(rho) if math.isfinite(rho) else NAN, "n": n,
           "units_per_category": dict(sorted(Counter(g.tolist()).items())),
           "determinable": bool(n >= MIN_UNITS_POOLED and ng >= MIN_GROUPS and math.isfinite(rho))}
    if boot and n >= 3:
        out["ci95"] = list(V.boot_ci(x, y, g, SEEDS["boot"], n_draws=draws.boot, level=CI_LEVEL))
    if perm_seed is not None:
        out["p_perm"] = V.perm_p(x, y, g, rho, perm_seed, "one", draws.perm) if n >= 3 and math.isfinite(rho) else NAN
        out["perm_seed"] = perm_seed
    out["_x"], out["_y"], out["_g"] = x, y, g
    return out


def _strip(d: dict) -> dict:
    return {k: v for k, v in d.items() if not k.startswith("_")}


def band(res: dict) -> str:
    """Separability rows (H2_t5, H3_t5, H5_t4, H6_t5): v1.11's bands on |rho| at one wave (section 6, single
    wave); UNDETERMINED under the floors."""
    return S.band_verdict(res["abs_rho"]) if res["determinable"] else "UNDETERMINED"


def stability_verdict(rho: float, p_perm: float, p_shuffle: float, determinable: bool) -> str:
    """H4: CONFIRMED iff rho >= 0.50 AND p_perm < .05 AND p_shuffle < .05; FALSIFIED iff rho < 0.30 OR
    p_perm >= .05 OR p_shuffle >= .05; MARGINAL otherwise; UNDETERMINED under the floors."""
    if not determinable or any(v is None or not math.isfinite(v) for v in (rho, p_perm, p_shuffle)):
        return "UNDETERMINED"
    if rho >= STAB_CONF and p_perm < ALPHA_P and p_shuffle < ALPHA_P:
        return "CONFIRMED"
    if rho < STAB_FALS or p_perm >= ALPHA_P or p_shuffle >= ALPHA_P:
        return "FALSIFIED"
    return "MARGINAL"


def _keys(U: dict, Y: Optional[dict], excl) -> List[tuple]:
    return sorted(k for k, v in U.items() if v["rated"] and v["value"] is not None and k not in excl
                  and (Y is None or (Y.get(k) is not None and math.isfinite(Y[k]))))


def sep(U: dict, Y: dict, draws: Draws, excl=frozenset(), boot: bool = True) -> dict:
    """|rho_w(measure, Y)| over rated units with Y (section 6, H2_t5 / H3_t5 / H5_t4 / H6_t5)."""
    ks = _keys(U, Y, excl)
    res = ptest([Y[k] for k in ks], [U[k]["value"] for k in ks], [k[0] for k in ks], draws, boot)
    res["verdict"] = band(res)
    return _strip(res)


def retest(c4: Dict[str, Comps], c5: Dict[str, Comps], kind: str, draws: Draws, floor: int = FLOOR,
           prior: float = PRIOR, excl=frozenset(), boot: bool = True) -> dict:
    """H4 (section 6): rho_w(X_t4, X_t5) over units rated at both waves (categories with >= 4 such units).
    (a) X_t5 permuted within category, one-sided, seed 121011. (b) within-answer shuffle null, seed 121010:
    at both waves each answer's valid unit scores are shuffled among the brands it names, the measure is
    recomputed (TONE refitted), and the hits are draws with rho >= observed (one-sided). The units kept are
    the observed ones (the shuffle keeps every answer's brand set, so n_contrib and the comparison graph,
    hence rating, are unchanged). Draw order: one generator; per draw t4 then t5, categories sorted.
    The mean shuffled rho is the negative control MQ7."""
    U4, U5 = wave_values(c4, kind, floor, prior), wave_values(c5, kind, floor, prior)
    ks = sorted(k for k in U4 if U4[k]["rated"] and k in U5 and U5[k]["rated"] and k not in excl)
    res = ptest([U4[k]["value"] for k in ks], [U5[k]["value"] for k in ks], [k[0] for k in ks], draws, boot,
                perm_seed=SEEDS["H4_perm"])
    g = res["_g"]
    m = V.keep_categories(np.asarray([k[0] for k in ks]), MIN_UNITS_PER_GROUP) if ks else np.zeros(0, bool)
    ks = [k for k, ok in zip(ks, m) if ok]
    rho = res["rho"]
    if ks and math.isfinite(rho):
        rng = np.random.default_rng(SEEDS["shuffle"])
        gidx = V._group_index(g)
        cats = sorted({k[0] for k in ks})
        hits, vals = 0, []
        for _ in range(draws.shuffle):
            sh = {}
            for side, C in (("t4", c4), ("t5", c5)):
                for cat in sorted(C):
                    uu = C[cat].shuffled_u(rng)
                    if cat not in cats:
                        continue
                    for b, v in cat_values(C[cat], kind, floor, prior, uu).items():
                        sh[(side, cat, b)] = v["value"]
            xs = np.array([sh[("t4",) + k] for k in ks], float)
            ys = np.array([sh[("t5",) + k] for k in ks], float)
            r = V._pearson(V._within_ranks_idx(xs, gidx), V._within_ranks_idx(ys, gidx))
            vals.append(r)
            hits += r >= rho - 1e-12
        res["p_shuffle"] = (hits + 1) / (draws.shuffle + 1)
        res["shuffled_mean_rho"] = float(np.nanmean(vals)) if vals else NAN
    else:
        res["p_shuffle"], res["shuffled_mean_rho"] = NAN, NAN
    res["shuffle_seed"] = SEEDS["shuffle"]
    res["verdict"] = stability_verdict(rho, res.get("p_perm", NAN), res["p_shuffle"], res["determinable"])
    return _strip(res)


def h1_t5(w5: Wave, draws: Draws, excl=frozenset(), role1: str = "J1", role2: str = "J2",
          floor: int = FLOOR, prior: float = PRIOR, weighting: str = "pairs") -> dict:
    """H1_t5 (section 6): Krippendorff alpha (ordinal) on valence over every t5 window with valid J1 and J2
    outputs (refers_to_brand either way, as v1.11's h1_block); brand rho_w(TONE_J1, TONE_J2), groups =
    category, units rated under both. Determinable iff the brand row is and >= 20 windows enter alpha."""
    pairs, ev1, ev2, conf = [], [], [], Counter()
    per_cat: Dict[str, list] = defaultdict(list)
    for r in w5.rows:
        if (r["category"], r["brand"]) in excl:
            continue
        a, b = r[role1], r[role2]
        if a["status"] != VALID or b["status"] != VALID:
            continue
        pairs.append((a["valence"], b["valence"]))
        per_cat[r["category"]].append((a["valence"], b["valence"]))
        ev1.append(a["evaluative"]); ev2.append(b["evaluative"])
        conf[(a["valence"], b["valence"])] += 1
    alpha = S.krippendorff_alpha_ordinal(pairs) if len(pairs) >= 2 else NAN
    T1 = wave_values(w5.comps(role1, weighting), "TONE", floor, prior)
    T2 = wave_values(w5.comps(role2, weighting), "TONE", floor, prior)
    ks = sorted(k for k in T1 if T1[k]["rated"] and k in T2 and T2[k]["rated"] and k not in excl)
    br = _strip(ptest([T1[k]["value"] for k in ks], [T2[k]["value"] for k in ks], [k[0] for k in ks], draws))
    det = br["determinable"] and len(pairs) >= MIN_UNITS_POOLED
    return {"verdict": S.judge_agreement_verdict(alpha, br["rho"], det), "alpha_ordinal": alpha,
            "windows_judged_by_both": len(pairs), "brand_rho": br,
            "alpha_by_category": {c: S.krippendorff_alpha_ordinal(v) if len(v) >= 2 else None
                                  for c, v in sorted(per_cat.items())},
            "kappa_evaluative": S.cohen_kappa(ev1, ev2) if ev1 else None,
            "confusion_J1_rows_J2_cols": {f"{a}|{b}": c for (a, b), c in sorted(conf.items())},
            "thresholds": {"CONFIRMED": "alpha >= 0.667 AND brand rho >= 0.80",
                           "FALSIFIED": "alpha < 0.50 OR brand rho < 0.60"}}


def h7_t5(w5: Wave, j1_model: str, excl=frozenset(), role1: str = "J1", role2: str = "J2") -> dict:
    """H7_t5 = v1.11's H9 on t5 windows: delta = mean(u_J1 - u_J2 | answer by J1's provider) - mean(... | other
    providers), windows with valid J1 and J2 outputs that both refer to the brand; >= 20 windows per group."""
    j1p = S.provider_of(j1_model)
    own, other = [], []
    for r in w5.rows:
        if (r["category"], r["brand"]) in excl:
            continue
        a, b = r[role1], r[role2]
        if a["status"] != VALID or b["status"] != VALID or not (a["refers"] and b["refers"]):
            continue
        d = S.unit_score(a["valence"]) - S.unit_score(b["valence"])
        (own if r["provider"] == j1p else other).append(d)
    delta = float(np.mean(own)) - float(np.mean(other)) if own and other else NAN
    return {"delta_points": delta, "n_own_provider": len(own), "n_other": len(other), "j1_provider": j1p,
            "mean_diff_own": float(np.mean(own)) if own else None,
            "mean_diff_other": float(np.mean(other)) if other else None,
            "verdict": S.self_pref_verdict(delta, len(own), len(other))}


def n_named_t5(w5: Wave, misses: Optional[Dict[Tuple[str, str], int]] = None) -> Dict[Tuple[str, str], float]:
    """n_named (H6_t5, MQ6): t5 S0 answers naming the brand. READING (6, H6): the certified record's count,
    i.e. answers with a window for the brand in the t5 unit table (every judged window, any outcome) plus the
    U0 extraction misses for that brand when supplied (v1.11 counts named answers from the certified record)."""
    acc: Dict[tuple, set] = defaultdict(set)
    for r in w5.rows:
        acc[(r["category"], r["brand"])].add(r["answer_id"])
    out = {k: float(len(v)) for k, v in acc.items()}
    for k, n in (misses or {}).items():
        out[k] = out.get(k, 0.0) + float(n)
    return out


def apply_noise_guard(v: Dict[str, str]) -> Tuple[Dict[str, str], bool]:
    """Section 6: if H1_t5 or H4 is FALSIFIED, H2_t5, H3_t5 and H5_t4 are reported as UNDETERMINED."""
    on = v.get("H1_t5") == "FALSIFIED" or v.get("H4") == "FALSIFIED"
    out = dict(v)
    if on:
        for h in NOISE_GUARDED:
            if h in out:
                out[h] = "UNDETERMINED"
    return out, on


def gate(v: Dict[str, str]) -> str:
    """Section 8: FAIL if any of H1_t5, H2_t5, H3_t5, H4 is FALSIFIED; else UNDETERMINED if any of them is
    UNDETERMINED; else PASS if all four are CONFIRMED and H5_t4 is not FALSIFIED; else MARGINAL.
    READING (8): H5_t4 UNDETERMINED or MARGINAL does not downgrade a PASS (only 'not FALSIFIED' is required)."""
    four = [v[h] for h in GATE_ROWS]
    if "FALSIFIED" in four:
        return "FAIL"
    if "UNDETERMINED" in four:
        return "UNDETERMINED"
    if all(x == "CONFIRMED" for x in four):
        return "MARGINAL" if v.get("H5_t4") == "FALSIFIED" else "PASS"
    return "MARGINAL"


def consequence(g: str) -> str:
    return CONSEQUENCE_PASS if g == "PASS" else CONSEQUENCE_NOT_PASS


def precision_table(n: int) -> dict:
    """Section 7: P(|rho_hat| <= 0.30) for one wave at the realised n, Fisher z with the Bonett-Wright variance
    (1 + rho^2 / 2) / (n - 3). Written into the Stage J output before P is opened."""
    if n <= 3:
        return {"n": n, "P_abs_rho_le_0.30": None}
    z30 = math.atanh(BAND_CONF)
    phi = lambda z: 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))  # noqa: E731
    tab = {}
    for r in PRECISION_TRUE_RHO:
        se = math.sqrt((1.0 + r * r / 2.0) / (n - 3))
        zr = math.atanh(r)
        tab[f"{r:.2f}"] = phi((z30 - zr) / se) - phi((-z30 - zr) / se)
    return {"n": n, "true_rho": list(PRECISION_TRUE_RHO), "P_abs_rho_le_0.30": tab,
            "method": "Fisher z, Bonett-Wright variance (1 + rho^2/2)/(n - 3)"}


# ======================================================================================
# 5. CHECKS (section 9) AND DESCRIPTIVES (section 10)
# ======================================================================================
def judge_fail_check(waves: Dict[str, Wave]) -> dict:
    """JUDGE_FAIL share per wave x category x judge among windows sent (VALID + JUDGE_FAIL), under the v1.20 rule;
    above 2% halts before scoring. READING (5, 9): applied to both scored waves (t5 and the re-scored t4)."""
    out, halt = {}, []
    for wn, w in sorted(waves.items()):
        for role in ("J1", "J2"):
            for cat in w.cats:
                c = Counter(r[role]["status"] for r in w.by_cat[cat])
                sent = c[VALID] + c[FAIL]
                share = c[FAIL] / sent if sent else 0.0
                key = f"{wn} {role} {cat}"
                out[key] = {"valid": c[VALID], "judge_fail": c[FAIL], "unjudged": c[UNJUDGED], "fail_share": share}
                if share > JUDGE_FAIL_HALT_SHARE:
                    halt.append(key)
    return {"per_wave_judge_category": out, "halt": halt, "threshold": JUDGE_FAIL_HALT_SHARE}


def u0_miss_check(mentions: Dict[str, int], misses: Dict[str, int]) -> dict:
    """U0 (section 9): extraction misses <= 5% of a category's certified mentions, else halt before any judge
    call. {category: count}. Provided for the U0 step; the scorer re-applies it when U0 counts are supplied."""
    per, halt = {}, []
    for cat in sorted(mentions):
        n = mentions[cat]
        share = misses.get(cat, 0) / n if n else 0.0
        per[cat] = {"mentions": n, "misses": misses.get(cat, 0), "share": share}
        if share > EXTRACTION_MISS_HALT_SHARE:
            halt.append(cat)
    return {"per_category": per, "halt": halt, "threshold": EXTRACTION_MISS_HALT_SHARE}


def mq9(w: Wave, floor: int = FLOOR) -> dict:
    """MQ9: units at the floor (>= floor contributing answers) outside the main comparison component."""
    at, out_main = 0, []
    for cat, c in w.comps().items():
        mc = c.main_component()
        for b, i in c.idx.items():
            if c.n_contrib[i] >= floor:
                at += 1
                if not mc[i]:
                    out_main.append(f"{cat}|{b}")
    share = len(out_main) / at if at else 0.0
    return {"units_at_floor": at, "outside_main_component": len(out_main), "units": out_main, "share": share,
            "flag": share > MQ9_MAX_SHARE}


def selfcon(w: Wave) -> dict:
    """Self-consistency (v1.11's 5% repeat sample): exact valence agreement main vs repeat; flag below 0.90."""
    out = {}
    for role in ("J1", "J2"):
        ps = [(r[role]["valence"], r[f"{role}rep"]["valence"]) for r in w.rows
              if r[f"{role}rep"]["status"] == VALID and r[role]["status"] == VALID]
        if not ps:
            out[role] = {"n": 0}
            continue
        exact = sum(a == b for a, b in ps) / len(ps)
        out[role] = {"n": len(ps), "exact_valence_agreement": exact,
                     "alpha_ordinal": S.krippendorff_alpha_ordinal(ps) if len(ps) >= 2 else None,
                     "flag_below_0.90": exact < SELFCON_MIN_EXACT}
    return out


def _dist(vals) -> Optional[dict]:
    v = np.asarray([x for x in vals if x is not None and math.isfinite(x)], float)
    if not len(v):
        return None
    return {"n": int(len(v)), "median": float(np.median(v)), "q25": float(np.quantile(v, .25)),
            "q75": float(np.quantile(v, .75)), "min": float(v.min()), "max": float(v.max())}


def descriptives_j(w: Wave) -> dict:
    """Pairs per category, tied share, answers with >= 2 valid brands, rated units, TONE distribution per
    category, mean u by answering model (J1)."""
    T = measure(w, "TONE")
    per = {}
    for cat, c in w.comps().items():
        per[cat] = {"answers_with_valid_window": c.n_answers, "answers_ge2_valid_brands": c.n_answers_ge2,
                    "pairs": int(len(c.ra)), "tied_pair_share": c.tied_share(), "brands": len(c.brands),
                    "rated_TONE": sum(1 for (k, b), v in T.items() if k == cat and v["rated"]),
                    "TONE": _dist([v["value"] for (k, b), v in T.items() if k == cat and v["rated"]])}
    acc: Dict[str, list] = defaultdict(list)
    for r in w.rows:
        if r["J1"]["status"] == VALID and r["J1"]["refers"]:
            acc[r["model"]].append(S.unit_score(r["J1"]["valence"]))
    return {"per_category": per,
            "mean_u_by_model_J1": {m: {"n": len(v), "mean_u": float(np.mean(v))} for m, v in sorted(acc.items())}}


def _ser(U: Dict[tuple, dict]) -> Dict[str, dict]:
    return {f"{k[0]}|{k[1]}": v for k, v in sorted(U.items())}


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        f = float(o)
        return f if math.isfinite(f) else None
    return o


def flatten_values(doc, prefix: str = "") -> Dict[str, object]:
    """values_v1_21.json: every scalar of the verdicts file under its dotted path (every number a paper uses is
    a value written by the scorer)."""
    out: Dict[str, object] = {}
    if isinstance(doc, dict):
        for k, v in doc.items():
            out.update(flatten_values(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(doc, list):
        for i, v in enumerate(doc):
            out.update(flatten_values(v, f"{prefix}[{i}]"))
    else:
        out[prefix] = doc
    return out


# ======================================================================================
# 6. STAGE J (section 13 step 6: judge gate and measure values; reads no P, C* or R*)
# ======================================================================================
def stage_j_core(waves: Dict[str, Wave], roles: Dict[str, str], draws: Draws, extra: Optional[dict] = None) -> dict:
    jf = judge_fail_check(waves)
    if jf["halt"]:
        raise Halt(f"JUDGE_FAIL above 2% (section 9): {jf['halt']}")
    vals: Dict[str, dict] = {}
    sref_check = {}
    for wn in WAVES:
        w = waves[wn]
        vals[wn] = {"TONE": _ser(measure(w, "TONE")), "TONE_J2": _ser(measure(w, "TONE", role="J2")),
                    "TONE_NV": _ser(measure(w, "TONE_NV")), "CONTRAST": _ser(measure(w, "CONTRAST")),
                    "S_ref": _ser(measure(w, "S_ref")), "S_cat": _ser(measure(w, "S_cat"))}
        a, b = measure(w, "S_ref"), s_ref_v111(w)
        bad = [k for k in sorted(set(a) | set(b))
               if bool(a.get(k, {}).get("rated")) != bool(b.get(k, {}).get("rated"))
               or (a.get(k, {}).get("rated") and abs(a[k]["value"] - b[k]["value"]) > 1e-9)]
        sref_check[wn] = {"matches_v1_11_brand_score": not bad, "differences": [f"{k[0]}|{k[1]}" for k in bad]}
        if bad:
            raise Halt(f"S_ref differs from v1.11's brand_score at {wn}: {bad[:3]} (scorer bug)")
    T5 = measure(waves["t5"], "TONE")
    g = np.asarray([k[0] for k, v in sorted(T5.items()) if v["rated"]])
    n_rated = int(V.keep_categories(g, MIN_UNITS_PER_GROUP).sum()) if len(g) else 0
    return {"phase": PHASE_ID, "stage": "J", "status": STATUS, "prereg": PREREG_REL, "prereg_tag": PREREG_TAG,
            "created_utc": _now(), "roles": roles, "seeds": SEEDS, "draws": draws.as_dict(),
            "rule": "v1.20 extraction rule (score_v1_20.outcomes, config_v1_20.json)",
            "JUDGE_FAIL_check": jf, "S_ref_vs_v1_11_brand_score": sref_check,
            "H1_t5_Judge_Agreement": h1_t5(waves["t5"], draws),
            "self_consistency": {wn: selfcon(waves[wn]) for wn in WAVES},
            "precision_at_realised_n": precision_table(n_rated),
            "MQ9_identification": {wn: mq9(waves[wn]) for wn in WAVES},
            "descriptives": {wn: descriptives_j(waves[wn]) for wn in WAVES},
            "values": vals, **(extra or {})}


# ======================================================================================
# 7. STAGE C (sections 6-8, 10): opens P and C*
# ======================================================================================
PRIMARY = {"role": "J1", "h1_roles": ("J1", "J2"), "weighting": "pairs", "prior": PRIOR, "floor": FLOOR,
           "excl": frozenset(), "uncentred": False, "h1": "compute"}


def gate_bundle(waves: Dict[str, Wave], P: Dict[str, dict], C: Dict[str, dict], draws: Draws, variant: dict,
                h1_primary: Optional[dict] = None) -> dict:
    """The gate statistics (H1_t5, H2_t5, H3_t5, H4, H5_t4), the noise guard and the gate under one variant
    (the primary analysis or one sensitivity of section 10)."""
    v = {**PRIMARY, **variant}

    def run() -> dict:
        c4 = waves["t4"].comps(v["role"], v["weighting"])
        c5 = waves["t5"].comps(v["role"], v["weighting"])
        T4 = wave_values(c4, "TONE", v["floor"], v["prior"])
        T5 = wave_values(c5, "TONE", v["floor"], v["prior"])
        if v["h1"] == "primary":
            h1 = h1_primary
        else:
            h1 = h1_t5(waves["t5"], draws, v["excl"], v["h1_roles"][0], v["h1_roles"][1], v["floor"], v["prior"],
                       v["weighting"])
        return {"H1_t5_Judge_Agreement": h1,
                "H2_t5_Sep_Presence": sep(T5, P["t5"], draws, v["excl"]),
                "H3_t5_Sep_Consistency": sep(T5, C["t5"], draws, v["excl"]),
                "H4_Retest_t4_t5": retest(c4, c5, "TONE", draws, v["floor"], v["prior"], v["excl"]),
                "H5_t4_Sep_Presence": sep(T4, P["t4"], draws, v["excl"])}

    if v["uncentred"]:
        with V.uncentred():
            res = run()
    else:
        res = run()
    raw = {"H1_t5": res["H1_t5_Judge_Agreement"]["verdict"], "H2_t5": res["H2_t5_Sep_Presence"]["verdict"],
           "H3_t5": res["H3_t5_Sep_Consistency"]["verdict"], "H4": res["H4_Retest_t4_t5"]["verdict"],
           "H5_t4": res["H5_t4_Sep_Presence"]["verdict"]}
    final, on = apply_noise_guard(raw)
    res.update({"verdicts_before_noise_guard": raw, "verdicts": final, "noise_guard_applied": on,
                "GATE": gate(final)})
    return res


def sensitivity_variants() -> Dict[str, dict]:
    """Section 10. READING (10, SD / S-COI): the excluded brands leave every correlation (and H1's alpha
    windows) but stay in the Bradley-Terry fits as rivals (v1.16's excl_units handling; TONE is not refitted).
    READING (10, TONE_J2): TONE refitted on J2's unit scores for H2-H5; H1_t5 is the primary's (it already
    compares the two judges). READING (10, S_floor): the floor of TONE's rating rule only."""
    out = {"SD_without_Denon": {"excl": frozenset([DENON])},
           "S-COI_without_Denon_and_five_agency_brands": {"excl": frozenset(COI)},
           "SU_uncentred_ranks": {"uncentred": True},
           "S_w_pair_weight_1_over_k_minus_1": {"weighting": "per_answer"}}
    for p in PRIOR_SENS:
        out[f"S_prior_lambda_{p:g}"] = {"prior": p}
    for f in FLOOR_SENS:
        out[f"S_floor_{f}"] = {"floor": f}
    out["TONE_J2"] = {"role": "J2", "h1": "primary"}
    out["S-ATT_v1_11_first_attempt_rule"] = {"role": "J1att", "h1_roles": ("J1att", "J2att")}
    return out


def s_res(waves: Dict[str, Wave], P: Dict[str, dict]) -> Tuple[Dict[tuple, dict], dict]:
    """S_res (section 3.4): per category, intercept and slope of S_ref on P_S0 fitted by least squares on the
    t4 units rated on S_ref with P; applied at t5: S_res = S_ref_t5 - (a_c + b_c P_t5). READING (3.4): a category
    whose t4 fit has < 2 units or no spread in P has no S_res (counted)."""
    S4, S5 = measure(waves["t4"], "S_ref"), measure(waves["t5"], "S_ref")
    fits, out = {}, {}
    for cat in sorted({k[0] for k in S4}):
        ks = [k for k in sorted(S4) if k[0] == cat and S4[k]["rated"] and P["t4"].get(k) is not None
              and math.isfinite(P["t4"][k])]
        x = np.array([P["t4"][k] for k in ks], float)
        y = np.array([S4[k]["value"] for k in ks], float)
        if len(ks) < 2 or float(np.var(x)) == 0.0:
            fits[cat] = {"n_t4": len(ks), "fitted": False}
            continue
        b = float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())
        a = float(y.mean() - b * x.mean())
        fits[cat] = {"n_t4": len(ks), "fitted": True, "intercept": a, "slope": b}
    for k, v in S5.items():
        f = fits.get(k[0])
        p5 = P["t5"].get(k)
        ok = v["rated"] and f and f["fitted"] and p5 is not None and math.isfinite(p5)
        out[k] = {"value": v["value"] - (f["intercept"] + f["slope"] * p5) if ok else None, "rated": bool(ok)}
    return out, fits


def _same(a: float, b: float) -> bool:
    if a is None or b is None:
        return a is None and b is None
    if not (math.isfinite(a) and math.isfinite(b)):
        return not math.isfinite(a) and not math.isfinite(b)
    return abs(a - b) <= 1e-12


def stage_c_core(waves: Dict[str, Wave], P: Dict[str, dict], C: Dict[str, dict], roles: Dict[str, str],
                 draws: Draws, stage_j: dict, misses: Optional[dict] = None, rank_t5: Optional[dict] = None,
                 v120_h2: Optional[dict] = None, sensitivities: bool = True) -> dict:
    w4, w5 = waves["t4"], waves["t5"]
    h1p = stage_j["H1_t5_Judge_Agreement"]
    prim = gate_bundle(waves, P, C, draws, {"h1": "primary"}, h1_primary=h1p)   # H1_t5 as written at Stage J
    T5 = measure(w5, "TONE")
    nn = n_named_t5(w5, misses)
    h6 = sep(T5, nn, draws)
    h7 = h7_t5(w5, roles["J1"])
    verdicts = {**prim["verdicts"], "H6_t5": h6["verdict"], "H7_t5": h7["verdict"]}
    # --- secondaries (section 3.4): H2_t5, H3_t5 and H4 for each; S_res has no t4 value, so no H4 ---
    sec = {}
    for kind in ("CONTRAST", "S_ref", "S_cat", "TONE_NV"):
        nv = kind == "TONE_NV"
        U5 = measure(w5, kind)
        sec[kind] = {"H2_t5": sep(U5, P["t5"], draws), "H3_t5": sep(U5, C["t5"], draws),
                     "H4": retest(w4.comps("J1", "pairs", nv), w5.comps("J1", "pairs", nv), kind, draws)}
    SR, fits = s_res(waves, P)
    sec["S_res"] = {"H2_t5": sep(SR, P["t5"], draws), "H3_t5": sep(SR, C["t5"], draws),
                    "H4": "not defined: S_res exists at t5 only (coefficients fitted at t4)", "t4_fits": fits}
    # --- identity check (section 9): S_cat's rho_w equals S_ref's on every row; halt otherwise ---
    ident = {row: (sec["S_cat"][row]["rho"], sec["S_ref"][row]["rho"]) for row in ("H2_t5", "H3_t5", "H4")}
    ident_ok = all(_same(a, b) for a, b in ident.values())
    if not ident_ok:
        raise Halt(f"Identity check failed: S_cat vs S_ref rho_w {ident} (scorer bug)")
    # --- checks ---
    mq6 = sep({k: {"value": v, "rated": True} for k, v in nn.items()}, P["t5"], draws)
    mq6.pop("verdict", None)
    mq7_mean = prim["H4_Retest_t4_t5"].get("shuffled_mean_rho")
    mq7 = {"shuffled_mean_rho": mq7_mean, "threshold": MQ7_MAX,
           "flag_list_composition_driven": bool(mq7_mean is not None and math.isfinite(mq7_mean) and mq7_mean >= MQ7_MAX)}
    # --- sensitivities (section 10): never change a verdict ---
    sens, changes = {}, []
    if sensitivities:
        for name, var in sensitivity_variants().items():
            b = gate_bundle(waves, P, C, draws, var, h1_primary=h1p)
            sens[name] = b
            for h, val in {**b["verdicts"], "GATE": b["GATE"]}.items():
                pv = prim["GATE"] if h == "GATE" else prim["verdicts"][h]
                if val != pv:
                    changes.append({"sensitivity": name, "hypothesis": h, "primary": pv, "under_sensitivity": val})
    # --- descriptives (section 10) ---
    desc = {"R_star_t5": None}
    if rank_t5 is not None:
        r = sep(T5, rank_t5, draws)
        r.pop("verdict", None)
        desc["R_star_t5"] = {"rho_w_TONE_vs_modal_position": r, "role": "descriptive only (section 4.3)"}
    else:
        desc["R_star_t5"] = "v1.14 Stage 2's t5 rank table not supplied"
    s_ref_rep = {"S_ref_H2_t5": sec["S_ref"]["H2_t5"], "v1_20_H2_per_wave": v120_h2}
    return {"phase": PHASE_ID, "stage": "C", "status": STATUS, "prereg": PREREG_REL, "prereg_tag": PREREG_TAG,
            "created_utc": _now(), "roles": roles, "seeds": SEEDS, "draws": draws.as_dict(),
            "bands": {"CONFIRMED_max_abs_rho": BAND_CONF, "FALSIFIED_min_abs_rho": BAND_FALS},
            "VERDICTS": verdicts, "verdicts_before_noise_guard": prim["verdicts_before_noise_guard"],
            "noise_guard_applied": prim["noise_guard_applied"], "GATE": prim["GATE"],
            "CONSEQUENCE": consequence(prim["GATE"]),
            **{k: prim[k] for k in ("H1_t5_Judge_Agreement", "H2_t5_Sep_Presence", "H3_t5_Sep_Consistency",
                                    "H4_Retest_t4_t5", "H5_t4_Sep_Presence")},
            "H6_t5_Naming_Frequency": h6, "H7_t5_Self_Preference": h7,
            "secondaries": sec, "S_ref_replication_of_v1_20_H2": s_ref_rep,
            "checks": {"Identity_S_cat_equals_S_ref": {"passes": ident_ok, "rho_pairs": ident},
                       "MQ6_positive_control_rho_w_n_named_P_S0_t5": mq6, "MQ7_negative_control": mq7,
                       "MQ9_identification": stage_j.get("MQ9_identification")},
            "sensitivities": sens, "sensitivity_verdict_changes": changes,
            "sensitivity_note": "A sensitivity never changes a verdict or the gate (section 10).",
            "descriptives": desc}


# ======================================================================================
# 8. INPUTS, PINS, LOCK STATUS, FILE STAGES
# ======================================================================================
def verify_code_pins(root: Path = ROOT) -> Dict[str, str]:
    got = {}
    for rel, want in CODE_PINS.items():
        p = Path(root) / rel
        if not p.exists():
            raise Halt(f"Pins: missing {rel}")
        h = sha256_file(p)
        if h != want:
            raise Halt(f"Pins: {rel} changed (sha256 {h[:12]}..., pinned {want[:12]}...)")
        got[rel] = h
    got[f"{V116_TAG}:{V116_PATH} (git blob)"] = V116_BLOB
    return got


def tag_exists(tag: str = PREREG_TAG, root: Path = ROOT) -> bool:
    r = subprocess.run(["git", "-C", str(root), "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
                       capture_output=True)
    return r.returncode == 0


def _read_csv(p: Path) -> List[dict]:
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# READING (4.1, 4.2, 18): the t5 U0 unit table and judge record are named after v1.15's files (the draft names
# U0 and the judge run but not their files): <t5 dir>/prereg/units_v1_21.csv, outputs/judge_outputs_frozen_v1_21.json,
# data/judge_raw_v1_21.jsonl, in v1.11's unit and record formats.
WAVE_FILES = {"t4": ("prereg/units_v1_15.csv", "outputs/judge_outputs_frozen_v1_15.json", "data/judge_raw_v1_15.jsonl"),
              "t5": ("prereg/units_v1_21.csv", "outputs/judge_outputs_frozen_v1_21.json", "data/judge_raw_v1_21.jsonl")}


def load_wave_dir(d: Path, wave: str) -> Tuple[List[dict], Dict[str, str], dict]:
    units_rel, frozen_rel, raw_rel = WAVE_FILES[wave]
    frozen_p, raw_p, units_p = Path(d) / frozen_rel, Path(d) / raw_rel, Path(d) / units_rel
    for p in (frozen_p, raw_p, units_p):
        if not p.exists():
            raise Halt(f"{wave}: missing {p}")
    frozen = json.loads(frozen_p.read_text(encoding="utf-8"))
    raw_sha, units_sha = sha256_file(raw_p), sha256_file(units_p)
    if raw_sha != frozen["raw_sha256"]:
        raise Halt(f"{wave}: judge raw file differs from its frozen hash")
    if units_sha != frozen["units_sha256"]:
        raise Halt(f"{wave}: unit table differs from the frozen record's units_sha256")
    if wave == "t4" and (raw_sha != T4_PINS["raw_sha256"] or units_sha != T4_PINS["units_sha256"]
                         or frozen["roles"] != T4_PINS["roles"]):
        raise Halt("t4: v1.15's frozen files do not match the pins of section 4.1")
    recs = [json.loads(x) for x in raw_p.read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = build_unit_rows(_read_csv(units_p), recs, frozen["roles"], wave)
    info = {"dir": str(d), "frozen_sha256": sha256_file(frozen_p), "raw_sha256": raw_sha, "units_sha256": units_sha,
            "records": len(recs), "served_models": dict(Counter(str(r.get("served_model")) for r in recs)),
            "finish_reasons": dict(Counter(str(r.get("finish_reason")) for r in recs))}
    return rows, frozen["roles"], info


def presence_t4(stage1: Path) -> Tuple[dict, dict, str]:
    """t4 P_S0 and C*_S0: v1.14 Stage 1's units[] (section 4.3), pinned."""
    h = sha256_file(stage1)
    if h != T4_PINS["stage1_sha256"]:
        raise Halt("Pins: stage1_v1_14.json differs from its pin")
    P, C = {}, {}
    for u in json.loads(Path(stage1).read_text(encoding="utf-8"))["units"]:
        k = (u["substrate"], u["brand"])
        if u.get("P_S0") is not None:
            P[k] = float(u["P_S0"])
        if u.get("C_star_S0") is not None:
            C[k] = float(u["C_star_S0"])
    return P, C, h


def presence_t5(table: Path) -> Tuple[dict, dict, str]:
    """t5 P_S0 and C*_S0 from v0.45's scored unit table (osf/v45/v45_unit_table.csv; section 4.3).
    READING (4.3): v0.45 writes P_t5_S0 and phi_t5_S0 / phi_partition_t5_S0, not a C* column; C* is
    v0.45's own transform 100 (1 - phi / 9) for 'defined', 100 for 'saturated', missing otherwise
    (score_v0_45.h_stab_consistency, C_star_alongside), with no C* rating floor applied."""
    P, C = {}, {}
    for r in _read_csv(table):
        k = (r["substrate"], r["brand"])
        if (r.get("P_t5_S0") or "").strip() not in ("", "None", "nan"):
            P[k] = float(r["P_t5_S0"])
        part = (r.get("phi_partition_t5_S0") or "").strip()
        if part == "defined":
            C[k] = 100.0 * (1.0 - float(r["phi_t5_S0"]) / 9.0)
        elif part == "saturated":
            C[k] = 100.0
    return P, C, sha256_file(table)


def v120_h2(root: Path = ROOT) -> Optional[dict]:
    p = Path(root) / V120_VERDICTS_REL
    if not p.exists():
        return None
    d = json.loads(p.read_text(encoding="utf-8"))["H2_Sep_Presence"]
    return {"file": V120_VERDICTS_REL, "sha256": sha256_file(p), "verdict": d["verdict"],
            "per_wave": {w: {"rho": v["rho"], "n": v["n"]} for w, v in d["per_wave"].items()}}


def _write_json(p: Path, doc: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(_clean(doc), indent=2, ensure_ascii=False, sort_keys=False) + "\n", encoding="utf-8")


def write_stage_j(out: Path, rows: Dict[str, List[dict]], doc_fn: Callable[[Dict[str, Wave]], dict]) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    shas = {}
    for wn in WAVES:
        b = unit_rows_csv_bytes(rows[wn])
        (out / OUTCOMES_NAME[wn]).write_bytes(b)
        shas[wn] = sha256_bytes(b)
    waves = {wn: Wave(wn, parse_unit_rows((out / OUTCOMES_NAME[wn]).read_text(encoding="utf-8"))) for wn in WAVES}
    doc = doc_fn(waves)
    doc["unit_outcomes_sha256"] = shas
    _write_json(out / STAGE_J_NAME, doc)
    return doc


def read_stage_j(out: Path) -> Tuple[dict, Dict[str, Wave]]:
    p = out / STAGE_J_NAME
    if not p.exists():
        raise Halt("ORDER: Stage J must be written before P or C* are opened (section 13)")
    sj = json.loads(p.read_text(encoding="utf-8"))
    waves = {}
    for wn in WAVES:
        q = out / OUTCOMES_NAME[wn]
        if sha256_file(q) != sj["unit_outcomes_sha256"][wn]:
            raise Halt(f"unit outcomes of {wn} changed since Stage J")
        waves[wn] = Wave(wn, parse_unit_rows(q.read_text(encoding="utf-8")))
    return sj, waves


def run_stage_j(out: Path, t4_dir: Path, t5_dir: Path, draws: Draws, log=print) -> dict:
    if not tag_exists():
        raise Halt(f"REFUSED: {PREREG_TAG} does not exist (score only after the lock)")
    if (out / STAGE_J_NAME).exists():
        raise Halt("REFUSED: Stage J has run once already")
    pins = verify_code_pins()
    r4, roles4, i4 = load_wave_dir(t4_dir, "t4")
    r5, roles5, i5 = load_wave_dir(t5_dir, "t5")
    doc = write_stage_j(out, {"t4": r4, "t5": r5},
                        lambda ws: stage_j_core(ws, roles5, draws, {"roles_t4": roles4, "pins": pins,
                                                                    "inputs": {"t4": i4, "t5": i5}}))
    log(f"[v1.21] Stage J: H1_t5 {doc['H1_t5_Judge_Agreement']['verdict']}")
    return doc


def run_stage_c(out: Path, t4_stage1: Path, t5_presence: Path, draws: Draws, rank_t5: Optional[Path] = None,
                log=print) -> dict:
    if not tag_exists():
        raise Halt(f"REFUSED: {PREREG_TAG} does not exist (score only after the lock)")
    if (out / VERDICTS_NAME).exists():
        raise Halt("REFUSED: Stage C has run once already")
    verify_code_pins()
    sj, waves = read_stage_j(out)
    P4, C4, h4 = presence_t4(t4_stage1)          # first read of P and C* (section 4.3, opening order)
    P5, C5, h5 = presence_t5(t5_presence)
    R5 = None
    if rank_t5 is not None:
        R5 = {(r["category"], r["brand"]): float(r["R_star"]) for r in _read_csv(rank_t5) if r.get("R_star")}
    doc = stage_c_core(waves, {"t4": P4, "t5": P5}, {"t4": C4, "t5": C5}, sj["roles"], draws, sj,
                       rank_t5=R5, v120_h2=v120_h2())
    doc["inputs"] = {"stage_j_sha256": sha256_file(out / STAGE_J_NAME), "t4_stage1_sha256": h4,
                     "t5_presence_sha256": h5, "t5_rank_table": str(rank_t5) if rank_t5 else None}
    _write_json(out / VERDICTS_NAME, doc)
    _write_json(out / VALUES_NAME, flatten_values(_clean(doc)))
    log(f"[v1.21] Stage C: {doc['VERDICTS']} GATE {doc['GATE']}")
    return doc


# ======================================================================================
# 9. SYNTHETIC FIXTURES (tests, dry run): FIXTURE_DIR/{fixture.json, unit_outcomes_t4.csv,
#    unit_outcomes_t5.csv, presence.csv (wave, category, brand, P_S0, C_star_S0)}
# ======================================================================================
def read_fixture(d: Path) -> Tuple[dict, Dict[str, List[dict]], dict, dict]:
    d = Path(d)
    meta = json.loads((d / "fixture.json").read_text(encoding="utf-8"))
    rows = {wn: parse_unit_rows((d / f"unit_outcomes_{wn}.csv").read_text(encoding="utf-8")) for wn in WAVES}
    P: Dict[str, dict] = {wn: {} for wn in WAVES}
    C: Dict[str, dict] = {wn: {} for wn in WAVES}
    for r in _read_csv(d / "presence.csv"):
        k = (r["category"], r["brand"])
        if r["P_S0"] != "":
            P[r["wave"]][k] = float(r["P_S0"])
        if r["C_star_S0"] != "":
            C[r["wave"]][k] = float(r["C_star_S0"])
    return meta, rows, P, C


def run_fixture(d: Path, out: Path, draws: Draws, sensitivities: bool = True) -> Tuple[dict, dict]:
    """Stage J then Stage C on a synthetic fixture, through the same files as a real run (no lock check)."""
    meta, rows, P, C = read_fixture(d)
    roles = meta["roles"]
    sj_doc = write_stage_j(Path(out), rows, lambda ws: stage_j_core(ws, roles, draws, {"fixture": meta.get("name")}))
    sj, waves = read_stage_j(Path(out))
    assert sj["unit_outcomes_sha256"] == sj_doc["unit_outcomes_sha256"]
    doc = stage_c_core(waves, P, C, roles, draws, sj, sensitivities=sensitivities)
    doc["fixture"] = meta.get("name")
    _write_json(Path(out) / VERDICTS_NAME, doc)
    _write_json(Path(out) / VALUES_NAME, flatten_values(_clean(doc)))
    return sj, doc


# ======================================================================================
# 10. EXPLORATORY RQ3 (section 10): t1-t3, only after the lock is anchored
# ======================================================================================
V120_OUTCOMES_REL = "osf/methodology/v1_20/outputs/unit_outcomes_v1_20.csv"
V111_UNITS_REL = "osf/methodology/v1_11/prereg/units_v1_11.csv"
PROFILES_REL = "osf/aias_2_0/aias_2_0_profiles.csv"


def exploratory_core(waves: Dict[str, Wave], P: Dict[str, dict], C: Dict[str, dict], draws: Draws,
                     v120: Optional[dict] = None) -> dict:
    """TONE and CONTRAST per legacy wave and their rho_w with P and C*; described, never tested (no verdict)."""
    out = {}
    for wn in sorted(waves):
        row = {}
        for kind in ("TONE", "CONTRAST"):
            U = measure(waves[wn], kind)
            a = sep(U, P.get(wn, {}), draws) if P.get(wn) else None
            b = sep(U, C.get(wn, {}), draws) if C.get(wn) else None
            for r in (a, b):
                if r:
                    r.pop("verdict", None)
            row[kind] = {"rated": sum(v["rated"] for v in U.values()), "rho_w_with_P": a, "rho_w_with_C_star": b}
        out[wn] = row
    return {"label": "EXPLORATORY (RQ3): described, never tested, never used to choose between measures",
            "per_wave": out, "v1_20_S_values": v120}


def run_exploratory(out: Path, draws: Draws, root: Path = ROOT, log=print) -> dict:
    if not (tag_exists() and ANCHOR_FILE.exists()):
        raise Halt("REFUSED: the exploratory t1-t3 analysis runs only after the lock is anchored (section 10)")
    if (out / EXPLORATORY_NAME).exists():
        raise Halt("REFUSED: the exploratory analysis has run once already")
    aid = {r["unit_id"]: r["answer_id"] for r in _read_csv(root / V111_UNITS_REL)}
    by_wave: Dict[str, List[dict]] = defaultdict(list)
    eblock: Dict[str, List[dict]] = defaultdict(list)
    for r in _read_csv(root / V120_OUTCOMES_REL):
        if r["block"] not in ("F", "E"):
            continue
        row = {"unit_id": r["unit_id"], "wave": r["wave"], "category": r["category"], "brand": r["brand"],
               "answer_id": aid[r["unit_id"]], "model": r["model"], "provider": r["provider"]}
        for role in ("J1", "J2"):
            st = r[f"{role}_status"] or UNJUDGED
            row[role] = {"status": st, "valence": int(r[f"{role}_valence"]) if st == VALID else None,
                         "evaluative": _b(r[f"{role}_evaluative"]) if st == VALID else False,
                         "refers": _b(r[f"{role}_refers"]) if st == VALID else False}
        if r["block"] == "F":
            by_wave[r["wave"]].append(row)
        else:
            row["wave"] = "E"
            eblock["E"].append(row)
    P, Cc, _nm = V.parse_profiles(_read_csv(root / PROFILES_REL))
    waves = {w: Wave(w, rs) for w, rs in sorted(by_wave.items())}
    doc = exploratory_core(waves, {w: P.get(w, {}) for w in waves}, {w: Cc.get(w, {}) for w in waves}, draws,
                           {"H2": (v120_h2(root) or {}).get("per_wave")})
    # READING (10): for the eight early categories (E block) there is no P or C*; their TONE and CONTRAST
    # values are described only.
    if eblock:
        ew = Wave("E", eblock["E"])
        doc["E_block_values"] = {k: _ser(measure(ew, k)) for k in ("TONE", "CONTRAST")}
    doc.update({"phase": PHASE_ID, "created_utc": _now(), "draws": draws.as_dict(), "seeds": SEEDS})
    _write_json(out / EXPLORATORY_NAME, doc)
    log("[v1.21] exploratory t1-t3 written")
    return doc


# ======================================================================================
# 11. LOCK MANIFEST (section 13 step 1, last; v1.20 / v1.11 format: '<sha256>  <path>' per line)
# ======================================================================================
def lock_files(root: Path = ROOT) -> List[str]:
    tests = sorted(str(p.relative_to(root)) for p in (root / V121 / "tests").rglob("*")
                   if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    return ([PREREG_REL, V121 + "/scripts/score_v1_21.py"] + tests + list(CODE_PINS))


def lock_manifest_text(root: Path = ROOT) -> str:
    return "".join(f"{sha256_file(root / f)}  {f}\n" for f in lock_files(root))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="AIAS v1.21 scorer (DRAFT)")
    ap.add_argument("--stage", choices=("J", "C"))
    ap.add_argument("--t4-dir", type=Path, help="Stage J: v1.15's study folder (osf/methodology/v1_15 of a v1.15 worktree)")
    ap.add_argument("--t5-dir", type=Path, help="Stage J: v1.21's t5 U0 + judge-record folder")
    ap.add_argument("--t4-stage1", type=Path, help="Stage C: osf/methodology/v1_14/outputs/stage1/stage1_v1_14.json")
    ap.add_argument("--t5-presence", type=Path, help="Stage C: osf/v45/v45_unit_table.csv")
    ap.add_argument("--t5-rank", type=Path, help="Stage C, optional: v1.14 Stage 2's t5 table (category, brand, R_star)")
    ap.add_argument("--exploratory", action="store_true")
    ap.add_argument("--fixture", type=Path)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--draws", type=int, help="fixtures / dry run only: perm, shuffle and bootstrap draws")
    ap.add_argument("--lock-manifest", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.lock_manifest:
            sys.stdout.write(lock_manifest_text())
            return 0
        if a.fixture:
            d = Draws(a.draws, a.draws, a.draws) if a.draws else Draws()
            sj, doc = run_fixture(a.fixture, a.out, d)
            print(f"[v1.21] fixture {doc.get('fixture')}: H1_t5 {sj['H1_t5_Judge_Agreement']['verdict']}; "
                  f"{doc['VERDICTS']}; GATE {doc['GATE']}")
            return 0
        if a.draws:
            raise Halt("--draws is for fixtures and the dry run only")
        if a.exploratory:
            run_exploratory(a.out, Draws())
            return 0
        if a.stage == "J":
            run_stage_j(a.out, a.t4_dir, a.t5_dir, Draws())
            return 0
        if a.stage == "C":
            run_stage_c(a.out, a.t4_stage1, a.t5_presence, Draws(), a.t5_rank)
            return 0
        ap.print_help()
        return 2
    except Halt as e:
        print(f"[v1.21] HALT: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
