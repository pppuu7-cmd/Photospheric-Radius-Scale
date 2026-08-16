#!/usr/bin/env python3
"""Quadratic-EFT proxy audit for the implemented RTK/Khronon fluid sector.

This is intentionally NOT a proof of a ghost-free fundamental action and NOT a UV
completion.  It checks what can already be inferred from the implemented background
and perturbation equations:

1. Background barotropic consistency: the coded c_a^2 agrees numerically with dp/drho.
2. Positive fluid quadratic proxies G = rho+p and K = (rho+p)/c_a^2 on a broad grid.
3. Positive finite-k effective proxy K_eff = (rho+p)/c_s^2 whenever c_s^2>0.
4. Explicit finite-k dispersion diagnostic.  Since the implementation uses
      c_s^2(k)=c_a^2/[1+(k/k_*)^2],
   the finite-k sector cannot be identified with a pure local two-derivative P(X)
   scalar without additional higher-derivative / auxiliary EFT structure.

The output therefore separates background-level P(X)-compatibility proxies from the
still-open theorem tasks: a derived quadratic action, Hamiltonian boundedness, strong
coupling scale, radiative stability and UV completion.
"""

import json
import math

LAMBDAS = [1e-6, 1e-4, 1e-2, 1.0, 1e2, 1e4, 1e6, 1e8]
XS = [10.0 ** (p / 2.0) for p in range(-24, 25)]  # 1e-12 ... 1e12
KR = [0.0, 1e-6, 1e-4, 1e-2, 0.1, 1.0, 10.0, 1e2, 1e4, 1e8]


def state(lam, x):
    s = math.hypot(1.0, math.sqrt(lam) * x)
    r = x / s
    t = x / (s + 1.0)
    # Overall positive factor 2 mu_K^2 cancels from all sign/ratio tests.
    rho = x * (1.0 + t)
    pressure = r * t
    ca2 = r / (s * (s + x))
    return rho, pressure, ca2, s, r, t


def log_derivative_dp_drho(lam, x):
    # Symmetric logarithmic derivative is robust across many decades in x.
    eps = 2.0e-5
    xm = x * math.exp(-eps)
    xp = x * math.exp(+eps)
    rm, pm, *_ = state(lam, xm)
    rp, pp, *_ = state(lam, xp)
    drho = rp - rm
    if drho == 0.0:
        return math.nan
    return (pp - pm) / drho


violations = []
max_ca2_rel_error = 0.0
min_gradient_proxy = math.inf
min_kinetic_proxy = math.inf
min_effective_kinetic_proxy = math.inf
max_dispersion_departure = 0.0
points_background = 0
points_finite_k = 0
finite_k_px_departures = 0

for lam in LAMBDAS:
    for x in XS:
        rho, pressure, ca2, s, r, t = state(lam, x)
        enthalpy = rho + pressure
        dpdrho = log_derivative_dp_drho(lam, x)
        denom = max(abs(ca2), abs(dpdrho), 1e-300)
        rel = abs(ca2 - dpdrho) / denom if math.isfinite(dpdrho) else math.inf
        max_ca2_rel_error = max(max_ca2_rel_error, rel)
        points_background += 1

        gradient_proxy = enthalpy
        kinetic_proxy = enthalpy / ca2 if ca2 > 0.0 else math.inf
        min_gradient_proxy = min(min_gradient_proxy, gradient_proxy)
        min_kinetic_proxy = min(min_kinetic_proxy, kinetic_proxy)

        if not (
            math.isfinite(rho)
            and math.isfinite(pressure)
            and math.isfinite(ca2)
            and math.isfinite(dpdrho)
            and rho > 0.0
            and enthalpy > 0.0
            and ca2 > 0.0
            and kinetic_proxy > 0.0
            and rel < 2e-6
        ):
            violations.append({
                "kind": "background_proxy",
                "lambda_D": lam,
                "x": x,
                "rho": rho,
                "p": pressure,
                "ca2": ca2,
                "dp_drho_numeric": dpdrho,
                "relative_error": rel,
                "gradient_proxy": gradient_proxy,
                "kinetic_proxy": kinetic_proxy,
            })

        for kr in KR:
            cs2 = ca2 / (1.0 + kr * kr)
            points_finite_k += 1
            if cs2 > 0.0:
                keff = enthalpy / cs2
                min_effective_kinetic_proxy = min(min_effective_kinetic_proxy, keff)
            else:
                keff = math.inf

            ratio = cs2 / ca2
            departure = abs(1.0 - ratio)
            max_dispersion_departure = max(max_dispersion_departure, departure)
            if kr > 0.0 and departure > 1e-14:
                finite_k_px_departures += 1

            if not (
                math.isfinite(cs2)
                and cs2 > 0.0
                and cs2 <= ca2 * (1.0 + 1e-13)
                and math.isfinite(keff)
                and keff > 0.0
            ):
                violations.append({
                    "kind": "finite_k_proxy",
                    "lambda_D": lam,
                    "x": x,
                    "k_over_kstar": kr,
                    "ca2": ca2,
                    "cs2": cs2,
                    "effective_kinetic_proxy": keff,
                })

out = {
    "status": "PASS" if not violations else "FAIL",
    "classification": "PROXY_ONLY_NOT_QUADRATIC_ACTION_PROOF",
    "background_points": points_background,
    "finite_k_points": points_finite_k,
    "violations": violations[:25],
    "diagnostics": {
        "max_relative_error_ca2_vs_dpdrho": max_ca2_rel_error,
        "min_gradient_proxy_rho_plus_p": min_gradient_proxy,
        "min_background_kinetic_proxy": min_kinetic_proxy,
        "min_finite_k_effective_kinetic_proxy": min_effective_kinetic_proxy,
        "max_fractional_finite_k_sound_speed_departure": max_dispersion_departure,
        "finite_k_points_incompatible_with_pure_two_derivative_PX": finite_k_px_departures,
    },
    "interpretation": {
        "background_barotropic_identity": "TESTED_NUMERICALLY",
        "background_PX_reconstruction_proxy": "COMPATIBLE_ON_SCANNED_DOMAIN",
        "fluid_gradient_proxy_positive": "TESTED_ON_SCANNED_DOMAIN",
        "fluid_kinetic_proxy_positive": "TESTED_ON_SCANNED_DOMAIN",
        "pure_two_derivative_PX_for_full_finite_k_sector": "INCOMPATIBLE_WITH_EXPLICIT_K_DEPENDENCE",
        "required_next_structure": "DERIVE_HIGHER_DERIVATIVE_OR_AUXILIARY_EFT_ACTION",
        "ghost_free_quadratic_action": "NOT_YET_DERIVED",
        "hamiltonian_boundedness": "NOT_YET_DERIVED",
        "strong_coupling_scale": "NOT_YET_DERIVED",
        "one_loop_radiative_stability": "NOT_YET_DERIVED",
        "uv_completion": "NOT_CLAIMED",
    },
}

print(json.dumps(out, indent=2, sort_keys=True))
if violations:
    raise SystemExit(2)
