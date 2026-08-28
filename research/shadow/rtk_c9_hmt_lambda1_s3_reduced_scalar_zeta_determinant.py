#!/usr/bin/env python3
import json, pathlib, datetime
import mpmath as mp

ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET = ROOT/'research/theory_targets/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_ZETA_DETERMINANT_TARGET_v1.json'
RESULT = ROOT/'research/theory_results/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_ZETA_DETERMINANT_RESULT_v1.json'
CHECKPOINT = ROOT/'research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_ZETA_DETERMINANT_2026-08-28.md'
PROV = ROOT/'research/provenance/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_ZETA_DETERMINANT_PROVENANCE_v1.json'
TARGET_FROZEN_COMMIT = '06ed86480e19a6b16d91307534bf1fe2d5b9d20c'
PARENT_HEAD = 'ae2011561fee83c16c52d1f8d662f3d6e96e08d1'

T = json.loads(TARGET.read_text())
assert T['parent_head'] == PARENT_HEAD
assert T['frozen_spectrum']['domain'] == 'l=0 and l>=2; l=1 gauge modes excluded'
assert T['frozen_spectrum']['ell0_eigenvalue'] == 12
S = T['frozen_semantics']
for key in ['full_HMT_gauge_fixed_constraint_matrix_constructed','complete_zero_mode_quotient_constructed','full_FS_determinant_computed','full_HMT_one_loop_evaluable','full_C9_closed','soft_s_retest_allowed','production_k003_unblocked','threshold_changed','ordinary_projectable_parent_beta_functions_imported','unresolved_HMT_matter_coefficients_chosen']:
    assert S[key] is False, key
assert S['no_DSIR'] is True

# Work at substantially higher precision than the frozen minimum.
mp.mp.dps = 180

def zeta_cont(s, K):
    """Analytic continuation from binomial expansion after n=l+1.

    zeta_A(s)=4^-s [3^-s + sum_{k>=0} (s)_k/k! 4^k
      { zeta_R(2s+2k-2)-1-2^(2-2s-2k) }].
    Around s=0 this is regular term-by-term and the k-series converges geometrically.
    """
    s = mp.mpf(s)
    B = mp.power(3, -s)
    for k in range(K + 1):
        p = 2*s + 2*k - 2
        coeff = mp.rf(s, k) / mp.factorial(k) * mp.power(4, k)
        B += coeff * (mp.zeta(p) - 1 - mp.power(2, -p))
    return mp.power(4, -s) * B

# Exact value at s=0: 1 + [zeta_R(-2)-1-4] = -4; k>=1 vanish because (0)_k=0.
zeta0_exact = mp.mpf(-4)
assert zeta_cont(0, 40) == zeta0_exact

# Controlled derivative convergence: two independently truncated analytic-continuation series.
def zeta_prime_formula(K):
    tail_series = mp.mpf('0')
    for k in range(1, K + 1):
        bracket = mp.zeta(2*k - 2) - 1 - mp.power(2, 2 - 2*k)
        # d/ds (s)_k/k! at s=0 = 1/k.
        tail_series += mp.power(4, k) * bracket / k
    Bprime0 = (-mp.log(3) + 2*mp.diff(mp.zeta, -2) + 8*mp.log(2) + tail_series)
    # zeta_A=4^-s B, B(0)=-4, hence derivative contribution is +4 ln 4.
    return 4*mp.log(4) + Bprime0

zp120 = zeta_prime_formula(120)
zp140 = zeta_prime_formula(140)
zp_diff = abs(zp140 - zp120)
assert zp_diff < mp.mpf('1e-30'), zp_diff
zeta_prime0 = zp140

# Independent check in the ordinary convergence half-plane using the original positive spectrum.
# At s=5 the direct partial sum to N=20000 differs from the full sum by far below 1e-30;
# we compare it to the analytically continued representation without using derivative-at-zero algebra.
s_cross = mp.mpf(5)
N = 20000
direct = mp.power(12, -s_cross)
for n in range(3, N + 1):
    direct += n*n * mp.power(4*(n*n - 4), -s_cross)
continued = zeta_cont(s_cross, 100)
cross_diff = abs(continued - direct)
assert cross_diff < mp.mpf('1e-30'), cross_diff

# Frozen dimensionless zeta determinant of the positive FS factor.
det_hat = mp.exp(-zeta_prime0)
assert mp.isfinite(det_hat) and det_hat > 0

# Multiplicative normalization law. Since zeta_A(0)=-4, this determinant is not
# invariant under A_hat -> c A_hat. Verify with a concrete c=2 witness.
c = mp.mpf(2)
det_scaled_from_law = mp.power(c, zeta0_exact) * det_hat
assert abs(det_scaled_from_law / det_hat - mp.mpf(1)/16) < mp.mpf('1e-60')

classification = 'RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_ZETA_DETERMINANT_FINITE_NORMALIZATION_DEPENDENT_PASS_SCOPED'
result = {
  'classification': classification,
  'frozen_target_parent_head': PARENT_HEAD,
  'target_frozen_commit': TARGET_FROZEN_COMMIT,
  'spectral_problem': {
    'operator': 'A_hat=a^4|C12|',
    'eigenvalues': 'lambda_l=|4(l-1)(l+3)|',
    'degeneracy': 'd_l=(l+1)^2',
    'domain': 'l=0 and l>=2; l=1 gauge modes excluded',
    'zeta_definition': 'zeta_A(s)=sum d_l lambda_l^(-s)',
    'n_form': "4^(-s)[3^(-s)+sum_{n=3}^infinity n^2(n^2-4)^(-s)]"
  },
  'analytic_continuation': {
    'regular_at_s0': True,
    'zeta_A_0_exact': -4,
    'zeta_A_prime_0': mp.nstr(zeta_prime0, 80),
    'prime_K120_vs_K140_abs_diff': mp.nstr(zp_diff, 20),
    'crosscheck_s': 5,
    'crosscheck_direct_N': N,
    'crosscheck_abs_diff': mp.nstr(cross_diff, 20)
  },
  'zeta_determinant': {
    'dimensionless_Det_zeta_A_hat': mp.nstr(det_hat, 80),
    'definition': 'exp[-zeta_A_prime(0)]',
    'positive_FS_factor_used': True,
    'signed_C12_phase_assigned': False,
    'normalization_rescaling_law': 'Det_zeta(c A_hat)=c^(zeta_A(0)) Det_zeta(A_hat)=c^(-4) Det_zeta(A_hat)',
    'c2_ratio': mp.nstr(det_scaled_from_law/det_hat, 30),
    'normalization_independent': False
  },
  'findings': {
    'reduced_scalar_zeta_regular_at_zero': True,
    'regularized_scalar_FS_determinant_computed_for_frozen_normalization': True,
    'finite_positive_dimensionless_determinant': True,
    'normalization_dependence_nonzero': True,
    'full_HMT_gauge_fixed_constraint_matrix_constructed': False,
    'complete_zero_mode_quotient_constructed': False,
    'full_FS_determinant_computed': False,
    'full_HMT_one_loop_evaluable': False,
    'full_C9_closed': False,
    'ordinary_projectable_parent_beta_functions_imported': False,
    'unresolved_HMT_matter_coefficients_chosen': False,
    'soft_s_retest_allowed': False,
    'production_k003_unblocked': False,
    'threshold_changed': False,
    'no_DSIR': True
  },
  'interpretation': 'The already-reduced round-S3 lambda=1 scalar/conformal Faddeev-Senjanovic factor has a well-defined finite zeta determinant after freezing the dimensionless normalization A_hat=a^4|C12|. The spectral zeta is regular at zero with zeta_A(0)=-4. Therefore the numerical determinant is normalization dependent: multiplying the normalized operator by c changes the determinant by c^-4. This is a scoped regularization result only and is not the complete HMT FS determinant, one-loop effective action, or C9 closure.',
  'next_gate': 'Freeze the remaining non-scalar HMT gauge/constraint sectors on the same round-S3 lambda=1 background and construct the complete gauge-fixed constraint-matrix block inventory before attempting any product of sector determinants; retain the scalar normalization dependence as an explicit counterterm/measure-normalization datum.'
}

RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(result, indent=2) + '\n')
CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
CHECKPOINT.write_text(f'''# RTK C9 HMT lambda=1 S3 reduced scalar zeta determinant checkpoint\n\nClassification: `{classification}`\n\nFrozen target commit: `{TARGET_FROZEN_COMMIT}`. Parent confirmed HEAD: `{PARENT_HEAD}`.\n\nFor the previously reduced scalar/conformal FS block define the positive dimensionless operator `A_hat=a^4|C12|`, with eigenvalues `lambda_l=|4(l-1)(l+3)|`, degeneracy `(l+1)^2`, and domain `l=0,l>=2` after removing the proven four-dimensional l=1 spatial-diffeomorphism gauge sector.\n\nThe spectral zeta `zeta_A(s)=sum d_l lambda_l^(-s)` has an explicit analytic continuation regular at s=0. The audit obtains exactly `zeta_A(0)=-4` and numerically `zeta_A'(0)={mp.nstr(zeta_prime0,50)}`. Thus for the frozen normalization, `Det_zeta(A_hat)=exp[-zeta_A'(0)]={mp.nstr(det_hat,50)}`.\n\nThis finite number is NOT normalization invariant: `Det_zeta(c A_hat)=c^(-4) Det_zeta(A_hat)`. The gate therefore closes only the regularizability of this already-reduced scalar FS factor for a declared normalization. No signed C12 phase is assigned; the FS square-root uses `|mu_l|`.\n\nStrict status: complete HMT gauge-fixed constraint matrix OPEN; complete zero-mode quotient OPEN; full FS determinant OPEN; HMT one-loop evaluability BLOCKED; full C9 OPEN. No parent beta functions imported, no unresolved HMT matter coefficients chosen, thresholds unchanged, soft-s forbidden, k=0.03 production blocked, no DSIR.\n\nNext gate: construct a frozen block inventory for the remaining HMT gauge/constraint sectors on the same background before combining determinant factors.\n''')
PROV.parent.mkdir(parents=True, exist_ok=True)
PROV.write_text(json.dumps({
  'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'target': str(TARGET.relative_to(ROOT)),
  'script': str(pathlib.Path(__file__).relative_to(ROOT)),
  'result': str(RESULT.relative_to(ROOT)),
  'checkpoint': str(CHECKPOINT.relative_to(ROOT)),
  'method': 'spectral-zeta analytic continuation using a convergent binomial/Riemann-zeta expansion; direct original-spectrum cross-check at s=5; high-precision K=120 versus K=140 derivative convergence check',
  'precision_decimal_digits': mp.mp.dps,
  'regularization': 'dimensionless zeta determinant of positive FS factor A_hat=a^4|C12|',
  'normalization_dependence_retained': True,
  'no_DSIR': True,
  'no_threshold_change': True
}, indent=2) + '\n')
print(json.dumps(result, indent=2))
