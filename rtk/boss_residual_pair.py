#!/usr/bin/env python3
import json,math
from pathlib import Path
import build_signature_atlas_pair as B
S=B.STATE;RF=147.78;C=299792.458
obs=[]
for l in Path('boss_DR12Consensus_final.dat').read_text().splitlines():
 if l.strip() and not l.lstrip().startswith('#'):
  z,v,k=l.split()[:3];obs.append((float(z),float(v),k))
cov=[[float(x) for x in l.split()] for l in Path('final_consensus_covtot_dM_Hz_fsig.txt').read_text().splitlines() if l.strip()]
def chol(A):
 n=len(A);L=[[0.]*n for _ in range(n)]
 for i in range(n):
  for j in range(i+1):
   s=sum(L[i][k]*L[j][k] for k in range(j));L[i][j]=math.sqrt(A[i][i]-s) if i==j else (A[i][j]-s)/L[j][j]
 return L
def q(A,r):
 L=chol(A);n=len(r);y=[0.]*n;x=[0.]*n
 for i in range(n):y[i]=(r[i]-sum(L[i][j]*y[j] for j in range(i)))/L[i][i]
 for i in range(n-1,-1,-1):x[i]=(y[i]-sum(L[j][i]*x[j] for j in range(i+1,n)))/L[i][i]
 return sum(r[i]*x[i] for i in range(n))
def subset(r,idx):return q([[cov[i][j] for j in idx] for i in idx],[r[i] for i in idx])
def pred(t,which):
 out=[]
 for z,_,k in obs:
  zz=str(z)
  if k=='DM_over_rs':out.append(t['background'][zz]['D_M_Mpc']*RF/t['rd_Mpc'])
  elif k=='bao_Hz_rs':out.append(t['background'][zz]['H_over_c_Mpc_inv']*C*t['rd_Mpc']/RF)
  else:out.append(t['growth'][zz]['fs8_eff' if which=='eff' else 'fs8_k01'])
 return out
def pack(t,which):
 p=pred(t,which);d=[x[1] for x in obs];r=[a-b for a,b in zip(p,d)];tot=q(cov,r);blocks={'z0.38':[0,1,2],'z0.51':[3,4,5],'z0.61':[6,7,8],'DM':[0,3,6],'H':[1,4,7],'fs8':[2,5,8]};loo={}
 for n,drop in blocks.items():
  keep=[i for i in range(9) if i not in drop];v=subset(r,keep);loo[n]={'chi2_retained':v,'total_minus_retained':tot-v}
 return {'prediction':p,'residual':r,'standardized_raw_residual':[r[i]/math.sqrt(cov[i][i]) for i in range(9)],'chi2':tot,'leave_one_block_out':loo}
def model(m,p,tag):
 t=B.run_model(m,p,tag);return {'params':p,'rd_Mpc':t['rd_Mpc'],'eff':pack(t,'eff'),'k01':pack(t,'k01')}
def main():
 r=model('RTK',dict(S['rtk']['accepted_center']),'bossdiag_rtk');l=model('LCDM',dict(S['lcdm']['accepted_score_params']),'bossdiag_lcdm')
 if abs(r['eff']['chi2']-7.612172203431612)>2e-6:raise RuntimeError('RTK BOSS chi2 mismatch')
 if abs(l['eff']['chi2']-6.727613594395151)>2e-6:raise RuntimeError('LCDM BOSS chi2 mismatch')
 x={'status':'BOSS_CURRENT_POINT_RESIDUAL_DIAGNOSTIC','objective':S['objective']['name'],'state_iteration':S.get('iteration'),'observable_order':[{'z':z,'kind':k,'data':v} for z,v,k in obs],'rtk':r,'lcdm':l,'warning':'Leave-one-block values are correlated influence diagnostics, not unique additive chi2 contributions. Compressed fs8 remains approximate for RTK.'}
 o=Path('output/boss_residual_pair');o.mkdir(parents=True,exist_ok=True);(o/'summary.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print('RTK_BOSS_RESIDUAL_PAIR',json.dumps(x,sort_keys=True));print('RTK_BOSS_RESIDUAL_PAIR_COMPLETE')
if __name__=='__main__':main()
