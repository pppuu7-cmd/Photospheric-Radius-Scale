#!/usr/bin/env python3
"""Build a reproducible final-objective candidate inference core.

Stage 1 delegates to prepare_inference_core.py, preserving the production
normalization: modern A_s/n_s, exact-float cache semantics, CLASS timeout, and
search-tail removal.  Stage 2 changes only numerical inference settings that
have dedicated audits:
  * dense BOSS growth redshift sampling (z_pk)
  * matched-ultra CLASS precision with l_linstep=2

This file creates a *candidate* final objective.  It does not by itself certify
l_linstep=2 versus 1 or a final cosmological fit; those remain external gates.
"""
from pathlib import Path
import subprocess, sys

src=Path(sys.argv[1] if len(sys.argv)>1 else 'joint_profile_runner.py')
out=Path(sys.argv[2] if len(sys.argv)>2 else 'inference_core_final.py')
base=out.with_suffix(out.suffix+'.base.tmp')
helper=Path(__file__).with_name('prepare_inference_core.py')
if not helper.exists():
    # Workflows normally copy both helpers into the CLASS root.
    helper=Path('prepare_inference_core.py')
subprocess.run([sys.executable,str(helper),str(src),str(base)],check=True)
s=base.read_text()
try: base.unlink()
except OSError: pass

sparse='"z_pk = 0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0"'
dense='"z_pk = 0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0"'
if s.count(sparse)!=1:
    raise SystemExit(f'expected exactly one production sparse z_pk line, found {s.count(sparse)}')
s=s.replace(sparse,dense,1)

anchor='"z_max_pk = 1.0",'
precision=[
 '"tol_background_integration = 3e-4",',
 '"tol_thermo_integration = 3e-4",',
 '"tol_perturb_integration = 3e-7",',
 '"perturb_sampling_stepsize = 0.0125",',
 '"k_per_decade_for_pk = 40",',
 '"k_per_decade_for_bao = 180",',
 '"k_max_tau0_over_l_max = 4.0",',
 '"l_logstep = 1.02",',
 '"l_linstep = 2",',
]
if s.count(anchor)!=1:
    raise SystemExit(f'expected exactly one z_max_pk anchor, found {s.count(anchor)}')
for line in precision:
    if line in s:
        raise SystemExit('precision line already present before final-objective patch: '+line)
s=s.replace(anchor,anchor+'\n      '+ '\n      '.join(precision),1)
out.write_text(s)

text=out.read_text()
assert sparse not in text and dense in text
assert 'A_s_ad' not in text and 'n_s_ad' not in text
assert 'round(float(p[k]),12)' not in text
assert 'timeout=float(os.environ.get' in text
for line in precision: assert line in text
assert text.count('l_linstep = 2')==1
print('FINAL_INFERENCE_CORE_PREPARED',out)
