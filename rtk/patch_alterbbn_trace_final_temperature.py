#!/usr/bin/env python3
"""Fail-closed trace-only extension of pinned AlterBBN final temperature."""
from pathlib import Path
import hashlib,json,sys
PINNED_BBN_SHA='528b1416876b0fc9d6ddc1d2a0f6ba8cab43796680cef4a7fd92339e974fb708'
OLD='double Tf=0.01*K_to_eV;'
NEW='double Tf=0.009*K_to_eV;'
root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
p=root/'src/bbn.c'
if not p.is_file(): raise RuntimeError(f'missing {p}')
before=hashlib.sha256(p.read_bytes()).hexdigest()
if before!=PINNED_BBN_SHA: raise RuntimeError(f'unexpected pinned bbn.c SHA {before}')
s=p.read_text()
if s.count(OLD)!=1: raise RuntimeError(f'expected exactly one pinned Tf initializer, found {s.count(OLD)}')
if NEW in s: raise RuntimeError('trace-only Tf extension already applied')
s=s.replace(OLD,NEW,1)
p.write_text(s)
after=hashlib.sha256(p.read_bytes()).hexdigest()
out={'classification':'ALTERBBN_TRACE_ONLY_TF_EXTENSION_PASS','pinned_bbn_sha256':before,'patched_bbn_sha256':after,'old_Tf_source':OLD,'new_Tf_source':NEW,'standard_abundance_network_changed':False,'scope':'T-a trace generation only'}
Path('alterbbn_trace_tf_extension_manifest.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_TRACE_ONLY_TF_EXTENSION_PASS',json.dumps(out,sort_keys=True))
