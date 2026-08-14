#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source/perturbations.c'
s=pt.read_text()

old='''      if (pba->has_cdm == _TRUE_) {\n        delta_rho_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_delta_cdm];\n        rho_m += ppw->pvecback[pba->index_bg_rho_cdm];\n      }'''
new='''      if (pba->has_cdm == _TRUE_) {\n        if (pba->model == 2.) {\n          /* For the generalized-dark-matter Khronon the CLASS matter\n             bookkeeping uses rho_m,K=rho_K-3 P_K and its perturbation\n             delta rho_m,K=delta rho_K-3 delta P_K. */\n          khr_params kp_m={pba->H0,(pba->gnl>0.?pba->gnl:1.e-14),pba->lambda_D,pba->Omega0_cdm};\n          khr_closure kc_m; khr_state kb_m; khr_pert_state ky_m; khr_class_sources ks_m; int kstat_m;\n          kstat_m=khr_closure_from_params(&kp_m,&kc_m);\n          class_test(kstat_m!=KHR_OK,ppt->error_message,"Khronon matter-source closure failed");\n          kstat_m=khr_background(&kp_m,&kc_m,a/pba->a_today,k,&kb_m);\n          class_test(kstat_m!=KHR_OK,ppt->error_message,"Khronon matter-source background failed");\n          ky_m.delta=y[ppw->pv->index_pt_delta_cdm];\n          ky_m.theta=y[ppw->pv->index_pt_theta_cdm];\n          kstat_m=khr_class_sources_newtonian(&kb_m,&ky_m,a*ppw->pvecback[pba->index_bg_H],&ks_m);\n          class_test(kstat_m!=KHR_OK,ppt->error_message,"Khronon matter sources failed");\n          delta_rho_m += ks_m.delta_rho_class-3.*ks_m.delta_p_class;\n          rho_m += ks_m.rho_class-3.*ks_m.p_class;\n        } else {\n          delta_rho_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_delta_cdm];\n          rho_m += ppw->pvecback[pba->index_bg_rho_cdm];\n        }\n      }'''
if old not in s: raise SystemExit('delta_m CDM aggregation block not found')
s=s.replace(old,new,1)

old='''      if (pba->has_cdm == _TRUE_) {\n        if (ppt->gauge == newtonian)\n          rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];\n        rho_plus_p_m += ppw->pvecback[pba->index_bg_rho_cdm];\n      }'''
new='''      if (pba->has_cdm == _TRUE_) {\n        if (pba->model == 2.) {\n          khr_params kp_tm={pba->H0,(pba->gnl>0.?pba->gnl:1.e-14),pba->lambda_D,pba->Omega0_cdm};\n          khr_closure kc_tm; khr_state kb_tm; int kstat_tm; double rhop_tm;\n          kstat_tm=khr_closure_from_params(&kp_tm,&kc_tm);\n          class_test(kstat_tm!=KHR_OK,ppt->error_message,"Khronon theta_m closure failed");\n          kstat_tm=khr_background(&kp_tm,&kc_tm,a/pba->a_today,k,&kb_tm);\n          class_test(kstat_tm!=KHR_OK,ppt->error_message,"Khronon theta_m background failed");\n          rhop_tm=(kb_tm.rho8piG+kb_tm.p8piG)/3.;\n          if (ppt->gauge == newtonian)\n            rho_plus_p_theta_m += rhop_tm*y[ppw->pv->index_pt_theta_cdm];\n          rho_plus_p_m += rhop_tm;\n        } else {\n          if (ppt->gauge == newtonian)\n            rho_plus_p_theta_m += ppw->pvecback[pba->index_bg_rho_cdm]*y[ppw->pv->index_pt_theta_cdm];\n          rho_plus_p_m += ppw->pvecback[pba->index_bg_rho_cdm];\n        }\n      }'''
if old not in s: raise SystemExit('theta_m CDM aggregation block not found')
s=s.replace(old,new,1)

pt.write_text(s)
print('RTK_MATTER_SOURCES_UPGRADED')
