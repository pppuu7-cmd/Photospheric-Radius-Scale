#!/usr/bin/env python3
import argparse,json,math,pathlib,re,sys

P=pathlib.Path

def load(p):
    return json.load(open(p))

def finite(x):
    return isinstance(x,(int,float)) and math.isfinite(float(x))

def rel(a,b):
    a=float(a); b=float(b)
    return abs(a-b)/max(1.0,abs(a),abs(b))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--class-source',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()

    target=load('research/theory_targets/RTK_C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_TARGET_v1.json')
    s2=load('research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json')
    s1=load('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json')
    s0=load('research/theory_results/RTK_C10_65S0_DIRECT_ONSET_STATE_VECTOR_ARCHITECTURE_RESULT_v1.json')
    r2=load('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json')

    checks={}
    checks['parents']=(
        s1.get('classification')==target['parents']['C10.65s1'] and
        s0.get('classification')==target['parents']['C10.65s0'] and
        r2.get('classification')==target['parents']['C10.65r2'])
    checks['s2_frozen']=s2.get('status')=='FROZEN_BEFORE_IMPLEMENTATION' and s2.get('gate')=='C10.65s2'

    dom=target['frozen_domain']; ks=[float(x) for x in dom['k_Mpc_inv']]
    s1rows=[x for x in s1['completed_states'] if float(x['lambda_HL'])==float(dom['lambda_HL']) and float(x['M_c_Mpc_inv'])==float(dom['M_c_Mpc_inv'])]
    s1rows=sorted(s1rows,key=lambda x:ks.index(float(x['k'])) if float(x['k']) in ks else 999)
    r2pt=next(x for x in r2['points'] if float(x['lambda_HL'])==float(dom['lambda_HL']) and float(x['M_c_Mpc_inv'])==float(dom['M_c_Mpc_inv']))
    r2rows=sorted(r2pt['records'],key=lambda x:ks.index(float(x['k'])) if float(x['k']) in ks else 999)
    checks['counts']=len(s1rows)==len(r2rows)==4
    checks['k_alignment']=checks['counts'] and [float(x['k']) for x in s1rows]==ks and [float(x['k']) for x in r2rows]==ks
    checks['a_on']=rel(s1.get('a_on'),dom['a_on'])==0.0 and all(rel(x.get('relative_a_error',0.0),0.0)==0.0 for x in r2rows)

    state_keys=['phi_CLASS','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_cdm_khr','theta_cdm_khr','Phi_N_constraint_not_state']
    rhs_keys=['c10_65r2_B_general','c10_65r2_B_prime','c10_65r2_Psi_N_prime','c10_65r2_metric_continuity_shadow','c10_65r2_metric_euler_shadow','c10_65r2_theta_b_prime_shadow','c10_65r2_theta_g_prime_shadow','c10_65r2_theta_ur_prime_shadow','c10_65r2_delta_khr_prime_shadow','c10_65r2_theta_khr_prime_shadow']
    checks['state_finite']=all(finite(row[k]) for row in s1rows for k in state_keys)
    checks['rhs_finite']=all(finite(row['C'][k]) for row in r2rows for k in rhs_keys)
    checks['legacy_excluded']=all(row.get('legacy_nlde_auxiliaries_excluded') is True for row in s1rows)

    manifest=[]; max_phi=0.0
    for sr,rr in zip(s1rows,r2rows):
        k=float(sr['k']); phi_r2=float(rr['C']['c10_65r2_metric_euler_shadow'])/(k*k)
        er=rel(phi_r2,sr['Phi_N_constraint_not_state']); max_phi=max(max_phi,er)
        manifest.append({
          'k':k,'a_on':float(dom['a_on']),
          'state':{q:sr[q] for q in state_keys},
          'higher_order_historical_control':sr['higher_order_historical_control'],
          'certified_first_rhs':{q:rr['C'][q] for q in rhs_keys},
          'phiN_from_metric_euler':phi_r2,
          'phiN_relative_crosscheck':er,
          'legacy_nlde_auxiliaries_excluded':True})
    checks['phi_crosscheck']=max_phi <= target['frozen_checks']['max_phiN_from_r2_metric_euler_vs_s1_constraint_relative']

    src=P(a.class_source).read_text()
    anchors={
      'perturb_initial_conditions':'int perturb_initial_conditions(',
      'perturb_vector_init':'perturb_vector_init(',
      'generic_evolver':'generic_evolver(perturb_derivs',
      'delta_cdm_derivative':'dy[pv->index_pt_delta_cdm]',
      'theta_cdm_derivative':'dy[pv->index_pt_theta_cdm]',
      'metric_psi':'ppw->pvecmetric[ppw->index_mt_psi]',
      'metric_phi_prime':'ppw->pvecmetric[ppw->index_mt_phi_prime]',
      'legacy_deltaU':'index_pt_deltaU_nlde',
      'legacy_deltaV':'index_pt_deltaV_nlde',
      'legacy_deltaZ':'index_pt_deltaZ_nlde'}
    source_lock={k:(v in src) for k,v in anchors.items()}
    checks['source_anchors']=all(source_lock.values())

    repo_text='\n'.join(p.read_text(errors='ignore') for p in list(P('rtk').glob('*.py'))+list(P('research/shadow').glob('*.py')) if p.name!='rtk_c10_65s2a_production_canary_source_lock_preflight.py')
    forbidden=['RTK_C10_65S2_PRODUCTION_CANARY_V1','c10_65s2_canary > 0.5']
    checks['no_s2_production_patch']=not any(x in repo_text for x in forbidden)

    passed=all(checks.values())
    out={
      'schema':'RTK_C10_65S2A_PRODUCTION_CANARY_SOURCE_LOCK_PREFLIGHT_RESULT_v1',
      'gate':'C10.65s2a',
      'classification':target['pass_classification'] if passed else target['fail_classification'],
      'checks':checks,
      'source_lock':source_lock,
      'max_phiN_from_r2_metric_euler_vs_s1_constraint_relative':max_phi,
      'manifest':manifest,
      'interpretation':'Source-lock and finite handoff manifest only; no production mutation or integrator step executed.',
      'threshold_changed':False}
    P(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'])
    print('max_phi_crosscheck',format(max_phi,'.17e'))
    for k,v in checks.items(): print(k,v)
    return 0 if passed else 2

if __name__=='__main__': sys.exit(main())
