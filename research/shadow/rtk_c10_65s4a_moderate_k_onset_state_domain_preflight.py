#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def rel(a,b): return abs(float(a)-float(b))/max(1.0,abs(float(a)),abs(float(b)))
def finite(x): return math.isfinite(float(x))
def parse_observer(path:Path):
    rows=[]
    for line in path.read_text().splitlines():
        if not line.strip(): continue
        p=line.split(',')
        if len(p)!=51: raise RuntimeError(f'observer column count {len(p)} != 51')
        r={'tau':float(p[0]),'a':float(p[1]),'k':float(p[2]),'tca':int(p[3]),'rsa':int(p[4]),'ufa':int(p[5]),'l_max_ur':int(p[6])}
        names=['phi_CLASS','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_cdm','theta_cdm','dU','dUprime','dV','dVprime','dZ','dZprime']
        for i,n in enumerate(names,7): r[n]=float(p[i])
        r['F_over_kpow']={l:float(p[23+(l-3)]) for l in range(3,31)}
        rows.append(r)
    return rows
def find_onset(rows,k,aon,tol):
    cand=[r for r in rows if rel(r['k'],k)<=1e-10]
    if not cand: raise RuntimeError(f'no observer rows for k={k}')
    q=min(cand,key=lambda r:abs(r['a']-aon))
    return q,rel(q['a'],aon)<=tol
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--observer',required=True);ap.add_argument('--off-identity',required=True);ap.add_argument('--patch',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_TARGET_v1.json');s3d=L('research/theory_results/RTK_C10_65S3D_MATERIALLY_LONGER_TIME_TRAJECTORY_RESULT_v1.json');s1=L('research/theory_results/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1.json');f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION';assert s3d['classification']=='C10_65S3D_MATERIALLY_LONGER_TIME_TRAJECTORY_PASS_SCOPED';assert s1['classification']=='C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_PASS_SCOPED';assert f['classification']=='C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_PASS_SCOPED'
    off=json.loads(Path(a.off_identity).read_text());rows=parse_observer(Path(a.observer));dom=t['domain'];g=t['prospective_domain_guards'];aon=float(dom['a_on']);ks=[float(x) for x in dom['all_k_Mpc_inv']];newks=[float(x) for x in dom['new_k_Mpc_inv']];regks=[float(x) for x in dom['regression_k_Mpc_inv']]
    onset=[];exact=True
    for k in ks:
        q,ok=find_onset(rows,k,aon,float(g['exact_onset_relative_a_tolerance']));onset.append(q);exact &= ok
    state_names=['phi_CLASS','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_cdm','theta_cdm'];legacy=['dU','dUprime','dV','dVprime','dZ','dZprime']
    statefinite=all(finite(r[n]) for r in onset for n in state_names);legacyfinite=all(finite(r[n]) for r in onset for n in legacy)
    higherfinite=True
    for r in onset:
        if r['ufa']==0:
            for l in range(3,r['l_max_ur']+1):
                q=r['F_over_kpow'][l];Fl=q*(r['k']**l);higherfinite &= finite(q) and finite(Fl)
    approx=all((r['tca'],r['rsa'],r['ufa'],r['l_max_ur'])==(int(g['require_TCA_enum']),int(g['require_RSA_enum']),int(g['require_UFA_enum']),int(g['require_l_max_ur'])) for r in onset)
    old={float(r['k']):r for r in s1['observer_onset_rows']};reg_ok=True;reg_errors={}
    cmp_names=['a','tca','rsa','ufa','l_max_ur']+state_names+legacy
    for k in regks:
        r=min(onset,key=lambda z:abs(z['k']-k));o=old[k];mx=0.0
        for n in cmp_names:
            if n in ('tca','rsa','ufa','l_max_ur'): er=0.0 if int(r[n])==int(o[n]) else 1.0
            else: er=rel(r[n],o[n])
            mx=max(mx,er)
        for l in range(3,18): mx=max(mx,rel(r['F_over_kpow'][l],o['F_over_kpow'][str(l)] if isinstance(next(iter(o['F_over_kpow'].keys())),str) else o['F_over_kpow'][l]))
        reg_errors[format(k,'.17g')]=mx;reg_ok &= mx<=1e-12
    Hc=float(dom['Hc_on_Mpc_inv']);J=float(dom['inherited_matching_J']);A2=float(dom['inherited_matching_A2_Mpc2']);ratios=[]
    for k in newks:ratios.append({'k':k,'k_over_Hc':k/Hc,'abs_A2_k2_over_J':abs(A2*k*k/J)})
    maxkh=max(x['k_over_Hc'] for x in ratios);maxcorr=max(x['abs_A2_k2_over_J'] for x in ratios)
    patch=Path(a.patch).read_text();static={'separate_translation_unit':'rtk_c10_65s1_observer.c' in patch,'noinline_noclone':'noinline,noclone' in patch,'no_dy_assignment':'dy[' not in patch,'no_metric_assignment':'pvecmetric[' not in patch};static_ok=all(static.values())
    checks={'observer_anchor_count':len(onset)==4,'new_anchor_count':len(newks)==2,'off_numeric_text_sha256_identical_all_four':off.get('all_four_numeric_rows_sha256_identical') is True,'regression_onset_rows_match_s1':reg_ok,'all_exact_onset_rows_present':exact,'all_state_coordinates_finite':statefinite,'all_legacy_auxiliary_observer_coordinates_finite':legacyfinite,'all_active_UR_higher_coordinates_finite':higherfinite,'all_approximation_states_tca_rsa_ufa_lmax':approx,'max_k_over_Hc_within_guard':maxkh<=float(g['max_k_over_Hc']),'max_abs_A2_k2_over_J_within_guard':maxcorr<=float(g['max_abs_A2_k2_over_J']),'observer_read_only_static_guard':static_ok,'threshold_changed':False}
    passed=all(v is True for k,v in checks.items() if k!='threshold_changed') and checks['threshold_changed'] is False
    out={'schema':'RTK_C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_RESULT_v1','gate':'C10.65s4a','classification':t['pass_classification'] if passed else t['fail_classification'],'checks':checks,'onset_rows':onset,'domain_ratios':ratios,'max_k_over_Hc':maxkh,'max_abs_A2_k2_over_J':maxcorr,'regression_max_relative_errors':reg_errors,'off_path':off,'static_observer_guards':static,'threshold_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'At least one preregistered moderate-k onset-domain check failed; preserve the selected k values and guards and diagnose before completed-U1 seed construction.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s4a without changing its frozen k domain or guards.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['classification']);print(json.dumps({'checks':checks,'max_k_over_Hc':maxkh,'max_abs_A2_k2_over_J':maxcorr,'regression':reg_errors},sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
