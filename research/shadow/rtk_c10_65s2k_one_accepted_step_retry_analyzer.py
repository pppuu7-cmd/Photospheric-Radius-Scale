#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def finite(x): return math.isfinite(float(x))
def parse(path):
    rows=[]
    ns=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N']
    nd=['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime']
    nk=['B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip']
    nr=['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm','feedback_denominator','implicit_denominator']
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',')
        if len(p)!=63: raise RuntimeError(f'columns {len(p)} != 63')
        r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8]),'_line':line.strip()}; j=9
        for n in ns: r[n]=float(p[j]); j+=1
        for n in nd: r[n]=float(p[j]); j+=1
        for n in nk: r[n]=float(p[j]); j+=1
        for n in nr: r[n]=float(p[j]); j+=1
        r['Fl']={l:float(p[j+l-3]) for l in range(3,18)}; rows.append(r)
    return rows
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--observer',required=True); ap.add_argument('--original-observer',required=True); ap.add_argument('--off-identity',required=True); ap.add_argument('--width-patch',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_TARGET_v1.json'); j=L('research/theory_results/RTK_C10_65S2J_PROSPECTIVE_RETRY_WIDTH_RESULT_v1.json'); s2=L('research/theory_results/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_RETRY_EXECUTION'; assert j['classification']=='C10_65S2J_PROSPECTIVE_RETRY_WIDTH_PASS_SCOPED'; assert s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'
    off=json.loads(Path(a.off_identity).read_text()); rows=parse(a.observer); orig=parse(a.original_observer); ks=[float(x) for x in t['frozen_domain']['k_Mpc_inv']]
    B=sorted((x for x in rows if x['phase']=='BEFORE'),key=lambda x:x['k']); A=sorted((x for x in rows if x['phase']=='AFTER'),key=lambda x:x['k']); OB=sorted((x for x in orig if x['phase']=='BEFORE'),key=lambda x:x['k'])
    checks={}; checks['original_s2_remains_fail']=s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'; checks['record_counts']=len(B)==len(A)==len(OB)==4 and [x['k'] for x in B]==ks and [x['k'] for x in A]==ks
    checks['off_identity']=off.get('all_four_numeric_rows_sha256_identical') is True
    # Full BEFORE rows include boundary state, first production RHS, kernel outputs and constraints; they must reproduce the immutable original s2 execution exactly.
    checks['before_observer_exact_original']=checks['record_counts'] and all(b['_line']==o['_line'] for b,o in zip(B,OB))
    checks['before_rhs_calls']=checks['record_counts'] and all(x['rhs_calls']==1 for x in B)
    checks['after_rhs_calls_exact7']=checks['record_counts'] and all(x['rhs_calls']==7 for x in A)
    w=float(t['retry_execution']['retry_width_Mpc']); atol=float(t['frozen_checks']['step_width_absolute_tolerance_Mpc'])
    widths={format(b['k'],'.17g'):(a2['tau']-b['tau']) for b,a2 in zip(B,A)}
    checks['retry_step_width']=checks['record_counts'] and all(abs(v-w)<=atol for v in widths.values())
    state_names=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','feedback_denominator','implicit_denominator']
    checks['post_state_finite']=checks['record_counts'] and all(finite(x[n]) for x in A for n in state_names) and all(finite(v) for x in A for v in x['Fl'].values())
    resnames=['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm']; checks['constraint_capture_finite']=checks['record_counts'] and all(finite(x[n]) for x in B+A for n in resnames)
    drift={}
    if checks['record_counts']:
        for b,a2 in zip(B,A):
            q={}
            for z in ['A','H','M']:
                raw=z+'_raw'; norm=z+'_norm'; q[z]={'before_raw':b[raw],'after_raw':a2[raw],'signed_change_raw':a2[raw]-b[raw],'absolute_change_raw':abs(a2[raw]-b[raw]),'before_normalized':b[norm],'after_normalized':a2[norm],'signed_change_normalized':a2[norm]-b[norm],'absolute_change_normalized':abs(a2[norm]-b[norm])}
            drift[format(b['k'],'.17g')]=q
    txt=Path(a.width_patch).read_text(); checks['same_kernel_and_tolerance_static_guard']=('implementation-scale-only retry patch' in txt and 'static const double DT=' in txt and 'tol_perturb_integration' not in txt and 'dy[' not in txt and 'index_pt_' not in txt)
    checks['first_rhs_bound_inherited']=s2['max_first_production_rhs_relative'] < float(t['frozen_checks']['first_rhs_relative_tolerance_inherited']) and checks['before_observer_exact_original']
    checks['threshold_unchanged']=s2['threshold_changed'] is False
    passed=all(checks.values())
    out={'schema':'RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1','gate':'C10.65s2k','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'retry_width_Mpc':w,'observed_step_widths_Mpc':widths,'expected_rhs_calls':7,'original_s2_classification_preserved':s2['classification'],'inherited_original_max_first_rhs_relative':s2['max_first_production_rhs_relative'],'constraint_drift_measurement_only':drift,'threshold_changed':False,'integrator_tolerance_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'The prospective retry failed at least one frozen requirement. Preserve both the original s2 failure and this retry result; diagnose before any stability gate.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s2k without changing the frozen retry width or tolerance post hoc.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(out['classification']); print(json.dumps(checks,sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
