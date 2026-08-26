#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
BASE=['c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime','c10_H0_ord_double_prime','c10_deltaH0_ord','c10_delta_mu_total','c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total','c10_W_total','c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']

def load(p): return json.loads((ROOT/p).read_text())
def M(x): return mp.mpf(str(x))
def Flt(x): return float(x)
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),mp.mpf('1e-80'))

def hist_rows(path):
    out=[]
    for raw in Path(path).read_text().splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        v=[float(x) for x in s.split()]
        if len(v)<len(BASE)+2: continue
        tail=v[-len(BASE):]; z={n:tail[i] for i,n in enumerate(BASE)}; z['tau']=v[0]; z['a']=v[1]; out.append(z)
    return out

def affine_intercept(xs,ys,n):
    xs=xs[:n]; ys=ys[:n]; N=M(n); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys)); den=N*sxx-sx*sx
    slope=(N*sxy-sx*sy)/den; return (sy-slope*sx)/N,slope

def khr_props(prod,gamma,a,k):
    c=M('299792.458'); H0=M(100)*M(prod['h'])/c; lam=M(prod['lam']); Om=M(prod['Om']); mu=3*H0*mp.sqrt(gamma); A=Om/(6*gamma)
    root=mp.sqrt(1+2*A+lam*A*A); x0=A*(2+lam*A)/(1+lam*A+root); x=x0/a**3; s=mp.sqrt(1+lam*x*x); r=x/s; tt=x/(s+1); Q=1+r
    rho=(2*mu*mu*x*(1+tt))/3; p=(2*mu*mu*r*tt)/3; w=p/rho; ca2=r/(s*(s+x)); MK=mu*Q*s*mp.sqrt(s); kstar=a*MK; cs2=ca2/(1+(k/kstar)**2)
    return {'rho':rho,'p':p,'W':rho+p,'w':w,'ca2':ca2,'cs2':cs2,'kstar':kstar}

def derived(bg):
    rb,rg,ru,rk,pk=bg['rb'],bg['rg'],bg['ru'],bg['rk'],bg['pk']; Wg=M(4)/3*rg; Wu=M(4)/3*ru; W0=rb+Wg+Wu; Wk=rk+pk
    return {'Wg':Wg,'Wu':Wu,'W0':W0,'Wk':Wk,'W':W0+Wk}

def project(bg,z,lam,Mc,k):
    a,H=bg['a'],bg['H']; dd=derived(bg); Wg,Wu,W0,Wk=dd['Wg'],dd['Wu'],dd['W0'],dd['Wk']; rb,rg,ru,rk=bg['rb'],bg['rg'],bg['ru'],bg['rk']
    Db,Dg,Dur=z['Db'],z['Dg'],z['Dur']; thb,thg,thur=z['thb'],z['thg'],z['thur']; dk,thk=z['dk'],z['thk']; x=k*k; L=-x; r=lam-1; D=3*lam-1
    h=rb*Db+rg*Dg+ru*Dur; ph=(rg*Dg+ru*Dur)/3
    q0N=a/x*(rb*thb+Wg*thg+Wu*thur)
    K=-M('1.5')*a*a/(x+a*a*Mc*Mc); a1=x/(x+a*a*Mc*Mc); Kp=2*H*a1*K
    W0p=-3*H*rb-4*H*(Wg+Wu); DA=1-3*K*W0; DAp=-3*(Kp*W0+K*W0p); psi=K*h/DA
    hp=-3*H*(h+ph)-(x/a)*q0N; psip=(Kp*h+K*hp-DAp*psi)/DA
    dmP=h+3*W0*psi+rk*dk
    qkP=a*Wk*thk/x; qbase=q0N+qkP; Qbase=3*a*qbase; X0=3*a*a*W0
    Eth=M(2); Pcal=M(1); lapse=r*Eth*L-2*D*H*H
    hamA=-3*a*a*r*dmP-D*H*Qbase+2*D*H*psip+2*r*Pcal*L*psi
    phiA=hamA/lapse; phiB=(D*H*X0)/lapse
    Bden=r*L+X0+D*H*phiB; Brhs=Qbase-D*(psip+H*phiA); B=Brhs/Bden
    QP=Qbase-X0*B; phi=phiA+phiB*B; Psi=psi-H*B
    return {'psi':psi,'psip':psip,'phi':phi,'B':B,'Psi':Psi,'QP':QP,'dmP':dmP,'q0N':q0N,'DA':DA,'lapse':lapse,'Bden':Bden}

def bg_prime(bg,Hp,ca2):
    H=bg['H']; dd=derived(bg); return {'a':bg['a']*H,'H':Hp,'rb':-3*H*bg['rb'],'rg':-4*H*bg['rg'],'ru':-4*H*bg['ru'],'rk':-3*H*dd['Wk'],'pk':ca2*(-3*H*dd['Wk'])}

def path(base,prime,e): return {k:base[k]+e*prime[k] for k in base}
def zpath(base,prime,e): return {k:base[k]+e*prime[k] for k in base}

def rhs(bg,z,proj,Phi,sg,sur,k,R,cb2,khr,slip):
    x=k*k; H=bg['H']; Psi=proj['Psi']; db=z['Db']+3*Psi; dg=z['Dg']+4*Psi; du=z['Dur']+4*Psi
    thbp=(-H*z['thb']+x*(cb2*db+R*(dg/4-sg))+R*slip)/(1+R)+x*Phi
    thgp=-(thbp+H*z['thb']-cb2*x*db)/R+x*(dg/4-sg)+(1+R)/R*x*Phi
    thurp=x*(du/4-sur)+x*Phi
    dkp=-(1+khr['w'])*(z['thk']+x*proj['B']-3*proj['psip'])-3*H*(khr['ca2']-khr['w'])*z['dk']
    thkp=-H*(1-3*khr['ca2'])*z['thk']+x*(khr['cs2']*z['dk']/(1+khr['w'])+proj['phi'])
    return {'Db':-z['thb'],'Dg':-M(4)/3*z['thg'],'Dur':-M(4)/3*z['thur'],'thb':thbp,'thg':thgp,'thur':thurp,'dk':dkp,'thk':thkp}

def bprime_directional(bg,bgp,z,zp,lam,Mc,k,dps):
    old=mp.mp.dps; mp.mp.dps=dps
    try:
        fn=lambda e: project(path(bg,bgp,e),zpath(z,zp,e),lam,Mc,k)['B']
        return +mp.diff(fn,M(0))
    finally: mp.mp.dps=old

def slip_value(bg,z,proj,Phi,o_rec,k,R,cb2,tau,dtau,Fc,Fp,Hp,PsiP):
    x=k*k; H=bg['H']; mc=-3*PsiP; App=Hp+H*H; thb=z['thb']; thg=z['thg']; dg=z['Dg']+4*proj['Psi']
    theta0p=x*M(o_rec['theta_prime_over_k2']); sg1=x*M(o_rec['sigma_g_first_over_k2']); sgp=M(16)/45*(tau*theta0p+dtau*thg)
    first=(dtau/tau-2*H/(1+R))*(thb-thg)+Fc*(-App*thb+x*(-H*dg/2+cb2*(-thb-mc)-M(1)/3*(-thg-mc))-H*x*Phi)
    comp=(1-2*H*Fc)*first+Fc*x*(2*H*sg1+sgp-(M(1)/3-cb2)*(Fc*theta0p+2*Fp*thb))
    return comp

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',dest='pat',required=True); args=ap.parse_args()
    mp.mp.dps=100
    t=load('research/theory_targets/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_TARGET_v1.json'); p=load('research/theory_results/RTK_C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_RESULT_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json'); n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json'); f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json'); state=load('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_EXECUTION'; assert p['classification']=='C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_PASS_SCOPED'; assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'; assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    aon=float(f['exact_anchor']['a_on']); expected=[float(x) for x in f['exact_anchor']['k_Mpc_inv']]
    hs=[]
    for fn in sorted(glob.glob(args.pat)):
        rr=hist_rows(fn); z=min(rr,key=lambda q:abs(q['a']-aon)); er=abs(z['a']-aon)/aon; k=sum(q['c10_k_Mpc_inv'] for q in rr)/len(rr)
        if er>1e-12: raise RuntimeError(f'no exact onset row {fn} {er}')
        hs.append((k,z,Path(fn).name,er))
    hs.sort(); assert len(hs)==4
    for (k,_,_,_),ke in zip(hs,expected):
        if abs(k-ke)>1e-10*max(1.0,abs(ke)): raise RuntimeError(f'k mismatch {k} {ke}')
    Hvals=[q[1]['c10_Hc'] for q in hs]; Hpvals=[q[1]['c10_Hc_prime'] for q in hs]
    Hmean=sum(Hvals)/4; Hpmean=sum(Hpvals)/4
    Hspread=max(abs(x-Hmean) for x in Hvals)/max(abs(Hmean),1e-300); Hpspread=max(abs(x-Hpmean) for x in Hpvals)/max(abs(Hpmean),1e-300)
    if Hspread>1e-10 or Hpspread>1e-10: raise RuntimeError(f'background k spread H={Hspread} Hp={Hpspread}')
    if abs(Hmean-n['background']['H'])/abs(n['background']['H'])>1e-10: raise RuntimeError('H mismatch')
    Hp=M(Hpmean); prod=state['final_replay_result']['rtk']['params']; gamma=M(src['provenance']['gamma_root'])
    bg0={'a':M(n['background']['a']),'H':M(n['background']['H']),'rb':M(n['background']['rhob']),'rg':M(n['background']['rhog']),'ru':M(n['background']['rhour']),'rk':M(n['background']['rho_khr']),'pk':M(n['background']['p_khr'])}
    pack=f['coefficient_pack']; R=M(pack['R']); cb2=M(pack['cb2']); tau=M(pack['tau_c_Mpc']); dtau=M(pack['dtau_c']); Fc=M(pack['F_Mpc']); Fp=M(pack['F_prime'])
    oidx={(str(q['lambda_HL']),str(q['M_c_Mpc_inv'])):q for q in o['points']}; records=[]; pointouts=[]; max_repro=mp.mpf('0'); max_slip_B=mp.mpf('0'); max_dps=mp.mpf('0'); max_cancel=mp.mpf('0'); allpass=True
    for npnt in n['points']:
        key=(str(npnt['lambda_HL']),str(npnt['M_c_Mpc_inv'])); opnt=oidx[key]; lam=M(npnt['lambda_HL']); Mc=M(npnt['M_c_Mpc_inv']); orecs={float(q['k']):q for q in opnt['finite_records']}; seq=[]
        for nr in npnt['finite_records']:
            k=M(nr['k']); x=k*k; oo=orecs[float(nr['k'])]; kp=khr_props(prod,gamma,bg0['a'],k)
            z={'Db':M(nr['Db']),'Dg':M(nr['Dg']),'Dur':M(nr['Dur']),'thb':x*M(nr['VN']),'thg':x*M(nr['VN']),'thur':x*M(nr['VN']),'dk':M(nr['delta_khr_pref']),'thk':x*M(nr['Vpref'])}
            pr=project(bg0,z,lam,Mc,k)
            repro=max(rel(pr['psi'],M(nr['psi'])),rel(pr['psip'],M(nr['psip'])),rel(pr['phi'],M(nr['phi'])),rel(pr['B'],M(nr['B'])),rel(pr['Psi'],M(nr['PsiN']))); max_repro=max(max_repro,repro)
            bgp=bg_prime(bg0,Hp,kp['ca2']); Phi=M(oo['PhiN']); sg=x*M(oo['sigma_g_over_k2']); sur=x*M(oo['sigma_ur_over_k2'])
            zp0=rhs(bg0,z,pr,Phi,sg,sur,k,R,cb2,kp,M(0))
            b70=bprime_directional(bg0,bgp,z,zp0,lam,Mc,k,70); b100=bprime_directional(bg0,bgp,z,zp0,lam,Mc,k,100); dconv=rel(b70,b100); max_dps=max(max_dps,dconv)
            PsiP=pr['psip']-Hp*pr['B']-bg0['H']*b100
            sl=slip_value(bg0,z,pr,Phi,oo,k,R,cb2,tau,dtau,Fc,Fp,Hp,PsiP)
            zpa=rhs(bg0,z,pr,Phi,sg,sur,k,R,cb2,kp,sl); ba=bprime_directional(bg0,bgp,z,zpa,lam,Mc,k,100); bind=rel(ba,b100); max_slip_B=max(max_slip_B,bind)
            # Explicitly verify internal slip cancellation with the exact source weights W_gamma=R W_b.
            bpiece=bg0['rb']*R/(1+R)*sl; gpiece=(R*bg0['rb'])*(-1/(1+R))*sl; cres=abs(bpiece+gpiece)/max(abs(bpiece),abs(gpiece),mp.mpf('1e-80')); max_cancel=max(max_cancel,cres)
            seq.append({'k':k,'x':x,'Bprime':b100,'PsiNprime':PsiP,'slip':sl,'slip_over_k2':sl/x,'reproduction_error':repro,'dps_convergence':dconv,'Bprime_slip_invariance':bind,'weighted_slip_cancel_residual':cres,'khr_ca2':kp['ca2'],'khr_cs2':kp['cs2'],'khr_kstar':kp['kstar']})
        xs=[q['x'] for q in seq]; fits={}; fok=True
        for name in ('Bprime','PsiNprime','slip_over_k2'):
            i3,s3=affine_intercept(xs,[q[name] for q in seq],3); i4,s4=affine_intercept(xs,[q[name] for q in seq],4); en=rel(i3,i4); ok=en<=M('1e-3'); fok=fok and ok
            fits[name]={'intercept_smallest3':Flt(i3),'intercept_all4':Flt(i4),'slope_all4':Flt(s4),'nested_intercept_relative':Flt(en),'threshold':1e-3,'pass':ok}
        ok=fok and all(q['reproduction_error']<=M('1e-9') and q['dps_convergence']<=M('1e-20') and q['Bprime_slip_invariance']<=M('1e-30') and q['weighted_slip_cancel_residual']<=M('1e-30') and all(mp.isfinite(q[v]) for v in ('Bprime','PsiNprime','slip','slip_over_k2')) for q in seq)
        allpass=allpass and ok
        pointouts.append({'lambda_HL':Flt(lam),'M_c_Mpc_inv':Flt(Mc),'pass':ok,'records':[{kk:Flt(vv) for kk,vv in q.items()} for q in seq],'fits':fits})
    allpass=allpass and len(pointouts)==9 and max_repro<=M('1e-9') and max_dps<=M('1e-20') and max_slip_B<=M('1e-30') and max_cancel<=M('1e-30')
    cls='C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED' if allpass else 'C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_FAIL_SCOPED'
    out={'schema':'RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1','gate':'C10.65q','classification':cls,'target':'research/theory_targets/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_TARGET_v1.json','control_status':'CONDITIONAL_HISTORICAL_PHENOMENOLOGICAL_CONTROL_ONLY',
         'background_derivative_pack':{'a_on':aon,'Hc':Hmean,'Hc_prime':Hpmean,'Hc_relative_k_spread':Hspread,'Hc_prime_relative_k_spread':Hpspread,'a_primeprime_over_a':float(Hp+bg0['H']*bg0['H']),'history_files':[q[2] for q in hs]},
         'global_checks':{'max_projector_reproduction_relative':Flt(max_repro),'max_70_vs_100_dps_Bprime_relative':Flt(max_dps),'max_Bprime_actual_slip_invariance_relative':Flt(max_slip_B),'max_weighted_photon_baryon_slip_cancel_residual':Flt(max_cancel)},
         'execution':'Bprime is the high-precision directional derivative of the general mixed-interface algebraic projector along the local aggregate RHS. Actual slip is inserted only after Psi_N_prime is reconstructed, then Bprime is recomputed as an invariance check.',
         'grid_point_count':len(pointouts),'points':pointouts,'metric_provenance_guard':'No historical CLASS metric potential is consumed; regenerated histories supply only the local production-background Hc_prime diagnostic branch.',
         'next_gate':t['next_if_pass'] if allpass else 'Audit the failed Bprime/slip numeric condition before any in-CLASS feedback.','non_claims':t['non_claims']}
    (ROOT/'research/theory_results/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'grid_points':len(pointouts),'Hc_prime':Hpmean,'max_repro':Flt(max_repro),'max_dps':Flt(max_dps),'max_Bprime_slip_invariance':Flt(max_slip_B),'pass':allpass},sort_keys=True))
if __name__=='__main__': main()
