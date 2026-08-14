#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source/perturbations.c'
s=pt.read_text()

# Local diagnostics needed to preserve the exact Khronon adiabatic factor 1+w.
old='''  double rho_r,rho_m,rho_nu,rho_m_over_rho_r;\n  double fracnu,fracg,fracb,fraccdm,om;'''
new='''  double rho_r,rho_m,rho_nu,rho_m_over_rho_r;\n  double rho_khr_m=0.,w_khr_ini=0.;\n  double fracnu,fracg,fracb,fraccdm,om;'''
if old not in s: raise SystemExit('IC local declarations not found')
s=s.replace(old,new,1)

old='''    if (pba->has_cdm == _TRUE_) {\n      rho_m += ppw->pvecback[pba->index_bg_rho_cdm];\n    }'''
new='''    if (pba->has_cdm == _TRUE_) {\n      if (pba->model == 2.) {\n        khr_params kp_ic={pba->H0,(pba->gnl>0.?pba->gnl:1.e-14),pba->lambda_D,pba->Omega0_cdm};\n        khr_closure kc_ic; khr_state kb_ic; int ks_ic;\n        ks_ic=khr_closure_from_params(&kp_ic,&kc_ic);\n        class_test(ks_ic!=KHR_OK,ppt->error_message,"Khronon IC closure failed");\n        ks_ic=khr_background(&kp_ic,&kc_ic,a/pba->a_today,0.,&kb_ic);\n        class_test(ks_ic!=KHR_OK,ppt->error_message,"Khronon IC background failed");\n        rho_khr_m=(kb_ic.rho8piG-3.*kb_ic.p8piG)/3.;\n        w_khr_ini=kb_ic.w;\n        rho_m += rho_khr_m;\n      } else {\n        rho_m += ppw->pvecback[pba->index_bg_rho_cdm];\n      }\n    }'''
if old not in s: raise SystemExit('IC rho_m CDM block not found')
s=s.replace(old,new,1)

old='''    /* f_cdm = Omega_cdm(t_i) / Omega_m(t_i) */\n    fraccdm = 1.-fracb;'''
new='''    /* f_cdm slot = Khronon effective non-relativistic fraction for model=2 */\n    if ((pba->model == 2.) && (pba->has_cdm == _TRUE_))\n      fraccdm = rho_khr_m/rho_m;\n    else\n      fraccdm = 1.-fracb;'''
if old not in s: raise SystemExit('IC fraccdm block not found')
s=s.replace(old,new,1)

old='''      if (pba->has_cdm == _TRUE_) {\n        ppw->pv->y[ppw->pv->index_pt_delta_cdm] = 3./4.*ppw->pv->y[ppw->pv->index_pt_delta_g]; /* cdm density */\n        /* cdm velocity velocity vanishes in the synchronous gauge */\n      }'''
new='''      if (pba->has_cdm == _TRUE_) {\n        if (pba->model == 2.)\n          ppw->pv->y[ppw->pv->index_pt_delta_cdm] = khr_delta_adiabatic_from_photon(w_khr_ini,ppw->pv->y[ppw->pv->index_pt_delta_g]);\n        else\n          ppw->pv->y[ppw->pv->index_pt_delta_cdm] = 3./4.*ppw->pv->y[ppw->pv->index_pt_delta_g];\n        /* Khronon velocity has the dust growing-mode value at leading early-time order. */\n      }'''
if old not in s: raise SystemExit('adiabatic CDM IC block not found')
s=s.replace(old,new,1)

old='''      if (pba->has_cdm == _TRUE_) {\n        ppw->pv->y[ppw->pv->index_pt_delta_cdm] -= 3.*a_prime_over_a*alpha;\n        ppw->pv->y[ppw->pv->index_pt_theta_cdm] = k*k*alpha;\n      }'''
new='''      if (pba->has_cdm == _TRUE_) {\n        if (pba->model == 2.)\n          ppw->pv->y[ppw->pv->index_pt_delta_cdm] -= 3.*(1.+w_khr_ini)*a_prime_over_a*alpha;\n        else\n          ppw->pv->y[ppw->pv->index_pt_delta_cdm] -= 3.*a_prime_over_a*alpha;\n        ppw->pv->y[ppw->pv->index_pt_theta_cdm] = k*k*alpha;\n      }'''
if old not in s: raise SystemExit('Newtonian gauge CDM transform block not found')
s=s.replace(old,new,1)

# The current project supports Khronon adiabatic IC only; fail loudly instead of
# silently treating Khronon as a CDM isocurvature mode.
needle='''    /** (b) starts by setting everything in synchronous gauge. If\n        another gauge is needed, we will perform a gauge\n        transformation below. */'''
repl='''    class_test((pba->model == 2.) && (index_ic != ppt->index_ic_ad),\n               ppt->error_message,\n               "RT+DBI-Khronon currently supports adiabatic initial conditions only");\n\n    /** (b) starts by setting everything in synchronous gauge. If\n        another gauge is needed, we will perform a gauge\n        transformation below. */'''
if needle not in s: raise SystemExit('IC section marker not found')
s=s.replace(needle,repl,1)

pt.write_text(s)
print('RTK_INITIAL_CONDITIONS_UPGRADED')
