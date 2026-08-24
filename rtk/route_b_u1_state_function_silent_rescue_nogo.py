#!/usr/bin/env python3
"""Scoped continuity no-go for an exactly cosmology-silent single higher-spatial rescue."""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_C8_U1_STATE_FUNCTION_SILENT_RESCUE_NOGO_TARGET_v1.json'
t=json.load(open(TARGET))
assert t['classification']=='RTK_C8_U1_STATE_FUNCTION_SILENT_RESCUE_NOGO_TARGET_V1'

# Production branch map. For lambda>0, r=x/sqrt(1+lambda x^2), x>0.
x,lam,Xs=sp.symbols('x lam Xs', positive=True, finite=True, real=True)
r=x/sp.sqrt(1+lam*x**2)
u=1+r
Xbar=sp.simplify(Xs*u**2)
assert sp.simplify(Xbar-Xs)>0
assert sp.limit(r,x,0,dir='+')==0
assert sp.limit(Xbar,x,0,dir='+')==Xs
# Monotonicity in x: the branch is a continuous interval with Xs as lower accumulation point.
drdx=sp.simplify(sp.diff(r,x))
assert sp.simplify(drdx-(1+lam*x**2)**sp.Rational(-3,2))==0
assert drdx.is_positive

# Logical theorem encoded explicitly: if continuous eta vanishes at every point of
# (Xs, Xmax) approached by the branch, its right-hand limit and hence eta(Xs) vanish.
# SymPy cannot quantify arbitrary continuous functions, so this is recorded as a
# topology/continuity implication after executable verification of the branch map.

out={
 'classification':'RTK_C8_U1_CONTINUOUS_STATE_FUNCTION_EXACT_SILENT_SINGLE_OPERATOR_RESCUE_NOGO_PASS',
 'status':'SCOPED_EXACT_NOGO_FOR_CONTINUOUS_SINGLE_STATE_FUNCTION_RESCUE_WITH_UNCHANGED_COSMOLOGICAL_KERNEL',
 'target':TARGET,
 'production_branch':{
   'r':'x/sqrt(1+lambda_D x^2)',
   'u':'1+r',
   'Xbar':'X_star(1+r)^2',
   'dr_dx':'(1+lambda_D x^2)^(-3/2)>0',
   'limit_x_to_0_plus':'Xbar -> X_star from above',
   'topology':'continuous interval of Xbar>X_star with X_star as an accumulation point'
 },
 'no_go_chain':[
   'For the isolated operator eta(X_U)(D^2 Sigma)^2, its quadratic rolling-branch k^4 contribution is proportional to eta(Xbar) times a nonzero background factor.',
   'Exact preservation of the frozen RTK cosmological quadratic kernel on every rolling production state requires eta(Xbar)=0 throughout that continuous interval.',
   'If eta is continuous at X_star, eta(X_star)=lim_{Xbar->X_star+} eta(Xbar)=0.',
   'Thus the same isolated continuous state-function coefficient cannot be exactly silent on the full rolling branch and nonzero at local rest.'
 ],
 'interpretation':'An exactly cosmology-silent local-rest rescue cannot be obtained merely by replacing the constant eta4 of the minimal (D^2 Sigma)^2 operator with a continuous function of X_U. A viable exact-silent construction must use structural operator cancellations/null projections, nonanalytic behavior requiring separate justification, or accept a modified cosmological kernel and refit it.',
 'non_claims':t['non_claims'],
 'next_gate':t['next_gate']
}
open('u1_state_function_silent_rescue_nogo_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
