#!/usr/bin/env python3
"""Write and fail-closed validate provenance for a B4 neutrino seed artifact.

Run from the patched CLASS working directory after
``neutrino_reoptimization_seed.py MODEL``.  This helper does not evaluate the
likelihood and cannot change the seed candidate; it only makes the artifact
self-contained and checks it against the frozen B4 protocol and reproducibility
lock.
"""
from __future__ import annotations
from pathlib import Path
import hashlib, importlib.metadata, json, os, platform, subprocess, sys
import numpy as np
import scipy

MODEL=(sys.argv[1] if len(sys.argv)>1 else '').upper()
if MODEL not in ('RTK','LCDM'):
    raise SystemExit('usage: write_neutrino_seed_provenance.py RTK|LCDM')

STATE=json.loads(Path('../research/state/current.json').read_text())
LOCK=json.loads(Path('../rtk/reproducibility_lock.json').read_text())
OUT=Path('output/neutrino_reoptimization_seed')/MODEL.lower()
SUMMARY=OUT/'summary.json'
if not SUMMARY.exists():
    raise RuntimeError(f'missing seed summary: {SUMMARY}')
s=json.loads(SUMMARY.read_text())

OBJ='matched-ultra-linstep2+dense-BOSS+nu0p06-additive-v1'
NEUTRINO={'N_ncdm':1,'m_ncdm_eV':0.06,'T_ncdm':0.71611,'deg_ncdm':1.0,'N_ur':2.0328}
if s.get('objective')!=OBJ:
    raise RuntimeError(f'B4 objective mismatch: {s.get("objective")!r}')
if s.get('model')!=MODEL:
    raise RuntimeError(f'B4 model mismatch: {s.get("model")!r}')
if s.get('neutrino')!=NEUTRINO:
    raise RuntimeError(f'B4 neutrino block mismatch: {s.get("neutrino")!r}')
if s.get('massless_final_replay_run_id')!=32148894768:
    raise RuntimeError('B4 seed is not anchored to the frozen clean-room replay')


def canon_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def git_head(path):
    return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()

def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

base_objective=STATE['objective']
robustness_spec={
    'name':OBJ,
    'base_objective':base_objective,
    'production_mapping':'eff',
    'neutrino':NEUTRINO,
    'parameter_semantics':{
        'RTK':'As,Ob,Om(Khronon),h,loglambda_D,ns,zre',
        'LCDM':'As,Ob,Om(cdm),h,ns,zre',
        'massive_neutrino_density':'separate_CLASS_species_not_presubtracted_from_Om',
    },
}
objective_fp=canon_hash(robustness_spec)
start_fp=canon_hash({'model':MODEL,'objective':OBJ,'start_params':s['start_params']})

planck=Path('planck.tar.gz')
if not planck.exists():
    raise RuntimeError('Planck archive missing while writing B4 provenance')
planck_sha=sha256_file(planck)
expected_planck=LOCK['likelihood']['planck_baseline_sha256']
if planck_sha!=expected_planck:
    raise RuntimeError(f'Planck SHA mismatch {planck_sha} != {expected_planck}')

class_sha=git_head('.')
pantheon_sha=git_head('pantheon')
research_sha=git_head('..')
expected_class=LOCK['external_git']['class_public']['commit']
expected_pantheon=LOCK['external_git']['pantheon']['commit']
if class_sha!=expected_class:
    raise RuntimeError(f'CLASS SHA mismatch {class_sha} != {expected_class}')
if pantheon_sha!=expected_pantheon:
    raise RuntimeError(f'Pantheon SHA mismatch {pantheon_sha} != {expected_pantheon}')
if np.__version__!=LOCK['python_packages']['numpy']:
    raise RuntimeError('NumPy version mismatch')
if scipy.__version__!=LOCK['python_packages']['scipy']:
    raise RuntimeError('SciPy version mismatch')
if platform.python_version()!=LOCK['runtime']['python']:
    raise RuntimeError('Python version mismatch')
clipy_version=importlib.metadata.version('clipy-like')
if clipy_version!=LOCK['likelihood']['clipy_like']:
    raise RuntimeError('clipy-like version mismatch')

prov={
    'classification':'B4_NEUTRINO_SEED_PROVENANCE_PASS',
    'model':MODEL,
    'objective':OBJ,
    'objective_fingerprint':objective_fp,
    'start_fingerprint':start_fp,
    'research_source_commit':research_sha,
    'class_upstream_commit':class_sha,
    'pantheon_commit':pantheon_sha,
    'planck_baseline_sha256':planck_sha,
    'python_version':platform.python_version(),
    'numpy_version':np.__version__,
    'scipy_version':scipy.__version__,
    'clipy_like_version':clipy_version,
    'massless_final_replay_run_id':s['massless_final_replay_run_id'],
    'seed_summary_sha256':sha256_file(SUMMARY),
    'warning':'Provenance identity for a B4 seed candidate only; not stationarity/minimum certification.',
}
(OUT/'provenance.json').write_text(json.dumps(prov,indent=2,sort_keys=True)+'\n')
print('B4_NEUTRINO_SEED_PROVENANCE_PASS',json.dumps(prov,sort_keys=True))
