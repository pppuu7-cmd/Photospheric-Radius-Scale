#!/usr/bin/env python3
from __future__ import annotations
import argparse,glob,json,math
from pathlib import Path

def numeric(path):
    return [s.strip() for s in Path(path).read_text().splitlines() if s.strip() and not s.lstrip().startswith('#')]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--control-glob',required=True)
    ap.add_argument('--off-glob',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    c=sorted(glob.glob(a.control_glob)); o=sorted(glob.glob(a.off_glob))
    assert len(c)==len(o)==4
    files=[]; g_abs=0.; g_rel=0.; all_shape=True; exact=True
    for cf,of in zip(c,o):
        cr=numeric(cf); orr=numeric(of)
        same_rows=len(cr)==len(orr); all_shape &= same_rows
        first=None; mabs=0.; mrel=0.; tokshape=True
        for ri,(x,y) in enumerate(zip(cr,orr)):
            if x==y: continue
            exact=False
            xs=x.split(); ys=y.split(); tokshape &= len(xs)==len(ys); all_shape &= len(xs)==len(ys)
            if len(xs)!=len(ys):
                if first is None: first={'row':ri,'kind':'token_count','control_tokens':len(xs),'off_tokens':len(ys)}
                continue
            for j,(sx,sy) in enumerate(zip(xs,ys)):
                if sx==sy: continue
                try:
                    vx=float(sx); vy=float(sy)
                    da=abs(vx-vy); dr=da/max(abs(vx),abs(vy),1e-300)
                    mabs=max(mabs,da); mrel=max(mrel,dr); g_abs=max(g_abs,da); g_rel=max(g_rel,dr)
                    if first is None: first={'row':ri,'column_index':j,'control':vx,'off':vy,'abs':da,'rel':dr}
                except ValueError:
                    if first is None: first={'row':ri,'column_index':j,'control_text':sx,'off_text':sy}
        files.append({'control':cf,'off':of,'same_row_count':same_rows,'token_shape_same':tokshape,'exact_numeric_text_identity':cr==orr,'max_abs':mabs,'max_rel':mrel,'first_difference':first})
    out={'schema':'RTK_C10_65R2_OFF_PATH_DIFF_DIAGNOSTIC_v1','exact_numeric_text_identity_all_four':exact,'shape_same_all_four':all_shape,'max_abs_all_four':g_abs,'max_rel_all_four':g_rel,'files':files,'interpretation':'Diagnostic only. Frozen C10.65r2 criteria are unchanged.'}
    Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__': main()
