#!/usr/bin/env python3
from __future__ import annotations
import inspect,json,math,pathlib,sys
P=pathlib.Path

def L(p): return json.load(open(p))
def rel(a,b):
    a=float(a); b=float(b); return abs(a-b)/max(abs(a),abs(b),1e-300)
def nres(res,*terms): return abs(res)/max(*(abs(float(x)) for x in terms),1e-300)

def current_state_metric_core(*,k,a,H,rb,rg,ru,rk,pk,lam,Mc,PsiN,db,tb,dg,tg,du,tu,dkN,tkN,E=2.0,Pcal=1.0):
    x=k*k; Lk=-x; r=lam-1.0; D=3.0*lam-1.0
    Wg=(4.0/3.0)*rg; Wu=(4.0/3.0)*ru; W0=rb+Wg+Wu; Wk=rk+pk; W=W0+Wk
    Db=db-3.0*PsiN; Dg=dg-4.0*PsiN; Dur=du-4.0*PsiN
    h=rb*Db+rg*Dg+ru*Dur
    ph=(rg*Dg+ru*Dur)/3.0
    den_filter=x+a*a*Mc*Mc
    K=-1.5*a*a/den_filter; a1=x/den_filter; Kp=2.0*H*a1*K
    W0p=-3.0*H*rb-4.0*H*(Wg+Wu)
    DA=1.0-3.0*K*W0; DAp=-3.0*(Kp*W0+K*W0p)
    psi=K*h/DA
    q0N=a*(rb*tb+Wg*tg+Wu*tu)/x
    hp=-3.0*H*(h+ph)-(x/a)*q0N
    psip=(Kp*h+K*hp-DAp*psi)/DA
    dm0=h+3.0*W0*psi+rk*dkN
    Q0=3.0*a*(q0N+a*Wk*tkN/x)
    X0=3.0*a*a*W0; Xt=3.0*a*a*W
    Bnum=E*Lk*(Q0-D*psip)+3.0*D*H*H*Q0+3.0*D*H*a*a*dm0-2.0*D*Pcal*Lk*H*psi
    Bden=r*E*Lk*Lk-2.0*D*Lk*H*H+E*Lk*Xt+3.0*D*H*H*X0
    B=Bnum/Bden
    dm=dm0+3.0*H*Wk*B
    Qpref=Q0-Xt*B
    lapse=r*E*Lk-2.0*D*H*H
    Hrhs=-3.0*a*a*r*dm-D*H*Qpref+2.0*D*H*psip+2.0*r*Pcal*Lk*psi
    phi=Hrhs/lapse
    Psi_rec=psi-H*B
    Ares=DA*psi-K*h
    Hres=lapse*phi-Hrhs
    Mleft=r*Lk*B; Mq=Qpref; Mgrav=D*(psip+H*phi)
    Mres=Mleft-Mq+Mgrav
    return {
      'B':B,'psi_pref':psi,'psi_pref_prime':psip,'phi_pref':phi,'Psi_N':Psi_rec,
      'D_b':Db,'D_g':Dg,'D_ur':Dur,'h':h,'p_hat0':ph,'q0_N':q0N,
      'delta_mu_pref':dm,'Q_pref':Qpref,'D_A':DA,'filter_denominator':den_filter,
      'B_denominator':Bden,'lapse_denominator':lapse,
      'A_residual':Ares,'A_residual_normalized':nres(Ares,DA*psi,K*h),
      'Hamiltonian_residual':Hres,'Hamiltonian_residual_normalized':nres(Hres,lapse*phi,-3*a*a*r*dm,-D*H*Qpref,2*D*H*psip,2*r*Pcal*Lk*psi),
      'momentum_residual':Mres,'momentum_residual_normalized':nres(Mres,Mleft,Mq,Mgrav)
    }

def main():
    target=L('research/theory_targets/RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_TARGET_v1.json')
    s2b=L('research/theory_results/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1.json')
    s1=L('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert s2b['classification']=='C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_PASS_SCOPED'
    assert s1['classification']=='C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_PASS_SCOPED'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    bg=n['background']; a=float(bg['a']); H=float(bg['H']); rb=float(bg['rhob']); rg=float(bg['rhog']); ru=float(bg['rhour']); rk=float(bg['rho_khr']); pk=float(bg['p_khr'])

    srows={(float(q['lambda_HL']),float(q['M_c_Mpc_inv']),float(q['k'])):q for q in s1['completed_states']}
    records=[]; maxima={q:0.0 for q in ['B','psi','psip','phi','PsiN','A','H','M']}; finite_all=True; den_ok=True
    for pt in n['points']:
        lam=float(pt['lambda_HL']); Mc=float(pt['M_c_Mpc_inv'])
        for ex in pt['finite_records']:
            k=float(ex['k']); st=srows[(lam,Mc,k)]
            z=current_state_metric_core(k=k,a=a,H=H,rb=rb,rg=rg,ru=ru,rk=rk,pk=pk,lam=lam,Mc=Mc,
              PsiN=float(st['phi_CLASS']),db=float(st['delta_b']),tb=float(st['theta_b']),dg=float(st['delta_g']),tg=float(st['theta_g']),du=float(st['delta_ur']),tu=float(st['theta_ur']),dkN=float(st['delta_cdm_khr']),tkN=float(st['theta_cdm_khr']))
            errs={
              'B':rel(z['B'],ex['B']),'psi':rel(z['psi_pref'],ex['psi']),'psip':rel(z['psi_pref_prime'],ex['psip']),
              'phi':rel(z['phi_pref'],ex['phi']),'PsiN':rel(z['Psi_N'],st['phi_CLASS']),
              'A':z['A_residual_normalized'],'H':z['Hamiltonian_residual_normalized'],'M':z['momentum_residual_normalized']}
            for q,v in errs.items(): maxima[q]=max(maxima[q],v)
            vals=[z['B'],z['psi_pref'],z['psi_pref_prime'],z['phi_pref'],z['Psi_N'],z['delta_mu_pref'],z['Q_pref']]
            finite_all &= all(math.isfinite(x) for x in vals)
            den_ok &= all(math.isfinite(z[q]) and z[q]!=0.0 for q in ['filter_denominator','D_A','B_denominator','lapse_denominator'])
            records.append({'lambda_HL':lam,'M_c_Mpc_inv':Mc,'k':k,'errors':errs,
              'core':{q:z[q] for q in ['B','psi_pref','psi_pref_prime','phi_pref','Psi_N','delta_mu_pref','Q_pref','D_A','filter_denominator','B_denominator','lapse_denominator','A_residual','Hamiltonian_residual','momentum_residual']},
              'expected':{'B':ex['B'],'psi_pref':ex['psi'],'psi_pref_prime':ex['psip'],'phi_pref':ex['phi'],'Psi_N':st['phi_CLASS']}})

    fc=target['frozen_checks']
    core_src=inspect.getsource(current_state_metric_core)
    forbidden=fc['forbidden_hard_coded_seed_inputs']
    forbidden_absent=all(x not in core_src for x in forbidden)
    checks={
      'record_count':len(records)==int(fc['grid_point_count'])*int(fc['anchor_count_per_point']),
      'B':maxima['B']<=float(fc['max_B_relative_vs_C10_65n']),
      'psi':maxima['psi']<=float(fc['max_psi_pref_relative_vs_C10_65n']),
      'psip':maxima['psip']<=float(fc['max_psi_pref_prime_relative_vs_C10_65n']),
      'phi':maxima['phi']<=float(fc['max_phi_pref_relative_vs_C10_65n']),
      'PsiN':maxima['PsiN']<=float(fc['max_Psi_N_relative_vs_integrated_state']),
      'A_residual':maxima['A']<=float(fc['max_normalized_A_residual']),
      'Hamiltonian_residual':maxima['H']<=float(fc['max_normalized_Hamiltonian_residual']),
      'momentum_residual':maxima['M']<=float(fc['max_normalized_momentum_residual']),
      'denominators':den_ok,'finite':finite_all,'hard_coded_seed_inputs_absent_from_core':forbidden_absent}
    passed=all(checks.values())
    out={'schema':'RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_RESULT_v1','gate':'C10.65s2c','classification':target['pass_classification'] if passed else target['fail_classification'],
      'target':'research/theory_targets/RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_TARGET_v1.json','checks':checks,'maxima':maxima,'record_count':len(records),
      'core_contract':{'inputs':'instantaneous Newtonian physical state + local background + lambda_HL,M_c','hard_coded_matching_coefficients_used':False,
        'traceless_Phi_N_included':False,'neutral_source_map_in_B_denominator':'exact Newtonian->preferred density and momentum coordinate dependence included algebraically'},
      'records':records,'threshold_changed':False,'next':target['next_if_pass'] if passed else 'Do not implement s2 production feedback; resolve the current-state DAE core discrepancy.','non_claims':target['non_claims']}
    P('research/theory_results/RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification']); print(json.dumps(maxima,sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': sys.exit(main())
