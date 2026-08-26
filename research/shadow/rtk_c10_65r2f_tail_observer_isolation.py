#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, hashlib, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
R1=['c10_65r1_W_khr','c10_65r1_Db','c10_65r1_Dg','c10_65r1_DA','c10_65r1_delta_mu_pref','c10_65r1_Qpref','c10_65r1_psi_pref','c10_65r1_psi_pref_prime','c10_65r1_phi_pref','c10_65r1_B_pref','c10_65r1_B_den','c10_65r1_V_N','c10_65r1_Psi_N','c10_65r1_Phi_N','c10_65r1_sigma_g_over_k2','c10_65r1_shear_feedback_den']
R2=['c10_65r2_B_general','c10_65r2_B_prime','c10_65r2_B_prime_actual','c10_65r2_Psi_N_prime','c10_65r2_metric_continuity_shadow','c10_65r2_metric_euler_shadow','c10_65r2_tca_slip_shadow','c10_65r2_theta_b_prime_shadow','c10_65r2_theta_g_prime_shadow','c10_65r2_theta_ur_prime_shadow','c10_65r2_delta_khr_prime_shadow','c10_65r2_theta_khr_prime_shadow','c10_65r2_weighted_slip_cancel']

def load(p): return json.loads((ROOT/p).read_text())
def numeric(p): return [s.strip() for s in Path(p).read_text().splitlines() if s.strip() and not s.lstrip().startswith('#')]
def digest(p): return hashlib.sha256(('\n'.join(numeric(p))+'\n').encode()).hexdigest()
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)

def modes(pat):
    out=[]
    for f in sorted(glob.glob(pat)):
        rr=[]
        for s in numeric(f):
            v=[float(x) for x in s.split()]
            rr.append((v[0],v[1],v))
        out.append((f,rr,digest(f)))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--control-glob',required=True); ap.add_argument('--off-glob',required=True); ap.add_argument('--on-glob',required=True)
    ap.add_argument('--base-patch',required=True); ap.add_argument('--isolation-patch',required=True); ap.add_argument('--output',required=True)
    a=ap.parse_args()
    t=load('research/theory_targets/RTK_C10_65R2F_TAIL_OBSERVER_CODEGEN_ISOLATION_TARGET_v1.json')
    old=load('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_FAIL_RUN2_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    aon=float(f['exact_anchor']['a_on']); ks=[float(x) for x in f['exact_anchor']['k_Mpc_inv']]
    c=modes(a.control_glob); o=modes(a.off_glob); n=modes(a.on_glob)
    assert len(c)==len(o)==len(n)==4
    off=[]; exact=True
    for (cf,cr,ch),(of,orr,oh),k in zip(c,o,ks):
        same=ch==oh; exact &= same
        off.append({'k':k,'control':cf,'off':of,'control_sha256':ch,'off_sha256':oh,'identical':same})
    oldp=old['points'][0]; oldrecs=oldp['records']
    max_prev=0.; max_r1=0.; finite=True; exact_on=True; onrecs=[]
    tail=R1+R2
    for (nf,rr,nh),k,prev in zip(n,ks,oldrecs):
        tau,av,v=min(rr,key=lambda z:abs(z[1]-aon)); ea=abs(av-aon)/aon; exact_on &= ea<=1e-12
        if len(v)<len(tail): raise RuntimeError('tail too short')
        z={name:v[-len(tail)+j] for j,name in enumerate(tail)}
        errs={name:rel(z[name],float(prev['C'][name])) for name in R2}
        mp=max(errs.values()); max_prev=max(max_prev,mp)
        br=rel(z['c10_65r2_B_general'],z['c10_65r1_B_pref']); max_r1=max(max_r1,br)
        finite &= all(math.isfinite(z[name]) for name in tail)
        onrecs.append({'k':k,'relative_a_error':ea,'max_r2_vs_previous_scientific_parity_relative':mp,'r1_projector_regression_relative':br,'r2':{x:z[x] for x in R2}})
    base=Path(a.base_patch).read_text(); iso=Path(a.isolation_patch).read_text()
    no_dy=('dy[' not in base and 'dy [' not in base and 'dy[' not in iso and 'dy [' not in iso)
    no_prod=('metric_continuity =' not in base and 'metric_euler =' not in base and 'ppw->metric_continuity=' not in base and 'ppw->metric_euler=' not in base)
    checks=t['frozen_checks']
    ok=(exact and exact_on and finite and max_prev<=float(checks['on_path_r2_vs_previous_scientific_parity_relative'])
        and max_r1<=float(checks['on_path_r1_projector_regression_relative']) and no_dy and no_prod)
    cls=t['pass_classification'] if ok else t['fail_classification']
    out={'schema':'RTK_C10_65R2F_TAIL_OBSERVER_CODEGEN_ISOLATION_RESULT_v1','gate':'C10.65r2f','classification':cls,
         'target':'research/theory_targets/RTK_C10_65R2F_TAIL_OBSERVER_CODEGEN_ISOLATION_TARGET_v1.json',
         'off_path':{'numeric_text_exact_identity_all_four':exact,'max_relative_difference':0.0 if exact else None,'records':off},
         'on_path':{'exact_onset_all':exact_on,'all_finite':finite,'max_r1_projector_regression_relative':max_r1,'max_r2_vs_previous_scientific_parity_relative':max_prev,'records':onrecs},
         'static_guards':{'no_dy_write':no_dy,'no_production_metric_or_rhs_write':no_prod},
         'threshold_changed':False,'implementation':'existing r2 arithmetic relocated after final r1 store; old title-order patch omitted; shear-unit fix retained',
         'next':t['next_if_pass'] if ok else t['next_if_fail'],'non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'off_exact':exact,'max_r1':max_r1,'max_r2_previous':max_prev},sort_keys=True))
    raise SystemExit(0 if ok else 1)
if __name__=='__main__': main()
