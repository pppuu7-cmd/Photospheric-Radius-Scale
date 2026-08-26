#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
mp.mp.dps=90

def load(p): return json.loads((ROOT/p).read_text())
def M(x): return mp.mpf(str(x))
def F(x): return float(x)
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),mp.mpf('1e-80'))
def normres(r,*ts): return abs(r)/max([abs(t) for t in ts]+[mp.mpf('1e-80')])

def affine_intercept(xs,ys,n):
    xs=xs[:n]; ys=ys[:n]; N=M(n); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    den=N*sxx-sx*sx; slope=(N*sxy-sx*sy)/den; return (sy-slope*sx)/N,slope

def closure(*,a,H,R,cb2,tau,dtau,Wg,Wur,Sur,VN,Psi,Db,Dg):
    # Work directly with regular coefficients theta/k^2 and sigma/k^2.
    delta_b=Db+3*Psi; delta_g=Dg+4*Psi
    thp_A=(-H*VN+cb2*delta_b+R*delta_g/4)/(1+R)
    thp_Phi=M(1)
    c=M(16)/45*tau
    s1=c*VN
    pref=1-M(11)/6*dtau
    sec=M(11)/6*tau*c
    sg_A=pref*s1-sec*thp_A
    sg_Phi=-sec*thp_Phi
    Pi_A=M('1.5')*(Wg*sg_A+Wur*Sur)
    Pi_Phi=M('1.5')*Wg*sg_Phi
    den=1+3*a*a*Pi_Phi
    Phi=(Psi-3*a*a*Pi_A)/den
    thp=thp_A+Phi
    sg=sg_A+sg_Phi*Phi
    Pi=M('1.5')*(Wg*sg+Wur*Sur)
    phi_res=normres(Phi-(Psi-3*a*a*Pi),Phi,Psi,3*a*a*Pi)
    pi_res=normres(Pi-(Pi_A+Pi_Phi*Phi),Pi,Pi_A,Pi_Phi*Phi)
    corr=(sg-s1)/max(abs(s1),mp.mpf('1e-80'))
    return {'delta_b':delta_b,'delta_g':delta_g,'theta_over_k2':VN,'theta_prime_over_k2':thp,'sigma_g_first_over_k2':s1,
            'sigma_g_over_k2':sg,'sigma_g_affine_A':sg_A,'sigma_g_affine_Phi':sg_Phi,'sigma_ur_over_k2':Sur,
            'Pi_A':Pi_A,'Pi_Phi':Pi_Phi,'Pi':Pi,'feedback_denominator':den,'PhiN':Phi,'PsiN':Psi,
            'compromise_relative_correction_to_first_shear':corr,'res_phi':phi_res,'res_pi':pi_res}

def main():
    t=load('research/theory_targets/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_TARGET_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    d=load('research/theory_results/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    assert d['classification']=='C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_PASS_SCOPED'
    assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
    assert src['classification']=='C10_PHYSICAL_CLASS_SOURCE_EXPORT_PASS'
    assert src['class_to_c10_map']['Pi_N']=='1.5*rpp_shear_total/k^2'
    anchors=[M(x) for x in f['exact_anchor']['k_Mpc_inv']]
    on={M(r['k_Mpc_inv']):bool(r['predicted_tca_on']) for r in f['tca_domain']['records']}
    assert all(on[k] for k in anchors)
    bg=n['background']; a=M(bg['a']); H=M(bg['H']); Wg=M(4)/3*M(bg['rhog']); Wur=M(4)/3*M(bg['rhour'])
    pack=f['coefficient_pack']; R=M(pack['R']); cb2=M(pack['cb2']); tau=M(pack['tau_c_Mpc']); dtau=M(pack['dtau_c'])
    Sur=M(n['control']['S_ur0']); J=M(n['control']['J_ad0'])
    points=[]; max_phi=mp.mpf('0'); max_pi=mp.mpf('0'); min_den=mp.inf; max_corr=mp.mpf('0'); allpass=True
    for p in n['points']:
        lead=p['leading']; lc=closure(a=a,H=H,R=R,cb2=cb2,tau=tau,dtau=dtau,Wg=Wg,Wur=Wur,Sur=Sur,VN=M(lead['VN']),Psi=M(lead['PsiN']),Db=J,Dg=M(4)/3*J)
        seq=[]
        for rr in p['finite_records']:
            cc=closure(a=a,H=H,R=R,cb2=cb2,tau=tau,dtau=dtau,Wg=Wg,Wur=Wur,Sur=Sur,VN=M(rr['VN']),Psi=M(rr['PsiN']),Db=M(rr['Db']),Dg=M(rr['Dg']))
            cc['k']=M(rr['k']); cc['x']=M(rr['x']); seq.append(cc)
        xs=[q['x'] for q in seq]; fits={}; fok=True
        for name in ('PhiN','sigma_g_over_k2','Pi'):
            i3,s3=affine_intercept(xs,[q[name] for q in seq],3); i4,s4=affine_intercept(xs,[q[name] for q in seq],4)
            er=rel(i4,lc[name]); en=rel(i3,i4); ok=er<=M('1e-5') and en<=M('1e-5'); fok=fok and ok
            fits[name]={'k0_certificate':F(lc[name]),'intercept_smallest3':F(i3),'intercept_all4':F(i4),'slope_all4':F(s4),'relative_to_k0':F(er),'nested_intercept_relative':F(en),'threshold':1e-5,'pass':ok}
        vals=[lc]+seq
        max_phi=max(max_phi,*[q['res_phi'] for q in vals]); max_pi=max(max_pi,*[q['res_pi'] for q in vals]); min_den=min(min_den,*[abs(q['feedback_denominator']) for q in vals]); max_corr=max(max_corr,*[abs(q['compromise_relative_correction_to_first_shear']) for q in vals])
        ok=fok and all(abs(q['feedback_denominator'])>=M('0.9') and q['res_phi']<=M('1e-24') and q['res_pi']<=M('1e-24') for q in vals)
        allpass=allpass and ok
        def conv(q): return {k:F(v) for k,v in q.items()}
        points.append({'lambda_HL':p['lambda_HL'],'M_c_Mpc_inv':p['M_c_Mpc_inv'],'pass':ok,'leading':conv(lc),'finite_records':[conv(q) for q in seq],'fits':fits})
    allpass=allpass and len(points)==9 and min_den>=M('0.9') and max_phi<=M('1e-24') and max_pi<=M('1e-24')
    cls='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED' if allpass else 'C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_FAIL_SCOPED'
    out={'schema':'RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1','gate':'C10.65o','classification':cls,'target':'research/theory_targets/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_TARGET_v1.json',
         'control_status':'CONDITIONAL_HISTORICAL_PHENOMENOLOGICAL_CONTROL_ONLY','source_lock':{'class_upstream_sha':d['pinned_upstream']['sha'],'perturbations_c_sha256':d['audited_source_hashes_sha256']['source/perturbations.c'],'tca':'compromise_CLASS'},
         'background_coefficients':{'a':F(a),'H':F(H),'R':F(R),'cb2':F(cb2),'tau_c':F(tau),'dtau_c':F(dtau),'W_gamma':F(Wg),'W_ur':F(Wur),'S_ur0':F(Sur)},
         'algebraic_closure':{'photon_shear':'source-locked compromise_CLASS in flat Newtonian gauge','Pi_map':'1.5*(W_gamma*sigma_g+W_ur*sigma_ur)/k^2','metric':'Phi_N=Psi_N-3a^2 Pi','solution':'Phi_N=(Psi_N-3a^2 Pi_A)/(1+3a^2 Pi_Phi)'},
         'global_guards':{'min_abs_shear_feedback_denominator':F(min_den),'required_min':0.9,'max_abs_compromise_relative_correction_to_first_shear':F(max_corr)},
         'global_residuals':{'max_Phi_normalized':F(max_phi),'max_Pi_normalized':F(max_pi),'threshold':1e-24},'grid_point_count':len(points),'points':points,
         'derivative_scope_guard':'B_prime, Psi_N_prime, metric_continuity and slip are deliberately not evaluated here; C10.65p must close them by differentiating the algebraic DAE along the local RHS rather than by a new initial datum.',
         'metric_provenance_guard':'No historical CLASS metric potential is consumed. Psi_N comes from C10.65n completed-U1 algebraic seed; Phi_N is reconstructed here from the source-locked radiation anisotropic stress.',
         'next_gate':t['next_if_pass'] if allpass else 'Audit the radiation shear/traceless closure before attempting derivative/slip closure.','non_claims':t['non_claims']}
    (ROOT/'research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'grid_points':len(points),'min_feedback_den':F(min_den),'max_phi_res':F(max_phi),'max_pi_res':F(max_pi),'max_compromise_rel_correction':F(max_corr),'pass':allpass},sort_keys=True))
if __name__=='__main__': main()
