#!/usr/bin/env python3
"""B10 T3 exact 6D fixed-lambda stationarity worker.

This worker certifies (or falsifies) local stationarity only in the six shared
cosmological coordinates at a preregistered large-lambda anchor. Lambda itself
is fixed exactly. It does not make a global-minimum or model-selection claim.
"""
from pathlib import Path
import copy,hashlib,json,math,os,subprocess,sys,time
import numpy as np

os.environ.setdefault('CLIPY_NOJAX','1')
sys.argv=['b10_fixed_lambda_stationarity','planck_data']
import inference_core as L

FACTOR=os.environ.get('B10_FACTOR','')
if FACTOR not in ('64','16384'):
    raise RuntimeError('B10_FACTOR must be 64 or 16384')
SCALE=float(os.environ.get('B10_T3_STENCIL_SCALE','1.0'))
if SCALE not in (1.0,0.5,0.25,0.125):
    raise RuntimeError(f'unsupported B10 T3 stencil scale {SCALE}')
ROOT=Path('..')
STATE=json.loads((ROOT/'research/state/current.json').read_text())
TARGET=json.loads((ROOT/'research/robustness/b10_t3_fixed_lambda_stationarity_targets.json').read_text())
if TARGET['classification']!='B10_T3_BASE_TARGETS_FROZEN_BEFORE_FIRST_STATIONARITY':
    raise RuntimeError('B10 T3 target classification mismatch')
if TARGET['objective']!=STATE['objective']['name']:
    raise RuntimeError('B10 T3 objective mismatch')
ANCHOR=TARGET['anchors'][FACTOR]
CENTER=copy.deepcopy(ANCHOR['center']);LAMBDA=float(ANCHOR['lambda_D'])
if float(CENTER['lam'])!=LAMBDA:raise RuntimeError('fixed lambda target mismatch')
AXES=list(TARGET['axes']);STEPS={k:float(v)*SCALE for k,v in TARGET['base_steps'].items()}
N=len(AXES)
if N!=6:raise RuntimeError(f'expected 6 shared axes, got {AXES}')
OBJ=TARGET['objective'];TOL=float(TARGET['recenter_tolerance_S']);PD_TOL=float(TARGET['positive_definite_threshold'])
DENSE=STATE['objective']['dense_z_pk'];ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()};SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
ORIG=L.make_ini

def make_ini(model,p,tag):
    if model!='RTK':raise RuntimeError('B10 T3 is RTK-only')
    if float(p['lam'])!=LAMBDA:raise RuntimeError('lambda changed inside fixed-lambda worker')
    path=ORIG(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('sparse z_pk baseline missing')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    text+='\n# B10 T3 exact fixed-lambda stationarity\n'+''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text);return path
L.make_ini=make_ini

OUT=ROOT/'output/b10_t3_fixed_lambda'/f'f{FACTOR}'/f'scale_{SCALE:g}';OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl';FAILURES=OUT/'failures.jsonl';SUMMARY=OUT/'summary.json';PROV=OUT/'provenance.json'
E={}

def canonical_hash(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None

def key(y):return tuple(float(x).hex() for x in np.asarray(y,float))
def pars(y):
    y=np.asarray(y,float);p=copy.deepcopy(CENTER);p['lam']=LAMBDA
    for yi,a in zip(y,AXES):p[a]=float(CENTER[a])+float(yi)*STEPS[a]
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
    if float(p['lam'])!=LAMBDA:raise RuntimeError('lambda mutation')
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate('RTK',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'label':label,'attempt':attempt,'y':y.tolist(),'params':p,'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
                 'logL_planck':r.get('logL_planck'),'chi2_SN':r.get('chi2_SN'),'chi2_BOSS_eff':r.get('chi2_BOSS_eff'),'chi2_BOSS_k01':r.get('chi2_BOSS_k01'),'rd':r.get('rd')}
            E[k]=row;append(POINTS,row);cleanup(r.get('tag'))
            print('B10_T3_POINT',FACTOR,SCALE,json.dumps(row,sort_keys=True),flush=True);return row
        last=r;append(FAILURES,{'label':label,'attempt':attempt,'y':y.tolist(),'params':p,'result':r});cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'B10 T3 factor {FACTOR} {label} failed after 3 exact retries: {last}')

prov={'classification':'B10_T3_FIXED_LAMBDA_PROVENANCE','factor':float(FACTOR),'lambda_D':LAMBDA,'stencil_scale':SCALE,
      'target_fingerprint':canonical_hash(TARGET),'center_fingerprint':canonical_hash(CENTER),'rtk_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon'),'numpy_version':np.__version__}
PROV.write_text(json.dumps(prov,indent=2,sort_keys=True)+'\n')

z=np.zeros(N);rcenter=ev(z,'center')
expected=float(ANCHOR['t2_best_score_eff'])
if abs(float(rcenter['score_eff'])-expected)>2e-6:
    raise RuntimeError(f'T2/T3 center replay mismatch: {rcenter["score_eff"]} vs {expected}')
for i in range(N):
    for s in (-1.,1.):
        y=np.zeros(N);y[i]=s;ev(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for a in (-1.,1.):
            for b in (-1.,1.):
                y=np.zeros(N);y[i]=a;y[j]=b;ev(y,f'cross_{i}_{j}_{int(a):+d}_{int(b):+d}')

def build(which):
    fld='score_eff' if which=='eff' else 'score_k01';zero=np.zeros(N);S0=float(E[key(zero)][fld]);g=np.zeros(N);H=np.zeros((N,N))
    for i in range(N):
        yp=np.zeros(N);ym=np.zeros(N);yp[i]=1.;ym[i]=-1.
        sp=float(E[key(yp)][fld]);sm=float(E[key(ym)][fld]);g[i]=(sp-sm)/2.;H[i,i]=sp-2.*S0+sm
    for i in range(N):
        for j in range(i+1,N):
            vals=[]
            for a,b in ((1.,1.),(1.,-1.),(-1.,1.),(-1.,-1.)):
                y=np.zeros(N);y[i]=a;y[j]=b;vals.append(float(E[key(y)][fld]))
            H[i,j]=H[j,i]=(vals[0]-vals[1]-vals[2]+vals[3])/4.
    eigvals,eigvecs=np.linalg.eigh(H)
    for j in range(eigvecs.shape[1]):
        q=int(np.argmax(np.abs(eigvecs[:,j])))
        if eigvecs[q,j]<0:eigvecs[:,j]*=-1
    delta=-np.linalg.pinv(H,rcond=1e-10)@g
    trust=np.clip(delta,-1.,1.)
    rn=ev(trust,f'newton_trust_{which}')
    best=min(E.values(),key=lambda r:float(r[fld]))
    return {'S_center':S0,'gradient_y':g.tolist(),'max_abs_gradient_y':float(np.max(np.abs(g))),
            'hessian_y':H.tolist(),'eigenvalues_y':eigvals.tolist(),'eigenvectors_y':eigvecs.T.tolist(),
            'positive_definite':bool(np.all(eigvals>PD_TOL)),'newton_delta':delta.tolist(),'newton_trust_y':trust.tolist(),'S_newton':float(rn[fld]),
            'newton_params':rn['params'],'best_exact_S':float(best[fld]),'best_improvement':float(S0-float(best[fld])),'best_label':best['label'],'best_params':best['params']}

EFF=build('eff');K01=build('k01')
if EFF['best_improvement']>TOL:
    nxt='RECENTER_REQUIRED_BEFORE_HALF_SCALE'
elif not EFF['positive_definite']:
    nxt='EXACT_NEGATIVE_MODE_RAY_REQUIRED'
else:
    nxt='HALF_SCALE_FIXED_LAMBDA_VALIDATION_REQUIRED'
summary={'classification':'B10_T3_FIXED_LAMBDA_BASE_STATIONARITY_COMPLETE','objective':OBJ,'production_mapping':'eff','factor':float(FACTOR),'lambda_D':LAMBDA,
         'anchor_role':ANCHOR['role'],'center':CENTER,'t2_expected_center_score_eff':expected,'stencil_scale':SCALE,'base_steps':TARGET['base_steps'],'scaled_steps':STEPS,
         'points':len(E),'eff':EFF,'k01':K01,'recenter_tolerance_S':TOL,'positive_definite_threshold':PD_TOL,'provenance':prov,'next_required_gate':nxt,
         'warning':'Fixed-lambda six-dimensional local stationarity gate only; no global minimum, confidence interval, Bayes factor, significance, or B10 closure from this base stencil alone.'}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('B10_T3_FIXED_LAMBDA_BASE_STATIONARITY_COMPLETE',FACTOR,SCALE,json.dumps(summary,sort_keys=True),flush=True)
