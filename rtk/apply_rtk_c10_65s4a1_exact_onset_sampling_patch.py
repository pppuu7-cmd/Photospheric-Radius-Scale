#!/usr/bin/env python3
"""C10.65s4a1 observer-only exact-onset sampling repair.

The frozen s4a scientific domain/guards are unchanged.  When the dedicated
runtime environment variable is present, the one uniform-approximation
integration interval containing tau_on is executed as two calls to the same
already-selected generic_evolver with identical arguments except endpoints:
[start,tau_on] then [tau_on,end].  This causes the inherited read-only s1
print observer to materialize the exact endpoint.  There are no manual state,
dy, metric, tolerance, kernel, or approximation-criterion writes here.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
pt=root/'source'/'perturbations.c'
ps=pt.read_text()
marker='RTK_C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_V1'
if marker in ps:
    print('C10_65S4A1_EXACT_ONSET_SAMPLING_PATCH_ALREADY_APPLIED'); raise SystemExit(0)
if 'RTK_C10_65S1_READONLY_STATE_OBSERVER_V1' not in ps:
    raise SystemExit('s4a1 requires inherited s1 read-only observer first')
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
if ps.count(old)!=1:
    raise SystemExit(f'expected one generic_evolver block, found {ps.count(old)}')
new='''    /* RTK_C10_65S4A1_EXACT_ONSET_SAMPLING_REPAIR_V1:
       observer-only deterministic endpoint; no physics/tolerance mutation. */
    if (getenv("RTK_C10_65S4A1_EXACT_ONSET") != NULL) {
      const double c10_65s4a1_a_on = 0.0002203229136467;
      double c10_65s4a1_tau_on;
      class_call(background_tau_of_z(pba,1./c10_65s4a1_a_on-1.,&c10_65s4a1_tau_on),
                 pba->error_message,
                 ppt->error_message);
      if ((c10_65s4a1_tau_on > interval_limit[index_interval]) &&
          (c10_65s4a1_tau_on < interval_limit[index_interval+1])) {
        class_call(generic_evolver(perturb_derivs,
                                   interval_limit[index_interval],
                                   c10_65s4a1_tau_on,
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
                   ppt->error_message);
        class_call(generic_evolver(perturb_derivs,
                                   c10_65s4a1_tau_on,
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
                   ppt->error_message);
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
                   ppt->error_message,
                   ppt->error_message);
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
                 ppt->error_message,
                 ppt->error_message);
    }'''
ps=ps.replace(old,new,1)
pt.write_text(ps)
print('C10_65S4A1_EXACT_ONSET_SAMPLING_PATCH_APPLIED')
