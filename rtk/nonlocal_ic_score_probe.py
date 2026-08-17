#!/usr/bin/env python3
"""One exact frozen-objective RTK evaluation for nonlocal-IC A/B comparison."""
from pathlib import Path
import json, os, sys

sys.argv=['nonlocal_ic_score_probe','planck_data']
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
CENTER=dict(STATE['rtk']['accepted_center'])
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
orig=L.make_ini

def make_ini(model,p,tag):
    path=orig(model,p,tag)
    text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:
        raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text)
        f.write('\n# exact nonlocal-IC A/B frozen dense objective\n')
        for k,v in ULTRA.items():
            f.write(f'{k} = {v}\n')
    return path
L.make_ini=make_ini
L.CACHE.clear()
r=L.evaluate('RTK',CENTER)
if not r.get('ok'):
    raise SystemExit('RTK_NONLOCAL_IC_SCORE_PROBE_FAIL '+json.dumps(r,sort_keys=True,default=str))
out={
  'label':os.environ.get('RTK_IC_VARIANT','unknown'),
  'objective':STATE['objective']['name'],
  'state_iteration':STATE.get('iteration'),
  'center':CENTER,
  'score_eff':float(r['score']),
  'score_k01':float(r['score_k01']),
  'logL_planck':float(r['logL_planck']),
  'chi2_SN':float(r['chi2_SN']),
  'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),
  'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),
  'rd':float(r['rd']),
}
Path(f"probe_{out['label']}.json").write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('RTK_NONLOCAL_IC_SCORE_PROBE_PASS',json.dumps(out,sort_keys=True))
