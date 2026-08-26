#!/usr/bin/env python3
"""C10.65s2i diagnostics only; no integration mutation."""
from pathlib import Path
import sys
r=Path(sys.argv[1]).resolve(); h=r/'include/dei_rkck.h'; c=r/'tools/dei_rkck.c'; p=r/'source/perturbations.c'
hs=h.read_text(); cs=c.read_text(); ps=p.read_text()
if 'RTK_C10_65S2I_TRACE_V1' in cs: raise SystemExit(0)
hs=hs.replace('  int initialize_generic_integrator(\n','  void rtk_c10_65s2i_trace_begin(double k);\n  void rtk_c10_65s2i_trace_end(void);\n\n  int initialize_generic_integrator(\n',1)
cs=cs.replace('#include "dei_rkck.h"\n',r'''#include "dei_rkck.h"
#include <stdio.h>
#include <stdlib.h>
/* RTK_C10_65S2I_TRACE_V1: diagnostics only; no integration mutation. */
static int s2i_on=0; static double s2i_k=0.;
static void s2i_write(const char *q,double x0,double x1,double ht,double hd,double hn,int nr,double er){const char *n=getenv("RTK_C10_65S2I_TRACE_FILE");FILE *f;if(!s2i_on||!n||!*n)return;f=fopen(n,"a");if(!f)return;fprintf(f,"%s,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%d,%.17e\n",q,s2i_k,x0,x1,ht,hd,hn,nr,er);fclose(f);}
void rtk_c10_65s2i_trace_begin(double k){const char *n=getenv("RTK_C10_65S2I_TRACE_FILE");FILE *f;s2i_k=k;s2i_on=1;if(!n||!*n)return;f=fopen(n,"a");if(f){fprintf(f,"BEGIN,%.17e,0,0,0,0,0,0,0\n",k);fclose(f);}}
void rtk_c10_65s2i_trace_end(void){const char *n=getenv("RTK_C10_65S2I_TRACE_FILE");FILE *f;if(s2i_on&&n&&*n){f=fopen(n,"a");if(f){fprintf(f,"END,%.17e,0,0,0,0,0,0,0\n",s2i_k);fclose(f);}}s2i_on=0;}
''',1)
cs=cs.replace('  int i;\n  double errmax,h,htemp,xnew;\n\n  h=htry;','  int i;\n  int s2i_rej=0;\n  double errmax,h,htemp,xnew;\n  double s2i_x0=*x,s2i_ht=htry;\n\n  h=htry;',1)
cs=cs.replace('    if (errmax <= 1.0) break;\n    htemp=','    if (errmax <= 1.0) break;\n    s2i_rej++;\n    htemp=',1)
cs=cs.replace('  for (i=0;i<pgi->n;i++) pgi->y[i]=pgi->ytemp[i];\n\n  return _SUCCESS_;','  for (i=0;i<pgi->n;i++) pgi->y[i]=pgi->ytemp[i];\n  s2i_write("ACCEPT",s2i_x0,*x,s2i_ht,*hdid,*hnext,s2i_rej,errmax);\n\n  return _SUCCESS_;',1)
q='      class_call(generic_evolver(perturb_derivs,\n                                 interval_limit[index_interval],c10_65s2_end,'
assert q in ps
ps=ps.replace(q,'      rtk_c10_65s2i_trace_begin(k);\n'+q,1)
q='                 ppt->error_message,ppt->error_message);\n      class_call(rtk_c10_65s2_observe("AFTER",c10_65s2_end,ppw->pv->y,NULL,&ppaw,ppt->error_message),ppt->error_message,ppt->error_message);'
assert q in ps
ps=ps.replace(q,'                 ppt->error_message,ppt->error_message);\n      rtk_c10_65s2i_trace_end();\n      class_call(rtk_c10_65s2_observe("AFTER",c10_65s2_end,ppw->pv->y,NULL,&ppaw,ppt->error_message),ppt->error_message,ppt->error_message);',1)
h.write_text(hs);c.write_text(cs);p.write_text(ps)
print('C10_65S2I_TRACE_PATCH_APPLIED')
# Frozen execution trigger only; no scientific or integration change.
