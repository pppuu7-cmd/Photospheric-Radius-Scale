#!/usr/bin/env python3
"""Inject one diagnostic homogeneous deltaU perturbation basis vector.

C10.46 only. This changes the scalar perturbation IC deltaU_nlde from 0 to 1
while leaving deltaU', deltaV, deltaV', deltaZ and deltaZ' at zero. It is
applied only to disposable diagnostic CLASS trees after the baseline run.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source'/'perturbations.c'
s=p.read_text()
marker='RTK_C10_LEGACY_RT_DU_PROJECTION_SEED_V1'
if marker in s:
    print('C10_DU_PROJECTION_SEED_ALREADY_APPLIED')
    raise SystemExit(0)
old='''      if (pba->has_nlde == _TRUE_) {
          ppw->pv->y[ppw->pv->index_pt_deltaU_nlde] = 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaU_prime_nlde] = 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaV_nlde] = 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaV_prime_nlde] = 0.;
          if(pba->model == 2.){
              ppw->pv->y[ppw->pv->index_pt_deltaZ_nlde] = 0.;
              ppw->pv->y[ppw->pv->index_pt_deltaZ_prime_nlde] = 0.;
          }
            
      }'''
new='''      if (pba->has_nlde == _TRUE_) {
          /* RTK_C10_LEGACY_RT_DU_PROJECTION_SEED_V1: diagnostic homogeneous basis vector only. */
          ppw->pv->y[ppw->pv->index_pt_deltaU_nlde] = (pba->model == 2.) ? 1.0 : 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaU_prime_nlde] = 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaV_nlde] = 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaV_prime_nlde] = 0.;
          if(pba->model == 2.){
              ppw->pv->y[ppw->pv->index_pt_deltaZ_nlde] = 0.;
              ppw->pv->y[ppw->pv->index_pt_deltaZ_prime_nlde] = 0.;
          }
            
      }'''
count=s.count(old)
if count != 1:
    raise SystemExit(f'C10_DU_PROJECTION_SEED_REFUSED expected exact IC block once, found {count}')
s=s.replace(old,new,1)
p.write_text(s)
check=p.read_text()
if check.count(marker)!=1:
    raise SystemExit('C10_DU_PROJECTION_SEED_FAILED marker count')
print('C10_DU_PROJECTION_SEED_APPLIED deltaU_ini=1 deltaUprime=deltaV=deltaVprime=deltaZ=deltaZprime=0')
