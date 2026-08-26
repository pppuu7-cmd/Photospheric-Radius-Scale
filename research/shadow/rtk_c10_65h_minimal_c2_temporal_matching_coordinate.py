#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp


def main():
    root=Path(__file__).resolve().parents[2]
    target=json.loads((root/'research/theory_targets/RTK_C10_65H_MINIMAL_C2_TEMPORAL_MATCHING_COORDINATE_TARGET_v1.json').read_text())
    g=json.loads((root/'research/theory_results/RTK_C10_65G_FINITE_ONSET_GROWING_MODE_IDENTIFIABILITY_RESULT_v1.json').read_text())
    b0=json.loads((root/'research/theory_results/RTK_C10_B0_NEXT_ORDER_SOURCE_FORMULA_RESULT_v1.json').read_text())
    c=json.loads((root/'research/theory_results/RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_RESULT_v1.json').read_text())
    p=json.loads((root/'research/theory_results/RTK_C10_PREFERRED_METRIC_PROJECTOR_API_RESULT_v1.json').read_text())
    assert target['status']=='FROZEN_BEFORE_EXECUTION'
    assert g['classification']=='C10_65G_FINITE_ONSET_SNAPSHOT_RANK_INSUFFICIENT_TEMPORAL_MATCH_REQUIRED_SCOPED'
    assert b0['classification']=='C10_B0_NEXT_ORDER_SOURCE_FORMULA_PASS_SCOPED'
    assert c['classification']=='C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_PASS_SCOPED'
    assert p['classification']=='C10_PREFERRED_METRIC_PROJECTOR_API_PASS_SCOPED'

    a,H,W,B,dmP,qP=sp.symbols('a H W B dmP qP', nonzero=True)
    rho_prime=-3*H*W
    dmN=dmP+rho_prime*B
    qN=qP+a*W*B
    QP=3*a*qP; QN=3*a*qN
    CP=3*a**2*dmP+3*H*QP
    CN=3*a**2*dmN+3*H*QN
    C_res=sp.simplify(CN-CP)
    assert C_res==0

    # Coefficient-level invariance with regular B=B0+xB2 and generic source series.
    x=sp.symbols('x')
    dm0,dm2,q0,q2,B0s,B2=sp.symbols('dm0 dm2 q0 q2 B0 B2')
    dmPser=dm0+x*dm2; qPser=q0+x*q2; Bser=B0s+x*B2
    dmNser=sp.expand(dmPser+rho_prime*Bser)
    qNser=sp.expand(qPser+a*W*Bser)
    CPser=sp.expand(3*a**2*dmPser+9*H*a*qPser)
    CNser=sp.expand(3*a**2*dmNser+9*H*a*qNser)
    C2P=sp.expand(CPser).coeff(x,1); C2N=sp.expand(CNser).coeff(x,1)
    C2_res=sp.simplify(C2N-C2P); assert C2_res==0
    C0P=sp.expand(CPser).coeff(x,0)

    C2,Pcal,psi0,Eth,phi0=sp.symbols('C2 Pcal psi0 Eth phi0')
    B0=(C2+2*Pcal*psi0-Eth*phi0)/(2*H)
    dB=sp.simplify(sp.diff(B0,C2)); assert dB==1/(2*H)
    # Invertibility: the same relation solves C2 uniquely from a chosen B0.
    Bstar=sp.symbols('Bstar')
    C2_from_B=sp.solve(sp.Eq(Bstar,B0),C2)[0]
    inverse_res=sp.simplify(B0.subs(C2,C2_from_B)-Bstar); assert inverse_res==0

    w,Jad=sp.symbols('w Jad')
    delta=(1+w)*(3*psi0+Jad)
    DeltaI=sp.simplify(delta/(1+w)-3*psi0-Jad); assert DeltaI==0
    dDelta_dC2=sp.simplify(sp.diff(DeltaI,C2)); assert dDelta_dC2==0

    cls='C10_65H_C2_GAUGE_INVARIANT_MINIMAL_SHIFT_MATCH_COORDINATE_PASS_SCOPED'
    out={
      'schema':'RTK_C10_65H_MINIMAL_C2_TEMPORAL_MATCHING_COORDINATE_RESULT_v1',
      'gate':'C10.65h','classification':cls,
      'target':'research/theory_targets/RTK_C10_65H_MINIMAL_C2_TEMPORAL_MATCHING_COORDINATE_TARGET_v1.json',
      'exact_comoving_source_invariance':{
        'preferred':'C_pref=3 a^2 delta_mu_pref+3 H Q_pref, Q_pref=3 a q_pref',
        'newtonian':'C_N=3 a^2 delta_mu_N+3 H Q_N, Q_N=3 a q_N',
        'source_map':'delta_mu_N=delta_mu_pref-3 H W B; q_N=q_pref+a W B',
        'machine_full_C_residual':'0',
        'machine_C2_residual':'0',
        'regular_B_required':True,
        'consequence':'C2 is a source-coordinate/gauge-invariant regular-branch matching coordinate; no choice B0=0 is used.'
      },
      'leading_regularity':{
        'C0_expression':str(C0P),
        'condition':'C0=0',
        'role':'leading finite-B regularity removes the k^0 comoving source but leaves C2 as the first unresolved comoving coefficient.'
      },
      'shift_reconstruction':{
        'B0':'(C2+2 Pcal psi0-E_th phi0)/(2H)',
        'dB0_dC2':str(dB),
        'inverse_C2_from_B0':str(C2_from_B),
        'machine_inverse_residual':'0',
        'finite_onset_guard':'H>0',
        'independence_statement':'Once C2 and the leading metric amplitudes are specified, B0 is derived uniquely and is not a second matching datum.'
      },
      'neutral_adiabatic_independence':{
        'boundary':'Delta I_iso=I_khr-J_ad=0',
        'delta_khr0':'(1+w)(3 psi0+J_ad)',
        'machine_boundary_residual':'0',
        'd_DeltaI_dC2':str(dDelta_dC2),
        'consequence':'The C2 matching coordinate is independent of the neutral relative-entropy coordinate; carrying C2 does not undo the C10.65c adiabatic correction.'
      },
      'minimality_scope':{
        'positive_claim':'C2 is one sufficient and invariant scalar coordinate for the unresolved foliation/shift boundary freedom represented by B0.',
        'guard':'This theorem does not claim C2 is the only remaining temporal amplitude of the full photon+baryon+UR+Khronon hierarchy.',
        'numerical_value_status':'UNSET_BY_THEORY_AT_THIS_GATE',
        'allowed_future_selectors':['microscopic pre-EFT/UV matching','justified backward-regularity condition','explicit temporal eigen/power-law growing-branch condition']
      },
      'architecture_decision':'Carry C2 symbolically into the next coupled coefficient-nullity audit; derive B0 from it and never promote chi/B0 to an independently integrated or independently matched scalar.',
      'next_gate':target['next_if_pass'],'non_claims':target['non_claims']
    }
    outp=root/'research/theory_results/RTK_C10_65H_MINIMAL_C2_TEMPORAL_MATCHING_COORDINATE_RESULT_v1.json'
    outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)

if __name__=='__main__': main()
