#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def finite(x): return math.isfinite(float(x))

def parse(path):
    rows=[]
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',')
        if len(p)!=19: raise RuntimeError(f'geometry columns {len(p)} != 19: {line}')
        rows.append({
          'k':float(p[0]),'tau_z':float(p[1]),'a_z':float(p[2]),'inverse_roundtrip_relative_a_error':float(p[3]),
          'tau_corrected':float(p[4]),'a_corrected':float(p[5]),'corrected_forward_relative_a_error':float(p[6]),
          'integration_tau_lo':float(p[7]),'integration_tau_hi':float(p[8]),
          'interval_index_tau_z':int(p[9]),'interval_lo_tau_z':float(p[10]),'interval_hi_tau_z':float(p[11]),
          'interval_index_corrected':int(p[12]),'interval_lo_corrected':float(p[13]),'interval_hi_corrected':float(p[14]),
          'same_interval':int(p[15]),'corrected_tca':int(p[16]),'corrected_rsa':int(p[17]),'corrected_ufa':int(p[18])})
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--geometry',required=True);ap.add_argument('--patch',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S4A2_EXACT_ONSET_GEOMETRY_AUDIT_TARGET_v1.json')
    s4a=L('research/theory_results/RTK_C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_RESULT_v1.json')
    s4a1=L('research/theory_results/RTK_C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert s4a['classification']=='C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_FAIL_SCOPED'
    assert s4a['provenance']['github_actions_run_id']==33008706959
    assert s4a['provenance']['historical_failed_attempt_run_id']==33008095108
    assert s4a1['classification']=='C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_PASS_SCOPED'
    assert s4a1['provenance']['github_actions_run_id']==33008538013
    rows=sorted(parse(a.geometry),key=lambda r:r['k'])
    expected=[float(x) for x in t['fixed_domain']['k_Mpc_inv']]
    patch=Path(a.patch).read_text()
    allvals=[]
    for r in rows:
        for k,v in r.items():
            if isinstance(v,float): allvals.append(v)
    corrected_limit=float(t['frozen_checks']['corrected_forward_relative_a_error_max'])
    record_ok=len(rows)==2 and len({round(r['k'],15) for r in rows})==2 and all(abs(r['k']-k)<=5e-12*k for r,k in zip(rows,expected))
    corrected_inside=record_ok and all(r['interval_index_corrected']>=0 and r['integration_tau_lo']<=r['tau_corrected']<=r['integration_tau_hi'] for r in rows)
    containing=record_ok and all(r['interval_index_tau_z']>=0 and r['interval_index_corrected']>=0 and finite(r['interval_lo_tau_z']) and finite(r['interval_hi_tau_z']) and finite(r['interval_lo_corrected']) and finite(r['interval_hi_corrected']) for r in rows)
    membership_reported=record_ok and all(r['same_interval'] in (0,1) for r in rows)
    checks={
      'record_count':record_ok,
      'all_values_finite':record_ok and all(finite(x) for x in allvals),
      'inverse_roundtrip_error_measured':record_ok and all(r['inverse_roundtrip_relative_a_error']>=0.0 for r in rows),
      'corrected_forward_relative_a_error_max':record_ok and max((r['corrected_forward_relative_a_error'] for r in rows),default=math.inf)<=corrected_limit,
      'corrected_tau_inside_existing_integration_domain_both':corrected_inside,
      'containing_interval_exported_both':containing,
      'same_approximation_interval_membership_reported':membership_reported,
      'diagnostic_patch_contains_no_dy_assignment':'dy[' not in patch,
      'diagnostic_patch_contains_no_pvecmetric_assignment':'pvecmetric[' not in patch,
      'diagnostic_patch_contains_no_index_pt_state_assignment':'index_pt_' not in patch,
      'diagnostic_patch_contains_no_tolerance_or_approximation_criterion_mutation':(
          re.search(r'tol_perturb_integration\s*=',patch) is None and
          re.search(r'perturb_integration_stepsize\s*=',patch) is None and
          all(x not in patch for x in ['tight_coupling_trigger_tau_c_over_tau_h =','tight_coupling_trigger_tau_c_over_tau_k =','radiation_streaming_trigger_tau_over_tau_k =','ur_fluid_trigger_tau_over_tau_k ='])),
      'threshold_changed':False
    }
    passed=all(v is True for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False
    max_inv=max((r['inverse_roundtrip_relative_a_error'] for r in rows),default=math.nan)
    max_corr=max((r['corrected_forward_relative_a_error'] for r in rows),default=math.nan)
    out={'schema':'RTK_C10_65S4A2_EXACT_ONSET_GEOMETRY_AUDIT_RESULT_v1','gate':'C10.65s4a2','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'records':rows,'max_inverse_roundtrip_relative_a_error':max_inv,'max_corrected_forward_relative_a_error':max_corr,'historical_failures_preserved':[{'run_id':33008095108,'classification':'C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_FAIL_SCOPED'},{'run_id':33008706959,'classification':s4a['classification']}],'s4a1_parent':s4a1['classification'],'threshold_changed':False,'interpretation':('The remaining acquisition problem is now measured without changing the perturbation evolution: tau(z_on), its forward-spline round trip, a forward-spline-consistent tau_*, and both approximation-interval memberships are explicitly recorded for the two new k anchors.' if passed else 'The read-only exact-onset geometry audit failed at least one preregistered acquisition/source guard; do not alter the original s4a scientific target.'),'next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s4a2 without changing the original s4a scientific domain or guards.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification']);print(json.dumps({'checks':checks,'max_inverse_roundtrip':max_inv,'max_corrected':max_corr,'intervals':[{'k':r['k'],'iz':r['interval_index_tau_z'],'ic':r['interval_index_corrected'],'same':r['same_interval']} for r in rows]},sort_keys=True))
    raise SystemExit(0 if passed else 2)
if __name__=='__main__': main()
