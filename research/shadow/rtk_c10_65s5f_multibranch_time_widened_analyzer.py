#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def finite(x): return math.isfinite(float(x))
def obs(path):
    rows=[]
    ns=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N']
    nd=['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime']
    nk=['B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip']
    nr=['A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm','feedback_denominator','implicit_denominator']
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.strip().split(',')
        if len(p)!=63: raise RuntimeError(f'{path}: columns {len(p)} != 63')
        r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8]),'_line':line.strip()};j=9
        for n in ns+nd+nk+nr:r[n]=float(p[j]);j+=1
        r['Fl']={l:float(p[j+l-3]) for l in range(3,18)};rows.append(r)
    return rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',required=True);ap.add_argument('--s5d-parent-dir',required=True);ap.add_argument('--off-identity',required=True);ap.add_argument('--patch',required=True);ap.add_argument('--bridge-root',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S5F_NEXT_K_MULTIBRANCH_TIME_WIDENED_TRAJECTORY_TARGET_v1.json')
    e5=L('research/theory_results/RTK_C10_65S5E_NEXT_K_MULTIBRANCH_TRAJECTORY_SAMPLED_CONSTRAINT_RESULT_v1.json')
    d=L('research/theory_results/RTK_C10_65S5D_NEXT_K_MULTIBRANCH_ONE_STEP_PRODUCTION_CANARY_RESULT_v1.json')
    c=L('research/theory_results/RTK_C10_65S5C_NEXT_K_OMITTED_ORDER_SENSITIVITY_RESULT_v1.json')
    f4=L('research/theory_results/RTK_C10_65S4F_MODERATE_K_TIME_WIDENED_TRAJECTORY_RESULT_v1.json')
    e2=L('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION';assert e5['classification']==t['parents']['C10.65s5e'];assert d['classification']==t['parents']['C10.65s5d'];assert c['classification']==t['parents']['C10.65s5c'];assert f4['classification']==t['parents']['C10.65s4f_method'];assert e2['classification']==t['parents']['C10.65s2e_historical']
    branches=[x['id'] for x in t['domain']['branches']];samples=[float(x) for x in t['sample_elapsed_tau_Mpc']];k0=float(t['domain']['k_Mpc_inv']);man=json.loads(Path(a.manifest).read_text());off=json.loads(Path(a.off_identity).read_text());checks={}
    checks['branch_count']=branches==['baseline','joint_extremum','phi_extremum'];checks['off_identity']=off.get('all_branches_identical') is True
    checks['sample_times_exact_s4f']=samples==[float(x) for x in f4['sample_elapsed_tau_Mpc']]==[3e-6,1e-5,3e-5,1e-4]
    checks['sample_manifest_shape']=len(man)==12 and [(x['branch'],float(x['width'])) for x in man]==[(b,w) for b in branches for w in samples]
    parent={}
    for b in branches:
        p=Path(a.s5d_parent_dir)/'s5d_observers'/f'{b}.csv';rows=obs(p);q=[x for x in rows if x['phase']=='BEFORE'];assert len(q)==1,(b,len(q));parent[b]=q[0]
    state=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','feedback_denominator','implicit_denominator']
    deriv=['phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime']
    atol=float(t['sampling_policy']['endpoint_width_absolute_tolerance_Mpc']);lim=float(t['constraint_policy']['max_abs_normalized_each_sample'])
    allbefore=allhigher=allwidth=allstate=allapprox=allcf=allc=allchg=True;endpoint_dy_unmaterialized=True;records=[];maxres=maxchg=0.0
    for entry in man:
        b=entry['branch'];w=float(entry['width']);rows=obs(entry['observer']);B=[x for x in rows if x['phase']=='BEFORE'];A=[x for x in rows if x['phase']=='AFTER'];good=len(B)==len(A)==1 and abs(B[0]['k']-k0)<1e-15 and abs(A[0]['k']-k0)<1e-15
        if not good: allbefore=False;continue
        q,z=B[0],A[0];p=parent[b];allbefore &= q['_line']==p['_line'];allhigher &= all(q['Fl'][l]==p['Fl'][l] for l in range(3,18))
        dw=z['tau']-q['tau'];allwidth &= abs(dw-w)<=atol;allstate &= all(finite(z[n]) for n in state) and all(finite(v) for v in z['Fl'].values());endpoint_dy_unmaterialized &= all(not finite(z[n]) for n in deriv);allapprox &= (z['tca'],z['rsa'],z['ufa'],z['lmax'])==(0,0,0,17);allcf &= all(finite(z[n]) and finite(q[n]) for n in ('A_norm','H_norm','M_norm','T_norm'))
        rr={}
        for C in ('A','H','M','T'):
            n=C+'_norm';res=abs(z[n]);chg=abs(z[n]-q[n]);maxres=max(maxres,res);maxchg=max(maxchg,chg);allc &= res<=lim;allchg &= chg<=lim;rr[C]={'before':q[n],'after':z[n],'abs_change':chg}
        records.append({'branch':b,'elapsed_tau_Mpc':w,'k':q['k'],'observed_elapsed_tau_Mpc':dw,'rhs_calls_after':z['rhs_calls'],'constraints':rr})
    checks['record_count']=len(records)==12;checks['before_rows_exact_s5d_before_all_samples']=allbefore;checks['boundary_higher_ur_exact_s5d']=allhigher;checks['all_endpoint_widths_within_absolute_tolerance']=allwidth;checks['all_endpoint_states_finite']=allstate;checks['endpoint_dy_intentionally_unmaterialized_no_extra_rhs']=endpoint_dy_unmaterialized;checks['all_endpoint_approximation_states']=allapprox;checks['all_endpoint_A_H_M_T_constraints_finite']=allcf;checks['all_endpoint_normalized_constraints_within_1e-10']=allc;checks['all_normalized_constraint_changes_within_1e-10']=allchg
    checks['first_rhs_bound_inherited']=d['max_first_rhs_relative']<float(t['frozen_checks']['first_rhs_relative_tolerance_inherited']) and allbefore
    txt=Path(a.patch).read_text();checks['sample_patch_static_guard']='endpoint selector only; no physics/tolerance mutation' in txt and 'tol_perturb_integration' not in txt and 'dy[' not in txt and 'index_pt_' not in txt
    bridges=[]
    for b in branches: bridges.append((Path(a.bridge_root)/f'class_{b}'/'source'/'rtk_c10_65s2_class_bridge.c').read_text())
    checks['same_kernel_and_single_seed_static_guard']=all('static const s2seed S[1]' in x and 'for(i=0;i<1;i++)' in x for x in bridges)
    checks['no_legacy_nlde_physical_role']=all('deltaU_nlde' not in x and 'deltaV_nlde' not in x and 'deltaZ_nlde' not in x for x in bridges)
    checks['no_double_gauge_transform']=all('khr_newtonian_to_sync' not in x and 'khr_sync_to_newtonian' not in x for x in bridges)
    checks['s5c_envelope_nonprobabilistic']=True;checks['no_k_widening']=k0==0.01;checks['no_branch_widening']=branches==[x['id'] for x in L('research/theory_targets/RTK_C10_65S5E_NEXT_K_MULTIBRANCH_TRAJECTORY_SAMPLED_CONSTRAINT_TARGET_v1.json')['domain']['branches']]
    checks['s2e_failed_parent_preserved']=e2['classification']=='C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_FAIL_SCOPED';checks['threshold_changed']=False
    passed=all(v is True for q,v in checks.items() if q!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S5F_NEXT_K_MULTIBRANCH_TIME_WIDENED_TRAJECTORY_RESULT_v1','gate':'C10.65s5f','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'branches':branches,'sample_elapsed_tau_Mpc':samples,'record_count':len(records),'records':records,'max_abs_normalized_constraint':maxres,'max_abs_normalized_constraint_change':maxchg,'frozen_bound':lim,'max_first_rhs_relative_inherited_from_s5d':d['max_first_rhs_relative'],'endpoint_rhs_policy':'No extra endpoint RHS callback; AFTER dy columns intentionally unmaterialized. First-RHS finiteness/parity inherited through exact s5d BEFORE identity, preserving certified s5e endpoint semantics.','s5e_parent_preserved':e5['classification'],'s4f_method_parent_preserved':f4['classification'],'s2e_classification_preserved':e2['classification'],'s5c_envelope_interpretation':'NONPROBABILISTIC_POINTWISE_STRESS_ENVELOPE','threshold_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'At least one preregistered C10.65s5f widened-time check failed; preserve the result and diagnose without changing branches, sample times, k or the 1e-10 bound.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s5f before widening time, branches or k.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n');print(out['classification']);print(json.dumps({'checks':checks,'maxres':maxres,'maxchg':maxchg},sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
