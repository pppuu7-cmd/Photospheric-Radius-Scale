#!/usr/bin/env python3
from __future__ import annotations
import json,math,pathlib,sys
P=pathlib.Path

def L(p): return json.load(open(p))
def rel(a,b):
    a=float(a); b=float(b)
    return abs(a-b)/max(abs(a),abs(b),1e-300)
def finite(*xs): return all(math.isfinite(float(x)) for x in xs)

def dbi_w_ca2_from_w_lambda(w_target,lam):
    # On the certified early DBI branch x is large and w(x) is monotone down.
    # Native production must use khr_background(); this inversion is audit-only.
    def vals(x):
        s=math.hypot(1.0,math.sqrt(lam)*x)
        w=x/(s*(s+1.0+x))
        ca2=x/(s*s*(s+x))
        return w,ca2,s
    lo,hi=1.0,1e30
    wlo=vals(lo)[0]; whi=vals(hi)[0]
    if not (wlo>w_target>whi): raise RuntimeError('target w not bracketed on large-x DBI branch')
    for _ in range(240):
        mid=math.sqrt(lo*hi); wm=vals(mid)[0]
        if wm>w_target: lo=mid
        else: hi=mid
    x=math.sqrt(lo*hi); w,ca2,s=vals(x)
    return x,w,ca2,s

def main():
    target=L('research/theory_targets/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_TARGET_v1.json')
    s2=L('research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json')
    s2a=L('research/theory_results/RTK_C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_RESULT_v1.json')
    s1=L('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    action=L('research/theory_results/RTK_C10_PREFERRED_KHRONON_ACTION_FLUID_EVOLUTION_RESULT_v1.json')
    srcmap=L('research/theory_results/RTK_C10_U1_NEWTONIAN_SOURCE_TRANSFORM_POLE_AUDIT_RESULT_v1.json')
    current=L('research/state/current.json')
    assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert s2['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert s2a['classification']=='C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_PASS_SCOPED'
    assert s1['classification']=='C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_PASS_SCOPED'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    assert action['classification']=='C10_PREFERRED_KHRONON_ACTION_FLUID_EVOLUTION_PASS_SCOPED'
    assert srcmap['classification']=='C10_U1_NEWTONIAN_SOURCE_TRANSFORM_AND_POLE_AUDIT_PASS_SCOPED'

    dom=target['frozen_domain']; ks=[float(x) for x in dom['k_Mpc_inv']]
    H=float(n['background']['H']); w=float(n['background']['w_khr'])
    lamD=float(current['final_replay_result']['rtk']['params']['lam'])
    x,w_recon,ca2,s=dbi_w_ca2_from_w_lambda(w,lamD)
    wprime=-3.0*H*(1.0+w)*(ca2-w)

    np=next(p for p in n['points'] if float(p['lambda_HL'])==float(dom['lambda_HL']) and float(p['M_c_Mpc_inv'])==float(dom['M_c_Mpc_inv']))
    nr=sorted(np['finite_records'],key=lambda r:ks.index(float(r['k'])))
    ar=sorted(s2a['manifest'],key=lambda r:ks.index(float(r['k'])))
    assert len(nr)==len(ar)==4

    records=[]; max_state=0.; max_delta_routes=0.; max_theta_identity=0.; min_direct_delta=1e300
    allfinite=True
    for q,m in zip(nr,ar):
        k=float(m['k']); assert k==float(q['k'])
        st=m['state']; rhs=m['certified_first_rhs']
        B=float(rhs['c10_65r2_B_general']); Bp=float(rhs['c10_65r2_B_prime'])
        PsiNp=float(rhs['c10_65r2_Psi_N_prime'])
        dprefp=float(rhs['c10_65r2_delta_khr_prime_shadow'])
        thprefp=float(rhs['c10_65r2_theta_khr_prime_shadow'])
        delta_pref=float(q['delta_khr_pref']); theta_pref=k*k*float(q['Vpref']); psip=float(q['psip'])
        deltaN=float(st['delta_cdm_khr']); thetaN=float(st['theta_cdm_khr'])

        deltaN_map=delta_pref-3.0*(1.0+w)*H*B
        thetaN_map=theta_pref+k*k*B
        state_err=max(rel(deltaN_map,deltaN),rel(thetaN_map,thetaN))
        max_state=max(max_state,state_err)

        Hprime=(psip-PsiNp-H*Bp)/B
        deltaN_charge=-3.0*H*(ca2-w)*deltaN-(1.0+w)*thetaN+3.0*(1.0+w)*PsiNp
        deltaN_mapprime=dprefp-3.0*(wprime*H*B+(1.0+w)*Hprime*B+(1.0+w)*H*Bp)
        delta_routes=rel(deltaN_charge,deltaN_mapprime); max_delta_routes=max(max_delta_routes,delta_routes)

        thetaN_prime=thprefp+k*k*Bp
        theta_identity=rel(thetaN_prime-thprefp,k*k*Bp); max_theta_identity=max(max_theta_identity,theta_identity)
        direct_delta=rel(deltaN_charge,dprefp); min_direct_delta=min(min_direct_delta,direct_delta)
        direct_theta=rel(thetaN_prime,thprefp)
        allfinite &= finite(deltaN_map,thetaN_map,Hprime,deltaN_charge,deltaN_mapprime,thetaN_prime)
        records.append({
          'k':k,'B':B,'B_prime':Bp,'Hc':H,'Hc_prime_reconstructed':Hprime,
          'w':w,'ca2_audit_reconstructed':ca2,'w_prime':wprime,
          'delta_pref':delta_pref,'theta_pref':theta_pref,'delta_N_state':deltaN,'theta_N_state':thetaN,
          'delta_N_from_map':deltaN_map,'theta_N_from_map':thetaN_map,'state_map_max_relative':state_err,
          'delta_pref_prime_certified':dprefp,'theta_pref_prime_certified':thprefp,
          'Psi_N_prime_certified':PsiNp,'delta_N_prime_from_charge':deltaN_charge,
          'delta_N_prime_from_differentiated_map':deltaN_mapprime,'delta_rhs_two_route_relative':delta_routes,
          'theta_N_prime_transformed':thetaN_prime,'theta_transform_identity_relative':theta_identity,
          'direct_preferred_delta_rhs_relative_mismatch':direct_delta,
          'direct_preferred_theta_rhs_relative_mismatch':direct_theta
        })

    fc=target['frozen_checks']
    checks={
      'state_coordinate_map':max_state<=float(fc['max_state_coordinate_map_relative']),
      'delta_rhs_two_route':max_delta_routes<=float(fc['max_delta_rhs_two_route_relative']),
      'theta_rhs_transform_identity':max_theta_identity<=float(fc['max_theta_rhs_transform_identity_relative']),
      'all_transformed_rhs_finite':allfinite,
      'direct_preferred_delta_rhs_mismatch_macroscopic':min_direct_delta>=float(fc['min_direct_preferred_delta_rhs_relative_mismatch']),
      's2_target_still_frozen':s2['status']=='FROZEN_BEFORE_IMPLEMENTATION',
      'dbi_w_reconstruction':rel(w_recon,w)<1e-12
    }
    passed=all(checks.values())
    out={
      'schema':'RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1','gate':'C10.65s2b',
      'classification':target['pass_classification'] if passed else target['fail_classification'],
      'target':'research/theory_targets/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_TARGET_v1.json',
      'checks':checks,
      'background_audit':{'Hc':H,'w':w,'lambda_D':lamD,'x_large_branch_reconstructed':x,'s':s,'ca2':ca2,'w_reconstruction_relative':rel(w_recon,w),'production_policy':'use native khr_background; inversion here is independent audit only'},
      'global':{'max_state_coordinate_map_relative':max_state,'max_delta_rhs_two_route_relative':max_delta_routes,'max_theta_rhs_transform_identity_relative':max_theta_identity,'min_direct_preferred_delta_rhs_relative_mismatch':min_direct_delta},
      'records':records,
      'production_bridge_contract':{
        'delta_cdm_slot_prime':'-3 H(c_a^2-w) delta_N -(1+w) theta_N +3(1+w) Psi_N_prime',
        'theta_cdm_slot_prime':'theta_pref_prime + k^2 B_prime',
        'preferred_shadow_derivatives_may_not_be_written_directly_to_newtonian_slots':True,
        'legacy_khr_perturb_derivs_newtonian_not_promoted_to_completed_action_rhs':True
      },
      'threshold_changed':False,'next':target['next_if_pass'] if passed else 'Do not execute C10.65s2; resolve coordinate bridge discrepancy first.',
      'non_claims':target['non_claims']}
    P('research/theory_results/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'])
    print(json.dumps(out['global'],sort_keys=True))
    return 0 if passed else 2
if __name__=='__main__': sys.exit(main())
