"""Shared state of the local fake provider SDKs (rehearsal only; LOCK_STEPS.md step R). Nothing leaves the machine.

FAKE_STATE   directory for the fake provider's bill (bill.jsonl: one line per billed request) and batches
FAKE_SCALE   multiplies every token count (default 1); FAKE_S1_SCALE multiplies S1 token counts again (default 1)
FAKE_BATCH_SECONDS  a Message Batch ends this many seconds after it was created (default 0)
Token counts per request (before scaling) are fixed below, so that a full 876-call run costs about $65 at the
budget_v0_42 prices (the central estimate of the pre-registration is $63.97).
"""
import json
import os
import threading
from pathlib import Path

STATE = Path(os.environ.get("FAKE_STATE", "/tmp/v42_fake_state"))
STATE.mkdir(parents=True, exist_ok=True)
_lock = threading.Lock()

# provider -> condition -> (input, output, thinking, searches); output includes thinking for anthropic/openai
TOKENS = {
    "anthropic": {"S0": (30, 1500, None, 0), "S1": (20000, 2000, None, 3)},
    "openai": {"S0": (30, 1200, 400, 0), "S1": (15000, 1500, 400, 3)},
    "google": {"S0": (30, 1000, 500, 0), "S1": (10000, 1000, 500, 3)},
}


def tokens(provider, cond):
    tin, tout, think, n = TOKENS[provider][cond]
    k = float(os.environ.get("FAKE_SCALE", "1")) * (float(os.environ.get("FAKE_S1_SCALE", "1")) if cond == "S1" else 1)
    return int(tin * k), int(tout * k), (int(think * k) if think is not None else None), n


def bill(provider, model, mode, tin, tout, think, searches):
    with _lock:
        with open(STATE / "bill.jsonl", "a") as f:
            f.write(json.dumps({"provider": provider, "model": model, "mode": mode, "input_tokens": tin,
                                "output_tokens": tout, "thinking_tokens": think, "n_searches": searches,
                                "pid": os.getpid()}) + "\n")


def next_id(prefix):
    with _lock:
        p = STATE / f"{prefix}.counter"
        n = int(p.read_text()) + 1 if p.exists() else 1
        p.write_text(str(n))
        return f"{prefix}_{n:04d}"
