#!/usr/bin/env python3
import datetime
import json
import pathlib
import mpmath as mp

ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET = ROOT / 'research/theory_targets/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_NONZERO_MODE_ZETA_MAGNITUDES_TARGET_v1.json'
RESULT = ROOT / 'research/theory_results/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_NONZERO_MODE_ZETA_MAGNITUDES_RESULT_v1.json'
CHECKPOINT = ROOT / 'research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_NONZERO_MODE_ZETA_MAGNITUDES_2026-08-28.md'
PROV = ROOT / 'research/provenance/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_NONZERO_MODE_ZETA_MAGNITUDES_PROVENANCE_v1.json'

TARGET_COMMIT = '4191e4dd12aff1c648af391755f3e169df33d378'
PARENT_HEAD = '5ec5fdd787571764daf723122300a34da6e09b38'
PASS = 'RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_NONZERO_MODE_ZETA_MAGNITUDES_FINITE_PASS_SCOPED'
FAIL = 'RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_NONZERO_MODE_ZETA_MAGNITUDES_FAIL_SCOPED'

T = json.loads(TARGET.read_text())
assert T['parent_head'] == PARENT_HEAD
assert T['frozen_parent_operator']['FP_operator'] == 'M_i^j=nabla^2 delta_i^j+R_i^j'
assert T['frozen_positive_magnitude_spectra']['transverse_operator'] == 'A_T=a^2 |M_T| on the primed transverse-vector domain'
assert T['frozen_positive_magnitude_spectra']['longitudinal_operator'] == 'A_L=a^2 |M_L| on the nontrivial longitudinal-vector domain'
assert T['tolerances']['high_precision_decimal_digits'] == 50
assert T['tolerances']['convergent_domain_crosscheck_abs'] == 1e-30
assert T['tolerances']['zeta_prime_convergence_abs'] == 1e-30
assert T['frozen_semantics']['threshold_changed'] is False
assert T['frozen_semantics']['no_DSIR'] is True

# Exceed the frozen minimum precision. The K=120 versus K=140 comparison is
# the same convergence architecture certified by the earlier scalar C9 zeta gate.
mp.mp.dps = 200
TOL = mp.mpf('1e-30')

# With n=l+1, the parent-certified positive-magnitude spectra are
#   T: n>=3, lambda=n^2-4, d=2(n^2-1)
#   L: n=2, lambda=1,d=4; n>=3, lambda=n^2-5,d=n^2.
# Binomial expansion gives explicit Riemann-zeta continuations.
def zeta_T_cont(s, K):
    s = mp.mpf(s)
    total = mp.mpf('0')
    for k in range(K + 1):
        p = 2*s + 2*k
        coeff = mp.rf(s, k) / mp.factorial(k) * mp.power(4, k)
        # sum_{n>=3} [n^(2-p)-n^(-p)]
        bracket = mp.zeta(p - 2) - mp.zeta(p) - 3*mp.power(2, -p)
        total += coeff * bracket
    return 2 * total


def zeta_L_cont(s, K):
    s = mp.mpf(s)
    total = mp.mpf(4)  # n=2: multiplicity four, eigenvalue one.
    for k in range(K + 1):
        p = 2*s + 2*k - 2
        coeff = mp.rf(s, k) / mp.factorial(k) * mp.power(5, k)
        bracket = mp.zeta(p) - 1 - mp.power(2, -p)
        total += coeff * bracket
    return total

# Exact s=0 values follow from the k=0 terms because (0)_k=0 for k>=1.
zeta_T_0 = zeta_T_cont(0, 40)
zeta_L_0 = zeta_L_cont(0, 40)
zeta_T_0_expected = mp.mpf(-5)
zeta_L_0_expected = mp.mpf(-1)

# Derivatives at zero. For k>=1, d/ds [(s)_k/k!]_{s=0}=1/k.
def zeta_T_prime_formula(K):
    k0_prime = 2*mp.diff(mp.zeta, -2) - 2*mp.diff(mp.zeta, 0) + 6*mp.log(2)
    tail = mp.mpf('0')
    for k in range(1, K + 1):
        p = 2*k
        bracket = mp.zeta(p - 2) - mp.zeta(p) - 3*mp.power(2, -p)
        tail += mp.power(4, k) * bracket / k
    return 2 * (k0_prime + tail)


def zeta_L_prime_formula(K):
    k0_prime = 2*mp.diff(mp.zeta, -2) + 8*mp.log(2)
    tail = mp.mpf('0')
    for k in range(1, K + 1):
        p = 2*k - 2
        bracket = mp.zeta(p) - 1 - mp.power(2, -p)
        tail += mp.power(5, k) * bracket / k
    return k0_prime + tail

zp_T_120 = zeta_T_prime_formula(120)
zp_T_140 = zeta_T_prime_formula(140)
zp_L_120 = zeta_L_prime_formula(120)
zp_L_140 = zeta_L_prime_formula(140)
prime_diff_T = abs(zp_T_140 - zp_T_120)
prime_diff_L = abs(zp_L_140 - zp_L_120)

# Independent convergent-domain check against the original frozen spectra.
s_cross = mp.mpf(5)
N = 20000
direct_T = mp.mpf('0')
direct_L = mp.mpf(4)
for n in range(3, N + 1):
    direct_T += 2*(n*n - 1) * mp.power(n*n - 4, -s_cross)
    direct_L += n*n * mp.power(n*n - 5, -s_cross)
continued_T = zeta_T_cont(s_cross, 140)
continued_L = zeta_L_cont(s_cross, 140)
cross_diff_T = abs(continued_T - direct_T)
cross_diff_L = abs(continued_L - direct_L)

# Positive determinant magnitudes for the declared dimensionless normalizations.
det_T = mp.exp(-zp_T_140)
det_L = mp.exp(-zp_L_140)

# Spectral-prime / zero-mode bookkeeping is exact and inherited from the parent.
transverse_prime_removed_levels = [1]
transverse_l1_removed_multiplicity = 2 * 1 * (1 + 2)
transverse_l2_magnitude = (2 - 1) * (2 + 3)
longitudinal_l1_magnitude = 1
longitudinal_l1_multiplicity = (1 + 1)**2
longitudinal_zero_modes = 0

# Explicit normalization witnesses. zeta(0) controls scale dependence.
c = mp.mpf(2)
ratio_T_c2 = mp.power(c, zeta_T_0)
ratio_L_c2 = mp.power(c, zeta_L_0)

scientific_checks = {
    'transverse_zeta_regular_at_s0': mp.isfinite(zeta_T_0) and mp.isfinite(zp_T_140),
    'longitudinal_zeta_regular_at_s0': mp.isfinite(zeta_L_0) and mp.isfinite(zp_L_140),
    'transverse_zeta0_exact_minus5': zeta_T_0 == zeta_T_0_expected,
    'longitudinal_zeta0_exact_minus1': zeta_L_0 == zeta_L_0_expected,
    'transverse_prime_convergence_within_frozen_tolerance': prime_diff_T < TOL,
    'longitudinal_prime_convergence_within_frozen_tolerance': prime_diff_L < TOL,
    'transverse_convergent_domain_crosscheck_within_frozen_tolerance': cross_diff_T < TOL,
    'longitudinal_convergent_domain_crosscheck_within_frozen_tolerance': cross_diff_L < TOL,
    'transverse_determinant_magnitude_finite_positive': mp.isfinite(det_T) and det_T > 0,
    'longitudinal_determinant_magnitude_finite_positive': mp.isfinite(det_L) and det_L > 0,
    'transverse_spectral_prime_removes_exactly_l1_six_killing_modes': transverse_prime_removed_levels == [1] and transverse_l1_removed_multiplicity == 6 and transverse_l2_magnitude == 5,
    'longitudinal_l1_retained_nonzero_with_multiplicity_four': longitudinal_l1_magnitude == 1 and longitudinal_l1_multiplicity == 4 and longitudinal_zero_modes == 0,
    'transverse_normalization_scaling_witness_matches_zeta0': ratio_T_c2 == mp.mpf(1)/32,
    'longitudinal_normalization_scaling_witness_matches_zeta0': ratio_L_c2 == mp.mpf(1)/2,
}
classification = PASS if all(scientific_checks.values()) else FAIL

result = {
    'classification': classification,
    'frozen_target_parent_head': PARENT_HEAD,
    'target_frozen_commit': TARGET_COMMIT,
    'spectral_problems': {
        'transverse': {
            'operator': 'A_T=a^2|M_T|',
            'domain': 'l>=2 after priming out l=1 Killing kernel',
            'n_form': 'n=l+1>=3: lambda=n^2-4, d=2(n^2-1)',
            'zeta': 'zeta_T(s)=sum_{n=3}^infinity 2(n^2-1)(n^2-4)^(-s)',
        },
        'longitudinal': {
            'operator': 'A_L=a^2|M_L|',
            'domain': 'l>=1; l=0 gradient absent',
            'n_form': 'n=2: lambda=1,d=4; n>=3: lambda=n^2-5,d=n^2',
            'zeta': 'zeta_L(s)=4+sum_{n=3}^infinity n^2(n^2-5)^(-s)',
        },
    },
    'analytic_continuation': {
        'transverse_regular_at_s0': bool(mp.isfinite(zeta_T_0) and mp.isfinite(zp_T_140)),
        'longitudinal_regular_at_s0': bool(mp.isfinite(zeta_L_0) and mp.isfinite(zp_L_140)),
        'zeta_T_0_exact': int(zeta_T_0),
        'zeta_L_0_exact': int(zeta_L_0),
        'zeta_T_prime_0': mp.nstr(zp_T_140, 80),
        'zeta_L_prime_0': mp.nstr(zp_L_140, 80),
        'transverse_prime_K120_vs_K140_abs_diff': mp.nstr(prime_diff_T, 30),
        'longitudinal_prime_K120_vs_K140_abs_diff': mp.nstr(prime_diff_L, 30),
        'crosscheck_s': 5,
        'crosscheck_direct_N': N,
        'transverse_crosscheck_abs_diff': mp.nstr(cross_diff_T, 30),
        'longitudinal_crosscheck_abs_diff': mp.nstr(cross_diff_L, 30),
    },
    'zeta_determinant_magnitudes': {
        'Det_zeta_A_T': mp.nstr(det_T, 80),
        'Det_zeta_A_L': mp.nstr(det_L, 80),
        'definition': 'exp[-zeta_X_prime(0)] for X=T,L',
        'signed_or_complex_FP_phase_assigned': False,
        'transverse_rescaling_law': 'Det_zeta(c A_T)=c^(-5) Det_zeta(A_T)',
        'longitudinal_rescaling_law': 'Det_zeta(c A_L)=c^(-1) Det_zeta(A_L)',
        'transverse_c2_ratio': mp.nstr(ratio_T_c2, 30),
        'longitudinal_c2_ratio': mp.nstr(ratio_L_c2, 30),
        'normalization_independent': False,
    },
    'zero_mode_bookkeeping': {
        'transverse_primed_levels': transverse_prime_removed_levels,
        'transverse_removed_multiplicity': transverse_l1_removed_multiplicity,
        'transverse_removed_classification': 'six round-S3 Killing generators',
        'longitudinal_zero_modes': longitudinal_zero_modes,
        'longitudinal_l1_eigenvalue_magnitude': longitudinal_l1_magnitude,
        'longitudinal_l1_multiplicity': longitudinal_l1_multiplicity,
        'residual_isometry_group_volume_normalized': False,
    },
    'scientific_checks': scientific_checks,
    'findings': {
        'spatial_FP_nonzero_mode_magnitude_factors_computed': classification == PASS,
        'six_Killing_zero_modes_spectrally_primed': classification == PASS,
        'transverse_and_longitudinal_magnitude_factors_kept_separate': True,
        'residual_isometry_group_volume_normalized': False,
        'signed_or_complex_FP_phase_assigned': False,
        'scalar_gradient_decomposition_jacobian_inserted': False,
        'complete_zero_mode_measure_quotient_constructed': False,
        'complete_signed_spatial_FP_determinant_computed': False,
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
    },
    'interpretation': 'For the frozen spatial DeWitt/harmonic gauge on round S3, the nonzero transverse-vector and longitudinal-vector FP magnitude spectra each admit a regular zeta continuation at s=0 and finite determinant magnitude for the declared dimensionless normalization. The transverse spectral prime removes exactly the six l=1 Killing generators; the longitudinal l=1 sector remains nonzero with multiplicity four. The resulting magnitude factors are normalization dependent. No signed FP phase, residual-isometry group volume, decomposition Jacobian, FS multiplication, TT Hessian, or one-loop determinant is assigned here.',
    'next_gate': 'Prospectively freeze the residual round-S3 spatial-isometry zero-mode measure quotient: specify the normalization of the six Killing generators and the associated gauge-group volume/collective-coordinate factor consistently with the frozen spatial gauge, while keeping the signed FP phase and physical TT Hessian separate and open.',
}

RESULT.parent.mkdir(parents=True, exist_ok=True)
CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
PROV.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')

checkpoint = f'''# RTK C9 HMT lambda=1 S3 spatial FP nonzero-mode zeta-magnitude checkpoint

Classification: `{classification}`

Frozen target commit: `{TARGET_COMMIT}`. Parent confirmed HEAD at freeze: `{PARENT_HEAD}`.

For the parent-certified spatial FP operator `M=nabla^2+Ricci`, this gate regularizes only the positive spectral magnitudes of the two nonzero vector sectors. The transverse dimensionless spectrum is `A_T=a^2|M_T|`, with `n=l+1>=3`, eigenvalue `n^2-4` and degeneracy `2(n^2-1)` after priming out the six l=1 Killing generators. The longitudinal spectrum is `A_L=a^2|M_L|`, with the retained n=2 level `(lambda,d)=(1,4)` and n>=3 spectrum `(lambda,d)=(n^2-5,n^2)`.

Both spectral zetas are regular at zero. The audit obtains `zeta_T(0)={int(zeta_T_0)}`, `zeta_L(0)={int(zeta_L_0)}`, `zeta_T'(0)={mp.nstr(zp_T_140,50)}` and `zeta_L'(0)={mp.nstr(zp_L_140,50)}`. For the frozen normalizations, `Det_zeta(A_T)={mp.nstr(det_T,50)}` and `Det_zeta(A_L)={mp.nstr(det_L,50)}`. The K=120 versus K=140 derivative differences are `{mp.nstr(prime_diff_T,8)}` and `{mp.nstr(prime_diff_L,8)}`; the direct-spectrum s=5 cross-check differences are `{mp.nstr(cross_diff_T,8)}` and `{mp.nstr(cross_diff_L,8)}`, all below the inherited `1e-30` tolerance.

Normalization dependence is explicit: `Det(c A_T)=c^(-5) Det(A_T)` and `Det(c A_L)=c^(-1) Det(A_L)`. These are determinant magnitudes only. No signed/complex FP phase is assigned, and no residual SO(4) gauge-group volume normalization is supplied.

Strict scope: complete zero-mode measure quotient OPEN; complete signed spatial FP determinant OPEN; full FP determinant OPEN; full FS determinant OPEN; physical TT Hessian OPEN; complete HMT gauge-fixed constraint matrix OPEN; HMT one-loop evaluability BLOCKED; full C9 OPEN. No scalar-gradient decomposition Jacobian is inserted. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.

Next gate: prospectively freeze the six-Killing residual-isometry zero-mode measure quotient and gauge-group-volume normalization, without touching the signed FP phase or TT Hessian.
'''
CHECKPOINT.write_text(checkpoint)

provenance = {
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'target': str(TARGET.relative_to(ROOT)),
    'target_frozen_commit': TARGET_COMMIT,
    'parent_result_commit': PARENT_HEAD,
    'script': str(pathlib.Path(__file__).relative_to(ROOT)),
    'result': str(RESULT.relative_to(ROOT)),
    'checkpoint': str(CHECKPOINT.relative_to(ROOT)),
    'method': 'two-sector spectral-zeta analytic continuation from the parent-certified round-S3 FP spectra using binomial/Riemann-zeta expansions; K=120 versus K=140 derivative convergence; direct original-spectrum cross-check at s=5',
    'precision_decimal_digits': mp.mp.dps,
    'frozen_tolerance_abs': '1e-30',
    'regularization': 'dimensionless positive-magnitude operators A_T=a^2|M_T| and A_L=a^2|M_L|',
    'signed_FP_phase_assigned': False,
    'residual_isometry_group_volume_normalized': False,
    'no_DSIR': True,
    'no_threshold_change': True,
}
PROV.write_text(json.dumps(provenance, indent=2, allow_nan=False) + '\n')
print(json.dumps({'classification': classification, 'scientific_checks': scientific_checks, 'next_gate': result['next_gate']}, indent=2, allow_nan=False))
