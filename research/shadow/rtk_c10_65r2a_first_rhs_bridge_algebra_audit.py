#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(p): return json.loads((ROOT/p).read_text())
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)

def key(lam,mc): return (round(float(lam),14),round(float(mc),8))

def main():
    t=load('research/theory_targets/RTK_C10_65R2A_FIRST_RHS_BRIDGE_ALGEBRA_AUDIT_TARGET_v1.json')
    q=load('research/theory_results/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    r1=load('research/theory_results/RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_RESULT_v1.json')
    sl=load('research/theory_results/RTK_C10_65R2_SOURCE_LOCK_PREFLIGHT_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_EXECUTION'
    assert q['classification']=='C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'
    assert r1['classification']=='C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_PASS_SCOPED'
    assert sl['classification']=='C10_65R2_SOURCE_LOCK_PREFLIGHT_PASS_SCOPED'
    assert sl['r2_gate_status']=='OPEN_NOT_EXECUTED'
    H=float(q['background_derivative_pack']['Hc']); Hp=float(q['background_derivative_pack']['Hc_prime'])
    ni={key(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in n['points']}
    oi={key(p['lambda_HL'],p['M_c_Mpc_inv']):p for p in o['points']}
    records=[]; maxpsi=0.; maxrepr=0.; maxbinv=0.; maxcancel=0.
    for qp in q['points']:
        k0=key(qp['lambda_HL'],qp['M_c_Mpc_inv']); np=ni[k0]; op=oi[k0]
        nr={round(float(r['k']),14):r for r in np['finite_records']}
        orr={round(float(r['k']),14):r for r in op['finite_records']}
        for qr in qp['records']:
            kk=round(float(qr['k']),14); nn=nr[kk]; oo=orr[kk]
            B=float(nn['B']); psip=float(nn['psip']); Bp=float(qr['Bprime'])
            rec=psip-Hp*B-H*Bp; qpsi=float(qr['PsiNprime'])
            e=rel(rec,qpsi); maxpsi=max(maxpsi,e)
            maxrepr=max(maxrepr,float(qr['reproduction_error']))
            maxbinv=max(maxbinv,float(qr['Bprime_slip_invariance']))
            maxcancel=max(maxcancel,float(qr['weighted_slip_cancel_residual']))
            Phi=float(oo['PhiN']); k=float(qr['k'])
            mc=-3.*rec; me=k*k*Phi
            if not all(math.isfinite(x) for x in (rec,mc,me)): raise RuntimeError('nonfinite bridge value')
            records.append({'lambda_HL':float(qp['lambda_HL']),'M_c_Mpc_inv':float(qp['M_c_Mpc_inv']),'k':k,'Bprime_q':Bp,'PsiNprime_q':qpsi,'PsiNprime_reconstructed':rec,'PsiNprime_relative':e,'metric_continuity_shadow':mc,'metric_euler_shadow':me})
    c=t['frozen_checks']; passed=(len(records)==c['record_count'] and maxpsi<=c['max_reconstructed_vs_q_PsiNprime_relative'] and maxrepr<=c['max_q_projector_reproduction_relative'] and maxbinv<=c['max_q_Bprime_slip_invariance_relative'] and maxcancel<=c['max_q_weighted_photon_baryon_cancel_residual'])
    out={'gate':'C10.65r2a','classification':'C10_65R2A_FIRST_RHS_BRIDGE_ALGEBRA_AUDIT_PASS_SCOPED' if passed else 'C10_65R2A_FIRST_RHS_BRIDGE_ALGEBRA_AUDIT_FAIL','r2_gate_status':'OPEN_NOT_EXECUTED','record_count':len(records),'checks':{'max_reconstructed_vs_q_PsiNprime_relative':maxpsi,'max_q_projector_reproduction_relative':maxrepr,'max_q_Bprime_slip_invariance_relative':maxbinv,'max_q_weighted_photon_baryon_cancel_residual':maxcancel},'frozen_equations':t['frozen_equations'],'records':records,'non_claims':t['hard_nonclaims'],'next_gate':t['next_if_pass']}
    p=ROOT/'research/theory_results/RTK_C10_65R2A_FIRST_RHS_BRIDGE_ALGEBRA_AUDIT_RESULT_v1.json'; p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'],json.dumps(out['checks'],sort_keys=True))
    raise SystemExit(0 if passed else 1)
if __name__=='__main__': main()
