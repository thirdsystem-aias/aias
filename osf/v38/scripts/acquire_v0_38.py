#!/usr/bin/env python3
"""
AIAS v0.38 — Home Coffee Roasters (Aillio-focal) acquisition script
Pre-reg tag: v0.38-prereg-r1 | Presence definitions per Methodology v1.2 (SSRN 6761698)

Forked from osf/v23/scripts/acquire_v0_23.py. Decoding is unchanged from v0.23:
temperature 0.0, max output 2,048 tokens, single user turn, no system prompt,
one call per probe x model. Changes vs v0.23 (all metadata-only): probes are read
from the locked probe file and checksum-verified; each record also stores the
served model id, finish reason, token usage, attempt count and prompt sha256;
transient errors retry up to 3x with backoff; an empty reply is retried once
with identical configuration (pre-registration section 4.4).

Calls: 22 probes (18 recommendation + 4 Aillio probes) x 6 models = 132.
Order: probes in battery order; models M1..M6 within probe.
Output: osf/v38/data/v38_raw.json (checkpointed every 12 calls).
Environment: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY.

Usage:
  cd /Users/pablou/aias
  python3 scripts/acquire_v0_38.py --dry-run
  python3 scripts/acquire_v0_38.py
  python3 scripts/acquire_v0_38.py --resume
"""
import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PIPELINE_ROOT = Path("/Users/pablou/aias")
PROBES_PATH = PIPELINE_ROOT / "osf" / "v38" / "prereg" / "probes_v0_38.json"
OUTPUT_DIR = PIPELINE_ROOT / "osf" / "v38" / "data"
RAW_PATH = OUTPUT_DIR / "v38_raw.json"

# Model panel (fixed from v0.17). Boundary = position relative to the Bullet R2
# announcement (2024-07-03): "pre" models have an October 2023 knowledge cutoff.
MODELS = [
    {"slot": "M1", "name": "Claude Opus 4.5",       "provider": "anthropic", "model_id": "claude-opus-4-5",       "boundary": "post", "documented_cutoff": "May 2025 (reliable knowledge)"},
    {"slot": "M2", "name": "Claude Sonnet 4.5",     "provider": "anthropic", "model_id": "claude-sonnet-4-5",     "boundary": "post", "documented_cutoff": "Jan 2025 (reliable knowledge)"},
    {"slot": "M3", "name": "GPT-4o",                "provider": "openai",    "model_id": "gpt-4o",                "boundary": "pre",  "documented_cutoff": "Oct 2023"},
    {"slot": "M4", "name": "GPT-4o-mini",           "provider": "openai",    "model_id": "gpt-4o-mini",           "boundary": "pre",  "documented_cutoff": "Oct 2023"},
    {"slot": "M5", "name": "Gemini 2.5 Flash",      "provider": "google",    "model_id": "gemini-2.5-flash",      "boundary": "post", "documented_cutoff": "Jan 2025"},
    {"slot": "M6", "name": "Gemini 2.5 Flash Lite", "provider": "google",    "model_id": "gemini-2.5-flash-lite", "boundary": "post", "documented_cutoff": "Jan 2025"},
]

PAUSE = {"anthropic": 2.0, "openai": 1.0, "google": 1.0}
MAX_ATTEMPTS = 3


class Transient(Exception):
    """Rate limit, 5xx/overload, connection or timeout error: retry-eligible."""


def call_anthropic(model_id, prompt):
    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    try:
        m = client.messages.create(model=model_id, max_tokens=2048, temperature=0.0,
                                   messages=[{"role": "user", "content": prompt}])
    except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except anthropic.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    text = "".join(b.text for b in m.content if hasattr(b, "text"))
    return {"text": text, "served_model": m.model, "finish_reason": m.stop_reason,
            "tokens_in": m.usage.input_tokens, "tokens_out": m.usage.output_tokens, "tokens_thought": None}


def call_openai(model_id, prompt):
    import openai
    client = openai.OpenAI()  # reads OPENAI_API_KEY
    try:
        r = client.chat.completions.create(model=model_id, max_tokens=2048, temperature=0.0,
                                           messages=[{"role": "user", "content": prompt}])
    except (openai.RateLimitError, openai.APIConnectionError, openai.APITimeoutError) as e:
        raise Transient(str(e)) from e
    except openai.APIStatusError as e:
        if e.status_code >= 500:
            raise Transient(str(e)) from e
        raise
    c = r.choices[0]
    return {"text": c.message.content or "", "served_model": r.model, "finish_reason": c.finish_reason,
            "tokens_in": r.usage.prompt_tokens, "tokens_out": r.usage.completion_tokens, "tokens_thought": None}


def call_google(model_id, prompt):
    from google import genai
    from google.genai import errors, types
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    try:
        r = client.models.generate_content(model=model_id, contents=prompt,
                                           config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=2048))
    except errors.ServerError as e:
        raise Transient(str(e)) from e
    except errors.ClientError as e:
        if getattr(e, "code", None) == 429:
            raise Transient(str(e)) from e
        raise
    um = r.usage_metadata
    try:
        fr = str(r.candidates[0].finish_reason)
    except Exception:
        fr = None
    return {"text": r.text or "", "served_model": getattr(r, "model_version", None), "finish_reason": fr,
            "tokens_in": getattr(um, "prompt_token_count", None), "tokens_out": getattr(um, "candidates_token_count", None),
            "tokens_thought": getattr(um, "thoughts_token_count", None)}


DISPATCH = {"anthropic": call_anthropic, "openai": call_openai, "google": call_google}


def _now():
    return datetime.now(timezone.utc).isoformat()


def _call_with_retry(fn, model_id, prompt):
    last = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return fn(model_id, prompt), attempt, None
        except Transient as e:
            last = f"transient: {e}"[:500]
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** (attempt - 1))
        except Exception as e:
            return None, attempt, f"{type(e).__name__}: {e}"[:500]
    return None, MAX_ATTEMPTS, last


def send_cell(model, probe):
    fn = DISPATCH[model["provider"]]
    ts_start = _now()
    out, attempts, err = _call_with_retry(fn, model["model_id"], probe["prompt"])
    empty_retry = False
    if out is not None and not out["text"].strip():
        empty_retry = True
        out2, a2, err2 = _call_with_retry(fn, model["model_id"], probe["prompt"])
        attempts += a2
        if out2 is not None:
            out = out2
        if err2:
            err = err2
    ts_end = _now()
    time.sleep(PAUSE[model["provider"]])
    status = "error" if out is None else ("empty" if not out["text"].strip() else "ok")
    out = out or {}
    return {
        "phase": "v0.38", "probe_id": probe["probe_id"], "tier": probe["tier"], "kind": probe["kind"],
        "prompt": probe["prompt"], "prompt_sha256": probe["sha256"],
        "model_slot": model["slot"], "model_name": model["name"], "model_id": model["model_id"],
        "provider": model["provider"], "boundary": model["boundary"],
        "response": out.get("text", ""), "status": status, "error": err,
        "served_model": out.get("served_model"), "finish_reason": out.get("finish_reason"),
        "tokens_in": out.get("tokens_in"), "tokens_out": out.get("tokens_out"), "tokens_thought": out.get("tokens_thought"),
        "attempts": attempts, "empty_retry": empty_retry, "ts_start": ts_start, "ts_end": ts_end,
    }


def load_probes():
    spec = json.loads(PROBES_PATH.read_text(encoding="utf-8"))
    for p in spec["probes"]:
        if hashlib.sha256(p["prompt"].encode()).hexdigest() != p["sha256"]:
            sys.exit(f"ABORT: checksum mismatch on probe {p['probe_id']}")
    return spec["probes"]


def save(records):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = RAW_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(RAW_PATH)


def main():
    ap = argparse.ArgumentParser(description="AIAS v0.38 acquisition — home coffee roasters (Aillio-focal)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--resume", action="store_true", help="keep cells already 'ok' in the raw file")
    args = ap.parse_args()
    probes = load_probes()
    total = len(probes) * len(MODELS)
    if args.dry_run:
        for p in probes:
            for m in MODELS:
                print(f"  DRY RUN: {p['probe_id']} [{p['tier']}] -> {m['slot']} {m['name']}")
        print(f"\nDry run complete. {total} calls would be sent.")
        return
    missing = [v for v in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY") if not os.environ.get(v)]
    if missing:
        sys.exit(f"ERROR: missing environment variables: {', '.join(missing)}")
    done = {}
    if args.resume and RAW_PATH.exists():
        for r in json.loads(RAW_PATH.read_text(encoding="utf-8")):
            if r["status"] == "ok":
                done[(r["probe_id"], r["model_slot"])] = r
    records, n = [], 0
    for p in probes:
        for m in MODELS:
            n += 1
            key = (p["probe_id"], m["slot"])
            if key in done:
                records.append(done[key])
                continue
            rec = send_cell(m, p)
            records.append(rec)
            print(f"  [{n:3d}/{total}] {p['probe_id']} -> {m['slot']} {m['name']:22s} {rec['status']:5s} "
                  f"served={rec['served_model']} out={rec['tokens_out']} fr={rec['finish_reason']}", flush=True)
            if n % 12 == 0:
                save(records)
    save(records)
    ok = sum(r["status"] == "ok" for r in records)
    print(f"\nAcquisition complete: {ok}/{len(records)} ok -> {RAW_PATH}")


if __name__ == "__main__":
    main()
