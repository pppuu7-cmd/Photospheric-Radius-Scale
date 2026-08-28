#!/usr/bin/env python3
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
t = json.loads((R/'research/theory_targets/RTK_C9_PROJECTABLE_RADIATIVE_EVALUABILITY_SOURCE_LOCK_AUDIT_TARGET_v1.json').read_text())
ct = json.loads((R/'research/theory_results/RTK_C9_PROJECTABLE_COUNTERTERM_BASIS_PREFLIGHT_RESULT_v1.json').read_text())
z = json.loads((R/'research/theory_results/RTK_C10_65S6FZ24_INTERFACE_IDENTIFIABILITY_BOUNDARY_DECISION_RESULT_v1.json').read_text())

checks = {
 'target_frozen': t['status']=='FROZEN_BEFORE_RADIATIVE_EVALUABILITY_AUDIT',
 'counterterm_parent_exact': ct['classification']=='RTK_C9_PROJECTABLE_SYMMETRY_ALLOWS_NONVANISHING_FINITE_K_COUNTERTERM_DIRECTIONS_PASS_SCOPED',
 'z24_parent_exact': z['classification']=='C10_65S6FZ24_PARAMETER_UNDERDETERMINED_STOP_DECISION_PASS_SCOPED',
 'no_representative_selected': z['checks']['no_representative_point_selected'] is True,
 'no_exact_selector': z['decision']['source_locked_exact_selector_found'] is False,
 'interface_underdetermined': z['decision']['current_hmt_z7_interface_parameter_underdetermined'] is True,
 'new_input_required': z['decision']['new_independent_microscopic_input_required'] is True,
 'no_beta_claim': ct['scope_boundary']['beta_functions_computed'] is False,
 'no_generation_claim': ct['scope_boundary']['actual_loop_generation_proven'] is False,
 'soft_s_blocked': z['soft_s_retest_allowed'] is False,
 'k003_blocked': z['production_k003_unblocked'] is False,
 'threshold_unchanged': t['threshold_changed'] is False and z['threshold_changed'] is False,
}
ok=all(checks.values())
classification='RTK_C9_PROJECTABLE_ONE_LOOP_EVALUABILITY_BLOCKED_BY_UNRESOLVED_MATTER_INTERFACE_PASS_SCOPED' if ok else 'RTK_C9_PROJECTABLE_RADIATIVE_EVALUABILITY_SOURCE_LOCK_AUDIT_FAIL_SCOPED'
result={
 'schema':'RTK_C9_PROJECTABLE_RADIATIVE_EVALUABILITY_SOURCE_LOCK_AUDIT_RESULT_v1',
 'classification':classification,
 'status':'PASS_SCOPED' if ok else 'FAIL_SCOPED',
 'checks':checks,
 'formal_identity':t['formal_identity'],
 'decision':{
  'unique_same_action_one_loop_functional_source_locked': False if ok else None,
  'quantitative_beta_function_calculation_authorized': False if ok else None,
  'new_independent_microscopic_interface_input_required': True if ok else None,
  'representative_interface_selection_authorized':False,
  'full_C9_closed':False},
 'interpretation':'Projectability removes the old acceleration pair but leaves invariant finite-k carrier directions, while Z24 leaves the physical HMT matter interface source-unfixed. A unique quantitative same-action one-loop/RG calculation therefore is not yet source-locked. This makes no claim that a particular beta function is nonzero.' if ok else 'Frozen source-lock criteria were not reproduced.',
 'nonclaims':t['non_claims'],
 'next_gate':t['next_gate_if_source_lock_incomplete'] if ok else 'diagnose without weakening frozen criteria',
 'threshold_changed':False}
(R/'research/theory_results/RTK_C9_PROJECTABLE_RADIATIVE_EVALUABILITY_SOURCE_LOCK_AUDIT_RESULT_v1.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
raise SystemExit(0 if ok else 1)
