#!/usr/bin/env python3
"""Build entropy-aware B6 R(T)=H_RTK/H_sameparams table.

Protocol v1.1 consumes an accepted-state AlterBBN trace carrying nucl_single
call serials.  It selects the direct standard central solve (err=0) and never
mixes trial/rejected RHS evaluations or uncertainty-network repeats.
"""
from __future__ import annotations
from bisect import bisect_left
from pathlib import Path
import csv,json,math,sys

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
        if len(q)<4:continue
        call_id=int(q[0]);err=int(q[1]);T=float(q[2]);a=float(q[3])
        if call_id>0 and math.isfinite(T) and math.isfinite(a) and T>0 and a>0:
            rows.append((call_id,err,T,a))
    if len(rows)<100:raise RuntimeError(f'too few accepted-state trace rows: {len(rows)}')
    return rows


def select_central_path(raw):
    groups={}
    for row in raw:groups.setdefault(row[0],[]).append(row)
    meta=[]
    for cid in sorted(groups):
        g=groups[cid];errs={r[1] for r in g}
        if len(errs)!=1:raise RuntimeError(f'call {cid} changes paramrelic.err within one nucl_single solve: {errs}')
        Ts=[r[2] for r in g];aa=[r[3] for r in g]
        meta.append({'call_id':cid,'err':next(iter(errs)),'rows':len(g),'T_start':Ts[0],'T_end':Ts[-1],'T_min':min(Ts),'T_max':max(Ts),'a_start':aa[0],'a_end':aa[-1]})
    # A complete direct central solve must include the fixed 0.01 MeV anchor,
    # start near the standard BBN initial temperature and reach the final tail.
    candidates=[]
    for m in meta:
        if m['err']==0 and m['T_min']<=T_ANCHOR<=m['T_max'] and m['T_max']>1e-3 and m['T_min']<2e-6 and m['rows']>=50:
            candidates.append(m['call_id'])
    if not candidates:raise RuntimeError('no complete accepted err=0 central solve found')
    cid=min(candidates)
    byid={m['call_id']:m for m in meta}
    if cid-1 not in byid or byid[cid-1]['err']!=2:
        raise RuntimeError(f'central call {cid} is not immediately preceded by audited low err=2 solve')
    if cid+1 not in byid or byid[cid+1]['err']!=1:
        raise RuntimeError(f'central call {cid} is not immediately followed by audited high err=1 solve')
    g=groups[cid]
    # Accepted states are recorded in physical integration order: T falls, a rises.
    if any(g[i+1][2]>=g[i][2] for i in range(len(g)-1)):
        raise RuntimeError(f'central accepted path call {cid}: T is not strictly decreasing')
    if any(g[i+1][3]<=g[i][3] for i in range(len(g)-1)):
        raise RuntimeError(f'central accepted path call {cid}: a is not strictly increasing')
    # Interpolation helpers below require increasing T.
    path=sorted([(r[2],r[3]) for r in g],key=lambda x:x[0])
    return path,meta,cid


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
        q=[float(x) for x in s.split()]
        if len(q)>=4 and q[0]>=0 and q[3]>0:out.append((q[0],q[3]))
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


def grid_from_path(path,n):
    Tmin,Tmax=path[0][0],path[-1][0]
    vals=[]
    for i in range(n):
        T=math.exp(math.log(Tmin)+i*(math.log(Tmax)-math.log(Tmin))/(n-1))
        vals.append((T,log_interp_xy(path,T,1)))
    return vals

raw=trace_rows();path,call_meta,central_call_id=select_central_path(raw)
if not (path[0][0] <= T_ANCHOR <= path[-1][0]):
    raise RuntimeError(f'fixed anchor {T_ANCHOR} GeV outside central trace [{path[0][0]},{path[-1][0]}]')
a_anchor=log_interp_xy(path,T_ANCHOR,1)
a_phys_anchor=T0/T_ANCHOR
rtkbg=bg_rows(RTK_BG);lcdbg=bg_rows(LCDM_BG)


def make_table(n):
    rows=[]
    for T,a_int in grid_from_path(path,n):
        a_phys=a_phys_anchor*(a_int/a_anchor);z=1./a_phys-1.
        Hr=interp_bg(rtkbg,z);Hl=interp_bg(lcdbg,z);R=Hr/Hl
        if not all(math.isfinite(x) and x>0 for x in (a_phys,Hr,Hl,R)):raise RuntimeError('nonpositive/nonfinite mapping value')
        rows.append({'T_GeV':T,'T_MeV':T*1e3,'a_internal':a_int,'a_physical':a_phys,'z':z,
                     'H_RTK_over_c_Mpc_inv':Hr,'H_sameparams_LCDM_over_c_Mpc_inv':Hl,'R_H':R})
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
for Tm in (10.0,3.0,2.0,1.0,0.3,0.1,0.03,0.01,0.003,0.001):
    T=Tm*1e-3
    if ref[0]['T_GeV']<=T<=ref[-1]['T_GeV']:
        rr=interp_R(ref,T);rep[str(Tm)]={'R_H':rr,'R_minus_1':rr-1.0}

for name,table in [('nominal_256',nom),('refined_512',ref)]:
    with (OUT/f'{name}.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)

summary={
 'classification':'RTK_BBN_ENTROPY_AWARE_HT_MAPPING_PASS',
 'mapping_protocol':'RTK_BBN_HT_MAPPING_PROTOCOL_v1_1_TRACE_FIX',
 'raw_accepted_trace_rows':len(raw),'central_call_id':central_call_id,'central_accepted_rows':len(path),
 'call_metadata':call_meta,
 'trace_T_GeV_range':[path[0][0],path[-1][0]],
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
