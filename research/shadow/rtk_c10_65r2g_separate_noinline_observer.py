#!/usr/bin/env python3
from __future__ import annotations
import argparse,glob,hashlib,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
R1=['c10_65r1_W_khr','c10_65r1_Db','c10_65r1_Dg','c10_65r1_DA','c10_65r1_delta_mu_pref','c10_65r1_Qpref','c10_65r1_psi_pref','c10_65r1_psi_pref_prime','c10_65r1_phi_pref','c10_65r1_B_pref','c10_65r1_B_den','c10_65r1_V_N','c10_65r1_Psi_N','c10_65r1_Phi_N','c10_65r1_sigma_g_over_k2','c10_65r1_shear_feedback_den']
R2=['c10_65r2_B_general','c10_65r2_B_prime','c10_65r2_B_prime_actual','c10_65r2_Psi_N_prime','c10_65r2_metric_continuity_shadow','c10_65r2_metric_euler_shadow','c10_65r2_tca_slip_shadow','c10_65r2_theta_b_prime_shadow','c10_65r2_theta_g_prime_shadow','c10_65r2_theta_ur_prime_shadow','c10_65r2_delta_khr_prime_shadow','c10_65r2_theta_khr_prime_shadow','c10_65r2_weighted_slip_cancel']
def L(p): return json.loads((ROOT/p).read_text())
def lines(p): return [s.strip() for s in Path(p).read_text().splitlines() if s.strip() and not s.lstrip().startswith('#')]
def sha(p): return hashlib.sha256(('\n'.join(lines(p))+'\n').encode()).hexdigest()
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)
def files(pat):
 out=[]
 for p in sorted(glob.glob(pat)):
  rr=[]
  for s in lines(p):
   v=[float(x) for x in s.split()]; rr.append((v[0],v[1],v))
  out.append((p,rr,sha(p)))
 return out
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--control-glob',required=True); ap.add_argument('--off-glob',required=True); ap.add_argument('--on-glob',required=True); ap.add_argument('--core-patch',required=True); ap.add_argument('--observer-c',required=True); ap.add_argument('--observer-h',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
 t=L('research/theory_targets/RTK_C10_65R2G_SEPARATE_NOINLINE_OBSERVER_TARGET_v1.json'); old=L('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_FAIL_RUN2_v1.json'); f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
 assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'; aon=float(f['exact_anchor']['a_on']); ks=[float(x) for x in f['exact_anchor']['k_Mpc_inv']]
 c,o,n=files(a.control_glob),files(a.off_glob),files(a.on_glob); assert len(c)==len(o)==len(n)==4
 off=[]; exact=True
 for (cf,cr,ch),(of,orr,oh),k in zip(c,o,ks):
  same=(ch==oh); exact &= same
  off.append({'k':k,'control_sha256':ch,'off_sha256':oh,'identical':same,'same_numeric_row_count':len(cr)==len(orr)})
 prev=old['points'][0]['records']; maxprev=0.; maxr1=0.; maxcancel=0.; finite=True; exacton=True; rec=[]
 tail=R1+R2
 for (nf,rr,nh),k,pv in zip(n,ks,prev):
  tau,av,v=min(rr,key=lambda z:abs(z[1]-aon)); erra=abs(av-aon)/aon; exacton &= erra<=float(t['frozen_checks']['on_path_exact_onset_relative_tolerance'])
  if len(v)<len(tail): raise RuntimeError('ON row shorter than r1+r2 tail')
  z={name:v[-len(tail)+j] for j,name in enumerate(tail)}
  errs={name:rel(z[name],float(pv['C'][name])) for name in R2}; mp=max(errs.values()); maxprev=max(maxprev,mp)
  er1=rel(z['c10_65r2_B_general'],z['c10_65r1_B_pref']); maxr1=max(maxr1,er1)
  maxcancel=max(maxcancel,abs(z['c10_65r2_weighted_slip_cancel']))
  finite &= all(math.isfinite(z[x]) for x in tail)
  rec.append({'k':k,'relative_a_error':erra,'max_r2_vs_previous_relative':mp,'r1_B_regression_relative':er1,'weighted_slip_cancel':z['c10_65r2_weighted_slip_cancel']})
 core=Path(a.core_patch).read_text(); oc=Path(a.observer_c).read_text(); oh=Path(a.observer_h).read_text()
 caller_line='rtk_c10_65r2_observe(pba,pth,ppw,k,dataptr,&storeidx);'
 caller_no_r1=(caller_line in core and 'r1_' not in caller_line)
 no_dy=('dy[' not in core and 'dy [' not in core and 'dy[' not in oc and 'dy [' not in oc)
 no_prod=('metric_continuity =' not in core and 'metric_euler =' not in core and 'ppw->metric_continuity=' not in core and 'ppw->metric_euler=' not in core)
 sep=('rtk_c10_65r2_observer.o' in core and 'rtk_c10_65r2_general_B' in oc and 'rtk_c10_65r2_general_B' not in core)
 noin=('__attribute__((noinline,noclone))' in oc)
 th=t['frozen_checks']
 ok=(exact and exacton and finite and maxr1<=float(th['on_path_r1_projector_regression_relative']) and maxprev<=float(th['on_path_r2_vs_previous_scientific_parity_relative']) and maxcancel<=float(th['on_path_weighted_slip_cancel_normalized']) and caller_no_r1 and no_dy and no_prod and sep and noin)
 cls=t['pass_classification'] if ok else t['fail_classification']
 out={'schema':'RTK_C10_65R2G_SEPARATE_NOINLINE_OBSERVER_RESULT_v1','gate':'C10.65r2g','classification':cls,'target':'research/theory_targets/RTK_C10_65R2G_SEPARATE_NOINLINE_OBSERVER_TARGET_v1.json','off_path':{'exact_numeric_text_identity_all_four':exact,'max_relative_difference':0.0 if exact else None,'records':off},'on_path':{'exact_onset_all':exacton,'all_finite':finite,'max_r1_projector_regression_relative':maxr1,'max_r2_vs_previous_scientific_parity_relative':maxprev,'max_weighted_slip_cancel_normalized':maxcancel,'records':rec},'static_guards':{'caller_does_not_reference_r1_temporaries':caller_no_r1,'no_dy_write':no_dy,'no_production_metric_or_rhs_write':no_prod,'observer_is_separate_object':sep,'observer_entry_noinline_noclone':noin},'threshold_changed':False,'next':t['next_if_pass'] if ok else t['next_if_fail'],'non_claims':t['non_claims']}
 Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(cls,json.dumps({'off_exact':exact,'max_r1':maxr1,'max_r2_previous':maxprev,'max_cancel':maxcancel},sort_keys=True))
if __name__=='__main__': main()
