#!/usr/bin/env python3
"""Audit standalone Planck lensing likelihood availability through clipy.

No cosmological score is evaluated here.  The script scans the already pinned
Planck R3.00 baseline tree, requires at least one .clik_lensing directory, and
verifies that clipy-like can instantiate the intended standalone likelihood.
"""
from pathlib import Path
import hashlib,json,os,sys
os.environ.setdefault('CLIPY_NOJAX','1')
import clipy

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
        row['lmax']=list(L.get_lmax())
        row['default_par_len']=len(L.default_par)
        row['default_par_sha256']=hashlib.sha256(memoryview(L.default_par).tobytes()).hexdigest()
    except Exception as exc:
        row['load_ok']=False;row['error']=repr(exc)
    rows.append(row)

loaded=[r for r in rows if r.get('load_ok')]
if not loaded: raise RuntimeError('Planck lensing directories exist but none load through clipy-like')
# Prefer the official SMICA minimum-variance PP product when present; otherwise
# fail closed rather than silently choosing another lensing likelihood.
smica=[r for r in loaded if 'smica' in r['path'].lower() and ('pp' in r['path'].lower() or 'lensing' in r['path'].lower())]
if not smica: raise RuntimeError(f'no loadable SMICA standalone lensing product among {loaded}')
chosen=sorted(smica,key=lambda r:r['path'])[0]
summary={'classification':'PLANCK_R3_STANDALONE_LENSING_CLIPY_INTERFACE_PASS','planck_root':str(root),
         'candidates':rows,'chosen':chosen,'clipy_version':getattr(clipy,'__version__',None),
         'next_gate':'freeze B9 matched-lensing robustness protocol before first cosmological lensing score',
         'warning':'Likelihood-interface audit only; no RTK/LCDM lensing score or robustness claim.'}
Path('planck_lensing_interface_audit.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('PLANCK_R3_STANDALONE_LENSING_CLIPY_INTERFACE_PASS',json.dumps(summary,sort_keys=True))
