"""
protocol/probe.py — canonical probe functions for Phase A and Phase B

Phase A: probe_brand() sends a Recognition (C_P) probe to a single model.
Phase B: probe_frame() sends a category-anchored query to a single model.

Both functions wrap route_call() with phase-specific prompt templates and
response-parsing logic. Phase scripts call these — they don't reimplement.

The C_P probe template is the canonical v1.4 wording. If the template
needs to change, that's a protocol-version bump (v1.5+) and a coordinated
update across this file + protocol/__init__.py.
"""

from .providers import route_call, ProviderResponse


# ============================================================
# Phase A — Recognition (C_P) probe
# ============================================================

C_P_PROBE_TEMPLATE = (
    "Is the brand \"{brand}\" commonly recognized as a {category}? "
    "Answer with exactly one word: yes or no."
)


def probe_brand(brand: str, model: str, category: str) -> dict:
    """
    Send the v1.4 C_P probe for `brand` to `model` in the context of
    `category`. Returns parsed recognition outcome plus raw response.

    Returns:
        {
            "brand": str,
            "model": str,
            "category": str,
            "prompt": str,
            "raw_response": str,
            "recognized": bool,
            "tokens_in": int,
            "tokens_out": int,
            "latency_ms": int,
        }
    """
    prompt = C_P_PROBE_TEMPLATE.format(brand=brand, category=category)
    response: ProviderResponse = route_call(model, prompt)
    recognized = _parse_yes_no(response["raw_response"])
    return {
        "brand": brand,
        "model": model,
        "category": category,
        "prompt": prompt,
        "raw_response": response["raw_response"],
        "recognized": recognized,
        "tokens_in": response["tokens_in"],
        "tokens_out": response["tokens_out"],
        "latency_ms": response["latency_ms"],
    }


def _parse_yes_no(text: str) -> bool:
    """
    Canonical yes/no parser for C_P probe responses.

    Rule (v1.4): True if the first content word is "yes" (case-insensitive,
    punctuation-stripped). False otherwise. Refusals, equivocations, and
    "I don't know" all parse to False.
    """
    if not text:
        return False
    first_word = text.strip().lower().lstrip(".,!?;:\"'(*-").split()[:1]
    if not first_word:
        return False
    return first_word[0].rstrip(".,!?;:\"')*-") == "yes"


# ============================================================
# Phase B — Recall (three-frame battery)
# ============================================================

def probe_frame(frame_query: str, model: str) -> dict:
    """
    Send a category-anchored frame query (e.g. "What are the best niche
    fragrances?") to a model. Returns the raw response for downstream
    brand-mention parsing.

    Returns:
        {
            "model": str,
            "frame_query": str,
            "raw_response": str,
            "tokens_in": int,
            "tokens_out": int,
            "latency_ms": int,
        }
    """
    response: ProviderResponse = route_call(model, frame_query)
    return {
        "model": model,
        "frame_query": frame_query,
        "raw_response": response["raw_response"],
        "tokens_in": response["tokens_in"],
        "tokens_out": response["tokens_out"],
        "latency_ms": response["latency_ms"],
    }
