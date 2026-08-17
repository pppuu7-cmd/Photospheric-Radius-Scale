#!/usr/bin/env python3
"""Make the pinned nonlocal CLASS auxiliary-field initial conditions explicit.

The pinned upstream source contains a copy/paste typo in input.c:
  U=0; U'=0; V=0; U'=0;
so V_prime_ini_nlde is not explicitly initialized before background.c uses it.
For the minimal retarded nonlocal model the intended homogeneous auxiliary
solution is zero. This patch changes only the second U' assignment to V'=0 and
fails closed if the exact audited upstream block is not present.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'class_public')
p = root / 'source' / 'input.c'
text = p.read_text()
old = '''/**NonLocal: auxiliary fields initial conditions*/
  pba->U_ini_nlde = 0.;
  pba->U_prime_ini_nlde = 0.;
  pba->V_ini_nlde = 0.;
  pba->U_prime_ini_nlde = 0.;'''
new = '''/**NonLocal: auxiliary fields initial conditions*/
  pba->U_ini_nlde = 0.;
  pba->U_prime_ini_nlde = 0.;
  pba->V_ini_nlde = 0.;
  pba->V_prime_ini_nlde = 0.;'''
count = text.count(old)
if count != 1:
    raise SystemExit(f'RTK_NONLOCAL_IC_PATCH_REFUSED expected exact upstream block once, found {count}')
text = text.replace(old, new, 1)
p.write_text(text)
check = p.read_text()
if 'pba->V_prime_ini_nlde = 0.;' not in check:
    raise SystemExit('RTK_NONLOCAL_IC_PATCH_FAILED')
print('RTK_NONLOCAL_IC_PATCH_PASS explicit U,Uprime,V,Vprime zero IC')
