#!/usr/bin/env python3
"""Conditional exact quarter-scale B4 recenter-v4 Hessian.

The target is frozen before the v4 half-eigenmode ray result. Execution is
permitted only after a persisted no-descent half-ray classification. The
worker evaluates the full 7D axis/cross stencil plus both mapping-specific
Newton candidates using exact-float likelihood semantics.
"""
from pathlib import Path
import copy, hashlib, json, math, os, subprocess, time
import numpy as np

os.environ.setdefault('CLIPY_NOJAX', '1')
import inference_core as L

ROOT = Path('..')
TARGET_PATH = ROOT / 'research/robustness/B4_NEUTRINO_RTK_RECENTER_V4_QUARTER_STATIONARITY_TARGET_v1.json'
RAY_RESULT_PATH = ROOT / 'research/robustness/B4_NEUTRINO_RTK_RECENTER_V4_HALF_EIGENMODE_RAYS_RESULT_v1.json'
t = json.loads(TARGET_PATH.read_text())
rays = json.loads(RAY_RESULT_PATH.read_text())
assert t['classification'] == 'B4_NEUTRINO_RTK_RECENTER_V4_QUARTER_STATIONARITY_TARGET_V1_FROZEN'
assert t['stencil_scale'] == 0.25
assert rays['classification'] == t['prerequisite']['required_classification']
assert rays['max_exact_improvement_eff'] <= t['prerequisite']['required_max_exact_improvement_lte'] == 0.005
assert rays['center'] == t['center']

CENTER = copy.deepcopy(t['center'])
AXES = list(t['axes'])
STEPS = {k: float(v) for k, v in t['steps'].items()}
TOL = float(t['recenter_tolerance_S'])
REPLAY_TOL = float(t['score_replay_tolerance_abs'])
PD_THR = float(t['positive_definite_threshold'])
state = json.loads((ROOT / 'research/state/current.json').read_text())
DENSE = state['objective']['dense_z_pk']
ULTRA = {k: str(v) for k, v in state['objective']['ultra'].items()}
SPARSE = '0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
N = len(AXES)
OUT = ROOT / 'output/b4_neutrino_recenter_v4_quarter_stationarity'
OUT.mkdir(parents=True, exist_ok=True)
POINTS = OUT / 'points.jsonl'
FAIL = OUT / 'failures.jsonl'
SUMMARY = OUT / 'summary.json'


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def git_head(path):
    try:
        return subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


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


ORIG = L.make_ini
def make_ini(model, p, tag):
    path = ORIG(model, p, tag)
    text = Path(path).read_text()
    if 'z_pk = ' + SPARSE not in text:
        raise RuntimeError('expected sparse z_pk baseline not found')
    text = text.replace('z_pk = ' + SPARSE, 'z_pk = ' + DENSE, 1)
    if 'N_ur = 3.046' not in text or 'N_ncdm = 0' not in text:
        raise RuntimeError('massless neutrino block not found')
    text = text.replace('N_ur = 3.046', 'N_ur = 2.0328', 1)
    text = text.replace('N_ncdm = 0', 'N_ncdm = 1\nm_ncdm = 0.06\nT_ncdm = 0.71611\ndeg_ncdm = 1.0', 1)
    text += '\n# B4 recenter-v4 quarter ultra overrides\n' + ''.join(f'{k} = {v}\n' for k, v in ULTRA.items())
    Path(path).write_text(text)
    return path
L.make_ini = make_ini


E = {}
def key(y): return tuple(float(x).hex() for x in np.asarray(y, float))

def pars(y):
    p = copy.deepcopy(CENTER)
    for yi, axis in zip(np.asarray(y, float), AXES):
        if axis == 'loglam':
            p['lam'] = float(CENTER['lam']) * math.exp(float(yi) * STEPS[axis])
        else:
            p[axis] = float(CENTER[axis]) + float(yi) * STEPS[axis]
    return p


def ev(y, label):
    y = np.asarray(y, float)
    k = key(y)
    if k in E:
        return E[k]
    p = pars(y)
    last = None
    for attempt in range(1, 4):
        L.CACHE.clear()
        try: r = L.evaluate('RTK', p)
        except Exception as exc: r = {'ok': False, 'exception': repr(exc)}
        if r.get('ok'):
            row = {
                'label': label, 'attempt': attempt, 'y': y.tolist(), 'params': p,
                'score_eff': float(r['score']), 'score_k01': float(r['score_k01']),
                'logL_planck': r.get('logL_planck'), 'chi2_SN': r.get('chi2_SN'),
                'chi2_BOSS_eff': r.get('chi2_BOSS_eff'), 'chi2_BOSS_k01': r.get('chi2_BOSS_k01'), 'rd': r.get('rd')
            }
            E[k] = row
            append(POINTS, row)
            cleanup(r.get('tag'))
            print('B4_RECENTER_V4_QUARTER_POINT', json.dumps(row, sort_keys=True, allow_nan=False), flush=True)
            return row
        last = r
        append(FAIL, {'label': label, 'attempt': attempt, 'y': y.tolist(), 'params': p, 'result': r})
        cleanup(r.get('tag') if isinstance(r, dict) else None)
        if attempt < 3: time.sleep(2 * attempt)
    raise RuntimeError(f'{label}: failed after 3 exact retries: {last}')


z = np.zeros(N)
center = ev(z, 'center')
if abs(float(center['score_eff']) - float(t['expected_center_score_eff'])) > REPLAY_TOL:
    raise RuntimeError('quarter center replay mismatch')
for i in range(N):
    for s in (-1.0, 1.0):
        y = np.zeros(N); y[i] = s; ev(y, f'axis_{i}_{int(s):+d}')
for i in range(N):
    for j in range(i + 1, N):
        for a in (-1.0, 1.0):
            for b in (-1.0, 1.0):
                y = np.zeros(N); y[i] = a; y[j] = b
                ev(y, f'cross_{i}_{j}_{int(a):+d}_{int(b):+d}')


def build(which):
    fld = 'score_eff' if which == 'eff' else 'score_k01'
    S0 = float(E[key(np.zeros(N))][fld])
    g = np.zeros(N); H = np.zeros((N, N))
    for i in range(N):
        yp = np.zeros(N); ym = np.zeros(N); yp[i] = 1; ym[i] = -1
        sp = float(E[key(yp)][fld]); sm = float(E[key(ym)][fld])
        g[i] = (sp - sm) / 2.0; H[i, i] = sp - 2.0 * S0 + sm
    for i in range(N):
        for j in range(i + 1, N):
            vv = []
            for a, b in ((1,1),(1,-1),(-1,1),(-1,-1)):
                y = np.zeros(N); y[i] = a; y[j] = b; vv.append(float(E[key(y)][fld]))
            H[i, j] = H[j, i] = (vv[0] - vv[1] - vv[2] + vv[3]) / 4.0
    vals, vecs = np.linalg.eigh(H)
    for j in range(vecs.shape[1]):
        q = int(np.argmax(np.abs(vecs[:, j])))
        if vecs[q, j] < 0: vecs[:, j] *= -1
    delta = -np.linalg.pinv(H, rcond=1e-10) @ g
    rn = ev(np.clip(delta, -1.0, 1.0), f'newton_trust_{which}')
    return {
        'S_center': S0, 'gradient_y': g.tolist(), 'hessian_y': H.tolist(),
        'eigenvalues_y': vals.tolist(), 'eigenvectors_y': vecs.T.tolist(),
        'positive_definite': bool(np.all(vals > PD_THR)),
        'newton_delta': delta.tolist(), 'S_newton': float(rn[fld]), 'newton_params': rn['params']
    }


def finalize(block, which):
    fld = 'score_eff' if which == 'eff' else 'score_k01'
    best = min(E.values(), key=lambda r: float(r[fld]))
    block.update({
        'best_exact_S': float(best[fld]),
        'best_improvement': float(block['S_center'] - float(best[fld])),
        'best_label': best['label'], 'best_params': best['params']
    })
    return block

EFF = build('eff'); K01 = build('k01')
EFF = finalize(EFF, 'eff'); K01 = finalize(K01, 'k01')
if EFF['best_improvement'] > TOL:
    decision = 'RECENTER_REQUIRED'
elif not EFF['positive_definite']:
    decision = 'RECENTER_CLEAR_NONPD_QUARTER_EIGENMODE_RAYS_REQUIRED'
else:
    decision = 'RECENTER_CLEAR_PD_FRESH_TREE_REQUIRED'
summary = {
    'classification': 'B4_NEUTRINO_RTK_RECENTER_V4_QUARTER_STATIONARITY_COMPLETE',
    'objective': t['objective'], 'production_mapping': 'eff', 'stencil_scale': 0.25,
    'center': CENTER, 'target_sha256': canonical_hash(t), 'points': len(E),
    'recenter_tolerance_S': TOL, 'eff': EFF, 'k01': K01, 'decision': decision,
    'center_replay_abs_error': abs(float(center['score_eff']) - float(t['expected_center_score_eff'])),
    'provenance': {'research_source_commit': git_head('..'), 'class_upstream_commit': git_head('.'), 'target_file': str(TARGET_PATH)},
    'guard': 'B4 minimal-neutrino local stationarity only; not global evidence and not comparable in absolute score to massless A5.'
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + '\n')
print('B4_RECENTER_V4_QUARTER_STATIONARITY_COMPLETE', json.dumps(summary, sort_keys=True, allow_nan=False), flush=True)
