#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def load(p): return json.loads((ROOT/p).read_text())

def parse_observer(path):
    rows=[]
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',')
        if len(p)!=63: raise RuntimeError(f'observer columns {len(p)} != 63')
        rows.append({'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'rhs_calls':int(p[8])})
    return rows

def compatible_counts(nrhs):
    # Pinned path: A current-point derivatives, five derivative stages per RKCK trial,
    # plus one compulsory final derivative in evolver_rk. T>=A because every accepted
    # substep requires at least one RKCK trial.
    out=[]
    for A in range(1,nrhs+1):
        rem=nrhs-1-A
        if rem>=0 and rem%5==0:
            T=rem//5
            if T>=A: out.append((A,T,T-A))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--observer',required=True)
    ap.add_argument('--v3-patch',required=True)
    ap.add_argument('--old-analyzer',required=True)
    ap.add_argument('--evolver-source',required=True)
    ap.add_argument('--dei-source',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    target=load('research/theory_targets/RTK_C10_65S2H_PRODUCTION_CANARY_FAILURE_DIAGNOSIS_TARGET_v1.json')
    s2=load('research/theory_results/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_RESULT_v1.json')
    assert target['status']=='FROZEN_BEFORE_DIAGNOSIS_EXECUTION'
    assert s2['classification']==target['parent']['classification']
    assert s2['provenance']['github_actions_run_id']==target['parent']['github_actions_run_id']

    checks={}
    failed={k for k,v in s2['checks'].items() if not v}
    checks['original_failed_checks_exact']=failed==set(target['frozen_diagnosis_contract']['required_original_failed_checks_exactly'])
    checks['original_physics_checks_preserved']=all(s2['checks'].get(k) is True for k in target['frozen_diagnosis_contract']['required_original_physics_checks_true'])
    checks['original_s2_preserved_fail']=s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'
    checks['threshold_unchanged']=s2.get('threshold_changed') is False and s2.get('max_first_production_rhs_relative',1)>0 and s2['max_first_production_rhs_relative'] < 5e-9

    ev=Path(a.evolver_source).read_text(); dei=Path(a.dei_source).read_text()
    source_tokens=[
      'class_call(generic_integrator(derivs,',
      'a last call is compulsory',
      'class_call((*derivs)(x1,',
      'class_call((*derivs)(x,pgi->y,pgi->dydx',
      'class_call(rkqs(&x,',
      'for (;;) {',
      'class_call(rkck(*x,h,derivs',
      'class_call((*derivs)(x+_RKCK_a2_*h',
      'class_call((*derivs)(x+_RKCK_a3_*h',
      'class_call((*derivs)(x+_RKCK_a4_*h',
      'class_call((*derivs)(x+_RKCK_a5_*h',
      'class_call((*derivs)(x+_RKCK_a6_*h'
    ]
    checks['pinned_cash_karp_accounting_source_locked']=all(t in ev+dei for t in source_tokens)

    rows=parse_observer(a.observer)
    before=sorted((x for x in rows if x['phase']=='BEFORE'),key=lambda x:x['k'])
    after=sorted((x for x in rows if x['phase']=='AFTER'),key=lambda x:x['k'])
    checks['observer_shape']=len(before)==len(after)==4 and [x['k'] for x in before]==[x['k'] for x in after]
    diagnostics=[]; substantive=True
    if checks['observer_shape']:
        for br,ar in zip(before,after):
            poss=compatible_counts(ar['rhs_calls'])
            minA=min((x[0] for x in poss),default=0)
            maxA=max((x[0] for x in poss),default=0)
            substantive &= minA>1
            diagnostics.append({
              'k':ar['k'],'before_rhs_calls':br['rhs_calls'],'after_rhs_calls':ar['rhs_calls'],
              'minimum_accepted_substeps':minA,'maximum_accepted_substeps_compatible':maxA,
              'compatible_A_trials_rejections':[{'accepted':q[0],'trials':q[1],'rejected':q[2]} for q in poss]
            })
    else: substantive=False
    checks['multiple_accepted_substeps_proven']=substantive

    old=Path(a.old_analyzer).read_text(); v3=Path(a.v3_patch).read_text()
    literal="'no physics/criteria changes' in v2txt"
    checks['old_static_guard_literal_identified']=literal in old
    checks['v3_semantic_compile_only_statement']=('No physics or frozen criteria change.' in v3 and 'compile-only thermo/prototype fixes' in v3)
    checks['literal_phrase_absent_from_v3']='no physics/criteria changes' not in v3
    other_static=s2.get('static_guards',{}).copy(); other_static.pop('thermo_signature_fix_only',None)
    checks['all_other_static_guards_pass']=bool(other_static) and all(other_static.values())
    checks['static_guard_false_negative_is_text_only']=(checks['old_static_guard_literal_identified'] and checks['v3_semantic_compile_only_statement'] and checks['literal_phrase_absent_from_v3'] and checks['all_other_static_guards_pass'] and s2['checks']['off_identity'] and s2['checks']['first_production_rhs'])

    passed=all(checks.values())
    out={
      'schema':'RTK_C10_65S2H_PRODUCTION_CANARY_FAILURE_DIAGNOSIS_RESULT_v1',
      'gate':'C10.65s2h',
      'classification':target['pass_classification'] if passed else target['fail_classification'],
      'checks':checks,
      'original_s2_classification_preserved':s2['classification'],
      'original_s2_failed_checks':sorted(failed),
      'adaptive_step_diagnostics':diagnostics,
      'cash_karp_accounting':'N_RHS = N_accepted + 5*N_RKCK_trials + 1, N_RKCK_trials >= N_accepted. The observed counts therefore lower-bound accepted substeps without assuming how many trials were rejected.',
      'static_guard_diagnosis':{'original_value':s2.get('static_guards',{}).get('thermo_signature_fix_only'),'diagnosis':'ANALYZER_LITERAL_NEEDLE_FALSE_NEGATIVE' if checks['static_guard_false_negative_is_text_only'] else 'UNRESOLVED'},
      'scientific_decision':'Keep C10.65s2 FAIL_SCOPED because the exactly-one-accepted-step condition genuinely failed. Do not treat the thermo static text mismatch as physics. Instrument adaptive accepted/rejected steps at the same frozen 1e-4 interval before prospectively choosing any retry width.' if passed else 'Diagnosis incomplete; do not modify C10.65s2 or select a retry width.',
      'next_gate':target['next_if_pass'] if passed else 'Repair only the diagnosis instrumentation and rerun C10.65s2h; do not alter C10.65s2 criteria.',
      'threshold_changed':False,
      's2_reclassified':False,
      'retry_width_selected':False,
      'non_claims':target['non_claims']
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'])
    print(json.dumps({'checks':checks,'diagnostics':diagnostics},sort_keys=True))
    return 0 if passed else 2

if __name__=='__main__': raise SystemExit(main())
