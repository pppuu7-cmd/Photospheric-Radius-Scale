#!/usr/bin/env python3
"""Prepare the reusable exact-likelihood core for inference workflows.

The helper accepts either the historical joint-profile source or an already
canonicalized source. It guarantees modern A_s/n_s names, an exact-float cache
key, a CLASS timeout, success-only memoization, a module-safe Planck data path,
and removal of the standalone deterministic-search tail.

Execution or post-processing failures are deliberately *not* memoized. A
failure return is not guaranteed to be a deterministic property of the
cosmological point; caching it could turn a transient numerical/resource/I/O
event into a permanent artificial wall in an optimizer or finite-difference
stencil. Only completed ``ok=True`` likelihood evaluations enter CACHE.

The reusable core is imported by workers that have their own command-line
arguments. Therefore it must never interpret the importing worker's sys.argv
as the Planck likelihood path. RTK_PLANCK_DATA is the explicit override;
``planck_data`` remains the reproducible workflow default.
"""
from pathlib import Path
import sys

src=Path(sys.argv[1] if len(sys.argv)>1 else 'joint_profile_runner.py')
out=Path(sys.argv[2] if len(sys.argv)>2 else 'inference_core.py')
s=src.read_text()

# Reusable modules must not inherit the caller's argv. Historically the source
# accepted the Planck directory as argv[1], which is valid for the standalone
# runner but unsafe after importing the generated module from workers such as
# ``neutrino_reoptimization_seed.py RTK``.
legacy_planck="PLANCK=Path(sys.argv[1]) if len(sys.argv)>1 else Path('planck_data')"
module_safe_planck="PLANCK=Path(os.environ.get('RTK_PLANCK_DATA','planck_data'))"
if legacy_planck in s:
    s=s.replace(legacy_planck,module_safe_planck,1)
elif module_safe_planck not in s:
    raise SystemExit('recognized Planck path block not found')

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
if 'def evaluate(' not in s or 'def make_ini(' not in s:
    raise SystemExit('likelihood core functions not found')

legacy="    cp=subprocess.run(['./class',str(ini)],stdout=log.open('w'),stderr=subprocess.STDOUT)\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag};CACHE[key]=r;HISTORY.append(r);return r\n"
timeout_cached="    try:\n        with log.open('w') as lf:\n            cp=subprocess.run(['./class',str(ini)],stdout=lf,stderr=subprocess.STDOUT,timeout=float(os.environ.get('RTK_CLASS_TIMEOUT','120')))\n    except subprocess.TimeoutExpired:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_TIMEOUT'};CACHE[key]=r;HISTORY.append(r);print('EVAL_TIMEOUT',model,tag,'params',p,flush=True);return r\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_RETURN_'+str(cp.returncode)};CACHE[key]=r;HISTORY.append(r);return r\n"
timeout_nonzero_cached="    try:\n        with log.open('w') as lf:\n            cp=subprocess.run(['./class',str(ini)],stdout=lf,stderr=subprocess.STDOUT,timeout=float(os.environ.get('RTK_CLASS_TIMEOUT','120')))\n    except subprocess.TimeoutExpired:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_TIMEOUT'};HISTORY.append(r);print('EVAL_TIMEOUT',model,tag,'params',p,flush=True);return r\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_RETURN_'+str(cp.returncode)};CACHE[key]=r;HISTORY.append(r);return r\n"
all_failures_uncached="    try:\n        with log.open('w') as lf:\n            cp=subprocess.run(['./class',str(ini)],stdout=lf,stderr=subprocess.STDOUT,timeout=float(os.environ.get('RTK_CLASS_TIMEOUT','120')))\n    except subprocess.TimeoutExpired:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_TIMEOUT'};HISTORY.append(r);print('EVAL_TIMEOUT',model,tag,'params',p,flush=True);return r\n    if cp.returncode!=0:\n        r={'ok':False,'score':1e30,'score_k01':1e30,'model':model,**p,'tag':tag,'error':'CLASS_RETURN_'+str(cp.returncode)};HISTORY.append(r);print('EVAL_CLASS_RETURN',model,tag,'returncode',cp.returncode,'params',p,flush=True);return r\n"
if legacy in s:
    s=s.replace(legacy,all_failures_uncached,1)
elif timeout_cached in s:
    s=s.replace(timeout_cached,all_failures_uncached,1)
elif timeout_nonzero_cached in s:
    s=s.replace(timeout_nonzero_cached,all_failures_uncached,1)
elif all_failures_uncached not in s:
    raise SystemExit('recognized CLASS subprocess block not found')

# Historical source caches the post-processing result unconditionally. Normalize
# this to success-only memoization; failed parsing/likelihood calls remain in
# HISTORY for diagnostics but cannot poison the exact cache.
unconditional="    CACHE[key]=r;HISTORY.append(r)\n    print('EVAL',model,tag,'score',r['score'],'params',p,flush=True)"
success_only="    if r.get('ok'):\n        CACHE[key]=r\n    HISTORY.append(r)\n    print('EVAL',model,tag,'score',r['score'],'params',p,flush=True)"
if unconditional in s:
    s=s.replace(unconditional,success_only,1)
elif success_only not in s:
    raise SystemExit('recognized final cache block not found')

out.write_text(s)
text=out.read_text()
assert 'A_s_ad' not in text and 'n_s_ad' not in text
assert 'timeout=float(os.environ.get' in text
assert 'round(float(p[k]),12)' not in text
assert "tuple(float(p[k]) for k in ['lam','h','Ob','Om','As','ns','zre'])" in text
assert module_safe_planck in text
assert legacy_planck not in text
assert 'def evaluate(' in text and 'def make_ini(' in text
# No failure path may poison the exact cache.
timeout_block=text.split('except subprocess.TimeoutExpired:',1)[1].split('if cp.returncode!=0:',1)[0]
return_block=text.split('if cp.returncode!=0:',1)[1].split('prefix=tag',1)[0]
except_block=text.split('except Exception as e:',1)[1].split("print('EVAL'",1)[0]
assert 'CACHE[key]' not in timeout_block
assert 'CACHE[key]' not in return_block
assert "if r.get('ok')" in except_block
print('INFERENCE_CORE_PREPARED',out)
