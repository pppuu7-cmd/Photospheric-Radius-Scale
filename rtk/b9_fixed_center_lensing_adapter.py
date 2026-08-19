#!/usr/bin/env python3
"""B9 Step-1 fixed-center Planck-R3 lensing adapter contract.

Evaluates the already-preregistered standalone lensing product at the frozen,
fresh-tree-replayed massless LCDM and RTK centers. This is an adapter and
fixed-center diagnostic only: no B9 reoptimization or model-selection claim.
"""
from __future__ import annotations
from pathlib import Path
import copy,json,math,os,sys
import numpy as np
os.environ.setdefault('CLIPY_NOJAX','1')
sys.argv=['b9_fixed_center_lensing_adapter','planck_data']
import clipy
import inference_core as C

ROOT=Path('..')
STATE=json.loads((ROOT/'research/state/current.json').read_text())
PROTOCOL=(ROOT/'research/robustness/B9_PLANCK_LENSING_ROBUSTNESS_PROTOCOL_v1.md').read_text()
if 'FROZEN BEFORE THE FIRST RTK/LCDM COSMOLOGICAL STANDALONE-LENSING SCORE' not in PROTOCOL:
    raise RuntimeError('B9 protocol not frozen before score')
if STATE['final_replay_certification']!='INDEPENDENT_FRESH_TREE_REPLAY_PASS':
    raise RuntimeError('massless frozen centers lack fresh-tree replay certification')
if STATE['objective']['name']!='matched-ultra-linstep2+dense-BOSS':
    raise RuntimeError('unexpected baseline objective')

PLANCK=Path('planck_data')
LENS_PATH=PLANCK/'baseline/plc_3.0/lensing/smicadx12_Dec5_ftl_mv2_ndclpp_p_teb_consext8.clik_lensing'
if not LENS_PATH.is_dir(): raise RuntimeError(f'missing frozen B9 lensing product: {LENS_PATH}')
LENS=clipy.clik(str(LENS_PATH))
LMAX=[int(x) for x in LENS.get_lmax()]
EXPECTED_LMAX=[2500,2500,2500,-1,2500,-1,-1]
if LMAX!=EXPECTED_LMAX: raise RuntimeError(f'B9 lmax contract changed: {LMAX}')
DEFAULT=np.asarray(LENS.default_par,dtype=float)
if DEFAULT.ndim!=1 or len(DEFAULT)!=10005 or not np.all(np.isfinite(DEFAULT)):
    raise RuntimeError(f'unexpected B9 default vector: shape={DEFAULT.shape}')
CL_LEN=sum(x+1 for x in LMAX if x>=0)
EXTRA_NAMES=[str(x) for x in LENS.get_extra_parameter_names()]
if CL_LEN+len(EXTRA_NAMES)!=len(DEFAULT):
    raise RuntimeError((CL_LEN,EXTRA_NAMES,len(DEFAULT)))
def scalar(x):
    a=np.asarray(x,dtype=float).reshape(-1)
    if a.size<1 or not np.isfinite(a[0]): raise RuntimeError(f'nonfinite likelihood result {a}')
    return float(a[0])
SELF_LOG_L=scalar(LENS(DEFAULT.copy()))

# Preserve the production exact objective precision when generating the spectra.
ORIG=C.make_ini
DENSE=STATE['objective']['dense_z_pk'];ULTRA={k:str(v) for k,v in STATE['objective']['ultra'].items()}
SPARSE='0.,0.25,0.3,0.4,0.5,0.6,0.7,0.75,1.0'
def make_ini(model,p,tag):
    path=ORIG(model,p,tag);text=Path(path).read_text()
    if 'z_pk = '+SPARSE in text:
        text=text.replace('z_pk = '+SPARSE,'z_pk = '+DENSE,1)
    elif 'z_pk = '+DENSE not in text:
        raise RuntimeError('could not establish dense z_pk objective')
    text+='\n# B9 fixed-center adapter: frozen production precision\n'+''.join(f'{k} = {v}\n' for k,v in ULTRA.items())
    Path(path).write_text(text);return path
C.make_ini=make_ini

UK2=(2.7255e6)**2
SPEC_NAMES=['phiphi','TT','EE','BB','TE','TB','EB']
def class_lensed_cls(path):
    path=Path(path);header='\n'.join(path.read_text().splitlines()[:12])
    for token in ('TT','EE','TE','BB','phiphi'):
        if token not in header: raise RuntimeError(f'{token} missing from CLASS lensed header')
    vals={}
    for line in path.read_text().splitlines():
        s=line.strip()
        if not s or s.startswith('#'): continue
        a=s.split();ell=int(float(a[0]))
        if len(a)<6: raise RuntimeError(f'too few CLASS lensed columns at ell {ell}')
        fac=ell*(ell+1)/(2*math.pi)
        if fac<=0: continue
        # Pinned CLASS class-format order is TT EE TE BB phiphi TPhi Ephi and
        # each printed value is D_l=ell(ell+1)C_l/(2pi). CMB C_l are then
        # converted from dimensionless to microK^2, while phiphi stays dimensionless.
        dtt,dee,dte,dbb,dpp=map(float,a[1:6])
        vals[ell]={'phiphi':dpp/fac,'TT':dtt/fac*UK2,'EE':dee/fac*UK2,
                   'BB':dbb/fac*UK2,'TE':dte/fac*UK2,'TB':0.0,'EB':0.0}
    if not vals or max(vals)<max(x for x in LMAX if x>=0):
        raise RuntimeError(f'CLASS lensed spectrum insufficient: max ell={max(vals) if vals else None}')
    return vals

def lens_vector(cls):
    v=DEFAULT.copy();off=0
    for spec,lm in enumerate(LMAX):
        if lm<0: continue
        arr=np.zeros(lm+1,dtype=float);name=SPEC_NAMES[spec]
        for ell in range(2,lm+1):
            arr[ell]=cls[ell][name]
        if not np.all(np.isfinite(arr)): raise RuntimeError(f'nonfinite {name}')
        v[off:off+lm+1]=arr;off+=lm+1
    if off!=CL_LEN: raise RuntimeError((off,CL_LEN))
    if not np.array_equal(v[CL_LEN:],DEFAULT[CL_LEN:]):
        raise RuntimeError('B9 nuisance/default tail changed')
    return v

out={
 'classification':'B9_FIXED_CENTER_LENSING_ADAPTER_CONTRACT_PASS',
 'objective':STATE['objective']['name'],'objective_fingerprint':STATE['objective'].get('fingerprint',STATE.get('objective_fingerprint')),
 'lensing_product':str(LENS_PATH.relative_to(PLANCK)),'lmax':LMAX,'spectrum_order':SPEC_NAMES,
 'default_par_len':len(DEFAULT),'cl_payload_len':CL_LEN,'extra_parameter_names':EXTRA_NAMES,'default_selfcheck_loglike':SELF_LOG_L,
 'models':{},
 'warning':'Fixed-center adapter diagnostic only; no B9 local-minimum, global preference, AIC/BIC, significance or Bayes-factor claim.'
}
for model,key in [('LCDM','lcdm'),('RTK','rtk')]:
    fr=STATE['final_replay_result'][key]
    p=copy.deepcopy(fr['params']);expected=float(fr['expected_score_eff'])
    C.CACHE.clear();r=C.evaluate(model,p)
    if not r.get('ok'): raise RuntimeError(f'baseline evaluation failed for {model}: {r}')
    replay=float(r['score']);err=abs(replay-expected)
    if err>2e-6: raise RuntimeError(f'{model} baseline replay drift {err}: {replay} vs {expected}')
    tag=r['tag'];clpath=C.OUT/f'{tag}_cl_lensed.dat'
    cls=class_lensed_cls(clpath);vec=lens_vector(cls);logl=scalar(LENS(vec))
    out['models'][model]={
      'params':p,'baseline_expected_S_eff':expected,'baseline_replayed_S_eff':replay,'baseline_replay_abs_error':err,
      'lensing_loglike':logl,'lensing_minus2loglike':-2.0*logl,
      'vector_min':float(np.min(vec[:CL_LEN])),'vector_max':float(np.max(vec[:CL_LEN])),
      'nuisance_tail':vec[CL_LEN:].tolist(),'class_lensed_file':str(clpath),
    }
    print('B9_FIXED_CENTER_MODEL',model,json.dumps(out['models'][model],sort_keys=True),flush=True)
Path('../output/b9_fixed_center_lensing').mkdir(parents=True,exist_ok=True)
Path('../output/b9_fixed_center_lensing/summary.json').write_text(json.dumps(out,indent=2,sort_keys=True,allow_nan=False)+'\n')
print('B9_FIXED_CENTER_LENSING_ADAPTER_CONTRACT_PASS',json.dumps(out,sort_keys=True,allow_nan=False),flush=True)
