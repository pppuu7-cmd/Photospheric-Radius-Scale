#!/usr/bin/env python3
from __future__ import annotations
import inspect,json,math,pathlib,sys
P=pathlib.Path
ROOT=P(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/shadow'))
from rtk_c10_65s2c_current_state_dae_metric_core import current_state_metric_core
from rtk_c10_65s2d_current_state_traceless_tca_closure import current_state_traceless_tca
from rtk_c10_65s2e_current_state_derivative_slip_closure import dynamic_derivative_slip

def L(p): return json.loads((ROOT/p).read_text())
def rel(a,b):
    a=float(a); b=float(b); return abs(a-b)/max(abs(a),abs(b),1e-300)
def finite_values(d): return all(math.isfinite(float(v)) for v in d.values())

def main():
    t=L('research/theory_targets/RTK_C10_65S4C_MODERATE_K_CURRENT_STATE_FIRST_RHS_PARITY_TARGET_v2.json')
    old=L('research/theory_targets/RTK_C10_65S4C_MODERATE_K_CURRENT_STATE_FIRST_RHS_PARITY_TARGET_v1.json')
    s4b=L('research/theory_results/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_RESULT_v1.json')
    s2c=L('research/theory_results/RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_RESULT_v1.json')
    s2d=L('research/theory_results/RTK_C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_RESULT_v1.json')
    s2e=L('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json')
    s2f=L('research/theory_results/RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_RESULT_v1.json')
    s2g=L('research/theory_results/RTK_C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_RESULT_v1.json')
    s2b=L('research/theory_results/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    cur=L('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert t['scientific_contract_changed_from_v1'] is False
    # Numerical/domain contract is byte-for-value identical to v1; only parent provenance is corrected.
    assert t['domain']==old['domain']
    for k in ['record_count','max_B_relative_vs_s4b','max_Psi_N_relative_vs_s4b','max_Phi_N_relative_vs_s4b',
              'max_preferred_A_Hamiltonian_momentum_normalized_residual','max_physical_traceless_normalized_residual',
              'max_weighted_photon_baryon_slip_cancellation','all_first_rhs_outputs_finite','all_algebraic_denominators_nonzero',
              'historical_metric_not_consumed','legacy_nlde_auxiliaries_excluded','threshold_changed']:
        assert t['frozen_checks'][k]==old['frozen_checks'][k]
    assert s4b['classification']=='C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_PASS_SCOPED'
    assert s2c['classification']=='C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_PASS_SCOPED'
    assert s2d['classification']=='C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_PASS_SCOPED'
    assert s2e['classification']=='C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_FAIL_SCOPED'
    assert s2f['classification']=='C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_PASS_SCOPED'
    assert s2f['failed_parent_classification_preserved']==s2e['classification']
    assert s2g['classification']=='C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_PASS_SCOPED'
    assert s2g['failed_s2e_classification_preserved']==s2e['classification']

    bg=n['background']; a=float(bg['a']); H=float(bg['H']); rb=float(bg['rhob']); rg=float(bg['rhog']); ru=float(bg['rhour']); rk=float(bg['rho_khr']); pk=float(bg['p_khr'])
    pack=f['coefficient_pack']; cb2=float(pack['cb2']); tau=float(pack['tau_c_Mpc']); dtau=float(pack['dtau_c'])
    Hps=[float(q['Hc_prime_reconstructed']) for q in s2b['records']]; Hprime=sum(Hps)/len(Hps); assert max(Hps)-min(Hps)<1e-15
    lamD=float(cur['final_replay_result']['rtk']['params']['lam']); xbg=float(s2b['background_audit']['x_large_branch_reconstructed']); sbg=math.hypot(1.0,math.sqrt(lamD)*xbg)
    ca2=xbg/(sbg*sbg*(sbg+xbg)); tt=xbg/(sbg+1.0); Q=1.0+xbg/sbg; mu2=3.0*rk/(2.0*xbg*(1.0+tt)); MK=math.sqrt(mu2)*Q*sbg*math.sqrt(sbg); kstar=a*MK; w=pk/rk

    lam=float(t['domain']['lambda_HL']); Mc=float(t['domain']['M_c_Mpc_inv'])
    assert rel(a,t['domain']['a_on'])<1e-12
    byk={float(r['k']):r for r in s4b['records']}
    records=[]; maxima={'B':0.0,'Psi_N':0.0,'Phi_N':0.0,'preferred_A_H_M':0.0,'traceless':0.0,'weighted_slip_cancel':0.0}; min_den=float('inf'); finite_all=True
    rhs_keys=['B_prime','Psi_N_prime','metric_continuity','metric_euler','tca_slip','theta_b_prime','theta_g_prime','theta_ur_prime','delta_khr_pref_prime','theta_khr_pref_prime','delta_khr_N_prime','theta_khr_N_prime']
    for k in map(float,t['domain']['k_Mpc_inv']):
        ref=byk[k]; st=ref['carrier']
        db=float(st['delta_b']);tb=float(st['theta_b']);dg=float(st['delta_g']);tg=float(st['theta_g']);du=float(st['delta_ur']);tu=float(st['theta_ur']);sur=float(st['shear_ur']);dk=float(st['delta_cdm_khr']);tk=float(st['theta_cdm_khr']);Psi=float(st['phi_CLASS_equals_Psi_N'])
        core=current_state_metric_core(k=k,a=a,H=H,rb=rb,rg=rg,ru=ru,rk=rk,pk=pk,lam=lam,Mc=Mc,PsiN=Psi,db=db,tb=tb,dg=dg,tg=tg,du=du,tu=tu,dkN=dk,tkN=tk)
        tr=current_state_traceless_tca(k=k,a=a,H=H,rb=rb,rg=rg,ru=ru,cb2=cb2,tau_c=tau,dtau_c=dtau,PsiN=core['Psi_N'],delta_b=db,theta_b=tb,delta_g=dg,theta_g=tg,sigma_ur=sur)
        cs2=ca2/(1.0+(k/kstar)*(k/kstar))
        dyn=dynamic_derivative_slip(k=k,a=a,H=H,Hprime=Hprime,rb=rb,rg=rg,ru=ru,rk=rk,pk=pk,lam=lam,Mc=Mc,cb2=cb2,tau=tau,dtau=dtau,PsiN=Psi,db=db,tb=tb,dg=dg,tg=tg,du=du,tu=tu,sigma_ur=sur,dkN=dk,thetaN=tk,w=w,ca2=ca2,cs2=cs2)
        errs={'B':rel(core['B'],ref['projector']['B_pref']),'Psi_N':rel(core['Psi_N'],ref['projector']['Psi_N']),'Phi_N':rel(tr['Phi_N'],ref['projector']['Phi_N'])}
        for q in ['B','Psi_N','Phi_N']: maxima[q]=max(maxima[q],errs[q])
        ahm=max(core['A_residual_normalized'],core['Hamiltonian_residual_normalized'],core['momentum_residual_normalized']); maxima['preferred_A_H_M']=max(maxima['preferred_A_H_M'],ahm); maxima['traceless']=max(maxima['traceless'],tr['traceless_residual_normalized']); maxima['weighted_slip_cancel']=max(maxima['weighted_slip_cancel'],dyn['weighted_slip_cancel'])
        dens={'filter':core['filter_denominator'],'D_A':core['D_A'],'B':core['B_denominator'],'lapse':core['lapse_denominator'],'shear_feedback':tr['feedback_denominator'],'Bprime_implicit':dyn['Bprime_implicit_denominator']}
        min_den=min(min_den,*(abs(float(v)) for v in dens.values()))
        finite_all &= all(math.isfinite(float(dyn[q])) for q in rhs_keys) and all(math.isfinite(float(v)) for v in core.values()) and all(math.isfinite(float(v)) for v in tr.values())
        records.append({'k':k,'lambda_HL':lam,'M_c_Mpc_inv':Mc,'cs2':cs2,'metric_relative_errors_vs_s4b':errs,'preferred_residuals':{'A':core['A_residual_normalized'],'Hamiltonian':core['Hamiltonian_residual_normalized'],'momentum':core['momentum_residual_normalized']},'traceless_residual_normalized':tr['traceless_residual_normalized'],'weighted_photon_baryon_slip_cancellation':dyn['weighted_slip_cancel'],'denominators':dens,'first_rhs':{q:dyn[q] for q in rhs_keys},'current_metric':{'B':core['B'],'Psi_N':core['Psi_N'],'Phi_N':tr['Phi_N']},'s4b_metric':{'B':ref['projector']['B_pref'],'Psi_N':ref['projector']['Psi_N'],'Phi_N':ref['projector']['Phi_N']},'historical_CLASS_metric_consumed':False,'legacy_nlde_auxiliaries_excluded':bool(ref['legacy_nlde_auxiliaries_excluded'])})

    fc=t['frozen_checks']; dynsrc=inspect.getsource(dynamic_derivative_slip); coresrc=inspect.getsource(current_state_metric_core); trsrc=inspect.getsource(current_state_traceless_tca)
    forbidden=['A2','C2','J_ad','S_ur0']
    source_clean=all(x not in dynsrc+coresrc+trsrc for x in forbidden)
    checks={
      'record_count':len(records)==int(fc['record_count']),
      'B':maxima['B']<=float(fc['max_B_relative_vs_s4b']),
      'Psi_N':maxima['Psi_N']<=float(fc['max_Psi_N_relative_vs_s4b']),
      'Phi_N':maxima['Phi_N']<=float(fc['max_Phi_N_relative_vs_s4b']),
      'preferred_A_H_M':maxima['preferred_A_H_M']<=float(fc['max_preferred_A_Hamiltonian_momentum_normalized_residual']),
      'traceless':maxima['traceless']<=float(fc['max_physical_traceless_normalized_residual']),
      'weighted_slip_cancel':maxima['weighted_slip_cancel']<=float(fc['max_weighted_photon_baryon_slip_cancellation']),
      'first_rhs_finite':finite_all,
      'algebraic_denominators_nonzero':min_den>0.0 and math.isfinite(min_den),
      'historical_metric_not_consumed':source_clean and all(not r['historical_CLASS_metric_consumed'] for r in records),
      'legacy_nlde_auxiliaries_excluded':all(r['legacy_nlde_auxiliaries_excluded'] for r in records),
      's2e_failed_parent_preserved':s2e['classification']=='C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_FAIL_SCOPED',
      's2f_conditioning_pass':s2f['classification']=='C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_PASS_SCOPED',
      's2g_kernel_preflight_pass':s2g['classification']=='C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_PASS_SCOPED',
      'threshold_changed':False}
    passed=(checks['threshold_changed'] is False and all(v for k,v in checks.items() if k!='threshold_changed'))
    out={'schema':'RTK_C10_65S4C_MODERATE_K_CURRENT_STATE_FIRST_RHS_PARITY_RESULT_v2','gate':'C10.65s4c','classification':t['pass_classification'] if passed else t['fail_classification'],'target':'research/theory_targets/RTK_C10_65S4C_MODERATE_K_CURRENT_STATE_FIRST_RHS_PARITY_TARGET_v2.json','superseded_target_v1_preserved':True,'checks':checks,'maxima':maxima,'min_abs_algebraic_denominator':min_den,'background':{'a':a,'Hc':H,'Hc_prime':Hprime,'w_khr':w,'ca2_khr':ca2,'kstar_Mpc_inv':kstar},'records':records,'threshold_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'The corrected frozen moderate-k first-RHS parity gate failed; do not open s4d.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s4c without changing the frozen scientific contract.','non_claims':t['non_claims']}
    outp=ROOT/'research/theory_results/RTK_C10_65S4C_MODERATE_K_CURRENT_STATE_FIRST_RHS_PARITY_RESULT_v2.json';outp.write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n')
    print(out['classification']);print(json.dumps({'maxima':maxima,'min_abs_algebraic_denominator':min_den},sort_keys=True));return 0 if passed else 2
if __name__=='__main__': sys.exit(main())
