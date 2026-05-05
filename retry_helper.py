"""
AIAS — Retry helper.
Wraps API calls with retry logic for transient errors and rate limits.
"""
import time
import re

# How long to wait between retries (seconds), per attempt
BACKOFF_SCHEDULE = [2, 5, 15]  # 1st retry after 2s, 2nd after 5s, 3rd after 15s
MAX_ATTEMPTS = len(BACKOFF_SCHEDULE) + 1  # 1 initial + 3 retries = 4 total


def is_rate_limit_error(exc):
    """Detect 429-style rate-limit errors across all three providers."""
    msg = str(exc).lower()
    if "429" in msg: return True
    if "rate" in msg and "limit" in msg: return True
    if "resource_exhausted" in msg: return True
    if "quota" in msg: return True
    return False


def is_transient_error(exc):
    """Detect retryable server-side issues (5xx, timeouts, network)."""
    msg = str(exc).lower()
    if "503" in msg: return True
    if "502" in msg: return True
    if "504" in msg: return True
    if "unavailable" in msg: return True
    if "timeout" in msg or "timed out" in msg: return True
    if "connection" in msg: return True
    return False


def is_hard_error(exc):
    """Errors that should not be retried."""
    msg = str(exc).lower()
    if "401" in msg or "authentication" in msg: return True
    if "403" in msg or "permission_denied" in msg: return True
    if "404" in msg or "model_not_found" in msg: return True
    if "invalid_api_key" in msg: return True
    return False


def parse_retry_after(exc):
    """Extract provider-specified retry delay from error messages. Returns seconds (float) or None."""
    msg = str(exc)
    # Google format: "Please retry in 41.41s"
    m = re.search(r"retry in ([\d.]+)s", msg, re.IGNORECASE)
    if m:
        return float(m.group(1))
    # OpenAI/Anthropic Retry-After header style
    m = re.search(r"retry[- ]after[:\s]+(\d+)", msg, re.IGNORECASE)
    if m:
        return float(m.group(1))
    return None


def retry_call(fn, *args, **kwargs):
    """
    Calls fn(*args, **kwargs) with retry logic.
    Returns (result, status, attempts) where:
      - result: the function's return value, or None on final failure
      - status: "ok", "rate_limit_final", "transient_final", "hard_error"
      - attempts: how many tries it took
    """
    last_exc = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            result = fn(*args, **kwargs)
            return result, "ok", attempt + 1
        except Exception as e:
            last_exc = e

            if is_hard_error(e):
                return None, "hard_error", attempt + 1

            if attempt >= MAX_ATTEMPTS - 1:
                # final attempt failed
                if is_rate_limit_error(e):
                    return None, "rate_limit_final", attempt + 1
                return None, "transient_final", attempt + 1

            # Decide wait time
            if is_rate_limit_error(e):
                provider_wait = parse_retry_after(e)
                if provider_wait is not None:
                    wait = min(provider_wait + 1, 60)  # cap at 60s
                else:
                    wait = BACKOFF_SCHEDULE[attempt]
            elif is_transient_error(e):
                wait = BACKOFF_SCHEDULE[attempt]
            else:
                # unknown error type — retry briefly
                wait = BACKOFF_SCHEDULE[attempt]

            time.sleep(wait)

    return None, "transient_final", MAX_ATTEMPTS
