#!/usr/bin/env python3
"""Independent exact correlated-direction acceptance test around a 7D RTK center.

Usage:
  python3 stage4d3_correlated_acceptance.py PLANCK_DIR LAMBDA h Ob Om As ns zre S_EFF S_K01

The test evaluates multiple deterministic non-axis directions in normalized
(log lambda,h,Ob,Om,As,ns,zre) coordinates. Both eff and k01 objectives are
recorded from every exact CLASS+Planck+Pantheon+BOSS evaluation.
"""
from pathlib import Path
import csv,json,math,os,sys
import numpy as np
import inference_core as L

if len(sys.argv)!=11: raise SystemExit(__doc__)
LAM=float(sys.argv[2]); vals=list(map(float,sys.argv[3:9])); SE=float(sys.argv[9]); SK=float(sys.argv[10])
if not (LAM>0 and math.isfinite(LAM)): raise SystemExit('invalid lambda')
CENTER={'lam':LAM,**dict(zip(('h','Ob','Om','As','ns','zre'),vals))}
TOL=float(os.environ.get('RTK_CORRELATED_IMPROVEMENT_TOL','0.005'))
if not (math.isfinite(TOL) and TOL>=0): raise SystemExit('invalid tolerance')
BASE=np.array([0.05,0.00035,0.00007,0.00070,4e-12,0.00035,0.070],float)
N=7
raw=np.array([
 [ 1, 1, 1, 1, 1, 1, 1],
 [ 1, 1, 1,-1,-1,-1, 1],
 [ 1, 1,-1, 1,-1, 1,-1],
 [ 1,-1, 1, 1,-1,-1,-1],
 [ 1,-1,-1,-1, 1, 1,-1],
 [-1,1,-1,-1, 1,-1, 1],
 [-1,-1,1,-1,-1, 1, 1],
 [ 1,-.08,.05,-.04,.03,.06,-.05],
],float)
dirs=raw/np.linalg.norm(raw,axis=1)[:,None]
alphas=(-1.0,-0.5,-0.25,0.25,0.5,1.0)
OUT=Path('output/stage4d3_correlated_acceptance');OUT.mkdir(parents=True,exist_ok=True)
rows=[]; RETRIES=0

def params(y):
    y=np.asarray(y,float);p=dict(CENTER)
    p['lam']=LAM*math.exp(y[0]*BASE[0])
    for yi,n,s in zip(y[1:],('h','Ob','Om','As','ns','zre'),BASE[1:]):p[n]=CENTER[n]+yi*s
    return p

def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def is_timeout(r):return r.get('error')=='CLASS_TIMEOUT' or r.get('reason')=='CLASS_TIMEOUT' or 'CLASS_TIMEOUT' in str(r.get('reason',''))

def evaluate(y,label,di=None,a=0.0):
    global RETRIES
    p=params(y);r=L.evaluate('RTK',p)
    if not r.get('ok') and is_timeout(r):
        RETRIES+=1; cleanup(r.get('tag'))
        try:
            ikey=('RTK',)+tuple(float(p[q]) for q in ['lam','h','Ob','Om','As','ns','zre'])
            L.CACHE.pop(ikey,None)
        except Exception:pass
        r=L.evaluate('RTK',p)
    if not r.get('ok'):raise RuntimeError(f'{label}: {r}')
    row={'label':label,'direction':di,'alpha':a,**p}
    for q in ('score','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):row[q]=r.get(q)
    rows.append(row);cleanup(r.get('tag'))
    print('CORRELATED_EXACT',json.dumps(row,sort_keys=True),flush=True)
    return row

center=evaluate(np.zeros(N),'center',-1,0.0)
if abs(center['score']-SE)>0.03 or abs(center['score_k01']-SK)>0.03:
    raise SystemExit(f'center regression mismatch exact=({center["score"]},{center["score_k01"]}) expected=({SE},{SK})')
for i,d in enumerate(dirs):
    for a in alphas:evaluate(a*d,f'dir{i}_a{a:+g}',i,a)

be=min(rows,key=lambda r:r['score']);bk=min(rows,key=lambda r:r['score_k01'])
ie=center['score']-be['score'];ik=center['score_k01']-bk['score_k01']
summary={
 'stage':'4D3-independent-correlated-multiray-acceptance',
 'scope':'local_exact_correlated_direction_test_not_global_or_statistical',
 'center':CENTER,'S_center_eff':center['score'],'S_center_k01':center['score_k01'],
 'directions':dirs.tolist(),'alphas':list(alphas),'exact_likelihood_calls':int(L.COUNTER),'timeout_retries':RETRIES,
 'best_eff':be,'best_k01':bk,'improvement_eff':ie,'improvement_k01':ik,
 'strict_no_lower_eff':bool(ie<=0.0),'strict_no_lower_k01':bool(ik<=0.0),
 'tolerance':TOL,'pass_eff':bool(ie<=TOL),'pass_k01':bool(ik<=TOL),
 'warning':'Passing is only local numerical evidence. Final model comparison still requires a frozen common objective and matched optimization.'
}
(OUT/'correlated_acceptance_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (OUT/'correlated_acceptance_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
print('STAGE4D3_CORRELATED_ACCEPTANCE_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D3_CORRELATED_ACCEPTANCE_'+('PASS' if summary['pass_eff'] and summary['pass_k01'] else 'FAIL'),flush=True)
