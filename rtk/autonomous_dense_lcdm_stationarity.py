#!/usr/bin/env python3
"""State-driven matched-ultra+dense LCDM 6D Hessian/stationarity worker."""
from pathlib import Path
import hashlib, json, os, subprocess, sys, time
import numpy as np

sys.argv=['autonomous_dense_lcdm_stationarity','planck_data']
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
CENTER=dict(STATE['lcdm']['accepted_center'])
# LCDM owns its finite-difference scale. Do not silently inherit scientific
# settings from the RTK block just because shared coordinates use the same
# numerical steps today.
DEFAULT_LCDM_STEPS={'h':0.00035,'Ob':0.00007,'Om':0.0007,'As':4e-12,'ns':0.00035,'zre':0.07}
bs=dict(STATE.get('lcdm',{}).get('base_steps',DEFAULT_LCDM_STEPS))
BASE=[('h',float(bs['h'])),('Ob',float(bs['Ob'])),('Om',float(bs['Om'])),('As',float(bs['As'])),('ns',float(bs['ns'])),('zre',float(bs['zre']))]
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
orig=L.make_ini
OUT=Path('output/autonomous_dense_lcdm_stationarity');OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl';FAILURES=OUT/'failures.jsonl'


def canonical_hash(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None


CENTER_FINGERPRINT=canonical_hash({'model':'LCDM','center':CENTER,'objective':STATE['objective']['name'],'mapping':STATE.get('production_mapping','eff')})
OBJECTIVE_FINGERPRINT=canonical_hash(STATE['objective'])
PROVENANCE={
    'state_iteration':STATE.get('iteration'),
    'center_fingerprint':CENTER_FINGERPRINT,
    'objective_fingerprint':OBJECTIVE_FINGERPRINT,
    'rtk_source_commit':git_head('..'),
    'class_upstream_commit':git_head('.'),
    'pantheon_commit':git_head('pantheon'),
    'numpy_version':np.__version__,
}
(OUT/'provenance.json').write_text(json.dumps(PROVENANCE,indent=2,sort_keys=True)+'\n')


def make_ini(model,p,tag):
    path=orig(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text);f.write('\n# autonomous matched-ultra+dense LCDM 6D Hessian\n')
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
    p=dict(CENTER)
    for yi,(n,s) in zip(np.asarray(y,float),BASE):p[n]=CENTER[n]+float(yi)*s
    return p


def key(y):return tuple(float(x) for x in np.asarray(y,float))


def append_jsonl(path,row):
    with path.open('a') as f:
        f.write(json.dumps(row,sort_keys=True,default=str)+'\n');f.flush()


def ev(y,label):
    y=np.asarray(y,float);k=key(y)
    if k in E:return E[k]
    last=None
    for attempt in range(1,4):
        # The generic core historically cached failures. Clear it before each
        # attempt so retries repeat the identical exact point rather than a
        # cached non-success result. Scientific coordinates never change.
        L.CACHE.clear()
        try:r=L.evaluate('LCDM',pars(y))
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            rr={
                'label':label,'attempt':attempt,
                'center_fingerprint':CENTER_FINGERPRINT,
                'y':y.tolist(),
                'score_eff':float(r['score']),
                'score_k01':float(r['score_k01']),
                'params':pars(y),
            }
            E[k]=rr;rows.append(rr);cleanup(r.get('tag'));append_jsonl(POINTS,rr)
            print('AUTO_DENSE_LCDM_HESSIAN_POINT',json.dumps(rr,sort_keys=True),flush=True)
            return rr
        last=r
        failure={
            'label':label,'attempt':attempt,
            'center_fingerprint':CENTER_FINGERPRINT,
            'y':y.tolist(),'params':pars(y),'result':r,
        }
        append_jsonl(FAILURES,failure)
        print('AUTO_DENSE_LCDM_HESSIAN_RETRY',json.dumps(failure,sort_keys=True,default=str),flush=True)
        cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'{label}: failed after 3 exact retries: {last}')


z=np.zeros(N);r0=ev(z,'center');S0=r0['score_eff']
for i in range(N):
    for s in (-1.,1.):
        y=np.zeros(N);y[i]=s;ev(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for a in (-1.,1.):
            for b in (-1.,1.):
                y=np.zeros(N);y[i]=a;y[j]=b;ev(y,f'cross_{i}_{j}_{int(a):+d}_{int(b):+d}')
g=np.zeros(N);H=np.zeros((N,N))
for i in range(N):
    yp=np.zeros(N);ym=np.zeros(N);yp[i]=1;ym[i]=-1
    sp=E[key(yp)]['score_eff'];sm=E[key(ym)]['score_eff'];g[i]=(sp-sm)/2;H[i,i]=sp-2*S0+sm
for i in range(N):
    for j in range(i+1,N):
        vals=[]
        for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
            y=np.zeros(N);y[i]=a;y[j]=b;vals.append(E[key(y)]['score_eff'])
        H[i,j]=H[j,i]=(vals[0]-vals[1]-vals[2]+vals[3])/4
eig=np.linalg.eigvalsh(H);delta=-np.linalg.pinv(H,rcond=1e-10)@g
rn=ev(np.clip(delta,-1,1),'newton_trust')
best=min(E.values(),key=lambda r:r['score_eff'])
summary={
    'stage':'autonomous-dense-lcdm-6d-stationarity',
    'objective':STATE['objective']['name'],
    'center':CENTER,
    'center_fingerprint':CENTER_FINGERPRINT,
    'objective_fingerprint':OBJECTIVE_FINGERPRINT,
    'provenance':PROVENANCE,
    'base_steps':dict(BASE),
    'points':len(E),
    'S_center':S0,
    'gradient_y':g.tolist(),
    'max_abs_gradient_y':float(np.max(np.abs(g))),
    'hessian_y':H.tolist(),
    'eigenvalues_y':eig.tolist(),
    'positive_definite':bool(np.all(eig>1e-8)),
    'newton_delta':delta.tolist(),
    'S_newton':rn['score_eff'],
    'newton_params':rn['params'],
    'best_exact_S':best['score_eff'],
    'best_improvement':S0-best['score_eff'],
    'best_label':best['label'],
    'best_params':best['params'],
    'warning':'Local numerical Hessian on frozen production objective; retries repeat identical exact points and do not alter the objective; not global evidence or model selection.',
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('AUTO_DENSE_LCDM_STATIONARITY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('AUTO_DENSE_LCDM_STATIONARITY_COMPLETE',flush=True)
