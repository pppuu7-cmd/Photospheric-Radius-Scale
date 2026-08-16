#!/usr/bin/env python3
"""Exact cross-evaluation of the leading strict-v5 Newton candidates.

Evaluates the candidate points in both RSD mappings at production/baseline and
at the matched-ultra l_linstep=2 settings.  This is a navigation/recenter audit,
not a global fit or model-selection calculation.
"""
from pathlib import Path
import json
import inference_core as L

POINTS={
 'eff_s1_newton':{
   'p':{'lam':281421.6615963474,'h':0.6903986240157457,'Ob':0.04685007998804382,'Om':0.25311134802564383,'As':2.08450872215591e-9,'ns':0.9643948196300038,'zre':7.238289012952434},
   'expected_eff':1050.0480026545695,
 },
 'k01_s05_newton':{
   'p':{'lam':287930.95430552866,'h':0.6904668858782219,'Ob':0.046835996338062985,'Om':0.2530185206833107,'As':2.0836316905673827e-9,'ns':0.9644013704702473,'zre':7.218930610576525},
   'expected_eff':1050.0475038880681,'expected_k01':1050.0618892996533,
 },
 'k01_s1_newton':{
   'p':{'lam':281391.5096867131,'h':0.6903983645486399,'Ob':0.04685010329664345,'Om':0.2531114663154684,'As':2.0844996373262537e-9,'ns':0.9643943147764725,'zre':7.238076894335914},
   'expected_eff':1050.0483232322536,'expected_k01':1050.0627954862323,
 },
}
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
active={};orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag)
    if active:
        with Path(path).open('a') as f:
            f.write('\n# strict-v5 Newton matched-ultra crosscheck\n')
            for k,v in active.items():f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini

rows=[]; regression=[]
for level,ov in [('baseline',{}),('matched_ultra_l2',ULTRA)]:
    active.clear();active.update(ov)
    for name,spec in POINTS.items():
        L.CACHE.clear();r=L.evaluate('RTK',dict(spec['p']))
        if not r.get('ok'):raise RuntimeError(f'{level}/{name}: {r}')
        row={'level':level,'point':name,'score_eff':r['score'],'score_k01':r['score_k01'],'logL_planck':r['logL_planck'],'logL_high':r['logL_high'],'logL_lowE':r['logL_lowE'],'logL_lowT':r['logL_lowT'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd'],'params':spec['p']}
        rows.append(row);print('STRICT_V5_NEWTON_CROSS_POINT',json.dumps(row,sort_keys=True),flush=True)
        if level=='baseline':
            reg={'point':name}
            if 'expected_eff' in spec:
                reg['delta_eff']=row['score_eff']-spec['expected_eff']
                if abs(reg['delta_eff'])>1e-9:raise RuntimeError(f'eff baseline regression {name}: {reg}')
            if 'expected_k01' in spec:
                reg['delta_k01']=row['score_k01']-spec['expected_k01']
                if abs(reg['delta_k01'])>1e-9:raise RuntimeError(f'k01 baseline regression {name}: {reg}')
            regression.append(reg);print('STRICT_V5_NEWTON_REGRESSION',json.dumps(reg,sort_keys=True),flush=True)

selection={}
for level in ('baseline','matched_ultra_l2'):
    subset=[r for r in rows if r['level']==level]
    be=min(subset,key=lambda r:r['score_eff']);bk=min(subset,key=lambda r:r['score_k01'])
    selection[level]={'best_eff_point':be['point'],'best_eff':be['score_eff'],'best_eff_k01_at_same_point':be['score_k01'],'best_k01_point':bk['point'],'best_k01':bk['score_k01'],'best_k01_eff_at_same_point':bk['score_eff']}
summary={'stage':'strict-v5-newton-crosscheck','scope':'exact fixed-point navigation audit only','rows':rows,'baseline_regression':regression,'matched_ultra_overrides':ULTRA,'selection':selection}
out=Path('output/strict_v5_newton_crosscheck');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('STRICT_V5_NEWTON_CROSS_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('STRICT_V5_NEWTON_CROSS_COMPLETE',flush=True)
