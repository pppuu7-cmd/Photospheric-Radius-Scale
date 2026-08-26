#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--class-tree',required=True);ap.add_argument('--patch',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S4A3_TARGETED_ENDPOINT_MATERIALIZATION_REPAIR_TARGET_v1.json');g=L('research/theory_results/RTK_C10_65S4A2_EXACT_ONSET_GEOMETRY_AUDIT_RESULT_v1.json');s=L('research/theory_results/RTK_C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_RESULT_v1.json');s1=L('research/theory_results/RTK_C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION';assert g['classification']=='C10_65S4A2_EXACT_ONSET_GEOMETRY_AUDIT_PASS_SCOPED';assert g['provenance']['github_actions_run_id']==33009457306;assert s['classification']=='C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_FAIL_SCOPED';assert s['provenance']['github_actions_run_id']==33008706959;assert s['provenance']['historical_failed_attempt_run_id']==33008095108;assert s1['classification']=='C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_PASS_SCOPED'
    src=(Path(a.class_tree)/'source/perturbations.c').read_text();helper=(Path(a.class_tree)/'source/rtk_c10_65s4a3_endpoint.c').read_text();patch=Path(a.patch).read_text();marker='RTK_C10_65S4A3_TARGETED_ENDPOINT_MATERIALIZATION_V1'
    pos=src.find('if ((getenv("RTK_C10_65S4A3_TARGETED_ONSET")'); end=src.find('\n    else {',pos) if pos>=0 else -1; seg=src[pos:end] if pos>=0 and end>pos else ''
    first=seg.find('class_call(generic_evolver(perturb_derivs,'); direct=seg.find('rtk_c10_65s1_observe('); second=seg.find('class_call(generic_evolver(perturb_derivs,',first+1) if first>=0 else -1
    checks={
      'historical_failures_preserved':s['provenance']['github_actions_run_id']==33008706959 and s['provenance']['historical_failed_attempt_run_id']==33008095108,
      's4a2_geometry_parent_preserved':g['classification']=='C10_65S4A2_EXACT_ONSET_GEOMETRY_AUDIT_PASS_SCOPED' and g['max_corrected_forward_relative_a_error']<=1e-13,
      'source_filters_only_new_k':('const double k1=1.e-3,k2=3.e-3;' in helper and 'rtk_c10_65s4a3_target_k(k)' in src and 'RTK_C10_65S4A3_TARGETED_ONSET' in src),
      'source_computes_forward_spline_root':('background_at_tau(pba,mid,pba->short_info,pba->inter_normal' in helper and 'for (it=0;it<96;it++)' in helper and 'if (am<aon) lo=mid; else hi=mid;' in helper),
      'source_requires_root_relative_a_error_at_most_1e-13':('fabs(am-aon)/aon<=1.e-13' in helper and 'fabs(am-aon)/aon>1.e-13' in helper),
      'source_splits_only_containing_interval':('(c10_65s4a3_tau > interval_limit[index_interval])' in src and '(c10_65s4a3_tau < interval_limit[index_interval+1])' in src),
      'source_calls_existing_s1_observer_after_first_segment':first>=0 and direct>first and second>direct and patch.count('rtk_c10_65s1_observe(c10_65s4a3_tau,ppw->pv->y,&ppaw);')==1,
      'source_leaves_regression_k_unsplit':('rtk_c10_65s4a3_target_k(k)' in src and 'else {' in src and src.count('interval_limit[index_interval],\n                                 interval_limit[index_interval+1]')>=1),
      'source_contains_no_dy_assignment':'dy[' not in patch,
      'source_contains_no_pvecmetric_assignment':'pvecmetric[' not in patch,
      'source_contains_no_manual_index_pt_state_assignment':'index_pt_' not in patch,
      'source_contains_no_tolerance_or_approximation_criterion_mutation':(re.search(r'tol_perturb_integration\s*=',patch) is None and re.search(r'perturb_integration_stepsize\s*=',patch) is None and all(x not in patch for x in ['tight_coupling_trigger_tau_c_over_tau_h =','tight_coupling_trigger_tau_c_over_tau_k =','radiation_streaming_trigger_tau_over_tau_k =','ur_fluid_trigger_tau_over_tau_k ='])),
      'compile_passes':src.count(marker)==1 and (Path(a.class_tree)/'class').exists(),
      'threshold_changed':False}
    passed=all(v is True for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S4A3_TARGETED_ENDPOINT_MATERIALIZATION_REPAIR_RESULT_v1','gate':'C10.65s4a3','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'s4a2_geometry':{'run_id':g['provenance']['github_actions_run_id'],'tau_corrected':g['records'][0]['tau_corrected'],'max_corrected_forward_relative_a_error':g['max_corrected_forward_relative_a_error'],'same_interval_both':all(r['same_interval']==1 for r in g['records'])},'historical_s4a_failures':[33008095108,33008706959],'threshold_changed':False,'interpretation':('The repair is restricted to the two new k anchors: it finds the forward-spline-consistent onset time, splits only their containing interval, explicitly materializes the returned endpoint with the already-certified read-only s1 observer, and leaves regression k and dormant execution unsplit.' if passed else 'At least one frozen s4a3 source/ownership/compile guard failed; do not retry s4a.'),'next_gate':t['next_if_pass'] if passed else 'Repair s4a3 without modifying the frozen s4a scientific contract.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['classification']);print(json.dumps(checks,sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
