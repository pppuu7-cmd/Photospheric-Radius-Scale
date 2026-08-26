#!/usr/bin/env python3
import json,math
from pathlib import Path
R=Path(__file__).resolve().parents[2]
L=lambda p: json.loads((R/p).read_text())
t=L('research/theory_targets/RTK_C10_65S2J_PROSPECTIVE_RETRY_WIDTH_TARGET_v1.json')
i=L('research/theory_results/RTK_C10_65S2I_ADAPTIVE_STEP_TRACE_RESULT_v1.json')
s=L('research/theory_results/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_RESULT_v1.json')
checks={}
checks['target_frozen']=t['status']=='FROZEN_BEFORE_SELECTION_CHECK'
checks['parents']=i['classification']=='C10_65S2I_ADAPTIVE_STEP_TRACE_PASS_SCOPED' and s['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'
observed=min(float(r['first_accepted_hdid']) for r in i['records'])
checks['source_value_exact']=observed==float(t['selection_rule']['source_value_Mpc'])
f=float(t['selection_rule']['fixed_safety_factor']); width=float(t['selection_rule']['retry_width_Mpc'])
checks['factor_frozen']=f==0.5
checks['width_exact']=width==f*observed
checks['width_positive_finite']=math.isfinite(width) and width>0
checks['tolerance_unchanged']=t['retry_contract']['same_integrator_tolerance'] is True and t['retry_contract']['first_rhs_relative_tolerance']==5e-9
checks['one_step_not_weakened']=t['retry_contract']['exactly_one_accepted_step_required'] is True and t['retry_contract']['zero_rejected_trials_required'] is True and t['retry_contract']['expected_rhs_calls']==7
checks['s2_preserved_fail']=s['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'
passed=all(checks.values())
out={'schema':'RTK_C10_65S2J_PROSPECTIVE_RETRY_WIDTH_RESULT_v1','gate':'C10.65s2j','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'source_minimum_first_accepted_hdid_Mpc':observed,'fixed_safety_factor':f,'retry_width_Mpc':width,'original_s2_classification_preserved':s['classification'],'threshold_changed':False,'integrator_tolerance_changed':False,'interpretation':'Prospective implementation-scale selection only; original s2 remains failed and no retry has been executed.' if passed else 'Selection audit failed; do not execute retry.','next_gate':t['next_if_pass'] if passed else 'Repair selection bookkeeping only; do not alter s2 criteria.','non_claims':t['non_claims']}
(R/'research/theory_results/RTK_C10_65S2J_PROSPECTIVE_RETRY_WIDTH_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'])
raise SystemExit(0 if passed else 2)
