#!/usr/bin/env python3
"""Compute RTK GW/EM luminosity-distance ratio from a CLASS background file.

For the pinned nonlocal CLASS RT branch (model=2), the tensor equation is

  h'' + [2 a H - 3 H0^2 gamma V] h' + k^2 h = source,

so relative to h''+2 Hconf(1-delta)h'+k^2 h=source,

  delta(z) = 3 H0^2 gamma V(z) / [2 a(z) H(z)].

For luminal GW speed, the sub-horizon standard-siren amplitude obeys

  dL_gw/dL_em = exp[- int_0^z delta(z')/(1+z') dz'].

This script evaluates that prediction directly from the exact CLASS background.
It does not add a GW likelihood and does not modify the frozen cosmology fit.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import numpy as np


def parse_titles(path: Path) -> dict[str, int]:
    # CLASS background files contain a numbered title line, e.g.
    # '# 1:z 2:proper time [Gyr] ... 13:U 14:U_prime 15:V ...'.
    comments=[]
    with path.open() as f:
        for line in f:
            if not line.startswith('#'):
                break
            comments.append(line.rstrip())
    text='\n'.join(comments)
    pairs=re.findall(r'(\d+):(.+?)(?=\s+\d+:|$)',text.replace('\n',' '))
    out={name.strip():int(num)-1 for num,name in pairs}
    required=('z','H [1/Mpc]','V')
    missing=[k for k in required if k not in out]
    if missing:
        raise RuntimeError(f'failed to parse CLASS background titles {missing}; parsed={out}')
    return out


def cumulative_trapezoid(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    out=np.zeros_like(x,dtype=float)
    if len(x)>1:
        out[1:]=np.cumsum(0.5*(y[1:]+y[:-1])*(x[1:]-x[:-1]))
    return out


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--background',required=True)
    ap.add_argument('--gamma',required=True,type=float)
    ap.add_argument('--H0',required=True,type=float,help='CLASS H0 in 1/Mpc')
    ap.add_argument('--output',default='gw_standard_siren.json')
    args=ap.parse_args()

    path=Path(args.background)
    titles=parse_titles(path)
    arr=np.loadtxt(path)
    if arr.ndim==1:
        arr=arr.reshape(1,-1)
    z=arr[:,titles['z']]
    H=arr[:,titles['H [1/Mpc]']]
    V=arr[:,titles['V']]
    mask=np.isfinite(z)&np.isfinite(H)&np.isfinite(V)&(z>=-1e-10)&(H>0)
    z=z[mask];H=H[mask];V=V[mask]
    order=np.argsort(z)
    z=z[order];H=H[order];V=V[order]
    # Remove any exact duplicate redshifts conservatively.
    keep=np.ones(len(z),dtype=bool)
    if len(z)>1:
        keep[1:]=np.diff(z)>0
    z=z[keep];H=H[keep];V=V[keep]
    if len(z)<3:
        raise RuntimeError('insufficient background rows')
    if abs(float(z[0]))>1e-7:
        raise RuntimeError(f'background does not reach z=0: zmin={z[0]}')
    z[0]=0.0

    a=1.0/(1.0+z)
    delta=3.0*args.H0*args.H0*args.gamma*V/(2.0*a*H)
    integrand=delta/(1.0+z)
    integ=cumulative_trapezoid(z,integrand)
    ratio=np.exp(-integ)

    targets=[0.0,0.1,0.38,0.51,0.61,1.0,2.0,5.0]
    targets=[t for t in targets if t<=float(z[-1])]
    rows=[]
    for t in targets:
        rows.append({
            'z':t,
            'delta_friction':float(np.interp(t,z,delta)),
            'dL_gw_over_dL_em':float(np.interp(t,z,ratio)),
            'fractional_difference':float(np.interp(t,z,ratio)-1.0),
        })

    result={
        'classification':'RTK_CURRENT_CENTER_STANDARD_SIREN_PREDICTION',
        'gamma':args.gamma,
        'H0_class_1_per_Mpc':args.H0,
        'equation':"h''+[2*a*H-3*H0^2*gamma*V]h'+k^2 h=source",
        'c_gw_over_c':1.0,
        'delta_definition':'3*H0^2*gamma*V/(2*a*H)',
        'distance_ratio_definition':'exp[-integral_0^z delta(z)/(1+z) dz]',
        'background_z_max':float(z[-1]),
        'delta_min':float(np.min(delta)),
        'delta_max':float(np.max(delta)),
        'ratio_min':float(np.min(ratio)),
        'ratio_max':float(np.max(ratio)),
        'targets':rows,
        'claim_boundary':{
            'current_center_prediction_only':True,
            'not_a_GW_likelihood':True,
            'not_a_new_fit':True,
            'frozen_scalar_objective_unchanged':True,
            'primordial_tensor_sector_not_claimed_complete':True,
        },
    }
    Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('RTK_STANDARD_SIREN_PREDICTION_COMPLETE',json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
