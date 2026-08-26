#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
hdr=root/'include/background.h'
inc=root/'source/input.c'
pt=root/'source/perturbations.c'
mk=root/'Makefile'
hs=hdr.read_text(); ins=inc.read_text(); ps=pt.read_text(); ms=mk.read_text()
marker='RTK_C10_65R2G_SEPARATE_NOINLINE_OBSERVER_V1'
if marker in ps:
    print('C10_65R2G_SEPARATE_OBSERVER_ALREADY_APPLIED')
    raise SystemExit(0)
if 'RTK_C10_65R1_IN_CLASS_COMPLETED_PROJECTOR_PARITY_V1' not in ps:
    raise SystemExit('C10.65r2g requires r1 patch first')
if not (root/'source/rtk_c10_65r2_observer.c').exists() or not (root/'include/rtk_c10_65r2_observer.h').exists():
    raise SystemExit('copy rtk_c10_65r2_observer.c/.h into the disposable CLASS tree first')

if 'double c10_65r2_diag;' not in hs:
    needle='  double c10_65r1_Mc;'; pos=hs.find(needle)
    if pos<0: raise SystemExit('C10.65r2g background anchor missing')
    eol=hs.find('\n',pos); hs=hs[:eol+1]+'  double c10_65r2_diag;/** C10.65r2 dormant first-RHS diagnostic flag */\n'+hs[eol+1:]
if 'pba->c10_65r2_diag = 0.;' not in ins:
    needle='  pba->c10_65r1_Mc = 1.;'; pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r2g default anchor missing')
    eol=ins.find('\n',pos); ins=ins[:eol+1]+'  pba->c10_65r2_diag = 0.;\n'+ins[eol+1:]
if 'class_read_double("c10_65r2_diag",pba->c10_65r2_diag);' not in ins:
    needle='  class_read_double("c10_65r1_Mc",pba->c10_65r1_Mc);'; pos=ins.find(needle)
    if pos<0: raise SystemExit('C10.65r2g parser anchor missing')
    eol=ins.find('\n',pos)
    add=('  class_read_double("c10_65r2_diag",pba->c10_65r2_diag);\n'
         '  class_test((pba->c10_65r2_diag != 0.) && (pba->c10_65r2_diag != 1.),errmsg,"c10_65r2_diag must be 0 or 1");\n')
    ins=ins[:eol+1]+add+ins[eol+1:]

# Stable pinned upstream include anchor; only a prototype is added here.
inc_anchor='#include "perturbations.h"'
if '#include "rtk_c10_65r2_observer.h"' not in ps:
    if inc_anchor not in ps: raise SystemExit('C10.65r2g include anchor missing')
    ps=ps.replace(inc_anchor,inc_anchor+'\n#include "rtk_c10_65r2_observer.h"',1)

cond='(pba->model == 2.) && (pba->c10_65r1_diag > 0.5) && (pba->c10_65r2_diag > 0.5)'
title_anchor='      class_store_columntitle(ppt->scalar_titles,"c10_65r1_shear_feedback_den",(pba->model == 2.) && (pba->c10_65r1_diag > 0.5));'
if 'c10_65r2_B_general' not in ps:
    if title_anchor not in ps: raise SystemExit('C10.65r2g r1 title anchor missing')
    titles=f'''
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_B_general",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_B_prime",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_B_prime_actual",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_Psi_N_prime",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_metric_continuity_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_metric_euler_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_tca_slip_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_b_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_g_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_ur_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_delta_khr_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_theta_khr_prime_shadow",{cond});
      class_store_columntitle(ppt->scalar_titles,"c10_65r2_weighted_slip_cancel",{cond});'''
    ps=ps.replace(title_anchor,title_anchor+titles,1)

store_anchor='        class_store_double(dataptr,r1_feedback,_TRUE_,storeidx);'
if 'rtk_c10_65r2_observe(pba,pth,ppw,k,dataptr,&storeidx);' not in ps:
    if ps.count(store_anchor)!=1: raise SystemExit(f'C10.65r2g expected one r1 final-store anchor, found {ps.count(store_anchor)}')
    call=('\n        /* '+marker+': diagnostic-only external observer after r1 materialization. */\n'
          '        rtk_c10_65r2_observe(pba,pth,ppw,k,dataptr,&storeidx);')
    ps=ps.replace(store_anchor,store_anchor+call,1)

if 'rtk_c10_65r2_observer.o' not in ms:
    needle='khronon_background.o khronon_perturbations.o'
    if needle not in ms: raise SystemExit('C10.65r2g Makefile RTK object anchor missing')
    ms=ms.replace(needle,needle+' rtk_c10_65r2_observer.o',1)

hdr.write_text(hs); inc.write_text(ins); pt.write_text(ps); mk.write_text(ms)
print('C10_65R2G_SEPARATE_NOINLINE_OBSERVER_APPLIED')
