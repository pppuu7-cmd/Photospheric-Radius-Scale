#!/usr/bin/env python3
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
    return {'a':a[:,1],'c':c,'k':float(np.mean(c['rtctl_k'])),'path':path}

def local_value(x,y,x0,n=10,deg=4):
    idx=np.argsort(np.abs(x-x0))[:min(n,len(x))]
    idx=np.sort(idx); xx=x[idx]-x0
    scale=max(float(np.max(np.abs(xx))),1e-30)
    z=xx/scale
    co=np.polyfit(z,y[idx],min(deg,len(idx)-1))
    return float(np.polyval(co,0.0))

def state_at(tab,a0):
    return {n:local_value(tab['a'],y,a0) for n,y in tab['c'].items()}

def residual_corr(v,a,k):
    H=v['rtctl_Hc']
    B=(v['rtctl_dU']-v['rtctl_dVprime']/a**2+H*v['rtctl_dV']/a**2
       +v['rtctl_psi']*v['rtctl_Vbgprime']/a**2
       -H*v['rtctl_psi']*v['rtctl_Vbg']/a**2)
    return (v['rtctl_Ccom']+2*k*k*v['rtctl_phi']/(3*a*a)
            +v['rtctl_gamma']*v['rtctl_H0']**2*B
            +2*H*v['rtctl_A0i_code']/a**2)

def load(root,req):
    tabs=sorted([read(p) for p in glob.glob(str(Path(root)/'corr_*perturbations*'))],key=lambda z:z['k'])
    if len(tabs)!=len(req): raise RuntimeError(f'{root}: got {len(tabs)} files, expected {len(req)}')
    for z,k in zip(tabs,req):
        if abs(z['k']-k)>1e-12*max(1.,abs(k)): raise RuntimeError(f'k mismatch {z["k"]} != {k}')
    return tabs

def medabs(xs): return float(np.median(np.abs(np.asarray(xs,float))))

def parent_old(parent,tree,a0):
    d=parent['trees'][tree]['default']['late'][str(a0)]
    return float(d['median_abs_R00_quartic10'])

def analyze(root,tree,req,epochs,parent):
    tabs=load(root,req); points={}; summary={}
    for a0 in epochs:
        rows=[]
        for tab in tabs:
            v=state_at(tab,a0)
            r=residual_corr(v,a0,tab['k'])
            rows.append({'k':tab['k'],'a':a0,'R00_corr':r})
        corr=medabs([r['R00_corr'] for r in rows])
        old=parent_old(parent,tree,a0)
        summary[str(a0)]={
          'median_abs_R00_corr':corr,
          'parent_old_default_median_abs_R00_quartic10':old,
          'corr_over_old':corr/max(old,1e-300)
        }
        points[str(a0)]=rows
    return {'summary':summary,'points':points}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--upstream-dir',required=True); ap.add_argument('--rtk-dir',required=True)
    ap.add_argument('--target',required=True); ap.add_argument('--parent-old',required=True); ap.add_argument('--output',required=True)
    q=ap.parse_args()
    t=json.load(open(q.target)); parent=json.load(open(q.parent_old))
    req=list(map(float,t['k_ladder_Mpc_inv']))
    diag=list(map(float,t['diagnostic_scale_factors'])); bind=list(map(float,t['binding_scale_factors'])); epochs=diag+bind
    trees={
      'untouched_upstream_model2':analyze(q.upstream_dir,'untouched_upstream_model2',req,epochs,parent),
      'historical_production_RTK_model2':analyze(q.rtk_dir,'historical_production_RTK_model2',req,epochs,parent)
    }
    vals=[]; finite=True
    for tree in trees.values():
        for a0 in bind:
            d=tree['summary'][str(a0)]; vals.append((d['corr_over_old'],d['median_abs_R00_corr']))
            finite=finite and np.isfinite(d['corr_over_old']) and np.isfinite(d['median_abs_R00_corr'])
    if not finite:
        cls=t['classifications']['nonfinite']
    elif all(r<=0.10 and a<=5e-11 for r,a in vals):
        cls=t['classifications']['closure']
    elif all(r>=0.50 for r,a in vals):
        cls=t['classifications']['no_closure']
    else:
        cls=t['classifications']['mixed']
    out={
      'schema':'RTK_C10_CORRECTED_RT_00_COVECTOR_ROUNDTRIP_RESULT_v1',
      'classification':cls,'target':q.target,'trees':trees,
      'binding_pairs_corr_over_old_and_abs':vals,
      'uses_reconstructed_psi_derivative':False,
      'physical_or_translation_coefficients_fitted':False,
      'production_modified':False
    }
    Path(q.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for n,v in trees.items(): print(n,json.dumps(v['summary'],sort_keys=True))
if __name__=='__main__': main()
