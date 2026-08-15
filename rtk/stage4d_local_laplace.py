#!/usr/bin/env python3
"""Stage 4D0: exact local stationarity + Laplace diagnostic around Stage 4C.

This script is intentionally a gate before posterior sampling.  It takes one
Stage 4C summary, refuses boundary-hit/non-stable inputs, evaluates a small
symmetric exact CLASS+Planck+Pantheon+BOSS stencil around the Stage 4C best
point, and measures gradient, Hessian, curvature and any exact improvement.

It does NOT produce a global posterior, confidence interval, exclusion
significance, or Bayesian evidence.  A Gaussian/Laplace covariance is emitted
only if the local Hessian is positive definite.

Usage:
  python3 stage4d_local_laplace.py PLANCK_DIR STAGE4C_SUMMARY.json
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
import inference_core as L

if len(sys.argv) != 3:
    raise SystemExit(__doc__)
summary_path=Path(sys.argv[2])
s4=json.loads(summary_path.read_text())
if s4.get('stage')!='4C': raise SystemExit('input is not Stage 4C')
MODEL=str(s4.get('model','')).upper(); MAPPING=str(s4.get('mapping','')).lower()
if MODEL not in ('RTK','LCDM') or MAPPING not in ('eff','k01'):
    raise SystemExit('invalid model/mapping')
if s4.get('status')!='local_minimum_candidate' or (s4.get('boundary_axes') or []):
    raise SystemExit('Stage 4C is not a boundary-free local minimum candidate; expand/refine Stage 4C first')

CENTER=dict(s4['best_params'])
S4=float(s4['best_S'])
# Use a small but not machine-noise-scale fraction of the Stage 4C trust box.
# Coordinates are finite-difference units y, not priors and not posterior sigma.
FRAC=0.12
COORDS=[]
for c in s4['coordinates']:
    name=c['name']; hw=float(c['halfwidth'])
    if name=='loglam': center_coord=math.log(float(CENTER['lam']))
    else: center_coord=float(CENTER[name])
    COORDS.append((name,center_coord,FRAC*hw))
N=len(COORDS)
OUT=Path('output/stage4d0')/MODEL.lower()/MAPPING
OUT.mkdir(parents=True,exist_ok=True)
EVALS={}; ROWS=[]; FAILED=0


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
    for yi,(name,c,step) in zip(y,COORDS):
        v=c+float(yi)*step
        if name=='loglam':p['lam']=math.exp(v)
        else:p[name]=v
    return p


def key(y):return tuple(float(f'{float(v):.10g}') for v in y)

def target(r):return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def evaluate_y(y,label):
    global FAILED
    y=np.asarray(y,dtype=float); k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    try:r=L.evaluate(MODEL,p)
    except Exception as e:r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        FAILED+=1
        rr={'ok':False,'reason':r.get('reason',str(r)),'params':p,'y':y.tolist()}
        EVALS[k]=rr
        print('EVAL_FAIL',MODEL,MAPPING,label,rr['reason'],flush=True)
        return rr
    rr=dict(r);rr['params']=p;rr['y']=y.tolist();EVALS[k]=rr
    row={'label':label,'model':MODEL,'mapping':MAPPING}
    for i,(name,_,_) in enumerate(COORDS):row['y_'+name]=float(y[i])
    row.update({q:p.get(q) for q in ('lam','h','Ob','Om','As','ns','zre')})
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
        row[q]=r.get(q)
    ROWS.append(row);cleanup(r.get('tag'))
    print('EVAL',MODEL,MAPPING,len(EVALS),target(r),p,flush=True)
    return rr

z=np.zeros(N); r0=evaluate_y(z,'center')
if not r0.get('ok'):raise SystemExit('Stage 4D0 center failed')
S0=target(r0); center_regression=S0-S4
if abs(center_regression)>0.25:
    raise SystemExit(f'Stage 4C center regression failed: {center_regression}')

# Symmetric 2N^2+1 exact design.
for i in range(N):
    for s in (-1.,1.):
        y=np.zeros(N);y[i]=s;evaluate_y(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for si in (-1.,1.):
            for sj in (-1.,1.):
                y=np.zeros(N);y[i]=si;y[j]=sj
                evaluate_y(y,f'cross_{i}_{j}_{int(si):+d}_{int(sj):+d}')

valid=[r for r in EVALS.values() if r.get('ok')]
if len(valid)!=(2*N*N+1):
    raise SystemExit(f'incomplete exact stencil: {len(valid)} / {2*N*N+1}')
best=min(valid,key=target); Sbest=target(best); improvement=S0-Sbest

g=np.zeros(N);H=np.zeros((N,N))
for i in range(N):
    yp=np.zeros(N);ym=np.zeros(N);yp[i]=1;ym[i]=-1
    Sp=target(EVALS[key(yp)]);Sm=target(EVALS[key(ym)])
    g[i]=(Sp-Sm)/2.;H[i,i]=Sp-2*S0+Sm
for i in range(N):
    for j in range(i+1,N):
        vals=[]
        for si,sj in ((1,1),(1,-1),(-1,1),(-1,-1)):
            y=np.zeros(N);y[i]=si;y[j]=sj;vals.append(target(EVALS[key(y)]))
        H[i,j]=H[j,i]=(vals[0]-vals[1]-vals[2]+vals[3])/4.

eigval,eigvec=np.linalg.eigh(H)
pd=bool(np.all(eigval>1e-8))
cond=float(np.max(np.abs(eigval))/max(np.min(np.abs(eigval)),1e-15))
gnorm=float(np.linalg.norm(g))
cov=corr=sig=None
if pd:
    cov=2.*np.linalg.inv(H)
    sig=np.sqrt(np.diag(cov));corr=cov/np.outer(sig,sig)

# Predeclared exact stationarity tolerance in objective units.
STATIONARY_TOL=0.03
status='laplace_ready_local_only' if (improvement<=STATIONARY_TOL and pd) else 'stage4c_needs_refinement'

result={
 'stage':'4D0','status':status,
 'scope':'exact_local_stationarity_and_laplace_diagnostic_not_global_posterior',
 'model':MODEL,'mapping':MAPPING,'stage4c_source':str(summary_path),
 'stage4c_best_S':S4,'center_regression_S':S0,'center_regression_delta':center_regression,
 'finite_difference_fraction_of_stage4c_halfwidth':FRAC,
 'coordinates':[{'name':n,'center_coordinate':c,'step':s} for n,c,s in COORDS],
 'exact_likelihood_calls':int(L.COUNTER),'failed_points':FAILED,
 'stencil_size':2*N*N+1,
 'best_stencil_S':Sbest,'best_stencil_params':best['params'],
 'improvement_over_stage4c_center':float(improvement),
 'stationarity_tolerance':STATIONARY_TOL,
 'gradient_y':g.tolist(),'gradient_norm_y':gnorm,
 'hessian_y':H.tolist(),'eigenvalues_y':eigval.tolist(),
 'eigenvectors_y_columns':eigvec.tolist(),'positive_definite':pd,
 'condition_number_abs':cond,
 'covariance_y_if_pd':None if cov is None else cov.tolist(),
 'sigma_y_if_pd':None if sig is None else sig.tolist(),
 'correlation_y_if_pd':None if corr is None else corr.tolist(),
 'warning':'Any covariance is a local Laplace approximation only. Do not quote it as a converged posterior interval.'
}
(OUT/'stage4d0_summary.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'stage4d0_stencil.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('STAGE4D0_RESULT',json.dumps(result,sort_keys=True),flush=True)
print('STAGE4D0_PASS' if status=='laplace_ready_local_only' else 'STAGE4D0_REFINE_STAGE4C',flush=True)
