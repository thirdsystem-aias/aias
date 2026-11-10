#!/usr/bin/env python3
"""
score_v1_11.py - AIAS v1.11, Sentiment component, Paper A
(AI-judged valence instrument, cross-category baseline, separability gate).

STATUS: r1 pre-lock (2026-11-10). Constants are transcribed from
osf/methodology/v1_11/prereg/PRE_REGISTRATION_v1_11.md (section cited inline) and from the
runner's decisions of 2026-11-10 (PRE_REGISTRATION section 15). Loaders, the v1.10 mention
extractor (E2), the Ranking statistic and the rank-correlation machinery are NOT rewritten:
they are imported from scripts/score_v1_10.py, a byte-identical copy of the file locked at tag
v1.10-prereg-r2 (git blob 0f8b981b; asserted by the tests and by the input manifest).

Modes
  --verify-manifest  SHA-256 and git blob of every frozen input (INPUTS_MANIFEST_v1_11.json)
  --parity           pre-lock: parse completion; mention parity (F: v1.10's E2 extractor vs the
                     certified mention record; E: E2 vs the archived brands_canonical,
                     descriptive); unit join on key columns. No window, no valence, no P, C* or R.
  --build-units      U0 (pre-lock; no model call, no valence): unit table, window cap, J2 sample,
                     self-consistency sample, Paper B human-label sample.
  --stage J          after the lock and the frozen judge outputs: parse -> S -> H1 and the
                     self-consistency check. Reads no P, C* or R value.
  --stage C          after Stage J: opens P / C* (aias_2_0_profiles.csv) and R* (v1.10's locked
                     code) -> H2-H9, sensitivities, descriptives -> v1_11_verdicts.json.
  --dry-run          any mode on the synthetic replicas in osf/methodology/v1_11/dryrun/.
  --lock-manifest    content lock, last step: prereg/LOCK_MANIFEST_v1_11.sha256 over LOCK_FILES.
  --write-anchor --osf-deposit "<where>"
                     after the tag is pushed: anchor/git_anchor_v1_11.json from the tag's tree
                     (ANCHOR_FIELDS; checked by anchor_problems, as judge_v1_11.py --run does).
No model call in this file (the judge calls are scripts/judge_v1_11.py); --write-anchor runs
git ls-remote against origin.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import random
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import score_v1_10 as V  # noqa: E402  (byte-identical copy of v1.10-prereg-r2:scripts/score_v1_10.py)

# ======================================================================================
# 0. IDENTITY AND PATHS
# ======================================================================================
PHASE_ID = "v1.11"
STATUS = "r1 pre-lock (2026-11-10)"
PREREG_TAG = "v1.11-prereg-r1"
ROOT = HERE.parent
V111 = "osf/methodology/v1_11"
MANIFEST = ROOT / V111 / "registries/INPUTS_MANIFEST_v1_11.json"
PREREG_DIR = ROOT / V111 / "prereg"
OUTDIR = ROOT / V111 / "outputs"
DATA_DIR = ROOT / V111 / "data"
ANCHOR_FILE = ROOT / V111 / "anchor/git_anchor_v1_11.json"
DRY_DIR = ROOT / V111 / "dryrun"
DRY_ROOT = DRY_DIR / "replica"
DRY_MANIFEST = DRY_DIR / "INPUTS_MANIFEST_dryrun_v1_11.json"
DRY_OUTDIR = DRY_DIR / "outputs"

# v1.10 (Ranking) objects used by H5 (decision 6). The scorer copy and the v0.23 registry are in
# this tree (byte-identical to the tag); the Stage S selection and rank-table index live on branch
# v1.10 (commit 0399a0b) and are read from the git object store by blob id, SHA-256-checked.
V110_TAG = "v1.10-prereg-r2"
V110_SCORER_BLOB = "0f8b981b2895a325b50629c85f8e0e6ce8e876f5"
V110_STAGE_S_COMMIT = "0399a0b861874efe54e35fd11cb2d5d98d627c99"
V110_SELECTION_REL = "osf/methodology/v1_10/outputs/selection_v1_10.json"
V110_RANK_INDEX_REL = "osf/methodology/v1_10/outputs/rank_tables_index_v1_10.json"
V110_VERDICTS_REL = "osf/methodology/v1_10/outputs/v1_10_verdicts.json"
V110_BRANCH = "v1.10"
V110_SELECTED_EXPECTED = "MNP"            # selection_v1_10.json, Stage S of 2026-11-10

PROFILES_REL = "osf/aias_2_0/aias_2_0_profiles.csv"       # P and C* (as v1.10; decision 12)
V19_TABLE_REL = "osf/methodology/v1_9/v1_9_unit_table.csv"  # cross-check of P and C* only

# ======================================================================================
# 1. FIXED RULES (PRE_REGISTRATION sections 4-8; decisions in section 15)
# ======================================================================================
VALENCES = (-2, -1, 0, 1, 2)
N_FLOOR = 6                      # S rated only with >= 6 valid units (v1.9 C* rule)
NV_MIN_EVALUATIVE = 3            # NV (descriptive) only with >= 3 evaluative units
WINDOW_CHAR_CAP = 1500           # mention window cap (characters)
RECOG_CHAR_CAP = 16000           # recognition answer cap (characters); longer is cut, flagged
K_CAP_PER_BRAND = 36             # max judged windows per brand x answer set x wave
EVIDENCE_MAX_WORDS = 20
MAX_PARSE_RETRIES = 2            # invalid output: 2 retries with identical input, then JUDGE_FAIL
JUDGE_FAIL_HALT_SHARE = 0.02     # > 2% JUDGE_FAIL in any set (per judge) -> halt before scoring
EXTRACTION_MISS_HALT_SHARE = 0.05  # > 5% certified mentions without a window in a set -> halt
J2_EARLY_SHARE = 0.10            # J2 judges 10% of E windows (stratified); all R and F
SELFCON_SHARE = 0.05             # self-consistency: 5% of units judged twice by the same judge
SELFCON_MIN_EXACT = 0.90         # flag (no halt) below this exact valence agreement

BAND_CONFIRMED_MAX = 0.30        # |rho| <= 0.30 -> CONFIRMED separable
BAND_FALSIFIED_MIN = 0.50        # |rho| >= 0.50 -> FALSIFIED
ALPHA_CONFIRMED_MIN = 0.667      # H1: Krippendorff alpha (ordinal)
ALPHA_FALSIFIED_BELOW = 0.50
BRAND_AGREE_CONFIRMED_MIN = 0.80  # H1: rho_w(S_J1, S_J2)
BRAND_AGREE_FALSIFIED_BELOW = 0.60
STAB_CONFIRMED_MIN = 0.50        # H4 / H6
STAB_FALSIFIED_BELOW = 0.30
ALPHA_P = 0.05
N_PERM = 10_000
N_BOOT = 10_000
CI_LEVEL = 0.95
MIN_UNITS_POOLED = 20            # a pooled statistic needs >= 20 units ...
MIN_GROUPS = 3                   # ... from >= 3 substrates / categories ...
MIN_UNITS_PER_GROUP = 4          # ... a substrate / category enters only with >= 4 units
MIN_UNITS_SINGLE = 20            # H8 (one substrate) and each H9 group
SELF_PREF_OK_MAX = 5.0           # H9, points on the 0-100 unit scale
SELF_PREF_MATERIAL_MIN = 10.0

SEEDS = {"unit_order": 111000, "window_cap": 111001, "j2_sample": 111002, "selfcon": 111003,
         "e_half": 111004, "H4": 111011, "H6": 111012, "boot": 111020, "human_sample": 111022}
WAVES = ["t1", "t2", "t3"]
OMNI = ["v0.19", "v0.20", "v0.21", "v0.22", "v0.23"]
DENON = ("v0.19", "Denon")       # decision 4: every gate statistic also without Denon (v0.19)

# Spending (PRE_REGISTRATION section 7; budget redesign of 2026-11-10 under Pablo's rule of
# 2026-11-10, 8:03 am: "at most $100 of paid model calls per paper, hard cap")
HARD_CAP_USD = 100.0             # hard stop, from recorded usage plus worst cases in flight
PAUSE_USD = 80.0                 # recorded spend at which the run pauses and Pablo is asked
PAUSE_SHARE = PAUSE_USD / HARD_CAP_USD
PLAN_TARGET_USD = PAUSE_USD      # the binding projection (with overhead) must fit under the pause
HARD_CAP_CALLS = 30_000
COST_OVERHEAD = 1.15             # retries + token-estimate error (planning only)
MAX_OUTPUT_TOKENS = 4096         # output cap, visible output + reasoning (was 16,384; section 7)
PLAN_OUT_VISIBLE = 100           # planning: visible JSON tokens per call (measured max 53, o200k)
PLAN_REASONING = 270             # planning: reasoning tokens per call = p90 of GPT-6 Astra's
                                 # reasoning tokens at default effort on the program's probes
                                 # (osf/v42/prereg/cost_inputs_v0_42.txt, branch v0.42)
CALIBRATION_CALLS = 200          # binding projection after the first 200 calls of each judge
# Input tokens (planning): measured offline with o200k_base on every judge request
# (prereg/token_counts_v1_11.json: 4.547 request characters per token), times a vendor factor:
# Anthropic 1.30 (its pricing page: models 4.7 and later use a tokenizer producing about 30% more
# tokens for the same text), OpenAI and Google 1.10 (tokenizers unpublished; margin).
O200K_CHARS_PER_TOKEN = 4.547
TOKEN_FACTOR = {"anthropic": 1.30, "openai": 1.10, "google": 1.10}
# US$ per 1M tokens (input, output; output includes reasoning / thinking), from the vendors' own
# pricing pages, accessed 2026-11-10 (PRICE_SOURCES). Standard (synchronous) and batch.
PRICES = {
    "claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0), "claude-fable-5-2": (8.0, 40.0),
    "gpt-6-astra": (10.0, 50.0), "gpt-6.1-sol": (2.0, 10.0),
    "gemini-4-argon": (2.0, 10.0)}
PRICES_BATCH = {
    "claude-opus-5-5": (2.0, 10.0), "claude-sonnet-5-5": (1.0, 5.0), "claude-fable-5-2": (4.0, 20.0),
    "gpt-6-astra": (5.0, 25.0), "gpt-6.1-sol": (1.0, 5.0),
    "gemini-4-argon": (1.0, 5.0)}
PRICE_CHANGES = {"gemini-4-argon": ("2026-12-01T00:00:00+00:00", (4.0, 20.0))}
PRICE_CHANGES_BATCH = {"gemini-4-argon": ("2026-12-01T00:00:00+00:00", (2.0, 10.0))}
PRICE_SOURCES = {
    "anthropic": "https://platform.claude.com/docs/en/about-claude/pricing (accessed 2026-11-10)",
    "openai": "https://developers.openai.com/api/docs/pricing (accessed 2026-11-10; Standard and Batch tabs)",
    "google": "https://ai.google.dev/gemini-api/docs/pricing (accessed 2026-11-10; Standard and Batch tabs)",
}
BATCH_MAX_REQUESTS = 500         # requests per submitted batch (bounds the worst case reserved)
BATCH_WINDOW_HOURS = 24          # both vendors' batch completion window
BATCH_POLL_SECONDS = 60

# ======================================================================================
# 2. JUDGES AND THE JUDGE PROMPT (prompt byte-identical to judge_prompt_v1_11.md; tested)
# ======================================================================================
# Budget redesign (2026-11-10; section 7, decision 21): J1 Claude Opus 5.5 (Anthropic's tier below
# its flagship Claude Fable 5.2) through the Message Batches API; J2 GPT-6.1 Sol (OpenAI's tier
# below its flagship GPT-6 Astra, which was the draft's J2) through the Batch API; alternate Gemini 4 Argon
# (synchronous API, contingency only). No sampling parameter is sent to any judge; reasoning runs
# at the lowest effort the vendor documents for the model ("low" for all three; vendor model pages
# accessed 2026-11-10).
JUDGES = {
    "J1": {"model_id": "claude-opus-5-5", "name": "Claude Opus 5.5", "provider": "anthropic", "mode": "batch",
           "reasoning_param": {"output_config": {"effort": "low"}}},
    "J2": {"model_id": "gpt-6.1-sol", "name": "GPT-6.1 Sol", "provider": "openai", "mode": "batch",
           "reasoning_param": {"reasoning": {"effort": "low"}}},
    "ALT": {"model_id": "gemini-4-argon", "name": "Gemini 4 Argon", "provider": "google", "mode": "sync",
            "reasoning_param": {"thinking_config": {"thinking_level": "low"}}},
}
JUDGE_CALL_POLICY = {
    "sampling_parameters": "none sent (no temperature, top_p or top_k) to any judge",
    "reasoning": "lowest documented effort, fixed per model (JUDGES[...]['reasoning_param'])",
    "endpoint": "J1 and J2: the vendor's batch API (50% of list price); alternate: synchronous API",
    "max_output_tokens": MAX_OUTPUT_TOKENS,
    "tools": None, "web_search": False,
    "response_schema": None,     # prompt-only JSON for every judge (decision 1)
    "messages": "system = SYSTEM_PROMPT; one user message = USER_TEMPLATE filled; no prior turns",
}

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

# {category} shown to the judge: the registry's category, in plain words (fixed; listed in
# judge_prompt_v1_11.md). Keys: OMNI substrate ids and EARLY category codes.
CATEGORY_LABELS = {
    "v0.19": "audiophile headphones", "v0.20": "skincare", "v0.21": "cosmetics",
    "v0.22": "automotive", "v0.23": "premium spirits",
    "pm": "project management software", "finance": "personal finance apps",
    "oliveoil": "premium olive oil", "running": "running shoes",
    "skincare": "premium facial skincare", "household": "household goods retail",
    "knives": "premium kitchen knives", "premium_tea": "premium tea",
}


class Halt(V.Halt):
    """A pre-registered halt condition (manifest mismatch, extraction misses > 5%, JUDGE_FAIL > 2%,
    order violation, failed join, v1.10 object mismatch)."""


# ======================================================================================
# 3. UNIT CONSTRUCTION (PRE_REGISTRATION section 4.1)
# ======================================================================================
def fold(s: str) -> str:
    """NFKC, accent-folded, casefolded form used for matching only (never sent to the judge)."""
    s = unicodedata.normalize("NFKC", s)
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    return s.casefold().replace("’", "'")


def alias_pattern(aliases: Iterable[str]) -> re.Pattern:
    """Word-bounded, case-insensitive, accent-folded alternation; longest alias first."""
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


def segment_spans(text: str) -> List[Tuple[str, int, int]]:
    """Segments with their source spans in text.replace('\\r\\n', '\\n'): lines (newline or 2+
    spaces), then inline headings / bullets / numbered items, then sentences. Only whitespace
    lies between consecutive segments, so each one is found by a forward search."""
    t = text.replace("\r\n", "\n")
    out: List[Tuple[str, int, int]] = []
    pos = 0
    for line in _LINE_SPLIT.split(t):
        for item in _INLINE_MARK.split(line.strip()):
            for p in _SENT_SPLIT.split(item.strip()):
                p = p.strip()
                if not p:
                    continue
                i = t.find(p, pos)
                if i < 0:                                  # cannot happen (see docstring)
                    raise ValueError("segment not found in source text")
                out.append((p, i, i + len(p)))
                pos = i + len(p)
    return out


def segments(text: str) -> List[str]:
    return [s for s, _a, _b in segment_spans(text)]


def is_heading(seg: str) -> bool:
    return bool(_HEADING.match(seg))


def fold_map(text: str) -> Tuple[str, List[int]]:
    """fold() character by character, with the source index of every output character."""
    out, idx = [], []
    for i, ch in enumerate(text):
        f = fold(ch)
        out.append(f)
        idx.extend([i] * len(f))
    return "".join(out), idx


class AnswerText:
    """One answer prepared for window building: segments with source spans and the folded text
    with its source index. Brand matches are found on the WHOLE folded answer and mapped back to
    segments, so an alias that the sentence splitter cuts ('e.l.f. Cosmetics', 'St. George
    Spirits', 'J.A. Henckels') is still located (pre-lock fix, PRE_REGISTRATION section 15)."""

    def __init__(self, text: str):
        self.t = text.replace("\r\n", "\n")
        self.segs = segment_spans(self.t)
        self.f, self.idx = fold_map(self.t)

    def spans(self, pat: Optional[re.Pattern]) -> List[Tuple[int, int]]:
        if pat is None:
            return []
        return [(self.idx[m.start()], self.idx[m.end() - 1] + 1) for m in pat.finditer(self.f)
                if m.end() > m.start()]


def other_pattern(pat: re.Pattern, other_aliases: Sequence[str]) -> Optional[re.Pattern]:
    alts = [a for a in other_aliases if fold(a).strip() and not pat.fullmatch(fold(a).strip())]
    return alias_pattern(alts) if alts else None


def build_window(text: str, aliases: Sequence[str], other_aliases: Sequence[str] = (),
                 cap: int = WINDOW_CHAR_CAP, *, pat: Optional[re.Pattern] = None,
                 other: Optional[re.Pattern] = None, prepared: Optional[AnswerText] = None,
                 other_given: bool = False) -> Optional[str]:
    """The mention window (brand block): every segment naming the brand, each followed by up to
    CONTINUATION_MAX segments until a heading / list label or a segment naming another registry
    brand; in answer order; gaps marked ' [...] '. Whole segments are added until the cap; a first
    segment longer than the cap is cut at the cap. None = no segment names the brand (an
    extraction miss, counted and reported)."""
    A = prepared if prepared is not None else AnswerText(text)
    pat = pat if pat is not None else alias_pattern(aliases)
    if not other_given and other is None:
        other = other_pattern(pat, other_aliases)
    segs = A.segs
    own = A.spans(pat)
    if not segs or not own:
        return None
    oth = A.spans(other)

    def touches(spans, a, b):
        return any(s < b and e > a for s, e in spans)

    hits = [i for i, (_s, a, b) in enumerate(segs) if touches(own, a, b)]
    if not hits:
        return None
    hitset = set(hits)
    keep: List[int] = []
    for i in hits:
        if i not in keep:
            keep.append(i)
        for j in range(i + 1, min(i + 1 + CONTINUATION_MAX, len(segs))):
            sj, a, b = segs[j]
            if j in hitset or is_heading(sj) or touches(oth, a, b):
                break
            if j not in keep:
                keep.append(j)
    keep.sort()
    parts: List[str] = []
    used, prev, cut = 0, None, False
    for i in keep:
        seg = segs[i][0]
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


def is_bare(window: str, pat: re.Pattern) -> bool:
    """'Bare' window (descriptive): fewer than 4 words besides the brand name (feasibility rule)."""
    rest = pat.sub(" ", fold(window.replace("[...]", " ")))
    return len(re.findall(r"[a-z]{2,}", rest)) < 4


def recognition_text(text: str, cap: int = RECOG_CHAR_CAP) -> Tuple[str, bool]:
    """The recognition unit is the whole answer; cut at the cap (flagged) if longer."""
    if len(text) <= cap:
        return text, False
    return text[:cap].rstrip() + " [...]", True


def cap_windows(units: List[dict], k: int = K_CAP_PER_BRAND, seed: int = SEEDS["window_cap"]) -> List[dict]:
    """At most k windows per (set, wave, brand), drawn round-robin over answering models in a
    seeded order, so no model dominates a capped brand. No-op where n <= k."""
    rng = random.Random(seed)
    groups: Dict[Tuple[str, str, str], List[dict]] = {}
    for u in units:
        groups.setdefault((u["set"], u["wave"], u["brand"]), []).append(u)
    kept: List[dict] = []
    for key in sorted(groups):
        g = sorted(groups[key], key=lambda u: u["unit_id"])
        if len(g) <= k:
            kept.extend(g)
            continue
        by_model: Dict[str, List[dict]] = {}
        for u in g:
            by_model.setdefault(u["model"], []).append(u)
        for m in sorted(by_model):
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


def _k_of(share: float, n: int) -> int:
    return int(math.floor(share * n + 0.5))


def stratified_sample(units: List[dict], share: float, stratum, seed: int) -> List[str]:
    """Seeded random sample of round(share * n) unit ids within each stratum (strata sorted)."""
    rng = random.Random(seed)
    strata: Dict[tuple, List[str]] = defaultdict(list)
    for u in units:
        strata[stratum(u)].append(u["unit_id"])
    out: List[str] = []
    for s in sorted(strata, key=lambda x: tuple(map(str, x))):
        ids = sorted(strata[s])
        rng.shuffle(ids)
        out.extend(sorted(ids[:_k_of(share, len(ids))]))
    return sorted(out)


def j2_sample(units: List[dict]) -> List[str]:
    """J2's E sample: 10% of judged E windows by category x answering model (seed 111002)."""
    return stratified_sample([u for u in units if u["block"] == "E"], J2_EARLY_SHARE,
                             lambda u: (u["category"], u["model"]), SEEDS["j2_sample"])


def selfcon_sample(units: List[dict]) -> List[str]:
    """Self-consistency repeat sample: 5% of judged units within block (seed 111003)."""
    return stratified_sample(units, SELFCON_SHARE, lambda u: (u["block"],), SEEDS["selfcon"])


HUMAN_PER_CATEGORY = 40
HUMAN_WAVE_SPLIT = {"t1": 14, "t2": 13, "t3": 13}
HUMAN_MAX_PER_BRAND = 3
HUMAN_RECOG_PER_BRAND = 2


def _human_fill(pool, quotas, cell_of, rng, max_per_brand):
    by_cell: Dict[tuple, Dict[str, List[dict]]] = defaultdict(lambda: defaultdict(list))
    for u in sorted(pool, key=lambda u: u["unit_id"]):
        by_cell[cell_of(u)][str(u["frame"])].append(u)
    for c in sorted(by_cell, key=lambda x: tuple(map(str, x))):
        for fr in sorted(by_cell[c]):
            rng.shuffle(by_cell[c][fr])
    brand_n: Counter = Counter()
    picked: List[dict] = []

    def take(c, q):
        frames = sorted(by_cell.get(c, {}))
        rng.shuffle(frames)
        got = 0
        while got < q:
            progressed = False
            for fr in frames:
                lst = by_cell[c][fr]
                while lst and brand_n[lst[-1]["brand"]] >= max_per_brand:
                    lst.pop()
                if lst and got < q:
                    u = lst.pop()
                    picked.append(u)
                    brand_n[u["brand"]] += 1
                    got += 1
                    progressed = True
            if not progressed:
                break
        return got

    short = 0
    for c in sorted(quotas, key=lambda x: tuple(map(str, x))):
        short += quotas[c] - take(c, quotas[c])
    while short > 0:                      # move a shortfall to cells with candidates left
        moved = False
        for c in sorted(by_cell, key=lambda x: tuple(map(str, x))):
            if short and take(c, 1):
                short -= 1
                moved = True
        if not moved:
            break
    return picked, short


def human_sample(units: List[dict], seed: int = SEEDS["human_sample"]) -> Tuple[List[dict], dict]:
    """Paper B human-label sample (PRE_REGISTRATION section 9), drawn at U0 before any judge call:
    40 windows per category (5 omnibus categories with t1/t2/t3 = 14/13/13; 8 early categories),
    equal allocation over the six answering models (7,7,7,7,6,6; seeded), frames as even as the
    cells allow, at most 3 units per brand per category, bare windows at their natural share; plus
    2 recognition answers per v0.23 brand from different models and waves."""
    rng = random.Random(seed)
    picked: List[dict] = []
    report: dict = {"per_category": {}, "shortfalls": {}}
    cats = sorted({(u["block"], u["category"]) for u in units if u["block"] in ("F", "E")})
    for blk, cat in cats:
        pool = [u for u in units if u["block"] == blk and u["category"] == cat]
        models = sorted({u["model"] for u in pool})
        order = models[:]
        rng.shuffle(order)
        base, rem = divmod(HUMAN_PER_CATEGORY, len(models))
        mq = {m: base + (1 if m in order[:rem] else 0) for m in models}
        if blk == "F":
            quotas = {}
            per_wave = {w: n for w, n in HUMAN_WAVE_SPLIT.items()}
            extra_models = [m for m in order if mq[m] > base]
            extra_waves = []
            for w in WAVES:
                k = per_wave[w] - base * len(models) // len(WAVES)
                extra_waves += [w] * max(0, k)
            per_cell_base = base // len(WAVES) if base % len(WAVES) == 0 else None
            if per_cell_base is None:     # general fallback: spread each model's quota over waves
                for m in models:
                    for j, w in enumerate(WAVES):
                        quotas[(w, m)] = mq[m] // len(WAVES) + (1 if j < mq[m] % len(WAVES) else 0)
            else:
                for m in models:
                    for w in WAVES:
                        quotas[(w, m)] = per_cell_base
                for m, w in zip(extra_models, extra_waves):
                    quotas[(w, m)] += 1
            got, short = _human_fill(pool, quotas, lambda u: (u["wave"], u["model"]), rng, HUMAN_MAX_PER_BRAND)
        else:
            got, short = _human_fill(pool, {(m,): mq[m] for m in models}, lambda u: (u["model"],), rng,
                                     HUMAN_MAX_PER_BRAND)
        picked += got
        report["per_category"][f"{blk} {cat}"] = len(got)
        if short:
            report["shortfalls"][f"{blk} {cat}"] = short
    rec = [u for u in units if u["block"] == "R"]
    for b in sorted({u["brand"] for u in rec}):
        cand = sorted([u for u in rec if u["brand"] == b], key=lambda u: u["unit_id"])
        rng.shuffle(cand)
        if not cand:
            continue
        first = cand[0]
        second = next((u for u in cand[1:] if u["model"] != first["model"] and u["wave"] != first["wave"]), None)
        got = [first] + ([second] if second else [])
        picked += got
        if len(got) < HUMAN_RECOG_PER_BRAND:
            report["shortfalls"][f"R {b}"] = HUMAN_RECOG_PER_BRAND - len(got)
    report["recognition"] = sum(1 for u in picked if u["block"] == "R")
    report["total"] = len(picked)
    return sorted(picked, key=lambda u: u["unit_id"]), report


# ======================================================================================
# 4. JUDGE REQUESTS AND OUTPUTS (judge_prompt_v1_11.md)
# ======================================================================================
def build_request(unit: dict) -> dict:
    """Judge input. The answering model, wave and answer set are never shown to the judge."""
    user = USER_TEMPLATE.format(brand=unit["brand_display"], category=unit["category_label"],
                                question=unit["question"], text_type=TEXT_TYPES[unit["unit_type"]],
                                text=unit["text"])
    return {"unit_id": unit["unit_id"], "system": SYSTEM_PROMPT, "user": user,
            "policy": dict(JUDGE_CALL_POLICY)}


def judge_call(request: dict, model_id: str) -> str:  # pragma: no cover
    raise NotImplementedError("Judge calls are paid model calls: scripts/judge_v1_11.py, after the "
                              "v1.11 lock is anchored, under the hard cap.")


class JudgeOutputError(ValueError):
    pass


def parse_judge_output(raw: str) -> dict:
    """Strict parse + consistency checks. Invalid output -> JudgeOutputError (retried up to
    MAX_PARSE_RETRIES times with identical input, then the unit is JUDGE_FAIL)."""
    s = (raw or "").strip()
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


# ======================================================================================
# 5. STATISTICS (PRE_REGISTRATION section 5). rho_w = pooled within-category Spearman with
# within-category average ranks CENTRED on the category mean rank, r - (m_c + 1)/2 (decision 2;
# v1.10 section 7). The machinery is v1.10's (V.within_ranks, V.pooled_within_rho, V.perm_p,
# V.boot_ci); `with V.uncentred():` gives the uncentred v0.37-v0.41 convention (sensitivity SU).
# ======================================================================================
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


def rho_w(groups: Sequence[str], x: Sequence[float], y: Sequence[float]) -> float:
    """The program's within-category rho (v1.10's implementation; centred unless V.uncentred())."""
    if len(x) < 3:
        return float("nan")
    return V.pooled_within_rho(np.asarray(x, float), np.asarray(y, float), np.asarray(groups))


def pooled_test(x, y, groups, *, boot_seed=None, perm_seed=None, sided="one", single_group=False,
                min_units=MIN_UNITS_POOLED) -> dict:
    """rho_w over groups with >= MIN_UNITS_PER_GROUP units; determinable iff >= min_units units from
    >= MIN_GROUPS groups (one group allowed when single_group). 95% bootstrap (units resampled
    within group) and an optional within-group permutation p (y permuted)."""
    x, y, g = np.asarray(x, float), np.asarray(y, float), np.asarray([str(v) for v in groups])
    if len(g):
        m = V.keep_categories(g, MIN_UNITS_PER_GROUP)
        x, y, g = x[m], y[m], g[m]
    n, ng = int(len(g)), len(set(g.tolist()))
    det = n >= min_units and (ng >= MIN_GROUPS or (single_group and ng >= 1))
    rho = V.pooled_within_rho(x, y, g) if n >= 3 else float("nan")
    out = {"rho": rho, "n": n, "groups": dict(Counter(g.tolist())), "determinable": bool(det and math.isfinite(rho))}
    if boot_seed is not None and n >= 3:
        out["ci95"] = list(V.boot_ci(x, y, g, boot_seed, n_draws=N_BOOT, level=CI_LEVEL))
        out["boot_seed"] = boot_seed
    if perm_seed is not None:
        out["p_perm"] = V.perm_p(x, y, g, rho, perm_seed, sided, N_PERM) if n >= 3 else float("nan")
        out["perm_seed"], out["perm_sided"], out["perm_draws"] = perm_seed, sided, N_PERM
    return out


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
    if n == 0:
        return float("nan")
    cats = sorted(set(a) | set(b), key=str)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((list(a).count(c) / n) * (list(b).count(c) / n) for c in cats)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def band_verdict(abs_rho: float) -> str:
    if abs_rho is None or math.isnan(abs_rho):
        return "UNDETERMINED"
    if abs_rho <= BAND_CONFIRMED_MAX:
        return "CONFIRMED"
    if abs_rho >= BAND_FALSIFIED_MIN:
        return "FALSIFIED"
    return "MARGINAL"


MIN_DETERMINED_WAVES = 2        # v1.10's MIN_WAVES (tag v1.10-prereg-r2, verdict_separability)


def separability_verdict(abs_rhos_by_wave: Sequence[float]) -> str:
    """Three-wave rule (section 5), aligned with v1.10's locked rule (decision 22); NaN marks an
    undetermined wave. UNDETERMINED if fewer than 2 waves are determined; else FALSIFIED if
    |rho| >= 0.50 at ANY determined wave; CONFIRMED if |rho| <= 0.30 at every determined wave;
    MARGINAL otherwise. Same order of tests as v1.10's verdict_separability."""
    det = [r for r in abs_rhos_by_wave if not (r is None or math.isnan(r))]
    if len(det) < MIN_DETERMINED_WAVES:
        return "UNDETERMINED"
    if any(r >= BAND_FALSIFIED_MIN for r in det):
        return "FALSIFIED"
    if all(r <= BAND_CONFIRMED_MAX for r in det):
        return "CONFIRMED"
    return "MARGINAL"


def wave_abs_rho(res: dict) -> float:
    return abs(res["rho"]) if res.get("determinable") else float("nan")


def stability_verdict(rho: float, p: float, determinable: bool = True) -> str:
    if not determinable or rho is None or math.isnan(rho) or p is None or math.isnan(p):
        return "UNDETERMINED"
    if rho >= STAB_CONFIRMED_MIN and p < ALPHA_P:
        return "CONFIRMED"
    if rho < STAB_FALSIFIED_BELOW or p >= ALPHA_P:
        return "FALSIFIED"
    return "MARGINAL"


def judge_agreement_verdict(alpha: float, brand_rho: float, determinable: bool = True) -> str:
    if not determinable or math.isnan(alpha) or math.isnan(brand_rho):
        return "UNDETERMINED"
    if alpha >= ALPHA_CONFIRMED_MIN and brand_rho >= BRAND_AGREE_CONFIRMED_MIN:
        return "CONFIRMED"
    if alpha < ALPHA_FALSIFIED_BELOW or brand_rho < BRAND_AGREE_FALSIFIED_BELOW:
        return "FALSIFIED"
    return "MARGINAL"


def self_pref_verdict(delta: float, n_own: int, n_other: int) -> str:
    if n_own < MIN_UNITS_SINGLE or n_other < MIN_UNITS_SINGLE or delta is None or math.isnan(delta):
        return "UNDETERMINED"
    if abs(delta) <= SELF_PREF_OK_MAX:
        return "CONFIRMED"
    if abs(delta) >= SELF_PREF_MATERIAL_MIN:
        return "FALSIFIED"
    return "MARGINAL"


NOISE_GUARDED = ("H2", "H3", "H5", "H7", "H8")


def apply_noise_guard(verdicts: Dict[str, str]) -> Tuple[Dict[str, str], bool]:
    """A noisy instrument is separable from everything: if H1 or H4 is FALSIFIED, H2, H3, H5, H7
    and H8 are reported as UNDETERMINED (statistics shown as descriptive only)."""
    on = verdicts.get("H1") == "FALSIFIED" or verdicts.get("H4") == "FALSIFIED"
    out = dict(verdicts)
    if on:
        for h in NOISE_GUARDED:
            if h in out and out[h] not in ("INACTIVE", "PENDING"):
                out[h] = "UNDETERMINED"
    return out, on


def provider_of(model: str) -> str:
    m = (model or "").lower()
    for pre, prov in (("claude", "anthropic"), ("gpt", "openai"), ("o1", "openai"), ("gemini", "google"),
                      ("grok", "xai")):
        if m.startswith(pre):
            return prov
    return "other"


# ======================================================================================
# 6. COST (PRE_REGISTRATION section 7). Prices: the vendors' pricing pages (PRICE_SOURCES).
# ======================================================================================
def est_tokens(chars: int) -> int:
    """Planning estimate: 1 token per 4 characters (rounded up), the program's convention."""
    return -(-int(chars) // 4)


def price(model_id: str, when: Optional[datetime] = None, batch: bool = False) -> Tuple[float, float]:
    """List price (US$ per 1M input / output tokens) at `when`; batch=True: the batch price."""
    when = when or datetime.now(timezone.utc)
    ch = (PRICE_CHANGES_BATCH if batch else PRICE_CHANGES).get(model_id)
    if ch and when >= datetime.fromisoformat(ch[0]):
        return ch[1]
    return (PRICES_BATCH if batch else PRICES)[model_id]


def judge_mode(model_id: str) -> str:
    """'batch' or 'sync' for a judge model (JUDGES); models outside JUDGES are priced as sync."""
    return next((j["mode"] for j in JUDGES.values() if j["model_id"] == model_id), "sync")


def plan_tokens_per_char(provider: str) -> float:
    """Planning input tokens per request character: measured o200k ratio x the vendor factor."""
    return TOKEN_FACTOR[provider] / O200K_CHARS_PER_TOKEN


def call_usd(model_id: str, tok_in: float, tok_out: float, when: Optional[datetime] = None,
             batch: bool = False) -> float:
    """Spend of one call at list price (no cache discount is assumed: an upper bound when the
    vendor applies one)."""
    pin, pout = price(model_id, when, batch)
    return (tok_in * pin + tok_out * pout) / 1e6


def project_plan(calls: Sequence[Tuple[str, int]], out_per_call: float, in_per_char: float = 0.25,
                 when: Optional[datetime] = None, overhead: float = COST_OVERHEAD) -> dict:
    """calls: (model_id, request characters). Projected USD and tokens with overhead."""
    usd = tin = tout = 0.0
    by_model: Dict[str, dict] = defaultdict(lambda: {"calls": 0, "tokens_in": 0.0, "tokens_out": 0.0, "usd": 0.0})
    for model_id, chars in calls:
        ti = math.ceil(chars * in_per_char)
        c = call_usd(model_id, ti, out_per_call, when, batch=judge_mode(model_id) == "batch")
        b = by_model[model_id]
        b["calls"] += 1
        b["tokens_in"] += ti
        b["tokens_out"] += out_per_call
        b["usd"] += c
        usd, tin, tout = usd + c, tin + ti, tout + out_per_call
    return {"calls": len(calls), "tokens_in": tin, "tokens_out": tout, "usd": usd,
            "usd_with_overhead": usd * overhead, "calls_with_overhead": math.ceil(len(calls) * overhead),
            "by_model": {k: dict(v) for k, v in by_model.items()}}


@dataclass
class CostGuard:
    """Worst-case guard (used by judge_v1_11.py): a call, or a batch of calls, is not sent if the
    recorded spend + the worst cases in flight + its worst case would pass the US$100 cap; once
    the recorded spend reaches the pause threshold (US$80) nothing is sent until Pablo's approval
    is recorded."""
    cap_usd: float = HARD_CAP_USD
    cap_calls: int = HARD_CAP_CALLS
    pause_share: float = PAUSE_SHARE
    spent_usd: float = 0.0
    reserved_usd: float = 0.0
    calls: int = 0
    approved_past_pause: Optional[str] = None

    @property
    def pause_usd(self) -> float:
        return self.cap_usd * self.pause_share

    def check(self, worst_usd: float) -> Optional[str]:
        if self.calls + 1 > self.cap_calls:
            return f"CALL CAP: {self.calls} calls sent; the cap is {self.cap_calls}"
        if self.spent_usd >= self.pause_usd and not self.approved_past_pause:
            return (f"PAUSED: recorded spend ${self.spent_usd:.2f} reached ${self.pause_usd:.2f} (the pause "
                    f"threshold); ask Pablo, then resume with --approve-past-pause")
        if self.spent_usd + self.reserved_usd + worst_usd > self.cap_usd:
            return (f"CAP: ${self.spent_usd:.2f} spent + ${self.reserved_usd:.2f} in flight + ${worst_usd:.4f} "
                    f"worst case would pass ${self.cap_usd:.0f}")
        return None

    def reserve(self, worst_usd: float) -> None:
        why = self.check(worst_usd)
        if why:
            raise RuntimeError(why)
        self.reserved_usd += worst_usd
        self.calls += 1

    def fit(self, worsts: Sequence[float]) -> Tuple[int, Optional[str]]:
        """Batches: how many of the leading requests fit (k), and why not one more (or None).
        The pause and the call cap apply as for a single call."""
        if not worsts:
            return 0, None
        why = self.check(worsts[0])
        if why:
            return 0, why
        k, tot = 0, 0.0
        for w in worsts:
            if self.calls + k + 1 > self.cap_calls or self.spent_usd + self.reserved_usd + tot + w > self.cap_usd:
                break
            k, tot = k + 1, tot + w
        return k, None

    def reserve_many(self, worsts: Sequence[float]) -> None:
        self.reserved_usd += sum(worsts)
        self.calls += len(worsts)

    def settle(self, reserved: float, actual: float) -> None:
        self.reserved_usd -= reserved
        self.spent_usd += actual


# ======================================================================================
# 7. FROZEN INPUTS (PRE_REGISTRATION section 2). Loaders are v1.10's (V.load_registry,
# V.load_answers, V._prompt_texts); the only new format is v0.23 Phase A (block R).
# ======================================================================================
R_FILES = {"t1": "osf/v23/data/v23_phase_a_raw.json", "t2": "osf/v34/data/v23/v23_phase_a_raw.json",
           "t3": "osf/v41/data/v23/v23_phase_a_raw.json"}
V23_REGISTRY = "osf/methodology/v1_10/registries/v0_23_registry_v1_10.json"   # v1.10's, verbatim
V19_QUERIES = "osf/v19/phase_b_queries.jsonl"       # v0.19 Phase B prompt texts (no text in the answers)
E_PROMPTS = {"pm": "prompts/prompts_pm.json", "finance": "prompts/prompts_finance.json",
             "oliveoil": "prompts/prompts_oliveoil.json", "running": "prompts/prompts_running.json",
             "skincare": "prompts/prompts_skincare.json", "household": "prompts/prompts_household.json",
             "knives": "prompts/prompts_knives.json", "premium_tea": "prompts/prompts_premium_tea.json"}
E_CATEGORIES = list(E_PROMPTS)   # the eight early sets (v1.10's EARLY-6 minus v0.16 kitchen knives)


def build_sets() -> List[dict]:
    """Every v1.11 answer set. R = v0.23 Phase A open recognition (3 waves); F = v1.10's OMNI
    specs (5 substrates x 3 waves; same set names, files and registries); E = v1.10's EARLY-6
    specs for the eight early categories (v1.0 household = the scored _final file; registries per
    REGISTRY_CHOICES_v1_10.md). The program's held studies and v0.28 are not loaded."""
    out = []
    for w in WAVES:
        out.append({"set": f"R {w} v0.23", "block": "R", "role": "recognition", "panel": "LEGACY-6",
                    "wave": w, "category": "v0.23", "answers": R_FILES[w], "fmt": "v23_phase_a_json",
                    "registry": V23_REGISTRY, "reg_fmt": "v23_json"})
    for s in V.build_sets():
        if s["role"] == "omni":
            q = {"questions": V19_QUERIES} if s["fmt"] == "v19_jsonl" else {}
            out.append({**s, "block": "F", **q})
        elif s["role"] == "early6" and s["category"] in E_PROMPTS:
            out.append({**s, "block": "E", "prompts": E_PROMPTS[s["category"]]})
    return out


def make_ctx(dry: bool = False, root=None, manifest=None, outdir=None) -> "V.Ctx":
    """v1.10's context class: every input path must be pinned in this run's manifest."""
    return V.Ctx(dry=dry, root=root or (DRY_ROOT if dry else ROOT),
                 manifest=manifest or (DRY_MANIFEST if dry else MANIFEST),
                 outdir=outdir or (DRY_OUTDIR if dry else OUTDIR))


def out_dir(ctx, kind: str) -> Path:
    """Where a mode writes: pre-lock records -> prereg/ (dry: dryrun/outputs/)."""
    if ctx.dry or str(ctx.outdir) != str(OUTDIR):
        return Path(ctx.outdir)
    return {"prereg": PREREG_DIR, "outputs": OUTDIR, "data": DATA_DIR}[kind]


def load_recognition(ctx, spec: dict) -> List[dict]:
    p = ctx.path(spec["answers"])
    out = []
    for i, r in enumerate(json.loads(p.read_text(encoding="utf-8"))):
        st = r.get("status", "ok")
        a = V._answer(spec, r["model_id"], "A", None, r.get("response"), None if st == "ok" else st,
                      row=i)
        a["answer_id"] = f"{spec['set']}::{r['model_id']}|{r['brand_id']}"
        a.update(brand=r["brand_id"], brand_name=r.get("brand_name"), question=r.get("prompt"))
        out.append(a)
    dup = [k for k, c in Counter(a["answer_id"] for a in out).items() if c > 1]
    if dup:
        raise Halt(f"duplicate recognition cells in {spec['set']}: {dup[:5]}")
    return out


def attach_questions(ctx, spec: dict, answers: List[dict]) -> None:
    """{question} = the exact prompt that produced the answer (section 4.2)."""
    fmt = spec["fmt"]
    if fmt == "frame_csv":
        rows = V._read_csv(ctx.path(spec["answers"]))
        for a in answers:
            a["question"] = rows[a["row"]].get("frame_text")
    elif fmt == "v19_jsonl":
        q: Dict[str, set] = defaultdict(set)
        for line in ctx.path(spec["questions"]).read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                q[r["frame"]].add(r["prompt"])
        if any(len(v) != 1 for v in q.values()):
            raise Halt("v0.19 queries: more than one prompt text per frame")
        for a in answers:
            a["question"] = next(iter(q.get(a["frame"], {None})))
    elif fmt == "v23_json":
        recs = json.loads(ctx.path(spec["answers"]).read_text(encoding="utf-8"))
        for a in answers:
            a["question"] = recs[a["row"]].get("prompt")
    elif fmt == "runner_csv":
        texts = V._prompt_texts(ctx.path(spec["prompts"]))
        for a in answers:
            a["question"] = texts.get(a["frame"])
    missing = [a["answer_id"] for a in answers if a["text"] is not None and not a.get("question")]
    if missing:
        raise Halt(f"no question text for {len(missing)} answers in {spec['set']} (e.g. {missing[0]})")


def load_set(ctx, spec: dict):
    reg, unit, notes = V.load_registry(ctx, spec["registry"], spec["reg_fmt"])
    if spec["block"] == "R":
        answers = load_recognition(ctx, spec)
    else:
        answers = V.load_answers(ctx, spec)
        attach_questions(ctx, spec, answers)
    return reg, unit, notes, answers


def e2_named(answers: List[dict], reg: dict, unit: dict) -> Dict[str, set]:
    """v1.10's E2 extractor (registry regex on v1.4-normalised text): the brands an answer names."""
    pats = V.compile_registry(reg)
    return {a["answer_id"]: {unit[b] for b in V.find_mentions(V.normalize(a["text"]), pats)}
            for a in answers if a["text"] is not None}


def certified_named(ctx, spec: dict, answers: List[dict], reg: dict, unit: dict) -> Tuple[Dict[str, set], int]:
    """F block: the program's certified mention record, the sources behind score_v41.load_wave and
    v1.9's mentions: v0.20-v0.22 the phase's certified detect_mention; v0.19 the coded
    phase_b_results.csv; v0.23 the coded v23_phase_b_scored.json. -> ({answer_id: unit keys},
    coded cells without an answer with text)."""
    ans = {a["answer_id"]: a for a in answers if a["text"] is not None}
    out: Dict[str, set] = {aid: set() for aid in ans}
    unmatched = 0
    known = set(unit.values())
    if spec.get("detector"):
        mod = V._import_file(ctx.path(spec["detector"]), "certified_" + V._slug(spec["detector"]))
        for aid, a in ans.items():
            out[aid] = {unit[b] for b in reg if mod.detect_mention(a["text"], b)}
    elif spec.get("coded"):
        by_cell = {(a["model"], a["frame"]): aid for aid, a in ans.items()}
        if spec["fmt"] == "v19_jsonl":
            coded = [((r["panel_model"], r["frame"]), r["brand"]) for r in V._read_csv(ctx.path(spec["coded"]))
                     if str(r["mentioned"]).strip() == "1"]
        else:
            coded = []
            for r in json.loads(ctx.path(spec["coded"]).read_text(encoding="utf-8")):
                if r.get("status", "ok") != "ok":
                    continue
                coded += [((r["model_id"], r["probe_id"]), b) for b, v in (r.get("brand_mentions") or {}).items() if v]
        for cell, b in coded:
            aid = by_cell.get(cell)
            if aid is None:
                unmatched += 1
                continue
            if b not in known:
                raise Halt(f"certified record names a brand outside the registry: {spec['set']} {b}")
            out[aid].add(b)
    else:
        raise Halt(f"no certified mention record for {spec['set']}")
    return out, unmatched


def named_sets(ctx, spec, answers, reg, unit) -> Tuple[Dict[str, set], int]:
    if spec["block"] == "E":
        return e2_named(answers, reg, unit), 0
    return certified_named(ctx, spec, answers, reg, unit)


UNIT_COLS = ["unit_id", "block", "set", "panel", "wave", "category", "category_label", "brand",
             "brand_display", "model", "provider", "frame", "channel", "run_idx", "answer_id",
             "unit_type", "question", "text", "chars", "request_chars", "cut", "bare", "judged",
             "j2", "selfcon", "human"]


def _unit(spec, a, brand, display, unit_type, text, cut, bare) -> dict:
    u = {"unit_id": f"{a['answer_id']}#{brand}", "block": spec["block"], "set": spec["set"],
         "panel": spec["panel"], "wave": spec["wave"], "category": spec["category"],
         "category_label": CATEGORY_LABELS[spec["category"]], "brand": brand, "brand_display": display,
         "model": a["model"], "provider": provider_of(a["model"]), "frame": a["frame"],
         "channel": a.get("channel") or "", "run_idx": "" if a["run_idx"] is None else a["run_idx"],
         "answer_id": a["answer_id"], "unit_type": unit_type, "question": a["question"], "text": text,
         "chars": len(text), "cut": bool(cut), "bare": bool(bare), "judged": True, "j2": False,
         "selfcon": False, "human": False}
    r = build_request(u)
    u["request_chars"] = len(r["system"]) + len(r["user"])
    return u


def build_units(ctx, log=print) -> dict:
    """U0: the unit table (all blocks), extraction misses, the E window cap, the samples."""
    bad = V.verify_manifest(ctx.manifest_path, ctx.root)
    if bad:
        raise Halt("manifest verification failed: " + "; ".join(bad[:10]))
    units: List[dict] = []
    misses: List[dict] = []
    per_set: Dict[str, dict] = {}
    n_named: Dict[str, Dict[str, int]] = {}
    for spec in build_sets():
        reg, unit, _notes, answers = load_set(ctx, spec)
        texts = [a for a in answers if a["text"] is not None]
        canon_of = {u: c for c, u in unit.items()}
        rec = {"block": spec["block"], "answers": len(answers), "with_text": len(texts)}
        if spec["block"] == "R":
            for a in texts:
                if a["brand"] not in canon_of:
                    raise Halt(f"recognition brand outside the v0.23 registry: {a['brand']}")
                t, cut = recognition_text(a["text"])
                units.append(_unit(spec, a, a["brand"], a.get("brand_name") or canon_of[a["brand"]],
                                   "recognition", t, cut, False))
            rec.update(units=len(texts), cut_at_cap=sum(1 for u in units if u["set"] == spec["set"] and u["cut"]))
        else:
            named, unmatched = named_sets(ctx, spec, answers, reg, unit)
            aliases = {u: [canon_of[u], *reg[canon_of[u]]] for u in canon_of}
            pats = {u: alias_pattern(al) for u, al in aliases.items()}
            others = {u: other_pattern(pats[u], [x for o, al in aliases.items() if o != u for x in al])
                      for u in aliases}
            mentions = windows = 0
            for a in texts:
                A = AnswerText(a["text"])
                for b in sorted(named[a["answer_id"]]):
                    mentions += 1
                    w = build_window(a["text"], aliases[b], pat=pats[b], other=others[b], prepared=A,
                                     other_given=True)
                    if w is None:
                        misses.append({"set": spec["set"], "answer_id": a["answer_id"], "brand": b})
                        continue
                    windows += 1
                    units.append(_unit(spec, a, b, canon_of[b], "mention", w,
                                       len(w) >= WINDOW_CHAR_CAP, is_bare(w, pats[b])))
            cnt = Counter(b for s in named.values() for b in s)
            n_named[spec["set"]] = {b: cnt.get(b, 0) for b in sorted(aliases)}
            rec.update(mentions=mentions, windows=windows, misses=mentions - windows,
                       miss_share=(mentions - windows) / mentions if mentions else 0.0,
                       coded_cells_without_answer_text=unmatched)
        per_set[spec["set"]] = rec
    over = {s: r["miss_share"] for s, r in per_set.items() if r.get("miss_share", 0) > EXTRACTION_MISS_HALT_SHARE}
    if over:
        raise Halt(f"extraction misses above 5% of a set's mentions: {over}")
    # E window cap (F is a no-op by design: asserted)
    capped = {u["unit_id"] for u in cap_windows([u for u in units if u["block"] in ("E", "F")])}
    for u in units:
        if u["block"] in ("E", "F") and u["unit_id"] not in capped:
            if u["block"] == "F":
                raise Halt("the 36-window cap removed an F unit (impossible by design)")
            u["judged"] = False
    judged = [u for u in units if u["judged"]]
    j2 = set(j2_sample(judged))
    sc = set(selfcon_sample(judged))
    hs, hrep = human_sample(judged)
    hid = {u["unit_id"] for u in hs}
    for u in units:
        u["j2"] = u["unit_id"] in j2 or (u["judged"] and u["block"] in ("R", "F"))
        u["selfcon"] = u["unit_id"] in sc
        u["human"] = u["unit_id"] in hid
    for s, r in per_set.items():
        us = [u for u in units if u["set"] == s]
        r.update(units_judged=sum(u["judged"] for u in us), capped_out=sum(not u["judged"] for u in us),
                 bare=sum(u["bare"] for u in us if u["judged"]), at_window_cap=sum(u["cut"] for u in us if u["judged"]))
    log(f"[v1.11] U0: {len(units)} units, {len(judged)} judged, {len(misses)} extraction misses, "
        f"J2 sample {len(j2)}, self-consistency {len(sc)}, human sample {len(hs)}")
    return {"units": sorted(units, key=lambda u: u["unit_id"]), "misses": misses, "per_set": per_set,
            "n_named": n_named, "human": hs, "human_report": hrep}


DEFAULT_PLAN = {"e_cap": K_CAP_PER_BRAND, "j2_e_share": J2_EARLY_SHARE, "e_half": False, "e_none": False}
REDUCTION_ORDER = [("e_cap", 24), ("j2_e_share", 0.05), ("e_half", True), ("e_none", True)]


def effective_units(units: List[dict], params: Optional[dict] = None) -> List[dict]:
    """The judged set under the budget reductions of section 7, applied in the fixed order
    (1) E window cap 36 -> 24, (2) J2's E sample 10% -> 5%, (3) E judged on a seeded 50% of each
    set's answers (seed 111004), (4) E not judged. R and F are never reduced, and the Paper B
    human-label units are always judged by J1. Decided before any E call. With no reduction the
    U0 flags are returned unchanged (tested). Used by judge_v1_11.py and by Stage J."""
    p = {**DEFAULT_PLAN, **(params or {})}
    if p == DEFAULT_PLAN:
        return [dict(u) for u in units]
    out = [dict(u) for u in units]
    E = [u for u in out if u["block"] == "E"]
    keep = {u["unit_id"] for u in cap_windows(E, k=int(p["e_cap"]))}
    if p["e_half"]:
        rng = random.Random(SEEDS["e_half"])
        half = set()
        for s in sorted({u["set"] for u in E}):
            aids = sorted({u["answer_id"] for u in E if u["set"] == s})
            rng.shuffle(aids)
            half |= set(aids[:_k_of(0.5, len(aids))])
        keep = {u["unit_id"] for u in E if u["unit_id"] in keep and u["answer_id"] in half}
    if p["e_none"]:
        keep = set()
    keep |= {u["unit_id"] for u in E if u["human"]}
    for u in E:
        u["judged"] = u["unit_id"] in keep
    judgedE = [u for u in E if u["judged"]]
    j2 = set(stratified_sample(judgedE, float(p["j2_e_share"]), lambda u: (u["category"], u["model"]),
                               SEEDS["j2_sample"]))
    for u in E:
        u["j2"] = u["unit_id"] in j2
        u["selfcon"] = u["selfcon"] and u["judged"]
    return out


def units_csv_bytes(units: List[dict]) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(UNIT_COLS)
    for u in units:
        w.writerow([int(u[c]) if isinstance(u[c], bool) else u[c] for c in UNIT_COLS])
    return buf.getvalue().encode("utf-8")


HUMAN_COLS = ["unit_id", "block", "category_label", "wave", "model", "frame", "brand_display", "question",
              "unit_type", "text_type", "text", "bare"]


def human_csv_bytes(units: List[dict]) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(HUMAN_COLS)
    for u in units:
        row = {**u, "text_type": TEXT_TYPES[u["unit_type"]]}
        w.writerow([int(row[c]) if isinstance(row[c], bool) else row[c] for c in HUMAN_COLS])
    return buf.getvalue().encode("utf-8")


def read_units(path: Path) -> List[dict]:
    csv.field_size_limit(sys.maxsize)
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for c in ("cut", "bare", "judged", "j2", "selfcon", "human"):
            r[c] = r[c] == "1"
        r["chars"], r["request_chars"] = int(r["chars"]), int(r["request_chars"])
    return rows


def token_summary(units: List[dict]) -> dict:
    out = {}
    for blk in ("R", "F", "E"):
        us = [u for u in units if u["block"] == blk and u["judged"]]
        rc = [u["request_chars"] for u in us]
        out[blk] = {"units": len(us), "request_chars_total": sum(rc),
                    "est_tokens_in_total": sum(est_tokens(c) for c in rc),
                    "est_tokens_in_mean": (sum(est_tokens(c) for c in rc) / len(rc)) if rc else None,
                    "window_chars_median": float(np.median([u["chars"] for u in us])) if us else None}
    return out


def run_build_units(ctx, log=print) -> dict:
    res = build_units(ctx, log)
    od = out_dir(ctx, "prereg")
    od.mkdir(parents=True, exist_ok=True)
    ub = units_csv_bytes(res["units"])
    hb = human_csv_bytes(res["human"])
    (od / "units_v1_11.csv").write_bytes(ub)
    (od / "human_sample_v1_11.csv").write_bytes(hb)
    judged = [u for u in res["units"] if u["judged"]]
    doc = {"phase": PHASE_ID, "kind": "U0 unit build (pre-lock): no model call, no valence, no P, C* or R",
           "created_utc": _now(), "dry_run": ctx.dry, "manifest_sha256": V.sha256(ctx.manifest_path),
           "scorer_sha256": V.sha256(Path(__file__)),
           "units_file": {"path": "units_v1_11.csv", "sha256": V.sha256_bytes(ub), "rows": len(res["units"])},
           "human_sample_file": {"path": "human_sample_v1_11.csv", "sha256": V.sha256_bytes(hb),
                                 "rows": len(res["human"]), **res["human_report"]},
           "units": {"total": len(res["units"]), "judged": len(judged),
                     "by_block": dict(Counter(u["block"] for u in judged)),
                     "capped_out_E": sum(1 for u in res["units"] if not u["judged"])},
           "samples": {"J2_E": sum(1 for u in judged if u["block"] == "E" and u["j2"]),
                       "J2_total": sum(1 for u in judged if u["j2"]),
                       "selfcon_by_block": dict(Counter(u["block"] for u in judged if u["selfcon"])),
                       "selfcon_J2": sum(1 for u in judged if u["selfcon"] and u["j2"])},
           "tokens": token_summary(res["units"]), "per_set": res["per_set"], "extraction_misses": res["misses"],
           "n_named": res["n_named"], "seeds": SEEDS}
    (od / "u0_v1_11.json").write_text(json.dumps(V._clean(doc), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"[v1.11] U0 written to {od} (units sha256 {doc['units_file']['sha256'][:16]}...)")
    return doc


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def run_parity(ctx, log=print) -> dict:
    """Pre-lock parity: parse completion (v1.10 normaliser, registry matcher and item parser; the
    v1.11 segmenter), mention parity and the unit join on key columns. Builds no window, reads no
    valence, no P, no C* and no rank position."""
    bad = V.verify_manifest(ctx.manifest_path, ctx.root)
    if bad:
        raise Halt("manifest verification failed: " + "; ".join(bad[:10]))
    res = {"phase": PHASE_ID, "kind": "pre-lock parity: parse completion, mention parity, unit join (key columns)",
           "declaration": ("Computed before the lock on the frozen inputs. Uses the normaliser, the registry "
                           "matchers, the list-item parser and the segmenter only; no window, no valence, no "
                           "judge output, and no P, C* or rank value was computed, read or printed."),
           "created_utc": _now(), "dry_run": ctx.dry, "manifest_sha256": V.sha256(ctx.manifest_path),
           "parse_completion": {}, "mention_parity_F": {}, "concordance_E_brands_canonical": {},
           "questions": {}, "join": {}}
    f_units = defaultdict(set)
    r_brands = defaultdict(set)
    for spec in build_sets():
        reg, unit, _notes, answers = load_set(ctx, spec)
        texts = [a for a in answers if a["text"] is not None]
        exc = []
        pats = V.compile_registry(reg)
        for a in texts:
            try:
                norm = V.normalize(a["text"])
                if spec["block"] != "R":
                    V.find_mentions(norm, pats)
                V.item_spans(norm)
                segment_spans(a["text"])
                fold_map(a["text"])
            except Exception as e:  # noqa: BLE001
                exc.append({"answer_id": a["answer_id"], "error": f"{type(e).__name__}: {e}"})
        res["parse_completion"][spec["set"]] = {"rows": len(answers), "with_text": len(texts),
                                                "missing_cells": len(answers) - len(texts),
                                                "parsed_without_exception": len(texts) - len(exc),
                                                "completion": (len(texts) - len(exc)) / len(texts) if texts else None,
                                                "exceptions": exc}
        res["questions"][spec["set"]] = {"answers_with_question": sum(1 for a in texts if a.get("question")),
                                         "distinct_questions": len({a.get("question") for a in texts})}
        if spec["block"] == "R":
            r_brands[spec["wave"]] |= {a["brand"] for a in texts}
            continue
        e2 = e2_named(answers, reg, unit)
        if spec["block"] == "F":
            cert, unmatched = certified_named(ctx, spec, answers, reg, unit)
            cells = agree = 0
            dis = []
            for aid in cert:
                for b in sorted(set(unit.values())):
                    c, x = b in cert[aid], b in e2[aid]
                    cells += 1
                    agree += c == x
                    if c != x:
                        dis.append({"answer_id": aid, "brand": b, "certified": c, "v1_10_E2": x})
            res["mention_parity_F"][spec["set"]] = {
                "certified_record": spec.get("detector") or spec.get("coded"), "cells": cells, "agree": agree,
                "agreement": agree / cells if cells else None, "certified_mentions": sum(len(v) for v in cert.values()),
                "e2_mentions": sum(len(v) for v in e2.values()), "coded_cells_without_answer_text": unmatched,
                "disagreements": dis}
            f_units[spec["wave"]] |= {(spec["category"], u) for u in unit.values()}
        else:
            rows = V._read_csv(ctx.path(spec["answers"]))
            if rows and "brands_canonical" in rows[0]:
                canon = {c: unit[c] for c in reg}
                cells = agree = only_e2 = only_arch = 0
                for a in texts:
                    raw = rows[a["row"]].get("brands_canonical") or ""
                    names = {re.sub(r"@\d+$", "", x).strip() for x in raw.split("|") if x.strip()}
                    archived = {canon[n] for n in names if n in canon}
                    for b in sorted(set(unit.values())):
                        c, x = b in archived, b in e2[a["answer_id"]]
                        cells += 1
                        agree += c == x
                        only_e2 += x and not c
                        only_arch += c and not x
                res["concordance_E_brands_canonical"][spec["set"]] = {
                    "cells": cells, "agree": agree, "agreement": agree / cells if cells else None,
                    "named_by_E2_only": only_e2, "named_by_brands_canonical_only": only_arch,
                    "note": "descriptive; brands_canonical (LLM function calling) never builds a unit"}
            else:
                res["concordance_E_brands_canonical"][spec["set"]] = {"available": False}
    keys = V.profile_keys(ctx.path(PROFILES_REL))
    res["join"]["F_vs_aias_2_0_profiles"] = V.join_check(keys, f_units)
    keys19 = V.profile_keys(ctx.path(V19_TABLE_REL))
    res["join"]["F_vs_v1_9_unit_table"] = V.join_check(keys19, f_units)
    prof_v23 = {(w, b) for (w, s, b) in keys if s == "v0.23"}
    res["join"]["R_vs_aias_2_0_profiles"] = {
        w: {"recognition_brands": len(r_brands[w]),
            "in_profiles": sum(1 for b in r_brands[w] if (w, b) in prof_v23)} for w in WAVES}
    pc = res["parse_completion"]
    par = res["mention_parity_F"]
    res["summary"] = {
        "parse_100pct_all_sets": all(v["completion"] in (None, 1.0) for v in pc.values()),
        "answers_with_text": {b: sum(v["with_text"] for s, v in pc.items() if s.startswith(p))
                              for b, p in (("R", "R "), ("F", "OMNI"), ("E", "EARLY"))},
        "F_mention_parity_min": min((v["agreement"] for v in par.values()), default=None),
        "F_join_1to1_all_waves": res["join"]["F_vs_aias_2_0_profiles"]["passes"],
        "F_join_v1_9_table_1to1": res["join"]["F_vs_v1_9_unit_table"]["passes"],
        "R_brands_in_profiles": all(v["recognition_brands"] == v["in_profiles"] == 24
                                    for v in res["join"]["R_vs_aias_2_0_profiles"].values())}
    od = out_dir(ctx, "prereg")
    od.mkdir(parents=True, exist_ok=True)
    (od / "parity_v1_11.json").write_text(json.dumps(V._clean(res), indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")
    for s, v in par.items():
        log(f"  F parity {s:16s} {v['agree']:5d}/{v['cells']:<5d} = {v['agreement']:.4f}")
    for s, v in res["concordance_E_brands_canonical"].items():
        if v.get("cells"):
            log(f"  E concordance {s:28s} {v['agree']:5d}/{v['cells']:<5d} = {v['agreement']:.4f}")
    log(f"  summary {json.dumps(V._clean(res['summary']))}")
    return res


# ======================================================================================
# 8. JUDGE OUTPUTS AND STAGE J (PRE_REGISTRATION section 8: outputs frozen -> H1 first)
# ======================================================================================
RAW_NAME = "judge_raw_v1_11.jsonl"
FROZEN_NAME = "judge_outputs_frozen_v1_11.json"
U0_NAME = "u0_v1_11.json"
UNITS_NAME = "units_v1_11.csv"
STAGE_J_NAME = "stage_j_v1_11.json"
OUTCOMES_NAME = "unit_outcomes_v1_11.csv"
VERDICTS_NAME = "v1_11_verdicts.json"
VALID, FAIL, UNJUDGED = "VALID", "JUDGE_FAIL", "UNJUDGED"


def skey(u: dict) -> Tuple[str, str, str, str]:
    """Score unit: (block, wave, category, brand). F/R waves t1-t3; E wave = the phase (one wave)."""
    return (u["block"], u["wave"], u["category"], u["brand"])


def load_u0(ctx) -> Tuple[dict, List[dict]]:
    od = out_dir(ctx, "prereg")
    doc = json.loads((od / U0_NAME).read_text(encoding="utf-8"))
    up = od / UNITS_NAME
    if V.sha256(up) != doc["units_file"]["sha256"]:
        raise Halt("unit table differs from the U0 record")
    return doc, read_units(up)


def load_frozen_outputs(ctx) -> Tuple[List[dict], dict]:
    frozen_p = out_dir(ctx, "outputs") / FROZEN_NAME
    if not frozen_p.exists():
        raise Halt("ORDER: judge outputs are not frozen (judge_v1_11.py --freeze)")
    frozen = json.loads(frozen_p.read_text(encoding="utf-8"))
    raw = out_dir(ctx, "data") / RAW_NAME
    if V.sha256(raw) != frozen["raw_sha256"]:
        raise Halt("judge raw file differs from its frozen hash")
    recs = [json.loads(x) for x in raw.read_text(encoding="utf-8").splitlines() if x.strip()]
    return recs, frozen


def outcomes(records: List[dict], roles: Dict[str, str]) -> Dict[Tuple[str, str, str], dict]:
    """Final outcome per (role, unit_id, pass) for the model assigned to the role: the first
    response that was served by the requested model and parses -> VALID; >= 3 invalid responses
    (1 + 2 retries with identical input) -> JUDGE_FAIL; otherwise UNJUDGED (never sent, API error,
    or the run stopped)."""
    g: Dict[tuple, List[dict]] = defaultdict(list)
    for r in records:
        if roles.get(r["role"]) == r["judge_model"]:
            g[(r["role"], r["unit_id"], r["pass"])].append(r)
    out = {}
    for k, rs in g.items():
        rs = sorted(rs, key=lambda r: (int(r["attempt"]), r.get("started_utc") or ""))
        valid, invalid = None, 0
        for r in rs:
            if r.get("status") not in ("ok", "empty"):
                continue
            ok = bool(r.get("served_ok"))
            parsed = None
            if ok and r.get("status") == "ok":
                try:
                    parsed = parse_judge_output(r.get("text") or "")
                except JudgeOutputError:
                    parsed = None
            if parsed is not None:
                valid = (r, parsed)
                break
            invalid += 1
        if valid:
            out[k] = {"status": VALID, "out": valid[1], "attempts": len(rs), "served_model": valid[0].get("served_model")}
        elif invalid >= 1 + MAX_PARSE_RETRIES:
            out[k] = {"status": FAIL, "out": None, "attempts": len(rs)}
        else:
            out[k] = {"status": UNJUDGED, "out": None, "attempts": len(rs)}
    return out


def _oc(oc, role, uid, pas="main"):
    return oc.get((role, uid, pas), {"status": UNJUDGED, "out": None, "attempts": 0})


def score_map(units: List[dict], oc: dict, role: str, keep=None, floor: int = N_FLOOR) -> Dict[tuple, dict]:
    """S per score unit from one judge's main-pass outcomes. UNJUDGED units are not counted;
    JUDGE_FAIL and refers_to_brand false are excluded and counted (section 4.3)."""
    groups: Dict[tuple, List[Optional[dict]]] = defaultdict(list)
    unj: Counter = Counter()
    for u in units:
        if not u["judged"] or (keep is not None and not keep(u)):
            continue
        o = _oc(oc, role, u["unit_id"])
        if role == "J2" and not u["j2"]:
            continue
        if o["status"] == UNJUDGED:
            unj[skey(u)] += 1
            continue
        groups[skey(u)].append(o["out"])
    out = {}
    for k, js in groups.items():
        bs = brand_score(js, floor)
        out[k] = {"n": bs.n, "S": bs.S, "E": bs.E, "NV": bs.NV, "rated": bs.S is not None,
                  "n_excluded": bs.n_excluded, "n_refers_false": sum(1 for j in js if j is not None and not j["refers_to_brand"]),
                  "n_judge_fail": sum(1 for j in js if j is None), "n_unjudged": unj.get(k, 0)}
    return out


def h1_block(units, oc, keep=None) -> dict:
    """H1: Krippendorff alpha (ordinal) on valence over every unit with VALID J1 and J2 main-pass
    outputs; brand rho_w(S_J1, S_J2) over F score units rated under both, waves pooled, groups =
    substrate x wave."""
    pairs, ev_a, ev_b, conf = [], [], [], Counter()
    per_block: Dict[str, list] = defaultdict(list)
    pairs_refers = []
    for u in units:
        if not u["judged"] or not u["j2"] or (keep is not None and not keep(u)):
            continue
        a, b = _oc(oc, "J1", u["unit_id"]), _oc(oc, "J2", u["unit_id"])
        if a["status"] != VALID or b["status"] != VALID:
            continue
        va, vb = a["out"]["valence"], b["out"]["valence"]
        pairs.append((va, vb))
        per_block[u["block"]].append((va, vb))
        ev_a.append(a["out"]["evaluative"])
        ev_b.append(b["out"]["evaluative"])
        conf[(va, vb)] += 1
        if a["out"]["refers_to_brand"] and b["out"]["refers_to_brand"]:
            pairs_refers.append((va, vb))
    alpha = krippendorff_alpha_ordinal(pairs) if len(pairs) >= 2 else float("nan")
    s1 = score_map(units, oc, "J1", keep)
    s2 = score_map(units, oc, "J2", keep)
    ks = sorted(k for k in s1 if k[0] == "F" and s1[k]["rated"] and k in s2 and s2[k]["rated"])
    br = pooled_test([s1[k]["S"] for k in ks], [s2[k]["S"] for k in ks], [f"{k[2]}|{k[1]}" for k in ks],
                     boot_seed=SEEDS["boot"])
    det = br["determinable"] and len(pairs) >= MIN_UNITS_POOLED
    return {"verdict": judge_agreement_verdict(alpha, br["rho"], det), "alpha_ordinal": alpha,
            "units_judged_by_both": len(pairs), "brand_rho": br,
            "alpha_by_block": {k: krippendorff_alpha_ordinal(v) if len(v) >= 2 else None for k, v in per_block.items()},
            "alpha_refers_true_both": krippendorff_alpha_ordinal(pairs_refers) if len(pairs_refers) >= 2 else None,
            "kappa_evaluative": cohen_kappa(ev_a, ev_b) if ev_a else None,
            "confusion_J1_rows_J2_cols": {f"{a}|{b}": c for (a, b), c in sorted(conf.items())},
            "thresholds": {"CONFIRMED": "alpha >= 0.667 AND brand rho >= 0.80",
                           "FALSIFIED": "alpha < 0.50 OR brand rho < 0.60"}}


def selfcon_block(units, oc) -> dict:
    """Self-consistency (decision 1): the fixed 5% repeat sample, judged a second time by the same
    judge with identical input. Reported; below 0.90 exact agreement is flagged (no halt)."""
    out = {}
    for role in ("J1", "J2"):
        rows = defaultdict(list)
        for u in units:
            if not (u["judged"] and u["selfcon"]) or (role == "J2" and not u["j2"]):
                continue
            a, b = _oc(oc, role, u["unit_id"], "main"), _oc(oc, role, u["unit_id"], "repeat")
            if a["status"] == VALID and b["status"] == VALID:
                rows[u["block"]].append((a["out"], b["out"]))
                rows["all"].append((a["out"], b["out"]))
        res = {}
        for blk, ps in rows.items():
            exact = sum(x["valence"] == y["valence"] for x, y in ps) / len(ps)
            res[blk] = {"n": len(ps), "exact_valence_agreement": exact,
                        "alpha_ordinal": krippendorff_alpha_ordinal([(x["valence"], y["valence"]) for x, y in ps])
                        if len(ps) >= 2 else None,
                        "kappa_evaluative": cohen_kappa([x["evaluative"] for x, _ in ps], [y["evaluative"] for _, y in ps]),
                        "flag_below_0.90": exact < SELFCON_MIN_EXACT}
        out[role] = res
    return out


def fail_check(units, oc, roles) -> dict:
    """JUDGE_FAIL share per judge x set (units sent: VALID + JUDGE_FAIL); > 2% halts before scoring."""
    out, halt = {}, []
    for role in roles:
        per = defaultdict(Counter)
        for u in units:
            if not u["judged"] or (role == "J2" and not u["j2"]):
                continue
            per[u["set"]][_oc(oc, role, u["unit_id"])["status"]] += 1
        for s, c in per.items():
            sent = c[VALID] + c[FAIL]
            share = c[FAIL] / sent if sent else 0.0
            out[f"{role} {s}"] = {"valid": c[VALID], "judge_fail": c[FAIL], "unjudged": c[UNJUDGED], "fail_share": share}
            if share > JUDGE_FAIL_HALT_SHARE:
                halt.append(f"{role} {s}")
    return {"per_judge_set": out, "halt": halt}


OUTCOME_COLS = ["unit_id", "block", "set", "wave", "category", "brand", "model", "provider", "frame",
                "J1_status", "J1_valence", "J1_evaluative", "J1_mixed", "J1_refers",
                "J2_status", "J2_valence", "J2_evaluative", "J2_mixed", "J2_refers",
                "J1_rep_status", "J1_rep_valence", "J2_rep_status", "J2_rep_valence"]


def outcomes_csv_bytes(units, oc) -> bytes:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(OUTCOME_COLS)
    for u in units:
        if not u["judged"]:
            continue
        row = [u[c] for c in OUTCOME_COLS[:9]]
        for role, pas in (("J1", "main"), ("J2", "main")):
            o = _oc(oc, role, u["unit_id"], pas)
            j = o["out"] or {}
            row += [o["status"], j.get("valence", ""), int(j["evaluative"]) if j else "",
                    int(j["mixed"]) if j else "", int(j["refers_to_brand"]) if j else ""]
        for role in ("J1", "J2"):
            o = _oc(oc, role, u["unit_id"], "repeat")
            row += [o["status"] if u["selfcon"] else "", (o["out"] or {}).get("valence", "")]
        w.writerow(row)
    return buf.getvalue().encode("utf-8")


def run_stage_j(ctx, log=print) -> dict:
    u0, units = load_u0(ctx)
    recs, frozen = load_frozen_outputs(ctx)
    if frozen.get("units_sha256") != u0["units_file"]["sha256"]:
        raise Halt("frozen judge outputs were produced on another unit table")
    units = effective_units(units, frozen.get("plan_params"))
    roles = frozen["roles"]
    oc = outcomes(recs, roles)
    fc = fail_check(units, oc, ("J1", "J2"))
    if fc["halt"]:
        raise Halt(f"JUDGE_FAIL above 2% of a set's units: {fc['halt']} (halt before scoring)")
    s1, s2 = score_map(units, oc, "J1"), score_map(units, oc, "J2")
    h1 = h1_block(units, oc)
    sc = selfcon_block(units, oc)
    od = out_dir(ctx, "outputs")
    od.mkdir(parents=True, exist_ok=True)
    ob = outcomes_csv_bytes(units, oc)
    (od / OUTCOMES_NAME).write_bytes(ob)
    scores = {"J1": {"|".join(k): v for k, v in s1.items()}, "J2": {"|".join(k): v for k, v in s2.items()}}
    doc = {"phase": PHASE_ID, "stage": "J", "created_utc": _now(), "dry_run": ctx.dry, "roles": roles,
           "replacements": frozen.get("replacements", {}), "frozen_sha256": V.sha256(out_dir(ctx, "outputs") / FROZEN_NAME),
           "units_sha256": u0["units_file"]["sha256"], "outcomes_sha256": V.sha256_bytes(ob),
           "judge_fail": fc, "H1_Judge_Agreement": h1, "self_consistency": sc, "scores": scores,
           "outcome_counts": {r: dict(Counter(v["status"] for k, v in oc.items() if k[0] == r and k[2] == "main"))
                              for r in ("J1", "J2")}}
    (od / STAGE_J_NAME).write_text(json.dumps(V._clean(doc), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"[v1.11] Stage J: H1 {h1['verdict']} (alpha {h1['alpha_ordinal']:.3f}, brand rho "
        f"{h1['brand_rho']['rho']:.3f}, n {h1['brand_rho']['n']}); self-consistency "
        + "; ".join(f"{r} {v.get('all', {}).get('exact_valence_agreement', float('nan')):.3f}" for r, v in sc.items()))
    return doc


# ======================================================================================
# 9. STAGE C (after Stage J): P, C* and R* are opened here and nowhere else
# ======================================================================================
def manifest_git_objects(ctx) -> Dict[str, dict]:
    man = json.loads(Path(ctx.manifest_path).read_text(encoding="utf-8"))
    return {e["path"]: e for e in man.get("git_objects", [])}


def git_blob_bytes(blob: str, root: Path = ROOT) -> bytes:
    r = subprocess.run(["git", "-C", str(root), "cat-file", "blob", blob], capture_output=True)
    if r.returncode != 0:
        raise Halt(f"git object {blob} not found")
    return r.stdout


def load_v110_object(ctx, rel: str) -> dict:
    """v1.10 Stage S objects (decision 6). Real runs: from the git object store by the blob id
    pinned in the manifest (SHA-256 checked); dry runs: the replica file pinned in the dry-run
    manifest."""
    if ctx.dry:
        return json.loads(ctx.path(rel).read_text(encoding="utf-8"))
    e = manifest_git_objects(ctx).get(rel)
    if e is None:
        raise Halt(f"v1.10 object not pinned in the manifest: {rel}")
    data = git_blob_bytes(e["git_blob"])
    if V.sha256_bytes(data) != e["sha256"]:
        raise Halt(f"v1.10 object differs from its pinned SHA-256: {rel}")
    return json.loads(data.decode("utf-8"))


def h5_status(ctx) -> Tuple[str, str]:
    """H5 is ACTIVE because tag v1.10-prereg-r2 existed before the v1.11 lock (section 5). R* is
    computed only after v1.10's own Stage C verdict file exists on branch v1.10 (v1.11 never
    computes a Ranking statistic first; it does not read that file)."""
    if ctx.dry:
        return "ACTIVE", "dry run"
    if not V._tag_exists(V110_TAG, ROOT):
        return "INACTIVE", f"tag {V110_TAG} not found"
    r = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{V110_BRANCH}:{V110_VERDICTS_REL}"],
                       capture_output=True)
    if r.returncode != 0:
        return "PENDING", "v1.10 Stage C verdicts not yet on branch v1.10; H5 is computed when they are"
    return "ACTIVE", "v1.10 Stage C verdicts exist (not read)"


def ranking_scores(ctx, log=print) -> Tuple[Dict[tuple, dict], dict]:
    """R* = the statistic of selection_v1_10.json (MNP), v1.10's lead-item extractor (E0-E7),
    rated at >= 6 rankable mentions, computed with v1.10's own functions on the same answer files.
    Every regenerated per-answer rank table must equal v1.10's Stage S rank table (SHA-256)."""
    sel = load_v110_object(ctx, V110_SELECTION_REL)
    idx = load_v110_object(ctx, V110_RANK_INDEX_REL)
    stat = sel.get("stat_for_stage_c")
    if sel.get("selected") != V110_SELECTED_EXPECTED or stat != V110_SELECTED_EXPECTED:
        raise Halt(f"v1.10 selection is {sel.get('selected')}, not {V110_SELECTED_EXPECTED}")
    R, checks = {}, {"statistic": stat, "rank_tables": {}}
    for spec in build_sets():
        if spec["block"] not in ("F", "E"):
            continue
        reg, unit, _n = V.load_registry(ctx, spec["registry"], spec["reg_fmt"])
        pats = V.compile_registry(reg)
        answers = V.load_answers(ctx, spec)
        infos = [V.extract_answer(a, pats, unit) for a in answers]
        sha = V.sha256_bytes(V.rank_table_bytes({"infos": infos}))
        ok = idx.get(spec["set"], {}).get("sha256") == sha
        checks["rank_tables"][spec["set"]] = {"sha256": sha, "matches_v1_10_stage_s": ok}
        if not ok:
            raise Halt(f"rank table of {spec['set']} differs from v1.10's Stage S table")
        rows = V.rank_rows({spec["set"]: {"spec": spec, "infos": infos}}, "lead_item")
        for (panel, wave, cat, b), v in V.score_units(rows).items():
            R[(spec["block"], wave, cat, b)] = {"R": v[stat], "rated": bool(v["rated"]), "n_ranked": v["n_ranked"]}
    log(f"[v1.11] R* ({stat}) computed with v1.10's locked code; {len(checks['rank_tables'])} rank tables match")
    return R, checks


def _Y(S: Dict[tuple, dict], block: str, field: str = "S") -> Dict[str, Dict[tuple, float]]:
    out: Dict[str, Dict[tuple, float]] = defaultdict(dict)
    for k, v in S.items():
        if k[0] == block and v.get("rated") and v.get(field) is not None:
            out[k[1]][(k[2], k[3])] = v[field]
    return out


def sep_by_wave(S, Y, block="F", keep_key=None, single_group=False, field="S") -> dict:
    per = {}
    for w in WAVES:
        ks = sorted(k for k, v in S.items() if k[0] == block and k[1] == w and v.get("rated")
                    and v.get(field) is not None and (k[2], k[3]) in Y.get(w, {})
                    and math.isfinite(Y[w][(k[2], k[3])]) and (keep_key is None or keep_key(k)))
        per[w] = pooled_test([Y[w][(k[2], k[3])] for k in ks], [S[k][field] for k in ks], [k[2] for k in ks],
                             boot_seed=SEEDS["boot"], single_group=single_group,
                             min_units=MIN_UNITS_SINGLE if single_group else MIN_UNITS_POOLED)
    return {"per_wave": per, "verdict": separability_verdict([wave_abs_rho(per[w]) for w in WAVES])}


def stab(S, wa, wb, seed, keep_key=None) -> dict:
    ks = sorted((k[2], k[3]) for k, v in S.items() if k[0] == "F" and k[1] == wa and v["rated"]
                and S.get(("F", wb, k[2], k[3]), {}).get("rated") and (keep_key is None or keep_key(k)))
    x = [S[("F", wa, c, b)]["S"] for c, b in ks]
    y = [S[("F", wb, c, b)]["S"] for c, b in ks]
    r = pooled_test(x, y, [c for c, _ in ks], boot_seed=SEEDS["boot"], perm_seed=seed, sided="one")
    r["verdict"] = stability_verdict(r["rho"], r.get("p_perm", float("nan")), r["determinable"])
    r["waves"] = f"{wa}->{wb}"
    return r


def h7(S, n_named, keep_key=None) -> dict:
    ks = sorted(k for k, v in S.items() if k[0] == "E" and v["rated"] and (keep_key is None or keep_key(k)))
    x = [n_named[f"EARLY-6 {k[1]} {k[2]}"][k[3]] for k in ks]
    r = pooled_test(x, [S[k]["S"] for k in ks], [k[2] for k in ks], boot_seed=SEEDS["boot"])
    r["verdict"] = band_verdict(abs(r["rho"])) if r["determinable"] else "UNDETERMINED"
    return r


def h9(units, oc, j1_provider, keep=None) -> dict:
    own, other = [], []
    for u in units:
        if not u["judged"] or u["block"] not in ("R", "F") or (keep is not None and not keep(u)):
            continue
        a, b = _oc(oc, "J1", u["unit_id"]), _oc(oc, "J2", u["unit_id"])
        if a["status"] != VALID or b["status"] != VALID:
            continue
        if not (a["out"]["refers_to_brand"] and b["out"]["refers_to_brand"]):
            continue
        d = unit_score(a["out"]["valence"]) - unit_score(b["out"]["valence"])
        (own if u["provider"] == j1_provider else other).append(d)
    delta = (float(np.mean(own)) - float(np.mean(other))) if own and other else float("nan")
    return {"delta_points": delta, "n_own_provider": len(own), "n_other": len(other),
            "mean_diff_own": float(np.mean(own)) if own else None, "mean_diff_other": float(np.mean(other)) if other else None,
            "j1_provider": j1_provider, "verdict": self_pref_verdict(delta, len(own), len(other))}


def model_balanced(units, oc, role="J1", keep=None) -> Dict[tuple, dict]:
    acc: Dict[tuple, Dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for u in units:
        if not u["judged"] or (keep is not None and not keep(u)):
            continue
        o = _oc(oc, role, u["unit_id"])
        if o["status"] == VALID and o["out"]["refers_to_brand"]:
            acc[skey(u)][u["model"]].append(unit_score(o["out"]["valence"]))
    out = {}
    for k, per in acc.items():
        n = sum(len(v) for v in per.values())
        out[k] = {"S": float(np.mean([np.mean(v) for v in per.values()])), "rated": n >= N_FLOOR, "n": n}
    return out


def gate_set(units, oc, S, P, C, R, n_named, h5_active, keep=None, keep_key=None) -> dict:
    """H1-H8 statistics under one convention / unit filter (used for the primary analysis and
    for the sensitivities)."""
    res = {"H1_Judge_Agreement": h1_block(units, oc, keep),
           "H2_Sep_Presence": sep_by_wave(S, P, keep_key=keep_key),
           "H3_Sep_Consistency": sep_by_wave(S, C, keep_key=keep_key),
           "H4_Stability_Short": stab(S, "t1", "t2", SEEDS["H4"], keep_key),
           "H6_Stability_Long": stab(S, "t2", "t3", SEEDS["H6"], keep_key),
           "H7_Naming_Frequency": h7(S, n_named, keep_key),
           "H8_Recognition_Sep": sep_by_wave(S, P, block="R", keep_key=keep_key, single_group=True)}
    if h5_active and R is not None:
        RY = _Y(R, "F", "R")
        res["H5_Sep_Ranking"] = sep_by_wave(S, RY, keep_key=keep_key)
        RE = {k: v for k, v in R.items() if k[0] == "E" and v["rated"]}
        ks = sorted(k for k, v in S.items() if k[0] == "E" and v["rated"] and k in RE and (keep_key is None or keep_key(k)))
        r = pooled_test([RE[k]["R"] for k in ks], [S[k]["S"] for k in ks], [k[2] for k in ks], boot_seed=SEEDS["boot"])
        r["verdict"] = band_verdict(abs(r["rho"])) if r["determinable"] else "UNDETERMINED"
        res["H5_secondary_early"] = r
    return res


def verdict_row(res: dict, h9res: dict, h5_state: str) -> Dict[str, str]:
    v = {"H1": res["H1_Judge_Agreement"]["verdict"], "H2": res["H2_Sep_Presence"]["verdict"],
         "H3": res["H3_Sep_Consistency"]["verdict"], "H4": res["H4_Stability_Short"]["verdict"],
         "H5": res["H5_Sep_Ranking"]["verdict"] if "H5_Sep_Ranking" in res else h5_state,
         "H6": res["H6_Stability_Long"]["verdict"], "H7": res["H7_Naming_Frequency"]["verdict"],
         "H8": res["H8_Recognition_Sep"]["verdict"], "H9": h9res["verdict"]}
    return v


def _dist(vals) -> Optional[dict]:
    v = np.asarray([x for x in vals if x is not None and math.isfinite(x)], float)
    if not len(v):
        return None
    return {"n": int(len(v)), "median": float(np.median(v)), "q25": float(np.quantile(v, .25)),
            "q75": float(np.quantile(v, .75)), "min": float(v.min()), "max": float(v.max())}


def legacy_labels(ctx) -> Dict[Tuple[str, str], str]:
    """Exploratory descriptive 6 only: the archived per-brand labels (extract_v09.py, gpt-5.4-mini
    function calling, positive / neutral / negative) of the five v0.9 sets, keyed (answer, brand)."""
    out = {}
    for spec in build_sets():
        if spec["block"] != "E" or spec["wave"] != "v0.9":
            continue
        reg, unit, _n = V.load_registry(ctx, spec["registry"], spec["reg_fmt"])
        answers = V.load_answers(ctx, spec)
        rows = V._read_csv(ctx.path(spec["answers"]))
        for a in answers:
            for pair in (rows[a["row"]].get("sentiment_summary") or "").split("|"):
                if ":" in pair:
                    name, lab = pair.rsplit(":", 1)
                    if name.strip() in unit:
                        out[(a["answer_id"], unit[name.strip()])] = lab.strip()
    return out


def descriptives(ctx, units, oc, S1, S2, u0) -> dict:
    d: dict = {"baseline": [], "convergence_rec_vs_frames": {}, "mean_u": {}, "legacy_label_agreement": None}
    groups = sorted({(u["block"], u["wave"], u["category"]) for u in units if u["judged"]})
    for blk, w, c in groups:
        us = [u for u in units if u["judged"] and (u["block"], u["wave"], u["category"]) == (blk, w, c)]
        o = [_oc(oc, "J1", u["unit_id"]) for u in us]
        val = [x["out"] for x in o if x["status"] == VALID]
        ref = [j for j in val if j["refers_to_brand"]]
        ks = [k for k in S1 if k[:3] == (blk, w, c)]
        d["baseline"].append({
            "block": blk, "wave": w, "category": c, "label": CATEGORY_LABELS[c], "units": len(us),
            "brands": len(ks), "brands_rated": sum(S1[k]["rated"] for k in ks),
            "S": _dist([S1[k]["S"] for k in ks if S1[k]["rated"]]),
            "E_mean": float(np.mean([S1[k]["E"] for k in ks if S1[k]["rated"]])) if any(S1[k]["rated"] for k in ks) else None,
            "NV": _dist([S1[k]["NV"] for k in ks if S1[k]["rated"] and S1[k]["NV"] is not None]),
            "share_non_evaluative": (sum(not j["evaluative"] for j in ref) / len(ref)) if ref else None,
            "share_mixed": (sum(j["mixed"] for j in ref) / len(ref)) if ref else None,
            "share_refers_false": (sum(not j["refers_to_brand"] for j in val) / len(val)) if val else None,
            "judge_fail": sum(x["status"] == FAIL for x in o), "unjudged": sum(x["status"] == UNJUDGED for x in o),
            "bare_share": sum(u["bare"] for u in us) / len(us) if us else None})
    for w in WAVES:
        ks = sorted(b for (blk, ww, c, b), v in S1.items() if blk == "R" and ww == w and v["rated"]
                    and S1.get(("F", w, "v0.23", b), {}).get("rated"))
        d["convergence_rec_vs_frames"][w] = {
            "n": len(ks), "spearman": spearman([S1[("R", w, "v0.23", b)]["S"] for b in ks],
                                               [S1[("F", w, "v0.23", b)]["S"] for b in ks]) if len(ks) >= 3 else None}
    acc: Dict[str, Dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for u in units:
        o = _oc(oc, "J1", u["unit_id"])
        if u["judged"] and o["status"] == VALID and o["out"]["refers_to_brand"]:
            x = unit_score(o["out"]["valence"])
            acc[f"{u['block']} by model"][u["model"]].append(x)
            acc[f"{u['block']} by frame"][str(u["frame"])].append(x)
            acc["by panel"][u["panel"]].append(x)
    d["mean_u"] = {g: {k: {"n": len(v), "mean_u": float(np.mean(v))} for k, v in sorted(m.items())} for g, m in acc.items()}
    try:
        lab = legacy_labels(ctx)
        tab, agree, n = Counter(), 0, 0
        for u in units:
            o = _oc(oc, "J1", u["unit_id"])
            L = lab.get((u["answer_id"], u["brand"]))
            if L and u["judged"] and o["status"] == VALID and o["out"]["refers_to_brand"]:
                s = "positive" if o["out"]["valence"] > 0 else "negative" if o["out"]["valence"] < 0 else "neutral"
                tab[f"{s}|{L}"] += 1
                agree += s == L
                n += 1
        d["legacy_label_agreement"] = {"exploratory": True, "n": n, "agreement": agree / n if n else None,
                                       "table_J1_sign_vs_legacy": dict(tab)}
    except Halt as e:
        d["legacy_label_agreement"] = {"exploratory": True, "not_computed": str(e)}
    d["extraction_misses_by_set"] = {s: r.get("misses") for s, r in u0["per_set"].items() if "misses" in r}
    return d


def run_stage_c(ctx, log=print) -> dict:
    sj_p = out_dir(ctx, "outputs") / STAGE_J_NAME
    if not sj_p.exists():
        raise Halt("ORDER: Stage J (H1) must be written before P, C* or R* are opened")
    sj = json.loads(sj_p.read_text(encoding="utf-8"))
    if V.sha256(out_dir(ctx, "outputs") / OUTCOMES_NAME) != sj["outcomes_sha256"]:
        raise Halt("unit outcomes changed since Stage J")
    bad = V.verify_manifest(ctx.manifest_path, ctx.root)
    if bad:
        raise Halt("manifest verification failed: " + "; ".join(bad[:10]))
    u0, units = load_u0(ctx)
    recs, frozen = load_frozen_outputs(ctx)
    units = effective_units(units, frozen.get("plan_params"))
    oc = outcomes(recs, frozen["roles"])
    S1, S2 = score_map(units, oc, "J1"), score_map(units, oc, "J2")
    # --- first read of P and C* (section 8) ---
    prof = V._read_csv(ctx.path(PROFILES_REL))
    f_units = defaultdict(set)
    for spec in build_sets():
        if spec["block"] == "F":
            _r, unit, _n = V.load_registry(ctx, spec["registry"], spec["reg_fmt"])
            f_units[spec["wave"]] |= {(spec["category"], u) for u in unit.values()}
    join = V.join_check([(r["wave"], r["substrate"], r["brand"]) for r in prof], f_units)
    if not join["passes"]:
        raise Halt("join: F units do not match aias_2_0_profiles.csv 1:1")
    P, C, NM = V.parse_profiles(prof)
    t19 = V._read_csv(ctx.path(V19_TABLE_REL))

    def _differs(r) -> bool:
        k = (r["substrate"], r["brand"])
        p = P.get(r["wave"], {}).get(k)
        if p is None or not math.isfinite(p) or abs(float(r["P"]) - p) > 1e-9:
            return True
        c19 = (r.get("C_star") or "").strip()
        c = C.get(r["wave"], {}).get(k)
        if (c19 == "") != (c is None):
            return True
        return c is not None and abs(float(c19) - c) > 1e-9

    diff = [r["wave"] + "|" + r["substrate"] + "|" + r["brand"] for r in t19 if _differs(r)]
    win = Counter((u["wave"], u["category"], u["brand"]) for u in units if u["block"] == "F")
    miss = Counter((s.split()[1], s.split()[2], m["brand"]) for m in u0["extraction_misses"] for s in [m["set"]]
                   if s.startswith("OMNI"))
    count_check = [f"{w}|{c}|{b}" for w in WAVES for (c, b), n in NM[w].items()
                   if math.isfinite(n) and win.get((w, c, b), 0) + miss.get((w, c, b), 0) != int(n)]
    state, why = h5_status(ctx)
    R, rchk = (None, {"status": state, "reason": why})
    if state == "ACTIVE":
        R, rchk = ranking_scores(ctx, log)
        rchk["status"] = state
    j1_prov = provider_of(frozen["roles"]["J1"])
    prim = gate_set(units, oc, S1, P, C, R, u0["n_named"], state == "ACTIVE")
    prim["H1_Judge_Agreement"] = sj["H1_Judge_Agreement"]          # H1 as written at Stage J
    h9res = h9(units, oc, j1_prov)
    raw_v = verdict_row(prim, h9res, state)
    final_v, guard_on = apply_noise_guard(raw_v)
    sens: dict = {}
    changes = []

    def note(name, v):
        for h, val in v.items():
            if val != raw_v.get(h):
                changes.append({"sensitivity": name, "hypothesis": h, "primary": raw_v.get(h), "under_sensitivity": val})

    with V.uncentred():
        su = gate_set(units, oc, S1, P, C, R, u0["n_named"], state == "ACTIVE")
    sens["SU_uncentred_ranks"] = su
    note("SU_uncentred_ranks", verdict_row(su, h9res, state))
    not_denon = lambda u: not (u["block"] == "F" and (u["category"], u["brand"]) == DENON)  # noqa: E731
    key_nd = lambda k: not (k[0] == "F" and (k[2], k[3]) == DENON)                           # noqa: E731
    sd = gate_set(units, oc, S1, P, C, R, u0["n_named"], state == "ACTIVE", keep=not_denon, keep_key=key_nd)
    sd_h9 = h9(units, oc, j1_prov, keep=not_denon)
    sens["SD_without_Denon_v0_19"] = {**sd, "H9_Self_Preference": sd_h9}
    note("SD_without_Denon_v0_19", verdict_row(sd, sd_h9, state))
    nv = {k: {**v, "rated": v["rated"] and v["NV"] is not None} for k, v in S1.items()}
    sens["S_NV_in_place_of_S"] = {"H2": sep_by_wave(nv, P, field="NV"), "H3": sep_by_wave(nv, C, field="NV")}
    mb = model_balanced(units, oc)
    sens["S_model_balanced"] = {"H2": sep_by_wave(mb, P), "H3": sep_by_wave(mb, C)}
    sens["S_J2_scored"] = {"H2": sep_by_wave(S2, P), "H3": sep_by_wave(S2, C)}
    if h9res["verdict"] == "FALSIFIED":
        keep_np = lambda u: u["provider"] != j1_prov  # noqa: E731
        Snp = score_map(units, oc, "J1", keep=keep_np)
        sens["S_without_J1_provider_answers"] = {"H2": sep_by_wave(Snp, P), "H3": sep_by_wave(Snp, C)}
    sens["verdict_changes"] = changes
    desc = descriptives(ctx, units, oc, S1, S2, u0)
    doc = {"phase": PHASE_ID, "stage": "C", "created_utc": _now(), "dry_run": ctx.dry, "prereg_tag": PREREG_TAG,
           "roles": frozen["roles"], "stage_j_sha256": V.sha256(sj_p), "units_sha256": u0["units_file"]["sha256"],
           "manifest_sha256": V.sha256(ctx.manifest_path), "rank_convention": "within-category average ranks centred on the category mean rank",
           "join": join, "P_Cstar_v1_9_cross_check": {"differences": diff, "rows_compared": len(t19)},
           "F_window_count_vs_n_mentions": {"mismatches": count_check},
           "ranking": rchk, "verdicts_before_noise_guard": raw_v, "VERDICTS": final_v, "noise_guard_applied": guard_on,
           "H1_marginal_flag_on_all_verdicts": final_v["H1"] == "MARGINAL",
           **{k: v for k, v in prim.items()}, "H9_Self_Preference": h9res, "sensitivities": sens,
           "descriptives": desc, "self_consistency": sj["self_consistency"], "seeds": SEEDS,
           "draws": {"perm": N_PERM, "boot": N_BOOT, "ci": CI_LEVEL}}
    od = out_dir(ctx, "outputs")
    (od / VERDICTS_NAME).write_text(json.dumps(V._clean(doc), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"[v1.11] Stage C verdicts: {final_v} (noise guard {'ON' if guard_on else 'off'}); "
        f"{len(changes)} sensitivity verdict changes; written to {od / VERDICTS_NAME}")
    return doc


# ======================================================================================
# 10. LOCK STATUS AND CLI
# ======================================================================================
# The files hashed in prereg/LOCK_MANIFEST_v1_11.sha256 and in the anchor's locked_files, in order.
LOCK_FILES = [
    f"{V111}/prereg/PRE_REGISTRATION_v1_11.md", f"{V111}/prereg/judge_prompt_v1_11.md",
    f"{V111}/prereg/feasibility_v1_11.md", f"{V111}/prereg/parity_v1_11.json", f"{V111}/prereg/u0_v1_11.json",
    f"{V111}/prereg/units_v1_11.csv", f"{V111}/prereg/human_sample_v1_11.csv",
    f"{V111}/prereg/dry_run_judge_v1_11.txt", f"{V111}/prereg/cost_projection_v1_11.json",
    f"{V111}/prereg/token_counts_v1_11.json", f"{V111}/prereg/precision_v1_11.json",
    f"{V111}/registries/INPUTS_MANIFEST_v1_11.json", f"{V111}/registries/build_inputs_manifest_v1_11.py",
    f"{V111}/scoping/feasibility_v1_11.py", f"{V111}/scoping/feasibility_v1_11.json",
    f"{V111}/scoping/token_count_v1_11.py", f"{V111}/scoping/precision_v1_11.py",
    f"{V111}/dryrun/build_dryrun_v1_11.py", f"{V111}/anchor/DEVIATIONS.md",
    "scripts/score_v1_11.py", "scripts/judge_v1_11.py", "scripts/test_score_v1_11.py", "scripts/test_judge_v1_11.py",
    "scripts/score_v1_10.py", "osf/methodology/v1_10/registries/v0_23_registry_v1_10.json",
]
LOCK_MANIFEST_FILE = PREREG_DIR / "LOCK_MANIFEST_v1_11.sha256"
# v1.10 objects committed in this tree byte-identical to tag v1.10-prereg-r2 (decision 23): path -> git blob
V110_COPIES = {"scripts/score_v1_10.py": V110_SCORER_BLOB,
               "osf/methodology/v1_10/registries/v0_23_registry_v1_10.json": "5d6df9c6b7afe07d1b23b4c28bd35449a3e77080"}
# The anchor record (decision 24): one schema, written by --write-anchor and checked by
# judge_v1_11.py --run and by --stage J / C (anchor_problems). osf_deposit must be non-empty.
ANCHOR_FIELDS = ("tag", "tag_object", "commit", "tree", "branch", "tagger_date", "remote_tag_ref",
                 "recorded_utc", "repository", "osf_deposit", "locked_files")


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise Halt(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def lock_manifest_text(root: Path = ROOT) -> str:
    """sha256sum format, LOCK_FILES order, from the working tree."""
    return "".join(f"{V.sha256(root / p)}  {p}\n" for p in LOCK_FILES)


def anchor_template(osf_deposit: str = "") -> dict:
    """The anchor record's schema with empty values (what --write-anchor fills)."""
    return {k: ({} if k == "locked_files" else "") for k in ANCHOR_FIELDS} | {"osf_deposit": osf_deposit}


def anchor_problems(anchor: dict, commit: Optional[str] = None) -> List[str]:
    """Why an anchor record does not anchor the lock (empty list = it does)."""
    why = [f"anchor field missing or empty: {k}" for k in ANCHOR_FIELDS
           if k != "osf_deposit" and not anchor.get(k)]
    if not str(anchor.get("osf_deposit") or "").strip():
        why.append("the anchor file records no OSF deposit (osf_deposit is empty)")
    if anchor.get("tag") and anchor["tag"] != PREREG_TAG:
        why.append(f"anchor tag {anchor['tag']} is not {PREREG_TAG}")
    if commit and anchor.get("commit") != commit and anchor.get("tag_object") != commit:
        why.append(f"the anchor file does not name the commit of {PREREG_TAG} ({commit})")
    lf = anchor.get("locked_files") or {}
    if lf and sorted(lf) != sorted(LOCK_FILES):
        why.append("the anchor's locked_files differ from LOCK_FILES")
    return why


def build_anchor(osf_deposit: str) -> dict:
    """The anchor record of the pushed tag: every locked file hashed from the TAG's tree (git blob
    and SHA-256), the tag's commit, tree and tagger date, the remote ref, and the OSF deposit."""
    if not str(osf_deposit or "").strip():
        raise Halt("--write-anchor needs a non-empty --osf-deposit")
    remote = _git("ls-remote", "--tags", "origin", PREREG_TAG)
    if f"refs/tags/{PREREG_TAG}" not in remote:
        raise Halt(f"tag {PREREG_TAG} is not on origin: push it before writing the anchor")
    import hashlib
    files = {}
    for p in LOCK_FILES:
        blob = _git("rev-parse", f"{PREREG_TAG}:{p}")
        data = subprocess.run(["git", "-C", str(ROOT), "cat-file", "blob", blob], capture_output=True).stdout
        files[p] = {"sha256": hashlib.sha256(data).hexdigest(), "git_blob": blob}
    doc = anchor_template(osf_deposit)
    doc.update({"tag": PREREG_TAG, "tag_object": _git("rev-parse", PREREG_TAG),
                "commit": _git("rev-parse", f"{PREREG_TAG}^{{commit}}"),
                "tree": _git("rev-parse", f"{PREREG_TAG}^{{tree}}"), "branch": "v1.11",
                "tagger_date": _git("for-each-ref", "--format=%(taggerdate:iso-strict)", f"refs/tags/{PREREG_TAG}"),
                "remote_tag_ref": remote.splitlines()[0], "recorded_utc": _now(),
                "repository": _git("remote", "get-url", "origin"), "locked_files": files})
    bad = anchor_problems(doc, doc["commit"])
    if bad:
        raise Halt("; ".join(bad))
    return doc


def lock_status() -> Tuple[bool, str]:
    """--stage J / C on real data need the pre-registration tag AND an anchor file that anchors it
    (anchor_problems: every field, the tag's commit, a non-empty osf_deposit)."""
    why = []
    if not V._tag_exists(PREREG_TAG, ROOT):
        why.append(f"git tag {PREREG_TAG} does not exist")
    if not ANCHOR_FILE.exists():
        why.append(f"anchor file {ANCHOR_FILE} does not exist")
    elif not why:
        commit = _git("rev-parse", f"{PREREG_TAG}^{{commit}}")
        why += anchor_problems(json.loads(ANCHOR_FILE.read_text(encoding="utf-8")), commit)
    return (not why), "; ".join(why)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--verify-manifest", action="store_true")
    ap.add_argument("--parity", action="store_true", help="pre-lock parity (no window, no valence)")
    ap.add_argument("--build-units", action="store_true", help="U0 unit build (no model call, no valence)")
    ap.add_argument("--stage", choices=["J", "C"])
    ap.add_argument("--dry-run", action="store_true", help="synthetic replicas only")
    ap.add_argument("--lock-manifest", action="store_true",
                    help="write prereg/LOCK_MANIFEST_v1_11.sha256 (LOCK_FILES, working tree); last step of the content lock")
    ap.add_argument("--write-anchor", action="store_true",
                    help="after the tag is pushed: write anchor/git_anchor_v1_11.json from the tag (needs --osf-deposit)")
    ap.add_argument("--osf-deposit", default=None, metavar="WHERE",
                    help="the OSF deposit the anchor records, e.g. 'https://osf.io/ec6wh/ (osfstorage: methodology/v1_11/...)'")
    a = ap.parse_args(argv)
    if a.lock_manifest:
        LOCK_MANIFEST_FILE.write_text(lock_manifest_text(), encoding="utf-8")
        print(f"[v1.11] {LOCK_MANIFEST_FILE} written ({len(LOCK_FILES)} files)")
        return 0
    if a.write_anchor:
        try:
            doc = build_anchor(a.osf_deposit)
        except V.Halt as e:
            print(f"[v1.11] REFUSED: {e}", file=sys.stderr)
            return 3
        ANCHOR_FILE.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"[v1.11] {ANCHOR_FILE} written: {doc['tag']} -> {doc['commit']}; osf_deposit {doc['osf_deposit']!r}")
        return 0
    ctx = make_ctx(a.dry_run)
    if a.dry_run and not Path(ctx.manifest_path).exists():
        print(f"[v1.11] no replica manifest at {ctx.manifest_path}; build it with "
              f"python3 {V111}/dryrun/build_dryrun_v1_11.py", file=sys.stderr)
        return 2
    try:
        if a.verify_manifest:
            bad = V.verify_manifest(ctx.manifest_path, ctx.root)
            print("manifest OK" if not bad else "\n".join(bad))
            return 0 if not bad else 1
        if a.parity:
            run_parity(ctx)
            return 0
        if a.build_units:
            run_build_units(ctx)
            return 0
        if a.stage:
            if not a.dry_run:
                ok, why = lock_status()
                if not ok:
                    print(f"[v1.11] refusing --stage {a.stage} on real data before the lock: {why}", file=sys.stderr)
                    return 3
            (run_stage_j if a.stage == "J" else run_stage_c)(ctx)
            return 0
    except V.Halt as e:              # v1.11's Halt and v1.10's (e.g. an unpinned input path)
        print(f"[v1.11] HALT: {e}", file=sys.stderr)
        return 2
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
