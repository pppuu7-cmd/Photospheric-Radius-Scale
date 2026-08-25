#!/usr/bin/env python3
"""Read-only diagnostics for an untouched pinned native RT CLASS control.

Apply directly to dirian/class_public at the frozen upstream SHA, with no RTK
background/stress/IC patches. Only scalar perturbation output columns are added.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_native_rt')
pt=root/'source'/'perturbations.c'
s=pt.read_text()
marker='RTK_C10_NATIVE_RT_CONTROL_EXPORT_V1'
if marker in s:
    print('C10_NATIVE_RT_CONTROL_EXPORT_ALREADY_APPLIED')
    raise SystemExit(0)

title_anchor='''    if(pba->model == 2.) class_store_columntitle(ppt->scalar_titles,"dZ_nlde",pba->has_nlde);'''
title_add=title_anchor+'''\n    /* RTK_C10_NATIVE_RT_CONTROL_EXPORT_V1: output-only native RT diagnostics. */\n    class_store_columntitle(ppt->scalar_titles,"rtctl_k",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_Hc",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_Ccom",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_dU",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_dV",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_dVprime",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_dZ",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_dZprime",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_Vbg",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_Vbgprime",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_phi",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_psi",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_phi_prime",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_gamma",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_H0",pba->model == 2.);\n    class_store_columntitle(ppt->scalar_titles,"rtctl_A0i_code",pba->model == 2.);'''
if title_anchor not in s:
    raise SystemExit('native RT title anchor not found')
s=s.replace(title_anchor,title_add,1)

data_anchor='''    if(pba->model == 2.) class_store_double(dataptr, dZ_nlde, pba->has_nlde, storeidx);'''
data_add=data_anchor+'''\n    if (pba->model == 2.) {\n      double rtctl_a=pvecback[pba->index_bg_a];\n      double rtctl_Hc=rtctl_a*pvecback[pba->index_bg_H];\n      double rtctl_C=ppw->delta_rho + 3.*rtctl_Hc*ppw->rho_plus_p_theta/(k*k);\n      double rtctl_dU=y[ppw->pv->index_pt_deltaU_nlde];\n      double rtctl_dV=y[ppw->pv->index_pt_deltaV_nlde];\n      double rtctl_dVp=y[ppw->pv->index_pt_deltaV_prime_nlde];\n      double rtctl_dZ=y[ppw->pv->index_pt_deltaZ_nlde];\n      double rtctl_dZp=y[ppw->pv->index_pt_deltaZ_prime_nlde];\n      double rtctl_V=pvecback[pba->index_bg_V_nlde];\n      double rtctl_Vp=pvecback[pba->index_bg_V_prime_nlde];\n      double rtctl_phi=y[ppw->pv->index_pt_phi];\n      double rtctl_psi=pvecmetric[ppw->index_mt_psi];\n      double rtctl_phip=pvecmetric[ppw->index_mt_phi_prime];\n      double rtctl_A0i=1.5*pba->gnl*pba->H0*pba->H0\n        *(rtctl_Hc*rtctl_dZ - 0.5*rtctl_dZp + 0.5*rtctl_V*rtctl_psi - 0.5*rtctl_dV);\n      class_store_double(dataptr,k,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_Hc,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_C,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_dU,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_dV,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_dVp,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_dZ,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_dZp,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_V,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_Vp,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_phi,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_psi,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_phip,_TRUE_,storeidx);\n      class_store_double(dataptr,pba->gnl,_TRUE_,storeidx);\n      class_store_double(dataptr,pba->H0,_TRUE_,storeidx);\n      class_store_double(dataptr,rtctl_A0i,_TRUE_,storeidx);\n    }'''
if data_anchor not in s:
    raise SystemExit('native RT data anchor not found')
s=s.replace(data_anchor,data_add,1)
pt.write_text(s)
print('C10_NATIVE_RT_CONTROL_EXPORT_PATCH_APPLIED')
