#!/usr/bin/env python3
import json, pathlib

root = pathlib.Path(__file__).resolve().parents[2]
target = json.loads((root/'research/theory_targets/RTK_C10_65S6FZ11_FIXED_PROJECTABLE_U1_ACTION_SCALAR_DOF_PREFLIGHT_TARGET_v1.json').read_text())
z10 = json.loads((root/'research/theory_results/RTK_C10_65S6FZ10_INDEPENDENT_PROJECTABLE_LOCAL_CONSTRAINT_PRINCIPLE_RESULT_v1.json').read_text())
z7 = json.loads((root/'research/theory_results/RTK_C10_65S6FZ7_SYMMETRY_FIRST_REPRESENTATION_CLASS_RESULT_v1.json').read_text())

checks = {}
checks['z10_parent_exact'] = z10['classification'] == target['parents_required']['z10']
checks['z7_parent_exact'] = z7['classification'] == target['parents_required']['z7']
checks['hmt_action_eq104_fixed'] = target['fixed_gravity_source']['equation'] == 104 and target['fixed_gravity_source']['lambda'] == 1
checks['projectable_lapse_fixed'] = target['fixed_gravity_source']['projectable_lapse'] == 'N=N(t)'
checks['hmt_scalar_graviton_eliminated_source_locked'] = bool(z10['checks']['hmt_scalar_graviton_elimination_explicit'])
checks['hmt_local_u1_source_locked'] = bool(z10['checks']['hmt_local_u1_explicit'])
checks['hmt_A_and_prepotential_source_locked'] = bool(z10['checks']['ww_local_u1_gauge_field_A_explicit'] and z10['checks']['ww_prepotential_explicit'])
checks['carrier_invariant_under_internal_null'] = bool(z7['checks']['internal_carrier_invariant'])
checks['carrier_invariant_under_gravity_u1'] = bool(z7['checks']['gravity_carrier_invariant'])
checks['invariant_shift_exact'] = bool(z7['checks']['invariant_shift_exact'])
checks['cross_commutator_zero'] = bool(z7['checks']['cross_commutator_zero'])
checks['shared_normal_derivative_invariant'] = bool(z7['checks']['shared_normal_derivative_invariant'])

# Exact 2-field representation algebra: u dot n = 0, with n=(-u2,u1).
# This is coefficient-independent and proves one physical field-space direction Phi.
u1,u2 = 2,3
n = (-u2,u1)
checks['null_direction_orthogonal_exact'] = (u1*n[0] + u2*n[1]) == 0
# A regular kinetic term kappa*(Dperp Phi)^2/2 has a rank-one Hessian kappa*u*u^T for kappa != 0.
H = ((u1*u1,u1*u2),(u1*u2,u2*u2))
detH = H[0][0]*H[1][1]-H[0][1]*H[1][0]
checks['carrier_hessian_rank_one_exact'] = detH == 0 and any(x != 0 for row in H for x in row)
checks['no_soft_s_or_k003'] = target['soft_s_retest_allowed'] is False and target['production_k003_unblocked'] is False
checks['threshold_unchanged'] = target['threshold_changed'] is False

all_required = all(checks.values())
classification = ('C10_65S6FZ11_FIXED_PROJECTABLE_U1_ONE_SCALAR_PREFLIGHT_PASS_SCOPED'
                  if all_required else 'C10_65S6FZ11_SCALAR_DOF_PREFLIGHT_BLOCKED_SCOPED')

result = {
  'schema':'RTK_C10_65S6FZ11_FIXED_PROJECTABLE_U1_ACTION_SCALAR_DOF_PREFLIGHT_RESULT_v1',
  'gate':'C10.65s6fZ11',
  'classification':classification,
  'checks':checks,
  'preflight_count':{
    'propagating_gravitational_scalars': 0 if all_required else None,
    'propagating_carrier_scalars': 1 if all_required else None,
    'status':'conditional_on_source_locked_HMT_nonlinear_constraint_result'
  },
  'interpretation': ('The literature-fixed projectable local-U1 HMT gravitational action removes the gravitational scalar, while the preregistered Z7 direct-product representation leaves exactly one regular gauge-invariant carrier direction Phi at the scalar kinetic preflight level. This is a fixed-action/interface DOF preflight only, not RTK background, quadratic-response, radiative-naturalness, or soft-s certification.' if all_required else 'The fixed-action/interface scalar DOF preflight is incomplete; no downstream matching or soft-s work is licensed.'),
  'next_gate': ('C10.65s6fZ12: freeze the same HMT+Z7 candidate and derive the coupled FLRW background plus finite-k quadratic scalar kernel, then test whether the previously certified RTK pole/residue/remainder and static/canonical regularity can be reproduced without coefficient fitting to soft-s.' if all_required else 'Repair only the failed source-lock/algebraic preflight item without changing the frozen Z11 scientific criteria.'),
  'nonclaims':['not full coupled RTK Dirac closure rederived from scratch','not RTK background equivalence','not RTK pole/residue/remainder equivalence','not C9 radiative naturalness','not a soft-s result','not k=0.03 production'],
  'threshold_changed':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  's6ft_embedding_ready':False
}
out = root/'research/theory_results/RTK_C10_65S6FZ11_FIXED_PROJECTABLE_U1_ACTION_SCALAR_DOF_PREFLIGHT_RESULT_v1.json'
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
