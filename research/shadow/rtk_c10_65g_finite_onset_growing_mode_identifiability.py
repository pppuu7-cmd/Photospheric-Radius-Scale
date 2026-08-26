#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp


def exact_rank_examples():
    cases=[]
    As=[
      sp.Matrix([[1,0,0],[0,1,0]]),
      sp.Matrix([[1,2,3],[2,4,6]]),
      sp.Matrix([[1,0,0],[0,1,0],[0,0,1],[1,1,1]]),
      sp.Matrix.zeros(0,3),
    ]
    Fs=[
      sp.Matrix([[1,2,0],[0,3,4],[5,0,6]]),
      sp.Matrix([[sp.Rational(1,2),-2,1],[3,sp.Rational(2,3),0],[1,4,-1]]),
    ]
    for ia,A in enumerate(As):
        n=A.cols; I=sp.eye(n); Z=sp.zeros(A.rows,n)
        for jf,F in enumerate(Fs):
            M=A.row_join(Z).col_join((-F).row_join(I))
            P=I.row_join(sp.zeros(n,n)).col_join(F.row_join(I))
            target=A.row_join(Z).col_join(sp.zeros(n,n).row_join(I))
            resid=sp.simplify(M*P-target)
            assert resid==sp.zeros(A.rows+n,2*n)
            assert sp.det(P)==1
            rankA=A.rank(); rankM=M.rank(); nullA=n-rankA; nullM=2*n-rankM
            assert rankM==rankA+n
            assert nullM==nullA
            cases.append({'A_case':ia,'F_case':jf,'n':n,'m':A.rows,'rank_A':rankA,'rank_augmented':rankM,'nullity_A':nullA,'nullity_augmented':nullM,'det_P':'1'})
    return cases


def main():
    root=Path(__file__).resolve().parents[2]
    target=json.loads((root/'research/theory_targets/RTK_C10_65G_FINITE_ONSET_GROWING_MODE_IDENTIFIABILITY_TARGET_v1.json').read_text())
    p65f=json.loads((root/'research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json').read_text())
    p65c=json.loads((root/'research/theory_results/RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_RESULT_v1.json').read_text())
    p54=json.loads((root/'research/theory_results/RTK_C10_FINITE_ONSET_ADIABATIC_INVARIANCE_RESULT_v1.json').read_text())
    p55=json.loads((root/'research/theory_results/RTK_C10_B0_NEXT_ORDER_SOURCE_FORMULA_RESULT_v1.json').read_text())
    p62=json.loads((root/'research/theory_results/RTK_C10_NEUTRAL_FINITE_ONSET_MEMORY_RESULT_v1.json').read_text())
    p63=json.loads((root/'research/theory_results/RTK_C10_NEUTRAL_CHARGE_PROJECTION_RESULT_v1.json').read_text())
    proj=json.loads((root/'research/theory_results/RTK_C10_PREFERRED_METRIC_PROJECTOR_API_RESULT_v1.json').read_text())
    assert target['status']=='FROZEN_BEFORE_EXECUTION'
    assert p65f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
    assert p65c['classification']=='C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_PASS_SCOPED'
    assert p54['classification']=='C10_FINITE_ONSET_ADIABATIC_INVARIANCE_PASS_UV_OR_GROWING_MODE_MATCH_REQUIRED_SCOPED'
    assert p55['classification']=='C10_B0_NEXT_ORDER_SOURCE_FORMULA_PASS_SCOPED'
    assert p62['classification']=='C10_NEUTRAL_FINITE_ONSET_MEMORY_RETAINED_OR_AMPLIFIED_SCOPED'
    assert p63['classification']=='C10_NEUTRAL_CHARGE_PROJECTION_RETENTION_PASS_SCOPED'
    assert proj['classification']=='C10_PREFERRED_METRIC_PROJECTOR_API_PASS_SCOPED'

    # Exact generic 2x2 symbolic block identity.
    a11,a12,a21,a22=sp.symbols('a11 a12 a21 a22')
    f11,f12,f21,f22=sp.symbols('f11 f12 f21 f22')
    A=sp.Matrix([[a11,a12],[a21,a22]])
    F=sp.Matrix([[f11,f12],[f21,f22]])
    I=sp.eye(2); Z=sp.zeros(2,2)
    M=A.row_join(Z).col_join((-F).row_join(I))
    P=I.row_join(Z).col_join(F.row_join(I))
    D=A.row_join(Z).col_join(Z.row_join(I))
    block_residual=sp.simplify(M*P-D)
    assert block_residual==sp.zeros(4,4)
    detP=sp.factor(P.det()); assert detP==1

    cases=exact_rank_examples()

    C2,Pcal,psi0,Eth,phi0,H=sp.symbols('C2 Pcal psi0 Eth phi0 H', nonzero=True)
    B0=(C2+2*Pcal*psi0-Eth*phi0)/(2*H)
    dB_dC2=sp.simplify(sp.diff(B0,C2)); assert dB_dC2==1/(2*H)

    w,Jad=sp.symbols('w Jad')
    delta_khr0=(1+w)*(3*psi0+Jad)
    ddelta_dC2=sp.simplify(sp.diff(delta_khr0,C2)); assert ddelta_dC2==0
    DeltaI=sp.simplify(delta_khr0/(1+w)-3*psi0-Jad); assert DeltaI==0

    classification='C10_65G_FINITE_ONSET_SNAPSHOT_RANK_INSUFFICIENT_TEMPORAL_MATCH_REQUIRED_SCOPED'
    out={
      'schema':'RTK_C10_65G_FINITE_ONSET_GROWING_MODE_IDENTIFIABILITY_RESULT_v1',
      'gate':'C10.65g','classification':classification,
      'target':'research/theory_targets/RTK_C10_65G_FINITE_ONSET_GROWING_MODE_IDENTIFIABILITY_TARGET_v1.json',
      'exact_block_rank_theorem':{
        'snapshot_matrix':'M=[[A,0],[-F,I_n]]',
        'invertible_column_transform':'P=[[I_n,0],[F,I_n]]',
        'identity':'M P = diag(A,I_n)',
        'det_P':str(detP),
        'machine_symbolic_block_residual':'0',
        'consequence':'rank(M)=rank(A)+n and nullity(M)=nullity(A); local first-order evolution fixes derivatives for admissible initial states but does not select a growing initial-state direction at one time.'
      },
      'exact_rational_rank_checks':cases,
      'B0_temporal_datum':{
        'formula':'B0=(C2+2 Pcal psi0-E_th phi0)/(2H)',
        'dB0_dC2':str(dB_dC2),
        'finite_onset_guard':'H>0',
        'interpretation':'C2 remains a genuine next-order boundary/history datum until a temporal branch condition is supplied; changing C2 changes B0 with nonzero coefficient.'
      },
      'corrected_adiabatic_boundary':{
        'Delta_I_iso':'I_khr-J_ad=0',
        'delta_khr0':'(1+w)(3 psi0+J_ad)',
        'machine_Delta_I_iso_residual':'0',
        'd_delta_khr0_dC2':str(ddelta_dC2),
        'interpretation':'The corrected common-curvature boundary removes the neutral relative-entropy amplitude but is independent of C2 and therefore does not select the global temporal growing/decaying branch.'
      },
      'parent_consistency':{
        'finite_onset_adiabaticity':'C10.54 already requires UV/growing-mode matching for C2/B0',
        'neutral_memory':'C10.62/C10.63 exclude relying on generic finite-time EFT memory loss as the missing branch selector',
        'metric_projector':'preferred algebraic A->H->M projection removes chi as an independent integrated state but does not provide a temporal boundary functional'
      },
      'architecture_decision':{
        'forbidden':'Do not claim unique growing-mode initial conditions by stacking instantaneous ODE RHS equations into a snapshot rank matrix.',
        'required':'Add an explicit temporal condition: a pre-EFT/UV matching functional, a justified backward-regularity prescription, or a frozen temporal eigen/power-law branch condition. Only then solve the corrected coupled O(k^2) coefficient system.',
        'model_status':'This is a boundary-identifiability limitation, not a model no-go and not a propagating-DOF theorem.'
      },
      'next_gate':target['next_if_pass'],'non_claims':target['non_claims']
    }
    p=root/'research/theory_results/RTK_C10_65G_FINITE_ONSET_GROWING_MODE_IDENTIFIABILITY_RESULT_v1.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification)

if __name__=='__main__': main()
