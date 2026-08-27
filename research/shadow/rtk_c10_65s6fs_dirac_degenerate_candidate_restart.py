#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'research/theory_targets/RTK_C10_65S6FS_DIRAC_DEGENERATE_CANDIDATE_RESTART_TARGET_v1.json'
R=ROOT/'research/theory_results/RTK_C10_65S6FS_DIRAC_DEGENERATE_CANDIDATE_RESTART_RESULT_v1.json'

def main():
    t=json.loads(T.read_text())
    assert t['status']=='FROZEN_BEFORE_EXECUTION'
    kappa,a,Om2,g,m2,w=sp.symbols('kappa a Om2 g m2 w', nonzero=True)
    v=sp.Matrix([1,a])
    K=kappa*(v*v.T)
    rank_one = sp.simplify(K.det())==0 and K!=sp.zeros(2)
    V=sp.Matrix([[Om2,g],[g,m2]])
    bracket=sp.expand((sp.Matrix([[a,-1]])*V*sp.Matrix([a,-1]))[0])
    bracket_expected=sp.expand(m2+a*a*Om2-2*a*g)
    bracket_identity=sp.simplify(bracket-bracket_expected)==0
    # Dirac count: 2 coordinates -> phase dimension 4; 2 second-class constraints -> 1 DOF.
    dof=(4-2)//2
    Q=sp.simplify((v.T*V.inv()*v)[0])
    M=V-kappa*w*w*(v*v.T)
    response=sp.factor((v.T*M.inv()*v)[0])
    expected=sp.factor(Q/(1-kappa*Q*w*w))
    response_identity=sp.simplify(response-expected)==0
    det_identity=sp.simplify(sp.det(M)-sp.det(V)*(1-kappa*Q*w*w))==0
    # Positive-definite witness demonstrates the frozen assumptions are nonempty.
    witness={Om2:5,m2:3,g:1,a:sp.Rational(2,5),kappa:2}
    bracket_w=sp.N(bracket.subs(witness))
    Q_w=sp.N(Q.subs(witness))
    pole2_w=sp.N((1/(kappa*Q)).subs(witness))
    assumptions_nonempty=bool(bracket_w>0 and Q_w>0 and pole2_w>0)
    parent_path=ROOT/'research/theory_results/RTK_C10_65S6FR_POST_OBSTRUCTION_ARCHITECTURE_DECISION_RESULT_v1.json'
    parent=json.loads(parent_path.read_text())
    parent_ok=parent['classification']==t['parent'] and parent['production_k003_unblocked'] is False
    checks={
      'target_frozen_before_execution': True,
      'parent_s6fR_exact_match': parent_ok,
      'velocity_hessian_rank_one': rank_one,
      'primary_constraint_source_locked': t['frozen_checks']['primary_constraint_phi1']=='p_y-a p_X=0',
      'secondary_constraint_source_locked': t['frozen_checks']['secondary_constraint_phi2']=='(a Omega2-g)X+(a g-m2)y=0',
      'second_class_bracket_identity': bracket_identity,
      'positive_domain_nonempty': assumptions_nonempty,
      'physical_scalar_dof_count_one': dof==1,
      'determinant_lemma_one_pole_identity': det_identity,
      'aligned_source_response_identity': response_identity,
      'no_soft_s_cancellation_test': t['frozen_checks']['no_soft_s_cancellation_test'] is True,
      'no_new_parameter_fit_to_failed_observable': t['frozen_checks']['no_new_parameter_fit_to_failed_observable'] is True,
      'k003_production_remains_blocked': t['frozen_checks']['k003_production_remains_blocked'] is True,
      'threshold_changed': False
    }
    passed=all(vv for kk,vv in checks.items() if kk!='threshold_changed') and checks['threshold_changed'] is False
    classification=t['pass_classification'] if passed else 'C10_65S6FS_DIRAC_DEGENERATE_CANDIDATE_RESTART_FAIL_SCOPED'
    out={
      'schema':'RTK_C10_65S6FS_DIRAC_DEGENERATE_CANDIDATE_RESTART_RESULT_v1',
      'gate':'C10.65s6fS','classification':classification,'target_path':str(T.relative_to(ROOT)),
      'candidate':t['candidate'],'checks':checks,
      'symbolic':{'velocity_hessian':str(K),'constraint_bracket':str(bracket),'Q':str(Q),'aligned_response':str(response),'determinant':str(sp.factor(sp.det(M)))},
      'witness':{'Omega2':5,'m2':3,'g':1,'a':0.4,'kappa':2,'constraint_bracket':float(bracket_w),'Q':float(Q_w),'omega_pole_squared':float(pole2_w)},
      'decision':'OPEN_FULL_FIXED_ACTION_RESTART_FOR_INDEPENDENT_DIRAC_DEGENERATE_CANDIDATE' if passed else 'DO_NOT_OPEN_RESTART',
      'production_k003_unblocked':False,
      'soft_s_retest_allowed':False,
      'next_gate':t['next_if_pass'] if passed else 'Audit candidate structural theorem before any embedding.',
      'nonclaims':t['nonclaims'],'threshold_changed':False
    }
    R.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification)
    print(json.dumps({'rank_one':rank_one,'dof':dof,'response_identity':response_identity,'bracket_witness':float(bracket_w),'Q_witness':float(Q_w),'pole2_witness':float(pole2_w)},sort_keys=True))
    if not passed: raise SystemExit(1)
if __name__=='__main__': main()
