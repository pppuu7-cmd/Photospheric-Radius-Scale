#!/usr/bin/env python3
"""Exact B9 LCDM recenter-v7 base negative-eigenmode rays.

Consumes the target frozen after the v7 scale-1 Hessian and before any ray
score. The v7 center is exact-recenter-clear but has one soft negative Hessian
mode. This worker evaluates that full frozen eigenvector with no clipping using
the same dense/ultra baseline plus standalone Planck R3 lensing objective as the
v7 Hessian worker.
"""
from __future__ import annotations
from pathlib import Path
import copy, hashlib, json, math, os, subprocess, sys, time
import numpy as np

os.environ.setdefault('CLIPY_NOJAX','1')
sys.argv=['b9_lcdm_recenter_v7_base_eigenmode_rays','planck_data']
import clipy
import inference_core as C

ROOT=Path('..')
T=json.loads((ROOT/'research/robustness/B9_LCDM_RECENTER_V7_BASE_EIGENMODE_RAYS_TARGET_v1.json').read_text())
B9=json.loads((ROOT/'research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json').read_text())
STATE=json.loads((ROOT/'research/state/current.json').read_text())
FIXED=json.loads((ROOT/'research/robustness/B9_FIXED_CENTER_LENSING_RESULT_v1.json').read_text())

assert T['classification']=='B9_LCDM_RECENTER_V7_BASE_EIGENMODE_RAYS_TARGET_V1_FROZEN'
assert T['objective']==B9['objective']=='matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1'
assert T['production_mapping']=='eff'
assert T['parent_base_run_id']==32601673857
assert T['parent_base_artifact_id']==9483908098
assert T['parent_stencil_scale']==1.0
assert T['parent_positive_definite_eff'] is False
assert T['best_improvement_eff']<=T['recenter_tolerance_S']==0.005
assert T['decision_rule']['no_clipping'] is True
assert len(T['eigenmodes'])==1 and T['eigenmodes'][0]['eigenvalue_y']<0
assert FIXED['classification']=='B9_FIXED_CENTER_LENSING_ADAPTER_CONTRACT_PASS'

CENTER=copy.deepcopy(T['center'])
AXES=list(T['axes'])
STEPS={k:float(v) for k,v in T['steps'].items()}
AMPS=[float(x) for x in T['ray_amplitudes']]
TOL=float(T['recenter_tolerance_S'])
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
OUT=ROOT/'output/b9_lcdm_recenter_v7_base_eigenmode_rays'
OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl'; FAIL=OUT/'failures.jsonl'; SUMMARY=OUT/'summary.json'


def canonical_hash(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None

def append(path,row):
    with path.open('a') as f:
        f.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n'); f.flush()

def cleanup(tag):
    if not tag:return
    for q in C.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

# Exact production dense/ultra objective.
ORIG=C.make_ini
def make_ini(model,p,tag):
    path=ORIG(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE in text:
        text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    elif 'z_pk = '+DENSE not in text:
        raise RuntimeError('could not establish dense B9 z_pk objective')
    text+='\n# B9 LCDM v7 eigenmode rays: frozen production precision\n'+''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text); return path
C.make_ini=make_ini

# Same standalone Planck R3 lensing contract as the B9 stationarity worker.
PLANCK=Path('planck_data')
LENS_PATH=PLANCK/B9['lensing_product']
if not LENS_PATH.is_dir(): raise RuntimeError(f'missing frozen B9 lensing product: {LENS_PATH}')
LENS=clipy.clik(str(LENS_PATH))
LMAX=[int(x) for x in LENS.get_lmax()]
if LMAX!=B9['lensing_lmax']: raise RuntimeError(f'B9 lmax contract drift: {LMAX}')
DEFAULT=np.asarray(LENS.default_par,dtype=float)
SPEC_NAMES=['phiphi','TT','EE','BB','TE','TB','EB']
CL_LEN=sum(x+1 for x in LMAX if x>=0)
EXTRA_NAMES=[str(x) for x in LENS.get_extra_parameter_names()]
if len(DEFAULT)!=10005 or CL_LEN!=10004 or CL_LEN+len(EXTRA_NAMES)!=len(DEFAULT):
    raise RuntimeError((len(DEFAULT),CL_LEN,EXTRA_NAMES))

def scalar(x):
    a=np.asarray(x,dtype=float).reshape(-1)
    if a.size<1 or not np.isfinite(a[0]): raise RuntimeError(f'nonfinite lensing likelihood: {a}')
    return float(a[0])
if not math.isfinite(scalar(LENS(DEFAULT.copy()))): raise RuntimeError('B9 lensing default selfcheck failed')

UK2=(2.7255e6)**2
def class_lensed_cls(path):
    path=Path(path)
    if not path.is_file(): raise RuntimeError(f'missing CLASS lensed spectrum: {path}')
    lines=path.read_text().splitlines(); header='\n'.join(lines[:12])
    for token in ('TT','EE','TE','BB','phiphi'):
        if token not in header: raise RuntimeError(f'{token} missing from CLASS lensed header')
    vals={}
    for line in lines:
        s=line.strip()
        if not s or s.startswith('#'): continue
        a=s.split(); ell=int(float(a[0]))
        if len(a)<6: raise RuntimeError(f'too few CLASS lensed columns at ell {ell}')
        fac=ell*(ell+1)/(2*math.pi)
        if fac<=0: continue
        dtt,dee,dte,dbb,dpp=map(float,a[1:6])
        vals[ell]={'phiphi':dpp/fac,'TT':dtt/fac*UK2,'EE':dee/fac*UK2,'BB':dbb/fac*UK2,'TE':dte/fac*UK2,'TB':0.0,'EB':0.0}
    required=max(x for x in LMAX if x>=0)
    if not vals or max(vals)<required: raise RuntimeError(f'CLASS lensed spectrum insufficient: {max(vals) if vals else None}')
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
    if not np.array_equal(v[CL_LEN:],DEFAULT[CL_LEN:]): raise RuntimeError('B9 nuisance/default tail changed')
    return v


def params_for(vec,alpha):
    p=copy.deepcopy(CENTER)
    for axis,v in zip(AXES,vec):
        p[axis]=float(CENTER[axis])+float(alpha)*float(v)*STEPS[axis]
    p['lam']=0.0
    checks={'h':(0.2,1.2),'Ob':(1e-6,0.5),'Om':(1e-6,0.9),'As':(1e-12,1e-8),'ns':(0.5,1.5),'zre':(0.0,40.0)}
    for k,(lo,hi) in checks.items():
        x=float(p[k])
        if not (math.isfinite(x) and lo<x<hi): raise RuntimeError(f'frozen ray point OOB {k}={x}')
    return p

CACHE={}
def key(p): return tuple(float(p[k]).hex() for k in ('h','Ob','Om','As','ns','zre'))
def evaluate(p,label,mode,alpha):
    k=key(p)
    if k in CACHE:return CACHE[k]
    last=None
    for attempt in range(1,4):
        C.CACHE.clear()
        try:r=C.evaluate('LCDM',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            tag=r.get('tag')
            try:
                cls=class_lensed_cls(C.OUT/f'{tag}_cl_lensed.dat')
                logl=scalar(LENS(lens_vector(cls)))
                row={'label':label,'mode_index':mode,'alpha':alpha,'attempt':attempt,'params':p,
                     'S_base_eff':float(r['score']),'S_base_k01':float(r['score_k01']),
                     'lensing_loglike':logl,'lensing_minus2loglike':-2.0*logl,
                     'S_B9_eff':float(r['score'])-2.0*logl,'S_B9_k01':float(r['score_k01'])-2.0*logl,
                     'logL_planck':r.get('logL_planck'),'chi2_SN':r.get('chi2_SN'),
                     'chi2_BOSS_eff':r.get('chi2_BOSS_eff'),'chi2_BOSS_k01':r.get('chi2_BOSS_k01'),'rd':r.get('rd')}
                if not all(math.isfinite(float(row[x])) for x in ('S_B9_eff','S_B9_k01','lensing_loglike')):
                    raise RuntimeError('nonfinite B9 ray score')
                CACHE[k]=row; append(POINTS,row); cleanup(tag)
                print('B9_LCDM_RECENTER_V7_BASE_EIGENMODE_RAY_POINT',json.dumps(row,sort_keys=True,allow_nan=False),flush=True)
                return row
            except Exception:
                cleanup(tag); raise
        last=r; append(FAIL,{'label':label,'mode_index':mode,'alpha':alpha,'attempt':attempt,'params':p,'result':r}); cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3: time.sleep(2*attempt)
    raise RuntimeError(f'{label}: failed after 3 exact retries: {last}')

center=evaluate(CENTER,'center',-1,0.0)
S0=float(center['S_B9_eff'])
if abs(S0-float(T['S_center_eff']))>float(T['fresh_tree_replay_abs_tolerance']):
    raise RuntimeError(f'center replay mismatch: {S0} vs {T["S_center_eff"]}')

mode_results=[]
for m in T['eigenmodes']:
    idx=int(m['mode_index']); vec=[float(x) for x in m['eigenvector_y']]
    if abs(sum(x*x for x in vec)-1.0)>1e-10: raise RuntimeError('frozen eigenvector is not unit normalized')
    rows=[]
    for alpha in AMPS:
        rows.append(evaluate(params_for(vec,alpha),f'mode{idx}_alpha_{alpha:+g}',idx,alpha))
    best=min(rows,key=lambda r:r['S_B9_eff'])
    mode_results.append({'mode_index':idx,'selection_reason':m['reason'],'parent_eigenvalue_y':float(m['eigenvalue_y']),
                         'eigenvector_y':vec,'best_alpha':float(best['alpha']),'best_exact_S_eff':float(best['S_B9_eff']),
                         'best_improvement_eff':S0-float(best['S_B9_eff']),'best_params':best['params'],
                         'scores':[{'alpha':float(r['alpha']),'S_eff':float(r['S_B9_eff']),'S_k01':float(r['S_B9_k01'])} for r in rows]})
maximp=max(x['best_improvement_eff'] for x in mode_results)
classification='B9_LCDM_RECENTER_V7_BASE_EIGENMODE_RECENTER_V8_REQUIRED' if maximp>TOL else 'B9_LCDM_RECENTER_V7_BASE_EIGENMODE_RAYS_NO_DESCENT_GT_0P005'
best_mode=max(mode_results,key=lambda x:x['best_improvement_eff'])
summary={'classification':classification,'objective':T['objective'],'production_mapping':'eff',
         'parent_base_run_id':T['parent_base_run_id'],'parent_base_artifact_id':T['parent_base_artifact_id'],
         'parent_base_artifact_digest':T['parent_base_artifact_digest'],'parent_stencil_scale':T['parent_stencil_scale'],
         'target_sha256':canonical_hash(T),'center':CENTER,'S_center_eff':S0,'recenter_tolerance_S':TOL,
         'ray_amplitudes':AMPS,'mode_results':mode_results,'max_exact_improvement_eff':maximp,'best_mode':best_mode,
         'provenance':{'research_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon'),'target_file':str(ROOT/'research/robustness/B9_LCDM_RECENTER_V7_BASE_EIGENMODE_RAYS_TARGET_v1.json')},
         'next_gate':('freeze best exact ray point as B9 LCDM recenter-v8 target' if maximp>TOL else 'run independent half-scale Hessian resolution audit at unchanged v7 center; v7 base Hessian remains non-PD'),
         'warning':'Local B9 LCDM Planck-R3-lensing stationarity robustness only; not global evidence, posterior preference, AIC/BIC or Bayes factor.'}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n')
print('B9_LCDM_RECENTER_V7_BASE_EIGENMODE_RAYS_COMPLETE',json.dumps(summary,sort_keys=True,allow_nan=False),flush=True)
