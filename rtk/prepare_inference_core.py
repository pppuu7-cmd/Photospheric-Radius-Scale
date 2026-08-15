#!/usr/bin/env python3
"""Prepare the reusable exact-likelihood core for inference workflows.

The helper accepts either the historical joint-profile source or an already
canonicalized source.  It guarantees modern A_s/n_s names, an exact-float cache
key, a CLASS timeout, and removal of the standalone deterministic-search tail.
This idempotence lets the source-of-truth be modernized later without changing
the generated inference core or breaking production workflows.
"""
from pathlib import Path
import sys

src=Path(sys.argv[1] if len(sys.argv)>1 else 'joint_profile_runner.py')
out=Path(sys.argv[2] if len(sys.argv)>2 else 'inference_core.py')
s=src.read_text()

# Primordial parameter names: legacy -> modern, while accepting modern input.
s=s.replace("f\"A_s_ad = {p['As']}\"", "f\"A_s = {p['As']}\"")
s=s.replace("f\"n_s_ad = {p['ns']}\"", "f\"n_s = {p['ns']}\"")
if "f\"A_s = {p['As']}\"" not in s or "f\"n_s = {p['ns']}\"" not in s:
    raise SystemExit('modern A_s/n_s blocks not found after normalization')

old_key="    key=(model,)+tuple(round(float(p[k]),12) for k in ['lam','h','Ob','Om','As','ns','zre'])"
new_key="    key=(model,)+tuple(float(p[k]) for k in ['lam','h','Ob','Om','As','ns','zre'])"
if old_key in s:
    s=s.replace(old_key,new_key,1)
elif new_key not in s:
    raise SystemExit('neither legacy nor exact-float likelihood cache-key block found')

# The reusable core excludes the standalone deterministic scan/search tail.
marker='\nRTK0='
if marker in s:
    s=s.split(marker,1)[0]+'\n'
elif '\nRTK0=' in s:
    raise SystemExit('ambiguous joint-profile split marker')
# Already-core-like source without RTK0 is allowed if the likelihood functions exist.
if 'def evaluate(' not in s or 'def make_ini(' not in s:
    raise SystemExit('likelihood core functions not found')

old="    cp=subprocess.run(['./class',str(ini)],stdout=log.open('w'),stderr=subprocess.STDOUT)\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag};CACHE[key]=r;HISTORY.append(r);return r\n"
new="    try:\n        with log.open('w') as lf:\n            cp=subprocess.run(['./class',str(ini)],stdout=lf,stderr=subprocess.STDOUT,timeout=float(os.environ.get('RTK_CLASS_TIMEOUT','120')))\n    except subprocess.TimeoutExpired:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_TIMEOUT'};CACHE[key]=r;HISTORY.append(r);print('EVAL_TIMEOUT',model,tag,'params',p,flush=True);return r\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_RETURN_'+str(cp.returncode)};CACHE[key]=r;HISTORY.append(r);return r\n"
if old in s:
    s=s.replace(old,new,1)
elif "timeout=float(os.environ.get('RTK_CLASS_TIMEOUT','120'))" not in s:
    raise SystemExit('neither legacy nor timeout-protected subprocess block found')

out.write_text(s)
text=out.read_text()
assert 'A_s_ad' not in text and 'n_s_ad' not in text
assert 'timeout=float(os.environ.get' in text
assert 'round(float(p[k]),12)' not in text
assert "tuple(float(p[k]) for k in ['lam','h','Ob','Om','As','ns','zre'])" in text
assert 'def evaluate(' in text and 'def make_ini(' in text
print('INFERENCE_CORE_PREPARED',out)
