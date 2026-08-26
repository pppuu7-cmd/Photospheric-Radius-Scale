#!/usr/bin/env python3
"""Append C10.65a read-only individual-species controls to scalar perturbation output.

Apply after apply_rtk_c10_source_export_patch.py on a disposable pinned CLASS tree.
No evolution/source equation is modified.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
s=pt.read_text()
marker='RTK_C10_65A_SPECIES_CONTROL_EXPORT_V1'
if marker in s:
    print('C10_65A_SPECIES_CONTROL_PATCH_ALREADY_APPLIED')
    raise SystemExit(0)

title_old='''      class_store_columntitle(ppt->scalar_titles,"c10_khr_ca2",pba->model == 2.);'''
title_new=title_old+'''\n      /* RTK_C10_65A_SPECIES_CONTROL_EXPORT_V1: controls only; no dynamics changed. */\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_delta_g",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_theta_g",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_shear_g",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_delta_b",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_theta_b",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_CLASS_psi_lapse",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_CLASS_phi_curvature",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_delta_ur",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_theta_ur",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65a_shear_ur",pba->model == 2.);'''
if title_old not in s:
    raise SystemExit('C10.65a title anchor not found; apply C10 source-export patch first')
s=s.replace(title_old,title_new,1)

data_old='''      class_store_double(dataptr,c10_kb.ca2,_TRUE_,storeidx);'''
data_new=data_old+'''\n      class_store_double(dataptr,delta_g,_TRUE_,storeidx);\n      class_store_double(dataptr,theta_g,_TRUE_,storeidx);\n      class_store_double(dataptr,shear_g,_TRUE_,storeidx);\n      class_store_double(dataptr,delta_b,_TRUE_,storeidx);\n      class_store_double(dataptr,theta_b,_TRUE_,storeidx);\n      class_store_double(dataptr,psi,_TRUE_,storeidx);\n      class_store_double(dataptr,phi,_TRUE_,storeidx);\n      class_store_double(dataptr,delta_ur,pba->has_ur,storeidx);\n      class_store_double(dataptr,theta_ur,pba->has_ur,storeidx);\n      class_store_double(dataptr,shear_ur,pba->has_ur,storeidx);'''
if data_old not in s:
    raise SystemExit('C10.65a data anchor not found; apply C10 source-export patch first')
s=s.replace(data_old,data_new,1)
pt.write_text(s)
print('C10_65A_SPECIES_CONTROL_PATCH_APPLIED')
