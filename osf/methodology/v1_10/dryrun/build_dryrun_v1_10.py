#!/usr/bin/env python3
"""Builds SYNTHETIC replicas of every v1.10 input format under dryrun/replica/ (same
relative paths, same columns / keys as the frozen files) plus the dry-run manifest
dryrun/INPUTS_MANIFEST_dryrun_v1_10.json, so that

    python3 scripts/score_v1_10.py --stage S --dry-run
    python3 scripts/score_v1_10.py --stage C --dry-run

run the whole pipeline end to end without reading any real answer file.

Synthetic: every answer file (OMNI v0.19 jsonl, v0.20-v0.22 / v0.28 / v0.32 csv, v0.23
json, the run_aias_v2 csv variants of EARLY-6 and EARLY-2), the coded mention files
(v0.19 csv, v0.23 scored json, produced by re-implementations of the phase coders), the
Presence/Consistency table (random P / C*), the v0.41 verdict stub (S6) and a COI flag
file (S7). Copied byte for byte (no answers in them): the registries, the certified
detector scripts and the prompt files. Answer texts name registry brands in numbered
lists, bullets, headings, bold runs and prose, with nested sub-bullets, comparison
mentions, intro / closing mentions, repeats, aliases and unregistered names; brand
order follows latent per-category propensities, so the replica has real structure
(stable across waves and halves) for every statistic to act on.

Run: python3 osf/methodology/v1_10/dryrun/build_dryrun_v1_10.py [--out DIR] [--seed N]
"""
import argparse
import csv
import hashlib
import io
import json
import random
import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
import score_v1_10 as S  # noqa: E402

LEGACY = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini", "gemini-2.5-flash",
          "gemini-2.5-flash-lite"]
EARLY = [("anthropic_sonnet", "anthropic", "claude-sonnet-4-6"), ("anthropic_opus", "anthropic", "claude-opus-4-7"),
         ("openai_mini", "openai", "gpt-5.4-mini"), ("openai_flagship", "openai", "gpt-5.5"),
         ("google_flash", "google", "gemini-2.5-flash"), ("xai_grok", "xai", "grok-4-1-fast")]
PROMPTS6 = [("p1_functional", "FUNCTIONAL_WHY"), ("p2_contextual", "CONTEXTUAL_WHEN"),
            ("p3_constraint", "CONSTRAINT_WITH"), ("p4_identity", "IDENTITY_HOW_FEELING"),
            ("p5_discovery", "DISCOVERY"), ("p6_comparison", "COMPARISON")]
KK_PROMPTS = ([(f"knives_b1_en_0{i}", "GENERAL_RECOMMENDATION") for i in range(1, 5)]
              + [(f"knives_b2_en_0{i}", "USE_CASE_RECOMMENDATION") for i in range(1, 5)]
              + [(f"knives_b3_en_{x}", "TRADITION_ANCHORED") for x in ("de", "fr", "jp")])
FRAMES = [("q1", "R_cat"), ("q2", "R_cat"), ("q3", "R_cat"), ("q4", "R_cult"), ("q5", "R_cult"), ("q6", "R_cult")]
V19_FRAMES = ["q1_audiophile", "q2_enthusiast", "q3_reference", "q4_famous", "q5_popular", "q6_iconic"]
V23_PROBES = [("EA-1", "editorial-authority", "Critical consensus"), ("EA-2", "editorial-authority", "Awards authority"),
              ("EA-3", "editorial-authority", "Professional authority"), ("CC-1", "cultural-cult", "Enthusiast community"),
              ("CC-2", "cultural-cult", "Cultural resonance"), ("CC-3", "cultural-cult", "Insider discovery")]
V23_MODELS = [("M1", "Claude Opus 4.5", "claude-opus-4-5", "anthropic"), ("M2", "Claude Sonnet 4.5", "claude-sonnet-4-5", "anthropic"),
              ("M3", "GPT-4o", "gpt-4o", "openai"), ("M4", "GPT-4o-mini", "gpt-4o-mini", "openai"),
              ("M5", "Gemini 2.5 Flash", "gemini-2.5-flash", "google"), ("M6", "Gemini 2.5 Flash Lite", "gemini-2.5-flash-lite", "google")]
V32_MODELS = {"A": ["claude-opus-4-5-20251101", "claude-sonnet-4-5-20250929", "gpt-4o-2024-11-20",
                    "gpt-4o-mini-2024-07-18", "gemini-2.5-flash", "gemini-2.5-flash-lite"],
              "B": ["claude-opus-4-8", "claude-sonnet-4-6", "gpt-5.5-2026-04-23", "gpt-5.4-mini-2026-03-17",
                    "gemini-3.5-flash", "gemini-3.1-flash-lite"]}
V32_SLOTS = ["claude_opus", "claude_sonnet", "gpt_4o", "gpt_4o_mini", "gemini_flash", "gemini_flash_lite"]
COLS_V09 = ["timestamp", "category", "methodology_version", "prompt_set_version", "brand_registry_version",
            "prompt_id", "cep", "model_slot", "provider", "model_version", "temperature", "run_idx", "call_status",
            "attempts", "elapsed_sec", "raw_response", "wave", "brands_canonical", "brands_unknown",
            "brands_ranked", "primary_recommendation", "sentiment_summary", "extraction_method"]
COLS_RUNNER = ["timestamp", "category", "methodology_version", "prompt_set_version", "brand_registry_version",
               "prompt_id", "cep", "model_slot", "provider", "model_version", "temperature", "run_idx",
               "call_status", "attempts", "elapsed_sec", "raw_response"]
COLS_HOUSEHOLD = [c for c in COLS_RUNNER if c != "category"]
COLS_V06 = ["timestamp", "methodology_version", "prompt_set_version", "brand_registry_version", "prompt_id",
            "cep", "model", "model_version", "temperature", "run_idx", "call_status", "attempts", "elapsed_sec",
            "raw_response"]
COLS_FRAME = ["model", "frame_id", "channel", "frame_text", "response_text", "timestamp", "latency_s"]
COLS_V32 = ["arm", "channel", "frame_id", "frame_text", "latency_ms", "model_id", "resolved_version",
            "response_text", "slot", "timestamp"]
UNREG = ["Acme Supply", "Northwind", "Contoso", "Fabrikam Labs", "Globex", "Initech", "Umbrella & Co",
         "Stark Goods", "Wayne Select", "Tyrell Craft"]
DESC = ["a dependable all-rounder", "strong on value", "the premium pick", "loved by enthusiasts",
        "easy to recommend", "consistent quality across the range", "worth the price", "widely available",
        "a classic choice", "great for beginners", "a favourite of professionals", "good customer support"]


def _norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


class Category:
    """Latent popularity (who gets named) and top propensity (who gets named first)."""

    def __init__(self, rng, registry):
        self.reg = registry
        self.brands = list(registry)
        self.pop = {b: rng.paretovariate(1.3) for b in self.brands}
        self.top = {b: 0.4 * (self.pop[b] ** 0.5) + rng.gauss(0, 1) for b in self.brands}

    def pick(self, rng):
        k = rng.choice([0, 1, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8])
        pool, chosen = list(self.brands), []
        for _ in range(min(k, len(pool))):
            b = rng.choices(pool, weights=[self.pop[x] for x in pool])[0]
            chosen.append(b)
            pool.remove(b)
        return sorted(chosen, key=lambda b: -(self.top[b] + rng.gauss(0, 0.8)))

    def show(self, rng, b):
        al = [a for a in self.reg[b] if a and a.strip()]
        name = rng.choice(al) if al and rng.random() < 0.3 else b
        return name.upper() if rng.random() < 0.05 else name


def render(rng, cat, chosen):
    """Synthetic answer text in one of five styles (E3 item kinds plus prose)."""
    if not chosen:
        return rng.choice(["I'm not able to point to specific brands here; it depends on your needs.",
                           "There isn't one best option. Look at reviews, price and warranty first."])
    style = rng.choices(["num", "bul", "head", "bold", "prose"], weights=[35, 20, 15, 15, 15])[0]
    lead, passing = list(chosen), []
    if len(chosen) >= 3 and rng.random() < 0.2:          # one brand only named in passing
        passing, lead = [chosen[-1]], list(chosen[:-1])
    if rng.random() < 0.15 and len(lead) >= 2:
        head = f"Many people already know {cat.show(rng, lead[-1])}, but here is how I would rank them:\n"
    else:
        head = "Here are some options worth considering:\n"
    items = []
    for b in lead:
        items.append(b)
        if rng.random() < 0.3:
            items.append(None)                               # an item without a registry brand
    out = []
    for j, b in enumerate(items, 1):
        d = rng.choice(DESC)
        name = cat.show(rng, b) if b else rng.choice(UNREG)
        others = [x for x in chosen if x != b]
        comp = f", often compared with {cat.show(rng, rng.choice(others))}" if (b and others and rng.random() < 0.15) else ""
        if style == "num":
            out.append(f"{j}. **{name}** - {d}{comp}.")
        elif style == "bul":
            out.append(f"{rng.choice(['-', '*', '•'])} {name}: {d}{comp}.")
        elif style == "head":
            out.append(f"{rng.choice(['##', '###'])} {name}\n{d.capitalize()}{comp}.")
        elif style == "bold":
            out.append(f"**{name}** - {d}{comp}.")
        else:
            out.append(f"{rng.choice(['I would start with', 'Consider', 'Then there is', 'Also good is'])} "
                       f"{name}, {d}{comp}.")
        if b and others and style in ("num", "bul") and rng.random() < 0.12:
            out.append(f"    - pairs well with {cat.show(rng, rng.choice(others))}")
    if passing:
        out.append(f"\nAlso consider {cat.show(rng, passing[0])} for some uses.")
    if rng.random() < 0.2:
        out.append(f"\nOverall, {cat.show(rng, lead[0])} remains a safe bet.")
    return head + (" " if style == "prose" else "\n").join(out)


def v19_code(text, brands):
    """Re-implementation of osf/v19/acquire_v0_19.detect_mentions_in_response (coder)."""
    norm = _norm(text)
    numbered = list(re.finditer(r"(?m)^\s*(\d{1,2})[.)]\s+", norm))
    if numbered:
        spans = [(m.start(), numbered[i + 1].start() if i + 1 < len(numbered) else len(norm), int(m.group(1)))
                 for i, m in enumerate(numbered)]
    else:
        bul = list(re.finditer(r"(?m)^\s*[-*•]\s+", norm))
        spans = [(m.start(), bul[i + 1].start() if i + 1 < len(bul) else len(norm), i + 1) for i, m in enumerate(bul)]
    found = {}
    for b in brands:
        m = re.search(r"(?<![a-z0-9])" + re.escape(_norm(b)) + r"(?:'s|s')?(?![a-z0-9])", norm)
        if m:
            found[b] = next((r for s, e, r in spans if s <= m.start() < e), None)
    return found


def v23_code(text, patterns):
    """Re-implementation of scripts/score_v0_23.find_brand_mentions (coder)."""
    low, out = text.lower(), {}
    for bid, pats in patterns.items():
        for p in pats:
            m = re.search(p, low)
            if m:
                out[bid] = m.start()
                break
    return out


def write_csv(path, cols, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator="\r\n")
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in cols})
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(buf.getvalue().encode("utf-8"))


def _ts(r, day):
    return f"{day}T{r.randint(0, 23):02d}:{r.randint(0, 59):02d}:{r.randint(0, 59):02d}"


def runner_rows(r, sp, cat, cols, models, prompts, runs=8, n_missing=0, n_absent=0, v06=False):
    cells = [(p, m, k) for p in prompts for m in models for k in range(1, runs + 1)]
    absent = set(r.sample(range(len(cells)), n_absent)) if n_absent else set()
    cells = [c for i, c in enumerate(cells) if i not in absent]
    missing = set(r.sample(range(len(cells)), n_missing)) if n_missing else set()
    rows = []
    for i, ((pid, cep), (slot, prov, mv), k) in enumerate(cells):
        chosen = cat.pick(r)
        text = render(r, cat, chosen)
        st = "ok"
        if i in missing:
            st, text = r.choice(["transient_final", "rate_limit_final", "hard_error"]), ""
        row = {"timestamp": _ts(r, "2026-05-07"), "category": sp["category"], "methodology_version": "0.4",
               "prompt_set_version": f"{sp['category']}_v1.0", "brand_registry_version": f"{sp['category']}_v1.0",
               "prompt_id": pid, "cep": cep, "model_slot": slot, "provider": prov, "model": prov,
               "model_version": mv, "temperature": "0.7" if mv not in ("claude-opus-4-7", "gpt-5.5") else "default",
               "run_idx": k, "call_status": st, "attempts": 1 if st == "ok" else 4,
               "elapsed_sec": f"{r.uniform(1, 20):.2f}", "raw_response": text}
        if "brands_ranked" in cols and st == "ok":
            ranked = list(chosen) + (["[unk]" + r.choice(UNREG)] if r.random() < 0.3 else [])
            if len(ranked) >= 2 and r.random() < 0.2:
                i1, i2 = r.sample(range(len(ranked)), 2)
                ranked[i1], ranked[i2] = ranked[i2], ranked[i1]
            row.update(wave="v09", brands_canonical="|".join(chosen), brands_unknown="",
                       brands_ranked="|".join(ranked), primary_recommendation=chosen[0] if chosen else "",
                       sentiment_summary="|".join(f"{b}:positive" for b in chosen),
                       extraction_method="function_calling")
        elif "brands_ranked" in cols:
            row.update(wave="v09", extraction_method="skipped_empty_or_failed")
        if v06:
            row["prompt_set_version"] = row["brand_registry_version"] = "v2"
        rows.append(row)
    return rows


def build(out: Path, manifest: Path, seed: int = 110099) -> Path:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    real = S.Ctx()        # registries / detectors / prompts only (no answer file is opened)
    sets = S.build_sets()
    regs, units, cats = {}, {}, {}
    rng_cat = random.Random(seed)
    for sp in sets:
        reg, unit, _ = S.load_registry(real, sp["registry"], sp["reg_fmt"])
        regs[sp["set"]], units[sp["set"]] = reg, unit
        if sp["category"] not in cats:      # latents shared across waves and panels of a category
            cats[sp["category"]] = Category(rng_cat, reg)
    copied, synthetic = set(), set()
    for sp in sets:
        for key in ("registry", "detector", "prompts"):
            if sp.get(key) and sp[key] not in copied:
                dst = out / sp[key]
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / sp[key], dst)
                copied.add(sp[key])
    v23reg = json.loads((ROOT / S.OMNI_REG["v0.23"][0]).read_text(encoding="utf-8"))
    v23pats = {b["id"]: b["source_patterns"] for b in v23reg["brands"]}
    truth = {}
    for sp in sets:
        r = random.Random(f"{seed}|{sp['set']}")
        cat, reg, unit = cats[sp["category"]], regs[sp["set"]], units[sp["set"]]
        tr = truth.setdefault((sp["wave"], sp["category"]), {u: 0 for u in unit.values()})
        fmt, dst = sp["fmt"], out / sp["answers"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if fmt == "frame_csv":
            rows = []
            for fr, ch in FRAMES:
                for i, m in enumerate(LEGACY):
                    chosen = cat.pick(r)
                    for b in chosen:
                        tr[unit[b]] += 1
                    text = render(r, cat, chosen)
                    if sp["role"] == "paperB":
                        arm = sp["set"][-1]
                        rows.append({"arm": arm, "channel": ch, "frame_id": fr, "frame_text": f"Synthetic frame {fr}",
                                     "latency_ms": r.randint(1300, 19000), "model_id": V32_MODELS[arm][i],
                                     "resolved_version": V32_MODELS[arm][i], "response_text": text,
                                     "slot": V32_SLOTS[i], "timestamp": _ts(r, "2026-06-05")})
                    else:
                        rows.append({"model": m, "frame_id": fr, "channel": ch, "frame_text": f"Synthetic frame {fr}",
                                     "response_text": text, "timestamp": _ts(r, "2026-06-10"),
                                     "latency_s": f"{r.uniform(2, 17):.3f}"})
            write_csv(dst, COLS_V32 if sp["role"] == "paperB" else COLS_FRAME, rows)
        elif fmt == "v19_jsonl":
            lines, coded = [], []
            for fr in V19_FRAMES:
                for m in LEGACY:
                    chosen = cat.pick(r)
                    for b in chosen:
                        tr[unit[b]] += 1
                    text = render(r, cat, chosen)
                    lines.append(json.dumps({"query_id": f"phase_b__{fr}__{m}", "phase": "B", "panel_model": m,
                                             "response": text, "tokens_in": r.randint(10, 20),
                                             "tokens_out": r.randint(200, 1024), "latency_ms": r.randint(2500, 15000),
                                             "frame": fr}))
                    found = v19_code(text, list(reg))
                    for b in reg:
                        coded.append({"brand": b, "panel_model": m, "frame": fr, "mentioned": int(b in found),
                                      "rank": "" if found.get(b) is None else found[b]})
            dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
            write_csv(out / sp["coded"], ["brand", "panel_model", "frame", "mentioned", "rank"], coded)
            synthetic.add(sp["coded"])
        elif fmt == "v23_json":
            raw, scored = [], []
            for pid, ch, lab in V23_PROBES:
                for slot, mname, mid, prov in V23_MODELS:
                    chosen = cat.pick(r)
                    for b in chosen:
                        tr[unit[b]] += 1
                    text = render(r, cat, chosen)
                    rec = {"model_slot": slot, "model_name": mname, "model_id": mid, "provider": prov,
                           "prompt": f"Synthetic probe {pid}", "response": text, "status": "ok", "error": None,
                           "ts_start": _ts(r, "2026-11-09"), "ts_end": _ts(r, "2026-11-09"), "phase": "B",
                           "probe_id": pid, "channel": ch, "probe_label": lab}
                    raw.append(rec)
                    ment = v23_code(text, v23pats)
                    order = sorted(ment, key=ment.get)
                    scored.append({**rec, "brand_mentions": {b: int(b in ment) for b in v23pats},
                                   "slot_positions": {b: k + 1 for k, b in enumerate(order)},
                                   "elaborations": {b: 0 for b in ment}})
            dst.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
            (out / sp["coded"]).write_text(json.dumps(scored, ensure_ascii=False, indent=2), encoding="utf-8")
            synthetic.add(sp["coded"])
        elif fmt == "runner_csv":
            c = sp["category"]
            if sp["role"] == "early2":
                rows = runner_rows(r, sp, cat, COLS_V06, [m for m in EARLY if m[2] in S.EARLY_SHARED_MODELS],
                                   PROMPTS6, v06=True)
                write_csv(dst, COLS_V06, rows)
            elif sp["wave"] == "v0.9":
                write_csv(dst, COLS_V09, runner_rows(r, sp, cat, COLS_V09, EARLY, PROMPTS6))
            elif c == "household":
                write_csv(dst, COLS_HOUSEHOLD, runner_rows(r, sp, cat, COLS_HOUSEHOLD, EARLY, PROMPTS6))  # _final: 288/288
            elif c == "kitchen_knives":
                write_csv(dst, COLS_RUNNER, runner_rows(r, sp, cat, COLS_RUNNER, EARLY, KK_PROMPTS,
                                                        n_missing=181, n_absent=13))
            else:
                write_csv(dst, COLS_RUNNER, runner_rows(r, sp, cat, COLS_RUNNER, EARLY, PROMPTS6))
        synthetic.add(sp["answers"])
    # Presence / Consistency table (synthetic values; the scorer opens it only after Stage S)
    r = random.Random(f"{seed}|profiles")
    rows = []
    for w in S.WAVES:
        for sub in S.OMNI:
            sp = next(x for x in sets if x["role"] == "omni" and x["wave"] == w and x["category"] == sub)
            cat = cats[sub]
            inv = {u: c for c, u in units[sp["set"]].items()}
            for u in sorted(units[sp["set"]].values()):
                n = truth[(w, sub)][u]
                pop = cat.pop[inv[u]]
                cp = max(0, min(6, int(round(2 + 4 * pop / (pop + 1) + r.gauss(0, 1)))))
                p = 100 * (cp / 6 + 2 * min(1.0, n / 36)) / 3
                rated = n >= 6
                cs = r.uniform(20, 95) if rated else None
                rows.append({"wave": w, "substrate": sub, "brand": u, "P": f"{p:.6f}",
                             "C_star": "" if cs is None else f"{cs:.6f}", "rated": int(rated), "n_mentions": n,
                             "A_descriptive": "" if cs is None else f"{(p + cs) / 2:.6f}"})
    write_csv(out / S.PROFILES_REL, ["wave", "substrate", "brand", "P", "C_star", "rated", "n_mentions",
                                     "A_descriptive"], rows)
    synthetic.add(S.PROFILES_REL)
    (out / S.V41_VERDICTS_REL).parent.mkdir(parents=True, exist_ok=True)
    (out / S.V41_VERDICTS_REL).write_text(json.dumps(
        {"phase": "v0.41 (synthetic replica)", "manipulation_checks": {
            "MC_Snapshot": {"status": "MISMATCH", "mismatched": ["gpt-4o-mini"]}}}, indent=2) + "\n")
    synthetic.add(S.V41_VERDICTS_REL)
    coi = out / S.COI_REL                                   # S7 input: present, NOT pinned (decision 12)
    coi.parent.mkdir(parents=True, exist_ok=True)
    coi.write_text(json.dumps({"flagged": [{"substrate": "v0.19", "brand": "Denon"},
                                           {"substrate": "v0.23", "brand": "Hennessy"}],
                               "note": "synthetic dry-run COI flag file"}, indent=2) + "\n")
    files = []
    for rel in sorted(copied | synthetic):
        p = out / rel
        files.append({"path": rel, "synthetic": rel in synthetic, "copied_from_repository": rel in copied,
                      "git_blob": S.git_blob_sha1(p), "sha256": S.sha256(p), "bytes": p.stat().st_size})
    manifest.write_text(json.dumps({"phase": "v1.10", "kind": "DRY-RUN manifest (synthetic replicas)",
                                    "replica_root": str(out.relative_to(ROOT)) if out.is_relative_to(ROOT) else str(out),
                                    "seed": seed, "files": files}, indent=2) + "\n")
    print(f"replica: {len(synthetic)} synthetic + {len(copied)} copied files under {out}; manifest {manifest}")
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "replica"))
    ap.add_argument("--seed", type=int, default=110099)
    a = ap.parse_args()
    o = Path(a.out).resolve()
    build(o, (HERE / "INPUTS_MANIFEST_dryrun_v1_10.json") if o == (HERE / "replica").resolve()
          else o.with_name(o.name + "_MANIFEST.json"), a.seed)
