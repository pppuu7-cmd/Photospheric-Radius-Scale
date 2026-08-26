#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def rel(a,b): return abs(float(a)-float(b))/max(1.0,abs(float(a)),abs(float(b)))
def finite(x): return math.isfinite(float(x))
def parse(path):
    out=[]
    for line in Path(path).read_text().splitlines():
        if not line.strip(): continue
        p=line.split(',')
        if len(p)!=51: raise RuntimeError(f'observer column count {len(p)} != 51')
        r={'tau':float(p[0]),'a':float(p[1]),'k':float(p[2]),'tca':int(p[3]),'rsa':int(p[4]),'ufa':int(p[5]),'l_max_ur':int(p[6])}
        names=['phi_CLASS','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_cdm','theta_cdm','dU','dUprime','dV','dVprime','dZ','dZprime']
        for i,n in enumerate(names,7): r[n]=float(p[i])
        r['F_over_kpow']={l:float(p[23+l-3]) for l in range(3,31)}
        out.append(r)
    return out
def nearest(rows,k,a):
    q=[r for r in rows if rel(r['k'],k)<=1e-10]
    if not q: raise RuntimeError(f'no observer rows for k={k}')
    return min(q,key=lambda r:abs(r['a']-a))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--observer',required=True);ap.add_argument('--off-identity',required=True);ap.add_argument('--patch',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S5A_NEXT_K_NEAR_HORIZON_ONSET_STATE_PREFLIGHT_TARGET_v1.json');g=L('research/theory_results/RTK_C10_65S4G_MODERATE_K_LONGER_TIME_TRAJECTORY_RESULT_v1.json');s4a=L('research/theory_results/RTK_C10_65S4A_MODERATE_K_ONSET_STATE_DOMAIN_PREFLIGHT_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION';assert g['classification']==t['parents']['C10.65s4g'];assert s4a['classification']==t['parents']['C10.65s4a']
    rows=parse(a.observer);dom=t['domain'];c=t['prospective_checks'];aon=float(dom['a_on']);ks=[float(x) for x in dom['all_k_Mpc_inv']];on=[nearest(rows,k,aon) for k in ks]
    exact=all(rel(r['a'],aon)<=float(c['exact_onset_relative_a_tolerance']) for r in on)
    states=['phi_CLASS','delta_b','theta_b','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_cdm','theta_cdm']
    statefinite=all(finite(r[n]) for r in on for n in states)
    higherfinite=all(finite(r['F_over_kpow'][l]) and finite(r['F_over_kpow'][l]*(r['k']**l)) for r in on if r['ufa']==0 for l in range(3,r['l_max_ur']+1))
    approx=all((r['tca'],r['rsa'],r['ufa'],r['l_max_ur'])==(int(c['require_TCA_enum']),int(c['require_RSA_enum']),int(c['require_UFA_enum']),int(c['require_l_max_ur'])) for r in on)
    prior={float(r['k']):r for r in s4a['onset_rows']};regk=float(dom['regression_k_Mpc_inv'][0]);r=nearest(on,regk,aon);o=prior[regk];mx=0.0
    for n in ['a']+states+['dU','dUprime','dV','dVprime','dZ','dZprime']:
        mx=max(mx,rel(r[n],o[n]))
    for n in ['tca','rsa','ufa','l_max_ur']:
        mx=max(mx,0.0 if int(r[n])==int(o[n]) else 1.0)
    for l in range(3,18):
        oo=o['F_over_kpow'][str(l)] if str(l) in o['F_over_kpow'] else o['F_over_kpow'][l];mx=max(mx,rel(r['F_over_kpow'][l],oo))
    off=json.loads(Path(a.off_identity).read_text());patch=Path(a.patch).read_text();static={'separate_translation_unit':'rtk_c10_65s1_observer.c' in patch,'noinline_noclone':'noinline,noclone' in patch,'no_dy_assignment':'dy[' not in patch,'no_metric_assignment':'pvecmetric[' not in patch};static_ok=all(static.values())
    newk=float(dom['new_k_Mpc_inv'][0]);H=float(dom['Hc_on_Mpc_inv']);J=float(dom['inherited_matching_J']);A2=float(dom['inherited_matching_A2_Mpc2']);rat={'k':newk,'k_over_Hc':newk/H,'abs_A2_k2_over_J':abs(A2*newk*newk/J)}
    checks={'observer_anchor_count':len(on)==2,'new_anchor_count':len(dom['new_k_Mpc_inv'])==1,'off_numeric_text_sha256_identical_both':off.get('all_two_numeric_rows_sha256_identical') is True,'regression_onset_row_matches_s4a':mx<=float(c['regression_relative_tolerance']),'all_exact_onset_rows_present':exact,'all_state_coordinates_finite':statefinite,'all_active_UR_higher_coordinates_finite':higherfinite,'all_approximation_states_tca_rsa_ufa_lmax':approx,'observer_read_only_static_guard':static_ok,'threshold_changed':False}
    passed=checks['threshold_changed'] is False and all(v for k,v in checks.items() if k!='threshold_changed')
    # Observer columns l>l_max_ur are inactive placeholders and may be NaN.
    # Persist only the active UR hierarchy already covered by the frozen finite check.
    serial_on=[]
    for z in on:
        zz=dict(z)
        zz['F_over_kpow']={l:z['F_over_kpow'][l] for l in range(3,z['l_max_ur']+1)}
        serial_on.append(zz)
    out={'schema':'RTK_C10_65S5A_NEXT_K_NEAR_HORIZON_ONSET_STATE_PREFLIGHT_RESULT_v1','gate':'C10.65s5a','classification':t['pass_classification'] if passed else t['fail_classification'],'target':'research/theory_targets/RTK_C10_65S5A_NEXT_K_NEAR_HORIZON_ONSET_STATE_PREFLIGHT_TARGET_v1.json','checks':checks,'onset_rows':serial_on,'inactive_ur_placeholder_policy':'observer l>l_max_ur columns are not active state coordinates and are omitted from persisted JSON; frozen active-UR finiteness check is unchanged','domain_ratio_measurement_only':rat,'regression_max_relative_error':mx,'off_path':off,'static_observer_guards':static,'threshold_changed':False,'interpretation':t['interpretation_if_pass'] if passed else 'The frozen single-anchor near-horizon onset-state preflight failed; do not construct a completed-U1 seed at k=0.01 before diagnosis.','next_gate':t['next_if_pass'] if passed else 'Diagnose C10.65s5a without altering its frozen anchor or criteria.','non_claims':t['non_claims']}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n');print(out['classification']);print(json.dumps({'checks':checks,'ratio':rat,'regression':mx},sort_keys=True));raise SystemExit(0 if passed else 2)
if __name__=='__main__':main()
