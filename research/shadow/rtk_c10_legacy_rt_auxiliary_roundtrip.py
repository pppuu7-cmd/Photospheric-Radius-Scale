#!/usr/bin/env python3
"""Frozen C10 audit of the legacy RT 00/0i comoving-source constraint.

The historical model-2 CLASS evolution uses 0i + traceless/trace equations.  This
script independently reconstructs the RT 00 auxiliary contribution and tests the
comoving-source identity on read-only perturbation histories.
"""
from __future__ import annotations

import argparse, glob, json, math
from pathlib import Path
import numpy as np

BASE=[
 'c10_k_Mpc_inv','c10_Hc','c10_Hc_prime','c10_H0_ord','c10_H0_ord_prime',
 'c10_H0_ord_double_prime','c10_deltaH0_ord','c10_delta_mu_total',
 'c10_rpp_theta_total','c10_delta_p_total','c10_rpp_shear_total','c10_W_total',
 'c10_rho_total_prime','c10_p_total_prime','c10_khr_w','c10_khr_ca2']
DIRECT=['c10_Ccom_direct','c10_Ccom_over_k2_direct','c10_dZ_nlde',
        'c10_dZ_prime_nlde','c10_dV_nlde','c10_V_bg_nlde','c10_model2_0i_aux']
RT=['c10_dU_nlde','c10_dV_prime_nlde','c10_V_bg_prime_nlde','c10_phi_CLASS',
    'c10_psi_CLASS','c10_phi_prime_CLASS','c10_gamma','c10_H0_Mpc_inv']
ALL=BASE+DIRECT+RT


def medabs(x):
    return float(np.median(np.abs(np.asarray(x,dtype=float))))


def read_table(path):
    text=Path(path).read_text()
    miss=[x for x in ALL if x not in text]
    if miss:
        raise RuntimeError(f'missing columns {miss} in {path}')
    arr=np.loadtxt(path)
    if arr.ndim==1:
        arr=arr[None,:]
    if arr.shape[1] < len(ALL)+2:
        raise RuntimeError(f'too few columns in {path}: {arr.shape}')
    tail=arr[:,-len(ALL):]
    cols={name:tail[:,i] for i,name in enumerate(ALL)}
    tau=arr[:,0]; a=arr[:,1]
    if not np.all(np.diff(tau)>0) or not np.all(np.diff(a)>0):
        raise RuntimeError(f'non-monotonic tau/a in {path}')
    return {'path':path,'tau':tau,'a':a,'cols':cols,'k':float(np.mean(cols['c10_k_Mpc_inv']))}


def local_poly(tau,y,t0,n,deg):
    n=min(n,len(tau))
    idx=np.argsort(np.abs(tau-t0))[:n]
    idx=np.sort(idx)
    x=tau[idx]-t0
    scale=max(float(np.max(np.abs(x))),1e-30)
    z=x/scale
    co=np.polyfit(z,np.asarray(y)[idx],deg)
    val=float(np.polyval(co,0.0))
    dco=np.polyder(co)
    der=float(np.polyval(dco,0.0)/scale)
    return val,der


def state_at(tab,a0):
    tau0=float(np.interp(a0,tab['a'],tab['tau']))
    vals={}
    for name,y in tab['cols'].items():
        vals[name]=local_poly(tab['tau'],y,tau0,6,3)[0]
    psi=tab['cols']['c10_psi_CLASS']
    _,psip3=local_poly(tab['tau'],psi,tau0,6,3)
    _,psip4=local_poly(tab['tau'],psi,tau0,10,4)
    phi=tab['cols']['c10_phi_CLASS']
    _,phip_fit=local_poly(tab['tau'],phi,tau0,6,3)
    vals['psi_prime_cubic6']=psip3
    vals['psi_prime_quartic10']=psip4
    vals['phi_prime_cubic6']=phip_fit
    vals['tau']=tau0
    return vals


def evaluate_one(tab,a0):
    v=state_at(tab,a0)
    a=float(a0); k=float(tab['k'])
    Hc=v['c10_Hc']; C=v['c10_Ccom_direct']; phi=v['c10_phi_CLASS']; psi=v['c10_psi_CLASS']
    dU=v['c10_dU_nlde']; dV=v['c10_dV_nlde']; dVp=v['c10_dV_prime_nlde']
    V=v['c10_V_bg_nlde']; Vp=v['c10_V_bg_prime_nlde']
    gamma=v['c10_gamma']; H0=v['c10_H0_Mpc_inv']; A0i=v['c10_model2_0i_aux']

    observed=C + 2.0*k*k*phi/(3.0*a*a)

    def pred(psip):
        B00=(dU - dVp/(a*a) + Hc*dV/(a*a)
             +2.0*psi*Vp/(a*a) -2.0*Hc*psi*V/(a*a) + psip*V/(a*a))
        p=-gamma*H0*H0*B00 - 2.0*Hc*A0i/(a*a)
        return B00,p,observed-p

    B3,p3,r3=pred(v['psi_prime_cubic6'])
    B4,p4,r4=pred(v['psi_prime_quartic10'])
    phip_direct=v['c10_phi_prime_CLASS']
    return {
      'k':k,'tau':v['tau'],'C_com':C,'phi_CLASS':phi,'psi_CLASS':psi,
      'observed_aux_required':observed,
      'B00_cubic6':B3,'predicted_aux_cubic6':p3,'roundtrip_residual_cubic6':r3,
      'B00_quartic10':B4,'predicted_aux_quartic10':p4,'roundtrip_residual_quartic10':r4,
      'psi_prime_cubic6':v['psi_prime_cubic6'],'psi_prime_quartic10':v['psi_prime_quartic10'],
      'phi_prime_direct':phip_direct,'phi_prime_cubic6':v['phi_prime_cubic6'],
      'phi_prime_derivative_abs_difference':abs(phip_direct-v['phi_prime_cubic6']),
      'A0i_code':A0i,'gamma':gamma,'H0_Mpc_inv':H0,
      'dU':dU,'dV':dV,'dVprime':dVp,'Vbg':V,'Vbgprime':Vp,
    }


def nearest(points,k0):
    return min(points,key=lambda q:abs(q['k']-k0))


def epoch_metrics(points,target,a0,binding):
    small=[nearest(points,float(k)) for k in target['binding_smallest_four_Mpc_inv']]
    obs=medabs([q['observed_aux_required'] for q in small])
    pred=medabs([q['predicted_aux_cubic6'] for q in small])
    rr=medabs([q['roundtrip_residual_cubic6'] for q in small])
    deriv=medabs([q['roundtrip_residual_cubic6']-q['roundtrip_residual_quartic10'] for q in small])
    den=max(obs,1e-300)
    m={
      'a':a0,'binding':binding,'observed_aux_median_abs':obs,'predicted_aux_median_abs':pred,
      'roundtrip_median_abs':rr,'roundtrip_over_observed':rr/den,
      'predicted_over_observed':pred/den,
      'psi_prime_estimator_roundtrip_difference_median_abs':deriv,
      'psi_prime_estimator_difference_over_observed':deriv/den,
      'smallest_four':small,
    }
    if binding:
        lim=target['frozen_acceptance_per_binding_epoch']
        m['passed']=(
          m['roundtrip_over_observed'] <= float(lim['median_roundtrip_abs_over_median_observed_aux_abs_max']) and
          float(lim['predicted_aux_median_abs_over_observed_aux_median_abs_min']) <= m['predicted_over_observed'] <= float(lim['predicted_aux_median_abs_over_observed_aux_median_abs_max']) and
          m['psi_prime_estimator_difference_over_observed'] <= float(lim['psi_prime_estimator_induced_roundtrip_difference_over_observed_aux_median_abs_max'])
        )
    else:
        m['passed']=None
    return m


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--glob',required=True)
    ap.add_argument('--target',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    target=json.load(open(args.target))
    tabs=sorted([read_table(p) for p in glob.glob(args.glob)],key=lambda t:t['k'])
    req=[float(x) for x in target['k_ladder_Mpc_inv']]
    if len(tabs)!=len(req):
        raise SystemExit(f'expected {len(req)} tables got {len(tabs)}')
    for t,k in zip(tabs,req):
        if abs(t['k']-k)>1e-12*max(1.0,abs(k)):
            raise SystemExit(f'k mismatch {t["k"]} {k}')

    epochs=[]
    bind=set(float(x) for x in target['binding_late_scale_factors'])
    all_a=[float(x) for x in target['diagnostic_early_scale_factors']]+[float(x) for x in target['binding_late_scale_factors']]
    for a0 in all_a:
        pts=[evaluate_one(t,a0) for t in tabs]
        epochs.append(epoch_metrics(pts,target,a0,a0 in bind))

    binding=[e for e in epochs if e['binding']]
    cls=(target['decision_rule']['both_binding_epochs_pass'] if all(e['passed'] for e in binding)
         else target['decision_rule']['otherwise'])
    out={
      'schema':'RTK_C10_LEGACY_RT_AUXILIARY_COMOVING_CONSTRAINT_RESULT_v1',
      'classification':cls,'epochs':epochs,
      'binding_pass_count':sum(bool(e['passed']) for e in binding),'binding_epoch_count':len(binding),
      'actual_k_values_Mpc_inv':[t['k'] for t in tabs],
      'parent_confirmatory_fail_retained':True,'production_modified':False,'completion_parameters_selected':False,
      'target':args.target,
      'interpretation_guard':'This is a read-only legacy RT constraint round-trip. It does not subtract anything from production and does not reclassify the parent completed-U1 source-compatibility FAIL.'
    }
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(cls)
    for e in epochs:
        print('EPOCH',e['a'],'binding=',e['binding'],'pass=',e['passed'],
              'roundtrip/obs=',e['roundtrip_over_observed'],
              'pred/obs=',e['predicted_over_observed'],
              'dpsi/obs=',e['psi_prime_estimator_difference_over_observed'])

if __name__=='__main__':
    main()
