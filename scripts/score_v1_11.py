#!/usr/bin/env python3
"""
score_v1_11.py - AIAS v1.11 Sentiment Paper A scorer (SKELETON, DRAFT r0 - not locked).

Pre-registration: osf/methodology/v1_11/prereg/PRE_REGISTRATION_v1_11.md
Judge prompt:     osf/methodology/v1_11/prereg/judge_prompt_v1_11.md (mirrored below; a test
                  asserts the two are byte-identical)

What is implemented (deterministic, no model calls):
  - mention-window construction (the unit for long-form answers)
  - judge request building, output parsing and validation
  - unit score, per-brand Sentiment score S with its n floor, descriptives E and NV
  - agreement statistics (Krippendorff alpha ordinal, Cohen kappa), Spearman on
    within-substrate ranks, verdict bands, stratified permutation test
  - cost projection and the hard spending cap guard
What is NOT implemented on purpose:
  - judge_call(): judge calls are paid model calls and run only after the lock.
  - loaders for the confirmatory inputs (TODO at lock; see INPUTS_MANIFEST_v1_11.json).
This file computes nothing on Presence, Consistency or Ranking data at draft time.
"""
from __future__ import annotations

import json
import math
import random
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

PHASE_ID = "v1.11"
STATUS = "DRAFT r0 (not locked)"

# --------------------------------------------------------------------------------------
# Fixed rules (every number here is mirrored in PRE_REGISTRATION_v1_11.md section 4)
# --------------------------------------------------------------------------------------
VALENCES = (-2, -1, 0, 1, 2)
N_FLOOR = 6                      # S rated only with >= 6 valid units (mirrors v1.9 C* rule)
NV_MIN_EVALUATIVE = 3            # NV (descriptive) reported only with >= 3 evaluative units
WINDOW_CHAR_CAP = 1500           # mention window cap (characters)
RECOG_CHAR_CAP = 16000           # recognition answer cap (characters); longer is cut, flagged
K_CAP_PER_BRAND = 36             # max judged windows per brand x answer set x wave
EVIDENCE_MAX_WORDS = 20
MAX_PARSE_RETRIES = 2
JUDGE_FAIL_HALT_SHARE = 0.02     # > 2% failed units in any set -> halt before scoring
EXTRACTION_MISS_HALT_SHARE = 0.05  # > 5% certified mentions without a locatable window -> halt
J2_EARLY_SHARE = 0.10            # reliability judge on 10% of early-panel windows (all omnibus)
DETERMINISM_SHARE = 0.02         # J1 repeat calls on 2% of units
DETERMINISM_MIN_EXACT = 0.90

BAND_CONFIRMED_MAX = 0.30        # |rho| <= 0.30 -> CONFIRMED separable
BAND_FALSIFIED_MIN = 0.50        # |rho| >= 0.50 -> FALSIFIED
ALPHA_CONFIRMED_MIN = 0.667      # judge agreement (Krippendorff alpha, ordinal)
ALPHA_FALSIFIED_BELOW = 0.50
BRAND_AGREE_CONFIRMED_MIN = 0.80  # rho(S_J1, S_J2), within-substrate ranks
BRAND_AGREE_FALSIFIED_BELOW = 0.60
STAB_CONFIRMED_MIN = 0.50        # test-retest rho
STAB_FALSIFIED_BELOW = 0.30
ALPHA_P = 0.05
N_PERM = 10_000
N_BOOT = 10_000
SELF_PREF_OK_MAX = 5.0           # points on the 0-100 unit scale
SELF_PREF_MATERIAL_MIN = 10.0

SEEDS = {"unit_order": 111000, "window_cap": 111001, "j2_sample": 111002,
         "determinism": 111003, "perm_base": 111010, "boot": 111020, "human_sample": 111022}

# Spending: hard cap; the projected cost uses prices verified at lock (TO VERIFY).
HARD_CAP_USD = 250.0
HARD_CAP_CALLS = 30_000
COST_OVERHEAD = 1.15             # retries + token-estimate error

# --------------------------------------------------------------------------------------
# Judge prompt (byte-identical to judge_prompt_v1_11.md; tested)
# --------------------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are an annotator in a research study of how AI assistants describe brands. "
    "You will read a text written by an AI assistant and rate how favourably it describes "
    "one target brand. Rate only what the text says; do not add what you know about the "
    "brand. Reply with one JSON object and nothing else."
)

USER_TEMPLATE = """TARGET BRAND: {brand}
CATEGORY: {category}
QUESTION THE ASSISTANT WAS ANSWERING: {question}
TEXT TYPE: {text_type}

TEXT:
<<<
{text}
>>>

Rate how favourably the TEXT describes the TARGET BRAND.

Rules:
1. Rate only statements about the target brand: its products, quality, performance, value, reputation, people and conduct, and comparisons that involve it. Ignore statements about other brands unless they compare the target brand with them.
2. Being named, listed or recommended by inclusion is not an evaluation in itself. List labels and phrases that only repeat the question (for example "Top picks:" or "Brands for beginners:") are not evaluations of the target brand. Rate the words that describe the target brand itself.
3. Plain facts are neutral: history, founding date, ownership, location, product range, ingredients, price level or market position stated without judgement.
4. Evaluations count: praise or criticism by the assistant, and judgements by others that the text reports (awards, ratings, critical acclaim, complaints, recalls, controversies, lawsuits).
5. "evaluative" is true if the text contains at least one evaluation of the target brand under rule 4, and false if it contains only facts or description.
6. If favourable and unfavourable evaluations are both present, set "mixed" to true and choose the valence that reflects their overall balance (0 if they are of similar weight).
7. If the text does not refer to the target brand (the name is used as an ordinary word or for a different company, or the assistant says it does not know the brand and describes nothing), set "refers_to_brand" to false, "evaluative" to false, "mixed" to false and "valence" to 0.

Valence scale:
2 = strongly favourable: emphatic praise or endorsement of the brand ("outstanding", "the best", "exceptional quality") with no substantive reservation.
1 = favourable: a positive evaluation ("well regarded", "reliable", "good value", "award-winning"), possibly with minor reservations.
0 = neutral: no evaluation of the brand (facts or description only), or favourable and unfavourable evaluations of similar weight.
-1 = unfavourable: a negative evaluation ("overpriced", "inconsistent quality", "mixed reviews", "less refined than"), possibly with some positives.
-2 = strongly unfavourable: emphatic criticism or warning ("avoid", "poor quality", a scandal or recall presented as defining) with no substantive positive.

Reply with one JSON object with exactly these keys:
"refers_to_brand" (true or false), "evaluative" (true or false), "mixed" (true or false), "valence" (one of -2, -1, 0, 1, 2), "evidence" (the shortest quote from the TEXT, at most 20 words, that best supports the valence; an empty string if "evaluative" is false)."""

TEXT_TYPES = {
    "recognition": "the assistant's full answer about the target brand",
    "mention": "the sentences of a longer answer that mention the target brand "
               "(the rest of the answer is omitted and marked [...])",
}

OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["refers_to_brand", "evaluative", "mixed", "valence", "evidence"],
    "properties": {
        "refers_to_brand": {"type": "boolean"},
        "evaluative": {"type": "boolean"},
        "mixed": {"type": "boolean"},
        "valence": {"type": "integer", "enum": [-2, -1, 0, 1, 2]},
        "evidence": {"type": "string"},
    },
}

JUDGE_CALL_PARAMS = {  # fixed; model IDs are filled at lock (TO VERIFY), never changed after
    "temperature": 0,
    "max_output_tokens": 200,
    "tools": None,
    "web_search": False,
    "extended_reasoning": "off (or the vendor's minimum if it cannot be switched off; recorded)",
    "J1_model_id": None,   # TO VERIFY at lock: newest GA flagship, provider A (dated snapshot ID)
    "J2_model_id": None,   # TO VERIFY at lock: newest GA flagship, provider B (dated snapshot ID)
}


# --------------------------------------------------------------------------------------
# Unit construction
# --------------------------------------------------------------------------------------
def fold(s: str) -> str:
    """NFKC, accent-folded, casefolded form used for matching only (never sent to the judge)."""
    s = unicodedata.normalize("NFKC", s)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return s.casefold().replace("’", "'")


def alias_pattern(aliases: Iterable[str]) -> re.Pattern:
    """Word-boundary, case-insensitive, accent-folded alternation; longest alias first."""
    alts = sorted({fold(a).strip() for a in aliases if a and a.strip()}, key=len, reverse=True)
    if not alts:
        raise ValueError("empty alias list")
    body = "|".join(re.escape(a) for a in alts)
    return re.compile(r"(?<!\w)(?:" + body + r")(?!\w)")


CONTINUATION_MAX = 4             # segments carried after a naming segment (brand block)
_LINE_SPLIT = re.compile(r"\n|\s{2,}")   # newline, or 2+ spaces (archived flattened newlines)
_INLINE_MARK = re.compile(r"\s+(?=(?:#{1,6}|[-*•]|\d{1,2}[.)])\s+\S)")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[\"'(\[*_A-Z0-9“])")
_HEADING = re.compile(r"^\s*(#{1,6}\s|\*\*[^*]+\*\*:?\s*$|[^.!?]{0,80}:\s*$)")


def segments(text: str) -> List[str]:
    """Lines (newline or 2+ spaces), then inline headings/bullets/numbered items, then
    sentences. Each list item or sentence is one segment."""
    out: List[str] = []
    for line in _LINE_SPLIT.split(text.replace("\r\n", "\n")):
        for item in _INLINE_MARK.split(line.strip()):
            out.extend(p.strip() for p in _SENT_SPLIT.split(item.strip()) if p.strip())
    return out


def is_heading(seg: str) -> bool:
    return bool(_HEADING.match(seg))


def build_window(text: str, aliases: Sequence[str], other_aliases: Sequence[str] = (),
                 cap: int = WINDOW_CHAR_CAP) -> Optional[str]:
    """The mention window (brand block): every segment naming the brand, each followed by up to
    CONTINUATION_MAX segments until a heading/list label or a segment naming another registry
    brand; in answer order; gaps marked ' [...] '. Whole segments are added until the cap; a
    first segment longer than the cap is cut at the cap. None = no segment names the brand
    (an extraction miss, counted and reported)."""
    pat = alias_pattern(aliases)
    alts = [a for a in other_aliases if fold(a).strip() and not pat.fullmatch(fold(a).strip())]
    other = alias_pattern(alts) if alts else None
    segs = segments(text)
    folded = [fold(s) for s in segs]
    hits = [i for i, s in enumerate(folded) if pat.search(s)]
    if not hits:
        return None
    keep: List[int] = []
    for i in hits:
        if i not in keep:
            keep.append(i)
        for j in range(i + 1, min(i + 1 + CONTINUATION_MAX, len(segs))):
            if j in hits or is_heading(segs[j]) or (other and other.search(folded[j])):
                break
            if j not in keep:
                keep.append(j)
    keep.sort()
    parts: List[str] = []
    used, prev, cut = 0, None, False
    for i in keep:
        seg = segs[i]
        sep = "" if prev is None else (" " if i == prev + 1 else " [...] ")
        if prev is None and len(seg) > cap:
            parts.append(seg[:cap].rstrip())
            cut = True
            break
        if used + len(sep) + len(seg) > cap:
            cut = True
            break
        parts.append(sep + seg)
        used += len(sep) + len(seg)
        prev = i
    window = "".join(parts)
    if keep[0] > 0:
        window = "[...] " + window
    if cut or keep[-1] < len(segs) - 1:
        window = window + " [...]"
    return window


def recognition_text(text: str, cap: int = RECOG_CHAR_CAP) -> Tuple[str, bool]:
    """The recognition unit is the whole answer; cut at the cap (flagged) if longer."""
    if len(text) <= cap:
        return text, False
    return text[:cap].rstrip() + " [...]", True


def cap_windows(units: List[dict], k: int = K_CAP_PER_BRAND, seed: int = SEEDS["window_cap"]) -> List[dict]:
    """At most k windows per (answer_set, wave, brand), drawn round-robin over answering models
    in a seeded order, so no model dominates a capped brand. No-op where n <= k."""
    rng = random.Random(seed)
    groups: Dict[Tuple[str, str, str], List[dict]] = {}
    for u in units:
        groups.setdefault((u["answer_set"], u["wave"], u["brand"]), []).append(u)
    kept: List[dict] = []
    for key in sorted(groups):
        g = sorted(groups[key], key=lambda u: u["unit_id"])
        if len(g) <= k:
            kept.extend(g)
            continue
        by_model: Dict[str, List[dict]] = {}
        for u in g:
            by_model.setdefault(u["model"], []).append(u)
        for m in by_model:
            rng.shuffle(by_model[m])
        order = sorted(by_model)
        rng.shuffle(order)
        picked: List[dict] = []
        while len(picked) < k:
            for m in order:
                if by_model[m] and len(picked) < k:
                    picked.append(by_model[m].pop())
        kept.extend(sorted(picked, key=lambda u: u["unit_id"]))
    return kept


def build_request(unit: dict) -> dict:
    """Judge input. The answering model, wave and answer set are never shown to the judge."""
    user = USER_TEMPLATE.format(brand=unit["brand_display"], category=unit["category"],
                                question=unit["question"], text_type=TEXT_TYPES[unit["unit_type"]],
                                text=unit["text"])
    return {"unit_id": unit["unit_id"], "system": SYSTEM_PROMPT, "user": user,
            "schema": OUTPUT_SCHEMA, "params": {k: v for k, v in JUDGE_CALL_PARAMS.items()
                                                if not k.endswith("_model_id")}}


def judge_call(request: dict, model_id: str) -> str:  # pragma: no cover
    raise NotImplementedError("Judge calls are paid model calls; they run only after the "
                              "v1.11 lock, under the hard cap (see CostGuard).")


# --------------------------------------------------------------------------------------
# Judge output
# --------------------------------------------------------------------------------------
class JudgeOutputError(ValueError):
    pass


def parse_judge_output(raw: str) -> dict:
    """Strict parse + consistency checks. Invalid output -> JudgeOutputError (retried up to
    MAX_PARSE_RETRIES times with identical input, then the unit is JUDGE_FAIL)."""
    s = raw.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    try:
        obj = json.loads(s)
    except json.JSONDecodeError as e:
        raise JudgeOutputError(f"not JSON: {e}") from e
    if not isinstance(obj, dict) or set(obj) != set(OUTPUT_SCHEMA["required"]):
        raise JudgeOutputError("keys differ from schema")
    for k in ("refers_to_brand", "evaluative", "mixed"):
        if not isinstance(obj[k], bool):
            raise JudgeOutputError(f"{k} not boolean")
    v = obj["valence"]
    if isinstance(v, bool) or not isinstance(v, int) or v not in VALENCES:
        raise JudgeOutputError("valence outside -2..2")
    if not isinstance(obj["evidence"], str):
        raise JudgeOutputError("evidence not a string")
    if not obj["refers_to_brand"] and (v != 0 or obj["evaluative"] or obj["mixed"]):
        raise JudgeOutputError("refers_to_brand false requires valence 0, not evaluative/mixed")
    if not obj["evaluative"] and (v != 0 or obj["mixed"]):
        raise JudgeOutputError("non-evaluative text requires valence 0 and mixed false")
    obj["evidence_over_limit"] = len(obj["evidence"].split()) > EVIDENCE_MAX_WORDS  # flag only
    return obj


def unit_score(valence: int) -> float:
    """0-100 unit scale: -2 -> 0, 0 -> 50 (neutral or balanced), +2 -> 100."""
    return 25.0 * (valence + 2)


# --------------------------------------------------------------------------------------
# Brand-level score
# --------------------------------------------------------------------------------------
@dataclass
class BrandScore:
    n: int
    S: Optional[float]           # Sentiment score (None = not rated, n < N_FLOOR)
    E: Optional[float]           # evaluative share (descriptive)
    NV: Optional[float]          # mean unit score among evaluative units (descriptive)
    n_excluded: int = 0          # refers_to_brand false or JUDGE_FAIL


def brand_score(judged: Sequence[Optional[dict]], floor: int = N_FLOOR) -> BrandScore:
    """judged: parsed outputs (None = JUDGE_FAIL). Near-neutral rule: non-evaluative units stay
    in S at 50; they are not dropped. Units that do not refer to the brand are excluded."""
    valid = [j for j in judged if j is not None and j["refers_to_brand"]]
    excl = len(judged) - len(valid)
    n = len(valid)
    if n == 0:
        return BrandScore(0, None, None, None, excl)
    scores = [unit_score(j["valence"]) for j in valid]
    ev = [unit_score(j["valence"]) for j in valid if j["evaluative"]]
    E = len(ev) / n
    NV = sum(ev) / len(ev) if len(ev) >= NV_MIN_EVALUATIVE else None
    S = sum(scores) / n if n >= floor else None
    return BrandScore(n, S, E, NV, excl)


# --------------------------------------------------------------------------------------
# Statistics (stdlib only)
# --------------------------------------------------------------------------------------
def average_ranks(x: Sequence[float]) -> List[float]:
    order = sorted(range(len(x)), key=lambda i: x[i])
    ranks = [0.0] * len(x)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def pearson(x: Sequence[float], y: Sequence[float]) -> float:
    n = len(x)
    if n < 3:
        return float("nan")
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return float("nan")
    return sxy / math.sqrt(sxx * syy)


def spearman(x: Sequence[float], y: Sequence[float]) -> float:
    return pearson(average_ranks(x), average_ranks(y))


def within_group_ranks(groups: Sequence[str], x: Sequence[float]) -> List[float]:
    """Ranks within each group (substrate/category), scaled to (0, 1] so groups pool."""
    out = [0.0] * len(x)
    for g in set(groups):
        idx = [i for i, gg in enumerate(groups) if gg == g]
        r = average_ranks([x[i] for i in idx])
        for i, ri in zip(idx, r):
            out[i] = ri / len(idx)
    return out


def rho_within(groups: Sequence[str], x: Sequence[float], y: Sequence[float]) -> float:
    """The program's 'within-category' rho: Pearson on within-group ranks, pooled (v1.9)."""
    return pearson(within_group_ranks(groups, x), within_group_ranks(groups, y))


def band_verdict(abs_rho: float) -> str:
    if math.isnan(abs_rho):
        return "UNDETERMINED"
    if abs_rho <= BAND_CONFIRMED_MAX:
        return "CONFIRMED"
    if abs_rho >= BAND_FALSIFIED_MIN:
        return "FALSIFIED"
    return "MARGINAL"


def separability_verdict(abs_rhos_by_wave: Sequence[float]) -> str:
    """Three omnibus waves: CONFIRMED iff every wave <= 0.30; FALSIFIED iff >= 2 waves >= 0.50;
    MARGINAL otherwise; UNDETERMINED if any wave is undefined."""
    if any(math.isnan(r) for r in abs_rhos_by_wave):
        return "UNDETERMINED"
    if all(r <= BAND_CONFIRMED_MAX for r in abs_rhos_by_wave):
        return "CONFIRMED"
    if sum(r >= BAND_FALSIFIED_MIN for r in abs_rhos_by_wave) >= 2:
        return "FALSIFIED"
    return "MARGINAL"


def perm_test_within(groups: Sequence[str], x: Sequence[float], y: Sequence[float],
                     n_perm: int = N_PERM, seed: int = SEEDS["perm_base"]) -> Tuple[float, float]:
    """One-sided stratified permutation (y permuted within group). Returns (rho, p)."""
    obs = rho_within(groups, x, y)
    rx = within_group_ranks(groups, x)
    ry = within_group_ranks(groups, y)
    rng = random.Random(seed)
    idx_by_g: Dict[str, List[int]] = {}
    for i, g in enumerate(groups):
        idx_by_g.setdefault(g, []).append(i)
    ge = 0
    for _ in range(n_perm):
        perm = list(ry)
        for idx in idx_by_g.values():
            vals = [ry[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                perm[i] = v
        if pearson(rx, perm) >= obs:
            ge += 1
    return obs, (ge + 1) / (n_perm + 1)


def stability_verdict(rho: float, p: float) -> str:
    if math.isnan(rho):
        return "UNDETERMINED"
    if rho >= STAB_CONFIRMED_MIN and p < ALPHA_P:
        return "CONFIRMED"
    if rho < STAB_FALSIFIED_BELOW or p >= ALPHA_P:
        return "FALSIFIED"
    return "MARGINAL"


def krippendorff_alpha_ordinal(pairs: Sequence[Tuple[int, int]],
                               values: Sequence[int] = VALENCES) -> float:
    """Krippendorff's alpha, ordinal metric, two coders, no missing values in a pair."""
    vals = list(values)
    o = {(c, k): 0.0 for c in vals for k in vals}
    for a, b in pairs:
        o[(a, b)] += 1.0
        o[(b, a)] += 1.0
    n_c = {c: sum(o[(c, k)] for k in vals) for c in vals}
    n = sum(n_c.values())
    if n <= 1:
        return float("nan")

    def delta(c: int, k: int) -> float:
        lo, hi = sorted((vals.index(c), vals.index(k)))
        s = sum(n_c[vals[g]] for g in range(lo, hi + 1)) - (n_c[vals[lo]] + n_c[vals[hi]]) / 2.0
        return s * s

    d_o = sum(o[(c, k)] * delta(c, k) for c in vals for k in vals)
    d_e = sum(n_c[c] * n_c[k] * delta(c, k) for c in vals for k in vals) / (n - 1)
    if d_e == 0:
        return float("nan")
    return 1.0 - d_o / d_e


def cohen_kappa(a: Sequence, b: Sequence) -> float:
    n = len(a)
    cats = sorted(set(a) | set(b), key=str)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((list(a).count(c) / n) * (list(b).count(c) / n) for c in cats)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def judge_agreement_verdict(alpha: float, brand_rho: float) -> str:
    if math.isnan(alpha) or math.isnan(brand_rho):
        return "UNDETERMINED"
    if alpha >= ALPHA_CONFIRMED_MIN and brand_rho >= BRAND_AGREE_CONFIRMED_MIN:
        return "CONFIRMED"
    if alpha < ALPHA_FALSIFIED_BELOW or brand_rho < BRAND_AGREE_FALSIFIED_BELOW:
        return "FALSIFIED"
    return "MARGINAL"


# --------------------------------------------------------------------------------------
# Cost projection and hard cap
# --------------------------------------------------------------------------------------
def est_tokens(chars: int) -> int:
    """Planning estimate: 1 token per 4 characters of English text (rounded up)."""
    return -(-chars // 4)


@dataclass
class CostGuard:
    price_in_per_mtok: float     # USD per million input tokens (verified at lock)
    price_out_per_mtok: float    # USD per million output tokens (verified at lock)
    cap_usd: float = HARD_CAP_USD
    cap_calls: int = HARD_CAP_CALLS
    spent_usd: float = 0.0
    calls: int = 0
    log: List[dict] = field(default_factory=list)

    def call_cost(self, tok_in: int, tok_out: int) -> float:
        return (tok_in * self.price_in_per_mtok + tok_out * self.price_out_per_mtok) / 1e6

    def project(self, plan: Sequence[Tuple[int, int, int]]) -> float:
        """plan: (n_calls, tokens_in_per_call, tokens_out_per_call) rows."""
        return COST_OVERHEAD * sum(n * self.call_cost(ti, to) for n, ti, to in plan)

    def check_plan(self, plan: Sequence[Tuple[int, int, int]]) -> bool:
        n_calls = sum(int(n * COST_OVERHEAD) for n, _, _ in plan)
        return self.project(plan) <= self.cap_usd and n_calls <= self.cap_calls

    def charge(self, tok_in: int, tok_out: int) -> None:
        """Record actual usage; raises before a call would push spend past the cap."""
        c = self.call_cost(tok_in, tok_out)
        if self.spent_usd + c > self.cap_usd or self.calls + 1 > self.cap_calls:
            raise RuntimeError("HARD CAP reached: stop judging; unjudged units are reported")
        self.spent_usd += c
        self.calls += 1


if __name__ == "__main__":  # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--build-units", action="store_true",
                    help="TODO at lock: build the frozen unit table from INPUTS_MANIFEST (no calls)")
    ap.add_argument("--dry-run", action="store_true", help="build requests, count tokens, no calls")
    a = ap.parse_args()
    raise SystemExit("v1.11 is a DRAFT: loaders and the judge run are added at lock (TODO).")
