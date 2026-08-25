#!/usr/bin/env python3
"""Exploratory C10 small-k scaling diagnostic on physical RT-CLASS exports.

This script does not select completion parameters and does not return a
scientific PASS/FAIL.  It measures the production source combination

    C_com = delta_mu_CLASS + 3 Hc * rpp_theta_CLASS / k^2

at common scale factors.  For fixed finite M_c and finite chi, C_com=O(k^2)
is a necessary compatibility condition for the completed-U1 regularity
bracket, but the present frozen target is explicitly diagnostic-only.
"""
from __future__ import annotations

import argparse
import glob
import json
import math
from pathlib import Path

DIAG = [
    "c10_k_Mpc_inv", "c10_Hc", "c10_Hc_prime", "c10_H0_ord",
    "c10_H0_ord_prime", "c10_H0_ord_double_prime", "c10_deltaH0_ord",
    "c10_delta_mu_total", "c10_rpp_theta_total", "c10_delta_p_total",
    "c10_rpp_shear_total", "c10_W_total", "c10_rho_total_prime",
    "c10_p_total_prime", "c10_khr_w", "c10_khr_ca2",
]


def read_table(path):
    text=Path(path).read_text()
    missing=[x for x in DIAG if x not in text]
    if missing:
        raise RuntimeError(f"missing diagnostic headers in {path}: {missing}")
    rows=[]
    for raw in text.splitlines():
        line=raw.strip()
        if not line or line.startswith('#'):
            continue
        vals=[float(x) for x in line.split()]
        rows.append(vals)
    if not rows:
        raise RuntimeError(f"empty numeric table {path}")
    n=len(rows[0])
    if any(len(r)!=n for r in rows):
        raise RuntimeError(f"ragged table {path}")
    tail=[r[-len(DIAG):] for r in rows]
    cols={name:[r[i] for r in tail] for i,name in enumerate(DIAG)}
    a=[r[1] for r in rows]
    if any(a[i+1] <= a[i] for i in range(len(a)-1)):
        raise RuntimeError(f"scale factor is not strictly increasing in {path}")
    k=sum(cols['c10_k_Mpc_inv'])/len(rows)
    if k<=0:
        raise RuntimeError(f"non-positive k in {path}")
    return {'path':path,'a':a,'k':k,'cols':cols}


def interp(x,y,x0):
    if x0 < x[0] or x0 > x[-1]:
        raise ValueError(f"target {x0} outside [{x[0]},{x[-1]}]")
    lo,hi=0,len(x)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if x[m] <= x0: lo=m
        else: hi=m
    if x0==x[lo]: return y[lo]
    if x0==x[hi]: return y[hi]
    t=(x0-x[lo])/(x[hi]-x[lo])
    return y[lo]+t*(y[hi]-y[lo])


def solve2(a00,a01,a11,b0,b1):
    det=a00*a11-a01*a01
    if det==0:
        return None
    return ((b0*a11-b1*a01)/det,(a00*b1-a01*b0)/det)


def fit_const_plus_x(xs,ys):
    # y=c0+c2*x
    n=len(xs); sx=sum(xs); sxx=sum(x*x for x in xs)
    sy=sum(ys); sxy=sum(x*y for x,y in zip(xs,ys))
    sol=solve2(float(n),sx,sxx,sy,sxy)
    if sol is None: return None
    c0,c2=sol
    pred=[c0+c2*x for x in xs]
    return c0,c2,pred


def fit_x_plus_x2(xs,ys):
    # y=c2*x+c4*x^2, exact zero intercept
    sxx=sum(x*x for x in xs)
    sx3=sum(x*x*x for x in xs)
    sx4=sum(x*x*x*x for x in xs)
    sxy=sum(x*y for x,y in zip(xs,ys))
    sx2y=sum(x*x*y for x,y in zip(xs,ys))
    sol=solve2(sxx,sx3,sx4,sxy,sx2y)
    if sol is None: return None
    c2,c4=sol
    pred=[c2*x+c4*x*x for x in xs]
    return c2,c4,pred


def norm_rms(y,p):
    rms=math.sqrt(sum((a-b)**2 for a,b in zip(y,p))/len(y))
    scale=max(max(abs(v) for v in y),1e-300)
    return rms/scale


def exponent(k1,c1,k2,c2):
    if c1==0 or c2==0 or c1*c2<0:
        return None
    return math.log(abs(c2/c1))/math.log(k2/k1)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--glob',dest='pattern',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--epochs',default='0.0005,0.001,0.01,0.1,0.5')
    args=ap.parse_args()
    epochs=[float(x) for x in args.epochs.split(',')]

    tabs=sorted((read_table(p) for p in glob.glob(args.pattern)),key=lambda t:t['k'])
    if len(tabs)<4:
        raise SystemExit('need at least four k tables')
    ks=[t['k'] for t in tabs]
    rows=[]

    for a0 in epochs:
        vals=[]
        for t in tabs:
            k=t['k']; c=t['cols']
            H=interp(t['a'],c['c10_Hc'],a0)
            dm=interp(t['a'],c['c10_delta_mu_total'],a0)
            rpt=interp(t['a'],c['c10_rpp_theta_total'],a0)
            C=dm+3.0*H*rpt/(k*k)
            vals.append({'k':k,'Hc':H,'delta_mu':dm,'rpp_theta':rpt,'C_com':C,'Y_C_over_k2':C/(k*k)})

        small4=vals[:4]
        xs=[v['k']**2 for v in small4]
        ys=[v['C_com'] for v in small4]
        f1=fit_const_plus_x(xs,ys)
        f0=fit_x_plus_x2(xs,ys)
        exps=[]
        for v1,v2 in zip(small4[:-1],small4[1:]):
            exps.append({
                'k1':v1['k'],'k2':v2['k'],
                'p_effective':exponent(v1['k'],v1['C_com'],v2['k'],v2['C_com']),
                'sign_change':v1['C_com']*v2['C_com']<0,
            })
        y3=[v['Y_C_over_k2'] for v in vals[:3]]
        y_abs=[abs(x) for x in y3]
        y_scale=max(y_abs+[1e-300])
        y_spread=(max(y3)-min(y3))/y_scale

        fit_const=None if f1 is None else {
            'c0':f1[0],'c2':f1[1],
            'normalized_rms':norm_rms(ys,f1[2]),
            'abs_c0_over_max_abs_C':abs(f1[0])/max(max(abs(y) for y in ys),1e-300),
        }
        fit_zero=None if f0 is None else {
            'c2':f0[0],'c4':f0[1],
            'normalized_rms':norm_rms(ys,f0[2]),
        }
        rows.append({
            'a':a0,
            'values':vals,
            'smallest4_effective_exponents':exps,
            'smallest4_const_plus_k2_fit':fit_const,
            'smallest4_zero_intercept_k2_plus_k4_fit':fit_zero,
            'smallest3_Y_values':y3,
            'smallest3_Y_signed_spread_over_max_abs':y_spread,
        })

    out={
        'schema':'RTK_C10_PARAMETER_FREE_SMALL_K_SOURCE_SCALING_DIAGNOSTIC_RESULT_v1',
        'classification':'C10_PARAMETER_FREE_SMALL_K_SOURCE_SCALING_DIAGNOSTIC_COMPLETE',
        'status_scope':'EXPLORATORY_DIAGNOSTIC_NO_PASS_FAIL_THRESHOLD',
        'definition':'C_com=delta_mu_CLASS+3 Hc rpp_theta_CLASS/k^2',
        'actual_k_values_Mpc_inv':ks,
        'common_scale_factors':epochs,
        'epochs':rows,
        'interpretation_guard':'This ladder measures a necessary completed-U1 source-compatibility scaling under fixed finite M_c and finite chi. It is not assumed to be an identity of the legacy model-2 production gravity equations, and this frozen exploratory target has no PASS/FAIL threshold.',
        'next_gate':'Use this diagnostic to freeze an independent confirmatory test with new smaller k values before classifying physical small-k source compatibility.',
        'completion_parameters_selected':False,
        'production_modified':False,
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'])
    for r in rows:
        print('a=',r['a'],'p=',[x['p_effective'] for x in r['smallest4_effective_exponents']],
              'Y3=',r['smallest3_Y_values'])

if __name__=='__main__':
    main()
