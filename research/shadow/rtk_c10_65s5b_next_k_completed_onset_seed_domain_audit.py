#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/shadow'))
import rtk_c10_65n_conditional_completed_u1_onset_seed_preflight as N
import rtk_c10_65o_radiation_shear_metric_closure as O
mp.mp.dps=90
M=N.M;F=N.F
def L(p):return json.loads((ROOT/p).read_text())
def rel(a,b):
    a=M(a);b=M(b);return abs(a-b)/max(abs(a),abs(b),M('1e-80'))
def main():
    t=L('research/theory_targets/RTK_C10_65S5B_NEXT_K_COMPLETED_ONSET_SEED_DOMAIN_AUDIT_TARGET_v1.json')
    s5a=L('research/theory_results/RTK_C10_65S5A_NEXT_K_NEAR_HORIZON_ONSET_STATE_PREFLIGHT_RESULT_v1.json')
    s4b=L('research/theory_results/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    m=L('research/theory_results/RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_RESULT_v1.json')
    f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=L('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json')
    state=L('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert s5a['classification']==t['parents']['C10.65s5a']
    assert s4b['classification']==t['parents']['C10.65s4b']
    ctl=m['phenomenological_regular_control_vector'];J=M('-3');A2=M(ctl['A2']);C2=M(ctl['C2']);Sur=M(ctl['S_ur0']);Eth=M(2);Pcal=M(1)
    prod=state['final_replay_result']['rtk']['params'];gamma=M(src['provenance']['gamma_root']);bg=N.background(prod,gamma,f)
    lam=M(t['domain']['lambda_HL']);Mc=M(t['domain']['M_c_Mpc_inv']);pack=f['coefficient_pack'];R=M(pack['R']);cb2=M(pack['cb2']);tau=M(pack['tau_c_Mpc']);dtau=M(pack['dtau_c']);Wg=M(4)/3*bg['rhog'];Wur=M(4)/3*bg['rhour']
    # Regression at the previously-certified largest moderate-k seed.
    regk=M(t['domain']['regression_k_Mpc_inv'][0]);old={M(r['k']):r for r in s4b['records']}[regk]
    rs=N.finite_seed(bg,lam,Mc,regk,J,A2,C2,Eth,Pcal);rc=O.closure(a=bg['a'],H=bg['H'],R=R,cb2=cb2,tau=tau,dtau=dtau,Wg=Wg,Wur=Wur,Sur=Sur,VN=rs['VN'],Psi=rs['PsiN'],Db=rs['Db'],Dg=rs['Dg'])
    reg=mp.mpf('0')
    pm=old['projector']
    pairs={'psi_pref':rs['psi'],'psi_pref_prime':rs['psip'],'phi_pref':rs['phi'],'B_pref':rs['B'],'Psi_N':rs['PsiN'],'Phi_N':rc['PhiN'],'V_N':rs['VN']}
    for name,val in pairs.items():reg=max(reg,rel(val,pm[name]))
    # New near-horizon anchor using exactly the inherited phenomenological polynomial.
    k=M(t['domain']['new_k_Mpc_inv'][0]);s=N.finite_seed(bg,lam,Mc,k,J,A2,C2,Eth,Pcal);cl=O.closure(a=bg['a'],H=bg['H'],R=R,cb2=cb2,tau=tau,dtau=dtau,Wg=Wg,Wur=Wur,Sur=Sur,VN=s['VN'],Psi=s['PsiN'],Db=s['Db'],Dg=s['Dg'])
    projmax=max(abs(s['res']['A']),abs(s['res']['Hamiltonian']),abs(s['res']['momentum']));tr=abs(cl['res_phi']);dens=[abs(s['DA']),abs(s['lapse']),abs(s['Bden']),abs(cl['feedback_denominator'])];mind=min(dens)
    carrier={'phi_CLASS_equals_Psi_N':F(s['PsiN']),'delta_b':F(s['Db']+3*s['PsiN']),'theta_b':F(k*k*s['VN']),'delta_g':F(s['Dg']+4*s['PsiN']),'theta_g':F(k*k*s['VN']),'delta_ur':F(s['Dur']+4*s['PsiN']),'theta_ur':F(k*k*s['VN']),'shear_ur':F(k*k*Sur),'delta_cdm_khr':F((1+bg['w_khr'])*(s['Jkhr']+3*s['PsiN'])),'theta_cdm_khr':F(k*k*s['VN'])}
    row={M(r['k']):r for r in s5a['onset_rows']}[k]
    hc=[]
    for ls,val in row['F_over_kpow'].items():
        l=int(ls)
        if 3<=l<=17:hc.append({'l':l,'F_l_over_k_pow_l':float(val),'F_l':float(M(val)*(k**l)),'status':'HIGHER_ORDER_HISTORICAL_CONTROL_FROM_S5A_ONLY'})
    vals=list(carrier.values())+[F(s[x]) for x in ('psi','psip','phi','B','PsiN','VN')]+[F(cl['PhiN']),F(cl['sigma_g_over_k2'])]+[float(x) for x in dens]
    finite_all=all(math.isfinite(x) for x in vals) and all(math.isfinite(x['F_l']) and math.isfinite(x['F_l_over_k_pow_l']) for x in hc)
    # Historical observer is diagnostic only; compare ordinary coordinates without consuming historical metric as completed boundary data.
    diag={}
    mapnames={'delta_b':'delta_b','theta_b':'theta_b','delta_g':'delta_g','theta_g':'theta_g','delta_ur':'delta_ur','theta_ur':'theta_ur','shear_ur':'shear_ur'}
    for a,b in mapnames.items():diag[a]={'completed':carrier[a],'legacy_observer':row[b],'relative_difference':float(rel(carrier[a],row[b]))}
    p=t['prospective_checks']
    checks={'new_anchor_count':1==int(p['new_anchor_count']),'all_projector_and_carrier_values_finite':finite_all,'preferred_A_Hamiltonian_momentum_normalized_residual_max':projmax<=M(p['projector_constraint_normalized_residual_max']),'physical_traceless_normalized_residual_max':tr<=M(p['physical_traceless_normalized_residual_max']),'all_projector_denominators_nonzero':mind>0,'regression_relative_max':reg<=M(p['regression_relative_max']),'legacy_nlde_auxiliaries_excluded':True,'historical_metric_not_consumed':True,'higher_ur_controls_explicitly_labeled':len(hc)==15 and all(x['status']==p['active_UR_l_ge_3_source'] for x in hc),'threshold_changed':False}
    passed=checks['threshold_changed'] is False and all(v for q,v in checks.items() if q!='threshold_changed')
    out={'schema':'RTK_C10_65S5B_NEXT_K_COMPLETED_ONSET_SEED_DOMAIN_AUDIT_RESULT_v1','gate':'C10.65s5b','classification':t['pass_classification'] if passed else t['fail_classification'],'target':'research/theory_targets/RTK_C10_65S5B_NEXT_K_COMPLETED_ONSET_SEED_DOMAIN_AUDIT_TARGET_v1.json','matching_polynomial_status':t['domain']['matching_polynomial_status'],'checks':checks,'maxima':{'projector_constraint_normalized':F(projmax),'traceless_normalized':F(tr),'regression_relative':F(reg),'min_abs_denominator':F(mind),'abs_A2_k2_over_J':s5a['domain_ratio_measurement_only']['abs_A2_k2_over_J']},'record':{'k':F(k),'projector':{'psi_pref':F(s['psi']),'psi_pref_prime':F(s['psip']),'phi_pref':F(s['phi']),'B_pref':F(s['B']),'Psi_N':F(s['PsiN']),'Phi_N':F(cl['PhiN']),'V_N':F(s['VN']),'A_residual_normalized':F(s['res']['A']),'Hamiltonian_residual_normalized':F(s['res']['Hamiltonian']),'momentum_residual_normalized':F(s['res']['momentum']),'traceless_residual_normalized':F(cl['res_phi']),'D_A':F(s['DA']),'lapse_denominator':F(s['lapse']),'B_denominator':F(s['Bden']),'shear_feedback_denominator':F(cl['feedback_denominator'])},'carrier':carrier,'ur_l_ge_3':hc,'legacy_nlde_auxiliaries_excluded':True,'historical_CLASS_metric_consumed':False},'completed_carrier_vs_legacy_observer_measurement_only':diag,'interpretation':t['interpretation_if_pass'] if passed else 'The frozen near-horizon inherited-seed algebraic audit failed; do not use k=0.01 for production feedback.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s5b without weakening frozen criteria.','non_claims':t['non_claims'],'threshold_changed':False}
    pth=ROOT/'research/theory_results/RTK_C10_65S5B_NEXT_K_COMPLETED_ONSET_SEED_DOMAIN_AUDIT_RESULT_v1.json';pth.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n');print(out['classification']);print(json.dumps(out['maxima'],sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
