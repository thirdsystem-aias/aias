"""Arm A fixed parameters (pre-registration r4, sections 2.1, 4.1, 5.1-5.4, 6.2). One place; every script imports it.
Changing any value after the lock is a dated DEVIATIONS entry."""
from pathlib import Path

ARM = Path(__file__).resolve().parents[1]          # osf/arm_a
ROOT = ARM.parents[1]                              # repository root (worktree)
REG = ARM / "registries"
DATA = ARM / "data"
RAW = DATA / "raw"                                 # raw/pull{1,2,3}/hro_{domain}_{UTC}.json (section 6.1)
ANCHOR = ARM / "anchor" / "osf_anchor_arm_a.json"  # written only after the lock is pushed and deposited
STUDY_TAG = "arm-a-prereg-r1"

# --- DataForSEO request (section 4.1) -------------------------------------------------------------------------
API_HOST = "https://api.dataforseo.com"
ENDPOINT = "/v3/dataforseo_labs/google/historical_rank_overview/live"
LOCATION_CODE = 2840
LANGUAGE_CODE = "en"
PRICE_PAGE = "https://dataforseo.com/pricing/dataforseo-labs/historical-rank"

# --- prices and limits (sections 5.1, 5.4) --------------------------------------------------------------------
PRICE_PER_REQUEST = 0.12
PRICE_PER_MONTH = 0.0012
PER_PULL_LIMIT = 13.00
HARD_STOP = 48.00            # cumulative, all pulls and retries; checked before every request
FIRST_COST_TOL = 0.005       # first request: |cost - (0.12 + 0.0012 x months)| above this stops the pull
MAX_REQUEST_COST = 0.20      # any single request above this stops the pull
RETRY_WAIT_S = 60            # one retry per failed request, after 60 s
MAX_RETRIES = 1
CEILING = 50.00              # the balance Pablo adds once; never fully drawn

# --- pull calendar (section 5.2, mode C) ----------------------------------------------------------------------
# months planned = calendar months from date_from to the pull month, both included (the partial pull month is
# returned and charged); a pull run on a fallback date has its own planned count by the same rule.
PULLS = {
    1: {"planned": "2026-12-07", "latest": "2026-12-31", "date_from": "2024-11-01", "mode": "full"},
    2: {"planned": "2027-01-04", "latest": "2027-01-29", "date_from": "2026-11-01", "mode": "incremental"},
    3: {"planned": "2027-03-01", "latest": "2027-04-05", "date_from": "2024-11-01", "mode": "full"},
}
N_DOMAINS = 76

# --- analysis (sections 2.1-2.12, 6.2-6.4) --------------------------------------------------------------------
SEEDS = {"H_A1": 610001, "H_A2": 610002, "H_A3": 610003, "H_A4": 610004, "H_A5": 610005, "H_A6": 610006,
         "H_A7": 610007, "boot_A1": 610011, "boot_A3": 610013, "boot_A4": 610014, "sens": 610020}
N_PERM = 10_000
N_BOOT = 10_000
ALPHA = 0.05
THRESHOLD = 0.30
MIN_POOL_N = 8               # categories with fewer analysable brands are shown, not pooled
MIN_CATEGORIES_A1 = 3
ZERO_OFFSET = 0.5            # H_A2 zero rule for R; sensitivity offsets below
ZERO_OFFSETS_SENS = (0.25, 1.0)
BREAK_MEDIAN = 0.40          # section 6.2: |median dg| above this flags a month
BREAK_MOVE = 0.20            # ... or at least 80% of domains move by more than 0.2 in the same direction
BREAK_SHARE = 0.80
RESTATE_SMALL, RESTATE_BIG, RESTATE_SHARE = 0.01, 0.10, 0.20   # section 6.1

# AI waves: month that ends each three-month window (section 2.1, 3.5, 6.3)
WAVE_MONTH = {"t1": (2026, 5), "t3": (2026, 11), "t4": (2026, 11), "t5": (2026, 12), "t6": (2027, 2),
              "v0.40": (2026, 11), "v0.24": (2026, 5)}
CATEGORY_WAVE = {"cars": "t1", "airlines": "v0.40", "banks": "v0.40", "software": "v0.24"}
H_A7_DEADLINE = "2027-03-31"

CAR_GROUPS = {"luxury": 7, "mass": 7, "electric": 4}
# S-COI (section 6.5): sample brands with a recorded Cheil Worldwide / Iris tie (v0.62 DEVIATIONS Entry 0, Part F)
COI_FLAGGED = ("BR-00385", "BR-00376", "BR-00374", "BR-00396")    # Chevrolet, BMW, Bentley, Jack Daniel's
