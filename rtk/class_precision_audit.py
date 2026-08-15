#!/usr/bin/env python3
"""Fixed-point CLASS precision convergence audit for the RTK exact likelihood.

The production likelihood implementation is imported from generated
``inference_core.py``.  This script changes only documented CLASS precision
parameters while holding cosmological parameters, likelihood data, BOSS z-grid,
and P_k_max fixed.  It is a numerical-systematics audit, not an optimizer or a
statistical significance calculation.
"""
from pathlib import Path
import json
import inference_core as core

P={
    'lam':500000.0,
    'h':0.6906735558373721,
    'Ob':0.04682420076998405,
    'Om':0.2528151585356755,
    'As':2.0696362950837475e-9,
    'ns':0.9643741898228925,
    'zre':6.860220172374236,
}

LEVELS=[
    ('baseline',{}),
    ('medium',{
        'tol_background_integration':'3e-3',
        'tol_thermo_integration':'3e-3',
        'tol_perturb_integration':'3e-6',
        'perturb_sampling_stepsize':'0.05',
        'k_per_decade_for_pk':'20',
        'k_per_decade_for_bao':'100',
        'k_max_tau0_over_l_max':'3.0',
        'l_logstep':'1.08',
        'l_linstep':'20',
    }),
    ('tight',{
        'tol_background_integration':'1e-3',
        'tol_thermo_integration':'1e-3',
        'tol_perturb_integration':'1e-6',
        'perturb_sampling_stepsize':'0.025',
        'k_per_decade_for_pk':'30',
        'k_per_decade_for_bao':'140',
        'k_max_tau0_over_l_max':'3.5',
        'l_logstep':'1.04',
        'l_linstep':'10',
    }),
]

orig_make_ini=core.make_ini
_active={}

def audited_make_ini(model,p,tag):
    path=orig_make_ini(model,p,tag)
    if _active:
        with Path(path).open('a') as f:
            f.write('\n# CLASS precision audit overrides\n')
            for k,v in _active.items():
                f.write(f'{k} = {v}\n')
    return path

core.make_ini=audited_make_ini
rows=[]
for label,overrides in LEVELS:
    _active.clear(); _active.update(overrides)
    core.CACHE.clear()
    r=core.evaluate('RTK',dict(P))
    if not r.get('ok',False):
        raise RuntimeError(f'CLASS/likelihood failed at precision level {label}: {r}')
    row={
        'level':label,
        'overrides':dict(overrides),
        'score_eff':r['score'],
        'score_k01':r['score_k01'],
        'rd':r['rd'],
        'logL_lowT':r['logL_lowT'],
        'logL_lowE':r['logL_lowE'],
        'logL_high':r['logL_high'],
        'logL_planck':r['logL_planck'],
        'chi2_SN':r['chi2_SN'],
        'chi2_BOSS_eff':r['chi2_BOSS_eff'],
        'chi2_BOSS_k01':r['chi2_BOSS_k01'],
    }
    rows.append(row)
    print('CLASS_PRECISION_POINT',json.dumps(row,sort_keys=True),flush=True)

base=rows[0]
for r in rows:
    for key in ['score_eff','score_k01','rd','logL_lowT','logL_lowE','logL_high','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01']:
        r['delta_'+key+'_vs_baseline']=r[key]-base[key]

tight=rows[-1]
medium=rows[-2]
summary={
    'stage':'CLASS-fixed-point-precision-convergence',
    'params':P,
    'levels':rows,
    'baseline_expected':{
        'score_eff':1050.598394220793,
        'score_k01':1050.6111993119548,
        'rd':146.973975,
    },
    'tight_vs_baseline':{k:tight[k]-base[k] for k in ['score_eff','score_k01','rd','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01']},
    'tight_vs_medium':{k:tight[k]-medium[k] for k in ['score_eff','score_k01','rd','logL_planck','chi2_SN','chi2_BOSS_eff','chi2_BOSS_k01']},
    'scope':'Numerical CLASS precision at one fixed RTK point; legacy production BOSS z-grid retained intentionally.',
}
# Baseline must reproduce the archived exact point before convergence deltas mean anything.
for k,v in summary['baseline_expected'].items():
    if abs(base[k]-v)>1e-9:
        raise RuntimeError(f'production baseline regression failed for {k}: got {base[k]}, expected {v}')

out=Path('output/class_precision_audit')
out.mkdir(parents=True,exist_ok=True)
(out/'class_precision_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('CLASS_PRECISION_RESULT',json.dumps(summary,sort_keys=True),flush=True)
print('CLASS_PRECISION_AUDIT_COMPLETE',flush=True)
