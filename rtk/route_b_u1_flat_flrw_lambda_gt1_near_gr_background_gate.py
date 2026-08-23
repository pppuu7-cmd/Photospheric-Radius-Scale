#!/usr/bin/env python3
"""Near-GR homogeneous normalization of the positive-source lambda>1 branch.

For d=3 same-action flat FLRW at fixed total homogeneous source rho_eff,
  (3/2)(3 lambda-1) M_Pl^2 H^2=rho_eff.
Relative to lambda=1 with the same source and M_Pl,
  R_H = H^2(lambda)/H^2(1)=2/(3 lambda-1).
For lambda=1+eps, eps>0,
  1-R_H=3 eps/(2+3 eps).
Thus for any fractional tolerance 0<delta<1, choosing
  0<eps<2 delta/[3(1-delta)]
keeps |R_H-1|<delta while remaining strictly on lambda>1.
This is a continuity/nonempty-intersection theorem, not an observational fit.
"""
import json
import sympy as sp

eps,delta=sp.symbols('eps delta', positive=True, finite=True)
lam=1+eps
R=sp.factor(2/(3*lam-1))
dev=sp.factor(1-R)
assert sp.simplify(R-2/(2+3*eps))==0
assert sp.simplify(dev-3*eps/(2+3*eps))==0
bound=sp.factor(2*delta/(3*(1-delta)))
# Boundary value equals delta exactly.
assert sp.simplify(dev.subs(eps,bound)-delta)==0

out={
  'classification':'RTK_ROUTE_B_U1_FLAT_FLRW_LAMBDA_GT1_NEAR_GR_BACKGROUND_PASS',
  'status_scope':'GREEN_CONTINUOUS_NEAR_GR_POSITIVE_SOURCE_BRANCH_FULL_SAME_ACTION_INFERENCE_PENDING',
  'domain':'d=3 flat homogeneous same-action lapse constraint at fixed positive rho_eff and fixed M_Pl; lambda=1+epsilon with epsilon>0',
  'ratio':'H^2(lambda)/H^2(lambda=1)=2/(3 lambda-1)=2/(2+3 epsilon)',
  'fractional_deviation':'1-H^2(lambda)/H^2(1)=3 epsilon/(2+3 epsilon)',
  'tolerance_condition':'For any 0<delta<1, 0<epsilon<2 delta/[3(1-delta)] implies fractional homogeneous-normalization deviation < delta.',
  'interpretation':'The exact lambda>1 rank-safe branch can approach the GR homogeneous normalization arbitrarily closely from above; positive-source compatibility does not force an order-one cosmological background change.',
  'pipeline_warning':'The current B9 phenomenological parameter lam/lambda_D is not lambda_HL. A final same-action CLASS implementation must expose lambda_HL separately and apply this homogeneous normalization rather than identifying it with the existing RTK lambda_D parameter.',
  'non_claims':[
    'does not identify the locally measured Newton constant after explicit S_mix is included',
    'does not turn a chosen observational tolerance into a fitted lambda_HL value',
    'does not prove perturbation-level cosmological equivalence to GR',
    'does not close same-action PPN, BBN or CMB constraints on lambda_HL'
  ],
  'next_gate':'add lambda_HL as a distinct same-action background/perturbation parameter after the classical action slice is frozen; compare cosmological and local gravitational normalizations without conflating lambda_HL with lambda_D.'
}
open('u1_flat_flrw_lambda_gt1_near_gr_background_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
