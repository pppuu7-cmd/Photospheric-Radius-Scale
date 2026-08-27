#!/usr/bin/env python3
import json
from pathlib import Path

TARGET=Path('research/theory_targets/RTK_C10_65S6FT_FULL_PROJECTABLE_ADM_EMBEDDING_SOURCE_LOCK_TARGET_v1.json')
PARENT=Path('research/theory_results/RTK_C10_65S6FS_DIRAC_DEGENERATE_CANDIDATE_RESTART_RESULT_v1.json')
APP=Path('research/methods/RTK_FORMULA_BIBLE_C8_DEGENERATE_AUXILIARY_APPENDIX.md')
OUT=Path('research/theory_results/RTK_C10_65S6FT_FULL_PROJECTABLE_ADM_EMBEDDING_SOURCE_LOCK_RESULT_v1.json')

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())
a=APP.read_text()

checks={
 'target_frozen_before_execution': t['status']=='FROZEN_BEFORE_EXECUTION',
 'parent_exact_classification': p.get('classification')=='C10_65S6FS_DIRAC_DEGENERATE_CANDIDATE_RESTART_PASS_SCOPED',
 'parent_explicitly_not_full_action': 'not a full RTK action' in p.get('nonclaims',[]),
 'parent_requires_source_alignment_derived': 'derive source alignment rather than impose it' in p.get('next_gate',''),
 'historical_appendix_quadratic_scoped': 'The statements here are quadratic and scoped. They do not constitute a final covariant completion.' in a,
 'historical_appendix_embedding_still_next': 'embed the rank-one kinetic pair into the full FLRW lapse/shift scalar constraint block' in a,
 'historical_appendix_source_direction_still_next': 'derive the source direction from the same action' in a,
 'no_soft_s_retest': p.get('soft_s_retest_allowed') is False,
 'k003_still_blocked': p.get('production_k003_unblocked') is False,
 'threshold_changed': False
}

missing=[
 'one explicit projectable ADM action containing the rank-one kinetic pair',
 'explicit map from toy variables X,y to ADM/clock fields',
 'lapse and scalar-shift dependence fixed by the same action',
 'source direction derived from the action rather than imposed',
 'background coefficient functions fixed without using the failed soft-s observable',
 'nonlinear action sufficient for a full Dirac constraint count'
]

assert all(v for k,v in checks.items() if k!='threshold_changed')
classification='C10_65S6FT_BLOCKED_NO_FULL_PROJECTABLE_ADM_EMBEDDING_SCOPED'
result={
 'schema':'RTK_C10_65S6FT_FULL_PROJECTABLE_ADM_EMBEDDING_SOURCE_LOCK_RESULT_v1',
 'gate':'C10.65s6fT',
 'classification':classification,
 'decision':'BLOCKED_NO_FULL_PROJECTABLE_ADM_EMBEDDING_SCOPED',
 'checks':checks,
 'missing_source_locked_inputs':missing,
 'evidence':{
   'parent_candidate_lagrangian':p['candidate']['lagrangian'],
   'parent_nonclaim':'not a full RTK action',
   'historical_scope':'quadratic/scoped; not a final covariant completion'
 },
 'soft_s_retest_allowed':False,
 'production_k003_unblocked':False,
 'threshold_changed':False,
 'next_gate':t['next_if_blocked'],
 'nonclaims':t['nonclaims']
}
OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(classification)
print(json.dumps(result,indent=2,sort_keys=True))
