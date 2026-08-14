#!/usr/bin/env python3
from pathlib import Path
import re, sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
models=[
 ('lcdm_baseline.ini','planck_lcdm.ini','output/planck_lcdm_'),
 ('rtk_lambda1000.ini','planck_rtk1.ini','output/planck_rtk1_'),
 ('rtk_lambda2000.ini','planck_rtk2.ini','output/planck_rtk2_'),
 ('rtk_lambda3000.ini','planck_rtk3.ini','output/planck_rtk3_'),
]
for src,dst,outroot in models:
    text=(root/src).read_text()
    text=re.sub(r'^output\s*=.*$', 'output = tCl,pCl,lCl', text, flags=re.M)
    text=re.sub(r'^l_max_scalars\s*=.*$', 'l_max_scalars = 2600', text, flags=re.M)
    text=re.sub(r'^root\s*=.*$', f'root = {outroot}', text, flags=re.M)
    if re.search(r'^lensing\s*=',text,flags=re.M):
        text=re.sub(r'^lensing\s*=.*$', 'lensing = yes', text, flags=re.M)
    else:
        text += '\nlensing = yes\n'
    (root/dst).write_text(text)
print('PLANCK_INPUTS_PREPARED')
