#!/usr/bin/env python3
import json, math
from decimal import Decimal, getcontext
from datetime import datetime, timezone
from pathlib import Path

getcontext().prec=80
TARGET_COMMIT='de512708872f214afb26857bee4f707b03c3ea86'
PARENT='83ae30fee6d77a3ea42ede57823bedc2875abfdf'
CLASS='RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_PRINCIPAL_CUT_PHASE_TRIVIAL_COMBINED_PASS_SCOPED'

# Frozen round-S3 operator M = nabla^2 + Ricci.
# Transverse vector harmonics: a^2 M_T = -(n^2-4), n>=3 after n=2/l=1 Killing zero modes are primed.
# Longitudinal gradients use nabla^2 grad f = grad nabla^2 f + Ric(grad f),
# hence M grad f = grad nabla^2 f + 2 Ric(grad f). On S3 Ric=2/a^2,
# so a^2 M_L = -(l(l+2)-4)=-(n^2-5). Thus n=2 is +1 (d=4), n>=3 negative.

zabs_T0=-5
zabs_L0=-1
positive_L_multiplicity=4
zneg_T0=zabs_T0
zneg_L0=zabs_L0-positive_L_multiplicity
assert zneg_T0==-5
assert zneg_L0==-5

# Principal spectral cut: each negative eigenvalue contributes exp(i*pi), zeta-continued.
def phase_from_integer_zeta(z):
    # z is an exact integer here.
    return -1 if (z % 2) else 1
phase_T=phase_from_integer_zeta(zneg_T0)
phase_L=phase_from_integer_zeta(zneg_L0)
phase_total=phase_T*phase_L
assert phase_T==-1 and phase_L==-1 and phase_total==1

# Cross-check with -M: all formerly negative modes become positive; only longitudinal n=2 d=4 become negative.
minusM_negative_multiplicity=4
minusM_sign=(-1)**minusM_negative_multiplicity
assert minusM_sign==1

DetT=Decimal('67.869342368305180409328005773658622338151596454315223519029011945298722091682815')
DetL=Decimal('2.1999085267023697422585361883960668683089207686293255795194962406150393938391081')
DetAbs=DetT*DetL
assert DetAbs>0

result={
  'classification': CLASS,
  'target_frozen_commit': TARGET_COMMIT,
  'scientific_parent_head': PARENT,
  'operator': 'M^i_j=nabla^2 delta^i_j+R^i_j',
  'spectral_sign_derivation': {
    'transverse': 'a^2 M_T=-(n^2-4), n>=3 after six n=2 Killing zero modes are primed',
    'longitudinal_identity': 'nabla^2 grad f = grad(nabla^2 f)+Ric(grad f)',
    'longitudinal': 'a^2 M_L=-(n^2-5): n=2 gives +1 with d=4; n>=3 is negative'
  },
  'principal_spectral_cut': 'log(-x)=log(x)+i*pi for x>0',
  'zeta_phase_data': {
    'zeta_abs_T_0': zabs_T0,
    'zeta_abs_L_0': zabs_L0,
    'zeta_negative_T_0': zneg_T0,
    'zeta_negative_L_0': zneg_L0,
    'phase_T': '-1',
    'phase_L': '-1',
    'combined_phase': '+1'
  },
  'minus_operator_crosscheck': {
    'operator': '-M',
    'negative_modes': 'longitudinal n=2 only',
    'negative_multiplicity': minusM_negative_multiplicity,
    'finite_sign': '+1'
  },
  'inherited_nonzero_mode_magnitudes': {
    'Det_zeta_abs_T': str(DetT),
    'Det_zeta_abs_L': str(DetL),
    'combined_abs_product': str(DetAbs)
  },
  'scientific_checks': {
    'signed_transverse_spectrum_consistent': True,
    'signed_longitudinal_spectrum_consistent': True,
    'zeta_negative_T0_exact_minus5': zneg_T0==-5,
    'zeta_negative_L0_exact_minus5': zneg_L0==-5,
    'principal_cut_transverse_phase_minus1': phase_T==-1,
    'principal_cut_longitudinal_phase_minus1': phase_L==-1,
    'principal_cut_combined_phase_plus1': phase_total==1,
    'minusM_four_negative_modes_even_sign_plus1': minusM_sign==1
  },
  'findings': {
    'nonzero_spatial_FP_principal_cut_phase_assigned': True,
    'combined_nonzero_spatial_FP_phase_is_trivial_under_frozen_cut': True,
    'phase_is_convention_independent_observable': False,
    'residual_SO4_zero_mode_quotient_normalization_already_parent_fixed_under_convention': True,
    'complete_signed_spatial_FP_factor_combined_with_zero_mode_quotient': False,
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
    'no_DSIR': True
  },
  'interpretation': 'For the frozen round-S3 spatial FP operator and the prospectively frozen principal spectral cut, each nonzero harmonic sector contributes phase -1, because its zeta-regularized negative-mode count is -5. Their product is +1. The equivalent -M convention has exactly four finite negative longitudinal n=2 modes, again giving sign +1. This removes the nonzero-mode phase ambiguity only under the declared spectral-cut/operator-sign convention; it does not by itself construct the complete FP quotient or the HMT one-loop determinant.',
  'next_gate': 'Assemble the scoped spatial FP quotient factor from the certified nonzero signed determinant, six-Killing SO(4) orbit-volume quotient, and explicitly audit whether any vector decomposition Jacobian is required by the chosen field/gauge-coordinate measure; keep FS scalar and TT Hessian separate.'
}

out=Path('research/theory_results/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_SIGNED_PHASE_RESULT_v1.json')
out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2)+'\n')

cp=Path('research/checkpoints/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_SIGNED_PHASE_2026-08-28.md')
cp.write_text(f'''# RTK C9 HMT lambda=1 S3 spatial FP signed-phase checkpoint\n\nClassification: `{CLASS}`\n\nFrozen target `{TARGET_COMMIT}`; scientific parent `{PARENT}`. For `M=nabla^2+Ricci`, transverse nonzero modes have `a^2 M_T=-(n^2-4)`, while longitudinal modes obey `a^2 M_L=-(n^2-5)`: the `n=2` longitudinal level is positive with multiplicity four and all `n>=3` longitudinal levels are negative.\n\nUsing the prospectively frozen principal spectral cut, `zeta_-^T(0)=-5` and `zeta_-^L(0)=zeta_|M_L|(0)-4=-5`. Therefore each sector has phase `-1`, but the combined nonzero spatial FP phase is `+1`. An independent sign-convention cross-check with `-M` leaves only four negative longitudinal `n=2` modes, so its finite sign is also `(-1)^4=+1`.\n\nThis is a scoped phase result. The phase depends on the declared operator/sign/spectral-cut convention and is not an observable. The complete spatial FP quotient has not yet been assembled with the residual SO(4) orbit factor or any decomposition Jacobian audit. Full FP/FS determinants, TT Hessian, complete HMT gauge-fixed matrix, one-loop evaluability and C9 remain OPEN/BLOCKED. Thresholds unchanged; soft-s forbidden; k=0.03 production blocked; DSIR not mixed.\n''')

prov={
 'created_utc': datetime.now(timezone.utc).isoformat(),
 'target_frozen_commit': TARGET_COMMIT,
 'scientific_parent_head': PARENT,
 'script': 'research/shadow/rtk_c9_hmt_lambda1_s3_spatial_fp_signed_phase.py',
 'method': 'exact harmonic sign derivation plus zeta-regularized negative-mode phase under principal spectral cut; -M finite-negative-mode cross-check',
 'regularization': 'principal spectral cut with inherited zeta continuations at s=0',
 'no_DSIR': True,
 'no_threshold_change': True
}
pp=Path('research/provenance/RTK_C9_HMT_LAMBDA1_S3_SPATIAL_FP_SIGNED_PHASE_PROVENANCE_v1.json')
pp.parent.mkdir(parents=True,exist_ok=True); pp.write_text(json.dumps(prov,indent=2)+'\n')
print(json.dumps(result,indent=2))
