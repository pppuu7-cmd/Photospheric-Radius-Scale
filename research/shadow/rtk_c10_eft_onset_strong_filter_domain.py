#!/usr/bin/env python3
"""C10.55 control of the fixed-a strong-filter gradient domain.

Shows explicitly that k->0 at fixed finite a and a->0 at fixed finite k do not
commute for the elliptic filter, then proves that the already-certified
history-wide M_c lower window places the declared cosmological EFT domain at
z=k_phys^2/M_c^2<=1/99.  This is a domain theorem, not a numerical parameter
selection and not an extrapolation before the EFT onset.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> None:
    k, a, Mc = sp.symbols("k a M_c", positive=True, finite=True)
    a1 = k**2/(k**2+a**2*Mc**2)
    lim_k0 = sp.limit(a1, k, 0, dir="+")
    lim_a0 = sp.limit(a1, a, 0, dir="+")
    assert lim_k0 == 0
    assert lim_a0 == 1

    z = sp.symbols("z", nonnegative=True, finite=True)
    a1z = z/(1+z)
    zmax = sp.Rational(1, 99)
    a1max = sp.simplify(a1z.subs(z, zmax))
    assert a1max == sp.Rational(1, 100)

    # K_hat = -(3/(2 M_c^2))/(1+z).  Relative error of the O(z)
    # truncation K0(1-z) with respect to the exact K is exactly z^2.
    K0 = sp.symbols("K0", nonzero=True, finite=True)
    Kexact = K0/(1+z)
    Ktrunc = K0*(1-z)
    Krel = sp.factor(sp.simplify((Ktrunc-Kexact)/Kexact))
    assert Krel == -z**2
    Krel_abs_max = zmax**2

    # Leading a1 approximation is z; relative error wrt exact a1 is z.
    a1lead = z
    a1_rel = sp.factor(sp.simplify((a1lead-a1z)/a1z))
    assert a1_rel == z
    a1_rel_max = zmax

    result = {
        "schema": "RTK_C10_EFT_ONSET_STRONG_FILTER_DOMAIN_RESULT_v1",
        "classification": "C10_EFT_ONSET_STRONG_FILTER_GRADIENT_DOMAIN_PASS_SCOPED",
        "target": "research/theory_targets/RTK_C10_EFT_ONSET_STRONG_FILTER_DOMAIN_TARGET_v1.json",
        "noncommuting_limits": {
            "filter": "a1_eff=k^2/(k^2+a^2 M_c^2)",
            "k_to_0_fixed_a": str(lim_k0),
            "a_to_0_fixed_k": str(lim_a0),
            "conclusion": "the IR fixed-a gradient branch cannot be extrapolated to an arbitrarily early a->0 limit at fixed k"
        },
        "history_window_implication": {
            "parent_bound": "M_c^2>=99 k_cos_phys^2 and k_phys^2<=k_cos_phys^2",
            "z": "k_phys^2/M_c^2",
            "z_max": "1/99",
            "a1_eff_max": "1/100",
            "proof": "z<=1/99 => z/(1+z)<=1/100"
        },
        "gradient_control": {
            "K_exact": "K0/(1+z), K0=-3/(2 M_c^2)",
            "K_O_z": "K0(1-z)",
            "K_relative_truncation_error_exact": str(Krel),
            "K_relative_truncation_error_abs_max": str(Krel_abs_max),
            "K_relative_truncation_error_abs_max_float": float(Krel_abs_max),
            "a1_leading": "z",
            "a1_relative_error_exact": str(a1_rel),
            "a1_relative_error_max": str(a1_rel_max),
            "a1_relative_error_max_float": float(a1_rel_max),
            "guard": "production/projector calculations use exact a1_eff; these bounds certify the analytic expansion hierarchy only"
        },
        "interpretation": {
            "core": "the previously certified history-wide M_c lower window uniformly places the declared cosmological EFT domain in the strongly-filtered branch used by C10.50-C10.54",
            "EFT_boundary": "a finite a_EFT/onset remains mandatory; no theorem here extends the same IR completion into the formal a->0 fixed-k regime"
        },
        "next_gate": "derive the physical baseline-species O(k^2) adiabatic C2 coefficient on this finite-onset strong-filter branch, then project B0 with C10.54",
        "non_claims": [
            "no numerical M_c or a_EFT selection",
            "no UV extrapolation before EFT onset",
            "no baseline-species C2 derivation",
            "not exact k=0",
            "no completed-U1 CLASS feedback, spectra or likelihood"
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
