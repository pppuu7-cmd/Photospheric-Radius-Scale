#!/usr/bin/env python3
"""Stage 4D2: conservative interpretation scaffold for an assembled lambda_D profile.

Input: CSV containing at least mapping, lambda_D and a score column (`S`,
`best_S`, or `score`).  The script works in delta_D=1/lambda_D >= 0 and
classifies whether the sampled minimum is interior or at the dust boundary.
It reports numerical shape crossings only.  It deliberately does NOT label
those crossings as confidence limits unless a future calibration step is
supplied.
"""
import csv, json, math, sys
from pathlib import Path
import numpy as np

if len(sys.argv) not in (2,3):
    raise SystemExit('usage: stage4d2_profile_interpret.py PROFILE.csv [OUTDIR]')
path=Path(sys.argv[1]); out=Path(sys.argv[2]) if len(sys.argv)==3 else Path('output/stage4d2')
out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(path.open()))
if not rows: raise SystemExit('empty profile CSV')

def get_score(r):
    for k in ('S','best_S','score','objective'):
        if k in r and r[k] not in ('',None): return float(r[k])
    raise KeyError('no score column')

def interp_cross(x0,y0,x1,y1,t):
    if (y0-t)*(y1-t)>0 or y1==y0:return None
    f=(t-y0)/(y1-y0); return x0+f*(x1-x0)

by={}
for r in rows:
    m=r.get('mapping','unknown')
    lam=float(r['lambda_D']); s=get_score(r)
    if not (lam>0 and math.isfinite(lam) and math.isfinite(s)):continue
    by.setdefault(m,[]).append({'lambda_D':lam,'delta_D':1.0/lam,'epsilon_D':lam**-0.5,'S':s})

report={'stage':'4D2-profile-interpretation-scaffold','warning':'Shape diagnostics only. No confidence level or evidence is claimed without coverage calibration / declared-prior posterior analysis.','mappings':{}}
for m,p in sorted(by.items()):
    # Sort from dust boundary outward in delta_D.
    p=sorted(p,key=lambda q:q['delta_D'])
    best=min(p,key=lambda q:q['S']); smin=best['S']
    for q in p:q['DeltaS']=q['S']-smin
    i=p.index(best)
    boundary_sampled=(i==0)
    classification='sampled_dust_boundary_minimum' if boundary_sampled else 'sampled_interior_minimum'
    # Finite-difference curvature in delta if there are neighbors on both sides.
    curvature=None
    if 0<i<len(p)-1:
        x=np.array([p[i-1]['delta_D'],p[i]['delta_D'],p[i+1]['delta_D']],float)
        y=np.array([p[i-1]['S'],p[i]['S'],p[i+1]['S']],float)
        try:
            a,b,c=np.polyfit(x,y,2); curvature=2*a
        except Exception:pass
    crossings={}
    for t in (1.0,2.71,3.84):
        xs=[]
        for a,b in zip(p[:-1],p[1:]):
            x=interp_cross(a['delta_D'],a['DeltaS'],b['delta_D'],b['DeltaS'],t)
            if x is not None: xs.append({'delta_D':x,'lambda_D':(1.0/x if x>0 else float('inf'))})
        crossings[str(t)]=xs
    note=[]
    if boundary_sampled:
        note.append('If the true optimum is delta_D=0, regular two-sided Wilks calibration is not automatic; a one-sided boundary treatment (e.g. Chernoff under its regularity conditions) or parametric-bootstrap coverage study is required.')
    else:
        note.append('The sampled optimum is interior. Wilks-like profile thresholds may become a useful approximation only after stationarity, grid refinement, nuisance regularity and coverage checks.')
    report['mappings'][m]={'classification':classification,'best':best,'local_delta_curvature':curvature,'points':p,'shape_crossings':crossings,'notes':note}

(out/'profile_interpretation.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
with (out/'profile_interpretation.md').open('w') as f:
    f.write('# Stage 4D2 profile interpretation\n\n')
    f.write('**Shape diagnostics only; not confidence limits or Bayesian evidence.**\n\n')
    for m,r in report['mappings'].items():
        b=r['best']; f.write(f'## {m}\n\nBest sampled point: lambda_D={b["lambda_D"]:.8g}, delta_D={b["delta_D"]:.8g}, S={b["S"]:.9f}.\n\nClassification: `{r["classification"]}`.\n\n')
        for n in r['notes']:f.write(n+'\n\n')
        f.write('| lambda_D | delta_D | Delta S |\n|---:|---:|---:|\n')
        for q in r['points']:f.write(f'| {q["lambda_D"]:.8g} | {q["delta_D"]:.8g} | {q["DeltaS"]:.6f} |\n')
        f.write('\n')
print('STAGE4D2_INTERPRET_PASS')
