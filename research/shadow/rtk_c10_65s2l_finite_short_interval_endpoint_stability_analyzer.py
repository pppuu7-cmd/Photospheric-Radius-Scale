#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def finite(x): return math.isfinite(float(x))
def obs(path):
    rows=[]; ns=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N']; nd=['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime']; nk=['B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip']; nr=['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm','feedback_denominator','implicit_denominator']
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',');
        if len(p)!=63: raise RuntimeError(f'observer columns {len(p)} != 63')
        r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8]),'_line':line.strip()}; j=9
        for n in ns+nd+nk+nr: r[n]=float(p[j]); j+=1
        r['Fl']={l:float(p[j+l-3]) for l in range(3,18)}; rows.append(r)
    return rows
def trace(path):
    d={}
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(','); tag=p[0]; k=float(p[1]); q=d.setdefault(k,{'begin':0,'end':0,'accept':[]})
        if tag=='BEGIN': q['begin']+=1
        elif tag=='END': q['end']+=1
        elif tag=='ACCEPT': q['accept'].append({'x0':float(p[2]),'x1':float(p[3]),'htry':float(p[4]),'hdid':float(p[5]),'hnext':float(p[6]),'rejected_trials':int(p[7]),'errmax':float(p[8])})
        else: raise RuntimeError('unknown trace tag '+tag)
    return d
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--observer',required=True); ap.add_argument('--s2k-observer',required=True); ap.add_argument('--trace',required=True); ap.add_argument('--off-identity',required=True); ap.add_argument('--interval-patch',required=True); ap.add_argument('--trace-patch',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S2L_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_TARGET_v1.json'); k=L('research/theory_results/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1.json'); s2=L('research/theory_results/RTK_C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_EXECUTION'; assert k['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED'; assert s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'
    rows=obs(a.observer); kr=obs(a.s2k_observer); tr=trace(a.trace); off=json.loads(Path(a.off_identity).read_text()); ks=[float(x) for x in t['frozen_domain']['k_Mpc_inv']]
    B=sorted((x for x in rows if x['phase']=='BEFORE'),key=lambda x:x['k']); A=sorted((x for x in rows if x['phase']=='AFTER'),key=lambda x:x['k']); KB=sorted((x for x in kr if x['phase']=='BEFORE'),key=lambda x:x['k'])
    checks={}; checks['original_s2_remains_fail']=s2['classification']=='C10_65S2_DIRECT_ONSET_ONE_STEP_PRODUCTION_CANARY_FAIL_SCOPED'; checks['s2k_remains_pass']=k['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED'; checks['record_counts']=len(B)==len(A)==len(KB)==4 and [x['k'] for x in B]==ks and [x['k'] for x in A]==ks
    checks['off_identity']=off.get('all_four_numeric_rows_sha256_identical') is True
    checks['before_exact_s2k']=checks['record_counts'] and all(b['_line']==q['_line'] for b,q in zip(B,KB))
    width=float(t['execution']['finite_short_interval_Mpc']); atol=float(t['frozen_checks']['terminal_interval_absolute_tolerance_Mpc']); widths={format(b['k'],'.17g'):a2['tau']-b['tau'] for b,a2 in zip(B,A)} if checks['record_counts'] else {}
    checks['terminal_interval']=checks['record_counts'] and all(abs(v-width)<=atol for v in widths.values())
    state=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','feedback_denominator','implicit_denominator']
    checks['terminal_finite']=checks['record_counts'] and all(finite(x[n]) for x in A for n in state) and all(finite(v) for x in A for v in x['Fl'].values())
    checks['terminal_approximation_state']=checks['record_counts'] and all((x['tca'],x['rsa'],x['ufa'],x['lmax'])==(0,0,0,17) for x in A)
    lim=float(t['frozen_checks']['terminal_constraint_normalized_abs_max']); terminal={}
    if checks['record_counts']:
        for x in A: terminal[format(x['k'],'.17g')]={'A_norm':x['A_norm'],'H_norm':x['H_norm'],'M_norm':x['M_norm']}
    checks['terminal_constraints']=checks['record_counts'] and all(abs(x[n])<=lim and finite(x[n]) for x in A for n in ('A_norm','H_norm','M_norm'))
    minacc=int(t['execution']['minimum_accepted_substeps_per_anchor']); stats={}; traceok=True
    for kk in ks:
        q=tr.get(kk); ok=q is not None and q['begin']==1 and q['end']==1 and len(q['accept'])>=minacc and all(finite(z['hdid']) and finite(z['errmax']) and z['hdid']>0 for z in q['accept'])
        traceok &= ok
        if q: stats[format(kk,'.17g')]={'accepted_substeps':len(q['accept']),'rejected_trials':sum(z['rejected_trials'] for z in q['accept']),'minimum_hdid':min((z['hdid'] for z in q['accept']),default=None),'maximum_errmax_on_accepted_trial':max((z['errmax'] for z in q['accept']),default=None),'sum_hdid':sum(z['hdid'] for z in q['accept'])}
    checks['adaptive_trace_minimum_steps']=traceok
    checks['trace_interval_consistency']=traceok and all(abs(v['sum_hdid']-width)<=atol for v in stats.values())
    ip=Path(a.interval_patch).read_text(); tp=Path(a.trace_patch).read_text(); checks['same_kernel_state_ownership_tolerance_guard']=('implementation-scale-only finite-interval patch' in ip and 'static const double DT=' in ip and 'tol_perturb_integration' not in ip and 'dy[' not in ip and 'index_pt_' not in ip and 'diagnostics only; no integration mutation' in tp)
    checks['first_rhs_bound_inherited']=k['inherited_original_max_first_rhs_relative']<float(t['frozen_checks']['first_rhs_relative_tolerance_inherited']) and checks['before_exact_s2k']
    checks['threshold_unchanged']=k['threshold_changed'] is False
    passed=all(checks.values()); out={'schema':'RTK_C10_65S2L_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_RESULT_v1','gate':'C10.65s2l','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'finite_short_interval_Mpc':width,'observed_terminal_widths_Mpc':widths,'adaptive_trace':stats,'terminal_constraints':terminal,'prospective_terminal_constraint_bound':lim,'original_s2_classification_preserved':s2['classification'],'s2k_classification_preserved':k['classification'],'threshold_changed':False,'integrator_tolerance_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'The frozen finite-short-interval endpoint gate failed at least one prospective requirement. Diagnose without weakening the frozen interval or constraint tolerance post hoc.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s2l before any time/domain widening.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(out['classification']); print(json.dumps(checks,sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': raise SystemExit(main())
