#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math
from pathlib import Path

BASE=[
'c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime','c10_H0_ord_double_prime',
'c10_deltaH0_ord','c10_delta_mu_total','c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total',
'c10_W_total','c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
CTRL=[
'c10_65a_delta_g','c10_65a_theta_g','c10_65a_shear_g','c10_65a_delta_b','c10_65a_theta_b',
'c10_65a_CLASS_psi_lapse','c10_65a_CLASS_phi_curvature','c10_65a_delta_ur','c10_65a_theta_ur','c10_65a_shear_ur']
COEFF=[
'c10_65e_R','c10_65e_cb2','c10_65e_dkappa','c10_65e_ddkappa','c10_65e_tau_c','c10_65e_dtau_c',
'c10_65e_F','c10_65e_F_prime','c10_65e_tca_flag','c10_65e_tau_c_over_tau_h','c10_65e_tau_c_over_tau_k',
'c10_65e_has_perturbed_recombination']
TAIL=BASE+CTRL+COEFF
SPREAD_KEYS=['c10_65e_R','c10_65e_cb2','c10_65e_dkappa','c10_65e_ddkappa','c10_65e_tau_c','c10_65e_dtau_c','c10_65e_F','c10_65e_F_prime']


def read_rows(path):
    rr=[]
    for raw in Path(path).read_text().splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        vals=[float(x) for x in s.split()]
        if len(vals)<len(TAIL): raise RuntimeError(f'row too short in {path}: {len(vals)} < {len(TAIL)}')
        tail=vals[-len(TAIL):]
        d={name:tail[i] for i,name in enumerate(TAIL)}
        d['tau']=vals[0]; d['a']=vals[1]
        rr.append(d)
    if len(rr)<3: raise RuntimeError(f'too few rows in {path}')
    return rr


def interp(rr,a):
    if not (rr[0]['a']<=a<=rr[-1]['a']): raise RuntimeError(f'a={a} outside support')
    lo=0; hi=len(rr)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if rr[m]['a']<=a: lo=m
        else: hi=m
    x0,x1=rr[lo],rr[hi]
    f=(a-x0['a'])/(x1['a']-x0['a']) if x1['a']!=x0['a'] else 0.0
    return {key:x0[key]+f*(x1[key]-x0[key]) for key in x0}


def relerr(a,b):
    return abs(a-b)/max(abs(a),abs(b),1e-300)


def relspread(vals):
    mean=sum(vals)/len(vals)
    return max(abs(x-mean) for x in vals)/max(max(abs(x) for x in vals),abs(mean),1e-300)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',dest='pattern',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]
    target=json.loads((root/'research/theory_targets/RTK_C10_65E_FROZEN_ONSET_TCA_COEFFICIENT_PACK_TARGET_v1.json').read_text())
    p65a=json.loads((root/'research/theory_results/RTK_C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_RESULT_v1.json').read_text())
    p65c=json.loads((root/'research/theory_results/RTK_C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_RESULT_v1.json').read_text())
    p65d=json.loads((root/'research/theory_results/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_RESULT_v1.json').read_text())
    assert target['status']=='FROZEN_BEFORE_EXECUTION'
    assert p65a['classification']=='C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_CONSISTENT_PASS_SCOPED'
    assert p65c['classification']=='C10_65C_COMMON_CURVATURE_ADIABATIC_BOUNDARY_PASS_SCOPED'
    assert p65d['classification']=='C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_PASS_SCOPED'
    a_on=float(p65a['technical']['a_on'])
    expected=[float(x) for x in p65a['technical']['k_values_Mpc_inv']]
    trig_h=float(p65d['frozen_port_contract']['trigger_tau_c_over_tau_h'])
    trig_k=float(p65d['frozen_port_contract']['trigger_tau_c_over_tau_k'])

    fs=sorted(glob.glob(args.pattern))
    if len(fs)!=len(expected): raise RuntimeError(f'expected {len(expected)} histories, got {len(fs)}')
    samples=[]
    for f in fs:
        rr=read_rows(f); z=interp(rr,a_on)
        k=sum(x['c10_k_Mpc_inv'] for x in rr)/len(rr)
        samples.append((k,z,Path(f).name))
    samples.sort(key=lambda x:x[0])
    for (k,_,_),ke in zip(samples,expected):
        if abs(k-ke)>1e-10*max(1.0,abs(ke)): raise RuntimeError(f'k mismatch {k} vs {ke}')

    recs=[]; max_alg=0.0; all_finite=True
    for k,z,name in samples:
        R=z['c10_65e_R']; cb2=z['c10_65e_cb2']; dk=z['c10_65e_dkappa']; ddk=z['c10_65e_ddkappa']; Hc=z['c10_Hc']
        tau=1.0/dk
        dtau=-ddk*tau*tau
        F=tau/(1.0+R)
        Fp=dtau/(1.0+R)+tau*Hc*R/(1.0+R)**2
        rh=tau*Hc; rk=tau*k
        checks={
          'tau_c':relerr(tau,z['c10_65e_tau_c']),
          'dtau_c':relerr(dtau,z['c10_65e_dtau_c']),
          'F':relerr(F,z['c10_65e_F']),
          'F_prime':relerr(Fp,z['c10_65e_F_prime']),
          'tau_c_over_tau_h':relerr(rh,z['c10_65e_tau_c_over_tau_h']),
          'tau_c_over_tau_k':relerr(rk,z['c10_65e_tau_c_over_tau_k'])}
        max_alg=max(max_alg,max(checks.values()))
        vals=[R,cb2,dk,ddk,tau,dtau,F,Fp,Hc,rh,rk,z['c10_65e_tca_flag'],z['c10_65e_has_perturbed_recombination']]
        all_finite=all_finite and all(math.isfinite(x) for x in vals)
        if not (R>0 and dk>0 and tau>0 and F>0 and 0<=cb2<1): raise RuntimeError(f'physical coefficient guard failed at k={k}')
        recs.append({'k_Mpc_inv':k,'a':a_on,'tau_Mpc':z['tau'],'Hc_Mpc_inv':Hc,'R':R,'cb2':cb2,'dkappa_Mpc_inv':dk,
                     'ddkappa_Mpc_inv2':ddk,'tau_c_Mpc':z['c10_65e_tau_c'],'dtau_c':z['c10_65e_dtau_c'],'F_Mpc':z['c10_65e_F'],
                     'F_prime':z['c10_65e_F_prime'],'tca_flag':z['c10_65e_tca_flag'],'tau_c_over_tau_h':z['c10_65e_tau_c_over_tau_h'],
                     'tau_c_over_tau_k':z['c10_65e_tau_c_over_tau_k'],'has_perturbed_recombination':z['c10_65e_has_perturbed_recombination'],
                     'algebraic_relative_residuals':checks,'source_file':name})

    spreads={key:relspread([z[key] for _,z,_ in samples]) for key in SPREAD_KEYS}
    max_spread=max(spreads.values())
    flags=[r['tca_flag'] for r in recs]; recomb=[r['has_perturbed_recombination'] for r in recs]
    flag_spread=max(flags)-min(flags); recomb_spread=max(recomb)-min(recomb)
    tca_triggers_ok=all(r['tau_c_over_tau_h']<trig_h and r['tau_c_over_tau_k']<trig_k for r in recs)
    technical_ok=(all_finite and max_alg<=1e-12 and max_spread<=1e-8 and flag_spread<=1e-12 and recomb_spread<=1e-12 and tca_triggers_ok)
    if not technical_ok:
        cls='C10_65E_FROZEN_ONSET_TCA_COEFFICIENT_PACK_TECHNICAL_FAIL_SCOPED'
    else:
        cls='C10_65E_FROZEN_ONSET_TCA_COEFFICIENT_PACK_PASS_SCOPED'

    means={key:sum(z[key] for _,z,_ in samples)/len(samples) for key in SPREAD_KEYS}
    out={
      'schema':'RTK_C10_65E_FROZEN_ONSET_TCA_COEFFICIENT_PACK_RESULT_v1','gate':'C10.65e','classification':cls,
      'target':'research/theory_targets/RTK_C10_65E_FROZEN_ONSET_TCA_COEFFICIENT_PACK_TARGET_v1.json',
      'frozen_onset':{'a_on':a_on,'k_values_Mpc_inv':[r['k_Mpc_inv'] for r in recs]},
      'coefficient_pack_mean_at_onset':{
        'R':means['c10_65e_R'],'cb2':means['c10_65e_cb2'],'dkappa_Mpc_inv':means['c10_65e_dkappa'],
        'ddkappa_Mpc_inv2':means['c10_65e_ddkappa'],'tau_c_Mpc':means['c10_65e_tau_c'],'dtau_c':means['c10_65e_dtau_c'],
        'F_Mpc':means['c10_65e_F'],'F_prime':means['c10_65e_F_prime'],
        'tca_flag_numeric':sum(flags)/len(flags),'has_perturbed_recombination_numeric':sum(recomb)/len(recomb)},
      'diagnostics':{'all_finite':all_finite,'max_algebraic_relative_residual':max_alg,'relative_spread_across_k':spreads,
                     'max_relative_spread_across_k':max_spread,'tca_flag_range':[min(flags),max(flags)],
                     'has_perturbed_recombination_range':[min(recomb),max(recomb)],
                     'max_tau_c_over_tau_h':max(r['tau_c_over_tau_h'] for r in recs),'trigger_tau_c_over_tau_h':trig_h,
                     'max_tau_c_over_tau_k':max(r['tau_c_over_tau_k'] for r in recs),'trigger_tau_c_over_tau_k':trig_k,
                     'tca_triggers_on_for_all_modes':tca_triggers_ok},
      'records':recs,
      'interpretation':'The pinned onset photon-baryon thermodynamic/TCA primitives are exported read-only and form a reproducible numeric coefficient pack for the corrected completed-U1 O(k^2) rank solver. Perturbed recombination is reported as a flag rather than promoted to an independent TCA initial datum.',
      'next_gate':target['next_if_pass'],'non_claims':target['non_claims']}
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps(out['diagnostics'],sort_keys=True))

if __name__=='__main__': main()
