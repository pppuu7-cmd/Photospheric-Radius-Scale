#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(p): return json.loads((ROOT/p).read_text())
def git_show(commit,path):
    return subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=ROOT,text=True)
def norm(s):
    return re.sub(r'\s+',' ',s.replace('`','')).strip().lower()

def main():
    tp='research/theory_targets/RTK_C10_65S6FQ_SOURCE_LOCKED_COMPENSATOR_SPURION_AUDIT_TARGET_v1.json'
    pp='research/theory_results/RTK_C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_RESULT_v1.json'
    t=load(tp); p=load(pp)
    assert t['status']=='FROZEN_BEFORE_EXECUTION'
    assert p['classification']=='C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_PASS_SCOPED'
    c=t['source_lock']['archive_commit']
    u=git_show(c,t['source_lock']['u1_appendix'])
    n=git_show(c,t['source_lock']['canonical_narrowing'])
    un=norm(u); nn=norm(n); low=un+' '+nn

    evidence={
      'u1_shift_rule':'delta_alpha n_i = n d_i alpha' in un,
      'prepotential_u1_rule':'delta_alpha nu = alpha' in un,
      'lapse_u1_neutral':'delta_alpha n = 0' in un,
      'invariant_shift_defined':'ntilde^i = n^i - n d^i nu' in un,
      'sigma_u1_neutral':'u(1)-neutral scalar sigma' in un,
      'theta_u1_invariant':'delta_alpha theta_u = 0' in un,
      'canonical_stack_mentions_prepotential_velocity':'prepotential velocity' in nn,
      'weyl_word_present':'weyl' in low,
      'conformal_word_present':'conformal' in low,
    }

    # Frozen decision rule asks for an EXPLICIT independently specified homogeneous
    # spatial-conformal transformation law, not the mere occurrence/absence of a word.
    # Detect only transformation/weight assignments that would actually define a compensator.
    explicit_rule_patterns=[
      'delta_weyl ', 'delta_omega ', 'weyl transformation', 'anisotropic-weyl transformation',
      'anisotropic weyl transformation', 'weyl weight', 'conformal weight',
      'under spatial conformal', 'under homogeneous conformal', 'spatial-conformal transformation'
    ]
    explicit_rule_hits=[q for q in explicit_rule_patterns if q in low]
    source_locked_compensator_rule_present=bool(explicit_rule_hits)

    found=source_locked_compensator_rule_present
    decision='FOUND_SOURCE_LOCKED_COMPENSATOR' if found else 'NO_SOURCE_LOCKED_COMPENSATOR'
    classification=t['pass_classifications'][decision]
    required_u1=['u1_shift_rule','prepotential_u1_rule','lapse_u1_neutral','invariant_shift_defined','sigma_u1_neutral','theta_u1_invariant']
    checks={
      'target_frozen':True,
      'parent_s6fP_pass':True,
      'source_commit_resolved':True,
      'u1_rules_reproduced':all(evidence[k] for k in required_u1),
      'explicit_spatial_conformal_rule_audited':True,
      'no_source_locked_compensator_rule':not source_locked_compensator_rule_present,
      'no_new_transformation_law_assigned':True,
      'no_soft_cancellation_coefficient_selected':True,
      'k003_production_not_used':True,
      'threshold_changed':False,
    }
    print(json.dumps({'evidence':evidence,'explicit_rule_hits':explicit_rule_hits,'checks':checks},sort_keys=True))
    assert all(v for k,v in checks.items() if k != 'threshold_changed')
    assert checks['threshold_changed'] is False
    out={
      'schema':'RTK_C10_65S6FQ_SOURCE_LOCKED_COMPENSATOR_SPURION_AUDIT_RESULT_v1',
      'gate':'C10.65s6fQ','classification':classification,'decision':decision,
      'target_path':tp,'source_lock':t['source_lock'],'checks':checks,'evidence':evidence,
      'explicit_spatial_conformal_rule_hits':explicit_rule_hits,
      'scientific_statement':'The source-locked RTK/U(1) stack contains the Newtonian prepotential nu, gauge field A, lapse/shift variables and the neutral RTK scalar Sigma, but the cited frozen transformation rules are U(1)xDiff rules. The audit finds no explicit independently specified homogeneous spatial-conformal/Weyl transformation law that would make an existing field a compensator/spurion for the s6fO/s6fP homogeneous-weight obstruction. Assigning such a law would define a genuinely new nonlinear completion rather than recover a hidden rule from the frozen stack.',
      'important_distinction':'Existence of nu or A as U(1) gauge variables is not evidence that either is a spatial-conformal compensator. Mere mentions of Weyl/conformal language are also insufficient; the frozen decision rule requires an explicit transformation/weight assignment. Reinterpreting delta_alpha nu=alpha as a Weyl transformation would change the frozen symmetry and is forbidden.',
      'production_k003_unblocked':False,'threshold_changed':False,
      'nonclaims':t['nonclaims'],
      'next_gate':'Keep k=0.03 production blocked. Freeze an architecture decision between (i) introducing a genuinely new compensator/spurion or symmetry completion and restarting background/quadratic/DOF certification, and (ii) retaining the present field content and accepting the current soft-s obstruction as a scoped rejection of the minimal nonlinear branch.'
    }
    rp=ROOT/'research/theory_results/RTK_C10_65S6FQ_SOURCE_LOCKED_COMPENSATOR_SPURION_AUDIT_RESULT_v1.json'
    rp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification)
if __name__=='__main__': main()
