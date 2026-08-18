#!/usr/bin/env python3
"""State-driven matched-ultra+dense RTK 7D Hessian/stationarity worker."""
from pathlib import Path
import hashlib, json, math, os, subprocess, sys, time
import numpy as np

sys.argv=['autonomous_dense_rtk_stationarity','planck_data']
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
CENTER=dict(STATE['rtk']['accepted_center'])
STENCIL_SCALE=float(os.environ.get('RTK_STENCIL_SCALE','1.0'))
if not (math.isfinite(STENCIL_SCALE) and STENCIL_SCALE>0.):
    raise RuntimeError(f'invalid RTK_STENCIL_SCALE={STENCIL_SCALE!r}')
bs=STATE['rtk']['base_steps']
BASE=[('loglam',float(bs['loglam'])*STENCIL_SCALE),('h',float(bs['h'])*STENCIL_SCALE),('Ob',float(bs['Ob'])*STENCIL_SCALE),('Om',float(bs['Om'])*STENCIL_SCALE),('As',float(bs['As'])*STENCIL_SCALE),('ns',float(bs['ns'])*STENCIL_SCALE),('zre',float(bs['zre'])*STENCIL_SCALE)]
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
orig=L.make_ini
OUT=Path('output/autonomous_dense_rtk_stationarity');OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl';FAILURES=OUT/'failures.jsonl'

def canonical_hash(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()
CENTER_FINGERPRINT=canonical_hash({'model':'RTK','center':CENTER,'objective':STATE['objective']['name'],'mapping':STATE.get('production_mapping','eff')})
OBJECTIVE_FINGERPRINT=canonical_hash(STATE['objective'])

def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None
PROVENANCE={'state_iteration':STATE.get('iteration'),'center_fingerprint':CENTER_FINGERPRINT,'objective_fingerprint':OBJECTIVE_FINGERPRINT,'stencil_scale':STENCIL_SCALE,'rtk_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon'),'numpy_version':np.__version__}
(OUT/'provenance.json').write_text(json.dumps(PROVENANCE,indent=2,sort_keys=True)+'\n')

def make_ini(model,p,tag):
    path=orig(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text);f.write(f'\n# autonomous matched-ultra+dense RTK 7D Hessian stencil_scale={STENCIL_SCALE}\n')
        for k,v in ULTRA.items():f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini
N=len(BASE);E={};rows=[]

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def pars(y):
    y=np.asarray(y,float);p=dict(CENTER);p['lam']=CENTER['lam']*math.exp(float(y[0])*BASE[0][1])
    for yi,(n,s) in zip(y[1:],BASE[1:]):p[n]=CENTER[n]+float(yi)*s
    return p

def key(y):return tuple(float(x) for x in np.asarray(y,float))

def append_jsonl(path,row):
    with path.open('a') as f:f.write(json.dumps(row,sort_keys=True,default=str)+'\n');f.flush()

def ev(y,label):
    y=np.asarray(y,float);k=key(y)
    if k in E:return E[k]
    last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate('RTK',pars(y))
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            rr={'label':label,'attempt':attempt,'center_fingerprint':CENTER_FINGERPRINT,'stencil_scale':STENCIL_SCALE,'y':y.tolist(),'score_eff':float(r['score']),'score_k01':float(r['score_k01']),'params':pars(y)}
            E[k]=rr;rows.append(rr);cleanup(r.get('tag'));append_jsonl(POINTS,rr)
            print('AUTO_DENSE_RTK_HESSIAN_POINT',json.dumps(rr,sort_keys=True),flush=True);return rr
        last=r;failure={'label':label,'attempt':attempt,'center_fingerprint':CENTER_FINGERPRINT,'stencil_scale':STENCIL_SCALE,'y':y.tolist(),'params':pars(y),'result':r};append_jsonl(FAILURES,failure)
        print('AUTO_DENSE_RTK_HESSIAN_RETRY',json.dumps(failure,sort_keys=True,default=str),flush=True);cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'{label}: failed after 3 exact retries: {last}')

z=np.zeros(N);r0=ev(z,'center')
for i in range(N):
    for s in (-1.,1.):
        y=np.zeros(N);y[i]=s;ev(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for a in (-1.,1.):
            for b in (-1.,1.):
                y=np.zeros(N);y[i]=a;y[j]=b;ev(y,f'cross_{i}_{j}_{int(a):+d}_{int(b):+d}')

def canonicalize_eigenvectors_columns(v):
    v=np.array(v,float,copy=True)
    for j in range(v.shape[1]):
        i=int(np.argmax(np.abs(v[:,j])))
        if v[i,j]<0:v[:,j]*=-1.0
    return v

def geom(field):
    S0=r0[field];g=np.zeros(N);H=np.zeros((N,N))
    for i in range(N):
        yp=np.zeros(N);ym=np.zeros(N);yp[i]=1;ym[i]=-1
        sp=E[key(yp)][field];sm=E[key(ym)][field];g[i]=(sp-sm)/2;H[i,i]=sp-2*S0+sm
    for i in range(N):
        for j in range(i+1,N):
            vals=[]
            for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
                y=np.zeros(N);y[i]=a;y[j]=b;vals.append(E[key(y)][field])
            H[i,j]=H[j,i]=(vals[0]-vals[1]-vals[2]+vals[3])/4
    eig,evec=np.linalg.eigh(H);evec=canonicalize_eigenvectors_columns(evec)
    delta=-np.linalg.pinv(H,rcond=1e-10)@g
    return g,H,eig,evec,delta

ge,He,ee,vee,de=geom('score_eff');gk,Hk,ek,vek,dk=geom('score_k01')
rne=ev(np.clip(de,-1,1),'newton_trust_eff');rnk=ev(np.clip(dk,-1,1),'newton_trust_k01')
best_eff=min(E.values(),key=lambda r:r['score_eff']);best_k01=min(E.values(),key=lambda r:r['score_k01'])
summary={'stage':'autonomous-dense-rtk-7d-stationarity','objective':STATE['objective']['name'],'center':CENTER,'center_fingerprint':CENTER_FINGERPRINT,'objective_fingerprint':OBJECTIVE_FINGERPRINT,'provenance':PROVENANCE,'stencil_scale':STENCIL_SCALE,'base_steps':dict(BASE),'points':len(E),'eigenvector_convention':'rows correspond to sorted ascending eigenvalues; sign fixed by largest-absolute component positive','eff':{'S_center':r0['score_eff'],'gradient_y':ge.tolist(),'max_abs_gradient_y':float(np.max(np.abs(ge))),'hessian_y':He.tolist(),'eigenvalues_y':ee.tolist(),'eigenvectors_y':vee.T.tolist(),'positive_definite':bool(np.all(ee>1e-8)),'newton_delta':de.tolist(),'S_newton':rne['score_eff'],'newton_params':rne['params'],'best_exact_S':best_eff['score_eff'],'best_improvement':r0['score_eff']-best_eff['score_eff'],'best_label':best_eff['label'],'best_params':best_eff['params']},'k01':{'S_center':r0['score_k01'],'gradient_y':gk.tolist(),'max_abs_gradient_y':float(np.max(np.abs(gk))),'hessian_y':Hk.tolist(),'eigenvalues_y':ek.tolist(),'eigenvectors_y':vek.T.tolist(),'positive_definite':bool(np.all(ek>1e-8)),'newton_delta':dk.tolist(),'S_newton':rnk['score_k01'],'newton_params':rnk['params'],'best_exact_S':best_k01['score_k01'],'best_improvement':r0['score_k01']-best_k01['score_k01'],'best_label':best_k01['label'],'best_params':best_k01['params']},'warning':'Local mapping-specific numerical Hessian on frozen production objective; retries repeat identical exact points and do not alter the objective; not posterior evidence or global model selection.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('AUTO_DENSE_RTK_STATIONARITY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('AUTO_DENSE_RTK_STATIONARITY_COMPLETE',flush=True)
