#!/usr/bin/env python3
"""B10 T2 exact fixed-lambda 6D profile candidate worker.

Lambda is fixed to one mechanically selected preregistered tail anchor. Only the
six shared cosmological coordinates are profiled. The result is a T2 candidate,
not a stationarity proof and not a B10 classification.
"""
from pathlib import Path
import copy,csv,json,math,os,sys,time
import numpy as np
from scipy.optimize import minimize

sys.argv=['b10_fixed_lambda_profile_seed','planck_data']
import inference_core as L

if len(os.environ.get('B10_FACTOR',''))==0:
    raise RuntimeError('B10_FACTOR environment variable is required')
FACTOR=float(os.environ['B10_FACTOR'])
ROOT=Path('..')
STATE=json.loads((ROOT/'research/state/current.json').read_text())
TARGET=json.loads((ROOT/'research/robustness/b10_t2_fixed_lambda_profile_targets.json').read_text())
if TARGET['classification']!='B10_T2_TARGETS_FROZEN_BEFORE_FIRST_PROFILE':
    raise RuntimeError('B10 T2 target classification mismatch')
if TARGET['objective']!=STATE['objective']['name']:
    raise RuntimeError('B10 T2 objective mismatch')
anchors={float(x['factor']):x for x in TARGET['anchors']}
if FACTOR not in anchors:
    raise RuntimeError(f'factor {FACTOR} is not a frozen B10 T2 anchor')
LAMBDA=float(anchors[FACTOR]['lambda_D'])
START=copy.deepcopy(STATE['rtk']['accepted_score_params']);START['lam']=LAMBDA
AXES=list(TARGET['optimizer_axes']);SCALE={k:float(v) for k,v in TARGET['optimizer_scales'].items()}
PHYS={k:tuple(map(float,v)) for k,v in TARGET['physical_bounds'].items()}
OPT=TARGET['optimizer']
OBJ=STATE['objective']['name'];DENSE=STATE['objective']['dense_z_pk'];ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
ORIG=L.make_ini

def make_ini(model,p,tag):
    path=ORIG(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('sparse z_pk baseline missing')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    text+='\n# B10 T2 exact fixed-lambda 6D profile\n'+''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text);return path
L.make_ini=make_ini

OUT=Path('../output/b10_t2_fixed_lambda')/('f'+str(int(FACTOR)))
OUT.mkdir(parents=True,exist_ok=True);JOURNAL=OUT/'points.jsonl';SUMMARY=OUT/'summary.json';TRACE=OUT/'trace.csv'
SUCCESS={};ROWS=[];NREQ=0

def from_y(y):
    p=copy.deepcopy(START);p['lam']=LAMBDA
    for a,v in zip(AXES,np.asarray(y,float)):p[a]=float(START[a])+SCALE[a]*float(v)
    return p

def bounds():
    return [((PHYS[a][0]-float(START[a]))/SCALE[a],(PHYS[a][1]-float(START[a]))/SCALE[a]) for a in AXES]
BOUNDS=bounds()

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def key(p):return tuple(float(p[k]).hex() for k in ('lam','h','Ob','Om','As','ns','zre'))

def violations(p):
    bad=[]
    if float(p['lam'])!=LAMBDA:bad.append({'axis':'lam','error':'lambda_not_fixed'})
    for a in AXES:
        v=float(p[a]);lo,hi=PHYS[a]
        if not math.isfinite(v) or v<lo or v>hi:bad.append({'axis':a,'value':v,'lower':lo,'upper':hi})
    return bad

def ev(p,label):
    global NREQ
    bad=violations(p)
    if bad:return {'ok':False,'error':'PHYSICAL_BOUNDS_REJECTION','violations':bad}
    k=key(p)
    if k in SUCCESS:return SUCCESS[k]
    last=None
    for attempt in range(1,4):
        NREQ+=1;L.CACHE.clear()
        try:r=L.evaluate('RTK',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            rr=dict(r);rr['params']=copy.deepcopy(p);rr['label']=label;rr['attempt']=attempt
            SUCCESS[k]=rr;cleanup(rr.get('tag'))
            row={'label':label,'attempt':attempt,'score_eff':float(rr['score']),'score_k01':float(rr['score_k01']),
                 'lambda_D':LAMBDA,**{a:float(p[a]) for a in AXES}}
            for q in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=rr.get(q)
            ROWS.append(row)
            with JOURNAL.open('a') as f:f.write(json.dumps(rr,sort_keys=True,default=str)+'\n')
            print('B10_T2_POINT',json.dumps(row,sort_keys=True),flush=True);return rr
        last=r;cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'{label}: failed after 3 exact retries: {last}')

r0=ev(START,'fixed_shared_start');S0=float(r0['score'])
CALL=0
def fun(y):
    global CALL
    CALL+=1
    r=ev(from_y(y),f'powell_{CALL:04d}')
    return float(r['score']) if r.get('ok') else 1e30
res=minimize(fun,np.zeros(len(AXES)),method=str(OPT['method']),bounds=BOUNDS,
             options={'maxfev':int(OPT['maxfev']),'xtol':float(OPT['xtol']),'ftol':float(OPT['ftol']),'disp':True})
ev(from_y(res.x),'powell_return')
best=min(SUCCESS.values(),key=lambda r:float(r['score']))
if ROWS:
    with TRACE.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(ROWS[0]));w.writeheader();w.writerows(ROWS)
summary={
 'classification':'B10_T2_FIXED_LAMBDA_PROFILE_CANDIDATE_COMPLETE','objective':OBJ,'production_mapping':'eff',
 'factor':FACTOR,'lambda_D':LAMBDA,'anchor_role':anchors[FACTOR]['role'],'target':TARGET,
 'fixed_shared_start_score_eff':S0,'best_score_eff':float(best['score']),'best_score_k01':float(best['score_k01']),
 'profile_improvement':S0-float(best['score']),'best_params':best['params'],
 'best_components':{k:best.get(k) for k in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'exact_requests':NREQ,'unique_success_points':len(SUCCESS),
 'optimizer_result':{'success':bool(res.success),'message':str(res.message),'nfev':int(res.nfev),'fun':float(res.fun),'x':res.x.tolist()},
 'next_required_gate':'T3 fixed-lambda 6D stationarity certification','warning':'T2 profile candidate only; not a certified tail minimum, not a global-minimum claim, and not a B10 closure.'}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('B10_T2_FIXED_LAMBDA_PROFILE_CANDIDATE_COMPLETE',json.dumps(summary,sort_keys=True),flush=True)
