#!/usr/bin/env python3
"""C10 completed-U(1) finite-k metric shadow in native CLASS source units.

CLASS background/perturbation density variables obey
    rho_hat = (8*pi*G/3) rho_phys.
This module consumes those hatted variables directly, so no explicit G appears
in the source interface and no double-normalization is possible.

It is a detached reference solver.  It does not import or modify CLASS.
Exact k=0 remains on the separately certified homogeneous bridge.
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
    lambda_hl: float
    E_th: float
    M_c: float
    Pcal: float
    alpha1: float


@dataclass(frozen=True)
class ShadowBackground:
    a: float
    H: float                       # conformal Hubble H=a'/a
    H0_prime: float                # CLASS-normalized ordinary H0 derivative
    H0_double_prime: float
    rho_total_prime: float         # CLASS-normalized
    p_total_prime: float           # CLASS-normalized
    W_total: float                 # CLASS-normalized rho+p


@dataclass(frozen=True)
class NewtonianSources:
    deltaH0_N: float               # CLASS-normalized ordinary source
    deltaH0_N_prime: float
    delta_mu_N: float              # CLASS-normalized total density source
    q_N: float                     # (8piG/3) q_phys
    delta_p_N: float               # CLASS-normalized total pressure source
    Pi_N: float                    # (8piG/3) Pi_phys


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
    K_hat: float
    y: float
    R_M: float
    R_H: float
    R_reg: float
    R_reg_over_k2: float
    regularity_bracket: float
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
    if b.a <= 0.0:
        raise OutsideCertifiedDomain("a must be positive")
    if p.M_c < 0.0:
        raise OutsideCertifiedDomain("M_c must be non-negative")
    if p.lambda_hl <= 1.0:
        raise OutsideCertifiedDomain("current finite-k C10 certificate requires lambda_hl>1")
    if p.E_th <= 0.0:
        raise OutsideCertifiedDomain("current finite-k C10 certificate requires E_th>0")
    if b.H0_prime == 0.0:
        raise OutsideCertifiedDomain("H0_prime must be nonzero in this Newtonian solve basis")


def solve_metric_mode(
    *,
    k: float,
    chi: float,
    params: ShadowParameters,
    background: ShadowBackground,
    sources: NewtonianSources,
) -> ShadowSolution:
    _validate(k, params, background)

    lam=params.lambda_hl; Eth=params.E_th; Mc=params.M_c
    Pcal=params.Pcal; alpha1=params.alpha1
    a=background.a; H=background.H; H0p=background.H0_prime
    H0pp=background.H0_double_prime; rhop=background.rho_total_prime
    pp=background.p_total_prime; W=background.W_total

    L=-(k*k)
    D=3.0*lam-1.0
    r=lam-1.0
    filter_denominator=k*k+a*a*Mc*Mc
    if filter_denominator <= 0.0:
        raise OutsideCertifiedDomain("k^2+a^2 M_c^2 must be positive")

    a1_eff=(k*k)/filter_denominator
    # 4*pi*G*a^2 * rho_phys -> (3/2)*a^2 * rho_CLASS.
    K_hat=1.5*a*a*a1_eff/L
    K_prime=2.0*H*a1_eff*K_hat

    deltaH0_pref=sources.deltaH0_N-H0p*chi
    delta_mu_pref=sources.delta_mu_N-rhop*chi
    q_pref=sources.q_N-a*W*chi
    delta_p_pref=sources.delta_p_N-pp*chi
    Pi_pref=sources.Pi_N

    psi=K_hat*deltaH0_pref
    S_psi=K_prime*deltaH0_pref+K_hat*(sources.deltaH0_N_prime-H0pp*chi)

    # Q_N := 8*pi*G*a*q_phys = 3*a*q_hat.
    Q_N=3.0*a*sources.q_N
    X=3.0*a*a*W
    Mq_pref=Q_N-X*chi
    Delta_phi=r*Eth*L-2.0*D*H*H

    R_M=Q_N-D*S_psi-(r*L+X)*chi
    R_H=(
        -3.0*a*a*r*delta_mu_pref
        -D*H*Mq_pref
        +2.0*D*H*S_psi
        +2.0*r*Pcal*L*psi
    )

    R_reg=R_H+2.0*H*R_M
    phi_den=r*Eth*L
    if phi_den == 0.0:
        raise HomogeneousModeRequired("finite-k reordered denominator vanishes only at k=0")
    phi=R_reg/phi_den

    y=H*phi-R_M/D
    KH0p=K_hat*H0p
    if KH0p == 0.0:
        raise OutsideCertifiedDomain("K_hat*H0_prime must be nonzero")
    chi_prime=y/KH0p
    psi_prime=S_psi-y

    momentum_residual=r*L*chi-(Mq_pref-D*(psi_prime+H*phi))
    hamiltonian_rhs=(
        -3.0*a*a*r*delta_mu_pref
        -D*H*Mq_pref
        +2.0*D*H*psi_prime
        +2.0*r*Pcal*L*psi
    )
    hamiltonian_residual=Delta_phi*phi-hamiltonian_rhs

    # 8*pi*G*a^2*Pi_phys = 3*a^2*Pi_hat.
    Phi_N=(1.0-Pcal)*phi+psi+alpha1*L*psi-H*chi-3.0*a*a*Pi_pref
    Psi_N=psi-H*chi

    det=(D*H)*(2.0*D*H*K_hat*H0p)-(-D*K_hat*H0p)*Delta_phi
    det_factor=1.5*a*a*D*r*Eth*H0p*a1_eff

    # Exact lambda-independent bracket: R_reg=-r*regularity_bracket.
    regularity_bracket=(
        3.0*a*a*sources.delta_mu_N
        +9.0*H*a*sources.q_N
        +2.0*H*L*chi
        -3.0*a*a*Pcal*a1_eff*(sources.deltaH0_N-H0p*chi)
    )

    roundtrip=(
        abs((delta_mu_pref+rhop*chi)-sources.delta_mu_N),
        abs((q_pref+a*W*chi)-sources.q_N),
        abs((delta_p_pref+pp*chi)-sources.delta_p_N),
        abs(Pi_pref-sources.Pi_N),
        abs((deltaH0_pref+H0p*chi)-sources.deltaH0_N),
    )

    return ShadowSolution(
        k=k,chi=chi,chi_prime=chi_prime,phi_pref=phi,psi_pref=psi,
        psi_prime_pref=psi_prime,Phi_N=Phi_N,Psi_N=Psi_N,a1_eff=a1_eff,
        K_hat=K_hat,y=y,R_M=R_M,R_H=R_H,R_reg=R_reg,
        R_reg_over_k2=R_reg/(k*k),regularity_bracket=regularity_bracket,
        reordered_phi_denominator=phi_den,determinant=det,
        determinant_factorized=det_factor,filter_denominator=filter_denominator,
        preferred_lapse_denominator=Delta_phi,momentum_residual=momentum_residual,
        hamiltonian_residual=hamiltonian_residual,
        source_roundtrip_max_abs_error=max(roundtrip),
    )


def _self_test() -> Dict[str, Any]:
    # Convert the v2 physical-unit deterministic sample with G=1 by the exact
    # CLASS factor f=8*pi/3.  Metric solutions must be unchanged.
    f=8.0*math.pi/3.0
    p=ShadowParameters(1.2,2.0,0.4,0.1,0.01)
    b=ShadowBackground(
        a=0.8,H=0.2,H0_prime=-0.1*f,H0_double_prime=0.03*f,
        rho_total_prime=-0.2*f,p_total_prime=-0.02*f,W_total=0.3*f,
    )
    s=NewtonianSources(
        deltaH0_N=0.02*f,deltaH0_N_prime=-0.005*f,
        delta_mu_N=0.03*f,q_N=0.01*f,delta_p_N=0.004*f,Pi_N=0.001*f,
    )
    sol=solve_metric_mode(k=0.5,chi=0.002,params=p,background=b,sources=s)

    expected={
        "phi_pref":1.1611579101470877,
        "psi_pref":-0.4610046518230288,
        "chi_prime":0.06276148157284411,
        "Phi_N":0.5687050245525279,
        "Psi_N":-0.4614046518230288,
    }
    errors={name:abs(getattr(sol,name)-value) for name,value in expected.items()}
    assert max(errors.values()) < 2e-14
    assert abs(sol.determinant-sol.determinant_factorized) < 3e-15
    assert abs(sol.R_reg + (p.lambda_hl-1.0)*sol.regularity_bracket) < 3e-15
    assert abs(sol.momentum_residual) < 1e-12
    assert abs(sol.hamiltonian_residual) < 1e-12
    assert sol.source_roundtrip_max_abs_error < 1e-14

    return {
        "classification":"C10_CLASS_NORMALIZED_SHADOW_V3_SELFTEST_PASS",
        "physical_v2_regression_max_abs_error":max(errors.values()),
        "individual_regression_errors":errors,
        "determinant_factorization_abs_error":abs(sol.determinant-sol.determinant_factorized),
        "lambda_cancellation_abs_error":abs(sol.R_reg+(p.lambda_hl-1.0)*sol.regularity_bracket),
        "momentum_residual":sol.momentum_residual,
        "hamiltonian_residual":sol.hamiltonian_residual,
        "source_roundtrip_max_abs_error":sol.source_roundtrip_max_abs_error,
        "sample_solution":sol.to_dict(),
    }


if __name__ == "__main__":
    print(json.dumps(_self_test(),indent=2,sort_keys=True))
