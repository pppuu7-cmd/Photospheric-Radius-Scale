#!/usr/bin/env python3
"""Diagnose the origin of the frozen C10 ultra-small-k compatibility failure.

This analyzer never reclassifies the parent confirmatory result.  It compares
that persisted baseline with two newly executed precision tiers and separates
integration/time-sampling convergence from interpolation error.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
from pathlib import Path

BASE=[
 'c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime',
 'c10_H0_ord_double_prime','c10_deltaH0_ord','c10_delta_mu_total',
 'c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total','c10_W_total',
 'c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
DIRECT=['c10_Ccom_direct','c10_Ccom_over_k2_direct','c10_dZ_nlde',
        'c10_dZ_prime_nlde','c10_dV_nlde','c10_V_bg_nlde','c10_model2_0i_aux']
ALL=BASE+DIRECT


def median(vals):
    s=sorted(vals)
    if not s:
        raise ValueError('median of empty list')
    n=len(s)
    return s[n//2] if n%2 else 0.5*(s[n//2-1]+s[n//2])


def solve_linear(A,b):
    n=len(b)
    M=[list(map(float,A[i]))+[float(b[i])] for i in range(n)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda r:abs(M[r][col]))
        if abs(M[pivot][col])<1e-300:
            return None
        if pivot!=col:
            M[col],M[pivot]=M[pivot],M[col]
        p=M[col][col]
        for j in range(col,n+1):
            M[col][j]/=p
        for r in range(n):
            if r==col:
                continue
            f=M[r][col]
            if f==0.0:
                continue
            for j in range(col,n+1):
                M[r][j]-=f*M[col][j]
    return [M[i][n] for i in range(n)]


def fit_powers(xs,ys,powers):
    A=[]; b=[]
    for p in powers:
        A.append([sum(x**(p+q) for x in xs) for q in powers])
        b.append(sum(y*x**p for x,y in zip(xs,ys)))
    c=solve_linear(A,b)
    if c is None:
        return None
    pred=[sum(ci*x**p for ci,p in zip(c,powers)) for x in xs]
    return c,pred


def read_table(path):
    txt=Path(path).read_text()
    miss=[x for x in ALL if x not in txt]
    if miss:
        raise RuntimeError(f'missing diagnostic headers {miss} in {path}')
    rows=[]
    for raw in txt.splitlines():
        z=raw.strip()
        if not z or z.startswith('#'):
            continue
        rows.append([float(x) for x in z.split()])
    if not rows:
        raise RuntimeError(f'empty perturbation table {path}')
    n=len(rows[0])
    if any(len(r)!=n for r in rows):
        raise RuntimeError(f'ragged perturbation table {path}')
    tail=[r[-len(ALL):] for r in rows]
    cols={name:[r[i] for r in tail] for i,name in enumerate(ALL)}
    a=[r[1] for r in rows]
    if any(a[i+1]<=a[i] for i in range(len(a)-1)):
        raise RuntimeError(f'non-monotonic scale factor in {path}')
    k=sum(cols['c10_k_Mpc_inv'])/len(rows)
    return {'path':path,'a':a,'k':k,'cols':cols}


def interp_linear(x,y,x0):
    if x0<x[0] or x0>x[-1]:
        raise ValueError(f'{x0} outside {x[0]}..{x[-1]}')
    lo,hi=0,len(x)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if x[m]<=x0:
            lo=m
        else:
            hi=m
    if x0==x[lo]:
        return y[lo]
    if x0==x[hi]:
        return y[hi]
    t=(x0-x[lo])/(x[hi]-x[lo])
    return y[lo]+t*(y[hi]-y[lo])


def interp_local_cubic(x,y,x0):
    if x0<x[0] or x0>x[-1]:
        raise ValueError(f'{x0} outside {x[0]}..{x[-1]}')
    if len(x)<4:
        return interp_linear(x,y,x0)
    # Four nearest points in x, then exact Lagrange interpolation.
    idx=sorted(range(len(x)),key=lambda i:abs(x[i]-x0))[:4]
    idx=sorted(idx)
    xs=[x[i] for i in idx]; ys=[y[i] for i in idx]
    total=0.0
    for i in range(4):
        term=ys[i]
        for j in range(4):
            if i==j:
                continue
            den=xs[i]-xs[j]
            if den==0.0:
                return interp_linear(x,y,x0)
            term*=((x0-xs[j])/den)
        total+=term
    return total


def find_by_k(values,k0):
    return min(values,key=lambda v:abs(v['k']-k0))


def verify_k(values,requested):
    actual=[v['k'] for v in values]
    if len(actual)!=len(requested):
        raise RuntimeError(f'k-count mismatch: {actual} vs {requested}')
    for a,b in zip(actual,requested):
        if abs(a-b)>1e-12*max(1.0,abs(b)):
            raise RuntimeError(f'k mismatch {a} vs {b}')


def epoch_values_from_tables(tabs,a0):
    out=[]
    for t in tabs:
        c=t['cols']['c10_Ccom_direct']
        lin=interp_linear(t['a'],c,a0)
        cub=interp_local_cubic(t['a'],c,a0)
        out.append({'k':t['k'],'C_linear':lin,'C_cubic':cub})
    return sorted(out,key=lambda v:v['k'])


def epoch_values_from_parent(epoch):
    return [
        {'k':float(v['k']),'C_linear':float(v['C_direct']),'C_cubic':None}
        for v in epoch['values']
    ]


def metric_for_interpolator(values,target,key):
    plateau=[find_by_k(values,float(k)) for k in target['plateau_k_Mpc_inv']]
    smallest=[find_by_k(values,float(k)) for k in target['smallest_four_Mpc_inv']]
    smallest8=values[:8]
    xp=[v['k']**2 for v in plateau]
    yp=[v[key] for v in plateau]
    fplat=fit_powers(xp,yp,[1,2])
    if fplat is None:
        raise RuntimeError('singular plateau fit')
    (c2,c4),_=fplat
    residuals=[]
    for v in smallest:
        x=v['k']**2
        pred=c2*x+c4*x*x
        residuals.append(abs(v[key]-pred))
    floor=median(residuals)
    x8=[v['k']**2 for v in smallest8]
    y8=[v[key] for v in smallest8]
    ffree=fit_powers(x8,y8,[0,1,2])
    if ffree is None:
        raise RuntimeError('singular smallest-eight free-intercept fit')
    (c0,c2free,c4free),pred8=ffree
    rms8=math.sqrt(sum((a-b)**2 for a,b in zip(y8,pred8))/len(y8))
    return {
        'plateau_c2':c2,
        'plateau_c4':c4,
        'smallest_four_floor_abs':floor,
        'smallest_four_residuals_abs':residuals,
        'smallest_eight_free_intercept_c0':c0,
        'smallest_eight_free_c2':c2free,
        'smallest_eight_free_c4':c4free,
        'smallest_eight_free_fit_rms_abs':rms8,
    }


def tier_epoch_metrics(values,target,has_cubic):
    linear=metric_for_interpolator(values,target,'C_linear')
    if has_cubic:
        cubic=metric_for_interpolator(values,target,'C_cubic')
        small=[find_by_k(values,float(k)) for k in target['smallest_four_Mpc_inv']]
        interp_metric=median([abs(v['C_linear']-v['C_cubic']) for v in small])
    else:
        cubic=None
        interp_metric=0.0
    return {'linear':linear,'cubic':cubic,'smallest_four_interpolation_abs':interp_metric}


def rel(a,b):
    return abs(a-b)/max(abs(b),1e-300)


def same_nonzero_sign(a,b):
    return a!=0.0 and b!=0.0 and a*b>0.0


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline',required=True)
    ap.add_argument('--ultra-glob',required=True)
    ap.add_argument('--tight-glob',required=True)
    ap.add_argument('--target',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()

    target=json.load(open(args.target))
    parent=json.load(open(args.baseline))
    if parent['classification']!=target['parent_required_classification']:
        raise SystemExit('parent confirmatory classification does not match frozen target')

    requested=[float(x) for x in target['k_ladder_Mpc_inv']]
    ultra_tabs=sorted((read_table(p) for p in glob.glob(args.ultra_glob)),key=lambda z:z['k'])
    tight_tabs=sorted((read_table(p) for p in glob.glob(args.tight_glob)),key=lambda z:z['k'])
    verify_k([{'k':t['k']} for t in ultra_tabs],requested)
    verify_k([{'k':t['k']} for t in tight_tabs],requested)

    parent_by_a={float(e['a']):e for e in parent['core_epochs']}
    parent_early=parent['nonbinding_early_epoch']
    epochs=[]
    numerical_count=0
    physical_count=0

    for a0 in [float(x) for x in target['core_scale_factors']]:
        bvals=epoch_values_from_parent(parent_by_a[a0])
        uvals=epoch_values_from_tables(ultra_tabs,a0)
        tvals=epoch_values_from_tables(tight_tabs,a0)
        verify_k(bvals,requested); verify_k(uvals,requested); verify_k(tvals,requested)
        bm=tier_epoch_metrics(bvals,target,False)
        um=tier_epoch_metrics(uvals,target,True)
        tm=tier_epoch_metrics(tvals,target,True)

        floor_b=bm['linear']['smallest_four_floor_abs']
        floor_u=um['linear']['smallest_four_floor_abs']
        floor_t=tm['linear']['smallest_four_floor_abs']
        c2_rel=rel(tm['linear']['plateau_c2'],um['linear']['plateau_c2'])
        cubic_floor_t=tm['cubic']['smallest_four_floor_abs']
        interp_t=tm['smallest_four_interpolation_abs']
        c0u=um['linear']['smallest_eight_free_intercept_c0']
        c0t=tm['linear']['smallest_eight_free_intercept_c0']
        c0_rel=rel(abs(c0t),abs(c0u))

        numerical=(
            floor_t<=0.5*floor_b and
            c2_rel<=0.05 and
            (cubic_floor_t<=0.5*floor_t or interp_t>=0.25*floor_t)
        )
        physical=(
            floor_u>=0.8*floor_b and
            floor_t>=0.8*floor_u and
            same_nonzero_sign(c0u,c0t) and
            c0_rel<=0.20 and
            abs(c0t)>5.0*interp_t
        )
        numerical_count+=int(numerical)
        physical_count+=int(physical)
        epochs.append({
            'a':a0,
            'baseline':bm,
            'historical_ultra':um,
            'tight_diagnostic':tm,
            'tight_over_baseline_floor_ratio':floor_t/max(floor_b,1e-300),
            'ultra_over_baseline_floor_ratio':floor_u/max(floor_b,1e-300),
            'tight_over_ultra_floor_ratio':floor_t/max(floor_u,1e-300),
            'tight_vs_ultra_plateau_c2_relative_difference':c2_rel,
            'tight_vs_ultra_free_intercept_magnitude_relative_difference':c0_rel,
            'numerical_floor_rule_pass':numerical,
            'physical_residual_rule_pass':physical,
        })

    if numerical_count>=3 and physical_count<3:
        cls=target['classifications']['numerical_floor_supported']
    elif physical_count>=3 and numerical_count<3:
        cls=target['classifications']['precision_stable_physical_residual_supported']
    else:
        cls=target['classifications']['inconclusive']

    # Early epoch is recorded only; it never enters classification.
    aearly=float(target['nonbinding_early_scale_factor'])
    early={
        'a':aearly,
        'baseline':tier_epoch_metrics(epoch_values_from_parent(parent_early),target,False),
        'historical_ultra':tier_epoch_metrics(epoch_values_from_tables(ultra_tabs,aearly),target,True),
        'tight_diagnostic':tier_epoch_metrics(epoch_values_from_tables(tight_tabs,aearly),target,True),
    }

    out={
        'schema':'RTK_C10_SMALL_K_PRECISION_CONVERGENCE_RESULT_v1',
        'classification':cls,
        'parent_confirmatory_classification_retained':parent['classification'],
        'numerical_floor_core_epoch_count':numerical_count,
        'physical_residual_core_epoch_count':physical_count,
        'core_epoch_count':len(epochs),
        'core_epochs':epochs,
        'nonbinding_early_epoch':early,
        'actual_k_values_Mpc_inv':[t['k'] for t in ultra_tabs],
        'completion_parameters_selected':False,
        'production_modified':False,
        'target':args.target,
        'guard':'This result diagnoses convergence only. The parent confirmatory FAIL remains historically and scientifically intact; any new compatibility PASS requires a separately frozen rerun.'
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for e in epochs:
        print('CORE',e['a'],
              'floor ratios u/b=',e['ultra_over_baseline_floor_ratio'],
              't/b=',e['tight_over_baseline_floor_ratio'],
              't/u=',e['tight_over_ultra_floor_ratio'],
              'c2rel=',e['tight_vs_ultra_plateau_c2_relative_difference'],
              'num=',e['numerical_floor_rule_pass'],
              'phys=',e['physical_residual_rule_pass'])


if __name__=='__main__':
    main()
