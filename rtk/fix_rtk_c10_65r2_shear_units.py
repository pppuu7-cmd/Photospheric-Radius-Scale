#!/usr/bin/env python3
"""Fix the C10.65r2 first-RHS shear dimensionality in a disposable CLASS tree.

C10.65r1 carries photon and UR shear as sigma/k^2 (the r1 output title is
explicitly `sigma_g_over_k2`, and the frozen UR seed uses the same convention).
The first r2 port accidentally inserted those quantities into Euler equations
as physical sigma.  Restore the missing k^2 exactly where sigma enters the
photon/UR first RHS.  This changes no frozen criterion and no production RHS.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source'/'perturbations.c'
s=p.read_text()
repls={
  'r1_R*(r2_dg/4.-r1_sg)': 'r1_R*(r2_dg/4.-r1_x*r1_sg)',
  'r1_x*(r2_dg/4.-r1_sg)': 'r1_x*(r2_dg/4.-r1_x*r1_sg)',
  'r1_x*(r2_du/4.-r1_Sur)': 'r1_x*(r2_du/4.-r1_x*r1_Sur)',
}
for old,new in repls.items():
    n=s.count(old)
    if n<1:
        raise SystemExit(f'missing C10.65r2 shear-unit anchor: {old}')
    s=s.replace(old,new)
p.write_text(s)
print('C10_65R2_SHEAR_UNITS_FIXED')
