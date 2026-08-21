#!/usr/bin/env python3
"""Exact B9-v1 RTK stationarity Hessian at the frozen reoptimization recenter.

The center is frozen in research/robustness/B9_RTK_RECENTER_TARGET_v1.json,
which was committed after the RTK reoptimization artifact and before the final
LCDM artifact was inspected.  This worker evaluates the exact production dense
objective plus the same standalone Planck R3 lensing product used by the B9
reoptimization.  It does not mutate the A1-A5 baseline.

Environment:
    RTK_B9_STENCIL_SCALE = 1.0 or 0.5 (also accepts 0.25,0.125 for explicit
                           future diagnostics, never silently selected)
"""
from __future__ import annotations
from pathlib import Path
import copy, csv, hashlib, json, math, os, subprocess, sys, time
import numpy as np

os.environ.setdefault('CLIPY_NOJAX','1')
sys.argv=['b9_rtk_stationarity_hessian','planck_data']
import clipy
import inference_core as C

MODEL='RTK'
SCALE=float(os.environ.get('RTK_B9_STENCIL_SCALE','1.0'))
if SCALE not in (1.0,0.5,0.25,0.125):
    raise RuntimeError(f'unsupported B9 stencil scale {SCALE!r}')

ROOT=Path('..')
TARGET=json.loads((ROOT/'research/robustness/B9_RTK_RECENTER_TARGET_v1.json').read_text())
B9=json.loads((ROOT/'research/robustness/B9_PAIRED_REOPTIMIZATION_TARGET_v1.json').read_text())
STATE=json.loads((ROOT/'research/state/current.json').read_text())
FIXED=json.loads((ROOT/'research/robustness/B9_FIXED_CENTER_LENSING_RESULT_v1.json').read_text())

assert TARGET['status']=='FROZEN_AFTER_RTK_REOPTIMIZATION_BEFORE_LCDM_RESULT_AND_BEFORE_RTK_STATIONARITY'
assert TARGET['objective']==B9['objective']=='matched-ultra-linstep2+dense-BOSS+PlanckR3-lensing-v1'
assert B9['baseline_objective']==STATE['objective']['name']
assert B9['baseline_objective_fingerprint']=='754edb2ff5380eff314867b0ecb1a23a8b861a69f7e46070c4b8251c98573666'
assert FIXED['classification']=='B9_FIXED_CENTER_LENSING_ADAPTER_CONTRACT_PASS'

CENTER=copy.deepcopy(TARGET['center'])
AXES=['loglam','h','Ob','Om','As','ns','zre']
STEPS={k:float(v)*SCALE for k,v in TARGET['base_steps'].items()}
N=len(AXES)
TOL=float(TARGET['recenter_tolerance_S'])
PD_THRESH=float(TARGET['positive_definite_threshold'])

OUT=ROOT/'output'/'b9_rtk_stationarity'/f'scale_{SCALE:g}'
OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl'; FAILURES=OUT/'failures.jsonl'; SUMMARY=OUT/'summary.json'; PROVFILE=OUT/'provenance.json'


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def git_head(path):
    try:
        return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None

TARGET_FP=canonical_hash(TARGET)
CENTER_FP=canonical_hash({'model':MODEL,'center':CENTER,'objective':TARGET['objective'],'mapping':'eff'})
PROV={
    'model':MODEL,'stencil_scale':SCALE,'target_fingerprint':TARGET_FP,'center_fingerprint':CENTER_FP,
    'parent_run_id':TARGET['parent_run_id'],'parent_artifact_id':TARGET['parent_artifact_id'],
    'parent_artifact_digest':TARGET['parent_artifact_digest'],
    'rtk_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon'),
    'numpy_version':np.__version__
}
PROVFILE.write_text(json.dumps(PROV,indent=2,sort_keys=True)+'\n')

# Exact production dense/ultra objective.
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
    text+='\n# B9 RTK stationarity: frozen production precision\n'
    text+=''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text)
    return path
C.make_ini=make_ini

# Same standalone Planck R3 lensing contract as B9 reoptimization.
PLANCK=Path('planck_data')
LENS_PATH=PLANCK/B9['lensing_product']
if not LENS_PATH.is_dir():
    raise RuntimeError(f'missing frozen B9 lensing product: {LENS_PATH}')
LENS=clipy.clik(str(LENS_PATH))
LMAX=[int(x) for x in LENS.get_lmax()]
if LMAX!=B9['lensing_lmax']:
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

UK2=(2.7255e6)**2
def class_lensed_cls(path):
    path=Path(path)
    if not path.is_file():
        raise RuntimeError(f'missing CLASS lensed spectrum: {path}')
    lines=path.read_text().splitlines(); header='\n'.join(lines[:12])
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
            'phiphi':dpp/fac,'TT':dtt/fac*UK2,'EE':dee/fac*UK2,
            'BB':dbb/fac*UK2,'TE':dte/fac*UK2,'TB':0.0,'EB':0.0
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

E={}
def key(y): return tuple(float(x).hex() for x in np.asarray(y,float))
def pars(y):
    y=np.asarray(y,float); p=copy.deepcopy(CENTER)
    for yi,a in zip(y,AXES):
        if a=='loglam': p['lam']=float(CENTER['lam'])*math.exp(float(yi)*STEPS[a])
        else: p[a]=float(CENTER[a])+float(yi)*STEPS[a]
    return p

def cleanup(tag):
    if not tag:return
    for q in C.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def append(path,row):
    with path.open('a') as f:
        f.write(json.dumps(row,sort_keys=True,default=str)+'\n'); f.flush()

def is_timeout(r):
    return 'CLASS_TIMEOUT' in str(r.get('error',r.get('reason',''))) if isinstance(r,dict) else False

def ev(y,label):
    y=np.asarray(y,float); k=key(y)
    if k in E:return E[k]
    p=pars(y); last=None
    for attempt in range(1,4):
        C.CACHE.clear()
        try:r=C.evaluate(MODEL,p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            tag=r.get('tag')
            try:
                cls=class_lensed_cls(C.OUT/f'{tag}_cl_lensed.dat')
                logl=scalar(LENS(lens_vector(cls)))
                base_eff=float(r['score']); base_k01=float(r['score_k01'])
                row={
                    'label':label,'attempt':attempt,'y':y.tolist(),'params':p,
                    'S_base_eff':base_eff,'S_base_k01':base_k01,
                    'lensing_loglike':logl,'lensing_minus2loglike':-2.0*logl,
                    'S_B9_eff':base_eff-2.0*logl,'S_B9_k01':base_k01-2.0*logl,
                    'logL_planck':r.get('logL_planck'),'chi2_SN':r.get('chi2_SN'),
                    'chi2_BOSS_eff':r.get('chi2_BOSS_eff'),'chi2_BOSS_k01':r.get('chi2_BOSS_k01'),'rd':r.get('rd')
                }
                if not all(math.isfinite(float(row[x])) for x in ('S_B9_eff','S_B9_k01','lensing_loglike')):
                    raise RuntimeError('nonfinite B9 score')
                E[k]=row; append(POINTS,row); cleanup(tag)
                print('B9_RTK_HESSIAN_POINT',SCALE,json.dumps(row,sort_keys=True),flush=True)
                return row
            except Exception:
                cleanup(tag); raise
        last=r; append(FAILURES,{'label':label,'attempt':attempt,'y':y.tolist(),'params':p,'result':r})
        cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3 and is_timeout(r): time.sleep(2*attempt); continue
        if attempt<3: time.sleep(2*attempt); continue
    raise RuntimeError(f'RTK {label}: failed after 3 identical exact retries: {last}')

z=np.zeros(N); ev(z,'center')
# The target center must replay the parent exact B9 score before any Hessian claim.
center_err=abs(float(E[key(z)]['S_B9_eff'])-float(TARGET['best_exact_S_B9']))
if center_err>float(TARGET['fresh_tree_replay_abs_tolerance']):
    raise RuntimeError(f'B9 RTK recenter replay drift: {center_err}')

for i in range(N):
    for s in (-1.,1.):
        y=np.zeros(N); y[i]=s; ev(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for a in (-1.,1.):
            for b in (-1.,1.):
                y=np.zeros(N); y[i]=a; y[j]=b
                ev(y,f'cross_{i}_{j}_{int(a):+d}_{int(b):+d}')


def build(which):
    fld='S_B9_eff' if which=='eff' else 'S_B9_k01'
    S0=float(E[key(np.zeros(N))][fld]); g=np.zeros(N); H=np.zeros((N,N))
    for i in range(N):
        yp=np.zeros(N); ym=np.zeros(N); yp[i]=1; ym[i]=-1
        sp=float(E[key(yp)][fld]); sm=float(E[key(ym)][fld])
        g[i]=(sp-sm)/2.; H[i,i]=sp-2.*S0+sm
    for i in range(N):
        for j in range(i+1,N):
            vals=[]
            for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
                y=np.zeros(N); y[i]=a; y[j]=b; vals.append(float(E[key(y)][fld]))
            H[i,j]=H[j,i]=(vals[0]-vals[1]-vals[2]+vals[3])/4.
    eig,vec=np.linalg.eigh(H)
    for j in range(vec.shape[1]):
        q=int(np.argmax(np.abs(vec[:,j])))
        if vec[q,j]<0: vec[:,j]*=-1
    delta=-np.linalg.pinv(H,rcond=1e-10)@g
    rn=ev(np.clip(delta,-1.,1.),f'newton_trust_{which}')
    return {
        'S_center':S0,'gradient_y':g.tolist(),'max_abs_gradient_y':float(np.max(np.abs(g))),
        'hessian_y':H.tolist(),'eigenvalues_y':eig.tolist(),'eigenvectors_y':vec.T.tolist(),
        'positive_definite':bool(np.all(eig>PD_THRESH)),
        'newton_delta':delta.tolist(),'S_newton':float(rn[fld]),'newton_params':rn['params']
    }

def finalize(block,which):
    fld='S_B9_eff' if which=='eff' else 'S_B9_k01'
    best=min(E.values(),key=lambda r:float(r[fld])); S0=float(block['S_center'])
    block.update({
        'best_exact_S':float(best[fld]),'best_improvement':float(S0-float(best[fld])),
        'best_label':best['label'],'best_params':best['params'],
        'best_selection_scope':'all_exact_points_after_both_mapping_newton_candidates'
    })
    return block

EFF=build('eff'); K01=build('k01')
EFF=finalize(EFF,'eff'); K01=finalize(K01,'k01')
summary={
    'classification':'B9_RTK_STATIONARITY_HESSIAN_COMPLETE','model':'RTK','objective':TARGET['objective'],
    'production_mapping':'eff','center':CENTER,'center_fingerprint':CENTER_FP,'target_fingerprint':TARGET_FP,
    'parent_run_id':TARGET['parent_run_id'],'parent_artifact_id':TARGET['parent_artifact_id'],
    'stencil_scale':SCALE,'base_steps':TARGET['base_steps'],'scaled_steps':STEPS,'points':len(E),
    'center_replay_abs_error':center_err,'eff':EFF,'k01':K01,'recenter_tolerance_S':TOL,
    'positive_definite_threshold':PD_THRESH,'provenance':PROV,
    'selection_guard':'production eff best selection occurs only after both eff/k01 Newton candidates are exact-evaluated',
    'warning':'Local B9-v1 numerical Hessian only; not a global minimum, significance, AIC/BIC, posterior preference or Bayes factor.'
}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n')
print('B9_RTK_STATIONARITY_HESSIAN_COMPLETE',SCALE,json.dumps(summary,sort_keys=True,allow_nan=False),flush=True)
