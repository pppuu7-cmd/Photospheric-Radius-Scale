#!/usr/bin/env python3
"""Fail closed if a completed autonomous artifact does not match current state.

The scientific orchestrator must never parse a successful artifact merely
because its workflow/run ID looks plausible. Before parsing, require the
artifact-declared objective and center to match the current accepted state.
For RTK Hessian/eigenray proof artifacts, additionally require canonical
objective/center fingerprints and measured upstream/runtime provenance. For
multiscale Hessians and source-scale eigenrays, also require the declared scale.

When a proof artifact carries runtime sidecars (Python version, pip freeze,
Planck archive SHA256), validate them against the live reproducibility lock as
well. This remains backward compatible with historical artifacts that predate
those sidecars.
"""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'research/state/current.json';REPRO=ROOT/'rtk/reproducibility_lock.json'
REPO=os.environ.get('GITHUB_REPOSITORY','pppuu7-cmd/Photospheric-Radius-Scale')
TOKEN=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')

def run(cmd,check=True):
    env=os.environ.copy()
    if TOKEN:env['GH_TOKEN']=TOKEN
    p=subprocess.run(cmd,text=True,capture_output=True,env=env)
    if check and p.returncode:raise RuntimeError(p.stderr.strip())
    return p

def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def _optional_unique_text(root,pattern,run_id):
    hits=list(root.rglob(pattern))
    if len(hits)>1:raise RuntimeError(f'run {run_id}: expected at most one {pattern}, found {len(hits)}')
    return hits[0].read_text() if hits else None

def download_bundle(run_id,artifact):
    td=Path(tempfile.mkdtemp(prefix=f'rtk-identity-{run_id}-'))
    try:
        p=run(['gh','run','download',str(run_id),'-R',REPO,'-n',artifact,'-D',str(td)],check=False)
        if p.returncode:raise RuntimeError(f'completed-success run {run_id} has no downloadable artifact {artifact}: {p.stderr.strip()}')
        hits=list(td.rglob('summary.json'))
        if len(hits)!=1:raise RuntimeError(f'run {run_id}: expected exactly one summary.json, found {len(hits)}')
        return {'summary':json.loads(hits[0].read_text()),'python_version':_optional_unique_text(td,'*python_version.txt',run_id),'pip_freeze':_optional_unique_text(td,'*pip_freeze.txt',run_id),'planck_sha256':_optional_unique_text(td,'*planck_sha256.txt',run_id)}
    finally:shutil.rmtree(td,ignore_errors=True)

def exact_center_equal(a,b):
    if not isinstance(a,dict) or not isinstance(b,dict):return False
    keys=('lam','h','Ob','Om','As','ns','zre')
    try:return all(float(a[k])==float(b[k]) for k in keys)
    except (KeyError,TypeError,ValueError):return False

def _canon_pkg(name):return re.sub(r'[-_.]+','-',name.strip().lower())

def validate_runtime_sidecars(repro,key,run_id,bundle):
    observed={};py=bundle.get('python_version')
    if py is not None:
        m=re.search(r'Python\s+([^\s]+)',py);actual=m.group(1) if m else None;expected=str(repro['runtime']['python'])
        if actual!=expected:raise RuntimeError(f'artifact runtime mismatch rtk.{key} run={run_id}: python={actual!r} expected={expected!r}')
        observed['python_version']=actual
    freeze=bundle.get('pip_freeze')
    if freeze is not None:
        packages={}
        for line in freeze.splitlines():
            if '==' not in line:continue
            name,version=line.split('==',1);packages[_canon_pkg(name)]=version.strip()
        expected_pkgs={'numpy':str(repro['python_packages']['numpy']),'scipy':str(repro['python_packages']['scipy']),'clipy-like':str(repro['likelihood']['clipy_like'])}
        bad={k:{'actual':packages.get(_canon_pkg(k)),'expected':v} for k,v in expected_pkgs.items() if packages.get(_canon_pkg(k))!=v}
        if bad:raise RuntimeError(f'artifact runtime package mismatch rtk.{key} run={run_id}: '+json.dumps(bad,sort_keys=True))
        observed['pip_locked_packages']=expected_pkgs
    ps=bundle.get('planck_sha256')
    if ps is not None:
        toks=ps.strip().split();actual=toks[0] if toks else None;expected=str(repro['likelihood']['planck_baseline_sha256'])
        if actual!=expected:raise RuntimeError(f'artifact runtime mismatch rtk.{key} run={run_id}: Planck SHA256={actual!r} expected={expected!r}')
        observed['planck_baseline_sha256']=actual
    return {'sidecars_present':{k:(bundle.get(k) is not None) for k in ('python_version','pip_freeze','planck_sha256')},**observed}

def validate_rtk_locked_provenance(state,repro,key,run_id,summary,bundle):
    prov=summary.get('provenance')
    if not isinstance(prov,dict):raise RuntimeError(f'artifact provenance missing rtk.{key} run={run_id}')
    expected_obj_fp=canonical_hash(state['objective']);actual_obj_fp=summary.get('objective_fingerprint') or prov.get('objective_fingerprint')
    if actual_obj_fp!=expected_obj_fp:raise RuntimeError(f'artifact provenance mismatch rtk.{key} run={run_id}: objective_fingerprint={actual_obj_fp!r} expected={expected_obj_fp!r}')
    expected_center_fp=canonical_hash({'model':'RTK','center':state['rtk']['accepted_center'],'objective':state['objective']['name'],'mapping':state.get('production_mapping','eff')});actual_center_fp=summary.get('center_fingerprint') or prov.get('center_fingerprint')
    if actual_center_fp!=expected_center_fp:raise RuntimeError(f'artifact provenance mismatch rtk.{key} run={run_id}: center_fingerprint={actual_center_fp!r} expected={expected_center_fp!r}')
    expected={'class_upstream_commit':repro['external_git']['class_public']['commit'],'pantheon_commit':repro['external_git']['pantheon']['commit'],'numpy_version':repro['python_packages']['numpy']};observed={k:prov.get(k) for k in expected}
    bad={k:{'actual':observed[k],'expected':expected[k]} for k in expected if observed[k]!=expected[k]}
    if bad:raise RuntimeError(f'artifact locked provenance mismatch rtk.{key} run={run_id}: '+json.dumps(bad,sort_keys=True))
    return {'objective_fingerprint_match':True,'center_fingerprint_match':True,**expected,'rtk_source_commit':prov.get('rtk_source_commit'),'runtime_sidecars':validate_runtime_sidecars(repro,key,run_id,bundle)}

def validate_slot(state,repro,model,key):
    slot=state.get(model,{}).get(key)
    if not isinstance(slot,dict):return None
    if slot.get('status')!='completed' or slot.get('conclusion')!='success' or slot.get('parsed'):return None
    run_id=int(slot['run_id']);bundle=download_bundle(run_id,slot['artifact']);summary=bundle['summary'];expected_objective=state['objective']['name']
    if summary.get('objective')!=expected_objective:raise RuntimeError(f'artifact identity mismatch {model}.{key} run={run_id}: objective={summary.get("objective")!r} expected={expected_objective!r}')
    expected_center=state[model]['accepted_center']
    if not exact_center_equal(summary.get('center'),expected_center):raise RuntimeError(f'artifact identity mismatch {model}.{key} run={run_id}: summary center does not equal current accepted_center')
    expected_scale=slot.get('expected_stencil_scale')
    if expected_scale is not None:
        actual=summary.get('stencil_scale')
        try:scale_match=float(actual)==float(expected_scale)
        except (TypeError,ValueError):scale_match=False
        if not scale_match:raise RuntimeError(f'artifact identity mismatch {model}.{key} run={run_id}: stencil_scale={actual!r} expected={expected_scale!r}')
    expected_source_scale=slot.get('expected_source_stencil_scale')
    if expected_source_scale is not None:
        actual=summary.get('source_stencil_scale')
        try:scale_match=float(actual)==float(expected_source_scale)
        except (TypeError,ValueError):scale_match=False
        if not scale_match:raise RuntimeError(f'artifact identity mismatch {model}.{key} run={run_id}: source_stencil_scale={actual!r} expected={expected_source_scale!r}')
    expected_source=slot.get('expected_eigenray_source')
    if expected_source is not None and summary.get('eigenray_source')!=expected_source:
        raise RuntimeError(f'artifact identity mismatch {model}.{key} run={run_id}: eigenray_source={summary.get("eigenray_source")!r} expected={expected_source!r}')
    row={'slot':f'{model}.{key}','run_id':run_id,'objective':expected_objective,'center_match':True,'stencil_scale':summary.get('stencil_scale'),'source_stencil_scale':summary.get('source_stencil_scale'),'eigenray_source':summary.get('eigenray_source')}
    proof_keys=('hessian_run','half_hessian_run','quarter_hessian_run','eighth_hessian_run','negative_eigenray_run','half_negative_eigenray_run','quarter_negative_eigenray_run')
    if model=='rtk' and key in proof_keys:row['locked_provenance']=validate_rtk_locked_provenance(state,repro,key,run_id,summary,bundle)
    return row

def main():
    state=json.loads(STATE.read_text());repro=json.loads(REPRO.read_text());checked=[]
    slots=(('rtk','axis_run'),('rtk','hessian_run'),('rtk','negative_eigenray_run'),('rtk','half_hessian_run'),('rtk','half_negative_eigenray_run'),('rtk','quarter_hessian_run'),('rtk','quarter_negative_eigenray_run'),('rtk','eighth_hessian_run'),('lcdm','hessian_run'))
    for model,key in slots:
        row=validate_slot(state,repro,model,key)
        if row:checked.append(row)
    print('RTK_ARTIFACT_IDENTITY_PASS',json.dumps(checked,sort_keys=True))
if __name__=='__main__':main()
