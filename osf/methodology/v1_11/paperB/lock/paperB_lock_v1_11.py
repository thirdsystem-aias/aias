#!/usr/bin/env python3
"""Sentiment Paper B (human labels, v1.11): lock helper. r1, 2026-11-11, AIAS runner (branch v1.11-paperB).

No network, no model call. Commands (run from anywhere; paths are relative to the repo root):
  --guide-md        write guide/STUDENT_GUIDE_v1_11_paperB.md from the two saved guide pages (guide/source)
  --diff-guide      compare guide page 2 with judge_prompt_v1_11.md rules 1-7 and the valence scale
                    (writes guide/guide_vs_judge_v1_11_paperB.json; exit 1 on any difference)
  --sync            write the statement (statement/statement_exercise_doc.md) into forms/Code.gs and into
                    the pre-registration, and the guide text into the pre-registration (between markers)
  --check           every readiness check (below); exit 1 if any fails
  --lock-manifest   write prereg/LOCK_MANIFEST_v1_11_paperB.sha256 (refuses if --check fails)
  --verify-lock     every file in the manifest has its recorded SHA-256
  --write-anchor --osf-note "..."   anchor/git_anchor_v1_11_paperB.json (after tag, push and OSF deposit)
"""
import argparse, ast, csv, datetime, hashlib, html, json, os, re, subprocess, sys, tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
PB = os.path.normpath(os.path.join(HERE, os.pardir))                       # .../v1_11/paperB
REPO = os.path.normpath(os.path.join(PB, os.pardir, os.pardir, os.pardir, os.pardir))
REL = lambda p: os.path.relpath(p, REPO)
TAG = "v1.11-paperB-prereg-r1"
BRANCH = "v1.11-paperB"
GUIDE_URL = "https://claude.ai/artifact/4sCt6DcfA4RD6h4TdvUdZZ"
GUIDE_VERSION = "1794367225-74d8"
GUIDE_READ = "2026-11-11"
STATEMENT_URL = "https://claude.ai/artifact/QHkHLwkqZHAaHs7pTrFTH2"
P = {
    "prereg": os.path.join(PB, "prereg", "PRE_REGISTRATION_v1_11_paperB.md"),
    "manifest": os.path.join(PB, "prereg", "LOCK_MANIFEST_v1_11_paperB.sha256"),
    "page1": os.path.join(PB, "guide", "source", "Main.dc.html"),
    "page2": os.path.join(PB, "guide", "source", "Rules.dc.html"),
    "guide_md": os.path.join(PB, "guide", "STUDENT_GUIDE_v1_11_paperB.md"),
    "diff": os.path.join(PB, "guide", "guide_vs_judge_v1_11_paperB.json"),
    "statement": os.path.join(PB, "statement", "statement_exercise_doc.md"),
    "code": os.path.join(PB, "forms", "Code.gs"),
    "judge": os.path.join(PB, os.pardir, "prereg", "judge_prompt_v1_11.md"),
    "sample": os.path.join(PB, "human_sample_v1_11_paperB_r1.csv"),
    "make_packets": os.path.join(PB, "packets", "make_packets_v1_11_paperB.py"),
    "coi": os.path.join(PB, "packets", "coi_screen_v1_11_paperB.py"),
    "design": os.path.join(PB, "packets", "packet_design_N19_b.json"),
    "anchor": os.path.join(PB, os.pardir, "anchor", "git_anchor_v1_11_paperB.json"),
}
LOCKED = [P["prereg"], P["guide_md"], P["page1"], P["page2"], P["diff"], P["statement"],
          os.path.join(PB, "statement", "statement_source.json"), P["code"],
          os.path.join(PB, "forms", "mock_test.js"), os.path.join(PB, "forms", "mock_driver.js"),
          os.path.join(PB, "forms", "mock_run.sh"), P["make_packets"], P["coi"], P["design"],
          os.path.abspath(__file__), os.path.join(HERE, "test_paperB_lock_v1_11.py"),
          os.path.join(PB, "LOCK_STEPS.md"),
          # pinned inputs (unchanged by this study)
          P["sample"], P["judge"], os.path.join(PB, os.pardir, "anchor", "DEVIATIONS.md")]
AI_USE = ("## Use of AI tools {-}\n\nDuring the preparation of this work the author used AI tools (Anthropic's "
          "Claude) to assist with study design, analysis and writing. The author reviewed and edited all content "
          "and takes full responsibility for it.")
MONTHS = "January February March April May June July August September October November December".split()


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------ guide pages -> text lines
class _Text(HTMLParser):
    BLOCK = {"div", "p", "h1", "h2", "h3", "li"}
    SKIP = {"head", "helmet", "style", "script", "title"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.cur, self.skip = [], [], 0

    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.cur)).strip()
        if t:
            self.lines.append(t)
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in self.BLOCK or tag == "br":
            self.flush()

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip -= 1
        elif tag in self.BLOCK:
            self.flush()

    def handle_data(self, data):
        if not self.skip:
            self.cur.append(data)


def page_lines(path):
    t = _Text()
    t.feed(read(path))
    t.flush()
    return t.lines


def guide_markdown():
    out = ["# Student guide, Sentiment Paper B (two pages), as read for the pre-registration", "",
           f"Source: {GUIDE_URL} (Design canvas \"Student guide — Labeling AI answers about brands\"), version "
           f"`{GUIDE_VERSION}`, read {GUIDE_READ} with the Artifact tool's read action (no web fetch). The two "
           "artboards are saved byte for byte in `guide/source/`; this file is generated from them by "
           "`lock/paperB_lock_v1_11.py --guide-md` (text only: one line per block element, HTML entities decoded, "
           "spaces collapsed; layout, colours and bold dropped). The words are the guide's, unchanged.", "",
           "| Page | File | SHA-256 |", "|---|---|---|",
           f"| 1 | `guide/source/Main.dc.html` | `{sha256(P['page1'])}` |",
           f"| 2 | `guide/source/Rules.dc.html` | `{sha256(P['page2'])}` |", ""]
    for n, key in ((1, "page1"), (2, "page2")):
        out += [f"## Page {n}", "", "```text"] + page_lines(P[key]) + ["```", ""]
    return "\n".join(out)


# ------------------------------------------------------------------ guide page 2 vs judge prompt
def judge_block(judge_md=None):
    txt = read(judge_md or P["judge"])
    tmpl = txt.split("<!-- BEGIN USER_TEMPLATE -->", 1)[1].split("<!-- END USER_TEMPLATE -->", 1)[0]
    lines = [l for l in tmpl.splitlines()]
    i = lines.index("Rules:")
    j = max(k for k, l in enumerate(lines) if l.startswith("-2 = "))
    return [l for l in lines[i:j + 1] if l.strip()]


def guide_block(lines=None):
    lines = lines if lines is not None else page_lines(P["page2"])
    i = lines.index("Rules:")
    j = max(k for k, l in enumerate(lines) if l.startswith("-2 = "))
    return lines[i:j + 1]


def diff_guide(g=None, j=None):
    g = guide_block() if g is None else g
    j = judge_block() if j is None else j
    diffs = []
    for k in range(max(len(g), len(j))):
        a = j[k] if k < len(j) else None
        b = g[k] if k < len(g) else None
        if a != b:
            diffs.append({"line": k + 1, "judge_prompt": a, "guide_page_2": b})
    return {"compared": "judge_prompt_v1_11.md USER_TEMPLATE, from 'Rules:' to the '-2 = ' scale line, vs "
                        "guide page 2 (guide/source/Rules.dc.html), the same span; exact string comparison per line",
            "judge_lines": len(j), "guide_lines": len(g), "rules": sum(1 for l in j if re.match(r"\d\. ", l)),
            "scale_lines": sum(1 for l in j if re.match(r"-?\d = ", l)), "identical": not diffs,
            "differences": diffs}


# ------------------------------------------------------------------ forms (Code.gs) vs guide page 1
def js_array(code, name):
    m = re.search(r"const " + name + r" = \[(.*?)\];", code, re.S)
    return [ast.literal_eval(x) for x in re.findall(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"", m.group(1))]


def guide_page1():
    h = read(P["page1"])
    heads = re.findall(r">(\d)</div><div style=\"font-size: 15px; font-weight: 700; color: #37237b\">([^<]+)</div>", h)
    strong = [html.unescape(s) for s in re.findall(r"<strong>([^<]+)</strong>", h)]
    return {"titles": [f"{n}. {html.unescape(t)}" for n, t in heads], "tone": strong[0:6],
            "both": strong[6:8], "source": strong[8:12], "sure": strong[12:14]}


def check_forms(code=None):
    code = code if code is not None else read(P["code"])
    g = guide_page1()
    got = {"titles": js_array(code, "Q_TITLES"), "tone": js_array(code, "TONE"), "both": js_array(code, "BOTH"),
           "source": js_array(code, "SOURCE"), "sure": js_array(code, "SURE")}
    return {k: {"guide": g[k], "forms": got[k], "same": g[k] == got[k]} for k in g}


# ------------------------------------------------------------------ statement
def statement_paragraphs(md=None):
    md = md if md is not None else read(P["statement"])
    return [re.sub(r"\s+", " ", p.replace("**", "")).strip() for p in md.split("\n\n") if p.strip()]


def code_statement(code=None):
    code = code if code is not None else read(P["code"])
    block = code.split("const STATEMENT = [", 1)[1].split("].join('\\n\\n');", 1)[0]
    return [ast.literal_eval(l.strip().rstrip(",")) for l in block.strip().splitlines()]


def js_literal(s):
    if "'" not in s:
        return "'" + s.replace("\\", "\\\\") + "'"
    return json.dumps(s, ensure_ascii=False)


def _date(m, d):
    return f"{m} {int(d)}"


def statement_vs_guide(md=None, page1=None):
    """Facts the statement shares with guide page 1 must agree (answers, time, due date, withdrawal date)."""
    st = " ".join(statement_paragraphs(md))
    g = " ".join(page_lines(P["page1"]) if page1 is None else page1)
    mon = {m[:3]: m for m in MONTHS}
    due = re.search(r"LABELS DUE (\w{3}) (\d+)", g)
    facts = {
        "answers": (re.search(r"about (\d+) short AI answers", st), re.search(r"about (\d+) short AI answers", g)),
        "time": (re.search(r"It takes (about [^,]+),", st), re.search(r"ABOUT (\d+ MINUTES)", g)),
        "due": (re.search(r"by (" + "|".join(MONTHS) + r") (\d+)", st), due),
        "withdraw_until": (re.search(r"withdraw your labels until (" + "|".join(MONTHS) + r") (\d+)", st),
                           re.search(r"withdraw your labels until (" + "|".join(MONTHS) + r") (\d+)", g)),
    }
    out = {}
    for k, (a, b) in facts.items():
        if k == "answers":
            sa, sb = a and a.group(1), b and b.group(1)
        elif k == "time":
            sa, sb = a and a.group(1), b and ("about " + b.group(1).lower())
        elif k == "due":
            sa, sb = a and _date(a.group(1), a.group(2)), b and _date(mon[b.group(1)], b.group(2))
        else:
            sa, sb = a and _date(a.group(1), a.group(2)), b and _date(b.group(1), b.group(2))
        out[k] = {"statement": sa, "guide": sb, "same": sa is not None and sa == sb}
    return out


# ------------------------------------------------------------------ pre-registration blocks
def replace_between(text, begin, end, body):
    a, rest = text.split(begin, 1)
    _, b = rest.split(end, 1)
    return a + begin + "\n" + body + "\n" + end + b


def prereg_statement_body(md=None):
    md = md if md is not None else read(P["statement"])
    return "\n>\n".join("> " + p.strip() for p in md.strip().split("\n\n"))


def prereg_guide_body():
    g = read(P["guide_md"]).split("## Page 1", 1)[1]
    return "#### Page 1" + g.replace("## Page 2", "#### Page 2").rstrip("\n")


def sync():
    md = read(P["statement"])
    code = read(P["code"])
    lines = ",\n".join("  " + js_literal(p) for p in statement_paragraphs(md)) + ","
    a, rest = code.split("const STATEMENT = [\n", 1)
    _, b = rest.split("].join('\\n\\n');", 1)
    open(P["code"], "w", encoding="utf-8").write(a + "const STATEMENT = [\n" + lines + "\n].join('\\n\\n');" + b)
    pr = read(P["prereg"])
    pr = replace_between(pr, "<!-- BEGIN STATEMENT -->", "<!-- END STATEMENT -->", prereg_statement_body(md))
    pr = replace_between(pr, "<!-- BEGIN GUIDE -->", "<!-- END GUIDE -->", prereg_guide_body())
    open(P["prereg"], "w", encoding="utf-8").write(pr)


# ------------------------------------------------------------------ packets and the COI screen
def rebuild_packets(n=19, variant="b"):
    d = tempfile.mkdtemp(prefix="paperB_packets_")
    subprocess.run([sys.executable, P["make_packets"], "--n", str(n), "--variant", variant, "--out", d],
                   check=True, capture_output=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return d


def check_packets(outdir):
    des = json.loads(read(os.path.join(outdir, "packet_design.json")))
    rec = json.loads(read(P["design"]))
    csv.field_size_limit(sys.maxsize)
    def rows(p):
        with open(p, newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    key = rows(os.path.join(outdir, "key_PRIVATE", "item_key.csv"))
    items = rows(os.path.join(outdir, "packets", "packets_all.csv"))
    per = {}
    for r in items:
        per.setdefault(r["student_id"], []).append(r["item_id"])
    loads = sorted(len(v) for v in per.values())
    coders_ok = all(int(k["n_coders"]) == 2 and len(set(k["coders"].split(";"))) == 2 for k in key)
    sys.path.insert(0, os.path.dirname(P["coi"]))
    import coi_screen_v1_11_paperB as coi
    sample = rows(P["sample"])
    labelled = {k["unit_id"] for k in key}
    subj, ment = coi.screen([r for r in sample if r["unit_id"] in labelled])
    return {
        "byte_identical_to_recorded": des["outputs_sha256"] == rec["outputs_sha256"],
        "units": des["units"], "labels": des["labels_total"], "seed": des["seed"], "variant": des["variant"],
        "sample_sha256": des["sample_sha256"],
        "loads": {"55": loads.count(55), "54": loads.count(54), "other": len(loads) - loads.count(55) - loads.count(54)},
        "every_unit_two_distinct_students": coders_ok and len(key) == des["units"],
        "no_student_sees_a_unit_twice": all(len(v) == len(set(v)) for v in per.values()),
        "recognition_units": sum(1 for k in key if k["unit_type"] == "recognition"),
        "coi_target_brand_hits": subj,
        "coi_text_mentions": [{"unit_id": m["unit_id"], "brand": m["brand"], "terms": sorted(m["hits"])} for m in ment],
    }


# ------------------------------------------------------------------ readiness
def checks(packets=True):
    res = []
    add = lambda name, ok, info="": res.append({"check": name, "ok": bool(ok), "info": info})
    add("guide markdown matches the saved pages", read(P["guide_md"]) == guide_markdown() + "\n")
    d = diff_guide()
    add("guide page 2 = judge rules 1-7 and scale, word for word", d["identical"] and d["rules"] == 7
        and d["scale_lines"] == 5, f"{len(d['differences'])} differences")
    f = check_forms()
    add("forms: four questions and options = guide page 1", all(v["same"] for v in f.values()),
        [k for k, v in f.items() if not v["same"]])
    add("forms: STATEMENT = statement file, word for word", code_statement() == statement_paragraphs())
    sv = statement_vs_guide()
    add("statement agrees with guide page 1 (answers, time, due date, withdrawal date)",
        all(v["same"] for v in sv.values()), {k: v for k, v in sv.items() if not v["same"]})
    pr = read(P["prereg"])
    add("pre-registration carries the statement verbatim",
        pr.split("<!-- BEGIN STATEMENT -->\n", 1)[1].split("\n<!-- END STATEMENT -->", 1)[0] == prereg_statement_body())
    add("pre-registration carries the guide verbatim",
        pr.split("<!-- BEGIN GUIDE -->\n", 1)[1].split("\n<!-- END GUIDE -->", 1)[0] == prereg_guide_body())
    coi_sec = pr.split("### Conflict of interest {-}", 1)[1].split("\n### ", 1)[0] if "### Conflict of interest {-}" in pr else ""
    add("Samsung named only in the COI section", "Samsung" in coi_sec and "Samsung" not in pr.replace(coi_sec, ""))
    eth = pr.find("### Ethics {-}")
    add("AI-use statement verbatim, after Ethics", eth >= 0 and pr.find(AI_USE) > eth)
    add("no open placeholder in the pre-registration", not re.search(r"\[OPEN|placeholder|TBD|TODO", pr))
    if packets:
        d2 = rebuild_packets()
        pk = check_packets(d2)
        add("packets: rebuilt byte-identical, 518 units, 10 x 55 + 9 x 54, two students per unit, no recognition",
            pk["byte_identical_to_recorded"] and pk["units"] == 518 and pk["labels"] == 1036
            and pk["loads"] == {"55": 10, "54": 9, "other": 0} and pk["every_unit_two_distinct_students"]
            and pk["no_student_sees_a_unit_twice"] and pk["recognition_units"] == 0 and pk["seed"] == 111023,
            {k: pk[k] for k in ("units", "labels", "loads", "seed")})
        add("packets: no Samsung-group target brand (Denon included)", pk["coi_target_brand_hits"] == [],
            pk["coi_text_mentions"])
    return res


# ------------------------------------------------------------------ manifest and anchor
def write_manifest():
    with open(P["manifest"], "w", encoding="utf-8") as fh:
        for p in LOCKED:
            fh.write(f"{sha256(p)}  {REL(p)}\n")


def verify_manifest(manifest=None, root=REPO):
    bad = []
    for line in open(manifest or P["manifest"], encoding="utf-8"):
        h, rel = line.rstrip("\n").split("  ", 1)
        p = os.path.join(root, rel)
        if not os.path.exists(p) or sha256(p) != h:
            bad.append(rel)
    return bad


def git(*a):
    return subprocess.run(["git", "-C", REPO, *a], check=True, capture_output=True, text=True).stdout.strip()


def write_anchor(osf_note):
    if not osf_note.strip():
        sys.exit("--osf-note is required (the OSF deposit)")
    if verify_manifest():
        sys.exit("lock manifest does not verify")
    commit = git("rev-parse", f"{TAG}^{{commit}}")
    if git("rev-parse", "HEAD") != commit:
        sys.exit("HEAD is not the tagged commit")
    remote = git("ls-remote", "--tags", "origin", TAG)
    tag_obj = git("rev-parse", TAG)
    if tag_obj not in remote:
        sys.exit("tag not on origin")
    files = {}
    for line in open(P["manifest"], encoding="utf-8"):
        h, rel = line.rstrip("\n").split("  ", 1)
        files[rel] = {"sha256": h, "git_blob": git("rev-parse", f"{TAG}:{rel}")}
    files[REL(P["manifest"])] = {"sha256": sha256(P["manifest"]), "git_blob": git("rev-parse", f"{TAG}:{REL(P['manifest'])}")}
    a = {"tag": TAG, "tag_object": tag_obj, "commit": commit, "tree": git("rev-parse", f"{TAG}^{{tree}}"),
         "branch": BRANCH, "tagger_date": git("for-each-ref", f"refs/tags/{TAG}", "--format=%(taggerdate:iso-strict)"),
         "remote_tag_ref": remote.splitlines()[0],
         "recorded_utc": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat(),
         "repository": git("remote", "get-url", "origin"), "osf_deposit": osf_note,
         "lock_manifest_sha256": sha256(P["manifest"]), "locked_files": files}
    with open(P["anchor"], "w", encoding="utf-8") as fh:
        json.dump(a, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("anchor written:", REL(P["anchor"]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for c in ("guide-md", "diff-guide", "sync", "check", "lock-manifest", "verify-lock", "write-anchor"):
        ap.add_argument("--" + c, action="store_true")
    ap.add_argument("--no-packets", action="store_true", help="--check without the packet rebuild")
    ap.add_argument("--osf-note", default="")
    a = ap.parse_args()
    if a.guide_md:
        open(P["guide_md"], "w", encoding="utf-8").write(guide_markdown() + "\n")
        print("written", REL(P["guide_md"]))
    if a.diff_guide:
        d = diff_guide()
        with open(P["diff"], "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
        print(f"guide vs judge: {d['rules']} rules, {d['scale_lines']} scale lines, identical={d['identical']}, "
              f"{len(d['differences'])} differences")
        if not d["identical"]:
            sys.exit(1)
    if a.sync:
        sync()
        print("statement -> Code.gs and pre-registration; guide -> pre-registration")
    if a.check or a.lock_manifest:
        res = checks(packets=not a.no_packets)
        for r in res:
            print(("PASS " if r["ok"] else "FAIL ") + r["check"] + (f"  {r['info']}" if r["info"] and not r["ok"] else ""))
        fails = sum(not r["ok"] for r in res)
        print(f"{len(res) - fails} of {len(res)} checks pass")
        if fails:
            sys.exit(1)
    if a.lock_manifest:
        write_manifest()
        print("written", REL(P["manifest"]), sha256(P["manifest"]))
    if a.verify_lock:
        bad = verify_manifest()
        print("lock manifest OK" if not bad else f"lock manifest FAILS: {bad}")
        if bad:
            sys.exit(1)
    if a.write_anchor:
        write_anchor(a.osf_note)


if __name__ == "__main__":
    main()
