#!/usr/bin/env python3
"""Stage 4C.1: exact bounded expansion after a Stage 4C boundary hit.

Usage:
  python3 stage4c_expand_optimizer.py PLANCK_DIR SEED.json

The seed must come from a completed Stage 4C artifact and explicitly list one
or more boundary_axes.  The expanded box is centered on the best exact seed
point.  Boundary directions are widened; non-boundary directions are narrowed
for refinement.  This remains a local exact optimization, not a global fit.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
from scipy.optimize import minimize
import inference_core as L

if len(sys.argv)!=3: raise SystemExit(__doc__)
seed_path=Path(sys.argv[2]); seed=json.loads(seed_path.read_text())
MODEL=str(seed.get('model','')).upper(); MAPPING=str(seed.get('mapping','')).lower()
if MODEL not in ('RTK','LCDM') or MAPPING not in ('eff','k01'):
    raise SystemExit('invalid seed model/mapping')
BOUND=set(seed.get('boundary_axes') or [])
if not BOUND: raise SystemExit('seed has no boundary axes; expansion not justified')
CENTER=dict(seed['best_params']); SREF=float(seed['best_S'])
old=dict(seed['previous_halfwidths'])

# New local trust box.  Boundary directions are materially expanded; the other
# axes are tightened around the recovered best exact point.
COORDS=[]
ordered=['loglam','h','Ob','Om','As','ns','zre'] if MODEL=='RTK' else ['h','Ob','Om','As','ns','zre']
for name in ordered:
    if name=='loglam': c=math.log(float(CENTER['lam']))
    else: c=float(CENTER[name])
    hw=float(old[name])
    if name in BOUND:
        # log-lambda gets a generous extension: factor exp(0.55) ~ 1.73 each way.
        new_hw=max(hw*1.55,0.55) if name=='loglam' else hw*1.5
    else:
        new_hw=hw*0.55
    COORDS.append((name,c,new_hw))
N=len(COORDS)
OUT=Path('output/stage4c1')/MODEL.lower()/MAPPING
OUT.mkdir(parents=True,exist_ok=True)
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
    for yi,(name,c,hw) in zip(y,COORDS):
        v=c+float(yi)*hw
        if name=='loglam':p['lam']=math.exp(v)
        else:p[name]=v
    return p

def key(y):return tuple(float(f'{float(v):.10g}') for v in y)
def target(r):return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def evaluate_y(y,label='opt'):
    global FAILED
    y=np.asarray(y,float)
    if np.any(~np.isfinite(y)) or np.any(y<-1.0000001) or np.any(y>1.0000001):
        return {'ok':False,'penalty':1e12,'reason':'outside_expanded_box'}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    try:r=L.evaluate(MODEL,p)
    except Exception as e:r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        FAILED+=1
        rr={'ok':False,'penalty':1e9+FAILED,'reason':r.get('reason',str(r)),'params':p,'y':y.tolist()}
        EVALS[k]=rr;print('EVAL_FAIL',MODEL,MAPPING,label,rr['reason'],p,flush=True);return rr
    rr=dict(r);rr['params']=p;rr['y']=y.tolist();EVALS[k]=rr
    row={'label':label,'model':MODEL,'mapping':MAPPING}
    for i,(name,_,_) in enumerate(COORDS):row['y_'+name]=float(y[i])
    row.update({q:p.get(q) for q in ('lam','h','Ob','Om','As','ns','zre')})
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
        row[q]=r.get(q)
    ROWS.append(row);cleanup(r.get('tag'))
    print('EVAL',MODEL,MAPPING,len(EVALS),target(r),p,flush=True)
    return rr

def objective(y):
    r=evaluate_y(y,'powell')
    return target(r) if r.get('ok') else float(r['penalty'])

z=np.zeros(N);r0=evaluate_y(z,'seed_center')
if not r0.get('ok'):raise SystemExit('seed center likelihood failed')
centerS=target(r0);reg=centerS-SREF
print('SEED_REGRESSION',centerS,SREF,reg,flush=True)
if abs(reg)>0.25:raise SystemExit(f'seed regression failed: {reg}')

bounds=[(-1.,1.)]*N
# Two deterministic starts: exact recovered seed and a modest push in the old
# boundary direction, while preserving all other coordinates.
seed2=np.zeros(N)
for i,(name,_,_) in enumerate(COORDS):
    if name in BOUND: seed2[i]=0.22
starts=[z,seed2]
opt=[]
for idx,start in enumerate(starts):
    res=minimize(objective,start,method='Powell',bounds=bounds,
                 options={'xtol':0.012,'ftol':0.002,'maxfev':145,'maxiter':14,'disp':True})
    opt.append({'start_index':idx,'success':bool(res.success),'message':str(res.message),
                'fun_reported':float(res.fun),'x_reported':np.asarray(res.x).tolist(),
                'nfev':int(res.nfev),'nit':int(res.nit)})
    evaluate_y(np.clip(res.x,-1,1),f'powell_result_{idx}')

valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target);best_y=np.asarray(best['y']);before=target(best)
# Independent smaller poll than Stage 4C because non-boundary axes are already tightened.
poll=0.05
for i in range(N):
    for s in (-1.,1.):
        y=best_y.copy();y[i]=np.clip(y[i]+s*poll,-1,1)
        if np.allclose(y,best_y,rtol=0,atol=1e-14):continue
        evaluate_y(y,f'poll_{i}_{int(s):+d}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target);after=target(best);poll_improvement=before-after

# One compact refine only when exact poll found a meaningful improvement.
refined=False
if poll_improvement>0.03:
    refined=True
    res=minimize(objective,np.asarray(best['y']),method='Powell',bounds=bounds,
                 options={'xtol':0.008,'ftol':0.0015,'maxfev':80,'maxiter':8,'disp':True})
    opt.append({'start_index':'poll_refine','success':bool(res.success),'message':str(res.message),
                'fun_reported':float(res.fun),'x_reported':np.asarray(res.x).tolist(),
                'nfev':int(res.nfev),'nit':int(res.nit)})
    evaluate_y(np.clip(res.x,-1,1),'poll_refine_result')
    valid=[r for r in EVALS.values() if r.get('ok')];best=min(valid,key=target)

best_y=np.asarray(best['y']);boundary=[]
for i,(name,_,_) in enumerate(COORDS):
    if abs(best_y[i])>0.96:boundary.append(name)
status='local_minimum_candidate' if not boundary else 'boundary_hit_expand_again'
summary={
 'stage':'4C.1','status':status,'scope':'expanded_bounded_local_exact_minimization_not_global',
 'model':MODEL,'mapping':MAPPING,'seed_file':str(seed_path),'seed_best_S':SREF,
 'seed_center_regression_S':centerS,'seed_center_regression_delta':reg,
 'center':CENTER,
 'coordinates':[{'name':n,'center_coordinate':c,'halfwidth':w,'normalized_bounds':[-1,1]} for n,c,w in COORDS],
 'optimizer':'scipy.optimize.minimize Powell with bounds','optimizer_runs':opt,
 'exact_likelihood_calls':int(L.COUNTER),'cached_points':len(EVALS),'failed_points':FAILED,
 'poll_step_normalized':poll,'poll_improvement_before_optional_refine':float(poll_improvement),
 'optional_refine_used':refined,'best_S':target(best),'improvement_vs_seed':SREF-target(best),
 'best_y':best_y.tolist(),'best_params':best['params'],
 'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'boundary_axes':boundary,
}
(OUT/'stage4c1_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'stage4c1_trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('STAGE4C1_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4C1_PASS',flush=True)
