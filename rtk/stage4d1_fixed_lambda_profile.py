#!/usr/bin/env python3
"""Stage 4D1: exact fixed-lambda_D local profile for RTK.

At one declared lambda_D this script reoptimizes the six remaining cosmological
parameters with the same exact CLASS + Planck + Pantheon + BOSS objective used
in Stage 4C.  It uses artifact-derived anchors only to initialize a local box;
the resulting point is a fixed-lambda local profile candidate, not a global
profile likelihood and not a posterior sample.

Usage:
  python3 stage4d1_fixed_lambda_profile.py PLANCK_DIR LAMBDA_D eff|k01
"""
from pathlib import Path
import csv, json, math, sys
import numpy as np
from scipy.optimize import minimize
import inference_core as L

if len(sys.argv) != 4:
    raise SystemExit(__doc__)
LAM=float(sys.argv[2]); MAPPING=sys.argv[3].lower()
if not (LAM>0 and math.isfinite(LAM)): raise SystemExit('lambda_D must be finite and positive')
if MAPPING not in ('eff','k01'): raise SystemExit('mapping must be eff or k01')

# Artifact-derived anchors from the exact Stage 4C basin recovery.
ANCHORS={
 'eff':[
  (1877.1636529486852, {'h':0.6875328470069375,'Ob':0.047139435833781454,'Om':0.2563454835564767,'As':2.0534202049956847e-9,'ns':0.9623987030279104,'zre':6.365733981713082}),
  (3253.599566504292,  {'h':0.6875880125513063,'Ob':0.04713328630443649,'Om':0.2563325481125729,'As':2.0544278930991403e-9,'ns':0.9623721530719445,'zre':6.3941396132027775}),
  (1.0e8,                {'h':0.6889847582522818,'Ob':0.047027380867605724,'Om':0.2549024293574165,'As':2.0571387558194685e-9,'ns':0.9629625837971857,'zre':6.476774772356462}),
 ],
 'k01':[
  (1877.1636529486852, {'h':0.6875764732320122,'Ob':0.04715130866468585,'Om':0.25628676475282963,'As':2.0533303725095226e-9,'ns':0.9624479917488239,'zre':6.349605708096564}),
  (7569.7351619466235, {'h':0.6876214603799424,'Ob':0.04712079421089344,'Om':0.25628644034914994,'As':2.0526443693319543e-9,'ns':0.9627241793811957,'zre':6.355220906256776}),
  (1.0e8,               {'h':0.689009022393018,'Ob':0.04702645348629918,'Om':0.25483311550468146,'As':2.058494763207974e-9,'ns':0.963116623172502,'zre':6.517401124751232}),
 ]
}

def interp_center(lam):
    aa=ANCHORS[MAPPING]
    if lam<=aa[0][0]: return dict(aa[0][1])
    if lam>=aa[-1][0]: return dict(aa[-1][1])
    x=math.log(lam)
    for (l0,p0),(l1,p1) in zip(aa[:-1],aa[1:]):
        if l0<=lam<=l1:
            t=(x-math.log(l0))/(math.log(l1)-math.log(l0))
            return {k:(1-t)*p0[k]+t*p1[k] for k in p0}
    raise RuntimeError('anchor interpolation failure')

C=interp_center(LAM); CENTER={'lam':LAM,**C}
# Local half-widths are deliberately wide enough to absorb interpolation error.
COORDS=[('h',CENTER['h'],0.0070),('Ob',CENTER['Ob'],0.0014),
        ('Om',CENTER['Om'],0.0140),('As',CENTER['As'],8.0e-11),
        ('ns',CENTER['ns'],0.0070),('zre',CENTER['zre'],1.4)]
N=len(COORDS)
label=(f'{LAM:.0f}' if LAM<1e7 else f'{LAM:.0e}').replace('+','')
OUT=Path('output/stage4d1')/MAPPING/label
OUT.mkdir(parents=True,exist_ok=True)
EVALS={};ROWS=[];FAILED=0

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
    for yi,(n,c,w) in zip(y,COORDS): p[n]=c+float(yi)*w
    return p

def key(y): return tuple(float(f'{float(v):.10g}') for v in y)
def target(r): return float(r['score'] if MAPPING=='eff' else r['score_k01'])

def ev(y,tag='opt'):
    global FAILED
    y=np.asarray(y,float)
    if np.any(~np.isfinite(y)) or np.any(y<-1.0000001) or np.any(y>1.0000001):
        return {'ok':False,'penalty':1e12,'reason':'outside_box'}
    k=key(y)
    if k in EVALS:return EVALS[k]
    p=y_to_params(y)
    try:r=L.evaluate('RTK',p)
    except Exception as e:r={'ok':False,'reason':repr(e)}
    if not r.get('ok'):
        FAILED+=1; rr={'ok':False,'penalty':1e9+FAILED,'reason':r.get('reason',str(r)),'params':p,'y':y.tolist()};EVALS[k]=rr
        print('EVAL_FAIL',LAM,MAPPING,tag,rr['reason'],flush=True);return rr
    rr=dict(r);rr['params']=p;rr['y']=y.tolist();EVALS[k]=rr
    row={'label':tag,'lambda_D':LAM,'mapping':MAPPING}
    row.update(p)
    for i,(n,_,_) in enumerate(COORDS):row['y_'+n]=float(y[i])
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=r.get(q)
    ROWS.append(row);cleanup(r.get('tag'))
    print('EVAL',LAM,MAPPING,len(EVALS),target(r),p,flush=True);return rr

def obj(y):
    r=ev(y,'powell');return target(r) if r.get('ok') else float(r['penalty'])

z=np.zeros(N);r0=ev(z,'center')
if not r0.get('ok'): raise SystemExit('center failed')
bounds=[(-1.,1.)]*N
# Multiple deterministic starts: center plus two weakly correlated shifts.
starts=[z,np.array([0.12,-0.08,-0.12,0.08,0.04,0.08]),np.array([-0.10,0.08,0.10,-0.06,-0.04,-0.06])]
opts=[]
for idx,start in enumerate(starts):
    res=minimize(obj,start,method='Powell',bounds=bounds,
                 options={'xtol':0.012,'ftol':0.002,'maxfev':135,'maxiter':13,'disp':True})
    opts.append({'start':idx,'success':bool(res.success),'fun':float(res.fun),'x':np.asarray(res.x).tolist(),'nfev':int(res.nfev),'nit':int(res.nit)})
    ev(np.clip(res.x,-1,1),f'result_{idx}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target);by=np.asarray(best['y']);before=target(best)
poll=0.05
for i in range(N):
    for s in (-1.,1.):
        y=by.copy();y[i]=np.clip(y[i]+s*poll,-1,1)
        if np.allclose(y,by,atol=1e-14,rtol=0):continue
        ev(y,f'poll_{i}_{int(s):+d}')
valid=[r for r in EVALS.values() if r.get('ok')]
best=min(valid,key=target);after=target(best)
boundary=[COORDS[i][0] for i,v in enumerate(best['y']) if abs(v)>0.96]
status='fixed_lambda_local_profile_candidate' if not boundary else 'fixed_lambda_boundary_hit'
summary={
 'stage':'4D1-fixed-lambda-profile','status':status,
 'scope':'fixed_lambda_local_profile_not_global_posterior_or_global_profile',
 'lambda_D':LAM,'mapping':MAPPING,'initial_center':CENTER,'center_S':target(r0),
 'best_S':target(best),'best_params':best['params'],
 'best_components':{q:best.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
 'boundary_axes':boundary,'poll_improvement':before-after,
 'exact_likelihood_calls':int(L.COUNTER),'failed_points':FAILED,'optimizer_runs':opts,
 'coordinates':[{'name':n,'center':c,'halfwidth':w} for n,c,w in COORDS],
 'warning':'Each point is a locally optimized fixed-lambda profile candidate. The assembled curve is not a global profile until boundary/stationarity and multi-start coverage are checked.'
}
(OUT/'profile_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
fields=[]
for r in ROWS:
    for k in r:
        if k not in fields:fields.append(k)
with (OUT/'profile_trace.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(ROWS)
print('STAGE4D1_PROFILE_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D1_PROFILE_PASS',flush=True)
