#!/usr/bin/env python3
"""Preferred-frame alpha1/alpha2 inheritance gate for the fixed U(1)+RTK action."""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_ROUTE_B_U1_PREFERRED_FRAME_INHERITANCE_TARGET_v1.json'
t=json.load(open(TARGET))
assert t['classification']=='RTK_ROUTE_B_U1_PREFERRED_FRAME_INHERITANCE_TARGET_V1_FROZEN'

p=t['prerequisite']
r=json.load(open(p['result']))
assert r['classification']==p['required_classification']

a1,a2,kappa,gamma1,lam=sp.symbols('a1 a2 kappa gamma1 lam', finite=True, real=True)
# arXiv:1310.6666v4 Eq.(5.42), sigma1=sigma2=0.
alpha1 = 4*((a2-a1)*gamma1-1)/(a1*gamma1+1) - 4*kappa*(a2*(1-1/(a1*gamma1+1))+a1-2)
alpha2 = (kappa*(a1**2*(3*lam-1)+a1*(2-6*lam)+4*lam-2)-lam+1)/(lam-1)

# Apply the family-I matter-frame values before the apparent singular limits.
a1_family=sp.cancel(alpha1.subs({a1:1,a2:0,kappa:1}))
a2_num=sp.factor(sp.together(alpha2).as_numer_denom()[0].subs({a1:1,kappa:1}))
assert sp.simplify(a1_family)==0
assert sp.simplify(a2_num)==0

# For alpha2, the rational expression is exactly zero for lam != 1 and has
# continuous extension zero at lam=1 after cancellation of the identically-zero numerator.
alpha2_family_nonunit=sp.simplify(alpha2.subs({a1:1,kappa:1}))
assert sp.simplify(alpha2_family_nonunit)==0

out={
  'classification':'RTK_ROUTE_B_U1_PREFERRED_FRAME_ALPHA1_ALPHA2_EXACT_PASS',
  'status':'WEAK_FIELD_PPN_PREFERRED_FRAME_GREEN_ON_CERTIFIED_STANDARD_BRANCH',
  'target':TARGET,
  'prerequisite':p['result'],
  'external_source':'Lin-Mukohyama-Wang-Zhu arXiv:1310.6666v4 Eq.(5.42), with Eq.(5.51) as consistency check',
  'regular_cancellations':{
    'alpha1':'At a1=kappa=1,a2=0 the two terms cancel exactly before gamma1=-1: -4 + 4 = 0.',
    'alpha2':'At a1=kappa=1 the Eq.(5.42) numerator is the zero polynomial in lambda_HL; the continuous lambda_HL=1 value is therefore 0.'
  },
  'alpha1_PPN':0,
  'alpha2_PPN':0,
  'combined_weak_field_static_and_vector_result':{
    'gamma_PPN':1,
    'beta_PPN':1,
    'alpha1_PPN':0,
    'alpha2_PPN':0
  },
  'interpretation':'Because the separately certified O3 RTK scalar-silence theorem shows no extra vector/shift source on the standard PPN branch, the pure-U1 family-I preferred-frame cancellations apply to the identical fixed action through O(v^3).',
  'non_claims':t['non_claims'],
  'next_gate':'retain radiative protection, strong coupling/EFT cutoff, higher-spatial UV/tensor dispersion and compact-object/nonlinear X_U->0 behavior as independent open gates'
}
open('u1_preferred_frame_inheritance_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
