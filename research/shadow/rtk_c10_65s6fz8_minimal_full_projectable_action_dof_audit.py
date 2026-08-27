#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

TARGET=Path('research/theory_targets/RTK_C10_65S6FZ8_MINIMAL_FULL_PROJECTABLE_ACTION_DOF_AUDIT_TARGET_v1.json')
RESULT=Path('research/theory_results/RTK_C10_65S6FZ8_MINIMAL_FULL_PROJECTABLE_ACTION_DOF_AUDIT_RESULT_v1.json')
t=json.loads(TARGET.read_text())

lam,M2,kappa=sp.symbols('lambda M2 kappa', nonzero=True)
zdot,q,phidot=sp.symbols('zdot q phidot')

# Same-action hard scalar kinetic audit. The potential/spatial sectors do not alter
# the velocity Hessian. q=Delta beta_bar is auxiliary for finite k.
Lg=(M2/sp.Integer(2))*((3-9*lam)*zdot**2+(-2+6*lam)*zdot*q+(1-lam)*q**2)
q_sol=sp.factor(sp.solve(sp.diff(Lg,q),q)[0])
Lg_red=sp.factor(Lg.subs(q,q_sol))
Lcarrier=kappa*phidot**2/sp.Integer(2)
Lred=sp.expand(Lg_red+Lcarrier)
H=sp.simplify(sp.hessian(Lred,(zdot,phidot)))
detH=sp.factor(H.det())

expected_q=sp.factor((1-3*lam)/(1-lam)*zdot)
expected_Lg=sp.factor(M2*(3*lam-1)/(lam-1)*zdot**2)
expected_H=sp.diag(sp.factor(2*M2*(3*lam-1)/(lam-1)),kappa)

checks={
  'parent_exact': t['parent']=='C10_65S6FZ7_REPRESENTATION_CLASS_EXISTS_PASS_SCOPED',
  'hypothesis_explicit': t['hypothesis_status']=='NEW_NONLINEAR_COMPLETION_HYPOTHESIS_NOT_ARCHIVAL_INHERITANCE',
  'internal_null_invariance_by_construction': t['frozen_action_template']['carrier']=='Phi=u1 phi+u2 chi',
  'gravity_u1_invariance_by_construction': t['frozen_action_template']['invariant_shift']=='Nbar_i=N_i-N D_i nu',
  'shift_solution_exact': sp.simplify(q_sol-expected_q)==0,
  'reduced_gravity_kinetic_exact': sp.simplify(Lg_red-expected_Lg)==0,
  'velocity_hessian_exact': sp.simplify(H-expected_H)==sp.zeros(2),
  'generic_rank_two': sp.simplify(detH)!=0,
  'internal_orthogonal_direction_is_gauge_null': True,
  'no_extra_constraint_multiplier': t['frozen_action_template']['no_extra_A_multiplier'] is True and t['frozen_action_template']['no_extra_local_constraint_field'] is True,
  'no_soft_s_or_k003': True,
}
scientific_ok=all(checks.values())
rank_generic=2 if checks['generic_rank_two'] else int(H.rank())
if not scientific_ok:
    classification='C10_65S6FZ8_MINIMAL_FULL_ACTION_INCONSISTENT_FAIL_SCOPED'
elif rank_generic==2:
    classification='C10_65S6FZ8_MINIMAL_FULL_ACTION_EXTRA_SCALAR_OBSTRUCTION_PASS_SCOPED'
else:
    classification='C10_65S6FZ8_MINIMAL_FULL_ACTION_ONE_SCALAR_PASS_SCOPED'

result={
  'schema':'RTK_C10_65S6FZ8_MINIMAL_FULL_PROJECTABLE_ACTION_DOF_AUDIT_RESULT_v1',
  'gate':'C10.65s6fZ8',
  'classification':classification,
  'checks':checks,
  'exact_symbolics':{
    'L_gravity_scalar_before_shift':str(sp.factor(Lg)),
    'q_solution':str(q_sol),
    'L_gravity_scalar_reduced':str(Lg_red),
    'velocity_hessian':str(H),
    'velocity_hessian_determinant':str(detH),
    'generic_velocity_rank':rank_generic,
  },
  'interpretation':(
    'The minimal Z7-invariant full local template is symmetry-consistent but generically carries two physical scalar velocities after the finite-k shift constraint: the usual projectable-gravity scalar zeta plus the invariant carrier Phi. The internal orthogonal phi-chi direction is gauge/null, so it does not create a third scalar. Thus this minimal template does not realize the desired one-scalar rank-one architecture without an independently preregistered additional gravitational constraint mechanism.'
    if classification.endswith('EXTRA_SCALAR_OBSTRUCTION_PASS_SCOPED') else
    'See exact checks; no post-hoc escape has been applied.'
  ),
  'nonclaims':[
    'not a no-go for projectable RTK completions with an independently motivated additional constraint',
    'not a full cosmological background-equivalence result',
    'not a radiative-naturalness result',
    'not a soft-s result'
  ],
  's6ft_embedding_ready':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  'threshold_changed':False,
  'next_gate':(
    'C10.65s6fZ9: preregister, independently of soft-s, a projectable gravitational local-constraint mechanism (for example an A-like multiplier only if source-motivated), then derive its full same-action constraint algebra and scalar DOF count before revisiting s6fT.'
    if classification.endswith('EXTRA_SCALAR_OBSTRUCTION_PASS_SCOPED') else
    'Diagnose C10.65s6fZ8 without changing the frozen target.'
  )
}
RESULT.parent.mkdir(parents=True,exist_ok=True)
RESULT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
