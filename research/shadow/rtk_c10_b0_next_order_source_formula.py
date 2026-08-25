#!/usr/bin/env python3
"""C10.54 exact next-order source formula for the finite preferred B0.

Combines the O(k^2) preferred Hamiltonian and momentum constraints after the
leading regular branch has been imposed.  The result eliminates psi_prime,2 and
shows that B0 is controlled by the O(k^2) total comoving source coefficient plus
leading metric/A-source data.  Also proves exact preferred/Newtonian invariance
of the total comoving source under the certified source time-shift.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> None:
    r, H, a, Eth, Pcal = sp.symbols(
        "r H a E_th Pcal", positive=True, finite=True
    )
    D = 2 + 3*r
    dm2, Q2, psip2, phi0, psi0 = sp.symbols(
        "dm2 Q2 psi_prime2 phi0 psi0", finite=True
    )

    # O(x) Hamiltonian, x=k^2 and L=-x:
    # -2 D H^2 phi2-r Eth phi0
    #   = -3a^2 r dm2-D H Q2+2D H psip2-2r Pcal psi0.
    phi2 = sp.symbols("phi2", finite=True)
    ham2_residual = sp.expand(
        -2*D*H**2*phi2 - r*Eth*phi0
        - (-3*a**2*r*dm2 - D*H*Q2 + 2*D*H*psip2 - 2*r*Pcal*psi0)
    )
    phi2_solution = sp.solve(sp.Eq(ham2_residual, 0), phi2)[0]

    N2 = sp.factor(sp.simplify(Q2 - D*(psip2 + H*phi2_solution)))
    N2_expected = sp.factor(
        -r*(-Eth*phi0 + 3*H*Q2 + 2*Pcal*psi0 + 3*a**2*dm2)/(2*H)
    )
    N2_residual = sp.simplify(N2 - N2_expected)
    assert N2_residual == 0

    # Verify the cancellation of the explicit psi_prime,2 coefficient.
    psip2_coefficient = sp.simplify(sp.diff(N2, psip2))
    assert psip2_coefficient == 0

    B0 = sp.factor(sp.simplify(-N2/r))
    B0_expected = sp.factor(
        (3*a**2*dm2 + 3*H*Q2 + 2*Pcal*psi0 - Eth*phi0)/(2*H)
    )
    B0_residual = sp.simplify(B0 - B0_expected)
    assert B0_residual == 0

    q2 = sp.symbols("q2", finite=True)
    C2 = 3*a**2*dm2 + 9*H*a*q2
    B0_C2 = sp.factor(B0_expected.subs(Q2, 3*a*q2))
    B0_C2_expected = sp.factor((C2 + 2*Pcal*psi0 - Eth*phi0)/(2*H))
    C2_formula_residual = sp.simplify(B0_C2 - B0_C2_expected)
    assert C2_formula_residual == 0

    # Exact preferred/Newtonian invariance of total comoving source.
    dmP, qP, rhop, W, B = sp.symbols(
        "delta_mu_pref q_pref rho_prime W B", finite=True
    )
    dmN = dmP + rhop*B
    qN = qP + a*W*B
    Cpref = 3*a**2*dmP + 9*H*a*qP
    CN = 3*a**2*dmN + 9*H*a*qN
    comoving_shift_residual = sp.simplify(
        (CN-Cpref).subs(rhop, -3*H*W)
    )
    assert comoving_shift_residual == 0

    # Match the C10.50 finite-phi regularity formula using the leading A solve.
    M2, A0 = sp.symbols("M_c2 deltaH0_pref0", positive=True, finite=True)
    psi0_A = -sp.Rational(3, 2)*A0/M2
    B0_A = sp.simplify(B0_C2_expected.subs(psi0, psi0_A))
    regularity_rearranged = sp.simplify(
        (C2 - 3*Pcal*A0/M2 - Eth*phi0)/(2*H)
    )
    regularity_match_residual = sp.simplify(B0_A - regularity_rearranged)
    assert regularity_match_residual == 0

    result = {
        "schema": "RTK_C10_B0_NEXT_ORDER_SOURCE_FORMULA_RESULT_v1",
        "classification": "C10_B0_NEXT_ORDER_SOURCE_FORMULA_PASS_SCOPED",
        "target": "research/theory_targets/RTK_C10_B0_NEXT_ORDER_SOURCE_FORMULA_TARGET_v1.json",
        "o_k2_hamiltonian": {
            "equation": "-2 D H^2 phi2-r E_th phi0=-3a^2 r dm2-D H Q2+2D H psi_prime2-2r Pcal psi0",
            "phi2_solution": str(phi2_solution)
        },
        "N2": {
            "definition": "N2=Q2-D(psi_prime2+H phi2)",
            "closed_form": "-(r/(2H))[-E_th phi0+3H Q2+2Pcal psi0+3a^2 dm2]",
            "psi_prime2_coefficient": str(psip2_coefficient),
            "machine_residual": str(N2_residual)
        },
        "B0": {
            "from_C10_53": "B0=-N2/r",
            "closed_form": "[3a^2 dm2+3H Q2+2Pcal psi0-E_th phi0]/(2H)",
            "with_Q2_3a_q2": "[C2+2Pcal psi0-E_th phi0]/(2H)",
            "C2": "3a^2 dm2+9Ha q2",
            "machine_residual": str(B0_residual),
            "machine_C2_formula_residual": str(C2_formula_residual)
        },
        "comoving_source_coordinate_invariance": {
            "source_map": "delta_mu_N=delta_mu_pref+rho_prime B; q_N=q_pref+a W B",
            "background": "rho_prime=-3H W",
            "identity": "3a^2 delta_mu_N+9Ha q_N = 3a^2 delta_mu_pref+9Ha q_pref",
            "machine_residual": str(comoving_shift_residual),
            "consequence": "for regular B, the O(k^2) coefficient C2 is the same in preferred and Newtonian representations"
        },
        "A_constraint_match": {
            "psi0": "-(3/(2 M_c^2)) deltaH0_pref,0",
            "B0": "[C2-3Pcal deltaH0_pref,0/M_c^2-E_th phi0]/(2H)",
            "machine_C10_50_regularity_match_residual": str(regularity_match_residual),
            "interpretation": "the O(k^2) preferred constraint formula is exactly the rearranged C10.50 finite-phi regularity limit"
        },
        "minimum_next_physical_data": [
            "the physical baseline-species O(k^2) total comoving coefficient C2",
            "the leading ordinary projected A-source deltaH0_pref,0 (equivalently psi0)",
            "the leading preferred lapse phi0/primordial normalization"
        ],
        "interpretation": {
            "core": "psi_prime2 and the detailed next-order differentiated A-source cancel from B0; the physical IC problem is smaller than a full arbitrary chi ODE initialization problem",
            "architecture": "derive the physical matter adiabatic gradient coefficients, algebraically project B0, and transform the projected state to the Newtonian Boltzmann interface"
        },
        "next_gate": "derive C2 and the leading A-source/metric amplitudes from the baseline completed-U1 adiabatic matter hierarchy; do not integrate chi independently",
        "non_claims": [
            "does not yet derive C2 from individual species",
            "does not fix primordial normalization",
            "does not calculate B0 numerically",
            "does not cover exact k=0",
            "does not include massive-neutrino anisotropic stress",
            "does not implement completed-U1 CLASS feedback",
            "does not select completion parameters"
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
