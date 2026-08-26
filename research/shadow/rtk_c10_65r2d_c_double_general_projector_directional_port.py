#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, math, subprocess, sys
from pathlib import Path
import mpmath as mp
ROOT=Path(__file__).resolve().parents[2]

def load(p): return json.loads((ROOT/p).read_text())
def M(x): return mp.mpf(str(x))
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),mp.mpf('1e-80'))
def pkey(lam,mc): return (round(float(lam),14),round(float(mc),8))
def rkey(k): return round(float(k),14)
def imod(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None; spec.loader.exec_module(mod); return mod

def main():
    mp.mp.dps=100
    t=load('research/theory_targets/RTK_C10_65R2D_C_DOUBLE_GENERAL_PROJECTOR_DIRECTIONAL_PORT_TARGET_v1.json')
    r1=load('research/theory_results/RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_RESULT_v1.json')
    qb=load('research/theory_results/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1.json')
    r2c=load('research/theory_results/RTK_C10_65R2C_GENERAL_PROJECTOR_DIRECTIONAL_EQUIVALENCE_RESULT_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    src=load('research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json'); state=load('research/state/current.json')
    assert t['status']=='FROZEN_BEFORE_EXECUTION'
    assert r1['classification']=='C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_PASS_SCOPED'
    assert qb['classification']=='C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED'
    assert r2c['classification']=='C10_65R2C_GENERAL_PROJECTOR_DIRECTIONAL_EQUIVALENCE_PASS_SCOPED'
    q=imod('c10q','research/shadow/rtk_c10_65q_numeric_bprime_slip_closure_v2.py')
    c2=imod('c10r2c','research/shadow/rtk_c10_65r2c_general_projector_directional_equivalence.py')
    Hp=M(qb['background_derivative_pack']['Hc_prime']); prod=state['final_replay_result']['rtk']['params']; gamma=M(src['provenance']['gamma_root'])
    bg={'a':M(n['background']['a']),'H':M(n['background']['H']),'rb':M(n['background']['rhob']),'rg':M(n['background']['rhog']),'ru':M(n['background']['rhour']),'rk':M(n['background']['rho_khr']),'pk':M(n['background']['p_khr'])}
    dd=q.derived(bg); R=dd['Wg']/bg['rb']; cb2=M(f['coefficient_pack']['cb2'])
    oi={pkey(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in o['points']}; qi={pkey(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in qb['points']}
    rows=[]; refs=[]
    for npnt in n['points']:
        pk=pkey(npnt['lambda_HL'],npnt['M_c_Mpc_inv']); op=oi[pk]; qp=qi[pk]; lam=M(npnt['lambda_HL']); Mc=M(npnt['M_c_Mpc_inv'])
        oo={rkey(r['k']):r for r in op['finite_records']}; qq={rkey(r['k']):r for r in qp['records']}
        for nr in npnt['finite_records']:
            k=M(nr['k']); x=k*k; ore=oo[rkey(k)]; qre=qq[rkey(k)]; kp=q.khr_props(prod,gamma,bg['a'],k)
            z={'Db':M(nr['Db']),'Dg':M(nr['Dg']),'Dur':M(nr['Dur']),'thb':x*M(nr['VN']),'thg':x*M(nr['VN']),'thur':x*M(nr['VN']),'dk':M(nr['delta_khr_pref']),'thk':x*M(nr['Vpref'])}
            pr=q.project(bg,z,lam,Mc,k); Phi=M(ore['PhiN']); sg=x*M(ore['sigma_g_over_k2']); sur=x*M(ore['sigma_ur_over_k2'])
            zp=q.rhs(bg,z,pr,Phi,sg,sur,k,R,cb2,kp,M(0)); bgp=q.bg_prime(bg,Hp,kp['ca2'])
            Bs=c2.stable_general_B(bg,z,lam,Mc,k); Bps=c2.stable_bprime(q,bg,bgp,z,zp,lam,Mc,k,100)
            bvals=[bg[x] for x in ('a','H','rb','rg','ru','rk','pk')]; bd=[bgp[x] for x in ('a','H','rb','rg','ru','rk','pk')]
            zvals=[z[x] for x in ('Db','Dg','Dur','thb','thg','thur','dk','thk')]; zd=[zp[x] for x in ('Db','Dg','Dur','thb','thg','thur','dk','thk')]
            vals=[lam,Mc,k]+bvals+bd+zvals+zd
            rows.append(' '.join(format(float(v),'.17e') for v in vals))
            refs.append((lam,Mc,k,Bs,Bps,M(qre['Bprime'])))
    exe=ROOT/'c10_65r2d_general_projector_dual'
    subprocess.run(['cc','-std=c11','-O2','-Wall','-Wextra','-pedantic',str(ROOT/'rtk/c10_65r2d_general_projector_dual.c'),'-lm','-o',str(exe)],check=True)
    cp=subprocess.run([str(exe)],input='\n'.join(rows)+'\n',text=True,capture_output=True,check=True)
    outs=[line.split() for line in cp.stdout.splitlines() if line.strip()]
    if len(outs)!=len(refs): raise RuntimeError(f'C output count {len(outs)} != {len(refs)}')
    eB=M(0); eBp=M(0); eStored=M(0); records=[]; finite=True
    for ref,out in zip(refs,outs):
        lam,Mc,k,Bs,Bps,Bstored=ref; Bc=M(out[0]); Bpc=M(out[1]); finite=finite and math.isfinite(float(Bc)) and math.isfinite(float(Bpc))
        eb=rel(Bc,Bs); ebp=rel(Bpc,Bps); es=rel(Bpc,Bstored); eB=max(eB,eb); eBp=max(eBp,ebp); eStored=max(eStored,es)
        records.append({'lambda_HL':float(lam),'M_c_Mpc_inv':float(Mc),'k':float(k),'C_B':float(Bc),'C_Bprime':float(Bpc),'C_vs_stable_B_relative':float(eb),'C_vs_stable_Bprime_relative':float(ebp),'C_vs_stored_q_Bprime_relative':float(es)})
    source=(ROOT/'rtk/c10_65r2d_general_projector_dual.c').read_text()
    fixed_c2_absent=('C2' not in source and 'c2' not in source.lower().replace('c10',''))
    c=t['frozen_checks']; passed=(len(records)==c['record_count'] and eB<=M(c['max_C_double_vs_high_precision_stable_B_relative']) and eBp<=M(c['max_C_double_vs_high_precision_stable_Bprime_relative']) and eStored<=M(c['max_C_double_vs_persisted_q_Bprime_relative']) and finite and fixed_c2_absent)
    out={'gate':'C10.65r2d','classification':t['pass_classification'] if passed else t['fail_classification'],'r2_gate_status':'OPEN_NOT_EXECUTED','record_count':len(records),'checks':{'max_C_double_vs_high_precision_stable_B_relative':float(eB),'max_C_double_vs_high_precision_stable_Bprime_relative':float(eBp),'max_C_double_vs_persisted_q_Bprime_relative':float(eStored),'all_outputs_finite':finite,'fixed_C2_absent_from_C_directional_source':fixed_c2_absent},'records':records,'r2_frozen_target_unchanged':True,'next_gate':t['next_if_pass'] if passed else 'Diagnose the C double directional port without weakening frozen criteria.','non_claims':t['non_claims']}
    p=ROOT/'research/theory_results/RTK_C10_65R2D_C_DOUBLE_GENERAL_PROJECTOR_DIRECTIONAL_PORT_RESULT_v1.json'; p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'],json.dumps(out['checks'],sort_keys=True)); raise SystemExit(0 if passed else 1)
if __name__=='__main__': main()
