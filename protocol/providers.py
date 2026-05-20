"""
protocol/providers.py — frontier-model provider abstraction

Single dispatch point for the 6-slot reference panel. All three providers
(Anthropic, OpenAI, Google) live behind one route_call() interface.

ONE-TIME LIFT: This file is the consolidation point for whatever provider
API client code currently lives in your v17 acquisition scripts. After
you port it here once, every future phase (v0.19, v0.20, ...) imports
from this module and never needs the lift again.

Lift instructions:
  1. Open scripts/acquire_phase_a_v17.py
  2. Find the function(s) that send prompts to Anthropic / OpenAI / Google
  3. Copy the implementation body into call_anthropic / call_openai /
     call_google below, conforming to the return-shape contract.
  4. Auth: keep using ANTHROPIC_API_KEY / OPENAI_API_KEY /
     GOOGLE_API_KEY environment variables (or whatever pattern v17 uses).
  5. Retry/backoff: lift any retry decorators or wrapper logic.
"""

from typing import TypedDict


class ProviderResponse(TypedDict):
    """Return-shape contract that all provider functions must satisfy."""
    raw_response: str       # model's text output
    tokens_in: int          # prompt tokens consumed
    tokens_out: int         # completion tokens generated
    latency_ms: int         # round-trip latency
    model: str              # the model identifier echoed back
    finish_reason: str      # "stop" | "length" | "error" | ...


def call_anthropic(model: str, prompt: str) -> ProviderResponse:
    """
    Call an Anthropic Claude model.

    Models in current 6-slot panel:
      - claude-opus-4-5
      - claude-sonnet-4-5

    [ONE-TIME LIFT from scripts/acquire_phase_a_v17.py]
    """
    raise NotImplementedError(
        "ONE-TIME LIFT: Copy the Anthropic API-client body from your "
        "v17 acquisition script's probe function. Must return a "
        "ProviderResponse-shaped dict."
    )


def call_openai(model: str, prompt: str) -> ProviderResponse:
    """
    Call an OpenAI GPT model.

    Models in current 6-slot panel:
      - gpt-4o
      - gpt-4o-mini

    [ONE-TIME LIFT from scripts/acquire_phase_a_v17.py]
    """
    raise NotImplementedError(
        "ONE-TIME LIFT: Copy the OpenAI API-client body from your "
        "v17 acquisition script. Must return a ProviderResponse-shaped dict."
    )


def call_google(model: str, prompt: str) -> ProviderResponse:
    """
    Call a Google Gemini model.

    Models in current 6-slot panel:
      - gemini-2.5-flash
      - gemini-2.5-flash-lite

    [ONE-TIME LIFT from scripts/acquire_phase_a_v17.py]
    """
    raise NotImplementedError(
        "ONE-TIME LIFT: Copy the Google API-client body from your "
        "v17 acquisition script. Must return a ProviderResponse-shaped dict."
    )


def route_call(model: str, prompt: str) -> ProviderResponse:
    """
    Dispatch a prompt to the appropriate provider based on model identifier.
    This is the function every higher-level protocol layer calls.

    All phase scripts use route_call() — they never touch the individual
    provider functions directly. That keeps the dispatch logic in one place.
    """
    if model.startswith("claude-"):
        return call_anthropic(model, prompt)
    if model.startswith("gpt-"):
        return call_openai(model, prompt)
    if model.startswith("gemini-"):
        return call_google(model, prompt)
    raise ValueError(f"Unrouted model identifier: {model}")
