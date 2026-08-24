#!/usr/bin/env python3
"""First time-dependent constrained local-rest scalar interaction."""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUINTIC_TIME_TARGET_v1.json'
PRE='research/theory_results/RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUARTIC_RESULT_v1.json'
t=json.load(open(TARGET)); pre=json.load(open(PRE))
assert t['classification']=='RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUINTIC_TIME_TARGET_V1_FROZEN'
assert pre['classification']=='RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUARTIC_SPATIAL_EXACT_PASS'

eps=sp.symbols('eps', real=True)
mu=sp.symbols('mu', positive=True, finite=True, real=True)
K=sp.symbols('K', nonnegative=True, finite=True, real=True)
y2,y3,J2,f1,f2=sp.symbols('y2 y3 J2 f1 f2', finite=True, real=True)
# f1 is dot(phi); f2 includes -B.grad(phi) and other second-order pieces.
y=eps**2*y2+eps**3*y3
J=eps**2*J2
F=1+eps*f1+eps**2*f2
Y=1+y
D=sp.expand(Y**2-2*J)
s=sp.series(sp.sqrt(D)-1,eps,0,6).removeO().expand()
p_lead=sp.expand(mu**2*s**2)  # DBI lambda corrections begin at s^4=O(eps^8)
mixed=K**2*y**2  # denominator 1/D changes this only at O(eps^6)+
pref=sp.series(F/Y,eps,0,6).removeO().expand()
L=sp.series(pref*(p_lead+mixed),eps,0,7).removeO().expand()
L4=sp.factor(L.coeff(eps,4))
L5=sp.factor(L.coeff(eps,5))
expected4=sp.expand(K**2*y2**2+mu**2*(y2-J2)**2)
assert sp.simplify(L4-expected4)==0
EL4=sp.diff(expected4,y2)
# Quintic structure = y3 * quartic auxiliary EL equation + f1*L4.
assert sp.simplify(L5-(y3*EL4+f1*expected4))==0
# f2 (including B.grad phi) cannot contribute at O5.
assert sp.diff(L5,f2)==0

ys=sp.simplify(mu**2*J2/(K**2+mu**2))
assert sp.simplify(EL4.subs(y2,ys))==0
L4_on=sp.factor(expected4.subs(y2,ys))
L5_on=sp.factor(L5.subs(y2,ys))
assert sp.simplify(L4_on-mu**2*K**2/(mu**2+K**2)*J2**2)==0
assert sp.simplify(L5_on-f1*L4_on)==0
# The reduced quintic piece is linear, not quadratic, in the first-order velocity f1=dot(phi).
assert sp.diff(L5_on,f1,2)==0

out={
 'classification':'RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUINTIC_TIME_DEGENERACY_EXACT_PASS',
 'status':'FIRST_TIME_DEPENDENCE_APPEARS_LINEarly_AT_QUINTIC_ORDER_WITH_ZERO_VELOCITY_HESSIAN',
 'target':TARGET,
 'prerequisite':PRE,
 'off_shell_quintic_identity':'L5 = y3*(delta L4/delta y2) + dot(phi)*L4; second-order shift-advection pieces enter only at O6',
 'on_shell_quartic':'L4 = J [mu_K^2(-Delta)/(mu_K^2-Delta)] J',
 'on_shell_quintic_time':'L5_time = dot(phi) * { J [mu_K^2(-Delta)/(mu_K^2-Delta)] J } up to the spatial representation/integrations by parts used for the quartic functional',
 'velocity_hessian_through_quintic':'zero about phi=0; the first time-dependent term is linear in dot(phi)',
 'interpretation':'The exact local-rest branch remains temporally degenerate beyond the vanished quadratic action: the first time-dependent constrained interaction appears only at quintic order and is linear in the perturbation velocity. This makes a canonical/Dirac rank analysis mandatory before deciding whether the local scalar is nonlinearly removed or represents a strongly-coupled background.',
 'non_claims':t['non_claims'],
 'next_gate':t['next_gate_if_pass']
}
open('u1_local_rest_constrained_quintic_time_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
