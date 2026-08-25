#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json
from pathlib import Path
import numpy as np

COLS=['rtctl_k','rtctl_Hc','rtctl_Ccom','rtctl_dU','rtctl_dV','rtctl_dVprime',
      'rtctl_dZ','rtctl_dZprime','rtctl_Vbg','rtctl_Vbgprime','rtctl_phi',
      'rtctl_psi','rtctl_phi_prime','rtctl_gamma','rtctl_H0','rtctl_A0i_code']
VARIANTS=['default','earlier_x2','earlier_x4']

def read(path):
    txt=Path(path).read_text()
    miss=[c for c in COLS if c not in txt]
    if miss: raise RuntimeError(f'missing {miss} in {path}')
    a=np.loadtxt(path)
    if a.ndim==1: a=a[None,:]
    tail=a[:,-len(COLS):]
    c={n:tail[:,i] for i,n in enumerate(COLS)}
    return {'tau':a[:,0],'a':a[:,1],'c':c,'k':float(np.mean(c['rtctl_k'])),'path':path}

def edge_derivative(x,y,n,deg):
    m=min(n,len(x)); xx=x[:m]-x[0]
    scale=max(float(np.max(np.abs(xx))),1e-30)
    z=xx/scale
    co=np.polyfit(z,y[:m],min(deg,m-1))
    return float(np.polyval(np.polyder(co),0.0)/scale)

def local_value_derivative(x,y,x0,n,deg):
    idx=np.argsort(np.abs(x-x0))[:min(n,len(x))]
    idx=np.sort(idx); xx=x[idx]-x0
    scale=max(float(np.max(np.abs(xx))),1e-30)
    z=xx/scale; co=np.polyfit(z,y[idx],min(deg,len(idx)-1))
    return float(np.polyval(co,0.0)),float(np.polyval(np.polyder(co),0.0)/scale)

def residual(v,a,k,psip):
    H=v['rtctl_Hc']
    B=(v['rtctl_dU']-v['rtctl_dVprime']/a**2+H*v['rtctl_dV']/a**2
       +2*v['rtctl_psi']*v['rtctl_Vbgprime']/a**2
       -2*H*v['rtctl_psi']*v['rtctl_Vbg']/a**2
       +psip*v['rtctl_Vbg']/a**2)
    return (v['rtctl_Ccom']+2*k*k*v['rtctl_phi']/(3*a*a)
            +v['rtctl_gamma']*v['rtctl_H0']**2*B
            +2*H*v['rtctl_A0i_code']/a**2)

def earliest(tab):
    v={n:float(y[0]) for n,y in tab['c'].items()}; a=float(tab['a'][0]); k=tab['k']
    p6=edge_derivative(tab['tau'],tab['c']['rtctl_psi'],6,3)
    p10=edge_derivative(tab['tau'],tab['c']['rtctl_psi'],10,4)
    r6=residual(v,a,k,p6); r10=residual(v,a,k,p10)
    aux=max(abs(v['rtctl_dU']),abs(v['rtctl_dV']),abs(v['rtctl_dVprime']),abs(v['rtctl_dZ']),abs(v['rtctl_dZprime']))
    return {'k':k,'a_earliest':a,'tau_earliest':float(tab['tau'][0]),'R00_cubic6':r6,'R00_quartic10':r10,
            'psi_prime_cubic6':p6,'psi_prime_quartic10':p10,'aux_initial_max_abs':aux}

def at_epoch(tab,a0):
    tau0=float(np.interp(a0,tab['a'],tab['tau']))
    v={n:local_value_derivative(tab['tau'],y,tau0,8,4)[0] for n,y in tab['c'].items()}
    _,p6=local_value_derivative(tab['tau'],tab['c']['rtctl_psi'],tau0,6,3)
    _,p10=local_value_derivative(tab['tau'],tab['c']['rtctl_psi'],tau0,10,4)
    return {'k':tab['k'],'a':a0,'R00_cubic6':residual(v,a0,tab['k'],p6),'R00_quartic10':residual(v,a0,tab['k'],p10),
            'psi_prime_cubic6':p6,'psi_prime_quartic10':p10}

def medabs(xs): return float(np.median(np.abs(np.asarray(xs,float))))
def discrepancy(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)

def load_variant(root,variant,req):
    tabs=sorted([read(p) for p in glob.glob(str(Path(root)/f'fi_{variant}_*perturbations*'))],key=lambda z:z['k'])
    if len(tabs)!=len(req): raise RuntimeError(f'{root}/{variant}: k count {len(tabs)} != {len(req)}')
    for z,k in zip(tabs,req):
        if abs(z['k']-k)>1e-12*max(1.,abs(k)): raise RuntimeError(f'k mismatch {z["k"]} != {k}')
    return tabs

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--upstream-dir',required=True); ap.add_argument('--rtk-dir',required=True); ap.add_argument('--target',required=True); ap.add_argument('--output',required=True); q=ap.parse_args()
    t=json.load(open(q.target)); req=list(map(float,t['k_ladder_Mpc_inv'])); epochs=list(map(float,t['late_binding_scale_factors']))
    trees={}; derivative_limited=False
    for tree,root in [('untouched_upstream_model2',q.upstream_dir),('historical_production_RTK_model2',q.rtk_dir)]:
        vr={}
        for variant in VARIANTS:
            tabs=load_variant(root,variant,req)
            ep=[earliest(z) for z in tabs]
            late={str(a0):[at_epoch(z,a0) for z in tabs] for a0 in epochs}
            em6=medabs([x['R00_cubic6'] for x in ep]); em10=medabs([x['R00_quartic10'] for x in ep])
            disc_e=discrepancy(em6,em10)
            lm={}
            maxdisc=disc_e
            for a0 in epochs:
                pts=late[str(a0)]; m6=medabs([x['R00_cubic6'] for x in pts]); m10=medabs([x['R00_quartic10'] for x in pts]); d=discrepancy(m6,m10); maxdisc=max(maxdisc,d)
                lm[str(a0)]={'median_abs_R00_cubic6':m6,'median_abs_R00_quartic10':m10,'estimator_relative_difference':d,'points':pts}
            if maxdisc>0.20: derivative_limited=True
            vr[variant]={'earliest':{'median_abs_R00_cubic6':em6,'median_abs_R00_quartic10':em10,'estimator_relative_difference':disc_e,'points':ep},'late':lm,'max_estimator_relative_difference':maxdisc}
        base=vr['default']; x4=vr['earlier_x4']
        ratios={'earliest':x4['earliest']['median_abs_R00_quartic10']/max(base['earliest']['median_abs_R00_quartic10'],1e-300)}
        for a0 in (0.1,0.5): ratios[str(a0)]=x4['late'][str(a0)]['median_abs_R00_quartic10']/max(base['late'][str(a0)]['median_abs_R00_quartic10'],1e-300)
        vr['earlier_x4_over_default_ratios']=ratios
        trees[tree]=vr
    rules=t['decision_rules']
    if derivative_limited: cls=t['classifications']['derivative_limited']
    else:
        start_sensitive=False; start_stable=True
        for tree,vr in trees.items():
            rr=vr['earlier_x4_over_default_ratios']
            if rr['earliest']<=1/3 and rr['0.1']<=1/3 and rr['0.5']<=1/3: start_sensitive=True
            if not all(0.5<=rr[k]<=2.0 for k in ('earliest','0.1','0.5')): start_stable=False
        if start_sensitive: cls=t['classifications']['start_sensitive']
        elif start_stable: cls=t['classifications']['start_stable']
        else: cls=t['classifications']['mixed']
    out={'schema':'RTK_C10_LEGACY_RT_00_INITIAL_FIRST_INTEGRAL_PROPAGATION_RESULT_v1','classification':cls,'target':q.target,'trees':trees,'derivative_limited':derivative_limited,'production_modified':False,'coefficients_fitted':False}
    Path(q.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(cls)
    for tree,vr in trees.items(): print(tree,vr['earlier_x4_over_default_ratios'])
if __name__=='__main__': main()
