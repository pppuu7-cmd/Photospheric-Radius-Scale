#!/usr/bin/env python3
"""Confirmatory C10 parameter-free small-k source compatibility analyzer.

Consumes RT-CLASS scalar outputs extended by both C10 source-export patches.
The classification thresholds and new k ladder are frozen in
RTK_C10_PARAMETER_FREE_SMALL_K_SOURCE_COMPATIBILITY_CONFIRM_TARGET_v1.json.
"""
from __future__ import annotations
import argparse, glob, json, math
from pathlib import Path

BASE=[
 'c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime',
 'c10_H0_ord_double_prime','c10_deltaH0_ord','c10_delta_mu_total',
 'c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total','c10_W_total',
 'c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
DIRECT=['c10_Ccom_direct','c10_Ccom_over_k2_direct','c10_dZ_nlde',
        'c10_dZ_prime_nlde','c10_dV_nlde','c10_V_bg_nlde','c10_model2_0i_aux']
ALL=BASE+DIRECT


def read(path):
    txt=Path(path).read_text()
    miss=[x for x in ALL if x not in txt]
    if miss: raise RuntimeError(f'missing headers {miss} in {path}')
    rows=[]
    for raw in txt.splitlines():
        z=raw.strip()
        if not z or z.startswith('#'): continue
        rows.append([float(x) for x in z.split()])
    if not rows: raise RuntimeError(f'empty {path}')
    n=len(rows[0])
    if any(len(r)!=n for r in rows): raise RuntimeError(f'ragged {path}')
    tail=[r[-len(ALL):] for r in rows]
    cols={name:[r[i] for r in tail] for i,name in enumerate(ALL)}
    a=[r[1] for r in rows]
    if any(a[i+1]<=a[i] for i in range(len(a)-1)): raise RuntimeError(f'nonmonotonic a {path}')
    k=sum(cols['c10_k_Mpc_inv'])/len(rows)
    return {'path':path,'a':a,'k':k,'cols':cols}


def interp(x,y,x0):
    if x0<x[0] or x0>x[-1]: raise ValueError(f'{x0} outside {x[0]}..{x[-1]}')
    lo,hi=0,len(x)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if x[m]<=x0: lo=m
        else: hi=m
    if x0==x[lo]: return y[lo]
    if x0==x[hi]: return y[hi]
    t=(x0-x[lo])/(x[hi]-x[lo])
    return y[lo]+t*(y[hi]-y[lo])


def solve2(a00,a01,a11,b0,b1):
    d=a00*a11-a01*a01
    if d==0: return None
    return ((b0*a11-b1*a01)/d,(a00*b1-a01*b0)/d)


def fit_const_x(xs,ys):
    n=float(len(xs)); sx=sum(xs); sxx=sum(x*x for x in xs)
    sy=sum(ys); sxy=sum(x*y for x,y in zip(xs,ys))
    q=solve2(n,sx,sxx,sy,sxy)
    if q is None: return None
    c0,c2=q; pred=[c0+c2*x for x in xs]
    return c0,c2,pred


def fit_x_x2(xs,ys):
    s2=sum(x*x for x in xs); s3=sum(x**3 for x in xs); s4=sum(x**4 for x in xs)
    b1=sum(x*y for x,y in zip(xs,ys)); b2=sum(x*x*y for x,y in zip(xs,ys))
    q=solve2(s2,s3,s4,b1,b2)
    if q is None: return None
    c2,c4=q; pred=[c2*x+c4*x*x for x in xs]
    return c2,c4,pred


def nrms(y,p):
    return math.sqrt(sum((a-b)**2 for a,b in zip(y,p))/len(y))/max(max(abs(v) for v in y),1e-300)


def median(vals):
    s=sorted(vals); n=len(s)
    return s[n//2] if n%2 else 0.5*(s[n//2-1]+s[n//2])


def exponent(k1,c1,k2,c2):
    if c1==0 or c2==0 or c1*c2<=0: return None
    return math.log(abs(c2/c1))/math.log(k2/k1)


def epoch_metrics(tabs,a0,small_n,limits):
    vals=[]
    for t in tabs:
        c=t['cols']; k=t['k']
        direct=interp(t['a'],c['c10_Ccom_direct'],a0)
        ydirect=direct/(k*k)
        H=interp(t['a'],c['c10_Hc'],a0)
        dm=interp(t['a'],c['c10_delta_mu_total'],a0)
        mom=interp(t['a'],c['c10_rpp_theta_total'],a0)
        post=dm+3*H*mom/(k*k)
        vals.append({
            'k':k,'C_direct':direct,'Y_direct':ydirect,'C_postprocessed':post,
            'direct_minus_postprocessed':direct-post,
            'dZ':interp(t['a'],c['c10_dZ_nlde'],a0),
            'dZ_prime':interp(t['a'],c['c10_dZ_prime_nlde'],a0),
            'dV':interp(t['a'],c['c10_dV_nlde'],a0),
            'V_bg':interp(t['a'],c['c10_V_bg_nlde'],a0),
            'model2_0i_aux':interp(t['a'],c['c10_model2_0i_aux'],a0),
        })
    s=vals[:small_n]
    exps=[]; sign_ok=True; exp_ok=True
    for a,b in zip(s[:-1],s[1:]):
        p=exponent(a['k'],a['C_direct'],b['k'],b['C_direct'])
        sign_change=a['C_direct']*b['C_direct']<=0
        sign_ok &= not sign_change
        exp_ok &= (p is not None and limits['pmin']<=p<=limits['pmax'])
        exps.append({'k1':a['k'],'k2':b['k'],'p_effective':p,'sign_change':sign_change})
    ys=[v['Y_direct'] for v in s]
    medabs=median([abs(x) for x in ys])
    yspread=(max(ys)-min(ys))/max(medabs,1e-300)
    xs=[v['k']**2 for v in s]; cs=[v['C_direct'] for v in s]
    ffree=fit_const_x(xs,cs); fzero=fit_x_x2(xs,cs)
    free_metric=float('inf') if ffree is None else abs(ffree[0])/max(max(abs(x) for x in cs),1e-300)
    zero_rms=float('inf') if fzero is None else nrms(cs,fzero[2])
    passed=(sign_ok and exp_ok and yspread<=limits['yspread'] and
            zero_rms<=limits['zrms'] and free_metric<=limits['c0'])
    return {
        'a':a0,'values':vals,'smallest_confirmatory_values':s,
        'effective_exponents':exps,'Y_signed_spread_over_median_abs':yspread,
        'free_intercept_abs_c0_over_max_abs_C':free_metric,
        'zero_intercept_k2_plus_k4_normalized_rms':zero_rms,
        'no_sign_change':sign_ok,'all_adjacent_exponents_in_window':exp_ok,
        'passed':passed,
        'fit_free_intercept':None if ffree is None else {'c0':ffree[0],'c2':ffree[1]},
        'fit_zero_intercept':None if fzero is None else {'c2':fzero[0],'c4':fzero[1]},
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',dest='pattern',required=True)
    ap.add_argument('--target',required=True); ap.add_argument('--output',required=True)
    args=ap.parse_args()
    target=json.load(open(args.target))
    tabs=sorted((read(p) for p in glob.glob(args.pattern)),key=lambda z:z['k'])
    requested=[float(x) for x in target['k_ladder_Mpc_inv']]
    actual=[t['k'] for t in tabs]
    if len(actual)!=len(requested): raise SystemExit(f'k count mismatch {actual} vs {requested}')
    for a,b in zip(actual,requested):
        if abs(a-b)>1e-12*max(1.0,abs(b)): raise SystemExit(f'k mismatch {a} vs {b}')
    small=[float(x) for x in target['confirmatory_smallest_four_Mpc_inv']]
    if any(abs(actual[i]-small[i])>1e-14 for i in range(len(small))):
        raise SystemExit('smallest confirmatory k values are not the first requested values')
    q=target['per_epoch_acceptance_smallest_four']
    limits={'pmin':float(q['effective_exponent_each_adjacent_pair_min']),
            'pmax':float(q['effective_exponent_each_adjacent_pair_max']),
            'yspread':float(q['Y_equals_C_over_k2_signed_spread_over_median_abs_max']),
            'zrms':float(q['zero_intercept_fit_C_equals_c2k2_plus_c4k4_normalized_rms_max']),
            'c0':float(q['free_intercept_fit_abs_c0_over_max_abs_C_max'])}
    core=[epoch_metrics(tabs,float(a),len(small),limits) for a in target['core_scale_factors']]
    early=epoch_metrics(tabs,float(target['nonbinding_early_diagnostic_scale_factor']),len(small),limits)
    core_pass=all(x['passed'] for x in core)
    cls=('C10_PARAMETER_FREE_SMALL_K_SOURCE_COMPATIBILITY_PASS_CORE_EPOCHS_SCOPED'
         if core_pass else 'C10_PARAMETER_FREE_SMALL_K_SOURCE_COMPATIBILITY_FAIL_CORE_EPOCHS_SCOPED')
    out={
        'schema':'RTK_C10_PARAMETER_FREE_SMALL_K_SOURCE_COMPATIBILITY_CONFIRM_RESULT_v1',
        'classification':cls,'core_pass':core_pass,'actual_k_values_Mpc_inv':actual,
        'confirmatory_smallest_four_Mpc_inv':small,'acceptance_limits':limits,
        'core_epochs':core,'nonbinding_early_epoch':early,
        'completion_parameters_selected':False,'production_modified':False,
        'target':args.target,
        'interpretation_guard':'PASS/FAIL concerns only the frozen necessary source-compatibility scaling over the core tested epochs. It does not close the full completed-U1 history replay or choose an EFT onset/completion parameters.'
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for e in core:
        print('CORE',e['a'],'pass=',e['passed'],'p=',[x['p_effective'] for x in e['effective_exponents']],
              'Yspread=',e['Y_signed_spread_over_median_abs'],'c0=',e['free_intercept_abs_c0_over_max_abs_C'],
              'zrms=',e['zero_intercept_k2_plus_k4_normalized_rms'])
    print('EARLY_NONBINDING',early['a'],'pass_metric=',early['passed'])

if __name__=='__main__': main()
