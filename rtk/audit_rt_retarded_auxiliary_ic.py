#!/usr/bin/env python3
"""Fail-closed source audit for the minimal causal RT auxiliary-field initial data.

This is an implementation/reproducibility invariant, not a full nonlinear DOF theorem.
It expects the pinned nonlocal CLASS tree after
upgrade_rtk_nonlocal_initial_conditions.py has been applied.
"""
from pathlib import Path
import json, re, sys

root=Path(sys.argv[1] if len(sys.argv)>1 else 'class_public')
input_c=(root/'source/input.c').read_text()
pert_c=(root/'source/perturbations.c').read_text()
bg_c=(root/'source/background.c').read_text()
bg_h=(root/'include/background.h').read_text()

checks={}
def require(name, cond, detail):
    if not cond:
        raise SystemExit(f'RTK_RETARDED_AUX_IC_AUDIT_FAIL {name}: {detail}')
    checks[name]=True

# Background minimal homogeneous solution must be explicit, exactly once each
# in the audited input block. This removes dependence on uninitialized storage.
for field in ('U_ini_nlde','U_prime_ini_nlde','V_ini_nlde','V_prime_ini_nlde'):
    pat=rf'pba->{field}\s*=\s*0\.;'
    require('background_'+field, len(re.findall(pat,input_c))==1,
            f'expected exactly one explicit {field}=0 assignment')

require('no_duplicate_Uprime_background_ic',
        len(re.findall(r'pba->U_prime_ini_nlde\s*=\s*0\.;',input_c))==1,
        'upstream copy/paste duplicate U_prime assignment must be removed')
require('Vprime_declared', 'double V_prime_ini_nlde' in bg_h,
        'V_prime_ini_nlde must be an explicit background field')
require('Vprime_consumed_by_background',
        'pba->V_prime_ini_nlde' in bg_c and 'index_bi_V_prime_nlde' in bg_c,
        'background evolution must consume the explicitly initialized V prime')

# The pinned adiabatic nonlocal perturbation IC block uses a nested workspace
# index, e.g. ppw->pv->y[ppw->pv->index_pt_deltaU_nlde] = 0.; . Require the
# exact audited direct-zero statements instead of guessing a simplified index
# syntax. This remains fail-closed if upstream changes the implementation.
common_zero_snippets={
 'deltaU':'ppw->pv->y[ppw->pv->index_pt_deltaU_nlde] = 0.;',
 'deltaUprime':'ppw->pv->y[ppw->pv->index_pt_deltaU_prime_nlde] = 0.;',
 'deltaV':'ppw->pv->y[ppw->pv->index_pt_deltaV_nlde] = 0.;',
 'deltaVprime':'ppw->pv->y[ppw->pv->index_pt_deltaV_prime_nlde] = 0.;',
}
for name,snippet in common_zero_snippets.items():
    require('perturbation_'+name+'_zero', pert_c.count(snippet)==1,
            f'expected exact pinned zero assignment once: {snippet}')

rt_block='''if(pba->model == 2.){
              ppw->pv->y[ppw->pv->index_pt_deltaZ_nlde] = 0.;
              ppw->pv->y[ppw->pv->index_pt_deltaZ_prime_nlde] = 0.;
          }'''
require('rt_model2_Z_Zprime_zero_block', pert_c.count(rt_block)==1,
        'RT/model-2 deltaZ and deltaZ_prime must both be explicitly zero in the adiabatic IC block')

# Also require the indices themselves are allocated only inside the RT/model-2
# condition, preventing accidental use of Z auxiliaries as generic RR fields.
allocation_block='''if(pba->model == 2.){
            class_define_index(ppv->index_pt_deltaZ_nlde,pba->has_nlde,index_pt,1);
            class_define_index(ppv->index_pt_deltaZ_prime_nlde,pba->has_nlde,index_pt,1);'''
require('rt_model2_Z_index_allocation', allocation_block in pert_c,
        'RT Z auxiliary perturbation indices must be allocated in model==2 branch')

result={
 'classification':'RTK_RETARDED_AUX_IC_IMPLEMENTATION_PASS',
 'background_zero_fields':['U','U_prime','V','V_prime'],
 'perturbation_zero_fields':['deltaU','deltaU_prime','deltaV','deltaV_prime','deltaZ','deltaZ_prime'],
 'model':'RT/model=2',
 'claim_boundary':'implementation-level minimal causal auxiliary IC invariant; not a full nonlinear RT physical-DOF proof',
 'checks':sorted(checks),
}
print('RTK_RETARDED_AUX_IC_AUDIT_PASS',json.dumps(result,sort_keys=True))
