#!/usr/bin/env python3
"""Add output-only direct model=2 metric-equation residuals.

Works on the pinned nonlocal upstream tree either untouched or after the normal
RTK production patch sequence.  It adds diagnostics only and does not change
background, perturbation, metric, source or approximation dynamics.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_direct_native')
pt=root/'source'/'perturbations.c'
s=pt.read_text()
marker='RTK_C10_DIRECT_NATIVE_MODEL2_METRIC_IDENTITY_V1'
if marker in s:
    print('C10_DIRECT_NATIVE_MODEL2_IDENTITY_ALREADY_APPLIED')
    raise SystemExit(0)

title_anchor='''    if(pba->model == 2.) class_store_columntitle(ppt->scalar_titles,"dZ_nlde",pba->has_nlde);'''
if title_anchor not in s:
    raise SystemExit('direct native metric identity title anchor not found')
title_add=title_anchor+'''\n    /* RTK_C10_DIRECT_NATIVE_MODEL2_METRIC_IDENTITY_V1: output-only residuals. */\n    class_store_columntitle(ppt->scalar_titles,"c10dn_k",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"c10dn_Rpsi",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"c10dn_R0i",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"c10dn_psi",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"c10dn_psi_rhs",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"c10dn_phip",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"c10dn_phip_rhs",pba->model == 2.);'''
s=s.replace(title_anchor,title_add,1)

data_anchor='''    if(pba->model == 2.) class_store_double(dataptr, dZ_nlde, pba->has_nlde, storeidx);'''
if data_anchor not in s:
    raise SystemExit('direct native metric identity data anchor not found')
data_add=data_anchor+'''\n    if (pba->model == 2.) {\n      double c10dn_a=pvecback[pba->index_bg_a];\n      double c10dn_a2=c10dn_a*c10dn_a;\n      double c10dn_k2=k*k;\n      double c10dn_Hc=c10dn_a*pvecback[pba->index_bg_H];\n      double c10dn_phi=y[ppw->pv->index_pt_phi];\n      double c10dn_psi=pvecmetric[ppw->index_mt_psi];\n      double c10dn_phip=pvecmetric[ppw->index_mt_phi_prime];\n      double c10dn_dZ=y[ppw->pv->index_pt_deltaZ_nlde];\n      double c10dn_dZp=y[ppw->pv->index_pt_deltaZ_prime_nlde];\n      double c10dn_dV=y[ppw->pv->index_pt_deltaV_nlde];\n      double c10dn_V=pvecback[pba->index_bg_V_nlde];\n      double c10dn_H02=pba->H0*pba->H0;\n      double c10dn_psi_rhs=c10dn_phi + 3.*pba->gnl*c10dn_dZ*c10dn_H02\n        - 4.5*(c10dn_a2/c10dn_k2)*ppw->rho_plus_p_shear;\n      double c10dn_aux=1.5*pba->gnl*c10dn_H02\n        *(c10dn_Hc*c10dn_dZ - 0.5*c10dn_dZp + 0.5*c10dn_V*c10dn_psi - 0.5*c10dn_dV);\n      double c10dn_phip_rhs=-c10dn_Hc*c10dn_psi\n        + 1.5*(c10dn_a2/c10dn_k2)*ppw->rho_plus_p_theta + c10dn_aux;\n      class_store_double(dataptr,k,_TRUE_,storeidx);\n      class_store_double(dataptr,c10dn_psi-c10dn_psi_rhs,_TRUE_,storeidx);\n      class_store_double(dataptr,c10dn_phip-c10dn_phip_rhs,_TRUE_,storeidx);\n      class_store_double(dataptr,c10dn_psi,_TRUE_,storeidx);\n      class_store_double(dataptr,c10dn_psi_rhs,_TRUE_,storeidx);\n      class_store_double(dataptr,c10dn_phip,_TRUE_,storeidx);\n      class_store_double(dataptr,c10dn_phip_rhs,_TRUE_,storeidx);\n    }'''
s=s.replace(data_anchor,data_add,1)
pt.write_text(s)
print('C10_DIRECT_NATIVE_MODEL2_METRIC_IDENTITY_PATCH_APPLIED')
