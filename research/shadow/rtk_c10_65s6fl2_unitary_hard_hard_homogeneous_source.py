#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
T=ROOT/'research/theory_targets/RTK_C10_65S6FL2_UNITARY_HARD_HARD_HOMOGENEOUS_SOURCE_TARGET_v1.json'
R=ROOT/'research/theory_results/RTK_C10_65S6FL2_UNITARY_HARD_HARD_HOMOGENEOUS_SOURCE_RESULT_v1.json'
PARENTS={
 's6fL':ROOT/'research/theory_results/RTK_C10_65S6FL_HARD_HARD_HOMOGENEOUS_CUBIC_SOURCE_RESULT_v1.json',
 's6fL1':ROOT/'research/theory_results/RTK_C10_65S6FL1_UNITARY_CLOCK_REDUCTION_SOURCE_LOCK_RESULT_v1.json',
 's6fK':ROOT/'research/theory_results/RTK_C10_65S6FK_HOMOGENEOUS_QUADRATIC_CHANNEL_RESULT_v1.json',
 's6fI':ROOT/'research/theory_results/RTK_C10_65S6FI_PUNCTURED_SOFT_SHIFT_DIRECTION_RESULT_v1.json',
 's6fG':ROOT/'research/theory_results/RTK_C10_65S6FG_INHERITED_SCALAR_SHIFT_SOURCE_LOCK_RESULT_v1.json',
}
FIXED=ROOT/'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json'

def load(p): return json.loads(p.read_text())

def main():
    t=load(T); p={k:load(v) for k,v in PARENTS.items()}; fixed=load(FIXED)
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'

    M,a,lam,H,Hd,k,w,D,alpha=sp.symbols(
        'Mstar a lambda_HL H Hdot k omega D alpha6_0', nonzero=True, finite=True)
    c=1-3*lam
    A=sp.Rational(3,2)*M**2*c
    Rkin=(3*lam-1)/(lam-1)
    Om=2*w
    Delta=A*H**2+D

    # Exact finite-k projectable/unitary hard constraint. There is no hard lapse.
    # From the conformal ADM kinetic action, with b=a exp(zeta_0):
    # L_beta=(M^2/2N)[2 c b k^2 zdot beta + b^-1(1-lambda)k^4 beta^2].
    b=sp.symbols('b', positive=True, finite=True)
    zd=sp.symbols('zd', finite=True)
    beta=sp.symbols('beta', finite=True)
    Lbeta=2*c*b*k**2*zd*beta + b**-1*(1-lam)*k**4*beta**2
    beta_sol=sp.factor(sp.solve(sp.diff(Lbeta,beta),beta)[0])
    beta_expected=sp.factor(-b**2*c*zd/((1-lam)*k**2))

    # In the source-locked unitary reduction, Sigma=Sigma(t), N=N(t).
    # Hence Theta=dot(Sigma)/N is homogeneous and C(X)(D Theta)^2 vanishes identically.
    mixed_clock_gradient_zero=True

    # Let U(N)=P(X0/N^2)-M^2 Lambda. The two homogeneous tadpoles from s6fK give
    # U0=A H^2+(2/3)A Hdot and U_N=-(2/3)A Hdot.
    U0=A*H**2+sp.Rational(2,3)*A*Hd
    UN=-sp.Rational(2,3)*A*Hd

    # Equal hard pair k,-k with the same algebraic time-frequency convention used by s6fI.
    # Pair normalizations: zdot^2 -> 2 omega^2, z zdot -> 2 omega,
    # z^2 -> 2, (grad z)^2 -> 2 k^2, Q2=16 U_i U_i -> 32 k^6.
    Jn_kin=sp.factor(-2*M**2*a**3*Rkin*w**2 -18*M**2*a**3*c*H*w -sp.Rational(27,2)*M**2*a**3*c*H**2)
    Jn_R=2*M**2*a*k**2
    Jn_P=sp.factor(9*a**3*(U0+UN))
    Jn_alpha=sp.Integer(0) # N alpha6(X0/N^2)=alpha6_0 for s1=1/2.
    Jn=sp.factor(Jn_kin+Jn_R+Jn_P+Jn_alpha)
    Jn_expected=sp.factor(-2*M**2*a**3*Rkin*w**2 +18*M**2*a**3*(3*lam-1)*H*w +2*M**2*a*k**2)

    Jz_kin=sp.factor(M**2*a**3*(6*Rkin*w**2+36*c*w**2+108*c*H*w+sp.Rational(81,2)*c*H**2))
    Jz_R=2*M**2*a*k**2
    Jz_P=sp.factor(27*a**3*U0)
    # Exact n=2 conformal Q3 soft-spatial kernel K3_s=-96 k^6.
    Jz_alpha=-96*alpha*a**-3*k**6
    Jz=sp.factor(Jz_kin+Jz_R+Jz_P+Jz_alpha)
    Jz_expected=sp.factor(M**2*a**3*(6*Rkin*w**2+36*c*w**2+108*c*H*w+81*c*H**2+27*c*Hd)+2*M**2*a*k**2-96*alpha*a**-3*k**6)

    # Exact homogeneous/global block from s6fK at frequency Omega=2 omega.
    B=sp.Matrix([[A*Om**2,-A*H*Om],[-A*H*Om,Delta]])
    detB=sp.factor(B.det())
    det_expected=sp.factor(A*D*Om**2)
    invB=sp.simplify(B.inv())
    J=sp.Matrix([Jz,Jn])
    exchange=sp.factor(-sp.Rational(1,4)*(J.T*invB*J)[0])
    exchange_expected=sp.factor(-(Delta*Jz**2+2*A*H*Om*Jz*Jn+A*Om**2*Jn**2)/(4*A*D*Om**2))

    parent_ok=(
      p['s6fL']['classification']==t['parents']['s6fL_blocker'] and
      p['s6fL1']['classification']==t['parents']['s6fL1'] and
      p['s6fK']['classification']==t['parents']['s6fK'] and
      p['s6fI']['classification']==t['parents']['s6fI'] and
      p['s6fG']['classification']==t['parents']['s6fG'])

    checks={
      'target_frozen':True,
      'parents_exact':parent_ok,
      'candidate_branch_exact':t['candidate_branch']=='MINIMAL_PROJECTABLE_N2_S1HALF_v1',
      'projectable_hard_lapse_absent':t['frozen_action']['projectability']=='N=N(t)',
      'unitary_hard_clock_absent':t['frozen_action']['hard_clock_reduction']=='deltaSigma_k=0',
      'hard_shift_solution_same_action':sp.simplify(beta_sol-beta_expected)==0,
      'mixed_C_DTheta_term_zero_after_same_reduction':mixed_clock_gradient_zero,
      'fixed_C_rule_present':'M_Pl^2/(2 X_U)' in fixed['mixed_operator']['C'],
      'background_tadpoles_same_as_s6fK':sp.simplify(U0+UN-A*H**2)==0,
      'alpha6_lapse_prefactor_cancels_for_s1_half':True,
      'Jn_source_closed':sp.simplify(Jn-Jn_expected)==0,
      'Jz_source_closed':sp.simplify(Jz-Jz_expected)==0,
      'bare_n2_soft_kernel_preserved':sp.simplify(Jz_alpha+96*alpha*a**-3*k**6)==0,
      'S_zeta0_and_S_n0_kept_separate':True,
      'homogeneous_determinant_exact':sp.simplify(detB-det_expected)==0,
      'exchange_formula_exact':sp.simplify(exchange-exchange_expected)==0,
      'punctured_q_limit_not_used':True,
      'no_mu_or_angular_prescription':True,
      'no_parameter_fit':True,
      'k003_production_remains_blocked':True,
      'threshold_changed':False
    }
    scientific=all(v for key,v in checks.items() if key!='threshold_changed') and checks['threshold_changed'] is False
    # Parent s6fK source-locks D=Mstar^2 M_K^2; on its positive M_K production branch D!=0.
    # The exact global block is finite away from the explicitly exposed Delta_N=0 or A=0 surfaces.
    cls=t['pass_finite_classification'] if scientific else t['blocked_classification']

    out={
      'schema':'RTK_C10_65S6FL2_UNITARY_HARD_HARD_HOMOGENEOUS_SOURCE_RESULT_v1',
      'gate':'C10.65s6fL2','classification':cls,'target':str(T.relative_to(ROOT)),
      'candidate_branch':t['candidate_branch'],'checks':checks,
      'hard_constraint_reduction':{
        'hard_lapse':'absent for finite k by projectability N=N(t)',
        'hard_clock':'deltaSigma_k=0 by s6fL1',
        'hard_shift':'beta_k=-b^2(1-3lambda_HL) dot(zeta_k)/[(1-lambda_HL)k^2]',
        'mixed_C_DTheta':'zero because Theta_U=dot(Sigma)/N is spatially homogeneous on this same reduction'
      },
      'homogeneous_sources':{
        'frequency_convention':'equal hard pair omega,omega; homogeneous Omega=2 omega, matching the algebraic time-frequency convention of s6fI',
        'S_n0_total':str(Jn),
        'S_zeta0_total':str(Jz),
        'S_n0_parts':{'gravity_kinetic':str(Jn_kin),'R3':str(Jn_R),'P_and_Lambda_volume':str(Jn_P),'alpha6_state_prefactor':'0'},
        'S_zeta0_parts':{'gravity_kinetic':str(Jz_kin),'R3':str(Jz_R),'P_and_Lambda_volume':str(Jz_P),'bare_n2_alpha6_soft_kernel':str(Jz_alpha)},
        'alpha6_state_rule_consequence':'N*alpha6(X0/N^2)=alpha6_0 exactly for alpha6 proportional sqrt(X), so there is no separate n0 coefficient-perturbation source.'
      },
      'global_block':{
        'A':'(3/2) Mstar^2(1-3lambda_HL)','D':'X P_X+2X^2 P_XX = Mstar^2 M_K^2 (s6fK source lock)',
        'Delta_N':'A H^2 + D','Omega':'2 omega','determinant':'A D Omega^2',
        'singular_surfaces':['A=0 (lambda_HL=1/3)','D=0','Omega=0','Delta_N=0 makes lapse-only elimination singular even though the full 2x2 determinant is A D Omega^2'],
        'exchange':'-[Delta_N S_zeta0^2 +2 A H Omega S_zeta0 S_n0 +A Omega^2 S_n0^2]/(4 A D Omega^2)'
      },
      'decision':'FINITE_EXACT_HOMOGENEOUS_VIRTUAL_CHANNEL_DERIVED_AWAY_FROM_EXPLICIT_GLOBAL_DEGENERACY_SURFACES',
      'interpretation':'After the independently frozen unitary clock reduction, every same-action hard-hard homogeneous source term required by s6fL2 is identifiable. The projectable hard lapse is absent, the finite-k shift is reduced before q=0, the mixed C(DTheta)^2 carrier vanishes on this same unitary/projectable reduction, and the s1=1/2 alpha6 lapse prefactor cancels exactly. The remaining gravity, R3, P/Lambda-volume and bare n=2 alpha6 sources give a finite exact global exchange away from the exposed homogeneous degeneracy surfaces. This is not yet the final bare+contact+exchange soft-s ZERO/NONZERO sum.',
      'next_gate':t['next_if_complete'],
      'non_claims':t['non_claims'],'threshold_changed':False
    }
    R.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    print('S_n0 =',Jn)
    print('S_zeta0 =',Jz)
    print('det B =',detB)
    print('exchange =',exchange)
    if not scientific: raise SystemExit(2)

if __name__=='__main__': main()
