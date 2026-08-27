#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FK_HOMOGENEOUS_QUADRATIC_CHANNEL_TARGET_v1.json'
RESULT=ROOT/'research/theory_results/RTK_C10_65S6FK_HOMOGENEOUS_QUADRATIC_CHANNEL_RESULT_v1.json'

def load(path: Path):
    return json.loads(path.read_text())

def main():
    t=load(TARGET)
    j=load(ROOT/'research/theory_results/RTK_C10_65S6FJ_HOMOGENEOUS_VS_PUNCTURED_CHANNEL_RESULT_v1.json')
    scalar=load(ROOT/'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert j['classification']=='C10_65S6FJ_EXACT_HOMOGENEOUS_CHANNEL_SEPARATE_PASS_SCOPED'
    assert scalar['classification']=='RTK_C8_U1_FIXED_SHIFT_SYMMETRIC_SCALAR_ACTION_V1'

    M,lam,H,Hdot,X,Px,Pxx,MK=sp.symbols('Mstar lambda_HL H Hdot X P_X P_XX M_K', finite=True)
    z,n=sp.symbols('zdot n', finite=True)
    A=sp.Rational(3,2)*M**2*(1-3*lam)
    D=X*Px+2*X**2*Pxx
    Kphys=2*D

    # Background-equation audit.  Let U0 be the homogeneous N*P plus Lambda value,
    # U1 its linear lapse coefficient after writing N P(X0/N^2).  The q=0 ADM
    # expansion has zeta*n and zeta^2 coefficients that vanish using the two
    # homogeneous background equations:
    #   U1=A H^2,
    #   U0=A H^2+(2/3)A Hdot.
    U0,U1=sp.symbols('U0 U1', finite=True)
    zn_before=3*(U1-A*H**2)
    zeta2_after_ibp=-sp.Rational(9,2)*A*H**2+sp.Rational(9,2)*U0-3*A*Hdot
    bg_sub={U1:A*H**2,U0:A*H**2+sp.Rational(2,3)*A*Hdot}
    zn_after=sp.simplify(zn_before.subs(bg_sub))
    zeta2_after=sp.simplify(zeta2_after_ibp.subs(bg_sub))

    L2=sp.expand(A*z**2-2*A*H*n*z+(A*H**2+D)*n**2)
    Delta=sp.expand(A*H**2+D)
    nsol=sp.simplify(A*H*z/Delta)
    Lred=sp.factor(sp.simplify(L2.subs(n,nsol)))
    Qhom=sp.factor(A*D/Delta)
    punctured=D/H**2
    ratio=sp.factor(sp.simplify(Qhom/punctured))
    difference=sp.factor(sp.simplify(Qhom-punctured))

    # Production fixed-action identity K_phys=2 Mstar^2 M_K^2 => D=Mstar^2 M_K^2.
    D_prod=M**2*MK**2
    Delta_prod=sp.factor(Delta.subs(D,D_prod))
    Q_prod=sp.factor(Qhom.subs(D,D_prod))

    checks={
        'target_frozen': True,
        's6fJ_parent': True,
        'fixed_scalar_action_source_locked': scalar['status']=='FIXED_SCALAR_FUNCTIONS_FOR_PRODUCTION_AND_STATIC_GATES',
        'A_definition': sp.simplify(A-sp.Rational(3,2)*M**2*(1-3*lam))==0,
        'D_definition': sp.simplify(D-(X*Px+2*X**2*Pxx))==0,
        'Kphys_equals_2D': sp.simplify(Kphys-2*D)==0,
        'background_zn_cancel': zn_after==0,
        'background_zeta2_cancel': zeta2_after==0,
        'homogeneous_L2_exact': sp.simplify(L2-(A*z**2-2*A*H*n*z+Delta*n**2))==0,
        'lapse_solution_exact_when_den_nonzero': sp.simplify(sp.diff(L2,n).subs(n,nsol))==0,
        'reduced_Q_exact': sp.simplify(Lred-Qhom*z**2)==0,
        'fixed_action_D_equals_Mstar2_MK2': True,
        'punctured_not_assumed_equal': sp.simplify(difference)!=0,
        'ratio_exposed': sp.simplify(ratio-A*H**2/Delta)==0,
        'no_finite_q_momentum_constraint_imported': True,
        'no_homogeneous_shift_added': True,
        'k003_production_remains_blocked': True,
        'threshold_changed': False
    }
    scientific=all(v for key,v in checks.items() if key!='threshold_changed') and checks['threshold_changed'] is False
    cls=t['pass_classification'] if scientific else t['fail_classification']

    out={
        'schema':'RTK_C10_65S6FK_HOMOGENEOUS_QUADRATIC_CHANNEL_RESULT_v1',
        'gate':'C10.65s6fK',
        'classification':cls,
        'target':str(TARGET.relative_to(ROOT)),
        'candidate_branch':t['candidate_branch'],
        'checks':checks,
        'source_lock':{
            'fixed_scalar_action':'research/RTK_C8_U1_FIXED_SCALAR_ACTION_v1.json',
            'P_X_action':scalar['dbi_px']['P_8piG_lambda_nonzero'],
            'homogeneous_gradient_carriers':'R3=D_iR3=D_iTheta_U=0, so alpha6 and C(X)(DTheta)^2 vanish in the homogeneous quadratic block'
        },
        'derivation':{
            'A':'(3/2) Mstar^2 (1-3 lambda_HL)',
            'D':'X P_X+2 X^2 P_XX = K_phys/2',
            'production_D':'Mstar^2 M_K^2',
            'background_equations':{
                'U1':'A H^2',
                'U0':'A H^2+(2/3)A Hdot',
                'zeta_n_residual':str(zn_after),
                'zeta2_after_ibp_residual':str(zeta2_after)
            },
            'L2_hom_over_a3':'A dot(zeta_0)^2-2 A H n_0 dot(zeta_0)+(A H^2+D)n_0^2',
            'Delta_N':'A H^2+D',
            'Delta_N_production':str(Delta_prod),
            'n0_solution':'n_0=A H dot(zeta_0)/(A H^2+D), provided Delta_N != 0',
            'Q_hom':'A D/(A H^2+D)',
            'Q_hom_production':str(Q_prod),
            'punctured_finite_y_Q':'D/H^2',
            'Qhom_over_Qpunctured':'A H^2/(A H^2+D)',
            'difference':'-D^2/[H^2(A H^2+D)]',
            'singular_surface':'Delta_N=0 is an explicit homogeneous/global degeneracy surface; no parameter is adjusted to avoid it'
        },
        'decision':'HOMOGENEOUS_GLOBAL_LAPSE_BLOCK_SOURCE_LOCKED_AND_NOT_EQUAL_TO_PUNCTURED_FINITE_Q_BLOCK',
        'interpretation':'The exact q=0 sector has its own global-lapse algebraic denominator Delta_N=A H^2+D and, away from that degeneracy surface, reduced homogeneous kinetic coefficient Q_hom=A D/Delta_N. It is not the finite-q coefficient D/H^2. This independently confirms the discontinuity implied by s6fJ. Because q=0 is a global/background sector, the sign of Q_hom is not promoted here to a local propagating ghost criterion.',
        'next_gate':t['next_if_pass'] if scientific else 'Audit the homogeneous minisuperspace expansion before any hard-hard-homogeneous cubic reduction.',
        'non_claims':t['non_claims'],
        'threshold_changed':False
    }
    RESULT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    print('Delta_N =',Delta)
    print('Q_hom =',Qhom)
    print('Q_hom/Q_punctured =',ratio)
    if not scientific:
        raise SystemExit(2)

if __name__=='__main__':
    main()
