#!/usr/bin/env python3
"""C10.52 executable preferred-coordinate completed-U1 metric projector.

The projector consumes a preferred-coordinate source snapshot and solves the
finite-k scalar constraints algebraically in the certified order

    A constraint -> Hamiltonian -> momentum.

It deliberately has no chi/B time-integration state.  Physical Newtonian
potentials are returned as outputs through the already-certified metric bridge.
Exact k=0 remains on the separate homogeneous bridge.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Any, Dict

from rtk_c10_completed_metric_shadow_v3_class_units import (
    HomogeneousModeRequired,
    NewtonianSources,
    OutsideCertifiedDomain,
    ShadowBackground,
    ShadowParameters,
    solve_metric_mode,
)


@dataclass(frozen=True)
class PreferredSources:
    deltaH0_pref: float
    deltaH0_pref_prime: float
    delta_mu_pref: float
    q_pref: float
    delta_p_pref: float
    Pi_pref: float


@dataclass(frozen=True)
class PreferredProjection:
    k: float
    a1_eff: float
    K_hat: float
    K_hat_prime: float
    psi_pref: float
    psi_prime_pref: float
    phi_pref: float
    B_pref: float
    Phi_N: float
    Psi_N: float
    A_constraint_residual: float
    hamiltonian_residual: float
    momentum_residual: float
    filter_denominator: float
    lapse_denominator: float
    shift_denominator: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _validate(k: float, p: ShadowParameters, b: ShadowBackground) -> None:
    if k == 0.0:
        raise HomogeneousModeRequired("exact k=0 must use the homogeneous bridge")
    if k < 0.0:
        raise OutsideCertifiedDomain("k must be positive")
    if b.a <= 0.0:
        raise OutsideCertifiedDomain("a must be positive")
    if p.M_c <= 0.0:
        raise OutsideCertifiedDomain("C10.52 projector certificate requires M_c>0")
    if p.lambda_hl <= 1.0:
        raise OutsideCertifiedDomain("lambda_hl must be >1")
    if p.E_th <= 0.0:
        raise OutsideCertifiedDomain("E_th must be positive")


def project_preferred_metric(
    *,
    k: float,
    params: ShadowParameters,
    background: ShadowBackground,
    sources: PreferredSources,
) -> PreferredProjection:
    _validate(k, params, background)

    lam=params.lambda_hl; Eth=params.E_th; Mc=params.M_c
    Pcal=params.Pcal; alpha1=params.alpha1
    a=background.a; H=background.H
    r=lam-1.0; D=3.0*lam-1.0; L=-(k*k)

    filter_denominator=k*k+a*a*Mc*Mc
    a1_eff=(k*k)/filter_denominator
    K_hat=1.5*a*a*a1_eff/L
    K_hat_prime=2.0*H*a1_eff*K_hat

    psi=K_hat*sources.deltaH0_pref
    psi_prime=(
        K_hat_prime*sources.deltaH0_pref
        + K_hat*sources.deltaH0_pref_prime
    )

    Q_pref=3.0*a*sources.q_pref
    lapse_den=r*Eth*L-2.0*D*H*H
    phi_rhs=(
        -3.0*a*a*r*sources.delta_mu_pref
        -D*H*Q_pref
        +2.0*D*H*psi_prime
        +2.0*r*Pcal*L*psi
    )
    phi=phi_rhs/lapse_den

    shift_den=r*L
    B=(Q_pref-D*(psi_prime+H*phi))/shift_den

    # Physical Newtonian potentials after the exact traceless/B-prime reduction.
    Phi_N=(
        (1.0-Pcal)*phi
        +psi
        +alpha1*L*psi
        -H*B
        -3.0*a*a*sources.Pi_pref
    )
    Psi_N=psi-H*B

    A_res=filter_denominator*psi+1.5*a*a*sources.deltaH0_pref
    H_res=lapse_den*phi-phi_rhs
    M_res=shift_den*B-(Q_pref-D*(psi_prime+H*phi))

    return PreferredProjection(
        k=k,a1_eff=a1_eff,K_hat=K_hat,K_hat_prime=K_hat_prime,
        psi_pref=psi,psi_prime_pref=psi_prime,phi_pref=phi,B_pref=B,
        Phi_N=Phi_N,Psi_N=Psi_N,A_constraint_residual=A_res,
        hamiltonian_residual=H_res,momentum_residual=M_res,
        filter_denominator=filter_denominator,lapse_denominator=lapse_den,
        shift_denominator=shift_den,
    )


def _self_test() -> Dict[str, Any]:
    p=ShadowParameters(lambda_hl=1.2,E_th=2.0,M_c=0.4,Pcal=0.1,alpha1=0.01)
    b=ShadowBackground(
        a=0.8,H=0.2,H0_prime=-0.1,H0_double_prime=0.03,
        rho_total_prime=-0.18,p_total_prime=-0.02,W_total=0.3,
    )
    sP=PreferredSources(
        deltaH0_pref=0.02,deltaH0_pref_prime=-0.005,
        delta_mu_pref=0.03,q_pref=0.01,delta_p_pref=0.004,Pi_pref=0.001,
    )
    k=0.5
    proj=project_preferred_metric(k=k,params=p,background=b,sources=sP)

    # Arbitrary derivative of the already-projected coordinate transform.  The
    # C10.51 theorem says shadow-v3 must return it identically after the complete
    # source co-transformation.
    B_prime=0.007
    B=proj.B_pref
    sN=NewtonianSources(
        deltaH0_N=sP.deltaH0_pref+b.H0_prime*B,
        deltaH0_N_prime=(
            sP.deltaH0_pref_prime+b.H0_double_prime*B+b.H0_prime*B_prime
        ),
        delta_mu_N=sP.delta_mu_pref+b.rho_total_prime*B,
        q_N=sP.q_pref+b.a*b.W_total*B,
        delta_p_N=sP.delta_p_pref+b.p_total_prime*B,
        Pi_N=sP.Pi_pref,
    )
    shadow=solve_metric_mode(k=k,chi=B,params=p,background=b,sources=sN)

    errors={
        "phi_pref":abs(shadow.phi_pref-proj.phi_pref),
        "psi_pref":abs(shadow.psi_pref-proj.psi_pref),
        "chi_prime":abs(shadow.chi_prime-B_prime),
        "Phi_N":abs(shadow.Phi_N-proj.Phi_N),
        "Psi_N":abs(shadow.Psi_N-proj.Psi_N),
    }
    max_error=max(errors.values())
    preferred_residual_max=max(
        abs(proj.A_constraint_residual),
        abs(proj.hamiltonian_residual),
        abs(proj.momentum_residual),
    )
    assert max_error < 2e-13, errors
    assert preferred_residual_max < 1e-13
    assert shadow.source_roundtrip_max_abs_error < 1e-14

    k0_routed=False
    try:
        project_preferred_metric(k=0.0,params=p,background=b,sources=sP)
    except HomogeneousModeRequired:
        k0_routed=True
    assert k0_routed

    return {
        "classification":"C10_PREFERRED_METRIC_PROJECTOR_API_SELFTEST_PASS",
        "projected_state":proj.to_dict(),
        "arbitrary_transformed_B_prime":B_prime,
        "shadow_roundtrip_errors":errors,
        "shadow_roundtrip_max_abs_error":max_error,
        "preferred_constraint_max_abs_residual":preferred_residual_max,
        "shadow_source_roundtrip_max_abs_error":shadow.source_roundtrip_max_abs_error,
        "k0_routed_to_homogeneous_bridge":k0_routed,
        "architecture":"preferred finite-k algebraic constraint projection; no independently integrated chi state",
    }


if __name__ == "__main__":
    print(json.dumps(_self_test(),indent=2,sort_keys=True))
