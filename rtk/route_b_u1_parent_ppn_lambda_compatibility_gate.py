#!/usr/bin/env python3
"""Parent-U(1) PPN compatibility of leaving lambda on the lambda>1 branch.

Literature scope: Lin, Mukohyama, Wang, Zhu, arXiv:1310.6666.
Their exact-GR PPN family-I relation at sigma1=sigma2=0 includes
  beta0(a1^2 kappa gamma1+1)+2 kappa(a1 gamma1+1)^2=0.
At a1=kappa=1, gamma1=-1 this is identically zero for any beta0 and contains
no lambda.  The paper's abstract/conclusion states that solar-system tests do
not constrain lambda in that parent U(1) theory.

Current corrected bare tuple uses beta0_bare=0, a1=kappa=1, gamma1=-1, so it
lies algebraically on this parent exact-GR branch for arbitrary lambda.
Critical non-claim: the published PPN calculation does NOT contain the separate
explicit rolling RTK S_mix term of our full action; therefore this gate is only
parent compatibility and not a same-action RTK PPN certification.
"""
import json
import sympy as sp

beta0,lam=sp.symbols('beta0 lambda', real=True, finite=True)
a1=kappa=sp.Integer(1)
gamma1=sp.Integer(-1)
rel=sp.expand(beta0*(a1**2*kappa*gamma1+1)+2*kappa*(a1*gamma1+1)**2)
assert sp.simplify(rel)==0
assert sp.diff(rel,lam)==0
assert sp.simplify(rel.subs(beta0,0))==0

out={
  'classification':'RTK_ROUTE_B_U1_PARENT_PPN_LAMBDA_COMPATIBILITY_PASS',
  'status_scope':'GREEN_PARENT_U1_PPN_LAMBDA_COMPATIBILITY_SAME_ACTION_S_MIX_PPN_PENDING',
  'literature_anchor':'Lin et al., arXiv:1310.6666, exact-GR PPN family and statement that solar-system tests impose no constraint on lambda in the parent U(1) theory',
  'parent_relation':'beta0(a1^2 kappa gamma1+1)+2 kappa(a1 gamma1+1)^2=0',
  'current_bare_substitution':'a1=kappa=1, gamma1=-1, beta0_bare=0 -> relation=0 identically for arbitrary lambda',
  'lambda_result':'The parent exact-GR PPN algebra does not exclude lambda>1 or force lambda=1.',
  'interpretation':'The newly found lambda>1 flat-FLRW rank-safe domain is not eliminated by the parent U(1) solar-system lambda statement.',
  'non_claims':[
    'does not certify PPN parameters of the full RTK action because explicit rolling S_mix is absent from the published parent PPN calculation',
    'does not freeze lambda or claim lambda>1 is observationally preferred',
    'does not identify the local Newton constant after including S_mix',
    'does not replace a fresh same-action static/Newton/PPN derivation'
  ],
  'next_gate':'derive the same-action static weak-field equations with explicit S_mix and corrected beta0_bare=0; separately compare the homogeneous lambda>1 kinetic normalization with cosmological bounds without assuming the parent local Newton normalization survives S_mix.'
}
open('u1_parent_ppn_lambda_compatibility_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
