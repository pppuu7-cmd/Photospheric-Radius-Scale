#!/usr/bin/env python3
"""Standalone C10 completed-U(1) scalar metric shadow reference solver.

This module deliberately does not import or patch production CLASS code.  It
implements only the already-frozen finite-k linear C10 source map and coupled
constraint solve documented in:

  research/theory_results/
    RTK_C10_U1_NEWTONIAN_SOURCE_TRANSFORM_POLE_AUDIT_RESULT_v1.json

Exact k=0 is intentionally rejected and must use the separately certified
homogeneous bridge.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from typing import Dict, Any


class HomogeneousModeRequired(ValueError):
    """Raised when k=0 is sent to the finite-k shadow solver."""


class OutsideCertifiedDomain(ValueError):
    """Raised when parameters leave the currently certified C10 domain."""


@dataclass(frozen=True)
class ShadowParameters:
    G: float
    lambda_hl: float
    E_th: float
    M_c: float
    Pcal: float
    alpha1: float


@dataclass(frozen=True)
class ShadowBackground:
    a: float
    H: float
    H0_prime: float
    H0_double_prime: float
    rho_total_prime: float
    p_total_prime: float
    W_total: float


@dataclass(frozen=True)
class NewtonianSources:
    deltaH0_N: float
    deltaH0_N_prime: float
    delta_mu_N: float
    q_N: float
    delta_p_N: float
    Pi_N: float


@dataclass(frozen=True)
class ShadowSolution:
    k: float
    chi: float
    chi_prime: float
    phi_pref: float
    psi_pref: float
    psi_prime_pref: float
    Phi_N: float
    Psi_N: float
    a1_eff: float
    K: float
    determinant: float
    determinant_factorized: float
    filter_denominator: float
    preferred_lapse_denominator: float
    momentum_residual: float
    hamiltonian_residual: float
    source_roundtrip_max_abs_error: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _validate_domain(k: float, p: ShadowParameters, b: ShadowBackground) -> None:
    if k == 0.0:
        raise HomogeneousModeRequired(
            "Exact k=0 belongs to the separately certified homogeneous bridge."
        )
    if k < 0.0:
        raise OutsideCertifiedDomain("k must be a non-negative comoving magnitude")
    if p.G <= 0.0:
        raise OutsideCertifiedDomain("G must be positive")
    if b.a <= 0.0:
        raise OutsideCertifiedDomain("a must be positive")
    if p.M_c < 0.0:
        raise OutsideCertifiedDomain("M_c must be non-negative")
    if p.lambda_hl <= 1.0:
        raise OutsideCertifiedDomain(
            "Current C10 finite-k rank/pole certificate assumes lambda_hl > 1"
        )
    if p.E_th <= 0.0:
        raise OutsideCertifiedDomain(
            "Current C10 finite-k rank/pole certificate assumes E_th > 0"
        )
    if b.H0_prime == 0.0:
        raise OutsideCertifiedDomain(
            "The Newtonian coupled (phi,chi') solve is singular when H0_prime=0; "
            "the certified expanding ordinary-matter branch has H0_prime<0."
        )


def solve_metric_mode(
    *,
    k: float,
    chi: float,
    params: ShadowParameters,
    background: ShadowBackground,
    sources: NewtonianSources,
) -> ShadowSolution:
    """Solve one finite-k scalar mode on the frozen C10 branch.

    Inputs are Newtonian-coordinate covariant sources plus the internal
    preferred-foliation Stueckelberg variable chi.  The routine reconstructs
    preferred-coordinate sources, solves the A constraint and the certified
    coupled (phi,chi') momentum/Hamiltonian system, then returns physical
    Newtonian potentials and diagnostics.
    """

    _validate_domain(k, params, background)

    G = params.G
    lam = params.lambda_hl
    E_th = params.E_th
    M_c = params.M_c
    Pcal = params.Pcal
    alpha1 = params.alpha1

    a = background.a
    H = background.H
    H0p = background.H0_prime
    H0pp = background.H0_double_prime
    rhop = background.rho_total_prime
    pp = background.p_total_prime
    W = background.W_total

    L = -(k * k)
    D = 3.0 * lam - 1.0
    r = lam - 1.0

    filter_denominator = k * k + a * a * M_c * M_c
    if filter_denominator <= 0.0:
        raise OutsideCertifiedDomain("k^2+a^2 M_c^2 must be positive")

    a1_eff = (k * k) / filter_denominator
    C = 4.0 * math.pi * G * a * a
    K = C * a1_eff / L

    # For constant comoving k, constant M_c and constant G:
    #   a1_eff' = -2 H a1_eff(1-a1_eff)
    #   C'      =  2 H C
    # hence K'/K = 2 H a1_eff.
    K_prime = 2.0 * H * a1_eff * K

    # Newtonian -> preferred source reconstruction.
    deltaH0_pref = sources.deltaH0_N - H0p * chi
    delta_mu_pref = sources.delta_mu_N - rhop * chi
    q_pref = sources.q_N - a * W * chi
    delta_p_pref = sources.delta_p_N - pp * chi
    Pi_pref = sources.Pi_N

    # A constraint.
    psi = K * deltaH0_pref

    # Isolate chi' in psi'.
    S_psi = (
        K_prime * deltaH0_pref
        + K * (sources.deltaH0_N_prime - H0pp * chi)
    )

    Q_N = 8.0 * math.pi * G * a * sources.q_N
    X = 8.0 * math.pi * G * a * a * W
    Mq_pref = Q_N - X * chi

    Delta_phi = r * E_th * L - 2.0 * D * H * H

    # Coupled unknown vector x=(phi, chi').
    a11 = D * H
    a12 = -D * K * H0p
    a21 = Delta_phi
    a22 = 2.0 * D * H * K * H0p

    rhs_momentum = Q_N - D * S_psi - (r * L + X) * chi
    rhs_hamiltonian = (
        -8.0 * math.pi * G * a * a * r * delta_mu_pref
        - D * H * Mq_pref
        + 2.0 * D * H * S_psi
        + 2.0 * r * Pcal * L * psi
    )

    determinant = a11 * a22 - a12 * a21
    determinant_factorized = C * D * r * E_th * H0p * a1_eff

    if determinant == 0.0:
        raise OutsideCertifiedDomain(
            "Transformed finite-k coupled determinant is exactly zero"
        )

    phi = (rhs_momentum * a22 - a12 * rhs_hamiltonian) / determinant
    chi_prime = (a11 * rhs_hamiltonian - rhs_momentum * a21) / determinant
    psi_prime = S_psi - K * H0p * chi_prime

    # Direct preferred-equation residuals.
    momentum_residual = r * L * chi - (
        Mq_pref - D * (psi_prime + H * phi)
    )

    hamiltonian_rhs_direct = (
        -8.0 * math.pi * G * a * a * r * delta_mu_pref
        - D * H * Mq_pref
        + 2.0 * D * H * psi_prime
        + 2.0 * r * Pcal * L * psi
    )
    hamiltonian_residual = Delta_phi * phi - hamiltonian_rhs_direct

    # Physical Newtonian metric outputs from the certified B'-free map.
    Phi_N = (
        (1.0 - Pcal) * phi
        + psi
        + alpha1 * L * psi
        - H * chi
        - 8.0 * math.pi * G * a * a * Pi_pref
    )
    Psi_N = psi - H * chi

    # Exact source-map round trip.
    roundtrip_errors = (
        abs((delta_mu_pref + rhop * chi) - sources.delta_mu_N),
        abs((q_pref + a * W * chi) - sources.q_N),
        abs((delta_p_pref + pp * chi) - sources.delta_p_N),
        abs(Pi_pref - sources.Pi_N),
        abs((deltaH0_pref + H0p * chi) - sources.deltaH0_N),
    )

    return ShadowSolution(
        k=k,
        chi=chi,
        chi_prime=chi_prime,
        phi_pref=phi,
        psi_pref=psi,
        psi_prime_pref=psi_prime,
        Phi_N=Phi_N,
        Psi_N=Psi_N,
        a1_eff=a1_eff,
        K=K,
        determinant=determinant,
        determinant_factorized=determinant_factorized,
        filter_denominator=filter_denominator,
        preferred_lapse_denominator=Delta_phi,
        momentum_residual=momentum_residual,
        hamiltonian_residual=hamiltonian_residual,
        source_roundtrip_max_abs_error=max(roundtrip_errors),
    )


def _self_test() -> Dict[str, Any]:
    """Deterministic algebra smoke test; not a cosmological likelihood test."""

    params = ShadowParameters(
        G=1.0,
        lambda_hl=1.2,
        E_th=2.0,
        M_c=0.4,
        Pcal=0.1,
        alpha1=0.01,
    )
    background = ShadowBackground(
        a=0.8,
        H=0.2,
        H0_prime=-0.1,
        H0_double_prime=0.03,
        rho_total_prime=-0.2,
        p_total_prime=-0.02,
        W_total=0.3,
    )
    sources = NewtonianSources(
        deltaH0_N=0.02,
        deltaH0_N_prime=-0.005,
        delta_mu_N=0.03,
        q_N=0.01,
        delta_p_N=0.004,
        Pi_N=0.001,
    )

    sol = solve_metric_mode(
        k=0.5,
        chi=0.002,
        params=params,
        background=background,
        sources=sources,
    )

    det_scale = max(1.0, abs(sol.determinant_factorized))
    det_error = abs(sol.determinant - sol.determinant_factorized) / det_scale

    assert det_error < 1.0e-14
    assert abs(sol.momentum_residual) < 1.0e-12
    assert abs(sol.hamiltonian_residual) < 1.0e-12
    assert sol.source_roundtrip_max_abs_error < 1.0e-15
    assert sol.filter_denominator > 0.0
    assert sol.preferred_lapse_denominator < 0.0
    assert sol.determinant < 0.0

    # chi=0 must make the covariant source reconstruction an identity.
    sol_chi0 = solve_metric_mode(
        k=0.5,
        chi=0.0,
        params=params,
        background=background,
        sources=sources,
    )
    assert sol_chi0.source_roundtrip_max_abs_error < 1.0e-15

    # Finite-k M_c=0 control: a1_eff must become exactly 1 in floating arithmetic.
    params_mc0 = ShadowParameters(
        G=params.G,
        lambda_hl=params.lambda_hl,
        E_th=params.E_th,
        M_c=0.0,
        Pcal=params.Pcal,
        alpha1=params.alpha1,
    )
    sol_mc0 = solve_metric_mode(
        k=0.5,
        chi=0.002,
        params=params_mc0,
        background=background,
        sources=sources,
    )
    assert sol_mc0.a1_eff == 1.0

    # Exact homogeneous mode must route away.
    k0_routed = False
    try:
        solve_metric_mode(
            k=0.0,
            chi=0.0,
            params=params,
            background=background,
            sources=sources,
        )
    except HomogeneousModeRequired:
        k0_routed = True
    assert k0_routed

    return {
        "classification": "C10_COMPLETED_GRAVITY_SHADOW_METRIC_API_REFERENCE_SELFTEST_PASS",
        "determinant": sol.determinant,
        "determinant_factorized": sol.determinant_factorized,
        "determinant_relative_error_scaled": det_error,
        "momentum_residual": sol.momentum_residual,
        "hamiltonian_residual": sol.hamiltonian_residual,
        "source_roundtrip_max_abs_error": sol.source_roundtrip_max_abs_error,
        "mc0_a1_eff": sol_mc0.a1_eff,
        "k0_routed_to_homogeneous_bridge": k0_routed,
        "sample_solution": sol.to_dict(),
    }


if __name__ == "__main__":
    print(json.dumps(_self_test(), indent=2, sort_keys=True))
