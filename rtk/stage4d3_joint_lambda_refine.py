#!/usr/bin/env python3
"""Seven-dimensional local COBYQA refinement including lambda_D.

Usage:
  python3 stage4d3_joint_lambda_refine.py PLANCK_DIR eff|k01 lambda0 h Ob Om As ns zre

The seventh coordinate is log(lambda_D/lambda0), so positivity is exact and
the optimizer can test whether the finite-lambda trough is an interior local
minimum rather than an artifact of a fixed-lambda grid.

This remains a local likelihood optimization, not a global posterior,
confidence construction, significance, or Bayesian evidence calculation.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
from scipy.optimize import minimize
import inference_core as L

if len(sys.argv) != 10:
    raise SystemExit(__doc__)
MAPPING=sys.argv[2].lower(); LAM0=float(sys.argv[3])
if MAPPING not in ('eff','k01') or not (LAM0>0 and math.isfinite(LAM0)):
    raise SystemExit('invalid lambda0 or mapping')
names=['h','Ob','Om','As','ns','zre']
vals=list(map(float,sys.argv[4:10]))
CENTER={'lam':LAM0,**dict(zip(names,vals))}
width={'h':0.0020,'Ob':0.00040,'Om':0.0040,'As':2.5e-11,'ns':0.0020,'zre':0.40}
LOG_LAM_HALFWIDTH=1.20
COORDS=[('loglam',0.0,LOG_LAM_HALFWIDTH)]+[(n,CENTER[n],width[n]) for n in names]
N=len(COORDS)
OUT=Path('output/stage4d3_joint_lambda')/MAPPING
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
    y=np.asarray(y,float)
    p=dict(CENTER)
    p['lam']=LAM0*math.exp(float(y[0])*LOG_LAM_HALFWIDTH)
    for yi,(n,c,w) in zip(y[1:],COORDS[1:]):
        p[n]=c+float(yi)*w
    return p

def key(y): return tuple(float(v) for v in np.asarray(y,float))
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
        FAILED+=1
        rr={'ok':False,'penalty':1e9+FAILED,'reason':r.get('reason',str(r)),'params':p,'y':y.tolist()}
        EVALS[k]=rr
        print('EVAL_FAIL',MAPPING,tag,rr['reason'],flush=True)
        return rr
    rr=dict(r); rr['params']=p; rr['y']=y.tolist(); EVALS[k]=rr
    row={'label':tag,'mapping':MAPPING}; row.update(p)
    for i,(n,_,_) in enumerate(COORDS): row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'): row[q]=r.get(q)
    ROWS.append(row); cleanup(r.get('tag'))
    print('EVAL',MAPPING,len(EVALS),target(r),p,flush=True)
    return rr

def obj(y):
    r=ev(y,'cobyqa'); return target(r) if r.get('ok') else float(r['penalty'])

z=np.zeros(N); r0=ev(z,'center')
if not r0.get('ok'): raise SystemExit('center failed')
bounds=[(-1.,1.)]*N
try:
    res=minimize(obj,z,method='COBYQA',bounds=bounds,
                 options={'maxfev':520,'maxiter':700,'initial_tr_radius':0.25,
                          'final_tr_radius':0.00035,'disp':True})
except Exception as e:
    raise SystemExit('COBYQA unavailable or failed to initialize: '+repr(e))
ev(np.clip(res.x,-1,1),'cobyqa_result')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target); before=target(best)
# Exact local 7-D coordinate polls.
for poll in (0.010,0.003):
    seed=np.asarray(min([r for r in EVALS.values() if r.get('ok')],key=target)['y'])
    for i in range(N):
        for sg in (-1.,1.):
            y=seed.copy(); y[i]=np.clip(y[i]+sg*poll,-1,1)
            if np.allclose(y,seed,atol=1e-14,rtol=0):continue
            ev(y,f'poll_{poll}_{i}_{int(sg):+d}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target); after=target(best)
boundary=[COORDS[i][0] for i,v in enumerate(best['y']) if abs(v)>0.97]
summary={
 'stage':'4D3-seven-dimensional-lambda-refinement',
 'status':'interior_local_candidate' if not boundary else 'local_boundary_hit',
 'scope':'seven_dimensional_local_optimizer_including_log_lambda_not_global_posterior_or_evidence',
 'mapping':MAPPING,'lambda0':LAM0,'log_lambda_halfwidth':LOG_LAM_HALFWIDTH,
 'lambda_bounds':[LAM0*math.exp(-LOG_LAM_HALFWIDTH),LAM0*math.exp(LOG_LAM_HALFWIDTH)],
 'initial_center':CENTER,'center_S':target(r0),'best_S':target(best),'best_params':best['params'],
 'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'boundary_axes':boundary,'poll_improvement_from_pre_poll_best':before-after,
 'optimizer':{'method':'COBYQA','success':bool(res.success),'message':str(res.message),
              'fun':float(res.fun),'nfev':int(res.nfev),'nit':int(res.nit),'x':np.asarray(res.x).tolist()},
 'memoization_key':'exact_float_normalized_coordinates',
 'exact_likelihood_calls':int(L.COUNTER),'failed_points':FAILED,
 'coordinates':[{'name':n,'center':c,'halfwidth':w} for n,c,w in COORDS],
 'warning':'Local 7-D optimization only. A numerical interior minimum still requires a local Hessian/stationarity check including the lambda direction.'
}
(OUT/'joint_lambda_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'joint_lambda_trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(ROWS)
print('STAGE4D3_JOINT_LAMBDA_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D3_JOINT_LAMBDA_PASS',flush=True)
