#!/usr/bin/env python3
from __future__ import annotations
import inspect, json, math, pathlib, sys
P=pathlib.Path
sys.path.insert(0,str(P(__file__).resolve().parent))
from rtk_c10_65s2c_current_state_dae_metric_core import current_state_metric_core
from rtk_c10_65s2d_current_state_traceless_tca_closure import current_state_traceless_tca
from rtk_c10_65s2e_current_state_derivative_slip_closure import dynamic_derivative_slip

def L(p): return json.load(open(p))
def rel(a,b):
    a=float(a); b=float(b); return abs(a-b)/max(abs(a),abs(b),1e-300)

def main():
    t=L('research/theory_targets/RTK_C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_TARGET_v1.json')
    b=L('research/theory_results/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1.json')
    c=L('research/theory_results/RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_RESULT_v1.json')
    d=L('research/theory_results/RTK_C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_RESULT_v1.json')
    e=L('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json')
    f=L('research/theory_results/RTK_C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_RESULT_v1.json')
    s2=L('research/theory_targets/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_TARGET_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    dom=t['frozen_domain']; lam=float(dom['lambda_HL']); Mc=float(dom['M_c_Mpc_inv']); ks=[float(x) for x in dom['k_Mpc_inv']]

    emap={(float(r['lambda_HL']),float(r['M_c_Mpc_inv']),float(r['k'])):r for r in e['records']}
    bmap={float(r['k']):r for r in b['records']}
    rows=[]; max_dn=0.0; max_tn=0.0; finite_all=True
    for k in ks:
        er=emap[(lam,Mc,k)]; br=bmap[k]; z=er['dynamic']
        ed=rel(z['delta_khr_N_prime'],br['delta_N_prime_from_charge'])
        et=rel(z['theta_khr_N_prime'],br['theta_N_prime_transformed'])
        max_dn=max(max_dn,ed); max_tn=max(max_tn,et)
        finite_all &= all(math.isfinite(float(v)) for v in z.values())
        rows.append({'k':k,'delta_khr_N_prime':z['delta_khr_N_prime'],'delta_s2b':br['delta_N_prime_from_charge'],'delta_relative':ed,
                     'theta_khr_N_prime':z['theta_khr_N_prime'],'theta_s2b':br['theta_N_prime_transformed'],'theta_relative':et,
                     'implicit_denominator':z['Bprime_implicit_denominator']})

    max_noncond=max(float(v) for k,v in e['maxima'].items())
    sig=set(inspect.signature(dynamic_derivative_slip).parameters)
    logical_to_python={'lambda_HL':'lam','M_c':'Mc'}
    required=[]
    for x in t['runtime_stage_inputs_required']:
        required.append(logical_to_python.get(x,x))
    runtime_args_ok=all(x in sig for x in required)
    src_e=inspect.getsource(dynamic_derivative_slip)
    src_c=inspect.getsource(current_state_metric_core)
    src_d=inspect.getsource(current_state_traceless_tca)
    onset_literals=['0.0002203229136467','0.0129629303512','-0.000131966812715','0.11571457684851365','0.0030000000135438033','2.46650315001575e-09','6.6951521502165']
    no_onset_literals=all(x not in src_e for x in onset_literals)
    no_reads=all(x not in src_e for x in ['open(','json.','Path(','glob','history','current.json'])
    no_seed=all(x not in (src_c+src_d+src_e) for x in ['A2','C2','J_ad','S_ur0'])
    no_prod_patch=all(x not in src_e for x in ['subprocess','apply_patch','perturbations.c','class_public'])

    fc=t['frozen_checks']
    checks={
      'anchor_count':len(rows)==int(fc['anchor_count']),
      'delta_khr_N_prime_vs_s2b':max_dn<=float(fc['max_delta_khr_N_prime_relative_vs_s2b']),
      'theta_khr_N_prime_vs_s2b':max_tn<=float(fc['max_theta_khr_N_prime_relative_vs_s2b']),
      'existing_s2e_nonconditioning_parity':max_noncond<=float(fc['max_existing_s2e_nonconditioning_parity_relative']),
      'scalar_implicit_amplification':float(f['global']['max_scalar_implicit_amplification'])<=float(fc['max_scalar_implicit_amplification']),
      'implicit_denominator':float(f['global']['min_abs_implicit_denominator'])>=float(fc['min_abs_implicit_denominator']),
      'runtime_stage_inputs':runtime_args_ok==bool(fc['all_runtime_stage_inputs_are_function_arguments']),
      'no_onset_numeric_literals':no_onset_literals==bool(fc['dynamic_kernel_contains_no_onset_numeric_literals']),
      'no_file_or_history_reads':no_reads==bool(fc['dynamic_kernel_contains_no_file_or_history_reads']),
      'no_matching_seed_constants':no_seed==bool(fc['s2c_s2d_dynamic_kernels_contain_no_matching_seed_constants']),
      's2e_failed_parent_preserved':(e['classification']=='C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_FAIL_SCOPED')==bool(fc['s2e_failed_parent_classification_preserved']),
      's2f_pass':(f['classification']=='C10_65S2F_IMPLICIT_CONDITIONING_AUDIT_PASS_SCOPED')==bool(fc['s2f_must_pass']),
      's2_target_frozen':(s2['status']=='FROZEN_BEFORE_IMPLEMENTATION')==bool(fc['s2_target_status_remains_FROZEN_BEFORE_IMPLEMENTATION']),
      's2_rhs_threshold_unchanged':(float(s2['frozen_checks']['max_first_production_rhs_vs_certified_r2_relative'])==5e-9)==bool(fc['s2_target_rhs_parity_threshold_remains_5e-9']),
      'finite':finite_all==bool(fc['all_outputs_finite']),
      'no_production_patch':no_prod_patch==bool(fc['no_production_patch_in_s2g'])
    }
    passed=all(checks.values())
    out={
      'schema':'RTK_C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_RESULT_v1','gate':'C10.65s2g',
      'classification':t['pass_classification'] if passed else t['fail_classification'],
      'target':'research/theory_targets/RTK_C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_TARGET_v1.json',
      'checks':checks,
      'maxima':{'delta_khr_N_prime_vs_s2b':max_dn,'theta_khr_N_prime_vs_s2b':max_tn,'existing_s2e_nonconditioning_parity':max_noncond},
      'conditioning':{'min_abs_implicit_denominator':f['global']['min_abs_implicit_denominator'],'max_scalar_implicit_amplification':f['global']['max_scalar_implicit_amplification']},
      'runtime_signature':sorted(sig),'records':rows,
      'failed_s2e_classification_preserved':e['classification'],
      'threshold_changed':False,'next':t['next_if_pass'] if passed else 'Do not implement s2 production canary; resolve production-kernel preflight failure.',
      'non_claims':t['non_claims']
    }
    P('research/theory_results/RTK_C10_65S2G_PRODUCTION_KERNEL_PREFLIGHT_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification']); print(json.dumps(out['maxima'],sort_keys=True))
    return 0 if passed else 2
if __name__=='__main__': sys.exit(main())
