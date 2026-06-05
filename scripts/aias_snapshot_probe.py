#!/usr/bin/env python3
"""
aias_snapshot_probe.py — v0.32 snapshot-availability probe.

Gate for the v0.32 before/after (version-snapshot stability) design. For each
provider it (1) enumerates the live model list, (2) confirms each candidate
dated model ID is callable today via a 1-token completion, and (3) emits
registries/v0_32_snapshot_resolution.json with REACHABLE/DEPRECATED per slot
plus a window-expiry note per slot so acquisition can be scheduled before any
deprecation cliff.

Two arms:
  A = oldest still-served dated snapshots ("v0.17-era class")
  B = current dated snapshots

Auth via env: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY (or GEMINI_API_KEY).

Usage:
  python3 scripts/aias_snapshot_probe.py \
      --emit registries/v0_32_snapshot_resolution.json
  python3 scripts/aias_snapshot_probe.py --no-emit   # dry tabulate, no file
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

# ------------------------------------------------------------------
# Candidate panel — six slots × two arms. "current GPT" snapshots are
# resolved against the live listing if left as None; everything else is a
# concrete ID we assert callable.
# ------------------------------------------------------------------
CANDIDATES = {
    "A": {  # oldest still-served, dated
        "claude_opus":       ("anthropic", "claude-opus-4-5-20251101"),
        "claude_sonnet":     ("anthropic", "claude-sonnet-4-5-20250929"),
        "gpt_4o":            ("openai",    "gpt-4o-2024-11-20"),
        "gpt_4o_mini":       ("openai",    "gpt-4o-mini-2024-07-18"),
        "gemini_flash":      ("google",    "gemini-2.5-flash"),
        "gemini_flash_lite": ("google",    "gemini-2.5-flash-lite"),
    },
    "B": {  # current, dated
        "claude_opus":       ("anthropic", "claude-opus-4-8"),
        "claude_sonnet":     ("anthropic", "claude-sonnet-4-6"),
        "gpt_4o":            ("openai",    "gpt-5.5-2026-04-23"),       # current flagship (gpt-4o family frozen at 2024-11-20)
        "gpt_4o_mini":       ("openai",    "gpt-5.4-mini-2026-03-17"),  # newest dated mini (no gpt-5.5-mini exists)
        "gemini_flash":      ("google",    "gemini-3.5-flash"),
        "gemini_flash_lite": ("google",    "gemini-3.1-flash-lite"),
    },
}

# Known retirement / window-expiry facts. Filled where we have an authoritative
# date; None means "confirm against provider deprecation page". Claude dates per
# the Anthropic model catalog (cached 2026-05-26).
WINDOW_EXPIRY = {
    # Arm A (deprecation-risk) — confirmed reachable on the *direct* APIs at probe time.
    "claude-opus-4-5-20251101":   "active; no retirement announced (Anthropic catalog)",
    "claude-sonnet-4-5-20250929": "active; no retirement announced (Anthropic catalog)",
    "gpt-4o-2024-11-20":          "served on OpenAI direct API at probe; Azure lifecycle lists 2026-10-01; OpenAI direct-API shutdown unannounced — confirm",
    "gpt-4o-mini-2024-07-18":     "served on OpenAI direct API at probe despite Azure 2026-02-27 retirement (Azure-only); direct-API shutdown unannounced — confirm",
    "gemini-2.5-flash":           "shutdown no earlier than 2026-10-16 (Gemini/Vertex); FLOATING ALIAS, not dated — may be repointed",
    "gemini-2.5-flash-lite":      "shutdown no earlier than 2026-10-16 (Gemini/Vertex); FLOATING ALIAS, not dated — may be repointed",
    # Arm B (current)
    "claude-opus-4-8":            "active (current)",
    "claude-sonnet-4-6":          "active (current)",
    "gpt-5.5-2026-04-23":         "active (current flagship)",
    "gpt-5.4-mini-2026-03-17":    "active (current mini; no gpt-5.5-mini exists)",
    "gemini-3.5-flash":           "active (current)",
    "gemini-3.1-flash-lite":      "active (current)",
}

# Tightest credible Arm-A cliff drives acquisition scheduling.
SCHEDULING_NOTE = ("Acquire Arm A before ~2026-10-16: gemini-2.5-flash/-lite shut down "
                   "no earlier than that date and gpt-4o-2024-11-20 carries an Azure 2026-10-01 "
                   "retirement. Claude 4.5-class has no announced cliff. Arm A gemini slots are "
                   "floating aliases (no dated snapshot exists) and may be repointed before shutdown.")


def _classify(exc) -> str:
    """Map an exception to DEPRECATED (gone) vs ERROR (other)."""
    name = type(exc).__name__
    msg = str(exc).lower()
    if name in ("NotFoundError",) or "not_found" in msg or "404" in msg \
       or "does not exist" in msg or "not found" in msg \
       or "is not available" in msg or "deprecated" in msg or "decommission" in msg:
        return "DEPRECATED"
    return "ERROR"


# ------------------------------------------------------------------
# Provider listings
# ------------------------------------------------------------------
def list_anthropic(client) -> list[str]:
    return sorted(m.id for m in client.models.list(limit=1000))


def list_openai(client) -> list[str]:
    return sorted(m.id for m in client.models.list().data)


def list_google(client) -> list[str]:
    out = []
    for m in client.models.list():
        out.append(m.name.split("/", 1)[-1] if m.name.startswith("models/") else m.name)
    return sorted(out)


# ------------------------------------------------------------------
# 1-token probes
# ------------------------------------------------------------------
def probe_anthropic(client, model_id: str):
    t0 = time.time()
    client.messages.create(model=model_id, max_tokens=1,
                           messages=[{"role": "user", "content": "hi"}])
    return round((time.time() - t0) * 1000)


def probe_openai(client, model_id: str):
    import openai
    msgs = [{"role": "user", "content": "hi"}]
    t0 = time.time()
    try:
        client.chat.completions.create(model=model_id, max_tokens=1, messages=msgs)
    except openai.BadRequestError as e:
        # Reasoning-era models (gpt-5.x): reject `max_tokens`, and a 1-token cap
        # is consumed by reasoning before any output ("output limit reached").
        # Retry with the new param name and a real budget so the call completes.
        m = str(e)
        if any(s in m for s in ("max_completion_tokens", "max_tokens", "output limit", "reached")):
            client.chat.completions.create(
                model=model_id, max_completion_tokens=2000, messages=msgs)
        else:
            raise
    return round((time.time() - t0) * 1000)


def probe_google(client, model_id: str):
    from google.genai import types
    t0 = time.time()
    client.models.generate_content(
        model=model_id, contents="hi",
        config=types.GenerateContentConfig(max_output_tokens=1))
    return round((time.time() - t0) * 1000)


PROBES = {"anthropic": probe_anthropic, "openai": probe_openai, "google": probe_google}
LISTERS = {"anthropic": list_anthropic, "openai": list_openai, "google": list_google}


def resolve_current_gpt(listing: list[str], mini: bool) -> str | None:
    """Newest dated gpt-4o / gpt-4o-mini snapshot from the live listing."""
    import re
    pat = re.compile(r"^gpt-4o-mini-\d{4}-\d{2}-\d{2}$" if mini
                     else r"^gpt-4o-\d{4}-\d{2}-\d{2}$")
    dated = [m for m in listing if pat.match(m)]
    return sorted(dated)[-1] if dated else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slots", default=None,
                    help="comma-separated slot names (dash form), validated against the panel")
    ap.add_argument("--vintage-a", default="v0.17-era")
    ap.add_argument("--vintage-b", default="current")
    ap.add_argument("--emit", default="registries/v0_32_snapshot_resolution.json")
    ap.add_argument("--no-emit", action="store_true")
    args = ap.parse_args()

    # Slot names are documented in dash form (claude-opus); internal keys use
    # underscores (claude_opus). Optionally restrict the panel to --slots.
    if args.slots:
        want = {s.strip().replace("-", "_") for s in args.slots.split(",") if s.strip()}
        unknown = want - set(CANDIDATES["A"])
        if unknown:
            print(f"[error] unknown slots: {sorted(unknown)}; "
                  f"valid: {sorted(CANDIDATES['A'])}")
            return 2
        for arm in CANDIDATES:
            CANDIDATES[arm] = {k: v for k, v in CANDIDATES[arm].items() if k in want}

    import anthropic
    import openai
    from google import genai

    clients = {
        "anthropic": anthropic.Anthropic(),
        "openai":    openai.OpenAI(),
        "google":    genai.Client(
            api_key=os.environ.get("GOOGLE_API_KEY") or os.environ["GEMINI_API_KEY"]),
    }

    # 1) Enumerate live models per provider
    listings: dict[str, list[str]] = {}
    for prov, client in clients.items():
        try:
            listings[prov] = LISTERS[prov](client)
            print(f"[list] {prov}: {len(listings[prov])} models")
        except Exception as e:
            listings[prov] = []
            print(f"[list] {prov}: FAILED — {type(e).__name__}: {e}")

    # 2) Resolve the None placeholders (current GPT snapshots) from the listing
    for mini, slot in ((False, "gpt_4o"), (True, "gpt_4o_mini")):
        if CANDIDATES["B"][slot][1] is None:
            resolved = resolve_current_gpt(listings.get("openai", []), mini)
            CANDIDATES["B"][slot] = ("openai", resolved)
            print(f"[resolve] B/{slot} -> {resolved}")

    # 3) Probe every candidate
    arms: dict[str, dict] = {}
    deprecated_slots: list[str] = []
    for arm, slots in CANDIDATES.items():
        arms[arm] = {}
        for slot, (prov, model_id) in slots.items():
            entry = {"provider": prov, "model_id": model_id,
                     "in_listing": model_id in listings.get(prov, []) if model_id else False,
                     "window_expiry": WINDOW_EXPIRY.get(model_id)}
            if not model_id:
                entry.update(status="UNRESOLVED", detail="no candidate id resolved")
                deprecated_slots.append(f"{arm}/{slot}")
            else:
                try:
                    entry["latency_ms"] = PROBES[prov](clients[prov], model_id)
                    entry["status"] = "REACHABLE"
                except Exception as e:
                    entry["status"] = _classify(e)
                    entry["detail"] = f"{type(e).__name__}: {str(e)[:200]}"
                    if entry["status"] != "REACHABLE":
                        deprecated_slots.append(f"{arm}/{slot}")
            arms[arm][slot] = entry
            print(f"  {arm}/{slot:18s} {str(model_id):32s} -> {entry['status']}"
                  + (f"  ({entry.get('latency_ms')}ms)" if entry.get("latency_ms") else ""))

    viable = len(deprecated_slots) == 0
    result = {
        "phase": "v0.32",
        "probed_at": datetime.now(timezone.utc).isoformat(),
        "vintages": {"A": args.vintage_a, "B": args.vintage_b},
        "arms": arms,
        "provider_listings": listings,
        "verdict": {"viable_cell_set": viable, "unreachable_slots": deprecated_slots},
        "scheduling_note": SCHEDULING_NOTE,
    }

    print("\n=== VERDICT ===")
    print(f"viable cell set: {viable}")
    if deprecated_slots:
        print(f"unreachable: {', '.join(deprecated_slots)}")

    if not args.no_emit:
        with open(args.emit, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nwrote {args.emit}")
    return 0 if viable else 2


if __name__ == "__main__":
    sys.exit(main())
