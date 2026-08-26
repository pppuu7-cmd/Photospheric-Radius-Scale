#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, hashlib, json, math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
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
R0=[
'c10_65r0_a','c10_65r0_Hc','c10_65r0_rho_b','c10_65r0_rho_g','c10_65r0_rho_ur','c10_65r0_R',
'c10_65r0_cb2','c10_65r0_dkappa','c10_65r0_ddkappa','c10_65r0_tau_c','c10_65r0_dtau_c',
'c10_65r0_F','c10_65r0_F_prime','c10_65r0_tca_flag']
TAIL=BASE+CTRL+COEFF


def load(rel): return json.loads((ROOT/rel).read_text())
def rel(a,b): return abs(a-b)/max(abs(a),abs(b),1e-300)

def numeric_lines(path):
    return [x.strip() for x in Path(path).read_text().splitlines() if x.strip() and not x.lstrip().startswith('#')]

def digest_numeric(path):
    return hashlib.sha256(('\n'.join(numeric_lines(path))+'\n').encode()).hexdigest()

def read_rows(path,on=False):
    names=TAIL+(R0 if on else [])
    out=[]
    for s in numeric_lines(path):
        vals=[float(x) for x in s.split()]
        if len(vals)<len(names): raise RuntimeError(f'row too short {path}: {len(vals)} < {len(names)}')
        tail=vals[-len(names):]
        d={n:tail[i] for i,n in enumerate(names)}
        d['tau']=vals[0]; d['a_standard']=vals[1]
        out.append(d)
    if len(out)<3: raise RuntimeError(f'too few rows in {path}')
    return out

def modes(pattern,on=False):
    fs=sorted(glob.glob(pattern))
    out=[]
    for f in fs:
        rr=read_rows(f,on)
        k=sum(r['c10_k_Mpc_inv'] for r in rr)/len(rr)
        out.append({'k':k,'file':f,'rows':rr,'numeric_sha256':digest_numeric(f)})
    return sorted(out,key=lambda x:x['k'])

def mean(v): return sum(v)/len(v)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline-glob',required=True); ap.add_argument('--off-glob',required=True); ap.add_argument('--on-glob',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    t=load('research/theory_targets/RTK_C10_65R0_OPT_IN_CLASS_LOCAL_ENVIRONMENT_EXPORT_TARGET_v1.json')
    f=load('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    n=load('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    o=load('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    p=load('research/theory_results/RTK_C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_RESULT_v1.json')
    q=load('research/theory_results/RTK_C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'
    assert p['classification']=='C10_65P_SLIP_DERIVATIVE_TRIANGULAR_CLOSURE_PASS_SCOPED'
    assert q['classification']=='C10_65Q_NUMERIC_BPRIME_SLIP_CLOSURE_PASS_SCOPED'

    b=modes(a.baseline_glob,False); off=modes(a.off_glob,False); on=modes(a.on_glob,True)
    expected=[float(x) for x in t['anchors']['k_Mpc_inv']]
    if len(b)!=4 or len(off)!=4 or len(on)!=4: raise RuntimeError(f'file counts baseline/off/on={len(b)}/{len(off)}/{len(on)}')
    for seq in (b,off,on):
        for m,k in zip(seq,expected):
            if rel(m['k'],k)>1e-12: raise RuntimeError(f'k mismatch {m["k"]} vs {k}')

    off_pairs=[]; off_exact=True
    for mb,mo in zip(b,off):
        same=mb['numeric_sha256']==mo['numeric_sha256']
        off_exact=off_exact and same
        off_pairs.append({'k_Mpc_inv':mb['k'],'baseline_numeric_sha256':mb['numeric_sha256'],'patched_off_numeric_sha256':mo['numeric_sha256'],'identical':same})

    dup_pairs={
      'a':('c10_65r0_a',None), 'Hc':('c10_65r0_Hc','c10_Hc'), 'R':('c10_65r0_R','c10_65e_R'),
      'cb2':('c10_65r0_cb2','c10_65e_cb2'), 'dkappa':('c10_65r0_dkappa','c10_65e_dkappa'),
      'ddkappa':('c10_65r0_ddkappa','c10_65e_ddkappa'), 'tau_c':('c10_65r0_tau_c','c10_65e_tau_c'),
      'dtau_c':('c10_65r0_dtau_c','c10_65e_dtau_c'), 'F':('c10_65r0_F','c10_65e_F'),
      'F_prime':('c10_65r0_F_prime','c10_65e_F_prime'), 'tca_flag':('c10_65r0_tca_flag','c10_65e_tca_flag')}
    maxdup=0.0
    for m in on:
        for r in m['rows']:
            for name,(x,y) in dup_pairs.items():
                ref=r['a_standard'] if y is None else r[y]
                maxdup=max(maxdup,rel(r[x],ref))

    a_on=float(t['anchors']['a_on']); tol_a=float(t['frozen_checks']['exact_onset_relative_a_tolerance'])
    onset=[]; all_finite=True; positive=True
    for m in on:
        z=min(m['rows'],key=lambda r:abs(r['c10_65r0_a']-a_on))
        ra=abs(z['c10_65r0_a']-a_on)/a_on
        rec={'k_Mpc_inv':m['k'],'relative_a_error':ra}
        for key in R0: rec[key]=z[key]
        onset.append(rec)
        vals=[z[k] for k in R0]
        all_finite=all_finite and all(math.isfinite(x) for x in vals)
        positive=positive and all(z[k]>0 for k in ['c10_65r0_rho_b','c10_65r0_rho_g','c10_65r0_rho_ur','c10_65r0_R','c10_65r0_dkappa','c10_65r0_tau_c','c10_65r0_F'])
    exact_onset=all(r['relative_a_error']<=tol_a for r in onset)

    pack=f['coefficient_pack']
    compare={
      'R':('c10_65r0_R',float(pack['R'])), 'cb2':('c10_65r0_cb2',float(pack['cb2'])),
      'dkappa':('c10_65r0_dkappa',float(pack['dkappa_Mpc_inv'])), 'ddkappa':('c10_65r0_ddkappa',float(pack['ddkappa_Mpc_inv2'])),
      'Hc':('c10_65r0_Hc',float(pack['Hc_Mpc_inv'])), 'tau_c':('c10_65r0_tau_c',float(pack['tau_c_Mpc'])),
      'dtau_c':('c10_65r0_dtau_c',float(pack['dtau_c'])), 'F':('c10_65r0_F',float(pack['F_Mpc'])),
      'F_prime':('c10_65r0_F_prime',float(pack['F_prime']))}
    pack_errors={}
    for name,(key,refv) in compare.items():
        v=mean([r[key] for r in onset]); pack_errors[name]={'on_mean':v,'frozen':refv,'relative':rel(v,refv)}
    maxpack=max(x['relative'] for x in pack_errors.values())
    expected_tca=float(f['tca_domain']['numeric_tca_on_flag'])
    tca_ok=all(r['c10_65r0_tca_flag']==expected_tca for r in onset)

    th=t['frozen_checks']
    ok=(off_exact and exact_onset and maxdup<=float(th['max_on_duplicate_relative_residual']) and
        maxpack<=float(th['max_onset_pack_relative_to_C10_65f']) and tca_ok and all_finite and positive)
    cls=t['pass_classification'] if ok else t['fail_classification']
    out={
      'schema':'RTK_C10_65R0_OPT_IN_CLASS_LOCAL_ENVIRONMENT_EXPORT_RESULT_v1','gate':'C10.65r0','classification':cls,
      'target':'research/theory_targets/RTK_C10_65R0_OPT_IN_CLASS_LOCAL_ENVIRONMENT_EXPORT_TARGET_v1.json',
      'runtime_flag':{'name':'c10_65r0_diag','default':0.0,'enabled':1.0},
      'off_path':{'numeric_text_sha256_identical_all_four':off_exact,'records':off_pairs},
      'on_path':{'max_duplicate_relative_residual':maxdup,'exact_onset_all_four':exact_onset,'all_finite':all_finite,'positive_guards':positive,
                 'expected_tca_on_flag':expected_tca,'tca_flag_match':tca_ok,'onset_records':onset},
      'frozen_pack_parity':{'max_relative':maxpack,'threshold':float(th['max_onset_pack_relative_to_C10_65f']),'components':pack_errors},
      'metric_provenance_guard':'C10.65r0 exports no metric potential. Historical CLASS psi/phi columns may coexist in the parent diagnostic output but are not consumed by this analyzer or certified as completed-U1 data.',
      'interpretation':t['interpretation_if_pass'] if ok else 'The dormant interface or its local environment parity failed a frozen implementation check; do not proceed to C10.65r1.',
      'next_gate':t['next_if_pass'] if ok else 'diagnose C10.65r0 without weakening frozen criteria',
      'non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'off_exact':off_exact,'maxdup':maxdup,'maxpack':maxpack,'exact_onset':exact_onset,'tca_ok':tca_ok},sort_keys=True))
    if not ok: raise SystemExit(2)

if __name__=='__main__': main()
