#!/usr/bin/env python3
"""
token_count_v1_11.py - AIAS v1.11: offline token count of every judge request (no model call, no
network after the tokenizer file is cached, no valence). PRE_REGISTRATION_v1_11.md section 7.

Counts, for every judged unit of the frozen U0 unit table, the tokens of the exact judge request
(SYSTEM_PROMPT + the filled USER_TEMPLATE, built by score_v1_11.build_request) with the open
o200k_base tokenizer (tiktoken), and the tokens of a maximal valid JSON reply. No vendor publishes
an offline tokenizer for Claude Opus 5.5 or GPT-6.1 Sol: o200k_base is the measurement, and the
pre-registration applies a fixed planning factor per vendor (section 7). Writes
prereg/token_counts_v1_11.json. Needs numpy and tiktoken (any Python 3.10+):

    python3 -m venv /tmp/v111tok && /tmp/v111tok/bin/pip install tiktoken numpy
    /tmp/v111tok/bin/python osf/methodology/v1_11/scoping/token_count_v1_11.py
"""
import hashlib
import json
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_11 as S  # noqa: E402
import tiktoken  # noqa: E402

ENC = "o200k_base"


def main() -> int:
    enc = tiktoken.get_encoding(ENC)
    units_path = S.PREREG_DIR / S.UNITS_NAME
    u0 = json.loads((S.PREREG_DIR / S.U0_NAME).read_text(encoding="utf-8"))
    sha = hashlib.sha256(units_path.read_bytes()).hexdigest()
    if sha != u0["units_file"]["sha256"]:
        sys.exit("ABORT: the unit table differs from the U0 record")
    units = [u for u in S.read_units(units_path) if u["judged"]]
    n = lambda s: len(enc.encode(s, disallowed_special=()))  # noqa: E731
    sys_tok = n(S.SYSTEM_PROMPT)
    head, tail = S.USER_TEMPLATE.split("{text}")
    fixed_tail = tail                                   # the rules, scale and reply format (after the text)
    per = defaultdict(list)
    chars = defaultdict(int)
    role_tok = defaultdict(int)
    for u in units:
        r = S.build_request(u)
        t = sys_tok + n(r["user"])
        per[u["block"]].append(t)
        chars[u["block"]] += u["request_chars"]
        role_tok["J1 main"] += t
        if u["j2"]:
            role_tok["J2 main"] += t
        if u["selfcon"]:
            role_tok["J1 repeat"] += t
            if u["j2"]:
                role_tok["J2 repeat"] += t
    reply = json.dumps({"refers_to_brand": True, "evaluative": True, "mixed": False, "valence": 1,
                        "evidence": " ".join(["exceptional"] * S.EVIDENCE_MAX_WORDS)})
    reply_typ = json.dumps({"refers_to_brand": True, "evaluative": True, "mixed": False, "valence": 1,
                            "evidence": "smooth, reliable, great value"})
    allt = [t for v in per.values() for t in v]
    doc = {
        "phase": S.PHASE_ID, "kind": "offline token count of the judge requests (no model call)",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tokenizer": f"tiktoken {tiktoken.__version__} {ENC}", "units_sha256": sha,
        "system_prompt_tokens": sys_tok, "user_template_fixed_tokens": n(head.format(
            brand="", category="", question="", text_type="")) + n(fixed_tail),
        "rules_after_text_tokens": n(fixed_tail),
        "reply_tokens": {"maximal_valid": n(reply), "typical": n(reply_typ)},
        "by_block": {b: {"units": len(v), "tokens_total": sum(v), "tokens_mean": round(sum(v) / len(v), 1),
                         "tokens_median": statistics.median(v), "tokens_max": max(v),
                         "request_chars_total": chars[b], "chars_per_token": round(chars[b] / sum(v), 3)}
                     for b, v in sorted(per.items())},
        "judged_units": len(allt), "tokens_total": sum(allt),
        "tokens_by_role": dict(role_tok),
        "chars_per_token_all": round(sum(chars.values()) / sum(allt), 3),
    }
    out = S.PREREG_DIR / "token_counts_v1_11.json"
    out.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(doc, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
