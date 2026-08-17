#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
L=json.loads((R/'rtk/reproducibility_lock.json').read_text())
W=(R/'rtk/autonomous_dense_lcdm_stationarity.py').read_text()
IC=(R/'rtk/upgrade_rtk_nonlocal_initial_conditions.py').read_text()
ic_lock=L.get('nonlocal_initial_conditions',{}).get('background',{})
C={
'numpy':L.get('python_packages',{}).get('numpy')=='2.5.2',
'scipy':L.get('python_packages',{}).get('scipy')=='1.18.0',
'python':L.get('runtime',{}).get('python')=='3.12.3',
'planck_sha':L.get('likelihood',{}).get('planck_baseline_sha256')=='0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6',
'class_sha':L.get('external_git',{}).get('class_public',{}).get('commit')=='36cf283628c4a3330ec9fd3d84239bf775f77317',
'pantheon_sha':L.get('external_git',{}).get('pantheon',{}).get('commit')=='7eb29dc87ba223b4ec8457cd3cccba1216c36fb7',
'lcdm_steps_decoupled':"STATE['rtk']['base_steps']" not in W and 'DEFAULT_LCDM_STEPS' in W,
'nonlocal_aux_ic_lock':ic_lock=={'U_ini_nlde':0.0,'U_prime_ini_nlde':0.0,'V_ini_nlde':0.0,'V_prime_ini_nlde':0.0},
'nonlocal_aux_ic_production_flag':L.get('production_constraints',{}).get('explicit_zero_nonlocal_aux_background_ic') is True,
'nonlocal_aux_ic_patch_fail_closed':"text.count(old)" in IC and "count != 1" in IC and "pba->V_prime_ini_nlde = 0.;" in IC,
'nonlocal_aux_ic_ab_equivalent':L.get('nonlocal_initial_conditions',{}).get('ab_control',{}).get('delta_fixed_minus_old_score_eff')==0.0,
}
b=[k for k,v in C.items() if not v]
if b:raise SystemExit('RTK_REPRO_EXT_AUDIT_FAIL '+json.dumps(b))
print('RTK_REPRO_EXT_AUDIT_PASS',json.dumps(sorted(C)))
