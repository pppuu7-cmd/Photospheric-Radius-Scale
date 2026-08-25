#!/usr/bin/env python3
"""C10.48 deterministic symbolic audit of legacy model=2 against published RT equations.

This script does not fit coefficients and does not modify production code.  It verifies
that the single perturbative covector dictionary

    dV_pub(code-normalized) = dV_code + Psi * Vbar_code

maps the published A.11, A.12 and A.7 structures to the pinned fork, using only the
published background V equation for the A.11 reduction.  It also derives the corrected
A.6/00 auxiliary bracket used by the separately frozen C10.49 replay.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

zeta,K2,h=sp.symbols('zeta K2 h', nonzero=True)
Psi,Psip,Psipp,Phip=sp.symbols('Psi Psip Psipp Phip')
V,Vp,Vpp,Up=sp.symbols('V Vp Vpp Up')
Vc,Vcp,Vcpp=sp.symbols('Vc Vcp Vcpp')

# A.11 after dV_pub = dV_code + Psi*Vbar.  The published background identity is
# Vbar''+(3+zeta)Vbar'-3Vbar=h^-1 Ubar'.
rhs_a11_after = (
    Psi*Vpp + ((3+zeta)*Psi + Psip - 3*Phip)*Vp
    + (6*Phip + (K2/sp.Integer(2)-3)*Psi)*V
)
rhs_a11_code = (
    (Psip-3*Phip)*Vp + (6*Phip+K2*Psi/sp.Integer(2))*V + Psi*Up/h
)
bg_V = Up/h-(3+zeta)*Vp+3*V
assert sp.simplify(rhs_a11_after.subs(Vpp,bg_V)-rhs_a11_code)==0

# A.12 bracket after the same field dictionary.
Phixp=sp.symbols('Phixp')
br_a12_pub=(
    Vcp + Psip*V + Psi*Vp + 5*(Vc+Psi*V)
    -4*Psi*Vp -2*(Psip-Phixp+4*Psi)*V
)
br_a12_code=Vc+5*Vc*0  # placeholder reset below to make the explicit expression obvious
br_a12_code=Vcp+5*Vc-3*Psi*Vp-(Psip-2*Phixp+3*Psi)*V
assert sp.simplify(br_a12_pub-br_a12_code)==0

# A.7 vector-source combination: Psi Vbar - dV_pub/2 -> Psi Vbar/2 - dV_code/2.
assert sp.simplify(Psi*V-sp.Rational(1,2)*(Vc+Psi*V)
                   -(sp.Rational(1,2)*Psi*V-sp.Rational(1,2)*Vc))==0

# Corrected A.6 bracket in conformal/code variables.  Factor 1/a^2 is external.
Hc,dV,dVp,Vbg,Vbgp,psi,psip=sp.symbols('Hc dV dVp Vbg Vbgp psi psip')
Q=dV+psi*Vbg
Qp=dVp+psip*Vbg+psi*Vbgp
corr_no_dU=sp.expand(-Qp+Hc*Q+2*psi*(Vbgp-Hc*Vbg)+psip*Vbg)
expected=-dVp+Hc*dV+psi*Vbgp-Hc*psi*Vbg
assert sp.simplify(corr_no_dU-expected)==0

out={
  'schema':'RTK_C10_LEGACY_MODEL2_PUBLISHED_EQUATION_SYMBOLIC_AUDIT_v1',
  'all_assertions_pass':True,
  'field_dictionary':'deltaV_pub_code_normalized = deltaV_code + Psi * Vbar_code',
  'a11_equivalent_after_published_background_V_identity':True,
  'a12_equivalent_directly':True,
  'a7_0i_equivalent_directly':True,
  'corrected_A6_B00_code':'deltaU + (-deltaVprime + Hc*deltaV + Psi*Vbarprime - Hc*Psi*Vbar)/a^2',
  'coefficients_fitted':False,
  'production_modified':False
}
Path('c10_48_symbolic_audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
