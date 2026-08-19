#!/usr/bin/env python3
"""Exact frozen-objective B10 fixed-shared lambda_D tail reconnaissance."""
from pathlib import Path
import json,math,sys,time,hashlib,subprocess

sys.argv=['lambda_tail_reconnaissance','planck_data']
import inference_core as L

ROOT=Path('..');STATE=json.loads((ROOT/'research/state/current.json').read_text())
CENTER=dict(STATE['rtk']['accepted_score_params'])
OBJ=STATE['objective']['name'];DENSE=STATE['objective']['dense_z_pk'];ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
FACTORS=(1/256,1/64,1/16,1/4,1,4,16,64,256,1024,4096,16384)
LAMSTAR=float(CENTER['lam'])
OUT=Path('output/b10_lambda_tail_recon');OUT.mkdir(parents=True,exist_ok=True)
ORIG=L.make_ini

def make_ini(model,p,tag):
    path=ORIG(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('sparse z_pk baseline missing')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    text+='\n# B10 exact lambda-tail frozen-objective reconnaissance\n'
    text+=''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text);return path
L.make_ini=make_ini

def cleanup(tag):
    if not tag:return
    for p in L.OUT.glob(tag+'_*'):
        try:p.unlink()
        except OSError:pass
    for p in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:p.unlink()
        except OSError:pass

def ev(factor):
    p=dict(CENTER);p['lam']=LAMSTAR*float(factor);last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate('RTK',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'factor':float(factor),'lambda_D':p['lam'],'attempt':attempt,'params':p,
                 'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
                 'logL_planck':float(r['logL_planck']),'chi2_SN':float(r['chi2_SN']),
                 'chi2_BOSS_eff':float(r['chi2_BOSS_eff']),'chi2_BOSS_k01':float(r['chi2_BOSS_k01']),'rd':float(r['rd'])}
            cleanup(r.get('tag'));return row
        last=r;cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    return {'factor':float(factor),'lambda_D':p['lam'],'failed':True,'last_result':last}

rows=[]
for f in FACTORS:
    row=ev(f);rows.append(row);print('B10_LAMBDA_TAIL_POINT',json.dumps(row,sort_keys=True,default=str),flush=True)

successful=[r for r in rows if not r.get('failed')]
if len(successful)<8:raise RuntimeError(f'too few successful preregistered tail points: {len(successful)}')
# Mechanically determine the T2 asymptotic onset exactly as preregistered.
large=[r for r in successful if r['factor']>=64]
last=max(large,key=lambda r:r['factor']) if large else None
onset=None
if last:
    for r in sorted(large,key=lambda x:x['factor']):
        tail=[q for q in large if q['factor']>=r['factor']]
        if all(abs(q['score_eff']-last['score_eff'])<=0.002 for q in tail):
            onset=r['factor'];break

def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None
summary={'classification':'B10_LAMBDA_TAIL_RECONNAISSANCE_COMPLETE','objective':OBJ,'production_mapping':'eff',
         'accepted_score_params':CENTER,'lambda_star':LAMSTAR,'factors':[float(x) for x in FACTORS],'rows':rows,
         'successful_points':len(successful),'asymptotic_onset_factor_by_protocol':onset,
         'largest_successful_factor':max(r['factor'] for r in successful),
         'largest_successful_score_eff':max(successful,key=lambda r:r['factor'])['score_eff'],
         'finite_f1_score_eff':next(r['score_eff'] for r in successful if r['factor']==1.0),
         'provenance':{'rtk_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon')},
         'next_gate':('freeze T2 fixed-lambda 6D profile targets using preregistered onset' if onset is not None else 'preregister farther tail extension'),
         'warning':'Fixed-shared reconnaissance only; cannot establish profiled lambda identifiability or a global minimum.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('B10_LAMBDA_TAIL_RECONNAISSANCE_COMPLETE',json.dumps(summary,sort_keys=True),flush=True)
