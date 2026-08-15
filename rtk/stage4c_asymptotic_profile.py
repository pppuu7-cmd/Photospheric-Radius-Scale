#!/usr/bin/env python3
"""Asymptotic RTK local profile at fixed very large lambda_D.

This tests the local lambda_D -> infinity basin suggested by the exact
conditional scan. lambda_D is fixed at 1e8; the six remaining cosmological
parameters are optimized with exact CLASS+Planck+Pantheon+BOSS evaluations.
This is a local asymptotic profile, not a global fit and not evidence that the
true optimum is mathematically at infinity.

Usage: python3 stage4c_asymptotic_profile.py PLANCK_DIR eff|k01
"""
from pathlib import Path
import csv,json,sys
import numpy as np
from scipy.optimize import minimize
import inference_core as L

MAPPING=(sys.argv[2] if len(sys.argv)>2 else 'eff').lower()
if MAPPING not in ('eff','k01'):raise SystemExit('mapping must be eff or k01')
LAM=1.0e8
CENTER={'lam':LAM,'h':0.6876415412107025,'Ob':0.04713370853636241,
        'Om':0.2563078649786827,'As':2.052560909053839e-9,
        'ns':0.9627323451269592,'zre':6.35470443812342}
COORDS=[('h',CENTER['h'],0.006),('Ob',CENTER['Ob'],0.0012),
        ('Om',CENTER['Om'],0.012),('As',CENTER['As'],7.0e-11),
        ('ns',CENTER['ns'],0.006),('zre',CENTER['zre'],1.2)]
N=len(COORDS);OUT=Path('output/stage4c_asymptotic')/MAPPING;OUT.mkdir(parents=True,exist_ok=True)
EVALS={};ROWS=[];FAILED=0

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
    for yi,(n,c,w) in zip(y,COORDS):p[n]=c+float(yi)*w
    return p

def key(y):return tuple(float(f'{float(v):.10g}') for v in y)
def target(r):return float(r['score'] if MAPPING=='eff' else r['score_k01'])
def ev(y,label='opt'):
    global FAILED
    y=np.asarray(y,float)
    if np.any(~np.isfinite(y)) or np.any(y<-1.0000001) or np.any(y>1.0000001):return {'ok':False,'penalty':1e12}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    try:r=L.evaluate('RTK',p)
    except Exception as e:r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        FAILED+=1;rr={'ok':False,'penalty':1e9+FAILED,'reason':r.get('reason',str(r))};EVALS[k]=rr;return rr
    rr=dict(r);rr['params']=p;rr['y']=y.tolist();EVALS[k]=rr
    row={'label':label,'mapping':MAPPING};row.update(p)
    for i,(n,_,_) in enumerate(COORDS):row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=r.get(q)
    ROWS.append(row);cleanup(r.get('tag'));print('EVAL',MAPPING,len(EVALS),target(r),p,flush=True);return rr

def obj(y):
    r=ev(y,'powell');return target(r) if r.get('ok') else r['penalty']

z=np.zeros(N);r0=ev(z,'center')
if not r0.get('ok'):raise SystemExit('asymptotic center failed')
bounds=[(-1.,1.)]*N
seed2=np.array([0.12,-0.10,-0.12,0.10,0.05,0.10])
opts=[]
for idx,start in enumerate((z,seed2)):
    res=minimize(obj,start,method='Powell',bounds=bounds,
                 options={'xtol':0.012,'ftol':0.002,'maxfev':130,'maxiter':13,'disp':True})
    opts.append({'start':idx,'success':bool(res.success),'fun':float(res.fun),'x':np.asarray(res.x).tolist(),'nfev':int(res.nfev),'nit':int(res.nit)})
    ev(np.clip(res.x,-1,1),f'result_{idx}')
valid=[r for r in EVALS.values() if r.get('ok')];best=min(valid,key=target);by=np.asarray(best['y']);before=target(best)
poll=0.05
for i in range(N):
    for s in (-1.,1.):
        y=by.copy();y[i]=np.clip(y[i]+s*poll,-1,1)
        if np.allclose(y,by,atol=1e-14,rtol=0):continue
        ev(y,f'poll_{i}_{int(s):+d}')
valid=[r for r in EVALS.values() if r.get('ok')];best=min(valid,key=target);after=target(best)
boundary=[COORDS[i][0] for i,v in enumerate(best['y']) if abs(v)>0.96]
status='asymptotic_local_minimum_candidate' if not boundary else 'asymptotic_boundary_hit'
summary={'stage':'4C-asymptotic','status':status,'scope':'fixed_lambda_1e8_local_exact_profile_not_global',
         'lambda_D_fixed':LAM,'mapping':MAPPING,'center_S':target(r0),'best_S':target(best),
         'improvement_from_center':target(r0)-target(best),'best_params':best['params'],
         'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
         'boundary_axes':boundary,'poll_improvement':before-after,'exact_likelihood_calls':int(L.COUNTER),
         'failed_points':FAILED,'optimizer_runs':opts,
         'coordinates':[{'name':n,'center':c,'halfwidth':w} for n,c,w in COORDS],
         'warning':'This profiles the large-lambda asymptotic basin only. It is not proof that the global finite-lambda likelihood maximum occurs at infinity.'}
(OUT/'asymptotic_profile_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'asymptotic_profile_trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('ASYMPTOTIC_PROFILE_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('ASYMPTOTIC_PROFILE_PASS',flush=True)
