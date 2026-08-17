#!/usr/bin/env python3
"""Trace both models along the straight shared-parameter bridge between minima.

No optimization is performed.  This diagnostic maps the strong model-parameter
non-separability exposed by the cross-anchor 2x2 experiment.
"""
from pathlib import Path
import json,sys
sys.argv=['matched_degeneracy_bridge','planck_data']
import inference_core as L
S=json.loads(Path('../research/state/current.json').read_text())
D=S['objective']['dense_z_pk'];U={k:str(v) for k,v in S['objective']['ultra'].items()};SP='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0';orig=L.make_ini
K=('As','Ob','Om','h','ns','zre');A=[0,.125,.25,.375,.5,.625,.75,.875,1.]
def make_ini(m,p,t):
 q=orig(m,p,t);x=Path(q).read_text()
 if 'z_pk = '+SP not in x:raise RuntimeError('production sparse z_pk line not found')
 x=x.replace('z_pk = '+SP,'z_pk = '+D,1)
 with Path(q).open('w') as f:
  f.write(x);f.write('\n# matched degeneracy-bridge diagnostic\n')
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
 o={k:float(r[k]) for k in ('score','score_k01','logL_lowT','logL_lowE','logL_high','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01')}
 for k in ('lowT','lowE','high','planck'):o['minus2logL_'+k]=-2*o['logL_'+k]
 clean(r.get('tag'));return o
def main():
 lo=S['lcdm']['accepted_center'];hi=S['rtk']['accepted_center'];lam=S['rtk']['accepted_center']['lam'];rows=[]
 for a in A:
  sh={k:(1-a)*float(lo[k])+a*float(hi[k]) for k in K};rp=dict(sh);rp['lam']=lam;lp=dict(sh);lp['lam']=0.0
  r=ev('RTK',rp);l=ev('LCDM',lp);row={'alpha':a,'shared_parameters':sh,'rtk':r,'lcdm':l,'delta_rtk_minus_lcdm':{k:r[k]-l[k] for k in ('score','score_k01','minus2logL_planck','minus2logL_high','minus2logL_lowE','minus2logL_lowT','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01')}};rows.append(row);print('RTK_DEGENERACY_BRIDGE_POINT',json.dumps(row,sort_keys=True),flush=True)
 x={'status':'MATCHED_DEGENERACY_BRIDGE_DIAGNOSTIC_NOT_OPTIMIZATION','objective':S['objective']['name'],'state_iteration':S.get('iteration'),'alpha_semantics':'0=LCDM accepted shared center, 1=RTK accepted shared center; both models evaluated at each shared point','rows':rows,'warning':'Straight-line shared-parameter diagnostic only; not a profile, posterior, evidence, or proof of a connecting likelihood valley.'};o=Path('output/matched_degeneracy_bridge');o.mkdir(parents=True,exist_ok=True);(o/'summary.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('RTK_DEGENERACY_BRIDGE_COMPLETE')
if __name__=='__main__':main()
