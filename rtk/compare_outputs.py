#!/usr/bin/env python3
from pathlib import Path
import numpy as np

out=Path('output')
rcl=np.loadtxt(out/'rtk_cl.dat')
lcl=np.loadtxt(out/'lcdm_cl.dat')
rpk=np.loadtxt(out/'rtk_pk.dat')
lpk=np.loadtxt(out/'lcdm_pk.dat')

# Interpolate controls onto RTK grids if necessary.
ell=rcl[:,0]
clcols=min(rcl.shape[1],lcl.shape[1])
clrows=[ell]
for j in range(1,clcols):
    control=np.interp(ell,lcl[:,0],lcl[:,j])
    ratio=np.divide(rcl[:,j],control,out=np.full_like(control,np.nan),where=np.abs(control)>0)
    clrows.append(ratio)
np.savetxt(out/'rtk_over_lcdm_cl.dat',np.column_stack(clrows),header='ell ratios of CLASS Cl columns: RTK/LCDM')

k=rpk[:,0]
control_pk=np.interp(k,lpk[:,0],lpk[:,1])
ratio_pk=rpk[:,1]/control_pk
np.savetxt(out/'rtk_over_lcdm_pk.dat',np.column_stack([k,ratio_pk]),header='k[h/Mpc] P_RTK/P_LCDM')

samples=[0.01,0.05,0.1,0.2,0.5,1.0]
print('P(k) ratio samples')
for q in samples:
    if q <= k[-1]:
        print(f'k={q:.3g} ratio={np.interp(q,k,ratio_pk):.9g}')
print('finite_pk=',bool(np.isfinite(ratio_pk).all()))
print('pk_ratio_min=',float(np.nanmin(ratio_pk)),'max=',float(np.nanmax(ratio_pk)))
# TT is column 1 in CLASS cl.dat.
tt=lcl[:,1]
rtt=np.interp(lcl[:,0],rcl[:,0],rcl[:,1])
mask=np.abs(tt)>0
rr=np.divide(rtt,tt,out=np.full_like(tt,np.nan),where=mask)
for L in [2,30,200,500,1000]:
    if L <= lcl[-1,0]: print(f'ell={L} TT_ratio={np.interp(L,lcl[:,0],rr):.9g}')
