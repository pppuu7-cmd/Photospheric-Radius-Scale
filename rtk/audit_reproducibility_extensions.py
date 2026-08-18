#!/usr/bin/env python3
from pathlib import Path
import json

R=Path(__file__).resolve().parents[1]
L=json.loads((R/'rtk/reproducibility_lock.json').read_text())
W=(R/'rtk/autonomous_dense_lcdm_stationarity.py').read_text()
LWF=(R/'.github/workflows/rtk-autonomous-dense-lcdm-stationarity.yml').read_text()
IC=(R/'rtk/upgrade_rtk_nonlocal_initial_conditions.py').read_text()
RUN=(R/'rtk/joint_profile_runner.py').read_text()
ic_lock=L.get('nonlocal_initial_conditions',{}).get('background',{})
base=L.get('cosmology_baseline',{})
C={
'numpy':L.get('python_packages',{}).get('numpy')=='2.5.2',
'scipy':L.get('python_packages',{}).get('scipy')=='1.18.0',
'python':L.get('runtime',{}).get('python')=='3.12.3',
'planck_sha':L.get('likelihood',{}).get('planck_baseline_sha256')=='0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6',
'class_sha':L.get('external_git',{}).get('class_public',{}).get('commit')=='36cf283628c4a3330ec9fd3d84239bf775f77317',
'pantheon_sha':L.get('external_git',{}).get('pantheon',{}).get('commit')=='7eb29dc87ba223b4ec8457cd3cccba1216c36fb7',
'lcdm_steps_decoupled':"STATE['rtk']['base_steps']" not in W and 'DEFAULT_LCDM_STEPS' in W,
'lcdm_exact_three_retry':'for attempt in range(1,4)' in W and "L.CACHE.clear()" in W and 'failed after 3 exact retries' in W,
'lcdm_failure_not_cached':"if r.get('ok'):" in W and "E[k]=rr" in W and "AUTO_DENSE_LCDM_HESSIAN_RETRY" in W,
'lcdm_points_failures_provenance':all(x in W for x in ("POINTS=OUT/'points.jsonl'","FAILURES=OUT/'failures.jsonl'","CENTER_FINGERPRINT","OBJECTIVE_FINGERPRINT","provenance.json")),
'lcdm_workflow_dispatch_only':"workflow_dispatch:" in LWF and "  push:" not in LWF,
'lcdm_workflow_class_pin':"RTK_CLASS_UPSTREAM_SHA: '36cf283628c4a3330ec9fd3d84239bf775f77317'" in LWF and 'reset --hard "$RTK_CLASS_UPSTREAM_SHA"' in LWF,
'lcdm_workflow_pantheon_pin':"RTK_PANTHEON_SHA: '7eb29dc87ba223b4ec8457cd3cccba1216c36fb7'" in LWF and 'reset --hard "$RTK_PANTHEON_SHA"' in LWF,
'lcdm_workflow_planck_pin':"RTK_PLANCK_SHA256: '0b73171e3acc671c28184466a45485a2d1c1d93676b832abdfe688c7b04024e6'" in LWF and 'sha256sum -c -' in LWF,
'lcdm_workflow_numpy_scipy_pins':"RTK_NUMPY_VERSION: '2.5.2'" in LWF and "RTK_SCIPY_VERSION: '1.18.0'" in LWF and 'numpy==$RTK_NUMPY_VERSION' in LWF and 'scipy==$RTK_SCIPY_VERSION' in LWF,
'lcdm_workflow_nonlocal_ic_patch':'upgrade_rtk_nonlocal_initial_conditions.py' in LWF and "pba->V_prime_ini_nlde = 0.;" in LWF,
'lcdm_workflow_provenance_upload':all(x in LWF for x in ('provenance.json','points.jsonl','failures.jsonl','lcdm_hessian_pip_freeze.txt','lcdm_hessian_planck_sha256.txt')),
'nonlocal_aux_ic_lock':ic_lock=={'U_ini_nlde':0.0,'U_prime_ini_nlde':0.0,'V_ini_nlde':0.0,'V_prime_ini_nlde':0.0},
'nonlocal_aux_ic_production_flag':L.get('production_constraints',{}).get('explicit_zero_nonlocal_aux_background_ic') is True,
'nonlocal_aux_ic_patch_fail_closed':"text.count(old)" in IC and "count != 1" in IC and "pba->V_prime_ini_nlde = 0.;" in IC,
'nonlocal_aux_ic_ab_equivalent':L.get('nonlocal_initial_conditions',{}).get('ab_control',{}).get('delta_fixed_minus_old_score_eff')==0.0,
'neutrino_baseline_locked':base.get('N_ur')==3.046 and base.get('N_ncdm')==0,
'recombination_baseline_locked':base.get('recombination')=='RECFAST',
'neutrino_baseline_matches_runner':'"N_ur = 3.046"' in RUN and '"N_ncdm = 0"' in RUN,
'recombination_baseline_matches_runner':'"recombination = RECFAST"' in RUN,
}
b=[k for k,v in C.items() if not v]
if b:raise SystemExit('RTK_REPRO_EXT_AUDIT_FAIL '+json.dumps(b))
print('RTK_REPRO_EXT_AUDIT_PASS',json.dumps(sorted(C)))
