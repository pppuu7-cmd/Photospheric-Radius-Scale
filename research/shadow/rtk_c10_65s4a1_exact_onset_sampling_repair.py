#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--class-tree',required=True);ap.add_argument('--patch',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_TARGET_v1.json');p=L('research/theory_results/RTK_C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION';assert p['classification']=='C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_FAIL_SCOPED'
    false_checks=[k for k,v in p['checks'].items() if v is False and k!='threshold_changed']; parent_preserved=(false_checks==['all_exact_onset_rows_present'] and p['provenance']['github_actions_run_id']==33008095108)
    src=(Path(a.class_tree)/'source/perturbations.c').read_text();patch=Path(a.patch).read_text();m='RTK_C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_V1'
    checks={
      'parent_failure_preserved':parent_preserved,
      'source_has_runtime_observer_guard':'getenv("RTK_C10_65S4A1_EXACT_ONSET")' in src,
      'source_uses_background_tau_of_z':'background_tau_of_z(pba,1./c10_65s4a1_a_on-1.,&c10_65s4a1_tau_on)' in src,
      'source_splits_only_containing_interval':('(c10_65s4a1_tau_on > interval_limit[index_interval])' in src and '(c10_65s4a1_tau_on < interval_limit[index_interval+1])' in src),
      'source_reuses_same_generic_evolver_arguments':src.count('c10_65s4a1_tau_on')>=6 and src.count('generic_evolver(perturb_derivs,')>=4,
      'source_contains_no_dy_assignment':'dy[' not in patch,
      'source_contains_no_pvecmetric_assignment':'pvecmetric[' not in patch,
      'source_contains_no_manual_index_pt_state_assignment':'index_pt_' not in patch,
      'source_contains_no_tolerance_mutation':re.search(r'tol_perturb_integration\s*=',patch) is None,
      'source_contains_no_approximation_criterion_mutation':all(x not in patch for x in ['tight_coupling_trigger_tau_c_over_tau_h =','tight_coupling_trigger_tau_c_over_tau_k =','radiation_streaming_trigger_tau_over_tau_k =','ur_fluid_trigger_tau_over_tau_k =']),
      'marker_unique':src.count(m)==1,
      'threshold_changed':False
    }
    passed=all(v is True for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_RESULT_v1','gate':'C10.65s4a1','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'historical_s4a_failure':{'classification':p['classification'],'run_id':p['provenance']['github_actions_run_id'],'false_checks':false_checks},'threshold_changed':False,'interpretation':'The exact-onset repair changes observer sampling geometry only: under a dedicated runtime opt-in it splits the already-selected uniform-approximation generic_evolver interval at tau_on, with the same RHS, state vector, tolerances, timescale and approximation flags.' if passed else 'The proposed exact-onset sampling repair failed at least one frozen source/ownership guard.','next_gate':t['next_if_pass'] if passed else 'Repair C10.65s4a1 without changing the frozen s4a domain or scientific guards.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['classification']);print(json.dumps(checks,sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
