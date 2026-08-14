#!/usr/bin/env python3
from pathlib import Path
from bisect import bisect_left
import math


def load(path):
    rows=[]
    for line in Path(path).read_text().splitlines():
        s=line.strip()
        if s and not s.startswith('#'): rows.append([float(x) for x in s.split()])
    return rows

def interp(x,xs,ys):
    if x<=xs[0]: return ys[0]
    if x>=xs[-1]: return ys[-1]
    i=bisect_left(xs,x); x0,x1=xs[i-1],xs[i]; y0,y1=ys[i-1],ys[i]
    return y0+(y1-y0)*(x-x0)/(x1-x0)

def ratio_table(model,control,col=1):
    cx=[r[0] for r in control]; cy=[r[col] for r in control]
    lo=max(model[0][0],control[0][0]); hi=min(model[-1][0],control[-1][0])
    out=[]
    for r in model:
        if lo<=r[0]<=hi:
            c=interp(r[0],cx,cy)
            if c!=0: out.append((r[0],r[col]/c))
    return out

def sample(tab,x): return interp(x,[r[0] for r in tab],[r[1] for r in tab])

out=Path('output')
lpk=load(out/'lcdm_pk.dat'); lcl=load(out/'lcdm_cl.dat')
models=[('lambda=10000','rtk'),('lambda=15000','rtk15')]
print('model,k0.01,k0.05,k0.1,k0.2,k0.5,ell2,ell30,ell200,ell500,ell1000')
for label,prefix in models:
    pk=ratio_table(load(out/f'{prefix}_pk.dat'),lpk)
    cl=ratio_table(load(out/f'{prefix}_cl.dat'),lcl)
    vals=[]
    for k in [0.01,0.05,0.1,0.2,0.5]: vals.append(sample(pk,k) if pk[0][0]<=k<=pk[-1][0] else float('nan'))
    for L in [2,30,200,500,1000]: vals.append(sample(cl,L) if cl[0][0]<=L<=cl[-1][0] else float('nan'))
    print(label+','+','.join(f'{v:.9g}' for v in vals))
