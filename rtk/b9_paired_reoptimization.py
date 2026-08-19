#!/usr/bin/env python3
"""B9-v1 paired local reoptimization with standalone Planck R3 lensing.

Usage:
  python3 b9_paired_reoptimization.py LCDM|RTK

The geometry and optimizer semantics are preregistered in
research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json and deliberately
reuse the validated Stage4D3 wide COBYQA + exact recentered-poll machinery.
The result is a local candidate only; stationarity, multiscale certification
and independent fresh-tree replay are separate mandatory gates.
"""
from __future__ import annotations
from pathlib import Path
import csv, json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize

os.environ.setdefault('CLIPY_NOJAX','1')
if len(sys.argv) != 2 or sys.argv[1].upper() not in ('LCDM','RTK'):
    raise SystemExit(__doc__)
MODEL=sys.argv[1].upper()
# inference_core expects argv[1] to identify the Planck tree at import time.
sys.argv=['b9_paired_reoptimization','planck_data']
import clipy
import inference_core as C

ROOT=Path('..')
TARGET=json.loads((ROOT/'research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json').read_text())
STATE=json.loads((ROOT/'research/state/current.json').read_text())
FIXED=json.loads((ROOT/'research/robustness/B9_FIXED_CENTER_LENSING_RESULT_v1.json').read_text())
if TARGET['status']!='PREREGISTERED_TARGET_BEFORE_FIRST_B9_REOPTIMIZATION_RESULT':
    raise RuntimeError('B9 paired target status changed')
if TARGET['baseline_objective']!=STATE['objective']['name']:
    raise RuntimeError('B9 baseline objective drift')
if TARGET['baseline_objective_fingerprint']!='754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666':
    raise RuntimeError('unexpected preregistered baseline fingerprint')
if FIXED['classification']!='B9_FIXED_CENTER_LENSING_ADAPTER_CONTRACT_PASS':
    raise RuntimeError('B9 fixed-center contract has not passed')

START={k:float(v) for k,v in TARGET['starts'][MODEL].items()}
GEOM=TARGET['reoptimization_geometry']
HW={k:float(v) for k,v in GEOM['shared_halfwidths'].items()}
if MODEL=='RTK':
    LOG_LAM_HW=float(GEOM['rtk_loglambda_halfwidth'])
    COORDS=[('loglam',math.log(START['lam']),LOG_LAM_HW)] + [
        (n,START[n],HW[n]) for n in ('h','Ob','Om','As','ns','zre')]
else:
    COORDS=[(n,START[n],HW[n]) for n in ('h','Ob','Om','As','ns','zre')]
N=len(COORDS)

# Exact same frozen B9 lensing product and adapter contract as Step 1.
PLANCK=Path('planck_data')
LENS_PATH=PLANCK/TARGET['lensing_product']
if not LENS_PATH.is_dir():
    raise RuntimeError(f'missing frozen B9 lensing product: {LENS_PATH}')
LENS=clipy.clik(str(LENS_PATH))
LMAX=[int(x) for x in LENS.get_lmax()]
if LMAX!=TARGET['lensing_lmax']:
    raise RuntimeError(f'B9 lmax contract drift: {LMAX}')
DEFAULT=np.asarray(LENS.default_par,dtype=float)
SPEC_NAMES=['phiphi','TT','EE','BB','TE','TB','EB']
CL_LEN=sum(x+1 for x in LMAX if x>=0)
EXTRA_NAMES=[str(x) for x in LENS.get_extra_parameter_names()]
if len(DEFAULT)!=10005 or CL_LEN!=10004 or CL_LEN+len(EXTRA_NAMES)!=len(DEFAULT):
    raise RuntimeError((len(DEFAULT),CL_LEN,EXTRA_NAMES))

def scalar(x):
    a=np.asarray(x,dtype=float).reshape(-1)
    if a.size<1 or not np.isfinite(a[0]):
        raise RuntimeError(f'nonfinite lensing likelihood result: {a}')
    return float(a[0])
if not math.isfinite(scalar(LENS(DEFAULT.copy()))):
    raise RuntimeError('B9 default-vector selfcheck failed')

# Preserve the frozen dense-z and ultra precision objective exactly as in the
# already-passed B9 fixed-center adapter.
ORIG_MAKE_INI=C.make_ini
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
def make_ini(model,p,tag):
    path=ORIG_MAKE_INI(model,p,tag)
    text=Path(path).read_text()
    if 'z_pk = '+SPARSE in text:
        text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    elif 'z_pk = '+DENSE not in text:
        raise RuntimeError('could not establish dense B9 z_pk objective')
    text+='\n# B9 paired reoptimization: frozen production precision\n'
    text+=''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text)
    return path
C.make_ini=make_ini

UK2=(2.7255e6)**2
def class_lensed_cls(path):
    path=Path(path)
    if not path.is_file():
        raise RuntimeError(f'missing CLASS lensed spectrum: {path}')
    lines=path.read_text().splitlines()
    header='\n'.join(lines[:12])
    for token in ('TT','EE','TE','BB','phiphi'):
        if token not in header:
            raise RuntimeError(f'{token} missing from CLASS lensed header')
    vals={}
    for line in lines:
        s=line.strip()
        if not s or s.startswith('#'): continue
        a=s.split(); ell=int(float(a[0]))
        if len(a)<6: raise RuntimeError(f'too few CLASS lensed columns at ell {ell}')
        fac=ell*(ell+1)/(2*math.pi)
        if fac<=0: continue
        dtt,dee,dte,dbb,dpp=map(float,a[1:6])
        vals[ell]={
            'phiphi':dpp/fac,
            'TT':dtt/fac*UK2,
            'EE':dee/fac*UK2,
            'BB':dbb/fac*UK2,
            'TE':dte/fac*UK2,
            'TB':0.0,
            'EB':0.0,
        }
    required=max(x for x in LMAX if x>=0)
    if not vals or max(vals)<required:
        raise RuntimeError(f'CLASS lensed spectrum insufficient: max ell={max(vals) if vals else None}')
    return vals

def lens_vector(cls):
    v=DEFAULT.copy(); off=0
    for spec,lm in enumerate(LMAX):
        if lm<0: continue
        arr=np.zeros(lm+1,dtype=float); name=SPEC_NAMES[spec]
        for ell in range(2,lm+1): arr[ell]=cls[ell][name]
        if not np.all(np.isfinite(arr)): raise RuntimeError(f'nonfinite {name}')
        v[off:off+lm+1]=arr; off+=lm+1
    if off!=CL_LEN: raise RuntimeError((off,CL_LEN))
    if not np.array_equal(v[CL_LEN:],DEFAULT[CL_LEN:]):
        raise RuntimeError('B9 nuisance/default tail changed')
    return v

OUT=ROOT/'output'/'b9_paired_reoptimization'/MODEL.lower()
OUT.mkdir(parents=True,exist_ok=True)
TRACE=OUT/'trace.csv'; FAILURES=OUT/'failures.jsonl'
EVALS={}; ROWS=[]; RETRIES=0

def cleanup(tag):
    if not tag:return
    for p in C.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def y_to_params(y):
    y=np.asarray(y,dtype=float)
    p=dict(START)
    offset=0
    if MODEL=='RTK':
        p['lam']=START['lam']*math.exp(float(y[0])*LOG_LAM_HW)
        offset=1
    else:
        p['lam']=0.0
    for yi,n in zip(y[offset:],('h','Ob','Om','As','ns','zre')):
        p[n]=START[n]+float(yi)*HW[n]
    return p

def key(y): return tuple(float(v) for v in np.asarray(y,dtype=float))
def append_failure(row):
    with FAILURES.open('a') as f:
        f.write(json.dumps(row,sort_keys=True,default=str)+'\n'); f.flush()

def is_timeout(r):
    text=str(r.get('error',r.get('reason','')))
    return 'CLASS_TIMEOUT' in text

def evaluate_y(y,label='opt'):
    global RETRIES
    y=np.asarray(y,dtype=float)
    if np.any(~np.isfinite(y)) or np.any(y < -1.0000001) or np.any(y > 1.0000001):
        raise RuntimeError(f'{label}: normalized point outside preregistered box: {y.tolist()}')
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    r=None
    for attempt in (1,2):
        # Force a real exact CLASS output for every new physical point. Local
        # memoization is exact-float only and stores successful scored points.
        C.CACHE.clear()
        try:r=C.evaluate(MODEL,p)
        except Exception as exc:r={'ok':False,'reason':repr(exc)}
        if r.get('ok'): break
        fail={'label':label,'attempt':attempt,'y':y.tolist(),'params':p,'result':r}
        append_failure(fail)
        cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt==1 and is_timeout(r):
            RETRIES+=1; time.sleep(2); continue
        raise RuntimeError(f'{label}: exact baseline evaluation failed closed: {r}')
    tag=r.get('tag')
    try:
        cls=class_lensed_cls(C.OUT/f'{tag}_cl_lensed.dat')
        logl=scalar(LENS(lens_vector(cls)))
        base=float(r['score'])
        total=base-2.0*logl
        if not all(math.isfinite(x) for x in (base,logl,total)):
            raise RuntimeError((base,logl,total))
    except Exception:
        cleanup(tag)
        raise
    rr={
        'ok':True,'label':label,'model':MODEL,'y':y.tolist(),'params':p,
        'S_base_eff':base,'lensing_loglike':logl,'lensing_minus2loglike':-2.0*logl,
        'S_B9':total,'score_k01':float(r['score_k01']),
        'logL_planck':r.get('logL_planck'),'chi2_SN':r.get('chi2_SN'),
        'chi2_BOSS_eff':r.get('chi2_BOSS_eff'),'chi2_BOSS_k01':r.get('chi2_BOSS_k01'),
        'rd':r.get('rd')
    }
    EVALS[k]=rr
    row=dict(rr); row.pop('ok',None); row['params_json']=json.dumps(p,sort_keys=True); row.pop('params',None)
    ROWS.append(row)
    cleanup(tag)
    print('B9_REOPT_EVAL',MODEL,len(EVALS),label,total,base,-2.0*logl,p,flush=True)
    return rr

def objective(y): return float(evaluate_y(y,'cobyqa')['S_B9'])

z=np.zeros(N)
r0=evaluate_y(z,'center')
fixed_expected=float(FIXED['models'][MODEL]['fixed_center_S_B9'])
center_err=abs(r0['S_B9']-fixed_expected)
if center_err>2e-6:
    raise RuntimeError(f'B9 fixed-center regression drift for {MODEL}: {center_err}')

bounds=[(-1.0,1.0)]*N
res=minimize(objective,z,method='COBYQA',bounds=bounds,
             options={'maxfev':int(GEOM['maxfev']),'maxiter':int(GEOM['maxiter']),
                      'initial_tr_radius':float(GEOM['initial_tr_radius']),
                      'final_tr_radius':float(GEOM['final_tr_radius']),'disp':True})
rx=np.asarray(res.x,dtype=float)
if np.any(rx < -1.0000001) or np.any(rx > 1.0000001):
    raise RuntimeError(f'COBYQA returned outside box: {rx.tolist()}')
evaluate_y(rx,'cobyqa_result')

# Exact recentered polls, identical sequence to the validated Stage4D3 wide
# search. Out-of-box proposals are skipped rather than clipped.
for poll in [float(x) for x in GEOM['exact_poll_sequence']]:
    seed=np.asarray(min(EVALS.values(),key=lambda q:q['S_B9'])['y'],dtype=float)
    for i in range(N):
        for sg in (-1.0,1.0):
            y=seed.copy(); y[i]+=sg*poll
            if np.any(y < -1.0) or np.any(y > 1.0):
                print('B9_REOPT_POLL_SKIP_BOUNDARY',MODEL,poll,i,sg,y.tolist(),flush=True)
                continue
            evaluate_y(y,f'poll_{poll}_{i}_{int(sg):+d}')

best=min(EVALS.values(),key=lambda q:q['S_B9'])
best_y=np.asarray(best['y'],dtype=float)
boundary_axes=[COORDS[i][0] for i,v in enumerate(best_y) if abs(v)>0.97]
status='INTERIOR_LOCAL_REOPTIMIZATION_CANDIDATE' if not boundary_axes else 'REOPTIMIZATION_BOUNDARY_HIT'
summary={
    'classification':'B9_PAIRED_REOPTIMIZATION_CANDIDATE',
    'status':status,
    'objective':TARGET['objective'],'score_definition':TARGET['score_definition'],
    'model':MODEL,'start':START,'coordinates':[{'name':n,'center_coordinate':c,'halfwidth':w,'normalized_bounds':[-1,1]} for n,c,w in COORDS],
    'fixed_center_expected_S_B9':fixed_expected,'fixed_center_replayed_S_B9':r0['S_B9'],
    'fixed_center_replay_abs_error':center_err,
    'best_S_B9':best['S_B9'],'best_S_base_eff':best['S_base_eff'],
    'best_lensing_loglike':best['lensing_loglike'],'best_lensing_minus2loglike':best['lensing_minus2loglike'],
    'improvement_from_A5_fixed_center':r0['S_B9']-best['S_B9'],
    'best_params':best['params'],'best_y':best['y'],'boundary_axes':boundary_axes,
    'optimizer':{'method':'COBYQA','success':bool(res.success),'message':str(res.message),'fun':float(res.fun),'x':rx.tolist(),'nfev':int(res.nfev),'nit':int(res.nit)},
    'exact_scored_points':len(EVALS),'class_timeout_retries':RETRIES,
    'exact_poll_sequence':GEOM['exact_poll_sequence'],
    'next_gate':'Recenter at this exact best point and run preregistered base plus independent half-scale stationarity/Hessian certification; then fresh-tree replay.',
    'warning':'Local B9-v1 reoptimization candidate only; not a global optimum, significance, AIC/BIC, posterior preference or Bayes factor.'
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n')
fields=[]
for row in ROWS:
    for k in row:
        if k not in fields:fields.append(k)
with TRACE.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('B9_PAIRED_REOPTIMIZATION_RESULT',json.dumps(summary,sort_keys=True,allow_nan=False),flush=True)
print('B9_PAIRED_REOPTIMIZATION_COMPLETE',MODEL,flush=True)
