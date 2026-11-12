"""Adversarial fake provider SDKs for the pre-lock dry run (no network). A PLAN maps
(model, prompt, cond) -> list of attempt dicts consumed in order (one per billed request)."""
import sys
import types
from datetime import datetime, timezone
from types import SimpleNamespace as NS

PLAN = {}          # (model, prompt, cond) -> [attempt, ...]
LOG = []           # every request served: (provider, model, cond, kind)
BILL = []          # independent bill: (model, tin, tout, think) of every request that returned usage


def take(model, prompt, cond):
    q = PLAN.get((model, prompt, cond))
    if not q:
        raise AssertionError(f"no planned attempt for {model} {cond} {prompt[:50]}")
    a = q.pop(0)
    LOG.append((model, cond, a["kind"]))
    return a


# ----------------------------------------------------------------------------- anthropic
anthropic = types.ModuleType("anthropic")


class _AErr(Exception):
    status_code = 400


for _n in ("RateLimitError", "APIConnectionError", "APITimeoutError", "APIStatusError"):
    setattr(anthropic, _n, type(_n, (_AErr,), {}))


def _a_message(model, a, cond):
    blocks = []
    if cond == "S1":
        for q in a.get("queries", []):
            blocks.append(NS(type="server_tool_use", name="web_search", input={"query": q}))
        if a.get("search_error"):
            blocks.append(NS(type="web_search_tool_result", content=NS(type="web_search_tool_result_error",
                                                                         error_code=a["search_error"])))
        if a.get("sources"):
            blocks.append(NS(type="web_search_tool_result",
                             content=[NS(type="web_search_result", url=s["url"], title=s.get("title"),
                                         page_age="2 days ago", encrypted_content="x") for s in a["sources"]]))
    text = a.get("text", "")
    if text:
        # split the answer into two text blocks; the second carries citations (web_search_result_location)
        h = len(text) // 2
        blocks.append(NS(type="text", text=text[:h], citations=None))
        cits = [NS(type="web_search_result_location", url=c["url"], title=c.get("title"), cited_text="...",
                   encrypted_index="x") for c in a.get("citations", [])]
        blocks.append(NS(type="text", text=text[h:], citations=cits or None))
    stop = {"refusal": "refusal", "trunc": "max_tokens", "tool_use_empty": "tool_use",
            "pause": "pause_turn"}.get(a["kind"], "end_turn")
    u = NS(input_tokens=a.get("tin", 40 if cond == "S0" else 9000), output_tokens=a.get("tout", 600))
    BILL.append((model, u.input_tokens, u.output_tokens, None))
    return NS(content=blocks, stop_reason=stop, model=a.get("served", model), usage=u)


class _AMessages:
    def __init__(self):
        self.batches = _ABatches()

    def create(self, model, messages, max_tokens, **kw):
        assert not ({"temperature", "top_p", "top_k"} & set(kw)), kw
        cond = "S1" if kw.get("tools") else "S0"
        prompt = messages[0]["content"]
        a = take(model, prompt, cond)
        if a["kind"] == "transient":
            raise anthropic.RateLimitError("429 fake")
        if a["kind"] == "fatal":
            e = anthropic.APIStatusError("400 fake invalid request")
            raise e
        if a["kind"] == "timeout":
            raise anthropic.APITimeoutError("Request timed out (fake)")
        return _a_message(model, a, cond)


class _ABatches:
    def __init__(self):
        self.store, self.n = {}, 0

    def create(self, requests):
        self.n += 1
        bid = f"msgbatch_fake_{self.n:03d}"
        res = []
        for r in requests:
            p = r["params"]
            assert not ({"temperature", "top_p", "top_k"} & set(p)), p
            cond = "S1" if p.get("tools") else "S0"
            a = take(p["model"], p["messages"][0]["content"], cond)
            if a["kind"] == "expired":
                result = NS(type="expired")
            elif a["kind"] == "errored_transient":
                result = NS(type="errored", error=NS(type="error", error=NS(type="overloaded_error", message="x")))
            elif a["kind"] == "errored_fatal":
                result = NS(type="errored", error=NS(type="error", error=NS(type="invalid_request_error", message="x")))
            else:
                result = NS(type="succeeded", message=_a_message(p["model"], a, cond))
            res.append(NS(custom_id=r["custom_id"], result=result))
        self.store[bid] = res
        return NS(id=bid, processing_status="in_progress")

    def retrieve(self, bid):
        return NS(id=bid, processing_status="ended", ended_at=datetime.now(timezone.utc))

    def results(self, bid):
        return list(self.store[bid])


class Anthropic:
    _shared = None

    def __init__(self, *a, **kw):
        if Anthropic._shared is None:
            Anthropic._shared = _AMessages()
        self.messages = Anthropic._shared


anthropic.Anthropic = Anthropic


# ----------------------------------------------------------------------------- openai
openai = types.ModuleType("openai")


class _OErr(Exception):
    status_code = 400


for _n in ("RateLimitError", "APIConnectionError", "APITimeoutError", "APIStatusError"):
    setattr(openai, _n, type(_n, (_OErr,), {}))


class _Item(dict):
    """dict item with model_dump (as the SDK's pydantic objects)."""
    def model_dump(self):
        return dict(self)


class _OResponses:
    def create(self, model, input, max_output_tokens, **kw):
        assert not ({"temperature", "top_p", "reasoning"} & set(kw)), kw
        cond = "S1" if kw.get("tools") else "S0"
        if cond == "S1":
            assert kw.get("include") == ["web_search_call.action.sources"], kw
        a = take(model, input, cond)
        if a["kind"] == "transient":
            raise openai.RateLimitError("429 fake")
        if a["kind"] == "fatal":
            raise openai.APIStatusError("400 fake")
        out = [_Item(type="reasoning", id="rs_1", summary=[])]
        if cond == "S1":
            for i, q in enumerate(a.get("queries", [])):
                srcs = a.get("sources", []) if i == 0 else []
                out.append(_Item(type="web_search_call", id=f"ws_{i}", status="completed",
                                 action={"type": "search", "query": q,
                                         "sources": [({"type": "url", "url": s["url"]} if s.get("url")
                                                      else {"type": "api", "name": "oai-sports"}) for s in srcs]}))
            for u in a.get("open_pages", []):
                out.append(_Item(type="web_search_call", id="ws_open", status="completed",
                                 action={"type": "open_page", "url": u}))
        if a["kind"] == "refusal":
            out.append(_Item(type="message", role="assistant",
                             content=[{"type": "refusal", "refusal": "I can't help with that."}]))
            text = ""
        else:
            text = a.get("text", "")
            anns = [{"type": "url_citation", "start_index": 0, "end_index": 5, "url": c["url"], "title": c.get("title")}
                    for c in a.get("citations", [])]
            out.append(_Item(type="message", role="assistant",
                             content=[{"type": "output_text", "text": text, "annotations": anns}]))
        trunc = a["kind"] == "trunc"
        BILL.append((model, a.get("tin", 30 if cond == "S0" else 12000), a.get("tout", 700), a.get("think", 200)))
        return NS(output=out, output_text=text, model=a.get("served", model),
                  status="incomplete" if trunc else "completed",
                  incomplete_details=NS(reason="max_output_tokens") if trunc else None,
                  usage=NS(input_tokens=a.get("tin", 30 if cond == "S0" else 12000), output_tokens=a.get("tout", 700),
                           output_tokens_details=NS(reasoning_tokens=a.get("think", 200))))


class OpenAI:
    def __init__(self, *a, **kw):
        self.responses = _OResponses()


openai.OpenAI = OpenAI

# ----------------------------------------------------------------------------- google.genai
google = types.ModuleType("google")
genai = types.ModuleType("google.genai")
gerrors = types.ModuleType("google.genai.errors")
gtypes = types.ModuleType("google.genai.types")


class ServerError(Exception):
    code = 500


class ClientError(Exception):
    def __init__(self, msg, code=400):
        super().__init__(msg)
        self.code = code


gerrors.ServerError, gerrors.ClientError = ServerError, ClientError
gtypes.Tool = lambda **kw: NS(**kw)
gtypes.GoogleSearch = lambda **kw: NS(**kw)
gtypes.GenerateContentConfig = lambda **kw: NS(**kw)


class _FR(str):
    """str(enum) of google-genai's FinishReason prints 'FinishReason.X' (feasibility record)."""
    def __str__(self):
        return "FinishReason." + str.__str__(self)


class _GModels:
    def generate_content(self, model, contents, config):
        for k in ("temperature", "top_p", "top_k", "thinking_config"):
            assert getattr(config, k, None) is None, k
        cond = "S1" if getattr(config, "tools", None) else "S0"
        a = take(model, contents, cond)
        if a["kind"] == "transient":
            raise ServerError("503 fake")
        if a["kind"] == "fatal":
            raise ClientError("400 fake", 400)
        gm = None
        if cond == "S1" and (a.get("queries") or a.get("sources")):
            chunks = [NS(web=NS(uri=s["url"], title=s.get("title")), retrieved_context=None) for s in a.get("sources", [])]
            chunks.append(NS(web=None, retrieved_context=NS(uri="x")))          # a non-web chunk
            sup = [NS(grounding_chunk_indices=ix) for ix in a.get("supports", [[0]] if chunks[:-1] else [])]
            gm = NS(web_search_queries=a.get("queries", []), grounding_chunks=chunks, grounding_supports=sup)
        fr = {"refusal": "SAFETY", "trunc": "MAX_TOKENS", "empty": "STOP"}.get(a["kind"], "STOP")
        text = "" if a["kind"] == "refusal" else a.get("text", "")
        cands = [NS(finish_reason=_FR(fr), grounding_metadata=gm)]
        BILL.append((model, a.get("tin", 40), a.get("tout", 900), a.get("think", 300)))
        return NS(candidates=cands, text=text or None, model_version=a.get("served", model),
                  usage_metadata=NS(prompt_token_count=a.get("tin", 40), candidates_token_count=a.get("tout", 900),
                                    thoughts_token_count=a.get("think", 300)))


class Client:
    def __init__(self, api_key=None, **kw):
        assert api_key
        self.models = _GModels()


genai.Client, genai.errors, genai.types = Client, gerrors, gtypes
google.genai = genai


def install():
    sys.modules.update({"anthropic": anthropic, "openai": openai, "google": google, "google.genai": genai,
                        "google.genai.errors": gerrors, "google.genai.types": gtypes})
