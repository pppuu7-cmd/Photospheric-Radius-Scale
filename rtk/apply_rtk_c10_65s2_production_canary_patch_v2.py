#!/usr/bin/env python3
"""Compile-fix wrapper for C10.65s2 production patch; no physics/criteria changes.

The v1 generator omitted the thermo pointer from the generated bridge's private
current-state evaluator and omitted the short-step accessor prototype.  This
wrapper applies v1, then repairs only those C signatures/call sites before build.
"""
from pathlib import Path
import subprocess,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public').resolve()
base=Path(__file__).resolve().with_name('apply_rtk_c10_65s2_production_canary_patch.py')
subprocess.run([sys.executable,str(base),str(root)],check=True)

h=root/'include'/'rtk_c10_65s2_class_bridge.h'; c=root/'source'/'rtk_c10_65s2_class_bridge.c'; p=root/'source'/'perturbations.c'
hs=h.read_text(); cs=c.read_text(); ps=p.read_text()

hs=hs.replace('int rtk_c10_65s2_cdm_rhs(struct background*,struct perturbs*,int,double,double*,double*,struct perturb_workspace*,ErrorMsg);',
              'int rtk_c10_65s2_cdm_rhs(struct background*,struct thermo*,struct perturbs*,int,double,double*,double*,struct perturb_workspace*,ErrorMsg);')
hs=hs.replace('int rtk_c10_65s2_observe(const char*,double,double*,double*,void*,ErrorMsg);',
              'double rtk_c10_65s2_short_dt(void);\nint rtk_c10_65s2_observe(const char*,double,double*,double*,void*,ErrorMsg);')

cs=cs.replace('static int eval(struct background *pba,struct perturbs *ppt,int index_md,double k,double *y,struct perturb_workspace *ppw,rtk_c10_65s2_output *o,ErrorMsg error_message)',
              'static int eval(struct background *pba,struct thermo *pth,struct perturbs *ppt,int index_md,double k,double *y,struct perturb_workspace *ppw,rtk_c10_65s2_output *o,ErrorMsg error_message)')
cs=cs.replace('class_call(eval(pba,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);',
              'class_call(eval(pba,pth,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);',1)
cs=cs.replace('int rtk_c10_65s2_cdm_rhs(struct background *pba,struct perturbs *ppt,int index_md,double k,double *y,double *dy,struct perturb_workspace *ppw,ErrorMsg error_message)',
              'int rtk_c10_65s2_cdm_rhs(struct background *pba,struct thermo *pth,struct perturbs *ppt,int index_md,double k,double *y,double *dy,struct perturb_workspace *ppw,ErrorMsg error_message)')
# second private eval call belongs to cdm_rhs
needle='class_call(eval(pba,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);'
if needle in cs:
    cs=cs.replace(needle,'class_call(eval(pba,pth,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);',1)
# observer obtains pth from ppaw
cs=cs.replace('class_call(eval(pba,ppt,ppaw->index_md,ppaw->k,y,ppw,&o,error_message),error_message,error_message);',
              'class_call(eval(pba,ppaw->pth,ppt,ppaw->index_md,ppaw->k,y,ppw,&o,error_message),error_message,error_message);')

ps=ps.replace('rtk_c10_65s2_cdm_rhs(pba,ppt,index_md,k,y,dy,ppw,error_message)',
              'rtk_c10_65s2_cdm_rhs(pba,pth,ppt,index_md,k,y,dy,ppw,error_message)')

h.write_text(hs); c.write_text(cs); p.write_text(ps)
print('C10_65S2_PRODUCTION_CANARY_PATCH_V2_APPLIED')
