#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,math,hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def L(p): return json.loads((ROOT/p).read_text())
def rel(a,b): return abs(a-b)/max(1.0,abs(a),abs(b))
def same(a,b,tol=1e-12): return rel(float(a),float(b))<=tol

def lin_slope(xs,ys):
    xm=sum(xs)/len(xs); ym=sum(ys)/len(ys)
    den=sum((x-xm)**2 for x in xs)
    return sum((x-xm)*(y-ym) for x,y in zip(xs,ys))/den

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

def point_find(points,lam,Mc):
    for p in points:
        if same(p['lambda_HL'],lam,1e-10) and same(p['M_c_Mpc_inv'],Mc,1e-10): return p
    raise KeyError((lam,Mc))
def rec_find(recs,k):
    for r in recs:
        if same(r['k'],k,1e-10): return r
    raise KeyError(k)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--observer',required=True); ap.add_argument('--off-identity',required=True); ap.add_argument('--patch',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
    t=L('research/theory_targets/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_TARGET_v1.json')
    s0=L('research/theory_results/RTK_C10_65S0_DIRECT_ONSET_STATE_VECTOR_ARCHITECTURE_RESULT_v1.json')
    n=L('research/theory_results/RTK_C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_RESULT_v1.json')
    o=L('research/theory_results/RTK_C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_RESULT_v1.json')
    f=L('research/theory_results/RTK_C10_65F_TCA_DOMAIN_PARTITION_EXACT_ONSET_PACK_RESULT_v1.json')
    r2=L('research/theory_results/RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_RESULT_v1.json')
    assert t['status']=='FROZEN_BEFORE_IMPLEMENTATION'
    assert s0['classification']=='C10_65S0_DIRECT_ONSET_INITIALIZATION_ARCHITECTURE_PASS_LEGACY_AUX_EXCLUSION_REQUIRED_SCOPED'
    assert n['classification']=='C10_65N_CONDITIONAL_COMPLETED_U1_ONSET_SEED_PREFLIGHT_PASS_SCOPED'
    assert o['classification']=='C10_65O_RADIATION_SHEAR_METRIC_CLOSURE_PASS_SCOPED'
    assert r2['classification']=='C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_PARITY_PASS_SCOPED'
    off=json.loads(Path(a.off_identity).read_text()); assert off['all_four_numeric_rows_sha256_identical'] is True
    aon=float(f['exact_anchor']['a_on']); kvals=[float(x) for x in f['exact_anchor']['k_Mpc_inv']]
    rows=parse_observer(Path(a.observer)); assert rows
    onset=[]
    for k in kvals:
        cand=[r for r in rows if same(r['k'],k,1e-8)]
        if not cand: raise RuntimeError(f'no observer rows for k={k}')
        q=min(cand,key=lambda r:abs(r['a']-aon))
        if rel(q['a'],aon)>1e-12: raise RuntimeError(f'onset miss k={k}: a={q["a"]} target={aon}')
        onset.append(q)
    assert all(r['tca']==0 for r in onset),[(r['k'],r['tca']) for r in onset]  # tca_on enum=0
    rsa_flags=sorted(set(r['rsa'] for r in onset)); ufa_flags=sorted(set(r['ufa'] for r in onset))
    if len(rsa_flags)!=1 or len(ufa_flags)!=1: raise RuntimeError('approximation flags differ across anchors')
    lmaxs=sorted(set(r['l_max_ur'] for r in onset));
    if len(lmaxs)!=1 or lmaxs[0]>30: raise RuntimeError(f'noncommon/too-large l_max_ur {lmaxs}')
    lmax=lmaxs[0]
    legacy_names=['dU','dUprime','dV','dVprime','dZ','dZprime']
    if not all(math.isfinite(r[x]) for r in onset for x in legacy_names): raise RuntimeError('legacy auxiliary observer values not finite')

    active_higher = onset[0]['ufa']==0
    slopes={}; resolution_limited=[]; historical_controls={}
    if active_higher:
        for l in range(3,lmax+1):
            vals=[]
            for r in onset:
                q=r['F_over_kpow'][l]
                if not math.isfinite(q): raise RuntimeError(f'nonfinite F_l/k^l l={l}')
                vals.append(q)
            historical_controls[str(l)]={format(r['k'],'.17g'): r['F_over_kpow'][l]*(r['k']**l) for r in onset}
        for l in (3,4,5):
            if l>lmax: continue
            Fs=[abs(r['F_over_kpow'][l]*(r['k']**l)) for r in onset]
            if all(v>1e-280 for v in Fs):
                sl=lin_slope([math.log(r['k']) for r in onset],[math.log(v) for v in Fs])
                slopes[str(l)]={'measured':sl,'expected':l,'abs_difference':abs(sl-l),'threshold':0.35,'pass':abs(sl-l)<=0.35}
                if abs(sl-l)>0.35: raise RuntimeError(f'UR l={l} regular slope failed: {sl}')
            else:
                resolution_limited.append(l)
                slopes[str(l)]={'classification':'RESOLUTION_LIMITED','min_abs_F':min(Fs)}

    w=float(n['background']['w_khr']); Sur=float(n['control']['S_ur0'])
    completed=[]
    for pn in n['points']:
        po=point_find(o['points'],pn['lambda_HL'],pn['M_c_Mpc_inv'])
        for rn in pn['finite_records']:
            k=float(rn['k']); ro=rec_find(po['finite_records'],k)
            Psi=float(rn['PsiN']); VN=float(rn['VN'])
            st={
              'lambda_HL':float(pn['lambda_HL']),'M_c_Mpc_inv':float(pn['M_c_Mpc_inv']),'k':k,
              'phi_CLASS':Psi,
              'delta_b':float(rn['Db'])+3.*Psi,'theta_b':k*k*VN,
              'delta_g':float(rn['Dg'])+4.*Psi,'theta_g':k*k*VN,
              'delta_ur':float(rn['Dur'])+4.*Psi,'theta_ur':k*k*VN,'shear_ur':k*k*Sur,
              'delta_cdm_khr':(1.+w)*(float(rn['Jkhr'])+3.*Psi),'theta_cdm_khr':k*k*VN,
              'Phi_N_constraint_not_state':float(ro['PhiN']),
              'legacy_nlde_auxiliaries_excluded':True,
              'higher_order_historical_control':{}
            }
            if active_higher:
                obs=min(onset,key=lambda z:abs(z['k']-k))
                st['higher_order_historical_control']={str(l):obs['F_over_kpow'][l]*(k**l) for l in range(3,lmax+1)}
            nums=[v for v in st.values() if isinstance(v,(float,int)) and not isinstance(v,bool)]
            nums += list(st['higher_order_historical_control'].values())
            if not all(math.isfinite(float(v)) for v in nums): raise RuntimeError('nonfinite completed state')
            completed.append(st)
    if len(completed)!=36: raise RuntimeError(f'completed state count {len(completed)} != 36')

    patch=Path(a.patch).read_text()
    static={'separate_translation_unit':"rtk_c10_65s1_observer.c" in patch,'noinline_noclone':('noinline,noclone' in patch),'no_dy_assignment':('dy[' not in patch),'no_metric_assignment':('pvecmetric[' not in patch)}
    if not all(static.values()): raise RuntimeError(f'static observer guard failed {static}')
    cls=t['conditional_classification'] if resolution_limited else t['pass_classification']
    out={
      'schema':'RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_RESULT_v1','gate':'C10.65s1','classification':cls,
      'target':'research/theory_targets/RTK_C10_65S1_FINITE_STATE_COMPLETION_AT_ONSET_TARGET_v1.json','a_on':aon,
      'anchor_count':4,'completion_record_count':len(completed),'off_path':off,
      'approximation_state':{'TCA':'ON','TCA_enum':onset[0]['tca'],'RSA_enum':onset[0]['rsa'],'UFA_enum':onset[0]['ufa'],'l_max_ur':lmax,'active_higher_UR_hierarchy':active_higher},
      'observer_onset_rows':onset,'higher_order_control':{'status':'HIGHER_ORDER_HISTORICAL_CONTROL','slopes':slopes,'resolution_limited_l':resolution_limited,'values':historical_controls},
      'legacy_auxiliary_audit':{'observed_allocated_and_finite':True,'excluded_from_completed_state':True,'names':legacy_names},
      'completed_states':completed,'static_observer_guards':static,
      'interpretation':'The complete finite state needed by a direct-at-a_on opt-in canary is now explicit at the certified four low-k anchors. Any retained UR l>=3 values are historical higher-order controls only, not a completed-U1 O(k^2) prediction.',
      'next_gate':t['next_if_pass'],'non_claims':t['non_claims']
    }
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps({'rsa':onset[0]['rsa'],'ufa':onset[0]['ufa'],'l_max_ur':lmax,'resolution_limited':resolution_limited,'completed':len(completed)},sort_keys=True))
if __name__=='__main__': main()
