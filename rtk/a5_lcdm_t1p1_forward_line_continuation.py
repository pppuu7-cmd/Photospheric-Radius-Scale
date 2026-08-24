#!/usr/bin/env python3
from pathlib import Path
import json, math, os, subprocess, time
os.environ.setdefault('CLIPY_NOJAX','1')
import inference_core as L

ROOT=Path('..')
t=json.loads((ROOT/'research/robustness/A5_LCDM_T1P1_FORWARD_LINE_CONTINUATION_TARGET_v1.json').read_text())
s=json.loads((ROOT/'research/state/current.json').read_text())
assert t['classification']=='A5_LCDM_T1P1_FORWARD_LINE_CONTINUATION_TARGET_V1_FROZEN'
assert t['objective']==s['objective']['name']
OLD=t['historical_center']; NEW=t['t1_seed']; GRID=[float(x) for x in t['t_grid']]
DENSE=s['objective']['dense_z_pk']; ULTRA={k:str(v) for k,v in s['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
OUT=ROOT/'output/a5_lcdm_t1p1_forward_line'; OUT.mkdir(parents=True,exist_ok=True)
PTS=OUT/'points.jsonl'; FAIL=OUT/'failures.jsonl'; SUMMARY=OUT/'summary.json'

ORIG=L.make_ini
def make_ini(model,p,tag):
    path=ORIG(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE in text:text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    elif 'z_pk = '+DENSE not in text:raise RuntimeError('dense objective not established')
    text+='\n# A5 t1p1 forward continuation\n'+''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text); return path
L.make_ini=make_ini

def append(path,row):
    with path.open('a') as f:f.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n');f.flush()
def cleanup(tag):
    if not tag:return
    for q in L.OUT.glob(tag+'_*'):
        try:q.unlink()
        except OSError:pass
    for q in (Path(f'profile_{tag}.ini'),Path(f'profile_{tag}.log')):
        try:q.unlink()
        except OSError:pass

def params_at(x):
    return {k:(0.0 if k=='lam' else float(OLD[k])+x*(float(NEW[k])-float(OLD[k]))) for k in OLD}
def evaluate(x):
    p=params_at(x); last=None
    for attempt in (1,2,3):
        L.CACHE.clear()
        try:r=L.evaluate('LCDM',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'t':x,'attempt':attempt,'params':p,'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
                 'logL_planck':r.get('logL_planck'),'chi2_SN':r.get('chi2_SN'),'chi2_BOSS_eff':r.get('chi2_BOSS_eff'),'rd':r.get('rd')}
            if not math.isfinite(row['score_eff']):raise RuntimeError('nonfinite score')
            append(PTS,row);cleanup(r.get('tag'));print('A5_T1P1_FORWARD_POINT',json.dumps(row,sort_keys=True),flush=True);return row
        last=r;append(FAIL,{'t':x,'attempt':attempt,'params':p,'result':r});cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'failed t={x}: {last}')

rows=[evaluate(x) for x in GRID]
by={round(r['t'],12):r for r in rows}
ref=by[1.1]; known=float(t['t1p1_center']['expected_score_eff'])
err=abs(ref['score_eff']-known)
if err>float(t['replay_tolerance_abs']):raise RuntimeError(f't1p1 replay mismatch {err}')
best=min(rows,key=lambda r:r['score_eff']); improvement=ref['score_eff']-best['score_eff']
upper=max(GRID)
if improvement>0.005 and abs(best['t']-upper)<1e-12:decision='EXTEND_FORWARD_FROM_BOUNDARY'
elif improvement>0.005:decision='RECENTER_AT_BEST_SAMPLED_POINT'
else:decision='T1P1_FORWARD_CLEAR_STATIONARITY_REQUIRED'
summary={'schema':'A5_LCDM_T1P1_FORWARD_LINE_CONTINUATION_RESULT_v1','status':'PASS','classification':'A5_LCDM_T1P1_FORWARD_LINE_CONTINUATION_COMPLETE',
         'objective':t['objective'],'production_mapping':'eff','t1p1_replay_abs_error':err,'S_t1p1':ref['score_eff'],
         'best_sample_t':best['t'],'best_sample_score':best['score_eff'],'improvement_vs_t1p1':improvement,'best_params':best['params'],
         'decision':decision,'rows':rows,'recenter_tolerance_S':0.005,
         'research_source_commit':subprocess.check_output(['git','-C','..','rev-parse','HEAD'],text=True).strip(),
         'warning':t['guard']}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n')
print('A5_LCDM_T1P1_FORWARD_LINE_CONTINUATION_COMPLETE',json.dumps({k:summary[k] for k in ('decision','best_sample_t','best_sample_score','improvement_vs_t1p1')},sort_keys=True),flush=True)
