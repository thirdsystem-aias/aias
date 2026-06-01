#!/usr/bin/env python3
"""
run_acquisition_v28.py — AIAS v0.28 (CV.04) acquisition runner.

Build tooling (NOT a pre-reg artifact). Forked from run_acquisition_v22.py.
The PROBES it sends are byte-locked to the r2-registered mega_prompt; a runtime
self-check asserts byte-equality and aborts on any drift (see verify_probes()).

Forked from run_acquisition_v22.py with these deltas:
  1. Panel loader reads prereg/v0_28_panel_brands.txt (the r2-frozen 24) directly.
     NO mod.REGISTRY dependency. NEVER reads brand_validator.csv (blinding).
  2. Flat single panel — v0.28 has NO Cell A/B/C measurement structure. All 24
     brands probed uniformly under one synthetic cell "T". Familiarity tertiles
     are BLINDED sampling metadata derived from the validator; the harness never
     sees or branches on them.
  3. Probes = v0.28 registered Tech probes (Phase A recognition + 6 Phase B
     frames, q1-q3 R_cat / q4-q6 R_cult). Byte-match the r2 mega_prompt; enforced.
  4. Phase B = 3 frames/channel (max 18) — matches the r2 bridge /18 normalization.
  5. Output -> osf/v28/data/phase_a_results.csv + phase_b_results.csv (feeds bridge_v28.py).
  6. Model ids unchanged from the locked six-slot panel.

Required env vars: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY (or GEMINI_API_KEY)
Required packages: anthropic, openai, google-generativeai

Usage:
    python run_acquisition_v28.py --stage0     # pre-flight (panel/COI/blinding/templates/model-ping)
    python run_acquisition_v28.py --dry-run    # no API calls
    python run_acquisition_v28.py --phase a    # Phase A only
    python run_acquisition_v28.py              # both phases
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration -----------------------------------------------------------

AIAS_ROOT = Path.home() / "aias"
PANEL_FILE = AIAS_ROOT / "prereg" / "v0_28_panel_brands.txt"
MEGA_PROMPT = AIAS_ROOT / "prereg" / "v0_28_mega_prompt.md"
DEFAULT_OUTPUT_DIR = AIAS_ROOT / "osf" / "v28"

# v0.28 registered probes — byte-locked to the r2 mega_prompt (verify_probes asserts).
PHASE_A_PROBE_TEMPLATE = (
    "Is the brand {BRAND} commonly recognized as a technology brand? Answer yes or no."
)
PHASE_B_FRAMES = {
    "R_cat": {
        "q1": "What are the best technology brands? List several with descriptions.",
        "q2": "What technology brands do industry experts and analysts recommend? Name several.",
        "q3": "What technology brands are highest quality and most reliable? Name several with descriptions.",
    },
    "R_cult": {
        "q4": "What technology brands are most talked about right now? List several.",
        "q5": "What technology brands have the biggest cultural footprint? Name several.",
        "q6": "Which technology brands have the most iconic or storied identity in popular culture? Name several.",
    },
}

PROVIDER_BY_MODEL = {
    "claude-opus-4-5":      "anthropic",
    "claude-sonnet-4-5":    "anthropic",
    "gpt-4o":               "openai",
    "gpt-4o-mini":          "openai",
    "gemini-2.5-flash":     "google",
    "gemini-2.5-flash-lite": "google",
}
REFERENCE_PANEL = list(PROVIDER_BY_MODEL.keys())


# --- Panel loader (flat 24; blinding-safe) ----------------------------------

def load_panel() -> list[str]:
    """Read the frozen 24-brand panel. Reads ONLY panel_brands.txt — never the
    validator (no familiarity/d'/tertile ever enters the harness)."""
    if not PANEL_FILE.exists():
        sys.exit(f"ERROR: frozen panel not found at {PANEL_FILE}")
    brands = [l.strip() for l in PANEL_FILE.read_text().splitlines() if l.strip()]
    if len(brands) != 24:
        sys.exit(f"ERROR: expected 24 panel brands, found {len(brands)}")
    return brands


# --- Probe byte-match self-check against the registered mega_prompt ----------

def verify_probes() -> None:
    """Abort unless the embedded probes byte-match the registered mega_prompt.
    Parses prereg/v0_28_mega_prompt.md (the working-tree copy, which CI/caller
    must confirm == the r2 tag) and asserts equality."""
    mp = MEGA_PROMPT.read_text()
    pa = re.search(r"Probe \(exact wording\):\s*\n+>\s*(.+)", mp).group(1).replace("**", "").strip()
    frames = dict(re.findall(r"-\s*(q[1-6])\s*\([^)]*\):\s*\*(.+?)\*", mp))
    embedded = {"PHASE_A": PHASE_A_PROBE_TEMPLATE}
    embedded.update({q: t for ch in PHASE_B_FRAMES.values() for q, t in ch.items()})
    registered = {"PHASE_A": pa}
    registered.update({q: t.strip() for q, t in frames.items()})
    mism = [k for k in embedded if embedded.get(k) != registered.get(k)]
    if mism:
        for k in mism:
            print(f"  PROBE DRIFT [{k}]:\n    embedded:   {embedded.get(k)!r}\n"
                  f"    registered: {registered.get(k)!r}", file=sys.stderr)
        sys.exit("ABORT: harness probes do not byte-match the registered mega_prompt.")


# --- Auth/error detection (inherited from v22) -------------------------------

class AuthErrorFatal(Exception):
    pass


def _is_auth_error(e: Exception) -> bool:
    msg = str(e).lower(); tn = type(e).__name__.lower()
    if "authentication" in tn or "permission" in tn:
        return True
    return any(m in msg for m in [
        "invalid x-api-key", "invalid api key", "api key not valid", "api_key_invalid",
        "incorrect api key", "authentication_error", "unauthorized", "401", "403 forbidden"])


def _is_rate_limit(e: Exception) -> bool:
    msg = str(e).lower(); tn = type(e).__name__.lower()
    if "ratelimit" in tn or "rate_limit" in tn:
        return True
    return any(m in msg for m in ["rate limit", "rate-limit", "429", "quota exceeded", "too many requests"])


# --- LLM adapters (lazy) -----------------------------------------------------

_anthropic_client = None
_openai_client = None
_google_models = {}


def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        try:
            from anthropic import Anthropic
        except ImportError:
            sys.exit("ERROR: anthropic not installed.")
        _anthropic_client = Anthropic()
    return _anthropic_client


def _get_openai():
    global _openai_client
    if _openai_client is None:
        try:
            from openai import OpenAI
        except ImportError:
            sys.exit("ERROR: openai not installed.")
        _openai_client = OpenAI()
    return _openai_client


def _get_google(model_name: str):
    if model_name not in _google_models:
        try:
            import google.generativeai as genai
        except ImportError:
            sys.exit("ERROR: google-generativeai not installed.")
        key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if not key:
            sys.exit("ERROR: GOOGLE_API_KEY (or GEMINI_API_KEY) not set")
        genai.configure(api_key=key)
        _google_models[model_name] = genai.GenerativeModel(model_name)
    return _google_models[model_name]


def call_llm(model_name: str, prompt: str, max_tokens: int = 1024,
             max_retries: int = 4) -> tuple[str, float]:
    provider = PROVIDER_BY_MODEL.get(model_name)
    if not provider:
        raise ValueError(f"Unknown model: {model_name}")
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            start = time.time()
            if provider == "anthropic":
                resp = _get_anthropic().messages.create(
                    model=model_name, max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}])
                text = resp.content[0].text if resp.content else ""
            elif provider == "openai":
                resp = _get_openai().chat.completions.create(
                    model=model_name, max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}])
                text = resp.choices[0].message.content or ""
            elif provider == "google":
                resp = _get_google(model_name).generate_content(prompt)
                try:
                    text = resp.text
                except Exception:
                    text = ""
                    if hasattr(resp, "candidates") and resp.candidates:
                        parts = getattr(resp.candidates[0].content, "parts", [])
                        text = "".join(getattr(p, "text", "") for p in parts)
            else:
                raise ValueError(f"Unhandled provider: {provider}")
            return text, time.time() - start
        except Exception as e:
            if _is_auth_error(e):
                raise AuthErrorFatal(f"{model_name} rejected the API key — {type(e).__name__}: {e}") from e
            last_err = e
            if attempt == max_retries:
                break
            sleep = min(5.0 * attempt + 5.0, 60.0) if _is_rate_limit(e) else min(2.0 ** attempt + 0.5, 30.0)
            print(f"    ! {model_name} attempt {attempt} ({type(e).__name__}); sleep {sleep:.1f}s", flush=True)
            time.sleep(sleep)
    raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_err}") from last_err


def parse_yes_no(response_text: str) -> str:
    if not response_text:
        return "ambiguous"
    t = response_text.strip().lower()
    while t and t[0] in "*_`#- \"'.,":
        t = t[1:]
    if not t:
        return "ambiguous"
    first_word = t.split()[0].strip(".,!?'\"`*_")
    if first_word == "yes":
        return "yes"
    if first_word == "no":
        return "no"
    fs = t.split(".")[0]
    has_yes = " yes" in (" " + fs) or fs.startswith("yes")
    has_no = " no " in (" " + fs + " ") or fs.startswith("no ")
    if has_yes and not has_no:
        return "yes"
    if has_no and not has_yes:
        return "no"
    return "ambiguous"


# --- Phase A: Recognition (flat 24 x 6 = 144) -------------------------------

def run_phase_a(panel, output_path, max_workers, dry_run) -> None:
    tasks = [{"brand": b, "cell": "T", "model": m}
             for b in panel for m in REFERENCE_PANEL]
    print(f"\n--- Phase A: Recognition ---")
    print(f"  {len(tasks)} probes ({len(REFERENCE_PANEL)} models × {len(panel)} brands)")
    print(f"  Probe template: {PHASE_A_PROBE_TEMPLATE!r}")
    if dry_run:
        print(f"  [dry-run] would call {len(tasks)} probes; skipping.")
        return
    rows, auth_failure = [], False
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        f2t = {}
        for task in tasks:
            prompt = PHASE_A_PROBE_TEMPLATE.replace("{BRAND}", task["brand"]).replace("{brand}", task["brand"])
            f2t[pool.submit(call_llm, task["model"], prompt, 64)] = (task, prompt)
        for i, fut in enumerate(as_completed(f2t), 1):
            task, prompt = f2t[fut]
            try:
                resp, lat = fut.result()
                rec = parse_yes_no(resp)
                rows.append({**task, "probe_text": prompt, "response_text": resp,
                             "recognized": rec,
                             "timestamp": datetime.now(timezone.utc).isoformat(),
                             "latency_s": f"{lat:.3f}"})
                print(f"  [{i:3d}/{len(tasks)}] {task['model']:25s} {task['brand']:28s} → {rec}", flush=True)
            except AuthErrorFatal as e:
                if not auth_failure:
                    auth_failure = True
                    print(f"\n  ✗ AUTH FAILURE: {e}", flush=True)
                for f in f2t:
                    f.cancel()
            except Exception as e:
                rows.append({**task, "probe_text": prompt,
                             "response_text": f"<ERROR: {type(e).__name__}: {e}>",
                             "recognized": "error",
                             "timestamp": datetime.now(timezone.utc).isoformat(), "latency_s": "0"})
                print(f"  [{i:3d}/{len(tasks)}] ! {task['brand']} on {task['model']}: FAILED ({e})", flush=True)
    if auth_failure:
        sys.exit(1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["brand", "cell", "model", "probe_text", "response_text",
              "recognized", "timestamp", "latency_s"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in sorted(rows, key=lambda r: (r["brand"], r["model"])):
            w.writerow(row)
    print(f"\n  → Phase A written: {output_path} ({len(rows)} rows)")
    print("\n  Per-brand C_P (0..6):")
    for b in panel:
        br = [r for r in rows if r["brand"] == b]
        yes = sum(1 for r in br if r["recognized"] == "yes")
        print(f"    {b:28s}  C_P = {yes}/{len(br)}")


# --- Phase B: Six-frame Recall (3/channel, max 18) --------------------------

def run_phase_b(output_path, max_workers, dry_run) -> None:
    tasks = [{"model": m, "frame_id": q, "channel": ch, "frame_text": t}
             for ch, frames in PHASE_B_FRAMES.items()
             for q, t in frames.items() for m in REFERENCE_PANEL]
    print(f"\n--- Phase B: Six-frame Recall ---")
    print(f"  {len(tasks)} queries ({len(REFERENCE_PANEL)} models × 6 frames; 3/channel, max 18)")
    if dry_run:
        print(f"  [dry-run] would call {len(tasks)} queries; skipping.")
        return
    rows, auth_failure = [], False
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        f2t = {pool.submit(call_llm, t["model"], t["frame_text"], 2048): t for t in tasks}
        for i, fut in enumerate(as_completed(f2t), 1):
            task = f2t[fut]
            try:
                resp, lat = fut.result()
                rows.append({**task, "response_text": resp,
                             "timestamp": datetime.now(timezone.utc).isoformat(),
                             "latency_s": f"{lat:.3f}"})
                print(f"  [{i:2d}/{len(tasks)}] {task['model']:25s} {task['frame_id']} "
                      f"({task['channel']:6s}): {resp[:70].replace(chr(10),' ')}...", flush=True)
            except AuthErrorFatal as e:
                if not auth_failure:
                    auth_failure = True
                    print(f"\n  ✗ AUTH FAILURE: {e}", flush=True)
                for f in f2t:
                    f.cancel()
            except Exception as e:
                rows.append({**task, "response_text": f"<ERROR: {type(e).__name__}: {e}>",
                             "timestamp": datetime.now(timezone.utc).isoformat(), "latency_s": "0"})
                print(f"  [{i:2d}/{len(tasks)}] ! {task['frame_id']} on {task['model']}: FAILED ({e})", flush=True)
    if auth_failure:
        sys.exit(1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["model", "frame_id", "channel", "frame_text", "response_text",
              "timestamp", "latency_s"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in sorted(rows, key=lambda r: (r["channel"], r["frame_id"], r["model"])):
            w.writerow(row)
    print(f"\n  → Phase B written: {output_path} ({len(rows)} responses)")


# --- Stage 0 pre-flight ------------------------------------------------------

COI_RE = re.compile(r"samsung|harman|jbl|akg|smartthings", re.I)


def stage0(panel) -> int:
    print("=== Stage 0 pre-flight (no Phase A/B probes) ===\n")
    # a. panel + COI
    print(f"a. Panel: {len(panel)} brands from {PANEL_FILE.name}")
    coi = [b for b in panel if COI_RE.search(b)]
    print(f"   COI re-grep (samsung|harman|jbl|akg|smartthings): "
          f"{'CLEAN (0)' if not coi else 'HITS: ' + str(coi)}")
    if coi:
        sys.exit("STOP: COI brand in panel.")
    # b. blinding — detect an actual READ PATH of the validator, not mere mentions.
    # A leak is a file-open/read whose target resolves to the validator. Comments,
    # docstrings, and this very self-check name the validator without reading it,
    # so we scan for open()/read_text/read_csv/DictReader bound to a validator path.
    src = Path(__file__).read_text()
    read_leak = re.search(
        r"(open|read_text|read_csv|DictReader)\s*\([^)]*"
        r"(validator|brand_validator|familiarity|dprime)", src, re.I)
    print(f"\nb. Blinding: validator file-read path in harness? "
          f"{'YES (LEAK!)' if read_leak else 'NO — only panel_brands.txt + mega_prompt are read'}")
    if read_leak:
        sys.exit("STOP: validator read path present (blinding leak): %r" % read_leak.group(0))
    # c. probe templates + byte-match
    print("\nc. Probe templates (verbatim) + byte-match vs r2 mega_prompt:")
    verify_probes()
    print(f"   Phase A: {PHASE_A_PROBE_TEMPLATE}")
    for ch, frames in PHASE_B_FRAMES.items():
        for q, t in frames.items():
            print(f"   {q} ({ch}): {t}")
    print("   -> verify_probes() PASSED (embedded == registered)")
    # d. model ping
    print("\nd. Model ping (raw replies):")
    for m in REFERENCE_PANEL:
        try:
            txt, lat = call_llm(m, "Reply with the single word: ping", max_tokens=16, max_retries=2)
            ts = datetime.now(timezone.utc).isoformat()
            print(f"   [{m}] {ts} ({lat:.2f}s) RAW: {txt!r}")
        except Exception as e:
            print(f"   [{m}] PING FAILED: {type(e).__name__}: {e}")
            sys.exit(f"STOP: model {m} down — no silent swap.")
    print("\n=== Stage 0 complete. ===")
    return 0


def sdk_versions() -> dict:
    """Record SDK + python versions for the deposit's run metadata."""
    import platform
    v = {"python": platform.python_version()}
    for mod, name in [("anthropic", "anthropic"), ("openai", "openai"),
                      ("google.generativeai", "google.generativeai")]:
        try:
            m = __import__(mod, fromlist=["__version__"])
            v[name] = getattr(m, "__version__", "unknown")
        except Exception as e:
            v[name] = f"import-failed: {e}"
    return v


def write_run_metadata(out: Path, phase: str) -> None:
    import json
    meta = {
        "phase": phase,
        "study": "v0.28 / CV.04",
        "acquired_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sdk_versions": sdk_versions(),
        "reference_panel": REFERENCE_PANEL,
        "panel_file": str(PANEL_FILE),
        "panel_n": len(load_panel()),
        "phase_a_probe": PHASE_A_PROBE_TEMPLATE,
        "phase_b_frames": PHASE_B_FRAMES,
        "probe_lock": "byte-verified == v0.28-prereg-r2 mega_prompt",
    }
    p = out / "data" / "v0.28_run_metadata.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    # merge across phase-a / phase-b runs rather than clobber
    existing = {}
    if p.exists():
        existing = json.loads(p.read_text())
    if "runs" not in existing:
        existing = {"study": meta["study"], "runs": []}
    existing["runs"].append(meta)
    p.write_text(json.dumps(existing, indent=2))
    print(f"  → run metadata: {p}")


def check_api_keys() -> list[str]:
    need = set(PROVIDER_BY_MODEL.values())
    miss = []
    if "anthropic" in need and "ANTHROPIC_API_KEY" not in os.environ:
        miss.append("ANTHROPIC_API_KEY")
    if "openai" in need and "OPENAI_API_KEY" not in os.environ:
        miss.append("OPENAI_API_KEY")
    if "google" in need and "GOOGLE_API_KEY" not in os.environ and "GEMINI_API_KEY" not in os.environ:
        miss.append("GOOGLE_API_KEY (or GEMINI_API_KEY)")
    return miss


def main() -> int:
    p = argparse.ArgumentParser(description="AIAS v0.28 (CV.04) acquisition runner")
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    p.add_argument("--phase", choices=["a", "b", "all"], default="all")
    p.add_argument("--max-workers", type=int, default=6)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--stage0", action="store_true", help="pre-flight only; no Phase A/B probes")
    args = p.parse_args()

    panel = load_panel()
    verify_probes()   # byte-lock gate on EVERY invocation

    if args.stage0:
        miss = check_api_keys()
        if miss:
            print(f"ERROR: missing API keys: {', '.join(miss)}", file=sys.stderr)
            return 2
        return stage0(panel)

    out = Path(args.output_dir).expanduser()
    print("AIAS v0.28 (CV.04) acquisition runner")
    print(f"  Panel:  {len(panel)} brands (flat; no cell structure)")
    print(f"  Output: {out}")
    miss = check_api_keys()
    if miss and not args.dry_run:
        print(f"\nERROR: missing API keys: {', '.join(miss)}", file=sys.stderr)
        return 2
    if args.dry_run:
        print("\n[DRY-RUN] No API calls will be made.")
    # results live under osf/v28/data/ (same dir as run_metadata + what bridge_v28 reads)
    data_dir = out / "data"
    if args.phase in ("a", "all"):
        run_phase_a(panel, data_dir / "phase_a_results.csv", args.max_workers, args.dry_run)
        if not args.dry_run:
            write_run_metadata(out, "phase_a")
    if args.phase in ("b", "all"):
        run_phase_b(data_dir / "phase_b_results.csv", args.max_workers, args.dry_run)
        if not args.dry_run:
            write_run_metadata(out, "phase_b")
    if not args.dry_run:
        print("\n✓ Acquisition complete. Next: python3 scripts/bridge_v28.py ; python3 scripts/score_v28.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
