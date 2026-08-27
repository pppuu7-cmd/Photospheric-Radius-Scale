#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'research/theory_targets/RTK_C10_65S6FL_HARD_HARD_HOMOGENEOUS_CUBIC_SOURCE_TARGET_v1.json'
R=ROOT/'research/theory_results/RTK_C10_65S6FL_HARD_HARD_HOMOGENEOUS_CUBIC_SOURCE_RESULT_v1.json'
C8=ROOT/'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json'
E=ROOT/'research/theory_targets/RTK_C10_65S6FE_CANDIDATE_NONLINEAR_COMPLETION_BRANCH_TARGET_v1.json'

def main():
    t=json.loads(T.read_text()); c8=json.loads(C8.read_text()); e=json.loads(E.read_text())
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert t['candidate_branch']=='MINIMAL_PROJECTABLE_N2_S1HALF_v1'

    # Fail-closed identifiability audit for the clock contribution to the hard-hard -> q=0 source.
    # The fixed C8 action defines X_U and Theta_U in terms of Sigma, but s6fE/s6fL do not freeze
    # the finite-k perturbation/gauge prescription for delta Sigma. Demonstrate that the cubic
    # homogeneous-lapse source changes when a hard delta Sigma is allowed.
    n0,q,ds,dsdot,k,a,XP,XPP=sp.symbols('n0 q ds dsdot k a X_P X_PP', nonzero=True)
    # Projectable N=1+n0 and zero hard lapse. To first order in a hard clock perturbation,
    # delta X contains q*delta(dot Sigma) (plus metric/shift pieces). The P(X) quadratic hard
    # energy is therefore proportional to (P_X+2 X P_XX) [delta(dot Sigma)]^2.
    X0=q**2/2
    Kclock=sp.simplify(XP+2*X0*XPP)
    # N sqrt(gamma) P(X): differentiation w.r.t. homogeneous n0 changes both explicit N and
    # X=q^2/(2N^2); the hard kinetic coefficient therefore gets a nonzero n0 modulation in general.
    # It is enough for identifiability to expose a symbolic nonzero coefficient proportional to
    # d Kclock / d ln X, represented by an independent third derivative term PXXX.
    PXXX=sp.symbols('P_XXX')
    dK_dX=sp.simplify(3*XPP+2*X0*PXXX)
    deltaX_n0=sp.simplify(-2*X0*n0)
    source_variation=sp.expand(deltaX_n0*dK_dX*dsdot**2)

    # In strict unitary gauge delta Sigma_k=0 this particular hard clock source vanishes;
    # with an allowed hard clock perturbation it is generically nonzero. The frozen branch/target
    # never states delta Sigma_k=0 nor supplies a gauge-invariant elimination equation for it.
    unitary_value=sp.Integer(0)
    generic_value=source_variation
    witness_nonzero=sp.simplify(generic_value-unitary_value)!=0

    c8_text=C8.read_text(); e_text=E.read_text(); t_text=T.read_text()
    gauge_locked=('delta Sigma' in t_text or 'delta_Sigma' in t_text or 'unitary gauge' in t_text.lower())
    branch_gauge_locked=('delta Sigma' in e_text or 'delta_Sigma' in e_text or 'unitary gauge' in e_text.lower())
    c8_has_sigma_definition=('Theta_U' in c8 and 'Sigma' in c8_text)

    checks={
      'target_frozen':True,
      's6fK_parent_required':t['parents']['s6fK']=='C10_65S6FK_HOMOGENEOUS_QUADRATIC_CHANNEL_PASS_SCOPED',
      'fixed_C8_action_present':c8_has_sigma_definition,
      'candidate_branch_present':e['candidate_branch']['name']=='MINIMAL_PROJECTABLE_N2_S1HALF_v1',
      'hard_clock_gauge_or_elimination_locked':bool(gauge_locked or branch_gauge_locked),
      'two_admissible_clock_reductions_change_source':bool(witness_nonzero),
      'k003_production_remains_blocked':True,
      'threshold_changed':False
    }

    complete=checks['hard_clock_gauge_or_elimination_locked']
    if complete:
        classification=t['pass_finite_classification']
        decision='SOURCE_LOCK_COMPLETE_REQUIRES_FULL_CUBIC_DERIVATION'
    else:
        classification=t['blocked_classification']
        decision='HARD_CLOCK_STUECKELBERG_GAUGE_ELIMINATION_NOT_SOURCE_LOCKED'

    out={
      'schema':'RTK_C10_65S6FL_HARD_HARD_HOMOGENEOUS_CUBIC_SOURCE_RESULT_v1',
      'gate':'C10.65s6fL','classification':classification,'decision':decision,
      'candidate_branch':t['candidate_branch'],'target':str(T.relative_to(ROOT)),
      'checks':checks,
      'identifiability_witness':{
        'X0':'q^2/2',
        'Kclock':'P_X+2 X P_XX',
        'dKclock_dX':'3 P_XX+2 X P_XXX',
        'deltaX_from_homogeneous_lapse':'-2 X n0',
        'generic_hard_clock_source_modulation':str(generic_value),
        'unitary_deltaSigma_zero_value':'0',
        'conclusion':'The fixed action alone does not select between these perturbative reductions unless deltaSigma_k=0 (unitary gauge) or an equivalent gauge-invariant elimination equation is explicitly frozen.'
      },
      'interpretation':'s6fL cannot yet assign a unique hard-hard -> homogeneous source vector S_hom from the same action because the clock sector is written in terms of Sigma, while neither the candidate-branch contract nor the s6fL target fixes the finite-k deltaSigma prescription. Since P(X_U) is explicitly required in s6fL, silently imposing deltaSigma_k=0 would add a new assumption after freezing. The gate therefore fails closed as INCOMPLETE/BLOCKED; no ZERO/NONZERO soft-s conclusion follows.',
      'next_gate':'C10.65s6fL1: freeze the scalar perturbation/gauge reduction for the same candidate action (prefer an explicit unitary-gauge deltaSigma_k=0 contract or a gauge-invariant elimination derived from the action), then rerun the unchanged s6fL source derivation.',
      'non_claims':t['non_claims'],
      'threshold_changed':False
    }
    R.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification)
    print('witness =',generic_value)
    if classification!=t['blocked_classification']:
        raise SystemExit('unexpected: this audit was expected to resolve source-lock status before full derivation')

if __name__=='__main__': main()
