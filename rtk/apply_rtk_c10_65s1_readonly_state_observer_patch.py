#!/usr/bin/env python3
"""C10.65s1 read-only full scalar-state observer for a disposable pinned CLASS tree.

The observer is dormant unless RTK_C10_65S1_OBSERVER_FILE is set.  It writes a
separate CSV sidecar and never changes dy, metric workspaces, or perturbation
output columns.  The heavy observer body lives in its own translation unit so
OFF-path code-generation effects are minimized and checked by the frozen gate.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
mk=root/'Makefile'
ps=pt.read_text(); ms=mk.read_text()
marker='RTK_C10_65S1_READONLY_STATE_OBSERVER_V1'
if marker in ps:
    print('C10_65S1_OBSERVER_PATCH_ALREADY_APPLIED'); raise SystemExit(0)

src=r'''/* RTK_C10_65S1_READONLY_STATE_OBSERVER_V1 */
#include "perturbations.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#if defined(__GNUC__)
#define RTK_NOINLINE __attribute__((noinline,noclone))
#else
#define RTK_NOINLINE
#endif

static double safe_y(struct perturb_vector *pv,double *y,int i) {
  if (i < 0 || i >= pv->pt_size) return NAN;
  return y[i];
}

RTK_NOINLINE void rtk_c10_65s1_observe(double tau,double *y,void *parameters_and_workspace) {
  const char *path=getenv("RTK_C10_65S1_OBSERVER_FILE");
  struct perturb_parameters_and_workspace *ppaw;
  struct perturb_workspace *ppw;
  struct perturb_vector *pv;
  struct background *pba;
  struct perturbs *ppt;
  FILE *f;
  double a,k;
  int tca,rsa,ufa,lmax,l;
  if (path==NULL || path[0]=='\0') return;
  ppaw=(struct perturb_parameters_and_workspace*)parameters_and_workspace;
  ppw=ppaw->ppw; pv=ppw->pv; pba=ppaw->pba; ppt=ppaw->ppt;
  if (!(ppt->has_scalars==_TRUE_ && ppaw->index_md==ppt->index_md_scalars)) return;
  a=ppw->pvecback[pba->index_bg_a]; k=ppaw->k;
  tca=ppw->approx[ppw->index_ap_tca];
  rsa=ppw->approx[ppw->index_ap_rsa];
  ufa=ppw->approx[ppw->index_ap_ufa];
  lmax=pv->l_max_ur;
  f=fopen(path,"a"); if (!f) return;
  fprintf(f,"%.17e,%.17e,%.17e,%d,%d,%d,%d,",tau,a,k,tca,rsa,ufa,lmax);
  fprintf(f,"%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,%.17e,",
    safe_y(pv,y,pv->index_pt_phi),
    safe_y(pv,y,pv->index_pt_delta_b),safe_y(pv,y,pv->index_pt_theta_b),
    safe_y(pv,y,pv->index_pt_delta_g),safe_y(pv,y,pv->index_pt_theta_g),
    safe_y(pv,y,pv->index_pt_delta_ur),safe_y(pv,y,pv->index_pt_theta_ur),safe_y(pv,y,pv->index_pt_shear_ur),
    safe_y(pv,y,pv->index_pt_delta_cdm),safe_y(pv,y,pv->index_pt_theta_cdm),
    safe_y(pv,y,pv->index_pt_deltaU_nlde),safe_y(pv,y,pv->index_pt_deltaU_prime_nlde),
    safe_y(pv,y,pv->index_pt_deltaV_nlde),safe_y(pv,y,pv->index_pt_deltaV_prime_nlde),
    safe_y(pv,y,pv->index_pt_deltaZ_nlde));
  fprintf(f,"%.17e",safe_y(pv,y,pv->index_pt_deltaZ_prime_nlde));
  for (l=3;l<=30;l++) {
    double q=NAN;
    if (ufa==ufa_off && l<=lmax && pv->index_pt_l3_ur>=0 && pv->index_pt_l3_ur+(l-3)<pv->pt_size) {
      double Fl=y[pv->index_pt_l3_ur+(l-3)];
      q=(k!=0.) ? Fl/pow(k,(double)l) : NAN;
    }
    fprintf(f,",%.17e",q);
  }
  fputc('\n',f); fclose(f);
}
'''
(root/'source'/'rtk_c10_65s1_observer.c').write_text(src)

# External declaration only; the body is a separate noinline/noclone unit.
decl='extern void rtk_c10_65s1_observe(double tau,double *y,void *parameters_and_workspace); /* '+marker+' */\n'
inc='#include "perturbations.h"\n'
if inc not in ps: raise SystemExit('perturbations include anchor missing')
ps=ps.replace(inc,inc+decl,1)
# perturbations.c needs stdlib for getenv. Add it before computing any byte
# offsets used for the later injection; changing ps after computing absret would
# shift the insertion point and can split an existing statement.
if '#include <stdlib.h>' not in ps:
    ps=ps.replace(decl,decl+'#include <stdlib.h>\n',1)

# Inject exactly one call at the very end of perturb_print_variables, after all
# ordinary scalar/vector/tensor output values have already been materialized.
start=ps.find('int perturb_print_variables(double tau,')
if start<0: raise SystemExit('perturb_print_variables not found')
brace=ps.find('{',start)
depth=0; end=None
for i in range(brace,len(ps)):
    if ps[i]=='{': depth+=1
    elif ps[i]=='}':
        depth-=1
        if depth==0: end=i; break
if end is None: raise SystemExit('cannot bound perturb_print_variables')
segment=ps[brace:end]
ret=segment.rfind('return _SUCCESS_;')
if ret<0: raise SystemExit('success return not found in perturb_print_variables')
absret=brace+ret
call='  if (getenv("RTK_C10_65S1_OBSERVER_FILE") != NULL) rtk_c10_65s1_observe(tau,y,parameters_and_workspace);\n\n  '
ps=ps[:absret]+call+ps[absret:]
pt.write_text(ps)

if 'rtk_c10_65s1_observer.o' not in ms:
    anchor='SOURCE = input.o background.o thermodynamics.o perturbations.o primordial.o nonlinear.o transfer.o spectra.o lensing.o'
    if anchor not in ms: raise SystemExit('Makefile SOURCE anchor missing')
    ms=ms.replace(anchor,anchor+' rtk_c10_65s1_observer.o',1)
    mk.write_text(ms)
print('C10_65S1_OBSERVER_PATCH_APPLIED')
