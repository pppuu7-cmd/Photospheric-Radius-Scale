#!/usr/bin/env python3
"""Exact frozen-objective profiles along negative RTK Hessian eigenmodes.

The worker is source-scale aware.  By default it profiles the parsed base
(scale=1) Hessian, preserving the historical Stage-4D3 behavior.  Dedicated
manual-only workflows may set ``RTK_EIGENRAY_SOURCE=half`` or ``quarter`` to
falsify a smaller non-PD Hessian before descending further in the pre-registered
adjacent-scale proof ladder.
"""
from pathlib import Path
import hashlib, json, math, os, subprocess, sys, time
import numpy as np

sys.argv=['autonomous_negative_eigenray_gate','planck_data']
import inference_core as L

STATE=json.loads(Path('../research/state/current.json').read_text())
RTK=STATE['rtk']
CENTER=dict(RTK['accepted_center'])
TOL=float(STATE['objective']['recenter_tolerance_S'])
SOURCE=os.environ.get('RTK_EIGENRAY_SOURCE','base').strip().lower()
SOURCE_CFG={
    'base':('hessian_result','hessian_run',1.0),
    'half':('half_hessian_result','half_hessian_run',0.5),
    'quarter':('quarter_hessian_result','quarter_hessian_run',0.25),
}
if SOURCE not in SOURCE_CFG:
    raise RuntimeError(f'unsupported RTK_EIGENRAY_SOURCE={SOURCE!r}')
RESULT_KEY,RUN_KEY,SOURCE_SCALE=SOURCE_CFG[SOURCE]
SOURCE_RESULT=RTK.get(RESULT_KEY) or {}
EFF=SOURCE_RESULT.get('eff') or {}
SOURCE_RUN=RTK.get(RUN_KEY) or {}
if not SOURCE_RUN.get('parsed'):
    raise RuntimeError(f'{SOURCE} RTK Hessian is not parsed')
if SOURCE_RESULT.get('objective')!=STATE['objective']['name']:
    raise RuntimeError(f'{SOURCE} Hessian objective mismatch')
if SOURCE_RESULT.get('center')!=CENTER:
    raise RuntimeError(f'{SOURCE} Hessian center is not current accepted center')
actual_scale=float(SOURCE_RESULT.get('stencil_scale',1.0 if SOURCE=='base' else -1.0))
if abs(actual_scale-SOURCE_SCALE)>1e-15:
    raise RuntimeError(f'{SOURCE} Hessian stencil_scale={actual_scale!r} expected={SOURCE_SCALE!r}')
if float(EFF.get('best_improvement',1e99))>TOL:
    raise RuntimeError(f'{SOURCE} Hessian is not recenter-clear; eigenray gate is premature')
if bool(EFF.get('positive_definite')):
    raise RuntimeError(f'{SOURCE} Hessian is already positive definite; negative-eigenray gate is unnecessary')

H=np.asarray(EFF['hessian_y'],float)
if H.shape!=(7,7) or not np.all(np.isfinite(H)):
    raise RuntimeError('invalid 7D RTK Hessian')
vals,vecs=np.linalg.eigh(H)
for j in range(vecs.shape[1]):
    i=int(np.argmax(np.abs(vecs[:,j])))
    if vecs[i,j]<0: vecs[:,j]*=-1
NEG=[j for j,v in enumerate(vals) if float(v)<0.0]

bs=RTK['base_steps']
BASE=[('loglam',float(bs['loglam'])*SOURCE_SCALE),('h',float(bs['h'])*SOURCE_SCALE),('Ob',float(bs['Ob'])*SOURCE_SCALE),('Om',float(bs['Om'])*SOURCE_SCALE),('As',float(bs['As'])*SOURCE_SCALE),('ns',float(bs['ns'])*SOURCE_SCALE),('zre',float(bs['zre'])*SOURCE_SCALE)]
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
DENSE=STATE['objective']['dense_z_pk']
ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
ORIG=L.make_ini
OUT=Path('output/autonomous_negative_eigenray_gate');OUT.mkdir(parents=True,exist_ok=True)
POINTS=OUT/'points.jsonl';FAILURES=OUT/'failures.jsonl'

def canonical_hash(obj):
    raw=json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()
CENTER_FP=canonical_hash({'model':'RTK','center':CENTER,'objective':STATE['objective']['name'],'mapping':STATE.get('production_mapping','eff')})
OBJECTIVE_FP=canonical_hash(STATE['objective'])

def git_head(path):
    try:return subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
    except Exception:return None
PROV={'state_iteration':STATE.get('iteration'),'center_fingerprint':CENTER_FP,'objective_fingerprint':OBJECTIVE_FP,
      'eigenray_source':SOURCE,'source_stencil_scale':SOURCE_SCALE,'source_hessian_run_id':SOURCE_RUN.get('run_id'),
      'base_hessian_run_id':(RTK.get('hessian_run') or {}).get('run_id'),'rtk_source_commit':git_head('..'),
      'class_upstream_commit':git_head('.'),'pantheon_commit':git_head('pantheon'),'numpy_version':np.__version__}
(OUT/'provenance.json').write_text(json.dumps(PROV,indent=2,sort_keys=True)+'\n')

def make_ini(model,p,tag):
    path=ORIG(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE not in text:raise RuntimeError('production sparse z_pk line not found')
    text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    with Path(path).open('w') as f:
        f.write(text);f.write(f'\n# exact automatic negative-Hessian-eigenmode ray gate source={SOURCE} scale={SOURCE_SCALE}\n')
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

def pars(y):
    y=np.asarray(y,float);p=dict(CENTER)
    p['lam']=CENTER['lam']*math.exp(float(y[0])*BASE[0][1])
    for yi,(name,step) in zip(y[1:],BASE[1:]):p[name]=CENTER[name]+float(yi)*step
    return p

def append(path,row):
    with path.open('a') as f:f.write(json.dumps(row,sort_keys=True,default=str)+'\n');f.flush()

def ev(y,label,mode_index,t):
    y=np.asarray(y,float);p=pars(y);last=None
    for attempt in range(1,4):
        L.CACHE.clear()
        try:r=L.evaluate('RTK',p)
        except Exception as exc:r={'ok':False,'exception':repr(exc)}
        if r.get('ok'):
            row={'label':label,'mode_index':mode_index,'t':float(t),'attempt':attempt,'y':y.tolist(),'params':p,
                 'source_stencil_scale':SOURCE_SCALE,'score_eff':float(r['score']),'score_k01':float(r['score_k01'])}
            cleanup(r.get('tag'));append(POINTS,row)
            print('RTK_NEGATIVE_EIGENRAY_POINT',json.dumps(row,sort_keys=True),flush=True)
            return row
        last=r;failure={'label':label,'mode_index':mode_index,'t':float(t),'attempt':attempt,'y':y.tolist(),'params':p,'source_stencil_scale':SOURCE_SCALE,'result':r}
        append(FAILURES,failure);cleanup(r.get('tag') if isinstance(r,dict) else None)
        if attempt<3:time.sleep(2*attempt)
    raise RuntimeError(f'{label}: failed after 3 exact retries: {last}')

T=(-2.0,-1.5,-1.0,-0.5,-0.25,0.0,0.25,0.5,1.0,1.5,2.0)
center_row=None;modes=[];all_rows=[]
if NEG:
    center_row=ev(np.zeros(7),'center',-1,0.0);all_rows.append(center_row)
    for j in NEG:
        v=vecs[:,j];rows=[]
        for t in T:
            if t==0.0:
                r=dict(center_row);r['mode_index']=int(j);r['label']=f'mode_{j}_center';r['t']=0.0
            else:
                r=ev(float(t)*v,f'mode_{j}_t_{t:+.2f}',int(j),float(t));all_rows.append(r)
            rows.append(r)
        S0=center_row['score_eff'];best=min(rows,key=lambda r:r['score_eff']);sym=[];by={r['t']:r for r in rows}
        for t in (0.25,0.5,1.0,1.5,2.0):
            sp=by[t]['score_eff'];sm=by[-t]['score_eff']
            sym.append({'abs_t':t,'symmetric_curvature_eff':(sp-2*S0+sm)/(t*t),'symmetric_gradient_eff':(sp-sm)/(2*t)})
        modes.append({'mode_index':int(j),'source_eigenvalue':float(vals[j]),'base_eigenvalue':float(vals[j]) if SOURCE=='base' else None,
                      'eigenvector':v.tolist(),'best_exact_S':float(best['score_eff']),'best_improvement':float(S0-best['score_eff']),
                      'best_t':float(best['t']),'best_params':best['params'],'symmetric_scale_diagnostics':sym,'points':rows})

if modes:
    best_mode=max(modes,key=lambda m:m['best_improvement']);global_best_improvement=float(best_mode['best_improvement']);global_best_params=best_mode['best_params'];global_best_S=float(best_mode['best_exact_S'])
else:
    best_mode=None;global_best_improvement=0.0;global_best_params=dict(CENTER);global_best_S=float(EFF['S_center'])

summary={'classification':'RTK_AUTONOMOUS_NEGATIVE_EIGENRAY_GATE_COMPLETE','objective':STATE['objective']['name'],
         'center':CENTER,'center_fingerprint':CENTER_FP,'objective_fingerprint':OBJECTIVE_FP,'provenance':PROV,
         'eigenray_source':SOURCE,'source_stencil_scale':SOURCE_SCALE,'source_hessian_run_id':SOURCE_RUN.get('run_id'),
         'base_hessian_run_id':(RTK.get('hessian_run') or {}).get('run_id'),'source_eigenvalues':vals.tolist(),
         'base_eigenvalues':vals.tolist() if SOURCE=='base' else None,'negative_mode_indices':[int(j) for j in NEG],
         'negative_mode_count':len(NEG),'modes':modes,'best_exact_S':global_best_S,'best_improvement':global_best_improvement,
         'best_params':global_best_params,'recenter_tolerance_S':TOL,'ray_recenter_required':bool(global_best_improvement>TOL),
         'warning':f'Exact frozen-objective diagnostic along strictly negative {SOURCE}-Hessian eigendirections at physical stencil scale {SOURCE_SCALE}; not a global-minimum or model-selection claim.'}
(OUT/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('RTK_AUTONOMOUS_NEGATIVE_EIGENRAY_GATE_COMPLETE',json.dumps(summary,sort_keys=True),flush=True)
