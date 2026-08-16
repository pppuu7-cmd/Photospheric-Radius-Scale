#!/usr/bin/env python3
"""Matched local COBYQA navigation on RTK_final_objective_v1.

Usage:
  python3 final_objective_cobyqa_refine.py PLANCK_DIR RTK|LCDM eff|k01 h Ob Om As ns zre [lambda_D]

For RTK, log(lambda_D) is an optimized seventh coordinate. For LCDM, six
cosmological coordinates are optimized. This is a matched final-objective
local navigation step, not a claim of a global minimum or model preference.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
from scipy.optimize import minimize
import inference_core_final as L

if len(sys.argv) not in (10,11):
    raise SystemExit(__doc__)
MODEL=sys.argv[2].upper(); MAPPING=sys.argv[3].lower()
if MODEL not in ('RTK','LCDM') or MAPPING not in ('eff','k01'):
    raise SystemExit('invalid model or mapping')
h,Ob,Om,As,ns,zre=map(float,sys.argv[4:10])
if MODEL=='RTK':
    if len(sys.argv)!=11: raise SystemExit('RTK requires lambda_D')
    lam=float(sys.argv[10])
    if not (lam>0 and math.isfinite(lam)): raise SystemExit('invalid lambda_D')
else:
    lam=0.0
CENTER={'lam':lam,'h':h,'Ob':Ob,'Om':Om,'As':As,'ns':ns,'zre':zre}
width={'h':0.0020,'Ob':0.00040,'Om':0.0040,'As':2.5e-11,'ns':0.0020,'zre':0.40}
names=(['loglam'] if MODEL=='RTK' else [])+['h','Ob','Om','As','ns','zre']
N=len(names)
OUT=Path('output/final_objective_cobyqa')/MODEL.lower()/MAPPING
OUT.mkdir(parents=True,exist_ok=True)
EVALS={}; ROWS=[]; FAILED=0; RETRIES=0

def key(y): return tuple(float(v) for v in np.asarray(y,float))
def target(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])
def y_to_params(y):
    y=np.asarray(y,float); p=dict(CENTER); j=0
    if MODEL=='RTK':
        p['lam']=CENTER['lam']*math.exp(float(y[0])*0.12); j=1
    for i,n in enumerate(['h','Ob','Om','As','ns','zre']):
        p[n]=CENTER[n]+float(y[j+i])*width[n]
    return p

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def is_timeout(r): return r.get('error')=='CLASS_TIMEOUT' or r.get('reason')=='CLASS_TIMEOUT' or 'CLASS_TIMEOUT' in str(r.get('reason',''))
def evaluate_once(p):
    try:return L.evaluate(MODEL,p)
    except Exception as e:return {'ok':False,'error':repr(e)}

def ev(y,label='opt'):
    global FAILED,RETRIES
    y=np.asarray(y,float)
    if np.any(~np.isfinite(y)) or np.any(y<-1.0000001) or np.any(y>1.0000001):
        return {'ok':False,'penalty':1e12,'reason':'outside_box'}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    r=evaluate_once(p)
    if not r.get('ok') and is_timeout(r):
        RETRIES+=1; cleanup(r.get('tag'))
        try:
            ikey=(MODEL,)+tuple(float(p[q]) for q in ['lam','h','Ob','Om','As','ns','zre'])
            L.CACHE.pop(ikey,None)
        except Exception: pass
        r=evaluate_once(p)
    if not r.get('ok'):
        FAILED+=1; rr={'ok':False,'penalty':1e9,'reason':r.get('error',r.get('reason','failed')),'params':p,'y':y.tolist()}; EVALS[k]=rr
        print('FINAL_NAV_FAIL',MODEL,MAPPING,label,rr['reason'],flush=True); return rr
    rr=dict(r); rr['params']=p; rr['y']=y.tolist(); EVALS[k]=rr
    row={'label':label,'model':MODEL,'mapping':MAPPING}; row.update(p)
    for i,n in enumerate(names):row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=r.get(q)
    ROWS.append(row); cleanup(r.get('tag'))
    print('FINAL_NAV_EVAL',MODEL,MAPPING,len(EVALS),target(r),p,flush=True)
    return rr

def obj(y):
    r=ev(y,'cobyqa'); return target(r) if r.get('ok') else float(r['penalty'])

z=np.zeros(N); r0=ev(z,'center')
if not r0.get('ok'): raise SystemExit('center failed')
res=minimize(obj,z,method='COBYQA',bounds=[(-1.,1.)]*N,
             options={'maxfev':60,'maxiter':180,'initial_tr_radius':0.18,
                      'final_tr_radius':0.003,'disp':True})
ev(np.clip(res.x,-1,1),'cobyqa_result')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target); pre_poll=target(best)
for poll in (0.010,0.003):
    seed=np.asarray(min([r for r in EVALS.values() if r.get('ok')],key=target)['y'])
    for i in range(N):
        for s in (-1.,1.):
            y=seed.copy(); y[i]=np.clip(y[i]+s*poll,-1,1)
            if np.allclose(y,seed,atol=1e-15,rtol=0):continue
            ev(y,f'poll_{poll}_{i}_{int(s):+d}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target); final=target(best)
summary={
 'stage':'matched-final-objective-v1-cobyqa-navigation',
 'objective':'RTK_final_objective_v1',
 'model':MODEL,'mapping':MAPPING,'initial_center':CENTER,
 'center_S':target(r0),'best_S':final,'best_params':best['params'],
 'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'poll_improvement_from_pre_poll_best':pre_poll-final,
 'optimizer':{'method':'COBYQA','success':bool(res.success),'message':str(res.message),'fun':float(res.fun),'nfev':int(res.nfev),'nit':int(res.nit),'x':np.asarray(res.x).tolist()},
 'exact_likelihood_calls':int(L.COUNTER),'failed_points':FAILED,'timeout_retries':RETRIES,
 'memoization_key':'exact_float_normalized_coordinates',
 'strict_status':'recenter_required' if pre_poll-final>0 else 'poll_stable_candidate',
 'scope':'matched local navigation only; no global minimum, significance, posterior or evidence claim'
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('FINAL_OBJECTIVE_COBYQA_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('FINAL_OBJECTIVE_COBYQA_PASS',flush=True)
