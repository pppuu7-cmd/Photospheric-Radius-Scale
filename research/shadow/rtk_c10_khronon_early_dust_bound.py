#!/usr/bin/env python3
"""C10.56 finite-X and asymptotic early-dust bounds for production Khronon.

Uses exactly the algebra implemented in rtk/khronon_background.c. lambda_D is
the DBI parameter and is intentionally kept distinct from completion lambda_HL.
"""
from __future__ import annotations
import json
import sympy as sp


def main() -> None:
    X, ell, mu = sp.symbols("X ell mu_K", positive=True, finite=True)
    s = sp.sqrt(1 + ell**2*X**2)
    raux = X/s
    taux = X/(s+1)
    Q = 1 + raux
    rho = 2*mu**2*X*(1+taux)
    p = 2*mu**2*raux*taux
    w = sp.simplify(p/rho)
    ca2 = sp.simplify(raux/(s*(s+X)))
    w_exact = X/(s*(s+1+X))
    ca2_exact = X/(s**2*(s+X))
    assert sp.simplify(w-w_exact) == 0
    assert sp.simplify(ca2-ca2_exact) == 0

    w_bound = 1/(ell*(ell+1)*X)
    ca2_bound = 1/(ell**2*(ell+1)*X**2)

    lim_Xw = sp.simplify(sp.limit(X*w, X, sp.oo))
    lim_X2ca2 = sp.simplify(sp.limit(X**2*ca2, X, sp.oo))
    lim_rho_over_X = sp.simplify(sp.limit(rho/X, X, sp.oo))
    lim_p = sp.simplify(sp.limit(p, X, sp.oo))
    MK = mu*Q*s*sp.sqrt(s)
    lim_MK = sp.simplify(sp.limit(MK/X**sp.Rational(3,2), X, sp.oo))

    expected = {
        "Xw": 1/(ell*(ell+1)),
        "X2ca2": 1/(ell**2*(ell+1)),
        "rho_over_X": 2*mu**2*(ell+1)/ell,
        "p": 2*mu**2/ell**2,
        "MK_over_X_3_2": mu*(ell+1)*sp.sqrt(ell),
    }
    actual = {
        "Xw": lim_Xw,
        "X2ca2": lim_X2ca2,
        "rho_over_X": lim_rho_over_X,
        "p": lim_p,
        "MK_over_X_3_2": lim_MK,
    }
    residuals={k:sp.simplify(actual[k]-expected[k]) for k in expected}
    assert all(v == 0 for v in residuals.values())

    u = sp.symbols("u", nonnegative=True, finite=True)
    cs2_over_ca2 = 1/(1+u**2)
    assert sp.limit(cs2_over_ca2, u, 0, dir="+") == 1

    a, x0 = sp.symbols("a x0", positive=True, finite=True)
    w_bound_a = sp.simplify(w_bound.subs(X, x0/a**3))
    ca2_bound_a = sp.simplify(ca2_bound.subs(X, x0/a**3))
    assert sp.simplify(w_bound_a-a**3/(ell*(ell+1)*x0)) == 0
    assert sp.simplify(ca2_bound_a-a**6/(ell**2*(ell+1)*x0**2)) == 0

    result = {
        "schema":"RTK_C10_KHRONON_EARLY_DUST_BOUND_RESULT_v1",
        "classification":"C10_KHRONON_EARLY_DUST_FINITE_X_BOUND_PASS_SCOPED",
        "target":"research/theory_targets/RTK_C10_KHRONON_EARLY_DUST_BOUND_TARGET_v1.json",
        "definitions":{
            "ell":"sqrt(lambda_D)","X":"x0/a^3","s":"sqrt(1+ell^2 X^2)",
            "lambda_guard":"lambda_D is DBI, not completion lambda_HL"
        },
        "exact_simplifications":{
            "w":"X/[s(s+1+X)]","ca2":"X/[s^2(s+X)]",
            "machine_w_residual":"0","machine_ca2_residual":"0"
        },
        "finite_X_bounds":{
            "proof_step":"s>=ell X, so s(s+1+X)>=ell(ell+1)X^2 and s^2(s+X)>=ell^2(ell+1)X^3",
            "w":"0<=w<=1/[ell(ell+1)X]=a^3/[ell(ell+1)x0]",
            "ca2":"0<=ca2<=1/[ell^2(ell+1)X^2]=a^6/[ell^2(ell+1)x0^2]",
            "cs2":"0<=cs2=ca2/[1+(k/k_star)^2]<=ca2",
            "w_bound_a":str(w_bound_a),"ca2_bound_a":str(ca2_bound_a)
        },
        "asymptotic_coefficients":{
            "lim_X_w":str(lim_Xw),"lim_X2_ca2":str(lim_X2ca2),
            "lim_rho_over_X":str(lim_rho_over_X),"lim_p":str(lim_p),
            "lim_MK_over_X_3_2":str(lim_MK),
            "kstar":"~mu_K(ell+1)sqrt(ell) x0^(3/2) a^(-7/2)",
            "machine_residuals":{k:str(v) for k,v in residuals.items()}
        },
        "adiabatic_IC_consequence":{
            "production_relation":"delta_khr=(3/4)(1+w_khr) delta_gamma",
            "dust_relation":"delta_dust=(3/4)delta_gamma",
            "fractional_factor_deviation":"w_khr",
            "rigorous_bound":"<=a^3/[sqrt(lambda_D)(1+sqrt(lambda_D))x0]",
            "velocity_note":"production Newtonian transform gives theta->theta+k^2 alpha at leading growing-mode order"
        },
        "interpretation":{
            "core":"production neutral Khronon has a rigorously controlled early dust limit: rho~a^-3, w=O(a^3), ca2=O(a^6), cs2<=ca2 and k_star~a^-7/2",
            "use_in_C10":"organize Khronon as dust plus explicit bounded corrections, evaluated at the eventual finite EFT onset"
        },
        "next_gate":"derive the radiation+baryon+massless-ur O(k^2) adiabatic C2 coefficient and add the neutral-Khronon dust term plus finite-onset bounded corrections",
        "non_claims":[
            "no numerical a_EFT or parameter selection",
            "no claim finite-onset corrections are negligible before evaluation",
            "no photon/ur anisotropic O(k^2) coefficient yet",
            "no completed-U1 CLASS feedback or spectra",
            "no massive-neutrino extension"
        ]
    }
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
