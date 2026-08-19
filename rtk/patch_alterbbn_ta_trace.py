#!/usr/bin/env python3
"""Instrument pinned AlterBBN v2.2 with an accepted-state T-a trace.

Protocol v1.1: assign a nucl_single call serial at entry and write diagnostics
only in the accepted stiff-step block used by failsafe=1.  No variable entering
the network is changed.
"""
from pathlib import Path
import hashlib,json,re,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
p=root/'src/bbn.c'
text=p.read_text();orig=text.encode()

# Insert call serial / trace handle in nucl_single, independent of formatting of
# the long function signature.
m=re.search(r'int\s+nucl_single\s*\([^\)]*\)\s*\n[^\{]*\{',text,re.S)
if not m: raise RuntimeError('nucl_single definition not found')
entry_insert=r'''

	/* RTK_BBN_TA_TRACE_V1_1: diagnostic-only accepted-state trace. */
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

# The first integration branch is the failsafe<20 stiff method.  Restrict the
# accepted-state insertion to that branch so trial/rejected states are never
# observed for stand_cosmo.x 1.
branch_marker='else if(paramrelic->failsafe<20) /* Runge-Kutta method of order 4 with adaptative stepsize */'
cut=text.find(branch_marker)
if cut<0: raise RuntimeError('failsafe<20 branch marker not found')
prefix,suffix=text[:cut],text[cut:]
accepted=r'''if(test==0&&test_precision==0)
			{
				T=T2;
				h_eta=h_eta2;
				phie=phie2;
				Tnu=Tnu2;
				a=a2;'''
if prefix.count(accepted)!=1:
    raise RuntimeError(f'expected one accepted stiff-step block before RK branch, found {prefix.count(accepted)}')
trace_write=r'''

				/* Accepted solver state only; diagnostic write cannot affect dynamics. */
				if(rtk_ta_trace != NULL)
				{
					fprintf(rtk_ta_trace,"%lu\t%d\t%.17g\t%.17g\n",rtk_trace_call_serial,paramrelic->err,T,a);
					fflush(rtk_ta_trace);
				}'''
prefix=prefix.replace(accepted,accepted+trace_write,1)
patched=prefix+suffix

# Fail closed if an obsolete RHS-level marker somehow remains.
if 'RTK_BBN_TA_TRACE_V1:' in patched:
    raise RuntimeError('legacy RHS trace marker remains')
if patched.count('RTK_BBN_TA_TRACE_V1_1')!=1:
    raise RuntimeError('accepted-state trace entry marker count mismatch')
if patched.count('Accepted solver state only')!=1:
    raise RuntimeError('accepted-state trace write marker count mismatch')

p.write_text(patched)
manifest={
 'classification':'ALTERBBN_ACCEPTED_TA_TRACE_INSTRUMENTATION_PATCH_APPLIED',
 'protocol':'RTK_BBN_HT_MAPPING_PROTOCOL_v1_1_TRACE_FIX',
 'path':'src/bbn.c','entry_marker':'RTK_BBN_TA_TRACE_V1_1','accepted_write_marker':'Accepted solver state only',
 'original_sha256':hashlib.sha256(orig).hexdigest(),
 'patched_sha256':hashlib.sha256(patched.encode()).hexdigest(),
 'semantic_rule':'records call serial, err, T and a only after a failsafe<20 step passes test==0 && test_precision==0; no network state assignment by instrumentation'
}
Path('alterbbn_ta_trace_patch_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_ACCEPTED_TA_TRACE_INSTRUMENTATION_PATCH_APPLIED',json.dumps(manifest,sort_keys=True))
