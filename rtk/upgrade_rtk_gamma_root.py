#!/usr/bin/env python3
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
bg=root/'source/background.c'
s=bg.read_text()
start_marker='    /**NonLocal recursive methods (secant, and Newtonian as a backup) to find the correct gamma*/'
end_marker='/**NonLocal verbose part moved here from background_solve*/'
start=s.find(start_marker)
end=s.find(end_marker,start)
if start<0 or end<0: raise SystemExit('nonlocal gamma tuner block not found')
old=s[start:end]
# Keep the published tuner untouched for model 1, but prevent it from running for model 2.
legacy=old.replace('if (pba->has_nlde == _TRUE_) {','if ((pba->has_nlde == _TRUE_) && (pba->model != 2.)) {',1)

rtk='''    /** RT+DBI-Khronon: positive, bracketed root in u=ln(gamma).\n        gamma=0 is not on the physical one-scale branch when Omega_K0>0. */\n    if ((pba->has_nlde == _TRUE_) && (pba->model == 2.)) {\n      double gamma_lo=1.e-12;\n      double gamma_hi=_GNL_HI_;\n      double u_lo=log(gamma_lo);\n      double u_hi=log(gamma_hi);\n      double u_mid=0.;\n      double f_lo=0.,f_hi=0.,f_mid=0.;\n      int i_rtk=0;\n\n      pba->gnl=gamma_lo;\n      class_call(background_solve(ppr,pba),pba->error_message,pba->error_message);\n      f_lo=(pba->background_table[(pba->bg_size)*(pba->bt_size-1)+pba->index_bg_H]-pba->H0)/pba->H0;\n\n      pba->gnl=gamma_hi;\n      class_call(background_solve(ppr,pba),pba->error_message,pba->error_message);\n      f_hi=(pba->background_table[(pba->bg_size)*(pba->bt_size-1)+pba->index_bg_H]-pba->H0)/pba->H0;\n\n      class_test(!isfinite(f_lo) || !isfinite(f_hi),pba->error_message,\n                 "RT+DBI-Khronon gamma bracket produced non-finite F: F(lo)=%e F(hi)=%e",f_lo,f_hi);\n      class_test(f_lo*f_hi>0.,pba->error_message,\n                 "RT+DBI-Khronon gamma root is not bracketed on [%e,%e]: F(lo)=%e F(hi)=%e",\n                 gamma_lo,gamma_hi,f_lo,f_hi);\n\n      while (i_rtk<_MAXS_) {\n        u_mid=0.5*(u_lo+u_hi);\n        pba->gnl=exp(u_mid);\n        class_call(background_solve(ppr,pba),pba->error_message,pba->error_message);\n        f_mid=(pba->background_table[(pba->bg_size)*(pba->bt_size-1)+pba->index_bg_H]-pba->H0)/pba->H0;\n        class_test(!isfinite(f_mid),pba->error_message,\n                   "RT+DBI-Khronon gamma root produced non-finite F at gamma=%e",pba->gnl);\n        if (fabs(f_mid)<=_TOLH_) break;\n        if (f_lo*f_mid<=0.) { u_hi=u_mid; f_hi=f_mid; }\n        else { u_lo=u_mid; f_lo=f_mid; }\n        i_rtk++;\n      }\n      class_test(fabs(f_mid)>_TOLH_,pba->error_message,\n                 "RT+DBI-Khronon positive log-gamma root failed after %d steps: gamma=%e F=%e",\n                 i_rtk,pba->gnl,f_mid);\n      printf("RTK_LOG_GAMMA_ROOT steps=%d gamma=%.12e F=%.12e bracket=[%.12e,%.12e]\\n",\n             i_rtk,pba->gnl,f_mid,exp(u_lo),exp(u_hi));\n    }\n\n'''
s=s[:start]+rtk+legacy+s[end:]
bg.write_text(s)
print('RTK_POSITIVE_LOG_GAMMA_ROOT_APPLIED')
