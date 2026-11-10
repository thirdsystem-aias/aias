"""LOCAL FAKE of the `anthropic` SDK (rehearsal only): messages.create and messages.batches.{create,retrieve,results}.
No network. Every processed request is written to the fake bill (_fakecore)."""
import json
import os
import time
from datetime import datetime, timezone
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


def _build(params):
    for k in ("temperature", "top_p", "top_k"):
        assert k not in params, f"{k} sent to {params['model']}"
    if params.get("tools"):
        assert params["tools"][0]["type"] == "web_search_20250305", params["tools"]
    cond = "S1" if params.get("tools") else "S0"
    tin, tout, _, n = F.tokens("anthropic", cond)
    blocks = []
    for i in range(n):
        blocks.append(NS(type="server_tool_use", name="web_search", input={"query": f"query {i}"}))
        blocks.append(NS(type="web_search_tool_result",
                         content=[NS(url=f"https://source{i}.example/", title=f"S{i}", page_age=None)]))
    blocks.append(NS(type="text", text=f"Fake answer to: {params['messages'][0]['content'][:60]}",
                     citations=[NS(url="https://source0.example/", title="S0")] if n else None))
    msg = NS(content=blocks, stop_reason="end_turn", model=params["model"], usage=NS(input_tokens=tin, output_tokens=tout))
    return msg, (tin, tout, n)


def _billed(params, mode):
    msg, (tin, tout, n) = _build(params)
    F.bill("anthropic", params["model"], mode, tin, tout, None, n)
    return msg


class _Batches:
    def create(self, requests):
        bid = F.next_id("msgbatch")
        (F.STATE / "batches").mkdir(exist_ok=True)
        for r in requests:                       # the provider processes (and bills) every request it accepted
            _billed(r["params"], "batch")
        (F.STATE / "batches" / f"{bid}.json").write_text(json.dumps({"created": time.time(), "requests": requests}))
        return NS(id=bid, processing_status="in_progress")

    def _load(self, bid):
        return json.loads((F.STATE / "batches" / f"{bid}.json").read_text())

    def retrieve(self, bid):
        d = self._load(bid)
        ended = time.time() - d["created"] >= float(os.environ.get("FAKE_BATCH_SECONDS", "0"))
        return NS(id=bid, processing_status="ended" if ended else "in_progress",
                  ended_at=datetime.now(timezone.utc) if ended else None)

    def results(self, bid):
        return [NS(custom_id=r["custom_id"], result=NS(type="succeeded", message=_build(r["params"])[0]))
                for r in self._load(bid)["requests"]]


class _Messages:
    def __init__(self):
        self.batches = _Batches()

    def create(self, **kw):
        return _billed(kw, "standard")


class Anthropic:
    def __init__(self, *a, **kw):
        self.messages = _Messages()
