#!/usr/bin/env python3
"""Stage 4B: exact local likelihood-basin recovery and Hessian construction.

This is deliberately local. It uses the exact CLASS + official Planck +
Pantheon + BOSS likelihood already validated in Stage 3, evaluates a symmetric
finite-difference stencil around the previously validated focused minimum, and
constructs gradients/Hessians for both BOSS growth mappings.

Outputs are proposal diagnostics, not global posteriors or Bayesian evidence.
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
import inference_core as L

MODEL=(sys.argv[2] if len(sys.argv)>2 else 'RTK').upper()
if MODEL not in ('RTK','LCDM'):
    raise SystemExit('model must be RTK or LCDM')
OUT=Path('output/basin')/MODEL.lower(); OUT.mkdir(parents=True,exist_ok=True)

if MODEL=='RTK':
    CENTER={'lam':1150.0,'h':0.684,'Ob':0.0475,'Om':0.26,'As':2.037e-9,'ns':0.963,'zre':6.0}
    COORDS=[
      ('loglam',math.log(CENTER['lam']),0.14),
      ('h',CENTER['h'],0.0015),
      ('Ob',CENTER['Ob'],0.0005),
      ('Om',CENTER['Om'],0.005),
      ('As',CENTER['As'],0.030e-9),
      ('ns',CENTER['ns'],0.0020),
      ('zre',CENTER['zre'],0.25),
    ]
    EXPECT={'eff':1060.4156870418112,'k01':1059.1663018827035}
else:
    CENTER={'lam':0.0,'h':0.678,'Ob':0.048,'Om':0.26,'As':2.1e-9,'ns':0.9675,'zre':8.0}
    COORDS=[
      ('h',CENTER['h'],0.0015),
      ('Ob',CENTER['Ob'],0.0005),
      ('Om',CENTER['Om'],0.005),
      ('As',CENTER['As'],0.030e-9),
      ('ns',CENTER['ns'],0.0020),
      ('zre',CENTER['zre'],0.25),
    ]
    EXPECT={'eff':1059.122613715511,'k01':1059.1242714438702}

N=len(COORDS)
EVALS={}
ROWS=[]


def cleanup(tag):
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
        if name=='loglam': p['lam']=math.exp(v)
        else:p[name]=v
    return p


def key(y): return tuple(float(f'{v:.8g}') for v in y)


def evaluate_y(y,label):
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    r=L.evaluate(MODEL,p)
    if not r.get('ok'):
        raise RuntimeError(f'likelihood failed at {label}: {r}')
    EVALS[k]=r
    row={'label':label,'model':MODEL}
    for i,(name,_,_) in enumerate(COORDS):row['y_'+name]=float(y[i])
    row.update({q:p[q] for q in ('lam','h','Ob','Om','As','ns','zre')})
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
        row[q]=r.get(q)
    ROWS.append(row)
    cleanup(r['tag'])
    return r


def score(r,mapping):return float(r['score'] if mapping=='eff' else r['score_k01'])

z=np.zeros(N)
r0=evaluate_y(z,'center')
for mapping in ('eff','k01'):
    diff=score(r0,mapping)-EXPECT[mapping]
    print('CENTER_REGRESSION',MODEL,mapping,score(r0,mapping),EXPECT[mapping],diff,flush=True)
    if abs(diff)>0.20:
        raise SystemExit(f'center regression failed for {MODEL} {mapping}: {diff}')

# Exact symmetric finite-difference design: 1 + 2N + 4*N*(N-1)/2 = 2N^2+1.
for i in range(N):
    for s in (-1.0,1.0):
        y=np.zeros(N);y[i]=s;evaluate_y(y,f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i+1,N):
        for si in (-1.0,1.0):
            for sj in (-1.0,1.0):
                y=np.zeros(N);y[i]=si;y[j]=sj
                evaluate_y(y,f'cross_{i}_{j}_{int(si):+d}_{int(sj):+d}')


def analyze(mapping):
    S0=score(r0,mapping); g=np.zeros(N); H=np.zeros((N,N))
    for i in range(N):
        yp=np.zeros(N);ym=np.zeros(N);yp[i]=1;ym[i]=-1
        Sp=score(EVALS[key(yp)],mapping);Sm=score(EVALS[key(ym)],mapping)
        g[i]=(Sp-Sm)/2.0
        H[i,i]=Sp-2*S0+Sm
    for i in range(N):
        for j in range(i+1,N):
            vals=[]
            for si,sj in ((1,1),(1,-1),(-1,1),(-1,-1)):
                y=np.zeros(N);y[i]=si;y[j]=sj
                vals.append(score(EVALS[key(y)],mapping))
            hij=(vals[0]-vals[1]-vals[2]+vals[3])/4.0
            H[i,j]=H[j,i]=hij
    eigval,eigvec=np.linalg.eigh(H)
    pd=bool(np.all(eigval>1e-8))
    cond=float(np.max(np.abs(eigval))/max(np.min(np.abs(eigval)),1e-15))
    pinv=np.linalg.pinv(H,rcond=1e-10)
    delta=-pinv@g
    trust=np.clip(delta,-2.0,2.0)
    pred=float(S0+g@trust+0.5*trust@H@trust)
    candidate=evaluate_y(trust,f'newton_{mapping}')
    actual=score(candidate,mapping)
    cov=None;corr=None;sig=None
    if pd:
        cov=2.0*np.linalg.inv(H)
        sig=np.sqrt(np.diag(cov))
        corr=cov/np.outer(sig,sig)
    return {
      'mapping':mapping,'S_center':S0,'expected_center':EXPECT[mapping],
      'gradient_y':g.tolist(),'hessian_y':H.tolist(),
      'eigenvalues_y':eigval.tolist(),'eigenvectors_y_columns':eigvec.tolist(),
      'positive_definite':pd,'condition_number_abs':cond,
      'newton_delta_y_unclipped':delta.tolist(),'trust_delta_y':trust.tolist(),
      'trust_was_clipped':bool(np.any(np.abs(delta)>2.0)),
      'quadratic_predicted_S_at_candidate':pred,'actual_S_at_candidate':actual,
      'candidate_params':y_to_params(trust),
      'improvement_actual':float(S0-actual),
      'covariance_y_if_pd':None if cov is None else cov.tolist(),
      'sigma_y_if_pd':None if sig is None else sig.tolist(),
      'correlation_y_if_pd':None if corr is None else corr.tolist(),
    }

analyses={m:analyze(m) for m in ('eff','k01')}

# Best exact point among the stencil + trust-region candidates.
best={}
for mapping in ('eff','k01'):
    kbest,rbest=min(EVALS.items(),key=lambda kv:score(kv[1],mapping))
    best[mapping]={
      'S':score(rbest,mapping),
      'params':{q:rbest.get(q) for q in ('lam','h','Ob','Om','As','ns','zre')},
      'components':{q:rbest.get(q) for q in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')}
    }

summary={
 'stage':'4B','status':'local_basin_diagnostic_not_global_posterior',
 'model':MODEL,'center':CENTER,
 'coordinates':[{'name':n,'center_coordinate':c,'step':s} for n,c,s in COORDS],
 'design_evaluations':len(EVALS),'exact_likelihood_calls':L.COUNTER,
 'center_scores':{'eff':score(r0,'eff'),'k01':score(r0,'k01')},
 'analysis':analyses,'best_exact':best,
}
(OUT/'basin_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')

fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'basin_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)

# Machine-readable Gaussian proposal only when curvature is positive definite.
proposal={'model':MODEL,'coordinates':[n for n,_,_ in COORDS],'mappings':{}}
for m,a in analyses.items():
    proposal['mappings'][m]={
      'positive_definite':a['positive_definite'],
      'center_params':CENTER,
      'candidate_params':a['candidate_params'],
      'covariance_y':a['covariance_y_if_pd'],
      'correlation_y':a['correlation_y_if_pd'],
    }
(OUT/'proposal.json').write_text(json.dumps(proposal,indent=2,sort_keys=True)+'\n')

print('BASIN_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4B_PASS',flush=True)
