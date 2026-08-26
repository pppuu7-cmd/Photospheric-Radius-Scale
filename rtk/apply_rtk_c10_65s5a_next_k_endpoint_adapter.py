#!/usr/bin/env python3
"""C10.65s5a sampling-only adapter for the certified s4a3 exact-onset materializer.

Changes only the two observer-eligible k constants from (1e-3,3e-3) to
(3e-3,1e-2). No perturbation equation, evolver tolerance, approximation
criterion, state coordinate, or scientific threshold is modified.
"""
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source'/'rtk_c10_65s4a3_endpoint.c'
s=p.read_text()
old='const double k1=1.e-3,k2=3.e-3;'
new='const double k1=3.e-3,k2=1.e-2; /* RTK_C10_65S5A_NEXT_K_ENDPOINT_ADAPTER_V1 */'
if new in s:
    print('C10_65S5A_NEXT_K_ENDPOINT_ADAPTER_ALREADY_APPLIED');raise SystemExit(0)
if s.count(old)!=1: raise SystemExit(f's4a3 target-k anchor not unique: {s.count(old)}')
s=s.replace(old,new,1);p.write_text(s)
print('C10_65S5A_NEXT_K_ENDPOINT_ADAPTER_APPLIED')
