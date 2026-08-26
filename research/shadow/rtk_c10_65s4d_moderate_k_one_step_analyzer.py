#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def rel(a,b):
    a=float(a);b=float(b);return abs(a-b)/max(abs(a),abs(b),1e-300)
def finite(x): return math.isfinite(float(x))
def parse(path):
    rows=[]; ns=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N']; nd=['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime']; nk=['B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip']; nr=['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm','feedback_denominator','implicit_denominator']
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',');
        if len(p)!=63: raise RuntimeError(f'columns {len(p)} != 63')
        r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8])};j=9
        for n in ns: r[n]=float(p[j]);j+=1
        for n in nd: r[n]=float(p[j]);j+=1
        for n in nk: r[n]=float(p[j]);j+=1
        for n in nr: r[n]=float(p[j]);j+=1
        r['Fl']={l:float(p[j+l-3]) for l in range(3,18)};rows.append(r)
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--observer',required=True);ap.add_argument('--off-identity',required=True);ap.add_argument('--domain-patch',required=True);ap.add_argument('--bridge',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S4D_MODERATE_K_ONE_ACCEPTED_STEP_PRODUCTION_CANARY_TARGET_v1.json'); b=L('research/theory_results/RTK_C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_RESULT_v1.json'); c=L('research/theory_results/RTK_C10_65S4C_MODERATE_K_CURRENT_STATE_FIRST_RHS_PARITY_RESULT_v2.json'); k=L('research/theory_results/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1.json'); e=L('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION';assert b['classification']=='C10_65S4B_MODERATE_K_COMPLETED_ONSET_SEED_PASS_SCOPED';assert c['classification']=='C10_65S4C_MODERATE_K_CURRENT_STATE_FIRST_RHS_PARITY_PASS_SCOPED';assert k['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED';assert e['classification']=='C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_FAIL_SCOPED'
    ks=[float(x) for x in t['domain']['k_Mpc_inv']]; br={float(r['k']):r for r in b['records']}; cr={float(r['k']):r for r in c['records']}; rows=parse(a.observer); B=sorted([r for r in rows if r['phase']=='BEFORE'],key=lambda x:x['k']); A=sorted([r for r in rows if r['phase']=='AFTER'],key=lambda x:x['k']); off=json.loads(Path(a.off_identity).read_text());fc=t['frozen_checks']
    checks={};checks['record_counts']=len(B)==len(A)==int(fc['record_count_each_phase']) and [r['k'] for r in B]==ks and [r['k'] for r in A]==ks;checks['off_identity']=off.get('all_two_numeric_rows_sha256_identical') is True
    maxcarrier=maxur=maxrhs=maxmetric=0.0; finite_post=True; finite_constraints=True; approx=True; onset=True; widths={}; drift={}
    smap={'phi':'phi_CLASS_equals_Psi_N','delta_b':'delta_b','theta_b':'theta_b','delta_g':'delta_g','theta_g':'theta_g','delta_ur':'delta_ur','theta_ur':'theta_ur','shear_ur':'shear_ur','delta_khr_N':'delta_cdm_khr','theta_khr_N':'theta_cdm_khr'}
    if checks['record_counts']:
      for q,z in zip(B,A):
        rb=br[q['k']];rc=cr[q['k']];car=rb['carrier']; U={int(x['l']):float(x['F_l']) for x in rb['ur_l_ge_3']}
        maxcarrier=max(maxcarrier,*(rel(q[n],car[m]) for n,m in smap.items()));maxur=max(maxur,*(rel(q['Fl'][l],U[l]) for l in range(3,18)))
        rr=rc['first_rhs']; refs={'phi_prime':rr['Psi_N_prime'],'theta_b_prime':rr['theta_b_prime'],'theta_g_prime':rr['theta_g_prime'],'theta_ur_prime':rr['theta_ur_prime'],'delta_khr_N_prime':rr['delta_khr_N_prime'],'theta_khr_N_prime':rr['theta_khr_N_prime'],'tca_slip':rr['tca_slip']}; maxrhs=max(maxrhs,*(rel(q[n],v) for n,v in refs.items()),rel(q['Phi_N']*q['k']*q['k'],rr['metric_euler']))
        cm=rc['current_metric']; maxmetric=max(maxmetric,rel(q['B'],cm['B']),rel(q['Psi_N'],cm['Psi_N']),rel(q['Phi_N'],cm['Phi_N']))
        approx &= q['tca']==z['tca']==int(fc['approximation_state']['TCA_enum']) and q['rsa']==z['rsa']==int(fc['approximation_state']['RSA_enum']) and q['ufa']==z['ufa']==int(fc['approximation_state']['UFA_enum']) and q['lmax']==z['lmax']==int(fc['approximation_state']['l_max_ur'])
        onset &= rel(q['a'],t['domain']['a_on'])<=float(fc['onset_relative_tolerance']); widths[format(q['k'],'.17g')]=z['tau']-q['tau']
        state=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','B','B_prime','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','feedback_denominator','implicit_denominator'];finite_post &= all(finite(z[n]) for n in state) and all(finite(v) for v in z['Fl'].values());finite_constraints &= all(finite(x[n]) for x in (q,z) for n in ['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm'])
        drift[format(q['k'],'.17g')]={m:{'before':q[m+'_norm'],'after':z[m+'_norm'],'absolute_change':abs(z[m+'_norm']-q[m+'_norm'])} for m in ['A','H','M','T']}
    pt=Path(a.domain_patch).read_text(); bs=Path(a.bridge).read_text(); low=['1.0000000000000001e-05','3.0000000000000001e-05']; static=('domain-only production patch' in pt and 'tol_perturb_integration' not in pt and 'dy[' not in pt and 'pvecmetric' not in pt); moderate=('static const s2seed S[2]' in bs and all(x not in bs for x in low)); nolegacy=all(x not in pt for x in ['deltaU_nlde','deltaV_nlde','deltaZ_nlde']); nodouble=('khr_class_sources_newtonian' not in pt and 'delta_khr_N' not in pt)
    checks.update({'boundary_carrier':maxcarrier<=float(fc['boundary_carrier_relative_tolerance_vs_s4b']),'boundary_higher_ur':maxur<=float(fc['boundary_higher_ur_relative_tolerance_vs_s4b']),'first_rhs':maxrhs<=float(fc['first_rhs_relative_tolerance_vs_s4c']),'kernel_metric':maxmetric<=float(fc['kernel_metric_relative_tolerance_vs_s4c']),'onset':onset,'approximation':approx,'before_rhs_calls':checks['record_counts'] and all(r['rhs_calls']==int(t['execution']['before_rhs_calls']) for r in B),'after_rhs_calls':checks['record_counts'] and all(r['rhs_calls']==int(t['execution']['after_rhs_calls']) for r in A),'step_width':checks['record_counts'] and all(abs(v-float(t['execution']['retry_width_Mpc']))<=float(fc['step_width_absolute_tolerance_Mpc']) for v in widths.values()),'post_step_finite':finite_post,'constraint_capture_finite':finite_constraints,'same_kernel_integrator_tolerance_static_guard':static,'moderate_k_seed_only_static_guard':moderate,'no_low_k_seed_lookup':moderate,'no_legacy_nlde_physical_role':nolegacy,'no_double_gauge_transform':nodouble,'s2e_failed_parent_preserved':True,'threshold_changed':False})
    passed=all(v for n,v in checks.items() if n!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S4D_MODERATE_K_ONE_ACCEPTED_STEP_PRODUCTION_CANARY_RESULT_v1','gate':'C10.65s4d','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'max_boundary_carrier_relative':maxcarrier,'max_boundary_higher_ur_relative':maxur,'max_first_rhs_relative_vs_s4c':maxrhs,'max_kernel_metric_relative_vs_s4c':maxmetric,'observed_step_widths_Mpc':widths,'constraint_drift_measurement_only':drift,'threshold_changed':False,'integrator_tolerance_changed':False,'s2e_classification_preserved':e['classification'],'interpretation':t['interpretation_if_pass'] if passed else 'At least one frozen moderate-k production-entry check failed; preserve the result and diagnose before any trajectory gate.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s4d without changing the frozen width, equations or tolerance post hoc.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n');print(out['classification']);print(json.dumps(checks,sort_keys=True));return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
