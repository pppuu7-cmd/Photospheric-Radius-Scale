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
        if len(p)!=63: raise RuntimeError(f'columns {len(p)} != 63')
        r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8]),'_line':line.strip()};j=9
        for n in ns+nd+nk+nr:r[n]=float(p[j]);j+=1
        r['Fl']={l:float(p[j+l-3]) for l in range(3,18)};rows.append(r)
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--manifest',required=True);ap.add_argument('--s2k-observer',required=True);ap.add_argument('--off-identity',required=True);ap.add_argument('--patch',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S3B_TRAJECTORY_SAMPLED_CONSTRAINT_TARGET_v1.json');s3=L('research/theory_results/RTK_C10_65S3A_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_RESULT_v1.json');k2=L('research/theory_results/RTK_C10_65S2K_ONE_ACCEPTED_STEP_RETRY_RESULT_v1.json');assert t['status']=='FROZEN_BEFORE_EXECUTION';assert s3['classification']=='C10_65S3A_FINITE_SHORT_INTERVAL_ENDPOINT_STABILITY_PASS_SCOPED';assert k2['classification']=='C10_65S2K_ONE_ACCEPTED_STEP_RETRY_PASS_SCOPED'
    man=json.loads(Path(a.manifest).read_text()); old=obs(a.s2k_observer);OB=sorted((x for x in old if x['phase']=='BEFORE'),key=lambda x:x['k']);ks=[float(x) for x in t['domain']['k_Mpc_inv']];samples=[float(x) for x in t['sample_elapsed_tau_Mpc']];off=json.loads(Path(a.off_identity).read_text());checks={}
    checks['off_identity']=off.get('all_four_numeric_rows_sha256_identical') is True; checks['sample_manifest_shape']=len(man)==len(samples) and [float(x['width']) for x in man]==samples
    state=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','feedback_denominator','implicit_denominator']
    atol=float(t['sampling_policy']['endpoint_width_absolute_tolerance_Mpc']);lim=1e-10; allbefore=True;allwidth=True;allfinite=True;allapprox=True;allcf=True;allc=True;allchg=True;records=[];maxres=0.;maxchg=0.
    for entry in man:
        w=float(entry['width']); rows=obs(entry['observer']);B=sorted((x for x in rows if x['phase']=='BEFORE'),key=lambda x:x['k']);A=sorted((x for x in rows if x['phase']=='AFTER'),key=lambda x:x['k']); good=len(B)==len(A)==4 and [x['k'] for x in B]==ks and [x['k'] for x in A]==ks; allbefore &= good and all(b['_line']==o['_line'] for b,o in zip(B,OB))
        for b,z in zip(B,A):
            dw=z['tau']-b['tau']; allwidth &= abs(dw-w)<=atol; allfinite &= all(finite(z[n]) for n in state) and all(finite(v) for v in z['Fl'].values()); allapprox &= (z['tca'],z['rsa'],z['ufa'],z['lmax'])==(0,0,0,17); allcf &= all(finite(z[n]) and finite(b[n]) for n in ('A_norm','H_norm','M_norm'))
            rr={};
            for q in ('A','H','M'):
                n=q+'_norm';res=abs(z[n]);chg=abs(z[n]-b[n]);maxres=max(maxres,res);maxchg=max(maxchg,chg);allc &= res<=lim;allchg &= chg<=lim;rr[q]={'before':b[n],'after':z[n],'abs_change':chg}
            records.append({'elapsed_tau_Mpc':w,'k':b['k'],'observed_elapsed_tau_Mpc':dw,'rhs_calls_after':z['rhs_calls'],'constraints':rr})
    checks['record_count']=len(records)==28;checks['before_rows_exact_s2k_before_all_samples']=allbefore;checks['all_endpoint_widths_within_absolute_tolerance']=allwidth;checks['all_endpoint_states_finite']=allfinite;checks['all_endpoint_approximation_states']=allapprox;checks['all_endpoint_constraints_finite']=allcf;checks['all_endpoint_normalized_constraints_within_1e-10']=allc;checks['all_normalized_constraint_changes_within_1e-10']=allchg;checks['first_rhs_bound_inherited']=k2['inherited_original_max_first_rhs_relative']<5e-9 and allbefore
    txt=Path(a.patch).read_text();checks['same_kernel_and_tolerance_static_guard']='endpoint selector only; no physics/tolerance mutation' in txt and 'tol_perturb_integration' not in txt and 'dy[' not in txt and 'index_pt_' not in txt;checks['threshold_changed']=False
    passed=all(v is True for q,v in checks.items() if q!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S3B_TRAJECTORY_SAMPLED_CONSTRAINT_RESULT_v1','gate':'C10.65s3b','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'sample_elapsed_tau_Mpc':samples,'record_count':len(records),'records':records,'max_abs_normalized_constraint':maxres,'max_abs_normalized_constraint_change':maxchg,'frozen_bound':lim,'s3a_parent_preserved':s3['classification'],'s2k_parent_preserved':k2['classification'],'threshold_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'At least one preregistered trajectory-sample check failed; preserve the result and diagnose without changing the fixed sample times or 1e-10 bound.','next_gate':t['next_if_pass'] if passed else 'Diagnose s3b before widening time or k domain.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['classification']);print(json.dumps({'checks':checks,'maxres':maxres,'maxchg':maxchg},sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
