#!/usr/bin/env python3
"""Matched-ultra+dense-BOSS 6D LCDM local Hessian/stationarity audit."""
from pathlib import Path
import json, numpy as np
import inference_core as L
CENTER={'lam':0.0,'h':0.6779337587382693,'Ob':0.04872764689799632,'Om':0.26187225794495356,'As':2.1094040998203598e-9,'ns':0.9649685632254442,'zre':7.8583129349509475}
BASE=[('h',0.00035),('Ob',0.00007),('Om',0.00070),('As',4e-12),('ns',0.00035),('zre',0.070)]
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'; DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
orig=L.make_ini
def make_ini(model,p,tag):
    path=orig(model,p,tag); text=Path(path).read_text(); text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text); f.write('\n# matched-ultra+dense overrides\n'); [f.write(f'{k} = {v}\n') for k,v in ULTRA.items()]
    return path
L.make_ini=make_ini
N=len(BASE); E={}; rows=[]
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
    for yi,(n,s) in zip(y,BASE):p[n]+=float(yi)*s
    return p
def key(y):return tuple(float(x) for x in y)
def ev(y,label):
    y=np.asarray(y,float); k=key(y)
    if k in E:return E[k]
    L.CACHE.clear(); r=L.evaluate('LCDM',pars(y))
    if not r.get('ok'):raise RuntimeError(f'{label}: {r}')
    rr={'label':label,'y':y.tolist(),'score_eff':float(r['score']),'score_k01':float(r['score_k01']),'params':pars(y)};E[k]=rr;rows.append(rr);cleanup(r.get('tag'));print('DENSE_LCDM_HESSIAN_POINT',json.dumps(rr,sort_keys=True),flush=True);return rr
z=np.zeros(N); S0=ev(z,'center')['score_eff']
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
        v=[]
        for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
            y=np.zeros(N);y[i]=a;y[j]=b;v.append(E[key(y)]['score_eff'])
        H[i,j]=H[j,i]=(v[0]-v[1]-v[2]+v[3])/4
eig=np.linalg.eigvalsh(H); pd=bool(np.all(eig>1e-8)); delta=-np.linalg.pinv(H,rcond=1e-10)@g; trust=np.clip(delta,-1,1); sn=ev(trust,'newton_trust')['score_eff']; best=min(x['score_eff'] for x in E.values())
summary={'stage':'dense-lcdm-6d-stationarity','objective':'matched-ultra-linstep2+dense-BOSS','center':CENTER,'S_center':S0,'gradient_y':g.tolist(),'hessian_y':H.tolist(),'eigenvalues_y':eig.tolist(),'positive_definite':pd,'newton_delta':delta.tolist(),'S_newton':sn,'best_exact_S':best,'best_improvement':S0-best,'points':len(E),'warning':'Local numerical Hessian only; not global evidence or model selection.'}
out=Path('output/dense_lcdm_stationarity');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print('DENSE_LCDM_STATIONARITY_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('DENSE_LCDM_STATIONARITY_COMPLETE',flush=True)
