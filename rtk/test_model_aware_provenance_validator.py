#!/usr/bin/env python3
"""No-network regression for RTK/LCDM locked proof-artifact provenance."""
import importlib.util,json
from pathlib import Path

P=Path(__file__).with_name('validate_artifact_identity.py')
spec=importlib.util.spec_from_file_location('rtk_identity',P)
V=importlib.util.module_from_spec(spec);assert spec and spec.loader;spec.loader.exec_module(V)

state={
 'production_mapping':'eff',
 'objective':{'name':'matched-ultra-linstep2+dense-BOSS','dense_z_pk':'x','recenter_tolerance_S':0.005,'ultra':{'a':'b'}},
 'rtk':{'accepted_center':{'lam':2.2e5,'h':0.69,'Ob':0.047,'Om':0.253,'As':2.08e-9,'ns':0.964,'zre':7.3}},
 'lcdm':{'accepted_center':{'lam':0.0,'h':0.678,'Ob':0.0486,'Om':0.261,'As':2.105e-9,'ns':0.965,'zre':7.79}},
}
repro={'runtime':{'python':'3.12.3'},'python_packages':{'numpy':'2.5.2','scipy':'1.18.0'},'likelihood':{'clipy_like':'0.15','planck_baseline_sha256':'abc'},'external_git':{'class_public':{'commit':'classsha'},'pantheon':{'commit':'pantheonsha'}}}

def make(model):
    key=model.lower();center=state[key]['accepted_center'];fp=V.canonical_hash({'model':model,'center':center,'objective':state['objective']['name'],'mapping':'eff'})
    ofp=V.canonical_hash(state['objective'])
    prov={'center_fingerprint':fp,'objective_fingerprint':ofp,'class_upstream_commit':'classsha','pantheon_commit':'pantheonsha','numpy_version':'2.5.2','rtk_source_commit':'researchsha'}
    return {'center_fingerprint':fp,'objective_fingerprint':ofp,'provenance':prov}

for model in ('RTK','LCDM'):
    s=make(model)
    out=V.validate_locked_provenance(state,repro,model.lower(),'hessian_run',123,s,{})
    assert out['objective_fingerprint_match'] is True
    assert out['center_fingerprint_match'] is True

bad=make('LCDM');bad['center_fingerprint']='0'*64;bad['provenance']['center_fingerprint']='0'*64
try:
    V.validate_locked_provenance(state,repro,'lcdm','hessian_run',124,bad,{})
except RuntimeError as exc:
    assert 'center_fingerprint' in str(exc)
else:
    raise AssertionError('bad LCDM center fingerprint was not rejected')

src=P.read_text()
assert "lcdm_proof_keys=('hessian_run',)" in src
assert "model=='lcdm' and key in lcdm_proof_keys" in src
print('RTK_MODEL_AWARE_PROVENANCE_VALIDATOR_UNIT_PASS')
