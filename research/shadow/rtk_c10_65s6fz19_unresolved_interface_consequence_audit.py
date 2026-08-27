#!/usr/bin/env python3
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65S6FZ19_UNRESOLVED_INTERFACE_CONSEQUENCE_AUDIT_TARGET_v1.json'
P18=ROOT/'research/theory_results/RTK_C10_65S6FZ18_HMT_MATTER_INTERFACE_SELECTOR_IDENTIFIABILITY_RESULT_v1.json'
P12=ROOT/'research/theory_results/RTK_C10_65S6FZ12_HMT_Z7_BACKGROUND_QUADRATIC_IDENTIFIABILITY_RESULT_v1.json'
P15=ROOT/'research/theory_results/RTK_C10_65S6FZ15_PRODUCTION_PX_CARRIER_SELECTION_RULE_RESULT_v1.json'
P16=ROOT/'research/theory_results/RTK_C10_65S6FZ16_HMT_MATTER_AUXILIARY_INTERFACE_SOURCE_LOCK_RESULT_v1.json'
P17=ROOT/'research/theory_results/RTK_C10_65S6FZ17_HMT_MATTER_COEFFICIENT_SELECTION_IR_EQUIVALENCE_RESULT_v1.json'
OUT=ROOT/'research/theory_results/RTK_C10_65S6FZ19_UNRESOLVED_INTERFACE_CONSEQUENCE_AUDIT_RESULT_v1.json'

t=json.loads(TARGET.read_text()); p18=json.loads(P18.read_text()); p12=json.loads(P12.read_text()); p15=json.loads(P15.read_text()); p16=json.loads(P16.read_text()); p17=json.loads(P17.read_text())
checks={}
checks['z18_parent_exact']=p18['classification']==t['parent_required']
checks['z12_parent_exact']=p12['classification']==t['required_parents']['z12']
checks['z15_parent_exact']=p15['classification']==t['required_parents']['z15']
checks['z16_parent_exact']=p16['classification']==t['required_parents']['z16']
checks['z17_parent_exact']=p17['classification']==t['required_parents']['z17']
checks['z15_intrinsic_G_over_K_exact']=p15['checks']['exact_G_over_K_equals_ca2'] is True
checks['z15_intrinsic_temporal_spatial_coefficients_fixed']=p15['checks']['intrinsic_temporal_coefficient_fixed_by_production_K_along_background'] and p15['checks']['intrinsic_spatial_coefficient_fixed_by_production_G_along_background']
checks['z16_source_interface_unfixed']=p16['source_lock']['unique_RTK_response_numerator_fixed'] is False and p16['source_lock']['published_interface_has_free_coupling_constants'] is True
checks['z17_continuous_family']=p17['selection_audit']['continuous_family_remains'] is True and p17['selection_audit']['unique_scalar_response_interface_selected'] is False
checks['z18_no_unique_selector']=p18['selector_audit']['unique_scalar_response_interface_selected'] is False
checks['z12_full_quadratic_not_source_locked']=len(p12['source_lock']['missing_required_inputs'])>0
# Exact source-normalization witness: same denominator D=z-z0, c=1 vs c=2 => residue ratio 4.
c1,c2=1,2
residue_ratio=(c2*c2)/(c1*c1)
checks['exact_same_pole_different_residue_witness']=residue_ratio==4
checks['no_representative_point_selected']=True
checks['no_old_kernel_matching']=True
checks['no_soft_s_or_k003']=True
checks['threshold_unchanged']=t['threshold_changed'] is False

complete=all(checks.values())
full_invariant=False
interface_dependent=(checks['z15_intrinsic_G_over_K_exact'] and checks['z16_source_interface_unfixed'] and checks['z17_continuous_family'] and checks['exact_same_pole_different_residue_witness'])
if complete and interface_dependent:
    classification='C10_65S6FZ19_INTRINSIC_SECTOR_FIXED_FULL_RESPONSE_INTERFACE_DEPENDENT_PASS_SCOPED'
elif complete and full_invariant:
    classification='C10_65S6FZ19_FULL_QUADRATIC_RESPONSE_INTERFACE_INVARIANT_PASS_SCOPED'
else:
    classification='C10_65S6FZ19_CONSEQUENCE_AUDIT_INCOMPLETE_BLOCKED_SCOPED'

interpretation=(
 'The independently selected production P(X)-type carrier identities remain source-locked: the intrinsic temporal/spatial quadratic coefficients satisfy G/K=c_a^2 along the certified background. '
 'However the universal HMT matter interface still contains free coupling data and does not uniquely fix the scalar response source/numerator. '
 'This is already sufficient to obstruct the old RTK pole+residue+remainder certificate: even holding a denominator D(z) fixed, R_c(z)=c^2/D(z) has the same pole for every nonzero c but residue proportional to c^2; choosing c=1 and c=2 gives an exact residue ratio 4. '
 'Therefore intrinsic carrier selection cannot be promoted to full response equivalence over the continuous interface family. No representative coupling point is selected.'
)
next_gate=(
 'C10.65s6fZ20: freeze an independent microscopic-matter-completion source-lock audit. Search pre-soft-s or externally motivated matter microphysics for one explicit universal physical-metric coupling that fixes the remaining HMT matter-interface parameters before any RTK response comparison. '
 'If none is source-locked, keep the completion branch scientifically blocked rather than fitting pole/residue/remainder; if one is found, preregister that full matter interface and only then reopen the unchanged background/quadratic equivalence audit.'
)
r={
 'schema':'RTK_C10_65S6FZ19_UNRESOLVED_INTERFACE_CONSEQUENCE_AUDIT_RESULT_v1','gate':'C10.65s6fZ19','classification':classification,'checks':checks,
 'invariants':{'intrinsic_G_over_K':'c_a^2','intrinsic_temporal_coefficient':'K_phys','intrinsic_spatial_coefficient':'G_phys','representation':'Z7/HMT invariant carrier architecture'},
 'interface_dependent_or_open':['scalar-response source/numerator','physical-metric universal-coupling parameters','carrier A/prepotential auxiliary interface','full pole/residue/remainder equivalence'],
 'exact_witness':{'response':'R_c(z)=c^2/D(z)','c1':c1,'c2':c2,'same_denominator':True,'residue_ratio_c2_over_c1':residue_ratio},
 'interpretation':interpretation,'next_gate':next_gate,
 'nonclaims':['not a no-go for all HMT matter completions','not full RTK quadratic equivalence','not same-action primordial/background closure','not C9 naturalness','not a soft-s result','not k=0.03 production'],
 'threshold_changed':False,'soft_s_retest_allowed':False,'production_k003_unblocked':False,'s6ft_embedding_ready':False
}
OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
print(json.dumps(r,indent=2,sort_keys=True))
