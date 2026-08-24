#!/usr/bin/env python3
"""Patch a disposable RT-CLASS tree with C10 read-only source diagnostics.

The patch adds columns to CLASS scalar perturbation output only.  It does not
modify the perturbation/background equations or feed completed-U(1) metric
potentials back into CLASS.

Apply *after* the normal RTK production patch/upgrade sequence so model=2 uses
its production Khronon source implementation and pba->lambda_D is available.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "class_public")
pt = root / "source" / "perturbations.c"
s = pt.read_text()

marker = "RTK_C10_READONLY_SOURCE_EXPORT_V1"
if marker in s:
    print("C10_SOURCE_EXPORT_PATCH_ALREADY_APPLIED")
    raise SystemExit(0)

# Add diagnostic titles after the final standard scalar-field columns.
title_old = '''      class_store_columntitle(ppt->scalar_titles, "delta_scf", pba->has_scf);\n      class_store_columntitle(ppt->scalar_titles, "theta_scf", pba->has_scf);'''
title_new = title_old + '''\n      /* RTK_C10_READONLY_SOURCE_EXPORT_V1: diagnostics only; no dynamics changed. */\n      class_store_columntitle(ppt->scalar_titles,"c10_k_Mpc_inv",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_Hc",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_Hc_prime",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_H0_ord",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_H0_ord_prime",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_H0_ord_double_prime",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_deltaH0_ord",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_delta_mu_total",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_rpp_theta_total",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_delta_p_total",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_rpp_shear_total",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_W_total",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_rho_total_prime",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_p_total_prime",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_khr_w",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_khr_ca2",pba->model == 2.);'''
if title_old not in s:
    raise SystemExit("C10 exporter: scalar title anchor not found")
s = s.replace(title_old, title_new, 1)

# Add values after the matching scalar-field values.  The aggregate ppw source
# fields have already been constructed by perturb_total_stress_energy(), and on
# model=2 the normal RTK production patch has inserted the neutral Khronon into
# delta_rho/rho_plus_p_theta/delta_p.
data_old = '''    class_store_double(dataptr, delta_scf, pba->has_scf, storeidx);\n    class_store_double(dataptr, theta_scf, pba->has_scf, storeidx);'''
data_new = data_old + '''\n\n    if (pba->model == 2.) {\n      double c10_a = pvecback[pba->index_bg_a];\n      double c10_H = pvecback[pba->index_bg_H];\n      double c10_Hp = pvecback[pba->index_bg_H_prime];\n      double c10_Hc = c10_a*c10_H;\n      double c10_Hcp = c10_a*c10_a*c10_H*c10_H + c10_a*c10_Hp;\n      double c10_rhob = pvecback[pba->index_bg_rho_b];\n      double c10_rhog = pvecback[pba->index_bg_rho_g];\n      double c10_rhour = (pba->has_ur == _TRUE_) ? pvecback[pba->index_bg_rho_ur] : 0.;\n      double c10_rhor = c10_rhog + c10_rhour;\n      double c10_H0 = c10_rhob + c10_rhor;\n      double c10_Dord = 3.*c10_rhob + 4.*c10_rhor;\n      double c10_H0p = -c10_Hc*c10_Dord;\n      double c10_H0pp = -c10_Hcp*c10_Dord\n        + c10_Hc*c10_Hc*(9.*c10_rhob + 16.*c10_rhor);\n      double c10_deltaH0 = c10_rhob*y[ppw->pv->index_pt_delta_b]\n        + c10_rhog*delta_g + c10_rhour*delta_ur;\n\n      khr_params c10_kp = {pba->H0,(pba->gnl>0.?pba->gnl:1.e-14),pba->lambda_D,pba->Omega0_cdm};\n      khr_closure c10_kc; khr_state c10_kb; int c10_ks;\n      double c10_rhok,c10_pk,c10_Wk,c10_Wtot,c10_rhotp,c10_ptp;\n      c10_ks=khr_closure_from_params(&c10_kp,&c10_kc);\n      class_test(c10_ks!=KHR_OK,error_message,"C10 exporter Khronon closure failed");\n      c10_ks=khr_background(&c10_kp,&c10_kc,c10_a/pba->a_today,k,&c10_kb);\n      class_test(c10_ks!=KHR_OK,error_message,"C10 exporter Khronon background failed");\n      c10_rhok=c10_kb.rho8piG/3.; c10_pk=c10_kb.p8piG/3.; c10_Wk=c10_rhok+c10_pk;\n      c10_Wtot=c10_rhob + (4./3.)*c10_rhor + c10_Wk;\n      c10_rhotp=-3.*c10_Hc*c10_Wtot;\n      c10_ptp=-(4./3.)*c10_Hc*c10_rhor - 3.*c10_Hc*c10_kb.ca2*c10_Wk;\n\n      class_store_double(dataptr,k,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_Hc,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_Hcp,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_H0,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_H0p,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_H0pp,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_deltaH0,_TRUE_,storeidx);\n      class_store_double(dataptr,ppw->delta_rho,_TRUE_,storeidx);\n      class_store_double(dataptr,ppw->rho_plus_p_theta,_TRUE_,storeidx);\n      class_store_double(dataptr,ppw->delta_p,_TRUE_,storeidx);\n      class_store_double(dataptr,ppw->rho_plus_p_shear,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_Wtot,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_rhotp,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_ptp,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_kb.w,_TRUE_,storeidx);\n      class_store_double(dataptr,c10_kb.ca2,_TRUE_,storeidx);\n    }'''
if data_old not in s:
    raise SystemExit("C10 exporter: scalar data anchor not found")
s = s.replace(data_old, data_new, 1)

pt.write_text(s)
print("C10_READONLY_SOURCE_EXPORT_PATCH_APPLIED")
