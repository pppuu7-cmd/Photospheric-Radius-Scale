#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def load(p): return json.loads((ROOT/p).read_text())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-tree',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=load('research/theory_targets/RTK_C10_65S0_INTEGRATION_SAFE_HANDOFF_ARCHITECTURE_TARGET_v1.json')
    r2=load('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert r2['classification']=='C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_PASS_SCOPED'
    root=Path(a.class_tree); pt=(root/'source/perturbations.c').read_text()
    checks={}
    checks['piecewise_interval_loop']='for (index_interval=0; index_interval<interval_number; index_interval++)' in pt
    checks['vector_init_present']='perturb_vector_init(ppr,' in pt
    checks['vector_init_before_evolver']=pt.find('perturb_vector_init(ppr,') < pt.find('generic_evolver(perturb_derivs')
    checks['first_interval_null_previous']='if (index_interval==0)' in pt and 'previous_approx=NULL;' in pt
    checks['later_interval_previous_approx']='previous_approx=interval_approx[index_interval-1];' in pt
    checks['approx_switches_define_interval_limits']='perturb_find_approximation_switches' in pt and 'interval_limit' in pt
    checks['metric_constraints_declared_nonintegrated']='indices of metric perturbations obeying to constraint' in pt and 'vector of quantities to\n      be integrated' in pt
    checks['model2_carrier_delta']='dy[pv->index_pt_delta_cdm]=kd.delta_prime;' in pt
    checks['model2_carrier_theta']='dy[pv->index_pt_theta_cdm]=kd.theta_prime;' in pt
    checks['model2_sources_read_same_carrier']='ky.delta=y[ppw->pv->index_pt_delta_cdm]; ky.theta=y[ppw->pv->index_pt_theta_cdm];' in pt
    checks['ordinary_rhs_exists']='int perturb_derivs(' in pt
    # Architecture conclusion: arbitrary a_on is not an existing switch by construction;
    # therefore a deterministic extra interval boundary is required before any handoff.
    checks['explicit_split_required_by_ownership']=checks['piecewise_interval_loop'] and checks['vector_init_before_evolver'] and checks['approx_switches_define_interval_limits']
    required=list(checks.values())
    ok=all(required)
    cls=t['pass_classification'] if ok else t['fail_classification']
    out={
      'schema':'RTK_C10_65S0_INTEGRATION_SAFE_HANDOFF_ARCHITECTURE_RESULT_v1',
      'gate':'C10.65s0','classification':cls,
      'target':'research/theory_targets/RTK_C10_65S0_INTEGRATION_SAFE_HANDOFF_ARCHITECTURE_TARGET_v1.json',
      'checks':checks,
      'architecture_decision':{
        'safe_handoff_site':'perturb_solve interval boundary, after perturb_vector_init and before generic_evolver',
        'arbitrary_a_on_policy':'split the containing interval at deterministic tau_on; do not alter approximation criteria',
        'allowed_integrated_writes':['pv->y[index_pt_delta_cdm]','pv->y[index_pt_theta_cdm]'],
        'forbidden_writes':['metric constraints','shift/projector algebraic quantities','TCA/collision coefficients','approximation flags','production metric source variables','state mutation inside perturb_derivs'],
        'reason':'The evolver owns pv->y inside each interval; vector allocation/redistribution is centralized at interval entry. A handoff performed there is deterministic and outside adaptive RHS callbacks.'
      },
      'threshold_changed':False,
      'next':t['next_if_pass'] if ok else t['next_if_fail'],
      'non_claims':t['non_claims']
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps(checks,sort_keys=True))
    raise SystemExit(0 if ok else 1)
if __name__=='__main__': main()
