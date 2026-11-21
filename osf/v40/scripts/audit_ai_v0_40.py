#!/usr/bin/env python3
"""
audit_ai_v0_40.py -- AIAS(TM) v0.40, step 8: the declared audit (pre-registration section 5.5) with the AI-only
analyst of DEVIATIONS entry "Coding-only step, scripted audit draw and AI-only audit analyst" (2026-11-21).

Two independent AI coders from two providers (A: Anthropic, B: OpenAI) each code the 200 sampled answers with the
same written coding rules, blind to the rule-based codes and to each other; where A and B disagree on any code of an
answer, a third model from a third provider (T: Google) codes that answer, blind in the same way, and breaks the
tie. Agreement of the AI codes with the rule-based codes of score_v0_40.py is reported per field (percent agreement
and Cohen's kappa). Threshold (locked, section 5.5): kappa >= 0.80 on the gone-flag. There is no human check.

Every request is the same for A, B and T: one system prompt (the coding rules and the category's registry list) and
one user message (the answer text only). No request carries a rule-based code, a probe's role or another coder's
codes. No sampling parameter is sent; reasoning at each model's lowest documented effort ("low"), as v1.11.
Reply rule (programme rule of 2026-11-12; pre-registration section 5.1): exactly one complete JSON object with the
required keys counts and any text around it is ignored; an invalid reply is re-sent once.

Budget: hard cap US$25.00 for this audit (DEVIATIONS entry). Each request's (or batch's) worst case is reserved before
it is sent and no request is sent that could take recorded spend past the cap; the run then stops (exit code 9) and
the shortfall is reported. Spend is recomputed from the recorded usage on every start (resumable).

Modes:
  --dry-run       no network and no provider SDK import: builds every request, writes the prompts and a cost
                  projection (audit/dry_run_audit_ai_v0_40.txt); works before the sample exists (length proxy)
  --check-models  free model-metadata lookups only (no generation): the three model IDs are served to these keys
  --run           the paid audit (A and B through the vendors' batch APIs at 50%, T synchronous), then --analyze
  --analyze       no network: agreement tables from the recorded replies (audit/v40_audit_agreement.json, .md)
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import score_v0_40 as S  # noqa: E402  (locked scorer: registry, coder, gone-flag rule; imported, never modified)
import code_only_v0_40 as C  # noqa: E402

V40 = S.V40
UTC = timezone.utc
CAP_USD = 25.00
MAX_OUTPUT_TOKENS = 4096          # visible output + reasoning; v1.11's judge cap
MAX_PASSES = 2                    # an invalid or failed reply is re-sent once (v1.11)
CHUNK = 25                        # requests per submitted batch (bounds the worst case reserved at once)
POLL_SECONDS = 60
MAX_ATTEMPTS = 3                  # transient retries per synchronous call (v0.42 / v1.11 policy)
EXIT_GUARD = 9

# ----------------------------------------------------------------------------- coders (vendor pages read 2026-11-21)
# Each provider's newest generally available flagship; restricted and pre-release models excluded.
#  A  Anthropic Models overview (https://platform.claude.com/docs/en/about-claude/models/overview.md): latest-models
#     table led by Claude Fable 5.2, "For demanding reasoning and long-horizon agentic work", $8 / $40, "Batch API
#     requests are 50% off"; Claude Mythos 5.2 "limited availability" (excluded). Effort levels incl. "low"
#     (https://platform.claude.com/docs/en/build-with-claude/effort.md: "Claude Fable 5.2 supports all five effort levels").
#  B  OpenAI Models (https://developers.openai.com/api/docs/models.md): "GPT-6.2 Astra, our flagship model for complex
#     reasoning and coding"; model page (.../models/gpt-6.2-astra.md): "Our most capable model", $8 / $40,
#     "Batch costs 50% of Standard rates", Batch endpoint supported; no preview or restricted label for the API
#     (its Google Cloud listing is "Private preview"). Newer than GPT-6 Astra (v0.40's current arm, $10 / $50).
#  T  Google Gemini API changelog (https://ai.google.dev/gemini-api/docs/changelog), 2026-11-10: "Gemini 4 Carbon
#     (gemini-4-carbon) generally available (GA) ... our most capable reasoning model"; model page: "Stable:
#     gemini-4-carbon"; pricing page: $2.00 / $10.00 through 2026-11-30, $4.00 / $20.00 from 2026-12-01; thinking
#     levels low, medium, high. Gemini 4 Neon (GA 2026-11-18) is newer but not positioned as the most capable.
#     Google Cloud's page still limits Carbon to "verified enterprise customers in select regions"; this audit uses
#     the Gemini Developer API (GOOGLE_API_KEY), where Google states GA. --check-models confirms the key sees it.
CODERS = {
    "A": {"model_id": "claude-fable-5-2", "name": "Claude Fable 5.2", "provider": "anthropic", "mode": "batch",
          "reasoning_param": {"output_config": {"effort": "low"}}},
    "B": {"model_id": "gpt-6.2-astra", "name": "GPT-6.2 Astra", "provider": "openai", "mode": "batch",
          "reasoning_param": {"reasoning": {"effort": "low"}}},
    "T": {"model_id": "gemini-4-carbon", "name": "Gemini 4 Carbon", "provider": "google", "mode": "sync",
          "reasoning_param": {"thinking_config": {"thinking_level": "low"}}},
}
# US$ per 1M tokens (input, output; output includes reasoning / thinking). Fable 5.2: the programme's price table
# (osf/methodology v1.11 scripts/score_v1_11.py PRICES / PRICES_BATCH, branch v1.11; v0.40 pre-registration section
# 6.1) and re-read on the Models overview 2026-11-21. GPT-6.2 Astra and Gemini 4 Carbon are not yet in any repo
# price table: vendor pages read 2026-11-21 (above). Batch = 50% of standard (both vendors' pages).
PRICES = {"claude-fable-5-2": (8.0, 40.0), "gpt-6.2-astra": (8.0, 40.0), "gemini-4-carbon": (2.0, 10.0)}
PRICES_BATCH = {"claude-fable-5-2": (4.0, 20.0), "gpt-6.2-astra": (4.0, 20.0), "gemini-4-carbon": (1.0, 5.0)}
PRICE_CHANGES = {"gemini-4-carbon": ("2026-12-01T00:00:00+00:00", (4.0, 20.0), (2.0, 10.0))}
# Planning only (dry run): o200k characters per token and vendor factors from score_v1_11.py (branch v1.11).
O200K_CHARS_PER_TOKEN = 4.547
TOKEN_FACTOR = {"anthropic": 1.30, "openai": 1.10, "google": 1.10}
PLAN_VISIBLE = {"recommendation": 450, "status": 120}      # visible JSON tokens per reply (planning)
PLAN_REASONING = {"central": 1000, "high": 2500}            # reasoning tokens per reply (planning)
PLAN_TIE_SHARE = {"central": 0.5, "high": 1.0}              # share of answers sent to T


def prices(model_id, when=None, batch=False):
    p = (PRICES_BATCH if batch else PRICES)[model_id]
    ch = PRICE_CHANGES.get(model_id)
    if ch and when is not None and when >= datetime.fromisoformat(ch[0]):
        p = ch[2] if batch else ch[1]
    return p


def call_usd(model_id, tin, tout, when=None, batch=False):
    pin, pout = prices(model_id, when, batch)
    return (tin or 0) * pin / 1e6 + (tout or 0) * pout / 1e6


# ----------------------------------------------------------------------------- the coding prompt (same for A, B, T)
CATEGORY_LABEL = {"airline": "airlines", "bank": "retail banks"}
SYSTEM_TEMPLATE = """You are an independent coder for a pre-registered research study (AIAS v0.40: how AI assistants answer questions about US {label}). You code one assistant answer at a time with the written coding rules below. You see no other coder's codes. Reply with exactly one JSON object and nothing else.

CODING RULES (quoted from the study's locked pre-registration, sections 2.1, 5.2, 5.3 and 5.4; references to files and decision numbers left out)
- Mention: "a whole-word, case-sensitive match of a registry alias in an answer; the longest alias wins and overlapping shorter matches are dropped."
- Ambiguous: "A mention through a bare collision alias is ambiguous." These bare aliases are coded ambiguous: {ambiguous}.
- Gone-flag: "A mention is gone-flagged when the locked, case-insensitive lexicon (for example "no longer", "defunct", "ceased operations", "merged into/with", "acquired by", "now part of", "rebranded", "formerly", "failed", "shut down", "bankrupt") occurs within 150 characters before or after the mention."
- Successor name: the coder "records whether the successor's name (registry successor column) occurs within the same 150-character window."

HOW TO APPLY THE RULES
1. The registry list below gives each entity's ID, name, aliases and successor. Find every whole-word, case-sensitive occurrence of any alias in the answer. An alias that is part of a longer listed alias that also occurs there counts only as the longer one. When the same alias is listed under two entities, it belongs to the entity listed first. An occurrence counts even when the word is used in another sense (for example "United" in "United States"); the ambiguous code exists for such cases.
2. Report each entity with at least one mention once, with three codes taken over all of its mentions in the answer:
   - "ambiguous": true only if every mention of the entity is through one of the bare collision aliases above (that exact alias, not a longer alias containing it); otherwise false.
   - "gone_flag": true if, for at least one of its mentions, the text within about 150 characters (about 25 words) before or after that mention contains wording of the lexicon's kind: words that say something no longer exists or operates, ceased, closed, failed, went bankrupt, was merged, acquired, absorbed, renamed or rebranded, or is now part of something else (the examples above, or the same meaning in other words). Otherwise false.
   - "successor_near": true if a name in the entity's successor field occurs within about 150 characters before or after at least one of its mentions; false if not, or if the entity has no successor.
3. "opening_says_gone": true if the first 300 characters of the answer contain wording of the gone-flag kind (as in rule 2), otherwise false.
4. Code only the answer text. Use only IDs from the list. If no entity is mentioned, give an empty list.

REPLY FORMAT (exactly one JSON object, no other text):
{{"mentions": [{{"entity": "<ID>", "ambiguous": false, "gone_flag": false, "successor_near": false}}], "opening_says_gone": false}}

REGISTRY LIST ({label}; ID | name | aliases | successor)
{entities}
"""
USER_TEMPLATE = "Answer to code:\n<answer>\n{text}\n</answer>"
REQUIRED_KEYS = ("mentions", "opening_says_gone")
MENTION_KEYS = ("ambiguous", "gone_flag", "successor_near")


def entity_list(units, subjects, category):
    """Entities of one category in the scorer's precedence order: ghosts and controls first (registry order), then
    current units; one row per ID (Sun Country is both a control and a unit under the same ID)."""
    rows, seen = [], {}
    for e in [s for s in subjects if s["category"] == category] + [u for u in units if u["category"] == category]:
        if e["id"] in seen:
            r = seen[e["id"]]
            r["aliases"] += [a for a in e["aliases"] if a not in r["aliases"]]
            continue
        succ = (e.get("successor") or "").strip()
        r = {"id": e["id"], "name": e.get("brand") or e["aliases"][0], "aliases": list(e["aliases"]),
             "successor": "" if (not succ or succ.lower().startswith("none")) else succ}
        seen[e["id"]] = r
        rows.append(r)
    return rows


def system_prompt(units, subjects, category):
    ents = "\n".join(f"{r['id']} | {r['name']} | {'; '.join(r['aliases'])} | {r['successor'] or '-'}"
                     for r in entity_list(units, subjects, category))
    return SYSTEM_TEMPLATE.format(label=CATEGORY_LABEL[category], ambiguous=", ".join(sorted(S.AMBIGUOUS)),
                                  entities=ents)


def user_message(text):
    return USER_TEMPLATE.format(text=text)


# ----------------------------------------------------------------------------- reply rule (exactly one JSON object)
def json_objects(text):
    """Every complete top-level JSON object in a reply, left to right (text between them is ignored)."""
    dec, out, i = json.JSONDecoder(), [], 0
    text = text or ""
    while True:
        j = text.find("{", i)
        if j < 0:
            return out
        try:
            obj, end = dec.raw_decode(text, j)
        except ValueError:
            i = j + 1
            continue
        if isinstance(obj, dict):
            out.append(obj)
        i = end


def parse_reply(text, valid_ids):
    """(codes, error). codes = {"mentions": {entity: {ambiguous, gone_flag, successor_near}}, "opening_says_gone",
    "unknown_entities"}. Valid only when exactly one complete JSON object carries the required keys with the
    required types; entries naming an ID outside the list are dropped and counted."""
    cands = [o for o in json_objects(text) if all(k in o for k in REQUIRED_KEYS)]
    if len(cands) != 1:
        return None, f"{len(cands)} JSON objects with the required keys"
    o = cands[0]
    if not isinstance(o["mentions"], list) or not isinstance(o["opening_says_gone"], bool):
        return None, "wrong types for the required keys"
    ms, unknown = {}, []
    for m in o["mentions"]:
        if not isinstance(m, dict) or not isinstance(m.get("entity"), str) or \
                not all(isinstance(m.get(k), bool) for k in MENTION_KEYS):
            return None, "a mention entry lacks entity or a boolean code"
        e = m["entity"].strip()
        if e not in valid_ids:
            unknown.append(e)
            continue
        if e in ms:                     # repeated entity: merged as the per-entity rule reads (all / any / any)
            ms[e] = {"ambiguous": ms[e]["ambiguous"] and m["ambiguous"], "gone_flag": ms[e]["gone_flag"] or m["gone_flag"],
                     "successor_near": ms[e]["successor_near"] or m["successor_near"]}
        else:
            ms[e] = {k: m[k] for k in MENTION_KEYS}
    return {"mentions": ms, "opening_says_gone": o["opening_says_gone"], "unknown_entities": unknown}, None


# ----------------------------------------------------------------------------- rule-based codes (locked coder)
def rule_codes(sc, r):
    """Per entity of one coded answer, aggregated as the AI coders are asked to: ambiguous = every mention ambiguous,
    gone_flag / successor_near = any mention. status_flag = score_v0_40.Scorer.flagged (section 2.1), S answers only."""
    ms = defaultdict(list)
    for m in r["_m"]:
        ms[m["entity"]].append(m)
    out = {e: {"ambiguous": all(m["ambiguous"] for m in v), "gone_flag": any(m["gone_flag"] for m in v),
               "successor_near": any(m["successor_near"] for m in v)} for e, v in ms.items()}
    sf = sc.flagged(r, r["brand_id"]) if r["tier"] == "S" else None
    return {"mentions": out, "status_flag": sf}


# ----------------------------------------------------------------------------- consensus (A, B; T breaks ties)
def _named(codes, e):
    return None if codes is None else (e in codes["mentions"])


def disagree(a, b, cand_ids):
    """True when A and B differ on any code of the answer (or one of them has no valid reply)."""
    if a is None or b is None:
        return True
    if a["opening_says_gone"] != b["opening_says_gone"]:
        return True
    for e in cand_ids:
        na, nb = e in a["mentions"], e in b["mentions"]
        if na != nb:
            return True
        if na and any(a["mentions"][e][k] != b["mentions"][e][k] for k in MENTION_KEYS):
            return True
    return False


def _vote(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    t = sum(1 for v in vals if v)
    if 2 * t > len(vals):
        return True
    if 2 * t < len(vals):
        return False
    return None                                          # tie among the available coders: unresolved


def consensus(a, b, t, cand_ids):
    """AI consensus codes per entity: A and B when they agree, otherwise the majority of the coders that gave a value
    (A, B and the tie-breaker T); unresolved (None) when no strict majority exists."""
    def field(get):
        va, vb = get(a), get(b)
        if va is not None and vb is not None and va == vb:
            return va
        return _vote([va, vb, get(t)])
    out = {"mentions": {}, "named": {}, "opening_says_gone": field(lambda c: None if c is None else c["opening_says_gone"])}
    for e in cand_ids:
        n = field(lambda c: _named(c, e))
        out["named"][e] = n
        if n:
            out["mentions"][e] = {k: field(lambda c, k=k: (c["mentions"][e][k] if c is not None and e in c["mentions"]
                                                             else None)) for k in MENTION_KEYS}
    return out


# ----------------------------------------------------------------------------- agreement statistics
def kappa(pairs):
    """Percent agreement and Cohen's kappa for binary (x, y) pairs; kappa None when chance agreement is 1."""
    n = len(pairs)
    if not n:
        return {"n": 0, "agree": 0, "percent_agreement": None, "kappa": None, "table": None}
    a = sum(1 for x, y in pairs if x == y)
    x1 = sum(1 for x, _ in pairs if x) / n
    y1 = sum(1 for _, y in pairs if y) / n
    po, pe = a / n, x1 * y1 + (1 - x1) * (1 - y1)
    k = None if abs(1 - pe) < 1e-12 else (po - pe) / (1 - pe)
    tab = {"rule1_ai1": sum(1 for x, y in pairs if x and y), "rule1_ai0": sum(1 for x, y in pairs if x and not y),
           "rule0_ai1": sum(1 for x, y in pairs if not x and y), "rule0_ai0": sum(1 for x, y in pairs if not x and not y)}
    return {"n": n, "agree": a, "percent_agreement": 100 * po, "kappa": k, "table": tab}


KAPPA_MIN = 0.80                        # locked threshold, pre-registration section 5.5 (gone-flag)
MARKED_IF_MISS = ["H_Flag", "H_Afterlife", "H_Search"]
MISS_LABEL = "coder reliability below threshold"
FIELDS = ["subject", "ambiguous", "gone_flag", "successor_near", "status_flag"]


def view(codes, cand_ids):
    """A single coder's codes in the consensus layout (named per candidate entity)."""
    if codes is None:
        return None
    return {"named": {e: (e in codes["mentions"]) for e in cand_ids}, "mentions": codes["mentions"],
            "opening_says_gone": codes["opening_says_gone"]}


def field_pairs(item, x, y):
    """Pairs (x, y) per field for one answer; x and y are views (rule view first when comparing with the rule)."""
    out = {f: [] for f in FIELDS}
    if x is None or y is None:
        return out
    for e in item["cand_ids"]:
        nx, ny = x["named"].get(e), y["named"].get(e)
        if nx is None or ny is None:
            continue
        out["subject"].append((nx, ny))
        if nx and ny:
            for k in ("ambiguous", "gone_flag") + (("successor_near",) if e in item["succ_ids"] else ()):
                vx, vy = x["mentions"][e].get(k), y["mentions"][e].get(k)
                if vx is not None and vy is not None:
                    out[k].append((vx, vy))
    if item["set"] == "status":
        sx, sy = status_flag(item, x), status_flag(item, y)
        if sx is not None and sy is not None:
            out["status_flag"].append((sx, sy))
    return out


def status_flag(item, v):
    """Section 2.1: flagged when a mention of the subject is gone-flagged; when the subject is not named, when the
    gone wording occurs in the first 300 characters."""
    if "status_flag" in v and v.get("status_flag") is not None:
        return v["status_flag"]                                    # the rule view carries Scorer.flagged directly
    ent = item["subject_entity"]
    n = v["named"].get(ent)
    if n is None:
        return None
    return v["mentions"][ent].get("gone_flag") if n else v.get("opening_says_gone")


def rule_view(item):
    rc = item["rule"]
    return {"named": {e: (e in rc["mentions"]) for e in item["cand_ids"]}, "mentions": rc["mentions"],
            "opening_says_gone": None, "status_flag": rc["status_flag"]}


def agreement(items, coded):
    """coded: {role: {call_id: codes or None}}. Per comparison and field: n, percent agreement, Cohen's kappa."""
    comps = {"consensus_vs_rule": [], "A_vs_rule": [], "B_vs_rule": [], "A_vs_B": []}
    for it in items:
        cid, cand = it["call_id"], it["cand_ids"]
        a, b, t = (coded.get(r, {}).get(cid) for r in ("A", "B", "T"))
        cons = consensus(a, b, t, cand)
        it["_consensus"] = cons
        rv = rule_view(it)
        comps["consensus_vs_rule"].append(field_pairs(it, rv, cons))
        comps["A_vs_rule"].append(field_pairs(it, rv, view(a, cand)))
        comps["B_vs_rule"].append(field_pairs(it, rv, view(b, cand)))
        comps["A_vs_B"].append(field_pairs(it, view(a, cand), view(b, cand)))
    res = {}
    for name, per in comps.items():
        res[name] = {}
        for f in FIELDS:
            res[name][f] = {"all": kappa([p for d in per for p in d[f]])}
            for st in ("recommendation", "status"):
                res[name][f][st] = kappa([p for d, it in zip(per, items) if it["set"] == st for p in d[f]])
    return res


def sample_rates(items, ghost_ids):
    """The analyst-coded (AI consensus) rates of the sample, with the rule-coded rates of the same answers beside them
    (section 5.5: reported beside H_Flag, H_Afterlife and H_Search on a miss)."""
    out = {}
    for who in ("rule", "ai"):
        g = [status_flag(it, rule_view(it) if who == "rule" else it["_consensus"]) for it in items
             if it["set"] == "status" and it["role"] == "ghost"]
        c = [status_flag(it, rule_view(it) if who == "rule" else it["_consensus"]) for it in items
             if it["set"] == "status" and it["role"] in ("control", "incumbent")]
        pairs = []
        for it in items:
            if it["set"] != "recommendation":
                continue
            v = rule_view(it) if who == "rule" else it["_consensus"]
            for e in it["cand_ids"]:
                if e in ghost_ids and v["named"].get(e) and v["mentions"][e].get("ambiguous") is False:
                    gf = v["mentions"][e].get("gone_flag")
                    if gf is not None:
                        pairs.append(not gf)
        rate = lambda xs: (sum(1 for x in xs if x) / len(xs)) if xs else None  # noqa: E731
        g, c = [x for x in g if x is not None], [x for x in c if x is not None]
        out[who] = {"status_ghost_answers": len(g), "status_ghost_flag_rate": rate(g),
                    "status_control_answers": len(c), "status_control_flag_rate": rate(c),
                    "rec_ghost_mentions": len(pairs), "rec_ghost_mentions_not_gone_flagged_rate": rate(pairs)}
    return out


def unresolved(items):
    n = {"named": 0, "codes": 0, "opening_says_gone": 0}
    for it in items:
        c = it["_consensus"]
        n["named"] += sum(1 for v in c["named"].values() if v is None)
        n["codes"] += sum(1 for m in c["mentions"].values() for v in m.values() if v is None)
        n["opening_says_gone"] += c["opening_says_gone"] is None
    return n


def summarize(items, coded, ghost_ids, meta):
    agr = agreement(items, coded)
    k = agr["consensus_vs_rule"]["gone_flag"]["all"]["kappa"]
    met = k is not None and k >= KAPPA_MIN
    return {"phase": "v0.40", "step": "audit (section 5.5) with the AI-only analyst (DEVIATIONS 2026-11-21)",
            "human_check": False, "coders": {r: CODERS[r]["model_id"] for r in CODERS}, **meta,
            "threshold": {"field": "gone_flag", "comparison": "consensus_vs_rule", "kappa_min": KAPPA_MIN,
                          "kappa": k, "met": met,
                          "note": None if k is not None else "kappa undefined (no variation); read as not met"},
            "marked_tests": [] if met else MARKED_IF_MISS, "mark": None if met else MISS_LABEL,
            "coder_not_changed": True, "agreement": agr, "sample_rates": sample_rates(items, ghost_ids),
            "unresolved_consensus_codes": unresolved(items),
            "answers": {"total": len(items), "tie_broken": sum(1 for it in items if coded.get("T", {}).get(it["call_id"])),
                        "missing": {r: sum(1 for it in items if coded.get(r, {}).get(it["call_id"]) is None)
                                    for r in ("A", "B")}}}


# ----------------------------------------------------------------------------- items (sample + locked rule codes)
def load_registry():
    units, subjects, _ = S.load_registry()
    return units, subjects + S.switch_controls(subjects)


def verify_sample(base):
    """The sample files must match AUDIT_SAMPLE_v0_40.sha256 (written by audit_draw_v0_40.py)."""
    aud = Path(base) / "audit"
    for line in (aud / "AUDIT_SAMPLE_v0_40.sha256").read_text(encoding="utf-8").splitlines():
        h, p = line.split(None, 1)
        f = Path(base) / Path(p).relative_to("osf/v40")
        if C.sha256_file(f) != h:
            raise SystemExit(f"[audit_ai] {p} does not match the sample manifest; stop")
    return json.loads((aud / "v40_audit_sample.json").read_text(encoding="utf-8"))


def build_items(sample, records, units, subjects, probes, mentions_rows=None):
    by_id = {r["call_id"]: r for r in records}
    picked = [by_id[x["call_id"]] for x in sample["items"]]
    sc = S.Scorer(picked, units, subjects, {}, perms=0)       # the locked coder, on the sampled answers only
    kept = {r["call_id"]: r for r in sc.ok}
    role_of = {p["probe_id"]: p.get("subject_role") for p in probes}
    ents = {cat: entity_list(units, subjects, cat) for cat in ("airline", "bank")}
    if mentions_rows is not None:                             # the codes must be those of the coding-only file
        want = defaultdict(list)
        for m in mentions_rows:
            if m["call_id"] in kept:
                want[m["call_id"]].append((m["entity"], int(m["start"])))
        for cid, r in kept.items():
            if sorted(want.get(cid, [])) != sorted((m["entity"], m["start"]) for m in r["_m"]):
                raise SystemExit(f"[audit_ai] rule codes of {cid} differ from v40_mentions.csv; stop")
    items = []
    for x in sample["items"]:
        r = kept.get(x["call_id"])
        if r is None:
            raise SystemExit(f"[audit_ai] sampled answer {x['call_id']} is not a coded answer; stop")
        el = ents[r["category"]]
        items.append({"call_id": r["call_id"], "set": x["set"], "stratum": x["stratum"], "category": r["category"],
                      "role": role_of.get(r["probe_id"]) if x["set"] == "status" else None,
                      "subject_entity": sc.inc.get(r.get("brand_id"), r.get("brand_id")),
                      "cand_ids": [e["id"] for e in el], "succ_ids": {e["id"] for e in el if e["successor"]},
                      "text": r["text"], "rule": rule_codes(sc, r)})
    ghost_ids = {s["id"] for s in subjects if s["role"] == "ghost"}
    return items, ghost_ids


def request_for(item, units, subjects, _cache={}):
    key = (item["category"], id(units), id(subjects))
    if key not in _cache:
        _cache[key] = system_prompt(units, subjects, item["category"])
    return {"system": _cache[key], "user": user_message(item["text"])}


def request_kwargs(role, system, user):
    """The exact SDK request for a coder (v1.11 request shapes; no sampling parameter)."""
    c = CODERS[role]
    m, rp = c["model_id"], c["reasoning_param"]
    if c["provider"] == "anthropic":
        return {"model": m, "max_tokens": MAX_OUTPUT_TOKENS, "system": system,
                "messages": [{"role": "user", "content": user}], **rp}
    if c["provider"] == "openai":
        return {"model": m, "instructions": system, "input": user, "max_output_tokens": MAX_OUTPUT_TOKENS, **rp}
    return {"model": m, "contents": user,
            "config": {"system_instruction": system, "max_output_tokens": MAX_OUTPUT_TOKENS, **rp}}


# ----------------------------------------------------------------------------- budget guard
class GuardStop(Exception):
    pass


class Guard:
    """Hard cap from recorded usage: worst cases are reserved before sending; nothing is sent that could take
    recorded spend past the cap (the run then stops)."""

    def __init__(self, cap=CAP_USD, spent=0.0):
        self.cap, self.spent, self.reserved = cap, spent, 0.0
        self.lock = threading.Lock()
        self.stopped = None

    def reserve(self, w):
        with self.lock:
            if self.stopped:
                raise GuardStop(self.stopped)
            if self.spent + self.reserved + w > self.cap + 1e-9:
                self.stopped = (f"next request's worst case ${w:.4f} would take spend ${self.spent:.4f} "
                                f"(+${self.reserved:.4f} reserved) past the ${self.cap:.2f} cap")
                raise GuardStop(self.stopped)
            self.reserved += w

    def reserve_batch(self, ws):
        """Reserve as many leading items as fit; 0 when other requests in flight hold the room; GuardStop when even
        one item would not fit with nothing in flight."""
        with self.lock:
            if self.stopped:
                raise GuardStop(self.stopped)
            k, tot = 0, 0.0
            for w in ws:
                if self.spent + self.reserved + tot + w > self.cap + 1e-9:
                    break
                tot += w
                k += 1
            if k == 0 and self.reserved < 1e-9 and ws:
                self.stopped = (f"worst case ${ws[0]:.4f} would take spend ${self.spent:.4f} past the "
                                f"${self.cap:.2f} cap")
                raise GuardStop(self.stopped)
            self.reserved += tot
            return k

    def settle(self, w, actual):
        with self.lock:
            self.reserved = self.reserved - w
            if self.reserved < 1e-9:                 # float residue: nothing is in flight
                self.reserved = 0.0
            self.spent += actual


def worst_usd(role, kw, when, batch):
    tin = len(json.dumps(kw).encode("utf-8"))                   # tokens <= bytes of the request (v1.11)
    tout = MAX_OUTPUT_TOKENS * (2 if CODERS[role]["provider"] == "google" else 1)
    return call_usd(CODERS[role]["model_id"], tin, tout, when, batch)


def actual_usd(role, when, tin, tout, tthought, batch):
    """Google thinking tokens are billed as output beside the candidate count; the others' output counts include
    reasoning (as v1.11)."""
    out = (tout or 0) + ((tthought or 0) if CODERS[role]["provider"] == "google" else 0)
    return call_usd(CODERS[role]["model_id"], tin or 0, out, when, batch)


# ----------------------------------------------------------------------------- provider calls (forked from v1.11)
class Transient(Exception):
    pass


def parse_anthropic_message(d):
    """A Messages API response (dict). All input tokens at the base input price (cache read/write included: an
    upper bound); output tokens include thinking."""
    u = d.get("usage") or {}
    tin = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return {"text": "".join(b.get("text", "") for b in (d.get("content") or []) if b.get("type") == "text"),
            "served_model": d.get("model"), "finish_reason": d.get("stop_reason"),
            "tokens_in": tin, "tokens_out": u.get("output_tokens"), "tokens_thought": None}


def parse_openai_response(d):
    """A Responses API response (dict; the batch output line's response.body)."""
    u = d.get("usage") or {}
    det = u.get("output_tokens_details") or {}
    text = "".join(c.get("text", "") for item in (d.get("output") or []) if item.get("type") == "message"
                   for c in (item.get("content") or []) if c.get("type") == "output_text")
    fr = d.get("status")
    inc = d.get("incomplete_details") or {}
    if inc.get("reason"):
        fr = f"{fr}:{inc['reason']}"
    return {"text": text, "served_model": d.get("model"), "finish_reason": fr, "tokens_in": u.get("input_tokens"),
            "tokens_out": u.get("output_tokens"), "tokens_thought": det.get("reasoning_tokens")}


PARSERS = {"anthropic": parse_anthropic_message, "openai": parse_openai_response}


def served_ok(requested, served):
    s = (served or "").strip().removeprefix("models/")
    return s == requested or re.fullmatch(re.escape(requested) + r"-(\d{4}-\d{2}-\d{2}|\d{8})", s) is not None


def call_google(kw):
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    c = dict(kw["config"])
    tc = c.pop("thinking_config", None)
    cfg = types.GenerateContentConfig(**c, thinking_config=types.ThinkingConfig(
        thinking_level=tc["thinking_level"]) if tc else None)
    try:
        r = client.models.generate_content(model=kw["model"], contents=kw["contents"], config=cfg)
    except errors.ServerError as e:
        raise Transient(str(e)) from e
    except errors.ClientError as e:
        if getattr(e, "code", None) == 429:
            raise Transient(str(e)) from e
        raise
    try:
        fr = str(r.candidates[0].finish_reason)
    except Exception:
        fr = None
    try:
        text = r.text or ""
    except Exception:
        text = ""
    um = r.usage_metadata
    return {"text": text, "served_model": getattr(r, "model_version", None), "finish_reason": fr,
            "tokens_in": getattr(um, "prompt_token_count", None), "tokens_out": getattr(um, "candidates_token_count", None),
            "tokens_thought": getattr(um, "thoughts_token_count", None)}


def call_with_retry(fn, kw, sleep=time.sleep):
    last = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fn(kw), attempt, None
        except Transient as e:
            last = f"transient: {e}"[:500]
            if attempt < MAX_ATTEMPTS:
                sleep(2 ** (attempt - 1))
        except Exception as e:  # noqa: BLE001
            return None, attempt, f"{type(e).__name__}: {e}"[:500]
    return None, MAX_ATTEMPTS, last


class RealBatchClient:
    """Anthropic Message Batches API and OpenAI Batch API (/v1/responses), as v1.11. Network: --run only."""
    TERMINAL = {"anthropic": {"ended"}, "openai": {"completed", "failed", "expired", "cancelled"}}

    def __init__(self):
        self._c = {}

    def _client(self, provider):
        if provider not in self._c:
            if provider == "anthropic":
                import anthropic
                self._c[provider] = anthropic.Anthropic()
            else:
                import openai
                self._c[provider] = openai.OpenAI()
        return self._c[provider]

    def submit(self, provider, items):
        c = self._client(provider)
        if provider == "anthropic":
            return c.messages.batches.create(requests=[{"custom_id": cid, "params": kw} for cid, kw in items]).id
        body = "".join(json.dumps({"custom_id": cid, "method": "POST", "url": "/v1/responses", "body": kw},
                                  ensure_ascii=False) + "\n" for cid, kw in items).encode("utf-8")
        f = c.files.create(file=("v0_40_audit_batch.jsonl", body), purpose="batch")
        return c.batches.create(input_file_id=f.id, endpoint="/v1/responses", completion_window="24h").id

    def status(self, provider, batch_id):
        c = self._client(provider)
        st = (c.messages.batches.retrieve(batch_id).processing_status if provider == "anthropic"
              else c.batches.retrieve(batch_id).status)
        return st in self.TERMINAL[provider], st

    def results(self, provider, batch_id):
        c = self._client(provider)
        out = {}
        if provider == "anthropic":
            for r in c.messages.batches.results(batch_id):
                d = r.model_dump()
                res = d.get("result") or {}
                out[d["custom_id"]] = ({"body": res.get("message"), "error": None} if res.get("type") == "succeeded"
                                       else {"body": None, "error": f"{res.get('type')}: {res.get('error')}"[:500]})
            return out
        b = c.batches.retrieve(batch_id)
        for fid in (b.output_file_id, b.error_file_id):
            if not fid:
                continue
            for line in c.files.content(fid).text.splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)
                resp = d.get("response") or {}
                if d.get("error") or resp.get("status_code") != 200:
                    out[d["custom_id"]] = {"body": None, "error": str(d.get("error") or resp.get("body"))[:500]}
                else:
                    out[d["custom_id"]] = {"body": resp.get("body"), "error": None}
        return out


def check_models():
    """Free metadata lookups (no generation, no charge): each coder's model ID is served to the key in use."""
    out = {}
    for role, c in CODERS.items():
        try:
            if c["provider"] == "anthropic":
                import anthropic
                out[role] = anthropic.Anthropic().models.retrieve(c["model_id"]).id
            elif c["provider"] == "openai":
                import openai
                out[role] = openai.OpenAI().models.retrieve(c["model_id"]).id
            else:
                from google import genai
                client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])     # keep a reference (open client)
                out[role] = client.models.get(model=c["model_id"]).name
        except Exception as e:  # noqa: BLE001
            out[role] = f"ERROR {type(e).__name__}: {e}"[:300]
    ok = all(not str(v).startswith("ERROR") and str(v).removeprefix("models/") == CODERS[r]["model_id"]
             for r, v in out.items())
    return ok, out


# ----------------------------------------------------------------------------- the run (resumable)
def _sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def custom_id(role, call_id, pas):
    return f"v040a-{role}-{pas}-" + hashlib.sha256(call_id.encode("utf-8")).hexdigest()[:24]


class Audit:
    def __init__(self, base, items, units, subjects, batch_client=None, dispatch=None, cap=CAP_USD,
                 sim=False, now=None, log=print):
        self.base, self.items, self.units, self.subjects = Path(base), items, units, subjects
        self.aud = self.base / "audit"
        self.raw, self.journal = self.aud / "ai_raw_v0_40.jsonl", self.aud / "ai_batches_v0_40.jsonl"
        self.bc, self.dispatch = batch_client, dispatch or {"google": call_google}
        self.sim, self.now, self.log = sim, now or (lambda: datetime.now(UTC)), log
        self.by = {it["call_id"]: it for it in items}
        self.lock = threading.Lock()
        self.passes = defaultdict(int)          # (role, call_id) -> replies recorded
        self.coded = {r: {} for r in CODERS}    # role -> call_id -> codes (valid replies only)
        spent = 0.0
        for rec in self._read(self.raw):
            spent += rec.get("usd") or 0.0
            self._apply(rec, write=False)
        self.guard = Guard(cap, spent)

    @staticmethod
    def _read(p):
        if not Path(p).exists():
            return []
        return [json.loads(x) for x in Path(p).read_text(encoding="utf-8").splitlines() if x.strip()]

    def _append(self, p, obj):
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def _apply(self, rec, write=True):
        with self.lock:
            if write:
                self._append(self.raw, rec)
            key = (rec["role"], rec["call_id"])
            self.passes[key] += 1
            if rec.get("valid") and rec["call_id"] in self.by:
                codes, _ = parse_reply(rec["text"], set(self.by[rec["call_id"]]["cand_ids"]))
                self.coded[rec["role"]][rec["call_id"]] = codes

    def request(self, role, it):
        rq = request_for(it, self.units, self.subjects)
        return request_kwargs(role, rq["system"], rq["user"])

    def record(self, role, it, kw, out, err, cost, w, t0, extra):
        model = CODERS[role]["model_id"]
        perr = None
        if out is not None and not served_ok(model, out.get("served_model")):
            perr = f"served model {out.get('served_model')!r} is not {model}"
        codes = None
        if out is not None and perr is None:
            codes, perr = parse_reply(out.get("text"), set(it["cand_ids"]))
        return {"role": role, "model": model, "call_id": it["call_id"], "pass": self.passes[(role, it["call_id"])] + 1,
                "status": "ok" if out is not None else "error", "error": err, "valid": codes is not None,
                "parse_error": perr if out is not None else None, "text": (out or {}).get("text", ""),
                "served_model": (out or {}).get("served_model"), "finish_reason": (out or {}).get("finish_reason"),
                "tokens_in": (out or {}).get("tokens_in"), "tokens_out": (out or {}).get("tokens_out"),
                "tokens_thought": (out or {}).get("tokens_thought"), "usd": cost, "worst_case_usd": w,
                "request_sha256": _sha(kw), "started_utc": t0, "finished_utc": self.now().isoformat(), **extra}

    def pending(self, role, ids=None):
        ids = [it["call_id"] for it in self.items] if ids is None else ids
        return [c for c in ids if c not in self.coded[role] and self.passes[(role, c)] < MAX_PASSES]

    # --- batches (coders A and B)
    def open_batches(self):
        ents = self._read(self.journal)
        closed = {e["batch_id"] for e in ents if e.get("event") == "collected"}
        return [e for e in ents if e.get("event") == "submitted" and e["batch_id"] not in closed]

    def collect(self, entry):
        role, prov, bid = entry["role"], CODERS[entry["role"]]["provider"], entry["batch_id"]
        polls = 0
        while True:
            try:
                ended, status = self.bc.status(prov, bid)
            except Exception as e:  # noqa: BLE001  (keep polling: the batch is already paid for)
                ended, status = False, f"status error: {type(e).__name__}: {e}"[:300]
            if ended:
                break
            polls += 1
            time.sleep(0 if self.sim else POLL_SECONDS)
        res = self.bc.results(prov, bid)
        when = datetime.fromisoformat(entry["submitted_utc"])
        for x in entry["items"]:
            it = self.by[x["call_id"]]
            kw = self.request(role, it)
            r = res.get(x["custom_id"]) or {"body": None, "error": f"missing from the batch results ({status})"}
            out = PARSERS[prov](r["body"]) if r.get("body") is not None else None
            cost = actual_usd(role, when, out.get("tokens_in"), out.get("tokens_out"), out.get("tokens_thought"),
                              True) if out else 0.0
            self.guard.settle(x["worst_case_usd"], cost)
            self._apply(self.record(role, it, kw, out, None if out else r.get("error"), cost, x["worst_case_usd"],
                                    entry["submitted_utc"], {"mode": "batch", "batch_id": bid,
                                                             "custom_id": x["custom_id"], "batch_status": status}))
        with self.lock:
            self._append(self.journal, {"event": "collected", "batch_id": bid, "role": role, "status": status,
                                        "results": len(res), "polls": polls, "collected_utc": self.now().isoformat()})

    def reattach(self):
        """Batches submitted by an interrupted run: hold their worst cases and record them before anything new."""
        ents = self.open_batches()
        for e in ents:
            self.guard.reserved += sum(x["worst_case_usd"] for x in e["items"])
        for e in ents:
            self.log(f"[audit_ai] re-attaching batch {e['batch_id']} ({e['role']}, {len(e['items'])} requests)")
            self.collect(e)
        return len(ents)

    def batch_worker(self, role):
        prov = CODERS[role]["provider"]
        while True:
            pend = self.pending(role)
            if not pend or self.guard.stopped:
                return
            now = self.now()
            cand = []
            for cid in pend[:CHUNK]:
                kw = self.request(role, self.by[cid])
                cand.append((cid, kw, worst_usd(role, kw, now, True)))
            try:
                k = self.guard.reserve_batch([c[2] for c in cand])
            except GuardStop:
                return
            if k == 0:
                time.sleep(0.01 if self.sim else POLL_SECONDS)
                continue
            cand = cand[:k]
            items = [(custom_id(role, cid, self.passes[(role, cid)] + 1), kw) for cid, kw, _ in cand]
            try:
                bid = self.bc.submit(prov, items)
            except Exception as e:  # noqa: BLE001
                for *_, w in cand:
                    self.guard.settle(w, 0.0)
                self.guard.stopped = f"batch submission failed ({role}): {type(e).__name__}: {e}"[:300]
                return
            entry = {"event": "submitted", "batch_id": bid, "role": role, "model": CODERS[role]["model_id"],
                     "submitted_utc": now.isoformat(), "n": len(items), "worst_case_usd": sum(c[2] for c in cand),
                     "items": [{"custom_id": ci, "call_id": cid, "worst_case_usd": w}
                               for (ci, _), (cid, _, w) in zip(items, cand)]}
            with self.lock:
                self._append(self.journal, entry)
            self.collect(entry)

    # --- tie-breaker T (synchronous)
    def needs_tiebreak(self):
        out = []
        for it in self.items:
            cid = it["call_id"]
            a_done = cid in self.coded["A"] or self.passes[("A", cid)] >= MAX_PASSES
            b_done = cid in self.coded["B"] or self.passes[("B", cid)] >= MAX_PASSES
            if a_done and b_done and disagree(self.coded["A"].get(cid), self.coded["B"].get(cid), it["cand_ids"]):
                out.append(cid)
        return out

    def tiebreak(self):
        role, prov = "T", CODERS["T"]["provider"]
        for cid in self.needs_tiebreak():
            while cid not in self.coded[role] and self.passes[(role, cid)] < MAX_PASSES:
                it = self.by[cid]
                kw = self.request(role, it)
                now = self.now()
                w = worst_usd(role, kw, now, False)
                try:
                    self.guard.reserve(w)
                except GuardStop:
                    return
                t0 = now.isoformat()
                out, tries, err = call_with_retry(self.dispatch[prov], kw, sleep=(lambda s: None) if self.sim else time.sleep)
                cost = actual_usd(role, now, out.get("tokens_in"), out.get("tokens_out"), out.get("tokens_thought"),
                                  False) if out else 0.0
                self.guard.settle(w, cost)
                self._apply(self.record(role, it, kw, out, err, cost, w, t0, {"mode": "sync", "tries": tries}))

    def run(self):
        self.reattach()
        threads = [threading.Thread(target=self.batch_worker, args=(r,)) for r in ("A", "B")]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        if not self.guard.stopped:
            self.tiebreak()
        return self.guard.stopped

    def summary(self):
        ghost_ids = {s["id"] for s in self.subjects if s["role"] == "ghost"}
        meta = {"cap_usd": self.guard.cap, "spent_usd": round(self.guard.spent, 6), "guard_stopped": self.guard.stopped,
                "complete": not self.guard.stopped and not self.pending("A") and not self.pending("B")
                and all(c in self.coded["T"] or self.passes[("T", c)] >= MAX_PASSES for c in self.needs_tiebreak())}
        return summarize(self.items, self.coded, ghost_ids, meta)


# ----------------------------------------------------------------------------- dry run (no network, no SDK)
RUN_DATE = datetime(2026, 11, 23, 15, 0, tzinfo=UTC)       # Monday 11/23 (step 8): prices in force


def est_tokens(chars, provider):
    return chars / O200K_CHARS_PER_TOKEN * TOKEN_FACTOR[provider]


def projection(reqs):
    """reqs: [(set, system_chars, user_chars)]. Central and high cost per coder and in total (US$)."""
    out = {}
    for case in ("central", "high"):
        per = {}
        for role, c in CODERS.items():
            batch = c["mode"] == "batch"
            tot = 0.0
            for st, sc_, uc in reqs:
                tin = est_tokens(sc_ + uc, c["provider"])
                tot += call_usd(c["model_id"], tin, PLAN_VISIBLE[st] + PLAN_REASONING[case], RUN_DATE, batch)
            per[role] = tot * (PLAN_TIE_SHARE[case] if role == "T" else 1.0)
        out[case] = {"per_coder": per, "total": sum(per.values())}
    return out


def proxy_requests(records, units, subjects):
    """Before the sample exists: 100 recommendation and 100 status answers in the population's category mix, at the
    population's mean answer length (central) and 90th percentile (high). Lengths only; nothing is coded."""
    from statistics import mean
    pops = defaultdict(list)
    for r in records:
        if r.get("status") == "ok" and (r.get("text") or "").strip() and r["kind"] in ("recommendation", "status"):
            pops[(r["kind"], r["category"])].append(len(user_message(r["text"])))
    sysc = {cat: len(system_prompt(units, subjects, cat)) for cat in ("airline", "bank")}
    out = {"central": [], "high": []}
    for st in ("recommendation", "status"):
        n_all = sum(len(v) for (k, _), v in pops.items() if k == st)
        for cat in ("airline", "bank"):
            v = sorted(pops[(st, cat)])
            n = round(100 * len(v) / n_all) if n_all else 0
            out["central"] += [(st, sysc[cat], mean(v))] * n
            out["high"] += [(st, sysc[cat], v[int(0.9 * (len(v) - 1))])] * n
    return out


def dry_run(base, items=None, records=None, units=None, subjects=None, log=print):
    base = Path(base)
    aud = base / "audit"
    aud.mkdir(parents=True, exist_ok=True)
    lines = ["v0.40 audit_ai_v0_40.py --dry-run (no network call, no provider SDK imported)",
             f"cap US${CAP_USD:.2f}; max output {MAX_OUTPUT_TOKENS} tokens; batch chunk {CHUNK}; passes {MAX_PASSES}"]
    for role, c in CODERS.items():
        lines.append(f"coder {role}: {c['name']} ({c['model_id']}, {c['provider']}, {c['mode']}), "
                     f"reasoning {json.dumps(c['reasoning_param'])}, prices {prices(c['model_id'], RUN_DATE, c['mode'] == 'batch')}")
    for cat in ("airline", "bank"):
        sp = system_prompt(units, subjects, cat)
        p = aud / f"prompt_system_{cat}_v0_40.txt"
        p.write_text(sp, encoding="utf-8")
        lines.append(f"system prompt {cat}: {len(sp)} chars, sha256 {hashlib.sha256(sp.encode()).hexdigest()} -> {p.name}")
    (aud / "prompt_user_template_v0_40.txt").write_text(USER_TEMPLATE, encoding="utf-8")
    if items:
        reqs = [(it["set"], len(request_for(it, units, subjects)["system"]), len(user_message(it["text"])))
                for it in items]
        kws = [request_kwargs(r, **request_for(it, units, subjects)) for it in items for r in CODERS]
        bad = [k for k in kws if any(f'"{w}"' in json.dumps(k) for w in ("temperature", "top_p", "top_k"))]
        lines.append(f"requests built from the drawn sample: {len(items)} answers x 3 coders = {len(kws)}; "
                     f"sampling parameters sent: {len(bad)}")
        p = projection(reqs)
        proj = {"central": p["central"], "high": p["high"]}
        basis = "the drawn sample"
    else:
        px = proxy_requests(records, units, subjects)
        proj = {"central": projection(px["central"])["central"], "high": projection(px["high"])["high"]}
        basis = "a length proxy (sample not drawn yet): population mean (central) and p90 (high) answer lengths"
    worst = sum(MAX_OUTPUT_TOKENS * prices(c["model_id"], RUN_DATE, c["mode"] == "batch")[1] / 1e6 * 200
                * (2 if c["provider"] == "google" else 1) for c in CODERS.values())
    lines.append(f"cost projection on {basis} (input chars / {O200K_CHARS_PER_TOKEN} x vendor factor "
                 f"{TOKEN_FACTOR}; output {PLAN_VISIBLE} visible + {PLAN_REASONING} reasoning tokens; T share {PLAN_TIE_SHARE}):")
    for case in ("central", "high"):
        p = proj[case]
        lines.append(f"  {case}: A ${p['per_coder']['A']:.2f}, B ${p['per_coder']['B']:.2f}, "
                     f"T ${p['per_coder']['T']:.2f}; total ${p['total']:.2f} (cap ${CAP_USD:.2f})")
    lines.append(f"  bound if every reply of all three coders on all 200 answers ran to the output cap (output only): "
                 f"${worst:.2f}; the guard stops before ${CAP_USD:.2f} in any case")
    txt = "\n".join(lines) + "\n"
    (aud / "dry_run_audit_ai_v0_40.txt").write_text(txt, encoding="utf-8")
    log(txt)
    return {"projection": proj, "text": txt}


# ----------------------------------------------------------------------------- outputs and command line
def fmt(x, nd=3):
    return "n/a" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def write_outputs(base, summ):
    aud = Path(base) / "audit"
    aud.mkdir(parents=True, exist_ok=True)
    (aud / "v40_audit_agreement.json").write_text(json.dumps(summ, indent=2, default=str), encoding="utf-8")
    L = ["# v0.40 audit: agreement of the AI-only analyst with the rule-based coder", "",
         "No human check: two AI coders from two providers, blind to the rule-based codes and to each other, with a "
         "third model from a third provider breaking ties (DEVIATIONS 2026-11-21).", "",
         f"Coders: A {summ['coders']['A']}, B {summ['coders']['B']}, tie-breaker T {summ['coders']['T']}. "
         f"Spend ${summ['spent_usd']:.2f} of the ${summ['cap_usd']:.2f} cap; complete: {summ['complete']}"
         + (f"; guard stop: {summ['guard_stopped']}" if summ["guard_stopped"] else "") + ".", "",
         f"Threshold (section 5.5): kappa >= {KAPPA_MIN:.2f} on the gone-flag. Consensus vs rule kappa = "
         f"{fmt(summ['threshold']['kappa'])}: **{'met' if summ['threshold']['met'] else 'NOT met'}**."
         + ("" if summ["threshold"]["met"] else f" {', '.join(summ['marked_tests'])} are reported as computed and "
            f"marked \"{MISS_LABEL}\", with the analyst-coded rates of the sample beside them; the coder is not changed."),
         "", "| comparison | field | n | % agreement | kappa |", "|---|---|---|---|---|"]
    for comp, fields in summ["agreement"].items():
        for f, d in fields.items():
            a = d["all"]
            L.append(f"| {comp} | {f} | {a['n']} | {fmt(a['percent_agreement'], 1)} | {fmt(a['kappa'])} |")
    L += ["", "Sample rates (rule-coded vs AI-coded, same answers): " + json.dumps(summ["sample_rates"]), ""]
    (aud / "v40_audit_agreement.md").write_text("\n".join(L), encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    for m in ("--dry-run", "--check-models", "--run", "--analyze"):
        g.add_argument(m, action="store_true")
    ap.add_argument("--base", default=str(V40))
    ap.add_argument("--raw", default=None)
    a = ap.parse_args(argv)
    base = Path(a.base)
    if a.check_models:
        ok, out = check_models()
        print(json.dumps(out, indent=2))
        return 0 if ok else 2
    vf = C.verdict_files(base)
    if vf:
        raise SystemExit(f"[audit_ai] refused: a verdict file exists ({', '.join(map(str, vf))})")
    units, subjects = load_registry()
    records = S.load_raw(a.raw or (base / "data" / "v40_raw.jsonl"))
    probes = json.loads((base / "prereg" / "probes_v0_40.json").read_text(encoding="utf-8"))["probes"]
    have_sample = (base / "audit" / "AUDIT_SAMPLE_v0_40.sha256").exists()
    if a.dry_run and not have_sample:
        dry_run(base, None, records, units, subjects)
        return 0
    sample = verify_sample(base)
    mrows = C_read_csv(base / "data" / "v40_mentions.csv")
    items, _ = build_items(sample, records, units, subjects, probes, mrows)
    if a.dry_run:
        dry_run(base, items, records, units, subjects)
        return 0
    if a.run:
        miss = [k for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY") if not os.environ.get(k)]
        if miss:
            raise SystemExit(f"[audit_ai] missing API keys: {miss}")
        ok, out = check_models()
        if not ok:
            raise SystemExit(f"[audit_ai] a coder model is not served to these keys: {out}; nothing was sent")
        au = Audit(base, items, units, subjects, batch_client=RealBatchClient())
        stopped = au.run()
    else:
        au = Audit(base, items, units, subjects)
    summ = au.summary()
    write_outputs(base, summ)
    print(f"[audit_ai] spend ${summ['spent_usd']:.2f}; gone-flag kappa {fmt(summ['threshold']['kappa'])} "
          f"(threshold {KAPPA_MIN}): {'met' if summ['threshold']['met'] else 'NOT met'}; complete {summ['complete']}")
    if au.guard.stopped:
        print(f"[audit_ai] STOPPED by the budget guard: {au.guard.stopped}")
        return EXIT_GUARD
    return 0


def C_read_csv(p):
    import csv
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


if __name__ == "__main__":
    sys.exit(main())
