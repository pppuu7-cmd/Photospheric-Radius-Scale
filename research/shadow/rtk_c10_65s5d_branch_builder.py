#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'research/shadow'))
import rtk_c10_65n_conditional_completed_u1_onset_seed_preflight as N
import rtk_c10_65o_radiation_shear_metric_closure as O
mp.mp.dps=90;M=N.M;F=N.F
def L(p):return json.loads((ROOT/p).read_text())
def build(branch_id:str):
 t=L('research/theory_targets/RTK_C10_65S5D_NEXT_K_MULTIBRANCH_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json');m=L('research/theory_results/RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_RESULT_v1.json');f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json');src=L('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json');state=L('research/state/current.json');b=L('research/theory_results/RTK_C10_65S5B_NEXT_K_COMPLETED_ONSET_SEED_DOMAIN_AUDIT_RESULT_v1.json')
 br=next(x for x in t['domain']['branches'] if x['id']==branch_id);ctl=m['phenomenological_regular_control_vector'];J=M('-3');A2=M(ctl['A2']);C2=M(ctl['C2']);Sur=M(ctl['S_ur0']);prod=state['final_replay_result']['rtk']['params'];gamma=M(src['provenance']['gamma_root']);bg=N.background(prod,gamma,f);k=M(t['domain']['k_Mpc_inv']);lam=M(t['domain']['lambda_HL']);Mc=M(t['domain']['M_c_Mpc_inv']);ed=M(br['eta_D']);ec=M(br['eta_C']);es=M(br['eta_S']);ss=N.finite_seed(bg,lam,Mc,k,J,A2*(1+ed),C2*(1+ec),M(2),M(1));pack=f['coefficient_pack'];cc=O.closure(a=bg['a'],H=bg['H'],R=M(pack['R']),cb2=M(pack['cb2']),tau=M(pack['tau_c_Mpc']),dtau=M(pack['dtau_c']),Wg=M(4)/3*bg['rhog'],Wur=M(4)/3*bg['rhour'],Sur=Sur*(1+es),VN=ss['VN'],Psi=ss['PsiN'],Db=ss['Db'],Dg=ss['Dg']);w=bg['w_khr'];carrier={'phi_CLASS_equals_Psi_N':F(ss['PsiN']),'delta_b':F(ss['Db']+3*ss['PsiN']),'theta_b':F(k*k*ss['VN']),'delta_g':F(ss['Dg']+4*ss['PsiN']),'theta_g':F(k*k*ss['VN']),'delta_ur':F(ss['Dur']+4*ss['PsiN']),'theta_ur':F(k*k*ss['VN']),'shear_ur':F(k*k*Sur*(1+es)),'delta_cdm_khr':F((1+w)*(ss['Jkhr']+3*ss['PsiN'])),'theta_cdm_khr':F(k*k*ss['VN'])};U={int(x['l']):float(x['F_l']) for x in b['record']['ur_l_ge_3']};return {'branch':br,'k':F(k),'background':{q:F(v) for q,v in bg.items()},'carrier':carrier,'ur_l_ge_3':U,'projector':{'B':F(ss['B']),'psi_pref':F(ss['psi']),'psi_pref_prime':F(ss['psip']),'phi_pref':F(ss['phi']),'Psi_N':F(ss['PsiN']),'Phi_N':F(cc['PhiN']),'feedback_denominator':F(cc['feedback_denominator'])}}
if __name__=='__main__':print(json.dumps(build(sys.argv[1]),indent=2,sort_keys=True))
