#!/usr/bin/env python3
from pathlib import Path
import json,sys
sys.argv=['matched_component_pair','planck_data']
import inference_core as L
S=json.loads(Path('../research/state/current.json').read_text())
D=S['objective']['dense_z_pk'];U={k:str(v) for k,v in S['objective']['ultra'].items()};SP='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0';orig=L.make_ini
def make_ini(m,p,t):
 q=orig(m,p,t);x=Path(q).read_text()
 if 'z_pk = '+SP not in x: raise RuntimeError('production sparse z_pk line not found')
 x=x.replace('z_pk = '+SP,'z_pk = '+D,1)
 with Path(q).open('w') as f:
  f.write(x);f.write('\n# matched component-pair frozen dense objective\n')
  for k,v in U.items(): f.write(f'{k} = {v}\n')
 return q
L.make_ini=make_ini
def clean(t):
 if not t:return
 for p in L.OUT.glob(t+'_*'):
  try:p.unlink()
  except OSError:pass
 for p in (Path(f'profile_{t}.ini'),Path(f'profile_{t}.log')):
  try:p.unlink()
  except OSError:pass
def run(m,p):
 L.CACHE.clear();r=L.evaluate(m,p)
 if not r.get('ok'): raise RuntimeError(f'{m} failed: {r}')
 o={k:r[k] for k in ('score','score_k01','logL_lowT','logL_lowE','logL_high','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd','z_drag')};o['params']=dict(p)
 for k in ('lowT','lowE','high','planck'):o['minus2logL_'+k]=-2.0*o['logL_'+k]
 clean(r.get('tag'));return o
rtk=run('RTK',dict(S['rtk']['accepted_center']));lcdm=run('LCDM',dict(S['lcdm']['accepted_score_params']))
er=float(S['rtk']['axis_result']['center_score_eff']);el=float(S['lcdm']['accepted_score_eff']);tol=2e-6
if abs(rtk['score']-er)>tol: raise RuntimeError(f'RTK score mismatch {rtk["score"]} != {er}')
if abs(lcdm['score']-el)>tol: raise RuntimeError(f'LCDM score mismatch {lcdm["score"]} != {el}')
keys=['minus2logL_lowT','minus2logL_lowE','minus2logL_high','minus2logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','score','score_k01','rd','z_drag'];d={k:rtk[k]-lcdm[k] for k in keys}
x={'status':'PROVISIONAL_BEST_KNOWN_COMPONENTS_RTK_STATIONARITY_PENDING','objective':S['objective']['name'],'state_iteration':S.get('iteration'),'rtk':rtk,'lcdm':lcdm,'delta_rtk_minus_lcdm':d,'score_guard_tolerance':tol,'expected_scores':{'rtk_eff':er,'lcdm_eff':el},'warning':'Current best-known matched points only; not final model selection.'}
o=Path('output/matched_component_pair');o.mkdir(parents=True,exist_ok=True);(o/'summary.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('RTK_MATCHED_COMPONENT_PAIR',json.dumps(x,sort_keys=True));print('RTK_MATCHED_COMPONENT_PAIR_COMPLETE')
