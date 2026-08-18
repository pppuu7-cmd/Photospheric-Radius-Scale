#!/usr/bin/env python3
"""Independent fresh-tree replay of the finally certified matched RTK/LCDM pair.

This worker is deliberately gated on Stage-4D3 interior-minimum certification.
It does not optimize. It re-evaluates the exact accepted-score parameter points
from state in a fresh pinned CLASS/likelihood tree and verifies numerical score
reproduction under the frozen dense+ultra objective.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

sys.argv=['clean_room_matched_pair_replay','planck_data']
import inference_core as L

ROOT=Path('..')
STATE=json.loads((ROOT/'research/state/current.json').read_text())
OUT=Path('output/clean_room_matched_pair');OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl';FAILURES=OUT/'failures.jsonl'
TOL=2e-6
OBJECTIVE_NAME='matched-ultra-linstep2+dense-BOSS'
ALLOWED_N5={
    'N5_BASE_AND_HALF_STENCIL_PASS',
    'N5_ADAPTIVE_HALF_AND_QUARTER_PASS',
}


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def append_jsonl(path,row):
    with path.open('a') as f:
        f.write(json.dumps(row,sort_keys=True,default=str)+'\n');f.flush()


def require_state_ready():
    if STATE.get('objective',{}).get('name')!=OBJECTIVE_NAME:
        raise RuntimeError('final replay objective mismatch')
    if STATE.get('production_mapping')!='eff':
        raise RuntimeError('final replay requires production mapping eff')
    rtk=STATE.get('rtk',{});lcdm=STATE.get('lcdm',{})
    if rtk.get('certification')!='local_dense_accepted':
        raise RuntimeError('RTK local dense candidate not certified')
    if rtk.get('interior_minimum_certification') not in ALLOWED_N5:
        raise RuntimeError('RTK Stage4D3 interior minimum not certified')
    if lcdm.get('certification')!='local_dense_accepted':
        raise RuntimeError('LCDM local dense candidate not certified')
    for name,block in (('RTK',rtk),('LCDM',lcdm)):
        if not isinstance(block.get('accepted_score_params'),dict):
            raise RuntimeError(f'{name} accepted_score_params missing')
        if block.get('accepted_score_eff') is None:
            raise RuntimeError(f'{name} accepted_score_eff missing')
    cmp=STATE.get('comparison',{})
    if cmp.get('status')!='matched_local_dense_raw_fit_ready' or not cmp.get('interior_minimum_certified'):
        raise RuntimeError('matched comparison is not final local-dense-ready')


require_state_ready()

SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
orig=L.make_ini


def make_ini(model,p,tag):
    path=orig(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:
        raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text)
        f.write('\n# clean-room final matched dense+ultra replay\n')
        for k,v in ULTRA.items():f.write(f'{k} = {v}\n')
    return path


L.make_ini=make_ini


def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass


def evaluate_exact(model,params):
    last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate(model,dict(params))
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={
                'model':model,'attempt':attempt,'params':dict(params),
                'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
                'components':{k:r.get(k) for k in ('logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01','rd')},
            }
            append_jsonl(POINTS,row);cleanup(r.get('tag'));return row
        last=r
        failure={'model':model,'attempt':attempt,'params':dict(params),'result':r}
        append_jsonl(FAILURES,failure);cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'{model} replay failed after 3 identical exact retries: {last}')


rtk_state=STATE['rtk'];lcdm_state=STATE['lcdm'];cmp=STATE['comparison']
rtk_params=dict(rtk_state['accepted_score_params']);lcdm_params=dict(lcdm_state['accepted_score_params'])
rtk=evaluate_exact('RTK',rtk_params)
lcdm=evaluate_exact('LCDM',lcdm_params)

expected_rtk=float(rtk_state['accepted_score_eff'])
expected_lcdm=float(lcdm_state['accepted_score_eff'])
actual_rtk=float(rtk['score_eff']);actual_lcdm=float(lcdm['score_eff'])
expected_delta=expected_rtk-expected_lcdm
actual_delta=actual_rtk-actual_lcdm
errors={
    'rtk_eff':actual_rtk-expected_rtk,
    'lcdm_eff':actual_lcdm-expected_lcdm,
    'delta_eff':actual_delta-expected_delta,
}
passed=abs(errors['rtk_eff'])<=TOL and abs(errors['lcdm_eff'])<=TOL

summary={
    'status':'PASS' if passed else 'FAIL',
    'classification':'INDEPENDENT_FRESH_TREE_MATCHED_MINIMA_REPLAY',
    'objective':STATE['objective'],
    'objective_fingerprint':canonical_hash(STATE['objective']),
    'production_mapping':STATE['production_mapping'],
    'state_iteration':STATE.get('iteration'),
    'state_last_iteration':STATE.get('last_iteration'),
    'rtk_interior_minimum_certification':rtk_state.get('interior_minimum_certification'),
    'score_tolerance_abs':TOL,
    'rtk':{
        'params':rtk_params,
        'params_fingerprint':canonical_hash(rtk_params),
        'expected_score_eff':expected_rtk,
        'replayed_score_eff':actual_rtk,
        'score_error_eff':errors['rtk_eff'],
        'score_k01':rtk['score_k01'],
        'components':rtk['components'],
        'attempt':rtk['attempt'],
    },
    'lcdm':{
        'params':lcdm_params,
        'params_fingerprint':canonical_hash(lcdm_params),
        'expected_score_eff':expected_lcdm,
        'replayed_score_eff':actual_lcdm,
        'score_error_eff':errors['lcdm_eff'],
        'score_k01':lcdm['score_k01'],
        'components':lcdm['components'],
        'attempt':lcdm['attempt'],
    },
    'comparison':{
        'expected_delta_S_eff':expected_delta,
        'replayed_delta_S_eff':actual_delta,
        'delta_replay_error':errors['delta_eff'],
        'state_dense_raw_delta_S':cmp.get('dense_raw_delta_S'),
    },
    'warning':'Independent numerical replay of frozen local minima only; not evidence of global optimality, preference, significance, AIC/BIC or Bayes factors.',
}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_CLEAN_ROOM_MATCHED_PAIR_REPLAY',json.dumps(summary,sort_keys=True),flush=True)
if not passed:
    raise SystemExit('RTK_CLEAN_ROOM_MATCHED_PAIR_REPLAY_MISMATCH '+json.dumps(errors,sort_keys=True))
print('RTK_CLEAN_ROOM_MATCHED_PAIR_REPLAY_PASS',flush=True)
