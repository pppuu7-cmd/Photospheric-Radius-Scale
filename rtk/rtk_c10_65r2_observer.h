#ifndef RTK_C10_65R2_OBSERVER_H
#define RTK_C10_65R2_OBSERVER_H

struct background;
struct thermo;
struct perturb_workspace;

/* Diagnostic-only observer.  The caller must invoke this only after the 16
 * C10.65r1 columns have been materialized at the end of the current output
 * row.  With c10_65r2_diag=0 the function returns without touching dataptr or
 * storeidx.  Heavy arithmetic lives in its own translation unit deliberately.
 */
void rtk_c10_65r2_observe(struct background *pba,
                          struct thermo *pth,
                          struct perturb_workspace *ppw,
                          double k,
                          double *dataptr,
                          int *storeidx);

#endif
