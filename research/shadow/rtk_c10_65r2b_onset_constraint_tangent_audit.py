#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import mpmath as mp

ROOT=Path(__file__).resolve().parents[2]
C2=mp.mpf('-1.314425482950032')

def load(p): return json.loads((ROOT/p).read_text())
def M(x): return mp.mpf(str(x))
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),mp.mpf('1e-80'))
def pkey(lam,mc): return (round(float(lam),14),round(float(mc),8))
def rkey(k): return round(float(k),14)

def load_q_module():
    p=ROOT/'research/shadow/rtk_c10_65q_numeric_bprime_slip_closure_v2.py'
    spec=importlib.util.spec_from_file_location('c10q',p)
    mod=importlib.util.module_from_spec(spec); assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def main():
    mp.mp.dps=100
    qmod=load_q_module()
    t=load('research/theory_targets/RTK_C10_65R2B_ONSET_CONSTRAINT_TANGENT_AUDIT_TARGET_v1.json')
    qres=load('research/theory_results/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    r1=load('research/theory_results/RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_RESULT_v1.json')
    r2a=load('research/theory_results/RTK_C10_65R2A_FIRST_RHS_BRIDGE_ALGEBRA_AUDIT_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json')
    state=load('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_EXECUTION'
    assert qres['classification']=='C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED'
    assert r1['classification']=='C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_PASS_SCOPED'
    assert r2a['classification']=='C10_65R2A_FIRST_RHS_BRIDGE_ALGEBRA_AUDIT_PASS_SCOPED'

    Hp=M(qres['background_derivative_pack']['Hc_prime'])
    prod=state['final_replay_result']['rtk']['params']
    gamma=M(src['provenance']['gamma_root'])
    bg0={'a':M(n['background']['a']),'H':M(n['background']['H']),
         'rb':M(n['background']['rhob']),'rg':M(n['background']['rhog']),
         'ru':M(n['background']['rhour']),'rk':M(n['background']['rho_khr']),
         'pk':M(n['background']['p_khr'])}
    dd0=qmod.derived(bg0)
    R=dd0['Wg']/bg0['rb']
    cb2=M(f['coefficient_pack']['cb2'])
    ni={pkey(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in n['points']}
    oi={pkey(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in o['points']}
    qindex={pkey(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in qres['points']}

    records=[]; max_c0=mp.mpf('0'); vals=[]
    for pk,npnt in ni.items():
        opnt=oi[pk]; qpnt=qindex[pk]
        lam=M(npnt['lambda_HL']); Mc=M(npnt['M_c_Mpc_inv'])
        orecs={rkey(r['k']):r for r in opnt['finite_records']}
        qrecs={rkey(r['k']):r for r in qpnt['records']}
        for nr in npnt['finite_records']:
            k=M(nr['k']); x=k*k; oo=orecs[rkey(k)]; qr=qrecs[rkey(k)]
            kp=qmod.khr_props(prod,gamma,bg0['a'],k)
            z={'Db':M(nr['Db']),'Dg':M(nr['Dg']),'Dur':M(nr['Dur']),
               'thb':x*M(nr['VN']),'thg':x*M(nr['VN']),'thur':x*M(nr['VN']),
               'dk':M(nr['delta_khr_pref']),'thk':x*M(nr['Vpref'])}
            pr=qmod.project(bg0,z,lam,Mc,k)
            Phi=M(oo['PhiN']); sg=x*M(oo['sigma_g_over_k2']); sur=x*M(oo['sigma_ur_over_k2'])
            zp=qmod.rhs(bg0,z,pr,Phi,sg,sur,k,R,cb2,kp,M(0))
            bgp=qmod.bg_prime(bg0,Hp,kp['ca2'])
            def cons(e):
                be=qmod.path(bg0,bgp,e); ze=qmod.zpath(z,zp,e)
                pe=qmod.project(be,ze,lam,Mc,k)
                return 3*be['H']*pe['QP']+3*be['a']*be['a']*pe['dmP']-C2*x
            c0=cons(M(0)); cp=mp.diff(cons,M(0))
            scale=abs(3*bg0['H']*pr['QP'])+abs(3*bg0['a']*bg0['a']*pr['dmP'])+abs(C2*x)
            c0rel=abs(c0)/max(scale,mp.mpf('1e-80'))
            norm=abs(cp)/max(abs(bg0['H'])*scale,mp.mpf('1e-80'))
            max_c0=max(max_c0,c0rel); vals.append(norm)
            records.append({'lambda_HL':float(lam),'M_c_Mpc_inv':float(Mc),'k':float(k),
                            'onset_constraint_relative':float(c0rel),
                            'normalized_abs_constraint_prime':float(norm),
                            'constraint_prime':float(cp),
                            'q_Bprime_reference':float(M(qr['Bprime']))})
    checks=t['frozen_checks']; max_norm=max(vals); min_norm=min(vals)
    onset_ok=(len(records)==t['grid']['record_count'] and max_c0<=M(checks['max_onset_constraint_relative']))
    tangent=onset_ok and max_norm<=M(checks['tangent_max_normalized_abs_Cprime'])
    non_tangent=onset_ok and min_norm>=M(checks['resolved_non_tangent_min_normalized_abs_Cprime'])
    if tangent:
        classification='C10_65R2B_TANGENT_PASS_SCOPED'
        next_gate='Implement r2 Bprime by dual-propagating the conditioned onset-reduced r1 closure, then execute unchanged C10.65r2 parity.'
    elif non_tangent:
        classification='C10_65R2B_NON_TANGENT_RESOLVED_SCOPED'
        next_gate='Do not differentiate fixed-C2 onset reduction. Implement r2 Bprime from the general mixed-interface projector used by C10.65q; keep conditioned r1 only for the onset algebraic B value.'
    else:
        classification='C10_65R2B_INCONCLUSIVE_FAIL'
        next_gate='Diagnose tangent audit before any r2 Bprime C port.'
    out={'gate':'C10.65r2b','classification':classification,'r2_gate_status':'OPEN_NOT_EXECUTED',
         'record_count':len(records),'checks':{'max_onset_constraint_relative':float(max_c0),
         'min_normalized_abs_constraint_prime':float(min_norm),'max_normalized_abs_constraint_prime':float(max_norm)},
         'frozen_checks':checks,'r2_frozen_target_unchanged':True,'records':records,
         'interpretation':t['pre_registered_interpretation'],'next_gate':next_gate,'non_claims':t['hard_nonclaims']}
    path=ROOT/'research/theory_results/RTK_C10_65R2B_ONSET_CONSTRAINT_TANGENT_AUDIT_RESULT_v1.json'
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(classification,json.dumps(out['checks'],sort_keys=True))
    raise SystemExit(0 if (tangent or non_tangent) else 1)

if __name__=='__main__': main()
