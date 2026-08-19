#!/usr/bin/env python3
"""Audit standalone Planck lensing likelihood availability through clipy.

No cosmological score is evaluated here. The script scans the already pinned
Planck R3.00 baseline tree, requires at least one .clik_lensing directory, and
verifies that clipy-like can instantiate the intended standalone likelihood.
All emitted metadata are recursively normalized to Python-native JSON types so
NumPy scalar metadata from clipy cannot turn a successful interface check into
an infrastructure failure.
"""
from pathlib import Path
import hashlib,json,math,os,sys
os.environ.setdefault('CLIPY_NOJAX','1')
import clipy


def native(x):
    """Recursively convert array/scalar metadata to strict JSON-native types."""
    if isinstance(x,dict):
        return {str(k):native(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):
        return [native(v) for v in x]
    if hasattr(x,'tolist'):
        try:return native(x.tolist())
        except Exception:pass
    if hasattr(x,'item'):
        try:return native(x.item())
        except Exception:pass
    if isinstance(x,(str,int,float,bool)) or x is None:
        if isinstance(x,float) and not math.isfinite(x):
            raise RuntimeError(f'non-finite metadata value {x!r}')
        return x
    return str(x)

root=Path(sys.argv[1] if len(sys.argv)>1 else 'planck_data')
base=root/'baseline'/'plc_3.0'
if not base.is_dir(): raise RuntimeError(f'missing Planck plc_3.0 tree: {base}')

cands=sorted([p for p in base.rglob('*') if p.is_dir() and p.name.endswith('.clik_lensing')])
if not cands: raise RuntimeError('no .clik_lensing directories found in pinned Planck baseline')
rows=[]
for p in cands:
    row={'path':p.relative_to(root).as_posix()}
    try:
        L=clipy.clik(str(p))
        row['load_ok']=True
        row['lmax']=native(L.get_lmax())
        row['default_par_len']=int(len(L.default_par))
        row['default_par_sha256']=hashlib.sha256(memoryview(L.default_par).tobytes()).hexdigest()
    except Exception as exc:
        row['load_ok']=False;row['error']=repr(exc)
    rows.append(native(row))

loaded=[r for r in rows if r.get('load_ok')]
if not loaded: raise RuntimeError('Planck lensing directories exist but none load through clipy-like')
smica=[r for r in loaded if 'smica' in r['path'].lower() and ('pp' in r['path'].lower() or 'lensing' in r['path'].lower())]
if not smica: raise RuntimeError(f'no loadable SMICA standalone lensing product among {loaded}')
# Prefer the non-CMB-marginalized minimum-variance reconstruction as the first
# B9 interface target; the choice is made structurally before any cosmological score.
non_marg=[r for r in smica if 'cmbmarged' not in r['path'].lower()]
if len(non_marg)!=1:
    raise RuntimeError(f'expected exactly one non-CMB-marginalized SMICA lensing product, found {len(non_marg)}')
chosen=non_marg[0]
summary=native({'classification':'PLANCK_R3_STANDALONE_LENSING_CLIPY_INTERFACE_PASS','planck_root':str(root),
         'candidates':rows,'chosen':chosen,'clipy_version':str(getattr(clipy,'__version__','unknown')),
         'next_gate':'freeze B9 matched-lensing robustness protocol before first cosmological lensing score',
         'warning':'Likelihood-interface audit only; no RTK/LCDM lensing score or robustness claim.'})
# allow_nan=False makes the artifact itself a fail-closed JSON contract.
payload=json.dumps(summary,indent=2,sort_keys=True,allow_nan=False)+'\n'
Path('planck_lensing_interface_audit.json').write_text(payload)
print('PLANCK_R3_STANDALONE_LENSING_CLIPY_INTERFACE_PASS',json.dumps(summary,sort_keys=True,allow_nan=False))
