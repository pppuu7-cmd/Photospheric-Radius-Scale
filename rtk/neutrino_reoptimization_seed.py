#!/usr/bin/env python3
"""Paired-model local seed reoptimization for the frozen minimal-neutrino robustness protocol.

This worker does not certify a minimum.  It generates a deterministic exact-likelihood
candidate from the independently replayed massless local minimum of the selected model.
The candidate must subsequently pass exact poll + model-appropriate multiscale
stationarity + clean-room replay before B4 can close.
"""
from pathlib import Path
import copy, csv, json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize

os.environ.setdefault('CLIPY_NOJAX','1')
import inference_core as L

MODEL=(sys.argv[1] if len(sys.argv)>1 else '').upper()
if MODEL not in ('RTK','LCDM'):
    raise SystemExit('usage: neutrino_reoptimization_seed.py RTK|LCDM')

STATE=json.loads(Path('../research/state/current.json').read_text())
if not (STATE.get('comparison',{}).get('final_replay_certified') and STATE.get('comparison',{}).get('interior_minimum_certified')):
    raise RuntimeError('massless matched comparison must be A4/A5 certified before B4 robustness search')

OBJ='matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
TOL=float(STATE['objective']['recenter_tolerance_S'])

if MODEL=='RTK':
    START=copy.deepcopy(STATE['final_replay_result']['rtk']['params'])
    AXES=['loglam','h','Ob','Om','As','ns','zre']
else:
    START=copy.deepcopy(STATE['final_replay_result']['lcdm']['params'])
    AXES=['h','Ob','Om','As','ns','zre']

# Broad but finite local-search normalization. These scales are optimizer coordinates,
# not Hessian proof steps. The following physical bounds are frozen before seeing the result.
SCALE={'loglam':0.50,'h':0.010,'Ob':0.0020,'Om':0.020,'As':0.10e-9,'ns':0.020,'zre':1.0}
PHYS={
 'loglam':(math.log(1.0e3),math.log(1.0e8)),
 'h':(0.58,0.80),'Ob':(0.025,0.075),'Om':(0.12,0.42),
 'As':(1.2e-9,3.2e-9),'ns':(0.85,1.10),'zre':(3.0,15.0)
}

ORIG=L.make_ini

def make_ini(model,p,tag):
    path=ORIG(model,p,tag)
    text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:
        raise RuntimeError('expected sparse z_pk baseline not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    if 'N_ur = 3.046' not in text or 'N_ncdm = 0' not in text:
        raise RuntimeError('frozen massless neutrino block not found')
    text=text.replace('N_ur = 3.046','N_ur = 2.0328',1)
    text=text.replace('N_ncdm = 0','N_ncdm = 1\nm_ncdm = 0.06\nT_ncdm = 0.71611\ndeg_ncdm = 1.0',1)
    text+='\n# B4 matched minimal-neutrino robustness ultra overrides\n'
    text+=''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text)
    return path
L.make_ini=make_ini

OUT=Path('../output/neutrino_reoptimization_seed')/MODEL.lower()
OUT.mkdir(parents=True,exist_ok=True)
JOURNAL=OUT/'points.jsonl'; SUMMARY=OUT/'summary.json'; TRACE=OUT/'trace.csv'
ROWS=[]; SUCCESS={}; NREQ=0

# Exact-float point identity at the worker level. inference_core also has exact-float success cache.
def point_key(p):
    return tuple(float(p[k]).hex() for k in ('lam','h','Ob','Om','As','ns','zre'))

def from_y(y):
    p=copy.deepcopy(START)
    for a,v in zip(AXES,y):
        if a=='loglam': p['lam']=math.exp(math.log(float(START['lam']))+SCALE[a]*float(v))
        else: p[a]=float(START[a])+SCALE[a]*float(v)
    if MODEL=='LCDM': p['lam']=0.0
    return p

def y_bounds():
    b=[]
    for a in AXES:
        lo,hi=PHYS[a]
        if a=='loglam':
            z0=math.log(float(START['lam'])); b.append(((lo-z0)/SCALE[a],(hi-z0)/SCALE[a]))
        else: b.append(((lo-float(START[a]))/SCALE[a],(hi-float(START[a]))/SCALE[a]))
    return b
BOUNDS=y_bounds()

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def persist(status='running',extra=None):
    valid=[r for r in SUCCESS.values() if r.get('ok')]
    best=min(valid,key=lambda r:float(r['score'])) if valid else None
    s={
      'classification':'B4_NEUTRINO_REOPTIMIZATION_SEED', 'status':status,
      'model':MODEL,'objective':OBJ,'production_mapping':'eff',
      'massless_state_iteration':STATE.get('iteration'),
      'massless_final_replay_run_id':STATE.get('comparison',{}).get('final_replay_run_id'),
      'start_params':START,'optimizer_axes':AXES,'optimizer_scales':SCALE,
      'physical_bounds':PHYS,'normalized_bounds':BOUNDS,
      'neutrino':{'N_ncdm':1,'m_ncdm_eV':0.06,'T_ncdm':0.71611,'deg_ncdm':1.0,'N_ur':2.0328},
      'exact_requests':NREQ,'unique_success_points':len(SUCCESS),
      'best_score_eff':float(best['score']) if best else None,
      'best_score_k01':float(best['score_k01']) if best else None,
      'best_params':best.get('params') if best else None,
      'best_components':({k:best.get(k) for k in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')} if best else None),
      'warning':'Seed optimization only; not a certified minimum, not B4 closure, not replacement of frozen massless objective.'
    }
    if extra:s.update(extra)
    SUMMARY.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
    if ROWS:
        fields=[]
        for r in ROWS:
            for k in r:
                if k not in fields:fields.append(k)
        with TRACE.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
    return s

def exact_eval(p,label):
    global NREQ
    k=point_key(p)
    if k in SUCCESS:return SUCCESS[k]
    last=None
    for attempt in range(1,4):
        NREQ+=1
        try:r=L.evaluate(MODEL,p)
        except Exception as e:r={'ok':False,'error':repr(e)}
        if r.get('ok'):
            rr=dict(r);rr['params']=copy.deepcopy(p);rr['label']=label;rr['attempt']=attempt
            SUCCESS[k]=rr
            row={'label':label,'attempt':attempt,'score':float(rr['score']),'score_k01':float(rr['score_k01']),
                 **{a:(math.log(float(p['lam'])) if a=='loglam' else float(p[a])) for a in AXES}}
            for q in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=rr.get(q)
            ROWS.append(row)
            with JOURNAL.open('a') as f:f.write(json.dumps(rr,sort_keys=True)+'\n')
            cleanup(rr.get('tag'));persist();
            print('B4_NEUTRINO_POINT',MODEL,json.dumps(row,sort_keys=True),flush=True)
            return rr
        last=r
        time.sleep(2*attempt)
    fail={'ok':False,'model':MODEL,'params':copy.deepcopy(p),'label':label,'error':last}
    with JOURNAL.open('a') as f:f.write(json.dumps(fail,sort_keys=True)+'\n')
    persist('evaluation_failure')
    return fail

CALL=0
def fun(y):
    global CALL
    CALL+=1
    p=from_y(y);r=exact_eval(p,f'powell_{CALL:04d}')
    return float(r['score']) if r.get('ok') else 1e30

# Exact neutrino score at frozen massless start.
r0=exact_eval(START,'massless_minimum_as_neutrino_start')
if not r0.get('ok'):raise SystemExit('initial neutrino evaluation failed')
S0=float(r0['score'])

res=minimize(fun,np.zeros(len(AXES)),method='Powell',bounds=BOUNDS,
             options={'maxfev':180,'xtol':0.015,'ftol':2e-5,'disp':True})
# Re-evaluate the optimizer-returned point through the exact cache/retry path.
r_opt=exact_eval(from_y(res.x),'powell_return')
valid=[r for r in SUCCESS.values() if r.get('ok')]
best=min(valid,key=lambda r:float(r['score']))

# One exact normalized coordinate poll at a preregistered diagnostic scale. This is a
# candidate-quality check, not the later stationarity proof. Any >0.005 downhill point
# is explicitly reported and becomes the next reoptimization center.
POLL={'loglam':0.10,'h':0.0010,'Ob':0.00020,'Om':0.0020,'As':0.010e-9,'ns':0.0020,'zre':0.10}
c=copy.deepcopy(best['params']);center_score=float(best['score']);poll_rows=[]
for a in AXES:
    for sg in (-1,1):
        p=copy.deepcopy(c)
        if a=='loglam':p['lam']=float(c['lam'])*math.exp(sg*POLL[a])
        else:p[a]=float(c[a])+sg*POLL[a]
        rr=exact_eval(p,f'poll_{a}_{sg:+d}')
        if rr.get('ok'):poll_rows.append({'axis':a,'sign':sg,'score':float(rr['score']),'params':rr['params']})
valid=[r for r in SUCCESS.values() if r.get('ok')]
best2=min(valid,key=lambda r:float(r['score']))
best_improvement=center_score-float(best2['score'])
summary=persist('complete',{
 'initial_neutrino_score_eff':S0,
 'seed_improvement_from_massless_start':S0-float(best2['score']),
 'powell_result':{'success':bool(res.success),'message':str(res.message),'nfev':int(res.nfev),'x':res.x.tolist(),'fun':float(res.fun)},
 'diagnostic_poll_steps':POLL,'diagnostic_poll_best_improvement_from_pre_poll_best':best_improvement,
 'recenter_required_by_0p005':bool(best_improvement>TOL),
 'next_required_gate':'recenter_and_repeat_seed' if best_improvement>TOL else 'dedicated_neutrino_stationarity_multiscale',
 'best_score_eff':float(best2['score']),'best_score_k01':float(best2['score_k01']),
 'best_params':best2['params'],
 'best_components':{k:best2.get(k) for k in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')}
})
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('B4_NEUTRINO_REOPTIMIZATION_SEED_COMPLETE',MODEL,json.dumps(summary,sort_keys=True),flush=True)
