#!/usr/bin/env python3
"""Move r2 diagnostic titles before r1 titles to match their read-only store order.

This is an interface-only correction for the first r2 in-CLASS execution. It
changes neither equations nor thresholds and is applied only to disposable
CLASS trees after the r2 diagnostic patch.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source'/'perturbations.c'
lines=p.read_text().splitlines()
r2=[x for x in lines if 'class_store_columntitle' in x and 'c10_65r2_' in x]
if len(r2)!=13:
    raise SystemExit(f'expected 13 r2 title lines, found {len(r2)}')
lines=[x for x in lines if not ('class_store_columntitle' in x and 'c10_65r2_' in x)]
idx=next((i for i,x in enumerate(lines) if 'class_store_columntitle' in x and 'c10_65r1_W_khr' in x),-1)
if idx<0: raise SystemExit('r1 title anchor missing')
lines[idx:idx]=r2
p.write_text('\n'.join(lines)+'\n')
print('C10_65R2_COLUMN_ORDER_FIXED')
