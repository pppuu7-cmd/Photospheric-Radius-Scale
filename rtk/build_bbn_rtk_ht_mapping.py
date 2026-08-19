#!/usr/bin/env python3
"""Build entropy-aware B6 R(T)=H_RTK/H_sameparams table.

Inputs are an instrument-only AlterBBN T-a trace and two pinned CLASS background
files (RTK and same-shared-parameter LCDM).  No abundance network modification
is performed here.
"""
from __future__ import annotations
from bisect import bisect_left
from pathlib import Path
import csv,json,math,statistics,sys

if len(sys.argv)!=4:
    raise SystemExit('usage: build_bbn_rtk_ht_mapping.py TRACE RTK_BACKGROUND LCDM_BACKGROUND')
TRACE=Path(sys.argv[1]);RTK_BG=Path(sys.argv[2]);LCDM_BG=Path(sys.argv[3])
OUT=Path('output/b6_bbn_ht_mapping');OUT.mkdir(parents=True,exist_ok=True)
T_ANCHOR=1e-5 # GeV = 0.01 MeV
TCMB_K=2.7255
KB_GEV_PER_K=8.617333262e-14
T0=TCMB_K*KB_GEV_PER_K
NOMINAL_N=256;REFINED_N=512


def trace_rows():
    rows=[]
    for line in TRACE.read_text(errors='replace').splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        q=s.split()
        if len(q)<3:continue
        T,a,H=map(float,q[:3])
        if all(math.isfinite(x) and x>0 for x in (T,a,H)):rows.append((T,a,H))
    if len(rows)<100:raise RuntimeError(f'too few raw trace rows: {len(rows)}')
    return rows


def reduce_trace(raw,nbin=2048):
    lo=min(math.log(r[0]) for r in raw);hi=max(math.log(r[0]) for r in raw)
    bins=[[] for _ in range(nbin)]
    for T,a,H in raw:
        u=(math.log(T)-lo)/(hi-lo);i=min(nbin-1,max(0,int(u*nbin)))
        bins[i].append((T,a,H))
    out=[]
    for b in bins:
        if not b:continue
        # Solver trial calls sample the same thermodynamic path. Median in log
        # variables suppresses repeated/rejected micro-steps without changing dynamics.
        T=math.exp(statistics.median([math.log(x[0]) for x in b]))
        a=math.exp(statistics.median([math.log(x[1]) for x in b]))
        H=math.exp(statistics.median([math.log(x[2]) for x in b]))
        out.append((T,a,H))
    out.sort(key=lambda r:r[0])
    if len(out)<REFINED_N:raise RuntimeError(f'reduced trace has only {len(out)} points')
    # a must decrease with increasing T. Permit only numerical scatter at 2e-4 in log a.
    bad=[]
    for x,y in zip(out,out[1:]):
        if math.log(y[1])-math.log(x[1]) > 2e-4:bad.append((x,y))
    if bad:raise RuntimeError(f'nonmonotone reduced a(T): {len(bad)} violations')
    return out


def log_interp_xy(rows,x,col=1):
    xs=[r[0] for r in rows]
    if not (xs[0]<=x<=xs[-1]):raise RuntimeError(f'x={x} outside [{xs[0]},{xs[-1]}]')
    j=bisect_left(xs,x)
    if j<len(xs) and xs[j]==x:return rows[j][col]
    x0,x1=xs[j-1],xs[j];y0,y1=rows[j-1][col],rows[j][col]
    lx=math.log(x);f=(lx-math.log(x0))/(math.log(x1)-math.log(x0))
    return math.exp(math.log(y0)+f*(math.log(y1)-math.log(y0)))


def bg_rows(path):
    out=[]
    for line in path.read_text(errors='replace').splitlines():
        s=line.strip()
        if not s or s.startswith('#'):continue
        a=[float(x) for x in s.split()]
        if len(a)>=4 and a[0]>=0 and a[3]>0:out.append((a[0],a[3]))
    out.sort()
    if len(out)<20:raise RuntimeError(f'too few background rows in {path}')
    return out


def interp_bg(rows,z):
    zs=[r[0] for r in rows]
    if not (zs[0]<=z<=zs[-1]):raise RuntimeError(f'z={z} outside CLASS coverage [{zs[0]},{zs[-1]}]')
    j=bisect_left(zs,z)
    if j<len(zs) and zs[j]==z:return rows[j][1]
    z0,h0=rows[j-1];z1,h1=rows[j]
    x=math.log1p(z);f=(x-math.log1p(z0))/(math.log1p(z1)-math.log1p(z0))
    return math.exp(math.log(h0)+f*(math.log(h1)-math.log(h0)))


def grid_from_trace(red,n):
    Tmin=max(red[0][0],min(r[0] for r in red));Tmax=red[-1][0]
    vals=[]
    for i in range(n):
        T=math.exp(math.log(Tmin)+i*(math.log(Tmax)-math.log(Tmin))/(n-1))
        a=log_interp_xy(red,T,1);Href_trace=log_interp_xy(red,T,2)
        vals.append((T,a,Href_trace))
    return vals

raw=trace_rows();red=reduce_trace(raw)
if not (red[0][0] <= T_ANCHOR <= red[-1][0]):
    raise RuntimeError(f'fixed anchor {T_ANCHOR} GeV outside trace [{red[0][0]},{red[-1][0]}]')
a_anchor=log_interp_xy(red,T_ANCHOR,1)
a_phys_anchor=T0/T_ANCHOR
rtkbg=bg_rows(RTK_BG);lcdbg=bg_rows(LCDM_BG)


def make_table(n):
    rows=[]
    for T,a_int,Htrace in grid_from_trace(red,n):
        a_phys=a_phys_anchor*(a_int/a_anchor);z=1./a_phys-1.
        Hr=interp_bg(rtkbg,z);Hl=interp_bg(lcdbg,z);R=Hr/Hl
        if not all(math.isfinite(x) and x>0 for x in (a_phys,Hr,Hl,R)):raise RuntimeError('nonpositive/nonfinite mapping value')
        rows.append({'T_GeV':T,'T_MeV':T*1e3,'a_internal':a_int,'a_physical':a_phys,'z':z,
                     'H_trace_standard':Htrace,'H_RTK_over_c_Mpc_inv':Hr,'H_sameparams_LCDM_over_c_Mpc_inv':Hl,'R_H':R})
    # increasing T => decreasing a_phys and increasing z
    if any(rows[i+1]['a_physical']>=rows[i]['a_physical'] for i in range(len(rows)-1)):
        raise RuntimeError('physical scale factor is not strictly decreasing with increasing T')
    if any(rows[i+1]['z']<=rows[i]['z'] for i in range(len(rows)-1)):
        raise RuntimeError('mapped z is not strictly increasing with T')
    return rows

nom=make_table(NOMINAL_N);ref=make_table(REFINED_N)

def interp_R(table,T):
    rr=[(x['T_GeV'],x['R_H']) for x in table]
    return log_interp_xy(rr,T,1)
errs=[abs(interp_R(nom,x['T_GeV'])-x['R_H']) for x in ref]
maxerr=max(errs)
if maxerr>2e-12:raise RuntimeError(f'nominal/refined R interpolation error {maxerr} > 2e-12')

rep={}
for Tm in (10.0,3.0,1.0,0.3,0.1,0.03,0.01):
    T=Tm*1e-3
    if ref[0]['T_GeV']<=T<=ref[-1]['T_GeV']:
        rep[str(Tm)]= {'R_H':interp_R(ref,T),'R_minus_1':interp_R(ref,T)-1.0}

for name,table in [('nominal_256',nom),('refined_512',ref)]:
    with (OUT/f'{name}.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)

summary={
 'classification':'RTK_BBN_ENTROPY_AWARE_HT_MAPPING_PASS',
 'mapping_protocol':'RTK_BBN_HT_MAPPING_PROTOCOL_v1',
 'raw_trace_rows':len(raw),'reduced_trace_rows':len(red),
 'trace_T_GeV_range':[red[0][0],red[-1][0]],
 'anchor':{'T_GeV':T_ANCHOR,'T_MeV':0.01,'a_internal':a_anchor,'T0_GeV':T0,'a_physical':a_phys_anchor},
 'mapped_z_range':[ref[0]['z'],ref[-1]['z']],
 'class_rtk_z_coverage':[rtkbg[0][0],rtkbg[-1][0]],
 'class_lcdm_z_coverage':[lcdbg[0][0],lcdbg[-1][0]],
 'nominal_points':len(nom),'refined_points':len(ref),
 'nominal_vs_refined_max_abs_R_error':maxerr,
 'max_abs_R_minus_1':max(abs(x['R_H']-1.) for x in ref),
 'representative_T_MeV':rep,
 'next_gate':'patch common AlterBBN Hubble rate with table lookup; run paired R=1 and RTK R(T) abundance/refinement tests',
 'warning':'Expansion-history table only; no abundance or observational consistency claim.'
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_BBN_ENTROPY_AWARE_HT_MAPPING_PASS',json.dumps(summary,sort_keys=True))
