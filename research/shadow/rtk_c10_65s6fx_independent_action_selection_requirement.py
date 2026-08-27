#!/usr/bin/env python3
import json, sys
from pathlib import Path

TARGET=Path('research/theory_targets/RTK_C10_65S6FX_INDEPENDENT_ACTION_SELECTION_REQUIREMENT_TARGET_v1.json')
P_V=Path('research/theory_results/RTK_C10_65S6FV_RANK_ONE_EMBEDDING_IDENTIFIABILITY_RESULT_v1.json')
P_W=Path('research/theory_results/RTK_C10_65S6FW_PRE_SOFTS_ARCHIVE_PRINCIPLE_AUDIT_RESULT_v1.json')

checks={
  'target_present': TARGET.exists(),
  'parent_s6fv_present': P_V.exists(),
  'parent_s6fw_present': P_W.exists(),
}
if not all(checks.values()):
    raise SystemExit('required frozen inputs missing')

t=json.loads(TARGET.read_text())
v=json.loads(P_V.read_text())
w=json.loads(P_W.read_text())
checks.update({
  'target_gate_exact': t.get('gate')=='C10.65s6fX',
  'threshold_unchanged': t.get('guards',{}).get('threshold_changed') is False,
  'no_soft_s_retest': t.get('guards',{}).get('no_soft_s_retest') is True,
  'no_k003_production': t.get('guards',{}).get('no_k003_production') is True,
  'parent_s6fv_exact': v.get('classification')=='C10_65S6FV_RANK_ONE_FULL_EMBEDDING_NON_IDENTIFIABLE_PASS_SCOPED',
  'parent_s6fw_exact': w.get('classification')=='C10_65S6FW_NO_INDEPENDENT_PRE_SOFTS_EMBEDDING_PRINCIPLE_FOUND_PASS_SCOPED',
  's6fw_embedding_not_ready': w.get('s6ft_embedding_ready') is False,
  's6fw_softs_forbidden': w.get('soft_s_retest_allowed') is False,
  's6fw_k003_forbidden': w.get('production_k003_unblocked') is False,
})

# Frozen logic: s6fV proves the rank-one class is non-identifiable from the one-pole
# structure; s6fW proves the source-locked pre-soft-s archive contains no unique
# selector for the missing field map / matrix / source direction. Therefore the
# present repository has no admissible uniquely selected full action. This is a
# fail-closed architecture result, not a theory no-go.
all_required=all(checks.values())
classification=(
  'C10_65S6FX_NO_ADMISSIBLE_INDEPENDENT_ACTION_SELECTION_BLOCKED_SCOPED'
  if all_required else
  'C10_65S6FX_ACTION_SELECTION_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
)
result={
  'schema':'RTK_C10_65S6FX_INDEPENDENT_ACTION_SELECTION_REQUIREMENT_RESULT_v1',
  'gate':'C10.65s6fX',
  'classification':classification,
  'checks':checks,
  'finding':(
    'The source-locked RTK state cannot uniquely select a full projectable rank-one nonlinear action without adding an independent principle. s6fV establishes non-identifiability inside the rank-one one-pole class and s6fW establishes that the pre-soft-s C8/C9 archive does not supply the missing selector. The correct action is therefore to retain the s6fT blocker rather than fit field-map, potential/algebraic data, or source direction to the already observed soft-s obstruction.'
    if all_required else
    'The frozen admissibility audit could not verify every parent/guard; fail closed.'
  ),
  'action_selection_ready':False,
  's6ft_embedding_ready':False,
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  'next_gate':'C10.65s6fY: symmetry-first candidate-space audit. Search only independently motivated projectable symmetry/degeneracy constructions that fix the missing full-action data before any new soft-s calculation; if none is source-lockable, keep the branch blocked.',
  'threshold_changed':False,
  'provenance':{
    'workflow':'rtk-c10-65s6fx-independent-action-selection-requirement.yml',
    'threshold_changed':False
  }
}
Path('research/theory_results/RTK_C10_65S6FX_INDEPENDENT_ACTION_SELECTION_REQUIREMENT_RESULT_v1.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
sys.exit(0 if all_required else 2)
