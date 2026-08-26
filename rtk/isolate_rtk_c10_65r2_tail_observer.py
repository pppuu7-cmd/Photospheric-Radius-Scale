#!/usr/bin/env python3
"""C10.65r2f: move the existing r2 diagnostic observer to the r1 output tail.

Apply after apply_rtk_c10_65r2_in_class_first_rhs_diagnostic_patch.py and before
fix_rtk_c10_65r2_shear_units.py.  This script changes no r2 arithmetic.  It
only (1) removes the already-audited all-history fatal finiteness abort and
(2) relocates the whole dormant observer block until after every r1 value has
already been stored.  The base r2 patch's original title order is r1 then r2,
which therefore matches the resulting store order; do NOT apply the old
column-order patch after this transform.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
p=root/'source'/'perturbations.c'
s=p.read_text()
marker='RTK_C10_65R2_TAIL_OBSERVER_ISOLATION_V1'
if marker in s:
    print('C10_65R2_TAIL_OBSERVER_ALREADY_ISOLATED')
    raise SystemExit(0)
if 'RTK_C10_65R2_IN_CLASS_FIRST_RHS_DIAGNOSTIC_V1' not in s:
    raise SystemExit('apply the base C10.65r2 patch first')

finite_guard='''          class_test(!isfinite(r2_B0.v)||!isfinite(r2_B0.d)||!isfinite(r2_Ba.d)||!isfinite(r2_Psip)||!isfinite(r2_slip)\n            ||!isfinite(r2_thbp)||!isfinite(r2_thgp)||!isfinite(r2_thurp)||!isfinite(r2_dkp)||!isfinite(r2_thkp),error_message,"C10.65r2 non-finite shadow first RHS");\n'''
if finite_guard not in s:
    raise SystemExit('r2 all-history finiteness guard anchor missing')
s=s.replace(finite_guard,'',1)

start_token='        if (pba->c10_65r2_diag > 0.5) {'
start=s.find(start_token)
if start<0 or s.find(start_token,start+1)>=0:
    raise SystemExit('expected exactly one r2 observer block')

def matching_brace(text, open_pos):
    depth=0; i=open_pos; quote=None; line_comment=False; block_comment=False; esc=False
    while i<len(text):
        c=text[i]; n=text[i+1] if i+1<len(text) else ''
        if line_comment:
            if c=='\n': line_comment=False
            i+=1; continue
        if block_comment:
            if c=='*' and n=='/': block_comment=False; i+=2; continue
            i+=1; continue
        if quote is not None:
            if esc: esc=False
            elif c=='\\': esc=True
            elif c==quote: quote=None
            i+=1; continue
        if c=='/' and n=='/': line_comment=True; i+=2; continue
        if c=='/' and n=='*': block_comment=True; i+=2; continue
        if c in ('"',"'"): quote=c; i+=1; continue
        if c=='{': depth+=1
        elif c=='}':
            depth-=1
            if depth==0: return i
        i+=1
    raise RuntimeError('unbalanced r2 observer block')

open_pos=s.find('{',start)
end_brace=matching_brace(s,open_pos)
end=end_brace+1
if end<len(s) and s[end]=='\n': end+=1
block=s[start:end]
# Guard on actual observer arithmetic/store symbols, not output-title strings
# (the titles live in a different code section).
if 'r2_B0=rtk_c10_65r2_general_B' not in block or 'class_store_double(dataptr,r2_cancel' not in block:
    raise SystemExit('captured r2 observer block failed content guard')

s=s[:start]+s[end:]
anchor='        class_store_double(dataptr,r1_feedback,_TRUE_,storeidx);'
pos=s.find(anchor)
if pos<0 or s.find(anchor,pos+1)>=0:
    raise SystemExit('expected exactly one r1 final-store anchor')
insert=pos+len(anchor)
s=s[:insert]+'\n        /* '+marker+': r1 output is fully materialized before dormant r2 observer. */\n'+block+s[insert:]

p.write_text(s)
print('C10_65R2_TAIL_OBSERVER_ISOLATED')
