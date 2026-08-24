#!/usr/bin/env python3
"""B5: exact linear-growth scale-dependence audit over the BOSS DR12 k window.

This is not a likelihood. It reproduces the production fsigma8_eff definition
(d sigma8 / d ln a on the dense z grid) and compares it with
0.5 d ln P(k,z)/d ln a * sigma8(z) at preregistered k values.
"""
from __future__ import annotations
from bisect import bisect_left
from pathlib import Path
import hashlib, json, math, re, subprocess

ROOT = Path('..')
TARGET_PATH = ROOT / 'research/robustness/B5_BOSS_LINEAR_SCALE_DEPENDENCE_TARGET_v1.json'
t = json.loads(TARGET_PATH.read_text())
assert t['classification'] == 'B5_BOSS_LINEAR_SCALE_DEPENDENCE_TARGET_V1_FROZEN'
assert t['frozen_before_scores'] is True
assert t['production_mapping'] == 'eff'
STATE = json.loads((ROOT / 'research/state/current.json').read_text())
DENSE = STATE['objective']['dense_z_pk']
ULTRA = {k: str(v) for k, v in STATE['objective']['ultra'].items()}
ZS = [float(x) for x in t['redshifts']]
KS = [float(x) for x in t['k_h_Mpc']]
OUT = ROOT / 'output/b5_boss_linear_scale_dependence'
OUT.mkdir(parents=True, exist_ok=True)
SUMMARY = OUT / 'summary.json'


def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def git_head(path):
    try:
        return subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def make_ini(model, p, tag):
    lines = [f"h = {p['h']}", "T_cmb = 2.7255", f"Omega_b = {p['Ob']}"]
    if model == 'RTK':
        lines += [f"Omega_khronon = {p['Om']}", f"lambda_D = {p['lam']}", "Omega_Lambda = 0.", "model = 2."]
    else:
        lines += [f"Omega_cdm = {p['Om']}", "model = 0."]
    lines += [
        "N_ur = 3.046", "N_ncdm = 0", "Omega_k = 0.", "Omega_fld = 0.", "Omega_scf = 0.",
        "recombination = RECFAST", "reio_parametrization = reio_camb", f"z_reio = {p['zre']}",
        "output = mPk", "gauge = newtonian", f"A_s = {p['As']}", f"n_s = {p['ns']}",
        "P_k_max_h/Mpc = 5.0", f"z_pk = {DENSE}", "z_max_pk = 1.0",
        # The worker runs from class_public while OUT intentionally lives in the
        # repository parent. Keep CLASS root and parser OUT on the same path.
        f"root = ../output/b5_boss_linear_scale_dependence/{tag}_", "background_verbose = 0",
        "thermodynamics_verbose = 0", "perturbations_verbose = 0"
    ]
    lines += [f"{k} = {v}" for k, v in ULTRA.items()]
    path = Path(f'b5_{tag}.ini')
    path.write_text('\n'.join(lines) + '\n')
    return path


def pk_load(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        a = s.split()
        rows.append((float(a[0]), float(a[1])))
    if len(rows) < 10:
        raise RuntimeError(f'too few P(k) rows in {path}')
    return rows


def z_from_pk(path):
    for line in Path(path).read_text().splitlines()[:12]:
        m = re.search(r'redshift z=([+\-0-9.eE]+)', line)
        if m:
            return float(m.group(1))
    raise RuntimeError(f'no redshift header in {path}')


def interp_pk(rows, k):
    xs = [r[0] for r in rows]
    j = bisect_left(xs, k)
    if j == 0:
        return rows[0][1]
    if j >= len(rows):
        return rows[-1][1]
    x0, y0 = rows[j - 1]; x1, y1 = rows[j]
    return y0 + (k - x0) * (y1 - y0) / (x1 - x0)


def top_hat(x):
    if abs(x) < 1e-3:
        x2 = x * x
        return 1 - x2 / 10 + x2 * x2 / 280
    return 3 * (math.sin(x) - x * math.cos(x)) / (x * x * x)


def sigma8(rows):
    terms = []
    for k, p in rows:
        W = top_hat(8 * k)
        terms.append((math.log(k), k ** 3 * p * W * W))
    integ = sum(0.5 * (terms[i - 1][1] + terms[i][1]) * (terms[i][0] - terms[i - 1][0]) for i in range(1, len(terms)))
    return math.sqrt(integ / (2 * math.pi ** 2))


def derivative3(x0, y0, x1, y1, x2, y2, xt):
    return (y0 * (2 * xt - x1 - x2) / ((x0 - x1) * (x0 - x2)) +
            y1 * (2 * xt - x0 - x2) / ((x1 - x0) * (x1 - x2)) +
            y2 * (2 * xt - x0 - x1) / ((x2 - x0) * (x2 - x1)))


def qvalue(xs, ys, x):
    val = 0.0
    for i in range(3):
        w = 1.0
        for j in range(3):
            if i != j:
                w *= (x - xs[j]) / (xs[i] - xs[j])
        val += ys[i] * w
    return val


def run_model(model, p, tag):
    ini = make_ini(model, p, tag)
    log = Path(f'b5_{tag}.log')
    with log.open('w') as f:
        cp = subprocess.run(['./class', str(ini)], stdout=f, stderr=subprocess.STDOUT)
    if cp.returncode:
        raise RuntimeError(f'{model} CLASS failed; see {log}')
    fam = {}
    for path in sorted(OUT.glob(f'{tag}_z*_pk.dat')):
        fam[z_from_pk(path)] = pk_load(path)
    if len(fam) < 5:
        raise RuntimeError(f'insufficient dense P(k,z) family for {model}: {sorted(fam)}')
    sig = {z: sigma8(rows) for z, rows in fam.items()}
    by_z = {}
    for z0 in ZS:
        znear = sorted(sorted(fam, key=lambda z: abs(z - z0))[:3])
        xp = [math.log(1 / (1 + z)) for z in znear]
        sp = [sig[z] for z in znear]
        xt = math.log(1 / (1 + z0))
        s8 = qvalue(xp, sp, xt)
        fs8_eff = derivative3(xp[0], sp[0], xp[1], sp[1], xp[2], sp[2], xt)
        krows = []
        for k in KS:
            lp = [(math.log(1 / (1 + z)), math.log(interp_pk(fam[z], k))) for z in znear]
            f_k = 0.5 * derivative3(lp[0][0], lp[0][1], lp[1][0], lp[1][1], lp[2][0], lp[2][1], xt)
            fs8_k = f_k * s8
            rel = fs8_k / fs8_eff - 1.0
            krows.append({'k_h_Mpc': k, 'f_k': f_k, 'fs8_k': fs8_k, 'relative_to_eff': rel})
        rels = [r['relative_to_eff'] for r in krows]
        vals = [r['fs8_k'] for r in krows]
        k01 = min(krows, key=lambda r: abs(r['k_h_Mpc'] - 0.1))
        by_z[str(z0)] = {
            'znear_used': znear,
            'sigma8': s8,
            'fs8_eff': fs8_eff,
            'fs8_k01': k01['fs8_k'],
            'k01_relative_to_eff': k01['relative_to_eff'],
            'max_abs_relative_to_eff': max(abs(x) for x in rels),
            'rms_relative_to_eff': math.sqrt(sum(x * x for x in rels) / len(rels)),
            'peak_to_peak_fs8_over_abs_eff': (max(vals) - min(vals)) / abs(fs8_eff),
            'k_rows': krows
        }
    primary = max(v['max_abs_relative_to_eff'] for v in by_z.values())
    return {'model': model, 'params': p, 'available_pk_redshifts': sorted(fam), 'by_z': by_z, 'primary_max_abs_relative': primary}


def classify(primary, control):
    if control > 0.005:
        return 'B5_LINEAR_SCALE_DEPENDENCE_CONTROL_REVIEW_REQUIRED'
    if primary <= 0.01:
        return 'B5_LINEAR_SCALE_DEPENDENCE_STRICT_SUBPERCENT'
    if primary <= 0.03:
        return 'B5_LINEAR_SCALE_DEPENDENCE_PERCENT_LEVEL_REQUIRES_SURVEY_PROPAGATION'
    return 'B5_LINEAR_SCALE_DEPENDENCE_MATERIAL_GT_3_PERCENT'


def main():
    rtk = run_model('RTK', dict(t['rtk_point']), 'rtk')
    lcdm = run_model('LCDM', dict(t['lcdm_control_point']), 'lcdm')
    classification = classify(rtk['primary_max_abs_relative'], lcdm['primary_max_abs_relative'])
    payload = {
        'schema': 'B5_BOSS_LINEAR_SCALE_DEPENDENCE_RESULT_v1',
        'classification': classification,
        'target_sha256': canonical_hash(t),
        'objective_context': t['objective_context'],
        'production_mapping': 'eff',
        'redshifts': ZS, 'k_h_Mpc': KS,
        'rtk': rtk, 'lcdm_control': lcdm,
        'primary_rtk_max_abs_relative': rtk['primary_max_abs_relative'],
        'lcdm_control_max_abs_relative': lcdm['primary_max_abs_relative'],
        'interpretation_guard': t['guard'],
        'provenance': {
            'research_source_commit': git_head('..'),
            'class_upstream_commit': git_head('.'),
            'target_file': str(TARGET_PATH),
            'production_objective_fingerprint': t['locked_environment']['production_objective_fingerprint']
        }
    }
    SUMMARY.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + '\n')
    print('B5_BOSS_LINEAR_SCALE_DEPENDENCE_COMPLETE', json.dumps({
        'classification': classification,
        'primary_rtk_max_abs_relative': payload['primary_rtk_max_abs_relative'],
        'lcdm_control_max_abs_relative': payload['lcdm_control_max_abs_relative']
    }, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
