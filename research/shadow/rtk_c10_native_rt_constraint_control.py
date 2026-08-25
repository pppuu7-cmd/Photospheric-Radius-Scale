#!/usr/bin/env python3
"""Evaluate the frozen untouched-native-RT 00/0i constraint control."""
from __future__ import annotations
import argparse, glob, json
from pathlib import Path
import numpy as np

COLS=['rtctl_k','rtctl_Hc','rtctl_Ccom','rtctl_dU','rtctl_dV','rtctl_dVprime',
      'rtctl_dZ','rtctl_dZprime','rtctl_Vbg','rtctl_Vbgprime','rtctl_phi',
      'rtctl_psi','rtctl_phi_prime','rtctl_gamma','rtctl_H0','rtctl_A0i_code']

def read(path):
    txt=Path(path).read_text()
    miss=[c for c in COLS if c not in txt]
    if miss: raise RuntimeError(f'missing {miss} in {path}')
    a=np.loadtxt(path)
    if a.ndim==1: a=a[None,:]
    tail=a[:,-len(COLS):]
    c={n:tail[:,i] for i,n in enumerate(COLS)}
    return {'tau':a[:,0],'a':a[:,1],'c':c,'k':float(np.mean(c['rtctl_k'])),'path':path}

def local_poly(x,y,x0,n=8,deg=4):
    idx=np.argsort(np.abs(x-x0))[:min(n,len(x))]
    idx=np.sort(idx); xx=x[idx]-x0
    scale=max(float(np.max(np.abs(xx))),1e-30)
    z=xx/scale
    co=np.polyfit(z,y[idx],deg)
    val=float(np.polyval(co,0.0)); der=float(np.polyval(np.polyder(co),0.0)/scale)
    return val,der

def state(t,a0):
    tau0=float(np.interp(a0,t['a'],t['tau']))
    v={n:local_poly(t['tau'],y,tau0)[0] for n,y in t['c'].items()}
    _,psip=local_poly(t['tau'],t['c']['rtctl_psi'],tau0)
    _,phip=local_poly(t['tau'],t['c']['rtctl_phi'],tau0)
    v['psi_prime_fit']=psip; v['phi_prime_fit']=phip; v['tau']=tau0
    return v

def eval_one(t,a0):
    v=state(t,a0); a=float(a0); k=t['k']; H=v['rtctl_Hc']
    B=(v['rtctl_dU']-v['rtctl_dVprime']/a**2+H*v['rtctl_dV']/a**2
       +2*v['rtctl_psi']*v['rtctl_Vbgprime']/a**2
       -2*H*v['rtctl_psi']*v['rtctl_Vbg']/a**2
       +v['psi_prime_fit']*v['rtctl_Vbg']/a**2)
    obs=v['rtctl_Ccom']+2*k*k*v['rtctl_phi']/(3*a*a)
    pred=-v['rtctl_gamma']*v['rtctl_H0']**2*B-2*H*v['rtctl_A0i_code']/a**2
    return {'k':k,'tau':v['tau'],'observed_aux':obs,'predicted_aux':pred,'residual':obs-pred,
            'B00':B,'Ccom':v['rtctl_Ccom'],'phi':v['rtctl_phi'],'psi':v['rtctl_psi'],
            'phi_prime_direct':v['rtctl_phi_prime'],'phi_prime_fit':v['phi_prime_fit'],
            'phi_prime_fit_abs_error':abs(v['rtctl_phi_prime']-v['phi_prime_fit']),
            'psi_prime_fit':v['psi_prime_fit'],'gamma':v['rtctl_gamma'],'H0':v['rtctl_H0'],
            'A0i_code':v['rtctl_A0i_code']}

def medabs(x): return float(np.median(np.abs(np.asarray(x,float))))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',required=True); ap.add_argument('--target',required=True); ap.add_argument('--output',required=True); q=ap.parse_args()
    tar=json.load(open(q.target)); tabs=sorted([read(p) for p in glob.glob(q.glob)],key=lambda t:t['k'])
    req=list(map(float,tar['k_ladder_Mpc_inv']))
    if len(tabs)!=len(req): raise SystemExit(f'k count {len(tabs)} != {len(req)}')
    for t,k in zip(tabs,req):
        if abs(t['k']-k)>1e-12*max(1,abs(k)): raise SystemExit(f'k mismatch {t["k"]} {k}')
    epochs=[]
    lim=tar['acceptance_per_epoch']
    for a0 in map(float,tar['binding_scale_factors']):
        pts=[eval_one(t,a0) for t in tabs]
        obs=medabs([p['observed_aux'] for p in pts]); pred=medabs([p['predicted_aux'] for p in pts]); res=medabs([p['residual'] for p in pts]); den=max(obs,1e-300)
        rp=res/den; pp=pred/den
        passed=(rp<=float(lim['median_abs_roundtrip_over_median_abs_observed_aux_max']) and float(lim['median_abs_predicted_aux_over_median_abs_observed_aux_min'])<=pp<=float(lim['median_abs_predicted_aux_over_median_abs_observed_aux_max']))
        epochs.append({'a':a0,'passed':passed,'observed_aux_median_abs':obs,'predicted_aux_median_abs':pred,'residual_median_abs':res,'roundtrip_over_observed':rp,'predicted_over_observed':pp,'points':pts})
    cls=tar['decision_rule']['all_binding_epochs_pass'] if all(e['passed'] for e in epochs) else tar['decision_rule']['otherwise']
    out={'schema':'RTK_C10_NATIVE_RT_CONSTRAINT_CONTROL_RESULT_v1','classification':cls,'epochs':epochs,'pass_count':sum(e['passed'] for e in epochs),'epoch_count':len(epochs),'actual_k_values_Mpc_inv':[t['k'] for t in tabs],'target':q.target,'production_rtk_patch_applied':False,'guard':'Code-equation control only; historical RTK Om is reused as ordinary CDM density solely for this diagnostic.'}
    Path(q.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for e in epochs: print('EPOCH',e['a'],'pass=',e['passed'],'R/obs=',e['roundtrip_over_observed'],'P/obs=',e['predicted_over_observed'])
if __name__=='__main__': main()
