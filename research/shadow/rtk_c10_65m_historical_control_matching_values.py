#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math
from pathlib import Path
import numpy as np

BASE=['c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime','c10_H0_ord_double_prime','c10_deltaH0_ord','c10_delta_mu_total','c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total','c10_W_total','c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
CTRL=['c10_65a_delta_g','c10_65a_theta_g','c10_65a_shear_g','c10_65a_delta_b','c10_65a_theta_b','c10_65a_CLASS_psi_lapse','c10_65a_CLASS_phi_curvature','c10_65a_delta_ur','c10_65a_theta_ur','c10_65a_shear_ur']
TAIL=BASE+CTRL

def rows(p):
 out=[]
 for raw in Path(p).read_text().splitlines():
  s=raw.strip()
  if not s or s.startswith('#'): continue
  v=[float(q) for q in s.split()]
  z={name:v[-len(TAIL)+i] for i,name in enumerate(TAIL)}; z['tau']=v[0]; z['a']=v[1]; out.append(z)
 return out

def fit_affine(x,y,n):
 X=np.column_stack([np.ones(n),x[:n]])
 c=np.linalg.lstsq(X,y[:n],rcond=None)[0]
 return float(c[0]),float(c[1])
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--glob',dest='pat',required=True); ap.add_argument('--output',required=True); A=ap.parse_args()
 root=Path(__file__).resolve().parents[2]
 t=json.loads((root/'research/theory_targets/RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_TARGET_v1.json').read_text())
 l=json.loads((root/'research/theory_results/RTK_C10_65L_UV_MATCHING_INTERFACE_BASIS_RESULT_v1.json').read_text())
 f=json.loads((root/'research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json').read_text())
 assert t['status']=='FROZEN_BEFORE_EXECUTION'; assert l['classification']=='C10_65L_UV_MATCHING_INTERFACE_BASIS_PASS_SCOPED'; assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
 aon=float(f['exact_anchor']['a_on']); expected=[float(q) for q in f['exact_anchor']['k_Mpc_inv']]
 files=sorted(glob.glob(A.pat)); assert len(files)==len(expected)
 samples=[]
 for fn in files:
  rr=rows(fn); k=sum(z['c10_k_Mpc_inv'] for z in rr)/len(rr)
  z=min(rr,key=lambda q:abs(q['a']-aon)); ea=abs(z['a']-aon)/aon
  if ea>1e-12: raise RuntimeError(f'no exact onset row k={k}: relerr={ea}')
  samples.append((k,z,Path(fn).name,ea))
 samples.sort()
 for (k,_,_,_),ke in zip(samples,expected):
  if abs(k-ke)>1e-10*max(1.,abs(ke)): raise RuntimeError(f'k mismatch {k} {ke}')
 rec=[]
 for k,z,fn,ea in samples:
  x=k*k; phi=z['c10_65a_CLASS_phi_curvature']; Db=z['c10_65a_delta_b']-3*phi
  Sur=z['c10_65a_shear_ur']/x
  H=z['c10_Hc']; dm=z['c10_delta_mu_total']; rpp=z['c10_rpp_theta_total']
  C=3*aon*aon*dm + 9*H*aon*aon*rpp/x
  rec.append({'k_Mpc_inv':k,'x_k2':x,'D_b':Db,'S_ur_over_k2':Sur,'C':C,'C_over_k2':C/x,'Hc':H,'delta_mu_total':dm,'rpp_theta_total':rpp,'source_file':fn,'relative_a_error':ea})
 x=np.array([r['x_k2'] for r in rec]); db=np.array([r['D_b'] for r in rec]); su=np.array([r['S_ur_over_k2'] for r in rec]); cy=np.array([r['C_over_k2'] for r in rec])
 db03,A3=fit_affine(x,db,3); db04,A4=fit_affine(x,db,4)
 S3,_=fit_affine(x,su,3); S4,_=fit_affine(x,su,4)
 C23,_=fit_affine(x,cy,3); C24,_=fit_affine(x,cy,4)
 Xq=np.column_stack([np.ones(4),x,x*x]); cq=np.linalg.lstsq(Xq,np.array([r['C'] for r in rec]),rcond=None)[0]
 dA=rel(A3,A4); dS=rel(S3,S4); dC=rel(C23,C24)
 finite=all(math.isfinite(q) for q in [A3,A4,S3,S4,C23,C24,*cq])
 ok=finite and dA<=1e-4 and dS<=1e-8 and dC<=0.1
 cls='C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_PASS_SCOPED' if ok else 'C10_65M_HISTORICAL_C2_CONTROL_NUMERICALLY_UNRESOLVED_SCOPED'
 vector={'A2':A4,'E_gb2':0.0,'E_urb2':0.0,'E_khr2':0.0,'R_gb0':0.0,'R_urb0':0.0,'R_khrb0':0.0,'S_ur0':S4,'C2':C24} if ok else None
 out={'schema':'RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_RESULT_v1','gate':'C10.65m','classification':cls,'target':'research/theory_targets/RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_TARGET_v1.json','a_on':aon,'records':rec,'fits':{'A2':{'smallest3':A3,'all4':A4,'nested_relative_disagreement':dA,'D_b0_smallest3':db03,'D_b0_all4':db04},'S_ur0':{'smallest3':S3,'all4':S4,'nested_relative_disagreement':dS},'C2':{'smallest3':C23,'all4':C24,'nested_relative_disagreement':dC},'direct_C_quadratic':{'C0':float(cq[0]),'C2':float(cq[1]),'C4':float(cq[2])}},'acceptance':{'all_finite':finite,'A2_nested_threshold':1e-4,'S_ur0_nested_threshold':1e-8,'C2_nested_threshold':0.1,'pass':ok},'phenomenological_regular_control_vector':vector,'control_status':'HISTORICAL_PHENOMENOLOGICAL_CONTROL_ONLY','interpretation':'These values are read-only historical boundary controls. They are not completed-U1 predictions and do not derive the pre-EFT matching physics. C(k) uses only total matter source columns and H, not historical metric potentials.','next_gate':t['next_if_pass'] if ok else 'Improve the numerical extraction of the gauge-invariant historical C2 control without weakening the frozen stability threshold; do not proceed to a conditional seed with an unresolved C2.','non_claims':t['non_claims']}
 Path(A.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(cls,json.dumps({'A2':A4,'S_ur0':S4,'C2':C24,'dA':dA,'dS':dS,'dC2':dC},sort_keys=True))
if __name__=='__main__': main()
