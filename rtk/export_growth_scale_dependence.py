#!/usr/bin/env python3
"""Export scale-dependent linear growth f(k,z) from a CLASS P(k,z) family.

The exporter uses only existing matter-power outputs. For linear growth,
P(k,a) proportional to D(k,a)^2, therefore

    f(k,a) = d ln D / d ln a = 0.5 d ln P / d ln a.

No EFT/PPF or modified-gravity closure assumption is introduced. The output
also reports Delta f(k,z)=f(k,z)-f(k_ref,z), with k_ref the smallest requested
k by default.

Usage:
  python3 export_growth_scale_dependence.py OUTPUT_DIR PREFIX OUT.json [k1,k2,...]

PREFIX is the CLASS root prefix before z*_pk.dat, e.g. rtk001_.
"""
import json, math, re, sys
from bisect import bisect_left
from pathlib import Path

if len(sys.argv) not in (4,5): raise SystemExit(__doc__)
root=Path(sys.argv[1]); prefix=sys.argv[2]; out=Path(sys.argv[3])
ks=[0.01,0.03,0.05,0.1,0.2,0.5] if len(sys.argv)==4 else [float(x) for x in sys.argv[4].split(',')]
if len(ks)<2 or any((not math.isfinite(k) or k<=0) for k in ks): raise SystemExit('invalid k grid')
ks=sorted(set(ks)); kref=ks[0]

def read_pk(path):
    z=None; rows=[]
    for line in path.read_text().splitlines():
        if z is None:
            m=re.search(r'redshift z=([+\-0-9.eE]+)',line)
            if m:z=float(m.group(1))
        s=line.strip()
        if not s or s.startswith('#'):continue
        a=s.split()
        try:rows.append((float(a[0]),float(a[1])))
        except (ValueError,IndexError):pass
    if z is None or len(rows)<3: raise RuntimeError(f'invalid pk file {path}')
    rows.sort(); return z,rows

def interp_logp(rows,k):
    xs=[r[0] for r in rows]; j=bisect_left(xs,k)
    if j==0 or j>=len(rows): raise RuntimeError(f'k={k} outside P(k) range')
    x0,p0=rows[j-1];x1,p1=rows[j]
    if p0<=0 or p1<=0: raise RuntimeError('non-positive P(k)')
    # log-log interpolation is natural for smooth linear spectra.
    t=(math.log(k)-math.log(x0))/(math.log(x1)-math.log(x0))
    return math.log(p0)+t*(math.log(p1)-math.log(p0))

def deriv3(x0,y0,x1,y1,x2,y2,x):
    return (y0*(2*x-x1-x2)/((x0-x1)*(x0-x2))+
            y1*(2*x-x0-x2)/((x1-x0)*(x1-x2))+
            y2*(2*x-x0-x1)/((x2-x0)*(x2-x1)))

fam=[]
for p in sorted(root.glob(prefix+'z*_pk.dat')):
    fam.append(read_pk(p))
if len(fam)<3: raise SystemExit('need at least three redshift P(k) outputs')
fam.sort(key=lambda t:t[0])
zs=[z for z,_ in fam]
# Targets exclude the extreme endpoints because a symmetric/local quadratic
# derivative is scientifically preferable to extrapolation.
targets=zs[1:-1]
rows=[]
for zt in targets:
    i=min(range(len(zs)),key=lambda j:abs(zs[j]-zt))
    i=max(1,min(len(zs)-2,i)); sel=fam[i-1:i+2]
    xa=[math.log(1/(1+z)) for z,_ in sel]; xt=math.log(1/(1+zt))
    fvals={}
    for k in ks:
        yp=[interp_logp(pk,k) for _,pk in sel]
        fvals[k]=0.5*deriv3(xa[0],yp[0],xa[1],yp[1],xa[2],yp[2],xt)
    fr=fvals[kref]
    for k in ks:
        rows.append({'z':zt,'a':1/(1+zt),'k_h_Mpc':k,'f':fvals[k],'delta_f_vs_kref':fvals[k]-fr,'kref_h_Mpc':kref})
result={
 'schema':'RTK_growth_scale_dependence_v1',
 'definition':'f(k,a)=0.5*dlnP(k,a)/dlna from three-point local quadratic derivative',
 'assumptions':['linear matter power family from one CLASS cosmology','P(k)>0','no EFT/PPF mapping assumed'],
 'source_directory':str(root),'source_prefix':prefix,'k_grid_h_Mpc':ks,'redshifts':targets,'rows':rows
}
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print('GROWTH_SCALE_DEPENDENCE_EXPORT_PASS',out,len(rows))
