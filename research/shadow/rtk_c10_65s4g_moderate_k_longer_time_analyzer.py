#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def obs(path):
 rows=[]; names=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','phi_prime','delta_b_prime','theta_b_prime','delta_g_prime','theta_g_prime','delta_ur_prime','theta_ur_prime','delta_khr_N_prime','theta_khr_N_prime','B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','A_raw','A_norm','H_raw','H_norm','M_raw','M_norm','T_raw','T_norm','feedback_denominator','implicit_denominator']
 for line in Path(path).read_text().splitlines():
  if not line.strip(): continue
  p=line.strip().split(','); assert len(p)==63,len(p); r={'phase':p[0],'tau':float(p[1]),'a':float(p[2]),'k':float(p[3]),'tca':int(p[4]),'rsa':int(p[5]),'ufa':int(p[6]),'lmax':int(p[7]),'rhs_calls':int(p[8]),'_line':line.strip()}; j=9
  for n in names: r[n]=float(p[j]); j+=1
  r['Fl']=[float(x) for x in p[j:]]; rows.append(r)
 return rows
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--manifest',required=True); ap.add_argument('--s4d-observer',required=True); ap.add_argument('--off-identity',required=True); ap.add_argument('--patch',required=True); ap.add_argument('--bridge',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
 t=L('research/theory_targets/RTK_C10_65S4G_MODERATE_K_LONGER_TIME_TRAJECTORY_TARGET_v1.json'); f=L('research/theory_results/RTK_C10_65S4F_MODERATE_K_TIME_WIDENED_TRAJECTORY_RESULT_v1.json'); d=L('research/theory_results/RTK_C10_65S4D_MODERATE_K_ONE_ACCEPTED_STEP_PRODUCTION_CANARY_RESULT_v1.json'); s2e=L('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json')
 assert t['status']=='FROZEN_BEFORE_EXECUTION'; assert f['classification']==t['parents']['C10.65s4f']; assert d['classification']==t['parents']['C10.65s4d']; assert s2e['classification']==t['parents']['C10.65s2e_historical']
 man=json.loads(Path(a.manifest).read_text()); samples=[float(x) for x in t['sample_elapsed_tau_Mpc']]; ks=[float(x) for x in t['domain']['k_Mpc_inv']]; base=sorted([r for r in obs(a.s4d_observer) if r['phase']=='BEFORE'],key=lambda r:r['k']); off=json.loads(Path(a.off_identity).read_text()); checks={'off_identity':off.get('all_two_numeric_rows_sha256_identical') is True,'sample_manifest_shape':len(man)==4 and [float(x['width']) for x in man]==samples}
 lim=float(t['constraint_policy']['max_abs_normalized_momentum']); atol=float(t['sampling_policy']['endpoint_width_absolute_tolerance_Mpc']); records=[]; mx=mc=0.; before=width=fin=approx=confin=within=chgok=True
 state=['phi','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_khr_N','theta_khr_N','B','B_prime','psi_pref','psi_pref_prime','phi_pref','Psi_N','Psi_N_prime','Phi_N','sigma_g','tca_slip','feedback_denominator','implicit_denominator']
 for ent in man:
  w=float(ent['width']); rows=obs(ent['observer']); B=sorted([r for r in rows if r['phase']=='BEFORE'],key=lambda r:r['k']); A=sorted([r for r in rows if r['phase']=='AFTER'],key=lambda r:r['k']); good=len(B)==len(A)==2 and [r['k'] for r in B]==ks and [r['k'] for r in A]==ks; before &= good and len(base)==2 and all(x['_line']==y['_line'] for x,y in zip(B,base))
  for x,y in zip(B,A):
   dw=y['tau']-x['tau']; width &= abs(dw-w)<=atol; fin &= all(math.isfinite(y[n]) for n in state) and all(math.isfinite(v) for v in y['Fl']); approx &= (y['tca'],y['rsa'],y['ufa'],y['lmax'])==(0,0,0,17); rr={}
   for q in ('A','H','M'):
    n=q+'_norm'; confin &= math.isfinite(x[n]) and math.isfinite(y[n]); r=abs(y[n]); cc=abs(y[n]-x[n]); mx=max(mx,r); mc=max(mc,cc); within &= r<=lim; chgok &= cc<=lim; rr[q]={'before':x[n],'after':y[n],'abs_change':cc}
   records.append({'elapsed_tau_Mpc':w,'k':x['k'],'observed_elapsed_tau_Mpc':dw,'rhs_calls_after':y['rhs_calls'],'constraints':rr})
 checks.update({'record_count':len(records)==8,'before_rows_exact_s4d_before_all_samples':before,'all_endpoint_widths_within_absolute_tolerance':width,'all_endpoint_states_finite':fin,'all_endpoint_approximation_states':approx,'all_endpoint_constraints_finite':confin,'all_endpoint_normalized_constraints_within_1e-10':within,'all_normalized_constraint_changes_within_1e-10':chgok})
 ptxt=Path(a.patch).read_text(); bridge=Path(a.bridge).read_text(); checks['same_kernel_and_tolerance_static_guard']='no physics/tolerance mutation' in ptxt and 'tol_perturb_integration' not in ptxt and 'dy[' not in ptxt and 'static const s2seed S[2]' in bridge; checks['moderate_k_seed_only_static_guard']='0.001' in bridge and '0.003' in bridge and '1.0000000000000001e-05' not in bridge; checks['s2e_failed_parent_preserved']=s2e['classification']==t['parents']['C10.65s2e_historical']; checks['threshold_changed']=False
 passed=all(v is True for k,v in checks.items() if k!='threshold_changed') and not checks['threshold_changed']; out={'schema':'RTK_C10_65S4G_MODERATE_K_LONGER_TIME_TRAJECTORY_RESULT_v1','gate':'C10.65s4g','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'sample_elapsed_tau_Mpc':samples,'record_count':len(records),'records':records,'max_abs_normalized_constraint':mx,'max_abs_normalized_constraint_change':mc,'frozen_bound':lim,'threshold_changed':False,'s4f_parent_preserved':f['classification'],'s2e_classification_preserved':s2e['classification'],'interpretation':t['interpretation_if_pass'] if passed else 'Frozen C10.65s4g check failed; diagnose without widening criteria.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s4g before any k-domain widening.','non_claims':t['non_claims']}
 Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n'); print(out['classification']); print(json.dumps({'maxres':mx,'maxchg':mc,'checks':checks},sort_keys=True)); raise SystemExit(0 if passed else 2)
if __name__=='__main__': main()
