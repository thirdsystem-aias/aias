"""LOCAL FAKE of `google.genai` (rehearsal only): Client(api_key).models.generate_content. No network; every request
is billed to the fake bill (_fakecore)."""
from types import SimpleNamespace as NS

import _fakecore as F

from . import errors, types  # noqa: F401


class _Models:
    def generate_content(self, model, contents, config):
        tools = getattr(config, "tools", None)
        for k in ("temperature", "top_p", "top_k", "thinking_config"):
            assert getattr(config, k, None) is None, f"{k} sent"
        cond = "S1" if tools else "S0"
        tin, tout, think, n = F.tokens("google", cond)
        F.bill("google", model, "standard", tin, tout, think, n)
        gm = None
        if n:
            gm = NS(web_search_queries=[f"query {i}" for i in range(n)],
                    grounding_chunks=[NS(web=NS(uri=f"https://vertexaisearch.example/{i}", title=f"source{i}.example"))
                                      for i in range(n)],
                    grounding_supports=[NS(grounding_chunk_indices=[0])])
        return NS(candidates=[NS(finish_reason="FinishReason.STOP", grounding_metadata=gm)],
                  usage_metadata=NS(prompt_token_count=tin, candidates_token_count=tout, thoughts_token_count=think),
                  text=f"Fake answer to: {contents[:60]}", model_version=model)


class Client:
    def __init__(self, api_key=None, **kw):
        assert api_key, "no api key"
        self.models = _Models()
