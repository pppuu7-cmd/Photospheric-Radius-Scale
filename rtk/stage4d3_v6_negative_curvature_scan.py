#!/usr/bin/env python3
"""Exact shared eff/k01 scan along the most-negative v6 Hessian eigenvector.

Navigation diagnostic only.  The v6 7D Hessian has a small negative eigenvalue
and a passing scaled-gradient gate, so the informative next probe is the
negative-curvature direction rather than another coordinate poll.
"""
from pathlib import Path
import csv,json,math,sys
import numpy as np
import inference_core as L

CENTER={'lam':287930.95430552866,'h':0.6904668858782219,'Ob':0.046835996338062985,'Om':0.2530185206833107,'As':2.0836316905673827e-9,'ns':0.9644013704702473,'zre':7.218930610576525}
# eigvec of scale=.25 eff Hessian; k01 vector agrees to ~1e-6 componentwise.
V=np.array([0.999111401,-0.0268472531,0.0267048615,0.0173508437,0.000476707074,0.00519799363,-0.00376631844],float)
NAMES=['loglam','h','Ob','Om','As','ns','zre']
BASE=np.array([0.05,0.00035,0.00007,0.0007,4e-12,0.00035,0.07],float)
SCALE=.25
TS=[-16,-12,-8,-6,-4,-2,-1,0,1,2,4,6,8,12,16]
OUT=Path('output/stage4d3_v6_negative_curvature');OUT.mkdir(parents=True,exist_ok=True)
rows=[]
def p_of(t):
    dy=t*V*SCALE*BASE
    p=dict(CENTER);p['lam']=CENTER['lam']*math.exp(dy[0])
    for i,n in enumerate(NAMES[1:],1):p[n]=CENTER[n]+dy[i]
    return p
def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass
for t in TS:
    p=p_of(t);r=L.evaluate('RTK',p)
    if not r.get('ok'):raise SystemExit('evaluation failed t='+str(t))
    row={'t':t,**p,**{q:r.get(q) for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')}}
    rows.append(row);cleanup(r.get('tag'));print('V6_NEGCURV_POINT',json.dumps(row,sort_keys=True),flush=True)
be=min(rows,key=lambda x:x['score']);bk=min(rows,key=lambda x:x['score_k01'])
summary={'stage':'stage4d3-v6-negative-curvature-scan','scope':'exact_navigation_not_stationarity_or_global_fit','center':CENTER,'scale':SCALE,'base_steps':dict(zip(NAMES,BASE.tolist())),'eigenvector_y':V.tolist(),'t_values':TS,'exact_calls':int(L.COUNTER),'best_eff':be,'best_k01':bk,'center_eff':next(r['score'] for r in rows if r['t']==0),'center_k01':next(r['score_k01'] for r in rows if r['t']==0)}
summary['eff_improvement']=summary['center_eff']-be['score'];summary['k01_improvement']=summary['center_k01']-bk['score_k01']
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (OUT/'points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('V6_NEGCURV_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('V6_NEGCURV_COMPLETE',flush=True)
