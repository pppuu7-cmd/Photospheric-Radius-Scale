#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research/shadow'))
import rtk_c10_65n_conditional_completed_u1_onset_seed_preflight as N
import rtk_c10_65o_radiation_shear_metric_closure as O
mp.mp.dps=90
M=N.M; F=N.F

def load(p): return json.loads((ROOT/p).read_text())
def rel(a,b):
    a=M(a); b=M(b); return abs(a-b)/max(abs(a),abs(b),M('1e-80'))

def main():
    t=load('research/theory_targets/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_TARGET_v1.json')
    s4a=load('research/theory_results/RTK_C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_RESULT_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    m=load('research/theory_results/RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json')
    state=load('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert s4a['classification']=='C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_PASS_SCOPED'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'
    assert m['classification']=='C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_PASS_SCOPED'
    ctl=m['phenomenological_regular_control_vector']; J=M('-3'); A2=M(ctl['A2']); C2=M(ctl['C2']); Sur=M(ctl['S_ur0']); Eth=M(2); Pcal=M(1)
    prod=state['final_replay_result']['rtk']['params']; gamma=M(src['provenance']['gamma_root']); bg=N.background(prod,gamma,f)
    q=n['points'][0]; lam=M(q['lambda_HL']); Mc=M(q['M_c_Mpc_inv'])
    assert rel(lam,t['domain']['lambda_HL'])<M('1e-15') and rel(Mc,t['domain']['M_c_Mpc_inv'])<M('1e-15')
    pack=f['coefficient_pack']; R=M(pack['R']); cb2=M(pack['cb2']); tau=M(pack['tau_c_Mpc']); dtau=M(pack['dtau_c'])
    Wg=M(4)/3*bg['rhog']; Wur=M(4)/3*bg['rhour']

    # Regression: same algebra must reproduce the persisted low-k C10.65n/o parent.
    oldks=[M('1e-4'),M('3e-4')]; nmap={M(r['k']):r for r in q['finite_records']}; omap={M(r['k']):r for r in o['points'][0]['finite_records']}
    max_reg=mp.mpf('0')
    for k in oldks:
        s=N.finite_seed(bg,lam,Mc,k,J,A2,C2,Eth,Pcal)
        for name in ('psi','psip','phi','B','PsiN','VN'):
            max_reg=max(max_reg,rel(s[name],nmap[k][name]))
        cl=O.closure(a=bg['a'],H=bg['H'],R=R,cb2=cb2,tau=tau,dtau=dtau,Wg=Wg,Wur=Wur,Sur=Sur,VN=s['VN'],Psi=s['PsiN'],Db=s['Db'],Dg=s['Dg'])
        max_reg=max(max_reg,rel(cl['PhiN'],omap[k]['PhiN']),rel(cl['sigma_g_over_k2'],omap[k]['sigma_g_over_k2']))

    rows_by_k={M(r['k']):r for r in s4a['onset_rows']}
    records=[]; max_projector=mp.mpf('0'); max_trace=mp.mpf('0'); min_den=mp.inf; finite_all=True; labels_ok=True
    for k in map(M,t['domain']['new_k_Mpc_inv']):
        assert k in rows_by_k
        s=N.finite_seed(bg,lam,Mc,k,J,A2,C2,Eth,Pcal)
        cl=O.closure(a=bg['a'],H=bg['H'],R=R,cb2=cb2,tau=tau,dtau=dtau,Wg=Wg,Wur=Wur,Sur=Sur,VN=s['VN'],Psi=s['PsiN'],Db=s['Db'],Dg=s['Dg'])
        max_projector=max(max_projector,abs(s['res']['A']),abs(s['res']['Hamiltonian']),abs(s['res']['momentum']))
        max_trace=max(max_trace,abs(cl['res_phi']))
        min_den=min(min_den,abs(s['DA']),abs(s['lapse']),abs(s['Bden']),abs(cl['feedback_denominator']))
        carrier={
          'phi_CLASS_equals_Psi_N':F(s['PsiN']),
          'delta_b':F(s['Db']+3*s['PsiN']), 'theta_b':F(k*k*s['VN']),
          'delta_g':F(s['Dg']+4*s['PsiN']), 'theta_g':F(k*k*s['VN']),
          'delta_ur':F(s['Dur']+4*s['PsiN']), 'theta_ur':F(k*k*s['VN']),
          'shear_ur':F(k*k*Sur),
          'delta_cdm_khr':F((1+bg['w_khr'])*(s['Jkhr']+3*s['PsiN'])),
          'theta_cdm_khr':F(k*k*s['VN'])}
        hc=[]
        for ls,val in rows_by_k[k]['F_over_kpow'].items():
            l=int(ls)
            if l<3 or l>17: continue
            ratio=M(val); actual=ratio*(k**l)
            hc.append({'l':l,'F_l_over_k_pow_l':F(ratio),'F_l':F(actual),'status':'HIGHER_ORDER_HISTORICAL_CONTROL'})
        labels_ok &= len(hc)==15 and all(x['status']=='HIGHER_ORDER_HISTORICAL_CONTROL' for x in hc)
        vals=list(carrier.values())+[F(s[x]) for x in ('psi','psip','phi','B','PsiN','VN')]+[F(cl['PhiN']),F(cl['sigma_g_over_k2'])]
        finite_all &= all(math.isfinite(x) for x in vals) and all(math.isfinite(x['F_l']) and math.isfinite(x['F_l_over_k_pow_l']) for x in hc)
        records.append({'k':F(k),'projector':{'psi_pref':F(s['psi']),'psi_pref_prime':F(s['psip']),'phi_pref':F(s['phi']),'B_pref':F(s['B']),'Psi_N':F(s['PsiN']),'Phi_N':F(cl['PhiN']),'V_N':F(s['VN']),'A_residual_normalized':F(s['res']['A']),'Hamiltonian_residual_normalized':F(s['res']['Hamiltonian']),'momentum_residual_normalized':F(s['res']['momentum']),'traceless_residual_normalized':F(cl['res_phi']),'D_A':F(s['DA']),'lapse_denominator':F(s['lapse']),'B_denominator':F(s['Bden']),'shear_feedback_denominator':F(cl['feedback_denominator'])},'carrier':carrier,'legacy_nlde_auxiliaries_excluded':True,'historical_CLASS_metric_consumed':False,'ur_l_ge_3':hc})

    checks={
      'new_anchor_count':len(records)==2,
      'all_projector_and_carrier_values_finite':bool(finite_all),
      'preferred_A_Hamiltonian_momentum_normalized_residual_max':bool(max_projector<=M('1e-20')),
      'physical_traceless_normalized_residual_max':bool(max_trace<=M('1e-20')),
      'all_projector_denominators_nonzero':bool(min_den>0),
      'low_k_parent_regression_relative_max':bool(max_reg<=M('1e-12')),
      's4a_domain_guards_inherited_unchanged':bool(s4a['max_k_over_Hc']<=M('0.25') and s4a['max_abs_A2_k2_over_J']<=M('0.005')),
      'legacy_nlde_auxiliaries_excluded':all(r['legacy_nlde_auxiliaries_excluded'] for r in records),
      'historical_metric_not_consumed':all(not r['historical_CLASS_metric_consumed'] for r in records),
      'higher_ur_controls_explicitly_labeled':bool(labels_ok),
      'threshold_changed':False}
    passed=all(checks.values())
    out={'schema':'RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_RESULT_v1','gate':'C10.65s4b','classification':t['pass_classification'] if passed else t['fail_classification'],'target':'research/theory_targets/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_TARGET_v1.json','completion_point':{'lambda_HL':F(lam),'M_c_Mpc_inv':F(Mc)},'control_status':'PRE_EFT_PHENOMENOLOGICAL_CONTROL_ONLY','checks':checks,'maxima':{'projector_constraint_normalized':F(max_projector),'traceless_normalized':F(max_trace),'low_k_parent_regression_relative':F(max_reg),'min_abs_denominator':F(min_den)},'records':records,'interpretation':t['interpretation_if_pass'] if passed else 'The frozen moderate-k completed onset seed gate failed; do not proceed to production/current-state RHS at the new modes.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s4b without weakening the frozen criteria.','non_claims':t['non_claims'],'threshold_changed':False}
    p=ROOT/'research/theory_results/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_RESULT_v1.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',allow_nan=False)
    print(out['classification']);print(json.dumps(out['maxima'],sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__': main()
