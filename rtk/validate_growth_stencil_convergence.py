#!/usr/bin/env python3
"""Compare 3-point and 5-point local derivatives for RTK scale-dependent growth.

Uses the same CLASS P(k,z) family and log-log k interpolation as
export_growth_scale_dependence.py.  This is a numerical convergence diagnostic,
not a modified-gravity closure assumption.

Usage:
  python3 validate_growth_stencil_convergence.py OUTPUT_DIR PREFIX OUT.json [k1,k2,...]
"""
import json, math, re, sys
from bisect import bisect_left
from pathlib import Path
import numpy as np

if len(sys.argv) not in (4,5):
    raise SystemExit(__doc__)
root=Path(sys.argv[1]); prefix=sys.argv[2]; out=Path(sys.argv[3])
ks=[0.01,0.03,0.05,0.1,0.2,0.5] if len(sys.argv)==4 else [float(x) for x in sys.argv[4].split(',')]
if len(ks)<2 or any((not math.isfinite(k) or k<=0) for k in ks):
    raise SystemExit('invalid k grid')
ks=sorted(set(ks)); kref=ks[0]

def read_pk(path):
    z=None; rows=[]
    for line in path.read_text().splitlines():
        if z is None:
            m=re.search(r'redshift z=([+\-0-9.eE]+)',line)
            if m: z=float(m.group(1))
        s=line.strip()
        if not s or s.startswith('#'): continue
        a=s.split()
        try: rows.append((float(a[0]),float(a[1])))
        except (ValueError,IndexError): pass
    if z is None or len(rows)<3: raise RuntimeError(f'invalid pk file {path}')
    rows.sort(); return z,rows

def interp_logp(rows,k):
    xs=[r[0] for r in rows]; j=bisect_left(xs,k)
    if j==0 or j>=len(rows): raise RuntimeError(f'k={k} outside P(k) range')
    x0,p0=rows[j-1]; x1,p1=rows[j]
    if p0<=0 or p1<=0: raise RuntimeError('non-positive P(k)')
    t=(math.log(k)-math.log(x0))/(math.log(x1)-math.log(x0))
    return math.log(p0)+t*(math.log(p1)-math.log(p0))

def poly_derivative(xs,ys,x,deg):
    # Centering x improves conditioning for the tiny local ln(a) intervals.
    u=np.asarray(xs,float)-x
    c=np.polyfit(u,np.asarray(ys,float),deg)
    dc=np.polyder(c)
    return float(np.polyval(dc,0.0))

fam=[read_pk(p) for p in sorted(root.glob(prefix+'z*_pk.dat'))]
if len(fam)<5: raise SystemExit('need at least five redshift P(k) outputs')
fam.sort(key=lambda t:t[0])
zs=[z for z,_ in fam]
xs=[math.log(1/(1+z)) for z in zs]
records=[]
for i in range(2,len(fam)-2):
    zt=zs[i]; xt=xs[i]
    f3={}; f5={}
    for k in ks:
        y3=[interp_logp(fam[j][1],k) for j in (i-1,i,i+1)]
        x3=[xs[j] for j in (i-1,i,i+1)]
        y5=[interp_logp(fam[j][1],k) for j in range(i-2,i+3)]
        x5=[xs[j] for j in range(i-2,i+3)]
        f3[k]=0.5*poly_derivative(x3,y3,xt,2)
        f5[k]=0.5*poly_derivative(x5,y5,xt,4)
    d3={k:f3[k]-f3[kref] for k in ks}
    d5={k:f5[k]-f5[kref] for k in ks}
    for k in ks:
        records.append({
            'z':zt,'a':1/(1+zt),'k_h_Mpc':k,'kref_h_Mpc':kref,
            'f_3pt':f3[k],'f_5pt':f5[k],
            'abs_f_diff':abs(f3[k]-f5[k]),
            'delta_f_3pt':d3[k],'delta_f_5pt':d5[k],
            'abs_delta_f_diff':abs(d3[k]-d5[k]),
        })
vals_f=[r['abs_f_diff'] for r in records]
vals_d=[r['abs_delta_f_diff'] for r in records]
if not records or any(not math.isfinite(x) for x in vals_f+vals_d):
    raise SystemExit('non-finite convergence diagnostic')
result={
    'schema':'RTK_growth_stencil_convergence_v1',
    'definition':'compare f=0.5*dlnP/dlna from local quadratic 3-point and quartic 5-point derivatives',
    'k_grid_h_Mpc':ks,
    'redshifts':[zs[i] for i in range(2,len(fam)-2)],
    'n_records':len(records),
    'max_abs_f_diff':max(vals_f),
    'rms_abs_f_diff':float(np.sqrt(np.mean(np.square(vals_f)))),
    'max_abs_delta_f_diff':max(vals_d),
    'rms_abs_delta_f_diff':float(np.sqrt(np.mean(np.square(vals_d)))),
    'records':records,
    'interpretation':'diagnostic only; scientific acceptance threshold must be chosen relative to the physical scale-dependent signal and data precision'
}
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print('GROWTH_STENCIL_CONVERGENCE_PASS',len(records))
print('MAX_ABS_F_DIFF',result['max_abs_f_diff'])
print('MAX_ABS_DELTA_F_DIFF',result['max_abs_delta_f_diff'])
