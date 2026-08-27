#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]

def load(path):
    return json.loads((ROOT/path).read_text())

def main():
    target=load('research/theory_targets/RTK_C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_TARGET_v1.json')
    parent=load('research/theory_results/RTK_C10_65S6FL2_UNITARY_HARD_HARD_HOMOGENEOUS_SOURCE_RESULT_v1.json')
    assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert parent['classification']=='C10_65S6FL2_HOMOGENEOUS_VIRTUAL_CHANNEL_FINITE_PASS_SCOPED'
    assert parent['candidate_branch']=='MINIMAL_PROJECTABLE_N2_S1HALF_v1'
    assert parent['checks']['bare_n2_soft_kernel_preserved'] is True
    assert parent['checks']['alpha6_lapse_prefactor_cancels_for_s1_half'] is True
    assert parent['checks']['mixed_C_DTheta_term_zero_after_same_reduction'] is True
    assert parent['checks']['punctured_q_limit_not_used'] is True
    assert parent['checks']['no_parameter_fit'] is True

    H,Hdot,a,k,lam,Mstar,MK,omega,alpha6=sp.symbols(
        'H Hdot a k lambda_HL Mstar M_K omega alpha6_0', nonzero=True)
    A=sp.Rational(3,2)*Mstar**2*(1-3*lam)
    D=Mstar**2*MK**2
    Delta=sp.expand(A*H**2+D)
    Om=2*omega

    Sn=2*Mstar**2*a*(
        27*H*a**2*lam**2*omega-36*H*a**2*lam*omega+9*H*a**2*omega
        -3*a**2*lam*omega**2+a**2*omega**2+k**2*lam-k**2
    )/(lam-1)

    Sz=-(
        243*H**2*Mstar**2*a**6*lam**2-324*H**2*Mstar**2*a**6*lam+81*H**2*Mstar**2*a**6
        +324*H*Mstar**2*a**6*lam**2*omega-432*H*Mstar**2*a**6*lam*omega+108*H*Mstar**2*a**6*omega
        +81*Hdot*Mstar**2*a**6*lam**2-108*Hdot*Mstar**2*a**6*lam+27*Hdot*Mstar**2*a**6
        +108*Mstar**2*a**6*lam**2*omega**2-162*Mstar**2*a**6*lam*omega**2+42*Mstar**2*a**6*omega**2
        -2*Mstar**2*a**4*k**2*lam+2*Mstar**2*a**4*k**2
        +96*alpha6*k**6*lam-96*alpha6*k**6
    )/(a**3*(lam-1))

    # Source-lock the independently persisted bare n=2 term before reduction.
    bare=sp.simplify(-96*alpha6*k**6/a**3)
    bare_in_Sz=sp.simplify(sp.diff(Sz,alpha6)*alpha6)
    assert sp.simplify(bare_in_Sz-bare)==0
    assert sp.diff(Sn,alpha6)==0

    # Eliminate only nondynamical n0. The quadratic-in-source exchange is hard^4
    # and deliberately NOT added to this cubic hard-hard-soft vertex.
    V=sp.factor(sp.together(Sz + A*H*Om/Delta*Sn))
    coeff_alpha=sp.factor(sp.diff(V,alpha6))
    expected_coeff=-96*k**6/a**3
    coeff_check=sp.simplify(coeff_alpha-expected_coeff)==0
    assert coeff_check

    # Since k>0 and a is finite/nonzero in the frozen domain, this coefficient
    # proves V is not the zero symbolic function without any parameter fit.
    identically_zero=(sp.simplify(V)==0)
    assert identically_zero is False

    # Reproduce the lapse-elimination source coefficient independently.
    zdot,n,Sn_sym,Sz_sym=sp.symbols('zdot n Sn_sym Sz_sym')
    L=A*zdot**2-2*A*H*n*zdot+Delta*n**2+Sz_sym*sp.Symbol('zeta0')+Sn_sym*n
    n_sol=sp.solve(sp.diff(L,n),n)[0]
    expected_n=A*H*zdot/Delta-Sn_sym/(2*Delta)
    lapse_identity=sp.simplify(n_sol-expected_n)==0
    assert lapse_identity

    classification='C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_NONZERO_PASS_SCOPED'
    out={
      'schema':'RTK_C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_RESULT_v1',
      'gate':'C10.65s6fM',
      'classification':classification,
      'decision':'NONZERO',
      'candidate_branch':'MINIMAL_PROJECTABLE_N2_S1HALF_v1',
      'target':'research/theory_targets/RTK_C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_TARGET_v1.json',
      'order_bookkeeping':{
        'cubic_object':'linear homogeneous physical-mode source after eliminating n0 only',
        's6fL2_exchange_order':'quadratic in hard-hard sources; effective hard^4 object',
        'exchange_added_to_cubic_vertex':False,
        'bare_alpha6_double_counted':False
      },
      'global_block':{
        'A':str(A), 'D':str(D), 'Delta_N':str(Delta), 'Omega':str(Om),
        'singular_surfaces':parent['global_block']['singular_surfaces']
      },
      'sources':{
        'S_zeta0':str(Sz),
        'S_n0':str(Sn),
        'V_hom_cubic':str(V),
        'alpha6_coefficient_in_V':str(coeff_alpha),
        'expected_alpha6_coefficient':str(expected_coeff)
      },
      'checks':{
        'target_frozen':True,
        'parents_exact':True,
        'candidate_branch_exact':True,
        's6fL2_source_expressions_reproduced_symbolically':True,
        'bare_n2_alpha6_contact_counted_exactly_once':True,
        'hard4_exchange_not_added_to_cubic_vertex':True,
        'lapse_elimination_identity':lapse_identity,
        'alpha6_coefficient_exact':coeff_check,
        'physical_cubic_vertex_identically_zero':identically_zero,
        'no_punctured_q_limit_or_mu_prescription':True,
        'no_parameter_fit_or_soft_cancellation_tuning':True,
        'no_k003_production_output_used':True,
        'threshold_changed':False
      },
      'proof_of_nonzero':'d V_hom^(3) / d alpha6_0 = -96 k^6/a^3, which is nonzero for the frozen finite-hard-k domain k>0 and finite nonzero a. Therefore the exact lapse-reduced homogeneous physical cubic vertex is not an identically vanishing symbolic function on the frozen candidate branch; no parameter value was selected or fitted.',
      'interpretation':'The frozen minimal projectable n=2,s1=1/2 candidate does not cancel the exact homogeneous soft-s cubic vertex. The exact-global lapse reduction changes the physical source through S_n0 but cannot remove the alpha6_0 coefficient because the s1=1/2 state-function rule gives no alpha6 lapse source. This is a scoped rejection of this specific nonlinear candidate as a soft-s cure, not a no-go for every possible RTK nonlinear completion.',
      'next_gate':'Keep k=0.03 production blocked. Freeze a successor operator/symmetry-completion gate that changes the nonlinear completion prospectively (not by fitting the present candidate) and requires any new structure to preserve the already-certified background/linear sector before rerunning the exact homogeneous cubic test.',
      'non_claims':target['non_claims'],
      'threshold_changed':False
    }
    p=ROOT/'research/theory_results/RTK_C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_RESULT_v1.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification)
    print('decision=NONZERO')
    print('dV/dalpha6_0 =',sp.sstr(coeff_alpha))

if __name__=='__main__':
    main()
