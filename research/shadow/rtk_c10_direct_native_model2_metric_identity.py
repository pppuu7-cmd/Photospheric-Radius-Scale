#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json
from pathlib import Path
import numpy as np

COLS=['c10dn_k','c10dn_Rpsi','c10dn_R0i','c10dn_psi','c10dn_psi_rhs','c10dn_phip','c10dn_phip_rhs']

def read(path):
    txt=Path(path).read_text()
    miss=[c for c in COLS if c not in txt]
    if miss: raise RuntimeError(f'missing {miss} in {path}')
    a=np.loadtxt(path)
    if a.ndim==1: a=a[None,:]
    tail=a[:,-len(COLS):]
    c={n:tail[:,i] for i,n in enumerate(COLS)}
    return {'path':path,'tau':a[:,0],'a':a[:,1],'c':c,'k':float(np.mean(c['c10dn_k']))}

def sample_at_a(tab,a0):
    out={'a':float(a0),'k':tab['k']}
    for n,y in tab['c'].items(): out[n]=float(np.interp(a0,tab['a'],y))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--upstream-glob',required=True)
    ap.add_argument('--rtk-glob',required=True)
    ap.add_argument('--target',required=True)
    ap.add_argument('--output',required=True)
    q=ap.parse_args()
    t=json.load(open(q.target))
    req=list(map(float,t['k_ladder_Mpc_inv']))
    epochs=list(map(float,t['binding_scale_factors']))
    lim=t['acceptance']
    trees={
      'untouched_upstream':sorted([read(p) for p in glob.glob(q.upstream_glob)],key=lambda z:z['k']),
      'production_rtk':sorted([read(p) for p in glob.glob(q.rtk_glob)],key=lambda z:z['k'])
    }
    results={}; allpass=True
    for name,tabs in trees.items():
      if len(tabs)!=len(req): raise SystemExit(f'{name}: k count {len(tabs)} != {len(req)}')
      for tab,k in zip(tabs,req):
        if abs(tab['k']-k)>1e-12*max(1.,abs(k)): raise SystemExit(f'{name}: k mismatch {tab["k"]} {k}')
      samples=[sample_at_a(tab,a0) for a0 in epochs for tab in tabs]
      finite=all(np.isfinite([s[c] for s in samples for c in COLS]))
      maxpsi=max(abs(s['c10dn_Rpsi']) for s in samples)
      max0i=max(abs(s['c10dn_R0i']) for s in samples)
      passed=finite and maxpsi<=float(lim['max_abs_R_psi']) and max0i<=float(lim['max_abs_R_0i'])
      allpass &= passed
      results[name]={
        'passed':passed,'all_samples_finite':finite,'max_abs_R_psi':maxpsi,'max_abs_R_0i':max0i,
        'sample_count':len(samples),'samples':samples
      }
    cls=t['pass_classification'] if allpass else t['fail_classification']
    out={
      'schema':'RTK_C10_DIRECT_NATIVE_MODEL2_METRIC_IDENTITY_RESULT_v1',
      'classification':cls,
      'target':q.target,
      'trees':results,
      'actual_k_values_Mpc_inv':req,
      'binding_scale_factors':epochs,
      'production_modified':False,
      'interpretation':'Direct residuals of the literal model=2 psi and phi-prime/0i code equations. This does not independently certify a Hamiltonian/00 equation.'
    }
    Path(q.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for n,r in results.items(): print(n,'pass=',r['passed'],'maxRpsi=',r['max_abs_R_psi'],'maxR0i=',r['max_abs_R_0i'])
if __name__=='__main__': main()
