#!/usr/bin/env python3
"""C10.65r0: add a dormant-by-default local environment export to pinned RTK CLASS.

Apply only to a disposable diagnostic tree after the normal RTK input upgrade and
the C10.65a/C10.65e read-only output patches.  With c10_65r0_diag omitted (the
default), no new output columns are stored and no dynamics are changed.  With
c10_65r0_diag=1, the perturbation-output path appends the local background/TCA
quantities needed by the detached completed-U1 seed.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
hdr=root/'include'/'background.h'
inc=root/'source'/'input.c'
pt=root/'source'/'perturbations.c'
hs=hdr.read_text(); ins=inc.read_text(); ps=pt.read_text()
marker='RTK_C10_65R0_OPT_IN_LOCAL_ENVIRONMENT_EXPORT_V1'
if marker in ps:
    print('C10_65R0_PATCH_ALREADY_APPLIED')
    raise SystemExit(0)

# Runtime flag: use the already RTK-upgraded background/input struct.  Keep it a
# double to follow the public nonlocal branch parser conventions used by model and
# lambda_D.  The default is exactly zero.
if 'double c10_65r0_diag;' not in hs:
    needle='  double lambda_D;'
    pos=hs.find(needle)
    if pos<0: raise SystemExit('C10.65r0 requires upgrade_rtk_inputs.py first (lambda_D field missing)')
    eol=hs.find('\n',pos)
    hs=hs[:eol+1]+'  double c10_65r0_diag;/** C10.65r0 dormant diagnostic output flag */\n'+hs[eol+1:]

if 'pba->c10_65r0_diag = 0.;' not in ins:
    needle='pba->lambda_D = 1.e4;'
    pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r0 default anchor not found')
    eol=ins.find('\n',pos)
    ins=ins[:eol+1]+'  pba->c10_65r0_diag = 0.; /* dormant by default */\n'+ins[eol+1:]

if 'class_read_double("c10_65r0_diag",pba->c10_65r0_diag);' not in ins:
    needle='class_read_double("lambda_D",pba->lambda_D);'
    pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r0 parser anchor not found')
    eol=ins.find('\n',pos)
    ins=ins[:eol+1]+'  class_read_double("c10_65r0_diag",pba->c10_65r0_diag);\n  class_test((pba->c10_65r0_diag != 0.) && (pba->c10_65r0_diag != 1.),errmsg,"c10_65r0_diag must be 0 or 1");\n'+ins[eol+1:]

# Title block: conditional storage means the default OFF output schema is exactly
# the same as the already-certified C10.65e diagnostic tree.
title_anchor='      class_store_columntitle(ppt->scalar_titles,"c10_65e_has_perturbed_recombination",pba->model == 2.);'
if title_anchor not in ps:
    raise SystemExit('C10.65r0 title anchor missing; apply C10.65e patch first')
titles='''
      /* RTK_C10_65R0_OPT_IN_LOCAL_ENVIRONMENT_EXPORT_V1: read-only diagnostic. */
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_a",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_Hc",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_rho_b",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_rho_g",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_rho_ur",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_R",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_cb2",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_dkappa",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_ddkappa",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_tau_c",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_dtau_c",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_F",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_F_prime",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));
      class_store_columntitle(ppt->scalar_titles,"c10_65r0_tca_flag",(pba->model == 2.) && (pba->c10_65r0_diag > 0.5));'''
ps=ps.replace(title_anchor,title_anchor+titles,1)

# Data block: recompute from the same local pvecback/pvecthermo/approx objects used
# by CLASS itself.  The formulas intentionally duplicate the source-locked C10.65e
# pack so r0 can test the future bridge interface independently.
data_anchor='''        class_store_double(dataptr,(double)ppt->has_perturbed_recombination,_TRUE_,storeidx);
      }'''
if data_anchor not in ps:
    raise SystemExit('C10.65r0 data anchor missing; apply C10.65e patch first')
data='''
      if ((pba->model == 2.) && (pba->c10_65r0_diag > 0.5)) {
        double r0_a = pvecback[pba->index_bg_a];
        double r0_Hc = r0_a*pvecback[pba->index_bg_H];
        double r0_rhob = pvecback[pba->index_bg_rho_b];
        double r0_rhog = pvecback[pba->index_bg_rho_g];
        double r0_rhour = pvecback[pba->index_bg_rho_ur];
        double r0_R = (4./3.)*r0_rhog/r0_rhob;
        double r0_cb2 = ppw->pvecthermo[pth->index_th_cb2];
        double r0_dkappa = ppw->pvecthermo[pth->index_th_dkappa];
        double r0_ddkappa = ppw->pvecthermo[pth->index_th_ddkappa];
        double r0_tau_c;
        double r0_dtau_c;
        double r0_F;
        double r0_F_prime;
        class_test(r0_rhob <= 0. || r0_rhog <= 0. || r0_rhour <= 0.,error_message,"C10.65r0 requires positive b/g/ur densities");
        class_test(r0_dkappa <= 0.,error_message,"C10.65r0 requires positive dkappa");
        r0_tau_c = 1./r0_dkappa;
        r0_dtau_c = -r0_ddkappa*r0_tau_c*r0_tau_c;
        r0_F = r0_tau_c/(1.+r0_R);
        r0_F_prime = r0_dtau_c/(1.+r0_R) + r0_tau_c*r0_Hc*r0_R/(1.+r0_R)/(1.+r0_R);
        class_store_double(dataptr,r0_a,_TRUE_,storeidx);
        class_store_double(dataptr,r0_Hc,_TRUE_,storeidx);
        class_store_double(dataptr,r0_rhob,_TRUE_,storeidx);
        class_store_double(dataptr,r0_rhog,_TRUE_,storeidx);
        class_store_double(dataptr,r0_rhour,_TRUE_,storeidx);
        class_store_double(dataptr,r0_R,_TRUE_,storeidx);
        class_store_double(dataptr,r0_cb2,_TRUE_,storeidx);
        class_store_double(dataptr,r0_dkappa,_TRUE_,storeidx);
        class_store_double(dataptr,r0_ddkappa,_TRUE_,storeidx);
        class_store_double(dataptr,r0_tau_c,_TRUE_,storeidx);
        class_store_double(dataptr,r0_dtau_c,_TRUE_,storeidx);
        class_store_double(dataptr,r0_F,_TRUE_,storeidx);
        class_store_double(dataptr,r0_F_prime,_TRUE_,storeidx);
        class_store_double(dataptr,(double)ppw->approx[ppw->index_ap_tca],_TRUE_,storeidx);
      }'''
ps=ps.replace(data_anchor,data_anchor+data,1)

hdr.write_text(hs); inc.write_text(ins); pt.write_text(ps)
print('C10_65R0_OPT_IN_LOCAL_ENVIRONMENT_EXPORT_PATCH_APPLIED')
