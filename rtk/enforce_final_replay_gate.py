#!/usr/bin/env python3
"""Autonomous fail-closed gate for independent final matched-minima replay."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STATE=ROOT/'research/state/current.json'
DISPATCH=ROOT/'research/state/dispatch_request.json'
LOCK_PATH=ROOT/'rtk/reproducibility_lock.json'
REPO=os.environ.get('GITHUB_REPOSITORY','pppuu7-cmd/Photospheric-Radius-Scale')
TOKEN=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
WF='rtk-clean-room-minimum-reproduction.yml'
ART='rtk-clean-room-matched-minima-reproduction'
TARGET='final_matched_minima_replay'
CLASSIFICATION='INDEPENDENT_FRESH_TREE_MATCHED_MINIMA_REPLAY'
TOL=2e-6
ALLOWED_N5={'N5_BASE_AND_HALF_STENCIL_PASS','N5_ADAPTIVE_HALF_AND_QUARTER_PASS'}
REQUIRED_REPLAY_SOURCE_COMMIT='d5d0d927ed8f0c94b070a844da152ad399db634a'


def run(cmd,check=True):
    env=os.environ.copy()
    if TOKEN:env['GH_TOKEN']=TOKEN
    p=subprocess.run(cmd,text=True,capture_output=True,env=env)
    if check and p.returncode:raise RuntimeError(p.stderr.strip() or 'command failed')
    return p


def gh(endpoint):return json.loads(run(['gh','api',endpoint]).stdout)
def get_run(run_id):return gh(f'repos/{REPO}/actions/runs/{int(run_id)}')


def parse_utc(value):
    if not isinstance(value,str) or not value:raise ValueError('missing timestamp')
    if value.endswith('Z'):value=value[:-1]+'+00:00'
    out=dt.datetime.fromisoformat(value)
    if out.tzinfo is None:out=out.replace(tzinfo=dt.timezone.utc)
    return out.astimezone(dt.timezone.utc)


def latest_qualifying(workflow,requested_at):
    rows=gh(f'repos/{REPO}/actions/workflows/{workflow}/runs?per_page=30').get('workflow_runs',[])
    t0=parse_utc(requested_at)
    good=[]
    for r in rows:
        try:t=parse_utc(r.get('created_at'))
        except Exception:continue
        actor=r.get('actor') if isinstance(r.get('actor'),dict) else {}
        if r.get('event')=='workflow_dispatch' and r.get('head_branch')=='main' and actor.get('login')=='github-actions[bot]' and t>=t0:
            good.append((t,r))
    return min(good,key=lambda x:x[0])[1] if good else None


def download_summary(run_id):
    td=Path(tempfile.mkdtemp(prefix=f'rtk-final-replay-{run_id}-'))
    try:
        p=run(['gh','run','download',str(run_id),'-R',REPO,'-n',ART,'-D',str(td)],check=False)
        if p.returncode:return None
        hits=list(td.rglob('summary.json'))
        if len(hits)!=1:raise RuntimeError(f'final replay run {run_id}: expected one summary.json, found {len(hits)}')
        return json.loads(hits[0].read_text())
    finally:shutil.rmtree(td,ignore_errors=True)


def canonical_hash(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def params_equal(a,b):
    keys=('lam','h','Ob','Om','As','ns','zre')
    try:return all(float(a[k])==float(b[k]) for k in keys)
    except Exception:return False


def ready(state):
    rtk=state.get('rtk',{});lcdm=state.get('lcdm',{});cmp=state.get('comparison',{})
    return (
        state.get('objective',{}).get('name')=='matched-ultra-linstep2+dense-BOSS'
        and state.get('production_mapping')=='eff'
        and rtk.get('certification')=='local_dense_accepted'
        and rtk.get('interior_minimum_certification') in ALLOWED_N5
        and isinstance(rtk.get('accepted_score_params'),dict)
        and rtk.get('accepted_score_eff') is not None
        and lcdm.get('certification')=='local_dense_accepted'
        and isinstance(lcdm.get('accepted_score_params'),dict)
        and lcdm.get('accepted_score_eff') is not None
        and cmp.get('status')=='matched_local_dense_raw_fit_ready'
        and cmp.get('interior_minimum_certified') is True
    )


def target_payload(state):
    return {
        'objective':state['objective'],
        'mapping':state['production_mapping'],
        'rtk':{
            'params':state['rtk']['accepted_score_params'],
            'score_eff':float(state['rtk']['accepted_score_eff']),
            'n5':state['rtk']['interior_minimum_certification'],
        },
        'lcdm':{
            'params':state['lcdm']['accepted_score_params'],
            'score_eff':float(state['lcdm']['accepted_score_eff']),
        },
    }


def target_fingerprint(state):return canonical_hash(target_payload(state))


def git_is_ancestor(base,head):
    p=run(['git','merge-base','--is-ancestor',base,head],check=False)
    return p.returncode==0


def validate_summary(summary,state,lock,check_git=True):
    errors=[]
    if not isinstance(summary,dict):return ['summary_not_object']
    if summary.get('status')!='PASS':errors.append('status_not_PASS')
    if summary.get('classification')!=CLASSIFICATION:errors.append('classification_mismatch')
    if summary.get('objective')!=state.get('objective'):errors.append('objective_mismatch')
    if summary.get('production_mapping')!='eff':errors.append('mapping_mismatch')
    if summary.get('rtk_interior_minimum_certification')!=state['rtk'].get('interior_minimum_certification'):errors.append('n5_mismatch')
    if float(summary.get('score_tolerance_abs',1e99))!=TOL:errors.append('tolerance_mismatch')
    sr=summary.get('rtk') if isinstance(summary.get('rtk'),dict) else {}
    sl=summary.get('lcdm') if isinstance(summary.get('lcdm'),dict) else {}
    if not params_equal(sr.get('params'),state['rtk'].get('accepted_score_params')):errors.append('rtk_params_mismatch')
    if not params_equal(sl.get('params'),state['lcdm'].get('accepted_score_params')):errors.append('lcdm_params_mismatch')
    er=float(state['rtk']['accepted_score_eff']);el=float(state['lcdm']['accepted_score_eff'])
    try:
        if float(sr.get('expected_score_eff'))!=er:errors.append('rtk_expected_score_mismatch')
        if float(sl.get('expected_score_eff'))!=el:errors.append('lcdm_expected_score_mismatch')
        if abs(float(sr.get('score_error_eff')))>TOL:errors.append('rtk_replay_error')
        if abs(float(sl.get('score_error_eff')))>TOL:errors.append('lcdm_replay_error')
        replay_delta=float(summary['comparison']['replayed_delta_S_eff'])
        if abs(replay_delta-(float(sr['replayed_score_eff'])-float(sl['replayed_score_eff'])))>1e-12:errors.append('delta_internal_inconsistency')
    except Exception:errors.append('score_fields_malformed')
    prov=summary.get('provenance') if isinstance(summary.get('provenance'),dict) else {}
    cls=lock.get('external_git',{}).get('class_public',{}).get('commit')
    pan=lock.get('external_git',{}).get('pantheon',{}).get('commit')
    psha=lock.get('likelihood',{}).get('planck_baseline_sha256')
    nv=lock.get('python_packages',{}).get('numpy');sv=lock.get('python_packages',{}).get('scipy')
    if prov.get('class_upstream_commit')!=cls or prov.get('class_upstream_sha_expected')!=cls:errors.append('class_provenance_mismatch')
    if prov.get('pantheon_commit')!=pan or prov.get('pantheon_sha_expected')!=pan:errors.append('pantheon_provenance_mismatch')
    if prov.get('planck_sha256_expected')!=psha:errors.append('planck_provenance_mismatch')
    if prov.get('numpy_version')!=nv or prov.get('numpy_version_expected')!=nv:errors.append('numpy_provenance_mismatch')
    if prov.get('scipy_version')!=sv or prov.get('scipy_version_expected')!=sv:errors.append('scipy_provenance_mismatch')
    if prov.get('cache_key_version')!='clean-room-exact-float-v2':errors.append('cache_key_version_mismatch')
    src=prov.get('research_source_commit')
    if not isinstance(src,str) or len(src)!=40:errors.append('research_source_commit_missing')
    elif check_git and not git_is_ancestor(REQUIRED_REPLAY_SOURCE_COMMIT,src):errors.append('replay_source_predates_required_worker')
    return errors


def write_dispatch(state,slot):
    if DISPATCH.exists():return False
    req={
        'created_at':state.get('updated_at'),
        'iteration':state.get('iteration'),
        'workflow':WF,
        'ref':'main',
        'reason':'Independent fresh-tree replay required after Stage4D3 matched local-minimum certification',
        'target':TARGET,
        'target_fingerprint':slot['target_fingerprint'],
    }
    DISPATCH.write_text(json.dumps(req,indent=2,sort_keys=True)+'\n')
    state['dispatch']=req
    return True


def archive_stale(state,changes):
    if any(state.get(k) is not None for k in ('final_replay_run','final_replay_result','final_replay_certification')):
        state.setdefault('final_replay_history',[]).append({
            'run':state.get('final_replay_run'),
            'result':state.get('final_replay_result'),
            'certification':state.get('final_replay_certification'),
        })
        state['final_replay_run']=None;state['final_replay_result']=None;state['final_replay_certification']=None
        changes.append('archive_stale_final_replay')


def main():
    state=json.loads(STATE.read_text());lock=json.loads(LOCK_PATH.read_text());changes=[]
    if not ready(state):
        # If scientific state moved away from a previously replayed target,
        # invalidate the replay rather than carrying it through recentering.
        if state.get('final_replay_certification')=='INDEPENDENT_FRESH_TREE_REPLAY_PASS':archive_stale(state,changes)
        if changes:STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
        print('RTK_FINAL_REPLAY_GATE',json.dumps(changes,sort_keys=True));return

    fp=target_fingerprint(state)
    slot=state.get('final_replay_run')
    if isinstance(slot,dict) and slot.get('target_fingerprint')!=fp:
        archive_stale(state,changes);slot=None

    if slot is None:
        slot={
            'run_id':None,'workflow':WF,'artifact':ART,'status':'requested',
            'requested_at':state.get('updated_at'),'target_fingerprint':fp,
        }
        state['final_replay_run']=slot
        state['final_replay_certification']='PENDING_INDEPENDENT_FRESH_TREE_REPLAY'
        state['stage']='final_matched_replay_running'
        if write_dispatch(state,slot):changes.append('dispatch_final_matched_minima_replay')
        STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
        print('RTK_FINAL_REPLAY_GATE',json.dumps(changes,sort_keys=True));return

    if not slot.get('run_id'):
        d=state.get('dispatch') if isinstance(state.get('dispatch'),dict) else {}
        rr=None
        if d.get('target')==TARGET and d.get('run_id') and d.get('target_fingerprint',fp)==fp:
            rr=get_run(d['run_id'])
        else:
            rr=latest_qualifying(WF,slot.get('requested_at') or state.get('updated_at'))
        if rr:
            slot['run_id']=int(rr['id']);slot['status']=rr.get('status');slot['conclusion']=rr.get('conclusion');slot['html_url']=rr.get('html_url')
            changes.append(f"attach_final_replay_run_{slot['run_id']}")
    else:
        rr=get_run(slot['run_id']);slot['status']=rr.get('status');slot['conclusion']=rr.get('conclusion');slot['html_url']=rr.get('html_url')

    if slot.get('status')=='completed' and slot.get('conclusion')=='success' and not slot.get('parsed'):
        summary=download_summary(slot['run_id'])
        if summary is None:
            state['final_replay_certification']='FINAL_REPLAY_ARTIFACT_MISSING';state['stage']='final_matched_replay_failed';changes.append('final_replay_artifact_missing')
        else:
            errors=validate_summary(summary,state,lock,check_git=True)
            state['final_replay_result']=summary;slot['parsed']=True;slot['validation_errors']=errors
            if errors:
                state['final_replay_certification']='FINAL_REPLAY_IDENTITY_OR_SCORE_MISMATCH';state['stage']='final_matched_replay_failed';changes.append('final_replay_validation_failed')
            else:
                state['final_replay_certification']='INDEPENDENT_FRESH_TREE_REPLAY_PASS';state['final_replay_target_fingerprint']=fp;state['stage']='matched_dense_replay_verified'
                state.setdefault('comparison',{})['final_replay_certified']=True
                state['comparison']['replayed_dense_raw_delta_S']=float(summary['comparison']['replayed_delta_S_eff'])
                state['comparison']['final_replay_run_id']=slot['run_id']
                changes.append('final_matched_minima_replay_pass')
    elif slot.get('status')=='completed' and slot.get('conclusion') not in (None,'success'):
        state['final_replay_certification']='FINAL_REPLAY_COMPUTE_FAILURE';state['stage']='final_matched_replay_failed';changes.append('final_replay_compute_failure')
    elif slot.get('parsed') and state.get('final_replay_certification')=='INDEPENDENT_FRESH_TREE_REPLAY_PASS':
        state.setdefault('comparison',{})['final_replay_certified']=True
        if isinstance(state.get('final_replay_result'),dict):
            state['comparison']['replayed_dense_raw_delta_S']=float(state['final_replay_result']['comparison']['replayed_delta_S_eff'])
            state['comparison']['final_replay_run_id']=slot.get('run_id')
        state['stage']='matched_dense_replay_verified'
    else:
        state['final_replay_certification']='PENDING_INDEPENDENT_FRESH_TREE_REPLAY';state['stage']='final_matched_replay_running'

    STATE.write_text(json.dumps(state,indent=2,sort_keys=True)+'\n')
    print('RTK_FINAL_REPLAY_GATE',json.dumps(changes,sort_keys=True))


if __name__=='__main__':main()
