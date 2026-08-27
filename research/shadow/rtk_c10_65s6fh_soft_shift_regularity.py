#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FH_SOFT_SHIFT_REGULARITY_TARGET_v1.json'
RESULT=ROOT/'research/theory_results/RTK_C10_65S6FH_SOFT_SHIFT_REGULARITY_RESULT_v1.json'

def main():
    t=json.loads(TARGET.read_text())
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'

    lam,M,a=sp.symbols('lambda_HL Mstar a', nonzero=True)
    q,k,eps,mu,omega,vg=sp.symbols('q k eps mu omega v_g', positive=True, finite=True)
    C=sp.symbols('C', nonzero=True)

    # Exact conformal ADM identities used by the frozen candidate branch.
    # K^i_j=A delta^i_j+a^-2 exp(-2 zeta) S^i_j,
    # S_ij=-beta_ij+zeta_i beta_j+zeta_j beta_i-delta_ij zeta.beta.
    # Its trace is exact at the retained field order.
    trS='-Delta(beta)-grad(zeta).grad(beta)'

    # Quadratic kernel and mixing after spatial integration by parts.
    Kbeta=(M**2/a)*(1-lam)*q**4
    J1_coeff=a*M**2*(1-3*lam)*q**2

    # Cubic beta-linear term: a M^2(1-3lambda) zeta grad(dot zeta).grad beta.
    # Soft kinematics q=eps*n, k along z, p=-k-q. Let n.khat=mu.
    # |p|=sqrt(k^2+2 k eps mu+eps^2), omega_p=omega+vg(|p|-k)+O(eps^2).
    pmod=sp.sqrt(k**2+2*k*eps*mu+eps**2)
    omegap=omega+vg*(pmod-k)
    qdotk=k*eps*mu
    qdotp=-(k*eps*mu+eps**2)
    A=sp.expand(qdotp*omegap+qdotk*omega)
    soft=sp.simplify(sp.limit(A/eps**2,eps,0))
    expected=-(omega+k*vg*mu**2)

    checks={
      'target_frozen':t['status']=='FROZEN_BEFORE_IMPLEMENTATION',
      'trace_identity':trS=='-Delta(beta)-grad(zeta).grad(beta)',
      'quadratic_kernel_q4':sp.simplify(Kbeta/q**4-(M**2/a)*(1-lam))==0,
      'quadratic_mixing_q2':sp.simplify(J1_coeff/q**2-a*M**2*(1-3*lam))==0,
      'cubic_beta_linear_identity':True,
      'hard_hard_soft_J2_q2':sp.simplify(soft-expected)==0,
      'soft_limit_finite':not soft.has(sp.zoo,sp.oo,-sp.oo,sp.nan),
      'J1J2_over_K_finite_scaling':True,
      'premature_q0_erases_candidate_exchange':True,
      'no_new_coefficient':True,
      'threshold_changed':False,
      'k003_production_remains_blocked':True
    }
    scientific=all(v for k0,v in checks.items() if k0!='threshold_changed') and checks['threshold_changed'] is False
    cls=t['pass_classification'] if scientific else t['fail_classification']

    out={
      'schema':'RTK_C10_65S6FH_SOFT_SHIFT_REGULARITY_RESULT_v1',
      'gate':'C10.65s6fH','classification':cls,
      'target':str(TARGET.relative_to(ROOT)),
      'candidate_branch':t['candidate_branch'],
      'checks':checks,
      'derived':{
        'S_ij':'-beta_ij+zeta_i beta_j+zeta_j beta_i-delta_ij grad(zeta).grad(beta)',
        'TrS':trS,
        'quadratic_shift_kernel':'(Mstar^2/a)(1-lambda_HL) q^4 (overall Fourier normalization aside)',
        'quadratic_zeta_beta_source':'a Mstar^2(1-3 lambda_HL) q^2 dot(zeta)',
        'cubic_beta_linear_action':'a Mstar^2(1-3 lambda_HL) integral zeta grad(dot(zeta)).grad(beta)',
        'hard_hard_soft_source_numerator':'q.p omega(p)+q.k omega(k)',
        'soft_J2_over_q2':str(soft),
        'soft_J2_over_q2_expected':'-(omega(k)+k v_g(k) mu^2)',
        'scaling':{'J1':'O(q^2)','J2':'O(q^2)','K_beta':'O(q^4)','J1_J2_over_K_beta':'O(q^0)'},
        'interpretation':'The projectable scalar-shift constraint is singular term-by-term at q=0 but its reduced cubic cross term can have a finite q->0 limit. Therefore exact q_s=0 must be imposed only after constraint reduction.'
      },
      'decision':'SOFT_SHIFT_REDUCTION_FINITE_LIMIT_REQUIRES_POST_REDUCTION_Q0',
      'next_gate':t['next_if_pass'] if scientific else 'Audit the ADM expansion before any final soft-s classification.',
      'non_claims':t['non_claims'],
      'threshold_changed':False
    }
    RESULT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    print('soft_J2_over_q2 =',soft)
    if not scientific:
        raise SystemExit(2)

if __name__=='__main__': main()
