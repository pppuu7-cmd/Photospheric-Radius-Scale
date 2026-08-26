#!/usr/bin/env python3
"""Run conditioned C10.65r1 parity using r1hp sidecars for ON histories only."""
from pathlib import Path
import glob, importlib.util

here=Path(__file__).resolve().parent
p=here/'rtk_c10_65r1_conditioned_parity_wrapper.py'
spec=importlib.util.spec_from_file_location('r1cond',p)
cond=importlib.util.module_from_spec(spec); spec.loader.exec_module(cond)
base=cond.base
_orig=base.read_modes

def hp_read_modes(pattern,r1=False):
    if not r1:
        return _orig(pattern,r1)
    fs=sorted(f for f in glob.glob(pattern) if f.endswith('_s_r1hp.dat'))
    out=[]
    for f in fs:
        rr=base.read_rows(f,True,True)
        k=sum(x['c10_k_Mpc_inv'] for x in rr)/len(rr)
        out.append({'k':k,'file':f,'rows':rr,'sha':base.digest(f)})
    return sorted(out,key=lambda x:x['k'])

base.read_modes=hp_read_modes
if __name__=='__main__':
    base.main()
