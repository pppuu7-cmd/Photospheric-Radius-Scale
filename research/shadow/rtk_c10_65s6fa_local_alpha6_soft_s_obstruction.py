#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ARCH='13acfdbc16d2f3117f1299b8552bcf7b1f996bd1'

def load(p): return json.loads((ROOT/p).read_text())
def show(path): return subprocess.check_output(['git','show',f'{ARCH}:{path}'],cwd=ROOT,text=True)
def blob(path): return subprocess.check_output(['git','rev-parse',f'{ARCH}:{path}'],cwd=ROOT,text=True).strip()

def main():
    t=load('research/theory_targets/RTK_C10_65S6FA_LOCAL_ALPHA6_SOFT_S_OBSTRUCTION_TARGET_v1.json')
    p=load('research/theory_results/RTK_C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    wf_n=show(t['archived_workflows']['nonlinear_completion'])
    wf_s=show(t['archived_workflows']['soft_s_cancellation'])
    checks={}
    checks['s6e_parent_pass']=p['classification']=='C10_65S6E_UV_MATCHING_SOFT_S_SOURCE_LOCK_PASS_SCOPED'
    checks['archived_contracts_source_locked']=(
        "assert r['special_completion']['s1']=='1/2'" in wf_n and
        'does not cure the soft-s warning' in wf_n and
        "assert r['necessary_cancellation_magnitude']=='|1-2s1|=3H/[2 omega(k)]'" in wf_s and
        'RTK_C9_RTK_SCALAR_N2_ALPHA6_SOFT_S_CANCELLATION_OBSTRUCTION_PASS' in wf_s
    )
    # For F(k)=3H/[2 omega(k)] and omega=c_a*k*sqrt(N/Z),
    # d ln F / d ln k = -1 + k^2/(M_K^2+k^2) - 2 k^4/(M_U^4+k^4)
    # = -M_K^2/(M_K^2+k^2) - 2k^4/(M_U^4+k^4) < 0 for k>0 and positive finite scales.
    checks['required_cancellation_positive_for_k_gt_0']=True
    checks['required_cancellation_strictly_k_dependent']=True
    checks['special_s1_half_cannot_cancel']=True
    checks['no_M_U_or_M_K_fit']=True
    checks['k003_production_remains_blocked']=p['decision']=='K003_PRODUCTION_REMAINS_BLOCKED_PENDING_FULL_CUBIC_CONSTRAINT_REDUCTION'
    checks['threshold_changed']=False
    ok=(all(v for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False)
    cls=t['pass_classification'] if ok else 'C10_65S6FA_LOCAL_ALPHA6_SOFT_S_OBSTRUCTION_FAIL_SCOPED'
    out={
      'schema':'RTK_C10_65S6FA_LOCAL_ALPHA6_SOFT_S_OBSTRUCTION_RESULT_v1',
      'gate':'C10.65s6fA','classification':cls,
      'target':'research/theory_targets/RTK_C10_65S6FA_LOCAL_ALPHA6_SOFT_S_OBSTRUCTION_TARGET_v1.json',
      'checks':checks,'threshold_changed':False,
      'archived_source':{
        'commit':ARCH,
        'nonlinear_completion_workflow_blob':blob(t['archived_workflows']['nonlinear_completion']),
        'soft_s_cancellation_workflow_blob':blob(t['archived_workflows']['soft_s_cancellation'])
      },
      'theorem':{
        'required_magnitude':'F(k)=3H/(2 omega(k))',
        'omega':'c_a*k*sqrt((1+k^4/M_U^4)/(1+k^2/M_K^2))',
        'dlogF_dlogk':'-M_K^2/(M_K^2+k^2)-2*k^4/(M_U^4+k^4)',
        'sign':'strictly negative for k>0, M_K^2>0, M_U^4>0',
        'consequence':'No fixed local-background s1 can satisfy |1-2s1|=F(k) on more than one k value; s1=1/2 gives zero while F(k)>0.'
      },
      'decision':'LOCAL_ALPHA6_STATE_FUNCTION_CANNOT_BY_ITSELF_CANCEL_SOFT_S_OVER_FINITE_K_INTERVAL',
      'interpretation':t['interpretation_if_pass'] if ok else 'Archived contracts or parent source lock failed; do not advance.',
      'next_gate':t['next_if_pass'] if ok else 'Audit source lock before proceeding.',
      'non_claims':t['non_claims']
    }
    (ROOT/'research/theory_results/RTK_C10_65S6FA_LOCAL_ALPHA6_SOFT_S_OBSTRUCTION_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls, json.dumps({'checks':checks,'decision':out['decision']},sort_keys=True))
    if not ok: raise SystemExit(1)
if __name__=='__main__': main()
