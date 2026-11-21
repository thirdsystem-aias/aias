#!/usr/bin/env python3
"""
ai_check_v0_62.py -- AIAS(TM) v0.62: the independent AI translation and alias check of DEVIATIONS Entry 2
("Native checks replaced by an independent AI translation and alias check", written Sat 2026-11-21, after the lock,
before any study call). THE ENTRY IS THE SPEC; this file implements it and nothing else.

Checks (Entry 2, "Checkers" and "What each check sees"):
  C1  one call per language (ES, KO, ZH), GPT-6 Astra (gpt-6-astra): ONLY the 50 target-language items (30 Phase B
      questions, 5 Phase A templates, 15 v0.23 labels) of translations_v0_62_r2.json, item IDs renumbered at random
      (seed 20261121; ids i01..i50, items sent in the order of the new ids), instruction "Translate literally into
      English". No English source, no notes, no back-translation, no item tags (probe ids, substrates).
  C2  one call per language, GPT-6 Astra: the English source and the target item side by side (same random ids), the
      section 3.3 checklist items 1-3 in plain words and the language variety of section 3.2 step 1. Not Claude's
      back-translation, codes or notes. Reply per item: equivalence, naturalness, three checklist flags, reason.
  C3  one call per language, Gemini 4 Argon (gemini-4-argon): the English source and C1's back-translation only.
      Reply per item: equivalent / minor drift / meaning change, reason.
  C4  one call each for Korean and Chinese, GPT-6 Astra: every alias of every row with status UNCONFIRMED or PARTLY in
      brand_aliases_v0_62_r2.csv (KO 88 rows / 94 aliases; ZH 44 rows / 48 aliases): registry name, category, alias;
      not the check source or status. Reply per alias: usage code, common word, reason.
Frozen texts: osf/v62/ai_check/ (c1..c4_instruction.txt, c1..c4_schema.json, check_params.json); their SHA-256 are in
FROZEN below and every mode refuses if a file differs. The schemas' enums are the codes the parser accepts.

Settings (Entry 2): the repo's API helpers acquire_v0_62.call_openai_current and call_google_current, called
unchanged with search off and no system prompt: provider defaults (no temperature, top_p or reasoning effort sent), no
tools, standard API, the helpers' maximum output of 16,384 tokens. One request per call; a failed request or an
unparseable reply is re-sent ONCE (MAX_ATTEMPTS = 2 per call, counted across invocations; the helpers' own retry
loop _call_with_retry is not used).
Reply extraction (fixed now, CLAUDE.md "LLM judges and strict JSON"): the reply counts if it contains a complete JSON
object (the first one, scanning left to right, that passes the check's validation) with exactly one entry for every
id sent and no other id, every code from the schema's enum (compared after strip() and lower()), every flag a JSON
boolean; text around the object is ignored. Otherwise the reply is unparseable.

Budget (Entry 2, "Cost and cap"; approved by the pre-registrant 2026-11-21 ~9:30 am CT): hard cap US$8 on recorded
usage, outside the locked acquisition guard (budget_v0_62 is not changed and this spend is not in it). Before every
request its worst case is reserved: input = UTF-8 bytes of the prompt + 512 tokens (a token covers at least one byte)
at the higher of the model's dated prices, output = 16,384 tokens (OpenAI; reasoning included) or 2 x 16,384
(Google: output + thinking, counted twice for safety) at the higher price; the request is not sent if recorded spend +
worst case > $8 (the run stops). Recorded cost = budget_v0_62.part_cost on the reply's usage at the price of its date
(Google thinking tokens billed as output); a request with no usage recorded (an exception) is charged its worst case.

Guards for --run: refused on or after 2026-11-29 00:00 US Central; refused if any study answer file exists
(osf/v62/data/v62_raw.jsonl, v62_batches.jsonl, data/coded/, v62_verdicts.json); refused if a frozen file differs;
refused unless DEVIATIONS.md Entry 2 names this file's SHA-256 (the dated addendum Entry 2 requires before the first
check call); refused unless --check-models recorded both models on the same US Central date; refused while another
paid run is in progress on this machine (an acquisition with --collect, a judge script, another ai_check --run).

Modes:
  --dry-run (default)  build every prompt, print the plan, the guards and the cost estimate; NO SDK import, no network
  --check-models       free metadata lookup of gpt-6-astra (OpenAI models.retrieve) and gemini-4-argon (Google
                       models.get); written to osf/v62/ai_check/results/model_check_<UTC>.json
  --run                the paid check (guarded); append-only raw file osf/v62/ai_check/results/ai_check_raw_v0_62.jsonl
  --analyze            agreement %, Cohen's kappa and linear-weighted kappa per pair (Claude r2 / C2 / C3), flagged
                       and strictly flagged lists, decision rule (e), C2 naturalness and checklist counts, C4 counts;
                       writes results/ai_check_analysis_v0_62.json and the inputs of S-Trans and S-AliasAI
                       (results/s_trans_flags_v0_62.json, results/s_alias_ai_off_v0_62.json; score_ai_sens_v0_62.py)

Paths: ROOT = AIAS_ROOT or the worktree that contains this file.
"""
import argparse
import csv
import hashlib
import json
import os
import random
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from string import Template
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve()
ROOT = Path(os.environ.get("AIAS_ROOT", str(HERE.parents[3]))).resolve()
sys.path.insert(0, str(HERE.parent))
import budget_v0_62 as BG  # noqa: E402  (no SDK import)

V62 = ROOT / "osf" / "v62"
FROZEN_DIR = V62 / "ai_check"
RESULTS = FROZEN_DIR / "results"
RAW_PATH = RESULTS / "ai_check_raw_v0_62.jsonl"
TRANSLATIONS = V62 / "translations" / "translations_v0_62_r2.json"
PROBE_FILES = {lg: V62 / "translations" / f"probes_{lg}_v0_62_r2.jsonl" for lg in ("es", "ko", "zh")}
ENGLISH_PROBES = V62 / "inputs" / "probes_v0_42.jsonl"
ALIAS_TABLE = V62 / "translations" / "brand_aliases_v0_62_r2.csv"
DEVIATIONS = V62 / "DEVIATIONS.md"
STUDY_ANSWER_PATHS = [V62 / "data" / "v62_raw.jsonl", V62 / "data" / "v62_batches.jsonl", V62 / "data" / "coded",
                      V62 / "v62_verdicts.json"]

FROZEN = {
    "c1_instruction.txt": "03b5c2828e81a518bff87fe092ce37f248c4407d539e1bb1e500526b3267f159",
    "c2_instruction.txt": "0dea6df1f3a03833eca35e630a80cf0b5bc622e1c0d013e2d926f8a1bfd0f9b6",
    "c3_instruction.txt": "98b673f59b8a029f1879e4cf6a2f99cd8387dd16b558519f161cc21ed02cca87",
    "c4_instruction.txt": "938e39ea4acc137259307f19c94026839f66e38719a5c174a2412b6b28bc34a7",
    "c1_schema.json": "5cffb945c35bbd4b8db9b2f1553d38f8b880691a8dc13d0e0539dad153cd940a",
    "c2_schema.json": "9889b5380de4cb2c0b8fda34c7ab9d6ac796985929ae1a744688003d49189591",
    "c3_schema.json": "77fffc84618b74322e77623dfc741b0692b9de0718d22a33ca4d5fd83af676c9",
    "c4_schema.json": "4a9db7985fab3b7061fe528557761d21c9fcea5ec276537654b45678d75c791e",
    "check_params.json": "6467489b542537df03014044f465993b0644451fda73eb196e853967df9808cb",
}

LANGS = ("es", "ko", "zh")
CHECKS = ("C1", "C2", "C3", "C4")
MAX_ATTEMPTS = 2                       # one send + one re-send
OUTPUT_CAP = 16384                     # = acquire_v0_62.CURRENT_MAX_TOKENS (checked by the tests)
INPUT_OVERHEAD_TOKENS = 512
CENTRAL = ZoneInfo("America/Chicago")
LAST_DAY_END = datetime(2026, 11, 29, 0, 0, tzinfo=CENTRAL)      # refuse at or after (collection window starts)
EQ_CODES = ("equivalent", "minor drift", "meaning change")       # ordered (weighted kappa)
# Entry 2 "Cost and cap": token figures per call (input, output central, output high)
ENTRY2_TOKENS = {"C1": (4500, 6000, 13000), "C2": (8000, 8000, 15000), "C3": (8000, 3000, 10000),
                 "C4": (4000, 6000, 14000)}


class Refused(RuntimeError):
    pass


# ============================================================================ frozen files
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frozen_problems(d=None):
    d = Path(d or FROZEN_DIR)
    bad = []
    for name, sha in FROZEN.items():
        p = d / name
        if not p.exists():
            bad.append(f"{name}: missing")
        elif sha256_file(p) != sha:
            bad.append(f"{name}: SHA-256 {sha256_file(p)} != frozen {sha}")
    return bad


def frozen_text(name):
    return (FROZEN_DIR / name).read_text(encoding="utf-8")


def params():
    return json.loads(frozen_text("check_params.json"))


def schema_enum(check, field):
    s = json.loads(frozen_text(f"{check.lower()}_schema.json"))
    key = "aliases" if check == "C4" else "items"
    return tuple(s["properties"][key]["items"]["properties"][field]["enum"])


# ============================================================================ items (what is checked)
def load_translations(path=None):
    return json.loads(Path(path or TRANSLATIONS).read_text(encoding="utf-8"))


def phase_b_key(substrate, probe_id):
    """Phase B item key 'v20|q1' (probe ids repeat across substrates: v0.20-v0.23 use q1..q6)."""
    return f"{substrate}|{probe_id}"


def items(lang, tr=None):
    """The 50 items of a language, in file order: 30 Phase B questions, 5 templates, 15 v0.23 labels.
    claude = Claude's r2 code (none for the labels: the r2 review codes the 30 + 5 items only)."""
    tr = tr or load_translations()
    out = []
    for x in tr["phase_b"]:
        out.append({"key": phase_b_key(x["substrate"], x["probe_id"]), "kind": "phase_b", "substrate": x["substrate"],
                    "probe_id": x["probe_id"], "en": x["en"], "target": x[lang], "claude": x.get(lang + "_drift")})
    for sub, t in tr["phase_a_templates"].items():
        out.append({"key": f"template__{sub}", "kind": "template", "substrate": sub, "en": t["en"],
                    "target": t[lang], "claude": t.get(lang + "_drift")})
    for lab, t in tr["v23_categories"].items():
        out.append({"key": f"label__{lab}", "kind": "label", "substrate": "v23", "en": lab, "target": t[lang],
                    "claude": None})
    return out


def blind_ids(tr=None, seed=None):
    """{lang: {item key: 'iNN'}}: one random.Random(seed) generator, a shuffle per language in LANGS order."""
    rng = random.Random(params()["seed"] if seed is None else seed)
    out = {}
    for lg in LANGS:
        its = items(lg, tr)
        perm = list(range(1, len(its) + 1))
        rng.shuffle(perm)
        out[lg] = {x["key"]: f"i{n:02d}" for x, n in zip(its, perm)}
    return out


def consistency_problems(tr=None):
    """The checked items are the locked stimuli: Phase B text = probe file prompt; templates filled with the brand (and
    a label for v0.23) = probe file prompt; English = probes_v0_42.jsonl."""
    tr = tr or load_translations()
    bad = []
    en = {}
    for line in ENGLISH_PROBES.read_text(encoding="utf-8").splitlines():
        if line.strip():
            d = json.loads(line)
            en[(d["substrate"], d["phase"], d["probe_id"])] = d
    for x in tr["phase_b"]:
        if en.get((x["substrate"], "B", x["probe_id"]), {}).get("prompt") != x["en"]:
            bad.append(f"EN {x['substrate']} {x['probe_id']}: source differs from probes_v0_42.jsonl")
    for lg in LANGS:
        pb = {(x["substrate"], x["probe_id"]): x[lg] for x in tr["phase_b"]}
        n_b = 0
        labels = [t[lg] for t in tr["v23_categories"].values()]
        for line in PROBE_FILES[lg].read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            if d["phase"] == "B":
                n_b += 1
                if pb.get((d["substrate"], d["probe_id"])) != d["prompt"]:
                    bad.append(f"{lg} {d['substrate']} {d['probe_id']}: probe text differs from translations json")
            else:
                t = tr["phase_a_templates"][d["substrate"]][lg].replace("{BRAND}", d["brand_name"])
                if d["substrate"] == "v23":
                    if not any(t.replace("{CATEGORY}", lab) == d["prompt"] for lab in labels):
                        bad.append(f"{lg} {d['probe_id']}: v23 template + label != probe text")
                elif t != d["prompt"]:
                    bad.append(f"{lg} {d['probe_id']}: template + brand != probe text")
        if n_b != len(pb):
            bad.append(f"{lg}: {n_b} Phase B probes in the probe file, {len(pb)} in the translations json")
    if len({x["key"] for x in items("es", tr)}) != len(items("es", tr)):
        bad.append("item keys are not unique")
    return bad


def alias_rows(lang, path=None):
    """C4 rows: every alias of every UNCONFIRMED / PARTLY row (table order), with ids a001...; status kept for the
    analysis only (never sent)."""
    statuses = set(params()["alias_statuses_checked"])
    out = []
    with open(path or ALIAS_TABLE, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r[lang + "_check_status"] not in statuses:
                continue
            for a in filter(None, (x.strip() for x in r[lang + "_aliases"].split("|"))):
                out.append({"id": f"a{len(out) + 1:03d}", "substrate": r["substrate"], "brand": r["brand"],
                            "alias": a, "status": r[lang + "_check_status"]})
    return out


# ============================================================================ prompts
def render(check, **kw):
    return Template(frozen_text(f"{check.lower()}_instruction.txt")).substitute(**kw)


def _dumps(rows):
    return json.dumps(rows, ensure_ascii=False, indent=1)


def c1_prompt(lang, tr=None):
    ids = blind_ids(tr)[lang]
    rows = sorted(({"id": ids[x["key"]], "text": x["target"]} for x in items(lang, tr)), key=lambda r: r["id"])
    return render("C1", ITEMS=_dumps(rows))


def c2_prompt(lang, tr=None):
    ids = blind_ids(tr)[lang]
    rows = sorted(({"id": ids[x["key"]], "english": x["en"], "translation": x["target"]} for x in items(lang, tr)),
                  key=lambda r: r["id"])
    return render("C2", VARIETY=params()["variety"][lang], ITEMS=_dumps(rows))


def c3_prompt(lang, back, tr=None):
    """back: {blind id: English back-translation} from C1's parsed reply."""
    ids = blind_ids(tr)[lang]
    rows = sorted(({"id": ids[x["key"]], "source": x["en"], "back_translation": back[ids[x["key"]]]}
                   for x in items(lang, tr)), key=lambda r: r["id"])
    return render("C3", ITEMS=_dumps(rows))


def c4_prompt(lang, path=None):
    cat = params()["category"]
    rows = [{"id": r["id"], "brand": r["brand"], "category": cat[r["substrate"]], "alias": r["alias"]}
            for r in alias_rows(lang, path)]
    return render("C4", LANGUAGE=params()["alias_language"][lang], ITEMS=_dumps(rows))


def expected_ids(check, lang, tr=None):
    if check == "C4":
        return {r["id"] for r in alias_rows(lang)}
    return set(blind_ids(tr)[lang].values())


def plan():
    """Call order: per language C1, C3 (needs C1), C2; then C4 KO, ZH."""
    langs = params()["languages"]
    out = []
    for lg in LANGS:
        for c in ("C1", "C3", "C2"):
            if lg in langs[c]:
                out.append((c, lg))
    out += [("C4", lg) for lg in langs["C4"]]
    return out


def model_of(check):
    return params()["models"][check]


# ============================================================================ reply extraction
def _norm(v):
    return v.strip().lower() if isinstance(v, str) else v


def validate(check, obj, ids):
    """None if obj is a complete reply for the ids sent, else the reason."""
    key = "aliases" if check == "C4" else "items"
    rows = obj.get(key) if isinstance(obj, dict) else None
    if not isinstance(rows, list):
        return f"no '{key}' list"
    seen = []
    for r in rows:
        if not isinstance(r, dict) or not isinstance(r.get("id"), str):
            return "entry without a string id"
        seen.append(r["id"].strip())
        if check == "C1":
            if not isinstance(r.get("english"), str) or not r["english"].strip():
                return f"{r['id']}: no english"
        elif check == "C2":
            if _norm(r.get("equivalence")) not in schema_enum("C2", "equivalence"):
                return f"{r['id']}: equivalence {r.get('equivalence')!r}"
            if _norm(r.get("naturalness")) not in schema_enum("C2", "naturalness"):
                return f"{r['id']}: naturalness {r.get('naturalness')!r}"
            for fl in ("category_scope", "speech_act_format", "added_or_removed"):
                if not isinstance(r.get(fl), bool):
                    return f"{r['id']}: {fl} not boolean"
            if not isinstance(r.get("reason"), str):
                return f"{r['id']}: no reason"
        elif check == "C3":
            if _norm(r.get("code")) not in schema_enum("C3", "code"):
                return f"{r['id']}: code {r.get('code')!r}"
            if not isinstance(r.get("reason"), str):
                return f"{r['id']}: no reason"
        elif check == "C4":
            if _norm(r.get("usage")) not in schema_enum("C4", "usage"):
                return f"{r['id']}: usage {r.get('usage')!r}"
            if not isinstance(r.get("common_word"), bool):
                return f"{r['id']}: common_word not boolean"
            if not isinstance(r.get("reason"), str):
                return f"{r['id']}: no reason"
    if len(seen) != len(set(seen)):
        return "duplicate ids"
    if set(seen) != set(ids):
        missing, extra = sorted(set(ids) - set(seen)), sorted(set(seen) - set(ids))
        return f"ids differ (missing {missing[:5]}{'...' if len(missing) > 5 else ''}, extra {extra[:5]})"
    return None


def extract(check, text, ids):
    """-> (object, None) or (None, reason). The first complete JSON object that validates; surrounding text ignored."""
    t = text or ""
    dec = json.JSONDecoder()
    first_reason = None
    for i, ch in enumerate(t):
        if ch != "{":
            continue
        try:
            obj, _end = dec.raw_decode(t, i)
        except ValueError:
            continue
        why = validate(check, obj, ids)
        if why is None:
            return obj, None
        first_reason = first_reason or why
    return None, first_reason or "no JSON object"


def entries(check, obj):
    """{id: entry with codes normalised}."""
    key = "aliases" if check == "C4" else "items"
    out = {}
    for r in obj[key]:
        e = {k: _norm(v) if k in ("equivalence", "naturalness", "code", "usage") else v for k, v in r.items()}
        out[r["id"].strip()] = e
    return out


# ============================================================================ budget
def cap_usd():
    return float(params()["cap_usd"])


def max_prices(model):
    """The higher of the model's dated prices (input, output), USD per 1M tokens (Gemini: the December price)."""
    tabs = [BG.prices(model, "standard", "2026-11-21")] + \
        [BG.prices(model, "standard", first) for m, first, _ in BG.PRICE_CHANGES if m == model]
    return max(p[0] for p in tabs), max(p[1] for p in tabs)


def worst_case(model, prompt):
    pin, pout = max_prices(model)
    tin = len(prompt.encode("utf-8")) + INPUT_OVERHEAD_TOKENS
    tout = OUTPUT_CAP * (2 if BG.PROVIDER[model] == "google" else 1)
    return (tin * pin + tout * pout) / 1e6


def recorded_cost(model, out, when_utc):
    """Cost from the reply's recorded usage (budget_v0_62.part_cost; Google thinking billed as output)."""
    part = {"mode": "standard", "input_tokens": out.get("tokens_in") or 0, "output_tokens": out.get("tokens_out") or 0,
            "thinking_tokens": out.get("tokens_thought") or 0, "n_searches": 0}
    return BG.part_cost(model, part, when_utc)


def read_raw(path=None):
    p = Path(path or RAW_PATH)
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def spent(lines):
    return sum(float(x.get("cost_usd") or 0.0) for x in lines)


def _append(path, rec):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


# ============================================================================ sending (repo helpers)
def helper_sender(model, prompt):
    """One request through the repo's helper, unchanged: search off, no system prompt, provider defaults.
    -> helper output dict; raises on failure. The SDK is imported inside the helper (never in --dry-run)."""
    import acquire_v0_62 as A
    fn = {"openai": A.call_openai_current, "google": A.call_google_current}[BG.PROVIDER[model]]
    return fn(model, prompt, False)


def send_once(check, lang, model, prompt, attempt, reserved, sender, ids):
    t0 = datetime.now(timezone.utc).isoformat()
    out, err = None, None
    try:
        out = sender(model, prompt)
    except Exception as e:                                       # noqa: BLE001 - recorded, re-sent once
        err = f"{type(e).__name__}: {e}"[:500]
    t1 = datetime.now(timezone.utc).isoformat()
    rec = {"call_key": f"{check}|{lang}", "check": check, "language": lang, "model_requested": model,
           "attempt": attempt, "started_utc": t0, "finished_utc": t1,
           "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(), "prompt": prompt,
           "worst_case_reserved_usd": round(reserved, 6), "error": err}
    if out is None or (out.get("tokens_in") is None and out.get("tokens_out") is None):
        rec.update({"text": (out or {}).get("text"), "cost_usd": reserved, "cost_basis": "worst_case (no usage)"})
    else:
        rec.update({k: out.get(k) for k in ("text", "served_model", "finish_reason", "tokens_in", "tokens_out",
                                            "tokens_thought")})
        rec.update({"cost_usd": recorded_cost(model, out, t0), "cost_basis": "usage"})
    obj, why = (None, err or "no reply") if out is None else extract(check, out.get("text"), ids)
    rec["parse_ok"], rec["parse_error"] = obj is not None, why
    return rec


def parsed(lines):
    """{call_key: entries} from the last parsed reply of each call."""
    out = {}
    for x in lines:
        if x.get("parse_ok"):
            obj, _ = extract(x["check"], x["text"], expected_ids(x["check"], x["language"]))
            out[x["call_key"]] = entries(x["check"], obj)
    return out


def build_prompt(check, lang, lines):
    if check == "C1":
        return c1_prompt(lang)
    if check == "C2":
        return c2_prompt(lang)
    if check == "C4":
        return c4_prompt(lang)
    c1 = parsed(lines).get(f"C1|{lang}")
    if c1 is None:
        return None
    return c3_prompt(lang, {i: e["english"] for i, e in c1.items()})


def run_checks(raw_path=None, sender=None, log=print):
    """Every call of plan() not yet answered, at most MAX_ATTEMPTS requests per call (across invocations); worst case
    reserved before each request against the $8 cap on recorded spend. -> 'done' | 'stop' | 'incomplete'."""
    raw_path = Path(raw_path or RAW_PATH)
    sender = sender or helper_sender
    lines = read_raw(raw_path)
    cap = cap_usd()
    incomplete = False
    for check, lg in plan():
        key = f"{check}|{lg}"
        prev = [x for x in lines if x["call_key"] == key]
        if any(x.get("parse_ok") for x in prev):
            continue
        model = model_of(check)
        prompt = build_prompt(check, lg, lines)
        if prompt is None:
            log(f"  {key}: not sent (C1|{lg} has no parsed reply)")
            incomplete = True
            continue
        ids = expected_ids(check, lg)
        attempt = len(prev)
        while attempt < MAX_ATTEMPTS:
            wc = worst_case(model, prompt)
            if spent(lines) + wc > cap:
                log(f"STOP before {key} attempt {attempt + 1}: recorded ${spent(lines):.4f} + worst case ${wc:.4f} "
                    f"> cap ${cap:.2f}")
                return "stop"
            attempt += 1
            rec = send_once(check, lg, model, prompt, attempt, wc, sender, ids)
            _append(raw_path, rec)
            lines.append(rec)
            log(f"  {key} attempt {attempt}: parse_ok={rec['parse_ok']} cost ${rec['cost_usd']:.4f} "
                f"({rec['cost_basis']}); total ${spent(lines):.4f}" + ("" if rec["parse_ok"] else
                                                                     f"; {rec['parse_error']}"))
            if rec["parse_ok"]:
                break
        else:
            if not any(x.get("parse_ok") for x in lines if x["call_key"] == key):
                log(f"  {key}: no parsed reply after {MAX_ATTEMPTS} attempts (not re-sent again)")
                incomplete = True
    return "incomplete" if incomplete else "done"


# ============================================================================ guards
def date_check(now=None):
    now = now or datetime.now(timezone.utc)
    if now >= LAST_DAY_END:
        return False, f"on or after {LAST_DAY_END.isoformat()} (the check ends before the collection window)"
    return True, f"before {LAST_DAY_END.isoformat()}"


def answer_files(paths=None):
    return [str(p) for p in (paths or STUDY_ANSWER_PATHS) if Path(p).exists()]


def entry2_body(path=None):
    text = Path(path or DEVIATIONS).read_text(encoding="utf-8")
    m = re.search(r"(?ms)^## Entry 2\b.*?(?=^## Entry \d|\Z)", text)
    return m.group(0) if m else ""


def addendum_names_script(path=None):
    return sha256_file(HERE) in entry2_body(path)


PAID_RE = re.compile(r"(?:(?:acquire|acquisition)[\w.-]*\.py.*--collect|run_acquisition_v\d+\.py|"
                     r"judge[\w.-]*\.py|ai_check[\w.-]*\.py.*--run)")


def _ps():
    return subprocess.run(["ps", "-axo", "pid=,ppid=,command="], capture_output=True, text=True, timeout=30).stdout


def other_paid_runs(ps_text=None, me=None):
    """Processes other than this one and its ancestors that run a paid collection, a judge or another check."""
    ps_text = _ps() if ps_text is None else ps_text
    me = os.getpid() if me is None else me
    procs = {}
    for line in ps_text.splitlines():
        f = line.strip().split(None, 2)
        if len(f) == 3 and f[0].isdigit() and f[1].isdigit():
            procs[int(f[0])] = (int(f[1]), f[2])
    anc, p = {me}, me
    while p in procs and procs[p][0] not in anc and procs[p][0] > 1:
        p = procs[p][0]
        anc.add(p)
    return [(pid, cmd) for pid, (_pp, cmd) in procs.items()
            if pid not in anc and PAID_RE.search(cmd) and "--dry-run" not in cmd]


def model_check_today(now=None, d=None):
    now = now or datetime.now(timezone.utc)
    day = now.astimezone(CENTRAL).date().isoformat()
    for p in sorted(Path(d or RESULTS).glob("model_check_*.json")):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if r.get("central_date") == day and all(m.get("found") for m in r.get("models", {}).values()) \
                and set(r.get("models", {})) >= {"gpt-6-astra", "gemini-4-argon"}:
            return str(p)
    return None


def run_guards(now=None):
    """-> list of refusal reasons (empty = may run)."""
    bad = []
    ok, why = date_check(now)
    if not ok:
        bad.append(why)
    a = answer_files()
    if a:
        bad.append(f"study answer file(s) exist: {a}")
    bad += [f"frozen file {x}" for x in frozen_problems()]
    if not addendum_names_script():
        bad.append(f"DEVIATIONS.md Entry 2 does not name this script's SHA-256 ({sha256_file(HERE)})")
    if not model_check_today(now):
        bad.append("no --check-models record with both models found today (US Central)")
    o = other_paid_runs()
    if o:
        bad.append("another paid run is in progress: " + "; ".join(f"{p} {c[:100]}" for p, c in o))
    return bad


def require_keys():
    if not os.environ.get("GOOGLE_API_KEY") and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
    missing = [v for v in ("OPENAI_API_KEY", "GOOGLE_API_KEY") if not os.environ.get(v)]
    if missing:
        raise Refused(f"missing environment variables: {', '.join(missing)}")


# ============================================================================ --check-models (free)
def check_models(out_dir=None):
    require_keys()
    import openai
    from google import genai
    now = datetime.now(timezone.utc)
    rec = {"utc": now.isoformat(), "central_date": now.astimezone(CENTRAL).date().isoformat(), "models": {}}
    try:
        m = openai.OpenAI().models.retrieve("gpt-6-astra")
        rec["models"]["gpt-6-astra"] = {"found": getattr(m, "id", None) == "gpt-6-astra", "id": getattr(m, "id", None),
                                        "created": getattr(m, "created", None), "owned_by": getattr(m, "owned_by", None)}
    except Exception as e:                                       # noqa: BLE001
        rec["models"]["gpt-6-astra"] = {"found": False, "error": f"{type(e).__name__}: {e}"[:300]}
    try:
        gc = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])   # held: an inline client is closed before the call
        g = gc.models.get(model="gemini-4-argon")
        name = getattr(g, "name", "") or ""
        rec["models"]["gemini-4-argon"] = {"found": name.endswith("gemini-4-argon"), "name": name,
                                           "display_name": getattr(g, "display_name", None),
                                           "version": getattr(g, "version", None),
                                           "input_token_limit": getattr(g, "input_token_limit", None),
                                           "output_token_limit": getattr(g, "output_token_limit", None)}
    except Exception as e:                                       # noqa: BLE001
        rec["models"]["gemini-4-argon"] = {"found": False, "error": f"{type(e).__name__}: {e}"[:300]}
    d = Path(out_dir or RESULTS)
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"model_check_{now.strftime('%Y%m%dT%H%M%SZ')}.json"
    p.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    return p, rec


# ============================================================================ --dry-run
def entry2_estimate(when="2026-12-01"):
    """Entry 2's central and high figures (Gemini at the December price, as the entry states)."""
    n = {c: len(params()["languages"][c]) for c in CHECKS}
    cen = high = 0.0
    for c in CHECKS:
        pin, pout = BG.prices(model_of(c), "standard", when)
        tin, oc, oh = ENTRY2_TOKENS[c]
        cen += n[c] * (tin * pin + oc * pout) / 1e6
        high += n[c] * (tin * pin + oh * pout) / 1e6
    return cen, high


def dry_run(out=print, now=None):
    out(f"AIAS v0.62 AI check (DEVIATIONS Entry 2): DRY RUN (nothing is sent; no SDK imported). ROOT = {ROOT}")
    fp = frozen_problems()
    out(f"frozen files ({FROZEN_DIR}): {'OK, ' + str(len(FROZEN)) + ' files match' if not fp else fp}")
    cp = consistency_problems()
    out(f"items = locked stimuli: {'OK' if not cp else cp[:5]}")
    for lg in LANGS:
        c = Counter(x["kind"] for x in items(lg))
        out(f"  {lg}: {len(items(lg))} items ({dict(c)}); Claude r2 codes on "
            f"{sum(1 for x in items(lg) if x['claude'])}")
    for lg in params()["languages"]["C4"]:
        rows = alias_rows(lg)
        out(f"  C4 {lg}: {len({(r['substrate'], r['brand']) for r in rows})} rows, {len(rows)} aliases "
            f"({dict(Counter(r['status'] for r in rows))})")
    total_wc = 0.0
    out(f"{'call':8s} {'model':15s} {'prompt bytes':>12s} {'worst case $':>13s}")
    for check, lg in plan():
        model = model_of(check)
        if check == "C3":                                       # C1's reply is unknown: English back stand-in
            ids = blind_ids()[lg]
            prompt = c3_prompt(lg, {ids[x["key"]]: x["en"] * 2 for x in items(lg)})   # bound: twice the source
        else:
            prompt = build_prompt(check, lg, [])
        wc = worst_case(model, prompt)
        total_wc += wc
        out(f"{check}|{lg:4s} {model:15s} {len(prompt.encode('utf-8')):12d} {wc:13.4f}")
    cen, high = entry2_estimate()
    out(f"cost estimate (Entry 2 token figures; Gemini at the December price): central ${cen:.2f}, high ${high:.2f}")
    out(f"worst case if every call ran to its output cap once: ${total_wc:.2f} (twice, with every re-send: "
        f"${2 * total_wc:.2f}); hard cap ${cap_usd():.2f} on recorded usage, worst case reserved before each request")
    ok, why = date_check(now)
    out(f"guard date: {'ok' if ok else 'REFUSE'} ({why})")
    a = answer_files()
    out(f"guard study answer files: {'none' if not a else 'REFUSE ' + str(a)}")
    out(f"guard DEVIATIONS Entry 2 names this script (SHA-256 {sha256_file(HERE)}): "
        f"{'yes' if addendum_names_script() else 'NO (--run refused until the dated addendum is committed)'}")
    out(f"guard model check today: {model_check_today(now) or 'none (--run refused until --check-models)'}")
    o = other_paid_runs()
    out(f"guard other paid runs: {'none' if not o else o}")
    raw = read_raw()
    out(f"raw file: {RAW_PATH} ({len(raw)} lines, recorded ${spent(raw):.4f})")
    return 0 if not fp and not cp else 2


# ============================================================================ --analyze
def kappa(a, b, cats=EQ_CODES, weighted=False):
    """Cohen's kappa of two code lists over the ordered categories `cats`; weighted=True uses linear agreement
    weights w_ij = 1 - |i - j| / (k - 1). None if no pairs or if chance agreement is 1 (undefined)."""
    n = len(a)
    if n == 0 or n != len(b):
        return None
    k = len(cats)
    ix = {c: i for i, c in enumerate(cats)}
    o = [[0.0] * k for _ in range(k)]
    for x, y in zip(a, b):
        o[ix[x]][ix[y]] += 1.0 / n
    ra = [sum(o[i]) for i in range(k)]
    cb = [sum(o[i][j] for i in range(k)) for j in range(k)]

    def w(i, j):
        return 1.0 - abs(i - j) / (k - 1) if weighted else float(i == j)
    po = sum(w(i, j) * o[i][j] for i in range(k) for j in range(k))
    pe = sum(w(i, j) * ra[i] * cb[j] for i in range(k) for j in range(k))
    if abs(1.0 - pe) < 1e-12:
        return None
    return (po - pe) / (1.0 - pe)


def agreement(a, b):
    n = len(a)
    return {"n": n, "agreement_pct": (100.0 * sum(x == y for x, y in zip(a, b)) / n) if n else None,
            "kappa": kappa(a, b), "kappa_linear_weighted": kappa(a, b, weighted=True)}


def analyze_language(lang, c2, c3, tr=None):
    """c2, c3: {blind id: entry} or None (no parsed reply)."""
    ids = blind_ids(tr)[lang]
    rows = []
    for x in items(lang, tr):
        i = ids[x["key"]]
        e2 = (c2 or {}).get(i)
        e3 = (c3 or {}).get(i)
        rows.append({"key": x["key"], "kind": x["kind"], "id": i, "claude": x["claude"],
                     "c2": e2["equivalence"] if e2 else None, "c3": e3["code"] if e3 else None,
                     "c2_entry": e2, "c3_reason": e3["reason"] if e3 else None})
    pairs = {}
    for p, q in (("claude", "c2"), ("claude", "c3"), ("c2", "c3")):
        both = [r for r in rows if r[p] is not None and r[q] is not None]
        pairs[f"{p}_vs_{q}"] = agreement([r[p] for r in both], [r[q] for r in both])
    mc = "meaning change"
    flagged = [r for r in rows if mc in (r["c2"], r["c3"])]
    strict = [r for r in rows if r["c2"] == mc and r["c3"] == mc]

    def keys(rs, kind=None):
        return [r["key"] for r in rs if kind is None or r["kind"] == kind]
    out = {"n_items": len(rows), "c2_available": c2 is not None, "c3_available": c3 is not None,
           "claude_codes": sum(1 for r in rows if r["claude"]), "pairs": pairs,
           "flagged": keys(flagged), "strictly_flagged": keys(strict),
           "phase_b_flagged": keys(flagged, "phase_b"), "phase_b_strictly_flagged": keys(strict, "phase_b"),
           "templates_flagged": keys(flagged, "template"), "labels_flagged": keys(flagged, "label")}
    out["rule_e_decision"] = len(out["phase_b_strictly_flagged"]) > 6
    if out["templates_flagged"]:
        out["template_note"] = ("flagged Phase A template(s): this language's block-4 recognition descriptive goes "
                                "into a 'translation flagged' footnote (Entry 2 (b))")
    if c2 is not None:
        out["c2_naturalness"] = dict(Counter(r["c2_entry"]["naturalness"] for r in rows if r["c2_entry"]))
        fl = ("category_scope", "speech_act_format", "added_or_removed")
        out["c2_checklist_counts"] = {f: sum(1 for r in rows if r["c2_entry"] and r["c2_entry"][f] is True) for f in fl}
        out["c2_checklist_flags"] = [{"key": r["key"], "flag": f, "reason": r["c2_entry"]["reason"]}
                                     for r in rows if r["c2_entry"] for f in fl if r["c2_entry"][f] is True]
    out["items"] = [{k: r[k] for k in ("key", "kind", "id", "claude", "c2", "c3")} for r in rows]
    return out


def analyze_aliases(lang, c4, path=None):
    rows = alias_rows(lang, path)
    if c4 is None:
        return {"available": False, "n_aliases": len(rows)}
    usage = Counter(c4[r["id"]]["usage"] for r in rows)
    off = [[r["substrate"], r["brand"], r["alias"]] for r in rows if c4[r["id"]]["usage"] == "not used for this brand"]
    return {"available": True, "n_rows": len({(r["substrate"], r["brand"]) for r in rows}), "n_aliases": len(rows),
            "usage_counts": dict(usage), "common_word_count": sum(1 for r in rows if c4[r["id"]]["common_word"]),
            "share_not_used": len(off) / len(rows) if rows else None, "not_used_for_this_brand": off,
            "by_status": {s: dict(Counter(c4[r["id"]]["usage"] for r in rows if r["status"] == s))
                          for s in sorted({r["status"] for r in rows})},
            "aliases": [{"substrate": r["substrate"], "brand": r["brand"], "alias": r["alias"],
                         "usage": c4[r["id"]]["usage"], "common_word": c4[r["id"]]["common_word"],
                         "reason": c4[r["id"]]["reason"]} for r in rows]}


def analyze(lines, tr=None):
    P_ = parsed(lines)
    res = {"spec": "osf/v62/DEVIATIONS.md Entry 2", "script_sha256": sha256_file(HERE),
           "recorded_spend_usd": round(spent(lines), 6), "cap_usd": cap_usd(), "n_requests": len(lines),
           "calls_parsed": sorted(P_), "languages": {}, "aliases": {}}
    for lg in LANGS:
        res["languages"][lg] = analyze_language(lg, P_.get(f"C2|{lg}"), P_.get(f"C3|{lg}"), tr)
    for lg in params()["languages"]["C4"]:
        res["aliases"][lg] = analyze_aliases(lg, P_.get(f"C4|{lg}"))
    s_trans = {lg: {"flagged": res["languages"][lg]["phase_b_flagged"],
                    "strictly_flagged": res["languages"][lg]["phase_b_strictly_flagged"],
                    "complete": res["languages"][lg]["c2_available"] and res["languages"][lg]["c3_available"]}
               for lg in LANGS}
    s_alias = {lg: {"off": res["aliases"][lg].get("not_used_for_this_brand", []),
                    "complete": res["aliases"][lg]["available"]} for lg in res["aliases"]}
    return res, s_trans, s_alias


def write_analysis(lines, d=None):
    d = Path(d or RESULTS)
    d.mkdir(parents=True, exist_ok=True)
    res, s_trans, s_alias = analyze(lines)
    (d / "ai_check_analysis_v0_62.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    (d / "s_trans_flags_v0_62.json").write_text(json.dumps(s_trans, indent=1, ensure_ascii=False), encoding="utf-8")
    (d / "s_alias_ai_off_v0_62.json").write_text(json.dumps(s_alias, indent=1, ensure_ascii=False), encoding="utf-8")
    return res, s_trans, s_alias


def summary_lines(res):
    out = [f"recorded spend ${res['recorded_spend_usd']:.4f} of ${res['cap_usd']:.2f}; calls parsed: {res['calls_parsed']}"]
    for lg, r in res["languages"].items():
        pr = "; ".join(f"{k}: n={v['n']} agree={v['agreement_pct'] if v['agreement_pct'] is None else round(v['agreement_pct'], 1)}% "
                       f"kappa={v['kappa'] if v['kappa'] is None else round(v['kappa'], 3)} "
                       f"wkappa={v['kappa_linear_weighted'] if v['kappa_linear_weighted'] is None else round(v['kappa_linear_weighted'], 3)}"
                       for k, v in r["pairs"].items())
        out.append(f"{lg}: {pr}")
        out.append(f"{lg}: flagged {r['flagged']}; strictly flagged {r['strictly_flagged']}; "
                   f"rule (e) decision: {r['rule_e_decision']}")
        if "c2_naturalness" in r:
            out.append(f"{lg}: C2 naturalness {r['c2_naturalness']}; checklist {r['c2_checklist_counts']}")
    for lg, a in res["aliases"].items():
        out.append(f"C4 {lg}: " + (f"{a['usage_counts']}, common word {a['common_word_count']}, share not used "
                                   f"{a['share_not_used']:.3f}" if a["available"] else "no parsed reply"))
    return out


# ============================================================================ main
def main(argv=None):
    ap = argparse.ArgumentParser(description="AIAS v0.62 AI translation and alias check (DEVIATIONS Entry 2)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true", help="the default: build prompts, print plan, guards, cost")
    g.add_argument("--check-models", action="store_true", help="free model metadata lookup (network)")
    g.add_argument("--run", action="store_true", help="the paid check (guarded; cap $8)")
    g.add_argument("--analyze", action="store_true", help="analysis of the recorded replies")
    a = ap.parse_args(argv)
    if a.check_models:
        p, rec = check_models()
        print(json.dumps(rec, indent=1))
        print(f"written: {p}")
        return 0 if all(m.get("found") for m in rec["models"].values()) else 4
    if a.run:
        bad = run_guards()
        if bad:
            for b in bad:
                print(f"REFUSED: {b}", file=sys.stderr)
            return 3
        try:
            require_keys()
        except Refused as e:
            print(f"REFUSED: {e}", file=sys.stderr)
            return 3
        st = run_checks()
        print(f"result: {st}; recorded spend ${spent(read_raw()):.4f}")
        return {"done": 0, "incomplete": 5, "stop": 6}[st]
    if a.analyze:
        fp = frozen_problems()
        if fp:
            print(f"REFUSED: frozen files differ: {fp}", file=sys.stderr)
            return 3
        res, _s, _a = write_analysis(read_raw())
        print("\n".join(summary_lines(res)))
        return 0
    return dry_run()


if __name__ == "__main__":
    sys.exit(main())
