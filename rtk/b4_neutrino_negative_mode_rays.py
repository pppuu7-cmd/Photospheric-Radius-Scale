#!/usr/bin/env python3
"""Exact-ray diagnosis of every negative B4 RTK recentered Hessian mode.

Consumes a target frozen before any ray score.  This is a robustness proof
component only; it never mutates the frozen massless A1-A5 state.
"""
from pathlib import Path
import copy,hashlib,json,math,os,subprocess,time

os.environ.setdefault('CLIPY_NOJAX','1')
import inference_core as L

ROOT=Path('..')
TARGET=ROOT/'research/robustness/b4_neutrino_rtk_negative_modes_target_v1.json'
t=json.loads(TARGET.read_text())
assert t['classification']=='B4_NEUTRINO_RTK_NEGATIVE_MODES_TARGET_V1_FROZEN'
assert t['production_mapping']=='eff'
assert t['decision_rule']['no_clipping'] is True
assert len(t['negative_modes'])==3

CENTER=copy.deepcopy(t['center'])
AXES=list(t['axes']); STEPS={k:float(v) for k,v in t['base_steps'].items()}
AMPS=[float(x) for x in t['ray_amplitudes']]
TOL=float(t['recenter_tolerance_S'])
DENSE=json.loads((ROOT/'research/state/current.json').read_text())['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in json.loads((ROOT/'research/state/current.json').read_text())['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
OUT=ROOT/'output/b4_neutrino_negative_modes'; OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl'; FAIL=OUT/'failures.jsonl'; SUMMARY=OUT/'summary.json'


def canonical_hash(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None

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

ORIG=L.make_ini
def make_ini(model,p,tag):
    path=ORIG(model,p,tag); text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text: raise RuntimeError('expected sparse z_pk baseline not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    if 'N_ur = 3.046' not in text or 'N_ncdm = 0' not in text: raise RuntimeError('massless neutrino block not found')
    text=text.replace('N_ur = 3.046','N_ur = 2.0328',1)
    text=text.replace('N_ncdm = 0','N_ncdm = 1\nm_ncdm = 0.06\nT_ncdm = 0.71611\ndeg_ncdm = 1.0',1)
    text+='\n# B4 exact negative-mode ultra overrides\n'+''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text); return path
L.make_ini=make_ini


def params_for(vec,alpha):
    p=copy.deepcopy(CENTER)
    for a,v in zip(AXES,vec):
        d=float(alpha)*float(v)*STEPS[a]
        if a=='loglam': p['lam']=float(CENTER['lam'])*math.exp(d)
        else: p[a]=float(CENTER[a])+d
    p['lam']=float(p['lam'])
    # Fail closed. These rays are small and should remain comfortably physical;
    # never project or clip a point into a permitted region.
    checks={
      'h':(0.2,1.2),'Ob':(1e-6,0.5),'Om':(1e-6,0.9),'As':(1e-12,1e-8),
      'ns':(0.5,1.5),'zre':(0.0,40.0),'lam':(1e-12,1e20)}
    for k,(lo,hi) in checks.items():
        x=float(p[k])
        if not (math.isfinite(x) and lo<x<hi): raise RuntimeError(f'pre-registered ray point OOB {k}={x}')
    return p

CACHE={}
def key(p):return tuple(float(p[k]).hex() for k in ('lam','h','Ob','Om','As','ns','zre'))
def evaluate(p,label,mode,alpha):
    k=key(p)
    if k in CACHE:return CACHE[k]
    last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate('RTK',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'label':label,'mode_index':mode,'alpha':alpha,'attempt':attempt,'params':p,
                 'score_eff':float(r['score']),'score_k01':float(r['score_k01']),
                 'logL_planck':r.get('logL_planck'),'chi2_SN':r.get('chi2_SN'),
                 'chi2_BOSS_eff':r.get('chi2_BOSS_eff'),'chi2_BOSS_k01':r.get('chi2_BOSS_k01'),'rd':r.get('rd')}
            CACHE[k]=row; append(POINTS,row); cleanup(r.get('tag'))
            print('B4_NEGATIVE_MODE_RAY_POINT',json.dumps(row,sort_keys=True,allow_nan=False),flush=True)
            return row
        last=r; append(FAIL,{'label':label,'mode_index':mode,'alpha':alpha,'attempt':attempt,'params':p,'result':r}); cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'{label}: failed after 3 exact retries: {last}')

center=evaluate(CENTER,'center',-1,0.0)
S0=float(center['score_eff'])
mode_results=[]
for m in t['negative_modes']:
    idx=int(m['mode_index']); vec=[float(x) for x in m['eigenvector_y']]
    rows=[]
    for alpha in AMPS:
        p=params_for(vec,alpha)
        rows.append(evaluate(p,f'mode{idx}_alpha_{alpha:+g}',idx,alpha))
    best=min(rows,key=lambda r:r['score_eff'])
    mode_results.append({'mode_index':idx,'parent_eigenvalue_y':float(m['eigenvalue_y']),
                         'best_alpha':float(best['alpha']),'best_exact_S_eff':float(best['score_eff']),
                         'best_improvement_eff':S0-float(best['score_eff']),'best_params':best['params'],
                         'scores':[{'alpha':float(r['alpha']),'S_eff':float(r['score_eff']),'S_k01':float(r['score_k01'])} for r in rows]})
maximp=max(x['best_improvement_eff'] for x in mode_results)
classification='B4_RTK_NEGATIVE_RAY_RECENTER_REQUIRED' if maximp>TOL else 'B4_RTK_NEGATIVE_RAYS_NO_DESCENT_GT_0P005'
summary={'classification':classification,'objective':t['objective'],'production_mapping':'eff','parent_recenter_run_id':t['parent_recenter_run_id'],
         'parent_recenter_artifact_id':t['parent_recenter_artifact_id'],'target_sha256':canonical_hash(t),'center':CENTER,'S_center_eff':S0,
         'recenter_tolerance_S':TOL,'ray_amplitudes':AMPS,'mode_results':mode_results,'max_exact_improvement_eff':maximp,
         'provenance':{'research_source_commit':git_head('..'),'class_upstream_commit':git_head('.'),'target_file':str(TARGET)},
         'next_gate':('freeze and run a B4 RTK recenter base at the best exact ray point' if maximp>TOL else 'preregister a reduced-scale Hessian resolution audit; negative-ray falsification does not itself make the parent base Hessian positive definite'),
         'warning':'Local B4 robustness diagnosis only; not global evidence and not a replacement for A1-A5.'}
SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n')
print('B4_RTK_NEGATIVE_MODE_RAYS_COMPLETE',json.dumps(summary,sort_keys=True,allow_nan=False),flush=True)
