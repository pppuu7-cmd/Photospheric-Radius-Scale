#!/usr/bin/env python3
"""First nonvanishing constrained local-rest scalar action at quartic order."""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUARTIC_TARGET_v1.json'
PRE='research/theory_results/RTK_C8_U1_LOCAL_REST_FULL_SCALAR_CONSTRAINT_RESULT_v1.json'
t=json.load(open(TARGET)); pre=json.load(open(PRE))
assert t['classification']=='RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUARTIC_TARGET_V1_FROZEN'
assert pre['classification']=='RTK_C8_U1_LOCAL_REST_FULL_SCALAR_QUADRATIC_RANK_ENHANCEMENT_EXACT_PASS'

# Perturbative bookkeeping. y=Y-1 starts at O(eps^2), J=|grad phi|^2/2 starts O(eps^2).
eps,y2,J2,mu,f1=sp.symbols('eps y2 J2 mu f1', finite=True, real=True)
mu=sp.symbols('mu', positive=True, finite=True, real=True)
y=eps**2*y2
J=eps**2*J2
F=1+eps*f1
Y=1+y
# D=Y^2-2J because |grad phi|^2=2J.
D=sp.expand(Y**2-2*J)
sqrtD=sp.series(sp.sqrt(D),eps,0,5).removeO().expand()
s=sp.expand(sqrtD-1)
# The DBI leading term about s=0 is mu^2 s^2; lambda enters only beyond the quartic amplitude order.
p_lead=sp.expand(mu**2*s**2)
# One Fourier component of y with composite momentum K represents |grad y|^2=K^2 y^2.
K=sp.symbols('K', nonnegative=True, finite=True, real=True)
mixed_lead=K**2*y**2
pref=sp.series(F/Y,eps,0,5).removeO().expand()
L=sp.series(pref*(p_lead+mixed_lead),eps,0,6).removeO().expand()
L4=sp.simplify(L.coeff(eps,4))
expected=K**2*y2**2+mu**2*(y2-J2)**2
assert sp.simplify(L4-expected)==0
# f1~dot phi or shift-advection does not enter the quartic action.
assert sp.diff(L4,f1)==0

# Eliminate the quartic lapse/clock auxiliary y2.
eqy=sp.factor(sp.diff(L4,y2))
ysol=sp.solve(sp.Eq(eqy,0),y2)
assert len(ysol)==1
ys=sp.simplify(ysol[0])
assert sp.simplify(ys-mu**2*J2/(K**2+mu**2))==0
Leff=sp.factor(sp.simplify(L4.subs(y2,ys)))
expected_eff=sp.factor(mu**2*K**2/(K**2+mu**2)*J2**2)
assert sp.simplify(Leff-expected_eff)==0
assert sp.limit(expected_eff/K**2,K,0,dir='+')==J2**2
assert sp.limit(expected_eff,K,sp.oo)==mu**2*J2**2

out={
 'classification':'RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUARTIC_SPATIAL_EXACT_PASS',
 'status':'FIRST_NONZERO_CONSTRAINED_LOCAL_REST_SCALAR_ACTION_IS_QUARTIC_AND_PURELY_SPATIAL',
 'target':TARGET,
 'prerequisite':PRE,
 'quartic_before_auxiliary_elimination':'S4/M_Pl^2 = integral [|grad y|^2 + mu_K^2 (y-J)^2], J=|grad phi|^2/2',
 'quartic_auxiliary_equation':'(-Delta+mu_K^2)y=mu_K^2 J',
 'quartic_effective_operator':'S4/M_Pl^2 = integral J [mu_K^2(-Delta)/(mu_K^2-Delta)] J',
 'fourier_composite_kernel':'mu_K^2 K^2/(mu_K^2+K^2) * |J_K|^2',
 'sign':'nonnegative for mu_K^2>0 and K^2>=0',
 'time_derivative_at_quartic':'absent; the F=1+dot(phi)-B.grad(phi) prefactor first multiplies a bracket that is already O(phi^4), so it contributes only at O(phi^5) or higher',
 'limits':{
   'K_much_less_mu':'kernel -> K^2 |J_K|^2',
   'K_much_greater_mu':'kernel -> mu_K^2 |J_K|^2'
 },
 'interpretation':'The enhanced local-rest branch has no quadratic finite-k scalar propagator, while its first nonzero constrained scalar self-action is a positive quartic spatial functional. This sharpens the constraint-bifurcation/strong-coupling warning but does not by itself decide whether the scalar is removed nonlinearly or becomes strongly coupled once the first time-dependent interaction is included.',
 'non_claims':t['non_claims'],
 'next_gate':t['next_gate_if_pass']
}
open('u1_local_rest_constrained_quartic_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
