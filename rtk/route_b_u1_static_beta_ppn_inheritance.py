#!/usr/bin/env python3
"""Static O(v^4) beta_PPN inheritance gate for the frozen U(1)+RTK action.

The gate is conditional on the exact nonlinear static bare-lapse uniqueness
result.  It deliberately does not touch the moving-source/vector sector.
"""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_ROUTE_B_U1_STATIC_BETA_PPN_INHERITANCE_TARGET_v1.json'
t=json.load(open(TARGET))
assert t['classification']=='RTK_ROUTE_B_U1_STATIC_BETA_PPN_INHERITANCE_TARGET_V1_FROZEN'

u=json.load(open(t['prerequisite']['result']))
assert u['classification']==t['prerequisite']['required_classification']
assert u['static_scalar_consequence']['N']=='1'
assert u['static_scalar_consequence']['a_i']=='0'
assert u['static_scalar_consequence']['P']=='0'
assert u['static_scalar_consequence']['P_N']=='0'

v=json.load(open('research/theory_results/RTK_ROUTE_B_U1_STATIC_VARIATION_BRIDGE_RESULT_v1.json'))
assert v['classification']=='RTK_ROUTE_B_U1_STATIC_VARIATION_BRIDGE_EXACT_PASS'

# arXiv:1310.6666v4 Eq.(5.42), sigma1=sigma2=0 branch.
a1,kappa,gamma1,a2,beta0=sp.symbols('a1 kappa gamma1 a2 beta0', finite=True, real=True)
beta_expr=(-a1**3*gamma1*kappa**2 + 3*a1**2*gamma1*kappa + 2*a1*gamma1 + a1*kappa + 3)/(4*a1*gamma1+4)
gamma_expr=(kappa*(a1**2*gamma1+a2*a1*gamma1+a1)-a2*gamma1)/(a1*gamma1+1)

# Family-I substitution a1=kappa=1, a2=0 must be performed before the
# canonical gamma1=-1 limit; the apparent 0/0 cancels identically.
beta_family=sp.cancel(beta_expr.subs({a1:1,kappa:1}))
gamma_family=sp.cancel(gamma_expr.subs({a1:1,kappa:1,a2:0}))
assert sp.simplify(beta_family-1)==0
assert sp.simplify(gamma_family-1)==0
assert sp.limit(beta_family,gamma1,-1)==1
assert sp.limit(gamma_family,gamma1,-1)==1

# Eq.(5.43): beta0[a1^2 kappa gamma1+1]+2 kappa(a1 gamma1+1)^2=0.
eq543=beta0*(a1**2*kappa*gamma1+1)+2*kappa*(a1*gamma1+1)**2
assert sp.simplify(eq543.subs({a1:1,kappa:1,gamma1:-1}))==0
# Hence both beta0_bare=0 and the exact static S_mix representative beta0_eff=2
# satisfy the same family-I compatibility condition.
assert sp.simplify(eq543.subs({a1:1,kappa:1,gamma1:-1,beta0:0}))==0
assert sp.simplify(eq543.subs({a1:1,kappa:1,gamma1:-1,beta0:2}))==0

out={
 'classification':'RTK_ROUTE_B_U1_STATIC_BETA_PPN_EXACT_PASS',
 'status':'STATIC_O4_BETA_GREEN_ON_CERTIFIED_ZERO_SHIFT_BRANCH',
 'target':TARGET,
 'prerequisite':t['prerequisite']['result'],
 'same_action_reduction':{
   'bare_lapse':'N=1 exactly on the certified static branch',
   'RTK_DBI':'P=P_N=0 on that branch',
   'RTK_mixed':'a_i=0 on the solution; its exact static variation is the beta0_eff=2 acceleration structure used in the uniqueness equation',
   'remaining_equations':'corresponding nonprojectable U1 family-I static equations with the same universal matter frame',
 },
 'literature_algebra':{
   'source':'Lin-Mukohyama-Wang-Zhu arXiv:1310.6666v4 Eqs.(5.42),(5.43),(5.50),(5.51), Appendix E',
   'beta_family_I_after_a1_kappa_1':'1',
   'gamma_family_I_after_a1_kappa_1_a2_0':'1',
   'gamma1_minus1_limit':'regular after algebraic cancellation',
   'Eq543_beta0_bare_0':'0=0',
   'Eq543_static_beta0_eff_2':'0=0',
 },
 'static_beta_PPN':1,
 'static_gamma_PPN':1,
 'interpretation':'The fixed RTK scalar does not alter the O(v^4) static Eddington beta coefficient on the certified regular asymptotically-flat zero-invariant-shift branch; beta=1 and gamma=1 there.',
 'non_claims':t['non_claims'],
 'next_gate':'derive O(v^3) moving-source/vector equations with explicit S_mix and fixed P(X_U) before alpha1/alpha2 claims',
}
open('u1_static_beta_ppn_inheritance_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
