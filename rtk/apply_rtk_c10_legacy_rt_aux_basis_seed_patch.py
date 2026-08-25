#!/usr/bin/env python3
"""Inject one C10.47 unit auxiliary perturbation IC basis seed.

Usage: python3 apply_rtk_c10_legacy_rt_aux_basis_seed_patch.py ROOT LABEL
where LABEL is one of dU,dUp,dV,dVp,dZ,dZp. Apply only to a disposable
model=2 diagnostic tree restored to the baseline source before each seed.
"""
from pathlib import Path
import sys

if len(sys.argv) != 3:
    raise SystemExit('usage: SCRIPT ROOT {dU|dUp|dV|dVp|dZ|dZp}')
root=Path(sys.argv[1]); label=sys.argv[2]
allowed={'dU','dUp','dV','dVp','dZ','dZp'}
if label not in allowed:
    raise SystemExit(f'unknown seed label {label}')
p=root/'source'/'perturbations.c'
s=p.read_text()
marker='RTK_C10_LEGACY_RT_AUX_BASIS_SEED_V1'
if marker in s:
    raise SystemExit('C10_AUX_BASIS_SEED_REFUSED source already contains a basis seed marker')
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
vals={k:('1.0' if k==label else '0.') for k in allowed}
new=f'''      if (pba->has_nlde == _TRUE_) {{
          /* {marker} label={label}; disposable tangent-basis diagnostic only. */
          ppw->pv->y[ppw->pv->index_pt_deltaU_nlde] = (pba->model == 2.) ? {vals['dU']} : 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaU_prime_nlde] = (pba->model == 2.) ? {vals['dUp']} : 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaV_nlde] = (pba->model == 2.) ? {vals['dV']} : 0.;
          ppw->pv->y[ppw->pv->index_pt_deltaV_prime_nlde] = (pba->model == 2.) ? {vals['dVp']} : 0.;
          if(pba->model == 2.){{
              ppw->pv->y[ppw->pv->index_pt_deltaZ_nlde] = {vals['dZ']};
              ppw->pv->y[ppw->pv->index_pt_deltaZ_prime_nlde] = {vals['dZp']};
          }}
            
      }}'''
count=s.count(old)
if count != 1:
    raise SystemExit(f'C10_AUX_BASIS_SEED_REFUSED expected exact IC block once, found {count}')
s=s.replace(old,new,1)
p.write_text(s)
check=p.read_text()
if check.count(marker)!=1 or f'label={label}' not in check:
    raise SystemExit('C10_AUX_BASIS_SEED_FAILED marker verification')
print(f'C10_AUX_BASIS_SEED_APPLIED {label}=1 all other auxiliary perturbation ICs zero')
