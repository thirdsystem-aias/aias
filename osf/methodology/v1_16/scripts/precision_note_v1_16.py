#!/usr/bin/env python3
"""Section 7 of PRE_REGISTRATION_v1_16.md: analytic precision note (no data). Fisher z with the
Bonett-Wright variance (1 + rho^2/2)/(n - 3), as v1.14 section 7. Joint probabilities over the four
separability waves multiply the single-wave probabilities (independence assumed; the same brands enter
every wave, so this is a rough guide only). n per wave: the units at the rating floor with P counted by the
input parity (t1 55, t2 54, t3 54, t4 71)."""
import json
from math import atanh, erf, sqrt


def Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def p_conf(n, rho, c=0.30):
    sd = sqrt((1 + rho * rho / 2) / (n - 3))
    return Phi((atanh(c) - atanh(rho)) / sd) - Phi((-atanh(c) - atanh(rho)) / sd)


def p_fals(n, rho, f=0.50):
    sd = sqrt((1 + rho * rho / 2) / (n - 3))
    return 1 - Phi((atanh(f) - atanh(rho)) / sd) + Phi((-atanh(f) - atanh(rho)) / sd)


def p_ge(n, rho, c=0.50):
    sd = sqrt((1 + rho * rho / 2) / (n - 3))
    return 1 - Phi((atanh(c) - atanh(rho)) / sd)


NS = {"t1": 55, "t2": 54, "t3": 54, "t4": 71}
out = {"method": "Fisher z, Bonett-Wright variance; analytic; joint = product over waves (independence assumed)",
       "separability": [], "retest": []}
for rho in (0.0, 0.10, 0.15, 0.20, 0.25, 0.30):
    per = {w: p_conf(n, rho) for w, n in NS.items()}
    joint_conf = 1.0
    joint_no_fals = 1.0
    for w, n in NS.items():
        joint_conf *= per[w]
        joint_no_fals *= 1 - p_fals(n, rho)
    out["separability"].append({"true_rho": rho, "P_conf_per_wave": per, "P_all_four_confirmed": joint_conf,
                                "P_any_wave_falsified": 1 - joint_no_fals})
for n in (40, 50):
    for rho in (0.40, 0.50, 0.60, 0.70):
        out["retest"].append({"n": n, "true_rho": rho, "P_rho_hat_ge_0.50": p_ge(n, rho),
                              "P_rho_hat_lt_0.30": 1 - p_ge(n, rho, 0.30)})
print(json.dumps(out, indent=1))
