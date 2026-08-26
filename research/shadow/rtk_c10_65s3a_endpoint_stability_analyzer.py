#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def finite(x): return math.isfinite(float(x))
def parse_observer(path):
    rows=[]; ns=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N']; nd=['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime']; nk=['B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip']; nr=['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm','feedback_denominator','implicit_denominator']
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',');
        if len(p)!=63: raise RuntimeError(f'observer columns {len(p)} != 63')
        r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8]),'_line':line.strip()}; j=9
        for n in ns: r[n]=float(p[j]); j+=1
        for n in nd: r[n]=float(p[j]); j+=1
        for n in nk: r[n]=float(p[j]); j+=1
        for n in nr: r[n]=float(p[j]); j+=1
        r['Fl']={l:float(p[j+l-3]) for l in range(3,18)}; rows.append(r)
    return rows
def parse_trace(path):
    G={}; beg=[]; end=[]
    for line in Path(path).read_text().splitlines():
        p=line.split(','); kind=p[0]; k=float(p[1])
        if kind=='BEGIN': beg.append(k); G.setdefault(k,[])
        elif kind=='END': end.append(k)
        elif kind=='ACCEPT': G.setdefault(k,[]).append({'x0':float(p[2]),'x1':float(p[3]),'htry':float(p[4]),'hdid':float(p[5]),'hnext':float(p[6]),'rejected':int(p[7]),'errmax':float(p[8])})
        else: raise RuntimeError(kind)
    return G,beg,end
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--observer',required=True); ap.add_argument('--trace',required=True); ap.add_argument('--s2k-observer',required=True); ap.add_argument('--off-identity',required=True); ap.add_argument('--interval-patch',required=True); ap.add_argument('--trace-patch',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S3A_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_TARGET_v1.json'); s2=L('research/theory_results/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_RESULT_v1.json'); k2=L('research/theory_results/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_EXECUTION'; assert s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'; assert k2['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED'
    off=json.loads(Path(a.off_identity).read_text()); rows=parse_observer(a.observer); old=parse_observer(a.s2k_observer); G,beg,end=parse_trace(a.trace); ks=[float(x) for x in t['domain']['k_Mpc_inv']]
    B=sorted((x for x in rows if x['phase']=='BEFORE'),key=lambda x:x['k']); A=sorted((x for x in rows if x['phase']=='AFTER'),key=lambda x:x['k']); OB=sorted((x for x in old if x['phase']=='BEFORE'),key=lambda x:x['k'])
    checks={}; checks['original_s2_preserved_fail']=s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'; checks['s2k_preserved_pass']=k2['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED'; checks['record_counts']=len(B)==len(A)==len(OB)==4 and [x['k'] for x in B]==ks and [x['k'] for x in A]==ks
    checks['off_identity']=off.get('all_four_numeric_rows_sha256_identical') is True; checks['before_observer_exact_s2k']=checks['record_counts'] and all(b['_line']==o['_line'] for b,o in zip(B,OB)); checks['first_rhs_bound_inherited']=checks['before_observer_exact_s2k'] and k2['inherited_original_max_first_rhs_relative'] < float(t['frozen_checks']['first_rhs_relative_tolerance_inherited'])
    dt=float(t['prospective_interval']['delta_tau_Mpc']); atol=float(t['frozen_checks']['interval_width_absolute_tolerance_Mpc']); widths={format(b['k'],'.17g'):a2['tau']-b['tau'] for b,a2 in zip(B,A)}; checks['interval_width']=checks['record_counts'] and all(abs(v-dt)<=atol for v in widths.values())
    checks['trace_markers']=sorted(beg)==ks and sorted(end)==ks
    minacc=int(t['prospective_interval']['minimum_accepted_substeps_required_per_anchor']); trace_records=[]; tracefinite=True; enough=True; accounting=True
    for ar in A:
        k=ar['k']; q=G.get(k,[]); ac=len(q); rej=sum(x['rejected'] for x in q); trials=ac+rej; tracefinite &= all(finite(v) for x in q for v in (x['x0'],x['x1'],x['htry'],x['hdid'],x['hnext'],x['errmax'])) and all(x['rejected']>=0 for x in q); enough &= ac>=minacc; expected=ac+5*trials+1; accounting &= ar['rhs_calls']==expected
        trace_records.append({'k':k,'accepted_substeps':ac,'rejected_trials':rej,'rkck_trials':trials,'after_rhs_calls':ar['rhs_calls'],'accounting_rhs_calls':expected,'sum_hdid':sum(x['hdid'] for x in q),'minimum_hdid':min((x['hdid'] for x in q),default=None),'maximum_hdid':max((x['hdid'] for x in q),default=None)})
    checks['minimum_accepted_substeps']=enough; checks['all_adaptive_trace_values_finite']=tracefinite; checks['trace_rhs_accounting']=accounting
    state_names=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','feedback_denominator','implicit_denominator']; checks['post_endpoint_state_all_finite']=checks['record_counts'] and all(finite(x[n]) for x in A for n in state_names) and all(finite(v) for x in A for v in x['Fl'].values())
    cn=['A_norm','H_norm','M_norm']; checks['endpoint_constraints_all_finite']=checks['record_counts'] and all(finite(x[n]) for x in B+A for n in cn)
    drift={}; maxend=0.; maxchg=0.
    for b,a2 in zip(B,A):
        q={}
        for z in ['A','H','M']:
            raw=z+'_raw'; norm=z+'_norm'; maxend=max(maxend,abs(a2[norm])); maxchg=max(maxchg,abs(a2[norm]-b[norm])); q[z]={'before_raw':b[raw],'after_raw':a2[raw],'before_normalized':b[norm],'after_normalized':a2[norm],'absolute_change_normalized':abs(a2[norm]-b[norm])}
        drift[format(b['k'],'.17g')]=q
    checks['max_abs_endpoint_normalized_residual']=maxend<=float(t['frozen_checks']['max_abs_endpoint_normalized_residual']); checks['max_abs_normalized_constraint_change']=maxchg<=float(t['frozen_checks']['max_abs_normalized_constraint_change'])
    ip=Path(a.interval_patch).read_text(); tp=Path(a.trace_patch).read_text(); checks['same_kernel_physics_and_tolerance_static_guard']=('implementation-scale-only interval patch' in ip and 'tol_perturb_integration' not in ip and 'dy[' not in ip and 'index_pt_' not in ip and 'diagnostics only' in tp and 'no integration mutation' in tp and 'tol_perturb_integration =' not in tp)
    checks['threshold_changed']=False
    passed=all(v is True for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S3A_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_RESULT_v1','gate':'C10.65s3a','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'interval_delta_tau_Mpc':dt,'observed_widths_Mpc':widths,'trace_records':trace_records,'constraint_drift':drift,'max_abs_endpoint_normalized_residual':maxend,'max_abs_normalized_constraint_change':maxchg,'frozen_constraint_bound':float(t['constraint_policy']['frozen_max_abs_endpoint_normalized_residual']),'original_s2_classification_preserved':s2['classification'],'s2k_classification_preserved':k2['classification'],'threshold_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'C10.65s3a failed a preregistered endpoint-stability check; preserve the result and diagnose without post-hoc changing the interval or drift bounds.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s3a with the frozen interval and bounds unchanged.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(out['classification']); print(json.dumps({'checks':checks,'maxend':maxend,'maxchg':maxchg,'trace':trace_records},sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
