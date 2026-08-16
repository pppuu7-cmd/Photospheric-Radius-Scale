#!/usr/bin/env python3
"""Exact seven-dimensional stationarity/Hessian check including log(lambda_D).

Usage:
  python3 stage4d3_7d_stationarity.py PLANCK_DIR eff|k01 lambda_D h Ob Om As ns zre EXPECTED_S [STEP_SCALE]

The first coordinate is q=ln(lambda/lambda0), so positivity is exact.  The
remaining six coordinates use the validated Stage-4D0 physical finite-
difference steps.  The full quadratic design has 2*N^2+1 = 99 points for N=7,
followed by one exact trust-clipped Newton point.
"""
from pathlib import Path
import csv,json,math,sys
import numpy as np
import inference_core as L

if len(sys.argv) not in (12,13): raise SystemExit(__doc__)
MAPPING=sys.argv[2].lower(); LAM0=float(sys.argv[3])
if MAPPING not in ('eff','k01') or not (LAM0>0 and math.isfinite(LAM0)):
    raise SystemExit('invalid mapping/lambda')
vals=list(map(float,sys.argv[4:10])); EXPECT=float(sys.argv[10]); SCALE=float(sys.argv[11]) if len(sys.argv)==12 else float(sys.argv[12])
# Compatibility: workflow always supplies explicit scale; if called without it, argv[11] is EXPECTED_S and default below is not reachable.
if len(sys.argv)==12:
    # Correct positional interpretation for PLANCK,mapping,lambda,h,Ob,Om,As,ns,zre,EXPECTED,STEP_SCALE
    EXPECT=float(sys.argv[10]); SCALE=float(sys.argv[11])
if not math.isfinite(SCALE) or SCALE<=0: raise SystemExit('STEP_SCALE must be >0')
CENTER={'lam':LAM0,**dict(zip(('h','Ob','Om','As','ns','zre'),vals))}
BASE=[('loglam',0.0,0.012),('h',CENTER['h'],0.00035),('Ob',CENTER['Ob'],0.00007),
      ('Om',CENTER['Om'],0.00070),('As',CENTER['As'],4.0e-12),
      ('ns',CENTER['ns'],0.00035),('zre',CENTER['zre'],0.070)]
COORDS=[(n,c,s*SCALE) for n,c,s in BASE]; N=len(COORDS)
OUT=Path('output/stage4d3_7d_stationarity')/MAPPING
OUT=OUT/('scale_'+(f'{SCALE:.8g}').replace('.','p').replace('-','m'))
OUT.mkdir(parents=True,exist_ok=True)
EVALS={}; ROWS=[]

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def params(y):
    y=np.asarray(y,float); p=dict(CENTER)
    p['lam']=LAM0*math.exp(float(y[0])*COORDS[0][2])
    for yi,(n,c,s) in zip(y[1:],COORDS[1:]): p[n]=c+float(yi)*s
    return p

def key(y): return tuple(float(v) for v in np.asarray(y,float))
def score(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def ev(y,label):
    y=np.asarray(y,float); k=key(y)
    if k in EVALS:return EVALS[k]
    p=params(y); r=L.evaluate('RTK',p)
    if not r.get('ok'): raise RuntimeError(f'{label}: {r}')
    rr=dict(r); rr['params']=p; rr['y']=y.tolist(); EVALS[k]=rr
    row={'label':label,'mapping':MAPPING,'step_scale':SCALE,'S':score(rr),**p}
    for i,(n,_,_) in enumerate(COORDS): row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'): row[q]=rr.get(q)
    ROWS.append(row); cleanup(rr.get('tag')); print('STENCIL7_EVAL',label,score(rr),flush=True)
    return rr

z=np.zeros(N); r0=ev(z,'center'); S0=score(r0)
if abs(S0-EXPECT)>0.03: raise SystemExit(f'center regression failed exact={S0} expected={EXPECT}')
for i in range(N):
    for sg in (-1.,1.):
        y=np.zeros(N); y[i]=sg; ev(y,f'axis_{i}_{int(sg):+d}')
for i in range(N):
    for j in range(i+1,N):
        for si in (-1.,1.):
            for sj in (-1.,1.):
                y=np.zeros(N); y[i]=si; y[j]=sj; ev(y,f'cross_{i}_{j}_{int(si):+d}_{int(sj):+d}')
g=np.zeros(N); H=np.zeros((N,N))
for i in range(N):
    yp=np.zeros(N); ym=np.zeros(N); yp[i]=1; ym[i]=-1
    Sp=score(EVALS[key(yp)]); Sm=score(EVALS[key(ym)])
    g[i]=(Sp-Sm)/2.; H[i,i]=Sp-2*S0+Sm
for i in range(N):
    for j in range(i+1,N):
        v=[]
        for si,sj in ((1,1),(1,-1),(-1,1),(-1,-1)):
            y=np.zeros(N); y[i]=si; y[j]=sj; v.append(score(EVALS[key(y)]))
        H[i,j]=H[j,i]=(v[0]-v[1]-v[2]+v[3])/4.
eigval,eigvec=np.linalg.eigh(H); pd=bool(np.all(eigval>1e-8))
delta=-np.linalg.pinv(H,rcond=1e-10)@g; trust=np.clip(delta,-1.,1.)
rnew=ev(trust,'newton_trust'); Snew=score(rnew)
best=min(EVALS.values(),key=score); Sbest=score(best)
summary={'stage':'4D3-seven-dimensional-stationarity','scope':'local_7d_check_including_log_lambda',
 'mapping':MAPPING,'lambda_D':LAM0,'step_scale':SCALE,'center':CENTER,'S_center':S0,'expected_S':EXPECT,
 'coordinates':[{'name':n,'base_step':bs,'step':s} for (n,_,bs),(_,_,s) in zip(BASE,COORDS)],
 'design_points_before_newton':2*N*N+1,'exact_likelihood_calls':int(L.COUNTER),
 'gradient_y':g.tolist(),'max_abs_gradient_y':float(np.max(np.abs(g))),
 'hessian_y':H.tolist(),'eigenvalues_y':eigval.tolist(),'positive_definite':pd,
 'newton_delta_y_unclipped':delta.tolist(),'newton_delta_y_used':trust.tolist(),
 'S_newton':Snew,'newton_improvement':S0-Snew,'best_exact_S_including_newton':Sbest,
 'best_exact_params':best['params'],'best_improvement_from_center':S0-Sbest,
 'center_is_best_within_0p005':bool(Sbest>=S0-0.005),
 'warning':'Local numerical 7D Hessian only; not a global posterior/evidence result.'}
(OUT/'stationarity_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields: fields.append(k)
with (OUT/'stationarity_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(ROWS)
print('STAGE4D3_7D_STATIONARITY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D3_7D_STATIONARITY_PASS',flush=True)
