#!/usr/bin/env python3
"""Combine the lambda>1 cosmological-Newton and anisotropic-rank margins.

Inputs:
1. homogeneous background normalization on the lambda>1 branch:
   G_cos/G_N=2/(3lambda-1). Requiring 1-G_cos/G_N<=eps_G gives
   lambda<=1+2 eps_G/[3(1-eps_G)].
2. conservative pure-traceless response margin
   ||Delta X_TF||<=r A requires
   r < [sqrt(2)-2/sqrt(3lambda-1)]/sqrt(3).

Eliminating lambda gives the exact maximum fractional traceless response that
can be certified while respecting the chosen background-normalization tolerance.
"""
import json
import sympy as sp

e=sp.symbols('eps_G', positive=True, finite=True)
lammax=sp.factor(1+2*e/(3*(1-e)))
rmax=sp.factor((sp.sqrt(2)-2/sp.sqrt(3*lammax-1))/sp.sqrt(3))
rclosed=sp.sqrt(sp.Rational(2,3))*(1-sp.sqrt(1-e))
# Exact principal-root proof without relying on SymPy to infer 0<e<1 from
# positivity alone. Set t=sqrt(1-e)>0, so e=1-t^2 and all radicals have a
# manifest positive branch.
t=sp.symbols('t', positive=True, finite=True)
assert sp.simplify((3*lammax-1)-2/(1-e))==0
rmax_t=sp.simplify(rmax.subs(e,1-t**2))
rclosed_t=sp.simplify(rclosed.subs(e,1-t**2))
assert sp.simplify(rmax_t-rclosed_t)==0
# Small-e slope.
slope=sp.simplify(sp.diff(rclosed,e).subs(e,0))
assert slope==1/sp.sqrt(6)
# Exact examples.
r1=sp.N(rclosed.subs(e,sp.Rational(1,100)),15)
r10=sp.N(rclosed.subs(e,sp.Rational(1,10)),15)

out={
  'classification':'RTK_U1_LAMBDA_GT1_COSMOLOGY_ANISOTROPY_WINDOW_PASS',
  'status_scope':'GREEN_EXACT_COMPATIBILITY_WINDOW_PHYSICAL_ANISOTROPY_RESPONSE_PENDING',
  'background_tolerance':'0<eps_G<1 and 1-G_cos/G_N<=eps_G on lambda>1',
  'lambda_upper':'lambda <= 1 + 2 eps_G/[3(1-eps_G)]',
  'anisotropy_definition':'||Delta X_TF||<=r A with tr Delta X=0 in the conservative response-margin theorem',
  'joint_window_exists_if':'r < sqrt(2/3) [1-sqrt(1-eps_G)]',
  'small_eps':'r_max=eps_G/sqrt(6)+O(eps_G^2)',
  'examples':{
    'eps_G_1_percent_rmax':str(r1),
    'eps_G_10_percent_rmax':str(r10)
  },
  'interpretation':'Near-GR homogeneous normalization and conservative anisotropic rank robustness compete through lambda. A physical Bianchi/anisotropic-stress calculation can now be judged against an exact target rather than an unspecified smallness requirement.',
  'branch_scope':'The response-margin algebra applies to the lambda>1 DeWitt channel used in both the nonprojectable flat-FLRW block and the surviving projectable (J,phi) pair, provided the same response assumptions hold.',
  'non_claims':[
    'does not identify eps_G with a current observational bound',
    'does not identify r with shear/H or a directly measured cosmological anisotropy',
    'does not derive Delta X from Bianchi I or free-streaming anisotropic stress',
    'does not choose lambda'
  ],
  'next_gate':'derive r in terms of Bianchi-I shear and/or an anisotropic-stress tensor from the same action, then combine with observationally defined eps_G and shear bounds.'
}
open('u1_lambda_gt1_cosmology_anisotropy_window_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
