#!/usr/bin/env python3
"""Flat-background TT tensor all-q stability domain for the corrected U(1)+RTK action.

On N=1, N^i=0, g_ij=delta_ij+h_ij^TT:
- K=0, so lambda drops out of the TT kinetic term;
- a_i=0, so beta0,beta2,beta4,beta8 lapse operators do not enter TT;
- homogeneous neutral RTK has D_i Theta=0, so explicit S_mix gives no TT
  spatial-derivative correction on this background;
- gamma1=-1 gives the GR-normalized q term;
- gamma3 R_ij R^ij and gamma5 C_ij C^ij give q^2 and q^3 terms.
Thus with y=q/zeta^2>=0,
  omega_T^2/q = 1 + gamma3 y + gamma5 y^2.
For gamma5>0 this is strictly positive for all y>=0 iff gamma3>-2 sqrt(gamma5).
"""
import json
import sympy as sp

y,g5=sp.symbols('y gamma5', positive=True, finite=True)
g3=sp.symbols('gamma3', real=True, finite=True)
f=sp.expand(1+g3*y+g5*y**2)
complete=sp.expand(g5*(y+g3/(2*g5))**2 + 1-g3**2/(4*g5))
assert sp.simplify(f-complete)==0
ystar=sp.simplify(-g3/(2*g5))
fstar=sp.simplify(f.subs(y,ystar))
assert sp.simplify(fstar-(1-g3**2/(4*g5)))==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_TT_ALLQ_STABILITY_PASS',
  'status_scope':'GREEN_FLAT_TT_ALL_Q_STABILITY_DOMAIN_GW_PHENOMENOLOGY_PENDING',
  'domain':'flat homogeneous background, transverse-traceless metric perturbations, gamma1=-1, gamma5>0, corrected beta0_bare=0 full-action bookkeeping',
  'dispersion':'omega_T^2=q[1+gamma3(q/zeta^2)+gamma5(q/zeta^2)^2]',
  'lambda_independence':'K=0 for TT, so the lambda K^2 term vanishes identically.',
  'lapse_uv_independence':'a_i=0 in the TT channel, so beta2+beta4 and beta8 do not enter the TT quadratic dispersion.',
  'rtk_mix_independence':'On the homogeneous rolling canonical background D_i Theta=0, so the explicit RTK S_mix supplies no TT spatial-gradient term.',
  'exact_positive_domain':'gamma5>0 and gamma3>-2 sqrt(gamma5) imply omega_T^2>0 for every q>0; this condition is also necessary for positivity of the quadratic polynomial on y>=0 when gamma5>0.',
  'ir_speed':'With gamma1=-1 normalization the q coefficient is unity, c_T^2=1 in the IR normalization of this action.',
  'interpretation':'The previously found flat/barotropic rank-safe lambda<1/3, beta24<=0, beta8<0 domain is not obstructed by the flat TT tensor sector; tensor stability can be imposed independently through gamma3,gamma5.',
  'non_claims':[
    'does not impose observational bounds on dispersive tensor corrections at LIGO/Virgo/KAGRA frequencies',
    'does not cover curved/time-dependent tensor backgrounds or nonlinear tensor interactions',
    'does not freeze gamma3, gamma5, lambda or the UV scale',
    'does not close the scalar/constraint rank problem on non-FLRW backgrounds'
  ],
  'next_gate':'combine the parent gamma5 sign relation with this condition and estimate the GW-frequency suppression scale allowed by current c_T/dispersion bounds only after the same-action UV normalization is frozen.'
}
open('u1_flat_tt_allq_stability_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
