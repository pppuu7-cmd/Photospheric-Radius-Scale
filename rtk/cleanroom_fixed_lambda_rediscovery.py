#!/usr/bin/env python3
"""Independent fixed-lambda rediscovery for RTK.

Unlike stage4d1_fixed_lambda_profile.py this script uses no artifact-derived
anchors and no current-best point.  Each lambda is optimized from the same
predeclared broad cosmological box and deterministic neutral starts.  It is a
clean-room basin-discovery tool, not a posterior or a proof of globality.

Usage:
  python3 cleanroom_fixed_lambda_rediscovery.py PLANCK_DIR lambda_D eff|k01
"""
from pathlib import Path
import csv,json,math,sys
import numpy as np
from scipy.optimize import minimize
import inference_core as L

if len(sys.argv)!=4: raise SystemExit(__doc__)
LAM=float(sys.argv[2]); MAPPING=sys.argv[3].lower()
if MAPPING not in ('eff','k01') or not (LAM>0 and math.isfinite(LAM)):
    raise SystemExit('invalid lambda_D or mapping')

# Declared a priori broad box; deliberately independent of the current RTK best.
BOUNDS={
 'h':(0.64,0.74),
 'Ob':(0.040,0.055),
 'Om':(0.20,0.34),
 'As':(1.80e-9,2.35e-9),
 'ns':(0.92,1.01),
 'zre':(4.5,9.5),
}
NAMES=['h','Ob','Om','As','ns','zre']
CENTER={k:0.5*(BOUNDS[k][0]+BOUNDS[k][1]) for k in NAMES}
HALF={k:0.5*(BOUNDS[k][1]-BOUNDS[k][0]) for k in NAMES}
# Deterministic symmetric starts chosen in normalized coordinates only.
STARTS=[
 np.zeros(6),
 np.array([ .35,-.25,-.35, .20, .15,-.20]),
 np.array([-.35, .25, .35,-.20,-.15, .20]),
]
OUT=Path('output/cleanroom_rediscovery')/MAPPING/(f'{LAM:.8g}'.replace('+',''))
OUT.mkdir(parents=True,exist_ok=True)
EVALS={}; ROWS=[]; FAILED=0; RETRIES=0
FAIL_PENALTY=1e9

def y_to_params(y):
    p={'lam':LAM}
    for yi,k in zip(np.asarray(y,float),NAMES): p[k]=CENTER[k]+float(yi)*HALF[k]
    return p

def key(y): return tuple(float(v) for v in np.asarray(y,float))
def target(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])
def is_timeout(r):
    return r.get('error')=='CLASS_TIMEOUT' or r.get('reason')=='CLASS_TIMEOUT' or 'CLASS_TIMEOUT' in str(r.get('reason',''))

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def once(p):
    try:return L.evaluate('RTK',p)
    except Exception as e:return {'ok':False,'reason':repr(e)}

def ev(y,label):
    global FAILED,RETRIES
    y=np.asarray(y,float)
    if np.any(~np.isfinite(y)) or np.any(y < -1.0000001) or np.any(y > 1.0000001):
        return {'ok':False,'penalty':1e12,'reason':'outside_box'}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y); r=once(p)
    if not r.get('ok') and is_timeout(r):
        RETRIES+=1; cleanup(r.get('tag')); r=once(p)
    if not r.get('ok'):
        FAILED+=1
        rr={'ok':False,'penalty':FAIL_PENALTY,'reason':r.get('error',r.get('reason',str(r))),'params':p,'y':y.tolist()}
        EVALS[k]=rr; print('REDISCOVERY_FAIL',MAPPING,LAM,label,rr['reason'],flush=True); return rr
    rr=dict(r); rr['params']=p; rr['y']=y.tolist(); EVALS[k]=rr
    row={'label':label,'mapping':MAPPING,**p}
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=r.get(q)
    ROWS.append(row); cleanup(r.get('tag'))
    print('REDISCOVERY_EVAL',MAPPING,LAM,len(EVALS),target(r),p,flush=True)
    return rr

def obj(y):
    r=ev(y,'cobyqa'); return target(r) if r.get('ok') else float(r['penalty'])

runs=[]
for i,start in enumerate(STARTS):
    r0=ev(start,f'start_{i}')
    if not r0.get('ok'): continue
    try:
        res=minimize(obj,start,method='COBYQA',bounds=[(-1.,1.)]*6,
          options={'maxfev':260,'maxiter':360,'initial_tr_radius':0.35,'final_tr_radius':0.003,'disp':True})
    except Exception as e:
        runs.append({'start':i,'error':repr(e)}); continue
    ev(np.clip(res.x,-1,1),f'result_{i}')
    runs.append({'start':i,'success':bool(res.success),'fun':float(res.fun),'nfev':int(res.nfev),'nit':int(res.nit),'x':np.asarray(res.x).tolist(),'message':str(res.message)})

valid=[r for r in EVALS.values() if r.get('ok')]
if not valid: raise SystemExit('no successful exact likelihood evaluations')
best=min(valid,key=target); before=target(best); seed=np.asarray(best['y'])
# A coarse independent coordinate poll guards against premature optimizer stop.
for j in range(6):
    for sg in (-1.,1.):
        y=seed.copy(); y[j]=np.clip(y[j]+sg*0.03,-1.,1.)
        if not np.allclose(y,seed,atol=1e-14,rtol=0): ev(y,f'poll_{j}_{int(sg):+d}')
valid=[r for r in EVALS.values() if r.get('ok')]; best=min(valid,key=target); after=target(best)
boundary=[NAMES[i] for i,v in enumerate(best['y']) if abs(v)>0.97]
summary={
 'stage':'clean-room-fixed-lambda-rediscovery','scope':'neutral_seed_broad_box_basin_discovery_not_global_posterior',
 'mapping':MAPPING,'lambda_D':LAM,'bounds':BOUNDS,'starts':[s.tolist() for s in STARTS],
 'best_S':target(best),'best_params':best['params'],'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'poll_improvement':before-after,'boundary_axes':boundary,'optimizer_runs':runs,
 'exact_likelihood_calls':int(L.COUNTER),'failed_points':FAILED,'timeout_retries':RETRIES,
 'memoization_key':'exact_float_normalized_coordinates','initialization':'no_artifact_anchors_no_current_best_seed'
}
(OUT/'rediscovery_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'rediscovery_trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(ROWS)
print('CLEANROOM_REDISCOVERY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('CLEANROOM_REDISCOVERY_PASS',flush=True)
