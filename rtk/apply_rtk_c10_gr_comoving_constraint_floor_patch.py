#!/usr/bin/env python3
"""Add a direct GR comoving-density constraint residual to scalar output.

Apply to untouched pinned upstream CLASS. Output only: no dynamics altered.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_grctl')
pt=root/'source'/'perturbations.c'; s=pt.read_text()
marker='RTK_C10_GR_COMOVING_CONSTRAINT_FLOOR_V1'
if marker in s:
    print('C10_GR_COMOVING_CONSTRAINT_FLOOR_ALREADY_APPLIED'); raise SystemExit(0)

title_anchor='''      class_store_columntitle(ppt->scalar_titles, "theta_scf", pba->has_scf);'''
if title_anchor not in s: raise SystemExit('GR control title anchor not found')
title_add=title_anchor+'''\n      /* RTK_C10_GR_COMOVING_CONSTRAINT_FLOOR_V1: output only. */\n      class_store_columntitle(ppt->scalar_titles,"c10gr_k",pba->model == 0.);\n      class_store_columntitle(ppt->scalar_titles,"c10gr_Ccom",pba->model == 0.);\n      class_store_columntitle(ppt->scalar_titles,"c10gr_phi",pba->model == 0.);\n      class_store_columntitle(ppt->scalar_titles,"c10gr_R",pba->model == 0.);'''
s=s.replace(title_anchor,title_add,1)

data_anchor='''    class_store_double(dataptr, theta_scf, pba->has_scf, storeidx);'''
if data_anchor not in s: raise SystemExit('GR control data anchor not found')
data_add=data_anchor+'''\n    if (pba->model == 0.) {\n      double c10gr_a=pvecback[pba->index_bg_a];\n      double c10gr_Hc=c10gr_a*pvecback[pba->index_bg_H];\n      double c10gr_k2=k*k;\n      double c10gr_phi=y[ppw->pv->index_pt_phi];\n      double c10gr_C=ppw->delta_rho+3.*c10gr_Hc*ppw->rho_plus_p_theta/c10gr_k2;\n      double c10gr_R=c10gr_C+2.*c10gr_k2*c10gr_phi/(3.*c10gr_a*c10gr_a);\n      class_store_double(dataptr,k,_TRUE_,storeidx);\n      class_store_double(dataptr,c10gr_C,_TRUE_,storeidx);\n      class_store_double(dataptr,c10gr_phi,_TRUE_,storeidx);\n      class_store_double(dataptr,c10gr_R,_TRUE_,storeidx);\n    }'''
s=s.replace(data_anchor,data_add,1)
pt.write_text(s)
print('C10_GR_COMOVING_CONSTRAINT_FLOOR_PATCH_APPLIED')
