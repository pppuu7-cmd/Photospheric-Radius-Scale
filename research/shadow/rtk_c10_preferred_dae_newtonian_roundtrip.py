#!/usr/bin/env python3
"""C10.51 preferred-DAE -> Newtonian/Stueckelberg exact roundtrip theorem.

The finite-k preferred-coordinate equations are solved algebraically first.  The
same state is then transformed into the Newtonian source variables consumed by
shadow-v3, while B_prime is left as an arbitrary symbolic derivative of the
coordinate/source map.  The theorem proves that shadow-v3 returns exactly that
B_prime and exactly the preferred phi.  Therefore the shadow chi_prime equation
is not an independent evolution equation on the preferred constraint manifold.
"""
from __future__ import annotations

import json
import sympy as sp


def main() -> None:
    r, D, H, a, Eth, Pcal, M2, x = sp.symbols(
        "r D H a E_th Pcal M_c2 x", positive=True, finite=True
    )
    A, Ap, dmP, qP = sp.symbols(
        "deltaH0_pref deltaH0_pref_prime delta_mu_pref q_pref", finite=True
    )
    H0p, H0pp, rhop, W, Bp = sp.symbols(
        "H0_prime H0_double_prime rho_prime W B_prime", finite=True
    )

    L = -x
    a1 = x / (x + a**2 * M2)
    K = sp.Rational(3, 2) * a**2 * a1 / L
    Kprime = 2 * H * a1 * K

    # Preferred-coordinate algebraic DAE projection.
    psiP = K * A
    psiP_prime = Kprime * A + K * Ap
    QP = 3 * a * qP
    Delta = r * Eth * L - 2 * D * H**2
    phiP = sp.simplify(
        (
            -3 * a**2 * r * dmP
            - D * H * QP
            + 2 * D * H * psiP_prime
            + 2 * r * Pcal * L * psiP
        )
        / Delta
    )
    B = sp.simplify((QP - D * (psiP_prime + H * phiP)) / (r * L))

    # Transform the same physical state to Newtonian source variables.  B_prime
    # is deliberately arbitrary here: along a trajectory it is just the time
    # derivative of the algebraic preferred B after sources/background evolve.
    deltaH0_N = A + H0p * B
    deltaH0_N_prime = Ap + H0pp * B + H0p * Bp
    delta_mu_N = dmP + rhop * B
    q_N = qP + a * W * B

    X = 3 * a**2 * W
    QN = 3 * a * q_N
    dH0_pref_roundtrip = sp.simplify(deltaH0_N - H0p * B)
    dm_pref_roundtrip = sp.simplify(delta_mu_N - rhop * B)
    q_pref_roundtrip = sp.simplify(q_N - a * W * B)
    Spsi = sp.simplify(
        Kprime * dH0_pref_roundtrip
        + K * (deltaH0_N_prime - H0pp * B)
    )

    RM = sp.simplify(QN - D * Spsi - (r * L + X) * B)
    expected_RM = sp.simplify(D * H * phiP - D * K * H0p * Bp)
    RM_residual = sp.simplify(RM - expected_RM)
    assert RM_residual == 0

    RH = sp.simplify(
        -3 * a**2 * r * dm_pref_roundtrip
        - D * H * (QN - X * B)
        + 2 * D * H * Spsi
        + 2 * r * Pcal * L * (K * dH0_pref_roundtrip)
    )
    Rreg = sp.simplify(RH + 2 * H * RM)
    phi_shadow = sp.simplify(Rreg / (r * Eth * L))
    phi_roundtrip_residual = sp.simplify(phi_shadow - phiP)
    assert phi_roundtrip_residual == 0

    y = sp.simplify(H * phi_shadow - RM / D)
    y_residual = sp.simplify(y - K * H0p * Bp)
    assert y_residual == 0
    chi_prime_shadow = sp.simplify(y / (K * H0p))
    chip_residual = sp.simplify(chi_prime_shadow - Bp)
    assert chip_residual == 0

    # Preferred residuals vanish by construction.
    momentum_pref_residual = sp.simplify(
        r * L * B - (QP - D * (psiP_prime + H * phiP))
    )
    assert momentum_pref_residual == 0
    hamiltonian_pref_residual = sp.simplify(
        Delta * phiP
        - (
            -3 * a**2 * r * dmP
            - D * H * QP
            + 2 * D * H * psiP_prime
            + 2 * r * Pcal * L * psiP
        )
    )
    assert hamiltonian_pref_residual == 0

    result = {
        "schema": "RTK_C10_PREFERRED_DAE_NEWTONIAN_ROUNDTRIP_RESULT_v1",
        "classification": "C10_PREFERRED_DAE_NEWTONIAN_ROUNDTRIP_PASS_CHI_NOT_INDEPENDENT_EVOLUTION_SCOPED",
        "target": "research/theory_targets/RTK_C10_PREFERRED_DAE_NEWTONIAN_ROUNDTRIP_TARGET_v1.json",
        "preferred_projection": {
            "psi": "K deltaH0_pref",
            "psi_prime": "K_prime deltaH0_pref+K deltaH0_pref_prime",
            "phi": "Hamiltonian algebraic solve with denominator -(r E_th k^2+2D H^2)",
            "B": "[3 a q_pref-D(psi_prime+H phi)]/(r L), L=-k^2",
            "temporal_B_initial_condition_required": False,
        },
        "newtonian_transform": {
            "deltaH0_N": "deltaH0_pref+H0_prime B",
            "deltaH0_N_prime": "deltaH0_pref_prime+H0_double_prime B+H0_prime B_prime",
            "delta_mu_N": "delta_mu_pref+rho_prime B",
            "q_N": "q_pref+a W B",
            "B_prime_status": "arbitrary derivative of the transformed algebraic B for this identity"
        },
        "exact_roundtrip": {
            "R_M": "D H phi-D K H0_prime B_prime",
            "y": "K H0_prime B_prime",
            "chi_prime_shadow": "B_prime",
            "machine_RM_residual": str(RM_residual),
            "machine_phi_roundtrip_residual": str(phi_roundtrip_residual),
            "machine_y_residual": str(y_residual),
            "machine_chi_prime_residual": str(chip_residual),
            "machine_preferred_momentum_residual": str(momentum_pref_residual),
            "machine_preferred_hamiltonian_residual": str(hamiltonian_pref_residual)
        },
        "interpretation": {
            "core": "on the finite-k preferred constraint manifold the shadow-v3 first-order chi equation exactly transports the derivative already present in the Newtonian coordinate/source transformation; it supplies no independent temporal dynamics",
            "architecture": "do not add chi as an independently integrated Boltzmann state; solve the preferred algebraic constraints per time/sample and transform the physical potentials/sources to the Newtonian interface",
            "why_detached_replay_looked_like_an_ODE": "holding Newtonian source histories externally fixed while varying chi breaks the co-transformation of deltaH0_N_prime and makes the representation identity look like a first-order evolution equation"
        },
        "next_gate": "build a detached preferred-source trajectory projector and then an opt-in DAE Boltzmann bridge; early-time matter ICs must be projected onto the preferred finite-k constraints instead of choosing chi=0",
        "non_claims": [
            "not exact k=0",
            "not yet a physical preferred early-time source-history derivation",
            "not completed-U1 CLASS feedback",
            "not a completion-parameter choice",
            "not spectra or likelihood evidence"
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
