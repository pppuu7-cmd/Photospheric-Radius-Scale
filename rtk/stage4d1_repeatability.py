#!/usr/bin/env python3
"""Measure numerical repeatability of one exact RTK/LCDM objective point.

Usage:
  python3 stage4d1_repeatability.py PLANCK_DIR MODEL LAMBDA H OB OM AS NS ZRE NREP

MODEL is RTK or LCDM. Each repetition deliberately clears the in-process
likelihood cache and launches a fresh CLASS calculation with a new output tag.
"""
import json, math, statistics, sys
from pathlib import Path
import inference_core as L

if len(sys.argv)!=11:
    raise SystemExit(__doc__)
model=sys.argv[2].upper(); lam=float(sys.argv[3]); nrep=int(sys.argv[10])
if model not in ('RTK','LCDM') or nrep<2:
    raise SystemExit('bad model or NREP')
p={'lam':lam,'h':float(sys.argv[4]),'Ob':float(sys.argv[5]),'Om':float(sys.argv[6]),
   'As':float(sys.argv[7]),'ns':float(sys.argv[8]),'zre':float(sys.argv[9])}
if model=='RTK' and not (lam>0 and math.isfinite(lam)):
    raise SystemExit('RTK lambda must be finite positive')
if model=='LCDM': p['lam']=0.0

rows=[]
for i in range(nrep):
    L.CACHE.clear()
    r=L.evaluate(model,p)
    if not r.get('ok'):
        raise SystemExit(f'repetition {i} failed: {r}')
    row={'rep':i,
         'score_eff':float(r['score']),
         'score_k01':float(r['score_k01']),
         'logL_lowT':float(r['logL_lowT']),
         'logL_lowE':float(r['logL_lowE']),
         'logL_high':float(r['logL_high']),
         'logL_planck':float(r['logL_planck']),
         'chi2_SN':float(r['chi2_SN']),
         'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),
         'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),
         'rd':float(r['rd'])}
    rows.append(row)
    tag=r.get('tag')
    if tag:
        for q in L.OUT.glob(tag+'_*'):
            try:q.unlink()
            except OSError:pass
        for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
            try:q.unlink()
            except OSError:pass
    print('REPEAT',i,json.dumps(row,sort_keys=True),flush=True)

def stats(name):
    x=[r[name] for r in rows]
    return {'min':min(x),'max':max(x),'range':max(x)-min(x),
            'mean':statistics.fmean(x),
            'stdev':statistics.stdev(x) if len(x)>1 else 0.0}
fields=('score_eff','score_k01','logL_lowT','logL_lowE','logL_high','logL_planck',
        'chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')
summary={'stage':'4D1-exact-repeatability','model':model,'params':p,'nrep':nrep,
         'stats':{k:stats(k) for k in fields},'rows':rows}
Path('repeatability_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('STAGE4D1_REPEATABILITY_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D1_REPEATABILITY_PASS',flush=True)
