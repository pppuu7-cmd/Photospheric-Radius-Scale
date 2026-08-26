#!/usr/bin/env python3
"""C10.65s2 production patch v3: RTK-base anchor compatibility only.

No physics or frozen criteria change. The original v1 assumed the pristine CLASS
CDM derivative text, but the disposable production tree already contains the RTK
model=2 Khronon derivative branch from apply_rtk_class_patch.py. This wrapper
executes a temporary v1 whose CDM insertion is anchored immediately before that
existing RTK branch, preserving it verbatim as the OFF fallback. It also carries
the v2 compile-only thermo/prototype fixes.
"""
from pathlib import Path
import subprocess,sys,tempfile

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public').resolve()
v1=Path(__file__).resolve().with_name('apply_rtk_c10_65s2_production_canary_patch.py')
src=v1.read_text()
start=src.index('# Khronon production RHS:')
end=src.index('# One-step canary',start)
replacement=r"""# Khronon production RHS: branch before the RTK-base model=2 Khronon fallback.
cdm_anchor='''      if ((pba->model == 2.) && (ppt->gauge == newtonian)) {
        khr_params kp ='''
cdm_new='''      if ((pba->model == 2.) && (ppt->gauge == newtonian) && (ppw->c10_65s2_active == 1) && rtk_c10_65s2_mode_enabled(pba,ppt,index_md,k)) {
        class_call(rtk_c10_65s2_cdm_rhs(pba,pth,ppt,index_md,k,y,dy,ppw,error_message),error_message,error_message);
      } else if ((pba->model == 2.) && (ppt->gauge == newtonian)) {
        khr_params kp ='''
if cdm_anchor not in ps: raise SystemExit('RTK-patched CDM derivative anchor missing')
ps=ps.replace(cdm_anchor,cdm_new,1)

"""
src=src[:start]+replacement+src[end:]
with tempfile.NamedTemporaryFile('w',suffix='.py',delete=False) as tf:
    tf.write(src); tmp=tf.name
subprocess.run([sys.executable,'-m','py_compile',tmp],check=True)
subprocess.run([sys.executable,tmp,str(root)],check=True)
Path(tmp).unlink(missing_ok=True)

# Carry the v2 compile-only signature fixes into the generated disposable tree.
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
needle='class_call(eval(pba,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);'
if needle in cs:
    cs=cs.replace(needle,'class_call(eval(pba,pth,ppt,index_md,k,y,ppw,&o,error_message),error_message,error_message);',1)
cs=cs.replace('class_call(eval(pba,ppt,ppaw->index_md,ppaw->k,y,ppw,&o,error_message),error_message,error_message);',
              'class_call(eval(pba,ppaw->pth,ppt,ppaw->index_md,ppaw->k,y,ppw,&o,error_message),error_message,error_message);')
ps=ps.replace('rtk_c10_65s2_cdm_rhs(pba,ppt,index_md,k,y,dy,ppw,error_message)',
              'rtk_c10_65s2_cdm_rhs(pba,pth,ppt,index_md,k,y,dy,ppw,error_message)')
h.write_text(hs); c.write_text(cs); p.write_text(ps)
print('C10_65S2_PRODUCTION_CANARY_PATCH_V3_APPLIED')
