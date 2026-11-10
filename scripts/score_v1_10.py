#!/usr/bin/env python3
"""
score_v1_10.py - AIAS v1.10, Ranking component, Paper A
(instrument specification + cross-category baseline + separability gate).

STATUS: r1 (2026-11-10), locked at tag v1.10-prereg-r2 (r1 superseded before any computation; DEVIATIONS Entry 1). Constants are transcribed from
osf/methodology/v1_10/prereg/PRE_REGISTRATION_v1_10.md (section cited inline) and from
the runner's settled decisions of 2026-11-10: primary position rule lead-item (E6),
first-mention = S1; floors 6 rankable mentions / 30 units / 5 units per category;
Stage S only after the lock; registry per early set as established in
osf/methodology/v1_10/registries/REGISTRY_CHOICES_v1_10.md; H3 = t1->t2 (gate),
H5 = t2->t3; the program's held studies excluded from v1.10 entirely; shuffle nulls
10,000 draws (H3/H5/H6 part b, seed 110010) and 2,000 for MQ7 (seed 110030);
sensitivity S7 (COI-flagged brands); refusal of --stage S/C before the lock. Follow-up of
the same day: within-category ranks CENTRED on the category mean rank for every pooled
statistic (S9 = the uncentred v0.37-v0.41 convention); S8 = Stage S without the two knife
sets; file swaps v0.6 olive oil -> the canonical post-revision run, v1.0 household -> the
scored _final file.

Modes
  --verify-manifest   hash check of every frozen input (SHA-256 + git blob)
  --parity            pre-lock MQ1 parse completion + MQ2 mention parity + unit join keys.
                      Computes no rank position and no rank statistic; reads only the key
                      columns of the Presence/Consistency table (never P or C*).
  --stage S           (after the lock) manifest -> extraction -> MQ1-MQ5 -> Stage S
  --stage C           (after the lock) re-extraction check -> open P / C* -> Stage C
  --dry-run           runs a mode on the synthetic replicas in osf/methodology/v1_10/dryrun/
                      (built by dryrun/build_dryrun_v1_10.py); bypasses the lock refusal and
                      never reads a real answer file.

Enforced order (section 3):
  verify manifest -> extract ranks for every frozen set -> MQ1-MQ5 data-quality checks
  -> Stage S (statistic selection on the early panel, blind to Presence/Consistency)
  -> write selection_v1_10.json -> only then open the Presence/Consistency table
  -> Stage C (gate H1-H3, secondary H4-H6, controls MQ6-MQ7, baseline, S1-S9) -> verdicts.
No network, no model calls.
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ===========================================================================
# TRANSCRIBED CONSTANTS (r1, including the runner decisions of 2026-11-10)
# ===========================================================================
PHASE_ID = "v1.10"
PREREG_TAG = "v1.10-prereg-r2"
ROOT = Path(__file__).resolve().parents[1]
V110 = "osf/methodology/v1_10"
MANIFEST = ROOT / V110 / "registries/INPUTS_MANIFEST_v1_10.json"
OUTDIR = ROOT / V110 / "outputs"
SELECTION_FILE = OUTDIR / "selection_v1_10.json"
ANCHOR_FILE = ROOT / V110 / "anchor/git_anchor_v1_10.json"
PARITY_FILE = ROOT / V110 / "prereg/parity_v1_10.json"
COI_REL = V110 + "/anchor/coi_flags_v1_10.json"     # S7 input; NOT a frozen input (decision 12)
PROFILES_REL = "osf/aias_2_0/aias_2_0_profiles.csv"
V41_VERDICTS_REL = "osf/v41/v41_verdicts.json"       # S6: MC_Snapshot flags
DRY_DIR = ROOT / V110 / "dryrun"
DRY_ROOT = DRY_DIR / "replica"
DRY_MANIFEST = DRY_DIR / "INPUTS_MANIFEST_dryrun_v1_10.json"
DRY_OUTDIR = DRY_DIR / "outputs"

MIN_NAMED_RANKABLE = 2        # E5: an answer is rankable iff >= 2 registry brands named
RATING_FLOOR = 6              # STATISTICS: R* rated iff >= 6 rankable mentions (v1.9 C* floor)
CANDIDATES = ["MNP", "IRW", "TOP3", "MR", "TOP1", "MODE"]   # also the Stage S tie order
REL_FLOOR = 0.50              # SELECTION: Spearman-Brown split-half floor
TIE_WINDOW = 0.02             # SELECTION: candidates within 0.02 of the best are tied
SEP_CONF, SEP_FALS = 0.30, 0.50    # H1/H2/H4: |rho| <= .30 CONFIRMED, >= .50 FALSIFIED
STAB_CONF, STAB_FALS = 0.50, 0.30  # H3/H5/H6: rho >= .50 CONFIRMED, < .30 FALSIFIED
P_ALPHA = 0.05
N_FLOOR_UNITS = 30            # n floor per wave / pair (units)
MIN_UNITS_PER_CATEGORY = 5    # a category enters a pooled statistic with >= 5 units
MIN_WAVES = 2                 # H1/H2 need >= 2 of 3 waves above the n floor
POS_CONTROL_MIN = 0.50        # MQ6: penalised variant must reach |rho| >= .50 with P
NEG_CONTROL_MAX = 0.20        # MQ7: shuffled-order split-half must stay below .20
PARITY_FLOOR_CODED = 0.98     # MQ2: v0.19 / v0.23 agreement with the coded mention files
MQ1_RANKABLE_FLAG = 0.50      # MQ1: sets with rankable share below 0.50 are flagged
MQ3_TAU_FLAG = 0.60           # MQ3: median Kendall tau below 0.60 flags an extraction review
N_PERM = 10_000               # H1-H6 permutation nulls
N_SHUFFLE = 10_000            # H3/H5/H6 part (b) within-answer order shuffle (decision 11)
N_SHUFFLE_MQ7 = 2_000         # MQ7 negative control (decision 11)
N_BOOT = 2_000                # bootstrap CI (reported, not a verdict input)
SEEDS = {"H1": 110001, "H2": 110002, "H3": 110003, "H4": 110004, "H5": 110005,
         "H6": 110006, "SHUFFLE": 110010, "BOOT": 110020, "MQ7": 110030}
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
WAVES = ["t1", "t2", "t3"]
N_BRAND_UNITS = 112           # OMNI units per wave in aias_2_0_profiles.csv
OMNI_ANSWERS_EXPECTED = 36    # MQ4: answers per category per wave
EARLY_SHARED_MODELS = ["claude-sonnet-4-6", "gpt-5.4-mini"]   # H6
RULES = ["lead_item", "first_mention"]   # primary (E6) and sensitivity S1
# rho_w convention (runner decision 2026-11-10): within-category average ranks are CENTRED on
# the category mean rank, r - (m_c + 1)/2, for every pooled statistic (H1-H6, MQ6, MQ7, Stage S,
# bootstrap, permutation and shuffle nulls). S9 = the uncentred v0.37-v0.41 convention.
CENTRE_RANKS = True
# S8 / MQ5 (runner decision 2026-11-10): the two knife sets, whose registries carry
# ordinary-word aliases; S8 = Stage S reliabilities without them (never changes the selection).
KNIFE_SETS = ["EARLY-6 v1.0 knives", "EARLY-6 v0.16 kitchen_knives"]
ORDINARY_WORD_ALIASES = ["global", "mac", "made in", "dick", "kramer", "new west"]


class Halt(RuntimeError):
    """A pre-registered halt condition (manifest mismatch, parse exception, parity < 100%
    on v0.20-v0.22, order violation, failed join)."""


# ===========================================================================
# RANK EXTRACTION (pre-registration section 4, rules E0-E7)
# ===========================================================================


def normalize(text: str) -> str:
    """E1: v1.4 canonical normalisation - NFKD, combining marks removed, lower case."""
    if not text:
        return ""
    s = unicodedata.normalize("NFKD", text)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def compile_registry(registry: dict[str, list[str]]) -> dict[str, list[re.Pattern]]:
    """E2: {canonical: [aliases]} -> word-bounded patterns, identical to the certified
    detector (r'\\b' + re.escape(alias) + r'\\b' on normalised text). The canonical
    name is always one of the aliases."""
    out = {}
    for canon, aliases in registry.items():
        names = {normalize(a).strip() for a in [canon, *aliases] if a and a.strip()}
        out[canon] = [re.compile(r"\b" + re.escape(a) + r"\b") for a in sorted(names, key=len, reverse=True)]
    return out


def find_mentions(norm_text: str, patterns: dict[str, list[re.Pattern]]) -> dict[str, list[int]]:
    """E2/E4: all match start offsets per brand, found independently per brand (so the
    set of named brands equals the certified detector's). Brand absent -> not in dict."""
    hits = {}
    for canon, pats in patterns.items():
        starts = sorted({m.start() for p in pats for m in p.finditer(norm_text)})
        if starts:
            hits[canon] = starts
    return hits


_ITEM_LINE = re.compile(
    r"^(?P<indent>[ \t]*)(?:"
    r"(?P<num>\d{1,2}[.)])[ \t]+"
    r"|(?P<bul>[-*+•–])[ \t]+"
    r"|(?P<head>#{1,6})[ \t]+"
    r"|(?P<bold>\*\*)(?=[^*\n]+\*\*)"
    r")", re.M)


def item_spans(norm_text: str) -> list[tuple[int, int, str]]:
    """E3: top-level list items. An item line is a numbered, bulleted, heading or
    bold-led line; top level = headings plus the non-heading item lines at the
    smallest indentation; deeper lines belong to their parent item. Each item runs to
    the next top-level item (the last one to the end of the answer)."""
    lines = list(_ITEM_LINE.finditer(norm_text))
    if not lines:
        return []
    ind = [len(m.group("indent").expandtabs(4)) for m in lines]
    non_head = [i for i, m in zip(ind, lines) if not m.group("head")]
    base = min(non_head) if non_head else 0
    tops = [(m.start(), next(k for k in ("num", "bul", "head", "bold") if m.group(k)))
            for i, m in zip(ind, lines) if m.group("head") or i <= base]
    return [(s, tops[j + 1][0] if j + 1 < len(tops) else len(norm_text), kind)
            for j, (s, kind) in enumerate(tops)]


def _lead_items(hits: dict[str, list[int]], spans) -> dict[str, int]:
    """Index of the first item each brand LEADS (is named first in)."""
    lead = {}
    for j, (s, e, _k) in enumerate(spans):
        inside = {b: next(x for x in xs if s <= x < e) for b, xs in hits.items()
                  if any(s <= x < e for x in xs)}
        if not inside:
            continue
        m = min(inside.values())
        for b, x in inside.items():
            if x == m and b not in lead:
                lead[b] = j
    return lead


def rank_answer(text: str, patterns, rule: str = "lead_item") -> dict:
    """E0-E7 for one answer. Returns {"named": n, "list_structured": bool,
    "ranks": {brand: (k_mid, k_min)}} with ranks only when rankable (n >= 2).
    rule 'lead_item' (primary): in a list-structured answer (>= 2 items led by a
    registry brand) brands are ordered by the first item they lead; brands leading no
    item follow, in first-mention order. Prose answers: first-mention order.
    rule 'first_mention' (sensitivity S1): first-mention order everywhere.
    Ties (equal keys) take mid-ranks (k_mid) and competition min-ranks (k_min)."""
    norm = normalize(text)
    hits = find_mentions(norm, patterns)
    n = len(hits)
    first = {b: xs[0] for b, xs in hits.items()}            # E4: first occurrence wins
    spans = item_spans(norm)
    lead = _lead_items(hits, spans) if spans else {}
    list_structured = len(set(lead.values())) >= 2
    if rule == "lead_item" and list_structured:
        key = {b: ((0, lead[b]) if b in lead else (1, first[b])) for b in hits}
    elif rule in ("lead_item", "first_mention"):
        key = {b: (0, first[b]) for b in hits}
    else:
        raise ValueError(rule)
    out = {"named": n, "list_structured": list_structured, "ranks": {}}
    if n < MIN_NAMED_RANKABLE:                                # E5
        return out
    pos = 1
    for kv in sorted(set(key.values())):
        group = [b for b in hits if key[b] == kv]
        g = len(group)
        for b in group:
            out["ranks"][b] = (pos + (g - 1) / 2.0, pos)
        pos += g
    return out


def nested_events(norm_text: str, patterns) -> int:
    """MQ5: matches of one brand lying inside a longer match of another brand."""
    spans = {b: [(m.start(), m.end()) for p in ps for m in p.finditer(norm_text)] for b, ps in patterns.items()}
    n = 0
    for b, sp in spans.items():
        for (s, e) in sp:
            if any(b2 != b and s2 <= s and e <= e2 and (e2 - s2) > (e - s)
                   for b2, sp2 in spans.items() for (s2, e2) in sp2):
                n += 1
    return n


def kendall_tau(a: dict, b: dict) -> float:
    """MQ3: (concordant - discordant) / (concordant + discordant) over common keys;
    pairs tied in either order are skipped (development-sample convention)."""
    keys = sorted(set(a) & set(b))
    conc = disc = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            x = (a[keys[i]] - a[keys[j]]) * (b[keys[i]] - b[keys[j]])
            conc += x > 0
            disc += x < 0
    return (conc - disc) / (conc + disc) if conc + disc else float("nan")


# ===========================================================================
# CANDIDATE STATISTICS (section 5). Every score is oriented so that
# HIGHER = NEARER THE TOP of the answer.
# ===========================================================================


def brand_scores(obs: list[tuple[float, int, int]]) -> dict:
    """obs: [(k_mid, k_min, n_named)] over the brand's rankable answers."""
    if not obs:
        return {"n_ranked": 0, **{c: float("nan") for c in CANDIDATES}}
    k = np.array([o[0] for o in obs], float)
    kmin = np.array([o[1] for o in obs], int)
    n = np.array([o[2] for o in obs], float)
    q = (k - 1.0) / (n - 1.0)
    vals, cnt = np.unique(kmin, return_counts=True)
    return {"n_ranked": len(obs),
            "MNP": float(100.0 * (1.0 - q.mean())),     # mean normalised position, 0-100
            "IRW": float(np.mean(1.0 / k)),             # inverse-rank weight
            "TOP3": float(np.mean(kmin <= 3)),          # top-3 share
            "MR": float(-k.mean()),                     # mean rank (negated)
            "TOP1": float(np.mean(kmin == 1)),          # named-first share
            "MODE": float(-vals[cnt == cnt.max()].min())}  # modal rank (negated)


def score_units(rows, floor: int = RATING_FLOOR) -> dict:
    """rows: iterable of dicts with unit key fields + brand + k_mid, k_min, n.
    Returns {unit_key: scores + rated flag}. unit_key = (panel, wave, category, brand)."""
    acc = defaultdict(list)
    for r in rows:
        acc[(r["panel"], r["wave"], r["category"], r["brand"])].append((r["k_mid"], r["k_min"], r["n"]))
    out = {}
    for key, obs in acc.items():
        s = brand_scores(obs)
        s["rated"] = s["n_ranked"] >= floor
        out[key] = s
    return out


def unit_stat_arrays(stat, u, kmid, kmin, n, nu):
    """Vectorised brand_scores for one candidate over unit indices u (for the shuffle
    nulls). Units without rows get NaN. Identical values to brand_scores (tested)."""
    cnt = np.bincount(u, minlength=nu).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        if stat == "MNP":
            v = 100.0 * (1.0 - np.bincount(u, weights=(kmid - 1.0) / (n - 1.0), minlength=nu) / cnt)
        elif stat == "IRW":
            v = np.bincount(u, weights=1.0 / kmid, minlength=nu) / cnt
        elif stat == "TOP3":
            v = np.bincount(u, weights=(kmin <= 3).astype(float), minlength=nu) / cnt
        elif stat == "MR":
            v = -np.bincount(u, weights=kmid, minlength=nu) / cnt
        elif stat == "TOP1":
            v = np.bincount(u, weights=(kmin == 1).astype(float), minlength=nu) / cnt
        elif stat == "MODE":
            K = int(kmin.max()) + 1 if len(kmin) else 1
            m = np.bincount(u * K + kmin, minlength=nu * K).reshape(nu, K)
            v = -np.argmax(m, axis=1).astype(float)
            v[cnt == 0] = np.nan
        else:
            raise ValueError(stat)
    return v


class RankMatrix:
    """Rankable rank rows as arrays, for fast re-scoring under within-answer order
    shuffles (H3/H5/H6 part b, MQ7). Rows of one answer are its named brands."""

    def __init__(self, rows, unit_of):
        rows = sorted(rows, key=lambda r: (str(r["answer_id"]), str(r["brand"])))
        self.units = sorted({unit_of(r) for r in rows}, key=lambda k: tuple(map(str, k)))
        self.uidx = {u: i for i, u in enumerate(self.units)}
        self.u = np.array([self.uidx[unit_of(r)] for r in rows], dtype=np.int64)
        aid = {}
        self.a = np.array([aid.setdefault(r["answer_id"], len(aid)) for r in rows], dtype=np.int64)
        N = len(rows)
        first = np.r_[0, np.flatnonzero(np.diff(self.a)) + 1] if N else np.array([], dtype=np.int64)
        lens = np.diff(np.r_[first, N]) if N else np.array([], dtype=np.int64)
        self.start = np.repeat(first, lens)
        self.kmid = np.array([r["k_mid"] for r in rows], float)
        self.kmin = np.array([r["k_min"] for r in rows], np.int64)
        self.n = np.array([r["n"] for r in rows], float)
        if N and not np.all(np.repeat(lens, lens) == self.n):
            raise Halt("RankMatrix: an answer's rows differ from its named count")
        self.nu = len(self.units)
        self.count = np.bincount(self.u, minlength=self.nu)

    def shuffled(self, rng):
        """Uniform random order of the named brands within every answer (no ties)."""
        N = len(self.a)
        order = np.lexsort((rng.random(N), self.a))
        k = np.empty(N, np.int64)
        k[order] = np.arange(N) - self.start[order] + 1
        return k.astype(float), k

    def stat(self, stat, kmid=None, kmin=None):
        return unit_stat_arrays(stat, self.u, self.kmid if kmid is None else kmid,
                                self.kmin if kmin is None else kmin, self.n, self.nu)


# ===========================================================================
# CORRELATION MACHINERY (v0.37 / v0.41 conventions)
# ===========================================================================


def _rank_avg(a):
    """Average ranks (1-based). Values are compared at 12 decimals so that float noise
    from different summation orders never breaks a tie (same rule for observed values,
    permutation, bootstrap and shuffle nulls)."""
    a = np.round(np.asarray(a, float), 12)
    if len(a) == 0:
        return np.empty(0)
    order = np.argsort(a, kind="mergesort")
    s = a[order]
    new = np.r_[True, s[1:] != s[:-1]]
    starts = np.flatnonzero(new)
    counts = np.diff(np.r_[starts, len(a)])
    r = np.empty(len(a))
    r[order] = np.repeat(starts + (counts + 1) / 2.0, counts)
    return r


def _rankdata(x):
    """Average ranks (kept for backward compatibility; same values as _rank_avg)."""
    return _rank_avg(x)


def _pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else float("nan")


def within_ranks(values, groups, centre=None):
    """Average ranks within each category, centred on the category mean rank (m_c + 1)/2
    (CENTRE_RANKS; S9 switches the centring off = the v0.37-v0.41 convention)."""
    centre = CENTRE_RANKS if centre is None else centre
    values, groups = np.asarray(values, float), np.asarray(groups)
    out = np.empty(len(values))
    for g in dict.fromkeys(groups.tolist()):
        idx = np.where(groups == g)[0]
        r = _rank_avg(values[idx])
        out[idx] = r - (len(idx) + 1) / 2.0 if centre else r
    return out


def _group_index(groups):
    groups = np.asarray(groups)
    return [np.where(groups == g)[0] for g in dict.fromkeys(groups.tolist())]


def _within_ranks_idx(values, gidx, centre=None):
    centre = CENTRE_RANKS if centre is None else centre
    out = np.empty(len(values))
    for idx in gidx:
        r = _rank_avg(values[idx])
        out[idx] = r - (len(idx) + 1) / 2.0 if centre else r
    return out


@contextlib.contextmanager
def uncentred():
    """S9: every pooled statistic computed inside uses uncentred within-category ranks."""
    global CENTRE_RANKS
    keep = CENTRE_RANKS
    CENTRE_RANKS = False
    try:
        yield
    finally:
        CENTRE_RANKS = keep


def keep_categories(groups, min_units: int = MIN_UNITS_PER_CATEGORY):
    """Mask of units whose category has >= min_units units in this comparison."""
    groups = np.asarray(groups)
    c = Counter(groups.tolist())
    return np.array([c[g] >= min_units for g in groups.tolist()], bool)


def pooled_within_rho(x, y, groups):
    """Pooled within-category Spearman: Pearson of within-category average ranks."""
    if len(x) < 3:
        return float("nan")
    return _pearson(within_ranks(x, groups), within_ranks(y, groups))


def perm_p(x, y, groups, obs, seed, sided, n_draws=None):
    """Within-category permutation null: y permuted within category. (hits+1)/(N+1)."""
    n_draws = N_PERM if n_draws is None else n_draws
    if not np.isfinite(obs):
        return float("nan")
    rng = np.random.default_rng(seed)
    groups = np.asarray(groups)
    rx = within_ranks(x, groups)
    ry = within_ranks(y, groups)
    gidx = _group_index(groups)
    idx = np.arange(len(ry))
    hits = 0
    for _ in range(n_draws):
        for g in gidx:
            idx[g] = rng.permutation(g)
        r = _pearson(rx, ry[idx])
        hits += (r >= obs - 1e-12) if sided == "one" else (abs(r) >= abs(obs) - 1e-12)
    return (hits + 1) / (n_draws + 1)


def boot_ci(x, y, groups, seed, n_draws=None, level=0.90):
    """Percentile CI of the pooled within-category rho; units resampled within category."""
    n_draws = N_BOOT if n_draws is None else n_draws
    rng = np.random.default_rng(seed)
    x, y, groups = np.asarray(x, float), np.asarray(y, float), np.asarray(groups)
    gidx = _group_index(groups)
    vals = []
    for _ in range(n_draws):
        idx = np.concatenate([rng.choice(g, size=len(g), replace=True) for g in gidx])
        vals.append(pooled_within_rho(x[idx], y[idx], groups[idx]))
    vals = np.array([v for v in vals if np.isfinite(v)])
    a = (1 - level) / 2
    return (float(np.quantile(vals, a)), float(np.quantile(vals, 1 - a))) if len(vals) else (float("nan"),) * 2


def spearman_brown(r):
    return float(2 * r / (1 + r)) if np.isfinite(r) and r > -1 else float("nan")


def shuffle_answer_ranks(rows, rng):
    """MQ7 / H3 shuffle null: within every answer, the named brands' order is replaced by
    a uniformly random order (no ties). List length n and the named set are kept.
    Same draw algorithm as RankMatrix.shuffled (rows ordered by answer, then brand)."""
    rows = sorted(rows, key=lambda r: (str(r["answer_id"]), str(r["brand"])))
    if not rows:
        return []
    keys = [(r["panel"], r["wave"], r["category"], r["answer_id"]) for r in rows]
    aid = {}
    a = np.array([aid.setdefault(k, len(aid)) for k in keys], dtype=np.int64)
    N = len(rows)
    first = np.r_[0, np.flatnonzero(np.diff(a)) + 1]
    start = np.repeat(first, np.diff(np.r_[first, N]))
    order = np.lexsort((rng.random(N), a))
    k = np.empty(N, np.int64)
    k[order] = np.arange(N) - start[order] + 1
    return [{**r, "k_mid": float(p), "k_min": int(p)} for r, p in zip(rows, k)]


# ===========================================================================
# STAGE S - statistic selection (section 6; blind to P and C)
# ===========================================================================


def split_half_reliability(rows_a, rows_b, stat: str, floor: int = RATING_FLOOR) -> tuple[float, int]:
    """rows_a / rows_b: rank rows of the two halves (odd vs even run_idx). Units rated in
    both halves; categories with >= MIN_UNITS_PER_CATEGORY units. Returns (r_SB, n)."""
    sa, sb = score_units(rows_a, floor), score_units(rows_b, floor)
    keys = sorted((k for k in sa if k in sb and sa[k]["rated"] and sb[k]["rated"]),
                  key=lambda k: tuple(map(str, k)))
    if not keys:
        return float("nan"), 0
    groups = np.array([f"{k[0]}|{k[2]}" for k in keys])
    m = keep_categories(groups)
    keys = [k for k, ok in zip(keys, m) if ok]
    if len(keys) < 3:
        return float("nan"), len(keys)
    groups = groups[m]
    r = pooled_within_rho([sa[k][stat] for k in keys], [sb[k][stat] for k in keys], groups)
    return spearman_brown(r), len(keys)


def select_statistic(reliability: dict[str, float]) -> dict:
    """Highest Spearman-Brown split-half reliability among candidates reaching
    REL_FLOOR; within TIE_WINDOW of the best -> first in CANDIDATES order."""
    elig = {s: r for s, r in reliability.items() if np.isfinite(r) and r >= REL_FLOOR}
    if not elig:
        return {"selected": None, "reliability": reliability,
                "outcome": "NO RELIABLE RANK STATISTIC (instrument FAIL; negative result)"}
    best = max(elig.values())
    tied = [s for s in CANDIDATES if s in elig and elig[s] >= best - TIE_WINDOW]
    return {"selected": tied[0], "tied": tied, "best": best, "reliability": reliability,
            "outcome": "SELECTED"}


# ===========================================================================
# VERDICT RULES (section 7)
# ===========================================================================


def verdict_separability(by_wave: dict[str, tuple[float, int]]) -> str:
    """H1/H2: {wave: (rho, n)}. Waves under the n floor are set aside; UNDETERMINED if
    fewer than MIN_WAVES remain. FALSIFIED if any |rho| >= .50; CONFIRMED if all
    |rho| <= .30; MARGINAL otherwise. Values compared unrounded."""
    ok = {w: r for w, (r, n) in by_wave.items() if n >= N_FLOOR_UNITS and np.isfinite(r)}
    if len(ok) < MIN_WAVES:
        return "UNDETERMINED"
    if any(abs(r) >= SEP_FALS for r in ok.values()):
        return "FALSIFIED"
    if all(abs(r) <= SEP_CONF for r in ok.values()):
        return "CONFIRMED"
    return "MARGINAL"


def verdict_single_separability(rho: float, n: int) -> str:
    """H4 (one comparison): same bands, single estimate."""
    if n < N_FLOOR_UNITS or not np.isfinite(rho):
        return "UNDETERMINED"
    if abs(rho) >= SEP_FALS:
        return "FALSIFIED"
    return "CONFIRMED" if abs(rho) <= SEP_CONF else "MARGINAL"


def verdict_stability(rho: float, p_perm: float, p_shuffle: float, n: int) -> str:
    """H3/H5/H6: CONFIRMED iff rho >= .50 AND p_perm < .05 AND p_shuffle < .05;
    FALSIFIED iff rho < .30 OR p_perm >= .05 OR p_shuffle >= .05; else MARGINAL."""
    if n < N_FLOOR_UNITS or not np.isfinite(rho):
        return "UNDETERMINED"
    if rho < STAB_FALS or p_perm >= P_ALPHA or p_shuffle >= P_ALPHA:
        return "FALSIFIED"
    if rho >= STAB_CONF:
        return "CONFIRMED"
    return "MARGINAL"


def gate_verdict(h1: str, h2: str, h3: str, h4: str | None = None,
                 instrument_fail: bool = False) -> str:
    """GATE: FAIL if Stage S ended in INSTRUMENT FAIL or any of H1-H3 FALSIFIED; else
    UNDETERMINED if any UNDETERMINED; PASS if all three CONFIRMED (downgraded to
    MARGINAL if the early-panel replication H4 is FALSIFIED); MARGINAL otherwise
    (Paper B then only on Pablo's recorded decision)."""
    trio = (h1, h2, h3)
    if instrument_fail or "FALSIFIED" in trio:
        return "FAIL"
    if "UNDETERMINED" in trio:
        return "UNDETERMINED"
    if all(v == "CONFIRMED" for v in trio):
        return "MARGINAL" if h4 == "FALSIFIED" else "PASS"
    return "MARGINAL"


# ===========================================================================
# INPUTS (section 2) - manifest, context, lock status
# ===========================================================================


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(path: Path) -> str:
    """Git blob id as git stores it: for a symlink, the link text (not the target)."""
    p = Path(path)
    data = str(p.readlink()).encode() if p.is_symlink() else p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def verify_manifest(manifest_path: Path = MANIFEST, root: Path = ROOT) -> list[str]:
    """Every frozen file must match its SHA-256 and git blob; returns mismatches
    (empty list = pass). Any mismatch halts the run (DEVIATIONS policy). A committed
    symlink is verified on its link text only (git pins nothing else); it is never read."""
    man = json.loads(Path(manifest_path).read_text())
    bad = []
    for e in man["files"]:
        p = root / e["path"]
        if e.get("symlink_to") is not None:
            if not p.is_symlink() or str(p.readlink()) != e["symlink_to"] or git_blob_sha1(p) != e["git_blob"]:
                bad.append(f"symlink mismatch: {e['path']}")
            continue
        if not p.exists():
            bad.append(f"missing: {e['path']}")
            continue
        if sha256(p) != e["sha256"] or git_blob_sha1(p) != e["git_blob"]:
            bad.append(f"hash mismatch: {e['path']}")
    return bad


class Ctx:
    """Where a run reads and writes. Real runs read the repository and write
    osf/methodology/v1_10/outputs/; dry runs read the synthetic replica tree and write
    osf/methodology/v1_10/dryrun/outputs/. Every input path must be pinned in the
    run's manifest (ctx.path refuses anything else)."""

    def __init__(self, dry: bool = False, root=None, manifest=None, outdir=None):
        self.dry = dry
        self.root = Path(root) if root else (DRY_ROOT if dry else ROOT)
        self.manifest_path = Path(manifest) if manifest else (DRY_MANIFEST if dry else MANIFEST)
        self.outdir = Path(outdir) if outdir else (DRY_OUTDIR if dry else OUTDIR)
        self.selection_file = self.outdir / "selection_v1_10.json" if (dry or outdir) else SELECTION_FILE
        self.stage_s_file = self.outdir / "stage_s_v1_10.json"
        self.verdicts_file = self.outdir / "v1_10_verdicts.json"
        self.rank_dir = self.outdir / "rank_tables"
        self.parity_file = (self.outdir / "parity_v1_10.json") if (dry or outdir) else PARITY_FILE
        self._pinned = None

    def pinned(self) -> dict:
        if self._pinned is None:
            man = json.loads(self.manifest_path.read_text())
            self._pinned = {e["path"]: e for e in man["files"]}
        return self._pinned

    def path(self, rel: str) -> Path:
        e = self.pinned().get(rel)
        if e is None:
            raise Halt(f"not a frozen input of this run's manifest: {rel}")
        if e.get("symlink_to") is not None:
            raise Halt(f"refusing to read a committed symlink: {rel}")
        return self.root / rel


def _tag_exists(tag: str = PREREG_TAG, root: Path = ROOT) -> bool:
    r = subprocess.run(["git", "-C", str(root), "rev-parse", "-q", "--verify", f"refs/tags/{tag}"],
                       capture_output=True, text=True)
    return r.returncode == 0 and bool(r.stdout.strip())


def lock_status() -> tuple[bool, str]:
    """Decision 13: --stage S / --stage C on real data need the pre-registration tag AND
    the git anchor file (written after the OSF deposit)."""
    why = []
    if not _tag_exists():
        why.append(f"git tag {PREREG_TAG} does not exist")
    if not Path(ANCHOR_FILE).exists():
        why.append(f"anchor file {ANCHOR_FILE} does not exist")
    return (not why), "; ".join(why)


# ===========================================================================
# FROZEN SETS (sections 2.1-2.3; the program's held studies excluded, decision 11)
# ===========================================================================
V09_TS = {"pm": "181205", "finance": "190816", "oliveoil": "184159", "running": "183238",
          "skincare": "185427"}
V06_FILES = {"pm": "data/pm/results_v2_20260429_181007.csv",
             "finance": "data/finance/results_v2_20260430_181613.csv",
             "oliveoil": "data/oliveoil/results_v2_20260430_091539.csv",   # canonical post-revision run (swap 2026-11-10)
             "running": "data/running/results_v2_20260429_205023.csv",
             "skincare": "data/skincare/results_v2_20260430_175139.csv"}
EARLY_SINGLE = [  # (category, phase wave, answers, registry) - registries per REGISTRY_CHOICES
    ("household", "v1.0", "data/household/results_v2_household_v1.0_final.csv",   # the scored file (swap 2026-11-10)
     "registries/brands_household.json"),
    ("knives", "v1.0", "data/knives/results_v2_knives_v1.0_final.csv",
     "registries/brands_knives_v1.0.json"),
    ("premium_tea", "v0.14", "data/premium_tea/results_v2_premium_tea_20260512_161817_filled.csv",
     "osf/v14/registries/brands_premium_tea.json"),
    ("kitchen_knives", "v0.16", "data/kitchen_knives/results_v2_kitchen_knives_20260516_212400.csv",
     "registries/brands_kitchen_knives.json"),
]
OMNI_BASE = {"t1": "osf", "t2": "osf/v34/data", "t3": "osf/v41/data"}
OMNI_REG = {"v0.19": ("osf/v19/panel_registry_v0_19.csv", "v19_csv"),
            "v0.20": ("prereg/v0_20_registry.json", "cells_json"),
            "v0.21": ("prereg/v0_21_registry.json", "cells_json"),
            "v0.22": ("prereg/v0_22_automotive_content.py", "v22_module"),
            "v0.23": (V110 + "/registries/v0_23_registry_v1_10.json", "v23_json")}
OMNI_DETECTOR = {"v0.20": "scripts/score_v20.py", "v0.21": "scripts/score_v21.py",
                 "v0.22": "scripts/score_v22.py"}


def build_sets() -> list[dict]:
    """Every frozen answer set with its format, registry and role. Roles: omni (gate),
    early6 (Stage S, H4, baseline), early2 (H6, baseline), paperB (v0.32 arms: rank tables
    only, never analysed), coi_hold (v0.28: MQ1 parse completion only - no rank extraction,
    no rank table, no statistic, no baseline stratum, until its COI screen)."""
    sets = []
    for w in WAVES:
        base = OMNI_BASE[w]
        for sub in OMNI:
            d = "v" + sub[3:]
            reg, rfmt = OMNI_REG[sub]
            s = {"set": f"OMNI {w} {sub}", "role": "omni", "panel": "LEGACY-6", "wave": w,
                 "category": sub, "registry": reg, "reg_fmt": rfmt}
            if sub == "v0.19":
                s.update(answers=f"{base}/v19/phase_b_responses.jsonl", fmt="v19_jsonl",
                         coded=f"{base}/v19/phase_b_results.csv")
            elif sub == "v0.23":
                v23 = "osf/v23/data" if w == "t1" else f"{base}/v23"
                s.update(answers=f"{v23}/v23_phase_b_raw.json", fmt="v23_json",
                         coded=f"{v23}/v23_phase_b_scored.json")
            else:
                s.update(answers=f"{base}/{d}/phase_b_results.csv", fmt="frame_csv",
                         detector=OMNI_DETECTOR[sub])
            sets.append(s)
    for c, ts in V09_TS.items():
        sets.append({"set": f"EARLY-6 v0.9 {c}", "role": "early6", "panel": "EARLY-6", "wave": "v0.9",
                     "category": c, "answers": f"data/{c}/results_enriched_v09_20260507_{ts}.csv",
                     "fmt": "runner_csv", "registry": f"osf_staging/v09/registries/brands_{c}.json",
                     "reg_fmt": "brands_json", "prompts": f"prompts/prompts_{c}.json"})
    for c, w, ans, reg in EARLY_SINGLE:
        sets.append({"set": f"EARLY-6 {w} {c}", "role": "early6", "panel": "EARLY-6", "wave": w,
                     "category": c, "answers": ans, "fmt": "runner_csv", "registry": reg,
                     "reg_fmt": "brands_json"})
    for c, ans in V06_FILES.items():
        sets.append({"set": f"EARLY-2 v0.6 {c}", "role": "early2", "panel": "EARLY-2", "wave": "v0.6",
                     "category": c, "answers": ans, "fmt": "runner_csv",
                     "registry": f"registries/brands_{c}.json", "reg_fmt": "brands_json",
                     "prompts": V110 + f"/registries/v06_prompts/prompts_{c}_v0_6.json"})
    # v0.28 (technology panel): COI screen pending (Samsung competes there; v0.43 decision).
    # Pinned and loaded for MQ1 parse completion only: no rank extraction, no rank table, no
    # statistic, no baseline stratum (runner decision 2026-11-10). LEGACY-6 = OMNI only.
    sets.append({"set": "COI-HOLD v0.28", "role": "coi_hold", "panel": "LEGACY-6", "wave": "v0.28",
                 "category": "v0.28", "answers": "osf/v28/data/phase_b_results.csv", "fmt": "frame_csv",
                 "registry": "prereg/v0_28_panel_brands.txt", "reg_fmt": "lines_txt"})
    for arm in ("A", "B"):
        sets.append({"set": f"PAPER-B v0.32 arm {arm}", "role": "paperB", "panel": f"V32-{arm}",
                     "wave": "v0.32", "category": "v0.32", "answers": f"osf/v32/data/phase_b_{arm}.csv",
                     "fmt": "frame_csv", "registry": "registries/v0_32_registry.json",
                     "reg_fmt": "cells_json"})
    return sets


# ===========================================================================
# LOADERS - one per frozen file format (registries and answers)
# ===========================================================================


def _read_csv(path: Path) -> list[dict]:
    csv.field_size_limit(sys.maxsize)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _import_file(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise Halt(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_registry(ctx: Ctx, rel: str, fmt: str):
    """-> (registry {canonical: [aliases]}, unit {canonical: unit brand key}, notes).
    The unit key is the brand key of the Presence/Consistency table (S-ids for v0.23,
    the canonical name everywhere else)."""
    p = ctx.path(rel)
    reg, unit, notes = {}, {}, []

    def add(canon, aliases=()):
        if canon in reg:
            notes.append(f"duplicate canonical entry merged: {canon}")
        lst = reg.setdefault(canon, [])
        lst += [a for a in aliases if a not in lst]

    if fmt == "brands_json":
        d = json.loads(p.read_text(encoding="utf-8"))
        for b in (d if isinstance(d, list) else d["brands"]):
            add(b.get("canonical") or b.get("brand"), b.get("aliases", []))
    elif fmt == "cells_json":
        d = json.loads(p.read_text(encoding="utf-8"))
        for cell in d["cells"].values():
            for b in (cell.get("brands", []) if isinstance(cell, dict) else cell):
                add(b["name"] if isinstance(b, dict) else b)
    elif fmt == "v22_module":   # same loader path as the certified scripts/score_v22.load_prereg_module
        mod = _import_file(p, "v22_prereg_v1_10")
        for names in mod.REGISTRY.values():
            for n in names:
                add(n)
    elif fmt == "v19_csv":
        for r in _read_csv(p):
            add(r["brand"])
    elif fmt == "v23_json":
        d = json.loads(p.read_text(encoding="utf-8"))
        for b in d["brands"]:
            add(b["brand"], b["aliases"])
            unit[b["brand"]] = b["id"]
    elif fmt == "lines_txt":
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                add(line.strip())
    else:
        raise ValueError(fmt)
    unit = {c: unit.get(c, c) for c in reg}
    return reg, unit, notes


def _answer(spec, model, frame, run_idx, text, bad_status=None, channel=None, row=None, archived=None):
    """E0: an answer without text, or with an error status, is a MISSING cell (text None)."""
    t = text if (isinstance(text, str) and text.strip()) else None
    reason = None
    if bad_status:
        reason, t = f"status:{bad_status}", None
    elif t is None:
        reason = "empty"
    rid = "" if run_idx is None else run_idx
    return {"set": spec["set"], "panel": spec["panel"], "wave": spec["wave"],
            "category": spec["category"], "model": model, "frame": frame, "run_idx": run_idx,
            "answer_id": f"{spec['set']}::{model}|{frame}|{rid}", "text": t,
            "missing_reason": reason, "channel": channel, "row": row, "archived_ranked": archived}


def load_answers(ctx: Ctx, spec: dict) -> list[dict]:
    """One loader per answer-file format. Yields every row (missing cells included)."""
    p = ctx.path(spec["answers"])
    fmt, out = spec["fmt"], []
    if fmt == "frame_csv":            # v0.20-v0.22 (t1-t3), v0.28, v0.32 arms
        for i, r in enumerate(_read_csv(p)):
            out.append(_answer(spec, r.get("model") or r.get("model_id"), r["frame_id"], None,
                               r.get("response_text"), channel=r.get("channel"), row=i))
    elif fmt == "v19_jsonl":          # v0.19 (t1-t3)
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
            if line.strip():
                r = json.loads(line)
                out.append(_answer(spec, r["panel_model"], r["frame"], None, r.get("response"), row=i))
    elif fmt == "v23_json":           # v0.23 (t1-t3)
        for i, r in enumerate(json.loads(p.read_text(encoding="utf-8"))):
            st = r.get("status", "ok")
            out.append(_answer(spec, r["model_id"], r["probe_id"], None, r.get("response"),
                               None if st == "ok" else st, channel=r.get("channel"), row=i))
    elif fmt == "runner_csv":         # EARLY-6 and EARLY-2 (run_aias_v2.py output, all variants)
        for i, r in enumerate(_read_csv(p)):
            st = r.get("call_status", "ok")
            out.append(_answer(spec, r["model_version"], r["prompt_id"], int(r["run_idx"]),
                               r.get("raw_response"), None if st == "ok" else st,
                               channel=r.get("cep"), row=i, archived=r.get("brands_ranked")))
    else:
        raise ValueError(fmt)
    seen = Counter(a["answer_id"] for a in out)
    for a in out:                     # duplicate cells keep their row number (logged in MQ4)
        if seen[a["answer_id"]] > 1:
            a["answer_id"] += f"#row{a['row']}"
            a["duplicate_cell"] = True
    return out


# ===========================================================================
# EXTRACTION PIPELINE (section 3 step 2) and per-answer rank tables
# ===========================================================================


def extract_answer(a: dict, patterns, unit: dict) -> dict:
    """E0-E7 on one answer, both rules (E6 primary, S1 sensitivity). Brands are reported
    by their unit key. An exception propagates (MQ1 halts)."""
    info = {k: a[k] for k in ("set", "panel", "wave", "category", "model", "frame", "run_idx",
                              "answer_id", "missing_reason", "channel")}
    if a["text"] is None:
        info.update(status="missing", named=[], n_named=0, rankable=False, list_structured=False,
                    numbered_list=False, n_items=0, nested=0, ranks={r: {} for r in RULES})
        return info
    norm = normalize(a["text"])
    hits = find_mentions(norm, patterns)
    spans = item_spans(norm)
    ranks = {}
    ls = False
    for rule in RULES:
        res = rank_answer(a["text"], patterns, rule)
        ranks[rule] = {unit[b]: v for b, v in res["ranks"].items()}
        if rule == "lead_item":
            ls = res["list_structured"]
    info.update(status="ok", named=sorted(unit[b] for b in hits), n_named=len(hits),
                rankable=len(hits) >= MIN_NAMED_RANKABLE, list_structured=ls,
                numbered_list=sum(1 for s in spans if s[2] == "num") >= 2, n_items=len(spans),
                nested=nested_events(norm, patterns), ranks=ranks)
    return info


PARSE_ONLY_ROLES = ("coi_hold",)   # loaded for MQ1 parse completion only (v0.28)


def parse_only_sets(ctx: Ctx) -> dict:
    """MQ1 parse completion for the parse-only sets: normalisation, registry matcher and
    item parser only - no rank_answer, no rank table, no statistic of any kind."""
    out = {}
    for spec in build_sets():
        if spec["role"] not in PARSE_ONLY_ROLES:
            continue
        reg, unit, _ = load_registry(ctx, spec["registry"], spec["reg_fmt"])
        pats = compile_registry(reg)
        answers = load_answers(ctx, spec)
        nt = sum(1 for a in answers if a["text"] is not None)
        for a in answers:
            if a["text"] is None:
                continue
            try:
                norm = normalize(a["text"])
                find_mentions(norm, pats)
                item_spans(norm)
            except Exception as e:  # MQ1: an exception halts
                raise Halt(f"MQ1: parser failed on {a['answer_id']}: {type(e).__name__}: {e}")
        out[spec["set"]] = {"rows": len(answers), "with_text": nt, "parsed": nt,
                            "note": "COI screen pending: parse completion only, never analysed"}
    return out


def run_extraction(ctx: Ctx, roles=None, log=print) -> dict:
    data = {}
    for spec in build_sets():
        if spec["role"] in PARSE_ONLY_ROLES or (roles and spec["role"] not in roles):
            continue
        reg, unit, notes = load_registry(ctx, spec["registry"], spec["reg_fmt"])
        pats = compile_registry(reg)
        answers = load_answers(ctx, spec)
        infos = []
        for a in answers:
            try:
                infos.append(extract_answer(a, pats, unit))
            except Exception as e:  # MQ1: an exception halts
                raise Halt(f"MQ1: extractor failed on {a['answer_id']}: {type(e).__name__}: {e}")
        data[spec["set"]] = {"spec": spec, "registry": reg, "unit": unit, "patterns": pats,
                             "registry_notes": notes, "answers": answers, "infos": infos}
    log(f"[v1.10] extracted {sum(len(d['infos']) for d in data.values())} rows "
        f"from {len(data)} frozen sets")
    return data


RANK_COLS = ["set", "panel", "wave", "category", "model", "frame", "run_idx", "answer_id", "status",
             "missing_reason", "n_named", "rankable", "list_structured", "numbered_list", "rule",
             "brand", "k_mid", "k_min", "q"]


def rank_table_bytes(entry: dict) -> bytes:
    """Per-answer rank table of one set: one row per (answer, rule, brand named); answers
    naming no brand get one row per rule with an empty brand; missing cells one row."""
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(RANK_COLS)
    for i in entry["infos"]:
        base = [i["set"], i["panel"], i["wave"], i["category"], i["model"], i["frame"],
                "" if i["run_idx"] is None else i["run_idx"], i["answer_id"], i["status"],
                i["missing_reason"] or "", i["n_named"], int(i["rankable"]), int(i["list_structured"]),
                int(i["numbered_list"])]
        if i["status"] == "missing":
            w.writerow(base + ["", "", "", "", ""])
            continue
        for rule in RULES:
            if not i["named"]:
                w.writerow(base + [rule, "", "", "", ""])
            for b in i["named"]:
                kv = i["ranks"][rule].get(b)
                if kv is None:
                    w.writerow(base + [rule, b, "", "", ""])
                else:
                    q = (kv[0] - 1.0) / (i["n_named"] - 1.0)
                    w.writerow(base + [rule, b, repr(float(kv[0])), kv[1], repr(float(q))])
    return buf.getvalue().encode("utf-8")


def _slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9.]+", "_", name).strip("_")


def rank_table_index(data: dict, write_dir: Path | None = None) -> dict:
    """{set: {path, sha256, rows}}; writes the tables when write_dir is given."""
    idx = {}
    for name, entry in data.items():
        b = rank_table_bytes(entry)
        rel = f"rank_tables/{_slug(name)}.csv"
        if write_dir is not None:
            (write_dir / rel).parent.mkdir(parents=True, exist_ok=True)
            (write_dir / rel).write_bytes(b)
        idx[name] = {"path": rel, "sha256": sha256_bytes(b), "rows": b.count(b"\n") - 1}
    return idx


def rank_rows(data: dict, rule: str, roles=None, sets=None, drop_models=()) -> list[dict]:
    """Rankable (answer, brand) rows for one rule: the input of every rank statistic."""
    out = []
    for name, entry in data.items():
        if (roles and entry["spec"]["role"] not in roles) or (sets and name not in sets):
            continue
        for i in entry["infos"]:
            if i["status"] != "ok" or not i["rankable"] or i["model"] in drop_models:
                continue
            for b, (km, kn) in i["ranks"][rule].items():
                out.append({"panel": i["panel"], "wave": i["wave"], "category": i["category"],
                            "answer_id": i["answer_id"], "model": i["model"], "run_idx": i["run_idx"],
                            "brand": b, "k_mid": km, "k_min": kn, "n": i["n_named"]})
    return out


# ===========================================================================
# DATA-QUALITY CHECKS MQ1-MQ5, MQ8, MQ9 (section 9) - before Stage S
# ===========================================================================


def mq1(data: dict) -> dict:
    out = {}
    for name, e in data.items():
        inf = e["infos"]
        t = [i for i in inf if i["status"] == "ok"]
        rk = sum(i["rankable"] for i in t)
        share = rk / len(t) if t else float("nan")
        out[name] = {"answers": len(inf), "with_text": len(t), "missing": len(inf) - len(t),
                     "parsed": len(t), "rankable": rk, "rankable_share": share,
                     "flag_below_0.50": bool(t) and share < MQ1_RANKABLE_FLAG}
    return out


def parity_set(ctx: Ctx, entry: dict, named_by_answer: dict) -> dict | None:
    """MQ2 mention parity of the extractor's named set for one OMNI set.
    v0.20-v0.22: against the certified detect_mention of the phase scorer (cells =
    answers with text x registry brands). v0.19 / v0.23: against the coded mention
    files (cells = coded rows of answers with text). Reads no rank column."""
    spec, reg, unit = entry["spec"], entry["registry"], entry["unit"]
    ans = {a["answer_id"]: a for a in entry["answers"]}
    cells = agree = 0
    dis, unmatched = [], 0
    if spec.get("detector"):
        mod = _import_file(ctx.path(spec["detector"]), "certified_" + _slug(spec["detector"]))
        for aid, a in ans.items():
            if a["text"] is None:
                continue
            for b in reg:
                cert = bool(mod.detect_mention(a["text"], b))
                ext = unit[b] in named_by_answer[aid]
                cells += 1
                agree += cert == ext
                if cert != ext:
                    dis.append({"answer_id": aid, "brand": unit[b], "certified": cert, "extractor": ext})
        kind = "certified detector " + spec["detector"]
    elif spec.get("coded"):
        by_cell = {(a["model"], a["frame"]): aid for aid, a in ans.items()}
        if spec["fmt"] == "v19_jsonl":
            coded = [((r["panel_model"], r["frame"]), r["brand"], str(r["mentioned"]).strip() == "1")
                     for r in _read_csv(ctx.path(spec["coded"]))]
        else:
            coded = []
            for r in json.loads(ctx.path(spec["coded"]).read_text(encoding="utf-8")):
                if r.get("status", "ok") != "ok":
                    continue
                for b, v in (r.get("brand_mentions") or {}).items():
                    coded.append(((r["model_id"], r["probe_id"]), b, bool(v)))
        for cell, b, flag in coded:
            aid = by_cell.get(cell)
            if aid is None or ans[aid]["text"] is None:
                unmatched += 1
                continue
            ext = b in named_by_answer[aid]
            cells += 1
            agree += flag == ext
            if flag != ext:
                dis.append({"answer_id": aid, "brand": b, "coded": flag, "extractor": ext})
        kind = "coded mention file " + spec["coded"]
    else:
        return None
    share = agree / cells if cells else float("nan")
    floor = 1.0 if spec.get("detector") else PARITY_FLOOR_CODED
    return {"against": kind, "cells": cells, "agree": agree, "agreement": share,
            "required": floor, "passes": bool(cells) and share >= floor,
            "coded_cells_without_answer_text": unmatched, "disagreements": dis}


def mq2_parity(ctx: Ctx, data: dict) -> dict:
    out = {"per_set": {}, "excluded_from_gate": [], "halt": []}
    for name, e in data.items():
        if e["spec"]["role"] != "omni":
            continue
        named = {i["answer_id"]: set(i["named"]) for i in e["infos"]}
        res = parity_set(ctx, e, named)
        out["per_set"][name] = res
        sub = e["spec"]["category"]
        if e["spec"].get("detector") and not res["passes"]:
            out["halt"].append(name)
        if e["spec"].get("coded") and not res["passes"] and sub not in out["excluded_from_gate"]:
            out["excluded_from_gate"].append(sub)   # leaves H1-H3 (deviation entry required)
    return out


def mq3_concordance(data: dict) -> dict:
    """EARLY sets with an archived brands_ranked column (function-calling extraction):
    median per-answer Kendall tau between the E6 order and the archived order, common
    registry brands only. Concordance check only - never a fallback extractor."""
    out = {}
    for name, e in data.items():
        if e["spec"]["role"] not in ("early6", "early2"):
            continue
        arch = {a["answer_id"]: a.get("archived_ranked") for a in e["answers"]}
        if not any(v is not None for v in arch.values()):
            out[name] = {"available": False}
            continue
        canon = {c: c for c in e["registry"]}
        taus = []
        for i in e["infos"]:
            if i["status"] != "ok" or not i["rankable"] or not arch.get(i["answer_id"]):
                continue
            names = [re.sub(r"@\d+$", "", x).strip() for x in arch[i["answer_id"]].split("|")]
            pos = {}
            for k, nm in enumerate(names):
                if nm in canon and canon[nm] not in pos:
                    pos[canon[nm]] = k + 1
            e6 = {b: v[0] for b, v in i["ranks"]["lead_item"].items()}
            if len(set(pos) & set(e6)) >= 2:
                t = kendall_tau(e6, pos)
                if np.isfinite(t):
                    taus.append(t)
        med = float(np.median(taus)) if taus else float("nan")
        out[name] = {"available": True, "answers_compared": len(taus), "median_tau": med,
                     "flag_review": bool(taus) and med < MQ3_TAU_FLAG}
    return out


def mq4_missing(data: dict) -> dict:
    out = {}
    for name, e in data.items():
        miss = [a for a in e["answers"] if a["text"] is None]
        rec = {"rows": len(e["answers"]), "missing": len(miss),
               "by_reason": dict(Counter(a["missing_reason"] for a in miss)),
               "by_model": dict(Counter(a["model"] for a in miss)),
               "duplicate_cells": sum(1 for a in e["answers"] if a.get("duplicate_cell")),
               "cells": [a["answer_id"] for a in miss]}
        if e["spec"]["role"] == "omni":
            rec["shortfall_vs_36"] = OMNI_ANSWERS_EXPECTED - (len(e["answers"]) - len(miss))
        if e["spec"]["fmt"] == "runner_csv":
            grid = (len({a["frame"] for a in e["answers"]}) * len({a["model"] for a in e["answers"]})
                    * len({a["run_idx"] for a in e["answers"]}))
            rec["design_grid"] = grid
            rec["cells_without_row"] = grid - len({(a["frame"], a["model"], a["run_idx"]) for a in e["answers"]})
        out[name] = rec
    return out


def mq5_overlap(data: dict) -> dict:
    out = {}
    for name, e in data.items():
        aliases = defaultdict(set)
        for c, al in e["registry"].items():
            for a in {normalize(x).strip() for x in [c, *al] if x and x.strip()}:
                aliases[a].add(c)
        shared = {a: sorted(e["unit"][c] for c in cs) for a, cs in aliases.items() if len(cs) > 1}
        nonword = sorted(a for a in aliases if not re.match(r"\w", a[-1]))
        canon_nonword = sorted(c for c in e["registry"] if not re.match(r"\w", normalize(c).strip()[-1]))
        ordinary = {a: sorted(e["unit"][c] for c in aliases[a]) for a in ORDINARY_WORD_ALIASES if a in aliases}
        out[name] = {"nested_match_events": sum(i["nested"] for i in e["infos"]),
                     "answers_with_nested_matches": sum(1 for i in e["infos"] if i["nested"]),
                     "aliases_shared_by_two_brands": shared,
                     "aliases_ending_non_word": nonword,
                     "canonical_names_ending_non_word": canon_nonword,
                     "ordinary_word_aliases": ordinary,
                     "registry_notes": e["registry_notes"]}
    return out


def _prompt_texts(path: Path) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    items = d if isinstance(d, list) else d["prompts"]
    return {p["id"]: (p.get("prompt") if p.get("prompt") is not None else p.get("text")) for p in items}


def mq8_prompt_parity(ctx: Ctx, data: dict) -> dict:
    """v0.6 vs v0.9: identical prompt ids (answer files) and prompt texts (the prompt
    files each wave's runner read; v0.6 as restored at 179b3d7) per category."""
    out, ok_all = {}, True
    for c in V09_TS:
        e6, e2 = data.get(f"EARLY-6 v0.9 {c}"), data.get(f"EARLY-2 v0.6 {c}")
        if e6 is None or e2 is None:
            continue
        ids6 = sorted({a["frame"] for a in e6["answers"]})
        ids2 = sorted({a["frame"] for a in e2["answers"]})
        t9 = _prompt_texts(ctx.path(e6["spec"]["prompts"]))
        t6 = _prompt_texts(ctx.path(e2["spec"]["prompts"]))
        same_ids = ids6 == ids2
        same_txt = all(t9.get(i) == t6.get(i) and t9.get(i) is not None for i in ids6)
        ok = same_ids and same_txt
        ok_all &= ok
        out[c] = {"prompt_ids_identical": same_ids, "prompt_texts_identical": same_txt, "passes": ok,
                  "prompt_files": {"v0.6": e2["spec"]["prompts"], "v0.9": e6["spec"]["prompts"]},
                  "differing_ids": sorted(i for i in set(t9) | set(t6) if t9.get(i) != t6.get(i))}
    return {"per_category": out, "passes": ok_all and bool(out)}


def mq9_truncation(data: dict) -> dict:
    return {"finish_reason_stored": {n: False for n in data},
            "note": ("No analysed set stores a finish reason. No answer file stores the token cap; caps are documented in "
                     "each phase's scripts. Kept: positions before any cut are valid.")}


def data_quality(ctx: Ctx, data: dict) -> dict:
    mq = {"MQ1": mq1(data), "MQ1_parse_only": parse_only_sets(ctx),
          "MQ2": mq2_parity(ctx, data), "MQ3": mq3_concordance(data),
          "MQ4": mq4_missing(data), "MQ5": mq5_overlap(data), "MQ8": mq8_prompt_parity(ctx, data),
          "MQ9": mq9_truncation(data)}
    if mq["MQ2"]["halt"]:
        raise Halt("MQ2: extractor named set != certified detector on "
                   + ", ".join(mq["MQ2"]["halt"]) + " (fix before Stage S)")
    return mq


# ===========================================================================
# PRESENCE / CONSISTENCY TABLE (opened only after Stage S) and the unit join
# ===========================================================================


def open_presence_consistency(path: Path, selection_file: Path | None = None):
    """Stage C input. Refuses to open P/C before Stage S has written its selection."""
    sel = Path(selection_file) if selection_file is not None else SELECTION_FILE
    if not sel.exists():
        raise Halt("ORDER: Stage S selection must exist before P/C are opened")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def profile_keys(path: Path) -> list[tuple[str, str, str]]:
    """Join keys ONLY (wave, substrate, brand) of the Presence/Consistency table, for the
    pre-lock join check: no other column is parsed or kept (P and C* are never read)."""
    csv.field_size_limit(sys.maxsize)
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        header = next(rd)
        iw, isub, ib = header.index("wave"), header.index("substrate"), header.index("brand")
        return [(row[iw], row[isub], row[ib]) for row in rd if row]


def omni_units(data: dict) -> dict:
    out = defaultdict(set)
    for e in data.values():
        if e["spec"]["role"] == "omni":
            out[e["spec"]["wave"]] |= {(e["spec"]["category"], u) for u in e["unit"].values()}
    return out


def join_check(keys, units_by_wave) -> dict:
    """MQ2 join: 112 OMNI units per wave, 1:1 with the table by substrate + brand key."""
    per = {}
    for w in WAVES:
        prof = Counter((s, b) for (wv, s, b) in keys if wv == w)
        exp = set(units_by_wave.get(w, set()))
        dup = sorted(k for k, c in prof.items() if c > 1)
        only_p, only_r = sorted(set(prof) - exp), sorted(exp - set(prof))
        per[w] = {"profile_units": len(prof), "registry_units": len(exp), "matched": len(set(prof) & exp),
                  "duplicates": dup, "only_in_profiles": only_p, "only_in_registries": only_r,
                  "one_to_one": not dup and not only_p and not only_r and len(exp) == N_BRAND_UNITS}
    return {"per_wave": per, "other_waves_in_table": sorted({k[0] for k in keys} - set(WAVES)),
            "passes": all(v["one_to_one"] for v in per.values())}


def parse_profiles(rows):
    """{wave: {(substrate, brand): value}} for P, C* (rated only) and total mentions."""
    P, C, NM = defaultdict(dict), defaultdict(dict), defaultdict(dict)

    def num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return float("nan")
    for r in rows:
        k = (r["substrate"], r["brand"])
        P[r["wave"]][k] = num(r["P"])
        c = num(r.get("C_star"))
        if str(r.get("rated", "")).strip().lower() in ("1", "true", "yes") and math.isfinite(c):
            C[r["wave"]][k] = c
        NM[r["wave"]][k] = num(r.get("n_mentions"))
    return P, C, NM


# ===========================================================================
# PRE-LOCK PARITY (task: MQ1 parse completion + MQ2 parity + join keys; no rank)
# ===========================================================================


def run_parity(ctx: Ctx, log=print) -> dict:
    """Runs only normalisation, mention detection and the item parser (structure only):
    no rank_answer, no lead items, no rank position, no rank statistic. The P/C table is
    read through profile_keys (key columns only)."""
    bad = verify_manifest(ctx.manifest_path, ctx.root)
    if bad:
        raise Halt("manifest verification failed: " + "; ".join(bad[:10]))
    res = {"phase": PHASE_ID, "kind": "pre-lock parity: MQ1 parse completion, MQ2 mention parity, unit join",
           "declaration": ("Computed before the lock on the frozen inputs. Uses normalisation, the "
                           "registry matcher and the list-item parser only; no rank position, no rank "
                           "statistic, and no P or C* value was computed, read or printed."),
           "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "dry_run": ctx.dry,
           "manifest": ctx.manifest_path.name, "manifest_sha256": sha256(ctx.manifest_path),
           "MQ1_parse_completion": {}, "MQ2_mention_parity": {}, "MQ2_join": None}
    units = defaultdict(set)
    for spec in build_sets():
        reg, unit, _ = load_registry(ctx, spec["registry"], spec["reg_fmt"])
        pats = compile_registry(reg)
        answers = load_answers(ctx, spec)
        named, exc = {}, []
        for a in answers:
            if a["text"] is None:
                continue
            try:
                norm = normalize(a["text"])
                h = find_mentions(norm, pats)
                item_spans(norm)
                named[a["answer_id"]] = {unit[b] for b in h}
            except Exception as e:  # noqa: BLE001 - recorded, MQ1 would halt
                exc.append({"answer_id": a["answer_id"], "error": f"{type(e).__name__}: {e}"})
        nt = sum(1 for a in answers if a["text"] is not None)
        res["MQ1_parse_completion"][spec["set"]] = {
            "rows": len(answers), "with_text": nt, "missing_cells": len(answers) - nt,
            "parsed_without_exception": nt - len(exc),
            "completion": (nt - len(exc)) / nt if nt else None, "exceptions": exc}
        if spec["role"] == "omni":
            entry = {"spec": spec, "registry": reg, "unit": unit, "answers": answers}
            res["MQ2_mention_parity"][spec["set"]] = parity_set(ctx, entry, named)
            units[spec["wave"]] |= {(spec["category"], u) for u in unit.values()}
    res["MQ2_join"] = join_check(profile_keys(ctx.path(PROFILES_REL)), units)
    mq1_ok = all(v["completion"] in (None, 1.0) for v in res["MQ1_parse_completion"].values())
    par = res["MQ2_mention_parity"]
    res["summary"] = {
        "MQ1_all_sets_parse_100pct": mq1_ok,
        "MQ2_detector_sets_100pct": all(v["passes"] for v in par.values() if v["required"] == 1.0),
        "MQ2_coded_sets_ge_0.98": all(v["passes"] for v in par.values() if v["required"] < 1.0),
        "MQ2_join_1to1_all_waves": res["MQ2_join"]["passes"]}
    ctx.parity_file.parent.mkdir(parents=True, exist_ok=True)
    ctx.parity_file.write_text(json.dumps(_clean(res), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for n, v in par.items():
        log(f"  MQ2 {n:16s} {v['agree']:5d}/{v['cells']:<5d} = {v['agreement']:.4f}  "
            f"(required {v['required']:.2f}) {'PASS' if v['passes'] else 'FAIL'}")
    for w, v in res["MQ2_join"]["per_wave"].items():
        log(f"  join {w}: profile units {v['profile_units']}, registry units {v['registry_units']}, "
            f"matched {v['matched']}, 1:1 {v['one_to_one']}")
    log(f"  MQ1 parse completion 100% on every set: {mq1_ok}")
    log(f"[v1.10] parity written to {ctx.parity_file}")
    return res


# ===========================================================================
# STAGE S (section 6) and MQ7
# ===========================================================================


def mq7_negative_control(rows, stat, n_draws=None, seed=None) -> dict:
    """Mean split-half reliability of `stat` with positions shuffled within each answer."""
    n_draws = N_SHUFFLE_MQ7 if n_draws is None else n_draws
    seed = SEEDS["MQ7"] if seed is None else seed
    RM = RankMatrix(rows, unit_of=lambda r: (r["panel"], r["wave"], r["category"], r["brand"],
                                             int(r["run_idx"]) % 2))
    pairs = []
    for uk, i in RM.uidx.items():
        if uk[4] == 1:
            j = RM.uidx.get(uk[:4] + (0,))
            if j is not None and RM.count[i] >= RATING_FLOOR and RM.count[j] >= RATING_FLOOR:
                pairs.append((uk, i, j))
    groups = np.array([f"{k[0]}|{k[2]}" for k, _, _ in pairs])
    m = keep_categories(groups) if len(groups) else np.zeros(0, bool)
    ia = np.array([i for (_, i, _), ok in zip(pairs, m) if ok], np.int64)
    ib = np.array([j for (_, _, j), ok in zip(pairs, m) if ok], np.int64)
    groups = groups[m] if len(groups) else groups
    out = {"statistic": stat, "draws": n_draws, "seed": seed, "n_units": int(len(ia)),
           "threshold": NEG_CONTROL_MAX}
    if len(ia) < 3:
        return {**out, "mean_reliability": float("nan"), "flag_list_composition_driven": False,
                "note": "fewer than 3 units rated in both halves"}
    gidx = _group_index(groups)
    v0 = RM.stat(stat)
    out["unshuffled_reliability_check"] = spearman_brown(
        _pearson(_within_ranks_idx(v0[ia], gidx), _within_ranks_idx(v0[ib], gidx)))
    rng = np.random.default_rng(seed)
    vals = np.empty(n_draws)
    for d in range(n_draws):
        km, kn = RM.shuffled(rng)
        v = RM.stat(stat, km, kn)
        vals[d] = spearman_brown(_pearson(_within_ranks_idx(v[ia], gidx), _within_ranks_idx(v[ib], gidx)))
    mean = float(np.nanmean(vals))
    return {**out, "mean_reliability": mean, "flag_list_composition_driven": mean >= NEG_CONTROL_MAX}


def _reliabilities(rows):
    odd = [r for r in rows if int(r["run_idx"]) % 2 == 1]
    even = [r for r in rows if int(r["run_idx"]) % 2 == 0]
    rel, nun = {}, {}
    for s in CANDIDATES:
        rel[s], nun[s] = split_half_reliability(odd, even, s)
    return rel, nun


def stage_s(data: dict, log=print) -> dict:
    """Selection on EARLY-6 rank tables only (lead-item rule), odd vs even run_idx.
    S8 (without the two knife sets) and S9 (uncentred ranks) are reported next to the
    selection and never change it."""
    sets6 = sorted(n for n, e in data.items() if e["spec"]["role"] == "early6")
    rows = rank_rows(data, "lead_item", roles=("early6",))
    rel, nun = _reliabilities(rows)
    sel = select_statistic(rel)
    fail = sel["selected"] is None
    stat_c = sel["selected"] or "MNP"   # INSTRUMENT FAIL: Stage C still runs, with MNP
    mq7 = mq7_negative_control(rows, stat_c)
    rel8, nun8 = _reliabilities(rank_rows(data, "lead_item", sets=set(sets6) - set(KNIFE_SETS)))
    sel8 = select_statistic(rel8)
    s8 = {"sets_removed": KNIFE_SETS, "reliability": rel8, "n_units": nun8,
          "would_select": sel8["selected"], "outcome": sel8["outcome"],
          "note": "reported next to the selection; never changes it"}
    with uncentred():
        rel9, nun9 = _reliabilities(rows)
        sel9 = select_statistic(rel9)
        mq7_9 = mq7_negative_control(rows, stat_c)
    s9 = {"convention": "uncentred within-category ranks (v0.37-v0.41)", "reliability": rel9, "n_units": nun9,
          "would_select": sel9["selected"], "outcome": sel9["outcome"], "MQ7": mq7_9,
          "note": "reported next to the selection; never changes it"}
    for s in CANDIDATES:
        log(f"  Stage S {s:5s} split-half reliability {rel[s]:.4f} (units {nun[s]})   "
            f"[S8 {rel8[s]:.4f} ({nun8[s]}); S9 uncentred {rel9[s]:.4f}]")
    log(f"  Stage S outcome: {sel['outcome']}; Stage C statistic: {stat_c}   "
        f"[S8 would select {sel8['selected']}; S9 would select {sel9['selected']}]")
    log(f"  MQ7 mean shuffled reliability {mq7['mean_reliability']:.4f} "
        f"({'FLAG' if mq7['flag_list_composition_driven'] else 'ok'})   [S9 uncentred {mq7_9['mean_reliability']:.4f}]")
    return {**sel, "n_units": nun, "instrument_fail": fail, "stat_for_stage_c": stat_c, "MQ7": mq7,
            "rank_convention": "within-category average ranks centred on the category mean rank",
            "S8_without_knife_sets": s8, "S9_uncentred": s9,
            "data": "EARLY-6 rank tables only, lead-item rule; halves = run_idx odd (1,3,5,7) vs even",
            "sets": sets6}


def _clean(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else "|".join(map(str, k)) if isinstance(k, tuple) else str(k)):
                _clean(v) for k, v in o.items()}
    if isinstance(o, set):
        return [_clean(v) for v in sorted(o, key=str)]
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        f = float(o)
        return f if math.isfinite(f) else None
    if isinstance(o, Path):
        return str(o)
    return o


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_stage_s(ctx: Ctx, log=print) -> dict:
    bad = verify_manifest(ctx.manifest_path, ctx.root)
    if bad:
        raise Halt("manifest verification failed: " + "; ".join(bad[:10]))
    log(f"[v1.10] manifest OK ({ctx.manifest_path.name}, dry_run={ctx.dry})")
    data = run_extraction(ctx, log=log)                                   # step 2
    ctx.outdir.mkdir(parents=True, exist_ok=True)
    idx = rank_table_index(data, write_dir=ctx.outdir)
    (ctx.outdir / "rank_tables_index_v1_10.json").write_text(json.dumps(idx, indent=2) + "\n")
    mq = data_quality(ctx, data)                                          # step 3 (halts)
    for n, v in mq["MQ2"]["per_set"].items():
        log(f"  MQ2 {n:16s} agreement {v['agreement']:.4f} (required {v['required']:.2f})")
    sel = stage_s(data, log)                                              # step 4
    doc = {"phase": PHASE_ID, "stage": "S", "created_utc": _now(), "dry_run": ctx.dry,
           "manifest_sha256": sha256(ctx.manifest_path), "rank_tables": idx, **sel}
    ctx.selection_file.write_text(json.dumps(_clean(doc), indent=2) + "\n")
    summary = {"phase": PHASE_ID, "stage": "S", "created_utc": _now(), "dry_run": ctx.dry,
               "manifest_sha256": sha256(ctx.manifest_path), "rank_tables": idx,
               "data_quality": mq, "selection_file": ctx.selection_file.name,
               "selection_sha256": sha256(ctx.selection_file)}
    ctx.stage_s_file.write_text(json.dumps(_clean(summary), indent=2, ensure_ascii=False) + "\n")
    log(f"[v1.10] Stage S written: {ctx.selection_file} (sha256 {summary['selection_sha256'][:16]}...)")
    return summary


# ===========================================================================
# STAGE C (section 7): hypotheses, controls, baseline (section 8), sensitivities (10)
# ===========================================================================


def units_cat_brand(rows, floor: int = RATING_FLOOR) -> dict:
    """{(category, brand): scores + rated} for rows of ONE panel x wave."""
    return {(k[2], k[3]): v for k, v in score_units(rows, floor).items()}


def _rho_only(x, y, groups):
    x, y, g = np.asarray(x, float), np.asarray(y, float), np.asarray(groups)
    if len(g):
        m = keep_categories(g)
        x, y, g = x[m], y[m], g[m]
    return {"rho": pooled_within_rho(x, y, g) if len(g) >= 3 else float("nan"), "n": int(len(g)),
            "units_per_category": dict(Counter(g.tolist()))}


def corr_test(x, y, groups, seed, sided, boot=True, n_perm=None) -> dict:
    """rho_w over categories with >= 5 units; y (the Ranking score) permuted within
    category; bootstrap CI reported (seed 110020)."""
    x, y, g = np.asarray(x, float), np.asarray(y, float), np.asarray(groups)
    if len(g):
        m = keep_categories(g)
        x, y, g = x[m], y[m], g[m]
    n = int(len(g))
    rho = pooled_within_rho(x, y, g) if n >= 3 else float("nan")
    p = perm_p(x, y, g, rho, seed, sided, n_perm) if n >= 3 else float("nan")
    ci = boot_ci(x, y, g, SEEDS["BOOT"]) if (boot and n >= 3) else (float("nan"), float("nan"))
    return {"rho": rho, "n": n, "p_perm": p, "sided": sided, "perm_seed": seed, "ci90": list(ci),
            "units_per_category": dict(Counter(g.tolist()))}


def separability(U: dict, Y: dict, stat: str, seed: int, excl_sub=(), excl_units=(), boot=True) -> dict:
    """H1 (Y = P) / H2 (Y = C*, rated only): rho_w(R*, Y) per OMNI wave."""
    per = {}
    for w in WAVES:
        keys = sorted(k for k, s in U[w].items() if s["rated"] and k[0] not in excl_sub
                      and k not in excl_units and k in Y.get(w, {}) and math.isfinite(Y[w][k]))
        per[w] = corr_test([Y[w][k] for k in keys], [U[w][k][stat] for k in keys], [k[0] for k in keys],
                           seed, "two", boot=boot)
    return {"verdict": verdict_separability({w: (per[w]["rho"], per[w]["n"]) for w in WAVES}),
            "per_wave": per}


def shuffle_p(rows_a, rows_b, keys, groups, stat, obs, seed=None, n_draws=None) -> float:
    """Part (b) null: the order of named brands is shuffled within every answer of both
    waves; R* recomputed for the same units; one-sided (hits: rho >= observed)."""
    seed = SEEDS["SHUFFLE"] if seed is None else seed
    n_draws = N_SHUFFLE if n_draws is None else n_draws
    if not np.isfinite(obs):
        return float("nan")
    tagged = [{**r, "_side": 0} for r in rows_a] + [{**r, "_side": 1} for r in rows_b]
    RM = RankMatrix(tagged, unit_of=lambda r: (r["_side"], r["category"], r["brand"]))
    ia = np.array([RM.uidx[(0,) + tuple(k)] for k in keys], np.int64)
    ib = np.array([RM.uidx[(1,) + tuple(k)] for k in keys], np.int64)
    gidx = _group_index(groups)
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_draws):
        km, kn = RM.shuffled(rng)
        v = RM.stat(stat, km, kn)
        hits += _pearson(_within_ranks_idx(v[ia], gidx), _within_ranks_idx(v[ib], gidx)) >= obs - 1e-12
    return (hits + 1) / (n_draws + 1)


def stability(rows_a, rows_b, stat, floor, seed_perm, excl_sub=(), excl_units=(), boot=True,
              nulls=True) -> dict:
    """H3/H5/H6: rho_w(R*_a, R*_b) over units rated in both; nulls (a) permutation of
    R*_b within category (one-sided) and (b) within-answer order shuffle (one-sided)."""
    Ua, Ub = units_cat_brand(rows_a, floor), units_cat_brand(rows_b, floor)
    keys = sorted(k for k in Ua if Ua[k]["rated"] and k in Ub and Ub[k]["rated"]
                  and k[0] not in excl_sub and k not in excl_units)
    g = np.array([k[0] for k in keys])
    if len(g):
        m = keep_categories(g)
        keys, g = [k for k, ok in zip(keys, m) if ok], g[m]
    n = len(keys)
    x = np.array([Ua[k][stat] for k in keys], float)
    y = np.array([Ub[k][stat] for k in keys], float)
    rho = pooled_within_rho(x, y, g) if n >= 3 else float("nan")
    res = {"rho": rho, "n": n, "units_per_category": dict(Counter(g.tolist()))}
    if nulls:
        res["p_perm"] = perm_p(x, y, g, rho, seed_perm, "one") if n >= 3 else float("nan")
        res["perm_seed"] = seed_perm
        res["p_shuffle"] = shuffle_p(rows_a, rows_b, keys, g, stat, rho) if n >= 3 else float("nan")
        res["shuffle_seed"], res["shuffle_draws"] = SEEDS["SHUFFLE"], N_SHUFFLE
        res["ci90"] = list(boot_ci(x, y, g, SEEDS["BOOT"])) if (boot and n >= 3) else [float("nan")] * 2
        res["verdict"] = verdict_stability(rho, res["p_perm"], res["p_shuffle"], n)
    return res


def omni_set_names(data: dict, wave: str) -> set:
    return {n for n, e in data.items() if e["spec"]["role"] == "omni" and e["spec"]["wave"] == wave}


def gate_block(rows_w: dict, stat: str, floor: int, P: dict, C: dict, excl_sub=(), excl_units=(),
               boot=True) -> dict:
    U = {w: units_cat_brand(rows_w[w], floor) for w in WAVES}
    return {"H1": separability(U, P, stat, SEEDS["H1"], excl_sub, excl_units, boot),
            "H2": separability(U, C, stat, SEEDS["H2"], excl_sub, excl_units, boot),
            "H3": stability(rows_w["t1"], rows_w["t2"], stat, floor, SEEDS["H3"], excl_sub, excl_units, boot)}


def h4_block(data: dict, stat: str, floor: int = RATING_FLOOR, boot=True) -> dict:
    """H4: rho_w(R*, pi_hat) on EARLY-6; pi_hat = share of the category's answers with
    text naming the brand (Presence's recall arm)."""
    x, y, g = [], [], []
    for name, e in data.items():
        if e["spec"]["role"] != "early6":
            continue
        U = units_cat_brand(rank_rows(data, "lead_item", sets={name}), floor)
        T = [i for i in e["infos"] if i["status"] == "ok"]
        for k, s in sorted(U.items()):
            if s["rated"]:
                x.append(sum(1 for i in T if k[1] in i["named"]) / len(T))
                y.append(s[stat])
                g.append(k[0])
    res = corr_test(x, y, g, SEEDS["H4"], "two", boot=boot)
    res["verdict"] = verdict_single_separability(res["rho"], res["n"])
    return res


def h6_block(data: dict, stat: str, mq8_pass: bool, floor: int = RATING_FLOOR, boot=True) -> dict:
    if not mq8_pass:
        return {"verdict": "UNDETERMINED", "reason": "MQ8 prompt parity failed: H6 is not run"}
    s06 = {n for n, e in data.items() if e["spec"]["role"] == "early2"}
    s09 = {f"EARLY-6 v0.9 {c}" for c in V09_TS} & set(data)
    ra = [r for r in rank_rows(data, "lead_item", sets=s06) if r["model"] in EARLY_SHARED_MODELS]
    rb = [r for r in rank_rows(data, "lead_item", sets=s09) if r["model"] in EARLY_SHARED_MODELS]
    res = stability(ra, rb, stat, floor, SEEDS["H6"], boot=boot)
    res["models"] = EARLY_SHARED_MODELS
    return res


def mq6_positive_control(data: dict, P: dict) -> dict:
    """Penalised MNP over all answers with text: unnamed brand q = 1; named in a
    rankable answer q = (k_mid - 1)/(n - 1); named alone q = 0 (position 1 of 1)."""
    per = {}
    for w in WAVES:
        x, y, g = [], [], []
        for n in sorted(omni_set_names(data, w)):
            e = data[n]
            sub = e["spec"]["category"]
            T = [i for i in e["infos"] if i["status"] == "ok"]
            for b in sorted(set(e["unit"].values())):
                if not T or (sub, b) not in P.get(w, {}):
                    continue
                qs = []
                for i in T:
                    if b not in i["named"]:
                        qs.append(1.0)
                    elif i["rankable"]:
                        qs.append((i["ranks"]["lead_item"][b][0] - 1.0) / (i["n_named"] - 1.0))
                    else:
                        qs.append(0.0)
                x.append(P[w][(sub, b)])
                y.append(100.0 * (1.0 - float(np.mean(qs))))
                g.append(sub)
        per[w] = _rho_only(x, y, g)
    ok = all(np.isfinite(v["rho"]) and abs(v["rho"]) >= POS_CONTROL_MIN for v in per.values())
    return {"per_wave": per, "threshold_abs_rho": POS_CONTROL_MIN, "passes": ok,
            "flag_gate_sensitivity": not ok}


def _dist(v):
    v = np.asarray([x for x in v if x is not None and np.isfinite(x)], float)
    if not len(v):
        return None
    return {"median": float(np.median(v)), "q25": float(np.quantile(v, .25)),
            "q75": float(np.quantile(v, .75)), "min": float(v.min()), "max": float(v.max()), "n": int(len(v))}


def baseline_tables(data: dict, stat: str, floor: int = RATING_FLOOR) -> list:
    """Section 8, descriptive, stratified by panel (never pooled across panels)."""
    strata = {"omni": "LEGACY-6", "early6": "EARLY-6", "early2": "EARLY-2"}   # v0.28 out (COI hold)
    out = []
    for name, e in data.items():
        sp = e["spec"]
        if sp["role"] not in strata:
            continue
        inf = e["infos"]
        T = [i for i in inf if i["status"] == "ok"]
        R = [i for i in T if i["rankable"]]
        U = units_cat_brand(rank_rows(data, "lead_item", sets={name}), floor)
        rated = sorted(b for (c, b), s in U.items() if s["rated"])
        firsts, led = Counter(), Counter()
        for i in R:
            f = [b for b, v in i["ranks"]["lead_item"].items() if v[1] == 1]
            for b in f:
                firsts[b] += 1.0 / len(f)
                led[b] += 1
        per_model = {}
        for m in sorted({i["model"] for i in inf}):
            Tm = [i for i in T if i["model"] == m]
            Rm = [i for i in Tm if i["rankable"]]
            nr = {b for i in Rm for b in i["named"]} & set(rated)
            per_model[m] = {"answers_with_text": len(Tm), "rankable": len(Rm),
                            "mean_list_length": float(np.mean([i["n_named"] for i in Rm])) if Rm else None,
                            "list_structured_share": (sum(i["list_structured"] for i in Tm) / len(Tm)) if Tm else None,
                            "share_of_rated_brands_named": (len(nr) / len(rated)) if rated else None}
        nn = [i["n_named"] for i in R]
        out.append({
            "stratum": strata[sp["role"]], "set": name, "category": sp["category"], "wave": sp["wave"],
            "answers": len(inf), "missing_cells": len(inf) - len(T),
            "rankable_share": len(R) / len(T) if T else None,
            "list_structured_share": sum(i["list_structured"] for i in T) / len(T) if T else None,
            "numbered_list_share": sum(i["numbered_list"] for i in T) / len(T) if T else None,
            "brands_named_per_rankable_answer": ({"median": float(np.median(nn)), "q25": float(np.quantile(nn, .25)),
                                                  "q75": float(np.quantile(nn, .75)), "max": int(max(nn))} if nn else None),
            "registry_size": len(e["registry"]), "brands_rated": len(rated),
            "rated_share_of_registry": len(rated) / len(e["registry"]) if e["registry"] else None,
            "R_star_selected": {"statistic": stat, **(_dist([U[(sp["category"], b)][stat] for b in rated]) or {})},
            "R_star_MNP": _dist([U[(sp["category"], b)]["MNP"] for b in rated]),
            "leader_share_most_frequent_first": (max(led.values()) / len(R)) if R else None,
            "leader_herfindahl": (sum((v / len(R)) ** 2 for v in firsts.values())) if R else None,
            "per_model": per_model,
            "top3_by_R_star": [{"brand": b, stat: U[(sp["category"], b)][stat]}
                               for b in sorted(rated, key=lambda b: (-U[(sp["category"], b)][stat], b))[:3]],
        })
    return out


def load_coi(ctx: Ctx, data: dict):
    """S7 input (not frozen; decision 12). -> (flagged units or None, sha256 or None, unknown)."""
    p = ctx.root / COI_REL
    if not p.exists():
        return None, None, []
    names = {}
    for e in data.values():
        if e["spec"]["role"] == "omni":
            sub = e["spec"]["category"]
            for canon, u in e["unit"].items():
                names[(sub, canon)] = u
                names[(sub, u)] = u
    flagged, unknown = set(), []
    for f in json.loads(p.read_text(encoding="utf-8")).get("flagged", []):
        u = names.get((f.get("substrate"), f.get("brand")))
        if u is None:
            unknown.append(f)
        else:
            flagged.add((f["substrate"], u))
    return flagged, sha256(p), unknown


def s6_flagged_models(ctx: Ctx):
    """S6: the models v0.41's MC_Snapshot flags (its 'mismatched' list)."""
    try:
        p = ctx.path(V41_VERDICTS_REL)
    except Halt:
        return [], "v0.41 verdicts not pinned in this run's manifest"
    mc = json.loads(p.read_text(encoding="utf-8")).get("manipulation_checks", {}).get("MC_Snapshot", {})
    return list(mc.get("mismatched", [])), f"v0.41 MC_Snapshot status {mc.get('status')}"


def _verdicts(block, h4v, instrument_fail):
    v = {h: block[h]["verdict"] for h in ("H1", "H2", "H3")}
    v["gate"] = gate_verdict(v["H1"], v["H2"], v["H3"], h4v, instrument_fail)
    return v


def sensitivities(ctx, data, stat, P, C, NM, excl, primary_v, h4v, instrument_fail, log=print,
                  extra=None) -> dict:
    """Section 10: reported; never change a verdict. Verdict changes are listed."""
    ow = {rule: {w: rank_rows(data, rule, sets=omni_set_names(data, w)) for w in WAVES} for rule in RULES}
    S, changes = {}, []

    def record(name, block, h4=None):
        v = _verdicts(block, h4v if h4 is None else h4, instrument_fail)
        S[name] = {"verdicts": v, "detail": block}
        for h, val in v.items():
            if val != primary_v[h]:
                changes.append({"sensitivity": name, "hypothesis": h, "primary": primary_v[h], "under_sensitivity": val})

    log("  S1 first-mention rule ...")
    record("S1_first_mention", gate_block(ow["first_mention"], stat, RATING_FLOOR, P, C, excl, boot=False))
    for fl in (3, 10):
        log(f"  S2 rating floor {fl} ...")
        record(f"S2_floor_{fl}", gate_block(ow["lead_item"], stat, fl, P, C, excl, boot=False))
    for s in CANDIDATES:
        log(f"  S3 candidate {s} ...")
        record(f"S3_candidate_{s}", gate_block(ow["lead_item"], s, RATING_FLOOR, P, C, excl, boot=False))
    loso = {}
    for sub in OMNI:
        log(f"  S4 leave out {sub} ...")
        name = f"S4_leave_out_{sub}"
        record(name, gate_block(ow["lead_item"], stat, RATING_FLOOR, P, C, tuple(set(excl) | {sub}), boot=False))
        loso[sub] = S[name]
    rng = {}
    for h in ("H1", "H2"):
        rng[h] = {w: [min(v["detail"][h]["per_wave"][w]["rho"] for v in loso.values()),
                      max(v["detail"][h]["per_wave"][w]["rho"] for v in loso.values())] for w in WAVES}
    rng["H3"] = [min(v["detail"]["H3"]["rho"] for v in loso.values()),
                 max(v["detail"]["H3"]["rho"] for v in loso.values())]
    S["S4_ranges"] = rng
    s5 = {}
    for w in WAVES:
        U = units_cat_brand(ow["lead_item"][w], RATING_FLOOR)
        pi = {}
        for n in omni_set_names(data, w):
            e = data[n]
            T = [i for i in e["infos"] if i["status"] == "ok"]
            for b in set(e["unit"].values()):
                pi[(e["spec"]["category"], b)] = sum(1 for i in T if b in i["named"]) / len(T) if T else float("nan")
        keys = sorted(k for k, s in U.items() if s["rated"] and k[0] not in excl and k in P.get(w, {}))
        r = [U[k][stat] for k in keys]
        g = [k[0] for k in keys]
        s5[w] = {"rho_R_P": _rho_only([P[w][k] for k in keys], r, g),
                 "rho_R_pi_hat": _rho_only([pi.get(k, float("nan")) for k in keys], r, g),
                 "rho_R_total_mentions": _rho_only([NM[w].get(k, float("nan")) for k in keys], r, g)}
    S["S5_recall_arm"] = s5
    models, note = s6_flagged_models(ctx)
    if models:
        log(f"  S6 without {models} ...")
        rows6 = {w: rank_rows(data, "lead_item", sets=omni_set_names(data, w), drop_models=tuple(models))
                 for w in WAVES}
        record("S6_without_flagged_models", gate_block(rows6, stat, RATING_FLOOR, P, C, excl, boot=False))
        S["S6_without_flagged_models"]["models_dropped"] = models
    else:
        S["S6_without_flagged_models"] = {"models_dropped": [], "verdicts": dict(primary_v),
                                          "note": note + "; MC_Snapshot lists no mismatch: S6 is identical "
                                                         "to the primary analysis"}
    if extra is not None:                    # S9: the uncentred v0.37-v0.41 rank convention
        log("  S9 uncentred within-category ranks ...")
        with uncentred():
            b9 = gate_block(ow["lead_item"], stat, RATING_FLOOR, P, C, excl, boot=False)
            h4_9 = h4_block(data, stat, boot=False)
            h5_9 = stability(ow["lead_item"]["t2"], ow["lead_item"]["t3"], stat, RATING_FLOOR, SEEDS["H5"], boot=False)
            t13_9 = stability(ow["lead_item"]["t1"], ow["lead_item"]["t3"], stat, RATING_FLOOR, None, nulls=False)
            h6_9 = h6_block(data, stat, extra["mq8_pass"], boot=False)
            mq6_9 = mq6_positive_control(data, P)
        record("S9_uncentred", b9, h4=h4_9["verdict"])
        S["S9_uncentred"].update(H4=h4_9, H5=h5_9, H5_t1_t3=t13_9, H6=h6_9, MQ6=mq6_9)
        for h, blk in (("H4", h4_9), ("H5", h5_9), ("H6", h6_9)):
            S["S9_uncentred"]["verdicts"][h] = blk["verdict"]
            if blk["verdict"] != extra[h]:
                changes.append({"sensitivity": "S9_uncentred", "hypothesis": h, "primary": extra[h],
                                "under_sensitivity": blk["verdict"]})
        if mq6_9["passes"] != extra["MQ6_passes"]:
            changes.append({"sensitivity": "S9_uncentred", "hypothesis": "MQ6_passes",
                            "primary": extra["MQ6_passes"], "under_sensitivity": mq6_9["passes"]})
    flagged, coi_sha, unknown = load_coi(ctx, data)
    if flagged is None:
        S["S7_without_coi_flagged"] = {"note": "no COI-flagged brands", "coi_file": None}
    else:
        log(f"  S7 without {len(flagged)} COI-flagged brand(s) ...")
        record("S7_without_coi_flagged", gate_block(ow["lead_item"], stat, RATING_FLOOR, P, C, excl,
                                                    excl_units=flagged, boot=False))
        S["S7_without_coi_flagged"].update(coi_file=COI_REL, coi_sha256=coi_sha, flagged=sorted(flagged),
                                           flagged_not_in_registry=unknown)
        if not flagged:
            S["S7_without_coi_flagged"]["note"] = "COI file present but lists no registry brand"
    S["verdict_changes"] = changes
    return S


def stage_c(ctx: Ctx, data: dict, selection: dict, prof_rows: list, mq: dict, log=print) -> dict:
    stat, fail = selection["stat_for_stage_c"], bool(selection["instrument_fail"])
    keys = [(r["wave"], r["substrate"], r["brand"]) for r in prof_rows]
    join = join_check(keys, omni_units(data))                         # MQ2 join (first act on P/C)
    if not join["passes"]:
        raise Halt("MQ2 join: OMNI units do not match aias_2_0_profiles.csv 1:1")
    P, C, NM = parse_profiles(prof_rows)
    excl = tuple(mq["MQ2"]["excluded_from_gate"])
    ow = {w: rank_rows(data, "lead_item", sets=omni_set_names(data, w)) for w in WAVES}
    log(f"[v1.10] Stage C with {stat} (instrument_fail={fail}); gate substrates excluded: {list(excl)}")
    prim = gate_block(ow, stat, RATING_FLOOR, P, C, excl)
    h4 = h4_block(data, stat)
    h5 = stability(ow["t2"], ow["t3"], stat, RATING_FLOOR, SEEDS["H5"])       # MQ2 exclusion: H1-H3 only
    t13 = stability(ow["t1"], ow["t3"], stat, RATING_FLOOR, None, nulls=False)
    h6 = h6_block(data, stat, bool(mq["MQ8"]["passes"]))
    gate = gate_verdict(prim["H1"]["verdict"], prim["H2"]["verdict"], prim["H3"]["verdict"], h4["verdict"], fail)
    mq6 = mq6_positive_control(data, P)
    primary_v = _verdicts(prim, h4["verdict"], fail)
    extra = {"H4": h4["verdict"], "H5": h5["verdict"], "H6": h6["verdict"], "MQ6_passes": mq6["passes"],
             "mq8_pass": bool(mq["MQ8"]["passes"])}
    sens = sensitivities(ctx, data, stat, P, C, NM, excl, primary_v, h4["verdict"], fail, log, extra=extra)
    s9 = sens["S9_uncentred"]
    sens["S9_next_to_primary"] = {
        "H1": {w: {"centred": prim["H1"]["per_wave"][w]["rho"], "uncentred": s9["detail"]["H1"]["per_wave"][w]["rho"]}
               for w in WAVES},
        "H2": {w: {"centred": prim["H2"]["per_wave"][w]["rho"], "uncentred": s9["detail"]["H2"]["per_wave"][w]["rho"]}
               for w in WAVES},
        "H3": {"centred": prim["H3"]["rho"], "uncentred": s9["detail"]["H3"]["rho"]},
        "H4": {"centred": h4["rho"], "uncentred": s9["H4"]["rho"]},
        "H5": {"centred": h5["rho"], "uncentred": s9["H5"]["rho"]},
        "H6": {"centred": h6.get("rho"), "uncentred": s9["H6"].get("rho")},
        "MQ6": {w: {"centred": mq6["per_wave"][w]["rho"], "uncentred": s9["MQ6"]["per_wave"][w]["rho"]} for w in WAVES},
        "MQ7": {"centred": selection["MQ7"]["mean_reliability"],
                "uncentred": selection.get("S9_uncentred", {}).get("MQ7", {}).get("mean_reliability")},
        "verdicts_uncentred": s9["verdicts"]}
    base = baseline_tables(data, stat)
    res = {"statistic": stat, "instrument_fail": fail, "MQ2_join": join, "gate_excluded_substrates": list(excl),
           "GATE": {"verdict": gate, "MQ6_flag": mq6["flag_gate_sensitivity"],
                    "MQ7_flag": bool(selection["MQ7"]["flag_list_composition_driven"])},
           "H1_Sep_Presence": prim["H1"], "H2_Sep_Consistency": prim["H2"], "H3_Rank_Stability": prim["H3"],
           "H4_Sep_Presence_Early": h4, "H5_Rank_LongHorizon": h5, "H5_t1_t3_descriptive": t13,
           "H6_Early_Stability": h6, "MQ6": mq6, "MQ7": selection["MQ7"], "baseline": base,
           "sensitivities": sens}
    for h in ("H1_Sep_Presence", "H2_Sep_Consistency"):
        log(f"  {h}: {res[h]['verdict']}  " + "  ".join(
            f"{w} rho={v['rho']:.3f} n={v['n']}" for w, v in res[h]["per_wave"].items()))
    for h in ("H3_Rank_Stability", "H5_Rank_LongHorizon", "H6_Early_Stability"):
        v = res[h]
        if "rho" in v:
            log(f"  {h}: {v['verdict']}  rho={v['rho']:.3f} n={v['n']} p_perm={v['p_perm']:.4f} "
                f"p_shuffle={v['p_shuffle']:.4f}")
        else:
            log(f"  {h}: {v['verdict']} ({v.get('reason')})")
    log(f"  H4_Sep_Presence_Early: {h4['verdict']}  rho={h4['rho']:.3f} n={h4['n']}")
    log(f"  GATE: {gate}   [MQ6 flag={res['GATE']['MQ6_flag']}, MQ7 flag={res['GATE']['MQ7_flag']}]")
    log(f"  S9 (uncentred ranks) verdicts: {sens['S9_uncentred']['verdicts']}")
    log(f"  S6: {sens['S6_without_flagged_models'].get('note', 'models dropped: ' + str(sens['S6_without_flagged_models'].get('models_dropped')))}")
    log(f"  sensitivity verdict changes: {len(sens['verdict_changes'])}")
    return res


def run_stage_c(ctx: Ctx, log=print) -> dict:
    if not ctx.selection_file.exists() or not ctx.stage_s_file.exists():
        raise Halt("ORDER: Stage S has not been run (no selection file); run --stage S first")
    summary = json.loads(ctx.stage_s_file.read_text())
    if sha256(ctx.selection_file) != summary["selection_sha256"]:
        raise Halt("selection file changed since Stage S")
    bad = verify_manifest(ctx.manifest_path, ctx.root)
    if bad:
        raise Halt("manifest verification failed: " + "; ".join(bad[:10]))
    if sha256(ctx.manifest_path) != summary["manifest_sha256"]:
        raise Halt("manifest changed since Stage S")
    log(f"[v1.10] manifest OK ({ctx.manifest_path.name}, dry_run={ctx.dry}); selection verified")
    data = run_extraction(ctx, log=log)
    idx = rank_table_index(data)
    if {k: v["sha256"] for k, v in idx.items()} != {k: v["sha256"] for k, v in summary["rank_tables"].items()}:
        raise Halt("re-extracted rank tables differ from the Stage S rank tables")
    selection = json.loads(ctx.selection_file.read_text())
    prof_rows = open_presence_consistency(ctx.path(PROFILES_REL), ctx.selection_file)   # step 5
    res = stage_c(ctx, data, selection, prof_rows, summary["data_quality"], log)
    coi = res["sensitivities"].get("S7_without_coi_flagged", {})
    doc = {"phase": PHASE_ID, "stage": "C", "created_utc": _now(), "dry_run": ctx.dry,
           "prereg_tag": PREREG_TAG, "manifest_sha256": summary["manifest_sha256"],
           "selection_sha256": summary["selection_sha256"],
           "stage_s_summary_sha256": sha256(ctx.stage_s_file),
           "rank_tables": summary["rank_tables"], "coi_flags_sha256": coi.get("coi_sha256"),
           "seeds": SEEDS, "draws": {"perm": N_PERM, "shuffle_H3_H5_H6": N_SHUFFLE, "MQ7": N_SHUFFLE_MQ7,
                                     "boot": N_BOOT},
           "selection": {k: selection[k] for k in ("selected", "outcome", "reliability", "n_units",
                                                    "instrument_fail", "stat_for_stage_c", "rank_convention",
                                                    "S8_without_knife_sets", "S9_uncentred") if k in selection},
           "data_quality_from_stage_s": summary["data_quality"], **res}
    ctx.verdicts_file.write_text(json.dumps(_clean(doc), indent=2, ensure_ascii=False) + "\n")
    log(f"[v1.10] verdicts written: {ctx.verdicts_file} (sha256 {sha256(ctx.verdicts_file)[:16]}...)")
    return doc


# ===========================================================================
# MAIN
# ===========================================================================


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--verify-manifest", action="store_true")
    ap.add_argument("--parity", action="store_true", help="pre-lock MQ1/MQ2 parity (no rank)")
    ap.add_argument("--stage", choices=["S", "C"])
    ap.add_argument("--dry-run", action="store_true", help="synthetic replicas only")
    a = ap.parse_args(argv)
    ctx = Ctx(dry=a.dry_run)
    if a.dry_run and not ctx.manifest_path.exists():
        print(f"[v1.10] no replica manifest at {ctx.manifest_path}; build it with "
              f"python3 {V110}/dryrun/build_dryrun_v1_10.py", file=sys.stderr)
        return 2
    try:
        if a.verify_manifest:
            bad = verify_manifest(ctx.manifest_path, ctx.root)
            print("manifest OK" if not bad else "\n".join(bad))
            return 0 if not bad else 1
        if a.parity:
            run_parity(ctx)
            return 0
        if a.stage:
            if not a.dry_run:
                ok, why = lock_status()
                if not ok:
                    print(f"[v1.10] refusing --stage {a.stage} on real data before the lock: {why}",
                          file=sys.stderr)
                    return 3
            (run_stage_s if a.stage == "S" else run_stage_c)(ctx)
            return 0
    except Halt as e:
        print(f"[v1.10] HALT: {e}", file=sys.stderr)
        return 2
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
