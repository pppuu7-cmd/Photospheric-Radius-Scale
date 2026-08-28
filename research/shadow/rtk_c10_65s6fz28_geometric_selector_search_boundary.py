#!/usr/bin/env python3
import json, pathlib

TARGET=pathlib.Path('research/theory_targets/RTK_C10_65S6FZ28_GEOMETRIC_SELECTOR_SEARCH_BOUNDARY_TARGET_v1.json')
PARENT=pathlib.Path('research/theory_results/RTK_C10_65S6FZ27_TNC_BARGMANN_HMT_INTERFACE_SELECTOR_AUDIT_RESULT_v1.json')
RESULT=pathlib.Path('research/theory_results/RTK_C10_65S6FZ28_GEOMETRIC_SELECTOR_SEARCH_BOUNDARY_RESULT_v1.json')

t=json.loads(TARGET.read_text())
p=json.loads(PARENT.read_text())

parent_exact=(p.get('classification')==t['parent_required'])
geo=p.get('geometric_checks',{})
sel=p.get('selector_checks',{})
req=t['required_parent_facts']
checks={
  'parent_exact': parent_exact,
  'projectable_horava_from_tnc': geo.get('projectable_horava_from_torsionless_newton_cartan') is req['projectable_horava_from_torsionless_newton_cartan'],
  'hmt_u1_from_bargmann': geo.get('hmt_u1_from_bargmann_extension') is req['hmt_u1_from_bargmann_extension'],
  'no_explicit_physical_metric_selector': sel.get('explicit_hmt_physical_metric_matter_interface') is req['explicit_hmt_physical_metric_matter_interface'],
  'no_unique_a1_a2_relation': sel.get('unique_a1_a2_equivalent_relation') is req['unique_a1_a2_equivalent_relation'],
  'no_same_principle_matter_coefficients': sel.get('same_principle_derives_matter_coefficients') is req['same_principle_derives_matter_coefficients'],
  'no_posthoc_coefficient_selection': True,
  'soft_s_and_k003_stay_blocked': (t['soft_s_retest_allowed'] is False and t['production_k003_unblocked'] is False),
  'threshold_unchanged': t['threshold_changed'] is False
}

if all(checks.values()):
    cls='C10_65S6FZ28_GEOMETRIC_SELECTOR_SEARCH_CLASS_STOP_PASS_SCOPED'
    interpretation=(
      'Z27 establishes a strong geometric origin for projectable Horava/HMT U(1) through torsionless Newton-Cartan/Bargmann structure, while the same audited source still does not derive the unresolved physical-matter interface or a unique a1,a2-equivalent relation. Therefore further geometric/covariant reformulations of the same structure are not admissible as coefficient selectors by themselves. This is a scoped identifiability boundary only; a genuinely new microscopic same-action matter derivation remains admissible.'
    )
else:
    cls='C10_65S6FZ28_PARENT_INCONSISTENT_BLOCKED_SCOPED'
    interpretation='The frozen Z27 parent facts were not reproduced exactly, so the boundary decision fails closed.'

out={
  'schema':'RTK_C10_65S6FZ28_GEOMETRIC_SELECTOR_SEARCH_BOUNDARY_RESULT_v1',
  'gate':'C10.65s6fZ28',
  'classification':cls,
  'checks':checks,
  'interpretation':interpretation,
  'successor_requirement':t['successor_requirement'],
  'soft_s_retest_allowed':False,
  'production_k003_unblocked':False,
  'c9_naturalness_closed':False,
  's6ft_embedding_ready':False,
  'threshold_changed':False
}
RESULT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
