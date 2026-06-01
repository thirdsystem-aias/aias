#!/usr/bin/env python3
"""
v0.28 (CV.04) scorer — BRAND discriminant validator.

Tests whether AIAS Presence over the frozen 24-brand Tech panel is DISCRIMINANT
from the BRAND database's familiarity (1-7) and recognition-memory (d') norms —
i.e. that Presence is NOT just re-measuring familiarity. Convergent benchmark is
the v0.25 Google Trends anchor (rho = 0.74); a discriminant instrument should
fall well below it.

LOCKED decision rules (pre-reg r1; mirror the CV.04 spec):
  CONVERGENT_BENCHMARK = 0.74
  band on |rho| (signed rho + negative_correlation flag also reported):
     |rho| < 0.50              -> CONFIRMED  (discriminant)
     0.50 <= |rho| < 0.74      -> PARTIAL
     |rho| >= 0.74             -> FALSIFIED  (converges with familiarity)
  UNDETERMINED if n < 12  OR  the BCa CI (mapped to |rho|) spans all three bands.
  verdict_basis = point |rho| vs bands ; BCa 95% CI reported, NON-GATING.
     ci_excludes_reducibility = (|rho| CI upper) < 0.74
     provisional = CONFIRMED and not ci_excludes_reducibility
  STAT: Spearman primary (drives verdict) ; Pearson secondary (reported) ;
        BCa bootstrap 95% CI, 10k resamples, seed 280400.

Hypotheses:
  H_Disc_Familiarity  (PRIMARY)    rho(Presence, familiarity_1_7)
  H_Disc_Recognition  (SECONDARY)  rho(Presence, dprime)
  H_Dissociation      (TERTIARY, DESCRIPTIVE, non-gating)
     within-panel z(Presence) - z(familiarity); amplified > +1.0, suppressed < -1.0
     FULL    (>=4 cases AND both directions present)
     PARTIAL (1-3 cases, OR >=4 one-directional)
     ABSENT  (0 cases)

Inputs:
  prereg/v0_28_brand_validator.csv   brand, familiarity_1_7, dprime   (frozen, exists)
  prereg/v0_28_panel_brands.txt      24 brands, frozen                (exists)
  osf/v28/data/v0.28_presence.csv    brand, presence                  (acquisition output)
       'presence' = the AIAS Presence score over the Tech panel.
       If absent, runs as a SMOKE TEST: Presence-dependent verdicts -> NOT_RUN.

Writes: osf/v28/v28_verdicts.json

NOTE: the locked pre-reg content module is loaded and ASSERTED against only if it
already defines the H_Disc_* hypothesis set. As of scaffold it still carries the
cloned v0.26 BSR study (H_PV_*); until that module is rewritten to CV.04 this
scorer prints a LOCK-DRIFT WARNING and runs on its own constants.
"""
import csv, json, os, sys, importlib.util, datetime
import numpy as np
from scipy.stats import spearmanr, pearsonr, norm

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/aias")
VALIDATOR = os.path.join(ROOT, "prereg/v0_28_brand_validator.csv")
PANEL = os.path.join(ROOT, "prereg/v0_28_panel_brands.txt")
PRESENCE = os.path.join(ROOT, "osf/v28/data/v0.28_presence.csv")
PREREG = os.path.join(ROOT, "prereg/v0_28_tech_brand_discriminant_content.py")
OUT = os.path.join(ROOT, "osf/v28/v28_verdicts.json")

# ---- LOCKED constants (pre-reg r1) ------------------------------------------
SEED = 280400
CONVERGENT_BENCHMARK = 0.74
CONFIRMED_CEIL = 0.50          # |rho| below -> CONFIRMED
N_BOOT = 10000
MIN_N = 12
RNG = np.random.default_rng(SEED)


# ---- IO ---------------------------------------------------------------------
def load_validator(path):
    out = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            b = row["brand"].strip()
            out[b] = {
                "familiarity": _f(row.get("familiarity_1_7")),
                "dprime": _f(row.get("dprime")),
            }
    return out


def load_presence(path):
    """brand -> presence float. Accepts 'presence' or 'C_P' column."""
    if not os.path.exists(path):
        return None
    out = {}
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        col = "presence" if "presence" in r.fieldnames else (
            "C_P" if "C_P" in (r.fieldnames or []) else None)
        if col is None:
            return None
        for row in r:
            v = _f(row.get(col))
            if v is not None:
                out[row["brand"].strip()] = v
    return out


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _match(brand, presence):
    """exact then case-insensitive presence lookup."""
    if brand in presence:
        return presence[brand]
    low = {k.lower(): v for k, v in presence.items()}
    return low.get(brand.lower())


# ---- BCa bootstrap ----------------------------------------------------------
def bca_ci(x, y, statfn, alpha=0.05):
    """Bias-corrected and accelerated 95% CI. Returns (lo, hi) or None."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    theta_hat = statfn(x, y)
    if not np.isfinite(theta_hat):
        return None
    boots = []
    for _ in range(N_BOOT):
        idx = RNG.integers(0, n, n)
        xb, yb = x[idx], y[idx]
        if np.std(xb) == 0 or np.std(yb) == 0:
            continue
        t = statfn(xb, yb)
        if np.isfinite(t):
            boots.append(t)
    boots = np.asarray(boots)
    if len(boots) < 100:
        return None
    # bias correction z0
    prop = np.mean(boots < theta_hat)
    prop = min(max(prop, 1.0 / (len(boots) + 1)), 1.0 - 1.0 / (len(boots) + 1))
    z0 = norm.ppf(prop)
    # acceleration via jackknife
    jack = np.empty(n)
    for i in range(n):
        m = np.ones(n, bool)
        m[i] = False
        jack[i] = statfn(x[m], y[m])
    jbar = jack.mean()
    den = 6.0 * (np.sum((jbar - jack) ** 2) ** 1.5)
    a = (np.sum((jbar - jack) ** 3) / den) if den != 0 else 0.0
    zlo, zhi = norm.ppf(alpha / 2), norm.ppf(1 - alpha / 2)

    def adj(z):
        return norm.cdf(z0 + (z0 + z) / (1 - a * (z0 + z)))

    lo = float(np.percentile(boots, 100 * adj(zlo)))
    hi = float(np.percentile(boots, 100 * adj(zhi)))
    return (lo, hi)


def abs_interval(ci):
    """Map a signed-rho CI to the |rho| interval it covers."""
    lo, hi = ci
    if lo <= 0 <= hi:
        return 0.0, max(abs(lo), abs(hi))
    return min(abs(lo), abs(hi)), max(abs(lo), abs(hi))


# ---- verdict ----------------------------------------------------------------
def disc_block(presence, yvals):
    """Compute the discriminant block for paired (presence, y) lists."""
    xy = [(p, y) for p, y in zip(presence, yvals) if p is not None and y is not None]
    n = len(xy)
    if n == 0:
        return {"status": "NOT_RUN", "n": 0,
                "note": "no Presence data joined (acquisition pending)"}
    x = np.array([p for p, _ in xy], float)
    y = np.array([v for _, v in xy], float)
    if n < MIN_N:
        return {"status": "UNDETERMINED", "n": n, "reason": "n < %d" % MIN_N}

    rho, p_s = spearmanr(x, y)
    r_p, p_p = pearsonr(x, y)
    ci = bca_ci(x, y, lambda a, b: spearmanr(a, b)[0])
    arho = abs(rho)

    if arho < CONFIRMED_CEIL:
        point = "CONFIRMED"
    elif arho < CONVERGENT_BENCHMARK:
        point = "PARTIAL"
    else:
        point = "FALSIFIED"

    flags = {"negative_correlation": bool(rho < 0)}
    status = point
    if ci is not None:
        amin, amax = abs_interval(ci)
        spans_all = (amin < CONFIRMED_CEIL) and (amax >= CONVERGENT_BENCHMARK)
        flags["ci_abs_interval"] = [round(amin, 3), round(amax, 3)]
        flags["ci_straddles_boundary"] = bool(
            (amin < CONFIRMED_CEIL <= amax) or (amin < CONVERGENT_BENCHMARK <= amax))
        flags["ci_excludes_reducibility"] = bool(amax < CONVERGENT_BENCHMARK)
        if spans_all:
            status = "UNDETERMINED"
            flags["undetermined_reason"] = "BCa CI spans all three |rho| bands"
        flags["provisional"] = bool(point == "CONFIRMED"
                                    and not flags["ci_excludes_reducibility"])
    else:
        flags["ci_excludes_reducibility"] = None
        flags["provisional"] = bool(point == "CONFIRMED")  # no CI -> provisional

    return {
        "status": status, "point_verdict": point, "n": n,
        "spearman_rho": round(float(rho), 4), "spearman_p": round(float(p_s), 5),
        "pearson_r": round(float(r_p), 4), "pearson_p": round(float(p_p), 5),
        "abs_rho": round(arho, 4),
        "bca_ci_95": [round(ci[0], 4), round(ci[1], 4)] if ci else None,
        "flags": flags,
        "bands": "CONFIRMED |rho|<0.50 | PARTIAL 0.50-0.74 | FALSIFIED >=0.74",
    }


def dissociation_block(brands, presence, fam):
    """Within-panel z(Presence)-z(familiarity) dissociation (DESCRIPTIVE)."""
    trip = [(b, p, f) for b, p, f in zip(brands, presence, fam)
            if p is not None and f is not None]
    n = len(trip)
    if n == 0:
        return {"tier": "DESCRIPTIVE", "status": "NOT_RUN", "n": 0,
                "note": "no Presence data joined (acquisition pending)"}
    pv = np.array([p for _, p, _ in trip], float)
    fv = np.array([f for _, _, f in trip], float)
    if pv.std() == 0 or fv.std() == 0:
        return {"tier": "DESCRIPTIVE", "status": "UNDETERMINED", "n": n,
                "note": "zero variance in Presence or familiarity"}
    zp = (pv - pv.mean()) / pv.std()      # population z within the panel
    zf = (fv - fv.mean()) / fv.std()
    diff = zp - zf
    amplified, suppressed = [], []
    for (b, _, _), d in zip(trip, diff):
        if d > 1.0:
            amplified.append((b, round(float(d), 3)))   # Presence >> familiarity
        elif d < -1.0:
            suppressed.append((b, round(float(d), 3)))  # familiarity >> Presence
    cases = len(amplified) + len(suppressed)
    if cases >= 4 and amplified and suppressed:
        pattern = "FULL"
    elif cases == 0:
        pattern = "ABSENT"
    else:
        pattern = "PARTIAL"
    return {
        "tier": "DESCRIPTIVE", "status": pattern, "n": n,
        "n_cases": cases,
        "amplified": amplified, "suppressed": suppressed,
        "note": ("Mechanically coupled to H_Disc_Familiarity; corroborating/"
                 "illustrative, NOT independent. Non-gating; excluded from headline."),
    }


# ---- main -------------------------------------------------------------------
def main():
    validator = load_validator(VALIDATOR)
    panel = [l.strip() for l in open(PANEL) if l.strip()]
    presence = load_presence(PRESENCE)

    # ordered by the frozen panel file; fall back to validator order
    order = [b for b in panel if b in validator] or list(validator)
    fam = [validator[b]["familiarity"] for b in order]
    dpr = [validator[b]["dprime"] for b in order]
    pres = ([_match(b, presence) for b in order] if presence else [None] * len(order))

    # lock-drift guard: assert the locked module's contract and that its numeric
    # constants match this implementation (lock is the single source of truth).
    lock_status = "absent"
    if os.path.exists(PREREG):
        spec = importlib.util.spec_from_file_location("prereg_v28", PREREG)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        hyp = set(getattr(m, "HYPOTHESES", {}))
        if {"H_Disc_Familiarity", "H_Disc_Recognition", "H_Dissociation"} <= hyp:
            lock_status = "matched"
            sc = getattr(m, "SCORING", {})
            mism = []
            if getattr(m, "CONVERGENT_BENCHMARK", CONVERGENT_BENCHMARK) != CONVERGENT_BENCHMARK:
                mism.append("benchmark")
            if getattr(m, "CONFIRMED_CEIL", CONFIRMED_CEIL) != CONFIRMED_CEIL:
                mism.append("confirmed_ceil")
            if sc.get("bootstrap_seed", SEED) != SEED:
                mism.append("seed")
            if sc.get("min_n_for_valid_rho", MIN_N) != MIN_N:
                mism.append("min_n")
            if sc.get("bootstrap_resamples", N_BOOT) != N_BOOT:
                mism.append("n_boot")
            if sc.get("band_on") not in (None, "abs(rho)"):
                mism.append("band_on")
            if sc.get("primary_family") not in (None, ["H_Disc_Familiarity", "H_Disc_Recognition"]):
                mism.append("primary_family")
            if mism:
                lock_status = "CONSTANT-DRIFT vs lock: %s" % ",".join(mism)
        else:
            lock_status = "DRIFT: module still defines %s" % sorted(hyp)

    res = {
        "H_Disc_Familiarity": {"role": "PRIMARY", **disc_block(pres, fam)},
        "H_Disc_Recognition": {"role": "SECONDARY", **disc_block(pres, dpr)},
        "H_Dissociation": {"role": "TERTIARY", **dissociation_block(order, pres, fam)},
    }

    meta = {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "study": "v0.28 / CV.04 BRAND discriminant validator",
        "seed": SEED, "n_boot": N_BOOT, "min_n": MIN_N,
        "convergent_benchmark": CONVERGENT_BENCHMARK,
        "panel_n": len(order),
        "presence_present": presence is not None,
        "presence_n_joined": sum(p is not None for p in pres),
        "lock_module": lock_status,
        "validator_sha_note": "familiarity_1_7 + dprime frozen in v0_28_brand_validator.csv",
    }
    out = {"_meta": meta, "verdicts": res}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)

    # console summary
    print("=== v0.28 / CV.04 discriminant scoring ===")
    if lock_status != "matched":
        print("  ** LOCK-DRIFT WARNING: %s" % lock_status)
        print("     (rewrite prereg/v0_28_tech_brand_discriminant_content.py to the")
        print("      CV.04 H_Disc_* study before pre-reg r1 lock)")
    if presence is None:
        print("  ** SMOKE TEST: no Presence CSV at %s" % PRESENCE)
        print("     Presence-dependent verdicts -> NOT_RUN (acquisition pending)")
    for hid in ["H_Disc_Familiarity", "H_Disc_Recognition", "H_Dissociation"]:
        r = res[hid]
        extra = ""
        if "spearman_rho" in r:
            extra = "  rho=%.3f |rho|=%.3f n=%d CI=%s" % (
                r["spearman_rho"], r["abs_rho"], r["n"], r["bca_ci_95"])
        elif "n_cases" in r:
            extra = "  cases=%d (amp=%d supp=%d)" % (
                r["n_cases"], len(r["amplified"]), len(r["suppressed"]))
        print("  %-20s %-6s %-12s%s" % (hid, r["role"], r["status"], extra))
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
