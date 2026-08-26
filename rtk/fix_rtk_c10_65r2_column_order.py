#!/usr/bin/env python3
"""Repair diagnostic output ordering and all-history finiteness scope for r2.

The frozen C10.65r2 finiteness criterion is defined on the 36 exact-onset
records.  The shadow algebra is nevertheless evaluated while CLASS writes the
full perturbation history, where the synthetic onset completion is not a
certified physical trajectory.  A fatal class_test over every history row can
therefore abort before the frozen onset records are emitted.  Remove only that
all-history abort; the unchanged frozen analyzer still requires every r2 field
to be finite at all 36 exact-onset records.

This also moves the r2 diagnostic titles before r1 titles to match their
read-only store order.  No equation, threshold, dy entry, production metric
source, or production RHS is changed.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source'/'perturbations.c'
text=p.read_text()
old='''          class_test(!isfinite(r2_B0.v)||!isfinite(r2_B0.d)||!isfinite(r2_Ba.d)||!isfinite(r2_Psip)||!isfinite(r2_slip)\n            ||!isfinite(r2_thbp)||!isfinite(r2_thgp)||!isfinite(r2_thurp)||!isfinite(r2_dkp)||!isfinite(r2_thkp),error_message,"C10.65r2 non-finite shadow first RHS");\n'''
if old not in text:
    raise SystemExit('r2 all-history finiteness guard anchor missing')
text=text.replace(old,'',1)
lines=text.splitlines()
r2=[x for x in lines if 'class_store_columntitle' in x and 'c10_65r2_' in x]
if len(r2)!=13:
    raise SystemExit(f'expected 13 r2 title lines, found {len(r2)}')
lines=[x for x in lines if not ('class_store_columntitle' in x and 'c10_65r2_' in x)]
idx=next((i for i,x in enumerate(lines) if 'class_store_columntitle' in x and 'c10_65r1_W_khr' in x),-1)
if idx<0: raise SystemExit('r1 title anchor missing')
lines[idx:idx]=r2
p.write_text('\n'.join(lines)+'\n')
print('C10_65R2_COLUMN_ORDER_AND_ONSET_FINITE_SCOPE_FIXED')
