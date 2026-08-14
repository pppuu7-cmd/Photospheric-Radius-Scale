#!/usr/bin/env python3
from pathlib import Path
from bisect import bisect_left
import math
import re


def load_table(path):
    rows=[]
    for line in Path(path).read_text().splitlines():
        line=line.strip()
        if not line or line.startswith('#'): continue
        rows.append([float(x) for x in line.split()])
    return rows


def interp(x, xs, ys):
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    i=bisect_left(xs,x)
    x0,x1=xs[i-1],xs[i]; y0,y1=ys[i-1],ys[i]
    return y0+(y1-y0)*(x-x0)/(x1-x0)


def save(path, header, rows):
    with Path(path).open('w') as f:
        f.write('# '+header+'\n')
        for row in rows:
            f.write(' '.join(f'{v:.12e}' for v in row)+'\n')


def z_of(path):
    for line in Path(path).read_text().splitlines()[:8]:
        m=re.search(r'redshift z=([+\-0-9.eE]+)',line)
        if m: return float(m.group(1))
    return None


def pk_at_z0(out,prefix):
    single=out/(prefix+'pk.dat')
    if single.exists(): return single
    for p in sorted(out.glob(prefix+'z*_pk.dat')):
        z=z_of(p)
        if z is not None and abs(z)<1e-12: return p
    raise RuntimeError('z=0 P(k) file not found for '+prefix)

out=Path('output')
rcl=load_table(out/'rtk_cl.dat'); lcl=load_table(out/'lcdm_cl.dat')
rpk=load_table(pk_at_z0(out,'rtk_')); lpk=load_table(pk_at_z0(out,'lcdm_'))

# Only compare within the common domain; no extrapolated extrema.
kmin=max(rpk[0][0],lpk[0][0]); kmax=min(rpk[-1][0],lpk[-1][0])
lkx=[r[0] for r in lpk]; lkP=[r[1] for r in lpk]
pkrows=[]
for row in rpk:
    k,P=row[0],row[1]
    if kmin <= k <= kmax:
        ctl=interp(k,lkx,lkP)
        if ctl != 0.0: pkrows.append([k,P/ctl])
save(out/'rtk_over_lcdm_pk.dat','k[h/Mpc] P_RTK/P_LCDM at z=0',pkrows)

ellmin=max(rcl[0][0],lcl[0][0]); ellmax=min(rcl[-1][0],lcl[-1][0])
clcols=min(len(rcl[0]),len(lcl[0])); lxs=[r[0] for r in lcl]
clrows=[]
for rr in rcl:
    L=rr[0]
    if ellmin <= L <= ellmax:
        vals=[L]
        for j in range(1,clcols):
            ctl=interp(L,lxs,[r[j] for r in lcl])
            vals.append(rr[j]/ctl if ctl != 0.0 else float('nan'))
        clrows.append(vals)
save(out/'rtk_over_lcdm_cl.dat','ell ratios of CLASS Cl columns: RTK/LCDM',clrows)

pkx=[r[0] for r in pkrows]; pkr=[r[1] for r in pkrows]
print('P(k,z=0) ratio samples')
for q in [0.01,0.05,0.1,0.2,0.5,1.0]:
    if pkx and pkx[0] <= q <= pkx[-1]: print(f'k={q:.3g} ratio={interp(q,pkx,pkr):.9g}')
print('finite_pk=',all(math.isfinite(x) for x in pkr))
print('pk_ratio_min=',min(pkr),'max=',max(pkr))

# TT is column 1.
ttx=[r[0] for r in clrows]; ttr=[r[1] for r in clrows]
print('TT ratio samples')
for L in [2,10,30,100,200,500,1000,1200]:
    if ttx and ttx[0] <= L <= ttx[-1]: print(f'ell={L} TT_ratio={interp(L,ttx,ttr):.9g}')
