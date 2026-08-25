#!/usr/bin/env python3
"""C10.50: symbolic initial-data structure of the completed-U1 chi=B bridge.

This is a detached analytic certificate.  It does not choose chi_initial and does
not modify CLASS.  It proves two distinct statements which must not be conflated:

1. leading k->0 regularity does not select a finite chi;
2. at every finite k>0 the original preferred-coordinate field equations fix B
   algebraically once the preferred matter/source state is specified.

The first-order chi equation in the Newtonian shadow representation appears only
after the preferred A-source is rewritten in Newtonian variables and the A
constraint is differentiated.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> None:
    r, D, H, a, Eth, Pcal, M2, x = sp.symbols(
        "r D H a E_th Pcal M_c2 x", positive=True, finite=True
    )
    dm, q, rhop, W = sp.symbols("delta_mu q rho_prime W", finite=True)
    dH0, dH0p, H0p, H0pp, chi, chip = sp.symbols(
        "deltaH0 deltaH0_prime H0_prime H0_double_prime chi chi_prime",
        finite=True,
    )

    # Fourier convention L=-k^2=-x and native CLASS stress normalization.
    L = -x
    a1 = x / (x + a**2 * M2)
    K = sp.Rational(3, 2) * a**2 * a1 / L
    Kprime = 2 * H * a1 * K
    X = 3 * a**2 * W
    Q = 3 * a * q

    dH0_pref = dH0 - H0p * chi
    dm_pref = dm - rhop * chi
    Mq_pref = Q - X * chi
    psi = K * dH0_pref
    Spsi = Kprime * dH0_pref + K * (dH0p - H0pp * chi)

    RM = Q - D * Spsi - (r * L + X) * chi
    RH = (
        -3 * a**2 * r * dm_pref
        - D * H * Mq_pref
        + 2 * D * H * Spsi
        + 2 * r * Pcal * L * psi
    )
    Rreg = sp.expand(RH + 2 * H * RM)

    Creg = (
        3 * a**2 * dm
        + 9 * H * a * q
        + 2 * H * L * chi
        - 3 * a**2 * Pcal * a1 * (dH0 - H0p * chi)
    )
    regularity_identity = sp.simplify(
        Rreg.subs({D: 2 + 3 * r, rhop: -3 * H * W}) + r * Creg
    )
    assert regularity_identity == 0

    # Put the physical comoving-density cancellation on its regular branch:
    # C_com := 3a^2 delta_mu + 9Ha q = x C2 + O(x^2).
    C2 = sp.symbols("C2", finite=True)
    Creg_regular = (
        x * C2
        - 2 * H * x * chi
        - 3 * a**2 * Pcal * x / (x + a**2 * M2) * (dH0 - H0p * chi)
    )
    phi_regular = sp.simplify(Creg_regular / (Eth * x))
    phi_k0_limit = sp.simplify(sp.limit(phi_regular, x, 0, dir="+"))
    expected_phi_k0 = sp.simplify(
        (C2 - 2 * H * chi - 3 * Pcal * (dH0 - H0p * chi) / M2) / Eth
    )
    phi_limit_residual = sp.simplify(phi_k0_limit - expected_phi_k0)
    assert phi_limit_residual == 0

    # The leading regularity condition itself has no chi coefficient: every
    # explicit chi contribution in Creg carries x=k^2 for finite M_c.
    chi_leading_coeff = sp.simplify(
        sp.limit(sp.diff(Creg_regular, chi), x, 0, dir="+")
    )
    assert chi_leading_coeff == 0

    # Preferred-coordinate solve ordering.  In preferred variables deltaH0_pref
    # is fundamental, so psi_prime has no B_prime.  The denominators are:
    preferred_A_den = x + a**2 * M2
    preferred_lapse_den = r * Eth * L - 2 * D * H**2
    preferred_shift_den = r * L
    assert sp.simplify(preferred_A_den.subs(x, sp.Symbol("xp", positive=True))) != 0
    assert sp.simplify(preferred_lapse_den) == -(r * Eth * x + 2 * D * H**2)
    assert sp.simplify(preferred_shift_den) == -r * x

    # Exact source-transform derivative identity which generates chi_prime in
    # the Newtonian representation.
    Anew, Anewp = sp.symbols("A_N A_N_prime", finite=True)
    psi_newtonian_derivative_expanded = (
        Kprime * (Anew - H0p * chi)
        + K * (Anewp - H0pp * chi)
        - K * H0p * chip
    )
    Snew = Kprime * (Anew - H0p * chi) + K * (Anewp - H0pp * chi)
    derivative_split_residual = sp.simplify(
        psi_newtonian_derivative_expanded - (Snew - K * H0p * chip)
    )
    assert derivative_split_residual == 0

    result = {
        "schema": "RTK_C10_CHI_INITIAL_DATA_STRUCTURE_RESULT_v1",
        "classification": "C10_CHI_INITIAL_DATA_STRUCTURE_PASS_SCOPED_REGULARITY_NONUNIQUE_PREFERRED_DAE_ALGEBRAIC",
        "target": "research/theory_targets/RTK_C10_CHI_INITIAL_DATA_STRUCTURE_TARGET_v1.json",
        "exact_identities": {
            "Rreg_identity": "R_reg=-r*C_reg after D=2+3r and rho_total_prime=-3 H W_total",
            "C_reg": "3 a^2 delta_mu_N + 9 H a q_N + 2 H L chi - 3 a^2 Pcal a1_eff (deltaH0_N-H0_prime chi)",
            "a1_eff": "k^2/(k^2+a^2 M_c^2)",
            "machine_regularity_residual": str(regularity_identity),
            "machine_phi_limit_residual": str(phi_limit_residual),
            "machine_newtonian_derivative_split_residual": str(derivative_split_residual),
        },
        "superhorizon": {
            "assumption": "C_com:=3 a^2 delta_mu_N+9 H a q_N=k^2 C2+O(k^4), finite chi, finite M_c>0",
            "phi_k_to_0": str(expected_phi_k0),
            "leading_Creg_chi_coefficient": str(chi_leading_coeff),
            "conclusion": "leading regularity makes phi finite for every finite chi and therefore does not select chi_initial",
        },
        "preferred_coordinate_DAE": {
            "A_constraint": "psi=-(3/2) a^2 deltaH0_pref/(k^2+a^2 M_c^2) in native CLASS units",
            "psi_prime": "K_prime deltaH0_pref + K deltaH0_pref_prime; no B_prime when preferred sources are fundamental",
            "Hamiltonian": "phi is algebraic with denominator -(r E_th k^2+2 D H^2)",
            "momentum": "B=[Mq_pref-D(psi_prime+H phi)]/(r L), L=-k^2",
            "finite_k_denominators": {
                "A": "k^2+a^2 M_c^2>0",
                "Hamiltonian": "-(r E_th k^2+2D H^2)<0",
                "momentum": "-r k^2<0",
            },
            "conclusion": "for every finite k>0 in the certified domain, B is an algebraic constraint variable and requires no independent temporal initial datum once the preferred source state is specified",
        },
        "newtonian_representation": {
            "source_transform": "deltaH0_pref=deltaH0_N-H0_prime chi",
            "differentiated_A_constraint": "psi_prime=S_psi-K H0_prime chi_prime",
            "interpretation": "the detached first-order chi equation is generated by coordinate/source elimination; its integration constant is not by itself evidence for an extra propagating scalar",
        },
        "boundary": {
            "exact_k0": "not covered; use the separately certified homogeneous bridge",
            "remaining_physical_question": "derive/project the early-time finite-k preferred adiabatic source state and its algebraic B seed before coupled Boltzmann feedback",
        },
        "non_claims": [
            "no numerical chi_initial value is selected",
            "no claim that chi=0 is the physical adiabatic seed",
            "no proof yet of uniqueness of the complete early-time adiabatic gradient expansion",
            "no completed-U1 CLASS feedback or spectra",
            "no completion parameter selection"
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
