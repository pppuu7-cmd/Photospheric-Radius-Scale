#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(rel):
    return json.loads((ROOT/rel).read_text())

def close(a,b,rtol=1e-12,atol=1e-15):
    return abs(a-b) <= atol + rtol*max(abs(a),abs(b),1.0)

def main():
    t=load('research/theory_targets/RTK_C10_65K_NONLOCAL_TEMPORAL_SELECTOR_FEASIBILITY_TARGET_v1.json')
    j=load('research/theory_results/RTK_C10_65J_FINITE_LOCAL_TEMPORAL_JET_IDENTIFIABILITY_RESULT_v1.json')
    i=load('research/theory_results/RTK_C10_65I_COUPLED_COEFFICIENT_NULLITY_WITH_SYMBOLIC_C2_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    a65=load('research/theory_results/RTK_C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json')
    proj=load('research/theory_results/RTK_C10_PREFERRED_METRIC_PROJECTOR_API_RESULT_v1.json')
    btarget=load('research/theory_targets/RTK_C10_65B_COMPLETED_U1_ADIABATIC_GRADIENT_SYSTEM_TARGET_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert j['classification']=='C10_65J_FINITE_LOCAL_TEMPORAL_JET_INSUFFICIENT_NONLOCAL_BRANCH_REQUIRED_SCOPED'
    assert i['classification']=='C10_65I_COUPLED_COEFFICIENT_NULLITY_REMAINING_TEMPORAL_AMPLITUDES_8_SCOPED'
    assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
    assert a65['classification']=='C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_CONSISTENT_PASS_SCOPED'
    assert src['classification']=='C10_PHYSICAL_CLASS_SOURCE_EXPORT_PASS'
    assert proj['classification']=='C10_PREFERRED_METRIC_PROJECTOR_API_PASS_SCOPED'

    a_on=float(f['exact_anchor']['a_on'])
    exact_ks=[float(x) for x in f['exact_anchor']['k_Mpc_inv']]
    assert len(exact_ks)>=3
    src_by_k={round(float(r['actual_k_Mpc_inv']),14):r for r in src['files']}
    rows=[]
    for k in exact_ks:
        r=src_by_k.get(round(k,14))
        if r is None:
            raise RuntimeError(f'missing source-support record for exact low-k anchor {k}')
        rows.append({
            'k_Mpc_inv':k,'a_min':float(r['a_min']),'a_max':float(r['a_max']),
            'tau_min_Mpc':float(r['tau_min_Mpc']),'tau_max_Mpc':float(r['tau_max_Mpc'])
        })

    common_earliest_a=max(r['a_min'] for r in rows)
    common_earliest_tau=max(r['tau_min_Mpc'] for r in rows)
    backward_width_a=a_on-common_earliest_a
    all_start_at_onset=all(close(r['a_min'],a_on) for r in rows)
    assert all_start_at_onset
    assert abs(backward_width_a)<=1e-15

    control_by_k={round(float(r['k_Mpc_inv']),14):r for r in a65['records']}
    control_anchor_consistency=[]
    for k in exact_ks:
        rr=control_by_k.get(round(k,14))
        if rr is None:
            raise RuntimeError(f'missing C10.65a control anchor {k}')
        control_anchor_consistency.append({
            'k_Mpc_inv':k,'a':float(rr['a']),'tau_Mpc':float(rr['tau_Mpc']),
            'a_equals_onset':close(float(rr['a']),a_on)
        })
    assert all(x['a_equals_onset'] for x in control_anchor_consistency)

    tca_records={round(float(r['k_Mpc_inv']),14):r for r in f['tca_domain']['records']}
    tca_low_k_ok=all(bool(tca_records[round(k,14)]['predicted_tca_on']) for k in exact_ks)
    assert tca_low_k_ok and bool(f['rank_seed_domain']['low_k_seed_ok'])

    khr_source=(ROOT/'rtk/khronon_background.c').read_text()
    analytic_khr_accepts_positive_a=('finite_positive(a)' in khr_source and 'khr_background' in khr_source)
    assert analytic_khr_accepts_positive_a

    background_guard=str(btarget['background_scope_guard'])
    same_action_open=('pinned production background only as a diagnostic matching branch' in background_guard
                      and 'same-full-action' in background_guard)
    assert same_action_open

    nonzero_backward_interval=(common_earliest_a < a_on*(1.0-1e-12))
    assert not nonzero_backward_interval

    cls='C10_65K_NO_CERTIFIED_PRE_ONSET_BACKWARD_INTERVAL_UV_MATCH_REQUIRED_SCOPED'
    out={
      'schema':'RTK_C10_65K_NONLOCAL_TEMPORAL_SELECTOR_FEASIBILITY_RESULT_v1',
      'gate':'C10.65k','classification':cls,
      'target':'research/theory_targets/RTK_C10_65K_NONLOCAL_TEMPORAL_SELECTOR_FEASIBILITY_TARGET_v1.json',
      'low_k_seed_support':{
        'a_on':a_on,'exact_anchor_k_Mpc_inv':exact_ks,'records':rows,
        'common_earliest_a':common_earliest_a,'common_earliest_tau_Mpc':common_earliest_tau,
        'backward_width_in_a_with_persisted_common_support':backward_width_a,
        'all_exact_low_k_histories_start_at_a_on':all_start_at_onset,
        'nonzero_certified_pre_onset_interval':False
      },
      'independent_control_anchor':control_anchor_consistency,
      'feasibility_matrix':{
        'low_k_TCA_at_onset':True,
        'low_k_gradient_seed_certified_at_onset':True,
        'preferred_finite_k_metric_projector_certified_given_a_supported_background_snapshot':True,
        'analytic_Khronon_background_accepts_positive_a':analytic_khr_accepts_positive_a,
        'persisted_coupled_production_support_strictly_before_onset_for_low_k_seed':False,
        'same_full_action_primordial_background_closed':False,
        'historical_CLASS_metric_allowed_as_completed_U1_backward_solution':False
      },
      'why_analytic_extension_is_not_enough':{
        'Khronon':'The analytic action-fluid background can be evaluated for positive a, but this certifies only that sector.',
        'coupled_background':'The completed projector needs H and total/ordinary source background data. Extending those below persisted production support would be a new assumption, not a consequence of the existing certificates.',
        'background_scope_guard':background_guard,
        'metric':'Historical CLASS phi/psi are read-only controls and cannot be used as the completed-U1 backward metric trajectory.'
      },
      'selector_consequence':{
        'backward_regularity_from_current_stack':'NOT_CERTIFIED',
        'asymptotic_primordial_eigenbranch_from_current_stack':'NOT_CERTIFIED',
        'later_time_boundedness':'Would be a new phenomenological final-time boundary condition, not silently equivalent to primordial growing-mode selection.',
        'required_boundary_class':'explicit pre-EFT/UV matching functional for C2 and the eight C10.65i fixed-C2 temporal amplitudes, unless a new independently certified earlier completed-U1 background branch is constructed'
      },
      'architecture_decision':'Do not extrapolate the pinned production histories below a_on to manufacture a growing-mode selector. Keep the unresolved seed explicitly UV/pre-EFT matched at this stage.',
      'next_gate':t['next_if_no_interval'],'non_claims':t['non_claims']
    }
    p=ROOT/'research/theory_results/RTK_C10_65K_NONLOCAL_TEMPORAL_SELECTOR_FEASIBILITY_RESULT_v1.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'a_on':a_on,'common_earliest_a':common_earliest_a,'backward_width_a':backward_width_a,'low_k_anchor_count':len(exact_ks)},sort_keys=True))

if __name__=='__main__':
    main()
