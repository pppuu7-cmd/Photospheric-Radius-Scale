#!/usr/bin/env python3
"""Paired B4 minimal-neutrino exact Hessian worker.

This worker is a robustness proof component only.  It reads pre-registered
centers/steps from b4_neutrino_stationarity_targets_v1.json and never mutates
the frozen massless state.  The production objective is eff; k01 is calculated
in parallel and must not choose the eff center.
"""
from pathlib import Path
import copy, hashlib, json, math, os, subprocess, sys, time
import numpy as np

os.environ.setdefault('CLIPY_NOJAX','1')
import inference_core as L

MODEL=(sys.argv[1] if len(sys.argv)>1 else '').upper()
if MODEL not in ('RTK','LCDM'):
    raise SystemExit('usage: neutrino_stationarity_hessian.py RTK|LCDM')
SCALE=float(os.environ.get('RTK_B4_STENCIL_SCALE','1.0'))
if SCALE not in (1.0,0.5,0.25,0.125):
    raise RuntimeError(f'unsupported B4 stencil scale {SCALE!r}')

ROOT=Path('..')
TARGETS=json.loads((ROOT/'research/robustness/b4_neutrino_stationarity_targets_v1.json').read_text())
CFG=TARGETS['models'][MODEL]
CENTER=copy.deepcopy(CFG['center'])
OBJ=TARGETS['objective']
TOL=float(TARGETS['recenter_tolerance_S'])
DENSE=json.loads((ROOT/'research/state/current.json').read_text())['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in json.loads((ROOT/'research/state/current.json').read_text())['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
if MODEL=='RTK':
    AXES=['loglam','h','Ob','Om','As','ns','zre']
else:
    AXES=['h','Ob','Om','As','ns','zre']
STEPS={k:float(v)*SCALE for k,v in CFG['base_steps'].items()}
N=len(AXES)

OUT=ROOT/'output/b4_neutrino_stationarity'/MODEL.lower()/f'scale_{SCALE:g}'
OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl';FAILURES=OUT/'failures.jsonl';SUMMARY=OUT/'summary.json';PROVFILE=OUT/'provenance.json'


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None

TARGET_FP=canonical_hash(TARGETS)
CENTER_FP=canonical_hash({'model':MODEL,'center':CENTER,'objective':OBJ,'mapping':TARGETS['production_mapping'],'neutrino':TARGETS['neutrino']})
PROV={
    'model':MODEL,'stencil_scale':SCALE,'target_fingerprint':TARGET_FP,'center_fingerprint':CENTER_FP,
    'source_seed_run_id':TARGETS['source_seed_run_id'],'massless_final_replay_run_id':TARGETS['massless_final_replay_run_id'],
    'rtk_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon'),
    'numpy_version':np.__version__,
}
PROVFILE.write_text(json.dumps(PROV,indent=2,sort_keys=True)+'\n')

ORIG=L.make_ini

def make_ini(model,p,tag):
    path=ORIG(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('expected sparse z_pk baseline not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    if 'N_ur = 3.046' not in text or 'N_ncdm = 0' not in text:
        raise RuntimeError('frozen massless neutrino block not found')
    text=text.replace('N_ur = 3.046','N_ur = 2.0328',1)
    text=text.replace('N_ncdm = 0','N_ncdm = 1\nm_ncdm = 0.06\nT_ncdm = 0.71611\ndeg_ncdm = 1.0',1)
    text+='\n# B4 neutrino stationarity ultra overrides\n'
    text+=''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text)
    return path
L.make_ini=make_ini

E={}
def key(y):return tuple(float(x).hex() for x in np.asarray(y,float))

def pars(y):
    y=np.asarray(y,float);p=copy.deepcopy(CENTER)
    for yi,a in zip(y,AXES):
        if a=='loglam':p['lam']=float(CENTER['lam'])*math.exp(float(yi)*STEPS[a])
        else:p[a]=float(CENTER[a])+float(yi)*STEPS[a]
    if MODEL=='LCDM':p['lam']=0.0
    return p

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def append(path,row):
    with path.open('a') as f:f.write(json.dumps(row,sort_keys=True,default=str)+'\n');f.flush()

def ev(y,label):
    y=np.asarray(y,float);k=key(y)
    if k in E:return E[k]
    p=pars(y);last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate(MODEL,p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'label':label,'attempt':attempt,'y':y.tolist(),'params':p,'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
                 'logL_planck':r.get('logL_planck'),'chi2_SN':r.get('chi2_SN'),'chi2_BOSS_eff':r.get('chi2_BOSS_eff'),'chi2_BOSS_k01':r.get('chi2_BOSS_k01'),'rd':r.get('rd')}
            E[k]=row;append(POINTS,row);cleanup(r.get('tag'))
            print('B4_NEUTRINO_HESSIAN_POINT',MODEL,SCALE,json.dumps(row,sort_keys=True),flush=True)
            return row
        last=r;failure={'label':label,'attempt':attempt,'y':y.tolist(),'params':p,'result':r};append(FAILURES,failure);cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'{MODEL} {label}: failed after 3 identical exact retries: {last}')

z=np.zeros(N);ev(z,'center')
for i in range(N):
    for s in (-1.,1.):
        y=np.zeros(N);y[i]=s;ev(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for a in (-1.,1.):
            for b in (-1.,1.):
                y=np.zeros(N);y[i]=a;y[j]=b;ev(y,f'cross_{i}_{j}_{int(a):+d}_{int(b):+d}')


def build(which):
    fld='score_eff' if which=='eff' else 'score_k01';S0=float(E[key(np.zeros(N))][fld]);g=np.zeros(N);H=np.zeros((N,N))
    for i in range(N):
        yp=np.zeros(N);ym=np.zeros(N);yp[i]=1;ym[i]=-1
        sp=float(E[key(yp)][fld]);sm=float(E[key(ym)][fld]);g[i]=(sp-sm)/2.;H[i,i]=sp-2.*S0+sm
    for i in range(N):
        for j in range(i+1,N):
            vv=[]
            for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
                y=np.zeros(N);y[i]=a;y[j]=b;vv.append(float(E[key(y)][fld]))
            H[i,j]=H[j,i]=(vv[0]-vv[1]-vv[2]+vv[3])/4.
    vals,vecs=np.linalg.eigh(H)
    for j in range(vecs.shape[1]):
        q=int(np.argmax(np.abs(vecs[:,j])))
        if vecs[q,j]<0:vecs[:,j]*=-1
    delta=-np.linalg.pinv(H,rcond=1e-10)@g
    rn=ev(np.clip(delta,-1.,1.),f'newton_trust_{which}')
    best=min(E.values(),key=lambda r:float(r[fld]))
    return {'S_center':S0,'gradient_y':g.tolist(),'max_abs_gradient_y':float(np.max(np.abs(g))),
            'hessian_y':H.tolist(),'eigenvalues_y':vals.tolist(),'eigenvectors_y':vecs.T.tolist(),
            'positive_definite':bool(np.all(vals>float(TARGETS['proof_logic']['positive_definite_threshold']))),
            'newton_delta':delta.tolist(),'S_newton':float(rn[fld]),'newton_params':rn['params'],
            'best_exact_S':float(best[fld]),'best_improvement':float(S0-float(best[fld])),'best_label':best['label'],'best_params':best['params']}

EFF=build('eff');K01=build('k01')
summary={'classification':'B4_NEUTRINO_STATIONARITY_HESSIAN_COMPLETE','model':MODEL,'objective':OBJ,'production_mapping':'eff',
         'neutrino':TARGETS['neutrino'],'center':CENTER,'center_fingerprint':CENTER_FP,'target_fingerprint':TARGET_FP,
         'source_seed_run_id':TARGETS['source_seed_run_id'],'stencil_scale':SCALE,'base_steps':CFG['base_steps'],'scaled_steps':STEPS,
         'points':len(E),'eff':EFF,'k01':K01,'recenter_tolerance_S':TOL,'provenance':PROV,
         'warning':'B4 robustness local numerical Hessian only; not a global minimum, model-selection statistic, or replacement of the massless A1-A5 result.'}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('B4_NEUTRINO_STATIONARITY_HESSIAN_COMPLETE',MODEL,SCALE,json.dumps(summary,sort_keys=True),flush=True)
