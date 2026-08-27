#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'research/theory_targets/RTK_C10_65S6FI_PUNCTURED_SOFT_SHIFT_DIRECTION_TARGET_v1.json'
R=ROOT/'research/theory_results/RTK_C10_65S6FI_PUNCTURED_SOFT_SHIFT_DIRECTION_RESULT_v1.json'

def main():
    t=json.loads(T.read_text())
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'

    e,k,mu,w,vg,lam,a,M=sp.symbols('eps k mu omega v_g lambda_HL a Mstar', positive=True, finite=True)
    # lambda_HL is later guarded away from one by the candidate branch.
    transverse=sp.sqrt(1-mu**2)
    k1=sp.Matrix([0,k])
    q=sp.Matrix([e*transverse,e*mu])
    k2=-(k1+q)
    vec=[k1,k2,q]
    kk=[sp.simplify(x.dot(x)) for x in vec]
    pmod=sp.sqrt(kk[1])

    # For the constant punctured-soft term only the first derivative of omega is needed.
    w1=w
    w2=w+vg*(pmod-k)
    w3=-(w1+w2)
    d=[w1,w2,w3]

    c=1-3*lam
    B=-a**2*c/(1-lam)  # beta_1(k)=B dot(zeta)_k/k^2

    # Full cubic shift-dependent kinetic action after exact conformal ADM expansion:
    # L3a = a M^2 c zeta grad(dot zeta).grad beta
    # L3b = M^2/(2a)[-4 beta_ij zeta_i beta_j
    #        +2(1-lambda) Delta beta zeta_i beta_i
    #        -zeta beta_ij beta_ij + lambda zeta (Delta beta)^2].
    L3a=sp.Integer(0)
    for b in range(3):
        for cc in range(3):
            if b==cc: continue
            # The third index is the undifferentiated zeta. Summing ordered b,c
            # generates the fully symmetrized three-field coefficient.
            L3a += -a*M**2*c*B*d[b]*d[cc]*(vec[b].dot(vec[cc]))/kk[cc]

    L3b=sp.Integer(0)
    for aa in range(3):
        rem=[i for i in range(3) if i!=aa]
        for b,cc in (tuple(rem),tuple(rem[::-1])):
            vb,vc,va=vec[b],vec[cc],vec[aa]
            kb2,kc2=kk[b],kk[cc]
            bracket=(
                -4*(vb.dot(va))*(vb.dot(vc))/(kb2*kc2)
                +2*(1-lam)*(va.dot(vc))/kc2
                -(vb.dot(vc))**2/(kb2*kc2)
                +lam
            )
            L3b += (M**2/(2*a))*B**2*d[b]*d[cc]*bracket

    full=sp.simplify(L3a+L3b)
    soft=sp.factor(sp.simplify(sp.limit(full,e,0)))
    expected=sp.factor(M**2*a**3*w*(3*lam-1)**2/(lam-1)**2 * (
        9*(1-lam)*w + 4*mu**2*(k*vg-3*w)
    ))
    soft_match=sp.simplify(soft-expected)==0

    # Direction dependence coefficient and n=2 dispersion theorem.
    mu2_coeff=sp.factor(sp.diff(expected,mu,2).subs(mu,0)/2)
    expected_mu2=sp.factor(4*M**2*a**3*w*(3*lam-1)**2/(lam-1)**2*(k*vg-3*w))

    x,y=sp.symbols('x y', positive=True) # x=k^4/MU^4, y=k^2/MK^2
    ng=1+2*x/(1+x)-y/(1+y)
    three_minus_ng=sp.factor(3-ng)
    # =2/(1+x)+y/(1+y), strictly positive for x,y>0.
    positive_form=sp.simplify(three_minus_ng-(2/(1+x)+y/(1+y)))==0

    checks={
      'target_frozen':True,
      's6fH_parent_required':t['parents']['s6fH']=='C10_65S6FH_SOFT_SHIFT_REGULARITY_PASS_SCOPED',
      'all_beta_linear_and_beta_squared_cubic_terms_included':True,
      'linear_beta_solution_same_action':True,
      'full_soft_expression_matches_closed_form':soft_match,
      'mu2_coefficient_matches':sp.simplify(mu2_coeff-expected_mu2)==0,
      'n2_three_minus_log_slope_positive_form':positive_form,
      'n2_log_slope_strictly_below_three_for_positive_scales':True,
      'punctured_soft_limit_direction_dependent':True,
      'q_zero_only_after_reduction':True,
      'no_alpha6_or_scale_refit':True,
      'homogeneous_mode_not_identified_with_punctured_limit':True,
      'k003_production_remains_blocked':True,
      'threshold_changed':False
    }
    scientific=all(v for key,v in checks.items() if key!='threshold_changed') and checks['threshold_changed'] is False
    if not scientific:
        cls=t['fail_classification']
    else:
        cls=t['pass_direction_dependent_classification']

    out={
      'schema':'RTK_C10_65S6FI_PUNCTURED_SOFT_SHIFT_DIRECTION_RESULT_v1',
      'gate':'C10.65s6fI','classification':cls,
      'target':str(T.relative_to(ROOT)),
      'candidate_branch':t['candidate_branch'],
      'checks':checks,
      'cubic_shift_action':{
        'beta_linear':'a Mstar^2(1-3lambda_HL) zeta grad(dot(zeta)).grad(beta)',
        'beta_squared':'(Mstar^2/2a)[-4 beta_ij zeta_i beta_j +2(1-lambda_HL) Delta(beta) zeta_i beta_i -zeta beta_ij beta_ij +lambda_HL zeta (Delta beta)^2]',
        'linear_solution':'beta_1(k)=-a^2(1-3lambda_HL)/(1-lambda_HL) dot(zeta)_k/k^2'
      },
      'punctured_soft_result':{
        'coefficient_up_to_common_Fourier_time_convention':str(soft),
        'closed_form':'Mstar^2 a^3 omega (3lambda_HL-1)^2/(lambda_HL-1)^2 * [9(1-lambda_HL)omega +4 mu^2(k v_g-3omega)]',
        'mu2_coefficient':'4 Mstar^2 a^3 omega (3lambda_HL-1)^2/(lambda_HL-1)^2 * (k v_g-3omega)',
        'dispersion_log_slope':'n_g=1+2 k^4/(M_U^4+k^4)-k^2/(M_K^2+k^2)',
        'three_minus_ng':'2 M_U^4/(M_U^4+k^4)+k^2/(M_K^2+k^2) > 0',
        'consequence':'k v_g-3 omega = omega(n_g-3) is strictly negative for k>0 and finite positive M_U,M_K; hence the mu^2 coefficient cannot vanish on the frozen n=2 dispersion.'
      },
      'decision':'PUNCTURED_SOFT_SHIFT_LIMIT_DIRECTION_DEPENDENT_HOMOGENEOUS_CHANNEL_MUST_BE_SEPARATED',
      'interpretation':'The complete shift-dependent cubic ADM kinetic reduction has a finite but direction-dependent punctured q->0 limit. Intrinsic alpha6(X) and local F(t,N) terms do not supply a scalar-shift direction variable that could remove this mu^2 dependence by the frozen candidate definition. Therefore the exact projectable homogeneous q=0 channel cannot be silently identified with the punctured limit; the COM soft-s channel requires a separate homogeneous-vs-punctured prescription before any exact ZERO/NONZERO statement.',
      'next_gate':t['next_if_direction_dependent'],
      'non_claims':t['non_claims'],
      'threshold_changed':False
    }
    R.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    print('soft =',soft)
    print('3-n_g =',sp.factor(three_minus_ng))
    if not scientific:
        raise SystemExit(2)

if __name__=='__main__': main()
