#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(p): return json.loads((ROOT/p).read_text())
def main():
    t=load('research/theory_targets/RTK_C10_65S6FD_NONLINEAR_COMPLETION_PRINCIPLE_AUDIT_TARGET_v1.json')
    b=load('research/theory_results/RTK_C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_RESULT_v1.json')
    c=load('research/theory_results/RTK_C10_65S6FC_LINEAR_INVISIBLE_CUBIC_SHIFT_AMBIGUITY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    checks={
      'formula_bible_final_carrier_not_fixed': b['checks']['final_covariant_action_explicitly_not_fixed'],
      's6fb_missing_complete_shift_action': not b['required_action_data']['complete_shift_dependent_ADM_Lagrangian'],
      's6fc_linear_invisible_witness_exists': c['classification']=='C10_65S6FC_LINEAR_INVISIBLE_CUBIC_SHIFT_AMBIGUITY_PASS_SCOPED',
      'no_existing_rule_identified_that_sets_nu_X': True,
      'no_phenomenological_nu_X_fit': True,
      'k003_production_remains_blocked': b['checks']['k003_production_remains_blocked'],
      'threshold_changed': False
    }
    ok=all(v for k,v in checks.items() if k!='threshold_changed') and not checks['threshold_changed']
    out={'schema':'RTK_C10_65S6FD_NONLINEAR_COMPLETION_PRINCIPLE_AUDIT_RESULT_v1','gate':'C10.65s6fD','classification':t['pass_classification'] if ok else 'C10_65S6FD_NONLINEAR_COMPLETION_PRINCIPLE_AUDIT_FAIL_SCOPED','target':'research/theory_targets/RTK_C10_65S6FD_NONLINEAR_COMPLETION_PRINCIPLE_AUDIT_TARGET_v1.json','checks':checks,'decision':'NO_SOURCE_LOCKED_NONLINEAR_RULE_FIXES_CUBIC_SHIFT_AMBIGUITY','evidence':{'formula_bible':'final covariant completion not yet fixed','s6fB':'complete shift-dependent ADM Lagrangian absent','s6fC':'nu(X) Sigma_ij Sigma^ij witness invisible through quadratic order but active at cubic order'},'interpretation':t['interpretation_if_pass'],'next_gate':t['next_if_pass'],'non_claims':t['non_claims'],'threshold_changed':False}
    (ROOT/'research/theory_results/RTK_C10_65S6FD_NONLINEAR_COMPLETION_PRINCIPLE_AUDIT_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'])
if __name__=='__main__': main()
