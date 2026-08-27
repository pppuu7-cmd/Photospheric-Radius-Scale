#!/usr/bin/env python3
from pathlib import Path
import sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source'/'rtk_c10_65s4a3_endpoint.c'
s=p.read_text()
old='const double k1=1.e-3,k2=3.e-3;'
new='const double k1=1.e-2,k2=3.e-2; /* RTK_C10_65S6A_K003_ENDPOINT_ADAPTER_V1 */'
if new in s:
    print('C10_65S6A_K003_ENDPOINT_ADAPTER_ALREADY_APPLIED');raise SystemExit(0)
if s.count(old)!=1: raise SystemExit(f's4a3 target-k anchor not unique: {s.count(old)}')
s=s.replace(old,new,1);p.write_text(s)
print('C10_65S6A_K003_ENDPOINT_ADAPTER_APPLIED')
