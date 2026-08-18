#!/usr/bin/env python3
"""Fail closed when an active main-branch proof workflow drifts from the live lock.

Run from a checkout that has `origin/main` available.  Historical/rescue
workflows are intentionally excluded; only the active proof/robustness chain is
audited.
"""
from __future__ import annotations
import json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LOCK=json.loads((ROOT/'rtk/reproducibility_lock.json').read_text())
FILES=[
 '.github/workflows/rtk-autonomous-dense-rtk-stationarity.yml',
 '.github/workflows/rtk-autonomous-dense-rtk-half-stencil.yml',
 '.github/workflows/rtk-autonomous-dense-rtk-quarter-stencil.yml',
 '.github/workflows/rtk-autonomous-dense-rtk-eighth-stencil.yml',
 '.github/workflows/rtk-autonomous-negative-eigenray.yml',
 '.github/workflows/rtk-autonomous-half-negative-eigenray.yml',
 '.github/workflows/rtk-autonomous-quarter-negative-eigenray.yml',
 '.github/workflows/rtk-autonomous-dense-lcdm-stationarity.yml',
 '.github/workflows/rtk-clean-room-minimum-reproduction.yml',
 '.github/workflows/rtk-neutrino-mass-robustness.yml',
]
EXPECTED={
 'RTK_CLASS_UPSTREAM_SHA':str(LOCK['external_git']['class_public']['commit']),
 'RTK_PANTHEON_SHA':str(LOCK['external_git']['pantheon']['commit']),
 'RTK_PLANCK_SHA256':str(LOCK['likelihood']['planck_baseline_sha256']),
 'RTK_NUMPY_VERSION':str(LOCK['python_packages']['numpy']),
 'RTK_SCIPY_VERSION':str(LOCK['python_packages']['scipy']),
}

def text_at_main(path):
    p=subprocess.run(['git','show',f'origin/main:{path}'],text=True,capture_output=True)
    if p.returncode:
        raise RuntimeError(f'active workflow missing on origin/main: {path}: {p.stderr.strip()}')
    return p.stdout

bad=[];rows=[]
for path in FILES:
    text=text_at_main(path);found={}
    for key,expected in EXPECTED.items():
        m=re.search(rf'^\s*{re.escape(key)}:\s*[\'\"]?([^\'\"\s#]+)',text,re.M)
        actual=m.group(1) if m else None;found[key]=actual
        if actual!=expected:bad.append({'workflow':path,'key':key,'actual':actual,'expected':expected})
    if 'sha256sum -c -' not in text:bad.append({'workflow':path,'key':'planck_fail_closed_check','actual':False,'expected':True})
    rows.append({'workflow':path,'locked_values':found})
if bad:
    raise SystemExit('RTK_MAIN_WORKFLOW_LOCK_CONSISTENCY_FAIL '+json.dumps(bad,sort_keys=True))
print('RTK_MAIN_WORKFLOW_LOCK_CONSISTENCY_PASS',json.dumps(rows,sort_keys=True))
