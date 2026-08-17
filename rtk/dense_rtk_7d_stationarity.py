#!/usr/bin/env python3
"""Full matched-ultra+dense-BOSS RTK 7D local Hessian/stationarity audit.

Prepared behind the dense 7D axis gate. Uses the same Round5 center and base
steps; evaluates center, +/- axes, all pairwise cross corners, then separate
exact Newton/trust proposals for eff and k01. One CLASS evaluation supplies
both scores, but the two BOSS mappings are treated as separate objectives.
"""
from pathlib import Path
import json, math, sys
import numpy as np
sys.argv=['dense_rtk_7d_stationarity','planck_data']
import inference_core as L

CENTER={'lam':217225.01601516694,'h':0.6904831253428524,'Ob':0.046836300417955265,'Om':0.25300743080221694,'As':2.0837288833768707e-9,'ns':0.9643603115669437,'zre':7.21843542110055}
BASE=[('loglam',0.05),('h',0.00035),('Ob',0.00007),('Om',0.00070),('As',4e-12),('ns',0.00035),('zre',0.070)]
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
TOL=0.005
orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text);f.write('\n# matched-ultra+dense RTK 7D Hessian\n')
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

def ev(y,label):
    y=np.asarray(y,float);k=key(y)
    if k in E:return E[k]
    L.CACHE.clear();r=L.evaluate('RTK',pars(y))
    if not r.get('ok'):raise RuntimeError(f'{label}: {r}')
    rr={'label':label,'y':y.tolist(),'score_eff':float(r['score']),'score_k01':float(r['score_k01']),'params':pars(y)}
    E[k]=rr;rows.append(rr);cleanup(r.get('tag'))
    print('DENSE_RTK_HESSIAN_POINT',json.dumps(rr,sort_keys=True),flush=True)
    return rr

z=np.zeros(N);r0=ev(z,'center')
for i in range(N):
    for s in (-1.,1.):
        y=np.zeros(N);y[i]=s;ev(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for a in (-1.,1.):
            for b in (-1.,1.):
                y=np.zeros(N);y[i]=a;y[j]=b;ev(y,f'cross_{i}_{j}_{int(a):+d}_{int(b):+d}')

def geom(field):
    S0=r0[field];g=np.zeros(N);H=np.zeros((N,N))
    for i in range(N):
        yp=np.zeros(N);ym=np.zeros(N);yp[i]=1;ym[i]=-1
        sp=E[key(yp)][field];sm=E[key(ym)][field]
        g[i]=(sp-sm)/2;H[i,i]=sp-2*S0+sm
    for i in range(N):
        for j in range(i+1,N):
            v=[]
            for a,b in ((1,1),(1,-1),(-1,1),(-1,-1)):
                y=np.zeros(N);y[i]=a;y[j]=b;v.append(E[key(y)][field])
            H[i,j]=H[j,i]=(v[0]-v[1]-v[2]+v[3])/4
    eig=np.linalg.eigvalsh(H)
    delta=-np.linalg.pinv(H,rcond=1e-10)@g
    return g,H,eig,delta

ge,He,ee,de=geom('score_eff')
gk,Hk,ek,dk=geom('score_k01')

# Each mapping gets its own exact trust proposal. If the two proposals happen to
# be identical, memoization reuses the same physical evaluation without mixing
# the geometry used to construct them.
trust_eff=np.clip(de,-1,1)
trust_k01=np.clip(dk,-1,1)
rn_eff=ev(trust_eff,'newton_trust_eff')
rn_k01=ev(trust_k01,'newton_trust_k01')

best_eff=min(E.values(),key=lambda r:r['score_eff'])
best_k01=min(E.values(),key=lambda r:r['score_k01'])
imp_eff=r0['score_eff']-best_eff['score_eff']
imp_k01=r0['score_k01']-best_k01['score_k01']

summary={
 'stage':'dense-rtk-7d-stationarity',
 'objective':'matched-ultra-linstep2+dense-BOSS',
 'center':CENTER,
 'base_steps':dict(BASE),
 'points':len(E),
 'improvement_tolerance':TOL,
 'eff':{
   'S_center':r0['score_eff'],
   'gradient_y':ge.tolist(),
   'hessian_y':He.tolist(),
   'eigenvalues_y':ee.tolist(),
   'positive_definite':bool(np.all(ee>1e-8)),
   'newton_delta':de.tolist(),
   'newton_delta_used':trust_eff.tolist(),
   'S_newton':rn_eff['score_eff'],
   'S_at_k01_newton':rn_k01['score_eff'],
   'best_exact_S':best_eff['score_eff'],
   'best_improvement':imp_eff,
   'best_label':best_eff['label'],
   'recenter_required':bool(imp_eff>TOL)
 },
 'k01':{
   'S_center':r0['score_k01'],
   'gradient_y':gk.tolist(),
   'hessian_y':Hk.tolist(),
   'eigenvalues_y':ek.tolist(),
   'positive_definite':bool(np.all(ek>1e-8)),
   'newton_delta':dk.tolist(),
   'newton_delta_used':trust_k01.tolist(),
   'S_newton':rn_k01['score_k01'],
   'S_at_eff_newton':rn_eff['score_k01'],
   'best_exact_S':best_k01['score_k01'],
   'best_improvement':imp_k01,
   'best_label':best_k01['label'],
   'recenter_required':bool(imp_k01>TOL)
 },
 'warning':'Local numerical Hessian on frozen candidate objective; eff and k01 are separate objective variants; not posterior evidence or global model selection.'
}
out=Path('output/dense_rtk_7d_stationarity');out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('DENSE_RTK_STATIONARITY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('DENSE_RTK_STATIONARITY_COMPLETE',flush=True)
