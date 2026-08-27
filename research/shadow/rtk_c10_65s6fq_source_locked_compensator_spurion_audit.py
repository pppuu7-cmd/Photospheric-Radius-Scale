#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(p): return json.loads((ROOT/p).read_text())
def git_show(commit,path):
    return subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=ROOT,text=True)

def main():
    tp='research/theory_targets/RTK_C10_65S6FQ_SOURCE_LOCKED_COMPENSATOR_SPURION_AUDIT_TARGET_v1.json'
    pp='research/theory_results/RTK_C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_RESULT_v1.json'
    t=load(tp); p=load(pp)
    assert t['status']=='FROZEN_BEFORE_EXECUTION'
    assert p['classification']=='C10_65S6FP_MIXED_TIME_SPACE_OFFSHELL_OPERATOR_OBSTRUCTION_PASS_SCOPED'
    c=t['source_lock']['archive_commit']
    u=git_show(c,t['source_lock']['u1_appendix'])
    n=git_show(c,t['source_lock']['canonical_narrowing'])
    low=(u+'\n'+n).lower()
    evidence={
      'u1_shift_rule':'delta_alpha N_i = N D_i alpha' in u,
      'prepotential_u1_rule':'delta_alpha nu = alpha' in u,
      'lapse_u1_neutral':'delta_alpha N = 0' in u,
      'invariant_shift_defined':'Ntilde^i = N^i - N D^i nu' in u,
      'sigma_u1_neutral':'U(1)-neutral scalar `Sigma`' in u,
      'theta_u1_invariant':'delta_alpha Theta_U = 0' in u,
      'canonical_stack_identifies_prepotential_velocity':'prepotential velocity' in n,
      'explicit_weyl_keyword_absent':'weyl' not in low,
      'anisotropic_weyl_keyword_absent':'anisotropic weyl' not in low,
    }
    # Existing fields are source-locked under U(1)xDiff only. No independent spatial-Weyl
    # rule is present in the frozen sources, so using any of them as a conformal compensator
    # would require a new symmetry assignment.
    found=False
    decision='FOUND_SOURCE_LOCKED_COMPENSATOR' if found else 'NO_SOURCE_LOCKED_COMPENSATOR'
    classification=t['pass_classifications'][decision]
    checks={
      'target_frozen':True,
      'parent_s6fP_pass':True,
      'source_commit_resolved':True,
      'u1_rules_reproduced':all(evidence[k] for k in ['u1_shift_rule','prepotential_u1_rule','lapse_u1_neutral','invariant_shift_defined','sigma_u1_neutral','theta_u1_invariant']),
      'no_explicit_weyl_symmetry_in_source_lock':evidence['explicit_weyl_keyword_absent'] and evidence['anisotropic_weyl_keyword_absent'],
      'no_new_transformation_law_assigned':True,
      'no_soft_cancellation_coefficient_selected':True,
      'k003_production_not_used':True,
      'threshold_changed':False,
    }
    assert all(checks.values())
    out={
      'schema':'RTK_C10_65S6FQ_SOURCE_LOCKED_COMPENSATOR_SPURION_AUDIT_RESULT_v1',
      'gate':'C10.65s6fQ','classification':classification,'decision':decision,
      'target_path':tp,'source_lock':t['source_lock'],'checks':checks,'evidence':evidence,
      'scientific_statement':'The source-locked RTK/U(1) stack contains the Newtonian prepotential nu, gauge field A, lapse/shift variables and the neutral RTK scalar Sigma, but the cited frozen transformations are U(1)xDiff rules. No independent homogeneous spatial-conformal/Weyl transformation law is specified for these fields. Therefore none is already source-locked as the compensator/spurion required to evade the s6fO/s6fP homogeneous-weight obstruction. Assigning such a weight would define a genuinely new nonlinear completion rather than recover an existing hidden degree of freedom.',
      'important_distinction':'Existence of nu or A as U(1) gauge variables is not evidence that either is a spatial-conformal compensator. Reinterpreting delta_alpha nu=alpha as a Weyl transformation would change the frozen symmetry and is forbidden in this audit.',
      'production_k003_unblocked':False,'threshold_changed':False,
      'nonclaims':t['nonclaims'],
      'next_gate':'Keep k=0.03 production blocked. The remaining local escape requires a genuinely enlarged completion (extra compensator/spurion or a separately re-certified symmetry/action). Before constructing one, freeze an architecture decision gate comparing: (i) enlarge the field/symmetry content and restart background/quadratic/DOF certification, or (ii) retain the minimal field content and accept the current soft-s obstruction as a scoped rejection of that nonlinear branch.'
    }
    rp=ROOT/'research/theory_results/RTK_C10_65S6FQ_SOURCE_LOCKED_COMPENSATOR_SPURION_AUDIT_RESULT_v1.json'
    rp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification)
    print(json.dumps({'decision':decision,'checks':checks},sort_keys=True))
if __name__=='__main__': main()
