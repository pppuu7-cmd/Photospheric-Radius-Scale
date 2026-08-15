#!/usr/bin/env python3
"""Exact conditional stationarity/Hessian check at fixed RTK lambda_D.

Usage:
  python3 stage4d0_fixed_lambda_stationarity.py PLANCK_DIR LAMBDA_D eff|k01 \
      h Ob Om As ns zre EXPECTED_S [STEP_SCALE]

The first PLANCK_DIR argument is retained because inference_core consumes the
same argv layout as the validated exact-likelihood runners.

This checks stationarity only in the six reoptimized cosmological coordinates
at fixed lambda_D.  It does not test the derivative along lambda_D and is not a
global profile, posterior, confidence construction, or evidence calculation.

STEP_SCALE rescales the validated Stage-4D0 finite-difference stencil.  The
default 1.0 preserves the original workflow behavior; explicit scales write to
separate output directories so 1, 1/2, 1/4 ... checks cannot overwrite each
other.
"""
from pathlib import Path
import csv,json,math,sys
import numpy as np
import inference_core as L

if len(sys.argv) not in (11,12):
    raise SystemExit(__doc__)
LAM=float(sys.argv[2]); MAPPING=sys.argv[3].lower()
if MAPPING not in ('eff','k01'): raise SystemExit('mapping must be eff or k01')
vals=list(map(float,sys.argv[4:10])); EXPECT=float(sys.argv[10])
STEP_SCALE=float(sys.argv[11]) if len(sys.argv)==12 else 1.0
if not math.isfinite(STEP_SCALE) or STEP_SCALE<=0:
    raise SystemExit('STEP_SCALE must be finite and > 0')
CENTER={'lam':LAM,**dict(zip(('h','Ob','Om','As','ns','zre'),vals))}
# Base steps equal the original 0.05 normalized independent poll used by Stage 4D1.
BASE_COORDS=[('h',CENTER['h'],0.00035),('Ob',CENTER['Ob'],0.00007),
             ('Om',CENTER['Om'],0.00070),('As',CENTER['As'],4.0e-12),
             ('ns',CENTER['ns'],0.00035),('zre',CENTER['zre'],0.070)]
COORDS=[(n,c,s*STEP_SCALE) for n,c,s in BASE_COORDS]
N=len(COORDS)
OUT=Path('output/stage4d0_fixed_lambda')/MAPPING/f'{LAM:.0f}'
if len(sys.argv)==12:
    scale_tag=(f'{STEP_SCALE:.8g}').replace('.','p').replace('-','m').replace('+','p')
    OUT=OUT/f'scale_{scale_tag}'
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

def y_to_params(y):
    p=dict(CENTER)
    for yi,(n,c,s) in zip(y,COORDS):p[n]=c+float(yi)*s
    return p

def key(y):return tuple(float(f'{float(v):.10g}') for v in y)
def score(r):return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def ev(y,label):
    y=np.asarray(y,float); k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y); r=L.evaluate('RTK',p)
    if not r.get('ok'):raise RuntimeError(f'{label}: {r}')
    rr=dict(r);rr['params']=p;rr['y']=y.tolist();EVALS[k]=rr
    row={'label':label,'lambda_D':LAM,'mapping':MAPPING,'step_scale':STEP_SCALE,'S':score(rr)}
    row.update(p)
    for i,(n,_,_) in enumerate(COORDS):row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=rr.get(q)
    ROWS.append(row);cleanup(rr.get('tag'))
    print('STENCIL_EVAL',label,score(rr),flush=True)
    return rr

z=np.zeros(N);r0=ev(z,'center');S0=score(r0)
if abs(S0-EXPECT)>0.03:
    raise SystemExit(f'center regression failed: exact={S0} expected={EXPECT}')

# 1 + 2N + 4*N*(N-1)/2 = 2N^2+1 = 73 points for N=6.
for i in range(N):
    for sgn in (-1.,1.):
        y=np.zeros(N);y[i]=sgn;ev(y,f'axis_{i}_{int(sgn):+d}')
for i in range(N):
    for j in range(i+1,N):
        for si in (-1.,1.):
            for sj in (-1.,1.):
                y=np.zeros(N);y[i]=si;y[j]=sj
                ev(y,f'cross_{i}_{j}_{int(si):+d}_{int(sj):+d}')

g=np.zeros(N);H=np.zeros((N,N))
for i in range(N):
    yp=np.zeros(N);ym=np.zeros(N);yp[i]=1;ym[i]=-1
    Sp=score(EVALS[key(yp)]);Sm=score(EVALS[key(ym)])
    g[i]=(Sp-Sm)/2.;H[i,i]=Sp-2*S0+Sm
for i in range(N):
    for j in range(i+1,N):
        vals=[]
        for si,sj in ((1,1),(1,-1),(-1,1),(-1,-1)):
            y=np.zeros(N);y[i]=si;y[j]=sj;vals.append(score(EVALS[key(y)]))
        H[i,j]=H[j,i]=(vals[0]-vals[1]-vals[2]+vals[3])/4.

eigval,eigvec=np.linalg.eigh(H);pd=bool(np.all(eigval>1e-8))
pinv=np.linalg.pinv(H,rcond=1e-10);delta=-pinv@g
trust=np.clip(delta,-1.,1.)
rnew=ev(trust,'newton_trust');Snew=score(rnew)
valid=list(EVALS.values());best=min(valid,key=score);Sbest=score(best)
max_grad=float(np.max(np.abs(g)))
center_is_best_stencil=bool(Sbest>=S0-0.005)
summary={
 'stage':'4D0-fixed-lambda-stationarity','scope':'conditional_six_parameter_local_check_at_fixed_lambda',
 'lambda_D':LAM,'mapping':MAPPING,'step_scale':STEP_SCALE,
 'center':CENTER,'S_center':S0,'expected_S':EXPECT,
 'coordinates':[{'name':n,'base_step':bs,'step':s} for (n,_,bs),(_,_,s) in zip(BASE_COORDS,COORDS)],
 'design_points_before_newton':2*N*N+1,'exact_likelihood_calls':int(L.COUNTER),
 'gradient_y':g.tolist(),'max_abs_gradient_y':max_grad,'hessian_y':H.tolist(),
 'eigenvalues_y':eigval.tolist(),'positive_definite':pd,
 'newton_delta_y_unclipped':delta.tolist(),'newton_delta_y_used':trust.tolist(),
 'S_newton':Snew,'newton_improvement':S0-Snew,
 'best_exact_S_including_newton':Sbest,'best_exact_params':best['params'],
 'best_improvement_from_center':S0-Sbest,'center_is_best_within_0p005':center_is_best_stencil,
 'warning':'This is conditional on fixed lambda_D and does not test the lambda direction or establish a global profile/posterior.'
}
(OUT/'stationarity_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'stationarity_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('STAGE4D0_FIXED_LAMBDA_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D0_FIXED_LAMBDA_PASS',flush=True)
