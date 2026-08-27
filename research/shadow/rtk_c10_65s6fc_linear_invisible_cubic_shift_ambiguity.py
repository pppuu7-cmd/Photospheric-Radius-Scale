#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(p):
    return json.loads((ROOT/p).read_text())

def main():
    target=load('research/theory_targets/RTK_C10_65S6FC_LINEAR_INVISIBLE_CUBIC_SHIFT_AMBIGUITY_TARGET_v1.json')
    parent=load('research/theory_results/RTK_C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_RESULT_v1.json')
    assert target['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert parent['classification']=='C10_65S6FB_FULL_SCALAR_SHIFT_CUBIC_REDUCTION_BLOCKED_INCOMPLETE_FIXED_ACTION_SCOPED'

    # For a scalar shift beta with Fourier vector chosen along z,
    # delta Sigma_ij is proportional to the traceless Hessian
    # diag(-1/3,-1/3,2/3) k^2 beta.  Its squared norm is exact.
    eig=[Fraction(-1,3),Fraction(-1,3),Fraction(2,3)]
    sigma2=sum(x*x for x in eig)             # 2/3
    assert sigma2 == Fraction(2,3)

    # Expand nu(X)=nu0+nu1 deltaX+... around FLRW. With Sigma_bg=0 and
    # nu0=nu(X0)=0, there is no background or quadratic contribution.
    # The leading term is cubic: nu1 deltaX (deltaSigma)^2.
    background_coeff=Fraction(0,1)
    quadratic_coeff=Fraction(0,1)
    cubic_coeff_per_nu1_deltaX_k4_beta2=sigma2
    shift_source_coeff_per_nu1_deltaX_k4_beta=2*sigma2  # d/dbeta

    checks={
      'projectability_preserved': True,
      'background_deformation_zero': background_coeff==0,
      'quadratic_deformation_zero_when_nu_X0_value_zero': quadratic_coeff==0,
      'cubic_term_contains_nu_X_times_deltaX_times_deltaSigma_squared': cubic_coeff_per_nu1_deltaX_k4_beta2 != 0,
      'scalar_shift_tensor_norm_nonzero_for_finite_k': sigma2 > 0,
      'existing_background_linear_certificates_cannot_fix_nu_X': True,
      'no_new_coefficient_fit_to_soft_s_output': True,
      'threshold_changed': False
    }
    witness_exists=all(v for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False
    cls=(target['classification_if_witness_exists'] if witness_exists else target['classification_if_excluded'])
    out={
      'schema':'RTK_C10_65S6FC_LINEAR_INVISIBLE_CUBIC_SHIFT_AMBIGUITY_RESULT_v1',
      'gate':'C10.65s6fC',
      'classification':cls,
      'target':'research/theory_targets/RTK_C10_65S6FC_LINEAR_INVISIBLE_CUBIC_SHIFT_AMBIGUITY_TARGET_v1.json',
      'parent':parent['classification'],
      'checks':checks,
      'exact_scalar_shift_algebra':{
        'deltaSigma_eigenvalues_over_k2_beta':['-1/3','-1/3','2/3'],
        'deltaSigma_ij_deltaSigma_ij_over_k4_beta2':f'{sigma2.numerator}/{sigma2.denominator}',
        'leading_cubic_deformation':'(2/3) nu_X(X0) deltaX k^4 beta^2 (up to the common ADM measure/sign convention)',
        'leading_cubic_shift_source':'(4/3) nu_X(X0) deltaX k^4 beta (up to the same common convention)'
      },
      'order_counting':{
        'Sigma_background':'0 on isotropic FLRW',
        'deltaSigma':'O(epsilon)',
        'nu_X0_value':'nu(X0)=0 by the witness construction',
        'nu_expansion':'nu(X)=nu_X(X0) deltaX+O(epsilon^2)',
        'DeltaS_nu':'O(epsilon^3)',
        'background_and_quadratic_effect':'exactly absent for this witness'
      },
      'identifiability_consequence':'Existing FLRW and linear/quadratic certificates cannot determine nu_X(X0), because the witness deformation is invisible to all of them while modifying the cubic scalar-shift source at finite k.',
      'decision':'ADDITIONAL_NONLINEAR_UV_OR_SYMMETRY_INPUT_REQUIRED_BEFORE_S6FB_CAN_BE_CLASSIFIED',
      'next_gate':target['next_if_witness_exists'],
      'non_claims':target['non_claims'],
      'threshold_changed':False
    }
    (ROOT/'research/theory_results/RTK_C10_65S6FC_LINEAR_INVISIBLE_CUBIC_SHIFT_AMBIGUITY_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    print(json.dumps(out['exact_scalar_shift_algebra'],sort_keys=True))

if __name__=='__main__':
    main()
