#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
FILES=[
 'inference_core.py','joint_profile_runner.py','boss_DR12Consensus_final.dat','final_consensus_covtot_dM_Hz_fsig.txt',
 'source/khronon_background.c','source/khronon_perturbations.c','include/khronon_background.h','include/khronon_perturbations.h'
]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(args,cwd='.'): return subprocess.check_output(['git','-C',cwd,*args],text=True).strip()
manifest={
 'stage':'candidate-production-objective-fingerprint-v1',
 'production_repo_head':sys.argv[1] if len(sys.argv)>1 else None,
 'class_public_head':git(['rev-parse','HEAD']),
 'class_public_branch':git(['rev-parse','--abbrev-ref','HEAD']),
 'files':{p:sha(p) for p in FILES},
 'objective_overrides':{
  'tol_background_integration':'3e-4','tol_thermo_integration':'3e-4','tol_perturb_integration':'3e-7',
  'perturb_sampling_stepsize':'0.0125','k_per_decade_for_pk':'40','k_per_decade_for_bao':'180',
  'k_max_tau0_over_l_max':'4.0','l_logstep':'1.02','l_linstep':'2',
  'z_pk_dense':'0.,0.25,0.30,0.34,0.36,0.37,0.38,0.39,0.40,0.42,0.47,0.49,0.50,0.51,0.52,0.53,0.55,0.57,0.59,0.60,0.61,0.62,0.63,0.65,0.70,0.75,1.0'},
 'likelihood':'Planck2018 baseline R3.00 Commander+SimAll+Plik-lite; Pantheon full covariance; BOSS DR12 9x9',
 'cache_semantics':'exact IEEE-754 normalized tuple; no decimal rounding',
 'status':'candidate frozen objective; requires matched RTK and LCDM reoptimization before model comparison'
}
blob=json.dumps(manifest,sort_keys=True,separators=(',',':')).encode(); manifest['manifest_sha256']=hashlib.sha256(blob).hexdigest()
Path('objective_fingerprint.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('OBJECTIVE_FINGERPRINT',json.dumps(manifest,sort_keys=True));print('OBJECTIVE_FINGERPRINT_COMPLETE')
