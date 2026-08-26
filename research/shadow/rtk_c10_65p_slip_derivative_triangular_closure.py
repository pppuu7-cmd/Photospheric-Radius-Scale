#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
def load(p): return json.loads((ROOT/p).read_text())

def main():
    t=load('research/theory_targets/RTK_C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_TARGET_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    d=load('research/theory_results/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_RESULT_v1.json')
    rtrip=load('research/theory_results/RTK_C10_PREFERRED_DAE_NEWTONIAN_ROUNDTRIP_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    assert d['classification']=='C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_PASS_SCOPED'
    assert rtrip['classification']=='C10_PREFERRED_DAE_NEWTONIAN_ROUNDTRIP_PASS_CHI_NOT_INDEPENDENT_EVOLUTION_SCOPED'

    R,Wb,k2,a=sp.symbols('R W_b k2 a', positive=True, finite=True)
    slip=sp.symbols('slip', finite=True)
    cb=R/(1+R); cg=-1/(1+R); Wg=R*Wb
    aggregate=sp.simplify(Wb*cb+Wg*cg)
    assert aggregate==0
    q0prime_coeff=sp.simplify(a/k2*aggregate)
    hhat2_coeff=sp.simplify(-k2/a*q0prime_coeff)
    assert q0prime_coeff==0 and hhat2_coeff==0

    H,Fc,cb2,dtau,tau,Fp,App,Phi,Psip=sp.symbols('H F cb2 dtau tau Fprime App Phi PsiNprime', finite=True)
    th,mc,dg,sg,sgp,thp=sp.symbols('theta metric_continuity delta_g sigma_g sigma_g_prime theta_prime', finite=True)
    first=Fc*(-App*th+k2*(-H*dg/sp.Integer(2)+cb2*(-th-mc)-sp.Rational(4,3)*(-th-mc)/4)-H*k2*Phi)
    # zero relative velocity eliminates the prefactor multiplying theta_b-theta_g.
    firstPsi=sp.expand(first.subs(mc,-3*Psip))
    comp=(1-2*H*Fc)*firstPsi + Fc*k2*(2*H*sg+sgp-(sp.Rational(1,3)-cb2)*(Fc*thp+2*Fp*th))
    coeff=sp.factor(sp.diff(comp,Psip))
    expected=sp.factor(-(1-2*H*Fc)*Fc*k2*(1-3*cb2))
    residual=sp.simplify(coeff-expected)
    assert residual==0

    pack=f['coefficient_pack']; Hn=float(pack['Hc_Mpc_inv']); Fn=float(pack['F_Mpc']); cbn=float(pack['cb2'])
    pref=1.0-2.0*Hn*Fn
    anchors=[float(x) for x in f['exact_anchor']['k_Mpc_inv']]
    records=[]
    for k in anchors:
        c=-(pref)*Fn*k*k*(1.0-3.0*cbn)
        records.append({'k_Mpc_inv':k,'d_slip_d_PsiNprime':c,'abs_coefficient':abs(c)})
    maxc=max(x['abs_coefficient'] for x in records)
    assert pref!=0.0 and all(sp.Float(x['d_slip_d_PsiNprime']).is_finite for x in records)

    cls='C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_PASS_SCOPED'
    out={
      'schema':'RTK_C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_RESULT_v1','gate':'C10.65p','classification':cls,
      'target':'research/theory_targets/RTK_C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_TARGET_v1.json',
      'source_lock':{'class_upstream_sha':d['pinned_upstream']['sha'],'perturbations_c_sha256':d['audited_source_hashes_sha256']['source/perturbations.c'],'tca':'compromise_CLASS'},
      'exact_aggregate_cancellation':{
        'baryon_slip_coefficient':'R/(1+R)','photon_slip_coefficient':'-1/(1+R)','W_gamma':'R W_b',
        'weighted_momentum_slip_coefficient':str(aggregate),'q0_N_prime_slip_coefficient':str(q0prime_coeff),'hhat_double_prime_slip_coefficient':str(hhat2_coeff),
        'consequence':'internal Thomson slip redistributes photon-baryon momentum but does not source the aggregate ordinary momentum derivative consumed by the completed-U1 projector derivative.'
      },
      'exact_slip_affinity':{
        'metric_continuity':'-3 Psi_N_prime','coefficient':str(coeff),'expected':'-(1-2 H F) F k^2 (1-3 cb2)','machine_residual':str(residual),
        'why_no_other_PsiNprime_terms':'theta_prime, photon shear and shear_prime in the pinned flat-Newtonian compromise correction use metric_euler/metric_shear but not metric_continuity; at the matching point theta_b=theta_g the separate relative-velocity prefactor vanishes.'
      },
      'onset_numeric_coefficients':{'one_minus_2HF':pref,'records':records,'max_abs_d_slip_d_PsiNprime':maxc},
      'roundtrip_certificate':{'chi_prime_status':rtrip['exact_roundtrip']['chi_prime_shadow'],'temporal_B_initial_condition_required':rtrip['preferred_projection']['temporal_B_initial_condition_required'],'interpretation':'B_prime is d/dtau of the algebraic preferred projector along the local source trajectory; it is not a ninth/tenth initial datum.'},
      'triangular_execution_order':[
        'evaluate the local aggregate ordinary+neutral RHS and background derivatives at the C10.65o conditional seed',
        'differentiate the algebraic completed-U1 projector to obtain B_prime; the aggregate derivative is slip-free by the exact cancellation above',
        'compute Psi_N_prime=psi_pref_prime-H_prime B-H B_prime',
        'evaluate the pinned compromise_CLASS slip using that Psi_N_prime',
        'recover individual theta_b_prime and theta_g_prime; their slip pieces cancel again in the aggregate momentum channel'
      ],
      'remaining_numeric_inputs':'C10.65q must provide H_prime/background derivatives and the aggregate ordinary+neutral derivative pack needed for d/dtau of the algebraic projector. These are local RHS/background data, not temporal boundary data.',
      'architecture_decision':'Do not solve B_prime and slip as two new dynamical states and do not set either derivative to zero. The closure is triangular because Thomson slip is internal to the photon-baryon aggregate momentum.',
      'next_gate':t['next_if_pass'],'non_claims':t['non_claims']
    }
    (ROOT/'research/theory_results/RTK_C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'one_minus_2HF':pref,'max_abs_d_slip_d_PsiNprime':maxc,'aggregate_slip_coefficient':str(aggregate)},sort_keys=True))
if __name__=='__main__': main()
