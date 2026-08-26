#!/usr/bin/env python3
from __future__ import annotations
import inspect,json,math,pathlib,sys
P=pathlib.Path

def L(p): return json.load(open(p))
def rel(a,b):
    a=float(a); b=float(b); return abs(a-b)/max(abs(a),abs(b),1e-300)
def nres(r,*xs): return abs(float(r))/max(*(abs(float(x)) for x in xs),1e-300)

def current_state_traceless_tca(*,k,a,H,rb,rg,ru,cb2,tau_c,dtau_c,PsiN,delta_b,theta_b,delta_g,theta_g,sigma_ur):
    k2=k*k
    R=(4.0/3.0)*rg/rb
    Wg=(4.0/3.0)*rg; Wur=(4.0/3.0)*ru
    c=(16.0/45.0)*tau_c
    theta0p=(-H*theta_b+k2*(cb2*delta_b+R*delta_g/4.0))/(1.0+R)
    pref=1.0-(11.0/6.0)*dtau_c
    sec=(11.0/6.0)*tau_c*c
    sigma_A=pref*c*theta_g-sec*theta0p
    sigma_Phi=-sec*k2
    Pi_A=1.5*(Wg*sigma_A+Wur*sigma_ur)/k2
    Pi_Phi=1.5*Wg*sigma_Phi/k2
    den=1.0+3.0*a*a*Pi_Phi
    Phi=(PsiN-3.0*a*a*Pi_A)/den
    sigma_g=sigma_A+sigma_Phi*Phi
    Pi=1.5*(Wg*sigma_g+Wur*sigma_ur)/k2
    res=Phi-(PsiN-3.0*a*a*Pi)
    return {'Phi_N':Phi,'sigma_g':sigma_g,'sigma_g_over_k2':sigma_g/k2,'Pi':Pi,
            'theta0_prime':theta0p,'sigma_A':sigma_A,'sigma_Phi':sigma_Phi,
            'Pi_A':Pi_A,'Pi_Phi':Pi_Phi,'feedback_denominator':den,
            'metric_euler':k2*Phi,'traceless_residual':res,
            'traceless_residual_normalized':nres(res,Phi,PsiN,3*a*a*Pi)}

def main():
    t=L('research/theory_targets/RTK_C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_TARGET_v1.json')
    c=L('research/theory_results/RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_RESULT_v1.json')
    o=L('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    s1=L('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json')
    r2=L('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    d=L('research/theory_results/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert c['classification']=='C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_PASS_SCOPED'
    assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'
    assert s1['classification']=='C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_PASS_SCOPED'
    assert r2['classification']=='C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_PASS_SCOPED'
    assert d['classification']=='C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_PASS_SCOPED'
    bg=n['background']; a=float(bg['a']); H=float(bg['H']); rb=float(bg['rhob']); rg=float(bg['rhog']); ru=float(bg['rhour'])
    pack=f['coefficient_pack']; cb2=float(pack['cb2']); tau=float(pack['tau_c_Mpc']); dtau=float(pack['dtau_c'])
    assert all(bool(x['predicted_tca_on']) for x in f['tca_domain']['records'] if float(x['k_Mpc_inv']) in [1e-5,3e-5,1e-4,3e-4])

    states={(float(q['lambda_HL']),float(q['M_c_Mpc_inv']),float(q['k'])):q for q in s1['completed_states']}
    cores={(float(q['lambda_HL']),float(q['M_c_Mpc_inv']),float(q['k'])):q for q in c['records']}
    expected={}
    for pt in o['points']:
        for q in pt['finite_records']:
            expected[(float(pt['lambda_HL']),float(pt['M_c_Mpc_inv']),float(q['k']))]=q
    r2map={}
    for pt in r2['points']:
        for q in pt['records']:
            r2map[(float(pt['lambda_HL']),float(pt['M_c_Mpc_inv']),float(q['k']))]=q
    assert len(states)==len(cores)==len(expected)==len(r2map)==36

    maxima={'Phi_N':0.0,'sigma_g':0.0,'metric_euler':0.0,'traceless_residual':0.0}; min_den=float('inf'); finite_all=True; rec=[]
    for key,st in states.items():
        cr=cores[key]; ex=expected[key]; rr=r2map[key]; k=key[2]
        z=current_state_traceless_tca(k=k,a=a,H=H,rb=rb,rg=rg,ru=ru,cb2=cb2,tau_c=tau,dtau_c=dtau,
             PsiN=float(cr['core']['Psi_N']),delta_b=float(st['delta_b']),theta_b=float(st['theta_b']),delta_g=float(st['delta_g']),theta_g=float(st['theta_g']),sigma_ur=float(st['shear_ur']))
        ePhi=rel(z['Phi_N'],ex['PhiN']); esg=rel(z['sigma_g_over_k2'],ex['sigma_g_over_k2'])
        em=rel(z['metric_euler'],float(rr['C']['c10_65r2_metric_euler_shadow']))
        maxima['Phi_N']=max(maxima['Phi_N'],ePhi); maxima['sigma_g']=max(maxima['sigma_g'],esg); maxima['metric_euler']=max(maxima['metric_euler'],em); maxima['traceless_residual']=max(maxima['traceless_residual'],z['traceless_residual_normalized'])
        min_den=min(min_den,abs(z['feedback_denominator'])); finite_all &= all(math.isfinite(float(v)) for v in z.values())
        rec.append({'lambda_HL':key[0],'M_c_Mpc_inv':key[1],'k':k,'errors':{'Phi_N':ePhi,'sigma_g_over_k2':esg,'metric_euler':em},'dynamic':z,'expected':{'PhiN':ex['PhiN'],'sigma_g_over_k2':ex['sigma_g_over_k2'],'metric_euler':rr['C']['c10_65r2_metric_euler_shadow']}})

    fc=t['frozen_checks']; src=inspect.getsource(current_state_traceless_tca)
    forbidden=['A2','C2','J_ad','S_ur0']
    checks={'record_count':len(rec)==36,'Phi_N':maxima['Phi_N']<=float(fc['max_Phi_N_relative_vs_C10_65o']),
      'sigma_g':maxima['sigma_g']<=float(fc['max_sigma_g_relative_vs_C10_65o']),
      'metric_euler':maxima['metric_euler']<=float(fc['max_metric_euler_relative_vs_C10_65r2']),
      'traceless':maxima['traceless_residual']<=float(fc['max_traceless_normalized_residual']),
      'feedback_denominator':min_den>=float(fc['min_abs_feedback_denominator']),'finite':finite_all,
      'no_seed_constants':all(x not in src for x in forbidden),'sigma_ur_current_state_argument':'sigma_ur' in src}
    passed=all(checks.values())
    out={'schema':'RTK_C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_RESULT_v1','gate':'C10.65s2d','classification':t['pass_classification'] if passed else t['fail_classification'],
      'target':'research/theory_targets/RTK_C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_TARGET_v1.json','checks':checks,'maxima':maxima,'min_abs_feedback_denominator':min_den,'record_count':len(rec),
      'source_lock':{'class_upstream_sha':d['pinned_upstream']['sha'],'tca':'compromise_CLASS','formula':'exact pinned compromise_CLASS current-state shear specialization in flat Newtonian gauge'},
      'dynamic_contract':{'inputs':'current Psi_N, photon/baryon state, current sigma_ur, local thermodynamics/background','historical_metric_consumed':False,'hard_coded_matching_coefficients_used':False},
      'records':rec,'threshold_changed':False,'next':t['next_if_pass'] if passed else 'Do not implement s2; resolve dynamic traceless/TCA mismatch.','non_claims':t['non_claims']}
    P('research/theory_results/RTK_C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification']); print(json.dumps({'maxima':maxima,'min_den':min_den},sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': sys.exit(main())
