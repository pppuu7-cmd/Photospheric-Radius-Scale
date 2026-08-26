#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def need(text,marker,label):
    if marker not in text: raise RuntimeError(f'missing {label}: {marker}')
    return True

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--class-root',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    cr=Path(a.class_root)
    t=L('research/theory_targets/RTK_C10_65S0_DIRECT_ONSET_STATE_VECTOR_ARCHITECTURE_TARGET_v1.json')
    r2=L('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json')
    k=L('research/theory_results/RTK_C10_65K_NONLOCAL_TEMPORAL_SELECTOR_FEASIBILITY_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    b=L('research/theory_targets/RTK_C10_65B_COMPLETED_U1_ADIABATIC_GRADIENT_SYSTEM_TARGET_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert r2['classification']=='C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_PASS_SCOPED'
    assert r2['off_path']['numeric_text_sha256_identical_all_four'] is True
    assert r2['grid_point_count']==9 and r2['anchor_count_per_point']==4
    assert k['classification']=='C10_65K_NO_CERTIFIED_PRE_ONSET_BACKWARD_INTERVAL_UV_MATCH_REQUIRED_SCOPED'
    assert k['low_k_seed_support']['nonzero_certified_pre_onset_interval'] is False
    aon=float(f['exact_anchor']['a_on'])

    ps=(cr/'source/perturbations.c').read_text()
    ph=(cr/'include/perturbations.h').read_text()
    bh=(cr/'include/background.h').read_text()
    inp=(cr/'source/input.c').read_text()
    patch=(ROOT/'rtk/apply_rtk_class_patch.py').read_text()

    source_checks={}
    for marker,label in [
      ('tau = tau_mid;','tau selected before interval construction'),
      ('perturb_find_approximation_number(','approximation interval construction'),
      ('previous_approx=NULL;','first interval has NULL previous approximation'),
      ('perturb_vector_init(','vector init invocation'),
      ('if (pa_old == NULL) {','new-mode vector init branch'),
      ('perturb_initial_conditions(','initial condition delegation'),
      ('class_define_index(ppv->index_pt_phi','Newtonian phi integrated state'),
      ('class_define_index(ppv->index_pt_delta_b','baryon density state'),
      ('class_define_index(ppv->index_pt_theta_b','baryon velocity state'),
      ('class_define_index(ppv->index_pt_delta_g','photon density state'),
      ('class_define_index(ppv->index_pt_theta_g','photon velocity state'),
      ('class_define_index(ppv->index_pt_delta_ur','UR density state'),
      ('class_define_index(ppv->index_pt_theta_ur','UR velocity state'),
      ('class_define_index(ppv->index_pt_shear_ur','UR shear state'),
      ('class_define_index(ppv->index_pt_l3_ur','UR l3 state'),
      ('class_define_index(ppv->index_pt_delta_cdm','CDM-slot density state'),
      ('class_define_index(ppv->index_pt_theta_cdm','CDM-slot velocity state'),
      ('class_define_index(ppw->index_mt_psi','psi metric workspace constraint'),
      ('class_define_index(ppw->index_mt_phi_prime','phi-prime metric workspace constraint'),
      ('class_define_index(ppv->index_pt_deltaU_nlde','legacy dU state'),
      ('class_define_index(ppv->index_pt_deltaU_prime_nlde','legacy dUprime state'),
      ('class_define_index(ppv->index_pt_deltaV_nlde','legacy dV state'),
      ('class_define_index(ppv->index_pt_deltaV_prime_nlde','legacy dVprime state'),
      ('class_define_index(ppv->index_pt_deltaZ_nlde','legacy dZ state'),
      ('class_define_index(ppv->index_pt_deltaZ_prime_nlde','legacy dZprime state'),
      ('ppw->pvecmetric[ppw->index_mt_psi] = y[ppw->pv->index_pt_phi] +3.*(pba->gnl)*y[ppw->pv->index_pt_deltaZ_nlde]','legacy model2 psi depends on dZ'),
    ]:
        source_checks[label]=need(ps,marker,label)
    source_checks['background_tau_of_z available']=need(bh,'int background_tau_of_z(','background_tau_of_z')
    source_checks['model2 forces has_nlde']=need(inp,'if (pba->model != 0.)\n      pba->has_nlde = _TRUE_;','model2 has_nlde parser rule')
    source_checks['RTK repurposes CDM slot as Khronon']=need(patch,'cdm slot / DBI-Khronon','RTK CDM-slot Khronon repurpose')
    source_checks['RTK Khronon derivative writes CDM state slots']=need(patch,'dy[pv->index_pt_delta_cdm]=kd.delta_prime; dy[pv->index_pt_theta_cdm]=kd.theta_prime;','Khronon CDM-slot derivatives')

    # Ordering certificate: tau assignment must precede interval discovery, and
    # initial interval must call vector_init after previous_approx=NULL is chosen.
    order={
      'tau_before_interval_number':ps.index('tau = tau_mid;') < ps.index('perturb_find_approximation_number('),
      'null_previous_before_vector_init_call':ps.index('previous_approx=NULL;') < ps.index('class_call(perturb_vector_init(',ps.index('previous_approx=NULL;')),
    }
    assert all(order.values())

    species=b['baseline_species']
    assert species['ordinary_filtered_A_source']==['baryons','photons','massless_UR']
    assert species['neutral_unfiltered_metric_source']==['RTK/Khronon']
    assert species['physical_CDM'] is False and species['massive_ncdm'] is False

    legacy=['deltaU_nlde','deltaU_prime_nlde','deltaV_nlde','deltaV_prime_nlde','deltaZ_nlde','deltaZ_prime_nlde']
    completed_integrated=[
      'phi_CLASS (= completed Psi_N in Newtonian state)',
      'delta_b','theta_b','delta_g','theta_g',
      'delta_ur','theta_ur','shear_ur',
      'delta_cdm slot -> Khronon delta_N','theta_cdm slot -> Khronon theta_N'
    ]
    higher=['UR F_l for l>=3 when UFA is off at onset']
    constrained=['psi_CLASS (= completed Phi_N)','phi_CLASS_prime (= completed Psi_N_prime)']

    cls='C10_65S0_DIRECT_ONSET_INITIALIZATION_ARCHITECTURE_PASS_LEGACY_AUX_EXCLUSION_REQUIRED_SCOPED'
    out={
      'schema':'RTK_C10_65S0_DIRECT_ONSET_STATE_VECTOR_ARCHITECTURE_RESULT_v1','gate':'C10.65s0','classification':cls,
      'target':'research/theory_targets/RTK_C10_65S0_DIRECT_ONSET_STATE_VECTOR_ARCHITECTURE_TARGET_v1.json',
      'a_on':aon,'z_on':1.0/aon-1.0,
      'parent_guards':{
        'C10_65r2_full_grid_pass':True,'C10_65r2_exact_off_identity':True,
        'C10_65k_certified_pre_onset_width_zero':True,'C10_65n_seed_pass':n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
      },
      'source_lock':source_checks,'ordering_certificate':order,
      'state_inventory':{
        'completed_integrated_coordinates':completed_integrated,
        'completed_metric_constraint_outputs_not_independent_state':constrained,
        'legacy_model2_integrated_auxiliary_coordinates':legacy,
        'finite_k_higher_order_coordinates_not_fixed_by_O_k2_matching':higher
      },
      'legacy_auxiliary_decision':{
        'historical_fact':'model=2 forces has_nlde=TRUE in the pinned fork and allocates six U/V/Z perturbation phase-space coordinates; historical psi/phi_prime constraints depend on them.',
        'completed_baseline_contract':'C10.65b defines the completed perturbation species as baryons+photons+massless-UR plus neutral Khronon, with no physical CDM or massive ncdm and no legacy nlde perturbation species.',
        'required_for_forward_feedback':'An opt-in completed-U1 perturbation path must not let dU/dV/dZ enter the completed metric/RHS. The safest implementation is to suppress their perturbation allocation/evolution in completed mode, while retaining the historical production background only under the already-declared scoped background guard.',
        'not_a_background_claim':'This does not remove or rederive the historical background contribution; same-full-action background closure remains separate and open.'
      },
      'initialization_architecture':{
        'selected':'DIRECT_OPT_IN_START_AT_CERTIFIED_A_ON',
        'reason':'C10.65k provides no certified coupled pre-onset low-k interval. Starting directly at a_on avoids importing an uncertified historical perturbation trajectory and avoids adaptive-integrator side effects from a one-time RHS overwrite.',
        'tau_on_method':'background_tau_of_z(pba,1/a_on-1,&tau_on), then use tau_on as the opt-in perturb_solve initial tau before approximation interval construction.',
        'initial_state_method':'Use the ordinary pa_old=NULL perturb_vector_init -> perturb_initial_conditions path, with a completed-mode initial-condition branch filling the full integrated state.',
        'metric_requirement':'Set integrated Newtonian phi state to completed Psi_N and, from the first RHS onward, replace historical model=2 metric constraint outputs by completed Phi_N/Psi_N_prime rather than consuming dZ/dV legacy constraints.',
        'no_custom_handoff_approximation_needed':True
      },
      'remaining_before_first_forward_step':{
        'approximation_state_at_a_on':['TCA already certified ON','UFA and RSA must be explicitly exported/source-locked in C10.65s1'],
        'higher_multipoles':'If UFA is OFF, F_l>=3 are genuine finite-k integrated coordinates. They are beyond the O(k^2) matching vector and need an explicit regular/historical higher-order control with scaling checks; they may not be silently inherited from a pre-onset completed trajectory that does not exist.',
        'production_feedback':'not implemented in s0'
      },
      'next_gate':t['next_if_pass'],'non_claims':t['non_claims']
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'a_on':aon,'z_on':out['z_on'],'legacy_aux_count':len(legacy),'higher_control_requirements':len(higher)},sort_keys=True))
if __name__=='__main__': main()
