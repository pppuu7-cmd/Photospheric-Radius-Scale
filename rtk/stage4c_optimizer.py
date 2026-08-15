#!/usr/bin/env python3
"""Stage 4C: bounded derivative-free exact likelihood minimization.

This stage minimizes the exact CLASS + official Planck + Pantheon + BOSS
objective in a deliberately local trust box around the best Stage 4B points.
It is not a global optimizer, posterior sampler, exclusion test or Bayesian
evidence calculation.

Usage:
    python3 stage4c_optimizer.py PLANCK_DIR RTK|LCDM eff|k01
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
from scipy.optimize import minimize
import inference_core as L

MODEL=(sys.argv[2] if len(sys.argv)>2 else 'RTK').upper()
MAPPING=(sys.argv[3] if len(sys.argv)>3 else 'eff').lower()
if MODEL not in ('RTK','LCDM'):
    raise SystemExit('model must be RTK or LCDM')
if MAPPING not in ('eff','k01'):
    raise SystemExit('mapping must be eff or k01')

# Stage 4B best exact points read from the archived basin_summary.json files.
# The boxes below are intentionally local and must never be reinterpreted as
# global priors.
if MODEL=='RTK':
    CENTER={'lam':1322.8148686858115,'h':0.6840,'Ob':0.0475,'Om':0.260,
            'As':2.037e-9,'ns':0.9630,'zre':6.0}
    COORDS=[
      ('loglam',math.log(CENTER['lam']),0.35),
      ('h',CENTER['h'],0.0100),
      ('Ob',CENTER['Ob'],0.0020),
      ('Om',CENTER['Om'],0.0200),
      ('As',CENTER['As'],0.120e-9),
      ('ns',CENTER['ns'],0.0100),
      ('zre',CENTER['zre'],2.0),
    ]
    STAGE4B={'eff':1059.9993684340136,'k01':1058.9852759905964}
else:
    # Actual Stage 4B best exact point was the exact newton_eff evaluation.
    # Earlier prose accidentally copied a different stencil coordinate.
    CENTER={'lam':0.0,'h':0.6750,'Ob':0.04897309644923192,
            'Om':0.26553983931210706,'As':2.0983169046423643e-9,
            'ns':0.9636847246752313,'zre':7.558399298038399}
    COORDS=[
      ('h',CENTER['h'],0.0100),
      ('Ob',CENTER['Ob'],0.0020),
      ('Om',CENTER['Om'],0.0200),
      ('As',CENTER['As'],0.120e-9),
      ('ns',CENTER['ns'],0.0100),
      ('zre',CENTER['zre'],2.0),
    ]
    STAGE4B={'eff':1051.264741454995,'k01':1051.2653441551797}

N=len(COORDS)
OUT=Path('output/stage4c')/MODEL.lower()/MAPPING
OUT.mkdir(parents=True,exist_ok=True)
EVALS={}
ROWS=[]
FAILED=0


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
    for yi,(name,c,halfwidth) in zip(y,COORDS):
        v=c+float(yi)*halfwidth
        if name=='loglam':p['lam']=math.exp(v)
        else:p[name]=v
    return p


def key(y):
    return tuple(float(f'{float(v):.10g}') for v in y)


def target(r):
    return float(r['score'] if MAPPING=='eff' else r['score_k01'])


def evaluate_y(y,label='opt'):
    global FAILED
    y=np.asarray(y,dtype=float)
    if np.any(~np.isfinite(y)) or np.any(y < -1.0000001) or np.any(y > 1.0000001):
        return {'ok':False,'penalty':1e12,'reason':'outside_local_box'}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    try:
        r=L.evaluate(MODEL,p)
    except Exception as e:
        r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        FAILED+=1
        rr={'ok':False,'penalty':1e9+FAILED,'reason':r.get('reason',str(r)),
            'params':p,'y':y.tolist()}
        EVALS[k]=rr
        print('EVAL_FAIL',MODEL,MAPPING,label,rr['reason'],p,flush=True)
        return rr
    row={'label':label,'model':MODEL,'mapping':MAPPING}
    for i,(name,_,_) in enumerate(COORDS):row['y_'+name]=float(y[i])
    row.update({q:p[q] for q in ('lam','h','Ob','Om','As','ns','zre')})
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
        row[q]=r.get(q)
    ROWS.append(row)
    r=dict(r);r['params']=p;r['y']=y.tolist();EVALS[k]=r
    print('EVAL',MODEL,MAPPING,len(EVALS),target(r),p,flush=True)
    cleanup(r.get('tag'))
    return r


def objective(y):
    r=evaluate_y(y,'powell')
    return target(r) if r.get('ok') else float(r['penalty'])

# Regression of the Stage 4B center through the same exact likelihood path.
z=np.zeros(N)
r0=evaluate_y(z,'center')
if not r0.get('ok'):
    raise SystemExit('center likelihood failed')
center_S=target(r0)
diff=center_S-STAGE4B[MAPPING]
print('CENTER_REGRESSION',MODEL,MAPPING,center_S,STAGE4B[MAPPING],diff,flush=True)
if abs(diff)>0.25:
    raise SystemExit(f'Stage 4B center regression failed: {diff}')

bounds=[(-1.0,1.0)]*N
# Deterministic second start follows the dominant Stage 4B degeneracies only
# weakly, so it tests start dependence without jumping out of the trust box.
if MODEL=='RTK':
    seed2=np.array([0.15,0.18,-0.12,-0.18,0.15,0.05,0.15],dtype=float)
else:
    seed2=np.array([0.18,-0.12,-0.18,0.15,0.05,0.15],dtype=float)
starts=[z,seed2]
opt_results=[]
for istart,start in enumerate(starts):
    res=minimize(objective,start,method='Powell',bounds=bounds,
                 options={'xtol':0.015,'ftol':0.003,'maxfev':115,'maxiter':12,'disp':True})
    opt_results.append({
      'start_index':istart,'success':bool(res.success),'message':str(res.message),
      'fun_reported':float(res.fun),'x_reported':np.asarray(res.x).tolist(),
      'nfev':int(res.nfev),'nit':int(res.nit),
    })
    evaluate_y(np.clip(res.x,-1,1),f'powell_result_{istart}')

valid=[r for r in EVALS.values() if r.get('ok')]
if not valid:raise SystemExit('no valid likelihood evaluations')
best=min(valid,key=target)
best_y=np.asarray(best['y'],dtype=float)
best_before_poll=target(best)

# Independent exact local poll.  This is deliberately not part of Powell.
poll_step=0.06
for i in range(N):
    for s in (-1.0,1.0):
        y=best_y.copy();y[i]=np.clip(y[i]+s*poll_step,-1,1)
        if np.allclose(y,best_y,rtol=0,atol=1e-14):continue
        evaluate_y(y,f'poll_{i}_{int(s):+d}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target)
best_after_poll=target(best)
poll_improvement=best_before_poll-best_after_poll

# If the independent poll found a meaningful improvement, do one short exact
# refinement from that point, then re-select the best exact evaluation.
refined=False
if poll_improvement>0.03:
    refined=True
    res=minimize(objective,np.asarray(best['y']),method='Powell',bounds=bounds,
                 options={'xtol':0.010,'ftol':0.002,'maxfev':70,'maxiter':8,'disp':True})
    opt_results.append({
      'start_index':'poll_refine','success':bool(res.success),'message':str(res.message),
      'fun_reported':float(res.fun),'x_reported':np.asarray(res.x).tolist(),
      'nfev':int(res.nfev),'nit':int(res.nit),
    })
    evaluate_y(np.clip(res.x,-1,1),'poll_refine_result')
    valid=[r for r in EVALS.values() if r.get('ok')]
    best=min(valid,key=target)

best_y=np.asarray(best['y'])
boundary_axes=[]
for i,(name,_,_) in enumerate(COORDS):
    if abs(best_y[i])>0.96:boundary_axes.append(name)

status='local_minimum_candidate'
if boundary_axes:status='boundary_hit_expand_local_box'
elif poll_improvement>0.03 and not refined:status='poll_found_improvement'

summary={
 'stage':'4C',
 'status':status,
 'scope':'bounded_local_exact_minimization_not_global',
 'model':MODEL,'mapping':MAPPING,
 'center':CENTER,
 'stage4b_reference_S':STAGE4B[MAPPING],
 'center_regression_S':center_S,
 'coordinates':[{'name':n,'center_coordinate':c,'halfwidth':w,'normalized_bounds':[-1,1]} for n,c,w in COORDS],
 'optimizer':'scipy.optimize.minimize Powell with bounds',
 'optimizer_runs':opt_results,
 'exact_likelihood_calls':int(L.COUNTER),
 'cached_points':len(EVALS),'failed_points':FAILED,
 'poll_step_normalized':poll_step,
 'poll_improvement_before_optional_refine':float(poll_improvement),
 'optional_refine_used':refined,
 'best_S':target(best),
 'improvement_vs_stage4b':float(STAGE4B[MAPPING]-target(best)),
 'best_y':best_y.tolist(),
 'best_params':best['params'],
 'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'boundary_axes':boundary_axes,
}
(OUT/'stage4c_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')

fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'stage4c_trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)

print('STAGE4C_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4C_PASS',flush=True)
