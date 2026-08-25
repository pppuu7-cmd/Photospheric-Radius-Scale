#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
target=json.loads((ROOT/'research/theory_targets/RTK_C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_TARGET_v1.json').read_text())
parent=json.loads((ROOT/'research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json').read_text())
assert target['status']=='FROZEN_BEFORE_EXECUTION'
assert parent['classification']=='C10_PHYSICAL_CLASS_SOURCE_EXPORT_PASS'

ks=sorted(float(x) for x in parent['actual_k_values_Mpc_inv'])
a_on=max(float(x['a_min']) for x in parent['files'])
k_ref=max(ks)
ufracs=[0.25,0.5,1.0]
lfracs=[0.25,0.5,1.0]
u_cap=0.01
dh_cap=0.01

def lam_from_dh(dh):
    return (1.0+2.0/(1.0-dh))/3.0

def mc_from_u(u):
    return (k_ref/a_on)*math.sqrt((1.0-u)/u)

def aeff(a,k,mc):
    return k*k/(k*k+a*a*mc*mc)

points=[]
max_roundtrip=0.0
max_filter=0.0
for fu in ufracs:
    u=fu*u_cap
    mc=mc_from_u(u)
    ur=aeff(a_on,k_ref,mc)
    max_roundtrip=max(max_roundtrip,abs(ur-u))
    for fl in lfracs:
        dh=fl*dh_cap
        lam=lam_from_dh(dh)
        assert lam>1.0 and mc>0.0
        per_k={format(k,'.17g'):aeff(a_on,k,mc) for k in ks}
        worst=max(per_k.values())
        max_filter=max(max_filter,worst)
        assert worst<=u+2e-15
        assert u<=0.01+1e-15
        points.append({
            'u_fraction':fu,'u_onset_kref':u,'M_c_Mpc_inv':mc,
            'delta_H_fraction':fl,'delta_H':dh,'lambda_HL':lam,
            'a1_eff_at_common_onset_by_k':per_k,
            'eta0_min_formula':'3*(3*lambda_HL-1)*H_EFT^2/(64*M_c^2)',
            'local_upper_guard':'M_c^2 <= k_local_phys^2/99 plus isolated rank-root buffer remains to be checked'
        })

# Exact algebraic lambda roundtrip.
for p in points:
    dh2=1.0-2.0/(3.0*p['lambda_HL']-1.0)
    assert abs(dh2-p['delta_H'])<2e-15

out={
  'schema':'RTK_C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_RESULT_v1',
  'classification':'C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_PASS_SCOPED',
  'production_history_reference':{
    'classification':parent['classification'],
    'a_on_common_support':a_on,
    'k_ref_Mpc_inv':k_ref,
    'k_values_Mpc_inv':ks,
    'onset_semantics':'max of persisted per-file a_min; common exported-history support only, not a fundamental EFT cutoff'
  },
  'ir_gravity_truncation':{
    'Pcal':1.0,'alpha1':0.0,'E_th':2.0,
    'guard':'two-spatial-derivative IR truncation only; higher-spatial UV coefficients remain unfrozen'
  },
  'grid_definition':{
    'u_cap':u_cap,'u_fractions':ufracs,'delta_H_cap':dh_cap,'delta_H_fractions':lfracs,
    'point_count':len(points),
    'M_c_formula':'(k_ref/a_on)*sqrt((1-u)/u)',
    'lambda_formula':'(1+2/(1-delta_H))/3'
  },
  'machine_guards':{
    'max_u_roundtrip_abs_error':max_roundtrip,
    'max_a1_eff_over_exported_k_at_common_onset':max_filter,
    'strong_filter_cap_satisfied':max_filter<=0.01+2e-15,
    'later_time_monotonicity':'for fixed positive M_c,k, a1_eff=k^2/(k^2+a^2 M_c^2) decreases with a>0'
  },
  'points':points,
  'unselected_guards':{
    'eta0':'not selected; evaluate eta0_min on the actual replay background',
    'k_local':'not selected; global local/cosmology upper-window certification remains open',
    'isolated_rank_root':'must remain separately buffered if positive',
    'higher_spatial_UV':'not selected; later UV-sensitivity gate'
  },
  'interpretation':'This is a deterministic non-fitted diagnostic grid derived from already persisted history support and dimensionless 1-percent design caps. It is suitable for attractor sensitivity tests but is not a physical parameter fit or a globally certified completion window.',
  'next_gate':'C10.62b reduced finite-onset memory-loss test on a regenerated pinned production RTK background across all nine diagnostic points, followed by the full photon+baryon+UR hierarchy.',
  'non_claims':['not parameter selection','not fundamental EFT onset','not local-window certification','not UV completion','not attractor theorem','not spectra or likelihood evidence']
}
Path('c10_diagnostic_completion_onset_protocol_result.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(out['classification'],json.dumps(out,sort_keys=True))
