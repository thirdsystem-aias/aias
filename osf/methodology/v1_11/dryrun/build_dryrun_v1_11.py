#!/usr/bin/env python3
"""Builds SYNTHETIC replicas of every v1.11 input format under dryrun/replica/ (same relative
paths, same columns / keys as the frozen files) plus the dry-run manifest
dryrun/INPUTS_MANIFEST_dryrun_v1_11.json, so that the whole pipeline runs end to end without
reading any real answer file and without any network call:

    python3 scripts/score_v1_11.py --parity --dry-run
    python3 scripts/score_v1_11.py --build-units --dry-run
    python3 scripts/judge_v1_11.py --dry-run --replica
    python3 scripts/judge_v1_11.py --simulate          (fake judge; calibration, pause, resume, freeze)
    python3 scripts/score_v1_11.py --stage J --dry-run
    python3 scripts/score_v1_11.py --stage C --dry-run

Synthetic: every answer file (v0.23 Phase A recognition json; OMNI v0.19 jsonl, v0.20-v0.22 csv,
v0.23 json; the run_aias_v2 csv variants of the eight early sets, the v0.9 ones with
brands_canonical and per-brand sentiment_summary), the coded mention files (v0.19 csv, v0.23
scored json, made by re-implementations of the phase coders, as v1.10's builder), the
Presence / Consistency table and the v1.9 unit table (random P / C*), and v1.10's Stage S
selection and rank-table index (computed with v1.10's own functions on the replica). Copied byte
for byte (no answers in them): registries, certified detectors, prompt and query files.

Run: python3 osf/methodology/v1_11/dryrun/build_dryrun_v1_11.py [--seed N]
"""
import argparse
import csv
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
import score_v1_11 as S  # noqa: E402

V = S.V
LEGACY = ["claude-opus-4-5", "claude-sonnet-4-5", "gpt-4o", "gpt-4o-mini", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
EARLY = [("anthropic_sonnet", "anthropic", "claude-sonnet-4-6"), ("anthropic_opus", "anthropic", "claude-opus-4-7"),
         ("openai_mini", "openai", "gpt-5.4-mini"), ("openai_flagship", "openai", "gpt-5.5"),
         ("google_flash", "google", "gemini-2.5-flash"), ("xai_grok", "xai", "grok-4-1-fast")]
PROMPTS6 = [("p1_functional", "FUNCTIONAL_WHY"), ("p2_contextual", "CONTEXTUAL_WHEN"), ("p3_constraint", "CONSTRAINT_WITH"),
            ("p4_identity", "IDENTITY_HOW_FEELING"), ("p5_discovery", "DISCOVERY"), ("p6_comparison", "COMPARISON")]
FRAMES = [("q1", "R_cat"), ("q2", "R_cat"), ("q3", "R_cat"), ("q4", "R_cult"), ("q5", "R_cult"), ("q6", "R_cult")]
V19_FRAMES = ["q1_audiophile", "q2_enthusiast", "q3_reference", "q4_famous", "q5_popular", "q6_iconic"]
V23_PROBES = [("EA-1", "editorial-authority"), ("EA-2", "editorial-authority"), ("EA-3", "editorial-authority"),
              ("CC-1", "cultural-cult"), ("CC-2", "cultural-cult"), ("CC-3", "cultural-cult")]
COLS_V09 = ["timestamp", "category", "methodology_version", "prompt_set_version", "brand_registry_version",
            "prompt_id", "cep", "model_slot", "provider", "model_version", "temperature", "run_idx", "call_status",
            "attempts", "elapsed_sec", "raw_response", "wave", "brands_canonical", "brands_unknown",
            "brands_ranked", "primary_recommendation", "sentiment_summary", "extraction_method"]
COLS_RUNNER = ["timestamp", "category", "methodology_version", "prompt_set_version", "brand_registry_version",
               "prompt_id", "cep", "model_slot", "provider", "model_version", "temperature", "run_idx",
               "call_status", "attempts", "elapsed_sec", "raw_response"]
COLS_HOUSEHOLD = [c for c in COLS_RUNNER if c != "category"]
COLS_FRAME = ["model", "frame_id", "channel", "frame_text", "response_text", "timestamp", "latency_s"]
POS = ["outstanding quality", "a reliable choice", "excellent value", "widely praised", "the best in its class"]
NEU = ["founded decades ago", "sold in many countries", "offers a broad range", "a mid-priced option", "family owned"]
NEG = ["often overpriced", "known for inconsistent quality", "has had a product recall", "mixed reviews lately"]
UNREG = ["Acme Supply", "Northwind", "Contoso", "Globex", "Initech"]


def _norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


class Category:
    def __init__(self, rng, registry):
        self.reg, self.brands = registry, list(registry)
        self.pop = {b: rng.paretovariate(1.3) for b in self.brands}
        self.val = {b: rng.gauss(0.6, 0.6) for b in self.brands}

    def pick(self, rng):
        k = rng.choice([0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 8])
        pool, chosen = list(self.brands), []
        for _ in range(min(k, len(pool))):
            b = rng.choices(pool, weights=[self.pop[x] for x in pool])[0]
            chosen.append(b)
            pool.remove(b)
        return chosen

    def show(self, rng, b):
        al = [a for a in self.reg[b] if a and a.strip()]
        return rng.choice(al) if al and rng.random() < 0.2 else b

    def desc(self, rng, b):
        x = self.val[b] + rng.gauss(0, 0.7)
        return rng.choice(POS if x > 0.8 else NEG if x < -0.2 else NEU)


def render(rng, cat, chosen):
    if not chosen:
        return "It depends on your needs; read reviews and compare warranties first."
    style = rng.choice(["num", "bul", "head", "prose"])
    out = ["Here are some options worth considering:"]
    for j, b in enumerate(chosen, 1):
        d, name = cat.desc(rng, b), cat.show(rng, b)
        extra = f" It is {cat.desc(rng, b)}." if rng.random() < 0.5 else ""
        if style == "num":
            out.append(f"{j}. **{name}** - {d}.{extra}")
        elif style == "bul":
            out.append(f"- {name}: {d}.{extra}")
        elif style == "head":
            out.append(f"### {name}\n{d.capitalize()}.{extra}")
        else:
            out.append(f"Consider {name}, {d}.{extra}")
        if rng.random() < 0.15:
            out.append(f"- also see {rng.choice(UNREG)} for budget buyers")
    if rng.random() < 0.2:
        out.append(f"Overall, {cat.show(rng, chosen[0])} remains a safe bet.")
    return ("\n" if style != "prose" else " ").join(out)


def v19_code(text, brands):
    """Re-implementation of the v0.19 coder's matcher (as v1.10's dry-run builder)."""
    norm = _norm(text)
    return {b: 1 for b in brands
            if re.search(r"(?<![a-z0-9])" + re.escape(_norm(b)) + r"(?:'s|s')?(?![a-z0-9])", norm)}


def v23_code(text, patterns):
    """Re-implementation of scripts/score_v0_23.find_brand_mentions (as v1.10's dry-run builder)."""
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


def _answers(out, sp, r, cat, reg, unit, tr, v23pats, v23name, v19q, synthetic):
    dst = out / sp["answers"]
    dst.parent.mkdir(parents=True, exist_ok=True)
    if sp["fmt"] == "v23_phase_a_json":
        recs = []
        for bid in sorted(v23name):
            for slot, m in enumerate(LEGACY, 1):
                d = ". ".join(cat.desc(r, v23name[bid]).capitalize() for _ in range(r.randint(2, 5)))
                recs.append({"brand_id": bid, "brand_name": v23name[bid], "conglomerate": "0", "error": None,
                             "model_id": m, "model_name": m, "model_slot": f"M{slot}", "phase": "A",
                             "prompt": f"What do you know about the spirits brand {v23name[bid]}?",
                             "provider": S.provider_of(m), "response": f"{v23name[bid]} is a spirits brand. {d}.",
                             "spirit_type": "Synthetic", "status": "ok", "tier": "Synthetic",
                             "ts_start": "2026-06-10T00:00:00", "ts_end": "2026-06-10T00:00:05"})
        dst.write_text(json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8")
    elif sp["fmt"] == "frame_csv":
        rows = []
        for fr, ch in FRAMES:
            for m in LEGACY:
                chosen = cat.pick(r)
                for b in chosen:
                    tr[unit[b]] += 1
                rows.append({"model": m, "frame_id": fr, "channel": ch, "frame_text": f"Synthetic frame {fr}: which brands?",
                             "response_text": render(r, cat, chosen), "timestamp": "2026-06-10T00:00:00",
                             "latency_s": f"{r.uniform(2, 17):.3f}"})
        write_csv(dst, COLS_FRAME, rows)
    elif sp["fmt"] == "v19_jsonl":
        lines, coded = [], []
        for fr in V19_FRAMES:
            for m in LEGACY:
                chosen = cat.pick(r)
                text = render(r, cat, chosen)
                found = v19_code(text, list(reg))
                for b in found:
                    tr[unit[b]] += 1
                lines.append(json.dumps({"query_id": v19q[(m, fr)], "phase": "B", "panel_model": m, "response": text,
                                         "tokens_in": 15, "tokens_out": 400, "latency_ms": 5000, "frame": fr}))
                coded += [{"brand": b, "panel_model": m, "frame": fr, "mentioned": int(b in found), "rank": ""} for b in reg]
        dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
        write_csv(out / sp["coded"], ["brand", "panel_model", "frame", "mentioned", "rank"], coded)
        synthetic.add(sp["coded"])
    elif sp["fmt"] == "v23_json":
        raw, scored = [], []
        for pid, ch in V23_PROBES:
            for slot, m in enumerate(LEGACY, 1):
                chosen = cat.pick(r)
                text = render(r, cat, chosen)
                ment = v23_code(text, v23pats)
                for b in ment:
                    tr[b] += 1
                rec = {"model_slot": f"M{slot}", "model_name": m, "model_id": m, "provider": S.provider_of(m),
                       "prompt": f"Synthetic probe {pid}: which spirits brands?", "response": text, "status": "ok",
                       "error": None, "ts_start": "2026-06-10T00:00:00", "ts_end": "2026-06-10T00:00:05", "phase": "B",
                       "probe_id": pid, "channel": ch, "probe_label": pid}
                raw.append(rec)
                scored.append({**rec, "brand_mentions": {b: int(b in ment) for b in v23pats},
                               "slot_positions": {}, "elaborations": {}})
        dst.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / sp["coded"]).write_text(json.dumps(scored, ensure_ascii=False, indent=2), encoding="utf-8")
        synthetic.add(sp["coded"])
    elif sp["fmt"] == "runner_csv":
        c = sp["category"]
        cols = COLS_V09 if sp["wave"] == "v0.9" else COLS_HOUSEHOLD if c == "household" else COLS_RUNNER
        rows = []
        for pid, cep in PROMPTS6:
            for slot, prov, mv in EARLY:
                for k in range(1, 9):
                    chosen = cat.pick(r)
                    row = {"timestamp": "2026-05-07T00:00:00", "category": c, "methodology_version": "0.4",
                           "prompt_set_version": f"{c}_v1.0", "brand_registry_version": f"{c}_v1.0",
                           "prompt_id": pid, "cep": cep, "model_slot": slot, "provider": prov, "model_version": mv,
                           "temperature": "0.7", "run_idx": k, "call_status": "ok", "attempts": 1,
                           "elapsed_sec": "3.00", "raw_response": render(r, cat, chosen)}
                    if cols is COLS_V09:
                        row.update(wave="v09", brands_canonical="|".join(chosen), brands_unknown="",
                                   brands_ranked="|".join(chosen), primary_recommendation=chosen[0] if chosen else "",
                                   sentiment_summary="|".join(f"{b}:{r.choice(['positive', 'neutral', 'negative'])}"
                                                              for b in chosen), extraction_method="function_calling")
                    rows.append(row)
        write_csv(dst, cols, rows)
    synthetic.add(sp["answers"])


def build(out: Path, manifest: Path, seed: int = 111099) -> Path:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    real = S.make_ctx(False)                 # registries / detectors / prompts only (no answer file opened)
    sets = S.build_sets()
    regs, units, cats = {}, {}, {}
    rng_cat = random.Random(seed)
    for sp in sets:
        reg, unit, _ = V.load_registry(real, sp["registry"], sp["reg_fmt"])
        regs[sp["set"]], units[sp["set"]] = reg, unit
        if sp["category"] not in cats:
            cats[sp["category"]] = Category(rng_cat, reg)
    copied, synthetic = set(), set()
    for sp in sets:
        for key in ("registry", "detector", "prompts", "questions"):
            if sp.get(key) and sp[key] not in copied:
                dst = out / sp[key]
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / sp[key], dst)
                copied.add(sp[key])
    v23reg = json.loads((ROOT / S.V23_REGISTRY).read_text(encoding="utf-8"))
    v23pats = {b["id"]: b["source_patterns"] for b in v23reg["brands"]}
    v23name = {b["id"]: b["brand"] for b in v23reg["brands"]}
    v19q = {}
    for line in (ROOT / S.V19_QUERIES).read_text(encoding="utf-8").splitlines():
        if line.strip():
            q = json.loads(line)
            v19q[(q["panel_model"], q["frame"])] = q["query_id"]
    truth = {}
    for sp in sets:
        r = random.Random(f"{seed}|{sp['set']}")
        tr = truth.setdefault((sp["wave"], sp["category"]), {u: 0 for u in units[sp["set"]].values()})
        if sp["block"] == "R":
            tr = {}
        _answers(out, sp, r, cats[sp["category"]], regs[sp["set"]], units[sp["set"]], tr, v23pats, v23name, v19q, synthetic)
    r = random.Random(f"{seed}|profiles")
    prof, t19 = [], []
    for w in S.WAVES:
        for sub in S.OMNI:
            sp = next(x for x in sets if x["block"] == "F" and x["wave"] == w and x["category"] == sub)
            for u in sorted(units[sp["set"]].values()):
                n = truth[(w, sub)][u]
                p = r.uniform(5, 95)
                cs = r.uniform(20, 95) if n >= 6 else None
                prof.append({"wave": w, "substrate": sub, "brand": u, "P": f"{p:.6f}",
                             "C_star": "" if cs is None else f"{cs:.6f}", "rated": int(n >= 6), "n_mentions": n,
                             "A_descriptive": ""})
                t19.append({"wave": w, "substrate": sub, "brand": u, "mentions": n, "P": f"{p:.6f}",
                            "C_star": "" if cs is None else f"{cs:.6f}", "A_add_descriptive": "", "C_phi_unfloored": ""})
    write_csv(out / S.PROFILES_REL, ["wave", "substrate", "brand", "P", "C_star", "rated", "n_mentions", "A_descriptive"], prof)
    write_csv(out / S.V19_TABLE_REL, ["wave", "substrate", "brand", "mentions", "P", "C_star", "A_add_descriptive",
                                      "C_phi_unfloored"], t19)
    synthetic |= {S.PROFILES_REL, S.V19_TABLE_REL}
    # v1.10 Stage S objects: synthetic selection; rank-table index computed with v1.10's own code
    pre = sorted(copied | synthetic)
    manifest.write_text(json.dumps({"files": [{"path": p, "git_blob": V.git_blob_sha1(out / p),
                                               "sha256": V.sha256(out / p)} for p in pre]}) + "\n")
    ctx = S.make_ctx(True, root=out, manifest=manifest)
    idx = {}
    for sp in sets:
        if sp["block"] in ("F", "E"):
            reg, unit, _ = V.load_registry(ctx, sp["registry"], sp["reg_fmt"])
            pats = V.compile_registry(reg)
            infos = [V.extract_answer(a, pats, unit) for a in V.load_answers(ctx, sp)]
            idx[sp["set"]] = {"path": f"rank_tables/{V._slug(sp['set'])}.csv",
                              "sha256": V.sha256_bytes(V.rank_table_bytes({"infos": infos}))}
    for rel, doc in ((S.V110_RANK_INDEX_REL, idx),
                     (S.V110_SELECTION_REL, {"phase": "v1.10 (synthetic replica)", "selected": "MNP", "outcome": "SELECTED",
                                             "stat_for_stage_c": "MNP", "instrument_fail": False, "dry_run": True})):
        (out / rel).parent.mkdir(parents=True, exist_ok=True)
        (out / rel).write_text(json.dumps(doc, indent=2) + "\n")
        synthetic.add(rel)
    files = []
    for rel in sorted(copied | synthetic):
        p = out / rel
        files.append({"path": rel, "synthetic": rel in synthetic, "copied_from_repository": rel in copied,
                      "git_blob": V.git_blob_sha1(p), "sha256": V.sha256(p), "bytes": p.stat().st_size})
    manifest.write_text(json.dumps({"phase": "v1.11", "kind": "DRY-RUN manifest (synthetic replicas)",
                                    "replica_root": str(out.relative_to(ROOT)), "seed": seed, "files": files},
                                   indent=2) + "\n")
    print(f"replica: {len(synthetic)} synthetic + {len(copied)} copied files under {out}; manifest {manifest}")
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=111099)
    a = ap.parse_args()
    build(S.DRY_ROOT, S.DRY_MANIFEST, a.seed)
