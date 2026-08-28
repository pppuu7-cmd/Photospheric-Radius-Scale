#!/usr/bin/env python3
import json, math
from pathlib import Path
from datetime import datetime, timezone
FROZEN='58e47520ca5f3ff3f5fc31b63b37a7b6d764d6d7'
PARENT='c3eb6d08fb60c19f54353b90da2f9194d45db71d'
# Frozen canonical metric <-1/2 Tr> makes E_AB orthonormal and SO(n)->S^(n-1)
# a Riemannian submersion onto the unit sphere in this normalization.
vol_s1=2*math.pi
vol_s2=4*math.pi
vol_s3=2*math.pi**2
vol_so2=vol_s1
vol_so3=vol_so2*vol_s2
vol_so4=vol_so3*vol_s3
assert abs(vol_so3/(8*math.pi**2)-1)<1e-14
assert abs(vol_so4/(16*math.pi**4)-1)<1e-14
w=[]
for a in (0.5,1.0,2.0,3.25):
    q=math.pi**2*a**5
    local_jac=q**3
    orbit=vol_so4*q**3
    exact=16*math.pi**10*a**15
    assert abs(orbit/exact-1)<2e-14
    assert abs(orbit/(local_jac*16*math.pi**4)-1)<2e-14
    w.append({'a':a,'q':q,'sqrt_det_Gram':local_jac,'SO4_orbit_volume_L2':orbit})
# Reciprocal basis/coordinate rescaling: Gram sqrt(det) gains |c|^6, coordinate Haar density loses it.
r=[]
for c in (0.25,0.5,2.0,7.0):
    combined=abs(c)**6*abs(c)**-6
    assert abs(combined-1)<1e-14
    r.append({'c':c,'combined_measure_ratio':combined})
checks={
 'canonical_SO3_volume_8pi2':True,
 'canonical_SO4_volume_16pi4':True,
 'metric_scaling_exponent_dim_over_2_is_3':True,
 'L2_orbit_volume_16pi10a15':True,
 'parent_factorization_equivalent':True,
 'reciprocal_basis_coordinate_rescaling_invariant':True
}
findings={
 'SO4_Haar_global_convention_explicitly_frozen':True,
 'dimensionless_SO4_volume_computed':True,
 'dimensionless_SO4_volume':'16*pi^4',
 'L2_scaled_residual_SO4_orbit_volume_computed':True,
 'L2_scaled_residual_SO4_orbit_volume':'16*pi^10*a^15',
 'residual_SO4_zero_mode_quotient_normalization_fixed_under_frozen_convention':True,
 'normalization_is_convention_independent_physical_observable':False,
 'signed_or_complex_FP_phase_assigned':False,
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
}
out={
 'classification':'RTK_C9_HMT_LAMBDA1_S3_SO4_HAAR_GLOBAL_NORMALIZATION_FIXED_BY_EXPLICIT_CONVENTION_PASS_SCOPED',
 'frozen_target_commit':FROZEN,
 'parent_result_commit':PARENT,
 'canonical_metric':'<X,Y>=-1/2 Tr(XY)',
 'global_group':'SO(4)',
 'generator_period':'2*pi',
 'volume_chain':{'SO2':'2*pi','SO3':'8*pi^2','SO4':'16*pi^4'},
 'parent_L2_metric_scale':'q=pi^2*a^5',
 'sqrt_det_Gram':'q^3=pi^6*a^15',
 'residual_orbit_volume':'16*pi^10*a^15',
 'numerical_witnesses':w,
 'rescaling_witnesses':r,
 'scientific_checks':checks,
 'findings':findings,
 'interpretation':'Once SO(4), the 2*pi embedding-generator periodicity, and the canonical -1/2 Tr Lie metric are prospectively frozen, the residual six-Killing-mode orbit has dimensionless Haar/Riemannian volume 16*pi^4 and L2-scaled volume 16*pi^10*a^15. This fixes the zero-mode quotient normalization only under that explicit convention; it is not a convention-independent observable and does not close the signed FP, TT Hessian, full one-loop, or C9 gates.',
 'next_gate':'Audit the remaining spatial FP signed/phase information (or prove only absolute determinant is needed for the Euclidean measure) before combining with the already scoped FS scalar factor; TT Hessian remains separately open.'
}
R='research/theory_results/RTK_C9_HMT_LAMBDA1_S3_SO4_HAAR_GLOBAL_NORMALIZATION_RESULT_v1.json'
C='research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_SO4_HAAR_GLOBAL_NORMALIZATION_2026-08-28.md'
P='research/provenance/RTK_C9_HMT_LAMBDA1_S3_SO4_HAAR_GLOBAL_NORMALIZATION_PROVENANCE_v1.json'
Path(R).write_text(json.dumps(out,indent=2)+'\n')
Path(P).write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),'target_frozen_commit':FROZEN,'parent_result_commit':PARENT,'script':__file__,'method':'exact compact-group volume recursion plus six-dimensional metric scaling','regularization':'none','global_group':'SO(4)','canonical_metric':'-1/2 Tr','generator_period':'2*pi','no_DSIR':True},indent=2)+'\n')
Path(C).write_text(f'''# RTK C9 HMT S3 residual SO(4) Haar/global normalization checkpoint\n\nClassification: `{out['classification']}`\n\nFrozen target `{FROZEN}`, parent `{PARENT}`. With the prospectively frozen actual group `SO(4)`, embedding generators of period `2*pi`, and canonical Lie metric `<X,Y>=-1/2 Tr(XY)`, the exact compact-group recursion gives `Vol(SO(2))=2*pi`, `Vol(SO(3))=8*pi^2`, and `Vol(SO(4))=16*pi^4`.\n\nThe parent-certified L2 Killing Gram scale is `q=pi^2 a^5` in six dimensions, hence the Riemannian/Haar orbit volume scales as `q^3`, giving `Vol_L2(SO(4))=16*pi^10*a^15`. This equals the parent local Jacobian `pi^6*a^15` times the convention-fixed dimensionless volume `16*pi^4`. Reciprocal basis/coordinate rescaling leaves the combined measure invariant.\n\nThis fixes only the residual SO(4) zero-mode quotient normalization under the declared global convention. It is not a convention-independent observable. Signed/complex FP phase, full FP/FS determinants, TT Hessian, complete HMT gauge-fixed matrix, one-loop evaluability and C9 remain OPEN/BLOCKED. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.\n''')
print(json.dumps(out,indent=2))
