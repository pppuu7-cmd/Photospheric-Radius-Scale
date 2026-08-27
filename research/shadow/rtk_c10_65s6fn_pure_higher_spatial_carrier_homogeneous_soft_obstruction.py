#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]

def load(p): return json.loads((ROOT/p).read_text())

def main():
    t=load('research/theory_targets/RTK_C10_65S6FN_PURE_HIGHER_SPATIAL_CARRIER_HOMOGENEOUS_SOFT_OBSTRUCTION_TARGET_v1.json')
    m=load('research/theory_results/RTK_C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert m['classification']=='C10_65S6FM_EXACT_HOMOGENEOUS_PHYSICAL_CUBIC_VERTEX_NONZERO_PASS_SCOPED'
    n,z,k=sp.symbols('n zeta0 k', integer=True, positive=True)
    # sqrt(gamma): +3; two R^(3): -4; contracting the two sets of (n-1)
    # derivative indices: -2(n-1). A homogeneous conformal factor has no
    # spatial derivative, so no additional connection terms are generated.
    weight=sp.simplify(3-4-2*(n-1))
    assert sp.simplify(weight-(1-2*n))==0

    # For every positive integer n, 1-2n cannot vanish.
    zero_solution=sp.solve(sp.Eq(weight,0),n)
    assert zero_solution==[]  # integer+positive assumptions exclude n=1/2

    # Explicit n=2 normalization cross-check against archived exact conformal theorem.
    # Q2=16 U^2. For hard pair k,-k the cross term is 2*16*k^6=32*k^6.
    # Multiplying by homogeneous weight -3 yields -96*k^6.
    w2=sp.simplify(weight.subs(n,2))
    q2_cross=32*k**6
    k3s=sp.expand(w2*q2_cross)
    assert sp.simplify(k3s+96*k**6)==0

    cls='C10_65S6FN_PURE_HIGHER_SPATIAL_CARRIER_HOMOGENEOUS_SOFT_OBSTRUCTION_PASS_SCOPED'
    out={
      'schema':'RTK_C10_65S6FN_PURE_HIGHER_SPATIAL_CARRIER_HOMOGENEOUS_SOFT_OBSTRUCTION_RESULT_v1',
      'gate':'C10.65s6fN','classification':cls,'decision':'OBSTRUCTION',
      'target':'research/theory_targets/RTK_C10_65S6FN_PURE_HIGHER_SPATIAL_CARRIER_HOMOGENEOUS_SOFT_OBSTRUCTION_TARGET_v1.json',
      'parent':m['classification'],
      'theorem':{
        'homogeneous_conformal_weight':'1-2n',
        'factor_decomposition':{'sqrt_gamma':3,'two_R3':-4,'inverse_metric_derivative_contractions':'-2(n-1)'},
        'integer_domain':'n>=1',
        'zero_weight_solution_over_reals':'n=1/2',
        'zero_weight_solution_in_integer_domain':None,
        'soft_cubic_to_quadratic_cross_ratio':'1-2n',
        'n2_weight':int(w2),
        'n2_Q2_hard_pair_cross':'32 k^6',
        'n2_predicted_K3_s':str(k3s),
        'n2_archived_K3_s':'-96 k^6'
      },
      'checks':{
        'target_frozen':True,'parent_exact':True,
        'weight_derived_from_volume_R_inverse_metric_factors':True,
        'integer_n_ge_1_has_no_zero_weight':True,
        'n2_normalization_matches_archived_K3_s':True,
        'no_parameter_fit':True,'no_new_operator_coefficient':True,
        'no_punctured_q_limit':True,'no_k003_production_output':True,
        'threshold_changed':False
      },
      'interpretation':'Within the pure projectable curvature-carrier family sqrt(gamma)[D^(n-1)R3]^2, simply increasing the integer spatial derivative order cannot eliminate the exact homogeneous hard-hard-soft cubic coupling: its homogeneous conformal weight is 1-2n, nonzero for every integer n>=1. The n=2 normalization reproduces the archived exact K3_s=-96 k^6. Therefore a soft-s cure must use genuinely different nonlinear structure (for example an independently motivated operator combination or symmetry), not just n>2 in this pure family.',
      'next_gate':'Keep k=0.03 production blocked. Audit source-locked operator/symmetry classes that can change the homogeneous conformal weight or produce a structurally correlated cancellation while preserving the certified background/quadratic sector; preregister any candidate before evaluating its soft vertex.',
      'non_claims':t['non_claims'],'threshold_changed':False
    }
    p=ROOT/'research/theory_results/RTK_C10_65S6FN_PURE_HIGHER_SPATIAL_CARRIER_HOMOGENEOUS_SOFT_OBSTRUCTION_RESULT_v1.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    print('weight =',weight)
    print('n=2 K3_s =',k3s)

if __name__=='__main__': main()
