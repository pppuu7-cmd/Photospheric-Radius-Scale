#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
L=json.loads((R/'rtk/reproducibility_lock.json').read_text());W=(R/'rtk/autonomous_dense_lcdm_stationarity.py').read_text()
C={'numpy':L.get('python_packages',{}).get('numpy')=='2.5.2','scipy':L.get('python_packages',{}).get('scipy')=='1.18.0','python':L.get('runtime',{}).get('python')=='3.12.3','planck_sha':L.get('likelihood',{}).get('planck_baseline_sha256')=='0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6','class_sha':L.get('external_git',{}).get('class_public',{}).get('commit')=='36cf283628c4a3330ec9fd3d84239bf775f77317','pantheon_sha':L.get('external_git',{}).get('pantheon',{}).get('commit')=='7eb29dc87ba223b4ec8457cd3cccba1216c36fb7','lcdm_steps_decoupled':"STATE['rtk']['base_steps']" not in W and 'DEFAULT_LCDM_STEPS' in W}
b=[k for k,v in C.items() if not v]
if b:raise SystemExit('RTK_REPRO_EXT_AUDIT_FAIL '+json.dumps(b))
print('RTK_REPRO_EXT_AUDIT_PASS',json.dumps(sorted(C)))
