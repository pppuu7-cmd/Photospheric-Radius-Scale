#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path

ARCHIVE='13acfdbc16d2f3117f1299b8552bcf7b1f996bd1'
FILES={
 'dirac':'research/methods/RTK_FORMULA_BIBLE_C8_DEGENERATE_AUXILIARY_APPENDIX.md',
 'u1':'research/methods/RTK_FORMULA_BIBLE_C8_U1_COMPLETION_APPENDIX.md',
 'u1n':'research/RTK_C8_U1_CANONICAL_NARROWING_2026-08-22.md',
}
def show(p):
    return subprocess.check_output(['git','show',f'{ARCHIVE}:{p}'],text=True)
s={k:show(v) for k,v in FILES.items()}
parent_path=Path('research/theory_results/RTK_C10_65S6FX_INDEPENDENT_ACTION_SELECTION_REQUIREMENT_RESULT_v1.json')
target_path=Path('research/theory_targets/RTK_C10_65S6FY_SYMMETRY_FIRST_CANDIDATE_SPACE_AUDIT_TARGET_v1.json')
parent=json.loads(parent_path.read_text()) if parent_path.exists() else {}
checks={
 'target_present':target_path.exists(),
 'parent_exact':parent.get('classification')=='C10_65S6FX_NO_ADMISSIBLE_INDEPENDENT_ACTION_SELECTION_BLOCKED_SCOPED',
 'dirac_explicitly_quadratic_scoped':'The statements here are quadratic and scoped. They do not constitute a final covariant completion.' in s['dirac'],
 'u1_route_not_asserted_solution':'The point of the U(1) route is not to assert that Hořava-U(1) solves RTK.' in s['u1'],
 'u1_requires_full_constrained_action':'must derive the desired one-scalar structure from the *full constrained action*' in s['u1'],
 'u1_next_candidate_explicitly_nonprojectable':'freeze one concrete nonprojectable U(1) family-I candidate' in s['u1'],
 'u1n_status_full_coupled_dof_open':'full coupled DOF rank still open' in s['u1n'],
 'u1n_route_explicitly_nonprojectable':'nonprojectable local-U(1) completion route' in s['u1n'],
 'u1n_next_gate_still_constraint_rank':'compute the coupled second-class Poisson submatrix/rank' in s['u1n'],
}
all_required=all(checks.values())
classification=('C10_65S6FY_NO_SOURCE_LOCKED_PROJECTABLE_CANDIDATE_FOUND_PASS_SCOPED' if all_required else 'C10_65S6FY_CANDIDATE_SPACE_AUDIT_INCOMPLETE_BLOCKED_SCOPED')
result={
 'schema':'RTK_C10_65S6FY_SYMMETRY_FIRST_CANDIDATE_SPACE_AUDIT_RESULT_v1',
 'gate':'C10.65s6fY',
 'classification':classification,
 'archived_source_commit':ARCHIVE,
 'checks':checks,
 'finding':('The pre-soft-s archive contains independently motivated degeneracy/U(1) directions, but none is already a source-locked projectable full nonlinear completion. The Dirac rank-one construction is explicitly quadratic/scoped; the U(1) action route is explicitly nonprojectable and still has an open coupled constraint rank. Therefore neither can be promoted into s6fT without new action-level work.' if all_required else 'The frozen archive candidate-space audit could not verify every required statement; fail closed.'),
 's6ft_embedding_ready':False,
 'soft_s_retest_allowed':False,
 'production_k003_unblocked':False,
 'next_gate':'C10.65s6fZ: derive a symmetry-first projectable completion requirement/class theorem rather than selecting coefficients from the failed soft-s channel. Any new candidate must be action-complete and preregistered before soft-s evaluation.',
 'threshold_changed':False,
 'provenance':{'workflow':'rtk-c10-65s6fy-symmetry-first-candidate-space-audit.yml','threshold_changed':False}
}
Path('research/theory_results/RTK_C10_65S6FY_SYMMETRY_FIRST_CANDIDATE_SPACE_AUDIT_RESULT_v1.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if all_required else 2)
