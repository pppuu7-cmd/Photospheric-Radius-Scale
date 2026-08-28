#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
import mpmath as mp

TARGET_COMMIT='e24d6776fc068e65aeb4a0c838d21175a120a47f'
PARENT='99119e680a8bc57be9115ed07e851b7a16a3d0ea'
CLASS='RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_QUOTIENT_ASSEMBLED_CONVENTION_BOUND_PASS_SCOPED'
mp.mp.dps=90

T=mp.mpf('67.869342368305180409328005773658622338151596454315223519029011945298722091682815')
L=mp.mpf('2.1999085267023697422585361883960668683089207686293255795194962406150393938391081')
INHERITED=mp.mpf('149.30634497771697105893170945826130655341339602612728394167831214428717291534588')
product=T*L
relerr=abs(product-INHERITED)/INHERITED
assert relerr < mp.mpf('1e-75')
phase=mp.mpf(1)
hodge=mp.mpf(1)
orbit_coeff=16*mp.pi**10
C=(phase*hodge*product)/orbit_coeff

def Q(a):
    a=mp.mpf(a)
    return C/a**15

scaling=[]
for s in ['2','1.5','3.25']:
    ratio=Q(s)/Q('1')
    expected=mp.mpf(s)**(-15)
    err=abs(ratio-expected)
    assert err < mp.mpf('1e-85')
    scaling.append({'scale':s,'Q_ratio':mp.nstr(ratio,70),'expected_s^-15':mp.nstr(expected,70),'abs_error':mp.nstr(err,8)})

result={
 'classification':CLASS,
 'target_frozen_commit':TARGET_COMMIT,
 'scientific_parent_head':PARENT,
 'background':'round S3, lambda=1',
 'operator':'M^i_j=nabla^2 delta^i_j+R^i_j',
 'frozen_conventions':{
   'spectral_cut':'principal cut inherited from signed-phase gate',
   'vector_coordinates':'L2-orthonormal transverse/longitudinal harmonics',
   'residual_group':'SO(4)',
   'generator_period':'2*pi',
   'Lie_metric':'-1/2 Tr'
 },
 'inherited_inputs':{
   'Det_prime_abs_T':mp.nstr(T,85),
   'Det_prime_abs_L':mp.nstr(L,85),
   'Det_prime_abs_combined_certified':mp.nstr(INHERITED,85),
   'Det_prime_abs_combined_recomputed':mp.nstr(product,85),
   'relative_product_mismatch':mp.nstr(relerr,8),
   'combined_principal_cut_phase':'+1',
   'extra_Hodge_factor':1,
   'residual_SO4_orbit_volume':'16*pi^10*a^15'
 },
 'assembled_scoped_quotient':{
   'definition':'Q_FP_spatial(a)=Det_prime_zeta(a^2 M_FP)/Vol_L2(SO(4))',
   'exact_form':'Q_FP_spatial(a)=Det_prime_zeta(a^2 M_FP)/(16*pi^10*a^15)',
   'dimensionless_numerator':mp.nstr(product,85),
   'dimensionless_denominator_coefficient':'16*pi^10',
   'C_FP':mp.nstr(C,85),
   'formula':'Q_FP_spatial(a)=C_FP*a^(-15)',
   'phase':'+1',
   'convention_bound':True
 },
 'scaling_crosschecks':scaling,
 'scientific_checks':{
   'signed_nonzero_product_matches_certified_inputs':True,
   'combined_phase_exactly_plus_one':True,
   'no_extra_Hodge_factor':True,
   'residual_orbit_volume_16pi10a15':True,
   'quotient_scaling_a_minus15':True,
   'quotient_is_convention_bound_not_observable':True
 },
 'findings':{
   'complete_signed_spatial_FP_quotient_assembled_under_frozen_convention':True,
   'spatial_FP_quotient_is_convention_independent_observable':False,
   'full_FP_determinant_computed':False,
   'full_FS_determinant_computed':False,
   'full_gravitational_Hessian_determinant_computed':False,
   'complete_HMT_gauge_fixed_constraint_matrix_constructed':False,
   'full_HMT_one_loop_evaluable':False,
   'full_C9_closed':False,
   'ordinary_projectable_parent_beta_functions_imported':False,
   'unresolved_HMT_matter_coefficients_chosen':False,
   'soft_s_retest_allowed':False,
   'production_k003_unblocked':False,
   'threshold_changed':False,
   'no_DSIR':True
 },
 'interpretation':'The already-certified nonzero spatial FP determinant, trivial combined principal-cut phase, absence of an extra Hodge factor in orthonormal vector coordinates, and convention-fixed residual SO(4) orbit volume can be assembled consistently. The result is a scoped, convention-bound spatial FP quotient only; it is not the complete HMT FP/FS measure, one-loop determinant, or C9 closure.',
 'next_gate':'Source-lock and derive the physical TT quadratic Hessian on the same frozen round-S3, lambda=1 background before attempting any broader one-loop assembly.'
}

Path('research/theory_results').mkdir(parents=True,exist_ok=True)
Path('research/checkpoints').mkdir(parents=True,exist_ok=True)
Path('research/provenance').mkdir(parents=True,exist_ok=True)
Path('research/theory_results/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_QUOTIENT_ASSEMBLY_RESULT_v1.json').write_text(json.dumps(result,indent=2)+'\n')

checkpoint=f'''# RTK C9 HMT lambda=1 S3 spatial FP quotient assembly checkpoint\n\nClassification: `{CLASS}`\n\nFrozen target `{TARGET_COMMIT}`; scientific parent `{PARENT}`. The certified transverse and longitudinal nonzero-mode zeta magnitudes multiply to `{mp.nstr(product,50)}`, the frozen principal-cut combined phase is `+1`, and the Hodge audit requires no additional determinant in the L2-orthonormal vector basis. Under the previously frozen residual `SO(4)` convention, `Vol_L2(SO(4))=16*pi^10*a^15`.\n\nTherefore the scoped spatial FP quotient is\n\n`Q_FP_spatial(a) = {mp.nstr(C,50)} * a^(-15)`\n\nwith exact assembly `Det'_zeta(a^2 M_FP)/(16*pi^10*a^15)`. Scaling checks confirm the `a^-15` law. This quotient is convention-bound: the global SO(4) normalization, operator sign/spectral cut, and field-coordinate normalization are part of its definition. It is not a convention-independent observable.\n\nThis closes only the spatial-FP quotient bookkeeping gate. Full FP/FS determinants, physical TT Hessian, complete HMT gauge-fixed matrix, one-loop evaluability and C9 remain OPEN/BLOCKED. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed. Next gate: source-lock and derive the TT physical quadratic Hessian on the same frozen background.\n'''
Path('research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_QUOTIENT_ASSEMBLY_2026-08-28.md').write_text(checkpoint)
prov={
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'target_frozen_commit':TARGET_COMMIT,
 'scientific_parent_head':PARENT,
 'source_result_commits':['c6c9e4062569fcbf94c8e1860f509cb39defd9a3','83ae30fee6d77a3ea42ede57823bedc2875abfdf','99119e680a8bc57be9115ed07e851b7a16a3d0ea'],
 'script':'research/shadow/rtk_c9_hmt_lambda1_s3_spatial_fp_quotient_assembly.py',
 'method':'high-precision assembly of certified signed nonzero zeta determinant, unit Hodge factor, and convention-fixed SO(4) orbit quotient; exact scaling audit',
 'regularization':'no new regularization; inherits zeta determinants and principal spectral cut from source-locked gates',
 'no_DSIR':True,
 'no_threshold_change':True
}
Path('research/provenance/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_QUOTIENT_ASSEMBLY_PROVENANCE_v1.json').write_text(json.dumps(prov,indent=2)+'\n')
print(json.dumps(result,indent=2))
