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
try:
    s={k:show(v) for k,v in FILES.items()}
except Exception as e:
    print(e); sys.exit(3)
parent=json.loads(Path('research/theory_results/RTK_C10_65S6FZ_SYMMETRY_FIRST_PROJECTABLE_COMPLETION_REQUIREMENT_RESULT_v1.json').read_text())
y=json.loads(Path('research/theory_results/RTK_C10_65S6FY_SYMMETRY_FIRST_CANDIDATE_SPACE_AUDIT_RESULT_v1.json').read_text())
target=Path('research/theory_targets/RTK_C10_65S6FZ1_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_AUDIT_TARGET_v1.json')
checks={
 'target_present':target.exists(),
 'parent_exact':parent.get('classification')=='C10_65S6FZ_SYMMETRY_PROTECTED_PROJECTABLE_RANK_ONE_CLASS_PASS_SCOPED',
 'candidate_space_parent_exact':y.get('classification')=='C10_65S6FY_NO_SOURCE_LOCKED_PROJECTABLE_CANDIDATE_FOUND_PASS_SCOPED',
 'dirac_quadratic_scoped':'The statements here are quadratic and scoped. They do not constitute a final covariant completion.' in s['dirac'],
 'u1_not_asserted_solution':'The point of the U(1) route is not to assert that Hořava-U(1) solves RTK.' in s['u1'],
 'u1_requires_full_constrained_action':'full constrained action' in s['u1'],
 'u1_candidate_nonprojectable':'nonprojectable U(1) family-I candidate' in s['u1'],
 'u1n_nonprojectable':'nonprojectable local-U(1) completion route' in s['u1n'],
 'u1n_full_coupled_rank_open':'full coupled DOF rank still open' in s['u1n'],
}
source_ok=all(checks.values())
# A realization can only be credited if an archived construction is simultaneously nonlinear/full,
# projectable, and has a closed coupled constraint rank. The source-locked statements above rule
# this out for both archived candidate directions without interpreting missing structure as zero.
realization_found=False
classification=('C10_65S6FZ1_NO_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_FOUND_PASS_SCOPED' if source_ok and not realization_found else 'C10_65S6FZ1_AUDIT_INCOMPLETE_BLOCKED_SCOPED')
result={
 'schema':'RTK_C10_65S6FZ1_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_AUDIT_RESULT_v1',
 'gate':'C10.65s6fZ1',
 'classification':classification,
 'archived_source_commit':ARCHIVE,
 'checks':checks,
 'realization_found':realization_found,
 'finding':'No pre-soft-s archived construction is a source-locked projectable nonlinear realization of the s6fZ null-direction symmetry. The rank-one Dirac direction is explicitly quadratic/scoped; the U(1) direction is explicitly nonprojectable and retains an open full coupled constraint rank. Therefore the s6fZ symmetry class is nonempty mathematically but has no already-certified RTK action representative in the archive.',
 's6ft_embedding_ready':False,
 'soft_s_retest_allowed':False,
 'production_k003_unblocked':False,
 'next_gate':'C10.65s6fZ2: derive a minimal action-level projectable gauge realization template (field content and transformation law first, coefficients unfitted), then test whether it can embed the rank-one class while preserving one scalar DOF. Do not evaluate soft-s in that gate.',
 'threshold_changed':False,
 'provenance':{'workflow':'rtk-c10-65s6fz1-source-locked-nonlinear-symmetry-realization-audit.yml','threshold_changed':False}
}
Path('research/theory_results/RTK_C10_65S6FZ1_SOURCE_LOCKED_NONLINEAR_SYMMETRY_REALIZATION_AUDIT_RESULT_v1.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if source_ok else 2)
