#!/usr/bin/env python3
"""Conditional exact A5 LCDM forward-line continuation beyond t=1.9.

The target is frozen before the parent t=1.1..1.9 result exists. Execution is
allowed only if that persisted result ends at the upper boundary t=1.9 with an
exact improvement above the frozen 0.005 recenter threshold.
"""
from pathlib import Path
import json, math, os, subprocess, time

os.environ.setdefault('CLIPY_NOJAX', '1')
import inference_core as L

ROOT = Path('..')
TARGET_PATH = ROOT / 'research/robustness/A5_LCDM_T1P9_FORWARD_LINE_CONTINUATION_TARGET_v2.json'
t = json.loads(TARGET_PATH.read_text())
s = json.loads((ROOT / 'research/state/current.json').read_text())
p = json.loads((ROOT / t['prerequisite']['result']).read_text())

assert t['classification'] == 'A5_LCDM_T1P9_FORWARD_LINE_CONTINUATION_TARGET_V2_FROZEN'
assert t['frozen_before_v1_forward_result'] is True
assert t['objective'] == s['objective']['name'] == 'matched-ultra-linstep2+dense-BOSS'
assert t['production_mapping'] == 'eff'
req = t['prerequisite']
if p.get('classification') != req['required_classification']:
    raise RuntimeError(f"v1 prerequisite classification mismatch: {p.get('classification')!r}")
if p.get('decision') != req['required_decision']:
    raise RuntimeError(f"v1 prerequisite decision does not authorize extension: {p.get('decision')!r}")
if abs(float(p.get('best_sample_t')) - float(req['required_best_sample_t'])) > 1e-12:
    raise RuntimeError(f"v1 best point is not frozen boundary t=1.9: {p.get('best_sample_t')!r}")
if not float(p.get('improvement_vs_t1p1')) > float(req['required_improvement_gt']):
    raise RuntimeError('v1 improvement does not exceed frozen recenter threshold')

OLD = t['line_definition']['historical_center']
NEW = t['line_definition']['t1_seed']
GRID = [float(x) for x in t['t_grid']]
DENSE = s['objective']['dense_z_pk']
ULTRA = {k: str(v) for k, v in s['objective']['ultra'].items()}
SPARSE = '0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
OUT = ROOT / 'output/a5_lcdm_t1p9_forward_line_v2'
OUT.mkdir(parents=True, exist_ok=True)
PTS = OUT / 'points.jsonl'
FAIL = OUT / 'failures.jsonl'
SUMMARY = OUT / 'summary.json'

ORIG = L.make_ini
def make_ini(model, pars, tag):
    path = ORIG(model, pars, tag)
    text = Path(path).read_text()
    if 'z_pk = ' + SPARSE in text:
        text = text.replace('z_pk = ' + SPARSE, 'z_pk = ' + DENSE, 1)
    elif 'z_pk = ' + DENSE not in text:
        raise RuntimeError('dense A5 objective not established')
    text += '\n# A5 conditional t1p9 forward continuation v2\n'
    text += ''.join(f'{k} = {v}\n' for k, v in ULTRA.items())
    Path(path).write_text(text)
    return path
L.make_ini = make_ini


def append(path, row):
    with path.open('a') as f:
        f.write(json.dumps(row, sort_keys=True, allow_nan=False) + '\n')
        f.flush()


def cleanup(tag):
    if not tag:
        return
    for q in L.OUT.glob(tag + '_*'):
        try: q.unlink()
        except OSError: pass
    for q in (Path(f'profile_{tag}.ini'), Path(f'profile_{tag}.log')):
        try: q.unlink()
        except OSError: pass


def params_at(x):
    return {k: (0.0 if k == 'lam' else float(OLD[k]) + float(x) * (float(NEW[k]) - float(OLD[k]))) for k in OLD}


def evaluate(x):
    pars = params_at(x)
    last = None
    for attempt in (1, 2, 3):
        L.CACHE.clear()
        try:
            r = L.evaluate('LCDM', pars)
        except Exception as exc:
            r = {'ok': False, 'exception': repr(exc)}
        if r.get('ok'):
            row = {
                't': float(x), 'attempt': attempt, 'params': pars,
                'score_eff': float(r['score']), 'score_k01': float(r['score_k01']),
                'logL_planck': r.get('logL_planck'), 'chi2_SN': r.get('chi2_SN'),
                'chi2_BOSS_eff': r.get('chi2_BOSS_eff'), 'chi2_BOSS_k01': r.get('chi2_BOSS_k01'),
                'rd': r.get('rd')
            }
            if not (math.isfinite(row['score_eff']) and math.isfinite(row['score_k01'])):
                raise RuntimeError('nonfinite exact score')
            append(PTS, row); cleanup(r.get('tag'))
            print('A5_T1P9_FORWARD_V2_POINT', json.dumps(row, sort_keys=True), flush=True)
            return row
        last = r
        append(FAIL, {'t': float(x), 'attempt': attempt, 'params': pars, 'result': r})
        cleanup(r.get('tag') if isinstance(r, dict) else None)
        if attempt < 3: time.sleep(2 * attempt)
    raise RuntimeError(f'failed exact evaluation t={x}: {last}')


rows = [evaluate(x) for x in GRID]
by = {round(float(r['t']), 12): r for r in rows}
anchor = by[1.9]
expected = float(p['best_sample_score'])
anchor_err = abs(float(anchor['score_eff']) - expected)
if anchor_err > float(t['replay_anchor']['tolerance_abs']):
    raise RuntimeError(f't=1.9 parent replay mismatch {anchor_err}')

best = min(rows, key=lambda r: r['score_eff'])
improvement = float(anchor['score_eff']) - float(best['score_eff'])
upper = max(GRID)
if improvement > float(t['recenter_tolerance_S']) and abs(float(best['t']) - upper) < 1e-12:
    decision = 'EXTEND_FORWARD_FROM_BOUNDARY_AGAIN'
elif improvement > float(t['recenter_tolerance_S']):
    decision = 'RECENTER_AT_BEST_SAMPLED_POINT'
else:
    decision = 'T1P9_FORWARD_CLEAR_STATIONARITY_REQUIRED'

summary = {
    'schema': 'A5_LCDM_T1P9_FORWARD_LINE_CONTINUATION_RESULT_v2',
    'status': 'PASS',
    'classification': 'A5_LCDM_T1P9_FORWARD_LINE_CONTINUATION_V2_COMPLETE',
    'objective': t['objective'],
    'production_mapping': 'eff',
    'parent_result': t['prerequisite']['result'],
    'parent_t1p9_score': expected,
    't1p9_replay_abs_error': anchor_err,
    'best_sample_t': float(best['t']),
    'best_sample_score': float(best['score_eff']),
    'improvement_vs_t1p9': improvement,
    'best_params': best['params'],
    'decision': decision,
    'rows': rows,
    'recenter_tolerance_S': float(t['recenter_tolerance_S']),
    'research_source_commit': subprocess.check_output(['git', '-C', '..', 'rev-parse', 'HEAD'], text=True).strip(),
    'warning': t['guard']
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + '\n')
print('A5_LCDM_T1P9_FORWARD_LINE_CONTINUATION_V2_COMPLETE', json.dumps({k: summary[k] for k in ('decision','best_sample_t','best_sample_score','improvement_vs_t1p9')}, sort_keys=True), flush=True)
