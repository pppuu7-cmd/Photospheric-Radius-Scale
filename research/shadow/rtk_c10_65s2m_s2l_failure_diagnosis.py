#!/usr/bin/env python3
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
L=lambda p:json.loads((R/p).read_text())
t=L('research/theory_targets/RTK_C10_65S2M_S2L_FAILURE_DIAGNOSIS_TARGET_v1.json'); l=L('research/theory_results/RTK_C10_65S2L_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_RESULT_v1.json'); a=L('research/theory_results/RTK_C10_65S3A_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_RESULT_v1.json'); src=(R/'research/shadow/rtk_c10_65s2l_finite_short_interval_endpoint_stability_analyzer.py').read_text(); trg=L('research/theory_targets/RTK_C10_65S2L_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_TARGET_v1.json')
assert t['status']=='FROZEN_BEFORE_DIAGNOSIS_EXECUTION'
width=float(l['finite_short_interval_Mpc']); atol=float(trg['frozen_checks']['terminal_interval_absolute_tolerance_Mpc']); stats=l['adaptive_trace']; accepted=[int(q['accepted_substeps']) for q in stats.values()]; diffs={k:abs(float(q['sum_hdid'])-width) for k,q in stats.items()}
checks={
's2l_preserved_fail':l['classification']=='C10_65S2L_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_FAIL_SCOPED',
's3a_preserved_pass':a['classification']=='C10_65S3A_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_PASS_SCOPED',
's2l_failed_sampling_density':l['checks']['adaptive_trace_minimum_steps'] is False and min(accepted)<int(trg['execution']['minimum_accepted_substeps_per_anchor']),
'all_s2l_trace_sum_hdid_within_original_terminal_interval_tolerance':all(v<=atol for v in diffs.values()),
'trace_interval_false_due_to_traceok_boolean_coupling':l['checks']['trace_interval_consistency'] is False and "checks['trace_interval_consistency']=traceok and all(" in src,
's2l_terminal_constraints_passed_original_bound':l['checks']['terminal_constraints'] is True and all(abs(float(v))<=float(l['prospective_terminal_constraint_bound']) for q in l['terminal_constraints'].values() for v in q.values()),
's2l_terminal_state_and_approximation_passed':l['checks']['terminal_finite'] is True and l['checks']['terminal_approximation_state'] is True,
'no_threshold_or_classification_change':l['threshold_changed'] is False and a['threshold_changed'] is False
}
passed=all(checks.values())
out={'schema':'RTK_C10_65S2M_S2L_FAILURE_DIAGNOSIS_RESULT_v1','gate':'C10.65s2m','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'s2l_classification_preserved':l['classification'],'s3a_classification_preserved':a['classification'],'accepted_substeps_per_anchor':accepted,'trace_interval_absolute_errors_Mpc':diffs,'original_interval_absolute_tolerance_Mpc':atol,'diagnosis':'S2L genuine frozen failure is sampling-density only (4/4/4/5 accepted versus required >=10); trace_interval_consistency false is secondary analyzer boolean coupling because each summed hdid satisfies the original interval tolerance. Terminal state/approximation/constraints passed. Independent longer and stricter s3a provides the valid endpoint-stability parent.' if passed else 'Diagnosis incomplete; preserve s2l fail and do not reinterpret it.','threshold_changed':False,'s2l_reclassified':False,'next_gate':t['next_if_pass'] if passed else 'Repair diagnosis only.','non_claims':t['non_claims']}
(R/'research/theory_results/RTK_C10_65S2M_S2L_FAILURE_DIAGNOSIS_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['classification']);print(json.dumps(checks,sort_keys=True));raise SystemExit(0 if passed else 2)
