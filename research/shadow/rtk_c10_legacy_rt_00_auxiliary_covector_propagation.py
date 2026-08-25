#!/usr/bin/env python3
"""C10.47 full auxiliary-IC covector propagation test for translated RT R00."""
from __future__ import annotations
import argparse, glob, itertools, json
from pathlib import Path
import numpy as np

COLS=['rtctl_k','rtctl_Hc','rtctl_Ccom','rtctl_dU','rtctl_dV','rtctl_dVprime',
      'rtctl_dZ','rtctl_dZprime','rtctl_Vbg','rtctl_Vbgprime','rtctl_phi',
      'rtctl_psi','rtctl_phi_prime','rtctl_gamma','rtctl_H0','rtctl_A0i_code']
LABELS=['dU','dUp','dV','dVp','dZ','dZp']

def read(path):
    txt=Path(path).read_text(); miss=[c for c in COLS if c not in txt]
    if miss: raise RuntimeError(f'missing {miss} in {path}')
    a=np.loadtxt(path)
    if a.ndim==1: a=a[None,:]
    tail=a[:,-len(COLS):]; c={n:tail[:,i] for i,n in enumerate(COLS)}
    return {'tau':a[:,0],'a':a[:,1],'c':c,'k':float(np.mean(c['rtctl_k'])),'path':path}

def edge_derivative(x,y,n,deg):
    m=min(n,len(x)); xx=x[:m]-x[0]; scale=max(float(np.max(np.abs(xx))),1e-30)
    co=np.polyfit(xx/scale,y[:m],min(deg,m-1))
    return float(np.polyval(np.polyder(co),0.0)/scale)

def local_value_derivative(x,y,x0,n,deg):
    idx=np.argsort(np.abs(x-x0))[:min(n,len(x))]; idx=np.sort(idx); xx=x[idx]-x0
    scale=max(float(np.max(np.abs(xx))),1e-30); co=np.polyfit(xx/scale,y[idx],min(deg,len(idx)-1))
    return float(np.polyval(co,0.0)),float(np.polyval(np.polyder(co),0.0)/scale)

def residual(v,a,k,psip):
    H=v['rtctl_Hc']
    B=(v['rtctl_dU']-v['rtctl_dVprime']/a**2+H*v['rtctl_dV']/a**2
       +2*v['rtctl_psi']*v['rtctl_Vbgprime']/a**2-2*H*v['rtctl_psi']*v['rtctl_Vbg']/a**2
       +psip*v['rtctl_Vbg']/a**2)
    return (v['rtctl_Ccom']+2*k*k*v['rtctl_phi']/(3*a*a)
            +v['rtctl_gamma']*v['rtctl_H0']**2*B+2*H*v['rtctl_A0i_code']/a**2)

def earliest(tab):
    v={n:float(y[0]) for n,y in tab['c'].items()}; a=float(tab['a'][0]); k=tab['k']
    p6=edge_derivative(tab['tau'],tab['c']['rtctl_psi'],6,3); p10=edge_derivative(tab['tau'],tab['c']['rtctl_psi'],10,4)
    return {'a':a,'tau':float(tab['tau'][0]),'R6':residual(v,a,k,p6),'R10':residual(v,a,k,p10)}

def at_epoch(tab,a0):
    tau0=float(np.interp(a0,tab['a'],tab['tau']))
    v={n:local_value_derivative(tab['tau'],y,tau0,10,4)[0] for n,y in tab['c'].items()}
    _,p6=local_value_derivative(tab['tau'],tab['c']['rtctl_psi'],tau0,6,3)
    _,p10=local_value_derivative(tab['tau'],tab['c']['rtctl_psi'],tau0,10,4)
    return {'R6':residual(v,a0,tab['k'],p6),'R10':residual(v,a0,tab['k'],p10)}

def load(root,prefix,req):
    tabs=sorted([read(p) for p in glob.glob(str(Path(root)/f'{prefix}_*perturbations*'))],key=lambda z:z['k'])
    if len(tabs)!=len(req): raise RuntimeError(f'{root}/{prefix}: k count {len(tabs)} != {len(req)}')
    for z,k in zip(tabs,req):
        if abs(z['k']-k)>1e-12*max(1.,abs(k)): raise RuntimeError(f'k mismatch {z["k"]} != {k}')
    return tabs

def pair_stats(r0,rt,labels,rel_floor):
    raw=[]
    for i,j in itertools.combinations(range(len(labels)),2):
        a=rt[i]*r0[j]; b=rt[j]*r0[i]; den=abs(a)+abs(b); num=abs(a-b)
        raw.append({'pair':f'{labels[i]}:{labels[j]}','numerator':float(num),'denominator':float(den),
                    'normalized_minor':float(num/max(den,1e-300))})
    maxden=max((x['denominator'] for x in raw),default=0.0)
    active=[x for x in raw if maxden>0 and x['denominator']>=rel_floor*maxden]
    vals=[x['normalized_minor'] for x in active]
    return {'active_pair_count':len(active),'max_pair_denominator':float(maxden),
            'median_normalized_minor':float(np.median(vals)) if vals else None,
            'max_normalized_minor':float(max(vals)) if vals else None,'active_pairs':active}

def analyze_tree(root,req,epochs,rel_floor):
    base=load(root,'basis_base',req); seeds={lab:load(root,f'basis_{lab}',req) for lab in LABELS}
    modes=[]
    for idx,b in enumerate(base):
        eb=earliest(b); es={lab:earliest(seeds[lab][idx]) for lab in LABELS}
        for lab,e in es.items():
            da=abs(e['a']-eb['a'])/max(abs(e['a']),abs(eb['a']),1e-300)
            dt=abs(e['tau']-eb['tau'])/max(abs(e['tau']),abs(eb['tau']),1e-300)
            if da>1e-8 or dt>1e-8: raise RuntimeError(f'grid mismatch {lab} k={b["k"]}')
        r0_10=np.array([es[lab]['R10']-eb['R10'] for lab in LABELS],float)
        r0_6=np.array([es[lab]['R6']-eb['R6'] for lab in LABELS],float)
        mode={'k':b['k'],'earliest':{'a':eb['a'],'tau':eb['tau'],'R_base_10':eb['R10'],'R_base_6':eb['R6'],
                                     'response_vector_10':dict(zip(LABELS,map(float,r0_10))),
                                     'response_vector_6':dict(zip(LABELS,map(float,r0_6)))},'epochs':{}}
        for a0 in epochs:
            bb=at_epoch(b,a0); ss={lab:at_epoch(seeds[lab][idx],a0) for lab in LABELS}
            rt10=np.array([ss[lab]['R10']-bb['R10'] for lab in LABELS],float)
            rt6=np.array([ss[lab]['R6']-bb['R6'] for lab in LABELS],float)
            mode['epochs'][str(a0)]={'R_base_10':bb['R10'],'R_base_6':bb['R6'],
                                     'response_vector_10':dict(zip(LABELS,map(float,rt10))),
                                     'response_vector_6':dict(zip(LABELS,map(float,rt6))),
                                     'minor_stats_10':pair_stats(r0_10,rt10,LABELS,rel_floor),
                                     'minor_stats_6':pair_stats(r0_6,rt6,LABELS,rel_floor)}
        modes.append(mode)
    summary={'epochs':{}}
    for a0 in epochs:
        p10=[m['epochs'][str(a0)]['minor_stats_10']['median_normalized_minor'] for m in modes]
        p6=[m['epochs'][str(a0)]['minor_stats_6']['median_normalized_minor'] for m in modes]
        if any(x is None for x in p10+p6): med10=med6=None
        else: med10=float(np.median(p10)); med6=float(np.median(p6))
        summary['epochs'][str(a0)]={'tree_median_normalized_minor_10':med10,
                                    'tree_median_normalized_minor_6':med6,
                                    'estimator_absolute_difference':None if med10 is None else abs(med10-med6),
                                    'min_active_pairs_10':min(m['epochs'][str(a0)]['minor_stats_10']['active_pair_count'] for m in modes),
                                    'min_active_pairs_6':min(m['epochs'][str(a0)]['minor_stats_6']['active_pair_count'] for m in modes)}
    return {'summary':summary,'modes':modes}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--upstream-dir',required=True); ap.add_argument('--rtk-dir',required=True); ap.add_argument('--target',required=True); ap.add_argument('--output',required=True); q=ap.parse_args()
    t=json.load(open(q.target)); req=list(map(float,t['k_ladder_Mpc_inv'])); diag=list(map(float,t['diagnostic_scale_factors'])); bind=list(map(float,t['binding_scale_factors'])); epochs=diag+bind
    rel=float(t['pair_activity']['relative_denominator_floor']); minpairs=int(t['pair_activity']['min_active_pairs_per_mode_epoch']); maxdiff=float(t['estimators']['max_allowed_tree_epoch_median_minor_difference'])
    trees={'untouched_upstream_model2':analyze_tree(q.upstream_dir,req,epochs,rel),
           'historical_production_RTK_model2':analyze_tree(q.rtk_dir,req,epochs,rel)}
    ill=any(v['summary']['epochs'][str(a)]['min_active_pairs_10']<minpairs for v in trees.values() for a in bind)
    deriv=any(v['summary']['epochs'][str(a)]['estimator_absolute_difference'] is None or v['summary']['epochs'][str(a)]['estimator_absolute_difference']>maxdiff for v in trees.values() for a in bind)
    vals={name:[v['summary']['epochs'][str(a)]['tree_median_normalized_minor_10'] for a in bind] for name,v in trees.items()}
    if ill: cls=t['classifications']['ill_conditioned']
    elif deriv: cls=t['classifications']['derivative_limited']
    elif all(x<=0.05 for xs in vals.values() for x in xs): cls=t['classifications']['invariant']
    elif all(any(x>=0.25 for x in xs) for xs in vals.values()): cls=t['classifications']['noninvariant']
    else: cls=t['classifications']['mixed']
    out={'schema':'RTK_C10_LEGACY_RT_00_AUXILIARY_COVECTOR_PROPAGATION_RESULT_v1','classification':cls,
         'target':q.target,'trees':trees,'binding_tree_medians_10':vals,
         'normalized_minor_is_seed_rescaling_invariant':True,'physical_coefficients_fitted':False,'production_modified':False}
    Path(q.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for name,v in trees.items(): print(name,v['summary'])
if __name__=='__main__': main()
