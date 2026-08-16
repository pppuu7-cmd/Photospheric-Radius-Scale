#!/usr/bin/env python3
"""Rank strict-v5 Newton candidates on the dense-BOSS matched-ultra l2 objective.

The sparse matched-ultra scores are regressed against run 31935767003 at 1e-9.
Then only z_pk is changed to the audited dense grid.  The lowest exact dense
candidate becomes the navigation center for strict-final geometry.  This is a
fixed-point navigation audit, not a global fit or model-selection result.
"""
from pathlib import Path
import json
import inference_core as L

POINTS={
 'A_eff_s1':{
  'p':{'lam':281421.6615963474,'h':0.6903986240157457,'Ob':0.04685007998804382,'Om':0.25311134802564383,'As':2.08450872215591e-9,'ns':0.9643948196300038,'zre':7.238289012952434},
  'sparse_eff':1050.367627731344,'sparse_k01':1050.382043112446},
 'B_k01_s05':{
  'p':{'lam':287930.95430552866,'h':0.6904668858782219,'Ob':0.046835996338062985,'Om':0.2530185206833107,'As':2.0836316905673827e-9,'ns':0.9644013704702473,'zre':7.218930610576525},
  'sparse_eff':1050.389351669405,'sparse_k01':1050.4036796007128},
 'C_k01_s1':{
  'p':{'lam':281391.5096867131,'h':0.6903983645486399,'Ob':0.04685010329664345,'Om':0.2531114663154684,'As':2.0844996373262537e-9,'ns':0.9643943147764725,'zre':7.238076894335914},
  'sparse_eff':1050.3678540135159,'sparse_k01':1050.38226798366},
}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE='0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'
ULTRA={'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7','perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180','k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2'}
mode='sparse';orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag)
    text=Path(path).read_text();needle='z_pk = '+SPARSE
    if needle not in text: raise RuntimeError('production sparse z_pk line not found')
    if mode=='dense': text=text.replace(needle,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text);f.write('\n# dense Newton crosscheck matched-ultra l2\n')
        for k,v in ULTRA.items():f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini

rows=[];reg=[]
for m in ('sparse','dense'):
    mode=m
    for name,spec in POINTS.items():
        L.CACHE.clear();r=L.evaluate('RTK',dict(spec['p']))
        if not r.get('ok'):raise RuntimeError(f'{m}/{name}: {r}')
        row={'mode':m,'point':name,'score_eff':r['score'],'score_k01':r['score_k01'],'logL_planck':r['logL_planck'],'chi2_SN':r['chi2_SN'],'chi2_BOSS_eff':r['chi2_BOSS_eff'],'chi2_BOSS_k01':r['chi2_BOSS_k01'],'rd':r['rd'],'params':spec['p']}
        rows.append(row);print('NEWTON_DENSE_L2_POINT',json.dumps(row,sort_keys=True),flush=True)
        if m=='sparse':
            q={'point':name,'delta_eff':r['score']-spec['sparse_eff'],'delta_k01':r['score_k01']-spec['sparse_k01']}
            reg.append(q);print('NEWTON_DENSE_L2_SPARSE_REGRESSION',json.dumps(q,sort_keys=True),flush=True)
            if abs(q['delta_eff'])>1e-9 or abs(q['delta_k01'])>1e-9:raise RuntimeError(f'sparse regression failed: {q}')
by={(r['mode'],r['point']):r for r in rows}
changes={}
for name in POINTS:
    a=by[('sparse',name)];b=by[('dense',name)]
    changes[name]={'delta_eff_dense_minus_sparse':b['score_eff']-a['score_eff'],'delta_k01_dense_minus_sparse':b['score_k01']-a['score_k01'],'delta_BOSS_eff':b['chi2_BOSS_eff']-a['chi2_BOSS_eff'],'delta_BOSS_k01':b['chi2_BOSS_k01']-a['chi2_BOSS_k01']}
dense=[r for r in rows if r['mode']=='dense'];be=min(dense,key=lambda r:r['score_eff']);bk=min(dense,key=lambda r:r['score_k01'])
selection={'best_eff_point':be['point'],'best_eff':be['score_eff'],'k01_at_best_eff':be['score_k01'],'best_k01_point':bk['point'],'best_k01':bk['score_k01'],'eff_at_best_k01':bk['score_eff'],'same_point':be['point']==bk['point']}
summary={'stage':'strict-v5-newton-dense-l2-crosscheck','scope':'exact fixed-point navigation audit only','ultra_overrides':ULTRA,'z_pk_sparse':SPARSE,'z_pk_dense':DENSE,'rows':rows,'sparse_regression':reg,'dense_minus_sparse':changes,'selection':selection}
out=Path('output/strict_v5_newton_dense_l2_crosscheck');out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('NEWTON_DENSE_L2_RESULT',json.dumps(summary,sort_keys=True),flush=True);print('NEWTON_DENSE_L2_COMPLETE',flush=True)
