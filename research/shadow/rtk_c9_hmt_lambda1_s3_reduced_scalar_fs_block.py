#!/usr/bin/env python3
import json, pathlib, datetime, math

ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET = ROOT/'research/theory_targets/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_FS_BLOCK_TARGET_v1.json'
RESULT = ROOT/'research/theory_results/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_FS_BLOCK_RESULT_v1.json'
CHECKPOINT = ROOT/'research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_FS_BLOCK_2026-08-28.md'
PROV = ROOT/'research/provenance/RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_FS_BLOCK_PROVENANCE_v1.json'

TARGET_FROZEN_COMMIT = 'a2b81b7808cf4928bef5ae9e000d6c2b18a94adc'
PARENT_HEAD = '9ccb2322a0aa9320886b25309cd2468975297e75'

t = json.loads(TARGET.read_text())
assert t['parent_head'] == PARENT_HEAD
assert t['frozen_background']['dimension'] == 3
assert t['frozen_background']['lambda'] == 1
assert t['frozen_inputs']['reduced_scalar_domain'] == 'ell=0 and ell>=2'
s = t['frozen_semantics']
for key in [
    'regularized_scalar_FS_determinant_computed',
    'full_HMT_gauge_fixed_constraint_matrix_constructed',
    'complete_zero_mode_quotient_constructed',
    'full_FS_determinant_computed',
    'full_HMT_one_loop_evaluable',
    'full_C9_closed',
    'soft_s_retest_allowed',
    'production_k003_unblocked',
    'threshold_changed',
    'ordinary_projectable_parent_beta_functions_imported',
    'unresolved_HMT_matter_coefficients_chosen',
]:
    assert s[key] is False, key
assert s['no_DSIR'] is True

# Dimensionless eigenvalue a^4 * mu_l for
# C12=(R/3)(-R-2 nabla^2), R=6/a^2,
# -nabla^2 Y_l=l(l+2)/a^2 Y_l.
def mu_a4(ell: int) -> int:
    return 4 * (ell * (ell + 2) - 3)

def mu_factorized_a4(ell: int) -> int:
    return 4 * (ell - 1) * (ell + 3)

def degeneracy(ell: int) -> int:
    return (ell + 1) ** 2

# Exact algebraic identity, sampled as a guard against implementation errors.
for ell in range(0, 128):
    assert mu_a4(ell) == mu_factorized_a4(ell)

assert mu_a4(0) == -12
assert mu_a4(1) == 0
assert degeneracy(1) == 4
for ell in range(2, 128):
    assert mu_a4(ell) > 0

# Analytic integer-domain proof encoded by factor signs:
# ell=0 -> (ell-1)(ell+3)<0 but nonzero;
# ell>=2 -> both factors >0; only nonnegative integer root is ell=1.
nonnegative_integer_roots = [ell for ell in range(0, 128) if mu_factorized_a4(ell) == 0]
assert nonnegative_integer_roots == [1]

# Reduced domain excludes precisely the already-classified ell=1 gauge sector.
reduced_sample = [0] + list(range(2, 128))
assert all(mu_a4(ell) != 0 for ell in reduced_sample)

# A second-class pair gives antisymmetric 2x2 mode matrix [[0,mu],[-mu,0]],
# whose determinant is mu^2. We use dimensionless a^4 mu_l, so det scales as a^-8.
mode_checks = []
for ell in [0, 2, 3, 4, 5, 10, 32, 127]:
    mu = mu_a4(ell)
    det_a8 = mu * mu
    assert det_a8 > 0
    mode_checks.append({
        'ell': ell,
        'degeneracy': degeneracy(ell),
        'mu_times_a4': mu,
        'FS_2x2_det_times_a8': det_a8,
    })

# A finite cutoff product/log can be used only as a diagnostic, never as a
# regularized functional determinant. Keep the diagnostic dimensionless.
L = 32
log_abs_cutoff_product = 0.0
for ell in [0] + list(range(2, L + 1)):
    log_abs_cutoff_product += degeneracy(ell) * math.log(abs(mu_a4(ell)))
assert math.isfinite(log_abs_cutoff_product)

classification = 'RTK_C9_HMT_LAMBDA1_S3_REDUCED_SCALAR_FS_BLOCK_NONDEGENERATE_PASS_SCOPED'
result = {
    'classification': classification,
    'frozen_target_parent_head': PARENT_HEAD,
    'target_frozen_commit': TARGET_FROZEN_COMMIT,
    'exact_spectrum': {
        'operator': 'C12=(R/3)(-R-2 nabla^2), R=6/a^2',
        'scalar_laplacian': '-nabla^2 Y_l=l(l+2)/a^2 Y_l',
        'mu_l_times_a4': '4[l(l+2)-3]=4(l-1)(l+3)',
        'degeneracy': 'd_l=(l+1)^2',
        'ell0_mu_times_a4': -12,
        'ell1_mu_times_a4': 0,
        'ell1_degeneracy': 4,
        'ell_ge2_sign': 'positive',
        'reduced_domain': 'ell=0 and ell>=2'
    },
    'mode_checks': mode_checks,
    'diagnostic_only': {
        'cutoff_L': L,
        'log_abs_product_of_dimensionless_mu_with_degeneracy': log_abs_cutoff_product,
        'is_regularized_determinant': False
    },
    'findings': {
        'ell1_four_dimensional_gauge_sector_projected_out': True,
        'reduced_scalar_C12_has_remaining_zero_modes': False,
        'ell0_eigenvalue_negative_but_nonzero': True,
        'ell_ge2_eigenvalues_positive': True,
        'reduced_scalar_C12_block_nondegenerate': True,
        'FS_2x2_mode_determinant_is_mu_squared': True,
        'FS_2x2_mode_determinant_positive_on_reduced_domain': True,
        'regularized_scalar_FS_determinant_computed': False,
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
    'interpretation': 'After explicitly quotienting the four ell=1 scalar/conformal modes already proven to be spatial-diffeomorphism gauge directions on round S3, the frozen lambda=1 scalar C12 spectrum has no remaining zero eigenvalues: ell=0 is negative but nonzero and every ell>=2 eigenvalue is positive. Hence each reduced 2x2 antisymmetric Faddeev-Senjanovic mode block is nondegenerate. This is only a scoped block-rank result; no regularized infinite product, complete HMT zero-mode quotient, full constraint determinant, one-loop evaluability, or C9 closure is claimed.',
    'next_gate': 'Freeze an explicit spectral regularization/normalization prescription for this reduced scalar block (preferably a dimensionless zeta or heat-kernel definition) and determine whether a finite reduced scalar determinant can be defined without conflating it with the still-open complete HMT gauge-fixed Faddeev-Senjanovic determinant.'
}

RESULT.parent.mkdir(parents=True, exist_ok=True)
RESULT.write_text(json.dumps(result, indent=2) + '\n')
CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)
CHECKPOINT.write_text(f'''# RTK C9 HMT lambda=1 S3 reduced scalar FS-block checkpoint

Classification: `{classification}`

Frozen target commit: `{TARGET_FROZEN_COMMIT}`.
Parent confirmed HEAD: `{PARENT_HEAD}`.

On round S3 at lambda=1,

`C12=(R/3)(-R-2 nabla^2)`, `R=6/a^2`,

so for scalar harmonics

`mu_l a^4 = 4[l(l+2)-3] = 4(l-1)(l+3)` with `d_l=(l+1)^2`.

The only nonnegative-integer zero is ell=1, with degeneracy four. The parent gate already proved these four conformal zero modes are spatial-diffeomorphism gauge directions. After quotienting exactly that sector, the reduced scalar domain is ell=0 and ell>=2. Here `mu_0 a^4=-12` is negative but nonzero, while `mu_l>0` for every ell>=2. Therefore the reduced scalar C12 block has no zero eigenvalues.

For the antisymmetric 2x2 second-class mode matrix `[[0,mu_l],[-mu_l,0]]`, `det=mu_l^2>0` on every reduced mode. This proves scoped nondegeneracy only.

Strict scope: no zeta/heat-kernel regularization was frozen, so no finite scalar functional determinant is claimed. The complete HMT gauge-fixed constraint matrix, complete zero-mode quotient, full FS determinant, HMT one-loop evaluability and full C9 remain OPEN/BLOCKED. Parent beta functions were not imported; unresolved HMT matter coefficients were not chosen; thresholds unchanged; soft-s retest forbidden; k=0.03 production blocked; no DSIR content used.

Next gate: preregister a dimensionless spectral regularization/normalization prescription for this reduced scalar block and test whether its finite reduced determinant is well defined, while explicitly keeping the complete HMT determinant and C9 open.
''')
PROV.parent.mkdir(parents=True, exist_ok=True)
PROV.write_text(json.dumps({
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'target': str(TARGET.relative_to(ROOT)),
    'script': str(pathlib.Path(__file__).relative_to(ROOT)),
    'result': str(RESULT.relative_to(ROOT)),
    'checkpoint': str(CHECKPOINT.relative_to(ROOT)),
    'method': 'exact round-S3 scalar-harmonic spectral factorization, explicit ell=1 gauge quotient inherited from the immediately preceding scoped gate, and 2x2 antisymmetric second-class determinant identity',
    'regularization': 'none; finite-cutoff log product is diagnostic only and is explicitly not interpreted as a functional determinant',
    'no_DSIR': True,
    'no_threshold_change': True
}, indent=2) + '\n')
print(json.dumps(result, indent=2))
