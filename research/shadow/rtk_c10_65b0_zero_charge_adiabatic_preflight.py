#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TARGET=ROOT/'research/theory_targets/RTK_C10_65B0_ZERO_CHARGE_ADIABATIC_PREFLIGHT_TARGET_v1.json'
P64=ROOT/'research/theory_results/RTK_C10_ZERO_CHARGE_ADIABATIC_BOUNDARY_RESULT_v1.json'
PADI=ROOT/'research/theory_results/RTK_C10_FINITE_ONSET_ADIABATIC_INVARIANCE_RESULT_v1.json'
P65A=ROOT/'research/theory_results/RTK_C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_RESULT_v1.json'
OUT=Path('c10_65b0_zero_charge_adiabatic_preflight_result.json')


def affine_fit(xs,ys):
    n=len(xs)
    xm=sum(xs)/n; ym=sum(ys)/n
    den=sum((x-xm)**2 for x in xs)
    if den<=0: raise RuntimeError('degenerate x grid')
    slope=sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/den
    intercept=ym-slope*xm
    residual=max(abs(y-(intercept+slope*x)) for x,y in zip(xs,ys))
    return intercept,slope,residual


def main():
    t=json.loads(TARGET.read_text())
    p64=json.loads(P64.read_text())
    padi=json.loads(PADI.read_text())
    p65=json.loads(P65A.read_text())
    assert t['status']=='FROZEN_BEFORE_EVALUATION'
    assert p64['classification']=='C10_ZERO_CHARGE_ADIABATIC_BOUNDARY_CONSISTENT_PASS_SCOPED'
    assert padi['classification']=='C10_FINITE_ONSET_ADIABATIC_INVARIANCE_PASS_UV_OR_GROWING_MODE_MATCH_REQUIRED_SCOPED'
    assert p65['classification']=='C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_CONSISTENT_PASS_SCOPED'
    assert p65['low_k_control']['pass'] is True

    m=int(t['evaluation']['low_k_modes'])
    recs=sorted(p65['records'],key=lambda r:float(r['k_Mpc_inv']))[:m]
    if len(recs)!=m: raise RuntimeError('insufficient low-k records')
    xs=[float(r['k_Mpc_inv'])**2 for r in recs]
    Js={'b':[],'g':[],'ur':[]}
    rows=[]
    for r in recs:
        phi=float(r['CLASS_phi_curvature'])
        jb=float(r['delta_b'])-3.0*phi
        jg=0.75*float(r['delta_g'])-3.0*phi
        jur=0.75*float(r['delta_ur'])-3.0*phi
        vals=[jb,jg,jur,phi]
        if not all(math.isfinite(v) for v in vals): raise RuntimeError('nonfinite parent data')
        Js['b'].append(jb); Js['g'].append(jg); Js['ur'].append(jur)
        rows.append({'k_Mpc_inv':float(r['k_Mpc_inv']),'J_b':jb,'J_g':jg,'J_ur':jur,
                     'S_zerocharge_minus_b':-jb,'S_zerocharge_minus_g':-jg,'S_zerocharge_minus_ur':-jur})

    fits={}
    for key in ('b','g','ur'):
        inter,slope,res=affine_fit(xs,Js[key])
        fits[key]={'intercept':inter,'slope_per_k2':slope,'max_abs_fit_residual':res}
    ints=[fits[k]['intercept'] for k in ('b','g','ur')]
    jad=sum(ints)/3.0
    spread=max(abs(x-jad) for x in ints)
    S0=-jad
    tol_sp=float(t['preregistered_tolerances']['ordinary_common_abs_spread'])
    tol_zero=float(t['preregistered_tolerances']['zero_intercept_abs'])
    if spread>tol_sp:
        cls='C10_65B0_PREFLIGHT_TECHNICAL_AMBIGUOUS'
    elif abs(jad)<=tol_zero:
        cls='C10_65B0_ZERO_CHARGE_ADIABATIC_COMPATIBLE_SCOPED'
    else:
        cls='C10_65B0_ZERO_CHARGE_ADIABATIC_INCOMPATIBLE_SCOPED'

    out={
      'schema':'RTK_C10_65B0_ZERO_CHARGE_ADIABATIC_PREFLIGHT_RESULT_v1',
      'gate':'C10.65b0',
      'classification':cls,
      'target':'research/theory_targets/RTK_C10_65B0_ZERO_CHARGE_ADIABATIC_PREFLIGHT_TARGET_v1.json',
      'exact_logic':{
        'gauge_invariant_component_curvature':'J_i=delta_i/(1+w_i)-3 Psi_N = delta_i,pref/(1+w_i)-3 psi_pref',
        'relative_entropy':'S_ij=J_i-J_j',
        'C10_64_boundary':'J_khr=I_khr=0',
        'adiabatic_criterion':'J_khr=J_b=J_g=J_ur at leading regular order, not J_i=0 component by component',
        'consequence':'the C10.64 absolute zero-charge boundary is compatible with a nonzero-curvature ordinary adiabatic mode iff the common ordinary J_ad tends to zero'
      },
      'low_k_records':rows,
      'affine_k2_fits':fits,
      'diagnostics':{
        'ordinary_common_J_ad_intercept':jad,
        'ordinary_intercept_abs_spread':spread,
        'zero_charge_relative_entropy_intercept_S_khr_minus_ad':S0,
        'ordinary_common_abs_spread_tolerance':tol_sp,
        'zero_intercept_abs_tolerance':tol_zero,
        'low_k_values_Mpc_inv':[float(r['k_Mpc_inv']) for r in recs]
      },
      'architecture_decision':(
        'If incompatible, preserve C10.64 as an exact zero-shift-charge sector theorem but do not call that absolute-zero sector the generic cosmological adiabatic branch. '
        'The replacement adiabatic boundary is I_khr=J_ad, and the independent neutral isocurvature coordinate is Delta I_iso=I_khr-J_ad. '
        'The frozen C10.65b zero-charge rank contract must therefore be superseded before implementation rather than interpreted as an adiabatic uniqueness test.'
      ),
      'next_gate':(
        'If incompatible, freeze C10.65c with the corrected common-curvature boundary I_khr=J_ad, derive delta_khr0 from it, solve V_khr0 and B0 from the completed preferred DAE O(k^2) system, and rerun the one-growing-direction rank test. '
        'If compatible, proceed with the existing C10.65b contract.'
      ),
      'non_claims':t['non_claims']
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps(out['diagnostics'],sort_keys=True))

if __name__=='__main__': main()
