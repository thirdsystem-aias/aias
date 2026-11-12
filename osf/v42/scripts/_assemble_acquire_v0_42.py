#!/usr/bin/env python3
"""Build osf/v42/scripts/acquire_v0_42.py: verbatim current-arm blocks from v0.39 (git show) +
v0.42 wrapper. Edits to the copied call functions: an optional `system` argument, and (clarification C28,
2026-11-11) the conservative billing fields `billed_searches` (OpenAI, Google) and `tokens_tool_prompt` (Google)."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
src = subprocess.run(["git", "show", "v0.39:osf/v39/scripts/acquire_v0_39.py"], cwd=ROOT,
                     capture_output=True, text=True, check=True).stdout.split("\n")


def block(start_marker, end_marker):
    s = next(i for i, l in enumerate(src) if l.startswith(start_marker))
    e = next(i for i, l in enumerate(src) if i > s and l.startswith(end_marker))
    return src[s:e]


consts = [l for l in block("# S1 tool configurations", "class Transient") if not l.startswith("LEGACY_MAX_TOKENS")]
helpers = block("class Transient", "# ======================= legacy arm")
current = block("# ======================= current arm", "LEGACY_DISPATCH")
retry = block("def _now", "def cells")


def patch(lines, old, new):
    txt = "\n".join(lines)
    assert txt.count(old) == 1, old
    return txt.replace(old, new).split("\n")


for prov, cond_line, put in (
    ("anthropic", '    if search:\n        kw["tools"] = [S1_ANTHROPIC]', '    if system:\n        kw["system"] = system\n'),
    ("openai", '    if search:\n        kw["tools"] = [S1_OPENAI]', '    if system:\n        kw["instructions"] = system\n'),
    ("google", '    if search:\n        cfg["tools"]', '    if system:\n        cfg["system_instruction"] = system\n'),
):
    current = patch(current, f"def call_{prov}_current(model_id, prompt, search):",
                    f"def call_{prov}_current(model_id, prompt, search, system=None):")
    current = patch(current, cond_line, put + cond_line)

# Clarification C28 (2026-11-11): conservative billing fields; the only other edits to the copied functions.
# OpenAI: every web_search_call output item (search, open_page, find_in_page, any other action) is a billed tool call.
current = patch(current, "    s = _empty_search()\n    for item in (r.output or []):",
                "    s = _empty_search()\n    n_calls = 0                 # C28: web_search_call items (billed tool calls)\n"
                "    for item in (r.output or []):")
current = patch(current, '        if d.get("type") == "web_search_call":\n            a = d.get("action") or {}',
                '        if d.get("type") == "web_search_call":\n            n_calls += 1\n            a = d.get("action") or {}')
current = patch(current, '"tokens_thought": getattr(det, "reasoning_tokens", None) if det is not None else None,\n'
                         '            "paused_continued": False,',
                '"tokens_thought": getattr(det, "reasoning_tokens", None) if det is not None else None,\n'
                '            "billed_searches": n_calls,\n            "paused_continued": False,')
# Google: tool_use_prompt_token_count (search-result tokens fed to the model) recorded and priced as input; a grounded
# answer with web chunks but no recorded query is billed as one query.
current = patch(current, '"tokens_thought": getattr(um, "thoughts_token_count", None),\n            "paused_continued": False,',
                '"tokens_thought": getattr(um, "thoughts_token_count", None),\n'
                '            "tokens_tool_prompt": getattr(um, "tool_use_prompt_token_count", None),\n'
                '            "billed_searches": max(s["n_searches"], 1 if s["sources"] else 0),\n'
                '            "paused_continued": False,')

head = (HERE / "_acquire_head.py.txt").read_text()
tail = (HERE / "_acquire_tail.py.txt").read_text()
out = head + "\n".join(consts) + "\n\n" + "\n".join(helpers) + "\n" + "\n".join(current) + "\n" + "\n".join(retry) + "\n" + tail
(HERE / "acquire_v0_42.py").write_text(out, encoding="utf-8")
print("wrote", HERE / "acquire_v0_42.py", len(out.split("\n")), "lines")
