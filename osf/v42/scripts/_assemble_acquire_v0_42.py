#!/usr/bin/env python3
"""Build osf/v42/scripts/acquire_v0_42.py: verbatim current-arm blocks from v0.39 (git show) +
v0.42 wrapper. Only edit to the copied call functions: an optional `system` argument."""
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

head = (HERE / "_acquire_head.py.txt").read_text()
tail = (HERE / "_acquire_tail.py.txt").read_text()
out = head + "\n".join(consts) + "\n\n" + "\n".join(helpers) + "\n" + "\n".join(current) + "\n" + "\n".join(retry) + "\n" + tail
(HERE / "acquire_v0_42.py").write_text(out, encoding="utf-8")
print("wrote", HERE / "acquire_v0_42.py", len(out.split("\n")), "lines")
