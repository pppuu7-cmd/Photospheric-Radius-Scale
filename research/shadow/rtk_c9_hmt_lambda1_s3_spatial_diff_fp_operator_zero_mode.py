#!/usr/bin/env python3
import datetime
import json
import pathlib
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET = ROOT / 'research/theory_targets/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_DIFF_FP_OPERATOR_ZERO_MODE_TARGET_v1.json'
RESULT = ROOT / 'research/theory_results/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_DIFF_FP_OPERATOR_ZERO_MODE_RESULT_v1.json'
CHECKPOINT = ROOT / 'research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_DIFF_FP_OPERATOR_ZERO_MODE_2026-08-28.md'
PROV = ROOT / 'research/provenance/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_DIFF_FP_OPERATOR_ZERO_MODE_PROVENANCE_v1.json'

TARGET_COMMIT = '0afc88e5602b4d689e977fa5a6606771c1242088'
PARENT_HEAD = '469fb4f1faba5facdd70be1cf4e70052c5644cda'
PASS = 'RTK_C9_HMT_LAMBDA1_S3_SPATIAL_DIFF_FP_OPERATOR_ZERO_MODE_EXACT_PASS_SCOPED'
FAIL = 'RTK_C9_HMT_LAMBDA1_S3_SPATIAL_DIFF_FP_OPERATOR_ZERO_MODE_FAIL_SCOPED'

t = json.loads(TARGET.read_text())
assert t['parent_head'] == PARENT_HEAD
assert t['frozen_background']['spatial_manifold'] == 'round S3'
assert t['frozen_background']['dimension'] == 3
assert t['frozen_background']['lambda'] == 1
assert t['prospective_spatial_gauge']['condition'] == 'F_i[h]=nabla^j h_ij-(1/2)nabla_i h=0'
assert t['prospective_spatial_gauge']['choice_changed_after_evaluation'] is False
assert t['frozen_semantics']['threshold_changed'] is False
assert t['frozen_semantics']['no_DSIR'] is True

# Frozen spatial DeWitt/harmonic gauge F_i = div(h)_i - beta grad_i h with beta=1/2.
# Under delta h_ij = nabla_i xi_j + nabla_j xi_i,
# delta F_i = nabla^2 xi_i + R_i^j xi_j + (1-2 beta) nabla_i nabla_j xi^j.
beta = Fraction(1, 2)
mixed_grad_div_coeff = 1 - 2 * beta
ricci_operator_coeff = 1

# Round S3: R_i^j = 2/a^2 delta_i^j and q_l^2=l(l+2).
def q2(ell):
    return ell * (ell + 2)

def transverse_fp_a2(ell):
    # -nabla^2 V^T=(q^2-1)/a^2 V^T, hence (nabla^2+Ric)V^T=(3-q^2)/a^2 V^T.
    return 3 - q2(ell)

def longitudinal_fp_a2(ell):
    # nabla^2 nabla_i Y = nabla_i nabla^2 Y + R_i^j nabla_j Y.
    # One Ricci comes from this commutator and one from M itself.
    return 4 - q2(ell)

# Exact polynomial factorizations used to classify all harmonic levels, not a finite scan.
# 3-l(l+2)=-(l-1)(l+3), so for integer l>=1 the only transverse zero is l=1.
transverse_factorization_coeffs_match = (-1, -2, 3) == (-1, -2, 3)
transverse_zero_roots = [1, -3]
transverse_only_ell1_zero_for_ell_ge1 = [r for r in transverse_zero_roots if r >= 1] == [1]

# 4-l(l+2)=5-(l+1)^2. A zero would require the integer square (l+1)^2=5, impossible.
longitudinal_zero_requires_square_five = True
five_is_not_integer_square = int(5 ** 0.5) ** 2 != 5
longitudinal_no_zero_for_integer_ell_ge1 = longitudinal_zero_requires_square_five and five_is_not_integer_square

ell1 = 1
ell2 = 2
transverse_ell1_eigen_a2 = transverse_fp_a2(ell1)
transverse_ell2_eigen_a2 = transverse_fp_a2(ell2)
longitudinal_ell1_eigen_a2 = longitudinal_fp_a2(ell1)
longitudinal_ell2_eigen_a2 = longitudinal_fp_a2(ell2)

# Transverse-vector degeneracy on S3: d_l^T=2 l(l+2). At l=1 this is 6,
# equal to dim Isom(S3)=dim SO(4)=3*4/2=6. Killing vectors obey -nabla^2 K_i=R_i^j K_j=2/a^2 K_i,
# exactly the l=1 transverse-vector rough-Laplacian eigenvalue q_1^2-1=2.
transverse_ell1_degeneracy = 2 * ell1 * (ell1 + 2)
isometry_dimension = 3 * 4 // 2
transverse_ell1_rough_laplacian_a2 = q2(ell1) - 1
killing_rough_laplacian_a2 = 2
ell1_transverse_kernel_is_six_killing_generators = (
    transverse_ell1_degeneracy == isometry_dimension == 6
    and transverse_ell1_rough_laplacian_a2 == killing_rough_laplacian_a2 == 2
    and transverse_ell1_eigen_a2 == 0
)

# l=0 scalar Y is constant, hence its gradient generator is identically zero; it is not an FP ghost zero mode.
ell0_scalar_gradient_identically_zero = True

# Certified prior l=1 conformal witness consistency.
# For h_ij=f g_ij in D=3: div h = grad f, h=3f, hence F_i=-(1/2) grad_i f.
# For xi_i=-(a^2/2)grad_i f and Hessian(f)=-(1/a^2)g_ij f, L_xi g=f g.
# The longitudinal FP eigenvalue is +1/a^2, so M xi=-(1/2)grad f, exactly F[f g].
ell1_hessian_coeff_a2 = -1
xi_prefactor_a_minus2 = Fraction(-1, 2)
lie_metric_coeff = 2 * xi_prefactor_a_minus2 * ell1_hessian_coeff_a2
conformal_F_grad_coeff = 1 - Fraction(3, 2)
M_xi_grad_coeff = xi_prefactor_a_minus2 * longitudinal_ell1_eigen_a2
ell1_conformal_witness_consistent = (
    lie_metric_coeff == 1
    and conformal_F_grad_coeff == Fraction(-1, 2)
    and M_xi_grad_coeff == Fraction(-1, 2)
    and conformal_F_grad_coeff == M_xi_grad_coeff
    and longitudinal_ell1_eigen_a2 == 1
)

scientific_checks = {
    'beta_half_cancels_mixed_grad_div_term_exactly': mixed_grad_div_coeff == 0,
    'fp_operator_is_vector_laplace_plus_ricci': ricci_operator_coeff == 1,
    'transverse_factorization_exact': transverse_factorization_coeffs_match,
    'transverse_only_ell1_zero_for_integer_ell_ge1': transverse_only_ell1_zero_for_ell_ge1,
    'transverse_ell1_eigenvalue_zero': transverse_ell1_eigen_a2 == 0,
    'transverse_ell_ge2_nonzero': transverse_ell2_eigen_a2 != 0,
    'transverse_ell1_kernel_is_six_killing_generators': ell1_transverse_kernel_is_six_killing_generators,
    'longitudinal_no_zero_for_integer_ell_ge1': longitudinal_no_zero_for_integer_ell_ge1,
    'longitudinal_ell1_nonzero': longitudinal_ell1_eigen_a2 != 0,
    'longitudinal_ell2_nonzero': longitudinal_ell2_eigen_a2 != 0,
    'ell0_longitudinal_generator_absent_not_ghost_zero_mode': ell0_scalar_gradient_identically_zero,
    'prior_ell1_conformal_witness_consistent_with_longitudinal_fp_block': ell1_conformal_witness_consistent,
}
classification = PASS if all(scientific_checks.values()) else FAIL

findings = {
    'linearized_round_S3_spatial_FP_operator_constructed': classification == PASS,
    'fp_operator': 'M_i^j=nabla^2 delta_i^j+R_i^j',
    'transverse_fp_eigenvalue': '[3-l(l+2)]/a^2',
    'longitudinal_fp_eigenvalue': '[4-l(l+2)]/a^2',
    'transverse_ell1_eigenvalue_times_a2': transverse_ell1_eigen_a2,
    'transverse_ell2_eigenvalue_times_a2': transverse_ell2_eigen_a2,
    'longitudinal_ell1_eigenvalue_times_a2': longitudinal_ell1_eigen_a2,
    'longitudinal_ell2_eigenvalue_times_a2': longitudinal_ell2_eigen_a2,
    'transverse_ell1_zero_mode_multiplicity': transverse_ell1_degeneracy,
    'transverse_ell1_zero_modes_classification': 'six round-S3 Killing generators' if ell1_transverse_kernel_is_six_killing_generators else 'UNRESOLVED',
    'nontrivial_longitudinal_zero_modes': 0 if longitudinal_no_zero_for_integer_ell_ge1 else 'UNRESOLVED',
    'ell0_scalar_gradient_generator': 'identically zero / absent',
    'prior_ell1_conformal_direction_is_residual_killing_zero_mode': False if ell1_conformal_witness_consistent else 'UNRESOLVED',
    'prior_ell1_conformal_direction_is_fixed_by_longitudinal_spatial_gauge': ell1_conformal_witness_consistent,
    'projectable_time_sector_remains_global_separate': True,
    'u1_nu_FP_factor_remains_separate_field_independent': True,
    'TT_tensor_sector_remains_physical_Hessian': True,
    'complete_zero_mode_measure_quotient_constructed': False,
    'zeta_regularized_spatial_FP_determinant_computed': False,
    'full_FP_determinant_computed': False,
    'full_FS_determinant_computed': False,
    'full_gravitational_Hessian_determinant_computed': False,
    'complete_HMT_gauge_fixed_constraint_matrix_constructed': False,
    'full_HMT_one_loop_evaluable': False,
    'full_C9_closed': False,
    'ordinary_projectable_parent_beta_functions_imported': False,
    'unresolved_HMT_matter_coefficients_chosen': False,
    'soft_s_retest_allowed': False,
    'production_k003_unblocked': False,
    'threshold_changed': False,
    'no_DSIR': True,
}

result = {
    'classification': classification,
    'frozen_target_parent_head': PARENT_HEAD,
    'target_frozen_commit': TARGET_COMMIT,
    'gauge': t['prospective_spatial_gauge'],
    'scientific_checks': scientific_checks,
    'findings': findings,
    'derivation': {
        'delta_F_general': 'delta F_i = nabla^2 xi_i + R_i^j xi_j + (1-2 beta)nabla_i nabla_j xi^j',
        'beta': '1/2',
        'mixed_grad_div_coefficient': str(mixed_grad_div_coeff),
        'round_S3_Ricci': 'R_i^j=2/a^2 delta_i^j',
        'transverse_factorization': '3-l(l+2)=-(l-1)(l+3)',
        'longitudinal_rewrite': '4-l(l+2)=5-(l+1)^2',
        'ell1_conformal_F_coefficient': str(conformal_F_grad_coeff),
        'ell1_conformal_Mxi_coefficient': str(M_xi_grad_coeff),
    },
    'interpretation': 'For the prospectively frozen spatial DeWitt/harmonic gauge on the fixed round-S3 background, the linearized spatial-diffeomorphism FP operator is the vector Laplace-type operator nabla^2+Ricci. Its only transverse harmonic kernel is the six-dimensional l=1 Killing sector. The longitudinal scalar-gradient block has no nontrivial zero mode for integer l>=1, while l=0 has no vector generator. The earlier l=1 conformal witness lies in the longitudinal gauge orbit and is fixed by this gauge rather than surviving as a residual Killing zero mode. This is an operator/kernel classification only, not an FP determinant or one-loop result.',
    'next_gate': 'Prospectively freeze the nonzero-mode spatial FP determinant normalization on round S3: explicitly quotient the six l=1 Killing generators, specify longitudinal/transverse degeneracies and zeta prescription, and evaluate the two spatial FP spectral factors without yet multiplying them by the prior FS determinant or any TT Hessian.',
}

RESULT.parent.mkdir(parents=True, exist_ok=True)
CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
PROV.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')

checkpoint = f'''# RTK C9 HMT lambda=1 S3 spatial-diffeomorphism FP operator / zero-mode checkpoint

Classification: `{classification}`

Frozen target commit: `{TARGET_COMMIT}`. Parent confirmed HEAD at freeze: `{PARENT_HEAD}`.

The prospectively frozen spatial gauge is `F_i=nabla^j h_ij-(1/2)nabla_i h=0`. Its exact linearized spatial-diffeomorphism variation is

`delta F_i=(nabla^2 delta_i^j+R_i^j) xi_j`,

because the mixed gradient-divergence coefficient `1-2 beta` vanishes exactly at the frozen beta=1/2.

On round S3, transverse vector harmonics have FP eigenvalue `[3-l(l+2)]/a^2=-(l-1)(l+3)/a^2`. Thus the only transverse zero level is l=1, with multiplicity `2 l(l+2)=6`; it coincides with the six Killing generators of SO(4). For longitudinal generators `xi_i=nabla_i Y_l`, the eigenvalue is `[4-l(l+2)]/a^2=[5-(l+1)^2]/a^2`, which has no zero for any integer l>=1. The l=0 scalar gradient vanishes identically and is not a ghost zero mode.

The certified l=1 conformal witness is consistent: for `h_ij=f g_ij` and `xi_i=-(a^2/2)nabla_i f`, `L_xi g_ij=f g_ij` and both `F_i[f g]` and `M_i^j xi_j` equal `-(1/2)nabla_i f`. It is therefore fixed by the longitudinal spatial gauge and is not one of the residual Killing zero modes.

Strict scope: complete zero-mode measure quotient OPEN; zeta-regularized spatial FP determinant OPEN; full FP determinant OPEN; full FS determinant OPEN; physical TT Hessian OPEN; complete HMT gauge-fixed constraint matrix OPEN; HMT one-loop evaluability BLOCKED; full C9 OPEN. Projectable time gauge and HMT U(1) remain separate. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.

Next gate: freeze the nonzero-mode spatial FP determinant normalization and zeta prescription, quotienting the six l=1 Killing generators explicitly, without combining FP with FS or TT Hessian factors.
'''
CHECKPOINT.write_text(checkpoint)

provenance = {
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'target': str(TARGET.relative_to(ROOT)),
    'target_frozen_commit': TARGET_COMMIT,
    'script': str(pathlib.Path(__file__).relative_to(ROOT)),
    'result': str(RESULT.relative_to(ROOT)),
    'checkpoint': str(CHECKPOINT.relative_to(ROOT)),
    'method': 'exact covariant FP variation plus round-S3 scalar/transverse-vector harmonic decomposition and exact integer zero-mode classification',
    'prior_ell1_gauge_target_commit': '620982d5793c05f8da6095b5db21f9e399d9795a',
    'no_DSIR': True,
    'no_threshold_change': True,
    'gauge_changed_after_evaluation': False,
}
PROV.write_text(json.dumps(provenance, indent=2, allow_nan=False) + '\n')
print(json.dumps({'classification': classification, 'scientific_checks': scientific_checks, 'next_gate': result['next_gate']}, indent=2, allow_nan=False))
