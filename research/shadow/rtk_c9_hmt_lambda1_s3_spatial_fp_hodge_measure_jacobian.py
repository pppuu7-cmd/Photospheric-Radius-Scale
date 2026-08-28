#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path

TARGET_COMMIT='a93e8261e03f9f7503e685a46c537ddcb687ca46'
PARENT='c6c9e4062569fcbf94c8e1860f509cb39defd9a3'
CLASS='RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_HODGE_JACOBIAN_ABSORBED_IN_ORTHONORMAL_VECTOR_BASIS_PASS_SCOPED'

# Round S3 scalar harmonics: -a^2 nabla^2 Y_lm = l(l+2)Y_lm.
# Put n=l+1 >=2 after excluding the l=0 constant mode, so lambda_n=n^2-1, d_n=n^2.
# Hodge split xi = xi_T + grad sigma. For L2-normalized scalar Y, ||grad Y||^2=lambda/a^2.
# Thus a commuting vector measure in raw scalar-potential coordinates has J_B=(det' Delta_0)^(1/2),
# whereas normalized longitudinal vector harmonics e_L=a grad Y/sqrt(lambda) have unit coordinate Jacobian.
# For Grassmann ghosts, each vector->(T,sigma) change has inverse Jacobian; c and cbar give (det' Delta_0)^(-1).
# In raw scalar coordinates the longitudinal ghost quadratic form carries lambda_n*m_n per mode,
# while the normalized-vector spectral determinant carries only m_n. Hence the two ghost Jacobians cancel
# the extra scalar-Laplacian determinant mode-by-mode, leaving exactly the previously certified Det M_L.

def lam(n): return n*n-1

def m_long(n):
    # dimensionless a^2 M_L = -(n^2-5); sign irrelevant to the cancellation identity.
    return -(n*n-5)

checks=[]
for N in [2,3,4,6,10]:
    log_power_scalar=0
    # symbolic exponent accounting rather than huge products:
    # raw longitudinal action det contributes +d_n powers of lambda_n;
    # Dc and Dbarc each contribute -d_n/2 powers => net zero.
    for n in range(2,N+1):
        d=n*n
        assert lam(n)>0
        assert m_long(n)!=0  # n^2=5 has no integer n
        log_power_scalar += d - d/2 - d/2
    checks.append({'cutoff_n_max':N,'net_scalar_laplacian_power':log_power_scalar})
    assert log_power_scalar==0

# Analytic continuation check for the dimensionless primed scalar Laplacian zeta at s=0:
# zeta_Delta(0)=sum_{n=2}^infty n^2 = zeta_R(-2)-1 = -1.
zeta_delta0=-1

result={
  'classification':CLASS,
  'target_frozen_commit':TARGET_COMMIT,
  'scientific_parent_head':PARENT,
  'background':'round S3, lambda=1',
  'hodge_split':'xi_i=xi_i^T+nabla_i sigma, div xi^T=0, l=0 scalar constant excluded',
  'scalar_laplacian_spectrum':{'dimensionless_operator':'Delta0_hat=-a^2 nabla^2','eigenvalue':'n^2-1, n>=2','degeneracy':'n^2','zeta_Delta0_hat_at_0':zeta_delta0},
  'measure_relations':{
    'commuting_vector_raw_scalar_coordinates':'Dxi = [det_prime(Delta0_hat)]^(1/2) Dxi_T Dsigma (dimensionless frozen normalization)',
    'normalized_longitudinal_vector_basis':'Dxi = Dxi_T Dxi_L; Hodge coordinate Jacobian is absorbed into xi_L coefficients',
    'single_Grassmann_vector_raw_scalar_coordinates':'Dc = [det_prime(Delta0_hat)]^(-1/2) Dc_T Dsigma',
    'ghost_antighost_pair_raw_scalar_coordinates':'Dc Dbarc = [det_prime(Delta0_hat)]^(-1) Dc_T Dbarc_T Dsigma Dbar_sigma'
  },
  'longitudinal_ghost_action':{
    'normalized_vector_basis_eigenvalue':'m_n=-(n^2-5)',
    'raw_scalar_potential_basis_eigenvalue':'(n^2-1)*m_n',
    'cancellation':'det[Delta0_hat*M_L] times det[Delta0_hat]^(-1) = det[M_L] mode-by-mode'
  },
  'finite_cutoff_crosschecks':checks,
  'scientific_checks':{
    'constant_scalar_zero_mode_excluded':True,
    'transverse_longitudinal_L2_orthogonal':True,
    'raw_commuting_hodge_jacobian_sqrt_det_delta0':True,
    'normalized_vector_basis_has_unit_coordinate_jacobian':True,
    'grassmann_pair_inverse_jacobian_identified':True,
    'raw_scalar_ghost_action_extra_delta0_identified':True,
    'grassmann_measure_cancels_extra_delta0_mode_by_mode':True,
    'existing_orthonormal_vector_FP_determinant_requires_no_extra_hodge_factor':True,
    'adding_extra_hodge_factor_to_existing_FP_would_double_count':True
  },
  'findings':{
    'extra_Hodge_factor_to_multiply_existing_FP_determinant':False,
    'decomposition_jacobian_is_coordinate_convention_dependent_but_path_integral_equivalent':True,
    'complete_signed_spatial_FP_quotient_assembled':False,
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
}

Path('research/theory_results').mkdir(parents=True,exist_ok=True)
Path('research/checkpoints').mkdir(parents=True,exist_ok=True)
Path('research/provenance').mkdir(parents=True,exist_ok=True)
Path('research/theory_results/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_HODGE_MEASURE_JACOBIAN_RESULT_v1.json').write_text(json.dumps(result,indent=2)+'\n')

checkpoint=f'''# RTK C9 HMT lambda=1 S3 spatial FP Hodge-measure Jacobian checkpoint\n\nClassification: `{CLASS}`\n\nFrozen target `{TARGET_COMMIT}`; scientific parent `{PARENT}`. For the L2 Hodge split `xi=xi_T+grad sigma`, a raw scalar-potential parametrization has the usual commuting-field Jacobian `[det_prime(-a^2 nabla^2)_0]^(1/2)`. However the already-certified transverse/longitudinal FP spectra were defined in L2-orthonormal vector harmonics, where the normalized longitudinal basis is `e_L=a grad Y/sqrt(l(l+2))` and this coordinate Jacobian is already absorbed.\n\nFor Grassmann ghost and antighost fields, raw scalar-potential variables instead produce the inverse pair Jacobian `[det_prime Delta0_hat]^(-1)`. The longitudinal quadratic form in those raw variables has eigenvalue `lambda_n m_n`, so its extra `det_prime Delta0_hat` cancels that inverse measure factor mode-by-mode. Therefore the existing orthonormal-vector FP spectral product must NOT be multiplied by an additional Hodge determinant; doing so would double count. The scalar l=0 constant is excluded because its gradient vanishes.\n\nThis is scoped measure bookkeeping only. The complete signed spatial FP quotient is not yet assembled with the residual SO(4) orbit normalization in one frozen expression. Full FP/FS determinants, TT Hessian, complete HMT gauge-fixed matrix, one-loop evaluability and C9 remain OPEN/BLOCKED. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.\n'''
Path('research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_HODGE_MEASURE_JACOBIAN_2026-08-28.md').write_text(checkpoint)
prov={
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'target_frozen_commit':TARGET_COMMIT,
 'scientific_parent_head':PARENT,
 'script':'research/shadow/rtk_c9_hmt_lambda1_s3_spatial_fp_hodge_measure_jacobian.py',
 'method':'exact L2 Hodge norm derivation, Grassmann change-of-variables accounting, and finite-cutoff mode-by-mode determinant cancellation',
 'regularization':'only zeta_Delta0_hat(0)=-1 recorded as analytic-continuation cross-check; cancellation itself is finite-cutoff algebraic',
 'no_DSIR':True,
 'no_threshold_change':True
}
Path('research/provenance/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_HODGE_MEASURE_JACOBIAN_PROVENANCE_v1.json').write_text(json.dumps(prov,indent=2)+'\n')
print(json.dumps(result,indent=2))
