#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
bg=root/'source/background.c'; pt=root/'source/perturbations.c'; mk=root/'Makefile'
bs=bg.read_text(); ps=pt.read_text(); ms=mk.read_text()

if '#include "khronon_background.h"' not in bs:
    bs=bs.replace('#include "background.h"','#include "background.h"\n#include "khronon_background.h"',1)
if '#include "khronon_perturbations.h"' not in ps:
    ps=ps.replace('#include "perturbations.h"','#include "perturbations.h"\n#include "khronon_perturbations.h"',1)

old='''  /* cdm */\n  if (pba->has_cdm == _TRUE_) {\n    pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a_rel,3);\n/**NonLocal*/    rho_H += pvecback[pba->index_bg_rho_cdm];\n    rho_tot += pvecback[pba->index_bg_rho_cdm];\n    p_tot += 0.;\n    rho_m += pvecback[pba->index_bg_rho_cdm];\n  }'''
new='''  /* cdm slot: in RT+Khronon model=2 this slot is repurposed as DBI-Khronon */\n  if (pba->has_cdm == _TRUE_) {\n    if (pba->model == 2.) {\n      khr_params kp = {pba->H0, (pba->gnl > 0. ? pba->gnl : 1.e-14), 1.e4, pba->Omega0_cdm};\n      khr_closure kc; khr_state ks; int kstat;\n      kstat = khr_closure_from_params(&kp,&kc);\n      class_test(kstat != KHR_OK,pba->error_message,"Khronon closure failed: %s",khr_status_string(kstat));\n      kstat = khr_background(&kp,&kc,a_rel,0.,&ks);\n      class_test(kstat != KHR_OK,pba->error_message,"Khronon background failed: %s",khr_status_string(kstat));\n      pvecback[pba->index_bg_rho_cdm] = ks.rho8piG/3.;\n/**NonLocal*/      rho_H += ks.rho8piG/3.;\n/**NonLocal*/      p_H += ks.p8piG/3.;\n      rho_tot += ks.rho8piG/3.;\n      p_tot += ks.p8piG/3.;\n      rho_m += (ks.rho8piG-3.*ks.p8piG)/3.;\n    } else {\n      pvecback[pba->index_bg_rho_cdm] = pba->Omega0_cdm * pow(pba->H0,2) / pow(a_rel,3);\n/**NonLocal*/      rho_H += pvecback[pba->index_bg_rho_cdm];\n      rho_tot += pvecback[pba->index_bg_rho_cdm];\n      p_tot += 0.;\n      rho_m += pvecback[pba->index_bg_rho_cdm];\n    }\n  }'''
if old not in bs: raise SystemExit('background cdm block not found')
bs=bs.replace(old,new,1)

old='''    /* cdm contribution */\n    if (pba->has_cdm == _TRUE_) {\n      ppw->delta_rho = ppw->delta_rho + ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_delta_cdm];\n      if (ppt->gauge == newtonian)\n        ppw->rho_plus_p_theta = ppw->rho_plus_p_theta + ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];\n    }'''
new='''    /* cdm slot / DBI-Khronon contribution */\n    if (pba->has_cdm == _TRUE_) {\n      if (pba->model == 2.) {\n        khr_params kp = {pba->H0,(pba->gnl > 0. ? pba->gnl : 1.e-14),1.e4,pba->Omega0_cdm};\n        khr_closure kc; khr_state kb; khr_pert_state ky; khr_class_sources ks; int kstat;\n        kstat=khr_closure_from_params(&kp,&kc);\n        class_test(kstat != KHR_OK,ppt->error_message,"Khronon closure failed in stress tensor");\n        kstat=khr_background(&kp,&kc,a/pba->a_today,k,&kb);\n        class_test(kstat != KHR_OK,ppt->error_message,"Khronon background failed in stress tensor");\n        ky.delta=y[ppw->pv->index_pt_delta_cdm]; ky.theta=y[ppw->pv->index_pt_theta_cdm];\n        kstat=khr_class_sources_newtonian(&kb,&ky,a*ppw->pvecback[pba->index_bg_H],&ks);\n        class_test(kstat != KHR_OK,ppt->error_message,"Khronon sources failed");\n        ppw->delta_rho += ks.delta_rho_class;\n        ppw->rho_plus_p_theta += ks.momentum_class;\n        ppw->delta_p += ks.delta_p_class;\n      } else {\n        ppw->delta_rho += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_delta_cdm];\n        if (ppt->gauge == newtonian)\n          ppw->rho_plus_p_theta += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];\n      }\n    }'''
if old not in ps: raise SystemExit('stress cdm block not found')
ps=ps.replace(old,new,1)

old='''    /** -> cdm */\n\n    if (pba->has_cdm == _TRUE_) {\n\n      /** ---> newtonian gauge: cdm density and velocity */\n\n      if (ppt->gauge == newtonian) {\n        dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity); /* cdm density */\n\n        dy[pv->index_pt_theta_cdm] = - a_prime_over_a*y[pv->index_pt_theta_cdm] + metric_euler; /* cdm velocity */\n      }\n\n      /** ---> synchronous gauge: cdm density only (velocity set to zero by definition of the gauge) */\n\n      if (ppt->gauge == synchronous) {\n        dy[pv->index_pt_delta_cdm] = -metric_continuity; /* cdm density */\n      }\n\n    }'''
new='''    /** -> cdm slot / DBI-Khronon */\n\n    if (pba->has_cdm == _TRUE_) {\n      if ((pba->model == 2.) && (ppt->gauge == newtonian)) {\n        khr_params kp = {pba->H0,(pba->gnl > 0. ? pba->gnl : 1.e-14),1.e4,pba->Omega0_cdm};\n        khr_closure kc; khr_state kb; khr_pert_state ky; khr_metric_sources km; khr_pert_derivs kd; int kstat;\n        kstat=khr_closure_from_params(&kp,&kc);\n        class_test(kstat != KHR_OK,error_message,"Khronon closure failed in derivatives");\n        kstat=khr_background(&kp,&kc,a/pba->a_today,k,&kb);\n        class_test(kstat != KHR_OK,error_message,"Khronon background failed in derivatives");\n        ky.delta=y[pv->index_pt_delta_cdm]; ky.theta=y[pv->index_pt_theta_cdm];\n        km.Hc=a_prime_over_a; km.phi_prime=-metric_continuity/3.; km.psi=metric_euler/k2;\n        kstat=khr_perturb_derivs_newtonian(&kb,&ky,&km,&kd);\n        class_test(kstat != KHR_OK,error_message,"Khronon perturbation derivative failed");\n        dy[pv->index_pt_delta_cdm]=kd.delta_prime; dy[pv->index_pt_theta_cdm]=kd.theta_prime;\n      } else if (ppt->gauge == newtonian) {\n        dy[pv->index_pt_delta_cdm] = -(y[pv->index_pt_theta_cdm]+metric_continuity);\n        dy[pv->index_pt_theta_cdm] = -a_prime_over_a*y[pv->index_pt_theta_cdm]+metric_euler;\n      } else if (ppt->gauge == synchronous) {\n        dy[pv->index_pt_delta_cdm] = -metric_continuity;\n      }\n    }'''
if old not in ps: raise SystemExit('derivative cdm block not found')
ps=ps.replace(old,new,1)

src='SOURCE = input.o background.o thermodynamics.o perturbations.o primordial.o nonlinear.o transfer.o spectra.o lensing.o'
if 'khronon_background.o' not in ms:
    if src not in ms: raise SystemExit('Makefile SOURCE not found')
    ms=ms.replace(src,src+' khronon_background.o khronon_perturbations.o',1)

bg.write_text(bs); pt.write_text(ps); mk.write_text(ms)
print('RTK_PATCH_APPLIED')
