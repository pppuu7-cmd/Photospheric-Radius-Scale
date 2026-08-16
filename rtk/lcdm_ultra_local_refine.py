#!/usr/bin/env python3
"""Exact bounded LCDM local refinement at matched ultra CLASS precision.

Starts from the best harvested exact-float LCDM candidate and refines six
nuisance/cosmological coordinates. This is a local numerical control, not a
global fit, posterior, evidence or model-selection result.
"""
from pathlib import Path
import csv,json,sys
import numpy as np
from scipy.optimize import minimize
import inference_core as core

MAPPING=(sys.argv[2] if len(sys.argv)>2 else 'eff').lower()
if MAPPING not in ('eff','k01'): raise SystemExit('mapping must be eff or k01')
CENTER={'lam':0.0,'h':0.6780618719300789,'Ob':0.04876205689548621,
        'Om':0.26191636161657555,'As':2.1105202470513124e-9,
        'ns':0.9651623965474088,'zre':7.8629952806182}
COORDS=[('h',CENTER['h'],0.0020),('Ob',CENTER['Ob'],0.00040),
        ('Om',CENTER['Om'],0.0040),('As',CENTER['As'],2.5e-11),
        ('ns',CENTER['ns'],0.0020),('zre',CENTER['zre'],0.40)]
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4',
       'tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125',
       'k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
       'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
N=len(COORDS); EVALS={}; ROWS=[]; FAILED=0
orig=core.make_ini
def make_ini(model,p,tag):
    path=orig(model,p,tag)
    with Path(path).open('a') as f:
        f.write('\n# matched ultra LCDM refinement\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
core.make_ini=make_ini

def y_to_p(y):
    p=dict(CENTER)
    for yi,(name,c,w) in zip(y,COORDS): p[name]=c+float(yi)*w
    return p

def key(y): return tuple(float(f'{float(v):.12g}') for v in y)
def target(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])
def ev(y,label):
    global FAILED
    y=np.asarray(y,float)
    if np.any(y < -1.0000001) or np.any(y > 1.0000001): return {'ok':False,'penalty':1e12}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_p(y); core.CACHE.clear(); r=core.evaluate('LCDM',p)
    if not r.get('ok',False):
        FAILED+=1; rr={'ok':False,'penalty':1e9+FAILED,'reason':r.get('reason','failed'),'p':p,'y':y.tolist()};EVALS[k]=rr;return rr
    rr=dict(r);rr['p']=p;rr['y']=y.tolist();EVALS[k]=rr
    row={'label':label,'mapping':MAPPING,**p,'score_eff':r['score'],'score_k01':r['score_k01'],
         'logL_planck':r['logL_planck'],'chi2_SN':r['chi2_SN'],
         'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd']}
    ROWS.append(row);print('LCDM_ULTRA_POINT',json.dumps(row,sort_keys=True),flush=True);return rr
def obj(y):
    r=ev(y,'powell');return target(r) if r.get('ok') else r['penalty']

z=np.zeros(N); r0=ev(z,'center')
if not r0.get('ok'): raise SystemExit('center failed')
starts=[z,np.array([0.12,-0.08,-0.12,0.10,0.04,0.10])]
opts=[]
for i,s in enumerate(starts):
    res=minimize(obj,s,method='Powell',bounds=[(-1,1)]*N,
                 options={'xtol':0.008,'ftol':0.001,'maxfev':180,'maxiter':18,'disp':True})
    opts.append({'start':i,'success':bool(res.success),'fun':float(res.fun),'nfev':int(res.nfev),'nit':int(res.nit),'x':np.asarray(res.x).tolist()})
    ev(np.clip(res.x,-1,1),f'result_{i}')
valid=[r for r in EVALS.values() if r.get('ok')]; best=min(valid,key=target)
pre=target(best); by=np.asarray(best['y']); poll=0.03
for i in range(N):
    for s in (-1,1):
        y=by.copy(); y[i]=np.clip(y[i]+s*poll,-1,1); ev(y,f'poll_{i}_{s:+d}')
valid=[r for r in EVALS.values() if r.get('ok')]; best=min(valid,key=target)
bound=[COORDS[i][0] for i,v in enumerate(best['y']) if abs(v)>0.96]
out=Path('output/lcdm_ultra_local_refine')/MAPPING;out.mkdir(parents=True,exist_ok=True)
summary={'stage':'LCDM-ultra-local-refine','mapping':MAPPING,'scope':'bounded local exact refinement only',
         'ultra_overrides':ULTRA,'center':CENTER,'center_S':target(r0),'best_S':target(best),
         'improvement_from_center':target(r0)-target(best),'best_params':best['p'],'best_y':best['y'],
         'poll_improvement_from_pre_poll':pre-target(best),'boundary_axes':bound,
         'optimizer_runs':opts,'evaluated_points':len(EVALS),'failed_points':FAILED,
         'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')}}
(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
if ROWS:
    with (out/'trace.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(ROWS[0].keys()));w.writeheader();w.writerows(ROWS)
print('LCDM_ULTRA_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('LCDM_ULTRA_COMPLETE',flush=True)
