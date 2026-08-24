#!/usr/bin/env python3
"""C10 exact closure of the reduced trace compatibility by total momentum conservation.

Primary source conventions: Zhu-Shu-Wu-Wang arXiv:1110.5106v2,
flat FLRW Eqs. (6.7),(6.10),(6.11) and scalar perturbation Eq. (7.18).
"""
import json
from pathlib import Path
import sympy as sp

D,H,Hp,a,G=sp.symbols('D H Hprime a G', nonzero=True, finite=True, real=True)
rho,p,phi,dp,Pi,L=sp.symbols('rho p phi delta_p Pi L', finite=True, real=True)
q,qp=sp.symbols('q qprime', finite=True, real=True)
Lam=sp.symbols('Lambda', finite=True, real=True)

# Flat-k background equations in the primary-source normalization:
# D/2 * H^2/a^2 = 8*pi*G*rho/3 + Lambda/3
# -D/2 * (2 H' + H^2) + a^2 Lambda = 8*pi*G*a^2*p
fried=sp.Eq(D*H**2/2, 8*sp.pi*G*a**2*rho/3 + Lam*a**2/3)
dyn=sp.Eq(-D*(2*Hp+H**2)/2 + Lam*a**2, 8*sp.pi*G*a**2*p)
# Solve the two equations for D*H^2 and D*H', then derive acceleration identity.
DH2=sp.solve(fried, D*H**2)[0]
# dyn is linear in Hp; replace D*H^2 first to avoid treating D and H independently.
dyn_expr=sp.expand((-D*Hp-D*H**2/2+Lam*a**2-8*sp.pi*G*a**2*p).subs(D*H**2,DH2))
DHp=sp.solve(sp.Eq(dyn_expr,0), D*Hp)[0]
accel=sp.simplify(DHp-DH2)
assert sp.simplify(accel + 8*sp.pi*G*a**2*(rho+p))==0

# C10 reduced trace compatibility.  Keep the acceleration combination grouped
# until the background identity is inserted.  A prior executable revision
# expanded this expression first and then tried to substitute the grouped
# D*(Hprime-H^2) pattern; SymPy correctly could not match that already-expanded
# tree.  The frozen physics target/formulas are unchanged by this implementation fix.
Mq=8*sp.pi*G*a*q
Mqp=8*sp.pi*G*a*(qp+H*q)  # derivative of a*q in conformal time
compat_grouped=D*(Hp-H**2)*phi + Mqp + 2*H*Mq - 8*sp.pi*G*a**2*dp - sp.Rational(16,3)*sp.pi*G*a**2*L*Pi
compat_accel=sp.expand(compat_grouped.subs(D*(Hp-H**2),accel))
target=8*sp.pi*G*a*(qp+3*H*q-a*((rho+p)*phi+dp+sp.Rational(2,3)*L*Pi))
assert sp.simplify(compat_accel-target)==0

# Independent derivation from primary Eq.(7.18).
# Let V=v+B and q=-a(rho+p)V.  Background conservation gives
# rho'=-3H(rho+p), p'=ca2*rho', hence (rho+p)'=-3H(1+ca2)(rho+p).
ca2,V,Vp=sp.symbols('ca2 V Vprime', finite=True, real=True)
rhop=-3*H*(rho+p)
pp=ca2*rhop
rhoplusp=sp.expand(rhop+pp)
# Differentiate q=-a(rho+p)V.
q_from_V=-a*(rho+p)*V
qprime_from_V=sp.expand(-a*H*(rho+p)*V-a*rhoplusp*V-a*(rho+p)*Vp)
# Eq.(7.18) with J_A_hat=J_varphi_hat=0:
# V' + H(1-3ca2)V + phi + [dp+(2/3)L Pi]/(rho+p)=0.
Vp_eom=-H*(1-3*ca2)*V-phi-(dp+sp.Rational(2,3)*L*Pi)/(rho+p)
qcons_from_V=sp.simplify((qprime_from_V+3*H*q_from_V).subs(Vp,Vp_eom)-a*((rho+p)*phi+dp+sp.Rational(2,3)*L*Pi))
assert qcons_from_V==0

out={
  'classification':'C10_U1_TRACE_COMPATIBILITY_IS_TOTAL_MOMENTUM_CONSERVATION_PASS_SCOPED',
  'status_scope':'GREEN_EXACT_LINEAR_TRACE_CLOSURE_BY_TOTAL_MOMENTUM_CONSERVATION',
  'background_acceleration_identity':'(3lambda-1)(Hprime-H^2)=-8 pi G a^2 (rho_total+p_total)',
  'reduced_trace_compatibility':'D(Hprime-H^2)phi+Mqprime+2H Mq=8 pi G a^2 delta_p_total+(16 pi G a^2/3)L Pi_total',
  'momentum_conservation_q_form':'q_total_prime+3H q_total=a[(rho_total+p_total)phi+delta_p_total+(2/3)L Pi_total]',
  'primary_eq_7p18_check':'PASS after q=-a(rho+p)(v+B), rho_prime+3H(rho+p)=0 and c_a^2=p_prime/rho_prime, with J_A_hat=J_varphi_hat=0',
  'symbolic_residual_reduced_to_conservation':'0',
  'symbolic_residual_primary_7p18_to_q_form':'0',
  'interpretation':'The final relation left after A/momentum/Hamiltonian/traceless elimination is not an independent propagating scalar-gravity equation in this scoped flat-FLRW k>0 system; it is exactly total momentum conservation once the background equations hold.',
  'non_claims':[
    'not a numerical CLASS auxiliary-source implementation',
    'not a B4 massive-neutrino anisotropic-stress implementation',
    'not nonlinear conservation closure',
    'not an exact k=0 perturbation theorem',
    'not a likelihood result'
  ],
  'target':'research/theory_targets/RTK_C10_U1_TRACE_MOMENTUM_CONSERVATION_CLOSURE_TARGET_v1.json'
}
Path('u1_trace_momentum_conservation_closure_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
