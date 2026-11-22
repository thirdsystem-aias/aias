#!/usr/bin/env python3
"""code_v0_46.py -- AIAS(TM) v0.46 (#76) choice coder (Stage 1 code r1; stage1_manuscript_r1.md section 5.3).

Codes each CHOICE answer (blocks C1-C3) to the category's registry, deterministically:
  VALID      exactly one registry unit on the choice line, a live unit (LIST: on the list)
  OTHER      OPEN: the choice line names something that matches no registry unit (text kept verbatim)
  OFF_LIST   LIST: the choice line names something that is not on the list (see DECISION NEEDED below)
  DEFUNCT    the one unit matched is a v0.22 Cell D car
  AMBIGUOUS  two or more registry units on the choice line
  NONE       no codable choice, a refusal, or a choice line with nothing on it
  MISSING    not an outcome: unanswered call, served by another model (MC_Served), or cut at the output limit
             before a CHOICE line (section 3.10: "treated as missing, never as NONE")
Matching uses the certified functions unchanged: v0.20-v0.22 `detect_mention` (score_v20/21/22) and the v0.23
patterns (`score_v0_23.find_brand_mentions`, the deterministic part of score_phase_b that v0.42's coder runs).

BLINDING: this coder reads answers and registries only; it never reads P or R*.
NO MODEL IS CALLED. Choices are never coded by a model (section 3.11). The predictor blocks (P1-P4) are coded by
v0.42's locked coder (osf/v42/scripts/code_t4_v0_42.py), unchanged; its v0.23 recognition judge is the only AI
coder in the study and is NOT run from here: --judge refuses (Stage 1 code; no paid or keyed call).

Usage:
  python3 osf/v46/scripts/code_v0_46.py --dry-run                 # synthetic answers incl. adversarial cases
  python3 osf/v46/scripts/code_v0_46.py --raw RAW.jsonl --probes PROBES.jsonl --out CODED.jsonl
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_probes_v0_46 as B  # noqa: E402  (registries, live units, categories)

ROOT = B.ROOT
OUTPUT_CAP = 16384
CODES = ("VALID", "OTHER", "OFF_LIST", "DEFUNCT", "AMBIGUOUS", "NONE", "MISSING")
# section 3.10 provider length stops; section 5.3 refusals. DECISION NEEDED (raw schema): the acquisition fork
# is not written yet; these field names (finish_reason, refusal, prompt_blocked, output_tokens, thinking_tokens,
# served_model, model) follow t4's raw schema where it has them and are assumptions otherwise.
LENGTH_STOPS = {"max_tokens", "length", "incomplete:max_output_tokens", "MAX_TOKENS", "FinishReason.MAX_TOKENS"}
REFUSAL_STOPS = {"refusal", "SAFETY", "PROHIBITED_CONTENT", "BLOCKLIST", "content_filter"}
# r3: acquire_v0_46 writes Google's finish reason as str(cand.finish_reason), which the google-genai enum renders
# "FinishReason.MAX_TOKENS" (or "FinishReason.SAFETY"). The enum prefix is removed before the set lookups, so both
# spellings match; "FinishReason.MAX_TOKENS" is also listed literally (same set as acquire_v0_46.LENGTH_STOPS).
FR_ENUM_PREFIX = "FinishReason."


def norm_finish_reason(fr):
    fr = "" if fr is None else str(fr).strip()
    return fr[len(FR_ENUM_PREFIX):] if fr.startswith(FR_ENUM_PREFIX) else fr


# URL removal: the same regular expressions as v0.42's coder (code_t4_v0_42.strip_urls), copied because that
# module re-executes the interpreter on import when the worktree is not ~/aias.
MD_LINK_RE = re.compile(
    r"\[([^\]]*)\]\(\s*(?:<[^>]*>|(?:[^()\s]|\([^()\s]*\))+)(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)")
URL_RE = re.compile(r"https?://[^\s<>\"'\])]+", re.I)
EMPH_RE = re.compile(r"[*_`]")          # DECISION NEEDED: "Markdown emphasis" = the characters * _ `
CHOICE_RE = re.compile(r"^\s*choice\s*:\s*(.*)$", re.I)
NAMES_SOMETHING_RE = re.compile(r"\w", re.U)
# r3 task 2 (runner handoff 2026-11-21, "LIST explicit refusal with no CHOICE line codes OFF_LIST (r2 text fix)"):
# an answered LIST call with no CHOICE line whose text explicitly declines to choose, and whose last line names no
# registry unit, is OFF_LIST (reason "refusal_text"): the model was shown the list and did not pick from it.
# Provider refusals (refusal flag, refusal/SAFETY stop, blocked prompt) stay NONE (section 5.3 / descriptive 6).
# DECISION: "explicit refusal" = this fixed pattern (first person + can't / won't / unable / decline + choose, pick,
# select, recommend or decide), set before data. Stage 1 manuscript r1 (sections 5.1, 5.3) still says a refusal is
# NONE; manuscript r2 carries the text fix.
REFUSAL_TEXT_RE = re.compile(
    r"\bi(?:['’]m|\s+am|['’]d|\s+would)?\s+"
    r"(?:can(?:no|['’])t|can\s+not|won['’]t|will\s+not|not\s+able\s+to|"
    r"unable\s+to|(?:must|have\s+to|need\s+to)\s+decline\s+to|decline\s+to|rather\s+not|prefer\s+not\s+to)\s+"
    r"(?:\w+\s+){0,2}?(?:choose|pick|select|recommend|decide|make\s+(?:a|the|that|this|your)\s+"
    r"(?:choice|decision|selection|pick))\b"
    r"|\bi\s+(?:must|have\s+to)\s+(?:respectfully\s+)?decline\b",
    re.I)


def strip_urls(text):
    if not text:
        return text or ""
    return URL_RE.sub(" ", MD_LINK_RE.sub(r"\1", text))


# --------------------------------------------------------------------------- matchers (certified, unchanged)
_MATCH = {}


def _matchers():
    if _MATCH:
        return _MATCH
    import score_v20
    import score_v21
    import score_v22
    import score_v0_23 as S23
    reg = B.registry_units()
    det = {"skincare": score_v20.detect_mention, "cosmetics": score_v21.detect_mention,
           "cars": score_v22.detect_mention}
    _MATCH["reg"] = reg
    _MATCH["det"] = det
    _MATCH["s23"] = S23
    _MATCH["s23_name"] = {b["id"]: b["brand"] for b in S23.REGISTRY}
    return _MATCH


def registry_matches(category, line):
    """Registry units (canonical names) the certified function finds on `line`, in registry order."""
    m = _matchers()
    if category == "spirits":
        found = m["s23"].find_brand_mentions(line)
        return [m["s23_name"][i] for i in sorted(found)]
    det = m["det"][category]
    return [b for b, _cell in m["reg"][category] if det(line, b)]


# --------------------------------------------------------------------------- the choice line
def choice_line(text):
    """(line, had_choice_prefix). The last line beginning with CHOICE: (case-insensitive, after emphasis is
    removed), its text after the prefix; else the answer's last non-empty line."""
    lines = [EMPH_RE.sub("", ln).strip() for ln in (text or "").splitlines()]
    for ln in reversed(lines):
        mm = CHOICE_RE.match(ln)
        if mm:
            return mm.group(1).strip(), True
    for ln in reversed(lines):
        if ln:
            return ln, False
    return "", False


def at_length_limit(rec):
    fr = rec.get("finish_reason")
    if fr:
        return fr in LENGTH_STOPS or norm_finish_reason(fr) in LENGTH_STOPS
    toks = (rec.get("output_tokens") or 0) + (rec.get("thinking_tokens") or 0)
    return toks >= OUTPUT_CAP


def is_refusal(rec):
    fr = rec.get("finish_reason")
    return (bool(rec.get("refusal")) or fr in REFUSAL_STOPS or (bool(fr) and norm_finish_reason(fr) in REFUSAL_STOPS)
            or bool(rec.get("prompt_blocked")))


def served_ok(requested, served):
    """Section 3.3 MC_Served: equal, or a dated snapshot of the requested identifier."""
    if not served or not requested:
        return True
    return served == requested or bool(re.fullmatch(re.escape(requested) + r"-\d{4}-?\d{2}-?\d{2}", served))


def is_answered(rec):
    return rec.get("status", "ok") == "ok" and bool((rec.get("text") or "").strip()) and not rec.get("error")


def code_answer(rec, live=None):
    """Code one choice answer. rec needs condition, category, text (+ order for LIST). Returns a dict."""
    live = live if live is not None else B.live_units()
    cat, cond = rec["category"], rec["condition"]
    out = {k: rec.get(k) for k in ("call_id", "condition", "category", "brief", "model", "model_slot",
                                   "square", "row", "run", "probe_id")}
    out.update(code=None, unit=None, reason=None, choice_line=None, other_text=None, position=None, L=None,
               order=rec.get("order"), at_limit=bool(at_length_limit(rec)) if is_answered(rec) else False)
    if rec.get("order"):
        out["L"] = len(rec["order"])
    if not served_ok(rec.get("model"), rec.get("served_model")):
        out.update(code="MISSING", reason="served_model")
        return out
    if is_refusal(rec):
        out.update(code="NONE", reason="refusal")
        return out
    if not is_answered(rec):
        out.update(code="MISSING", reason="unanswered")
        return out
    text = rec["text"]
    line, had_prefix = choice_line(text)
    if at_length_limit(rec) and not had_prefix:
        out.update(code="MISSING", reason="cut_at_limit")
        return out
    line = strip_urls(line).strip()
    out["choice_line"] = line
    hits = registry_matches(cat, line)
    if len(hits) >= 2:
        out.update(code="AMBIGUOUS", reason="two_or_more_units")
        return out
    if len(hits) == 1:
        u = hits[0]
        out["unit"] = u
        if cat == "cars" and u in B.CELL_D:
            out.update(code="DEFUNCT")
        elif u not in live[cat]:
            out.update(code="DEFUNCT" if cat == "cars" else "OFF_LIST")   # e.g. Fisker after D7
        elif cond == "LIST" and rec.get("order") and u not in rec["order"]:
            out.update(code="OFF_LIST")
        else:
            out.update(code="VALID")
            if cond == "LIST" and rec.get("order"):
                out["position"] = rec["order"].index(u) + 1
        return out
    if cond == "LIST" and not had_prefix and REFUSAL_TEXT_RE.search(strip_urls(EMPH_RE.sub("", text))):
        out.update(code="OFF_LIST", reason="refusal_text", other_text=line)   # r3 task 2 (see REFUSAL_TEXT_RE)
        return out
    if NAMES_SOMETHING_RE.search(line):
        # DECISION NEEDED: section 5.3 says "none -> OTHER if the line names something"; section 5.1 says
        # OTHER is OPEN only and OFF_LIST is "LIST: a brand not on the list". Here: LIST -> OFF_LIST, OPEN -> OTHER.
        # "Names something" = the line has at least one letter or digit.
        out.update(code="OFF_LIST" if cond == "LIST" else "OTHER", other_text=line)
    else:
        out.update(code="NONE", reason="empty_choice_line")
    return out


def code_all(records, probes=None):
    """Code a list of raw records. If probes (choice rows of the probe file) are given, condition, category,
    brief, square, row and order are filled from the probe row with the same probe_id."""
    pmap = {p["probe_id"]: p for p in (probes or [])}
    live = B.live_units()
    out = []
    for r in records:
        r = dict(r)
        p = pmap.get(r.get("probe_id"))
        if p:
            for k in ("condition", "category", "brief", "square", "row", "run", "order", "model_slot"):
                r.setdefault(k, p.get(k))
        out.append(code_answer(r, live))
    return out


def read_jsonl(path):
    return [json.loads(ln) for ln in open(path, encoding="utf-8") if ln.strip()]


def choice_probes(path=B.OUT_DEFAULT):
    return [d for d in read_jsonl(path) if d.get("part") == "choice"]


# --------------------------------------------------------------------------- dry run
ADVERSARIAL = [
    # (name, record, expected code, expected unit)
    ("two brands on the choice line",
     {"condition": "OPEN", "category": "skincare", "text": "Both are great.\nCHOICE: CeraVe or La Roche-Posay"},
     "AMBIGUOUS", None),
    ("brand in the reason, not on the choice line",
     {"condition": "OPEN", "category": "skincare",
      "text": "CeraVe is good, but I prefer something else.\nCHOICE: Neutrogena"}, "OTHER", None),
    ("Estee without accent",
     {"condition": "OPEN", "category": "skincare", "text": "Classic.\nCHOICE: Estee Lauder"}, "VALID", "Estée Lauder"),
    ("Estée with accent",
     {"condition": "OPEN", "category": "skincare", "text": "Classic.\nCHOICE: Estée Lauder"}, "VALID", "Estée Lauder"),
    # DECISION NEEDED: the certified v0.20 matcher needs "Dior Beauty"; a bare "Dior" matches no unit -> OTHER.
    ("Dior vs the unit Dior Beauty",
     {"condition": "OPEN", "category": "skincare", "text": "Luxurious.\nCHOICE: Dior"}, "OTHER", None),
    ("Cell D car", {"condition": "OPEN", "category": "cars", "text": "Nostalgia.\nCHOICE: Pontiac"}, "DEFUNCT",
     "Pontiac"),
    ("no choice line, last line names a brand",
     {"condition": "OPEN", "category": "cars", "text": "I would go with a Toyota.\nToyota"}, "VALID", "Toyota"),
    ("no choice line, last line is prose",
     {"condition": "OPEN", "category": "cars", "text": "Hard to say.\nIt depends on your needs."}, "OTHER", None),
    ("emphasis around the prefix",
     {"condition": "OPEN", "category": "spirits", "text": "Smooth.\n**CHOICE:** *Lagavulin*"}, "VALID", "Lagavulin"),
    ("last CHOICE line wins",
     {"condition": "OPEN", "category": "spirits", "text": "CHOICE: Bacardi\nOn reflection:\nchoice: Jameson"},
     "VALID", "Jameson"),
    ("URL on the choice line",
     {"condition": "OPEN", "category": "cosmetics", "text": "x\nCHOICE: NARS (https://www.lancome.com/nars)"},
     "VALID", "NARS"),
    ("LIST valid with position",
     {"condition": "LIST", "category": "cars", "order": ["Tesla", "Toyota", "Honda"],
      "text": "Reliable.\nCHOICE: Honda"}, "VALID", "Honda"),
    ("LIST, brand outside the registry",
     {"condition": "LIST", "category": "cars", "order": ["Tesla", "Toyota"], "text": "x\nCHOICE: Subaru"},
     "OFF_LIST", None),
    ("empty choice line", {"condition": "OPEN", "category": "cars", "text": "Sorry.\nCHOICE:"}, "NONE", None),
    ("refusal", {"condition": "OPEN", "category": "cars", "text": "I can't help.", "finish_reason": "refusal"},
     "NONE", None),
    ("cut at the limit, no CHOICE line",
     {"condition": "OPEN", "category": "cars", "text": "Let me think about Toyota", "finish_reason": "max_tokens"},
     "MISSING", None),
    ("at the limit but CHOICE line present",
     {"condition": "OPEN", "category": "cars", "text": "x\nCHOICE: Ford", "finish_reason": "length"}, "VALID", "Ford"),
    ("unanswered", {"condition": "OPEN", "category": "cars", "text": "", "status": "error"}, "MISSING", None),
    ("served by another model",
     {"condition": "OPEN", "category": "cars", "text": "x\nCHOICE: Ford", "model": "gpt-6-astra",
      "served_model": "gpt-6.1-sol"}, "MISSING", None),
    ("dated snapshot accepted",
     {"condition": "OPEN", "category": "cars", "text": "x\nCHOICE: Ford", "model": "gpt-6-astra",
      "served_model": "gpt-6-astra-2026-10-01"}, "VALID", "Ford"),
    ("LIST explicit refusal, no CHOICE line",
     {"condition": "LIST", "category": "cars", "order": ["Tesla", "Toyota"],
      "text": "I'm sorry, but I can't choose a car for you.\nPlease weigh these options yourself."}, "OFF_LIST", None),
    ("LIST explicit refusal, punctuation-only last line",
     {"condition": "LIST", "category": "cars", "order": ["Tesla", "Toyota"],
      "text": "I won't pick a brand on your behalf.\n--"}, "OFF_LIST", None),
    ("LIST provider refusal stays NONE",
     {"condition": "LIST", "category": "cars", "order": ["Tesla", "Toyota"], "text": "I can't choose.",
      "finish_reason": "refusal"}, "NONE", None),
    ("Rare Beauty in cosmetics",
     {"condition": "OPEN", "category": "cosmetics", "text": "x\nCHOICE: Rare Beauty"}, "VALID", "Rare Beauty"),
]


def dry_run(probes_path=B.OUT_DEFAULT, seed=46, log=print):
    """Code the adversarial cases and one synthetic answer per choice probe (no model is called)."""
    import numpy as np
    fails = []
    for name, rec, want_code, want_unit in ADVERSARIAL:
        got = code_answer(rec)
        ok = got["code"] == want_code and got["unit"] == want_unit
        log(f"  {'ok  ' if ok else 'FAIL'} {name:46s} -> {got['code']:9s} {got['unit']}")
        if not ok:
            fails.append(name)
    if Path(probes_path).exists():
        probes = choice_probes(probes_path)
    else:
        _body, probes, _pred = B.build()
    rng = np.random.default_rng(seed)
    live = B.live_units()
    raw = []
    for p in probes:
        pool = p["order"] if p["condition"] == "LIST" else live[p["category"]] + ["Acme House Brand"]
        b = pool[int(rng.integers(len(pool)))]
        raw.append({"call_id": p["probe_id"] + "__M", "probe_id": p["probe_id"], "status": "ok",
                    "text": f"A sensible pick for this buyer.\nCHOICE: {b}"})
    coded = code_all(raw, probes)
    c = Counter((d["condition"], d["code"]) for d in coded)
    log(f"  synthetic answers coded: {len(coded)}; " + ", ".join(f"{k[0]}/{k[1]} {v}" for k, v in sorted(c.items())))
    bad_pos = [d for d in coded if d["condition"] == "LIST" and d["code"] == "VALID" and not d["position"]]
    if bad_pos:
        fails.append("LIST valid without position")
    return fails, coded


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--raw")
    ap.add_argument("--probes", default=str(B.OUT_DEFAULT))
    ap.add_argument("--out")
    ap.add_argument("--judge", action="store_true",
                    help="v0.23 recognition judge (predictor blocks only). Refused in Stage 1 code r1.")
    a = ap.parse_args(argv)
    if a.judge:
        print("[v46] --judge refused: the v0.23 recognition judge runs only through v0.42's locked coder after "
              "IPA and J1 (section 3.4); no paid or keyed call is made by this script.", file=sys.stderr)
        return 2
    if a.dry_run:
        print("[v46] coder dry run (no model called)")
        fails, _ = dry_run(a.probes)
        print(f"[v46] coder dry run {'PASS' if not fails else 'FAIL: ' + ', '.join(fails)}")
        return 1 if fails else 0
    if not (a.raw and a.out):
        ap.error("--raw and --out are required unless --dry-run")
    coded = code_all(read_jsonl(a.raw), choice_probes(a.probes))
    with open(a.out, "w", encoding="utf-8") as f:
        for d in coded:
            f.write(json.dumps(d, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"[v46] coded {len(coded)} -> {a.out}: {dict(Counter(d['code'] for d in coded))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
