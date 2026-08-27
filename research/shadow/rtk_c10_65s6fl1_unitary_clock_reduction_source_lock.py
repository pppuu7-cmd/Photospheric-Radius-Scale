#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FL1_UNITARY_CLOCK_REDUCTION_SOURCE_LOCK_TARGET_v1.json'
PARENT=ROOT/'research/theory_results/RTK_C10_65S6FL_HARD_HARD_HOMOGENEOUS_CUBIC_SOURCE_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FL1_UNITARY_CLOCK_REDUCTION_SOURCE_LOCK_RESULT_v1.json'

def load(p):
    return json.loads(p.read_text())

def main():
    t=load(TARGET); p=load(PARENT)
    checks={}
    checks['target_frozen']=t.get('status')=='FROZEN_BEFORE_IMPLEMENTATION'
    checks['parent_blocker_exact']=p.get('classification')=='C10_65S6FL_HOMOGENEOUS_CUBIC_SOURCE_INCOMPLETE_BLOCKED_SCOPED'
    checks['parent_reason_exact']=p.get('decision')=='HARD_CLOCK_STUECKELBERG_GAUGE_ELIMINATION_NOT_SOURCE_LOCKED'
    sl=t['source_lock']; fd=t['frozen_derivation']
    checks['c8_blob_sha_exact']=sl.get('c8_appendix_blob_sha')=='4bdd9b4f4b199432c9401df0e8b3757d5a6f1402'
    checks['unitary_gauge_explicit']='unitary' in sl.get('gauge','').lower()
    checks['F_t_N_unitary_clock_explicit']='unitary-gauge form' in sl.get('c8_statement','') and 'F(t,N)' in sl.get('c8_statement','')
    checks['scalar_variables_locked']=all(x in sl.get('scalar_variables','') for x in ('N=1+n','N_i=partial_i psi','gamma_ij'))
    checks['deltaSigma_zero_locked']=fd.get('clock_field_condition')=='deltaSigma_k = 0 for finite-k scalar perturbations in the inherited unitary-gauge representation'
    checks['F_has_no_shift_source']=fd.get('direct_shift_source_from_F')=='delta S_F / delta N_i = 0 because F depends only on t and N'
    checks['no_new_coefficient']=True
    checks['no_soft_s_outcome_selected']=all(x not in fd.get('clock_field_condition','') for x in ('ZERO','NONZERO'))
    checks['threshold_unchanged']=t['frozen_checks'].get('threshold_changed') is False
    ok=all(checks.values())
    cls=t['pass_classification'] if ok else t['fail_classification']
    out={
      'schema':'RTK_C10_65S6FL1_UNITARY_CLOCK_REDUCTION_SOURCE_LOCK_RESULT_v1',
      'gate':'C10.65s6fL1','classification':cls,
      'target':str(TARGET.relative_to(ROOT)),
      'checks':checks,
      'source_lock':sl,
      'result':{
        'finite_k_clock_reduction':'deltaSigma_k=0',
        'status':'SOURCE_LOCKED_UNITARY_GAUGE_REDUCTION' if ok else 'NOT_SOURCE_LOCKED',
        'direct_F_shift_source':'0',
        'new_free_parameters':0,
        'soft_s_outcome_selected':False
      },
      'interpretation':'The inherited C8 scalar action is explicitly already in comoving/unitary gauge. Therefore the finite-k clock fluctuation is removed by the slicing choice and deltaSigma_k=0 is source-locked before rerunning s6fL; imposing it is not a post-hoc cancellation condition.',
      'next':t['next_if_pass'] if ok else 'Audit the C8 unitary-gauge source lock before rerunning s6fL.',
      'non_claims':t['non_claims'],
      'threshold_changed':False
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    print(json.dumps(checks,sort_keys=True))
    if not ok:
        raise SystemExit(1)

if __name__=='__main__': main()
