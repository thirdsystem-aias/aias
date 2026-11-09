#!/usr/bin/env python3
"""
feasibility_v0_41.py — pre-lock technical check for the v0.41 t3 wave.

NON-ACQUISITION: sends one neutral prompt ("Reply with the single word: ready",
the v0.39/v0.40 feasibility prompt) to each of the six panel aliases through each
of the three provider call paths the five verbatim t1 runners use, and no study
probe. It answers one question before the lock: does every runner's SDK path still
reach every panel model, and which dated snapshot does each alias serve today?

Call paths (the runners' own functions, imported, not re-implemented):
  P19  protocol/providers.py  call_anthropic / call_openai / call_google
       (v0.19 runner; Gemini via google-generativeai, max_output_tokens 1024)
  P20  scripts/run_acquisition_v20.py  call_llm   (v0.20–v0.22 share this code;
       Gemini via google-generativeai with server defaults; max_tokens 1024)
  P23  scripts/acquire_v0_23.py  call_anthropic / call_openai / call_google
       (v0.23 runner; Gemini via google-genai; temperature 0, 2,048 tokens)

Served model ids, finish reasons and token counts are teed through the v41
provenance wrapper into osf/v41/prereg/feasibility_provenance_v0_41.csv; the
summary goes to osf/v41/prereg/feasibility_v0_41.json.

Run on the Mac (keys come from the login shell):
  zsh -ic 'cd <worktree> && AIAS_ROOT=$PWD ~/aias/.venv-v41/bin/python osf/v41/scripts/feasibility_v0_41.py'
"""
import hashlib
import importlib.util
import json
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("AIAS_ROOT", str(Path.home() / "aias")))
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import v41_provenance as PROV  # noqa: E402

PROV.SIDECAR = ROOT / "osf" / "v41" / "prereg" / "feasibility_provenance_v0_41.csv"
OUT = ROOT / "osf" / "v41" / "prereg" / "feasibility_v0_41.json"
PROMPT = "Reply with the single word: ready"
PANEL = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini",
         "gemini-2.5-flash", "gemini-2.5-flash-lite"]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def main():
    acq = _load(HERE / "run_acquisition_v41.py", "racq41")
    acq.install_sdk_provenance()
    providers = _load(ROOT / "protocol" / "providers.py", "prov19")
    r20 = _load(ROOT / "scripts" / "run_acquisition_v20.py", "racq_v20_feas")
    r23 = _load(ROOT / "scripts" / "acquire_v0_23.py", "racq_v23_feas")

    def p19(model):
        fn = (providers.call_anthropic if model.startswith("claude") else
              providers.call_openai if model.startswith("gpt") else providers.call_google)
        r = fn(model, PROMPT)
        return getattr(r, "text", None) or getattr(r, "response", None) or str(r)[:200]

    def p20(model):
        text, _ = r20.call_llm(model, PROMPT)
        return text

    def p23(model):
        fn = (r23.call_anthropic if model.startswith("claude") else
              r23.call_openai if model.startswith("gpt") else r23.call_google)
        return fn(model, PROMPT)

    records = []
    for path_id, fn in [("P19", p19), ("P20", p20), ("P23", p23)]:
        for model in PANEL:
            PROV.set_context("feas", path_id)
            t0 = time.time()
            rec = {"path": path_id, "alias": model, "prompt": PROMPT,
                   "prompt_sha256": hashlib.sha256(PROMPT.encode()).hexdigest()}
            try:
                out = fn(model)
                rec.update(status="ok", response=(out or "").strip()[:200], error=None)
            except SystemExit as e:
                rec.update(status="error", response=None, error=f"SystemExit: {e}")
            except Exception as e:
                rec.update(status="error", response=None,
                           error=f"{type(e).__name__}: {str(e)[:300]}")
            rec["seconds"] = round(time.time() - t0, 2)
            records.append(rec)
            print(f"{path_id} {model:24s} {rec['status']:5s} {rec['response'] or rec['error']}")

    # join served ids from the provenance tee (one row per SDK call, in order)
    served = []
    if PROV.SIDECAR.exists():
        import csv
        served = list(csv.DictReader(open(PROV.SIDECAR, encoding="utf-8")))
    import platform
    import anthropic, openai
    import google.genai as gg
    try:
        import google.generativeai as gga
        gga_v = gga.__version__
    except Exception:
        gga_v = None
    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump({
        "phase": "v0.41-feasibility",
        "purpose": "pre-lock technical check (non-acquisition; no study probe sent)",
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": platform.python_version(), "platform": platform.platform(),
                        "anthropic": anthropic.__version__, "openai": openai.__version__,
                        "google_genai": getattr(gg, "__version__", None),
                        "google_generativeai": gga_v},
        "prompt": PROMPT,
        "records": records,
        "served": served,
        "n_ok": sum(r["status"] == "ok" for r in records),
        "n_calls": len(records),
    }, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"\nfeasibility_v0_41: {sum(r['status']=='ok' for r in records)}/{len(records)} ok -> {OUT}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
