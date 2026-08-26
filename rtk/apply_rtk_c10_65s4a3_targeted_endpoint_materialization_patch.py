#!/usr/bin/env python3
"""C10.65s4a3 targeted, sampling-only exact-onset materialization.

Only k=1e-3 and 3e-3 Mpc^-1 are eligible.  A forward-spline-consistent
conformal time is computed read-only, the already-selected uniform
approximation interval is split there with the same evolver arguments, and the
existing C10.65s1 read-only observer is called after the first segment returns.
All other k values and the dormant path use the original unsplit call.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'; mk=root/'Makefile'
ps=pt.read_text(); ms=mk.read_text()
marker='RTK_C10_65S4A3_TARGETED_ENDPOINT_MATERIALIZATION_V1'
if marker in ps:
    print('C10_65S4A3_PATCH_ALREADY_APPLIED'); raise SystemExit(0)
if 'RTK_C10_65S1_READONLY_STATE_OBSERVER_V1' not in ps:
    raise SystemExit('s4a3 requires the certified s1 read-only observer')

src=r'''/* RTK_C10_65S4A3_TARGETED_ENDPOINT_MATERIALIZATION_V1 */
#include "perturbations.h"
#include <math.h>
#include <stdlib.h>

int rtk_c10_65s4a3_target_k(double k) {
  const double k1=1.e-3,k2=3.e-3;
  return (fabs(k-k1)<=5.e-12*k1) || (fabs(k-k2)<=5.e-12*k2);
}

int rtk_c10_65s4a3_forward_tau(struct background *pba,double *tau_out,ErrorMsg error_message) {
  const double aon=0.0002203229136467;
  double lo=pba->tau_table[0],hi=pba->tau_table[pba->bt_size-1],mid=0.,am=0.;
  double *buf;
  int last,it;
  buf=(double*)malloc((size_t)pba->bg_size_short*sizeof(double));
  class_test(buf==NULL,error_message,"C10.65s4a3 background buffer allocation failed");
  for (it=0;it<96;it++) {
    mid=0.5*(lo+hi); last=0;
    class_call(background_at_tau(pba,mid,pba->short_info,pba->inter_normal,&last,buf),pba->error_message,error_message);
    am=buf[pba->index_bg_a];
    if (fabs(am-aon)/aon<=1.e-13) break;
    if (am<aon) lo=mid; else hi=mid;
  }
  free(buf);
  class_test(fabs(am-aon)/aon>1.e-13,error_message,
             "C10.65s4a3 forward root missed frozen relative-a target: %g",fabs(am-aon)/aon);
  *tau_out=mid;
  return _SUCCESS_;
}
'''
(root/'source'/'rtk_c10_65s4a3_endpoint.c').write_text(src)

inc='#include "perturbations.h"\n'
if inc not in ps: raise SystemExit('perturbations include anchor missing')
decl=('extern int rtk_c10_65s4a3_target_k(double); /* '+marker+' */\n'
      'extern int rtk_c10_65s4a3_forward_tau(struct background*,double*,ErrorMsg);\n')
ps=ps.replace(inc,inc+decl,1)
old='''    class_call(generic_evolver(perturb_derivs,
                               interval_limit[index_interval],
                               interval_limit[index_interval+1],
                               ppw->pv->y,
                               ppw->pv->used_in_sources,
                               ppw->pv->pt_size,
                               &ppaw,
                               ppr->tol_perturb_integration,
                               ppr->smallest_allowed_variation,
                               perturb_timescale,
                               ppr->perturb_integration_stepsize,
                               ppt->tau_sampling,
                               tau_actual_size,
                               perturb_sources,
                               perhaps_print_variables,
                               ppt->error_message),
               ppt->error_message,
               ppt->error_message);'''
if ps.count(old)!=1: raise SystemExit(f'expected one original evolver block, found {ps.count(old)}')
new='''    /* RTK_C10_65S4A3_TARGETED_ENDPOINT_MATERIALIZATION_V1 */
    if ((getenv("RTK_C10_65S4A3_TARGETED_ONSET") != NULL) && rtk_c10_65s4a3_target_k(k)) {
      double c10_65s4a3_tau;
      class_call(rtk_c10_65s4a3_forward_tau(pba,&c10_65s4a3_tau,ppt->error_message),
                 ppt->error_message,ppt->error_message);
      if ((c10_65s4a3_tau > interval_limit[index_interval]) &&
          (c10_65s4a3_tau < interval_limit[index_interval+1])) {
        class_call(generic_evolver(perturb_derivs,
                                   interval_limit[index_interval],
                                   c10_65s4a3_tau,
                                   ppw->pv->y,
                                   ppw->pv->used_in_sources,
                                   ppw->pv->pt_size,
                                   &ppaw,
                                   ppr->tol_perturb_integration,
                                   ppr->smallest_allowed_variation,
                                   perturb_timescale,
                                   ppr->perturb_integration_stepsize,
                                   ppt->tau_sampling,
                                   tau_actual_size,
                                   perturb_sources,
                                   perhaps_print_variables,
                                   ppt->error_message),
                   ppt->error_message,ppt->error_message);
        if (getenv("RTK_C10_65S1_OBSERVER_FILE") != NULL)
          rtk_c10_65s1_observe(c10_65s4a3_tau,ppw->pv->y,&ppaw);
        class_call(generic_evolver(perturb_derivs,
                                   c10_65s4a3_tau,
                                   interval_limit[index_interval+1],
                                   ppw->pv->y,
                                   ppw->pv->used_in_sources,
                                   ppw->pv->pt_size,
                                   &ppaw,
                                   ppr->tol_perturb_integration,
                                   ppr->smallest_allowed_variation,
                                   perturb_timescale,
                                   ppr->perturb_integration_stepsize,
                                   ppt->tau_sampling,
                                   tau_actual_size,
                                   perturb_sources,
                                   perhaps_print_variables,
                                   ppt->error_message),
                   ppt->error_message,ppt->error_message);
      }
      else {
        class_call(generic_evolver(perturb_derivs,
                                   interval_limit[index_interval],
                                   interval_limit[index_interval+1],
                                   ppw->pv->y,
                                   ppw->pv->used_in_sources,
                                   ppw->pv->pt_size,
                                   &ppaw,
                                   ppr->tol_perturb_integration,
                                   ppr->smallest_allowed_variation,
                                   perturb_timescale,
                                   ppr->perturb_integration_stepsize,
                                   ppt->tau_sampling,
                                   tau_actual_size,
                                   perturb_sources,
                                   perhaps_print_variables,
                                   ppt->error_message),
                   ppt->error_message,ppt->error_message);
      }
    }
    else {
      class_call(generic_evolver(perturb_derivs,
                                 interval_limit[index_interval],
                                 interval_limit[index_interval+1],
                                 ppw->pv->y,
                                 ppw->pv->used_in_sources,
                                 ppw->pv->pt_size,
                                 &ppaw,
                                 ppr->tol_perturb_integration,
                                 ppr->smallest_allowed_variation,
                                 perturb_timescale,
                                 ppr->perturb_integration_stepsize,
                                 ppt->tau_sampling,
                                 tau_actual_size,
                                 perturb_sources,
                                 perhaps_print_variables,
                                 ppt->error_message),
                 ppt->error_message,ppt->error_message);
    }'''
ps=ps.replace(old,new,1);pt.write_text(ps)
if 'rtk_c10_65s4a3_endpoint.o' not in ms:
    ma='SOURCE = input.o background.o thermodynamics.o perturbations.o primordial.o nonlinear.o transfer.o spectra.o lensing.o'
    if ma not in ms: raise SystemExit('Makefile SOURCE anchor missing')
    ms=ms.replace(ma,ma+' rtk_c10_65s4a3_endpoint.o',1);mk.write_text(ms)
print('C10_65S4A3_TARGETED_ENDPOINT_MATERIALIZATION_PATCH_APPLIED')
