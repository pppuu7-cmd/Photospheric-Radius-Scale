#!/usr/bin/env python3
"""Instrument pinned AlterBBN v2.2 with a failsafe=1 accepted-state T-a trace.

Protocol v1.2: assign a nucl_single call serial at entry and write diagnostics
only after the corrected loop==2 state of the actual failsafe<5 integration
branch used by stand_cosmo.x 1. No variable entering the network is changed.
"""
from pathlib import Path
import hashlib,json,re,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
p=root/'src/bbn.c'
text=p.read_text();orig=text.encode()

m=re.search(r'int\s+nucl_single\s*\([^\)]*\)\s*\n[^\{]*\{',text,re.S)
if not m: raise RuntimeError('nucl_single definition not found')
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
# in the first `failsafe<5` predictor/corrector branch, not in the later
# adaptive failsafe<10 branch. Restrict the search to that exact source region.
branch_start=text.find('if(paramrelic->failsafe<5) /* Original order 2 method for stiff equations */')
branch_end=text.find('else if(paramrelic->failsafe<10) /* Original order 2 method for stiff equations with improved adaptative timestep */')
if branch_start<0 or branch_end<0 or branch_end<=branch_start:
    raise RuntimeError('failsafe<5 / failsafe<10 branch boundaries not found as expected')
prefix=text[:branch_start];branch=text[branch_start:branch_end];suffix=text[branch_end:]

corrected_tail=r'''					for (i=1;i<=NNUC;i++)
					{
						Y[i]=Y0[i]+(dY_dt[i]+dY_dt0[i])*0.5*dt;
						if (Y[i]<Ytmin) Y[i]=Ytmin;
					}

#ifdef OUTPUT'''
if branch.count(corrected_tail)!=1:
    raise RuntimeError(f'expected exactly one failsafe<5 corrected loop==2 tail, found {branch.count(corrected_tail)}')
trace_write=r'''					for (i=1;i<=NNUC;i++)
					{
						Y[i]=Y0[i]+(dY_dt[i]+dY_dt0[i])*0.5*dt;
						if (Y[i]<Ytmin) Y[i]=Ytmin;
					}

					/* RTK_BBN_FAILSAFE1_CORRECTED_STATE: observe only, never mutate. */
					if(rtk_ta_trace != NULL)
					{
						fprintf(rtk_ta_trace,"%lu\t%d\t%.17g\t%.17g\n",rtk_trace_call_serial,paramrelic->err,T,a);
						fflush(rtk_ta_trace);
					}

#ifdef OUTPUT'''
branch=branch.replace(corrected_tail,trace_write,1)
patched=prefix+branch+suffix

if 'RTK_BBN_TA_TRACE_V1:' in patched or 'RTK_BBN_TA_TRACE_V1_1' in patched:
    raise RuntimeError('obsolete trace marker remains')
if patched.count('RTK_BBN_TA_TRACE_V1_2')!=1:
    raise RuntimeError('v1.2 trace entry marker count mismatch')
if patched.count('RTK_BBN_FAILSAFE1_CORRECTED_STATE')!=1:
    raise RuntimeError('failsafe=1 corrected-state write marker count mismatch')
# Ensure no diagnostic assignment targets any physical state variable.
inserted=trace_write[len(corrected_tail.split('#ifdef OUTPUT')[0]):] if False else trace_write
for forbidden in ('T=','a=','dt=','Y['):
    # The replacement includes the original physical corrected-state code, so
    # audit the diagnostic block only rather than the whole replacement.
    diag=trace_write.split('/* RTK_BBN_FAILSAFE1_CORRECTED_STATE:',1)[1]
    if forbidden in diag:
        raise RuntimeError(f'diagnostic block unexpectedly assigns/contains forbidden token {forbidden!r}')

p.write_text(patched)
manifest={
 'classification':'ALTERBBN_FAILSAFE1_ACCEPTED_TA_TRACE_PATCH_APPLIED',
 'protocol':'RTK_BBN_HT_MAPPING_PROTOCOL_v1_2_FAILSAFE1_TRACE_FIX',
 'path':'src/bbn.c','entry_marker':'RTK_BBN_TA_TRACE_V1_2','accepted_write_marker':'RTK_BBN_FAILSAFE1_CORRECTED_STATE',
 'original_sha256':hashlib.sha256(orig).hexdigest(),
 'patched_sha256':hashlib.sha256(patched.encode()).hexdigest(),
 'semantic_rule':'for the actual failsafe<5 branch used by failsafe=1, record call serial, err, corrected T and corrected a only after loop==2 updates T,a,Tnu,Y; diagnostic block performs no state assignment'
}
Path('alterbbn_ta_trace_patch_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_FAILSAFE1_ACCEPTED_TA_TRACE_PATCH_APPLIED',json.dumps(manifest,sort_keys=True))
