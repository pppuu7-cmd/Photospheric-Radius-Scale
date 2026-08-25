#!/usr/bin/env python3
"""C10.53: determine the first gradient order that fixes finite preferred B.

At fixed a>0 and finite M_c>0, x=k^2->0 implies a1_eff=O(x).  The
preferred momentum constraint is

    -r x B = N(x),   N=Q-D(psi'+H phi),  Q=3 a q_pref.

For regular B=B0+O(x), N0 must vanish.  Combining N0=0 with the leading
Hamiltonian constraint proves that this condition is exactly the already-known
leading comoving-source regularity condition.  Therefore B0 is not fixed at
O(x^0); it is fixed by N2 in N=x N2+O(x^2): B0=-N2/r.

Detached symbolic certificate only; no production code or parameter choice.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> None:
    r, H, a = sp.symbols("r H a", positive=True, finite=True)
    D = 2 + 3*r
    dm0, q0, psip0, phi0 = sp.symbols(
        "delta_mu0 q0 psi_prime0 phi0", finite=True
    )
    Q0 = 3*a*q0

    # Leading regular-B condition from momentum: N0=0.
    N0 = sp.expand(Q0 - D*(psip0 + H*phi0))
    psip_from_N0 = sp.solve(sp.Eq(N0, 0), psip0)[0]

    # At O(x^0), both r E_th L and 2 r Pcal L psi vanish in Hamiltonian.
    ham0 = sp.expand(
        -2*D*H**2*phi0
        - (-3*a**2*r*dm0 - D*H*Q0 + 2*D*H*psip0)
    )
    ham_after_N0 = sp.factor(sp.simplify(ham0.subs(psip0, psip_from_N0)))
    expected = 3*r*(a**2*dm0 + H*Q0)
    leading_equivalence_residual = sp.simplify(ham_after_N0 - expected)
    assert leading_equivalence_residual == 0

    comoving0 = 3*a**2*dm0 + 9*H*a*q0
    comoving_equivalence_residual = sp.simplify(
        comoving0 - 3*(a**2*dm0 + H*Q0)
    )
    assert comoving_equivalence_residual == 0

    # Next-order coefficient theorem.
    x, B0, B2, N2, N4 = sp.symbols(
        "x B0 B2 N2 N4", finite=True
    )
    lhs = sp.expand(-r*x*(B0 + B2*x))
    rhs = sp.expand(x*N2 + x**2*N4)
    coeff_x_residual = sp.simplify(lhs.coeff(x, 1) - rhs.coeff(x, 1))
    B0_solution = sp.solve(sp.Eq(coeff_x_residual, 0), B0)[0]
    B0_expected = -N2/r
    B0_residual = sp.simplify(B0_solution - B0_expected)
    assert B0_residual == 0

    # The leading finite-B requirement itself contains no B0.
    leading_B0_coefficient = sp.simplify(sp.diff(N0, sp.Symbol("B0_aux")))
    assert leading_B0_coefficient == 0

    result = {
        "schema": "RTK_C10_CHI_NEXT_ORDER_ADIABATIC_REQUIREMENT_RESULT_v1",
        "classification": "C10_CHI_LEADING_CONSTRAINT_DEGENERACY_PASS_B_FIXED_AT_O_K2_SCOPED",
        "target": "research/theory_targets/RTK_C10_CHI_NEXT_ORDER_ADIABATIC_REQUIREMENT_TARGET_v1.json",
        "limit": {
            "x": "k^2 -> 0 at fixed a>0 and finite M_c>0",
            "a1_eff": "O(x)",
            "regular_B": "B=B0+O(x)"
        },
        "leading_momentum": {
            "equation": "-r x B=N(x), N=Q-D(psi_prime+H phi), Q=3 a q_pref",
            "finite_B_requirement": "N0=0",
            "N0": str(N0),
            "B0_appears": False
        },
        "leading_hamiltonian": {
            "equation": "-2 D H^2 phi0=-3 a^2 r delta_mu0-D H Q0+2 D H psi_prime0",
            "after_N0": str(ham_after_N0),
            "identity": "N0=0 plus Hamiltonian0 iff a^2 delta_mu_pref,0+H Q0=0 for r>0",
            "comoving_equivalent": "3 a^2 delta_mu_pref,0+9 H a q_pref,0=0",
            "machine_leading_equivalence_residual": str(leading_equivalence_residual),
            "machine_comoving_equivalence_residual": str(comoving_equivalence_residual)
        },
        "next_order": {
            "expansion": "N(x)=x N2+O(x^2), B=B0+O(x)",
            "coefficient_equation": "-r B0=N2",
            "B0": "-N2/r",
            "machine_B0_residual": str(B0_residual)
        },
        "interpretation": {
            "core": "the leading finite-B condition is exactly the already-required comoving-source regularity condition and supplies no independent equation for B0",
            "first_determining_order": "O(k^2) in the preferred adiabatic gradient expansion",
            "required_physical_input": "compute N2 from the self-consistent O(k^2) preferred source/metric series for the baseline species and then set B0=-N2/r",
            "forbidden_shortcut": "do not set B0 or chi_initial to zero by convenience"
        },
        "next_gate": "derive the baseline preferred-coordinate O(k^2) adiabatic gradient series for baryons, photons, massless relativistic species and neutral RTK/Khronon; massive-neutrino anisotropic stress remains separate",
        "non_claims": [
            "does not calculate N2 or B0 numerically",
            "does not prove uniqueness of the complete adiabatic series",
            "does not cover exact k=0",
            "does not include massive-neutrino anisotropic stress",
            "does not implement completed-U1 CLASS feedback",
            "does not select completion parameters",
            "does not provide spectra or likelihood evidence"
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
