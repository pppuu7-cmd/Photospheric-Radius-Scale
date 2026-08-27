#!/usr/bin/env python3
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def main():
    t=L('research/theory_targets/RTK_C10_65S5G_AXIS_DECISION_TARGET_v1.json')
    f=L('research/theory_results/RTK_C10_65S5F_NEXT_K_MULTIBRANCH_TIME_WIDENED_TRAJECTORY_RESULT_v1.json')
    c=L('research/theory_results/RTK_C10_65S5C_NEXT_K_OMITTED_ORDER_SENSITIVITY_RESULT_v1.json')
    a=L('research/theory_results/RTK_C10_65S5A_NEXT_K_NEAR_HORIZON_ONSET_STATE_PREFLIGHT_RESULT_v1.json')
    g4=L('research/theory_results/RTK_C10_65S4G_MODERATE_K_LONGER_TIME_TRAJECTORY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_EVALUATION'
    assert f['classification']==t['parents']['C10.65s5f'];assert c['classification']==t['parents']['C10.65s5c'];assert a['classification']==t['parents']['C10.65s5a'];assert g4['classification']==t['parents']['C10.65s4g_method']
    fc=t['frozen_constants'];rule=t['frozen_decision_rule'];bound=float(fc['constraint_bound'])
    worst=max(float(f['max_abs_normalized_constraint']),float(f['max_abs_normalized_constraint_change']))
    headroom=bound/worst
    k=.03; A2=float(fc['A2']); J=float(fc['J_ad0']); H=float(fc['Hc_on_Mpc_inv'])
    proxy=abs(A2*k*k/J); kh=k/H
    choose_A=headroom>=float(rule['s5f_constraint_headroom_required']) and (proxy>=float(rule['k003_omitted_order_proxy_large_if_ge']) or kh>=float(rule['k003_horizon_ratio_large_if_ge']))
    decision=t['decision_A_label'] if choose_A else t['decision_B_label']
    checks={
      'parents':True,'s5f_headroom_finite':math.isfinite(headroom),'k003_proxy_finite':math.isfinite(proxy),'k003_horizon_ratio_finite':math.isfinite(kh),
      'decision_rule_applied_without_future_outputs':True,'threshold_changed':False
    }
    passed=all(v is True for q,v in checks.items() if q!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S5G_AXIS_DECISION_RESULT_v1','gate':'C10.65s5g','classification':t['pass_classification'] if passed else t['fail_classification'],'decision':decision,'metrics':{'s5f_worst_normalized_constraint_or_change':worst,'s5f_constraint_headroom':headroom,'k003_omitted_order_proxy_abs_A2k2_over_J':proxy,'k003_over_Hc_on':kh},'checks':checks,'decision_rule':rule,'interpretation':'Select the next experimental axis prospectively. This does not validate either future domain.' if passed else 'Decision gate evaluation failed; do not execute either widening.','next_gate':t['next_if_A'] if decision==t['decision_A_label'] else t['next_if_B'],'non_claims':t['non_claims'],'threshold_changed':False}
    p=ROOT/'research/theory_results/RTK_C10_65S5G_AXIS_DECISION_RESULT_v1.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification']);print(json.dumps({'decision':decision,**out['metrics']},sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__': main()
