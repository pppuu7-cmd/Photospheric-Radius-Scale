#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, hashlib, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=['c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime','c10_H0_ord_double_prime','c10_deltaH0_ord','c10_delta_mu_total','c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total','c10_W_total','c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
CTRL=['c10_65a_delta_g','c10_65a_theta_g','c10_65a_shear_g','c10_65a_delta_b','c10_65a_theta_b','c10_65a_CLASS_psi_lapse','c10_65a_CLASS_phi_curvature','c10_65a_delta_ur','c10_65a_theta_ur','c10_65a_shear_ur']
COEFF=['c10_65e_R','c10_65e_cb2','c10_65e_dkappa','c10_65e_ddkappa','c10_65e_tau_c','c10_65e_dtau_c','c10_65e_F','c10_65e_F_prime','c10_65e_tca_flag','c10_65e_tau_c_over_tau_h','c10_65e_tau_c_over_tau_k','c10_65e_has_perturbed_recombination']
R0=['c10_65r0_a','c10_65r0_Hc','c10_65r0_rho_b','c10_65r0_rho_g','c10_65r0_rho_ur','c10_65r0_R','c10_65r0_cb2','c10_65r0_dkappa','c10_65r0_ddkappa','c10_65r0_tau_c','c10_65r0_dtau_c','c10_65r0_F','c10_65r0_F_prime','c10_65r0_tca_flag']
R1=['c10_65r1_W_khr','c10_65r1_Db','c10_65r1_Dg','c10_65r1_DA','c10_65r1_delta_mu_pref','c10_65r1_Qpref','c10_65r1_psi_pref','c10_65r1_psi_pref_prime','c10_65r1_phi_pref','c10_65r1_B_pref','c10_65r1_B_den','c10_65r1_V_N','c10_65r1_Psi_N','c10_65r1_Phi_N','c10_65r1_sigma_g_over_k2','c10_65r1_shear_feedback_den']
TAIL=BASE+CTRL+COEFF


def load(rel): return json.loads((ROOT/rel).read_text())
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)
def numeric_lines(path): return [x.strip() for x in Path(path).read_text().splitlines() if x.strip() and not x.lstrip().startswith('#')]
def digest(path): return hashlib.sha256(('\n'.join(numeric_lines(path))+'\n').encode()).hexdigest()

def read_rows(path, r0=True, r1=False):
    names=TAIL+(R0 if r0 else [])+(R1 if r1 else [])
    out=[]
    for s in numeric_lines(path):
        vals=[float(x) for x in s.split()]
        if len(vals)<len(names): raise RuntimeError(f'row too short {path}: {len(vals)} < {len(names)}')
        z=vals[-len(names):]
        d={n:z[i] for i,n in enumerate(names)}; d['tau']=vals[0]; d['a_standard']=vals[1]
        out.append(d)
    if len(out)<3: raise RuntimeError(f'too few rows in {path}')
    return out

def read_modes(pattern,r1=False):
    fs=sorted(glob.glob(pattern)); out=[]
    for f in fs:
        rr=read_rows(f,True,r1); k=sum(x['c10_k_Mpc_inv'] for x in rr)/len(rr)
        out.append({'k':k,'file':f,'rows':rr,'sha':digest(f)})
    return sorted(out,key=lambda x:x['k'])

def local_project(r,lam,Mc):
    J=-3.; A2=-1120.906563855608; C2=-1.314425482950032; Sur=298.90841588141416
    a=r['c10_65r0_a']; H=r['c10_65r0_Hc']; rhob=r['c10_65r0_rho_b']; rhog=r['c10_65r0_rho_g']; rhour=r['c10_65r0_rho_ur']
    R=r['c10_65r0_R']; cb2=r['c10_65r0_cb2']; tau=r['c10_65r0_tau_c']; dtau=r['c10_65r0_dtau_c']; Wk=r['c10_65r1_W_khr']; k=r['c10_k_Mpc_inv']
    x=k*k; L=-x; rr=lam-1.; D=3.*lam-1.; Db=J+A2*x; Dg=4./3.*Db
    W0=rhob+4./3.*(rhog+rhour); C0=4./9.*(rhog+rhour); W=W0+Wk
    h=W0*Db; ph=C0*Db; muhat=W*Db
    K=-1.5*a*a/(x+a*a*Mc*Mc); a1=x/(x+a*a*Mc*Mc); Kp=2.*H*a1*K
    W0p=-3.*H*(W0+C0); DA=1.-3.*K*W0; DAp=-3.*(Kp*W0+K*W0p); psi=K*h/DA
    dm=muhat+3.*W*psi; Q=(C2*x-3.*a*a*dm)/(3.*H); qpref=Q/(3.*a); q0pref=(W0/W)*qpref
    hpA=-3.*H*(h+ph)-(x/a)*q0pref; hpB=-x*W0
    psipA=(Kp*h+K*hpA-DAp*psi)/DA; psipB=K*hpB/DA
    lapse=rr*2.*L-2.*D*H*H
    phiA=(-3.*a*a*rr*dm-D*H*Q+2.*D*H*psipA+2.*rr*L*psi)/lapse
    phiB=(2.*D*H*psipB)/lapse; shift=rr*L; Bden=shift+D*(psipB+H*phiB); Brhs=Q-D*(psipA+H*phiA); B=Brhs/Bden
    psip=psipA+psipB*B; phi=phiA+phiB*B; Vpref=qpref/(a*W); VN=Vpref+B; Psi=psi-H*B
    Wg=4./3.*rhog; Wur=4./3.*rhour; db=Db+3.*Psi; dg=Dg+4.*Psi
    thpA=(-H*VN+cb2*db+R*dg/4.)/(1.+R); c=16./45.*tau; s1=c*VN; pref=1.-11./6.*dtau; sec=11./6.*tau*c
    sgA=pref*s1-sec*thpA; sgPhi=-sec; PiA=1.5*(Wg*sgA+Wur*Sur); PiPhi=1.5*Wg*sgPhi; feedback=1.+3.*a*a*PiPhi
    Phi=(Psi-3.*a*a*PiA)/feedback; sg=sgA+sgPhi*Phi
    return {'c10_65r1_W_khr':Wk,'c10_65r1_Db':Db,'c10_65r1_Dg':Dg,'c10_65r1_DA':DA,'c10_65r1_delta_mu_pref':dm,'c10_65r1_Qpref':Q,'c10_65r1_psi_pref':psi,'c10_65r1_psi_pref_prime':psip,'c10_65r1_phi_pref':phi,'c10_65r1_B_pref':B,'c10_65r1_B_den':Bden,'c10_65r1_V_N':VN,'c10_65r1_Psi_N':Psi,'c10_65r1_Phi_N':Phi,'c10_65r1_sigma_g_over_k2':sg,'c10_65r1_shear_feedback_den':feedback}

def match_point(points,lam,Mc):
    return min(points,key=lambda p:abs(float(p['lambda_HL'])-lam)+abs(float(p['M_c_Mpc_inv'])-Mc)/max(Mc,1.))

def match_record(records,k): return min(records,key=lambda r:abs(float(r['k'])-k))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--r0-control-glob',required=True); ap.add_argument('--r1-off-glob',required=True); ap.add_argument('--r1-dir',required=True); ap.add_argument('--manifest',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=load('research/theory_targets/RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_TARGET_v1.json'); r0=load('research/theory_results/RTK_C10_65R0_OPT_IN_CLASS_LOCAL_ENVIRONMENT_EXPORT_RESULT_v1.json'); n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json'); o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'; assert r0['classification']=='C10_65R0_OPT_IN_CLASS_LOCAL_ENVIRONMENT_EXPORT_PASS_SCOPED'; assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'; assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'
    expected=[1e-5,3e-5,1e-4,3e-4]; base=read_modes(a.r0_control_glob,False); off=read_modes(a.r1_off_glob,False)
    if len(base)!=4 or len(off)!=4: raise RuntimeError('r0 control/r1 off must each have four modes')
    off_exact=True; off_records=[]
    for b,z,k in zip(base,off,expected):
        if rel(b['k'],k)>1e-12 or rel(z['k'],k)>1e-12: raise RuntimeError('off-path k mismatch')
        same=b['sha']==z['sha']; off_exact=off_exact and same; off_records.append({'k_Mpc_inv':k,'r0_sha256':b['sha'],'r1_off_sha256':z['sha'],'identical':same})
    manifest=json.loads(Path(a.manifest).read_text()); entries=manifest['points']
    if len(entries)!=9: raise RuntimeError(f'expected 9 grid points, got {len(entries)}')
    a_on=float(t['parents'] and r0['on_path']['onset_records'][0]['c10_65r0_a']); tol_a=float(t['frozen_checks']['exact_onset_relative_a_tolerance'])
    max_local=0.; max_parent=0.; max_wk=0.; min_DA=float('inf'); min_Bden=float('inf'); min_fb=float('inf'); all_finite=True; exact_all=True; points=[]
    map_n={'c10_65r1_Db':'Db','c10_65r1_Dg':'Dg','c10_65r1_DA':'DA','c10_65r1_delta_mu_pref':'delta_mu_pref','c10_65r1_Qpref':'Qpref','c10_65r1_psi_pref':'psi','c10_65r1_psi_pref_prime':'psip','c10_65r1_phi_pref':'phi','c10_65r1_B_pref':'B','c10_65r1_B_den':'Bden','c10_65r1_V_N':'VN','c10_65r1_Psi_N':'PsiN'}
    map_o={'c10_65r1_Phi_N':'PhiN','c10_65r1_sigma_g_over_k2':'sigma_g_over_k2','c10_65r1_shear_feedback_den':'feedback_denominator'}
    for e in entries:
        lam=float(e['lambda_HL']); Mc=float(e['M_c_Mpc_inv']); prefix=e['prefix']; ms=read_modes(str(Path(a.r1_dir)/(prefix+'*perturbations*')),True)
        if len(ms)!=4: raise RuntimeError(f'{prefix}: expected four histories, got {len(ms)}')
        np=match_point(n['points'],lam,Mc); op=match_point(o['points'],lam,Mc); recs=[]; pmaxloc=0.; pmaxpar=0.
        for m,k in zip(ms,expected):
            if rel(m['k'],k)>1e-12: raise RuntimeError(f'{prefix}: k mismatch')
            z=min(m['rows'],key=lambda r:abs(r['c10_65r0_a']-a_on)); ra=abs(z['c10_65r0_a']-a_on)/a_on; exact_all=exact_all and ra<=tol_a
            py=local_project(z,lam,Mc); errs={}
            for key in R1:
                er=rel(z[key],py[key]); errs[key]=er; pmaxloc=max(pmaxloc,er); max_local=max(max_local,er)
            nr=match_record(np['finite_records'],k); orr=match_record(op['finite_records'],k); perrs={}
            for ck,nk in map_n.items():
                er=rel(z[ck],float(nr[nk])); perrs[ck]=er; pmaxpar=max(pmaxpar,er); max_parent=max(max_parent,er)
            for ck,okey in map_o.items():
                er=rel(z[ck],float(orr[okey])); perrs[ck]=er; pmaxpar=max(pmaxpar,er); max_parent=max(max_parent,er)
            ew=rel(z['c10_65r1_W_khr'],float(n['background']['W_khr'])); max_wk=max(max_wk,ew)
            min_DA=min(min_DA,z['c10_65r1_DA']); min_Bden=min(min_Bden,abs(z['c10_65r1_B_den'])); min_fb=min(min_fb,abs(z['c10_65r1_shear_feedback_den']))
            all_finite=all_finite and all(math.isfinite(z[q]) for q in R1)
            recs.append({'k_Mpc_inv':k,'relative_a_error':ra,'max_C_vs_local_python_relative':max(errs.values()),'max_C_vs_detached_parent_relative':max(perrs.values()),'W_khr_relative_to_detached':ew,'C_outputs':{q:z[q] for q in R1}})
        points.append({'prefix':prefix,'lambda_HL':lam,'M_c_Mpc_inv':Mc,'max_C_vs_local_python_relative':pmaxloc,'max_C_vs_detached_parent_relative':pmaxpar,'records':recs})
    th=t['frozen_checks']; ok=(off_exact and exact_all and all_finite and max_local<=float(th['max_C_vs_local_python_relative']) and max_parent<=float(th['max_C_vs_detached_parent_relative']) and max_wk<=float(th['max_W_khr_relative_to_detached_background']) and min_DA>1. and min_Bden>0. and min_fb>=float(th['radiation_shear_feedback_abs_denominator_min']))
    cls=t['pass_classification'] if ok else t['fail_classification']
    out={'schema':'RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_RESULT_v1','gate':'C10.65r1','classification':cls,'target':'research/theory_targets/RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_TARGET_v1.json','off_path':{'numeric_text_sha256_identical_all_four':off_exact,'records':off_records},'grid_point_count':len(points),'anchor_count_per_point':4,'global_checks':{'exact_onset_all':exact_all,'all_outputs_finite':all_finite,'max_C_vs_local_python_relative':max_local,'threshold_local':float(th['max_C_vs_local_python_relative']),'max_C_vs_detached_parent_relative':max_parent,'threshold_detached':float(th['max_C_vs_detached_parent_relative']),'max_W_khr_relative_to_detached_background':max_wk,'threshold_W_khr':float(th['max_W_khr_relative_to_detached_background']),'min_DA':min_DA,'min_abs_B_linear_denominator':min_Bden,'min_abs_radiation_shear_feedback_denominator':min_fb},'points':points,'metric_provenance_guard':'The local Python reconstruction consumes only C10.65r0 environment columns, diagnostic completion inputs, the C-exported Khronon enthalpy and frozen C10.65m matching constants. Standard CLASS psi/phi columns are parsed only as part of the inherited tail layout and are never consumed by the parity calculation.','interpretation':t['interpretation_if_pass'] if ok else 'C10.65r1 failed a frozen C/local-Python or detached-parent parity guard; do not proceed to RHS parity.','next_gate':t['next_if_pass'] if ok else 'diagnose C10.65r1 without weakening frozen thresholds','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(cls,json.dumps({'off_exact':off_exact,'max_local':max_local,'max_parent':max_parent,'max_Wk':max_wk,'min_DA':min_DA,'min_Bden':min_Bden,'min_feedback':min_fb,'exact_onset':exact_all},sort_keys=True))
    if not ok: raise SystemExit(2)
if __name__=='__main__': main()
