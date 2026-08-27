#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
target=json.loads((ROOT/'research/theory_targets/RTK_C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_TARGET_v1.json').read_text())
parents={
 'C10.65s6fB':json.loads((ROOT/'research/theory_results/RTK_C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_RESULT_v1.json').read_text()),
 'C10.65s6fC':json.loads((ROOT/'research/theory_results/RTK_C10_65S6FC_LINEAR_INVISIBLE_CUBIC_SHIFT_AMBIGUITY_RESULT_v1.json').read_text()),
 'C10.65s6fD':json.loads((ROOT/'research/theory_results/RTK_C10_65S6FD_NONLINEAR_COMPLETION_PRINCIPLE_AUDIT_RESULT_v1.json').read_text()),
}
for k,v in parents.items():
    assert v['classification']==target['parents'][k], (k,v['classification'],target['parents'][k])
assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
b=target['candidate_branch']
checks={}
checks['branch_explicitly_labeled_hypothesis']=b['hypothesis_label']=='NEW_NONLINEAR_COMPLETION_HYPOTHESIS'
checks['projectable_lapse_fixed']=b['projectability']=='N=N(t)'
checks['kinetic_sector_explicit']='K_ij K^ij - lambda_HL K^2' in b['gravitational_kinetic_sector']
checks['n2_carrier_explicit']=b['n2_carrier']=='alpha6(X) D_i R3 D^i R3'
checks['alpha6_rule_exact']=b['alpha6_rule']=='alpha6(X)=alpha6_0*(X/X0)^(1/2)'
# The logarithmic derivative d ln(alpha6)/d ln X is exactly 1/2 for this frozen rule.
checks['alpha6_log_slope_exact']=b['alpha6_log_slope_s1']=='1/2'
checks['nu_rule_fixed_before_reduction']=b['nu_Sigma2_rule']=='nu(X) identically zero by candidate-branch definition'
checks['nu_X_not_fitted']=target['frozen_checks']['nu_X_not_fitted_to_soft_s_output'] is True
checks['mixed_shift_operator_basis_explicitly_closed']=b['mixed_K_R_and_DK_operators']=='absent by candidate-branch definition' and b['extra_shift_dependent_operator_basis']==[]
checks['s6e_bare_vertex_not_used_to_choose_branch']=parents['C10.65s6fD']['decision']=='NO_SOURCE_LOCKED_NONLINEAR_RULE_FIXES_CUBIC_SHIFT_AMBIGUITY'
checks['k003_production_remains_blocked']=target['frozen_checks']['k003_production_remains_blocked'] is True
checks['threshold_changed']=False
ok=all(v for k,v in checks.items() if k!='threshold_changed')
classification=target['pass_classification'] if ok else 'C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_CONTRACT_FAIL_SCOPED'
result={
 'schema':'RTK_C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_RESULT_v1',
 'gate':'C10.65s6fE',
 'classification':classification,
 'candidate_branch':b,
 'checks':checks,
 'decision':'CANDIDATE_BRANCH_FROZEN_FOR_CONDITIONAL_CUBIC_REDUCTION' if ok else 'CANDIDATE_BRANCH_CONTRACT_INVALID',
 'interpretation':target['interpretation_if_pass'] if ok else 'The candidate branch contract did not satisfy its frozen source-lock/completeness checks.',
 'next_gate':target['next_if_pass'] if ok else 'Diagnose contract failure without weakening frozen checks.',
 'non_claims':target['non_claims'],
 'threshold_changed':False
}
out=ROOT/'research/theory_results/RTK_C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_RESULT_v1.json'
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(classification, json.dumps({'checks':checks},sort_keys=True))
raise SystemExit(0 if ok else 1)
