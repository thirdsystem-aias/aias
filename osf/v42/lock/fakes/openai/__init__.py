"""LOCAL FAKE of the `openai` SDK (rehearsal only): OpenAI().responses.create. No network; every request is billed
to the fake bill (_fakecore)."""
from types import SimpleNamespace as NS

import _fakecore as F


class APIError(Exception):
    pass


class RateLimitError(APIError):
    pass


class APIConnectionError(APIError):
    pass


class APITimeoutError(APIError):
    pass


class APIStatusError(APIError):
    status_code = 400


class _Responses:
    def create(self, **kw):
        for k in ("temperature", "top_p", "reasoning"):
            assert k not in kw, f"{k} sent"
        cond = "S1" if kw.get("tools") else "S0"
        if cond == "S1":
            assert kw["tools"][0]["type"] == "web_search" and kw.get("include") == ["web_search_call.action.sources"]
        tin, tout, think, n = F.tokens("openai", cond)
        F.bill("openai", kw["model"], "standard", tin, tout, think, n)
        output = [{"type": "web_search_call", "action": {"type": "search", "query": f"query {i}",
                                                         "sources": [{"url": f"https://source{i}.example/", "title": f"S{i}"}]}}
                  for i in range(n)]
        output.append({"type": "message", "content": [{"type": "output_text", "text": "x", "annotations": (
            [{"type": "url_citation", "url": "https://source0.example/", "title": "S0"}] if n else [])}]})
        return NS(output=output, output_text=f"Fake answer to: {kw['input'][:60]}", model=kw["model"],
                  status="completed", incomplete_details=None,
                  usage=NS(input_tokens=tin, output_tokens=tout, output_tokens_details=NS(reasoning_tokens=think)))


class OpenAI:
    def __init__(self, *a, **kw):
        self.responses = _Responses()
