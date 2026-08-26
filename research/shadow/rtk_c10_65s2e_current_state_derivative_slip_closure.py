#!/usr/bin/env python3
from __future__ import annotations
import inspect,json,math,pathlib,sys
P=pathlib.Path
sys.path.insert(0,str(P(__file__).resolve().parent))
from rtk_c10_65s2c_current_state_dae_metric_core import current_state_metric_core
from rtk_c10_65s2d_current_state_traceless_tca_closure import current_state_traceless_tca

def L(p): return json.load(open(p))
def rel(a,b):
    a=float(a); b=float(b); return abs(a-b)/max(abs(a),abs(b),1e-300)
def finite(*xs): return all(math.isfinite(float(x)) for x in xs)

class D:
    __slots__=('v','d')
    def __init__(self,v,d=0.0): self.v=float(v); self.d=float(d)
    @staticmethod
    def co(x): return x if isinstance(x,D) else D(x,0.0)
    def __add__(self,o): o=D.co(o); return D(self.v+o.v,self.d+o.d)
    __radd__=__add__
    def __sub__(self,o): o=D.co(o); return D(self.v-o.v,self.d-o.d)
    def __rsub__(self,o): o=D.co(o); return D(o.v-self.v,o.d-self.d)
    def __neg__(self): return D(-self.v,-self.d)
    def __mul__(self,o): o=D.co(o); return D(self.v*o.v,self.d*o.v+self.v*o.d)
    __rmul__=__mul__
    def __truediv__(self,o):
        o=D.co(o); q=self.v/o.v; return D(q,(self.d-q*o.d)/o.v)
    def __rtruediv__(self,o): return D.co(o).__truediv__(self)

def dae_dual(*,k,a,H,rb,rg,ru,rk,pk,Db,Dg,Dur,J,q0,thetaN,lam,Mc,Pcal=1.0,E=2.0):
    x=k*k; Lk=-x; r=lam-1.0; DD=3.0*lam-1.0
    Wg=(4.0/3.0)*rg; Wu=(4.0/3.0)*ru; W0=rb+Wg+Wu; Wk=rk+pk; W=W0+Wk
    h=rb*Db+rg*Dg+ru*Dur; ph=(rg*Dg+ru*Dur)/3.0
    denf=x+a*a*Mc*Mc; K=(-1.5)*a*a/denf; a1=x/denf; Kp=2.0*H*a1*K
    W0p=(-3.0)*H*rb+(-4.0)*H*(Wg+Wu)
    DA=1.0-3.0*K*W0; DAp=(-3.0)*(Kp*W0+K*W0p)
    psi=K*h/DA
    hp=(-3.0)*H*(h+ph)-(x/a)*q0
    psip=(Kp*h+K*hp-DAp*psi)/DA
    dm=h+3.0*W*psi+Wk*J
    Q0=3.0*a*(q0+a*Wk*thetaN/x)
    Xt=3.0*a*a*W
    lapse=r*E*Lk-2.0*DD*H*H
    A11=lapse; A12=(-DD)*H*Xt; A21=DD*H; A22=r*Lk+Xt
    b1=(-3.0)*a*a*r*dm-DD*H*Q0+2.0*DD*H*psip+2.0*r*Pcal*Lk*psi
    b2=Q0-DD*psip
    det=A11*A22-A12*A21
    phi=(b1*A22-A12*b2)/det
    B=(A11*b2-b1*A21)/det
    return {'B':B,'phi':phi,'psi':psi,'psip':psip,'det':det,'dm':dm,'Q0':Q0}

def dynamic_derivative_slip(*,k,a,H,Hprime,rb,rg,ru,rk,pk,lam,Mc,cb2,tau,dtau,
                            PsiN,db,tb,dg,tg,du,tu,sigma_ur,dkN,thetaN,w,ca2,cs2):
    x=k*k; Wg=(4.0/3.0)*rg; Wu=(4.0/3.0)*ru; Wk=rk+pk; R=Wg/rb
    Db=db-3.0*PsiN; Dg=dg-4.0*PsiN; Dur=du-4.0*PsiN; J=dkN/(1.0+w)-3.0*PsiN
    q0=a*(rb*tb+Wg*tg+Wu*tu)/x
    core=current_state_metric_core(k=k,a=a,H=H,rb=rb,rg=rg,ru=ru,rk=rk,pk=pk,lam=lam,Mc=Mc,PsiN=PsiN,
        db=db,tb=tb,dg=dg,tg=tg,du=du,tu=tu,dkN=dkN,tkN=thetaN)
    tr=current_state_traceless_tca(k=k,a=a,H=H,rb=rb,rg=rg,ru=ru,cb2=cb2,tau_c=tau,dtau_c=dtau,PsiN=core['Psi_N'],
        delta_b=db,theta_b=tb,delta_g=dg,theta_g=tg,sigma_ur=sigma_ur)
    B=core['B']; psi=core['psi_pref']; psip=core['psi_pref_prime']; phi=core['phi_pref']; Phi=tr['Phi_N']; sg=tr['sigma_g']
    deltaPref=(1.0+w)*(J+3.0*psi); thetaPref=thetaN-x*B
    thetaPrefP=-H*(1.0-3.0*ca2)*thetaPref+x*(cs2*deltaPref/(1.0+w)+phi)
    deltaPrefP=-(1.0+w)*(thetaPref+x*B-3.0*psip)-3.0*H*(ca2-w)*deltaPref

    rbp=-3.0*H*rb; Wgp=-4.0*H*Wg; Wup=-4.0*H*Wu
    agg_bg=rbp*tb+Wgp*tg+Wup*tu
    agg_pb=rb*(-H*tb+x*(cb2*db+R*(dg/4.0-sg))+(1.0+R)*x*Phi)
    agg_ur=Wu*x*(du/4.0-sigma_ur+Phi)
    M0=rb*tb+Wg*tg+Wu*tu; M0p=agg_bg+agg_pb+agg_ur
    ap=a*H; q0p=(ap*M0+a*M0p)/x

    derivatives={'a':ap,'H':Hprime,'rb':rbp,'rg':-4.0*H*rg,'ru':-4.0*H*ru,
                 'rk':-3.0*H*Wk,'pk':ca2*(-3.0*H*Wk),'Db':-tb,'Dg':-(4.0/3.0)*tg,'Dur':-(4.0/3.0)*tu,'J':-thetaN,'q0':q0p}
    def trial(u):
        z=dae_dual(k=k,a=D(a,derivatives['a']),H=D(H,derivatives['H']),rb=D(rb,derivatives['rb']),rg=D(rg,derivatives['rg']),ru=D(ru,derivatives['ru']),
          rk=D(rk,derivatives['rk']),pk=D(pk,derivatives['pk']),Db=D(Db,derivatives['Db']),Dg=D(Dg,derivatives['Dg']),Dur=D(Dur,derivatives['Dur']),
          J=D(J,derivatives['J']),q0=D(q0,derivatives['q0']),thetaN=D(thetaN,thetaPrefP+x*u),lam=lam,Mc=Mc)
        return z['B'].d,z
    f0,z0=trial(0.0); f1,_=trial(1.0); coeff=f1-f0; implicit_den=1.0-coeff; Bp=f0/implicit_den
    PsiNp=psip-Hprime*B-H*Bp

    metric_cont=-3.0*PsiNp; metric_euler=x*Phi; App=Hprime+H*H
    F=tau/(1.0+R); Fp=dtau/(1.0+R)+tau*H*R/((1.0+R)*(1.0+R))
    slip1=(dtau/tau-2.0*H/(1.0+R))*(tb-tg)+F*(-App*tb+x*(-H*dg/2.0+cb2*(-tb-metric_cont)-(4.0/3.0)*(-tg-metric_cont)/4.0)-H*metric_euler)
    shear1=(16.0/45.0)*tau*tg; thetaCommon=tr['theta0_prime']+metric_euler
    shear1p=(16.0/45.0)*(tau*thetaCommon+dtau*tg)
    slip=(1.0-2.0*H*F)*slip1+F*x*(2.0*H*shear1+shear1p-(1.0/3.0-cb2)*(F*thetaCommon+2.0*Fp*tb))
    tbp=(-H*tb+x*(cb2*db+R*(dg/4.0-sg))+R*slip)/(1.0+R)+metric_euler
    tgp=-(tbp+H*tb-cb2*x*db)/R+x*(dg/4.0-sg)+(1.0+R)/R*metric_euler
    tup=x*(du/4.0-sigma_ur)+metric_euler
    thetaNP=thetaPrefP+x*Bp
    deltaNP=-3.0*H*(ca2-w)*dkN-(1.0+w)*thetaN+3.0*(1.0+w)*PsiNp
    bp=rb*R/(1.0+R)*slip; gp=Wg*(-1.0/(1.0+R))*slip
    cancel=abs(bp+gp)/max(abs(bp),abs(gp),1e-300)
    return {'B':B,'B_prime':Bp,'Bprime_affine_f0':f0,'Bprime_affine_coefficient':coeff,'Bprime_implicit_denominator':implicit_den,
      'Psi_N_prime':PsiNp,'metric_continuity':metric_cont,'metric_euler':metric_euler,'Phi_N':Phi,'sigma_g':sg,'tca_slip':slip,
      'theta_b_prime':tbp,'theta_g_prime':tgp,'theta_ur_prime':tup,'delta_khr_pref_prime':deltaPrefP,'theta_khr_pref_prime':thetaPrefP,
      'delta_khr_N_prime':deltaNP,'theta_khr_N_prime':thetaNP,'weighted_slip_cancel':cancel,'q0_N':q0,'q0_N_prime':q0p,'J_khr':J}

def main():
    t=L('research/theory_targets/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_TARGET_v1.json')
    b=L('research/theory_results/RTK_C10_65S2B_NEWTONIAN_KHRONON_RHS_BRIDGE_RESULT_v1.json')
    c=L('research/theory_results/RTK_C10_65S2C_CURRENT_STATE_DAE_METRIC_CORE_RESULT_v1.json')
    d=L('research/theory_results/RTK_C10_65S2D_CURRENT_STATE_TRACELESS_TCA_CLOSURE_RESULT_v1.json')
    s1=L('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json')
    r2=L('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    cur=L('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert all(x['classification'].endswith('PASS_SCOPED') for x in [b,c,d])
    bg=n['background']; a=float(bg['a']); H=float(bg['H']); rb=float(bg['rhob']); rg=float(bg['rhog']); ru=float(bg['rhour']); rk=float(bg['rho_khr']); pk=float(bg['p_khr'])
    Hps=[float(q['Hc_prime_reconstructed']) for q in b['records']]; Hprime=sum(Hps)/len(Hps); assert max(Hps)-min(Hps)<1e-15
    pack=f['coefficient_pack']; cb2=float(pack['cb2']); tau=float(pack['tau_c_Mpc']); dtau=float(pack['dtau_c'])
    lamD=float(cur['final_replay_result']['rtk']['params']['lam']); xbg=float(b['background_audit']['x_large_branch_reconstructed']); sbg=math.hypot(1.0,math.sqrt(lamD)*xbg)
    ca2=xbg/(sbg*sbg*(sbg+xbg)); tt=xbg/(sbg+1.0); Q=1.0+xbg/sbg; mu2=3.0*rk/(2.0*xbg*(1.0+tt)); MK=math.sqrt(mu2)*Q*sbg*math.sqrt(sbg); kstar=a*MK
    w=pk/rk

    states={(float(q['lambda_HL']),float(q['M_c_Mpc_inv']),float(q['k'])):q for q in s1['completed_states']}
    exp={}
    for pt in r2['points']:
        for q in pt['records']: exp[(float(pt['lambda_HL']),float(pt['M_c_Mpc_inv']),float(q['k']))]=q['C']
    assert len(states)==len(exp)==36
    names={'B_prime':'c10_65r2_B_prime_actual','Psi_N_prime':'c10_65r2_Psi_N_prime','metric_continuity':'c10_65r2_metric_continuity_shadow','tca_slip':'c10_65r2_tca_slip_shadow','theta_b_prime':'c10_65r2_theta_b_prime_shadow','theta_g_prime':'c10_65r2_theta_g_prime_shadow','theta_ur_prime':'c10_65r2_theta_ur_prime_shadow','delta_khr_pref_prime':'c10_65r2_delta_khr_prime_shadow','theta_khr_pref_prime':'c10_65r2_theta_khr_prime_shadow'}
    maxima={q:0.0 for q in names}; maxcancel=0.0; minden=float('inf'); finite_all=True; rec=[]
    for key,st in states.items():
        lam,Mc,k=key; cs2=ca2/(1.0+(k/kstar)*(k/kstar))
        z=dynamic_derivative_slip(k=k,a=a,H=H,Hprime=Hprime,rb=rb,rg=rg,ru=ru,rk=rk,pk=pk,lam=lam,Mc=Mc,cb2=cb2,tau=tau,dtau=dtau,
            PsiN=float(st['phi_CLASS']),db=float(st['delta_b']),tb=float(st['theta_b']),dg=float(st['delta_g']),tg=float(st['theta_g']),du=float(st['delta_ur']),tu=float(st['theta_ur']),sigma_ur=float(st['shear_ur']),dkN=float(st['delta_cdm_khr']),thetaN=float(st['theta_cdm_khr']),w=w,ca2=ca2,cs2=cs2)
        er={q:rel(z[q],float(exp[key][col])) for q,col in names.items()}
        for q,v in er.items(): maxima[q]=max(maxima[q],v)
        maxcancel=max(maxcancel,z['weighted_slip_cancel']); minden=min(minden,abs(z['Bprime_implicit_denominator'])); finite_all &= all(math.isfinite(float(v)) for v in z.values())
        rec.append({'lambda_HL':lam,'M_c_Mpc_inv':Mc,'k':k,'cs2':cs2,'errors':er,'dynamic':z,'expected':{q:exp[key][col] for q,col in names.items()}})
    fc=t['frozen_checks']; lim={'B_prime':fc['max_B_prime_relative_vs_C10_65r2'],'Psi_N_prime':fc['max_Psi_N_prime_relative_vs_C10_65r2'],'metric_continuity':fc['max_metric_continuity_relative_vs_C10_65r2'],'tca_slip':fc['max_tca_slip_relative_vs_C10_65r2'],'theta_b_prime':fc['max_theta_b_prime_relative_vs_C10_65r2'],'theta_g_prime':fc['max_theta_g_prime_relative_vs_C10_65r2'],'theta_ur_prime':fc['max_theta_ur_prime_relative_vs_C10_65r2'],'delta_khr_pref_prime':fc['max_preferred_delta_khr_prime_relative_vs_C10_65r2'],'theta_khr_pref_prime':fc['max_preferred_theta_khr_prime_relative_vs_C10_65r2']}
    src=inspect.getsource(dynamic_derivative_slip); forbidden=['A2','C2','J_ad','S_ur0']
    checks={q:maxima[q]<=float(lim[q]) for q in names}; checks.update({'record_count':len(rec)==36,'weighted_slip_cancel':maxcancel<=float(fc['max_weighted_photon_baryon_slip_cancel_normalized']),'Bprime_implicit_denominator':minden>=float(fc['min_abs_Bprime_implicit_denominator']),'finite':finite_all,'no_seed_constants':all(x not in src for x in forbidden)})
    passed=all(checks.values())
    out={'schema':'RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1','gate':'C10.65s2e','classification':t['pass_classification'] if passed else t['fail_classification'],'target':'research/theory_targets/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_TARGET_v1.json','checks':checks,'maxima':maxima,'max_weighted_slip_cancel_normalized':maxcancel,'min_abs_Bprime_implicit_denominator':minden,'record_count':len(rec),'background':{'Hc':H,'Hc_prime':Hprime,'w_khr':w,'ca2_khr':ca2,'kstar_Mpc_inv':kstar},'dynamic_contract':{'Bprime':'scalar affine implicit solve from differentiated current-state DAE','PsiNprime':'psi_pref_prime-Hprime B-H Bprime','ordinary_aggregate_slip_dependence':'exactly cancelled before Bprime solve','neutral_coordinate_bridge':'s2b Newtonian image of preferred action RHS','new_temporal_datum_added':False},'records':rec,'threshold_changed':False,'next':t['next_if_pass'] if passed else 'Do not implement s2 production canary; resolve current-state derivative/slip mismatch.','non_claims':t['non_claims']}
    P('research/theory_results/RTK_C10_65S2E_CURRENT_STATE_DERIVATIVE_SLIP_CLOSURE_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification']); print(json.dumps({'maxima':maxima,'maxcancel':maxcancel,'minden':minden},sort_keys=True)); return 0 if passed else 2
if __name__=='__main__': sys.exit(main())
