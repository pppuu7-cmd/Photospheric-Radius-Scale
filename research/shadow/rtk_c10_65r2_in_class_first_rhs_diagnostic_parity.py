#!/usr/bin/env python3
from __future__ import annotations
import argparse,glob,hashlib,json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=['c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime','c10_H0_ord_double_prime','c10_deltaH0_ord','c10_delta_mu_total','c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total','c10_W_total','c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
CTRL=['c10_65a_delta_g','c10_65a_theta_g','c10_65a_shear_g','c10_65a_delta_b','c10_65a_theta_b','c10_65a_CLASS_psi_lapse','c10_65a_CLASS_phi_curvature','c10_65a_delta_ur','c10_65a_theta_ur','c10_65a_shear_ur']
COEFF=['c10_65e_R','c10_65e_cb2','c10_65e_dkappa','c10_65e_ddkappa','c10_65e_tau_c','c10_65e_dtau_c','c10_65e_F','c10_65e_F_prime','c10_65e_tca_flag','c10_65e_tau_c_over_tau_h','c10_65e_tau_c_over_tau_k','c10_65e_has_perturbed_recombination']
R0=['c10_65r0_a','c10_65r0_Hc','c10_65r0_rho_b','c10_65r0_rho_g','c10_65r0_rho_ur','c10_65r0_R','c10_65r0_cb2','c10_65r0_dkappa','c10_65r0_ddkappa','c10_65r0_tau_c','c10_65r0_dtau_c','c10_65r0_F','c10_65r0_F_prime','c10_65r0_tca_flag']
R2=['c10_65r2_B_general','c10_65r2_B_prime','c10_65r2_B_prime_actual','c10_65r2_Psi_N_prime','c10_65r2_metric_continuity_shadow','c10_65r2_metric_euler_shadow','c10_65r2_tca_slip_shadow','c10_65r2_theta_b_prime_shadow','c10_65r2_theta_g_prime_shadow','c10_65r2_theta_ur_prime_shadow','c10_65r2_delta_khr_prime_shadow','c10_65r2_theta_khr_prime_shadow','c10_65r2_weighted_slip_cancel']
R1=['c10_65r1_W_khr','c10_65r1_Db','c10_65r1_Dg','c10_65r1_DA','c10_65r1_delta_mu_pref','c10_65r1_Qpref','c10_65r1_psi_pref','c10_65r1_psi_pref_prime','c10_65r1_phi_pref','c10_65r1_B_pref','c10_65r1_B_den','c10_65r1_V_N','c10_65r1_Psi_N','c10_65r1_Phi_N','c10_65r1_sigma_g_over_k2','c10_65r1_shear_feedback_den']
TAIL=BASE+CTRL+COEFF+R0

def load(p): return json.loads((ROOT/p).read_text())
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)
def numeric(path): return [s.strip() for s in Path(path).read_text().splitlines() if s.strip() and not s.lstrip().startswith('#')]
def digest(path): return hashlib.sha256(('\n'.join(numeric(path))+'\n').encode()).hexdigest()
def rows(path,r2=False):
    names=TAIL+(R2+R1 if r2 else R1)
    out=[]
    for s in numeric(path):
        v=[float(x) for x in s.split()]
        if len(v)<len(names): raise RuntimeError(f'row too short {path}: {len(v)} < {len(names)}')
        z=v[-len(names):]; d={n:z[i] for i,n in enumerate(names)}; d['tau']=v[0]; out.append(d)
    return out

def modes(pat,r2=False):
    a=[]
    for f in sorted(glob.glob(pat)):
        rr=rows(f,r2); k=sum(x['c10_k_Mpc_inv'] for x in rr)/len(rr); a.append((k,f,rr,digest(f)))
    return sorted(a)
def point(points,lam,Mc): return min(points,key=lambda p:abs(float(p['lambda_HL'])-lam)+abs(float(p['M_c_Mpc_inv'])-Mc)/max(Mc,1.))
def record(recs,k): return min(recs,key=lambda r:abs(float(r['k'])-k))

def parent_rhs(nr,orr,qr,bg,pack):
    k=float(nr['k']); x=k*k; H=float(bg['H']); R=float(bg['R']); cb2=float(pack['cb2'])
    Psi=float(nr['PsiN']); Phi=float(orr['PhiN']); sg=x*float(orr['sigma_g_over_k2']); sur=x*float(orr['sigma_ur_over_k2'])
    Db=float(nr['Db']); Dg=float(nr['Dg']); Dur=float(nr['Dur']); VN=float(nr['VN']); Vp=float(nr['Vpref']); B=float(nr['B']); psip=float(nr['psip']); phipref=float(nr['phi'])
    thb=x*VN; thg=thb; thur=thb; dk=float(nr['delta_khr_pref']); thk=x*Vp; slip=float(qr['slip'])
    db=Db+3*Psi; dg=Dg+4*Psi; du=Dur+4*Psi
    thbp=(-H*thb+x*(cb2*db+R*(dg/4-sg))+R*slip)/(1+R)+x*Phi
    thgp=-(thbp+H*thb-cb2*x*db)/R+x*(dg/4-sg)+(1+R)/R*x*Phi
    thurp=x*(du/4-sur)+x*Phi
    w=float(bg['w']); ca2=float(qr['khr_ca2']); cs2=float(qr['khr_cs2'])
    dkp=-(1+w)*(thk+x*B-3*psip)-3*H*(ca2-w)*dk
    thkp=-H*(1-3*ca2)*thk+x*(cs2*dk/(1+w)+phipref)
    return {'c10_65r2_B_prime':float(qr['Bprime']),'c10_65r2_Psi_N_prime':float(qr['PsiNprime']),
      'c10_65r2_metric_continuity_shadow':-3*float(qr['PsiNprime']),'c10_65r2_metric_euler_shadow':x*Phi,
      'c10_65r2_tca_slip_shadow':slip,'c10_65r2_theta_b_prime_shadow':thbp,'c10_65r2_theta_g_prime_shadow':thgp,
      'c10_65r2_theta_ur_prime_shadow':thurp,'c10_65r2_delta_khr_prime_shadow':dkp,'c10_65r2_theta_khr_prime_shadow':thkp}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--r1-control-glob',required=True); ap.add_argument('--r2-off-glob',required=True); ap.add_argument('--r2-dir',required=True); ap.add_argument('--manifest',required=True); ap.add_argument('--patch',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=load('research/theory_targets/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_TARGET_v1.json'); n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json'); o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json'); q=load('research/theory_results/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1.json'); f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json'); r1=load('research/theory_results/RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'; assert r1['classification']=='C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_PASS_SCOPED'; assert q['classification']=='C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED'; assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'; assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'; assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
    expected=[float(x) for x in f['exact_anchor']['k_Mpc_inv']]; aon=float(f['exact_anchor']['a_on']); tol=float(t['frozen_checks']['exact_onset_relative_a_tolerance']); th=t['frozen_checks']
    c1=modes(a.r1_control_glob,False); c2=modes(a.r2_off_glob,False); off=[]; off_ok=len(c1)==len(c2)==4
    if off_ok:
      for u,v,k in zip(c1,c2,expected):
        same=u[3]==v[3]; off_ok &= same and rel(u[0],k)<=1e-12 and rel(v[0],k)<=1e-12; off.append({'k':k,'r1_sha256':u[3],'r2_off_sha256':v[3],'identical':same})
    manifest=json.loads(Path(a.manifest).read_text())['points']; assert len(manifest)==9
    op={(str(p['lambda_HL']),str(p['M_c_Mpc_inv'])):p for p in o['points']}; qp={(str(p['lambda_HL']),str(p['M_c_Mpc_inv'])):p for p in q['points']}
    bg={'H':float(n['background']['H']),'R':(4/3)*float(n['background']['rhog'])/float(n['background']['rhob']),'w':float(n['background']['w_khr'])}; pack=f['coefficient_pack']
    max_local=max_parent=max_r1=max_binv=max_cancel=0.; finite=True; exact=True; all_tca=True; points=[]
    comps=['c10_65r2_B_prime','c10_65r2_Psi_N_prime','c10_65r2_metric_continuity_shadow','c10_65r2_metric_euler_shadow','c10_65r2_tca_slip_shadow','c10_65r2_theta_b_prime_shadow','c10_65r2_theta_g_prime_shadow','c10_65r2_theta_ur_prime_shadow','c10_65r2_delta_khr_prime_shadow','c10_65r2_theta_khr_prime_shadow']
    for e in manifest:
      lam=float(e['lambda_HL']); Mc=float(e['M_c_Mpc_inv']); ms=modes(str(Path(a.r2_dir)/(e['prefix']+'*perturbations*')),True); assert len(ms)==4
      np=point(n['points'],lam,Mc); oo=point(o['points'],lam,Mc); qq=point(q['points'],lam,Mc); rec=[]; pmax=0.
      for (km,fn,rr,sha),k in zip(ms,expected):
        z=min(rr,key=lambda x:abs(x['c10_65r0_a']-aon)); erra=abs(z['c10_65r0_a']-aon)/aon; exact &= erra<=tol; all_tca &= z['c10_65r0_tca_flag']<0.5
        nr=record(np['finite_records'],k); orr=record(oo['finite_records'],k); qr=record(qq['records'],k); ex=parent_rhs(nr,orr,qr,bg,pack)
        errs={c:rel(z[c],ex[c]) for c in comps}; loc=max(errs.values()); pmax=max(pmax,loc); max_local=max(max_local,loc); max_parent=max(max_parent,loc)
        e1=rel(z['c10_65r2_B_general'],z['c10_65r1_B_pref']); max_r1=max(max_r1,e1)
        bi=rel(z['c10_65r2_B_prime_actual'],z['c10_65r2_B_prime']); max_binv=max(max_binv,bi); max_cancel=max(max_cancel,abs(z['c10_65r2_weighted_slip_cancel']))
        finite &= all(math.isfinite(z[x]) for x in R2)
        rec.append({'k':k,'relative_a_error':erra,'max_C_vs_independent_parent_reconstruction_relative':loc,'r1_projector_regression_relative':e1,'Bprime_actual_slip_invariance_relative':bi,'weighted_slip_cancel':z['c10_65r2_weighted_slip_cancel'],'C':{c:z[c] for c in R2},'expected':ex})
      points.append({'lambda_HL':lam,'M_c_Mpc_inv':Mc,'max_C_vs_independent_parent_reconstruction_relative':pmax,'records':rec})
    src=Path(a.patch).read_text(); static_no_dy=('dy[' not in src and 'dy [' not in src); static_no_prod=('ppw->metric_continuity=' not in src and 'ppw->metric_euler=' not in src and 'metric_continuity =' not in src and 'metric_euler =' not in src)
    ok=off_ok and exact and all_tca and finite and static_no_dy and static_no_prod and max_r1<=float(th['max_r1_projector_regression_relative']) and max_local<=float(th['max_C_vs_independent_local_rhs_relative']) and max_parent<=float(th['max_C_vs_detached_parent_rhs_relative']) and max_binv<=float(th['max_Bprime_actual_slip_invariance_relative']) and max_cancel<=float(th['max_weighted_photon_baryon_slip_cancel_normalized_residual'])
    cls=t['pass_classification'] if ok else t['fail_classification']
    out={'schema':'RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1','gate':'C10.65r2','classification':cls,'target':'research/theory_targets/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_TARGET_v1.json','grid_point_count':len(points),'anchor_count_per_point':4,'off_path':{'numeric_text_sha256_identical_all_four':off_ok,'records':off},'global_checks':{'exact_onset_all':exact,'all_four_anchors_tca_on':all_tca,'all_outputs_finite':finite,'max_r1_projector_regression_relative':max_r1,'max_C_vs_independent_local_rhs_relative':max_local,'max_C_vs_detached_parent_rhs_relative':max_parent,'max_Bprime_actual_slip_invariance_relative':max_binv,'max_weighted_photon_baryon_slip_cancel_normalized_residual':max_cancel,'no_dy_write_static_guard':static_no_dy,'no_production_metric_or_rhs_write_static_guard':static_no_prod},'thresholds':th,'threshold_changed':False,'points':points,'interpretation':'Diagnostic-only in-CLASS first-RHS parity. No state handoff or production feedback is claimed.'}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(cls,json.dumps(out['global_checks'],sort_keys=True))
    raise SystemExit(0 if ok else 1)
if __name__=='__main__': main()
