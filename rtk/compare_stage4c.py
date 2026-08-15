#!/usr/bin/env python3
"""Compare completed Stage 4C exact local optimizations.

Usage:
  python3 compare_stage4c.py RTK_EFF.json RTK_K01.json LCDM_EFF.json LCDM_K01.json [OUTDIR]

The script refuses to call a comparison stable if either model hits a trust-box
boundary.  It reports local exact objective differences only; it never labels
them as global Delta chi2, significance, posterior odds, or Bayesian evidence.
"""
from pathlib import Path
import csv, json, sys

if len(sys.argv) < 5:
    raise SystemExit(__doc__)

paths = [Path(x) for x in sys.argv[1:5]]
out = Path(sys.argv[5]) if len(sys.argv) > 5 else Path('stage4c_comparison')
out.mkdir(parents=True, exist_ok=True)

summaries = {}
for p in paths:
    d = json.loads(p.read_text())
    if d.get('stage') != '4C':
        raise SystemExit(f'{p}: not a Stage 4C summary')
    model = str(d.get('model','')).upper()
    mapping = str(d.get('mapping','')).lower()
    if model not in ('RTK','LCDM') or mapping not in ('eff','k01'):
        raise SystemExit(f'{p}: invalid model/mapping {model}/{mapping}')
    key = (model,mapping)
    if key in summaries:
        raise SystemExit(f'duplicate summary for {key}')
    summaries[key] = d

required = {(m,g) for m in ('RTK','LCDM') for g in ('eff','k01')}
missing = required - set(summaries)
if missing:
    raise SystemExit(f'missing summaries: {sorted(missing)}')

rows=[]
comparisons={}
for mapping in ('eff','k01'):
    r=summaries[('RTK',mapping)]
    l=summaries[('LCDM',mapping)]
    sr=float(r['best_S']); sl=float(l['best_S'])
    dr=sr-sl
    rb=list(r.get('boundary_axes') or [])
    lb=list(l.get('boundary_axes') or [])
    stable=(not rb and not lb and
            r.get('status')=='local_minimum_candidate' and
            l.get('status')=='local_minimum_candidate')
    comparisons[mapping]={
        'S_RTK_local':sr,
        'S_LCDM_local':sl,
        'DeltaS_RTK_minus_LCDM_local':dr,
        'RTK_status':r.get('status'),
        'LCDM_status':l.get('status'),
        'RTK_boundary_axes':rb,
        'LCDM_boundary_axes':lb,
        'stable_matched_local_comparison':stable,
        'interpretation':'local exact comparison only; not global Delta chi2/evidence'
    }
    for model,d in (('RTK',r),('LCDM',l)):
        c=d.get('best_components') or {}
        p=d.get('best_params') or {}
        row={
            'mapping':mapping,'model':model,'best_S':float(d['best_S']),
            'status':d.get('status'),'boundary_axes':';'.join(d.get('boundary_axes') or []),
            'exact_likelihood_calls':d.get('exact_likelihood_calls'),
            'improvement_vs_stage4b':d.get('improvement_vs_stage4b'),
        }
        for k in ('lam','h','Ob','Om','As','ns','zre'):
            row[k]=p.get(k)
        for k in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd'):
            row[k]=c.get(k)
        rows.append(row)

report={
    'stage':'4C-comparison',
    'scope':'matched bounded local exact minima only',
    'comparisons':comparisons,
    'warning':'Do not interpret DeltaS as a global likelihood ratio unless both basins are shown stable and a broader global search independently recovers them.'
}
(out/'stage4c_comparison.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')

fields=[]
for r in rows:
    for k in r:
        if k not in fields: fields.append(k)
with (out/'stage4c_best_points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)

md=['# RT+DBI-Khronon — Stage 4C matched local comparison','',
    'This report compares bounded exact local optimizations only. It is not a global posterior, exclusion significance, or Bayesian evidence calculation.','']
for mapping in ('eff','k01'):
    c=comparisons[mapping]
    md += [f'## {mapping}', '',
           f"- S_RTK(local) = {c['S_RTK_local']:.9f}",
           f"- S_LCDM(local) = {c['S_LCDM_local']:.9f}",
           f"- Delta S_RTK-LCDM(local) = {c['DeltaS_RTK_minus_LCDM_local']:+.9f}",
           f"- RTK status = {c['RTK_status']}; boundary axes = {c['RTK_boundary_axes'] or 'none'}",
           f"- LCDM status = {c['LCDM_status']}; boundary axes = {c['LCDM_boundary_axes'] or 'none'}",
           f"- stable matched local comparison = {c['stable_matched_local_comparison']}", '']
(out/'STAGE4C_COMPARISON.md').write_text('\n'.join(md)+'\n')

print(json.dumps(report,indent=2,sort_keys=True))
