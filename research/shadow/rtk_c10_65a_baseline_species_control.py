#!/usr/bin/env python3
from __future__ import annotations
import argparse, glob, json, math
from pathlib import Path

BASE_DIAG=[
'c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime','c10_H0_ord_double_prime',
'c10_deltaH0_ord','c10_delta_mu_total','c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total',
'c10_W_total','c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
CTRL=[
'c10_65a_delta_g','c10_65a_theta_g','c10_65a_shear_g','c10_65a_delta_b','c10_65a_theta_b',
'c10_65a_CLASS_psi_lapse','c10_65a_CLASS_phi_curvature','c10_65a_delta_ur','c10_65a_theta_ur','c10_65a_shear_ur']
TAIL=BASE_DIAG+CTRL


def read_rows(path):
    rr=[]
    for raw in Path(path).read_text().splitlines():
        s=raw.strip()
        if not s or s.startswith('#'): continue
        vals=[float(x) for x in s.split()]
        if len(vals)<len(TAIL): raise RuntimeError(f'row too short in {path}')
        tail=vals[-len(TAIL):]
        d={name:tail[i] for i,name in enumerate(TAIL)}
        d['tau']=vals[0]; d['a']=vals[1]
        rr.append(d)
    if len(rr)<3: raise RuntimeError(f'too few rows in {path}')
    return rr


def interp(rr,a):
    if not (rr[0]['a']<=a<=rr[-1]['a']):
        raise RuntimeError(f'a={a} outside support [{rr[0]["a"]},{rr[-1]["a"]}]')
    lo=0; hi=len(rr)-1
    while hi-lo>1:
        m=(lo+hi)//2
        if rr[m]['a']<=a: lo=m
        else: hi=m
    x0,x1=rr[lo],rr[hi]
    f=(a-x0['a'])/(x1['a']-x0['a']) if x1['a']!=x0['a'] else 0.0
    return {key:x0[key]+f*(x1[key]-x0[key]) for key in x0}


def relmax(vals,scalevals):
    return max(abs(v) for v in vals)/max(max(abs(x) for x in scalevals),1e-300)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--glob',dest='pattern',required=True); ap.add_argument('--output',required=True); args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]
    target=json.loads((root/'research/theory_targets/RTK_C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_TARGET_v1.json').read_text())
    parent=json.loads((root/'research/theory_results/RTK_C10_PHYSICAL_CLASS_SOURCE_EXPORT_RESULT_v1.json').read_text())
    assert target['status']=='FROZEN_BEFORE_EXECUTION'
    assert parent['classification']=='C10_PHYSICAL_CLASS_SOURCE_EXPORT_PASS'
    a_on=float(target['sample']['a'])
    expected=[float(x) for x in target['sample']['k_Mpc_inv']]
    fs=sorted(glob.glob(args.pattern))
    if len(fs)!=len(expected): raise RuntimeError(f'expected {len(expected)} histories, got {len(fs)}')
    samples=[]
    for f in fs:
        rr=read_rows(f); z=interp(rr,a_on)
        k=sum(x['c10_k_Mpc_inv'] for x in rr)/len(rr)
        samples.append((k,z,f))
    samples.sort(key=lambda x:x[0])
    for (k,_,_),ke in zip(samples,expected):
        if abs(k-ke)>1e-10*max(1.0,abs(ke)): raise RuntimeError(f'k mismatch {k} vs {ke}')

    recs=[]; all_finite=True
    for k,z,f in samples:
        dg=z['c10_65a_delta_g']; db=z['c10_65a_delta_b']; du=z['c10_65a_delta_ur']
        tg=z['c10_65a_theta_g']; tb=z['c10_65a_theta_b']; tu=z['c10_65a_theta_ur']
        sg=z['c10_65a_shear_g']; su=z['c10_65a_shear_ur']; phi=z['c10_65a_CLASS_phi_curvature']; psi=z['c10_65a_CLASS_psi_lapse']
        Dg=dg-4.0*phi; Db=db-3.0*phi; Du=du-4.0*phi
        eps_d=relmax([Dg-(4.0/3.0)*Db,Du-Dg],[Dg,(4.0/3.0)*Db,Du])
        eps_v=relmax([tg-tb,tu-tg],[tg,tb,tu])
        raw_d=relmax([dg-(4.0/3.0)*db,du-dg],[dg,(4.0/3.0)*db,du])
        vals=[dg,db,du,tg,tb,tu,sg,su,phi,psi,Dg,Db,Du,eps_d,eps_v,raw_d]
        all_finite=all_finite and all(math.isfinite(v) for v in vals)
        recs.append({
          'k_Mpc_inv':k,'a':a_on,'tau_Mpc':z['tau'],
          'delta_g':dg,'theta_g':tg,'shear_g':sg,'delta_b':db,'theta_b':tb,
          'CLASS_psi_lapse':psi,'CLASS_phi_curvature':phi,
          'delta_ur':du,'theta_ur':tu,'shear_ur':su,
          'D_g':Dg,'D_b':Db,'D_ur':Du,
          'epsilon_density_curvature_dressed':eps_d,
          'epsilon_density_raw':raw_d,
          'epsilon_velocity':eps_v,
          'theta_g_over_k2':tg/(k*k),'theta_b_over_k2':tb/(k*k),'theta_ur_over_k2':tu/(k*k),
          'shear_g_over_k2':sg/(k*k),'shear_ur_over_k2':su/(k*k),
          'source_file':Path(f).name
        })

    low=recs[0]
    control_ok=all_finite and low['epsilon_density_curvature_dressed']<1e-3 and low['epsilon_velocity']<1e-2
    cls=('C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_CONSISTENT_PASS_SCOPED' if control_ok else
         'C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_DEVIATION_SCOPED')
    out={
      'schema':'RTK_C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_RESULT_v1',
      'classification':cls,
      'scope':target['scope'],
      'target':'research/theory_targets/RTK_C10_65A_BASELINE_RADIATION_SPECIES_CONTROL_TARGET_v1.json',
      'pinned_class_upstream_sha':target['pinned_class_upstream_sha'],
      'technical':{'history_count':len(recs),'all_finite':all_finite,'a_on':a_on,'k_values_Mpc_inv':[r['k_Mpc_inv'] for r in recs]},
      'low_k_control':{
        'k_Mpc_inv':low['k_Mpc_inv'],
        'epsilon_density_curvature_dressed':low['epsilon_density_curvature_dressed'],
        'epsilon_velocity':low['epsilon_velocity'],
        'density_threshold':1e-3,'velocity_threshold':1e-2,'pass':control_ok
      },
      'records':recs,
      'interpretation':('This is a read-only historical action-fluid CLASS control for baryon/photon/massless-UR signs, normalizations and superhorizon adiabatic ratios. It is not imported as the completed-U1 solution. C10.65b must independently solve the preferred-coordinate completed DAE gradient system and may use these values only as a regression/control comparison.'),
      'next_gate':'C10.65b completed-U1 O(k^2) radiation+neutral-Khronon gradient/rank solve with I_khr(tau_on)=0 on the adiabatic branch; solve B0 from N2/C2 rather than prescribe chi/B.',
      'non_claims':target['non_claims']
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls,json.dumps(out['low_k_control'],sort_keys=True))

if __name__=='__main__': main()
