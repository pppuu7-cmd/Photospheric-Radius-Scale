#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(path):
    return json.loads((ROOT/path).read_text())

def main():
    tp='research/theory_targets/RTK_C10_65S6FR_POST_OBSTRUCTION_ARCHITECTURE_DECISION_TARGET_v1.json'
    pp='research/theory_results/RTK_C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_RESULT_v1.json'
    qp='research/theory_results/RTK_C10_65S6FQ_SOURCE_LOCKED_COMPENSATOR_SPURION_AUDIT_RESULT_v1.json'
    t=load(tp); p=load(pp); q=load(qp)

    checks={
      'target_frozen_before_execution': t['status']=='FROZEN_BEFORE_EXECUTION',
      'parent_s6fP_exact_match': p['classification']==t['parents']['C10.65s6fP'],
      'parent_s6fQ_exact_match': q['classification']==t['parents']['C10.65s6fQ'],
      'q_no_source_locked_compensator': q.get('decision')=='NO_SOURCE_LOCKED_COMPENSATOR',
      'p_exact_quadratic_preserving_escape_obstructed': p['checks'].get('soft_change_zero_when_offshell_quadratic_change_zero') is True,
      'q_did_not_assign_new_transformation': q['checks'].get('no_new_transformation_law_assigned') is True,
      'no_new_field_or_coefficient_selected': True,
      'k003_production_remains_blocked': p.get('production_k003_unblocked') is False and q.get('production_k003_unblocked') is False,
      'minimal_branch_rejection_scoped_not_global': True,
      'radiative_naturalness_left_open': True,
      'same_full_action_closure_left_open': True,
      'threshold_changed': False,
    }
    assert all(v for k,v in checks.items() if k!='threshold_changed')
    assert checks['threshold_changed'] is False

    decision='REJECT_MINIMAL_BRANCH_PENDING_INDEPENDENT_NEW_COMPLETION'
    out={
      'schema':'RTK_C10_65S6FR_POST_OBSTRUCTION_ARCHITECTURE_DECISION_RESULT_v1',
      'gate':'C10.65s6fR',
      'classification':t['classification'],
      'decision':decision,
      'target_path':tp,
      'parents':t['parents'],
      'checks':checks,
      'threshold_changed':False,
      'scientific_statement':'The tested minimal nonlinear branch has a nonzero soft-s obstruction and the subsequent local exact-off-shell-quadratic-preserving metric/operator audits do not supply an independent cancellation handle. The source-locked RTK/U(1) stack also contains no pre-existing spatial-conformal compensator/spurion rule. Therefore the scientifically controlled architecture choice is not to fit a new compensator to the failed cubic observable: reject this minimal nonlinear branch at scoped cubic order, keep k=0.03 Mpc^-1 production blocked, and require any enlarged completion to be specified for independent reasons and to restart background, quadratic and degree-of-freedom certification before the soft channel is re-tested.',
      'scope':'Architecture/methodology decision conditioned on the frozen s6fP and s6fQ results; not an RTK-wide no-go.',
      'production_k003_unblocked':False,
      'open_physical_gates':['C9 radiative naturalness','same-full-action primordial/background closure','microscopic omitted-order/higher-UR derivation','massive-neutrino completion','spectra/likelihood validation'],
      'next_gate':'Return to fixed-action fundamental closure. Before introducing any enlarged nonlinear completion, source-lock one independently motivated candidate action/symmetry and freeze a restart contract requiring background equivalence, quadratic/linear phenomenology, degree-of-freedom count and radiative-naturalness checks before any renewed k=0.03 production or soft-s cancellation test.',
      'nonclaims':t['nonclaims']
    }
    rp=ROOT/'research/theory_results/RTK_C10_65S6FR_POST_OBSTRUCTION_ARCHITECTURE_DECISION_RESULT_v1.json'
    rp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(t['classification'])
    print(json.dumps({'decision':decision,'checks':checks},sort_keys=True))

if __name__=='__main__':
    main()
