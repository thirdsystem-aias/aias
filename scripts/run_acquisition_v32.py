#!/usr/bin/env python3
"""
run_acquisition_v32.py — v0.32 two-arm acquisition runner.

Sends the LOCKED v0.32 probe text (prereg/v0_32_cpc_version_stability_content.py
ACQUISITION; verbatim v0.22) to the EXACT dated model ID per slot per vintage arm
(MODEL_PANEL_ARMS). Probe wording / registry / frames are identical across arms;
only the dated ID changes. Provider-returned model/version is captured on every
call (mandatory for the Gemini floating-alias slots).

Phase A: Recognition, 24 brands x 6 slots per arm (144/arm).
Phase B: Six-frame Recall, 6 frames x 6 slots per arm (36/arm), raw responses preserved.

Usage:
  # smoke: 1 brand x 6 slots x 2 arms (Phase A), print payloads+responses+versions
  python3 scripts/run_acquisition_v32.py --smoke [--smoke-brand Tesla]
  # full single arm:
  python3 scripts/run_acquisition_v32.py --arm A --phase both
  python3 scripts/run_acquisition_v32.py --arm B --phase both

Auth: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY (or GEMINI_API_KEY).
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "aias"
PREREG = ROOT / "prereg" / "v0_32_cpc_version_stability_content.py"
REGISTRY = ROOT / "registries" / "v0_32_registry.json"
OUTDIR = ROOT / "osf" / "v32" / "data"


def load_prereg():
    spec = importlib.util.spec_from_file_location("v032", PREREG)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def provider_of(model_id: str) -> str:
    if model_id.startswith("claude"):
        return "anthropic"
    if model_id.startswith("gpt") or model_id.startswith("o"):
        return "openai"
    if model_id.startswith("gemini"):
        return "google"
    raise ValueError(f"unrouted model id: {model_id}")


# ------------------------------------------------------------------ providers
def call_anthropic(client, model_id, prompt, max_out):
    r = client.messages.create(model=model_id, max_tokens=max_out,
                               messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in r.content if getattr(b, "type", None) == "text")
    return text, r.model  # r.model = resolved version


def call_openai(client, model_id, prompt, max_out):
    import openai
    msgs = [{"role": "user", "content": prompt}]
    try:
        r = client.chat.completions.create(model=model_id, max_tokens=max_out, messages=msgs)
    except openai.BadRequestError as e:
        m = str(e)
        if any(s in m for s in ("max_completion_tokens", "max_tokens", "output limit", "reached")):
            # reasoning-era (gpt-5.x): new param name + reasoning headroom
            r = client.chat.completions.create(
                model=model_id, max_completion_tokens=max_out + 2000, messages=msgs)
        else:
            raise
    return (r.choices[0].message.content or ""), r.model


def call_google(client, model_id, prompt, max_out):
    from google.genai import types
    r = client.models.generate_content(
        model=model_id, contents=prompt,
        config=types.GenerateContentConfig(max_output_tokens=max_out))
    text = r.text or ""
    ver = getattr(r, "model_version", None) or model_id  # resolved version for floating aliases
    return text, ver


def make_clients():
    import anthropic, openai
    from google import genai
    return {
        "anthropic": anthropic.Anthropic(),
        "openai": openai.OpenAI(),
        "google": genai.Client(
            api_key=os.environ.get("GOOGLE_API_KEY") or os.environ["GEMINI_API_KEY"]),
    }


CALLERS = {"anthropic": call_anthropic, "openai": call_openai, "google": call_google}


def one_call(clients, model_id, prompt, max_out):
    prov = provider_of(model_id)
    t0 = time.time()
    text, resolved = CALLERS[prov](clients[prov], model_id, prompt, max_out)
    return text, resolved, round((time.time() - t0) * 1000)


def parse_yes_no(text: str) -> str:
    t = (text or "").strip().lower()
    if t.startswith("yes"):
        return "yes"
    if t.startswith("no"):
        return "no"
    if "yes" in t[:40]:
        return "yes"
    if "no" in t[:40]:
        return "no"
    return "unclear"


def brands_from_registry(reg):
    out = []
    for cell_id, cell in reg["cells"].items():
        for b in cell["brands"]:
            out.append({"brand": b["name"], "cell": cell_id, "cascade_order": b["cascade_order"]})
    return out


# ---------------------------------------------------------------------- smoke
def smoke(clients, m, brand):
    panel = m.MODEL_PANEL_ARMS
    template = m.ACQUISITION["phase_a_recognition_template"]
    prompt = template.replace("{BRAND}", brand)
    print(f"\n=== SMOKE: Phase A recognition, brand={brand!r}, 6 slots x 2 arms = 12 calls ===")
    print(f"prompt sent (identical both arms): {prompt!r}\n")
    rows = []
    for arm in ("A", "B"):
        idx = 1 if arm == "A" else 2  # tuple is (tier_label, arm_A_id, arm_B_id)
        for slot, spec in panel.items():
            model_id = spec[idx]
            try:
                text, resolved, ms = one_call(clients, model_id, prompt, 64)
                verdict = parse_yes_no(text)
                print(f"[{arm}] {slot:18s} -> {model_id:30s} | resolved={resolved} | "
                      f"{verdict:7s} {ms}ms | {text.strip()[:60]!r}")
                rows.append({"arm": arm, "slot": slot, "model_id": model_id,
                             "resolved_version": resolved, "verdict": verdict,
                             "latency_ms": ms, "response": text.strip()[:200]})
            except Exception as e:
                print(f"[{arm}] {slot:18s} -> {model_id:30s} | ERROR {type(e).__name__}: {str(e)[:80]}")
                rows.append({"arm": arm, "slot": slot, "model_id": model_id, "error": f"{type(e).__name__}: {e}"})
    # echo the locked Phase B frame battery (text only -- not called in smoke)
    print("\n--- locked Phase B frames (verbatim; full run sends these to all slots/arms) ---")
    for ch, frames in m.ACQUISITION["phase_b_frames"].items():
        for fid, ftext in frames.items():
            print(f"  {ch}/{fid}: {ftext!r}")
    ok = sum(1 for r in rows if r.get("verdict") in ("yes", "no", "unclear"))
    print(f"\nsmoke: {ok}/12 calls returned; "
          f"{sum(1 for r in rows if 'error' in r)} errors")
    return rows


# ----------------------------------------------------------------- full phases
def run_phase_a(clients, m, reg, arm):
    panel = m.MODEL_PANEL_ARMS
    idx = 1 if arm == "A" else 2
    template = m.ACQUISITION["phase_a_recognition_template"]
    brands = brands_from_registry(reg)
    rows = []
    for b in brands:
        prompt = template.replace("{BRAND}", b["brand"])
        for slot, spec in panel.items():
            model_id = spec[idx]
            try:
                text, resolved, ms = one_call(clients, model_id, prompt, 64)
                rows.append({**b, "arm": arm, "slot": slot, "model_id": model_id,
                             "resolved_version": resolved, "probe_text": prompt,
                             "response_text": text, "recognized": parse_yes_no(text),
                             "latency_ms": ms, "timestamp": datetime.now(timezone.utc).isoformat()})
            except Exception as e:
                rows.append({**b, "arm": arm, "slot": slot, "model_id": model_id,
                             "probe_text": prompt, "response_text": f"ERROR {type(e).__name__}: {e}",
                             "recognized": "error"})
            print(f"  A[{arm}] {b['brand']:14s} {slot:18s} {rows[-1].get('recognized')}", flush=True)
    return rows


def run_phase_b(clients, m, arm):
    panel = m.MODEL_PANEL_ARMS
    idx = 1 if arm == "A" else 2
    frames = m.ACQUISITION["phase_b_frames"]
    rows = []
    for ch, chframes in frames.items():
        for fid, ftext in chframes.items():
            for slot, spec in panel.items():
                model_id = spec[idx]
                try:
                    text, resolved, ms = one_call(clients, model_id, ftext, 2048)
                    rows.append({"arm": arm, "channel": ch, "frame_id": fid, "frame_text": ftext,
                                 "slot": slot, "model_id": model_id, "resolved_version": resolved,
                                 "response_text": text, "latency_ms": ms,
                                 "timestamp": datetime.now(timezone.utc).isoformat()})
                except Exception as e:
                    rows.append({"arm": arm, "channel": ch, "frame_id": fid, "frame_text": ftext,
                                 "slot": slot, "model_id": model_id,
                                 "response_text": f"ERROR {type(e).__name__}: {e}"})
                print(f"  B[{arm}] {fid} {ch:6s} {slot:18s} {len(rows[-1].get('response_text',''))}c", flush=True)
    return rows


def write_csv(rows, path):
    if not rows:
        return
    fields = sorted({k for r in rows for k in r})
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"  wrote {path} ({len(rows)} rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--smoke-brand", default="Tesla")
    ap.add_argument("--arm", choices=["A", "B"])
    ap.add_argument("--phase", choices=["a", "b", "both"], default="both")
    args = ap.parse_args()

    m = load_prereg()
    reg = json.load(open(REGISTRY))
    clients = make_clients()

    if args.smoke:
        rows = smoke(clients, m, args.smoke_brand)
        (OUTDIR).mkdir(parents=True, exist_ok=True)
        json.dump(rows, open(OUTDIR / "smoke.json", "w"), indent=2)
        print(f"\nsmoke rows -> {OUTDIR/'smoke.json'}")
        return 0

    if not args.arm:
        print("error: --arm A|B required for a full run (or use --smoke)")
        return 2
    arm = args.arm
    print(f"=== v0.32 acquisition — Arm {arm} ({m.VINTAGES[arm]}) ===")
    if args.phase in ("a", "both"):
        write_csv(run_phase_a(clients, m, reg, arm), OUTDIR / f"phase_a_{arm}.csv")
    if args.phase in ("b", "both"):
        write_csv(run_phase_b(clients, m, arm), OUTDIR / f"phase_b_{arm}.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
