#!/usr/bin/env python3
"""Evaluate official Planck 2018 baseline CMB likelihood pieces with clipy.

Fixed calibration/nuisance values are taken from each likelihood's distributed
self-test/default vector. Thus this is an official-likelihood fixed-parameter
comparison, not yet a nuisance-profiled cosmological parameter fit.
"""
from pathlib import Path
import csv, math, os, sys
os.environ.setdefault('CLIPY_NOJAX','1')
import numpy as np
import clipy

PLANCK=Path(sys.argv[1]) if len(sys.argv)>1 else Path('planck_data')
BASE=PLANCK/'baseline'
OUT=Path('output')
TCMB=2.7255
UK2=(TCMB*1.0e6)**2
MODELS=[
 ('LCDM',None,'planck_lcdm_'),
 ('RTK',1000.0,'planck_rtk1_'),
 ('RTK',2000.0,'planck_rtk2_'),
 ('RTK',3000.0,'planck_rtk3_'),
]
FILES={
 'lowT': BASE/'plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik',
 'lowE': BASE/'plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik',
 'high': BASE/'plc_3.0/hi_l/plik_lite/plik_lite_v22_TTTEEE.clik',
}
for name,p in FILES.items():
    if not p.exists(): raise SystemExit(f'MISSING_PLANCK_LIKELIHOOD {name} {p}')

likes={name:clipy.clik(str(p)) for name,p in FILES.items()}


def load_cls(prefix):
    p=OUT/f'{prefix}cl_lensed.dat'
    if not p.exists(): raise RuntimeError(f'missing lensed CLASS spectrum {p}')
    vals={}
    for line in p.read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        a=s.split(); ell=int(float(a[0]))
        dl=[float(x) for x in a[1:5]]
        fac=2.0*math.pi/(ell*(ell+1.0))*UK2
        # CLASS columns are TT, EE, TE, BB; clik ordering is TT, EE, BB, TE, TB, EB.
        vals[ell]=(dl[0]*fac,dl[1]*fac,dl[3]*fac,dl[2]*fac,0.0,0.0)
    if max(vals)<2508: raise RuntimeError(f'CLASS lmax too small: {max(vals)}')
    return vals


def clik_vector(L,cls):
    lmax=list(L.get_lmax())
    v=np.array(L.default_par,dtype=float,copy=True)
    off=0
    for spec,lm in enumerate(lmax):
        if lm<0: continue
        arr=np.zeros(lm+1,dtype=float)
        for ell in range(2,lm+1):
            arr[ell]=cls[ell][spec]
        v[off:off+lm+1]=arr
        off += lm+1
    return v

rows=[]
for model,lam,prefix in MODELS:
    cls=load_cls(prefix)
    parts={}
    for name,L in likes.items():
        val=float(np.asarray(L(clik_vector(L,cls))).reshape(-1)[0])
        parts[name]=val
    total=sum(parts.values())
    rows.append({'model':model,'lambda_D':'' if lam is None else lam,
                 'loglike_lowT':parts['lowT'],'loglike_lowE':parts['lowE'],
                 'loglike_high_pliklite':parts['high'],'loglike_total':total,
                 'minus2logL_total':-2.0*total})
ref=rows[0]['loglike_total']
for r in rows:
    r['delta_minus2logL_vs_LCDM']=-2.0*(r['loglike_total']-ref)

with (OUT/'planck_official_fixed_summary.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

print('PLANCK_OFFICIAL_FIXED_LIKELIHOOD')
print('Nuisance/calibration values are fixed to the official likelihood self-test/default vector; this is not yet a nuisance-profiled fit.')
print('model lambda logL_lowT logL_lowE logL_high delta(-2lnL)')
for r in rows:
    lam='-' if r['lambda_D']=='' else f"{float(r['lambda_D']):.0f}"
    print(f"{r['model']:4s} {lam:6s} {r['loglike_lowT']:12.5f} {r['loglike_lowE']:12.5f} {r['loglike_high_pliklite']:14.5f} {r['delta_minus2logL_vs_LCDM']:14.5f}")
print('PLANCK_OFFICIAL_FIXED_PASS')
