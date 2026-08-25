#!/usr/bin/env python3
"""C10.46: project the translated legacy RT 00 residual at the initial surface.

Uses linear superposition of a baseline model=2 solution and one disposable
homogeneous deltaU_ini=1 auxiliary seed solution. No coefficient in the RT
constraint is fitted or rescaled.
"""
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

def edge_derivative(x,y,n,deg):
    m=min(n,len(x)); xx=x[:m]-x[0]
    scale=max(float(np.max(np.abs(xx))),1e-30)
    z=xx/scale; co=np.polyfit(z,y[:m],min(deg,m-1))
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
    return {'k':k,'a':a,'tau':float(tab['tau'][0]),
            'R6':residual(v,a,k,p6),'R10':residual(v,a,k,p10),
            'psi_prime_6':p6,'psi_prime_10':p10,'dU':v['rtctl_dU'],
            'dUprime':v['rtctl_dVprime']*0.0+float(tab['c']['rtctl_dU'][0]*0.0)}

def at_epoch(tab,a0):
    tau0=float(np.interp(a0,tab['a'],tab['tau']))
    v={n:local_value_derivative(tab['tau'],y,tau0,10,4)[0] for n,y in tab['c'].items()}
    _,p6=local_value_derivative(tab['tau'],tab['c']['rtctl_psi'],tau0,6,3)
    _,p10=local_value_derivative(tab['tau'],tab['c']['rtctl_psi'],tau0,10,4)
    return {'k':tab['k'],'a':float(a0),'tau':tau0,'R6':residual(v,a0,tab['k'],p6),'R10':residual(v,a0,tab['k'],p10)}

def load(root,prefix,req):
    tabs=sorted([read(p) for p in glob.glob(str(Path(root)/f'{prefix}_*perturbations*'))],key=lambda z:z['k'])
    if len(tabs)!=len(req): raise RuntimeError(f'{root}/{prefix}: k count {len(tabs)} != {len(req)}')
    for z,k in zip(tabs,req):
        if abs(z['k']-k)>1e-12*max(1.,abs(k)): raise RuntimeError(f'k mismatch {z["k"]} != {k}')
    return tabs

def medabs(xs): return float(np.median(np.abs(np.asarray(xs,float))))

def analyze_tree(root,req,diag_epochs,bind_epochs,cond):
    base=load(root,'proj_base',req); seed=load(root,'proj_seed',req)
    projected=[]
    for b,s in zip(base,seed):
        eb,es=earliest(b),earliest(s)
        da=abs(eb['a']-es['a'])/max(abs(eb['a']),abs(es['a']),1e-300)
        dt=abs(eb['tau']-es['tau'])/max(abs(eb['tau']),abs(es['tau']),1e-300)
        if da>1e-8 or dt>1e-8:
            raise RuntimeError(f'baseline/seed earliest grids differ k={b["k"]}: da={da} dt={dt}')
        dR10=es['R10']-eb['R10']; dR6=es['R6']-eb['R6']
        alpha=-eb['R10']/dR10 if dR10!=0 else float('inf')
        well=(np.isfinite(alpha) and abs(dR10)>=0.25*abs(eb['R10']) and abs(alpha)<=4.0)
        p={'k':b['k'],'alpha':float(alpha),'well_conditioned':bool(well),
           'earliest':{'a':eb['a'],'tau':eb['tau'],'R_base_10':eb['R10'],'R_seed_10':es['R10'],
                       'DeltaR_seed_10':dR10,'R_projected_10':eb['R10']+alpha*dR10,
                       'R_base_6':eb['R6'],'R_seed_6':es['R6'],'DeltaR_seed_6':dR6,
                       'R_projected_6':eb['R6']+alpha*dR6,
                       'dU_base':eb['dU'],'dU_seed':es['dU']},
           'epochs':{}}
        for a0 in diag_epochs+bind_epochs:
            bb=at_epoch(b,a0); ss=at_epoch(s,a0)
            p['epochs'][str(a0)]={
                'R_base_10':bb['R10'],'R_seed_10':ss['R10'],'DeltaR_seed_10':ss['R10']-bb['R10'],
                'R_projected_10':bb['R10']+alpha*(ss['R10']-bb['R10']),
                'R_base_6':bb['R6'],'R_seed_6':ss['R6'],'DeltaR_seed_6':ss['R6']-bb['R6'],
                'R_projected_6':bb['R6']+alpha*(ss['R6']-bb['R6'])}
        projected.append(p)
    well_count=sum(p['well_conditioned'] for p in projected)
    eb10=medabs([p['earliest']['R_base_10'] for p in projected])
    ep10=medabs([p['earliest']['R_projected_10'] for p in projected])
    eb6=medabs([p['earliest']['R_base_6'] for p in projected])
    ep6=medabs([p['earliest']['R_projected_6'] for p in projected])
    summary={'well_conditioned_modes':well_count,'mode_count':len(projected),
             'earliest_baseline_median_abs_R10':eb10,'earliest_projected_median_abs_R10':ep10,
             'earliest_baseline_median_abs_R6':eb6,'earliest_projected_median_abs_R6':ep6,
             'cross_estimator_projected_over_baseline':ep6/max(eb6,1e-300),
             'epoch_ratios':{}}
    for a0 in diag_epochs+bind_epochs:
        b10=medabs([p['epochs'][str(a0)]['R_base_10'] for p in projected])
        q10=medabs([p['epochs'][str(a0)]['R_projected_10'] for p in projected])
        b6=medabs([p['epochs'][str(a0)]['R_base_6'] for p in projected])
        q6=medabs([p['epochs'][str(a0)]['R_projected_6'] for p in projected])
        summary['epoch_ratios'][str(a0)]={'baseline_median_abs_R10':b10,'projected_median_abs_R10':q10,
                                          'projected_over_baseline_R10':q10/max(b10,1e-300),
                                          'baseline_median_abs_R6':b6,'projected_median_abs_R6':q6,
                                          'projected_over_baseline_R6':q6/max(b6,1e-300)}
    return {'summary':summary,'points':projected}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--upstream-dir',required=True); ap.add_argument('--rtk-dir',required=True); ap.add_argument('--target',required=True); ap.add_argument('--output',required=True); q=ap.parse_args()
    t=json.load(open(q.target)); req=list(map(float,t['k_ladder_Mpc_inv']))
    diag=list(map(float,t['diagnostic_scale_factors'])); bind=list(map(float,t['binding_scale_factors'])); cond=t['conditioning']
    trees={
      'untouched_upstream_model2':analyze_tree(q.upstream_dir,req,diag,bind,cond),
      'historical_production_RTK_model2':analyze_tree(q.rtk_dir,req,diag,bind,cond)}
    min_modes=int(cond['min_well_conditioned_modes_per_tree']); crossmax=float(cond['cross_estimator_projected_earliest_over_baseline_median_max'])
    ill=any(v['summary']['well_conditioned_modes']<min_modes for v in trees.values())
    deriv=any(v['summary']['cross_estimator_projected_over_baseline']>crossmax for v in trees.values())
    ratios=[trees[name]['summary']['epoch_ratios'][str(a)]['projected_over_baseline_R10'] for name in trees for a in bind]
    if ill: cls=t['classifications']['projection_ill_conditioned']
    elif deriv: cls=t['classifications']['derivative_limited']
    elif all(r<=0.1 for r in ratios): cls=t['classifications']['preserved']
    elif all(r>=0.5 for r in ratios): cls=t['classifications']['regenerated']
    else: cls=t['classifications']['mixed']
    out={'schema':'RTK_C10_LEGACY_RT_00_CONSTRAINT_PROJECTION_PROPAGATION_RESULT_v1','classification':cls,
         'target':q.target,'trees':trees,'binding_ratios_R10':ratios,
         'physical_coefficients_fitted':False,'production_modified':False,
         'projection_is_diagnostic_linear_superposition':True}
    Path(q.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for n,v in trees.items(): print(n,v['summary'])
if __name__=='__main__': main()
