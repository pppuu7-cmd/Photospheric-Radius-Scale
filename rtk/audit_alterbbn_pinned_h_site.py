#!/usr/bin/env python3
"""Audit exact Friedmann-H and final-temperature sites in a pinned AlterBBN tree."""
from pathlib import Path
import hashlib,json,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
p=root/'src/bbn.c'
text=p.read_text();lines=text.splitlines()
expected=('rho_gamma','rho_epem','rho_wimp','rho_neutrinos','rho_neuteq','rho_baryons','rhod')
hits=[]
for i,line in enumerate(lines):
    q=''.join(line.split())
    if 'H=' in q and 'sqrt(' in q and all(x in q for x in expected): hits.append(i)
if not hits: raise RuntimeError('no Friedmann H density-sum assignment found')
rows=[]
for i in hits:
    lo=max(0,i-80);hi=min(len(lines),i+21)
    ctx='\n'.join(f'{j+1}: {lines[j]}' for j in range(lo,hi))
    rows.append({'line_number_1based':i+1,'line':lines[i],'context':ctx})
call_hits=[]
for i,line in enumerate(lines):
    if 'fill_params' in line:
        lo=max(0,i-4);hi=min(len(lines),i+5)
        call_hits.append({'line_number_1based':i+1,'context':'\n'.join(f'{j+1}: {lines[j]}' for j in range(lo,hi))})
tf_hits=[]
for i,line in enumerate(lines):
    # Keep exact source context for every Tf token, including initialization and stop test.
    if 'Tf' in line:
        lo=max(0,i-5);hi=min(len(lines),i+6)
        tf_hits.append({'line_number_1based':i+1,'line':line,'context':'\n'.join(f'{j+1}: {lines[j]}' for j in range(lo,hi))})
out={'classification':'ALTERBBN_PINNED_FRIEDMANN_H_SITE_AUDIT_COMPLETE','bbn_c_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'friedmann_hits':rows,'fill_params_mentions':call_hits,'Tf_mentions':tf_hits}
Path('alterbbn_pinned_h_site_audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_PINNED_FRIEDMANN_H_SITE_AUDIT_COMPLETE',json.dumps({'bbn_c_sha256':out['bbn_c_sha256'],'friedmann_hit_count':len(rows),'fill_params_mention_count':len(call_hits),'Tf_mention_count':len(tf_hits)},sort_keys=True))
