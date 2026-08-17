#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/'research/state/current.json').read_text())
runner=(ROOT/'rtk/joint_profile_runner.py').read_text()
prep=(ROOT/'rtk/prepare_inference_core.py').read_text()
protocol=(ROOT/'rtk/FINAL_MATCHED_COMPARISON_PROTOCOL.md').read_text()
inputs=(ROOT/'rtk/upgrade_rtk_inputs.py').read_text()

checks=[]
def ok(name, cond, detail=''):
    if not cond:
        raise SystemExit(f'AUDIT_INVARIANT_FAIL {name}: {detail}')
    checks.append(name)

ok('production_gauge_newtonian', '"gauge = newtonian"' in runner,
   'production likelihood must not enter the unsupported Khronon synchronous dynamics branch')
ok('exact_float_cache_preparation', "tuple(float(p[k]) for k in ['lam','h','Ob','Om','As','ns','zre'])" in prep and 'round(float(p[k]),12)' in prep,
   'preparation script must explicitly replace legacy rounded cache keys with exact-float keys')
ok('production_mapping_eff', state.get('production_mapping')=='eff')
ok('matched_dense_objective', state.get('objective',{}).get('name')=='matched-ultra-linstep2+dense-BOSS')
ok('lambda_is_real_input', 'class_read_double("lambda_D",pba->lambda_D)' in inputs)
ok('mapping_separation_protocol', 'eff` and `k01`' in protocol and 'treated as separate objective variants' in protocol)

tol=float(state['objective']['recenter_tolerance_S'])
for model in ('lcdm','rtk'):
    m=state.get(model,{})
    if m.get('certification')!='local_dense_accepted':
        continue
    result=m.get('hessian_result') or {}
    if model=='rtk':
        result=result.get('eff',{})
    imp=float(result.get('best_improvement',1e99))
    best=result.get('best_exact_S')
    accepted=m.get('accepted_score_eff')
    if imp<=tol and best is not None and accepted is not None:
        ok(f'{model}_freeze_uses_best_exact', abs(float(accepted)-float(best))<=1e-12,
           f'accepted={accepted} best_exact={best} improvement={imp}')

print('RTK_AUDIT_INVARIANTS_PASS', json.dumps(checks, sort_keys=True))
