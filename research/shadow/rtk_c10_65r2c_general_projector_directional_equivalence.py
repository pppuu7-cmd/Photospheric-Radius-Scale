#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]

def load(p): return json.loads((ROOT/p).read_text())
def M(x): return mp.mpf(str(x))
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),mp.mpf('1e-80'))
def pkey(lam,mc): return (round(float(lam),14),round(float(mc),8))
def rkey(k): return round(float(k),14)

def load_q():
    p=ROOT/'research/shadow/rtk_c10_65q_numeric_bprime_slip_closure_v2.py'
    spec=importlib.util.spec_from_file_location('c10q',p); mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None; spec.loader.exec_module(mod); return mod

def stable_general_B(bg,z,lam,Mc,k):
    a,H=bg['a'],bg['H']; rb,rg,ru,rk,pk=bg['rb'],bg['rg'],bg['ru'],bg['rk'],bg['pk']
    Wg=M(4)/3*rg; Wu=M(4)/3*ru; W0=rb+Wg+Wu; Wk=rk+pk
    Db,Dg,Dur=z['Db'],z['Dg'],z['Dur']; thb,thg,thur=z['thb'],z['thg'],z['thur']; dk,thk=z['dk'],z['thk']
    x=k*k; L=-x; r=lam-1; D=3*lam-1; E=M(2); P=M(1)
    h=rb*Db+rg*Dg+ru*Dur; ph=(rg*Dg+ru*Dur)/3
    q0N=a/x*(rb*thb+Wg*thg+Wu*thur)
    K=-M('1.5')*a*a/(x+a*a*Mc*Mc); a1=x/(x+a*a*Mc*Mc); Kp=2*H*a1*K
    W0p=-3*H*rb-4*H*(Wg+Wu); DA=1-3*K*W0; DAp=-3*(Kp*W0+K*W0p)
    psi=K*h/DA; hp=-3*H*(h+ph)-(x/a)*q0N; psip=(Kp*h+K*hp-DAp*psi)/DA
    dm=h+3*W0*psi+rk*dk; qk=a*Wk*thk/x; Q=3*a*(q0N+qk); X0=3*a*a*W0
    num=E*L*(Q-D*psip)+3*D*H*H*Q+3*D*H*a*a*dm-2*D*H*P*L*psi
    den=r*E*L*L-2*D*H*H*L+E*L*X0+3*D*H*H*X0
    return num/den

def stable_bprime(q,bg,bgp,z,zp,lam,Mc,k,dps):
    old=mp.mp.dps; mp.mp.dps=dps
    try:
        fn=lambda e: stable_general_B(q.path(bg,bgp,e),q.zpath(z,zp,e),lam,Mc,k)
        return +mp.diff(fn,M(0))
    finally: mp.mp.dps=old

def main():
    mp.mp.dps=100; q=load_q()
    t=load('research/theory_targets/RTK_C10_65R2C_GENERAL_PROJECTOR_DIRECTIONAL_EQUIVALENCE_TARGET_v1.json')
    qb=load('research/theory_results/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json'); state=load('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_EXECUTION'; assert qb['classification']=='C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED'
    Hp=M(qb['background_derivative_pack']['Hc_prime']); prod=state['final_replay_result']['rtk']['params']; gamma=M(src['provenance']['gamma_root'])
    bg={'a':M(n['background']['a']),'H':M(n['background']['H']),'rb':M(n['background']['rhob']),'rg':M(n['background']['rhog']),'ru':M(n['background']['rhour']),'rk':M(n['background']['rho_khr']),'pk':M(n['background']['p_khr'])}
    dd=q.derived(bg); R=dd['Wg']/bg['rb']; cb2=M(f['coefficient_pack']['cb2'])
    oi={pkey(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in o['points']}; qi={pkey(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in qb['points']}
    recs=[]; eB=M(0); eBp=M(0); eDps=M(0); eStored=M(0)
    for npnt in n['points']:
        pk=pkey(npnt['lambda_HL'],npnt['M_c_Mpc_inv']); op=oi[pk]; qp=qi[pk]; lam=M(npnt['lambda_HL']); Mc=M(npnt['M_c_Mpc_inv'])
        oo={rkey(r['k']):r for r in op['finite_records']}; qq={rkey(r['k']):r for r in qp['records']}
        for nr in npnt['finite_records']:
            k=M(nr['k']); x=k*k; ore=oo[rkey(k)]; qre=qq[rkey(k)]; kp=q.khr_props(prod,gamma,bg['a'],k)
            z={'Db':M(nr['Db']),'Dg':M(nr['Dg']),'Dur':M(nr['Dur']),'thb':x*M(nr['VN']),'thg':x*M(nr['VN']),'thur':x*M(nr['VN']),'dk':M(nr['delta_khr_pref']),'thk':x*M(nr['Vpref'])}
            pr=q.project(bg,z,lam,Mc,k); Phi=M(ore['PhiN']); sg=x*M(ore['sigma_g_over_k2']); sur=x*M(ore['sigma_ur_over_k2'])
            zp=q.rhs(bg,z,pr,Phi,sg,sur,k,R,cb2,kp,M(0)); bgp=q.bg_prime(bg,Hp,kp['ca2'])
            Bs=stable_general_B(bg,z,lam,Mc,k); eb=rel(Bs,pr['B']); eB=max(eB,eb)
            bo=q.bprime_directional(bg,bgp,z,zp,lam,Mc,k,100); bs100=stable_bprime(q,bg,bgp,z,zp,lam,Mc,k,100); bs70=stable_bprime(q,bg,bgp,z,zp,lam,Mc,k,70)
            ebp=rel(bs100,bo); ed=rel(bs70,bs100); es=rel(bs100,M(qre['Bprime']))
            eBp=max(eBp,ebp); eDps=max(eDps,ed); eStored=max(eStored,es)
            recs.append({'lambda_HL':float(lam),'M_c_Mpc_inv':float(Mc),'k':float(k),'B_relative':float(eb),'Bprime_relative':float(ebp),'stable_70_vs_100_relative':float(ed),'stable_vs_stored_q_Bprime_relative':float(es),'Bprime_stable':float(bs100)})
    c=t['frozen_checks']; passed=(len(recs)==c['record_count'] and eB<=M(c['max_stable_vs_original_B_relative']) and eBp<=M(c['max_stable_vs_original_Bprime_relative']) and eDps<=M(c['max_70_vs_100_dps_stable_Bprime_relative']) and eStored<=M(c['max_onset_q_Bprime_record_relative']))
    out={'gate':'C10.65r2c','classification':t['pass_classification'] if passed else t['fail_classification'],'r2_gate_status':'OPEN_NOT_EXECUTED','record_count':len(recs),'checks':{'max_stable_vs_original_B_relative':float(eB),'max_stable_vs_original_Bprime_relative':float(eBp),'max_70_vs_100_dps_stable_Bprime_relative':float(eDps),'max_stable_vs_stored_q_Bprime_relative':float(eStored)},'derived_general_form':t['derived_general_form'],'r2_frozen_target_unchanged':True,'records':recs,'next_gate':'Implement diagnostic C Bprime by differentiating the validated general cancellation-reduced mixed-interface projector, then execute unchanged C10.65r2 first-RHS parity.' if passed else 'Diagnose general projector equivalence before C port.','non_claims':t['hard_nonclaims']}
    p=ROOT/'research/theory_results/RTK_C10_65R2C_GENERAL_PROJECTOR_DIRECTIONAL_EQUIVALENCE_RESULT_v1.json'; p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'],json.dumps(out['checks'],sort_keys=True)); raise SystemExit(0 if passed else 1)
if __name__=='__main__': main()
