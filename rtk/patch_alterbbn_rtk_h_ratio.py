#!/usr/bin/env python3
"""Fail-closed AlterBBN v2.2 patch for paired B6 H(T) abundance tests."""
from __future__ import annotations
from pathlib import Path
import argparse,csv,hashlib,json,math,re

KB_GEV_PER_K=8.617333262e-14
TGEV_PER_T9=1.0e9*KB_GEV_PER_K
BOUNDARY_REL_TOL=5.0e-7

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load_table(path,mode):
    rows=[]
    with Path(path).open(newline='') as f:
        for row in csv.DictReader(f):
            T=float(row['T_GeV']);R=float(row['R_H'])
            if mode=='reference': R=1.0
            if not(math.isfinite(T) and T>0 and math.isfinite(R) and R>0): raise RuntimeError(row)
            rows.append((T,R))
    if len(rows)<100: raise RuntimeError(f'too few H(T) rows: {len(rows)}')
    if any(rows[i+1][0]<=rows[i][0] for i in range(len(rows)-1)): raise RuntimeError('T grid not strictly increasing')
    return rows

def make_header(rows,source_sha,mode):
    Ts=',\n  '.join(f'{x:.17e}' for x,_ in rows);Rs=',\n  '.join(f'{x:.17e}' for _,x in rows)
    return f'''/* AUTO-GENERATED fail-closed B6 H(T) input. */
#ifndef RTK_BBN_H_RATIO_H
#define RTK_BBN_H_RATIO_H
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#define RTK_BBN_HT_N {len(rows)}
#define RTK_BBN_HT_SOURCE_SHA256 "{source_sha}"
#define RTK_BBN_HT_MODE "{mode}"
static const double rtk_bbn_T_GeV[RTK_BBN_HT_N]={{\n  {Ts}\n}};
static const double rtk_bbn_RH[RTK_BBN_HT_N]={{\n  {Rs}\n}};
static double rtk_bbn_h_ratio_from_T9(double T9){{
 const double k={TGEV_PER_T9:.17e},reltol={BOUNDARY_REL_TOL:.17e}; double T=T9*k;
 const double lo=rtk_bbn_T_GeV[0],hi=rtk_bbn_T_GeV[RTK_BBN_HT_N-1];
 if(!(isfinite(T)&&T>0.0)){{fprintf(stderr,"RTK_BBN_HT_NONFINITE_T %.17e\\n",T);abort();}}
 if(T<lo){{if((lo-T)/lo<=reltol)T=lo;else{{fprintf(stderr,"RTK_BBN_HT_OOB_LOW %.17e %.17e\\n",T,lo);abort();}}}}
 if(T>hi){{if((T-hi)/hi<=reltol)T=hi;else{{fprintf(stderr,"RTK_BBN_HT_OOB_HIGH %.17e %.17e\\n",T,hi);abort();}}}}
 if(T==lo)return rtk_bbn_RH[0]; if(T==hi)return rtk_bbn_RH[RTK_BBN_HT_N-1];
 int a=0,b=RTK_BBN_HT_N-1;while(b-a>1){{int m=a+(b-a)/2;if(rtk_bbn_T_GeV[m]<=T)a=m;else b=m;}}
 const double lT=log(T),l0=log(rtk_bbn_T_GeV[a]),l1=log(rtk_bbn_T_GeV[b]),f=(lT-l0)/(l1-l0);
 return exp(log(rtk_bbn_RH[a])+f*(log(rtk_bbn_RH[b])-log(rtk_bbn_RH[a])));
}}
#endif
'''

def patch_bbn(path):
    s=Path(path).read_text();lines=s.splitlines(True)
    if 'rtk_bbn_h_ratio.h' in s: raise RuntimeError('bbn.c already patched')
    expected=('rho_gamma','rho_epem','rho_wimp','rho_neutrinos','rho_neuteq','rho_baryons','rhod')
    hits=[]
    for i,line in enumerate(lines):
        q=''.join(line.split())
        # The published v2.2 archive is the byte-verified authority. Match the
        # unique common Friedmann assignment structurally instead of depending
        # on punctuation/spacing of the public mirror. Still fail closed unless
        # exactly one source line contains H=, sqrt(, and every expected density.
        if 'H=' in q and 'sqrt(' in q and q.endswith(';') and all(x in q for x in expected):
            hits.append(i)
    if len(hits)!=1: raise RuntimeError(f'expected one common Friedmann H assignment; found {len(hits)}')
    matched=''.join(lines[hits[0]].split())
    if matched.count('H=')!=1 or matched.count('sqrt(')!=1:
        raise RuntimeError(f'ambiguous Friedmann assignment structure: {matched!r}')
    inc=[i for i,l in enumerate(lines) if '#include' in l and 'include.h' in l]
    if len(inc)!=1: raise RuntimeError(f'expected one include.h; found {len(inc)}')
    lines.insert(inc[0]+1,'#include "rtk_bbn_h_ratio.h"\n');hidx=hits[0]+(1 if inc[0]<hits[0] else 0)
    indent=re.match(r'\s*',lines[hidx]).group(0);lines.insert(hidx+1,indent+'H *= rtk_bbn_h_ratio_from_T9(T9); /* RTK_BBN_H_RATIO_V1 */\n')
    Path(path).write_text(''.join(lines))

def patch_driver(path,eta):
    s=Path(path).read_text();init='Init_cosmomodel(&paramrelic);'
    if 'RTK_BBN_ETA_V1' in s: raise RuntimeError('stand_cosmo.c already patched')
    if s.count(init)!=1: raise RuntimeError(f'expected one Init_cosmomodel call; found {s.count(init)}')
    s=s.replace(init,init+f'\n\tparamrelic.eta0={eta:.17e}; /* RTK_BBN_ETA_V1 */',1)
    n=s.count('%.3e')
    if n<6: raise RuntimeError(f'expected >=6 abundance precision tokens; found {n}')
    Path(path).write_text(s.replace('%.3e','%.17e'));return n

def main():
    ap=argparse.ArgumentParser();ap.add_argument('tree',type=Path);ap.add_argument('table',type=Path);ap.add_argument('--mode',choices=('reference','rtk'),required=True);ap.add_argument('--eta',type=float,required=True);ap.add_argument('--manifest',type=Path)
    a=ap.parse_args()
    if not 0<a.eta<1e-8: raise RuntimeError(f'implausible eta {a.eta}')
    bbn=a.tree/'src/bbn.c';driver=a.tree/'stand_cosmo.c'
    if not bbn.is_file() or not driver.is_file(): raise RuntimeError('missing pinned source files')
    rows=load_table(a.table,a.mode);table_sha=sha256(a.table);before={'bbn.c':sha256(bbn),'stand_cosmo.c':sha256(driver)}
    header=a.tree/'src/rtk_bbn_h_ratio.h';header.write_text(make_header(rows,table_sha,a.mode));patch_bbn(bbn);fmt=patch_driver(driver,a.eta)
    out={
      'classification':'ALTERBBN_B6_H_RATIO_PATCH_APPLIED','mode':a.mode,'eta':a.eta,'table_sha256':table_sha,'table_rows':len(rows),'T_GeV_range':[rows[0][0],rows[-1][0]],
      'max_abs_R_minus_1':max(abs(r-1.0) for _,r in rows),'TGeV_per_T9':TGEV_PER_T9,'boundary_relative_tolerance':BOUNDARY_REL_TOL,'source_before_sha256':before,
      'source_after_sha256':{'bbn.c':sha256(bbn),'stand_cosmo.c':sha256(driver),'header':sha256(header)},'driver_abundance_format_tokens_upgraded':fmt,
      'scientific_difference_rule':'reference and RTK receive identical eta/output/H-call patch; only R_H table values differ'}
    p=a.manifest or a.tree/f'rtk_b6_patch_manifest_{a.mode}.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('ALTERBBN_B6_H_RATIO_PATCH_PASS',json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
