#!/usr/bin/env python3
"""
score_v1_10.py - AIAS v1.10, Ranking component, Paper A
(instrument specification + cross-category baseline + separability gate).

STATUS: DRAFT r1 SKELETON (2026-11-10). NOT LOCKED. Constants are transcribed from
osf/methodology/v1_10/prereg/PRE_REGISTRATION_v1_10.md (section cited inline).
Implemented and unit-tested on synthetic data only (scripts/test_score_v1_10.py):
the rank extractor (rules E0-E7), the candidate statistics, the rating floor, the
Stage S selection rule, the correlation / permutation / shuffle machinery, the verdict
bands and the gate rule. TODO before the lock: the archive loaders (one per frozen
input set, see LOADERS) and the end-to-end run. No network, no model calls.

Enforced order (ORDER section of the pre-registration):
  verify manifest -> extract ranks for every frozen set -> MQ1-MQ5 data-quality checks
  -> Stage S (statistic selection on the early panel, blind to Presence/Consistency)
  -> write selection_v1_10.json -> only then open the Presence/Consistency table
  -> Stage C (gate H1-H3, secondary H4-H6, controls MQ6-MQ7) -> verdicts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import numpy as np

# ===========================================================================
# TRANSCRIBED CONSTANTS (draft r1)
# ===========================================================================
PHASE_ID = "v1.10"
PREREG_TAG = "v1.10-prereg-r1"            # not created yet (draft)
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "osf/methodology/v1_10/registries/INPUTS_MANIFEST_v1_10.json"
OUTDIR = ROOT / "osf/methodology/v1_10/outputs"
SELECTION_FILE = OUTDIR / "selection_v1_10.json"

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
N_PERM = 10_000
N_SHUFFLE = 2_000
N_BOOT = 2_000
SEEDS = {"H1": 110001, "H2": 110002, "H3": 110003, "H4": 110004, "H5": 110005,
         "H6": 110006, "SHUFFLE": 110010, "BOOT": 110020, "MQ7": 110030}
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
WAVES = ["t1", "t2", "t3"]

# ===========================================================================
# RANK EXTRACTION (pre-registration section EXTRACTION, rules E0-E7)
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


# ===========================================================================
# CANDIDATE STATISTICS (section STATISTICS). Every score is oriented so that
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


# ===========================================================================
# CORRELATION MACHINERY (v0.37 / v0.41 conventions)
# ===========================================================================


def _rankdata(x):
    x = np.asarray(x, float)
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    xs = x[order]
    i = 0
    while i < len(x):
        j = i
        while j + 1 < len(x) and xs[j + 1] == xs[i]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


def _pearson(a, b):
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d > 0 else float("nan")


def within_ranks(values, groups):
    values, groups = np.asarray(values, float), np.asarray(groups)
    out = np.empty(len(values))
    for g in dict.fromkeys(groups.tolist()):
        idx = np.where(groups == g)[0]
        out[idx] = _rankdata(values[idx])
    return out


def keep_categories(groups, min_units: int = MIN_UNITS_PER_CATEGORY):
    """Mask of units whose category has >= min_units units in this comparison."""
    groups = np.asarray(groups)
    return np.array([np.sum(groups == g) >= min_units for g in groups], bool)


def pooled_within_rho(x, y, groups):
    """Pooled within-category Spearman: Pearson of within-category average ranks."""
    if len(x) < 3:
        return float("nan")
    return _pearson(within_ranks(x, groups), within_ranks(y, groups))


def perm_p(x, y, groups, obs, seed, sided, n_draws=N_PERM):
    """Within-category permutation null: y permuted within category. (hits+1)/(N+1)."""
    if not np.isfinite(obs):
        return float("nan")
    rng = np.random.default_rng(seed)
    groups = np.asarray(groups)
    rx = within_ranks(x, groups)
    ry = within_ranks(y, groups)
    gidx = [np.where(groups == g)[0] for g in dict.fromkeys(groups.tolist())]
    idx = np.arange(len(ry))
    hits = 0
    for _ in range(n_draws):
        for g in gidx:
            idx[g] = rng.permutation(g)
        r = _pearson(rx, ry[idx])
        hits += (r >= obs - 1e-12) if sided == "one" else (abs(r) >= abs(obs) - 1e-12)
    return (hits + 1) / (n_draws + 1)


def boot_ci(x, y, groups, seed, n_draws=N_BOOT, level=0.90):
    """Percentile CI of the pooled within-category rho; units resampled within category."""
    rng = np.random.default_rng(seed)
    x, y, groups = np.asarray(x, float), np.asarray(y, float), np.asarray(groups)
    gidx = [np.where(groups == g)[0] for g in dict.fromkeys(groups.tolist())]
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
    a uniformly random order (no ties). List length n and the named set are kept."""
    by_answer = defaultdict(list)
    for r in rows:
        by_answer[(r["panel"], r["wave"], r["category"], r["answer_id"])].append(r)
    out = []
    for grp in by_answer.values():
        perm = rng.permutation(len(grp)) + 1
        for r, p in zip(grp, perm):
            out.append({**r, "k_mid": float(p), "k_min": int(p)})
    return out


# ===========================================================================
# STAGE S - statistic selection (section SELECTION; blind to P and C)
# ===========================================================================


def split_half_reliability(rows_a, rows_b, stat: str) -> tuple[float, int]:
    """rows_a / rows_b: rank rows of the two halves (odd vs even run_idx). Units rated in
    both halves; categories with >= MIN_UNITS_PER_CATEGORY units. Returns (r_SB, n)."""
    sa, sb = score_units(rows_a), score_units(rows_b)
    keys = [k for k in sa if k in sb and sa[k]["rated"] and sb[k]["rated"]]
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
# VERDICT RULES (section HYPOTHESES)
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


def gate_verdict(h1: str, h2: str, h3: str, h4: str | None = None) -> str:
    """GATE: FAIL if any of H1-H3 FALSIFIED; else UNDETERMINED if any UNDETERMINED;
    PASS if all three CONFIRMED (downgraded to MARGINAL if the early-panel replication
    H4 is FALSIFIED); MARGINAL otherwise."""
    trio = (h1, h2, h3)
    if "FALSIFIED" in trio:
        return "FAIL"
    if "UNDETERMINED" in trio:
        return "UNDETERMINED"
    if all(v == "CONFIRMED" for v in trio):
        return "MARGINAL" if h4 == "FALSIFIED" else "PASS"
    return "MARGINAL"


# ===========================================================================
# INPUTS (section FROZEN INPUTS) - manifest verification implemented; loaders TODO
# ===========================================================================


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    """Git blob id as git stores it: for a symlink, the link text (not the target)."""
    p = Path(path)
    data = str(p.readlink()).encode() if p.is_symlink() else p.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def verify_manifest(manifest_path: Path = MANIFEST, root: Path = ROOT) -> list[str]:
    """Every frozen file must match its SHA-256 and git blob; returns mismatches
    (empty list = pass). Any mismatch halts the run (DEVIATIONS policy)."""
    man = json.loads(Path(manifest_path).read_text())
    bad = []
    for e in man["files"]:
        p = root / e["path"]
        if not p.exists():
            bad.append(f"missing: {e['path']}")
            continue
        if sha256(p) != e["sha256"] or git_blob_sha1(p) != e["git_blob"]:
            bad.append(f"hash mismatch: {e['path']}")
    return bad


def open_presence_consistency(path: Path):
    """Stage C input. Refuses to open P/C before Stage S has written its selection."""
    if not SELECTION_FILE.exists():
        raise RuntimeError("ORDER: Stage S selection must exist before P/C are opened")
    import csv
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


LOADERS = {
    # TODO(v1.10 before lock): each loader yields answers as
    # {"panel","wave","category","answer_id","model","frame_or_prompt","run_idx","text"}
    # and the phase registry {canonical: [aliases]}; empty/error answers are yielded
    # with text "" and counted as MISSING (MQ4), never as "no brand named".
    "early_v09": "data/<cat>/results_enriched_v09_*.csv: raw_response, prompt_id, model_version, run_idx, call_status; registry osf_staging/v09/registries/brands_<cat>.json",
    "early_v06": "data/<cat>/results_v2_2026043*.csv (2 models); registry registries/brands_<cat>.json",
    "early_single": "v1.0 household / knives, v0.14 premium_tea, v0.16 kitchen_knives CSVs; registries/brands_*.json",
    "omni_v20_v22": "osf/{v20,v21,v22}/phase_b_results.csv (+ osf/v34/data, osf/v41/data copies): model, frame_id, response_text; detector scripts/score_v2x.detect_mention",
    "omni_v19": "osf/v19/phase_b_responses.jsonl (+ v34/v41 copies): panel_model, query_id, response; registry osf/v19/panel_registry_v0_19.csv; parity vs phase_b_results.csv",
    "omni_v23": "osf/v23/data/v23_phase_b_raw.json (+ copies): response; registry inline; parity vs v23_phase_b_scored.json",
    "held_v38_v39": "osf/v38/data/v38_raw.json, osf/v39/data/v39_raw.json (+ registries)",
    "baseline_v28": "osf/v28/data/phase_b_results.csv",
    "paperB_v32": "osf/v32/data/phase_b_A.csv, phase_b_B.csv (frozen now, analysed in Paper B)",
}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--verify-manifest", action="store_true")
    ap.add_argument("--stage", choices=["S", "C"], help="TODO: end-to-end stages")
    a = ap.parse_args(argv)
    if a.verify_manifest:
        bad = verify_manifest()
        print("manifest OK" if not bad else "\n".join(bad))
        return 0 if not bad else 1
    if a.stage:
        raise NotImplementedError("v1.10 draft r1: loaders are TODO (see LOADERS)")
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
