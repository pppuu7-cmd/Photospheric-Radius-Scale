#!/usr/bin/env python3
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def main():
 t=L('research/theory_targets/RTK_C10_65S6D_K003_PRODUCTION_ARCHITECTURE_DECISION_TARGET_v1.json')
 s=L('research/theory_results/RTK_C10_65S6C_K003_OMITTED_ORDER_SENSITIVITY_RESULT_v1.json')
 assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
 assert s['classification']==t['parents']['C10.65s6c']
 assert t['threshold_changed'] is False
 keys=t['decision_inputs']['key_metric_carrier_responses']; boundary=float(t['decision_inputs']['order_unity_boundary_relative']); r=s['response_map_measurement_only']
 vals={k:float(r[k]['max_relative']) for k in keys}; finite=all(math.isfinite(v) for v in vals.values()); maximum=max(vals.values()); exceeding={k:v for k,v in vals.items() if v>=boundary}
 decision=t['decision_if_any_key_ge_1'] if exceeding else t['decision_if_all_key_lt_1']
 checks={'s6c_parent_pass':True,'all_key_responses_present_and_finite':finite,'decision_uses_no_production_output':True,'threshold_changed':False}
 passed=checks['threshold_changed'] is False and all(v for k,v in checks.items() if k!='threshold_changed')
 out={'schema':'RTK_C10_65S6D_K003_PRODUCTION_ARCHITECTURE_DECISION_RESULT_v1','gate':'C10.65s6d','classification':t['pass_classification'] if passed else t['fail_classification'],'target':'research/theory_targets/RTK_C10_65S6D_K003_PRODUCTION_ARCHITECTURE_DECISION_TARGET_v1.json','checks':checks,'decision':decision,'order_unity_boundary_relative':boundary,'key_response_maxima':vals,'key_responses_at_or_above_order_unity':exceeding,'max_key_response_relative':maximum,'production_k003_allowed':decision==t['decision_if_all_key_lt_1'],'interpretation':t['interpretation_if_pass'] if passed else 'Decision gate failed internal provenance/finite checks; do not execute k=0.03 production.','next_gate':'Return to the pre-EFT/UV matching interface and strengthen or derive the omitted higher-order matching input before any k=0.03 production canary.' if decision==t['decision_if_any_key_ge_1'] else 'Freeze a bounded multibranch k=0.03 production canary before execution.','non_claims':t['non_claims'],'threshold_changed':False}
 (ROOT/'research/theory_results/RTK_C10_65S6D_K003_PRODUCTION_ARCHITECTURE_DECISION_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n')
 print(out['classification']);print(json.dumps({'decision':decision,'max_key_response_relative':maximum,'exceeding':exceeding},sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
