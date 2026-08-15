#!/usr/bin/env python3
"""Tight exact fixed-lambda refinement around an externally supplied RTK center.

Usage:
  python3 stage4d1_tight_refine.py PLANCK_DIR LAMBDA_D eff|k01 h Ob Om As ns zre

This is a local numerical refinement only. It does not establish a global
profile, posterior, confidence interval, or Bayesian evidence.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
from scipy.optimize import minimize
import inference_core as L

if len(sys.argv) != 10:
    raise SystemExit(__doc__)
LAM=float(sys.argv[2]); MAPPING=sys.argv[3].lower()
if MAPPING not in ('eff','k01') or not (LAM>0 and math.isfinite(LAM)):
    raise SystemExit('invalid lambda_D or mapping')
names=['h','Ob','Om','As','ns','zre']
vals=list(map(float,sys.argv[4:10]))
CENTER={'lam':LAM,**dict(zip(names,vals))}
# Tight but still conservative relative to the 4D0 Newton displacement.
width={'h':0.0020,'Ob':0.00040,'Om':0.0040,'As':2.5e-11,'ns':0.0020,'zre':0.40}
COORDS=[(n,CENTER[n],width[n]) for n in names]
N=len(COORDS)
label=(f'{LAM:.0f}' if LAM<1e7 else f'{LAM:.0e}').replace('+','')
OUT=Path('output/stage4d1_tight')/MAPPING/label
OUT.mkdir(parents=True,exist_ok=True)
EVALS={}; ROWS=[]; FAILED=0

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def y_to_params(y):
    p=dict(CENTER)
    for yi,(n,c,w) in zip(y,COORDS): p[n]=c+float(yi)*w
    return p

def key(y): return tuple(float(f'{float(v):.11g}') for v in y)
def target(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def ev(y,tag='opt'):
    global FAILED
    y=np.asarray(y,float)
    if np.any(~np.isfinite(y)) or np.any(y<-1.0000001) or np.any(y>1.0000001):
        return {'ok':False,'penalty':1e12,'reason':'outside_box'}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    try:r=L.evaluate('RTK',p)
    except Exception as e:r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        FAILED+=1; rr={'ok':False,'penalty':1e9+FAILED,'reason':r.get('reason',str(r)),'params':p,'y':y.tolist()};EVALS[k]=rr
        print('EVAL_FAIL',LAM,MAPPING,tag,rr['reason'],flush=True);return rr
    rr=dict(r); rr['params']=p; rr['y']=y.tolist(); EVALS[k]=rr
    row={'label':tag,'lambda_D':LAM,'mapping':MAPPING}; row.update(p)
    for i,(n,_,_) in enumerate(COORDS): row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'): row[q]=r.get(q)
    ROWS.append(row); cleanup(r.get('tag'))
    print('EVAL',LAM,MAPPING,len(EVALS),target(r),p,flush=True); return rr

def obj(y):
    r=ev(y,'powell'); return target(r) if r.get('ok') else float(r['penalty'])

z=np.zeros(N); r0=ev(z,'center')
if not r0.get('ok'): raise SystemExit('center failed')
bounds=[(-1.,1.)]*N
starts=[
 z,
 np.array([ 0.18,-0.12,-0.18, 0.10,-0.10, 0.12]),
 np.array([-0.18, 0.12, 0.18,-0.10, 0.10,-0.12]),
 np.array([ 0.10,-0.10,-0.10,-0.05, 0.10, 0.05]),
 np.array([-0.10, 0.10, 0.10, 0.05,-0.10,-0.05]),
]
opts=[]
for idx,start in enumerate(starts):
    res=minimize(obj,start,method='Powell',bounds=bounds,
                 options={'xtol':0.003,'ftol':0.00015,'maxfev':260,'maxiter':24,'disp':True})
    opts.append({'start':idx,'success':bool(res.success),'fun':float(res.fun),'x':np.asarray(res.x).tolist(),'nfev':int(res.nfev),'nit':int(res.nit)})
    ev(np.clip(res.x,-1,1),f'result_{idx}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target); before=target(best); by=np.asarray(best['y'])
# Two exact poll radii to catch residual gradients.
for poll in (0.025,0.010):
    seed=np.asarray(min([r for r in EVALS.values() if r.get('ok')],key=target)['y'])
    for i in range(N):
        for s in (-1.,1.):
            y=seed.copy(); y[i]=np.clip(y[i]+s*poll,-1,1)
            if np.allclose(y,seed,atol=1e-14,rtol=0):continue
            ev(y,f'poll_{poll}_{i}_{int(s):+d}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target); after=target(best)
boundary=[COORDS[i][0] for i,v in enumerate(best['y']) if abs(v)>0.97]
summary={
 'stage':'4D1-tight-fixed-lambda-refinement',
 'status':'tight_local_candidate' if not boundary else 'tight_local_boundary_hit',
 'scope':'local_refinement_only_not_global_profile_or_posterior',
 'lambda_D':LAM,'mapping':MAPPING,'initial_center':CENTER,'center_S':target(r0),
 'best_S':target(best),'best_params':best['params'],
 'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'boundary_axes':boundary,'poll_improvement_from_pre_poll_best':before-after,
 'exact_likelihood_calls':int(L.COUNTER),'failed_points':FAILED,'optimizer_runs':opts,
 'coordinates':[{'name':n,'center':c,'halfwidth':w} for n,c,w in COORDS],
 'warning':'Tight local refinement only. Globality and lambda-direction behavior require the assembled profile and posterior/calibration.'
}
(OUT/'refine_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'refine_trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(ROWS)
print('STAGE4D1_TIGHT_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D1_TIGHT_PASS',flush=True)
