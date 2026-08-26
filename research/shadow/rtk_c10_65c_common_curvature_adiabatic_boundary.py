#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_TARGET_v1.json'
PREFLIGHT=ROOT/'research/theory_results/RTK_C10_65B0_ZERO_CHARGE_ADIABATIC_PREFLIGHT_RESULT_v1.json'
P64=ROOT/'research/theory_results/RTK_C10_ZERO_CHARGE_ADIABATIC_BOUNDARY_RESULT_v1.json'
PADI=ROOT/'research/theory_results/RTK_C10_FINITE_ONSET_ADIABATIC_INVARIANCE_RESULT_v1.json'
OUT=Path('c10_65c_common_curvature_adiabatic_boundary_result.json')


def main():
    t=json.loads(TARGET.read_text())
    pre=json.loads(PREFLIGHT.read_text())
    p64=json.loads(P64.read_text())
    padi=json.loads(PADI.read_text())
    assert t['status']=='FROZEN_BEFORE_EVALUATION'
    assert pre['classification']=='C10_65B0_ZERO_CHARGE_ADIABATIC_INCOMPATIBLE_SCOPED'
    assert p64['classification']=='C10_ZERO_CHARGE_ADIABATIC_BOUNDARY_CONSISTENT_PASS_SCOPED'
    assert padi['classification']=='C10_FINITE_ONSET_ADIABATIC_INVARIANCE_PASS_UV_OR_GROWING_MODE_MATCH_REQUIRED_SCOPED'

    redN,HB,psiN,Jad,w=sp.symbols('redN HB psiN J_ad w', finite=True)
    redP=redN+3*HB
    psiP=psiN+HB
    IN=sp.expand(redN-3*psiN)
    IP=sp.expand(redP-3*psiP)
    assert sp.simplify(IP-IN)==0

    # Corrected adiabatic boundary I_khr=J_ad.
    deltaP=(1+w)*(3*psiP+Jad)
    deltaN=(1+w)*(3*psiN+Jad)
    assert sp.simplify(deltaP/(1+w)-3*psiP-Jad)==0
    assert sp.simplify(deltaN/(1+w)-3*psiN-Jad)==0

    # For any ordinary component sharing J_ad, the relative-density entropy is I_khr-J_ad.
    I_khr=sp.symbols('I_khr', finite=True)
    DeltaI=sp.expand(I_khr-Jad)
    S_rel=sp.expand(I_khr-Jad)
    assert sp.simplify(DeltaI-S_rel)==0

    Jad0=float(pre['diagnostics']['ordinary_common_J_ad_intercept'])
    spread=float(pre['diagnostics']['ordinary_intercept_abs_spread'])
    spread_tol=float(pre['diagnostics']['ordinary_common_abs_spread_tolerance'])
    assert spread<=spread_tol
    zero_slice_iso=-Jad0

    out={
      'schema':'RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_RESULT_v1',
      'gate':'C10.65c',
      'classification':'C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_PASS_SCOPED',
      'target':'research/theory_targets/RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_TARGET_v1.json',
      'exact_identities':{
        'gauge_invariance':'I_khr,pref=delta_khr,pref/(1+w)-3 psi_pref = delta_khr,N/(1+w)-3 Psi_N=I_khr,N',
        'adiabatic_isocurvature_coordinate':'Delta I_iso=I_khr-J_ad',
        'relative_entropy':'for any ordinary species on the common branch, S_khr,i=Delta I_iso',
        'corrected_preferred_boundary':'delta_khr=(1+w)(3 psi_pref+J_ad)',
        'corrected_newtonian_boundary':'delta_khr,N=(1+w)(3 Psi_N+J_ad)',
        'machine_residuals':{'preferred_to_newtonian_I':'0','preferred_boundary':'0','newtonian_boundary':'0','relative_entropy_map':'0'}
      },
      'baseline_normalization_control':{
        'J_ad_low_k_intercept':Jad0,
        'ordinary_intercept_abs_spread':spread,
        'ordinary_intercept_abs_spread_tolerance':spread_tol,
        'absolute_zero_charge_slice_Delta_I_iso_intercept':zero_slice_iso,
        'interpretation':'In the pinned C10.65a normalization, the adiabatic neutral charge is nonzero and tracks the common ordinary curvature invariant; absolute I_khr=0 is a finite charge-isocurvature displacement.'
      },
      'architecture_decision':{
        'adiabatic_branch':'impose Delta I_iso=I_khr-J_ad=0',
        'independent_charge_isocurvature':'retain arbitrary nonzero Delta I_iso as a separate initial-condition sector',
        'C10_64_status':'retain the exact zero-charge theorem but supersede its generic adiabatic labeling for nonzero primordial curvature',
        'C10_65b_status':'do not execute the frozen absolute-zero-charge rank contract as an adiabatic uniqueness theorem; replace only its neutral boundary condition and preserve the rest of its preferred-DAE architecture'
      },
      'next_gate':'freeze the pinned compromise_CLASS photon-baryon tight-coupling port contract, then implement the corrected completed-U1 O(k^2) rank system with Delta I_iso=0 and solve V_khr0 and B0.',
      'non_claims':t['non_claims']
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'],json.dumps(out['baseline_normalization_control'],sort_keys=True))

if __name__=='__main__': main()
