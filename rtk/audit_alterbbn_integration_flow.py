#!/usr/bin/env python3
"""Audit pinned AlterBBN v2.2 integration flow for accepted-state tracing.

Structural only: no source modification.  Emits call/order/context around
stand_cosmo network calls and the BBN integrator/update loop so a diagnostic
trace can be moved from RHS trial evaluations to accepted integration states.
"""
from pathlib import Path
import json,re,sys,hashlib
root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
if not root.is_dir(): raise SystemExit(f'missing tree {root}')

candidates=[]
for name in ('stand_cosmo.c','src/bbn.c','src/general.c','src/include.h'):
    p=root/name
    if p.exists(): candidates.append(p)
if not candidates: raise RuntimeError('expected AlterBBN source files missing')

patterns={
 'network_call':re.compile(r'\bnucl(?:_err)?\s*\('),
 'fill_params_call':re.compile(r'\bfill_params\s*\('),
 'integration_loop':re.compile(r'\bwhile\s*\(|\bfor\s*\('),
 'dt_update':re.compile(r'\bdt\b|dT_dt|da_dt'),
 'state_update':re.compile(r'\bT\s*[+\-*/]?=|\ba\s*[+\-*/]?='),
 'linearize':re.compile(r'linearize|Runge|evolver|rkck|RK',re.I),
 'failsafe':re.compile(r'failsafe',re.I),
}
rows=[]
for p in candidates:
    lines=p.read_text(errors='replace').splitlines()
    for i,line in enumerate(lines,1):
        kinds=[k for k,pat in patterns.items() if pat.search(line)]
        if not kinds: continue
        lo=max(1,i-5);hi=min(len(lines),i+8)
        context='\n'.join(f'{j}: {lines[j-1]}' for j in range(lo,hi+1))
        rows.append({'path':p.relative_to(root).as_posix(),'line':i,'kinds':kinds,'text':line.strip(),'context':context})

# Compact exact source excerpts: all network calls plus neighborhoods around
# fill_params and assignments to T/a in bbn.c.
selected=[]
for r in rows:
    if {'network_call','fill_params_call','state_update','linearize'} & set(r['kinds']):
        selected.append(r)

h=hashlib.sha256()
for p in candidates:
    h.update(p.relative_to(root).as_posix().encode()+b'\0'+hashlib.sha256(p.read_bytes()).digest())
summary={
 'classification':'ALTERBBN_V2_2_INTEGRATION_FLOW_AUDIT_PASS',
 'source_digest_sha256':h.hexdigest(),
 'files':[p.relative_to(root).as_posix() for p in candidates],
 'counts':{k:sum(k in r['kinds'] for r in rows) for k in patterns},
 'selected_contexts':selected,
 'all_matches':rows,
 'next_gate':'instrument accepted integration state or deterministically isolate central solve using exact source call order',
 'warning':'Structural source audit only.'
}
Path('alterbbn_integration_flow_audit.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_V2_2_INTEGRATION_FLOW_AUDIT_PASS',json.dumps({k:v for k,v in summary.items() if k not in ('selected_contexts','all_matches')},sort_keys=True))
for r in selected:
    print('ALTERBBN_FLOW_CONTEXT',json.dumps(r,sort_keys=True))
