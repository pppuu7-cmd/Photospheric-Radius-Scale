#!/usr/bin/env python3
"""Append C10.65e read-only tight-coupling coefficient diagnostics.

Apply after the C10 source-export and C10.65a species-control patches to a
disposable pinned CLASS tree. This patch adds perturbation-output columns only;
it does not alter any background, thermodynamics, collision, perturbation or
gravity equation.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
s=pt.read_text()
marker='RTK_C10_65E_TCA_COEFFICIENT_EXPORT_V1'
if marker in s:
    print('C10_65E_TCA_COEFFICIENT_PATCH_ALREADY_APPLIED')
    raise SystemExit(0)

title_old='''      class_store_columntitle(ppt->scalar_titles,"c10_65a_shear_ur",pba->model == 2.);'''
title_new=title_old+'''\n      /* RTK_C10_65E_TCA_COEFFICIENT_EXPORT_V1: diagnostics only; no dynamics changed. */\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_R",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_cb2",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_dkappa",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_ddkappa",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_tau_c",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_dtau_c",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_F",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_F_prime",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_tca_flag",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_tau_c_over_tau_h",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_tau_c_over_tau_k",pba->model == 2.);\n      class_store_columntitle(ppt->scalar_titles,"c10_65e_has_perturbed_recombination",pba->model == 2.);'''
if title_old not in s:
    raise SystemExit('C10.65e title anchor not found; apply C10.65a species-control patch first')
s=s.replace(title_old,title_new,1)

# Unique C10.65a tail: unlike the standard scalar output, these five stores are
# contiguous because the standard perturbed-recombination columns are not between
# phi and the UR controls here.
data_old='''      class_store_double(dataptr,psi,_TRUE_,storeidx);\n      class_store_double(dataptr,phi,_TRUE_,storeidx);\n      class_store_double(dataptr,delta_ur,pba->has_ur,storeidx);\n      class_store_double(dataptr,theta_ur,pba->has_ur,storeidx);\n      class_store_double(dataptr,shear_ur,pba->has_ur,storeidx);'''
data_new=data_old+'''\n      if (pba->model == 2.) {\n        double c10_65e_a = pvecback[pba->index_bg_a];\n        double c10_65e_Hc = c10_65e_a*pvecback[pba->index_bg_H];\n        double c10_65e_R = (4./3.)*pvecback[pba->index_bg_rho_g]/pvecback[pba->index_bg_rho_b];\n        double c10_65e_cb2 = ppw->pvecthermo[pth->index_th_cb2];\n        double c10_65e_dkappa = ppw->pvecthermo[pth->index_th_dkappa];\n        double c10_65e_ddkappa = ppw->pvecthermo[pth->index_th_ddkappa];\n        double c10_65e_tau_c;\n        double c10_65e_dtau_c;\n        double c10_65e_F;\n        double c10_65e_F_prime;\n        class_test(c10_65e_dkappa <= 0.,error_message,"C10.65e requires positive dkappa");\n        c10_65e_tau_c = 1./c10_65e_dkappa;\n        c10_65e_dtau_c = -c10_65e_ddkappa*c10_65e_tau_c*c10_65e_tau_c;\n        c10_65e_F = c10_65e_tau_c/(1.+c10_65e_R);\n        c10_65e_F_prime = c10_65e_dtau_c/(1.+c10_65e_R)\n          + c10_65e_tau_c*c10_65e_Hc*c10_65e_R/(1.+c10_65e_R)/(1.+c10_65e_R);\n        class_store_double(dataptr,c10_65e_R,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_cb2,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_dkappa,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_ddkappa,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_tau_c,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_dtau_c,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_F,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_F_prime,_TRUE_,storeidx);\n        class_store_double(dataptr,(double)ppw->approx[ppw->index_ap_tca],_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_tau_c*c10_65e_Hc,_TRUE_,storeidx);\n        class_store_double(dataptr,c10_65e_tau_c*k,_TRUE_,storeidx);\n        class_store_double(dataptr,(double)ppt->has_perturbed_recombination,_TRUE_,storeidx);\n      }'''
if data_old not in s:
    raise SystemExit('C10.65e unique C10.65a data anchor not found')
if s.count(data_old) != 1:
    raise SystemExit(f'C10.65e expected unique data anchor, found {s.count(data_old)}')
s=s.replace(data_old,data_new,1)
pt.write_text(s)
print('C10_65E_TCA_COEFFICIENT_PATCH_APPLIED')
