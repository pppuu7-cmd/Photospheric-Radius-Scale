#!/usr/bin/env python3
"""Exact likelihood-component cross-anchor diagnostic.

At each shared-parameter anchor, compare RTK and LCDM with identical
As,Ob,Om,h,ns,zre. RTK uses the current accepted lambda_D. This isolates the
model-sector likelihood effect before standard-parameter retuning.
"""
from pathlib import Path
import json,sys
sys.argv=['matched_component_cross_anchor','planck_data']
import inference_core as L
S=json.loads(Path('../research/state/current.json').read_text())
D=S['objective']['dense_z_pk'];U={k:str(v) for k,v in S['objective']['ultra'].items()};SP='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0';orig=L.make_ini
KEYS=('As','Ob','Om','h','ns','zre')
def make_ini(m,p,t):
 q=orig(m,p,t);x=Path(q).read_text()
 if 'z_pk = '+SP not in x:raise RuntimeError('production sparse z_pk line not found')
 x=x.replace('z_pk = '+SP,'z_pk = '+D,1)
 with Path(q).open('w') as f:
  f.write(x);f.write('\n# exact likelihood cross-anchor diagnostic\n')
  for k,v in U.items():f.write(f'{k} = {v}\n')
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
def ev(m,p):
 L.CACHE.clear();r=L.evaluate(m,p)
 if not r.get('ok'):raise RuntimeError(f'{m} failed {r}')
 o={k:float(r[k]) for k in ('score','score_k01','logL_lowT','logL_lowE','logL_high','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd','z_drag')};o['params']=dict(p)
 for k in ('lowT','lowE','high','planck'):o['minus2logL_'+k]=-2*o['logL_'+k]
 clean(r.get('tag'));return o
def anchor(name,c):
 shared={k:c[k] for k in KEYS};rp=dict(shared);rp['lam']=S['rtk']['accepted_center']['lam'];lp=dict(shared);lp['lam']=0.0
 r=ev('RTK',rp);l=ev('LCDM',lp);ks=['minus2logL_lowT','minus2logL_lowE','minus2logL_high','minus2logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','score','score_k01','rd','z_drag']
 return {'name':name,'shared_parameters':shared,'rtk':r,'lcdm':l,'delta_rtk_minus_lcdm':{k:r[k]-l[k] for k in ks}}
def main():
 x={'status':'CROSS_ANCHORED_LIKELIHOOD_DIAGNOSTIC_NOT_MODEL_SELECTION','objective':S['objective']['name'],'state_iteration':S.get('iteration'),'rtk_center_anchor':anchor('rtk_center',S['rtk']['accepted_center']),'lcdm_center_anchor':anchor('lcdm_center',S['lcdm']['accepted_center']),'warning':'Fixed-shared-parameter likelihood diagnostic only; not a reoptimized model comparison.'}
 o=Path('output/matched_component_cross_anchor');o.mkdir(parents=True,exist_ok=True);(o/'summary.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('RTK_MATCHED_COMPONENT_CROSS_ANCHOR',json.dumps(x,sort_keys=True));print('RTK_MATCHED_COMPONENT_CROSS_ANCHOR_COMPLETE')
if __name__=='__main__':main()
