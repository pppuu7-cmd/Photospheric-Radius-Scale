#!/usr/bin/env python3
"""Exact 7-D stationarity/Hessian check including log(lambda_D).

Usage:
  python3 stage4d3_joint_stationarity.py PLANCK_DIR eff|k01 LAMBDA_D \
      h Ob Om As ns zre EXPECTED_S [STEP_SCALE]

The design is the full central axis/cross stencil in seven normalized
coordinates.  The lambda coordinate is logarithmic, preserving lambda_D>0.
This proves at most a local numerical minimum of the current likelihood
harness; it is not a posterior, significance, evidence, or observational proof.
"""
from pathlib import Path
import csv,json,math,os,sys
import numpy as np
import inference_core as L

if len(sys.argv) not in (11,12):
    raise SystemExit(__doc__)
MAPPING=sys.argv[2].lower(); LAM=float(sys.argv[3])
if MAPPING not in ('eff','k01') or not (LAM>0 and math.isfinite(LAM)):
    raise SystemExit('invalid mapping or lambda_D')
vals=list(map(float,sys.argv[4:10])); EXPECT=float(sys.argv[10])
STEP_SCALE=float(sys.argv[11]) if len(sys.argv)==12 else 1.0
if not math.isfinite(STEP_SCALE) or STEP_SCALE<=0:
    raise SystemExit('STEP_SCALE must be finite and > 0')
GRAD_TOL=float(os.environ.get('RTK_STATIONARITY_GRAD_TOL','0.03'))
IMPROVE_TOL=float(os.environ.get('RTK_STATIONARITY_IMPROVEMENT_TOL','0.005'))
if not (math.isfinite(GRAD_TOL) and GRAD_TOL>0):
    raise SystemExit('RTK_STATIONARITY_GRAD_TOL must be finite and > 0')
if not (math.isfinite(IMPROVE_TOL) and IMPROVE_TOL>=0):
    raise SystemExit('RTK_STATIONARITY_IMPROVEMENT_TOL must be finite and >= 0')
CENTER={'lam':LAM,**dict(zip(('h','Ob','Om','As','ns','zre'),vals))}
# Base finite-difference scales. loglam=0.05 is about a 5% multiplicative step.
BASE=[('loglam',0.0,0.05),
      ('h',CENTER['h'],0.00035),('Ob',CENTER['Ob'],0.00007),
      ('Om',CENTER['Om'],0.00070),('As',CENTER['As'],4.0e-12),
      ('ns',CENTER['ns'],0.00035),('zre',CENTER['zre'],0.070)]
N=len(BASE)
scale_tag=(f'{STEP_SCALE:.8g}').replace('.','p').replace('-','m').replace('+','p')
OUT=Path('output/stage4d3_joint_stationarity')/MAPPING/f'{LAM:.0f}'/f'scale_{scale_tag}'
OUT.mkdir(parents=True,exist_ok=True)
EVALS={}; ROWS=[]; RETRIES=0

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def y_to_params(y):
    y=np.asarray(y,float)
    p=dict(CENTER)
    p['lam']=LAM*math.exp(float(y[0])*BASE[0][2]*STEP_SCALE)
    for yi,(n,c,s) in zip(y[1:],BASE[1:]):
        p[n]=c+float(yi)*s*STEP_SCALE
    return p

def key(y):return tuple(float(v) for v in np.asarray(y,float))
def score(r):return float(r['score'] if MAPPING=='eff' else r['score_k01'])
def is_timeout(r):return r.get('error')=='CLASS_TIMEOUT' or r.get('reason')=='CLASS_TIMEOUT' or 'CLASS_TIMEOUT' in str(r.get('reason',''))

def ev(y,label):
    global RETRIES
    y=np.asarray(y,float); k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y); r=L.evaluate('RTK',p)
    if not r.get('ok') and is_timeout(r):
        RETRIES+=1; cleanup(r.get('tag'))
        try:
            ikey=('RTK',)+tuple(float(p[q]) for q in ['lam','h','Ob','Om','As','ns','zre'])
            L.CACHE.pop(ikey,None)
        except Exception: pass
        r=L.evaluate('RTK',p)
    if not r.get('ok'):raise RuntimeError(f'{label}: {r}')
    rr=dict(r);rr['params']=p;rr['y']=y.tolist();EVALS[k]=rr
    row={'label':label,'mapping':MAPPING,'step_scale':STEP_SCALE,'S':score(rr)}
    row.update(p)
    for i,(n,_,_) in enumerate(BASE):row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=rr.get(q)
    ROWS.append(row);cleanup(rr.get('tag'))
    print('JOINT_STENCIL_EVAL',label,score(rr),p['lam'],flush=True)
    return rr

z=np.zeros(N);r0=ev(z,'center');S0=score(r0)
if abs(S0-EXPECT)>0.03:
    raise SystemExit(f'center regression failed: exact={S0} expected={EXPECT}')
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
    yp=np.zeros(N);ym=np.zeros(N);yp[i]=1.;ym[i]=-1.
    Sp=score(EVALS[key(yp)]);Sm=score(EVALS[key(ym)])
    g[i]=(Sp-Sm)/2.;H[i,i]=Sp-2*S0+Sm
for i in range(N):
    for j in range(i+1,N):
        vals=[]
        for si,sj in ((1,1),(1,-1),(-1,1),(-1,-1)):
            y=np.zeros(N);y[i]=si;y[j]=sj;vals.append(score(EVALS[key(y)]))
        H[i,j]=H[j,i]=(vals[0]-vals[1]-vals[2]+vals[3])/4.

eigval=np.linalg.eigvalsh(H);pd=bool(np.all(eigval>1e-8))
gbase=g/STEP_SCALE; Hbase=H/(STEP_SCALE*STEP_SCALE)
eigbase=np.linalg.eigvalsh(Hbase)
delta=-np.linalg.pinv(H,rcond=1e-10)@g
trust=np.clip(delta,-1.,1.)
rnew=ev(trust,'newton_trust');Snew=score(rnew)
best=min(EVALS.values(),key=score);Sbest=score(best)
best_improvement=S0-Sbest
newton_improvement=S0-Snew
max_grad_base=float(np.max(np.abs(gbase)))
gates={
 'positive_definite_hessian':pd,
 'gradient_within_tolerance':bool(max_grad_base<=GRAD_TOL),
 'no_exact_improvement_beyond_tolerance':bool(best_improvement<=IMPROVE_TOL),
 'correlated_newton_not_improving_beyond_tolerance':bool(newton_improvement<=IMPROVE_TOL),
}
stationarity_pass=bool(all(gates.values()))
summary={
 'stage':'4D3-seven-dimensional-stationarity','scope':'local_exact_hessian_including_log_lambda',
 'mapping':MAPPING,'lambda_D':LAM,'step_scale':STEP_SCALE,'center':CENTER,
 'S_center':S0,'expected_S':EXPECT,'design_points_before_newton':2*N*N+1,
 'exact_likelihood_calls':int(L.COUNTER),
 'base_coordinates':[{'name':n,'base_step':s} for n,_,s in BASE],
 'gradient_y':g.tolist(),'gradient_base_scaled':gbase.tolist(),
 'max_abs_gradient_y':float(np.max(np.abs(g))),
 'max_abs_gradient_base_scaled':max_grad_base,
 'gradient_tolerance_base_scaled':GRAD_TOL,
 'hessian_y':H.tolist(),'hessian_base_scaled':Hbase.tolist(),
 'eigenvalues_y':eigval.tolist(),'eigenvalues_base_scaled':eigbase.tolist(),
 'positive_definite':pd,
 'newton_delta_y_unclipped':delta.tolist(),'newton_delta_y_used':trust.tolist(),
 'S_newton':Snew,'newton_improvement':newton_improvement,
 'best_exact_S_including_newton':Sbest,'best_exact_params':best['params'],
 'best_improvement_from_center':best_improvement,
 'improvement_tolerance':IMPROVE_TOL,
 'center_is_best_within_0p005':bool(Sbest>=S0-0.005),
 'acceptance_gates':gates,
 'stationarity_pass':stationarity_pass,
 'memoization_key':'exact_float_normalized_coordinates','timeout_retries':RETRIES,
 'warning':'Local numerical Hessian only; not a global statistical or observational proof.'
}
(OUT/'joint_stationarity_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'joint_stationarity_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('STAGE4D3_JOINT_STATIONARITY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D3_JOINT_STATIONARITY_'+('PASS' if stationarity_pass else 'FAIL'),flush=True)
