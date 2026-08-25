#!/usr/bin/env python3
"""Extend the C10 read-only source export with direct cancellation diagnostics.

Apply after rtk/apply_rtk_c10_source_export_patch.py on a disposable RT-CLASS
clone.  The crucial C_com combination is evaluated inside CLASS from the
same workspace state in double precision, before ASCII output/interpolation:

  C_com = delta_rho_CLASS + 3 Hc rho_plus_p_theta_CLASS / k^2.

Additional model-2 auxiliary columns are diagnostic provenance only.  No
production dynamics are changed and nothing is fed back into CLASS.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
s=pt.read_text()
marker='RTK_C10_DIRECT_REGULARITY_EXPORT_V1'
if marker in s:
    print('C10_DIRECT_REGULARITY_EXPORT_ALREADY_APPLIED')
    raise SystemExit(0)
if 'RTK_C10_READONLY_SOURCE_EXPORT_V1' not in s:
    raise SystemExit('apply the base C10 source export patch first')

title_anchor='''      class_store_columntitle(ppt->scalar_titles,"c10_khr_ca2",pba->model == 2.);'''
title_add=title_anchor+'''\n      /* RTK_C10_DIRECT_REGULARITY_EXPORT_V1: direct same-workspace diagnostics. */\n      class_store_columntitle(ppt->scalar_titles,"c10_Ccom_direct",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_Ccom_over_k2_direct",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_dZ_nlde",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_dZ_prime_nlde",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_dV_nlde",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_V_bg_nlde",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_model2_0i_aux",pba->model == 2.);'''
if title_anchor not in s:
    raise SystemExit('direct regularity title anchor not found')
s=s.replace(title_anchor,title_add,1)

data_anchor='''      class_store_double(dataptr,c10_kb.ca2,_TRUE_,storeidx);'''
data_add=data_anchor+'''\n      {\n        double c10_Ccom = ppw->delta_rho + 3.*c10_Hc*ppw->rho_plus_p_theta/(k*k);\n        double c10_dZ = y[ppw->pv->index_pt_deltaZ_nlde];\n        double c10_dZp = y[ppw->pv->index_pt_deltaZ_prime_nlde];\n        double c10_dV = y[ppw->pv->index_pt_deltaV_nlde];\n        double c10_Vbg = ppw->pvecback[pba->index_bg_V_nlde];\n        double c10_aux = 1.5*(pba->gnl)*(pba->H0)*(pba->H0)\n          *(c10_Hc*c10_dZ - 0.5*c10_dZp + 0.5*c10_Vbg*psi - 0.5*c10_dV);\n        class_store_double(dataptr,c10_Ccom,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_Ccom/(k*k),_TRUE_,storeidx);\n        class_store_double(dataptr,c10_dZ,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_dZp,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_dV,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_Vbg,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_aux,_TRUE_,storeidx);\n      }'''
if data_anchor not in s:
    raise SystemExit('direct regularity data anchor not found')
s=s.replace(data_anchor,data_add,1)
pt.write_text(s)
print('C10_DIRECT_REGULARITY_EXPORT_PATCH_APPLIED')
