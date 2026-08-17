#!/usr/bin/env python3
import json
from pathlib import Path
import build_signature_atlas_pair as B
S=B.STATE; OUT=Path('output/signature_atlas'); OUT.mkdir(parents=True,exist_ok=True)
KEYS=('As','Ob','Om','h','ns','zre')
def shared(c): return {k:c[k] for k in KEYS}
def one(name,p,lam):
 r=dict(p);r['lam']=lam;l=dict(p);l['lam']=0.0
 a=B.run_model('RTK',r,f'cross_{name}_rtk');b=B.run_model('LCDM',l,f'cross_{name}_lcdm')
 return {'shared_parameters':p,'rtk_lambda_D':lam,'residual_rtk_over_lcdm_minus_one':B.build_residuals(a,b),'rtk':a,'lcdm':b}
def main():
 lam=S['rtk']['accepted_center']['lam']
 x={'status':'CROSS_ANCHORED_SIGNATURE_DIAGNOSTIC_NOT_MODEL_SELECTION','objective':S['objective']['name'],'state_iteration':S.get('iteration'),'method':'Hold As,Ob,Om,h,ns,zre identical; RTK uses accepted lambda_D.','rtk_center_anchor':one('rtk_center',shared(S['rtk']['accepted_center']),lam),'lcdm_center_anchor':one('lcdm_center',shared(S['lcdm']['accepted_center']),lam),'warning':'Theory-output diagnostic only; not preference/significance.'}
 (OUT/'cross_anchor.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
 for k in ('rtk_center_anchor','lcdm_center_anchor'): print('RTK_CROSS_ANCHOR',k,json.dumps(x[k]['residual_rtk_over_lcdm_minus_one'],sort_keys=True))
 print('RTK_SIGNATURE_CROSS_ANCHOR_COMPLETE')
if __name__=='__main__': main()
