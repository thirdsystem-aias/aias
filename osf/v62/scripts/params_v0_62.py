"""AIAS v0.62 -- the pre-registrant's open choices, one parameter each (r2 draft).

Changing a choice is a one-line edit of this file, logged in the pre-registration's change log (and, after the
lock, as a DEVIATIONS entry). acquire_v0_62.py, cost_estimate_v0_62.py, code_v0_62.py and score_v0_62.py read
these values; nothing else in the code needs to change.

HEADPHONES_OPTION (DEVIATIONS Entry 0, Part C; pre-registration section 9 question 3):
  "A"  registry unchanged, Denon included and disclosed; sensitivities S-Denon and S-Headphones   (default, r0)
  "B"  as A, but the Denon brand question (Phase A) is not asked; Denon dropped from every test (111 units)
  "C"  the headphones category (v0.19) is not collected; tests on 96 units in four categories
WINDOW: the collection window, inclusive US Central dates (pre-registration section 5.5; section 9 question 2).
  Default 2026-11-29 .. 2026-12-02 (before t5). It may never touch the machine's blackout (BLACKOUT, the v0.40
  collection, 2026-11-17 .. 2026-11-21) and must start after the lock.
"""
from datetime import date

HEADPHONES_OPTION = "A"                      # "A" | "B" | "C"
WINDOW = ("2026-11-29", "2026-12-02")        # inclusive, US Central
# r2 (pre-registrant's decision 2026-11-10 20:44 CT): category questions first in all three languages; the
# brand-question extras (Phase A, blocks 4-5) only if they fit. At r2 the HIGH estimate of the category questions
# alone ($142.06, December prices) is above the $100 cap, so the extras are OFF; the final pre-registration
# re-evaluates this once t4's recorded English usage replaces the per-call basis (cost_estimate_v0_62_r2.txt).
BRAND_EXTRAS = False                         # True: collect blocks 4-5 (Phase A) after blocks 1-3
# r3 update (pre-registrant's decision, 2026-11-12 00:48 CT, pre-registration section 9 item 7 (b)): the 88 yes/no brand
# questions (block 4: v0.19-v0.22, 792 calls) are collected, LAST, after the three category-question runs, under the
# same $80 pause and $100 stop; the 24 open brand questions (block 5: v0.23, which need the recognition judge) are not.
# The projection pause after block 1 then uses the central ratio of "core + block 4" (cost_estimate_v0_62_r3.json).
# BRAND_EXTRAS True (blocks 4-5) overrides this; both False = the three category-question runs only.
BRAND_YES_NO = True                          # True: collect block 4 (yes/no brand questions) after blocks 1-3
LANGS = ("es", "ko", "zh")                   # r2: Spanish, Korean, Chinese (Simplified, Mainland usage)

BLACKOUT = ("2026-11-17", "2026-11-21")      # inclusive, US Central: never collect (v0.40's booking)
DENON = ("v19", "Denon")                     # (substrate, brand_id) of the unit flagged in DEVIATIONS Entry 0
HEADPHONES = "v19"
# r3 (DEVIATIONS Entry 0, Part F; pre-registration section 7.5): the registry units with a Samsung-group tie found by the
# conflict-of-interest screen. Each stays in every primary test (as Denon); sensitivity S-COI removes the whole set.
# Denon: owned by Harman International (Samsung) since 2025-09-23. The other five: advertising, PR or search work for
# the brand by Cheil Worldwide (a Samsung affiliate) or its Iris agency (sources and dates in Entry 0, Part F).
# The pre-registrant may change this set before the lock (section 9); a change is a one-line edit here.
COI_FLAGGED = (("v0.19", "Denon"), ("v0.20", "Eucerin"), ("v0.22", "BMW"), ("v0.22", "Bentley"),
               ("v0.22", "Chevrolet"), ("v0.23", "Jack Daniel's"))


def validate(option=None, window=None):
    """Raise ValueError if a choice is not admissible. Returns (option, window)."""
    option = HEADPHONES_OPTION if option is None else option
    window = WINDOW if window is None else tuple(window)
    if option not in ("A", "B", "C"):
        raise ValueError(f"HEADPHONES_OPTION must be A, B or C, not {option!r}")
    a, b = date.fromisoformat(window[0]), date.fromisoformat(window[1])
    if b < a:
        raise ValueError("WINDOW ends before it starts")
    x, y = date.fromisoformat(BLACKOUT[0]), date.fromisoformat(BLACKOUT[1])
    if a <= y and b >= x:
        raise ValueError(f"WINDOW {window} overlaps the blackout {BLACKOUT}")
    return option, window


def excluded_probe(substrate, phase, brand_id, option=None):
    """True if the headphones option removes this probe from the design."""
    option = HEADPHONES_OPTION if option is None else option
    if option == "C" and substrate == HEADPHONES:
        return True
    if option == "B" and phase == "A" and (substrate, brand_id) == DENON:
        return True
    return False


def excluded_unit(substrate, brand, option=None):
    """True if the headphones option removes this unit from every test (B: Denon; C: the v0.19 category)."""
    option = HEADPHONES_OPTION if option is None else option
    if option == "C" and substrate in (HEADPHONES, "v0.19"):
        return True
    if option == "B" and substrate in (HEADPHONES, "v0.19") and brand == DENON[1]:
        return True
    return False


validate()
