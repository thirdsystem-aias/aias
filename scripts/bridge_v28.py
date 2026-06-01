#!/usr/bin/env python3
"""
v0.28 (CV.04) bridge — raw Phase A/B acquisition -> brand,presence.

Sits between the acquisition harness (which writes raw probe rows) and
score_v28.py (which consumes an aggregated brand,presence CSV). This is the only
gap in the v0.28 pipeline; it is PLUMBING, not methodology.

Presence definition (pinned at v0.28-prereg-r2, DEVIATIONS Entry 2):
  Reuses the SEMANTIC of v0.25's presence_composite — an equal-weighted mean of
  each component's fraction-of-its-own-max, scaled to 0-100 — instantiated at the
  v1.6-canonical denominators for a 3-frame-per-channel Phase B:

      C_P_scaled    = (C_P    /  6) * 100      # Phase A, 6 models, max 6
      R_cat_scaled  = (R_cat  / 18) * 100      # Phase B q1-q3 x 6 models, max 18
      R_cult_scaled = (R_cult / 18) * 100      # Phase B q4-q6 x 6 models, max 18
      presence      = mean(C_P_scaled, R_cat_scaled, R_cult_scaled)

  NOTE the /18 (NOT v0.25's /36 literal). v0.25 divided by 36 because v0.24's
  Phase B was a NON-canonical 6-frame-per-channel battery (empirically: 6 distinct
  probe_num per channel x 6 models). v1.6 canon is 3 frames/channel, max 18 —
  which the v0.28 r1 Phase B follows. The fraction-of-max semantic is identical;
  only the denominator tracks the (canonical) design. See DEVIATIONS Entry 2 and
  the anchor-commensurability caveat (3-cue vs 6-cue/channel) vs the rho=0.74
  convergent benchmark.

Inputs (raw, written by the acquisition harness):
  osf/v28/data/phase_a_results.csv   brand, ..., model, recognized  (yes/no/error)
  osf/v28/data/phase_b_results.csv   model, channel(R_cat|R_cult), response_text, ...
       Phase B brand mentions are detected with the v1.4 canonical rule
       (case-insensitive, accent-stripped, word-boundary) over the frozen panel.

Output:
  osf/v28/data/v0.28_presence.csv    brand, presence, C_P, R_cat, R_cult
       (score_v28.load_presence reads the 'presence' column; the component
        columns are carried for transparency / audit.)

Blinding: reads the frozen panel from prereg/v0_28_panel_brands.txt ONLY. Never
reads prereg/v0_28_brand_validator.csv. Presence is composed with no reference to
familiarity or d'.

Usage:
  python3 scripts/bridge_v28.py
"""
import csv, os, re, sys, unicodedata

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/aias")
PANEL = os.path.join(ROOT, "prereg/v0_28_panel_brands.txt")
PHASE_A = os.path.join(ROOT, "osf/v28/data/phase_a_results.csv")
PHASE_B = os.path.join(ROOT, "osf/v28/data/phase_b_results.csv")
OUT = os.path.join(ROOT, "osf/v28/data/v0.28_presence.csv")

# denominators — pinned r2, v1.6-canonical 3-frame/channel design
CP_MAX, RCAT_MAX, RCULT_MAX = 6, 18, 18


def load_panel():
    return [l.strip() for l in open(PANEL) if l.strip()]


def fold(s):
    """v1.4 canonical mention folding: lowercase, accent-strip, collapse space."""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.lower()).strip()


def mentioned(brand, text):
    """word-boundary, accent-stripped, case-insensitive presence of brand in text."""
    b = re.escape(fold(brand))
    return re.search(r"(?<![a-z0-9])" + b + r"(?![a-z0-9])", fold(text)) is not None


def phase_a_cp(panel):
    """Per-brand C_P = count of recognized=='yes' across the 6 models."""
    cp = {b: 0 for b in panel}
    seen = {b: 0 for b in panel}
    with open(PHASE_A, newline="") as f:
        for r in csv.DictReader(f):
            b = r["brand"].strip()
            if b not in cp:
                continue
            seen[b] += 1
            if r.get("recognized", "").strip().lower() == "yes":
                cp[b] += 1
    return cp, seen


def phase_b_recall(panel):
    """Per-brand R_cat / R_cult = mentions across each channel's responses."""
    rcat = {b: 0 for b in panel}
    rcult = {b: 0 for b in panel}
    with open(PHASE_B, newline="") as f:
        for r in csv.DictReader(f):
            ch = r.get("channel", "").strip()
            txt = r.get("response_text", "") or r.get("response_excerpt", "")
            for b in panel:
                if mentioned(b, txt):
                    if ch == "R_cat":
                        rcat[b] += 1
                    elif ch == "R_cult":
                        rcult[b] += 1
    return rcat, rcult


def main():
    panel = load_panel()
    for p in (PHASE_A, PHASE_B):
        if not os.path.exists(p):
            sys.exit("bridge_v28: missing acquisition input %s "
                     "(run the harness first; acquisition pending)" % p)

    cp, seen = phase_a_cp(panel)
    rcat, rcult = phase_b_recall(panel)

    rows = []
    for b in panel:
        cp_s = cp[b] / CP_MAX * 100
        rcat_s = rcat[b] / RCAT_MAX * 100
        rcult_s = rcult[b] / RCULT_MAX * 100
        presence = (cp_s + rcat_s + rcult_s) / 3
        rows.append({"brand": b, "presence": round(presence, 4),
                     "C_P": cp[b], "R_cat": rcat[b], "R_cult": rcult[b]})

    # integrity: every panel brand must have all 6 Phase A probes
    bad = [b for b in panel if seen[b] != 6]
    if bad:
        print("  WARNING: brands without exactly 6 Phase A probes: %s" % bad)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["brand", "presence", "C_P", "R_cat", "R_cult"])
        w.writeheader()
        w.writerows(rows)

    print("=== v0.28 bridge: raw Phase A/B -> brand,presence ===")
    print("  panel brands: %d   presence = mean(C_P/6, R_cat/18, R_cult/18)*100" % len(panel))
    for r in sorted(rows, key=lambda x: -x["presence"]):
        print("  %-26s presence=%6.2f  (C_P=%d R_cat=%d R_cult=%d)"
              % (r["brand"], r["presence"], r["C_P"], r["R_cat"], r["R_cult"]))
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
