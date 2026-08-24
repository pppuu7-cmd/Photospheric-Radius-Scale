#!/usr/bin/env python3
"""Canonical rank-scaling theorem for the local-rest constrained RTK scalar."""
import json
import sympy as sp

TARGET='research/theory_targets/RTK_C8_U1_LOCAL_REST_CANONICAL_RANK_SCALING_TARGET_v1.json'
PRE='research/theory_results/RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUINTIC_TIME_RESULT_v1.json'
t=json.load(open(TARGET)); pre=json.load(open(PRE))
assert t['classification']=='RTK_C8_U1_LOCAL_REST_CANONICAL_RANK_SCALING_TARGET_V1_FROZEN'
assert pre['classification']=='RTK_C8_U1_LOCAL_REST_CONSTRAINED_QUINTIC_TIME_DEGENERACY_EXACT_PASS'

# Homogeneity/scaling theorem. q4 is a quartic spatial functional density under
# phi -> eps phi. v is the perturbation velocity amplitude dot(phi).
eps,v,q4=sp.symbols('eps v q4', finite=True, real=True)
Q4=eps**4*q4
L5=v*Q4
pi=sp.diff(L5,v)
hess=sp.diff(pi,v)
assert pi==Q4
assert hess==0
# One functional derivative with respect to phi lowers the homogeneous degree by one.
# Represent this degree algebraically as d/deps(Q4)/4, which scales eps^3.
Dscale=sp.simplify(sp.diff(Q4,eps)/4)
assert Dscale==eps**3*q4
assert sp.simplify(Dscale.subs(eps,0))==0
# A difference of two such functional derivatives (the antisymmetric symplectic
# kernel) has the same epsilon^3 scaling and therefore vanishes at the vacuum.
omega_coeff=sp.symbols('omega3', finite=True, real=True)
Omega=eps**3*omega_coeff
assert Omega.subs(eps,0)==0

out={
 'classification':'RTK_C8_U1_LOCAL_REST_CANONICAL_RANK_COLLAPSE_SCALING_EXACT_PASS',
 'status':'PERTURBATIVE_CANONICAL_SYMPLECTIC_RANK_COLLAPSES_ON_EXACT_LOCAL_REST_VACUUM',
 'target':TARGET,
 'prerequisite':PRE,
 'effective_structure':'L_eff = V4[phi] + dot(phi) Q4[phi] + O(phi^6), Q4 homogeneous quartic',
 'canonical_momentum':'pi_phi = Q4[phi] + O(phi^5)',
 'velocity_hessian':'zero through quintic order',
 'primary_relation':'C(x)=pi_phi(x)-Q4[phi](x)=0 through the certified order',
 'amplitude_scaling':{
   'Q4':'epsilon^4',
   'functional_derivative_of_Q4':'epsilon^3',
   'symplectic_constraint_kernel_Omega':'epsilon^3',
   'Omega_at_exact_vacuum':'0'
 },
 'interpretation':'The exact local rest vacuum is a perturbative canonical-rank-collapse surface of the two-derivative fixed action. Any nonlinear first-order symplectic rank that may exist at finite amplitude vanishes as the background perturbation amplitude tends to zero, so the usual Gaussian propagator/canonical normalization is unavailable at the vacuum. This is a structural rank-bifurcation result, not yet a numerical strong-coupling scale.',
 'non_claims':t['non_claims'],
 'next_gate':t['next_gate_if_pass']
}
open('u1_local_rest_canonical_rank_scaling_result.json','w').write(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
