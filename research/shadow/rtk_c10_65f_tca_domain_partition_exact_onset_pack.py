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
PACK_KEYS=['c10_65e_R','c10_65e_cb2','c10_65e_dkappa','c10_65e_ddkappa','c10_65e_tau_c','c10_65e_dtau_c','c10_65e_F','c10_65e_F_prime','c10_Hc']


def read_rows(path):
    out=[]
    for raw in Path(path).read_text().splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        vals=[float(x) for x in s.split()]
        if len(vals)<len(TAIL): raise RuntimeError(f'row too short in {path}: {len(vals)} < {len(TAIL)}')
        tail=vals[-len(TAIL):]
        d={name:tail[i] for i,name in enumerate(TAIL)}
        d['tau']=vals[0]; d['a']=vals[1]
        out.append(d)
    if len(out)<3: raise RuntimeError(f'too few rows in {path}')
    return out


def relerr(a,b):
    return abs(a-b)/max(abs(a),abs(b),1e-300)


def relspread(vals):
    m=sum(vals)/len(vals)
    return max(abs(v-m) for v in vals)/max(abs(m),max(abs(v) for v in vals),1e-300)


def mean(rows,key): return sum(r[key] for r in rows)/len(rows)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',dest='pattern',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]
    target=json.loads((root/'research/theory_targets/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_TARGET_v1.json').read_text())
    a65=json.loads((root/'research/theory_results/RTK_C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_RESULT_v1.json').read_text())
    d65=json.loads((root/'research/theory_results/RTK_C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_RESULT_v1.json').read_text())
    audit=json.loads((root/'research/theory_results/RTK_C10_65E_FAILURE_AUDIT_RESULT_v1.json').read_text())
    assert target['status']=='FROZEN_BEFORE_EXECUTION'
    assert d65['classification']=='C10_65D_PINNED_COMPROMISE_TCA_PORT_CONTRACT_PASS_SCOPED'
    assert audit['classification']=='C10_65E_PREREGISTERED_ASSUMPTIONS_FALSE_METHOD_REFINEMENT_REQUIRED_SCOPED'
    a_on=float(a65['technical']['a_on']); expected=[float(x) for x in a65['technical']['k_values_Mpc_inv']]
    tol_a=1e-12; trig_h=float(d65['frozen_port_contract']['trigger_tau_c_over_tau_h']); trig_k=float(d65['frozen_port_contract']['trigger_tau_c_over_tau_k'])

    files=sorted(glob.glob(args.pattern))
    if len(files)!=len(expected): raise RuntimeError(f'expected {len(expected)} histories, got {len(files)}')
    modes=[]
    for f in files:
        rr=read_rows(f)
        k=sum(x['c10_k_Mpc_inv'] for x in rr)/len(rr)
        z=min(rr,key=lambda x:abs(x['a']-a_on))
        ra=abs(z['a']-a_on)/a_on
        modes.append({'k':k,'row':z,'rel_a':ra,'exact':ra<=tol_a,'file':Path(f).name})
    modes.sort(key=lambda m:m['k'])
    for m,ke in zip(modes,expected):
        if abs(m['k']-ke)>1e-10*max(1.0,abs(ke)): raise RuntimeError(f'k mismatch {m["k"]} vs {ke}')

    anchors=[m for m in modes if m['exact']]
    if len(anchors)<3: raise RuntimeError(f'only {len(anchors)} exact onset anchors; need >=3')
    rows=[m['row'] for m in anchors]
    spreads={key:relspread([r[key] for r in rows]) for key in PACK_KEYS}
    max_spread=max(spreads.values())
    pack={key:mean(rows,key) for key in PACK_KEYS}
    R=pack['c10_65e_R']; cb2=pack['c10_65e_cb2']; dk=pack['c10_65e_dkappa']; ddk=pack['c10_65e_ddkappa']; Hc=pack['c10_Hc']
    tau=1.0/dk; dtau=-ddk*tau*tau; F=tau/(1.0+R); Fp=dtau/(1.0+R)+tau*Hc*R/(1.0+R)**2; rh=tau*Hc
    algebraic=[]
    for r in rows:
        algebraic += [
          relerr(1.0/r['c10_65e_dkappa'],r['c10_65e_tau_c']),
          relerr(-r['c10_65e_ddkappa']*(1.0/r['c10_65e_dkappa'])**2,r['c10_65e_dtau_c']),
          relerr((1.0/r['c10_65e_dkappa'])/(1.0+r['c10_65e_R']),r['c10_65e_F']),
          relerr((-r['c10_65e_ddkappa']*(1.0/r['c10_65e_dkappa'])**2)/(1+r['c10_65e_R'])+(1.0/r['c10_65e_dkappa'])*r['c10_Hc']*r['c10_65e_R']/(1+r['c10_65e_R'])**2,r['c10_65e_F_prime']),
          relerr((1.0/r['c10_65e_dkappa'])*r['c10_Hc'],r['c10_65e_tau_c_over_tau_h'])]
    max_alg=max(algebraic)
    physical=all(math.isfinite(x) for x in [R,cb2,dk,ddk,Hc,tau,dtau,F,Fp]) and R>0 and 0<=cb2<1 and dk>0 and tau>0 and F>0
    k_tca=trig_k/tau
    on_flag=modes[0]['row']['c10_65e_tca_flag']
    partitions=[]; flag_ok=True
    for m in modes:
        predicted=(rh<trig_h and tau*m['k']<trig_k)
        actual=m['row']['c10_65e_tca_flag']
        match=(actual==on_flag) if predicted else (actual!=on_flag)
        flag_ok=flag_ok and match
        partitions.append({'k_Mpc_inv':m['k'],'nearest_rel_a_error':m['rel_a'],'exact_onset_anchor':m['exact'],
                           'predicted_tca_on':predicted,'nearest_exported_tca_flag':actual,'matches_partition':match})
    on_modes=[p['k_Mpc_inv'] for p in partitions if p['predicted_tca_on']]
    off_modes=[p['k_Mpc_inv'] for p in partitions if not p['predicted_tca_on']]
    first_off=min(off_modes) if off_modes else None
    lowk_seed_ok=len(on_modes)>=3 and all(on_modes[i]==expected[i] for i in range(3))
    ok=(physical and len(anchors)>=3 and max_spread<=1e-10 and max_alg<=1e-12 and rh<trig_h and flag_ok and lowk_seed_ok)
    cls='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED' if ok else 'C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_FAIL_SCOPED'
    out={
      'schema':'RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1','gate':'C10.65f','classification':cls,
      'target':'research/theory_targets/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_TARGET_v1.json',
      'exact_anchor':{'a_on':a_on,'relative_a_tolerance':tol_a,'count':len(anchors),'k_Mpc_inv':[m['k'] for m in anchors],
                      'max_relative_pack_spread':max_spread,'relative_spreads':spreads,'max_algebraic_relative_residual':max_alg},
      'coefficient_pack':{'R':R,'cb2':cb2,'dkappa_Mpc_inv':dk,'ddkappa_Mpc_inv2':ddk,'Hc_Mpc_inv':Hc,
                          'tau_c_Mpc':tau,'dtau_c':dtau,'F_Mpc':F,'F_prime':Fp,'tau_c_over_tau_h':rh},
      'tca_domain':{'trigger_tau_c_over_tau_h':trig_h,'trigger_tau_c_over_tau_k':trig_k,'derived_k_TCA_Mpc_inv':k_tca,
                    'numeric_tca_on_flag':on_flag,'on_modes_Mpc_inv':on_modes,'off_modes_Mpc_inv':off_modes,
                    'first_frozen_off_mode_Mpc_inv':first_off,'exported_flag_partition_match':flag_ok,'records':partitions},
      'rank_seed_domain':{'low_k_seed_ok':lowk_seed_ok,'interpretation':'The O(k^2) superhorizon rank system is a k->0 expansion and is certified to use the source-locked TCA branch. Finite-k evolution must retain the upstream TCA switch rather than extrapolate TCA beyond k_TCA.'},
      'interpretation':'C10.65e failed because it mixed sparse-history interpolation with a false all-k TCA assumption. C10.65f certifies an interpolation-safe exact-onset low-k coefficient pack and an explicit finite-k TCA regime boundary without weakening the failed C10.65e target after execution.',
      'next_gate':target['next_if_pass'],'non_claims':target['non_claims']}
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'exact_anchor_count':len(anchors),'max_pack_spread':max_spread,'max_alg':max_alg,'k_TCA':k_tca,'first_off':first_off,'flag_match':flag_ok},sort_keys=True))
    if not ok: raise SystemExit(2)

if __name__=='__main__': main()
