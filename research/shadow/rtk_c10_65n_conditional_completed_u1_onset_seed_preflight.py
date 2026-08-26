#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
mp.mp.dps=90

def load(rel): return json.loads((ROOT/rel).read_text())
def M(x): return mp.mpf(str(x))
def F(x): return float(x)
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),mp.mpf('1e-80'))
def normres(r,*terms): return abs(r)/max([abs(t) for t in terms]+[mp.mpf('1e-80')])

def affine_intercept(xs,ys,n):
    xs=xs[:n]; ys=ys[:n]; nn=mp.mpf(n)
    sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    den=nn*sxx-sx*sx
    slope=(nn*sxy-sx*sy)/den
    intercept=(sy-slope*sx)/nn
    return intercept,slope

def khr_background(prod,gamma,a):
    c=M('299792.458'); H0=M(100)*M(prod['h'])/c
    lamD=M(prod['lam']); Om=M(prod['Om'])
    mu=M(3)*H0*mp.sqrt(gamma); A=Om/(M(6)*gamma)
    root=mp.sqrt(1+2*A+lamD*A*A)
    x0=A*(2+lamD*A)/(1+lamD*A+root)
    x=x0/(a**3); s=mp.sqrt(1+lamD*x*x); rr=x/s; tt=x/(s+1)
    rho=(2*mu*mu*x*(1+tt))/3; p=(2*mu*mu*rr*tt)/3
    return {'H0':H0,'rho':rho,'p':p,'w':p/rho,'W':rho+p,'x0':x0}

def background(prod,gamma,f65):
    a=M(f65['exact_anchor']['a_on']); H=M(f65['coefficient_pack']['Hc_Mpc_inv']); R=M(f65['coefficient_pack']['R'])
    kh=khr_background(prod,gamma,a); H0=kh['H0']
    rhob=H0*H0*M(prod['Ob'])/(a**3); rhog=M('0.75')*R*rhob
    ur_ratio=M('3.046')*M(7)/M(8)*(M(4)/M(11))**(M(4)/M(3)); rhour=ur_ratio*rhog
    W0=rhob+M(4)/M(3)*(rhog+rhour); C0=M(4)/M(9)*(rhog+rhour); W=W0+kh['W']
    return {'a':a,'H':H,'rhob':rhob,'rhog':rhog,'rhour':rhour,'W0':W0,'C0':C0,'W':W,
            'rho_khr':kh['rho'],'p_khr':kh['p'],'w_khr':kh['w'],'W_khr':kh['W'],'ur_ratio':ur_ratio}

def leading_seed(bg,lam,Mc,J,C2,Eth,Pcal):
    a,H,W0,C0,W=bg['a'],bg['H'],bg['W0'],bg['C0'],bg['W']; r=lam-1; D=3*lam-1
    K=-M(3)/(2*Mc*Mc); DA=1-3*K*W0; h=W0*J; ph=C0*J
    psi=K*h/DA; W0p=-3*H*(W0+C0); DAp=-3*K*W0p; hp=-3*H*(h+ph)
    psip=(K*hp-DAp*psi)/DA; muhat=W*J; dm=muhat+3*W*psi; Q=-(a*a*dm)/H
    lapse=-2*D*H*H; rhs=-3*a*a*r*dm-D*H*Q+2*D*H*psip; phi=rhs/lapse
    B=(C2+2*Pcal*psi-Eth*phi)/(2*H); Vpref=(Q/(3*a))/(a*W); VN=Vpref+B
    delta_khr=(1+bg['w_khr'])*(J+3*psi)
    res={
      'A':normres(DA*psi-K*h,DA*psi,K*h),
      'comoving':normres(a*a*dm+H*Q,a*a*dm,H*Q),
      'Hamiltonian':normres(lapse*phi-rhs,lapse*phi,rhs),
      'B_matching':normres(2*H*B-(C2+2*Pcal*psi-Eth*phi),2*H*B,C2,2*Pcal*psi,Eth*phi),
      'neutral_common_curvature':normres(delta_khr/(1+bg['w_khr'])-3*psi-J,delta_khr/(1+bg['w_khr']),3*psi,J)
    }
    return {'K':K,'DA':DA,'psi':psi,'psip':psip,'muhat':muhat,'delta_mu_pref':dm,'Qpref':Q,'phi':phi,'B':B,
            'Vpref':Vpref,'VN':VN,'PsiN':psi-H*B,'delta_khr_pref':delta_khr,'lapse':lapse,'res':res}

def finite_seed(bg,lam,Mc,k,J,A2,C2,Eth,Pcal):
    a,H,W0,C0,W=bg['a'],bg['H'],bg['W0'],bg['C0'],bg['W']; x=k*k; L=-x; r=lam-1; D=3*lam-1
    Db=J+A2*x; Dg=M(4)/3*Db; Dur=M(4)/3*Db; Jk=Db
    h=W0*Db; ph=C0*Db; muhat=W*Db
    K=-M('1.5')*a*a/(x+a*a*Mc*Mc); a1=x/(x+a*a*Mc*Mc); Kp=2*H*a1*K
    W0p=-3*H*(W0+C0); DA=1-3*K*W0; DAp=-3*(Kp*W0+K*W0p); psi=K*h/DA
    dm=muhat+3*W*psi; Ctarget=C2*x; Q=(Ctarget-3*a*a*dm)/(3*H); qpref=Q/(3*a); q0pref=(W0/W)*qpref
    hpA=-3*H*(h+ph)-(x/a)*q0pref; hpB=-x*W0
    psipA=(Kp*h+K*hpA-DAp*psi)/DA; psipB=K*hpB/DA
    lapse=r*Eth*L-2*D*H*H
    phiA=(-3*a*a*r*dm-D*H*Q+2*D*H*psipA+2*r*Pcal*L*psi)/lapse
    phiB=(2*D*H*psipB)/lapse
    shift=r*L; Bden=shift+D*(psipB+H*phiB); Brhs=Q-D*(psipA+H*phiA); B=Brhs/Bden
    psip=psipA+psipB*B; phi=phiA+phiB*B; hp=hpA+hpB*B
    Vpref=qpref/(a*W); VN=Vpref+B; q0N=q0pref+a*W0*B
    delta_khr=(1+bg['w_khr'])*(Jk+3*psi)
    hpres=-3*H*(h+ph)-(x/a)*q0N
    Hrhs=-3*a*a*r*dm-D*H*Q+2*D*H*psip+2*r*Pcal*L*psi
    Mbr=Q-D*(psip+H*phi)
    res={
      'A':normres(DA*psi-K*h,DA*psi,K*h),
      'dA':normres(DA*psip+DAp*psi-Kp*h-K*hp,DA*psip,DAp*psi,Kp*h,K*hp),
      'hprime_partition':normres(hp-hpres,hp,hpres),
      'Hamiltonian':normres(lapse*phi-Hrhs,lapse*phi,Hrhs),
      'momentum':normres(shift*B-Mbr,shift*B,Mbr),
      'C':normres(3*a*a*dm+3*H*Q-Ctarget,3*a*a*dm,3*H*Q,Ctarget),
      'neutral_common_curvature':normres(delta_khr/(1+bg['w_khr'])-3*psi-Db,delta_khr/(1+bg['w_khr']),3*psi,Db)
    }
    return {'k':k,'x':x,'Db':Db,'Dg':Dg,'Dur':Dur,'Jkhr':Jk,'K':K,'DA':DA,'a1':a1,'psi':psi,'psip':psip,
            'delta_mu_pref':dm,'Qpref':Q,'phi':phi,'B':B,'Bden':Bden,'Vpref':Vpref,'VN':VN,'PsiN':psi-H*B,
            'delta_khr_pref':delta_khr,'lapse':lapse,'shift':shift,'res':res}

def main():
    t=load('research/theory_targets/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_TARGET_v1.json')
    m=load('research/theory_results/RTK_C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_RESULT_v1.json')
    l=load('research/theory_results/RTK_C10_65L_UV_MATCHING_INTERFACE_BASIS_RESULT_v1.json')
    c=load('research/theory_results/RTK_C10_CURVATURE_DRESSED_ORDINARY_DAE_CLOSURE_RESULT_v1.json')
    p=load('research/theory_results/RTK_C10_PREFERRED_METRIC_PROJECTOR_API_RESULT_v1.json')
    proto=load('research/theory_results/RTK_C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json'); state=load('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'; assert m['classification']=='C10_65M_HISTORICAL_CONTROL_MATCHING_VALUES_PASS_SCOPED'
    assert l['classification']=='C10_65L_UV_MATCHING_INTERFACE_BASIS_PASS_SCOPED'; assert c['classification']=='C10_CURVATURE_DRESSED_ORDINARY_DAE_CLOSURE_PASS_POLE_FREE_SCOPED'
    assert p['classification']=='C10_PREFERRED_METRIC_PROJECTOR_API_PASS_SCOPED'; assert proto['classification']=='C10_DIAGNOSTIC_COMPLETION_ONSET_PROTOCOL_PASS_SCOPED'
    assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'; assert src['classification']=='C10_PHYSICAL_CLASS_SOURCE_EXPORT_PASS'
    ctl=m['phenomenological_regular_control_vector']; J=M(-3); A2=M(ctl['A2']); C2=M(ctl['C2']); Sur=M(ctl['S_ur0']); Eth=M(2); Pcal=M(1)
    prod=state['final_replay_result']['rtk']['params']; gamma=M(src['provenance']['gamma_root']); bg=background(prod,gamma,f)
    assert bg['W']>0 and 1+bg['w_khr']>0
    ks=[M(x) for x in f['exact_anchor']['k_Mpc_inv']]
    points=[]; seen=set(); maxres=mp.mpf('0'); max_lead=mp.mpf('0'); pass_all=True
    min_DA=mp.inf; min_lapse=mp.inf; min_Bden=mp.inf
    for q in proto['points']:
        key=(str(q['lambda_HL']),str(q['M_c_Mpc_inv']))
        if key in seen: continue
        seen.add(key); lam=M(q['lambda_HL']); Mc=M(q['M_c_Mpc_inv'])
        lead=leading_seed(bg,lam,Mc,J,C2,Eth,Pcal); max_lead=max(max_lead,*lead['res'].values())
        seq=[finite_seed(bg,lam,Mc,k,J,A2,C2,Eth,Pcal) for k in ks]
        maxres=max(maxres,*[v for s in seq for v in s['res'].values()])
        min_DA=min(min_DA,*[s['DA'] for s in seq],lead['DA']); min_lapse=min(min_lapse,*[abs(s['lapse']) for s in seq],abs(lead['lapse'])); min_Bden=min(min_Bden,*[abs(s['Bden']) for s in seq])
        xs=[s['x'] for s in seq]; fits={}; fit_ok=True
        for name,tol in [('psi',M('1e-5')),('psip',M('1e-5')),('phi',M('1e-5')),('B',M('1e-3'))]:
            i3,s3=affine_intercept(xs,[s[name] for s in seq],3); i4,s4=affine_intercept(xs,[s[name] for s in seq],4); ref=lead[name]
            e_ref=rel(i4,ref); e_nested=rel(i3,i4); ok=e_ref<=tol and e_nested<=tol; fit_ok=fit_ok and ok
            fits[name]={'k0_certificate':F(ref),'intercept_smallest3':F(i3),'intercept_all4':F(i4),'slope_all4':F(s4),'relative_to_k0':F(e_ref),'nested_intercept_relative':F(e_nested),'threshold':F(tol),'pass':ok}
        guards=lead['DA']>1 and all(s['DA']>1 and s['lapse']!=0 and s['Bden']!=0 for s in seq)
        residual_ok=max(lead['res'].values())<=M('1e-24') and max(v for s in seq for v in s['res'].values())<=M('1e-24')
        ok=guards and residual_ok and fit_ok; pass_all=pass_all and ok
        points.append({'lambda_HL':F(lam),'M_c_Mpc_inv':F(Mc),'pass':ok,'leading':{k:F(v) for k,v in lead.items() if k not in ('res',)},'leading_residuals':{k:F(v) for k,v in lead['res'].items()},'finite_records':[{**{k:F(v) for k,v in s.items() if k not in ('res',)},'residuals':{k:F(v) for k,v in s['res'].items()}} for s in seq],'fits':fits})
    assert len(points)==9
    pass_all=pass_all and maxres<=M('1e-24') and max_lead<=M('1e-24') and min_DA>1 and min_lapse>0 and min_Bden>0
    cls='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED' if pass_all else 'C10_65N_CONDITIONAL_ONSET_SEED_PREFLIGHT_FAIL_SCOPED'
    out={'schema':'RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1','gate':'C10.65n','classification':cls,
         'target':'research/theory_targets/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_TARGET_v1.json','control_status':'HISTORICAL_PHENOMENOLOGICAL_CONTROL_ONLY',
         'control':{'J_ad0':-3.0,'A2':F(A2),'S_ur0':F(Sur),'C2':F(C2),'relative_entropy_gradients_zero':True,'relative_velocities_zero':True},
         'background':{k:F(v) for k,v in bg.items()},'grid_point_count':len(points),'points':points,
         'global_guards':{'min_DA':F(min_DA),'min_abs_lapse_denominator':F(min_lapse),'min_abs_finite_k_B_linear_denominator':F(min_Bden),'W_total':F(bg['W']),'one_plus_w_khr':F(1+bg['w_khr'])},
         'global_residuals':{'max_leading_normalized':F(max_lead),'max_finite_k_normalized':F(maxres),'threshold':1e-24},
         'metric_provenance_guard':'All preferred/Newtonian metric quantities in this result are reconstructed from the completed-U1 algebraic constraints and the declared invariant matching vector; no historical metric potential is consumed.',
         'UR_shear_status':'S_ur0 is carried as boundary data but full photon/UR anisotropic-stress insertion into Phi_N is deferred to C10.65o.',
         'interpretation':'Conditional preflight only: the historical control vector is external pre-EFT matching data, while the metric seed is independently reconstructed by the completed-U1 preferred DAE.',
         'next_gate':t['next_if_pass'] if pass_all else 'Audit the failed algebraic/low-k condition before any radiation-shear completion.','non_claims':t['non_claims']}
    path=ROOT/'research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json'; path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'grid_points':len(points),'max_leading_residual':F(max_lead),'max_finite_residual':F(maxres),'min_DA':F(min_DA),'min_Bden':F(min_Bden),'pass':pass_all},sort_keys=True))

if __name__=='__main__': main()
