#!/usr/bin/env python3
import json
from pathlib import Path
import boss_residual_pair as D
S=D.S;P=dict(S['rtk']['accepted_center']);L=P['lam'];F=[.125,.25,.5,1,2,4,8]
def main():
 a=[]
 for f in F:
  p=dict(P);p['lam']=L*f;t=D.B.run_model('RTK',p,f'bosslam_{f:g}');e=D.pack(t,'eff')
  r={'factor':f,'lambda_D':p['lam'],'chi2_eff':e['chi2'],'prediction':e['prediction'],'std_residual':e['standardized_raw_residual']};a.append(r);print('BOSS_LAMBDA_POINT',json.dumps(r,sort_keys=True),flush=True)
 x={'status':'FIXED_SHARED_BOSS_LAMBDA_DIAGNOSTIC','objective':S['objective']['name'],'base_center':P,'rows':a,'warning':'No retuning/optimization; BOSS-only sensitivity diagnostic.'};o=Path('output/boss_lambda_sensitivity');o.mkdir(parents=True,exist_ok=True);(o/'summary.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('BOSS_LAMBDA_SENSITIVITY_COMPLETE')
if __name__=='__main__':main()
