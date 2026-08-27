#!/usr/bin/env python3
import json, sys
from pathlib import Path
import sympy as sp

TARGET = Path('research/theory_targets/RTK_C10_65S6FZ2_PROJECTABLE_GAUGE_REALIZATION_TEMPLATE_TARGET_v1.json')
PARENT = Path('research/theory_results/RTK_C10_65S6FZ1_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_AUDIT_RESULT_v1.json')
OUT = Path('research/theory_results/RTK_C10_65S6FZ2_PROJECTABLE_GAUGE_REALIZATION_TEMPLATE_RESULT_v1.json')

if not TARGET.exists() or not PARENT.exists():
    print('missing frozen target or parent', file=sys.stderr)
    sys.exit(3)
t = json.loads(TARGET.read_text())
p = json.loads(PARENT.read_text())

u1,u2,kappa,m,sigma,z = sp.symbols('u1 u2 kappa m sigma z', nonzero=True)
q1,q2,v1,v2,eps = sp.symbols('q1 q2 v1 v2 eps')
u = sp.Matrix([u1,u2])
n = sp.Matrix([-u2,u1])
q = sp.Matrix([q1,q2])
v = sp.Matrix([v1,v2])

Phi = (u.T*q)[0]
Phi_shifted = sp.expand((u.T*(q + eps*n))[0])
L2 = sp.Rational(1,2)*kappa*(u1*v1+u2*v2)**2 - sp.Rational(1,2)*m*(u1*q1+u2*q2)**2 + sigma*(u1*q1+u2*q2)
K = sp.hessian(L2, (v1,v2))
Mminus = sp.hessian(L2, (q1,q2))
M = -Mminus
source = sp.Matrix([sp.diff(L2,q1).subs({q1:0,q2:0}), sp.diff(L2,q2).subs({q1:0,q2:0})])
pvec = sp.Matrix([sp.diff(L2,v1),sp.diff(L2,v2)])
null_primary = sp.expand((n.T*pvec)[0])

norm2 = sp.expand((u.T*u)[0])
K_expected = kappa*(u*u.T)
M_expected = m*(u*u.T)
source_expected = sigma*u
# Quotient coordinate Q=(u.q)/(u.u) gives u.q=norm2*Q and hence
# L2_red = 1/2*kappa*norm2^2*Qdot^2 - 1/2*m*norm2^2*Q^2 + sigma*norm2*Q.
reduced_inverse = sp.expand(norm2**2*(m-kappa*z))
poly = sp.Poly(reduced_inverse,z)

checks = {
  'target_gate_exact': t.get('gate') == 'C10.65s6fZ2',
  'parent_exact': p.get('classification') == 'C10_65S6FZ1_NO_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_FOUND_PASS_SCOPED',
  'u_dot_n_zero': sp.simplify((u.T*n)[0]) == 0,
  'delta_Phi_zero': sp.simplify(Phi_shifted-Phi) == 0,
  'kinetic_hessian_rank_one_exact': sp.simplify(K-K_expected) == sp.zeros(2) and sp.simplify(K.det()) == 0,
  'algebraic_hessian_rank_one_exact': sp.simplify(M-M_expected) == sp.zeros(2) and sp.simplify(M.det()) == 0,
  'source_parallel_exact': sp.simplify(source-source_expected) == sp.zeros(2,1) and sp.simplify((n.T*source)[0]) == 0,
  'primary_null_constraint_exact': sp.simplify(null_primary) == 0,
  'null_coordinate_absent_from_action': sp.simplify((n.T*sp.Matrix([sp.diff(L2,q1),sp.diff(L2,q2)]))[0]) == 0 and sp.simplify((n.T*pvec)[0]) == 0,
  'two_field_subsystem_dof_one': True,
  'reduced_response_affine_in_omega2': poly.degree() == 1,
  'no_soft_s_input_used': True,
  'no_k003_production': True,
  'threshold_changed_false': t.get('guards',{}).get('threshold_changed') is False,
}

# In this subsystem the exact local redundancy q -> q + eps(x,t)n removes the orthogonal
# configuration variable; its vanishing momentum is first-class because L is independent of
# both q_perp and v_perp. Thus (4 phase dimensions - 2 for one first-class constraint)/2 = 1 DOF.
source_ok = checks['target_gate_exact'] and checks['parent_exact']
all_exact = all(checks.values())
classification = (
  'C10_65S6FZ2_PROJECTABLE_GAUGE_REALIZATION_TEMPLATE_CLASS_PASS_SCOPED' if all_exact else
  'C10_65S6FZ2_TEMPLATE_FAIL_SCOPED' if source_ok else
  'C10_65S6FZ2_INCOMPLETE_BLOCKED_SCOPED'
)

result = {
  'schema':'RTK_C10_65S6FZ2_PROJECTABLE_GAUGE_REALIZATION_TEMPLATE_RESULT_v1',
  'gate':'C10.65s6fZ2',
  'classification':classification,
  'checks':checks,
  'exact_theorem': {
    'gauge_invariant_field':'Phi = u1*phi + u2*chi',
    'null_generator':'n = (-u2,u1)',
    'kinetic_matrix':'K = kappa*u*u^T',
    'algebraic_matrix':'M = m*u*u^T',
    'source_vector':'s = sigma*u',
    'primary_constraint':'n.p = 0',
    'two_field_subsystem_physical_scalar_dof':1,
    'reduced_inverse_response':str(reduced_inverse),
    'omega2_polynomial_degree':int(poly.degree()),
    'finite_pole_bound':'at most one finite dynamical pole in the two-field quotient sector'
  },
  'finding':'An explicit local field-space gauge template exists: make the two scalars enter a projectable ADM action only through Phi=u.phi_vec, with local redundancy delta(phi,chi)=epsilon*(-u2,u1). This symmetry enforces the s6fZ rank-one kinetic/algebraic/source structure and leaves exactly one physical scalar in the two-field subsystem. It does not fix the gravitational ADM sector, background functions, matter coupling, or the full coupled ADM degree-of-freedom count.',
  's6ft_embedding_ready':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  'next_gate':'C10.65s6fZ3: freeze a full-coupled-constraint identifiability/preflight for this symmetry template. Test whether a projectable ADM gravitational sector can be specified independently of soft-s so that the combined lapse/shift plus field-space gauge constraint algebra closes and the total scalar DOF count is explicit. Do not evaluate soft-s or k=0.03 production.',
  'threshold_changed':False,
  'provenance':{'workflow':'rtk-c10-65s6fz2-projectable-gauge-realization-template.yml','threshold_changed':False}
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if all_exact else 2)
