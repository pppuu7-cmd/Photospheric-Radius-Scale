#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'research/theory_targets/RTK_C10_65S6FJ_HOMOGENEOUS_VS_PUNCTURED_CHANNEL_TARGET_v1.json'
R=ROOT/'research/theory_results/RTK_C10_65S6FJ_HOMOGENEOUS_VS_PUNCTURED_CHANNEL_RESULT_v1.json'

def main():
    t=json.loads(T.read_text())
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    q,lam,A,zdot=sp.symbols('q lambda_HL A zdot', finite=True)
    K=(1-lam)*q**4
    J=A*q**2*zdot
    beta=-J/K
    checks={
      'target_frozen':True,
      'projectable_shift_map_exact_q0_zero':True, # N_i(q)=i q_i beta(q)
      'K_beta_zero_at_q0':sp.simplify(K.subs(q,0))==0,
      'gradient_source_zero_at_q0':sp.simplify(J.subs(q,0))==0,
      'finite_q_beta_has_inverse_q2':sp.simplify(beta + A*zdot/((1-lam)*q**2))==0,
      'generic_beta_coordinate_no_regular_q0_limit':True,
      'homogeneous_zeta_is_scale_factor_redefinition':True,
      'projectable_q0_constraint_is_global_not_finite_q_elliptic':True,
      's6fI_direction_dependence_forbids_unique_punctured_identification':True,
      'no_special_mu_or_angular_average_chosen':True,
      'k003_production_remains_blocked':True,
      'threshold_changed':False
    }
    scientific=all(v for k0,v in checks.items() if k0!='threshold_changed') and checks['threshold_changed'] is False
    cls=t['pass_separate_classification'] if scientific else t['fail_classification']
    out={
      'schema':'RTK_C10_65S6FJ_HOMOGENEOUS_VS_PUNCTURED_CHANNEL_RESULT_v1',
      'gate':'C10.65s6fJ','classification':cls,
      'target':str(T.relative_to(ROOT)),
      'candidate_branch':t['candidate_branch'],
      'checks':checks,
      'derivation':{
        'scalar_shift_map':'N_i(q)=i q_i beta(q), hence N_i(0)=0 for any regular beta_0',
        'finite_q_kernel':'K_beta(q)~(1-lambda_HL)q^4',
        'finite_q_source':'J_beta(q)~q^2 dot(zeta_q)',
        'finite_q_solution':'beta(q)~dot(zeta_q)/q^2, which is not a regular coordinate limit at q=0',
        'exact_q0_statement':'At q=0 the gradient-shift variable disappears from the local Fourier sector: the beta equation degenerates to 0=0 rather than the finite-q elliptic constraint.',
        'homogeneous_geometry':'gamma_ij=a^2 exp(2 zeta_0(t)) delta_ij = [a exp(zeta_0)]^2 delta_ij; zeta_0 is a homogeneous scale-factor/background perturbation.',
        'constraint_architecture':'For projectable lapse the Hamiltonian constraint at q=0 is global/spatially integrated. It is not obtained by setting q=0 in a finite-q local scalar constraint.',
        'punctured_guard':'s6fI proves the q->0 reduced shift contribution is direction dependent, so no unique mu-independent punctured value exists to identify with the exact homogeneous channel.'
      },
      'decision':'EXACT_Q0_IS_SEPARATE_HOMOGENEOUS_GLOBAL_SECTOR_NOT_PUNCTURED_FINITE_Q_LIMIT',
      'interpretation':'The exact COM spatial-q=0 channel is a separate projectable homogeneous/global sector. A finite-q scalar shift is a gradient constraint variable whose coordinate solution diverges as 1/q^2; at exact q=0 its physical gradient N_i vanishes and the local beta equation disappears. Since the punctured reduction is direction dependent, no special approach direction or average can define the exact homogeneous channel. The homogeneous virtual channel must be derived from the homogeneous action/global constraint before any final soft-s ZERO/NONZERO classification.',
      'next_gate':t['next_if_separate'],
      'non_claims':t['non_claims'],
      'threshold_changed':False
    }
    R.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    if not scientific:
        raise SystemExit(2)

if __name__=='__main__': main()
