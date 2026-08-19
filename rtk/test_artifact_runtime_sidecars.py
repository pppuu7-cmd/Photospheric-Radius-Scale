#!/usr/bin/env python3
"""No-network regression tests for proof-artifact runtime sidecar validation."""
import importlib.util
from pathlib import Path

MODULE=Path(__file__).with_name('validate_artifact_identity.py')
spec=importlib.util.spec_from_file_location('rtk_artifact_identity',MODULE)
M=importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(M)

REPRO={
  'runtime':{'python':'3.12.3'},
  'python_packages':{'numpy':'2.5.2','scipy':'1.18.0'},
  'likelihood':{'clipy_like':'0.15','planck_baseline_sha256':'abc123'},
}
GOOD={
  'python_version':'Python 3.12.3\n',
  'pip_freeze':'clipy-like==0.15\nnumpy==2.5.2\nscipy==1.18.0\n',
  'planck_sha256':'abc123  planck.tar.gz\n',
}
r=M.validate_runtime_sidecars(REPRO,'rtk','half_hessian_run',123,GOOD)
assert r['python_version']=='3.12.3'
assert r['planck_baseline_sha256']=='abc123'
assert r['pip_locked_packages']['numpy']=='2.5.2'

# Historical artifacts with no runtime sidecars remain backward compatible.
r=M.validate_runtime_sidecars(REPRO,'rtk','negative_eigenray_run',124,{'python_version':None,'pip_freeze':None,'planck_sha256':None})
assert not any(r['sidecars_present'].values())

# LCDM uses the same runtime-sidecar checker with an explicit model label.
r=M.validate_runtime_sidecars(REPRO,'lcdm','hessian_run',124,GOOD)
assert r['python_version']=='3.12.3'

for label,bad in [
  ('python',{**GOOD,'python_version':'Python 3.12.4\n'}),
  ('numpy',{**GOOD,'pip_freeze':'clipy-like==0.15\nnumpy==2.5.3\nscipy==1.18.0\n'}),
  ('scipy',{**GOOD,'pip_freeze':'clipy_like==0.15\nnumpy==2.5.2\nscipy==1.18.1\n'}),
  ('clipy',{**GOOD,'pip_freeze':'clipy_like==0.16\nnumpy==2.5.2\nscipy==1.18.0\n'}),
  ('planck',{**GOOD,'planck_sha256':'deadbeef  planck.tar.gz\n'}),
]:
    try:
        M.validate_runtime_sidecars(REPRO,'rtk','half_hessian_run',125,bad)
    except RuntimeError:
        pass
    else:
        raise AssertionError(f'{label} mismatch was not rejected')

print('RTK_ARTIFACT_RUNTIME_SIDECARS_UNIT_PASS')
