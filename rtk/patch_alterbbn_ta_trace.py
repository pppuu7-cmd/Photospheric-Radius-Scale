#!/usr/bin/env python3
"""Mechanically instrument pinned AlterBBN v2.2 with a T-a-H trace.

The inserted code writes diagnostics only after the unmodified standard Hubble
rate is computed. No variable entering the network is changed.
"""
from pathlib import Path
import hashlib,json,sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'alterbbn_v2.2')
p=root/'src/bbn.c'
text=p.read_text()
needle='\tdouble H=sqrt(G*8.*pi/3.*(rho_gamma+rho_epem+rho_wimp+rho_neutrinos+rho_neuteq+rho_baryons+rho_cdm+rhod+rho_phi));'
if text.count(needle)!=1:
    raise RuntimeError(f'expected exactly one standard Hubble line, found {text.count(needle)}')
insert=r'''

	/* RTK_BBN_TA_TRACE_V1: diagnostic-only instrumentation; H is unchanged. */
	{
		static FILE *rtk_ta_trace = NULL;
		static double rtk_last_logT = 1.e300;
		double rtk_logT = log(T);
		if(rtk_ta_trace == NULL)
		{
			rtk_ta_trace = fopen("rtk_bbn_Ta_trace.tsv","w");
			if(rtk_ta_trace != NULL) fprintf(rtk_ta_trace,"# T_internal\ta_internal\tH_standard\n");
		}
		if(rtk_ta_trace != NULL && (rtk_last_logT > 1.e200 || fabs(rtk_logT-rtk_last_logT) >= 2.e-5))
		{
			fprintf(rtk_ta_trace,"%.17g\t%.17g\t%.17g\n",T,a,H);
			fflush(rtk_ta_trace);
			rtk_last_logT = rtk_logT;
		}
	}
'''
orig=text.encode();patched=text.replace(needle,needle+insert,1)
p.write_text(patched)
manifest={
 'classification':'ALTERBBN_TA_TRACE_INSTRUMENTATION_PATCH_APPLIED',
 'path':'src/bbn.c','marker':'RTK_BBN_TA_TRACE_V1','replacement_count':1,
 'original_sha256':hashlib.sha256(orig).hexdigest(),
 'patched_sha256':hashlib.sha256(patched.encode()).hexdigest(),
 'semantic_rule':'diagnostic write occurs after H assignment and does not assign to T,a,H or network state'
}
Path('alterbbn_ta_trace_patch_manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print('ALTERBBN_TA_TRACE_INSTRUMENTATION_PATCH_APPLIED',json.dumps(manifest,sort_keys=True))
