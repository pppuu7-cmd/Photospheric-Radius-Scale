#!/usr/bin/env python3
"""Numerically reordered C10 completed-U(1) finite-k metric shadow solver.

This v2 reference keeps production CLASS untouched.  It uses the exact
elimination identity

    r E_th L phi = R_H + 2 H R_M

instead of a direct Cramer solve for (phi, chi').  The reordering removes an
avoidable high-k cancellation from the direct 2x2 representation.  Exact k=0
is still excluded and must use the separately certified homogeneous bridge.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
from typing import Any, Dict


class HomogeneousModeRequired(ValueError):
    pass


class OutsideCertifiedDomain(ValueError):
    pass


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
class ReorderedShadowSolution:
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
    y: float
    R_M: float
    R_H: float
    R_reg: float
    R_reg_over_k2: float
    reordered_phi_denominator: float
    determinant: float
    determinant_factorized: float
    filter_denominator: float
    preferred_lapse_denominator: float
    momentum_residual: float
    hamiltonian_residual: float
    source_roundtrip_max_abs_error: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _validate(k: float, p: ShadowParameters, b: ShadowBackground) -> None:
    if k == 0.0:
        raise HomogeneousModeRequired("exact k=0 must use the homogeneous bridge")
    if k < 0.0:
        raise OutsideCertifiedDomain("k must be non-negative")
    if p.G <= 0.0 or b.a <= 0.0:
        raise OutsideCertifiedDomain("G and a must be positive")
    if p.M_c < 0.0:
        raise OutsideCertifiedDomain("M_c must be non-negative")
    if p.lambda_hl <= 1.0:
        raise OutsideCertifiedDomain("certified branch requires lambda_hl>1")
    if p.E_th <= 0.0:
        raise OutsideCertifiedDomain("certified branch requires E_th>0")
    if b.H0_prime == 0.0:
        raise OutsideCertifiedDomain("current Newtonian bridge requires H0_prime!=0")


def solve_metric_mode_reordered(
    *,
    k: float,
    chi: float,
    params: ShadowParameters,
    background: ShadowBackground,
    sources: NewtonianSources,
) -> ReorderedShadowSolution:
    _validate(k, params, background)

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
    K_prime = 2.0 * H * a1_eff * K

    deltaH0_pref = sources.deltaH0_N - H0p * chi
    delta_mu_pref = sources.delta_mu_N - rhop * chi
    q_pref = sources.q_N - a * W * chi
    delta_p_pref = sources.delta_p_N - pp * chi
    Pi_pref = sources.Pi_N

    psi = K * deltaH0_pref
    S_psi = K_prime * deltaH0_pref + K * (
        sources.deltaH0_N_prime - H0pp * chi
    )

    Q_N = 8.0 * math.pi * G * a * sources.q_N
    X = 8.0 * math.pi * G * a * a * W
    Mq_pref = Q_N - X * chi

    Delta_phi = r * E_th * L - 2.0 * D * H * H

    R_M = Q_N - D * S_psi - (r * L + X) * chi
    R_H = (
        -8.0 * math.pi * G * a * a * r * delta_mu_pref
        - D * H * Mq_pref
        + 2.0 * D * H * S_psi
        + 2.0 * r * Pcal * L * psi
    )

    # Exact elimination of y=K H0' chi' from the two transformed constraints.
    R_reg = R_H + 2.0 * H * R_M
    phi_den = r * E_th * L
    if phi_den == 0.0:
        raise HomogeneousModeRequired("reordered finite-k denominator vanishes only at k=0")

    phi = R_reg / phi_den
    y = H * phi - R_M / D

    KH0p = K * H0p
    if KH0p == 0.0:
        raise OutsideCertifiedDomain("K H0_prime must be nonzero for finite-k chi-prime reconstruction")
    chi_prime = y / KH0p
    psi_prime = S_psi - y

    momentum_residual = r * L * chi - (
        Mq_pref - D * (psi_prime + H * phi)
    )
    hamiltonian_rhs = (
        -8.0 * math.pi * G * a * a * r * delta_mu_pref
        - D * H * Mq_pref
        + 2.0 * D * H * psi_prime
        + 2.0 * r * Pcal * L * psi
    )
    hamiltonian_residual = Delta_phi * phi - hamiltonian_rhs

    Phi_N = (
        (1.0 - Pcal) * phi
        + psi
        + alpha1 * L * psi
        - H * chi
        - 8.0 * math.pi * G * a * a * Pi_pref
    )
    Psi_N = psi - H * chi

    determinant = (
        D * H * (2.0 * D * H * K * H0p)
        - (-D * K * H0p) * Delta_phi
    )
    determinant_factorized = C * D * r * E_th * H0p * a1_eff

    roundtrip_errors = (
        abs((delta_mu_pref + rhop * chi) - sources.delta_mu_N),
        abs((q_pref + a * W * chi) - sources.q_N),
        abs((delta_p_pref + pp * chi) - sources.delta_p_N),
        abs(Pi_pref - sources.Pi_N),
        abs((deltaH0_pref + H0p * chi) - sources.deltaH0_N),
    )

    return ReorderedShadowSolution(
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
        y=y,
        R_M=R_M,
        R_H=R_H,
        R_reg=R_reg,
        R_reg_over_k2=R_reg/(k*k),
        reordered_phi_denominator=phi_den,
        determinant=determinant,
        determinant_factorized=determinant_factorized,
        filter_denominator=filter_denominator,
        preferred_lapse_denominator=Delta_phi,
        momentum_residual=momentum_residual,
        hamiltonian_residual=hamiltonian_residual,
        source_roundtrip_max_abs_error=max(roundtrip_errors),
    )


def _self_test() -> Dict[str, Any]:
    p = ShadowParameters(1.0, 1.2, 2.0, 0.4, 0.1, 0.01)
    b = ShadowBackground(0.8, 0.2, -0.1, 0.03, -0.2, -0.02, 0.3)
    s = NewtonianSources(0.02, -0.005, 0.03, 0.01, 0.004, 0.001)

    sol = solve_metric_mode_reordered(k=0.5, chi=0.002, params=p, background=b, sources=s)

    assert abs(sol.determinant-sol.determinant_factorized) < 2.0e-15
    assert abs(sol.momentum_residual) < 1.0e-12
    assert abs(sol.hamiltonian_residual) < 1.0e-12
    assert sol.source_roundtrip_max_abs_error < 1.0e-15
    assert sol.filter_denominator > 0.0
    assert sol.preferred_lapse_denominator < 0.0
    assert sol.reordered_phi_denominator < 0.0

    k0_routed = False
    try:
        solve_metric_mode_reordered(k=0.0, chi=0.0, params=p, background=b, sources=s)
    except HomogeneousModeRequired:
        k0_routed = True
    assert k0_routed

    return {
        "classification": "C10_SHADOW_METRIC_REORDERED_REFERENCE_SELFTEST_PASS",
        "k0_routed": k0_routed,
        "sample_solution": sol.to_dict(),
    }


if __name__ == "__main__":
    print(json.dumps(_self_test(), indent=2, sort_keys=True))
