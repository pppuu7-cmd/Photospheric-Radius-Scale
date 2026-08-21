#!/usr/bin/env python3
"""Evaluate the normalization-independent tensor-null diagnostic Q_cosm(a).

For the production DBI-Khronon background,

    K_phys = M_cosm^2 K_8piG = 2 M_cosm^2 M_K^2,

so define

    Q_cosm(a) := K_phys/(H^2 M_cosm^2) = 2 M_K(a)^2/H(a)^2.

For a fixed carrier with time-independent gravitational-normalization ratio

    xi := M_cosm^2/M_*^2,

its grad-K tensor-null variable is

    R_*(a) = K_phys/(H^2 M_*^2) = xi Q_cosm(a).

The exact scalar grad-K tensor-null theorem requires R_*(a)=2.  Therefore a
necessary condition for tensor-null matching over more than one epoch is that
Q_cosm(a) be constant.  This script evaluates Q_cosm on the frozen production
redshift grid using the exact CLASS background H and the exact production M_K
state functions.  It does not choose xi and therefore does not conflate bare,
cosmological, or Newton gravitational normalizations.
"""

from __future__ import annotations
import argparse
import json
import math
import re
from pathlib import Path
import numpy as np


def parse_titles(path: Path) -> dict[str,int]:
    comments=[]
    with path.open() as f:
        for line in f:
            if not line.startswith('#'):
                break
            comments.append(line.rstrip())
    text=' '.join(comments)
    pairs=re.findall(r'(\d+):(.+?)(?=\s+\d+:|$)',text)
    out={name.strip():int(num)-1 for num,name in pairs}
    for key in ('z','H [1/Mpc]'):
        if key not in out:
            raise RuntimeError(f'missing CLASS background column {key}; parsed={out}')
    return out


def closure(H0:float,gamma:float,lambda_D:float,Omega_K0:float):
    if not (H0>0 and gamma>0 and lambda_D>0 and Omega_K0>0):
        raise ValueError('positive H0,gamma,lambda_D,Omega_K0 required')
    muK=3.0*H0*math.sqrt(gamma)
    A=Omega_K0/(6.0*gamma)
    if abs(lambda_D-1.0)<64.0*2.220446049250313e-16:
        x0=A*(A+2.0)/(2.0*(A+1.0))
    else:
        D=1.0+2.0*A+lambda_D*A*A
        x0=A*(2.0+lambda_D*A)/(1.0+lambda_D*A+math.sqrt(D))
    if not (muK>0 and x0>0 and math.isfinite(muK) and math.isfinite(x0)):
        raise ValueError('nonphysical closure')
    return muK,x0


def MK_at_a(muK:float,x0:float,lambda_D:float,a:float)->float:
    x=x0/a**3
    s=math.hypot(1.0,math.sqrt(lambda_D)*x)
    MK=muK*math.sqrt(s)*(s+x)
    if not (MK>0 and math.isfinite(MK)):
        raise ValueError('nonphysical M_K')
    return MK


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--background',required=True)
    ap.add_argument('--gamma',type=float,required=True)
    ap.add_argument('--H0',type=float,required=True)
    ap.add_argument('--lambda-D',type=float,required=True)
    ap.add_argument('--Omega-K0',type=float,required=True)
    ap.add_argument('--z-grid',required=True)
    ap.add_argument('--output',default='gradk_tensor_ratio_dictionary.json')
    args=ap.parse_args()

    zs=[float(q) for q in args.z_grid.split(',') if q.strip()]
    if not zs or any(z<0 for z in zs):
        raise SystemExit('invalid z grid')

    path=Path(args.background)
    titles=parse_titles(path)
    arr=np.loadtxt(path)
    if arr.ndim==1:
        arr=arr.reshape(1,-1)
    z_bg=arr[:,titles['z']]
    H_bg=arr[:,titles['H [1/Mpc]']]
    mask=np.isfinite(z_bg)&np.isfinite(H_bg)&(z_bg>=-1e-10)&(H_bg>0)
    z_bg=z_bg[mask]; H_bg=H_bg[mask]
    order=np.argsort(z_bg)
    z_bg=z_bg[order]; H_bg=H_bg[order]
    keep=np.ones(len(z_bg),dtype=bool)
    if len(z_bg)>1:
        keep[1:]=np.diff(z_bg)>0
    z_bg=z_bg[keep]; H_bg=H_bg[keep]
    if len(z_bg)<10:
        raise RuntimeError('insufficient CLASS background rows')
    if min(zs)<z_bg[0]-1e-8 or max(zs)>z_bg[-1]+1e-8:
        raise RuntimeError(f'z grid outside background [{z_bg[0]},{z_bg[-1]}]')

    muK,x0=closure(args.H0,args.gamma,args.lambda_D,args.Omega_K0)
    rows=[]
    for z in zs:
        a=1.0/(1.0+z)
        H=float(np.interp(z,z_bg,H_bg))
        MK=MK_at_a(muK,x0,args.lambda_D,a)
        Q=2.0*(MK/H)**2
        rows.append({
            'z':z,'a':a,'H_1_per_Mpc':H,'M_K_1_per_Mpc':MK,
            'M_K_over_H':MK/H,'Q_cosm_2MK2_over_H2':Q,
        })

    vals=np.array([r['Q_cosm_2MK2_over_H2'] for r in rows],dtype=float)
    qmin=float(vals.min()); qmax=float(vals.max())
    frac_span=(qmax-qmin)/max(abs(qmin),1e-300)
    endpoint_ratio=float(vals[-1]/vals[0])
    # Tensor-null with any constant xi needs Q_cosm exactly constant.  Use a
    # deliberately weak numerical non-constancy guard: >1e-6 relative span.
    # The actual result is expected to be far larger; this avoids mistaking
    # interpolation noise for physics.
    nonconstant=bool(frac_span>1e-6)

    out={
        'classification':'RTK_ROUTE_B_GRADK_TENSOR_RATIO_DICTIONARY',
        'definition':'Q_cosm(a)=2 M_K(a)^2/H(a)^2',
        'relation_to_tensor_null':'R_*(a)=xi Q_cosm(a), xi=M_cosm^2/M_*^2 constant; exact tensor-null over all tested epochs requires Q_cosm constant',
        'inputs':{
            'gamma':args.gamma,'H0_1_per_Mpc':args.H0,
            'lambda_D':args.lambda_D,'Omega_K0':args.Omega_K0,
            'z_grid':zs
        },
        'closure':{'muK_1_per_Mpc':muK,'x0':x0},
        'rows':rows,
        'summary':{
            'Q_min':qmin,'Q_max':qmax,'relative_span_over_min':frac_span,
            'Q_last_over_Q_first':endpoint_ratio,
            'constant_xi_tensor_null_possible_on_grid':not nonconstant,
            'nonconstant_threshold_relative_span':1e-6
        },
        'interpretation':(
            'If constant_xi_tensor_null_possible_on_grid is false, then no fixed time-independent bare-to-cosmological gravitational normalization can keep the exact grad-K scalar carrier tensor-null across the frozen production redshift grid. This does not exclude time-dependent gravitational normalization, tensor-only companion cancellation, or another carrier.'
        )
    }
    if nonconstant:
        out['classification']='RTK_ROUTE_B_GRADK_TENSOR_NULL_CONSTANT_NORMALIZATION_FAIL'
    else:
        out['classification']='RTK_ROUTE_B_GRADK_TENSOR_NULL_CONSTANT_NORMALIZATION_NOT_EXCLUDED'
    Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['classification'],json.dumps(out,sort_keys=True))

if __name__=='__main__':
    main()
