#!/usr/bin/env python3
"""Exact likelihood scan along a correlated 7D RTK direction.

Usage:
  python3 stage4d3_ray_scan.py PLANCK_DIR \
    lam0 h0 Ob0 Om0 As0 ns0 zre0 lam1 h1 Ob1 Om1 As1 ns1 zre1 TLIST

TLIST is a comma-separated list such as 0,0.5,1,1.25,1.5,2.
Lambda is interpolated linearly in log(lambda); the six remaining parameters
are interpolated linearly. Both eff and k01 scores are recorded at every
exact point. This is a navigation diagnostic, not a stationarity/global-fit
or statistical-significance test.
"""
from pathlib import Path
import csv, json, math, sys
import inference_core as L

if len(sys.argv) != 17:
    raise SystemExit(__doc__)
names = ('h','Ob','Om','As','ns','zre')
vals = list(map(float, sys.argv[2:16]))
p0 = {'lam': vals[0], **dict(zip(names, vals[1:7]))}
p1 = {'lam': vals[7], **dict(zip(names, vals[8:14]))}
ts = [float(x.strip()) for x in sys.argv[16].split(',') if x.strip()]
if not ts or p0['lam'] <= 0 or p1['lam'] <= 0:
    raise SystemExit('invalid endpoints or TLIST')
OUT = Path('output/stage4d3_ray_scan'); OUT.mkdir(parents=True, exist_ok=True)
rows = []; RETRIES=0

def point(t):
    p = {'lam': math.exp(math.log(p0['lam']) + t*(math.log(p1['lam'])-math.log(p0['lam'])))}
    for n in names:p[n] = p0[n] + t*(p1[n]-p0[n])
    return p

def cleanup(tag):
    if not tag:return
    for f in L.OUT.glob(tag+'_*'):
        try:f.unlink()
        except OSError:pass
    for f in (Path(f'profile_{tag}.ini'), Path(f'profile_{tag}.log')):
        try:f.unlink()
        except OSError:pass

def is_timeout(r):return r.get('error')=='CLASS_TIMEOUT' or r.get('reason')=='CLASS_TIMEOUT' or 'CLASS_TIMEOUT' in str(r.get('reason',''))

def evaluate(p,t):
    global RETRIES
    r=L.evaluate('RTK',p)
    if not r.get('ok') and is_timeout(r):
        RETRIES+=1;cleanup(r.get('tag'))
        try:
            ikey=('RTK',)+tuple(float(p[q]) for q in ['lam','h','Ob','Om','As','ns','zre'])
            L.CACHE.pop(ikey,None)
        except Exception:pass
        r=L.evaluate('RTK',p)
    if not r.get('ok'):raise RuntimeError(f'exact evaluation failed at t={t}: {r}')
    return r

for t in ts:
    p=point(t);r=evaluate(p,t)
    row={'t':t,**p}
    for q in ('score','score_k01','logL_planck','logL_lowT','logL_lowE','logL_high','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
        row[q]=r.get(q)
    rows.append(row);print('RAY_EXACT',json.dumps(row,sort_keys=True),flush=True);cleanup(r.get('tag'))

best_eff=min(rows,key=lambda r:r['score']);best_k01=min(rows,key=lambda r:r['score_k01'])
summary={'stage':'4D3-exact-correlated-ray-navigation','scope':'exact_likelihood_navigation_not_stationarity_or_global_profile','endpoint0':p0,'endpoint1':p1,'t_values':ts,'best_eff':best_eff,'best_k01':best_k01,'exact_likelihood_calls':int(L.COUNTER),'timeout_retries':RETRIES,'warning':'A lower point on this ray is only a new exact candidate; it is not a converged minimum or statistical preference.'}
(OUT/'ray_scan_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (OUT/'ray_scan_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
print('STAGE4D3_RAY_SCAN_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('STAGE4D3_RAY_SCAN_COMPLETE',flush=True)
