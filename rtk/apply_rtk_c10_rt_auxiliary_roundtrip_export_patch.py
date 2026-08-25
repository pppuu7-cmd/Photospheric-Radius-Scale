#!/usr/bin/env python3
"""Append read-only fields needed for the C10 legacy-RT 00/0i round-trip.

Apply only to a disposable CLASS clone after the existing C10 direct regularity
export patch.  No equation, source, metric, or integration variable is changed.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
s=pt.read_text()
marker='RTK_C10_RT_AUXILIARY_ROUNDTRIP_EXPORT_V1'
if marker in s:
    print('C10_RT_AUXILIARY_ROUNDTRIP_EXPORT_ALREADY_APPLIED')
    raise SystemExit(0)
if 'RTK_C10_DIRECT_REGULARITY_EXPORT_V1' not in s:
    raise SystemExit('apply the direct C10 regularity export patch first')

title_anchor='''      class_store_columntitle(ppt->scalar_titles,"c10_model2_0i_aux",pba->model == 2.);'''
title_add=title_anchor+'''\n      /* RTK_C10_RT_AUXILIARY_ROUNDTRIP_EXPORT_V1: independent RT 00 audit inputs. */\n      class_store_columntitle(ppt->scalar_titles,"c10_dU_nlde",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_dV_prime_nlde",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_V_bg_prime_nlde",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_phi_CLASS",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_psi_CLASS",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_phi_prime_CLASS",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_gamma",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_H0_Mpc_inv",pba->model == 2.);'''
if title_anchor not in s:
    raise SystemExit('roundtrip title anchor not found')
s=s.replace(title_anchor,title_add,1)

data_anchor='''        class_store_double(dataptr,c10_aux,_TRUE_,storeidx);'''
data_add=data_anchor+'''\n        class_store_double(dataptr,y[ppw->pv->index_pt_deltaU_nlde],_TRUE_,storeidx);\n        class_store_double(dataptr,y[ppw->pv->index_pt_deltaV_prime_nlde],_TRUE_,storeidx);\n        class_store_double(dataptr,ppw->pvecback[pba->index_bg_V_prime_nlde],_TRUE_,storeidx);\n        class_store_double(dataptr,phi,_TRUE_,storeidx);\n        class_store_double(dataptr,psi,_TRUE_,storeidx);\n        class_store_double(dataptr,pvecmetric[ppw->index_mt_phi_prime],_TRUE_,storeidx);\n        class_store_double(dataptr,pba->gnl,_TRUE_,storeidx);\n        class_store_double(dataptr,pba->H0,_TRUE_,storeidx);'''
if data_anchor not in s:
    raise SystemExit('roundtrip data anchor not found')
s=s.replace(data_anchor,data_add,1)
pt.write_text(s)
print('C10_RT_AUXILIARY_ROUNDTRIP_EXPORT_PATCH_APPLIED')
