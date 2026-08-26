#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def rel(a,b):
    a=float(a); b=float(b); return abs(a-b)/max(1.0,abs(a),abs(b))
def finite(x): return isinstance(x,(int,float)) and math.isfinite(float(x))

def parse(path):
    rows=[]
    names_state=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N']
    names_dy=['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime']
    names_k=['B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip']
    names_r=['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm','feedback_denominator','implicit_denominator']
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',')
        if len(p)!=63: raise RuntimeError(f'C10.65s2 observer columns {len(p)} != 63')
        r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8])}
        j=9
        for n in names_state: r[n]=float(p[j]); j+=1
        for n in names_dy: r[n]=float(p[j]); j+=1
        for n in names_k: r[n]=float(p[j]); j+=1
        for n in names_r: r[n]=float(p[j]); j+=1
        r['Fl']={l:float(p[j+l-3]) for l in range(3,18)}
        rows.append(r)
    return rows

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--observer',required=True); ap.add_argument('--off-identity',required=True); ap.add_argument('--patch',required=True); ap.add_argument('--patch-v2',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json')
    plan=L('research/theory_targets/RTK_C10_65S2_PRODUCTION_IMPLEMENTATION_PLAN_v1.json')
    s1=L('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json')
    r2=L('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json')
    b=L('research/theory_results/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1.json')
    fcond=L('research/theory_results/RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_RESULT_v1.json')
    g=L('research/theory_results/RTK_C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_RESULT_v1.json')
    cimpl=L('research/theory_results/RTK_C10_65S2_C_KERNEL_PARITY_AUDIT_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert plan['status']=='FROZEN_BEFORE_PRODUCTION_EXECUTION'
    assert s1['classification']=='C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_PASS_SCOPED'
    assert r2['classification']=='C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_PASS_SCOPED'
    assert b['classification']=='C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_PASS_SCOPED'
    assert fcond['classification']=='C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_PASS_SCOPED'
    assert g['classification']=='C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_PASS_SCOPED'
    assert cimpl['classification']=='C10_65S2_C_KERNEL_PARITY_PASS_SCOPED'
    off=json.loads(Path(a.off_identity).read_text())
    dom=t['canary_domain']; ks=[float(x) for x in dom['k_Mpc_inv']]; lam=float(dom['lambda_HL']); Mc=float(dom['M_c_Mpc_inv']); aon=float(dom['a_on'])
    lim=float(t['frozen_checks']['max_first_production_rhs_vs_certified_r2_relative'])
    onset_tol=float(t['frozen_checks']['exact_onset_relative_a_tolerance'])
    rows=parse(a.observer); before=[x for x in rows if x['phase']=='BEFORE']; after=[x for x in rows if x['phase']=='AFTER']
    before.sort(key=lambda x:x['k']); after.sort(key=lambda x:x['k'])
    states={(float(q['k'])):q for q in s1['completed_states'] if float(q['lambda_HL'])==lam and float(q['M_c_Mpc_inv'])==Mc and float(q['k']) in ks}
    p2=next(q for q in r2['points'] if float(q['lambda_HL'])==lam and float(q['M_c_Mpc_inv'])==Mc)
    r2m={float(q['k']):q for q in p2['records']}; bm={float(q['k']):q for q in b['records']}
    checks={}
    checks['off_identity']=off.get('all_four_numeric_rows_sha256_identical') is True
    checks['record_counts']=len(before)==len(after)==4 and sorted(x['k'] for x in before)==sorted(ks) and sorted(x['k'] for x in after)==sorted(ks)
    checks['onset']=checks['record_counts'] and all(rel(x['a'],aon)<=onset_tol for x in before)
    checks['approximation']=checks['record_counts'] and all(x['tca']==0 and x['rsa']==0 and x['ufa']==0 and x['lmax']==17 for x in before+after)
    state_errors={}; higher_errors={}; rhs_errors={}; drift={}; allfinite=True
    for br,ar in zip(before,after):
        k=br['k']; st=states[k]; rr=r2m[k]['C']; bb=bm[k]
        pairs={'phi':st['phi_CLASS'],'delta_b':st['delta_b'],'theta_b':st['theta_b'],'delta_g':st['delta_g'],'theta_g':st['theta_g'],'delta_ur':st['delta_ur'],'theta_ur':st['theta_ur'],'shear_ur':st['shear_ur'],'delta_khr_N':st['delta_cdm_khr'],'theta_khr_N':st['theta_cdm_khr']}
        state_errors[format(k,'.17g')]={n:rel(br[n],v) for n,v in pairs.items()}
        higher_errors[format(k,'.17g')]={str(l):rel(br['Fl'][l],st['higher_order_historical_control'][str(l)]) for l in range(3,18)}
        # First real production RHS. Ordinary density derivatives are implied by the certified metric-continuity plus state velocities.
        mc=float(rr['c10_65r2_metric_continuity_shadow']); me=float(rr['c10_65r2_metric_euler_shadow'])
        expected={
          'phi_prime':float(rr['c10_65r2_Psi_N_prime']),
          'delta_b_prime':-(float(st['theta_b'])+mc),
          'theta_b_prime':float(rr['c10_65r2_theta_b_prime_shadow']),
          'delta_g_prime':-(4./3.)*(float(st['theta_g'])+mc),
          'theta_g_prime':float(rr['c10_65r2_theta_g_prime_shadow']),
          'delta_ur_prime':-(4./3.)*(float(st['theta_ur'])+mc),
          'theta_ur_prime':float(rr['c10_65r2_theta_ur_prime_shadow']),
          'delta_khr_N_prime':float(bb['delta_N_prime_from_charge']),
          'theta_khr_N_prime':float(bb['theta_N_prime_transformed']),
          'Psi_N_prime':float(rr['c10_65r2_Psi_N_prime']),
          'metric_euler':me,
        }
        actual={q:br[q] for q in ['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime','Psi_N_prime']}
        actual['metric_euler']=k*k*br['Phi_N']
        rhs_errors[format(k,'.17g')]={q:rel(actual[q],v) for q,v in expected.items()}
        drift[format(k,'.17g')]={}
        for short,raw,norm in [('A','A_raw','A_norm'),('H','H_raw','H_norm'),('M','M_raw','M_norm')]:
            drift[format(k,'.17g')][short]={'before_raw':br[raw],'after_raw':ar[raw],'signed_change_raw':ar[raw]-br[raw],'absolute_change_raw':abs(ar[raw]-br[raw]),'before_normalized':br[norm],'after_normalized':ar[norm],'signed_change_normalized':ar[norm]-br[norm],'absolute_change_normalized':abs(ar[norm]-br[norm])}
        allfinite &= all(finite(v) for x in (br,ar) for n,v in x.items() if n not in ('phase','Fl') and not (x is ar and n.endswith('_prime') and math.isnan(v)))
        allfinite &= all(finite(v) for x in (br,ar) for v in x['Fl'].values())
    max_state=max((v for d in state_errors.values() for v in d.values()),default=math.inf)
    max_higher=max((v for d in higher_errors.values() for v in d.values()),default=math.inf)
    max_rhs=max((v for d in rhs_errors.values() for v in d.values()),default=math.inf)
    checks['boundary_state']=max_state<=1e-12 and max_higher<=1e-12
    checks['first_production_rhs']=max_rhs<=lim
    checks['first_rhs_calls']=checks['record_counts'] and all(x['rhs_calls']==1 for x in before)
    expected_calls=int(plan['execution']['expected_rhs_calls_for_one_accepted_no_rejection_cash_karp_step'])
    checks['exactly_one_accepted_step']=checks['record_counts'] and all(x['rhs_calls']==expected_calls for x in after)
    dt=float(plan['execution']['short_step_delta_tau_Mpc'])
    checks['step_width']=checks['record_counts'] and all(rel(ar['tau']-br['tau'],dt)<=1e-12 for br,ar in zip(before,after))
    checks['finite']=allfinite
    checks['constraint_capture']=checks['record_counts'] and all(finite(x[q]) for x in before+after for q in ['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm'])
    ptxt=Path(a.patch).read_text(); v2txt=Path(a.patch_v2).read_text()
    static={
      'default_off_present':'pba->c10_65s2_canary = 0.' in ptxt,
      'direct_tau_before_intervals':'background_tau_of_z' in ptxt and "tau = tau_mid" in ptxt,
      'ordinary_seed_owned_by_initial_conditions':"insert_before_success(ps,'int perturb_initial_conditions('" in ptxt and 'rtk_c10_65s2_seed_owned' in ptxt,
      'post_vector_handoff_two_slots_only': 'Frozen post-vector write whitelist: exactly these two integrated slots.' in ptxt and 'pv->y[pv->index_pt_delta_cdm]=s->dk' in ptxt and 'pv->y[pv->index_pt_theta_cdm]=s->tk' in ptxt,
      'dynamic_kernel_current_state':'rtk_c10_65s2_current_state(&in,o)' in ptxt,
      'legacy_not_consumed_by_bridge': all(z not in ptxt.split("bridge_c=f'''",1)[1].split("'''",1)[0] for z in ['index_pt_deltaU_nlde','index_pt_deltaV_nlde','index_pt_deltaZ_nlde']),
      'no_approximation_mutation': 'ppw->approx[ppw->index_ap_tca]=' not in ptxt and 'ppw->approx[ppw->index_ap_rsa]=' not in ptxt and 'ppw->approx[ppw->index_ap_ufa]=' not in ptxt,
      'one_step_then_exit':'goto c10_65s2_finish' in ptxt and 'tau_actual_size=0' in ptxt,
      'thermo_signature_fix_only':'no physics/criteria changes' in v2txt,
    }
    checks['static_guards']=all(static.values())
    checks['threshold_unchanged']=lim==5e-9 and cimpl.get('threshold_changed') is False
    passed=all(checks.values())
    out={
      'schema':'RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_RESULT_v1','gate':'C10.65s2',
      'classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'static_guards':static,
      'off_path':off,'max_boundary_state_relative':max_state,'max_higher_ur_relative':max_higher,'max_first_production_rhs_relative':max_rhs,
      'first_production_rhs_errors':rhs_errors,'boundary_state_errors':state_errors,'higher_ur_errors':higher_errors,
      'constraint_drift_measurement_only':drift,'step_delta_tau_Mpc':dt,'expected_rhs_calls_per_accepted_step':expected_calls,
      'interpretation':t['interpretation_if_pass'] if passed else 'The frozen one-step production canary did not satisfy every preregistered check. Preserve the failure and diagnose the failing check before any later stability gate.',
      'next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s2 without weakening frozen criteria unless a separately justified scientific correction is frozen first.',
      'threshold_changed':False,'non_claims':t['non_claims']
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification']); print(json.dumps({'max_state':max_state,'max_higher':max_higher,'max_rhs':max_rhs,'checks':checks},sort_keys=True))
    return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
