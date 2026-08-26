#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

LOW_K = [1e-5, 3e-5, 1e-4]
A_FINAL = 0.5


def w_of_a(a: float, closure: dict) -> float:
    x = float(closure['x0']) / (a*a*a)
    lam = float(closure['lambda_D'])
    s = math.hypot(1.0, math.sqrt(lam)*x)
    r = x/s
    t = x/(s+1.0)
    return r*t/(x*(1.0+t))


def transfer(rec: dict) -> tuple[float, float, float, float]:
    k = float(rec['k_Mpc_inv'])
    d1,t1,d2,t2 = [float(x) for x in rec['final_transfer_columns_physical']]
    if not k > 0.0:
        raise RuntimeError('nonpositive k')
    return d1,d2,t1/k,t2/k


def max_abs_diff(a, b):
    return max(abs(x-y) for x,y in zip(a,b))


def log_slope(xs, ys):
    if any((not math.isfinite(y)) or y <= 0.0 for y in ys):
        return None
    lx=[math.log(float(x)) for x in xs]
    ly=[math.log(float(y)) for y in ys]
    mx=sum(lx)/len(lx); my=sum(ly)/len(ly)
    den=sum((x-mx)**2 for x in lx)
    if den == 0.0:
        return None
    return sum((x-mx)*(y-my) for x,y in zip(lx,ly))/den


def dominant_y_charge_alignment(T):
    a,b,c,d=T
    A=a*a+c*c
    B=a*b+c*d
    D=b*b+d*d
    disc=math.hypot(A-D,2.0*B)
    eig=0.5*(A+D+disc)
    if abs(B) > 0.0:
        vx=B; vy=eig-A
    elif A >= D:
        vx=1.0; vy=0.0
    else:
        vx=0.0; vy=1.0
    n=math.hypot(vx,vy)
    return abs(vx/n) if n > 0.0 else float('nan')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    root=Path(__file__).resolve().parents[2]
    target=json.loads((root/'research/theory_targets/RTK_C10_NEUTRAL_CHARGE_PROJECTION_TARGET_v1.json').read_text())
    parent=json.loads((root/'research/theory_results/RTK_C10_NEUTRAL_FINITE_ONSET_MEMORY_RESULT_v1.json').read_text())
    invariant=json.loads((root/'research/theory_results/RTK_C10_NEUTRAL_SHIFT_CHARGE_MEMORY_RESULT_v1.json').read_text())
    theorem=json.loads((root/'research/theory_results/RTK_C10_NEUTRAL_CHARGE_LONG_WAVE_MEMORY_BOUND_RESULT_v1.json').read_text())
    assert target['status']=='FROZEN_BEFORE_EXECUTION'
    assert parent['classification']=='C10_NEUTRAL_FINITE_ONSET_MEMORY_RETAINED_OR_AMPLIFIED_SCOPED'
    assert invariant['classification']=='C10_NEUTRAL_SHIFT_CHARGE_MEMORY_INVARIANT_PASS_SCOPED'
    assert theorem['classification']=='C10_NEUTRAL_CHARGE_LONG_WAVE_FINITE_TIME_MEMORY_BOUND_PASS_SCOPED'

    closure=parent['khronon_reconstruction']
    a_i=float(parent['production_reference']['a_on'])
    H_EFT=float(parent['production_reference']['H_EFT_max_Mpc_inv'])
    wi=w_of_a(a_i,closure); wf=w_of_a(A_FINAL,closure)

    groups={}
    for rec in parent['records']:
        k=float(rec['k_Mpc_inv']); lam=float(rec['lambda_HL'])
        key=(round(k,14),round(lam,14))
        groups.setdefault(key,[]).append(rec)

    max_mc_diff=0.0
    unique={}
    for key,recs in groups.items():
        Ts=[transfer(r) for r in recs]
        ref=Ts[0]
        for T in Ts[1:]:
            max_mc_diff=max(max_mc_diff,max_abs_diff(ref,T))
        unique[key]=recs[0]

    lambdas=sorted(set(float(r['lambda_HL']) for r in unique.values()))
    per_lambda=[]
    all_finite=True
    all_trends=True
    min_pq=float('inf'); min_pu=float('inf')

    for lam in lambdas:
        rows=[]
        for k in LOW_K:
            candidates=[r for (key,r) in unique.items()
                        if abs(float(r['lambda_HL'])-lam) <= 1e-13*max(1.0,abs(lam))
                        and abs(float(r['k_Mpc_inv'])-k) <= 1e-13*max(1.0,abs(k))]
            if len(candidates)!=1:
                raise RuntimeError(f'expected one unique record for k={k}, lambda={lam}; got {len(candidates)}')
            rec=candidates[0]
            T=transfer(rec)
            RQ=T[0]*(1.0+wi)/(1.0+wf)
            LQV=T[1]/(1.0+wf)
            LQU=(k/H_EFT)*LQV
            align=dominant_y_charge_alignment(T)
            vals=(RQ,LQV,LQU,align)+T
            if not all(math.isfinite(x) for x in vals): all_finite=False
            rows.append({
                'k_Mpc_inv':k,
                'R_Q_pure_charge':RQ,
                'abs_R_Q_minus_1':abs(RQ-1.0),
                'L_QV_Y_velocity_to_charge':LQV,
                'L_QU_regular_velocity_to_charge':LQU,
                'abs_L_QU':abs(LQU),
                'dominant_Y_singular_vector_charge_axis_alignment_abs':align,
                'T_Y':[[T[0],T[1]],[T[2],T[3]]]
            })
        dq=[r['abs_R_Q_minus_1'] for r in rows]
        du=[r['abs_L_QU'] for r in rows]
        pq=log_slope(LOW_K,dq); pu=log_slope(LOW_K,du)
        trend_q=(dq[0] < dq[1] < dq[2])
        trend_u=(du[0] < du[1] < du[2])
        slope_q=(pq is not None and pq>1.5)
        slope_u=(pu is not None and pu>1.5)
        ok=trend_q and trend_u and slope_q and slope_u
        all_trends = all_trends and ok
        if pq is not None: min_pq=min(min_pq,pq)
        if pu is not None: min_pu=min(min_pu,pu)
        per_lambda.append({
            'lambda_HL':lam,
            'low_k_records':rows,
            'p_Q_loglog':pq,
            'p_U_loglog':pu,
            'charge_deviation_monotone_to_zero_as_k_decreases':trend_q,
            'regular_velocity_leakage_monotone_to_zero_as_k_decreases':trend_u,
            'slope_conditions_pass':slope_q and slope_u,
            'classification_conditions_pass':ok
        })

    technical=(not all_finite) or max_mc_diff>1e-12
    if technical:
        cls='C10_NEUTRAL_CHARGE_PROJECTION_TECHNICAL_FAIL'
    elif all_trends:
        cls='C10_NEUTRAL_CHARGE_PROJECTION_RETENTION_PASS_SCOPED'
    else:
        cls='C10_NEUTRAL_CHARGE_PROJECTION_INCONCLUSIVE_SCOPED'

    out={
        'schema':'RTK_C10_NEUTRAL_CHARGE_PROJECTION_RESULT_v1',
        'classification':cls,
        'target':'research/theory_targets/RTK_C10_NEUTRAL_CHARGE_PROJECTION_TARGET_v1.json',
        'parents':target['parents'],
        'coordinate_statement':{
            'fixed_difference_subspace':'Delta psi_pref=0, hence I_khr=delta/(1+w)',
            'Y':'(delta,theta/k)',
            'regular_velocity':'U=H_EFT*theta/k^2',
            'warning':'A unit Y velocity basis has theta=O(k), so its singular norm is not the regular theta=O(k^2) long-wave family.'
        },
        'background_reconstruction':{
            'a_i':a_i,'a_f':A_FINAL,'w_i':wi,'w_f':wf,'H_EFT_Mpc_inv':H_EFT,
            'closure':closure
        },
        'diagnostics':{
            'all_finite':all_finite,
            'max_M_c_duplicate_transfer_abs_difference':max_mc_diff,
            'unique_k_lambda_count':len(unique),
            'lambda_count':len(lambdas),
            'minimum_p_Q_loglog':None if min_pq==float('inf') else min_pq,
            'minimum_p_U_loglog':None if min_pu==float('inf') else min_pu,
            'all_preregistered_asymptotic_conditions_pass':all_trends
        },
        'per_lambda':per_lambda,
        'interpretation':('On the fixed-ordinary C10.62b difference subspace, pure neutral charge is tested directly rather than through the coordinate norm Y. The regular velocity family rescales the Y velocity basis by k/H_EFT, enforcing theta=O(k^2). A scoped pass confirms the numerical low-k transfer approaches the exact finite-time charge-memory theorem; it does not establish full coupled cosmological initial-condition uniqueness.'),
        'next_gate':('Freeze a pre-EFT/UV neutral-charge boundary prescription (for example a declared I_khr value, without claiming a dynamical mechanism), then implement the photon+baryon+massless-UR dual-interface growing/decaying-mode test. Keep C9 radiative protection independent and open.'),
        'non_claims':target['non_claims']
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps(out['diagnostics'],sort_keys=True))


if __name__=='__main__':
    main()
