#!/usr/bin/env python3
"""Matched-ultra+dense-BOSS local nuisance poll around the production LCDM control."""
from pathlib import Path
import json
import inference_core as L
CENTER={'lam':0.0,'h':0.6779337587382693,'Ob':0.04872764689799632,'Om':0.26187225794495356,
        'As':2.1094040998203598e-9,'ns':0.9649685632254442,'zre':7.8583129349509475}
STEPS={'h':0.00070,'Ob':0.00014,'Om':0.00140,'As':8e-12,'ns':0.00070,'zre':0.14}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7',
       'perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
       'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
orig=L.make_ini
def make_ini(model,p,tag):
    path=orig(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text: raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text); f.write('\n# frozen-candidate matched-ultra+dense overrides\n')
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

def ev(p,label):
    L.CACHE.clear();r=L.evaluate('LCDM',dict(p))
    if not r.get('ok'):raise RuntimeError(f'{label}: {r}')
    row={'label':label,'score_eff':r['score'],'score_k01':r['score_k01'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],
         'chi2_BOSS_k01':r['chi2_BOSS_k01'],'chi2_SN':r['chi2_SN'],'logL_planck':r['logL_planck'],'rd':r['rd'],**p}
    cleanup(r.get('tag'));rows.append(row);print('DENSE_LCDM_POLL_POINT',json.dumps(row,sort_keys=True),flush=True)
rows=[];ev(CENTER,'center')
for q,s in STEPS.items():
    for sign in (-1,1):
        p=dict(CENTER);p[q]+=sign*s;ev(p,f'{q}_{sign:+d}')
best_eff=min(rows,key=lambda r:r['score_eff']);best_k01=min(rows,key=lambda r:r['score_k01'])
summary={'stage':'dense-lcdm-local-nuisance-poll','objective':'matched-ultra-linstep2+dense-BOSS','center':CENTER,
         'steps':STEPS,'best_eff':best_eff,'best_k01':best_k01,'rows':rows,
         'warning':'Local one-step nuisance poll, not final LCDM optimization or model comparison.'}
out=Path('output/dense_lcdm_nuisance_poll');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('DENSE_LCDM_POLL_RESULT',json.dumps(summary,sort_keys=True));print('DENSE_LCDM_POLL_COMPLETE')
