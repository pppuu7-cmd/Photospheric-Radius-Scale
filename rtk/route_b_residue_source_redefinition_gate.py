#!/usr/bin/env python3
"""Exact Route-B C8 gate for residue repair by scalar field redefinition.

Starting point (already proved by route_b_pole_residue_distinction.py):

    K_RTK = F(q) K_BPS,          F(q)=1+r q^2, r>0.

The two kernels have the same dispersion pole but different fixed-source
residues.  This module asks the narrow next question: can a scalar-only linear
field redefinition repair the off-shell kernel while keeping a standard fixed
local source normalization?

For a quadratic/source action

    L_BPS = 1/2 K_BPS phi_B^2 + J_B phi_B,

a multiplicative Fourier-space redefinition phi_B=T(q) phi_R gives

    K_new = T(q)^2 K_BPS,
    J_new = T(q) J_B.

Exact kernel matching therefore forces T^2=F.  On the positive branch,
T=sqrt(1+r q^2), so a q-independent source J_B becomes a momentum-dependent
source coupling.  Moreover sqrt(1+r q^2) is not a finite polynomial in q^2
for r>0; its exact scalar-only realization is pseudodifferential/nonlocal (or
requires an enlarged local field/constraint system whose elimination generates
the same factor).

Scope: scalar-only multiplicative field redefinitions with a fixed source.
This is NOT a no-go for local multi-field/constraint completions, disformal
matter maps, auxiliary fields, or an explicit lapse/shift Schur-complement
construction that generates the required source factor dynamically.
"""

import json
import sympy as sp

q, r, A, G, y, J = sp.symbols(
    "q r A G y J", positive=True, finite=True, real=True
)
F = 1 + r*q**2
K_bps = A*y - G*q**2/F
K_rtk = sp.expand(A*F*y - G*q**2)

assert sp.simplify(K_rtk - F*K_bps) == 0

# General scalar-only multiplicative field map phi_B=T phi_R.
T = sp.sqrt(F)
K_new = sp.simplify(T**2 * K_bps)
J_new = sp.simplify(T * J)
assert sp.simplify(K_new - K_rtk) == 0
assert sp.simplify(J_new/J - sp.sqrt(F)) == 0

# Fixed source normalization cannot survive unless F=1.  For r>0 and generic
# nonzero q, F>1, so T is not a constant.
dT_dq = sp.simplify(sp.diff(T, q))
assert sp.simplify(dT_dq - r*q/sp.sqrt(F)) == 0

# Prove there is no finite polynomial P(x), x=q^2, with P(x)^2=1+r x for r>0.
# Degree argument: if deg P=n>=1 then deg P^2=2n, which cannot equal degree 1;
# if n=0 then P^2 is constant and cannot reproduce the r*x term.  We encode
# the first few generic coefficient identities as an executable guard and state
# the all-degree proof explicitly in the output.
x = sp.symbols("x", real=True)
a0, a1, a2 = sp.symbols("a0 a1 a2", real=True)
P2 = sp.Poly(sp.expand((a0+a1*x+a2*x**2)**2 - (1+r*x)), x)
# A quadratic candidate would require the x^4 coefficient a2^2=0 -> a2=0,
# then x^2 coefficient a1^2=0 -> a1=0, contradicting the x coefficient -r.
coeff = {k: sp.expand(P2.coeff_monomial(x**k)) for k in range(5)}
assert coeff[4] == a2**2
assert sp.simplify(coeff[2].subs(a2, 0) - a1**2) == 0
assert sp.simplify(coeff[1].subs({a2: 0, a1: 0}) + r) == 0

# Residues after the field redefinition agree, but only together with the
# transformed source.  Fixed-source two-point responses therefore remain
# inequivalent if one refuses the momentum-dependent source map.
res_bps = sp.simplify(1/sp.diff(K_bps, y))
res_rtk = sp.simplify(1/sp.diff(K_rtk, y))
assert sp.simplify(res_bps/res_rtk - F) == 0

out = {
    "classification": "RTK_ROUTE_B_RESIDUE_SOURCE_REDEFINITION_GATE_PASS",
    "starting_relation": "K_RTK=(1+r q^2) K_BPS",
    "forced_scalar_redefinition": "phi_BPS=sqrt(1+r q^2) phi_RTK (positive branch)",
    "transformed_source": "J_RTK=sqrt(1+r q^2) J_BPS",
    "fixed_source_obstruction": (
        "For r>0 the required T(q) is momentum dependent, so exact kernel/residue "
        "repair by this scalar-only redefinition does not preserve a q-independent fixed source coupling."
    ),
    "finite_derivative_locality_gate": (
        "sqrt(1+r q^2) is not a finite polynomial in q^2 for r>0. Degree proof: "
        "P polynomial with deg n>=1 gives deg(P^2)=2n != 1; deg n=0 cannot match the r q^2 term."
    ),
    "interpretation": (
        "The exact BPS pole embedding cannot be promoted to an exact fixed-source RTK "
        "off-shell mapping by a scalar-only finite-derivative local normalization."
    ),
    "allowed_escape_routes": [
        "lapse/shift constraint mixing whose Schur complement generates the required factor",
        "additional auxiliary/local fields whose elimination realizes the pseudodifferential factor",
        "a derived momentum-dependent/disformal matter-source map consistent with equivalence-principle and PPN bounds",
        "a different local carrier whose off-shell kernel already has the RTK residue"
    ],
    "non_claims": [
        "not a no-go for local multi-field or constrained completions",
        "not a proof that a consistent matter/source map cannot exist",
        "not a nonlinear or radiative-stability theorem",
        "does not invalidate the exact BPS dispersion/pole embedding"
    ],
    "next_step": (
        "Derive the source vector J=(P,R) together with the lapse/shift matrix M from one explicit fixed FLRW action, "
        "then test whether its Schur complement produces both the RTK denominator and the required residue/source factor "
        "without inserting sqrt(1+r q^2) by hand."
    )
}

print("RTK_ROUTE_B_RESIDUE_SOURCE_REDEFINITION_GATE_PASS", json.dumps(out, sort_keys=True))
