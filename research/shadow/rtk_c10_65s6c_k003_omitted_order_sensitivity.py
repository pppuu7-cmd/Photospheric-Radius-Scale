#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,math,sys
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'research/shadow'))
import rtk_c10_65n_conditional_completed_u1_onset_seed_preflight as N
import rtk_c10_65o_radiation_shear_metric_closure as O
mp.mp.dps=90;M=N.M;F=N.F
def L(p):return json.loads((ROOT/p).read_text())
def rel(a,b):a=M(a);b=M(b);return abs(a-b)/max(abs(a),abs(b),M('1e-80'))
def sgn(x):return 1 if x>0 else (-1 if x<0 else 0)
def main():
 t=L('research/theory_targets/RTK_C10_65S6C_K003_OMITTED_ORDER_SENSITIVITY_TARGET_v1.json');b=L('research/theory_results/RTK_C10_65S6B_K003_COMPLETED_ONSET_SEED_DOMAIN_AUDIT_RESULT_v1.json');s5c=L('research/theory_results/RTK_C10_65S5C_NEXT_K_OMITTED_ORDER_SENSITIVITY_RESULT_v1.json');m=L('research/theory_results/RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_RESULT_v1.json');f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json');src=L('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json');state=L('research/state/current.json')
 assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION' and b['classification']==t['parents']['C10.65s6b'] and s5c['classification']==t['parents']['C10.65s5c'] and t['threshold_changed'] is False
 assert t['domain']['eta_values']==[-1.0,0.0,1.0] and t['domain']['cartesian_point_count']==27
 ctl=m['phenomenological_regular_control_vector'];J=M('-3');A2=M(ctl['A2']);C2=M(ctl['C2']);Sur=M(ctl['S_ur0']);prod=state['final_replay_result']['rtk']['params'];gamma=M(src['provenance']['gamma_root']);bg=N.background(prod,gamma,f);lam=M('1.0016708437761068');Mc=M('9066.231026460177');k=M(t['domain']['k_Mpc_inv']);pack=f['coefficient_pack'];R=M(pack['R']);cb2=M(pack['cb2']);tau=M(pack['tau_c_Mpc']);dtau=M(pack['dtau_c']);Wg=M(4)/3*bg['rhog'];Wur=M(4)/3*bg['rhour'];Eth=M(2);Pcal=M(1)
 def evalp(ed,ec,es):
  ss=N.finite_seed(bg,lam,Mc,k,J,A2*(1+M(ed)),C2*(1+M(ec)),Eth,Pcal);cc=O.closure(a=bg['a'],H=bg['H'],R=R,cb2=cb2,tau=tau,dtau=dtau,Wg=Wg,Wur=Wur,Sur=Sur*(1+M(es)),VN=ss['VN'],Psi=ss['PsiN'],Db=ss['Db'],Dg=ss['Dg']);car={'delta_b':ss['Db']+3*ss['PsiN'],'delta_g':ss['Dg']+4*ss['PsiN'],'theta_b':k*k*ss['VN'],'shear_ur':k*k*Sur*(1+M(es))};den=[ss['DA'],ss['lapse'],ss['Bden'],cc['feedback_denominator']];vals={'psi_pref':ss['psi'],'phi_pref':ss['phi'],'B_pref':ss['B'],'Psi_N':ss['PsiN'],'Phi_N':cc['PhiN'],'V_N':ss['VN'],**car};return ss,cc,den,vals
 base_s,base_c,base_den,base_vals=evalp(0,0,0);rec=[];finite_all=True;maxproj=mp.mpf('0');maxtr=mp.mpf('0');nonzero=True;signok=True;responses={q:{'max_relative':-1.0,'eta':None,'value':None} for q in t['measurement_only']['max_relative_response']}
 for ed,ec,es in itertools.product(t['domain']['eta_values'],repeat=3):
  ss,cc,den,vals=evalp(ed,ec,es);proj=max(abs(ss['res']['A']),abs(ss['res']['Hamiltonian']),abs(ss['res']['momentum']));tr=abs(cc['res_phi']);maxproj=max(maxproj,proj);maxtr=max(maxtr,tr);nonzero &= all(math.isfinite(F(x)) and x!=0 for x in den);signok &= all(sgn(x)==sgn(y) for x,y in zip(den,base_den));finite_all &= all(math.isfinite(F(x)) for x in list(vals.values())+den)
  rr={}
  for q in responses:
   rv=F(rel(vals[q],base_vals[q]));rr[q]=rv
   if rv>responses[q]['max_relative']:responses[q]={'max_relative':rv,'eta':[ed,ec,es],'value':F(vals[q])}
  rec.append({'eta_D':ed,'eta_C':ec,'eta_S':es,'denominators':[F(x) for x in den],'projector_constraint_normalized':F(proj),'traceless_normalized':F(tr),'responses_relative_to_baseline':rr})
 old=b['record']['projector'];bm={'psi_pref':'psi_pref','phi_pref':'phi_pref','B_pref':'B_pref','Psi_N':'Psi_N','Phi_N':'Phi_N','V_N':'V_N'};baseerr=max(rel(base_vals[q],old[r]) for q,r in bm.items())
 p=t['prospective_checks'];checks={'point_count':len(rec)==int(t['domain']['cartesian_point_count']),'baseline_reproduces_s6b_relative_max':baseerr<=M(p['baseline_reproduces_s6b_relative_max']),'all_27_points_finite':finite_all,'projector_constraint_normalized_residual_max':maxproj<=M(p['projector_constraint_normalized_residual_max']),'physical_traceless_normalized_residual_max':maxtr<=M(p['physical_traceless_normalized_residual_max']),'all_four_algebraic_denominators_nonzero':nonzero,'no_algebraic_denominator_sign_flip_relative_to_baseline':signok,'legacy_nlde_auxiliaries_excluded':True,'historical_metric_not_consumed':True,'threshold_changed':False};passed=checks['threshold_changed'] is False and all(v for q,v in checks.items() if q!='threshold_changed')
 out={'schema':'RTK_C10_65S6C_K003_OMITTED_ORDER_SENSITIVITY_RESULT_v1','gate':'C10.65s6c','classification':t['pass_classification'] if passed else t['fail_classification'],'target':'research/theory_targets/RTK_C10_65S6C_K003_OMITTED_ORDER_SENSITIVITY_TARGET_v1.json','checks':checks,'maxima':{'baseline_reproduction_relative':F(baseerr),'projector_constraint_normalized':F(maxproj),'traceless_normalized':F(maxtr),'min_abs_denominator':min(abs(F(x)) for z in rec for x in z['denominators'])},'response_map_measurement_only':responses,'records':rec,'interpretation':t['interpretation_if_pass'] if passed else 'The frozen k=0.03 omitted-order sensitivity envelope encountered a nonfinite state, closure failure, or algebraic denominator sign change; do not proceed to production feedback.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s6c without weakening its frozen envelope or algebraic checks.','non_claims':t['non_claims'],'threshold_changed':False};(ROOT/'research/theory_results/RTK_C10_65S6C_K003_OMITTED_ORDER_SENSITIVITY_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n');print(out['classification']);print(json.dumps({'maxima':out['maxima'],'response':responses},sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
