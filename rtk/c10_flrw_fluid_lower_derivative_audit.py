#!/usr/bin/env python3
"""C10 expanding-FLRW lower-derivative audit: fixed action vs production GDM.

This is a symbolic/repository replay of an analytic derivation.  It proves the
scoped equation difference; it does not convert that difference into a
likelihood or observable error.
"""
import json
from pathlib import Path
import sympy as sp

root=Path(__file__).resolve().parents[1]
src=(root/'rtk/khronon_perturbations.c').read_text()
# Guard the exact current production choices under audit.
assert "-m->Hc*(1.0-3.0*bg->cs2)*y->theta" in src
assert "-9.0*m->Hc*m->Hc*onepw*entropy*y->theta/k2" in src
assert "entropy=bg->cs2-bg->ca2" in src

H,w,ca,cs,delta,theta,k2,phip,psi=sp.symbols(
    'H w ca2 cs2 delta theta k2 phi_prime psi', finite=True, real=True
)
onepw=1+w
# Fixed-action equations derived from the homogeneous shift-current action.
action_delta=sp.expand(-onepw*(theta-3*phip)-3*H*(ca-w)*delta)
action_theta=sp.expand(-H*(1-3*ca)*theta+k2*(cs*delta/onepw+psi))
# Current production implementation, exactly matching khronon_perturbations.c.
prod_delta=sp.expand(-onepw*(theta-3*phip)-3*H*(cs-w)*delta-9*H**2*onepw*(cs-ca)*theta/k2)
prod_theta=sp.expand(-H*(1-3*cs)*theta+k2*(cs*delta/onepw+psi))

res_delta=sp.factor(prod_delta-action_delta)
res_theta=sp.factor(prod_theta-action_theta)
expected_delta=-3*H*(cs-ca)*(delta+3*H*onepw*theta/k2)
expected_theta=3*H*(cs-ca)*theta
assert sp.simplify(res_delta-expected_delta)==0
assert sp.simplify(res_theta-expected_theta)==0
assert sp.simplify(res_delta.subs(cs,ca))==0
assert sp.simplify(res_theta.subs(cs,ca))==0

out={
  'classification':'C10_FLRW_FIXED_ACTION_VS_PRODUCTION_GDM_LOWER_DERIVATIVE_MISMATCH_IDENTIFIED_SCOPED',
  'status_scope':'YELLOW_EXACT_LOWER_DERIVATIVE_DIFFERENCE_PRINCIPAL_RATIONAL_KERNEL_STILL_MATCHES',
  'fixed_action_delta_equation':"delta'=-(1+w)(theta-3phi')-3H(c_a^2-w)delta",
  'fixed_action_theta_equation':"theta'=-H(1-3c_a^2)theta+k^2[c_s^2 delta/(1+w)+psi]",
  'production_delta_equation':"delta'=-(1+w)(theta-3phi')-3H(c_s^2-w)delta-9H^2(1+w)(c_s^2-c_a^2)theta/k^2",
  'production_theta_equation':"theta'=-H(1-3c_s^2)theta+k^2[c_s^2 delta/(1+w)+psi]",
  'production_minus_action_delta':'-3H(c_s^2-c_a^2)[delta+3H(1+w)theta/k^2]',
  'production_minus_action_theta':'3H(c_s^2-c_a^2)theta',
  'common_limit':'Both residuals vanish identically when c_s^2=c_a^2 (F=1).',
  'interpretation':'The fixed action and current production effective-fluid implementation agree on the rational principal pressure/dispersion relation but differ in expanding-FLRW lower-derivative entropy/friction terms. This is a same-action implementation gap, not by itself an observational failure. An additional U1-gravity/Ward contribution may in principle restore the GDM form, but must be derived explicitly.',
  'next_gate':'Quantify the coefficient size on the replay-certified RTK background and test whether the completed U1 metric/Ward system supplies the missing residual; if not, implement a shadow corrected-fluid solver and compare observables before changing the production likelihood path.',
  'non_claims':[
    'not a full CLASS rerun',
    'not an observable-error estimate',
    'not a proof that no additional U1 gravity/Ward term restores the GDM equations',
    'not nonlinear perturbation closure',
    'not a B4 massive-neutrino extension'
  ],
  'target':'research/theory_targets/RTK_C10_FLRW_FLUID_LOWER_DERIVATIVE_AUDIT_TARGET_v1.json'
}
Path('c10_flrw_fluid_lower_derivative_audit_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
