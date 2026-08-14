#!/usr/bin/env python3
"""Prepare the reusable exact-likelihood core for inference workflows.

The legacy nonlocal CLASS branch expects A_s and n_s. This helper also adds a
per-CLASS timeout so a pathological parameter point cannot hang an entire CI
inference job. It strips the deterministic coordinate-search tail beginning at
RTK0= and leaves the tested likelihood functions intact.
"""
from pathlib import Path
import sys

src=Path(sys.argv[1] if len(sys.argv)>1 else 'joint_profile_runner.py')
out=Path(sys.argv[2] if len(sys.argv)>2 else 'inference_core.py')
s=src.read_text()

s=s.replace("f\"A_s_ad = {p['As']}\"", "f\"A_s = {p['As']}\"")
s=s.replace("f\"n_s_ad = {p['ns']}\"", "f\"n_s = {p['ns']}\"")
marker='\nRTK0='
if marker not in s:
    raise SystemExit('joint-profile split marker not found')
s=s.split(marker,1)[0]+'\n'

old="    cp=subprocess.run(['./class',str(ini)],stdout=log.open('w'),stderr=subprocess.STDOUT)\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag};CACHE[key]=r;HISTORY.append(r);return r\n"
new="    try:\n        with log.open('w') as lf:\n            cp=subprocess.run(['./class',str(ini)],stdout=lf,stderr=subprocess.STDOUT,timeout=float(os.environ.get('RTK_CLASS_TIMEOUT','120')))\n    except subprocess.TimeoutExpired:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_TIMEOUT'};CACHE[key]=r;HISTORY.append(r);print('EVAL_TIMEOUT',model,tag,'params',p,flush=True);return r\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_RETURN_'+str(cp.returncode)};CACHE[key]=r;HISTORY.append(r);return r\n"
if old not in s:
    raise SystemExit('subprocess block not found')
s=s.replace(old,new,1)

out.write_text(s)
text=out.read_text()
assert 'A_s_ad' not in text and 'n_s_ad' not in text
assert 'timeout=float(os.environ.get' in text
print('INFERENCE_CORE_PREPARED',out)
