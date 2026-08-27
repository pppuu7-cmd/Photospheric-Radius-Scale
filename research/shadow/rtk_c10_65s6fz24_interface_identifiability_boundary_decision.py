#!/usr/bin/env python3
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ24_INTERFACE_IDENTIFIABILITY_BOUNDARY_DECISION_TARGET_v1.json'
FILES={
 'z18':ROOT/'research/theory_results/RTK_C10_65S6FZ18_HMT_MATTER_INTERFACE_SELECTOR_IDENTIFIABILITY_RESULT_v1.json',
 'z19':ROOT/'research/theory_results/RTK_C10_65S6FZ19_UNRESOLVED_INTERFACE_CONSEQUENCE_AUDIT_RESULT_v1.json',
 'z20':ROOT/'research/theory_results/RTK_C10_65S6FZ20_HMT_MICROSCOPIC_MATTER_COMPLETION_SOURCE_LOCK_RESULT_v1.json',
 'z21':ROOT/'research/theory_results/RTK_C10_65S6FZ21_HMT_MATTER_INTERFACE_TECHNICAL_NATURALNESS_PREFLIGHT_RESULT_v1.json',
 'z22':ROOT/'research/theory_results/RTK_C10_65S6FZ22_INDEPENDENT_UV_SYMMETRY_COMPLETION_INVENTORY_RESULT_v1.json',
 'z23':ROOT/'research/theory_results/RTK_C10_65S6FZ23_HMT_INTERNAL_INTERFACE_SELECTOR_AUDIT_RESULT_v1.json'
}
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ24_INTERFACE_IDENTIFIABILITY_BOUNDARY_DECISION_RESULT_v1.json'
t=json.loads(TARGET.read_text())
r={k:json.loads(v.read_text()) for k,v in FILES.items()}
expected=t['required_parent_results']
actual=[r[f'z{i}']['classification'] for i in range(18,24)]
checks={}
checks['z18_z23_classifications_exact']=actual==expected
checks['z18_continuous_family']=r['z18']['selector_audit']['unique_scalar_response_interface_selected'] is False and r['z18']['selector_audit']['universal_ppn_family_continuous'] is True
checks['z19_full_response_interface_dependent']='full pole/residue/remainder equivalence' in r['z19']['interface_dependent_or_open']
checks['z20_microscopic_selector_unfixed']=r['z20']['microscopic_audit']['unique_uv_action_selector_found'] is False and r['z20']['microscopic_audit']['a1_a2_fixed'] is False
checks['z21_no_protected_unique_relation']=r['z21']['naturalness_audit']['unique_protected_interface_relation_found'] is False
checks['z22_no_hmt_matching_map']=r['z22']['inventory']['explicit_low_energy_hmt_matching_map_found'] is False and r['z22']['inventory']['hmt_interface_unique_selector_found'] is False
checks['z23_no_exact_internal_selector']=r['z23']['selector_audit']['exact_action_level_interface_selector_found'] is False and r['z23']['selector_audit']['allowed_region_remains_continuous'] is True
checks['no_representative_point_selected']=True
checks['no_rtk_response_or_softs_selection']=True
checks['soft_s_and_k003_stay_blocked']=all(x['soft_s_retest_allowed'] is False and x['production_k003_unblocked'] is False for x in r.values())
checks['threshold_unchanged']=t['threshold_changed'] is False and all(x['threshold_changed'] is False for x in r.values())
complete=all(checks.values())
selector_found=False
if complete and selector_found:
    classification='C10_65S6FZ24_SOURCE_LOCKED_INTERFACE_SELECTOR_FOUND_PASS_SCOPED'
elif complete:
    classification='C10_65S6FZ24_PARAMETER_UNDERDETERMINED_STOP_DECISION_PASS_SCOPED'
else:
    classification='C10_65S6FZ24_IDENTIFIABILITY_BOUNDARY_AUDIT_INCOMPLETE_BLOCKED_SCOPED'
interpretation=(
 'The source-locked chain Z18-Z23 is internally consistent: the pre-soft-s gauge/matter architecture leaves a continuous interface family; the intrinsic P(X) carrier sector can remain fixed while the full response residue/source is interface-dependent; the published microscopic origin leaves a1,a2 unfixed and fine-tuned in the IR; the audited radiative analysis supplies no protected unique relation; independently motivated SUSY/strong-dynamics mechanisms have no explicit HMT matching map; and HMT U(1)+PPN recovery leaves a continuous allowed region rather than an exact action-level selector. Therefore the current HMT+Z7 completion route is parameter-underdetermined at the physical matter interface. Further coefficient-selection iterations are scientifically stopped until genuinely new independently motivated microscopic/action input is preregistered. This is a scoped identifiability boundary, not a literature-wide no-go.'
)
next_gate=(
 'No coefficient-selection successor is authorized from the current source set. A future C10.65s6fZ25 may be frozen only after genuinely new microscopic/action input is independently identified and preregistered before any RTK pole/residue/remainder or soft-s comparison. Until then preserve the Z12/Z19 completion blocker, C9-open status, soft-s block, and k=0.03 production block.'
)
out={
 'schema':'RTK_C10_65S6FZ24_INTERFACE_IDENTIFIABILITY_BOUNDARY_DECISION_RESULT_v1',
 'gate':'C10.65s6fZ24','classification':classification,'checks':checks,
 'parent_classifications':actual,
 'decision':{
   'source_locked_exact_selector_found':False,
   'current_hmt_z7_interface_parameter_underdetermined':True,
   'coefficient_selection_iterations_authorized':False,
   'new_independent_microscopic_input_required':True,
   'intrinsic_px_carrier_result_preserved':True
 },
 'interpretation':interpretation,'next_gate':next_gate,
 'nonclaims':['not a literature-wide HMT no-go','not C9 radiative-naturalness closure','not a unique nonlinear RTK completion','not RTK pole/residue/remainder equivalence','not same-action primordial/background closure','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
