#!/usr/bin/env python3
"""Instrument pinned AlterBBN v2.2 with a failsafe=1 accepted-state T-a trace.

Protocol v1.2: assign a nucl_single call serial at entry and write diagnostics
only after the corrected loop==2 state of the actual failsafe<5 integration
branch used by stand_cosmo.x 1. No variable entering the network is changed.

The patch is intentionally structural rather than indentation-literal: the
published v2.2 source uses mixed tab/space formatting around the corrected
abundance block. We therefore anchor on the exact failsafe branch and the
unique loop==2 abundance update semantics, then insert diagnostics *after* the
matched original block without replacing any physical-state statements.
"""
from pathlib import Path
import hashlib,json,re,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
p=root/'src/bbn.c'
text=p.read_text();orig=text.encode()

m=re.search(r'int\s+nucl_single\s*\([^\)]*\)\s*\n[^\{]*\{',text,re.S)
if not m:
    raise RuntimeError('nucl_single definition not found')
entry_insert=r'''

	/* RTK_BBN_TA_TRACE_V1_2: diagnostic-only failsafe=1 corrected-state trace. */
	static unsigned long rtk_trace_call_serial_global = 0;
	unsigned long rtk_trace_call_serial = ++rtk_trace_call_serial_global;
	static FILE *rtk_ta_trace = NULL;
	if(rtk_ta_trace == NULL)
	{
		rtk_ta_trace = fopen("rtk_bbn_Ta_trace.tsv","w");
		if(rtk_ta_trace != NULL)
			fprintf(rtk_ta_trace,"# call_id\terr\tT_internal\ta_internal\n");
	}
'''
text=text[:m.end()]+entry_insert+text[m.end():]

# stand_cosmo.x 1 uses failsafe=1, therefore the accepted observation point is
# in the first failsafe<5 predictor/corrector branch. Restrict every following
# source match to this exact region; never fall through to the adaptive branches.
branch_start=text.find('if(paramrelic->failsafe<5) /* Original order 2 method for stiff equations */')
branch_end=text.find('else if(paramrelic->failsafe<10) /* Original order 2 method for stiff equations with improved adaptative timestep */')
if branch_start<0 or branch_end<0 or branch_end<=branch_start:
    raise RuntimeError('failsafe<5 / failsafe<10 branch boundaries not found as expected')
prefix=text[:branch_start];branch=text[branch_start:branch_end];suffix=text[branch_end:]

# Unique corrected loop==2 abundance block from pinned AlterBBN v2.2.  Match
# semantics with whitespace tolerance, and require #ifdef OUTPUT immediately
# after optional whitespace. This distinguishes it from the predictor loop==1
# block above and from other abundance loops in later failsafe branches.
corrected_re=re.compile(
    r'(?P<indent>^[ \t]*)for\s*\(i=1;i<=NNUC;i\+\+\)\s*\n'
    r'(?P=indent)\{\s*\n'
    r'(?P=indent)[ \t]+Y\[i\]=Y0\[i\]\+\(dY_dt\[i\]\+dY_dt0\[i\]\)\*0\.5\*dt;\s*\n'
    r'(?P=indent)[ \t]+if\s*\(Y\[i\]<Ytmin\)\s*Y\[i\]=Ytmin;\s*\n'
    r'(?P=indent)\}',
    re.M,
)
matches=list(corrected_re.finditer(branch))
# Keep only the candidate whose immediate successor is the OUTPUT block.
accepted=[]
for mm in matches:
    tail=branch[mm.end():]
    if re.match(r'\s*#ifdef\s+OUTPUT\b',tail):
        accepted.append(mm)
if len(accepted)!=1:
    raise RuntimeError(
        f'expected exactly one failsafe<5 corrected loop==2 abundance block before OUTPUT, found {len(accepted)} '
        f'(semantic abundance matches={len(matches)})'
    )
mm=accepted[0]
matched_block=mm.group(0)
indent=mm.group('indent')
# Source sanity: corrected T/a/Tnu updates must precede the accepted abundance
# block within the same loop==2 branch.
pre=branch[:mm.start()]
for anchor in (
    'T=T0+(dT_dt+dT0_dt)*0.5*dt;',
    'a=a0+(da_dt+da_dt0)*0.5*dt;',
    'Tnu=Tnu0+(dTnu_dt+dTnu0_dt)*0.5*dt;',
):
    if pre.rfind(anchor)<0:
        raise RuntimeError(f'corrected-state anchor missing before abundance block: {anchor}')

trace_write=(
    '\n\n'+indent+'/* RTK_BBN_FAILSAFE1_CORRECTED_STATE: observe only, never mutate. */\n'
    +indent+'if(rtk_ta_trace != NULL)\n'
    +indent+'{\n'
    +indent+'\tfprintf(rtk_ta_trace,"%lu\\t%d\\t%.17g\\t%.17g\\n",rtk_trace_call_serial,paramrelic->err,T,a);\n'
    +indent+'\tfflush(rtk_ta_trace);\n'
    +indent+'}'
)
# Insert only; do not rewrite the matched original physical update block.
branch=branch[:mm.end()]+trace_write+branch[mm.end():]
patched=prefix+branch+suffix

if 'RTK_BBN_TA_TRACE_V1:' in patched or 'RTK_BBN_TA_TRACE_V1_1' in patched:
    raise RuntimeError('obsolete trace marker remains')
if patched.count('RTK_BBN_TA_TRACE_V1_2')!=1:
    raise RuntimeError('v1.2 trace entry marker count mismatch')
if patched.count('RTK_BBN_FAILSAFE1_CORRECTED_STATE')!=1:
    raise RuntimeError('failsafe=1 corrected-state write marker count mismatch')
# Diagnostic block must not assign physical state. The only '=' tokens allowed
# are the NULL comparison and ordinary function arguments contain no assignment.
diag=trace_write.split('/* RTK_BBN_FAILSAFE1_CORRECTED_STATE:',1)[1]
for forbidden in ('T=','a=','dt=','Y[','h_eta=','phie=','Tnu=','rho_phi='):
    if forbidden in diag:
        raise RuntimeError(f'diagnostic block unexpectedly contains forbidden token {forbidden!r}')
# Prove the original physical abundance block survived byte-for-byte.
if matched_block not in patched:
    raise RuntimeError('original corrected abundance block was not preserved verbatim')

p.write_text(patched)
manifest={
 'classification':'ALTERBBN_FAILSAFE1_ACCEPTED_TA_TRACE_PATCH_APPLIED',
 'protocol':'RTK_BBN_HT_MAPPING_PROTOCOL_v1_2_FAILSAFE1_TRACE_FIX',
 'path':'src/bbn.c',
 'entry_marker':'RTK_BBN_TA_TRACE_V1_2',
 'accepted_write_marker':'RTK_BBN_FAILSAFE1_CORRECTED_STATE',
 'original_sha256':hashlib.sha256(orig).hexdigest(),
 'matched_corrected_block_sha256':hashlib.sha256(matched_block.encode()).hexdigest(),
 'matched_corrected_block_preserved_verbatim':True,
 'patched_sha256':hashlib.sha256(patched.encode()).hexdigest(),
 'semantic_rule':'within pinned failsafe<5 branch, uniquely match loop==2 Y correction immediately before OUTPUT; insert call serial/err/T/a trace after corrected T,a,Tnu,Y updates; diagnostic block performs no state assignment'
}
Path('alterbbn_ta_trace_patch_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_FAILSAFE1_ACCEPTED_TA_TRACE_PATCH_APPLIED',json.dumps(manifest,sort_keys=True))
