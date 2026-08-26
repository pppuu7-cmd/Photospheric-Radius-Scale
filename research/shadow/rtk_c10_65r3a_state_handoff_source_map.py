#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',default='.')
    ap.add_argument('--class-root',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    rr=Path(a.repo_root); cr=Path(a.class_root)
    target=json.loads((rr/'research/theory_targets/RTK_C10_65R3A_STATE_HANDOFF_SOURCE_MAP_TARGET_v1.json').read_text())
    r2=json.loads((rr/'research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json').read_text())
    patch=(rr/'rtk/apply_rtk_class_patch.py').read_text()
    ps=(cr/'source/perturbations.c').read_text()
    rk=(cr/'tools/evolver_rkck.c').read_text()
    ndf=(cr/'tools/evolver_ndf15.c').read_text()

    checks={}
    checks['r2_parent_pass']=r2.get('classification')=='C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_PASS_SCOPED'
    checks['khronon_state_reuses_delta_cdm_slot']='ky.delta=y[ppw->pv->index_pt_delta_cdm]' in patch and 'ky.delta=y[pv->index_pt_delta_cdm]' in patch
    checks['khronon_state_reuses_theta_cdm_slot']='ky.theta=y[ppw->pv->index_pt_theta_cdm]' in patch and 'ky.theta=y[pv->index_pt_theta_cdm]' in patch
    checks['stress_tensor_reads_same_two_slots']='ky.delta=y[ppw->pv->index_pt_delta_cdm]; ky.theta=y[ppw->pv->index_pt_theta_cdm];' in patch
    checks['derivative_callback_writes_same_two_slots']='dy[pv->index_pt_delta_cdm]=kd.delta_prime; dy[pv->index_pt_theta_cdm]=kd.theta_prime;' in patch
    checks['newtonian_phi_prime_from_metric_continuity']='km.phi_prime=-metric_continuity/3.' in patch
    checks['newtonian_psi_from_metric_euler_over_k2']='km.psi=metric_euler/k2' in patch
    rk_owns=('int (*derivs)(double x' in rk and 'double * dy' in rk and '(*derivs)(x2' in rk)
    ndf_owns=('int (*derivs)(double x' in ndf and 'double * dy' in ndf)
    checks['integrator_derivative_callback_owns_dy']=rk_owns or ndf_owns
    checks['integrator_advances_y_in_place']=('generic_integrator(derivs' in rk and '\n\t\t\t\t  y,' in rk) or ('y,' in ndf and 'derivs' in ndf)
    pos_int=rk.find('generic_integrator(derivs')
    pos_out=rk.find('(*output)(x2')
    checks['accepted_step_output_occurs_after_integrator']=pos_int>=0 and pos_out>pos_int
    all_prod='\n'.join([patch,ps])
    checks['r3_production_write_absent_before_later_gate']='c10_65r3' not in all_prod

    state_map={
      'state_slots':{'delta':'index_pt_delta_cdm','theta':'index_pt_theta_cdm'},
      'stress_tensor_read_slots':['index_pt_delta_cdm','index_pt_theta_cdm'],
      'derivative_write_slots':['index_pt_delta_cdm','index_pt_theta_cdm'],
      'metric_mapping':{'phi_prime':'-metric_continuity/3','psi':'metric_euler/k2'},
      'integrator_evidence':{
        'rk_derivs_callback':rk_owns,
        'ndf_derivs_callback':ndf_owns,
        'rk_generic_integrator_in_place_y':checks['integrator_advances_y_in_place'],
        'rk_output_after_integrator':checks['accepted_step_output_occurs_after_integrator']
      },
      'source_files':['rtk/apply_rtk_class_patch.py','source/perturbations.c','tools/evolver_rkck.c','tools/evolver_ndf15.c']
    }
    frozen=target['frozen_checks']
    ok=all(checks.get(k) is v for k,v in frozen.items())
    out={
      'schema':'RTK_C10_65R3A_STATE_HANDOFF_SOURCE_MAP_RESULT_v1',
      'gate':'C10.65r3a',
      'classification':target['pass_classification'] if ok else target['fail_classification'],
      'target':'research/theory_targets/RTK_C10_65R3A_STATE_HANDOFF_SOURCE_MAP_TARGET_v1.json',
      'checks':checks,
      'state_map':state_map,
      'threshold_changed':False,
      'interpretation':target['interpretation_if_pass'] if ok else 'Source ownership map did not satisfy the frozen preflight contract; no production handoff is authorized.',
      'next':target['next_if_pass'] if ok else 'Diagnose the exact failed source-map assertion without adding state writes.',
      'non_claims':target['non_claims']
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'],json.dumps(checks,sort_keys=True))
    raise SystemExit(0 if ok else 1)

if __name__=='__main__': main()
