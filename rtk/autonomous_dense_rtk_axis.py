#!/usr/bin/env python3
"""State-driven matched-ultra+dense RTK 7D exact axis gate."""
from pathlib import Path
import csv, json, math, sys

sys.argv=['autonomous_dense_rtk_axis','planck_data']
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
CENTER=dict(STATE['rtk']['accepted_center'])
bs=STATE['rtk']['base_steps']
BASE=[('loglam',float(bs['loglam'])),('h',float(bs['h'])),('Ob',float(bs['Ob'])),('Om',float(bs['Om'])),('As',float(bs['As'])),('ns',float(bs['ns'])),('zre',float(bs['zre']))]
TOL=float(STATE['objective']['recenter_tolerance_S'])
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text: raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text); f.write('\n# autonomous matched-ultra+dense RTK axis\n')
        for k,v in ULTRA.items(): f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def ev(p,label,axis='',sign=0):
    L.CACHE.clear(); r=L.evaluate('RTK',dict(p))
    if not r.get('ok'): raise RuntimeError(f'{label}: {r}')
    row={'label':label,'axis':axis,'sign':sign,'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
         'logL_planck':float(r['logL_planck']),'chi2_SN':float(r['chi2_SN']),
         'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),
         'rd':float(r['rd']),'params':dict(p)}
    rows.append(row); cleanup(r.get('tag'))
    print('AUTO_DENSE_RTK_AXIS_POINT',json.dumps(row,sort_keys=True),flush=True)
    return row

rows=[]; center=ev(CENTER,'center')
for q,s in BASE:
    for sign in (-1,1):
        p=dict(CENTER)
        if q=='loglam': p['lam']=CENTER['lam']*math.exp(sign*s)
        else: p[q]=CENTER[q]+sign*s
        ev(p,f'{q}_{sign:+d}',q,sign)

best_eff=min(rows,key=lambda r:r['score_eff']); best_k01=min(rows,key=lambda r:r['score_k01'])
imp_eff=center['score_eff']-best_eff['score_eff']; imp_k01=center['score_k01']-best_k01['score_k01']
summary={'stage':'autonomous-dense-rtk-axis','objective':STATE['objective']['name'],'center':CENTER,
         'center_score_eff':center['score_eff'],'center_score_k01':center['score_k01'],'points':len(rows),
         'best_eff':best_eff,'best_k01':best_k01,'best_improvement_eff':imp_eff,'best_improvement_k01':imp_k01,
         'improvement_tolerance':TOL,'recenter_allowed_eff':bool(imp_eff>TOL),'recenter_allowed_k01':bool(imp_k01>TOL),
         'gate_eff':'RECENTER' if imp_eff>TOL else 'NO_RECENTER_AXIS_CLEAR',
         'gate_k01':'RECENTER' if imp_k01>TOL else 'NO_RECENTER_AXIS_CLEAR',
         'warning':'Mapping-specific exact axis gate; eff and k01 must not recenter each other.'}
out=Path('output/autonomous_dense_rtk_axis');out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
with (out/'points.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['label','axis','sign','score_eff','score_k01','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd','params']);w.writeheader();w.writerows(rows)
print('AUTO_DENSE_RTK_AXIS_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('AUTO_DENSE_RTK_AXIS_COMPLETE',flush=True)
