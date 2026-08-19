#!/usr/bin/env python3
"""Inspect a pinned extracted AlterBBN tree for H(T)/alternative-cosmology hooks.

This is a structural source audit only. It does not modify AlterBBN and does not
claim BBN consistency. The output is meant to identify the narrowest auditable
injection point for a tabulated RTK expansion history.
"""
from pathlib import Path
import hashlib,json,re,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
if not root.is_dir(): raise SystemExit(f'missing AlterBBN tree: {root}')

patterns={
 'dark_density':re.compile(r'\bdark_density\b'),
 'dark_entropy':re.compile(r'\bdark_entropy\b'),
 'dark_entropy_derivative':re.compile(r'\bdark_entropy_derivative\b'),
 'dark_entropy_Sigmad':re.compile(r'\bdark_entropy_Sigmad\b'),
 'relicparam':re.compile(r'\brelicparam\b'),
 'hubble_symbol':re.compile(r'\bH\b|Hubble|hubble',re.I),
 'friedmann_sqrt':re.compile(r'sqrt\s*\([^\n;]*(?:G|rho|density)',re.I),
 'rho_tot':re.compile(r'rho[_A-Za-z0-9]*tot|rho_tot',re.I),
 'Init_dark_density':re.compile(r'\bInit_dark_density\b'),
}

suffixes={'.c','.h','.cpp','.hpp'}
files=sorted(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in suffixes)
rows=[]
for p in files:
    try: lines=p.read_text(errors='replace').splitlines()
    except Exception: continue
    for i,line in enumerate(lines,1):
        kinds=[k for k,pat in patterns.items() if pat.search(line)]
        if not kinds: continue
        lo=max(1,i-2);hi=min(len(lines),i+2)
        context='\n'.join(f'{j}: {lines[j-1]}' for j in range(lo,hi+1))
        rows.append({'path':p.relative_to(root).as_posix(),'line':i,'kinds':kinds,'text':line.strip(),'context':context})

by_kind={k:[] for k in patterns}
for r in rows:
    for k in r['kinds']: by_kind[k].append({'path':r['path'],'line':r['line'],'text':r['text']})

# Fail closed on the public alternative-cosmology API that should exist in v2.2.
required=('relicparam','dark_density','Init_dark_density')
missing=[k for k in required if not by_kind[k]]
if missing: raise RuntimeError(f'expected AlterBBN v2.2 expansion hooks missing: {missing}')

# Digest only the inspected source files so the structural result is tied to bytes.
h=hashlib.sha256()
for p in files:
    rel=p.relative_to(root).as_posix();b=p.read_bytes()
    h.update(rel.encode()+b'\0'+hashlib.sha256(b).digest())

summary={
 'classification':'ALTERBBN_V2_2_EXPANSION_INTERFACE_AUDIT_PASS',
 'inspected_source_files':len(files),
 'inspected_source_digest_sha256':h.hexdigest(),
 'required_hooks':required,
 'match_counts':{k:len(v) for k,v in by_kind.items()},
 'matches_by_kind':by_kind,
 'all_context_matches':rows,
 'next_gate':'select_minimal_tabulated_RTK_H_over_Href_injection_point_before_modification',
 'warning':'Structural source audit only; no AlterBBN source modification, abundance result, or observational claim.'
}
Path('alterbbn_expansion_interface_audit.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_V2_2_EXPANSION_INTERFACE_AUDIT_PASS',json.dumps({k:v for k,v in summary.items() if k not in ('matches_by_kind','all_context_matches')},sort_keys=True))
